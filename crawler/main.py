"""
Crawler orchestrator
爬虫调度器 - 统一管理所有爬虫
"""

import yaml
import logging
import time
from typing import List, Dict
from pathlib import Path

from crawler.github_trending import GitHubTrendingCrawler
from crawler.hacker_news import HackerNewsCrawler
from crawler.arxiv_papers import ArxivPapersCrawler
from crawler.juejin_rss import JuejinRSSCrawler
from crawler.blogs_podcasts import BlogsPodcastsCrawler
from crawler.reddit import RedditCrawler
from crawler.twitter_crawler import TwitterRecentCrawler
from crawler.dedupe import canonicalize_url
from runtime_profile import apply_sources_runtime_profile, get_runtime_profile
from ai_stack.source_contract import SourceContractError, apply_source_contract

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrawlerOrchestrator:
    """爬虫调度器"""

    def __init__(
        self,
        config_path='config/sources.yaml',
        dedupe: bool = True,
        dedupe_scope: str = "global",
        runtime_profile: str | None = None,
    ):
        self.config_path = Path(config_path)
        self.runtime_profile = get_runtime_profile(runtime_profile)
        self.config = self._load_config()
        self.dedupe = dedupe
        self.dedupe_scope = dedupe_scope  # global | per_source
        # Every valid capture is retained for lineage, even when URL dedupe keeps
        # only one winner for the expensive generation path.
        self.last_observations: List[Dict] = []
        self.crawlers = self._init_crawlers()

    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {'sources': {}}
                return apply_sources_runtime_profile(config, self.runtime_profile)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {'sources': {}}

    def _init_crawlers(self) -> Dict[str, object]:
        """初始化爬虫实例"""
        crawlers = {}
        sources_config = self.config.get('sources', {})
        search_fallback_config = self.config.get('search_fallback', {})

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
                rss_url=config.get('rss_url'),
                tags=config.get('tags', []),
                limit=config.get('limit', 5),
                search_fallback=search_fallback_config,
            )
            logger.info("Initialized Juejin RSS crawler")

        # Blogs & Podcasts (RSS/Atom)
        if sources_config.get('blogs_podcasts', {}).get('enabled', False):
            config = sources_config['blogs_podcasts']
            crawlers['blogs_podcasts'] = BlogsPodcastsCrawler(
                feeds=config.get('feeds'),
                limit=config.get('limit', 10),
                timeout=config.get('timeout', 30),
                search_fallback=search_fallback_config,
            )
            logger.info("Initialized Blogs/Podcasts crawler")

        # Reddit (subreddits)
        if sources_config.get('reddit', {}).get('enabled', False):
            config = sources_config['reddit']
            crawlers['reddit'] = RedditCrawler(
                subreddits=config.get('subreddits'),
                limit_per_subreddit=config.get('limit_per_subreddit', 10),
                sort=config.get('sort', 'hot'),
                include_selftext=config.get('include_selftext', True),
                timeout=config.get('timeout', 15),
                search_fallback=search_fallback_config,
            )
            logger.info("Initialized Reddit crawler")

        # Twitter/X (Recent tweets from tech leaders)
        if sources_config.get('twitter', {}).get('enabled', False):
            config = sources_config['twitter']
            crawlers['twitter'] = TwitterRecentCrawler(
                accounts=config.get('accounts'),
                headless=config.get('headless', True),
                tweets_per_account=config.get('tweets_per_account', 30),
                lookback_minutes=config.get('lookback_minutes', 90),
                timeout=config.get('timeout', 30000),
                save_screenshots=config.get('save_screenshots', True),
                account_profiles=config.get('account_profiles'),
            )
            logger.info("Initialized Twitter/X crawler")

        return crawlers

    def _dedupe_results(self, results: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """对爬取结果去重（默认跨数据源去重）。"""
        contracted: Dict[str, List[Dict]] = {str(source): [] for source in results}
        for source, items in results.items():
            for item in items:
                try:
                    contracted[str(source)].append(apply_source_contract(item))
                except (SourceContractError, TypeError, ValueError) as exc:
                    logger.warning("Rejected invalid %s source record: %s", source, exc)
        results = contracted
        self.last_observations = sorted(
            (item for items in results.values() for item in items),
            key=lambda item: (
                str(item.get("url") or ""),
                str(item.get("source") or ""),
                str(item.get("source_snapshot_sha256") or ""),
            ),
        )
        if not self.dedupe:
            return results

        strength = {
            "abstract": 4,
            "excerpt": 4,
            "social_post": 3,
            "metadata_only": 1,
        }

        def evidence_key(item: Dict) -> tuple:
            return (
                -strength.get(str(item.get("source_capture_mode") or ""), 0),
                item.get("source_is_truncated") is True,
                -int(item.get("source_text_chars") or 0),
                str(item.get("source") or ""),
                str(item.get("source_snapshot_sha256") or ""),
            )

        def strongest(items: List[Dict]) -> List[Dict]:
            by_url: Dict[str, List[Dict]] = {}
            for item in items:
                url = canonicalize_url(item.get("url", "") or "")
                item["url"] = url
                by_url.setdefault(url, []).append(item)
            winner_ids = {
                id(sorted(candidates, key=evidence_key)[0])
                for candidates in by_url.values()
            }
            return [item for item in items if id(item) in winner_ids]

        deduped: Dict[str, List[Dict]] = {source: [] for source in results}

        if self.dedupe_scope == "per_source":
            for source, items in results.items():
                unique = strongest(items)
                removed = len(items) - len(unique)
                if removed:
                    logger.info(f"Dedupe(per_source) removed {removed} items from {source}")
                deduped[source] = unique
            return deduped

        all_items = [item for items in results.values() for item in items]
        winners = strongest(all_items)
        for item in winners:
            deduped.setdefault(str(item.get("source") or ""), []).append(item)
        removed_total = len(all_items) - len(winners)
        if removed_total:
            logger.info(
                "Dedupe(global) removed %s weaker duplicate source records",
                removed_total,
            )
        return deduped

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

        return self._dedupe_results(results)

    def crawl_for_duration(self, duration_hours: float, interval_minutes: int = 30) -> Dict[str, List[Dict]]:
        """
        在指定时长内反复抓取（适合长时间运行的去重聚合）。
        默认最终仍按各爬虫的 limit 截断，以避免输出无限膨胀。
        """
        if duration_hours <= 0:
            return self.crawl_all()

        end_ts = time.time() + duration_hours * 3600
        logger.info(f"Starting long crawl: {duration_hours}h, interval {interval_minutes}m")

        aggregated: Dict[str, Dict[str, Dict]] = {name: {} for name in self.crawlers.keys()}
        seen_global: set[str] = set()

        round_idx = 0
        while True:
            now = time.time()
            if now >= end_ts:
                break

            round_idx += 1
            logger.info(f"[Long crawl] Round {round_idx} ...")

            batch = {}
            for name, crawler in self.crawlers.items():
                try:
                    batch[name] = crawler.fetch()
                except Exception as e:
                    logger.error(f"{name} crawler failed: {e}")
                    batch[name] = []

            # incremental dedupe across the whole run
            for source, items in batch.items():
                for item in items:
                    url = canonicalize_url(item.get("url", "") or "")
                    if url:
                        item["url"] = url
                    key = url or f"{source}:{item.get('title','')}".strip()
                    if self.dedupe and self.dedupe_scope == "global":
                        if url and url in seen_global:
                            continue
                        if url:
                            seen_global.add(url)
                    elif self.dedupe and self.dedupe_scope == "per_source":
                        pass  # handled by per-source dict below

                    if key in aggregated[source]:
                        continue
                    aggregated[source][key] = item

            sleep_seconds = max(0, int(end_ts - time.time()))
            if sleep_seconds <= 0:
                break
            time.sleep(min(interval_minutes * 60, sleep_seconds))

        # finalize: convert to list and truncate per crawler.limit
        finalized: Dict[str, List[Dict]] = {}
        for source, items_map in aggregated.items():
            items_list = list(items_map.values())

            # prefer newest first when available
            def _sort_key(it: Dict) -> str:
                return (
                    it.get("published_at")
                    or it.get("published")
                    or str(it.get("time") or "")
                    or it.get("crawled_at")
                    or ""
                )

            items_list.sort(key=_sort_key, reverse=True)

            limit = getattr(self.crawlers.get(source), "limit", None)
            if isinstance(limit, int) and limit > 0:
                items_list = items_list[:limit]
            finalized[source] = items_list

        return self._dedupe_results(finalized)

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
            return [apply_source_contract(item) for item in data]
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
