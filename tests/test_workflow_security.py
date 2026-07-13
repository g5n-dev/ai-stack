from __future__ import annotations

from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
PINNED_ACTION = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")
FORBIDDEN_GIT = ("reset --hard", "pull --rebase", " rebase ", "git add -A", "--force")


def _workflow(name: str) -> tuple[dict[str, object], str]:
    path = WORKFLOWS / name
    text = path.read_text(encoding="utf-8")
    # BaseLoader preserves the YAML key `on` instead of treating it as YAML 1.1 bool.
    parsed = yaml.load(text, Loader=yaml.BaseLoader)
    assert isinstance(parsed, dict)
    return parsed, text


def _jobs(workflow: dict[str, object]) -> dict[str, dict[str, object]]:
    jobs = workflow.get("jobs")
    assert isinstance(jobs, dict)
    assert all(isinstance(job, dict) for job in jobs.values())
    return jobs  # type: ignore[return-value]


def _job_text(job: dict[str, object]) -> str:
    return yaml.safe_dump(job, sort_keys=True)


def _needs(job: dict[str, object]) -> list[str]:
    value = job.get("needs")
    return value if isinstance(value, list) else [value]  # type: ignore[list-item]


def test_every_remote_action_is_pinned_to_a_full_commit() -> None:
    violations: list[str] = []
    for path in sorted(WORKFLOWS.glob("*.yml")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = re.search(r"\buses:\s*([^\s#]+)", line)
            if not match:
                continue
            action = match.group(1)
            if action.startswith("./") or PINNED_ACTION.fullmatch(action):
                continue
            violations.append(f"{path.name}:{line_number}:{action}")

    assert violations == []


def test_pr_ci_keeps_branch_update_contract_and_has_no_secrets() -> None:
    workflow, text = _workflow("ci.yml")
    triggers = workflow["on"]
    assert isinstance(triggers, dict)
    assert "pull_request" in triggers
    pull_request = triggers["pull_request"]
    assert isinstance(pull_request, dict)
    assert pull_request["branches"] == ["main"]
    assert "workflow_dispatch" in triggers
    assert workflow["permissions"] == {"contents": "read"}
    assert "${{ secrets." not in text
    assert "cancel-in-progress: true" in text

    for required in (
        "uv sync --frozen",
        "ruff check",
        "mypy",
        "pytest",
        "pip-audit",
        "npm ci",
        "npm audit",
        "npm test",
        "hugo",
        "validate_public_content",
    ):
        assert required in text


def test_deploy_preserves_public_triggers_but_uses_one_explicit_dag() -> None:
    workflow, text = _workflow("deploy.yml")
    assert workflow["name"] == "Build and Deploy"
    triggers = workflow["on"]
    assert isinstance(triggers, dict)
    assert "schedule" in triggers
    assert "workflow_dispatch" in triggers
    push = triggers["push"]
    assert isinstance(push, dict)
    assert push["branches"] == ["main"]
    assert workflow["permissions"] == {"contents": "read"}
    assert all(forbidden not in text for forbidden in FORBIDDEN_GIT)

    jobs = _jobs(workflow)
    required_jobs = (
        "crawl",
        "validate_discovery",
        "persist_discovery",
        "reserve_budget",
        "generate",
        "validate_result",
        "persist_result",
        "build",
        "deploy",
        "health",
        "publish",
        "persist_receipt",
    )
    assert tuple(jobs) == required_jobs
    assert "crawl" in _needs(jobs["validate_discovery"])
    assert "validate_discovery" in _needs(jobs["persist_discovery"])
    assert "persist_discovery" in _needs(jobs["reserve_budget"])
    assert "reserve_budget" in _needs(jobs["generate"])
    assert "generate" in _needs(jobs["validate_result"])
    assert "validate_result" in _needs(jobs["persist_result"])
    assert "persist_result" in _needs(jobs["build"])
    assert "build" in _needs(jobs["deploy"])
    assert "deploy" in _needs(jobs["health"])
    assert "health" in _needs(jobs["publish"])
    assert "publish" in _needs(jobs["persist_receipt"])


def test_deploy_jobs_enforce_credential_separation_and_revalidate_artifacts() -> None:
    workflow, text = _workflow("deploy.yml")
    jobs = _jobs(workflow)
    generate = _job_text(jobs["generate"])
    content_writer = _job_text(jobs["persist_result"])
    publisher = _job_text(jobs["publish"])
    receipt_writer = _job_text(jobs["persist_receipt"])

    assert "ANTHROPIC_AUTH_TOKEN" in generate
    assert jobs["generate"]["permissions"] == {"contents": "read"}
    assert jobs["persist_result"]["permissions"] == {"contents": "write"}
    assert "${{ secrets." not in content_writer
    assert jobs["publish"]["permissions"] == {"contents": "read"}
    assert jobs["publish"]["environment"] == "production-publish"
    assert "${{ secrets." in publisher
    assert jobs["persist_receipt"]["permissions"] == {"contents": "write"}
    assert "${{ secrets." not in receipt_writer

    for job_name in (
        "validate_discovery",
        "persist_discovery",
        "validate_result",
        "persist_result",
        "publish",
        "persist_receipt",
    ):
        job = _job_text(jobs[job_name])
        assert "actions/download-artifact" in job
        assert "artifact_guard.py" in job
    assert "git_cas_writer.py" in text
    assert "release_guard.py" in _job_text(jobs["deploy"])


def test_delete_workflow_is_break_glass_dry_run_and_bounded() -> None:
    workflow, text = _workflow("delete-post.yml")
    assert all(forbidden not in text for forbidden in FORBIDDEN_GIT)
    assert "ANTHROPIC_AUTH_TOKEN" not in text
    assert "scan" not in text.casefold()
    trigger = workflow["on"]
    assert isinstance(trigger, dict)
    dispatch = trigger["workflow_dispatch"]
    assert isinstance(dispatch, dict)
    inputs = dispatch["inputs"]
    assert isinstance(inputs, dict)
    assert inputs["dry_run"]["default"] == "true"  # type: ignore[index]
    for required in ("expected_source_sha", "backup_id", "max_changes"):
        assert required in inputs

    jobs = _jobs(workflow)
    deletion = jobs["delete"]
    assert deletion["environment"] == "data-deletion"
    assert deletion["permissions"] == {"contents": "write"}
    assert "--dry-run" in text
    assert "--expected-source-sha" in text
    assert "--backup-id" in text
    assert "--max-changes" in text


def test_monitoring_is_read_only_and_does_not_claim_fake_metrics() -> None:
    workflow, text = _workflow("monitoring.yml")
    assert workflow["permissions"] == {"contents": "read"}
    assert "analytics_data.json" not in text
    assert "engagement_data.json" not in text
    assert "Total Token" not in text
