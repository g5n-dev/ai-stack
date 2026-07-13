from __future__ import annotations

import re
import shutil
import subprocess
import textwrap
import tomllib
import xml.etree.ElementTree as ET
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
BLOG = ROOT / "blog"
THEMES = BLOG / "themes"
PAGE_SIZE = 50


def test_production_config_emits_only_one_bounded_rss_feed() -> None:
    config = tomllib.loads((BLOG / "config.toml").read_text(encoding="utf-8"))

    assert config["outputs"] == {
        "home": ["HTML", "RSS"],
        "page": ["HTML"],
        "section": ["HTML"],
        "taxonomy": ["HTML"],
        "term": ["HTML"],
    }
    assert config["services"]["rss"]["limit"] == PAGE_SIZE
    assert config["permalinks"]["post"] == "/:year/:month/:slug/"


def test_rss_template_is_summary_only_and_has_no_html_bypass() -> None:
    template = (BLOG / "themes/terminal-theme/layouts/home.rss.xml").read_text(encoding="utf-8")

    assert ".Site.Config.Services.RSS.Limit" in template
    assert ".Plain" in template
    assert "truncate" in template
    assert ".Content" not in template
    assert "safeHTML" not in template


def test_list_templates_exclude_duplicate_navigation_text_from_pagefind() -> None:
    section = (BLOG / "themes/terminal-theme/layouts/_default/list.html").read_text(
        encoding="utf-8"
    )
    term = (BLOG / "themes/terminal-theme/layouts/partials/compact-term.html").read_text(
        encoding="utf-8"
    )
    taxonomy = (BLOG / "themes/terminal-theme/layouts/partials/compact-taxonomy.html").read_text(
        encoding="utf-8"
    )

    assert 'data-pagefind-ignore="all"' in section
    assert 'data-pagefind-ignore="all"' in term
    assert 'data-pagefind-ignore="all"' in taxonomy
    assert "data-pagefind-body" not in term
    assert "data-pagefind-body" not in taxonomy


@pytest.mark.skipif(shutil.which("hugo") is None, reason="Hugo is not installed")
def test_fixture_build_has_bounded_feeds_and_fifty_item_taxonomy_pages(
    tmp_path: Path,
) -> None:
    site = tmp_path / "site"
    public = site / "public"
    posts = site / "content/posts"
    posts.mkdir(parents=True)
    (site / "hugo.toml").write_text(
        textwrap.dedent(
            f"""\
            baseURL = "https://fixture.example/"
            languageCode = "zh-CN"
            title = "Output Boundary Fixture"
            theme = "terminal-theme"
            themesDir = "{THEMES.as_posix()}"
            disableKinds = ["sitemap", "robotsTXT", "404"]

            [params]
            description = "output boundary fixture"
            author = "fixture"
            github = "https://github.com/example/example"
            profile_image = "/img/profile-holo.png"
            paginate = {PAGE_SIZE}

            [taxonomies]
            tag = "tags"

            [permalinks]
            post = "/:year/:month/:slug/"

            [outputs]
            home = ["HTML", "RSS"]
            page = ["HTML"]
            section = ["HTML"]
            taxonomy = ["HTML"]
            term = ["HTML"]

            [services.rss]
            limit = {PAGE_SIZE}
            """
        ),
        encoding="utf-8",
    )

    start = datetime(2026, 1, 1, tzinfo=UTC)
    for index in range(55):
        published = start + timedelta(minutes=index)
        body = "摘要边界 " + ("可验证内容 " * 120) + f" FULL_BODY_SECRET_{index:03d}"
        (posts / f"post-{index:03d}.md").write_text(
            textwrap.dedent(
                f"""\
                ---
                title: "Fixture Post {index:03d}"
                date: {published.isoformat()}
                draft: false
                source: fixture
                tags: ["shared", "unique-{index:03d}"]
                ---

                {body}
                """
            ),
            encoding="utf-8",
        )

    result = subprocess.run(
        [
            "hugo",
            "--source",
            str(site),
            "--destination",
            str(public),
            "--minify",
            "--quiet",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr

    feeds = sorted(path.relative_to(public).as_posix() for path in public.rglob("*.xml"))
    assert feeds == ["index.xml"]

    feed_path = public / "index.xml"
    assert feed_path.stat().st_size <= 80_000
    feed = ET.parse(feed_path)
    items = feed.findall("./channel/item")
    assert len(items) == PAGE_SIZE
    assert items[0].findtext("link") == "https://fixture.example/posts/post-054/"
    assert all("FULL_BODY_SECRET" not in (item.findtext("description") or "") for item in items)
    assert all(len(item.findtext("description") or "") <= 650 for item in items)

    shared_pages = [
        public / "tags/shared/index.html",
        public / "tags/shared/page/2/index.html",
    ]
    assert [
        len(
            re.findall(
                r'data-taxonomy-entry=(?:"[^"]+"|[^\s>]+)',
                path.read_text(encoding="utf-8"),
            )
        )
        for path in shared_pages
    ] == [PAGE_SIZE, 5]
    assert all(path.stat().st_size <= 45_000 for path in shared_pages)

    taxonomy_pages = [
        public / "tags/index.html",
        public / "tags/page/2/index.html",
    ]
    assert [
        len(
            re.findall(
                r'data-term-link=(?:"[^"]+"|[^\s>]+)',
                path.read_text(encoding="utf-8"),
            )
        )
        for path in taxonomy_pages
    ] == [PAGE_SIZE, 6]
    assert all(path.stat().st_size <= 45_000 for path in taxonomy_pages)

    for path in [*shared_pages, *taxonomy_pages, public / "posts/index.html"]:
        html = path.read_text(encoding="utf-8")
        assert re.search(r'data-pagefind-ignore=(?:"all"|all)', html)
        assert "data-pagefind-body" not in html

    assert re.search(
        r"<link rel=canonical href=https://fixture\.example/tags/shared/page/2/\s*/?>",
        shared_pages[1].read_text(encoding="utf-8"),
    )
