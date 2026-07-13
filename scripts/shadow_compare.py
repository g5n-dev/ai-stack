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
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path


class ShadowComparisonError(RuntimeError):
    """Raised when a build tree cannot be safely inspected."""


_GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_MAX_FILES = 200_000
_MAX_FILE_BYTES = 128 * 1024 * 1024
_MAX_TOTAL_BYTES = 10 * 1024 * 1024 * 1024
_MAX_DIFFERENCES = 500


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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        report = compare_trees(
            args.baseline,
            args.candidate,
            code_sha=args.code_sha,
            content_sha=args.content_sha,
        )
        _atomic_json(args.report, report)
    except (OSError, ShadowComparisonError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["matches"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
