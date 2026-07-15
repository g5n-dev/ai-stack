#!/usr/bin/env python3
"""Build the Hugo data manifest that quarantines unverifiable archive bodies."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ai_stack.content_quality import write_content_quality_manifest  # noqa: E402


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--content-root",
        type=Path,
        default=Path("blog/content"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("blog/data/content_quality.json"),
    )
    args = parser.parse_args(argv)

    manifest = write_content_quality_manifest(args.content_root, args.output)
    print(
        "content quality manifest: "
        f"sources={manifest['source_file_count']} "
        f"quarantined={manifest['quarantined_count']} "
        f"archived={manifest['archived_count']} "
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
