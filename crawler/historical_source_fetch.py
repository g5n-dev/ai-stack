"""Bounded, source-specific recovery fetchers for historical Post evidence.

These adapters never publish fetched text. They return a small capture that the
historical rehydration planner can sign and render as an honest Tier-C source
brief. Arbitrary URLs are accepted only by the explicit public-article adapter,
which requires a caller-owned host allowlist and revalidates every redirect.
"""

from __future__ import annotations

import ipaddress
import json
import re
import socket
import xml.etree.ElementTree as ET
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

from ai_stack.identity import canonicalize_url
from crawler.juejin_article import JuejinArticleCapture, fetch_juejin_article

_ARXIV_ID = re.compile(r"^(?:[a-z-]+(?:\.[A-Z]{2})?/)?\d{4}\.\d{4,5}(?:v\d+)?$", re.IGNORECASE)
_GITHUB_COMPONENT = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,98}[A-Za-z0-9])?$")
_HN_ID = re.compile(r"^[1-9]\d{0,19}$")
_REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})
_MAX_API_BYTES = 512 * 1024
_MAX_HTML_BYTES = 2 * 1024 * 1024
_MAX_EXCERPT_CHARS = 6_000
_MIN_ARTICLE_CHARS = 600
# Some controlled CI/desktop environments resolve every approved public host to
# an RFC 2544 synthetic address before an outbound proxy performs the real DNS
# lookup. The exact host allowlist still applies; no arbitrary URL can use this
# exception, and private/loopback/link-local ranges remain rejected.
_OUTBOUND_PROXY_DNS = ipaddress.ip_network("198.18.0.0/15")
_BLOCKED_PAGE_MARKERS = (
    "cf-chl-",
    "captcha",
    "waf-jschallenge",
    "access denied",
    "enable javascript and cookies to continue",
)


class HistoricalSourceFetchError(ValueError):
    """Typed, safe-to-log recovery failure."""


@dataclass(frozen=True, slots=True)
class HistoricalSourceCapture:
    source: str
    title: str
    external_url: str
    source_text: str
    captured_at: str
    capture_mode: str
    source_completeness: str
    source_is_truncated: bool
    metadata: dict[str, Any]


def _now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _one_line(value: object) -> str:
    return " ".join(str(value or "").split()).strip()


def _read_response(response: Any, *, maximum_bytes: int, too_large: str) -> bytes:
    length = str(response.headers.get("Content-Length") or "").strip()
    if length.isdigit() and int(length) > maximum_bytes:
        raise HistoricalSourceFetchError(too_large)
    total = 0
    chunks: list[bytes] = []
    iterator = getattr(response, "iter_content", None)
    if callable(iterator):
        for chunk in iterator(chunk_size=64 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > maximum_bytes:
                raise HistoricalSourceFetchError(too_large)
            chunks.append(bytes(chunk))
        return b"".join(chunks)
    body = bytes(response.content)
    if len(body) > maximum_bytes:
        raise HistoricalSourceFetchError(too_large)
    return body


def _request(
    session: Any,
    url: str,
    *,
    timeout: int,
    accept: str,
    maximum_bytes: int,
    too_large: str,
) -> tuple[Any, bytes]:
    try:
        response = session.get(
            url,
            headers={
                "User-Agent": "AI-Stack-Historical-Rehydration/1.0 (+https://ai-stack.site/)",
                "Accept": accept,
            },
            timeout=timeout,
            allow_redirects=False,
            stream=True,
        )
    except requests.RequestException as exc:
        raise HistoricalSourceFetchError("source_request_failed") from exc
    try:
        body = _read_response(response, maximum_bytes=maximum_bytes, too_large=too_large)
    except Exception:
        response.close()
        raise
    return response, body


def fetch_arxiv_sources(
    arxiv_ids: Iterable[str],
    *,
    session: Any = requests,
    timeout: int = 15,
) -> list[HistoricalSourceCapture]:
    identifiers = [str(value or "").strip() for value in arxiv_ids]
    if (
        not identifiers
        or len(identifiers) > 50
        or len(set(identifiers)) != len(identifiers)
        or any(_ARXIV_ID.fullmatch(identifier) is None for identifier in identifiers)
    ):
        raise HistoricalSourceFetchError("invalid_arxiv_id")
    endpoint = "https://export.arxiv.org/api/query?" + urlencode(
        {"id_list": ",".join(identifiers)}
    )
    response, body = _request(
        session,
        endpoint,
        timeout=timeout,
        accept="application/atom+xml, application/xml;q=0.9",
        maximum_bytes=_MAX_API_BYTES,
        too_large="source_response_too_large",
    )
    try:
        if response.status_code != 200:
            raise HistoricalSourceFetchError(f"source_http_{response.status_code}")
        content_type = str(response.headers.get("Content-Type") or "").casefold()
        if "xml" not in content_type:
            raise HistoricalSourceFetchError("source_content_type_invalid")
        try:
            root = ET.fromstring(body)
        except ET.ParseError as exc:
            raise HistoricalSourceFetchError("source_payload_invalid") from exc
    finally:
        response.close()

    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    entries = root.findall("atom:entry", ns)
    if not entries:
        raise HistoricalSourceFetchError("source_record_not_found")
    captured_at = _now_iso()
    by_identifier: dict[str, HistoricalSourceCapture] = {}
    for entry in entries:
        entry_id = _one_line(entry.findtext("atom:id", default="", namespaces=ns))
        identifier = entry_id.rsplit("/", 1)[-1]
        if identifier not in identifiers or identifier in by_identifier:
            raise HistoricalSourceFetchError("source_identity_mismatch")
        title = _one_line(entry.findtext("atom:title", default="", namespaces=ns))
        summary = _one_line(entry.findtext("atom:summary", default="", namespaces=ns))
        if not title or not summary:
            raise HistoricalSourceFetchError("source_payload_incomplete")
        authors = [
            _one_line(author.findtext("atom:name", default="", namespaces=ns))
            for author in entry.findall("atom:author", ns)
        ]
        authors = [author for author in authors if author]
        primary = entry.find("arxiv:primary_category", ns)
        category = _one_line(primary.get("term") if primary is not None else "")
        published = _one_line(
            entry.findtext("atom:published", default="", namespaces=ns)
        )
        by_identifier[identifier] = HistoricalSourceCapture(
            source="arxiv",
            title=title,
            external_url=f"https://arxiv.org/abs/{identifier}",
            source_text=summary,
            captured_at=captured_at,
            capture_mode="abstract",
            source_completeness="abstract_only",
            source_is_truncated=False,
            metadata={
                "arxiv_id": identifier,
                "authors": authors,
                "category": category,
                "published": published,
                "pdf_url": f"https://arxiv.org/pdf/{identifier}.pdf",
            },
        )
    missing = [identifier for identifier in identifiers if identifier not in by_identifier]
    if missing:
        raise HistoricalSourceFetchError("source_record_not_found")
    return [by_identifier[identifier] for identifier in identifiers]


def fetch_arxiv_source(
    arxiv_id: str,
    *,
    session: Any = requests,
    timeout: int = 15,
) -> HistoricalSourceCapture:
    return fetch_arxiv_sources([arxiv_id], session=session, timeout=timeout)[0]


def fetch_github_source(
    owner: str,
    repository: str,
    *,
    session: Any = requests,
    timeout: int = 15,
) -> HistoricalSourceCapture:
    owner_name = str(owner or "").strip()
    repository_name = str(repository or "").strip()
    if (
        _GITHUB_COMPONENT.fullmatch(owner_name) is None
        or _GITHUB_COMPONENT.fullmatch(repository_name) is None
        or owner_name in {".", ".."}
        or repository_name in {".", ".."}
    ):
        raise HistoricalSourceFetchError("invalid_github_locator")
    endpoint = f"https://api.github.com/repos/{owner_name}/{repository_name}"
    response, body = _request(
        session,
        endpoint,
        timeout=timeout,
        accept="application/vnd.github+json",
        maximum_bytes=_MAX_API_BYTES,
        too_large="source_response_too_large",
    )
    try:
        if response.status_code != 200:
            raise HistoricalSourceFetchError(f"source_http_{response.status_code}")
        if "json" not in str(response.headers.get("Content-Type") or "").casefold():
            raise HistoricalSourceFetchError("source_content_type_invalid")
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise HistoricalSourceFetchError("source_payload_invalid") from exc
    finally:
        response.close()
    if not isinstance(payload, dict):
        raise HistoricalSourceFetchError("source_payload_invalid")
    expected = f"{owner_name}/{repository_name}".casefold()
    full_name = _one_line(payload.get("full_name"))
    if full_name.casefold() != expected:
        raise HistoricalSourceFetchError("source_identity_mismatch")
    external_url = canonicalize_url(_one_line(payload.get("html_url")))
    if urlsplit(external_url).hostname != "github.com":
        raise HistoricalSourceFetchError("source_identity_mismatch")
    description = _one_line(payload.get("description"))
    license_data = payload.get("license") if isinstance(payload.get("license"), dict) else {}
    topics = payload.get("topics") if isinstance(payload.get("topics"), list) else []
    return HistoricalSourceCapture(
        source="github_trending",
        title=full_name,
        external_url=external_url,
        source_text=description or full_name,
        captured_at=_now_iso(),
        capture_mode="metadata_only",
        source_completeness="metadata_only",
        source_is_truncated=False,
        metadata={
            "language": _one_line(payload.get("language")),
            "stars": int(payload.get("stargazers_count") or 0),
            "forks": int(payload.get("forks_count") or 0),
            "license": _one_line(license_data.get("spdx_id")),
            "topics": [_one_line(topic) for topic in topics if _one_line(topic)][:20],
            "updated_at": _one_line(payload.get("updated_at")),
        },
    )


def fetch_hacker_news_source(
    hn_id: str,
    *,
    session: Any = requests,
    timeout: int = 15,
) -> HistoricalSourceCapture:
    identifier = str(hn_id or "").strip()
    if _HN_ID.fullmatch(identifier) is None:
        raise HistoricalSourceFetchError("invalid_hn_id")
    endpoint = f"https://hacker-news.firebaseio.com/v0/item/{identifier}.json"
    response, body = _request(
        session,
        endpoint,
        timeout=timeout,
        accept="application/json",
        maximum_bytes=_MAX_API_BYTES,
        too_large="source_response_too_large",
    )
    try:
        if response.status_code != 200:
            raise HistoricalSourceFetchError(f"source_http_{response.status_code}")
        if "json" not in str(response.headers.get("Content-Type") or "").casefold():
            raise HistoricalSourceFetchError("source_content_type_invalid")
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise HistoricalSourceFetchError("source_payload_invalid") from exc
    finally:
        response.close()
    if not isinstance(payload, dict) or str(payload.get("id")) != identifier:
        raise HistoricalSourceFetchError("source_identity_mismatch")
    if _one_line(payload.get("type")) != "story" or payload.get("deleted") is True:
        raise HistoricalSourceFetchError("source_record_unavailable")
    title = _one_line(payload.get("title"))
    if not title:
        raise HistoricalSourceFetchError("source_payload_incomplete")
    raw_url = _one_line(payload.get("url"))
    if raw_url:
        try:
            external_url = canonicalize_url(raw_url)
        except ValueError as exc:
            raise HistoricalSourceFetchError("source_external_url_invalid") from exc
    else:
        external_url = f"https://news.ycombinator.com/item?id={identifier}"
    timestamp = int(payload.get("time") or 0)
    published = (
        datetime.fromtimestamp(timestamp, UTC).isoformat().replace("+00:00", "Z")
        if timestamp > 0
        else ""
    )
    return HistoricalSourceCapture(
        source="hacker_news",
        title=title,
        external_url=external_url,
        source_text=title,
        captured_at=_now_iso(),
        capture_mode="metadata_only",
        source_completeness="metadata_only",
        source_is_truncated=False,
        metadata={
            "hn_id": int(identifier),
            "author": _one_line(payload.get("by")),
            "score": int(payload.get("score") or 0),
            "descendants": int(payload.get("descendants") or 0),
            "published": published,
        },
    )


def _default_resolver(hostname: str) -> set[str]:
    try:
        return {
            item[4][0]
            for item in socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)
        }
    except OSError as exc:
        raise HistoricalSourceFetchError("source_dns_failed") from exc


def _validate_public_url(
    value: str,
    *,
    allowed_hosts: set[str],
    resolver: Callable[[str], Iterable[str]],
) -> str:
    raw = str(value or "").strip()
    try:
        canonicalize_url(raw)
    except ValueError as exc:
        raise HistoricalSourceFetchError("source_url_not_allowed") from exc
    parsed = urlsplit(raw)
    hostname = (parsed.hostname or "").casefold()
    normalized_hosts = {str(host).strip().casefold() for host in allowed_hosts}
    if (
        parsed.scheme.casefold() != "https"
        or not hostname
        or hostname not in normalized_hosts
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port not in {None, 443}
    ):
        raise HistoricalSourceFetchError("source_url_not_allowed")
    addresses = set(resolver(hostname))
    if not addresses:
        raise HistoricalSourceFetchError("source_dns_failed")
    try:
        parsed_addresses = [ipaddress.ip_address(address) for address in addresses]
    except ValueError as exc:
        raise HistoricalSourceFetchError("source_dns_failed") from exc
    if any(
        not address.is_global and address not in _OUTBOUND_PROXY_DNS
        for address in parsed_addresses
    ):
        raise HistoricalSourceFetchError("source_host_not_public")
    netloc = hostname if parsed.port in {None, 443} else f"{hostname}:{parsed.port}"
    return urlunsplit(("https", netloc, parsed.path or "/", parsed.query, ""))


def _article_text(document: str) -> tuple[str, str]:
    folded = document.casefold()
    if any(marker in folded for marker in _BLOCKED_PAGE_MARKERS):
        raise HistoricalSourceFetchError("source_access_interstitial")
    soup = BeautifulSoup(document, "lxml")
    title_node = (
        soup.select_one('meta[property="og:title"]')
        or soup.select_one('meta[name="twitter:title"]')
        or soup.select_one("title")
        or soup.select_one("h1")
    )
    if title_node is None:
        raise HistoricalSourceFetchError("source_title_missing")
    title = _one_line(title_node.get("content") or title_node.get_text(" ", strip=True))
    if not title:
        raise HistoricalSourceFetchError("source_title_missing")
    container = soup.select_one("article") or soup.select_one("main")
    if container is None:
        raise HistoricalSourceFetchError("source_article_not_found")
    for node in container.select(
        "script, style, noscript, iframe, form, nav, footer, header, aside, button, svg"
    ):
        node.decompose()
    paragraphs = [
        _one_line(node.get_text(" ", strip=True))
        for node in container.select("p, li")
    ]
    paragraphs = [paragraph for paragraph in paragraphs if len(paragraph) >= 24]
    text = "\n\n".join(paragraphs)
    if len(paragraphs) < 3 or len(re.sub(r"\s+", "", text)) < _MIN_ARTICLE_CHARS:
        raise HistoricalSourceFetchError("source_article_incomplete")
    return title, text


def _bounded_excerpt(text: str, maximum_chars: int = _MAX_EXCERPT_CHARS) -> tuple[str, bool]:
    if len(text) <= maximum_chars:
        return text, False
    paragraphs = text.split("\n\n")
    selected: list[str] = []
    size = 0
    for paragraph in paragraphs:
        added = len(paragraph) + (2 if selected else 0)
        if size + added > maximum_chars:
            break
        selected.append(paragraph)
        size += added
    if not selected:
        selected = [text[:maximum_chars].rstrip()]
    return "\n\n".join(selected), True


def fetch_public_article_excerpt(
    source_url: str,
    *,
    allowed_hosts: set[str],
    session: Any = requests,
    resolver: Callable[[str], Iterable[str]] = _default_resolver,
    timeout: int = 15,
    max_redirects: int = 3,
) -> HistoricalSourceCapture:
    origin = _validate_public_url(
        source_url,
        allowed_hosts=allowed_hosts,
        resolver=resolver,
    )
    current = origin
    redirects = 0
    while True:
        response, body = _request(
            session,
            current,
            timeout=timeout,
            accept="text/html,application/xhtml+xml;q=0.9",
            maximum_bytes=_MAX_HTML_BYTES,
            too_large="source_response_too_large",
        )
        try:
            if response.status_code in _REDIRECT_STATUSES:
                if redirects >= max_redirects:
                    raise HistoricalSourceFetchError("source_redirect_limit")
                location = str(response.headers.get("Location") or "").strip()
                if not location:
                    raise HistoricalSourceFetchError("source_redirect_invalid")
                current = _validate_public_url(
                    urljoin(current, location),
                    allowed_hosts=allowed_hosts,
                    resolver=resolver,
                )
                redirects += 1
                continue
            if response.status_code != 200:
                raise HistoricalSourceFetchError(f"source_http_{response.status_code}")
            content_type = str(response.headers.get("Content-Type") or "").casefold()
            if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
                raise HistoricalSourceFetchError("source_content_type_invalid")
            try:
                document = body.decode("utf-8")
            except UnicodeDecodeError:
                document = body.decode("utf-8", errors="replace")
            title, full_text = _article_text(document)
            excerpt, truncated = _bounded_excerpt(full_text)
            return HistoricalSourceCapture(
                source="blogs_podcasts",
                title=title,
                external_url=current,
                source_text=excerpt,
                captured_at=_now_iso(),
                capture_mode="excerpt",
                source_completeness="partial",
                source_is_truncated=truncated,
                metadata={
                    "origin_url": origin,
                    "source_text_chars_original": len(full_text),
                    "redirect_count": redirects,
                },
            )
        finally:
            response.close()


def fetch_juejin_source_excerpt(
    source_url: str,
    *,
    discovery_title: str,
    fetcher: Callable[..., JuejinArticleCapture] = fetch_juejin_article,
    timeout: int = 15,
) -> HistoricalSourceCapture:
    """Recover a verified SSR body but expose only a bounded Tier-C excerpt.

    The complete capture can later feed an independently reviewed Tier-B
    rewrite. Historical bulk repair deliberately does not republish that body.
    """

    fallback_title = _one_line(discovery_title)
    if not fallback_title:
        raise HistoricalSourceFetchError("source_title_missing")
    try:
        article = fetcher(source_url, timeout=timeout)
    except (OSError, ValueError) as exc:
        reason = str(exc).strip() or "source_request_failed"
        raise HistoricalSourceFetchError(reason) from exc
    title = _one_line(article.title) or fallback_title
    source_text, _storage_truncated = _bounded_excerpt(article.plain_text)
    if not source_text:
        raise HistoricalSourceFetchError("source_article_incomplete")
    return HistoricalSourceCapture(
        source="juejin",
        title=title,
        external_url=article.source_url,
        source_text=source_text,
        captured_at=_now_iso(),
        capture_mode="excerpt",
        source_completeness="partial",
        # An excerpt is intentionally incomplete even when the temporary SSR
        # capture was complete; the full source is never published by bulk repair.
        source_is_truncated=True,
        metadata={
            "article_id": article.article_id,
            "heading_count": article.heading_count,
            "code_block_count": article.code_block_count,
            "source_truncation_reason": "historical_excerpt_only",
        },
    )


__all__ = [
    "HistoricalSourceCapture",
    "HistoricalSourceFetchError",
    "fetch_arxiv_source",
    "fetch_arxiv_sources",
    "fetch_github_source",
    "fetch_hacker_news_source",
    "fetch_juejin_source_excerpt",
    "fetch_public_article_excerpt",
]
