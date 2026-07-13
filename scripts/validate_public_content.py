#!/usr/bin/env python3
"""Read-only security gate for Markdown inputs and rendered Hugo post bodies."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from content_security import (  # noqa: E402
    ContentSecurityError,
    scan_rendered_html,
    validate_markdown_document,
)

_GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


def _changed_markdown_files(
    *,
    base_sha: str | None = None,
    project_root: Path = PROJECT_ROOT,
) -> list[Path]:
    if base_sha is not None and not _GIT_SHA.fullmatch(base_sha.casefold()):
        raise ValueError("--base-sha must be a full Git SHA")
    revision = f"{base_sha.casefold()}...HEAD" if base_sha is not None else "HEAD"
    commands = (
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
            revision,
            "--",
            "blog/content/posts",
        ],
        ["git", "ls-files", "--others", "--exclude-standard", "-z", "--", "blog/content/posts"],
    )
    names: set[str] = set()
    for command in commands:
        output = subprocess.check_output(command, cwd=project_root)
        names.update(name for name in output.decode("utf-8").split("\0") if name)
    return sorted(
        (project_root / name for name in names if name.endswith(".md")),
        key=lambda path: str(path),
    )


def _safe_files(paths: Iterable[Path], *, suffix: str) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_symlink():
            raise ContentSecurityError(
                # Keep the CLI independent from private helpers in the module.
                # ValueError text is sufficient for the operator report.
                []
            )
        if path.is_file() and path.suffix.lower() == suffix:
            files.append(path)
    return sorted(set(files), key=lambda candidate: str(candidate))


def _markdown_files(args: argparse.Namespace) -> list[Path]:
    candidates = [Path(value) for value in args.markdown_file]
    for root_value in args.markdown_root:
        root = Path(root_value)
        candidates.extend(root.rglob("*.md"))
    if args.changed_markdown:
        candidates.extend(_changed_markdown_files(base_sha=args.base_sha))
    return _safe_files(candidates, suffix=".md")


def _rendered_files(args: argparse.Namespace) -> tuple[list[Path], bool]:
    explicit = [Path(value) for value in args.rendered_file]
    candidates = list(explicit)
    for root_value in args.rendered_root:
        candidates.extend(Path(root_value).rglob("*.html"))
    return _safe_files(candidates, suffix=".html"), bool(explicit)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown-file", action="append", default=[])
    parser.add_argument("--markdown-root", action="append", default=[])
    parser.add_argument("--changed-markdown", action="store_true")
    parser.add_argument("--base-sha")
    parser.add_argument("--rendered-file", action="append", default=[])
    parser.add_argument("--rendered-root", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures: list[str] = []

    try:
        markdown_files = _markdown_files(args)
        rendered_files, has_explicit_rendered_files = _rendered_files(args)
    except (OSError, ValueError, subprocess.SubprocessError, ContentSecurityError) as exc:
        print(f"content-security: discovery failed: {exc}", file=sys.stderr)
        return 1

    for path in markdown_files:
        try:
            validate_markdown_document(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ContentSecurityError) as exc:
            failures.append(f"{path}: {exc}")

    rendered_candidates = 0
    explicit_set = {Path(value) for value in args.rendered_file}
    for path in rendered_files:
        try:
            rendered = path.read_text(encoding="utf-8")
            is_explicit = has_explicit_rendered_files and path in explicit_set
            if 'class="post-content' not in rendered and "class='post-content" not in rendered:
                if is_explicit:
                    raise ContentSecurityError([])
                continue
            rendered_candidates += 1
            scan_rendered_html(rendered, content_selector=".post-content")
        except (OSError, UnicodeError, ContentSecurityError) as exc:
            failures.append(f"{path}: {exc}")

    if args.rendered_root and rendered_candidates == 0:
        failures.append("rendered roots contained no .post-content document")

    if failures:
        for failure in failures:
            print(f"content-security: REJECTED: {failure}", file=sys.stderr)
        return 1

    print(
        "content-security: accepted "
        f"{len(markdown_files)} Markdown file(s), "
        f"{rendered_candidates} rendered post(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
