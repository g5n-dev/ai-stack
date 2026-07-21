"""Auditable, fail-closed GitHub repository hardening.

The command is a read-only planner unless ``--apply`` is explicitly supplied
together with four independently checked repository identity guards.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Protocol, cast
from urllib.parse import quote

API_VERSION = "2026-03-10"
EXPECTED_SCHEMA = "github_hardening_expected_v1"
SNAPSHOT_SCHEMA = "github_hardening_snapshot_v1"
PLAN_SCHEMA = "github_hardening_plan_v1"

_REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_HTTP_STATUS = re.compile(r"\bHTTP\s+([1-5][0-9]{2})\b")
_MANAGED_RULESETS = frozenset(
    {
        "ai-stack/main-protection-v1",
        "ai-stack/data-branches-v1",
        "ai-stack/backup-tags-v1",
    }
)
_MANAGED_ENVIRONMENTS = frozenset(
    {"github-pages", "production-publish", "data-deletion", "production-recovery"}
)


class GitHubHardeningError(RuntimeError):
    """Raised before or during hardening when an invariant is not satisfied."""


class GitHubApiError(GitHubHardeningError):
    """Raised for a GitHub API transport or response failure."""


class GitHubApi(Protocol):
    """Small injectable API surface used by the planner and tests."""

    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
        *,
        allow_not_found: bool = False,
    ) -> object | None: ...


class GhCliApi:
    """GitHub REST adapter that never places credentials in argv or output."""

    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
        *,
        allow_not_found: bool = False,
    ) -> object | None:
        normalized_method = method.upper()
        if normalized_method not in {"GET", "PUT", "POST"}:
            raise GitHubApiError("unsupported GitHub API method")
        if not endpoint.startswith("/") or any(ord(char) < 32 for char in endpoint):
            raise GitHubApiError("unsafe GitHub API endpoint")

        command = [
            "gh",
            "api",
            "--method",
            normalized_method,
            "--header",
            "Accept: application/vnd.github+json",
            "--header",
            f"X-GitHub-Api-Version: {API_VERSION}",
            endpoint,
        ]
        encoded_body: str | None = None
        if body is not None:
            command.extend(["--input", "-"])
            encoded_body = canonical_json(body)
        attempts = 3 if normalized_method == "GET" else 1
        completed: subprocess.CompletedProcess[str] | None = None
        failure_status: int | None = None
        for attempt in range(attempts):
            try:
                completed = subprocess.run(
                    command,
                    input=encoded_body,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
            except subprocess.TimeoutExpired:
                completed = None
            except OSError as exc:
                raise GitHubApiError("GitHub CLI could not be executed") from exc
            if completed is not None and completed.returncode == 0:
                break
            if completed is not None:
                match = _HTTP_STATUS.search(completed.stderr)
                failure_status = int(match.group(1)) if match is not None else None
                if allow_not_found and failure_status == 404:
                    return None
                # Retrying validation/authentication errors cannot make the request
                # valid and can multiply a state-changing mistake. Only transient
                # failures (including 429) remain eligible for the bounded GET retry.
                if (
                    failure_status is not None
                    and 400 <= failure_status < 500
                    and failure_status != 429
                ):
                    break
            if attempt + 1 < attempts:
                time.sleep(attempt + 1)
        if completed is None:
            raise GitHubApiError(
                f"GitHub API request timed out ({normalized_method} {endpoint})"
            )
        if completed.returncode != 0:
            # Do not forward stderr: credential helpers and proxies are outside our
            # trust boundary and may include sensitive request metadata.
            status_suffix = (
                f"; HTTP {failure_status}" if failure_status is not None else ""
            )
            raise GitHubApiError(
                "GitHub API request failed "
                f"({normalized_method} {endpoint}{status_suffix})"
            )
        if not completed.stdout.strip():
            return None
        try:
            decoded: object = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise GitHubApiError("GitHub API returned invalid JSON") from exc
        _normalize_json(decoded, "GitHub API response")
        return decoded


def canonical_json(value: object) -> str:
    """Return the canonical JSON representation used by every digest."""

    normalized = _normalize_json(value, "canonical JSON value")
    return json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _normalize_json(value: object, label: str) -> object:
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, list):
        return [_normalize_json(item, label) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise GitHubHardeningError(f"{label} contains a non-string object key")
        typed = cast(dict[str, object], value)
        return {key: _normalize_json(typed[key], label) for key in sorted(typed)}
    raise GitHubHardeningError(f"{label} contains a non-JSON value")


def _unordered_json(value: object, label: str) -> object:
    """Canonicalize API arrays whose order has no configuration meaning."""

    normalized = _normalize_json(value, label)
    if isinstance(normalized, list):
        items = [_unordered_json(item, label) for item in normalized]
        return sorted(items, key=canonical_json)
    if isinstance(normalized, dict):
        typed = cast(dict[str, object], normalized)
        return {key: _unordered_json(typed[key], label) for key in sorted(typed)}
    return normalized


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise GitHubHardeningError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _array(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise GitHubHardeningError(f"{label} must be an array")
    return cast(list[object], value)


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise GitHubHardeningError(f"{label} must be a non-empty string")
    return value


def _integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise GitHubHardeningError(f"{label} must be a positive integer")
    return value


def _boolean(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise GitHubHardeningError(f"{label} must be a boolean")
    return value


def _validate_repository_name(repository: str) -> str:
    if not _REPOSITORY.fullmatch(repository) or ".." in repository:
        raise GitHubHardeningError("repository must be a safe owner/name pair")
    return repository


def _paginated(
    api: GitHubApi,
    endpoint: str,
    *,
    response_key: str | None = None,
) -> list[object]:
    collected: list[object] = []
    for page in range(1, 101):
        separator = "&" if "?" in endpoint else "?"
        response = api.request("GET", f"{endpoint}{separator}per_page=100&page={page}")
        if response_key is None:
            items = _array(response, f"paginated response for {endpoint}")
        else:
            wrapper = _object(response, f"paginated response for {endpoint}")
            items = _array(wrapper.get(response_key), f"{endpoint} {response_key}")
        collected.extend(items)
        if len(items) < 100:
            return collected
    raise GitHubHardeningError(f"pagination limit exceeded for {endpoint}")


def _ruleset_body(value: object, *, require_visible_bypass: bool) -> dict[str, object]:
    payload = _object(value, "ruleset")
    name = _string(payload.get("name"), "ruleset name")
    target = _string(payload.get("target"), f"ruleset {name} target")
    enforcement = _string(payload.get("enforcement"), f"ruleset {name} enforcement")
    if target not in {"branch", "tag", "push"}:
        raise GitHubHardeningError(f"ruleset {name} has an unsupported target")
    if enforcement not in {"active", "disabled", "evaluate"}:
        raise GitHubHardeningError(f"ruleset {name} has invalid enforcement")
    conditions = _object(payload.get("conditions"), f"ruleset {name} conditions")
    ref_name = _object(conditions.get("ref_name"), f"ruleset {name} ref condition")
    for key in ("include", "exclude"):
        values = _array(ref_name.get(key), f"ruleset {name} ref {key}")
        if not all(isinstance(item, str) for item in values):
            raise GitHubHardeningError(f"ruleset {name} ref {key} must contain strings")
    rules = _array(payload.get("rules"), f"ruleset {name} rules")
    normalized_rules: list[dict[str, object]] = []
    for rule in rules:
        rule_object = _object(rule, f"ruleset {name} rule")
        rule_type = _string(rule_object.get("type"), f"ruleset {name} rule type")
        normalized_rule = copy.deepcopy(rule_object)
        if (
            name == "ai-stack/backup-tags-v1"
            and target == "tag"
            and rule_type == "update"
        ):
            parameters_raw = normalized_rule.get("parameters")
            if parameters_raw is None:
                parameters: dict[str, object] = {}
            else:
                parameters = _object(
                    parameters_raw,
                    f"ruleset {name} update parameters",
                )
            if frozenset(parameters) - {"update_allows_fetch_and_merge"}:
                raise GitHubHardeningError(
                    f"ruleset {name} update parameters are unsupported"
                )
            allows_fetch_and_merge = parameters.get(
                "update_allows_fetch_and_merge",
                False,
            )
            if not isinstance(allows_fetch_and_merge, bool):
                raise GitHubHardeningError(
                    f"ruleset {name} update permission must be a boolean"
                )
            if allows_fetch_and_merge:
                raise GitHubHardeningError(
                    f"ruleset {name} must not allow fetch and merge"
                )
            # GitHub may omit this false-valued parameter in responses. Both forms
            # mean that the protected tag cannot move and share one canonical form.
            normalized_rule = {"type": "update"}
        normalized_rules.append(normalized_rule)

    if "bypass_actors" not in payload:
        if require_visible_bypass:
            raise GitHubHardeningError(
                f"managed ruleset {name} did not expose bypass actors; refusing update"
            )
        bypass: object = None
    else:
        bypass = _array(payload["bypass_actors"], f"ruleset {name} bypass actors")

    body: dict[str, object] = {
        "name": name,
        "target": target,
        "enforcement": enforcement,
        "bypass_actors": bypass,
        "conditions": conditions,
        "rules": normalized_rules,
    }
    normalized = _unordered_json(body, f"ruleset {name}")
    return _object(normalized, f"normalized ruleset {name}")


def _snapshot_ruleset(value: object) -> dict[str, object]:
    payload = _object(value, "repository ruleset")
    body = _ruleset_body(payload, require_visible_bypass=False)
    body["id"] = _integer(payload.get("id"), "ruleset id")
    body["source_type"] = _string(payload.get("source_type"), "ruleset source type")
    body["source"] = _string(payload.get("source"), "ruleset source")
    return body


def _normalize_reviewer(value: object, label: str) -> dict[str, object]:
    reviewer = _object(value, label)
    reviewer_type = _string(reviewer.get("type"), f"{label} type")
    if reviewer_type not in {"User", "Team"}:
        raise GitHubHardeningError(f"{label} type is invalid")
    if "reviewer" in reviewer:
        nested = _object(reviewer["reviewer"], f"{label} identity")
        reviewer_id = _integer(nested.get("id"), f"{label} id")
    else:
        reviewer_id = _integer(reviewer.get("id"), f"{label} id")
    return {"type": reviewer_type, "id": reviewer_id}


def _snapshot_environment(
    api: GitHubApi,
    repository: str,
    value: object,
) -> dict[str, object]:
    payload = _object(value, "environment")
    name = _string(payload.get("name"), "environment name")
    protection_rules = _array(payload.get("protection_rules", []), f"environment {name} rules")
    wait_timer = 0
    prevent_self_review = False
    reviewers: list[object] = []
    for raw_rule in protection_rules:
        rule = _object(raw_rule, f"environment {name} protection rule")
        rule_type = _string(rule.get("type"), f"environment {name} rule type")
        if rule_type == "wait_timer":
            timer = rule.get("wait_timer")
            if isinstance(timer, bool) or not isinstance(timer, int) or not 0 <= timer <= 43_200:
                raise GitHubHardeningError(f"environment {name} wait timer is invalid")
            wait_timer = timer
        elif rule_type == "required_reviewers":
            prevent_self_review = _boolean(
                rule.get("prevent_self_review", False),
                f"environment {name} prevent self review",
            )
            reviewers = [
                _normalize_reviewer(item, f"environment {name} reviewer")
                for item in _array(rule.get("reviewers", []), f"environment {name} reviewers")
            ]

    deployment_policy_raw = payload.get("deployment_branch_policy")
    if deployment_policy_raw is None:
        deployment_policy: object = None
        branch_policies: list[object] = []
    else:
        policy = _object(deployment_policy_raw, f"environment {name} deployment policy")
        protected = _boolean(
            policy.get("protected_branches"),
            f"environment {name} protected branches",
        )
        custom = _boolean(
            policy.get("custom_branch_policies"),
            f"environment {name} custom branch policies",
        )
        if protected == custom:
            raise GitHubHardeningError(f"environment {name} deployment policy is invalid")
        deployment_policy = {
            "protected_branches": protected,
            "custom_branch_policies": custom,
        }
        branch_policies = []
        if custom:
            encoded = quote(name, safe="")
            raw_policies = _paginated(
                api,
                f"/repos/{repository}/environments/{encoded}/deployment-branch-policies",
                response_key="branch_policies",
            )
            for raw_policy in raw_policies:
                branch_policy = _object(raw_policy, f"environment {name} branch policy")
                policy_name = _string(
                    branch_policy.get("name"),
                    f"environment {name} branch policy name",
                )
                policy_type = branch_policy.get("type", "branch")
                if policy_type not in {"branch", "tag"}:
                    raise GitHubHardeningError(
                        f"environment {name} branch policy type is invalid"
                    )
                branch_policies.append(
                    {
                        "id": _integer(
                            branch_policy.get("id"),
                            f"environment {name} branch policy id",
                        ),
                        "name": policy_name,
                        "type": policy_type,
                    }
                )

    normalized = _unordered_json(
        {
            "name": name,
            "wait_timer": wait_timer,
            "prevent_self_review": prevent_self_review,
            "reviewers": reviewers,
            "deployment_branch_policy": deployment_policy,
            "deployment_branch_policies": branch_policies,
        },
        f"environment {name}",
    )
    return _object(normalized, f"normalized environment {name}")


def collect_snapshot(api: GitHubApi, repository: str) -> dict[str, object]:
    """Read and canonicalize all settings relevant to the hardening plan."""

    requested_repository = _validate_repository_name(repository)
    prefix = f"/repos/{requested_repository}"
    metadata = _object(api.request("GET", prefix), "repository metadata")
    try:
        repository_id = _integer(metadata.get("id"), "repository metadata id")
        full_name = _string(metadata.get("full_name"), "repository metadata full name")
        default_branch = _string(
            metadata.get("default_branch"),
            "repository metadata default branch",
        )
        owner = _object(metadata.get("owner"), "repository metadata owner")
        owner_id = _integer(owner.get("id"), "repository metadata owner id")
        owner_login = _string(owner.get("login"), "repository metadata owner login")
        owner_type = _string(owner.get("type"), "repository metadata owner type")
    except GitHubHardeningError as exc:
        raise GitHubHardeningError(f"repository metadata is invalid: {exc}") from exc
    if full_name.lower() != requested_repository.lower():
        raise GitHubHardeningError("repository metadata full name does not match request")
    if default_branch != "main":
        raise GitHubHardeningError("repository default branch must be main")

    reference = _object(
        api.request("GET", f"{prefix}/git/ref/heads/main"),
        "main reference",
    )
    reference_object = _object(reference.get("object"), "main reference object")
    main_sha = _string(reference_object.get("sha"), "main reference SHA")
    if not _OBJECT_ID.fullmatch(main_sha):
        raise GitHubHardeningError("main reference SHA is not a full Git object ID")

    actions_raw = _object(
        api.request("GET", f"{prefix}/actions/permissions/workflow"),
        "Actions workflow permissions",
    )
    actions = {
        "default_workflow_permissions": _string(
            actions_raw.get("default_workflow_permissions"),
            "default workflow permissions",
        ),
        "can_approve_pull_request_reviews": _boolean(
            actions_raw.get("can_approve_pull_request_reviews"),
            "Actions PR approval permission",
        ),
    }
    if actions["default_workflow_permissions"] not in {"read", "write"}:
        raise GitHubHardeningError("default workflow permissions are invalid")

    immutable_raw = api.request(
        "GET",
        f"{prefix}/immutable-releases",
        allow_not_found=True,
    )
    if immutable_raw is None:
        immutable: dict[str, object] = {
            "enabled": False,
            "enforced_by_owner": False,
        }
    else:
        immutable_object = _object(immutable_raw, "immutable releases response")
        immutable = {
            "enabled": _boolean(
                immutable_object.get("enabled"),
                "immutable releases enabled",
            ),
            "enforced_by_owner": _boolean(
                immutable_object.get("enforced_by_owner"),
                "immutable releases owner enforcement",
            ),
        }

    summaries = _paginated(
        api,
        f"{prefix}/rulesets?includes_parents=false",
    )
    rulesets: list[dict[str, object]] = []
    seen_ruleset_ids: set[int] = set()
    for summary_raw in summaries:
        summary = _object(summary_raw, "ruleset summary")
        ruleset_id = _integer(summary.get("id"), "ruleset summary id")
        if ruleset_id in seen_ruleset_ids:
            raise GitHubHardeningError("duplicate ruleset id in GitHub response")
        seen_ruleset_ids.add(ruleset_id)
        detail = _snapshot_ruleset(api.request("GET", f"{prefix}/rulesets/{ruleset_id}"))
        if detail["id"] != ruleset_id:
            raise GitHubHardeningError("ruleset detail id does not match summary")
        rulesets.append(detail)
    rulesets.sort(key=lambda item: (_string(item["name"], "ruleset name"), cast(int, item["id"])))

    raw_environments = _paginated(api, f"{prefix}/environments", response_key="environments")
    environments = [
        _snapshot_environment(api, requested_repository, environment)
        for environment in raw_environments
    ]
    names = [_string(item["name"], "environment name") for item in environments]
    if len(names) != len(set(names)):
        raise GitHubHardeningError("duplicate environment name in GitHub response")
    environments.sort(key=lambda item: _string(item["name"], "environment name"))

    snapshot: dict[str, object] = {
        "schema_version": SNAPSHOT_SCHEMA,
        "api_version": API_VERSION,
        "repository": {
            "id": repository_id,
            "full_name": full_name,
            "default_branch": default_branch,
            "owner": {"id": owner_id, "login": owner_login, "type": owner_type},
        },
        "main_sha": main_sha,
        "actions": actions,
        "immutable_releases": immutable,
        "rulesets": rulesets,
        "environments": environments,
    }
    return _object(_normalize_json(snapshot, "repository snapshot"), "repository snapshot")


def snapshot_digest(snapshot: Mapping[str, object]) -> str:
    """Digest a canonical current-state snapshot for compare-and-set apply."""

    return hashlib.sha256(canonical_json(dict(snapshot)).encode()).hexdigest()


def _load_json_file(path: Path) -> dict[str, object]:
    try:
        details = path.lstat()
        if not path.is_file() or path.is_symlink() or details.st_nlink != 1:
            raise GitHubHardeningError("expected configuration must be a regular file")
        if not 0 < details.st_size <= 1024 * 1024:
            raise GitHubHardeningError("expected configuration size is invalid")
        decoded: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GitHubHardeningError("expected configuration is missing or invalid") from exc
    return _object(decoded, "expected configuration")


def _validate_expected_contract(
    expected: dict[str, object],
    *,
    owner_id: int | None = None,
) -> None:
    if frozenset(expected) != {
        "schema_version",
        "api_version",
        "actions",
        "immutable_releases",
        "rulesets",
        "environments",
    }:
        raise GitHubHardeningError("expected configuration top-level schema is invalid")
    if expected["schema_version"] != EXPECTED_SCHEMA or expected["api_version"] != API_VERSION:
        raise GitHubHardeningError("expected configuration version is unsupported")
    actions = _object(expected["actions"], "expected Actions settings")
    if actions != {
        "default_workflow_permissions": "read",
        "can_approve_pull_request_reviews": True,
    }:
        raise GitHubHardeningError("expected Actions settings do not match the audited contract")
    if _object(expected["immutable_releases"], "expected immutable releases") != {
        "enabled": True
    }:
        raise GitHubHardeningError("immutable releases must be enabled")

    rulesets = _array(expected["rulesets"], "expected rulesets")
    by_name: dict[str, dict[str, object]] = {}
    for raw_ruleset in rulesets:
        normalized = _ruleset_body(raw_ruleset, require_visible_bypass=True)
        name = _string(normalized["name"], "expected ruleset name")
        if name in by_name:
            raise GitHubHardeningError("duplicate expected ruleset name")
        by_name[name] = normalized
    if frozenset(by_name) != _MANAGED_RULESETS:
        raise GitHubHardeningError("expected managed ruleset set is invalid")

    expected_refs = {
        "ai-stack/main-protection-v1": ("branch", ["refs/heads/main"]),
        "ai-stack/data-branches-v1": (
            "branch",
            ["refs/heads/content", "refs/heads/ops"],
        ),
        "ai-stack/backup-tags-v1": (
            "tag",
            ["refs/tags/backup-*", "refs/tags/content-seed-*"],
        ),
    }
    for name, (target, includes) in expected_refs.items():
        ruleset = by_name[name]
        if (
            ruleset["target"] != target
            or ruleset["enforcement"] != "active"
            or ruleset["bypass_actors"] != []
        ):
            raise GitHubHardeningError(f"ruleset {name} target/enforcement/bypass is invalid")
        conditions = _object(ruleset["conditions"], f"ruleset {name} conditions")
        refs = _object(conditions["ref_name"], f"ruleset {name} refs")
        if refs.get("include") != includes or refs.get("exclude") != []:
            raise GitHubHardeningError(f"ruleset {name} ref scope is invalid")

    def rule_types(name: str) -> set[str]:
        rules = _array(by_name[name]["rules"], f"expected {name} rules")
        types = {
            _string(_object(rule, f"expected {name} rule").get("type"), "rule type")
            for rule in rules
        }
        if len(types) != len(rules):
            raise GitHubHardeningError(f"ruleset {name} contains duplicate rules")
        return types

    if rule_types("ai-stack/main-protection-v1") != {
        "deletion",
        "non_fast_forward",
        "pull_request",
        "required_status_checks",
    }:
        raise GitHubHardeningError("main ruleset contract is incomplete")
    if rule_types("ai-stack/data-branches-v1") != {
        "deletion",
        "non_fast_forward",
        "required_linear_history",
    }:
        raise GitHubHardeningError("data branch ruleset contract is incomplete")
    if rule_types("ai-stack/backup-tags-v1") != {"deletion", "update"}:
        raise GitHubHardeningError("backup tag ruleset contract is incomplete")

    main_rules = _array(by_name["ai-stack/main-protection-v1"]["rules"], "main rules")
    status_rule = next(
        (
            _object(rule, "main status rule")
            for rule in main_rules
            if _object(rule, "main rule").get("type") == "required_status_checks"
        ),
        None,
    )
    if status_rule is None:
        raise GitHubHardeningError("main status check rule is missing")
    parameters = _object(status_rule.get("parameters"), "main status parameters")
    checks = _array(parameters.get("required_status_checks"), "main required checks")
    if checks != [{"context": "Unit Tests", "integration_id": 15368}]:
        raise GitHubHardeningError("main stable status check contract is invalid")
    if parameters.get("strict_required_status_checks_policy") is not True:
        raise GitHubHardeningError("main status checks must use the latest main revision")

    pull_request_rule = next(
        _object(rule, "main pull request rule")
        for rule in main_rules
        if _object(rule, "main rule").get("type") == "pull_request"
    )
    pull_request_parameters = _object(
        pull_request_rule.get("parameters"),
        "main pull request parameters",
    )
    if pull_request_parameters != {
        "allowed_merge_methods": ["merge", "squash"],
        "dismiss_stale_reviews_on_push": True,
        "require_code_owner_review": False,
        "require_last_push_approval": False,
        "required_approving_review_count": 0,
        "required_review_thread_resolution": True,
    }:
        raise GitHubHardeningError("main pull request contract is invalid")

    backup_rules = _array(by_name["ai-stack/backup-tags-v1"]["rules"], "backup rules")
    update_rule = next(
        _object(rule, "backup update rule")
        for rule in backup_rules
        if _object(rule, "backup rule").get("type") == "update"
    )
    if update_rule != {"type": "update"}:
        raise GitHubHardeningError("backup tag updates must remain disabled")

    environments = _array(expected["environments"], "expected environments")
    environments_by_name = {
        _string(_object(item, "expected environment").get("name"), "environment name"): _object(
            item, "expected environment"
        )
        for item in environments
    }
    if frozenset(environments_by_name) != _MANAGED_ENVIRONMENTS or len(environments) != len(
        _MANAGED_ENVIRONMENTS
    ):
        raise GitHubHardeningError("expected environment set is invalid")
    expected_policy = {
        "protected_branches": False,
        "custom_branch_policies": True,
    }
    main_branch_policy = [{"name": "main", "type": "branch"}]
    expected_branch_policies = {
        "github-pages": main_branch_policy,
        "production-publish": main_branch_policy,
        "data-deletion": main_branch_policy,
        "production-recovery": main_branch_policy,
    }
    for name, environment in environments_by_name.items():
        if (
            environment.get("wait_timer") != 0
            or environment.get("prevent_self_review") is not False
            or environment.get("deployment_branch_policy") != expected_policy
            or environment.get("deployment_branch_policies")
            != expected_branch_policies[name]
        ):
            raise GitHubHardeningError(f"environment {name} policy is invalid")
    for name in ("github-pages", "production-publish"):
        if environments_by_name[name].get("reviewers") != []:
            raise GitHubHardeningError(f"environment {name} must not require an approver")
    expected_reviewer = [{"id": owner_id, "type": "User"}] if owner_id is not None else None
    for name in ("data-deletion", "production-recovery"):
        reviewers = environments_by_name[name].get("reviewers")
        if not isinstance(reviewers, list) or len(reviewers) != 1:
            raise GitHubHardeningError(
                f"{name} must require one repository owner review"
            )
        reviewer = _object(reviewers[0], f"{name} reviewer")
        if reviewer.get("type") != "User":
            raise GitHubHardeningError(f"{name} reviewer is invalid")
        _integer(reviewer.get("id"), f"{name} reviewer id")
        if expected_reviewer is not None and reviewers != expected_reviewer:
            raise GitHubHardeningError(
                f"{name} reviewer must be the repository owner"
            )


def load_expected_config(path: Path | str, *, owner_id: int) -> dict[str, object]:
    """Load, bind and validate the audited desired-state document."""

    if isinstance(owner_id, bool) or not isinstance(owner_id, int) or owner_id <= 0:
        raise GitHubHardeningError("repository owner id must be a positive integer")
    expected = _load_json_file(Path(path).absolute())
    bound = copy.deepcopy(expected)
    environments = _array(bound.get("environments"), "expected environments")
    for raw_environment in environments:
        environment = _object(raw_environment, "expected environment")
        reviewers = _array(environment.get("reviewers"), "expected environment reviewers")
        for raw_reviewer in reviewers:
            reviewer = _object(raw_reviewer, "expected environment reviewer")
            if reviewer.get("id") == "$REPOSITORY_OWNER_ID":
                reviewer["id"] = owner_id
    normalized = _unordered_json(bound, "expected configuration")
    result = _object(normalized, "normalized expected configuration")
    _validate_expected_contract(result, owner_id=owner_id)
    return result


def _environment_body(value: object) -> dict[str, object]:
    environment = _object(value, "environment configuration")
    return {
        "wait_timer": environment.get("wait_timer"),
        "prevent_self_review": environment.get("prevent_self_review"),
        "reviewers": environment.get("reviewers"),
        "deployment_branch_policy": environment.get("deployment_branch_policy"),
    }


def _operation(
    operation_id: str,
    method: str,
    endpoint: str,
    body: dict[str, object] | None,
) -> dict[str, object]:
    if method not in {"PUT", "POST"}:
        raise GitHubHardeningError("hardening plan attempted a destructive API method")
    return {"id": operation_id, "method": method, "endpoint": endpoint, "body": body}


def build_plan(
    snapshot: Mapping[str, object],
    expected: Mapping[str, object],
) -> dict[str, object]:
    """Build a deterministic, non-destructive update/create plan."""

    current = dict(snapshot)
    desired = dict(expected)
    _validate_expected_contract(desired)
    repository = _object(current.get("repository"), "snapshot repository")
    full_name = _string(repository.get("full_name"), "snapshot repository full name")
    repository_id = _integer(repository.get("id"), "snapshot repository id")
    main_sha = _string(current.get("main_sha"), "snapshot main SHA")
    prefix = f"/repos/{full_name}"
    operations: list[dict[str, object]] = []

    current_actions = _object(current.get("actions"), "snapshot Actions settings")
    desired_actions = _object(desired["actions"], "expected Actions settings")
    if canonical_json(current_actions) != canonical_json(desired_actions):
        operations.append(
            _operation(
                "actions/default-workflow-permissions",
                "PUT",
                f"{prefix}/actions/permissions/workflow",
                desired_actions,
            )
        )

    immutable = _object(current.get("immutable_releases"), "snapshot immutable releases")
    if immutable.get("enabled") is not True:
        operations.append(
            _operation(
                "immutable-releases/enable",
                "PUT",
                f"{prefix}/immutable-releases",
                None,
            )
        )

    current_rulesets = [
        _object(item, "snapshot ruleset")
        for item in _array(current.get("rulesets"), "snapshot rulesets")
    ]
    rulesets_by_name: dict[str, list[dict[str, object]]] = {}
    for ruleset in current_rulesets:
        rulesets_by_name.setdefault(
            _string(ruleset.get("name"), "snapshot ruleset name"), []
        ).append(ruleset)
    unmanaged_rulesets: list[dict[str, object]] = []
    for ruleset in current_rulesets:
        name = _string(ruleset.get("name"), "snapshot ruleset name")
        if name not in _MANAGED_RULESETS:
            unmanaged_rulesets.append(
                {
                    "id": _integer(ruleset.get("id"), "unmanaged ruleset id"),
                    "name": name,
                    "target": _string(ruleset.get("target"), "unmanaged ruleset target"),
                    "enforcement": _string(
                        ruleset.get("enforcement"),
                        "unmanaged ruleset enforcement",
                    ),
                }
            )
    unmanaged_rulesets.sort(key=lambda item: (_string(item["name"], "name"), cast(int, item["id"])))

    for desired_raw in _array(desired["rulesets"], "expected rulesets"):
        desired_ruleset = _ruleset_body(desired_raw, require_visible_bypass=True)
        name = _string(desired_ruleset["name"], "expected ruleset name")
        matches = rulesets_by_name.get(name, [])
        if len(matches) > 1:
            raise GitHubHardeningError(f"duplicate managed ruleset name: {name}")
        if not matches:
            operations.append(
                _operation(f"ruleset/{name}", "POST", f"{prefix}/rulesets", desired_ruleset)
            )
            continue
        existing = matches[0]
        if existing.get("source_type") != "Repository" or existing.get("source") != full_name:
            raise GitHubHardeningError(
                f"managed ruleset {name} is not owned by the target repository"
            )
        existing_body = _ruleset_body(existing, require_visible_bypass=True)
        if canonical_json(existing_body) != canonical_json(desired_ruleset):
            ruleset_id = _integer(existing.get("id"), f"managed ruleset {name} id")
            operations.append(
                _operation(
                    f"ruleset/{name}",
                    "PUT",
                    f"{prefix}/rulesets/{ruleset_id}",
                    desired_ruleset,
                )
            )

    current_environments = {
        _string(environment.get("name"), "snapshot environment name"): environment
        for environment in (
            _object(item, "snapshot environment")
            for item in _array(current.get("environments"), "snapshot environments")
        )
    }
    unmanaged_environment_policies: list[dict[str, object]] = []
    for desired_raw in _array(desired["environments"], "expected environments"):
        desired_environment = _object(desired_raw, "expected environment")
        name = _string(desired_environment.get("name"), "expected environment name")
        encoded_name = quote(name, safe="")
        desired_body = _environment_body(desired_environment)
        existing_environment = current_environments.get(name)
        if existing_environment is None or canonical_json(
            _environment_body(existing_environment)
        ) != canonical_json(desired_body):
            operations.append(
                _operation(
                    f"environment/{name}",
                    "PUT",
                    f"{prefix}/environments/{encoded_name}",
                    desired_body,
                )
            )

        current_policies = (
            []
            if existing_environment is None
            else [
                _object(item, f"environment {name} current branch policy")
                for item in _array(
                    existing_environment.get("deployment_branch_policies", []),
                    f"environment {name} current branch policies",
                )
            ]
        )
        desired_policies = [
            _object(item, f"environment {name} desired branch policy")
            for item in _array(
                desired_environment.get("deployment_branch_policies"),
                f"environment {name} desired branch policies",
            )
        ]
        for current_policy in current_policies:
            if not any(
                current_policy.get("name") == desired_policy.get("name")
                and current_policy.get("type", "branch") == desired_policy.get("type")
                for desired_policy in desired_policies
            ):
                unmanaged_environment_policies.append(
                    {
                        "environment": name,
                        "id": _integer(
                            current_policy.get("id"),
                            f"environment {name} unmanaged branch policy id",
                        ),
                        "name": _string(
                            current_policy.get("name"),
                            f"environment {name} unmanaged branch policy name",
                        ),
                        "type": _string(
                            current_policy.get("type", "branch"),
                            f"environment {name} unmanaged branch policy type",
                        ),
                    }
                )
        for desired_policy in desired_policies:
            policy_name = _string(desired_policy.get("name"), "branch policy name")
            policy_type = _string(desired_policy.get("type"), "branch policy type")
            same_name = [item for item in current_policies if item.get("name") == policy_name]
            if same_name and not any(
                item.get("type", "branch") == policy_type for item in same_name
            ):
                raise GitHubHardeningError(
                    f"environment {name} has a conflicting deployment policy named {policy_name}"
                )
            if not any(
                item.get("name") == policy_name
                and item.get("type", "branch") == policy_type
                for item in current_policies
            ):
                operations.append(
                    _operation(
                        f"environment/{name}/branch-policy/{policy_type}/{policy_name}",
                        "POST",
                        f"{prefix}/environments/{encoded_name}/deployment-branch-policies",
                        {"name": policy_name, "type": policy_type},
                    )
                )

    operations.sort(key=lambda item: _string(item["id"], "operation id"))
    unmanaged_environment_policies.sort(
        key=lambda item: (
            _string(item["environment"], "environment"),
            _string(item["name"], "policy name"),
            cast(int, item["id"]),
        )
    )
    plan: dict[str, object] = {
        "schema_version": PLAN_SCHEMA,
        "api_version": API_VERSION,
        "repository": {
            "id": repository_id,
            "full_name": full_name,
            "main_sha": main_sha,
        },
        "snapshot_sha256": snapshot_digest(current),
        "expected_config_sha256": hashlib.sha256(canonical_json(desired).encode()).hexdigest(),
        "operations": operations,
        "unmanaged_rulesets": unmanaged_rulesets,
        "unmanaged_environment_policies": unmanaged_environment_policies,
    }
    return _object(_normalize_json(plan, "hardening plan"), "hardening plan")


def apply_hardening(
    *,
    api: GitHubApi,
    repository: str,
    expected: Mapping[str, object],
    expected_full_name: str,
    expected_repository_id: int,
    expected_main_sha: str,
    expected_snapshot_digest: str,
) -> dict[str, object]:
    """Apply a plan only after all repository identity/CAS guards match."""

    _validate_repository_name(expected_full_name)
    _integer(expected_repository_id, "expected repository id")
    if not _OBJECT_ID.fullmatch(expected_main_sha):
        raise GitHubHardeningError("expected main SHA must be a full Git object ID")
    if not _DIGEST.fullmatch(expected_snapshot_digest):
        raise GitHubHardeningError("expected snapshot digest must be a SHA-256 digest")

    snapshot = collect_snapshot(api, repository)
    identity = _object(snapshot["repository"], "snapshot repository")
    actual_full_name = _string(identity.get("full_name"), "snapshot full name")
    actual_repository_id = _integer(identity.get("id"), "snapshot repository id")
    actual_main_sha = _string(snapshot.get("main_sha"), "snapshot main SHA")
    actual_digest = snapshot_digest(snapshot)
    if actual_full_name != expected_full_name:
        raise GitHubHardeningError("repository full name guard mismatch")
    if actual_repository_id != expected_repository_id:
        raise GitHubHardeningError("repository id guard mismatch")
    if actual_main_sha != expected_main_sha:
        raise GitHubHardeningError("main SHA guard mismatch")
    if actual_digest != expected_snapshot_digest:
        raise GitHubHardeningError("snapshot digest guard mismatch")

    plan = build_plan(snapshot, expected)
    operations = _array(plan["operations"], "hardening plan operations")
    unmanaged_environment_policies = _array(
        plan["unmanaged_environment_policies"],
        "unmanaged environment policies",
    )
    if unmanaged_environment_policies:
        raise GitHubHardeningError(
            "managed environments contain unapproved deployment branch policies; "
            "review and remove them manually before apply"
        )
    for raw_operation in operations:
        operation = _object(raw_operation, "hardening operation")
        operation_id = _string(operation.get("id"), "hardening operation id")
        method = _string(operation.get("method"), f"operation {operation_id} method")
        endpoint = _string(operation.get("endpoint"), f"operation {operation_id} endpoint")
        body_raw = operation.get("body")
        body = None if body_raw is None else _object(body_raw, f"operation {operation_id} body")
        if method not in {"PUT", "POST"} or not endpoint.startswith(
            f"/repos/{actual_full_name}/"
        ):
            raise GitHubHardeningError("hardening operation escaped the approved repository")
        api.request(method, endpoint, body)

    return {
        "schema_version": "github_hardening_apply_result_v1",
        "status": "applied",
        "repository": actual_full_name,
        "repository_id": actual_repository_id,
        "main_sha": actual_main_sha,
        "snapshot_sha256": actual_digest,
        "operation_count": len(operations),
        "operation_ids": [
            _string(_object(operation, "operation").get("id"), "operation id")
            for operation in operations
        ],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan or explicitly apply fail-closed GitHub repository hardening"
    )
    parser.add_argument("--repository", required=True, help="exact owner/repository name")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "config"
        / "github-hardening.expected.json",
        help="audited expected-state JSON",
    )
    parser.add_argument("--apply", action="store_true", help="perform planned PUT/POST calls")
    parser.add_argument("--expected-full-name")
    parser.add_argument("--expected-repository-id", type=int)
    parser.add_argument("--expected-main-sha")
    parser.add_argument("--expected-snapshot-digest")
    return parser


def main(argv: Sequence[str] | None = None, *, api: GitHubApi | None = None) -> int:
    """CLI entry point; dry-run is the unconditional default."""

    arguments = _parser().parse_args(argv)
    client: GitHubApi = api or GhCliApi()
    if arguments.apply and any(
        value is None
        for value in (
            arguments.expected_full_name,
            arguments.expected_repository_id,
            arguments.expected_main_sha,
            arguments.expected_snapshot_digest,
        )
    ):
        print(
            "error: --apply requires all four expected repository guards: "
            "--expected-full-name, --expected-repository-id, --expected-main-sha, "
            "--expected-snapshot-digest",
            file=sys.stderr,
        )
        return 2
    try:
        snapshot = collect_snapshot(client, arguments.repository)
        repository = _object(snapshot["repository"], "snapshot repository")
        owner = _object(repository["owner"], "snapshot repository owner")
        expected = load_expected_config(
            arguments.config,
            owner_id=_integer(owner["id"], "owner id"),
        )
        if arguments.apply:
            result = apply_hardening(
                api=client,
                repository=arguments.repository,
                expected=expected,
                expected_full_name=arguments.expected_full_name,
                expected_repository_id=arguments.expected_repository_id,
                expected_main_sha=arguments.expected_main_sha,
                expected_snapshot_digest=arguments.expected_snapshot_digest,
            )
        else:
            result = build_plan(snapshot, expected)
            result["mode"] = "dry-run"
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except GitHubHardeningError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
