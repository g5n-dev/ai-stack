from __future__ import annotations

import pytest

from ai_stack import source_contract
from ai_stack.source_contract import (
    SourceContractError,
    apply_source_contract,
    verify_source_contract,
)
from processor.ai_filter import AIThemeFilter
from processor.main import ProcessorOrchestrator
from processor.summarizer import ContentSummarizer


class _Explodes:
    def __getattr__(self, name: str):
        raise AssertionError(f"metadata-only source must not call {name}")


def test_hacker_news_contract_is_metadata_only_and_deterministic() -> None:
    item = {
        "source": "hacker_news",
        "title": "A new AI runtime",
        "url": "https://example.com/story?utm_source=hn",
        "author": "ada",
        "score": 42,
        "descendants": 7,
        "hn_id": 123,
        "crawled_at": "2026-07-15T12:00:00+00:00",
    }

    first = apply_source_contract(item)
    second = apply_source_contract(item)

    assert first == second
    assert first["source_capture_mode"] == "metadata_only"
    assert first["content_mode"] == "source_brief"
    assert first["publication_tier"] == "C"
    assert first["source_text_chars"] == len(item["title"])
    assert first["source_snapshot_sha256"].startswith("sha256:")
    assert first["source_is_truncated"] is False
    assert first["source_summary_original"] == ""
    verify_source_contract(first)

    tampered = dict(first)
    tampered["evidence"] = dict(first["evidence"])
    tampered["evidence"]["fields"] = dict(first["evidence"]["fields"])
    tampered["evidence"]["fields"]["score"] = 999
    with pytest.raises(SourceContractError, match="digest"):
        verify_source_contract(tampered)

    top_level_tampered = dict(first)
    top_level_tampered["source_text_original"] = "A rewritten title"
    with pytest.raises(SourceContractError, match="source text"):
        verify_source_contract(top_level_tampered)

    truncation_tampered = dict(first)
    truncation_tampered["source_is_truncated"] = True
    with pytest.raises(SourceContractError, match="truncation"):
        verify_source_contract(truncation_tampered)

    url_tampered = dict(first)
    url_tampered["url"] = "https://evil.example/replacement"
    with pytest.raises(SourceContractError, match="external URL"):
        verify_source_contract(url_tampered)

    title_tampered = dict(first)
    title_tampered["title"] = "A rewritten title"
    with pytest.raises(SourceContractError, match="title"):
        verify_source_contract(title_tampered)


def test_contract_normalizes_source_identity_and_accepts_string_hn_ids() -> None:
    contracted = apply_source_contract(
        {
            "source": "Hacker_News",
            "title": "Canonical identity",
            "url": "https://example.com/story",
            "hn_id": "123",
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )

    assert contracted["source"] == "hacker_news"
    assert contracted["evidence"]["origin_url"].endswith("/123.json")
    verify_source_contract(contracted)


def test_existing_contract_cannot_be_rehashed_after_downstream_tampering() -> None:
    contracted = apply_source_contract(
        {
            "source": "arxiv",
            "title": "Evidence-aware agents",
            "url": "https://arxiv.org/abs/2607.12345",
            "summary": "Original abstract text.",
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )
    tampered = dict(contracted)
    tampered["source_summary_original"] = "Downstream rewritten abstract."

    with pytest.raises(SourceContractError, match="source summary"):
        apply_source_contract(tampered)


def test_contract_rejects_unknown_sources_and_missing_minimum_evidence() -> None:
    with pytest.raises(SourceContractError, match="unsupported source"):
        apply_source_contract(
            {
                "source": "unknown",
                "title": "AI item",
                "url": "https://example.com/item",
            }
        )
    with pytest.raises(SourceContractError, match="title"):
        apply_source_contract(
            {
                "source": "arxiv",
                "title": "",
                "url": "https://arxiv.org/abs/2607.12345",
                "summary": "Abstract",
            }
        )
    with pytest.raises(SourceContractError, match="source text"):
        apply_source_contract(
            {
                "source": "arxiv",
                "title": "AI paper",
                "url": "https://arxiv.org/abs/2607.12345",
                "summary": "",
                "crawled_at": "2026-07-15T12:00:00Z",
            }
        )


def test_contract_keeps_full_payload_hash_and_publishes_all_stored_evidence() -> None:
    original = "智能体证据段落。" * 2_000
    contracted = apply_source_contract(
        {
            "source": "juejin",
            "title": "AI 智能体证据",
            "url": "https://juejin.cn/post/123",
            "description": original,
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )

    assert contracted["source_payload_sha256"].startswith("sha256:")
    assert contracted["source_text_chars_original"] == len(original)
    assert contracted["source_display_excerpt"] == contracted["source_text_original"]
    assert len(contracted["source_display_excerpt"].encode("utf-8")) <= 24 * 1024
    assert contracted["source_is_truncated"] is True
    assert "source_contract_limit" in contracted["source_truncation_reason"]
    assert "publication_excerpt_limit" not in contracted["source_truncation_reason"]
    verify_source_contract(contracted)


def test_contract_publishes_a_complete_stored_english_capture() -> None:
    original = "complete-token " * 1_000
    contracted = apply_source_contract(
        {
            "source": "arxiv",
            "title": "Word-safe source excerpt",
            "url": "https://arxiv.org/abs/2607.54321",
            "summary": original,
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )

    assert contracted["source_display_excerpt"] == original.strip()
    assert contracted["source_is_truncated"] is False
    assert contracted["source_truncation_reason"] == ""
    verify_source_contract(contracted)


def test_verifier_accepts_the_pinned_legacy_v1_display_derivative() -> None:
    contracted = apply_source_contract(
        {
            "source": "arxiv",
            "title": "Legacy v1 display derivative",
            "url": "https://arxiv.org/abs/2607.54322",
            "summary": "complete-token " * 1_000,
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )
    evidence = contracted["evidence"]
    evidence["is_truncated"] = True
    evidence["truncation_reason"] = "publication_excerpt_limit"
    evidence["digest"] = source_contract._evidence_digest(evidence)
    contracted["source_snapshot_sha256"] = evidence["digest"]
    contracted["source_display_excerpt"] = source_contract._truncate_utf8(
        contracted["source_text_original"], 6_000
    )[0]
    contracted["source_is_truncated"] = True
    contracted["source_truncation_reason"] = "publication_excerpt_limit"

    verify_source_contract(contracted)


def test_verifier_accepts_a_frozen_v1_digest_without_v2_fields() -> None:
    contracted = apply_source_contract(
        {
            "source": "hacker_news",
            "title": "Frozen legacy contract",
            "url": "https://example.com/story",
            "author": "ada",
            "score": 42,
            "descendants": 7,
            "hn_id": 123,
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )
    for name in ("source_completeness", "parent_snapshot_sha256"):
        contracted.pop(name)
        contracted["evidence"].pop(name)
    contracted["evidence"]["schema_version"] = "source_evidence_v1"
    frozen_digest = "sha256:c7e7df981bf0b72977079842fca694b37d34b6184efd1218a57175c1bf9917c9"
    contracted["evidence"]["digest"] = frozen_digest
    contracted["source_snapshot_sha256"] = frozen_digest

    verify_source_contract(contracted)


def test_contract_bounds_publication_title_without_mutating_immutable_title() -> None:
    title = ("complete-title-token " * 30) + "final-token"
    contracted = apply_source_contract(
        {
            "source": "hacker_news",
            "title": title,
            "url": "https://example.com/long-title",
            "hn_id": 987,
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )

    assert contracted["evidence"]["fields"]["title"] == title
    assert contracted["source_title_chars_original"] == len(title)
    assert len(contracted["source_display_title"]) <= 300
    assert contracted["source_display_title"].endswith("complete-title-token")
    assert contracted["source_is_truncated"] is True
    assert "publication_title_limit" in contracted["source_truncation_reason"]
    verify_source_contract(contracted)


def test_explicit_false_does_not_trigger_the_legacy_2000_character_rss_rule() -> None:
    contracted = apply_source_contract(
        {
            "source": "blogs_podcasts",
            "title": "Exactly bounded feed text",
            "url": "https://example.com/exactly-bounded",
            "description": "x" * 2_000,
            "source_is_truncated": False,
            "source_truncation_reason": "",
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )

    assert contracted["source_is_truncated"] is False
    assert contracted["source_truncation_reason"] == ""
    verify_source_contract(contracted)


def test_contract_digest_excludes_capture_time_and_search_snippets_are_metadata_only() -> None:
    base = {
        "source": "juejin",
        "title": "AI agent notes",
        "url": "https://juejin.cn/post/1",
        "description": "search result snippet",
        "discovery_method": "search_fallback",
    }
    first = apply_source_contract({**base, "crawled_at": "2026-07-15T12:00:00Z"})
    second = apply_source_contract({**base, "crawled_at": "2026-07-15T13:00:00Z"})

    assert first["source_snapshot_sha256"] == second["source_snapshot_sha256"]
    assert first["source_capture_mode"] == "metadata_only"
    assert first["content_mode"] == "source_brief"


def test_v2_contract_separates_capture_and_source_publication_times() -> None:
    contracted = apply_source_contract(
        {
            "source": "blogs_podcasts",
            "title": "A verifiable release",
            "url": "https://example.com/releases/agent-runtime",
            "description": "The runtime release includes deterministic evidence metadata.",
            "published_at": "2026-07-15T10:00:00Z",
            "crawled_at": "2026-07-15T12:00:00Z",
            "feed_url": "https://example.com/feed.xml",
        }
    )

    assert contracted["evidence"]["schema_version"] == "source_evidence_v2"
    assert contracted["captured_at"] == "2026-07-15T12:00:00Z"
    assert contracted["source_published_at"] == "2026-07-15T10:00:00Z"
    assert contracted["timestamp_confidence"] == "feed"
    assert contracted["evidence"]["source_published_at"] == "2026-07-15T10:00:00Z"
    verify_source_contract(contracted)


def test_v2_contract_never_substitutes_publication_time_for_capture_time() -> None:
    with pytest.raises(SourceContractError, match="capture time"):
        apply_source_contract(
            {
                "source": "arxiv",
                "title": "Publication time is not observation time",
                "url": "https://arxiv.org/abs/2607.99999",
                "summary": "A sufficiently complete abstract for the source contract.",
                "published_at": "2026-07-15T10:00:00Z",
            }
        )


def test_v2_timestamp_metadata_is_hash_bound() -> None:
    contracted = apply_source_contract(
        {
            "source": "reddit",
            "title": "Agent release discussion",
            "url": "https://reddit.com/r/MachineLearning/comments/abc123/release",
            "selftext": "Source-backed community discussion about an agent runtime release.",
            "published_at": "2026-07-15T10:00:00Z",
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )
    tampered = dict(contracted)
    tampered["evidence"] = dict(contracted["evidence"])
    tampered["evidence"]["source_published_at"] = "2026-07-14T10:00:00Z"

    with pytest.raises(SourceContractError, match="digest"):
        verify_source_contract(tampered)


def test_feed_publication_time_is_normalized_to_utc_and_unstructured_time_is_ignored() -> None:
    feed = apply_source_contract(
        {
            "source": "juejin",
            "title": "Structured feed time",
            "url": "https://juejin.cn/post/structured-time",
            "description": "A bounded RSS discovery excerpt.",
            "published": "Wed, 15 Jul 2026 10:00:00 +0800",
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )
    fallback = apply_source_contract(
        {
            "source": "juejin",
            "title": "Unstructured search time",
            "url": "https://juejin.cn/post/unstructured-time",
            "description": "search result snippet",
            "published_at": "昨天",
            "discovery_method": "search_fallback",
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )

    assert feed["source_published_at"] == "2026-07-15T02:00:00Z"
    assert feed["timestamp_confidence"] == "feed"
    assert fallback["source_published_at"] == ""
    assert fallback["timestamp_confidence"] == "unknown"


def test_arxiv_contract_preserves_original_abstract() -> None:
    item = {
        "source": "arxiv",
        "title": "Evidence-aware agents",
        "url": "https://arxiv.org/abs/2607.12345",
        "summary": "Original abstract text.",
        "crawled_at": "2026-07-15T12:00:00+00:00",
    }

    contracted = apply_source_contract(item)

    assert contracted["source_capture_mode"] == "abstract"
    assert contracted["content_mode"] == "source_brief"
    assert contracted["source_summary_original"] == "Original abstract text."
    assert contracted["source_text_original"] == "Original abstract text."


def test_contract_signs_official_arxiv_metadata_and_detects_tampering() -> None:
    item = {
        "source": "arxiv",
        "title": "Evidence-aware agents",
        "url": "https://arxiv.org/abs/2607.12345v1",
        "summary": "Original abstract text.",
        "arxiv_id": "2607.12345v1",
        "authors": ["Ada Lovelace"],
        "category": "cs.AI",
        "published": "2026-07-17T01:02:03Z",
        "pdf_url": "https://arxiv.org/pdf/2607.12345v1.pdf",
        "crawled_at": "2026-07-18T02:03:04Z",
    }

    contracted = apply_source_contract(item)
    fields = contracted["evidence"]["fields"]

    assert fields["published"] == item["published"]
    assert fields["pdf_url"] == item["pdf_url"]
    verify_source_contract(contracted)

    tampered = dict(contracted)
    tampered["evidence"] = dict(contracted["evidence"])
    tampered["evidence"]["fields"] = dict(fields)
    tampered["evidence"]["fields"]["pdf_url"] = "https://evil.example/paper.pdf"
    with pytest.raises(SourceContractError, match="digest"):
        verify_source_contract(tampered)


def test_contract_signs_official_github_metadata_and_detects_tampering() -> None:
    item = {
        "source": "github_trending",
        "title": "octo/evidence-agent",
        "url": "https://github.com/octo/evidence-agent",
        "description": "A Rust agent runtime.",
        "language": "Rust",
        "stars": 123,
        "today_stars": 5,
        "forks": 7,
        "license": "Apache-2.0",
        "topics": ["agent", "rust"],
        "crawled_at": "2026-07-18T02:03:04Z",
    }

    contracted = apply_source_contract(item)
    fields = contracted["evidence"]["fields"]

    assert fields["forks"] == "7"
    assert fields["license"] == "Apache-2.0"
    assert fields["topics"] == ["agent", "rust"]
    verify_source_contract(contracted)

    tampered = dict(contracted)
    tampered["evidence"] = dict(contracted["evidence"])
    tampered["evidence"]["fields"] = dict(fields)
    tampered["evidence"]["fields"]["license"] = "MIT"
    with pytest.raises(SourceContractError, match="digest"):
        verify_source_contract(tampered)


def test_hacker_news_processor_returns_source_brief_without_any_llm_call() -> None:
    processor = ProcessorOrchestrator.__new__(ProcessorOrchestrator)
    processor.ai_filter = AIThemeFilter(_Explodes(), {"enabled": True})
    processor.summarizer = _Explodes()
    processor.translator = _Explodes()
    processor.generator = _Explodes()
    processor.tagger = _Explodes()
    processor.scenario_analyzer = _Explodes()

    result = processor.process_single(
        apply_source_contract(
            {
                "source": "hacker_news",
                "title": "A new AI runtime",
                "url": "https://example.com/story",
                "author": "ada",
                "score": 42,
                "descendants": 7,
                "hn_id": 123,
                "crawled_at": "2026-07-15T12:00:00+00:00",
            }
        )
    )

    assert result["content_mode"] == "source_brief"
    assert result["catchy_title"] == "A new AI runtime"
    assert result["tags"] == ["Hacker News", "来源快报"]
    assert result["categories"] == []
    assert result["scenarios"] == []
    assert "不生成扩展判断" in result["source_note"]


def test_non_ai_source_brief_is_rejected_without_any_llm_call() -> None:
    processor = ProcessorOrchestrator.__new__(ProcessorOrchestrator)
    processor.ai_filter = AIThemeFilter(_Explodes(), {"enabled": True})
    processor.summarizer = _Explodes()
    processor.translator = _Explodes()
    processor.generator = _Explodes()
    processor.tagger = _Explodes()
    processor.scenario_analyzer = _Explodes()

    result = processor.process_single(
        apply_source_contract(
            {
                "source": "hacker_news",
                "title": "PostgreSQL vacuum internals",
                "url": "https://example.com/postgres-vacuum",
                "hn_id": 456,
                "crawled_at": "2026-07-15T12:00:00+00:00",
            }
        )
    )

    assert result["skip_post"] is True
    assert result["ai_related"] is False
    assert result["should_publish"] is False


def test_source_brief_tags_are_derived_from_immutable_crawler_evidence() -> None:
    processor = ProcessorOrchestrator.__new__(ProcessorOrchestrator)
    processor.ai_filter = AIThemeFilter(_Explodes(), {"enabled": True})
    processor.summarizer = _Explodes()
    processor.translator = _Explodes()
    processor.generator = _Explodes()
    processor.tagger = _Explodes()
    processor.scenario_analyzer = _Explodes()
    contracted = apply_source_contract(
        {
            "source": "arxiv",
            "title": "RAG agents with verifiable evidence",
            "url": "https://arxiv.org/abs/2607.54321",
            "summary": "A retrieval augmented generation agent benchmark.",
            "category": "cs.AI",
            "tags": ["RAG"],
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )
    tampered = dict(contracted)
    tampered["tags"] = ["区块链"]
    tampered["category"] = "cs.CR"

    result = processor.process_single(tampered)

    assert "RAG" in result["tags"]
    assert "cs.AI" in result["tags"]
    assert "区块链" not in result["tags"]
    assert "cs.CR" not in result["tags"]


def test_mutable_top_level_tags_cannot_make_non_ai_evidence_publishable() -> None:
    processor = ProcessorOrchestrator.__new__(ProcessorOrchestrator)
    processor.ai_filter = AIThemeFilter(_Explodes(), {"enabled": True})
    processor.summarizer = _Explodes()
    processor.translator = _Explodes()
    processor.generator = _Explodes()
    processor.tagger = _Explodes()
    processor.scenario_analyzer = _Explodes()
    contracted = apply_source_contract(
        {
            "source": "hacker_news",
            "title": "PostgreSQL vacuum internals",
            "url": "https://example.com/postgres-vacuum-2",
            "hn_id": 789,
            "tags": [],
            "crawled_at": "2026-07-15T12:00:00Z",
        }
    )
    tampered = dict(contracted)
    tampered["tags"] = ["AI", "LLM", "Agent"]

    result = processor.process_single(tampered)

    assert result["skip_post"] is True
    assert result["ai_related"] is False
    assert result["should_publish"] is False


def test_processor_fails_closed_when_crawler_evidence_is_missing() -> None:
    processor = ProcessorOrchestrator.__new__(ProcessorOrchestrator)
    processor.ai_filter = _Explodes()

    result = processor.process_single(
        {
            "source": "hacker_news",
            "title": "LLM runtime",
            "url": "https://example.com/llm-runtime",
        }
    )

    assert result["skip_post"] is True
    assert result["should_publish"] is False
    assert "source evidence" in result["processing_error"]


def test_article_summarizer_never_overwrites_original_source_summary() -> None:
    summarizer = ContentSummarizer.__new__(ContentSummarizer)
    summarizer.summarize = lambda _content, style="concise": "Generated Chinese summary"
    item = {
        "source": "arxiv",
        "title": "Evidence-aware agents",
        "summary": "Original abstract text.",
        "source_summary_original": "Original abstract text.",
    }

    result = summarizer.summarize_article(item)

    assert result["summary"] == "Original abstract text."
    assert result["source_summary_original"] == "Original abstract text."
    assert result["generated_summary"] == "Generated Chinese summary"
