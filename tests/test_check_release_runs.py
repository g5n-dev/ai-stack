"""Detection rules for a broken release chain.

A cancelled run discards everything it generated, and GitHub reports a job
killed by timeout-minutes as cancelled — neither red nor green, notifying
nobody. Before this check the only signals were a stale release marker (12h)
or the publication heartbeat (26h).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from scripts.check_release_runs import (
    ReleaseRunError,
    evaluate_runs,
    fetch_first_failure,
    main,
    summarize,
)


class _FakeApi:
    """Minimal GitHubApi double; a wrong endpoint shape fails the test loudly."""

    def __init__(self, runs: object, jobs: object | None = None) -> None:
        self.runs = runs
        self.jobs = jobs
        self.endpoints: list[str] = []

    def request(self, method: str, endpoint: str) -> object | None:
        assert method == "GET"
        self.endpoints.append(endpoint)
        if "/jobs?" in endpoint:
            return self.jobs
        return self.runs


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


def test_first_failure_names_the_step_that_actually_failed() -> None:
    """The 2026-10-05 outage was in refresh, but alerts kept naming validate."""

    api = _FakeApi(
        runs={},
        jobs={
            "jobs": [
                {
                    "name": "refresh",
                    "conclusion": "failure",
                    "steps": [
                        {"name": "Set up Python", "conclusion": "success"},
                        {"name": "Install crawler browser", "conclusion": "failure"},
                        {"name": "Refresh Posts", "conclusion": "skipped"},
                    ],
                },
                {"name": "validate", "conclusion": "skipped", "steps": []},
            ]
        },
    )

    failure = fetch_first_failure(api, repository="g5n-dev/ai-stack", run_id=41784410985)

    assert failure == {
        "job": "refresh",
        "step": "Install crawler browser",
        "conclusion": "failure",
    }
    assert api.endpoints == [
        "/repos/g5n-dev/ai-stack/actions/runs/41784410985/jobs?per_page=100"
    ]


def test_first_failure_falls_back_to_the_job_for_a_runner_level_failure() -> None:
    api = _FakeApi(
        runs={},
        jobs={
            "jobs": [
                {"name": "refresh", "conclusion": "failure", "steps": []},
            ]
        },
    )

    failure = fetch_first_failure(api, repository="g5n-dev/ai-stack", run_id=1)

    assert failure is not None
    assert failure["job"] == "refresh"
    assert "runner-level" in failure["step"]


def test_first_failure_returns_none_when_nothing_failed() -> None:
    api = _FakeApi(
        runs={},
        jobs={"jobs": [{"name": "refresh", "conclusion": "success", "steps": []}]},
    )

    assert fetch_first_failure(api, repository="g5n-dev/ai-stack", run_id=1) is None


@pytest.mark.parametrize("bad_id", [None, 0, -1, True, "../../secrets", 1.5])
def test_first_failure_rejects_unsafe_run_ids(bad_id: object) -> None:
    api = _FakeApi(runs={}, jobs={"jobs": []})

    with pytest.raises(ReleaseRunError):
        fetch_first_failure(api, repository="g5n-dev/ai-stack", run_id=bad_id)


def test_first_failure_rejects_an_unreadable_jobs_payload() -> None:
    api = _FakeApi(runs={}, jobs={"jobs": "not-a-list"})

    with pytest.raises(ReleaseRunError):
        fetch_first_failure(api, repository="g5n-dev/ai-stack", run_id=1)


def test_alert_carries_the_exact_failed_step(tmp_path: Path) -> None:
    runs = {"workflow_runs": [_run("failure", 1), _run("failure", 2)]}
    jobs = {
        "jobs": [
            {
                "name": "refresh",
                "conclusion": "failure",
                "steps": [{"name": "Install crawler browser", "conclusion": "failure"}],
            }
        ]
    }
    api = _FakeApi(runs=runs, jobs=jobs)
    summary = tmp_path / "release_runs.md"

    code = main(
        [
            "--repository",
            "g5n-dev/ai-stack",
            "--summary-output",
            str(summary),
        ],
        api=api,
    )

    assert code == 1
    text = summary.read_text(encoding="utf-8")
    assert "Install crawler browser" in text
    assert "`refresh` →" in text
    assert "不要预判断为 `validate`" in text


def test_a_broken_diagnostic_never_masks_a_detected_outage(tmp_path: Path) -> None:
    api = _FakeApi(
        runs={"workflow_runs": [_run("failure", 1), _run("failure", 2)]},
        jobs={"jobs": "unreadable"},
    )
    summary = tmp_path / "release_runs.md"

    code = main(
        ["--repository", "g5n-dev/ai-stack", "--summary-output", str(summary)],
        api=api,
    )

    assert code == 1
    text = summary.read_text(encoding="utf-8")
    assert "发布链已经中断" in text
    assert "首个失败步骤定位失败" in text


def test_summary_reports_the_first_failed_step_when_available() -> None:
    report = evaluate_runs([_run("failure", 1), _run("failure", 2)])
    report["first_failure"] = {
        "job": "refresh",
        "step": "Install crawler browser",
        "conclusion": "failure",
    }

    text = summarize(report)

    assert "首个失败步骤" in text
    assert "`refresh` → `Install crawler browser`" in text
