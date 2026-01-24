"""
Twitter publisher
Twitter/X 推送模块
"""

import os
import tweepy
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterPublisher:
    """Twitter 推送器"""

    def __init__(self, api_key=None, api_secret=None, access_token=None,
                 access_token_secret=None, bearer_token=None):
        self.api_key = api_key or os.environ.get('TWITTER_API_KEY')
        self.api_secret = api_secret or os.environ.get('TWITTER_API_SECRET')
        self.access_token = access_token or os.environ.get('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = access_token_secret or os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = bearer_token or os.environ.get('TWITTER_BEARER_TOKEN')

        self.client = self._init_client()

    def _init_client(self):
        """初始化 Twitter 客户端"""
        try:
            if not self.bearer_token:
                logger.warning("Twitter bearer token not configured")
                return None

            # 使用 API v2
            client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            logger.info("Twitter client initialized")
            return client

        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
            return None

    def tweet(self, text: str) -> bool:
        """
        发布推文

        Args:
            text: 推文内容

        Returns:
            bool: 是否成功
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return False

        try:
            response = self.client.create_tweet(text=text)
            logger.info(f"Tweet posted successfully: {response.data['id']}")
            return True

        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return False

    def tweet_with_media(self, text: str, media_paths: List[str]) -> bool:
        """
        发布带媒体的推文

        Args:
            text: 推文内容
            media_paths: 媒体文件路径列表

        Returns:
            bool: 是否成功
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return False

        try:
            # 上传媒体
            media_ids = []
            for media_path in media_paths:
                media = self.client.media_upload(filename=media_path)
                media_ids.append(media.media_id)

            # 发布推文
            response = self.client.create_tweet(text=text, media_ids=media_ids)
            logger.info(f"Tweet with media posted successfully: {response.data['id']}")
            return True

        except Exception as e:
            logger.error(f"Failed to post tweet with media: {e}")
            return False

    def format_tweet(self, content: Dict, max_length=280) -> str:
        """
        格式化内容为推文

        Args:
            content: 内容数据
            max_length: 最大长度

        Returns:
            str: 格式化后的推文
        """
        title = content.get('title', '')
        summary = content.get('summary', '')
        url = content.get('url', '')

        # 构建推文
        tweet_parts = []

        if title:
            tweet_parts.append(title)

        if summary:
            tweet_parts.append(f"{summary[:100]}...")

        if url:
            tweet_parts.append(url)

        tweet = '\n'.join(tweet_parts)

        # 添加标签
        tags = content.get('tags', [])
        if tags:
            hashtags = ' '.join([f"#{tag}" for tag in tags[:3]])
            tweet = f"{tweet}\n\n{hashtags}"

        # 截断
        if len(tweet) > max_length:
            tweet = tweet[:max_length-3] + '...'

        return tweet

    def publish_content(self, content: Dict) -> bool:
        """
        推送内容到 Twitter

        Args:
            content: 内容数据

        Returns:
            bool: 是否成功
        """
        try:
            tweet_text = self.format_tweet(content)
            return self.tweet(tweet_text)

        except Exception as e:
            logger.error(f"Failed to publish content to Twitter: {e}")
            return False


if __name__ == '__main__':
    # 测试 Twitter 推送
    publisher = TwitterPublisher()

    test_content = {
        'title': 'GitHub Trending: awesome-project',
        'summary': 'A powerful tool for developers',
        'url': 'https://github.com/user/awesome-project',
        'tags': ['github', 'trending', 'AI']
    }

    success = publisher.publish_content(test_content)
    print(f"Publish result: {success}")
