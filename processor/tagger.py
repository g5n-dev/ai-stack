"""
Content tagger
内容打标/归类模块 - 使用大模型为文章生成 tags + categories
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import json
import logging
import re

from .anthropic_client import AnthropicClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TaggingResult:
    categories: List[str]
    tags: List[str]


class ContentTagger:
    """内容打标器（tags + categories）"""

    DEFAULT_CATEGORIES = [
        "大模型",
        "AI 工程",
        "论文",
        "开发工具",
        "系统与基础设施",
        "安全",
        "数据",
        "前端",
        "后端",
        "产品与创业",
        "效率与方法论",
        "开源生态",
        "生活与杂谈",
    ]

    def __init__(self, client: AnthropicClient, config: Optional[Dict[str, Any]] = None):
        self.client = client
        self.config = config or {}
        self.enabled = bool(self.config.get("enabled", True))
        self.max_tags = int(self.config.get("max_tags", 8))
        self.max_categories = int(self.config.get("max_categories", 2))
        self.temperature = float(self.config.get("temperature", 0.2))

    def tag(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """为内容生成 tags + categories，并写回 content。"""
        if not self.enabled:
            return content

        # If already tagged, skip unless forced.
        existing_tags = content.get("tags")
        existing_categories = content.get("categories")
        if isinstance(existing_tags, list) and len(existing_tags) > 0 and isinstance(existing_categories, list) and len(existing_categories) > 0:
            return content

        try:
            prompt = self._build_prompt(content)
            raw = self.client.create_message(prompt, max_tokens=500, temperature=self.temperature)
            result = self._parse_result(raw)
            if not result:
                fallback = self._fallback(content)
                content["tags"] = fallback.tags
                content["categories"] = fallback.categories
                return content

            categories, tags = self._normalize(content, result.categories, result.tags)
            content["tags"] = tags
            content["categories"] = categories
            return content
        except Exception as e:
            logger.error(f"Failed to tag content: {e}")
            fallback = self._fallback(content)
            content["tags"] = fallback.tags
            content["categories"] = fallback.categories
            return content

    def _build_prompt(self, content: Dict[str, Any]) -> str:
        source = (content.get("source") or "").strip()
        title = (content.get("catchy_title") or content.get("title") or "").strip()
        original_title = (content.get("title") or "").strip()
        description = (content.get("description_translated") or content.get("description") or "").strip()
        summary = (content.get("summary_translated") or content.get("summary") or "").strip()
        language = (content.get("language") or "").strip()
        arxiv_category = (content.get("category") or "").strip()

        deepwiki_excerpt = (content.get("deepwiki_content") or "").strip()
        if deepwiki_excerpt:
            deepwiki_excerpt = deepwiki_excerpt[:900]

        # Keep prompt compact & structured.
        categories_list = "\n".join([f"- {c}" for c in self.DEFAULT_CATEGORIES])

        context_lines = [
            f"source: {source}",
            f"title: {title}",
            f"original_title: {original_title}",
        ]
        if description:
            context_lines.append(f"description: {description[:600]}")
        if summary:
            context_lines.append(f"summary: {summary[:900]}")
        if language:
            context_lines.append(f"language: {language}")
        if arxiv_category:
            context_lines.append(f"arxiv_category: {arxiv_category}")
        if deepwiki_excerpt:
            context_lines.append(f"deepwiki_excerpt: {deepwiki_excerpt}")

        context = "\n".join(context_lines)

        return f"""你是一个信息架构师。请基于给定内容，为文章生成「分类 categories」与「标签 tags」。

要求：
1) categories 只能从下列列表中选择 1-2 个（必须严格命中，不要自造分类）：
{categories_list}
2) tags 生成 {self.max_tags} 个左右（允许 5~{max(5, self.max_tags + 2)} 个），用中文为主，必要时可包含英文缩写（如 LLM/RAG/Rust）。
3) tags 要短（建议 2~8 个字），统一风格、去重、不要带 #、不要带句号。
4) 输出必须是严格 JSON，且仅输出 JSON（不要 Markdown，不要解释）：
{{"categories":["..."],"tags":["..."]}}

内容：
{context}
"""

    def _parse_result(self, raw: str) -> Optional[TaggingResult]:
        if not raw or not raw.strip():
            return None

        text = raw.strip()

        # First try: direct JSON.
        parsed = self._try_json(text)
        if parsed is None:
            # Try to extract the first JSON object.
            m = re.search(r"\{[\s\S]*\}", text)
            if m:
                parsed = self._try_json(m.group(0))

        if not isinstance(parsed, dict):
            return None

        categories = parsed.get("categories")
        tags = parsed.get("tags")
        if not isinstance(categories, list) or not isinstance(tags, list):
            return None

        categories = [str(x) for x in categories]
        tags = [str(x) for x in tags]
        return TaggingResult(categories=categories, tags=tags)

    def _try_json(self, text: str) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(text)
        except Exception:
            return None

    def _normalize(
        self,
        content: Optional[Dict[str, Any]],
        categories: List[str],
        tags: List[str],
    ) -> Tuple[List[str], List[str]]:
        # Strip, de-dupe, clamp length, enforce category whitelist.
        categories_clean: List[str] = []
        allowed = set(self.DEFAULT_CATEGORIES)
        for c in categories:
            c2 = self._clean_token(c)
            if not c2:
                continue
            if c2 not in allowed:
                continue
            if c2 not in categories_clean:
                categories_clean.append(c2)
            if len(categories_clean) >= max(1, self.max_categories):
                break

        tags_clean: List[str] = []
        for t in tags:
            t2 = self._clean_token(t)
            if not t2:
                continue
            if t2 not in tags_clean:
                tags_clean.append(t2)
            if len(tags_clean) >= max(1, self.max_tags):
                break

        # Ensure at least one category.
        if not categories_clean:
            categories_clean = [self._fallback(content).categories[0]]

        # Ensure at least one tag (helps UI and search).
        if not tags_clean:
            tags_clean = self._fallback(content).tags[: self.max_tags]

        return categories_clean, tags_clean

    def _clean_token(self, s: str) -> str:
        s = str(s or "").strip()
        s = s.replace("#", "")
        s = re.sub(r"[\u3002。]+$", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def _fallback(self, content: Optional[Dict[str, Any]]) -> TaggingResult:
        # Lightweight heuristic fallback to avoid empty taxonomies.
        source = (content or {}).get("source", "")
        language = (content or {}).get("language", "")
        arxiv_category = (content or {}).get("category", "")

        if source == "arxiv" or arxiv_category:
            categories = ["论文"]
        elif source == "github_trending":
            categories = ["开源生态"]
        elif source in {"hacker_news", "blogs_podcasts", "juejin"}:
            categories = ["效率与方法论"]
        else:
            categories = ["AI 工程"]

        tags: List[str] = []
        if source:
            tags.append(source)
        if language:
            tags.append(language)
        if arxiv_category:
            tags.append(arxiv_category)

        return TaggingResult(categories=categories, tags=tags[: self.max_tags])
