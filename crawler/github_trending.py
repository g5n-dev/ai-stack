"""
GitHub Trending crawler
爬取 GitHub Trending 数据
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubTrendingCrawler:
    """爬取 GitHub Trending 仓库"""

    def __init__(self, period='daily', language='all', spoken_language='zh', limit=10):
        self.period = period  # 'daily' or 'weekly'
        self.language = language
        self.spoken_language = spoken_language
        self.limit = limit
        self.base_url = "https://github.com/trending"

    def fetch(self) -> List[Dict]:
        """
        获取 Trending 数据

        Returns:
            List[Dict]: 仓库信息列表
        """
        try:
            params = {
                'since': self.period,
                'spoken_language_code': self.spoken_language
            }
            if self.language != 'all':
                params['l'] = self.language

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(self.base_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()

            repos = self.parse(response.text)
            return repos[:self.limit]

        except Exception as e:
            logger.error(f"Failed to fetch GitHub Trending: {e}")
            return []

    def parse(self, html: str) -> List[Dict]:
        """
        解析 GitHub Trending 页面

        Args:
            html: 页面 HTML 内容

        Returns:
            List[Dict]: 解析后的仓库信息
        """
        soup = BeautifulSoup(html, 'html.parser')
        repos = []

        articles = soup.find_all('article', class_='Box-row')
        for article in articles:
            try:
                repo_info = self._extract_repo_info(article)
                if repo_info:
                    repos.append(repo_info)
            except Exception as e:
                logger.warning(f"Failed to parse repository: {e}")
                continue

        return repos

    def _extract_repo_info(self, article) -> Dict:
        """从文章元素中提取仓库信息"""
        # 获取仓库标题和链接
        title_elem = article.find('h2', class_='h3')
        if not title_elem:
            return None

        link_elem = title_elem.find('a')
        if not link_elem:
            return None

        repo_name = link_elem.text.strip()
        repo_url = 'https://github.com' + link_elem.get('href', '')

        # 获取描述
        desc_elem = article.find('p', class_='col-9')
        description = desc_elem.text.strip() if desc_elem else ''

        # 获取编程语言
        language_elem = article.find('span', class_='d-inline-block')
        language = language_elem.text.strip() if language_elem else ''

        # 获取星标数
        stars_elem = article.find('a', href=lambda x: x and 'stargazers' in x)
        stars = stars_elem.text.strip() if stars_elem else '0'

        # 获取 forks 数
        forks_elem = article.find('a', href=lambda x: x and 'network/members' in x)
        forks = forks_elem.text.strip() if forks_elem else '0'

        # 获取今日星标增长
        today_stars_elem = article.find('span', class_='d-inline-block float-sm-right')
        today_stars = today_stars_elem.text.strip() if today_stars_elem else '0'

        return {
            'title': repo_name,
            'url': repo_url,
            'description': description,
            'language': language,
            'stars': stars,
            'forks': forks,
            'today_stars': today_stars,
            'source': 'github_trending',
            'crawled_at': datetime.now().isoformat()
        }


if __name__ == '__main__':
    crawler = GitHubTrendingCrawler(limit=5)
    repos = crawler.fetch()
    print(f"Found {len(repos)} trending repositories:")
    for repo in repos:
        print(f"\n{repo['title']}")
        print(f"  Stars: {repo['stars']} (+{repo['today_stars']})")
        print(f"  Description: {repo['description'][:100]}...")
