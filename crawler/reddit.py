"""
Reddit crawler
爬取 Reddit 子版块热门帖子（不需要 API）
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional

import requests

from .search_fallback import SearchFallbackService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedditCrawler:
    def __init__(
        self,
        subreddits: Optional[List[str]] = None,
        limit_per_subreddit: int = 10,
        sort: str = "hot",
        include_selftext: bool = True,
        timeout: int = 15,
        search_fallback: Optional[Dict] = None,
    ):
        self.subreddits = subreddits or ["MachineLearning", "LocalLLaMA", "OpenAI", "ArtificialInteligence"]
        self.limit_per_subreddit = int(limit_per_subreddit)
        self.sort = sort if sort in {"hot", "new", "top"} else "hot"
        self.include_selftext = bool(include_selftext)
        self.timeout = int(timeout)
        self.base_url = "https://www.reddit.com"
        self.search_topics = ["AI", "人工智能", "LLM", "大模型", "agents", "智能体", "open source", "开源"]
        self.search_fallback_service = SearchFallbackService(search_fallback)

    def _fetch_listing(self, subreddit: str) -> List[Dict]:
        url = f"{self.base_url}/r/{subreddit}/{self.sort}.json"
        params = {"limit": max(1, min(100, self.limit_per_subreddit))}
        headers = {
            "User-Agent": "Mozilla/5.0 (AI-Stack; +https://github.com/)",
            "Accept": "application/json,text/plain;q=0.9,*/*;q=0.8",
        }

        resp = requests.get(url, params=params, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json() or {}
        children = (((data.get("data") or {}).get("children")) or [])

        items: List[Dict] = []
        for child in children:
            post = (child or {}).get("data") or {}
            if not post:
                continue
            if post.get("stickied"):
                continue

            title = (post.get("title") or "").strip()
            permalink = post.get("permalink") or ""
            post_url = f"{self.base_url}{permalink}" if permalink else (post.get("url") or "")
            created_utc = post.get("created_utc")
            published_at = ""
            if created_utc:
                try:
                    published_at = datetime.fromtimestamp(float(created_utc), tz=timezone.utc).isoformat()
                except Exception:
                    published_at = ""

            description = ""
            if self.include_selftext:
                description = (post.get("selftext") or "").strip()

            items.append(
                {
                    "title": title,
                    "url": post_url,
                    "description": description,
                    "author": post.get("author") or "",
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "subreddit": subreddit,
                    "source": "reddit",
                    "published_at": published_at,
                    "crawled_at": datetime.now(timezone.utc).isoformat(),
                }
            )
        return items

    def fetch(self) -> List[Dict]:
        all_items: List[Dict] = []
        for subreddit in self.subreddits:
            try:
                items = self._fetch_listing(subreddit)
                if items:
                    all_items.extend(items)
                    logger.info(f"Reddit r/{subreddit} fetched: {len(items)} items")
                    continue

                logger.warning(f"Reddit r/{subreddit} returned 0 items, trying search fallback")
                fallback_items = self.search_fallback_service.search_reddit_subreddit(
                    subreddit=subreddit,
                    limit=self.limit_per_subreddit,
                    topics=self.search_topics,
                    fallback_reason="empty_listing",
                )
                if fallback_items:
                    all_items.extend(fallback_items)
                    logger.info(
                        f"Reddit r/{subreddit} search fallback recovered: {len(fallback_items)} items"
                    )
            except Exception as e:
                logger.error(f"Reddit r/{subreddit} failed: {e}")
                fallback_items = self.search_fallback_service.search_reddit_subreddit(
                    subreddit=subreddit,
                    limit=self.limit_per_subreddit,
                    topics=self.search_topics,
                    fallback_reason="api_blocked",
                )
                if fallback_items:
                    all_items.extend(fallback_items)
                    logger.info(
                        f"Reddit r/{subreddit} search fallback recovered: {len(fallback_items)} items"
                    )
        return all_items
