"""Explicit-path, fast-forward-only Git writer for content and ops ledgers."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
from typing import Sequence


class UnsafeWriteError(RuntimeError):
    """Raised before staging when the worktree violates the writer policy."""


class CASConflictError(RuntimeError):
    """Raised when the expected parent is stale or a normal push is rejected."""


@dataclass(frozen=True)
class CASCommit:
    changed: bool
    commit_sha: str
    parent_sha: str
    paths: tuple[str, ...]


_FULL_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_MAX_FILES = 5_000
_MAX_FILE_BYTES = 4 * 1024 * 1024
_MAX_TOTAL_BYTES = 64 * 1024 * 1024


class GitCASWriter:
    """Prepare and push one Git commit without merge, rebase, reset, or force."""

    def __init__(
        self,
        repository: Path | str,
        *,
        branch: str,
        allowed_roots: Sequence[str],
    ) -> None:
        self.repository = Path(repository).resolve()
        if not allowed_roots or any(
            not root or "/" in root or "\\" in root or root in {".", ".."}
            for root in allowed_roots
        ):
            raise UnsafeWriteError("allowed roots must be simple relative names")
        self.allowed_roots = frozenset(allowed_roots)
        self.branch = branch
        branch_check = self._run(
            ["check-ref-format", "--branch", branch],
            check=False,
            text=True,
        )
        if branch_check.returncode != 0:
            raise UnsafeWriteError(f"invalid branch name: {branch!r}")

        top = self._run(["rev-parse", "--show-toplevel"], check=False, text=True)
        if top.returncode != 0:
            raise UnsafeWriteError(f"not a Git repository: {self.repository}")
        if Path(top.stdout.strip()).resolve() != self.repository:
            raise UnsafeWriteError("writer must be initialized at the Git worktree root")
        current_branch = self._run(
            ["symbolic-ref", "--quiet", "--short", "HEAD"],
            check=False,
            text=True,
        )
        if current_branch.returncode != 0 or current_branch.stdout.strip() != branch:
            actual = current_branch.stdout.strip() or "DETACHED"
            raise UnsafeWriteError(f"writer branch mismatch: expected {branch}, found {actual}")

    def _run(
        self,
        args: Sequence[str],
        *,
        check: bool,
        text: bool,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", "-C", str(self.repository), *args],
            check=check,
            capture_output=True,
            text=text,
            env=env,
        )

    def _git_text(self, *args: str) -> str:
        result = self._run(args, check=True, text=True)
        assert isinstance(result.stdout, str)
        return result.stdout.strip()

    def _git_bytes(self, *args: str) -> bytes:
        result = self._run(args, check=True, text=False)
        assert isinstance(result.stdout, bytes)
        return result.stdout

    def _head(self) -> str:
        head = self._git_text("rev-parse", "HEAD")
        if not _FULL_SHA.fullmatch(head):
            raise UnsafeWriteError("Git returned an invalid HEAD")
        return head

    @staticmethod
    def _decode_paths(raw: bytes) -> set[str]:
        try:
            return {path.decode("utf-8") for path in raw.split(b"\0") if path}
        except UnicodeDecodeError as exc:
            raise UnsafeWriteError("non-UTF-8 Git path is not allowed") from exc

    def _changed_paths(self) -> tuple[str, ...]:
        tracked = self._decode_paths(
            self._git_bytes("diff", "--name-only", "-z", "HEAD", "--")
        )
        untracked = self._decode_paths(
            self._git_bytes("ls-files", "--others", "--exclude-standard", "-z", "--")
        )
        return tuple(sorted(tracked | untracked))

    def _validate_path(self, raw_path: str) -> int:
        path = PurePosixPath(raw_path)
        if (
            not raw_path
            or path.is_absolute()
            or any(part in {"", ".", "..", ".git", ".github"} for part in path.parts)
            or any(ord(character) < 32 for character in raw_path)
            or path.parts[0] not in self.allowed_roots
        ):
            raise UnsafeWriteError(f"path outside writer allowlist: {raw_path!r}")
        absolute = self.repository.joinpath(*path.parts)
        try:
            details = absolute.lstat()
        except OSError as exc:
            raise UnsafeWriteError(f"deletions are not allowed: {raw_path}") from exc
        if not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
            raise UnsafeWriteError(f"only regular, single-link files are allowed: {raw_path}")
        if details.st_mode & 0o111:
            raise UnsafeWriteError(f"executable files are not allowed: {raw_path}")
        if details.st_size > _MAX_FILE_BYTES:
            raise UnsafeWriteError(f"file exceeds writer size limit: {raw_path}")
        return details.st_size

    def commit(self, *, expected_base: str, message: str) -> CASCommit:
        actual_base = self._head()
        if not _FULL_SHA.fullmatch(expected_base) or actual_base != expected_base:
            raise CASConflictError(
                f"expected parent {expected_base}, found {actual_base}"
            )
        if not message.strip() or len(message) > 200:
            raise UnsafeWriteError("commit message must contain 1-200 characters")

        paths = self._changed_paths()
        if not paths:
            return CASCommit(False, actual_base, actual_base, ())
        if len(paths) > _MAX_FILES:
            raise UnsafeWriteError("writer file-count limit exceeded")
        total_bytes = sum(self._validate_path(path) for path in paths)
        if total_bytes > _MAX_TOTAL_BYTES:
            raise UnsafeWriteError("writer total-size limit exceeded")

        deleted = self._decode_paths(
            self._git_bytes(
                "diff",
                "--no-renames",
                "--diff-filter=D",
                "--name-only",
                "-z",
                "HEAD",
                "--",
            )
        )
        if deleted:
            raise UnsafeWriteError(f"deletions are not allowed: {sorted(deleted)}")

        for path in paths:
            self._run(["add", "--", path], check=True, text=True)
            staged_body = self._git_bytes("show", f":{path}")
            worktree_body = self.repository.joinpath(*PurePosixPath(path).parts).read_bytes()
            if not hashlib.sha256(staged_body).digest() == hashlib.sha256(
                worktree_body
            ).digest():
                raise UnsafeWriteError(f"Git filter changed staged bytes: {path}")

        staged = self._decode_paths(
            self._git_bytes("diff", "--cached", "--name-only", "-z", "HEAD", "--")
        )
        if staged != set(paths):
            raise UnsafeWriteError("staged path set differs from validated path set")
        if self._head() != expected_base:
            raise CASConflictError("expected parent changed while preparing commit")

        environment = os.environ.copy()
        environment.update(
            {
                "GIT_AUTHOR_NAME": "ai-stack writer",
                "GIT_AUTHOR_EMAIL": "ai-stack-writer@users.noreply.github.com",
                "GIT_COMMITTER_NAME": "ai-stack writer",
                "GIT_COMMITTER_EMAIL": "ai-stack-writer@users.noreply.github.com",
            }
        )
        self._run(
            [
                "-c",
                "commit.gpgsign=false",
                "-c",
                "core.hooksPath=/dev/null",
                "commit",
                "-m",
                message.strip(),
            ],
            check=True,
            text=True,
            env=environment,
        )
        commit_sha = self._head()
        parent = self._git_text("rev-parse", f"{commit_sha}^")
        if parent != expected_base:
            raise CASConflictError("created commit is not based on the expected parent")
        return CASCommit(True, commit_sha, parent, paths)

    def push(self, commit: CASCommit, *, remote: str = "origin") -> None:
        if not commit.changed:
            return
        parent = self._git_text("rev-parse", f"{commit.commit_sha}^")
        if parent != commit.parent_sha:
            raise CASConflictError("commit parent changed before push")
        result = self._run(
            ["push", "--porcelain", remote, f"{commit.commit_sha}:refs/heads/{self.branch}"],
            check=False,
            text=True,
        )
        if result.returncode != 0:
            detail = " ".join((result.stdout or "", result.stderr or "")).strip()
            raise CASConflictError(f"fast-forward push rejected: {detail}")
