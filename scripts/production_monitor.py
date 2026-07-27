#!/usr/bin/env python3
"""监控生产标记与 main 收敛、证据刷新和事件时间。"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timedelta, timezone

try:
    from scripts.production_smoke import (
        ProductionSmokeError,
        validate_release_marker_payload,
        verify_production_sample as _verify_production_sample,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution path
    from production_smoke import (  # type: ignore[no-redef]
        ProductionSmokeError,
        validate_release_marker_payload,
        verify_production_sample as _verify_production_sample,
    )


class MonitoringError(RuntimeError):
    """生产状态超过明确的故障阈值。"""


_FULL_SHA = re.compile(r"[0-9a-f]{40}\Z")


def _utc(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise MonitoringError(f"invalid {field} timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise MonitoringError(f"{field} timestamp must be UTC")
    return parsed


def evaluate_production_state(
    marker: Mapping[str, object],
    *,
    main_sha: str,
    main_committed_at: str,
    refresh_as_of: str,
    data_as_of: str,
    now: datetime | None = None,
    live_is_main_ancestor: bool = True,
    max_divergence_hours: float = 3,
    max_stale_hours: float = 12,
) -> dict[str, object]:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None or current.utcoffset() != timedelta(0):
        raise MonitoringError("monitor clock must be UTC")
    try:
        checked_marker = validate_release_marker_payload(marker)
    except ProductionSmokeError as exc:
        raise MonitoringError("invalid production release marker") from exc
    live_sha = checked_marker["exact_sha"]
    assert isinstance(live_sha, str)
    if not _FULL_SHA.fullmatch(main_sha):
        raise MonitoringError("invalid main SHA")
    marker_data_as_of = str(marker.get("generated_at", ""))
    if data_as_of != marker_data_as_of:
        raise MonitoringError("production data clock does not match release marker")
    refresh_clock = _utc(refresh_as_of, "refresh")
    data_clock = _utc(data_as_of, "data")
    refresh_age = current - refresh_clock
    data_age = current - data_clock
    if refresh_age < timedelta(0):
        raise MonitoringError("production refresh clock is in the future")
    if data_age < timedelta(0):
        raise MonitoringError("production data clock is in the future")
    refresh_age_hours = refresh_age.total_seconds() / 3600
    data_age_hours = data_age.total_seconds() / 3600
    if refresh_age >= timedelta(hours=max_stale_hours):
        raise MonitoringError(
            "production content refresh is stale "
            f"(refresh_as_of={refresh_as_of}, "
            f"refresh_age_hours={refresh_age_hours:.3f}, "
            f"data_as_of={data_as_of}, "
            f"data_age_hours={data_age_hours:.3f}, "
            f"threshold_hours={max_stale_hours:g})"
        )
    if live_sha == main_sha:
        status = "healthy"
        divergence_hours = 0.0
    else:
        if not live_is_main_ancestor:
            raise MonitoringError("production SHA is not a main ancestor")
        main_time = _utc(main_committed_at, "main commit")
        divergence = current - main_time
        if divergence >= timedelta(hours=max_divergence_hours):
            raise MonitoringError("production/main divergence exceeded threshold")
        status = "converging"
        divergence_hours = max(0.0, divergence.total_seconds() / 3600)
    return {
        "status": status,
        "refresh_as_of": refresh_as_of,
        "refresh_age_hours": refresh_age_hours,
        "data_as_of": data_as_of,
        "data_age_hours": data_age_hours,
        # Preserve the old machine-readable key while changing its source from
        # event time to the successful evidence-refresh clock.
        "stale_hours": refresh_age_hours,
        "divergence_hours": divergence_hours,
    }


def verify_production_sample(
    base_url: str,
    marker: Mapping[str, object],
    *,
    fetch: Callable[[str], bytes] | None = None,
) -> dict[str, object]:
    """将 smoke 的安全取数函数用于轻量小时抽查，并统一监控错误边界。"""

    try:
        if fetch is None:
            return _verify_production_sample(base_url, marker)
        return _verify_production_sample(base_url, marker, fetch=fetch)
    except (KeyError, OSError, ProductionSmokeError) as exc:
        raise MonitoringError("production release sample is invalid") from exc


def _base_url_from_marker_url(marker_url: str) -> str:
    parts = urllib.parse.urlsplit(marker_url)
    if (
        parts.scheme != "https"
        or not parts.netloc
        or parts.username
        or parts.password
        or not parts.path.endswith("/ai_stack_release_v1.json")
    ):
        raise MonitoringError("production marker URL is invalid")
    directory = parts.path.removesuffix("ai_stack_release_v1.json")
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, directory, "", ""))


def _load_marker(url: str) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        headers={"Cache-Control": "no-cache", "User-Agent": "ai-stack-monitor/1"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read(128 * 1024 + 1)
        value = json.loads(body)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MonitoringError("production marker is unavailable") from exc
    if len(body) > 128 * 1024 or not isinstance(value, dict):
        raise MonitoringError("production marker is invalid")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--marker-url", required=True)
    parser.add_argument("--main-sha", required=True)
    parser.add_argument("--main-committed-at", required=True)
    parser.add_argument("--max-divergence-hours", type=float, default=3)
    parser.add_argument("--max-stale-hours", type=float, default=12)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        marker = _load_marker(args.marker_url)
        sample = verify_production_sample(
            _base_url_from_marker_url(args.marker_url),
            marker,
        )
        live_sha = marker.get("exact_sha")
        ancestor = False
        if isinstance(live_sha, str) and _FULL_SHA.fullmatch(live_sha):
            ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", live_sha, args.main_sha],
                check=False,
                capture_output=True,
            ).returncode == 0
        report = evaluate_production_state(
            marker,
            main_sha=args.main_sha,
            main_committed_at=args.main_committed_at,
            refresh_as_of=str(sample.get("refresh_as_of", "")),
            data_as_of=str(sample.get("data_as_of", "")),
            live_is_main_ancestor=ancestor,
            max_divergence_hours=args.max_divergence_hours,
            max_stale_hours=args.max_stale_hours,
        )
    except MonitoringError as exc:
        print(f"production-monitor: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
