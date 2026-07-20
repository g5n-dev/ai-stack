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


def test_global_url_dedupe_retains_every_contracted_observation_for_lineage() -> None:
    orchestrator = _orchestrator()
    results = orchestrator._dedupe_results(
        {
            "hacker_news": [
                {
                    "source": "hacker_news",
                    "title": "Agent runtime release",
                    "url": "https://example.com/releases/runtime?utm_source=hn",
                    "hn_id": 456,
                    "crawled_at": "2026-07-15T12:00:00Z",
                }
            ],
            "blogs_podcasts": [
                {
                    "source": "blogs_podcasts",
                    "title": "Agent runtime release",
                    "url": "https://example.com/releases/runtime",
                    "description": "Official source-backed release excerpt.",
                    "feed_url": "https://example.com/feed.xml",
                    "published_at": "2026-07-15T10:00:00Z",
                    "crawled_at": "2026-07-15T12:01:00Z",
                }
            ],
        }
    )

    assert sum(len(items) for items in results.values()) == 1
    assert len(orchestrator.last_observations) == 2
    assert [item["source"] for item in orchestrator.last_observations] == [
        "blogs_podcasts",
        "hacker_news",
    ]
    assert all(
        item["url"] == "https://example.com/releases/runtime"
        for item in orchestrator.last_observations
    )
    assert all(item["evidence"]["schema_version"] == "source_evidence_v2" for item in orchestrator.last_observations)
