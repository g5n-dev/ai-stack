from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"

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


def test_actions_workflow_inventory_is_explicit() -> None:
    assert {path.name for path in WORKFLOWS.glob("*.yml")} == {
        "ci.yml",
        "delete-post.yml",
        "deploy.yml",
        "monitoring.yml",
    }


def test_pr_ci_keeps_the_existing_single_required_check() -> None:
    workflow, text = _workflow("ci.yml")
    assert workflow["name"] == "PR CI"
    assert workflow["on"] == {
        "pull_request": {"branches": ["main"]},
        "workflow_dispatch": "",
    }
    assert workflow["concurrency"] == {
        "group": "pr-ci-${{ github.event.pull_request.number || github.ref }}",
        "cancel-in-progress": "true",
    }
    assert workflow["permissions"] == {"contents": "read"}
    jobs = _jobs(workflow)
    assert tuple(jobs) == ("unit-tests",)
    assert jobs["unit-tests"]["name"] == "Unit Tests"
    assert "pytest==9.0.3" in text
    assert "tests/test_content_freshness.py" in text
    assert "tests/test_workflow_security.py" in text
    assert "static-site" not in text
    assert "browser-e2e" not in text


def test_deploy_keeps_a_single_fail_closed_job_flow() -> None:
    workflow, text = _workflow("deploy.yml")
    assert workflow["name"] == "Build and Deploy"
    assert workflow["on"] == {
        "schedule": [{"cron": "17 * * * *"}],
        "workflow_dispatch": {
            "inputs": {
                "refresh_data": {
                    "description": "Crawl and regenerate Post-derived data before deploy",
                    "required": "false",
                    "default": "true",
                    "type": "boolean",
                }
            }
        },
        "push": {"branches": ["main"]},
    }
    assert workflow["concurrency"] == {
        "group": "build-and-deploy-main",
        "cancel-in-progress": "false",
    }
    assert workflow["permissions"] == {
        "contents": "write",
        "pages": "write",
        "id-token": "write",
    }
    jobs = _jobs(workflow)
    assert tuple(jobs) == ("build-and-deploy",)
    assert jobs["build-and-deploy"]["if"] == (
        "${{ !(github.event_name == 'push' && github.actor == 'github-actions[bot]') }}"
    )
    for dormant_component in (
        "git_cas_writer.py",
        "release_guard.py",
        "artifact_guard.py",
        "persist_receipt",
    ):
        assert dormant_component not in text

    steps = jobs["build-and-deploy"]["steps"]
    assert isinstance(steps, list)
    step_names = [step.get("name") for step in steps if isinstance(step, dict)]
    steps_by_name = {
        step.get("name"): step for step in steps if isinstance(step, dict)
    }
    assert step_names.index("Build Hugo site") < step_names.index(
        "Commit generated data"
    )
    assert step_names.index(
        "Build Pagefind search index and result catalog"
    ) < step_names.index("Commit generated data")
    assert step_names.index("Commit generated data") < step_names.index(
        "Upload artifact"
    )
    for data_refresh_step in (
        "Install Playwright browsers",
        "Run crawler",
        "Sanitize broken relref links",
        "Build historical content quality manifest",
        "Build tag graph",
        "Commit generated data",
    ):
        assert steps_by_name[data_refresh_step]["if"] == (
            "${{ env.AI_STACK_REFRESH_DATA == 'true' }}"
        )
    assert steps_by_name["Moderation cleanup (LLM)"]["if"] == (
        "${{ env.AI_STACK_REFRESH_DATA == 'true' "
        "&& env.AI_STACK_RUNTIME_PROFILE != 'ci' }}"
    )
    assert steps_by_name["Verify committed Post quality gate"]["if"] == (
        "${{ env.AI_STACK_REFRESH_DATA != 'true' }}"
    )
    verify_run = steps_by_name["Verify generated graph"]["run"]
    assert isinstance(verify_run, str)
    assert 'if [ "${AI_STACK_REFRESH_DATA}" != "true" ]; then' in verify_run
    assert (
        "python3 scripts/verify_graph.py --assets-only --public-dir blog/static"
        in verify_run
    )
    assert "python3 scripts/verify_graph.py" in verify_run
    assert "reset --hard" not in text
    assert "git pull --rebase" not in text
    assert "reusing existing graph artifacts" not in text


def test_delete_workflow_rebuilds_derived_data_and_waits_for_deploy() -> None:
    deletion, text = _workflow("delete-post.yml")
    assert deletion["name"] == "Delete Post"
    assert deletion["concurrency"] == {
        "group": "delete-post-main",
        "cancel-in-progress": "false",
    }
    assert deletion["permissions"] == {"actions": "write", "contents": "write"}
    dispatch = deletion["on"]["workflow_dispatch"]  # type: ignore[index]
    assert isinstance(dispatch, dict)
    inputs = dispatch["inputs"]
    assert isinstance(inputs, dict)
    assert tuple(inputs) == ("mode", "post_path", "scan_limit", "dry_run")
    assert tuple(_jobs(deletion)) == ("delete-post",)
    job = _jobs(deletion)["delete-post"]
    assert job["timeout-minutes"] == "180"
    steps = job["steps"]
    assert isinstance(steps, list)
    steps_by_name = {
        step.get("name"): step for step in steps if isinstance(step, dict)
    }
    assert tuple(steps_by_name) == (
        "Checkout main branch",
        "Configure Git",
        "Set up Python",
        "Install Python dependencies",
        "Validate inputs and prepare deletion",
        "Rebuild Post-derived data",
        "Commit deletion and generated data",
        "Deploy committed deletion and wait",
    )
    rebuild = steps_by_name["Rebuild Post-derived data"]
    assert rebuild["if"] == "${{ steps.prepare.outputs.changed == 'true' }}"
    rebuild_run = rebuild["run"]
    assert "scripts/build_content_quality_manifest.py" in rebuild_run
    assert "--fail-on-quarantine" in rebuild_run
    assert "--fail-on-structural-warning" in rebuild_run
    assert 'TAG_GRAPH_ENABLE_CONTENT_MINING: "0"' in text
    assert 'TAG_INTRO_ENABLED: "0"' in text
    assert 'TAG_INTRO_MAX_NEW: "0"' in text
    assert "python3 -m processor.tag_graph" in rebuild_run
    assert "scripts/verify_graph.py --assets-only --public-dir blog/static" in rebuild_run

    commit = steps_by_name["Commit deletion and generated data"]
    commit_run = commit["run"]
    assert "blog/data/content_quality.json" in commit_run
    assert "blog/static/data/tag-graph" in commit_run
    assert "git push origin HEAD:main" in commit_run
    assert "[skip ci]" not in text

    deploy = steps_by_name["Deploy committed deletion and wait"]
    deploy_run = deploy["run"]
    assert "gh workflow run deploy.yml --ref main -f refresh_data=false" in deploy_run
    assert "gh run watch" in deploy_run
    assert "--exit-status" in deploy_run
    assert deploy["if"] == "${{ steps.commit.outputs.head_sha != '' }}"



def test_monitoring_checks_main_and_live_data_instead_of_legacy_gh_pages() -> None:
    monitoring, text = _workflow("monitoring.yml")
    assert monitoring["name"] == "System Monitoring & Content Quality Tracking"
    assert monitoring["on"] == {
        "schedule": [{"cron": "23 */6 * * *"}],
        "workflow_dispatch": "",
    }
    assert monitoring["concurrency"] == {
        "group": "content-freshness-monitor",
        "cancel-in-progress": "true",
    }
    assert monitoring["permissions"] == {"contents": "read"}
    assert tuple(_jobs(monitoring)) == ("verify-data-freshness",)
    assert "scripts/verify_content_freshness.py" in text
    assert "https://ai-stack.site/data/tag-graph/index.json" in text
    assert "--max-age-hours 12" in text
    assert "gh-pages" not in text


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


def test_hugo_external_mount_keeps_local_pages_and_uses_content_ledger() -> None:
    text = (ROOT / "blog" / "ledger-mount.toml").read_text(encoding="utf-8")
    assert 'source = "content"' in text
    assert 'source = "../content-ledger/content/posts"' in text
    assert 'target = "content/posts"' in text
    assert text.count('target = "content"') == 1


def test_branch_architecture_marks_the_new_coordinator_as_dormant() -> None:
    document = (ROOT / "docs" / "BRANCH_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )
    for required in (
        "main`：只保存代码",
        "content`：orphan 内容账本",
        "ops`：orphan 运维事实账本",
        "PR CI",
        "Build and Deploy",
        "System Monitoring & Content Quality Tracking",
        "17 * * * *",
        "23 */6 * * *",
        "Unit Tests",
        "本次可靠性修复修改 `deploy.yml` 与 `monitoring.yml`",
        "目标协调 DAG 尚未接入 GitHub Actions",
    ):
        assert required in document
