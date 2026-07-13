from __future__ import annotations

import json
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def test_pagefind_and_node_test_runner_are_exactly_locked() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))

    assert package["devDependencies"]["pagefind"] == "1.5.2"
    assert package["scripts"]["build:search"] == (
        "pagefind --site blog/public && "
        "uv run python scripts/build_pagefind_catalog.py --public-root blog/public"
    )
    assert package["scripts"]["test"] == (
        "node --test tests/js/*.mjs && "
        "uv run pytest -q tests/test_pagefind_catalog.py tests/test_static_search_configuration.py"
    )
    assert lock["packages"][""]["devDependencies"]["pagefind"] == "1.5.2"
    assert lock["packages"]["node_modules/pagefind"]["version"] == "1.5.2"

    pagefind = yaml.safe_load((ROOT / "pagefind.yml").read_text(encoding="utf-8"))
    assert pagefind == {"site": "blog/public", "glob": "**/index.html"}


def test_search_page_is_semantic_keyboard_ready_and_self_hosted() -> None:
    template = ROOT / "blog/themes/terminal-theme/layouts/search/list.html"
    soup = BeautifulSoup(template.read_text(encoding="utf-8"), "html.parser")

    assert soup.html is not None and soup.html.get("lang")
    assert soup.title is not None
    assert len(soup.select("main")) == 1
    assert len(soup.select("h1")) == 1
    assert soup.select_one('a[href="#search-query"]') is not None
    assert soup.select_one('form[role="search"]') is not None
    assert soup.select_one('input[name="query"]') is not None
    for name in ("source", "date", "entity", "tag", "scenario"):
        control = soup.select_one(f'[name="{name}"]')
        assert control is not None
        assert soup.select_one(f'label[for="{control.get("id")}"]') is not None

    script = soup.select_one('script[src="/js/search.js"]')
    assert script is not None

    template_text = template.read_text(encoding="utf-8")
    for low_contrast_class in (
        "text-primary/70",
        "text-muted-teal/70",
        "text-off-white/45",
    ):
        assert low_contrast_class not in template_text

    search_script = (ROOT / "blog/static/js/search.js").read_text(encoding="utf-8")
    assert "text-muted-teal/60" not in search_script
    assert "result.data(" not in search_script
    assert 'fetch("/pagefind/catalog.json"' in search_script
    assert not template.read_text(encoding="utf-8").__contains__("https://cdn.")


def test_article_template_exposes_search_body_and_versioned_facets() -> None:
    template = (ROOT / "blog/themes/terminal-theme/layouts/_default/single.html").read_text(
        encoding="utf-8"
    )
    metadata = (
        ROOT / "blog/themes/terminal-theme/layouts/partials/pagefind-metadata.html"
    ).read_text(encoding="utf-8")

    assert "data-pagefind-body" in template
    assert 'partial "pagefind-metadata.html"' in template
    for key in ("source", "date", "entity", "tag", "scenario"):
        assert f'data-pagefind-filter="{key}' in metadata
    assert 'data-pagefind-meta="title[content]"' in metadata
    assert 'data-pagefind-sort="date[content]"' in metadata
