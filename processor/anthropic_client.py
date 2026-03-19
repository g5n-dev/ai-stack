"""
Anthropic API client wrapper
Anthropic API 客户端封装
"""

import os
import yaml
import anthropic
from typing import Any, Dict, Optional
import logging
import random
import threading
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NullAnthropicClient:
    def __init__(self, reason: str = "disabled"):
        self.reason = reason

    def create_message(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        *,
        temperature: Optional[float] = None,
    ) -> str:
        return ""


class AnthropicClient:
    """Anthropic API 客户端封装"""

    def __init__(self, config_path='config/anthropic.yaml'):
        self.config = self._load_config(config_path)
        self.client = self._init_client()
        concurrency = self.config.get("llm_concurrency", 3)
        try:
            concurrency = int(concurrency)
        except Exception:
            concurrency = 3
        concurrency = max(1, concurrency)
        self._semaphore = threading.BoundedSemaphore(value=concurrency)

    def _load_config(self, config_path: str) -> Dict:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                anthropic_config = config.get('anthropic', {}) or {}
                anthropic_config = {
                    key: self._resolve_env_placeholder(value)
                    for key, value in anthropic_config.items()
                }
                return anthropic_config

        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def _resolve_env_placeholder(self, value: Any) -> Any:
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var = value[2:-1]
            return os.environ.get(env_var, '')
        return value

    def _default_model(self) -> str:
        base_url = str(self.config.get("base_url") or "").lower()
        if "minimax" in base_url:
            return "MiniMax-M2.7-highspeed"
        return "claude-3-5-sonnet-20241022"

    def _extract_text_from_message(self, message: Any) -> str:
        blocks = getattr(message, "content", None) or []
        texts: list[str] = []
        block_types: list[str] = []

        for block in blocks:
            block_type = getattr(block, "type", None)
            if not block_type and isinstance(block, dict):
                block_type = str(block.get("type") or "")
            if block_type:
                block_types.append(str(block_type))

            text = ""
            if isinstance(block, dict):
                if block.get("type") == "text":
                    text = str(block.get("text") or "")
            elif getattr(block, "type", None) == "text":
                text = str(getattr(block, "text", "") or "")
            elif hasattr(block, "text"):
                text = str(getattr(block, "text", "") or "")

            if text.strip():
                texts.append(text.strip())

        if texts:
            return "\n\n".join(texts).strip()

        raise ValueError(f"No text content found in response blocks: {block_types or ['unknown']}")

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

    def create_message(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        *,
        temperature: Optional[float] = None,
    ) -> str:
        """
        创建消息并获取响应

        Args:
            prompt: 提示词
            max_tokens: 最大 token 数

        Returns:
            str: 响应内容
        """
        max_tokens = max_tokens or self.config.get('max_tokens', 4096)
        model = (
            os.environ.get("ANTHROPIC_MODEL")
            or self.config.get('model')
            or self._default_model()
        )
        temperature = temperature if temperature is not None else self.config.get('temperature', 0.7)
        max_retries = self.config.get("llm_max_retries", 3)
        try:
            max_retries = int(max_retries)
        except Exception:
            max_retries = 3
        max_retries = max(0, max_retries)

        attempt = 0
        while True:
            try:
                with self._semaphore:
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

                response_text = self._extract_text_from_message(message)
                return response_text

            except anthropic.APIError as e:
                retryable = isinstance(
                    e,
                    (
                        getattr(anthropic, "RateLimitError", anthropic.APIError),
                        getattr(anthropic, "APITimeoutError", anthropic.APIError),
                        getattr(anthropic, "APIConnectionError", anthropic.APIError),
                        getattr(anthropic, "InternalServerError", anthropic.APIError),
                    ),
                )
                status_code = getattr(e, "status_code", None)
                if status_code is not None and isinstance(status_code, int) and status_code >= 500:
                    retryable = True

                if (not retryable) or attempt >= max_retries:
                    logger.error(f"Anthropic API error: {e}")
                    raise

                backoff = min(30.0, (2 ** attempt)) + random.uniform(0, 0.5)
                logger.warning(f"Anthropic API retrying in {backoff:.2f}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(backoff)
                attempt += 1

            except Exception as e:
                if attempt >= max_retries:
                    logger.error(f"Failed to create message: {e}")
                    raise
                backoff = min(30.0, (2 ** attempt)) + random.uniform(0, 0.5)
                logger.warning(f"LLM call retrying in {backoff:.2f}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(backoff)
                attempt += 1


if __name__ == '__main__':
    client = AnthropicClient()
    test_prompt = "请用中文简要介绍一下人工智能的发展历史。"
    response = client.create_message(test_prompt)
    print(f"Response: {response}")
