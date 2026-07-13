from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_hugo_disables_raw_goldmark_html() -> None:
    config = (ROOT / "blog" / "config.toml").read_text(encoding="utf-8")

    assert "unsafe = false" in config
    assert "unsafe = true" not in config


def test_article_template_has_a_script_csp_and_no_unsafe_content_cast() -> None:
    template = (
        ROOT / "blog" / "themes" / "terminal-theme" / "layouts" / "_default" / "single.html"
    ).read_text(encoding="utf-8")

    assert 'http-equiv="Content-Security-Policy"' in template
    assert "script-src 'self'" in template
    assert "safeHTML" not in template
    assert "cdn.tailwindcss.com" not in template
    assert "fonts.googleapis.com" not in template
    assert "INTEGRITY_VERIFIED_99.9%" not in template
    assert "CITATION_GRAPH: LINKED" not in template


def test_disabled_comments_do_not_load_utterances() -> None:
    config = (ROOT / "blog" / "config.toml").read_text(encoding="utf-8")
    template = (
        ROOT / "blog" / "themes" / "terminal-theme" / "layouts" / "_default" / "single.html"
    ).read_text(encoding="utf-8")

    assert "enabled = false" in config
    assert "utteranc.es" not in template
