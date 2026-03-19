"""
Crawler module for AI Stack Blog System
爬虫模块 - 从多个来源抓取内容
"""

from importlib import import_module


__all__ = [
    "GitHubTrendingCrawler",
    "HackerNewsCrawler",
    "ArxivPapersCrawler",
    "JuejinRSSCrawler",
    "BlogsPodcastsCrawler",
    "RedditCrawler",
    "CrawlerOrchestrator",
]


_EXPORTS = {
    "GitHubTrendingCrawler": ("crawler.github_trending", "GitHubTrendingCrawler"),
    "HackerNewsCrawler": ("crawler.hacker_news", "HackerNewsCrawler"),
    "ArxivPapersCrawler": ("crawler.arxiv_papers", "ArxivPapersCrawler"),
    "JuejinRSSCrawler": ("crawler.juejin_rss", "JuejinRSSCrawler"),
    "BlogsPodcastsCrawler": ("crawler.blogs_podcasts", "BlogsPodcastsCrawler"),
    "RedditCrawler": ("crawler.reddit", "RedditCrawler"),
    "CrawlerOrchestrator": ("crawler.main", "CrawlerOrchestrator"),
}


def __getattr__(name: str):
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(name)
    module_name, attr_name = target
    module = import_module(module_name)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
