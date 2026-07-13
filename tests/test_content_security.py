from __future__ import annotations

from pathlib import Path

import pytest

import content_security
from content_security import (
    ContentSecurityError,
    scan_rendered_html,
    validate_markdown_document,
    validate_public_url,
)

SAFE_DOCUMENT = """---
title: \"安全的 AI 文章\"
date: 2026-07-13T00:00:00Z
source: arxiv
external_url: https://arxiv.org/abs/2607.00001
tags:
  - AI
---

## 摘要

请阅读[原始论文](https://arxiv.org/abs/2607.00001)和[站内归档](/posts/)。

```html
<script>alert("code samples are inert")</script>
```
"""


@pytest.mark.parametrize(
    ("url", "allow_relative"),
    [
        ("https://example.com/a?q=1", False),
        ("http://localhost:1313/post", False),
        ("/posts/example/", True),
        ("#evidence", True),
    ],
)
def test_validate_public_url_accepts_explicit_safe_destinations(
    url: str, allow_relative: bool
) -> None:
    assert validate_public_url(url, allow_relative=allow_relative) == url


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "java%73cript:alert(1)",
        "jav&#x61;script:alert(1)",
        "data:text/html,<script>alert(1)</script>",
        "vbscript:msgbox(1)",
        "file:///etc/passwd",
        "//evil.example/redirect",
        "https://example.com/\x00payload",
    ],
)
def test_validate_public_url_rejects_dangerous_or_ambiguous_destinations(url: str) -> None:
    with pytest.raises(ContentSecurityError):
        validate_public_url(url)


@pytest.mark.parametrize(
    ("url", "allow_relative"),
    [
        ("", False),
        ("https:", False),
        ("relative/path", False),
        (":ambiguous", True),
    ],
)
def test_validate_public_url_rejects_incomplete_destinations(
    url: str, allow_relative: bool
) -> None:
    with pytest.raises(ContentSecurityError):
        validate_public_url(url, allow_relative=allow_relative)


def test_security_error_normalizes_an_empty_finding_sequence() -> None:
    error = ContentSecurityError([])

    assert error.findings[0].code == "unknown"


def test_validate_markdown_document_accepts_safe_markdown_and_inert_code_samples() -> None:
    result = validate_markdown_document(SAFE_DOCUMENT)

    assert result.frontmatter["title"] == "安全的 AI 文章"
    assert result.frontmatter["source"] == "arxiv"
    assert result.body.startswith("\n## 摘要")


@pytest.mark.parametrize(
    ("payload", "finding_code"),
    [
        ("<script>alert(1)</script>", "raw-html"),
        ("<img src=x onerror=alert(1)>", "raw-html"),
        ("<svg><a xlink:href='javascript:alert(1)'>x</a></svg>", "raw-html"),
        ("[click](javascript:alert(1))", "unsafe-url"),
        ("![pixel](data:image/svg+xml,<svg onload=alert(1)>)", "unsafe-url"),
        ('{{< figure src="https://example.com/x.png" >}}', "shortcode"),
        ("{{% rawhtml %}}<script>alert(1)</script>{{% /rawhtml %}}", "shortcode"),
    ],
)
def test_validate_markdown_document_fails_closed_for_active_content(
    payload: str, finding_code: str
) -> None:
    document = "---\ntitle: test\ndate: 2026-07-13\n---\n\n" + payload

    with pytest.raises(ContentSecurityError) as exc_info:
        validate_markdown_document(document)

    assert finding_code in {finding.code for finding in exc_info.value.findings}


@pytest.mark.parametrize(
    "frontmatter",
    [
        "title: !!python/object/apply:os.system ['id']\ndate: 2026-07-13",
        "title: safe\ntitle: overwritten\ndate: 2026-07-13",
        "title: '{{< readfile file=\"/etc/passwd\" >}}'\ndate: 2026-07-13",
        "title: safe\nexternal_url: javascript:alert(1)\ndate: 2026-07-13",
        "- title\n- not-a-mapping",
    ],
)
def test_validate_markdown_document_rejects_malicious_frontmatter(frontmatter: str) -> None:
    with pytest.raises(ContentSecurityError):
        validate_markdown_document(f"---\n{frontmatter}\n---\n\nbody")


def test_validate_markdown_document_requires_closed_frontmatter() -> None:
    with pytest.raises(ContentSecurityError, match="frontmatter"):
        validate_markdown_document("---\ntitle: never closed\nbody")


def test_validate_markdown_document_requires_frontmatter_at_the_start() -> None:
    with pytest.raises(ContentSecurityError, match="frontmatter"):
        validate_markdown_document("# title\n\nbody")


def test_validate_markdown_document_handles_crlf_after_frontmatter() -> None:
    result = validate_markdown_document("---\ntitle: safe\ndate: 2026-07-13\n---\r\nbody")

    assert result.body == "body"


def test_validate_markdown_document_enforces_size_and_control_limits(monkeypatch) -> None:
    monkeypatch.setattr(content_security, "MAX_DOCUMENT_BYTES", 8)
    with pytest.raises(ContentSecurityError, match="2 MiB"):
        validate_markdown_document(SAFE_DOCUMENT)

    monkeypatch.setattr(content_security, "MAX_DOCUMENT_BYTES", 2 * 1024 * 1024)
    with pytest.raises(ContentSecurityError, match="control"):
        validate_markdown_document("---\ntitle: x\n---\nbody\x01")
    with pytest.raises(ContentSecurityError, match="must be text"):
        validate_markdown_document(None)  # type: ignore[arg-type]


def test_validate_markdown_document_enforces_frontmatter_limits(monkeypatch) -> None:
    monkeypatch.setattr(content_security, "MAX_FRONTMATTER_BYTES", 8)

    with pytest.raises(ContentSecurityError, match="64 KiB"):
        validate_markdown_document("---\ntitle: too-long\n---\nbody")


def test_validate_markdown_document_rejects_non_scalar_mapping_key() -> None:
    with pytest.raises(ContentSecurityError, match="scalar"):
        validate_markdown_document("---\n? [a, b]\n: value\n---\nbody")


def test_frontmatter_walker_rejects_invalid_keys_and_unsupported_values() -> None:
    with pytest.raises(ContentSecurityError, match="keys"):
        content_security._walk_frontmatter({1: "value"})
    with pytest.raises(ContentSecurityError, match="unsupported"):
        content_security._walk_frontmatter({"value": object()})
    with pytest.raises(ContentSecurityError, match="too many"):
        content_security._walk_frontmatter(
            ["one", "two"], seen=[content_security.MAX_NESTED_VALUES - 1]
        )


def test_markdown_autolinks_and_reference_links_are_validated() -> None:
    safe = "---\ntitle: safe\n---\n<https://example.com>\n[x][ref]\n[ref]: /posts/\n"
    assert validate_markdown_document(safe).frontmatter["title"] == "safe"

    unsafe = "---\ntitle: unsafe\n---\n[x][ref]\n[ref]: javascript:alert(1)\n"
    with pytest.raises(ContentSecurityError, match="unsafe-url"):
        validate_markdown_document(unsafe)


def test_scan_rendered_html_accepts_normal_hugo_output() -> None:
    scan_rendered_html(
        '<article class="post-content"><h2>标题</h2><p>正文 '
        '<a href="https://example.com" rel="noopener">来源</a></p></article>'
    )


@pytest.mark.parametrize(
    "html",
    [
        '<div class="post-content"><script>alert(1)</script></div>',
        '<div class="post-content"><img src="x" onerror="alert(1)"></div>',
        '<div class="post-content"><a href="javascript:alert(1)">x</a></div>',
        '<div class="post-content"><iframe srcdoc="<script>alert(1)</script>"></iframe></div>',
        '<div class="post-content"><svg><script>alert(1)</script></svg></div>',
        '<div class="post-content"><meta http-equiv="refresh" '
        'content="0;url=//evil.example"></div>',
    ],
)
def test_scan_rendered_html_rejects_executable_dom(html: str) -> None:
    with pytest.raises(ContentSecurityError):
        scan_rendered_html(html)


def test_rendered_site_scanner_only_trusts_scripts_outside_post_body(tmp_path: Path) -> None:
    document = tmp_path / "index.html"
    document.write_text(
        """<!doctype html><html><head><script src="/js/terminal.js"></script></head>
        <body><article class="post-content"><p>safe</p></article></body></html>""",
        encoding="utf-8",
    )

    scan_rendered_html(document.read_text(encoding="utf-8"), content_selector=".post-content")


def test_scan_rendered_html_requires_selected_content_and_bounded_text(monkeypatch) -> None:
    with pytest.raises(ContentSecurityError, match="selector"):
        scan_rendered_html("<main>no post</main>", content_selector=".post-content")
    with pytest.raises(ContentSecurityError, match="missing"):
        scan_rendered_html(None)  # type: ignore[arg-type]

    monkeypatch.setattr(content_security, "MAX_DOCUMENT_BYTES", 1)
    with pytest.raises(ContentSecurityError, match="16 MiB"):
        scan_rendered_html("<p>too large</p>")


def test_scan_rendered_html_rejects_active_styles_and_srcset_urls() -> None:
    with pytest.raises(ContentSecurityError, match="active style"):
        scan_rendered_html('<p style="background:url(javascript:alert(1))">x</p>')
    with pytest.raises(ContentSecurityError, match="unsafe-url"):
        scan_rendered_html('<img srcset="https://example.com/x.png 1x, data:text/html,x 2x">')

    scan_rendered_html('<img srcset="/images/x.png 1x, https://example.com/x@2.png 2x">')
