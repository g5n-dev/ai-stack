#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_TEMPLATE = (
    ROOT / "blog" / "themes" / "terminal-theme" / "layouts" / "scenarios" / "list.html"
)
VERIFY_SCRIPT = ROOT / "scripts" / "verify_graph.py"
DEPLOY_WORKFLOW = ROOT / ".github" / "workflows" / "deploy.yml"


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

        self.assertIn("actions/setup-node@v4", source)
        self.assertIn("npm ci --ignore-scripts", source)
        self.assertIn("python3 scripts/build_content_quality_manifest.py", source)
        self.assertIn("blog/data/content_quality.json", source)
        self.assertIn("./node_modules/.bin/pagefind --site blog/public", source)
        self.assertIn(
            "python3 -m ai_stack.pagefind_catalog --public-root blog/public",
            source,
        )
        self.assertNotIn("uv run", source)
        self.assertNotIn("npm run build:search", source)
        self.assertIn("test -s blog/public/pagefind/pagefind.js", source)
        self.assertLess(
            source.index("./node_modules/.bin/pagefind --site blog/public"),
            source.index("actions/upload-pages-artifact@v3"),
        )


if __name__ == "__main__":
    unittest.main()
