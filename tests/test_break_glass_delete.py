from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import scripts.break_glass_delete as deletion
from scripts.break_glass_delete import DeletionSafetyError, delete_content, main


def _git(path: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(path), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _repository(tmp_path: Path) -> tuple[Path, Path, str, Path]:
    repository = tmp_path / "ledger"
    remote = tmp_path / "remote.git"
    repository.mkdir()
    _git(repository, "init", "-b", "content")
    _git(repository, "config", "user.name", "Test")
    _git(repository, "config", "user.email", "test@example.test")
    target = repository / "content" / "posts" / "sensitive.md"
    target.parent.mkdir(parents=True)
    target.write_text("secret material\n", encoding="utf-8")
    _git(repository, "add", "--", "content/posts/sensitive.md")
    _git(repository, "commit", "-m", "seed")
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    _git(repository, "remote", "add", "origin", str(remote))
    _git(repository, "push", "-u", "origin", "content")
    source_sha = _git(repository, "rev-parse", "HEAD")
    backup = tmp_path / "backup.json"
    backup.write_text(
        json.dumps(
            {
                "schema_version": "backup_record_v1",
                "backup_id": "backup-20260713",
                "source_sha": source_sha,
                "archive_sha256": "a" * 64,
                "verified_at": "2026-07-13T08:00:00Z",
                "immutable_release_url": (
                    "https://github.com/g5n-dev/ai-stack/releases/tag/backup-20260713"
                ),
            }
        ),
        encoding="utf-8",
    )
    return repository, remote, source_sha, backup


def _arguments(repository: Path, source_sha: str, backup: Path) -> dict[str, object]:
    return {
        "repository": repository,
        "target_path": "content/posts/sensitive.md",
        "reason": "pii",
        "expected_source_sha": source_sha,
        "backup_id": "backup-20260713",
        "backup_record": backup,
        "max_changes": 1,
        "execute": False,
    }


def test_dry_run_is_default_and_does_not_change_repository(tmp_path: Path) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)

    result = delete_content(
        repository=repository,
        target_path="content/posts/sensitive.md",
        reason="pii",
        expected_source_sha=source_sha,
        backup_id="backup-20260713",
        backup_record=backup,
        max_changes=1,
        execute=False,
    )

    assert result["dry_run"] is True
    assert (repository / "content" / "posts" / "sensitive.md").is_file()
    assert _git(repository, "rev-parse", "HEAD") == source_sha
    assert _git(repository, "status", "--porcelain") == ""


def test_execute_deletes_one_file_with_normal_fast_forward_push(tmp_path: Path) -> None:
    repository, remote, source_sha, backup = _repository(tmp_path)

    result = delete_content(
        repository=repository,
        target_path="content/posts/sensitive.md",
        reason="legal_request",
        expected_source_sha=source_sha,
        backup_id="backup-20260713",
        backup_record=backup,
        max_changes=1,
        execute=True,
    )

    assert result["dry_run"] is False
    assert not (repository / "content" / "posts" / "sensitive.md").exists()
    remote_head = _git(remote, "rev-parse", "refs/heads/content")
    assert remote_head == result["commit_sha"]
    assert _git(repository, "rev-parse", "HEAD^") == source_sha


@pytest.mark.parametrize(
    ("changes", "reason"),
    [
        ({"target_path": "../main/.github/workflows/deploy.yml"}, "unsafe target"),
        ({"reason": "cleanup"}, "deletion reason"),
        ({"expected_source_sha": "0" * 40}, "source SHA mismatch"),
        ({"backup_id": "different"}, "backup ID mismatch"),
        ({"max_changes": 101}, "max_changes"),
    ],
)
def test_safety_gate_fails_before_mutation(
    tmp_path: Path,
    changes: dict[str, object],
    reason: str,
) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    arguments: dict[str, object] = {
        "repository": repository,
        "target_path": "content/posts/sensitive.md",
        "reason": "pii",
        "expected_source_sha": source_sha,
        "backup_id": "backup-20260713",
        "backup_record": backup,
        "max_changes": 1,
        "execute": True,
    }
    arguments.update(changes)

    with pytest.raises(DeletionSafetyError, match=reason):
        delete_content(**arguments)  # type: ignore[arg-type]

    assert (repository / "content" / "posts" / "sensitive.md").is_file()
    assert _git(repository, "rev-parse", "HEAD") == source_sha


def test_rejects_missing_target_and_tampered_backup(tmp_path: Path) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    payload = json.loads(backup.read_text(encoding="utf-8"))
    payload["archive_sha256"] = "not-a-digest"
    backup.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(DeletionSafetyError, match="backup record"):
        delete_content(
            repository=repository,
            target_path="content/posts/sensitive.md",
            reason="pii",
            expected_source_sha=source_sha,
            backup_id="backup-20260713",
            backup_record=backup,
            max_changes=1,
            execute=False,
        )

    backup.unlink()
    with pytest.raises(DeletionSafetyError, match="backup record"):
        delete_content(
            repository=repository,
            target_path="content/posts/missing.md",
            reason="pii",
            expected_source_sha=source_sha,
            backup_id="backup-20260713",
            backup_record=backup,
            max_changes=1,
            execute=False,
        )


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("schema_version", "backup_record_v0", "schema version"),
        ("source_sha", "0" * 40, "source SHA"),
        ("immutable_release_url", "https://example.test/backup", "release URL"),
        ("verified_at", "not-a-time", "timestamp"),
        ("verified_at", "2026-07-13T08:00:00", "include UTC"),
        ("verified_at", "2026-07-13T08:00:00+08:00", "must be UTC"),
    ],
)
def test_rejects_invalid_backup_record_fields(
    tmp_path: Path,
    field: str,
    value: str,
    reason: str,
) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    payload = json.loads(backup.read_text(encoding="utf-8"))
    payload[field] = value
    backup.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(DeletionSafetyError, match=reason):
        delete_content(**_arguments(repository, source_sha, backup))  # type: ignore[arg-type]


@pytest.mark.parametrize("mutation", ["extra", "non_string", "invalid_json", "empty"])
def test_rejects_malformed_backup_record(tmp_path: Path, mutation: str) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    if mutation == "extra":
        payload = json.loads(backup.read_text(encoding="utf-8"))
        payload["trusted"] = True
        backup.write_text(json.dumps(payload), encoding="utf-8")
    elif mutation == "non_string":
        payload = json.loads(backup.read_text(encoding="utf-8"))
        payload["archive_sha256"] = 123
        backup.write_text(json.dumps(payload), encoding="utf-8")
    elif mutation == "invalid_json":
        backup.write_text("{", encoding="utf-8")
    else:
        backup.write_bytes(b"")

    with pytest.raises(DeletionSafetyError, match="backup record"):
        delete_content(**_arguments(repository, source_sha, backup))  # type: ignore[arg-type]


def test_rejects_backup_symlink_and_mismatched_release_tag(tmp_path: Path) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    real = backup.with_name("real-backup.json")
    backup.rename(real)
    backup.symlink_to(real)
    with pytest.raises(DeletionSafetyError, match="regular single-link"):
        delete_content(**_arguments(repository, source_sha, backup))  # type: ignore[arg-type]

    backup.unlink()
    payload = json.loads(real.read_text(encoding="utf-8"))
    payload["immutable_release_url"] = (
        "https://github.com/g5n-dev/ai-stack/releases/tag/another-backup"
    )
    backup.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(DeletionSafetyError, match="release tag"):
        delete_content(**_arguments(repository, source_sha, backup))  # type: ignore[arg-type]


def test_rejects_repository_branch_dirty_remote_and_sha_invariants(tmp_path: Path) -> None:
    repository, remote, source_sha, backup = _repository(tmp_path)
    arguments = _arguments(repository, source_sha, backup)

    arguments["expected_source_sha"] = "short"
    with pytest.raises(DeletionSafetyError, match="full Git object"):
        delete_content(**arguments)  # type: ignore[arg-type]

    arguments["expected_source_sha"] = source_sha
    _git(repository, "switch", "-c", "not-content")
    with pytest.raises(DeletionSafetyError, match="content branch"):
        delete_content(**arguments)  # type: ignore[arg-type]
    _git(repository, "switch", "content")

    (repository / "untracked.txt").write_text("dirty", encoding="utf-8")
    with pytest.raises(DeletionSafetyError, match="must be clean"):
        delete_content(**arguments)  # type: ignore[arg-type]
    (repository / "untracked.txt").unlink()

    _git(remote, "update-ref", "-d", "refs/heads/content")
    with pytest.raises(DeletionSafetyError, match="remote content source SHA mismatch"):
        delete_content(**arguments)  # type: ignore[arg-type]


def test_rejects_non_root_repository_untracked_symlink_and_hardlink_targets(
    tmp_path: Path,
) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    arguments = _arguments(repository, source_sha, backup)
    arguments["repository"] = repository / "content"
    with pytest.raises(DeletionSafetyError, match="worktree root"):
        delete_content(**arguments)  # type: ignore[arg-type]

    arguments["repository"] = repository
    arguments["target_path"] = "content/posts/untracked.md"
    untracked = repository / "content" / "posts" / "untracked.md"
    untracked.write_text("untracked", encoding="utf-8")
    with pytest.raises(DeletionSafetyError, match="must be clean"):
        delete_content(**arguments)  # type: ignore[arg-type]
    untracked.unlink()

    target = repository / "content" / "posts" / "sensitive.md"
    target.unlink()
    target.symlink_to("elsewhere.md")
    with pytest.raises(DeletionSafetyError, match="must be clean"):
        delete_content(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "target_path",
    ["/content/post.md", "content\\post.md", "content", "state/post.md", "content/\x01.md"],
)
def test_rejects_unsafe_target_forms(tmp_path: Path, target_path: str) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    arguments = _arguments(repository, source_sha, backup)
    arguments["target_path"] = target_path
    with pytest.raises(DeletionSafetyError, match="unsafe target"):
        delete_content(**arguments)  # type: ignore[arg-type]


def test_rejects_invalid_backup_id_and_non_unit_change_limit(tmp_path: Path) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    arguments = _arguments(repository, source_sha, backup)
    arguments["backup_id"] = "../backup"
    with pytest.raises(DeletionSafetyError, match="backup ID"):
        delete_content(**arguments)  # type: ignore[arg-type]
    arguments["backup_id"] = "backup-20260713"
    arguments["max_changes"] = 2
    with pytest.raises(DeletionSafetyError, match="exactly one"):
        delete_content(**arguments)  # type: ignore[arg-type]


def test_cli_defaults_to_dry_run_and_reports_failure(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    cli = [
        "--repository",
        str(repository),
        "--target-path",
        "content/posts/sensitive.md",
        "--reason",
        "pii",
        "--expected-source-sha",
        source_sha,
        "--backup-id",
        "backup-20260713",
        "--backup-record",
        str(backup),
        "--max-changes",
        "1",
    ]
    assert main(cli) == 0
    assert json.loads(capsys.readouterr().out)["dry_run"] is True

    assert main([*cli, "--execute"]) == 0
    executed = json.loads(capsys.readouterr().out)
    assert executed["dry_run"] is False
    assert executed["commit_sha"]

    assert main(cli) == 2
    assert "source SHA mismatch" in capsys.readouterr().err


def test_push_rejection_retains_local_commit_for_forensics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository, _, source_sha, backup = _repository(tmp_path)
    real_git = deletion._git

    def reject_push(
        repo: Path,
        *arguments: str,
        check: bool = True,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        if arguments and arguments[0] == "push":
            return subprocess.CompletedProcess(
                ["git", *arguments],
                1,
                stdout="",
                stderr="non-fast-forward",
            )
        return real_git(repo, *arguments, check=check, env=env)

    monkeypatch.setattr(deletion, "_git", reject_push)
    arguments = _arguments(repository, source_sha, backup)
    arguments["execute"] = True
    with pytest.raises(DeletionSafetyError, match="fast-forward deletion push"):
        delete_content(**arguments)  # type: ignore[arg-type]

    assert _git(repository, "rev-parse", "HEAD^") == source_sha
    assert not (repository / "content" / "posts" / "sensitive.md").exists()
