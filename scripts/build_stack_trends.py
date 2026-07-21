#!/usr/bin/env python3
"""Build deterministic, progressively loaded trend insight assets."""

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
    DEFAULT_CONFIG_PATH,
    DEFAULT_LINEAGE_ROOT,
    StackTrendsValidationError,
    build_stack_trends,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-root", type=Path, default=Path("blog/content"))
    parser.add_argument(
        "--quality-manifest",
        type=Path,
        default=Path("blog/data/content_quality.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("blog/static/data/stack-trends"),
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--lineage-root",
        type=Path,
        default=DEFAULT_LINEAGE_ROOT,
        help="verified public lineage assets; missing index falls back to URL identity",
    )
    parser.add_argument(
        "--as-of",
        help=(
            "optional ISO-8601 calculation cutoff; defaults to the latest eligible "
            "Post timestamp so identical inputs produce identical bytes"
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = build_stack_trends(
            content_root=args.content_root,
            quality_manifest_path=args.quality_manifest,
            output_dir=args.output,
            config_path=args.config,
            lineage_root=args.lineage_root,
            as_of=args.as_of,
        )
    except (OSError, StackTrendsValidationError) as exc:
        print(f"build_stack_trends: {exc}", file=sys.stderr)
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
