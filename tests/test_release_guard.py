from __future__ import annotations

import hashlib
import json
import os
import tarfile
import zipfile
from pathlib import Path

import pytest

from scripts import release_guard
from scripts.release_guard import (
    ReleaseDescriptor,
    ReleaseValidationError,
    assert_release_is_fresh,
    assert_release_matches,
    load_release_descriptor,
    main,
    validate_public_tree_manifest_digest,
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
    artifact_digest_kind: str = "public_tree_manifest_v2",
) -> ReleaseDescriptor:
    return ReleaseDescriptor(
        code_sha=code_sha,
        content_sha=content_sha,
        schema_version="1.0",
        release_seq=sequence,
        artifact_digest=artifact_digest,
        artifact_digest_kind=artifact_digest_kind,
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


def test_exact_release_match_accepts_only_the_same_descriptor() -> None:
    candidate = _release(12, code_sha=CODE_B, artifact_digest=ARTIFACT_B)

    assert_release_matches(candidate, candidate)
    with pytest.raises(ReleaseValidationError, match="healthy release mismatch"):
        assert_release_matches(candidate, _release(12, code_sha=CODE_B))


def test_public_tree_manifest_digest_is_recomputed_and_structurally_validated(
    tmp_path: Path,
) -> None:
    manifest = {
        "schema_version": "public_tree_manifest_v1",
        "file_count": 1,
        "total_bytes": 5,
        "files": [
            {
                "path": "index.html",
                "bytes": 5,
                "sha256": hashlib.sha256(b"safe\n").hexdigest(),
            }
        ],
    }
    digest = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    descriptor = _release(
        7,
        artifact_digest=digest,
        artifact_digest_kind="public_tree_manifest_v1",
    )
    path = tmp_path / "public-tree-manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    validate_public_tree_manifest_digest(descriptor, path)

    manifest["total_bytes"] = 6
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ReleaseValidationError, match="public tree manifest totals"):
        validate_public_tree_manifest_digest(descriptor, path)


def test_v2_manifest_binds_html_routes_and_pages_artifact_estimate(
    tmp_path: Path,
) -> None:
    public = tmp_path / "public"
    (public / "posts/one").mkdir(parents=True)
    (public / "assets").mkdir()
    (public / "index.html").write_text("home", encoding="utf-8")
    (public / "404.html").write_text("missing", encoding="utf-8")
    (public / "posts/one/index.html").write_text("post", encoding="utf-8")
    (public / "assets/site.css").write_text("body{}", encoding="utf-8")

    first = release_guard._public_tree_manifest(public)
    second = release_guard._public_tree_manifest(public)
    expected_routes = ["/", "/404.html", "/posts/one/"]

    assert first == second
    assert first["schema_version"] == "public_tree_manifest_v2"
    assert first["route_count"] == 3
    assert first["route_digest"] == hashlib.sha256(
        json.dumps(expected_routes, separators=(",", ":")).encode()
    ).hexdigest()
    assert first["pages_artifact"] == second["pages_artifact"]
    assert first["pages_artifact"]["compression_level"] == 6  # type: ignore[index]
    assert first["pages_artifact"]["status"] == "ok"  # type: ignore[index]
    assert first["pages_artifact"]["directory_count"] == 3  # type: ignore[index]
    assert first["pages_artifact"]["tar_entry_count"] == 8  # type: ignore[index]


@pytest.mark.parametrize("field", ["route_count", "route_digest"])
def test_v2_manifest_rejects_forged_route_inventory(tmp_path: Path, field: str) -> None:
    public = tmp_path / "public"
    public.mkdir()
    (public / "index.html").write_text("safe", encoding="utf-8")
    manifest = release_guard._public_tree_manifest(public)
    manifest[field] = 2 if field == "route_count" else "f" * 64
    path = tmp_path / "tree.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    descriptor = _release(
        1,
        artifact_digest=hashlib.sha256(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    )

    with pytest.raises(ReleaseValidationError, match="HTML route inventory"):
        validate_public_tree_manifest_digest(descriptor, path)


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("status", "ok-if-you-ignore-the-size", "status"),
        ("estimated_bytes", 100 * 1024 * 1024, "100 MiB"),
        ("compression_level", 0, "policy"),
    ],
)
def test_v2_manifest_rejects_forged_pages_artifact_estimate(
    tmp_path: Path,
    field: str,
    value: object,
    reason: str,
) -> None:
    public = tmp_path / "public"
    public.mkdir()
    (public / "index.html").write_text("safe", encoding="utf-8")
    manifest = release_guard._public_tree_manifest(public)
    pages_artifact = manifest["pages_artifact"]
    assert isinstance(pages_artifact, dict)
    pages_artifact[field] = value
    path = tmp_path / "tree.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    descriptor = _release(
        1,
        artifact_digest=hashlib.sha256(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    )

    with pytest.raises(ReleaseValidationError, match=reason):
        validate_public_tree_manifest_digest(descriptor, path)


def test_v1_tree_manifest_and_descriptor_remain_readable(tmp_path: Path) -> None:
    manifest = {
        "schema_version": "public_tree_manifest_v1",
        "file_count": 1,
        "total_bytes": 4,
        "files": [
            {
                "path": "index.html",
                "bytes": 4,
                "sha256": hashlib.sha256(b"safe").hexdigest(),
            }
        ],
    }
    digest = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    descriptor = _release(
        1,
        artifact_digest=digest,
        artifact_digest_kind="public_tree_manifest_v1",
    )
    descriptor_path = tmp_path / "release.json"
    tree_path = tmp_path / "tree.json"
    write_release_descriptor(descriptor_path, descriptor)
    tree_path.write_text(json.dumps(manifest), encoding="utf-8")

    assert load_release_descriptor(descriptor_path) == descriptor
    validate_public_tree_manifest_digest(descriptor, tree_path)


def test_pages_artifact_soft_and_hard_size_boundaries() -> None:
    warning = release_guard._PAGES_ARTIFACT_WARNING_BYTES
    maximum = release_guard._MAX_PAGES_ARTIFACT_BYTES

    assert release_guard._pages_artifact_status(warning - 1) == "ok"
    assert release_guard._pages_artifact_status(warning) == "warning"
    assert release_guard._pages_artifact_status(maximum - 1) == "warning"
    with pytest.raises(ReleaseValidationError, match="100 MiB"):
        release_guard._pages_artifact_status(maximum)


def test_compressible_payload_cannot_bypass_raw_tree_limit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    public = tmp_path / "public"
    public.mkdir()
    (public / "index.html").write_bytes(b"0" * 4_096)
    monkeypatch.setattr(release_guard, "_MAX_PUBLIC_TREE_BYTES", 4_095)

    with pytest.raises(ReleaseValidationError, match="total size limit"):
        release_guard._public_tree_manifest(public)


def test_pages_artifact_hard_failure_cleans_temporary_archives(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    public = tmp_path / "public"
    public.mkdir()
    (public / "index.html").write_bytes(os.urandom(4_096))
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr(release_guard.tempfile, "tempdir", str(scratch))
    monkeypatch.setattr(release_guard, "_MAX_PAGES_ARTIFACT_BYTES", 128)

    with pytest.raises(ReleaseValidationError, match="100 MiB"):
        release_guard._public_tree_manifest(public)

    assert list(scratch.iterdir()) == []


def test_tar_and_single_member_level_6_zip_are_byte_deterministic(
    tmp_path: Path,
) -> None:
    public = tmp_path / "public"
    (public / "posts/one").mkdir(parents=True)
    (public / "index.html").write_text("home", encoding="utf-8")
    (public / "posts/one/index.html").write_text("post", encoding="utf-8")
    manifest = release_guard._public_tree_manifest(public)
    files = manifest["files"]
    assert isinstance(files, list)
    directories = ["posts", "posts/one"]
    first_tar = tmp_path / "first.tar"
    second_tar = tmp_path / "second.tar"
    first_zip = tmp_path / "first.zip"
    second_zip = tmp_path / "second.zip"

    release_guard._write_deterministic_tar(public, files, directories, first_tar)
    release_guard._write_deterministic_tar(public, files, directories, second_tar)
    release_guard._write_deterministic_zip(first_tar, first_zip)
    release_guard._write_deterministic_zip(second_tar, second_zip)

    assert first_tar.read_bytes() == second_tar.read_bytes()
    assert first_zip.read_bytes() == second_zip.read_bytes()
    with zipfile.ZipFile(first_zip) as archive:
        assert archive.namelist() == ["artifact.tar"]
        entry = archive.getinfo("artifact.tar")
        assert entry.compress_type == zipfile.ZIP_DEFLATED
        assert entry.date_time == (1980, 1, 1, 0, 0, 0)
        assert archive.read("artifact.tar") == first_tar.read_bytes()
        assert archive.testzip() is None
    with tarfile.open(first_tar) as archive:
        members = archive.getmembers()
        assert [member.name for member in members] == [
            ".",
            "index.html",
            "posts",
            "posts/one",
            "posts/one/index.html",
        ]
        assert all(
            member.mode == (0o755 if member.isdir() else 0o644) for member in members
        )
        assert all(member.uid == member.gid == member.mtime == 0 for member in members)


def test_pages_artifact_rejects_file_changed_after_tree_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    public = tmp_path / "public"
    public.mkdir()
    page = public / "index.html"
    page.write_bytes(b"before")
    original = release_guard._estimate_pages_artifact

    def mutate_before_estimate(
        root: Path,
        files: list[dict[str, object]],
        directories: list[str],
    ) -> int:
        page.write_bytes(b"after!")
        return original(root, files, directories)

    monkeypatch.setattr(release_guard, "_estimate_pages_artifact", mutate_before_estimate)

    with pytest.raises(ReleaseValidationError, match="changed after tree hash"):
        release_guard._public_tree_manifest(public)


def test_public_file_fuse_is_30k_and_boundary_is_enforced(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert release_guard._MAX_PUBLIC_FILES == 30_000
    public = tmp_path / "public"
    public.mkdir()
    (public / "index.html").write_text("safe", encoding="utf-8")
    (public / "asset.css").write_text("safe", encoding="utf-8")
    monkeypatch.setattr(release_guard, "_MAX_PUBLIC_FILES", 2)
    release_guard._public_tree_manifest(public)
    monkeypatch.setattr(release_guard, "_MAX_PUBLIC_FILES", 1)

    with pytest.raises(ReleaseValidationError, match="too many files"):
        release_guard._public_tree_manifest(public)


def test_empty_directory_flood_is_bounded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    public = tmp_path / "public"
    public.mkdir()
    (public / "index.html").write_text("safe", encoding="utf-8")
    (public / "empty").mkdir()
    monkeypatch.setattr(release_guard, "_MAX_PUBLIC_DIRECTORIES", 0)

    with pytest.raises(ReleaseValidationError, match="too many directories"):
        release_guard._public_tree_manifest(public)


def test_verify_cli_binds_candidate_to_healthy_state_and_public_tree(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tree = {
        "schema_version": "public_tree_manifest_v1",
        "file_count": 1,
        "total_bytes": 4,
        "files": [
            {
                "path": "index.html",
                "bytes": 4,
                "sha256": hashlib.sha256(b"safe").hexdigest(),
            }
        ],
    }
    digest = hashlib.sha256(
        json.dumps(tree, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    candidate = _release(
        8,
        code_sha=CODE_B,
        content_sha=CONTENT_B,
        artifact_digest=digest,
        artifact_digest_kind="public_tree_manifest_v1",
    )
    candidate_path = tmp_path / "candidate.json"
    current_path = tmp_path / "current.json"
    tree_path = tmp_path / "tree.json"
    write_release_descriptor(candidate_path, candidate)
    write_release_descriptor(current_path, candidate)
    tree_path.write_text(json.dumps(tree), encoding="utf-8")

    assert (
        main(
            [
                "verify",
                "--candidate",
                str(candidate_path),
                "--current",
                str(current_path),
                "--tree-manifest",
                str(tree_path),
                "--expected-release-id",
                candidate.release_id,
                "--expected-code-sha",
                CODE_B,
                "--expected-content-sha",
                CONTENT_B,
                "--expected-artifact-digest",
                digest,
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["release_id"] == candidate.release_id

    write_release_descriptor(tmp_path / "different.json", _release(9))
    with pytest.raises(ReleaseValidationError, match="healthy release mismatch"):
        main(
            [
                "verify",
                "--candidate",
                str(candidate_path),
                "--current",
                str(tmp_path / "different.json"),
                "--tree-manifest",
                str(tree_path),
            ]
        )


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

    hardlink = tmp_path / "hardlink.json"
    hardlink.hardlink_to(target)
    with pytest.raises(ReleaseValidationError, match="small regular file"):
        load_release_descriptor(hardlink)
    hardlink.unlink()

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
    assert descriptor.artifact_digest_kind == "public_tree_manifest_v2"
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
