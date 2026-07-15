from __future__ import annotations

from datetime import UTC, datetime

from ai_stack.source_contract import apply_source_contract, verify_source_contract
from crawler.blogs_podcasts import BlogsPodcastsCrawler, FeedConfig, _html_to_text


def _entry(*, summary: str, content: str, title: str = "Complete AI feed title") -> dict:
    return {
        "title": title,
        "link": "https://example.com/complete-feed-entry",
        "summary": summary,
        "content": [{"type": "text/html", "value": content}],
        "published": "Wed, 15 Jul 2026 12:00:00 GMT",
        "published_parsed": datetime(2026, 7, 15, 12, tzinfo=UTC).timetuple(),
    }


def test_html_capture_preserves_readable_block_boundaries() -> None:
    captured = _html_to_text(
        "<h2>Architecture</h2>"
        "<p>The first <strong>complete</strong> paragraph.</p>"
        "<ul><li>Review stage</li><li>Generation stage</li></ul>"
        "<p>The complete conclusion.</p>"
    )

    assert captured.split("\n\n") == [
        "Architecture",
        "The first complete paragraph.",
        "Review stage",
        "Generation stage",
        "The complete conclusion.",
    ]


def test_feed_content_recovers_a_broken_short_summary_without_model_inference() -> None:
    crawler = BlogsPodcastsCrawler(feeds=[], limit=1)
    item = crawler._extract_entry(
        _entry(
            summary=("Flo Health built a production-grade medical content review system. T"),
            content=(
                "<p>Flo Health built a production-grade medical content review system. "
                "This system reduced review time by 60 percent and tripled content "
                "throughput without expanding the medical team.</p>"
            ),
            title=("Scaling medical content review at Flo Health with Amazon Bedrock – Part 2"),
        ),
        FeedConfig(
            name="AWS Machine Learning Blog",
            url="https://aws.amazon.com/blogs/machine-learning/feed/",
        ),
    )

    assert item is not None
    assert item["description"].endswith("without expanding the medical team.")
    assert not item["description"].endswith(". T")
    assert item["source_is_truncated"] is False
    assert item["source_truncation_reason"] == ""

    contracted = apply_source_contract(item)
    assert contracted["source_display_excerpt"] == item["description"]
    assert contracted["source_is_truncated"] is False
    verify_source_contract(contracted)


def test_feed_content_limit_is_word_safe_and_explicitly_propagated() -> None:
    crawler = BlogsPodcastsCrawler(feeds=[], limit=1)
    content = "<p>" + ("complete-token " * 5_000) + "final-token.</p>"

    item = crawler._extract_entry(
        _entry(summary="Short summary.", content=content),
        FeedConfig(name="Long Feed", url="https://example.com/feed.xml"),
    )

    assert item is not None
    assert len(item["description"].encode("utf-8")) <= 24 * 1024
    assert item["description"].endswith("complete-token")
    assert item["source_is_truncated"] is True
    assert item["source_truncation_reason"] == "crawler_feed_content_limit"

    contracted = apply_source_contract(item)
    assert contracted["source_display_excerpt"] == item["description"]
    assert contracted["source_is_truncated"] is True
    assert "crawler_feed_content_limit" in contracted["source_truncation_reason"]
    assert "publication_excerpt_limit" not in contracted["source_truncation_reason"]
    verify_source_contract(contracted)
