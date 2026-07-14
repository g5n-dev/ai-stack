#!/usr/bin/env python3

from __future__ import annotations

import unittest
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_TEMPLATE = (
    ROOT / "blog" / "themes" / "terminal-theme" / "layouts" / "scenarios" / "list.html"
)
VERIFY_SCRIPT = ROOT / "scripts" / "verify_graph.py"


class GraphDeployContractTest(unittest.TestCase):
    def test_browser_smoke_uses_the_committed_hugo_fixture(self) -> None:
        spec = importlib.util.spec_from_file_location("verify_graph_contract", VERIFY_SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertTrue(module.FIXTURE_CONTENT.is_dir())
        self.assertEqual("hugo_content", module.FIXTURE_CONTENT.name)

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


if __name__ == "__main__":
    unittest.main()
