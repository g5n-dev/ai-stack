"""Immutable release identity and stale-deployment protection."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Mapping, Sequence


class ReleaseValidationError(ValueError):
    """Raised when a release manifest cannot be trusted."""


_GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SCHEMA_VERSION = re.compile(r"[1-9][0-9]*\.[0-9]+\Z")
_FIELDS = frozenset(
    {
        "release_id",
        "code_sha",
        "content_sha",
        "schema_version",
        "release_seq",
        "artifact_digest",
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

    def __post_init__(self) -> None:
        if not isinstance(self.code_sha, str) or not _GIT_SHA.fullmatch(self.code_sha):
            raise ReleaseValidationError("invalid code_sha")
        if not isinstance(self.content_sha, str) or not _GIT_SHA.fullmatch(self.content_sha):
            raise ReleaseValidationError("invalid content_sha")
        if not isinstance(self.artifact_digest, str) or not _SHA256.fullmatch(
            self.artifact_digest
        ):
            raise ReleaseValidationError("invalid artifact_digest")
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
        return (
            f"r{self.release_seq:012d}-{self.code_sha[:12]}-"
            f"{self.content_sha[:12]}-{self.artifact_digest[:12]}"
        )

    def to_dict(self) -> dict[str, str | int]:
        return {
            "release_id": self.release_id,
            "code_sha": self.code_sha,
            "content_sha": self.content_sha,
            "schema_version": self.schema_version,
            "release_seq": self.release_seq,
            "artifact_digest": self.artifact_digest,
            "generated_at": self.generated_at,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "ReleaseDescriptor":
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
        )
        claimed_release_id = value.get("release_id")
        if claimed_release_id is not None and claimed_release_id != descriptor.release_id:
            raise ReleaseValidationError("release_id mismatch")
        return descriptor


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


def write_release_descriptor(path: Path | str, descriptor: ReleaseDescriptor) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        descriptor.to_dict(),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
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
    validate = subparsers.add_parser("validate", help="reject forged or stale release metadata")
    validate.add_argument("--candidate", type=Path, required=True)
    validate.add_argument("--current", type=Path)
    validate.add_argument("--expected-code-sha")
    validate.add_argument("--expected-content-sha")
    validate.add_argument("--expected-artifact-digest")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
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
