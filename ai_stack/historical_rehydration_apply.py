"""Safe planning and transactional application for historical source recovery.

Planning is the default and is strictly read-only.  A caller must separately
provide an exact Git HEAD, the reviewed plan digest, a bounded change count and
an external backup destination before any Markdown can be replaced.
"""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import yaml

from crawler.historical_source_fetch import HistoricalSourceCapture

from ._json import sha256_digest
from .content_quality import analyze_post, markdown_frontmatter
from .historical_publication import (
    HistoricalPublicationError,
    render_historical_tier_c_markdown,
)
from .historical_rehydration import (
    HISTORICAL_RECOVERY_FAILURE_TYPES,
    HISTORICAL_REHYDRATION_SCHEMA,
    HISTORICAL_REHYDRATION_VERSION,
)
from .identity import canonicalize_url

HISTORICAL_REHYDRATION_APPLY_PLAN_SCHEMA = "ai_stack.historical_rehydration.apply_plan"
HISTORICAL_REHYDRATION_APPLY_PLAN_VERSION = 1
HISTORICAL_REHYDRATION_APPLY_RECEIPT_SCHEMA = "ai_stack.historical_rehydration.apply_receipt"
HISTORICAL_REHYDRATION_APPLY_RECEIPT_VERSION = 1

_SUPPORTED_SOURCES = frozenset(
    {"arxiv", "blogs_podcasts", "github_trending", "hacker_news", "juejin"}
)
_SOURCE_LABELS = {
    "arxiv": "ArXiv",
    "blogs_podcasts": "博客与播客",
    "github_trending": "GitHub",
    "hacker_news": "Hacker News",
    "juejin": "掘金",
}
_MAX_INVENTORY_ENTRIES = 100_000
_MAX_MARKDOWN_BYTES = 2 * 1024 * 1024
_MAX_APPLY_CHANGES = 10_000
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_SHA256_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_GIT_HEAD = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_BACKUP_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_FAILURE_REASON = re.compile(r"^[a-z][a-z0-9_]{1,127}$")
_ARXIV_PATH = re.compile(r"^/(?:abs|pdf)/(?P<identifier>[^/?#]+?)(?:\.pdf)?/?$")
_JUEJIN_PATH = re.compile(r"^/post/(?P<identifier>[1-9]\d{5,24})/?$")
_UNSAFE_URL_CHARACTER = re.compile(r"[\s<>\"']")
_SENSITIVE_QUERY_KEY = re.compile(
    r"(?:^|[_-])(?:api[_-]?key|access[_-]?token|auth|authorization|credential|"
    r"password|secret|signature|signed|token)(?:$|[_-])",
    re.IGNORECASE,
)


class HistoricalRehydrationApplyError(ValueError):
    """Raised before an unsafe or stale recovery operation can mutate data."""


class HistoricalRehydrationRollbackError(RuntimeError):
    """Raised when a failed mutation cannot be restored from its backup."""


@dataclass(frozen=True, slots=True)
class HistoricalRecoveryFailure:
    """One explicit terminal outcome selected for transparent archival."""

    failure_type: str
    reason: str
    attempted_at: str


@dataclass(frozen=True, slots=True)
class PlannedHistoricalRehydrationWrite:
    """One compare-and-swap Markdown replacement relative to the posts root."""

    path: str
    source: str
    outcome: str
    input_sha256: str
    output_sha256: str
    source_identity_sha256: str
    outcome_sha256: str
    content: bytes


@dataclass(frozen=True, slots=True)
class HistoricalRehydrationApplyPlan:
    """A public digest-authenticated manifest plus private output bytes."""

    content_root: Path
    manifest: dict[str, Any]
    writes: tuple[PlannedHistoricalRehydrationWrite, ...]


@dataclass(frozen=True, slots=True)
class _RepositoryState:
    root: Path
    branch: str
    head: str
    status: str


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _same_digest(left: object, right: object) -> bool:
    return isinstance(left, str) and isinstance(right, str) and hmac.compare_digest(left, right)


def _safe_relative_markdown_path(value: object) -> str:
    if not isinstance(value, str):
        raise HistoricalRehydrationApplyError("inventory path is invalid")
    raw = value
    path = PurePosixPath(raw)
    if (
        not raw
        or raw != raw.strip()
        or "\\" in raw
        or path.is_absolute()
        or raw != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.suffix.casefold() != ".md"
    ):
        raise HistoricalRehydrationApplyError(f"inventory path is unsafe: {raw!r}")
    return raw


def _safe_content_root(value: str | Path) -> Path:
    root = Path(value).absolute()
    try:
        details = root.lstat()
    except OSError as exc:
        raise HistoricalRehydrationApplyError(f"content root is unavailable: {root}") from exc
    if root.is_symlink() or not stat.S_ISDIR(details.st_mode):
        raise HistoricalRehydrationApplyError(f"content root is unsafe: {root}")
    return root


def _validated_inventory_entries(
    inventory: Mapping[str, Any], *, content_root: Path
) -> tuple[dict[str, Any], ...]:
    if not isinstance(inventory, Mapping) or (
        inventory.get("schema") != HISTORICAL_REHYDRATION_SCHEMA
        or type(inventory.get("version")) is not int
        or inventory.get("version") != HISTORICAL_REHYDRATION_VERSION
        or inventory.get("offline") is not True
    ):
        raise HistoricalRehydrationApplyError("inventory contract is invalid")
    recorded_root = inventory.get("content_root")
    if not isinstance(recorded_root, str) or Path(recorded_root).absolute() != content_root:
        raise HistoricalRehydrationApplyError("inventory content root does not match")
    raw_entries = inventory.get("entries")
    if not isinstance(raw_entries, list) or len(raw_entries) > _MAX_INVENTORY_ENTRIES:
        raise HistoricalRehydrationApplyError("inventory entries are invalid")
    if type(inventory.get("entry_count")) is not int or inventory.get("entry_count") != len(
        raw_entries
    ):
        raise HistoricalRehydrationApplyError("inventory count does not match entries")
    try:
        calculated_digest = sha256_digest(raw_entries)
    except (TypeError, ValueError) as exc:
        raise HistoricalRehydrationApplyError("inventory entries are not canonical JSON") from exc
    if not _same_digest(inventory.get("entries_sha256"), calculated_digest):
        raise HistoricalRehydrationApplyError("inventory digest does not match entries")

    entries: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, Mapping):
            raise HistoricalRehydrationApplyError("inventory entry is invalid")
        if any(not isinstance(key, str) for key in raw_entry):
            raise HistoricalRehydrationApplyError("inventory entry keys are invalid")
        entry = {str(key): value for key, value in raw_entry.items()}
        path = _safe_relative_markdown_path(entry.get("path"))
        if path in seen_paths:
            raise HistoricalRehydrationApplyError(f"inventory path is duplicated: {path}")
        seen_paths.add(path)
        target_sha256 = entry.get("target_sha256")
        if not isinstance(target_sha256, str) or _SHA256_HEX.fullmatch(target_sha256) is None:
            raise HistoricalRehydrationApplyError(f"inventory target SHA is invalid: {path}")
        classification = entry.get("recovery_classification")
        if classification not in {
            "needs_source_recovery",
            "terminal_unrecoverable",
            "verified_rewrite",
            "verified_source_brief",
        }:
            raise HistoricalRehydrationApplyError(
                f"inventory recovery classification is invalid: {path}"
            )
        locator = entry.get("source_locator")
        if not isinstance(locator, Mapping) or any(not isinstance(key, str) for key in locator):
            raise HistoricalRehydrationApplyError(f"inventory source locator is invalid: {path}")
        entry["path"] = path
        entry["source_locator"] = {str(key): value for key, value in locator.items()}
        entries.append(entry)
    if [entry["path"] for entry in entries] != sorted(seen_paths):
        raise HistoricalRehydrationApplyError("inventory entries are not stably sorted")
    return tuple(entries)


def _safe_read_target(root: Path, relative_path: str) -> tuple[Path, bytes, int]:
    path = PurePosixPath(_safe_relative_markdown_path(relative_path))
    current = root
    for component in path.parts[:-1]:
        current /= component
        try:
            details = current.lstat()
        except OSError as exc:
            raise HistoricalRehydrationApplyError(
                f"target parent is unavailable: {relative_path}"
            ) from exc
        if current.is_symlink() or not stat.S_ISDIR(details.st_mode):
            raise HistoricalRehydrationApplyError(
                f"target path crosses an unsafe parent: {relative_path}"
            )
    target = root.joinpath(*path.parts)
    try:
        before = target.lstat()
    except OSError as exc:
        raise HistoricalRehydrationApplyError(f"target is unavailable: {relative_path}") from exc
    if (
        target.is_symlink()
        or not stat.S_ISREG(before.st_mode)
        or before.st_nlink != 1
        or before.st_size > _MAX_MARKDOWN_BYTES
    ):
        raise HistoricalRehydrationApplyError(f"target is an unsafe file: {relative_path}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(target, flags)
        with os.fdopen(descriptor, "rb") as stream:
            opened = os.fstat(stream.fileno())
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened.st_nlink != 1
                or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)
            ):
                raise HistoricalRehydrationApplyError(
                    f"target changed while opening: {relative_path}"
                )
            payload = stream.read(_MAX_MARKDOWN_BYTES + 1)
    except HistoricalRehydrationApplyError:
        raise
    except OSError as exc:
        raise HistoricalRehydrationApplyError(
            f"target cannot be read safely: {relative_path}"
        ) from exc
    if len(payload) > _MAX_MARKDOWN_BYTES:
        raise HistoricalRehydrationApplyError(f"target is too large: {relative_path}")
    return target, payload, before.st_mode & 0o777


def _canonical_public_url(value: object, *, field: str) -> str:
    if not isinstance(value, str) or _UNSAFE_URL_CHARACTER.search(value):
        raise HistoricalRehydrationApplyError(f"{field} is unsafe")
    try:
        canonical = str(canonicalize_url(value))
    except ValueError as exc:
        raise HistoricalRehydrationApplyError(f"{field} is invalid") from exc
    if _UNSAFE_URL_CHARACTER.search(canonical):
        raise HistoricalRehydrationApplyError(f"{field} is unsafe")
    if any(
        _SENSITIVE_QUERY_KEY.search(key) for key, _value in parse_qsl(urlsplit(canonical).query)
    ):
        raise HistoricalRehydrationApplyError(f"{field} contains a sensitive query")
    return canonical


def _capture_metadata(capture: HistoricalSourceCapture) -> Mapping[str, Any]:
    if not isinstance(capture.metadata, Mapping):
        raise HistoricalRehydrationApplyError("capture metadata is invalid")
    return capture.metadata


def _arxiv_url_identifier(value: str) -> str | None:
    parsed = urlsplit(value)
    match = _ARXIV_PATH.fullmatch(parsed.path)
    if parsed.hostname not in {"arxiv.org", "www.arxiv.org"} or match is None:
        return None
    return match.group("identifier")


def _github_url_identity(value: str) -> tuple[str, str] | None:
    parsed = urlsplit(value)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.hostname != "github.com" or len(parts) != 2:
        return None
    repository = parts[1][:-4] if parts[1].casefold().endswith(".git") else parts[1]
    if not repository:
        return None
    return parts[0].casefold(), repository.casefold()


def _juejin_url_identifier(value: str) -> str | None:
    parsed = urlsplit(value)
    match = _JUEJIN_PATH.fullmatch(parsed.path)
    if parsed.hostname not in {"juejin.cn", "www.juejin.cn"} or match is None:
        return None
    return match.group("identifier")


def _positive_redirect_count(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _same_location_https_upgrade(origin: str, capture_url: str) -> bool:
    before = urlsplit(origin)
    after = urlsplit(capture_url)
    return (
        before.scheme == "http"
        and after.scheme == "https"
        and before.hostname == after.hostname
        and before.port in {None, 80}
        and after.port in {None, 443}
        and before.path == after.path
        and before.query == after.query
    )


def _verify_capture_identity(
    entry: Mapping[str, Any], capture: HistoricalSourceCapture
) -> tuple[str, str]:
    path = str(entry["path"])
    source = str(entry.get("source") or "").strip().casefold()
    if not isinstance(capture, HistoricalSourceCapture):
        raise HistoricalRehydrationApplyError(f"capture type is invalid: {path}")
    if not isinstance(capture.source, str) or capture.source.strip().casefold() != source:
        raise HistoricalRehydrationApplyError(f"capture source does not match: {path}")
    if source not in _SUPPORTED_SOURCES:
        raise HistoricalRehydrationApplyError(f"capture source is unsupported: {path}")
    inventory_url = _canonical_public_url(
        entry.get("canonical_url"), field=f"inventory canonical URL for {path}"
    )
    capture_url = _canonical_public_url(
        capture.external_url, field=f"capture external URL for {path}"
    )
    locator = entry.get("source_locator")
    if not isinstance(locator, Mapping) or locator.get("status") != "resolved":
        raise HistoricalRehydrationApplyError(f"capture source locator is unresolved: {path}")
    kind = str(locator.get("kind") or "").strip().casefold()
    metadata = _capture_metadata(capture)

    matches = False
    if source == "arxiv" and kind == "arxiv":
        identifier = str(locator.get("arxiv_id") or "").strip()
        matches = bool(identifier) and all(
            value == identifier
            for value in (
                str(metadata.get("arxiv_id") or "").strip(),
                _arxiv_url_identifier(inventory_url),
                _arxiv_url_identifier(capture_url),
            )
        )
    elif source == "github_trending" and kind == "github":
        expected = (
            str(locator.get("owner") or "").strip().casefold(),
            str(locator.get("repo") or "").strip().removesuffix(".git").casefold(),
        )
        matches = bool(all(expected)) and all(
            identity == expected
            for identity in (
                _github_url_identity(inventory_url),
                _github_url_identity(capture_url),
            )
        )
    elif source == "hacker_news" and kind == "hacker_news":
        identifier = str(locator.get("hn_id") or "").strip()
        matches = identifier.isdigit() and str(metadata.get("hn_id") or "") == identifier
    elif source == "juejin" and kind == "juejin":
        identifier = str(locator.get("article_id") or "").strip()
        matches = bool(identifier) and all(
            value == identifier
            for value in (
                str(metadata.get("article_id") or "").strip(),
                _juejin_url_identifier(inventory_url),
                _juejin_url_identifier(capture_url),
            )
        )
    elif source == "blogs_podcasts" and kind == "external_url":
        origin = _canonical_public_url(
            metadata.get("origin_url"), field=f"capture origin URL for {path}"
        )
        parsed_capture = urlsplit(capture_url)
        try:
            address = ipaddress.ip_address(parsed_capture.hostname or "")
        except ValueError:
            hostname = parsed_capture.hostname or ""
            public_host = (
                "." in hostname
                and hostname != "localhost"
                and not hostname.endswith((".local", ".internal", ".localhost"))
            )
        else:
            public_host = address.is_global
        redirect_is_consistent = (
            capture_url == origin
            or _same_location_https_upgrade(origin, capture_url)
            or _positive_redirect_count(metadata.get("redirect_count"))
        )
        matches = (
            origin == inventory_url
            and parsed_capture.scheme == "https"
            and public_host
            and redirect_is_consistent
        )
    if not matches:
        raise HistoricalRehydrationApplyError(f"capture identity does not match: {path}")

    identity_digest = sha256_digest(
        {
            "canonical_url": inventory_url,
            "locator": dict(locator),
            "source": source,
        }
    )
    try:
        capture_digest = sha256_digest(capture)
    except (TypeError, ValueError) as exc:
        raise HistoricalRehydrationApplyError(f"capture cannot be authenticated: {path}") from exc
    return identity_digest, capture_digest


def _aware_timestamp(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise HistoricalRehydrationApplyError(f"{field} is invalid")
    normalized = f"{value[:-1]}+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise HistoricalRehydrationApplyError(f"{field} is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise HistoricalRehydrationApplyError(f"{field} requires a timezone")
    return value


def _route_date(value: object) -> object:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise HistoricalRehydrationApplyError("historical date requires a timezone")
        return value
    _aware_timestamp(value, field="historical date")
    return value


def _route_aliases(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise HistoricalRehydrationApplyError("historical aliases must be a list")
    result: list[str] = []
    for raw in value:
        if not isinstance(raw, str):
            raise HistoricalRehydrationApplyError("historical alias is unsafe")
        parsed = urlsplit(raw)
        path = PurePosixPath(parsed.path)
        if (
            raw != raw.strip()
            or not raw.startswith("/")
            or len(raw) > 512
            or "\\" in raw
            or any(ord(character) < 32 for character in raw)
            or parsed.scheme
            or parsed.netloc
            or parsed.query
            or parsed.fragment
            or any(part == ".." for part in path.parts)
        ):
            raise HistoricalRehydrationApplyError("historical alias is unsafe")
        result.append(raw)
    return result


def _failure_values(failure: HistoricalRecoveryFailure) -> tuple[str, str, str]:
    if not isinstance(failure, HistoricalRecoveryFailure):
        raise HistoricalRehydrationApplyError("historical recovery failure type is invalid")
    if not all(
        isinstance(value, str)
        for value in (failure.failure_type, failure.reason, failure.attempted_at)
    ):
        raise HistoricalRehydrationApplyError("historical recovery failure type is invalid")
    failure_type = failure.failure_type.strip()
    reason = failure.reason.strip()
    if failure_type not in HISTORICAL_RECOVERY_FAILURE_TYPES:
        raise HistoricalRehydrationApplyError("historical recovery failure type is invalid")
    if _FAILURE_REASON.fullmatch(reason) is None:
        raise HistoricalRehydrationApplyError("historical recovery failure reason is invalid")
    attempted_at = _aware_timestamp(failure.attempted_at, field="historical recovery attempted_at")
    return failure_type, reason, attempted_at


def _render_failure_archive(
    entry: Mapping[str, Any],
    failure: HistoricalRecoveryFailure,
    *,
    prior_metadata: Mapping[str, Any],
) -> str:
    path = str(entry["path"])
    source = str(entry.get("source") or "").strip().casefold()
    if source not in _SUPPORTED_SOURCES:
        raise HistoricalRehydrationApplyError(f"failure source is unsupported: {path}")
    canonical_url = _canonical_public_url(
        entry.get("canonical_url"), field=f"inventory canonical URL for {path}"
    )
    failure_type, reason, attempted_at = _failure_values(failure)
    date = _route_date(prior_metadata.get("date"))
    aliases = _route_aliases(prior_metadata.get("aliases"))
    label = _SOURCE_LABELS[source]
    metadata: dict[str, Any] = {
        "title": f"历史来源恢复记录 · {label}",
        "date": date,
        "draft": False,
        "entry_kind": "auto",
        "tags": [],
        "categories": [],
        "scenarios": [],
        "source": source,
        "description": "历史来源恢复未成功；旧正文已移除，仅保留可审计归档记录。",
        "external_url": canonical_url,
        "aliases": aliases,
        "archived": True,
        "content_mode": "archived",
        "publication_tier": "ARCHIVED",
        "source_provenance": "historical_recovery_failed",
        "source_support": 0.0,
        "archive_reason": "historical_source_recovery_failed",
        "recovery_failure_type": failure_type,
        "recovery_failure_reason": reason,
        "recovery_attempted_at": attempted_at,
        "build": {"list": "never", "render": "always"},
    }
    frontmatter = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip()
    body = (
        "## 历史来源恢复说明\n\n"
        "该条目的公开来源恢复未能完成。为避免继续传播不可核验文本，"
        "旧正文未被保留，本页仅保存透明归档记录。\n\n"
        f"- **来源类型**: `{source}`\n"
        f"- **恢复尝试时间**: `{attempted_at}`\n"
        f"- **恢复失败类型**: `{failure_type}`\n"
        f"- **恢复失败原因**: `{reason}`\n"
        f"- **原始来源**: [查看公开来源](<{canonical_url}>)"
    )
    document = f"---\n{frontmatter}\n---\n\n{body}\n"
    if analyze_post(document).status != "archived":
        raise HistoricalRehydrationApplyError(
            f"failure archive did not satisfy the archived contract: {path}"
        )
    return document


def _public_write(operation: PlannedHistoricalRehydrationWrite) -> dict[str, Any]:
    return {
        "path": operation.path,
        "source": operation.source,
        "outcome": operation.outcome,
        "input_sha256": operation.input_sha256,
        "output_sha256": operation.output_sha256,
        "source_identity_sha256": operation.source_identity_sha256,
        "outcome_sha256": operation.outcome_sha256,
    }


def build_historical_rehydration_apply_plan(
    inventory: Mapping[str, Any],
    captures: Mapping[str, HistoricalSourceCapture],
    *,
    content_root: str | Path,
    failures: Mapping[str, HistoricalRecoveryFailure] | None = None,
) -> HistoricalRehydrationApplyPlan:
    """Build a deterministic recovery plan without writing any file."""

    root = _safe_content_root(content_root)
    entries = _validated_inventory_entries(inventory, content_root=root)
    if not isinstance(captures, Mapping):
        raise HistoricalRehydrationApplyError("captures must be a path mapping")
    if failures is not None and not isinstance(failures, Mapping):
        raise HistoricalRehydrationApplyError("failures must be a path mapping")
    selected_failures: Mapping[str, HistoricalRecoveryFailure] = (
        failures if failures is not None else {}
    )
    capture_paths = {_safe_relative_markdown_path(path) for path in captures}
    failure_paths = {_safe_relative_markdown_path(path) for path in selected_failures}
    overlap = capture_paths.intersection(failure_paths)
    if overlap:
        raise HistoricalRehydrationApplyError(
            f"path has both capture and failure outcomes: {sorted(overlap)[0]}"
        )
    selected_paths = capture_paths.union(failure_paths)
    if not selected_paths:
        raise HistoricalRehydrationApplyError("at least one recovery outcome is required")
    by_path = {str(entry["path"]): entry for entry in entries}
    unknown = selected_paths.difference(by_path)
    if unknown:
        raise HistoricalRehydrationApplyError(
            f"recovery path is absent from inventory: {sorted(unknown)[0]}"
        )

    operations: list[PlannedHistoricalRehydrationWrite] = []
    for path in sorted(selected_paths):
        entry = by_path[path]
        if entry.get("recovery_classification") != "needs_source_recovery":
            raise HistoricalRehydrationApplyError(
                f"recovery path is already terminal or verified: {path}"
            )
        _target, payload, _mode = _safe_read_target(root, path)
        input_sha256 = _sha256(payload)
        if not _same_digest(input_sha256, entry.get("target_sha256")):
            raise HistoricalRehydrationApplyError(f"stale target SHA does not match: {path}")
        try:
            document = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise HistoricalRehydrationApplyError(f"target is not UTF-8: {path}") from exc
        prior = markdown_frontmatter(document)
        if not prior:
            raise HistoricalRehydrationApplyError(f"target frontmatter is invalid: {path}")
        source = str(entry.get("source") or "").strip().casefold()
        identity_digest = sha256_digest(
            {
                "canonical_url": _canonical_public_url(
                    entry.get("canonical_url"),
                    field=f"inventory canonical URL for {path}",
                ),
                "locator": dict(entry["source_locator"]),
                "source": source,
            }
        )
        if path in capture_paths:
            capture = captures[path]
            identity_digest, outcome_digest = _verify_capture_identity(entry, capture)
            try:
                rendered = render_historical_tier_c_markdown(
                    capture,
                    prior_metadata={
                        "date": prior.get("date"),
                        "aliases": prior.get("aliases"),
                    },
                )
            except HistoricalPublicationError as exc:
                raise HistoricalRehydrationApplyError(
                    f"capture cannot render a Tier-C source brief: {path}: {exc}"
                ) from exc
            outcome = "source_brief"
        else:
            failure = selected_failures[path]
            rendered = _render_failure_archive(
                entry,
                failure,
                prior_metadata={
                    "date": prior.get("date"),
                    "aliases": prior.get("aliases"),
                },
            )
            outcome_digest = sha256_digest(failure)
            outcome = "terminal_unrecoverable"
        output = rendered.encode("utf-8")
        if len(output) > _MAX_MARKDOWN_BYTES:
            raise HistoricalRehydrationApplyError(f"rendered target is too large: {path}")
        operations.append(
            PlannedHistoricalRehydrationWrite(
                path=path,
                source=source,
                outcome=outcome,
                input_sha256=input_sha256,
                output_sha256=_sha256(output),
                source_identity_sha256=identity_digest,
                outcome_sha256=outcome_digest,
                content=output,
            )
        )

    outcome_counts = Counter(operation.outcome for operation in operations)
    base_manifest: dict[str, Any] = {
        "schema": HISTORICAL_REHYDRATION_APPLY_PLAN_SCHEMA,
        "version": HISTORICAL_REHYDRATION_APPLY_PLAN_VERSION,
        "content_root": str(root),
        "inventory_schema": inventory.get("schema"),
        "inventory_version": inventory.get("version"),
        "inventory_entry_count": inventory.get("entry_count"),
        "inventory_entries_sha256": inventory.get("entries_sha256"),
        "planned_changes": len(operations),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "writes": [_public_write(operation) for operation in operations],
        "identity_policy": {
            "arxiv": "locator_arxiv_id_with_http_https_equivalence",
            "github_trending": "locator_owner_repo_with_optional_dot_git",
            "hacker_news": "locator_hn_id",
            "juejin": "locator_article_id",
            "blogs_podcasts": (
                "inventory_url_equals_capture_origin_and_redirect_was_allowlist_validated"
            ),
        },
        "execution_policy": {
            "default_mutation": False,
            "requires_clean_codex_branch": True,
            "requires_exact_head": True,
            "requires_exact_plan_digest": True,
            "requires_max_changes": True,
            "backup_before_mutation": True,
            "atomic_strategy": "same_directory_replace_with_full_backup_rollback",
        },
    }
    manifest = dict(base_manifest)
    manifest["plan_digest"] = sha256_digest(base_manifest)
    return HistoricalRehydrationApplyPlan(
        content_root=root,
        manifest=manifest,
        writes=tuple(operations),
    )


def _validated_plan(plan: HistoricalRehydrationApplyPlan) -> None:
    if not isinstance(plan, HistoricalRehydrationApplyPlan):
        raise HistoricalRehydrationApplyError("plan type is invalid")
    manifest = plan.manifest
    if (
        not isinstance(manifest, Mapping)
        or manifest.get("schema") != HISTORICAL_REHYDRATION_APPLY_PLAN_SCHEMA
        or manifest.get("version") != HISTORICAL_REHYDRATION_APPLY_PLAN_VERSION
    ):
        raise HistoricalRehydrationApplyError("plan integrity check failed")
    base_manifest = dict(manifest)
    recorded_digest = base_manifest.pop("plan_digest", None)
    try:
        calculated_digest = sha256_digest(base_manifest)
    except (TypeError, ValueError) as exc:
        raise HistoricalRehydrationApplyError("plan integrity check failed") from exc
    if not _same_digest(recorded_digest, calculated_digest):
        raise HistoricalRehydrationApplyError("plan integrity check failed")
    if manifest.get("content_root") != str(plan.content_root):
        raise HistoricalRehydrationApplyError("plan integrity check failed")
    if manifest.get("planned_changes") != len(plan.writes) or not plan.writes:
        raise HistoricalRehydrationApplyError("plan integrity check failed")
    paths = [operation.path for operation in plan.writes]
    if paths != sorted(set(paths)):
        raise HistoricalRehydrationApplyError("plan integrity check failed")
    for operation in plan.writes:
        _safe_relative_markdown_path(operation.path)
        if (
            _SHA256_HEX.fullmatch(operation.input_sha256) is None
            or _SHA256_HEX.fullmatch(operation.output_sha256) is None
            or _SHA256_DIGEST.fullmatch(operation.source_identity_sha256) is None
            or _SHA256_DIGEST.fullmatch(operation.outcome_sha256) is None
            or _sha256(operation.content) != operation.output_sha256
        ):
            raise HistoricalRehydrationApplyError("plan integrity check failed")
    if manifest.get("writes") != [_public_write(operation) for operation in plan.writes]:
        raise HistoricalRehydrationApplyError("plan integrity check failed")
    _safe_content_root(plan.content_root)


def _run_git(root: Path, arguments: list[str], *, failure: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise HistoricalRehydrationApplyError(failure)
    return result.stdout.strip()


def _repository_state(content_root: Path) -> _RepositoryState:
    root_text = _run_git(
        content_root,
        ["rev-parse", "--show-toplevel"],
        failure="content root is not inside a Git repository",
    )
    repository = Path(root_text).absolute()
    try:
        content_root.resolve().relative_to(repository.resolve())
    except ValueError as exc:
        raise HistoricalRehydrationApplyError("content root escapes its Git repository") from exc
    branch = _run_git(
        repository,
        ["symbolic-ref", "--quiet", "--short", "HEAD"],
        failure="historical rehydration requires an attached branch",
    )
    head = _run_git(
        repository,
        ["rev-parse", "HEAD"],
        failure="historical rehydration cannot read Git HEAD",
    ).casefold()
    if _GIT_HEAD.fullmatch(head) is None:
        raise HistoricalRehydrationApplyError("historical rehydration Git HEAD is invalid")
    status = _run_git(
        repository,
        ["status", "--porcelain=v1", "--untracked-files=all"],
        failure="historical rehydration cannot read Git worktree state",
    )
    return _RepositoryState(repository, branch, head, status)


def _validate_repository_gate(state: _RepositoryState, *, expected_head: str) -> None:
    if not isinstance(expected_head, str) or _GIT_HEAD.fullmatch(expected_head.casefold()) is None:
        raise HistoricalRehydrationApplyError("expected HEAD must be a full Git hash")
    if not state.branch.startswith("codex/"):
        raise HistoricalRehydrationApplyError("historical rehydration requires a codex/ branch")
    if state.status:
        raise HistoricalRehydrationApplyError(
            "historical rehydration requires a clean Git worktree"
        )
    if not hmac.compare_digest(state.head, expected_head.casefold()):
        raise HistoricalRehydrationApplyError(
            f"historical rehydration HEAD mismatch: expected {expected_head}, found {state.head}"
        )


def _is_within(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _validated_backup_root(value: str | Path, *, repository_root: Path) -> Path:
    root = Path(value).absolute()
    resolved = root.resolve(strict=False)
    repository_resolved = repository_root.resolve()
    if _is_within(resolved, repository_resolved):
        raise HistoricalRehydrationApplyError("backup root must be outside the Git repository")
    if root.is_symlink() or (root.exists() and not root.is_dir()):
        raise HistoricalRehydrationApplyError("backup root is unsafe")
    existed = root.exists()
    try:
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
    except OSError as exc:
        raise HistoricalRehydrationApplyError("backup root cannot be created") from exc
    if root.is_symlink() or not root.is_dir() or root.resolve() != resolved:
        raise HistoricalRehydrationApplyError("backup root is unsafe")
    if not existed:
        root.chmod(0o700)
    return root


def _replace_target_atomically(path: Path, payload: bytes, *, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    finally:
        Path(temporary_name).unlink(missing_ok=True)


def _write_json_atomically(path: Path, value: Mapping[str, Any]) -> None:
    payload = (
        json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    _replace_target_atomically(path, payload, mode=0o600)


def _verify_inputs(
    plan: HistoricalRehydrationApplyPlan,
) -> dict[str, tuple[Path, bytes, int]]:
    records: dict[str, tuple[Path, bytes, int]] = {}
    for operation in plan.writes:
        target, payload, mode = _safe_read_target(plan.content_root, operation.path)
        if _sha256(payload) != operation.input_sha256:
            raise HistoricalRehydrationApplyError(
                f"stale recovery plan target changed: {operation.path}"
            )
        records[operation.path] = (target, payload, mode)
    return records


def _create_complete_backup(
    plan: HistoricalRehydrationApplyPlan,
    *,
    backup_root: Path,
    backup_id: str,
    inputs: Mapping[str, tuple[Path, bytes, int]],
) -> Path:
    backup_directory = backup_root / backup_id
    if backup_directory.exists() or backup_directory.is_symlink():
        raise HistoricalRehydrationApplyError(
            f"backup id already exists or is incomplete: {backup_id}"
        )
    staging = Path(tempfile.mkdtemp(prefix=f".{backup_id}.", dir=backup_root))
    try:
        before_root = staging / "before"
        for operation in plan.writes:
            _target, payload, mode = inputs[operation.path]
            destination = before_root.joinpath(*PurePosixPath(operation.path).parts)
            _replace_target_atomically(destination, payload, mode=mode)
        _write_json_atomically(staging / "plan.json", plan.manifest)
        for operation in plan.writes:
            _path, payload, _mode = _safe_read_target(before_root, operation.path)
            if _sha256(payload) != operation.input_sha256:
                raise HistoricalRehydrationApplyError(
                    f"backup verification failed: {operation.path}"
                )
        os.replace(staging, backup_directory)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return backup_directory


def _verify_outputs(plan: HistoricalRehydrationApplyPlan) -> None:
    for operation in plan.writes:
        _target, payload, _mode = _safe_read_target(plan.content_root, operation.path)
        if _sha256(payload) != operation.output_sha256:
            raise HistoricalRehydrationApplyError(
                f"applied recovery output does not match: {operation.path}"
            )


def _restore_all_from_backup(
    plan: HistoricalRehydrationApplyPlan, *, backup_directory: Path
) -> None:
    before_root = backup_directory / "before"
    failures: list[str] = []
    for operation in plan.writes:
        try:
            _backup, payload, mode = _safe_read_target(before_root, operation.path)
            if _sha256(payload) != operation.input_sha256:
                raise HistoricalRehydrationApplyError("backup digest mismatch")
            target = plan.content_root.joinpath(*PurePosixPath(operation.path).parts)
            _replace_target_atomically(target, payload, mode=mode)
        except BaseException:
            failures.append(operation.path)
    for operation in plan.writes:
        try:
            _target, payload, _mode = _safe_read_target(plan.content_root, operation.path)
        except BaseException:
            failures.append(operation.path)
            continue
        if _sha256(payload) != operation.input_sha256:
            failures.append(operation.path)
    if failures:
        unique = ", ".join(sorted(set(failures)))
        raise HistoricalRehydrationRollbackError(
            f"historical rehydration rollback failed for: {unique}"
        )


def _now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def apply_historical_rehydration_plan(
    plan: HistoricalRehydrationApplyPlan,
    *,
    expected_head: str,
    expected_plan_digest: str,
    max_changes: int,
    backup_id: str,
    backup_root: str | Path,
) -> dict[str, Any]:
    """Apply one explicitly reviewed plan with a complete rollback backup."""

    _validated_plan(plan)
    plan_digest = str(plan.manifest["plan_digest"])
    if not _same_digest(expected_plan_digest, plan_digest):
        raise HistoricalRehydrationApplyError("reviewed plan digest does not match")
    if (
        not isinstance(max_changes, int)
        or isinstance(max_changes, bool)
        or not 1 <= max_changes <= _MAX_APPLY_CHANGES
    ):
        raise HistoricalRehydrationApplyError(
            f"max_changes must be between 1 and {_MAX_APPLY_CHANGES}"
        )
    if len(plan.writes) > max_changes:
        raise HistoricalRehydrationApplyError(
            f"planned changes exceed max_changes: {len(plan.writes)}>{max_changes}"
        )
    if not isinstance(backup_id, str) or _BACKUP_ID.fullmatch(backup_id) is None:
        raise HistoricalRehydrationApplyError("backup id is invalid")

    state = _repository_state(plan.content_root)
    _validate_repository_gate(state, expected_head=expected_head)
    destination_root = Path(backup_root).absolute()
    if destination_root.exists() and not destination_root.is_dir():
        raise HistoricalRehydrationApplyError("backup root is unsafe")
    if destination_root.is_symlink():
        raise HistoricalRehydrationApplyError("backup root is unsafe")
    if (destination_root / backup_id).exists() or (destination_root / backup_id).is_symlink():
        raise HistoricalRehydrationApplyError(
            f"backup id already exists or is incomplete: {backup_id}"
        )

    inputs = _verify_inputs(plan)
    safe_backup_root = _validated_backup_root(destination_root, repository_root=state.root)
    backup_directory = _create_complete_backup(
        plan,
        backup_root=safe_backup_root,
        backup_id=backup_id,
        inputs=inputs,
    )
    second_state = _repository_state(plan.content_root)
    _validate_repository_gate(second_state, expected_head=expected_head)
    if second_state != state:
        raise HistoricalRehydrationApplyError("Git repository state changed after backup creation")
    _verify_inputs(plan)

    receipt: dict[str, Any] = {
        "schema": HISTORICAL_REHYDRATION_APPLY_RECEIPT_SCHEMA,
        "version": HISTORICAL_REHYDRATION_APPLY_RECEIPT_VERSION,
        "state": "applied",
        "applied_at": _now_iso(),
        "plan_digest": plan_digest,
        "inventory_entries_sha256": plan.manifest["inventory_entries_sha256"],
        "expected_head": expected_head.casefold(),
        "branch": state.branch,
        "backup_id": backup_id,
        "applied_count": len(plan.writes),
        "items": [_public_write(operation) for operation in plan.writes],
    }
    receipt_path = backup_directory / "receipt.json"
    try:
        for operation in plan.writes:
            target, payload, mode = _safe_read_target(plan.content_root, operation.path)
            if _sha256(payload) != operation.input_sha256:
                raise HistoricalRehydrationApplyError(
                    f"stale recovery plan target changed: {operation.path}"
                )
            _replace_target_atomically(target, operation.content, mode=mode)
        _verify_outputs(plan)
        _write_json_atomically(receipt_path, receipt)
    except BaseException as mutation_error:
        receipt_path.unlink(missing_ok=True)
        try:
            _restore_all_from_backup(plan, backup_directory=backup_directory)
        except BaseException as rollback_error:
            raise HistoricalRehydrationRollbackError(
                "historical rehydration failed and rollback was incomplete"
            ) from rollback_error
        raise mutation_error
    return receipt


__all__ = [
    "HISTORICAL_REHYDRATION_APPLY_PLAN_SCHEMA",
    "HISTORICAL_REHYDRATION_APPLY_PLAN_VERSION",
    "HISTORICAL_REHYDRATION_APPLY_RECEIPT_SCHEMA",
    "HISTORICAL_REHYDRATION_APPLY_RECEIPT_VERSION",
    "HistoricalRecoveryFailure",
    "HistoricalRehydrationApplyError",
    "HistoricalRehydrationApplyPlan",
    "HistoricalRehydrationRollbackError",
    "PlannedHistoricalRehydrationWrite",
    "apply_historical_rehydration_plan",
    "build_historical_rehydration_apply_plan",
]
