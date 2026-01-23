"""
Content summarizer
内容总结模块
"""

from typing import Dict
import logging

from .anthropic_client import AnthropicClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentSummarizer:
    """内容总结器"""

    def __init__(self, client: AnthropicClient, max_length=200):
        self.client = client
        self.max_length = max_length

    def summarize(self, content: str, style='concise') -> str:
        """
        总结内容

        Args:
            content: 要总结的内容
            style: 总结风格 ('concise', 'detailed', 'bullet')

        Returns:
            str: 总结后的内容
        """
        if not content or len(content.strip()) < 10:
            return ""

        try:
            prompt = self._build_summary_prompt(content, style)
            summary = self.client.create_message(prompt, max_tokens=500)
            return summary.strip()

        except Exception as e:
            logger.error(f"Failed to summarize content: {e}")
            return ""

    def _build_summary_prompt(self, content: str, style: str) -> str:
        """构建总结提示词"""
        if style == 'concise':
            instruction = f"请用中文简洁地总结以下内容，不超过{self.max_length}字。"
        elif style == 'detailed':
            instruction = f"请用中文详细总结以下内容，突出重点信息。"
        elif style == 'bullet':
            instruction = f"请用中文以要点形式总结以下内容，每点不超过30字。"
        else:
            instruction = f"请用中文总结以下内容。"

        prompt = f"{instruction}\n\n内容：\n{content}"
        return prompt

    def summarize_repository(self, repo_data: Dict) -> Dict:
        """
        总结仓库信息

        Args:
            repo_data: 仓库数据

        Returns:
            Dict: 包含总结的数据
        """
        try:
            # 构建要总结的内容
            content = f"""
            仓库名称：{repo_data.get('title', '')}
            描述：{repo_data.get('description', '')}
            编程语言：{repo_data.get('language', '')}
            星标数：{repo_data.get('stars', '')} (+{repo_data.get('today_stars', '')})
            """

            summary = self.summarize(content, style='concise')

            repo_data['summary'] = summary
            return repo_data

        except Exception as e:
            logger.error(f"Failed to summarize repository: {e}")
            repo_data['summary'] = ""
            return repo_data

    def summarize_article(self, article_data: Dict) -> Dict:
        """
        总结文章信息

        Args:
            article_data: 文章数据

        Returns:
            Dict: 包含总结的数据
        """
        try:
            title = article_data.get('title', '')
            description = article_data.get('description', '')
            summary = article_data.get('summary', '')

            # 优先使用已有的摘要，否则总结标题和描述
            if summary:
                content = f"{title}\n{summary}"
            elif description:
                content = f"{title}\n{description}"
            else:
                content = title

            summary_text = self.summarize(content, style='concise')

            article_data['summary'] = summary_text
            return article_data

        except Exception as e:
            logger.error(f"Failed to summarize article: {e}")
            article_data['summary'] = ""
            return article_data


if __name__ == '__main__':
    client = AnthropicClient()
    summarizer = ContentSummarizer(client)

    test_content = """
    这是一个关于 GitHub 上的热门项目。它是一个强大的工具，
    可以帮助开发者更好地管理代码和协作。项目使用了 Python 编写，
    具有丰富的功能和良好的文档支持。
    """

    summary = summarizer.summarize(test_content)
    print(f"Summary: {summary}")
