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

from runtime_env import load_project_env
from runtime_profile import apply_anthropic_runtime_profile, get_runtime_profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NoTextContentError(ValueError):
    def __init__(self, block_types: list[str], stop_reason: str | None = None):
        self.block_types = block_types
        self.stop_reason = stop_reason
        suffix = f", stop_reason={stop_reason}" if stop_reason else ""
        super().__init__(f"No text content found in response blocks: {block_types}{suffix}")


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

    def __init__(self, config_path='config/anthropic.yaml', runtime_profile: str | None = None):
        load_project_env()
        self.runtime_profile = get_runtime_profile(runtime_profile)
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
                return apply_anthropic_runtime_profile(anthropic_config, self.runtime_profile)

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

    def _is_minimax_backend(self) -> bool:
        return "minimax" in str(self.config.get("base_url") or "").lower()

    def _thinking_disabled_by_default(self) -> bool:
        configured = self.config.get("disable_thinking")
        if isinstance(configured, bool):
            return configured
        if isinstance(configured, str) and configured.strip():
            return configured.strip().lower() in {"1", "true", "yes", "on"}
        return self._is_minimax_backend()

    def _build_request_kwargs(
        self,
        *,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        disable_thinking: Optional[bool] = None,
    ) -> Dict[str, Any]:
        request: Dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                }
            ],
        }
        if disable_thinking is None:
            disable_thinking = self._thinking_disabled_by_default()
        if disable_thinking:
            request["thinking"] = {"type": "disabled"}
        return request

    def _fallback_max_tokens(self, max_tokens: int) -> int:
        configured_max = self.config.get("max_tokens", max_tokens)
        try:
            configured_max = int(configured_max)
        except Exception:
            configured_max = max_tokens
        min_fallback = self.config.get("min_fallback_max_tokens", 2048)
        try:
            min_fallback = int(min_fallback)
        except Exception:
            min_fallback = 2048
        target = max(min_fallback, max_tokens * 2)
        return max(max_tokens, min(configured_max, target))

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

        raise NoTextContentError(
            block_types=block_types or ["unknown"],
            stop_reason=getattr(message, "stop_reason", None),
        )

    def _should_retry_truncated_text(self, *, message: Any, text: str) -> bool:
        if not text or not text.strip():
            return False
        return getattr(message, "stop_reason", None) == "max_tokens"

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
        current_max_tokens = max_tokens or self.config.get('max_tokens', 4096)
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
        retried_truncated_text = False
        while True:
            try:
                with self._semaphore:
                    message = self.client.messages.create(
                        **self._build_request_kwargs(
                            prompt=prompt,
                            model=model,
                            max_tokens=current_max_tokens,
                            temperature=temperature,
                        )
                    )

                try:
                    response_text = self._extract_text_from_message(message)
                except NoTextContentError as e:
                    if ("thinking" in e.block_types) and self._is_minimax_backend():
                        fallback_max_tokens = self._fallback_max_tokens(current_max_tokens)
                        logger.info(
                            "MiniMax returned thinking without text; retrying once with thinking disabled "
                            f"and max_tokens={fallback_max_tokens}"
                        )
                        current_max_tokens = fallback_max_tokens
                        with self._semaphore:
                            fallback_message = self.client.messages.create(
                                **self._build_request_kwargs(
                                    prompt=prompt,
                                    model=model,
                                    max_tokens=current_max_tokens,
                                    temperature=temperature,
                                    disable_thinking=True,
                                )
                            )
                        response_text = self._extract_text_from_message(fallback_message)
                        message = fallback_message
                    else:
                        raise

                if self._should_retry_truncated_text(message=message, text=response_text) and not retried_truncated_text:
                    fallback_max_tokens = self._fallback_max_tokens(current_max_tokens)
                    if fallback_max_tokens > current_max_tokens:
                        logger.info(
                            "LLM response ended at max_tokens; retrying once with max_tokens="
                            f"{fallback_max_tokens}"
                        )
                        current_max_tokens = fallback_max_tokens
                        retried_truncated_text = True
                        continue
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
