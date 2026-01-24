"""
AI Theme Filter
AI主题过滤器 - 使用大模型判断内容是否与AI主题相关
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import logging
import re
import json

from .anthropic_client import AnthropicClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FilterResult:
    is_ai_related: bool
    reason: str
    confidence: float


class AIThemeFilter:
    """AI主题过滤器"""

    AI_RELATED_CATEGORIES = [
        "大模型",
        "AI 工程",
        "论文",
        "AI",
        "机器学习",
        "深度学习",
        "自然语言处理",
        "计算机视觉",
    ]

    AI_RELATED_KEYWORDS = [
        "ai", "llm", "gpt", "claude", "gemini", "llama",
        "机器学习", "深度学习", "神经网络", "transformer",
        "nlp", "自然语言处理", "计算机视觉", "cv",
        "rag", "agent", "prompt", "chatbot",
        "模型训练", "推理", "微调",
        "ai开发", "ai应用", "ai工具",
    ]

    def __init__(self, client: AnthropicClient, config: Optional[Dict[str, Any]] = None):
        self.client = client
        self.config = config or {}
        self.enabled = bool(self.config.get("enabled", True))
        self.strict_mode = bool(self.config.get("strict_mode", False))
        self.min_confidence = float(self.config.get("min_confidence", 0.6))

    def filter(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        判断内容是否与AI主题相关

        Returns:
            Dict: 添加了 ai_related, ai_reason, ai_confidence 字段的内容
        """
        if not self.enabled:
            content["ai_related"] = True
            content["ai_reason"] = "Filter disabled"
            content["ai_confidence"] = 1.0
            return content

        try:
            result = self._check_ai_relevance(content)
            content["ai_related"] = result.is_ai_related
            content["ai_reason"] = result.reason
            content["ai_confidence"] = result.confidence
            return content
        except Exception as e:
            logger.error(f"Failed to check AI relevance: {e}")
            content["ai_related"] = False
            content["ai_reason"] = f"Error: {e}"
            content["ai_confidence"] = 0.0
            return content

    def _check_ai_relevance(self, content: Dict[str, Any]) -> FilterResult:
        source = (content.get("source") or "").strip()
        title = (content.get("catchy_title") or content.get("title") or "").strip()
        description = (content.get("description_translated") or content.get("description") or "").strip()
        summary = (content.get("summary_translated") or content.get("summary") or "").strip()
        language = (content.get("language") or "").strip()
        tags = content.get("tags", [])
        categories = content.get("categories", [])

        context_lines = [
            f"source: {source}",
            f"title: {title}",
        ]
        if description:
            context_lines.append(f"description: {description[:500]}")
        if summary:
            context_lines.append(f"summary: {summary[:700]}")
        if language:
            context_lines.append(f"language: {language}")
        if tags:
            context_lines.append(f"tags: {', '.join(str(t) for t in tags[:5])}")
        if categories:
            context_lines.append(f"categories: {', '.join(str(c) for c in categories[:2])}")

        context = "\n".join(context_lines)

        prompt = f"""你是一个内容审核专家，负责判断内容是否与AI（人工智能）主题相关。

AI相关主题包括但不限于：
- 大语言模型（LLM）：GPT, Claude, Llama, Gemini等
- 机器学习/深度学习
- 自然语言处理（NLP）
- 计�算机视觉（CV）
- RAG、Agent、Prompt工程
- AI应用开发、AI工具
- AI相关论文、研究

请判断以下内容是否与AI主题相关，并给出理由和置信度。

要求：
1. 输出严格的JSON格式：{{"is_ai_related": true/false, "reason": "简要理由（中文）", "confidence": 0.0-1.0}}
2. confidence是判断的置信度（0.0-1.0），越接近1.0表示越确定
3. 理由要简洁明确（50字以内）

内容：
{context}

只输出JSON，不要其他内容："""

        try:
            raw = self.client.create_message(prompt, max_tokens=200, temperature=0.1)
            parsed = self._parse_result(raw)

            if parsed:
                if self.strict_mode:
                    if parsed.confidence < self.min_confidence:
                        parsed.is_ai_related = False
                        parsed.reason = f"置信度不足 ({parsed.confidence:.2f} < {self.min_confidence})"
                return parsed

        except Exception as e:
            logger.warning(f"LLM check failed, using fallback: {e}")

        return self._fallback(content)

    def _parse_result(self, raw: str) -> Optional[FilterResult]:
        if not raw or not raw.strip():
            return None

        text = raw.strip()

        parsed = self._try_json(text)
        if parsed is None:
            m = re.search(r"\{[\s\S]*\}", text)
            if m:
                parsed = self._try_json(m.group(0))

        if not isinstance(parsed, dict):
            return None

        is_ai_related = parsed.get("is_ai_related", False)
        reason = parsed.get("reason", "")
        confidence = float(parsed.get("confidence", 0.5))

        return FilterResult(
            is_ai_related=bool(is_ai_related),
            reason=str(reason),
            confidence=confidence
        )

    def _try_json(self, text: str) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(text)
        except Exception:
            return None

    def _fallback(self, content: Dict[str, Any]) -> FilterResult:
        title = (content.get("title") or "").lower()
        description = (content.get("description_translated") or content.get("description") or "").lower()
        summary = (content.get("summary_translated") or content.get("summary") or "").lower()
        tags = [str(t).lower() for t in content.get("tags", [])]
        categories = [str(c).lower() for c in content.get("categories", [])]

        text = " ".join([title, description, summary] + tags + categories)

        keyword_matches = [kw for kw in self.AI_RELATED_KEYWORDS if kw in text]
        category_matches = [cat for cat in self.AI_RELATED_CATEGORIES if any(cat.lower() in c for c in categories)]

        if keyword_matches or category_matches:
            confidence = min(0.9, 0.5 + 0.1 * len(keyword_matches))
            return FilterResult(
                is_ai_related=True,
                reason=f"包含AI关键词: {', '.join(keyword_matches[:3])}" if keyword_matches else f"AI分类: {', '.join(category_matches)}",
                confidence=confidence
            )

        return FilterResult(
            is_ai_related=False,
            reason="未检测到AI相关内容",
            confidence=0.3
        )


def filter_batch(contents: List[Dict[str, Any]], filter: AIThemeFilter) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    批量过滤内容

    Returns:
        tuple: (ai_related_contents, non_ai_related_contents)
    """
    ai_related = []
    non_ai_related = []

    for content in contents:
        filtered_content = filter.filter(content)
        if filtered_content.get("ai_related", False):
            ai_related.append(filtered_content)
        else:
            non_ai_related.append(filtered_content)

    return ai_related, non_ai_related


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from anthropic_client import AnthropicClient
    import yaml

    config = yaml.safe_load(open(Path(__file__).parent.parent / "config" / "anthropic.yaml"))
    client = AnthropicClient(Path(__file__).parent.parent / "config" / "anthropic.yaml")

    filter_config = config.get("anthropic", {}).get("ai_filter", {})
    ai_filter = AIThemeFilter(client, filter_config)

    test_contents = [
        {
            "source": "github_trending",
            "title": "A powerful LLM framework for building AI applications",
            "description": "Build production-ready AI apps with our framework",
        },
        {
            "source": "github_trending",
            "title": "A beautiful React UI component library",
            "description": "Modern UI components for your web applications",
        },
    ]

    for content in test_contents:
        result = ai_filter.filter(content)
        print(f"\n{content['title']}")
        print(f"  AI Related: {result['ai_related']}")
        print(f"  Reason: {result['ai_reason']}")
        print(f"  Confidence: {result['ai_confidence']}")
