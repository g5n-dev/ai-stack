from __future__ import annotations

from dataclasses import replace
from datetime import datetime

import pytest
import yaml

from ai_stack.content_quality import analyze_post
from ai_stack.source_contract import verify_source_contract
from crawler.historical_source_fetch import HistoricalSourceCapture

CAPTURED_AT = "2026-07-18T02:03:04Z"
HISTORICAL_DATE = "2026-01-25T12:39:55+08:00"


def _capture(source: str, *, truncated: bool = False) -> HistoricalSourceCapture:
    fixtures = {
        "arxiv": {
            "title": "Evidence-aware agents",
            "external_url": "https://arxiv.org/abs/2607.12345v1",
            "source_text": "A verified abstract about retrieval agents and evaluation.",
            "capture_mode": "abstract",
            "source_completeness": "abstract_only",
            "metadata": {
                "arxiv_id": "2607.12345v1",
                "authors": ["Ada Lovelace", "Alan Turing"],
                "category": "cs.AI",
                "published": "2026-07-17T01:02:03Z",
                "pdf_url": "https://arxiv.org/pdf/2607.12345v1.pdf",
            },
        },
        "github_trending": {
            "title": "octo/evidence-agent",
            "external_url": "https://github.com/octo/evidence-agent",
            "source_text": "A repository for evidence-aware agents.",
            "capture_mode": "metadata_only",
            "source_completeness": "metadata_only",
            "metadata": {
                "language": "Rust",
                "stars": 123,
                "forks": 7,
                "license": "Apache-2.0",
                "topics": ["agent", "rust"],
            },
        },
        "hacker_news": {
            "title": "A new evidence-aware AI runtime",
            "external_url": "https://example.com/evidence-runtime",
            "source_text": "A new evidence-aware AI runtime",
            "capture_mode": "metadata_only",
            "source_completeness": "metadata_only",
            "metadata": {
                "hn_id": 47158975,
                "author": "ada",
                "score": 284,
                "descendants": 38,
                "published": "2026-07-17T01:02:03Z",
            },
        },
        "blogs_podcasts": {
            "title": "Building evidence-aware agents",
            "external_url": "https://openai.com/index/evidence-aware-agents",
            "source_text": (
                "The source describes a concrete agent architecture.\n\n"
                "It records evaluation boundaries and deployment constraints."
            ),
            "capture_mode": "excerpt",
            "source_completeness": "partial",
            "metadata": {
                "author": "Source Author",
                "published": "2026-07-17T01:02:03Z",
            },
        },
        "juejin": {
            "title": "用 Rust 构建可验证的 AI Agent",
            "external_url": "https://juejin.cn/post/7663304647513718799",
            "source_text": "这是通过 SSR 结构校验后保存的来源正文节选。",
            "capture_mode": "excerpt",
            "source_completeness": "partial",
            "metadata": {
                "article_id": "7663304647513718799",
                "heading_count": 3,
                "code_block_count": 2,
                "source_truncation_reason": "historical_excerpt_only",
            },
        },
    }
    values = fixtures[source]
    return HistoricalSourceCapture(
        source=source,
        title=str(values["title"]),
        external_url=str(values["external_url"]),
        source_text=str(values["source_text"]),
        captured_at=CAPTURED_AT,
        capture_mode=str(values["capture_mode"]),
        source_completeness=str(values["source_completeness"]),
        source_is_truncated=truncated,
        metadata=dict(values["metadata"]),
    )


def _frontmatter(document: str) -> dict[str, object]:
    assert document.startswith("---\n")
    raw = document.split("---\n", 2)[1]
    parsed = yaml.safe_load(raw)
    assert isinstance(parsed, dict)
    return parsed


@pytest.mark.parametrize(
    ("source", "capture_mode", "completeness", "discovery_method"),
    (
        ("arxiv", "abstract", "abstract_only", "arxiv_api"),
        (
            "github_trending",
            "metadata_only",
            "metadata_only",
            "repository_metadata",
        ),
        ("hacker_news", "metadata_only", "metadata_only", "api_metadata"),
        ("blogs_podcasts", "excerpt", "partial", "article_html_excerpt"),
        ("juejin", "excerpt", "partial", "article_html_excerpt"),
    ),
)
def test_capture_to_source_contract_item_is_strict_and_verifiable(
    source: str,
    capture_mode: str,
    completeness: str,
    discovery_method: str,
) -> None:
    from ai_stack.historical_publication import capture_to_source_contract_item

    capture = _capture(source, truncated=source in {"blogs_podcasts", "juejin"})

    first = capture_to_source_contract_item(capture)
    second = capture_to_source_contract_item(capture)

    assert first == second
    assert first["content_mode"] == "source_brief"
    assert first["publication_tier"] == "C"
    assert first["source_capture_mode"] == capture_mode
    assert first["source_completeness"] == completeness
    assert first["discovery_method"] == discovery_method
    assert first["source_is_truncated"] is capture.source_is_truncated
    if capture.source_is_truncated:
        expected_reason = (
            "historical_excerpt_only"
            if source == "juejin"
            else "historical_capture_limit"
        )
        assert expected_reason in first["source_truncation_reason"]
    else:
        assert first["source_truncation_reason"] == ""
    verify_source_contract(first)


@pytest.mark.parametrize(
    "source",
    ("arxiv", "github_trending", "hacker_news", "blogs_podcasts", "juejin"),
)
def test_renderer_preserves_route_metadata_and_emits_a_valid_tier_c_post(
    source: str,
) -> None:
    from ai_stack.historical_publication import render_historical_tier_c_markdown

    prior = {
        "title": "OLD TITLE MUST NOT SURVIVE",
        "description": "OLD DESCRIPTION MUST NOT SURVIVE",
        "date": HISTORICAL_DATE,
        "aliases": ["/posts/old-route/", "/archive/stable-route/"],
        "archived": True,
        "build": {"list": "never", "render": "always"},
        "_build": {"list": False},
        "tags": ["OLD FACT"],
        "categories": ["OLD FACT"],
    }

    capture = _capture(source, truncated=source == "juejin")
    first = render_historical_tier_c_markdown(capture, prior_metadata=prior)
    second = render_historical_tier_c_markdown(capture, prior_metadata=prior)
    metadata = _frontmatter(first)
    analysis = analyze_post(first)

    assert first == second
    assert str(metadata["date"]) == HISTORICAL_DATE
    assert metadata["aliases"] == prior["aliases"]
    assert metadata["content_mode"] == "source_brief"
    assert metadata["publication_tier"] == "C"
    assert metadata["source_support"] == 1.0
    assert "archived" not in metadata
    assert "build" not in metadata
    assert "_build" not in metadata
    assert "OLD TITLE MUST NOT SURVIVE" not in first
    assert "OLD DESCRIPTION MUST NOT SURVIVE" not in first
    assert "OLD FACT" not in first
    assert analysis.status == "source_brief"
    assert analysis.fatal_reasons == ()


@pytest.mark.parametrize(
    ("source", "expected"),
    (
        (
            "arxiv",
            {
                "tags": ["ArXiv", "AI Agent"],
                "categories": ["论文"],
                "scenarios": ["AI/ML项目"],
            },
        ),
        (
            "github_trending",
            {
                "tags": ["GitHub", "AI Agent", "Rust"],
                "categories": ["开源生态", "开发工具"],
                "scenarios": ["AI/ML项目"],
            },
        ),
        (
            "hacker_news",
            {
                "tags": ["Hacker News"],
                "categories": [],
                "scenarios": [],
            },
        ),
        (
            "juejin",
            {
                "tags": ["掘金", "AI Agent", "Rust"],
                "categories": ["AI 工程"],
                "scenarios": ["AI/ML项目"],
            },
        ),
    ),
)
def test_renderer_uses_capture_taxonomy_in_frontmatter(
    source: str,
    expected: dict[str, list[str]],
) -> None:
    from ai_stack.historical_publication import render_historical_tier_c_markdown

    document = render_historical_tier_c_markdown(
        _capture(source, truncated=source == "juejin"),
        prior_metadata={"date": HISTORICAL_DATE, "aliases": []},
    )
    metadata = _frontmatter(document)

    assert metadata["tags"] == expected["tags"]
    assert metadata["categories"] == expected["categories"]
    assert metadata["scenarios"] == expected["scenarios"]


def test_renderer_displays_only_signed_official_repository_and_paper_metadata() -> None:
    from ai_stack.historical_publication import (
        _render_body,
        capture_to_source_contract_item,
        render_historical_tier_c_markdown,
    )

    github_document = render_historical_tier_c_markdown(
        _capture("github_trending"),
        prior_metadata={"date": HISTORICAL_DATE, "aliases": []},
    )
    arxiv_document = render_historical_tier_c_markdown(
        _capture("arxiv"),
        prior_metadata={"date": HISTORICAL_DATE, "aliases": []},
    )

    assert "- **Forks**: 7" in github_document
    assert "- **许可证**: Apache-2.0" in github_document
    assert "- **Topics**: agent, rust" in github_document
    assert "- **论文时间**: 2026-07-17T01:02:03Z" in arxiv_document
    assert "https://arxiv.org/pdf/2607.12345v1.pdf" in arxiv_document

    contracted = capture_to_source_contract_item(_capture("github_trending"))
    contracted["license"] = "UNSIGNED LICENSE MUST NOT RENDER"
    body = _render_body(contracted)
    assert "Apache-2.0" in body
    assert "UNSIGNED LICENSE MUST NOT RENDER" not in body


def test_renderer_accepts_large_but_bounded_official_author_lists() -> None:
    from ai_stack.historical_publication import render_historical_tier_c_markdown

    base = _capture("arxiv")
    capture = replace(
        base,
        metadata={**base.metadata, "authors": [f"Author {index}" for index in range(34)]},
    )

    document = render_historical_tier_c_markdown(
        capture,
        prior_metadata={"date": HISTORICAL_DATE, "aliases": []},
    )

    assert "Author 0" in document
    assert "Author 33" in document
    assert analyze_post(document).status == "source_brief"


def test_renderer_escapes_untrusted_source_text_without_hiding_the_evidence() -> None:
    from ai_stack.historical_publication import render_historical_tier_c_markdown

    capture = HistoricalSourceCapture(
        source="blogs_podcasts",
        title='Unsafe <title> "quoted"',
        external_url="https://example.com/source",
        source_text=(
            '<script>alert("x")</script> {{< unsafe >}} '
            "[click](javascript:alert(1)) **bold** _italic_ `code`"
        ),
        captured_at=CAPTURED_AT,
        capture_mode="excerpt",
        source_completeness="partial",
        source_is_truncated=False,
        metadata={"author": '<img src=x onerror=alert("x")>'},
    )

    document = render_historical_tier_c_markdown(
        capture,
        prior_metadata={"date": HISTORICAL_DATE, "aliases": []},
    )

    assert "<script>" not in document
    assert "<img" not in document
    assert "{{<" not in document
    assert "[click](javascript:" not in document
    assert "&#123;&#123;&lt; unsafe &gt;&#125;&#125;" in document
    assert "\\[click\\]\\(javascript:alert\\(1\\)\\)" in document
    assert analyze_post(document).status == "source_brief"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("capture_mode", "metadata_only", "capture mode"),
        ("source_completeness", "complete", "completeness"),
        ("captured_at", "2026-07-18T02:03:04", "timezone"),
        ("external_url", "https://example.com/a > injected", "URL"),
        ("external_url", "https://[::1", "URL"),
    ),
)
def test_capture_adapter_rejects_inconsistent_or_unbounded_claims(
    field: str,
    value: object,
    message: str,
) -> None:
    from ai_stack.historical_publication import (
        HistoricalPublicationError,
        capture_to_source_contract_item,
    )

    base = _capture("arxiv")
    values = {
        "source": base.source,
        "title": base.title,
        "external_url": base.external_url,
        "source_text": base.source_text,
        "captured_at": base.captured_at,
        "capture_mode": base.capture_mode,
        "source_completeness": base.source_completeness,
        "source_is_truncated": base.source_is_truncated,
        "metadata": base.metadata,
    }
    values[field] = value
    capture = HistoricalSourceCapture(**values)

    with pytest.raises(HistoricalPublicationError, match=message):
        capture_to_source_contract_item(capture)


def test_renderer_rejects_unsafe_route_metadata() -> None:
    from ai_stack.historical_publication import (
        HistoricalPublicationError,
        render_historical_tier_c_markdown,
    )

    with pytest.raises(HistoricalPublicationError, match="date"):
        render_historical_tier_c_markdown(
            _capture("arxiv"),
            prior_metadata={"aliases": []},
        )
    with pytest.raises(HistoricalPublicationError, match="alias"):
        render_historical_tier_c_markdown(
            _capture("arxiv"),
            prior_metadata={
                "date": datetime.fromisoformat(HISTORICAL_DATE),
                "aliases": ["../../escape"],
            },
        )


@pytest.mark.parametrize(
    ("capture", "message"),
    (
        (replace(_capture("arxiv"), source="unsupported"), "unsupported"),
        (replace(_capture("arxiv"), title=""), "title is missing"),
        (replace(_capture("arxiv"), title="x" * 301), "title exceeds"),
        (replace(_capture("arxiv"), source_text=""), "source text is missing"),
        (
            replace(_capture("arxiv"), source_text="证" * (24 * 1024)),
            "evidence limit",
        ),
        (replace(_capture("arxiv"), source_is_truncated="yes"), "boolean"),
        (replace(_capture("arxiv"), metadata=[]), "metadata"),
        (replace(_capture("arxiv"), metadata={"authors": []}), "arxiv_id"),
        (
            replace(
                _capture("arxiv"),
                metadata={"arxiv_id": "2607.12345v1", "authors": "Ada"},
            ),
            "authors",
        ),
        (
            replace(_capture("github_trending"), metadata={"stars": -1}),
            "stars",
        ),
        (
            replace(_capture("github_trending"), metadata={"forks": -1}),
            "forks",
        ),
        (
            replace(_capture("github_trending"), metadata={"topics": "agent"}),
            "topics",
        ),
        (
            replace(
                _capture("arxiv"),
                metadata={
                    "arxiv_id": "2607.12345v1",
                    "authors": ["Ada Lovelace"],
                    "pdf_url": "https://evil.example/2607.12345v1.pdf",
                },
            ),
            "PDF URL",
        ),
        (
            replace(_capture("hacker_news"), source_text="different title"),
            "must match",
        ),
        (
            replace(_capture("hacker_news"), metadata={"hn_id": 0}),
            "hn_id",
        ),
        (
            replace(_capture("juejin"), metadata={"article_id": ""}),
            "article_id",
        ),
        (
            replace(
                _capture("juejin"),
                metadata={"article_id": "123"},
            ),
            "article_id",
        ),
        (_capture("juejin"), "marked truncated"),
        (
            replace(
                _capture("juejin", truncated=True),
                metadata={
                    "article_id": "7663304647513718799",
                    "source_truncation_reason": "unknown_reason",
                },
            ),
            "truncation reason",
        ),
    ),
)
def test_capture_adapter_fails_closed_on_malformed_capture_fields(
    capture: HistoricalSourceCapture,
    message: str,
) -> None:
    from ai_stack.historical_publication import (
        HistoricalPublicationError,
        capture_to_source_contract_item,
    )

    with pytest.raises(HistoricalPublicationError, match=message):
        capture_to_source_contract_item(capture)


@pytest.mark.parametrize(
    "prior_metadata",
    (
        [],
        {"date": "not-a-date", "aliases": []},
        {"date": "2026-01-25T12:39:55", "aliases": []},
        {"date": f" {HISTORICAL_DATE}", "aliases": []},
        {"date": HISTORICAL_DATE, "aliases": "/not-a-list/"},
        {"date": HISTORICAL_DATE, "aliases": [123]},
        {"date": HISTORICAL_DATE, "aliases": ["/route/?query=1"]},
        {"date": HISTORICAL_DATE, "aliases": [" /route/"]},
        {"date": HISTORICAL_DATE, "aliases": ["//["]},
    ),
)
def test_renderer_rejects_malformed_prior_metadata(prior_metadata: object) -> None:
    from ai_stack.historical_publication import (
        HistoricalPublicationError,
        render_historical_tier_c_markdown,
    )

    with pytest.raises(HistoricalPublicationError):
        render_historical_tier_c_markdown(
            _capture("arxiv"),
            prior_metadata=prior_metadata,
        )


def test_renderer_fails_closed_when_signed_source_text_trips_the_post_gate() -> None:
    from ai_stack.historical_publication import (
        HistoricalPublicationError,
        render_historical_tier_c_markdown,
    )

    capture = replace(
        _capture("blogs_podcasts"),
        source_text="你没有提供完整正文，因此只能根据标题推演生成文章内容。",
    )

    with pytest.raises(HistoricalPublicationError, match="quality gate"):
        render_historical_tier_c_markdown(
            capture,
            prior_metadata={"date": HISTORICAL_DATE, "aliases": []},
        )
