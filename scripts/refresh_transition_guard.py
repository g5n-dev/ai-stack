#!/usr/bin/env python3
"""拒绝刷新候选相对已检出基线的破坏性 Post 转换。"""

from __future__ import annotations

import argparse
import json
import stat
import sys
from collections.abc import Sequence
from pathlib import Path


class RefreshTransitionError(ValueError):
    """刷新候选删除或异常膨胀时抛出。"""


def _post_names(root: Path | str, label: str) -> frozenset[str]:
    directory = Path(root)
    if directory.is_symlink() or not directory.is_dir():
        raise RefreshTransitionError(f"{label} Post directory is invalid")
    names: set[str] = set()
    for item in directory.iterdir():
        if item.name == ".gitkeep" and item.is_file() and not item.is_symlink():
            continue
        details = item.lstat()
        if (
            item.is_symlink()
            or not stat.S_ISREG(details.st_mode)
            or details.st_nlink != 1
            or item.suffix.casefold() != ".md"
        ):
            raise RefreshTransitionError(
                f"{label} must contain only regular Markdown Posts"
            )
        names.add(item.name)
    return frozenset(names)


def validate_post_transition(
    baseline_root: Path | str,
    candidate_root: Path | str,
    *,
    max_added: int = 500,
    max_added_percent: int = 35,
) -> dict[str, int]:
    if max_added < 0 or not 0 <= max_added_percent <= 100:
        raise RefreshTransitionError("refresh transition limits are invalid")
    baseline = _post_names(baseline_root, "baseline")
    candidate = _post_names(candidate_root, "candidate")
    if not candidate:
        raise RefreshTransitionError("refresh candidate must be non-empty")
    removed = baseline.difference(candidate)
    if removed:
        raise RefreshTransitionError("refresh candidate must not delete existing Posts")
    added = candidate.difference(baseline)
    if len(added) > max_added:
        raise RefreshTransitionError("refresh candidate adds more than 500 Posts")
    if len(added) * 100 > len(baseline) * max_added_percent:
        raise RefreshTransitionError("refresh candidate additions exceed 35% of baseline")
    return {
        "baseline": len(baseline),
        "candidate": len(candidate),
        "added": len(added),
        "removed": 0,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--max-added", type=int, default=500)
    parser.add_argument("--max-added-percent", type=int, default=35)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        report = validate_post_transition(
            args.baseline,
            args.candidate,
            max_added=args.max_added,
            max_added_percent=args.max_added_percent,
        )
    except (OSError, RefreshTransitionError) as exc:
        print(f"refresh-transition: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
