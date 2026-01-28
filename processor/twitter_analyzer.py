"""
Twitter Content Analyzer using Claude AI
Twitter内容分析器 - 使用Claude AI分析推文内容，解析大佬观点，分析利弊
"""

import logging
import os
from typing import List, Dict, Optional
from datetime import datetime
import json

from anthropic import Anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterContentAnalyzer:
    """Twitter内容分析器"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化分析器

        Args:
            api_key: Anthropic API密钥
            base_url: 自定义API基础URL（用于Claude Code）
        """
        resolved_api_key = (api_key or "").strip() or os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
        resolved_base_url = (base_url or "").strip() or os.environ.get("ANTHROPIC_BASE_URL")

        if not resolved_api_key:
            logger.warning("TwitterContentAnalyzer disabled: Anthropic API key not configured")
            self.client = None
            return

        try:
            self.client = Anthropic(api_key=resolved_api_key, base_url=resolved_base_url)
        except Exception as e:
            logger.warning(f"TwitterContentAnalyzer disabled: failed to init Anthropic client: {e}")
            self.client = None

    def _build_analysis_prompt(self, tweets: List[Dict]) -> str:
        """构建分析提示词"""
        prompt = """你是一个专业的科技内容分析师。请分析以下Twitter推文，并按照以下格式输出：

分析要求：
1. 总结这些推文的主要观点和主题
2. 识别出推文中的关键技术趋势、商业洞察或重要声明
3. 分析这些观点的利弊（优点和缺点）
4. 提供简短精炼的总结，适合作为社交媒体post

推文数据：
"""

        for i, tweet in enumerate(tweets, 1):
            prompt += f"\n推文 {i}:\n"
            prompt += f"账号: @{tweet.get('account', 'unknown')}\n"
            prompt += f"内容: {tweet.get('text', 'N/A')}\n"
            prompt += f"时间: {tweet.get('timestamp', 'N/A')}\n"
            prompt += f"互动: {tweet.get('likes', '0')} likes, {tweet.get('retweets', '0')} retweets\n"

        prompt += """
请以JSON格式输出分析结果，包含以下字段：
{
  "summary": "简要总结（200字以内）",
  "key_points": ["关键点1", "关键点2", ...],
  "tech_trends": ["技术趋势1", "技术趋势2", ...],
  "pros_and_cons": {
    "pros": ["优点1", "优点2", ...],
    "cons": ["缺点1", "缺点2", ...]
  },
  "social_post": "适合社交媒体的简短post（150字以内）",
  "hashtags": ["#tag1", "#tag2", ...]
}

只返回JSON，不要包含其他文字说明。
"""

        return prompt

    def analyze_tweets(self, tweets: List[Dict]) -> Dict:
        """
        分析推文内容

        Args:
            tweets: 推文列表

        Returns:
            分析结果字典
        """
        if not tweets:
            return {
                "summary": "没有推文需要分析",
                "key_points": [],
                "tech_trends": [],
                "pros_and_cons": {"pros": [], "cons": []},
                "social_post": "",
                "hashtags": []
            }

        if self.client is None:
            return {
                "summary": "分析器未启用（缺少 Anthropic API key）",
                "key_points": [],
                "tech_trends": [],
                "pros_and_cons": {"pros": [], "cons": []},
                "social_post": "",
                "hashtags": [],
                "analyzed_at": datetime.now().isoformat(),
            }

        try:
            logger.info(f"开始分析 {len(tweets)} 条推文")

            prompt = self._build_analysis_prompt(tweets)

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = message.content[0].text

            logger.info(f"Claude AI分析完成")

            json_match = None
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
                json_match = json_str
            elif "{" in response_text and "}" in response_text:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                json_match = response_text[start:end]

            if json_match:
                analysis_result = json.loads(json_match)
                analysis_result["analyzed_at"] = datetime.now().isoformat()
                analysis_result["source_tweets_count"] = len(tweets)
                analysis_result["source_accounts"] = list(set(tweet.get('account', 'unknown') for tweet in tweets))
                return analysis_result
            else:
                logger.warning("无法从响应中提取JSON，返回原始响应")
                return {
                    "summary": response_text[:200],
                    "key_points": [],
                    "tech_trends": [],
                    "pros_and_cons": {"pros": [], "cons": []},
                    "social_post": "",
                    "hashtags": [],
                    "analyzed_at": datetime.now().isoformat()
                }

        except Exception as e:
            logger.error(f"分析推文失败: {e}", exc_info=True)
            return {
                "summary": f"分析失败: {str(e)}",
                "key_points": [],
                "tech_trends": [],
                "pros_and_cons": {"pros": [], "cons": []},
                "social_post": "",
                "hashtags": [],
                "analyzed_at": datetime.now().isoformat()
            }

    def analyze_account_tweets(self, account_tweets: Dict[str, List[Dict]]) -> Dict:
        """
        按账号分析推文

        Args:
            account_tweets: 按账号分组的推文字典

        Returns:
            按账号分组的分析结果
        """
        results = {}

        for account, tweets in account_tweets.items():
            if tweets:
                logger.info(f"分析账号 @{account} 的 {len(tweets)} 条推文")
                analysis = self.analyze_tweets(tweets)
                results[account] = analysis

        return results

    def generate_markdown_post(self, analysis: Dict, account: str) -> str:
        """
        生成Markdown格式的post

        Args:
            analysis: 分析结果
            account: 账号名

        Returns:
            Markdown字符串
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        markdown = f"""# Twitter 精选: @{account}

**分析时间**: {timestamp}

## 摘要

{analysis.get('summary', '暂无摘要')}

## 社交媒体 Post

{analysis.get('social_post', '暂无')}

## 关键观点

"""

        for i, point in enumerate(analysis.get('key_points', []), 1):
            markdown += f"{i}. {point}\n"

        markdown += "\n## 技术趋势\n\n"

        for trend in analysis.get('tech_trends', []):
            markdown += f"- {trend}\n"

        markdown += "\n## 利弊分析\n\n"

        pros = analysis.get('pros_and_cons', {}).get('pros', [])
        if pros:
            markdown += "### 优点\n\n"
            for pro in pros:
                markdown += f"- {pro}\n"

        cons = analysis.get('pros_and_cons', {}).get('cons', [])
        if cons:
            markdown += "\n### 缺点\n\n"
            for con in cons:
                markdown += f"- {con}\n"

        markdown += "\n## 相关标签\n\n"

        hashtags = analysis.get('hashtags', [])
        if hashtags:
            markdown += " ".join(hashtags)

        return markdown


class TwitterPostGenerator:
    """Twitter Post生成器 - 整合爬虫和分析功能"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        headless: bool = True
    ):
        """
        初始化生成器

        Args:
            api_key: Anthropic API密钥
            base_url: 自定义API基础URL
            headless: 是否使用无头浏览器
        """
        from crawler.twitter_crawler import TwitterRecentCrawler

        self.crawler = TwitterRecentCrawler(headless=headless)
        self.analyzer = TwitterContentAnalyzer(api_key=api_key, base_url=base_url)

    def generate_posts(self) -> Dict[str, Dict]:
        """
        生成所有账号的分析post

        Returns:
            按账号分组的分析结果
        """
        import asyncio

        loop = asyncio.get_event_loop()
        account_tweets = loop.run_until_complete(self.crawler.crawl_all())

        analysis_results = self.analyzer.analyze_account_tweets(account_tweets)

        return analysis_results

    def save_markdown_posts(self, output_dir: str = "blog/content/posts"):
        """
        保存Markdown格式的posts

        Args:
            output_dir: 输出目录
        """
        from pathlib import Path

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        analysis_results = self.generate_posts()

        saved_files = []

        for account, analysis in analysis_results.items():
            markdown_content = self.analyzer.generate_markdown_post(analysis, account)

            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"{timestamp}-twitter-{account}.md"
            filepath = output_path / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            saved_files.append(filepath)
            logger.info(f"保存post: {filepath}")

        return saved_files
