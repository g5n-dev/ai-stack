#!/usr/bin/env python3
"""
Content generation script
内容生成主脚本 - 整合爬虫、处理和推送
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import logging
import argparse
import re
import urllib.parse
import yaml
from typing import Optional

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from runtime_env import load_project_env
load_project_env(project_root)
from runtime_profile import get_runtime_profile

from crawler.main import CrawlerOrchestrator
from processor.main import ProcessorOrchestrator
from processor.markdown_normalizer import remove_markdown_sections_by_heading
from publisher.main import PublisherOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

_RELREF_RE = re.compile(r"""\{\{[<%]\s*relref\s+(['"])(.+?)\1\s*[>%]\}\}""")
_TAXONOMY_MD_LINK_RE = re.compile(r"""\[([^\]]+)\]\(/(tags|categories|scenarios)/([^)]+?)\)""")

_PROMPT_LEAK_KEYWORDS = [
    "评价对象",
    "评价视角",
    "字数控制",
    "输出要求",
    "结构要求",
    "格式要求",
    "写作要求",
    "使用markdown格式组织内容",
    "只输出 JSON",
    "只输出json",
    "只返回",
    "不要其他内容",
    "不要emoji",
    "不要 emoji",
]

_PROMPT_LEAK_LINE_RE = re.compile(
    r"^\s*(?:[-*•]\s*)?(?:\*\*)?"
    r"(评价对象|评价视角|字数控制|输出要求|结构要求|格式要求|写作要求)"
    r"(?:\*\*)?\s*[:：]\s*.+$"
)

_AUTH_FAILURE_HINTS = (
    "401",
    "403",
    "unauthorized",
    "forbidden",
    "authentication",
    "auth",
    "invalid api key",
    "invalid_api_key",
    "身份验证失败",
    "鉴权",
    "api key",
    "access token",
    "token",
)

_COMPAT_FAILURE_HINTS = (
    "no text content found in response blocks",
    "thinking without text",
    "stop_reason=max_tokens",
    "compatibility",
)


def _looks_like_prompt_leak_line(line: str) -> bool:
    s = str(line or "").strip()
    if not s:
        return False
    high_signal = [
        "我们被要求",
        "我们需要生成",
        "我们需要按照格式输出",
        "但我们没有实际的内容",
        "用户忘记",
        "作为助手",
    ]
    if any(k in s for k in high_signal):
        return True
    if len(s) > 260:
        return False
    if _PROMPT_LEAK_LINE_RE.match(s):
        return True
    lowered = s.lower()
    if "使用markdown格式组织内容" in s:
        return True
    if ("只输出" in s and "json" in lowered) or ("不要其他内容" in s):
        return True
    if "只返回" in s and (("内容" in s) or ("案例" in s) or ("json" in lowered)):
        return True
    if ("不要" in s) and (("emoji" in lowered) or ("其他内容" in s) or ("解释" in s)):
        return True
    if ("控制在" in s and "字" in s) and ("以内" in s or "左右" in s) and len(s) <= 60:
        return True
    return any(k in s for k in _PROMPT_LEAK_KEYWORDS)


def sanitize_prompt_leaks_in_markdown_text(*, text: str) -> tuple[str, int]:
    if not text:
        return text, 0

    removed = 0
    out_lines: list[str] = []
    in_frontmatter = False
    frontmatter_done = False
    in_code_fence = False

    lines = text.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()

        if idx == 0 and stripped == "---":
            in_frontmatter = True
            out_lines.append(line)
            continue

        if in_frontmatter:
            out_lines.append(line)
            if stripped == "---":
                in_frontmatter = False
                frontmatter_done = True
            continue

        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            out_lines.append(line)
            continue

        if not frontmatter_done:
            out_lines.append(line)
            continue

        if _looks_like_prompt_leak_line(line):
            removed += 1
            continue

        out_lines.append(line)

    out = "\n".join(out_lines)
    if text.endswith("\n") and not out.endswith("\n"):
        out += "\n"
    return out, removed


def sanitize_prompt_leaks_in_posts(*, posts_dir: Path) -> tuple[int, int]:
    changed_files = 0
    removed_lines_total = 0

    try:
        paths = sorted(posts_dir.glob("*.md"))
    except Exception:
        return 0, 0

    for path in paths:
        try:
            original = path.read_text(encoding="utf-8")
        except Exception:
            continue

        sanitized, removed = sanitize_prompt_leaks_in_markdown_text(text=original)
        if removed <= 0:
            continue

        try:
            path.write_text(sanitized, encoding="utf-8")
        except Exception:
            continue

        changed_files += 1
        removed_lines_total += removed

    return changed_files, removed_lines_total


def sanitize_public_markdown_text(
    *, text: str, validate_security: bool = True
) -> tuple[str, int]:
    if not text:
        return text, 0
    sanitized, removed = remove_markdown_sections_by_heading(
        text, {"思考题", "挑战与思考题"}
    )
    # Imported lazily so lightweight guard tests can load this legacy script
    # without importing the complete crawler/publisher dependency graph.
    if validate_security:
        from content_security import validate_markdown_document

        validate_markdown_document(sanitized)
    return sanitized, removed


def sanitize_public_sections_in_posts(*, posts_dir: Path) -> tuple[int, int]:
    changed_files = 0
    removed_sections_total = 0

    try:
        paths = sorted(posts_dir.glob("*.md"))
    except Exception:
        return 0, 0

    for path in paths:
        try:
            original = path.read_text(encoding="utf-8")
        except Exception:
            continue

        # This maintenance pass predates the strict publishing contract and
        # traverses historical posts that still contain legacy relrefs.  New
        # documents are validated before their first write; historical content
        # is migrated separately and never silently rewritten here.
        sanitized, removed = sanitize_public_markdown_text(
            text=original, validate_security=False
        )
        if removed <= 0:
            continue

        try:
            path.write_text(sanitized, encoding="utf-8")
        except Exception:
            continue

        changed_files += 1
        removed_sections_total += removed

    return changed_files, removed_sections_total


def looks_like_llm_auth_failure(text: str) -> bool:
    s = str(text or "").strip()
    if not s:
        return False
    lowered = s.lower()
    return any(hint in lowered or hint in s for hint in _AUTH_FAILURE_HINTS)


def looks_like_llm_compat_failure(text: str) -> bool:
    s = str(text or "").strip()
    if not s:
        return False
    lowered = s.lower()
    return any(hint in lowered for hint in _COMPAT_FAILURE_HINTS)


def summarize_processed_postability(processed_data: dict) -> dict:
    summary = {
        "total_items": 0,
        "skipped_items": 0,
        "auth_error_items": 0,
        "auth_error_examples": [],
        "compat_error_items": 0,
        "compat_error_examples": [],
        "guard_failed_items": 0,
        "guard_failed_examples": [],
    }

    if not isinstance(processed_data, dict):
        return summary

    for source, items in processed_data.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            summary["total_items"] += 1

            if item.get("skip_post", False):
                summary["skipped_items"] += 1

            reasons = [
                item.get("ai_reason", ""),
                item.get("moderation_reason", ""),
                item.get("processing_error", ""),
            ]
            if any(looks_like_llm_auth_failure(reason) for reason in reasons):
                summary["auth_error_items"] += 1
                if len(summary["auth_error_examples"]) < 3:
                    title = str(item.get("title") or item.get("catchy_title") or "Untitled").strip()
                    summary["auth_error_examples"].append(f"{source}: {title}")
            compat_categories = {
                str(item.get("ai_error_category") or "").strip(),
                str(item.get("moderation_error_category") or "").strip(),
                str(item.get("processing_error_category") or "").strip(),
            }
            if "compatibility" in compat_categories or any(looks_like_llm_compat_failure(reason) for reason in reasons):
                summary["compat_error_items"] += 1
                if len(summary["compat_error_examples"]) < 3:
                    title = str(item.get("title") or item.get("catchy_title") or "Untitled").strip()
                    summary["compat_error_examples"].append(f"{source}: {title}")
            guard_failed_sections = item.get("guard_failed_sections", [])
            if isinstance(guard_failed_sections, list) and guard_failed_sections:
                summary["guard_failed_items"] += 1
                if len(summary["guard_failed_examples"]) < 3:
                    title = str(item.get("title") or item.get("catchy_title") or "Untitled").strip()
                    sections = ",".join(str(x) for x in guard_failed_sections[:3])
                    summary["guard_failed_examples"].append(f"{source}: {title} [{sections}]")

    return summary


def _relref_target_exists(*, content_root: Path, target: str) -> bool:
    raw = str(target or "").strip().strip('"').strip("'").strip()
    if not raw:
        return False

    raw = raw.lstrip("/")

    candidates: list[Path] = []
    base = content_root / raw
    candidates.append(base)

    if base.suffix.lower() != ".md":
        candidates.append(content_root / f"{raw}.md")
        candidates.append(content_root / raw / "_index.md")

    for p in candidates:
        try:
            if p.exists():
                return True
        except Exception:
            continue
    return False


def sanitize_relrefs_in_markdown_text(*, text: str, content_root: Path) -> tuple[str, int]:
    if not text:
        return text, 0

    removed = 0
    out_lines: list[str] = []

    for line in text.splitlines():
        matches = list(_RELREF_RE.finditer(line))
        if not matches:
            out_lines.append(line)
            continue

        broken = False
        for m in matches:
            target = (m.group(2) or "").strip()
            if not _relref_target_exists(content_root=content_root, target=target):
                broken = True
                break

        if broken:
            removed += 1
            continue

        out_lines.append(line)

    out = "\n".join(out_lines)
    if text.endswith("\n") and not out.endswith("\n"):
        out += "\n"
    return out, removed


def sanitize_relrefs_in_posts(*, posts_dir: Path, content_root: Path) -> tuple[int, int]:
    changed_files = 0
    removed_lines_total = 0

    try:
        paths = sorted(posts_dir.glob("*.md"))
    except Exception:
        return 0, 0

    for path in paths:
        try:
            original = path.read_text(encoding="utf-8")
        except Exception:
            continue

        sanitized, removed = sanitize_relrefs_in_markdown_text(text=original, content_root=content_root)
        if removed <= 0:
            continue

        try:
            path.write_text(sanitized, encoding="utf-8")
        except Exception:
            continue

        changed_files += 1
        removed_lines_total += removed

    return changed_files, removed_lines_total


def _taxonomy_term_slug(term: str) -> str:
    s = str(term or "").strip().lower()
    s = re.sub(r"[^\w\s\.-]", " ", s, flags=re.UNICODE)
    s = s.replace("_", "-")
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return urllib.parse.quote(s, safe="-.")


def sanitize_taxonomy_links_in_markdown_text(*, text: str) -> tuple[str, int]:
    if not text:
        return text, 0

    changed = 0

    def _replace(m: re.Match) -> str:
        nonlocal changed
        label = (m.group(1) or "").strip()
        taxonomy = (m.group(2) or "").strip()
        raw_tail = (m.group(3) or "").strip()

        if not label or taxonomy not in {"tags", "categories", "scenarios"}:
            return m.group(0)

        tail = raw_tail.split("#", 1)[0].split("?", 1)[0].strip()
        if tail.endswith("/"):
            tail = tail[:-1]

        expected = _taxonomy_term_slug(label)
        if tail != expected:
            changed += 1
            return f"[{m.group(1)}](/{taxonomy}/{expected}/)"

        return m.group(0)

    out = _TAXONOMY_MD_LINK_RE.sub(_replace, text)
    return out, changed


def sanitize_taxonomy_links_in_posts(*, posts_dir: Path) -> tuple[int, int]:
    changed_files = 0
    changed_links_total = 0

    try:
        paths = sorted(posts_dir.glob("*.md"))
    except Exception:
        return 0, 0

    for path in paths:
        try:
            original = path.read_text(encoding="utf-8")
        except Exception:
            continue

        sanitized, changed_links = sanitize_taxonomy_links_in_markdown_text(text=original)
        if changed_links <= 0:
            continue

        try:
            path.write_text(sanitized, encoding="utf-8")
        except Exception:
            continue

        changed_files += 1
        changed_links_total += changed_links

    return changed_files, changed_links_total


class SuperEnhancedContentGenerator:
    """内容生成器"""

    def __init__(
        self,
        *,
        dedupe: bool = True,
        dedupe_scope: str = "global",
        runtime_profile: Optional[str] = None,
    ):
        self.runtime_profile = get_runtime_profile(runtime_profile)
        self.crawler = CrawlerOrchestrator(
            dedupe=dedupe,
            dedupe_scope=dedupe_scope,
            runtime_profile=self.runtime_profile,
        )
        self.processor = ProcessorOrchestrator(runtime_profile=self.runtime_profile)
        self.publisher = PublisherOrchestrator()
        self.posts_dir = project_root / 'blog' / 'content' / 'posts'

        # 确保 posts 目录存在
        self.posts_dir.mkdir(parents=True, exist_ok=True)
        self._post_index = self._load_post_index()

    def run(
        self,
        *,
        crawl_duration_hours: float = 0,
        crawl_interval_minutes: int = 30,
        sanitize_relrefs: bool = True,
    ):
        """运行完整的超级增强内容生成流程"""
        try:
            logger.info("=" * 80)
            logger.info("Starting content generation process")
            logger.info("Mode: 15+ LLM calls per article")
            logger.info(f"Runtime profile: {self.runtime_profile}")
            logger.info("=" * 80)

            # 1. 爬取内容
            logger.info("\n[1/4] Crawling content from sources...")
            if crawl_duration_hours and crawl_duration_hours > 0:
                crawled_data = self.crawler.crawl_for_duration(
                    duration_hours=crawl_duration_hours,
                    interval_minutes=crawl_interval_minutes,
                )
            else:
                crawled_data = self.crawler.crawl_all()

            total_items = sum(len(items) for items in crawled_data.values())
            logger.info(f"✓ Crawled {total_items} items from {len(crawled_data)} sources")

            # 2. 超级增强处理（15次大模型调用）
            logger.info("\n[2/4] Processing content with AI (15+ LLM calls)...")
            logger.info("    This may take a while.")
            processed_data = self.processor.process_by_source(crawled_data)
            logger.info(f"✓ Super enhanced content from {len(processed_data)} sources")
            postability = summarize_processed_postability(processed_data)

            # 3. 生成超级增强版 Markdown 文章
            logger.info("\n[3/4] Generating Markdown posts...")
            posts_created = self._generate_posts(processed_data)
            logger.info(f"✓ Created {posts_created} Markdown posts")
            self._raise_for_fatal_post_generation_state(
                posts_created=posts_created,
                postability=postability,
            )

            if sanitize_relrefs:
                content_root = project_root / "blog" / "content"
                changed_files, removed_lines = sanitize_relrefs_in_posts(
                    posts_dir=self.posts_dir,
                    content_root=content_root,
                )
                if changed_files > 0:
                    logger.info(f"✓ Sanitized relref links: files={changed_files} lines_removed={removed_lines}")
                changed_files, changed_links = sanitize_taxonomy_links_in_posts(posts_dir=self.posts_dir)
                if changed_files > 0:
                    logger.info(f"✓ Sanitized taxonomy links: files={changed_files} links_fixed={changed_links}")
                changed_files, removed_lines = sanitize_prompt_leaks_in_posts(posts_dir=self.posts_dir)
                if changed_files > 0:
                    logger.info(f"✓ Sanitized prompt leaks: files={changed_files} lines_removed={removed_lines}")
                changed_files, removed_sections = sanitize_public_sections_in_posts(posts_dir=self.posts_dir)
                if changed_files > 0:
                    logger.info(f"✓ Sanitized public-only sections: files={changed_files} sections_removed={removed_sections}")

            # 4. 推送内容
            logger.info("\n[4/4] Publishing to social platforms...")
            self._publish_content(processed_data)

            logger.info("\n" + "=" * 80)
            logger.info("Content generation completed successfully")
            logger.info("Each article contains 15+ AI-generated sections")
            logger.info("=" * 80)

            return True

        except Exception as e:
            logger.error(f"Content generation failed: {e}", exc_info=True)
            return False

    def _raise_for_fatal_post_generation_state(self, *, posts_created: int, postability: dict) -> None:
        total_items = int(postability.get("total_items", 0) or 0)
        auth_error_items = int(postability.get("auth_error_items", 0) or 0)
        compat_error_items = int(postability.get("compat_error_items", 0) or 0)
        guard_failed_items = int(postability.get("guard_failed_items", 0) or 0)

        if posts_created > 0:
            if auth_error_items > 0:
                logger.warning(
                    "Some content failed due to LLM authentication issues: items=%s examples=%s",
                    auth_error_items,
                    ", ".join(postability.get("auth_error_examples", [])) or "n/a",
                )
            if compat_error_items > 0:
                logger.warning(
                    "Some content hit MiniMax compatibility issues: items=%s examples=%s",
                    compat_error_items,
                    ", ".join(postability.get("compat_error_examples", [])) or "n/a",
                )
            if guard_failed_items > 0:
                logger.warning(
                    "Some content failed output guards after regeneration: items=%s examples=%s",
                    guard_failed_items,
                    ", ".join(postability.get("guard_failed_examples", [])) or "n/a",
                )
            return

        if total_items <= 0:
            return

        if auth_error_items > 0:
            examples = ", ".join(postability.get("auth_error_examples", [])) or "n/a"
            raise RuntimeError(
                "LLM authentication failed and no Markdown posts were created. "
                "Check ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL, and ANTHROPIC_MODEL. "
                f"Examples: {examples}"
            )
        if compat_error_items > 0:
            examples = ", ".join(postability.get("compat_error_examples", [])) or "n/a"
            raise RuntimeError(
                "MiniMax compatibility failed and no Markdown posts were created. "
                f"Examples: {examples}"
            )
        if guard_failed_items > 0:
            examples = ", ".join(postability.get("guard_failed_examples", [])) or "n/a"
            raise RuntimeError(
                "Generated content failed output guards and no Markdown posts were created. "
                f"Examples: {examples}"
            )

    def _generate_posts(self, processed_data: dict) -> int:
        """
        生成超级增强版 Markdown 文章文件

        Args:
            processed_data: 处理后的数据

        Returns:
            int: 创建的文章数量
        """
        created_count = 0
        timestamp = datetime.now().strftime('%Y%m%d')

        for source, items in processed_data.items():
            for idx, item in enumerate(items):
                try:
                    if self._should_skip_post(item):
                        continue

                    # 生成文件名
                    slug = self._generate_slug(item.get('title', ''), idx)
                    filename = f"{timestamp}-{source}-{slug}.md"
                    filepath = self.posts_dir / filename

                    # 生成 Markdown 内容
                    markdown_content = self._format_super_enhanced_markdown(item, current_filename=filename)
                    markdown_content, _ = sanitize_public_markdown_text(text=markdown_content)

                    # 写入文件
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)

                    logger.info(f"✓ Created post: {filename}")
                    created_count += 1
                    self._post_index.append(self._post_entry_from_data(filename, item))

                except Exception as e:
                    logger.error(f"Failed to generate post for {item.get('title', 'Unknown')}: {e}")
                    continue

        return created_count

    def _looks_like_meta_disclaimer(self, text: str) -> bool:
        t = str(text or "").strip()
        if not t:
            return False
        banned = [
            "由于您提供",
            "仅为标题",
            "我将基于",
            "我无法从",
            "无法从提供",
            "鉴于您提供",
            "评价对象",
            "评价视角",
            "字数控制",
            "输出要求",
            "结构要求",
            "格式要求",
            "写作要求",
            "使用markdown格式组织内容",
        ]
        return any(w in t for w in banned)

    def _drop_guard_failed_sections(self, item: dict, sections: list[str]) -> list[str]:
        dropped: list[str] = []
        for section in sections:
            name = str(section or "").strip()
            if not name:
                continue
            if name in item:
                item.pop(name, None)
                dropped.append(name)
        if dropped:
            item["guard_dropped_sections"] = dropped
        return dropped

    def _has_publishable_body(self, item: dict) -> bool:
        text_fields = [
            "summary",
            "description_translated",
            "description",
            "deepwiki_content",
            "comprehensive_analysis",
            "analysis",
            "best_practices",
            "comparison_analysis",
            "performance_tips",
            "practical_recommendations",
            "learning_path",
        ]
        for field in text_fields:
            value = str(item.get(field) or "").strip()
            if not value:
                continue
            if self._looks_like_meta_disclaimer(value):
                continue
            return True

        list_fields = [
            "code_examples",
            "case_studies",
            "learning_takeaways",
            "faq",
            "challenges",
            "related_resources",
        ]
        for field in list_fields:
            value = item.get(field)
            if isinstance(value, list) and len(value) > 0:
                return True

        return False

    def _should_skip_post(self, item: dict) -> bool:
        if not isinstance(item, dict):
            return True
        if item.get("skip_post", False):
            return True
        if item.get("ai_related") is False:
            return True
        if item.get("should_publish") is False:
            return True
        guard_failed_sections = [
            str(section).strip()
            for section in (item.get("guard_failed_sections") or [])
            if str(section).strip()
        ]
        for k in [
            "summary",
            "engaging_intro",
            "deep_comment",
            "comprehensive_analysis",
            "analysis",
            "generated_intro",
            "generated_comment",
        ]:
            if self._looks_like_meta_disclaimer(item.get(k, "")):
                if k not in guard_failed_sections:
                    guard_failed_sections.append(k)
        if guard_failed_sections:
            item["guard_failed_sections"] = guard_failed_sections
            dropped_sections = self._drop_guard_failed_sections(item, guard_failed_sections)
            if not self._has_publishable_body(item):
                item["guard_failure_reason"] = f"guard_failed: {', '.join(guard_failed_sections)}"
                return True
            item["guard_failure_reason"] = f"guard_dropped: {', '.join(dropped_sections or guard_failed_sections)}"
        return False

    def _generate_slug(self, title: str, index: int) -> str:
        """生成 URL 友好的 slug"""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')[:50]
        return f"{slug}-{index}"

    def _format_super_enhanced_markdown(self, item: dict, *, current_filename: str | None = None) -> str:
        """
        格式化内容为超级增强版 Markdown（15+ 个章节）

        Args:
            item: 内容项

        Returns:
            str: Markdown 内容
        """
        source = item.get('source', 'unknown')
        raw_title = item.get('catchy_title') or item.get('title_translated') or item.get('title', 'Untitled')
        title = self._sanitize_title_for_seo(raw_title)
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

        # 构建标签
        tags = self._normalize_taxonomy_list(item.get('tags', []))
        tags_str = ', '.join([f'"{self._yaml_escape(tag)}"' for tag in tags])

        # 构建分类
        categories = self._normalize_taxonomy_list(item.get('categories', []))
        categories_str = ', '.join([f'"{self._yaml_escape(cat)}"' for cat in categories])

        scenarios = self._normalize_scenarios(item.get("scenarios"))
        scenarios_str = ', '.join([f'"{self._yaml_escape(s)}"' for s in scenarios])

        # 获取 URL
        url = item.get('url', '')
        if not url and source == 'github_trending':
            url = item.get('repo_url', '')

        # 开始构建 Markdown
        lines = [
            '---',
            f'title: "{self._yaml_escape(title)}"',
            f'date: {date}',
            'draft: false',
            'entry_kind: "auto"',
            f'tags: [{tags_str}]',
            f'categories: [{categories_str}]',
            f'source: {source}',
        ]

        seo_description = self._seo_description(item)
        if seo_description:
            lines.append(f'description: "{self._yaml_escape(seo_description)}"')

        if url:
            lines.append(f'external_url: {url}')
        if scenarios:
            lines.append(f'scenarios: [{scenarios_str}]')

        lines.append('---')
        lines.append('')

        # 根据来源生成不同格式
        if source == 'github_trending':
            lines.extend(self._format_github_repo_super_enhanced(item))
        elif source == 'hacker_news':
            lines.extend(self._format_hacker_news_super_enhanced(item))
        elif source == 'arxiv':
            lines.extend(self._format_arxiv_paper_super_enhanced(item))
        elif source == 'juejin':
            lines.extend(self._format_juejin_article_super_enhanced(item))
        elif source == 'blogs_podcasts':
            lines.extend(self._format_blogs_podcasts_super_enhanced(item))
        elif source == 'twitter':
            lines.extend(self._format_twitter_brief(item))
        else:
            lines.extend(self._format_generic_super_enhanced(item))

        related = self._find_related_posts(item, current_filename=current_filename)
        self._inject_internal_links(lines, item, related)
        return '\n'.join(lines)

    def _sanitize_title_for_seo(self, title: str) -> str:
        t = str(title or "").strip()
        if not t:
            return "Untitled"
        t = re.sub(r"[\U0001F300-\U0001FAFF]", "", t)
        t = re.sub(r"[\u2600-\u27BF]", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        if len(t) > 55:
            t = t[:55].rstrip()
        t = t.rstrip("!！。．. ")
        return t or "Untitled"

    def _strip_markdown_for_seo(self, text: str) -> str:
        t = str(text or "").strip()
        if not t:
            return ""
        t = re.sub(r"```[\s\S]*?```", " ", t)
        t = re.sub(r"`[^`]*`", " ", t)
        t = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", t)
        t = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", t)
        t = re.sub(r"#+\s*", "", t)
        t = re.sub(r">\s*", "", t)
        t = re.sub(r"[\U0001F300-\U0001FAFF]", "", t)
        t = re.sub(r"[\u2600-\u27BF]", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def _seo_description(self, item: dict) -> str:
        if not isinstance(item, dict):
            return ""
        candidates = [
            item.get("summary", ""),
            item.get("engaging_intro", ""),
            item.get("description_translated", ""),
            item.get("description", ""),
        ]
        for c in candidates:
            s = self._strip_markdown_for_seo(c)
            if not s:
                continue
            if self._looks_like_meta_disclaimer(s):
                continue
            if len(s) > 160:
                s = s[:160].rstrip()
            return s
        return ""

    def _yaml_escape(self, text: str) -> str:
        return str(text or "").replace("\\", "\\\\").replace('"', '\\"').strip()

    def _normalize_taxonomy_list(self, value) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            return []
        out: list[str] = []
        for x in value:
            s = str(x or "").strip()
            if not s:
                continue
            if s not in out:
                out.append(s)
        return out

    def _normalize_scenarios(self, value) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            value = [value]
        if isinstance(value, list):
            out: list[str] = []
            for x in value:
                if isinstance(x, str):
                    name = x.strip()
                elif isinstance(x, dict):
                    name = str(x.get("name") or "").strip()
                else:
                    name = str(x or "").strip()
                if not name:
                    continue
                if name not in out:
                    out.append(name)
            return out
        return []

    def _term_slug(self, term: str) -> str:
        return _taxonomy_term_slug(term)

    def _term_link(self, taxonomy: str, term: str) -> str:
        slug = self._term_slug(term)
        return f"/{taxonomy}/{slug}/"

    def _relref(self, content_path: str) -> str:
        p = str(content_path or "").strip().lstrip("/")
        filename = Path(p).name
        if not filename.endswith(".md"):
            return ""
        slug = filename[:-3]
        encoded_slug = urllib.parse.quote(slug, safe="-._~")
        return f"/posts/{encoded_slug}/"

    def _post_entry_from_data(self, filename: str, item: dict) -> dict:
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')
        return {
            "filename": filename,
            "content_path": f"posts/{filename}",
            "title": str(title or "").strip(),
            "tags": self._normalize_taxonomy_list(item.get("tags", [])),
            "categories": self._normalize_taxonomy_list(item.get("categories", [])),
            "scenarios": self._normalize_scenarios(item.get("scenarios")),
        }

    def _post_entry_from_file(self, path: Path) -> dict | None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        except Exception:
            return None

        if not lines or lines[0].strip() != "---":
            return None

        end_idx = None
        for i in range(1, min(len(lines), 200)):
            if lines[i].strip() == "---":
                end_idx = i
                break
        if end_idx is None:
            return None

        fm_text = "\n".join(lines[1:end_idx]).strip()
        if not fm_text:
            return None

        try:
            fm = yaml.safe_load(fm_text) or {}
        except Exception:
            return None

        filename = path.name
        title = str(fm.get("title") or "").strip()
        return {
            "filename": filename,
            "content_path": f"posts/{filename}",
            "title": title,
            "tags": self._normalize_taxonomy_list(fm.get("tags", [])),
            "categories": self._normalize_taxonomy_list(fm.get("categories", [])),
            "scenarios": self._normalize_taxonomy_list(fm.get("scenarios", [])),
        }

    def _load_post_index(self) -> list[dict]:
        posts: list[dict] = []
        try:
            for p in sorted(self.posts_dir.glob("*.md")):
                entry = self._post_entry_from_file(p)
                if entry:
                    posts.append(entry)
        except Exception:
            return []
        return posts

    def _find_related_posts(self, item: dict, *, current_filename: str | None = None) -> list[dict]:
        tags = set(self._normalize_taxonomy_list(item.get("tags", [])))
        categories = set(self._normalize_taxonomy_list(item.get("categories", [])))
        scenarios = set(self._normalize_scenarios(item.get("scenarios")))

        scored: list[tuple[int, dict]] = []
        for p in self._post_index:
            if current_filename and p.get("filename") == current_filename:
                continue
            score = 0
            ptags = set(p.get("tags") or [])
            pcats = set(p.get("categories") or [])
            psc = set(p.get("scenarios") or [])
            score += 2 * len(tags & ptags)
            score += 1 * len(categories & pcats)
            score += 1 * len(scenarios & psc)
            if score <= 0:
                continue
            scored.append((score, p))

        scored.sort(key=lambda x: (-x[0], str(x[1].get("filename") or "")))
        return [p for _, p in scored[:5]]

    def _inject_internal_links(self, lines: list[str], item: dict, related_posts: list[dict]) -> None:
        tags = self._normalize_taxonomy_list(item.get("tags", []))
        categories = self._normalize_taxonomy_list(item.get("categories", []))
        scenarios = self._normalize_scenarios(item.get("scenarios"))

        section: list[str] = []
        section.extend([
            "",
            "---",
            "## 站内链接",
            "",
        ])

        if categories:
            section.append("- 分类： " + " / ".join([f"[{c}]({self._term_link('categories', c)})" for c in categories[:6]]))
        if tags:
            section.append("- 标签： " + " / ".join([f"[{t}]({self._term_link('tags', t)})" for t in tags[:12]]))
        if scenarios:
            section.append("- 场景： " + " / ".join([f"[{s}]({self._term_link('scenarios', s)})" for s in scenarios[:8]]))

        if related_posts:
            section.extend([
                "",
                "### 相关文章",
                "",
            ])
            for p in related_posts:
                title = (p.get("title") or "").strip() or (p.get("filename") or "")
                href = self._relref(p.get("content_path") or "")
                if href:
                    section.append(f"- [{title}]({href})")

        insert_at = len(lines)
        for i in range(len(lines) - 1, -1, -1):
            if "AI Stack 自动生成" in str(lines[i]):
                insert_at = i
                break
        lines[insert_at:insert_at] = section

    def _format_twitter_brief(self, item: dict) -> list:
        account = item.get("account", "unknown")
        account_url = item.get("account_url") or item.get("url") or ""
        tweets = item.get("tweets") or []

        lines = [
            f'# Twitter 简讯：@{account}',
            '',
            '---',
            '',
            '## 信息',
            '',
            f'- **账号**: @{account}',
        ]

        if account_url:
            lines.append(f'- **主页**: [{account_url}]({account_url})')

        lines.extend([
            f'- **收录条数**: {len(tweets)}',
            '',
        ])

        if not tweets:
            lines.extend([
                '暂无可用推文。',
            ])
            self._append_references(lines, item)
            lines.extend([
                '',
                '---',
                '',
                '*本文由 AI Stack 自动生成，观点为 AI 分析，事实以引用链接为准。*',
            ])
            return lines

        lines.extend([
            '---',
            '## 简讯',
        ])

        for idx, t in enumerate(tweets, 1):
            brief = t.get("brief") or {}
            headline = (brief.get("headline") or "").strip()
            url = (t.get("url") or "").strip()
            screenshot = (t.get("screenshot") or "").strip()
            text = (t.get("text") or "").strip()
            timestamp = (t.get("timestamp") or "").strip()

            lines.extend([
                '',
                '---',
                f'### {idx}. {headline or "推文更新"}',
                '',
            ])

            if timestamp:
                lines.append(f'- **时间**: {timestamp}')
            if url:
                lines.append(f'- **原推文**: [{url}]({url})')

            if screenshot:
                lines.extend([
                    '',
                    f'![tweet]({screenshot})',
                ])

            if text:
                quoted_text = text.replace("\n", " ")
                lines.extend([
                    '',
                    '#### 原话',
                    '',
                    f'> {quoted_text}',
                ])

            evidence = brief.get("evidence_snippets") or []
            if isinstance(evidence, list) and evidence:
                lines.extend([
                    '',
                    '#### 证据片段（原文摘录）',
                    '',
                ])
                for s in evidence[:5]:
                    if isinstance(s, str) and s.strip():
                        lines.append(f'- "{s.strip()}"')

            commentary = (brief.get("commentary") or "").strip()
            if commentary:
                lines.extend([
                    '',
                    '#### 点评',
                    '',
                    commentary,
                ])

            background = brief.get("background") or []
            if isinstance(background, list) and background:
                lines.extend([
                    '',
                    '#### 背景',
                    '',
                ])
                for b in background[:6]:
                    if isinstance(b, str) and b.strip():
                        lines.append(f'- {b.strip()}')

            to_verify = brief.get("to_verify") or []
            if isinstance(to_verify, list) and to_verify:
                lines.extend([
                    '',
                    '#### 待核实',
                    '',
                ])
                for v in to_verify[:6]:
                    if isinstance(v, str) and v.strip():
                        lines.append(f'- {v.strip()}')

        self._append_references(lines, item)

        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，观点为 AI 分析，事实以引用链接为准。*',
        ])

        return lines

    def _append_references(self, lines: list, item: dict) -> None:
        """追加引用信息（最小可用：原文/讨论/PDF/DeepWiki/RSS/音频）。"""
        source = item.get("source", "")

        refs: list[tuple[str, str]] = []

        url = item.get("url") or item.get("repo_url") or item.get("external_url") or ""
        if isinstance(url, str):
            url = url.strip()

        if source == "github_trending":
            if url:
                refs.append(("GitHub 仓库", url))
            deepwiki_url = (item.get("deepwiki_url") or "").strip()
            if deepwiki_url:
                refs.append(("DeepWiki", deepwiki_url))
        elif source == "hacker_news":
            if url:
                refs.append(("原文链接", url))
            hn_id = item.get("hn_id")
            if hn_id:
                refs.append(("HN 讨论", f"https://news.ycombinator.com/item?id={hn_id}"))
        elif source == "arxiv":
            if url:
                refs.append(("ArXiv", url))
            pdf_url = (item.get("pdf_url") or "").strip()
            if pdf_url:
                refs.append(("PDF", pdf_url))
        elif source == "blogs_podcasts":
            if url:
                refs.append(("文章/节目", url))
            audio_url = (item.get("audio_url") or "").strip()
            if audio_url:
                refs.append(("音频", audio_url))
            feed_url = (item.get("feed_url") or "").strip()
            if feed_url:
                refs.append(("RSS 源", feed_url))
        elif source == "juejin":
            if url:
                refs.append(("掘金原文", url))
        else:
            if url:
                refs.append(("原文链接", url))

        if not refs:
            return

        lines.extend([
            '',
            '---',
            '## 引用',
            '',
        ])

        for label, link in refs:
            lines.append(f'- **{label}**: [{link}]({link})')

        lines.extend([
            '',
            '> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。',
        ])

    def _format_github_repo_super_enhanced(self, item: dict) -> list:
        """格式化 GitHub 仓库（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')
        original_title = item.get('title', '')
        description = item.get("description_translated") or item.get("description", "")

        lines = [
            f'# {title}',
            '',
            f'> **原名**: {original_title}',
            '',
            '---',
            '',
            '## 基本信息',
            '',
            f'- **描述**: {description}',
            f'- **语言**: {item.get("language", "Unknown")}',
            f'- **星标**: {item.get("stars", "0")} (+{item.get("today_stars", "0")})',
        ]

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        if item.get('deepwiki_url'):
            lines.append(f'- **DeepWiki**: [{item.get("deepwiki_url", "")}]({item.get("deepwiki_url", "")})')

        if item.get('deepwiki_content'):
            lines.extend([
                '',
                '---',
                '## DeepWiki 速览（节选）',
                '',
                item.get('deepwiki_content', ''),
            ])

        # 1. 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## 导语',
                '',
                item.get('engaging_intro', ''),
            ])

        # 2. AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 摘要',
                '',
                item.get('summary', ''),
            ])

        # 3. 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 评论',
                '',
                item.get('deep_comment', ''),
            ])

        # 4. 全面技术分析
        if item.get('comprehensive_analysis'):
            lines.extend([
                '',
                '---',
                '## 技术分析',
                '',
                item.get('comprehensive_analysis', ''),
            ])

        # 5. 代码示例
        if item.get('code_examples'):
            lines.extend([
                '',
                '---',
                '## 代码示例',
                '',
            ])
            for example in item.get('code_examples', []):
                lines.extend([
                    '',
                    example.get('description', ''),
                    '',
                    example.get('code', ''),
                ])

        # 6. 案例研究
        if item.get('case_studies'):
            lines.extend([
                '',
                '---',
                '## 案例研究',
                '',
            ])
            for study in item.get('case_studies', []):
                lines.extend([
                    '',
                    f"### {study.get('title', '案例')}",
                    '',
                    study.get('content', ''),
                ])

        # 7. 对比分析
        if item.get('comparison_analysis'):
            lines.extend([
                '',
                '---',
                '## 对比分析',
                '',
                item.get('comparison_analysis', ''),
            ])

        # 8. 最佳实践
        if item.get('best_practices'):
            lines.extend([
                '',
                '---',
                '## 最佳实践',
                '',
                item.get('best_practices', ''),
            ])

        # 9. 性能优化
        if item.get('performance_tips'):
            lines.extend([
                '',
                '---',
                '## 性能优化建议',
                '',
                item.get('performance_tips', ''),
            ])

        # 10. 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # 11. 学习路径
        if item.get('learning_path'):
            lines.extend([
                '',
                '',
                '---',
                '## 学习路径',
                '',
                item.get('learning_path', ''),
            ])

        # 12. FAQ
        if item.get('faq'):
            lines.extend([
                '',
                '---',
                '## 常见问题',
                '',
            ])
            for faq in item.get('faq', []):
                lines.extend([
                    '',
                    f"### {faq.get('question', 'Question')}",
                    '',
                    faq.get('answer', 'Answer'),
                ])

        # 14. 实践建议
        if item.get('practical_recommendations'):
            lines.extend([
                '',
                '---',
                '## 实践建议',
                '',
                item.get('practical_recommendations', ''),
            ])

        # 15. 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 推荐资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**",
                    f"  - 链接: {resource.get('link', '')}",
                    f"  - 说明: {resource.get('description', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*',
        ])

        return lines

    def _format_hacker_news_super_enhanced(self, item: dict) -> list:
        """格式化 Hacker News 故事（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')

        lines = [
            f'# {title}',
            '',
            '---',
            '',
            '## 基本信息',
            '',
            f'- **作者**: {item.get("author", "")}',
            f'- **评分**: {item.get("score", "0")}',
            f'- **评论数**: {item.get("descendants", "0")}',
        ]

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        if item.get("hn_id"):
            hn_url = f'https://news.ycombinator.com/item?id={item.get("hn_id")}'
            lines.append(f'- **HN 讨论**: [{hn_url}]({hn_url})')

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## 导语',
                '',
                item.get('engaging_intro', ''),
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 摘要',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 评论',
                '',
                item.get('deep_comment', ''),
            ])

        # 代码示例
        if item.get('code_examples'):
            lines.extend([
                '',
                '---',
                '## 代码示例',
                '',
            ])
            for example in item.get('code_examples', []):
                lines.extend([
                    '',
                    example.get('description', ''),
                    '',
                    example.get('code', ''),
                ])

        # 案例研究
        if item.get('case_studies'):
            lines.extend([
                '',
                '---',
                '## 案例研究',
                '',
            ])
            for study in item.get('case_studies', []):
                lines.extend([
                    '',
                    f"### {study.get('title', '案例')}",
                    '',
                    study.get('content', ''),
                ])

        # 最佳实践
        if item.get('best_practices'):
            lines.extend([
                '',
                '---',
                '## 最佳实践',
                '',
                item.get('best_practices', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # FAQ
        if item.get('faq'):
            lines.extend([
                '',
                '---',
                '## 常见问题',
                '',
            ])
            for faq in item.get('faq', []):
                lines.extend([
                    '',
                    f"### {faq.get('question', 'Q')}",
                    '',
                    faq.get('answer', 'A'),
                ])

        # 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 相关资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**: {resource.get('link', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*',
        ])

        return lines

    def _format_blogs_podcasts_super_enhanced(self, item: dict) -> list:
        """格式化博客/播客条目（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')
        description = item.get("description_translated") or item.get("description", "")

        lines = [
            f'# {title}',
            '',
            '---',
            '',
            '## 基本信息',
            '',
            f'- **来源**: {item.get("feed_name", "")} ({item.get("feed_type", "")})',
            f'- **发布时间**: {item.get("published_at") or item.get("published") or ""}',
        ]

        if item.get('url'):
            lines.append(f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})')

        if item.get('audio_url'):
            lines.append(f'- **音频**: [{item.get("audio_url", "")}]({item.get("audio_url", "")})')

        if description:
            lines.extend([
                '',
                '---',
                '## 摘要/简介',
                '',
                description,
            ])

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## 导语',
                '',
                item.get('engaging_intro', ''),
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 摘要',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 评论',
                '',
                item.get('deep_comment', ''),
            ])

        # 全面分析
        if item.get('comprehensive_analysis'):
            lines.extend([
                '',
                '---',
                '## 技术分析',
                '',
                item.get('comprehensive_analysis', ''),
            ])

        # 最佳实践
        if item.get('best_practices'):
            lines.extend([
                '',
                '---',
                '## 最佳实践',
                '',
                item.get('best_practices', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 相关资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**: {resource.get('link', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*',
        ])

        return lines

    def _format_arxiv_paper_super_enhanced(self, item: dict) -> list:
        """格式化 ArXiv 论文（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')

        lines = [
            f'# {title}',
            '',
            '---',
            '',
            '## 基本信息',
            '',
            f'- **ArXiv ID**: {item.get("arxiv_id", "")}',
            f'- **分类**: {item.get("category", "")}',
            f'- **作者**: {", ".join(item.get("authors", [])[:5])}',
        ]

        if item.get('pdf_url'):
            lines.extend([
                f'- **PDF**: [{item.get("pdf_url", "")}]({item.get("pdf_url", "")})',
            ])

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## 导语',
                '',
                item.get('engaging_intro', ''),
            ])

        # 摘要
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 摘要',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 评论',
                '',
                item.get('deep_comment', ''),
            ])

        # 全面分析
        if item.get('comprehensive_analysis'):
            lines.extend([
                '',
                '---',
                '## 技术分析',
                '',
                item.get('comprehensive_analysis', ''),
            ])

        # 最佳实践
        if item.get('best_practices'):
            lines.extend([
                '',
                '---',
                '## 研究最佳实践',
                '',
                item.get('best_practices', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # 学习路径
        if item.get('learning_path'):
            lines.extend([
                '',
                '',
                '---',
                '## 学习路径',
                '',
                item.get('learning_path', ''),
            ])

        # FAQ
        if item.get('faq'):
            lines.extend([
                '',
                '---',
                '## 常见问题',
                '',
            ])
            for faq in item.get('faq', []):
                lines.extend([
                    '',
                    f"### {faq.get('question', 'Q')}",
                    '',
                    faq.get('answer', 'A'),
                ])

        # 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 相关资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**: {resource.get('link', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，深度解读学术研究。*',
        ])

        return lines

    def _format_juejin_article_super_enhanced(self, item: dict) -> list:
        """格式化掘金文章（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')
        description = item.get("description_translated") or item.get("description", "")

        lines = [
            f'# {title}',
            '',
            '---',
            '',
            '## 基本信息',
            '',
            f'- **作者**: {item.get("author", "")}',
        ]

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## 导语',
                '',
                item.get('engaging_intro', ''),
            ])

        # 描述
        if description:
            lines.extend([
                '',
                '---',
                '## 描述',
                '',
                description,
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 摘要',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 评论',
                '',
                item.get('deep_comment', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # FAQ
        if item.get('faq'):
            lines.extend([
                '',
                '---',
                '## 常见问题',
                '',
            ])
            for faq in item.get('faq', []):
                lines.extend([
                    '',
                    f"### {faq.get('question', 'Q')}",
                    '',
                    faq.get('answer', 'A'),
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，提供深度内容分析。*',
        ])

        return lines

    def _format_generic_super_enhanced(self, item: dict) -> list:
        """格式化通用内容（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')

        lines = [
            f'# {title}',
            '',
            '---',
            '',
            '## 基本信息',
            '',
        ]

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## 导语',
                '',
                item.get('engaging_intro', ''),
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 摘要',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 评论',
                '',
                item.get('deep_comment', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 相关资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**: {resource.get('link', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成。*',
        ])

        return lines

    def _publish_content(self, processed_data: dict):
        """
        推送内容到社交平台

        Args:
            processed_data: 处理后的数据
        """
        enabled_platforms = self.publisher.get_enabled_platforms()

        if not enabled_platforms:
            logger.info("No publishing platforms enabled")
            return

        # 只推送每个来源的前几篇内容
        for source, items in processed_data.items():
            for item in items[:2]:  # 每个来源最多推送2篇
                try:
                    logger.info(f"Publishing {source} item to {enabled_platforms}...")
                    results = self.publisher.publish_all(item)

                    for platform, success in results.items():
                        if success:
                            logger.info(f"Successfully published to {platform}")
                        else:
                            logger.warning(f"Failed to publish to {platform}")

                except Exception as e:
                    logger.error(f"Failed to publish item: {e}")
                    continue


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AI Stack content generator")
    parser.add_argument("--crawl-duration-hours", type=float, default=0, help="长时间抓取（小时），0 表示单次抓取")
    parser.add_argument("--crawl-interval-minutes", type=int, default=30, help="长时间抓取时的间隔（分钟）")
    parser.add_argument("--no-dedupe", action="store_true", help="关闭去重")
    parser.add_argument(
        "--dedupe-scope",
        choices=["global", "per_source"],
        default="global",
        help="去重范围：global=跨数据源去重，per_source=仅同数据源去重",
    )
    parser.add_argument(
        "--sanitize-relrefs-only",
        action="store_true",
        help="仅清理失效 relref，不运行抓取/处理/推送",
    )
    parser.add_argument(
        "--no-sanitize-relrefs",
        action="store_true",
        help="关闭 relref 清理",
    )
    parser.add_argument(
        "--runtime-profile",
        default=None,
        help="运行档位：default（本地完整模式）或 ci（GitHub Actions 轻量模式）",
    )

    args = parser.parse_args()

    if args.sanitize_relrefs_only:
        content_root = project_root / "blog" / "content"
        posts_dir = content_root / "posts"
        changed_files, removed_lines = sanitize_relrefs_in_posts(posts_dir=posts_dir, content_root=content_root)
        if changed_files > 0:
            logger.info(f"✓ Sanitized relref links: files={changed_files} lines_removed={removed_lines}")
        else:
            logger.info("✓ Relref links OK")
        changed_files, changed_links = sanitize_taxonomy_links_in_posts(posts_dir=posts_dir)
        if changed_files > 0:
            logger.info(f"✓ Sanitized taxonomy links: files={changed_files} links_fixed={changed_links}")
        else:
            logger.info("✓ Taxonomy links OK")
        changed_files, removed_lines = sanitize_prompt_leaks_in_posts(posts_dir=posts_dir)
        if changed_files > 0:
            logger.info(f"✓ Sanitized prompt leaks: files={changed_files} lines_removed={removed_lines}")
        else:
            logger.info("✓ Prompt leaks OK")
        changed_files, removed_sections = sanitize_public_sections_in_posts(posts_dir=posts_dir)
        if changed_files > 0:
            logger.info(f"✓ Sanitized public-only sections: files={changed_files} sections_removed={removed_sections}")
        else:
            logger.info("✓ Public-only sections OK")
        return 0

    generator = SuperEnhancedContentGenerator(
        dedupe=not args.no_dedupe,
        dedupe_scope=args.dedupe_scope,
        runtime_profile=args.runtime_profile,
    )
    success = generator.run(
        crawl_duration_hours=args.crawl_duration_hours,
        crawl_interval_minutes=args.crawl_interval_minutes,
        sanitize_relrefs=not args.no_sanitize_relrefs,
    )

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
