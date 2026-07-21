from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github/workflows"
PINNED_ACTION = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")


def _load(name: str) -> tuple[dict[str, object], str]:
    text = (WORKFLOWS / name).read_text(encoding="utf-8")
    value = yaml.load(text, Loader=yaml.BaseLoader)
    assert isinstance(value, dict)
    return value, text


def _uses(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "uses" and isinstance(child, str):
                found.append(child)
            found.extend(_uses(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_uses(child))
    return found


def test_deploy_is_a_fail_closed_least_privilege_job_chain() -> None:
    workflow, text = _load("deploy.yml")
    jobs = workflow["jobs"]
    assert isinstance(jobs, dict)
    assert tuple(jobs) == (
        "refresh",
        "validate",
        "persist",
        "build",
        "deploy",
        "production-verify",
        "notify",
    )
    assert workflow["permissions"] == {}
    permissions = {name: job["permissions"] for name, job in jobs.items()}
    assert permissions == {
        "refresh": {"contents": "read"},
        "validate": {"contents": "read"},
        "persist": {
            "actions": "write",
            "checks": "write",
            "contents": "write",
            "pull-requests": "write",
        },
        "build": {"contents": "read"},
        "deploy": {"pages": "write", "id-token": "write"},
        "production-verify": {"contents": "read"},
        "notify": {"contents": "read"},
    }
    assert jobs["deploy"]["environment"]["name"] == "github-pages"
    assert jobs["validate"]["needs"] == "refresh"
    assert jobs["persist"]["needs"] == ["refresh", "validate"]
    assert jobs["build"]["needs"] == "persist"
    assert jobs["deploy"]["needs"] == "build"
    assert jobs["production-verify"]["needs"] == ["build", "deploy"]
    assert jobs["notify"]["needs"] == ["build", "production-verify"]
    assert "ref: ${{ needs.persist.outputs.persisted_sha }}" in text
    build_text = text[text.index("  build:"):text.index("  deploy:")]
    assert "bash scripts/rebuild_release_data.sh" in build_text
    assert "npm run build:css" in build_text
    assert "git diff --exit-code" in build_text
    assert "--expected-base \"${BASE_SHA}\"" in text
    assert "--branch \"$AUTOMATION_BRANCH\"" in text
    assert "scripts/protected_branch_merge.py merge" in text
    assert "ref: ${{ github.sha }}" in text
    assert "--branch main" not in text[text.index("  persist:"):text.index("  build:")]
    assert "[skip ci]" in text
    assert 'cron: "17 * * * *"' in text
    assert "github-actions[bot]" in text
    assert "secrets." not in text[text.index("  validate:"):text.index("  notify:")]
    assert "secrets." in text[text.index("  refresh:"):text.index("  validate:")]
    assert "secrets." in text[text.index("  notify:"):]
    refresh_steps = jobs["refresh"]["steps"]
    sanitize = next(
        step for step in refresh_steps if step.get("name") == "Sanitize public source URLs"
    )
    assert "if" not in sanitize
    assert sanitize["run"] == "python3 scripts/generate_content.py --sanitize-relrefs-only"
    step_names = [step.get("name") for step in refresh_steps]
    assert step_names.index("Sanitize public source URLs") < step_names.index(
        "Package exact refresh handoff"
    )


def test_workflow_artifacts_are_hashed_allowlisted_and_actions_are_pinned() -> None:
    for name in (
        "ci.yml",
        "deploy.yml",
        "delete-post.yml",
        "monitoring.yml",
        "pr-gate.yml",
        "production-recovery.yml",
    ):
        workflow, _ = _load(name)
        assert all(PINNED_ACTION.fullmatch(action) for action in _uses(workflow)), name

    _, deploy = _load("deploy.yml")
    for path in (
        "blog/content/posts",
        "data/lineage",
        "blog/static/data/lineage",
        "blog/data/content_quality.json",
        "blog/static/data/stack-trends",
        "blog/static/data/tag-graph",
    ):
        assert path in deploy
    assert "scripts/artifact_guard.py" in deploy
    assert "scripts/release_guard.py guard-marker" in deploy
    assert "ai_stack_release_v1.json" in deploy
    assert "scripts/refresh_transition_guard.py" in deploy
    assert deploy.index("scripts/refresh_transition_guard.py") < deploy.index(
        "find blog/content/posts -type f -name '*.md' -delete"
    )
    refresh_pack = deploy[
        deploy.index("- name: Package exact refresh handoff"):
        deploy.index("- name: Upload refresh handoff")
    ]
    refresh_generation = deploy[
        deploy.index("- name: Refresh Posts with crawler and model"):
        deploy.index("- name: Package exact refresh handoff")
    ]
    assert "secrets.ANTHROPIC_MODEL" in refresh_generation
    for name in (
        "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_BASE_URL",
        "SEARXNG_BASE_URL",
    ):
        assert f"--reject-env {name}" in refresh_pack
        assert f"secrets.{name}" in refresh_pack


def test_trusted_ci_dispatch_contract_matches_the_controller_helper() -> None:
    ci, ci_text = _load("ci.yml")
    dispatch = ci["on"]["workflow_dispatch"]
    assert dispatch["inputs"]["target_sha"]["required"] == "true"
    assert ci["run-name"] == "trusted-ci:${{ inputs.target_sha }}"
    assert ci["concurrency"]["group"] == "trusted-pr-ci-${{ inputs.target_sha }}"
    assert "ref: ${{ inputs.target_sha }}" in ci_text
    assert "persist-credentials: false" in ci_text
    assert "cache:" not in ci_text

    gate, gate_text = _load("pr-gate.yml")
    gate_job = gate["jobs"]["validate"]
    assert gate_job["permissions"]["actions"] == "write"
    assert "scripts/protected_branch_merge.py validate-pr" in gate_text
    assert "github.event.pull_request.head.sha" in gate_text

    helper = (ROOT / "scripts/protected_branch_merge.py").read_text(encoding="utf-8")
    assert 'body={"inputs": {"target_sha": target_sha}, "ref": "main"}' in helper
    assert 'run.get("display_title") != f"trusted-ci:{target_sha}"' in helper


def test_recovery_monitoring_and_delete_workflows_enforce_locked_boundaries() -> None:
    recovery, recovery_text = _load("production-recovery.yml")
    assert recovery["on"] == {"workflow_dispatch": recovery["on"]["workflow_dispatch"]}
    assert recovery["permissions"] == {}
    assert "production-recovery" in recovery_text
    assert "merge-base --is-ancestor" in recovery_text
    assert "verified-release-" in recovery_text
    assert "git push" not in recovery_text

    monitoring, monitoring_text = _load("monitoring.yml")
    assert monitoring["on"]["schedule"] == [{"cron": "41 * * * *"}]
    assert "--max-divergence-hours 3" in monitoring_text
    assert "--max-stale-hours 12" in monitoring_text

    deletion, deletion_text = _load("delete-post.yml")
    jobs = deletion["jobs"]
    assert isinstance(jobs, dict)
    assert tuple(jobs) == ("analyze", "writer")
    assert jobs["analyze"]["permissions"] == {"contents": "read"}
    assert jobs["writer"]["permissions"] == {
        "actions": "write",
        "checks": "write",
        "contents": "write",
        "pull-requests": "write",
    }
    assert "scripts/protected_branch_merge.py merge" in deletion_text
    assert "scripts/protected_branch_merge.py deploy" in deletion_text
    assert "gh run list" not in deletion_text
    writer_text = deletion_text[deletion_text.index("  writer:"):]
    assert "--branch main" not in writer_text
    assert "secrets." not in deletion_text[deletion_text.index("  writer:"):]
    rebuild = (ROOT / "scripts/rebuild_release_data.sh").read_text(encoding="utf-8")
    order = rebuild.index("scripts/build_lineage.py")
    assert "scripts/build_lineage.py --apply-post-metadata" in rebuild
    assert order < rebuild.index("scripts/build_stack_trends.py", order)
    assert order < rebuild.index("python3 -m processor.tag_graph", order)
