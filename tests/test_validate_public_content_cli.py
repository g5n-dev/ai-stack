from __future__ import annotations

from pathlib import Path

from scripts.validate_public_content import main


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
