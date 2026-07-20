"""Immutable release identity and stale-deployment protection."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import io
import json
import os
import re
import stat
import tarfile
import tempfile
import zipfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import BinaryIO


class ReleaseValidationError(ValueError):
    """Raised when a release manifest cannot be trusted."""


_GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SCHEMA_VERSION = re.compile(r"[1-9][0-9]*\.[0-9]+\Z")
_ARTIFACT_DIGEST_KIND = "public_tree_manifest_v2"
_SUPPORTED_ARTIFACT_DIGEST_KINDS = frozenset(
    {"public_tree_manifest_v1", _ARTIFACT_DIGEST_KIND}
)
_BASIS_SCHEMA_VERSION = "release_basis_v1"
_TREE_SCHEMA_VERSION = "public_tree_manifest_v2"
_PREVIOUS_TREE_SCHEMA_VERSION = "public_tree_manifest_v1"
_SUPPORTED_TREE_SCHEMA_VERSIONS = frozenset(
    {_PREVIOUS_TREE_SCHEMA_VERSION, _TREE_SCHEMA_VERSION}
)
# At 30k files, POSIX tar's mandatory 512-byte header alone is already
# 14.65 MiB.  This fuse bounds traversal/inode pressure and deliberately stops
# the current oversized topology before upload; it is not an acceptance target.
_MAX_PUBLIC_FILES = 30_000
_MAX_PUBLIC_DIRECTORIES = 30_000
_MAX_PUBLIC_FILE_BYTES = 16 * 1024 * 1024
_MAX_PUBLIC_TREE_BYTES = 256 * 1024 * 1024
_MAX_TREE_MANIFEST_BYTES = 8 * 1024 * 1024
_PAGES_ARTIFACT_WARNING_BYTES = 90 * 1024 * 1024
_MAX_PAGES_ARTIFACT_BYTES = 100 * 1024 * 1024
_PAGES_ARTIFACT_SCHEMA_VERSION = "pages_artifact_estimate_v1"
_PAGES_ARTIFACT_ARCHIVE_NAME = "artifact.tar"
_PAGES_ARTIFACT_COMPRESSION = "zip_deflate"
_PAGES_ARTIFACT_COMPRESSION_LEVEL = 6
_TREE_V1_FIELDS = frozenset({"schema_version", "file_count", "total_bytes", "files"})
_TREE_V2_FIELDS = _TREE_V1_FIELDS.union(
    {"route_count", "route_digest", "pages_artifact"}
)
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
        if self.artifact_digest_kind not in _SUPPORTED_ARTIFACT_DIGEST_KINDS:
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


def assert_release_matches(
    candidate: ReleaseDescriptor,
    current: ReleaseDescriptor,
) -> None:
    """Require a consumer to use the descriptor persisted after health.

    Freshness is the deploy-time rule.  Publisher consumption happens after
    the candidate has become the current healthy release, so it needs exact
    equality instead of another monotonicity comparison.
    """

    if candidate != current:
        raise ReleaseValidationError("healthy release mismatch")


def load_release_descriptor(path: Path | str) -> ReleaseDescriptor:
    manifest = Path(path)
    try:
        stat = manifest.lstat()
    except OSError as exc:
        raise ReleaseValidationError("release manifest is unreadable") from exc
    if (
        manifest.is_symlink()
        or not manifest.is_file()
        or stat.st_nlink != 1
        or stat.st_size > 64 * 1024
    ):
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


def _html_routes(paths: Sequence[str]) -> list[str]:
    routes: list[str] = []
    for relative in paths:
        if not relative.endswith(".html"):
            continue
        if relative == "index.html":
            route = "/"
        elif relative.endswith("/index.html"):
            route = f"/{relative.removesuffix('index.html')}"
        else:
            route = f"/{relative}"
        routes.append(route)
    routes.sort()
    if len(routes) != len(set(routes)):
        raise ReleaseValidationError("public tree contains duplicate HTML routes")
    return routes


def _route_digest(routes: Sequence[str]) -> str:
    return hashlib.sha256(_canonical_json_bytes(list(routes))).hexdigest()


def _pages_artifact_status(estimated_bytes: int) -> str:
    if (
        not isinstance(estimated_bytes, int)
        or isinstance(estimated_bytes, bool)
        or estimated_bytes <= 0
    ):
        raise ReleaseValidationError("Pages artifact estimate must be positive")
    if estimated_bytes >= _MAX_PAGES_ARTIFACT_BYTES:
        raise ReleaseValidationError(
            "estimated Pages artifact reaches the 100 MiB hard limit"
        )
    if estimated_bytes >= _PAGES_ARTIFACT_WARNING_BYTES:
        return "warning"
    return "ok"


def _pages_artifact_metadata(
    estimated_bytes: int,
    *,
    directory_count: int,
    file_count: int,
) -> dict[str, object]:
    return {
        "schema_version": _PAGES_ARTIFACT_SCHEMA_VERSION,
        "archive_name": _PAGES_ARTIFACT_ARCHIVE_NAME,
        "compression": _PAGES_ARTIFACT_COMPRESSION,
        "compression_level": _PAGES_ARTIFACT_COMPRESSION_LEVEL,
        "estimated_bytes": estimated_bytes,
        "warning_at_bytes": _PAGES_ARTIFACT_WARNING_BYTES,
        "hard_limit_bytes": _MAX_PAGES_ARTIFACT_BYTES,
        "status": _pages_artifact_status(estimated_bytes),
        "directory_count": directory_count,
        "tar_entry_count": 1 + directory_count + file_count,
    }


def _validate_pages_artifact_metadata(value: object, *, file_count: int) -> None:
    fields = {
        "schema_version",
        "archive_name",
        "compression",
        "compression_level",
        "estimated_bytes",
        "warning_at_bytes",
        "hard_limit_bytes",
        "status",
        "directory_count",
        "tar_entry_count",
    }
    if not isinstance(value, dict) or set(value) != fields:
        raise ReleaseValidationError("Pages artifact estimate fields are invalid")
    expected_constants: dict[str, object] = {
        "schema_version": _PAGES_ARTIFACT_SCHEMA_VERSION,
        "archive_name": _PAGES_ARTIFACT_ARCHIVE_NAME,
        "compression": _PAGES_ARTIFACT_COMPRESSION,
        "compression_level": _PAGES_ARTIFACT_COMPRESSION_LEVEL,
        "warning_at_bytes": _PAGES_ARTIFACT_WARNING_BYTES,
        "hard_limit_bytes": _MAX_PAGES_ARTIFACT_BYTES,
    }
    if any(value.get(field) != expected for field, expected in expected_constants.items()):
        raise ReleaseValidationError("Pages artifact estimate policy is invalid")
    estimated_bytes = value.get("estimated_bytes")
    if not isinstance(estimated_bytes, int) or isinstance(estimated_bytes, bool):
        raise ReleaseValidationError("Pages artifact estimate is invalid")
    if value.get("status") != _pages_artifact_status(estimated_bytes):
        raise ReleaseValidationError("Pages artifact estimate status is invalid")
    directory_count = value.get("directory_count")
    tar_entry_count = value.get("tar_entry_count")
    if (
        not isinstance(directory_count, int)
        or isinstance(directory_count, bool)
        or not 0 <= directory_count <= _MAX_PUBLIC_DIRECTORIES
        or not isinstance(tar_entry_count, int)
        or isinstance(tar_entry_count, bool)
        or tar_entry_count != 1 + directory_count + file_count
    ):
        raise ReleaseValidationError("Pages artifact directory inventory is invalid")


def _load_public_tree_manifest(path: Path | str) -> dict[str, object]:
    manifest_path = Path(path)
    try:
        details = manifest_path.lstat()
    except OSError as exc:
        raise ReleaseValidationError("public tree manifest is unreadable") from exc
    if (
        manifest_path.is_symlink()
        or not stat.S_ISREG(details.st_mode)
        or details.st_nlink != 1
        or details.st_size > _MAX_TREE_MANIFEST_BYTES
    ):
        raise ReleaseValidationError("public tree manifest must be a bounded regular file")
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseValidationError("invalid public tree manifest JSON") from exc
    if not isinstance(raw, dict):
        raise ReleaseValidationError("public tree manifest must be a JSON object")
    schema_version = raw.get("schema_version")
    if schema_version not in _SUPPORTED_TREE_SCHEMA_VERSIONS:
        raise ReleaseValidationError("public tree manifest schema is invalid")
    expected_fields = (
        _TREE_V2_FIELDS if schema_version == _TREE_SCHEMA_VERSION else _TREE_V1_FIELDS
    )
    if set(raw) != expected_fields:
        raise ReleaseValidationError("public tree manifest fields are invalid")
    file_count = raw.get("file_count")
    total_bytes = raw.get("total_bytes")
    files = raw.get("files")
    if (
        not isinstance(file_count, int)
        or isinstance(file_count, bool)
        or not 0 < file_count <= _MAX_PUBLIC_FILES
        or not isinstance(total_bytes, int)
        or isinstance(total_bytes, bool)
        or not 0 <= total_bytes <= _MAX_PUBLIC_TREE_BYTES
        or not isinstance(files, list)
        or len(files) != file_count
    ):
        raise ReleaseValidationError("public tree manifest totals are invalid")

    seen: set[str] = set()
    paths: list[str] = []
    calculated_bytes = 0
    previous_path = ""
    for entry in files:
        if not isinstance(entry, dict) or set(entry) != {"path", "bytes", "sha256"}:
            raise ReleaseValidationError("public tree manifest file entry is invalid")
        relative = entry.get("path")
        size = entry.get("bytes")
        digest = entry.get("sha256")
        if (
            not isinstance(relative, str)
            or len(relative) > 1_024
            or any(ord(character) < 32 for character in relative)
            or relative.startswith("/")
            or "\\" in relative
            or any(part in {"", ".", ".."} for part in relative.split("/"))
            or relative in seen
            or relative <= previous_path
        ):
            raise ReleaseValidationError("public tree manifest path is invalid")
        if (
            not isinstance(size, int)
            or isinstance(size, bool)
            or not 0 <= size <= _MAX_PUBLIC_FILE_BYTES
        ):
            raise ReleaseValidationError("public tree manifest file size is invalid")
        if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
            raise ReleaseValidationError("public tree manifest file digest is invalid")
        seen.add(relative)
        paths.append(relative)
        previous_path = relative
        calculated_bytes += size
    if calculated_bytes != total_bytes:
        raise ReleaseValidationError("public tree manifest totals are invalid")
    if schema_version == _TREE_SCHEMA_VERSION:
        routes = _html_routes(paths)
        route_count = raw.get("route_count")
        route_digest = raw.get("route_digest")
        if (
            not routes
            or not isinstance(route_count, int)
            or isinstance(route_count, bool)
            or route_count != len(routes)
            or not isinstance(route_digest, str)
            or not _SHA256.fullmatch(route_digest)
            or not hmac.compare_digest(route_digest, _route_digest(routes))
        ):
            raise ReleaseValidationError("public tree HTML route inventory is invalid")
        _validate_pages_artifact_metadata(raw.get("pages_artifact"), file_count=file_count)
    return raw


def validate_public_tree_manifest_digest(
    descriptor: ReleaseDescriptor,
    manifest_path: Path | str,
) -> None:
    manifest = _load_public_tree_manifest(manifest_path)
    if descriptor.artifact_digest_kind != manifest["schema_version"]:
        raise ReleaseValidationError("public tree manifest digest kind mismatch")
    actual = hashlib.sha256(_canonical_json_bytes(manifest)).hexdigest()
    if not hmac.compare_digest(actual, descriptor.artifact_digest):
        raise ReleaseValidationError("public tree manifest digest mismatch")


def _file_version(details: os.stat_result) -> tuple[int, ...]:
    return (
        details.st_dev,
        details.st_ino,
        details.st_mode,
        details.st_nlink,
        details.st_size,
        details.st_mtime_ns,
        details.st_ctime_ns,
    )


def _hash_public_file(path: Path, initial: os.stat_result, relative: str) -> tuple[int, str]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        file_descriptor = os.open(path, flags)
    except OSError as exc:
        raise ReleaseValidationError(f"public file is unreadable: {path}") from exc
    try:
        opened = os.fstat(file_descriptor)
        if _file_version(initial) != _file_version(opened):
            raise ReleaseValidationError(f"public file changed while opening: {relative}")
        digest = hashlib.sha256()
        size = 0
        while True:
            chunk = os.read(file_descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
        closed = os.fstat(file_descriptor)
    except OSError as exc:
        raise ReleaseValidationError(f"public file changed while hashing: {relative}") from exc
    finally:
        os.close(file_descriptor)
    try:
        final = path.lstat()
    except OSError as exc:
        raise ReleaseValidationError(f"public file changed while hashing: {relative}") from exc
    if (
        _file_version(opened) != _file_version(closed)
        or _file_version(opened) != _file_version(final)
        or size != opened.st_size
    ):
        raise ReleaseValidationError(f"public file changed while hashing: {relative}")
    return size, digest.hexdigest()


class _HashingReader(io.RawIOBase):
    def __init__(self, source: BinaryIO) -> None:
        super().__init__()
        self._source = source
        self.digest = hashlib.sha256()
        self.bytes_read = 0

    def readable(self) -> bool:
        return True

    def read(self, size: int = -1) -> bytes:
        chunk = self._source.read(size)
        self.digest.update(chunk)
        self.bytes_read += len(chunk)
        return chunk


def _write_deterministic_tar(
    public_root: Path,
    files: Sequence[dict[str, object]],
    directories: Sequence[str],
    destination: Path,
) -> None:
    try:
        archive = tarfile.open(
            destination,
            mode="w",
            format=tarfile.PAX_FORMAT,
            encoding="utf-8",
            errors="strict",
        )
    except (OSError, tarfile.TarError) as exc:
        raise ReleaseValidationError("cannot create Pages artifact estimate tar") from exc
    file_entries: dict[str, dict[str, object]] = {}
    for file_entry in files:
        relative = file_entry.get("path")
        if not isinstance(relative, str) or relative in file_entries:
            raise ReleaseValidationError("public tree manifest file entry is invalid")
        file_entries[relative] = file_entry
    if len(directories) != len(set(directories)):
        raise ReleaseValidationError("public tree directory inventory is invalid")
    archive_entries: list[tuple[str, dict[str, object] | None]] = [
        (".", None),
        *((relative, None) for relative in directories),
        *file_entries.items(),
    ]
    archive_entries.sort(key=lambda item: item[0])
    with archive:
        for relative, archive_entry in archive_entries:
            if archive_entry is None:
                path = public_root if relative == "." else public_root / relative
                try:
                    initial = path.lstat()
                except OSError as exc:
                    raise ReleaseValidationError(
                        f"public directory changed after tree scan: {relative}"
                    ) from exc
                if path.is_symlink() or not stat.S_ISDIR(initial.st_mode):
                    raise ReleaseValidationError(
                        f"public directory changed after tree scan: {relative}"
                    )
                tar_info = tarfile.TarInfo(relative)
                tar_info.size = 0
                tar_info.mode = 0o755
                tar_info.uid = 0
                tar_info.gid = 0
                tar_info.uname = ""
                tar_info.gname = ""
                tar_info.mtime = 0
                tar_info.type = tarfile.DIRTYPE
                tar_info.pax_headers = {}
                try:
                    archive.addfile(tar_info)
                    final = path.lstat()
                except (OSError, tarfile.TarError) as exc:
                    raise ReleaseValidationError(
                        f"public directory changed while archiving: {relative}"
                    ) from exc
                if _file_version(initial) != _file_version(final):
                    raise ReleaseValidationError(
                        f"public directory changed while archiving: {relative}"
                    )
                continue
            expected_size = archive_entry["bytes"]
            expected_digest = archive_entry["sha256"]
            if (
                not isinstance(relative, str)
                or not isinstance(expected_size, int)
                or isinstance(expected_size, bool)
                or not isinstance(expected_digest, str)
            ):
                raise ReleaseValidationError("public tree manifest file entry is invalid")
            path = public_root / relative
            try:
                initial = path.lstat()
            except OSError as exc:
                raise ReleaseValidationError(
                    f"public file changed after tree hash: {relative}"
                ) from exc
            if (
                path.is_symlink()
                or not stat.S_ISREG(initial.st_mode)
                or initial.st_nlink != 1
                or initial.st_mode & 0o111
                or initial.st_size != expected_size
            ):
                raise ReleaseValidationError(f"public file changed after tree hash: {relative}")
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            try:
                file_descriptor = os.open(path, flags)
            except OSError as exc:
                raise ReleaseValidationError(
                    f"public file changed after tree hash: {relative}"
                ) from exc
            try:
                with os.fdopen(file_descriptor, "rb", closefd=True) as source:
                    opened = os.fstat(source.fileno())
                    if _file_version(initial) != _file_version(opened):
                        raise ReleaseValidationError(
                            f"public file changed after tree hash: {relative}"
                        )
                    reader = _HashingReader(source)
                    tar_info = tarfile.TarInfo(relative)
                    tar_info.size = expected_size
                    tar_info.mode = 0o644
                    tar_info.uid = 0
                    tar_info.gid = 0
                    tar_info.uname = ""
                    tar_info.gname = ""
                    tar_info.mtime = 0
                    tar_info.type = tarfile.REGTYPE
                    tar_info.pax_headers = {}
                    try:
                        archive.addfile(tar_info, reader)
                    except (OSError, tarfile.TarError) as exc:
                        raise ReleaseValidationError(
                            f"public file changed while archiving: {relative}"
                        ) from exc
                    closed = os.fstat(source.fileno())
            except OSError as exc:
                raise ReleaseValidationError(
                    f"public file changed while archiving: {relative}"
                ) from exc
            try:
                final = path.lstat()
            except OSError as exc:
                raise ReleaseValidationError(
                    f"public file changed while archiving: {relative}"
                ) from exc
            if (
                _file_version(opened) != _file_version(closed)
                or _file_version(opened) != _file_version(final)
                or reader.bytes_read != expected_size
                or not hmac.compare_digest(reader.digest.hexdigest(), expected_digest)
            ):
                raise ReleaseValidationError(f"public file changed after tree hash: {relative}")


def _write_deterministic_zip(tar_path: Path, destination: Path) -> int:
    member = zipfile.ZipInfo(
        filename=_PAGES_ARTIFACT_ARCHIVE_NAME,
        date_time=(1980, 1, 1, 0, 0, 0),
    )
    member.compress_type = zipfile.ZIP_DEFLATED
    member.create_system = 3
    member.external_attr = (stat.S_IFREG | 0o644) << 16
    member.extra = b""
    member.comment = b""
    # ZipFile.open has no public per-entry level argument before Python 3.13.
    # ZipInfo stores the explicit level used by the stdlib's streaming writer.
    member._compresslevel = _PAGES_ARTIFACT_COMPRESSION_LEVEL  # type: ignore[attr-defined]
    try:
        with zipfile.ZipFile(
            destination,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=_PAGES_ARTIFACT_COMPRESSION_LEVEL,
            allowZip64=False,
        ) as archive:
            with tar_path.open("rb") as source, archive.open(member, mode="w") as target:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    target.write(chunk)
                    if archive.fp is None or archive.fp.tell() >= _MAX_PAGES_ARTIFACT_BYTES:
                        raise ReleaseValidationError(
                            "estimated Pages artifact reaches the 100 MiB hard limit"
                        )
    except ReleaseValidationError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise ReleaseValidationError("cannot create Pages artifact estimate ZIP") from exc
    try:
        estimated_bytes = destination.stat().st_size
    except OSError as exc:
        raise ReleaseValidationError("Pages artifact estimate ZIP is unreadable") from exc
    _pages_artifact_status(estimated_bytes)
    return estimated_bytes


def _estimate_pages_artifact(
    public_root: Path,
    files: list[dict[str, object]],
    directories: list[str],
) -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="ai-stack-pages-estimate-") as temporary:
            temporary_root = Path(temporary)
            tar_path = temporary_root / _PAGES_ARTIFACT_ARCHIVE_NAME
            zip_path = temporary_root / "artifact.zip"
            _write_deterministic_tar(public_root, files, directories, tar_path)
            return _write_deterministic_zip(tar_path, zip_path)
    except ReleaseValidationError:
        raise
    except OSError as exc:
        raise ReleaseValidationError("cannot allocate Pages artifact estimate files") from exc


def _public_tree_manifest(public_root: Path) -> dict[str, object]:
    if public_root.is_symlink() or not public_root.is_dir():
        raise ReleaseValidationError("public root must be a regular directory")
    files: list[dict[str, object]] = []
    directories: list[str] = []
    total_bytes = 0
    for current, directory_names, file_names in os.walk(public_root, followlinks=False):
        current_path = Path(current)
        directory_names.sort()
        file_names.sort()
        for name in directory_names:
            directory = current_path / name
            try:
                directory_details = directory.lstat()
            except OSError as exc:
                raise ReleaseValidationError(
                    f"public directory is unreadable: {directory}"
                ) from exc
            if directory.is_symlink() or not stat.S_ISDIR(directory_details.st_mode):
                raise ReleaseValidationError(f"public tree contains symlink: {directory}")
            relative_directory = directory.relative_to(public_root).as_posix()
            if (
                not relative_directory
                or relative_directory.startswith("/")
                or "\\" in relative_directory
                or any(
                    part in {"", ".", ".."} for part in relative_directory.split("/")
                )
            ):
                raise ReleaseValidationError(
                    f"unsafe public directory path: {relative_directory!r}"
                )
            directories.append(relative_directory)
            if len(directories) > _MAX_PUBLIC_DIRECTORIES:
                raise ReleaseValidationError("public tree contains too many directories")
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
            size, digest = _hash_public_file(path, details, relative)
            files.append({"path": relative, "bytes": size, "sha256": digest})
            total_bytes += size
            if len(files) > _MAX_PUBLIC_FILES:
                raise ReleaseValidationError("public tree contains too many files")
            if total_bytes > _MAX_PUBLIC_TREE_BYTES:
                raise ReleaseValidationError("public tree exceeds total size limit")
    if not files:
        raise ReleaseValidationError("public tree must not be empty")
    files.sort(key=lambda item: str(item["path"]))
    directories.sort()
    routes = _html_routes([str(item["path"]) for item in files])
    if not routes:
        raise ReleaseValidationError("public tree must contain at least one HTML route")
    estimated_bytes = _estimate_pages_artifact(public_root, files, directories)
    return {
        "schema_version": _TREE_SCHEMA_VERSION,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "route_count": len(routes),
        "route_digest": _route_digest(routes),
        "pages_artifact": _pages_artifact_metadata(
            estimated_bytes,
            directory_count=len(directories),
            file_count=len(files),
        ),
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
    release_id: str | None,
) -> None:
    expected = {
        "code_sha": code_sha,
        "content_sha": content_sha,
        "artifact_digest": artifact_digest,
        "release_id": release_id,
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
    validate.add_argument("--tree-manifest", type=Path)
    validate.add_argument("--expected-release-id")
    validate.add_argument("--expected-code-sha")
    validate.add_argument("--expected-content-sha")
    validate.add_argument("--expected-artifact-digest")
    verify = subparsers.add_parser(
        "verify",
        help="bind a post-health consumer to the exact persisted healthy release",
    )
    verify.add_argument("--candidate", type=Path, required=True)
    verify.add_argument("--current", type=Path, required=True)
    verify.add_argument("--tree-manifest", type=Path, required=True)
    verify.add_argument("--expected-release-id")
    verify.add_argument("--expected-code-sha")
    verify.add_argument("--expected-content-sha")
    verify.add_argument("--expected-artifact-digest")
    marker = subparsers.add_parser(
        "guard-marker",
        help="bind ai_stack_release_v1 marker to the complete Pages tree",
    )
    marker.add_argument("--public-root", type=Path, required=True)
    marker.add_argument("--marker", type=Path, required=True)
    marker.add_argument("--expected-sha", required=True)
    marker.add_argument("--tree-manifest-output", type=Path, required=True)
    marker.add_argument("--require-lineage", action="store_true")
    return parser


def _guard_marker(
    *,
    public_root: Path,
    marker_path: Path,
    expected_sha: str,
    tree_manifest_output: Path,
    require_lineage: bool,
) -> dict[str, object]:
    if __package__:
        from scripts.release_marker import ReleaseMarkerError, verify_release_marker
    else:
        from release_marker import ReleaseMarkerError, verify_release_marker

    try:
        marker_details = marker_path.lstat()
        if (
            marker_path.is_symlink()
            or not stat.S_ISREG(marker_details.st_mode)
            or marker_details.st_nlink != 1
            or marker_details.st_size > 128 * 1024
        ):
            raise ReleaseValidationError("release marker must be a small regular file")
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseValidationError("release marker is unreadable or invalid") from exc
    if not isinstance(marker, dict):
        raise ReleaseValidationError("release marker must be a JSON object")
    try:
        verified = verify_release_marker(
            public_root,
            marker,
            expected_sha=expected_sha,
            require_lineage=require_lineage,
        )
    except ReleaseMarkerError as exc:
        raise ReleaseValidationError(str(exc)) from exc
    tree = _public_tree_manifest(public_root)
    if not any(
        item.get("path") == marker_path.relative_to(public_root).as_posix()
        for item in tree["files"]
        if isinstance(item, dict)
    ):
        raise ReleaseValidationError("release marker is outside the Pages tree")
    if tree_manifest_output.exists() or tree_manifest_output.is_symlink():
        raise ReleaseValidationError("tree manifest output must not already exist")
    tree_manifest_output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(tree, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=tree_manifest_output.parent,
            prefix=f".{tree_manifest_output.name}.",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            os.chmod(handle.name, 0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, tree_manifest_output)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
    return {
        "release_id": verified["release_id"],
        "exact_sha": verified["exact_sha"],
        "tree_digest": hashlib.sha256(_canonical_json_bytes(tree)).hexdigest(),
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "guard-marker":
        result = _guard_marker(
            public_root=args.public_root,
            marker_path=args.marker,
            expected_sha=args.expected_sha,
            tree_manifest_output=args.tree_manifest_output,
            require_lineage=args.require_lineage,
        )
        print(json.dumps(result, separators=(",", ":"), sort_keys=True))
        return 0
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
    if args.command == "verify":
        if current is None:  # argparse requires it, retained for type narrowing.
            raise ReleaseValidationError("current healthy release is required")
        assert_release_matches(candidate, current)
    else:
        assert_release_is_fresh(candidate, current)
    _validate_expected(
        candidate,
        code_sha=args.expected_code_sha,
        content_sha=args.expected_content_sha,
        artifact_digest=args.expected_artifact_digest,
        release_id=args.expected_release_id,
    )
    if args.tree_manifest is not None:
        validate_public_tree_manifest_digest(candidate, args.tree_manifest)
    print(json.dumps(candidate.to_dict(), separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
