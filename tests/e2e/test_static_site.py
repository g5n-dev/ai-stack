from __future__ import annotations

import json
import os
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
