#!/usr/bin/env python3

import os
import sys
import json
import logging
from typing import List
import requests
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SearchEngineNotifier:
    def __init__(self, base_url: str, google_api_key: str = None, google_search_console_url: str = None, bing_api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.google_api_key = google_api_key
        self.google_search_console_url = google_search_console_url
        self.bing_api_key = bing_api_key

    def get_sitemap_urls(self, sitemap_path: str = None) -> List[str]:
        if sitemap_path and os.path.exists(sitemap_path):
            with open(sitemap_path, 'r') as f:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(f.read())
                ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                urls = [loc.text for loc in root.findall('.//ns:loc', ns)]
                logger.info(f"Found {len(urls)} URLs in sitemap")
                return urls

        logger.warning(f"Sitemap not found at {sitemap_path}, using fallback")
        return [self.base_url]

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
    sitemap_path = os.getenv('SITEMAP_PATH', 'blog/public/sitemap.xml')

    logger.info(f"Base URL: {base_url}")
    logger.info(f"Sitemap path: {sitemap_path}")

    notifier = SearchEngineNotifier(
        base_url=base_url,
        google_api_key=google_api_key,
        google_search_console_url=google_search_console_url,
        bing_api_key=bing_api_key
    )

    urls = notifier.get_sitemap_urls(sitemap_path)

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
