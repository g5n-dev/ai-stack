"""
Twitter/X Scraper using Playwright
Twitter/X爬虫 - 使用Playwright模拟浏览器，不需要API
"""

import asyncio
import hashlib
import logging
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ai_stack.reset_signals import classify_reset_signal, signal_title_prefix
from ai_stack.twitter_fallback import (
    download_fallback_payload,
    parse_fallback_feed,
    validated_fallback_url,
)

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
        timeout: int = 30000,
        save_screenshots: bool = True,
        screenshots_dir: Optional[str] = None,
        account_profiles: Optional[Dict[str, Dict[str, Any]]] = None,
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
                "Playwright not installed. Install it with: "
                "pip install playwright && playwright install"
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
        self.save_screenshots = save_screenshots
        raw_profiles = account_profiles if isinstance(account_profiles, dict) else {}
        self.account_profiles = {
            str(handle).strip().casefold(): dict(profile)
            for handle, profile in raw_profiles.items()
            if str(handle).strip() and isinstance(profile, dict)
        }

        project_root = Path(__file__).resolve().parents[1]
        default_dir = project_root / "blog" / "static" / "images" / "twitter"
        self.screenshots_dir = Path(screenshots_dir) if screenshots_dir else default_dir
        if self.save_screenshots:
            self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    def _account_profile(self, account: str) -> Dict[str, Any]:
        profile = self.account_profiles.get(str(account or "").strip().casefold(), {})
        return dict(profile) if isinstance(profile, dict) else {}

    def _account_crawl_url(self, account: str) -> str:
        profile = self._account_profile(account)
        suffix = "/with_replies" if profile.get("include_replies") is True else ""
        return f"{self.base_url}/{account}{suffix}"

    @staticmethod
    def _validated_fallback_url(value: object) -> str:
        return validated_fallback_url(value)

    @classmethod
    def _download_fallback_payload(cls, feed_url: str, timeout_seconds: float) -> Dict:
        return download_fallback_payload(feed_url, timeout_seconds)

    def _fallback_items_from_payload(
        self,
        payload: object,
        *,
        account: str,
        feed_url: str,
        now: Optional[datetime] = None,
        max_age_minutes: int = 90,
    ) -> List[Dict]:
        items = parse_fallback_feed(
            payload,
            account=account,
            feed_url=feed_url,
            now=now,
            max_age_minutes=max_age_minutes,
        )
        return [self._enrich_monitored_tweet(item, account=account) for item in items]

    async def _crawl_account_fallback(self, account: str) -> List[Dict]:
        profile = self._account_profile(account)
        feed_url = self._validated_fallback_url(profile.get("fallback_feed_url"))
        if not feed_url:
            return []
        try:
            max_age_minutes = max(1, int(profile.get("fallback_max_age_minutes", 90)))
        except (TypeError, ValueError):
            return []
        timeout_seconds = max(1.0, min(float(self.timeout) / 1000.0, 15.0))
        payload = await asyncio.to_thread(
            self._download_fallback_payload,
            feed_url,
            timeout_seconds,
        )
        items = self._fallback_items_from_payload(
            payload,
            account=account,
            feed_url=feed_url,
            max_age_minutes=max_age_minutes,
        )
        return self._prioritize_monitored_tweets(items, account=account)[
            : self.tweets_per_account
        ]

    def _enrich_monitored_tweet(self, tweet: Dict, *, account: str) -> Dict:
        enriched = dict(tweet)
        profile = self._account_profile(account)
        if profile.get("monitor") != "codex_usage_reset":
            return enriched

        assessment = dict(
            classify_reset_signal(
                enriched.get("text", ""),
                context=enriched.get("context_text")
                or enriched.get("quoted_text")
                or "",
            )
        )
        mirrored = enriched.get("discovery_method") == "structured_fallback"
        if mirrored:
            assessment["source_verification"] = "independent_mirror"
            if assessment.get("status") in {"confirmed", "promised"}:
                assessment["reported_status"] = assessment["status"]
                assessment["status"] = "watch"
                assessment["notify"] = False
                assessment["confidence"] = min(
                    float(assessment.get("confidence") or 0.0),
                    0.7,
                )
                verification_status = str(
                    enriched.get("reset_verification_status") or ""
                )
                assessment["reason"] = (
                    f"独立社区镜像报告该信号（外部核验状态："
                    f"{verification_status or 'unknown'}），尚未由 X 直接核验"
                )
        enriched["signal_assessment"] = assessment
        enriched["monitor"] = "codex_usage_reset"

        tags: List[str] = []
        raw_tags = enriched.get("tags")
        if isinstance(raw_tags, list):
            tags.extend(str(tag).strip() for tag in raw_tags if str(tag).strip())
        profile_tags = profile.get("tags")
        if (
            assessment.get("status") != "insufficient_evidence"
            and isinstance(profile_tags, list)
        ):
            tags.extend(str(tag).strip() for tag in profile_tags if str(tag).strip())
        state_tags = {
            ("hard_reset", "confirmed"): "重置确认",
            ("hard_reset", "promised"): "重置预告",
            ("hard_reset", "watch"): "重置观察",
            ("hard_reset", "negated"): "重置否定",
            ("banked_reset", "confirmed"): "重置卡",
            ("banked_reset", "promised"): "重置卡预告",
            ("temp_boost", "confirmed"): "临时额度提升",
            ("policy_change", "confirmed"): "额度政策",
            ("forecast_signal", "watch"): "重置观察",
        }
        state_tag = state_tags.get(
            (str(assessment.get("kind") or ""), str(assessment.get("status") or ""))
        )
        if state_tag:
            tags.append(state_tag)
        enriched["tags"] = list(dict.fromkeys(tags))

        prefix = signal_title_prefix(assessment)
        if mirrored and assessment.get("status") != "insufficient_evidence":
            prefix = "[独立镜像待核验]"
        title = str(enriched.get("title") or "").strip()
        if prefix and not title.startswith(prefix):
            enriched["source_title_unclassified"] = title
            enriched["title"] = f"{prefix} {title}".strip()
        return enriched

    def _prioritize_monitored_tweets(
        self,
        tweets: List[Dict],
        *,
        account: str,
    ) -> List[Dict]:
        if self._account_profile(account).get("monitor") != "codex_usage_reset":
            return list(tweets)

        tier_map = {
            ("hard_reset", "confirmed"): 0,
            ("hard_reset", "promised"): 0,
            ("hard_reset", "negated"): 0,
            ("banked_reset", "confirmed"): 1,
            ("banked_reset", "promised"): 1,
            ("temp_boost", "confirmed"): 1,
            ("policy_change", "confirmed"): 1,
            ("forecast_signal", "watch"): 2,
            ("hard_reset", "watch"): 2,
        }

        def key(item: Dict) -> tuple[int, float, str]:
            raw_signal = item.get("signal_assessment")
            signal = raw_signal if isinstance(raw_signal, dict) else {}
            status = str(signal.get("reported_status") or signal.get("status") or "")
            tier = tier_map.get((str(signal.get("kind") or ""), status), 3)
            timestamp = str(item.get("timestamp") or "")
            try:
                parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                epoch = parsed.timestamp() if parsed.tzinfo is not None else 0.0
            except (TypeError, ValueError, OverflowError):
                epoch = 0.0
            stable_id = str(item.get("tweet_id") or item.get("url") or "")
            return tier, -epoch, stable_id

        return sorted(tweets, key=key)

    @staticmethod
    def _merge_tweet_sources(
        primary: List[Dict],
        secondary: List[Dict],
    ) -> List[Dict]:
        """Merge account feeds while preferring direct X records on duplicates."""

        merged: List[Dict] = []
        seen: set[str] = set()
        for item in [*primary, *secondary]:
            identity = str(item.get("tweet_id") or item.get("url") or "").strip()
            if identity and identity in seen:
                continue
            if identity:
                seen.add(identity)
            merged.append(item)
        return merged

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

    def _build_screenshot_filename(
        self,
        account: str,
        tweet_url: str,
        tweet_timestamp: str,
        tweet_text: str,
    ) -> str:
        tweet_id = ""
        if tweet_url:
            m = re.search(r"/status/(\d+)", tweet_url)
            if m:
                tweet_id = m.group(1)

        if tweet_id:
            return f"{account}-{tweet_id}.png"

        key = f"{account}|{tweet_timestamp}|{tweet_text}".encode("utf-8", errors="ignore")
        digest = hashlib.sha256(key).hexdigest()[:16]
        ts = (tweet_timestamp or "unknown").replace(":", "-").replace("/", "-")
        ts = ts.replace("T", "_").replace("Z", "")
        ts = re.sub(r"[^0-9A-Za-z_+.-]+", "-", ts).strip("-")[:40] or "unknown"
        return f"{account}-{ts}-{digest}.png"

    async def _capture_tweet_screenshot(
        self,
        tweet_element,
        *,
        account: str,
        tweet_url: str,
        tweet_timestamp: str,
        tweet_text: str,
    ) -> Optional[str]:
        if not self.save_screenshots:
            return None

        filename = self._build_screenshot_filename(account, tweet_url, tweet_timestamp, tweet_text)
        file_path = self.screenshots_dir / filename

        for attempt in range(3):
            try:
                await tweet_element.scroll_into_view_if_needed()
                await asyncio.sleep(0.2)
                await tweet_element.screenshot(path=str(file_path))
                return f"/images/twitter/{filename}"
            except Exception as e:
                msg = str(e)
                if ("not attached to the DOM" in msg) or ("Element is not attached" in msg):
                    logger.info("推文截图跳过：元素已从 DOM 移除")
                    return None
                if attempt < 2:
                    await asyncio.sleep(0.35)
                    continue
                logger.info(f"推文截图失败（已跳过）: {e}")
                return None

    async def _extract_tweet_data(self, tweet_element, *, account: str) -> Dict:
        """从推文元素中提取数据"""
        try:
            tweet_data = {}

            tweet_text = await tweet_element.query_selector('[data-testid="tweetText"]')
            if tweet_text:
                tweet_data['text'] = await tweet_text.inner_text()
                tweet_data['title'] = tweet_data['text'].replace('\n', ' ')[:80]

            time_element = await tweet_element.query_selector('time')
            if time_element:
                tweet_data['timestamp'] = await time_element.get_attribute('datetime')
                tweet_url = await time_element.evaluate("el => el.closest('a')?.href || ''")
                if tweet_url:
                    tweet_data['url'] = tweet_url

            tweet_url = tweet_data.get("url", "")
            tweet_timestamp = tweet_data.get("timestamp", "")
            tweet_text_value = tweet_data.get("text", "")
            tweet_id = ""
            if tweet_url:
                m = re.search(r"/status/(\d+)", tweet_url)
                if m:
                    tweet_id = m.group(1)
            if tweet_id:
                tweet_data["tweet_id"] = tweet_id

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

            screenshot_rel = await self._capture_tweet_screenshot(
                tweet_element,
                account=account,
                tweet_url=tweet_url,
                tweet_timestamp=tweet_timestamp,
                tweet_text=tweet_text_value,
            )
            if screenshot_rel:
                tweet_data["screenshot"] = screenshot_rel

            tweet_data['scraped_at'] = datetime.now(timezone.utc).isoformat()

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

                url = self._account_crawl_url(account)
                await page.goto(url, timeout=self.timeout)

                await asyncio.sleep(3)

                await self._scroll_to_load_tweets(page, self.tweets_per_account)

                tweet_elements = await page.query_selector_all('[data-testid="tweet"]')

                logger.info(f"找到 {len(tweet_elements)} 条推文")

                for i, tweet_element in enumerate(tweet_elements[:self.tweets_per_account]):
                    tweet_data = await self._extract_tweet_data(tweet_element, account=account)
                    if tweet_data:
                        tweet_data = self._enrich_monitored_tweet(tweet_data, account=account)
                        tweet_data['account'] = account
                        tweet_data['account_url'] = f"{self.base_url}/{account}"
                        tweet_data['source'] = 'twitter'
                        tweets.append(tweet_data)
                        logger.info(f"提取第 {i+1} 条推文成功")

                await browser.close()

            tweets = self._prioritize_monitored_tweets(tweets, account=account)
            logger.info(f"账号 @{account} 爬取完成，共 {len(tweets)} 条推文")

        except Exception as e:
            logger.error(f"爬取账号 @{account} 失败: {e}")

        if not tweets:
            fallback_tweets = await self._crawl_account_fallback(account)
            if fallback_tweets:
                logger.info(
                    "账号 @%s 使用结构化回退源，共 %s 条",
                    account,
                    len(fallback_tweets),
                )
                tweets = fallback_tweets

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
        try:
            all_tweets = asyncio.run(self.crawl_all())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                all_tweets = loop.run_until_complete(self.crawl_all())
            finally:
                try:
                    loop.close()
                except Exception:
                    pass

        flattened_tweets = []
        for _account, tweets in all_tweets.items():
            flattened_tweets.extend(tweets)

        return flattened_tweets


class TwitterRecentCrawler(TwitterCrawler):
    """最近推文爬虫 - 只爬取最近一段时间内的推文"""

    def __init__(
        self,
        accounts: Optional[List[str]] = None,
        *,
        headless: bool = True,
        tweets_per_account: int = 30,
        lookback_minutes: int = 90,
        timeout: int = 30000,
        save_screenshots: bool = True,
        screenshots_dir: Optional[str] = None,
        account_profiles: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        super().__init__(
            accounts=accounts,
            tweets_per_account=tweets_per_account,
            headless=headless,
            timeout=timeout,
            save_screenshots=save_screenshots,
            screenshots_dir=screenshots_dir,
            account_profiles=account_profiles,
        )
        self.lookback_minutes = max(1, int(lookback_minutes))

    def _account_lookback_minutes(self, account: str) -> int:
        raw = self._account_profile(account).get(
            "lookback_minutes",
            self.lookback_minutes,
        )
        try:
            return max(1, min(int(raw), 24 * 60))
        except (TypeError, ValueError):
            return self.lookback_minutes

    def _filter_recent(
        self,
        tweets: List[Dict],
        *,
        account: str,
        now: Optional[datetime] = None,
    ) -> List[Dict]:
        observed_now = now or datetime.now(timezone.utc)
        threshold = observed_now - timedelta(
            minutes=self._account_lookback_minutes(account)
        )
        recent_tweets = []

        for tweet in tweets:
            try:
                if 'timestamp' in tweet:
                    timestamp_str = tweet['timestamp']
                    if timestamp_str.endswith('Z'):
                        timestamp_str = timestamp_str[:-1] + '+00:00'
                    tweet_time = datetime.fromisoformat(timestamp_str)
                    if tweet_time.tzinfo is None:
                        continue
                    tweet_time = tweet_time.astimezone(timezone.utc)
                    if threshold <= tweet_time <= observed_now + timedelta(minutes=5):
                        recent_tweets.append(tweet)
            except Exception as e:
                logger.warning(f"解析推文时间失败: {e}")

        return recent_tweets

    async def crawl_account(self, account: str) -> List[Dict]:
        """爬取单个账号的最近推文"""
        all_tweets = await super().crawl_account(account)
        observed_now = datetime.now(timezone.utc)
        came_from_fallback = any(
            isinstance(tweet, dict)
            and tweet.get("discovery_method") == "structured_fallback"
            for tweet in all_tweets
        )
        fallback_attempted = came_from_fallback
        monitored = self._account_profile(account).get("monitor") == (
            "codex_usage_reset"
        )
        if monitored and all_tweets and not came_from_fallback:
            fallback_tweets = await self._crawl_account_fallback(account)
            fallback_attempted = True
            all_tweets = self._merge_tweet_sources(all_tweets, fallback_tweets)

        recent_tweets = self._filter_recent(
            all_tweets,
            account=account,
            now=observed_now,
        )
        if not recent_tweets and all_tweets and not fallback_attempted:
            fallback_tweets = await self._crawl_account_fallback(account)
            recent_tweets = self._filter_recent(
                self._merge_tweet_sources(all_tweets, fallback_tweets),
                account=account,
                now=observed_now,
            )

        recent_tweets = self._prioritize_monitored_tweets(
            recent_tweets,
            account=account,
        )
        lookback = self._account_lookback_minutes(account)
        logger.info(
            f"账号 @{account} 最近{lookback}分钟内有 {len(recent_tweets)} 条新推文"
        )

        return recent_tweets[: self.tweets_per_account]
