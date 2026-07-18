#!/usr/bin/env python3
"""Build a pure-offline inventory for reviewed historical source recovery."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_stack.historical_rehydration import (  # noqa: E402
    HistoricalRehydrationError,
    build_historical_rehydration_inventory,
)
from ai_stack.inventory import write_inventory_report  # noqa: E402
from ai_stack.stores import UnsafeStorePathError  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        action="store_true",
        help="scan only; never fetch or rewrite historical content",
    )
    parser.add_argument(
        "--content-root",
        type=Path,
        default=PROJECT_ROOT / "blog/content/posts",
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=PROJECT_ROOT,
        help="local Git repository used only for the pinned HN history lookup",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="explicit audit output; omitted means a zero-write dry run",
    )
    return parser


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.inventory:
        parser.error("--inventory is required; recovery mutation is not implemented")
    content_root = args.content_root.resolve(strict=False)
    try:
        if args.output is not None:
            destination = args.output.resolve(strict=False)
            if _is_within(destination, content_root):
                raise HistoricalRehydrationError(
                    "inventory audit output must be outside --content-root"
                )
        report = build_historical_rehydration_inventory(
            content_root,
            repository_root=args.repository_root,
        )
        if args.output is not None:
            write_inventory_report(args.output, report)
    except (
        HistoricalRehydrationError,
        UnsafeStorePathError,
        FileNotFoundError,
        OSError,
        ValueError,
    ) as exc:
        print(f"historical-rehydration: rejected: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
