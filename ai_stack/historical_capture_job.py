"""Bounded source-capture batches for an offline historical inventory.

The job consumes only the immutable inventory JSON produced by
``historical_rehydration``. It never reads or writes Markdown. Network adapters
are source-specific, result ordering is deterministic, and evidence is written
only to an explicit mode-0600 JSON audit file by the caller.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import stat
import threading
import time
import unicodedata
import urllib.robotparser
import uuid
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import parse_qsl, urljoin, urlsplit, urlunsplit

from crawler import historical_source_fetch as source_fetch_adapter
from crawler.historical_source_fetch import (
    HistoricalSourceCapture,
    HistoricalSourceFetchError,
    fetch_arxiv_sources,
    fetch_github_source,
    fetch_hacker_news_source,
    fetch_juejin_source_excerpt,
    fetch_public_article_excerpt,
)

from ._json import canonical_json_bytes, sha256_digest
from .historical_rehydration import (
    HISTORICAL_REHYDRATION_SCHEMA,
    HISTORICAL_REHYDRATION_VERSION,
)
from .identity import canonicalize_url

CAPTURE_AUDIT_SCHEMA = "ai_stack.historical_capture.audit"
CAPTURE_AUDIT_VERSION = 1
BLOG_ALLOWLIST_SCHEMA = "ai_stack.historical_capture.blog_allowlist"
BLOG_ALLOWLIST_VERSION = 1

DEFAULT_LIMIT = 20
MAX_LIMIT = 500
DEFAULT_CONCURRENCY = 4
MAX_CONCURRENCY = 8
DEFAULT_PER_HOST_CONCURRENCY = 2
MAX_PER_HOST_CONCURRENCY = 4
DEFAULT_TIMEOUT = 15
MAX_TIMEOUT = 60

_MAX_INPUT_BYTES = 64 * 1024 * 1024
_MAX_ALLOWLIST_BYTES = 64 * 1024
_MAX_CAPTURE_TEXT_CHARS = 12_000
_MAX_CAPTURE_METADATA_BYTES = 64 * 1024
_MAX_ROBOTS_BYTES = 256 * 1024
_MAX_ROBOTS_REDIRECTS = 3
_ROBOTS_USER_AGENT = "AI-Stack-Historical-Rehydration"
_ARXIV_BATCH_SIZE = 50
_ARXIV_BATCH_INTERVAL_SECONDS = 3.0
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_HOST_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_SAFE_FAILURE = re.compile(r"^[a-z][a-z0-9_]{1,127}$")
_SENSITIVE_QUERY_KEY = re.compile(
    r"(?:^|[_-])(?:api[_-]?key|access[_-]?token|auth|authorization|credential|"
    r"password|secret|signature|signed|token)(?:$|[_-])",
    re.IGNORECASE,
)
_SUPPORTED_SOURCES = frozenset(
    {"arxiv", "github_trending", "hacker_news", "juejin", "blogs_podcasts"}
)


class HistoricalCaptureJobError(ValueError):
    """Safe, typed configuration or audit-integrity failure."""


class _CaptureDispatchError(ValueError):
    """One-target dispatch failure that must not terminate the batch."""


@dataclass(frozen=True, slots=True)
class CaptureTarget:
    path: str
    target_sha256: str
    source: str
    canonical_url: str
    source_locator: dict[str, Any]


CaptureDispatcher = Callable[
    [CaptureTarget, frozenset[str], int], HistoricalSourceCapture
]
RobotsPolicy = Callable[[str], bool]
RobotsChecker = Callable[
    [str, frozenset[str], int], RobotsPolicy | bool
]


@dataclass(frozen=True, slots=True)
class _RobotsOutcome:
    policy: RobotsPolicy | None = None
    failure_type: str = ""
    reason: str = ""


class _RobotsPolicyCache:
    def __init__(self, checker: RobotsChecker) -> None:
        self.checker = checker
        self._guard = threading.Lock()
        self._host_locks: dict[str, threading.Lock] = {}
        self._outcomes: dict[str, _RobotsOutcome] = {}

    def _host_lock(self, host: str) -> threading.Lock:
        with self._guard:
            return self._host_locks.setdefault(host, threading.Lock())

    def allowed(
        self,
        *,
        host: str,
        source_url: str,
        allowed_hosts: frozenset[str],
        timeout: int,
    ) -> tuple[bool, str, str]:
        with self._host_lock(host):
            outcome = self._outcomes.get(host)
            if outcome is None:
                try:
                    loaded = self.checker(source_url, allowed_hosts, timeout)
                    if isinstance(loaded, bool):
                        def constant_policy(
                            _url: str, decision: bool = loaded
                        ) -> bool:
                            return decision

                        policy: RobotsPolicy = constant_policy
                    elif callable(loaded):
                        policy = loaded
                    else:
                        raise TypeError("invalid robots policy")
                    outcome = _RobotsOutcome(policy=policy)
                except Exception:
                    outcome = _RobotsOutcome(
                        failure_type="robots_fetch_error",
                        reason="robots_fetch_failed",
                    )
                self._outcomes[host] = outcome
        if outcome.policy is None:
            return False, outcome.failure_type, outcome.reason
        try:
            allowed = outcome.policy(source_url)
        except Exception:
            return False, "robots_fetch_error", "robots_fetch_failed"
        if allowed is not True:
            return False, "robots_disallowed", "robots_disallowed"
        return True, "", ""


def _now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _is_timezone_aware_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _reject_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            raise HistoricalCaptureJobError("unsafe_symlink_path")


def _read_json_file(path: str | Path, *, maximum_bytes: int) -> Mapping[str, Any]:
    candidate = Path(path).absolute()
    _reject_symlink_components(candidate)
    try:
        details = candidate.lstat()
    except FileNotFoundError as exc:
        raise HistoricalCaptureJobError("json_input_missing") from exc
    if not stat.S_ISREG(details.st_mode) or details.st_size > maximum_bytes:
        raise HistoricalCaptureJobError("json_input_invalid")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
        with os.fdopen(descriptor, "rb") as stream:
            raw = stream.read(maximum_bytes + 1)
    except OSError as exc:
        raise HistoricalCaptureJobError("json_input_unreadable") from exc
    if len(raw) > maximum_bytes:
        raise HistoricalCaptureJobError("json_input_invalid")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HistoricalCaptureJobError("json_input_invalid") from exc
    if not isinstance(payload, Mapping):
        raise HistoricalCaptureJobError("json_input_invalid")
    return {str(key): value for key, value in payload.items()}


def load_historical_capture_inventory(path: str | Path) -> dict[str, Any]:
    """Load and authenticate one pure-offline rehydration inventory."""

    inventory = dict(_read_json_file(path, maximum_bytes=_MAX_INPUT_BYTES))
    _validated_inventory_entries(inventory)
    return inventory


def _normalized_host(value: object) -> str:
    raw = str(value or "").strip().rstrip(".")
    if not raw or len(raw) > 253 or "://" in raw or any(
        character in raw for character in "/?#@:*"
    ):
        raise HistoricalCaptureJobError("blog_allowlist_invalid")
    try:
        host = raw.encode("idna").decode("ascii").casefold()
    except UnicodeError as exc:
        raise HistoricalCaptureJobError("blog_allowlist_invalid") from exc
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise HistoricalCaptureJobError("blog_allowlist_invalid")
    labels = host.split(".")
    if len(labels) < 2 or any(_HOST_LABEL.fullmatch(label) is None for label in labels):
        raise HistoricalCaptureJobError("blog_allowlist_invalid")
    return host


def _normalized_allowed_hosts(values: Iterable[object]) -> frozenset[str]:
    hosts = frozenset(_normalized_host(value) for value in values)
    if not hosts or len(hosts) > 200:
        raise HistoricalCaptureJobError("blog_allowlist_invalid")
    return hosts


def load_blog_allowlist(path: str | Path) -> frozenset[str]:
    """Load exact blog hosts from an explicit, versioned JSON config."""

    payload = _read_json_file(path, maximum_bytes=_MAX_ALLOWLIST_BYTES)
    if (
        payload.get("schema") != BLOG_ALLOWLIST_SCHEMA
        or payload.get("version") != BLOG_ALLOWLIST_VERSION
    ):
        raise HistoricalCaptureJobError("blog_allowlist_invalid")
    values = payload.get("allowed_hosts")
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        raise HistoricalCaptureJobError("blog_allowlist_invalid")
    return _normalized_allowed_hosts(values)


def _safe_relative_markdown_path(value: object) -> str:
    raw = str(value or "").strip()
    path = PurePosixPath(raw)
    if (
        not raw
        or path.is_absolute()
        or raw != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.suffix.casefold() != ".md"
    ):
        raise HistoricalCaptureJobError("inventory_entry_invalid")
    return raw


def _validated_inventory_entries(
    inventory: Mapping[str, Any],
) -> tuple[Mapping[str, Any], ...]:
    if (
        inventory.get("schema") != HISTORICAL_REHYDRATION_SCHEMA
        or inventory.get("version") != HISTORICAL_REHYDRATION_VERSION
        or inventory.get("offline") is not True
    ):
        raise HistoricalCaptureJobError("inventory_contract_invalid")
    entries = inventory.get("entries")
    if not isinstance(entries, list) or len(entries) > 100_000:
        raise HistoricalCaptureJobError("inventory_contract_invalid")
    if inventory.get("entry_count") != len(entries):
        raise HistoricalCaptureJobError("inventory_integrity_invalid")
    if inventory.get("entries_sha256") != sha256_digest(entries):
        raise HistoricalCaptureJobError("inventory_integrity_invalid")
    validated: list[Mapping[str, Any]] = []
    seen_paths: set[str] = set()
    for raw_entry in entries:
        if not isinstance(raw_entry, Mapping):
            raise HistoricalCaptureJobError("inventory_entry_invalid")
        entry = {str(key): value for key, value in raw_entry.items()}
        path = _safe_relative_markdown_path(entry.get("path"))
        if path in seen_paths:
            raise HistoricalCaptureJobError("inventory_entry_invalid")
        seen_paths.add(path)
        target_sha256 = str(entry.get("target_sha256") or "").strip()
        source = str(entry.get("source") or "").strip().casefold()
        classification = str(entry.get("recovery_classification") or "").strip()
        locator = entry.get("source_locator")
        if (
            _SHA256_HEX.fullmatch(target_sha256) is None
            or not source
            or len(source) > 80
            or not classification
            or not isinstance(locator, Mapping)
        ):
            raise HistoricalCaptureJobError("inventory_entry_invalid")
        canonical_url = str(entry.get("canonical_url") or "").strip()
        if canonical_url:
            try:
                canonical_url = canonicalize_url(canonical_url)
            except ValueError as exc:
                raise HistoricalCaptureJobError("inventory_entry_invalid") from exc
        entry["path"] = path
        entry["target_sha256"] = target_sha256
        entry["source"] = source
        entry["canonical_url"] = canonical_url
        entry["source_locator"] = {str(key): value for key, value in locator.items()}
        validated.append(entry)
    return tuple(validated)


def _selection_filter(value: object) -> str:
    normalized = " ".join(unicodedata.normalize("NFKC", str(value or "")).split())
    if len(normalized) > 256 or any(ord(character) < 32 for character in normalized):
        raise HistoricalCaptureJobError("filter_invalid")
    return normalized.casefold()


def _validated_sources(sources: Iterable[str] | None) -> frozenset[str]:
    normalized = frozenset(
        str(source or "").strip().casefold() for source in (sources or ())
    )
    if "" in normalized or not normalized.issubset(_SUPPORTED_SOURCES):
        raise HistoricalCaptureJobError("source_filter_invalid")
    return normalized


def _validated_limit(limit: int) -> int:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_LIMIT:
        raise HistoricalCaptureJobError("limit_invalid")
    return limit


def select_capture_targets(
    inventory: Mapping[str, Any],
    *,
    sources: Iterable[str] | None = None,
    filter_text: str = "",
    limit: int = DEFAULT_LIMIT,
) -> tuple[CaptureTarget, ...]:
    """Select a deterministic prefix of resolved recovery candidates."""

    maximum = _validated_limit(limit)
    return _eligible_capture_targets(
        inventory,
        sources=sources,
        filter_text=filter_text,
    )[:maximum]


def _eligible_capture_targets(
    inventory: Mapping[str, Any],
    *,
    sources: Iterable[str] | None = None,
    filter_text: str = "",
) -> tuple[CaptureTarget, ...]:
    entries = _validated_inventory_entries(inventory)
    source_filter = _validated_sources(sources)
    folded_filter = _selection_filter(filter_text)
    targets: list[CaptureTarget] = []
    for entry in entries:
        source = str(entry["source"])
        locator = entry["source_locator"]
        if entry.get("recovery_classification") != "needs_source_recovery":
            continue
        if locator.get("status") != "resolved":
            continue
        if source_filter and source not in source_filter:
            continue
        haystack = " ".join(
            (str(entry["path"]), source, str(entry["canonical_url"]))
        ).casefold()
        if folded_filter and folded_filter not in haystack:
            continue
        targets.append(
            CaptureTarget(
                path=str(entry["path"]),
                target_sha256=str(entry["target_sha256"]),
                source=source,
                canonical_url=str(entry["canonical_url"]),
                source_locator=dict(locator),
            )
        )
    targets.sort(
        key=lambda target: (
            target.path,
            target.source,
            target.canonical_url,
            target.target_sha256,
        )
    )
    return tuple(targets)


def _required_locator_text(target: CaptureTarget, name: str) -> str:
    value = target.source_locator.get(name)
    if not isinstance(value, (str, int)):
        raise _CaptureDispatchError("source_locator_invalid")
    normalized = str(value).strip()
    if not normalized or len(normalized) > 512:
        raise _CaptureDispatchError("source_locator_invalid")
    return normalized


def load_blog_robots_policy(
    source_url: str,
    allowed_hosts: frozenset[str],
    timeout: int,
) -> RobotsPolicy:
    """Fetch one host policy through the article adapter's SSRF-safe URL guard."""

    parsed_source = urlsplit(source_url)
    host = (parsed_source.hostname or "").encode("idna").decode("ascii").casefold()
    robots_url = urlunsplit(("https", host, "/robots.txt", "", ""))
    current = source_fetch_adapter._validate_public_url(  # noqa: SLF001
        robots_url,
        allowed_hosts=set(allowed_hosts),
        resolver=source_fetch_adapter._default_resolver,  # noqa: SLF001
    )
    redirects = 0
    while True:
        response, body = source_fetch_adapter._request(  # noqa: SLF001
            source_fetch_adapter.requests,
            current,
            timeout=timeout,
            accept="text/plain",
            maximum_bytes=_MAX_ROBOTS_BYTES,
            too_large="robots_response_too_large",
        )
        try:
            if response.status_code in source_fetch_adapter._REDIRECT_STATUSES:  # noqa: SLF001
                if redirects >= _MAX_ROBOTS_REDIRECTS:
                    raise HistoricalSourceFetchError("robots_redirect_limit")
                location = str(response.headers.get("Location") or "").strip()
                if not location:
                    raise HistoricalSourceFetchError("robots_redirect_invalid")
                current = source_fetch_adapter._validate_public_url(  # noqa: SLF001
                    urljoin(current, location),
                    allowed_hosts=set(allowed_hosts),
                    resolver=source_fetch_adapter._default_resolver,  # noqa: SLF001
                )
                redirects += 1
                continue
            if response.status_code != 200:
                raise HistoricalSourceFetchError("robots_http_failure")
            content_type = str(response.headers.get("Content-Type") or "").casefold()
            if "text/plain" not in content_type:
                raise HistoricalSourceFetchError("robots_content_type_invalid")
            try:
                document = body.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise HistoricalSourceFetchError("robots_payload_invalid") from exc
            parser = urllib.robotparser.RobotFileParser()
            parser.set_url(current)
            parser.parse(document.splitlines())
            return lambda target_url: parser.can_fetch(
                _ROBOTS_USER_AGENT, target_url
            )
        finally:
            response.close()


def _default_dispatcher(
    target: CaptureTarget,
    blog_allowed_hosts: frozenset[str],
    timeout: int,
) -> HistoricalSourceCapture:
    locator = target.source_locator
    kind = str(locator.get("kind") or "").strip().casefold()
    if target.source == "arxiv":
        raise _CaptureDispatchError("arxiv_batch_required")
    if target.source == "github_trending" and kind == "github":
        return fetch_github_source(
            _required_locator_text(target, "owner"),
            _required_locator_text(target, "repo"),
            timeout=timeout,
        )
    if target.source == "hacker_news" and kind == "hacker_news":
        return fetch_hacker_news_source(
            _required_locator_text(target, "hn_id"), timeout=timeout
        )
    if target.source == "juejin" and kind == "juejin":
        _required_locator_text(target, "article_id")
        return fetch_juejin_source_excerpt(
            target.canonical_url,
            discovery_title=PurePosixPath(target.path).stem,
            timeout=timeout,
        )
    if target.source == "blogs_podcasts" and kind == "external_url":
        transport_url = _blog_transport_url(target, blog_allowed_hosts)
        capture = fetch_public_article_excerpt(
            transport_url,
            allowed_hosts=set(blog_allowed_hosts),
            timeout=timeout,
        )
        return replace(
            capture,
            metadata={**capture.metadata, "origin_url": target.canonical_url},
        )
    raise _CaptureDispatchError("source_dispatch_unsupported")


def _target_host(target: CaptureTarget, allowed_hosts: frozenset[str]) -> str:
    official_hosts = {
        "arxiv": "export.arxiv.org",
        "github_trending": "api.github.com",
        "hacker_news": "hacker-news.firebaseio.com",
        "juejin": "juejin.cn",
    }
    if target.source in official_hosts:
        return official_hosts[target.source]
    if target.source != "blogs_podcasts":
        raise _CaptureDispatchError("source_dispatch_unsupported")
    parsed = urlsplit(_blog_transport_url(target, allowed_hosts))
    host = (parsed.hostname or "").encode("idna").decode("ascii").casefold()
    if host not in allowed_hosts:
        raise _CaptureDispatchError("blog_host_not_allowlisted")
    if any(_SENSITIVE_QUERY_KEY.search(key) for key, _value in parse_qsl(parsed.query)):
        raise _CaptureDispatchError("sensitive_query_not_allowed")
    return host


def _blog_transport_url(
    target: CaptureTarget, allowed_hosts: frozenset[str]
) -> str:
    parsed = urlsplit(target.canonical_url)
    try:
        host = (parsed.hostname or "").encode("idna").decode("ascii").casefold()
    except UnicodeError as exc:
        raise _CaptureDispatchError("blog_host_not_allowlisted") from exc
    if host not in allowed_hosts or parsed.scheme.casefold() not in {"http", "https"}:
        raise _CaptureDispatchError("blog_host_not_allowlisted")
    upgraded = urlunsplit(
        ("https", parsed.netloc, parsed.path or "/", parsed.query, "")
    )
    try:
        return canonicalize_url(upgraded)
    except ValueError as exc:
        raise _CaptureDispatchError("source_url_not_allowed") from exc


def _safe_failure_reason(value: object, fallback: str) -> str:
    reason = str(value or "").strip().casefold()
    return reason if _SAFE_FAILURE.fullmatch(reason) else fallback


def _capture_payload(
    target: CaptureTarget, capture: HistoricalSourceCapture
) -> dict[str, Any]:
    if not isinstance(capture, HistoricalSourceCapture) or capture.source != target.source:
        raise _CaptureDispatchError("capture_payload_invalid")
    title = " ".join(str(capture.title or "").split())
    source_text = str(capture.source_text or "").strip()
    if (
        not title
        or len(title) > 500
        or not source_text
        or len(source_text) > _MAX_CAPTURE_TEXT_CHARS
        or not isinstance(capture.metadata, Mapping)
    ):
        raise _CaptureDispatchError("capture_payload_invalid")
    try:
        external_url = canonicalize_url(capture.external_url)
        metadata_bytes = canonical_json_bytes(dict(capture.metadata))
        metadata = json.loads(metadata_bytes)
    except (TypeError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
        raise _CaptureDispatchError("capture_payload_invalid") from exc
    if len(metadata_bytes) > _MAX_CAPTURE_METADATA_BYTES:
        raise _CaptureDispatchError("capture_payload_invalid")
    return {
        "source": capture.source,
        "title": title,
        "external_url": external_url,
        "source_text": source_text,
        "captured_at": str(capture.captured_at or "").strip(),
        "capture_mode": str(capture.capture_mode or "").strip(),
        "source_completeness": str(capture.source_completeness or "").strip(),
        "source_is_truncated": capture.source_is_truncated,
        "metadata": metadata,
    }


def _base_result(
    target: CaptureTarget,
    *,
    attempt_count: int,
    attempted_at: str,
) -> dict[str, Any]:
    return {
        "path": target.path,
        "target_sha256": target.target_sha256,
        "source": target.source,
        "canonical_url": target.canonical_url,
        "source_locator": dict(target.source_locator),
        "attempt_count": attempt_count,
        "attempted_at": attempted_at,
    }


def _failed_result(
    target: CaptureTarget,
    *,
    failure_type: str,
    reason: str,
    attempt_count: int,
    attempted_at: str,
) -> dict[str, Any]:
    return {
        **_base_result(
            target,
            attempt_count=attempt_count,
            attempted_at=attempted_at,
        ),
        "status": "failed",
        "failure": {"type": failure_type, "reason": reason},
    }


def _capture_one(
    target: CaptureTarget,
    *,
    allowed_hosts: frozenset[str],
    timeout: int,
    dispatcher: CaptureDispatcher,
    robots_cache: _RobotsPolicyCache,
    attempt_count: int,
    attempted_at: str,
    per_host_concurrency: int,
    host_semaphores: dict[str, threading.BoundedSemaphore],
    semaphore_lock: threading.Lock,
) -> dict[str, Any]:
    try:
        host = _target_host(target, allowed_hosts)
    except (_CaptureDispatchError, UnicodeError) as exc:
        return _failed_result(
            target,
            failure_type="dispatch_error",
            reason=_safe_failure_reason(exc, "source_dispatch_invalid"),
            attempt_count=attempt_count,
            attempted_at=attempted_at,
        )
    with semaphore_lock:
        semaphore = host_semaphores.setdefault(
            host, threading.BoundedSemaphore(per_host_concurrency)
        )
    try:
        with semaphore:
            if target.source == "blogs_podcasts":
                robots_source_url = _blog_transport_url(target, allowed_hosts)
                allowed, failure_type, reason = robots_cache.allowed(
                    host=host,
                    source_url=robots_source_url,
                    allowed_hosts=allowed_hosts,
                    timeout=timeout,
                )
                if not allowed:
                    return _failed_result(
                        target,
                        failure_type=failure_type,
                        reason=reason,
                        attempt_count=attempt_count,
                        attempted_at=attempted_at,
                    )
            capture = dispatcher(target, allowed_hosts, timeout)
        payload = _capture_payload(target, capture)
    except HistoricalSourceFetchError as exc:
        return _failed_result(
            target,
            failure_type="source_fetch_error",
            reason=_safe_failure_reason(exc, "source_request_failed"),
            attempt_count=attempt_count,
            attempted_at=attempted_at,
        )
    except _CaptureDispatchError as exc:
        return _failed_result(
            target,
            failure_type="dispatch_error",
            reason=_safe_failure_reason(exc, "source_dispatch_invalid"),
            attempt_count=attempt_count,
            attempted_at=attempted_at,
        )
    except Exception:
        return _failed_result(
            target,
            failure_type="unexpected_fetch_error",
            reason="unexpected_fetch_error",
            attempt_count=attempt_count,
            attempted_at=attempted_at,
        )
    return {
        **_base_result(
            target,
            attempt_count=attempt_count,
            attempted_at=attempted_at,
        ),
        "status": "captured",
        "capture": payload,
    }


def _capture_arxiv_batches(
    targets: Sequence[CaptureTarget],
    *,
    timeout: int,
    attempt_counts: Mapping[tuple[str, str], int],
    attempted_at: str,
) -> dict[tuple[str, str], dict[str, Any]]:
    results: dict[tuple[str, str], dict[str, Any]] = {}
    valid: list[tuple[CaptureTarget, str]] = []

    def attempt_count(target: CaptureTarget) -> int:
        return attempt_counts[(target.path, target.target_sha256)]

    for target in targets:
        try:
            if str(target.source_locator.get("kind") or "").casefold() != "arxiv":
                raise _CaptureDispatchError("source_locator_invalid")
            identifier = _required_locator_text(target, "arxiv_id")
        except _CaptureDispatchError as exc:
            results[(target.path, target.target_sha256)] = _failed_result(
                target,
                failure_type="dispatch_error",
                reason=_safe_failure_reason(exc, "source_locator_invalid"),
                attempt_count=attempt_count(target),
                attempted_at=attempted_at,
            )
        else:
            valid.append((target, identifier))

    request_count = 0

    def fetch_batch(batch: Sequence[tuple[CaptureTarget, str]]) -> None:
        nonlocal request_count
        if request_count:
            time.sleep(_ARXIV_BATCH_INTERVAL_SECONDS)
        request_count += 1
        identifiers = [identifier for _target, identifier in batch]
        try:
            captures = fetch_arxiv_sources(identifiers, timeout=timeout)
            if len(captures) != len(batch):
                raise HistoricalSourceFetchError("source_identity_mismatch")
        except HistoricalSourceFetchError as exc:
            reason = _safe_failure_reason(exc, "source_request_failed")
            if reason in {
                "source_identity_mismatch",
                "source_record_not_found",
            } and len(batch) > 1:
                midpoint = len(batch) // 2
                fetch_batch(batch[:midpoint])
                fetch_batch(batch[midpoint:])
                return
            for target, _identifier in batch:
                results[(target.path, target.target_sha256)] = _failed_result(
                    target,
                    failure_type="source_fetch_error",
                    reason=reason,
                    attempt_count=attempt_count(target),
                    attempted_at=attempted_at,
                )
            return
        except Exception:
            for target, _identifier in batch:
                results[(target.path, target.target_sha256)] = _failed_result(
                    target,
                    failure_type="unexpected_fetch_error",
                    reason="unexpected_fetch_error",
                    attempt_count=attempt_count(target),
                    attempted_at=attempted_at,
                )
            return
        for (target, _identifier), capture in zip(batch, captures, strict=True):
            try:
                payload = _capture_payload(target, capture)
            except _CaptureDispatchError as exc:
                result = _failed_result(
                    target,
                    failure_type="dispatch_error",
                    reason=_safe_failure_reason(exc, "capture_payload_invalid"),
                    attempt_count=attempt_count(target),
                    attempted_at=attempted_at,
                )
            except Exception:
                result = _failed_result(
                    target,
                    failure_type="unexpected_fetch_error",
                    reason="unexpected_fetch_error",
                    attempt_count=attempt_count(target),
                    attempted_at=attempted_at,
                )
            else:
                result = {
                    **_base_result(
                        target,
                        attempt_count=attempt_count(target),
                        attempted_at=attempted_at,
                    ),
                    "status": "captured",
                    "capture": payload,
                }
            results[(target.path, target.target_sha256)] = result

    for offset in range(0, len(valid), _ARXIV_BATCH_SIZE):
        fetch_batch(valid[offset : offset + _ARXIV_BATCH_SIZE])
    return results


def _validated_runtime_bounds(
    *, concurrency: int, per_host_concurrency: int, timeout: int
) -> tuple[int, int, int]:
    values = (concurrency, per_host_concurrency, timeout)
    if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
        raise HistoricalCaptureJobError("capture_bounds_invalid")
    if not 1 <= concurrency <= MAX_CONCURRENCY:
        raise HistoricalCaptureJobError("capture_bounds_invalid")
    if not 1 <= per_host_concurrency <= min(MAX_PER_HOST_CONCURRENCY, concurrency):
        raise HistoricalCaptureJobError("capture_bounds_invalid")
    if not 1 <= timeout <= MAX_TIMEOUT:
        raise HistoricalCaptureJobError("capture_bounds_invalid")
    return concurrency, per_host_concurrency, timeout


def _validated_resume_results(
    audit: Mapping[str, Any] | None,
) -> dict[tuple[str, str], dict[str, Any]]:
    if audit is None:
        return {}
    if (
        audit.get("schema") != CAPTURE_AUDIT_SCHEMA
        or audit.get("version") != CAPTURE_AUDIT_VERSION
    ):
        raise HistoricalCaptureJobError("resume_audit_invalid")
    results = audit.get("results")
    if not isinstance(results, list) or audit.get("results_sha256") != sha256_digest(results):
        raise HistoricalCaptureJobError("resume_audit_invalid")
    validated: dict[tuple[str, str], dict[str, Any]] = {}
    for raw in results:
        if not isinstance(raw, Mapping) or raw.get("status") not in {
            "captured",
            "failed",
        }:
            raise HistoricalCaptureJobError("resume_audit_invalid")
        path = str(raw.get("path") or "")
        digest = str(raw.get("target_sha256") or "")
        raw_attempt_count = raw.get("attempt_count", 1)
        raw_attempted_at = raw.get("attempted_at")
        if (
            not path
            or _SHA256_HEX.fullmatch(digest) is None
            or isinstance(raw_attempt_count, bool)
            or not isinstance(raw_attempt_count, int)
            or raw_attempt_count < 0
            or (
                raw_attempted_at is not None
                and not _is_timezone_aware_timestamp(raw_attempted_at)
            )
            or (
                raw.get("status") == "captured"
                and not isinstance(raw.get("capture"), Mapping)
            )
            or (
                raw.get("status") == "failed"
                and not isinstance(raw.get("failure"), Mapping)
            )
        ):
            raise HistoricalCaptureJobError("resume_audit_invalid")
        key = (path, digest)
        if key in validated:
            raise HistoricalCaptureJobError("resume_audit_invalid")
        normalized = {str(name): value for name, value in raw.items()}
        normalized["attempt_count"] = raw_attempt_count
        validated[key] = normalized
    return validated


def _validated_resume_successes(
    audit: Mapping[str, Any] | None,
) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        key: result
        for key, result in _validated_resume_results(audit).items()
        if result.get("status") == "captured"
    }


def run_historical_capture_job(
    inventory: Mapping[str, Any],
    *,
    sources: Iterable[str] | None = None,
    filter_text: str = "",
    limit: int = DEFAULT_LIMIT,
    blog_allowed_hosts: Iterable[str] = (),
    concurrency: int = DEFAULT_CONCURRENCY,
    per_host_concurrency: int = DEFAULT_PER_HOST_CONCURRENCY,
    timeout: int = DEFAULT_TIMEOUT,
    resume_audit: Mapping[str, Any] | None = None,
    dispatcher: CaptureDispatcher | None = None,
    robots_checker: RobotsChecker | None = None,
) -> dict[str, Any]:
    """Capture a bounded batch while keeping every target outcome isolated."""

    attempted_at = _now_iso()
    concurrency, per_host_concurrency, timeout = _validated_runtime_bounds(
        concurrency=concurrency,
        per_host_concurrency=per_host_concurrency,
        timeout=timeout,
    )
    source_filter = _validated_sources(sources)
    folded_filter = _selection_filter(filter_text)
    maximum = _validated_limit(limit)
    all_targets = _eligible_capture_targets(inventory)
    all_targets_by_key = {
        (target.path, target.target_sha256): target for target in all_targets
    }
    eligible_targets = _eligible_capture_targets(
        inventory,
        sources=source_filter,
        filter_text=folded_filter,
    )
    raw_hosts = tuple(blog_allowed_hosts)
    allowed_hosts = (
        _normalized_allowed_hosts(raw_hosts) if raw_hosts else frozenset()
    )
    previous_results = _validated_resume_results(resume_audit)
    if resume_audit is not None and resume_audit.get(
        "inventory_entries_sha256"
    ) != inventory.get("entries_sha256"):
        raise HistoricalCaptureJobError("resume_audit_invalid")
    for key, previous in previous_results.items():
        target = all_targets_by_key.get(key)
        if target is None or any(
            previous.get(field) != expected
            for field, expected in (
                ("path", target.path),
                ("target_sha256", target.target_sha256),
                ("source", target.source),
                ("canonical_url", target.canonical_url),
                ("source_locator", target.source_locator),
            )
        ):
            raise HistoricalCaptureJobError("resume_audit_invalid")
    retained: dict[tuple[str, str], dict[str, Any]] = dict(previous_results)
    never_attempted: list[CaptureTarget] = []
    failed_retries: list[CaptureTarget] = []
    skipped_success_count = 0
    for target in eligible_targets:
        key = (target.path, target.target_sha256)
        previous = previous_results.get(key)
        if previous is None:
            never_attempted.append(target)
        else:
            retained[key] = previous
            if previous.get("status") == "captured":
                skipped_success_count += 1
            else:
                failed_retries.append(target)
    # A permanent failure must not starve unseen inventory rows. Retry old
    # failures only after the never-attempted queue has advanced.
    failed_retries.sort(
        key=lambda target: (
            int(
                previous_results[(target.path, target.target_sha256)][
                    "attempt_count"
                ]
            ),
            target.path,
            target.target_sha256,
        )
    )
    pending = (never_attempted + failed_retries)[:maximum]
    attempt_counts = {
        (target.path, target.target_sha256): int(
            previous_results.get(
                (target.path, target.target_sha256), {"attempt_count": 0}
            )["attempt_count"]
        )
        + 1
        for target in pending
    }

    selected_dispatcher = dispatcher or _default_dispatcher
    robots_cache = _RobotsPolicyCache(robots_checker or load_blog_robots_policy)
    host_semaphores: dict[str, threading.BoundedSemaphore] = {}
    semaphore_lock = threading.Lock()
    captured_now: dict[tuple[str, str], dict[str, Any]] = {}
    if dispatcher is None:
        arxiv_pending = [target for target in pending if target.source == "arxiv"]
        threaded_pending = [target for target in pending if target.source != "arxiv"]
        captured_now.update(
            _capture_arxiv_batches(
                arxiv_pending,
                timeout=timeout,
                attempt_counts=attempt_counts,
                attempted_at=attempted_at,
            )
        )
    else:
        threaded_pending = pending
    if threaded_pending:
        workers = min(concurrency, len(threaded_pending))
        with ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="historical-capture",
        ) as executor:
            futures = [
                executor.submit(
                    _capture_one,
                    target,
                    allowed_hosts=allowed_hosts,
                    timeout=timeout,
                    dispatcher=selected_dispatcher,
                    robots_cache=robots_cache,
                    attempt_count=attempt_counts[
                        (target.path, target.target_sha256)
                    ],
                    attempted_at=attempted_at,
                    per_host_concurrency=per_host_concurrency,
                    host_semaphores=host_semaphores,
                    semaphore_lock=semaphore_lock,
                )
                for target in threaded_pending
            ]
            for target, future in zip(threaded_pending, futures, strict=True):
                try:
                    result = future.result()
                except Exception:
                    result = _failed_result(
                        target,
                        failure_type="unexpected_fetch_error",
                        reason="unexpected_fetch_error",
                        attempt_count=attempt_counts[
                            (target.path, target.target_sha256)
                        ],
                        attempted_at=attempted_at,
                    )
                captured_now[(target.path, target.target_sha256)] = result

    retained.update(captured_now)
    results = [
        retained[(target.path, target.target_sha256)]
        for target in all_targets
        if (target.path, target.target_sha256) in retained
    ]
    captured_count = sum(result["status"] == "captured" for result in results)
    failed_count = len(results) - captured_count
    batch_captured_count = sum(
        result["status"] == "captured" for result in captured_now.values()
    )
    batch_failed_count = len(captured_now) - batch_captured_count
    entries_sha256 = str(inventory.get("entries_sha256") or "")
    return {
        "schema": CAPTURE_AUDIT_SCHEMA,
        "version": CAPTURE_AUDIT_VERSION,
        "generated_at": _now_iso(),
        "inventory_schema": inventory.get("schema"),
        "inventory_version": inventory.get("version"),
        "inventory_entries_sha256": entries_sha256,
        "selection": {
            "sources": sorted(source_filter),
            "filter_applied": bool(folded_filter),
            "filter_sha256": sha256_digest(folded_filter),
            "limit": maximum,
            "concurrency": concurrency,
            "per_host_concurrency": per_host_concurrency,
            "timeout_seconds": timeout,
            "blog_allowlist_count": len(allowed_hosts),
            "blog_allowlist_sha256": sha256_digest(sorted(allowed_hosts)),
        },
        "eligible_count": len(eligible_targets),
        "selected_count": len(pending),
        "attempted_count": len(pending),
        "skipped_success_count": skipped_success_count,
        "batch_captured_count": batch_captured_count,
        "batch_failed_count": batch_failed_count,
        "captured_count": captured_count,
        "failed_count": failed_count,
        "results_sha256": sha256_digest(results),
        "results": results,
    }


def load_capture_audit(path: str | Path) -> dict[str, Any]:
    audit = dict(_read_json_file(path, maximum_bytes=_MAX_INPUT_BYTES))
    _validated_resume_successes(audit)
    return audit


def write_capture_audit(path: str | Path, audit: Mapping[str, Any]) -> None:
    """Atomically write evidence with an exact owner-read/write mode."""

    destination = Path(path).absolute()
    if destination.suffix.casefold() != ".json":
        raise HistoricalCaptureJobError("capture_output_invalid")
    _validated_resume_successes(audit)
    _reject_symlink_components(destination)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    except OSError as exc:
        raise HistoricalCaptureJobError("capture_output_invalid") from exc
    _reject_symlink_components(destination)
    if destination.exists() and not destination.is_file():
        raise HistoricalCaptureJobError("capture_output_invalid")
    data = (
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")
    if len(data) > _MAX_INPUT_BYTES:
        raise HistoricalCaptureJobError("capture_output_too_large")
    temporary = destination.parent / f".{destination.name}.{uuid.uuid4().hex}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(temporary, flags, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory = os.open(destination.parent, directory_flags)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise HistoricalCaptureJobError("capture_output_invalid") from exc


def capture_audit_summary(
    audit: Mapping[str, Any], *, write_performed: bool
) -> dict[str, Any]:
    """Return a body-free, URL-free receipt suitable for CI logs."""

    return {
        "schema": audit.get("schema"),
        "version": audit.get("version"),
        "dry_run": not write_performed,
        "write_performed": write_performed,
        "selected_count": audit.get("selected_count"),
        "attempted_count": audit.get("attempted_count"),
        "skipped_success_count": audit.get("skipped_success_count"),
        "captured_count": audit.get("captured_count"),
        "failed_count": audit.get("failed_count"),
        "results_sha256": audit.get("results_sha256"),
    }


__all__ = [
    "BLOG_ALLOWLIST_SCHEMA",
    "BLOG_ALLOWLIST_VERSION",
    "CAPTURE_AUDIT_SCHEMA",
    "CAPTURE_AUDIT_VERSION",
    "CaptureTarget",
    "HistoricalCaptureJobError",
    "capture_audit_summary",
    "load_blog_allowlist",
    "load_blog_robots_policy",
    "load_capture_audit",
    "load_historical_capture_inventory",
    "run_historical_capture_job",
    "select_capture_targets",
    "write_capture_audit",
]
