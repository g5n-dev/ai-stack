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

from .anthropic_client import AnthropicClient, LLMRequestError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FilterResult:
    is_ai_related: bool
    reason: str
    confidence: float


@dataclass
class ModerationResult:
    should_publish: bool
    reason: str
    confidence: float
    flags: Dict[str, bool]


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
        "openai", "anthropic", "mistral", "copilot", "diffusion",
        "machine learning", "generative ai", "agents",
        "机器学习", "深度学习", "神经网络", "transformer",
        "nlp", "自然语言处理", "计算机视觉", "cv",
        "rag", "agent", "prompt", "chatbot",
        "deep learning",
        "模型训练", "推理", "微调",
        "ai开发", "ai应用", "ai工具",
    ]

    EVIDENCE_TOPIC_GROUPS = (
        (
            "大语言模型",
            frozenset(
                {
                    "llm",
                    "gpt",
                    "claude",
                    "gemini",
                    "llama",
                    "mistral",
                    "chatbot",
                }
            ),
        ),
        ("RAG", frozenset({"rag"})),
        ("AI Agent", frozenset({"agent", "agents"})),
        ("生成式 AI", frozenset({"generative ai", "diffusion"})),
        ("机器学习", frozenset({"machine learning", "机器学习", "模型训练", "微调"})),
        ("深度学习", frozenset({"deep learning", "深度学习", "神经网络"})),
        ("自然语言处理", frozenset({"nlp", "自然语言处理"})),
        ("计算机视觉", frozenset({"cv", "计算机视觉"})),
        ("Prompt 工程", frozenset({"prompt"})),
    )

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
            content["ai_filter_mode"] = "disabled"
            return content

        try:
            result, mode = self._check_ai_relevance(content)
            self._apply_filter_result(content, result, mode=mode)
            return content
        except LLMRequestError as e:
            if e.category in {"compatibility", "transient_api"}:
                logger.warning(f"AI relevance check degraded to fallback: {e}")
                fallback = self._fallback(content)
                self._apply_filter_result(content, fallback, mode="fallback")
                content["ai_error_category"] = e.category
                return content
            logger.error(f"Failed to check AI relevance: {e}")
            content["ai_related"] = False
            content["ai_reason"] = f"Error: {e}"
            content["ai_confidence"] = 0.0
            content["ai_filter_mode"] = "llm"
            content["ai_error_category"] = e.category
            return content
        except Exception as e:
            logger.error(f"Failed to check AI relevance: {e}")
            fallback = self._fallback(content)
            self._apply_filter_result(content, fallback, mode="fallback")
            content["ai_error_category"] = "unknown"
            return content

    def moderate(self, content: Dict[str, Any]) -> Dict[str, Any]:
        if not self.enabled:
            content["should_publish"] = True
            content["moderation_reason"] = "Filter disabled"
            content["moderation_confidence"] = 1.0
            content["moderation_flags"] = {
                "non_tech": False,
                "religion": False,
                "violence": False,
                "low_quality": False,
            }
            content["moderation_mode"] = "disabled"
            return content
        try:
            result, mode = self._check_moderation(content)
            self._apply_moderation_result(content, result, mode=mode)
            return content
        except LLMRequestError as e:
            if e.category in {"compatibility", "transient_api"}:
                logger.warning(f"Moderation degraded after provider issue: {e}")
                try:
                    result, _ = self._check_moderation(content, compact=True)
                    self._apply_moderation_result(content, result, mode="retry")
                    content["moderation_error_category"] = e.category
                    return content
                except LLMRequestError as retry_error:
                    logger.warning(f"Compact moderation retry failed: {retry_error}")
                    fallback = self._fallback_moderation(content)
                    self._apply_moderation_result(content, fallback, mode="fallback")
                    content["moderation_error_category"] = retry_error.category
                    return content
                except Exception as retry_error:
                    logger.warning(f"Compact moderation retry failed: {retry_error}")
                    fallback = self._fallback_moderation(content)
                    self._apply_moderation_result(content, fallback, mode="fallback")
                    content["moderation_error_category"] = "unknown"
                    return content
            logger.error(f"Failed to moderate content: {e}")
            content["should_publish"] = False
            content["moderation_reason"] = f"Error: {e}"
            content["moderation_confidence"] = 0.0
            content["moderation_flags"] = {
                "non_tech": False,
                "religion": False,
                "violence": False,
                "low_quality": True,
            }
            content["moderation_mode"] = "llm"
            content["moderation_error_category"] = e.category
            return content
        except Exception as e:
            logger.error(f"Failed to moderate content: {e}")
            fallback = self._fallback_moderation(content)
            self._apply_moderation_result(content, fallback, mode="fallback")
            content["moderation_error_category"] = "unknown"
            return content

    def filter_evidence_only(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Run the deterministic AI-topic gate without invoking a model."""

        if not self.enabled:
            content["ai_related"] = True
            content["ai_reason"] = "Filter disabled"
            content["ai_confidence"] = 1.0
            content["ai_filter_mode"] = "disabled"
            return content
        self._apply_filter_result(content, self._fallback(content), mode="evidence_only")
        return content

    def moderate_evidence_only(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Apply fail-closed deterministic moderation to a source card."""

        if not self.enabled:
            content["should_publish"] = True
            content["moderation_reason"] = "Filter disabled"
            content["moderation_confidence"] = 1.0
            content["moderation_flags"] = {
                "non_tech": False,
                "religion": False,
                "violence": False,
                "low_quality": False,
            }
            content["moderation_mode"] = "disabled"
            return content
        self._apply_moderation_result(
            content,
            self._fallback_moderation(content),
            mode="evidence_only",
        )
        return content

    def evidence_topic_tags(self, content: Dict[str, Any]) -> List[str]:
        """Derive conservative taxonomy tags from the same evidence as the AI gate."""

        keyword_matches, category_matches = self._fallback_matches(content)
        matched = {keyword.lower() for keyword in keyword_matches}
        topics = [
            topic
            for topic, keywords in self.EVIDENCE_TOPIC_GROUPS
            if matched.intersection(keywords)
        ]
        for category in category_matches:
            if category not in topics:
                topics.append(category)
        if (keyword_matches or category_matches) and not topics:
            topics.append("AI")
        return topics

    def _apply_filter_result(self, content: Dict[str, Any], result: FilterResult, *, mode: str) -> None:
        content["ai_related"] = result.is_ai_related
        content["ai_reason"] = result.reason
        content["ai_confidence"] = result.confidence
        content["ai_filter_mode"] = mode

    def _apply_moderation_result(self, content: Dict[str, Any], result: ModerationResult, *, mode: str) -> None:
        content["should_publish"] = result.should_publish
        content["moderation_reason"] = result.reason
        content["moderation_confidence"] = result.confidence
        content["moderation_flags"] = result.flags
        content["moderation_mode"] = mode

    def _check_ai_relevance(self, content: Dict[str, Any]) -> tuple[FilterResult, str]:
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

        raw = self.client.create_message(
            prompt,
            max_tokens=200,
            temperature=0.1,
            purpose="classification",
        )
        parsed = self._parse_result(raw)

        if parsed:
            if self.strict_mode and parsed.confidence < self.min_confidence:
                parsed.is_ai_related = False
                parsed.reason = f"置信度不足 ({parsed.confidence:.2f} < {self.min_confidence})"
            return parsed, "llm"

        return self._fallback(content), "fallback"

    def _check_moderation(self, content: Dict[str, Any], *, compact: bool = False) -> tuple[ModerationResult, str]:
        source = (content.get("source") or "").strip()
        title = (content.get("catchy_title") or content.get("title") or "").strip()
        url = (content.get("url") or content.get("external_url") or "").strip()
        description = (content.get("description_translated") or content.get("description") or "").strip()
        summary = (content.get("summary_translated") or content.get("summary") or "").strip()
        language = (content.get("language") or "").strip()
        tags = content.get("tags", [])
        categories = content.get("categories", [])
        score = content.get("score")
        comments = content.get("comments")

        context_lines = [
            f"source: {source}",
            f"title: {title}",
        ]
        if url:
            context_lines.append(f"url: {url}")
        if description:
            context_lines.append(f"description: {description[:500]}")
        if summary:
            context_lines.append(f"summary: {summary[:700]}")
        if language:
            context_lines.append(f"language: {language}")
        if tags:
            context_lines.append(f"tags: {', '.join(str(t) for t in tags[:8])}")
        if categories:
            context_lines.append(f"categories: {', '.join(str(c) for c in categories[:4])}")
        if score is not None:
            context_lines.append(f"score: {score}")
        if comments is not None:
            context_lines.append(f"comments: {comments}")

        context = "\n".join(context_lines)

        prompt = self._build_moderation_prompt(context, compact=compact)

        raw = self.client.create_message(
            prompt,
            max_tokens=180 if compact else 250,
            temperature=0.1,
            purpose="classification",
        )
        parsed = self._parse_moderation_result(raw)
        if parsed:
            if self.strict_mode and parsed.confidence < self.min_confidence:
                parsed.should_publish = False
                parsed.reason = f"置信度不足 ({parsed.confidence:.2f} < {self.min_confidence})"
            return parsed, "llm"

        return self._fallback_moderation(content), "fallback"

    def _build_moderation_prompt(self, context: str, *, compact: bool = False) -> str:
        if compact:
            return f"""你是 AI Stack 的内容审核器。请仅基于给定内容判断是否可发布。

只拦截以下情况：
1) 明确与 AI/机器学习/大模型/Agent/RAG/Prompt/AI应用 无关
2) 明确包含宗教、暴力、血腥、仇恨、极端主义
3) 内容为空、只有标题、或明显是提示词/解释性废话

输出严格 JSON：
{{"should_publish": true/false, "reason": "中文，<=40字", "confidence": 0.0-1.0, "flags": {{"non_tech": true/false, "religion": true/false, "violence": true/false, "low_quality": true/false}}}}

内容：
{context}

只输出 JSON。"""

        return f"""你是一个严格的内容审核员，负责决定内容是否应该发布到“AI Stack”技术站点。

审核标准（全部满足才可发布）：
1) 必须与 AI/机器学习/大模型/Agent/RAG/Prompt 工程/AI应用开发/AI工具/AI论文 强相关
2) 必须是科技/工程/研究导向，禁止宗教/暴力/血腥/仇恨/极端主义等内容
3) 必须具备可读的信息量：如果只有标题、或信息不足以形成可信总结，判为低质并拒绝发布

请输出严格 JSON：
{{
  "should_publish": true/false,
  "reason": "中文，<=60字",
  "confidence": 0.0-1.0,
  "flags": {{
    "non_tech": true/false,
    "religion": true/false,
    "violence": true/false,
    "low_quality": true/false
  }}
}}

内容：
{context}

只输出 JSON，不要其他内容："""

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

    def _parse_moderation_result(self, raw: str) -> Optional[ModerationResult]:
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

        should_publish = bool(parsed.get("should_publish", False))
        reason = str(parsed.get("reason", "") or "")
        confidence = float(parsed.get("confidence", 0.5))
        flags = parsed.get("flags", {}) if isinstance(parsed.get("flags", {}), dict) else {}
        normalized_flags = {
            "non_tech": bool(flags.get("non_tech", False)),
            "religion": bool(flags.get("religion", False)),
            "violence": bool(flags.get("violence", False)),
            "low_quality": bool(flags.get("low_quality", False)),
        }

        return ModerationResult(
            should_publish=should_publish,
            reason=reason,
            confidence=confidence,
            flags=normalized_flags,
        )

    def _try_json(self, text: str) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(text)
        except Exception:
            return None

    def _fallback_matches(
        self,
        content: Dict[str, Any],
    ) -> tuple[List[str], List[str]]:
        title = (content.get("title") or "").lower()
        description = (content.get("description_translated") or content.get("description") or "").lower()
        summary = (content.get("summary_translated") or content.get("summary") or "").lower()
        tags = [str(t).lower() for t in content.get("tags", [])]
        categories = [str(c).lower() for c in content.get("categories", [])]

        source_text = str(
            content.get("source_display_excerpt")
            or content.get("source_text_original")
            or ""
        ).lower()
        category = str(content.get("category") or "").lower()
        language = str(content.get("language") or "").lower()
        text = " ".join(
            [title, description, summary, source_text, category, language]
            + tags
            + categories
        )

        def matches(keyword: str) -> bool:
            token = keyword.lower()
            if not token.isascii():
                return token in text
            pattern = r"llms?" if token == "llm" else re.escape(token)
            return re.search(
                rf"(?<![a-z0-9]){pattern}(?![a-z0-9])",
                text,
            ) is not None

        keyword_matches = [kw for kw in self.AI_RELATED_KEYWORDS if matches(kw)]
        category_matches = [cat for cat in self.AI_RELATED_CATEGORIES if any(cat.lower() in c for c in categories)]
        return keyword_matches, category_matches

    def _fallback(self, content: Dict[str, Any]) -> FilterResult:
        keyword_matches, category_matches = self._fallback_matches(content)
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

    def _fallback_moderation(self, content: Dict[str, Any]) -> ModerationResult:
        fallback_result = self._fallback(dict(content))
        ai_related = bool(fallback_result.is_ai_related)
        if ai_related:
            return ModerationResult(
                should_publish=True,
                reason="fallback: AI相关",
                confidence=float(fallback_result.confidence or 0.5),
                flags={"non_tech": False, "religion": False, "violence": False, "low_quality": False},
            )
        return ModerationResult(
            should_publish=False,
            reason="fallback: 非AI或不确定",
            confidence=float(fallback_result.confidence or 0.3),
            flags={"non_tech": True, "religion": False, "violence": False, "low_quality": True},
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
