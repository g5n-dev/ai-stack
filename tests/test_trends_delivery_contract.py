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


def test_deploy_rebuilds_and_verifies_trends_before_persist_and_pages() -> None:
    workflow, text = _workflow("deploy.yml")
    rebuild = (ROOT / "scripts" / "rebuild_release_data.sh").read_text(encoding="utf-8")
    validate_steps = _steps_by_name(_job(workflow, "validate"))
    build_steps = _steps_by_name(_job(workflow, "build"))
    persist = str(_steps_by_name(_job(workflow, "persist"))["Persist validated files with exact-base CAS"]["run"])

    assert "bash scripts/rebuild_release_data.sh" in str(
        validate_steps["Rebuild and validate derived release data without secrets"]["run"]
    )
    assert "bash scripts/rebuild_release_data.sh" in str(
        build_steps["Rebuild persisted products and prove fixed point"]["run"]
    )
    assert "scripts/build_stack_trends.py" in rebuild
    assert "scripts/verify_stack_trends.py" in rebuild
    assert rebuild.index("scripts/build_content_quality_manifest.py") < rebuild.index(
        "scripts/build_stack_trends.py"
    )
    assert TREND_ASSETS in persist
    assert text.index("bash scripts/rebuild_release_data.sh") < text.index(
        "actions/upload-pages-artifact@"
    )


def test_delete_rebuilds_verifies_and_persists_trends_before_deploy() -> None:
    workflow, _text = _workflow("delete-post.yml")
    steps = _steps_by_name(_job(workflow, "writer"))
    rebuild_run = str(
        steps["Delete approved Posts and rebuild lineage then trends then graph"]["run"]
    )
    persist_run = str(steps["CAS persist deletion and all derived products"]["run"])
    deploy_run = str(steps["Deploy committed deletion and wait"]["run"])

    assert "bash scripts/rebuild_release_data.sh" in rebuild_run
    assert TREND_ASSETS in persist_run
    assert "gh workflow run deploy.yml" in deploy_run


def test_monitoring_checks_the_complete_live_release_with_trend_freshness() -> None:
    workflow, text = _workflow("monitoring.yml")
    steps = _steps_by_name(_job(workflow, "verify-production-state"))
    run = str(steps["Enforce divergence and stale thresholds"]["run"])
    monitor = (ROOT / "scripts" / "production_monitor.py").read_text(encoding="utf-8")
    smoke = (ROOT / "scripts" / "production_smoke.py").read_text(encoding="utf-8")

    assert "scripts/production_monitor.py" in run
    assert "--max-divergence-hours 3" in run
    assert "--max-stale-hours 12" in run
    assert "ai_stack_release_v1.json" in run
    assert "verify_production_sample" in monitor
    assert '"trends_hash", "stack-trends"' in smoke
    assert "verify_stack_trends_live.py" not in text


def test_trend_build_steps_never_receive_secrets_and_writer_is_secret_free() -> None:
    deploy, deploy_text = _workflow("deploy.yml")
    _assert_no_secret_expression(deploy.get("env", {}))
    for name in ("validate", "persist", "build", "deploy", "production-verify"):
        _assert_no_secret_expression(_job(deploy, name))

    refresh_text = deploy_text[
        deploy_text.index("  refresh:"):deploy_text.index("  validate:")
    ]
    notify_text = deploy_text[deploy_text.index("  notify:"):]
    assert "ANTHROPIC_AUTH_TOKEN" in refresh_text
    assert "GOOGLE_INDEXING_API_KEY" in notify_text

    deletion, deletion_text = _workflow("delete-post.yml")
    _assert_no_secret_expression(_job(deletion, "writer"))
    analyze_text = deletion_text[
        deletion_text.index("  analyze:"):deletion_text.index("  writer:")
    ]
    assert "ANTHROPIC_AUTH_TOKEN" in analyze_text


def test_local_runner_refreshes_and_verifies_trends_before_hugo() -> None:
    source = (ROOT / "scripts" / "run_local.sh").read_text(encoding="utf-8")

    build = "python3 scripts/build_stack_trends.py"
    verify = "python3 scripts/verify_stack_trends.py"
    hugo = "hugo --minify --cleanDestinationDir"
    assert build in source
    assert verify in source
    assert source.index(build) < source.index(hugo)
    assert source.index(verify) < source.index(hugo)
