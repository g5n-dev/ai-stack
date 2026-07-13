from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from ai_stack import migrations
from ai_stack.migrations import MigrationSafetyError
from ai_stack.stores import UnsafeStorePathError

SHA = "a" * 40


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"expected_source_sha": "short"}, "full Git SHA"),
        ({"backup_id": "../unsafe"}, "safe identifier"),
        ({"max_changes": 0}, "between 1"),
        ({"max_changes": 10_001}, "between 1"),
        ({"actual_source_sha": "b" * 40}, "source SHA mismatch"),
    ],
)
def test_execution_gate_rejects_invalid_or_stale_authority(
    changes: dict[str, object], message: str
) -> None:
    values: dict[str, object] = {
        "execute": True,
        "expected_source_sha": SHA,
        "backup_id": "backup-1",
        "max_changes": 1,
        "actual_source_sha": SHA,
    }
    values.update(changes)

    with pytest.raises(MigrationSafetyError, match=message):
        migrations.validate_execution_gate(**values)  # type: ignore[arg-type]


def test_execution_gate_is_noop_for_dry_run_and_requires_every_execute_field() -> None:
    migrations.validate_execution_gate(
        execute=False,
        expected_source_sha=None,
        backup_id=None,
        max_changes=None,
        actual_source_sha=None,
    )
    with pytest.raises(MigrationSafetyError, match="--backup-id"):
        migrations.validate_execution_gate(
            execute=True,
            expected_source_sha=SHA,
            backup_id=None,
            max_changes=1,
            actual_source_sha=SHA,
        )


def test_source_revision_reads_seed_manifest_and_rejects_malformed_manifest(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (content / "seed-manifest.json").write_text(
        json.dumps({"expected_source_sha": SHA}), encoding="utf-8"
    )
    assert migrations.source_revision(posts) == SHA

    (content / "seed-manifest.json").write_text("{", encoding="utf-8")
    assert migrations.source_revision(posts) is None


def test_copy_migration_rejects_symlink_roots_files_and_oversized_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = tmp_path / "real"
    real.mkdir()
    linked = tmp_path / "linked"
    linked.symlink_to(real, target_is_directory=True)
    with pytest.raises(UnsafeStorePathError, match="regular directory"):
        migrations.copy_content_migration(
            migration="seed-content",
            source_root=linked,
            target_root=tmp_path / "target",
            execute=False,
            expected_source_sha=None,
            backup_id=None,
            max_changes=None,
        )

    outside = tmp_path / "outside.md"
    outside.write_text("outside", encoding="utf-8")
    (real / "linked.md").symlink_to(outside)
    with pytest.raises(UnsafeStorePathError, match="unsafe file"):
        migrations.copy_content_migration(
            migration="seed-content",
            source_root=real,
            target_root=tmp_path / "target",
            execute=False,
            expected_source_sha=None,
            backup_id=None,
            max_changes=None,
        )
    (real / "linked.md").unlink()

    large = real / "large.md"
    large.write_bytes(b"xx")
    monkeypatch.setattr(migrations, "_MAX_FILE_BYTES", 1)
    with pytest.raises(MigrationSafetyError, match="too large"):
        migrations.copy_content_migration(
            migration="seed-content",
            source_root=real,
            target_root=tmp_path / "target",
            execute=False,
            expected_source_sha=None,
            backup_id=None,
            max_changes=None,
        )


def test_copy_migration_rejects_change_limit_and_existing_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "one.md").write_text("one", encoding="utf-8")
    (source / "two.md").write_text("two", encoding="utf-8")
    monkeypatch.setattr(migrations, "source_revision", lambda _path: SHA)

    with pytest.raises(MigrationSafetyError, match="exceed"):
        migrations.copy_content_migration(
            migration="seed-content",
            source_root=source,
            target_root=tmp_path / "target",
            execute=True,
            expected_source_sha=SHA,
            backup_id="backup-1",
            max_changes=1,
        )

    destination = tmp_path / "existing/content/posts"
    destination.mkdir(parents=True)
    (destination / "one.md").write_text("old", encoding="utf-8")
    with pytest.raises(MigrationSafetyError, match="overwrite"):
        migrations.copy_content_migration(
            migration="restore",
            source_root=source,
            target_root=tmp_path / "existing",
            execute=True,
            expected_source_sha=SHA,
            backup_id="backup-1",
            max_changes=2,
        )


def test_atomic_copy_and_manifest_never_overwrite_or_cross_symlinks(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.md"
    source.write_text("safe", encoding="utf-8")
    existing = tmp_path / "existing.md"
    existing.write_text("old", encoding="utf-8")
    with pytest.raises(MigrationSafetyError, match="overwrite"):
        migrations._atomic_copy(source, existing)

    target = tmp_path / "target"
    target.mkdir()
    linked_parent = tmp_path / "linked-parent"
    linked_parent.symlink_to(target, target_is_directory=True)
    with pytest.raises(MigrationSafetyError, match="symlink"):
        migrations._atomic_copy(source, linked_parent / "copy.md")

    manifest = tmp_path / "manifest.json"
    migrations._write_manifest(manifest, {"safe": True})
    assert json.loads(manifest.read_text(encoding="utf-8")) == {"safe": True}
    with pytest.raises(MigrationSafetyError, match="overwrite"):
        migrations._write_manifest(manifest, {"safe": False})


def test_hardlinked_source_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    first = source / "first.md"
    second = source / "second.md"
    first.write_text("same", encoding="utf-8")
    os.link(first, second)

    with pytest.raises(UnsafeStorePathError, match="unsafe file"):
        migrations.copy_content_migration(
            migration="seed-content",
            source_root=source,
            target_root=tmp_path / "target",
            execute=False,
            expected_source_sha=None,
            backup_id=None,
            max_changes=None,
        )
