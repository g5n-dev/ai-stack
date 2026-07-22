from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "blog/themes/terminal-theme/layouts/trends/list.html"
CSS = ROOT / "blog/static/css/trends.css"
SCRIPT = ROOT / "blog/static/js/trends.js"


def test_trends_page_is_a_progressive_shared_header_workbench() -> None:
    source = TEMPLATE.read_text(encoding="utf-8")
    soup = BeautifulSoup(source, "html.parser")

    assert '{{ partial "site-head.html"' in source
    assert '{{ partial "site-header.html" . }}' in source
    assert '"css/trends.css" | relURL' in source
    assert '"js/trends.js" | relURL' in source
    assert '"js/watchlist.js" | relURL' in source
    assert soup.select_one('main[id="trend-workbench"]') is not None
    matrix = soup.select_one('canvas[id="trend-matrix"]')
    assert matrix is not None
    assert matrix.get("role") == "button"
    assert matrix.get("tabindex") == "0"
    assert matrix.get("aria-keyshortcuts") == "Enter Space"
    assert matrix.get("aria-describedby") == "trend-matrix-tooltip"
    tooltip = soup.select_one('[id="trend-matrix-tooltip"][role="tooltip"]')
    assert tooltip is not None
    assert tooltip.has_attr("hidden")
    assert soup.select_one('ol[id="trend-list"]') is not None
    assert soup.select_one('[id="trend-detail"]') is not None
    assert soup.select_one('[id="trend-status"][aria-live="polite"]') is not None
    assert soup.select_one('[id="trend-filter-summary"][aria-live="polite"]') is not None
    assert soup.select_one('a[href="#trend-controls"]') is not None
    assert soup.select_one('button.trend-mobile-filter-toggle[aria-controls="trend-filter-body"]') is not None
    assert soup.select_one('[id="trend-filter-body"]') is not None
    enhanced_selects = soup.select('[data-trend-select] > select')
    assert [select.get("id") for select in enhanced_selects] == [
        "trend-signal",
        "trend-source",
        "trend-scenario",
    ]
    assert soup.select_one('.trend-matrix-legend [data-heat="cold"]') is not None
    assert soup.select_one('.trend-matrix-legend [data-heat="signal"]') is not None
    assert "颜色 / 辉光：综合热度" in source
    assert "符号：变化状态" in source
    assert source.count("<h1") == 1
    assert "趋势洞察" in source
    assert "STACK趋势" not in source
    assert "不代表全网热度" in source
    assert "位置用于主题分组与排名轨道" in source
    assert "外围圈径编码证据数量" in source
    assert "中心为固定放大展开态" in source
    assert "横轴为增长方向" not in source
    assert "https://cdn." not in source
    assert "requestAnimationFrame" not in source


def test_trends_styles_are_scoped_and_share_site_tokens() -> None:
    source = CSS.read_text(encoding="utf-8")

    assert ".site-header" not in source
    for token in (
        "var(--site-font-sans)",
        "var(--site-font-mono)",
        "var(--site-page-title-size, 30px)",
        "var(--site-page-title-line-height, 1.2)",
        "var(--site-copy-size, 14px)",
        "var(--site-control-size, 13px)",
        "var(--primary)",
        "var(--deep-navy)",
        "var(--terminal-bg)",
        "var(--muted-teal)",
        "var(--off-white)",
    ):
        assert token in source
    assert "@media (prefers-reduced-motion: reduce)" in source
    assert "min-height: 44px" in source
    assert "--trend-faint: rgba(var(--off-white), 0.58)" in source
    assert not any(f"font-size: {size}px" in source for size in (8, 9, 10))
    assert ".trend-evidence-link" in source
    assert ".trend-mobile-filter-toggle" in source
    assert ".trend-select__trigger" in source
    assert ".trend-select__list" in source
    assert '[role="option"]' in source
    assert '.trend-matrix-legend span[data-heat="signal"]' in source
    assert ".trend-matrix-tooltip" in source
    assert ".trend-card__focus-details" in source
    assert ".trend-card__button:focus-visible .trend-card__focus-details" in source
    assert ".trend-list:has(.trend-card__button:focus-visible)" in source
    assert ".trend-score-method__formula" in source
    assert ".trend-score-method__audit" in source
    assert '.trend-workbench[data-detail="open"] .trend-detail' in source
    assert "@media (max-width: 1439px)" in source
    assert source.count(".trend-hero h1 {") == 1
    assert "font-size: clamp(28px, 3vw, 44px)" not in source
    assert "font-size: clamp(27px, 2.4vw, 36px)" not in source
    assert re.search(
        r"@media \(hover: none\) and \(pointer: coarse\).*?"
        r"\.trend-control-group input\s*\{\s*font-size:\s*16px;",
        source,
        re.DOTALL,
    )
    compact_height = re.search(
        r"@media \(min-width: 761px\) and \(max-height: 900px\) \{(.*?)"
        r"@media \(max-width: 1020px\)",
        source,
        re.DOTALL,
    )
    assert compact_height is not None
    assert ".trend-hero h1" not in compact_height.group(1)
    compact_lead = re.search(
        r"\.trend-hero__lead\s*\{(.*?)\}",
        compact_height.group(1),
        re.DOTALL,
    )
    assert compact_lead is not None
    assert "line-height:" not in compact_lead.group(1)


def test_trends_runtime_uses_safe_text_progressive_loading_and_distinct_links() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    assert "textContent" in source
    assert "innerHTML" not in source
    assert "AbortController" in source
    assert "requestAnimationFrame" not in source
    assert "history.pushState" in source
    assert 'listen(windowObject, "popstate"' in source
    assert "/scenarios/" in source
    assert 'mode: "focus"' in source
    assert "AIStackWatchlist" in source
    assert "external_url" not in source
    assert "time.dateTime = item.published_at" in source
    assert "completeDetailTransition" in source
    assert "closeTopicDetail(true)" in source
    assert "restoreTrendOrigin(previousTopic" in source
    assert "loadTopic(model.state.topic, { push: false, focus: true, scroll: true })" in source
    assert "setFilterPanel(!filterMedia?.matches)" in source
    assert "resolveWindowSignal" in source
    assert "MAX_TOPOLOGY_CELLS = 11" in source
    assert "MAX_MATRIX_PIXELS = 8 * 1024 * 1024" in source
    assert "createTrendSelect" in source
    assert "aria-activedescendant" in source
    assert "heatVisual" in source
    assert "matrixTooltipCopy" in source
    assert "renderMatrixTooltip" in source
    assert "trendCardScoreCopy" in source
    assert "appendScoreExplanation" in source
    assert "scoreExplanation(signal, model.state.window, model.index.formula)" in source
    assert "appendComponents(elements.detail, signal.components)" in source
    assert "buildTrendReturnUrl(windowObject.location.pathname, model.state)" in source
    assert "appendReturnContext" in source
    assert "elements.matrix.title" not in source
    assert 'root.dataset.detail = model.state.topic ? "open" : "closed"' in source
    load_topic = source.index("async function loadTopic")
    invalidate = source.index("const sequence = invalidateTopicLoad(model);", load_topic)
    cache_lookup = source.index("const cached = model.topicCache.get(id);", load_topic)
    assert invalidate < cache_lookup
    assert "30 天来源分布" in source
    assert "30 天证据文章" in source


def test_trends_route_and_navigation_use_the_short_user_facing_name() -> None:
    config = (ROOT / "blog/config.toml").read_text(encoding="utf-8")
    content = ROOT / "blog/content/trends/_index.md"

    assert content.is_file()
    assert 'name = "趋势"' in config
    assert 'url = "/trends/"' in config
    assert "STACK趋势" not in config
    labels = ("首页", "归档", "搜索", "标签", "趋势", "图谱", "关于")
    positions = [config.index(f'name = "{label}"') for label in labels]
    assert positions == sorted(positions)
