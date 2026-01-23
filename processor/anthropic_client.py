"""
Anthropic API client wrapper
Anthropic API 客户端封装
"""

import os
import yaml
import anthropic
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnthropicClient:
    """Anthropic API 客户端封装"""

    def __init__(self, config_path='config/anthropic.yaml'):
        self.config = self._load_config(config_path)
        self.client = self._init_client()

    def _load_config(self, config_path: str) -> Dict:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                anthropic_config = config.get('anthropic', {})

                # 处理环境变量替换
                api_key = anthropic_config.get('api_key', '')
                base_url = anthropic_config.get('base_url', '')

                if api_key.startswith('${'):
                    env_var = api_key[2:-1]
                    anthropic_config['api_key'] = os.environ.get(env_var, '')

                if base_url.startswith('${'):
                    env_var = base_url[2:-1]
                    anthropic_config['base_url'] = os.environ.get(env_var, '')

                return anthropic_config

        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def _init_client(self) -> anthropic.Anthropic:
        """初始化 Anthropic 客户端"""
        api_key = self.config.get('api_key')
        base_url = self.config.get('base_url')

        if not api_key:
            raise ValueError("Anthropic API key is not configured")

        logger.info(f"Initializing Anthropic client with base_url: {base_url}")

        if base_url:
            return anthropic.Anthropic(api_key=api_key, base_url=base_url)
        else:
            return anthropic.Anthropic(api_key=api_key)

    def create_message(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        创建消息并获取响应

        Args:
            prompt: 提示词
            max_tokens: 最大 token 数

        Returns:
            str: 响应内容
        """
        try:
            max_tokens = max_tokens or self.config.get('max_tokens', 4096)
            model = self.config.get('model', 'claude-3-5-sonnet-20241022')
            temperature = self.config.get('temperature', 0.7)

            logger.info(f"Calling Anthropic API with model: {model}, max_tokens: {max_tokens}")

            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = message.content[0].text
            logger.info(f"API response received, length: {len(response_text)}")

            return response_text

        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to create message: {e}")
            raise


if __name__ == '__main__':
    client = AnthropicClient()
    test_prompt = "请用中文简要介绍一下人工智能的发展历史。"
    response = client.create_message(test_prompt)
    print(f"Response: {response}")
