"""Grading rules for capacity gauges.

The outage this exists for happened because a ceiling had two states: fine, and
release fails. The risk in fixing that is the opposite failure — a report that
cries wolf until nobody reads it, which is what let the real incident run for
four days. These tests pin both edges.
"""

from __future__ import annotations

import pytest

from scripts.capacity_report import CapacityError, Gauge, build_report, summarize


def _gauge(used: int | None, limit: int = 100, **kwargs: object) -> Gauge:
    return Gauge(name="example", limit=limit, used=used, detail="d", **kwargs)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("used", "expected"),
    [(0, "ok"), (69, "ok"), (70, "warning"), (84, "warning"), (85, "critical"), (200, "critical")],
)
def test_growing_gauges_are_graded_before_they_fail(used: int, expected: str) -> None:
    assert _gauge(used).status(warning=0.70, critical=0.85) == expected


@pytest.mark.parametrize("used", [0, 85, 99, 100])
def test_structural_gauges_never_warn_on_proximity(used: int) -> None:
    # lineage_public_files is shard_count*2+1 — a constant. Warning at 85.7% of
    # its limit would light up permanently and train the reader to ignore the
    # entire report.
    assert _gauge(used, structural=True).status(warning=0.70, critical=0.85) == "ok"


def test_structural_gauges_still_catch_a_real_breach() -> None:
    # Doubling shard_count would genuinely exceed the file ceiling.
    assert _gauge(101, structural=True).status(warning=0.70, critical=0.85) == "critical"


def test_an_unmeasurable_gauge_is_never_reported_healthy() -> None:
    report = build_report([_gauge(None, required=False)])

    assert report["gauges"][0]["status"] == "unavailable"  # type: ignore[index]
    # A monitor that defaults to ok when its input is missing manufactures
    # confidence, which is worse than having no monitor at all.
    assert report["status"] == "unavailable"


def test_overall_status_takes_the_worst_gauge() -> None:
    report = build_report([_gauge(10), _gauge(75), _gauge(90)])

    assert report["status"] == "critical"


def test_healthy_gauges_report_ok() -> None:
    assert build_report([_gauge(10), _gauge(20)])["status"] == "ok"


def test_required_gauge_that_cannot_be_measured_raises(tmp_path) -> None:
    from scripts.capacity_report import collect_gauges

    # An empty tree has no lineage assets, which must fail loudly rather than
    # silently reporting a healthy zero.
    with pytest.raises((CapacityError, OSError, ValueError)):
        collect_gauges(tmp_path)


def test_summary_names_the_gauge_and_its_headroom() -> None:
    report = build_report([_gauge(90, limit=1000)])

    text = summarize(report)

    assert "example" in text
    assert "9.0%" in text
