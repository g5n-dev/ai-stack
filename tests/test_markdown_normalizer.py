#!/usr/bin/env python3

import unittest

from processor.markdown_normalizer import (
    extract_bulleted_items,
    looks_incomplete_text,
    normalize_generated_markdown,
    parse_faq_markdown,
    remove_markdown_sections_by_heading,
)


class MarkdownNormalizerTest(unittest.TestCase):
    def test_normalize_generated_markdown_strips_wrapper_headings(self):
        text = """## 学习路径

### 阶段 1：基础

## 学习路径

### 阶段 2：进阶
"""

        normalized = normalize_generated_markdown(
            text,
            wrapper_headings={"学习路径"},
            strip_first_heading=True,
            demote_headings=False,
        )

        self.assertNotIn("## 学习路径", normalized)
        self.assertIn("### 阶段 1：基础", normalized)
        self.assertIn("### 阶段 2：进阶", normalized)

    def test_parse_faq_markdown_keeps_question_and_answer_body_only(self):
        text = """## 常见问题解答

### Q1: LoST 是什么？

**A**: 一种 3D 形状语义层级分词方法。

---

### Q2: 它解决什么问题？

答案：提升 token 使用效率并增强语义连贯性。
"""

        faq = parse_faq_markdown(text)

        self.assertEqual(len(faq), 2)
        self.assertEqual(faq[0]["question"], "LoST 是什么？")
        self.assertEqual(faq[0]["answer"], "一种 3D 形状语义层级分词方法。")
        self.assertEqual(faq[1]["question"], "它解决什么问题？")
        self.assertEqual(faq[1]["answer"], "提升 token 使用效率并增强语义连贯性。")

    def test_extract_bulleted_items_discards_wrapper_heading(self):
        text = """## 学习要点

• 第一条
• 第二条
"""

        items = extract_bulleted_items(text)

        self.assertEqual(items, ["第一条", "第二条"])

    def test_looks_incomplete_text_detects_truncated_tail(self):
        self.assertTrue(looks_incomplete_text("LoST 通过语义驱"))
        self.assertTrue(looks_incomplete_text("### 总结"))
        self.assertFalse(looks_incomplete_text("LoST 通过语义驱动提升了 3D 形状生成效率。"))

    def test_remove_markdown_sections_by_heading_removes_thought_section(self):
        text = """---
title: test
---

# 标题

## 摘要

正文

## 思考题

### 挑战 1

问题

## 评论

后续正文
"""

        sanitized, removed = remove_markdown_sections_by_heading(text, {"思考题", "挑战与思考题"})

        self.assertEqual(removed, 1)
        self.assertNotIn("## 思考题", sanitized)
        self.assertIn("## 评论", sanitized)


if __name__ == "__main__":
    unittest.main()
