"""
Content enrichment helpers
内容增强：为爬取数据补充更多上下文（如 DeepWiki）
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Dict, Optional, Tuple
from urllib.parse import urlsplit

import html2text
import requests
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeepWikiResult:
    url: str
    text: str


def build_deepwiki_url(github_repo_url: str) -> str:
    """
    Convert a GitHub repo URL into a DeepWiki URL.
    Example: https://github.com/openai/openai-python -> https://deepwiki.com/openai/openai-python
    """
    if not github_repo_url:
        return ""
    try:
        parts = urlsplit(github_repo_url.strip())
        if parts.netloc.lower() != "github.com":
            return ""
        path = parts.path.strip("/").split("/")
        if len(path) < 2:
            return ""
        owner, repo = path[0], path[1]
        return f"https://deepwiki.com/{owner}/{repo}"
    except Exception:
        return ""


def _extract_main_prose_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # DeepWiki uses Tailwind + prose blocks; pick the most content-dense prose container.
    candidates = soup.select("div.prose")
    if not candidates:
        candidates = soup.select("div[class*='prose']")

    if candidates:
        best = max(candidates, key=lambda el: len(el.get_text(" ", strip=True)))
        return str(best)

    body = soup.body
    return str(body) if body else html


def fetch_deepwiki(github_repo_url: str, *, timeout: int = 30, max_chars: int = 8000) -> Optional[DeepWikiResult]:
    deepwiki_url = build_deepwiki_url(github_repo_url)
    if not deepwiki_url:
        return None

    try:
        resp = requests.get(deepwiki_url, headers={"User-Agent": "Mozilla/5.0 (AI-Stack)"}, timeout=timeout)
        if resp.status_code >= 400:
            return None

        prose_html = _extract_main_prose_html(resp.text)

        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0
        text = (h.handle(prose_html) or "").strip()

        # Trim to avoid blowing up LLM context; keep the beginning (usually overview/TOC).
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n[...truncated...]"

        if not text or len(text) < 200:
            return None

        return DeepWikiResult(url=deepwiki_url, text=text)

    except Exception as e:
        logger.debug(f"DeepWiki fetch failed: {e}")
        return None


def enrich_github_repo(repo_data: Dict, *, timeout: int = 30, max_chars: int = 8000) -> Dict:
    """
    Enrich GitHub repo item with DeepWiki URL + extracted text (best-effort).
    """
    repo_url = repo_data.get("url") or repo_data.get("repo_url") or ""
    deepwiki = fetch_deepwiki(repo_url, timeout=timeout, max_chars=max_chars)
    if deepwiki:
        repo_data["deepwiki_url"] = deepwiki.url
        repo_data["deepwiki_content"] = deepwiki.text
    else:
        repo_data.setdefault("deepwiki_url", build_deepwiki_url(repo_url))
        repo_data.setdefault("deepwiki_content", "")
    return repo_data

