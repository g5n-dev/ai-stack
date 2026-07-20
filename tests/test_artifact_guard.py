from __future__ import annotations

import json
import tarfile
from hashlib import sha256
from io import BytesIO
from pathlib import Path

import pytest

import scripts.artifact_guard as guard
from scripts.artifact_guard import (
    ArtifactPolicy,
    ArtifactValidationError,
    main,
    package_tar_artifact,
    validate_packaged_artifact,
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


def _pack_cli(profile: str, root: Path, archive: Path, manifest: Path) -> list[str]:
    return [
        "pack",
        "--profile",
        profile,
        "--root",
        str(root),
        "--archive",
        str(archive),
        "--manifest",
        str(manifest),
    ]


def _validate_cli(
    profile: str,
    archive: Path,
    manifest: Path,
    destination: Path | None = None,
) -> list[str]:
    result = [
        "validate",
        "--profile",
        profile,
        "--archive",
        str(archive),
        "--manifest",
        str(manifest),
    ]
    if destination is not None:
        result.extend(("--extract-to", str(destination)))
    return result


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
        (
            json.dumps(
                {
                    "schema_version": "1",
                    "event_id": "evt",
                    "token": "ghp_abcdefghijklmnopqrstuvwxyz1234567890",
                }
            ).encode(),
            "secret-like content",
        ),
        (
            json.dumps(
                {
                    "schema_version": "1",
                    "event_id": "evt",
                    "url": "https://source.invalid/item?token=private-query-value-123",
                }
            ).encode(),
            "secret-like content",
        ),
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


def test_accepts_non_sensitive_public_url_query_names(tmp_path: Path) -> None:
    artifact = tmp_path / "public-query.tar"
    payload = json.dumps(
        {
            "schema_version": "1",
            "event_id": "evt",
            "url": "https://source.invalid/item?id=42&post=one&v=3&langVersion=en",
        }
    ).encode()
    expected = _write_tar(
        artifact,
        [("content/events/evt.json", payload, 0o644, "file")],
    )

    assert validate_tar_artifact(
        artifact,
        policy=_policy(),
        expected_files=expected,
    ).file_count == 1


def test_accepts_public_model_name_assignment(tmp_path: Path) -> None:
    artifact = tmp_path / "public-model.tar"
    payload = b"ANTHROPIC_MODEL=claude-sonnet-public-model\n"
    expected = _write_tar(
        artifact,
        [("content/post.md", payload, 0o644, "file")],
    )

    assert validate_tar_artifact(
        artifact,
        policy=_policy(),
        expected_files=expected,
    ).file_count == 1


@pytest.mark.parametrize(
    "payload",
    [
        b'key: "sk-ant-api03-super-secret-material"',
        b'key: "sk-proj-super-secret-material"',
        b'Authorization: Bearer opaque-private-token-value',
        b'jwt=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwcml2YXRlIn0.c2lnbmF0dXJl',
        b'https://private-user:private-password@example.test/resource',
        b'ANTHROPIC_AUTH_TOKEN=provider-private-value',
        b'OPENAI_API_KEY: provider-private-value',
        b'SEARXNG_BASE_URL=https://private-search.internal',
        b'https://example.test/item?X-Amz-Credential=private-value',
    ],
)
def test_rejects_provider_credentials_authenticated_urls_and_sensitive_queries(
    tmp_path: Path,
    payload: bytes,
) -> None:
    artifact = tmp_path / "handoff.tar"
    expected = _write_tar(
        artifact,
        [("content/post.md", payload, 0o644, "file")],
    )

    with pytest.raises(ArtifactValidationError, match="secret-like content"):
        validate_tar_artifact(artifact, policy=_policy(), expected_files=expected)


def test_allows_qualified_javascript_api_identifiers(tmp_path: Path) -> None:
    artifact = tmp_path / "javascript-api.tar"
    expected = _write_tar(
        artifact,
        [
            (
                "content/post.md",
                b"navigator.modelContext.registerTool()\n",
                0o644,
                "file",
            )
        ],
    )

    report = validate_tar_artifact(
        artifact,
        policy=_policy(),
        expected_files=expected,
    )

    assert report.file_count == 1


def test_pack_rejects_exact_job_secret_without_disclosing_value_or_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    secret = "unknown-format-private-material-984731"
    root = tmp_path / "handoff"
    (root / "content").mkdir(parents=True)
    (root / "content" / "post.md").write_text(
        f"ordinary prose accidentally contains {secret}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", secret)
    archive = tmp_path / "handoff.tar"
    manifest = tmp_path / "handoff.json"

    assert main(
        _pack_cli("generated", root, archive, manifest)
        + ["--reject-env", "ANTHROPIC_AUTH_TOKEN"]
    ) == 2

    output = capsys.readouterr()
    combined = output.out + output.err
    assert secret not in combined
    assert sha256(secret.encode()).hexdigest() not in combined
    assert not archive.exists()


def test_pack_ignores_unset_and_short_exact_secret_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "handoff"
    (root / "content").mkdir(parents=True)
    (root / "content" / "post.md").write_text("short xyz value\n", encoding="utf-8")
    monkeypatch.delenv("UNSET_EXACT_SECRET", raising=False)
    monkeypatch.setenv("SHORT_EXACT_SECRET", "xyz")

    assert main(
        _pack_cli("generated", root, tmp_path / "a.tar", tmp_path / "a.json")
        + [
            "--reject-env",
            "UNSET_EXACT_SECRET",
            "--reject-env",
            "SHORT_EXACT_SECRET",
        ]
    ) == 0


def test_cli_packages_validates_and_safely_extracts_handoff(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "handoff"
    (root / "content" / "events").mkdir(parents=True)
    (root / "state").mkdir()
    (root / "content" / "events" / "evt.json").write_bytes(_valid_event())
    (root / "state" / "run.json").write_text(
        json.dumps({"schema_version": "1", "run_id": "run-1"}),
        encoding="utf-8",
    )
    archive = tmp_path / "transfer" / "handoff.tar"
    manifest = tmp_path / "transfer" / "handoff.manifest.json"

    assert (
        main(
            [
                "pack",
                "--profile",
                "discovery",
                "--root",
                str(root),
                "--archive",
                str(archive),
                "--manifest",
                str(manifest),
            ]
        )
        == 0
    )
    packed = json.loads(manifest.read_text(encoding="utf-8"))
    assert packed["schema_version"] == "artifact_manifest_v1"
    assert packed["profile"] == "discovery"
    assert packed["file_count"] == 2
    assert list(packed["files"]) == ["content/events/evt.json", "state/run.json"]

    destination = tmp_path / "validated"
    assert (
        main(
            [
                "validate",
                "--profile",
                "discovery",
                "--archive",
                str(archive),
                "--manifest",
                str(manifest),
                "--extract-to",
                str(destination),
            ]
        )
        == 0
    )
    assert (destination / "content" / "events" / "evt.json").read_bytes() == _valid_event()
    reports = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert reports[-1]["file_count"] == 2


def test_packaged_artifact_rejects_manifest_tampering_and_wrong_profile(
    tmp_path: Path,
) -> None:
    root = tmp_path / "handoff"
    (root / "content").mkdir(parents=True)
    (root / "content" / "event.json").write_bytes(_valid_event())
    archive = tmp_path / "handoff.tar"
    manifest = tmp_path / "handoff.manifest.json"
    assert main(_pack_cli("generated", root, archive, manifest)) == 0

    assert main(_validate_cli("receipt", archive, manifest)) == 2

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["command"] = "trust-me"
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    assert main(_validate_cli("generated", archive, manifest)) == 2


def test_pack_rejects_symlink_and_extract_refuses_existing_destination(tmp_path: Path) -> None:
    root = tmp_path / "handoff"
    (root / "content").mkdir(parents=True)
    (root / "content" / "link.json").symlink_to("../../outside.json")
    archive = tmp_path / "handoff.tar"
    manifest = tmp_path / "handoff.manifest.json"

    assert main(_pack_cli("discovery", root, archive, manifest)) == 2

    (root / "content" / "link.json").unlink()
    (root / "content" / "event.json").write_bytes(_valid_event())
    assert main(_pack_cli("discovery", root, archive, manifest)) == 0
    destination = tmp_path / "existing"
    destination.mkdir()
    assert main(_validate_cli("discovery", archive, manifest, destination)) == 2


def _packaged_fixture(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "handoff"
    (root / "content").mkdir(parents=True)
    (root / "content" / "event.json").write_bytes(_valid_event())
    archive = tmp_path / "handoff.tar"
    manifest = tmp_path / "handoff.manifest.json"
    package_tar_artifact(
        root,
        archive_path=archive,
        manifest_path=manifest,
        profile="generated",
    )
    return root, archive, manifest


@pytest.mark.parametrize(
    "mutation",
    [
        "invalid_json",
        "archive_digest",
        "files_not_object",
        "record_not_object",
        "record_fields",
        "record_size",
        "totals",
    ],
)
def test_rejects_each_invalid_manifest_shape(tmp_path: Path, mutation: str) -> None:
    _, archive, manifest = _packaged_fixture(tmp_path)
    if mutation == "invalid_json":
        manifest.write_text("{", encoding="utf-8")
    else:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        name = next(iter(payload["files"]))
        if mutation == "archive_digest":
            payload["archive_sha256"] = False
        elif mutation == "files_not_object":
            payload["files"] = []
        elif mutation == "record_not_object":
            payload["files"][name] = "trust-me"
        elif mutation == "record_fields":
            payload["files"][name]["mode"] = 0o644
        elif mutation == "record_size":
            payload["files"][name]["bytes"] = True
        else:
            payload["total_bytes"] += 1
        manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ArtifactValidationError):
        validate_packaged_artifact(
            archive_path=archive,
            manifest_path=manifest,
            profile="generated",
        )


def test_rejects_missing_symlinked_and_oversized_manifest_or_archive(tmp_path: Path) -> None:
    _, archive, manifest = _packaged_fixture(tmp_path)
    missing = tmp_path / "missing.tar"
    with pytest.raises(ArtifactValidationError, match="archive must be"):
        validate_packaged_artifact(
            archive_path=missing,
            manifest_path=manifest,
            profile="generated",
        )

    real_manifest = manifest.with_name("real-manifest.json")
    manifest.rename(real_manifest)
    manifest.symlink_to(real_manifest)
    with pytest.raises(ArtifactValidationError, match="manifest must be"):
        validate_packaged_artifact(
            archive_path=archive,
            manifest_path=manifest,
            profile="generated",
        )

    manifest.unlink()
    manifest.write_bytes(b"x" * (1024 * 1024 + 1))
    with pytest.raises(ArtifactValidationError, match="manifest must be"):
        validate_packaged_artifact(
            archive_path=archive,
            manifest_path=manifest,
            profile="generated",
        )


def test_packaging_rejects_invalid_roots_outputs_and_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    invalid_root = tmp_path / "not-a-directory"
    invalid_root.write_text("file", encoding="utf-8")
    with pytest.raises(ArtifactValidationError, match="regular directory"):
        package_tar_artifact(
            invalid_root,
            archive_path=tmp_path / "a.tar",
            manifest_path=tmp_path / "a.json",
            profile="generated",
        )

    root = tmp_path / "root"
    (root / "content").mkdir(parents=True)
    (root / "content" / "event.json").write_bytes(_valid_event())
    with pytest.raises(ArtifactValidationError, match="outside artifact root"):
        package_tar_artifact(
            root,
            archive_path=root / "a.tar",
            manifest_path=tmp_path / "a.json",
            profile="generated",
        )

    tiny = ArtifactPolicy(
        allowed_roots=("content",),
        allowed_suffixes=(".json",),
        max_files=1,
        max_file_bytes=8,
        max_total_bytes=8,
    )
    monkeypatch.setitem(guard._PROFILES, "tiny", tiny)
    with pytest.raises(ArtifactValidationError, match="file too large"):
        package_tar_artifact(
            root,
            archive_path=tmp_path / "tiny.tar",
            manifest_path=tmp_path / "tiny.json",
            profile="tiny",
        )

    executable = root / "content" / "event.json"
    executable.write_text("{}", encoding="utf-8")
    executable.chmod(0o755)
    with pytest.raises(ArtifactValidationError, match="executable"):
        package_tar_artifact(
            root,
            archive_path=tmp_path / "exec.tar",
            manifest_path=tmp_path / "exec.json",
            profile="tiny",
        )


def test_packaging_rejects_disallowed_suffix_hardlink_and_file_count(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "root"
    (root / "content").mkdir(parents=True)
    (root / "content" / "unsafe.bin").write_bytes(b"safe")
    with pytest.raises(ArtifactValidationError, match="disallowed suffix"):
        package_tar_artifact(
            root,
            archive_path=tmp_path / "suffix.tar",
            manifest_path=tmp_path / "suffix.json",
            profile="generated",
        )

    (root / "content" / "unsafe.bin").unlink()
    first = root / "content" / "a.json"
    second = root / "content" / "b.json"
    first.write_text("{}", encoding="utf-8")
    second.hardlink_to(first)
    with pytest.raises(ArtifactValidationError, match="non-regular file"):
        package_tar_artifact(
            root,
            archive_path=tmp_path / "links.tar",
            manifest_path=tmp_path / "links.json",
            profile="generated",
        )

    second.unlink()
    first.unlink()
    (root / "content" / "a.json").write_text("{}", encoding="utf-8")
    (root / "content" / "b.json").write_text("{}", encoding="utf-8")
    one_file = ArtifactPolicy(
        allowed_roots=("content",),
        allowed_suffixes=(".json",),
        max_files=1,
        max_file_bytes=100,
        max_total_bytes=100,
    )
    monkeypatch.setitem(guard._PROFILES, "one-file", one_file)
    with pytest.raises(ArtifactValidationError, match="too many files"):
        package_tar_artifact(
            root,
            archive_path=tmp_path / "count.tar",
            manifest_path=tmp_path / "count.json",
            profile="one-file",
        )


def test_rejects_invalid_webp_subtype_and_unknown_profile(tmp_path: Path) -> None:
    assert guard._profile_policy("release").max_file_bytes == 8 * 1024 * 1024

    artifact = tmp_path / "image.tar"
    payload = b"RIFF\x04\x00\x00\x00NOPE"
    expected = _write_tar(
        artifact,
        [("content/media/image.webp", payload, 0o644, "file")],
    )
    with pytest.raises(ArtifactValidationError, match="invalid image MIME"):
        validate_tar_artifact(
            artifact,
            policy=_policy(allowed_suffixes=(".json", ".md", ".webp")),
            expected_files=expected,
        )
    with pytest.raises(ArtifactValidationError, match="unknown artifact profile"):
        package_tar_artifact(
            tmp_path,
            archive_path=tmp_path / "unknown.tar",
            manifest_path=tmp_path / "unknown.json",
            profile="unknown",
        )


def test_refresh_and_validated_profiles_enforce_exact_delivery_path_allowlist(
    tmp_path: Path,
) -> None:
    root = tmp_path / "handoff"
    (root / "blog/content/posts").mkdir(parents=True)
    (root / "data/lineage/registry").mkdir(parents=True)
    (root / "blog/content/posts/one.md").write_text("safe\n", encoding="utf-8")
    (root / "data/lineage/registry/00.json").write_text("{}\n", encoding="utf-8")

    report = package_tar_artifact(
        root,
        archive_path=tmp_path / "refresh.tar",
        manifest_path=tmp_path / "refresh.json",
        profile="refresh",
    )
    assert report.file_count == 2

    (root / "blog/static/data/untrusted").mkdir(parents=True)
    (root / "blog/static/data/untrusted/payload.json").write_text("{}\n")
    with pytest.raises(ArtifactValidationError, match="allowlist"):
        package_tar_artifact(
            root,
            archive_path=tmp_path / "forged.tar",
            manifest_path=tmp_path / "forged.json",
            profile="validated",
        )


def test_extraction_rejects_digest_and_removes_partial_destination(tmp_path: Path) -> None:
    artifact = tmp_path / "handoff.tar"
    payload = _valid_event()
    _write_tar(
        artifact,
        [
            ("content/events", b"", 0o755, "directory"),
            ("content/events/evt.json", payload, 0o644, "file"),
        ],
    )
    destination = tmp_path / "extracted"
    with pytest.raises(ArtifactValidationError, match="extraction digest mismatch"):
        guard._extract_validated(
            artifact,
            destination,
            {"content/events/evt.json": "0" * 64},
            _policy(),
        )
    assert not destination.exists()


def test_extraction_rejects_symlinked_parent_and_archive_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, archive, manifest = _packaged_fixture(tmp_path)
    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    linked_parent = tmp_path / "linked-parent"
    linked_parent.symlink_to(real_parent, target_is_directory=True)
    with pytest.raises(ArtifactValidationError, match="symlink extraction path"):
        validate_packaged_artifact(
            archive_path=archive,
            manifest_path=manifest,
            profile="generated",
            extract_to=linked_parent / "output",
        )

    real_hash = guard._hash_file
    calls = 0

    def changed_hash(path: Path) -> str:
        nonlocal calls
        calls += 1
        return real_hash(path) if calls == 1 else "0" * 64

    monkeypatch.setattr(guard, "_hash_file", changed_hash)
    destination = tmp_path / "changed"
    with pytest.raises(ArtifactValidationError, match="changed during extraction"):
        validate_packaged_artifact(
            archive_path=archive,
            manifest_path=manifest,
            profile="generated",
            extract_to=destination,
        )
    assert not destination.exists()
