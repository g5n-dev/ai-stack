from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

from ._json import json_ready
from .inventory import scan_markdown_inventory, write_inventory_report
from .stores import FileContentStore, FileOpsStore, StoreError


PIPELINE_STEPS = (
    "discover",
    "generate",
    "validate",
    "persist",
    "build",
    "deploy",
    "health",
    "notify",
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-stack")
    commands = parser.add_subparsers(dest="command", required=True)

    for name in ("status", "validate"):
        command = commands.add_parser(name)
        command.add_argument("--state-root", type=Path, default=Path(".ai-stack"))

    resume = commands.add_parser("resume")
    resume.add_argument("--state-root", type=Path, default=Path(".ai-stack"))
    resume.add_argument("--run-id", required=True)

    migrate = commands.add_parser("migrate")
    migration = migrate.add_subparsers(dest="migration", required=True)
    inventory = migration.add_parser("inventory")
    inventory.add_argument(
        "content_root", type=Path, nargs="?", default=Path("blog/content/posts")
    )
    inventory.add_argument("--output", type=Path)
    inventory.add_argument("--execute", action="store_true")
    inventory.add_argument("--expected-source-sha")
    inventory.add_argument("--backup-id")
    inventory.add_argument("--max-changes", type=int)
    return parser


def _print_json(value: Any) -> None:
    print(json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, indent=2))


def _store_status(path: Path, store_type: type[Any]) -> dict[str, Any]:
    if not path.exists():
        return {"present": False, "base_revision": None, "record_counts": {}}
    store = store_type(path)
    return {"present": True, **json_ready(store.status())}


def _status(state_root: Path) -> int:
    _print_json(
        {
            "content": _store_status(state_root / "content", FileContentStore),
            "ops": _store_status(state_root / "ops", FileOpsStore),
        }
    )
    return 0


def _store_validation(path: Path, store_type: type[Any]) -> dict[str, Any]:
    if not path.exists():
        return {
            "present": False,
            "valid": True,
            "base_revision": None,
            "record_counts": {},
            "errors": [],
        }
    return {"present": True, **json_ready(store_type(path).validate())}


def _validate(state_root: Path) -> int:
    content = _store_validation(state_root / "content", FileContentStore)
    ops = _store_validation(state_root / "ops", FileOpsStore)
    valid = bool(content["valid"] and ops["valid"])
    _print_json({"valid": valid, "content": content, "ops": ops})
    return 0 if valid else 1


def _resume(state_root: Path, run_id: str) -> int:
    content_path = state_root / "content"
    if not content_path.exists():
        print("content ledger does not exist", file=sys.stderr)
        return 1
    run = FileContentStore(content_path).get_run(run_id)
    if run is None:
        print(f"run not found: {run_id}", file=sys.stderr)
        return 1
    _print_json(
        {
            "run_id": run.run_id,
            "status": run.status,
            "next_step": run.next_incomplete_step(PIPELINE_STEPS),
            "read_only": True,
        }
    )
    return 0


def _git_head(path: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _inventory(args: argparse.Namespace) -> int:
    if args.execute:
        missing = [
            flag
            for flag, value in (
                ("--expected-source-sha", args.expected_source_sha),
                ("--backup-id", args.backup_id),
                ("--max-changes", args.max_changes),
            )
            if value is None
        ]
        if missing:
            print(
                "--execute requires " + ", ".join(missing),
                file=sys.stderr,
            )
            return 2
        if args.max_changes <= 0:
            print("--max-changes must be greater than zero", file=sys.stderr)
            return 2
        actual_head = _git_head(args.content_root)
        if actual_head is None or actual_head != args.expected_source_sha:
            print(
                f"source SHA mismatch: expected {args.expected_source_sha}, found {actual_head}",
                file=sys.stderr,
            )
            return 3

    report = scan_markdown_inventory(args.content_root, dry_run=not args.execute)
    if args.execute:
        report["safety_gate"] = {
            "backup_id": args.backup_id,
            "expected_source_sha": args.expected_source_sha,
            "max_changes": args.max_changes,
        }
    if args.output:
        write_inventory_report(args.output, report)
    _print_json(report)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "status":
            return _status(args.state_root)
        if args.command == "validate":
            return _validate(args.state_root)
        if args.command == "resume":
            return _resume(args.state_root, args.run_id)
        if args.command == "migrate" and args.migration == "inventory":
            return _inventory(args)
    except (OSError, ValueError, StoreError) as error:
        print(str(error), file=sys.stderr)
        return 1
    raise AssertionError("unreachable command")


if __name__ == "__main__":
    raise SystemExit(main())
