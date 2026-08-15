"""Bounded, provenance-preserving fallback for a mirrored X account feed."""

from __future__ import annotations

import json
import logging
import re
import time
import urllib.parse
from datetime import UTC, datetime, timedelta
from typing import Any

import requests

FALLBACK_ALLOWED_HOSTS = frozenset({"codex-reset.com"})
FALLBACK_PATH = "/api/feed"
MAX_FALLBACK_RESPONSE_BYTES = 512 * 1024
MAX_FALLBACK_TWEETS = 200
MAX_FALLBACK_TWEET_TEXT_CHARS = 20_000
FALLBACK_VERIFICATION_STATES = frozenset(
    {"confirmed", "rejected", "expired", "pending"}
)

logger = logging.getLogger(__name__)


def validated_fallback_url(value: object) -> str:
    """Return one allowlisted HTTPS feed URL, or an empty string."""

    raw = str(value or "").strip()
    try:
        parsed = urllib.parse.urlsplit(raw)
        port = parsed.port
    except ValueError:
        return ""
    if (
        parsed.scheme.casefold() != "https"
        or (parsed.hostname or "").casefold() not in FALLBACK_ALLOWED_HOSTS
        or parsed.username is not None
        or parsed.password is not None
        or port not in {None, 443}
        or parsed.path != FALLBACK_PATH
        or parsed.query
        or parsed.fragment
    ):
        return ""
    return raw


def _timestamp(value: object) -> datetime | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(UTC)


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def download_fallback_payload(feed_url: str, timeout_seconds: float) -> dict[str, Any]:
    """Download a small JSON object without following redirects."""

    validated = validated_fallback_url(feed_url)
    if not validated:
        return {}
    budget_seconds = max(1.0, min(float(timeout_seconds), 15.0))
    socket_timeout = min(budget_seconds, 5.0)
    deadline = time.monotonic() + budget_seconds
    try:
        with requests.get(
            validated,
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "identity",
                "User-Agent": "AI-Stack/1.0 reset-monitor",
            },
            timeout=(socket_timeout, socket_timeout),
            allow_redirects=False,
            stream=True,
        ) as response:
            if time.monotonic() > deadline:
                return {}
            if response.status_code != 200 or response.url != validated:
                return {}
            content_type = str(response.headers.get("Content-Type") or "")
            if content_type.split(";", 1)[0].strip().casefold() != "application/json":
                return {}
            declared_length = response.headers.get("Content-Length")
            if declared_length:
                try:
                    if int(declared_length) > MAX_FALLBACK_RESPONSE_BYTES:
                        return {}
                except ValueError:
                    return {}
            body = bytearray()
            for chunk in response.iter_content(chunk_size=64 * 1024):
                if time.monotonic() > deadline:
                    return {}
                body.extend(chunk)
                if len(body) > MAX_FALLBACK_RESPONSE_BYTES:
                    return {}
    except Exception as exc:  # noqa: BLE001 - fail closed on any transport error
        logger.warning("Structured Twitter fallback unavailable: %s", type(exc).__name__)
        return {}
    try:
        payload = json.loads(bytes(body).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def parse_fallback_feed(
    payload: object,
    *,
    account: str,
    feed_url: str,
    now: datetime | None = None,
    max_age_minutes: int = 90,
) -> list[dict[str, Any]]:
    """Validate a mirrored account feed and rebuild canonical X post records."""

    if not validated_fallback_url(feed_url):
        return []
    if not re.fullmatch(r"[A-Za-z0-9_]{1,15}", account):
        return []
    if not isinstance(payload, dict) or payload.get("stale") is not False:
        return []
    profile = payload.get("profile")
    if not isinstance(profile, dict):
        return []
    handle = str(profile.get("handle") or "").strip()
    if handle.casefold() != account.casefold():
        return []
    fetched_at = _timestamp(payload.get("fetched_at"))
    observed_now = now or datetime.now(UTC)
    if observed_now.tzinfo is None or observed_now.utcoffset() is None:
        return []
    observed_now = observed_now.astimezone(UTC)
    if fetched_at is None:
        return []
    age = observed_now - fetched_at
    if age < -timedelta(minutes=5) or age > timedelta(
        minutes=max(1, int(max_age_minutes))
    ):
        return []
    raw_tweets = payload.get("tweets")
    if not isinstance(raw_tweets, list) or len(raw_tweets) > MAX_FALLBACK_TWEETS:
        return []

    provider = str(payload.get("source") or "unknown").strip()[:80]
    captured_at = _iso(fetched_at)
    items: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for raw_tweet in raw_tweets:
        if not isinstance(raw_tweet, dict):
            continue
        tweet_id = str(raw_tweet.get("id") or "").strip()
        text = str(raw_tweet.get("text") or "").strip()
        published_at = _timestamp(raw_tweet.get("at"))
        if (
            not re.fullmatch(r"\d{8,24}", tweet_id)
            or tweet_id in seen_ids
            or not text
            or len(text) > MAX_FALLBACK_TWEET_TEXT_CHARS
            or published_at is None
            or published_at > fetched_at + timedelta(minutes=5)
        ):
            continue
        seen_ids.add(tweet_id)

        verification_status = str(
            raw_tweet.get("reset_verification_status") or ""
        ).strip().casefold()
        if verification_status not in FALLBACK_VERIFICATION_STATES:
            verification_status = ""

        item: dict[str, Any] = {
            "title": " ".join(text.split())[:80],
            "text": text,
            "timestamp": _iso(published_at),
            "published_at": _iso(published_at),
            "url": f"https://x.com/{account}/status/{tweet_id}",
            "tweet_id": tweet_id,
            "scraped_at": captured_at,
            "captured_at": captured_at,
            "account": account,
            "account_url": f"https://x.com/{account}",
            "source": "twitter",
            "feed_url": feed_url,
            "discovery_method": "structured_fallback",
            "fetch_status": "captured",
            "fallback_source": "independent_community_mirror",
            "fallback_provider": provider,
            "source_verification": "independent_mirror",
            "timestamp_confidence": "unknown",
        }
        if verification_status:
            item["reset_verification_status"] = verification_status
        for source_key, target_key in (
            ("likes", "likes"),
            ("reposts", "retweets"),
            ("replies", "replies"),
        ):
            metric = raw_tweet.get(source_key)
            if type(metric) is int and 0 <= metric <= 1_000_000_000:
                item[target_key] = metric
        items.append(item)
    return items


__all__ = [
    "download_fallback_payload",
    "parse_fallback_feed",
    "validated_fallback_url",
]
