"""Threshold behaviour for the publication heartbeat.

The thresholds encode measured history (median 2.8h, p95 11.4h, max 23.6h over
the healthy 2026-07 period). These tests pin that calibration so a future edit
cannot quietly reintroduce an alert that fires during normal operation — which
is how alerts become noise and then get ignored.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from scripts.publish_heartbeat import (
    HeartbeatError,
    evaluate_publish_heartbeat,
    summarize,
)

NOW = datetime(2026, 8, 3, 12, 0, 0, tzinfo=UTC)


def _at(hours_ago: float) -> dict[str, object]:
    return evaluate_publish_heartbeat(NOW - timedelta(hours=hours_ago), now=NOW)


@pytest.mark.parametrize("hours", [0.0, 2.8, 5.8, 11.4])
def test_normal_publishing_cadence_never_alerts(hours: float) -> None:
    # Median, p90 and p95 of the healthy period must all stay silent.
    assert _at(hours)["status"] == "ok"


@pytest.mark.parametrize("hours", [12.0, 20.2, 23.6])
def test_slow_but_historically_observed_gaps_only_warn(hours: float) -> None:
    # The longest healthy gap on record was 23.6h; it must not page.
    assert _at(hours)["status"] == "warning"


@pytest.mark.parametrize("hours", [26.0, 48.0, 96.0])
def test_gaps_beyond_anything_healthy_are_critical(hours: float) -> None:
    assert _at(hours)["status"] == "critical"


def test_the_real_outage_would_have_been_caught_within_a_day() -> None:
    # The incident ran ~4 days; detection must not need anywhere near that.
    assert _at(26.0)["status"] == "critical"
    assert _at(96.0)["age_hours"] == 96.0


def test_future_timestamps_are_refused_rather_than_reported_healthy() -> None:
    with pytest.raises(HeartbeatError):
        evaluate_publish_heartbeat(NOW + timedelta(hours=1), now=NOW)


def test_inverted_thresholds_are_refused() -> None:
    with pytest.raises(HeartbeatError):
        evaluate_publish_heartbeat(
            NOW - timedelta(hours=1), now=NOW, warning_hours=30, critical_hours=10
        )


def test_summary_names_the_age_and_the_place_to_look() -> None:
    text = summarize(_at(96.0))

    assert "96.0 小时" in text
    assert "已停止产出新文章" in text
    assert "validate" in text
