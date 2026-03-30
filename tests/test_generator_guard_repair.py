#!/usr/bin/env python3

import unittest

from processor.generator import SuperEnhancedContentGenerator


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


class GeneratorGuardRepairTest(unittest.TestCase):
    def setUp(self):
        self.base_content = {
            "title": "LLM agent toolkit",
            "source": "github_trending",
            "description": "A toolkit for building production AI agents",
            "summary": "This toolkit provides orchestration, memory, and tool execution capabilities.",
            "engaging_intro": "由于您提供的标题有限，我将基于常见技术写法生成内容。",
            "deep_comment": "深度评论" * 80,
            "comprehensive_analysis": "技术分析" * 160,
        }

    def test_repairs_invalid_intro_once(self):
        fixed_intro = "这是一段合格的技术导语，用于解释项目的核心价值、使用场景、工程约束与落地方式，帮助读者快速理解项目重点。" * 2
        generator = SuperEnhancedContentGenerator(_FakeClient([fixed_intro]), {"quality_retries": 0})

        result = generator._repair_guarded_sections(dict(self.base_content))

        self.assertEqual(result["guard_repaired_sections"], ["engaging_intro"])
        self.assertNotIn("guard_failed_sections", result)
        self.assertIn("技术导语", result["engaging_intro"])
        self.assertEqual(generator.client.calls[0]["purpose"], "generation")

    def test_marks_guard_failed_when_repair_still_invalid(self):
        generator = SuperEnhancedContentGenerator(
            _FakeClient(["由于您提供的标题有限，我仍然只能给出泛化说明。"]),
            {"quality_retries": 0},
        )

        result = generator._repair_guarded_sections(dict(self.base_content))

        self.assertIn("engaging_intro", result["guard_failed_sections"])


if __name__ == "__main__":
    unittest.main()
