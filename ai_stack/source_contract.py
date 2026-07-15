"""Deterministic source-evidence contracts for the production content path.

This module does not fetch arbitrary URLs.  It records exactly what each
crawler already captured, so downstream generators cannot mistake metadata or
an excerpt for a full article.
"""

from __future__ import annotations

import hashlib
import hmac
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

from ._json import canonical_json_bytes
from .identity import canonicalize_url

EXTRACTOR_VERSION = "source-contract-v1"
EVIDENCE_SCHEMA = "source_evidence_v1"
_MAX_EVIDENCE_BYTES = 64 * 1024
_MAX_STORED_SOURCE_BYTES = 24 * 1024
_MAX_DISPLAY_EXCERPT_BYTES = 6_000
_ALLOWED_SOURCES = frozenset(
    {
        "arxiv",
        "blogs_podcasts",
        "github_trending",
        "hacker_news",
        "juejin",
        "reddit",
        "twitter",
    }
)


class SourceContractError(ValueError):
    """Raised when source evidence cannot be verified exactly."""


def _text(value: object) -> str:
    return str(value or "").strip()


def _truncate_utf8(value: str, limit: int) -> tuple[str, bool]:
    raw = str(value or "").encode("utf-8")
    if len(raw) <= limit:
        return str(value or ""), False
    return raw[:limit].decode("utf-8", errors="ignore").rstrip(), True


def _source_summary(source: str, item: Mapping[str, Any]) -> str:
    if source == "hacker_news":
        return ""
    if source == "arxiv":
        return _text(item.get("summary"))
    if source in {"blogs_podcasts", "juejin"}:
        return _text(item.get("summary") or item.get("description"))
    if source == "github_trending":
        return _text(item.get("description"))
    if source == "twitter":
        return _text(item.get("text"))
    if source == "reddit":
        return _text(item.get("selftext") or item.get("description"))
    return ""


def _canonical_url(item: Mapping[str, Any]) -> str:
    raw = _text(item.get("url") or item.get("repo_url") or item.get("external_url"))
    if not raw:
        return ""
    try:
        return canonicalize_url(raw)
    except ValueError:
        return ""


def _capture(item: Mapping[str, Any]) -> tuple[str, str, str, str]:
    source = _text(item.get("source")).casefold()
    original_summary = _source_summary(source, item)
    if _text(item.get("discovery_method")).casefold() == "search_fallback":
        return "metadata_only", "source_brief", _text(item.get("title")), "search_fallback"
    if source == "hacker_news":
        return "metadata_only", "source_brief", _text(item.get("title")), "api_metadata"
    if source == "arxiv":
        return "abstract", "source_brief", original_summary, "arxiv_api"
    if source in {"blogs_podcasts", "juejin"}:
        return "excerpt", "source_brief", original_summary, "rss_excerpt"
    if source == "github_trending":
        evidence = _text(item.get("description"))
        return "metadata_only", "source_brief", evidence or _text(item.get("title")), "repository_metadata"
    if source in {"twitter", "reddit"}:
        evidence = _text(item.get("text") or item.get("selftext") or item.get("description"))
        if evidence:
            return "social_post", "source_brief", evidence, "social_api"
        return "metadata_only", "source_brief", _text(item.get("title")), "social_metadata"
    raise SourceContractError(f"unsupported source: {source or '<empty>'}")


def _origin_url(source: str, item: Mapping[str, Any], final_url: str) -> str:
    hn_id = _text(item.get("hn_id"))
    if source == "hacker_news" and hn_id.isdigit():
        return f"https://hacker-news.firebaseio.com/v0/item/{hn_id}.json"
    if source == "arxiv":
        return "https://export.arxiv.org/api/query"
    feed_url = _text(item.get("feed_url"))
    return feed_url or final_url


def _evidence_fields(source: str, item: Mapping[str, Any], source_text: str) -> dict[str, Any]:
    raw_tags = item.get("tags")
    source_tags = (
        [_text(value) for value in raw_tags if _text(value)]
        if isinstance(raw_tags, (list, tuple))
        else []
    )
    common: dict[str, Any] = {
        "title": _text(item.get("title")),
        "source_text": source_text,
        "tags": source_tags,
    }
    if source == "hacker_news":
        common.update(
            {
                "author": _text(item.get("author")),
                "score": item.get("score"),
                "descendants": item.get("descendants"),
                "hn_id": item.get("hn_id"),
            }
        )
    elif source == "arxiv":
        common.update(
            {
                "authors": list(item.get("authors") or []),
                "category": _text(item.get("category")),
                "arxiv_id": _text(item.get("arxiv_id")),
            }
        )
    elif source in {"blogs_podcasts", "juejin", "reddit"}:
        common.update(
            {
                "author": _text(item.get("author")),
                "published": _text(item.get("published_at") or item.get("published")),
            }
        )
    elif source == "github_trending":
        common.update(
            {
                "language": _text(item.get("language")),
                "stars": _text(item.get("stars")),
                "today_stars": _text(item.get("today_stars")),
            }
        )
    return common


def _evidence_digest(evidence: Mapping[str, Any]) -> str:
    payload = {
        "schema_version": evidence.get("schema_version"),
        "source": evidence.get("source"),
        "capture_mode": evidence.get("capture_mode"),
        "origin_url": evidence.get("origin_url"),
        "external_url": evidence.get("external_url"),
        "discovery_method": evidence.get("discovery_method"),
        "fetch_status": evidence.get("fetch_status"),
        "extractor_version": evidence.get("extractor_version"),
        "source_payload_sha256": evidence.get("source_payload_sha256"),
        "source_text_chars_original": evidence.get("source_text_chars_original"),
        "source_summary_original": evidence.get("source_summary_original"),
        "is_truncated": evidence.get("is_truncated"),
        "truncation_reason": evidence.get("truncation_reason"),
        "fields": evidence.get("fields"),
    }
    return "sha256:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def apply_source_contract(item: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy labeled with immutable evidence and truncation metadata."""

    result = {str(key): value for key, value in item.items()}
    if "evidence" in result:
        verify_source_contract(result)
        return result

    source = _text(result.get("source")).casefold()
    if source not in _ALLOWED_SOURCES:
        raise SourceContractError(f"unsupported source: {source or '<empty>'}")
    result["source"] = source
    title = _text(result.get("title"))
    if not title:
        raise SourceContractError("source title is missing")
    final_url = _canonical_url(result)
    if not final_url:
        raise SourceContractError("source external URL is missing or invalid")
    captured_at = _text(
        result.get("captured_at")
        or result.get("crawled_at")
        or result.get("published_at")
        or result.get("published")
    )
    if not captured_at:
        raise SourceContractError("source capture time is missing")
    if source == "hacker_news" and not _text(result.get("hn_id")).isdigit():
        raise SourceContractError("Hacker News evidence requires a numeric hn_id")

    capture_mode, content_mode, raw_source_text, discovery_method = _capture(result)
    if capture_mode in {"abstract", "excerpt", "social_post"} and not raw_source_text:
        raise SourceContractError(f"{capture_mode} source text is missing")
    source_payload_sha256 = "sha256:" + hashlib.sha256(
        raw_source_text.encode("utf-8")
    ).hexdigest()
    source_text_chars_original = len(raw_source_text)
    source_text, storage_truncated = _truncate_utf8(
        raw_source_text, _MAX_STORED_SOURCE_BYTES
    )
    source_display_excerpt, display_truncated = _truncate_utf8(
        source_text, _MAX_DISPLAY_EXCERPT_BYTES
    )
    raw_original_summary = _source_summary(source, result)
    original_summary, _ = _truncate_utf8(
        raw_original_summary, _MAX_STORED_SOURCE_BYTES
    )
    explicit_truncated = result.get("source_is_truncated") is True
    marker_truncated = "[...truncated...]" in source_text.casefold()
    rss_limit_truncated = source == "blogs_podcasts" and len(raw_source_text) >= 2_000
    truncation_reasons: list[str] = []
    if explicit_truncated:
        truncation_reasons.append(
            _text(result.get("source_truncation_reason")) or "crawler_reported"
        )
    if marker_truncated:
        truncation_reasons.append("explicit_truncation_marker")
    if rss_limit_truncated:
        truncation_reasons.append("rss_excerpt_limit")
    if storage_truncated:
        truncation_reasons.append("source_contract_limit")
    if display_truncated:
        truncation_reasons.append("publication_excerpt_limit")
    truncation_reason = ",".join(dict.fromkeys(truncation_reasons))
    is_truncated = bool(truncation_reasons)

    discovery_method = _text(result.get("discovery_method")) or discovery_method
    fetch_status = _text(result.get("fetch_status")) or "captured"
    fields = _evidence_fields(source, result, source_text)
    evidence: dict[str, Any] = {
        "schema_version": EVIDENCE_SCHEMA,
        "source": source,
        "capture_mode": capture_mode,
        "origin_url": _origin_url(source, result, final_url),
        "external_url": final_url,
        "captured_at": captured_at,
        "discovery_method": discovery_method,
        "fetch_status": fetch_status,
        "extractor_version": EXTRACTOR_VERSION,
        "source_payload_sha256": source_payload_sha256,
        "source_text_chars_original": source_text_chars_original,
        "source_summary_original": original_summary,
        "is_truncated": is_truncated,
        "truncation_reason": truncation_reason,
        "fields": fields,
    }
    evidence["digest"] = _evidence_digest(evidence)
    if len(canonical_json_bytes(evidence)) > _MAX_EVIDENCE_BYTES:
        raise SourceContractError("source evidence exceeds the size limit")

    snapshot_digest = str(evidence["digest"])

    result.update(
        {
            "content_mode": content_mode,
            "publication_tier": "C" if content_mode == "source_brief" else "B",
            "source_capture_mode": capture_mode,
            "discovery_method": discovery_method,
            "fetch_status": fetch_status,
            "final_url": final_url,
            "source_text_original": source_text,
            "source_display_excerpt": source_display_excerpt,
            "source_text_chars": len(source_text),
            "source_text_chars_original": source_text_chars_original,
            "source_payload_sha256": source_payload_sha256,
            "source_snapshot_sha256": snapshot_digest,
            "extractor_version": EXTRACTOR_VERSION,
            "source_is_truncated": is_truncated,
            "source_truncation_reason": truncation_reason,
            "captured_at": captured_at,
            "source_summary_original": original_summary,
            "evidence": evidence,
        }
    )
    if final_url:
        result["url"] = final_url
    return result


def verify_source_contract(item: Mapping[str, Any]) -> None:
    """Fail closed when the immutable crawler evidence is missing or changed."""

    evidence = item.get("evidence")
    if not isinstance(evidence, Mapping):
        raise SourceContractError("source evidence is missing")
    if evidence.get("schema_version") != EVIDENCE_SCHEMA:
        raise SourceContractError("source evidence schema is invalid")
    fields = evidence.get("fields")
    if not isinstance(fields, Mapping) or not fields:
        raise SourceContractError("source evidence fields are invalid")
    for name in ("origin_url", "external_url"):
        value = _text(evidence.get(name))
        parsed = urlsplit(value)
        if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
            raise SourceContractError(f"source evidence {name} is invalid")
    expected = _evidence_digest(evidence)
    actual = _text(evidence.get("digest"))
    if not hmac.compare_digest(expected, actual):
        raise SourceContractError("source evidence digest mismatch")
    if _text(item.get("source_snapshot_sha256")) != actual:
        raise SourceContractError("source snapshot digest mismatch")
    if _text(item.get("source")).casefold() != _text(evidence.get("source")).casefold():
        raise SourceContractError("source evidence identity mismatch")
    if _text(item.get("source_capture_mode")) != _text(evidence.get("capture_mode")):
        raise SourceContractError("source evidence mode mismatch")
    if _text(item.get("source")).casefold() not in _ALLOWED_SOURCES:
        raise SourceContractError("source evidence uses an unsupported source")
    if _text(item.get("final_url")) != _text(evidence.get("external_url")):
        raise SourceContractError("source evidence external URL mismatch")
    if _canonical_url(item) != _text(evidence.get("external_url")):
        raise SourceContractError("source external URL does not match evidence")
    if _text(item.get("title")) != _text(fields.get("title")):
        raise SourceContractError("source title does not match evidence")
    if _text(item.get("source_text_original")) != _text(fields.get("source_text")):
        raise SourceContractError("source text does not match evidence")
    if item.get("source_text_chars") != len(_text(fields.get("source_text"))):
        raise SourceContractError("source text length does not match evidence")
    if _text(item.get("captured_at")) != _text(evidence.get("captured_at")):
        raise SourceContractError("source capture time does not match evidence")
    if _text(item.get("discovery_method")) != _text(evidence.get("discovery_method")):
        raise SourceContractError("source discovery method mismatch")
    if _text(item.get("fetch_status")) != _text(evidence.get("fetch_status")):
        raise SourceContractError("source fetch status mismatch")
    if _text(item.get("extractor_version")) != _text(evidence.get("extractor_version")):
        raise SourceContractError("source extractor version mismatch")
    if _text(item.get("source_payload_sha256")) != _text(
        evidence.get("source_payload_sha256")
    ):
        raise SourceContractError("source payload digest mismatch")
    _mode, _content_mode, current_source_payload, _method = _capture(item)
    current_payload_digest = "sha256:" + hashlib.sha256(
        current_source_payload.encode("utf-8")
    ).hexdigest()
    if current_payload_digest != _text(evidence.get("source_payload_sha256")):
        raise SourceContractError("source payload no longer matches evidence")
    if len(current_source_payload) != evidence.get("source_text_chars_original"):
        raise SourceContractError("source payload length no longer matches evidence")
    if item.get("source_text_chars_original") != evidence.get(
        "source_text_chars_original"
    ):
        raise SourceContractError("source original text length mismatch")
    if _text(item.get("source_summary_original")) != _text(
        evidence.get("source_summary_original")
    ):
        raise SourceContractError("source summary does not match evidence")
    expected_display_excerpt, _ = _truncate_utf8(
        _text(fields.get("source_text")), _MAX_DISPLAY_EXCERPT_BYTES
    )
    if _text(item.get("source_display_excerpt")) != expected_display_excerpt:
        raise SourceContractError("source display excerpt does not match evidence")
    if item.get("source_is_truncated") is not evidence.get("is_truncated"):
        raise SourceContractError("source truncation flag mismatch")
    if _text(item.get("source_truncation_reason")) != _text(
        evidence.get("truncation_reason")
    ):
        raise SourceContractError("source truncation reason mismatch")
    if _text(item.get("content_mode")) != "source_brief":
        raise SourceContractError("unsupported publication content mode")
    if _text(item.get("publication_tier")) != "C":
        raise SourceContractError("source brief must use publication tier C")
    if (
        _text(item.get("discovery_method")).casefold() == "search_fallback"
        and _text(item.get("source_capture_mode")) != "metadata_only"
    ):
        raise SourceContractError("search fallback cannot claim source body evidence")
    if len(canonical_json_bytes(dict(evidence))) > _MAX_EVIDENCE_BYTES:
        raise SourceContractError("source evidence exceeds the size limit")


__all__ = [
    "EVIDENCE_SCHEMA",
    "EXTRACTOR_VERSION",
    "SourceContractError",
    "apply_source_contract",
    "verify_source_contract",
]
