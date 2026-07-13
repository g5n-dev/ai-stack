"""Bounded break-glass deletion for the content ledger.

This is deliberately separate from normal writers, which never permit deletion.
Execution requires an exact content SHA and a verified, external backup record.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
from collections.abc import Sequence
from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path, PurePosixPath
from typing import Any


class DeletionSafetyError(RuntimeError):
    """Raised before deletion when a break-glass invariant is not satisfied."""


_FULL_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_BACKUP_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_RELEASE_URL = re.compile(
    r"https://github\.com/g5n-dev/ai-stack/releases/tag/[A-Za-z0-9._-]+\Z"
)
_ALLOWED_REASONS = frozenset({"secret_leakage", "pii", "legal_request"})
_BACKUP_FIELDS = frozenset(
    {
        "schema_version",
        "backup_id",
        "source_sha",
        "archive_sha256",
        "verified_at",
        "immutable_release_url",
    }
)


def _git(
    repository: Path,
    *arguments: str,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=check,
        capture_output=True,
        text=True,
        env=env,
    )


def _git_text(repository: Path, *arguments: str) -> str:
    try:
        return _git(repository, *arguments).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise DeletionSafetyError(f"Git safety check failed: {' '.join(arguments)}") from exc


def _git_bytes(repository: Path, *arguments: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise DeletionSafetyError(f"Git safety check failed: {' '.join(arguments)}") from exc
    return result.stdout


def _validate_repository(repository: Path, expected_source_sha: str) -> None:
    if not _FULL_SHA.fullmatch(expected_source_sha):
        raise DeletionSafetyError("expected source SHA must be a full Git object ID")
    root = _git_text(repository, "rev-parse", "--show-toplevel")
    if Path(root).resolve() != repository:
        raise DeletionSafetyError("repository must be the Git worktree root")
    branch = _git_text(repository, "symbolic-ref", "--quiet", "--short", "HEAD")
    if branch != "content":
        raise DeletionSafetyError(f"content branch required, found {branch or 'DETACHED'}")
    head = _git_text(repository, "rev-parse", "HEAD")
    if head != expected_source_sha:
        raise DeletionSafetyError(
            f"source SHA mismatch: expected {expected_source_sha}, found {head}"
        )
    if _git_text(repository, "status", "--porcelain=v1", "--untracked-files=all"):
        raise DeletionSafetyError("content worktree must be clean before deletion")
    remote = _git_text(repository, "ls-remote", "--heads", "origin", "refs/heads/content")
    remote_sha = remote.split(maxsplit=1)[0] if remote else ""
    if remote_sha != expected_source_sha:
        raise DeletionSafetyError(
            "remote content source SHA mismatch; refresh the checkout and approval inputs"
        )


def _validate_backup(
    backup_record: Path,
    *,
    backup_id: str,
    expected_source_sha: str,
) -> dict[str, str]:
    if not _BACKUP_ID.fullmatch(backup_id):
        raise DeletionSafetyError("backup ID contains unsafe characters")
    try:
        details = backup_record.lstat()
        if not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
            raise DeletionSafetyError("backup record must be a regular single-link file")
        if details.st_size <= 0 or details.st_size > 64 * 1024:
            raise DeletionSafetyError("backup record size is invalid")
        raw = backup_record.read_text(encoding="utf-8")
        payload: Any = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DeletionSafetyError("backup record is missing or invalid") from exc
    if not isinstance(payload, dict) or frozenset(payload) != _BACKUP_FIELDS:
        raise DeletionSafetyError("backup record schema is invalid")
    if not all(isinstance(payload[field], str) for field in _BACKUP_FIELDS):
        raise DeletionSafetyError("backup record values must be strings")
    typed = {field: payload[field] for field in _BACKUP_FIELDS}
    if typed["schema_version"] != "backup_record_v1":
        raise DeletionSafetyError("backup record schema version is unsupported")
    if typed["backup_id"] != backup_id:
        raise DeletionSafetyError("backup ID mismatch")
    if typed["source_sha"] != expected_source_sha:
        raise DeletionSafetyError("backup record source SHA mismatch")
    if not re.fullmatch(r"[0-9a-f]{64}", typed["archive_sha256"]):
        raise DeletionSafetyError("backup record archive digest is invalid")
    if not _RELEASE_URL.fullmatch(typed["immutable_release_url"]):
        raise DeletionSafetyError("backup record immutable release URL is invalid")
    try:
        verified_at = datetime.fromisoformat(typed["verified_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise DeletionSafetyError("backup record verification timestamp is invalid") from exc
    if verified_at.tzinfo is None or verified_at.utcoffset() is None:
        raise DeletionSafetyError("backup record verification timestamp must include UTC")
    if verified_at.utcoffset() != timedelta(0):
        raise DeletionSafetyError("backup record verification timestamp must be UTC")
    if not typed["immutable_release_url"].endswith(f"/tag/{backup_id}"):
        raise DeletionSafetyError("backup record release tag does not match backup ID")
    return typed


def _validate_target(repository: Path, target_path: str) -> tuple[Path, str]:
    path = PurePosixPath(target_path)
    if (
        not target_path
        or path.is_absolute()
        or "\\" in target_path
        or any(part in {"", ".", "..", ".git", ".github"} for part in path.parts)
        or any(ord(character) < 32 for character in target_path)
        or len(path.parts) < 2
        or path.parts[0] != "content"
    ):
        raise DeletionSafetyError(f"unsafe target path: {target_path!r}")
    absolute = repository.joinpath(*path.parts)
    try:
        details = absolute.lstat()
    except OSError as exc:
        raise DeletionSafetyError(f"target is missing: {target_path}") from exc
    if not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
        raise DeletionSafetyError("target must be a regular single-link file")
    tracked = _git(repository, "ls-files", "--error-unmatch", "--", target_path, check=False)
    if tracked.returncode != 0 or tracked.stdout.strip() != target_path:
        raise DeletionSafetyError("target must be exactly one tracked content file")
    committed = _git_bytes(repository, "show", f"HEAD:{target_path}")
    current = absolute.read_bytes()
    if sha256(committed).digest() != sha256(current).digest():
        raise DeletionSafetyError("target bytes differ from the approved source commit")
    return absolute, sha256(current).hexdigest()


def delete_content(
    *,
    repository: Path | str,
    target_path: str,
    reason: str,
    expected_source_sha: str,
    backup_id: str,
    backup_record: Path | str,
    max_changes: int,
    execute: bool = False,
) -> dict[str, object]:
    """Validate and optionally delete one file through a normal FF-only push."""

    repo = Path(repository).resolve()
    # Preserve the final path component so ``lstat`` can reject a symlinked record.
    record = Path(backup_record).absolute()
    if reason not in _ALLOWED_REASONS:
        raise DeletionSafetyError("deletion reason is not an allowed break-glass reason")
    if not 1 <= max_changes <= 100:
        raise DeletionSafetyError("max_changes must be between 1 and 100")
    if max_changes != 1:
        raise DeletionSafetyError("this command deletes exactly one path; max_changes must be 1")

    _validate_repository(repo, expected_source_sha)
    backup = _validate_backup(
        record,
        backup_id=backup_id,
        expected_source_sha=expected_source_sha,
    )
    target, target_digest = _validate_target(repo, target_path)
    result: dict[str, object] = {
        "schema_version": "break_glass_deletion_v1",
        "dry_run": not execute,
        "branch": "content",
        "source_sha": expected_source_sha,
        "target_path": target_path,
        "target_sha256": target_digest,
        "reason": reason,
        "backup_id": backup["backup_id"],
        "backup_archive_sha256": backup["archive_sha256"],
        "change_count": 1,
    }
    if not execute:
        return result

    target.unlink()
    try:
        _git(repo, "add", "-u", "--", target_path)
        staged = _git_text(
            repo,
            "diff",
            "--cached",
            "--no-renames",
            "--name-status",
            "HEAD",
            "--",
        ).splitlines()
        if staged != [f"D\t{target_path}"]:
            raise DeletionSafetyError("staged deletion differs from the approved target")
        if _git_text(repo, "rev-parse", "HEAD") != expected_source_sha:
            raise DeletionSafetyError("source SHA changed while preparing deletion")
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_AUTHOR_NAME": "ai-stack break-glass writer",
                "GIT_AUTHOR_EMAIL": "ai-stack-writer@users.noreply.github.com",
                "GIT_COMMITTER_NAME": "ai-stack break-glass writer",
                "GIT_COMMITTER_EMAIL": "ai-stack-writer@users.noreply.github.com",
            }
        )
        message = f"delete(content): {reason} [{backup_id}]"
        _git(
            repo,
            "-c",
            "commit.gpgsign=false",
            "-c",
            "core.hooksPath=/dev/null",
            "commit",
            "-m",
            message,
            env=environment,
        )
        commit_sha = _git_text(repo, "rev-parse", "HEAD")
        if _git_text(repo, "rev-parse", f"{commit_sha}^") != expected_source_sha:
            raise DeletionSafetyError("deletion commit is not based on the approved source SHA")
        pushed = _git(
            repo,
            "push",
            "--porcelain",
            "origin",
            f"{commit_sha}:refs/heads/content",
            check=False,
        )
        if pushed.returncode != 0:
            detail = " ".join((pushed.stdout, pushed.stderr)).strip()
            raise DeletionSafetyError(
                "fast-forward deletion push was rejected; local evidence is retained: "
                f"{detail}"
            )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise DeletionSafetyError(
            "deletion transaction failed; inspect the local checkout without reset/rebase"
        ) from exc

    result["commit_sha"] = commit_sha
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--reason", choices=sorted(_ALLOWED_REASONS), required=True)
    parser.add_argument("--expected-source-sha", required=True)
    parser.add_argument("--backup-id", required=True)
    parser.add_argument("--backup-record", type=Path, required=True)
    parser.add_argument("--max-changes", type=int, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = delete_content(
            repository=args.repository,
            target_path=args.target_path,
            reason=args.reason,
            expected_source_sha=args.expected_source_sha,
            backup_id=args.backup_id,
            backup_record=args.backup_record,
            max_changes=args.max_changes,
            execute=args.execute,
        )
    except DeletionSafetyError as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
