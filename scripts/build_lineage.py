#!/usr/bin/env python3
"""Build deterministic internal and public intelligence-lineage assets."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_stack.lineage import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    LineageValidationError,
    apply_lineage_post_metadata,
    build_lineage_assets,
)


def _git_first_seen(content_root: Path) -> dict[Path, str]:
    try:
        relative = content_root.resolve().relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        return {}
    try:
        shallow = subprocess.run(
            ["git", "rev-parse", "--is-shallow-repository"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return {}
    # A depth-one checkout reports every tracked Post as added by the shallow
    # boundary commit.  Treating that boundary as first-seen time advances
    # last_seen_at and makes the committed registry differ between local and
    # CI builds.  Post metadata and the existing registry remain the safe
    # fallback until complete history is available.
    if shallow.stdout.strip().casefold() != "false":
        return {}
    command = [
        "git",
        "log",
        "--diff-filter=A",
        "--format=__LINEAGE_COMMIT__%aI",
        "--name-only",
        "--",
        (relative / "posts").as_posix(),
    ]
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return {}
    current: str | None = None
    first_seen: dict[Path, str] = {}
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("__LINEAGE_COMMIT__"):
            current = line.removeprefix("__LINEAGE_COMMIT__")
            continue
        if current is None or not line.endswith(".md"):
            continue
        path = (PROJECT_ROOT / line).resolve()
        first_seen.setdefault(path, current)
    return first_seen


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-root", type=Path, default=Path("blog/content"))
    parser.add_argument("--internal-output", type=Path, default=Path("data/lineage"))
    parser.add_argument("--public-output", type=Path, default=Path("blog/static/data/lineage"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument(
        "--as-of",
        help="optional ISO-8601 cutoff; defaults to the latest eligible Post timestamp",
    )
    parser.add_argument(
        "--apply-post-metadata",
        action="store_true",
        help="explicitly backfill active Post lineage metadata after a successful build",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = build_lineage_assets(
            content_root=args.content_root,
            internal_dir=args.internal_output,
            public_dir=args.public_output,
            config_path=args.config,
            as_of=args.as_of,
            first_seen_by_path=_git_first_seen(args.content_root),
        )
        if args.apply_post_metadata:
            result["post_metadata"] = apply_lineage_post_metadata(
                content_root=args.content_root,
                internal_dir=args.internal_output,
                apply=True,
            )
    except (OSError, ValueError, LineageValidationError) as exc:
        print(f"build_lineage: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
