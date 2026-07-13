from __future__ import annotations

import hashlib
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


def test_release_id_binds_sequence_code_content_and_schema_without_artifact_cycle() -> None:
    release = _release(42)
    identity = json.dumps(
        {
            "code_sha": CODE_A,
            "content_sha": CONTENT_A,
            "release_seq": 42,
            "schema_version": "1.0",
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()

    assert release.release_id == f"r-{hashlib.sha256(identity).hexdigest()[:24]}"
    assert release.to_dict()["release_id"] == release.release_id
    assert _release(42, artifact_digest=ARTIFACT_B).release_id == release.release_id
    assert _release(42, content_sha=CONTENT_B).release_id != release.release_id


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
        ({"artifact_digest_kind": "transport_tar_sha256"}, "artifact_digest_kind"),
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


def test_create_cli_hashes_the_final_public_tree_and_keeps_transport_digest_separate(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    public = tmp_path / "public"
    (public / "api/v1").mkdir(parents=True)
    (public / "index.html").write_text("<h1>AI Stack</h1>\n", encoding="utf-8")
    (public / "api/v1/manifest.json").write_text(
        json.dumps(
            {
                "active_release": _release(7).release_id,
                "build": {
                    "release_id": _release(7).release_id,
                    "code_sha": CODE_A,
                    "content_sha": CONTENT_A,
                },
            }
        ),
        encoding="utf-8",
    )
    basis = tmp_path / "handoff/state/release-basis.json"
    basis.parent.mkdir(parents=True)
    basis.write_text(
        json.dumps(
            {
                "basis_schema_version": "release_basis_v1",
                "release_id": _release(7).release_id,
                "code_sha": CODE_A,
                "content_sha": CONTENT_A,
                "schema_version": "1.0",
                "release_seq": 7,
                "generated_at": "2026-07-13T08:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    output = basis.parent / "release.json"

    assert (
        main(
            [
                "create",
                "--public-root",
                str(public),
                "--basis",
                str(basis),
                "--output",
                str(output),
            ]
        )
        == 0
    )

    result = json.loads(capsys.readouterr().out)
    descriptor = load_release_descriptor(output)
    tree_manifest = json.loads(
        (basis.parent / "public-tree-manifest.json").read_text(encoding="utf-8")
    )
    manifest_bytes = json.dumps(
        tree_manifest,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    assert result["artifact_digest"] == descriptor.artifact_digest
    assert descriptor.artifact_digest == hashlib.sha256(manifest_bytes).hexdigest()
    assert descriptor.artifact_digest_kind == "public_tree_manifest_v1"
    assert "transport_archive_digest" not in descriptor.to_dict()
    assert {item["path"] for item in tree_manifest["files"]} == {
        "api/v1/manifest.json",
        "index.html",
    }


def test_create_cli_rejects_public_symlinks_and_release_identity_mismatch(
    tmp_path: Path,
) -> None:
    public = tmp_path / "public"
    public.mkdir()
    outside = tmp_path / "outside.html"
    outside.write_text("outside", encoding="utf-8")
    (public / "linked.html").symlink_to(outside)
    basis = tmp_path / "release-basis.json"
    basis.write_text(
        json.dumps(
            {
                "basis_schema_version": "release_basis_v1",
                "release_id": _release(8).release_id,
                "code_sha": CODE_A,
                "content_sha": CONTENT_A,
                "schema_version": "1.0",
                "release_seq": 8,
                "generated_at": "2026-07-13T08:00:00Z",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ReleaseValidationError, match="symlink"):
        main(
            [
                "create",
                "--public-root",
                str(public),
                "--basis",
                str(basis),
                "--output",
                str(tmp_path / "release.json"),
            ]
        )


def _basis_payload(sequence: int = 1) -> dict[str, object]:
    release = _release(sequence)
    return {
        "basis_schema_version": "release_basis_v1",
        "release_id": release.release_id,
        "code_sha": release.code_sha,
        "content_sha": release.content_sha,
        "schema_version": release.schema_version,
        "release_seq": sequence,
        "generated_at": release.generated_at,
    }


def test_release_basis_loader_rejects_missing_symlink_json_shape_and_forgery(
    tmp_path: Path,
) -> None:
    with pytest.raises(ReleaseValidationError, match="unreadable"):
        release_guard.load_release_basis(tmp_path / "missing.json")

    target = tmp_path / "target.json"
    target.write_text(json.dumps(_basis_payload()), encoding="utf-8")
    linked = tmp_path / "linked.json"
    linked.symlink_to(target)
    with pytest.raises(ReleaseValidationError, match="small regular"):
        release_guard.load_release_basis(linked)

    target.write_text("{", encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="invalid release basis"):
        release_guard.load_release_basis(target)
    target.write_text("[]", encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="JSON object"):
        release_guard.load_release_basis(target)
    target.write_text(json.dumps({"basis_schema_version": "future"}), encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="fields or schema"):
        release_guard.load_release_basis(target)
    forged = _basis_payload()
    forged["release_id"] = "r-forged"
    target.write_text(json.dumps(forged), encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="release_id mismatch"):
        release_guard.load_release_basis(target)


def test_public_tree_rejects_empty_executable_hardlink_and_size_limits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(ReleaseValidationError, match="regular directory"):
        release_guard._public_tree_manifest(tmp_path / "missing")
    public = tmp_path / "public"
    public.mkdir()
    with pytest.raises(ReleaseValidationError, match="must not be empty"):
        release_guard._public_tree_manifest(public)

    executable = public / "run.js"
    executable.write_text("safe", encoding="utf-8")
    executable.chmod(0o755)
    with pytest.raises(ReleaseValidationError, match="executable"):
        release_guard._public_tree_manifest(public)
    executable.chmod(0o644)

    hardlink = public / "hardlink.js"
    hardlink.hardlink_to(executable)
    with pytest.raises(ReleaseValidationError, match="non-regular"):
        release_guard._public_tree_manifest(public)
    hardlink.unlink()

    monkeypatch.setattr(release_guard, "_MAX_PUBLIC_FILE_BYTES", 1)
    with pytest.raises(ReleaseValidationError, match="size limit"):
        release_guard._public_tree_manifest(public)
    monkeypatch.setattr(release_guard, "_MAX_PUBLIC_FILE_BYTES", 16 * 1024 * 1024)
    monkeypatch.setattr(release_guard, "_MAX_PUBLIC_FILES", 0)
    with pytest.raises(ReleaseValidationError, match="too many"):
        release_guard._public_tree_manifest(public)


def test_create_rejects_public_identity_mismatch_and_existing_outputs(
    tmp_path: Path,
) -> None:
    public = tmp_path / "public"
    (public / "api/v1").mkdir(parents=True)
    (public / "index.html").write_text("safe", encoding="utf-8")
    basis = tmp_path / "state/release-basis.json"
    basis.parent.mkdir()
    basis.write_text(json.dumps(_basis_payload(3)), encoding="utf-8")
    manifest = public / "api/v1/manifest.json"
    manifest.write_text("{}", encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="release identity mismatch"):
        release_guard.create_release_descriptor(
            public_root=public,
            basis_path=basis,
            output_path=basis.parent / "release.json",
        )

    payload = _basis_payload(3)
    manifest.write_text(
        json.dumps(
            {
                "active_release": payload["release_id"],
                "build": {
                    "release_id": payload["release_id"],
                    "code_sha": CODE_A,
                    "content_sha": "d" * 40,
                },
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ReleaseValidationError, match="build identity mismatch"):
        release_guard.create_release_descriptor(
            public_root=public,
            basis_path=basis,
            output_path=basis.parent / "release.json",
        )

    output = basis.parent / "release.json"
    output.write_text("existing", encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="must not already exist"):
        release_guard.create_release_descriptor(
            public_root=public, basis_path=basis, output_path=output
        )
