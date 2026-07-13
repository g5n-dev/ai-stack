from __future__ import annotations

import re
from pathlib import Path

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

    jobs = _jobs(workflow)
    assert "unit-tests" in jobs
    assert jobs["unit-tests"]["name"] == "Unit Tests"
    static_site = _job_text(jobs["static-site"])
    assert "fetch-depth: '0'" in static_site
    assert "--base-sha" in static_site
    assert "github.event.pull_request.base.sha" in static_site

    for required in (
        "uv sync --frozen",
        "ruff check",
        "mypy",
        "pytest",
        "pip-audit",
        "npm ci",
        "npm audit",
        "npm test",
        "npm run build:search",
        "build_related_index.py",
        "hugo",
        "validate_public_content",
        "tests/test_pipeline_cli.py",
        "tests/test_pipeline_safety.py",
        "tests/test_migration_safety.py",
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
        "persist_release",
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
    assert "health" in _needs(jobs["persist_release"])
    assert "persist_release" in _needs(jobs["publish"])
    assert "health" in _needs(jobs["publish"])
    assert "publish" in _needs(jobs["persist_receipt"])


def test_deploy_jobs_enforce_credential_separation_and_revalidate_artifacts() -> None:
    workflow, text = _workflow("deploy.yml")
    jobs = _jobs(workflow)
    generate = _job_text(jobs["generate"])
    content_writer = _job_text(jobs["persist_result"])
    publisher = _job_text(jobs["publish"])
    release_writer = _job_text(jobs["persist_release"])
    receipt_writer = _job_text(jobs["persist_receipt"])

    assert "ANTHROPIC_AUTH_TOKEN" in generate
    assert jobs["generate"]["permissions"] == {"contents": "read"}
    assert jobs["persist_result"]["permissions"] == {"contents": "write"}
    assert "${{ secrets." not in content_writer
    assert jobs["publish"]["permissions"] == {"contents": "read"}
    assert jobs["publish"]["environment"] == "production-publish"
    assert "${{ secrets." in publisher
    assert jobs["persist_release"]["permissions"] == {"contents": "write"}
    assert "${{ secrets." not in release_writer
    assert jobs["persist_receipt"]["permissions"] == {"contents": "write"}
    assert "${{ secrets." not in receipt_writer

    for job_name in (
        "validate_discovery",
        "persist_discovery",
        "validate_result",
        "persist_result",
        "persist_release",
        "publish",
        "persist_receipt",
    ):
        job = _job_text(jobs[job_name])
        assert "actions/download-artifact" in job
        assert "artifact_guard.py" in job
    assert "git_cas_writer.py" in text
    assert "release_guard.py" in _job_text(jobs["deploy"])
    assert "release_guard.py verify" in publisher
    assert "state/public-tree-manifest.json" in publisher

    publish_steps = jobs["publish"]["steps"]
    assert isinstance(publish_steps, list)
    secret_step = next(
        step
        for step in publish_steps
        if isinstance(step, dict) and "TWITTER_API_KEY" in _job_text(step)
    )
    validation_step = next(
        step
        for step in publish_steps
        if isinstance(step, dict) and "release_guard.py verify" in _job_text(step)
    )
    assert "${{ secrets." not in _job_text(validation_step)
    assert "ai-stack publish" in _job_text(secret_step)

    channel_secrets = (
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
        "TWITTER_BEARER_TOKEN",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "WECHAT_APPID",
        "WECHAT_SECRET",
    )
    secret_text = _job_text(secret_step)
    for variable in channel_secrets:
        assert f"{variable}: ${{{{ secrets.{variable} }}}}" in secret_text
        for job_name, job in jobs.items():
            if job_name != "publish":
                assert f"secrets.{variable}" not in _job_text(job)
    assert "WECHAT_APP_ID" not in publisher
    assert "WECHAT_APP_SECRET" not in publisher


def test_all_external_publishers_remain_disabled_by_default() -> None:
    config = yaml.safe_load((ROOT / "config/publisher.yaml").read_text(encoding="utf-8"))
    assert isinstance(config, dict)
    publishers = config.get("publishers")
    assert isinstance(publishers, dict)
    assert publishers
    assert all(
        isinstance(settings, dict) and settings.get("enabled") is False
        for settings in publishers.values()
    )
    assert publishers["wechat"]["app_id"] == "${WECHAT_APPID}"
    assert publishers["wechat"]["app_secret"] == "${WECHAT_SECRET}"
    assert publishers["twitter"]["api_key"] == "${TWITTER_API_KEY}"
    assert publishers["twitter"]["api_secret"] == "${TWITTER_API_SECRET}"
    assert publishers["twitter"]["access_token"] == "${TWITTER_ACCESS_TOKEN}"
    assert (
        publishers["twitter"]["access_token_secret"]
        == "${TWITTER_ACCESS_TOKEN_SECRET}"
    )
    assert publishers["twitter"]["bearer_token"] == "${TWITTER_BEARER_TOKEN}"


def test_deploy_binds_main_code_and_keeps_cas_writers_on_named_branches() -> None:
    workflow, _ = _workflow("deploy.yml")
    jobs = _jobs(workflow)
    crawl = _job_text(jobs["crawl"])
    content_writer = _job_text(jobs["persist_result"])
    receipt_writer = _job_text(jobs["persist_receipt"])
    release_writer = _job_text(jobs["persist_release"])
    content_runs = "\n".join(
        str(step.get("run", ""))
        for step in jobs["persist_result"]["steps"]  # type: ignore[union-attr]
        if isinstance(step, dict)
    )
    receipt_runs = "\n".join(
        str(step.get("run", ""))
        for step in jobs["persist_receipt"]["steps"]  # type: ignore[union-attr]
        if isinstance(step, dict)
    )

    assert "github.event_name == 'push' && github.sha || 'main'" in crawl
    assert "ref: content" in content_writer
    assert "symbolic-ref --quiet --short HEAD" in content_runs
    assert "ref: ops" in receipt_writer
    assert "ref: ops" in release_writer
    assert "symbolic-ref --quiet --short HEAD" in receipt_runs
    assert "needs.persist_discovery.outputs.content_sha" in content_writer
    assert "needs.persist_release.outputs.ops_sha" in receipt_writer


def test_build_finalizes_public_tree_before_packaging_release_metadata() -> None:
    workflow, _ = _workflow("deploy.yml")
    steps = _jobs(workflow)["build"]["steps"]
    assert isinstance(steps, list)
    release_step = next(
        step for step in steps if isinstance(step, dict) and step.get("id") == "release"
    )
    build = release_step["run"]
    assert isinstance(build, str)

    render = build.index("ai-stack render")
    hugo = build.index("hugo --source blog")
    pagefind = build.index("npm run build:search")
    dom_validation = build.index("validate_public_content.py --rendered-root")
    finalize = build.index("release_guard.py create")
    package = build.index("artifact_guard.py pack")

    assert render < hugo < pagefind < dom_validation < finalize < package
    assert "build_related_index.py" in build
    assert "build-handoff/state/release-basis.json" in build
    assert "build-handoff/state/release.json" in build
    assert "build-handoff/state/public-tree-manifest.json" in build
    assert 'json.load(open("build-handoff/state/release.json"))["artifact_digest"]' in build
    assert 'json.load(open("build-handoff/state/release.json"))["release_id"]' in build
    assert "archive_sha256" not in build


def test_hugo_external_mount_keeps_local_pages_and_uses_content_ledger() -> None:
    mount = ROOT / "blog" / "ledger-mount.toml"
    text = mount.read_text(encoding="utf-8")

    assert 'source = "content"' in text
    assert 'source = "../content-ledger/content"' in text
    assert text.count('target = "content"') == 2


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
