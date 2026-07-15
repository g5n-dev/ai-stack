from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from ai_stack.content_quality import analyze_post, markdown_body, markdown_frontmatter
from ai_stack.historical_repair import build_historical_repair_plan
from ai_stack.migrations import MigrationSafetyError
from scripts.repair_historical_content import build_parser

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAFE_DESCRIPTION = "该摘要来自当前条目元数据，用于验证固定 Git blob 的历史正文恢复。"
COMPLETE_BODY = (
    "## 摘要\n\n"
    "这是历史提交中保存完整的正文，包含可核验的工程事实、运行约束、失败证据和"
    "闭合结论。恢复流程只能读取清单固定的 Git blob，不能根据当前残缺内容推测或"
    "生成任何缺失段落。\n\n"
    "## 结论\n\n历史版本的最后一句具有完整标点。"
)
NORMALIZABLE_BODY = (
    "# 历史源标题\n\n"
    "## 引言\n\n"
    "这里为您撰写了一个极具吸引力的引言，融合工程冲突与悬念：\n\n"
    "**【引言】**\n\n"
    "真实正文记录了已有日志、边界条件和最终结论。这些内容来自固定历史 blob，"
    "恢复时必须完整保留，并由现有规范化流程清理重复标题与助手前导语。\n\n"
    "## 结论\n\n现有证据支持这一完整结论。"
)
TRUNCATED_BODY = (
    "## 摘要\n\n"
    "这段 Hacker News 历史正文在引用之前突然停止，最后一个技术判断包含足够长的"
    "中文内容但没有形成闭合句子并且仍然停留在未完成的推理链条中，\n\n"
    "## 🔗 引用\n\n- [原始来源](https://example.com/source)"
)


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _write_post(
    path: Path,
    *,
    external_url: str,
    title: str,
    body: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, object] = {
        "title": title,
        "description": SAFE_DESCRIPTION,
        "date": "2026-01-01T00:00:00+08:00",
        "draft": False,
        "source": "hacker_news",
        "external_url": external_url,
        "tags": ["AI 工程"],
        "categories": ["AI 工程"],
        "scenarios": ["AI/ML项目"],
        "entry_kind": "auto",
        "content_mode": "legacy_analysis",
        "publication_tier": "LEGACY",
        "source_provenance": "legacy_no_snapshot",
        "source_support": 0.0,
    }
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    path.write_text(f"---\n{frontmatter}\n---\n\n{body.strip()}\n", encoding="utf-8")


def _commit(repo: Path, message: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _fixture(
    tmp_path: Path,
    *,
    same_path: bool,
    source_body: str = COMPLETE_BODY,
    source_payload: bytes | None = None,
    source_external_url: str | None = None,
) -> tuple[Path, Path, Path, dict[str, Any]]:
    repo = tmp_path / "repo"
    content_root = repo / "blog/content/posts"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "Historical Repair Test")
    _git(repo, "config", "user.email", "historical-repair@example.com")

    canonical_url = "https://example.com/pinned-history"
    source_name = "target.md" if same_path else "historical-sibling.md"
    source = content_root / source_name
    if source_payload is None:
        _write_post(
            source,
            external_url=source_external_url or canonical_url,
            title="历史源标题",
            body=source_body,
        )
    else:
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(source_payload)
    source_commit = _commit(repo, "complete historical source")
    source_repo_path = source.relative_to(repo).as_posix()
    source_git_blob = _git(repo, "rev-parse", f"{source_commit}:{source_repo_path}")
    source_payload = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "blob", source_git_blob],
        check=True,
        capture_output=True,
    ).stdout

    target = content_root / "target.md"
    if not same_path:
        source.unlink()
    _write_post(
        target,
        external_url=canonical_url,
        title="当前目标标题",
        body=TRUNCATED_BODY,
    )
    _commit(repo, "current truncated target")
    target_payload = target.read_bytes()

    audit_payload = {
        "schema_version": "historical_git_recovery_audit_v1",
        "fixture": "pinned Git recovery audit",
    }
    audit_bytes = (
        json.dumps(audit_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()
    manifest_data: dict[str, Any] = {
        "schema_version": "historical_git_recovery_manifest_v1",
        "audit_path": "historical-post-recovery-audit-v1.json",
        "audit_sha256": hashlib.sha256(audit_bytes).hexdigest(),
        "entry_count": 1,
        "entries": [
            {
                "target_path": target.relative_to(content_root).as_posix(),
                "target_file_sha256": hashlib.sha256(target_payload).hexdigest(),
                "canonical_url": canonical_url,
                "recovery_basis": "detected_truncation",
                "source_commit": source_commit,
                "source_path": source_repo_path,
                "source_git_blob": source_git_blob,
                "source_file_sha256": hashlib.sha256(source_payload).hexdigest(),
            }
        ],
    }
    manifest = repo / "config/historical-post-recovery-v1.json"
    manifest.parent.mkdir()
    (manifest.parent / manifest_data["audit_path"]).write_bytes(audit_bytes)
    manifest.write_text(
        json.dumps(manifest_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return content_root, target, manifest, manifest_data


def _write_manifest(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _rendered(plan, target_name: str) -> str:
    return next(write.content for write in plan.writes if write.path == target_name).decode()


def test_git_recovery_is_explicit_and_normalizes_a_pinned_same_path_blob(
    tmp_path: Path,
) -> None:
    root, target, manifest, data = _fixture(
        tmp_path,
        same_path=True,
        source_body=NORMALIZABLE_BODY,
    )

    default_plan = build_historical_repair_plan(content_root=root)
    assert default_plan.manifest["groups"][0]["disposition"] == "archive_stub"

    plan = build_historical_repair_plan(
        content_root=root,
        recovery_manifest_path=manifest,
    )
    rendered = _rendered(plan, target.name)
    group = plan.manifest["groups"][0]

    assert markdown_frontmatter(rendered)["title"] == "当前目标标题"
    assert "真实正文记录了已有日志" in markdown_body(rendered)
    assert "这里为您撰写" not in rendered
    assert "# 历史源标题" not in rendered
    assert analyze_post(rendered).fatal_reasons == ()
    assert group["integrity_decision"] == {
        "action": "restore_from_git_history",
        "failed_paths": [target.name],
        "failure_reasons": ["truncated_pre_citation_tail"],
        "recovery_basis": "detected_truncation",
        "source_commit": data["entries"][0]["source_commit"],
        "source_file_sha256": data["entries"][0]["source_file_sha256"],
        "source_git_blob": data["entries"][0]["source_git_blob"],
        "source_path": data["entries"][0]["source_path"],
        "target_file_sha256": data["entries"][0]["target_file_sha256"],
    }
    assert "真实正文记录了已有日志" not in json.dumps(
        plan.manifest,
        ensure_ascii=False,
    )


def test_git_recovery_accepts_a_pinned_historical_sibling_body(tmp_path: Path) -> None:
    root, target, manifest, _data = _fixture(tmp_path, same_path=False)

    plan = build_historical_repair_plan(
        content_root=root,
        recovery_manifest_path=manifest,
    )
    rendered = _rendered(plan, target.name)

    assert COMPLETE_BODY in markdown_body(rendered)
    assert markdown_frontmatter(rendered)["title"] == "当前目标标题"
    assert plan.manifest["groups"][0]["integrity_decision"]["action"] == (
        "restore_from_git_history"
    )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("target_file_sha256", "0" * 64, "target precondition"),
        ("source_git_blob", "0" * 40, "commit:path blob"),
        ("source_file_sha256", "0" * 64, "source payload"),
        ("canonical_url", "https://example.com/wrong", "canonical URL"),
    ),
)
def test_git_recovery_rejects_pinned_evidence_drift(
    tmp_path: Path,
    field: str,
    value: str,
    message: str,
) -> None:
    root, _target, manifest, data = _fixture(tmp_path, same_path=True)
    data["entries"][0][field] = value
    _write_manifest(manifest, data)

    with pytest.raises(MigrationSafetyError, match=message):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_git_recovery_rejects_a_historical_body_that_still_fails_quality(
    tmp_path: Path,
) -> None:
    root, _target, manifest, _data = _fixture(
        tmp_path,
        same_path=True,
        source_body="## 证据\n\n```python\nprint('historically truncated')",
    )

    with pytest.raises(MigrationSafetyError, match="quality gate"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


@pytest.mark.parametrize(
    ("source_payload", "message"),
    (
        (b"\xff\xfeinvalid", "not UTF-8"),
        (b"historical body without frontmatter\n", "invalid frontmatter"),
    ),
)
def test_git_recovery_rejects_invalid_historical_document_encoding_or_frontmatter(
    tmp_path: Path,
    source_payload: bytes,
    message: str,
) -> None:
    root, _target, manifest, _data = _fixture(
        tmp_path,
        same_path=True,
        source_payload=source_payload,
    )

    with pytest.raises(MigrationSafetyError, match=message):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_git_recovery_rejects_a_source_with_another_canonical_url(
    tmp_path: Path,
) -> None:
    root, _target, manifest, _data = _fixture(
        tmp_path,
        same_path=True,
        source_external_url="https://example.com/another-article",
    )

    with pytest.raises(MigrationSafetyError, match="source canonical URL"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_git_recovery_rejects_manifest_path_traversal(tmp_path: Path) -> None:
    root, _target, manifest, data = _fixture(tmp_path, same_path=True)
    data["entries"][0]["source_path"] = "../outside.md"
    _write_manifest(manifest, data)

    with pytest.raises(MigrationSafetyError, match="source_path"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_git_recovery_rejects_a_tampered_or_non_regular_audit(
    tmp_path: Path,
) -> None:
    root, _target, manifest, data = _fixture(tmp_path, same_path=True)
    audit = manifest.parent / data["audit_path"]
    audit.write_text('{"schema_version":"historical_git_recovery_audit_v1"}\n')

    with pytest.raises(MigrationSafetyError, match="audit SHA256"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )

    audit.unlink()
    outside = manifest.parent.parent / "outside-audit.json"
    outside.write_text('{"schema_version":"historical_git_recovery_audit_v1"}\n')
    audit.symlink_to(outside)
    data["audit_sha256"] = hashlib.sha256(outside.read_bytes()).hexdigest()
    _write_manifest(manifest, data)

    with pytest.raises(MigrationSafetyError, match="audit must be a regular file"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_git_recovery_rejects_an_unsafe_audit_path(tmp_path: Path) -> None:
    root, _target, manifest, data = _fixture(tmp_path, same_path=True)
    data["audit_path"] = "../outside-audit.json"
    _write_manifest(manifest, data)

    with pytest.raises(MigrationSafetyError, match="audit_path"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_git_recovery_rejects_a_nested_audit_path(tmp_path: Path) -> None:
    root, _target, manifest, data = _fixture(tmp_path, same_path=True)
    data["audit_path"] = "nested/historical-post-recovery-audit-v1.json"
    _write_manifest(manifest, data)

    with pytest.raises(MigrationSafetyError, match="audit_path"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_reviewed_complete_history_basis_allows_a_pinned_nonfatal_target(
    tmp_path: Path,
) -> None:
    root, target, manifest, data = _fixture(tmp_path, same_path=True)
    _write_post(
        target,
        external_url=data["entries"][0]["canonical_url"],
        title="当前已退出高置信检测的含糊目标",
        body=COMPLETE_BODY.replace("这是历史提交中", "这是当前含糊版本中"),
    )
    data["entries"][0]["target_file_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    data["entries"][0]["recovery_basis"] = "reviewed_complete_same_canonical_history"
    _write_manifest(manifest, data)

    plan = build_historical_repair_plan(
        content_root=root,
        recovery_manifest_path=manifest,
    )

    assert plan.manifest["git_history_recovery"]["recovered_count"] == 1
    assert plan.manifest["groups"][0]["integrity_decision"]["recovery_basis"] == (
        "reviewed_complete_same_canonical_history"
    )


def test_detected_basis_still_rejects_a_nonfatal_target(tmp_path: Path) -> None:
    root, target, manifest, data = _fixture(tmp_path, same_path=True)
    _write_post(
        target,
        external_url=data["entries"][0]["canonical_url"],
        title="当前完整目标",
        body=COMPLETE_BODY,
    )
    data["entries"][0]["target_file_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    _write_manifest(manifest, data)

    with pytest.raises(MigrationSafetyError, match="no longer has the audited truncation"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_git_recovery_rejects_an_unknown_recovery_basis(tmp_path: Path) -> None:
    root, _target, manifest, data = _fixture(tmp_path, same_path=True)
    data["entries"][0]["recovery_basis"] = "trust_me"
    _write_manifest(manifest, data)

    with pytest.raises(MigrationSafetyError, match="recovery_basis"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_git_recovery_fails_closed_when_a_manifest_target_cannot_be_parsed(
    tmp_path: Path,
) -> None:
    root, target, manifest, data = _fixture(tmp_path, same_path=True)
    target.write_text("target without closed frontmatter\n", encoding="utf-8")
    data["entries"][0]["target_file_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    _write_manifest(manifest, data)

    with pytest.raises(MigrationSafetyError, match=r"not recovered.*target\.md"):
        build_historical_repair_plan(
            content_root=root,
            recovery_manifest_path=manifest,
        )


def test_cli_requires_an_explicit_recovery_manifest_argument(tmp_path: Path) -> None:
    parser = build_parser()

    assert parser.parse_args([]).recovery_manifest is None
    assert parser.parse_args(
        ["--recovery-manifest", str(tmp_path / "reviewed.json")]
    ).recovery_manifest == (tmp_path / "reviewed.json")


def test_reviewed_recovery_manifest_pins_exactly_75_audited_sources() -> None:
    manifest_path = PROJECT_ROOT / "config/historical-post-recovery-v1.json"
    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )
    entries = manifest["entries"]
    audit_path = manifest_path.parent / manifest["audit_path"]
    audit_payload = audit_path.read_bytes()
    audit = json.loads(audit_payload)

    assert manifest["schema_version"] == "historical_git_recovery_manifest_v1"
    assert manifest["audit_path"] == "historical-post-recovery-audit-v1.json"
    assert manifest["audit_sha256"] == (
        "78a6bdda299d16d8634ec9348bcd200905b314d80116e66a0ded1dede99220e7"
    )
    assert hashlib.sha256(audit_payload).hexdigest() == manifest["audit_sha256"]
    assert audit["schema_version"] == "historical_git_recovery_audit_v1"
    assert audit["scope"]["target_count"] == 232
    assert audit["counts"]["high_confidence_recover"] == 27
    assert audit["counts"]["high_confidence_archive"] == 70
    assert audit["counts"]["ambiguous_recover"] == 48
    assert audit["counts"]["ambiguous_preserved"] == 87
    assert manifest["entry_count"] == len(entries) == 75
    entries_payload = (
        json.dumps(entries, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()
    assert hashlib.sha256(entries_payload).hexdigest() == audit["manifest_entries_sha256"]
    assert [entry["target_path"] for entry in entries] == sorted(
        entry["target_path"] for entry in entries
    )
    assert len({entry["target_path"] for entry in entries}) == 75
    assert {entry["recovery_basis"] for entry in entries} == {
        "detected_truncation",
        "reviewed_complete_same_canonical_history",
    }
    assert sum(entry["recovery_basis"] == "detected_truncation" for entry in entries) == 27
    assert (
        sum(
            entry["recovery_basis"] == "reviewed_complete_same_canonical_history"
            for entry in entries
        )
        == 48
    )
    assert all(len(entry["target_file_sha256"]) == 64 for entry in entries)
    assert all(len(entry["source_git_blob"]) == 40 for entry in entries)
    assert all(len(entry["source_file_sha256"]) == 64 for entry in entries)
    restore_decisions = {
        decision["target_path"]: decision
        for decision in audit["decisions"]
        if decision["action"] == "restore_from_git_history"
    }
    assert set(restore_decisions) == {entry["target_path"] for entry in entries}
    for entry in entries:
        decision = restore_decisions[entry["target_path"]]
        for field in (
            "target_file_sha256",
            "canonical_url",
            "recovery_basis",
            "source_commit",
            "source_path",
            "source_git_blob",
            "source_file_sha256",
        ):
            assert decision[field] == entry[field]
    assert all(
        not ({"body", "content", "tail", "history_candidates"} & set(decision))
        for decision in audit["decisions"]
    )
