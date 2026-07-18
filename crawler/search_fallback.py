"""
Search fallback utilities
使用多语言查询 + SearXNG 搜索兜底被封禁或失效的数据源。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import logging
import os
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence
from urllib.parse import urlparse

import requests

from .dedupe import canonicalize_url


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_SEARXNG_BASE_URLS = [
    "https://searx.tiekoetter.com/search",
    "https://search.inetol.net/search",
    "https://searx.be/search",
]

DEFAULT_QUERY_LANGUAGES = ["zh-CN", "en-US"]
DEFAULT_QUERY_TOPICS = [
    "AI",
    "人工智能",
    "LLM",
    "大模型",
    "machine learning",
    "机器学习",
    "agents",
    "智能体",
]

DEFAULT_TOPIC_EXPANSIONS = {
    "ai": ["人工智能", "artificial intelligence"],
    "人工智能": ["AI", "artificial intelligence"],
    "machine learning": ["机器学习", "ML"],
    "机器学习": ["machine learning", "ML"],
    "deep learning": ["深度学习"],
    "深度学习": ["deep learning"],
    "llm": ["大模型", "large language model"],
    "大模型": ["LLM", "large language model"],
    "large language model": ["LLM", "大模型"],
    "agents": ["智能体", "agentic AI"],
    "智能体": ["agents", "agentic AI"],
    "open source": ["开源"],
    "开源": ["open source"],
}


def _dedupe_preserve_order(items: Iterable[str]) -> List[str]:
    seen: set[str] = set()
    output: List[str] = []
    for item in items:
        value = str(item or "").strip()
        if not value:
            continue
        lowered = value.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        output.append(value)
    return output


def _has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def _normalize_searxng_base_url(url: str) -> str:
    base = str(url or "").strip()
    if not base:
        return ""
    if not base.startswith("http://") and not base.startswith("https://"):
        base = f"https://{base}"
    if base.endswith("/"):
        base = base[:-1]
    parsed = urlparse(base)
    if parsed.path in {"", "/"}:
        return f"{base}/search"
    if parsed.path.endswith("/search"):
        return base
    return base


def _extract_domain(url: str) -> str:
    parsed = urlparse(str(url or "").strip())
    return (parsed.netloc or "").lower()


@dataclass(frozen=True)
class PlannedQuery:
    query: str
    language: str = "all"
    target: str = ""


class MultilingualQueryPlanner:
    """规则化查询规划器，为被封源生成中英文检索词。"""

    def __init__(
        self,
        query_languages: Optional[Sequence[str]] = None,
        topic_expansions: Optional[Dict[str, Sequence[str]]] = None,
        default_topics: Optional[Sequence[str]] = None,
        max_queries_per_target: int = 4,
    ):
        self.query_languages = list(query_languages or DEFAULT_QUERY_LANGUAGES)
        self.topic_expansions = {
            str(k).strip().lower(): _dedupe_preserve_order(v)
            for k, v in (topic_expansions or DEFAULT_TOPIC_EXPANSIONS).items()
            if str(k).strip()
        }
        self.default_topics = _dedupe_preserve_order(default_topics or DEFAULT_QUERY_TOPICS)
        self.max_queries_per_target = max(1, int(max_queries_per_target))

    def _expand_topics(self, topics: Optional[Sequence[str]]) -> List[str]:
        seeds = _dedupe_preserve_order(list(topics or []) + self.default_topics)
        expanded: List[str] = list(seeds)
        for term in seeds:
            expanded.extend(self.topic_expansions.get(term.lower(), []))
        return _dedupe_preserve_order(expanded)

    def _topics_for_language(self, topics: Sequence[str], language: str) -> List[str]:
        if language.lower().startswith("zh"):
            preferred = [topic for topic in topics if _has_cjk(topic)]
        else:
            preferred = [topic for topic in topics if not _has_cjk(topic)]
        return preferred or list(topics)

    def plan_site_queries(
        self,
        site: str,
        topics: Optional[Sequence[str]] = None,
        target: str = "",
        max_queries: Optional[int] = None,
    ) -> List[PlannedQuery]:
        site_filter = site if str(site).startswith("site:") else f"site:{site}"
        expanded_topics = self._expand_topics(topics)
        limit = max(1, int(max_queries or self.max_queries_per_target))
        plans: List[PlannedQuery] = []

        for language in self.query_languages:
            terms = self._topics_for_language(expanded_topics, language)[:limit]
            for term in terms:
                parts = [site_filter]
                if target:
                    parts.append(f"\"{target}\"")
                parts.append(term)
                plans.append(
                    PlannedQuery(
                        query=" ".join(p for p in parts if p),
                        language=language,
                        target=target,
                    )
                )
        return plans


class SearXNGSearchClient:
    """轻量 SearXNG 客户端。"""

    def __init__(
        self,
        base_urls: Optional[Sequence[str]] = None,
        timeout: int = 12,
        per_query_limit: int = 5,
        session: Optional[requests.Session] = None,
    ):
        self.timeout = max(3, int(timeout))
        self.per_query_limit = max(1, int(per_query_limit))
        self.session = session or requests.Session()
        self.base_urls = self._resolve_base_urls(base_urls)

    def _resolve_base_urls(self, base_urls: Optional[Sequence[str]]) -> List[str]:
        env_url = os.getenv("SEARXNG_BASE_URL", "").strip()
        candidates = []
        if env_url:
            candidates.append(env_url)
        candidates.extend(base_urls or [])
        candidates.extend(DEFAULT_SEARXNG_BASE_URLS)
        return _dedupe_preserve_order(_normalize_searxng_base_url(url) for url in candidates)

    def search(self, plan: PlannedQuery, limit: Optional[int] = None, time_range: str = "month") -> List[Dict[str, Any]]:
        params = {
            "q": plan.query,
            "format": "json",
            "language": plan.language,
            "categories": "general",
            "safesearch": 0,
            "pageno": 1,
            "time_range": time_range,
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (AI-Stack SearchFallback; +https://github.com/g5n-dev/ai-stack)",
            "Accept": "application/json,text/plain;q=0.9,*/*;q=0.8",
        }
        max_results = max(1, min(10, int(limit or self.per_query_limit)))

        for provider_index, base_url in enumerate(self.base_urls, start=1):
            try:
                response = self.session.get(base_url, params=params, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                payload = response.json() or {}
                results = payload.get("results") or []
                normalized = [
                    self._normalize_result(item, plan=plan, provider=base_url)
                    for item in results[:max_results]
                ]
                normalized = [item for item in normalized if item]
                if normalized:
                    return normalized
            except Exception as exc:
                logger.warning(
                    "SearXNG query failed (provider_index=%d error_type=%s)",
                    provider_index,
                    type(exc).__name__,
                )

        return []

    def search_many(
        self,
        plans: Sequence[PlannedQuery],
        max_total: int,
        per_query_limit: Optional[int] = None,
        time_range: str = "month",
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        seen_urls: set[str] = set()
        per_query = max(1, int(per_query_limit or self.per_query_limit))

        for plan in plans:
            for item in self.search(plan, limit=per_query, time_range=time_range):
                url = canonicalize_url(item.get("url", ""))
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                item["url"] = url
                results.append(item)
                if len(results) >= max_total:
                    return results
        return results

    def _normalize_result(self, item: Dict[str, Any], plan: PlannedQuery, provider: str) -> Optional[Dict[str, Any]]:
        title = str(item.get("title") or "").strip()
        url = canonicalize_url(str(item.get("url") or item.get("link") or "").strip())
        if not title or not url:
            return None

        description = str(item.get("content") or item.get("snippet") or "").strip()
        published_at = str(item.get("publishedDate") or item.get("published_at") or "").strip()

        return {
            "title": title,
            "url": url,
            "description": description,
            "published_at": published_at,
            "search_query": plan.query,
            "search_language": plan.language,
            "search_provider": provider,
        }


class SearchFallbackService:
    """对各被封源统一提供搜索兜底。"""

    def __init__(self, config: Optional[Dict[str, Any]] = None, session: Optional[requests.Session] = None):
        self.config = config or {}
        self.enabled = bool(self.config.get("enabled", False))
        self.planner = MultilingualQueryPlanner(
            query_languages=self.config.get("query_languages"),
            default_topics=self.config.get("default_topics"),
            max_queries_per_target=self.config.get("max_queries_per_target", 4),
        )
        self.client = SearXNGSearchClient(
            base_urls=self.config.get("instances"),
            timeout=self.config.get("timeout", 12),
            per_query_limit=self.config.get("per_query_limit", 5),
            session=session,
        )
        self.time_range = str(self.config.get("time_range", "month") or "month")

    def search_reddit_subreddit(
        self,
        subreddit: str,
        limit: int,
        topics: Optional[Sequence[str]] = None,
        fallback_reason: str = "blocked",
    ) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []

        subreddit = str(subreddit or "").strip()
        if not subreddit:
            return []

        site = f"reddit.com/r/{subreddit}"
        plans = self.planner.plan_site_queries(site=site, topics=topics, target=f"r/{subreddit}")
        raw_results = self.client.search_many(plans, max_total=max(1, int(limit)), time_range=self.time_range)

        items: List[Dict[str, Any]] = []
        subreddit_marker = f"/r/{subreddit.lower()}/"
        for result in raw_results:
            if subreddit_marker not in result.get("url", "").lower():
                continue
            items.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("description", ""),
                    "author": "",
                    "score": 0,
                    "num_comments": 0,
                    "subreddit": subreddit,
                    "source": "reddit",
                    "published_at": result.get("published_at", ""),
                    "crawled_at": datetime.now(timezone.utc).isoformat(),
                    "discovery_method": "search_fallback",
                    "search_query": result.get("search_query", ""),
                    "search_language": result.get("search_language", ""),
                    "search_provider": result.get("search_provider", ""),
                    "fallback_reason": fallback_reason,
                }
            )
        return items

    def search_juejin_articles(
        self,
        tags: Optional[Sequence[str]],
        limit: int,
        fallback_reason: str = "empty_feed",
    ) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []

        plans = self.planner.plan_site_queries(site="juejin.cn/post", topics=tags, target="掘金")
        raw_results = self.client.search_many(plans, max_total=max(1, int(limit)), time_range=self.time_range)

        items: List[Dict[str, Any]] = []
        for result in raw_results:
            if "juejin.cn/post" not in result.get("url", ""):
                continue
            items.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("description", ""),
                    "author": "",
                    "published": result.get("published_at", ""),
                    "published_at": result.get("published_at", ""),
                    "tags": list(tags or []),
                    "source": "juejin",
                    "crawled_at": datetime.now(timezone.utc).isoformat(),
                    "discovery_method": "search_fallback",
                    "search_query": result.get("search_query", ""),
                    "search_language": result.get("search_language", ""),
                    "search_provider": result.get("search_provider", ""),
                    "fallback_reason": fallback_reason,
                }
            )
        return items

    def search_feed_domain(
        self,
        feed_name: str,
        feed_url: str,
        limit: int,
        topics: Optional[Sequence[str]] = None,
        fallback_reason: str = "feed_fetch_failed",
    ) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []

        domain = _extract_domain(feed_url)
        if not domain:
            return []

        plans = self.planner.plan_site_queries(site=domain, topics=topics, target=feed_name)
        raw_results = self.client.search_many(plans, max_total=max(1, int(limit)), time_range=self.time_range)

        items: List[Dict[str, Any]] = []
        for result in raw_results:
            if domain not in _extract_domain(result.get("url", "")):
                continue
            items.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("description", ""),
                    "author": "",
                    "published": result.get("published_at", ""),
                    "published_at": result.get("published_at", ""),
                    "feed_name": feed_name,
                    "feed_url": feed_url,
                    "feed_type": "blog",
                    "audio_url": "",
                    "tags": [],
                    "source": "blogs_podcasts",
                    "crawled_at": datetime.now(timezone.utc).isoformat(),
                    "discovery_method": "search_fallback",
                    "search_query": result.get("search_query", ""),
                    "search_language": result.get("search_language", ""),
                    "search_provider": result.get("search_provider", ""),
                    "fallback_reason": fallback_reason,
                }
            )
        return items
