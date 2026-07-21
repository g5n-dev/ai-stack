from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_public_setup_docs_do_not_publish_stale_or_provider_specific_examples() -> None:
    paths = (
        ROOT / ".env.example",
        ROOT / "DEPLOYMENT.md",
        ROOT / "docs" / "README.md",
        ROOT / "docs" / "定时抓取配置说明.md",
        ROOT / "docs" / "系统设计文档.md",
    )
    forbidden = (
        "daily-update.yml",
        "Daily Blog Update",
        "yourusername",
        "/Users/frank/",
        "api.minimaxi.com",
        "MiniMax-M2.7-highspeed",
        "sk-ant-",
    )

    for path in paths:
        source = path.read_text(encoding="utf-8")
        for marker in forbidden:
            assert marker not in source, (
                f"{path.relative_to(ROOT)} contains stale marker {marker!r}"
            )


def test_release_and_contribution_docs_cover_the_v1_operating_contract() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs" / "V1_RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
    runbook = (ROOT / "docs" / "operations" / "freshness-runbook.md").read_text(
        encoding="utf-8"
    )

    assert "./CONTRIBUTING.md" in readme
    assert "./docs/V1_RELEASE_CHECKLIST.md" in readme
    for marker in (
        "npm test",
        "python3 -m pytest",
        "敏感",
        "Issue",
        "Pull Request",
    ):
        assert marker in contributing

    for marker in (
        ".github/workflows/ci.yml",
        ".github/workflows/deploy.yml",
        ".github/workflows/monitoring.yml",
        "build_content_quality_manifest.py",
        "verify_graph.py",
        "verify_stack_trends.py",
        "Pagefind",
        "390",
        "1280",
        "ai-stack.site",
        "密钥",
    ):
        assert marker in checklist

    assert "./docs/operations/freshness-runbook.md" in readme
    for marker in (
        "12 小时",
        "采集",
        "内容质量",
        "派生数据",
        "写入冲突",
        "Pages",
        "线上新鲜度",
        "Actions Summary",
        "密钥",
    ):
        assert marker in runbook


def test_issue_forms_are_safe_and_route_work_to_the_v1_milestone() -> None:
    forms = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "bug.yml",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "feature.yml",
    )
    for path in forms:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(payload, dict)
        assert payload.get("name")
        assert payload.get("description")
        assert payload.get("body")
        assert payload.get("labels")
        text = path.read_text(encoding="utf-8")
        assert "密钥" in text
        assert "v1.0 · 可持续情报闭环" in text

    config = yaml.safe_load(
        (ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(encoding="utf-8")
    )
    assert config["blank_issues_enabled"] is False


def test_pr_ci_builds_the_same_hugo_and_pagefind_delivery_boundary() -> None:
    source = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert 'hugo --baseURL "https://ai-stack.site/" --minify --cleanDestinationDir' in source
    assert "pagefind --site blog/public" in source
    assert "python3 -m ai_stack.pagefind_catalog --public-root blog/public" in source
    assert "test -s blog/public/pagefind/pagefind.js" in source
    assert "test -s blog/public/pagefind/catalog.json" in source
    assert "python3 -m playwright install --with-deps chromium" in source
    assert "run: python3 scripts/verify_graph.py" in source
    assert "AI_STACK_PUBLIC_DIR" in source
    assert "tests/e2e/test_static_site.py" in source
    assert "scripts/verify_graph.py --public-dir blog/public" in source


def test_every_production_manifest_gate_rejects_unverified_provenance() -> None:
    paths = (
        ROOT / ".github" / "workflows" / "ci.yml",
        ROOT / ".github" / "workflows" / "deploy.yml",
        ROOT / ".github" / "workflows" / "delete-post.yml",
        ROOT / "scripts" / "deploy.sh",
        ROOT / "scripts" / "run_local.sh",
    )
    for path in paths:
        source = path.read_text(encoding="utf-8")
        assert source.count("--fail-on-unverified-provenance") == source.count(
            "scripts/build_content_quality_manifest.py"
        ), path.relative_to(ROOT)


def test_local_release_preflight_covers_every_committed_delivery_asset() -> None:
    source = (ROOT / "scripts" / "deploy.sh").read_text(encoding="utf-8")

    for marker in (
        "repair_historical_content.py --check",
        "build_lineage.py",
        "verify_lineage.py",
        "verify_graph.py --assets-only",
        "build_stack_trends.py",
        "verify_stack_trends.py",
        "npm run build:css",
        'hugo --baseURL "$SITE_BASE_URL"',
        "pagefind --site",
        "ai_stack.pagefind_catalog",
        "AI_STACK_PUBLIC_DIR",
        "tests/e2e/test_static_site.py",
        'verify_graph.py --public-dir "$PUBLIC_DIR"',
    ):
        assert marker in source

    assert "generate_content.py" not in source
    assert "gh-pages" not in source
    assert "SITE_BASE_URL:-https://ai-stack.site/" in source
    assert "v0.153.4+extended" in source


def test_local_content_refresh_rebuilds_all_post_derived_products_in_dependency_order() -> None:
    source = (ROOT / "scripts" / "run_local.sh").read_text(encoding="utf-8")

    assert "python3 scripts/build_lineage.py" in source
    assert "python3 scripts/verify_lineage.py" in source
    assert "python3 -m processor.tag_graph" in source
    assert "verify_graph.py --assets-only" in source
    assert source.index("build_lineage.py") < source.index(
        "build_content_quality_manifest.py"
    ) < source.index("build_stack_trends.py") < source.index(
        "python3 -m processor.tag_graph"
    )


def test_removed_gh_pages_branch_sync_has_no_stale_local_entrypoint() -> None:
    assert not (ROOT / "scripts" / "verify_sync.py").exists()


def test_repository_hardening_requires_only_checks_that_ci_actually_emits() -> None:
    expected = yaml.safe_load(
        (ROOT / "config" / "github-hardening.expected.json").read_text(encoding="utf-8")
    )
    main = next(
        item
        for item in expected["rulesets"]
        if item["name"] == "ai-stack/main-protection-v1"
    )
    status = next(rule for rule in main["rules"] if rule["type"] == "required_status_checks")
    assert status["parameters"]["required_status_checks"] == [
        {"context": "Unit Tests", "integration_id": 15368}
    ]
    controller = (ROOT / "scripts" / "protected_branch_merge.py").read_text(
        encoding="utf-8"
    )
    assert '_REQUIRED_CHECK = "Unit Tests"' in controller
    assert "_TRUSTED_ACTIONS_APP_ID = 15368" in controller

    pages = next(item for item in expected["environments"] if item["name"] == "github-pages")
    assert pages["deployment_branch_policies"] == [{"name": "main", "type": "branch"}]


def test_setup_and_docs_share_the_supported_python_and_test_tooling_contract() -> None:
    setup = (ROOT / "scripts" / "setup.sh").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    docs = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")

    assert "pytest==9.0.3" in setup
    assert "3.11–3.13" in readme
    assert "3.11–3.13" in docs


def test_indexnow_public_key_is_validated_before_it_becomes_a_path() -> None:
    workflow = (ROOT / ".github" / "workflows" / "deploy.yml").read_text(
        encoding="utf-8"
    )
    deployment = (ROOT / "DEPLOYMENT.md").read_text(encoding="utf-8")

    prepare = workflow.index("- name: Prepare dedicated public IndexNow ownership key")
    upload = workflow.index("- name: Upload guarded Pages artifact")
    step = workflow[prepare:upload]
    assert "^[A-Za-z0-9-]{8,128}$" in step
    assert "专用公开" in deployment
    assert "不可复用" in deployment
