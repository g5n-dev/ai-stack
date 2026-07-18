from __future__ import annotations

import contextlib
import logging
import traceback

import anthropic
import httpx
import pytest

from crawler.search_fallback import PlannedQuery, SearXNGSearchClient
from processor.anthropic_client import AnthropicClient, LLMAuthError, LLMRequestError
from scripts import notify_search_engines

SECRET = "do-not-log-this-token"
PRIVATE_ENDPOINT = f"https://user:{SECRET}@private.example/search?token={SECRET}"


def _messages(caplog) -> str:
    return "\n".join(record.getMessage() for record in caplog.records)


@pytest.mark.parametrize(
    "value",
    ("short", "a" * 129, "contains/slash", "contains space", "包含中文12345678"),
)
def test_indexnow_public_ownership_key_rejects_unsafe_values(value: str) -> None:
    with pytest.raises(ValueError, match="IndexNow ownership key"):
        notify_search_engines.validate_indexnow_key(value)


def test_indexnow_public_ownership_key_accepts_the_documented_character_set() -> None:
    assert notify_search_engines.validate_indexnow_key("Abcd-1234") == "Abcd-1234"
    assert notify_search_engines.validate_indexnow_key(None) is None


class _FailingMessages:
    def __init__(self, error: BaseException):
        self.error = error

    def create(self, **_kwargs):
        raise self.error


class _FailingModelClient:
    def __init__(self, error: BaseException):
        self.messages = _FailingMessages(error)


def _client_with_failure(error: BaseException) -> AnthropicClient:
    client = AnthropicClient.__new__(AnthropicClient)
    client.config = {
        "base_url": "",
        "model": "test-model",
        "llm_max_retries": 0,
        "max_tokens": 128,
        "temperature": 0.0,
    }
    client._semaphore = contextlib.nullcontext()
    client.client = _FailingModelClient(error)
    return client


def test_model_client_initialization_logs_capability_not_private_endpoint(
    monkeypatch, caplog
) -> None:
    client = AnthropicClient.__new__(AnthropicClient)
    client.config = {"api_key": SECRET, "base_url": PRIVATE_ENDPOINT}
    monkeypatch.setattr(anthropic, "Anthropic", lambda **_kwargs: object())

    with caplog.at_level(logging.INFO):
        client._init_client()

    output = _messages(caplog)
    assert "custom_base_url=true" in output
    assert SECRET not in output
    assert PRIVATE_ENDPOINT not in output


def test_model_client_default_endpoint_logs_no_credentials(monkeypatch, caplog) -> None:
    captured = {}
    client = AnthropicClient.__new__(AnthropicClient)
    client.config = {"api_key": SECRET, "base_url": ""}
    monkeypatch.setattr(
        anthropic,
        "Anthropic",
        lambda **kwargs: captured.update(kwargs) or object(),
    )

    with caplog.at_level(logging.INFO):
        client._init_client()

    output = _messages(caplog)
    assert captured == {"api_key": SECRET}
    assert "custom_base_url=false" in output
    assert SECRET not in output


def test_model_runtime_error_logs_only_public_failure_metadata(caplog) -> None:
    error = RuntimeError(f"upstream leaked token={SECRET} endpoint={PRIVATE_ENDPOINT}")
    client = _client_with_failure(error)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(LLMRequestError) as raised:
            client.create_message("prompt", purpose="metadata")

    output = _messages(caplog)
    assert "error_type=RuntimeError" in output
    assert "category=unknown" in output
    assert "purpose=metadata" in output
    assert SECRET not in output
    assert PRIVATE_ENDPOINT not in output
    assert SECRET not in str(raised.value)
    assert PRIVATE_ENDPOINT not in str(raised.value)
    rendered = "".join(traceback.format_exception(raised.value))
    assert SECRET not in rendered
    assert PRIVATE_ENDPOINT not in rendered


def test_model_runtime_auth_failure_keeps_detection_but_redacts_details(caplog) -> None:
    error = RuntimeError(
        f"401 unauthorized token={SECRET} endpoint={PRIVATE_ENDPOINT}"
    )
    client = _client_with_failure(error)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(LLMAuthError) as raised:
            client.create_message("prompt", purpose="generation")

    output = _messages(caplog)
    assert "error_type=RuntimeError" in output
    assert "category=auth" in output
    assert "retryable=false" in output
    assert SECRET not in output
    assert PRIVATE_ENDPOINT not in output
    rendered = "".join(traceback.format_exception(raised.value))
    assert SECRET not in rendered
    assert PRIVATE_ENDPOINT not in rendered


def test_model_request_error_logs_metadata_without_exception_message(caplog) -> None:
    error = LLMRequestError(
        "provider-specific compatibility detail",
        category="compatibility",
        retryable=False,
    )
    client = _client_with_failure(error)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(LLMRequestError):
            client.create_message("prompt", purpose="tag_intro")

    output = _messages(caplog)
    assert "error_type=LLMRequestError" in output
    assert "category=compatibility" in output
    assert "purpose=tag_intro" in output
    assert "provider-specific compatibility detail" not in output


def test_model_api_error_logs_only_public_category_and_status(caplog) -> None:
    error = anthropic.APIError(
        f"provider echoed token={SECRET} endpoint={PRIVATE_ENDPOINT}",
        httpx.Request("POST", PRIVATE_ENDPOINT),
        body={"token": SECRET},
    )
    client = _client_with_failure(error)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(LLMRequestError) as raised:
            client.create_message("prompt", purpose="classification")

    output = _messages(caplog)
    assert "error_type=APIError" in output
    assert "category=api" in output
    assert "status=unknown" in output
    assert "purpose=classification" in output
    assert SECRET not in output
    assert PRIVATE_ENDPOINT not in output
    assert SECRET not in str(raised.value)
    assert PRIVATE_ENDPOINT not in str(raised.value)
    rendered = "".join(traceback.format_exception(raised.value))
    assert SECRET not in rendered
    assert PRIVATE_ENDPOINT not in rendered


def test_model_status_api_error_logs_status_without_response_details(caplog) -> None:
    request = httpx.Request("POST", PRIVATE_ENDPOINT)
    response = httpx.Response(
        429,
        request=request,
        json={"error": f"token={SECRET}"},
    )
    error = anthropic.RateLimitError(
        f"provider echoed token={SECRET}",
        response=response,
        body={"token": SECRET},
    )
    client = _client_with_failure(error)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(LLMRequestError) as raised:
            client.create_message("prompt", purpose="classification")

    output = _messages(caplog)
    assert "error_type=RateLimitError" in output
    assert "category=transient_api" in output
    assert "status=429" in output
    assert "retryable=true" in output
    assert SECRET not in output
    assert PRIVATE_ENDPOINT not in output
    rendered = "".join(traceback.format_exception(raised.value))
    assert SECRET not in rendered
    assert PRIVATE_ENDPOINT not in rendered


def test_search_fallback_logs_only_error_category(monkeypatch, caplog) -> None:
    class FailingSession:
        def get(self, *_args, **_kwargs):
            raise RuntimeError(f"upstream echoed token={SECRET}")

    monkeypatch.delenv("SEARXNG_BASE_URL", raising=False)
    client = SearXNGSearchClient(base_urls=[PRIVATE_ENDPOINT], session=FailingSession())
    client.base_urls = [PRIVATE_ENDPOINT]

    with caplog.at_level(logging.WARNING):
        assert client.search(PlannedQuery(query="AI")) == []

    output = _messages(caplog)
    assert "RuntimeError" in output
    assert SECRET not in output
    assert PRIVATE_ENDPOINT not in output


def test_search_engine_failures_never_log_response_bodies_or_exception_text(
    monkeypatch, caplog
) -> None:
    class FailedResponse:
        status_code = 400
        text = f'{{"error":"token={SECRET}"}}'

    monkeypatch.setattr(
        notify_search_engines.requests,
        "post",
        lambda *_args, **_kwargs: FailedResponse(),
    )
    notifier = notify_search_engines.SearchEngineNotifier(
        base_url="https://ai-stack.site/",
        google_api_key=SECRET,
        google_search_console_url="https://indexing.example/v3/publish",
        bing_api_key=SECRET,
    )

    with caplog.at_level(logging.WARNING):
        assert notifier.notify_google(["https://ai-stack.site/posts/example/"])
        assert notifier.notify_bing(["https://ai-stack.site/posts/example/"])

    output = _messages(caplog)
    assert "status=400" in output
    assert SECRET not in output
    assert FailedResponse.text not in output

    def fail(*_args, **_kwargs):
        raise RuntimeError(f"credential={SECRET}")

    caplog.clear()
    monkeypatch.setattr(notify_search_engines.requests, "post", fail)
    with caplog.at_level(logging.ERROR):
        assert notifier.notify_google(["https://ai-stack.site/posts/example/"]) is False
    output = _messages(caplog)
    assert "RuntimeError" in output
    assert SECRET not in output
