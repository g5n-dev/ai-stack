"""
Dedup helpers for crawled items
爬取结果去重工具（跨数据源/同数据源）
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


_TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "utm_id",
    "gclid",
    "fbclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "ref_src",
}


def canonicalize_url(url: str) -> str:
    """Canonicalize URL for dedupe purposes (strip fragments + tracking params)."""
    if not url:
        return ""
    try:
        parts = urlsplit(url.strip())
        scheme = (parts.scheme or "https").lower()
        netloc = parts.netloc.lower()
        path = parts.path.rstrip("/")
        query = [(k, v) for (k, v) in parse_qsl(parts.query, keep_blank_values=True) if k not in _TRACKING_PARAMS]
        new_query = urlencode(query, doseq=True)
        return urlunsplit((scheme, netloc, path, new_query, ""))
    except Exception:
        return url.strip()


def dedupe_items(items: Iterable[Dict[str, Any]], url_field: str = "url") -> Tuple[List[Dict[str, Any]], int]:
    """Return (unique_items, removed_count). Keeps first occurrence."""
    seen: set[str] = set()
    unique: List[Dict[str, Any]] = []
    removed = 0

    for item in items:
        url = canonicalize_url(str(item.get(url_field, "") or ""))
        if not url:
            unique.append(item)
            continue
        if url in seen:
            removed += 1
            continue
        seen.add(url)
        # store normalized url back to item to reduce future duplicates
        item[url_field] = url
        unique.append(item)

    return unique, removed

