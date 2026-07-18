from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_stack.content_quality import analyze_post, is_curated_evidence_backed_rewrite
from ai_stack.historical_repair import build_historical_repair_plan

CANONICAL_URL = "https://example.com/shared-source"
SENTENCE = "这段内容只陈述来源可以支持的工程事实，并以完整句子自然结束。"
REWRITE_HEADINGS = (
    "转写说明",
    "核心结论",
    "能力机制",
    "快速开始",
    "适用边界",
    "核验清单",
    "来源与核验",
)


def _write_post(
    root: Path,
    name: str,
    *,
    metadata: dict[str, object],
    body: str,
    date: str,
    expect_clean: bool = True,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    frontmatter = {
        "title": name.removesuffix(".md"),
        "description": "用于验证历史正文来源证明优先级的固定摘要。",
        "date": date,
        "draft": False,
        "external_url": CANONICAL_URL,
        "tags": ["AI"],
        "categories": ["AI 工程"],
        "scenarios": ["AI/ML项目"],
        **metadata,
    }
    payload = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).rstrip()
    path = root / name
    path.write_text(f"---\n{payload}\n---\n\n{body.strip()}\n", encoding="utf-8")
    if expect_clean:
        assert analyze_post(path.read_text(encoding="utf-8")).fatal_reasons == ()
    return path


def _strict_v2(root: Path, name: str, *, date: str) -> Path:
    body = "\n\n".join(f"## {heading}\n\n{SENTENCE * 5}" for heading in REWRITE_HEADINGS)
    return _write_post(
        root,
        name,
        date=date,
        body=body,
        metadata={
            "entry_kind": "auto",
            "source": "juejin",
            "content_mode": "evidence_backed_rewrite",
            "publication_tier": "B",
            "source_capture_mode": "full_article",
            "source_completeness": "complete",
            "source_is_truncated": False,
            "source_snapshot_sha256": "sha256:" + "a" * 64,
            "parent_snapshot_sha256": "sha256:" + "b" * 64,
            "extractor_version": "source-contract-v2",
            "discovery_method": "article_html",
            "source_support": 1.0,
        },
    )


def _modern_brief(root: Path, name: str, *, date: str, repeat: int) -> Path:
    return _write_post(
        root,
        name,
        date=date,
        body="## 基本信息\n\n- **来源**: RSS\n\n" + SENTENCE * repeat,
        metadata={
            "entry_kind": "auto",
            "source": "blogs_podcasts",
            "content_mode": "source_brief",
            "publication_tier": "C",
            "source_capture_mode": "excerpt",
            "source_snapshot_sha256": "sha256:" + "c" * 64,
            "extractor_version": "source-contract-v1",
            "discovery_method": "rss_excerpt",
            "source_is_truncated": False,
            "source_support": 1.0,
        },
    )


def _curated(root: Path, name: str, *, date: str, repeat: int) -> Path:
    return _write_post(
        root,
        name,
        date=date,
        body="## 独立核验\n\n" + SENTENCE * repeat,
        metadata={
            "entry_kind": "curated",
            "source": "blogs_podcasts",
            "content_mode": "evidence_backed_rewrite",
            "publication_tier": "B",
            "source_capture_mode": "curated_sources",
            "source_completeness": "verified",
            "source_is_truncated": False,
            "editorial_sources": [
                CANONICAL_URL,
                "https://docs.example.com/primary",
            ],
        },
    )


def _unverified_curated(root: Path, name: str, *, date: str, repeat: int) -> Path:
    return _write_post(
        root,
        name,
        date=date,
        expect_clean=False,
        body="## 未完成核验\n\n" + SENTENCE * repeat,
        metadata={
            "entry_kind": "curated",
            "source": "blogs_podcasts",
            "content_mode": "evidence_backed_rewrite",
            "publication_tier": "B",
            "source_capture_mode": "curated_sources",
            "source_completeness": "partial",
            "source_is_truncated": False,
            "editorial_sources": [CANONICAL_URL],
        },
    )


def _legacy_analysis(root: Path, name: str, *, date: str, repeat: int) -> Path:
    return _write_post(
        root,
        name,
        date=date,
        body="## 历史分析\n\n" + SENTENCE * repeat,
        metadata={
            "entry_kind": "auto",
            "source": "hacker_news",
            "content_mode": "legacy_analysis",
            "publication_tier": "LEGACY",
            "source_provenance": "legacy_no_snapshot",
            "source_support": 0.0,
        },
    )


def _legacy_brief(root: Path, name: str, *, date: str, repeat: int) -> Path:
    return _write_post(
        root,
        name,
        date=date,
        body="## 基本信息\n\n- **来源**: Hacker News\n\n" + SENTENCE * repeat,
        metadata={
            "entry_kind": "auto",
            "source": "hacker_news",
            "content_mode": "legacy_source_brief",
            "publication_tier": "C",
            "source_provenance": "legacy_no_snapshot",
            "source_support": 0.0,
        },
    )


@pytest.mark.parametrize(
    ("higher_factory", "higher_repeat", "lower_factory", "lower_repeat"),
    (
        (_strict_v2, None, _modern_brief, 800),
        (_modern_brief, 3, _curated, 500),
        (_curated, 30, _legacy_analysis, 800),
        (_legacy_analysis, 4, _legacy_brief, 8),
    ),
)
def test_duplicate_winner_prefers_modern_source_proof_over_body_length(
    tmp_path: Path,
    higher_factory,
    higher_repeat: int | None,
    lower_factory,
    lower_repeat: int,
) -> None:
    root = tmp_path / "content/posts"
    higher_kwargs = {"date": "2026-02-01T00:00:00+08:00"}
    if higher_repeat is not None:
        higher_kwargs["repeat"] = higher_repeat
    higher = higher_factory(root, "higher.md", **higher_kwargs)
    lower = lower_factory(
        root,
        "lower-stable-route.md",
        date="2026-01-01T00:00:00+08:00",
        repeat=lower_repeat,
    )

    plan = build_historical_repair_plan(content_root=root)
    group = plan.manifest["groups"][0]

    assert group["canonical_path"] == lower.name
    assert group["body_source"] == higher.name


def test_unverified_curated_candidate_cannot_outrank_legacy_analysis(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    legacy = _legacy_analysis(
        root,
        "legacy.md",
        date="2026-01-01T00:00:00+08:00",
        repeat=4,
    )
    _unverified_curated(
        root,
        "unverified-curated.md",
        date="2026-02-01T00:00:00+08:00",
        repeat=800,
    )

    plan = build_historical_repair_plan(content_root=root)

    assert plan.manifest["groups"][0]["body_source"] == legacy.name


def test_unverified_curated_rewrite_fails_the_shared_evidence_contract(
    tmp_path: Path,
) -> None:
    path = _unverified_curated(
        tmp_path / "content/posts",
        "unverified-curated.md",
        date="2026-02-01T00:00:00+08:00",
        repeat=40,
    )
    document = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(document.split("---", 2)[1])
    body = document.split("---", 2)[2]

    assert is_curated_evidence_backed_rewrite(metadata, body) is False
    assert "invalid_evidence_backed_rewrite" in analyze_post(document).fatal_reasons
