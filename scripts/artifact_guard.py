"""Fail-closed validation for artifacts crossing workflow trust boundaries.

The archive is inspected before extraction.  Only explicitly allowlisted,
regular, non-executable files with exact caller-provided digests are accepted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import hmac
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
from typing import Mapping


class ArtifactValidationError(ValueError):
    """Raised when an untrusted artifact violates any validation rule."""


@dataclass(frozen=True)
class ArtifactPolicy:
    allowed_roots: tuple[str, ...] = ("content", "state")
    allowed_suffixes: tuple[str, ...] = (".json", ".md", ".txt", ".yaml", ".yml")
    max_files: int = 2_000
    max_file_bytes: int = 2 * 1024 * 1024
    max_total_bytes: int = 64 * 1024 * 1024
    required_json_fields: Mapping[str, frozenset[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.allowed_roots or any(
            not root or "/" in root or "\\" in root or root in {".", ".."}
            for root in self.allowed_roots
        ):
            raise ValueError("allowed_roots must contain simple relative names")
        if not self.allowed_suffixes or any(
            not suffix.startswith(".") or suffix.casefold() == ".svg"
            for suffix in self.allowed_suffixes
        ):
            raise ValueError("allowed_suffixes must be safe file extensions")
        if min(self.max_files, self.max_file_bytes, self.max_total_bytes) <= 0:
            raise ValueError("artifact limits must be positive")


@dataclass(frozen=True)
class ArtifactReport:
    archive_sha256: str
    file_count: int
    total_bytes: int
    files: tuple[str, ...]


_SECRET_PATTERNS = (
    re.compile(rb"ghp_[A-Za-z0-9]{30,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{40,}"),
    re.compile(rb"AKIA[A-Z0-9]{16}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(
        rb"(?i)(?:anthropic|openai|minimax|telegram|twitter)[A-Z0-9_]*(?:api_)?"
        rb"(?:key|token)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}"
    ),
)

_IMAGE_MAGIC: Mapping[str, tuple[bytes, ...]] = {
    ".gif": (b"GIF87a", b"GIF89a"),
    ".jpg": (b"\xff\xd8\xff",),
    ".jpeg": (b"\xff\xd8\xff",),
    ".png": (b"\x89PNG\r\n\x1a\n",),
    ".webp": (b"RIFF",),
}


def _hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_member_path(raw_name: str, allowed_roots: tuple[str, ...]) -> PurePosixPath:
    if (
        not raw_name
        or raw_name.startswith("/")
        or "\\" in raw_name
        or "\x00" in raw_name
        or any(part in {"", ".", ".."} for part in raw_name.split("/"))
    ):
        raise ArtifactValidationError(f"unsafe path: {raw_name!r}")
    path = PurePosixPath(raw_name)
    if path.is_absolute():
        raise ArtifactValidationError(f"unsafe path: {raw_name!r}")
    if path.parts[0] not in allowed_roots:
        raise ArtifactValidationError(f"outside allowed roots: {raw_name}")
    return path


def _decode_text(name: str, payload: bytes) -> str:
    if b"\x00" in payload:
        raise ArtifactValidationError(f"invalid text MIME for {name}: NUL byte")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ArtifactValidationError(f"invalid text MIME for {name}: not UTF-8") from exc


def _validate_payload(
    name: str,
    suffix: str,
    payload: bytes,
    required_json_fields: Mapping[str, frozenset[str]],
) -> None:
    if any(pattern.search(payload) for pattern in _SECRET_PATTERNS):
        raise ArtifactValidationError(f"secret-like content in {name}")

    if suffix == ".json":
        text = _decode_text(name, payload)
        try:
            value = json.loads(text)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ArtifactValidationError(f"invalid JSON MIME for {name}") from exc
        for pattern, fields in required_json_fields.items():
            if PurePosixPath(name).match(pattern):
                if not isinstance(value, dict):
                    raise ArtifactValidationError(f"JSON object required for {name}")
                missing = sorted(fields.difference(value))
                if missing:
                    raise ArtifactValidationError(
                        f"missing required JSON fields in {name}: {', '.join(missing)}"
                    )
    elif suffix in {".md", ".txt", ".yaml", ".yml"}:
        _decode_text(name, payload)
    elif suffix in _IMAGE_MAGIC:
        signatures = _IMAGE_MAGIC[suffix]
        if not any(payload.startswith(signature) for signature in signatures):
            raise ArtifactValidationError(f"invalid image MIME for {name}")
        if suffix == ".webp" and payload[8:12] != b"WEBP":
            raise ArtifactValidationError(f"invalid image MIME for {name}")


def validate_tar_artifact(
    archive_path: Path | str,
    *,
    policy: ArtifactPolicy,
    expected_files: Mapping[str, str],
    expected_archive_sha256: str | None = None,
) -> ArtifactReport:
    """Validate an untrusted tar archive without extracting any member.

    ``expected_files`` is mandatory and must describe the exact path set and
    SHA-256 of every regular file.  This prevents a producer from smuggling an
    extra file even if it otherwise satisfies the allowlist.
    """

    archive = Path(archive_path)
    archive_digest = _hash_file(archive)
    if expected_archive_sha256 is not None and not hmac.compare_digest(
        archive_digest, expected_archive_sha256.casefold()
    ):
        raise ArtifactValidationError("archive digest mismatch")

    seen: dict[str, str] = {}
    total_bytes = 0
    file_count = 0
    try:
        handle = tarfile.open(archive, mode="r:*")
    except (tarfile.TarError, OSError) as exc:
        raise ArtifactValidationError("invalid tar artifact") from exc

    with handle:
        for member in handle:
            member_path = _safe_member_path(member.name, policy.allowed_roots)
            if member.isdir():
                continue
            if not member.isreg():
                raise ArtifactValidationError(f"non-regular member: {member.name}")
            if member.name in seen:
                raise ArtifactValidationError(f"duplicate path: {member.name}")
            if member.mode & 0o111:
                raise ArtifactValidationError(f"executable file: {member.name}")

            suffix = member_path.suffix.casefold()
            if suffix not in policy.allowed_suffixes:
                raise ArtifactValidationError(f"disallowed suffix: {member.name}")

            file_count += 1
            if file_count > policy.max_files:
                raise ArtifactValidationError("too many files in artifact")
            if member.size < 0 or member.size > policy.max_file_bytes:
                raise ArtifactValidationError(f"file too large: {member.name}")
            total_bytes += member.size
            if total_bytes > policy.max_total_bytes:
                raise ArtifactValidationError("artifact too large")

            extracted = handle.extractfile(member)
            if extracted is None:
                raise ArtifactValidationError(f"unreadable member: {member.name}")
            payload = extracted.read(policy.max_file_bytes + 1)
            if len(payload) != member.size:
                raise ArtifactValidationError(f"member size mismatch: {member.name}")
            _validate_payload(member.name, suffix, payload, policy.required_json_fields)
            seen[member.name] = sha256(payload).hexdigest()

    expected_names = set(expected_files)
    if set(seen) != expected_names:
        missing = sorted(expected_names.difference(seen))
        extra = sorted(set(seen).difference(expected_names))
        raise ArtifactValidationError(
            f"manifest file set mismatch (missing={missing}, extra={extra})"
        )
    for name, actual_digest in seen.items():
        expected_digest = str(expected_files[name]).casefold()
        if not hmac.compare_digest(actual_digest, expected_digest):
            raise ArtifactValidationError(f"digest mismatch: {name}")

    return ArtifactReport(
        archive_sha256=archive_digest,
        file_count=file_count,
        total_bytes=total_bytes,
        files=tuple(sorted(seen)),
    )
