"""
Hacker News crawler
爬取 Hacker News 热门内容
"""

import requests
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HackerNewsCrawler:
    """爬取 Hacker News 热门故事"""

    def __init__(self, limit=5):
        self.limit = limit
        self.api_base = 'https://hacker-news.firebaseio.com/v0'

    def fetch(self) -> List[Dict]:
        """
        获取热门故事列表

        Returns:
            List[Dict]: 故事信息列表
        """
        try:
            # 获取热门故事 ID 列表
            top_stories_url = f'{self.api_base}/topstories.json'
            response = requests.get(top_stories_url, timeout=10)
            response.raise_for_status()

            # 预取更多 ID，避免过滤（无 URL / 非 story）导致数量不足
            story_ids = response.json()[: max(self.limit * 3, self.limit)]

            # 获取每个故事的详细信息
            stories = []
            for story_id in story_ids:
                story = self._fetch_story(story_id)
                if story:
                    stories.append(story)
                if len(stories) >= self.limit:
                    break

            return stories

        except Exception as e:
            logger.error(f"Failed to fetch Hacker News: {e}")
            return []

    def _fetch_story(self, story_id: int) -> Dict:
        """
        获取单个故事的详细信息

        Args:
            story_id: 故事 ID

        Returns:
            Dict: 故事信息
        """
        try:
            story_url = f'{self.api_base}/item/{story_id}.json'
            response = requests.get(story_url, timeout=10)
            response.raise_for_status()

            story_data = response.json()

            # 只返回有效的故事
            if not story_data or story_data.get('type') != 'story':
                return None

            # 过滤掉没有 URL 的故事（通常是 Ask HN 等）
            if not story_data.get('url'):
                return None

            return {
                'title': story_data.get('title', ''),
                'url': story_data.get('url', ''),
                'author': story_data.get('by', ''),
                'score': story_data.get('score', 0),
                'time': story_data.get('time', 0),
                'descendants': story_data.get('descendants', 0),
                'hn_id': story_id,
                'source': 'hacker_news',
                'crawled_at': datetime.now().isoformat()
            }

        except Exception as e:
            logger.warning(f"Failed to fetch story {story_id}: {e}")
            return None


if __name__ == '__main__':
    crawler = HackerNewsCrawler(limit=5)
    stories = crawler.fetch()
    print(f"Found {len(stories)} Hacker News stories:")
    for story in stories:
        print(f"\n{story['title']}")
        print(f"  Score: {story['score']} | Comments: {story['descendants']}")
        print(f"  URL: {story['url']}")
