#!/usr/bin/env python3
"""Fail closed when deployed STACK trend assets are stale or hash-inconsistent."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath


INDEX_SCHEMA = "stack_trends_index_v1"
WINDOW_SCHEMA = "stack_trends_window_v1"
TOPIC_SCHEMA = "stack_trends_topic_v1"
EXPECTED_WINDOWS = frozenset({"24h", "7d", "30d"})
INDEX_LIMIT_BYTES = 64 * 1024
ASSET_LIMIT_BYTES = 128 * 1024
TOTAL_LIMIT_BYTES = 2 * 1024 * 1024
MAX_ASSET_COUNT = 100
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class TrendMonitoringError(ValueError):
    """Raised when production cannot prove trend release integrity."""


Loader = Callable[[str, int], bytes]


def _positive_hours(value: object) -> float:
    if isinstance(value, bool):
        raise TrendMonitoringError("max_age_hours must be a positive finite number")
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise TrendMonitoringError(
            "max_age_hours must be a positive finite number"
        ) from exc
    if not math.isfinite(parsed) or parsed <= 0:
        raise TrendMonitoringError("max_age_hours must be a positive finite number")
    return parsed


def _aware_utc(value: datetime, *, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise TrendMonitoringError(f"{field} must be timezone-aware")
    return value.astimezone(UTC)


def _timestamp(value: object, *, field: str) -> datetime:
    if not isinstance(value, str) or not RFC3339_RE.fullmatch(value):
        raise TrendMonitoringError(f"{field} must be an aware RFC3339 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise TrendMonitoringError(
            f"{field} must be an aware RFC3339 timestamp"
        ) from exc
    return _aware_utc(parsed, field=field)


def _decode_json(raw: bytes, *, source: str) -> dict[str, object]:
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TrendMonitoringError(f"{source}: invalid JSON") from exc
    if not isinstance(payload, dict):
        raise TrendMonitoringError(f"{source}: JSON root must be an object")
    return payload


def load_url(url: str, max_bytes: int) -> bytes:
    """Read a bounded JSON asset without permitting redirect-based origin changes."""
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise TrendMonitoringError("live URL must use http or https")
    if type(max_bytes) is not int or max_bytes <= 0:
        raise TrendMonitoringError("live size limit must be a positive integer")

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "User-Agent": "ai-stack-trend-monitor/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            final_url = response.geturl()
            if final_url != url:
                raise TrendMonitoringError("live redirect is not permitted")
            raw = response.read(max_bytes + 1)
    except TrendMonitoringError:
        raise
    except (OSError, TimeoutError, urllib.error.URLError) as exc:
        raise TrendMonitoringError("live network error") from exc
    if len(raw) > max_bytes:
        raise TrendMonitoringError("live asset exceeds its size limit")
    return raw


def _safe_ref_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise TrendMonitoringError("asset path must be a non-empty string")
    if "%" in value or "\\" in value or "?" in value or "#" in value:
        raise TrendMonitoringError("asset path contains unsafe characters")
    parsed = urllib.parse.urlsplit(value)
    path = PurePosixPath(value)
    if (
        parsed.scheme
        or parsed.netloc
        or value.startswith("/")
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.suffix != ".json"
    ):
        raise TrendMonitoringError("asset path must be a safe relative JSON path")
    return value


def _mapping(value: object, *, field: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TrendMonitoringError(f"{field} must be an object")
    return value


def _array(value: object, *, field: str) -> list[object]:
    if not isinstance(value, list):
        raise TrendMonitoringError(f"{field} must be an array")
    return value


def _count(value: object, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TrendMonitoringError(f"{field} must be a non-negative integer")
    return value


def _validated_refs(index: dict[str, object]) -> list[dict[str, object]]:
    windows = index.get("windows")
    topics = index.get("topics")
    if not isinstance(windows, dict) or set(windows) != EXPECTED_WINDOWS:
        raise TrendMonitoringError("index window identities are invalid")
    if not isinstance(topics, dict):
        raise TrendMonitoringError("index topics must contain asset references")

    refs: list[dict[str, object]] = []
    for identity, reference in windows.items():
        if not isinstance(reference, dict):
            raise TrendMonitoringError("window reference must be an object")
        refs.append({**reference, "kind": "window", "identity": identity})
    for identity, reference in topics.items():
        if not isinstance(reference, dict):
            raise TrendMonitoringError("topic reference must be an object")
        refs.append({**reference, "kind": "topic", "identity": identity})
    if not refs:
        raise TrendMonitoringError("index contains no asset references")
    if len(refs) > MAX_ASSET_COUNT:
        raise TrendMonitoringError("index exceeds the asset count limit")

    validated: list[dict[str, object]] = []
    paths: set[str] = set()
    total_bytes = 0
    for ref in refs:
        path = _safe_ref_path(ref.get("path"))
        kind = ref.get("kind")
        expected_prefix = "windows/" if kind == "window" else "topics/"
        if not path.startswith(expected_prefix):
            raise TrendMonitoringError("asset path does not match reference kind")
        digest = ref.get("sha256")
        size = ref.get("bytes")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise TrendMonitoringError(f"asset hash is invalid: {path}")
        if type(size) is not int or size <= 0 or size > ASSET_LIMIT_BYTES:
            raise TrendMonitoringError(f"asset size is invalid: {path}")
        if path in paths:
            raise TrendMonitoringError(f"duplicate asset path: {path}")
        paths.add(path)
        total_bytes += size
        validated.append(
            {
                "path": path,
                "sha256": digest,
                "bytes": size,
                "kind": kind,
                "identity": ref.get("identity"),
            }
        )
    if total_bytes > TOTAL_LIMIT_BYTES:
        raise TrendMonitoringError("trend assets exceed the total size limit")
    return sorted(validated, key=lambda item: str(item["path"]))


def _topic_identity(
    payload: dict[str, object],
    *,
    expected_id: str,
    location: str,
) -> None:
    topic = payload.get("topic")
    if not isinstance(topic, str) or not topic or f"tag:{topic}" != expected_id:
        raise TrendMonitoringError(f"topic identity mismatch: {location}")
    if payload.get("id") != expected_id or payload.get("graph_node_id") != expected_id:
        raise TrendMonitoringError(f"topic identity mismatch: {location}")


def _verify_release_semantics(
    index: dict[str, object],
    *,
    assets: dict[str, dict[str, object]],
) -> None:
    data_as_of = index.get("data_as_of")
    windows = _mapping(index.get("windows"), field="index windows")
    topics = _mapping(index.get("topics"), field="index topics")
    if index.get("default_window") not in windows:
        raise TrendMonitoringError("index default_window must reference a window")
    stats = _mapping(index.get("stats"), field="index stats")
    stats_windows = _mapping(stats.get("windows"), field="index stats.windows")
    if set(stats_windows) != EXPECTED_WINDOWS:
        raise TrendMonitoringError("index stats.windows identity mismatch")
    if _count(stats.get("topic_count"), field="index stats.topic_count") != len(topics):
        raise TrendMonitoringError("index topic_count mismatch")

    topic_paths: dict[str, str] = {}
    for topic_id, raw_reference in sorted(topics.items()):
        reference = _mapping(raw_reference, field="topic reference")
        path = _safe_ref_path(reference.get("path"))
        payload = assets.get(path)
        if payload is None or payload.get("schema_version") != TOPIC_SCHEMA:
            raise TrendMonitoringError(f"topic schema mismatch: {path}")
        _topic_identity(payload, expected_id=topic_id, location=path)
        if payload.get("data_as_of") != data_as_of:
            raise TrendMonitoringError(f"topic data_as_of mismatch: {path}")
        topic_paths[topic_id] = path

    topics_seen: set[str] = set()
    for window_name, raw_reference in sorted(windows.items()):
        reference = _mapping(raw_reference, field="window reference")
        path = _safe_ref_path(reference.get("path"))
        payload = assets.get(path)
        if payload is None or payload.get("schema_version") != WINDOW_SCHEMA:
            raise TrendMonitoringError(f"window schema mismatch: {path}")
        if payload.get("window") != window_name:
            raise TrendMonitoringError(f"window identity mismatch: {path}")
        if payload.get("data_as_of") != data_as_of:
            raise TrendMonitoringError(f"window data_as_of mismatch: {path}")
        trends = _array(payload.get("trends"), field="window trends")
        expected_count = len(trends)
        reference_count = _count(
            reference.get("trend_count"), field="window reference trend_count"
        )
        stats_count = _count(
            _mapping(stats_windows.get(window_name), field="window stats").get(
                "trend_count"
            ),
            field="window stats trend_count",
        )
        if reference_count != expected_count or stats_count != expected_count:
            raise TrendMonitoringError(f"window trend_count mismatch: {path}")
        window_topics: set[str] = set()
        for raw_trend in trends:
            trend = _mapping(raw_trend, field="window trend")
            trend_id = trend.get("id")
            if not isinstance(trend_id, str):
                raise TrendMonitoringError(f"trend topic identity mismatch: {path}")
            _topic_identity(trend, expected_id=trend_id, location=path)
            if trend_id in window_topics:
                raise TrendMonitoringError(f"duplicate trend topic: {path}")
            window_topics.add(trend_id)
            expected_detail = topic_paths.get(trend_id)
            if expected_detail is None:
                raise TrendMonitoringError(f"trend topic reference missing: {path}")
            if trend.get("detail_path") != expected_detail:
                raise TrendMonitoringError(f"trend detail_path mismatch: {path}")
        topics_seen.update(window_topics)
    if topics_seen != set(topic_paths):
        raise TrendMonitoringError("index topic references do not match window trends")


def _asset_url(index_url: str, path: str) -> str:
    parsed_index = urllib.parse.urlsplit(index_url)
    base_path = parsed_index.path.rsplit("/", 1)[0] + "/"
    base_url = urllib.parse.urlunsplit(
        (parsed_index.scheme, parsed_index.netloc, base_path, "", "")
    )
    target = urllib.parse.urljoin(base_url, path)
    parsed_target = urllib.parse.urlsplit(target)
    if (
        parsed_target.scheme != parsed_index.scheme
        or parsed_target.netloc != parsed_index.netloc
        or not parsed_target.path.startswith(base_path)
    ):
        raise TrendMonitoringError("asset path escaped the trend release root")
    return target


def verify_live_release(
    index_url: str,
    *,
    now: datetime,
    max_age_hours: float,
    loader: Loader = load_url,
) -> dict[str, object]:
    """Verify live index freshness plus every referenced asset byte and hash."""
    checked_now = _aware_utc(now, field="now")
    checked_max_age = _positive_hours(max_age_hours)
    index_raw = loader(index_url, INDEX_LIMIT_BYTES)
    index = _decode_json(index_raw, source="live index")
    if index.get("schema_version") != INDEX_SCHEMA:
        raise TrendMonitoringError(f"live index schema must be {INDEX_SCHEMA}")

    generated_at = _timestamp(index.get("generated_at"), field="generated_at")
    data_as_of = _timestamp(index.get("data_as_of"), field="data_as_of")
    for field, timestamp in (
        ("generated_at", generated_at),
        ("data_as_of", data_as_of),
    ):
        age_hours = (checked_now - timestamp).total_seconds() / 3600
        if age_hours < 0:
            raise TrendMonitoringError(f"{field} is in the future")
        if age_hours > checked_max_age:
            raise TrendMonitoringError(
                f"{field} is stale ({age_hours:.2f}h > {checked_max_age:.2f}h)"
            )
    if index.get("generated_at") != index.get("data_as_of"):
        raise TrendMonitoringError(
            "generated_at must equal data_as_of for deterministic releases"
        )

    refs = _validated_refs(index)
    verified_bytes = 0
    manifest = hashlib.sha256()
    decoded_assets: dict[str, dict[str, object]] = {}
    for ref in refs:
        path = str(ref["path"])
        expected_size = int(ref["bytes"])
        expected_hash = str(ref["sha256"])
        raw = loader(_asset_url(index_url, path), expected_size)
        if len(raw) != expected_size:
            raise TrendMonitoringError(f"asset size mismatch: {path}")
        actual_hash = hashlib.sha256(raw).hexdigest()
        if actual_hash != expected_hash:
            raise TrendMonitoringError(f"asset hash mismatch: {path}")
        decoded_assets[path] = _decode_json(raw, source=f"live asset {path}")
        verified_bytes += len(raw)
        manifest.update(f"{path}\0{expected_size}\0{expected_hash}\n".encode("utf-8"))

    _verify_release_semantics(index, assets=decoded_assets)

    data_age = (checked_now - data_as_of).total_seconds() / 3600
    return {
        "status": "ok",
        "schema_version": INDEX_SCHEMA,
        "generated_at": index["generated_at"],
        "data_as_of": index["data_as_of"],
        "age_hours": round(data_age, 6),
        "asset_count": len(refs),
        "verified_bytes": verified_bytes,
        "index_sha256": hashlib.sha256(index_raw).hexdigest(),
        "asset_manifest_sha256": manifest.hexdigest(),
    }


def _append_summary(report: dict[str, object], path: Path) -> None:
    status = str(report.get("status") or "error")
    lines = [f"### STACK trend freshness: {status}", ""]
    if status == "ok":
        lines.append(
            "- live: ok"
            f" — {report.get('asset_count')} assets, age {report.get('age_hours')}h"
        )
    else:
        lines.append(f"- live: error — {report.get('error') or 'validation failed'}")
    lines.append("")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live-index-url", required=True)
    parser.add_argument("--max-age-hours", type=float, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None, *, now: datetime | None = None) -> int:
    args = parse_args(argv)
    checked_now = now if now is not None else datetime.now(UTC)
    try:
        report = verify_live_release(
            args.live_index_url,
            now=checked_now,
            max_age_hours=args.max_age_hours,
        )
        status = 0
    except Exception as exc:
        message = " ".join(str(exc).split()) or exc.__class__.__name__
        report = {"status": "error", "error": message}
        status = 1

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        try:
            _append_summary(report, Path(summary_path))
        except OSError:
            report = {"status": "error", "error": "unable to write job summary"}
            status = 1
    print(json.dumps(report, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
