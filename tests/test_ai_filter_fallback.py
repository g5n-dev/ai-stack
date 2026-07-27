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

    def test_evidence_only_filter_uses_token_boundaries_without_calling_model(self):
        client = _FakeClient([])
        flt = AIThemeFilter(client, {"enabled": True})

        false_positive = flt.filter_evidence_only(
            {"title": "A chair design with stainless steel rails"}
        )
        prefixed_token = flt.filter_evidence_only({"title": "xLLMs runtime"})
        suffixed_token = flt.filter_evidence_only({"title": "LLMsomething runtime"})
        ai_story = flt.filter_evidence_only(
            {"title": "OpenAI releases an LLM agent runtime"}
        )

        self.assertFalse(false_positive["ai_related"])
        self.assertFalse(prefixed_token["ai_related"])
        self.assertFalse(suffixed_token["ai_related"])
        self.assertTrue(ai_story["ai_related"])
        self.assertEqual(client.calls, [])

    def test_evidence_topics_use_canonical_taxonomy_for_english_terms(self):
        client = _FakeClient([])
        flt = AIThemeFilter(client, {"enabled": True})
        evidence = {"title": "Modern deep learning systems for production"}

        result = flt.filter_evidence_only(dict(evidence))

        self.assertTrue(result["ai_related"])
        self.assertEqual(flt.evidence_topic_tags(evidence), ["深度学习"])
        self.assertEqual(client.calls, [])

    def test_evidence_only_moderation_rejects_non_ai_source_cards(self):
        flt = AIThemeFilter(_FakeClient([]), {"enabled": True})

        result = flt.moderate_evidence_only(
            {"title": "PostgreSQL vacuum internals"}
        )

        self.assertFalse(result["should_publish"])
        self.assertEqual(result["moderation_mode"], "evidence_only")


if __name__ == "__main__":
    unittest.main()
