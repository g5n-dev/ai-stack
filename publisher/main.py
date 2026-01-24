"""
Publisher orchestrator
推送调度器 - 统一管理所有推送平台
"""

import yaml
import logging
from typing import List, Dict
from pathlib import Path

from .twitter_publisher import TwitterPublisher
from .telegram_publisher import TelegramPublisher
from .wechat_publisher import WeChatPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PublisherOrchestrator:
    """推送调度器"""

    def __init__(self, config_path='config/publisher.yaml'):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.publishers = self._init_publishers()

    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {'publishers': {}}

    def _init_publishers(self) -> Dict[str, object]:
        """初始化推送器实例"""
        publishers = {}
        publishers_config = self.config.get('publishers', {})

        # Twitter
        if publishers_config.get('twitter', {}).get('enabled', False):
            publishers['twitter'] = TwitterPublisher()
            logger.info("Initialized Twitter publisher")

        # Telegram
        if publishers_config.get('telegram', {}).get('enabled', False):
            publishers['telegram'] = TelegramPublisher()
            logger.info("Initialized Telegram publisher")

        # WeChat
        if publishers_config.get('wechat', {}).get('enabled', False):
            publishers['wechat'] = WeChatPublisher()
            logger.info("Initialized WeChat publisher")

        return publishers

    def publish_all(self, content: Dict) -> Dict[str, bool]:
        """
        推送内容到所有启用的平台

        Args:
            content: 内容数据

        Returns:
            Dict[str, bool]: 各平台的推送结果
        """
        results = {}

        for name, publisher in self.publishers.items():
            try:
                logger.info(f"Publishing to {name}...")
                result = publisher.publish_content(content)
                results[name] = result

                if result:
                    logger.info(f"Successfully published to {name}")
                else:
                    logger.warning(f"Failed to publish to {name}")

            except Exception as e:
                logger.error(f"Error publishing to {name}: {e}")
                results[name] = False

        return results

    def publish_to(self, platform: str, content: Dict) -> bool:
        """
        推送内容到指定平台

        Args:
            platform: 平台名称 ('twitter', 'telegram', 'wechat')
            content: 内容数据

        Returns:
            bool: 是否成功
        """
        if platform not in self.publishers:
            logger.error(f"Unknown publisher: {platform}")
            return False

        try:
            logger.info(f"Publishing to {platform}...")
            publisher = self.publishers[platform]
            result = publisher.publish_content(content)

            if result:
                logger.info(f"Successfully published to {platform}")
            else:
                logger.warning(f"Failed to publish to {platform}")

            return result

        except Exception as e:
            logger.error(f"Error publishing to {platform}: {e}")
            return False

    def publish_batch(self, contents: List[Dict]) -> Dict[str, List[bool]]:
        """
        批量推送内容

        Args:
            contents: 内容列表

        Returns:
            Dict[str, List[bool]]: 各平台的推送结果
        """
        results = {}

        for name, publisher in self.publishers.items():
            results[name] = []

            for content in contents:
                try:
                    result = publisher.publish_content(content)
                    results[name].append(result)
                except Exception as e:
                    logger.error(f"Error publishing to {name}: {e}")
                    results[name].append(False)

        # 统计
        for name, results_list in results.items():
            success_count = sum(results_list)
            logger.info(f"Published {success_count}/{len(contents_list)} contents to {name}")

        return results

    def get_enabled_platforms(self) -> List[str]:
        """
        获取已启用的平台列表

        Returns:
            List[str]: 平台名称列表
        """
        return list(self.publishers.keys())


if __name__ == '__main__':
    # 测试推送器
    orchestrator = PublisherOrchestrator()

    test_content = {
        'title': 'GitHub Trending: awesome-project',
        'summary': 'A powerful tool for developers',
        'url': 'https://github.com/user/awesome-project',
        'source': 'github_trending',
        'tags': ['github', 'trending', 'AI'],
        'generated_comment': 'This project has great potential.'
    }

    enabled = orchestrator.get_enabled_platforms()
    print(f"Enabled platforms: {enabled}")

    if enabled:
        results = orchestrator.publish_all(test_content)
        print(f"Publish results: {results}")
