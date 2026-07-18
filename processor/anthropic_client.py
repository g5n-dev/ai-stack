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


class LLMRequestError(RuntimeError):
    def __init__(self, message: str, *, category: str, retryable: bool = False):
        self.category = category
        self.retryable = retryable
        super().__init__(message)


class LLMAuthError(LLMRequestError):
    def __init__(self, message: str):
        super().__init__(message, category="auth", retryable=False)


class LLMTransientAPIError(LLMRequestError):
    def __init__(self, message: str):
        super().__init__(message, category="transient_api", retryable=True)


class LLMCompatibilityError(LLMRequestError):
    def __init__(self, message: str):
        super().__init__(message, category="compatibility", retryable=False)


class NoTextContentError(LLMCompatibilityError, ValueError):
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
        purpose: str = "generation",
    ) -> str:
        return ""


class AnthropicClient:
    """Anthropic API 客户端封装"""

    PURPOSE_GENERATION = "generation"
    PURPOSE_CLASSIFICATION = "classification"
    PURPOSE_METADATA = "metadata"
    PURPOSE_TAG_INTRO = "tag_intro"
    SUPPORTED_PURPOSES = {
        PURPOSE_GENERATION,
        PURPOSE_CLASSIFICATION,
        PURPOSE_METADATA,
        PURPOSE_TAG_INTRO,
    }

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

    def _normalize_purpose(self, purpose: str | None) -> str:
        value = str(purpose or self.PURPOSE_GENERATION).strip().lower()
        if value in self.SUPPORTED_PURPOSES:
            return value
        return self.PURPOSE_GENERATION

    def _purpose_policy(self, purpose: str, configured_max_retries: int) -> Dict[str, int | bool]:
        purpose = self._normalize_purpose(purpose)
        if self._is_minimax_backend():
            return {
                "allow_structural_fallback": purpose in {
                    self.PURPOSE_GENERATION,
                    self.PURPOSE_CLASSIFICATION,
                    self.PURPOSE_METADATA,
                    self.PURPOSE_TAG_INTRO,
                },
                "api_retries": min(max(0, configured_max_retries), 1)
                if purpose == self.PURPOSE_GENERATION
                else 0,
            }
        return {
            "allow_structural_fallback": purpose in {
                self.PURPOSE_GENERATION,
                self.PURPOSE_CLASSIFICATION,
                self.PURPOSE_METADATA,
                self.PURPOSE_TAG_INTRO,
            },
            "api_retries": max(0, configured_max_retries)
            if purpose == self.PURPOSE_GENERATION
            else 0,
        }

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
                candidate_text = block.get("text")
                if block.get("type") == "text" or (candidate_text and not block.get("type")):
                    text = str(candidate_text or "")
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

    def _looks_like_auth_error(self, text: str) -> bool:
        lowered = str(text or "").lower()
        return any(
            hint in lowered
            for hint in [
                "authentication",
                "unauthorized",
                "forbidden",
                "invalid api key",
                "身份验证失败",
                "认证失败",
                "鉴权失败",
                "invalid x-api-key",
            ]
        )

    def _classify_api_error(self, error: anthropic.APIError) -> LLMRequestError:
        status_code = getattr(error, "status_code", None)
        message = str(error)
        if status_code in {401, 403} or self._looks_like_auth_error(message):
            return LLMAuthError("Model request authentication failed")
        retryable = isinstance(
            error,
            (
                getattr(anthropic, "RateLimitError", anthropic.APIError),
                getattr(anthropic, "APITimeoutError", anthropic.APIError),
                getattr(anthropic, "APIConnectionError", anthropic.APIError),
                getattr(anthropic, "InternalServerError", anthropic.APIError),
            ),
        )
        if status_code is not None and isinstance(status_code, int):
            if status_code in {408, 409, 429} or status_code >= 500:
                retryable = True
        if retryable:
            return LLMTransientAPIError("Model API request failed transiently")
        return LLMRequestError("Model API request failed", category="api", retryable=False)

    def _log_request_failure(
        self,
        *,
        error: BaseException,
        category: str,
        purpose: str,
        retryable: bool,
    ) -> None:
        status_code = getattr(error, "status_code", None)
        public_status = (
            str(status_code)
            if isinstance(status_code, int) and 100 <= status_code <= 599
            else "unknown"
        )
        logger.error(
            "Model request failed "
            "(error_type=%s, category=%s, status=%s, purpose=%s, retryable=%s)",
            type(error).__name__,
            category,
            public_status,
            purpose,
            "true" if retryable else "false",
        )

    def _init_client(self) -> anthropic.Anthropic:
        """初始化 Anthropic 客户端"""
        api_key = self.config.get('api_key')
        base_url = self.config.get('base_url')

        if not api_key:
            raise ValueError("Anthropic API key is not configured")

        logger.info(
            "Initializing Anthropic client (custom_base_url=%s)",
            "true" if bool(base_url) else "false",
        )

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
        purpose: str = PURPOSE_GENERATION,
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
        purpose = self._normalize_purpose(purpose)
        temperature = temperature if temperature is not None else self.config.get('temperature', 0.7)
        max_retries = self.config.get("llm_max_retries", 3)
        try:
            max_retries = int(max_retries)
        except Exception:
            max_retries = 3
        max_retries = max(0, max_retries)
        policy = self._purpose_policy(purpose, max_retries)

        api_attempt = 0
        structural_fallback_used = False
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
                    if (
                        policy["allow_structural_fallback"]
                        and self._is_minimax_backend()
                        and (not structural_fallback_used)
                        and ("thinking" in e.block_types)
                    ):
                        fallback_max_tokens = self._fallback_max_tokens(current_max_tokens)
                        logger.info(
                            "MiniMax returned thinking without text; retrying once with thinking disabled "
                            f"and max_tokens={fallback_max_tokens}"
                        )
                        current_max_tokens = fallback_max_tokens
                        structural_fallback_used = True
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

                if (
                    policy["allow_structural_fallback"]
                    and self._should_retry_truncated_text(message=message, text=response_text)
                    and (not structural_fallback_used)
                ):
                    fallback_max_tokens = self._fallback_max_tokens(current_max_tokens)
                    if fallback_max_tokens > current_max_tokens:
                        logger.info(
                            "LLM response ended at max_tokens; retrying once with max_tokens="
                            f"{fallback_max_tokens}"
                        )
                        current_max_tokens = fallback_max_tokens
                        structural_fallback_used = True
                        continue
                return response_text

            except anthropic.APIError as e:
                classified = self._classify_api_error(e)
                if classified.retryable and api_attempt < int(policy["api_retries"]):
                    backoff = min(30.0, (2 ** api_attempt)) + random.uniform(0, 0.5)
                    logger.warning(
                        "Anthropic API retrying in %.2fs (attempt %s/%s, purpose=%s)",
                        backoff,
                        api_attempt + 1,
                        int(policy["api_retries"]),
                        purpose,
                    )
                    time.sleep(backoff)
                    api_attempt += 1
                    continue
                self._log_request_failure(
                    error=e,
                    category=classified.category,
                    purpose=purpose,
                    retryable=classified.retryable,
                )
                raise classified from None

            except LLMRequestError as e:
                self._log_request_failure(
                    error=e,
                    category=e.category,
                    purpose=purpose,
                    retryable=e.retryable,
                )
                raise

            except Exception as e:
                if self._looks_like_auth_error(str(e)):
                    self._log_request_failure(
                        error=e,
                        category="auth",
                        purpose=purpose,
                        retryable=False,
                    )
                    raise LLMAuthError("Model request authentication failed") from None
                self._log_request_failure(
                    error=e,
                    category="unknown",
                    purpose=purpose,
                    retryable=False,
                )
                raise LLMRequestError(
                    "Model request failed",
                    category="unknown",
                    retryable=False,
                ) from None


if __name__ == '__main__':
    client = AnthropicClient()
    test_prompt = "请用中文简要介绍一下人工智能的发展历史。"
    response = client.create_message(test_prompt)
    print(f"Response: {response}")
