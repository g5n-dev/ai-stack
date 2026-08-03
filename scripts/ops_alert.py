#!/usr/bin/env python3
"""Deliver pipeline failures somewhere a human actually reads them.

The 2026-07-30 outage ran for four days while `monitoring.yml` failed correctly
every hour.  Detection was never the problem: a red Actions job was the only
delivery channel, and nobody was watching it.

This turns a check result into a GitHub Issue, which GitHub itself pushes to the
repository owner by email and in the mobile app, using only ``GITHUB_TOKEN`` —
no new secrets to configure and therefore nothing that can silently expire.

Notification volume is the reason alerts get ignored, so state changes notify
and repetition does not:

* first failure  -> open an issue                 (notifies once)
* still failing  -> edit that issue's body        (no notification)
* recovered      -> comment and close the issue   (notifies once)

A four-day outage therefore produces exactly two notifications, not ninety-six.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any, Protocol

API_VERSION = "2022-11-28"
ALERT_LABEL = "ops-alert"
_KEY_RE = re.compile(r"^[a-z][a-z0-9-]{2,48}$")
_MARKER_RE = re.compile(r"<!-- ops-alert:(?P<key>[a-z0-9-]+) -->")
_STATE_RE = re.compile(r"<!-- ops-state:(?P<payload>\{.*?\}) -->")
_MAX_SUMMARY_CHARS = 8_000


class OpsAlertError(RuntimeError):
    """Raised when the alert channel itself cannot be trusted to have delivered."""


class GitHubApi(Protocol):
    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
    ) -> object | None: ...


class GhCliApi:
    """Minimal REST adapter that keeps the token and response bodies out of logs."""

    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
    ) -> object | None:
        normalized = method.upper()
        if normalized not in {"GET", "POST", "PATCH"}:
            raise OpsAlertError("unsupported GitHub API method")
        if not endpoint.startswith("/repos/") or any(ord(char) < 32 for char in endpoint):
            raise OpsAlertError("unsafe GitHub API endpoint")
        command = [
            "gh",
            "api",
            "--method",
            normalized,
            "--header",
            "Accept: application/vnd.github+json",
            "--header",
            f"X-GitHub-Api-Version: {API_VERSION}",
            endpoint,
        ]
        encoded: str | None = None
        if body is not None:
            command.extend(["--input", "-"])
            encoded = json.dumps(body, sort_keys=True, separators=(",", ":"))
        try:
            result = subprocess.run(
                command,
                input=encoded,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise OpsAlertError("GitHub API transport failed") from exc
        if result.returncode != 0:
            status = re.search(r"\bHTTP ([0-9]{3})\b", result.stderr or "")
            suffix = f" (HTTP {status.group(1)})" if status else ""
            raise OpsAlertError(f"GitHub API request failed{suffix}")
        if not result.stdout.strip():
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise OpsAlertError("GitHub API returned invalid JSON") from exc


def _now(value: datetime | None = None) -> str:
    current = value or datetime.now(UTC)
    offset = current.utcoffset()
    if offset is None or offset.total_seconds() != 0:
        raise OpsAlertError("alert clock must be UTC")
    return current.strftime("%Y-%m-%dT%H:%M:%SZ")


def _marker(key: str) -> str:
    return f"<!-- ops-alert:{key} -->"


def find_open_alert(api: GitHubApi, *, repository: str, key: str) -> dict[str, Any] | None:
    """Return the open issue tracking this alert key, if one exists."""

    listed = api.request("GET", f"/repos/{repository}/issues?state=open&per_page=100")
    if listed is None:
        return None
    if not isinstance(listed, list):
        raise OpsAlertError("GitHub issue listing is invalid")
    marker = _marker(key)
    for entry in listed:
        if not isinstance(entry, dict):
            continue
        # Pull requests are issues too; they can never be alert trackers.
        if entry.get("pull_request") is not None:
            continue
        if marker in str(entry.get("body") or ""):
            return entry
    return None


def _prior_state(body: str) -> dict[str, Any]:
    match = _STATE_RE.search(str(body or ""))
    if match is None:
        return {}
    try:
        value = json.loads(match.group("payload"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def render_body(
    *,
    key: str,
    summary: str,
    first_seen: str,
    last_seen: str,
    occurrences: int,
    run_url: str,
) -> str:
    state = json.dumps(
        {"first_seen": first_seen, "occurrences": occurrences},
        sort_keys=True,
        separators=(",", ":"),
    )
    run_line = f"\n最近一次运行：{run_url}\n" if run_url else "\n"
    return (
        f"{_marker(key)}\n"
        f"<!-- ops-state:{state} -->\n\n"
        f"**首次发现**：{first_seen}\n"
        f"**最近发现**：{last_seen}\n"
        f"**连续次数**：{occurrences}\n"
        f"{run_line}\n"
        "---\n\n"
        f"{summary}\n\n"
        "---\n\n"
        "此 Issue 由 `scripts/ops_alert.py` 自动维护：持续故障只更新正文（不再推送通知），"
        "恢复后会自动关闭。请勿手动改动上方的 HTML 注释标记。\n"
    )


def sync_alert(
    api: GitHubApi,
    *,
    repository: str,
    key: str,
    title: str,
    summary: str,
    failing: bool,
    run_url: str = "",
    now: datetime | None = None,
) -> dict[str, Any]:
    """Open, update or close the tracker for one alert key. Returns the action taken."""

    if not _KEY_RE.fullmatch(key):
        raise OpsAlertError("alert key must be lowercase kebab-case")
    if not title.strip():
        raise OpsAlertError("alert title is required")
    stamp = _now(now)
    existing = find_open_alert(api, repository=repository, key=key)

    if not failing:
        if existing is None:
            return {"action": "noop", "key": key}
        number = existing.get("number")
        api.request(
            "POST",
            f"/repos/{repository}/issues/{number}/comments",
            {"body": f"✅ 已恢复：{stamp}\n\n检查重新通过，自动关闭。"},
        )
        api.request("PATCH", f"/repos/{repository}/issues/{number}", {"state": "closed"})
        return {"action": "resolved", "key": key, "issue": number}

    trimmed = summary.strip()[:_MAX_SUMMARY_CHARS] or "(no detail provided)"
    if existing is None:
        body = render_body(
            key=key,
            summary=trimmed,
            first_seen=stamp,
            last_seen=stamp,
            occurrences=1,
            run_url=run_url,
        )
        created = api.request(
            "POST",
            f"/repos/{repository}/issues",
            {"title": f"[ops] {title}", "body": body, "labels": [ALERT_LABEL]},
        )
        number = created.get("number") if isinstance(created, dict) else None
        return {"action": "opened", "key": key, "issue": number}

    prior = _prior_state(str(existing.get("body") or ""))
    first_seen = str(prior.get("first_seen") or stamp)
    try:
        occurrences = int(prior.get("occurrences", 0)) + 1
    except (TypeError, ValueError):
        occurrences = 1
    body = render_body(
        key=key,
        summary=trimmed,
        first_seen=first_seen,
        last_seen=stamp,
        occurrences=occurrences,
        run_url=run_url,
    )
    number = existing.get("number")
    # Editing the body deliberately does not notify: a recurring hourly failure
    # must not bury the one notification that mattered.
    api.request("PATCH", f"/repos/{repository}/issues/{number}", {"body": body})
    return {"action": "updated", "key": key, "issue": number, "occurrences": occurrences}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--key", required=True, help="stable kebab-case alert identifier")
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", default="", help="Markdown detail, or use --summary-file")
    parser.add_argument("--summary-file")
    parser.add_argument("--run-url", default="")
    state = parser.add_mutually_exclusive_group(required=True)
    state.add_argument("--failing", action="store_true", help="the check is failing now")
    state.add_argument("--resolved", action="store_true", help="the check passes now")
    return parser


def main(argv: Sequence[str] | None = None, *, api: GitHubApi | None = None) -> int:
    args = _parser().parse_args(argv)
    summary = args.summary
    if args.summary_file:
        try:
            with open(args.summary_file, encoding="utf-8") as handle:
                summary = handle.read()
        except OSError as exc:
            print(f"ops_alert: cannot read summary file: {exc}", file=sys.stderr)
            return 2
    try:
        result = sync_alert(
            api or GhCliApi(),
            repository=args.repository,
            key=args.key,
            title=args.title,
            summary=summary,
            failing=bool(args.failing),
            run_url=args.run_url,
        )
    except OpsAlertError as exc:
        # Never swallow this: an alerter that fails quietly is indistinguishable
        # from a healthy system, which is the failure mode this file exists for.
        print(f"ops_alert: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
