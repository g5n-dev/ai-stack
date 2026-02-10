"""
Juejin RSS crawler
爬取掘金 RSS 内容
"""

import feedparser
from datetime import datetime
from typing import List, Dict
import logging
import html
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JuejinRSSCrawler:
    """爬取掘金 RSS 内容"""

    def __init__(self, rss_url=None, tags=None, limit=5):
        self.rss_url = rss_url or 'https://juejin.cn/rss/frontend'
        self.tags = tags or []
        self.limit = limit

    def fetch(self) -> List[Dict]:
        """
        获取 RSS 文章列表

        Returns:
            List[Dict]: 文章信息列表
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (AI-Stack; +https://github.com/)",
                "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
            }
            resp = requests.get(self.rss_url, headers=headers, timeout=15)
            resp.raise_for_status()
            feed = feedparser.parse(resp.text)

            if feed.bozo:
                logger.warning(f"RSS feed parsing warning: {feed.bozo}")

            articles = []
            for entry in feed.entries[:self.limit * 2]:  # 获取更多以进行过滤
                article = self._extract_article_info(entry)
                if article:
                    articles.append(article)

            return articles[:self.limit]

        except Exception as e:
            logger.error(f"Failed to fetch Juejin RSS: {e}")
            return []

    def _extract_article_info(self, entry) -> Dict:
        """从 RSS 条目中提取文章信息"""
        try:
            title = html.unescape(entry.get('title', '') or '')
            link = entry.get('link', '') or ''
            description = entry.get('summary', '') or entry.get('description', '') or ''
            author = entry.get('author', '')
            published = entry.get('published', '')
            tags = [tag.get('term', '') for tag in entry.get('tags', [])]

            # 如果指定了标签，检查是否匹配
            keywords = [str(t).strip() for t in (self.tags or []) if str(t).strip()]
            if keywords:
                hay = " ".join([title, description, " ".join(str(t) for t in tags)]).lower()
                if not any(k.lower() in hay for k in keywords):
                    return None

            # 清理 HTML 标签
            if description:
                # 简单的 HTML 清理
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(description, 'html.parser')
                description = soup.get_text(" ", strip=True)
                description = html.unescape(description)

            return {
                'title': title,
                'url': link,
                'description': description,
                'author': author,
                'published': published,
                'tags': tags,
                'source': 'juejin',
                'crawled_at': datetime.now().isoformat()
            }

        except Exception as e:
            logger.warning(f"Failed to extract article info: {e}")
            return None


if __name__ == '__main__':
    crawler = JuejinRSSCrawler(limit=5)
    articles = crawler.fetch()
    print(f"Found {len(articles)} Juejin articles:")
    for article in articles:
        print(f"\n{article['title']}")
        print(f"  Author: {article['author']}")
        print(f"  Description: {article['description'][:100]}...")
