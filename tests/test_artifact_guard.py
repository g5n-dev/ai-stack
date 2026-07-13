from __future__ import annotations

from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import tarfile

import pytest

from scripts.artifact_guard import (
    ArtifactPolicy,
    ArtifactValidationError,
    validate_tar_artifact,
)


def _write_tar(
    path: Path,
    entries: list[tuple[str, bytes, int, str]],
) -> dict[str, str]:
    digests: dict[str, str] = {}
    with tarfile.open(path, "w") as archive:
        for name, payload, mode, kind in entries:
            info = tarfile.TarInfo(name)
            info.mode = mode
            if kind == "directory":
                info.type = tarfile.DIRTYPE
                archive.addfile(info)
                continue
            if kind == "symlink":
                info.type = tarfile.SYMTYPE
                info.linkname = "../../.github/workflows/release.yml"
                archive.addfile(info)
                continue
            info.size = len(payload)
            archive.addfile(info, BytesIO(payload))
            digests[name] = sha256(payload).hexdigest()
    return digests


def _policy(**overrides: object) -> ArtifactPolicy:
    defaults: dict[str, object] = {
        "allowed_roots": ("content", "state"),
        "allowed_suffixes": (".json", ".md"),
        "max_files": 5,
        "max_file_bytes": 4_096,
        "max_total_bytes": 8_192,
        "required_json_fields": {
            "content/events/*.json": frozenset({"schema_version", "event_id"}),
        },
    }
    defaults.update(overrides)
    return ArtifactPolicy(**defaults)


def _valid_event() -> bytes:
    return json.dumps({"schema_version": "1", "event_id": "evt_1"}).encode()


def test_accepts_exact_allowlisted_artifact(tmp_path: Path) -> None:
    artifact = tmp_path / "handoff.tar"
    expected = _write_tar(
        artifact,
        [
            ("content/events/evt_1.json", _valid_event(), 0o644, "file"),
            ("state/run.md", b"validated\n", 0o600, "file"),
        ],
    )

    report = validate_tar_artifact(
        artifact,
        policy=_policy(),
        expected_archive_sha256=sha256(artifact.read_bytes()).hexdigest(),
        expected_files=expected,
    )

    assert report.file_count == 2
    assert report.total_bytes == len(_valid_event()) + len(b"validated\n")
    assert report.files == tuple(sorted(expected))


@pytest.mark.parametrize(
    ("name", "mode", "kind", "reason"),
    [
        ("../.github/workflows/pwn.yml", 0o644, "file", "unsafe path"),
        ("/content/events/evt.json", 0o644, "file", "unsafe path"),
        ("content/events/link.json", 0o777, "symlink", "non-regular"),
        ("content/events/evt.json", 0o755, "file", "executable"),
        (".github/workflows/pwn.json", 0o644, "file", "outside allowed roots"),
        ("content/events/payload.sh", 0o644, "file", "disallowed suffix"),
    ],
)
def test_rejects_dangerous_members(
    tmp_path: Path,
    name: str,
    mode: int,
    kind: str,
    reason: str,
) -> None:
    artifact = tmp_path / "handoff.tar"
    expected = _write_tar(artifact, [(name, _valid_event(), mode, kind)])

    with pytest.raises(ArtifactValidationError, match=reason):
        validate_tar_artifact(artifact, policy=_policy(), expected_files=expected)


def test_rejects_duplicate_member_names(tmp_path: Path) -> None:
    artifact = tmp_path / "handoff.tar"
    payload = _valid_event()
    _write_tar(
        artifact,
        [
            ("content/events/evt.json", payload, 0o644, "file"),
            ("content/events/evt.json", payload, 0o644, "file"),
        ],
    )

    with pytest.raises(ArtifactValidationError, match="duplicate path"):
        validate_tar_artifact(
            artifact,
            policy=_policy(),
            expected_files={"content/events/evt.json": sha256(payload).hexdigest()},
        )


def test_rejects_digest_and_manifest_mismatch(tmp_path: Path) -> None:
    artifact = tmp_path / "handoff.tar"
    expected = _write_tar(
        artifact,
        [("content/events/evt.json", _valid_event(), 0o644, "file")],
    )
    expected["content/events/evt.json"] = "0" * 64

    with pytest.raises(ArtifactValidationError, match="digest mismatch"):
        validate_tar_artifact(artifact, policy=_policy(), expected_files=expected)

    with pytest.raises(ArtifactValidationError, match="archive digest mismatch"):
        validate_tar_artifact(
            artifact,
            policy=_policy(),
            expected_archive_sha256="f" * 64,
            expected_files={},
        )


def test_rejects_missing_or_extra_manifest_files(tmp_path: Path) -> None:
    artifact = tmp_path / "handoff.tar"
    _write_tar(
        artifact,
        [("content/events/evt.json", _valid_event(), 0o644, "file")],
    )

    with pytest.raises(ArtifactValidationError, match="manifest file set mismatch"):
        validate_tar_artifact(
            artifact,
            policy=_policy(),
            expected_files={"content/events/other.json": "0" * 64},
        )


@pytest.mark.parametrize(
    ("payload", "reason"),
    [
        (b"not-json", "invalid JSON"),
        (json.dumps({"schema_version": "1"}).encode(), "missing required JSON fields"),
        (json.dumps({"schema_version": "1", "event_id": "evt", "token": "ghp_abcdefghijklmnopqrstuvwxyz1234567890"}).encode(), "secret-like content"),
    ],
)
def test_rejects_invalid_schema_mime_and_secrets(
    tmp_path: Path,
    payload: bytes,
    reason: str,
) -> None:
    artifact = tmp_path / "handoff.tar"
    expected = _write_tar(
        artifact,
        [("content/events/evt.json", payload, 0o644, "file")],
    )

    with pytest.raises(ArtifactValidationError, match=reason):
        validate_tar_artifact(artifact, policy=_policy(), expected_files=expected)


def test_rejects_file_count_and_size_limits(tmp_path: Path) -> None:
    artifact = tmp_path / "handoff.tar"
    payload = _valid_event()
    expected = _write_tar(
        artifact,
        [
            ("content/events/a.json", payload, 0o644, "file"),
            ("content/events/b.json", payload, 0o644, "file"),
        ],
    )

    with pytest.raises(ArtifactValidationError, match="too many files"):
        validate_tar_artifact(artifact, policy=_policy(max_files=1), expected_files=expected)

    with pytest.raises(ArtifactValidationError, match="file too large"):
        validate_tar_artifact(
            artifact,
            policy=_policy(max_file_bytes=len(payload) - 1),
            expected_files=expected,
        )

    with pytest.raises(ArtifactValidationError, match="artifact too large"):
        validate_tar_artifact(
            artifact,
            policy=_policy(max_total_bytes=(len(payload) * 2) - 1),
            expected_files=expected,
        )


@pytest.mark.parametrize(
    "changes",
    [
        {"allowed_roots": ("../content",)},
        {"allowed_suffixes": (".svg",)},
        {"max_files": 0},
    ],
)
def test_rejects_unsafe_policy_configuration(changes: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        _policy(**changes)


def test_accepts_directory_entries_but_does_not_count_them(tmp_path: Path) -> None:
    artifact = tmp_path / "handoff.tar"
    payload = _valid_event()
    expected = _write_tar(
        artifact,
        [
            ("content/events", b"", 0o755, "directory"),
            ("content/events/evt.json", payload, 0o644, "file"),
        ],
    )

    report = validate_tar_artifact(artifact, policy=_policy(), expected_files=expected)

    assert report.file_count == 1


@pytest.mark.parametrize("payload", [b"bad\x00text", b"\xff\xfe"])
def test_rejects_non_text_markdown(tmp_path: Path, payload: bytes) -> None:
    artifact = tmp_path / "handoff.tar"
    expected = _write_tar(
        artifact,
        [("content/post.md", payload, 0o644, "file")],
    )

    with pytest.raises(ArtifactValidationError, match="invalid text MIME"):
        validate_tar_artifact(artifact, policy=_policy(), expected_files=expected)


def test_rejects_non_object_json_when_schema_requires_fields(tmp_path: Path) -> None:
    artifact = tmp_path / "handoff.tar"
    payload = b"[]"
    expected = _write_tar(
        artifact,
        [("content/events/evt.json", payload, 0o644, "file")],
    )

    with pytest.raises(ArtifactValidationError, match="JSON object required"):
        validate_tar_artifact(artifact, policy=_policy(), expected_files=expected)


def test_rejects_invalid_tar_and_image_mime(tmp_path: Path) -> None:
    invalid_tar = tmp_path / "invalid.tar"
    invalid_tar.write_bytes(b"not a tar archive")
    with pytest.raises(ArtifactValidationError, match="invalid tar"):
        validate_tar_artifact(invalid_tar, policy=_policy(), expected_files={})

    image_tar = tmp_path / "image.tar"
    expected = _write_tar(
        image_tar,
        [("content/media/image.png", b"not-png", 0o644, "file")],
    )
    with pytest.raises(ArtifactValidationError, match="invalid image MIME"):
        validate_tar_artifact(
            image_tar,
            policy=_policy(allowed_suffixes=(".json", ".md", ".png")),
            expected_files=expected,
        )


def test_accepts_allowlisted_png_magic(tmp_path: Path) -> None:
    artifact = tmp_path / "image.tar"
    payload = b"\x89PNG\r\n\x1a\n" + b"safe-payload"
    expected = _write_tar(
        artifact,
        [("content/media/image.png", payload, 0o644, "file")],
    )

    report = validate_tar_artifact(
        artifact,
        policy=_policy(allowed_suffixes=(".json", ".md", ".png")),
        expected_files=expected,
    )

    assert report.file_count == 1
