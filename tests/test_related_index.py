#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from processor.related_index import (
    RelatedIndexValidationError,
    build_related_index,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "related_posts"
SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "build_related_index.py"


class RelatedIndexTest(unittest.TestCase):
    def test_builds_o1_route_and_stable_id_lookups(self):
        payload = build_related_index(FIXTURE_DIR, max_related=6)

        self.assertEqual(payload["schema_version"], "related_index_v1")
        self.assertEqual(payload["post_count"], 5)
        self.assertEqual(payload["by_id"]["evt-alpha"], "/posts/alpha/")
        self.assertEqual(payload["by_id"]["item-gamma"], "/research/gamma/")
        self.assertIn("/posts/beta/", payload["by_route"])
        self.assertNotIn("/posts/draft/", payload["by_route"])

    def test_related_order_prefers_shared_tags_then_distance_then_route(self):
        payload = build_related_index(FIXTURE_DIR, max_related=6)

        alpha_related = payload["by_route"]["/posts/alpha/"]

        self.assertEqual(
            [entry["route"] for entry in alpha_related],
            ["/posts/beta/", "/posts/epsilon/", "/research/gamma/"],
        )
        self.assertEqual(alpha_related[0]["shared_tags"], ["agent", "python"])
        self.assertEqual(alpha_related[0]["shared_tag_count"], 2)

    def test_respects_max_related_and_never_returns_self(self):
        payload = build_related_index(FIXTURE_DIR, max_related=2)

        for route, related in payload["by_route"].items():
            self.assertLessEqual(len(related), 2)
            self.assertNotIn(route, [entry["route"] for entry in related])

    def test_output_is_byte_stable_and_atomic(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            first = Path(tmp_dir) / "first/index.json"
            second = Path(tmp_dir) / "second/index.json"

            first_payload = build_related_index(FIXTURE_DIR, output_path=first)
            second_payload = build_related_index(FIXTURE_DIR, output_path=second)

            self.assertEqual(first_payload, second_payload)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertTrue(first.read_bytes().endswith(b"\n"))
            self.assertFalse(list(Path(tmp_dir).rglob("*.tmp")))

    def test_rejects_duplicate_routes_instead_of_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            content = Path(tmp_dir)
            for name in ("one", "two"):
                (content / f"{name}.md").write_text(
                    "---\n"
                    f'title: "{name}"\n'
                    "date: 2026-07-01T00:00:00+00:00\n"
                    "url: /same-route/\n"
                    "tags: [Agent]\n"
                    "---\n",
                    encoding="utf-8",
                )

            with self.assertRaises(RelatedIndexValidationError):
                build_related_index(content)

    def test_written_json_contains_no_absolute_source_paths(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "index.json"
            build_related_index(FIXTURE_DIR, output_path=output)

            serialized = output.read_text(encoding="utf-8")
            payload = json.loads(serialized)
            self.assertNotIn(str(FIXTURE_DIR), serialized)
            self.assertRegex(payload["content_sha256"], r"^[0-9a-f]{64}$")

    def test_cli_writes_the_hugo_data_contract(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "related/index.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--content-dir",
                    str(FIXTURE_DIR),
                    "--output",
                    str(output),
                    "--max-related",
                    "2",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )

            summary = json.loads(result.stdout)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(summary["post_count"], 5)
            self.assertEqual(payload["max_related"], 2)
            self.assertIn("/posts/alpha/", payload["by_route"])

    def test_empty_content_and_invalid_options_fail_predictably(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            empty = build_related_index(tmp_dir)
            self.assertEqual(empty["post_count"], 0)
            self.assertIsNone(empty["data_as_of"])

            invalid_options = (
                {"max_related": -1},
                {"candidate_window": 0},
                {"section": "nested/posts"},
            )
            for options in invalid_options:
                with self.subTest(options=options):
                    with self.assertRaises(RelatedIndexValidationError):
                        build_related_index(tmp_dir, **options)

    def test_malformed_frontmatter_and_unsafe_routes_fail_closed(self):
        invalid_documents = {
            "missing-frontmatter.md": "plain text",
            "unterminated.md": "---\ntitle: no closing marker\n",
            "missing-date.md": "---\ntitle: Missing Date\ntags: [Agent]\n---\n",
            "naive-date.md": (
                "---\ntitle: Naive Date\ndate: 2026-07-01T00:00:00\n"
                "tags: [Agent]\n---\n"
            ),
            "bad-tags.md": (
                "---\ntitle: Bad Tags\ndate: 2026-07-01T00:00:00+00:00\n"
                "tags: Agent\n---\n"
            ),
            "external-url.md": (
                "---\ntitle: External\ndate: 2026-07-01T00:00:00+00:00\n"
                "url: https://evil.example/post/\ntags: [Agent]\n---\n"
            ),
        }

        for filename, document in invalid_documents.items():
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as tmp_dir:
                (Path(tmp_dir) / filename).write_text(document, encoding="utf-8")
                with self.assertRaises(RelatedIndexValidationError):
                    build_related_index(tmp_dir)


if __name__ == "__main__":
    unittest.main()
