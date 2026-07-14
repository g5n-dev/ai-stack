"""
Publisher orchestrator
推送调度器 - 统一管理所有推送平台
"""

import logging
import os
import re
from pathlib import Path
from typing import Any, Protocol

import yaml

from .telegram_publisher import TelegramPublisher
from .twitter_publisher import TwitterPublisher
from .wechat_publisher import WeChatPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_ENV_REFERENCE_RE = re.compile(r"^\$\{([A-Z][A-Z0-9_]*)\}$")


class Publisher(Protocol):
    """Minimal interface shared by every outbound publisher."""

    def publish_content(self, content: dict) -> bool: ...


class PublisherOrchestrator:
    """推送调度器"""

    def __init__(self, config_path: str | Path = "config/publisher.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.publishers = self._init_publishers()

    @staticmethod
    def _resolve_environment_references(value: Any) -> Any:
        """Resolve whole-value ``${NAME}`` references without shell expansion."""
        if isinstance(value, str):
            match = _ENV_REFERENCE_RE.fullmatch(value.strip())
            return os.environ.get(match.group(1)) if match else value
        if isinstance(value, list):
            return [PublisherOrchestrator._resolve_environment_references(item) for item in value]
        if isinstance(value, dict):
            return {
                key: PublisherOrchestrator._resolve_environment_references(item)
                for key, item in value.items()
            }
        return value

    def _load_config(self) -> dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, encoding="utf-8") as f:
                loaded = yaml.safe_load(f) or {}
                if not isinstance(loaded, dict):
                    raise ValueError("publisher configuration must be a mapping")
                return self._resolve_environment_references(loaded)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {"publishers": {}}

    def _init_publishers(self) -> dict[str, Publisher]:
        """初始化推送器实例"""
        publishers: dict[str, Publisher] = {}
        publishers_config = self.config.get("publishers", {})

        # Twitter
        twitter_config = publishers_config.get("twitter", {})
        if twitter_config.get("enabled", False):
            publishers["twitter"] = TwitterPublisher(
                api_key=twitter_config.get("api_key"),
                api_secret=twitter_config.get("api_secret"),
                access_token=twitter_config.get("access_token"),
                access_token_secret=twitter_config.get("access_token_secret"),
                bearer_token=twitter_config.get("bearer_token"),
                max_length=int(twitter_config.get("max_length", 280)),
            )
            logger.info("Initialized Twitter publisher")

        # Telegram
        telegram_config = publishers_config.get("telegram", {})
        if telegram_config.get("enabled", False):
            publishers["telegram"] = TelegramPublisher(
                bot_token=telegram_config.get("bot_token"),
                chat_id=telegram_config.get("chat_id"),
                parse_mode=telegram_config.get("parse_mode", "HTML"),
                disable_web_page_preview=bool(
                    telegram_config.get("disable_web_page_preview", False)
                ),
            )
            logger.info("Initialized Telegram publisher")

        # WeChat
        wechat_config = publishers_config.get("wechat", {})
        if wechat_config.get("enabled", False):
            publishers["wechat"] = WeChatPublisher(
                app_id=wechat_config.get("app_id"),
                app_secret=wechat_config.get("app_secret"),
                media_id=wechat_config.get("media_id"),
            )
            logger.info("Initialized WeChat publisher")

        return publishers

    def publish_all(self, content: dict) -> dict[str, bool]:
        """
        推送内容到所有启用的平台

        Args:
            content: 内容数据

        Returns:
            Dict[str, bool]: 各平台的推送结果
        """
        results: dict[str, bool] = {}

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

    def publish_to(self, platform: str, content: dict) -> bool:
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

    def publish_batch(self, contents: list[dict]) -> dict[str, list[bool]]:
        """
        批量推送内容

        Args:
            contents: 内容列表

        Returns:
            Dict[str, List[bool]]: 各平台的推送结果
        """
        results: dict[str, list[bool]] = {}

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
            logger.info(f"Published {success_count}/{len(contents)} contents to {name}")

        return results

    def get_enabled_platforms(self) -> list[str]:
        """
        获取已启用的平台列表

        Returns:
            List[str]: 平台名称列表
        """
        return list(self.publishers.keys())


if __name__ == "__main__":
    # 测试推送器
    orchestrator = PublisherOrchestrator()

    test_content = {
        "title": "GitHub Trending: awesome-project",
        "summary": "A powerful tool for developers",
        "url": "https://github.com/user/awesome-project",
        "source": "github_trending",
        "tags": ["github", "trending", "AI"],
        "generated_comment": "This project has great potential.",
    }

    enabled = orchestrator.get_enabled_platforms()
    print(f"Enabled platforms: {enabled}")

    if enabled:
        results = orchestrator.publish_all(test_content)
        print(f"Publish results: {results}")
