#!/usr/bin/env python3
"""Fast graph workbench smoke test with a minimal Hugo content fixture."""

from __future__ import annotations

import argparse
import functools
import http.server
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
FIXTURE_CONTENT = ROOT / "tests" / "fixtures" / "hugo_content"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *args: object) -> None:
        return


def build_fixture(destination: Path) -> None:
    if not shutil.which("hugo"):
        raise RuntimeError("Hugo is not installed")
    subprocess.run(
        [
            "hugo",
            "--source",
            str(BLOG),
            "--contentDir",
            str(FIXTURE_CONTENT),
            "--destination",
            str(destination),
            "--cleanDestinationDir",
            "--noBuildLock",
            "--minify",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def verify(public_dir: Path, screenshot: Path | None = None) -> list[str]:
    from playwright.sync_api import sync_playwright

    failures: list[str] = []
    handler = functools.partial(QuietHandler, directory=str(public_dir))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/scenarios/"

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.on("pageerror", lambda error: failures.append(f"page error: {error}"))
            page.on(
                "requestfailed",
                lambda request: failures.append(
                    f"request failed: {request.url} ({request.failure})"
                ),
            )

            def capture_console(message) -> None:
                text = message.text
                if message.type == "error" or "invalid selector" in text.casefold():
                    failures.append(f"console {message.type}: {text}")

            page.on("console", capture_console)

            response = page.goto(url, wait_until="domcontentloaded")
            if response is None or response.status != 200:
                failures.append(f"unexpected navigation status: {getattr(response, 'status', None)}")

            try:
                page.wait_for_selector("#graph-workbench.is-ready", timeout=20_000)
                page.wait_for_function(
                    "window.graphEngine && graphEngine.cy && graphEngine.cy.nodes().length > 0",
                    timeout=20_000,
                )
            except Exception as exc:
                failures.append(f"graph did not become ready: {exc}")

            runtime = page.evaluate(
                """() => {
                  const engine = window.graphEngine;
                  return {
                    canvas: Boolean(document.querySelector('#graph-container canvas')),
                    nodeCount: engine?.cy?.nodes().length || 0,
                    edgeCount: engine?.cy?.edges().length || 0,
                    api: ['setMode', 'focusNode', 'clearSelection', 'pause', 'resume', 'destroy']
                      .every((name) => typeof engine?.[name] === 'function')
                  };
                }"""
            )
            if not runtime["canvas"]:
                failures.append("Cytoscape canvas is missing")
            if runtime["nodeCount"] <= 0:
                failures.append("no graph nodes were rendered")
            if not runtime["api"]:
                failures.append("public graph engine API is incomplete")

            if runtime["nodeCount"] > 0:
                page.evaluate("() => graphEngine.cy.nodes().first().emit('tap')")
                try:
                    page.wait_for_selector('#graph-detail[aria-hidden="false"]', timeout=5_000)
                except Exception as exc:
                    failures.append(f"node detail did not open: {exc}")
                detail = page.locator("#detail-name").inner_text().strip()
                if not detail or detail == "节点详情":
                    failures.append("selected node detail is empty")
                page.wait_for_timeout(450)

            if screenshot:
                screenshot.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(screenshot), full_page=True)

            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--public-dir",
        type=Path,
        help="Use an existing Hugo public directory instead of building the minimal fixture.",
    )
    parser.add_argument("--screenshot", type=Path, help="Optional screenshot output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.public_dir:
            failures = verify(args.public_dir.resolve(), args.screenshot)
        else:
            with tempfile.TemporaryDirectory(prefix="ai-stack-graph-verify-") as tmp_dir:
                public_dir = Path(tmp_dir) / "public"
                build_fixture(public_dir)
                failures = verify(public_dir, args.screenshot)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        print(f"Graph verification failed with {len(failures)} issue(s).", file=sys.stderr)
        return 1

    print("Graph verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
