from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import yaml

from ai_stack import twitter_fallback
from ai_stack.source_contract import apply_source_contract, verify_source_contract
from crawler.main import CrawlerOrchestrator
from crawler.twitter_crawler import TwitterCrawler, TwitterRecentCrawler

ROOT = Path(__file__).resolve().parents[1]


def _crawler() -> TwitterCrawler:
    crawler = TwitterCrawler.__new__(TwitterCrawler)
    crawler.base_url = "https://twitter.com"
    crawler.account_profiles = {
        "thsottiaux": {
            "include_replies": True,
            "monitor": "codex_usage_reset",
            "tags": ["Codex", "额度重置"],
        }
    }
    return crawler


def test_priority_account_profile_reads_replies_for_early_reset_hints() -> None:
    crawler = _crawler()

    assert crawler._account_crawl_url("thsottiaux") == (
        "https://twitter.com/thsottiaux/with_replies"
    )
    assert crawler._account_crawl_url("OpenAI") == "https://twitter.com/OpenAI"


def test_monitored_tweet_gets_structured_assessment_and_visible_title_label() -> None:
    crawler = _crawler()
    tweet = {
        "title": "I'll reset usage limits tomorrow",
        "text": "I'll reset Codex usage limits tomorrow.",
    }

    enriched = crawler._enrich_monitored_tweet(tweet, account="thsottiaux")

    assert enriched is not tweet
    assert enriched["title"].startswith("[额度重置已预告]")
    assert enriched["source_title_unclassified"] == "I'll reset usage limits tomorrow"
    assert enriched["signal_assessment"]["status"] == "promised"
    assert enriched["signal_assessment"]["notify"] is True
    assert enriched["tags"] == ["Codex", "额度重置", "重置预告"]


def test_irrelevant_tweet_is_retained_without_an_alarm_label() -> None:
    crawler = _crawler()
    tweet = {"title": "Computer History", "text": "Try the new Computer History plugin."}

    enriched = crawler._enrich_monitored_tweet(tweet, account="thsottiaux")

    assert enriched["title"] == "Computer History"
    assert enriched["signal_assessment"]["status"] == "insufficient_evidence"
    assert "source_title_unclassified" not in enriched
    assert enriched["tags"] == []


def test_unprofiled_account_is_not_reclassified() -> None:
    crawler = _crawler()
    tweet = {"title": "Reset the demo", "text": "I reset the demo."}

    enriched = crawler._enrich_monitored_tweet(tweet, account="OpenAI")

    assert enriched == tweet
    assert enriched is not tweet


def test_thsottiaux_is_a_production_priority_subscription_with_reset_focus() -> None:
    config = yaml.safe_load((ROOT / "config/sources.yaml").read_text(encoding="utf-8"))
    twitter = config["sources"]["twitter"]

    assert twitter["accounts"].count("thsottiaux") == 1
    assert twitter["priority_accounts"] == ["thsottiaux"]
    assert twitter["account_profiles"]["thsottiaux"] == {
        "include_replies": True,
        "monitor": "codex_usage_reset",
        "tags": ["Codex", "ChatGPT Work", "额度重置"],
        "fallback_feed_url": "https://codex-reset.com/api/feed",
        "fallback_max_age_minutes": 90,
        "lookback_minutes": 360,
    }


def test_ci_orchestrator_consumes_the_priority_profile() -> None:
    orchestrator = CrawlerOrchestrator(runtime_profile="ci")
    twitter = orchestrator.crawlers["twitter"]

    assert twitter.accounts == ["thsottiaux"]
    assert twitter.tweets_per_account == 8
    assert twitter.save_screenshots is False
    assert twitter._account_crawl_url("thsottiaux").endswith("/with_replies")


def test_structured_fallback_is_https_and_host_allowlisted() -> None:
    assert TwitterCrawler._validated_fallback_url("https://codex-reset.com/api/feed") == (
        "https://codex-reset.com/api/feed"
    )
    for invalid in (
        "http://codex-reset.com/api/feed",
        "https://evil.example/api/feed",
        "https://codex-reset.com.evil.example/api/feed",
        "https://user:pass@codex-reset.com/api/feed",
        "https://codex-reset.com:444/api/feed",
        "https://codex-reset.com:bad/api/feed",
        "https://codex-reset.com/other",
    ):
        assert TwitterCrawler._validated_fallback_url(invalid) == ""


def _fallback_payload(*, fetched_at: str = "2026-08-15T08:00:00Z") -> dict:
    return {
        "version": 1,
        "fetched_at": fetched_at,
        "source": "x-api",
        "stale": False,
        "profile": {"handle": "thsottiaux", "name": "Tibo"},
        "tweets": [
            {
                "id": "2089000000000000001",
                "url": "https://evil.example/ignored",
                "text": "I'll reset Codex usage limits tomorrow.",
                "at": "2026-08-15T07:55:00Z",
                "replies": 12,
                "reposts": 34,
                "likes": 56,
                "reset_verification_status": "confirmed",
            }
        ],
    }


def test_structured_fallback_rebuilds_original_urls_and_marks_provenance() -> None:
    crawler = _crawler()

    items = crawler._fallback_items_from_payload(
        _fallback_payload(),
        account="thsottiaux",
        feed_url="https://codex-reset.com/api/feed",
        now=datetime(2026, 8, 15, 8, 5, tzinfo=UTC),
        max_age_minutes=90,
    )

    assert len(items) == 1
    item = items[0]
    assert item["url"] == "https://x.com/thsottiaux/status/2089000000000000001"
    assert item["feed_url"] == "https://codex-reset.com/api/feed"
    assert item["discovery_method"] == "structured_fallback"
    assert item["fallback_source"] == "independent_community_mirror"
    assert item["source_verification"] == "independent_mirror"
    assert item["reset_verification_status"] == "confirmed"
    assert item["timestamp_confidence"] == "unknown"
    assert item["timestamp"] == "2026-08-15T07:55:00Z"
    assert item["scraped_at"] == "2026-08-15T08:00:00Z"
    assert item["title"].startswith("[独立镜像待核验]")
    assert item["signal_assessment"]["reported_status"] == "promised"
    assert item["signal_assessment"]["status"] == "watch"
    assert item["signal_assessment"]["notify"] is False

    contracted = apply_source_contract(item)
    verify_source_contract(contracted)
    assert contracted["evidence"]["origin_url"] == "https://codex-reset.com/api/feed"
    assert contracted["evidence"]["external_url"] == item["url"]
    assert contracted["timestamp_confidence"] == "unknown"
    assert contracted["evidence"]["fields"]["source_verification"] == (
        "independent_mirror"
    )
    assert contracted["evidence"]["fields"]["reset_verification_status"] == (
        "confirmed"
    )


def test_recent_crawler_uses_fallback_when_direct_x_only_returns_old_posts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    crawler = TwitterRecentCrawler(
        accounts=["thsottiaux"],
        tweets_per_account=8,
        lookback_minutes=90,
        save_screenshots=False,
        account_profiles={
            "thsottiaux": {
                "monitor": "codex_usage_reset",
                "lookback_minutes": 360,
                "fallback_feed_url": "https://codex-reset.com/api/feed",
            }
        },
    )
    old = {
        "title": "old cached post",
        "text": "old cached post",
        "timestamp": "2026-08-14T00:00:00Z",
    }
    fresh = {
        "title": "fresh fallback post",
        "text": "I'll reset Codex usage limits tomorrow.",
        "timestamp": "2026-08-15T07:55:00Z",
        "discovery_method": "structured_fallback",
    }
    calls: list[str] = []

    async def fake_direct(_self: TwitterCrawler, account: str) -> list[dict]:
        assert account == "thsottiaux"
        return [old]

    async def fake_fallback(account: str) -> list[dict]:
        calls.append(account)
        return [fresh]

    monkeypatch.setattr(TwitterCrawler, "crawl_account", fake_direct)
    monkeypatch.setattr(crawler, "_crawl_account_fallback", fake_fallback)
    monkeypatch.setattr(
        "crawler.twitter_crawler.datetime",
        type(
            "FixedDateTime",
            (datetime,),
            {
                "now": classmethod(
                    lambda cls, tz=None: datetime(2026, 8, 15, 8, 5, tzinfo=UTC)
                )
            },
        ),
    )

    items = asyncio.run(crawler.crawl_account("thsottiaux"))

    assert calls == ["thsottiaux"]
    assert items == [fresh]


def test_priority_profile_uses_six_hour_window_without_widening_other_accounts() -> None:
    crawler = TwitterRecentCrawler(
        accounts=["thsottiaux"],
        lookback_minutes=90,
        save_screenshots=False,
        account_profiles={"thsottiaux": {"lookback_minutes": 360}},
    )
    now = datetime(2026, 8, 15, 8, 0, tzinfo=UTC)
    four_hours_old = [{"timestamp": "2026-08-15T04:00:00Z"}]

    assert crawler._filter_recent(
        four_hours_old,
        account="thsottiaux",
        now=now,
    ) == four_hours_old
    assert crawler._filter_recent(
        four_hours_old,
        account="OpenAI",
        now=now,
    ) == []


def test_priority_monitor_merges_fresh_direct_and_fallback_posts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    crawler = TwitterRecentCrawler(
        accounts=["thsottiaux"],
        lookback_minutes=90,
        save_screenshots=False,
        account_profiles={
            "thsottiaux": {
                "monitor": "codex_usage_reset",
                "fallback_feed_url": "https://codex-reset.com/api/feed",
            }
        },
    )
    fresh = {
        "title": "fresh direct post",
        "text": "Codex update.",
        "timestamp": "2026-08-15T07:55:00Z",
    }

    async def fake_direct(_self: TwitterCrawler, _account: str) -> list[dict]:
        return [fresh]

    hidden_reset = {
        "title": "hidden reset reply",
        "text": "I'll reset Codex usage limits tomorrow.",
        "timestamp": "2026-08-15T07:54:00Z",
        "tweet_id": "2089000000000000001",
        "discovery_method": "structured_fallback",
        "signal_assessment": {
            "kind": "hard_reset",
            "status": "watch",
            "reported_status": "promised",
            "notify": False,
        },
    }
    calls: list[str] = []

    async def fake_fallback(account: str) -> list[dict]:
        calls.append(account)
        return [hidden_reset]

    monkeypatch.setattr(TwitterCrawler, "crawl_account", fake_direct)
    monkeypatch.setattr(crawler, "_crawl_account_fallback", fake_fallback)
    monkeypatch.setattr(
        "crawler.twitter_crawler.datetime",
        type(
            "FixedDateTime",
            (datetime,),
            {
                "now": classmethod(
                    lambda cls, tz=None: datetime(2026, 8, 15, 8, 5, tzinfo=UTC)
                )
            },
        ),
    )

    items = asyncio.run(crawler.crawl_account("thsottiaux"))

    assert calls == ["thsottiaux"]
    assert items == [hidden_reset, fresh]


def test_direct_tweet_wins_when_mirror_contains_the_same_tweet_id() -> None:
    crawler = TwitterRecentCrawler(
        accounts=["thsottiaux"],
        save_screenshots=False,
        account_profiles={"thsottiaux": {"monitor": "codex_usage_reset"}},
    )
    direct = {"tweet_id": "2089000000000000001", "text": "direct"}
    mirrored = {
        "tweet_id": "2089000000000000001",
        "text": "mirrored",
        "discovery_method": "structured_fallback",
    }

    assert crawler._merge_tweet_sources([direct], [mirrored]) == [direct]


def test_monitored_items_are_ordered_by_actionability_then_recency() -> None:
    crawler = _crawler()
    items = [
        {
            "title": "new but irrelevant",
            "text": "A new Codex feature.",
            "timestamp": "2026-08-15T08:00:00Z",
        },
        {
            "title": "watch",
            "text": "I'm feeling like a Codex limit reset.",
            "timestamp": "2026-08-15T07:58:00Z",
        },
        {
            "title": "promise",
            "text": "I'll reset Codex usage limits tomorrow.",
            "timestamp": "2026-08-15T07:57:00Z",
        },
    ]
    enriched = [
        crawler._enrich_monitored_tweet(item, account="thsottiaux")
        for item in items
    ]

    ordered = crawler._prioritize_monitored_tweets(enriched, account="thsottiaux")

    assert [item["signal_assessment"]["status"] for item in ordered] == [
        "promised",
        "watch",
        "insufficient_evidence",
    ]


def test_structured_fallback_fails_closed_on_identity_freshness_and_shape() -> None:
    crawler = _crawler()
    now = datetime(2026, 8, 15, 8, 5, tzinfo=UTC)

    stale_flag = _fallback_payload()
    stale_flag["stale"] = True
    wrong_handle = _fallback_payload()
    wrong_handle["profile"]["handle"] = "attacker"
    stale_timestamp = _fallback_payload(
        fetched_at=(now - timedelta(hours=2)).isoformat().replace("+00:00", "Z")
    )
    invalid_tweets = _fallback_payload()
    invalid_tweets["tweets"] = "not-an-array"

    for payload in (stale_flag, wrong_handle, stale_timestamp, invalid_tweets):
        assert crawler._fallback_items_from_payload(
            payload,
            account="thsottiaux",
            feed_url="https://codex-reset.com/api/feed",
            now=now,
            max_age_minutes=90,
        ) == []


def test_structured_fallback_skips_invalid_items_and_bounds_untrusted_text() -> None:
    crawler = _crawler()
    payload = _fallback_payload()
    payload["tweets"] = [
        {"id": "not-digits", "text": "reset", "at": "2026-08-15T07:55:00Z"},
        {
            "id": "2089000000000000002",
            "text": "x" * 20_001,
            "at": "2026-08-15T07:55:00Z",
        },
        {"id": "2089000000000000003", "text": "", "at": "2026-08-15T07:55:00Z"},
    ]

    assert crawler._fallback_items_from_payload(
        payload,
        account="thsottiaux",
        feed_url="https://codex-reset.com/api/feed",
        now=datetime(2026, 8, 15, 8, 5, tzinfo=UTC),
        max_age_minutes=90,
    ) == []


class _FallbackResponse:
    def __init__(
        self,
        body: bytes,
        *,
        status_code: int = 200,
        url: str = "https://codex-reset.com/api/feed",
        content_type: str = "application/json; charset=utf-8",
        content_length: str | None = None,
    ) -> None:
        self.body = body
        self.status_code = status_code
        self.url = url
        self.headers = {"Content-Type": content_type}
        if content_length is not None:
            self.headers["Content-Length"] = content_length

    def __enter__(self) -> _FallbackResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def iter_content(self, *, chunk_size: int) -> list[bytes]:
        assert chunk_size == 64 * 1024
        return [self.body]


def test_fallback_download_is_bounded_and_never_follows_redirects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = json.dumps(_fallback_payload()).encode()
    calls: list[dict] = []

    def fake_get(_url: str, **kwargs: object) -> _FallbackResponse:
        calls.append(kwargs)
        return _FallbackResponse(body, content_length=str(len(body)))

    monkeypatch.setattr(twitter_fallback.requests, "get", fake_get)

    payload = twitter_fallback.download_fallback_payload(
        "https://codex-reset.com/api/feed", 999
    )

    assert payload["profile"]["handle"] == "thsottiaux"
    assert calls[0]["allow_redirects"] is False
    assert calls[0]["stream"] is True
    assert calls[0]["timeout"] == (5.0, 5.0)
    assert calls[0]["headers"]["Accept-Encoding"] == "identity"


@pytest.mark.parametrize(
    "response",
    [
        _FallbackResponse(b"{}", status_code=302),
        _FallbackResponse(b"{}", url="https://evil.example/api/feed"),
        _FallbackResponse(b"{}", content_type="text/html"),
        _FallbackResponse(b"{}", content_length="not-an-integer"),
        _FallbackResponse(
            b"{}",
            content_length=str(twitter_fallback.MAX_FALLBACK_RESPONSE_BYTES + 1),
        ),
        _FallbackResponse(b"x" * (twitter_fallback.MAX_FALLBACK_RESPONSE_BYTES + 1)),
        _FallbackResponse(b"not-json"),
        _FallbackResponse(b"[]"),
    ],
)
def test_fallback_download_rejects_invalid_or_unbounded_responses(
    monkeypatch: pytest.MonkeyPatch,
    response: _FallbackResponse,
) -> None:
    monkeypatch.setattr(twitter_fallback.requests, "get", lambda *_a, **_k: response)

    assert twitter_fallback.download_fallback_payload(
        "https://codex-reset.com/api/feed", 10
    ) == {}


def test_fallback_download_enforces_a_total_wall_clock_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = json.dumps(_fallback_payload()).encode()
    response = _FallbackResponse(body)
    ticks = iter([0.0, 0.0, 16.0])
    monkeypatch.setattr(twitter_fallback.requests, "get", lambda *_a, **_k: response)
    monkeypatch.setattr(twitter_fallback.time, "monotonic", lambda: next(ticks))

    assert twitter_fallback.download_fallback_payload(
        "https://codex-reset.com/api/feed", 15
    ) == {}


def test_fallback_download_fails_closed_on_transport_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def explode(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("network unavailable")

    monkeypatch.setattr(twitter_fallback.requests, "get", explode)

    assert twitter_fallback.download_fallback_payload(
        "https://codex-reset.com/api/feed", 10
    ) == {}
