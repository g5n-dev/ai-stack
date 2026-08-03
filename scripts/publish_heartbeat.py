#!/usr/bin/env python3
"""Measure whether the site is still actually publishing new articles.

Almost every way this pipeline breaks — a crossed capacity ceiling, a dead
model endpoint, a starved scheduler, an empty crawl — ends in the same
observable state: no new article appears.  Watching that single outcome
therefore catches failures that no individual component check anticipates,
including the ones where every job stays green.

Only file *additions* count.  Deletions and edits touch the same directory, so a
heartbeat keyed on "posts were modified" is silently reset by a delete-post run
or a data-repair commit, buying a fully stalled pipeline another day of silence.

Thresholds are measured, not asserted.  Over the healthy period 2026-07-10 to
2026-07-29 (133 additions) the gap between additions was: median 2.8h, p90 5.8h,
p95 11.4h, max 23.6h.  Warning sits just above p95 and critical above the
observed maximum, so a healthy pipeline never pages while the four-day outage
would have been caught inside a day.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime

DEFAULT_WARNING_HOURS = 12.0
DEFAULT_CRITICAL_HOURS = 26.0
_POSTS_GLOB = "blog/content/posts/*.md"


class HeartbeatError(RuntimeError):
    """Raised when publication age cannot be established.

    This is never downgraded to "healthy": a monitor that reports ok when it
    cannot measure is worse than no monitor, because it manufactures confidence.
    """


def _last_addition(repository_root: str, pathspec: str) -> datetime:
    command = [
        "git",
        "-C",
        repository_root,
        "log",
        "--diff-filter=A",
        "--format=%cI",
        "-1",
        "--",
        pathspec,
    ]
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise HeartbeatError("git history is unavailable") from exc
    if result.returncode != 0:
        raise HeartbeatError("git log failed while reading publication history")
    stamp = result.stdout.strip().splitlines()
    if not stamp or not stamp[0].strip():
        # A shallow clone truncates history and would read as "never published".
        raise HeartbeatError(
            "no article addition found; a full-history checkout is required"
        )
    try:
        parsed = datetime.fromisoformat(stamp[0].strip())
    except ValueError as exc:
        raise HeartbeatError("git returned an unparsable commit time") from exc
    return parsed.astimezone(UTC)


def evaluate_publish_heartbeat(
    last_addition: datetime,
    *,
    now: datetime | None = None,
    warning_hours: float = DEFAULT_WARNING_HOURS,
    critical_hours: float = DEFAULT_CRITICAL_HOURS,
) -> dict[str, object]:
    current = now or datetime.now(UTC)
    offset = current.utcoffset()
    if offset is None or offset.total_seconds() != 0:
        raise HeartbeatError("heartbeat clock must be UTC")
    if warning_hours <= 0 or critical_hours <= warning_hours:
        raise HeartbeatError("critical threshold must exceed the warning threshold")
    age_hours = (current - last_addition).total_seconds() / 3600
    if age_hours < 0:
        raise HeartbeatError("last publication is in the future")
    if age_hours >= critical_hours:
        status = "critical"
    elif age_hours >= warning_hours:
        status = "warning"
    else:
        status = "ok"
    return {
        "status": status,
        "age_hours": round(age_hours, 3),
        "last_published_at": last_addition.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "warning_hours": warning_hours,
        "critical_hours": critical_hours,
    }


def summarize(report: dict[str, object]) -> str:
    status = str(report["status"])
    age = float(report["age_hours"])  # type: ignore[arg-type]
    headline = {
        "ok": "站点仍在正常产出新文章。",
        "warning": "新文章产出已慢于正常节奏，请留意。",
        "critical": "站点已停止产出新文章。",
    }[status]
    return (
        f"{headline}\n\n"
        f"- 最近一篇新增文章：`{report['last_published_at']}`\n"
        f"- 距今：**{age:.1f} 小时**\n"
        f"- 阈值：warning {report['warning_hours']}h / critical {report['critical_hours']}h\n\n"
        "此检查只统计新增的文章文件，删除与修订不会重置它，"
        "因此它能覆盖各类「任务全绿但没有新内容」的故障。\n\n"
        "排查顺序：`Build and Deploy` 最近几次运行的 `validate` 与 `refresh` 阶段日志。"
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--pathspec", default=_POSTS_GLOB)
    parser.add_argument("--warning-hours", type=float, default=DEFAULT_WARNING_HOURS)
    parser.add_argument("--critical-hours", type=float, default=DEFAULT_CRITICAL_HOURS)
    parser.add_argument(
        "--summary-output",
        help="write a Markdown summary here for the alert channel",
    )
    parser.add_argument(
        "--fail-on",
        choices=("critical", "warning", "never"),
        default="critical",
        help="exit non-zero at this severity",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        last = _last_addition(args.repository_root, args.pathspec)
        report = evaluate_publish_heartbeat(
            last,
            warning_hours=args.warning_hours,
            critical_hours=args.critical_hours,
        )
    except HeartbeatError as exc:
        print(f"publish_heartbeat: {exc}", file=sys.stderr)
        return 2
    if args.summary_output:
        try:
            with open(args.summary_output, "w", encoding="utf-8") as handle:
                handle.write(summarize(report))
        except OSError as exc:
            print(f"publish_heartbeat: cannot write summary: {exc}", file=sys.stderr)
            return 2
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    status = str(report["status"])
    if args.fail_on == "critical" and status == "critical":
        return 1
    if args.fail_on == "warning" and status in {"warning", "critical"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
