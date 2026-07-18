"""Pure-offline inventory for evidence-based historical content recovery.

The inventory never fetches a source and never rewrites Markdown.  It records
the exact current file digest, provenance class, canonical source URL and the
minimum stable locator required by a later, separately reviewed recovery job.
For archived Hacker News entries only, the locator may be read from one pinned
local Git revision.  Lazy object fetching is explicitly disabled, so a missing
local blob becomes a typed outcome instead of network traffic.
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
import subprocess
from collections import Counter
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

from ._json import sha256_digest
from .content_quality import (
    HISTORICAL_RECOVERY_FAILURE_TYPES,
    analyze_post,
    is_curated_evidence_backed_rewrite,
    is_evidence_backed_rewrite,
    is_source_brief,
    is_terminal_recovery_failure_archive,
    markdown_body,
    markdown_frontmatter,
)
from .identity import canonicalize_url

HISTORICAL_REHYDRATION_SCHEMA = "ai_stack.historical_rehydration.inventory"
HISTORICAL_REHYDRATION_VERSION = 1
PINNED_HN_HISTORY_REVISION = "b71a275de15c8ee27f6f0428b4bac901d63001f6"

_MAX_MARKDOWN_BYTES = 2 * 1024 * 1024
_SOURCE_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ARXIV_PATH_RE = re.compile(r"^/(?:abs|pdf)/(?P<arxiv_id>[^/?#]+?)(?:\.pdf)?/?$")
_JUEJIN_PATH_RE = re.compile(r"^/post/(?P<article_id>\d+)/?$")
_HN_URL_RE = re.compile(
    r"(?:"
    r"https?://news\.ycombinator\.com/item\?[^\s)>#]*\bid=(?P<news_id>\d+)"
    r"|https?://hacker-news\.firebaseio\.com/v0/item/(?P<api_id>\d+)\.json"
    r")",
    re.IGNORECASE,
)
_FENCE_LINE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<tail>.*)$")
_CLASSIFICATIONS = (
    "needs_source_recovery",
    "terminal_unrecoverable",
    "verified_rewrite",
    "verified_source_brief",
)


class HistoricalRehydrationError(ValueError):
    """Raised when the inventory root itself cannot be scanned safely."""


def _regular_markdown_files(root: Path) -> tuple[list[Path], list[str]]:
    if root.is_symlink() or not root.is_dir():
        raise HistoricalRehydrationError(
            f"historical rehydration root must be a regular directory: {root}"
        )
    paths: list[Path] = []
    symlinks: list[str] = []
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            candidate = current_path / name
            if candidate.is_symlink():
                symlinks.append(candidate.relative_to(root).as_posix())
            else:
                retained_directories.append(name)
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            candidate = current_path / name
            details = candidate.lstat()
            relative = candidate.relative_to(root).as_posix()
            if candidate.is_symlink() or not stat.S_ISREG(details.st_mode):
                symlinks.append(relative)
                continue
            if candidate.suffix.casefold() != ".md":
                continue
            if details.st_size > _MAX_MARKDOWN_BYTES:
                raise HistoricalRehydrationError(f"historical Markdown is too large: {relative}")
            paths.append(candidate)
    return (
        sorted(paths, key=lambda path: path.relative_to(root).as_posix()),
        sorted(symlinks),
    )


def _canonical_url(metadata: Mapping[str, Any]) -> tuple[str, str | None]:
    value = metadata.get("external_url")
    if not isinstance(value, str):
        return "", "external_url_missing"
    try:
        return canonicalize_url(value), None
    except ValueError:
        return "", "external_url_invalid"


def _verified_modern_source_brief(metadata: Mapping[str, Any], body: str) -> bool:
    return (
        str(metadata.get("content_mode") or "").strip().casefold() == "source_brief"
        and str(metadata.get("publication_tier") or "").strip() == "C"
        and bool(
            _SOURCE_DIGEST_RE.fullmatch(str(metadata.get("source_snapshot_sha256") or "").strip())
        )
        and str(metadata.get("extractor_version") or "").strip() == "source-contract-v1"
        and metadata.get("source_support") == 1.0
        and is_source_brief(metadata, body)
    )


def _classification(metadata: Mapping[str, Any], body: str, current_status: str) -> str:
    if current_status == "archived" and is_terminal_recovery_failure_archive(metadata, body):
        return "terminal_unrecoverable"
    if current_status == "source_brief" and _verified_modern_source_brief(metadata, body):
        return "verified_source_brief"
    declared_mode = str(metadata.get("content_mode") or "").strip().casefold()
    if current_status == "complete" and declared_mode == "evidence_backed_rewrite":
        if is_evidence_backed_rewrite(metadata, body) or is_curated_evidence_backed_rewrite(
            metadata, body
        ):
            return "verified_rewrite"
    return "needs_source_recovery"


def _unfenced_lines(document: str) -> tuple[str, ...]:
    result: list[str] = []
    open_character: str | None = None
    open_length = 0
    for line in str(document or "").splitlines():
        match = _FENCE_LINE_RE.match(line)
        if match is not None:
            fence = match.group("fence")
            character = fence[0]
            if open_character is None:
                open_character = character
                open_length = len(fence)
            elif (
                character == open_character
                and len(fence) >= open_length
                and not match.group("tail").strip()
            ):
                open_character = None
                open_length = 0
            continue
        if open_character is None:
            result.append(line)
    return tuple(result)


def _hn_ids(document: str, metadata: Mapping[str, Any]) -> tuple[str, ...]:
    values: set[str] = set()
    native_id = str(metadata.get("hn_id") or "").strip()
    if native_id.isdigit():
        values.add(native_id)
    lines = _unfenced_lines(document)
    discussion_lines = [line for line in lines if "hn 讨论" in line.casefold()]
    searchable = "\n".join(discussion_lines or lines)
    for match in _HN_URL_RE.finditer(searchable):
        value = match.group("news_id") or match.group("api_id") or ""
        if value.isdigit():
            values.add(value)
    return tuple(sorted(values, key=lambda value: (int(value), value)))


class _OfflineGitReader:
    """Read a pinned local Git blob without allowing promisor lazy fetches."""

    def __init__(self, repository_root: Path, revision: str) -> None:
        self.repository_root = repository_root
        self.revision = revision
        self._revision_available: bool | None = None

    @staticmethod
    def _environment() -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_NO_LAZY_FETCH": "1",
                "GIT_TERMINAL_PROMPT": "0",
            }
        )
        return environment

    def _run(self, *args: str) -> subprocess.CompletedProcess[bytes]:
        try:
            return subprocess.run(
                [
                    "git",
                    "--no-optional-locks",
                    "-C",
                    str(self.repository_root),
                    *args,
                ],
                check=False,
                capture_output=True,
                timeout=10,
                env=self._environment(),
            )
        except (OSError, subprocess.TimeoutExpired):
            return subprocess.CompletedProcess(args=args, returncode=127, stdout=b"", stderr=b"")

    def revision_available(self) -> bool:
        if self._revision_available is None:
            completed = self._run(
                "rev-parse",
                "--verify",
                "--quiet",
                f"{self.revision}^{{commit}}",
            )
            self._revision_available = completed.returncode == 0
        return self._revision_available

    def read_document(self, repository_relative_path: str) -> tuple[str | None, str]:
        if not self.revision_available():
            return None, "hn_git_revision_unavailable"
        spec = f"{self.revision}:{repository_relative_path}"
        resolved = self._run("rev-parse", "--verify", "--quiet", spec)
        if resolved.returncode != 0:
            return None, "hn_git_path_unavailable"
        try:
            blob_id = resolved.stdout.decode("ascii").strip()
        except UnicodeDecodeError:
            return None, "hn_git_blob_unavailable"
        if not re.fullmatch(r"[0-9a-f]{40,64}", blob_id):
            return None, "hn_git_blob_unavailable"
        blob_type = self._run("cat-file", "-t", blob_id)
        if blob_type.returncode != 0 or blob_type.stdout.strip() != b"blob":
            return None, "hn_git_blob_unavailable"
        size = self._run("cat-file", "-s", blob_id)
        try:
            byte_count = int(size.stdout.strip()) if size.returncode == 0 else -1
        except ValueError:
            byte_count = -1
        if byte_count < 0 or byte_count > _MAX_MARKDOWN_BYTES:
            return None, "hn_git_blob_size_invalid"
        blob = self._run("cat-file", "blob", blob_id)
        if blob.returncode != 0 or len(blob.stdout) != byte_count:
            return None, "hn_git_blob_unavailable"
        try:
            return blob.stdout.decode("utf-8"), "resolved"
        except UnicodeDecodeError:
            return None, "hn_git_blob_invalid_utf8"


def _simple_locator(source: str, canonical_url: str) -> dict[str, Any]:
    parsed = urlsplit(canonical_url)
    hostname = (parsed.hostname or "").casefold()
    if source == "arxiv":
        match = _ARXIV_PATH_RE.fullmatch(parsed.path)
        if hostname not in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"} or match is None:
            return {
                "kind": "arxiv",
                "status": "arxiv_id_missing",
                "origin": "canonical_url",
            }
        return {
            "kind": "arxiv",
            "status": "resolved",
            "arxiv_id": match.group("arxiv_id"),
            "origin": "canonical_url",
        }
    if source == "github_trending":
        parts = [part for part in parsed.path.split("/") if part]
        if hostname != "github.com" or len(parts) != 2:
            return {
                "kind": "github",
                "status": "github_repository_missing",
                "origin": "canonical_url",
            }
        repository = parts[1][:-4] if parts[1].casefold().endswith(".git") else parts[1]
        if not parts[0] or not repository:
            return {
                "kind": "github",
                "status": "github_repository_missing",
                "origin": "canonical_url",
            }
        return {
            "kind": "github",
            "status": "resolved",
            "owner": parts[0],
            "repo": repository,
            "origin": "canonical_url",
        }
    if source == "juejin":
        match = _JUEJIN_PATH_RE.fullmatch(parsed.path)
        if hostname not in {"juejin.cn", "www.juejin.cn"} or match is None:
            return {
                "kind": "juejin",
                "status": "juejin_article_id_missing",
                "origin": "canonical_url",
            }
        return {
            "kind": "juejin",
            "status": "resolved",
            "article_id": match.group("article_id"),
            "origin": "canonical_url",
        }
    if source == "blogs_podcasts":
        return {
            "kind": "external_url",
            "status": "resolved",
            "origin": "canonical_url",
        }
    return {
        "kind": "external_url",
        "status": "unsupported_source",
        "origin": "canonical_url",
    }


def _hn_locator(
    *,
    document: str,
    metadata: Mapping[str, Any],
    current_status: str,
    repository_relative_path: str | None,
    git_reader: _OfflineGitReader,
) -> dict[str, Any]:
    current_ids = _hn_ids(document, metadata)
    if len(current_ids) == 1:
        return {
            "kind": "hacker_news",
            "status": "resolved",
            "hn_id": current_ids[0],
            "origin": "current_document",
        }
    if len(current_ids) > 1:
        return {
            "kind": "hacker_news",
            "status": "hn_id_ambiguous_in_current_document",
            "origin": "current_document",
            "candidate_count": len(current_ids),
        }
    if current_status != "archived":
        return {
            "kind": "hacker_news",
            "status": "hn_id_missing_in_current_document",
            "origin": "current_document",
        }
    base = {
        "kind": "hacker_news",
        "origin": "pinned_git_history",
        "git_revision": git_reader.revision,
    }
    if repository_relative_path is None:
        return {**base, "status": "hn_git_path_outside_repository"}
    historical_document, outcome = git_reader.read_document(repository_relative_path)
    if historical_document is None:
        return {**base, "status": outcome}
    historical_metadata = markdown_frontmatter(historical_document)
    historical_ids = _hn_ids(historical_document, historical_metadata)
    if not historical_ids:
        return {**base, "status": "hn_id_missing_in_git_history"}
    if len(historical_ids) > 1:
        return {
            **base,
            "status": "hn_id_ambiguous_in_git_history",
            "candidate_count": len(historical_ids),
        }
    return {
        "kind": "hacker_news",
        "status": "resolved",
        "hn_id": historical_ids[0],
        "origin": "pinned_git_history",
        "git_revision": git_reader.revision,
    }


def build_historical_rehydration_inventory(
    content_root: str | Path,
    *,
    repository_root: str | Path,
    hn_git_revision: str = PINNED_HN_HISTORY_REVISION,
) -> dict[str, Any]:
    """Return a deterministic, read-only historical recovery inventory."""

    root = Path(content_root).absolute()
    repository = Path(repository_root).absolute()
    paths, symlinks = _regular_markdown_files(root)
    git_reader = _OfflineGitReader(repository, hn_git_revision)
    entries: list[dict[str, Any]] = []

    for path in paths:
        relative_path = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        target_sha256 = hashlib.sha256(raw).hexdigest()
        try:
            document = raw.decode("utf-8")
        except UnicodeDecodeError:
            entries.append(
                {
                    "path": relative_path,
                    "target_sha256": target_sha256,
                    "source": "",
                    "canonical_url": "",
                    "current_status": "invalid_document",
                    "current_mode": "invalid_document",
                    "recovery_classification": "needs_source_recovery",
                    "source_locator": {
                        "kind": "unknown",
                        "status": "document_invalid_utf8",
                        "origin": "current_document",
                    },
                }
            )
            continue

        metadata = markdown_frontmatter(document)
        body = markdown_body(document)
        analysis = analyze_post(document)
        source = str(metadata.get("source") or "").strip().casefold()
        canonical_url, url_error = _canonical_url(metadata)
        current_mode = (
            str(metadata.get("content_mode") or "").strip().casefold() or analysis.content_mode
        )
        classification = _classification(metadata, body, analysis.status)

        if url_error is not None:
            locator: dict[str, Any] = {
                "kind": source or "unknown",
                "status": url_error,
                "origin": "current_document",
            }
        elif source == "hacker_news":
            try:
                repository_relative = PurePosixPath(
                    path.relative_to(repository).as_posix()
                ).as_posix()
            except ValueError:
                repository_relative = None
            locator = _hn_locator(
                document=document,
                metadata=metadata,
                current_status=analysis.status,
                repository_relative_path=repository_relative,
                git_reader=git_reader,
            )
        else:
            locator = _simple_locator(source, canonical_url)

        entries.append(
            {
                "path": relative_path,
                "target_sha256": target_sha256,
                "source": source,
                "canonical_url": canonical_url,
                "current_status": analysis.status,
                "current_mode": current_mode,
                "recovery_classification": classification,
                "source_locator": locator,
            }
        )

    classifications = Counter(entry["recovery_classification"] for entry in entries)
    sources = Counter(entry["source"] or "unknown" for entry in entries)
    locator_statuses = Counter(entry["source_locator"]["status"] for entry in entries)
    return {
        "schema": HISTORICAL_REHYDRATION_SCHEMA,
        "version": HISTORICAL_REHYDRATION_VERSION,
        "offline": True,
        "content_root": str(root),
        "hn_git_revision": hn_git_revision,
        "entry_count": len(entries),
        "symlinks_skipped": symlinks,
        "classification_counts": {name: classifications.get(name, 0) for name in _CLASSIFICATIONS},
        "source_counts": dict(sorted(sources.items())),
        "locator_status_counts": dict(sorted(locator_statuses.items())),
        "entries_sha256": sha256_digest(entries),
        "entries": entries,
    }


__all__ = [
    "HISTORICAL_REHYDRATION_SCHEMA",
    "HISTORICAL_REHYDRATION_VERSION",
    "HISTORICAL_RECOVERY_FAILURE_TYPES",
    "PINNED_HN_HISTORY_REVISION",
    "HistoricalRehydrationError",
    "build_historical_rehydration_inventory",
]
