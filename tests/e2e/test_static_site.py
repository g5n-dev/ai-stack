from __future__ import annotations

import json
import os
import re
import threading
from collections.abc import Generator
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
from bs4 import BeautifulSoup
from playwright.sync_api import Browser, Page, Request, Route, expect, sync_playwright

ROOT = Path(__file__).resolve().parents[2]
AXE_SCRIPT = ROOT / "node_modules" / "axe-core" / "axe.min.js"


class _QuietStaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


@pytest.fixture(scope="module")
def public_dir() -> Path:
    configured = os.environ.get("AI_STACK_PUBLIC_DIR")
    if not configured:
        pytest.fail("AI_STACK_PUBLIC_DIR must point to the exact built site artifact")
    root = Path(configured).resolve()
    required = [
        root / "index.html",
        root / "search" / "index.html",
        root / "pagefind" / "pagefind.js",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        pytest.fail(f"built site artifact is incomplete: {missing}")
    return root


@pytest.fixture(scope="module")
def site_url(public_dir: Path) -> Generator[str, None, None]:
    handler = partial(_QuietStaticHandler, directory=str(public_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.fixture(scope="module")
def browser() -> Generator[Browser, None, None]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def page(browser: Browser) -> Generator[Page, None, None]:
    context = browser.new_context(reduced_motion="reduce")
    if not AXE_SCRIPT.is_file():
        pytest.fail("npm ci must install the exact axe-core runtime before browser tests")
    context.add_init_script(path=AXE_SCRIPT)
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()


def _basic_wcag_violations(page: Page) -> list[str]:
    return page.evaluate(
        """
        () => {
          const violations = [];
          const html = document.documentElement;
          if (!html.lang || !html.lang.trim()) violations.push("html-lang");
          if (!document.title.trim()) violations.push("document-title");
          if (document.querySelectorAll("main").length !== 1) violations.push("one-main");
          if (document.querySelectorAll("h1").length !== 1) violations.push("one-h1");

          const ids = [...document.querySelectorAll("[id]")].map((node) => node.id);
          if (new Set(ids).size !== ids.length) violations.push("duplicate-id");

          for (const image of document.images) {
            if (!image.hasAttribute("alt")) violations.push("image-alt");
          }
          for (const control of document.querySelectorAll("input, select, textarea")) {
            if (control.type === "hidden") continue;
            const labelled = control.labels?.length > 0
              || control.hasAttribute("aria-label")
              || control.hasAttribute("aria-labelledby");
            if (!labelled) violations.push(`control-name:${control.id || control.name}`);
          }
          for (const element of document.querySelectorAll("a[href], button")) {
            const name = element.getAttribute("aria-label")
              || element.getAttribute("aria-labelledby")
              || element.textContent;
            if (!name || !name.trim()) violations.push("interactive-name");
          }
          return [...new Set(violations)];
        }
        """
    )


def test_search_is_keyboard_operable_filtered_and_same_origin(page: Page, site_url: str) -> None:
    external_requests: list[str] = []

    def record_external_request(request: Request) -> None:
        url = request.url
        if urlparse(url).netloc != urlparse(site_url).netloc:
            external_requests.append(url)

    page.on("request", record_external_request)
    response = page.goto(f"{site_url}/search/", wait_until="networkidle")
    assert response is not None and response.ok

    page.keyboard.press("Tab")
    expect(page.locator('a[href="#search-query"]')).to_be_focused()
    page.keyboard.press("Enter")
    expect(page.locator("#search-query")).to_be_focused()

    expect(page.locator("#search-source option")).not_to_have_count(1, timeout=15_000)
    page.locator("#search-query").fill("VideoGPA")
    page.locator("#search-source-trigger").click()
    page.locator(
        '#search-source-listbox [role="option"][data-value="arxiv"]'
    ).click()
    page.locator("#search-query").focus()
    page.keyboard.press("Enter")

    expect(page.locator("#search-status")).to_contain_text("找到", timeout=15_000)
    expect(page.locator("#search-results li").first).to_be_visible()
    expect(page.locator("#search-results li").first).to_contain_text("VideoGPA")

    # Reuse a term present in the verified abstract; UCF-101 was only present
    # in an older generated draft and is intentionally not reintroduced as an
    # unsupported claim.
    page.locator("#search-query").fill("VideoGPA")
    page.keyboard.press("Enter")
    expect(page.locator("#search-status")).to_contain_text("找到", timeout=15_000)
    expect(page.locator("#search-results")).to_contain_text("VideoGPA")
    assert external_requests == []


def test_search_page_passes_basic_automated_wcag_checks(page: Page, site_url: str) -> None:
    response = page.goto(f"{site_url}/search/", wait_until="domcontentloaded")
    assert response is not None and response.ok

    assert _basic_wcag_violations(page) == []
    violations = page.evaluate(
        """
        async () => {
          const result = await axe.run(document, {
            runOnly: {
              type: "tag",
              values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"],
            },
          });
          return result.violations.map((violation) => ({
            id: violation.id,
            impact: violation.impact,
            targets: violation.nodes.map((node) => node.target),
          }));
        }
        """
    )
    assert violations == []


def test_trends_initializes_and_all_primary_controls_change_real_state(
    page: Page, site_url: str
) -> None:
    response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
    assert response is not None and response.ok

    workbench = page.locator("#trend-workbench")
    status = page.locator("#trend-status")
    expect(status).to_contain_text("已发现", timeout=15_000)
    expect(status).not_to_have_class(re.compile(r"\bis-error\b"))
    expect(page.locator("#trend-result-count")).to_contain_text("个主题")

    page.locator('[data-trend-view="list"]').click()
    expect(workbench).to_have_attribute("data-view", "list")
    expect(page.locator("#trend-list .trend-card__button").first).to_be_visible()
    assert "view=list" in page.url

    page.locator('[data-trend-view="matrix"]').click()
    expect(workbench).to_have_attribute("data-view", "matrix")
    expect(page.locator("#trend-matrix-panel")).to_be_visible()

    page.locator('[data-trend-window="7d"]').click()
    expect(page.locator("#trend-stat-window")).to_have_text("7 天", timeout=15_000)
    expect(page.locator('[data-trend-window="7d"]')).to_have_attribute("aria-pressed", "true")
    assert "window=7d" in page.url

    page.locator("#trend-signal-trigger").click()
    page.locator('#trend-signal-listbox [role="option"][data-value="all"]').click()
    expect(page.locator("#trend-signal-trigger")).to_have_attribute("aria-expanded", "false")

    page.locator("#trend-source-trigger").click()
    source_option = page.locator(
        '#trend-source-listbox [role="option"]:not([data-value=""])'
    ).first
    source_value = source_option.get_attribute("data-value")
    assert source_value
    source_option.click()
    expect(page.locator("#trend-filter-summary")).to_contain_text("来源")
    assert "source=" in page.url

    page.locator("#trend-scenario-trigger").click()
    scenario_option = page.locator(
        '#trend-scenario-listbox [role="option"]:not([data-value=""])'
    ).first
    scenario_value = scenario_option.get_attribute("data-value")
    assert scenario_value
    scenario_option.click()
    expect(page.locator("#trend-filter-summary")).to_contain_text("场景")
    assert "scenario=" in page.url

    page.locator("#trend-clear").click()
    expect(page.locator("#trend-filter-summary")).to_contain_text("当前未启用附加筛选")
    assert "source=" not in page.url and "scenario=" not in page.url

    page.locator('[data-trend-view="list"]').click()
    first_topic = page.locator("#trend-list .trend-card__button").first
    first_topic.click()
    expect(workbench).to_have_attribute("data-detail", "open")
    expect(page.locator("#trend-detail .trend-link--graph")).to_be_visible(timeout=15_000)
    assert "topic=" in page.url

    page.locator("#trend-detail [data-close-trend-detail]").click()
    expect(workbench).to_have_attribute("data-detail", "closed")
    assert "topic=" not in page.url

    page.locator('[data-trend-view="matrix"]').click()
    matrix = page.locator("#trend-matrix")
    box = matrix.bounding_box()
    assert box is not None
    matrix.click(position={"x": box["width"] / 2, "y": box["height"] / 2})
    expect(workbench).to_have_attribute("data-detail", "open", timeout=15_000)
    expect(page.locator("#trend-detail .trend-link--graph")).to_be_visible(timeout=15_000)


def test_trends_typography_uses_the_shared_site_scale(
    page: Page, site_url: str
) -> None:
    runtime_errors: list[str] = []
    page.on("pageerror", lambda error: runtime_errors.append(str(error)))
    page.set_viewport_size({"width": 1440, "height": 900})
    response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
    assert response is not None and response.ok
    expect(page.locator("#trend-status")).to_contain_text("已发现", timeout=15_000)

    desktop = page.evaluate(
        """
        () => {
          const style = (selector) => getComputedStyle(document.querySelector(selector));
          return {
            title: style("#trend-page-title").fontSize,
            titleLine: style("#trend-page-title").lineHeight,
            titleWeight: style("#trend-page-title").fontWeight,
            lead: style(".trend-hero__lead").fontSize,
            module: style(".trend-stage__toolbar h2").fontSize,
            moduleLine: style(".trend-stage__toolbar h2").lineHeight,
            control: style("#trend-query").fontSize,
            button: style('[data-trend-window="30d"]').fontSize,
            buttonFamily: style('[data-trend-window="30d"]').fontFamily,
            buttonLine: style('[data-trend-window="30d"]').lineHeight,
            buttonWeight: style('[data-trend-window="30d"]').fontWeight,
            inputFamily: style("#trend-query").fontFamily,
            inputLine: style("#trend-query").lineHeight,
            inputWeight: style("#trend-query").fontWeight,
            selectFamily: style(".trend-select__trigger").fontFamily,
            selectLine: style(".trend-select__trigger").lineHeight,
            selectWeight: style(".trend-select__trigger").fontWeight,
            kickerLine: style(".trend-kicker").lineHeight,
          };
        }
        """
    )
    assert desktop["title"] == "30px"
    assert desktop["titleLine"] == "36px"
    assert desktop["titleWeight"] == "300"
    assert desktop["lead"] == "14px"
    assert desktop["module"] == "18px"
    assert float(desktop["moduleLine"].removesuffix("px")) == pytest.approx(24.3, abs=0.1)
    assert desktop["control"] == "13px"
    assert desktop["button"] == "13px"
    assert desktop["buttonFamily"] == desktop["inputFamily"]
    assert desktop["selectFamily"] == desktop["inputFamily"]
    assert float(desktop["buttonLine"].removesuffix("px")) == pytest.approx(19.5, abs=0.1)
    assert float(desktop["inputLine"].removesuffix("px")) == pytest.approx(19.5, abs=0.1)
    assert float(desktop["selectLine"].removesuffix("px")) == pytest.approx(19.5, abs=0.1)
    assert {desktop["buttonWeight"], desktop["inputWeight"], desktop["selectWeight"]} == {"600"}
    assert float(desktop["kickerLine"].removesuffix("px")) == pytest.approx(15.95, abs=0.1)

    page.set_viewport_size({"width": 1440, "height": 901})
    expect(page.locator("#trend-page-title")).to_have_css("font-size", "30px")
    expect(page.locator(".trend-hero__lead")).to_have_css("line-height", "24.5px")

    response = page.goto(f"{site_url}/search/", wait_until="domcontentloaded")
    assert response is not None and response.ok
    expect(page.locator(".search-page__title")).to_have_css("font-size", desktop["title"])
    expect(page.locator(".search-page__lead")).to_have_css("font-size", desktop["lead"])

    page.set_viewport_size({"width": 390, "height": 844})
    response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
    assert response is not None and response.ok
    expect(page.locator("#trend-page-title")).to_have_css("font-size", "30px")
    expect(page.locator("#trend-query")).to_have_css("font-size", "16px")
    assert runtime_errors == []


def test_all_regular_modules_share_one_dom_typography_hierarchy(
    page: Page, site_url: str
) -> None:
    page.set_viewport_size({"width": 1440, "height": 900})
    routes = (
        "/",
        "/posts/",
        "/archive/",
        "/search/",
        "/tags/",
        "/about/",
        "/trends/?window=30d",
    )
    title_styles: list[dict[str, str]] = []

    for route in routes:
        response = page.goto(f"{site_url}{route}", wait_until="domcontentloaded")
        assert response is not None and response.ok, route
        title = page.locator(".site-page-title").first
        expect(title).to_be_visible()
        title_styles.append(
            title.evaluate(
                """
                (node) => {
                  const style = getComputedStyle(node);
                  return {
                    family: style.fontFamily,
                    size: style.fontSize,
                    line: style.lineHeight,
                    weight: style.fontWeight,
                  };
                }
                """
            )
        )

    assert len({style["family"] for style in title_styles}) == 1
    assert {style["size"] for style in title_styles} == {"30px"}
    assert {style["line"] for style in title_styles} == {"36px"}
    assert {style["weight"] for style in title_styles} == {"300"}

    response = page.goto(f"{site_url}/scenarios/", wait_until="domcontentloaded")
    assert response is not None and response.ok
    expect(page.locator(".site-workbench-title")).to_have_css("font-size", "22px")
    expect(page.locator(".mode-button").first).to_have_css("font-size", "13px")
    expect(page.locator(".graph-search input")).to_have_css("font-size", "13px")

    page.set_viewport_size({"width": 390, "height": 844})
    response = page.goto(f"{site_url}/scenarios/", wait_until="domcontentloaded")
    assert response is not None and response.ok
    expect(page.locator(".site-workbench-title")).to_have_css("font-size", "18px")
    expect(page.locator(".mode-button").first).to_have_css("font-size", "13px")


def test_touch_inputs_avoid_mobile_browser_zoom(
    browser: Browser, site_url: str
) -> None:
    context = browser.new_context(
        viewport={"width": 844, "height": 390},
        has_touch=True,
        is_mobile=True,
        reduced_motion="reduce",
    )
    page = context.new_page()
    try:
        response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
        assert response is not None and response.ok
        expect(page.locator("#trend-status")).to_contain_text("已发现", timeout=15_000)
        expect(page.locator("#trend-query")).to_have_css("font-size", "16px")
        response = page.goto(f"{site_url}/scenarios/", wait_until="domcontentloaded")
        assert response is not None and response.ok
        expect(page.locator(".graph-search input")).to_have_css("font-size", "16px")
    finally:
        context.close()


def test_trend_matrix_badge_is_a_pointer_and_click_target(
    page: Page, site_url: str
) -> None:
    response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
    assert response is not None and response.ok

    workbench = page.locator("#trend-workbench")
    expect(page.locator("#trend-status")).to_contain_text("已发现", timeout=15_000)
    matrix = page.locator("#trend-matrix")
    box = matrix.bounding_box()
    assert box is not None

    width = box["width"]
    height = box["height"]
    center_y = round(height * 0.51, 3)
    cell_radius_y = max(72, min(height * 0.2, width * 0.18))
    badge_height = 42 if round(width) >= 900 else 38
    badge_position = {
        "x": width / 2,
        "y": max(
            8 + (badge_height / 2),
            center_y - cell_radius_y - 4 - (badge_height / 2),
        ),
    }

    matrix.hover(position=badge_position)
    expect(matrix).to_have_css("cursor", "pointer")
    matrix.click(position=badge_position)
    expect(workbench).to_have_attribute("data-detail", "open", timeout=15_000)
    expect(page.locator("#trend-detail .trend-link--graph")).to_be_visible(timeout=15_000)


def test_trend_matrix_canvas_keyboard_opens_the_first_visible_topic(
    page: Page, site_url: str
) -> None:
    response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
    assert response is not None and response.ok

    workbench = page.locator("#trend-workbench")
    expect(page.locator("#trend-status")).to_contain_text("已发现", timeout=15_000)
    first_topic = page.locator("#trend-list .trend-card__button").first
    expected_topic_id = first_topic.get_attribute("data-topic-id")
    assert expected_topic_id

    matrix = page.locator("#trend-matrix")
    expect(matrix).to_have_attribute("tabindex", "0")
    matrix.focus()
    expect(matrix).to_be_focused()
    page.keyboard.press("Enter")
    expect(workbench).to_have_attribute("data-detail", "open", timeout=15_000)
    assert parse_qs(urlparse(page.url).query).get("topic") == [expected_topic_id]

    page.locator("#trend-detail [data-close-trend-detail]").click()
    expect(workbench).to_have_attribute("data-detail", "closed")
    expect(matrix).to_be_focused()
    page.keyboard.press("Space")
    expect(workbench).to_have_attribute("data-detail", "open", timeout=15_000)
    assert parse_qs(urlparse(page.url).query).get("topic") == [expected_topic_id]

    page.locator('[data-trend-view="list"]').click()
    page.locator("#trend-detail [data-close-trend-detail]").click()
    expect(workbench).to_have_attribute("data-detail", "closed")
    expect(first_topic).to_be_focused()


def test_trends_fails_closed_without_presenting_phantom_data_controls(
    page: Page, site_url: str
) -> None:
    page.route(
        "**/data/stack-trends/index.json",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"schema_version":"stack_trends_index_v2","stats":{"unexpected":1}}',
        ),
    )
    response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
    assert response is not None and response.ok

    expect(page.locator("#trend-status")).to_have_class(re.compile(r"\bis-error\b"))
    expect(page.locator("#trend-workbench")).to_have_attribute("data-load-state", "error")
    expect(page.locator("#trend-workbench")).to_have_attribute("aria-busy", "false")
    expect(page.locator('[data-trend-window="30d"]')).to_be_disabled()
    expect(page.locator('[data-trend-view="list"]')).to_be_disabled()
    expect(page.locator("#trend-query")).to_be_disabled()
    expect(page.locator("#trend-signal-trigger")).to_be_disabled()
    expect(page.locator("#trend-source-trigger")).to_be_disabled()
    expect(page.locator("#trend-scenario-trigger")).to_be_disabled()
    expect(page.locator("#trend-clear")).to_be_disabled()

    # Layout disclosure remains usable even when the external data contract is rejected.
    page.set_viewport_size({"width": 390, "height": 844})
    toggle = page.locator("#trend-mobile-filter-toggle")
    expect(toggle).to_be_enabled()
    toggle.click()
    expect(toggle).to_have_attribute("aria-expanded", "true")


def test_trends_window_shard_failure_keeps_window_recovery_actionable(
    page: Page, site_url: str
) -> None:
    window_requests = 0

    def fail_first_window_shard(route: Route) -> None:
        nonlocal window_requests
        window_requests += 1
        if window_requests == 1:
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"schema_version":"invalid_window_fixture"}',
            )
            return
        route.continue_()

    page.route("**/data/stack-trends/windows/30d-*.json", fail_first_window_shard)
    response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
    assert response is not None and response.ok

    workbench = page.locator("#trend-workbench")
    expect(page.locator("#trend-status")).to_have_class(re.compile(r"\bis-error\b"))
    expect(workbench).to_have_attribute("data-load-state", "window-error")
    expect(workbench).to_have_attribute("aria-busy", "false")
    expect(page.locator('[data-trend-window="30d"]')).to_be_enabled()
    expect(page.locator('[data-trend-window="7d"]')).to_be_enabled()
    expect(page.locator('[data-trend-view="list"]')).to_be_disabled()
    expect(page.locator("#trend-query")).to_be_disabled()
    expect(page.locator("#trend-signal-trigger")).to_be_disabled()
    expect(page.locator("#trend-source-trigger")).to_be_disabled()
    expect(page.locator("#trend-scenario-trigger")).to_be_disabled()
    expect(page.locator("#trend-clear")).to_be_disabled()
    expect(page.locator("#trend-matrix")).to_have_attribute("aria-disabled", "true")
    expect(page.locator("#trend-matrix")).to_have_attribute("tabindex", "-1")

    page.locator('[data-trend-window="7d"]').click()
    expect(page.locator("#trend-status")).to_contain_text("已发现", timeout=15_000)
    expect(workbench).to_have_attribute("data-load-state", "ready")
    expect(workbench).to_have_attribute("aria-busy", "false")
    expect(page.locator("#trend-stat-window")).to_have_text("7 天")
    expect(page.locator('[data-trend-window="30d"]')).to_be_enabled()
    expect(page.locator('[data-trend-view="list"]')).to_be_enabled()
    expect(page.locator("#trend-query")).to_be_enabled()
    expect(page.locator("#trend-signal-trigger")).to_be_enabled()
    expect(page.locator("#trend-source-trigger")).to_be_enabled()
    expect(page.locator("#trend-scenario-trigger")).to_be_enabled()
    expect(page.locator("#trend-clear")).to_be_enabled()
    expect(page.locator("#trend-matrix")).to_have_attribute("aria-disabled", "false")
    expect(page.locator("#trend-matrix")).to_have_attribute("tabindex", "0")
    assert window_requests == 1


def test_trend_matrix_cannot_activate_stale_nodes_while_a_window_is_loading(
    page: Page, site_url: str
) -> None:
    pending_routes: list[Route] = []
    page.route(
        "**/data/stack-trends/windows/7d-*.json",
        lambda route: pending_routes.append(route),
    )
    response = page.goto(f"{site_url}/trends/?window=30d", wait_until="networkidle")
    assert response is not None and response.ok
    expect(page.locator("#trend-status")).to_contain_text("已发现", timeout=15_000)

    workbench = page.locator("#trend-workbench")
    matrix = page.locator("#trend-matrix")
    first_topic = page.locator("#trend-list .trend-card__button").first
    expected_topic_id = first_topic.get_attribute("data-topic-id")
    expected_topic_name = first_topic.locator(".trend-card__title").inner_text()
    assert expected_topic_id and expected_topic_name
    first_topic.click()
    expect(page.locator("#trend-detail .trend-link--graph")).to_be_visible(timeout=15_000)
    expect(page.locator("#trend-detail-title")).to_have_text(expected_topic_name)

    page.locator('[data-trend-window="7d"]').click()
    expect(workbench).to_have_attribute("data-load-state", "loading")
    expect(matrix).to_have_attribute("aria-disabled", "true")
    assert pending_routes
    expect(page.locator("#trend-detail-title")).to_have_text("正在切换观察窗口")
    expect(page.locator("#trend-detail .trend-link--graph")).to_have_count(0)
    expect(page.locator("#trend-stat-topics")).to_have_text("—")
    expect(page.locator("#trend-stat-sources")).to_have_text("—")
    expect(page.locator("#trend-stat-window")).to_have_text("7 天")
    expect(page.locator("#trend-result-count")).to_have_text("— 个主题")

    matrix.click(force=True)
    matrix.press("Enter")
    expect(workbench).to_have_attribute("data-detail", "open")
    assert parse_qs(urlparse(page.url).query).get("topic") == [expected_topic_id]

    pending_routes[0].abort()
    expect(workbench).to_have_attribute("data-load-state", "window-error")
    expect(page.locator("#trend-detail-title")).to_have_text("观察窗口暂不可用")
    expect(page.locator("#trend-detail")).not_to_contain_text(expected_topic_name)
    expect(page.locator("#trend-filter-summary")).to_contain_text("当前窗口数据不可用")


def test_pagefind_index_contains_article_body_and_facets(public_dir: Path) -> None:
    article = next(
        path
        for path in public_dir.rglob("index.html")
        if path.parent.name != "search" and "data-pagefind-body" in path.read_text(encoding="utf-8")
    )
    soup = BeautifulSoup(article.read_text(encoding="utf-8"), "html.parser")

    assert soup.select_one("[data-pagefind-body]") is not None
    assert soup.select_one('[data-pagefind-meta="title[content]"]') is not None
    assert soup.select_one('[data-pagefind-filter="source[content]"]') is not None
    assert soup.select_one('[data-pagefind-filter="date[content]"]') is not None
    assert any((public_dir / "pagefind").rglob("*.pf_index"))
    assert not any((public_dir / "pagefind").rglob("*.pf_fragment"))
    catalog = json.loads((public_dir / "pagefind/catalog.json").read_text(encoding="utf-8"))
    manifest = json.loads(
        (public_dir / "pagefind/catalog.manifest.json").read_text(encoding="utf-8")
    )
    assert catalog["schema_version"] == "pagefind_result_catalog_v1"
    assert catalog["record_count"] == len(catalog["records"])
    assert manifest["catalog_gzip_bytes"] <= 1024 * 1024
