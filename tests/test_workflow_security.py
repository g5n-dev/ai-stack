from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"

# These digests are the byte-for-byte Actions contract on origin/main at
# 8b6addc4d9d35ab731e5f843351b5e72494fb37f.  The upgrade branch deliberately
# keeps that contract unchanged; the hardened coordinator remains dormant code.
WORKFLOW_DIGESTS = {
    "ci.yml": "b6663c0a0dd77371960a462fd7f9e761552b7a1a750cbf9cf4e0594c5d440391",
    "delete-post.yml": "579f48b15fa398dd915eededece3254d3b9413b5eb3af9d5216ae11389d00a94",
    "deploy.yml": "e3aeeaafc58b4467f64cc6f7c3d2945626576e537a90d4a81cd67f21283242f8",
    "monitoring.yml": "41f79677828d5163593cb81108101905ba9610c740e8e3260163923d543c544a",
}


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


def test_actions_workflows_match_main_contract_byte_for_byte() -> None:
    assert {path.name for path in WORKFLOWS.glob("*.yml")} == set(WORKFLOW_DIGESTS)
    for name, expected in WORKFLOW_DIGESTS.items():
        actual = hashlib.sha256((WORKFLOWS / name).read_bytes()).hexdigest()
        assert actual == expected, f"{name} changed the protected Actions contract"


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
    assert "static-site" not in text
    assert "browser-e2e" not in text


def test_deploy_keeps_the_existing_single_job_flow() -> None:
    workflow, text = _workflow("deploy.yml")
    assert workflow["name"] == "Build and Deploy"
    assert workflow["on"] == {
        "schedule": [{"cron": "0 * * * *"}],
        "workflow_dispatch": "",
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


def test_delete_and_monitoring_keep_the_existing_jobs_and_inputs() -> None:
    deletion, _ = _workflow("delete-post.yml")
    assert deletion["name"] == "Delete Post"
    assert deletion["concurrency"] == {
        "group": "delete-post-main",
        "cancel-in-progress": "false",
    }
    assert deletion["permissions"] == {"contents": "write"}
    dispatch = deletion["on"]["workflow_dispatch"]  # type: ignore[index]
    assert isinstance(dispatch, dict)
    inputs = dispatch["inputs"]
    assert isinstance(inputs, dict)
    assert tuple(inputs) == ("mode", "post_path", "scan_limit", "dry_run")
    assert tuple(_jobs(deletion)) == ("delete-post",)

    monitoring, _ = _workflow("monitoring.yml")
    assert monitoring["name"] == "System Monitoring & Content Quality Tracking"
    assert monitoring["on"] == {
        "schedule": [{"cron": "0 */6 * * *"}],
        "workflow_dispatch": "",
    }
    assert "concurrency" not in monitoring
    assert "permissions" not in monitoring
    assert tuple(_jobs(monitoring)) == (
        "monitor-main-branch",
        "monitor-gh-pages-branch",
        "monitor-content-quality",
        "monitor-user-value",
        "monitor-token-usage",
        "monitor-sync-status",
        "generate-report",
    )


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
        "0 * * * *",
        "0 */6 * * *",
        "Unit Tests",
        "当前升级 PR 不修改任何 `.github/workflows/*.yml` 字节",
        "目标协调 DAG 尚未接入 GitHub Actions",
    ):
        assert required in document
