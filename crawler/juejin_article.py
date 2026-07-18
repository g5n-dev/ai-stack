"""Fail-closed extraction of server-rendered Juejin article bodies.

The public Juejin page can return either the complete server-rendered article or
an interstitial WAF challenge.  This module never attempts to solve or bypass
that challenge: callers receive a typed error and must keep the RSS Tier-C
brief instead.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlsplit

import html2text
import requests
from bs4 import BeautifulSoup

_ARTICLE_PATH_RE = re.compile(r"^/post/(?P<article_id>\d+)(?:/)?$")
_WAF_MARKERS = (
    "waf-jschallenge",
    "wafjs('start')",
    "please wait...",
    "_wafchallengeid",
)
_MAX_RESPONSE_BYTES = 2 * 1024 * 1024


class JuejinArticleAccessError(ValueError):
    """Raised when a Juejin response cannot prove a complete article capture."""


@dataclass(frozen=True, slots=True)
class JuejinArticleCapture:
    article_id: str
    source_url: str
    markdown: str
    plain_text: str
    heading_count: int
    code_block_count: int
    title: str = ""


def _article_id_from_url(value: str) -> str:
    parsed = urlsplit(str(value or "").strip())
    hostname = (parsed.hostname or "").casefold()
    if parsed.scheme.casefold() != "https":
        raise JuejinArticleAccessError("invalid_source_url")
    if hostname not in {"juejin.cn", "www.juejin.cn"}:
        raise JuejinArticleAccessError("invalid_source_host")
    match = _ARTICLE_PATH_RE.fullmatch(parsed.path)
    if match is None:
        raise JuejinArticleAccessError("invalid_article_url")
    return match.group("article_id")


def extract_juejin_article_html(
    document: str,
    *,
    expected_article_id: str,
    source_url: str,
    minimum_text_chars: int = 600,
) -> JuejinArticleCapture:
    """Extract one complete SSR article or fail without returning partial text."""

    expected = str(expected_article_id or "").strip()
    if not expected.isdigit():
        raise JuejinArticleAccessError("invalid_expected_article_id")
    if _article_id_from_url(source_url) != expected:
        raise JuejinArticleAccessError("article_id_mismatch")

    raw = str(document or "")
    folded = raw.casefold()
    if any(marker in folded for marker in _WAF_MARKERS):
        raise JuejinArticleAccessError("waf_challenge")

    soup = BeautifulSoup(raw, "lxml")
    articles = soup.select("article[data-entry-id]")
    if not articles:
        raise JuejinArticleAccessError("article_not_found")
    article = next(
        (node for node in articles if str(node.get("data-entry-id") or "") == expected),
        None,
    )
    if article is None:
        raise JuejinArticleAccessError("article_id_mismatch")

    article_open = re.search(
        rf"<article\b(?=[^>]*\bdata-entry-id\s*=\s*(['\"]?){re.escape(expected)}\1(?:\s|>))[^>]*>",
        raw,
        re.IGNORECASE,
    )
    if article_open is None or re.search(
        r"</article\s*>", raw[article_open.end() :], re.IGNORECASE
    ) is None:
        raise JuejinArticleAccessError("article_structure_incomplete")

    body = (
        article.select_one("#article-root .article-viewer.markdown-body")
        or article.select_one(".article-viewer.markdown-body")
        or article.select_one(".markdown-body")
        or article.select_one(".article-content")
    )
    if body is None:
        raise JuejinArticleAccessError("article_body_not_found")
    for unwanted in body.select("script, style, noscript, iframe, form, button"):
        unwanted.decompose()

    heading_count = len(body.select("h1, h2, h3, h4, h5, h6"))
    code_block_count = len(body.select("pre"))
    plain_text = body.get_text("\n", strip=True)
    if len(re.sub(r"\s+", "", plain_text)) < minimum_text_chars:
        raise JuejinArticleAccessError("article_body_too_short")
    if heading_count < 2:
        raise JuejinArticleAccessError("article_structure_incomplete")

    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = True
    converter.ignore_links = False
    converter.ignore_emphasis = False
    converter.single_line_break = False
    markdown = converter.handle(str(body)).strip()
    if not markdown or len(re.sub(r"\s+", "", markdown)) < minimum_text_chars:
        raise JuejinArticleAccessError("article_markdown_too_short")

    title_node = (
        article.select_one("h1.article-title")
        or article.select_one("h1")
        or soup.select_one('meta[property="og:title"]')
        or soup.select_one("title")
    )
    source_title = ""
    if title_node is not None:
        source_title = " ".join(
            str(title_node.get("content") or title_node.get_text(" ", strip=True)).split()
        ).strip()

    return JuejinArticleCapture(
        article_id=expected,
        source_url=source_url,
        markdown=markdown,
        plain_text=plain_text,
        heading_count=heading_count,
        code_block_count=code_block_count,
        title=source_title,
    )


def fetch_juejin_article(
    source_url: str,
    *,
    timeout: int = 10,
    session: requests.Session | None = None,
) -> JuejinArticleCapture:
    """Fetch one public article once; WAF/interstitial responses are not bypassed."""

    article_id = _article_id_from_url(source_url)
    client = session or requests
    response = client.get(
        source_url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; AI-Stack/1.0; +https://ai-stack.site/)",
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        },
        timeout=timeout,
        allow_redirects=False,
        stream=True,
    )
    try:
        if response.status_code != 200:
            raise JuejinArticleAccessError(f"http_status_{response.status_code}")
        content_type = str(response.headers.get("Content-Type") or "").casefold()
        if "text/html" not in content_type:
            raise JuejinArticleAccessError("invalid_content_type")
        final_id = _article_id_from_url(str(response.url))
        if final_id != article_id:
            raise JuejinArticleAccessError("article_id_mismatch")
        chunks: list[bytes] = []
        total = 0
        for chunk in response.iter_content(chunk_size=64 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > _MAX_RESPONSE_BYTES:
                raise JuejinArticleAccessError("article_response_too_large")
            chunks.append(chunk)
        encoding = str(response.encoding or "utf-8")
        try:
            document = b"".join(chunks).decode(encoding, errors="replace")
        except LookupError as exc:
            raise JuejinArticleAccessError("invalid_response_encoding") from exc
    finally:
        response.close()
    return extract_juejin_article_html(
        document,
        expected_article_id=article_id,
        source_url=source_url,
    )


__all__ = [
    "JuejinArticleAccessError",
    "JuejinArticleCapture",
    "extract_juejin_article_html",
    "fetch_juejin_article",
]
