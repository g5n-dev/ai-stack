"""Deterministic, progressively loaded trend assets for the Hugo site.

The module adapts quality-gated Posts to the existing ``trend_v1`` event model,
then projects only presentation-safe fields into small static JSON shards.  It
has no network, model or wall-clock dependency.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import tempfile
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml

from ai_stack.content_quality import analyze_post, markdown_frontmatter
from ai_stack.identity import canonicalize_url
from ai_stack.tag_taxonomy import normalize_tags
from processor.intelligence import TREND_FORMULA, WINDOWS, calculate_trends

INDEX_SCHEMA_VERSION_V1 = "stack_trends_index_v1"
WINDOW_SCHEMA_VERSION_V1 = "stack_trends_window_v1"
TOPIC_SCHEMA_VERSION_V1 = "stack_trends_topic_v1"
INDEX_SCHEMA_VERSION_V2 = "stack_trends_index_v2"
WINDOW_SCHEMA_VERSION_V2 = "stack_trends_window_v2"
TOPIC_SCHEMA_VERSION_V2 = "stack_trends_topic_v2"

# New builds emit v2; readers and verifiers retain a bounded v1 rollout fallback.
INDEX_SCHEMA_VERSION = INDEX_SCHEMA_VERSION_V2
WINDOW_SCHEMA_VERSION = WINDOW_SCHEMA_VERSION_V2
TOPIC_SCHEMA_VERSION = TOPIC_SCHEMA_VERSION_V2
CONFIG_VERSION = 1
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "stack_trends.yaml"
DEFAULT_LINEAGE_ROOT = (
    Path(__file__).resolve().parents[1] / "blog" / "static" / "data" / "lineage"
)

DEFAULT_WINDOW = "30d"
MINIMUM_UNIQUE_EVENTS = 3
WINDOW_TREND_LIMIT = 24
TOPIC_EVIDENCE_LIMIT = 30
RELATED_TOPIC_LIMIT = 12
SPARKLINE_BUCKETS = 12

SAME_EVENT_MIN_SUCCESSFUL_REFRESHES = 24
SAME_EVENT_MIN_DETERMINISTIC_FULL_BUILDS = 3
SAME_EVENT_MIN_STABLE_DURATION = timedelta(days=7)
SAME_EVENT_MAX_FALSE_MERGE_RATE = 0.005

INDEX_MAX_BYTES = 64 * 1024
WINDOW_MAX_BYTES = 128 * 1024
TOPIC_MAX_BYTES = 96 * 1024
TOTAL_MAX_BYTES = 2 * 1024 * 1024
TOTAL_MAX_FILES = 100

_QUALITY_SCHEMA = "content_quality_manifest_v4"
_ACTIVE_QUALITY_STATUSES = {
    "complete",
    "interpreted_brief",
    "legacy_analysis",
    "source_brief",
}
_DENIED_PUBLIC_KEYS = {"body", "content", "external_url", "frontmatter", "local_path"}
_ASSET_PATH_RE = re.compile(r"^(?:windows|topics)/[a-z0-9][a-z0-9._/-]{0,220}\.json$")
_LINEAGE_PATH_RE = re.compile(
    r"^(?:routes|clusters)/[0-7][0-9a-f]-[0-9a-f]{16}\.json$"
)
_LINEAGE_ID_RE = re.compile(r"^(?:obs|evt)_[0-9a-f]{64}$")
_LINEAGE_RELATIONS = {
    "original",
    "exact_copy",
    "syndicated",
    "derivative",
    "same_event",
    "related_only",
}
_LINEAGE_MERGED_RELATIONS = {"original", "exact_copy", "syndicated"}
_SAME_EVENT_PROMOTION_FIELDS = frozenset(
    {
        "event_id",
        "observation_id",
        "parent_observation_id",
        "successful_refreshes",
        "deterministic_full_builds",
        "stable_since",
        "reviewed_at",
        "false_merge_rate",
    }
)
_SENSITIVE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?:^|[\s\"'])/(?:Users|home)/[^\s\"']+"),
    re.compile(r"\b[A-Za-z]:\\Users\\[^\s\"']+", re.IGNORECASE),
)


class StackTrendsValidationError(ValueError):
    """Raised when trend input or generated public assets fail closed."""


@dataclass(frozen=True, slots=True)
class SameEventPromotion:
    """Reviewed proof required before one ``same_event`` pair affects trends."""

    event_id: str
    observation_id: str
    parent_observation_id: str
    successful_refreshes: int
    deterministic_full_builds: int
    stable_since: datetime
    reviewed_at: datetime
    false_merge_rate: float


@dataclass(frozen=True, slots=True)
class StackTrendsConfig:
    """Reviewed configuration for the deterministic Post adapter."""

    version: int
    excluded_tags: frozenset[str]
    source_weight: float
    same_event_promotions: tuple[SameEventPromotion, ...]


def _stable_json_bytes(value: Any) -> bytes:
    try:
        serialized = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise StackTrendsValidationError(f"non-deterministic JSON value: {exc}") from exc
    return f"{serialized}\n".encode()


def _parse_timestamp(value: Any, *, field: str) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = f"{normalized[:-1]}+00:00"
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise StackTrendsValidationError(f"{field} must be an ISO-8601 timestamp") from exc
    else:
        raise StackTrendsValidationError(f"{field} must be an ISO-8601 timestamp")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise StackTrendsValidationError(f"{field} must include a timezone")
    return parsed.astimezone(UTC)


def _isoformat(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_stack_trends_config(path: str | Path = DEFAULT_CONFIG_PATH) -> StackTrendsConfig:
    """Load the versioned, exact trend-label exclusion registry."""

    config_path = Path(path)
    try:
        payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise StackTrendsValidationError(f"failed to load trend config: {exc}") from exc
    if not isinstance(payload, Mapping) or payload.get("version") != CONFIG_VERSION:
        raise StackTrendsValidationError(
            f"trend config version must be {CONFIG_VERSION}"
        )
    unknown_top_level = set(payload) - {
        "version",
        "excluded_tags",
        "source_weight",
        "same_event_promotions",
    }
    if unknown_top_level:
        raise StackTrendsValidationError(
            "trend config has unknown fields: " + ", ".join(sorted(unknown_top_level))
        )
    raw_excluded = payload.get("excluded_tags")
    if not isinstance(raw_excluded, list) or any(
        not isinstance(item, str) or not item.strip() for item in raw_excluded
    ):
        raise StackTrendsValidationError("excluded_tags must be non-empty strings")
    excluded = [item.strip() for item in raw_excluded]
    if len(excluded) != len(set(excluded)):
        raise StackTrendsValidationError("excluded_tags must not contain duplicates")
    source_weight = payload.get("source_weight", 0.5)
    if (
        isinstance(source_weight, bool)
        or not isinstance(source_weight, (int, float))
        or not math.isfinite(source_weight)
        or not 0 <= source_weight <= 1
    ):
        raise StackTrendsValidationError("source_weight must be between 0 and 1")

    raw_promotions = payload.get("same_event_promotions", [])
    if not isinstance(raw_promotions, list):
        raise StackTrendsValidationError("same_event_promotions must be an array")
    promotions: list[SameEventPromotion] = []
    promotion_keys: set[tuple[str, str, str]] = set()
    for index, raw in enumerate(raw_promotions):
        location = f"same_event_promotions[{index}]"
        if not isinstance(raw, Mapping):
            raise StackTrendsValidationError(f"{location} must be an object")
        unknown = set(raw) - _SAME_EVENT_PROMOTION_FIELDS
        missing = _SAME_EVENT_PROMOTION_FIELDS - set(raw)
        if unknown:
            raise StackTrendsValidationError(
                f"{location} has unknown fields: " + ", ".join(sorted(unknown))
            )
        if missing:
            raise StackTrendsValidationError(
                f"{location} is missing fields: " + ", ".join(sorted(missing))
            )
        event_id = _lineage_identifier(raw.get("event_id"), field=f"{location}.event_id")
        if not event_id.startswith("evt_"):
            raise StackTrendsValidationError(f"{location}.event_id must start with evt_")
        observation_id = _lineage_identifier(
            raw.get("observation_id"), field=f"{location}.observation_id"
        )
        if not observation_id.startswith("obs_"):
            raise StackTrendsValidationError(
                f"{location}.observation_id must start with obs_"
            )
        parent_observation_id = _lineage_identifier(
            raw.get("parent_observation_id"),
            field=f"{location}.parent_observation_id",
        )
        if not parent_observation_id.startswith("obs_"):
            raise StackTrendsValidationError(
                f"{location}.parent_observation_id must start with obs_"
            )
        if observation_id == parent_observation_id:
            raise StackTrendsValidationError(
                f"{location} cannot promote a self-referential same_event pair"
            )

        successful_refreshes = raw.get("successful_refreshes")
        if (
            isinstance(successful_refreshes, bool)
            or not isinstance(successful_refreshes, int)
            or successful_refreshes < SAME_EVENT_MIN_SUCCESSFUL_REFRESHES
        ):
            raise StackTrendsValidationError(
                f"{location}.successful_refreshes must be at least "
                f"{SAME_EVENT_MIN_SUCCESSFUL_REFRESHES}"
            )
        deterministic_full_builds = raw.get("deterministic_full_builds")
        if (
            isinstance(deterministic_full_builds, bool)
            or not isinstance(deterministic_full_builds, int)
            or deterministic_full_builds < SAME_EVENT_MIN_DETERMINISTIC_FULL_BUILDS
        ):
            raise StackTrendsValidationError(
                f"{location}.deterministic_full_builds must be at least "
                f"{SAME_EVENT_MIN_DETERMINISTIC_FULL_BUILDS}"
            )
        false_merge_rate = raw.get("false_merge_rate")
        if (
            isinstance(false_merge_rate, bool)
            or not isinstance(false_merge_rate, (int, float))
            or not math.isfinite(false_merge_rate)
            or false_merge_rate < 0
            or false_merge_rate >= SAME_EVENT_MAX_FALSE_MERGE_RATE
        ):
            raise StackTrendsValidationError(
                f"{location}.false_merge_rate must be below "
                f"{SAME_EVENT_MAX_FALSE_MERGE_RATE:.3f}"
            )
        stable_since = _parse_timestamp(
            raw.get("stable_since"), field=f"{location}.stable_since"
        )
        reviewed_at = _parse_timestamp(
            raw.get("reviewed_at"), field=f"{location}.reviewed_at"
        )
        if reviewed_at - stable_since < SAME_EVENT_MIN_STABLE_DURATION:
            raise StackTrendsValidationError(
                f"{location} must remain stable for seven full days before review"
            )
        key = (event_id, observation_id, parent_observation_id)
        if key in promotion_keys:
            raise StackTrendsValidationError("duplicate same_event promotion pair")
        promotion_keys.add(key)
        promotions.append(
            SameEventPromotion(
                event_id=event_id,
                observation_id=observation_id,
                parent_observation_id=parent_observation_id,
                successful_refreshes=successful_refreshes,
                deterministic_full_builds=deterministic_full_builds,
                stable_since=stable_since,
                reviewed_at=reviewed_at,
                false_merge_rate=float(false_merge_rate),
            )
        )
    return StackTrendsConfig(
        version=CONFIG_VERSION,
        excluded_tags=frozenset(excluded),
        source_weight=float(source_weight),
        same_event_promotions=tuple(
            sorted(
                promotions,
                key=lambda item: (
                    item.event_id,
                    item.observation_id,
                    item.parent_observation_id,
                ),
            )
        ),
    )


def _lineage_identifier(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not _LINEAGE_ID_RE.fullmatch(value):
        raise StackTrendsValidationError(f"{field} must be a namespaced SHA-256 id")
    return value


def _lineage_reference(root: Path, value: Any, *, prefix: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise StackTrendsValidationError(f"lineage {prefix} reference must be an object")
    bucket = value.get("bucket")
    path = value.get("path")
    digest = value.get("sha256")
    expected_bytes = value.get("bytes")
    if not isinstance(bucket, str) or not re.fullmatch(r"[0-7][0-9a-f]", bucket):
        raise StackTrendsValidationError("lineage bucket must be a two-digit lowercase hex key")
    if (
        not isinstance(path, str)
        or not path.startswith(f"{prefix}/")
        or not path.startswith(f"{prefix}/{bucket}-")
        or not _LINEAGE_PATH_RE.fullmatch(path)
        or ".." in PurePosixPath(path).parts
        or "//" in path
    ):
        raise StackTrendsValidationError("unsafe lineage shard path")
    if not isinstance(digest, str) or not re.fullmatch(r"(?:sha256:)?[0-9a-f]{64}", digest):
        raise StackTrendsValidationError("invalid lineage shard digest")
    if (
        isinstance(expected_bytes, bool)
        or not isinstance(expected_bytes, int)
        or expected_bytes <= 0
    ):
        raise StackTrendsValidationError("invalid lineage shard byte size")
    shard_path = root / path
    try:
        body = shard_path.read_bytes()
    except OSError as exc:
        raise StackTrendsValidationError(f"missing lineage shard: {path}") from exc
    expected_digest = digest.removeprefix("sha256:")
    if len(body) != expected_bytes or hashlib.sha256(body).hexdigest() != expected_digest:
        raise StackTrendsValidationError(f"lineage shard integrity mismatch: {path}")
    try:
        payload = json.loads(body)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise StackTrendsValidationError(f"invalid lineage shard JSON: {path}") from exc
    if (
        not isinstance(payload, dict)
        or payload.get("version") != 1
        or payload.get("bucket") != bucket
    ):
        raise StackTrendsValidationError(f"lineage shard identity mismatch: {path}")
    _scan_public_value(payload)
    return payload


def _load_lineage_observations(
    root: str | Path | None,
) -> tuple[dict[str, dict[str, Any]], str]:
    """Load verified public lineage metadata without retaining source text.

    Missing lineage assets are an intentional rolling-deploy fallback.  Once an
    index exists, every referenced shard fails closed on identity and hash.
    """

    if root is None:
        return {}, "url_fallback"
    lineage_root = Path(root)
    index_path = lineage_root / "index.json"
    if not index_path.is_file():
        return {}, "url_fallback"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StackTrendsValidationError("invalid lineage index") from exc
    if (
        not isinstance(index, dict)
        or index.get("version") != 1
        or index.get("schema") != "lineage_index_v1"
        or index.get("bucket_count") != 128
        or index.get("bucket_algorithm") != "sha256_prefix32_mod_v1"
    ):
        raise StackTrendsValidationError("unsupported lineage index")
    _scan_public_value(index)
    route_refs = index.get("route_buckets")
    cluster_refs = index.get("cluster_buckets")
    if not isinstance(route_refs, list) or not isinstance(cluster_refs, list):
        raise StackTrendsValidationError("lineage index buckets must be arrays")

    routes: dict[str, dict[str, Any]] = {}
    for reference in sorted(route_refs, key=lambda item: str(item.get("bucket", ""))):
        payload = _lineage_reference(lineage_root, reference, prefix="routes")
        entries = payload.get("routes")
        if not isinstance(entries, list):
            raise StackTrendsValidationError("lineage routes must be an array")
        for entry in entries:
            if not isinstance(entry, Mapping):
                raise StackTrendsValidationError("lineage route must be an object")
            observation_id = _lineage_identifier(
                entry.get("observation_id"), field="observation_id"
            )
            event_id = _lineage_identifier(entry.get("event_id"), field="event_id")
            if observation_id in routes:
                raise StackTrendsValidationError("duplicate lineage observation route")
            routes[observation_id] = {"event_id": event_id}

    observations: dict[str, dict[str, Any]] = {}
    for reference in sorted(cluster_refs, key=lambda item: str(item.get("bucket", ""))):
        payload = _lineage_reference(lineage_root, reference, prefix="clusters")
        clusters = payload.get("clusters")
        if not isinstance(clusters, list):
            raise StackTrendsValidationError("lineage clusters must be an array")
        for cluster in clusters:
            if not isinstance(cluster, Mapping):
                raise StackTrendsValidationError("lineage cluster must be an object")
            event_id = _lineage_identifier(cluster.get("event_id"), field="event_id")
            members = cluster.get("observations")
            if not isinstance(members, list) or not members:
                raise StackTrendsValidationError("lineage cluster observations must be non-empty")
            for raw in members:
                if not isinstance(raw, Mapping):
                    raise StackTrendsValidationError("lineage observation must be an object")
                observation_id = _lineage_identifier(
                    raw.get("observation_id"), field="observation_id"
                )
                relation = raw.get("relation")
                if relation not in _LINEAGE_RELATIONS:
                    raise StackTrendsValidationError("unsupported lineage relation")
                route = routes.get(observation_id)
                if route is None or route["event_id"] != event_id:
                    raise StackTrendsValidationError("lineage route and cluster disagree")
                article_url = raw.get("article_url")
                if article_url is not None and (
                    not isinstance(article_url, str) or not article_url.startswith("/")
                ):
                    raise StackTrendsValidationError("lineage article_url must be internal or null")
                if observation_id in observations:
                    raise StackTrendsValidationError("duplicate lineage observation")
                title = raw.get("title")
                source = raw.get("source")
                if not isinstance(title, str) or not title.strip():
                    raise StackTrendsValidationError("lineage observation title must be non-empty")
                if not isinstance(source, str) or not source.strip():
                    raise StackTrendsValidationError("lineage observation source must be non-empty")
                parent_observation_id = raw.get("parent_observation_id")
                if parent_observation_id is not None:
                    parent_observation_id = _lineage_identifier(
                        parent_observation_id,
                        field="parent_observation_id",
                    )
                    if not parent_observation_id.startswith("obs_"):
                        raise StackTrendsValidationError(
                            "lineage parent_observation_id must start with obs_"
                        )
                    if parent_observation_id == observation_id:
                        raise StackTrendsValidationError(
                            "lineage observation cannot be its own parent"
                        )
                observations[observation_id] = {
                    "event_id": event_id,
                    "relation": relation,
                    "parent_observation_id": parent_observation_id,
                    "article_url": article_url,
                    "source_published_at": raw.get("source_published_at"),
                    "first_seen_at": raw.get("first_seen_at"),
                    "timestamp_confidence": raw.get("timestamp_confidence") or "unknown",
                    "title": title.strip(),
                    "source": source.strip(),
                }
    if set(routes) != set(observations):
        raise StackTrendsValidationError("lineage routes and observations are incomplete")
    for observation_id, record in observations.items():
        parent_observation_id = record.get("parent_observation_id")
        if parent_observation_id is None:
            continue
        parent = observations.get(str(parent_observation_id))
        if parent is None:
            raise StackTrendsValidationError(
                f"lineage parent is missing: {observation_id}"
            )
    return observations, "lineage_index_v1"


def _source_tree_digest(content_root: Path) -> tuple[str, int, set[str]]:
    digest = hashlib.sha256()
    count = 0
    relative_paths: set[str] = set()
    for path in sorted(content_root.rglob("*.md"), key=lambda item: item.as_posix()):
        if not path.is_file():
            continue
        relative = path.relative_to(content_root)
        if not relative.parts or relative.parts[0] != "posts":
            continue
        payload = path.read_bytes()
        count += 1
        relative_text = relative.as_posix()
        relative_paths.add(relative_text)
        digest.update(relative_text.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(payload).digest())
    return digest.hexdigest(), count, relative_paths


def _load_quality_manifest(path: Path, *, content_root: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StackTrendsValidationError(f"failed to load quality manifest: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != _QUALITY_SCHEMA:
        raise StackTrendsValidationError("unsupported content quality manifest")
    pages = payload.get("pages")
    if not isinstance(pages, dict):
        raise StackTrendsValidationError("quality manifest pages must be an object")
    actual_digest, actual_count, actual_paths = _source_tree_digest(content_root)
    if (
        payload.get("source_tree_sha256") != actual_digest
        or payload.get("source_file_count") != actual_count
    ):
        raise StackTrendsValidationError("content quality manifest is stale")
    unknown_paths = sorted(set(pages) - actual_paths)
    if unknown_paths:
        raise StackTrendsValidationError("quality manifest references missing Posts")
    complete_count = payload.get("complete_count")
    if (
        isinstance(complete_count, bool)
        or not isinstance(complete_count, int)
        or complete_count < 0
        or len(actual_paths - set(pages)) != complete_count
    ):
        raise StackTrendsValidationError("quality manifest complete-page coverage is invalid")
    return payload


def _quality_status(
    manifest: Mapping[str, Any],
    relative_path: str,
    *,
    document: str,
) -> str:
    raw_page = manifest["pages"].get(relative_path)
    if raw_page is None:
        # content_quality_manifest_v4 deliberately omits clean complete pages.
        # Re-run the shared gate before accepting an omission so a manipulated
        # pages mapping cannot silently turn archived/quarantined content active.
        if analyze_post(document).status != "complete":
            raise StackTrendsValidationError(
                f"missing quality record for non-complete Post: {relative_path}"
            )
        return "complete"
    if not isinstance(raw_page, Mapping):
        raise StackTrendsValidationError(f"invalid quality record for {relative_path}")
    status = raw_page.get("status")
    if not isinstance(status, str):
        raise StackTrendsValidationError(f"missing quality status for {relative_path}")
    return status


def _string(value: Any, *, field: str, maximum: int) -> str:
    if not isinstance(value, str):
        raise StackTrendsValidationError(f"{field} must be a string")
    normalized = re.sub(r"\s+", " ", value).strip()
    if not normalized:
        raise StackTrendsValidationError(f"{field} must not be empty")
    if len(normalized) > maximum:
        normalized = normalized[: maximum - 1].rstrip() + "…"
    return normalized


def _facet_values(value: Any) -> list[str]:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, (list, tuple, set)):
        return []
    result = {
        re.sub(r"\s+", " ", item).strip()
        for item in value
        if isinstance(item, str) and item.strip()
    }
    return sorted(result, key=lambda item: (item.casefold(), item))[:8]


def _safe_internal_url(path: Path, metadata: Mapping[str, Any]) -> str:
    explicit = metadata.get("url")
    if explicit is not None:
        if not isinstance(explicit, str) or not explicit.startswith("/"):
            raise StackTrendsValidationError(f"unsafe internal url in {path.name}")
        parsed = urlsplit(explicit)
        decoded_path = unquote(parsed.path)
        pure = PurePosixPath(decoded_path)
        if (
            parsed.scheme
            or parsed.netloc
            or parsed.query
            or parsed.fragment
            or ".." in pure.parts
            or "\\" in decoded_path
            or any(ord(character) < 32 for character in decoded_path)
        ):
            raise StackTrendsValidationError(f"unsafe internal url in {path.name}")
        result = parsed.path
    else:
        raw_slug = metadata.get("slug", path.stem)
        if not isinstance(raw_slug, str):
            raise StackTrendsValidationError(f"slug must be a string in {path.name}")
        slug = raw_slug.strip()
        if (
            not slug
            or slug in {".", ".."}
            or any(character in slug for character in ("/", "\\", "?", "#"))
            or any(ord(character) < 32 for character in slug)
        ):
            raise StackTrendsValidationError(f"unsafe slug in {path.name}")
        # Hugo currently publishes the content/posts section at /posts/:slug/.
        # Do not infer a date permalink from the stale singular `post` config key.
        result = f"/posts/{slug}/"
    if not result.endswith("/") and "." not in PurePosixPath(result).name:
        result += "/"
    return result


def _identity_digest(canonical_url: str) -> str:
    return hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()


def _observation_identity(canonical_url: str) -> str:
    return f"obs_{_identity_digest(canonical_url)}"


def _event_identity(canonical_url: str) -> str:
    return f"evt_{_identity_digest(canonical_url)}"


def _optional_timestamp(value: Any, *, field: str) -> datetime | None:
    if value is None or value == "":
        return None
    return _parse_timestamp(value, field=field)


def _candidate_from_post(
    path: Path,
    *,
    content_root: Path,
    manifest: Mapping[str, Any],
    config: StackTrendsConfig,
    cutoff: datetime | None,
) -> tuple[str, dict[str, Any]] | None:
    relative = path.relative_to(content_root).as_posix()
    try:
        document = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise StackTrendsValidationError(f"failed to read {path.name}: {exc}") from exc
    metadata = markdown_frontmatter(document)
    if not metadata:
        raise StackTrendsValidationError(f"active post has invalid frontmatter: {path.name}")
    if _quality_status(manifest, relative, document=document) not in _ACTIVE_QUALITY_STATUSES:
        return None
    if metadata.get("draft") is True or metadata.get("archived") is True:
        return None
    archived_at = _parse_timestamp(metadata.get("date"), field=f"{path.name}.date")
    source_published_at = _optional_timestamp(
        metadata.get("source_published_at"),
        field=f"{path.name}.source_published_at",
    )
    first_seen_at = _optional_timestamp(
        metadata.get("first_seen_at"),
        field=f"{path.name}.first_seen_at",
    ) or archived_at
    occurred_at = source_published_at or archived_at
    raw_url = metadata.get("external_url")
    if not isinstance(raw_url, str):
        raise StackTrendsValidationError(f"active post lacks external_url: {path.name}")
    try:
        canonical_url = canonicalize_url(raw_url)
    except ValueError as exc:
        raise StackTrendsValidationError(f"invalid external_url in {path.name}") from exc

    topics = [
        topic
        for topic in normalize_tags(metadata.get("tags"), limit=8)
        if topic not in config.excluded_tags
    ]
    topics = sorted(set(topics), key=lambda item: (item.casefold(), item))
    if not topics:
        return None

    source = str(metadata.get("source") or "unknown").strip() or "unknown"
    observation_id = metadata.get("observation_id")
    if observation_id is None:
        observation_id = _observation_identity(canonical_url)
    else:
        observation_id = _lineage_identifier(
            observation_id, field=f"{path.name}.observation_id"
        )
    event_id = _event_identity(canonical_url)
    event = {
        "event_id": event_id,
        "canonical_event_id": event_id,
        "observation_id": observation_id,
        "lineage_event_id": event_id,
        "lineage_relation": "original",
        "lineage_parent_id": None,
        "occurred_at": _isoformat(occurred_at),
        "first_seen": _isoformat(first_seen_at),
        "source_published_at": (
            _isoformat(source_published_at) if source_published_at is not None else None
        ),
        "timestamp_confidence": str(
            metadata.get("timestamp_confidence")
            or ("publisher" if source_published_at is not None else "observed")
        ),
        "source": source,
        "source_weight": config.source_weight,
        "topics": topics,
        "title": _string(metadata.get("title"), field=f"{path.name}.title", maximum=300),
        "summary": _string(
            metadata.get("description"),
            field=f"{path.name}.description",
            maximum=240,
        ),
        "internal_url": _safe_internal_url(path, metadata),
        "scenarios": _facet_values(metadata.get("scenarios")),
        "categories": _facet_values(metadata.get("categories")),
    }
    return canonical_url, event


def _apply_lineage_to_events(
    events: list[dict[str, Any]],
    lineage: Mapping[str, Mapping[str, Any]],
    *,
    config: StackTrendsConfig,
    cutoff: datetime | None,
    promotion_as_of: datetime,
) -> list[dict[str, Any]]:
    promotion_pairs = {
        (
            promotion.event_id,
            promotion.observation_id,
            promotion.parent_observation_id,
        ): promotion
        for promotion in config.same_event_promotions
    }
    lineage_same_event_pairs: dict[
        tuple[str, str, str], tuple[Mapping[str, Any], Mapping[str, Any]]
    ] = {}
    for observation_id, record in lineage.items():
        if record.get("relation") != "same_event":
            continue
        parent_observation_id = record.get("parent_observation_id")
        if not isinstance(parent_observation_id, str):
            continue
        parent = lineage.get(parent_observation_id)
        if parent is None:
            continue
        lineage_same_event_pairs[
            (str(parent["event_id"]), observation_id, parent_observation_id)
        ] = (record, parent)
    for key in promotion_pairs:
        pair = lineage_same_event_pairs.get(key)
        if pair is None:
            raise StackTrendsValidationError(
                "reviewed same_event promotion does not match lineage"
            )
        _record, parent = pair
        if parent.get("relation") not in _LINEAGE_MERGED_RELATIONS:
            raise StackTrendsValidationError(
                "reviewed same_event parent must already be canonical"
            )

    joined: list[dict[str, Any]] = []
    for event in events:
        candidate = dict(event)
        record = lineage.get(candidate["observation_id"])
        if record is not None:
            if record.get("article_url") != candidate["internal_url"]:
                raise StackTrendsValidationError(
                    f"lineage article route mismatch: {candidate['observation_id']}"
                )
            relation = str(record["relation"])
            lineage_event_id = _lineage_identifier(
                record.get("event_id"), field="lineage event_id"
            )
            candidate["lineage_event_id"] = lineage_event_id
            candidate["lineage_relation"] = relation
            candidate["lineage_parent_id"] = record.get("parent_observation_id")
            candidate["timestamp_confidence"] = str(
                record.get("timestamp_confidence") or candidate["timestamp_confidence"]
            )
            published = _optional_timestamp(
                record.get("source_published_at"), field="lineage source_published_at"
            )
            first_seen = _optional_timestamp(
                record.get("first_seen_at"), field="lineage first_seen_at"
            )
            if published is not None:
                candidate["occurred_at"] = _isoformat(published)
                candidate["source_published_at"] = _isoformat(published)
            if first_seen is not None:
                candidate["first_seen"] = _isoformat(first_seen)
            if relation in _LINEAGE_MERGED_RELATIONS:
                candidate["canonical_event_id"] = lineage_event_id
                if relation == "original":
                    candidate["event_id"] = lineage_event_id
            elif relation == "same_event":
                parent_observation_id = record.get("parent_observation_id")
                parent = lineage.get(str(parent_observation_id))
                target_event_id = (
                    str(parent["event_id"])
                    if parent is not None
                    else lineage_event_id
                )
                promotion = promotion_pairs.get(
                    (
                        target_event_id,
                        candidate["observation_id"],
                        str(parent_observation_id),
                    )
                )
                if promotion is not None and promotion.reviewed_at <= promotion_as_of:
                    candidate["canonical_event_id"] = promotion.event_id
        if cutoff is not None and _parse_timestamp(
            candidate["occurred_at"], field="occurred_at"
        ) > cutoff:
            continue
        joined.append(candidate)

    # High-confidence copies may be suppressed before a local Post is written.
    # They still matter as propagation observations, but inherit only the
    # representative event's already-public topic facets and internal drilldown.
    # Archived observations retain an article_url and remain outside this path.
    present_observations = {event["observation_id"] for event in joined}
    representatives: dict[str, dict[str, Any]] = {}
    for event in joined:
        if event["lineage_relation"] not in _LINEAGE_MERGED_RELATIONS:
            continue
        canonical_id = event["canonical_event_id"]
        current = representatives.get(canonical_id)
        if current is None or (
            event["occurred_at"], event["first_seen"], event["observation_id"]
        ) < (
            current["occurred_at"], current["first_seen"], current["observation_id"]
        ):
            representatives[canonical_id] = event
    for observation_id, record in sorted(lineage.items()):
        if observation_id in present_observations:
            continue
        if record.get("article_url") is not None:
            continue
        relation = str(record.get("relation") or "")
        if relation not in {"exact_copy", "syndicated"}:
            continue
        canonical_id = str(record.get("event_id") or "")
        representative = representatives.get(canonical_id)
        if representative is None:
            continue
        published = _optional_timestamp(
            record.get("source_published_at"), field="lineage source_published_at"
        )
        first_seen = _optional_timestamp(
            record.get("first_seen_at"), field="lineage first_seen_at"
        )
        occurred = published or first_seen
        if occurred is None:
            continue
        if cutoff is not None and occurred > cutoff:
            continue
        joined.append({
            "event_id": f"evt_{observation_id.removeprefix('obs_')}",
            "canonical_event_id": canonical_id,
            "observation_id": observation_id,
            "lineage_event_id": canonical_id,
            "lineage_relation": relation,
            "lineage_parent_id": record.get("parent_observation_id"),
            "occurred_at": _isoformat(occurred),
            "first_seen": _isoformat(first_seen or occurred),
            "source_published_at": _isoformat(published) if published is not None else None,
            "timestamp_confidence": str(record.get("timestamp_confidence") or "unknown"),
            "source": str(record["source"]),
            "source_weight": representative["source_weight"],
            "topics": list(representative["topics"]),
            "title": str(record["title"]),
            "summary": (
                "高置信重复观察未生成独立文章；"
                "可在代表文章的溯源区核验来源链。"
            ),
            "internal_url": representative["internal_url"],
            "scenarios": list(representative["scenarios"]),
            "categories": list(representative["categories"]),
            "suppressed_observation": True,
        })

    # A canonical event may be archived or outside the selected content cutoff.
    # Promote the earliest active observation to a synthetic canonical record so
    # valid aliases do not disappear from trend calculation.
    merged_groups: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in joined:
        if event["canonical_event_id"] != event["event_id"]:
            merged_groups[event["canonical_event_id"]].append(event)
        elif event["lineage_relation"] in _LINEAGE_MERGED_RELATIONS:
            merged_groups[event["canonical_event_id"]].append(event)
    for canonical_id, members in merged_groups.items():
        canonical = next(
            (event for event in members if event["event_id"] == canonical_id),
            None,
        )
        if canonical is None:
            canonical = min(
                members,
                key=lambda event: (
                    event["occurred_at"],
                    event["first_seen"],
                    event["observation_id"],
                ),
            )
            canonical["event_id"] = canonical_id
        canonical_topics = list(canonical["topics"])
        for member in members:
            member["topics"] = canonical_topics

    return sorted(joined, key=lambda event: (event["event_id"], event["observation_id"]))


def adapt_posts_to_events(
    *,
    content_root: str | Path,
    quality_manifest_path: str | Path,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    lineage_root: str | Path | None = None,
    as_of: datetime | str | None = None,
) -> dict[str, Any]:
    """Adapt active Posts to public-safe, canonical ``trend_v1`` events."""

    root = Path(content_root).resolve()
    if not root.is_dir():
        raise StackTrendsValidationError(f"content root does not exist: {root}")
    manifest = _load_quality_manifest(Path(quality_manifest_path), content_root=root)
    config = load_stack_trends_config(config_path)
    cutoff = _parse_timestamp(as_of, field="as_of") if as_of is not None else None
    lineage, lineage_mode = _load_lineage_observations(lineage_root)

    by_canonical_url: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in sorted(root.rglob("*.md"), key=lambda item: item.as_posix()):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if not relative.parts or relative.parts[0] != "posts":
            continue
        candidate = _candidate_from_post(
            path,
            content_root=root,
            manifest=manifest,
            config=config,
            cutoff=cutoff,
        )
        if candidate is not None:
            canonical_url, event = candidate
            by_canonical_url[canonical_url].append(event)

    selected_events: list[dict[str, Any]] = []
    for canonical_url in sorted(by_canonical_url):
        candidates = by_canonical_url[canonical_url]
        # The earliest public observation represents the canonical source event;
        # duplicates cannot move it forward or boost trend quantity/novelty.
        selected = min(
            candidates,
            key=lambda event: (
                event["occurred_at"],
                event["internal_url"],
                _stable_json_bytes(event),
            ),
        )
        selected_events.append(selected)
    promotion_as_of = cutoff or max(
        (
            _parse_timestamp(event["occurred_at"], field="occurred_at")
            for event in selected_events
        ),
        default=datetime(1970, 1, 1, tzinfo=UTC),
    )
    events = _apply_lineage_to_events(
        selected_events,
        lineage,
        config=config,
        cutoff=cutoff,
        promotion_as_of=promotion_as_of,
    )

    if events:
        latest = max(
            _parse_timestamp(event["occurred_at"], field="occurred_at")
            for event in events
        )
    elif cutoff is not None:
        latest = cutoff
    else:
        latest = datetime(1970, 1, 1, tzinfo=UTC)
    effective_cutoff = cutoff or latest
    return {
        "events": events,
        "as_of": _isoformat(effective_cutoff),
        "data_as_of": _isoformat(latest),
        "quality_manifest_sha256": hashlib.sha256(
            Path(quality_manifest_path).read_bytes()
        ).hexdigest(),
        "config_version": config.version,
        "lineage_mode": lineage_mode,
    }


def _duration_by_name() -> dict[str, timedelta]:
    return dict(WINDOWS)


def _events_for_topic(
    events: Iterable[Mapping[str, Any]],
    topic: str,
    *,
    start: datetime,
    end: datetime,
    include_end: bool = True,
    canonical_only: bool = False,
) -> list[Mapping[str, Any]]:
    result = []
    for event in events:
        if canonical_only and event.get("event_id") != event.get("canonical_event_id"):
            continue
        occurred_at = _parse_timestamp(event["occurred_at"], field="occurred_at")
        in_range = start <= occurred_at <= end if include_end else start <= occurred_at < end
        if in_range and topic in event["topics"]:
            result.append(event)
    return sorted(result, key=lambda event: event["event_id"])


def _trend_counts(
    events: list[Mapping[str, Any]],
    topic: str,
    *,
    cutoff: datetime,
    duration: timedelta,
) -> dict[str, int]:
    current_start = cutoff - duration
    previous_start = current_start - duration
    pre_previous_start = previous_start - duration
    return {
        "current": len(
            _events_for_topic(
                events,
                topic,
                start=current_start,
                end=cutoff,
                canonical_only=True,
            )
        ),
        "previous": len(
            _events_for_topic(
                events,
                topic,
                start=previous_start,
                end=current_start,
                include_end=False,
                canonical_only=True,
            )
        ),
        "pre_previous": len(
            _events_for_topic(
                events,
                topic,
                start=pre_previous_start,
                end=previous_start,
                include_end=False,
                canonical_only=True,
            )
        ),
    }


def _signal_state(counts: Mapping[str, int]) -> str:
    current = counts["current"]
    previous = counts["previous"]
    if previous == 0 and current >= MINIMUM_UNIQUE_EVENTS:
        return "new"
    if current > previous:
        return "rising"
    if current == previous:
        return "steady"
    return "cooling"


def _confidence(unique_events: int, unique_sources: int) -> str:
    return "high" if unique_events >= 5 and unique_sources >= 2 else "medium"


def _sparkline(
    events: Iterable[Mapping[str, Any]],
    topic: str,
    *,
    cutoff: datetime,
    duration: timedelta,
) -> list[int]:
    start = cutoff - duration
    duration_seconds = duration.total_seconds()
    buckets = [0] * SPARKLINE_BUCKETS
    for event in _events_for_topic(
        events,
        topic,
        start=start,
        end=cutoff,
        canonical_only=True,
    ):
        occurred_at = _parse_timestamp(event["occurred_at"], field="occurred_at")
        offset = max(0.0, (occurred_at - start).total_seconds())
        index = min(
            SPARKLINE_BUCKETS - 1,
            int((offset / duration_seconds) * SPARKLINE_BUCKETS),
        )
        buckets[index] += 1
    return buckets


def _facet(items: Iterable[str], *, limit: int = 12) -> list[dict[str, Any]]:
    counts = Counter(item for item in items if item)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0].casefold(), item[0]))
    return [{"name": name, "count": count} for name, count in ranked[:limit]]


def _event_facets(events: Iterable[Mapping[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    selected = list(events)
    return {
        "sources": _facet(str(event["source"]) for event in selected),
        "scenarios": _facet(
            scenario for event in selected for scenario in event.get("scenarios", [])
        ),
    }


def _trend_projection(
    trend: Mapping[str, Any],
    *,
    events: list[Mapping[str, Any]],
    cutoff: datetime,
    duration: timedelta,
) -> dict[str, Any]:
    topic = str(trend["topic"])
    topic_id = f"tag:{topic}"
    current_events = _events_for_topic(
        events,
        topic,
        start=cutoff - duration,
        end=cutoff,
    )
    counts = _trend_counts(events, topic, cutoff=cutoff, duration=duration)
    facets = _event_facets(current_events)
    observations = int(trend["observations"])
    unique_events = int(trend["unique_events"])
    source_diversity = len({str(event["source"]) for event in current_events})
    return {
        "id": topic_id,
        "topic": topic,
        "graph_node_id": topic_id,
        "score": trend["score"],
        "state": _signal_state(counts),
        "confidence": _confidence(trend["unique_events"], trend["unique_sources"]),
        "unique_events": unique_events,
        "observations": observations,
        "redundant_observations": max(0, observations - unique_events),
        "source_diversity": source_diversity,
        "unique_sources": trend["unique_sources"],
        "duplicate_rate": trend["duplicate_rate"],
        "counts": counts,
        "components": trend["components"],
        "sparkline": _sparkline(
            events,
            topic,
            cutoff=cutoff,
            duration=duration,
        ),
        "sources": facets["sources"],
        "scenarios": facets["scenarios"],
    }


def _reference(path: str, body: bytes, **extra: Any) -> dict[str, Any]:
    return {
        "path": path,
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        **extra,
    }


def _related_topics(
    *,
    topic: str,
    events: list[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    topic_events = [event for event in events if topic in event["topics"]]
    topic_event_ids = {event["canonical_event_id"] for event in topic_events}
    all_topic_ids: defaultdict[str, set[str]] = defaultdict(set)
    for event in events:
        for label in event["topics"]:
            all_topic_ids[label].add(event["canonical_event_id"])
    related: list[dict[str, Any]] = []
    for label, event_ids in all_topic_ids.items():
        if label == topic:
            continue
        cooccurrence = len(topic_event_ids & event_ids)
        if cooccurrence < 2:
            continue
        union = len(topic_event_ids | event_ids)
        topic_id = f"tag:{label}"
        related.append(
            {
                "id": topic_id,
                "topic": label,
                "graph_node_id": topic_id,
                "cooccurrence": cooccurrence,
                "jaccard": round(cooccurrence / union, 6) if union else 0,
            }
        )
    related.sort(
        key=lambda item: (
            -item["jaccard"],
            -item["cooccurrence"],
            item["topic"].casefold(),
            item["topic"],
        )
    )
    return related[:RELATED_TOPIC_LIMIT]


def _evidence_projection(events: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: defaultdict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for event in events:
        grouped[str(event["canonical_event_id"])].append(event)
    evidence: list[dict[str, Any]] = []
    for event_id, observations in grouped.items():
        representative = next(
            (item for item in observations if item["event_id"] == event_id),
            min(
                observations,
                key=lambda item: (
                    item["occurred_at"],
                    item["first_seen"],
                    item["observation_id"],
                ),
            ),
        )
        related = sorted(
            (
                item
                for item in observations
                if item["observation_id"] != representative["observation_id"]
            ),
            key=lambda item: (item["occurred_at"], item["observation_id"]),
            reverse=True,
        )
        evidence.append(
            {
                "id": event_id,
                "observation_id": representative["observation_id"],
                "title": representative["title"],
                "summary": representative["summary"],
                "source": representative["source"],
                "published_at": representative["occurred_at"],
                "internal_url": representative["internal_url"],
                "relation": representative["lineage_relation"],
                "associated_observations": len(observations),
                "related_reports": [
                    {
                        "observation_id": item["observation_id"],
                        "title": item["title"],
                        "source": item["source"],
                        "published_at": item["occurred_at"],
                        "internal_url": item["internal_url"],
                        "relation": item["lineage_relation"],
                    }
                    for item in related[:5]
                ],
            }
        )
    evidence.sort(
        key=lambda item: (item["published_at"], item["id"]),
        reverse=True,
    )
    return evidence[:TOPIC_EVIDENCE_LIMIT]


def _topic_payload(
    *,
    topic: str,
    projected_by_window: Mapping[str, Mapping[str, Mapping[str, Any]]],
    events: list[Mapping[str, Any]],
    cutoff: datetime,
    data_as_of: str,
) -> dict[str, Any]:
    topic_id = f"tag:{topic}"
    thirty_days = _events_for_topic(
        events,
        topic,
        start=cutoff - _duration_by_name()["30d"],
        end=cutoff,
    )
    ordered_evidence = _evidence_projection(thirty_days)
    windows: dict[str, Any] = {}
    for window_name, _ in WINDOWS:
        projected = projected_by_window[window_name].get(topic_id)
        windows[window_name] = (
            None
            if projected is None
            else {
                "score": projected["score"],
                "state": projected["state"],
                "confidence": projected["confidence"],
                "unique_events": projected["unique_events"],
                "observations": projected["observations"],
                "redundant_observations": projected["redundant_observations"],
                "unique_sources": projected["unique_sources"],
                "source_diversity": projected["source_diversity"],
                "counts": projected["counts"],
                "sparkline": projected["sparkline"],
            }
        )
    return {
        "schema_version": TOPIC_SCHEMA_VERSION,
        "id": topic_id,
        "topic": topic,
        "graph_node_id": topic_id,
        "data_as_of": data_as_of,
        "description": f"本站近 30 天收录的 {topic} 相关证据与变化。",
        "windows": windows,
        "related_topics": _related_topics(
            topic=topic,
            events=thirty_days,
        ),
        "sources": _facet(str(event["source"]) for event in thirty_days),
        "scenarios": _facet(
            scenario for event in thirty_days for scenario in event.get("scenarios", [])
        ),
        "categories": _facet(
            category for event in thirty_days for category in event.get("categories", [])
        ),
        "evidence": ordered_evidence,
    }


def _scan_public_value(value: Any, *, location: str = "root") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in _DENIED_PUBLIC_KEYS:
                raise StackTrendsValidationError(f"denied public field {key} at {location}")
            _scan_public_value(child, location=f"{location}.{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _scan_public_value(child, location=f"{location}[{index}]")
        return
    if isinstance(value, str):
        if any(ord(character) < 32 for character in value) or any(
            character in value for character in "<>"
        ):
            raise StackTrendsValidationError(f"unsafe public text at {location}")
        if any(pattern.search(value) for pattern in _SENSITIVE_PATTERNS):
            raise StackTrendsValidationError(f"sensitive public text at {location}")


def _safe_reference_path(value: Any, *, prefix: str) -> str:
    if not isinstance(value, str) or not value:
        raise StackTrendsValidationError("asset reference path must be non-empty")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or ".." in pure.parts
        or not value.startswith(prefix)
        or not _ASSET_PATH_RE.fullmatch(value)
        or "//" in value
    ):
        raise StackTrendsValidationError(f"unsafe asset reference path: {value}")
    return value


def _write_atomic(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as output:
            output.write(body)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def build_stack_trends(
    *,
    content_root: str | Path,
    quality_manifest_path: str | Path,
    output_dir: str | Path,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    lineage_root: str | Path | None = None,
    as_of: datetime | str | None = None,
) -> dict[str, Any]:
    """Build content-addressed trend assets and write ``index.json`` last."""

    dataset = adapt_posts_to_events(
        content_root=content_root,
        quality_manifest_path=quality_manifest_path,
        config_path=config_path,
        lineage_root=lineage_root,
        as_of=as_of,
    )
    events = dataset["events"]
    cutoff = _parse_timestamp(dataset["as_of"], field="as_of")
    calculated = calculate_trends(
        events,
        as_of=cutoff,
        minimum_unique_events=MINIMUM_UNIQUE_EVENTS,
    )
    durations = _duration_by_name()

    projected_by_window: dict[str, dict[str, dict[str, Any]]] = {}
    ordered_by_window: dict[str, list[dict[str, Any]]] = {}
    for window_name, _ in WINDOWS:
        trends = calculated["windows"][window_name]["trends"][:WINDOW_TREND_LIMIT]
        projected = [
            _trend_projection(
                trend,
                events=events,
                cutoff=cutoff,
                duration=durations[window_name],
            )
            for trend in trends
        ]
        ordered_by_window[window_name] = projected
        projected_by_window[window_name] = {trend["id"]: trend for trend in projected}

    topic_labels = sorted(
        {
            trend["topic"]
            for trends in ordered_by_window.values()
            for trend in trends
        },
        key=lambda item: (item.casefold(), item),
    )
    assets: dict[str, bytes] = {}
    topic_refs: dict[str, dict[str, Any]] = {}
    for topic in topic_labels:
        payload = _topic_payload(
            topic=topic,
            projected_by_window=projected_by_window,
            events=events,
            cutoff=cutoff,
            data_as_of=dataset["data_as_of"],
        )
        _scan_public_value(payload)
        body = _stable_json_bytes(payload)
        topic_id = f"tag:{topic}"
        id_hash = hashlib.sha256(topic_id.encode("utf-8")).hexdigest()[:16]
        content_hash = hashlib.sha256(body).hexdigest()
        path = f"topics/{id_hash}-{content_hash[:12]}.json"
        assets[path] = body
        topic_refs[topic_id] = _reference(path, body)

    window_refs: dict[str, dict[str, Any]] = {}
    window_stats: dict[str, dict[str, int]] = {}
    for window_name, _ in WINDOWS:
        projected = []
        for trend in ordered_by_window[window_name]:
            projected.append(
                {
                    **trend,
                    "detail_path": topic_refs[trend["id"]]["path"],
                }
            )
        evidence_ids = {
            event_id
            for trend in calculated["windows"][window_name]["trends"][:WINDOW_TREND_LIMIT]
            for event_id in trend["event_ids"]
        }
        evidence = [
            event for event in events if event["canonical_event_id"] in evidence_ids
        ]
        facets = _event_facets(evidence)
        sample_notice = (
            "样本量较小，建议结合更长时间窗口判断。"
            if len(projected) < 3 or len(evidence) < 30
            else None
        )
        payload = {
            "schema_version": WINDOW_SCHEMA_VERSION,
            "window": window_name,
            "data_as_of": dataset["data_as_of"],
            "minimum_unique_events": MINIMUM_UNIQUE_EVENTS,
            "formula": TREND_FORMULA,
            "sample_notice": sample_notice,
            "facets": facets,
            "trends": projected,
        }
        _scan_public_value(payload)
        body = _stable_json_bytes(payload)
        content_hash = hashlib.sha256(body).hexdigest()
        path = f"windows/{window_name}-{content_hash[:12]}.json"
        assets[path] = body
        window_refs[window_name] = _reference(
            path,
            body,
            trend_count=len(projected),
        )
        window_stats[window_name] = {
            "trend_count": len(projected),
            "evidence_articles": len(evidence),
            "unique_events": len(evidence_ids),
            "redundant_observations": max(0, len(evidence) - len(evidence_ids)),
            "source_count": len({event["source"] for event in evidence}),
        }

    index = {
        "schema_version": INDEX_SCHEMA_VERSION,
        # Deliberately deterministic: no wall clock enters committed assets.
        "generated_at": dataset["data_as_of"],
        "data_as_of": dataset["data_as_of"],
        "realtime": False,
        "lineage_mode": dataset["lineage_mode"],
        "timezone": "Asia/Shanghai",
        "default_window": DEFAULT_WINDOW,
        "disclaimer": "基于本站收录证据，不代表全网热度。",
        "formula": TREND_FORMULA,
        "normalization": calculated["normalization"],
        "stats": {
            "eligible_articles": len(events),
            "unique_events": len(
                {event["canonical_event_id"] for event in events}
            ),
            "redundant_observations": max(
                0,
                len(events) - len({event["canonical_event_id"] for event in events}),
            ),
            "promoted_same_event_pairs": sum(
                event["lineage_relation"] == "same_event"
                and event["canonical_event_id"] != event["event_id"]
                for event in events
            ),
            "topic_count": len(topic_refs),
            "source_count": len({event["source"] for event in events}),
            "windows": window_stats,
        },
        "windows": window_refs,
        "topics": topic_refs,
    }
    _scan_public_value(index)
    index_body = _stable_json_bytes(index)
    assets["index.json"] = index_body

    if len(index_body) > INDEX_MAX_BYTES:
        raise StackTrendsValidationError("index exceeds 64 KiB")
    for path, body in assets.items():
        if path.startswith("windows/") and len(body) > WINDOW_MAX_BYTES:
            raise StackTrendsValidationError(f"window asset exceeds 128 KiB: {path}")
        if path.startswith("topics/") and len(body) > TOPIC_MAX_BYTES:
            raise StackTrendsValidationError(f"topic asset exceeds 96 KiB: {path}")
    if len(assets) > TOTAL_MAX_FILES:
        raise StackTrendsValidationError("trend assets exceed 100 files")
    if sum(len(body) for body in assets.values()) > TOTAL_MAX_BYTES:
        raise StackTrendsValidationError("trend assets exceed 2 MiB")

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    for relative_path in sorted(path for path in assets if path != "index.json"):
        _write_atomic(output / relative_path, assets[relative_path])
    expected = set(assets)
    for existing in sorted(output.rglob("*.json"), key=lambda item: item.as_posix()):
        relative = existing.relative_to(output).as_posix()
        if relative not in expected and relative != "index.json":
            existing.unlink()
    _write_atomic(output / "index.json", index_body)
    for directory in sorted(
        (path for path in output.rglob("*") if path.is_dir()),
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        try:
            directory.rmdir()
        except OSError:
            pass

    verification = verify_stack_trends(output, verify_hashes=True)
    return {
        "index_path": "index.json",
        "data_as_of": dataset["data_as_of"],
        "file_count": verification["file_count"],
        "total_bytes": verification["total_bytes"],
    }


def _load_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StackTrendsValidationError(f"invalid JSON asset {path.name}: {exc}") from exc
    if not isinstance(payload, dict):
        raise StackTrendsValidationError(f"asset root must be an object: {path.name}")
    return payload


def _verified_mapping(value: Any, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise StackTrendsValidationError(f"{field} must be an object")
    return value


def _verified_list(value: Any, *, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise StackTrendsValidationError(f"{field} must be an array")
    return value


def _verified_count(value: Any, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise StackTrendsValidationError(f"{field} must be a non-negative integer")
    return value


def _verified_release_timestamp(value: Any, *, field: str) -> str:
    parsed = _parse_timestamp(value, field=field)
    canonical = _isoformat(parsed)
    if value != canonical:
        raise StackTrendsValidationError(f"{field} must use canonical UTC RFC3339")
    return canonical


def _verify_topic_identity(
    payload: Mapping[str, Any],
    *,
    expected_id: str,
    location: str,
) -> None:
    topic = payload.get("topic")
    if not isinstance(topic, str) or not topic or f"tag:{topic}" != expected_id:
        raise StackTrendsValidationError(f"topic identity mismatch: {location}")
    if payload.get("id") != expected_id or payload.get("graph_node_id") != expected_id:
        raise StackTrendsValidationError(f"topic identity mismatch: {location}")


def _verify_asset_reference(
    *,
    output: Path,
    reference: Any,
    prefix: str,
    schema: str,
    verify_hashes: bool,
    referenced: set[str],
) -> tuple[str, dict[str, Any], int]:
    checked = _verified_mapping(reference, field="asset reference")
    relative = _safe_reference_path(checked.get("path"), prefix=prefix)
    if relative in referenced:
        raise StackTrendsValidationError(f"duplicate asset reference path: {relative}")
    referenced.add(relative)
    path = output / relative
    try:
        body = path.read_bytes()
    except OSError:
        body = b""
    if not body:
        raise StackTrendsValidationError(f"missing referenced asset: {relative}")
    expected_size = checked.get("bytes")
    if (
        isinstance(expected_size, bool)
        or not isinstance(expected_size, int)
        or expected_size != len(body)
    ):
        raise StackTrendsValidationError(f"byte size mismatch: {relative}")
    expected_digest = checked.get("sha256")
    if not isinstance(expected_digest, str) or not re.fullmatch(
        r"[0-9a-f]{64}", expected_digest
    ):
        raise StackTrendsValidationError(f"invalid sha256 reference: {relative}")
    digest = hashlib.sha256(body).hexdigest()
    if verify_hashes and expected_digest != digest:
        raise StackTrendsValidationError(f"sha256 mismatch: {relative}")
    if not Path(relative).name.endswith(f"-{digest[:12]}.json"):
        raise StackTrendsValidationError(f"content hash filename mismatch: {relative}")
    payload = _load_json_object(path)
    if payload.get("schema_version") != schema:
        raise StackTrendsValidationError(f"schema mismatch: {relative}")
    _scan_public_value(payload)
    limit = WINDOW_MAX_BYTES if prefix == "windows/" else TOPIC_MAX_BYTES
    if len(body) > limit:
        raise StackTrendsValidationError(f"asset exceeds byte budget: {relative}")
    return relative, payload, len(body)


def verify_stack_trends(
    root: str | Path,
    *,
    verify_hashes: bool = True,
) -> dict[str, Any]:
    """Verify schemas, references, hashes, budgets and public-data boundaries."""

    output = Path(root)
    index_path = output / "index.json"
    index = _load_json_object(index_path)
    index_schema = index.get("schema_version")
    if index_schema not in {INDEX_SCHEMA_VERSION_V1, INDEX_SCHEMA_VERSION_V2}:
        raise StackTrendsValidationError("invalid stack trends index schema")
    is_v2 = index_schema == INDEX_SCHEMA_VERSION_V2
    window_schema = WINDOW_SCHEMA_VERSION_V2 if is_v2 else WINDOW_SCHEMA_VERSION_V1
    topic_schema = TOPIC_SCHEMA_VERSION_V2 if is_v2 else TOPIC_SCHEMA_VERSION_V1
    _scan_public_value(index)
    data_as_of = _verified_release_timestamp(
        index.get("data_as_of"), field="index.data_as_of"
    )
    generated_at = _verified_release_timestamp(
        index.get("generated_at"), field="index.generated_at"
    )
    if generated_at != data_as_of:
        raise StackTrendsValidationError(
            "index generated_at must equal data_as_of for deterministic releases"
        )

    expected_windows = {name for name, _ in WINDOWS}
    windows = _verified_mapping(index.get("windows"), field="index windows")
    if set(windows) != expected_windows:
        raise StackTrendsValidationError("index must reference 24h, 7d and 30d windows")
    topics = _verified_mapping(index.get("topics"), field="index topics")
    if index.get("default_window") not in windows:
        raise StackTrendsValidationError("index default_window must reference a window")
    stats = _verified_mapping(index.get("stats"), field="index stats")
    stats_windows = _verified_mapping(
        stats.get("windows"), field="index stats.windows"
    )
    if set(stats_windows) != expected_windows:
        raise StackTrendsValidationError("index stats.windows identity mismatch")
    if _verified_count(stats.get("topic_count"), field="index stats.topic_count") != len(
        topics
    ):
        raise StackTrendsValidationError("index topic_count mismatch")
    if is_v2:
        eligible_articles = _verified_count(
            stats.get("eligible_articles"), field="index stats.eligible_articles"
        )
        unique_events = _verified_count(
            stats.get("unique_events"), field="index stats.unique_events"
        )
        redundant_observations = _verified_count(
            stats.get("redundant_observations"),
            field="index stats.redundant_observations",
        )
        promoted_same_event_pairs = _verified_count(
            # Additive v2 rollout fallback: an older v2 index predating the
            # reviewed-promotion gate could not have promoted same_event pairs.
            stats.get("promoted_same_event_pairs", 0),
            field="index stats.promoted_same_event_pairs",
        )
        if (
            unique_events > eligible_articles
            or redundant_observations != eligible_articles - unique_events
            or promoted_same_event_pairs > redundant_observations
        ):
            raise StackTrendsValidationError("index event accounting mismatch")

    referenced = {"index.json"}
    topic_paths: dict[str, str] = {}
    topic_payloads: dict[str, Mapping[str, Any]] = {}
    for topic_id in sorted(topics):
        if not isinstance(topic_id, str):
            raise StackTrendsValidationError("index topic identity must be a string")
        relative, payload, _ = _verify_asset_reference(
            output=output,
            reference=topics[topic_id],
            prefix="topics/",
            schema=topic_schema,
            verify_hashes=verify_hashes,
            referenced=referenced,
        )
        _verify_topic_identity(payload, expected_id=topic_id, location=relative)
        if payload.get("data_as_of") != data_as_of:
            raise StackTrendsValidationError(f"topic data_as_of mismatch: {relative}")
        if is_v2:
            evidence = _verified_list(
                payload.get("evidence"), field=f"{relative} evidence"
            )
            for position, raw_evidence in enumerate(evidence):
                item = _verified_mapping(
                    raw_evidence, field=f"{relative} evidence[{position}]"
                )
                associated = _verified_count(
                    item.get("associated_observations"),
                    field=f"{relative} associated_observations",
                )
                related = _verified_list(
                    item.get("related_reports"),
                    field=f"{relative} related_reports",
                )
                if associated < 1 or associated < len(related) + 1:
                    raise StackTrendsValidationError(
                        f"topic associated observation count mismatch: {relative}"
                    )
        topic_paths[topic_id] = relative
        topic_payloads[topic_id] = payload

    topics_seen_in_windows: set[str] = set()
    for window_name in sorted(windows):
        relative, payload, _ = _verify_asset_reference(
            output=output,
            reference=windows[window_name],
            prefix="windows/",
            schema=window_schema,
            verify_hashes=verify_hashes,
            referenced=referenced,
        )
        if payload.get("window") != window_name:
            raise StackTrendsValidationError(f"window identity mismatch: {relative}")
        if payload.get("data_as_of") != data_as_of:
            raise StackTrendsValidationError(f"window data_as_of mismatch: {relative}")
        trends = _verified_list(payload.get("trends"), field=f"{relative} trends")
        expected_count = len(trends)
        reference_count = _verified_count(
            _verified_mapping(windows[window_name], field="window reference").get(
                "trend_count"
            ),
            field=f"{relative} trend_count",
        )
        stats_count = _verified_count(
            _verified_mapping(
                stats_windows[window_name], field="index window stats"
            ).get("trend_count"),
            field=f"index stats.windows.{window_name}.trend_count",
        )
        if reference_count != expected_count or stats_count != expected_count:
            raise StackTrendsValidationError(f"window trend_count mismatch: {relative}")
        window_topic_ids: set[str] = set()
        for position, raw_trend in enumerate(trends):
            trend = _verified_mapping(
                raw_trend, field=f"{relative} trends[{position}]"
            )
            trend_id = trend.get("id")
            if not isinstance(trend_id, str):
                raise StackTrendsValidationError(f"trend topic identity mismatch: {relative}")
            _verify_topic_identity(
                trend,
                expected_id=trend_id,
                location=f"{relative} trends[{position}]",
            )
            if trend_id in window_topic_ids:
                raise StackTrendsValidationError(f"duplicate trend topic: {relative}")
            window_topic_ids.add(trend_id)
            expected_detail = topic_paths.get(trend_id)
            if expected_detail is None:
                raise StackTrendsValidationError(f"trend topic reference missing: {relative}")
            if trend.get("detail_path") != expected_detail:
                raise StackTrendsValidationError(f"trend detail_path mismatch: {relative}")
            if is_v2:
                unique_events = _verified_count(
                    trend.get("unique_events"), field=f"{relative} unique_events"
                )
                observations = _verified_count(
                    trend.get("observations"), field=f"{relative} observations"
                )
                redundant = _verified_count(
                    trend.get("redundant_observations"),
                    field=f"{relative} redundant_observations",
                )
                _verified_count(
                    trend.get("source_diversity"),
                    field=f"{relative} source_diversity",
                )
                if observations < unique_events or redundant != observations - unique_events:
                    raise StackTrendsValidationError(
                        f"trend observation accounting mismatch: {relative}"
                    )
        topics_seen_in_windows.update(window_topic_ids)

    if topics_seen_in_windows != set(topic_payloads):
        raise StackTrendsValidationError("index topic references do not match window trends")

    files = {
        path.relative_to(output).as_posix(): path
        for path in output.rglob("*")
        if path.is_file()
    }
    orphans = sorted(set(files) - referenced)
    if orphans:
        raise StackTrendsValidationError(f"orphan trend assets: {', '.join(orphans)}")
    if set(files) != referenced:
        missing = sorted(referenced - set(files))
        raise StackTrendsValidationError(f"missing trend assets: {', '.join(missing)}")
    total_bytes = sum(path.stat().st_size for path in files.values())
    if index_path.stat().st_size > INDEX_MAX_BYTES:
        raise StackTrendsValidationError("index exceeds byte budget")
    if len(files) > TOTAL_MAX_FILES or total_bytes > TOTAL_MAX_BYTES:
        raise StackTrendsValidationError("trend asset collection exceeds budget")
    return {
        "schema_version": index_schema,
        "data_as_of": data_as_of,
        "file_count": len(files),
        "total_bytes": total_bytes,
    }


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "DEFAULT_LINEAGE_ROOT",
    "INDEX_SCHEMA_VERSION",
    "INDEX_SCHEMA_VERSION_V1",
    "INDEX_SCHEMA_VERSION_V2",
    "SameEventPromotion",
    "StackTrendsConfig",
    "StackTrendsValidationError",
    "TOPIC_SCHEMA_VERSION",
    "TOPIC_SCHEMA_VERSION_V1",
    "TOPIC_SCHEMA_VERSION_V2",
    "WINDOW_SCHEMA_VERSION",
    "WINDOW_SCHEMA_VERSION_V1",
    "WINDOW_SCHEMA_VERSION_V2",
    "adapt_posts_to_events",
    "build_stack_trends",
    "load_stack_trends_config",
    "verify_stack_trends",
]
