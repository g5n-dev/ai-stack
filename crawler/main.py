"""
Crawler orchestrator
爬虫调度器 - 统一管理所有爬虫
"""

import yaml
import logging
from typing import List, Dict
from pathlib import Path

from .github_trending import GitHubTrendingCrawler
from .hacker_news import HackerNewsCrawler
from .arxiv_papers import ArxivPapersCrawler
from .juejin_rss import JuejinRSSCrawler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrawlerOrchestrator:
    """爬虫调度器"""

    def __init__(self, config_path='config/sources.yaml'):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.crawlers = self._init_crawlers()

    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {'sources': {}}

    def _init_crawlers(self) -> Dict[str, object]:
        """初始化爬虫实例"""
        crawlers = {}
        sources_config = self.config.get('sources', {})

        # GitHub Trending
        if sources_config.get('github_trending', {}).get('enabled', False):
            config = sources_config['github_trending']
            crawlers['github_trending'] = GitHubTrendingCrawler(
                period=config.get('period', 'daily'),
                language=config.get('language', 'all'),
                spoken_language=config.get('spoken_language_code', 'zh'),
                limit=config.get('limit', 10)
            )
            logger.info("Initialized GitHub Trending crawler")

        # Hacker News
        if sources_config.get('hacker_news', {}).get('enabled', False):
            config = sources_config['hacker_news']
            crawlers['hacker_news'] = HackerNewsCrawler(
                limit=config.get('limit', 5)
            )
            logger.info("Initialized Hacker News crawler")

        # ArXiv Papers
        if sources_config.get('arxiv_ai', {}).get('enabled', False):
            config = sources_config['arxiv_ai']
            crawlers['arxiv_ai'] = ArxivPapersCrawler(
                categories=config.get('categories', ['cs.AI', 'cs.LG']),
                limit=config.get('limit', 3),
                sort_by=config.get('sort_by', 'submittedDate')
            )
            logger.info("Initialized ArXiv Papers crawler")

        # Juejin RSS
        if sources_config.get('juejin', {}).get('enabled', False):
            config = sources_config['juejin']
            crawlers['juejin'] = JuejinRSSCrawler(
                tags=config.get('tags', []),
                limit=config.get('limit', 5)
            )
            logger.info("Initialized Juejin RSS crawler")

        return crawlers

    def crawl_all(self) -> Dict[str, List[Dict]]:
        """
        运行所有启用的爬虫

        Returns:
            Dict[str, List[Dict]]: 各爬虫获取的数据
        """
        results = {}

        for name, crawler in self.crawlers.items():
            try:
                logger.info(f"Running {name} crawler...")
                data = crawler.fetch()
                results[name] = data
                logger.info(f"{name} crawler completed: {len(data)} items")
            except Exception as e:
                logger.error(f"{name} crawler failed: {e}")
                results[name] = []

        return results

    def crawl_single(self, source_name: str) -> List[Dict]:
        """
        运行单个爬虫

        Args:
            source_name: 爬虫名称

        Returns:
            List[Dict]: 爬取的数据
        """
        if source_name not in self.crawlers:
            logger.error(f"Unknown crawler: {source_name}")
            return []

        try:
            logger.info(f"Running {source_name} crawler...")
            data = self.crawlers[source_name].fetch()
            logger.info(f"{source_name} crawler completed: {len(data)} items")
            return data
        except Exception as e:
            logger.error(f"{source_name} crawler failed: {e}")
            return []

    def get_all_data(self) -> List[Dict]:
        """
        获取所有爬取的数据，合并为统一格式

        Returns:
            List[Dict]: 所有数据
        """
        results = self.crawl_all()
        all_data = []

        for source, items in results.items():
            all_data.extend(items)

        return all_data


if __name__ == '__main__':
    orchestrator = CrawlerOrchestrator()
    results = orchestrator.crawl_all()

    print("\n=== Crawl Results ===")
    for source, items in results.items():
        print(f"\n{source}: {len(items)} items")
        for item in items[:2]:  # 只显示前2个
            print(f"  - {item.get('title', 'N/A')[:50]}...")
