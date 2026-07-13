"""Append-only, content-addressed evidence for shadow migration gates.

The filesystem chain is an integrity layer inside the ``ops`` branch. Git CAS
still supplies the cross-machine serialization and durable trust anchor.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import stat
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from ._json import canonical_json_bytes

EVIDENCE_SCHEMA = "shadow_migration_evidence_v1"
GATE_SCHEMA = "shadow_migration_gate_v1"
REPORT_SCHEMA = "shadow_compare_v1"
MIN_CONSECUTIVE_RUNS = 24
MIN_FULL_BUILDS = 3
MIN_SOAK = timedelta(days=7)

_GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_DIGEST = re.compile(r"sha256:([0-9a-f]{64})\Z")
_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_REPORT_FILE = re.compile(r"([0-9a-f]{64})\.json\Z")
_RECORD_FILE = re.compile(r"([0-9]{20})-([0-9a-f]{64})\.json\Z")
_MAX_EVIDENCE_FILE_BYTES = 16 * 1024 * 1024
_MAX_RECORDS = 100_000


class ShadowEvidenceError(RuntimeError):
    """Raised when shadow evidence is incomplete, unsafe, or tampered with."""


@dataclass(frozen=True, slots=True)
class ShadowEvidenceRecord:
    sequence: int
    run_id: str
    completed_at: datetime
    status: str
    full_build: bool
    code_sha: str
    content_sha: str
    report_digest: str
    previous_evidence_digest: str | None
    record_digest: str


@dataclass(frozen=True, slots=True)
class ShadowGateResult:
    ready: bool
    consecutive_successful_runs: int
    full_build_count: int
    soak_seconds: int
    head_digest: str | None
    latest_run_id: str | None
    latest_code_sha: str | None
    latest_content_sha: str | None
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": GATE_SCHEMA,
            "ready": self.ready,
            "requirements": {
                "consecutive_successful_runs": MIN_CONSECUTIVE_RUNS,
                "full_shadow_builds": MIN_FULL_BUILDS,
                "soak_seconds": int(MIN_SOAK.total_seconds()),
            },
            "observed": {
                "consecutive_successful_runs": self.consecutive_successful_runs,
                "full_shadow_builds": self.full_build_count,
                "soak_seconds": self.soak_seconds,
                "head_digest": self.head_digest,
                "latest_run_id": self.latest_run_id,
                "latest_code_sha": self.latest_code_sha,
                "latest_content_sha": self.latest_content_sha,
            },
            "reasons": list(self.reasons),
        }


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ShadowEvidenceError(f"{field} must include a timezone")
    return value.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return _utc(value, "timestamp").isoformat().replace("+00:00", "Z")


def _parse_time(value: object, field: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ShadowEvidenceError(f"{field} must be a canonical UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ShadowEvidenceError(f"{field} is invalid") from exc
    parsed = _utc(parsed, field)
    if _format_time(parsed) != value:
        raise ShadowEvidenceError(f"{field} must be canonical")
    return parsed


def _payload_bytes(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _check_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            raise ShadowEvidenceError(f"shadow evidence crosses a symlink: {current}")


def _regular_directory(path: Path, *, create: bool = False) -> None:
    _check_components(path)
    if create:
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
        _check_components(path)
    try:
        details = path.lstat()
    except OSError as exc:
        raise ShadowEvidenceError(f"shadow evidence directory is missing: {path}") from exc
    if path.is_symlink() or not stat.S_ISDIR(details.st_mode):
        raise ShadowEvidenceError(f"shadow evidence path is not a regular directory: {path}")


def _read_canonical_object(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        details = path.lstat()
    except OSError as exc:
        raise ShadowEvidenceError(f"shadow evidence file is unreadable: {path}") from exc
    if path.is_symlink() or not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
        raise ShadowEvidenceError(f"shadow evidence file is unsafe: {path}")
    if details.st_size > _MAX_EVIDENCE_FILE_BYTES:
        raise ShadowEvidenceError(f"shadow evidence file exceeds size limit: {path}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
            raise ShadowEvidenceError(f"shadow evidence file is unsafe: {path}")
        if opened.st_size > _MAX_EVIDENCE_FILE_BYTES:
            raise ShadowEvidenceError(f"shadow evidence file exceeds size limit: {path}")
        with os.fdopen(descriptor, "rb") as stream:
            data = stream.read()
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise
    if len(data) != opened.st_size:
        raise ShadowEvidenceError(f"shadow evidence changed while reading: {path}")
    try:
        value = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ShadowEvidenceError(f"shadow evidence is not canonical JSON: {path}") from exc
    if not isinstance(value, dict) or _payload_bytes(value) != data:
        raise ShadowEvidenceError(f"shadow evidence is not canonical JSON: {path}")
    return value, data


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _create_once(path: Path, data: bytes) -> None:
    if path.exists() or path.is_symlink():
        value, existing = _read_canonical_object(path)
        del value
        if existing != data:
            raise ShadowEvidenceError(f"content-addressed object collision: {path.name}")
        return
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        _fsync_directory(path.parent)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise


@contextmanager
def _locked(root: Path) -> Iterator[None]:
    lock = root / ".lock"
    if lock.is_symlink():
        raise ShadowEvidenceError("shadow evidence lock must not be a symlink")
    descriptor = os.open(
        lock,
        os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _require_sha(value: object, field: str) -> str:
    if not isinstance(value, str) or not _GIT_SHA.fullmatch(value):
        raise ShadowEvidenceError(f"{field} must be a lowercase full Git object ID")
    return value


def _require_digest(value: object, field: str) -> str:
    if not isinstance(value, str) or not _DIGEST.fullmatch(value):
        raise ShadowEvidenceError(f"{field} must be a SHA-256 digest")
    return value


def _require_nonnegative_int(value: object, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ShadowEvidenceError(f"{field} must be a non-negative integer")
    return value


def _validate_report(
    report: Mapping[str, Any],
    *,
    code_sha: str,
    content_sha: str,
) -> bool:
    if report.get("schema_version") != REPORT_SCHEMA:
        raise ShadowEvidenceError("shadow report schema is invalid")
    matches = report.get("matches")
    if not isinstance(matches, bool):
        raise ShadowEvidenceError("shadow report matches status is invalid")
    if report.get("code_sha") != code_sha:
        raise ShadowEvidenceError("shadow report code_sha does not match the evidence")
    if report.get("content_sha") != content_sha:
        raise ShadowEvidenceError("shadow report content_sha does not match the evidence")
    _require_sha(report.get("code_sha"), "report code_sha")
    _require_sha(report.get("content_sha"), "report content_sha")

    baseline_tree = _require_digest(
        "sha256:" + str(report.get("baseline_tree_sha256", "")),
        "baseline tree digest",
    )
    candidate_tree = _require_digest(
        "sha256:" + str(report.get("candidate_tree_sha256", "")),
        "candidate tree digest",
    )
    baseline_files = _require_nonnegative_int(
        report.get("baseline_file_count"), "baseline_file_count"
    )
    candidate_files = _require_nonnegative_int(
        report.get("candidate_file_count"), "candidate_file_count"
    )
    baseline_html = _require_nonnegative_int(
        report.get("baseline_html_count"), "baseline_html_count"
    )
    candidate_html = _require_nonnegative_int(
        report.get("candidate_html_count"), "candidate_html_count"
    )
    difference_counts = tuple(
        _require_nonnegative_int(report.get(field), field)
        for field in ("missing_path_count", "extra_path_count", "changed_path_count")
    )
    difference_lists = tuple(
        report.get(field) for field in ("missing_paths", "extra_paths", "changed_paths")
    )
    if any(not isinstance(value, list) for value in difference_lists):
        raise ShadowEvidenceError("shadow report difference lists are invalid")
    if not isinstance(report.get("external_links_match"), bool):
        raise ShadowEvidenceError("shadow report external link status is invalid")
    if not isinstance(report.get("differences_truncated"), bool):
        raise ShadowEvidenceError("shadow report truncation status is invalid")

    if matches:
        file_count = _require_nonnegative_int(report.get("file_count"), "file_count")
        html_count = _require_nonnegative_int(report.get("html_count"), "html_count")
        link_sets = tuple(
            report.get(field)
            for field in (
                "external_links",
                "baseline_external_links",
                "candidate_external_links",
            )
        )
        if any(
            not isinstance(values, list)
            or any(not isinstance(value, str) for value in values)
            for values in link_sets
        ):
            raise ShadowEvidenceError("shadow report external link lists are invalid")
        valid_success = (
            baseline_tree == candidate_tree
            and baseline_files == candidate_files == file_count
            and baseline_html == candidate_html == html_count
            and report.get("external_links_match") is True
            and link_sets[0] == link_sets[1] == link_sets[2]
            and difference_counts == (0, 0, 0)
            and difference_lists == ([], [], [])
            and report.get("differences_truncated") is False
        )
        if not valid_success:
            raise ShadowEvidenceError("successful shadow report contradicts its comparison data")
    return matches


def _successful_report_is_nonempty(report: Mapping[str, Any]) -> bool:
    file_count = report.get("file_count")
    html_count = report.get("html_count")
    return (
        isinstance(file_count, int)
        and not isinstance(file_count, bool)
        and file_count > 0
        and isinstance(html_count, int)
        and not isinstance(html_count, bool)
        and html_count > 0
    )


def _load_reports(report_root: Path) -> dict[str, Mapping[str, Any]]:
    reports: dict[str, Mapping[str, Any]] = {}
    for path in sorted(report_root.iterdir(), key=lambda item: item.name):
        match = _REPORT_FILE.fullmatch(path.name)
        if match is None:
            raise ShadowEvidenceError(f"unexpected shadow report path: {path.name}")
        value, data = _read_canonical_object(path)
        digest = _digest(data)
        if match.group(1) != digest.removeprefix("sha256:"):
            raise ShadowEvidenceError(f"shadow report digest mismatch: {path.name}")
        reports[digest] = value
    return reports


def _load_records(root: Path, *, as_of: datetime) -> tuple[ShadowEvidenceRecord, ...]:
    report_root = root / "reports"
    record_root = root / "records"
    _regular_directory(report_root)
    _regular_directory(record_root)
    reports = _load_reports(report_root)
    paths = sorted(record_root.iterdir(), key=lambda item: item.name)
    if len(paths) > _MAX_RECORDS:
        raise ShadowEvidenceError("shadow evidence exceeds the record-count limit")

    records: list[ShadowEvidenceRecord] = []
    seen_run_ids: set[str] = set()
    previous_digest: str | None = None
    previous_completed_at: datetime | None = None
    for expected_sequence, path in enumerate(paths, start=1):
        match = _RECORD_FILE.fullmatch(path.name)
        if match is None:
            raise ShadowEvidenceError(f"unexpected shadow evidence path: {path.name}")
        filename_sequence = int(match.group(1))
        if filename_sequence != expected_sequence:
            raise ShadowEvidenceError(
                f"shadow evidence sequence is not continuous: expected {expected_sequence}"
            )
        value, data = _read_canonical_object(path)
        record_digest = _digest(data)
        if match.group(2) != record_digest.removeprefix("sha256:"):
            raise ShadowEvidenceError(f"shadow evidence digest mismatch: {path.name}")
        expected_fields = {
            "schema_version",
            "sequence",
            "run_id",
            "completed_at",
            "status",
            "full_build",
            "code_sha",
            "content_sha",
            "report_digest",
            "previous_evidence_digest",
        }
        if set(value) != expected_fields or value.get("schema_version") != EVIDENCE_SCHEMA:
            raise ShadowEvidenceError(f"shadow evidence schema is invalid: {path.name}")
        if value.get("sequence") != expected_sequence:
            raise ShadowEvidenceError(f"shadow evidence sequence payload is invalid: {path.name}")
        run_id = value.get("run_id")
        if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
            raise ShadowEvidenceError(f"shadow evidence run_id is invalid: {path.name}")
        if run_id in seen_run_ids:
            raise ShadowEvidenceError(f"duplicate run_id in shadow evidence: {run_id}")
        seen_run_ids.add(run_id)
        completed_at = _parse_time(value.get("completed_at"), "completed_at")
        if completed_at > as_of:
            raise ShadowEvidenceError(f"shadow evidence timestamp is in the future: {run_id}")
        if previous_completed_at is not None and completed_at <= previous_completed_at:
            raise ShadowEvidenceError("shadow evidence timestamps must be strictly increasing")
        code_sha = _require_sha(value.get("code_sha"), "code_sha")
        content_sha = _require_sha(value.get("content_sha"), "content_sha")
        report_digest = _require_digest(value.get("report_digest"), "report_digest")
        if report_digest not in reports:
            raise ShadowEvidenceError(f"shadow evidence report is missing: {report_digest}")
        if value.get("previous_evidence_digest") != previous_digest:
            raise ShadowEvidenceError("shadow evidence previous digest breaks the hash chain")
        status = value.get("status")
        if status not in {"SUCCEEDED", "FAILED"}:
            raise ShadowEvidenceError(f"shadow evidence status is invalid: {run_id}")
        full_build = value.get("full_build")
        if not isinstance(full_build, bool):
            raise ShadowEvidenceError(f"shadow evidence full_build flag is invalid: {run_id}")
        matches = _validate_report(
            reports[report_digest], code_sha=code_sha, content_sha=content_sha
        )
        expected_status = "SUCCEEDED" if matches else "FAILED"
        if status != expected_status:
            raise ShadowEvidenceError(f"shadow evidence status contradicts its report: {run_id}")
        if full_build and (
            status != "SUCCEEDED"
            or not _successful_report_is_nonempty(reports[report_digest])
        ):
            raise ShadowEvidenceError(
                "full build evidence requires a successful nonempty HTML tree"
            )
        records.append(
            ShadowEvidenceRecord(
                sequence=expected_sequence,
                run_id=run_id,
                completed_at=completed_at,
                status=status,
                full_build=full_build,
                code_sha=code_sha,
                content_sha=content_sha,
                report_digest=report_digest,
                previous_evidence_digest=previous_digest,
                record_digest=record_digest,
            )
        )
        previous_digest = record_digest
        previous_completed_at = completed_at
    return tuple(records)


def load_shadow_evidence(
    root: Path | str,
    *,
    as_of: datetime | None = None,
) -> tuple[ShadowEvidenceRecord, ...]:
    """Load and verify the complete content-addressed evidence chain."""

    evidence_root = Path(root).absolute()
    _regular_directory(evidence_root)
    checked_at = _utc(as_of or datetime.now(UTC), "as_of")
    return _load_records(evidence_root, as_of=checked_at)


def append_shadow_evidence(
    root: Path | str,
    *,
    report: Mapping[str, Any],
    run_id: str,
    completed_at: datetime,
    full_build: bool,
    code_sha: str,
    content_sha: str,
    expected_previous_digest: str | None,
    now: datetime | None = None,
) -> ShadowEvidenceRecord:
    """Append one immutable run record after validating its exact predecessor."""

    evidence_root = Path(root).absolute()
    _regular_directory(evidence_root, create=True)
    _regular_directory(evidence_root / "reports", create=True)
    _regular_directory(evidence_root / "records", create=True)
    checked_at = _utc(now or datetime.now(UTC), "now")
    completed = _utc(completed_at, "completed_at")
    if completed > checked_at:
        raise ShadowEvidenceError("shadow evidence timestamp is in the future")
    if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
        raise ShadowEvidenceError("run_id is invalid")
    code_sha = _require_sha(code_sha, "code_sha")
    content_sha = _require_sha(content_sha, "content_sha")
    if expected_previous_digest is not None:
        _require_digest(expected_previous_digest, "expected previous evidence digest")
    if not isinstance(full_build, bool):
        raise ShadowEvidenceError("full_build must be a boolean")

    with _locked(evidence_root):
        records = _load_records(evidence_root, as_of=checked_at)
        actual_previous = records[-1].record_digest if records else None
        if expected_previous_digest != actual_previous:
            raise ShadowEvidenceError(
                "expected previous evidence digest does not match the current head"
            )
        if any(record.run_id == run_id for record in records):
            raise ShadowEvidenceError(f"duplicate run_id in shadow evidence: {run_id}")
        if records and completed <= records[-1].completed_at:
            raise ShadowEvidenceError("completed_at must be strictly later than the prior run")

        matches = _validate_report(report, code_sha=code_sha, content_sha=content_sha)
        status = "SUCCEEDED" if matches else "FAILED"
        if full_build and (
            status != "SUCCEEDED"
            or not _successful_report_is_nonempty(report)
        ):
            raise ShadowEvidenceError(
                "full build evidence requires a successful nonempty HTML tree"
            )

        report_data = _payload_bytes(report)
        report_digest = _digest(report_data)
        report_path = evidence_root / "reports" / (report_digest.removeprefix("sha256:") + ".json")
        _create_once(report_path, report_data)

        sequence = len(records) + 1
        value: dict[str, Any] = {
            "schema_version": EVIDENCE_SCHEMA,
            "sequence": sequence,
            "run_id": run_id,
            "completed_at": _format_time(completed),
            "status": status,
            "full_build": full_build,
            "code_sha": code_sha,
            "content_sha": content_sha,
            "report_digest": report_digest,
            "previous_evidence_digest": actual_previous,
        }
        record_data = _payload_bytes(value)
        record_digest = _digest(record_data)
        record_path = (
            evidence_root
            / "records"
            / (f"{sequence:020d}-{record_digest.removeprefix('sha256:')}.json")
        )
        _create_once(record_path, record_data)
        return ShadowEvidenceRecord(
            sequence=sequence,
            run_id=run_id,
            completed_at=completed,
            status=status,
            full_build=full_build,
            code_sha=code_sha,
            content_sha=content_sha,
            report_digest=report_digest,
            previous_evidence_digest=actual_previous,
            record_digest=record_digest,
        )


def evaluate_shadow_gate(
    root: Path | str,
    *,
    as_of: datetime | None = None,
    expected_content_sha: str | None = None,
    expected_code_sha: str | None = None,
) -> ShadowGateResult:
    """Evaluate the latest uninterrupted success window against migration policy."""

    checked_at = _utc(as_of or datetime.now(UTC), "as_of")
    if expected_content_sha is not None:
        expected_content_sha = _require_sha(expected_content_sha, "expected_content_sha")
    if expected_code_sha is not None:
        expected_code_sha = _require_sha(expected_code_sha, "expected_code_sha")
    records = load_shadow_evidence(root, as_of=checked_at)
    streak: list[ShadowEvidenceRecord] = []
    for record in records:
        if record.status == "SUCCEEDED":
            streak.append(record)
        else:
            streak.clear()

    full_build_count = sum(record.full_build for record in streak)
    soak_seconds = (
        max(0, int((checked_at - streak[0].completed_at).total_seconds())) if streak else 0
    )
    latest = records[-1] if records else None
    reasons: list[str] = []
    if latest is not None and latest.status == "FAILED":
        reasons.append("latest_shadow_run_failed")
    if len(streak) < MIN_CONSECUTIVE_RUNS:
        reasons.append("requires_24_consecutive_successful_runs")
    if full_build_count < MIN_FULL_BUILDS:
        reasons.append("requires_3_full_shadow_builds")
    if soak_seconds < int(MIN_SOAK.total_seconds()):
        reasons.append("requires_7_day_soak")
    if expected_content_sha is not None and (
        latest is None or latest.content_sha != expected_content_sha
    ):
        reasons.append("current_content_sha_mismatch")
    if expected_code_sha is not None and (latest is None or latest.code_sha != expected_code_sha):
        reasons.append("current_code_sha_mismatch")
    return ShadowGateResult(
        ready=not reasons,
        consecutive_successful_runs=len(streak),
        full_build_count=full_build_count,
        soak_seconds=soak_seconds,
        head_digest=latest.record_digest if latest else None,
        latest_run_id=latest.run_id if latest else None,
        latest_code_sha=latest.code_sha if latest else None,
        latest_content_sha=latest.content_sha if latest else None,
        reasons=tuple(reasons),
    )


__all__ = [
    "EVIDENCE_SCHEMA",
    "GATE_SCHEMA",
    "MIN_CONSECUTIVE_RUNS",
    "MIN_FULL_BUILDS",
    "MIN_SOAK",
    "ShadowEvidenceError",
    "ShadowEvidenceRecord",
    "ShadowGateResult",
    "append_shadow_evidence",
    "evaluate_shadow_gate",
    "load_shadow_evidence",
]
