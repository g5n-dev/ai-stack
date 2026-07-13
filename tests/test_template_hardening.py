from __future__ import annotations

import re
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LAYOUT_ROOT = ROOT / "blog/themes/terminal-theme/layouts"
PAGE_TEMPLATES = (
    LAYOUT_ROOT / "404.html",
    LAYOUT_ROOT / "index.html",
    LAYOUT_ROOT / "_default/archive.html",
    LAYOUT_ROOT / "_default/list.html",
    LAYOUT_ROOT / "_default/single.html",
    LAYOUT_ROOT / "_default/terms.html",
    LAYOUT_ROOT / "about/single.html",
    LAYOUT_ROOT / "scenarios/list.html",
    LAYOUT_ROOT / "scenarios/single.html",
)


def _template_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in PAGE_TEMPLATES)


def test_all_page_templates_share_the_strict_local_head() -> None:
    head = (LAYOUT_ROOT / "partials/site-head.html").read_text(encoding="utf-8")

    assert "default-src 'self'" in head
    assert "script-src 'self'" in head
    assert "object-src 'none'" in head
    assert "base-uri 'none'" in head
    assert 'href="/css/tailwind.css"' in head
    assert 'href="/css/style.css"' in head
    for template in PAGE_TEMPLATES:
        assert 'partial "site-head.html"' in template.read_text(encoding="utf-8"), template


def test_templates_do_not_depend_on_remote_or_inline_executable_scripts() -> None:
    templates = _template_text()

    assert "cdn.tailwindcss.com" not in templates
    assert "fonts.googleapis.com" not in templates
    assert "fonts.gstatic.com" not in templates
    assert not re.search(r'<script[^>]+src=["\']https?://', templates, re.IGNORECASE)
    assert not re.search(
        r"<script(?![^>]*type=\"application/ld\+json\")(?![^>]*\bsrc=)[^>]*>",
        templates,
        re.IGNORECASE,
    )


def test_article_related_posts_use_the_offline_index_without_site_scan() -> None:
    template = (LAYOUT_ROOT / "_default/single.html").read_text(encoding="utf-8")

    assert ".Site.Data.related.index.by_route" in template
    assert ".Site.Data.related.index.by_id" in template
    assert "data-related-source=\"offline-index\"" in template
    assert ".Site.RegularPages" not in template


def test_templates_have_no_unsafe_casts_or_hard_coded_trust_claims() -> None:
    templates = _template_text()

    assert "safeHTML" not in templates
    assert "INTEGRITY_VERIFIED" not in templates
    assert "99.9%" not in templates
    assert "CITATION_GRAPH: LINKED" not in templates


def test_graph_template_is_a_non_executable_integration_placeholder() -> None:
    template = (LAYOUT_ROOT / "scenarios/list.html").read_text(encoding="utf-8")

    assert "GRAPH_UI_PENDING_INTEGRATION" in template
    assert "cytoscape.min.js" not in template
    assert "dagre.min.js" not in template
    assert "graph-page.js" not in template


@pytest.mark.skipif(shutil.which("hugo") is None, reason="Hugo is not installed")
def test_single_page_resolves_related_entries_by_stable_id_in_constant_lookup(
    tmp_path: Path,
) -> None:
    site = tmp_path / "site"
    (site / "content/posts").mkdir(parents=True)
    (site / "data/related").mkdir(parents=True)
    themes_dir = ROOT / "blog/themes"
    (site / "hugo.toml").write_text(
        textwrap.dedent(
            f"""\
            baseURL = "https://fixture.example/"
            languageCode = "zh-CN"
            title = "Template Fixture"
            theme = "terminal-theme"
            themesDir = "{themes_dir.as_posix()}"
            disableKinds = ["home", "taxonomy", "term", "RSS", "sitemap", "robotsTXT", "404"]

            [params]
            description = "fixture"
            profile_image = "/img/profile-holo.png"
            """
        ),
        encoding="utf-8",
    )
    (site / "content/posts/alpha.md").write_text(
        textwrap.dedent(
            """\
            ---
            title: Alpha
            date: 2026-07-13T00:00:00+00:00
            event_id: event-alpha
            tags: [agent]
            ---

            Alpha body.
            """
        ),
        encoding="utf-8",
    )
    (site / "content/posts/beta.md").write_text(
        textwrap.dedent(
            """\
            ---
            title: Beta
            date: 2026-07-12T00:00:00+00:00
            tags: [agent]
            ---

            Beta body.
            """
        ),
        encoding="utf-8",
    )
    (site / "data/related/index.json").write_text(
        """{
          "schema_version": "related_index_v1",
          "by_id": {"event-alpha": "/canonical/alpha/"},
          "by_route": {
            "/canonical/alpha/": [{
              "id": "event-beta",
              "route": "/posts/beta/",
              "title": "Beta",
              "published_at": "2026-07-12T00:00:00Z",
              "shared_tags": ["agent"],
              "shared_tag_count": 1
            }]
          }
        }\n""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            "hugo",
            "--source",
            str(site),
            "--destination",
            str(site / "public"),
            "--quiet",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr

    html = (site / "public/posts/alpha/index.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    related = soup.select_one('[data-related-source="offline-index"]')
    assert related is not None
    link = related.select_one('a[href="/posts/beta/"]')
    assert link is not None
    assert "Beta" in link.get_text(" ", strip=True)
    assert soup.select_one('meta[http-equiv="Content-Security-Policy"]') is not None
    assert soup.select_one('link[href="/css/tailwind.css"]') is not None


@pytest.mark.skipif(shutil.which("hugo") is None, reason="Hugo is not installed")
def test_rendered_core_pages_have_basic_keyboard_accessibility(tmp_path: Path) -> None:
    public = tmp_path / "public"
    result = subprocess.run(
        [
            "hugo",
            "--source",
            str(ROOT / "blog"),
            "--destination",
            str(public),
            "--quiet",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, result.stderr

    for relative in (
        "index.html",
        "404.html",
        "posts/index.html",
        "about/index.html",
        "scenarios/index.html",
    ):
        document = public / relative
        assert document.is_file(), document
        soup = BeautifulSoup(document.read_text(encoding="utf-8"), "html.parser")
        assert soup.select_one("main") is not None, relative
        assert soup.select_one("h1") is not None, relative
        assert not soup.select('[tabindex]:not([tabindex="0"]):not([tabindex="-1"])'), relative
        for control in soup.select("a[href], button, input"):
            accessible_name = control.get("aria-label") or control.get_text(" ", strip=True)
            if control.name == "input":
                accessible_name = accessible_name or control.get("placeholder")
            assert accessible_name, f"{relative}: unnamed {control}"
