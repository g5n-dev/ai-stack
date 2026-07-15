#!/usr/bin/env python3
"""Plan or safely apply deterministic historical Markdown repairs."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_stack.historical_repair import (  # noqa: E402
    apply_historical_repair_plan,
    build_historical_repair_batch,
    build_historical_repair_plan,
    write_repair_manifest,
)
from ai_stack.migrations import MigrationSafetyError  # noqa: E402
from ai_stack.stores import UnsafeStorePathError  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--content-root",
        type=Path,
        default=PROJECT_ROOT / "blog/content/posts",
        help="Hugo posts directory (default: blog/content/posts)",
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        help="Optional audit manifest path; omitted by default so dry-run performs zero writes",
    )
    parser.add_argument("--apply", action="store_true", help="Apply the reviewed plan")
    parser.add_argument(
        "--batch",
        action="store_true",
        help=(
            "Select the largest deterministic prefix of complete canonical URL groups "
            "that fits --max-changes; repeat after each committed batch"
        ),
    )
    parser.add_argument("--expected-source-sha")
    parser.add_argument("--expected-code-sha")
    parser.add_argument("--backup-id")
    parser.add_argument("--max-changes", type=int)
    parser.add_argument("--shadow-evidence-root", type=Path)
    parser.add_argument(
        "--backup-root",
        type=Path,
        default=PROJECT_ROOT / ".artifacts/historical-repair",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.batch:
            if args.max_changes is None:
                raise MigrationSafetyError("--batch requires --max-changes")
            plan = build_historical_repair_batch(
                content_root=args.content_root,
                max_changes=args.max_changes,
            )
        else:
            plan = build_historical_repair_plan(content_root=args.content_root)
        if args.manifest_output is not None:
            write_repair_manifest(args.manifest_output, plan.manifest)
        if args.apply:
            result = apply_historical_repair_plan(
                plan,
                expected_source_sha=args.expected_source_sha,
                expected_code_sha=args.expected_code_sha,
                backup_id=args.backup_id,
                max_changes=args.max_changes,
                shadow_evidence_root=args.shadow_evidence_root,
                backup_root=args.backup_root,
            )
            output = {"plan": plan.manifest, "result": result}
        else:
            output = plan.manifest
    except (MigrationSafetyError, UnsafeStorePathError, OSError, ValueError) as exc:
        print(f"historical-repair: rejected: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
