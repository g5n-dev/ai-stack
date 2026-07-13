#!/usr/bin/env python3
"""Build deterministic static intelligence API artifacts from a JSON bundle."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from processor.intelligence import (  # noqa: E402
    IntelligenceValidationError,
    build_static_intelligence,
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
    parser = argparse.ArgumentParser(
        description=(
            "Generate byte-stable /api/v1 intelligence files. "
            "--as-of is required so output never silently claims current data."
        )
    )
    parser.add_argument("--input", required=True, type=Path, help="JSON bundle path")
    parser.add_argument("--output", required=True, type=Path, help="static output root")
    parser.add_argument("--as-of", required=True, help="ISO-8601 data cutoff with timezone")
    parser.add_argument("--release-id", help="safe immutable release identifier")
    parser.add_argument("--base-url", default="", help="optional absolute public site URL")
    parser.add_argument(
        "--max-items-per-shard",
        type=_positive_integer,
        default=500,
    )
    parser.add_argument(
        "--max-shard-bytes",
        type=_positive_integer,
        default=1_048_576,
    )
    return parser


def _object_array(bundle: dict[str, Any], key: str) -> Sequence[dict[str, Any]]:
    value = bundle.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise IntelligenceValidationError(f"{key} must be an array of objects")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        with args.input.open("r", encoding="utf-8") as input_file:
            bundle = json.load(input_file)
        if not isinstance(bundle, dict):
            raise IntelligenceValidationError("input root must be an object")

        result = build_static_intelligence(
            output_dir=args.output,
            events=_object_array(bundle, "events"),
            entities=_object_array(bundle, "entities"),
            graph=_object_array(bundle, "graph"),
            as_of=args.as_of,
            release_id=args.release_id,
            base_url=args.base_url,
            max_items_per_shard=args.max_items_per_shard,
            max_shard_bytes=args.max_shard_bytes,
        )
    except (OSError, json.JSONDecodeError, IntelligenceValidationError) as exc:
        print(f"build_intelligence: {exc}", file=sys.stderr)
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
