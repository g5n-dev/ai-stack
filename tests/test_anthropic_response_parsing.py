#!/usr/bin/env python3

import contextlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def _load_module(module_name: str, relative_path: str):
    fake_anthropic = types.ModuleType("anthropic")
    fake_anthropic.Anthropic = object
    fake_anthropic.APIError = Exception
    fake_anthropic.RateLimitError = Exception
    fake_anthropic.APITimeoutError = Exception
    fake_anthropic.APIConnectionError = Exception
    fake_anthropic.InternalServerError = Exception
    fake_yaml = types.ModuleType("yaml")
    fake_yaml.safe_load = lambda *args, **kwargs: {}

    prev = sys.modules.get("anthropic")
    prev_yaml = sys.modules.get("yaml")
    sys.modules["anthropic"] = fake_anthropic
    sys.modules["yaml"] = fake_yaml
    try:
        spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Failed to load module: {relative_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if prev is None:
            sys.modules.pop("anthropic", None)
        else:
            sys.modules["anthropic"] = prev
        if prev_yaml is None:
            sys.modules.pop("yaml", None)
        else:
            sys.modules["yaml"] = prev_yaml


class _ThinkingBlock:
    type = "thinking"


class _TextBlock:
    type = "text"

    def __init__(self, text: str):
        self.text = text


class _Message:
    def __init__(self, content, stop_reason=None):
        self.content = content
        self.stop_reason = stop_reason


class _FakeMessagesAPI:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if not self.responses:
            raise AssertionError("No more fake responses configured")
        return self.responses.pop(0)


class _FakeClient:
    def __init__(self, responses):
        self.messages = _FakeMessagesAPI(responses)


class AnthropicResponseParsingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anthropic_client_module = _load_module("anthropic_client_test", "processor/anthropic_client.py")
        cls.twitter_analyzer_module = _load_module("twitter_analyzer_test", "processor/twitter_analyzer.py")

    def test_extract_text_skips_thinking_blocks(self):
        client = self.anthropic_client_module.AnthropicClient.__new__(self.anthropic_client_module.AnthropicClient)
        message = _Message([_ThinkingBlock(), _TextBlock("final answer")])

        text = client._extract_text_from_message(message)

        self.assertEqual(text, "final answer")

    def test_extract_text_joins_multiple_text_blocks(self):
        client = self.anthropic_client_module.AnthropicClient.__new__(self.anthropic_client_module.AnthropicClient)
        message = _Message([_TextBlock("part 1"), _TextBlock("part 2")])

        text = client._extract_text_from_message(message)

        self.assertEqual(text, "part 1\n\npart 2")

    def test_default_model_switches_for_minimax(self):
        client = self.anthropic_client_module.AnthropicClient.__new__(self.anthropic_client_module.AnthropicClient)
        client.config = {"base_url": "https://api.minimaxi.com/anthropic"}

        self.assertEqual(client._default_model(), "MiniMax-M2.7-highspeed")

    def test_request_kwargs_disable_thinking_for_minimax(self):
        client = self.anthropic_client_module.AnthropicClient.__new__(self.anthropic_client_module.AnthropicClient)
        client.config = {"base_url": "https://api.minimaxi.com/anthropic"}

        kwargs = client._build_request_kwargs(
            prompt="hello",
            model="MiniMax-M2.7-highspeed",
            max_tokens=256,
            temperature=0.2,
        )

        self.assertEqual(kwargs["thinking"], {"type": "disabled"})
        self.assertEqual(kwargs["messages"][0]["content"][0]["type"], "text")
        self.assertEqual(kwargs["messages"][0]["content"][0]["text"], "hello")

    def test_create_message_retries_thinking_only_minimax_response_once(self):
        client = self.anthropic_client_module.AnthropicClient.__new__(self.anthropic_client_module.AnthropicClient)
        client.config = {
            "base_url": "https://api.minimaxi.com/anthropic",
            "max_tokens": 8192,
            "llm_max_retries": 0,
            "temperature": 0.3,
            "min_fallback_max_tokens": 2048,
        }
        client._semaphore = contextlib.nullcontext()
        client.client = _FakeClient(
            [
                _Message([_ThinkingBlock()], stop_reason="max_tokens"),
                _Message([_TextBlock("final answer")], stop_reason="end_turn"),
            ]
        )

        text = client.create_message("prompt", max_tokens=200, temperature=0.1)

        self.assertEqual(text, "final answer")
        self.assertEqual(len(client.client.messages.calls), 2)
        self.assertEqual(client.client.messages.calls[0]["thinking"], {"type": "disabled"})
        self.assertEqual(client.client.messages.calls[1]["thinking"], {"type": "disabled"})
        self.assertEqual(client.client.messages.calls[1]["max_tokens"], 2048)

    def test_create_message_retries_text_response_stopped_by_max_tokens_once(self):
        client = self.anthropic_client_module.AnthropicClient.__new__(self.anthropic_client_module.AnthropicClient)
        client.config = {
            "base_url": "https://api.minimaxi.com/anthropic",
            "max_tokens": 8192,
            "llm_max_retries": 0,
            "temperature": 0.3,
            "min_fallback_max_tokens": 2048,
        }
        client._semaphore = contextlib.nullcontext()
        client.client = _FakeClient(
            [
                _Message([_TextBlock("half answer")], stop_reason="max_tokens"),
                _Message([_TextBlock("full answer")], stop_reason="end_turn"),
            ]
        )

        text = client.create_message("prompt", max_tokens=300, temperature=0.1)

        self.assertEqual(text, "full answer")
        self.assertEqual(len(client.client.messages.calls), 2)
        self.assertEqual(client.client.messages.calls[0]["max_tokens"], 300)
        self.assertEqual(client.client.messages.calls[1]["max_tokens"], 2048)

    def test_twitter_analyzer_extracts_text_from_mixed_blocks(self):
        analyzer = self.twitter_analyzer_module.TwitterContentAnalyzer.__new__(self.twitter_analyzer_module.TwitterContentAnalyzer)
        message = _Message([_ThinkingBlock(), _TextBlock('{"summary":"ok"}')])

        text = analyzer._extract_response_text(message)

        self.assertEqual(text, '{"summary":"ok"}')


if __name__ == "__main__":
    unittest.main()
