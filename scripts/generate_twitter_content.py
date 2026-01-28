#!/usr/bin/env python3
"""
Twitter Content Generation Script
Twitter内容生成脚本 - 抓取科技大佬推文，使用Claude分析并生成博客文章
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import logging
import argparse

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from processor.twitter_analyzer import TwitterPostGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TwitterContentGenerator:
    """Twitter内容生成器"""

    def __init__(self, api_key: str = None, base_url: str = None, headless: bool = True):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.base_url = base_url or os.environ.get('ANTHROPIC_BASE_URL')
        self.headless = headless
        self.posts_dir = project_root / 'blog' / 'content' / 'posts'

        self.posts_dir.mkdir(parents=True, exist_ok=True)

    def run(self, save_markdown: bool = True):
        """运行Twitter内容生成流程"""
        try:
            logger.info("=" * 80)
            logger.info("Starting Twitter content generation")
            logger.info("=" * 80)

            # 1. 初始化生成器
            logger.info("\n[1/4] Initializing Twitter post generator...")
            generator = TwitterPostGenerator(
                api_key=self.api_key,
                base_url=self.base_url,
                headless=self.headless
            )
            logger.info(f"✓ Monitoring accounts: {generator.crawler.accounts}")

            # 2. 抓取推文
            logger.info("\n[2/4] Crawling recent tweets (last 30 minutes)...")
            logger.info("    This may take a while as we're using browser automation...")
            tweets_data = generator.crawl_tweets()
            total_tweets = sum(len(tweets) for tweets in tweets_data.values())
            logger.info(f"✓ Crawled {total_tweets} tweets from {len(tweets_data)} accounts")

            # 3. 分析推文
            logger.info("\n[3/4] Analyzing tweets with Claude AI...")
            logger.info("    Extracting insights, trends, and pros/cons...")
            analysis_results = generator.analyze_tweets(tweets_data)
            logger.info(f"✓ Analyzed {len(analysis_results)} accounts")

            # 4. 生成内容
            if save_markdown:
                logger.info("\n[4/4] Generating blog posts...")
                posts = generator.save_markdown_posts(str(self.posts_dir))
                logger.info(f"✓ Created {len(posts)} blog posts:")
                for post in posts:
                    logger.info(f"    - {post.name}")
            else:
                posts = []

            logger.info("\n" + "=" * 80)
            logger.info("Twitter content generation completed successfully")
            logger.info("=" * 80)

            return {
                'tweets_crawled': total_tweets,
                'accounts_analyzed': len(analysis_results),
                'posts_created': len(posts),
                'analysis_results': analysis_results
            }

        except Exception as e:
            logger.error(f"Twitter content generation failed: {e}", exc_info=True)
            return None


def main():
    parser = argparse.ArgumentParser(description='Generate content from Twitter tech leaders')
    parser.add_argument('--no-markdown', action='store_true', help='Skip saving markdown files')
    parser.add_argument('--headful', action='store_true', help='Run browser in visible mode (for debugging)')
    parser.add_argument('--api-key', help='Anthropic API key (default: ANTHROPIC_API_KEY env var)')
    parser.add_argument('--base-url', help='Anthropic API base URL (default: ANTHROPIC_BASE_URL env var)')

    args = parser.parse_args()

    generator = TwitterContentGenerator(
        api_key=args.api_key,
        base_url=args.base_url,
        headless=not args.headful
    )

    result = generator.run(save_markdown=not args.no_markdown)

    if result:
        print("\nSummary:")
        print(f"  Tweets crawled: {result['tweets_crawled']}")
        print(f"  Accounts analyzed: {result['accounts_analyzed']}")
        print(f"  Posts created: {result['posts_created']}")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
