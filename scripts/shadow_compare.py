"""Byte-exact comparison gate for legacy and external-ledger site builds."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path

from ai_stack._json import canonical_json_bytes
from ai_stack.shadow_evidence import (
    ShadowEvidenceError,
    append_shadow_evidence,
)


class ShadowComparisonError(RuntimeError):
    """Raised when a build tree cannot be safely inspected."""


_GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_MAX_FILES = 200_000
_MAX_FILE_BYTES = 128 * 1024 * 1024
_MAX_TOTAL_BYTES = 10 * 1024 * 1024 * 1024
_MAX_DIFFERENCES = 500
_MAX_SUMMARY_DIFFERENCES = 20


class _ExternalLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: set[str] = set()

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        interesting = {
            "a": {"href"},
            "img": {"src", "srcset"},
            "script": {"src"},
            "link": {"href"},
            "iframe": {"src"},
            "form": {"action"},
        }.get(tag.casefold(), set())
        for name, value in attrs:
            if name.casefold() not in interesting or value is None:
                continue
            candidates = value.split(",") if name.casefold() == "srcset" else [value]
            for candidate in candidates:
                url = candidate.strip().split(maxsplit=1)[0]
                if url.startswith(("https://", "http://", "//")):
                    self.links.add(url)

    handle_startendtag = handle_starttag


@dataclass(frozen=True)
class _Tree:
    files: dict[str, tuple[int, str]]
    tree_sha256: str
    html_count: int
    external_links: frozenset[str]


def _inspect_tree(root: Path | str) -> _Tree:
    source = Path(root).absolute()
    try:
        details = source.lstat()
    except OSError as exc:
        raise ShadowComparisonError(f"build root is unreadable: {source}") from exc
    if source.is_symlink() or not stat.S_ISDIR(details.st_mode):
        raise ShadowComparisonError("build root must be a regular directory")

    files: dict[str, tuple[int, str]] = {}
    external_links: set[str] = set()
    total_bytes = 0
    html_count = 0
    for candidate in sorted(source.rglob("*"), key=lambda path: path.as_posix()):
        if candidate.is_symlink():
            raise ShadowComparisonError(f"build tree contains symlink: {candidate}")
        if candidate.is_dir():
            continue
        try:
            item = candidate.lstat()
        except OSError as exc:
            raise ShadowComparisonError(f"build file is unreadable: {candidate}") from exc
        if not stat.S_ISREG(item.st_mode) or item.st_nlink != 1:
            raise ShadowComparisonError(f"build tree contains non-regular file: {candidate}")
        if item.st_size > _MAX_FILE_BYTES:
            raise ShadowComparisonError(f"build file exceeds size limit: {candidate}")
        if len(files) >= _MAX_FILES:
            raise ShadowComparisonError("build tree exceeds file-count limit")
        total_bytes += item.st_size
        if total_bytes > _MAX_TOTAL_BYTES:
            raise ShadowComparisonError("build tree exceeds total-size limit")

        relative = candidate.relative_to(source).as_posix()
        payload = candidate.read_bytes()
        if len(payload) != item.st_size:
            raise ShadowComparisonError(f"build file changed while reading: {relative}")
        files[relative] = (len(payload), sha256(payload).hexdigest())
        if candidate.suffix.casefold() == ".html":
            html_count += 1
            try:
                text = payload.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ShadowComparisonError(f"HTML is not UTF-8: {relative}") from exc
            parser = _ExternalLinkParser()
            try:
                parser.feed(text)
                parser.close()
            except Exception as exc:
                raise ShadowComparisonError(f"HTML parsing failed: {relative}") from exc
            external_links.update(parser.links)

    manifest = {
        "schema_version": "shadow_tree_v1",
        "files": [
            {"path": path, "bytes": size, "sha256": digest}
            for path, (size, digest) in sorted(files.items())
        ],
    }
    canonical = json.dumps(
        manifest,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _Tree(
        files=files,
        tree_sha256=sha256(canonical).hexdigest(),
        html_count=html_count,
        external_links=frozenset(external_links),
    )


def compare_trees(
    baseline_root: Path | str,
    candidate_root: Path | str,
    *,
    code_sha: str | None = None,
    content_sha: str | None = None,
) -> dict[str, object]:
    """Compare two safe static trees and return a canonical evidence report."""

    for field_name, value in (("code_sha", code_sha), ("content_sha", content_sha)):
        if value is not None and not _GIT_SHA.fullmatch(value):
            raise ShadowComparisonError(f"{field_name} must be a full Git object ID")
    baseline = _inspect_tree(baseline_root)
    candidate = _inspect_tree(candidate_root)
    baseline_paths = set(baseline.files)
    candidate_paths = set(candidate.files)
    missing = sorted(baseline_paths.difference(candidate_paths))
    extra = sorted(candidate_paths.difference(baseline_paths))
    changed = sorted(
        path
        for path in baseline_paths.intersection(candidate_paths)
        if baseline.files[path] != candidate.files[path]
    )
    links_match = baseline.external_links == candidate.external_links
    matches = not missing and not extra and not changed and links_match
    report: dict[str, object] = {
        "schema_version": "shadow_compare_v1",
        "matches": matches,
        "code_sha": code_sha,
        "content_sha": content_sha,
        "file_count": len(baseline.files) if matches else None,
        "html_count": baseline.html_count if matches else None,
        "baseline_file_count": len(baseline.files),
        "candidate_file_count": len(candidate.files),
        "baseline_html_count": baseline.html_count,
        "candidate_html_count": candidate.html_count,
        "baseline_tree_sha256": baseline.tree_sha256,
        "candidate_tree_sha256": candidate.tree_sha256,
        "external_links_match": links_match,
        "external_links": sorted(baseline.external_links) if links_match else None,
        "baseline_external_links": sorted(baseline.external_links),
        "candidate_external_links": sorted(candidate.external_links),
        "missing_path_count": len(missing),
        "extra_path_count": len(extra),
        "changed_path_count": len(changed),
        "missing_paths": missing[:_MAX_DIFFERENCES],
        "extra_paths": extra[:_MAX_DIFFERENCES],
        "changed_paths": changed[:_MAX_DIFFERENCES],
        "differences_truncated": any(
            len(paths) > _MAX_DIFFERENCES for paths in (missing, extra, changed)
        ),
    }
    return report


def summarize_report(
    report: dict[str, object],
    *,
    record_digest: str | None,
) -> dict[str, object]:
    """Return a bounded log-safe view while preserving the full report on disk."""

    def difference_list(field: str) -> list[object]:
        value = report.get(field)
        return value[:_MAX_SUMMARY_DIFFERENCES] if isinstance(value, list) else []

    external_links = report.get("external_links")
    baseline_links = report.get("baseline_external_links")
    candidate_links = report.get("candidate_external_links")
    difference_counts = {
        field: report.get(field)
        for field in ("missing_path_count", "extra_path_count", "changed_path_count")
    }
    summary_truncated = bool(report.get("differences_truncated")) or any(
        isinstance(count, int) and count > _MAX_SUMMARY_DIFFERENCES
        for count in difference_counts.values()
    )
    report_digest = "sha256:" + sha256(canonical_json_bytes(report) + b"\n").hexdigest()
    return {
        "schema_version": "shadow_compare_summary_v1",
        "report_schema_version": report.get("schema_version"),
        "matches": report.get("matches"),
        "code_sha": report.get("code_sha"),
        "content_sha": report.get("content_sha"),
        "file_count": report.get("file_count"),
        "html_count": report.get("html_count"),
        "baseline_file_count": report.get("baseline_file_count"),
        "candidate_file_count": report.get("candidate_file_count"),
        "baseline_html_count": report.get("baseline_html_count"),
        "candidate_html_count": report.get("candidate_html_count"),
        "baseline_tree_sha256": report.get("baseline_tree_sha256"),
        "candidate_tree_sha256": report.get("candidate_tree_sha256"),
        "external_links_match": report.get("external_links_match"),
        "external_link_count": len(external_links) if isinstance(external_links, list) else None,
        "baseline_external_link_count": (
            len(baseline_links) if isinstance(baseline_links, list) else None
        ),
        "candidate_external_link_count": (
            len(candidate_links) if isinstance(candidate_links, list) else None
        ),
        **difference_counts,
        "missing_paths": difference_list("missing_paths"),
        "extra_paths": difference_list("extra_paths"),
        "changed_paths": difference_list("changed_paths"),
        "differences_truncated": summary_truncated,
        "report_digest": report_digest,
        "record_digest": record_digest,
    }


def _atomic_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary_name = handle.name
            os.chmod(handle.name, 0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--code-sha")
    parser.add_argument("--content-sha")
    parser.add_argument("--evidence-root", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--completed-at")
    parser.add_argument("--full-build", action="store_true")
    parser.add_argument("--expected-previous-digest")
    return parser


def _evidence_time(value: str) -> datetime:
    if not value.endswith("Z"):
        raise ShadowComparisonError("--completed-at must be a UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ShadowComparisonError("--completed-at is invalid") from exc
    if parsed.isoformat().replace("+00:00", "Z") != value:
        raise ShadowComparisonError("--completed-at must be canonical")
    return parsed


def _validate_evidence_args(args: argparse.Namespace) -> datetime | None:
    optional_evidence = (
        args.run_id,
        args.completed_at,
        args.expected_previous_digest,
        args.full_build,
    )
    if args.evidence_root is None:
        if any(optional_evidence):
            raise ShadowComparisonError("shadow evidence options require --evidence-root")
        return None
    missing = [
        flag
        for flag, value in (
            ("--run-id", args.run_id),
            ("--completed-at", args.completed_at),
            ("--code-sha", args.code_sha),
            ("--content-sha", args.content_sha),
        )
        if value is None
    ]
    if missing:
        raise ShadowComparisonError("--evidence-root requires " + ", ".join(missing))
    assert isinstance(args.completed_at, str)
    return _evidence_time(args.completed_at)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    record_digest: str | None = None
    try:
        completed_at = _validate_evidence_args(args)
        report = compare_trees(
            args.baseline,
            args.candidate,
            code_sha=args.code_sha,
            content_sha=args.content_sha,
        )
        _atomic_json(args.report, report)
        if args.evidence_root is not None:
            assert completed_at is not None
            assert isinstance(args.run_id, str)
            assert isinstance(args.code_sha, str)
            assert isinstance(args.content_sha, str)
            record = append_shadow_evidence(
                args.evidence_root,
                report=report,
                run_id=args.run_id,
                completed_at=completed_at,
                full_build=args.full_build,
                code_sha=args.code_sha,
                content_sha=args.content_sha,
                expected_previous_digest=args.expected_previous_digest,
            )
            record_digest = record.record_digest
    except (OSError, ShadowComparisonError, ShadowEvidenceError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1
    print(
        json.dumps(
            summarize_report(report, record_digest=record_digest),
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if report["matches"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
