#!/usr/bin/env python3
"""Fast graph workbench smoke test with a minimal Hugo content fixture."""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
FIXTURE_CONTENT = ROOT / "tests" / "fixtures" / "hugo_content"
GRAPH_DATA_PATH = Path("data/tag-graph")
GRAPH_STATIC_FILE_KEYS = ("core", "community", "search", "tag", "tagHot", "conceptHot")
GRAPH_NODE_LIMIT = 100
GRAPH_EDGE_LIMIT = 500
GRAPH_FOCUS_EDGE_LIMIT = 80
GRAPH_READY_TIMEOUT_MS = 20_000
GRAPH_INTERACTION_TIMEOUT_MS = 8_000


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *args: object) -> None:
        return


def _load_json_object(path: Path, label: str, failures: list[str]) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        failures.append(f"missing graph asset: {label}")
        return {}
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid graph asset {label}: {exc}")
        return {}

    if not isinstance(payload, dict):
        failures.append(f"graph asset is not an object: {label}")
        return {}
    return payload


def _resolve_graph_asset(
    graph_root: Path,
    relative_path: object,
    label: str,
    failures: list[str],
) -> Path | None:
    if not isinstance(relative_path, str) or not relative_path.strip():
        failures.append(f"invalid graph asset path for {label}")
        return None

    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        failures.append(f"unsafe graph asset path for {label}: {relative_path}")
        return None
    return graph_root / relative


def verify_graph_assets(public_dir: Path) -> list[str]:
    """Verify every file referenced by the progressive graph manifest."""

    failures: list[str] = []
    graph_root = public_dir / GRAPH_DATA_PATH
    index = _load_json_object(graph_root / "index.json", "index.json", failures)
    if not index:
        return failures
    if index.get("version") != 2:
        failures.append("graph index version is not 2")

    files = index.get("files")
    if not isinstance(files, dict):
        failures.append("graph index files map is missing")
        return failures

    loaded: dict[str, dict[str, Any]] = {}
    for key in GRAPH_STATIC_FILE_KEYS:
        relative = files.get(key)
        path = _resolve_graph_asset(graph_root, relative, f"files.{key}", failures)
        if path is None:
            continue
        payload = _load_json_object(path, str(relative), failures)
        if payload and payload.get("version") != 2:
            failures.append(f"graph asset version is not 2: {relative}")
        loaded[key] = payload

    focus_paths = files.get("focusShards")
    if not isinstance(focus_paths, list) or not focus_paths:
        failures.append("graph focus shard manifest is empty")
        focus_paths = []
    elif len(focus_paths) != len(set(focus_paths)):
        failures.append("graph focus shard manifest contains duplicate paths")

    focus_ids: set[str] = set()
    referenced_ids: set[str] = set()
    for expected_bucket, relative in enumerate(focus_paths):
        path = _resolve_graph_asset(
            graph_root,
            relative,
            f"focusShards[{expected_bucket}]",
            failures,
        )
        if path is None:
            continue
        payload = _load_json_object(path, str(relative), failures)
        if not payload:
            continue
        if payload.get("version") != 2:
            failures.append(f"focus shard version is not 2: {relative}")
        if payload.get("bucket") != expected_bucket:
            failures.append(
                f"focus shard bucket mismatch: {relative} "
                f"(expected {expected_bucket}, got {payload.get('bucket')})"
            )
        entries = payload.get("entries")
        if not isinstance(entries, dict):
            failures.append(f"focus shard entries are invalid: {relative}")
            continue
        duplicate_ids = focus_ids.intersection(entries)
        if duplicate_ids:
            failures.append(f"duplicate focus entries across shards: {relative}")
        focus_ids.update(str(node_id) for node_id in entries)
        for neighbors in entries.values():
            if not isinstance(neighbors, list):
                failures.append(f"focus neighbors are invalid: {relative}")
                continue
            for neighbor in neighbors:
                if isinstance(neighbor, list) and neighbor and isinstance(neighbor[0], str):
                    referenced_ids.add(neighbor[0])
                else:
                    failures.append(f"focus neighbor record is invalid: {relative}")

    search = loaded.get("search", {})
    items = search.get("items")
    search_ids: set[str] = set()
    if not isinstance(items, list):
        failures.append("graph search items are invalid")
    else:
        for item in items:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                search_ids.add(item["id"])
            else:
                failures.append("graph search contains an invalid item")

    missing_focus = search_ids - focus_ids
    extra_focus = focus_ids - search_ids
    dangling_neighbors = referenced_ids - search_ids
    if missing_focus:
        failures.append(f"search nodes missing focus entries: {len(missing_focus)}")
    if extra_focus:
        failures.append(f"focus entries missing from search: {len(extra_focus)}")
    if dangling_neighbors:
        failures.append(f"focus neighbors missing from search: {len(dangling_neighbors)}")

    community = loaded.get("community", {})
    communities = community.get("communities")
    if not isinstance(communities, list):
        failures.append("graph community list is invalid")
    else:
        hotspot_paths: set[str] = set()
        for entry in communities:
            if not isinstance(entry, dict) or not entry.get("hotspot_file"):
                continue
            relative = entry["hotspot_file"]
            if relative in hotspot_paths:
                failures.append(f"duplicate community hotspot path: {relative}")
                continue
            hotspot_paths.add(relative)
            path = _resolve_graph_asset(graph_root, relative, "community hotspot", failures)
            if path is None:
                continue
            payload = _load_json_object(path, str(relative), failures)
            if payload and payload.get("version") != 2:
                failures.append(f"community hotspot version is not 2: {relative}")
            if payload and payload.get("community_id") != entry.get("id"):
                failures.append(f"community hotspot identity mismatch: {relative}")

    return failures


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


def _attach_page_diagnostics(page: Any, failures: list[str], label: str) -> None:
    page.on("pageerror", lambda error: failures.append(f"{label} page error: {error}"))
    page.on(
        "requestfailed",
        lambda request: failures.append(
            f"{label} request failed: {request.url} ({request.failure})"
        ),
    )

    def capture_response(response: Any) -> None:
        if response.status >= 400:
            failures.append(f"{label} HTTP {response.status}: {response.url}")

    def capture_console(message: Any) -> None:
        text = message.text
        if message.type == "error" or "invalid selector" in text.casefold():
            failures.append(f"{label} console {message.type}: {text}")

    page.on("response", capture_response)
    page.on("console", capture_console)


def _wait_for_graph(page: Any) -> None:
    page.wait_for_selector("#graph-workbench.is-ready", timeout=GRAPH_READY_TIMEOUT_MS)
    page.wait_for_function(
        "() => window.graphEngine && graphEngine.cy && graphEngine.cy.nodes().length > 0",
        timeout=GRAPH_READY_TIMEOUT_MS,
    )


def _runtime_snapshot(page: Any) -> dict[str, Any]:
    return page.evaluate(
        """() => {
          const engine = window.graphEngine;
          const visible = engine?.getVisibleCounts?.() || { nodes: 0, edges: 0 };
          return {
            mode: engine?.mode || "unknown",
            canvas: Boolean(document.querySelector('#graph-container canvas')),
            nodeCount: engine?.cy?.nodes().length || 0,
            edgeCount: engine?.cy?.edges().length || 0,
            visibleNodes: visible.nodes || 0,
            visibleEdges: visible.edges || 0,
            api: ['setMode', 'focusNode', 'clearSelection', 'pause', 'resume', 'destroy']
              .every((name) => typeof engine?.[name] === 'function')
          };
        }"""
    )


def _assert_runtime_budget(
    runtime: dict[str, Any],
    failures: list[str],
    label: str,
) -> None:
    if not runtime["canvas"]:
        failures.append(f"{label} Cytoscape canvas is missing")
    if runtime["nodeCount"] <= 0:
        failures.append(f"{label} rendered no graph nodes")
    if not runtime["api"]:
        failures.append(f"{label} public graph engine API is incomplete")
    if runtime["nodeCount"] > GRAPH_NODE_LIMIT:
        failures.append(
            f"{label} node budget exceeded: {runtime['nodeCount']} > {GRAPH_NODE_LIMIT}"
        )
    if runtime["edgeCount"] > GRAPH_EDGE_LIMIT:
        failures.append(
            f"{label} edge budget exceeded: {runtime['edgeCount']} > {GRAPH_EDGE_LIMIT}"
        )
    if runtime["mode"] == "focus" and runtime["edgeCount"] > GRAPH_FOCUS_EDGE_LIMIT:
        failures.append(
            f"{label} focus edge budget exceeded: "
            f"{runtime['edgeCount']} > {GRAPH_FOCUS_EDGE_LIMIT}"
        )


def _verify_desktop_workbench(
    browser: Any,
    url: str,
    failures: list[str],
    screenshot: Path | None,
) -> None:
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    graph_requests: list[str] = []
    _attach_page_diagnostics(page, failures, "desktop")

    def capture_graph_request(request: Any) -> None:
        path = urlsplit(request.url).path
        if "/data/tag-graph/" in path:
            graph_requests.append(path[path.index("/data/tag-graph/") :])

    page.on("request", capture_graph_request)
    try:
        response = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=GRAPH_READY_TIMEOUT_MS,
        )
        if response is None or response.status != 200:
            status = getattr(response, "status", None)
            failures.append(f"desktop unexpected navigation status: {status}")
        _wait_for_graph(page)

        expected_bootstrap = [
            "/data/tag-graph/index.json",
            "/data/tag-graph/core.json",
        ]
        if graph_requests != expected_bootstrap:
            failures.append(
                "desktop first-screen graph request budget mismatch: "
                f"expected {expected_bootstrap}, got {graph_requests}"
            )
        overview = _runtime_snapshot(page)
        if overview["mode"] != "overview":
            failures.append(f"desktop expected overview mode, got {overview['mode']}")
        _assert_runtime_budget(overview, failures, "desktop overview")

        page.locator('[data-graph-mode="community"]').click(
            timeout=GRAPH_INTERACTION_TIMEOUT_MS
        )
        page.wait_for_function(
            "() => window.graphEngine?.mode === 'community' && "
            "window.graphEngine?._defaultCommunityExpansion === null",
            timeout=GRAPH_INTERACTION_TIMEOUT_MS,
        )
        community = _runtime_snapshot(page)
        _assert_runtime_budget(community, failures, "desktop community")

        page.locator('[data-graph-mode="focus"]').click(
            timeout=GRAPH_INTERACTION_TIMEOUT_MS
        )
        page.wait_for_function(
            "() => window.graphEngine?.mode === 'focus' && "
            "Boolean(window.graphEngine?.selectedNodeId)",
            timeout=GRAPH_INTERACTION_TIMEOUT_MS,
        )
        focus = _runtime_snapshot(page)
        _assert_runtime_budget(focus, failures, "desktop focus")

        search = page.locator("#graph-search")
        search.fill("API")
        page.wait_for_selector(
            "#graph-search-results:not([hidden]) .graph-search-result",
            timeout=GRAPH_INTERACTION_TIMEOUT_MS,
        )
        result_count = page.locator("#graph-search-results .graph-search-result").count()
        if not 1 <= result_count <= 10:
            failures.append(f"desktop search result budget invalid: {result_count}")
        target_id = page.evaluate(
            "window.graphRenderer?._searchItems?.[0]?.id || ''"
        )
        search.press("ArrowDown")
        search.press("Enter")
        if target_id:
            page.wait_for_function(
                "nodeId => window.graphEngine?.selectedNodeId === nodeId",
                arg=target_id,
                timeout=GRAPH_INTERACTION_TIMEOUT_MS,
            )
        page.wait_for_selector(
            '#graph-detail[aria-hidden="false"]',
            timeout=GRAPH_INTERACTION_TIMEOUT_MS,
        )
        detail = page.locator("#detail-name").inner_text().strip()
        if not detail or detail == "节点详情":
            failures.append("desktop selected node detail is empty")
        _assert_runtime_budget(_runtime_snapshot(page), failures, "desktop search focus")

        if screenshot:
            screenshot.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot), full_page=True)
    finally:
        context.close()


def _verify_mobile_reduced_motion(
    browser: Any,
    url: str,
    failures: list[str],
) -> None:
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        reduced_motion="reduce",
    )
    page = context.new_page()
    _attach_page_diagnostics(page, failures, "mobile reduced-motion")
    try:
        response = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=GRAPH_READY_TIMEOUT_MS,
        )
        if response is None or response.status != 200:
            status = getattr(response, "status", None)
            failures.append(f"mobile unexpected navigation status: {status}")
        _wait_for_graph(page)
        runtime = _runtime_snapshot(page)
        _assert_runtime_budget(runtime, failures, "mobile overview")
        mobile = page.evaluate(
            """() => {
              const engine = window.graphEngine;
              const modeButtons = Array.from(document.querySelectorAll('[data-graph-mode]'));
              const stage = document.querySelector('.graph-stage');
              return {
                reducedMotion: engine?.reducedMotion === true,
                particleFrameStopped: engine?._particleFrame === null,
                particleCount: engine?._particles?.length || 0,
                starfieldAnimation: stage
                  ? getComputedStyle(stage, '::before').animationName
                  : 'missing',
                horizontalOverflow: document.documentElement.scrollWidth - window.innerWidth,
                shortestModeButton: Math.min(
                  ...modeButtons.map((button) => button.getBoundingClientRect().height)
                )
              };
            }"""
        )
        if not mobile["reducedMotion"]:
            failures.append("mobile reduced-motion preference did not reach graph engine")
        if not mobile["particleFrameStopped"] or mobile["particleCount"] != 0:
            failures.append("mobile reduced-motion still has a running particle loop")
        if mobile["starfieldAnimation"] != "none":
            failures.append(
                "mobile reduced-motion starfield animation is still active: "
                f"{mobile['starfieldAnimation']}"
            )
        if mobile["horizontalOverflow"] > 1:
            failures.append(
                f"mobile page overflows horizontally by {mobile['horizontalOverflow']}px"
            )
        if mobile["shortestModeButton"] < 44:
            failures.append(
                "mobile mode control touch target is below 44px: "
                f"{mobile['shortestModeButton']}px"
            )
    finally:
        context.close()


def verify(public_dir: Path, screenshot: Path | None = None) -> list[str]:
    from playwright.sync_api import sync_playwright

    failures = verify_graph_assets(public_dir)
    handler = functools.partial(QuietHandler, directory=str(public_dir))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/scenarios/"

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                _verify_desktop_workbench(
                    browser,
                    url,
                    failures,
                    screenshot,
                )
                _verify_mobile_reduced_motion(browser, url, failures)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--assets-only",
        action="store_true",
        help=(
            "Validate progressive graph JSON assets without starting Hugo, "
            "Playwright, or Chromium."
        ),
    )
    parser.add_argument(
        "--public-dir",
        type=Path,
        help=(
            "Use an existing Hugo public directory instead of building the minimal "
            "fixture. With --assets-only, defaults to blog/static."
        ),
    )
    parser.add_argument("--screenshot", type=Path, help="Optional screenshot output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.assets_only:
            public_dir = (args.public_dir or BLOG / "static").resolve()
            failures = verify_graph_assets(public_dir)
        elif args.public_dir:
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
