"""
Blogs & Podcasts crawler (RSS/Atom)
抓取「大佬博客 / 播客」等 RSS/Atom 源内容（聚合+排序+去重）
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import feedparser
import requests
from bs4 import BeautifulSoup

from .dedupe import canonicalize_url
from .search_fallback import SearchFallbackService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


_MAX_CAPTURED_FEED_BYTES = 24 * 1024
_HTML_BLOCK_TAGS = (
    "address",
    "article",
    "aside",
    "blockquote",
    "dd",
    "div",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "td",
    "th",
    "tr",
    "ul",
)


DEFAULT_FEEDS: list[dict[str, str]] = [
    {"name": "Andrej Karpathy Blog", "url": "https://karpathy.github.io/feed.xml", "type": "blog"},
    {
        "name": "Lilian Weng (Lil'Log)",
        "url": "https://lilianweng.github.io/lil-log/feed.xml",
        "type": "blog",
    },
    {"name": "Jay Alammar", "url": "https://jalammar.github.io/feed.xml", "type": "blog"},
    {"name": "Colah's Blog", "url": "https://colah.github.io/rss.xml", "type": "blog"},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "type": "blog"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "type": "blog"},
    {"name": "Latent Space", "url": "https://www.latent.space/feed", "type": "blog"},
    {"name": "The Gradient", "url": "https://thegradient.pub/feed/", "type": "blog"},
    {"name": "Import AI (Jack Clark)", "url": "https://importai.substack.com/feed", "type": "blog"},
    {
        "name": "Lex Fridman Podcast",
        "url": "https://lexfridman.com/feed/podcast/",
        "type": "podcast",
    },
]


def _to_iso(dt: datetime | None) -> str:
    if not dt:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.isoformat()


def _parse_entry_datetime(entry: Any) -> datetime | None:
    # feedparser gives time.struct_time in *_parsed fields.
    ts = entry.get("published_parsed") or entry.get("updated_parsed") or entry.get("created_parsed")
    if not ts:
        return None
    try:
        return datetime(*ts[:6], tzinfo=UTC)
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
        for tag in soup.find_all(("script", "style", "noscript")):
            tag.decompose()
        for tag in soup.find_all("br"):
            tag.replace_with("\n")
        for tag in soup.find_all(_HTML_BLOCK_TAGS):
            tag.insert_before("\n\n")
            tag.insert_after("\n\n")

        paragraphs: list[str] = []
        for segment in re.split(r"\n+", soup.get_text()):
            normalized = re.sub(r"[ \t\f\v]+", " ", segment).strip()
            if normalized:
                paragraphs.append(normalized)
        return "\n\n".join(paragraphs)
    except Exception:
        return s


def _truncate_utf8_at_word_boundary(value: str, limit: int) -> tuple[str, bool]:
    """Bound feed captures without leaving a visibly cut Latin token."""

    text = str(value or "")
    raw = text.encode("utf-8")
    if len(raw) <= limit:
        return text, False

    prefix = raw[:limit].decode("utf-8", errors="ignore").rstrip()
    consumed = len(prefix.encode("utf-8"))
    remainder = raw[consumed:].decode("utf-8", errors="ignore")
    if prefix and remainder:
        left = prefix[-1]
        right = remainder[0]
        continues_token = (
            not left.isspace()
            and not right.isspace()
            and (left.isalnum() or left in "_-")
            and (right.isalnum() or right in "_-")
        )
        if continues_token:
            boundary = re.search(r"\s+\S*$", prefix)
            if boundary is not None and boundary.start() >= int(len(prefix) * 0.8):
                prefix = prefix[: boundary.start()].rstrip()
    return prefix, True


def _feed_entry_text(entry: Any) -> str:
    """Prefer the richest text already present in the RSS/Atom payload."""

    candidates: list[str] = []
    for part in entry.get("content") or []:
        value = part.get("value") if hasattr(part, "get") else ""
        cleaned = _html_to_text(str(value or "")).strip()
        if cleaned:
            candidates.append(cleaned)

    summary = entry.get("summary") or entry.get("description") or ""
    cleaned_summary = _html_to_text(str(summary or "")).strip()
    if cleaned_summary:
        candidates.append(cleaned_summary)

    return max(candidates, key=len, default="")


@dataclass(frozen=True)
class FeedConfig:
    name: str
    url: str
    type: str = "blog"  # blog | podcast | other


class BlogsPodcastsCrawler:
    """聚合多个 RSS/Atom 源，按时间排序后返回最新条目。"""

    def __init__(
        self,
        feeds: list[dict[str, str]] | None = None,
        limit: int = 10,
        timeout: int = 30,
        search_fallback: dict[str, Any] | None = None,
    ):
        self.feeds = [FeedConfig(**f) for f in (feeds or DEFAULT_FEEDS)]
        self.limit = limit
        self.timeout = timeout
        self.search_fallback_service = SearchFallbackService(search_fallback)

    def fetch(self) -> list[dict]:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (AI-Stack; +https://github.com/)"}
            all_items: list[dict[str, Any]] = []

            for feed_cfg in self.feeds:
                items = self._fetch_single_feed(feed_cfg, headers=headers)
                all_items.extend(items)

            # sort by published_dt desc
            all_items.sort(
                key=lambda x: x.get("_published_dt") or datetime.min.replace(tzinfo=UTC),
                reverse=True,
            )

            # dedupe by normalized url
            seen: set[str] = set()
            unique: list[dict[str, Any]] = []
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

    def _fetch_single_feed(
        self,
        feed_cfg: FeedConfig,
        headers: dict[str, str],
    ) -> list[dict[str, Any]]:
        try:
            resp = requests.get(feed_cfg.url, headers=headers, timeout=self.timeout)
            resp.raise_for_status()

            parsed = feedparser.parse(resp.content)
            if getattr(parsed, "bozo", False):
                # bozo_exception may include useful details; log at debug to avoid noisy runs.
                logger.debug(
                    "Feed parsing warning for %s: %s",
                    feed_cfg.url,
                    getattr(parsed, "bozo_exception", None),
                )

            items: list[dict[str, Any]] = []
            for entry in getattr(parsed, "entries", [])[: max(self.limit * 3, 50)]:
                item = self._extract_entry(entry, feed_cfg)
                if item:
                    items.append(item)
            return items
        except Exception as e:
            logger.warning(f"Failed to fetch feed {feed_cfg.name} ({feed_cfg.url}): {e}")
            fallback_items = self.search_fallback_service.search_feed_domain(
                feed_name=feed_cfg.name,
                feed_url=feed_cfg.url,
                limit=max(1, min(3, self.limit)),
                topics=[feed_cfg.name, "AI", "人工智能", "LLM", "大模型"],
                fallback_reason="feed_fetch_failed",
            )
            if fallback_items:
                logger.info(
                    f"Feed {feed_cfg.name} search fallback recovered: {len(fallback_items)} items"
                )
                return fallback_items
            return []

    def _extract_entry(self, entry: Any, feed_cfg: FeedConfig) -> dict[str, Any] | None:
        try:
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            if not title or not link:
                return None

            captured_text = _feed_entry_text(entry)
            description, capture_truncated = _truncate_utf8_at_word_boundary(
                captured_text,
                _MAX_CAPTURED_FEED_BYTES,
            )

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
                "source_is_truncated": capture_truncated,
                "source_truncation_reason": (
                    "crawler_feed_content_limit" if capture_truncated else ""
                ),
                "author": (entry.get("author") or "").strip(),
                "published": published,
                "published_at": _to_iso(published_dt),
                "feed_name": feed_cfg.name,
                "feed_url": feed_cfg.url,
                "feed_type": feed_cfg.type,
                "audio_url": audio_url,
                "tags": tags,
                "source": "blogs_podcasts",
                "crawled_at": datetime.now(UTC).isoformat(),
                "_published_dt": published_dt,
            }
        except Exception as e:
            logger.debug(f"Failed to extract feed entry ({feed_cfg.name}): {e}")
            return None
