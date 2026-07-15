from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml

from ai_stack.migrations import MigrationSafetyError

CATEGORIES = {"AI 工程", "大模型", "开发工具"}
SCENARIOS = {"AI/ML项目", "大语言模型", "RAG应用"}
SOURCE_SHA = "a" * 40
CODE_SHA = "b" * 40


def _write_post(
    root: Path,
    name: str,
    *,
    external_url: str,
    body: str,
    date: str,
    title: str | None = None,
    tags: list[str] | None = None,
    categories: list[str] | None = None,
    scenarios: list[str] | None = None,
    archived: bool = False,
) -> Path:
    import yaml

    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = {
        "title": title or name.removesuffix(".md"),
        "date": date,
        "external_url": external_url,
        "tags": tags or [],
        "categories": categories or [],
        "scenarios": scenarios or [],
    }
    if archived:
        frontmatter["archived"] = True
    payload = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False)
    path.write_text(f"---\n{payload}---\n\n{body.strip()}\n", encoding="utf-8")
    return path


def _build(root: Path, *, input_paths: list[Path] | None = None):
    from ai_stack.historical_repair import build_historical_repair_plan

    return build_historical_repair_plan(
        content_root=root,
        category_whitelist=CATEGORIES,
        scenario_whitelist=SCENARIOS,
        input_paths=input_paths,
    )


def _write_by_path(plan, relative_path: str) -> str:
    operation = next(write for write in plan.writes if write.path == relative_path)
    return operation.content.decode("utf-8")


def test_canonical_route_and_body_winner_are_independent(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    old = _write_post(
        root,
        "20260101-stable-route.md",
        external_url="https://Example.com/story?utm_source=rss",
        body="# 摘要\n\n干净的短稿，保留了原始事实。",
        date="2026-01-01T00:00:00+08:00",
    )
    winner = _write_post(
        root,
        "20260201-richer-body.md",
        external_url="https://example.com/story",
        body="# 摘要\n\n这是更完整、结构更清晰的干净正文。\n\n## 证据\n\n" + "事实。" * 80,
        date="2026-02-01T00:00:00+08:00",
    )

    plan = _build(root, input_paths=[winner, old])
    group = plan.manifest["groups"][0]

    assert group["canonical_url"] == "https://example.com/story"
    assert group["canonical_path"] == old.name
    assert group["body_source"] == winner.name
    assert group["canonical_path"] != group["body_source"]


def test_polluted_long_draft_never_beats_clean_short_copy(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    polluted = _write_post(
        root,
        "20260101-polluted.md",
        external_url="https://example.com/polluted",
        body="由于您提供的信息仅为标题，我将基于常识生成完整分析。\n\n" + "看似完整。" * 1500,
        date="2026-01-01T00:00:00+08:00",
    )
    clean = _write_post(
        root,
        "20260201-clean.md",
        external_url="https://example.com/polluted",
        body="# 原文摘要\n\n可核验的干净短稿，链接见 <https://example.com/polluted>。",
        date="2026-02-01T00:00:00+08:00",
    )

    plan = _build(root)
    group = plan.manifest["groups"][0]

    assert group["body_source"] == clean.name
    polluted_quality = next(item for item in group["candidates"] if item["path"] == polluted.name)
    assert polluted_quality["polluted"] is True
    assert "title_only_generation" in polluted_quality["contamination_reasons"]


def test_pollution_is_detected_beyond_the_intro_without_flagging_normal_analysis(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    polluted = _write_post(
        root,
        "20260101-polluted.md",
        external_url="https://example.com/late-pollution",
        body=(
            "背景事实。" * 500
            + "由于您没有提供原始正文，我将基于标题推演后续细节。"
        ),
        date="2026-01-01T00:00:00+08:00",
    )
    clean = _write_post(
        root,
        "20260201-clean.md",
        external_url="https://example.com/late-pollution",
        body="本文基于公开信息分析已披露的工程事实。" * 20,
        date="2026-02-01T00:00:00+08:00",
    )

    group = _build(root).manifest["groups"][0]
    polluted_quality = next(
        item for item in group["candidates"] if item["path"] == polluted.name
    )

    assert group["body_source"] == clean.name
    assert polluted_quality["polluted"] is True
    assert "missing_source_content" in polluted_quality["contamination_reasons"]


def test_all_polluted_group_plans_a_transparent_archive_stub(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    canonical = _write_post(
        root,
        "20260101-first.md",
        external_url="https://example.com/archive",
        body="鉴于您提供的只是标题，我将基于公开知识进行推测。",
        date="2026-01-01T00:00:00+08:00",
    )
    _write_post(
        root,
        "20260201-second.md",
        external_url="https://example.com/archive",
        body="仅为标题，无法访问原文。以下内容是推测。",
        date="2026-02-01T00:00:00+08:00",
    )

    plan = _build(root)
    group = plan.manifest["groups"][0]
    replacement = _write_by_path(plan, canonical.name)

    assert group["disposition"] == "archive_stub"
    assert group["body_source"] is None
    assert group["archive_reason"] == "all_candidates_failed_content_quality_gate"
    assert "archived: true" in replacement
    assert "历史内容质量门未通过" in replacement
    assert "https://example.com/archive" in replacement
    metadata = yaml.safe_load(replacement.split("---", 2)[1])
    assert metadata["tags"] == []
    assert metadata["categories"] == []
    assert metadata["scenarios"] == []
    assert metadata["_build"] == {"list": "never", "render": "always"}


def test_polluted_singleton_is_also_replaced_by_a_transparent_archive_stub(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    polluted = _write_post(
        root,
        "20260101-singleton.md",
        external_url="https://example.com/singleton",
        body="由于您没有提供完整正文，我将基于标题推测文章细节。",
        date="2026-01-01T00:00:00+08:00",
    )

    plan = _build(root)
    group = plan.manifest["groups"][0]
    replacement = _write_by_path(plan, polluted.name)

    assert plan.manifest["duplicate_group_count"] == 0
    assert plan.manifest["repair_group_count"] == 1
    assert group["source_file_count"] == 1
    assert group["disposition"] == "archive_stub"
    assert "仅保留透明归档记录" in replacement


def test_metadata_is_filtered_from_winner_without_duplicate_union(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    _write_post(
        root,
        "20260101-route.md",
        external_url="https://example.com/meta",
        body="短正文。",
        date="2026-01-01T00:00:00+08:00",
        tags=["副本独有标签"],
        categories=["开发工具"],
        scenarios=["RAG应用"],
    )
    winner_tags = [f"Tag {index}" for index in range(10)]
    _write_post(
        root,
        "20260201-winner.md",
        external_url="https://example.com/meta",
        body="# 完整正文\n\n" + "可核验事实。" * 100,
        date="2026-02-01T00:00:00+08:00",
        tags=winner_tags,
        categories=["AI 工程", "不存在的分类", "大模型"],
        scenarios=["AI/ML项目", "工具", "大语言模型"],
    )

    group = _build(root).manifest["groups"][0]

    assert group["metadata"]["tags"] == winner_tags[:8]
    assert "副本独有标签" not in group["metadata"]["tags"]
    assert group["metadata"]["categories"] == ["AI 工程", "大模型"]
    assert group["metadata"]["scenarios"] == ["AI/ML项目", "大语言模型"]


def test_winner_frontmatter_uses_conservative_taxonomy_normalization(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    canonical = _write_post(
        root,
        "20260101-route.md",
        external_url="https://example.com/taxonomy",
        body="短正文。",
        date="2026-01-01T00:00:00+08:00",
        tags=["旧副本标签"],
    )
    _write_post(
        root,
        "20260201-winner.md",
        external_url="https://example.com/taxonomy",
        body="# 完整正文\n\n" + "可核验事实。" * 100,
        date="2026-02-01T00:00:00+08:00",
        tags=[
            "AI编程",
            "AI 编程",
            "VibeCoding",
            "Vibe Coding",
            "XAI",
            "xAI",
            "SWE-bench",
            "SWE-Bench",
        ],
    )

    plan = _build(root)
    rendered = _write_by_path(plan, canonical.name)
    frontmatter = yaml.safe_load(rendered.split("---", 2)[1])

    assert frontmatter["tags"] == [
        "AI 编程",
        "Vibe Coding",
        "XAI",
        "xAI",
        "SWE-bench",
        "SWE-Bench",
    ]
    assert plan.manifest["groups"][0]["metadata"]["tags"] == frontmatter["tags"]


def test_clean_active_singleton_is_canonically_normalized_and_then_idempotent(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    singleton = _write_post(
        root,
        "20260101-singleton.md",
        external_url="https://Example.com:443/story/?b=2&utm_source=feed&a=1#fragment",
        body="# 原文摘要\n\n这是可核验的干净正文。",
        date="2026-01-01T00:00:00+08:00",
        tags=[" AI编程 ", "AI 编程", "VibeCoding", "Vibe Coding"],
        categories=["不应在标签修复中改写的分类"],
        scenarios=["不应在标签修复中改写的场景"],
    )

    plan = _build(root)
    rendered = _write_by_path(plan, singleton.name)
    frontmatter = yaml.safe_load(rendered.split("---", 2)[1])
    group = plan.manifest["groups"][0]

    assert plan.manifest["planned_changes"] == 1
    assert plan.manifest["duplicate_group_count"] == 0
    assert plan.manifest["normalization_group_count"] == 1
    assert group["disposition"] == "normalize_metadata"
    assert group["canonical_path"] == singleton.name
    assert group["body_source"] == singleton.name
    assert frontmatter["external_url"] == "https://example.com/story?a=1&b=2"
    assert frontmatter["tags"] == ["AI 编程", "Vibe Coding"]
    assert frontmatter["categories"] == ["不应在标签修复中改写的分类"]
    assert frontmatter["scenarios"] == ["不应在标签修复中改写的场景"]
    assert rendered.endswith("# 原文摘要\n\n这是可核验的干净正文。\n")

    singleton.write_text(rendered, encoding="utf-8")
    repeated = _build(root)

    assert repeated.manifest["planned_changes"] == 0
    assert repeated.manifest["groups"] == []


def test_plan_documents_both_safe_execution_profiles(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    _write_post(
        root,
        "20260101-repair.md",
        external_url="https://example.com/repair-policy",
        body="您没有提供完整正文，因此以下内容只能根据标题推演。",
        date="2026-01-01T00:00:00+08:00",
    )

    policy = _build(root).manifest["execution_policy"]

    assert policy["shadow_soak_profile"] == "24_runs_3_full_builds_7_day_soak"
    assert policy["reviewed_repository_profile"] == (
        "clean_codex_branch_exact_head_exact_plan_digest_with_backup"
    )
    assert policy["repository_reviewed_batch_limit"] == 10_000


def test_archived_singleton_is_not_treated_as_active_taxonomy(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    _write_post(
        root,
        "20260101-archived.md",
        external_url="https://Example.com/archive/?utm_source=old",
        body="这是透明归档记录。",
        date="2026-01-01T00:00:00+08:00",
        tags=["AI编程"],
        archived=True,
    )

    plan = _build(root)

    assert plan.manifest["planned_changes"] == 0
    assert plan.manifest["normalization_group_count"] == 0
    assert plan.manifest["groups"] == []


def test_alias_and_relref_rewrite_plan_preserves_old_routes(tmp_path: Path) -> None:
    content = tmp_path / "content"
    root = content / "posts"
    canonical = _write_post(
        root,
        "20260101-canonical.md",
        external_url="https://example.com/refs",
        body="干净正文。",
        date="2026-01-01T00:00:00+08:00",
    )
    duplicate = _write_post(
        root,
        "20260201-duplicate.md",
        external_url="https://example.com/refs",
        body="# 更完整正文\n\n" + "事实。" * 80,
        date="2026-02-01T00:00:00+08:00",
    )
    referring = content / "guide.md"
    referring.write_text(
        '{{< relref "posts/20260201-duplicate.md" >}}\n', encoding="utf-8"
    )

    plan = _build(root)
    group = plan.manifest["groups"][0]
    guide = _write_by_path(plan, "../guide.md")

    assert group["aliases"] == ["/posts/20260201-duplicate/"]
    assert group["delete_paths"] == [duplicate.name]
    assert plan.manifest["relref_rewrites"] == [
        {
            "document": "../guide.md",
            "from": "posts/20260201-duplicate.md",
            "occurrences": 1,
            "to": f"posts/{canonical.name}",
        }
    ]
    assert f'posts/{canonical.name}' in guide
    assert duplicate.name not in guide


def test_manifest_is_deterministic_when_input_order_changes(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    first = _write_post(
        root,
        "a.md",
        external_url="https://example.com/deterministic?utm_medium=x",
        body="干净正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    second = _write_post(
        root,
        "b.md",
        external_url="https://example.com/deterministic",
        body="干净正文 B，更完整。" * 20,
        date="2026-02-01T00:00:00+08:00",
    )

    forward = _build(root, input_paths=[first, second]).manifest
    reverse = _build(root, input_paths=[second, first]).manifest

    assert forward == reverse
    assert forward["plan_digest"].startswith("sha256:")


def test_cli_defaults_to_dry_run_and_does_not_write(tmp_path: Path, capsys) -> None:
    from scripts.repair_historical_content import main

    root = tmp_path / "content/posts"
    _write_post(
        root,
        "a.md",
        external_url="https://example.com/cli",
        body="正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    _write_post(
        root,
        "b.md",
        external_url="https://example.com/cli",
        body="正文 B。" * 30,
        date="2026-02-01T00:00:00+08:00",
    )
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    status = main(["--content-root", str(root)])
    output = json.loads(capsys.readouterr().out)
    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    assert status == 0
    assert output["dry_run"] is True
    assert output["mutation_performed"] is False
    assert before == after


def test_apply_requires_full_safety_gate_arguments(tmp_path: Path) -> None:
    from ai_stack.historical_repair import apply_historical_repair_plan

    root = tmp_path / "content/posts"
    _write_post(
        root,
        "a.md",
        external_url="https://example.com/gate",
        body="正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    _write_post(
        root,
        "b.md",
        external_url="https://example.com/gate",
        body="正文 B。" * 20,
        date="2026-02-01T00:00:00+08:00",
    )

    with pytest.raises(MigrationSafetyError, match="expected-source-sha"):
        apply_historical_repair_plan(
            _build(root),
            expected_source_sha=None,
            expected_code_sha=None,
            backup_id=None,
            max_changes=None,
            shadow_evidence_root=None,
            backup_root=tmp_path / "backups",
        )


def test_apply_uses_shadow_gate_and_is_idempotent(tmp_path: Path, monkeypatch) -> None:
    import ai_stack.historical_repair as repair

    content = tmp_path / "content"
    root = content / "posts"
    canonical = _write_post(
        root,
        "a.md",
        external_url="https://example.com/apply",
        body="正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    duplicate = _write_post(
        root,
        "b.md",
        external_url="https://example.com/apply",
        body="# 完整正文\n\n" + "事实。" * 60,
        date="2026-02-01T00:00:00+08:00",
    )
    plan = _build(root)
    calls: list[dict[str, object]] = []

    def allow_gate(**kwargs):
        calls.append(kwargs)
        return object()

    monkeypatch.setattr(repair, "validate_dedupe_execution_gate", allow_gate)
    backup_root = tmp_path / "backups"
    arguments = {
        "expected_source_sha": SOURCE_SHA,
        "expected_code_sha": CODE_SHA,
        "backup_id": "repair-001",
        "max_changes": 10,
        "shadow_evidence_root": tmp_path / "shadow",
        "backup_root": backup_root,
    }

    first = repair.apply_historical_repair_plan(plan, **arguments)
    after_first = canonical.read_bytes()
    second = repair.apply_historical_repair_plan(plan, **arguments)

    assert len(calls) == 2
    assert calls[0]["content_root"] == root
    assert calls[0]["expected_code_sha"] == CODE_SHA
    assert first["mutation_performed"] is True
    assert first["already_applied"] is False
    assert second["mutation_performed"] is False
    assert second["already_applied"] is True
    assert canonical.read_bytes() == after_first
    assert not duplicate.exists()
    receipt = json.loads((backup_root / "repair-001/receipt.json").read_text(encoding="utf-8"))
    assert receipt["plan_digest"] == plan.manifest["plan_digest"]


def test_repository_reviewed_apply_uses_git_guard_instead_of_shadow_gate(
    tmp_path: Path, monkeypatch
) -> None:
    import ai_stack.historical_repair as repair

    root = tmp_path / "content/posts"
    canonical = _write_post(
        root,
        "a.md",
        external_url="https://example.com/repository-apply",
        body="正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    duplicate = _write_post(
        root,
        "b.md",
        external_url="https://example.com/repository-apply",
        body="# 完整正文\n\n" + "事实。" * 60,
        date="2026-02-01T00:00:00+08:00",
    )
    plan = _build(root)
    execution_calls: list[dict[str, object]] = []

    def reject_shadow_gate(**_kwargs):
        raise AssertionError("repository migration must not use the shadow gate")

    def allow_execution_gate(**kwargs):
        execution_calls.append(kwargs)

    monkeypatch.setattr(repair, "validate_dedupe_execution_gate", reject_shadow_gate)
    monkeypatch.setattr(repair, "validate_execution_gate", allow_execution_gate)
    monkeypatch.setattr(
        repair,
        "_repository_review_state",
        lambda _root: ("codex/history-repair", ""),
        raising=False,
    )

    result = repair.apply_historical_repair_plan(
        plan,
        expected_source_sha=SOURCE_SHA,
        expected_code_sha=None,
        expected_plan_digest=plan.manifest["plan_digest"],
        backup_id="repository-repair-001",
        max_changes=10,
        shadow_evidence_root=None,
        backup_root=tmp_path / "backups",
        repository_reviewed=True,
    )

    assert len(execution_calls) == 1
    assert execution_calls[0]["execute"] is True
    assert result["safety_profile"] == "reviewed_git_repository"
    assert canonical.exists()
    assert not duplicate.exists()


@pytest.mark.parametrize(
    ("branch", "status", "message"),
    [
        ("main", "", "codex/ branch"),
        ("codex/history-repair", " M content/posts/a.md", "clean Git worktree"),
    ],
)
def test_repository_reviewed_apply_rejects_main_or_dirty_worktree(
    tmp_path: Path,
    monkeypatch,
    branch: str,
    status: str,
    message: str,
) -> None:
    import ai_stack.historical_repair as repair

    root = tmp_path / "content/posts"
    _write_post(
        root,
        "a.md",
        external_url="https://example.com/repository-guard",
        body="您没有提供原文，我将根据标题推测。",
        date="2026-01-01T00:00:00+08:00",
    )
    plan = _build(root)
    monkeypatch.setattr(repair, "validate_execution_gate", lambda **_kwargs: None)
    monkeypatch.setattr(
        repair,
        "_repository_review_state",
        lambda _root: (branch, status),
        raising=False,
    )

    with pytest.raises(MigrationSafetyError, match=message):
        repair.apply_historical_repair_plan(
            plan,
            expected_source_sha=SOURCE_SHA,
            expected_code_sha=None,
            expected_plan_digest=plan.manifest["plan_digest"],
            backup_id="repository-guard",
            max_changes=10,
            shadow_evidence_root=None,
            backup_root=tmp_path / "backups",
            repository_reviewed=True,
        )


def test_repository_reviewed_apply_rejects_plan_digest_mismatch(
    tmp_path: Path, monkeypatch
) -> None:
    import ai_stack.historical_repair as repair

    root = tmp_path / "content/posts"
    _write_post(
        root,
        "a.md",
        external_url="https://example.com/repository-digest",
        body="您没有提供原文，我将根据标题推测。",
        date="2026-01-01T00:00:00+08:00",
    )
    plan = _build(root)
    monkeypatch.setattr(repair, "validate_execution_gate", lambda **_kwargs: None)
    monkeypatch.setattr(
        repair,
        "_repository_review_state",
        lambda _root: ("codex/history-repair", ""),
        raising=False,
    )

    with pytest.raises(MigrationSafetyError, match="plan digest mismatch"):
        repair.apply_historical_repair_plan(
            plan,
            expected_source_sha=SOURCE_SHA,
            expected_code_sha=None,
            expected_plan_digest="sha256:" + "0" * 64,
            backup_id="repository-digest",
            max_changes=10,
            shadow_evidence_root=None,
            backup_root=tmp_path / "backups",
            repository_reviewed=True,
        )


def test_stale_plan_is_rejected_before_any_mutation(tmp_path: Path, monkeypatch) -> None:
    import ai_stack.historical_repair as repair

    root = tmp_path / "content/posts"
    canonical = _write_post(
        root,
        "a.md",
        external_url="https://example.com/stale",
        body="正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    duplicate = _write_post(
        root,
        "b.md",
        external_url="https://example.com/stale",
        body="正文 B。" * 30,
        date="2026-02-01T00:00:00+08:00",
    )
    plan = _build(root)
    canonical.write_text(canonical.read_text(encoding="utf-8") + "\n人工修改\n", encoding="utf-8")
    before = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.glob("*.md")
    }
    monkeypatch.setattr(repair, "validate_dedupe_execution_gate", lambda **_kwargs: object())

    with pytest.raises(MigrationSafetyError, match="stale repair plan"):
        repair.apply_historical_repair_plan(
            plan,
            expected_source_sha=SOURCE_SHA,
            expected_code_sha=CODE_SHA,
            backup_id="repair-stale",
            max_changes=10,
            shadow_evidence_root=tmp_path / "shadow",
            backup_root=tmp_path / "backups",
        )

    after = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in root.glob("*.md")}
    assert before == after
    assert duplicate.exists()
    assert not (tmp_path / "backups").exists()


def test_apply_enforces_max_changes_even_if_gate_adapter_is_stubbed(
    tmp_path: Path, monkeypatch
) -> None:
    import ai_stack.historical_repair as repair

    root = tmp_path / "content/posts"
    _write_post(
        root,
        "a.md",
        external_url="https://example.com/max",
        body="正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    _write_post(
        root,
        "b.md",
        external_url="https://example.com/max",
        body="正文 B。" * 30,
        date="2026-02-01T00:00:00+08:00",
    )
    plan = _build(root)
    monkeypatch.setattr(repair, "validate_dedupe_execution_gate", lambda **_kwargs: object())

    with pytest.raises(MigrationSafetyError, match="planned changes exceed"):
        repair.apply_historical_repair_plan(
            plan,
            expected_source_sha=SOURCE_SHA,
            expected_code_sha=CODE_SHA,
            backup_id="repair-max",
            max_changes=1,
            shadow_evidence_root=tmp_path / "shadow",
            backup_root=tmp_path / "backups",
        )

    assert not (tmp_path / "backups").exists()


def test_apply_rolls_back_every_file_when_atomic_phase_fails(
    tmp_path: Path, monkeypatch
) -> None:
    import ai_stack.historical_repair as repair

    content = tmp_path / "content"
    root = content / "posts"
    canonical = _write_post(
        root,
        "a.md",
        external_url="https://example.com/rollback",
        body="正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    duplicate = _write_post(
        root,
        "b.md",
        external_url="https://example.com/rollback",
        body="正文 B。" * 30,
        date="2026-02-01T00:00:00+08:00",
    )
    guide = content / "guide.md"
    guide.write_text('{{< relref "posts/b.md" >}}\n', encoding="utf-8")
    plan = _build(root)
    originals = {path: path.read_bytes() for path in (canonical, duplicate, guide)}
    monkeypatch.setattr(repair, "validate_dedupe_execution_gate", lambda **_kwargs: object())
    original_atomic_write = repair._atomic_write
    failed = False

    def fail_once(path: Path, payload: bytes, *, mode: int = 0o644) -> None:
        nonlocal failed
        if path == canonical and not failed:
            failed = True
            raise OSError("simulated atomic replacement failure")
        original_atomic_write(path, payload, mode=mode)

    monkeypatch.setattr(repair, "_atomic_write", fail_once)

    with pytest.raises(OSError, match="simulated"):
        repair.apply_historical_repair_plan(
            plan,
            expected_source_sha=SOURCE_SHA,
            expected_code_sha=CODE_SHA,
            backup_id="repair-rollback",
            max_changes=10,
            shadow_evidence_root=tmp_path / "shadow",
            backup_root=tmp_path / "backups",
        )

    assert failed is True
    assert {path: path.read_bytes() for path in originals} == originals
    assert not (tmp_path / "backups/repair-rollback/receipt.json").exists()


def test_receipt_write_failure_rolls_back_the_committed_file_set(
    tmp_path: Path, monkeypatch
) -> None:
    import ai_stack.historical_repair as repair

    content = tmp_path / "content"
    root = content / "posts"
    canonical = _write_post(
        root,
        "a.md",
        external_url="https://example.com/receipt-rollback",
        body="正文 A。",
        date="2026-01-01T00:00:00+08:00",
    )
    duplicate = _write_post(
        root,
        "b.md",
        external_url="https://example.com/receipt-rollback",
        body="# 完整正文\n\n" + "事实。" * 60,
        date="2026-02-01T00:00:00+08:00",
    )
    guide = content / "guide.md"
    guide.write_text('{{< relref "posts/b.md" >}}\n', encoding="utf-8")
    plan = _build(root)
    originals = {path: path.read_bytes() for path in (canonical, duplicate, guide)}
    monkeypatch.setattr(repair, "validate_dedupe_execution_gate", lambda **_kwargs: object())
    original_atomic_json = repair._atomic_json

    def fail_receipt(path: Path, value) -> None:
        if path.name == "receipt.json":
            raise OSError("simulated receipt commit failure")
        original_atomic_json(path, value)

    monkeypatch.setattr(repair, "_atomic_json", fail_receipt)

    with pytest.raises(OSError, match="receipt commit"):
        repair.apply_historical_repair_plan(
            plan,
            expected_source_sha=SOURCE_SHA,
            expected_code_sha=CODE_SHA,
            backup_id="repair-receipt",
            max_changes=10,
            shadow_evidence_root=tmp_path / "shadow",
            backup_root=tmp_path / "backups",
        )

    assert {path: path.read_bytes() for path in originals} == originals
    assert not (tmp_path / "backups/repair-receipt/receipt.json").exists()


def test_batch_selection_is_deterministic_and_keeps_canonical_groups_atomic(
    tmp_path: Path,
) -> None:
    from ai_stack.historical_repair import build_historical_repair_batch

    root = tmp_path / "content/posts"
    for prefix, url in (("c", "https://example.com/c"), ("a", "https://example.com/a"), ("b", "https://example.com/b")):
        _write_post(
            root,
            f"{prefix}-route.md",
            external_url=url,
            body=f"{prefix} route",
            date="2026-01-01T00:00:00+08:00",
        )
        _write_post(
            root,
            f"{prefix}-winner.md",
            external_url=url,
            body=f"# {prefix}\n\n" + "事实。" * 40,
            date="2026-02-01T00:00:00+08:00",
        )

    first = build_historical_repair_batch(
        content_root=root,
        category_whitelist=CATEGORIES,
        scenario_whitelist=SCENARIOS,
        max_changes=4,
    )
    second = build_historical_repair_batch(
        content_root=root,
        category_whitelist=CATEGORIES,
        scenario_whitelist=SCENARIOS,
        max_changes=4,
    )

    selection = first.manifest["batch_selection"]
    assert first.manifest == second.manifest
    assert first.manifest["planned_changes"] <= 4
    assert selection["atomic_unit"] == "canonical_url_group"
    assert selection["selected_canonical_urls"] == [
        "https://example.com/a",
        "https://example.com/b",
    ]
    assert selection["selected_group_count"] == 2
    assert selection["remaining_group_count"] == 1
    assert {group["canonical_url"] for group in first.manifest["groups"]} == {
        "https://example.com/a",
        "https://example.com/b",
    }
    assert {delete.path for delete in first.deletes} == {
        "a-winner.md",
        "b-winner.md",
    }


def test_batch_selection_rejects_a_canonical_group_larger_than_the_gate(
    tmp_path: Path,
) -> None:
    from ai_stack.historical_repair import build_historical_repair_batch

    root = tmp_path / "content/posts"
    for index in range(3):
        _write_post(
            root,
            f"group-{index}.md",
            external_url="https://example.com/unsplittable",
            body=("# 完整正文\n\n" + "事实。" * (index + 1) * 20),
            date=f"2026-01-0{index + 1}T00:00:00+08:00",
        )

    with pytest.raises(MigrationSafetyError, match="canonical group exceeds"):
        build_historical_repair_batch(
            content_root=root,
            category_whitelist=CATEGORIES,
            scenario_whitelist=SCENARIOS,
            max_changes=2,
        )


def test_cli_batch_dry_run_selects_a_safe_prefix_without_writing(
    tmp_path: Path, capsys
) -> None:
    from scripts.repair_historical_content import main

    root = tmp_path / "content/posts"
    for prefix in ("a", "b"):
        for suffix, repeat in (("route", 1), ("winner", 30)):
            _write_post(
                root,
                f"{prefix}-{suffix}.md",
                external_url=f"https://example.com/{prefix}",
                body="事实。" * repeat,
                date=(
                    "2026-01-01T00:00:00+08:00"
                    if suffix == "route"
                    else "2026-02-01T00:00:00+08:00"
                ),
            )
    before = {path.name: path.read_bytes() for path in root.glob("*.md")}

    status = main(
        [
            "--content-root",
            str(root),
            "--batch",
            "--max-changes",
            "2",
        ]
    )
    output = json.loads(capsys.readouterr().out)

    assert status == 0
    assert output["dry_run"] is True
    assert output["planned_changes"] <= 2
    assert output["batch_selection"]["selected_group_count"] == 1
    assert before == {path.name: path.read_bytes() for path in root.glob("*.md")}
