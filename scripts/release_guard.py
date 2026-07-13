"""Immutable release identity and stale-deployment protection."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


class ReleaseValidationError(ValueError):
    """Raised when a release manifest cannot be trusted."""


_GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SCHEMA_VERSION = re.compile(r"[1-9][0-9]*\.[0-9]+\Z")
_ARTIFACT_DIGEST_KIND = "public_tree_manifest_v1"
_BASIS_SCHEMA_VERSION = "release_basis_v1"
_TREE_SCHEMA_VERSION = "public_tree_manifest_v1"
_MAX_PUBLIC_FILES = 20_000
_MAX_PUBLIC_FILE_BYTES = 16 * 1024 * 1024
_MAX_PUBLIC_TREE_BYTES = 256 * 1024 * 1024
_FIELDS = frozenset(
    {
        "release_id",
        "code_sha",
        "content_sha",
        "schema_version",
        "release_seq",
        "artifact_digest",
        "artifact_digest_kind",
        "generated_at",
    }
)
_REQUIRED_FIELDS = _FIELDS.difference({"release_id"})


@dataclass(frozen=True)
class ReleaseDescriptor:
    code_sha: str
    content_sha: str
    schema_version: str
    release_seq: int
    artifact_digest: str
    generated_at: str
    artifact_digest_kind: str = _ARTIFACT_DIGEST_KIND

    def __post_init__(self) -> None:
        if not isinstance(self.code_sha, str) or not _GIT_SHA.fullmatch(self.code_sha):
            raise ReleaseValidationError("invalid code_sha")
        if not isinstance(self.content_sha, str) or not _GIT_SHA.fullmatch(self.content_sha):
            raise ReleaseValidationError("invalid content_sha")
        if not isinstance(self.artifact_digest, str) or not _SHA256.fullmatch(self.artifact_digest):
            raise ReleaseValidationError("invalid artifact_digest")
        if self.artifact_digest_kind != _ARTIFACT_DIGEST_KIND:
            raise ReleaseValidationError("invalid artifact_digest_kind")
        if not isinstance(self.schema_version, str) or not _SCHEMA_VERSION.fullmatch(
            self.schema_version
        ):
            raise ReleaseValidationError("invalid schema_version")
        if (
            not isinstance(self.release_seq, int)
            or isinstance(self.release_seq, bool)
            or self.release_seq <= 0
        ):
            raise ReleaseValidationError("invalid release_seq")
        if not isinstance(self.generated_at, str):
            raise ReleaseValidationError("invalid generated_at")
        try:
            datetime.strptime(self.generated_at, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as exc:
            raise ReleaseValidationError("invalid generated_at") from exc

    @property
    def release_id(self) -> str:
        # Artifact bytes are deliberately excluded.  Public files embed this
        # release id, so including the public-tree digest would create a
        # self-referential hash.  The independent artifact_digest still binds
        # the external release descriptor to the completed public tree.
        identity = json.dumps(
            {
                "code_sha": self.code_sha,
                "content_sha": self.content_sha,
                "release_seq": self.release_seq,
                "schema_version": self.schema_version,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        return "r-" + hashlib.sha256(identity).hexdigest()[:24]

    def to_dict(self) -> dict[str, str | int]:
        return {
            "release_id": self.release_id,
            "code_sha": self.code_sha,
            "content_sha": self.content_sha,
            "schema_version": self.schema_version,
            "release_seq": self.release_seq,
            "artifact_digest": self.artifact_digest,
            "artifact_digest_kind": self.artifact_digest_kind,
            "generated_at": self.generated_at,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> ReleaseDescriptor:
        unknown = set(value).difference(_FIELDS)
        if unknown:
            raise ReleaseValidationError(f"unknown release fields: {sorted(unknown)}")
        missing = _REQUIRED_FIELDS.difference(value)
        if missing:
            raise ReleaseValidationError(f"missing release fields: {sorted(missing)}")
        descriptor = cls(
            code_sha=value["code_sha"],  # type: ignore[arg-type]
            content_sha=value["content_sha"],  # type: ignore[arg-type]
            schema_version=value["schema_version"],  # type: ignore[arg-type]
            release_seq=value["release_seq"],  # type: ignore[arg-type]
            artifact_digest=value["artifact_digest"],  # type: ignore[arg-type]
            generated_at=value["generated_at"],  # type: ignore[arg-type]
            artifact_digest_kind=value["artifact_digest_kind"],  # type: ignore[arg-type]
        )
        claimed_release_id = value.get("release_id")
        if claimed_release_id is not None and claimed_release_id != descriptor.release_id:
            raise ReleaseValidationError("release_id mismatch")
        return descriptor


@dataclass(frozen=True)
class ReleaseBasis:
    code_sha: str
    content_sha: str
    schema_version: str
    release_seq: int
    generated_at: str

    def __post_init__(self) -> None:
        # Reuse the descriptor's strict identity validators without allowing a
        # transport or tree digest to participate in the release id.
        ReleaseDescriptor(
            code_sha=self.code_sha,
            content_sha=self.content_sha,
            schema_version=self.schema_version,
            release_seq=self.release_seq,
            artifact_digest="0" * 64,
            generated_at=self.generated_at,
        )

    @property
    def release_id(self) -> str:
        return ReleaseDescriptor(
            code_sha=self.code_sha,
            content_sha=self.content_sha,
            schema_version=self.schema_version,
            release_seq=self.release_seq,
            artifact_digest="0" * 64,
            generated_at=self.generated_at,
        ).release_id

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> ReleaseBasis:
        fields = {
            "basis_schema_version",
            "release_id",
            "code_sha",
            "content_sha",
            "schema_version",
            "release_seq",
            "generated_at",
        }
        if set(value) != fields or value.get("basis_schema_version") != _BASIS_SCHEMA_VERSION:
            raise ReleaseValidationError("release basis fields or schema are invalid")
        basis = cls(
            code_sha=value["code_sha"],  # type: ignore[arg-type]
            content_sha=value["content_sha"],  # type: ignore[arg-type]
            schema_version=value["schema_version"],  # type: ignore[arg-type]
            release_seq=value["release_seq"],  # type: ignore[arg-type]
            generated_at=value["generated_at"],  # type: ignore[arg-type]
        )
        if value["release_id"] != basis.release_id:
            raise ReleaseValidationError("release basis release_id mismatch")
        return basis


def assert_release_is_fresh(
    candidate: ReleaseDescriptor,
    current: ReleaseDescriptor | None,
) -> None:
    if current is not None and candidate.release_seq <= current.release_seq:
        raise ReleaseValidationError(
            f"stale release sequence: candidate={candidate.release_seq}, "
            f"current={current.release_seq}"
        )


def load_release_descriptor(path: Path | str) -> ReleaseDescriptor:
    manifest = Path(path)
    try:
        stat = manifest.lstat()
    except OSError as exc:
        raise ReleaseValidationError("release manifest is unreadable") from exc
    if manifest.is_symlink() or not manifest.is_file() or stat.st_size > 64 * 1024:
        raise ReleaseValidationError("release manifest must be a small regular file")
    try:
        raw = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseValidationError("invalid release manifest JSON") from exc
    if not isinstance(raw, dict):
        raise ReleaseValidationError("release manifest must be a JSON object")
    return ReleaseDescriptor.from_mapping(raw)


def load_release_basis(path: Path | str) -> ReleaseBasis:
    basis_path = Path(path)
    try:
        details = basis_path.lstat()
    except OSError as exc:
        raise ReleaseValidationError("release basis is unreadable") from exc
    if (
        basis_path.is_symlink()
        or not stat.S_ISREG(details.st_mode)
        or details.st_nlink != 1
        or details.st_size > 64 * 1024
    ):
        raise ReleaseValidationError("release basis must be a small regular file")
    try:
        raw = json.loads(basis_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseValidationError("invalid release basis JSON") from exc
    if not isinstance(raw, dict):
        raise ReleaseValidationError("release basis must be a JSON object")
    return ReleaseBasis.from_mapping(raw)


def _public_tree_manifest(public_root: Path) -> dict[str, object]:
    if public_root.is_symlink() or not public_root.is_dir():
        raise ReleaseValidationError("public root must be a regular directory")
    files: list[dict[str, object]] = []
    total_bytes = 0
    for current, directory_names, file_names in os.walk(public_root, followlinks=False):
        current_path = Path(current)
        for name in directory_names:
            directory = current_path / name
            if directory.is_symlink():
                raise ReleaseValidationError(f"public tree contains symlink: {directory}")
        for name in file_names:
            path = current_path / name
            try:
                details = path.lstat()
            except OSError as exc:
                raise ReleaseValidationError(f"public file is unreadable: {path}") from exc
            if path.is_symlink():
                raise ReleaseValidationError(f"public tree contains symlink: {path}")
            if not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
                raise ReleaseValidationError(f"public tree contains non-regular file: {path}")
            if details.st_mode & 0o111:
                raise ReleaseValidationError(f"public tree contains executable file: {path}")
            if details.st_size > _MAX_PUBLIC_FILE_BYTES:
                raise ReleaseValidationError(f"public file exceeds size limit: {path}")
            relative = path.relative_to(public_root).as_posix()
            if (
                not relative
                or relative.startswith("/")
                or "\\" in relative
                or any(part in {"", ".", ".."} for part in relative.split("/"))
            ):
                raise ReleaseValidationError(f"unsafe public path: {relative!r}")
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(path, flags)
            try:
                opened = os.fstat(descriptor)
                digest = hashlib.sha256()
                size = 0
                while True:
                    chunk = os.read(descriptor, 1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    size += len(chunk)
                closed = os.fstat(descriptor)
            finally:
                os.close(descriptor)
            if (
                opened.st_ino != closed.st_ino
                or opened.st_size != closed.st_size
                or opened.st_mtime_ns != closed.st_mtime_ns
                or size != opened.st_size
            ):
                raise ReleaseValidationError(f"public file changed while hashing: {relative}")
            files.append({"path": relative, "bytes": size, "sha256": digest.hexdigest()})
            total_bytes += size
            if len(files) > _MAX_PUBLIC_FILES:
                raise ReleaseValidationError("public tree contains too many files")
            if total_bytes > _MAX_PUBLIC_TREE_BYTES:
                raise ReleaseValidationError("public tree exceeds total size limit")
    if not files:
        raise ReleaseValidationError("public tree must not be empty")
    files.sort(key=lambda item: str(item["path"]))
    return {
        "schema_version": _TREE_SCHEMA_VERSION,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "files": files,
    }


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _validate_public_identity(public_root: Path, basis: ReleaseBasis) -> None:
    manifest_path = public_root / "api/v1/manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseValidationError("public API manifest is missing or invalid") from exc
    if not isinstance(manifest, dict) or manifest.get("active_release") != basis.release_id:
        raise ReleaseValidationError("public API release identity mismatch")
    build = manifest.get("build")
    if not isinstance(build, dict):
        raise ReleaseValidationError("public API build identity is missing")
    expected = {
        "release_id": basis.release_id,
        "code_sha": basis.code_sha,
        "content_sha": basis.content_sha,
    }
    if any(build.get(field) != value for field, value in expected.items()):
        raise ReleaseValidationError("public API build identity mismatch")


def create_release_descriptor(
    *, public_root: Path | str, basis_path: Path | str, output_path: Path | str
) -> ReleaseDescriptor:
    public = Path(public_root)
    output = Path(output_path)
    basis = load_release_basis(basis_path)
    if output.exists() or output.is_symlink():
        raise ReleaseValidationError("release descriptor output must not already exist")
    tree_manifest_path = output.parent / "public-tree-manifest.json"
    if tree_manifest_path.exists() or tree_manifest_path.is_symlink():
        raise ReleaseValidationError("public tree manifest output must not already exist")
    tree_manifest = _public_tree_manifest(public)
    _validate_public_identity(public, basis)
    artifact_digest = hashlib.sha256(_canonical_json_bytes(tree_manifest)).hexdigest()
    descriptor = ReleaseDescriptor(
        code_sha=basis.code_sha,
        content_sha=basis.content_sha,
        schema_version=basis.schema_version,
        release_seq=basis.release_seq,
        artifact_digest=artifact_digest,
        artifact_digest_kind=_ARTIFACT_DIGEST_KIND,
        generated_at=basis.generated_at,
    )
    if descriptor.release_id != basis.release_id:
        raise ReleaseValidationError("release descriptor identity changed after render")
    write_release_descriptor(output, descriptor)
    payload = (
        json.dumps(
            tree_manifest,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=tree_manifest_path.parent,
            prefix=f".{tree_manifest_path.name}.",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            os.chmod(handle.name, 0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, tree_manifest_path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
    return descriptor


def write_release_descriptor(path: Path | str, descriptor: ReleaseDescriptor) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(
            descriptor.to_dict(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            os.chmod(handle.name, 0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, destination)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)


def _validate_expected(
    descriptor: ReleaseDescriptor,
    *,
    code_sha: str | None,
    content_sha: str | None,
    artifact_digest: str | None,
) -> None:
    expected = {
        "code_sha": code_sha,
        "content_sha": content_sha,
        "artifact_digest": artifact_digest,
    }
    for field_name, expected_value in expected.items():
        if expected_value is not None and getattr(descriptor, field_name) != expected_value:
            raise ReleaseValidationError(f"{field_name} does not match workflow input")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser(
        "create",
        help="bind a completed Hugo/Pagefind public tree to a release basis",
    )
    create.add_argument("--public-root", type=Path, required=True)
    create.add_argument("--basis", type=Path, required=True)
    create.add_argument("--output", type=Path, required=True)
    validate = subparsers.add_parser("validate", help="reject forged or stale release metadata")
    validate.add_argument("--candidate", type=Path, required=True)
    validate.add_argument("--current", type=Path)
    validate.add_argument("--expected-code-sha")
    validate.add_argument("--expected-content-sha")
    validate.add_argument("--expected-artifact-digest")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "create":
        descriptor = create_release_descriptor(
            public_root=args.public_root,
            basis_path=args.basis,
            output_path=args.output,
        )
        print(json.dumps(descriptor.to_dict(), separators=(",", ":"), sort_keys=True))
        return 0
    candidate = load_release_descriptor(args.candidate)
    current = load_release_descriptor(args.current) if args.current else None
    assert_release_is_fresh(candidate, current)
    _validate_expected(
        candidate,
        code_sha=args.expected_code_sha,
        content_sha=args.expected_content_sha,
        artifact_digest=args.expected_artifact_digest,
    )
    print(json.dumps(candidate.to_dict(), separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
