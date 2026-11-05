"""Contracts that keep the release chain independent of runner-image drift.

Incident 2026-10-05: the floating ``ubuntu-latest`` label rolled to 26.04, the
pinned Playwright build refused to install Chromium on that image, and an
*optional* browser install inside the production ``refresh`` job failed every
scheduled run for 30 days. The monitor kept alerting, but the chain never got
past job one.

These tests are the durable part of the fix: no amount of future editing should
be able to reintroduce a floating runner label or a browser dependency on the
release-critical path without failing CI.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
PINNED_RUNNER = "ubuntu-24.04"
# Sources that are fetched over HTTP/RSS/API and never need a browser.
BROWSER_FREE_SOURCES = frozenset(
    {"github_trending", "hacker_news", "arxiv_ai", "juejin", "blogs_podcasts"}
)


def _parse(path: Path) -> dict[str, Any]:
    # BaseLoader keeps the YAML key `on` instead of YAML 1.1's boolean True.
    parsed = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert isinstance(parsed, dict)
    return parsed


def _jobs(path: Path) -> dict[str, Any]:
    jobs = _parse(path).get("jobs")
    assert isinstance(jobs, dict)
    return jobs


def test_every_workflow_job_uses_the_pinned_runner_image() -> None:
    offenders: list[str] = []
    for path in sorted(WORKFLOWS.glob("*.yml")):
        for name, job in _jobs(path).items():
            if not isinstance(job, dict) or job.get("runs-on") != PINNED_RUNNER:
                offenders.append(f"{path.name}:{name}={job.get('runs-on') if isinstance(job, dict) else '?'}")

    assert offenders == [], f"unpinned runner images: {offenders}"


def test_no_workflow_uses_the_floating_latest_label() -> None:
    # Only the actual directive matters; documentation may mention the label
    # when explaining why it is forbidden.
    offenders = [
        path.name
        for path in sorted(WORKFLOWS.glob("*.yml"))
        if "runs-on: ubuntu-latest" in path.read_text(encoding="utf-8")
    ]

    assert offenders == [], f"floating runner label in: {offenders}"


def test_production_refresh_never_installs_a_browser() -> None:
    deploy = WORKFLOWS / "deploy.yml"
    text = deploy.read_text(encoding="utf-8")

    assert "python3 -m playwright install" not in text
    assert "Install crawler browser" not in text

    refresh = _jobs(deploy)["refresh"]
    assert isinstance(refresh, dict)
    steps = refresh.get("steps")
    assert isinstance(steps, list)
    names = [str(step.get("name", "")).lower() for step in steps if isinstance(step, dict)]
    assert not any("browser" in name or "chromium" in name for name in names)


def test_ci_still_installs_chromium_for_browser_smoke_tests() -> None:
    """Browser tests are legitimate in CI; they just must not gate publishing."""

    text = (WORKFLOWS / "ci.yml").read_text(encoding="utf-8")

    assert "python3 -m playwright install --with-deps chromium" in text
    assert "tests/e2e/test_static_site.py" in text


def test_ci_profile_enables_only_browser_free_sources() -> None:
    """The checked-in source list also contains optional browser-based sources.

    ``runtime_profile.py`` disables them under the ``ci`` profile that deploy.yml
    sets for every production refresh. Assert the effective set, not the raw one,
    so a future change to that profile cannot silently put Chromium back on the
    release-critical path.
    """

    from runtime_profile import apply_sources_runtime_profile

    config = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text(encoding="utf-8"))
    assert isinstance(config, dict)
    effective = apply_sources_runtime_profile(config, "ci")
    sources = effective.get("sources")
    assert isinstance(sources, dict)
    enabled = {
        name
        for name, settings in sources.items()
        if isinstance(settings, dict) and settings.get("enabled") is True
    }

    assert enabled, "at least one production source must stay enabled"
    assert enabled <= BROWSER_FREE_SOURCES, f"browser-dependent source enabled: {enabled - BROWSER_FREE_SOURCES}"
    assert sources["twitter"]["enabled"] is False
    assert sources["reddit"]["enabled"] is False


def test_monitoring_does_not_hardcode_a_wrong_failure_stage() -> None:
    text = (WORKFLOWS / "monitoring.yml").read_text(encoding="utf-8")

    assert "不要预判断为 \\`validate\\` 阶段" in text
    assert "首个失败 job 与失败步骤" in text


def test_incident_and_runner_policy_are_documented() -> None:
    incident = ROOT / "docs" / "operations" / "INCIDENT-2026-10-05.md"
    policy = ROOT / "docs" / "operations" / "runner-pinning.md"

    assert incident.is_file()
    assert "ubuntu26.04-x64" in incident.read_text(encoding="utf-8")
    assert PINNED_RUNNER in policy.read_text(encoding="utf-8")
    assert "INCIDENT-2026-10-05" in policy.read_text(encoding="utf-8")


def test_release_chain_test_is_registered_in_ci() -> None:
    """A test that never runs is decoration, not a control."""

    text = (WORKFLOWS / "ci.yml").read_text(encoding="utf-8")

    assert "tests/test_check_release_runs.py" in text
    assert "tests/test_runner_pinning_contract.py" in text
