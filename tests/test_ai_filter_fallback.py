#!/usr/bin/env python3

import unittest

from processor.ai_filter import AIThemeFilter
from processor.anthropic_client import LLMAuthError, LLMCompatibilityError


class _FakeClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def create_message(self, prompt, max_tokens=None, *, temperature=None, purpose="generation"):
        self.calls.append(
            {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "purpose": purpose,
            }
        )
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


class AIThemeFilterFallbackTest(unittest.TestCase):
    def test_filter_compatibility_error_uses_fallback(self):
        flt = AIThemeFilter(_FakeClient([LLMCompatibilityError("thinking-only")]), {"enabled": True})

        result = flt.filter(
            {
                "title": "LLM agent toolkit",
                "summary": "An AI agent framework for RAG workflows",
                "tags": ["LLM", "Agent"],
            }
        )

        self.assertTrue(result["ai_related"])
        self.assertEqual(result["ai_filter_mode"], "fallback")
        self.assertEqual(result["ai_error_category"], "compatibility")

    def test_moderation_compatibility_error_retries_then_falls_back(self):
        flt = AIThemeFilter(
            _FakeClient(
                [
                    LLMCompatibilityError("thinking-only"),
                    LLMCompatibilityError("still bad"),
                ]
            ),
            {"enabled": True},
        )

        result = flt.moderate(
            {
                "title": "LLM agent toolkit",
                "summary": "An AI agent framework for RAG workflows",
                "tags": ["LLM", "Agent"],
            }
        )

        self.assertTrue(result["should_publish"])
        self.assertEqual(result["moderation_mode"], "fallback")
        self.assertEqual(result["moderation_error_category"], "compatibility")

    def test_auth_error_remains_fail_closed(self):
        flt = AIThemeFilter(_FakeClient([LLMAuthError("401 unauthorized")]), {"enabled": True})

        result = flt.filter({"title": "LLM agent toolkit"})

        self.assertFalse(result["ai_related"])
        self.assertEqual(result["ai_filter_mode"], "llm")
        self.assertEqual(result["ai_error_category"], "auth")


if __name__ == "__main__":
    unittest.main()
