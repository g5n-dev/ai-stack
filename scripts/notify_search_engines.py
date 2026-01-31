#!/usr/bin/env python3

import os
import sys
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple
import requests
from urllib.parse import urljoin, urlparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def _parse_iso_datetime(value: str) -> Optional[datetime]:
    v = (value or "").strip()
    if not v:
        return None
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(v)
    except Exception:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(str(raw).strip())
    except Exception:
        return default


def _split_prefixes(raw: str) -> List[str]:
    parts = [p.strip() for p in (raw or "").split(",")]
    return [p for p in parts if p]


def _path_matches_prefix(path: str, prefix: str) -> bool:
    if prefix == "/":
        return path == "/"
    return path.startswith(prefix)


def _select_indexnow_urls(entries: List[Tuple[str, Optional[datetime]]], base_url: str) -> List[str]:
    days = _parse_int_env("BING_INDEXNOW_DAYS", 2)
    if days < 0:
        days = 2

    include_prefixes_raw = os.getenv("BING_INDEXNOW_INCLUDE_PREFIXES", "/posts/,/scenarios/,/about/,/")
    exclude_prefixes_raw = os.getenv("BING_INDEXNOW_EXCLUDE_PREFIXES", "/tags/,/categories/,/page/,/index.xml,/sitemap.xml,/robots.txt")
    include_prefixes = _split_prefixes(include_prefixes_raw)
    exclude_prefixes = _split_prefixes(exclude_prefixes_raw)

    threshold = datetime.now(timezone.utc) - timedelta(days=days)
    def pick(require_recent: bool) -> List[str]:
        selected: List[Tuple[datetime, str]] = []
        for url, lastmod in entries:
            if not url:
                continue
            path = urlparse(url).path or "/"
            if any(_path_matches_prefix(path, p) for p in exclude_prefixes):
                continue
            if include_prefixes and not any(_path_matches_prefix(path, p) for p in include_prefixes):
                continue
            if require_recent and lastmod is not None and lastmod < threshold:
                continue
            selected.append((lastmod or datetime.min.replace(tzinfo=timezone.utc), url))

        def prio(path: str) -> int:
            if path.startswith("/posts/"):
                return 0
            if path == "/":
                return 1
            if path == "/about/" or path.startswith("/about/"):
                return 2
            if path == "/scenarios/" or path.startswith("/scenarios/"):
                return 3
            return 9

        def sort_key(item: Tuple[datetime, str]) -> Tuple[int, float, str]:
            lastmod_dt, url = item
            path = urlparse(url).path or "/"
            ts = lastmod_dt.timestamp() if lastmod_dt != datetime.min.replace(tzinfo=timezone.utc) else 0.0
            return (prio(path), -ts, url)

        selected.sort(key=sort_key)
        return [u for _, u in selected]

    urls = pick(require_recent=True)
    if not urls:
        urls = pick(require_recent=False)
    if not urls:
        return [base_url.rstrip("/") + "/"]
    return urls



class SearchEngineNotifier:
    def __init__(
        self,
        base_url: str,
        google_api_key: str = None,
        google_search_console_url: str = None,
        bing_api_key: str = None,
        bing_max_urls: Optional[int] = None,
    ):
        self.base_url = base_url.rstrip('/')
        self.google_api_key = google_api_key
        self.google_search_console_url = google_search_console_url
        self.bing_api_key = bing_api_key
        self.bing_max_urls = bing_max_urls

    def get_sitemap_entries(self, sitemap_path: str = None) -> List[Tuple[str, Optional[datetime]]]:
        if sitemap_path and os.path.exists(sitemap_path):
            with open(sitemap_path, 'r') as f:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(f.read())
                ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                url_elems = root.findall('.//ns:url', ns)
                best: dict[str, Optional[datetime]] = {}
                for el in url_elems:
                    loc_el = el.find('ns:loc', ns)
                    if loc_el is None or not (loc_el.text or "").strip():
                        continue
                    loc = loc_el.text.strip()
                    lastmod_el = el.find('ns:lastmod', ns)
                    lastmod = _parse_iso_datetime(lastmod_el.text if lastmod_el is not None else None)
                    prev = best.get(loc)
                    if prev is None or (lastmod is not None and lastmod > prev):
                        best[loc] = lastmod
                entries = list(best.items())
                logger.info(f"Found {len(entries)} URLs in sitemap")
                return entries

        logger.warning(f"Sitemap not found at {sitemap_path}, using fallback")
        return [(self.base_url, None)]

    def notify_google(self, urls: List[str]) -> bool:
        if not self.google_api_key or not self.google_search_console_url:
            logger.warning("Google API credentials not configured, skipping Google indexing")
            return False

        google_url = f"{self.google_search_console_url}?key={self.google_api_key}"

        try:
            for url in urls[:100]:
                payload = {"url": url}
                response = requests.post(google_url, json=payload, timeout=30)
                if response.status_code == 200:
                    logger.info(f"✓ Google indexing request sent: {url}")
                else:
                    logger.warning(f"✗ Google indexing failed: {url} - {response.text}")
            return True
        except Exception as e:
            logger.error(f"Error notifying Google: {e}")
            return False

    def notify_bing(self, urls: List[str]) -> bool:
        if not self.bing_api_key:
            logger.warning("Bing API key not configured, skipping Bing indexing")
            return False

        bing_url = "https://www.bing.com/indexnow"
        host = self.base_url.replace('https://', '').replace('http://', '').split('/')[0]

        try:
            if self.bing_max_urls is not None and self.bing_max_urls > 0:
                urls = urls[:self.bing_max_urls]
            batch_size = 100
            for i in range(0, len(urls), batch_size):
                batch = urls[i:i + batch_size]
                payload = {
                    "host": host,
                    "key": self.bing_api_key,
                    "urlList": batch
                }
                response = requests.post(bing_url, json=payload, timeout=30)
                if response.status_code == 200:
                    logger.info(f"✓ Bing indexing request sent for batch {i//batch_size + 1} ({len(batch)} URLs)")
                else:
                    logger.warning(f"✗ Bing indexing failed for batch {i//batch_size + 1}: {response.text}")
            return True
        except Exception as e:
            logger.error(f"Error notifying Bing: {e}")
            return False


def main():
    base_url = os.getenv('SITE_BASE_URL', 'https://ai-stack.site/')
    google_api_key = os.getenv('GOOGLE_INDEXING_API_KEY')
    google_search_console_url = os.getenv('GOOGLE_INDEXING_API_URL', 'https://indexing.googleapis.com/v3/urlNotifications:publish')
    bing_api_key = os.getenv('BING_INDEXNOW_API_KEY')
    bing_max_urls_raw = os.getenv('BING_INDEXNOW_MAX_URLS', '80')
    sitemap_path = os.getenv('SITEMAP_PATH', 'blog/public/sitemap.xml')

    logger.info(f"Base URL: {base_url}")
    logger.info(f"Sitemap path: {sitemap_path}")

    try:
        bing_max_urls = int(bing_max_urls_raw)
    except Exception:
        bing_max_urls = 80
    if bing_max_urls < 0:
        bing_max_urls = 80

    notifier = SearchEngineNotifier(
        base_url=base_url,
        google_api_key=google_api_key,
        google_search_console_url=google_search_console_url,
        bing_api_key=bing_api_key,
        bing_max_urls=bing_max_urls,
    )

    entries = notifier.get_sitemap_entries(sitemap_path)
    urls = _select_indexnow_urls(entries, base_url)
    logger.info(f"IndexNow candidate URLs: {len(urls)}")

    if not urls:
        logger.error("No URLs found to submit")
        sys.exit(1)

    google_success = notifier.notify_google(urls)
    bing_success = notifier.notify_bing(urls)

    if google_success or bing_success:
        logger.info("✓ Search engine indexing completed successfully")
        sys.exit(0)
    else:
        logger.warning("No search engines were notified (check API credentials)")
        sys.exit(1)


if __name__ == '__main__':
    main()
