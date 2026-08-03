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
        "pr-gate.yml",
        "production-recovery.yml",
    }


def test_pr_ci_runs_only_as_a_trusted_main_dispatch_for_one_exact_target() -> None:
    workflow, text = _workflow("ci.yml")
    assert workflow["name"] == "PR CI"
    assert workflow["run-name"] == "trusted-ci:${{ inputs.target_sha }}"
    assert workflow["on"] == {
        "workflow_dispatch": {
            "inputs": {
                "target_sha": {
                    "description": "Exact commit SHA tested by the trusted main workflow",
                    "required": "true",
                    "type": "string",
                }
            }
        }
    }
    assert workflow["concurrency"] == {
        "group": "trusted-pr-ci-${{ inputs.target_sha }}",
        "cancel-in-progress": "true",
    }
    assert workflow["permissions"] == {"contents": "read"}
    jobs = _jobs(workflow)
    assert tuple(jobs) == ("unit-tests",)
    assert jobs["unit-tests"]["name"] == "PR Test Suite"
    assert "pytest==9.0.3" in text
    assert "tests/test_content_freshness.py" in text
    assert "tests/test_workflow_security.py" in text
    assert "tests/test_protected_branch_merge.py" in text
    assert "ref: ${{ inputs.target_sha }}" in text
    assert "persist-credentials: false" in text
    assert '[[ "$TARGET_SHA" =~ ^[0-9a-f]{40}$ ]]' in text
    assert "cache:" not in text
    assert "static-site" not in text
    assert "browser-e2e" not in text


def test_pr_gate_uses_pull_request_target_only_as_a_trusted_dispatch_controller() -> None:
    workflow, text = _workflow("pr-gate.yml")
    assert workflow["name"] == "Protected PR Gate"
    assert workflow["on"] == {
        "pull_request_target": {
            "branches": ["main"],
            "types": ["opened", "reopened", "synchronize", "ready_for_review"],
        }
    }
    assert workflow["permissions"] == {}
    assert workflow["concurrency"] == {
        "group": "protected-pr-gate-${{ github.event.pull_request.number }}",
        "cancel-in-progress": "true",
    }
    jobs = _jobs(workflow)
    assert tuple(jobs) == ("validate",)
    job = jobs["validate"]
    assert job["permissions"] == {
        "actions": "write",
        "checks": "write",
        "contents": "read",
        "pull-requests": "read",
    }
    assert "github.event.pull_request.draft == false" in str(job["if"])
    assert "automation/" in str(job["if"])
    assert "ref: ${{ github.sha }}" in text
    assert "scripts/protected_branch_merge.py validate-pr" in text
    assert "github.event.pull_request.head.sha" in text
    assert "checkout exact target" not in text.lower()
    assert "secrets." not in text


def test_deploy_uses_a_fail_closed_least_privilege_job_flow() -> None:
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
                },
                "expected_sha": {
                    "description": "Optional exact main SHA required for chained deploys",
                    "required": "false",
                    "default": "",
                    "type": "string",
                }
            }
        },
        "push": {"branches": ["main"]},
    }
    assert workflow["concurrency"] == {
        "group": "build-and-deploy-main",
        "cancel-in-progress": "false",
    }
    assert workflow["permissions"] == {}
    jobs = _jobs(workflow)
    assert tuple(jobs) == (
        "refresh",
        "validate",
        "persist",
        "build",
        "deploy",
        "production-verify",
        "notify",
    )
    assert jobs["refresh"]["if"] == (
        "${{ !(github.event_name == 'push' && github.actor == 'github-actions[bot]') }}"
    )
    assert {name: job["permissions"] for name, job in jobs.items()} == {
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
    assert "scripts/artifact_guard.py" in text
    assert "scripts/git_cas_writer.py" in text
    assert "scripts/protected_branch_merge.py merge" in text
    assert '--force-with-lease="refs/heads/${AUTOMATION_BRANCH}:${head_sha}"' in text
    assert "ref: ${{ github.sha }}" in text
    assert "main SHA does not match chained deploy receipt" in text
    assert "scripts/release_guard.py guard-marker" in text
    assert "scripts/production_smoke.py" in text
    assert "ref: ${{ needs.persist.outputs.persisted_sha }}" in text
    assert "[skip ci]" in text
    assert "reset --hard" not in text
    assert "git pull --rebase" not in text


def test_delete_workflow_rebuilds_derived_data_and_waits_for_deploy() -> None:
    deletion, text = _workflow("delete-post.yml")
    assert deletion["name"] == "Delete Post"
    assert deletion["concurrency"] == {
        "group": "delete-post-main",
        "cancel-in-progress": "false",
    }
    assert deletion["permissions"] == {}
    dispatch = deletion["on"]["workflow_dispatch"]  # type: ignore[index]
    assert isinstance(dispatch, dict)
    inputs = dispatch["inputs"]
    assert isinstance(inputs, dict)
    assert tuple(inputs) == ("mode", "post_path", "scan_limit", "dry_run")
    jobs = _jobs(deletion)
    assert tuple(jobs) == ("analyze", "writer")
    assert jobs["analyze"]["permissions"] == {"contents": "read"}
    assert jobs["writer"]["permissions"] == {
        "actions": "write",
        "checks": "write",
        "contents": "write",
        "pull-requests": "write",
    }
    writer_text = text[text.index("  writer:"):]
    assert "secrets." not in writer_text
    assert "scripts/artifact_guard.py validate" in writer_text
    assert "scripts/git_cas_writer.py commit-and-push" in writer_text
    assert "scripts/protected_branch_merge.py merge" in writer_text
    assert '--force-with-lease="refs/heads/${AUTOMATION_BRANCH}:${head_sha}"' in writer_text
    assert "bash scripts/rebuild_release_data.sh" in writer_text
    assert "scripts/protected_branch_merge.py deploy" in writer_text
    assert "--expected-sha \"$PERSISTED_SHA\"" in writer_text
    assert "gh workflow run" not in writer_text
    assert "gh run list" not in writer_text



def test_monitoring_checks_main_and_live_data_instead_of_legacy_gh_pages() -> None:
    monitoring, text = _workflow("monitoring.yml")
    assert monitoring["name"] == "System Monitoring & Content Quality Tracking"
    assert monitoring["on"] == {
        "schedule": [{"cron": "41 * * * *"}],
        "workflow_dispatch": "",
    }
    assert monitoring["concurrency"] == {
        "group": "production-release-monitor",
        "cancel-in-progress": "true",
    }
    assert monitoring["permissions"] == {}
    assert tuple(_jobs(monitoring)) == ("verify-production-state",)
    assert "scripts/production_monitor.py" in text
    assert "--max-divergence-hours 3" in text
    assert "--max-stale-hours 12" in text
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


def test_branch_architecture_documents_the_active_release_coordinator() -> None:
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
        "41 * * * *",
        "Unit Tests",
        "当前 v1 工作流已经覆盖内容来源门禁",
        "refresh → validate → persist → build → deploy → production-verify → notify",
    ):
        assert required in document
