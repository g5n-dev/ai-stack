"""Wiring invariants for the monitoring job's alert delivery.

Run 30798868809 detected a real outage — the publication heartbeat correctly
exited 1 after 101 hours without a new post — and told nobody. GitHub's default
shell already sets -e, so the non-zero exit aborted the step before
`exit_code` reached $GITHUB_OUTPUT, and the delivery step's
`steps.<id>.outputs.exit_code != ''` guard was therefore false. The alert was
skipped.

That is exactly the failure this monitoring exists to prevent, so it is pinned
here rather than left to review.
"""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "monitoring.yml"


def _steps() -> list[dict]:
    document = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return document["jobs"]["verify-production-state"]["steps"]


def test_every_measurement_disables_errexit_before_capturing_its_code() -> None:
    for step in _steps():
        run = str(step.get("run") or "")
        if "GITHUB_OUTPUT" not in run or "exit_code" not in run:
            continue
        assert "set +e" in run, (
            f"{step.get('name')} records an exit code, but GitHub's default shell "
            "sets -e; without 'set +e' the step aborts before writing the output "
            "and its alert is skipped"
        )


def test_every_delivery_step_runs_even_after_its_measurement_fails() -> None:
    for step in _steps():
        name = str(step.get("name") or "")
        if not name.startswith("Deliver"):
            continue
        condition = str(step.get("if") or "")
        assert condition.startswith("always()"), (
            f"{name} must run after a failed measurement, otherwise a detected "
            "outage produces no notification"
        )


def test_checks_do_not_block_one_another() -> None:
    # A failing heartbeat previously skipped the release-state and capacity
    # checks entirely, hiding whatever else was wrong.
    ids = {"release_state", "release_runs", "capacity"}
    for step in _steps():
        if step.get("id") in ids:
            assert str(step.get("if") or "").startswith("always()"), (
                f"{step.get('name')} must not be skipped because an earlier check failed"
            )


def test_the_job_still_reports_unhealthy_in_its_own_colour() -> None:
    gate = [s for s in _steps() if "Fail the job" in str(s.get("name") or "")]
    assert gate, "the job must fail on its own when production is unhealthy"
    run = str(gate[0]["run"])
    # A broken alert channel must not be able to make an outage look healthy.
    for signal in ("heartbeat", "release_state", "release_runs", "capacity"):
        assert signal in run
