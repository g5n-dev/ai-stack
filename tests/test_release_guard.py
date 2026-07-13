from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import release_guard
from scripts.release_guard import (
    ReleaseDescriptor,
    ReleaseValidationError,
    assert_release_is_fresh,
    load_release_descriptor,
    main,
    write_release_descriptor,
)


CODE_A = "a" * 40
CODE_B = "b" * 40
CONTENT_A = "c" * 40
CONTENT_B = "d" * 40
ARTIFACT_A = "e" * 64
ARTIFACT_B = "f" * 64


def _release(
    sequence: int,
    *,
    code_sha: str = CODE_A,
    content_sha: str = CONTENT_A,
    artifact_digest: str = ARTIFACT_A,
) -> ReleaseDescriptor:
    return ReleaseDescriptor(
        code_sha=code_sha,
        content_sha=content_sha,
        schema_version="1.0",
        release_seq=sequence,
        artifact_digest=artifact_digest,
        generated_at="2026-07-13T08:00:00Z",
    )


def test_release_id_binds_sequence_and_exact_inputs() -> None:
    release = _release(42)

    assert release.release_id == f"r000000000042-{CODE_A[:12]}-{CONTENT_A[:12]}-{ARTIFACT_A[:12]}"
    assert release.to_dict()["release_id"] == release.release_id


def test_rejects_equal_or_late_release_sequence() -> None:
    current = _release(10)

    with pytest.raises(ReleaseValidationError, match="stale release sequence"):
        assert_release_is_fresh(_release(10, code_sha=CODE_B), current)
    with pytest.raises(ReleaseValidationError, match="stale release sequence"):
        assert_release_is_fresh(_release(9, code_sha=CODE_B), current)


def test_compensation_rollback_uses_higher_sequence_with_old_shas() -> None:
    current = _release(
        11,
        code_sha=CODE_B,
        content_sha=CONTENT_B,
        artifact_digest=ARTIFACT_B,
    )
    compensation = _release(12)

    assert_release_is_fresh(compensation, current)


@pytest.mark.parametrize(
    ("changes", "reason"),
    [
        ({"code_sha": "main"}, "code_sha"),
        ({"content_sha": "c" * 39}, "content_sha"),
        ({"artifact_digest": "e" * 63}, "artifact_digest"),
        ({"schema_version": "latest"}, "schema_version"),
        ({"release_seq": 0}, "release_seq"),
        ({"generated_at": "2026-07-13"}, "generated_at"),
    ],
)
def test_rejects_un_dict_malformed_release_identity(
    changes: dict[str, object],
    reason: str,
) -> None:
    values: dict[str, object] = {
        "code_sha": CODE_A,
        "content_sha": CONTENT_A,
        "schema_version": "1.0",
        "release_seq": 1,
        "artifact_digest": ARTIFACT_A,
        "generated_at": "2026-07-13T08:00:00Z",
    }
    values.update(changes)

    with pytest.raises(ReleaseValidationError, match=reason):
        ReleaseDescriptor(**values)  # type: ignore[arg-type]


def test_round_trip_is_canonical_and_refuses_forged_release_id(tmp_path: Path) -> None:
    path = tmp_path / "release.json"
    release = _release(99)

    write_release_descriptor(path, release)

    assert load_release_descriptor(path) == release
    assert path.read_text(encoding="utf-8").endswith("\n")
    assert json.loads(path.read_text(encoding="utf-8"))["release_id"] == release.release_id

    forged = release.to_dict()
    forged["release_id"] = "r000000000100-forged"
    path.write_text(json.dumps(forged), encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="release_id mismatch"):
        load_release_descriptor(path)


def test_refuses_unknown_manifest_fields(tmp_path: Path) -> None:
    path = tmp_path / "release.json"
    payload = _release(1).to_dict()
    payload["untrusted_command"] = "deploy-anything"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ReleaseValidationError, match="unknown release fields"):
        load_release_descriptor(path)


def test_refuses_missing_fields_invalid_json_and_non_object(tmp_path: Path) -> None:
    path = tmp_path / "release.json"
    path.write_text(json.dumps({"code_sha": CODE_A}), encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="missing release fields"):
        load_release_descriptor(path)

    path.write_text("{", encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="invalid release manifest JSON"):
        load_release_descriptor(path)

    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="JSON object"):
        load_release_descriptor(path)


def test_refuses_missing_symlink_directory_and_oversized_manifest(tmp_path: Path) -> None:
    with pytest.raises(ReleaseValidationError, match="unreadable"):
        load_release_descriptor(tmp_path / "missing.json")

    with pytest.raises(ReleaseValidationError, match="small regular file"):
        load_release_descriptor(tmp_path)

    target = tmp_path / "target.json"
    write_release_descriptor(target, _release(1))
    link = tmp_path / "link.json"
    link.symlink_to(target)
    with pytest.raises(ReleaseValidationError, match="small regular file"):
        load_release_descriptor(link)

    target.write_bytes(b" " * (64 * 1024 + 1))
    with pytest.raises(ReleaseValidationError, match="small regular file"):
        load_release_descriptor(target)


def test_atomic_write_removes_temporary_file_on_replace_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_replace(source: str, destination: Path) -> None:
        raise OSError(f"cannot replace {source} with {destination}")

    monkeypatch.setattr(release_guard.os, "replace", fail_replace)
    with pytest.raises(OSError, match="cannot replace"):
        write_release_descriptor(tmp_path / "release.json", _release(1))

    assert list(tmp_path.iterdir()) == []


def test_validate_cli_checks_freshness_and_exact_workflow_inputs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    current_path = tmp_path / "current.json"
    candidate_path = tmp_path / "candidate.json"
    write_release_descriptor(current_path, _release(1))
    candidate = _release(2, code_sha=CODE_B, content_sha=CONTENT_B, artifact_digest=ARTIFACT_B)
    write_release_descriptor(candidate_path, candidate)

    assert (
        main(
            [
                "validate",
                "--candidate",
                str(candidate_path),
                "--current",
                str(current_path),
                "--expected-code-sha",
                CODE_B,
                "--expected-content-sha",
                CONTENT_B,
                "--expected-artifact-digest",
                ARTIFACT_B,
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["release_id"] == candidate.release_id

    with pytest.raises(ReleaseValidationError, match="code_sha does not match"):
        main(
            [
                "validate",
                "--candidate",
                str(candidate_path),
                "--expected-code-sha",
                CODE_A,
            ]
        )
