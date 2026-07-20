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

    def test_source_url_sanitizer_removes_sensitive_queries_only(self):
        document = (
            "---\n"
            "external_url: https://example.com/item?lang=zh&code=temporary-access-value\n"
            "---\n\n"
            "[来源](https://example.com/item?token=temporary-access-value&page=2)\n"
            "[安全查询](https://example.com/list?page=3&sort=new)\n"
        )

        sanitized, removed = (
            self.module.sanitize_sensitive_source_urls_in_markdown_text(text=document)
        )

        self.assertEqual(removed, 2)
        self.assertIn("external_url: https://example.com/item?lang=zh", sanitized)
        self.assertIn("[来源](https://example.com/item?page=2)", sanitized)
        self.assertIn(
            "[安全查询](https://example.com/list?page=3&sort=new)", sanitized
        )

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

    def test_archived_posts_do_not_block_a_fresh_source_contract_capture(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            posts_dir = Path(temp_dir)
            (posts_dir / "archived.md").write_text(
                "\n".join(
                    [
                        "---",
                        'title: "Archived legacy copy"',
                        "archived: true",
                        'external_url: "https://example.com/articles/recover-me"',
                        "---",
                        "",
                        "This body is intentionally no longer publishable.",
                    ]
                ),
                encoding="utf-8",
            )

            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = posts_dir

            self.assertEqual(generator._load_post_index(), [])

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

    def test_source_brief_ignores_generated_translation_and_legacy_tail_leaks(self):
        generated_at = datetime.fromisoformat("2026-07-15T02:00:00+00:00")
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir)
            generator._post_index = []
            item = self._contract(
                {
                    "title": "Safe evidence card",
                    "source": "hacker_news",
                    "url": "https://example.com/safe-evidence-card",
                    "summary": "Crawler metadata is sufficient for a source card.",
                    "tags": ["AI"],
                }
            )
            item["description_translated"] = (
                "这段内容本身就是中文，无需翻译，请告诉我。"
            )
            item["comprehensive_analysis"] = (
                "## 技术分析\n\n2. **如果需要极高的灵活性**：\n\n## 引用\n"
            )

            created = generator._generate_posts(
                {"hacker_news": [item]}, generated_at=generated_at
            )

            self.assertEqual(created, 1)
            document = next(generator.posts_dir.glob("*.md")).read_text(
                encoding="utf-8"
            )
            self.assertNotIn("本身就是中文", document)
            self.assertNotIn("如果需要极高的灵活性", document)
            self.assertNotIn("\n# Safe evidence card\n", document)
            self.assertEqual(self.module.analyze_post(document).fatal_reasons, ())

    def test_source_brief_preserves_the_complete_immutable_crawler_title(self):
        title = (
            "Win by Silence: Deletion Non-Monotonicity, Autonomous Exploitation, "
            "and Typed-State Gating in LLM Plan Evaluation"
        )
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        generator._post_index = []
        item = self._contract(
            {
                "title": title,
                "source": "arxiv",
                "url": "https://arxiv.org/abs/2607.12986v1",
                "summary": "A complete source abstract.",
                "category": "cs.AI",
            }
        )

        document = generator._format_super_enhanced_markdown(
            item,
            generated_at=datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc),
        )
        frontmatter = real_yaml.safe_load(document.split("---", 2)[1])

        self.assertEqual(frontmatter["title"], title)
        self.assertNotIn("Autonomous E\"", document)
        self.assertEqual(generator._source_brief_publication_payload(item)["title"], title)

    def test_source_brief_publishes_the_complete_stored_rss_capture(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        generator._post_index = []
        source_text = (
            "Flo Health evidence paragraph with verified implementation details. " * 220
        ) + "This is the complete final sentence."
        item = self._contract(
            {
                "title": "Complete RSS evidence",
                "source": "blogs_podcasts",
                "url": "https://example.com/complete-rss-evidence",
                "description": source_text,
                "source_is_truncated": False,
                "source_truncation_reason": "",
                "feed_url": "https://example.com/feed.xml",
            }
        )

        self.assertGreater(len(item["source_display_excerpt"].encode("utf-8")), 6_000)
        self.assertEqual(item["source_display_excerpt"], source_text)

        document = generator._format_super_enhanced_markdown(
            item,
            generated_at=datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc),
        )
        frontmatter = real_yaml.safe_load(document.split("---", 2)[1])

        self.assertIn("This is the complete final sentence.", document)
        self.assertFalse(frontmatter["source_is_truncated"])
        self.assertNotIn("source_truncation_reason", frontmatter)
        self.assertEqual(self.module.analyze_post(document).fatal_reasons, ())

    def test_source_brief_bounds_an_extreme_title_at_a_complete_word(self):
        title = ("complete-title-token " * 30) + "final-token"
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        generator._post_index = []
        item = self._contract(
            {
                "title": title,
                "source": "arxiv",
                "url": "https://arxiv.org/abs/2607.12987v1",
                "summary": "A complete source abstract.",
                "category": "cs.AI",
            }
        )

        document = generator._format_super_enhanced_markdown(
            item,
            generated_at=datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc),
        )
        frontmatter = real_yaml.safe_load(document.split("---", 2)[1])

        self.assertEqual(frontmatter["title"], item["source_display_title"])
        self.assertLessEqual(len(frontmatter["title"]), 300)
        self.assertTrue(frontmatter["title"].endswith("complete-title-token"))
        self.assertTrue(frontmatter["source_is_truncated"])
        self.assertIn(
            "publication_title_limit",
            frontmatter["source_truncation_reason"],
        )
        self.assertEqual(
            generator._source_brief_publication_payload(item)["title"],
            item["source_display_title"],
        )

    def test_source_brief_derives_a_bounded_title_when_v1_derivatives_are_missing(self):
        title = ("immutable-title-token " * 30) + "final-token"
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        generator._post_index = []
        item = self._contract(
            {
                "title": title,
                "source": "arxiv",
                "url": "https://arxiv.org/abs/2607.12988v1",
                "summary": "A complete source abstract.",
                "category": "cs.AI",
            }
        )
        expected = item.pop("source_display_title")
        item.pop("source_title_chars_original")

        document = generator._format_super_enhanced_markdown(
            item,
            generated_at=datetime(2026, 7, 15, 2, 0, tzinfo=timezone.utc),
        )
        frontmatter = real_yaml.safe_load(document.split("---", 2)[1])
        publication = generator._source_brief_publication_payload(item)

        self.assertEqual(frontmatter["title"], expected)
        self.assertEqual(publication["title"], expected)
        self.assertLessEqual(len(publication["title"]), 300)
        self.assertEqual(frontmatter["source_title_chars_original"], len(title))

    def test_seo_description_prefers_a_complete_chinese_sentence(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        sentence = (
            "这份说明基于可核验来源，完整交代系统边界、证据范围和部署条件，"
            "同时保留关键指标与风险提示，方便读者快速判断内容价值，"
            "并给出可复现的检查路径、适用条件和清晰结论。"
        )
        description = generator._seo_description(
            {"summary": sentence + ("后续补充信息仍在展开" * 20)}
        )

        self.assertEqual(description, sentence)
        self.assertGreaterEqual(len(description), 80)
        self.assertLessEqual(len(description), 160)

    def test_seo_description_truncates_english_at_a_complete_word(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        description = generator._seo_description(
            {"summary": "evidence-aware systems require careful validation " * 12}
        )

        self.assertLessEqual(len(description), 160)
        self.assertTrue(description.endswith("…"))
        self.assertRegex(description, r"validation…$")
        self.assertNotRegex(description, r"[,，:：;；\-\[(]…$")

    def test_seo_description_truncates_long_chinese_without_spaces_safely(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        description = generator._seo_description(
            {"summary": "知识图谱动态分析能力" * 40}
        )

        self.assertEqual(len(description), 160)
        self.assertTrue(description.endswith("…"))
        self.assertTrue(description[-2].isalpha())

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

    def test_generated_post_persists_hash_bound_lineage_frontmatter(self):
        generator = self.module.SuperEnhancedContentGenerator.__new__(
            self.module.SuperEnhancedContentGenerator
        )
        generator._post_index = []
        item = self._contract(
            {
                "title": "Agent runtime release analysis",
                "source": "blogs_podcasts",
                "url": "https://example.com/analysis/runtime",
                "description": "A source-backed derivative analysis of the runtime release.",
                "feed_url": "https://example.com/feed.xml",
                "published_at": "2026-07-15T10:00:00Z",
            }
        )
        item.update(
            {
                "observation_id": "obs_" + "1" * 64,
                "event_id": "evt_" + "2" * 64,
                "first_seen_at": "2026-07-15T12:00:00Z",
                "lineage_relation": "derivative",
                "parent_observation_id": "obs_" + "3" * 64,
            }
        )

        document = generator._format_super_enhanced_markdown(
            item,
            generated_at=datetime(2026, 7, 15, 13, 0, tzinfo=timezone.utc),
        )
        frontmatter = real_yaml.safe_load(document.split("---", 2)[1])

        self.assertEqual(
            frontmatter["source_payload_sha256"], item["source_payload_sha256"]
        )
        self.assertEqual(frontmatter["observation_id"], item["observation_id"])
        self.assertEqual(frontmatter["event_id"], item["event_id"])
        self.assertEqual(frontmatter["source_published_at"], "2026-07-15T10:00:00Z")
        self.assertEqual(frontmatter["first_seen_at"], "2026-07-15T12:00:00Z")
        self.assertEqual(frontmatter["timestamp_confidence"], "feed")
        self.assertEqual(frontmatter["lineage_relation"], "derivative")
        self.assertEqual(
            frontmatter["parent_observation_id"], item["parent_observation_id"]
        )

    def test_lineage_policy_suppresses_cross_url_exact_copy_before_processing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir) / "posts"
            generator.posts_dir.mkdir()
            generator.lineage_registry_dir = Path(temp_dir) / "lineage-registry"
            source_text = " ".join(f"evidence{index}" for index in range(180))
            origin = self._contract(
                {
                    "title": "Agent Runtime production release",
                    "source": "blogs_podcasts",
                    "url": "https://publisher.example/runtime",
                    "description": source_text,
                    "feed_url": "https://publisher.example/feed.xml",
                    "published_at": "2026-07-15T08:00:00Z",
                }
            )
            mirror = self._contract(
                {
                    "title": "Agent Runtime production release",
                    "source": "blogs_podcasts",
                    "url": "https://mirror.example/runtime",
                    "description": source_text,
                    "feed_url": "https://mirror.example/feed.xml",
                    "published_at": "2026-07-15T09:00:00Z",
                }
            )

            selected = generator._apply_lineage_policy(
                {"blogs_podcasts": [origin, mirror]},
                observations=[origin, mirror],
            )

            self.assertEqual(selected["blogs_podcasts"], [origin])
            self.assertEqual(origin["lineage_relation"], "original")
            self.assertFalse(origin["lineage_suppressed"])
            self.assertEqual(mirror["lineage_relation"], "exact_copy")
            self.assertTrue(mirror["lineage_suppressed"])
            self.assertEqual(origin["event_id"], mirror["event_id"])
            self.assertEqual(mirror["parent_observation_id"], origin["observation_id"])
            self.assertEqual(origin["first_seen_at"], "2026-07-15T12:00:00Z")
            self.assertEqual(origin["last_seen_at"], "2026-07-15T00:00:00Z")
            self.assertTrue(any(generator.lineage_registry_dir.rglob("*.json")))

    def test_lineage_policy_keeps_derivative_as_an_independent_event(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.posts_dir = Path(temp_dir) / "posts"
            generator.posts_dir.mkdir()
            generator.lineage_registry_dir = Path(temp_dir) / "lineage-registry"
            origin_text = " ".join(f"signal{index}" for index in range(150))
            derivative_text = " ".join(f"signal{index}" for index in range(300))
            origin_parent = self._contract(
                {
                    "title": "Research Agent architecture",
                    "source": "juejin",
                    "url": "https://publisher.example/research",
                    "description": "Verified discovery excerpt for the original.",
                    "published_at": "2026-07-15T08:00:00Z",
                }
            )
            analysis_parent = self._contract(
                {
                    "title": "Research Agent architecture explained",
                    "source": "juejin",
                    "url": "https://analyst.example/research",
                    "description": "Verified discovery excerpt for the analysis.",
                    "published_at": "2026-07-16T08:00:00Z",
                }
            )
            origin = self.module.promote_juejin_full_article(origin_parent, origin_text)
            analysis = self.module.promote_juejin_full_article(
                analysis_parent, derivative_text
            )

            selected = generator._apply_lineage_policy(
                {"blogs_podcasts": [origin, analysis]},
                observations=[origin, analysis],
            )

            self.assertEqual(selected["blogs_podcasts"], [origin, analysis])
            self.assertEqual(analysis["lineage_relation"], "derivative")
            self.assertFalse(analysis["lineage_suppressed"])
            self.assertNotEqual(origin["event_id"], analysis["event_id"])
            self.assertEqual(analysis["parent_observation_id"], origin["observation_id"])

    def test_run_never_sends_suppressed_copy_to_the_model_processor(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_text = " ".join(f"source{index}" for index in range(180))
            origin = self._contract(
                {
                    "title": "Runtime release evidence",
                    "source": "blogs_podcasts",
                    "url": "https://publisher.example/release",
                    "description": source_text,
                    "feed_url": "https://publisher.example/feed.xml",
                    "published_at": "2026-07-15T08:00:00Z",
                }
            )
            copy = self._contract(
                {
                    "title": "Runtime release evidence",
                    "source": "blogs_podcasts",
                    "url": "https://mirror.example/release",
                    "description": source_text,
                    "feed_url": "https://mirror.example/feed.xml",
                    "published_at": "2026-07-15T09:00:00Z",
                }
            )

            class FakeCrawler:
                last_observations = [origin, copy]

                @staticmethod
                def crawl_all():
                    return {"blogs_podcasts": [origin, copy]}

            class RecordingProcessor:
                def __init__(self):
                    self.received = None

                def process_by_source(self, value):
                    self.received = value
                    return value

            generator = self.module.SuperEnhancedContentGenerator.__new__(
                self.module.SuperEnhancedContentGenerator
            )
            generator.runtime_profile = "ci"
            generator.crawler = FakeCrawler()
            generator.processor = RecordingProcessor()
            generator.posts_dir = Path(temp_dir) / "posts"
            generator.posts_dir.mkdir()
            generator.lineage_registry_dir = Path(temp_dir) / "lineage"
            generator.max_new_items_per_source = None
            generator._post_index = []
            generator._generate_posts = types.MethodType(
                lambda self, processed, generated_at=None: (
                    setattr(
                        self,
                        "last_generation_stats",
                        {
                            "created": 1,
                            "skipped_existing": 0,
                            "skipped_quality": 0,
                            "contract_failed": 0,
                            "generation_failed": 0,
                        },
                    )
                    or 1
                ),
                generator,
            )
            generator._raise_for_fatal_post_generation_state = types.MethodType(
                lambda self, **kwargs: None, generator
            )
            generator._publish_content = types.MethodType(
                lambda self, processed: None, generator
            )
            original_manifest = self.module.build_content_quality_manifest
            self.module.build_content_quality_manifest = lambda _root: {
                "quarantined_count": 0
            }
            try:
                self.assertTrue(generator.run(sanitize_relrefs=False))
            finally:
                self.module.build_content_quality_manifest = original_manifest

            received = generator.processor.received
            self.assertIsNotNone(received)
            self.assertEqual(received["blogs_podcasts"], [origin])
            self.assertTrue(copy["lineage_suppressed"])

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
