#!/usr/bin/env python3
"""Verify deterministic lineage assets without network or secret-bearing inputs."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_stack.lineage import LineageValidationError, verify_lineage_assets  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-root", type=Path, default=Path("blog/static/data/lineage"))
    parser.add_argument("--internal-root", type=Path, default=Path("data/lineage"))
    parser.add_argument("--verify-hashes", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = verify_lineage_assets(
            args.public_root,
            internal_dir=args.internal_root,
            verify_hashes=args.verify_hashes,
        )
    except (OSError, ValueError, LineageValidationError) as exc:
        print(f"verify_lineage: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
