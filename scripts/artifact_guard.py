"""Fail-closed validation for artifacts crossing workflow trust boundaries.

The archive is inspected before extraction.  Only explicitly allowlisted,
regular, non-executable files with exact caller-provided digests are accepted.
"""

from __future__ import annotations

import argparse
import hmac
import json
import os
import re
import shutil
import stat
import sys
import tarfile
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePosixPath


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

_ARTIFACT_SCHEMA_VERSION = "artifact_manifest_v1"
_MANIFEST_FIELDS = frozenset(
    {"schema_version", "profile", "archive_sha256", "file_count", "total_bytes", "files"}
)
_SAFE_SUFFIXES = (
    ".json",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".gif",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
)
_PROFILES: Mapping[str, ArtifactPolicy] = {
    "discovery": ArtifactPolicy(
        allowed_roots=("content", "state"),
        allowed_suffixes=_SAFE_SUFFIXES,
        required_json_fields={
            "content/events/*.json": frozenset({"schema_version", "event_id"}),
        },
    ),
    "generated": ArtifactPolicy(
        allowed_roots=("content", "state"),
        allowed_suffixes=_SAFE_SUFFIXES,
    ),
    "validated": ArtifactPolicy(
        allowed_roots=("content", "state"),
        allowed_suffixes=_SAFE_SUFFIXES,
    ),
    "release": ArtifactPolicy(
        allowed_roots=("content", "state"),
        allowed_suffixes=_SAFE_SUFFIXES,
    ),
    "receipt": ArtifactPolicy(
        allowed_roots=("ops", "state"),
        allowed_suffixes=(".json", ".txt"),
    ),
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


def _profile_policy(profile: str) -> ArtifactPolicy:
    try:
        return _PROFILES[profile]
    except KeyError as exc:
        raise ArtifactValidationError(f"unknown artifact profile: {profile}") from exc


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
            temporary_name = temporary.name
            os.chmod(temporary.name, 0o600)
            temporary.write(payload)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)


def package_tar_artifact(
    root: Path | str,
    *,
    archive_path: Path | str,
    manifest_path: Path | str,
    profile: str,
) -> ArtifactReport:
    policy = _profile_policy(profile)
    source = Path(root)
    archive = Path(archive_path)
    manifest = Path(manifest_path)
    if source.is_symlink() or not source.is_dir():
        raise ArtifactValidationError("artifact root must be a regular directory")
    if _is_within(archive, source) or _is_within(manifest, source):
        raise ArtifactValidationError("archive outputs must be outside artifact root")

    files: list[tuple[str, bytes]] = []
    total_bytes = 0
    for candidate in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
        if candidate.is_symlink():
            raise ArtifactValidationError(f"artifact root contains symlink: {candidate}")
        if candidate.is_dir():
            continue
        details = candidate.lstat()
        if not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
            raise ArtifactValidationError(f"artifact root contains non-regular file: {candidate}")
        relative = candidate.relative_to(source).as_posix()
        member = _safe_member_path(relative, policy.allowed_roots)
        if member.suffix.casefold() not in policy.allowed_suffixes:
            raise ArtifactValidationError(f"disallowed suffix: {relative}")
        if details.st_mode & 0o111:
            raise ArtifactValidationError(f"executable file: {relative}")
        if details.st_size > policy.max_file_bytes:
            raise ArtifactValidationError(f"file too large: {relative}")
        payload = candidate.read_bytes()
        if len(payload) != details.st_size:
            raise ArtifactValidationError(f"file changed while packaging: {relative}")
        _validate_payload(relative, member.suffix.casefold(), payload, policy.required_json_fields)
        files.append((relative, payload))
        total_bytes += len(payload)
        if len(files) > policy.max_files:
            raise ArtifactValidationError("too many files in artifact")
        if total_bytes > policy.max_total_bytes:
            raise ArtifactValidationError("artifact too large")

    archive.parent.mkdir(parents=True, exist_ok=True)
    temporary_archive: str | None = None
    try:
        descriptor, temporary_archive = tempfile.mkstemp(
            prefix=f".{archive.name}.",
            dir=archive.parent,
        )
        os.close(descriptor)
        with tarfile.open(temporary_archive, mode="w", format=tarfile.PAX_FORMAT) as output:
            for relative, payload in files:
                info = tarfile.TarInfo(relative)
                info.size = len(payload)
                info.mode = 0o644
                info.mtime = 0
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                output.addfile(info, BytesIO(payload))
        os.chmod(temporary_archive, 0o600)
        os.replace(temporary_archive, archive)
        temporary_archive = None
    finally:
        if temporary_archive is not None:
            Path(temporary_archive).unlink(missing_ok=True)

    archive_digest = _hash_file(archive)
    file_manifest = {
        relative: {"bytes": len(payload), "sha256": sha256(payload).hexdigest()}
        for relative, payload in files
    }
    manifest_payload = {
        "schema_version": _ARTIFACT_SCHEMA_VERSION,
        "profile": profile,
        "archive_sha256": archive_digest,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "files": file_manifest,
    }
    _atomic_bytes(
        manifest,
        (json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n").encode(),
    )
    return ArtifactReport(archive_digest, len(files), total_bytes, tuple(file_manifest))


def _load_manifest(path: Path, profile: str) -> tuple[str, dict[str, str]]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 1024 * 1024:
        raise ArtifactValidationError("artifact manifest must be a small regular file")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ArtifactValidationError("invalid artifact manifest JSON") from exc
    if not isinstance(value, dict) or set(value) != _MANIFEST_FIELDS:
        raise ArtifactValidationError("artifact manifest fields do not match schema")
    if value["schema_version"] != _ARTIFACT_SCHEMA_VERSION or value["profile"] != profile:
        raise ArtifactValidationError("artifact manifest schema or profile mismatch")
    archive_digest = value["archive_sha256"]
    if not isinstance(archive_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", archive_digest):
        raise ArtifactValidationError("invalid archive digest in manifest")
    raw_files = value["files"]
    if not isinstance(raw_files, dict):
        raise ArtifactValidationError("artifact manifest files must be an object")
    expected: dict[str, str] = {}
    total_bytes = 0
    for name, details in raw_files.items():
        if not isinstance(name, str) or not isinstance(details, dict):
            raise ArtifactValidationError("invalid artifact manifest file record")
        if set(details) != {"bytes", "sha256"}:
            raise ArtifactValidationError("invalid artifact manifest file fields")
        size = details["bytes"]
        digest = details["sha256"]
        if (
            not isinstance(size, int)
            or isinstance(size, bool)
            or size < 0
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
        ):
            raise ArtifactValidationError("invalid artifact manifest size or digest")
        expected[name] = digest
        total_bytes += size
    if value["file_count"] != len(expected) or value["total_bytes"] != total_bytes:
        raise ArtifactValidationError("artifact manifest totals mismatch")
    return archive_digest, expected


def _reject_symlink_components(path: Path) -> None:
    current = Path(path.absolute().anchor)
    for component in path.absolute().parts[1:]:
        current /= component
        if current.is_symlink():
            raise ArtifactValidationError(f"symlink extraction path: {current}")


def _extract_validated(
    archive: Path,
    destination: Path,
    expected_files: Mapping[str, str],
    policy: ArtifactPolicy,
) -> None:
    if destination.exists() or destination.is_symlink():
        raise ArtifactValidationError("extraction destination must not already exist")
    _reject_symlink_components(destination.parent)
    destination.mkdir(parents=True, mode=0o700)
    try:
        with tarfile.open(archive, mode="r:*") as source:
            for member in source:
                if member.isdir():
                    continue
                member_path = _safe_member_path(member.name, policy.allowed_roots)
                if not member.isreg() or member.name not in expected_files:
                    raise ArtifactValidationError(f"unexpected extraction member: {member.name}")
                target = destination.joinpath(*member_path.parts)
                target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                _reject_symlink_components(target.parent)
                stream = source.extractfile(member)
                if stream is None:
                    raise ArtifactValidationError(f"unreadable extraction member: {member.name}")
                payload = stream.read(policy.max_file_bytes + 1)
                if sha256(payload).hexdigest() != expected_files[member.name]:
                    raise ArtifactValidationError(f"extraction digest mismatch: {member.name}")
                descriptor = os.open(
                    target,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                )
                with os.fdopen(descriptor, "wb") as output:
                    output.write(payload)
                    output.flush()
                    os.fsync(output.fileno())
                target.chmod(0o644)
    except BaseException:
        shutil.rmtree(destination, ignore_errors=True)
        raise


def validate_packaged_artifact(
    *,
    archive_path: Path | str,
    manifest_path: Path | str,
    profile: str,
    extract_to: Path | str | None = None,
) -> ArtifactReport:
    archive = Path(archive_path)
    if archive.is_symlink() or not archive.is_file():
        raise ArtifactValidationError("artifact archive must be a regular file")
    policy = _profile_policy(profile)
    archive_digest, expected_files = _load_manifest(Path(manifest_path), profile)
    report = validate_tar_artifact(
        archive,
        policy=policy,
        expected_archive_sha256=archive_digest,
        expected_files=expected_files,
    )
    if extract_to is not None:
        _extract_validated(archive, Path(extract_to), expected_files, policy)
        if _hash_file(archive) != archive_digest:
            shutil.rmtree(Path(extract_to), ignore_errors=True)
            raise ArtifactValidationError("archive changed during extraction")
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    pack = commands.add_parser("pack")
    pack.add_argument("--profile", choices=sorted(_PROFILES), required=True)
    pack.add_argument("--root", type=Path, required=True)
    pack.add_argument("--archive", type=Path, required=True)
    pack.add_argument("--manifest", type=Path, required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--profile", choices=sorted(_PROFILES), required=True)
    validate.add_argument("--archive", type=Path, required=True)
    validate.add_argument("--manifest", type=Path, required=True)
    validate.add_argument("--extract-to", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "pack":
            report = package_tar_artifact(
                args.root,
                archive_path=args.archive,
                manifest_path=args.manifest,
                profile=args.profile,
            )
        else:
            report = validate_packaged_artifact(
                archive_path=args.archive,
                manifest_path=args.manifest,
                profile=args.profile,
                extract_to=args.extract_to,
            )
    except (OSError, tarfile.TarError, ArtifactValidationError) as exc:
        print(f"artifact-guard: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "archive_sha256": report.archive_sha256,
                "file_count": report.file_count,
                "files": report.files,
                "total_bytes": report.total_bytes,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
