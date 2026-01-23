"""
WeChat publisher
微信公众号推送模块
"""

import os
import requests
from typing import Dict, List
import logging
import hashlib
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeChatPublisher:
    """微信公众号推送器"""

    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or os.environ.get('WECHAT_APPID')
        self.app_secret = app_secret or os.environ.get('WECHAT_SECRET')
        self.access_token = None
        self.token_expires_at = 0

    def _get_access_token(self) -> str:
        """
        获取访问令牌

        Returns:
            str: 访问令牌
        """
        # 检查是否需要刷新 token
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token

        try:
            url = "https://api.weixin.qq.com/cgi-bin/token"
            params = {
                'grant_type': 'client_credential',
                'appid': self.app_id,
                'secret': self.app_secret
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            self.access_token = data.get('access_token')
            self.token_expires_at = time.time() + data.get('expires_in', 7200) - 300  # 提前5分钟过期

            logger.info("WeChat access token refreshed")
            return self.access_token

        except Exception as e:
            logger.error(f"Failed to get WeChat access token: {e}")
            return None

    def upload_media(self, media_path: str, media_type='image') -> Dict:
        """
        上传媒体文件

        Args:
            media_path: 媒体文件路径
            media_type: 媒体类型 ('image', 'voice', 'video', 'thumb')

        Returns:
            Dict: 上传结果，包含 media_id
        """
        try:
            access_token = self._get_access_token()
            if not access_token:
                return {}

            url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type={media_type}"

            with open(media_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files, timeout=60)

            response.raise_for_status()
            data = response.json()

            logger.info(f"WeChat media uploaded: {data.get('media_id')}")
            return data

        except Exception as e:
            logger.error(f"Failed to upload WeChat media: {e}")
            return {}

    def publish_article(self, articles: List[Dict]) -> bool:
        """
        发布图文消息

        Args:
            articles: 图文文章列表，每个文章包含 title, author, digest, content, content_source_url, thumb_media_id

        Returns:
            bool: 是否成功
        """
        try:
            access_token = self._get_access_token()
            if not access_token:
                return False

            url = f"https://api.weixin.qq.com/cgi-bin/material/add_news?access_token={access_token}"

            data = {
                'articles': articles
            }

            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()

            result = response.json()
            media_id = result.get('media_id')

            logger.info(f"WeChat article published: {media_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish WeChat article: {e}")
            return False

    def format_article(self, content: Dict, thumb_media_id: str = None) -> Dict:
        """
        格式化内容为微信公众号文章

        Args:
            content: 内容数据
            thumb_media_id: 缩略图媒体 ID

        Returns:
            Dict: 格式化后的文章
        """
        title = content.get('title', '')
        summary = content.get('summary', '')
        url = content.get('url', '')
        source = content.get('source', '')

        # 构建 HTML 内容
        html_content = f"""
        <section style="padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <h1 style="color: #333; margin-bottom: 20px;">{title}</h1>
            <p style="color: #666; margin-bottom: 15px;"><strong>来源：</strong>{source.upper()}</p>
            <p style="color: #333; line-height: 1.8; margin-bottom: 20px;">{summary}</p>
            """

        # 添加 AI 生成内容
        if content.get('generated_comment'):
            html_content += f"""
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <h3 style="color: #666; margin-bottom: 10px;">💭 AI 评论</h3>
                <p style="color: #333;">{content['generated_comment']}</p>
            </div>
            """

        if content.get('generated_analysis'):
            html_content += f"""
            <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <h3 style="color: #2e7d32; margin-bottom: 10px;">📊 深度分析</h3>
                <p style="color: #333;">{content['generated_analysis'][:500]}...</p>
            </div>
            """

        html_content += f"""
            <p style="text-align: center; margin: 30px 0;">
                <a href="{url}" style="display: inline-block; padding: 12px 30px; background: #07c160; color: #fff; text-decoration: none; border-radius: 5px;">
                    查看详情
                </a>
            </p>
        </section>
        """

        return {
            'title': title,
            'author': 'AI Stack Bot',
            'digest': summary[:120],
            'content': html_content,
            'content_source_url': url,
            'thumb_media_id': thumb_media_id
        }

    def publish_content(self, content: Dict, thumb_media_id: str = None) -> bool:
        """
        推送内容到微信公众号

        Args:
            content: 内容数据
            thumb_media_id: 缩略图媒体 ID

        Returns:
            bool: 是否成功
        """
        try:
            article = self.format_article(content, thumb_media_id)
            return self.publish_article([article])

        except Exception as e:
            logger.error(f"Failed to publish content to WeChat: {e}")
            return False


if __name__ == '__main__':
    # 测试微信推送
    publisher = WeChatPublisher()

    test_content = {
        'title': 'GitHub Trending: awesome-project',
        'summary': 'A powerful tool for developers',
        'url': 'https://github.com/user/awesome-project',
        'source': 'github_trending',
        'generated_comment': 'This project has great potential.'
    }

    # 需要先上传图片获取 thumb_media_id
    success = publisher.publish_content(test_content)
    print(f"Publish result: {success}")
