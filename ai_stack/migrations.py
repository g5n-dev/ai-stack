from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .inventory import scan_markdown_inventory
from .stores import UnsafeStorePathError

_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
_BACKUP_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_MAX_FILE_BYTES = 2 * 1024 * 1024


class MigrationSafetyError(RuntimeError):
    """Raised before a migration can mutate data unsafely."""


def _git_head(path: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip().casefold()
    return value if result.returncode == 0 and _GIT_SHA.fullmatch(value) else None


def _seed_manifest_sha(path: Path) -> str | None:
    for parent in (path, *path.parents):
        candidate = parent / "seed-manifest.json"
        if candidate.is_file() and not candidate.is_symlink():
            try:
                value = json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                return None
            if isinstance(value, dict):
                source_sha = value.get("expected_source_sha")
                if isinstance(source_sha, str) and _GIT_SHA.fullmatch(source_sha):
                    return source_sha
        if parent.name == "content":
            break
    return None


def source_revision(path: Path) -> str | None:
    return _git_head(path) or _seed_manifest_sha(path)


def validate_execution_gate(
    *,
    execute: bool,
    expected_source_sha: str | None,
    backup_id: str | None,
    max_changes: int | None,
    actual_source_sha: str | None,
) -> None:
    if not execute:
        return
    missing = [
        flag
        for flag, value in (
            ("--expected-source-sha", expected_source_sha),
            ("--backup-id", backup_id),
            ("--max-changes", max_changes),
        )
        if value is None
    ]
    if missing:
        raise MigrationSafetyError("--execute requires " + ", ".join(missing))
    if not isinstance(expected_source_sha, str) or not _GIT_SHA.fullmatch(
        expected_source_sha.casefold()
    ):
        raise MigrationSafetyError("--expected-source-sha must be a full Git SHA")
    if not isinstance(backup_id, str) or not _BACKUP_ID.fullmatch(backup_id):
        raise MigrationSafetyError("--backup-id must be a safe identifier")
    if (
        not isinstance(max_changes, int)
        or isinstance(max_changes, bool)
        or not 1 <= max_changes <= 10_000
    ):
        raise MigrationSafetyError("--max-changes must be between 1 and 10000")
    if actual_source_sha != expected_source_sha.casefold():
        raise MigrationSafetyError(
            f"source SHA mismatch: expected {expected_source_sha}, found {actual_source_sha}"
        )


def _markdown_files(root: Path) -> list[Path]:
    if root.is_symlink() or not root.is_dir():
        raise UnsafeStorePathError(f"migration source must be a regular directory: {root}")
    files: list[Path] = []
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained: list[str] = []
        for name in sorted(directory_names):
            path = current_path / name
            if path.is_symlink():
                raise UnsafeStorePathError(f"migration source contains symlink: {path}")
            retained.append(name)
        directory_names[:] = retained
        for name in sorted(file_names):
            path = current_path / name
            details = path.lstat()
            if path.is_symlink() or not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
                raise UnsafeStorePathError(f"migration source contains unsafe file: {path}")
            if path.suffix.casefold() != ".md":
                continue
            if details.st_size > _MAX_FILE_BYTES:
                raise MigrationSafetyError(f"migration source file is too large: {path}")
            files.append(path)
    return files


def _file_manifest(root: Path, paths: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in paths:
        payload = path.read_bytes()
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return records


def _atomic_copy(source: Path, destination: Path) -> None:
    if destination.is_symlink() or destination.exists():
        raise MigrationSafetyError(f"migration refuses to overwrite: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.parent.is_symlink():
        raise MigrationSafetyError(f"migration destination crosses a symlink: {destination}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(source.read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, destination)
    finally:
        Path(temporary_name).unlink(missing_ok=True)


def _write_manifest(path: Path, value: dict[str, Any]) -> None:
    if path.exists() or path.is_symlink():
        raise MigrationSafetyError(f"migration refuses to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    finally:
        Path(temporary_name).unlink(missing_ok=True)


def copy_content_migration(
    *,
    migration: str,
    source_root: Path,
    target_root: Path,
    execute: bool,
    expected_source_sha: str | None,
    backup_id: str | None,
    max_changes: int | None,
) -> dict[str, Any]:
    if migration not in {"seed-content", "restore"}:
        raise ValueError(f"unsupported copy migration: {migration}")
    paths = _markdown_files(source_root)
    actual_source_sha = source_revision(source_root)
    validate_execution_gate(
        execute=execute,
        expected_source_sha=expected_source_sha,
        backup_id=backup_id,
        max_changes=max_changes,
        actual_source_sha=actual_source_sha,
    )
    records = _file_manifest(source_root, paths)
    if execute and max_changes is not None and len(records) > max_changes:
        raise MigrationSafetyError(
            f"planned changes exceed --max-changes: {len(records)}>{max_changes}"
        )
    destination = target_root / "content/posts"
    for record in records:
        target = destination / str(record["path"])
        if target.exists() or target.is_symlink():
            raise MigrationSafetyError(f"migration refuses to overwrite: {target}")
    if execute:
        for source in paths:
            _atomic_copy(source, destination / source.relative_to(source_root))
        _write_manifest(
            target_root / "content/seed-manifest.json",
            {
                "schema_version": "content_seed_v1",
                "migration": migration,
                "backup_id": backup_id,
                "expected_source_sha": expected_source_sha,
                "file_count": len(records),
                "files": records,
            },
        )
    return {
        "schema_version": "migration_plan_v1",
        "migration": migration,
        "source_root": str(source_root.absolute()),
        "target_root": str(target_root.absolute()),
        "dry_run": not execute,
        "mutation_performed": execute and bool(records),
        "planned_changes": len(records),
        "files": records,
        "safety_gate": (
            {
                "expected_source_sha": expected_source_sha,
                "backup_id": backup_id,
                "max_changes": max_changes,
            }
            if execute
            else None
        ),
    }


def dedupe_plan(content_root: Path) -> dict[str, Any]:
    report = scan_markdown_inventory(content_root, dry_run=True)
    report["migration"] = "dedupe"
    report["execution_blocked"] = "requires_24_shadow_runs_and_7_day_soak"
    report["mutation_performed"] = False
    return report


__all__ = [
    "MigrationSafetyError",
    "copy_content_migration",
    "dedupe_plan",
    "source_revision",
    "validate_execution_gate",
]
