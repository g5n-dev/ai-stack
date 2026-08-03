"""Detection rules for a broken release chain.

A cancelled run discards everything it generated, and GitHub reports a job
killed by timeout-minutes as cancelled — neither red nor green, notifying
nobody. Before this check the only signals were a stale release marker (12h)
or the publication heartbeat (26h).
"""

from __future__ import annotations

from typing import Any

import pytest

from scripts.check_release_runs import ReleaseRunError, evaluate_runs, summarize


def _run(conclusion: str, run_id: int = 1, status: str = "completed") -> dict[str, Any]:
    return {
        "id": run_id,
        "status": status,
        "conclusion": conclusion,
        "created_at": "2026-08-03T04:00:00Z",
        "event": "schedule",
        "html_url": f"https://github.com/g5n-dev/ai-stack/actions/runs/{run_id}",
    }


def test_a_single_failure_is_not_worth_waking_anyone() -> None:
    # One transient failure is normal; the next run usually recovers.
    report = evaluate_runs([_run("failure", 1), _run("success", 2)])

    assert report["status"] == "ok"
    assert report["consecutive_incomplete"] == 1


@pytest.mark.parametrize("conclusion", ["cancelled", "failure", "timed_out", "startup_failure"])
def test_two_consecutive_incomplete_runs_alert(conclusion: str) -> None:
    report = evaluate_runs([_run(conclusion, 1), _run(conclusion, 2), _run("success", 3)])

    assert report["status"] == "failing"
    assert report["consecutive_incomplete"] == 2


def test_cancelled_counts_because_that_is_how_a_timeout_appears() -> None:
    # The two runs that silently discarded generated posts were both 'cancelled'.
    report = evaluate_runs([_run("cancelled", 1), _run("cancelled", 2)])

    assert report["status"] == "failing"
    assert report["latest_conclusion"] == "cancelled"


def test_a_success_clears_the_streak() -> None:
    report = evaluate_runs([_run("success", 1), _run("cancelled", 2), _run("cancelled", 3)])

    assert report["status"] == "ok"
    assert report["consecutive_incomplete"] == 0


def test_in_progress_runs_do_not_count_either_way() -> None:
    runs = [_run("", 1, status="in_progress"), _run("cancelled", 2), _run("cancelled", 3)]

    report = evaluate_runs(runs)

    assert report["status"] == "failing"
    assert report["consecutive_incomplete"] == 2


def test_no_completed_run_is_an_error_not_a_healthy_default() -> None:
    # Reporting ok when history cannot be read is the pathology being fixed.
    with pytest.raises(ReleaseRunError):
        evaluate_runs([_run("", 1, status="in_progress")])


def test_summary_points_at_checkout_rather_than_tests() -> None:
    report = evaluate_runs([_run("cancelled", 1), _run("cancelled", 2)])

    text = summarize(report)

    assert "cancelled" in text
    assert "Checkout" in text
    assert "timeout-minutes" in text


def test_a_push_triggered_run_cannot_clear_a_stalled_schedule() -> None:
    """A push to main re-deploys without crawling; a bot push skips every job.

    Counting either would let a green run that never refreshed content mask a
    genuine stall in the scheduled chain.
    """

    runs = [
        {**_run("success", 1), "event": "push"},
        _run("cancelled", 2),
        _run("cancelled", 3),
    ]

    report = evaluate_runs(runs)

    assert report["status"] == "failing"
    assert report["consecutive_incomplete"] == 2


def test_only_scheduled_history_counts_as_history() -> None:
    with pytest.raises(ReleaseRunError):
        evaluate_runs([{**_run("success", 1), "event": "push"}])
