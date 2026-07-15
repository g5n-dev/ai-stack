"""Safely compact Pagefind result fragments into one release-bound catalog."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unicodedata
import uuid
import zlib
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import cast
from urllib.parse import urlsplit, urlunsplit


class PagefindCatalogError(ValueError):
    """Raised when Pagefind output cannot be compacted without losing integrity."""


CATALOG_SCHEMA_VERSION = "pagefind_result_catalog_v1"
MANIFEST_SCHEMA_VERSION = "pagefind_result_catalog_manifest_v1"
RELEASE_BASIS_SCHEMA_VERSION = "release_basis_v1"
REPOSITORY_BASIS_SCHEMA_VERSION = "repository_build_basis_v1"
PAGEFIND_FRAGMENT_PREFIX = b"pagefind_dcd"
CANONICAL_ORIGIN = "https://ai-stack.site"
SUMMARY_CODEPOINTS = 120

MAX_FRAGMENT_COUNT = 20_000
MAX_FRAGMENT_COMPRESSED_BYTES = 1024 * 1024
MAX_FRAGMENT_UNCOMPRESSED_BYTES = 4 * 1024 * 1024
MAX_TOTAL_FRAGMENT_COMPRESSED_BYTES = 256 * 1024 * 1024
MAX_CATALOG_BYTES = 32 * 1024 * 1024
MAX_CATALOG_GZIP_BYTES = 1024 * 1024
MAX_MANIFEST_BYTES = 128 * 1024
CATALOG_GZIP_LEVEL = 6

# Pagefind starts with seven hexadecimal hash characters and extends the hash
# when two fragments collide.  Accept the complete SHA-1 suffix so a future
# collision cannot make a valid index undeployable.
_FRAGMENT_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,15}_[0-9a-f]{7,40}\Z")
_GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SCHEMA_VERSION = re.compile(r"[1-9][0-9]*\.[0-9]+\Z")
_RELEASE_ID = re.compile(r"r-[0-9a-f]{24}\Z")


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _require_git_sha(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not _GIT_SHA.fullmatch(value):
        raise PagefindCatalogError(f"invalid {field_name}")
    return value


def _require_sha256(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise PagefindCatalogError(f"invalid {field_name}")
    return value


def _require_mapping(value: object, field_name: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise PagefindCatalogError(f"{field_name} must be an object")
    return cast(dict[str, object], value)


def _require_string(
    value: object,
    field_name: str,
    *,
    max_length: int,
    allow_empty: bool = False,
) -> str:
    if not isinstance(value, str) or len(value) > max_length or (not allow_empty and not value):
        raise PagefindCatalogError(f"invalid {field_name}")
    return value


def _release_identity(
    *, code_sha: str, content_sha: str, release_seq: int, schema_version: str
) -> str:
    identity = _canonical_json(
        {
            "code_sha": code_sha,
            "content_sha": content_sha,
            "release_seq": release_seq,
            "schema_version": schema_version,
        }
    )
    return "r-" + hashlib.sha256(identity).hexdigest()[:24]


@dataclass(frozen=True)
class CatalogBasis:
    """The non-self-referential code/content basis embedded in a catalog."""

    basis_schema_version: str
    code_sha: str
    content_sha: str
    schema_version: str | None = None
    release_seq: int | None = None
    generated_at: str | None = None
    release_basis_sha256: str | None = None

    def __post_init__(self) -> None:
        _require_git_sha(self.code_sha, "code_sha")
        _require_git_sha(self.content_sha, "content_sha")
        if self.basis_schema_version == REPOSITORY_BASIS_SCHEMA_VERSION:
            if any(
                value is not None
                for value in (
                    self.schema_version,
                    self.release_seq,
                    self.generated_at,
                    self.release_basis_sha256,
                )
            ):
                raise PagefindCatalogError("repository basis contains release-only fields")
            return
        if self.basis_schema_version != RELEASE_BASIS_SCHEMA_VERSION:
            raise PagefindCatalogError("invalid catalog basis schema")
        if not isinstance(self.schema_version, str) or not _SCHEMA_VERSION.fullmatch(
            self.schema_version
        ):
            raise PagefindCatalogError("invalid release schema_version")
        if (
            not isinstance(self.release_seq, int)
            or isinstance(self.release_seq, bool)
            or self.release_seq <= 0
        ):
            raise PagefindCatalogError("invalid release_seq")
        if not isinstance(self.generated_at, str):
            raise PagefindCatalogError("invalid release generated_at")
        try:
            datetime.strptime(self.generated_at, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as exc:
            raise PagefindCatalogError("invalid release generated_at") from exc
        _require_sha256(self.release_basis_sha256, "release_basis_sha256")

    @classmethod
    def repository(cls, *, code_sha: str, content_sha: str) -> CatalogBasis:
        return cls(
            basis_schema_version=REPOSITORY_BASIS_SCHEMA_VERSION,
            code_sha=code_sha,
            content_sha=content_sha,
        )

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> CatalogBasis:
        schema = value.get("basis_schema_version")
        if schema == REPOSITORY_BASIS_SCHEMA_VERSION:
            expected = {"basis_schema_version", "code_sha", "content_sha"}
            if set(value) != expected:
                raise PagefindCatalogError("invalid repository catalog basis fields")
            return cls.repository(
                code_sha=_require_git_sha(value.get("code_sha"), "code_sha"),
                content_sha=_require_git_sha(value.get("content_sha"), "content_sha"),
            )
        if schema != RELEASE_BASIS_SCHEMA_VERSION:
            raise PagefindCatalogError("invalid catalog basis schema")
        expected = {
            "basis_schema_version",
            "code_sha",
            "content_sha",
            "schema_version",
            "release_seq",
            "generated_at",
            "release_basis_sha256",
        }
        if set(value) != expected:
            raise PagefindCatalogError("invalid release catalog basis fields")
        return cls(
            basis_schema_version=RELEASE_BASIS_SCHEMA_VERSION,
            code_sha=_require_git_sha(value.get("code_sha"), "code_sha"),
            content_sha=_require_git_sha(value.get("content_sha"), "content_sha"),
            schema_version=cast(str, value.get("schema_version")),
            release_seq=cast(int, value.get("release_seq")),
            generated_at=cast(str, value.get("generated_at")),
            release_basis_sha256=cast(str, value.get("release_basis_sha256")),
        )

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "basis_schema_version": self.basis_schema_version,
            "code_sha": self.code_sha,
            "content_sha": self.content_sha,
        }
        if self.basis_schema_version == RELEASE_BASIS_SCHEMA_VERSION:
            result.update(
                {
                    "schema_version": self.schema_version,
                    "release_seq": self.release_seq,
                    "generated_at": self.generated_at,
                    "release_basis_sha256": self.release_basis_sha256,
                }
            )
        return result


@dataclass(frozen=True)
class CatalogRecord:
    fragment_id: str
    url: str
    title: str
    source: str
    date: str
    summary: str

    def to_dict(self) -> dict[str, str]:
        return {
            "url": self.url,
            "title": self.title,
            "source": self.source,
            "date": self.date,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class CatalogBuildReport:
    record_count: int
    source_fragment_tree_sha256: str
    catalog_sha256: str
    catalog_bytes: int
    catalog_gzip_bytes: int
    code_sha: str
    content_sha: str
    basis_schema_version: str
    release_basis_sha256: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "basis_schema_version": self.basis_schema_version,
            "catalog_bytes": self.catalog_bytes,
            "catalog_gzip_bytes": self.catalog_gzip_bytes,
            "catalog_sha256": self.catalog_sha256,
            "code_sha": self.code_sha,
            "content_sha": self.content_sha,
            "record_count": self.record_count,
            "release_basis_sha256": self.release_basis_sha256,
            "source_fragment_tree_sha256": self.source_fragment_tree_sha256,
        }


@dataclass(frozen=True)
class _FragmentSnapshot:
    path: Path
    fragment_id: str
    compressed_bytes: int
    compressed_sha256: str
    uncompressed_bytes: int


def _load_release_basis(path: Path) -> CatalogBasis:
    try:
        details = path.lstat()
    except OSError as exc:
        raise PagefindCatalogError("release basis is unreadable") from exc
    if (
        path.is_symlink()
        or not stat.S_ISREG(details.st_mode)
        or details.st_nlink != 1
        or details.st_size > MAX_MANIFEST_BYTES
    ):
        raise PagefindCatalogError("release basis must be a bounded single-link regular file")
    raw = _read_regular(path, MAX_MANIFEST_BYTES, "release basis")
    value = _load_json(raw, "release basis")
    mapping = _require_mapping(value, "release basis")
    expected = {
        "basis_schema_version",
        "release_id",
        "code_sha",
        "content_sha",
        "schema_version",
        "release_seq",
        "generated_at",
    }
    if (
        set(mapping) != expected
        or mapping.get("basis_schema_version") != RELEASE_BASIS_SCHEMA_VERSION
    ):
        raise PagefindCatalogError("release basis fields or schema are invalid")
    code_sha = _require_git_sha(mapping.get("code_sha"), "release basis code_sha")
    content_sha = _require_git_sha(mapping.get("content_sha"), "release basis content_sha")
    schema_version = _require_string(
        mapping.get("schema_version"), "release basis schema_version", max_length=32
    )
    if not _SCHEMA_VERSION.fullmatch(schema_version):
        raise PagefindCatalogError("invalid release basis schema_version")
    release_seq = mapping.get("release_seq")
    if not isinstance(release_seq, int) or isinstance(release_seq, bool) or release_seq <= 0:
        raise PagefindCatalogError("invalid release basis release_seq")
    generated_at = _require_string(
        mapping.get("generated_at"), "release basis generated_at", max_length=32
    )
    try:
        datetime.strptime(generated_at, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise PagefindCatalogError("invalid release basis generated_at") from exc
    release_id = _require_string(
        mapping.get("release_id"), "release basis release_id", max_length=26
    )
    expected_release_id = _release_identity(
        code_sha=code_sha,
        content_sha=content_sha,
        release_seq=release_seq,
        schema_version=schema_version,
    )
    if not _RELEASE_ID.fullmatch(release_id) or release_id != expected_release_id:
        raise PagefindCatalogError("release basis release_id mismatch")
    normalized_without_release_id = {
        "basis_schema_version": RELEASE_BASIS_SCHEMA_VERSION,
        "code_sha": code_sha,
        "content_sha": content_sha,
        "schema_version": schema_version,
        "release_seq": release_seq,
        "generated_at": generated_at,
    }
    basis_digest = hashlib.sha256(_canonical_json(normalized_without_release_id)).hexdigest()
    return CatalogBasis(
        basis_schema_version=RELEASE_BASIS_SCHEMA_VERSION,
        code_sha=code_sha,
        content_sha=content_sha,
        schema_version=schema_version,
        release_seq=release_seq,
        generated_at=generated_at,
        release_basis_sha256=basis_digest,
    )


def _git_head(directory: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=directory,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise PagefindCatalogError("cannot determine repository build basis") from exc
    return _require_git_sha(completed.stdout.strip(), "repository HEAD")


def _resolve_basis(
    *,
    release_basis_path: Path | None,
    code_sha: str | None,
    content_sha: str | None,
) -> CatalogBasis:
    selected_basis = release_basis_path
    if selected_basis is None:
        configured = os.environ.get("AI_STACK_RELEASE_BASIS")
        candidate = (
            Path(configured)
            if configured
            else Path("build-handoff/state/release-basis.json")
        )
        if candidate.exists() or candidate.is_symlink():
            selected_basis = candidate
    if selected_basis is not None:
        basis = _load_release_basis(selected_basis)
        if code_sha is not None and basis.code_sha != _require_git_sha(code_sha, "code_sha"):
            raise PagefindCatalogError("code_sha does not match release basis")
        if content_sha is not None and basis.content_sha != _require_git_sha(
            content_sha, "content_sha"
        ):
            raise PagefindCatalogError("content_sha does not match release basis")
        return basis

    code_candidate = code_sha or os.environ.get("CODE_SHA")
    content_candidate = content_sha or os.environ.get("CONTENT_SHA")
    if (code_candidate is None) != (content_candidate is None):
        raise PagefindCatalogError("code_sha and content_sha must be provided together")
    if code_candidate is None or content_candidate is None:
        head = _git_head(Path.cwd())
        code_candidate = head
        content_candidate = head
    return CatalogBasis.repository(
        code_sha=_require_git_sha(code_candidate, "code_sha"),
        content_sha=_require_git_sha(content_candidate, "content_sha"),
    )


def _require_directory(path: Path, field_name: str) -> None:
    try:
        details = path.lstat()
    except OSError as exc:
        raise PagefindCatalogError(f"{field_name} is missing") from exc
    if path.is_symlink() or not stat.S_ISDIR(details.st_mode):
        raise PagefindCatalogError(f"{field_name} must be a regular directory")


def _discover_fragment_paths(pagefind_root: Path, fragment_root: Path) -> list[Path]:
    _require_directory(pagefind_root, "Pagefind root")
    _require_directory(fragment_root, "Pagefind fragment directory")
    for current, directories, files in os.walk(pagefind_root, followlinks=False):
        current_path = Path(current)
        for directory in directories:
            candidate = current_path / directory
            if candidate.is_symlink():
                raise PagefindCatalogError("Pagefind tree must not contain directory links")
        for filename in files:
            if filename.endswith(".pf_fragment") and current_path != fragment_root:
                raise PagefindCatalogError(
                    "all fragments must be in the canonical fragment directory"
                )

    try:
        entries = sorted(fragment_root.iterdir(), key=lambda path: path.name)
    except OSError as exc:
        raise PagefindCatalogError("Pagefind fragment directory is unreadable") from exc
    if not entries:
        raise PagefindCatalogError("Pagefind fragment directory is empty")
    if len(entries) > MAX_FRAGMENT_COUNT:
        raise PagefindCatalogError("Pagefind fragment count exceeds the safety limit")
    paths: list[Path] = []
    seen: set[str] = set()
    for path in entries:
        if path.suffix != ".pf_fragment":
            raise PagefindCatalogError("unexpected file in Pagefind fragment directory")
        fragment_id = path.name.removesuffix(".pf_fragment")
        if not _FRAGMENT_ID.fullmatch(fragment_id):
            raise PagefindCatalogError("invalid Pagefind fragment ID")
        if fragment_id in seen:
            raise PagefindCatalogError("duplicate Pagefind fragment ID")
        seen.add(fragment_id)
        paths.append(path)
    return paths


def _read_regular(path: Path, limit: int, field_name: str) -> bytes:
    try:
        before = path.lstat()
    except OSError as exc:
        raise PagefindCatalogError(f"{field_name} is unreadable") from exc
    if (
        path.is_symlink()
        or not stat.S_ISREG(before.st_mode)
        or before.st_nlink != 1
    ):
        raise PagefindCatalogError(f"{field_name} must be a single-link regular file")
    if before.st_size > limit:
        raise PagefindCatalogError(f"{field_name} compressed size exceeds the safety limit")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise PagefindCatalogError(f"{field_name} cannot be opened safely") from exc
    try:
        opened = os.fstat(descriptor)
        if (
            opened.st_dev != before.st_dev
            or opened.st_ino != before.st_ino
            or not stat.S_ISREG(opened.st_mode)
            or opened.st_nlink != 1
            or opened.st_size > limit
        ):
            raise PagefindCatalogError(f"{field_name} changed before it was read")
        chunks: list[bytes] = []
        size = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, limit + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            if size > limit:
                raise PagefindCatalogError(
                    f"{field_name} compressed size exceeds the safety limit"
                )
        after = os.fstat(descriptor)
        if (
            after.st_size != opened.st_size
            or after.st_mtime_ns != opened.st_mtime_ns
            or after.st_ctime_ns != opened.st_ctime_ns
        ):
            raise PagefindCatalogError(f"{field_name} changed while it was read")
        return b"".join(chunks)
    except OSError as exc:
        raise PagefindCatalogError(f"{field_name} could not be read") from exc
    finally:
        os.close(descriptor)


def _decompress_fragment(compressed: bytes, field_name: str) -> bytes:
    if not compressed.startswith(b"\x1f\x8b"):
        raise PagefindCatalogError(f"{field_name} is not a gzip stream")
    decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        output = decompressor.decompress(compressed, MAX_FRAGMENT_UNCOMPRESSED_BYTES + 1)
        if len(output) > MAX_FRAGMENT_UNCOMPRESSED_BYTES or decompressor.unconsumed_tail:
            raise PagefindCatalogError(f"{field_name} decompressed size exceeds the safety limit")
        output += decompressor.flush(MAX_FRAGMENT_UNCOMPRESSED_BYTES + 1 - len(output))
    except zlib.error as exc:
        raise PagefindCatalogError(f"{field_name} contains invalid gzip data") from exc
    if len(output) > MAX_FRAGMENT_UNCOMPRESSED_BYTES:
        raise PagefindCatalogError(f"{field_name} decompressed size exceeds the safety limit")
    if not decompressor.eof:
        raise PagefindCatalogError(f"{field_name} contains a truncated gzip stream")
    if decompressor.unused_data:
        raise PagefindCatalogError(f"{field_name} must contain a single gzip member")
    return output


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PagefindCatalogError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> object:
    raise PagefindCatalogError(f"invalid JSON constant: {value}")


def _load_json(raw: bytes, field_name: str) -> object:
    try:
        return cast(
            object,
            json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=_reject_duplicate_keys,
                parse_constant=_reject_json_constant,
            ),
        )
    except PagefindCatalogError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PagefindCatalogError(f"{field_name} contains invalid JSON") from exc


def _sanitize_text(value: object, field_name: str, *, max_length: int) -> str:
    if not isinstance(value, str):
        raise PagefindCatalogError(f"invalid {field_name}")
    normalized = unicodedata.normalize("NFKC", value)
    visible = "".join(
        character
        for character in normalized
        if unicodedata.category(character) not in {"Cc", "Cf", "Cs", "Co", "Cn"}
    )
    collapsed = " ".join(visible.split())
    if not collapsed:
        raise PagefindCatalogError(f"invalid {field_name}")
    return collapsed[:max_length].rstrip()


def _safe_same_origin_url(value: object) -> str:
    if not isinstance(value, str) or not value or len(value) > 2048:
        raise PagefindCatalogError("invalid Pagefind result URL")
    if "\\" in value or any(character.isspace() or ord(character) < 32 for character in value):
        raise PagefindCatalogError("unsafe Pagefind result URL")
    try:
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc:
            if parsed.scheme != "https" or parsed.hostname != "ai-stack.site":
                raise PagefindCatalogError("cross-origin Pagefind result URL")
            if parsed.username is not None or parsed.password is not None:
                raise PagefindCatalogError("credentialed Pagefind result URL")
            if parsed.port not in {None, 443}:
                raise PagefindCatalogError("cross-origin Pagefind result URL")
        elif not value.startswith("/") or value.startswith("//"):
            raise PagefindCatalogError("unsafe Pagefind result URL")
    except ValueError as exc:
        raise PagefindCatalogError("invalid Pagefind result URL") from exc
    if not parsed.path.startswith("/") or parsed.path.startswith("//"):
        raise PagefindCatalogError("unsafe Pagefind result URL")
    return urlunsplit(("", "", parsed.path, parsed.query, parsed.fragment))


def _parse_fragment(fragment_id: str, compressed: bytes) -> tuple[CatalogRecord, int]:
    field_name = f"Pagefind fragment {fragment_id}"
    uncompressed = _decompress_fragment(compressed, field_name)
    if not uncompressed.startswith(PAGEFIND_FRAGMENT_PREFIX):
        raise PagefindCatalogError(f"{field_name} has an invalid Pagefind prefix")
    value = _load_json(uncompressed[len(PAGEFIND_FRAGMENT_PREFIX) :], field_name)
    payload = _require_mapping(value, field_name)
    metadata = _require_mapping(payload.get("meta"), f"{field_name} meta")
    title = _sanitize_text(metadata.get("title"), f"{field_name} title", max_length=300)
    source = _sanitize_text(metadata.get("source"), f"{field_name} source", max_length=200)
    date_text = _sanitize_text(metadata.get("date"), f"{field_name} date", max_length=10)
    try:
        if date.fromisoformat(date_text).isoformat() != date_text:
            raise ValueError
    except ValueError as exc:
        raise PagefindCatalogError(f"{field_name} contains an invalid date") from exc
    summary = _sanitize_text(
        payload.get("content"), f"{field_name} content", max_length=SUMMARY_CODEPOINTS
    )
    return (
        CatalogRecord(
            fragment_id=fragment_id,
            url=_safe_same_origin_url(payload.get("url")),
            title=title,
            source=source,
            date=date_text,
            summary=summary,
        ),
        len(uncompressed),
    )


def make_catalog_payload(
    records: Iterable[CatalogRecord],
    *,
    basis: CatalogBasis,
    source_fragment_tree_sha256: str,
) -> dict[str, object]:
    tree_digest = _require_sha256(
        source_fragment_tree_sha256, "source_fragment_tree_sha256"
    )
    mapped: dict[str, object] = {}
    for record in records:
        if not _FRAGMENT_ID.fullmatch(record.fragment_id):
            raise PagefindCatalogError("invalid Pagefind fragment ID")
        if record.fragment_id in mapped:
            raise PagefindCatalogError("duplicate fragment ID")
        mapped[record.fragment_id] = record.to_dict()
    return {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "summary_codepoints": SUMMARY_CODEPOINTS,
        "source_fragment_tree_sha256": tree_digest,
        "basis": basis.to_dict(),
        "record_count": len(mapped),
        "records": mapped,
    }


def _collect_fragments(
    pagefind_root: Path, fragment_root: Path
) -> tuple[list[CatalogRecord], list[_FragmentSnapshot], str]:
    paths = _discover_fragment_paths(pagefind_root, fragment_root)
    records: list[CatalogRecord] = []
    snapshots: list[_FragmentSnapshot] = []
    total_compressed = 0
    tree_entries: list[dict[str, object]] = []
    for path in paths:
        fragment_id = path.name.removesuffix(".pf_fragment")
        compressed = _read_regular(
            path,
            MAX_FRAGMENT_COMPRESSED_BYTES,
            f"Pagefind fragment {fragment_id}",
        )
        total_compressed += len(compressed)
        if total_compressed > MAX_TOTAL_FRAGMENT_COMPRESSED_BYTES:
            raise PagefindCatalogError("total Pagefind fragment size exceeds the safety limit")
        record, uncompressed_bytes = _parse_fragment(fragment_id, compressed)
        digest = hashlib.sha256(compressed).hexdigest()
        records.append(record)
        snapshot = _FragmentSnapshot(
            path=path,
            fragment_id=fragment_id,
            compressed_bytes=len(compressed),
            compressed_sha256=digest,
            uncompressed_bytes=uncompressed_bytes,
        )
        snapshots.append(snapshot)
        tree_entries.append(
            {
                "compressed_bytes": snapshot.compressed_bytes,
                "compressed_sha256": snapshot.compressed_sha256,
                "fragment_id": snapshot.fragment_id,
                "uncompressed_bytes": snapshot.uncompressed_bytes,
            }
        )
    tree_digest = hashlib.sha256(
        b"pagefind_fragment_tree_v1\0" + _canonical_json(tree_entries)
    ).hexdigest()
    return records, snapshots, tree_digest


def _verify_fragment_snapshot(
    pagefind_root: Path, fragment_root: Path, snapshots: Sequence[_FragmentSnapshot]
) -> None:
    current = _discover_fragment_paths(pagefind_root, fragment_root)
    if [path.name for path in current] != [snapshot.path.name for snapshot in snapshots]:
        raise PagefindCatalogError("Pagefind fragment set changed during catalog construction")
    for path, snapshot in zip(current, snapshots, strict=True):
        compressed = _read_regular(
            path,
            MAX_FRAGMENT_COMPRESSED_BYTES,
            f"Pagefind fragment {snapshot.fragment_id}",
        )
        if (
            len(compressed) != snapshot.compressed_bytes
            or hashlib.sha256(compressed).hexdigest() != snapshot.compressed_sha256
        ):
            raise PagefindCatalogError("Pagefind fragment changed during catalog construction")


def _ensure_replaceable_output(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    try:
        details = path.lstat()
    except OSError as exc:
        raise PagefindCatalogError("catalog output cannot be inspected") from exc
    if path.is_symlink() or not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
        raise PagefindCatalogError("catalog output must be a single-link regular file")


def _atomic_write(path: Path, payload: bytes) -> None:
    temporary: Path | None = None
    try:
        descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(name)
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except OSError as exc:
        raise PagefindCatalogError("catalog output could not be written atomically") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _read_artifact(path: Path, limit: int, field_name: str) -> bytes:
    return _read_regular(path, limit, field_name)


def _validate_catalog_record(fragment_id: str, value: object) -> None:
    if not _FRAGMENT_ID.fullmatch(fragment_id):
        raise PagefindCatalogError("invalid catalog fragment ID")
    record = _require_mapping(value, f"catalog record {fragment_id}")
    if set(record) != {"url", "title", "source", "date", "summary"}:
        raise PagefindCatalogError("invalid catalog record fields")
    if _safe_same_origin_url(record.get("url")) != record.get("url"):
        raise PagefindCatalogError("catalog URL is not canonical")
    limits = {"title": 300, "source": 200, "date": 10, "summary": SUMMARY_CODEPOINTS}
    for field_name, limit in limits.items():
        value_text = record.get(field_name)
        if _sanitize_text(value_text, field_name, max_length=limit) != value_text:
            raise PagefindCatalogError(f"catalog {field_name} is not canonical")
    date_text = cast(str, record["date"])
    try:
        if date.fromisoformat(date_text).isoformat() != date_text:
            raise ValueError
    except ValueError as exc:
        raise PagefindCatalogError("catalog date is invalid") from exc


def verify_catalog_artifact(
    catalog_path: Path | str, manifest_path: Path | str
) -> CatalogBuildReport:
    catalog_file = Path(catalog_path)
    manifest_file = Path(manifest_path)
    catalog_bytes = _read_artifact(catalog_file, MAX_CATALOG_BYTES, "catalog")
    manifest_bytes = _read_artifact(manifest_file, MAX_MANIFEST_BYTES, "catalog manifest")
    manifest = _require_mapping(_load_json(manifest_bytes, "catalog manifest"), "catalog manifest")
    expected_manifest_fields = {
        "schema_version",
        "catalog_sha256",
        "catalog_bytes",
        "catalog_gzip_bytes",
        "record_count",
        "source_fragment_tree_sha256",
        "basis",
    }
    if set(manifest) != expected_manifest_fields or manifest.get(
        "schema_version"
    ) != MANIFEST_SCHEMA_VERSION:
        raise PagefindCatalogError("catalog manifest fields or schema are invalid")
    digest = hashlib.sha256(catalog_bytes).hexdigest()
    if manifest.get("catalog_sha256") != digest:
        raise PagefindCatalogError("catalog digest does not match its manifest")
    if manifest.get("catalog_bytes") != len(catalog_bytes):
        raise PagefindCatalogError("catalog byte count does not match its manifest")
    gzip_bytes = len(
        gzip.compress(catalog_bytes, compresslevel=CATALOG_GZIP_LEVEL, mtime=0)
    )
    if gzip_bytes > MAX_CATALOG_GZIP_BYTES or manifest.get("catalog_gzip_bytes") != gzip_bytes:
        raise PagefindCatalogError("catalog gzip size does not match its manifest")

    catalog = _require_mapping(_load_json(catalog_bytes, "catalog"), "catalog")
    expected_catalog_fields = {
        "schema_version",
        "summary_codepoints",
        "source_fragment_tree_sha256",
        "basis",
        "record_count",
        "records",
    }
    if set(catalog) != expected_catalog_fields or catalog.get(
        "schema_version"
    ) != CATALOG_SCHEMA_VERSION:
        raise PagefindCatalogError("catalog fields or schema are invalid")
    if catalog.get("summary_codepoints") != SUMMARY_CODEPOINTS:
        raise PagefindCatalogError("catalog summary policy is invalid")
    tree_digest = _require_sha256(
        catalog.get("source_fragment_tree_sha256"), "source_fragment_tree_sha256"
    )
    if manifest.get("source_fragment_tree_sha256") != tree_digest:
        raise PagefindCatalogError("catalog fragment tree digest does not match its manifest")
    basis_mapping = _require_mapping(catalog.get("basis"), "catalog basis")
    manifest_basis = _require_mapping(manifest.get("basis"), "catalog manifest basis")
    basis = CatalogBasis.from_mapping(basis_mapping)
    if manifest_basis != basis.to_dict():
        raise PagefindCatalogError("catalog basis does not match its manifest")
    records = _require_mapping(catalog.get("records"), "catalog records")
    record_count = catalog.get("record_count")
    if (
        not isinstance(record_count, int)
        or isinstance(record_count, bool)
        or record_count <= 0
        or record_count > MAX_FRAGMENT_COUNT
        or record_count != len(records)
        or manifest.get("record_count") != record_count
    ):
        raise PagefindCatalogError("catalog record count is invalid")
    for fragment_id, record in records.items():
        _validate_catalog_record(fragment_id, record)
    return CatalogBuildReport(
        record_count=record_count,
        source_fragment_tree_sha256=tree_digest,
        catalog_sha256=digest,
        catalog_bytes=len(catalog_bytes),
        catalog_gzip_bytes=gzip_bytes,
        code_sha=basis.code_sha,
        content_sha=basis.content_sha,
        basis_schema_version=basis.basis_schema_version,
        release_basis_sha256=basis.release_basis_sha256,
    )


def _remove_fragment_directory(pagefind_root: Path, fragment_root: Path) -> None:
    quarantine = pagefind_root / f".fragment-removal-{uuid.uuid4().hex}"
    try:
        os.replace(fragment_root, quarantine)
        shutil.rmtree(quarantine)
    except OSError as exc:
        if quarantine.exists() and not fragment_root.exists():
            try:
                os.replace(quarantine, fragment_root)
            except OSError:
                pass
        raise PagefindCatalogError("validated fragments could not be removed") from exc


def convert_pagefind_fragments(
    public_root: Path | str,
    *,
    release_basis_path: Path | str | None = None,
    code_sha: str | None = None,
    content_sha: str | None = None,
) -> CatalogBuildReport:
    """Create and verify a compact catalog before removing Pagefind fragments."""

    public = Path(public_root)
    _require_directory(public, "public root")
    pagefind_root = public / "pagefind"
    fragment_root = pagefind_root / "fragment"
    selected_basis = Path(release_basis_path) if release_basis_path is not None else None
    basis = _resolve_basis(
        release_basis_path=selected_basis,
        code_sha=code_sha,
        content_sha=content_sha,
    )
    records, snapshots, tree_digest = _collect_fragments(pagefind_root, fragment_root)
    catalog_payload = make_catalog_payload(
        records,
        basis=basis,
        source_fragment_tree_sha256=tree_digest,
    )
    catalog_bytes = _canonical_json(catalog_payload)
    if len(catalog_bytes) > MAX_CATALOG_BYTES:
        raise PagefindCatalogError("catalog size exceeds the safety limit")
    catalog_gzip_bytes = len(
        gzip.compress(catalog_bytes, compresslevel=CATALOG_GZIP_LEVEL, mtime=0)
    )
    if catalog_gzip_bytes > MAX_CATALOG_GZIP_BYTES:
        raise PagefindCatalogError("catalog gzip size exceeds the safety limit")
    catalog_digest = hashlib.sha256(catalog_bytes).hexdigest()
    manifest_bytes = _canonical_json(
        {
            "schema_version": MANIFEST_SCHEMA_VERSION,
            "catalog_sha256": catalog_digest,
            "catalog_bytes": len(catalog_bytes),
            "catalog_gzip_bytes": catalog_gzip_bytes,
            "record_count": len(records),
            "source_fragment_tree_sha256": tree_digest,
            "basis": basis.to_dict(),
        }
    )
    catalog_path = pagefind_root / "catalog.json"
    manifest_path = pagefind_root / "catalog.manifest.json"
    _ensure_replaceable_output(catalog_path)
    _ensure_replaceable_output(manifest_path)
    _atomic_write(catalog_path, catalog_bytes)
    _atomic_write(manifest_path, manifest_bytes)
    report = verify_catalog_artifact(catalog_path, manifest_path)
    if report.catalog_sha256 != catalog_digest:
        raise PagefindCatalogError("written catalog failed its integrity check")
    _verify_fragment_snapshot(pagefind_root, fragment_root, snapshots)
    _remove_fragment_directory(pagefind_root, fragment_root)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-root", type=Path, required=True)
    parser.add_argument("--release-basis", type=Path)
    parser.add_argument("--code-sha")
    parser.add_argument("--content-sha")
    arguments = parser.parse_args(argv)
    report = convert_pagefind_fragments(
        arguments.public_root,
        release_basis_path=arguments.release_basis,
        code_sha=arguments.code_sha,
        content_sha=arguments.content_sha,
    )
    print(json.dumps(report.to_dict(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
