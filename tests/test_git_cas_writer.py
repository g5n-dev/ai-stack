from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from scripts.git_cas_writer import (
    CASCommit,
    CASConflictError,
    GitCASWriter,
    UnsafeWriteError,
)


def _git(path: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _seed_remote(tmp_path: Path) -> tuple[Path, Path]:
    seed = tmp_path / "seed"
    remote = tmp_path / "remote.git"
    seed.mkdir()
    _git(seed, "init", "-b", "content")
    _git(seed, "config", "user.name", "Test Writer")
    _git(seed, "config", "user.email", "writer@example.test")
    (seed / "content").mkdir()
    (seed / "content" / "base.json").write_text('{"base":true}\n', encoding="utf-8")
    _git(seed, "add", "--", "content/base.json")
    _git(seed, "commit", "-m", "seed")
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    _git(seed, "remote", "add", "origin", str(remote))
    _git(seed, "push", "-u", "origin", "content")
    return seed, remote


def _clone(remote: Path, destination: Path) -> Path:
    subprocess.run(
        ["git", "clone", "--branch", "content", str(remote), str(destination)],
        check=True,
        capture_output=True,
    )
    return destination


def test_commits_only_allowlisted_files_and_noop_is_stable(tmp_path: Path) -> None:
    _, remote = _seed_remote(tmp_path)
    clone = _clone(remote, tmp_path / "clone")
    base = _git(clone, "rev-parse", "HEAD")
    (clone / "content" / "event.json").write_text('{"event_id":"evt"}\n', encoding="utf-8")
    writer = GitCASWriter(clone, branch="content", allowed_roots=("content", "state"))

    commit = writer.commit(expected_base=base, message="persist event")

    assert commit.changed
    assert commit.parent_sha == base
    assert commit.paths == ("content/event.json",)
    assert _git(clone, "diff", "--name-only") == ""
    writer.push(commit)
    assert _git(remote, "rev-parse", "refs/heads/content") == commit.commit_sha

    no_op = writer.commit(expected_base=commit.commit_sha, message="same state")
    assert not no_op.changed
    assert no_op.commit_sha == commit.commit_sha
    writer.push(no_op)


@pytest.mark.parametrize("kind", ["outside", "deletion", "symlink", "executable"])
def test_rejects_unsafe_worktree_changes(tmp_path: Path, kind: str) -> None:
    _, remote = _seed_remote(tmp_path)
    clone = _clone(remote, tmp_path / "clone")
    base = _git(clone, "rev-parse", "HEAD")
    writer = GitCASWriter(clone, branch="content", allowed_roots=("content", "state"))

    if kind == "outside":
        (clone / ".github" / "workflows").mkdir(parents=True)
        (clone / ".github" / "workflows" / "pwn.yml").write_text("pwn", encoding="utf-8")
    elif kind == "deletion":
        (clone / "content" / "base.json").unlink()
    elif kind == "symlink":
        (clone / "content" / "link.json").symlink_to("../../outside")
    else:
        path = clone / "content" / "run.json"
        path.write_text("{}\n", encoding="utf-8")
        path.chmod(0o755)

    with pytest.raises(UnsafeWriteError):
        writer.commit(expected_base=base, message="unsafe")


def test_rejects_wrong_expected_parent_before_staging(tmp_path: Path) -> None:
    _, remote = _seed_remote(tmp_path)
    clone = _clone(remote, tmp_path / "clone")
    (clone / "content" / "event.json").write_text("{}\n", encoding="utf-8")
    writer = GitCASWriter(clone, branch="content", allowed_roots=("content",))

    with pytest.raises(CASConflictError, match="expected parent"):
        writer.commit(expected_base="0" * 40, message="wrong base")

    assert _git(clone, "status", "--porcelain") == "?? content/event.json"


def test_two_writers_from_same_parent_cannot_overwrite_each_other(tmp_path: Path) -> None:
    _, remote = _seed_remote(tmp_path)
    clone_a = _clone(remote, tmp_path / "clone-a")
    clone_b = _clone(remote, tmp_path / "clone-b")
    base = _git(clone_a, "rev-parse", "HEAD")
    assert _git(clone_b, "rev-parse", "HEAD") == base

    (clone_a / "content" / "a.json").write_text('{"writer":"a"}\n', encoding="utf-8")
    (clone_b / "content" / "b.json").write_text('{"writer":"b"}\n', encoding="utf-8")
    writer_a = GitCASWriter(clone_a, branch="content", allowed_roots=("content",))
    writer_b = GitCASWriter(clone_b, branch="content", allowed_roots=("content",))
    commit_a = writer_a.commit(expected_base=base, message="writer a")
    commit_b = writer_b.commit(expected_base=base, message="writer b")

    writer_a.push(commit_a)
    with pytest.raises(CASConflictError, match="fast-forward push rejected"):
        writer_b.push(commit_b)

    inspection = _clone(remote, tmp_path / "inspection")
    assert (inspection / "content" / "a.json").is_file()
    assert not (inspection / "content" / "b.json").exists()
    assert (inspection / "content" / "base.json").is_file()


def test_refuses_wrong_branch_and_non_repository(tmp_path: Path) -> None:
    _, remote = _seed_remote(tmp_path)
    clone = _clone(remote, tmp_path / "clone")
    with pytest.raises(UnsafeWriteError, match="branch"):
        GitCASWriter(clone, branch="ops", allowed_roots=("ops",))

    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(UnsafeWriteError, match="Git repository"):
        GitCASWriter(empty, branch="content", allowed_roots=("content",))

    with pytest.raises(UnsafeWriteError, match="allowed roots"):
        GitCASWriter(clone, branch="content", allowed_roots=("../content",))
    with pytest.raises(UnsafeWriteError, match="invalid branch"):
        GitCASWriter(clone, branch="../content", allowed_roots=("content",))


def test_rejects_non_utf8_paths_invalid_messages_and_oversized_files(tmp_path: Path) -> None:
    with pytest.raises(UnsafeWriteError, match="non-UTF-8"):
        GitCASWriter._decode_paths(b"content/\xff.json\0")

    _, remote = _seed_remote(tmp_path)
    clone = _clone(remote, tmp_path / "clone")
    base = _git(clone, "rev-parse", "HEAD")
    writer = GitCASWriter(clone, branch="content", allowed_roots=("content",))
    (clone / "content" / "event.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(UnsafeWriteError, match="commit message"):
        writer.commit(expected_base=base, message="")

    (clone / "content" / "event.json").write_bytes(b"x" * (4 * 1024 * 1024 + 1))
    with pytest.raises(UnsafeWriteError, match="file exceeds"):
        writer.commit(expected_base=base, message="too large")


def test_push_verifies_recorded_parent(tmp_path: Path) -> None:
    _, remote = _seed_remote(tmp_path)
    clone = _clone(remote, tmp_path / "clone")
    base = _git(clone, "rev-parse", "HEAD")
    writer = GitCASWriter(clone, branch="content", allowed_roots=("content",))
    (clone / "content" / "event.json").write_text("{}\n", encoding="utf-8")
    commit = writer.commit(expected_base=base, message="event")
    forged = CASCommit(True, commit.commit_sha, "0" * 40, commit.paths)

    with pytest.raises(CASConflictError, match="parent changed"):
        writer.push(forged)
