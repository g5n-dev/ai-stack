from __future__ import annotations

from crawler.main import CrawlerOrchestrator


def _orchestrator() -> CrawlerOrchestrator:
    orchestrator = CrawlerOrchestrator.__new__(CrawlerOrchestrator)
    orchestrator.dedupe = True
    orchestrator.dedupe_scope = "global"
    return orchestrator


def test_global_dedupe_keeps_the_strongest_source_evidence_independent_of_order() -> None:
    hn = {
        "source": "hacker_news",
        "title": "OpenAI agent update",
        "url": "https://example.com/openai-agent",
        "hn_id": 123,
        "crawled_at": "2026-07-15T12:00:00Z",
    }
    rss = {
        "source": "blogs_podcasts",
        "title": "OpenAI agent update",
        "url": "https://example.com/openai-agent",
        "description": "Official RSS excerpt with source-backed details.",
        "feed_url": "https://example.com/feed.xml",
        "crawled_at": "2026-07-15T12:01:00Z",
    }

    first = _orchestrator()._dedupe_results(
        {"hacker_news": [hn], "blogs_podcasts": [rss]}
    )
    second = _orchestrator()._dedupe_results(
        {"blogs_podcasts": [rss], "hacker_news": [hn]}
    )

    assert first["hacker_news"] == []
    assert first["blogs_podcasts"][0]["source_capture_mode"] == "excerpt"
    assert second["hacker_news"] == []
    assert second["blogs_podcasts"] == first["blogs_podcasts"]
