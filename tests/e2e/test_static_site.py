from __future__ import annotations

import json
import os
import re
import threading
from collections.abc import Generator
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import pytest
from bs4 import BeautifulSoup
from playwright.sync_api import Browser, Page, Request, expect, sync_playwright

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
