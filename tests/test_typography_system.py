from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ROOT / "blog" / "themes" / "terminal-theme" / "layouts"
CSS = ROOT / "blog" / "static" / "css"


def _normalise_whitespace(value: str) -> str:
    return " ".join(value.split())


def _split_selectors(selector_list: str) -> list[str]:
    """Split a selector list without treating commas inside :where() as separators."""

    selectors: list[str] = []
    current: list[str] = []
    depth = 0
    for character in selector_list:
        if character == "(":
            depth += 1
        elif character == ")":
            depth = max(0, depth - 1)
        if character == "," and depth == 0:
            selectors.append(_normalise_whitespace("".join(current)))
            current = []
            continue
        current.append(character)
    if current:
        selectors.append(_normalise_whitespace("".join(current)))
    return selectors


def _css_rule(source: str, selector: str) -> str:
    """Return all declaration blocks that contain an exact selector."""

    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    wanted = _normalise_whitespace(selector)
    bodies: list[str] = []
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", source):
        selector_list, declarations = match.groups()
        if wanted in _split_selectors(selector_list):
            bodies.append(declarations)
    if not bodies:
        raise AssertionError(f"missing CSS rule: {selector}")
    return "\n".join(bodies)


def _heading_classes_containing(relative_path: str, needle: str) -> set[str]:
    source = (LAYOUTS / relative_path).read_text(encoding="utf-8")
    for match in re.finditer(
        r"<(h[1-3])\b([^>]*)>(.*?)</\1>",
        source,
        flags=re.DOTALL | re.IGNORECASE,
    ):
        attributes, content = match.group(2), match.group(3)
        if needle not in content:
            continue
        class_match = re.search(r'\bclass="([^"]*)"', attributes)
        return set(class_match.group(1).split()) if class_match else set()
    raise AssertionError(f"missing heading containing {needle!r} in {relative_path}")


def test_shared_type_tokens_drive_the_global_body_and_semantic_classes() -> None:
    shared = (CSS / "style.css").read_text(encoding="utf-8")
    root_rule = _css_rule(shared, ":root")

    required_tokens = {
        "--site-page-title-size",
        "--site-page-title-line-height",
        "--site-page-title-weight",
        "--site-workbench-title-size",
        "--site-workbench-title-line-height",
        "--site-workbench-title-weight",
        "--site-section-title-size",
        "--site-section-title-line-height",
        "--site-section-title-weight",
        "--site-copy-size",
        "--site-copy-line-height",
        "--site-control-size",
        "--site-control-line-height",
        "--site-meta-size",
        "--site-meta-line-height",
    }
    for token in sorted(required_tokens):
        assert f"{token}:" in root_rule, f"missing shared typography token {token}"

    body_rule = _css_rule(shared, "body")
    assert "var(--site-font-sans)" in body_rule
    assert "var(--site-copy-size" in body_rule
    assert "var(--site-copy-line-height" in body_rule

    semantic_rules = {
        ".site-page-title": (
            "var(--site-page-title-size)",
            "var(--site-page-title-line-height)",
            "var(--site-page-title-weight)",
        ),
        ".site-workbench-title": (
            "var(--site-workbench-title-size)",
            "var(--site-workbench-title-line-height)",
            "var(--site-workbench-title-weight)",
        ),
        ".site-section-title": (
            "var(--site-section-title-size)",
            "var(--site-section-title-line-height)",
            "var(--site-section-title-weight)",
        ),
        ".site-body-copy": ("var(--site-copy-size)", "var(--site-copy-line-height)"),
        ".site-control-text": (
            "var(--site-control-size)",
            "var(--site-control-line-height)",
        ),
        ".site-meta-text": ("var(--site-meta-size)", "var(--site-meta-line-height)"),
    }
    for selector, tokens in semantic_rules.items():
        rule = _css_rule(shared, selector)
        for token in tokens:
            assert token in rule, f"{selector} must use {token}"


def test_tailwind_font_utilities_delegate_to_the_shared_font_variables() -> None:
    config = (ROOT / "tailwind.config.js").read_text(encoding="utf-8")
    font_family = re.search(r"fontFamily:\s*\{(.*?)\n\s*\}\n\s*\}", config, re.DOTALL)
    assert font_family is not None

    display = re.search(r"display:\s*\[(.*?)\]", font_family.group(1), re.DOTALL)
    mono = re.search(r"mono:\s*\[(.*?)\]", font_family.group(1), re.DOTALL)
    assert display is not None and "var(--site-font-sans)" in display.group(1)
    assert mono is not None and "var(--site-font-mono)" in mono.group(1)


def test_regular_page_titles_share_one_semantic_class() -> None:
    # Article headlines/read copy intentionally retain their editorial scale. The graph
    # canvas is also excluded because its collision-aware labels are not DOM typography.
    regular_titles = {
        "index.html": "情报总览",
        "_default/list.html": "情报归档",
        "_default/archive.html": "时间线归档",
        "partials/compact-taxonomy.html": "{{ $pageTitle }}",
        "partials/compact-term.html": "{{ $termTitle }}",
        "scenarios/single.html": "{{ .Title }}",
        "search/list.html": "检索情报归档",
        "about/single.html": "{{ .Title }}",
        "trends/list.html": "趋势洞察",
        "scenarios/list.html": "动态场景知识图谱",
    }
    for template, title_text in regular_titles.items():
        classes = _heading_classes_containing(template, title_text)
        assert "site-page-title" in classes, (
            f"{template} visible page title must use .site-page-title"
        )


def test_home_and_about_keep_a_semantic_heading_hierarchy() -> None:
    home = (LAYOUTS / "index.html").read_text(encoding="utf-8")
    about = (LAYOUTS / "about/single.html").read_text(encoding="utf-8")

    assert re.search(r'<h1\b[^>]*site-page-title[^>]*>.*?情报总览', home, re.DOTALL)
    assert '<h2 id="home-system-log-heading">日志流</h2>' in home
    assert len(re.findall(r'<h2\b[^>]*site-section-title', home)) >= 3
    assert re.search(r'<h1\b[^>]*site-page-title[^>]*>.*?{{ \.Title }}', about, re.DOTALL)
    assert len(re.findall(r'<h2\b[^>]*site-section-title', about)) >= 2


def test_workbench_and_module_titles_use_shared_semantic_classes() -> None:
    expectations = {
        ("scenarios/list.html", "动态场景知识图谱"): "site-page-title",
        ("scenarios/list.html", "节点详情"): "site-section-title",
        ("trends/list.html", "趋势筛选"): "site-section-title",
        ("trends/list.html", "趋势矩阵"): "site-section-title",
        ("trends/list.html", "主题详情"): "site-section-title",
    }
    for (template, title_text), semantic_class in expectations.items():
        classes = _heading_classes_containing(template, title_text)
        assert semantic_class in classes, (
            f"{template} heading {title_text!r} must use .{semantic_class}"
        )


def test_graph_reset_preserves_component_type_and_dom_controls_use_tokens() -> None:
    graph = (CSS / "graph.css").read_text(encoding="utf-8")

    reset = _css_rule(graph, ".graph-body :where(button, input)")
    assert "font: inherit" in reset
    assert not re.search(
        r"\.graph-body\s+button\s*,\s*\.graph-body\s+input\s*\{[^{}]*font:\s*inherit",
        graph,
        flags=re.DOTALL,
    ), "the high-specificity reset overrides graph component typography"

    for selector in (
        ".mode-button",
        ".graph-search input",
        ".graph-search-results button",
        ".detail-focus-button",
    ):
        rule = _css_rule(graph, selector)
        assert "var(--site-control-size" in rule, (
            f"{selector} must use the shared DOM control size token"
        )

    mobile_input = _css_rule(graph, ".graph-search input")
    assert "font-size: 16px" in mobile_input

    graph_title_override = _css_rule(graph, ".console-heading h1")
    for declaration in (
        "font-family",
        "font-size",
        "font-weight",
        "line-height",
        "letter-spacing",
    ):
        assert declaration not in graph_title_override, (
            "the graph page title must inherit the complete .site-page-title contract "
            f"instead of redeclaring {declaration}"
        )
    assert "var(--site-section-title-size" in _css_rule(
        graph, ".graph-detail__header h2"
    )

    for selector in (
        ".graph-search > label",
        ".console-section summary",
        ".graph-telemetry dt",
        ".detail-identity dt",
        ".graph-detail section h3",
        ".detail-identity dd",
        ".graph-stage__mode-chip",
        ".detail-article-link span",
        ".detail-article-lineage",
        ".detail-list-heading span",
        ".detail-intel-list__metric",
    ):
        assert "var(--graph-sans)" in _css_rule(graph, selector), (
            f"{selector} contains Chinese UI copy and must use the shared sans role"
        )

    assert "var(--graph-mono)" in _css_rule(graph, ".detail-metrics dd")


def test_trend_dom_titles_and_controls_use_the_shared_tokens() -> None:
    trends = (CSS / "trends.css").read_text(encoding="utf-8")

    for selector in (
        ".trend-panel-heading h2",
        ".trend-stage__toolbar h2",
        ".trend-detail h2",
    ):
        assert "var(--site-section-title-size" in _css_rule(trends, selector)

    control_selectors = (
        ".trend-segmented button",
        ".trend-control-group input",
        ".trend-select__trigger",
        '.trend-select__list [role="option"]',
        ".trend-button",
    )
    for selector in control_selectors:
        rule = _css_rule(trends, selector)
        assert "var(--site-control-size" in rule
        assert "var(--site-font-sans)" in rule
        assert "var(--site-control-line-height" in rule
        assert "var(--site-control-weight" in rule

    for selector in (".trend-mobile-filter-toggle",):
        rule = _css_rule(trends, selector)
        assert "var(--site-font-sans)" in rule
        assert "var(--site-control-line-height" in rule
        assert "var(--site-control-weight" in rule

    kicker = _css_rule(trends, ".trend-kicker")
    assert "var(--site-meta-size" in kicker
    assert "var(--site-meta-line-height" in kicker

    labels = _css_rule(trends, ".trend-control-group label")
    assert "var(--site-font-sans)" in labels
    assert "var(--site-control-size" in labels

    kpi_labels = _css_rule(trends, ".trend-kpis dt")
    assert "var(--site-font-sans)" in kpi_labels


def test_lineage_uses_the_canonical_site_monospace_token() -> None:
    lineage = (CSS / "lineage.css").read_text(encoding="utf-8")

    assert "var(--site-font-mono" in lineage
    assert "var(--font-mono" not in lineage

    article = (LAYOUTS / "_default/single.html").read_text(encoding="utf-8")
    assert 'md5 (readFile "static/css/lineage.css")' in article
    assert 'printf "%s?v=%s" ("css/lineage.css" | relURL)' in article


def test_shared_styles_do_not_duplicate_the_monospace_stack() -> None:
    shared = (CSS / "style.css").read_text(encoding="utf-8")
    assert "ui-monospace, SFMono-Regular" not in shared
