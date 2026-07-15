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

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
FIXTURE_CONTENT = ROOT / "tests" / "fixtures" / "hugo_content"
GRAPH_DATA_PATH = Path("data/tag-graph")
GRAPH_STATIC_FILE_KEYS = ("core", "community", "search", "tag", "tagHot", "conceptHot")


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
                status = getattr(response, "status", None)
                failures.append(f"unexpected navigation status: {status}")

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
