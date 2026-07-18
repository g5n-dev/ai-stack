from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
TREND_ASSETS = "blog/static/data/stack-trends"


def _workflow(name: str) -> tuple[dict[str, object], str]:
    path = WORKFLOWS / name
    text = path.read_text(encoding="utf-8")
    parsed = yaml.load(text, Loader=yaml.BaseLoader)
    assert isinstance(parsed, dict)
    return parsed, text


def _job(workflow: dict[str, object], job_name: str) -> dict[str, object]:
    jobs = workflow.get("jobs")
    assert isinstance(jobs, dict)
    job = jobs.get(job_name)
    assert isinstance(job, dict)
    return job


def _steps_by_name(job: dict[str, object]) -> dict[str, dict[str, object]]:
    steps = job.get("steps")
    assert isinstance(steps, list)
    result: dict[str, dict[str, object]] = {}
    for step in steps:
        assert isinstance(step, dict)
        name = step.get("name")
        if isinstance(name, str):
            result[name] = step
    return result


def _assert_no_secret_expression(value: object) -> None:
    if isinstance(value, dict):
        for item in value.values():
            _assert_no_secret_expression(item)
    elif isinstance(value, list):
        for item in value:
            _assert_no_secret_expression(item)
    elif isinstance(value, str):
        assert "secrets." not in value


def test_deploy_rebuilds_and_verifies_committed_trend_assets_for_every_event() -> None:
    workflow, _text = _workflow("deploy.yml")
    job = _job(workflow, "build-and-deploy")
    steps = _steps_by_name(job)

    build = steps["Build STACK trends"]
    verify = steps["Verify STACK trend assets"]
    commit = steps["Commit generated data"]

    # No event guard means schedule/dispatch refreshes and ordinary pushes all
    # execute the exact same deterministic builder.
    assert "if" not in build
    assert "scripts/build_stack_trends.py" in str(build["run"])
    assert "scripts/verify_stack_trends.py" in str(verify["run"])
    assert 'if [ "${AI_STACK_REFRESH_DATA}" != "true" ]; then' in str(
        verify["run"]
    )
    assert f"git diff --exit-code -- {TREND_ASSETS}" in str(verify["run"])
    assert TREND_ASSETS in str(commit["run"])

    names = list(steps)
    assert names.index("Build historical content quality manifest") < names.index(
        "Build STACK trends"
    )
    assert names.index("Verify committed Post quality gate") < names.index(
        "Build STACK trends"
    )
    assert names.index("Build STACK trends") < names.index("Build Hugo site")
    assert names.index("Verify STACK trend assets") < names.index("Build Hugo site")


def test_delete_rebuilds_verifies_and_commits_trends_before_deploy() -> None:
    workflow, _text = _workflow("delete-post.yml")
    steps = _steps_by_name(_job(workflow, "delete-post"))
    rebuild_run = str(steps["Rebuild Post-derived data"]["run"])
    commit_run = str(steps["Commit deletion and generated data"]["run"])

    assert "scripts/build_stack_trends.py" in rebuild_run
    assert "scripts/verify_stack_trends.py" in rebuild_run
    assert TREND_ASSETS in commit_run


def test_monitoring_checks_local_and_live_trend_freshness_and_hashes() -> None:
    workflow, _text = _workflow("monitoring.yml")
    steps = _steps_by_name(_job(workflow, "verify-data-freshness"))
    check = steps["Verify local and live trend freshness"]
    run = str(check["run"])

    assert "scripts/verify_stack_trends.py" in run
    assert f"--root {TREND_ASSETS}" in run
    assert "scripts/verify_stack_trends_live.py" in run
    assert "--live-index-url https://ai-stack.site/data/stack-trends/index.json" in run
    assert "--max-age-hours 12" in run
    assert "--verify-hashes" in run


def test_trend_steps_never_receive_secrets_and_workflow_secrets_are_step_scoped() -> None:
    for workflow_name, job_name in (
        ("deploy.yml", "build-and-deploy"),
        ("delete-post.yml", "delete-post"),
    ):
        workflow, _text = _workflow(workflow_name)
        _assert_no_secret_expression(workflow.get("env", {}))
        job = _job(workflow, job_name)
        _assert_no_secret_expression(job.get("env", {}))

        for name, step in _steps_by_name(job).items():
            if "trend" in name.casefold():
                _assert_no_secret_expression(step)

    deploy, _text = _workflow("deploy.yml")
    deploy_steps = _steps_by_name(_job(deploy, "build-and-deploy"))
    crawler_env = deploy_steps["Run crawler"].get("env")
    indexnow_env = deploy_steps["Prepare IndexNow key file"].get("env")
    notify_env = deploy_steps["Notify search engines (IndexNow/Google)"].get("env")
    assert isinstance(crawler_env, dict)
    assert isinstance(indexnow_env, dict)
    assert isinstance(notify_env, dict)
    assert "ANTHROPIC_AUTH_TOKEN" in crawler_env
    assert "BING_INDEXNOW_API_KEY" in indexnow_env
    assert "GOOGLE_INDEXING_API_KEY" in notify_env

    deletion, _text = _workflow("delete-post.yml")
    delete_steps = _steps_by_name(_job(deletion, "delete-post"))
    prepare_env = delete_steps["Validate inputs and prepare deletion"].get("env")
    assert isinstance(prepare_env, dict)
    assert "ANTHROPIC_AUTH_TOKEN" in prepare_env


def test_local_runner_refreshes_and_verifies_trends_before_hugo() -> None:
    source = (ROOT / "scripts" / "run_local.sh").read_text(encoding="utf-8")

    build = "python3 scripts/build_stack_trends.py"
    verify = "python3 scripts/verify_stack_trends.py"
    hugo = "hugo --minify --cleanDestinationDir"
    assert build in source
    assert verify in source
    assert source.index(build) < source.index(hugo)
    assert source.index(verify) < source.index(hugo)


def test_required_ci_check_runs_delivery_and_trend_contract_tests() -> None:
    workflow, text = _workflow("ci.yml")
    job = _job(workflow, "unit-tests")
    steps = _steps_by_name(job)

    assert job["name"] == "Unit Tests"
    assert "tests/test_trends_delivery_contract.py" in text
    assert "tests/test_trends_page.py" in text
    assert "tests/test_stack_trends.py" in text
    assert "tests/test_stack_trends_monitoring.py" in text

    build = steps["Build committed STACK trend assets"]
    verify = steps["Verify committed STACK trend assets"]
    assert "scripts/build_stack_trends.py" in str(build["run"])

    verify_run = str(verify["run"])
    assert "scripts/verify_stack_trends.py" in verify_run
    assert "--verify-hashes" in verify_run
    assert f"git add --intent-to-add {TREND_ASSETS}" in verify_run
    assert f"git diff --exit-code -- {TREND_ASSETS}" in verify_run
    assert verify_run.index("--verify-hashes") < verify_run.index(
        f"git add --intent-to-add {TREND_ASSETS}"
    )
    assert verify_run.index(f"git add --intent-to-add {TREND_ASSETS}") < verify_run.index(
        f"git diff --exit-code -- {TREND_ASSETS}"
    )

    names = list(steps)
    assert names.index("Build committed STACK trend assets") < names.index(
        "Verify committed STACK trend assets"
    )
    assert names.index("Verify committed STACK trend assets") < names.index(
        "Run browser-runtime unit tests"
    )
