#!/usr/bin/env python3
"""Generate the Hugo data file used for O(1) related-post lookup."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from processor.related_index import (  # noqa: E402
    RelatedIndexValidationError,
    build_related_index,
)


def _positive_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=PROJECT_ROOT / "blog/content/posts",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "blog/data/related/index.json",
    )
    parser.add_argument("--section", default="posts")
    parser.add_argument("--max-related", type=_positive_integer, default=6)
    parser.add_argument("--candidate-window", type=_positive_integer, default=100)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = build_related_index(
            args.content_dir,
            output_path=args.output,
            section=args.section,
            max_related=args.max_related,
            candidate_window=args.candidate_window,
        )
    except (OSError, UnicodeError, RelatedIndexValidationError) as exc:
        print(f"build_related_index: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "output": str(args.output),
                "post_count": payload["post_count"],
                "content_sha256": payload["content_sha256"],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
