#!/usr/bin/env python3
"""Alert when release runs stop completing, without waiting for staleness.

A deploy that is cancelled loses everything it produced. Runs 30782886940 and
30785596371 each crawled, generated posts and threw them away, because the job
was killed inside checkout — and GitHub reports a job killed by
``timeout-minutes`` as ``cancelled``, which is neither red nor green and
notifies nobody.

Until now the only signals were downstream: the release marker going stale
(12h) or the publication heartbeat tripping (26h). This closes that window by
looking at the runs themselves, so a broken release chain is visible in one
cycle rather than the next day.

Two rules keep it quiet enough to be worth reading, and honest:

* a single non-success is ignored, since one transient failure is normal and
  the next run usually recovers;
* only scheduled runs count. A push to main re-deploys without crawling
  (AI_STACK_REFRESH_DATA is false outside schedule), and a bot push skips every
  job while still reporting success — counting either would let a green run
  that never refreshed content mask a stall.

This answers "is the release chain completing", not "is new content
appearing". The latter is what publish_heartbeat.py measures, and both are
needed: a chain can complete every cycle while publishing nothing.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from typing import Any, Protocol

API_VERSION = "2022-11-28"
DEFAULT_CONSECUTIVE = 2
DEFAULT_INSPECTED = 10
# 'cancelled' dominates here: it is how a job killed by timeout-minutes appears.
_INCOMPLETE = frozenset({"cancelled", "failure", "startup_failure", "timed_out", "stale"})


class ReleaseRunError(RuntimeError):
    """Raised when run history cannot be established at all."""


class GitHubApi(Protocol):
    def request(self, method: str, endpoint: str) -> object | None: ...


class GhCliApi:
    def request(self, method: str, endpoint: str) -> object | None:
        if method != "GET":
            raise ReleaseRunError("only read access is required here")
        if not endpoint.startswith("/repos/") or any(ord(char) < 32 for char in endpoint):
            raise ReleaseRunError("unsafe GitHub API endpoint")
        command = [
            "gh",
            "api",
            "--header",
            "Accept: application/vnd.github+json",
            "--header",
            f"X-GitHub-Api-Version: {API_VERSION}",
            endpoint,
        ]
        try:
            result = subprocess.run(
                command, check=False, capture_output=True, text=True, timeout=60
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ReleaseRunError("GitHub API transport failed") from exc
        if result.returncode != 0:
            status = re.search(r"\bHTTP ([0-9]{3})\b", result.stderr or "")
            raise ReleaseRunError(
                f"GitHub API request failed{f' (HTTP {status.group(1)})' if status else ''}"
            )
        try:
            return json.loads(result.stdout or "null")
        except json.JSONDecodeError as exc:
            raise ReleaseRunError("GitHub API returned invalid JSON") from exc


def fetch_runs(
    api: GitHubApi,
    *,
    repository: str,
    workflow: str,
    limit: int,
) -> list[dict[str, Any]]:
    payload = api.request(
        "GET",
        f"/repos/{repository}/actions/workflows/{workflow}/runs?per_page={limit}",
    )
    if not isinstance(payload, dict):
        raise ReleaseRunError("workflow run listing is invalid")
    runs = payload.get("workflow_runs")
    if not isinstance(runs, list):
        raise ReleaseRunError("workflow run listing has no runs")
    return [run for run in runs if isinstance(run, dict)]


def evaluate_runs(
    runs: Sequence[dict[str, Any]],
    *,
    consecutive: int = DEFAULT_CONSECUTIVE,
) -> dict[str, Any]:
    """Return the health of the most recent completed release runs."""

    if consecutive < 1:
        raise ReleaseRunError("consecutive threshold must be at least one")
    completed = [
        run
        for run in runs
        if str(run.get("status")) == "completed" and str(run.get("event")) == "schedule"
    ]
    if not completed:
        # No completed run at all is itself a problem, never a healthy default.
        raise ReleaseRunError("no completed scheduled release run was found")

    streak: list[dict[str, Any]] = []
    for run in completed:
        conclusion = str(run.get("conclusion") or "")
        if conclusion in _INCOMPLETE:
            streak.append(run)
            continue
        break

    failing = len(streak) >= consecutive
    return {
        "status": "failing" if failing else "ok",
        "consecutive_incomplete": len(streak),
        "threshold": consecutive,
        "latest_conclusion": str(completed[0].get("conclusion") or "unknown"),
        "runs": [
            {
                "id": run.get("id"),
                "conclusion": str(run.get("conclusion") or "unknown"),
                "created_at": str(run.get("created_at") or ""),
                "event": str(run.get("event") or ""),
                "url": str(run.get("html_url") or ""),
            }
            for run in streak
        ],
    }


def summarize(report: dict[str, Any]) -> str:
    count = int(report["consecutive_incomplete"])
    lines = [
        f"最近 **{count}** 次已完成的发布运行都没有成功，发布链已经中断。",
        "",
        "被取消（`cancelled`）的运行同样计入：GitHub 把 `timeout-minutes` 杀掉的 job "
        "报告为 cancelled，它既不是红也不是绿，不会触发任何通知，"
        "而那次运行已经生成的文章会被整批丢弃。",
        "",
        "| 运行 | 结论 | 触发 | 时间 |",
        "| --- | --- | --- | --- |",
    ]
    for run in report["runs"]:
        lines.append(
            f"| [{run['id']}]({run['url']}) | `{run['conclusion']}` "
            f"| {run['event']} | {run['created_at']} |"
        )
    lines.extend(
        [
            "",
            "排查顺序：打开最新一次运行，看**哪一步**耗尽了时间或失败——"
            "若停在 `Checkout`，那是仓库体积问题而非测试问题。",
        ]
    )
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--workflow", default="deploy.yml")
    parser.add_argument("--consecutive", type=int, default=DEFAULT_CONSECUTIVE)
    parser.add_argument("--inspect", type=int, default=DEFAULT_INSPECTED)
    parser.add_argument("--summary-output")
    return parser


def main(argv: Sequence[str] | None = None, *, api: GitHubApi | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        runs = fetch_runs(
            api or GhCliApi(),
            repository=args.repository,
            workflow=args.workflow,
            limit=max(1, min(args.inspect, 100)),
        )
        report = evaluate_runs(runs, consecutive=args.consecutive)
    except ReleaseRunError as exc:
        print(f"check_release_runs: {exc}", file=sys.stderr)
        if args.summary_output:
            try:
                with open(args.summary_output, "w", encoding="utf-8") as handle:
                    handle.write(f"发布运行历史无法读取：`{exc}`\n\n这本身就是需要排查的问题。")
            except OSError:
                pass
        return 2
    if args.summary_output and report["status"] != "ok":
        try:
            with open(args.summary_output, "w", encoding="utf-8") as handle:
                handle.write(summarize(report))
        except OSError as exc:
            print(f"check_release_runs: cannot write summary: {exc}", file=sys.stderr)
            return 2
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 1 if report["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
