#!/usr/bin/env python3

import json
import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from processor.tag_graph import (
    build_tag_graph_data,
    get_tag_graph_runtime_options,
    write_tag_graph_split_from_result,
)


class TagGraphRuntimeTest(unittest.TestCase):
    def test_runtime_options_respect_env_flag(self):
        with mock.patch.dict(os.environ, {"TAG_GRAPH_ENABLE_CONTENT_MINING": "0"}, clear=False):
            options = get_tag_graph_runtime_options()

        self.assertFalse(options["enable_content_mining"])

    def test_build_tag_graph_without_content_mining_writes_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir) / "posts"
            posts_dir.mkdir(parents=True, exist_ok=True)
            (posts_dir / "demo.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: "Demo Agent Toolkit"
                    tags: ["LLM", "Agent"]
                    ---

                    Demo content mentioning Kubernetes and Python.
                    """
                ),
                encoding="utf-8",
            )

            result = build_tag_graph_data(
                enable_content_mining=False,
                existing_output_path=None,
                content_dir=str(posts_dir),
            )

            self.assertEqual(result["stats"]["tag_stats"]["total_articles"], 1)
            self.assertEqual(result["stats"]["tag_stats"]["total_concepts"], 0)

            out_dir = write_tag_graph_split_from_result(
                result=result,
                output_dir=str(Path(tmp_dir) / "out"),
                hot_tag_limit=10,
                hot_concept_limit=10,
            )
            tag_payload = json.loads((out_dir / "tag.json").read_text(encoding="utf-8"))

            self.assertIn("nodes", tag_payload)
            self.assertIn("links", tag_payload)
            self.assertTrue(any(node.get("id") == "LLM" for node in tag_payload["nodes"]))


if __name__ == "__main__":
    unittest.main()
