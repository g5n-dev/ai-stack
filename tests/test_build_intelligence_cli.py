#!/usr/bin/env python3

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "intelligence_events.json"
SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "build_intelligence.py"
SCRIPT_SPEC = importlib.util.spec_from_file_location("build_intelligence_cli", SCRIPT_PATH)
if SCRIPT_SPEC is None or SCRIPT_SPEC.loader is None:
    raise RuntimeError("unable to load build_intelligence.py")
SCRIPT_MODULE = importlib.util.module_from_spec(SCRIPT_SPEC)
SCRIPT_SPEC.loader.exec_module(SCRIPT_MODULE)
main = SCRIPT_MODULE.main


class BuildIntelligenceCliTest(unittest.TestCase):
    def test_builds_static_api_and_prints_machine_readable_result(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = main(
                    [
                        "--input",
                        str(FIXTURE_PATH),
                        "--output",
                        tmp_dir,
                        "--as-of",
                        "2026-07-13T12:00:00Z",
                        "--max-items-per-shard",
                        "2",
                        "--max-shard-bytes",
                        "2048",
                    ]
                )

            result = json.loads(output.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp_dir) / result["root_manifest_path"]).is_file())
            self.assertTrue((Path(tmp_dir) / result["release_manifest_path"]).is_file())

    def test_fails_closed_for_invalid_input_without_creating_manifest(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            invalid_path = Path(tmp_dir) / "invalid.json"
            invalid_path.write_text('{"events":"not-an-array"}', encoding="utf-8")
            output_dir = Path(tmp_dir) / "public"
            errors = io.StringIO()

            with contextlib.redirect_stderr(errors):
                exit_code = main(
                    [
                        "--input",
                        str(invalid_path),
                        "--output",
                        str(output_dir),
                        "--as-of",
                        "2026-07-13T12:00:00Z",
                    ]
                )

            self.assertEqual(exit_code, 2)
            self.assertIn("events must be an array of objects", errors.getvalue())
            self.assertFalse((output_dir / "api/v1/manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
