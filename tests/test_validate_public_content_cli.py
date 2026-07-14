from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts.validate_public_content import _changed_markdown_files, main


def _post(body: str) -> str:
    return f"---\ntitle: test\ndate: 2026-07-13\n---\n\n{body}\n"


def test_cli_validates_explicit_markdown_and_rendered_post(tmp_path: Path) -> None:
    markdown = tmp_path / "safe.md"
    markdown.write_text(_post("[source](https://example.com)"), encoding="utf-8")
    public = tmp_path / "public"
    public.mkdir()
    (public / "index.html").write_text(
        '<html><script src="/trusted.js"></script>'
        '<article class="post-content"><p>safe</p></article></html>',
        encoding="utf-8",
    )

    assert main(["--markdown-file", str(markdown), "--rendered-root", str(public)]) == 0


def test_cli_returns_nonzero_and_does_not_rewrite_unsafe_input(tmp_path: Path) -> None:
    markdown = tmp_path / "unsafe.md"
    original = _post("<img src=x onerror=alert(1)>")
    markdown.write_text(original, encoding="utf-8")

    assert main(["--markdown-file", str(markdown)]) == 1
    assert markdown.read_text(encoding="utf-8") == original


def test_cli_rejects_rendered_post_without_required_content_container(tmp_path: Path) -> None:
    public = tmp_path / "public"
    public.mkdir()
    (public / "index.html").write_text("<html><p>missing post content</p></html>", encoding="utf-8")

    assert main(["--rendered-root", str(public)]) == 1


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_changed_markdown_compares_pull_request_base_to_head(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    posts = repository / "blog/content/posts"
    posts.mkdir(parents=True)
    _git(repository, "init", "-b", "main")
    _git(repository, "config", "user.name", "Test")
    _git(repository, "config", "user.email", "test@example.invalid")
    original = posts / "original.md"
    original.write_text(_post("original"), encoding="utf-8")
    _git(repository, "add", "--", "blog/content/posts/original.md")
    _git(repository, "commit", "-m", "base")
    base = _git(repository, "rev-parse", "HEAD")

    original.write_text(_post("changed"), encoding="utf-8")
    added = posts / "added.md"
    added.write_text(_post("added"), encoding="utf-8")
    _git(repository, "add", "--", "blog/content/posts")
    _git(repository, "commit", "-m", "head")

    changed = _changed_markdown_files(base_sha=base, project_root=repository)

    assert changed == [added, original]


def test_changed_markdown_rejects_an_unsafe_base_revision(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="full Git SHA"):
        _changed_markdown_files(base_sha="--output=/tmp/pwn", project_root=tmp_path)
