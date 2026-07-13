from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from ._json import json_ready
from .inventory import scan_markdown_inventory, write_inventory_report
from .migrations import (
    MigrationSafetyError,
    copy_content_migration,
    dedupe_plan,
)
from .pipeline import (
    PipelineError,
    crawl,
    generate,
    persist_discovery,
    persist_receipt,
    persist_release,
    persist_result,
    publish,
    render,
    reserve_budget,
    validate_discovery,
    validate_generated,
)
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

    status = commands.add_parser("status")
    status.add_argument("--state-root", type=Path, default=Path(".ai-stack"))

    validate = commands.add_parser("validate")
    validate.add_argument("--state-root", type=Path, default=Path(".ai-stack"))
    validate.add_argument("--kind", choices=("discovery", "generated"))
    validate.add_argument("--input", type=Path)
    validate.add_argument("--output", type=Path)
    validate.add_argument("--publisher-config", type=Path, default=Path("config/publisher.yaml"))

    resume = commands.add_parser("resume")
    resume.add_argument("--state-root", type=Path, default=Path(".ai-stack"))
    resume.add_argument("--run-id", required=True)

    crawl_command = commands.add_parser("crawl")
    crawl_command.add_argument("--run-id", required=True)
    crawl_command.add_argument("--output", type=Path, required=True)
    crawl_command.add_argument("--config", type=Path, default=Path("config/sources.yaml"))
    crawl_command.add_argument("--runtime-profile")

    process = commands.add_parser("process")
    process.add_argument(
        "--phase",
        choices=(
            "persist-discovery",
            "reserve-budget",
            "generate",
            "persist-result",
            "persist-release",
            "persist-receipt",
        ),
        required=True,
    )
    process.add_argument("--run-id", required=True)
    process.add_argument("--input", type=Path, required=True)
    process.add_argument("--state-root", type=Path)
    process.add_argument("--ops-root", type=Path)
    process.add_argument("--output", type=Path)
    process.add_argument("--expected-release-id")
    process.add_argument("--expected-code-sha")
    process.add_argument("--expected-content-sha")
    process.add_argument("--expected-artifact-digest")

    render_command = commands.add_parser("render")
    render_command.add_argument("--run-id", required=True)
    render_command.add_argument("--code-sha", required=True)
    render_command.add_argument("--content-sha", required=True)
    render_command.add_argument("--ops-sha", required=True)
    render_command.add_argument("--content-root", type=Path, required=True)
    render_command.add_argument("--ops-root", type=Path, required=True)
    render_command.add_argument("--output", type=Path, required=True)
    render_command.add_argument("--site-static-root", type=Path, default=Path("blog/static"))

    publish_command = commands.add_parser("publish")
    publish_command.add_argument("--run-id", required=True)
    publish_command.add_argument("--input", type=Path, required=True)
    publish_command.add_argument("--output", type=Path, required=True)
    publish_command.add_argument("--config", type=Path, default=Path("config/publisher.yaml"))

    migrate = commands.add_parser("migrate")
    migration = migrate.add_subparsers(dest="migration", required=True)
    inventory = migration.add_parser("inventory")
    inventory.add_argument("content_root", type=Path, nargs="?", default=Path("blog/content/posts"))
    inventory.add_argument("--output", type=Path)
    inventory.add_argument("--execute", action="store_true")
    inventory.add_argument("--expected-source-sha")
    inventory.add_argument("--backup-id")
    inventory.add_argument("--max-changes", type=int)

    for name in ("seed-content", "restore"):
        copy = migration.add_parser(name)
        copy.add_argument("source_root", type=Path)
        copy.add_argument("--target-root", type=Path, required=True)
        copy.add_argument("--execute", action="store_true")
        copy.add_argument("--expected-source-sha")
        copy.add_argument("--backup-id")
        copy.add_argument("--max-changes", type=int)

    dedupe = migration.add_parser("dedupe")
    dedupe.add_argument("content_root", type=Path, nargs="?", default=Path("blog/content/posts"))
    dedupe.add_argument("--execute", action="store_true")
    dedupe.add_argument("--expected-source-sha")
    dedupe.add_argument("--backup-id")
    dedupe.add_argument("--max-changes", type=int)
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


def _require_phase_path(args: argparse.Namespace, field: str, phase: str) -> Path:
    value = getattr(args, field)
    if not isinstance(value, Path):
        raise PipelineError(f"process --phase {phase} requires --{field.replace('_', '-')}")
    return value


def _require_phase_text(args: argparse.Namespace, field: str, phase: str) -> str:
    value = getattr(args, field)
    if not isinstance(value, str) or not value:
        raise PipelineError(f"process --phase {phase} requires --{field.replace('_', '-')}")
    return value


def _process(args: argparse.Namespace) -> int:
    phase = str(args.phase)
    if phase == "persist-discovery":
        result = persist_discovery(
            run_id=args.run_id,
            input_root=args.input,
            state_root=_require_phase_path(args, "state_root", phase),
        )
    elif phase == "reserve-budget":
        result = reserve_budget(
            run_id=args.run_id,
            input_root=args.input,
            state_root=_require_phase_path(args, "state_root", phase),
        )
    elif phase == "generate":
        result = generate(
            run_id=args.run_id,
            input_root=args.input,
            ops_root=_require_phase_path(args, "ops_root", phase),
            output=_require_phase_path(args, "output", phase),
        )
    elif phase == "persist-result":
        result = persist_result(
            run_id=args.run_id,
            input_root=args.input,
            state_root=_require_phase_path(args, "state_root", phase),
        )
    elif phase == "persist-release":
        result = persist_release(
            run_id=args.run_id,
            input_root=args.input,
            state_root=_require_phase_path(args, "state_root", phase),
            expected_release_id=_require_phase_text(args, "expected_release_id", phase),
            expected_code_sha=_require_phase_text(args, "expected_code_sha", phase),
            expected_content_sha=_require_phase_text(args, "expected_content_sha", phase),
            expected_artifact_digest=_require_phase_text(
                args, "expected_artifact_digest", phase
            ),
        )
    elif phase == "persist-receipt":
        result = persist_receipt(
            run_id=args.run_id,
            input_root=args.input,
            state_root=_require_phase_path(args, "state_root", phase),
        )
    else:
        raise AssertionError("unreachable process phase")
    _print_json(result)
    return 0


def _validate_command(args: argparse.Namespace) -> int:
    if args.kind is None:
        if args.input is not None or args.output is not None:
            raise PipelineError("validate --input/--output requires --kind")
        return _validate(args.state_root)
    if not isinstance(args.input, Path) or not isinstance(args.output, Path):
        raise PipelineError("validate --kind requires --input and --output")
    if args.kind == "discovery":
        result = validate_discovery(input_root=args.input, output=args.output)
    else:
        result = validate_generated(
            input_root=args.input,
            output=args.output,
            publisher_config=args.publisher_config,
        )
    _print_json(result)
    return 0


def _migration(args: argparse.Namespace) -> int:
    if args.migration == "inventory":
        return _inventory(args)
    if args.migration in {"seed-content", "restore"}:
        result = copy_content_migration(
            migration=args.migration,
            source_root=args.source_root,
            target_root=args.target_root,
            execute=args.execute,
            expected_source_sha=args.expected_source_sha,
            backup_id=args.backup_id,
            max_changes=args.max_changes,
        )
        _print_json(result)
        return 0
    if args.migration == "dedupe":
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
                raise MigrationSafetyError("--execute requires " + ", ".join(missing))
            raise MigrationSafetyError(
                "dedupe execution is blocked until 24 shadow runs and the 7-day soak complete"
            )
        _print_json(dedupe_plan(args.content_root))
        return 0
    raise AssertionError("unreachable migration")


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "status":
            return _status(args.state_root)
        if args.command == "validate":
            return _validate_command(args)
        if args.command == "resume":
            return _resume(args.state_root, args.run_id)
        if args.command == "crawl":
            result = crawl(
                run_id=args.run_id,
                output=args.output,
                config_path=args.config,
                runtime_profile=args.runtime_profile,
            )
            _print_json(result)
            return 0
        if args.command == "process":
            return _process(args)
        if args.command == "render":
            result = render(
                run_id=args.run_id,
                code_sha=args.code_sha,
                content_sha=args.content_sha,
                ops_sha=args.ops_sha,
                content_root=args.content_root,
                ops_root=args.ops_root,
                output=args.output,
                site_static_root=args.site_static_root,
            )
            _print_json(result)
            return 0
        if args.command == "publish":
            result = publish(
                run_id=args.run_id,
                input_root=args.input,
                output=args.output,
                config_path=args.config,
            )
            _print_json(result)
            return 0
        if args.command == "migrate":
            return _migration(args)
    except MigrationSafetyError as error:
        print(str(error), file=sys.stderr)
        return 2
    except (OSError, TypeError, ValueError, PipelineError, StoreError) as error:
        print(str(error), file=sys.stderr)
        return 1
    raise AssertionError("unreachable command")


if __name__ == "__main__":
    raise SystemExit(main())
