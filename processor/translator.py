"""
Content translator
内容翻译模块
"""

from typing import Dict
import logging

from .anthropic_client import AnthropicClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentTranslator:
    """内容翻译器"""

    def __init__(self, client: AnthropicClient, default_target_lang='zh'):
        self.client = client
        self.default_target_lang = default_target_lang

    def translate(self, content: str, target_lang: str = None) -> str:
        """
        翻译内容

        Args:
            content: 要翻译的内容
            target_lang: 目标语言 ('zh' 中文, 'en' 英文)

        Returns:
            str: 翻译后的内容
        """
        if not content or len(content.strip()) < 1:
            return ""

        target_lang = target_lang or self.default_target_lang

        try:
            prompt = self._build_translation_prompt(content, target_lang)
            translation = self.client.create_message(prompt, max_tokens=2000, purpose="generation")
            return translation.strip()

        except Exception as e:
            logger.error(f"Failed to translate content: {e}")
            return content  # 翻译失败返回原文

    def _build_translation_prompt(self, content: str, target_lang: str) -> str:
        """构建翻译提示词"""
        lang_map = {
            'zh': '中文',
            'en': '英文',
            'ja': '日文',
            'ko': '韩文'
        }

        target_lang_name = lang_map.get(target_lang, target_lang)
        prompt = f"请将以下内容翻译成{target_lang_name}，保持原文格式和语气：\n\n{content}"
        return prompt

    def translate_repository(self, repo_data: Dict, target_lang='zh') -> Dict:
        """
        翻译仓库信息

        Args:
            repo_data: 仓库数据
            target_lang: 目标语言

        Returns:
            Dict: 包含翻译的数据
        """
        try:
            title = repo_data.get('title', '')
            description = repo_data.get('description', '')

            # 翻译标题
            if title:
                repo_data['title_translated'] = self.translate(title, target_lang)

            # 翻译描述
            if description:
                repo_data['description_translated'] = self.translate(description, target_lang)

            return repo_data

        except Exception as e:
            logger.error(f"Failed to translate repository: {e}")
            return repo_data

    def translate_article(self, article_data: Dict, target_lang='zh') -> Dict:
        """
        翻译文章信息

        Args:
            article_data: 文章数据
            target_lang: 目标语言

        Returns:
            Dict: 包含翻译的数据
        """
        try:
            title = article_data.get('title', '')
            description = article_data.get('description', '')
            summary = article_data.get('summary', '')

            # 翻译标题
            if title:
                article_data['title_translated'] = self.translate(title, target_lang)

            # 翻译描述
            if description:
                article_data['description_translated'] = self.translate(description, target_lang)

            # 翻译摘要
            if summary:
                article_data['summary_translated'] = self.translate(summary, target_lang)

            return article_data

        except Exception as e:
            logger.error(f"Failed to translate article: {e}")
            return article_data


if __name__ == '__main__':
    client = AnthropicClient()
    translator = ContentTranslator(client)

    test_content = "This is a powerful tool for developers to manage code and collaborate effectively."
    translation = translator.translate(test_content, target_lang='zh')
    print(f"Translation: {translation}")
