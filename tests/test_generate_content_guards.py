#!/usr/bin/env python3

import importlib.util
import hashlib
import sys
import tempfile
import types
import unittest
from datetime import datetime, timezone
from pathlib import Path

import yaml as real_yaml


ROOT = Path(__file__).resolve().parent.parent


def _load_module():
    fake_runtime_env = types.ModuleType("runtime_env")
    fake_runtime_env.load_project_env = lambda *args, **kwargs: None

    fake_yaml = types.ModuleType("yaml")
    fake_yaml.safe_load = real_yaml.safe_load

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

    def _contract(self, item):
        prepared = dict(item)
        prepared.setdefault("crawled_at", "2026-07-15T12:00:00Z")
        if prepared.get("source") == "hacker_news":
            prepared.setdefault("hn_id", 1)
        return self.module.apply_source_contract(prepared)

    def test_detects_auth_failure_reason(self):
        self.assertTrue(self.module.looks_like_llm_auth_failure("Error code: 401 - 身份验证失败"))
        self.assertTrue(self.module.looks_like_llm_auth_failure("403 Forbidden"))
        self.assertFalse(self.module.looks_like_llm_auth_failure("timeout while reading response"))

    def test_detects_compat_failure_reason(self):
        self.assertTrue(self.module.looks_like_llm_compat_failure("No text content found in response blocks: ['thinking']"))
        self.assertTrue(self.module.looks_like_llm_compat_failure("LLM request failed (compatibility, purpose=classification)"))
        self.assertFalse(self.module.looks_like_llm_compat_failure("403 Forbidden"))

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

    def test_summarizes_compat_and_guard_failed_items(self):
        summary = self.module.summarize_processed_postability(
            {
                "github_trending": [
                    {
                        "title": "repo-a",
                        "skip_post": True,
                        "moderation_reason": "LLM request failed (compatibility, purpose=classification)",
                        "moderation_error_category": "compatibility",
                    },
                    {
                        "title": "repo-b",
                        "skip_post": True,
                        "guard_failed_sections": ["engaging_intro", "deep_comment"],
                    },
                ]
            }
        )

        self.assertEqual(summary["compat_error_items"], 1)
        self.assertEqual(summary["compat_error_examples"], ["github_trending: repo-a"])
        self.assertEqual(summary["guard_failed_items"], 1)
        self.assertEqual(summary["guard_failed_examples"], ["github_trending: repo-b [engaging_intro,deep_comment]"])

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

    def test_empty_crawl_is_fatal_instead_of_green_success(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )

        with self.assertRaisesRegex(RuntimeError, "Crawler returned no items"):
            generator._validate_crawled_data(
                {
                    "github_trending": [],
                    "hacker_news": [],
                    "arxiv_ai": [],
                }
            )

    def test_raise_for_fatal_post_generation_state_on_compat_failure(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(self.module.SuperEnhancedContentGenerator)

        with self.assertRaisesRegex(RuntimeError, "MiniMax compatibility failed and no Markdown posts were created"):
            generator._raise_for_fatal_post_generation_state(
                posts_created=0,
                postability={
                    "total_items": 4,
                    "compat_error_items": 2,
                    "compat_error_examples": ["github_trending: repo-a"],
                },
            )

    def test_raise_for_fatal_post_generation_state_on_guard_failure(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(self.module.SuperEnhancedContentGenerator)

        with self.assertRaisesRegex(RuntimeError, "Generated content failed output guards and no Markdown posts were created"):
            generator._raise_for_fatal_post_generation_state(
                posts_created=0,
                postability={
                    "total_items": 4,
                    "guard_failed_items": 2,
                    "guard_failed_examples": ["github_trending: repo-b [engaging_intro]"],
                },
            )

    def test_raise_for_fatal_post_generation_state_on_provenance_failure(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )

        with self.assertRaisesRegex(RuntimeError, "failed the provenance gate"):
            generator._raise_for_fatal_post_generation_state(
                posts_created=0,
                postability={"total_items": 1},
                quality_failed_items=1,
            )

    def test_raise_for_fatal_post_generation_state_on_contract_failure(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )

        with self.assertRaisesRegex(RuntimeError, "source contract"):
            generator._raise_for_fatal_post_generation_state(
                posts_created=0,
                postability={"total_items": 1},
                contract_failed_items=1,
            )

    def test_should_not_skip_post_when_guard_failed_sections_are_dropped(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(self.module.SuperEnhancedContentGenerator)
        item = {
            "title": "repo-a",
            "summary": "这是一段正常摘要，仍然足够支撑文章发布。",
            "engaging_intro": "由于您提供的标题有限，我将基于常见技术写法生成内容。",
            "deep_comment": "由于您提供的内容有限，我只能给出泛化评价。",
            "guard_failed_sections": ["engaging_intro", "deep_comment"],
        }

        should_skip = generator._should_skip_post(item)

        self.assertFalse(should_skip)
        self.assertEqual(item["guard_dropped_sections"], ["engaging_intro", "deep_comment"])
        self.assertNotIn("engaging_intro", item)
        self.assertNotIn("deep_comment", item)
        self.assertEqual(item["guard_failure_reason"], "guard_dropped: engaging_intro, deep_comment")

    def test_should_skip_post_when_guard_failed_sections_leave_no_publishable_body(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(self.module.SuperEnhancedContentGenerator)
        item = {
            "title": "repo-a",
            "engaging_intro": "由于您提供的标题有限，我将基于常见技术写法生成内容。",
            "deep_comment": "由于您提供的内容有限，我只能给出泛化评价。",
            "guard_failed_sections": ["engaging_intro", "deep_comment"],
        }

        should_skip = generator._should_skip_post(item)

        self.assertTrue(should_skip)
        self.assertEqual(item["guard_dropped_sections"], ["engaging_intro", "deep_comment"])
        self.assertEqual(item["guard_failure_reason"], "guard_failed: engaging_intro, deep_comment")

    def test_public_markdown_guard_accepts_safe_complete_document(self):
        document = (
            "---\n"
            "title: Safe post\n"
            "date: 2026-07-13\n"
            "external_url: https://example.com/source\n"
            "---\n\n"
            "## Summary\n\n[Source](https://example.com/source)\n"
        )

        sanitized, removed = self.module.sanitize_public_markdown_text(text=document)

        self.assertEqual(sanitized, document)
        self.assertEqual(removed, 0)

    def test_public_markdown_guard_fails_closed_before_write(self):
        document = (
            "---\n"
            "title: Unsafe post\n"
            "date: 2026-07-13\n"
            "---\n\n"
            "[click](javascript:alert(1))\n"
        )

        with self.assertRaisesRegex(ValueError, "unsafe-url"):
            self.module.sanitize_public_markdown_text(text=document)

    def test_prompt_sanitizer_preserves_matching_text_inside_code_fences(self):
        document = (
            "---\ntitle: Fence\n---\n\n"
            "```text\n输出要求：这是测试字符串\n```\n"
        )

        sanitized, removed = self.module.sanitize_prompt_leaks_in_markdown_text(
            text=document
        )

        self.assertEqual(sanitized, document)
        self.assertEqual(removed, 0)

    def test_related_post_links_do_not_emit_hugo_shortcodes(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )

        link = generator._relref(
            "posts/20260713-hacker_news-safe-project-0.md"
        )

        self.assertEqual(
            link,
            "/posts/20260713-hacker_news-safe-project-0/",
        )
        self.assertNotIn("{{", link)

    def test_filters_historical_canonical_urls_before_per_source_limit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            posts_dir = Path(temp_dir)
            (posts_dir / "20260714-hacker_news-seen-0.md").write_text(
                "\n".join(
                    [
                        "---",
                        'title: "Seen"',
                        "date: 2026-07-14T08:00:00+08:00",
                        'external_url: "https://Example.com/articles/seen/?utm_source=archive"',
                        "---",
                        "",
                        "Already archived.",
                    ]
                ),
                encoding="utf-8",
            )

            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = posts_dir
            generator._post_index = generator._load_post_index()
            crawled = {
                "hacker_news": [
                    {
                        "title": "Seen again",
                        "url": "https://example.com/articles/seen#discussion",
                    },
                    {"title": "New one", "url": "https://example.com/articles/new-1"},
                    {"title": "New two", "url": "https://example.com/articles/new-2"},
                    {"title": "New three", "url": "https://example.com/articles/new-3"},
                ]
            }

            selected = generator._filter_unseen_crawled_data(
                crawled,
                max_items_per_source=2,
            )

            self.assertEqual(
                [item["url"] for item in selected["hacker_news"]],
                [
                    "https://example.com/articles/new-1",
                    "https://example.com/articles/new-2",
                ],
            )

    def test_generated_frontmatter_uses_shared_tag_and_url_canonicalization(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        generator._post_index = []

        document = generator._format_super_enhanced_markdown(
            {
                "title": "Canonical metadata",
                "source": "hacker_news",
                "url": (
                    "https://Example.com:443/story/?b=2&utm_source=feed&a=1#fragment"
                ),
                "summary": "A safe source summary.",
                "tags": [" AI编程 ", "AI 编程", "VibeCoding", "Vibe Coding"],
                "categories": ["News"],
            },
            generated_at=datetime(2026, 7, 15, tzinfo=timezone.utc),
        )
        frontmatter = real_yaml.safe_load(document.split("---", 2)[1])

        self.assertEqual(
            frontmatter["external_url"],
            "https://example.com/story?a=1&b=2",
        )
        self.assertEqual(frontmatter["tags"], ["AI 编程", "Vibe Coding"])
        self.assertEqual(
            self.module.canonicalize_content_url(
                "https://Example.com:443/story/?b=2&utm_source=feed&a=1#fragment"
            ),
            "https://example.com/story?a=1&b=2",
        )

    def test_invalid_content_url_fails_closed_before_frontmatter_is_built(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        generator._post_index = []

        with self.assertRaisesRegex(ValueError, "valid canonical source URL"):
            generator._format_super_enhanced_markdown(
                {
                    "title": "Invalid source",
                    "source": "unknown",
                    "url": "javascript:alert(1)",
                    "summary": "A safe summary without a usable source URL.",
                    "tags": ["AI编程"],
                },
                generated_at=datetime(2026, 7, 15, tzinfo=timezone.utc),
            )
        self.assertEqual(
            self.module.canonicalize_content_url("javascript:alert(1)"),
            "",
        )

    def test_explicit_utc_generation_time_crosses_into_shanghai_next_day(self):
        generated_at = datetime(2026, 7, 14, 16, 30, tzinfo=timezone.utc)
        local_now = self.module.content_now(generated_at)

        self.assertIs(local_now.tzinfo, self.module.SHANGHAI_TZ)
        self.assertEqual(local_now.isoformat(), "2026-07-15T00:30:00+08:00")

        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir)
            generator._post_index = []

            created = generator._generate_posts(
                {
                    "hacker_news": [
                        self._contract({
                            "title": "Midnight AI",
                            "source": "hacker_news",
                            "url": "https://example.com/midnight-ai",
                            "summary": "A safe AI summary.",
                            "tags": ["AI"],
                            "categories": ["News"],
                        })
                    ]
                },
                generated_at=generated_at,
            )

            files = list(generator.posts_dir.glob("*.md"))
            self.assertEqual(created, 1)
            identity = hashlib.sha256(
                b"https://example.com/midnight-ai"
            ).hexdigest()[:10]
            self.assertEqual(
                [path.name for path in files],
                [f"20260715-hacker_news-midnight-ai-0-{identity}.md"],
            )
            self.assertIn(
                "date: 2026-07-15T00:30:00+08:00",
                files[0].read_text(encoding="utf-8"),
            )

    def test_existing_target_file_is_not_overwritten_or_counted_as_created(self):
        generated_at = datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir)
            generator._post_index = []
            identity = hashlib.sha256(
                b"https://example.com/existing-target"
            ).hexdigest()[:10]
            target = generator.posts_dir / (
                f"20260715-hacker_news-existing-target-0-{identity}.md"
            )
            original = b"existing immutable article\n"
            target.write_bytes(original)

            created = generator._generate_posts(
                {
                    "hacker_news": [
                        self._contract({
                            "title": "Existing target",
                            "source": "hacker_news",
                            "url": "https://example.com/existing-target",
                            "summary": "Replacement content must not be written.",
                        })
                    ]
                },
                generated_at=generated_at,
            )

            self.assertEqual(created, 0)
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(generator.last_generation_stats["generation_failed"], 1)
            self.assertEqual(generator.last_generation_stats["skipped_existing"], 0)

    def test_same_day_same_title_uses_url_identity_instead_of_silently_colliding(self):
        generated_at = datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir)
            generator._post_index = []

            first = self._contract({
                "title": "Same AI title",
                "source": "hacker_news",
                "url": "https://example.com/story-a",
                "summary": "First source-backed item.",
            })
            second = self._contract({
                "title": "Same AI title",
                "source": "hacker_news",
                "url": "https://example.com/story-b",
                "summary": "Second source-backed item.",
            })

            self.assertEqual(
                generator._generate_posts(
                    {"hacker_news": [first]}, generated_at=generated_at
                ),
                1,
            )
            self.assertEqual(
                generator._generate_posts(
                    {"hacker_news": [second]}, generated_at=generated_at
                ),
                1,
            )

            files = sorted(generator.posts_dir.glob("*.md"))
            self.assertEqual(len(files), 2)
            self.assertNotEqual(files[0].name, files[1].name)
            self.assertEqual(
                {
                    generator._post_entry_from_file(path)["external_url"]
                    for path in files
                },
                {
                    "https://example.com/story-a",
                    "https://example.com/story-b",
                },
            )

    def test_source_brief_drops_prompt_context_leaks_in_generated_fields(self):
        generated_at = datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir)
            generator._post_index = []

            created = generator._generate_posts(
                {
                    "hacker_news": [
                        self._contract({
                            "title": "Unverifiable analysis",
                            "source": "hacker_news",
                            "url": "https://example.com/unverifiable",
                            "summary": (
                                "你在提示词中没有提供完整正文，因此以下内容只能根据标题推演。"
                            ),
                            "tags": ["AI"],
                            "categories": ["News"],
                        })
                    ]
                },
                generated_at=generated_at,
            )

            self.assertEqual(created, 1)
            document = next(generator.posts_dir.glob("*.md")).read_text(encoding="utf-8")
            self.assertNotIn("你在提示词中没有提供", document)
            self.assertIn("## 来源说明", document)
            self.assertEqual(generator.last_generation_stats["skipped_quality"], 0)

    def test_source_brief_drops_truncated_generated_code_sections(self):
        generated_at = datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir)
            generator._post_index = []

            created = generator._generate_posts(
                {
                    "hacker_news": [
                        self._contract({
                            "title": "Truncated code",
                            "source": "hacker_news",
                            "url": "https://example.com/truncated-code",
                            "summary": "A safe summary backed by the source.",
                            "code_examples": [
                                {
                                    "description": "Incomplete example",
                                    "code": "```python\nprint('cut')",
                                }
                            ],
                            "tags": ["AI"],
                            "categories": ["News"],
                        })
                    ]
                },
                generated_at=generated_at,
            )

            self.assertEqual(created, 1)
            document = next(generator.posts_dir.glob("*.md")).read_text(encoding="utf-8")
            self.assertNotIn("print('cut')", document)
            self.assertNotIn("## 代码示例", document)
            self.assertEqual(generator.last_generation_stats["skipped_quality"], 0)

    def test_metadata_only_hn_writes_only_a_tier_c_source_card(self):
        generated_at = datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir)
            generator._post_index = []
            item = self._contract({
                "title": "Evidence-first AI agents",
                "source": "hacker_news",
                "url": "https://example.com/evidence-first",
                "author": "ada",
                "score": 42,
                "descendants": 7,
                "hn_id": 123,
                "crawled_at": "2026-07-15T12:00:00Z",
                "source_note": "Untrusted generated analysis must not be published.",
                "deep_comment": "This generated section must never be rendered.",
                "code_examples": [{"description": "bad", "code": "print('bad')"}],
            })
            item["catchy_title"] = "Untrusted rewritten title"
            item["author"] = "untrusted-author"
            item["score"] = 9999

            created = generator._generate_posts(
                {"hacker_news": [item]}, generated_at=generated_at
            )

            self.assertEqual(created, 1)
            document = next(generator.posts_dir.glob("*.md")).read_text(encoding="utf-8")
            frontmatter = real_yaml.safe_load(document.split("---", 2)[1])
            self.assertEqual(frontmatter["content_mode"], "source_brief")
            self.assertEqual(frontmatter["publication_tier"], "C")
            self.assertTrue(frontmatter["source_snapshot_sha256"].startswith("sha256:"))
            self.assertIn("## 基本信息", document)
            self.assertIn("## 来源说明", document)
            self.assertNotIn("## 评论", document)
            self.assertNotIn("## 代码示例", document)
            self.assertNotIn("This generated section", document)
            self.assertNotIn("Untrusted rewritten title", document)
            self.assertNotIn("untrusted-author", document)
            self.assertNotIn("9999", document)
            self.assertNotIn("Untrusted generated analysis", document)
            self.assertEqual(item["_publication_gate"], "passed")
            self.assertNotIn(
                "Untrusted generated analysis",
                item["_publication_payload"]["summary"],
            )

    def test_generate_posts_rejects_items_without_a_crawler_contract(self):
        generated_at = datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir)
            generator._post_index = []

            created = generator._generate_posts(
                {
                    "hacker_news": [
                        {
                            "title": "LLM source without evidence",
                            "source": "hacker_news",
                            "url": "https://example.com/no-contract",
                        }
                    ]
                },
                generated_at=generated_at,
            )

            self.assertEqual(created, 0)
            self.assertEqual(list(generator.posts_dir.glob("*.md")), [])

    def test_social_publish_only_receives_items_that_passed_markdown_gate(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )

        class Publisher:
            def __init__(self):
                self.items = []

            def get_enabled_platforms(self):
                return ["telegram"]

            def publish_all(self, item):
                self.items.append(item)
                return {"telegram": True}

        generator.publisher = Publisher()
        passed = {
            "title": "passed",
            "summary": "untrusted generated summary",
            "_publication_gate": "passed",
            "_publication_payload": {
                "title": "passed",
                "summary": "来源证据快报",
                "url": "https://example.com/passed",
                "source": "hacker_news",
                "tags": ["AI"],
                "content_mode": "source_brief",
                "publication_tier": "C",
                "source_snapshot_sha256": "sha256:" + "a" * 64,
            },
        }
        generator._publish_content(
            {"hacker_news": [{"title": "blocked"}, passed]}
        )

        self.assertEqual(generator.publisher.items, [passed["_publication_payload"]])
        self.assertNotIn("untrusted generated summary", generator.publisher.items[0].values())


if __name__ == "__main__":
    unittest.main()
