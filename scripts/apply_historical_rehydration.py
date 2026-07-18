#!/usr/bin/env python3
"""Plan or explicitly apply authenticated historical source-recovery evidence."""

from __future__ import annotations

import argparse
import hmac
import json
import os
import re
import stat
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_stack._json import sha256_digest  # noqa: E402
from ai_stack.content_quality import content_quality_reasons  # noqa: E402
from ai_stack.historical_capture_job import (  # noqa: E402
    CAPTURE_AUDIT_SCHEMA,
    CAPTURE_AUDIT_VERSION,
    HistoricalCaptureJobError,
    load_capture_audit,
    load_historical_capture_inventory,
)
from ai_stack.historical_rehydration import (  # noqa: E402
    HISTORICAL_RECOVERY_FAILURE_TYPES,
    HISTORICAL_REHYDRATION_SCHEMA,
    HISTORICAL_REHYDRATION_VERSION,
)
from ai_stack.historical_rehydration_apply import (  # noqa: E402
    HistoricalRecoveryFailure,
    HistoricalRehydrationApplyError,
    HistoricalRehydrationApplyPlan,
    HistoricalRehydrationRollbackError,
    apply_historical_rehydration_plan,
    build_historical_rehydration_apply_plan,
)
from crawler.historical_source_fetch import HistoricalSourceCapture  # noqa: E402

SUMMARY_SCHEMA = "ai_stack.historical_rehydration.cli_summary"
SUMMARY_VERSION = 1

_CAPTURE_FIELDS = frozenset(
    {
        "source",
        "title",
        "external_url",
        "source_text",
        "captured_at",
        "capture_mode",
        "source_completeness",
        "source_is_truncated",
        "metadata",
    }
)
_RESULT_BASE_FIELDS = frozenset(
    {
        "path",
        "target_sha256",
        "source",
        "canonical_url",
        "source_locator",
        "attempt_count",
        "attempted_at",
        "status",
    }
)
_SAFE_FAILURE = re.compile(r"^[a-z][a-z0-9_]{1,127}$")
_MAX_CAPTURE_TEXT_CHARS = 12_000
_MAX_CAPTURE_METADATA_BYTES = 64 * 1024
_TERMINAL_CAPTURE_QUALITY_REASONS = frozenset({"encoding_replacement_character"})


class HistoricalRehydrationCLIError(ValueError):
    """Safe, typed rejection whose reason may be written to a terminal."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True, slots=True)
class HistoricalRehydrationOutcomes:
    inventory: dict[str, Any]
    captures: dict[str, HistoricalSourceCapture]
    failures: dict[str, HistoricalRecoveryFailure]
    captured_result_count: int
    failed_result_count: int
    excluded_failure_count: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--capture-audit", type=Path, required=True)
    parser.add_argument(
        "--content-root",
        type=Path,
        default=PROJECT_ROOT / "blog/content/posts",
    )
    parser.add_argument(
        "--archive-failures",
        action="store_true",
        help="include typed failed capture results as transparent terminal archives",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform the reviewed transaction; omitted means a zero-write plan",
    )
    parser.add_argument("--expected-head")
    parser.add_argument("--expected-plan-digest")
    parser.add_argument("--max-changes", type=int)
    parser.add_argument("--backup-id")
    parser.add_argument("--backup-root", type=Path)
    return parser


def _reject_symlink_components(path: Path, *, reason: str) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        if current.is_symlink():
            raise HistoricalRehydrationCLIError(reason)


def _same_input(left: Path, right: Path) -> bool:
    if left.absolute() == right.absolute():
        return True
    try:
        return os.path.samefile(left, right)
    except OSError:
        return False


def _require_private_capture_audit(path: Path) -> None:
    _reject_symlink_components(path, reason="input_rejected")
    try:
        details = path.lstat()
    except OSError as exc:
        raise HistoricalRehydrationCLIError("input_rejected") from exc
    if (
        not stat.S_ISREG(details.st_mode)
        or details.st_nlink != 1
        or stat.S_IMODE(details.st_mode) != 0o600
    ):
        raise HistoricalRehydrationCLIError("capture_audit_mode_invalid")


def _aware_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    normalized = f"{value[:-1]}+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _capture_from_payload(payload: object) -> HistoricalSourceCapture:
    if not isinstance(payload, Mapping) or set(payload) != _CAPTURE_FIELDS:
        raise HistoricalRehydrationCLIError("capture_payload_invalid")
    string_fields = (
        "source",
        "title",
        "external_url",
        "source_text",
        "captured_at",
        "capture_mode",
        "source_completeness",
    )
    if any(
        not isinstance(payload.get(field), str)
        or not str(payload.get(field)).strip()
        or payload.get(field) != str(payload.get(field)).strip()
        for field in string_fields
    ):
        raise HistoricalRehydrationCLIError("capture_payload_invalid")
    title = str(payload["title"])
    source_text = str(payload["source_text"])
    metadata = payload.get("metadata")
    if (
        len(title) > 500
        or len(source_text) > _MAX_CAPTURE_TEXT_CHARS
        or type(payload.get("source_is_truncated")) is not bool
        or not _aware_timestamp(payload.get("captured_at"))
        or not isinstance(metadata, Mapping)
        or any(not isinstance(key, str) for key in metadata)
    ):
        raise HistoricalRehydrationCLIError("capture_payload_invalid")
    try:
        canonical_metadata = json.loads(
            json.dumps(
                dict(metadata),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        )
        metadata_size = len(
            json.dumps(
                canonical_metadata,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        )
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise HistoricalRehydrationCLIError("capture_payload_invalid") from exc
    if metadata_size > _MAX_CAPTURE_METADATA_BYTES or not isinstance(canonical_metadata, dict):
        raise HistoricalRehydrationCLIError("capture_payload_invalid")
    return HistoricalSourceCapture(
        source=str(payload["source"]),
        title=title,
        external_url=str(payload["external_url"]),
        source_text=source_text,
        captured_at=str(payload["captured_at"]),
        capture_mode=str(payload["capture_mode"]),
        source_completeness=str(payload["source_completeness"]),
        source_is_truncated=bool(payload["source_is_truncated"]),
        metadata=canonical_metadata,
    )


def _mapped_failure(result: Mapping[str, Any]) -> HistoricalRecoveryFailure:
    payload = result.get("failure")
    if not isinstance(payload, Mapping) or set(payload) != {"type", "reason"}:
        raise HistoricalRehydrationCLIError("failure_payload_invalid")
    raw_type = payload.get("type")
    reason = payload.get("reason")
    attempted_at = result.get("attempted_at")
    if not all(isinstance(value, str) for value in (raw_type, reason, attempted_at)):
        raise HistoricalRehydrationCLIError("failure_payload_invalid")
    failure_type = "source_fetch_error" if str(raw_type).startswith("robots_") else str(raw_type)
    if (
        failure_type not in HISTORICAL_RECOVERY_FAILURE_TYPES
        or _SAFE_FAILURE.fullmatch(str(reason)) is None
        or not _aware_timestamp(attempted_at)
    ):
        raise HistoricalRehydrationCLIError("failure_payload_invalid")
    return HistoricalRecoveryFailure(
        failure_type=failure_type,
        reason=str(reason),
        # This must be the result timestamp, never the audit generation time.
        attempted_at=str(attempted_at),
    )


def _validated_audit_counts(audit: Mapping[str, Any], results: list[Any]) -> tuple[int, int]:
    captured = sum(
        isinstance(result, Mapping) and result.get("status") == "captured" for result in results
    )
    failed = sum(
        isinstance(result, Mapping) and result.get("status") == "failed" for result in results
    )
    if (
        type(audit.get("captured_count")) is not int
        or type(audit.get("failed_count")) is not int
        or audit.get("captured_count") != captured
        or audit.get("failed_count") != failed
        or captured + failed != len(results)
    ):
        raise HistoricalRehydrationCLIError("capture_audit_counts_invalid")
    return captured, failed


def load_historical_rehydration_outcomes(
    inventory_path: str | Path,
    capture_audit_path: str | Path,
    *,
    archive_failures: bool,
) -> HistoricalRehydrationOutcomes:
    """Authenticate both artifacts and rebuild typed, path-keyed outcomes."""

    inventory_file = Path(inventory_path).absolute()
    audit_file = Path(capture_audit_path).absolute()
    if _same_input(inventory_file, audit_file):
        raise HistoricalRehydrationCLIError("input_paths_must_differ")
    _require_private_capture_audit(audit_file)
    inventory = load_historical_capture_inventory(inventory_file)
    audit = load_capture_audit(audit_file)
    if (
        audit.get("schema") != CAPTURE_AUDIT_SCHEMA
        or audit.get("version") != CAPTURE_AUDIT_VERSION
        or audit.get("inventory_schema") != HISTORICAL_REHYDRATION_SCHEMA
        or audit.get("inventory_version") != HISTORICAL_REHYDRATION_VERSION
    ):
        raise HistoricalRehydrationCLIError("capture_audit_contract_invalid")
    inventory_digest = inventory.get("entries_sha256")
    audit_inventory_digest = audit.get("inventory_entries_sha256")
    if not (
        isinstance(inventory_digest, str)
        and isinstance(audit_inventory_digest, str)
        and hmac.compare_digest(inventory_digest, audit_inventory_digest)
    ):
        raise HistoricalRehydrationCLIError("inventory_digest_mismatch")

    raw_entries = inventory.get("entries")
    raw_results = audit.get("results")
    if not isinstance(raw_entries, list) or not isinstance(raw_results, list):
        raise HistoricalRehydrationCLIError("capture_audit_contract_invalid")
    entries = {str(entry.get("path")): entry for entry in raw_entries if isinstance(entry, Mapping)}
    if len(entries) != len(raw_entries):
        raise HistoricalRehydrationCLIError("capture_audit_contract_invalid")
    captured_count, failed_count = _validated_audit_counts(audit, raw_results)
    captures: dict[str, HistoricalSourceCapture] = {}
    failures: dict[str, HistoricalRecoveryFailure] = {}
    included_failed_result_count = 0
    seen_paths: set[str] = set()
    for raw_result in raw_results:
        if not isinstance(raw_result, Mapping):
            raise HistoricalRehydrationCLIError("capture_result_invalid")
        result = {str(key): value for key, value in raw_result.items()}
        status_value = result.get("status")
        status = status_value if isinstance(status_value, str) else ""
        expected_fields = _RESULT_BASE_FIELDS.union(
            {"capture"} if status == "captured" else {"failure"}
        )
        if set(result) != expected_fields or status not in {"captured", "failed"}:
            raise HistoricalRehydrationCLIError("capture_result_invalid")
        path_value = result.get("path")
        path = path_value if isinstance(path_value, str) else ""
        if not path or path in seen_paths or path not in entries:
            raise HistoricalRehydrationCLIError("capture_result_invalid")
        seen_paths.add(path)
        entry = entries[path]
        attempt_count = result.get("attempt_count")
        if (
            type(attempt_count) is not int
            or attempt_count < 1
            or not _aware_timestamp(result.get("attempted_at"))
        ):
            raise HistoricalRehydrationCLIError("capture_result_invalid")
        for field in (
            "target_sha256",
            "source",
            "canonical_url",
            "source_locator",
        ):
            if result.get(field) != entry.get(field):
                raise HistoricalRehydrationCLIError("capture_result_inventory_mismatch")
        if status == "captured":
            capture = _capture_from_payload(result.get("capture"))
            if capture.source != result.get("source"):
                raise HistoricalRehydrationCLIError("capture_result_inventory_mismatch")
            terminal_reasons = sorted(
                _TERMINAL_CAPTURE_QUALITY_REASONS.intersection(
                    content_quality_reasons(capture.source_text)
                )
            )
            if terminal_reasons:
                if not archive_failures:
                    raise HistoricalRehydrationCLIError("capture_payload_invalid")
                failures[path] = HistoricalRecoveryFailure(
                    failure_type="capture_validation_error",
                    reason=f"capture_{terminal_reasons[0]}",
                    attempted_at=str(result["attempted_at"]),
                )
                continue
            captures[path] = capture
        elif archive_failures:
            failures[path] = _mapped_failure(result)
            included_failed_result_count += 1
    return HistoricalRehydrationOutcomes(
        inventory=inventory,
        captures=captures,
        failures=failures,
        captured_result_count=captured_count,
        failed_result_count=failed_count,
        excluded_failure_count=failed_count - included_failed_result_count,
    )


def _summary(
    outcomes: HistoricalRehydrationOutcomes,
    plan: HistoricalRehydrationApplyPlan | None,
    *,
    archive_failures: bool,
    receipt: Mapping[str, Any] | None,
) -> dict[str, Any]:
    manifest = plan.manifest if plan is not None else {}
    return {
        "schema": SUMMARY_SCHEMA,
        "version": SUMMARY_VERSION,
        "dry_run": receipt is None,
        "apply_performed": receipt is not None,
        "archive_failures": archive_failures,
        "captured_result_count": outcomes.captured_result_count,
        "failed_result_count": outcomes.failed_result_count,
        "excluded_failure_count": outcomes.excluded_failure_count,
        "planned_changes": manifest.get("planned_changes", 0),
        "outcome_counts": manifest.get("outcome_counts", {}),
        "plan_digest": manifest.get("plan_digest"),
        "inventory_entries_sha256": outcomes.inventory.get("entries_sha256"),
        "applied_count": receipt.get("applied_count", 0) if receipt is not None else 0,
        "receipt_sha256": sha256_digest(receipt) if receipt is not None else None,
    }


def _apply_arguments_present(args: argparse.Namespace) -> bool:
    return any(
        value is not None
        for value in (
            args.expected_head,
            args.expected_plan_digest,
            args.max_changes,
            args.backup_id,
            args.backup_root,
        )
    )


def _validate_apply_boundary(args: argparse.Namespace) -> None:
    provided = (
        args.expected_head,
        args.expected_plan_digest,
        args.max_changes,
        args.backup_id,
        args.backup_root,
    )
    if args.apply and any(value is None for value in provided):
        raise HistoricalRehydrationCLIError("apply_guards_incomplete")
    if not args.apply and _apply_arguments_present(args):
        raise HistoricalRehydrationCLIError("apply_flag_required")
    if args.apply:
        assert args.backup_root is not None
        _reject_symlink_components(args.backup_root, reason="backup_path_rejected")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        _validate_apply_boundary(args)
        outcomes = load_historical_rehydration_outcomes(
            args.inventory,
            args.capture_audit,
            archive_failures=args.archive_failures,
        )
        plan: HistoricalRehydrationApplyPlan | None = None
        if outcomes.captures or outcomes.failures:
            plan = build_historical_rehydration_apply_plan(
                outcomes.inventory,
                outcomes.captures,
                failures=outcomes.failures,
                content_root=args.content_root,
            )
        if args.apply and plan is None:
            raise HistoricalRehydrationCLIError("no_selected_outcomes")
        receipt: Mapping[str, Any] | None = None
        if args.apply:
            assert plan is not None
            assert args.expected_head is not None
            assert args.expected_plan_digest is not None
            assert args.max_changes is not None
            assert args.backup_id is not None
            assert args.backup_root is not None
            receipt = apply_historical_rehydration_plan(
                plan,
                expected_head=args.expected_head,
                expected_plan_digest=args.expected_plan_digest,
                max_changes=args.max_changes,
                backup_id=args.backup_id,
                backup_root=args.backup_root,
            )
        summary = _summary(
            outcomes,
            plan,
            archive_failures=args.archive_failures,
            receipt=receipt,
        )
    except HistoricalRehydrationCLIError as exc:
        print(f"historical-rehydration-apply: rejected: {exc.reason}", file=sys.stderr)
        return 2
    except HistoricalRehydrationRollbackError:
        print("historical-rehydration-apply: rejected: rollback_failed", file=sys.stderr)
        return 3
    except (HistoricalCaptureJobError, HistoricalRehydrationApplyError):
        print("historical-rehydration-apply: rejected: input_or_plan_rejected", file=sys.stderr)
        return 2
    except (OSError, TypeError, ValueError):
        print("historical-rehydration-apply: rejected: operation_rejected", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
