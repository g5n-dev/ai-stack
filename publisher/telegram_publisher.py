"""
Telegram publisher
Telegram 推送模块
"""

import os
import requests
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramPublisher:
    """Telegram 推送器"""

    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or os.environ.get('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.environ.get('TELEGRAM_CHAT_ID')
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, text: str, parse_mode='HTML') -> bool:
        """
        发送文本消息

        Args:
            text: 消息内容
            parse_mode: 解析模式 ('HTML', 'Markdown')

        Returns:
            bool: 是否成功
        """
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': False
            }

            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()

            logger.info("Telegram message sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    def send_photo(self, photo_url: str, caption: str = None) -> bool:
        """
        发送图片

        Args:
            photo_url: 图片 URL
            caption: 图片说明

        Returns:
            bool: 是否成功
        """
        try:
            url = f"{self.api_url}/sendPhoto"
            data = {
                'chat_id': self.chat_id,
                'photo': photo_url,
                'caption': caption
            }

            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()

            logger.info("Telegram photo sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send Telegram photo: {e}")
            return False

    def format_message(self, content: Dict) -> str:
        """
        格式化内容为 Telegram 消息

        Args:
            content: 内容数据

        Returns:
            str: 格式化后的消息（HTML 格式）
        """
        title = content.get('title', '')
        summary = content.get('summary', '')
        url = content.get('url', '')
        source = content.get('source', '')

        # 构建 HTML 消息
        message_parts = []

        # 标题
        if title:
            message_parts.append(f"<b>{title}</b>")

        # 来源标签
        if source:
            message_parts.append(f"📌 <i>[{source.upper()}]</i>")

        # 摘要
        if summary:
            message_parts.append(f"\n{summary}")

        # 链接
        if url:
            message_parts.append(f"\n🔗 <a href='{url}'>查看详情</a>")

        # AI 生成内容
        if content.get('generated_comment'):
            message_parts.append(f"\n\n💭 <b>AI 评论：</b>")
            message_parts.append(f"{content['generated_comment'][:300]}...")

        return '\n'.join(message_parts)

    def publish_content(self, content: Dict) -> bool:
        """
        推送内容到 Telegram

        Args:
            content: 内容数据

        Returns:
            bool: 是否成功
        """
        try:
            message = self.format_message(content)
            return self.send_message(message, parse_mode='HTML')

        except Exception as e:
            logger.error(f"Failed to publish content to Telegram: {e}")
            return False

    def publish_batch(self, contents: List[Dict]) -> List[bool]:
        """
        批量推送内容

        Args:
            contents: 内容列表

        Returns:
            List[bool]: 推送结果列表
        """
        results = []
        for content in contents:
            result = self.publish_content(content)
            results.append(result)

        success_count = sum(results)
        logger.info(f"Published {success_count}/{len(contents)} contents to Telegram")

        return results


if __name__ == '__main__':
    # 测试 Telegram 推送
    publisher = TelegramPublisher()

    test_content = {
        'title': 'GitHub Trending: awesome-project',
        'summary': 'A powerful tool for developers with many stars',
        'url': 'https://github.com/user/awesome-project',
        'source': 'github_trending',
        'generated_comment': 'This project has great potential and is worth watching.'
    }

    success = publisher.publish_content(test_content)
    print(f"Publish result: {success}")
