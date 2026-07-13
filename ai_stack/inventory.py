from __future__ import annotations

import json
import os
import re
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterator

from .identity import canonicalize_url
from .stores import UnsafeStorePathError


_EXTERNAL_URL = re.compile(
    r"^\s*(?:external_url|externalUrl|external-url)\s*[:=]\s*(.*?)\s*$"
)
_MAX_FRONTMATTER_BYTES = 512 * 1024


def _markdown_files(root: Path) -> tuple[list[Path], int]:
    if root.is_symlink():
        raise UnsafeStorePathError(f"inventory root must not be a symlink: {root}")
    if not root.is_dir():
        raise FileNotFoundError(f"inventory root is not a directory: {root}")
    files: list[Path] = []
    symlinks = 0
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            path = current_path / name
            if path.is_symlink():
                symlinks += 1
            else:
                retained_directories.append(name)
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            path = current_path / name
            if path.is_symlink():
                symlinks += 1
            elif path.suffix.casefold() == ".md" and path.is_file():
                files.append(path)
    files.sort(key=lambda path: path.relative_to(root).as_posix())
    return files, symlinks


def _frontmatter_lines(path: Path) -> Iterator[str]:
    with path.open("rb") as stream:
        raw = stream.read(_MAX_FRONTMATTER_BYTES + 1)
    if len(raw) > _MAX_FRONTMATTER_BYTES:
        raw = raw[:_MAX_FRONTMATTER_BYTES]
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() not in {"---", "+++"}:
        return
    delimiter = lines[0].strip()
    for line in lines[1:]:
        if line.strip() == delimiter:
            return
        yield line


def _external_url(path: Path) -> str | None:
    for line in _frontmatter_lines(path):
        match = _EXTERNAL_URL.match(line)
        if match is None:
            continue
        value = match.group(1).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1].strip()
        return value or None
    return None


def scan_markdown_inventory(content_root: str | Path, *, dry_run: bool = True) -> dict[str, Any]:
    root = Path(content_root).absolute()
    files, symlinks = _markdown_files(root)
    urls: dict[str, list[str]] = defaultdict(list)
    missing = 0
    invalid: list[dict[str, str]] = []

    for path in files:
        relative = path.relative_to(root).as_posix()
        value = _external_url(path)
        if value is None:
            missing += 1
            continue
        try:
            canonical = canonicalize_url(value)
        except ValueError as error:
            invalid.append({"path": relative, "reason": str(error), "value": value})
            continue
        urls[canonical].append(relative)

    duplicate_groups = [
        {"canonical_url": url, "count": len(paths), "paths": sorted(paths)}
        for url, paths in sorted(urls.items())
        if len(paths) > 1
    ]
    return {
        "schema_version": 1,
        "source_root": str(root),
        "dry_run": dry_run,
        "mutation_performed": False,
        "files_scanned": len(files),
        "symlinks_skipped": symlinks,
        "missing_external_url": missing,
        "invalid_external_urls": invalid,
        "unique_external_urls": len(urls),
        "duplicate_group_count": len(duplicate_groups),
        "duplicate_file_count": sum(
            len(paths) - 1 for paths in urls.values() if len(paths) > 1
        ),
        "duplicate_groups": duplicate_groups,
    }


def write_inventory_report(path: str | Path, report: dict[str, Any]) -> None:
    destination = Path(path).absolute()
    if destination.is_symlink():
        raise UnsafeStorePathError(f"report path must not be a symlink: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if destination.parent.is_symlink():
        raise UnsafeStorePathError(
            f"report directory must not be a symlink: {destination.parent}"
        )
    data = (
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    temporary = destination.parent / f".{destination.name}.{uuid.uuid4().hex}.tmp"
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
