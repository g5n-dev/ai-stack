from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "blog" / "static" / "css"
LAYOUTS = ROOT / "blog" / "themes" / "terminal-theme" / "layouts"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _css_rule(source: str, selector: str) -> str:
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    matches = []
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", source):
        selectors, declarations = match.groups()
        if selector in {item.strip() for item in selectors.split(",")}:
            matches.append(declarations)
    if not matches:
        raise AssertionError(f"missing CSS rule: {selector}")
    return "\n".join(matches)


def test_intelligence_ledger_tokens_define_one_site_geometry() -> None:
    shared = _read(CSS / "style.css")
    root = _css_rule(shared, ":root")

    expected = {
        "--site-header-height: 64px",
        "--site-shell-max-width: 1600px",
        "--site-page-gutter: clamp(20px, 2.5vw, 40px)",
        "--site-rail-width: clamp(300px, 26.4vw, 392px)",
        "--site-layout-gap: clamp(20px, 2vw, 32px)",
        "--site-radius-panel: 8px",
        "--site-row-min-height: 72px",
        "--site-page-title-size: 30px",
        "--site-page-title-weight: 600",
        "--site-copy-line-height: 1.65",
        "--site-reading-measure: 74ch",
        "--site-reading-size: 16px",
    }
    for declaration in expected:
        assert declaration in root


def test_shared_shell_components_are_the_only_page_geometry_contract() -> None:
    shared = _read(CSS / "style.css")

    contracts = {
        ".site-shell": ("var(--site-shell-max-width)", "var(--site-page-gutter)"),
        ".site-page-hero": ("var(--site-hero-block-padding)",),
        ".site-page-kicker": ("var(--site-font-mono)", "var(--site-meta-size)"),
        ".site-layout": ("var(--site-rail-width)", "var(--site-layout-gap)"),
        ".site-rail": ("var(--site-rail-width)",),
        ".site-panel": ("var(--site-radius-panel)", "var(--site-border-color)"),
        ".site-ledger-row": ("var(--site-row-min-height)",),
        ".site-reading-body": ("var(--site-reading-measure)", "var(--site-reading-size)"),
    }
    for selector, tokens in contracts.items():
        rule = _css_rule(shared, selector)
        for token in tokens:
            assert token in rule, f"{selector} must use {token}"


def test_primary_archive_implements_the_selected_intelligence_ledger() -> None:
    posts = _read(LAYOUTS / "_default" / "list.html")

    assert 'class="site-shell' in posts
    assert 'class="site-layout' in posts
    assert 'class="site-rail' in posts
    assert 'class="site-main' in posts
    assert 'class="site-page-hero' in posts
    assert "INTELLIGENCE ARCHIVE / LIVE INDEX" in posts
    assert ">情报归档<" in posts
    assert 'class="site-panel site-ledger' in posts
    assert 'class="site-ledger-row' in posts

    for deprecated_geometry in ("max-w-6xl", "w-56", "rounded-xl"):
        assert deprecated_geometry not in posts


def test_search_and_taxonomy_reuse_the_same_shell_and_title_language() -> None:
    search = _read(LAYOUTS / "search" / "list.html")
    taxonomy = _read(LAYOUTS / "partials" / "compact-taxonomy.html")

    for source in (search, taxonomy):
        assert 'class="site-shell' in source
        assert 'class="site-page-hero' in source

    assert 'class="site-layout' in search
    assert 'class="site-rail' in search
    assert 'class="site-main' in search
    assert "STATIC INDEX / PAGEFIND_V2" in search

    assert "标签索引" in taxonomy
    assert "TAG TAXONOMY / LIVE INDEX" in taxonomy


def test_archive_about_trends_and_graph_share_the_same_visual_frame() -> None:
    archive = _read(LAYOUTS / "_default" / "archive.html")
    about = _read(LAYOUTS / "about" / "single.html")
    trends = _read(LAYOUTS / "trends" / "list.html")
    graph = _read(LAYOUTS / "scenarios" / "list.html")

    for source in (archive, about, trends):
        assert 'class="site-shell' in source
        assert 'class="site-page-hero' in source

    assert "TEMPORAL ARCHIVE / LIVE INDEX" in archive
    assert "SYSTEM DOSSIER / ABOUT" in about
    assert "INTELLIGENCE TRENDS / LIVE SIGNALS" in trends

    assert '<h1 class="site-page-title">动态场景知识图谱</h1>' in graph
    assert "INTELLIGENCE GRAPH / LIVE TOPOLOGY" in graph


def test_module_css_delegates_geometry_and_typography_to_shared_tokens() -> None:
    search = _read(CSS / "search.css")
    trends = _read(CSS / "trends.css")
    graph = _read(CSS / "graph.css")

    assert "var(--site-shell-max-width)" in search
    assert "var(--site-rail-width)" in search
    assert "var(--site-layout-gap)" in search

    assert "var(--site-shell-max-width)" in trends
    assert "var(--site-rail-width)" in trends
    assert "var(--site-layout-gap)" in trends

    assert "var(--site-rail-width)" in graph
    assert "var(--site-page-title-size)" not in _css_rule(graph, ".console-heading h1")
    assert "var(--site-page-title-weight)" not in _css_rule(graph, ".console-heading h1")

    trend_script = _read(ROOT / "blog" / "static" / "js" / "trends.js")
    graph_engine = _read(ROOT / "blog" / "static" / "js" / "cytoscape-graph-engine.js")
    for source in (trend_script, graph_engine):
        assert "--site-font-mono" in source
        assert "getComputedStyle" in source
    assert "--site-font-sans" in graph_engine


def test_font_roles_keep_chinese_ui_out_of_the_monospace_stack() -> None:
    shared = _read(CSS / "style.css")
    assert "var(--site-font-sans)" in _css_rule(shared, ".site-meta-text")
    assert "var(--site-font-mono)" in _css_rule(shared, ".site-code-text")
    assert "var(--site-font-mono)" in _css_rule(shared, ".site-page-kicker")

    single = _read(LAYOUTS / "_default" / "single.html")
    assert "site-reading-title" in single
    assert "site-reading-body" in single
    assert "max-w-none" not in single


def test_shared_header_matches_the_selected_64px_control_bar() -> None:
    shared = _read(CSS / "style.css")

    header = _css_rule(shared, ".site-header")
    assert "var(--site-header-height)" in header
    assert "var(--site-page-gutter)" in header

    title = _css_rule(shared, ".site-header__title")
    assert "font-size: 17px" in title
    assert "font-weight: 700" in title

    navigation = _css_rule(shared, ".site-header__nav a")
    assert "var(--site-control-size)" in navigation
    assert "min-height: 44px" in navigation
