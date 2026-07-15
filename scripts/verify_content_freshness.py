#!/usr/bin/env python3
"""Fail-closed freshness check for local and deployed tag-graph v2 indexes."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCAL_INDEX = ROOT / "blog" / "static" / "data" / "tag-graph" / "index.json"
MAX_LIVE_INDEX_BYTES = 2 * 1024 * 1024
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


class FreshnessError(ValueError):
    """Raised when an index cannot prove that its content is valid and fresh."""


def _aware_utc(value: datetime, *, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise FreshnessError(f"{field} must be timezone-aware")
    return value.astimezone(UTC)


def _parse_generated_at(value: object, *, source: str) -> datetime:
    if not isinstance(value, str) or not RFC3339_RE.fullmatch(value):
        raise FreshnessError(f"{source}: generated_at must be an aware RFC3339 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise FreshnessError(
            f"{source}: generated_at must be an aware RFC3339 timestamp"
        ) from exc
    return _aware_utc(parsed, field=f"{source}: generated_at")


def _positive_max_age(value: object) -> float:
    if isinstance(value, bool):
        raise FreshnessError("max_age_hours must be a positive finite number")
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise FreshnessError("max_age_hours must be a positive finite number") from exc
    if not math.isfinite(parsed) or parsed <= 0:
        raise FreshnessError("max_age_hours must be a positive finite number")
    return parsed


def validate_index(
    payload: object,
    *,
    source: str,
    now: datetime,
    max_age_hours: float,
) -> dict[str, object]:
    """Validate the v2 index contract and prove freshness relative to explicit time."""
    checked_now = _aware_utc(now, field="now")
    checked_max_age = _positive_max_age(max_age_hours)

    if not isinstance(payload, dict):
        raise FreshnessError(f"{source}: index must be a JSON object")
    if type(payload.get("version")) is not int or payload.get("version") != 2:
        raise FreshnessError(f"{source}: index version must be 2")

    stats = payload.get("stats")
    if not isinstance(stats, dict):
        raise FreshnessError(f"{source}: stats must be a JSON object")
    total_articles = stats.get("total_articles")
    if type(total_articles) is not int or total_articles <= 0:
        raise FreshnessError(f"{source}: stats.total_articles must be a positive integer")

    generated_at_text = payload.get("generated_at")
    generated_at = _parse_generated_at(generated_at_text, source=source)
    age_seconds = (checked_now - generated_at).total_seconds()
    if age_seconds < 0:
        raise FreshnessError(f"{source}: generated_at is in the future")

    age_hours = age_seconds / 3600
    if age_hours > checked_max_age:
        raise FreshnessError(
            f"{source}: stale index ({age_hours:.2f}h > {checked_max_age:.2f}h)"
        )

    return {
        "source": source,
        "status": "ok",
        "version": 2,
        "generated_at": generated_at_text,
        "age_hours": round(age_hours, 6),
        "total_articles": total_articles,
    }


def _decode_index(raw: bytes, *, source: str) -> dict[str, object]:
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FreshnessError(f"{source}: invalid JSON") from exc
    if not isinstance(payload, dict):
        raise FreshnessError(f"{source}: index must be a JSON object")
    return payload


def load_local_index(path: Path) -> dict[str, object]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FreshnessError(f"local: unable to read index: {exc}") from exc
    return _decode_index(raw, source="local")


def load_live_index(url: str) -> dict[str, object]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise FreshnessError("live: URL must use http or https")

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "User-Agent": "ai-stack-content-freshness/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read(MAX_LIVE_INDEX_BYTES + 1)
    except (OSError, TimeoutError, urllib.error.URLError) as exc:
        raise FreshnessError(f"live: network error: {exc}") from exc
    if len(raw) > MAX_LIVE_INDEX_BYTES:
        raise FreshnessError("live: index exceeds the 2 MiB safety limit")
    return _decode_index(raw, source="live")


def _error_check(source: str, exc: Exception) -> dict[str, str]:
    message = " ".join(str(exc).split()) or exc.__class__.__name__
    return {"source": source, "status": "error", "error": message}


def run_checks(
    *,
    local_index: Path,
    live_index_url: str | None,
    now: datetime,
    max_age_hours: float,
    local_loader: Callable[[Path], dict[str, object]] = load_local_index,
    live_loader: Callable[[str], dict[str, object]] = load_live_index,
) -> dict[str, object]:
    """Run local and optional live checks independently and collect all failures."""
    checks: list[dict[str, object]] = []

    try:
        checks.append(
            validate_index(
                local_loader(local_index),
                source="local",
                now=now,
                max_age_hours=max_age_hours,
            )
        )
    except Exception as exc:
        checks.append(_error_check("local", exc))

    if live_index_url:
        try:
            checks.append(
                validate_index(
                    live_loader(live_index_url),
                    source="live",
                    now=now,
                    max_age_hours=max_age_hours,
                )
            )
        except Exception as exc:
            checks.append(_error_check("live", exc))

    status = "ok" if checks and all(check.get("status") == "ok" for check in checks) else "error"
    return {"status": status, "checks": checks}


def append_github_summary(report: dict[str, object], path: Path) -> None:
    status = str(report.get("status") or "error")
    lines = [f"### Content freshness: {status}", ""]
    checks = report.get("checks")
    if isinstance(checks, list):
        for check in checks:
            if not isinstance(check, dict):
                continue
            source = str(check.get("source") or "unknown")
            check_status = str(check.get("status") or "error")
            detail = ""
            if check_status == "ok":
                detail = (
                    f" — {check.get('total_articles')} articles, "
                    f"age {check.get('age_hours')}h"
                )
            elif check.get("error"):
                detail = f" — {check['error']}"
            lines.append(f"- {source}: {check_status}{detail}")
    lines.append("")
    with path.open("a", encoding="utf-8") as summary:
        summary.write("\n".join(lines))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--local-index",
        type=Path,
        default=DEFAULT_LOCAL_INDEX,
        help="Local tag-graph index.json (default: repository v2 index).",
    )
    parser.add_argument(
        "--live-index-url",
        help="Optional deployed tag-graph index.json URL.",
    )
    parser.add_argument(
        "--max-age-hours",
        type=float,
        required=True,
        help="Maximum allowed age for each checked index.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None, *, now: datetime | None = None) -> int:
    args = parse_args(argv)
    checked_now = now if now is not None else datetime.now(UTC)
    report = run_checks(
        local_index=args.local_index,
        live_index_url=args.live_index_url,
        now=checked_now,
        max_age_hours=args.max_age_hours,
        live_loader=load_live_index,
    )

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        try:
            append_github_summary(report, Path(summary_path))
        except OSError as exc:
            checks = report.setdefault("checks", [])
            if isinstance(checks, list):
                checks.append(_error_check("summary", exc))
            report["status"] = "error"

    print(json.dumps(report, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    return 0 if report.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
