#!/usr/bin/env python3
"""Turn every release-blocking ceiling into a graduated signal.

The 2026-07-30 outage happened because a ceiling had exactly two states: fine,
and release fails.  Public lineage crossed 3 MiB and thirteen consecutive
deploys died at the same guard with no prior warning of any kind.

Each gauge here reports how much of its budget is spent, so approaching a limit
becomes scheduled work instead of an outage.

A gauge that cannot be measured reports ``unavailable`` and never ``ok``.  A
monitor that silently defaults to healthy when its input is missing manufactures
confidence, which is worse than having no monitor: the pathology it was built to
prevent is exactly the one it then hides.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

WARNING_RATIO = 0.70
CRITICAL_RATIO = 0.85


class CapacityError(RuntimeError):
    """Raised when a required gauge cannot be evaluated at all."""


@dataclass(frozen=True)
class Gauge:
    name: str
    limit: int
    used: int | None
    detail: str
    # False for gauges whose inputs only exist after a site build.
    required: bool = True
    # A structural gauge is a constant of the configuration rather than a
    # growing quantity, so proximity to its limit predicts nothing.  Warning on
    # one would light up permanently from day one and train the reader to ignore
    # the whole report — the alert fatigue that let the real outage run for days.
    structural: bool = False

    @property
    def ratio(self) -> float | None:
        if self.used is None or self.limit <= 0:
            return None
        return self.used / self.limit

    def status(self, *, warning: float, critical: float) -> str:
        ratio = self.ratio
        if ratio is None:
            return "unavailable"
        if self.structural:
            return "critical" if ratio > 1 else "ok"
        if ratio >= critical:
            return "critical"
        if ratio >= warning:
            return "warning"
        return "ok"


def _tree_bytes(root: Path, pattern: str = "*") -> int | None:
    if not root.is_dir():
        return None
    return sum(path.stat().st_size for path in root.rglob(pattern) if path.is_file())


def _tree_files(root: Path, pattern: str = "*") -> int | None:
    if not root.is_dir():
        return None
    return sum(1 for path in root.rglob(pattern) if path.is_file())


def _largest_file_bytes(root: Path, pattern: str) -> int | None:
    if not root.is_dir():
        return None
    sizes = [path.stat().st_size for path in root.rglob(pattern) if path.is_file()]
    return max(sizes) if sizes else 0


def collect_gauges(repository_root: Path) -> list[Gauge]:
    """Measure every ceiling that can be read exactly from the working tree."""

    from ai_stack.lineage import load_lineage_config
    from scripts.release_guard import _MAX_PUBLIC_FILES, _MAX_PUBLIC_TREE_BYTES

    config = load_lineage_config(repository_root / "config" / "lineage.yaml")
    lineage_public = repository_root / "blog" / "static" / "data" / "lineage"
    public_tree = repository_root / "blog" / "public"

    gauges = [
        Gauge(
            name="lineage_public_bytes",
            limit=config.public_max_bytes,
            used=_tree_bytes(lineage_public, "*.json"),
            detail=(
                "溯源公共资产总字节。这是 2026-07-30 停更的直接原因；"
                f"超过 {config.public_retention_ratio:.0%} 后构建会开始淘汰最旧事件以保持有界。"
            ),
        ),
        Gauge(
            name="lineage_public_files",
            limit=config.public_max_files,
            used=_tree_files(lineage_public, "*.json"),
            detail=(
                f"溯源公共文件数。恒等于 shard_count×2+1（当前 {config.shard_count}），"
                "不随内容增长，只有改动分片配置才会越界。"
            ),
            structural=True,
        ),
        Gauge(
            name="lineage_shard_bytes",
            limit=config.shard_max_bytes,
            used=_largest_file_bytes(lineage_public / "clusters", "*.json"),
            detail="最大的单个 cluster 分片。这一项才真正决定前端下钻的单次请求大小。",
        ),
        Gauge(
            name="lineage_index_bytes",
            limit=config.index_max_bytes,
            used=(
                (lineage_public / "index.json").stat().st_size
                if (lineage_public / "index.json").is_file()
                else None
            ),
            detail="溯源索引。每次下钻都要先取它，因此它先于分片影响首屏。",
        ),
        Gauge(
            name="public_tree_bytes",
            limit=_MAX_PUBLIC_TREE_BYTES,
            used=_tree_bytes(public_tree),
            detail="构建产物总字节，随文章数持续增长。",
            required=False,
        ),
        Gauge(
            name="public_tree_files",
            limit=_MAX_PUBLIC_FILES,
            used=_tree_files(public_tree),
            detail="构建产物文件数。",
            required=False,
        ),
    ]
    missing = [gauge.name for gauge in gauges if gauge.required and gauge.used is None]
    if missing:
        raise CapacityError(f"required capacity gauges could not be measured: {', '.join(missing)}")
    return gauges


def build_report(
    gauges: Sequence[Gauge],
    *,
    warning: float = WARNING_RATIO,
    critical: float = CRITICAL_RATIO,
) -> dict[str, object]:
    rows = []
    for gauge in gauges:
        ratio = gauge.ratio
        rows.append(
            {
                "name": gauge.name,
                "limit": gauge.limit,
                "used": gauge.used,
                "ratio": None if ratio is None else round(ratio, 4),
                "status": gauge.status(warning=warning, critical=critical),
                "detail": gauge.detail,
            }
        )
    statuses = {str(row["status"]) for row in rows}
    if "critical" in statuses:
        overall = "critical"
    elif "warning" in statuses:
        overall = "warning"
    elif "unavailable" in statuses:
        # Not ok: something asked for could not be read.
        overall = "unavailable"
    else:
        overall = "ok"
    return {
        "status": overall,
        "warning_ratio": warning,
        "critical_ratio": critical,
        "gauges": rows,
    }


def summarize(report: dict[str, object]) -> str:
    raw = report.get("gauges")
    rows: list[dict[str, Any]] = list(raw) if isinstance(raw, list) else []
    noteworthy = {"warning", "critical", "unavailable"}
    interesting = [row for row in rows if row["status"] in noteworthy]
    lines = [
        "以下容量水位已越过预警线。硬上限一旦触及，发布会直接失败，"
        "因此请把它当作排期项而不是故障。",
        "",
        "| 指标 | 已用 / 上限 | 占比 | 状态 |",
        "| --- | --- | --- | --- |",
    ]
    for row in interesting or rows:
        ratio = row["ratio"]
        percent = "—" if ratio is None else f"{float(ratio) * 100:.1f}%"
        used = "无法测量" if row["used"] is None else f"{row['used']:,}"
        lines.append(
            f"| `{row['name']}` | {used} / {row['limit']:,} | {percent} | {row['status']} |"
        )
    lines.append("")
    for row in interesting:
        lines.append(f"- **{row['name']}**：{row['detail']}")
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=str(PROJECT_ROOT))
    parser.add_argument("--warning-ratio", type=float, default=WARNING_RATIO)
    parser.add_argument("--critical-ratio", type=float, default=CRITICAL_RATIO)
    parser.add_argument("--summary-output")
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
        gauges = collect_gauges(Path(args.repository_root))
        report = build_report(
            gauges,
            warning=args.warning_ratio,
            critical=args.critical_ratio,
        )
    except (CapacityError, OSError, ValueError) as exc:
        print(f"capacity_report: {exc}", file=sys.stderr)
        return 2
    if args.summary_output:
        try:
            with open(args.summary_output, "w", encoding="utf-8") as handle:
                handle.write(summarize(report))
        except OSError as exc:
            print(f"capacity_report: cannot write summary: {exc}", file=sys.stderr)
            return 2
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    status = str(report["status"])
    if args.fail_on == "critical" and status == "critical":
        return 1
    if args.fail_on == "warning" and status in {"warning", "critical", "unavailable"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
