#!/usr/bin/env python3

import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import patch

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - local fallback for bare Python
    requests = types.ModuleType("requests")

    class _HTTPError(Exception):
        pass

    class _DummySession:
        def get(self, *args, **kwargs):
            raise NotImplementedError

    requests.HTTPError = _HTTPError
    requests.Session = _DummySession
    requests.get = lambda *args, **kwargs: None
    sys.modules["requests"] = requests

try:
    __import__("feedparser")
except ModuleNotFoundError:  # pragma: no cover - local fallback for bare Python
    fake_feedparser = types.ModuleType("feedparser")
    fake_feedparser.parse = lambda *args, **kwargs: SimpleNamespace(bozo=0, entries=[])
    sys.modules["feedparser"] = fake_feedparser

try:
    __import__("bs4")
except ModuleNotFoundError:  # pragma: no cover - local fallback for bare Python
    fake_bs4 = types.ModuleType("bs4")

    class _BeautifulSoup:
        def __init__(self, text, parser):
            self.text = text

        def get_text(self, sep=" ", strip=True):
            return self.text

    fake_bs4.BeautifulSoup = _BeautifulSoup
    sys.modules["bs4"] = fake_bs4

from crawler.juejin_rss import JuejinRSSCrawler
from crawler.reddit import RedditCrawler
from crawler.search_fallback import (
    MultilingualQueryPlanner,
    PlannedQuery,
    SearchFallbackService,
    SearXNGSearchClient,
)


class _FakeResponse:
    def __init__(self, payload=None, text=""):
        self._payload = payload or {}
        self.text = text
        self.content = text.encode("utf-8")

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class _FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls.append(
            {
                "url": url,
                "params": params or {},
                "headers": headers or {},
                "timeout": timeout,
            }
        )
        if not self.responses:
            raise AssertionError("No more fake responses configured")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class _FakeFallbackService:
    def __init__(self, reddit_items=None, juejin_items=None):
        self.reddit_items = reddit_items or []
        self.juejin_items = juejin_items or []
        self.calls = []

    def search_reddit_subreddit(self, **kwargs):
        self.calls.append(("reddit", kwargs))
        return list(self.reddit_items)

    def search_juejin_articles(self, **kwargs):
        self.calls.append(("juejin", kwargs))
        return list(self.juejin_items)


class SearchFallbackTest(unittest.TestCase):
    def test_query_planner_generates_multilingual_site_queries(self):
        planner = MultilingualQueryPlanner(max_queries_per_target=2)

        plans = planner.plan_site_queries(
            site="juejin.cn/post",
            topics=["人工智能", "LLM"],
            target="掘金",
        )

        self.assertGreaterEqual(len(plans), 4)
        self.assertIn("zh-CN", {plan.language for plan in plans})
        self.assertIn("en-US", {plan.language for plan in plans})
        self.assertTrue(all(plan.query.startswith("site:juejin.cn/post") for plan in plans))
        self.assertTrue(any("人工智能" in plan.query for plan in plans))
        self.assertTrue(any("LLM" in plan.query for plan in plans))

    def test_searxng_client_normalizes_results(self):
        session = _FakeSession(
            [
                _FakeResponse(
                    payload={
                        "results": [
                            {
                                "title": "LLM roundup",
                                "url": "https://juejin.cn/post/123",
                                "content": "Latest AI tooling",
                                "publishedDate": "2026-03-20T00:00:00Z",
                            }
                        ]
                    }
                )
            ]
        )
        client = SearXNGSearchClient(
            base_urls=["https://example-searx.local/search"],
            timeout=7,
            per_query_limit=3,
            session=session,
        )

        results = client.search_many(
            [PlannedQuery(query="site:juejin.cn/post LLM", language="en-US")],
            max_total=2,
            time_range="month",
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "LLM roundup")
        self.assertEqual(results[0]["url"], "https://juejin.cn/post/123")
        self.assertEqual(results[0]["search_language"], "en-US")
        self.assertEqual(session.calls[0]["params"]["format"], "json")
        self.assertEqual(session.calls[0]["params"]["time_range"], "month")

    def test_search_service_maps_reddit_results(self):
        session = _FakeSession(
            [
                _FakeResponse(
                    payload={
                        "results": [
                            {
                                "title": "New model release",
                                "url": "https://www.reddit.com/r/LocalLLaMA/comments/abc123/new_model_release/",
                                "content": "Weights and benchmarks",
                            }
                        ]
                    }
                )
            ]
        )
        service = SearchFallbackService(
            {
                "enabled": True,
                "instances": ["https://example-searx.local/search"],
                "query_languages": ["en-US"],
                "default_topics": ["LLM"],
                "max_queries_per_target": 1,
            },
            session=session,
        )

        items = service.search_reddit_subreddit("LocalLLaMA", limit=1, topics=["LLM"])

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["source"], "reddit")
        self.assertEqual(items[0]["subreddit"], "LocalLLaMA")
        self.assertEqual(items[0]["discovery_method"], "search_fallback")

    @patch.object(RedditCrawler, "_fetch_listing", side_effect=requests.HTTPError("403 blocked"))
    def test_reddit_fetch_uses_search_fallback_when_blocked(self, _mock_fetch):
        crawler = RedditCrawler(
            subreddits=["MachineLearning"],
            limit_per_subreddit=2,
            search_fallback={"enabled": True},
        )
        crawler.search_fallback_service = _FakeFallbackService(
            reddit_items=[
                {
                    "title": "Fallback reddit item",
                    "url": "https://www.reddit.com/r/MachineLearning/comments/test/fallback/",
                    "description": "Recovered by search",
                    "subreddit": "MachineLearning",
                    "source": "reddit",
                    "discovery_method": "search_fallback",
                }
            ]
        )

        items = crawler.fetch()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Fallback reddit item")
        self.assertEqual(crawler.search_fallback_service.calls[0][0], "reddit")

    @patch("crawler.juejin_rss.feedparser.parse", return_value=SimpleNamespace(bozo=0, entries=[]))
    @patch("crawler.juejin_rss.requests.get", return_value=_FakeResponse(text="<rss />"))
    def test_juejin_fetch_uses_search_fallback_when_feed_empty(self, _mock_get, _mock_parse):
        crawler = JuejinRSSCrawler(
            rss_url="https://juejin.cn/rss",
            tags=["人工智能", "大模型"],
            limit=2,
            search_fallback={"enabled": True},
        )
        crawler.search_fallback_service = _FakeFallbackService(
            juejin_items=[
                {
                    "title": "Fallback juejin item",
                    "url": "https://juejin.cn/post/123456",
                    "description": "Recovered by search",
                    "source": "juejin",
                    "discovery_method": "search_fallback",
                }
            ]
        )

        items = crawler.fetch()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Fallback juejin item")
        self.assertEqual(crawler.search_fallback_service.calls[0][0], "juejin")


if __name__ == "__main__":
    unittest.main()
