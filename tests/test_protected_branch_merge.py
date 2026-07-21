from __future__ import annotations

import copy
from collections.abc import Callable

import pytest

from scripts.protected_branch_merge import (
    ProtectedBranchMergeError,
    dispatch_deploy_and_wait,
    merge_validated_branch,
    validate_pull_request,
)


REPOSITORY = "g5n-dev/ai-stack"
BASE_SHA = "a" * 40
HEAD_SHA = "b" * 40
MERGE_SHA = "c" * 40
BRANCH = "automation/data-12345-1"


class FakeApi:
    def __init__(
        self,
        responder: Callable[[str, str, dict[str, object] | None], object | None],
    ) -> None:
        self.responder = responder
        self.calls: list[tuple[str, str, dict[str, object] | None]] = []

    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
    ) -> object | None:
        self.calls.append((method, endpoint, copy.deepcopy(body)))
        return self.responder(method, endpoint, body)


def _successful_responder() -> tuple[
    Callable[[str, str, dict[str, object] | None], object | None], dict[str, int]
]:
    state = {"main_reads": 0}

    def respond(method: str, endpoint: str, body: dict[str, object] | None) -> object | None:
        del body
        if endpoint.endswith("/git/ref/heads/main"):
            state["main_reads"] += 1
            sha = MERGE_SHA if state["main_reads"] >= 4 else BASE_SHA
            return {"object": {"sha": sha}}
        if endpoint.endswith("/git/ref/heads/automation%2Fdata-12345-1"):
            return {"object": {"sha": HEAD_SHA}}
        if endpoint.endswith(f"/git/commits/{HEAD_SHA}"):
            return {"sha": HEAD_SHA, "parents": [{"sha": BASE_SHA}]}
        if endpoint.endswith(f"/git/commits/{MERGE_SHA}"):
            return {"sha": MERGE_SHA, "parents": [{"sha": BASE_SHA}]}
        if endpoint.endswith("/actions/workflows/ci.yml/dispatches") and method == "POST":
            return {
                "workflow_run_id": 99,
                "run_url": "https://api.github.com/repos/g5n-dev/ai-stack/actions/runs/99",
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/99",
            }
        if endpoint.endswith("/actions/runs/99"):
            return {
                "id": 99,
                "name": f"trusted-ci:{HEAD_SHA}",
                "path": ".github/workflows/ci.yml",
                "event": "workflow_dispatch",
                "head_branch": "main",
                "head_sha": BASE_SHA,
                "display_title": f"trusted-ci:{HEAD_SHA}",
                "status": "completed",
                "conclusion": "success",
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/99",
            }
        if endpoint.endswith(f"/commits/{BASE_SHA}/check-runs?per_page=100"):
            return {
                "check_runs": [
                    {
                        "name": "PR Test Suite",
                        "status": "completed",
                        "conclusion": "success",
                        "details_url": (
                            "https://github.com/g5n-dev/ai-stack/actions/runs/99/job/100"
                        ),
                        "app": {"id": 15368},
                    }
                ]
            }
        if endpoint.endswith("/actions/jobs/100"):
            return {
                "id": 100,
                "run_id": 99,
                "name": "PR Test Suite",
                "workflow_name": "PR CI",
                "head_sha": BASE_SHA,
                "status": "completed",
                "conclusion": "success",
                "html_url": (
                    "https://github.com/g5n-dev/ai-stack/actions/runs/99/job/100"
                ),
            }
        if endpoint.endswith(f"/commits/{HEAD_SHA}/check-runs?per_page=100"):
            return {
                "check_runs": [
                    {
                        "name": "Unit Tests",
                        "status": "completed",
                        "conclusion": "success",
                        "details_url": (
                            "https://github.com/g5n-dev/ai-stack/actions/runs/99"
                        ),
                        "app": {"id": 15368},
                    }
                ]
            }
        if endpoint.endswith("/check-runs") and method == "POST":
            return {
                "name": "Unit Tests",
                "head_sha": HEAD_SHA,
                "status": "completed",
                "conclusion": "success",
                "app": {"id": 15368},
            }
        if endpoint.endswith("/pulls") and method == "POST":
            return {
                "number": 77,
                "head": {"sha": HEAD_SHA, "ref": BRANCH},
                "base": {"sha": BASE_SHA, "ref": "main"},
            }
        if endpoint.endswith("/pulls/77") and method == "GET":
            return {
                "number": 77,
                "state": "open",
                "draft": False,
                "head": {"sha": HEAD_SHA, "ref": BRANCH},
                "base": {"sha": BASE_SHA, "ref": "main"},
                "mergeable": True,
                "mergeable_state": "clean",
            }
        if endpoint.endswith("/pulls/77/merge") and method == "PUT":
            return {"merged": True, "sha": MERGE_SHA, "message": "merged"}
        raise AssertionError(f"unexpected API request: {method} {endpoint}")

    return respond, state


def test_dispatches_real_ci_then_sha_locks_pr_merge() -> None:
    responder, state = _successful_responder()
    api = FakeApi(responder)

    receipt = merge_validated_branch(
        api,
        repository=REPOSITORY,
        branch=BRANCH,
        base_sha=BASE_SHA,
        head_sha=HEAD_SHA,
        title="chore(data): persist validated release",
        body="Validated by the isolated release pipeline.",
        timeout_seconds=5,
        poll_seconds=0,
        sleep=lambda _seconds: None,
    )

    assert receipt == {
        "base_sha": BASE_SHA,
        "branch": BRANCH,
        "check_name": "Unit Tests",
        "head_sha": HEAD_SHA,
        "merge_sha": MERGE_SHA,
        "pr_number": 77,
        "run_id": 99,
        "schema_version": "protected_branch_merge_v1",
    }
    assert state["main_reads"] == 4
    dispatch = next(call for call in api.calls if call[1].endswith("/dispatches"))
    assert dispatch == (
        "POST",
        "/repos/g5n-dev/ai-stack/actions/workflows/ci.yml/dispatches",
        {"inputs": {"target_sha": HEAD_SHA}, "ref": "main"},
    )
    assert not any("/actions/workflows/ci.yml/runs?" in call[1] for call in api.calls)
    required_check = next(
        call
        for call in api.calls
        if call[0] == "POST" and call[1].endswith("/check-runs")
    )
    assert required_check[2] == {
        "conclusion": "success",
        "details_url": "https://github.com/g5n-dev/ai-stack/actions/runs/99",
        "head_sha": HEAD_SHA,
        "name": "Unit Tests",
        "output": {
            "summary": "PR Test Suite run 99 passed for the exact automation head.",
            "title": "Validated GitHub Actions test run",
        },
        "status": "completed",
    }
    merge = next(call for call in api.calls if call[1].endswith("/pulls/77/merge"))
    assert merge[2] == {
        "commit_message": "Validated by the isolated release pipeline.",
        "commit_title": "chore(data): persist validated release",
        "merge_method": "squash",
        "sha": HEAD_SHA,
    }


def test_wrong_check_app_fails_before_pr_creation() -> None:
    responder, _state = _successful_responder()

    def wrong_app(method: str, endpoint: str, body: dict[str, object] | None) -> object | None:
        response = responder(method, endpoint, body)
        if endpoint.endswith(f"/commits/{BASE_SHA}/check-runs?per_page=100"):
            assert isinstance(response, dict)
            response["check_runs"][0]["app"]["id"] = 999  # type: ignore[index]
        return response

    api = FakeApi(wrong_app)
    with pytest.raises(ProtectedBranchMergeError, match="trusted PR Test Suite check"):
        merge_validated_branch(
            api,
            repository=REPOSITORY,
            branch=BRANCH,
            base_sha=BASE_SHA,
            head_sha=HEAD_SHA,
            title="chore(data): persist validated release",
            body="Validated by the isolated release pipeline.",
            timeout_seconds=1,
            poll_seconds=0,
            sleep=lambda _seconds: None,
        )
    assert not any(endpoint.endswith("/pulls") for _, endpoint, _ in api.calls)


def test_trusted_dispatch_waits_for_dynamic_run_name_to_stabilize() -> None:
    responder, _state = _successful_responder()
    run_reads = 0

    def eventual_name(
        method: str,
        endpoint: str,
        body: dict[str, object] | None,
    ) -> object | None:
        nonlocal run_reads
        response = responder(method, endpoint, body)
        if endpoint.endswith("/actions/runs/99"):
            run_reads += 1
            if run_reads == 1:
                assert isinstance(response, dict)
                response["name"] = "PR CI"
                response["display_title"] = "PR CI"
                response["status"] = "queued"
                response["conclusion"] = None
        return response

    receipt = merge_validated_branch(
        FakeApi(eventual_name),
        repository=REPOSITORY,
        branch=BRANCH,
        base_sha=BASE_SHA,
        head_sha=HEAD_SHA,
        title="chore(data): persist validated release",
        body="Validated by the isolated release pipeline.",
        timeout_seconds=5,
        poll_seconds=0,
        sleep=lambda _seconds: None,
    )

    assert receipt["run_id"] == 99
    assert run_reads == 2


def test_dispatch_deploy_uses_returned_run_id_and_exact_sha() -> None:
    calls: list[tuple[str, str, dict[str, object] | None]] = []

    def respond(method: str, endpoint: str, body: dict[str, object] | None) -> object:
        calls.append((method, endpoint, body))
        if endpoint.endswith("/git/ref/heads/main"):
            return {"object": {"sha": MERGE_SHA}}
        if endpoint.endswith("/actions/workflows/deploy.yml/dispatches"):
            return {
                "workflow_run_id": 801,
                "run_url": "https://api.github.com/repos/g5n-dev/ai-stack/actions/runs/801",
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/801",
            }
        if endpoint.endswith("/actions/runs/801"):
            return {
                "id": 801,
                "name": "Build and Deploy",
                "path": ".github/workflows/deploy.yml",
                "event": "workflow_dispatch",
                "head_branch": "main",
                "head_sha": MERGE_SHA,
                "status": "completed",
                "conclusion": "success",
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/801",
            }
        raise AssertionError(f"unexpected API request: {method} {endpoint}")

    receipt = dispatch_deploy_and_wait(
        FakeApi(respond),
        repository=REPOSITORY,
        expected_sha=MERGE_SHA,
        timeout_seconds=5,
        poll_seconds=0,
        sleep=lambda _seconds: None,
    )

    assert receipt == {
        "conclusion": "success",
        "head_sha": MERGE_SHA,
        "run_id": 801,
        "schema_version": "protected_deploy_dispatch_v1",
        "url": "https://github.com/g5n-dev/ai-stack/actions/runs/801",
    }
    dispatch_call = next(call for call in calls if call[1].endswith("/dispatches"))
    assert dispatch_call == (
        "POST",
        "/repos/g5n-dev/ai-stack/actions/workflows/deploy.yml/dispatches",
        {
            "inputs": {"expected_sha": MERGE_SHA, "refresh_data": "false"},
            "ref": "main",
        },
    )


def test_dispatch_deploy_rejects_a_run_for_another_sha() -> None:
    def respond(method: str, endpoint: str, body: dict[str, object] | None) -> object:
        del method, body
        if endpoint.endswith("/git/ref/heads/main"):
            return {"object": {"sha": MERGE_SHA}}
        if endpoint.endswith("/actions/workflows/deploy.yml/dispatches"):
            return {
                "workflow_run_id": 802,
                "run_url": "https://api.github.com/repos/g5n-dev/ai-stack/actions/runs/802",
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/802",
            }
        if endpoint.endswith("/actions/runs/802"):
            return {
                "id": 802,
                "name": "Build and Deploy",
                "path": ".github/workflows/deploy.yml",
                "event": "workflow_dispatch",
                "head_branch": "main",
                "head_sha": HEAD_SHA,
                "status": "queued",
                "conclusion": None,
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/802",
            }
        raise AssertionError(f"unexpected endpoint: {endpoint}")

    with pytest.raises(ProtectedBranchMergeError, match="deploy workflow identity mismatch"):
        dispatch_deploy_and_wait(
            FakeApi(respond),
            repository=REPOSITORY,
            expected_sha=MERGE_SHA,
            timeout_seconds=1,
            poll_seconds=0,
            sleep=lambda _seconds: None,
        )


def test_dispatch_deploy_refuses_to_start_after_main_moves() -> None:
    api = FakeApi(
        lambda _method, endpoint, _body: (
            {"object": {"sha": HEAD_SHA}}
            if endpoint.endswith("/git/ref/heads/main")
            else pytest.fail(f"unexpected write after stale main: {endpoint}")
        )
    )

    with pytest.raises(ProtectedBranchMergeError, match="main moved before deploy dispatch"):
        dispatch_deploy_and_wait(
            api,
            repository=REPOSITORY,
            expected_sha=MERGE_SHA,
            timeout_seconds=1,
            poll_seconds=0,
            sleep=lambda _seconds: None,
        )
    assert not any(endpoint.endswith("/dispatches") for _, endpoint, _ in api.calls)


def test_default_branch_controller_runs_trusted_ci_for_a_human_pr() -> None:
    def respond(method: str, endpoint: str, body: dict[str, object] | None) -> object | None:
        if endpoint.endswith("/pulls/88") and method == "GET":
            return {
                "number": 88,
                "state": "open",
                "draft": False,
                "head": {"ref": "codex/human-change", "sha": HEAD_SHA},
                "base": {"ref": "main", "sha": BASE_SHA},
            }
        if endpoint.endswith("/git/ref/heads/main"):
            return {"object": {"sha": BASE_SHA}}
        if endpoint.endswith("/actions/workflows/ci.yml/dispatches") and method == "POST":
            return {
                "workflow_run_id": 501,
                "run_url": "https://api.github.com/repos/g5n-dev/ai-stack/actions/runs/501",
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/501",
            }
        if endpoint.endswith("/actions/runs/501") and method == "GET":
            return {
                "id": 501,
                "name": f"trusted-ci:{HEAD_SHA}",
                "path": ".github/workflows/ci.yml",
                "event": "workflow_dispatch",
                "head_sha": BASE_SHA,
                "head_branch": "main",
                "display_title": f"trusted-ci:{HEAD_SHA}",
                "status": "completed",
                "conclusion": "success",
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/501",
            }
        if endpoint.endswith(f"/commits/{BASE_SHA}/check-runs?per_page=100"):
            return {
                "check_runs": [
                    {
                        "name": "PR Test Suite",
                        "status": "completed",
                        "conclusion": "success",
                        "details_url": (
                            "https://github.com/g5n-dev/ai-stack/actions/runs/501/job/502"
                        ),
                        "app": {"id": 15368},
                    }
                ]
            }
        if endpoint.endswith("/actions/jobs/502"):
            return {
                "id": 502,
                "run_id": 501,
                "name": "PR Test Suite",
                "workflow_name": "PR CI",
                "head_sha": BASE_SHA,
                "status": "completed",
                "conclusion": "success",
                "html_url": (
                    "https://github.com/g5n-dev/ai-stack/actions/runs/501/job/502"
                ),
            }
        if endpoint.endswith("/check-runs") and method == "POST":
            assert body is not None
            return {
                "name": body["name"],
                "head_sha": body["head_sha"],
                "status": body["status"],
                "conclusion": body["conclusion"],
                "app": {"id": 15368},
            }
        raise AssertionError(f"unexpected API request: {method} {endpoint}")

    api = FakeApi(respond)
    receipt = validate_pull_request(
        api,
        repository=REPOSITORY,
        pr_number=88,
        head_sha=HEAD_SHA,
        timeout_seconds=5,
        poll_seconds=0,
        sleep=lambda _seconds: None,
    )

    assert receipt == {
        "check_conclusion": "success",
        "head_sha": HEAD_SHA,
        "pr_number": 88,
        "run_id": 501,
        "schema_version": "protected_pr_gate_v2",
    }
    published = api.calls[-1]
    assert published[0] == "POST"
    assert published[1].endswith("/check-runs")
    assert published[2]["name"] == "Unit Tests"  # type: ignore[index]


@pytest.mark.parametrize("test_conclusion", ["failure", "cancelled", "timed_out"])
def test_controller_maps_failed_trusted_test_run_to_failed_required_check(
    test_conclusion: str,
) -> None:
    def respond(method: str, endpoint: str, body: dict[str, object] | None) -> object | None:
        if endpoint.endswith("/pulls/89"):
            return {
                "number": 89,
                "state": "open",
                "draft": False,
                "head": {"ref": "codex/failing-change", "sha": HEAD_SHA},
                "base": {"ref": "main", "sha": BASE_SHA},
            }
        if endpoint.endswith("/git/ref/heads/main"):
            return {"object": {"sha": BASE_SHA}}
        if endpoint.endswith("/actions/workflows/ci.yml/dispatches"):
            return {
                "workflow_run_id": 601,
                "run_url": "https://api.github.com/repos/g5n-dev/ai-stack/actions/runs/601",
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/601",
            }
        if endpoint.endswith("/actions/runs/601"):
            return {
                "id": 601,
                "name": f"trusted-ci:{HEAD_SHA}",
                "path": ".github/workflows/ci.yml",
                "event": "workflow_dispatch",
                "head_sha": BASE_SHA,
                "head_branch": "main",
                "display_title": f"trusted-ci:{HEAD_SHA}",
                "status": "completed",
                "conclusion": test_conclusion,
                "html_url": "https://github.com/g5n-dev/ai-stack/actions/runs/601",
            }
        if endpoint.endswith(f"/commits/{BASE_SHA}/check-runs?per_page=100"):
            return {
                "check_runs": [
                    {
                        "name": "PR Test Suite",
                        "status": "completed",
                        "conclusion": test_conclusion,
                        "details_url": (
                            "https://github.com/g5n-dev/ai-stack/actions/runs/601/job/602"
                        ),
                        "app": {"id": 15368},
                    }
                ]
            }
        if endpoint.endswith("/actions/jobs/602"):
            return {
                "id": 602,
                "run_id": 601,
                "name": "PR Test Suite",
                "workflow_name": "PR CI",
                "head_sha": BASE_SHA,
                "status": "completed",
                "conclusion": test_conclusion,
                "html_url": (
                    "https://github.com/g5n-dev/ai-stack/actions/runs/601/job/602"
                ),
            }
        if endpoint.endswith("/check-runs") and method == "POST":
            assert body is not None
            return {
                "name": body["name"],
                "head_sha": body["head_sha"],
                "status": body["status"],
                "conclusion": body["conclusion"],
                "app": {"id": 15368},
            }
        raise AssertionError(f"unexpected API request: {method} {endpoint}")

    api = FakeApi(respond)
    receipt = validate_pull_request(
        api,
        repository=REPOSITORY,
        pr_number=89,
        head_sha=HEAD_SHA,
        timeout_seconds=5,
        poll_seconds=0,
        sleep=lambda _seconds: None,
    )
    assert receipt["check_conclusion"] == "failure"
    assert api.calls[-1][2]["conclusion"] == "failure"  # type: ignore[index]


def test_main_cas_movement_after_ci_fails_before_pr_creation() -> None:
    responder, state = _successful_responder()

    def moved_main(method: str, endpoint: str, body: dict[str, object] | None) -> object | None:
        if endpoint.endswith("/git/ref/heads/main") and state["main_reads"] == 1:
            state["main_reads"] += 1
            return {"object": {"sha": "d" * 40}}
        return responder(method, endpoint, body)

    api = FakeApi(moved_main)
    with pytest.raises(ProtectedBranchMergeError, match="main moved"):
        merge_validated_branch(
            api,
            repository=REPOSITORY,
            branch=BRANCH,
            base_sha=BASE_SHA,
            head_sha=HEAD_SHA,
            title="chore(data): persist validated release",
            body="Validated by the isolated release pipeline.",
            timeout_seconds=1,
            poll_seconds=0,
            sleep=lambda _seconds: None,
        )
    assert not any(endpoint.endswith("/pulls") for _, endpoint, _ in api.calls)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("repository", "https://github.com/g5n-dev/ai-stack"),
        ("branch", "main"),
        ("base_sha", "short"),
        ("head_sha", BASE_SHA),
        ("title", ""),
    ],
)
def test_rejects_unsafe_identity_before_api_calls(field: str, value: str) -> None:
    api = FakeApi(lambda _method, _endpoint, _body: None)
    arguments = {
        "repository": REPOSITORY,
        "branch": BRANCH,
        "base_sha": BASE_SHA,
        "head_sha": HEAD_SHA,
        "title": "chore(data): persist validated release",
        "body": "Validated by the isolated release pipeline.",
    }
    arguments[field] = value

    with pytest.raises(ProtectedBranchMergeError):
        merge_validated_branch(
            api,
            **arguments,
            timeout_seconds=1,
            poll_seconds=0,
            sleep=lambda _seconds: None,
        )
    assert api.calls == []
