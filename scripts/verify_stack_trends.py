#!/usr/bin/env python3
"""Verify local STACK trend assets without network or secret-bearing inputs."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from processor.stack_trends import (  # noqa: E402
    StackTrendsValidationError,
    verify_stack_trends,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("blog/static/data/stack-trends"),
    )
    parser.add_argument(
        "--verify-hashes",
        action="store_true",
        help="verify every referenced file's SHA-256 digest",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = verify_stack_trends(args.root, verify_hashes=args.verify_hashes)
    except (OSError, StackTrendsValidationError) as exc:
        print(f"verify_stack_trends: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
