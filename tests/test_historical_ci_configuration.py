from __future__ import annotations

import ipaddress
import json
from pathlib import Path
from urllib.parse import urlsplit

from ai_stack.historical_capture_job import (
    BLOG_ALLOWLIST_SCHEMA,
    BLOG_ALLOWLIST_VERSION,
    load_blog_allowlist,
)
from ai_stack.historical_rehydration import build_historical_rehydration_inventory

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST = ROOT / "config" / "historical-blog-allowlist-v1.json"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
DEPLOY_WORKFLOW = ROOT / ".github" / "workflows" / "deploy.yml"


def test_versioned_blog_allowlist_covers_every_pending_inventory_origin_host() -> None:
    payload = json.loads(ALLOWLIST.read_text(encoding="utf-8"))

    assert payload["schema"] == BLOG_ALLOWLIST_SCHEMA
    assert payload["version"] == BLOG_ALLOWLIST_VERSION == 1
    raw_hosts = payload["allowed_hosts"]
    assert isinstance(raw_hosts, list)
    assert raw_hosts == sorted(set(raw_hosts))
    assert raw_hosts

    allowed_hosts = load_blog_allowlist(ALLOWLIST)
    assert allowed_hosts == frozenset(raw_hosts)
    for host in raw_hosts:
        assert host == host.casefold()
        assert not any(character in host for character in "*/:@?#")
        try:
            ipaddress.ip_address(host)
        except ValueError:
            pass
        else:  # pragma: no cover - the production loader rejects this first
            raise AssertionError(f"IP address is not an exact public hostname: {host}")

    inventory = build_historical_rehydration_inventory(
        ROOT / "blog" / "content" / "posts",
        repository_root=ROOT,
        # This gate inspects only blog origins.  An unavailable HN revision keeps
        # the scan deterministic/offline and avoids reading unrelated Git blobs.
        hn_git_revision="0" * 40,
    )
    required_hosts = {
        (urlsplit(str(entry["canonical_url"])).hostname or "").casefold()
        for entry in inventory["entries"]
        if entry["source"] == "blogs_podcasts"
        and entry["recovery_classification"] == "needs_source_recovery"
    }
    assert "" not in required_hosts
    assert required_hosts <= allowed_hosts


def test_ci_runs_every_historical_recovery_contract_without_network_capture() -> None:
    source = CI_WORKFLOW.read_text(encoding="utf-8")
    required_tests = (
        "tests/test_historical_rehydration.py",
        "tests/test_historical_publication.py",
        "tests/test_historical_taxonomy.py",
        "tests/test_historical_source_fetch.py",
        "tests/test_historical_capture_job.py",
        "tests/test_historical_rehydration_apply.py",
        "tests/test_apply_historical_rehydration_cli.py",
        "tests/test_content_quality_terminal_archives.py",
        "tests/test_historical_ci_configuration.py",
    )
    for test_path in required_tests:
        assert test_path in source

    assert "python3 scripts/repair_historical_content.py --check" in source
    assert "scripts/capture_historical_sources.py" not in source
    assert "python3 crawler/historical_source_fetch.py" not in source
    assert "python3 -m crawler.historical_source_fetch" not in source


def test_deploy_uses_only_offline_historical_gates_before_derived_assets() -> None:
    source = DEPLOY_WORKFLOW.read_text(encoding="utf-8")
    rebuild = (ROOT / "scripts" / "rebuild_release_data.sh").read_text(encoding="utf-8")
    fixed_point = "python3 scripts/repair_historical_content.py --check"

    assert "bash scripts/rebuild_release_data.sh" in source
    assert fixed_point in rebuild
    assert "python3 scripts/build_content_quality_manifest.py" in rebuild
    assert rebuild.index(fixed_point) < rebuild.index("scripts/build_lineage.py")
    assert rebuild.index(fixed_point) < rebuild.index("scripts/build_stack_trends.py")
    assert rebuild.index(fixed_point) < rebuild.index("python3 -m processor.tag_graph")
    for forbidden in (
        "scripts/capture_historical_sources.py",
        "python3 crawler/historical_source_fetch.py",
        "python3 -m crawler.historical_source_fetch",
        "python3 ai_stack/historical_capture_job.py",
        "python3 -m ai_stack.historical_capture_job",
    ):
        assert forbidden not in source
        assert forbidden not in rebuild
