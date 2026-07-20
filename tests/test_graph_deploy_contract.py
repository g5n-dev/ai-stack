#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_TEMPLATE = (
    ROOT / "blog" / "themes" / "terminal-theme" / "layouts" / "scenarios" / "list.html"
)
VERIFY_SCRIPT = ROOT / "scripts" / "verify_graph.py"
DEPLOY_WORKFLOW = ROOT / ".github" / "workflows" / "deploy.yml"
REBUILD_SCRIPT = ROOT / "scripts" / "rebuild_release_data.sh"


class GraphDeployContractTest(unittest.TestCase):
    @staticmethod
    def _load_verify_module():
        spec = importlib.util.spec_from_file_location("verify_graph_contract", VERIFY_SCRIPT)
        assert spec is not None
        assert spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def _write_json(path: Path, payload: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")

    def _build_graph_fixture(self, public: Path) -> Path:
        graph = public / "data" / "tag-graph"
        files = {
            "core": "core.json",
            "community": "community.json",
            "search": "search.json",
            "tag": "tag.json",
            "tagHot": "tag.hot.json",
            "conceptHot": "concept.hot.json",
            "focusShards": ["focus-shards/000-fixture.json"],
        }
        self._write_json(graph / "index.json", {"version": 2, "files": files})
        for name in ("core.json", "tag.json", "tag.hot.json", "concept.hot.json"):
            self._write_json(graph / name, {"version": 2})
        self._write_json(
            graph / "search.json",
            {"version": 2, "items": [{"id": "tag:fixture"}]},
        )
        self._write_json(
            graph / "focus-shards" / "000-fixture.json",
            {"version": 2, "bucket": 0, "entries": {"tag:fixture": []}},
        )
        self._write_json(
            graph / "community.json",
            {
                "version": 2,
                "communities": [
                    {
                        "id": "community:fixture",
                        "hotspot_file": "community-hotspots/01-fixture.json",
                    }
                ],
            },
        )
        self._write_json(
            graph / "community-hotspots" / "01-fixture.json",
            {"version": 2, "community_id": "community:fixture"},
        )
        return graph

    def test_browser_smoke_uses_the_committed_hugo_fixture(self) -> None:
        module = self._load_verify_module()

        self.assertTrue(module.FIXTURE_CONTENT.is_dir())
        self.assertEqual("hugo_content", module.FIXTURE_CONTENT.name)

    def test_browser_smoke_contract_covers_http_failures_modes_mobile_and_reduced_motion(self) -> None:
        source = VERIFY_SCRIPT.read_text(encoding="utf-8")

        self.assertIn('page.on("response"', source)
        self.assertIn("response.status >= 400", source)
        self.assertIn('data-graph-mode="community"', source)
        self.assertIn('data-graph-mode="focus"', source)
        self.assertIn('fill("API")', source)
        self.assertIn('{"width": 390, "height": 844}', source)
        self.assertIn('reduced_motion="reduce"', source)
        self.assertIn("_particleFrame === null", source)

    def test_asset_verifier_checks_every_progressive_graph_file(self) -> None:
        module = self._load_verify_module()
        with tempfile.TemporaryDirectory() as tmp_dir:
            public = Path(tmp_dir)
            graph = self._build_graph_fixture(public)

            self.assertEqual([], module.verify_graph_assets(public))

            (graph / "focus-shards" / "000-fixture.json").unlink()
            failures = module.verify_graph_assets(public)

        self.assertTrue(any("missing graph asset" in failure for failure in failures))
        self.assertTrue(any("missing focus entries" in failure for failure in failures))

    def test_asset_verifier_rejects_uncovered_search_nodes(self) -> None:
        module = self._load_verify_module()
        with tempfile.TemporaryDirectory() as tmp_dir:
            public = Path(tmp_dir)
            graph = self._build_graph_fixture(public)
            self._write_json(
                graph / "search.json",
                {
                    "version": 2,
                    "items": [{"id": "tag:fixture"}, {"id": "tag:missing"}],
                },
            )

            failures = module.verify_graph_assets(public)

        self.assertIn("search nodes missing focus entries: 1", failures)

    def test_assets_only_mode_never_starts_the_browser_smoke_test(self) -> None:
        module = self._load_verify_module()
        with tempfile.TemporaryDirectory() as tmp_dir:
            public = Path(tmp_dir)
            self._build_graph_fixture(public)
            args = SimpleNamespace(
                assets_only=True,
                public_dir=public,
                screenshot=None,
            )

            with (
                mock.patch.object(module, "parse_args", return_value=args),
                mock.patch.object(
                    module,
                    "verify",
                    side_effect=AssertionError("browser verification must not run"),
                ),
            ):
                status = module.main()

        self.assertEqual(0, status)

    def test_production_template_uses_the_live_progressive_workbench(self) -> None:
        source = SCENARIO_TEMPLATE.read_text(encoding="utf-8")

        self.assertNotIn("GRAPH_UI_PENDING_INTEGRATION", source)
        self.assertIn('id="graph-workbench"', source)
        self.assertIn("data-index-url", source)
        self.assertIn("data-worker-url", source)
        for asset in (
            "cytoscape-3.34.0.min.js",
            "cytoscape-graph-engine.js",
            "cytoscape-graph-renderer.js",
            "graph-workbench.js",
            "data-parser-worker.js",
            "graph.css",
        ):
            with self.subTest(asset=asset):
                self.assertIn(asset, source)

    def test_graph_cache_version_tracks_generated_manifest_and_runtime(self) -> None:
        source = SCENARIO_TEMPLATE.read_text(encoding="utf-8")

        self.assertNotIn("production-v11", source)
        self.assertIn('readFile "static/data/tag-graph/index.json"', source)
        self.assertIn('readFile "static/js/data-parser-worker.js"', source)
        self.assertIn("| md5", source)

    def test_deploy_builds_pagefind_before_uploading_pages_artifact(self) -> None:
        source = DEPLOY_WORKFLOW.read_text(encoding="utf-8")
        rebuild = REBUILD_SCRIPT.read_text(encoding="utf-8")

        self.assertRegex(source, r"actions/setup-node@[0-9a-f]{40}")
        self.assertIn("npm ci --ignore-scripts", source)
        self.assertIn("bash scripts/rebuild_release_data.sh", source)
        self.assertIn("python3 scripts/build_content_quality_manifest.py", rebuild)
        self.assertIn("blog/data/content_quality.json", source)
        self.assertIn("./node_modules/.bin/pagefind --site blog/public", source)
        self.assertIn(
            "python3 -m ai_stack.pagefind_catalog --public-root blog/public",
            source,
        )
        self.assertNotIn("uv run", source)
        self.assertNotIn("npm run build:search", source)
        self.assertIn("test -s blog/public/pagefind/pagefind.js", source)
        upload = re.search(r"actions/upload-pages-artifact@[0-9a-f]{40}", source)
        self.assertIsNotNone(upload)
        self.assertLess(
            source.index("./node_modules/.bin/pagefind --site blog/public"),
            upload.start(),
        )
        self.assertIn("--assets-only --public-dir blog/static", rebuild)


if __name__ == "__main__":
    unittest.main()
