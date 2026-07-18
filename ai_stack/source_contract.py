"""Deterministic source-evidence contracts for the production content path.

This module does not fetch arbitrary URLs.  It records exactly what each
crawler already captured, so downstream generators cannot mistake metadata or
an excerpt for a full article.
"""

from __future__ import annotations

import hashlib
import hmac
import re
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

from ._json import canonical_json_bytes
from .identity import canonicalize_url

EXTRACTOR_VERSION = "source-contract-v1"
FULL_ARTICLE_EXTRACTOR_VERSION = "source-contract-v2"
EVIDENCE_SCHEMA = "source_evidence_v1"
_MAX_EVIDENCE_BYTES = 64 * 1024
_MAX_STORED_SOURCE_BYTES = 24 * 1024
_LEGACY_MAX_DISPLAY_EXCERPT_BYTES = 6_000
_MAX_PUBLICATION_TITLE_CHARS = 300
_SHA256_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
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

    prefix = raw[:limit].decode("utf-8", errors="ignore").rstrip()
    consumed = len(prefix.encode("utf-8"))
    remainder = raw[consumed:].decode("utf-8", errors="ignore")
    if prefix and remainder:
        left = prefix[-1]
        right = remainder[0]
        continues_token = (
            not left.isspace()
            and not right.isspace()
            and (left.isalnum() or left in "_-")
            and (right.isalnum() or right in "_-")
        )
        if continues_token:
            boundary = re.search(r"\s+\S*$", prefix)
            if boundary is not None and boundary.start() >= int(len(prefix) * 0.8):
                prefix = prefix[: boundary.start()].rstrip()
    return prefix, True


def _truncate_title(value: str, limit: int) -> tuple[str, bool]:
    title = str(value or "")
    if len(title) <= limit:
        return title, False

    prefix = title[:limit].rstrip()
    remainder = title[len(prefix) :]
    if prefix and remainder and not prefix[-1].isspace() and not remainder[0].isspace():
        boundary = re.search(r"\s+\S*$", prefix)
        if boundary is not None:
            prefix = prefix[: boundary.start()].rstrip()
    return prefix, True


def _publication_title(value: object) -> tuple[str, bool]:
    normalized = " ".join(str(value or "").split()).strip()
    return _truncate_title(normalized, _MAX_PUBLICATION_TITLE_CHARS)


def _source_summary(source: str, item: Mapping[str, Any]) -> str:
    if source == "hacker_news":
        return ""
    if source == "arxiv":
        return _text(item.get("summary"))
    if source == "juejin" and _text(item.get("full_article_text")):
        return _text(item.get("full_article_text"))
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
    if source == "juejin" and _text(item.get("full_article_text")):
        return "full_article", "evidence_backed_rewrite", original_summary, "article_html"
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
        return (
            "metadata_only",
            "source_brief",
            evidence or _text(item.get("title")),
            "repository_metadata",
        )
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
    if source == "juejin" and _text(item.get("full_article_text")):
        return final_url
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
    capture_field_names = (
        "source_capture_sha256",
        "source_capture_chars_original",
        "source_publication_excerpt_chars",
    )
    if any(name in item for name in capture_field_names):
        capture_sha256 = _text(item.get("source_capture_sha256"))
        capture_chars = item.get("source_capture_chars_original")
        excerpt_chars = item.get("source_publication_excerpt_chars")
        if (
            _SHA256_DIGEST_RE.fullmatch(capture_sha256) is None
            or type(capture_chars) is not int
            or type(excerpt_chars) is not int
            or capture_chars < 1
            or excerpt_chars < 1
            or excerpt_chars > capture_chars
            or (
                source in {"blogs_podcasts", "juejin"}
                and excerpt_chars > 800
            )
            or excerpt_chars != len(source_text)
            or (
                excerpt_chars == capture_chars
                and capture_sha256
                != "sha256:"
                + hashlib.sha256(source_text.encode("utf-8")).hexdigest()
            )
        ):
            raise SourceContractError("source capture publication metadata is invalid")
        common.update(
            {
                "source_capture_sha256": capture_sha256,
                "source_capture_chars_original": capture_chars,
                "source_publication_excerpt_chars": excerpt_chars,
            }
        )
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
        if "published" in item or "published_at" in item:
            common["published"] = _text(
                item.get("published_at") or item.get("published")
            )
        if "pdf_url" in item:
            common["pdf_url"] = _text(item.get("pdf_url"))
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
        if "forks" in item:
            common["forks"] = _text(item.get("forks"))
        if "license" in item:
            common["license"] = _text(item.get("license"))
        if "topics" in item:
            raw_topics = item.get("topics")
            common["topics"] = (
                [_text(topic) for topic in raw_topics if _text(topic)]
                if isinstance(raw_topics, (list, tuple))
                else []
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
    # v1 digests are already persisted in historical crawler records.  New v2
    # provenance fields are hash-bound only by v2 so those immutable v1 snapshots
    # remain verifiable during rolling deploys and archive repair.
    if _text(evidence.get("extractor_version")) == FULL_ARTICLE_EXTRACTOR_VERSION:
        payload.update(
            {
                "captured_at": evidence.get("captured_at"),
                "source_completeness": evidence.get("source_completeness"),
                "parent_snapshot_sha256": evidence.get("parent_snapshot_sha256"),
            }
        )
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
    source_display_title, title_truncated = _publication_title(title)
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
    if (
        capture_mode in {"abstract", "excerpt", "social_post", "full_article"}
        and not raw_source_text
    ):
        raise SourceContractError(f"{capture_mode} source text is missing")
    source_payload_sha256 = "sha256:" + hashlib.sha256(raw_source_text.encode("utf-8")).hexdigest()
    source_text_chars_original = len(raw_source_text)
    source_text, storage_truncated = _truncate_utf8(raw_source_text, _MAX_STORED_SOURCE_BYTES)
    if capture_mode == "full_article" and storage_truncated:
        raise SourceContractError("full article exceeds the verified evidence limit")
    # Publication must not silently discard evidence that was already captured and
    # retained by the contract.  Older v1 records used a second 6 KB display cap;
    # verification below keeps those immutable records readable, while every new
    # record publishes the complete stored source text.
    source_display_excerpt = source_text
    raw_original_summary = _source_summary(source, result)
    original_summary, _ = _truncate_utf8(raw_original_summary, _MAX_STORED_SOURCE_BYTES)
    explicit_truncated = result.get("source_is_truncated") is True
    marker_truncated = "[...truncated...]" in source_text.casefold()
    legacy_rss_limit_truncated = (
        source == "blogs_podcasts"
        and len(raw_source_text) == 2_000
        and "source_is_truncated" not in result
    )
    truncation_reasons: list[str] = []
    if explicit_truncated:
        truncation_reasons.append(
            _text(result.get("source_truncation_reason")) or "crawler_reported"
        )
    if marker_truncated:
        truncation_reasons.append("explicit_truncation_marker")
    if legacy_rss_limit_truncated:
        truncation_reasons.append("rss_excerpt_limit")
    if title_truncated:
        truncation_reasons.append("publication_title_limit")
    if storage_truncated:
        truncation_reasons.append("source_contract_limit")
    truncation_reason = ",".join(dict.fromkeys(truncation_reasons))
    is_truncated = bool(truncation_reasons)
    if capture_mode == "full_article" and is_truncated:
        raise SourceContractError("full article capture cannot be marked truncated")

    source_completeness = _text(result.get("source_completeness")).casefold()
    if not source_completeness:
        source_completeness = {
            "full_article": "complete",
            "excerpt": "partial",
            "abstract": "abstract_only",
            "metadata_only": "metadata_only",
            "social_post": "single_item",
        }.get(capture_mode, "unknown")
    allowed_completeness = {
        "complete",
        "partial",
        "abstract_only",
        "metadata_only",
        "single_item",
        "unknown",
    }
    if source_completeness not in allowed_completeness:
        raise SourceContractError("source completeness is invalid")
    if capture_mode == "full_article" and source_completeness != "complete":
        raise SourceContractError("full article capture requires complete source evidence")

    parent_snapshot_sha256 = _text(result.get("parent_snapshot_sha256"))
    extractor_version = (
        FULL_ARTICLE_EXTRACTOR_VERSION
        if capture_mode == "full_article"
        else EXTRACTOR_VERSION
    )
    if capture_mode == "full_article" and not re.fullmatch(
        r"sha256:[0-9a-f]{64}", parent_snapshot_sha256
    ):
        raise SourceContractError("full article capture requires a parent source snapshot")

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
        "extractor_version": extractor_version,
        "source_payload_sha256": source_payload_sha256,
        "source_text_chars_original": source_text_chars_original,
        "source_summary_original": original_summary,
        "source_completeness": source_completeness,
        "parent_snapshot_sha256": parent_snapshot_sha256,
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
            "source_display_title": source_display_title,
            "source_title_chars_original": len(title),
            "source_text_chars": len(source_text),
            "source_text_chars_original": source_text_chars_original,
            "source_payload_sha256": source_payload_sha256,
            "source_snapshot_sha256": snapshot_digest,
            "extractor_version": extractor_version,
            "source_completeness": source_completeness,
            "parent_snapshot_sha256": parent_snapshot_sha256,
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
    expected_display_title, _ = _publication_title(fields.get("title"))
    if (
        "source_display_title" in item
        and _text(item.get("source_display_title")) != expected_display_title
    ):
        raise SourceContractError("source display title does not match evidence")
    if "source_title_chars_original" in item and item.get("source_title_chars_original") != len(
        _text(fields.get("title"))
    ):
        raise SourceContractError("source title length does not match evidence")
    if _text(item.get("source_text_original")) != _text(fields.get("source_text")):
        raise SourceContractError("source text does not match evidence")
    if item.get("source_text_chars") != len(_text(fields.get("source_text"))):
        raise SourceContractError("source text length does not match evidence")
    for name, label in (
        ("source_capture_sha256", "capture payload digest"),
        ("source_capture_chars_original", "capture payload length"),
        ("source_publication_excerpt_chars", "publication excerpt length"),
    ):
        if name in fields and item.get(name) != fields.get(name):
            raise SourceContractError(f"source {label} does not match evidence")
    if _text(item.get("captured_at")) != _text(evidence.get("captured_at")):
        raise SourceContractError("source capture time does not match evidence")
    if _text(item.get("discovery_method")) != _text(evidence.get("discovery_method")):
        raise SourceContractError("source discovery method mismatch")
    if _text(item.get("fetch_status")) != _text(evidence.get("fetch_status")):
        raise SourceContractError("source fetch status mismatch")
    if _text(item.get("extractor_version")) != _text(evidence.get("extractor_version")):
        raise SourceContractError("source extractor version mismatch")
    if _text(item.get("source_payload_sha256")) != _text(evidence.get("source_payload_sha256")):
        raise SourceContractError("source payload digest mismatch")
    _mode, _content_mode, current_source_payload, _method = _capture(item)
    current_payload_digest = (
        "sha256:" + hashlib.sha256(current_source_payload.encode("utf-8")).hexdigest()
    )
    if current_payload_digest != _text(evidence.get("source_payload_sha256")):
        raise SourceContractError("source payload no longer matches evidence")
    if len(current_source_payload) != evidence.get("source_text_chars_original"):
        raise SourceContractError("source payload length no longer matches evidence")
    if item.get("source_text_chars_original") != evidence.get("source_text_chars_original"):
        raise SourceContractError("source original text length mismatch")
    if _text(item.get("source_summary_original")) != _text(evidence.get("source_summary_original")):
        raise SourceContractError("source summary does not match evidence")
    if _text(item.get("source_completeness")) != _text(evidence.get("source_completeness")):
        raise SourceContractError("source completeness does not match evidence")
    if _text(item.get("parent_snapshot_sha256")) != _text(
        evidence.get("parent_snapshot_sha256")
    ):
        raise SourceContractError("parent source snapshot does not match evidence")
    evidence_truncation_reason = _text(evidence.get("truncation_reason"))
    if "publication_excerpt_limit" in evidence_truncation_reason.split(","):
        expected_display_excerpt, _ = _truncate_utf8(
            _text(fields.get("source_text")), _LEGACY_MAX_DISPLAY_EXCERPT_BYTES
        )
    else:
        expected_display_excerpt = _text(fields.get("source_text"))
    if _text(item.get("source_display_excerpt")) != expected_display_excerpt:
        raise SourceContractError("source display excerpt does not match evidence")
    if item.get("source_is_truncated") is not evidence.get("is_truncated"):
        raise SourceContractError("source truncation flag mismatch")
    if _text(item.get("source_truncation_reason")) != _text(evidence.get("truncation_reason")):
        raise SourceContractError("source truncation reason mismatch")
    content_mode = _text(item.get("content_mode"))
    capture_mode = _text(item.get("source_capture_mode"))
    publication_tier = _text(item.get("publication_tier"))
    extractor_version = _text(item.get("extractor_version"))
    if content_mode == "source_brief":
        if publication_tier != "C":
            raise SourceContractError("source brief must use publication tier C")
        if capture_mode == "full_article":
            raise SourceContractError("full article cannot be published as a source brief")
        if extractor_version != EXTRACTOR_VERSION:
            raise SourceContractError("source brief extractor version is invalid")
        expected_completeness = {
            "abstract": "abstract_only",
            "excerpt": "partial",
            "metadata_only": "metadata_only",
            "social_post": "single_item",
        }.get(capture_mode, "unknown")
        declared_completeness = _text(item.get("source_completeness"))
        if declared_completeness and declared_completeness != expected_completeness:
            raise SourceContractError("source brief completeness is invalid")
        if _text(item.get("parent_snapshot_sha256")):
            raise SourceContractError("source brief cannot declare a parent snapshot")
    elif content_mode == "evidence_backed_rewrite":
        if publication_tier != "B":
            raise SourceContractError("evidence-backed rewrite must use publication tier B")
        if capture_mode != "full_article":
            raise SourceContractError("evidence-backed rewrite requires full article evidence")
        if extractor_version != FULL_ARTICLE_EXTRACTOR_VERSION:
            raise SourceContractError("evidence-backed rewrite extractor version is invalid")
        if item.get("source_is_truncated") is not False:
            raise SourceContractError("evidence-backed rewrite cannot use truncated evidence")
        if _text(item.get("source_completeness")) != "complete":
            raise SourceContractError("evidence-backed rewrite requires complete evidence")
        if not re.fullmatch(
            r"sha256:[0-9a-f]{64}", _text(item.get("parent_snapshot_sha256"))
        ):
            raise SourceContractError("evidence-backed rewrite parent snapshot is invalid")
    else:
        raise SourceContractError("unsupported publication content mode")
    if (
        _text(item.get("discovery_method")).casefold() == "search_fallback"
        and _text(item.get("source_capture_mode")) != "metadata_only"
    ):
        raise SourceContractError("search fallback cannot claim source body evidence")
    if len(canonical_json_bytes(dict(evidence))) > _MAX_EVIDENCE_BYTES:
        raise SourceContractError("source evidence exceeds the size limit")


def promote_juejin_full_article(
    item: Mapping[str, Any],
    full_article_text: str,
) -> dict[str, Any]:
    """Promote a verified Juejin RSS snapshot with a complete SSR body.

    The original Tier-C digest remains linked as ``parent_snapshot_sha256`` so
    an article body cannot appear without a traceable discovery record.
    """

    verify_source_contract(item)
    evidence = item.get("evidence")
    fields = evidence.get("fields") if isinstance(evidence, Mapping) else None
    if not isinstance(fields, Mapping):
        raise SourceContractError("source evidence fields are invalid")
    if _text(item.get("source")).casefold() != "juejin":
        raise SourceContractError("only Juejin evidence can be promoted by this function")
    if _text(item.get("content_mode")) != "source_brief":
        raise SourceContractError("Juejin promotion requires a Tier-C source brief")
    if _text(item.get("source_capture_mode")) != "excerpt":
        raise SourceContractError("Juejin promotion requires an RSS excerpt parent")
    body = str(full_article_text or "").strip()
    if len(re.sub(r"\s+", "", body)) < 600:
        raise SourceContractError("full article evidence is too short")

    raw: dict[str, Any] = {
        "source": "juejin",
        "title": _text(fields.get("title")),
        "url": _text(evidence.get("external_url")),
        "author": _text(fields.get("author")),
        "published": _text(fields.get("published")),
        "tags": list(fields.get("tags") or []),
        "crawled_at": _text(evidence.get("captured_at")),
        "captured_at": _text(evidence.get("captured_at")),
        "full_article_text": body,
        "discovery_method": "article_html",
        "fetch_status": "captured",
        "source_completeness": "complete",
        "source_is_truncated": False,
        "source_truncation_reason": "",
        "parent_snapshot_sha256": _text(item.get("source_snapshot_sha256")),
    }
    promoted = apply_source_contract(raw)
    verify_source_contract(promoted)
    return promoted


def publication_title_from_contract(item: Mapping[str, Any]) -> str:
    """Derive the bounded display title from hash-bound immutable evidence."""

    verify_source_contract(item)
    evidence = item.get("evidence")
    fields = evidence.get("fields") if isinstance(evidence, Mapping) else None
    if not isinstance(fields, Mapping):
        raise SourceContractError("source evidence fields are invalid")
    title, _ = _publication_title(fields.get("title"))
    if not title:
        raise SourceContractError("source title is missing")
    return title


__all__ = [
    "EVIDENCE_SCHEMA",
    "EXTRACTOR_VERSION",
    "FULL_ARTICLE_EXTRACTOR_VERSION",
    "SourceContractError",
    "apply_source_contract",
    "publication_title_from_contract",
    "promote_juejin_full_article",
    "verify_source_contract",
]
