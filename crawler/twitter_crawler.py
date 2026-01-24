"""
Twitter/X Scraper using Playwright
Twitter/X爬虫 - 使用Playwright模拟浏览器，不需要API
"""

import asyncio
import logging
from typing import List, Dict, Optional, TYPE_CHECKING, Any
from datetime import datetime, timedelta, timezone
import json

if TYPE_CHECKING:
    from playwright.async_api import Page

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterCrawler:
    """Twitter爬虫类"""

    def __init__(
        self,
        accounts: Optional[List[str]] = None,
        tweets_per_account: int = 10,
        headless: bool = True,
        timeout: int = 30000
    ):
        """
        初始化Twitter爬虫

        Args:
            accounts: 要爬取的Twitter账号列表（不包含@符号）
            tweets_per_account: 每个账号爬取的推文数量
            headless: 是否使用无头浏览器模式
            timeout: 超时时间（毫秒）
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright not installed. Install it with: pip install playwright && playwright install"
            )

        self.accounts = accounts or [
            "elonmusk",
            "sama",
            "ylecun",
            "AndrewYNg",
            "hardmaru",
            "fchollet",
            "karpathy"
        ]
        self.tweets_per_account = tweets_per_account
        self.headless = headless
        self.timeout = timeout
        self.base_url = "https://twitter.com"

    async def _scroll_to_load_tweets(self, page: Any, max_tweets: int):
        """滚动页面加载更多推文"""
        tweets_collected = 0

        while tweets_collected < max_tweets:
            previous_height = await page.evaluate("document.body.scrollHeight")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            await asyncio.sleep(2)

            new_height = await page.evaluate("document.body.scrollHeight")

            tweets = await page.query_selector_all('[data-testid="tweet"]')
            tweets_collected = len(tweets)

            logger.info(f"已加载 {tweets_collected} 条推文，目标 {max_tweets} 条")

            if new_height == previous_height:
                break

        return tweets_collected

    async def _extract_tweet_data(self, tweet_element) -> Dict:
        """从推文元素中提取数据"""
        try:
            tweet_data = {}

            tweet_text = await tweet_element.query_selector('[data-testid="tweetText"]')
            if tweet_text:
                tweet_data['text'] = await tweet_text.inner_text()

            time_element = await tweet_element.query_selector('time')
            if time_element:
                tweet_data['timestamp'] = await time_element.get_attribute('datetime')

            likes_element = await tweet_element.query_selector('[data-testid="like"]')
            if likes_element:
                likes_text = await likes_element.inner_text()
                tweet_data['likes'] = likes_text

            retweets_element = await tweet_element.query_selector('[data-testid="retweet"]')
            if retweets_element:
                retweets_text = await retweets_element.inner_text()
                tweet_data['retweets'] = retweets_text

            replies_element = await tweet_element.query_selector('[data-testid="reply"]')
            if replies_element:
                replies_text = await replies_element.inner_text()
                tweet_data['replies'] = replies_text

            tweet_data['scraped_at'] = datetime.now().isoformat()

            return tweet_data

        except Exception as e:
            logger.error(f"提取推文数据失败: {e}")
            return {}

    async def crawl_account(self, account: str) -> List[Dict]:
        """爬取单个账号的推文"""
        tweets = []

        try:
            logger.info(f"开始爬取账号: @{account}")

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                )
                page = await context.new_page()

                url = f"{self.base_url}/{account}"
                await page.goto(url, timeout=self.timeout)

                await asyncio.sleep(3)

                await self._scroll_to_load_tweets(page, self.tweets_per_account)

                tweet_elements = await page.query_selector_all('[data-testid="tweet"]')

                logger.info(f"找到 {len(tweet_elements)} 条推文")

                for i, tweet_element in enumerate(tweet_elements[:self.tweets_per_account]):
                    tweet_data = await self._extract_tweet_data(tweet_element)
                    if tweet_data:
                        tweet_data['account'] = account
                        tweet_data['account_url'] = url
                        tweets.append(tweet_data)
                        logger.info(f"提取第 {i+1} 条推文成功")

                await browser.close()

            logger.info(f"账号 @{account} 爬取完成，共 {len(tweets)} 条推文")

        except Exception as e:
            logger.error(f"爬取账号 @{account} 失败: {e}")

        return tweets

    async def crawl_all(self) -> Dict[str, List[Dict]]:
        """爬取所有配置的账号"""
        all_tweets = {}

        for account in self.accounts:
            tweets = await self.crawl_account(account)
            all_tweets[account] = tweets

        total_tweets = sum(len(tweets) for tweets in all_tweets.values())
        logger.info(f"所有账号爬取完成，共 {total_tweets} 条推文")

        return all_tweets

    def fetch(self) -> List[Dict]:
        """同步接口，便于集成到现有爬虫系统"""
        loop = asyncio.get_event_loop()
        all_tweets = loop.run_until_complete(self.crawl_all())

        flattened_tweets = []
        for account, tweets in all_tweets.items():
            flattened_tweets.extend(tweets)

        return flattened_tweets


class TwitterRecentCrawler(TwitterCrawler):
    """最近推文爬虫 - 只爬取最近30分钟内的推文"""

    def __init__(self, accounts: Optional[List[str]] = None, headless: bool = True):
        super().__init__(accounts=accounts, tweets_per_account=50, headless=headless)

    async def crawl_account(self, account: str) -> List[Dict]:
        """爬取单个账号的最近推文"""
        all_tweets = await super().crawl_account(account)

        thirty_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=30)
        recent_tweets = []

        for tweet in all_tweets:
            try:
                if 'timestamp' in tweet:
                    timestamp_str = tweet['timestamp']
                    if timestamp_str.endswith('Z'):
                        timestamp_str = timestamp_str[:-1] + '+00:00'
                    tweet_time = datetime.fromisoformat(timestamp_str)
                    if tweet_time.tzinfo is None:
                        tweet_time = tweet_time.replace(tzinfo=timezone.utc)
                    if tweet_time > thirty_minutes_ago:
                        recent_tweets.append(tweet)
            except Exception as e:
                logger.warning(f"解析推文时间失败: {e}")

        logger.info(f"账号 @{account} 最近30分钟内有 {len(recent_tweets)} 条新推文")

        return recent_tweets
