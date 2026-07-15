"""
Content summarizer
内容总结模块
"""

from typing import Dict
import logging

from .anthropic_client import AnthropicClient
from .markdown_normalizer import looks_incomplete_text, normalize_generated_markdown

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
            summary = self.client.create_message(prompt, max_tokens=500, purpose="generation")
            text = normalize_generated_markdown(
                summary or "",
                wrapper_headings={"摘要", "摘要/简介", "核心摘要"},
                strip_first_heading=True,
                demote_headings=True,
            ).strip()
            if self._looks_like_meta_disclaimer(text):
                return ""
            if looks_incomplete_text(text):
                return ""
            return text

        except Exception as e:
            logger.error(f"Failed to summarize content: {e}")
            return ""

    def _looks_like_meta_disclaimer(self, text: str) -> bool:
        t = (text or "").strip()
        if not t:
            return False
        patterns = [
            "由于您提供",
            "仅为标题",
            "我将基于",
            "我无法从",
            "无法从提供",
            "鉴于您提供",
            "评价对象",
            "评价视角",
            "字数控制",
            "输出要求",
            "结构要求",
            "格式要求",
            "写作要求",
            "使用markdown格式组织内容",
        ]
        return any(p in t for p in patterns)

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

        prompt = (
            f"{instruction}\n"
            "只输出正文，不要写标题，不要写“## 摘要”这类区块名，不要额外包裹 Markdown 总标题；"
            "如果需要小节，请从三级标题（###）开始。\n\n"
            f"内容：\n{content}"
        )
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

            deepwiki_text = repo_data.get('deepwiki_content', '') or ''
            if deepwiki_text.strip():
                content += f"\nDeepWiki（节选）：\n{deepwiki_text[:2000]}\n"

            summary = self.summarize(content, style='concise')

            repo_data['generated_summary'] = summary
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
            if "source_summary_original" not in article_data:
                article_data["source_summary_original"] = summary or description or ""

            # 优先使用已有的摘要，否则总结标题和描述
            if summary:
                content = f"{title}\n{summary}"
            elif description:
                content = f"{title}\n{description}"
            else:
                article_data['generated_summary'] = ""
                return article_data

            summary_text = self.summarize(content, style='concise')

            article_data['generated_summary'] = summary_text
            return article_data

        except Exception as e:
            logger.error(f"Failed to summarize article: {e}")
            article_data['generated_summary'] = ""
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
