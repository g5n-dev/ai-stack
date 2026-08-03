#!/usr/bin/env python3
"""Merge a validated automation commit through a SHA-locked protected PR."""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from typing import Protocol, cast
from urllib.parse import quote


API_VERSION = "2026-03-10"
_REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
_AUTOMATION_BRANCH = re.compile(r"automation/(?:data|delete)-[0-9]+-[0-9]+\Z")
_SHA = re.compile(r"[0-9a-f]{40}\Z")
_TRUSTED_ACTIONS_APP_ID = 15368
_TEST_CHECK = "PR Test Suite"
_REQUIRED_CHECK = "Unit Tests"
_FAILED_TEST_CONCLUSIONS = frozenset(
    {
        "action_required",
        "cancelled",
        "failure",
        "neutral",
        "skipped",
        "stale",
        "startup_failure",
        "timed_out",
    }
)


class ProtectedBranchMergeError(RuntimeError):
    """Raised before an unsafe dispatch, PR creation, or merge can continue."""


class GitHubApi(Protocol):
    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
    ) -> object | None: ...


class GhCliApi:
    """Minimal REST adapter that keeps the token and response errors out of logs."""

    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
    ) -> object | None:
        normalized = method.upper()
        if normalized not in {"GET", "POST", "PUT"}:
            raise ProtectedBranchMergeError("unsupported GitHub API method")
        if not endpoint.startswith("/repos/") or any(ord(char) < 32 for char in endpoint):
            raise ProtectedBranchMergeError("unsafe GitHub API endpoint")
        command = [
            "gh",
            "api",
            "--method",
            normalized,
            "--header",
            "Accept: application/vnd.github+json",
            "--header",
            f"X-GitHub-Api-Version: {API_VERSION}",
            endpoint,
        ]
        encoded: str | None = None
        if body is not None:
            command.extend(["--input", "-"])
            encoded = json.dumps(body, sort_keys=True, separators=(",", ":"))
        try:
            result = subprocess.run(
                command,
                input=encoded,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ProtectedBranchMergeError("GitHub API transport failed") from exc
        if result.returncode != 0:
            status = re.search(r"\bHTTP ([0-9]{3})\b", result.stderr or "")
            suffix = f" (HTTP {status.group(1)})" if status else ""
            raise ProtectedBranchMergeError(f"GitHub API request failed{suffix}")
        if not result.stdout.strip():
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise ProtectedBranchMergeError("GitHub API returned invalid JSON") from exc


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ProtectedBranchMergeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _array(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise ProtectedBranchMergeError(f"{label} must be an array")
    return cast(list[object], value)


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ProtectedBranchMergeError(f"{label} must be a non-empty string")
    return value


def _integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ProtectedBranchMergeError(f"{label} must be a positive integer")
    return value


def _sha(value: object, label: str) -> str:
    resolved = _string(value, label)
    if not _SHA.fullmatch(resolved):
        raise ProtectedBranchMergeError(f"{label} must be a full SHA")
    return resolved


def _validate_text(value: str, label: str, maximum: int) -> str:
    if not value.strip() or len(value) > maximum or any(ord(char) < 32 for char in value):
        raise ProtectedBranchMergeError(f"{label} is invalid")
    return value.strip()


def _validate_identity(
    *,
    repository: str,
    branch: str,
    base_sha: str,
    head_sha: str,
    title: str,
    body: str,
) -> None:
    if not _REPOSITORY.fullmatch(repository) or ".." in repository:
        raise ProtectedBranchMergeError("repository is invalid")
    if not _AUTOMATION_BRANCH.fullmatch(branch):
        raise ProtectedBranchMergeError("automation branch is invalid")
    _sha(base_sha, "base SHA")
    _sha(head_sha, "head SHA")
    if base_sha == head_sha:
        raise ProtectedBranchMergeError("automation head must differ from its base")
    _validate_text(title, "PR title", 120)
    _validate_text(body, "PR body", 1000)


def _ref_sha(api: GitHubApi, repository: str, ref: str) -> str:
    encoded = quote(ref, safe="")
    response = _object(
        api.request("GET", f"/repos/{repository}/git/ref/heads/{encoded}"),
        f"{ref} reference",
    )
    target = _object(response.get("object"), f"{ref} reference target")
    return _sha(target.get("sha"), f"{ref} reference SHA")


def _single_parent(api: GitHubApi, repository: str, commit_sha: str) -> str:
    response = _object(
        api.request("GET", f"/repos/{repository}/git/commits/{commit_sha}"),
        "Git commit",
    )
    if _sha(response.get("sha"), "Git commit SHA") != commit_sha:
        raise ProtectedBranchMergeError("Git commit identity mismatch")
    parents = _array(response.get("parents"), "Git commit parents")
    if len(parents) != 1:
        raise ProtectedBranchMergeError("validated commit must have exactly one parent")
    return _sha(_object(parents[0], "Git commit parent").get("sha"), "parent SHA")


def _poll_attempts(timeout_seconds: int, poll_seconds: int) -> int:
    if not 1 <= timeout_seconds <= 1800 or not 0 <= poll_seconds <= 60:
        raise ProtectedBranchMergeError("polling bounds are invalid")
    return max(1, math.ceil(timeout_seconds / max(1, poll_seconds)))


def _dispatch_workflow(
    api: GitHubApi,
    *,
    repository: str,
    workflow: str,
    body: dict[str, object],
) -> int:
    if workflow not in {"ci.yml", "deploy.yml"}:
        raise ProtectedBranchMergeError("workflow dispatch target is invalid")
    response = _object(
        api.request(
            "POST",
            f"/repos/{repository}/actions/workflows/{workflow}/dispatches",
            body,
        ),
        "workflow dispatch response",
    )
    run_id = _integer(response.get("workflow_run_id"), "workflow run id")
    expected_api_url = f"https://api.github.com/repos/{repository}/actions/runs/{run_id}"
    expected_html_url = f"https://github.com/{repository}/actions/runs/{run_id}"
    if (
        response.get("run_url") != expected_api_url
        or response.get("html_url") != expected_html_url
    ):
        raise ProtectedBranchMergeError("workflow dispatch response identity mismatch")
    return run_id


def _trusted_test_check(
    api: GitHubApi,
    *,
    repository: str,
    head_sha: str,
    run_id: int,
    expected_workflow_name: str,
    expected_success: bool,
) -> dict[str, object]:
    response = _object(
        api.request(
            "GET",
            f"/repos/{repository}/commits/{head_sha}/check-runs?per_page=100",
        ),
        "check run response",
    )
    matches: list[dict[str, object]] = []
    details_pattern = re.compile(
        rf"https://github\.com/{re.escape(repository)}/actions/runs/{run_id}/job/([1-9][0-9]*)\Z"
    )
    for raw in _array(response.get("check_runs"), "check runs"):
        check = _object(raw, "check run")
        app = _object(check.get("app"), "check run app")
        details = check.get("details_url")
        conclusion = check.get("conclusion")
        conclusion_matches = (
            conclusion == "success"
            if expected_success
            else conclusion in _FAILED_TEST_CONCLUSIONS
        )
        details_match = details_pattern.fullmatch(details) if isinstance(details, str) else None
        if (
            check.get("name") == _TEST_CHECK
            and check.get("status") == "completed"
            and conclusion_matches
            and app.get("id") == _TRUSTED_ACTIONS_APP_ID
            and details_match is not None
        ):
            matches.append(check)
    if len(matches) != 1:
        raise ProtectedBranchMergeError("trusted PR Test Suite check is missing or ambiguous")
    details_url = _string(matches[0].get("details_url"), "trusted check details URL")
    match = details_pattern.fullmatch(details_url)
    if match is None:
        raise ProtectedBranchMergeError("trusted PR Test Suite job URL is invalid")
    job_id = int(match.group(1))
    job = _object(
        api.request("GET", f"/repos/{repository}/actions/jobs/{job_id}"),
        "trusted test job",
    )
    job_conclusion = job.get("conclusion")
    job_conclusion_matches = (
        job_conclusion == "success"
        if expected_success
        else job_conclusion in _FAILED_TEST_CONCLUSIONS
    )
    if (
        job.get("id") != job_id
        or job.get("run_id") != run_id
        or job.get("name") != _TEST_CHECK
        or job.get("workflow_name") != expected_workflow_name
        or job.get("head_sha") != head_sha
        or job.get("status") != "completed"
        or not job_conclusion_matches
        or job.get("html_url") != details_url
    ):
        raise ProtectedBranchMergeError("trusted PR Test Suite job identity mismatch")
    return matches[0]


def _publish_required_check(
    api: GitHubApi,
    *,
    repository: str,
    head_sha: str,
    run_id: int,
    details_url: str,
    conclusion: str,
    subject: str,
    raw_conclusion: str = "",
) -> tuple[int, str]:
    if conclusion not in {"success", "failure"}:
        raise ProtectedBranchMergeError("required check conclusion is invalid")
    if conclusion == "success":
        outcome = "passed"
    elif raw_conclusion == "cancelled":
        # GitHub reports a job killed by timeout-minutes as 'cancelled', and on
        # this repository that is the dominant way CI stops: a cold
        # fetch-depth: 0 checkout of a multi-GB tree runs past the job budget.
        # Calling it "failed" sends the reader hunting for a broken test that
        # does not exist, when the fix is elsewhere entirely.
        outcome = "did not complete (cancelled — typically a job timeout)"
    elif raw_conclusion and raw_conclusion != "failure":
        outcome = f"did not complete ({raw_conclusion})"
    else:
        outcome = "failed"
    summary = f"PR Test Suite run {run_id} {outcome} for the exact {subject}."
    external_id = f"trusted-ci:{run_id}:{head_sha}"
    requested_details_url = f"https://github.com/{repository}/actions/runs/{run_id}"
    if details_url != requested_details_url:
        raise ProtectedBranchMergeError("required check trusted run URL mismatch")
    response = _object(
        api.request(
            "POST",
            f"/repos/{repository}/check-runs",
            {
                "conclusion": conclusion,
                "details_url": requested_details_url,
                "external_id": external_id,
                "head_sha": head_sha,
                "name": _REQUIRED_CHECK,
                "output": {
                    "summary": summary,
                    "title": "Validated GitHub Actions test run",
                },
                "status": "completed",
            },
        ),
        "required check response",
    )
    check_id = _integer(response.get("id"), "required check ID")
    app = _object(response.get("app"), "required check app")
    output = _object(response.get("output"), "required check output")
    # GitHub Actions currently normalizes an explicitly supplied workflow URL
    # to the canonical check-run URL for checks created with GITHUB_TOKEN.
    # Bind the check to the trusted run through its immutable ID, external_id,
    # exact head SHA and signed output instead of assuming details_url survives.
    canonical_details_url = f"https://github.com/{repository}/runs/{check_id}"
    if (
        response.get("name") != _REQUIRED_CHECK
        or response.get("head_sha") != head_sha
        or response.get("status") != "completed"
        or response.get("conclusion") != conclusion
        or response.get("external_id") != external_id
        or response.get("details_url")
        not in {requested_details_url, canonical_details_url}
        or output.get("summary") != summary
        or output.get("title") != "Validated GitHub Actions test run"
        or app.get("id") != _TRUSTED_ACTIONS_APP_ID
    ):
        raise ProtectedBranchMergeError("required check response failed identity validation")
    return check_id, external_id


def _required_check_visible(
    api: GitHubApi,
    *,
    repository: str,
    head_sha: str,
    run_id: int,
    check_id: int,
    external_id: str,
) -> bool:
    response = _object(
        api.request(
            "GET",
            f"/repos/{repository}/commits/{head_sha}/check-runs?per_page=100",
        ),
        "required check list",
    )
    expected_summary = f"PR Test Suite run {run_id} passed for the exact automation head."
    accepted_urls = {
        f"https://github.com/{repository}/actions/runs/{run_id}",
        f"https://github.com/{repository}/runs/{check_id}",
    }
    matches = []
    for raw in _array(response.get("check_runs"), "required check runs"):
        check = _object(raw, "required check run")
        if check.get("id") != check_id:
            continue
        app = _object(check.get("app"), "required check app")
        output = _object(check.get("output"), "required check output")
        if (
            check.get("name") == _REQUIRED_CHECK
            and check.get("head_sha") == head_sha
            and check.get("status") == "completed"
            and check.get("conclusion") == "success"
            and check.get("external_id") == external_id
            and check.get("details_url") in accepted_urls
            and output.get("summary") == expected_summary
            and output.get("title") == "Validated GitHub Actions test run"
            and app.get("id") == _TRUSTED_ACTIONS_APP_ID
        ):
            matches.append(check)
    return len(matches) == 1


def _run_trusted_ci(
    api: GitHubApi,
    *,
    repository: str,
    target_sha: str,
    main_sha: str,
    attempts: int,
    poll_seconds: int,
    sleep: Callable[[float], None],
) -> tuple[int, str, str]:
    """Run the test definition from main while checking out one exact target SHA."""

    run_id = _dispatch_workflow(
        api,
        repository=repository,
        workflow="ci.yml",
        body={"inputs": {"target_sha": target_sha}, "ref": "main"},
    )
    completed: dict[str, object] | None = None
    expected_run_name = f"trusted-ci:{target_sha}"
    for _ in range(attempts):
        run = _object(
            api.request("GET", f"/repos/{repository}/actions/runs/{run_id}"),
            "trusted validation workflow run",
        )
        if (
            run.get("id") != run_id
            or run.get("path") != ".github/workflows/ci.yml"
            or run.get("event") != "workflow_dispatch"
            or run.get("head_branch") != "main"
            or run.get("head_sha") != main_sha
        ):
            raise ProtectedBranchMergeError("trusted validation workflow identity mismatch")
        if (
            run.get("name") != expected_run_name
            or run.get("display_title") != expected_run_name
        ):
            if run.get("status") == "completed":
                raise ProtectedBranchMergeError(
                    "trusted validation workflow title identity mismatch"
                )
            # GitHub may briefly expose the static workflow name immediately after
            # dispatch before materializing run-name. Immutable path/event/SHA
            # fields above must already match; only this presentation field waits.
            sleep(poll_seconds)
            continue
        if run.get("status") == "completed":
            completed = run
            break
        sleep(poll_seconds)
    if completed is None:
        raise ProtectedBranchMergeError("trusted validation workflow did not complete")
    raw_conclusion = completed.get("conclusion")
    if raw_conclusion == "success":
        conclusion = "success"
    elif raw_conclusion in _FAILED_TEST_CONCLUSIONS:
        conclusion = "failure"
    else:
        raise ProtectedBranchMergeError("trusted validation conclusion is invalid")
    run_url = _string(completed.get("html_url"), "trusted validation workflow URL")
    if run_url != f"https://github.com/{repository}/actions/runs/{run_id}":
        raise ProtectedBranchMergeError("trusted validation workflow URL identity mismatch")
    _trusted_test_check(
        api,
        repository=repository,
        head_sha=main_sha,
        run_id=run_id,
        expected_workflow_name=expected_run_name,
        expected_success=conclusion == "success",
    )
    return run_id, run_url, conclusion, str(raw_conclusion or "")


def merge_validated_branch(
    api: GitHubApi,
    *,
    repository: str,
    branch: str,
    base_sha: str,
    head_sha: str,
    title: str,
    body: str,
    timeout_seconds: int = 1200,
    poll_seconds: int = 5,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, object]:
    """Run real tests, publish the required check, and squash-merge one PR."""

    _validate_identity(
        repository=repository,
        branch=branch,
        base_sha=base_sha,
        head_sha=head_sha,
        title=title,
        body=body,
    )
    attempts = _poll_attempts(timeout_seconds, poll_seconds)
    if _ref_sha(api, repository, "main") != base_sha:
        raise ProtectedBranchMergeError("main moved before validation dispatch")
    if _ref_sha(api, repository, branch) != head_sha:
        raise ProtectedBranchMergeError("automation branch head mismatch")
    if _single_parent(api, repository, head_sha) != base_sha:
        raise ProtectedBranchMergeError("automation commit is not based on the expected main SHA")

    run_id, run_url, conclusion, _raw_conclusion = _run_trusted_ci(
        api,
        repository=repository,
        target_sha=head_sha,
        main_sha=base_sha,
        attempts=attempts,
        poll_seconds=poll_seconds,
        sleep=sleep,
    )
    if conclusion != "success":
        raise ProtectedBranchMergeError("validation workflow did not succeed")
    required_check_id, required_check_external_id = _publish_required_check(
        api,
        repository=repository,
        head_sha=head_sha,
        run_id=run_id,
        details_url=run_url,
        conclusion="success",
        subject="automation head",
    )

    if _ref_sha(api, repository, "main") != base_sha:
        raise ProtectedBranchMergeError("main moved after validation")
    created = _object(
        api.request(
            "POST",
            f"/repos/{repository}/pulls",
            {
                "base": "main",
                "body": body,
                "draft": False,
                "head": branch,
                "title": title,
            },
        ),
        "created pull request",
    )
    pr_number = _integer(created.get("number"), "pull request number")
    created_head = _object(created.get("head"), "pull request head")
    created_base = _object(created.get("base"), "pull request base")
    if (
        created_head.get("sha") != head_sha
        or created_head.get("ref") != branch
        or created_base.get("sha") != base_sha
        or created_base.get("ref") != "main"
    ):
        raise ProtectedBranchMergeError("created pull request identity mismatch")

    ready = False
    for _ in range(attempts):
        current = _object(
            api.request("GET", f"/repos/{repository}/pulls/{pr_number}"),
            "pull request",
        )
        current_head = _object(current.get("head"), "pull request head")
        current_base = _object(current.get("base"), "pull request base")
        if (
            current.get("number") != pr_number
            or current.get("state") != "open"
            or current.get("draft") is not False
            or current_head.get("sha") != head_sha
            or current_head.get("ref") != branch
            or current_base.get("sha") != base_sha
            or current_base.get("ref") != "main"
        ):
            raise ProtectedBranchMergeError("pull request changed after creation")
        if not _required_check_visible(
            api,
            repository=repository,
            head_sha=head_sha,
            run_id=run_id,
            check_id=required_check_id,
            external_id=required_check_external_id,
        ):
            sleep(poll_seconds)
            continue
        mergeable = current.get("mergeable")
        if mergeable is False:
            raise ProtectedBranchMergeError("pull request is not mergeable")
        if mergeable is True and current.get("mergeable_state") == "clean":
            ready = True
            break
        sleep(poll_seconds)
    if not ready:
        raise ProtectedBranchMergeError("pull request mergeability did not resolve")
    if _ref_sha(api, repository, "main") != base_sha:
        raise ProtectedBranchMergeError("main moved before squash merge")

    merged = _object(
        api.request(
            "PUT",
            f"/repos/{repository}/pulls/{pr_number}/merge",
            {
                "commit_message": body,
                "commit_title": title,
                "merge_method": "squash",
                "sha": head_sha,
            },
        ),
        "pull request merge response",
    )
    if merged.get("merged") is not True:
        raise ProtectedBranchMergeError("GitHub refused the protected squash merge")
    merge_sha = _sha(merged.get("sha"), "merge SHA")
    if _single_parent(api, repository, merge_sha) != base_sha:
        raise ProtectedBranchMergeError("squash merge parent does not match expected main")
    if _ref_sha(api, repository, "main") != merge_sha:
        raise ProtectedBranchMergeError("main does not point to the returned merge SHA")
    return {
        "base_sha": base_sha,
        "branch": branch,
        "check_name": _REQUIRED_CHECK,
        "head_sha": head_sha,
        "merge_sha": merge_sha,
        "pr_number": pr_number,
        "run_id": run_id,
        "schema_version": "protected_branch_merge_v1",
    }


def dispatch_deploy_and_wait(
    api: GitHubApi,
    *,
    repository: str,
    expected_sha: str,
    timeout_seconds: int = 1800,
    poll_seconds: int = 10,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, object]:
    """Dispatch one non-refresh deploy and wait for that exact run and SHA."""

    if not _REPOSITORY.fullmatch(repository) or ".." in repository:
        raise ProtectedBranchMergeError("repository is invalid")
    _sha(expected_sha, "expected deploy SHA")
    attempts = _poll_attempts(timeout_seconds, poll_seconds)
    if _ref_sha(api, repository, "main") != expected_sha:
        raise ProtectedBranchMergeError("main moved before deploy dispatch")
    run_id = _dispatch_workflow(
        api,
        repository=repository,
        workflow="deploy.yml",
        body={
            "inputs": {
                "expected_sha": expected_sha,
                "refresh_data": "false",
            },
            "ref": "main",
        },
    )
    completed: dict[str, object] | None = None
    for _ in range(attempts):
        run = _object(
            api.request("GET", f"/repos/{repository}/actions/runs/{run_id}"),
            "deploy workflow run",
        )
        if (
            run.get("id") != run_id
            or run.get("name") != "Build and Deploy"
            or run.get("path") != ".github/workflows/deploy.yml"
            or run.get("event") != "workflow_dispatch"
            or run.get("head_branch") != "main"
            or run.get("head_sha") != expected_sha
        ):
            raise ProtectedBranchMergeError("deploy workflow identity mismatch")
        if run.get("status") == "completed":
            completed = run
            break
        sleep(poll_seconds)
    if completed is None:
        raise ProtectedBranchMergeError("deploy workflow did not complete")
    if completed.get("conclusion") != "success":
        raise ProtectedBranchMergeError("deploy workflow did not succeed")
    url = _string(completed.get("html_url"), "deploy workflow URL")
    if url != f"https://github.com/{repository}/actions/runs/{run_id}":
        raise ProtectedBranchMergeError("deploy workflow URL identity mismatch")
    return {
        "conclusion": "success",
        "head_sha": expected_sha,
        "run_id": run_id,
        "schema_version": "protected_deploy_dispatch_v1",
        "url": url,
    }


def validate_pull_request(
    api: GitHubApi,
    *,
    repository: str,
    pr_number: int,
    head_sha: str,
    timeout_seconds: int = 1200,
    poll_seconds: int = 5,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, object]:
    """Run main's trusted test definition against one exact human PR head."""

    if not _REPOSITORY.fullmatch(repository) or ".." in repository:
        raise ProtectedBranchMergeError("repository is invalid")
    _integer(pr_number, "pull request number")
    _sha(head_sha, "pull request head SHA")
    attempts = _poll_attempts(timeout_seconds, poll_seconds)

    def current_pr() -> tuple[str, str]:
        pull_request = _object(
            api.request("GET", f"/repos/{repository}/pulls/{pr_number}"),
            "pull request",
        )
        if (
            pull_request.get("number") != pr_number
            or pull_request.get("state") != "open"
            or pull_request.get("draft") is not False
        ):
            raise ProtectedBranchMergeError("pull request is not open and ready")
        pr_head = _object(pull_request.get("head"), "pull request head")
        pr_base = _object(pull_request.get("base"), "pull request base")
        head_branch = _string(pr_head.get("ref"), "pull request head branch")
        base_sha = _sha(pr_base.get("sha"), "pull request base SHA")
        if (
            pr_head.get("sha") != head_sha
            or head_branch.startswith("automation/")
            or pr_base.get("ref") != "main"
        ):
            raise ProtectedBranchMergeError("pull request identity mismatch")
        return head_branch, base_sha

    _head_branch, base_sha = current_pr()
    if _ref_sha(api, repository, "main") != base_sha:
        raise ProtectedBranchMergeError("main moved before trusted PR validation")
    run_id, run_url, conclusion, raw_conclusion = _run_trusted_ci(
        api,
        repository=repository,
        target_sha=head_sha,
        main_sha=base_sha,
        attempts=attempts,
        poll_seconds=poll_seconds,
        sleep=sleep,
    )
    current_pr()
    if _ref_sha(api, repository, "main") != base_sha:
        raise ProtectedBranchMergeError("main moved after trusted PR validation")
    _publish_required_check(
        api,
        repository=repository,
        head_sha=head_sha,
        run_id=run_id,
        details_url=run_url,
        conclusion=conclusion,
        subject="pull request head",
        raw_conclusion=raw_conclusion,
    )
    return {
        "check_conclusion": conclusion,
        "head_sha": head_sha,
        "pr_number": pr_number,
        "run_id": run_id,
        "schema_version": "protected_pr_gate_v2",
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    merge = commands.add_parser("merge")
    merge.add_argument("--repository", required=True)
    merge.add_argument("--branch", required=True)
    merge.add_argument("--base-sha", required=True)
    merge.add_argument("--head-sha", required=True)
    merge.add_argument("--title", required=True)
    merge.add_argument("--body", required=True)
    merge.add_argument("--timeout-seconds", type=int, default=1200)
    merge.add_argument("--poll-seconds", type=int, default=5)
    validate_pr = commands.add_parser("validate-pr")
    validate_pr.add_argument("--repository", required=True)
    validate_pr.add_argument("--pr-number", required=True, type=int)
    validate_pr.add_argument("--head-sha", required=True)
    validate_pr.add_argument("--timeout-seconds", type=int, default=1200)
    validate_pr.add_argument("--poll-seconds", type=int, default=5)
    deploy = commands.add_parser("deploy")
    deploy.add_argument("--repository", required=True)
    deploy.add_argument("--expected-sha", required=True)
    deploy.add_argument("--timeout-seconds", type=int, default=1800)
    deploy.add_argument("--poll-seconds", type=int, default=10)
    return parser


def main(argv: Sequence[str] | None = None, *, api: GitHubApi | None = None) -> int:
    args = _parser().parse_args(argv)
    client: GitHubApi = api or GhCliApi()
    try:
        if args.command == "merge":
            result = merge_validated_branch(
                client,
                repository=args.repository,
                branch=args.branch,
                base_sha=args.base_sha,
                head_sha=args.head_sha,
                title=args.title,
                body=args.body,
                timeout_seconds=args.timeout_seconds,
                poll_seconds=args.poll_seconds,
            )
        elif args.command == "validate-pr":
            result = validate_pull_request(
                client,
                repository=args.repository,
                pr_number=args.pr_number,
                head_sha=args.head_sha,
                timeout_seconds=args.timeout_seconds,
                poll_seconds=args.poll_seconds,
            )
        else:
            result = dispatch_deploy_and_wait(
                client,
                repository=args.repository,
                expected_sha=args.expected_sha,
                timeout_seconds=args.timeout_seconds,
                poll_seconds=args.poll_seconds,
            )
    except ProtectedBranchMergeError as exc:
        print(f"protected-branch-merge: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
