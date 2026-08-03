#!/usr/bin/env python3
"""
Content generation script
内容生成主脚本 - 整合爬虫、处理和推送
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
import argparse
import hashlib
import html
import re
import urllib.parse
import yaml
from typing import Any, Optional

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from runtime_env import load_project_env
load_project_env(project_root)
from runtime_profile import get_runtime_profile

from ai_stack.content_quality import (
    INTERPRETATION_HEADING,
    analyze_post,
    build_content_quality_manifest,
)
from ai_stack.identity import canonicalize_url
from ai_stack.lineage import (
    LineageRegistry,
    LineageValidationError,
    observation_from_contract,
    parse_historical_post,
)
from ai_stack.source_contract import (
    INTERPRETED_BRIEF_TIER,
    SourceContractError,
    apply_source_contract,
    publication_title_from_contract,
    promote_juejin_full_article,
    verify_source_contract,
)
from ai_stack.tag_taxonomy import normalize_tags
from crawler.main import CrawlerOrchestrator
from processor.main import ProcessorOrchestrator
from processor.markdown_normalizer import remove_markdown_sections_by_heading
from publisher.main import PublisherOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")
CONTENT_TIMEZONE = SHANGHAI_TZ
# Modes whose title, URL and provenance come from the hash-bound source
# contract rather than from free-form crawler fields.
_CONTRACT_MODES = frozenset({"source_brief", "interpreted_brief", "evidence_backed_rewrite"})
# Modes that publish captured evidence as a card and must not carry internal links.
_BRIEF_MODES = frozenset({"source_brief", "interpreted_brief"})
_SOURCE_METADATA_URL_RE = re.compile(r"(?i)\b(?:https?://|www\.)\S+")
_MARKDOWN_PUNCTUATION_RE = re.compile(r"([\\`*_[\]{}()#+.!|>~-])")


def fetch_selected_juejin_article(source_url: str, *, timeout: int = 10):
    """Lazy import keeps lightweight content-guard tooling dependency-isolated."""

    from crawler.juejin_article import fetch_juejin_article

    return fetch_juejin_article(source_url, timeout=timeout)


def content_now(value: datetime | None = None) -> datetime:
    """Return one timezone-aware clock value for filenames and frontmatter."""
    if value is None:
        return datetime.now(CONTENT_TIMEZONE)
    if value.tzinfo is None:
        raise ValueError("content generation time must be timezone-aware")
    return value.astimezone(CONTENT_TIMEZONE)


def safe_source_metadata_text(value: object, *, maximum_length: int = 160) -> str:
    """Render hash-bound but untrusted source metadata as one inert text line."""

    normalized = " ".join(str(value or "").split())
    normalized = _SOURCE_METADATA_URL_RE.sub("", normalized)
    normalized = " ".join(normalized.split()).strip()[:maximum_length].rstrip()
    escaped = _MARKDOWN_PUNCTUATION_RE.sub(r"\\\1", normalized)
    return html.escape(escaped, quote=False)


def canonicalize_content_url(value: object) -> str:
    """Use the shared URL identity policy and fail closed for invalid sources."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    try:
        return canonicalize_url(raw)
    except ValueError:
        return ""

_RELREF_RE = re.compile(r"""\{\{[<%]\s*relref\s+(['"])(.+?)\1\s*[>%]\}\}""")
_TAXONOMY_MD_LINK_RE = re.compile(r"""\[([^\]]+)\]\(/(tags|categories|scenarios)/([^)]+?)\)""")
_PUBLIC_HTTP_URL_RE = re.compile(r"https?://[^\s<>\"']+")
_URL_TRAILING_PUNCTUATION = ".,;:!?)]}"
_SENSITIVE_PUBLIC_QUERY_KEYS = frozenset(
    {"sk", "token", "code", "key", "sig", "signature", "session"}
)

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

        if in_code_fence:
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


_GENERATION_TERMINAL_FIELDS = (
    "created",
    "policy_rejected",
    "skipped_existing",
    "skipped_quality",
    "contract_failed",
    "generation_failed",
)


def validate_generation_accounting(stats: dict) -> None:
    """Require every processed candidate to have one terminal outcome."""

    try:
        processed = int(stats.get("processed", 0) or 0)
        outcomes = {
            field: int(stats.get(field, 0) or 0)
            for field in _GENERATION_TERMINAL_FIELDS
        }
    except (AttributeError, TypeError, ValueError) as exc:
        raise RuntimeError("generation accounting is invalid") from exc
    if processed < 0 or any(value < 0 for value in outcomes.values()):
        raise RuntimeError("generation accounting is invalid")
    terminal_total = sum(outcomes.values())
    if terminal_total != processed:
        raise RuntimeError(
            "generation accounting mismatch: "
            f"processed={processed} terminal_outcomes={terminal_total}"
        )


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


def _is_sensitive_public_query_key(value: str) -> bool:
    folded = str(value or "").strip().casefold()
    return folded in _SENSITIVE_PUBLIC_QUERY_KEYS or folded.startswith("x-amz-")


def sanitize_sensitive_source_urls_in_markdown_text(*, text: str) -> tuple[str, int]:
    """Remove credential-like query parameters while preserving public URL identity."""

    if not text:
        return text, 0

    removed = 0

    def _replace(match: re.Match[str]) -> str:
        nonlocal removed
        raw = match.group(0)
        url = raw.rstrip(_URL_TRAILING_PUNCTUATION)
        trailing = raw[len(url) :]
        try:
            parsed = urllib.parse.urlsplit(url)
            pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        except ValueError:
            return raw
        filtered = [
            (key, value)
            for key, value in pairs
            if not _is_sensitive_public_query_key(key)
        ]
        removed_now = len(pairs) - len(filtered)
        if removed_now <= 0:
            return raw
        removed += removed_now
        sanitized = urllib.parse.urlunsplit(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                urllib.parse.urlencode(filtered, doseq=True),
                parsed.fragment,
            )
        )
        return sanitized + trailing

    return _PUBLIC_HTTP_URL_RE.sub(_replace, text), removed


def sanitize_sensitive_source_urls_in_posts(*, posts_dir: Path) -> tuple[int, int]:
    changed_files = 0
    removed_parameters_total = 0

    try:
        paths = sorted(posts_dir.glob("*.md"))
    except Exception:
        return 0, 0

    for path in paths:
        try:
            original = path.read_text(encoding="utf-8")
        except Exception:
            continue
        sanitized, removed = sanitize_sensitive_source_urls_in_markdown_text(text=original)
        if removed <= 0:
            continue
        try:
            path.write_text(sanitized, encoding="utf-8")
        except Exception:
            continue
        changed_files += 1
        removed_parameters_total += removed

    return changed_files, removed_parameters_total


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
        self.lineage_registry_dir = project_root / "data" / "lineage"
        self.max_new_items_per_source = 1 if self.runtime_profile == "ci" else None

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
            logger.info("Mode: source-contract first; Tier-C briefs for partial evidence")
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
            self._validate_crawled_data(crawled_data)
            crawled_data = self._apply_lineage_policy(
                crawled_data,
                observations=getattr(self.crawler, "last_observations", None),
            )
            crawled_data = self._filter_unseen_crawled_data(
                crawled_data,
                max_items_per_source=None,
            )
            unseen_items = sum(len(items) for items in crawled_data.values())
            logger.info(
                "✓ Selected %s archive-new items for AI processing",
                unseen_items,
            )

            # 2. 超级增强处理（15次大模型调用）
            logger.info("\n[2/4] Applying evidence-aware content policy...")
            if unseen_items > 0:
                processed_data = self._process_candidates_with_quota(
                    crawled_data,
                    max_items_per_source=self.max_new_items_per_source,
                )
            else:
                processed_data = {source: [] for source in crawled_data}
                self.last_quota_stats = {
                    "available_candidates": 0,
                    "processed_candidates": 0,
                    "policy_rejected": 0,
                    "eligible_candidates": 0,
                    "quota_deferred": 0,
                }
                logger.info("No archive-new items; skipping LLM processing")
            logger.info(f"✓ Super enhanced content from {len(processed_data)} sources")
            postability = summarize_processed_postability(processed_data)

            # 3. 生成超级增强版 Markdown 文章
            logger.info("\n[3/4] Generating Markdown posts...")
            posts_created = self._generate_posts(
                processed_data,
                generated_at=content_now(),
            )
            generation_stats = getattr(self, "last_generation_stats", {})
            logger.info(
                "✓ Markdown write summary: processed=%s created=%s "
                "policy_rejected=%s skipped_existing=%s skipped_quality=%s "
                "contract_failed=%s generation_failed=%s",
                int(generation_stats.get("processed", 0) or 0),
                posts_created,
                int(generation_stats.get("policy_rejected", 0) or 0),
                int(generation_stats.get("skipped_existing", 0) or 0),
                int(generation_stats.get("skipped_quality", 0) or 0),
                int(generation_stats.get("contract_failed", 0) or 0),
                int(generation_stats.get("generation_failed", 0) or 0),
            )
            self._raise_for_fatal_post_generation_state(
                posts_created=posts_created,
                postability=postability,
                quality_failed_items=int(generation_stats.get("skipped_quality", 0) or 0),
                contract_failed_items=int(generation_stats.get("contract_failed", 0) or 0),
                generation_failed_items=int(generation_stats.get("generation_failed", 0) or 0),
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

            final_quality = build_content_quality_manifest(project_root / "blog/content")
            if final_quality["quarantined_count"]:
                raise RuntimeError(
                    "Post tree failed the final completeness gate after sanitization: "
                    f"quarantined={final_quality['quarantined_count']}"
                )

            # 4. 推送内容
            logger.info("\n[4/4] Publishing to social platforms...")
            self._publish_content(processed_data)

            logger.info("\n" + "=" * 80)
            logger.info("Content generation completed successfully")
            logger.info("Every published Post passed source and completeness gates")
            logger.info("=" * 80)

            return True

        except Exception as e:
            logger.error(f"Content generation failed: {e}", exc_info=True)
            return False

    def _validate_crawled_data(self, crawled_data: dict) -> None:
        if not isinstance(crawled_data, dict):
            raise RuntimeError("Crawler returned an invalid result")
        total_items = sum(
            len(items) for items in crawled_data.values() if isinstance(items, list)
        )
        if total_items <= 0:
            raise RuntimeError(
                "Crawler returned no items from all enabled sources; refusing a green no-op deployment"
            )

    def _filter_unseen_crawled_data(
        self,
        crawled_data: dict,
        *,
        max_items_per_source: int | None = None,
    ) -> dict:
        existing_urls = {
            canonicalize_content_url(post.get("external_url"))
            for post in getattr(self, "_post_index", [])
            if isinstance(post, dict) and post.get("external_url")
        }
        seen_urls = set(existing_urls)
        selected: dict[str, list[dict]] = {}
        candidate_count = 0
        skipped_historical = 0
        invalid_candidates = 0
        quota_deferred = 0

        for source, raw_items in (crawled_data or {}).items():
            chosen: list[dict] = []
            items = raw_items if isinstance(raw_items, list) else []
            candidate_count += len(items)
            for index, item in enumerate(items):
                if not isinstance(item, dict):
                    invalid_candidates += 1
                    continue
                external_url = canonicalize_content_url(
                    item.get("url") or item.get("repo_url") or item.get("link")
                )
                if external_url and external_url in seen_urls:
                    skipped_historical += 1
                    continue
                if external_url:
                    seen_urls.add(external_url)
                    item["url"] = external_url
                chosen.append(item)
                if (
                    max_items_per_source is not None
                    and max_items_per_source > 0
                    and len(chosen) >= max_items_per_source
                ):
                    quota_deferred += len(items) - index - 1
                    break
            selected[str(source)] = chosen

        self.last_filter_stats = {
            "candidates": candidate_count,
            "historical_urls": len(existing_urls),
            "skipped_historical": skipped_historical,
            "invalid_candidates": invalid_candidates,
            "selected": sum(len(items) for items in selected.values()),
            "quota_deferred": quota_deferred,
        }
        accounted_candidates = (
            self.last_filter_stats["skipped_historical"]
            + self.last_filter_stats["invalid_candidates"]
            + self.last_filter_stats["selected"]
            + self.last_filter_stats["quota_deferred"]
        )
        if candidate_count != accounted_candidates:
            raise RuntimeError(
                "archive filter accounting mismatch: "
                f"candidates={candidate_count} accounted={accounted_candidates}"
            )
        logger.info(
            "Archive dedupe: candidates=%s historical_urls=%s skipped=%s "
            "invalid=%s selected=%s quota_deferred=%s",
            self.last_filter_stats["candidates"],
            self.last_filter_stats["historical_urls"],
            self.last_filter_stats["skipped_historical"],
            self.last_filter_stats["invalid_candidates"],
            self.last_filter_stats["selected"],
            self.last_filter_stats["quota_deferred"],
        )
        return selected

    def _process_candidates_with_quota(
        self,
        candidates: dict,
        *,
        max_items_per_source: int | None,
    ) -> dict:
        """Scan past policy rejects until each source fills its eligible quota."""

        if max_items_per_source is not None and max_items_per_source <= 0:
            raise ValueError("per-source candidate quota must be positive")

        normalized = {
            str(source): [item for item in items if isinstance(item, dict)]
            for source, items in (candidates or {}).items()
            if isinstance(items, list)
        }
        available_candidates = sum(len(items) for items in normalized.values())

        if max_items_per_source is None:
            hydrated = self._hydrate_selected_juejin_articles(normalized)
            processed = self.processor.process_by_source(hydrated)
            processed_candidates = 0
            policy_rejected = 0
            eligible_candidates = 0
            for source, source_candidates in hydrated.items():
                bulk_results = (
                    processed.get(source) if isinstance(processed, dict) else None
                )
                if (
                    not isinstance(bulk_results, list)
                    or len(bulk_results) != len(source_candidates)
                    or any(not isinstance(item, dict) for item in bulk_results)
                ):
                    raise RuntimeError(
                        f"processor result count mismatch for source {source}"
                    )
                processed_candidates += len(bulk_results)
                for item in bulk_results:
                    if self._policy_rejection_reason(item) is not None:
                        policy_rejected += 1
                    else:
                        eligible_candidates += 1
            quota_deferred = 0
        else:
            processed = {}
            processed_candidates = 0
            policy_rejected = 0
            eligible_candidates = 0
            quota_deferred = 0
            for source, source_candidates in normalized.items():
                source_processed_results: list[dict] = []
                source_eligible = 0
                for index, candidate in enumerate(source_candidates):
                    if source_eligible >= max_items_per_source:
                        quota_deferred += len(source_candidates) - index
                        break

                    preflight = self.processor.preflight_candidate(candidate)
                    if not isinstance(preflight, dict):
                        raise RuntimeError(
                            f"processor preflight result mismatch for source {source}"
                        )
                    if self._policy_rejection_reason(preflight) is not None:
                        source_processed_results.append(preflight)
                        processed_candidates += 1
                        policy_rejected += 1
                        continue

                    processed_candidates += 1
                    source_eligible += 1
                    eligible_candidates += 1
                    candidate_batch = {source: [preflight]}
                    if source == "juejin":
                        candidate_batch = self._hydrate_selected_juejin_articles(
                            candidate_batch
                        )
                    batch_result = self.processor.process_by_source(candidate_batch)
                    batch_items = (
                        batch_result.get(source)
                        if isinstance(batch_result, dict)
                        else None
                    )
                    if (
                        not isinstance(batch_items, list)
                        or len(batch_items) != 1
                        or not isinstance(batch_items[0], dict)
                    ):
                        raise RuntimeError(
                            f"processor result count mismatch for source {source}"
                        )
                    item = batch_items[0]
                    source_processed_results.append(item)
                processed[source] = source_processed_results

        self.last_quota_stats = {
            "available_candidates": available_candidates,
            "processed_candidates": processed_candidates,
            "policy_rejected": policy_rejected,
            "eligible_candidates": eligible_candidates,
            "quota_deferred": quota_deferred,
        }
        if available_candidates != processed_candidates + quota_deferred:
            raise RuntimeError(
                "candidate quota accounting mismatch: "
                f"available={available_candidates} "
                f"processed={processed_candidates} deferred={quota_deferred}"
            )
        if processed_candidates != policy_rejected + eligible_candidates:
            raise RuntimeError(
                "candidate policy accounting mismatch: "
                f"processed={processed_candidates} "
                f"policy_rejected={policy_rejected} "
                f"eligible={eligible_candidates}"
            )
        logger.info(
            "Candidate quota: available=%s processed=%s policy_rejected=%s "
            "eligible=%s deferred=%s",
            available_candidates,
            processed_candidates,
            policy_rejected,
            eligible_candidates,
            quota_deferred,
        )
        return processed

    def _apply_lineage_policy(
        self,
        crawled_data: dict,
        *,
        observations: list[dict] | None = None,
    ) -> dict:
        """Resolve provenance before archive filtering or any model call.

        URL dedupe and lineage serve different purposes: generation receives one
        winner per URL, while this method records every contracted cross-source
        observation and suppresses only high-confidence cross-URL copies.
        """

        raw_observations = observations
        if raw_observations is None:
            raw_observations = [
                item
                for items in (crawled_data or {}).values()
                if isinstance(items, list)
                for item in items
                if isinstance(item, dict)
            ]
        if not raw_observations:
            return {
                str(source): list(items) if isinstance(items, list) else []
                for source, items in (crawled_data or {}).items()
            }

        # One observation is one canonical URL. Multiple source captures of the
        # same URL are revisions; choose the strongest immutable capture for the
        # current resolution while the crawler still retains all raw contracts.
        strongest_by_observation: dict[str, tuple[dict, object]] = {}
        propagation_targets = [
            *raw_observations,
            *(
                item
                for items in (crawled_data or {}).values()
                if isinstance(items, list)
                for item in items
            ),
        ]
        for item in propagation_targets:
            if not isinstance(item, dict):
                continue
            verify_source_contract(item)
            captured_at = str(item.get("captured_at") or "").strip()
            last_seen_at = (
                f"{captured_at[:10]}T00:00:00Z"
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", captured_at[:10])
                else None
            )
            observation = observation_from_contract(item, last_seen_at=last_seen_at)
            strength = (
                str(item.get("source_capture_mode") or "") != "metadata_only",
                item.get("source_is_truncated") is not True,
                int(item.get("source_text_chars") or 0),
                str(item.get("source_snapshot_sha256") or ""),
            )
            previous = strongest_by_observation.get(observation.observation_id)
            if previous is None or strength > previous[0]["_lineage_strength"]:
                candidate = dict(item)
                candidate["_lineage_strength"] = strength
                strongest_by_observation[observation.observation_id] = (
                    candidate,
                    observation,
                )

        if not strongest_by_observation:
            return {
                str(source): list(items) if isinstance(items, list) else []
                for source, items in (crawled_data or {}).items()
            }

        ordered_pairs = sorted(
            strongest_by_observation.values(),
            key=lambda pair: (
                str(pair[1].source_published_at or pair[1].first_seen_at or ""),
                pair[1].observation_id,
            ),
        )
        lineage_inputs = [pair[1] for pair in ordered_pairs]
        registry_root = Path(getattr(self, "lineage_registry_dir", project_root / "data" / "lineage"))
        registry = LineageRegistry.load(registry_root)

        historical_baseline = []
        # Reconstruct exact shingles from the bounded, source-only historical
        # excerpts on every run.  The persisted registry intentionally keeps
        # only Bitmap / SimHash / KMV candidate signatures, so approximate
        # suppression is never decided from a lossy sketch alone.
        content_root = self.posts_dir.parent
        current_ids = {item.observation_id for item in lineage_inputs}
        for path in sorted(self.posts_dir.glob("*.md")):
            try:
                historical = parse_historical_post(path, content_root=content_root)
            except (OSError, UnicodeError, LineageValidationError) as exc:
                raise RuntimeError(
                    f"Historical lineage baseline is invalid: {path.name}: {exc}"
                ) from exc
            if historical is not None and historical.observation_id not in current_ids:
                historical_baseline.append(historical)

        batch = registry.resolve_batch(
            lineage_inputs,
            historical_baseline=historical_baseline,
        )
        resolutions = {item.observation_id: item for item in batch.items}
        lineage_input_by_id = {
            item.observation_id: item for item in lineage_inputs
        }
        contracted_by_id = {
            identifier: pair[0]
            for identifier, pair in strongest_by_observation.items()
        }
        for identifier, resolution in resolutions.items():
            contracted = contracted_by_id[identifier]
            lineage_input = lineage_input_by_id[identifier]
            contracted.update(
                {
                    "observation_id": resolution.observation_id,
                    "revision_id": resolution.revision_id,
                    "event_id": resolution.event_id,
                    "lineage_relation": resolution.relation.value,
                    "parent_observation_id": resolution.parent_observation_id,
                    "lineage_confidence": resolution.confidence,
                    "lineage_suppressed": resolution.suppress,
                    "first_seen_at": lineage_input.first_seen_at,
                    "last_seen_at": lineage_input.last_seen_at,
                }
            )

        # Propagate resolution fields to all object instances that represent the
        # same URL, including the generation winner returned by crawler dedupe.
        for item in propagation_targets:
            if not isinstance(item, dict):
                continue
            identifier = observation_from_contract(item).observation_id
            metadata = contracted_by_id.get(identifier)
            if metadata is not None:
                for field in (
                    "observation_id",
                    "revision_id",
                    "event_id",
                    "lineage_relation",
                    "parent_observation_id",
                    "lineage_confidence",
                    "lineage_suppressed",
                    "first_seen_at",
                    "last_seen_at",
                ):
                    item[field] = metadata.get(field)

        generated_at = max(
            (
                str(item.get("captured_at") or "")
                for item in raw_observations
                if isinstance(item, dict)
            ),
            default="",
        ) or content_now().astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")
        registry.save(registry_root, generated_at=generated_at)

        selected: dict[str, list[dict]] = {}
        for source, items in (crawled_data or {}).items():
            selected[str(source)] = [
                item
                for item in (items if isinstance(items, list) else [])
                if isinstance(item, dict) and item.get("lineage_suppressed") is not True
            ]
        self.last_lineage_stats = {
            **batch.stats,
            "circuit_breaker_tripped": batch.circuit_breaker.tripped,
            "circuit_breaker_reason": batch.circuit_breaker.reason,
        }
        logger.info(
            "Lineage resolution: observations=%s suppressed=%s derivatives=%s breaker=%s",
            batch.stats.get("observations", 0),
            batch.stats.get("suppressed", 0),
            batch.stats.get("derivatives", 0),
            batch.circuit_breaker.reason or "off",
        )
        return selected

    def _hydrate_selected_juejin_articles(self, crawled_data: dict) -> dict:
        """Promote only selected Juejin candidates when complete SSR is provable.

        Hydration intentionally happens after archive dedupe and the CI
        per-source eligible quota, so an hourly run performs at most one article
        request.  WAF and structural failures keep the already hash-bound Tier-C
        RSS brief.
        """

        selected = {
            str(source): list(items) if isinstance(items, list) else []
            for source, items in (crawled_data or {}).items()
        }
        items = selected.get("juejin", [])
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            if str(item.get("content_mode") or "") != "source_brief":
                continue
            if str(item.get("source_capture_mode") or "") != "excerpt":
                continue
            evidence = item.get("evidence") if isinstance(item.get("evidence"), dict) else {}
            source_url = str(evidence.get("external_url") or item.get("url") or "").strip()
            try:
                capture = fetch_selected_juejin_article(source_url, timeout=10)
                items[index] = promote_juejin_full_article(item, capture.markdown)
                logger.info(
                    "Juejin full article verified: id=%s chars=%s headings=%s code_blocks=%s",
                    capture.article_id,
                    len(capture.plain_text),
                    capture.heading_count,
                    capture.code_block_count,
                )
            except (SourceContractError, OSError, ValueError) as exc:
                logger.warning(
                    "Juejin full article unavailable; keeping Tier-C RSS excerpt: %s (%s)",
                    source_url,
                    exc,
                )
        selected["juejin"] = items
        return selected

    def _raise_for_fatal_post_generation_state(
        self,
        *,
        posts_created: int,
        postability: dict,
        quality_failed_items: int = 0,
        contract_failed_items: int = 0,
        generation_failed_items: int = 0,
    ) -> None:
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
            if quality_failed_items > 0:
                logger.warning(
                    "Some generated Markdown failed the provenance gate: items=%s",
                    quality_failed_items,
                )
            if contract_failed_items > 0 or generation_failed_items > 0:
                logger.warning(
                    "Some candidates failed contract/render/write gates: contract=%s generation=%s",
                    contract_failed_items,
                    generation_failed_items,
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
        if quality_failed_items > 0:
            raise RuntimeError(
                "Generated Markdown failed the provenance gate and no posts were created. "
                f"Rejected items: {quality_failed_items}"
            )
        if contract_failed_items > 0:
            raise RuntimeError(
                "Crawler source contract failed and no posts were created. "
                f"Rejected items: {contract_failed_items}"
            )
        if generation_failed_items > 0:
            raise RuntimeError(
                "Post rendering or persistence failed and no posts were created. "
                f"Rejected items: {generation_failed_items}"
            )

    def _generate_posts(
        self,
        processed_data: dict,
        *,
        generated_at: datetime | None = None,
    ) -> int:
        """
        生成超级增强版 Markdown 文章文件

        Args:
            processed_data: 处理后的数据

        Returns:
            int: 创建的文章数量
        """
        processed_count = 0
        created_count = 0
        policy_rejected = 0
        skipped_existing = 0
        skipped_quality = 0
        contract_failed = 0
        generation_failed = 0
        local_generated_at = content_now(generated_at)
        timestamp = local_generated_at.strftime('%Y%m%d')

        for source, items in processed_data.items():
            for idx, item in enumerate(items):
                processed_count += 1
                try:
                    verify_source_contract(item)
                    processing_failure = self._processing_failure_reason(item)
                    if processing_failure is not None:
                        generation_failed += 1
                        logger.error(
                            "Candidate processing failed before Markdown generation: "
                            "source=%s category=%s title=%s",
                            source,
                            str(
                                item.get("processing_error_category")
                                or "processing_error"
                            ),
                            item.get("title", "Untitled"),
                        )
                        continue
                    policy_reason = self._policy_rejection_reason(item)
                    if policy_reason is not None:
                        policy_rejected += 1
                        logger.info(
                            "↷ Policy rejected candidate: source=%s reason=%s title=%s",
                            source,
                            policy_reason,
                            item.get("title", "Untitled"),
                        )
                        continue
                    if self._should_skip_post(item):
                        skipped_quality += 1
                        logger.warning(
                            "Skipped candidate without a publishable guarded body: "
                            "source=%s title=%s",
                            source,
                            item.get("title", "Untitled"),
                        )
                        continue

                    # 生成文件名
                    slug = self._generate_slug(item.get('title', ''), idx)
                    external_url = canonicalize_content_url(
                        item["evidence"].get("external_url")
                    )
                    identity = hashlib.sha256(
                        external_url.encode("utf-8")
                    ).hexdigest()[:10]
                    filename = f"{timestamp}-{source}-{slug}-{identity}.md"
                    filepath = self.posts_dir / filename

                    if filepath.exists():
                        existing = self._post_entry_from_file(filepath)
                        if (
                            existing is None
                            or existing.get("external_url") != external_url
                        ):
                            generation_failed += 1
                            logger.error(
                                "Refusing immutable Post filename collision: %s",
                                filename,
                            )
                            continue
                        skipped_existing += 1
                        logger.info("↷ Skipped existing immutable post: %s", filename)
                        continue

                    # 生成 Markdown 内容
                    markdown_content = self._format_super_enhanced_markdown(
                        item,
                        current_filename=filename,
                        generated_at=local_generated_at,
                    )
                    markdown_content, _ = sanitize_public_markdown_text(text=markdown_content)

                    quality_reasons = analyze_post(markdown_content).fatal_reasons
                    if quality_reasons:
                        skipped_quality += 1
                        logger.warning(
                            "Skipped unverifiable generated post %s: %s",
                            filename,
                            ", ".join(quality_reasons),
                        )
                        continue

                    publication_payload = self._publication_payload(item)

                    # 写入文件
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)

                    logger.info(f"✓ Created post: {filename}")
                    created_count += 1
                    item["_publication_gate"] = "passed"
                    item["_publication_payload"] = publication_payload
                    self._post_index.append(self._post_entry_from_data(filename, item))

                except SourceContractError as e:
                    contract_failed += 1
                    logger.error(
                        "Failed source contract for %s: %s",
                        item.get("title", "Unknown"),
                        e,
                    )
                    continue
                except Exception as e:
                    generation_failed += 1
                    logger.error(f"Failed to generate post for {item.get('title', 'Unknown')}: {e}")
                    continue

        self.last_generation_stats = {
            "processed": processed_count,
            "created": created_count,
            "policy_rejected": policy_rejected,
            "skipped_existing": skipped_existing,
            "skipped_quality": skipped_quality,
            "contract_failed": contract_failed,
            "generation_failed": generation_failed,
        }
        validate_generation_accounting(self.last_generation_stats)
        return created_count

    def _publication_payload(self, item: dict) -> dict:
        """Build a mode-aware payload only after the Post validation gate."""

        verify_source_contract(item)
        evidence = item["evidence"]
        if str(item.get("content_mode") or "") == "evidence_backed_rewrite":
            return {
                "title": publication_title_from_contract(item),
                "summary": self._truncate_seo_description(
                    self._strip_markdown_for_seo(item.get("rewritten_body", "")),
                    maximum_length=160,
                ),
                "url": str(evidence.get("external_url") or "").strip(),
                "source": str(evidence.get("source") or "").strip(),
                "tags": self._normalize_tags(item.get("tags", [])),
                "content_mode": "evidence_backed_rewrite",
                "publication_tier": "B",
                "source_snapshot_sha256": str(evidence.get("digest") or "").strip(),
            }
        if str(item.get("content_mode") or "") == "interpreted_brief":
            return {
                "title": publication_title_from_contract(item),
                "summary": self._truncate_seo_description(
                    self._strip_markdown_for_seo(
                        self._interpretation_summary(item.get("interpretation_text", ""))
                    ),
                    maximum_length=160,
                ),
                "url": str(evidence.get("external_url") or "").strip(),
                "source": str(evidence.get("source") or "").strip(),
                "tags": self._normalize_tags(item.get("tags", [])),
                "content_mode": "interpreted_brief",
                "publication_tier": INTERPRETED_BRIEF_TIER,
                "source_snapshot_sha256": str(evidence.get("digest") or "").strip(),
            }
        return {
            "title": publication_title_from_contract(item),
            "summary": (
                "来源证据快报，仅呈现抓取时保存的来源字段；"
                "请以原始来源为准。"
            ),
            "url": str(evidence.get("external_url") or "").strip(),
            "source": str(evidence.get("source") or "").strip(),
            "tags": self._normalize_tags(item.get("tags", [])),
            "content_mode": "source_brief",
            "publication_tier": "C",
            "source_snapshot_sha256": str(evidence.get("digest") or "").strip(),
        }

    def _source_brief_publication_payload(self, item: dict) -> dict:
        """Backward-compatible wrapper for callers that publish Tier-C cards."""

        payload = self._publication_payload(item)
        if payload.get("content_mode") != "source_brief":
            raise SourceContractError("expected a source brief publication payload")
        return payload

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

    @staticmethod
    def _processing_failure_reason(item: dict) -> str | None:
        if not isinstance(item, dict):
            return None
        if "processing_error" not in item:
            return None
        reason = str(item.get("processing_error") or "").strip()
        return reason or "unknown_processing_error"

    @staticmethod
    def _policy_rejection_reason(item: dict) -> str | None:
        if not isinstance(item, dict):
            return "invalid_candidate"
        if SuperEnhancedContentGenerator._processing_failure_reason(item) is not None:
            return None
        if item.get("ai_related") is False:
            return "not_ai_related"
        if item.get("should_publish") is False:
            return "moderation_rejected"
        if item.get("skip_post", False):
            return "skip_post"
        return None

    def _should_skip_post(self, item: dict) -> bool:
        if self._processing_failure_reason(item) is not None:
            return True
        if self._policy_rejection_reason(item) is not None:
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

    def _format_super_enhanced_markdown(
        self,
        item: dict,
        *,
        current_filename: str | None = None,
        generated_at: datetime | None = None,
    ) -> str:
        """
        格式化内容为超级增强版 Markdown（15+ 个章节）

        Args:
            item: 内容项

        Returns:
            str: Markdown 内容
        """
        content_mode = str(item.get("content_mode") or "").strip()
        evidence: dict[str, Any] = (
            item.get("evidence") if isinstance(item.get("evidence"), dict) else {}
        )
        evidence_fields: dict[str, Any] = (
            evidence.get("fields")
            if isinstance(evidence.get("fields"), dict)
            else {}
        )
        if content_mode in _CONTRACT_MODES:
            source = str(evidence.get("source") or "unknown")
            title = publication_title_from_contract(item)
        else:
            source = item.get('source', 'unknown')
            raw_title = item.get('catchy_title') or item.get('title_translated') or item.get('title', 'Untitled')
            title = self._sanitize_title_for_seo(raw_title, max_length=55)
        date = content_now(generated_at).isoformat(timespec="seconds")

        # 构建标签
        tags = self._normalize_tags(item.get('tags', []))
        tags_str = ', '.join([f'"{self._yaml_escape(tag)}"' for tag in tags])

        # 构建分类
        categories = self._normalize_taxonomy_list(item.get('categories', []))
        categories_str = ', '.join([f'"{self._yaml_escape(cat)}"' for cat in categories])

        scenarios = self._normalize_scenarios(item.get("scenarios"))
        scenarios_str = ', '.join([f'"{self._yaml_escape(s)}"' for s in scenarios])

        # 获取 URL
        url = (
            evidence.get("external_url", "")
            if content_mode in _CONTRACT_MODES
            else item.get('url', '')
        )
        if not url and source == 'github_trending':
            url = item.get('repo_url', '')
        url = canonicalize_content_url(url)
        if not url:
            raise ValueError("generated posts require a valid canonical source URL")

        # 开始构建 Markdown
        lines = [
            '---',
            f'title: "{self._yaml_escape(title)}"',
            f'date: {date}',
            'draft: false',
            'entry_kind: "auto"',
            f'tags: [{tags_str}]',
            f'categories: [{categories_str}]',
            f'source: "{self._yaml_escape(source)}"',
        ]

        if content_mode:
            lines.append(f'content_mode: "{self._yaml_escape(content_mode)}"')
        publication_tier = str(item.get("publication_tier") or "").strip()
        if publication_tier:
            lines.append(f'publication_tier: "{self._yaml_escape(publication_tier)}"')
        source_capture_mode = str(item.get("source_capture_mode") or "").strip()
        if source_capture_mode:
            lines.append(f'source_capture_mode: "{self._yaml_escape(source_capture_mode)}"')
        snapshot_digest = str(item.get("source_snapshot_sha256") or "").strip()
        if snapshot_digest:
            lines.append(f'source_snapshot_sha256: "{self._yaml_escape(snapshot_digest)}"')
        payload_digest = str(item.get("source_payload_sha256") or "").strip()
        if payload_digest:
            lines.append(f'source_payload_sha256: "{self._yaml_escape(payload_digest)}"')
        for field_name in ("observation_id", "event_id", "revision_id"):
            value = str(item.get(field_name) or "").strip()
            if value:
                lines.append(f'{field_name}: "{self._yaml_escape(value)}"')
        for field_name in ("source_published_at", "first_seen_at"):
            value = str(item.get(field_name) or "").strip()
            if value:
                lines.append(f'{field_name}: "{self._yaml_escape(value)}"')
        timestamp_confidence = str(item.get("timestamp_confidence") or "").strip()
        if timestamp_confidence:
            lines.append(
                f'timestamp_confidence: "{self._yaml_escape(timestamp_confidence)}"'
            )
        lineage_relation = str(item.get("lineage_relation") or "").strip()
        if lineage_relation:
            allowed_lineage_relations = {
                "original",
                "exact_copy",
                "syndicated",
                "same_event",
                "derivative",
                "related_only",
            }
            if lineage_relation not in allowed_lineage_relations:
                raise ValueError("generated post has an invalid lineage relation")
            lines.append(
                f'lineage_relation: "{self._yaml_escape(lineage_relation)}"'
            )
        parent_observation_id = str(item.get("parent_observation_id") or "").strip()
        if parent_observation_id:
            lines.append(
                "parent_observation_id: "
                f'"{self._yaml_escape(parent_observation_id)}"'
            )
        extractor_version = str(item.get("extractor_version") or "").strip()
        if extractor_version:
            lines.append(f'extractor_version: "{self._yaml_escape(extractor_version)}"')
        discovery_method = str(item.get("discovery_method") or "").strip()
        if discovery_method:
            lines.append(f'discovery_method: "{self._yaml_escape(discovery_method)}"')
        source_completeness = str(item.get("source_completeness") or "").strip()
        if source_completeness:
            lines.append(
                f'source_completeness: "{self._yaml_escape(source_completeness)}"'
            )
        parent_snapshot = str(item.get("parent_snapshot_sha256") or "").strip()
        if parent_snapshot:
            lines.append(
                f'parent_snapshot_sha256: "{self._yaml_escape(parent_snapshot)}"'
            )
        lines.append(
            f'source_is_truncated: {"true" if item.get("source_is_truncated") is True else "false"}'
        )
        truncation_reason = str(item.get("source_truncation_reason") or "").strip()
        if truncation_reason:
            lines.append(f'source_truncation_reason: "{self._yaml_escape(truncation_reason)}"')
        if content_mode in _CONTRACT_MODES:
            lines.append('source_support: 1.0')
            source_title = str(evidence_fields.get("title") or "").strip()
            if source_title:
                lines.append(f"source_title_chars_original: {len(source_title)}")
        if content_mode == "interpreted_brief":
            interpretation_digest = str(item.get("interpretation_sha256") or "").strip()
            if interpretation_digest:
                lines.append(f'interpretation_sha256: "{interpretation_digest}"')

        if content_mode == "source_brief":
            seo_description = self._source_brief_note(
                str(evidence.get("capture_mode") or "metadata_only"),
                source,
            )
        elif content_mode == "interpreted_brief":
            # Lead with what the thing is rather than a disclaimer; fall back to
            # the capture note if the section cannot be recovered.
            seo_description = self._truncate_seo_description(
                self._strip_markdown_for_seo(
                    self._interpretation_summary(item.get("interpretation_text", ""))
                ),
                maximum_length=160,
            ) or self._source_brief_note(
                str(evidence.get("capture_mode") or "metadata_only"),
                source,
            )
        elif content_mode == "evidence_backed_rewrite":
            seo_description = self._truncate_seo_description(
                self._strip_markdown_for_seo(item.get("rewritten_body", "")),
                maximum_length=160,
            )
        else:
            seo_description = self._seo_description(item)
        if seo_description:
            lines.append(f'description: "{self._yaml_escape(seo_description)}"')

        lines.append(f'external_url: {url}')
        if scenarios:
            lines.append(f'scenarios: [{scenarios_str}]')

        lines.append('---')
        lines.append('')

        # 根据来源生成不同格式
        if content_mode in _BRIEF_MODES:
            lines.extend(self._format_source_brief(item))
        elif content_mode == "evidence_backed_rewrite":
            lines.extend(self._format_evidence_backed_rewrite(item))
        elif source == 'github_trending':
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

        if content_mode not in _BRIEF_MODES:
            related = self._find_related_posts(item, current_filename=current_filename)
            self._inject_internal_links(lines, item, related)
        return '\n'.join(lines)

    def _format_evidence_backed_rewrite(self, item: dict) -> list[str]:
        """Render a Tier-B rewrite without exposing the captured source body."""

        evidence: dict[str, Any] = (
            item.get("evidence") if isinstance(item.get("evidence"), dict) else {}
        )
        fields: dict[str, Any] = (
            evidence.get("fields")
            if isinstance(evidence.get("fields"), dict)
            else {}
        )
        url = canonicalize_content_url(evidence.get("external_url"))
        author = safe_source_metadata_text(fields.get("author"), maximum_length=120)
        author = author or "来源作者"
        published = safe_source_metadata_text(fields.get("published"), maximum_length=96)
        body = str(item.get("rewritten_body") or "").strip()
        if not body:
            raise ValueError("evidence-backed rewrite body is missing")
        lines = [
            "## 转写说明",
            "",
            "> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。",
            "> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。",
            "",
            f"- **原作者**: {author}",
            f"- **原始来源**: [{url}]({url})",
        ]
        if published:
            lines.append(f"- **原文发布时间**: {published}")
        lines.extend(["", body, "", "## 来源与核验", ""])
        lines.extend(
            [
                f"- [原始文章]({url})",
                "- 页面事实以原始来源及其引用的官方资料为准；版本、星标和模型能力会随时间变化。",
                "- AI Stack 不公开抓取到的全文快照，只发布独立转写与来源入口。",
            ]
        )
        return lines

    def _format_source_brief(self, item: dict) -> list[str]:
        """Render captured evidence, plus a labelled reading when one exists.

        A Tier-C card shows evidence only.  A Tier-C+ card adds the validated
        interpretation between the metadata and the captured excerpt, so the
        reading always sits next to the evidence it was drawn from.
        """

        interpretation = (
            str(item.get("interpretation_text") or "").strip()
            if str(item.get("content_mode") or "") == "interpreted_brief"
            else ""
        )
        evidence: dict[str, Any] = (
            item.get("evidence") if isinstance(item.get("evidence"), dict) else {}
        )
        fields: dict[str, Any] = (
            evidence.get("fields")
            if isinstance(evidence.get("fields"), dict)
            else {}
        )
        source = str(evidence.get("source") or "unknown").strip()
        url = canonicalize_content_url(evidence.get("external_url"))
        capture_mode = str(evidence.get("capture_mode") or "metadata_only")
        note = self._source_brief_note(capture_mode, source)

        def safe(value: object) -> str:
            text = html.escape(str(value or "").strip(), quote=False)
            return text.replace("{{", "&#123;&#123;").replace("}}", "&#125;&#125;")

        lines = [
            "## 基本信息",
            "",
            f"- **来源**: {safe(source)}",
            f"- **原始来源**: [{safe(url)}]({url})",
        ]
        # The publishing host is the one piece of placement a reader can act on
        # when no body text was captured: a vendor announcement and a personal
        # blog post carry very different weight under the same headline.
        host = urllib.parse.urlsplit(url).hostname or ""
        if host:
            lines.append(f"- **发布域名**: {safe(host)}")
        if source == "github_trending":
            for label, key in (
                ("主要语言", "language"),
                ("Star", "stars"),
                ("今日新增 Star", "today_stars"),
                ("许可协议", "license"),
            ):
                value = safe(fields.get(key))
                if value:
                    lines.append(f"- **{label}**: {value}")
            topics = fields.get("topics")
            if isinstance(topics, list):
                labels = [safe(topic) for topic in topics if safe(topic)]
                if labels:
                    lines.append(f"- **主题标签**: {'、'.join(labels[:8])}")
        elif source == "arxiv":
            category = safe(fields.get("category"))
            if category:
                lines.append(f"- **分类**: {category}")
            authors = fields.get("authors")
            if isinstance(authors, list):
                names = [safe(name) for name in authors if safe(name)]
                if names:
                    shown = "、".join(names[:3])
                    suffix = " 等" if len(names) > 3 else ""
                    lines.append(f"- **作者**: {shown}{suffix}")
        if source == "hacker_news":
            lines.extend(
                [
                    f"- **作者**: {safe(fields.get('author'))}",
                    f"- **评分**: {safe(fields.get('score', 0))}",
                    f"- **评论数**: {safe(fields.get('descendants', 0))}",
                ]
            )
            if fields.get("hn_id"):
                hn_url = f"https://news.ycombinator.com/item?id={fields.get('hn_id')}"
                lines.append(f"- **HN 讨论**: [{hn_url}]({hn_url})")

        if interpretation:
            # Already validated at generation time: no links, no markup, no
            # numbers or names absent from the evidence above.
            lines.extend(["", f"## {INTERPRETATION_HEADING}", ""])
            lines.extend(interpretation.splitlines())

        source_text = str(item.get("source_display_excerpt") or "").strip()
        if capture_mode != "metadata_only" and source_text:
            lines.extend(["", "## 来源摘要/节选", ""])
            lines.extend(f"> {safe(line)}" if line.strip() else ">" for line in source_text.splitlines())

        lines.extend(["", "## 来源说明", "", safe(note), ""])
        if interpretation:
            # The Tier-C promise ("no inference beyond the captured evidence")
            # would be false on this page, so state what was added instead.
            lines.append(
                "> 「要点解读」由 AI Stack 依据上方已保存内容整理，"
                "不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。"
            )
        else:
            lines.append("> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。")
        return lines

    @staticmethod
    def _interpretation_summary(interpretation: object) -> str:
        """Return the prose under the reading's first section, for SEO use."""

        text = str(interpretation or "")
        match = re.search(
            r"(?ms)^###[ \t]+这是什么[ \t]*$\n(?P<body>.*?)(?=^###[ \t]+|\Z)",
            text,
        )
        if match is None:
            return ""
        return " ".join(line.strip() for line in match.group("body").splitlines() if line.strip())

    @staticmethod
    def _source_brief_note(capture_mode: str, source: str) -> str:
        labels = {
            "metadata_only": "当前只保存了标题与来源元数据，未抓取外链全文。",
            "abstract": "当前保存的是来源摘要，不代表论文全文。",
            "excerpt": "当前保存的是 RSS 或来源节选，不代表原文全文。",
            "repository_excerpt": "当前保存的是仓库元数据或来源节选。",
            "social_post": "当前保存的是单条社交内容，不代表完整讨论串。",
        }
        note = labels.get(str(capture_mode), labels["metadata_only"])
        if str(source) == "hacker_news":
            return f"{note}请以原始来源和 Hacker News 讨论为准。"
        return f"{note}请以原始来源为准。"

    def _sanitize_title_for_seo(
        self,
        title: str,
        *,
        max_length: int | None = 55,
    ) -> str:
        t = str(title or "").strip()
        if not t:
            return "Untitled"
        t = re.sub(r"[\U0001F300-\U0001FAFF]", "", t)
        t = re.sub(r"[\u2600-\u27BF]", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        if max_length is not None and max_length > 0 and len(t) > max_length:
            shortened = t[:max_length].rstrip()
            next_character = t[len(shortened) : len(shortened) + 1]
            if (
                shortened
                and next_character
                and not shortened[-1].isspace()
                and not next_character.isspace()
            ):
                boundary = shortened.rfind(" ")
                if boundary >= int(max_length * 0.8):
                    shortened = shortened[:boundary].rstrip()
            t = shortened
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

    @staticmethod
    def _truncate_seo_description(
        text: str,
        *,
        minimum_sentence_length: int = 80,
        maximum_length: int = 160,
    ) -> str:
        value = str(text or "").strip()
        if len(value) <= maximum_length:
            return value

        window = value[:maximum_length]
        sentence_ends = [
            match.end()
            for match in re.finditer(r"(?:[。！？!?]|\.(?=\s|$))", window)
            if match.end() >= minimum_sentence_length
        ]
        if sentence_ends:
            return window[: sentence_ends[-1]].strip()

        content_limit = maximum_length - 1
        prefix = value[:content_limit].rstrip()
        next_character = value[len(prefix) : len(prefix) + 1]

        def ascii_word_character(character: str) -> bool:
            return bool(character) and character.isascii() and (
                character.isalnum() or character in "_-"
            )

        if (
            prefix
            and next_character
            and ascii_word_character(prefix[-1])
            and ascii_word_character(next_character)
        ):
            boundaries = list(re.finditer(r"[^A-Za-z0-9_-]+", prefix))
            if not boundaries:
                return "…"
            prefix = prefix[: boundaries[-1].start()].rstrip()

        prefix = prefix.rstrip(" \t\r\n,，:：;；、-—–([{（【《“‘/\\")
        return f"{prefix}…" if prefix else "…"

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
            return self._truncate_seo_description(s)
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

    def _normalize_tags(self, value) -> list[str]:
        return normalize_tags(value, limit=8)

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
            "external_url": canonicalize_content_url(
                item.get("url") or item.get("repo_url") or item.get("link")
            ),
            "tags": self._normalize_tags(item.get("tags", [])),
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
        if fm.get("archived") is True:
            return None

        filename = path.name
        title = str(fm.get("title") or "").strip()
        return {
            "filename": filename,
            "content_path": f"posts/{filename}",
            "title": title,
            "external_url": canonicalize_content_url(
                fm.get("external_url") or fm.get("url")
            ),
            "tags": self._normalize_tags(fm.get("tags", [])),
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
        tags = set(self._normalize_tags(item.get("tags", [])))
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
        tags = self._normalize_tags(item.get("tags", []))
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

        url = canonicalize_content_url(
            item.get("url") or item.get("repo_url") or item.get("external_url")
        )

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
            eligible_payloads = [
                item.get("_publication_payload")
                for item in items
                if item.get("_publication_gate") == "passed"
                and isinstance(item.get("_publication_payload"), dict)
            ]
            for payload in eligible_payloads[:2]:  # 每个来源最多推送2篇
                try:
                    logger.info(f"Publishing {source} item to {enabled_platforms}...")
                    results = self.publisher.publish_all(dict(payload))

                    for platform, success in results.items():
                        if success:
                            logger.info(f"Successfully published to {platform}")
                        else:
                            logger.warning(f"Failed to publish to {platform}")

                except Exception as e:
                    logger.error(f"Failed to publish item: {e}")
                    continue


_UNIFIED_CLI_COMMANDS = {
    "crawl",
    "process",
    "render",
    "publish",
    "validate",
    "status",
    "resume",
    "migrate",
}


def main(argv=None):
    """兼容入口。

    新的分阶段命令直接委托 ``ai-stack`` CLI；原有参数仍走历史兼容路径，
    便于本地维护脚本在迁移窗口内继续使用。
    """
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] in _UNIFIED_CLI_COMMANDS:
        from ai_stack.cli import main as unified_cli_main

        return unified_cli_main(arguments)

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

    args = parser.parse_args(arguments)

    if args.sanitize_relrefs_only:
        content_root = project_root / "blog" / "content"
        posts_dir = content_root / "posts"
        changed_files, removed_lines = sanitize_relrefs_in_posts(posts_dir=posts_dir, content_root=content_root)
        if changed_files > 0:
            logger.info(f"✓ Sanitized relref links: files={changed_files} lines_removed={removed_lines}")
        else:
            logger.info("✓ Relref links OK")
        changed_files, removed_parameters = sanitize_sensitive_source_urls_in_posts(
            posts_dir=posts_dir
        )
        if changed_files > 0:
            logger.info(
                "✓ Sanitized source URLs: "
                f"files={changed_files} query_parameters_removed={removed_parameters}"
            )
        else:
            logger.info("✓ Source URLs OK")
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
