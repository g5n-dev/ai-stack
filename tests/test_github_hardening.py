from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from scripts.github_hardening import (
    API_VERSION,
    GhCliApi,
    GitHubApiError,
    GitHubHardeningError,
    apply_hardening,
    build_plan,
    canonical_json,
    collect_snapshot,
    load_expected_config,
    main,
    snapshot_digest,
)

REPOSITORY = "g5n-dev/ai-stack"
REPOSITORY_ID = 987_654
OWNER_ID = 123_456
MAIN_SHA = "a" * 40


class FakeGitHubApi:
    def __init__(self, responses: dict[tuple[str, str], object]) -> None:
        self.responses = copy.deepcopy(responses)
        self.calls: list[tuple[str, str, dict[str, object] | None]] = []

    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
        *,
        allow_not_found: bool = False,
    ) -> object | None:
        self.calls.append((method, endpoint, copy.deepcopy(body)))
        key = (method, endpoint)
        if key not in self.responses:
            if allow_not_found:
                return None
            if method != "GET":
                return {}
            raise AssertionError(f"unexpected API request: {method} {endpoint}")
        response = self.responses[key]
        if isinstance(response, Exception):
            raise response
        return copy.deepcopy(response)

    @property
    def writes(self) -> list[tuple[str, str, dict[str, object] | None]]:
        return [call for call in self.calls if call[0] != "GET"]


def _base_responses(
    *,
    ruleset_summaries: list[dict[str, object]] | None = None,
    ruleset_details: list[dict[str, object]] | None = None,
    environments: list[dict[str, object]] | None = None,
    immutable: object | None = None,
) -> dict[tuple[str, str], object]:
    prefix = f"/repos/{REPOSITORY}"
    summaries = ruleset_summaries or []
    details = ruleset_details or []
    environment_items = environments or []
    responses: dict[tuple[str, str], object] = {
        ("GET", prefix): {
            "id": REPOSITORY_ID,
            "full_name": REPOSITORY,
            "default_branch": "main",
            "owner": {"id": OWNER_ID, "login": "g5n-dev", "type": "User"},
        },
        ("GET", f"{prefix}/git/ref/heads/main"): {"object": {"sha": MAIN_SHA}},
        ("GET", f"{prefix}/actions/permissions/workflow"): {
            "default_workflow_permissions": "write",
            "can_approve_pull_request_reviews": True,
        },
        (
            "GET",
            f"{prefix}/rulesets?includes_parents=false&per_page=100&page=1",
        ): summaries,
        ("GET", f"{prefix}/environments?per_page=100&page=1"): {
            "total_count": len(environment_items),
            "environments": environment_items,
        },
    }
    if immutable is not None:
        responses[("GET", f"{prefix}/immutable-releases")] = immutable
    for detail in details:
        responses[("GET", f"{prefix}/rulesets/{detail['id']}")] = detail
    for environment in environment_items:
        policy = environment.get("deployment_branch_policy")
        if isinstance(policy, dict) and policy.get("custom_branch_policies") is True:
            name = environment["name"]
            responses[
                (
                    "GET",
                    f"{prefix}/environments/{name}/deployment-branch-policies"
                    "?per_page=100&page=1",
                )
            ] = {"total_count": 0, "branch_policies": []}
    return responses


def _expected_config() -> dict[str, object]:
    path = Path(__file__).parents[1] / "config" / "github-hardening.expected.json"
    return load_expected_config(path, owner_id=OWNER_ID)


def _snapshot(api: FakeGitHubApi | None = None) -> tuple[FakeGitHubApi, dict[str, object]]:
    client = api or FakeGitHubApi(_base_responses())
    return client, collect_snapshot(client, REPOSITORY)


def _managed_ruleset(name: str, ruleset_id: int) -> dict[str, object]:
    rulesets = _expected_config()["rulesets"]
    assert isinstance(rulesets, list)
    body = next(item for item in rulesets if isinstance(item, dict) and item["name"] == name)
    return {
        "id": ruleset_id,
        "source_type": "Repository",
        "source": REPOSITORY,
        **copy.deepcopy(body),
    }


def test_expected_configuration_encodes_the_repository_security_contract() -> None:
    expected = _expected_config()

    assert expected["api_version"] == API_VERSION == "2026-03-10"
    assert expected["actions"] == {
        "default_workflow_permissions": "read",
        "can_approve_pull_request_reviews": False,
    }
    assert expected["immutable_releases"] == {"enabled": True}

    rulesets = {item["name"]: item for item in expected["rulesets"]}  # type: ignore[index]
    main_rules = rulesets["ai-stack/main-protection-v1"]["rules"]
    assert {rule["type"] for rule in main_rules} == {
        "deletion",
        "non_fast_forward",
        "pull_request",
        "required_status_checks",
    }
    status_rule = next(rule for rule in main_rules if rule["type"] == "required_status_checks")
    contexts = status_rule["parameters"]["required_status_checks"]
    assert [check["context"] for check in contexts] == [
        "Unit Tests",
        "browser-e2e",
        "static-site",
    ]

    data_rules = rulesets["ai-stack/data-branches-v1"]
    assert data_rules["conditions"]["ref_name"]["include"] == [
        "refs/heads/content",
        "refs/heads/ops",
    ]
    assert {rule["type"] for rule in data_rules["rules"]} == {
        "deletion",
        "non_fast_forward",
        "required_linear_history",
    }

    backup_rules = rulesets["ai-stack/backup-tags-v1"]
    assert backup_rules["target"] == "tag"
    assert {rule["type"] for rule in backup_rules["rules"]} == {"deletion", "update"}

    environments = {item["name"]: item for item in expected["environments"]}  # type: ignore[index]
    assert set(environments) == {"github-pages", "production-publish", "data-deletion"}
    assert environments["data-deletion"]["reviewers"] == [
        {"type": "User", "id": OWNER_ID}
    ]
    assert all(
        environment["deployment_branch_policies"] == [{"name": "main", "type": "branch"}]
        for environment in environments.values()
    )


def test_collect_snapshot_is_canonical_and_treats_immutable_404_as_disabled() -> None:
    unknown_a = {
        "id": 41,
        "name": "user-owned-rule",
        "source_type": "Repository",
        "source": REPOSITORY,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {"ref_name": {"include": ["refs/heads/z"], "exclude": []}},
        "rules": [{"type": "deletion"}],
    }
    unknown_b = {**copy.deepcopy(unknown_a), "id": 40, "name": "another-user-rule"}
    summaries = [
        {"id": unknown_a["id"], "name": unknown_a["name"]},
        {"id": unknown_b["id"], "name": unknown_b["name"]},
    ]
    first = FakeGitHubApi(
        _base_responses(
            ruleset_summaries=summaries,
            ruleset_details=[unknown_a, unknown_b],
        )
    )
    second = FakeGitHubApi(
        _base_responses(
            ruleset_summaries=list(reversed(summaries)),
            ruleset_details=[unknown_b, unknown_a],
        )
    )

    first_snapshot = collect_snapshot(first, REPOSITORY)
    second_snapshot = collect_snapshot(second, REPOSITORY)

    assert first_snapshot == second_snapshot
    assert snapshot_digest(first_snapshot) == snapshot_digest(second_snapshot)
    assert first_snapshot["immutable_releases"] == {
        "enabled": False,
        "enforced_by_owner": False,
    }


def test_collect_snapshot_normalizes_environment_reviewers_and_branch_policies() -> None:
    environment = {
        "id": 501,
        "name": "data-deletion",
        "protection_rules": [
            {"id": 1, "type": "wait_timer", "wait_timer": 10},
            {
                "id": 2,
                "type": "required_reviewers",
                "prevent_self_review": True,
                "reviewers": [
                    {"type": "User", "reviewer": {"id": OWNER_ID, "login": "g5n-dev"}},
                    {"type": "Team", "reviewer": {"id": 999, "name": "security"}},
                ],
            },
        ],
        "deployment_branch_policy": {
            "protected_branches": False,
            "custom_branch_policies": True,
        },
    }
    responses = _base_responses(environments=[environment])
    endpoint = (
        f"/repos/{REPOSITORY}/environments/data-deletion/deployment-branch-policies"
        "?per_page=100&page=1"
    )
    responses[("GET", endpoint)] = {
        "total_count": 2,
        "branch_policies": [
            {"id": 12, "name": "release/*", "type": "branch"},
            {"id": 11, "name": "main"},
        ],
    }

    snapshot = collect_snapshot(FakeGitHubApi(responses), REPOSITORY)
    environments = snapshot["environments"]
    assert isinstance(environments, list)
    assert environments == [
        {
            "name": "data-deletion",
            "wait_timer": 10,
            "prevent_self_review": True,
            "reviewers": [
                {"id": OWNER_ID, "type": "User"},
                {"id": 999, "type": "Team"},
            ],
            "deployment_branch_policy": {
                "protected_branches": False,
                "custom_branch_policies": True,
            },
            "deployment_branch_policies": [
                {"id": 11, "name": "main", "type": "branch"},
                {"id": 12, "name": "release/*", "type": "branch"},
            ],
        }
    ]


def test_gh_cli_adapter_uses_stdin_and_never_exposes_failure_stderr(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[list[str], str | None]] = []

    def successful_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        raw_input = kwargs.get("input")
        calls.append((command, raw_input if isinstance(raw_input, str) else None))
        return subprocess.CompletedProcess(command, 0, '{"ok":true}', "")

    monkeypatch.setattr(subprocess, "run", successful_run)
    api = GhCliApi()

    assert api.request("put", "/repos/g5n-dev/ai-stack/example", {"b": 2, "a": 1}) == {
        "ok": True
    }
    command, body = calls[0]
    assert command[:4] == ["gh", "api", "--method", "PUT"]
    assert command[-2:] == ["--input", "-"]
    assert body == canonical_json({"a": 1, "b": 2})

    secret = "credential-sentinel-that-must-not-be-printed"

    def failed_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 1, "", f"failure {secret} (HTTP 500)")

    monkeypatch.setattr(subprocess, "run", failed_run)
    with pytest.raises(GitHubApiError) as failure:
        api.request("GET", "/repos/g5n-dev/ai-stack")
    assert secret not in str(failure.value)


def test_gh_cli_adapter_handles_no_content_404_and_invalid_responses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api = GhCliApi()

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(command, 0, "", ""),
    )
    assert api.request("PUT", "/repos/g5n-dev/ai-stack/immutable-releases") is None

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(
            command, 1, '{"message":"Not Found"}', "gh: Not Found (HTTP 404)"
        ),
    )
    assert (
        api.request(
            "GET",
            "/repos/g5n-dev/ai-stack/immutable-releases",
            allow_not_found=True,
        )
        is None
    )

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(command, 0, "not-json", ""),
    )
    with pytest.raises(GitHubApiError, match="invalid JSON"):
        api.request("GET", "/repos/g5n-dev/ai-stack")

    with pytest.raises(GitHubApiError, match="unsupported"):
        api.request("DELETE", "/repos/g5n-dev/ai-stack")
    with pytest.raises(GitHubApiError, match="unsafe"):
        api.request("GET", "https://api.github.com/repos/g5n-dev/ai-stack")


def test_plan_is_canonical_preserves_unknown_rulesets_and_never_deletes() -> None:
    unknown = {
        "id": 77,
        "name": "keep-me",
        "source_type": "Repository",
        "source": REPOSITORY,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {"ref_name": {"include": ["refs/heads/release/*"], "exclude": []}},
        "rules": [{"type": "required_signatures"}],
    }
    api = FakeGitHubApi(
        _base_responses(
            ruleset_summaries=[{"id": 77, "name": "keep-me"}],
            ruleset_details=[unknown],
        )
    )
    snapshot = collect_snapshot(api, REPOSITORY)

    plan = build_plan(snapshot, _expected_config())
    operations = plan["operations"]
    assert isinstance(operations, list)

    assert plan["unmanaged_rulesets"] == [
        {"id": 77, "name": "keep-me", "target": "branch", "enforcement": "active"}
    ]
    assert all(operation["method"] != "DELETE" for operation in operations)
    assert [operation["id"] for operation in operations] == sorted(
        operation["id"] for operation in operations
    )
    assert {operation["id"] for operation in operations} >= {
        "actions/default-workflow-permissions",
        "environment/data-deletion",
        "environment/github-pages",
        "environment/production-publish",
        "immutable-releases/enable",
        "ruleset/ai-stack/backup-tags-v1",
        "ruleset/ai-stack/data-branches-v1",
        "ruleset/ai-stack/main-protection-v1",
    }
    assert all("keep-me" not in operation["endpoint"] for operation in operations)
    assert json.dumps(plan, sort_keys=True, separators=(",", ":")) == json.dumps(
        build_plan(snapshot, _expected_config()),
        sort_keys=True,
        separators=(",", ":"),
    )


def test_unapproved_managed_environment_policy_is_reported_and_blocks_apply() -> None:
    environment = {
        "id": 501,
        "name": "production-publish",
        "protection_rules": [],
        "deployment_branch_policy": {
            "protected_branches": False,
            "custom_branch_policies": True,
        },
    }
    responses = _base_responses(environments=[environment])
    policies_endpoint = (
        f"/repos/{REPOSITORY}/environments/production-publish/deployment-branch-policies"
        "?per_page=100&page=1"
    )
    responses[("GET", policies_endpoint)] = {
        "total_count": 2,
        "branch_policies": [
            {"id": 1, "name": "main", "type": "branch"},
            {"id": 2, "name": "release/*", "type": "branch"},
        ],
    }
    api = FakeGitHubApi(responses)
    snapshot = collect_snapshot(api, REPOSITORY)
    plan = build_plan(snapshot, _expected_config())

    assert plan["unmanaged_environment_policies"] == [
        {
            "environment": "production-publish",
            "id": 2,
            "name": "release/*",
            "type": "branch",
        }
    ]

    api.calls.clear()
    with pytest.raises(GitHubHardeningError, match="unapproved deployment branch policies"):
        apply_hardening(
            api=api,
            repository=REPOSITORY,
            expected=_expected_config(),
            expected_full_name=REPOSITORY,
            expected_repository_id=REPOSITORY_ID,
            expected_main_sha=MAIN_SHA,
            expected_snapshot_digest=snapshot_digest(snapshot),
        )
    assert api.writes == []


def test_named_rulesets_are_idempotently_updated_or_created_without_touching_others() -> None:
    exact = _managed_ruleset("ai-stack/main-protection-v1", 10)
    stale = _managed_ruleset("ai-stack/data-branches-v1", 11)
    stale["enforcement"] = "disabled"
    summaries = [
        {"id": exact["id"], "name": exact["name"]},
        {"id": stale["id"], "name": stale["name"]},
    ]
    api = FakeGitHubApi(
        _base_responses(
            ruleset_summaries=summaries,
            ruleset_details=[exact, stale],
            immutable={"enabled": True, "enforced_by_owner": False},
        )
    )
    snapshot = collect_snapshot(api, REPOSITORY)

    operations = build_plan(snapshot, _expected_config())["operations"]
    assert isinstance(operations, list)
    ruleset_operations = [item for item in operations if item["id"].startswith("ruleset/")]

    assert {item["id"] for item in ruleset_operations} == {
        "ruleset/ai-stack/backup-tags-v1",
        "ruleset/ai-stack/data-branches-v1",
    }
    stale_update = next(item for item in ruleset_operations if "data-branches" in item["id"])
    assert stale_update["method"] == "PUT"
    assert stale_update["endpoint"].endswith("/rulesets/11")
    backup_create = next(item for item in ruleset_operations if "backup-tags" in item["id"])
    assert backup_create["method"] == "POST"
    assert backup_create["endpoint"].endswith("/rulesets")


def test_duplicate_managed_ruleset_names_fail_closed() -> None:
    first = _managed_ruleset("ai-stack/main-protection-v1", 10)
    second = _managed_ruleset("ai-stack/main-protection-v1", 11)
    summaries = [
        {"id": first["id"], "name": first["name"]},
        {"id": second["id"], "name": second["name"]},
    ]
    api = FakeGitHubApi(
        _base_responses(
            ruleset_summaries=summaries,
            ruleset_details=[first, second],
        )
    )

    with pytest.raises(GitHubHardeningError, match="duplicate managed ruleset"):
        build_plan(collect_snapshot(api, REPOSITORY), _expected_config())


@pytest.mark.parametrize(
    ("override", "message"),
    [
        ({"expected_full_name": "attacker/fork"}, "full name"),
        ({"expected_repository_id": REPOSITORY_ID + 1}, "repository id"),
        ({"expected_main_sha": "b" * 40}, "main SHA"),
        ({"expected_snapshot_digest": "0" * 64}, "snapshot digest"),
    ],
)
def test_apply_requires_all_concurrent_identity_guards_before_any_write(
    override: dict[str, object],
    message: str,
) -> None:
    api, snapshot = _snapshot()
    arguments: dict[str, Any] = {
        "api": api,
        "repository": REPOSITORY,
        "expected": _expected_config(),
        "expected_full_name": REPOSITORY,
        "expected_repository_id": REPOSITORY_ID,
        "expected_main_sha": MAIN_SHA,
        "expected_snapshot_digest": snapshot_digest(snapshot),
    }
    arguments.update(override)
    api.calls.clear()

    with pytest.raises(GitHubHardeningError, match=message):
        apply_hardening(**arguments)

    assert api.writes == []


def test_apply_uses_only_planned_put_and_post_requests_after_all_guards_match() -> None:
    api, snapshot = _snapshot()
    api.calls.clear()

    result = apply_hardening(
        api=api,
        repository=REPOSITORY,
        expected=_expected_config(),
        expected_full_name=REPOSITORY,
        expected_repository_id=REPOSITORY_ID,
        expected_main_sha=MAIN_SHA,
        expected_snapshot_digest=snapshot_digest(snapshot),
    )

    assert result["status"] == "applied"
    assert result["operation_count"] == len(api.writes) > 0
    assert {method for method, _, _ in api.writes} <= {"PUT", "POST"}
    assert all(
        body is not None or endpoint.endswith("/immutable-releases")
        for _, endpoint, body in api.writes
    )


def test_cli_is_dry_run_by_default_and_apply_requires_every_guard(
    capsys: pytest.CaptureFixture[str],
) -> None:
    dry_api = FakeGitHubApi(_base_responses())

    assert main(["--repository", REPOSITORY], api=dry_api) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["mode"] == "dry-run"
    assert dry_api.writes == []

    apply_api = FakeGitHubApi(_base_responses())
    assert main(["--repository", REPOSITORY, "--apply"], api=apply_api) == 2
    error = capsys.readouterr().err
    assert "all four expected repository guards" in error
    assert apply_api.writes == []


def test_api_and_schema_errors_fail_closed_without_exposing_tokens(
    capsys: pytest.CaptureFixture[str],
) -> None:
    secret = "credential-sentinel-value"
    failing = FakeGitHubApi(_base_responses())
    failing.responses[("GET", f"/repos/{REPOSITORY}")] = GitHubApiError(
        "GitHub API request failed"
    )

    assert main(["--repository", REPOSITORY], api=failing) == 2
    output = capsys.readouterr()
    assert secret not in output.out + output.err
    assert "GitHub API request failed" in output.err

    malformed = FakeGitHubApi(_base_responses())
    malformed.responses[("GET", f"/repos/{REPOSITORY}")] = {
        "id": "not-an-integer",
        "full_name": REPOSITORY,
    }
    with pytest.raises(GitHubHardeningError, match="repository metadata"):
        collect_snapshot(malformed, REPOSITORY)


def test_documentation_states_github_token_writer_identity_limit() -> None:
    root = Path(__file__).parents[1]
    document = (root / "docs" / "operations" / "github-hardening.md").read_text(
        encoding="utf-8"
    )

    assert "同一个 `GITHUB_TOKEN`" in document
    assert "job 级 writer identity" in document
    assert "GitHub App" in document
    assert "--apply" in document
    assert "--expected-snapshot-digest" in document
