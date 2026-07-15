from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from ai_stack.content_quality import analyze_post, markdown_body
from ai_stack.historical_repair import build_historical_repair_plan

TRUSTED_BODY = (
    "## 摘要\n\n"
    "这是同一来源 URL 下保存完好的可信正文，完整保留了采集时获得的工程事实、"
    "约束条件与结论。历史修复只能选择这份已有副本恢复 canonical Post，不能根据"
    "损坏文本猜测缺失内容，也不能删除乱码后把残缺正文伪装成完整文章。\n\n"
    "## 证据\n\n"
    "恢复来源具有闭合结构、有效 UTF-8 文本和完整句末标点。"
)

INTEGRITY_CASES = (
    pytest.param(
        "unclosed_code_fence",
        "## 证据\n\n```python\nprint('BROKEN_UNCLOSED_FENCE')",
        "fixture",
        id="unclosed-fence",
    ),
    pytest.param(
        "encoding_replacement_character",
        "## 摘要\n\nBROKEN_REPLACEMENT_CHARACTER：采集正文中出现了 \ufffd 字符。",
        "fixture",
        id="replacement-character",
    ),
    pytest.param(
        "translation_response_leak",
        (
            "## 描述\n\nBROKEN_TRANSLATION_RESPONSE：您好！我注意到您提供的这段内容"
            "已经是中文，下面提供相应的英文版本。"
        ),
        "fixture",
        id="translation-response",
    ),
    pytest.param(
        "truncated_pre_citation_tail",
        (
            "## 摘要\n\nBROKEN_UNTERMINATED_PROSE 这段历史 Hacker News 正文在采集时"
            "被意外截断并且最后一句没有任何闭合标点仍然停留在半句话中，"
            "缺失的后续内容也无法通过当前保存的证据准确确定，\n\n"
            "## 引用\n\n- [原文](https://example.com/source)"
        ),
        "hacker_news",
        id="truncated-pre-citation-tail",
    ),
)


def _write_post(
    root: Path,
    name: str,
    *,
    external_url: str,
    body: str,
    date: str,
    source: str = "fixture",
    archived: bool = False,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, object] = {
        "title": f"完整性测试 {name}",
        "description": "该固定摘要用于验证历史完整性恢复，不参与正文修补或候选排序。",
        "date": date,
        "draft": False,
        "source": source,
        "external_url": external_url,
        "tags": ["AI 工程"],
        "categories": ["AI 工程"],
        "scenarios": ["AI/ML项目"],
        "content_mode": "legacy_analysis",
        "publication_tier": "LEGACY",
        "source_provenance": "legacy_no_snapshot",
        "source_support": 0.0,
    }
    if archived:
        metadata["archived"] = True
        metadata["content_mode"] = "archived"
        metadata["publication_tier"] = "ARCHIVED"
    if source == "hacker_news":
        metadata["entry_kind"] = "auto"
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    path = root / name
    path.write_text(f"---\n{frontmatter}\n---\n\n{body.strip()}\n", encoding="utf-8")
    return path


def _write_content(plan, relative_path: str) -> str:
    operation = next(write for write in plan.writes if write.path == relative_path)
    return operation.content.decode("utf-8")


@pytest.mark.parametrize(("reason", "broken_body", "source"), INTEGRITY_CASES)
def test_integrity_failure_restores_the_complete_same_url_sibling_losslessly(
    tmp_path: Path,
    reason: str,
    broken_body: str,
    source: str,
) -> None:
    root = tmp_path / "content/posts"
    external_url = f"https://example.com/recover/{reason}"
    broken = _write_post(
        root,
        "20260101-broken.md",
        external_url=external_url,
        body=broken_body,
        date="2026-01-01T00:00:00+08:00",
        source=source,
    )
    trusted = _write_post(
        root,
        "20260201-trusted.md",
        external_url=external_url,
        body=TRUSTED_BODY,
        date="2026-02-01T00:00:00+08:00",
        source=source,
    )

    assert reason in analyze_post(broken.read_text(encoding="utf-8")).fatal_reasons
    plan = build_historical_repair_plan(content_root=root)
    group = plan.manifest["groups"][0]
    decision = group["integrity_decision"]
    rendered = _write_content(plan, broken.name)

    assert group["canonical_path"] == broken.name
    assert group["body_source"] == trusted.name
    assert decision == {
        "action": "restore_from_complete_sibling",
        "failed_paths": [broken.name],
        "failure_reasons": [reason],
        "source_file_sha256": hashlib.sha256(trusted.read_bytes()).hexdigest(),
        "source_path": trusted.name,
    }
    assert markdown_body(rendered).strip() == TRUSTED_BODY
    assert broken_body.strip() not in rendered


@pytest.mark.parametrize(("reason", "broken_body", "source"), INTEGRITY_CASES)
def test_integrity_failure_without_a_trusted_sibling_is_transparently_archived(
    tmp_path: Path,
    reason: str,
    broken_body: str,
    source: str,
) -> None:
    root = tmp_path / "content/posts"
    broken = _write_post(
        root,
        "20260101-broken.md",
        external_url=f"https://example.com/archive/{reason}",
        body=broken_body,
        date="2026-01-01T00:00:00+08:00",
        source=source,
    )

    plan = build_historical_repair_plan(content_root=root)
    group = plan.manifest["groups"][0]
    rendered = _write_content(plan, broken.name)
    metadata = yaml.safe_load(rendered.split("---", 2)[1])

    assert group["disposition"] == "archive_stub"
    assert group["body_source"] is None
    assert group["integrity_decision"] == {
        "action": "transparent_archive",
        "failed_paths": [broken.name],
        "failure_reasons": [reason],
        "source_file_sha256": None,
        "source_path": None,
    }
    assert metadata["archived"] is True
    assert broken_body.strip() not in markdown_body(rendered)


def test_archived_same_url_page_is_not_a_trusted_recovery_sibling(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    external_url = "https://example.com/archived-is-not-source"
    broken = _write_post(
        root,
        "20260101-broken.md",
        external_url=external_url,
        body="## 摘要\n\n损坏字符 \ufffd 不能通过删除字符来修补。",
        date="2026-01-01T00:00:00+08:00",
    )
    archived = _write_post(
        root,
        "20260201-archived.md",
        external_url=external_url,
        body=TRUSTED_BODY * 3,
        date="2026-02-01T00:00:00+08:00",
        archived=True,
    )

    group = build_historical_repair_plan(content_root=root).manifest["groups"][0]

    assert group["body_source"] is None
    assert group["disposition"] == "archive_stub"
    assert group["integrity_decision"]["action"] == "transparent_archive"
    assert archived.name not in group["integrity_decision"]["failed_paths"]
    assert broken.name in group["integrity_decision"]["failed_paths"]


def test_complete_canonical_candidate_is_retained_when_only_a_duplicate_is_broken(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    external_url = "https://example.com/retain-complete-canonical"
    trusted = _write_post(
        root,
        "20260101-trusted.md",
        external_url=external_url,
        body=TRUSTED_BODY,
        date="2026-01-01T00:00:00+08:00",
    )
    broken = _write_post(
        root,
        "20260201-broken.md",
        external_url=external_url,
        body="## 摘要\n\n重复副本包含无法恢复的乱码 \ufffd。",
        date="2026-02-01T00:00:00+08:00",
    )

    group = build_historical_repair_plan(content_root=root).manifest["groups"][0]

    assert group["body_source"] == trusted.name
    assert group["integrity_decision"] == {
        "action": "retain_complete_candidate",
        "failed_paths": [broken.name],
        "failure_reasons": ["encoding_replacement_character"],
        "source_file_sha256": hashlib.sha256(trusted.read_bytes()).hexdigest(),
        "source_path": trusted.name,
    }


def test_integrity_recovery_is_idempotent_after_the_reviewed_plan_is_materialized(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    external_url = "https://example.com/idempotent-recovery"
    broken = _write_post(
        root,
        "20260101-broken.md",
        external_url=external_url,
        body="## 摘要\n\n正文含损坏字符 \ufffd。",
        date="2026-01-01T00:00:00+08:00",
    )
    trusted = _write_post(
        root,
        "20260201-trusted.md",
        external_url=external_url,
        body=TRUSTED_BODY,
        date="2026-02-01T00:00:00+08:00",
    )

    first = build_historical_repair_plan(content_root=root)
    broken.write_bytes(next(write.content for write in first.writes if write.path == broken.name))
    trusted.unlink()

    repeated = build_historical_repair_plan(content_root=root)

    assert repeated.manifest["planned_changes"] == 0
    assert repeated.manifest["groups"] == []
