#!/usr/bin/env python3

import importlib.util
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def _load_module():
    fake_runtime_env = types.ModuleType("runtime_env")
    fake_runtime_env.load_project_env = lambda *args, **kwargs: None

    fake_yaml = types.ModuleType("yaml")
    fake_yaml.safe_load = lambda *args, **kwargs: {}

    fake_crawler_main = types.ModuleType("crawler.main")
    fake_crawler_main.CrawlerOrchestrator = object
    fake_processor_main = types.ModuleType("processor.main")
    fake_processor_main.ProcessorOrchestrator = object
    fake_markdown_normalizer = types.ModuleType("processor.markdown_normalizer")
    fake_markdown_normalizer.remove_markdown_sections_by_heading = lambda text, headings: (text, 0)
    fake_publisher_main = types.ModuleType("publisher.main")
    fake_publisher_main.PublisherOrchestrator = object

    fake_crawler_pkg = types.ModuleType("crawler")
    fake_processor_pkg = types.ModuleType("processor")
    fake_publisher_pkg = types.ModuleType("publisher")

    saved = {
        name: sys.modules.get(name)
        for name in [
            "runtime_env",
            "yaml",
            "crawler",
            "crawler.main",
            "processor",
            "processor.main",
            "processor.markdown_normalizer",
            "publisher",
            "publisher.main",
        ]
    }

    sys.modules["runtime_env"] = fake_runtime_env
    sys.modules["yaml"] = fake_yaml
    sys.modules["crawler"] = fake_crawler_pkg
    sys.modules["crawler.main"] = fake_crawler_main
    sys.modules["processor"] = fake_processor_pkg
    sys.modules["processor.main"] = fake_processor_main
    sys.modules["processor.markdown_normalizer"] = fake_markdown_normalizer
    sys.modules["publisher"] = fake_publisher_pkg
    sys.modules["publisher.main"] = fake_publisher_main

    try:
        spec = importlib.util.spec_from_file_location(
            "generate_content_test",
            ROOT / "scripts" / "generate_content.py",
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("Failed to load generate_content.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for name, previous in saved.items():
            if previous is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous


class GenerateContentGuardsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = _load_module()

    def test_detects_auth_failure_reason(self):
        self.assertTrue(self.module.looks_like_llm_auth_failure("Error code: 401 - 身份验证失败"))
        self.assertTrue(self.module.looks_like_llm_auth_failure("403 Forbidden"))
        self.assertFalse(self.module.looks_like_llm_auth_failure("timeout while reading response"))

    def test_summarizes_auth_failed_items(self):
        summary = self.module.summarize_processed_postability(
            {
                "github_trending": [
                    {
                        "title": "repo-a",
                        "skip_post": True,
                        "moderation_reason": "Error: Error code: 401 - {'message': '身份验证失败。'}",
                    },
                    {
                        "title": "repo-b",
                        "skip_post": True,
                        "moderation_reason": "fallback: 非AI或不确定",
                    },
                ]
            }
        )

        self.assertEqual(summary["total_items"], 2)
        self.assertEqual(summary["skipped_items"], 2)
        self.assertEqual(summary["auth_error_items"], 1)
        self.assertEqual(summary["auth_error_examples"], ["github_trending: repo-a"])

    def test_raise_for_fatal_post_generation_state_on_auth_failure(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(self.module.SuperEnhancedContentGenerator)

        with self.assertRaisesRegex(RuntimeError, "LLM authentication failed and no Markdown posts were created"):
            generator._raise_for_fatal_post_generation_state(
                posts_created=0,
                postability={
                    "total_items": 5,
                    "auth_error_items": 3,
                    "auth_error_examples": ["github_trending: repo-a"],
                },
            )

    def test_no_raise_when_posts_exist(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(self.module.SuperEnhancedContentGenerator)

        generator._raise_for_fatal_post_generation_state(
            posts_created=1,
            postability={
                "total_items": 5,
                "auth_error_items": 3,
                "auth_error_examples": ["github_trending: repo-a"],
            },
        )


if __name__ == "__main__":
    unittest.main()
