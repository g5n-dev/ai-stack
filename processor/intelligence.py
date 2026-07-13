"""Deterministic static-intelligence primitives.

This module deliberately has no network, database, or model dependency.  It turns
validated event records into transparent trend scores and immutable JSON shards
that a static Hugo deployment can serve directly.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
import tempfile
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


API_SCHEMA_VERSION = "intelligence_api_v1"
TREND_SCHEMA_VERSION = "trend_v1"
TREND_FORMULA = (
    "100 × (0.25×quantity + 0.25×growth + 0.15×acceleration + "
    "0.15×source_diversity + 0.10×novelty + 0.10×source_weight) "
    "× (1 − 0.5×duplicate_rate)"
)

WINDOWS: tuple[tuple[str, timedelta], ...] = (
    ("24h", timedelta(hours=24)),
    ("7d", timedelta(days=7)),
    ("30d", timedelta(days=30)),
)
MINIMUM_UNIQUE_EVENTS = 3
QUANTITY_NORMALIZATION_TARGET = 10
RELEASE_ID_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,126}[A-Za-z0-9])?$")
BLOCKED_PUBLIC_STATUSES = {
    "ALIAS",
    "DEAD_LETTER",
    "DELETED",
    "MERGED",
    "QUARANTINED",
    "REJECTED",
    "UNKNOWN",
}


class IntelligenceValidationError(ValueError):
    """Raised when untrusted intelligence input fails closed validation."""


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
        raise IntelligenceValidationError(f"value is not deterministic JSON: {exc}") from exc
    return f"{serialized}\n".encode("utf-8")


def _isoformat_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_timestamp(value: datetime | str, *, field: str) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = f"{normalized[:-1]}+00:00"
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise IntelligenceValidationError(f"{field} must be an ISO-8601 timestamp") from exc
    else:
        raise IntelligenceValidationError(f"{field} must be an ISO-8601 timestamp")

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise IntelligenceValidationError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _event_timestamp(event: Mapping[str, Any]) -> datetime:
    for field in ("occurred_at", "first_seen", "published_at"):
        if event.get(field):
            return _parse_timestamp(event[field], field=field)
    raise IntelligenceValidationError(
        f"event {event.get('event_id', '<missing>')} requires occurred_at, first_seen, or published_at"
    )


def _record_id(record: Mapping[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise IntelligenceValidationError(f"{field} must be a non-empty string")
    normalized = value.strip()
    if any(ord(character) < 32 for character in normalized):
        raise IntelligenceValidationError(f"{field} contains control characters")
    return normalized


def _string_list(value: Any, *, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise IntelligenceValidationError(f"{field} must be an array")

    result: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise IntelligenceValidationError(f"{field} entries must be non-empty strings")
        normalized = item.strip()
        if any(ord(character) < 32 for character in normalized):
            raise IntelligenceValidationError(f"{field} entries contain control characters")
        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return sorted(result, key=lambda item: (item.casefold(), item))


def _is_public_canonical(event: Mapping[str, Any]) -> bool:
    if event.get("public", True) is not True:
        return False
    status = str(event.get("status", "")).strip().upper()
    return status not in BLOCKED_PUBLIC_STATUSES


def _canonical_identity(event: Mapping[str, Any]) -> tuple[str, str]:
    event_id = _record_id(event, "event_id")
    canonical_id_raw = event.get("canonical_event_id", event_id)
    if not isinstance(canonical_id_raw, str) or not canonical_id_raw.strip():
        raise IntelligenceValidationError("canonical_event_id must be a non-empty string")
    return event_id, canonical_id_raw.strip()


def _revision_sort_key(event: Mapping[str, Any]) -> tuple[str, bytes]:
    timestamp = ""
    for field in ("updated_at", "last_verified_at", "occurred_at", "first_seen", "published_at"):
        if event.get(field):
            timestamp = _isoformat_utc(_parse_timestamp(event[field], field=field))
            break
    return timestamp, _stable_json_bytes(event)


def canonical_events(events: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return one deterministic, public canonical revision for every event.

    Alias records never supply public fields.  This prevents an untrusted alias
    observation from injecting topics or presentation data into a canonical event.
    """

    latest: dict[str, dict[str, Any]] = {}
    for raw_event in events:
        if not isinstance(raw_event, Mapping):
            raise IntelligenceValidationError("every event must be an object")
        event_id, canonical_id = _canonical_identity(raw_event)
        if event_id != canonical_id or not _is_public_canonical(raw_event):
            continue

        candidate = copy.deepcopy(dict(raw_event))
        candidate["event_id"] = event_id
        candidate["canonical_event_id"] = canonical_id
        for field in ("topics", "tags", "entities"):
            if field in candidate:
                candidate[field] = _string_list(candidate[field], field=field)

        current = latest.get(canonical_id)
        if current is None or _revision_sort_key(candidate) > _revision_sort_key(current):
            latest[canonical_id] = candidate

    return [latest[event_id] for event_id in sorted(latest)]


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _normalized_delta(current: int, previous: int) -> float:
    scale = max(current, previous, 1)
    return _clamp(0.5 + 0.5 * ((current - previous) / scale))


def _normalized_acceleration(current: int, previous: int, pre_previous: int) -> float:
    current_velocity = current - previous
    previous_velocity = previous - pre_previous
    scale = max(current, previous, pre_previous, 1)
    return _clamp(0.5 + 0.5 * ((current_velocity - previous_velocity) / scale))


def _event_first_seen(event: Mapping[str, Any]) -> datetime:
    if event.get("first_seen"):
        return _parse_timestamp(event["first_seen"], field="first_seen")
    return _event_timestamp(event)


def _source_weight(event: Mapping[str, Any]) -> float:
    raw = event.get("source_weight", 0.5)
    if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not math.isfinite(raw):
        raise IntelligenceValidationError("source_weight must be a finite number")
    if raw < 0 or raw > 1:
        raise IntelligenceValidationError("source_weight must be between 0 and 1")
    return float(raw)


def _observation_counts(
    events: Iterable[Mapping[str, Any]],
    canonical_by_id: Mapping[str, Mapping[str, Any]],
    *,
    start: datetime,
    end: datetime,
) -> dict[str, int]:
    counts: defaultdict[str, int] = defaultdict(int)
    for event in events:
        if not isinstance(event, Mapping) or event.get("public", True) is not True:
            continue
        _, canonical_id = _canonical_identity(event)
        canonical = canonical_by_id.get(canonical_id)
        if canonical is None:
            continue
        occurred_at = _event_timestamp(event)
        if not (start <= occurred_at <= end):
            continue
        for topic in _string_list(canonical.get("topics", []), field="topics"):
            counts[topic] += 1
    return dict(counts)


def calculate_trends(
    events: Iterable[Mapping[str, Any]],
    *,
    as_of: datetime | str,
    minimum_unique_events: int = MINIMUM_UNIQUE_EVENTS,
) -> dict[str, Any]:
    """Calculate deterministic ``trend_v1`` windows with inspectable components."""

    if minimum_unique_events < 1:
        raise IntelligenceValidationError("minimum_unique_events must be at least 1")
    cutoff = _parse_timestamp(as_of, field="as_of")
    raw_events = list(events)
    canonical = canonical_events(raw_events)
    canonical_by_id = {event["event_id"]: event for event in canonical}

    timestamped: list[tuple[dict[str, Any], datetime]] = []
    for event in canonical:
        occurred_at = _event_timestamp(event)
        if occurred_at <= cutoff:
            timestamped.append((event, occurred_at))

    result: dict[str, Any] = {
        "schema_version": TREND_SCHEMA_VERSION,
        "as_of": _isoformat_utc(cutoff),
        "realtime": False,
        "formula": TREND_FORMULA,
        "normalization": {
            "quantity_target_unique_events": QUANTITY_NORMALIZATION_TARGET,
            "growth_neutral": 0.5,
            "acceleration_neutral": 0.5,
            "component_range": [0, 1],
            "score_range": [0, 100],
        },
        "windows": {},
    }

    for window_name, duration in WINDOWS:
        current_start = cutoff - duration
        previous_start = current_start - duration
        pre_previous_start = previous_start - duration

        current_by_topic: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        previous_counts: defaultdict[str, int] = defaultdict(int)
        pre_previous_counts: defaultdict[str, int] = defaultdict(int)

        for event, occurred_at in timestamped:
            topics = _string_list(event.get("topics", []), field="topics")
            for topic in topics:
                if current_start <= occurred_at <= cutoff:
                    current_by_topic[topic].append(event)
                elif previous_start <= occurred_at < current_start:
                    previous_counts[topic] += 1
                elif pre_previous_start <= occurred_at < previous_start:
                    pre_previous_counts[topic] += 1

        observations = _observation_counts(
            raw_events,
            canonical_by_id,
            start=current_start,
            end=cutoff,
        )
        trends: list[dict[str, Any]] = []
        for topic in sorted(current_by_topic, key=lambda item: (item.casefold(), item)):
            topic_events = current_by_topic[topic]
            unique_count = len(topic_events)
            if unique_count < minimum_unique_events:
                continue

            observation_count = max(observations.get(topic, unique_count), unique_count)
            duplicate_rate = (observation_count - unique_count) / observation_count
            sources = {
                str(event.get("source", "unknown")).strip() or "unknown"
                for event in topic_events
            }
            components = {
                "quantity": round(
                    _clamp(unique_count / QUANTITY_NORMALIZATION_TARGET), 6
                ),
                "growth": round(
                    _normalized_delta(unique_count, previous_counts[topic]), 6
                ),
                "acceleration": round(
                    _normalized_acceleration(
                        unique_count,
                        previous_counts[topic],
                        pre_previous_counts[topic],
                    ),
                    6,
                ),
                "source_diversity": round(
                    _clamp(len(sources) / unique_count), 6
                ),
                "novelty": round(
                    sum(
                        1 for event in topic_events if _event_first_seen(event) >= current_start
                    )
                    / unique_count,
                    6,
                ),
                "source_weight": round(
                    sum(_source_weight(event) for event in topic_events) / unique_count,
                    6,
                ),
            }
            weighted = (
                0.25 * components["quantity"]
                + 0.25 * components["growth"]
                + 0.15 * components["acceleration"]
                + 0.15 * components["source_diversity"]
                + 0.10 * components["novelty"]
                + 0.10 * components["source_weight"]
            )
            trends.append(
                {
                    "topic": topic,
                    "score": round(100 * weighted * (1 - 0.5 * duplicate_rate), 6),
                    "unique_events": unique_count,
                    "observations": observation_count,
                    "unique_sources": len(sources),
                    "duplicate_rate": round(duplicate_rate, 6),
                    "components": components,
                    "event_ids": sorted(event["event_id"] for event in topic_events),
                }
            )

        trends.sort(key=lambda trend: (-trend["score"], trend["topic"].casefold(), trend["topic"]))
        result["windows"][window_name] = {
            "window": window_name,
            "data_as_of": _isoformat_utc(cutoff),
            "minimum_unique_events": minimum_unique_events,
            "trends": trends,
        }

    return result


def _validate_base_url(base_url: str) -> str:
    if not base_url:
        return ""
    if not isinstance(base_url, str):
        raise IntelligenceValidationError("base_url must be a string")
    normalized = base_url.strip().rstrip("/")
    parsed = urlsplit(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise IntelligenceValidationError("base_url must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise IntelligenceValidationError("base_url must not include credentials, query, or fragment")
    return normalized


def _sort_collection(
    records: Sequence[Mapping[str, Any]],
    *,
    identity_field: str,
) -> list[dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for raw_record in records:
        if not isinstance(raw_record, Mapping):
            raise IntelligenceValidationError("collection entries must be objects")
        record = copy.deepcopy(dict(raw_record))
        identity = _record_id(record, identity_field)
        if identity in result:
            raise IntelligenceValidationError(f"duplicate {identity_field}: {identity}")
        result[identity] = record
    return [result[identity] for identity in sorted(result)]


def _filter_graph(
    graph: Sequence[Mapping[str, Any]],
    canonical_ids: set[str],
) -> list[dict[str, Any]]:
    filtered: list[Mapping[str, Any]] = []
    for raw_edge in graph:
        if not isinstance(raw_edge, Mapping):
            raise IntelligenceValidationError("graph entries must be objects")
        edge = copy.deepcopy(dict(raw_edge))
        if "evidence_event_ids" in edge:
            evidence = [
                event_id
                for event_id in _string_list(
                    edge["evidence_event_ids"], field="evidence_event_ids"
                )
                if event_id in canonical_ids
            ]
            if not evidence:
                continue
            edge["evidence_event_ids"] = evidence
        filtered.append(edge)
    return _sort_collection(filtered, identity_field="edge_id")


def _validate_release_id(release_id: str) -> str:
    if not isinstance(release_id, str) or not RELEASE_ID_RE.fullmatch(release_id):
        raise IntelligenceValidationError(
            "release_id must be 1-128 safe letters, digits, dots, underscores, or hyphens"
        )
    return release_id


def _shard_payload(
    *,
    collection: str,
    release_id: str,
    items: Sequence[Mapping[str, Any]],
) -> bytes:
    return _stable_json_bytes(
        {
            "schema_version": API_SCHEMA_VERSION,
            "release_id": release_id,
            "collection": collection,
            "items": list(items),
        }
    )


def _make_shards(
    *,
    collection: str,
    release_id: str,
    items: Sequence[Mapping[str, Any]],
    max_items: int,
    max_bytes: int,
) -> list[bytes]:
    shards: list[bytes] = []
    current: list[Mapping[str, Any]] = []

    for item in items:
        candidate = [*current, item]
        candidate_body = _shard_payload(
            collection=collection,
            release_id=release_id,
            items=candidate,
        )
        if current and (len(candidate) > max_items or len(candidate_body) > max_bytes):
            shards.append(
                _shard_payload(
                    collection=collection,
                    release_id=release_id,
                    items=current,
                )
            )
            current = [item]
            single_body = _shard_payload(
                collection=collection,
                release_id=release_id,
                items=current,
            )
            if len(single_body) > max_bytes:
                raise IntelligenceValidationError(
                    f"one {collection} item exceeds max_shard_bytes={max_bytes}"
                )
        else:
            if len(candidate_body) > max_bytes:
                raise IntelligenceValidationError(
                    f"one {collection} item exceeds max_shard_bytes={max_bytes}"
                )
            current = candidate

    if current:
        shards.append(
            _shard_payload(
                collection=collection,
                release_id=release_id,
                items=current,
            )
        )
    return shards


def _write_atomic(path: Path, body: bytes, *, immutable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_bytes()
        if existing == body:
            return
        if immutable:
            raise IntelligenceValidationError(f"refusing to overwrite immutable path: {path}")

    file_descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(file_descriptor, 0o644)
        with os.fdopen(file_descriptor, "wb") as temporary_file:
            temporary_file.write(body)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def _file_reference(path: str, body: bytes, *, count: int | None = None) -> dict[str, Any]:
    reference: dict[str, Any] = {
        "path": path,
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
    }
    if count is not None:
        reference["count"] = count
    return reference


def _feed_metadata(*, base_url: str, release_id: str, as_of: datetime) -> dict[str, Any]:
    def absolute(path: str) -> str:
        return f"{base_url}{path}" if base_url else path

    return {
        "schema_version": API_SCHEMA_VERSION,
        "release_id": release_id,
        "data_as_of": _isoformat_utc(as_of),
        "realtime": False,
        "watchlist_scope": "local_browser_only",
        "feeds": [
            {
                "format": "rss",
                "media_type": "application/rss+xml",
                "url": absolute("/index.xml"),
            },
            {
                "format": "json_feed",
                "media_type": "application/feed+json",
                "url": absolute("/feed.json"),
            },
            {
                "format": "opml",
                "media_type": "text/x-opml",
                "url": absolute("/feeds.opml"),
            },
        ],
    }


def build_static_intelligence(
    *,
    output_dir: str | Path,
    events: Sequence[Mapping[str, Any]],
    entities: Sequence[Mapping[str, Any]] = (),
    graph: Sequence[Mapping[str, Any]] = (),
    as_of: datetime | str,
    release_id: str | None = None,
    base_url: str = "",
    max_items_per_shard: int = 500,
    max_shard_bytes: int = 1_048_576,
) -> dict[str, Any]:
    """Build deterministic content-addressed static API files.

    Release files are immutable: a caller cannot reuse a release id for different
    bytes.  The mutable root manifest is written last and acts as the atomic pointer
    to the fully materialized release.
    """

    if max_items_per_shard < 1:
        raise IntelligenceValidationError("max_items_per_shard must be at least 1")
    if max_shard_bytes < 128:
        raise IntelligenceValidationError("max_shard_bytes must be at least 128")
    cutoff = _parse_timestamp(as_of, field="as_of")
    normalized_base_url = _validate_base_url(base_url)
    canonical = canonical_events(events)
    canonical_ids = {event["event_id"] for event in canonical}
    normalized_entities = _sort_collection(entities, identity_field="entity_id")
    normalized_graph = _filter_graph(graph, canonical_ids)
    trends = calculate_trends(events, as_of=cutoff)

    content_identity = {
        "schema_version": API_SCHEMA_VERSION,
        "as_of": _isoformat_utc(cutoff),
        "base_url": normalized_base_url,
        "events": canonical,
        "entities": normalized_entities,
        "graph": normalized_graph,
        "trends": trends,
        "shard_policy": {
            "max_items_per_shard": max_items_per_shard,
            "max_shard_bytes": max_shard_bytes,
        },
    }
    content_identity_body = _stable_json_bytes(content_identity)
    content_identity_digest = hashlib.sha256(content_identity_body).hexdigest()
    normalized_release_id = _validate_release_id(
        release_id if release_id is not None else f"r-{content_identity_digest[:20]}"
    )
    root = Path(output_dir)
    release_prefix = f"api/v1/releases/{normalized_release_id}"
    public_release_prefix = f"/{release_prefix}"

    identity_body = _stable_json_bytes(
        {
            "schema_version": API_SCHEMA_VERSION,
            "release_id": normalized_release_id,
            "content_sha256": content_identity_digest,
        }
    )
    identity_relative_path = f"{release_prefix}/identity.json"
    # This preflight happens before any shard write.  Reusing an explicit release
    # id for different content therefore cannot leave stray files in that release.
    _write_atomic(root / identity_relative_path, identity_body, immutable=True)

    collections: dict[str, Any] = {}
    for collection_name, items in (
        ("events", canonical),
        ("entities", normalized_entities),
        ("graph", normalized_graph),
    ):
        shard_bodies = _make_shards(
            collection=collection_name,
            release_id=normalized_release_id,
            items=items,
            max_items=max_items_per_shard,
            max_bytes=max_shard_bytes,
        )
        shard_references: list[dict[str, Any]] = []
        offset = 0
        for body in shard_bodies:
            digest = hashlib.sha256(body).hexdigest()
            shard_name = f"{digest[:20]}.json"
            relative_path = f"{release_prefix}/{collection_name}/{shard_name}"
            public_path = f"/{relative_path}"
            payload = json.loads(body)
            count = len(payload["items"])
            _write_atomic(root / relative_path, body, immutable=True)
            reference = _file_reference(public_path, body, count=count)
            reference["offset"] = offset
            shard_references.append(reference)
            offset += count
        collections[collection_name] = {
            "count": len(items),
            "shards": shard_references,
        }

    trend_references: dict[str, dict[str, Any]] = {}
    for window_name, _ in WINDOWS:
        body = _stable_json_bytes(
            {
                "schema_version": TREND_SCHEMA_VERSION,
                "release_id": normalized_release_id,
                "as_of": trends["as_of"],
                "realtime": False,
                "formula": trends["formula"],
                "normalization": trends["normalization"],
                **trends["windows"][window_name],
            }
        )
        relative_path = f"{release_prefix}/trends/{window_name}.json"
        _write_atomic(root / relative_path, body, immutable=True)
        trend_references[window_name] = _file_reference(f"/{relative_path}", body)

    feeds = _feed_metadata(
        base_url=normalized_base_url,
        release_id=normalized_release_id,
        as_of=cutoff,
    )
    feeds_body = _stable_json_bytes(feeds)
    feeds_relative_path = f"{release_prefix}/feeds.json"
    _write_atomic(root / feeds_relative_path, feeds_body, immutable=True)

    release_manifest = {
        "schema_version": API_SCHEMA_VERSION,
        "release_id": normalized_release_id,
        "data_as_of": _isoformat_utc(cutoff),
        "realtime": False,
        "limits": {
            "max_items_per_shard": max_items_per_shard,
            "max_shard_bytes": max_shard_bytes,
        },
        "identity": _file_reference(f"/{identity_relative_path}", identity_body),
        "collections": collections,
        "trends": trend_references,
        "feeds": _file_reference(f"/{feeds_relative_path}", feeds_body),
    }
    release_manifest_body = _stable_json_bytes(release_manifest)
    release_manifest_relative_path = f"{release_prefix}/manifest.json"
    _write_atomic(
        root / release_manifest_relative_path,
        release_manifest_body,
        immutable=True,
    )

    root_manifest = {
        "schema_version": API_SCHEMA_VERSION,
        "active_release": normalized_release_id,
        "data_as_of": _isoformat_utc(cutoff),
        "realtime": False,
        "release_manifest": _file_reference(
            f"/{release_manifest_relative_path}", release_manifest_body
        ),
    }
    _write_atomic(root / "api/v1/manifest.json", _stable_json_bytes(root_manifest))

    return {
        "release_id": normalized_release_id,
        "root_manifest_path": "api/v1/manifest.json",
        "release_manifest_path": release_manifest_relative_path,
        "feeds_path": feeds_relative_path,
        "release_path": public_release_prefix,
    }


__all__ = [
    "API_SCHEMA_VERSION",
    "IntelligenceValidationError",
    "TREND_FORMULA",
    "TREND_SCHEMA_VERSION",
    "build_static_intelligence",
    "calculate_trends",
    "canonical_events",
]
