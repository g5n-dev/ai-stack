"""
Blogs & Podcasts crawler (RSS/Atom)
抓取「大佬博客 / 播客」等 RSS/Atom 源内容（聚合+排序+去重）
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup

from .dedupe import canonicalize_url


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_FEEDS: List[Dict[str, str]] = [
    {"name": "Andrej Karpathy Blog", "url": "https://karpathy.github.io/feed.xml", "type": "blog"},
    {"name": "Lilian Weng (Lil'Log)", "url": "https://lilianweng.github.io/lil-log/feed.xml", "type": "blog"},
    {"name": "Jay Alammar", "url": "https://jalammar.github.io/feed.xml", "type": "blog"},
    {"name": "Colah's Blog", "url": "https://colah.github.io/rss.xml", "type": "blog"},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "type": "blog"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "type": "blog"},
    {"name": "Latent Space", "url": "https://www.latent.space/feed", "type": "blog"},
    {"name": "The Gradient", "url": "https://thegradient.pub/feed/", "type": "blog"},
    {"name": "Import AI (Jack Clark)", "url": "https://importai.substack.com/feed", "type": "blog"},
    {"name": "Lex Fridman Podcast", "url": "https://lexfridman.com/feed/podcast/", "type": "podcast"},
]


def _to_iso(dt: Optional[datetime]) -> str:
    if not dt:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def _parse_entry_datetime(entry: Any) -> Optional[datetime]:
    # feedparser gives time.struct_time in *_parsed fields.
    ts = entry.get("published_parsed") or entry.get("updated_parsed") or entry.get("created_parsed")
    if not ts:
        return None
    try:
        return datetime(*ts[:6], tzinfo=timezone.utc)
    except Exception:
        return None


def _extract_audio_url(entry: Any) -> str:
    # Podcasts commonly use enclosures or link rel="enclosure".
    enclosures = entry.get("enclosures") or []
    for enc in enclosures:
        href = enc.get("href") or enc.get("url")
        if href:
            return href
    for link in entry.get("links") or []:
        if link.get("rel") == "enclosure":
            href = link.get("href")
            if href:
                return href
    return ""


def _html_to_text(s: str) -> str:
    if not s:
        return ""
    try:
        soup = BeautifulSoup(s, "html.parser")
        return soup.get_text(" ", strip=True)
    except Exception:
        return s


@dataclass(frozen=True)
class FeedConfig:
    name: str
    url: str
    type: str = "blog"  # blog | podcast | other


class BlogsPodcastsCrawler:
    """聚合多个 RSS/Atom 源，按时间排序后返回最新条目。"""

    def __init__(self, feeds: Optional[List[Dict[str, str]]] = None, limit: int = 10, timeout: int = 30):
        self.feeds = [FeedConfig(**f) for f in (feeds or DEFAULT_FEEDS)]
        self.limit = limit
        self.timeout = timeout

    def fetch(self) -> List[Dict]:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (AI-Stack; +https://github.com/)"}
            all_items: List[Dict[str, Any]] = []

            for feed_cfg in self.feeds:
                items = self._fetch_single_feed(feed_cfg, headers=headers)
                all_items.extend(items)

            # sort by published_dt desc
            all_items.sort(key=lambda x: x.get("_published_dt") or datetime.min.replace(tzinfo=timezone.utc), reverse=True)

            # dedupe by normalized url
            seen: set[str] = set()
            unique: List[Dict[str, Any]] = []
            for item in all_items:
                key = canonicalize_url(item.get("url", "")).lower().strip()
                if not key:
                    continue
                if key in seen:
                    continue
                seen.add(key)
                item["url"] = canonicalize_url(item.get("url", ""))
                item.pop("_published_dt", None)
                unique.append(item)
                if len(unique) >= self.limit:
                    break

            return unique
        except Exception as e:
            logger.error(f"Failed to fetch blogs/podcasts feeds: {e}")
            return []

    def _fetch_single_feed(self, feed_cfg: FeedConfig, headers: Dict[str, str]) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(feed_cfg.url, headers=headers, timeout=self.timeout)
            resp.raise_for_status()

            parsed = feedparser.parse(resp.content)
            if getattr(parsed, "bozo", False):
                # bozo_exception may include useful details; log at debug to avoid noisy runs.
                logger.debug(f"Feed parsing warning for {feed_cfg.url}: {getattr(parsed, 'bozo_exception', None)}")

            items: List[Dict[str, Any]] = []
            for entry in getattr(parsed, "entries", [])[: max(self.limit * 3, 50)]:
                item = self._extract_entry(entry, feed_cfg)
                if item:
                    items.append(item)
            return items
        except Exception as e:
            logger.warning(f"Failed to fetch feed {feed_cfg.name} ({feed_cfg.url}): {e}")
            return []

    def _extract_entry(self, entry: Any, feed_cfg: FeedConfig) -> Optional[Dict[str, Any]]:
        try:
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            if not title or not link:
                return None

            summary = entry.get("summary") or entry.get("description") or ""
            description = _html_to_text(summary)[:2000]

            published_dt = _parse_entry_datetime(entry)
            published = entry.get("published") or entry.get("updated") or ""

            tags = []
            for t in entry.get("tags") or []:
                term = (t.get("term") or "").strip()
                if term:
                    tags.append(term)

            audio_url = _extract_audio_url(entry) if feed_cfg.type == "podcast" else ""

            return {
                "title": title,
                "url": canonicalize_url(link),
                "description": description,
                "author": (entry.get("author") or "").strip(),
                "published": published,
                "published_at": _to_iso(published_dt),
                "feed_name": feed_cfg.name,
                "feed_url": feed_cfg.url,
                "feed_type": feed_cfg.type,
                "audio_url": audio_url,
                "tags": tags,
                "source": "blogs_podcasts",
                "crawled_at": datetime.now(timezone.utc).isoformat(),
                "_published_dt": published_dt,
            }
        except Exception as e:
            logger.debug(f"Failed to extract feed entry ({feed_cfg.name}): {e}")
            return None
