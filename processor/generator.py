"""
Content Generator
通过多次大模型调用生成结构化文章内容
"""

from typing import Callable, Dict, List, Optional
import logging
import re

from .anthropic_client import AnthropicClient
from .markdown_normalizer import (
    DEFAULT_WRAPPER_HEADINGS,
    extract_bulleted_items,
    filter_related_resources,
    looks_incomplete_text,
    normalize_generated_markdown,
    parse_faq_markdown,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SuperEnhancedContentGenerator:
    """内容生成器（多次大模型调用）"""

    def __init__(self, client: AnthropicClient, config: Dict = None):
        self.client = client
        self.config = config or {}
        self.intro_length = self.config.get('intro_length', 500)
        self.comment_length = self.config.get('comment_length', 1200)
        self.analysis_length = self.config.get('analysis_length', 2500)
        self.use_emoji = self.config.get('use_emoji', False)
        self.add_recommendations = self.config.get('add_recommendations', True)

        # 新增的内容生成开关
        self._generate_code_examples_enabled = self.config.get('generate_code_examples', True)
        self._generate_case_studies_enabled = self.config.get('generate_case_studies', True)
        self._generate_faq_enabled = self.config.get('generate_faq', True)
        self._generate_comparison_enabled = self.config.get('generate_comparison', True)
        self._generate_best_practices_enabled = self.config.get('generate_best_practices', True)
        self._generate_performance_tips_enabled = self.config.get('generate_performance_tips', True)
        self._generate_learning_path_enabled = self.config.get('generate_learning_path', True)
        self._generate_challenges_enabled = self.config.get('generate_challenges', True)
        self._add_recommendations_enabled = self.add_recommendations
        self._quality_retries = int(self.config.get("quality_retries", 1) or 0)

    def _contains_emoji(self, text: str) -> bool:
        if not text:
            return False
        return re.search(r"[\U0001F300-\U0001FAFF]", text) is not None

    def _has_placeholders(self, text: str) -> bool:
        if not text:
            return False
        placeholder_patterns = [
            r"\[标题\]",
            r"\[问题\]",
            r"\[详细解答\]",
            r"\[说明\]",
            r"\[简单\]",
            r"\[中等\]",
            r"\[困难\]",
        ]
        return any(re.search(p, text) for p in placeholder_patterns)

    def _has_hype_words(self, text: str) -> bool:
        if not text:
            return False
        banned = [
            "最强",
            "史上",
            "震撼",
            "引爆",
            "颠覆",
            "必看",
            "神器",
            "爆款",
            "引人入胜",
            "超级",
            "疯狂",
            "炸裂",
            "封神",
            "无敌",
        ]
        return any(w in text for w in banned)

    def _looks_like_meta_disclaimer(self, text: str) -> bool:
        if not text:
            return False
        banned = [
            "由于您提供",
            "仅为标题",
            "我将基于",
            "我无法从",
            "无法从提供",
            "鉴于您提供",
            "评价对象",
            "评价视角",
            "字数控制",
            "输出要求",
            "结构要求",
            "格式要求",
            "写作要求",
            "使用markdown格式组织内容",
        ]
        return any(w in text for w in banned)

    def _normalize_section_text(
        self,
        text: str,
        *,
        wrapper_headings: set[str] | None = None,
        demote_headings: bool = True,
    ) -> str:
        headings = set(DEFAULT_WRAPPER_HEADINGS)
        if wrapper_headings:
            headings.update(wrapper_headings)
        return normalize_generated_markdown(
            text,
            wrapper_headings=headings,
            strip_first_heading=True,
            demote_headings=demote_headings,
        ).strip()

    def _normalize_intro_text(self, text: str) -> str:
        cleaned = self._normalize_section_text(
            text,
            wrapper_headings={"导语"},
            demote_headings=False,
        )
        cleaned = re.sub(r"\n{2,}", "\n\n", cleaned)
        return cleaned.strip()

    def _normalize_body_section_text(self, text: str) -> str:
        return self._normalize_section_text(text, demote_headings=True)

    def _body_only_rule(self, section_name: str, *, allow_subsections: bool = True) -> str:
        if allow_subsections:
            return (
                f"只输出 {section_name} 正文，不要写标题，不要写“## {section_name}”或其他一级/二级总标题；"
                "如果需要分节，请从三级标题（###）开始。"
            )
        return f"只输出 {section_name} 正文，不要写标题、区块名或额外包裹标题。"

    def _validate_text(
        self,
        text: str,
        *,
        min_chars: int,
        max_chars: Optional[int] = None,
        allow_emoji: bool,
        allow_hype: bool,
        allow_placeholders: bool,
    ) -> bool:
        if not text or not isinstance(text, str):
            return False
        t = text.strip()
        if len(t) < min_chars:
            return False
        if max_chars is not None and len(t) > max_chars:
            return False
        if self._looks_like_meta_disclaimer(t):
            return False
        if (not allow_emoji) and self._contains_emoji(t):
            return False
        if (not allow_hype) and self._has_hype_words(t):
            return False
        if (not allow_placeholders) and self._has_placeholders(t):
            return False
        if looks_incomplete_text(t):
            return False
        return True

    def _generate_with_quality_retry(
        self,
        *,
        prompt: str,
        max_tokens: int,
        temperature: float,
        validator: Callable[[str], bool],
        label: str,
        postprocess: Callable[[str], str] | None = None,
    ) -> str:
        attempts = max(1, 1 + self._quality_retries)
        for attempt in range(attempts):
            response = self.client.create_message(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                purpose="generation",
            )
            text = (response or "").strip()
            if postprocess is not None:
                text = postprocess(text)
            if validator(text):
                return text
            if attempt < attempts - 1:
                feedback = []
                if not text:
                    feedback.append("输出为空")
                if self._contains_emoji(text):
                    feedback.append("包含 emoji")
                if self._has_hype_words(text):
                    feedback.append("包含夸张/营销用语")
                if self._has_placeholders(text):
                    feedback.append("包含占位符（如[标题]）")
                if looks_incomplete_text(text):
                    feedback.append("输出不完整，结尾疑似被截断")
                if not feedback:
                    feedback.append("未满足格式/长度要求")
                prompt = "\n".join(
                    [
                        "你是中文技术内容编辑。请严格按要求重写。",
                        f"你正在重写的部分：{label}",
                        "",
                        "上一次输出：",
                        text[:2000],
                        "",
                        "需要修正的问题：",
                        "- " + "\n- ".join(feedback),
                        "",
                        "现在请直接给出新的最终版本（不要解释）。",
                    ]
                )
        raise ValueError(f"{label} failed quality validation after {attempts} attempt(s)")

    def _validate_intro_output(self, text: str) -> bool:
        return self._validate_text(
            text,
            min_chars=80,
            max_chars=220,
            allow_emoji=False,
            allow_hype=False,
            allow_placeholders=False,
        )

    def _validate_comment_output(self, text: str) -> bool:
        return self._validate_text(
            text,
            min_chars=280,
            max_chars=9000,
            allow_emoji=False,
            allow_hype=False,
            allow_placeholders=False,
        )

    def _validate_analysis_output(self, text: str) -> bool:
        return self._validate_text(
            text,
            min_chars=600,
            max_chars=14000,
            allow_emoji=False,
            allow_hype=False,
            allow_placeholders=False,
        )

    def _guard_feedback(self, text: str, *, min_chars: int, max_chars: Optional[int] = None) -> list[str]:
        t = (text or "").strip()
        feedback: list[str] = []
        if not t:
            feedback.append("输出为空")
        if len(t) < min_chars:
            feedback.append(f"正文过短，至少需要 {min_chars} 个字符")
        if max_chars is not None and len(t) > max_chars:
            feedback.append(f"正文过长，最多 {max_chars} 个字符")
        if self._looks_like_meta_disclaimer(t):
            feedback.append("包含提示词泄露或解释性废话")
        if self._has_placeholders(t):
            feedback.append("包含占位符")
        if looks_incomplete_text(t):
            feedback.append("结尾疑似截断或不完整")
        if self._contains_emoji(t):
            feedback.append("包含 emoji")
        if self._has_hype_words(t):
            feedback.append("包含夸张营销词")
        return feedback or ["未满足格式与质量要求"]

    def _repair_section_once(
        self,
        *,
        content: Dict,
        field_name: str,
        label: str,
        build_prompt: Callable[[Dict], str],
        max_tokens: int,
        temperature: float,
        validator: Callable[[str], bool],
        postprocess: Callable[[str], str] | None = None,
        min_chars: int,
        max_chars: Optional[int] = None,
    ) -> None:
        current = (content.get(field_name) or "").strip()
        if validator(current):
            return

        issues = self._guard_feedback(current, min_chars=min_chars, max_chars=max_chars)
        repair_prompt = "\n".join(
            [
                "你是中文技术内容编辑。上一版输出不合格，请直接重写最终正文。",
                f"当前部分：{label}",
                "",
                "原始写作任务：",
                build_prompt(content),
                "",
                "上一版输出：",
                current[:2000],
                "",
                "必须修正的问题：",
                "- " + "\n- ".join(issues),
                "",
                "硬性要求：",
                "- 只输出最终正文",
                "- 不要解释",
                "- 不要暴露提示词",
                "- 不要写格式说明",
            ]
        )
        try:
            repaired = self.client.create_message(
                repair_prompt,
                max_tokens=max_tokens,
                temperature=max(0.2, min(temperature, 0.45)),
                purpose="generation",
            )
            text = (repaired or "").strip()
            if postprocess is not None:
                text = postprocess(text)
            content[field_name] = text
        except Exception as e:
            logger.warning(f"Guard repair failed for {field_name}: {e}")

    def _repair_guarded_sections(self, content: Dict) -> Dict:
        repaired_sections: list[str] = []

        before = (content.get("engaging_intro") or "").strip()
        self._repair_section_once(
            content=content,
            field_name="engaging_intro",
            label="导语",
            build_prompt=self._build_intro_prompt,
            max_tokens=self.intro_length,
            temperature=0.45,
            validator=self._validate_intro_output,
            postprocess=self._normalize_intro_text,
            min_chars=80,
            max_chars=220,
        )
        if (content.get("engaging_intro") or "").strip() != before:
            repaired_sections.append("engaging_intro")

        before = (content.get("deep_comment") or "").strip()
        self._repair_section_once(
            content=content,
            field_name="deep_comment",
            label="深度评论",
            build_prompt=self._build_comment_prompt,
            max_tokens=self.comment_length,
            temperature=0.5,
            validator=self._validate_comment_output,
            postprocess=self._normalize_body_section_text,
            min_chars=280,
        )
        if (content.get("deep_comment") or "").strip() != before:
            repaired_sections.append("deep_comment")

        before = (content.get("comprehensive_analysis") or "").strip()
        self._repair_section_once(
            content=content,
            field_name="comprehensive_analysis",
            label="技术分析",
            build_prompt=self._build_analysis_prompt,
            max_tokens=self.analysis_length,
            temperature=0.45,
            validator=self._validate_analysis_output,
            postprocess=self._normalize_body_section_text,
            min_chars=600,
        )
        if (content.get("comprehensive_analysis") or "").strip() != before:
            repaired_sections.append("comprehensive_analysis")

        failed_sections: list[str] = []
        if not self._validate_intro_output((content.get("engaging_intro") or "").strip()):
            failed_sections.append("engaging_intro")
        if not self._validate_comment_output((content.get("deep_comment") or "").strip()):
            failed_sections.append("deep_comment")
        if not self._validate_analysis_output((content.get("comprehensive_analysis") or "").strip()):
            failed_sections.append("comprehensive_analysis")

        if repaired_sections:
            content["guard_repaired_sections"] = repaired_sections
        if failed_sections:
            content["guard_failed_sections"] = failed_sections
        else:
            content.pop("guard_failed_sections", None)
        return content

    # ============ 基础内容生成（3次调用） ============

    def generate_catchy_title(self, content: Dict) -> str:
        """1. 生成标题"""
        try:
            prompt = self._build_title_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=200,
                temperature=0.4,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=4,
                    max_chars=40,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="标题",
            )
        except Exception as e:
            logger.error(f"Failed to generate catchy title: {e}")
            return content.get('title', '')

    def generate_engaging_intro(self, content: Dict) -> str:
        """2. 生成导语"""
        try:
            prompt = self._build_intro_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=self.intro_length,
                temperature=0.5,
                validator=self._validate_intro_output,
                label="导语",
                postprocess=self._normalize_intro_text,
            )
        except Exception as e:
            logger.error(f"Failed to generate engaging intro: {e}")
            return ""

    def generate_deep_comment(self, content: Dict) -> str:
        """3. 生成深度评论"""
        try:
            prompt = self._build_comment_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=self.comment_length,
                temperature=0.6,
                validator=self._validate_comment_output,
                label="深度评论",
                postprocess=self._normalize_body_section_text,
            )
        except Exception as e:
            logger.error(f"Failed to generate deep comment: {e}")
            return ""

    # ============ 技术深度内容（3次调用） ============

    def generate_comprehensive_analysis(self, content: Dict) -> str:
        """4. 生成全面的技术分析"""
        try:
            prompt = self._build_analysis_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=self.analysis_length,
                temperature=0.55,
                validator=self._validate_analysis_output,
                label="技术分析",
                postprocess=self._normalize_body_section_text,
            )
        except Exception as e:
            logger.error(f"Failed to generate comprehensive analysis: {e}")
            return ""

    def generate_code_examples(self, content: Dict) -> List[Dict]:
        """5. 生成实用代码示例"""
        if not self._generate_code_examples_enabled:
            return []
        try:
            prompt = self._build_code_examples_prompt(content)
            response = self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=1200,
                temperature=0.55,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=160,
                    max_chars=20000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="代码示例",
                postprocess=self._normalize_body_section_text,
            )
            examples = self._parse_code_examples(response)
            if not examples:
                return []
            return examples
        except Exception as e:
            logger.error(f"Failed to generate code examples: {e}")
            return []

    def generate_case_studies(self, content: Dict) -> List[Dict]:
        """6. 生成真实案例研究"""
        if not self._generate_case_studies_enabled:
            return []
        try:
            prompt = self._build_case_studies_prompt(content)
            response = self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=1400,
                temperature=0.6,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=260,
                    max_chars=20000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="案例研究",
                postprocess=self._normalize_body_section_text,
            )
            return self._parse_case_studies(response)
        except Exception as e:
            logger.error(f"Failed to generate case studies: {e}")
            return []

    # ============ 对比和最佳实践（3次调用） ============

    def generate_comparison_analysis(self, content: Dict) -> str:
        """7. 生成与同类方案的对比分析"""
        if not self._generate_comparison_enabled:
            return ""
        try:
            prompt = self._build_comparison_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=900,
                temperature=0.55,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=220,
                    max_chars=16000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="对比分析",
                postprocess=self._normalize_body_section_text,
            )
        except Exception as e:
            logger.error(f"Failed to generate comparison: {e}")
            return ""

    def generate_best_practices(self, content: Dict) -> str:
        """8. 生成最佳实践"""
        if not self._generate_best_practices_enabled:
            return ""
        try:
            prompt = self._build_best_practices_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=1100,
                temperature=0.55,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=260,
                    max_chars=20000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="最佳实践",
                postprocess=self._normalize_body_section_text,
            )
        except Exception as e:
            logger.error(f"Failed to generate best practices: {e}")
            return ""

    def generate_performance_tips(self, content: Dict) -> str:
        """9. 生成性能优化建议"""
        if not self._generate_performance_tips_enabled:
            return ""
        try:
            prompt = self._build_performance_tips_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=900,
                temperature=0.55,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=220,
                    max_chars=16000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="性能优化建议",
                postprocess=self._normalize_body_section_text,
            )
        except Exception as e:
            logger.error(f"Failed to generate performance tips: {e}")
            return ""

    # ============ 学习资源（3次调用） ============

    def generate_learning_takeaways(self, content: Dict) -> List[str]:
        """10. 生成学习要点"""
        try:
            prompt = self._build_takeaways_prompt(content)
            response = self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=450,
                temperature=0.45,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=40,
                    max_chars=2000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="学习要点",
                postprocess=lambda text: self._normalize_section_text(
                    text,
                    wrapper_headings={"学习要点", "关键要点"},
                    demote_headings=False,
                ),
            )
            takeaways = extract_bulleted_items(response, max_items=7)
            return takeaways[:7]  # 最多7个要点
        except Exception as e:
            logger.error(f"Failed to generate learning takeaways: {e}")
            return []

    def generate_practical_recommendations(self, content: Dict) -> str:
        """11. 生成实践建议"""
        if not self._add_recommendations_enabled:
            return ""
        try:
            prompt = self._build_recommendations_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=900,
                temperature=0.55,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=120,
                    max_chars=16000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="实践建议",
                postprocess=self._normalize_body_section_text,
            )
        except Exception as e:
            logger.error(f"Failed to generate practical recommendations: {e}")
            return ""

    def generate_related_resources(self, content: Dict) -> List[Dict]:
        """12. 生成相关资源推荐"""
        if not self._add_recommendations_enabled:
            return []
        try:
            prompt = self._build_resources_prompt(content)
            response = self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=700,
                temperature=0.45,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=140,
                    max_chars=12000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="资源推荐",
                postprocess=self._normalize_body_section_text,
            )
            return filter_related_resources(self._parse_resources(response))
        except Exception as e:
            logger.error(f"Failed to generate related resources: {e}")
            return []

    # ============ 进阶内容（3次调用） ============

    def generate_learning_path(self, content: Dict) -> str:
        """13. 生成学习路径"""
        if not self._generate_learning_path_enabled:
            return ""
        try:
            prompt = self._build_learning_path_prompt(content)
            return self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=1100,
                temperature=0.5,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=260,
                    max_chars=20000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="学习路径",
                postprocess=self._normalize_body_section_text,
            )
        except Exception as e:
            logger.error(f"Failed to generate learning path: {e}")
            return ""

    def generate_faq(self, content: Dict) -> List[Dict]:
        """14. 生成常见问题解答"""
        if not self._generate_faq_enabled:
            return []
        try:
            prompt = self._build_faq_prompt(content)
            response = self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=1100,
                temperature=0.5,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=220,
                    max_chars=20000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="FAQ",
                postprocess=lambda text: self._normalize_section_text(
                    text,
                    wrapper_headings={"常见问题", "常见问题解答", "FAQ"},
                    demote_headings=False,
                ),
            )
            return parse_faq_markdown(response)
        except Exception as e:
            logger.error(f"Failed to generate FAQ: {e}")
            return []

    def generate_challenges(self, content: Dict) -> List[str]:
        """15. 生成挑战和思考题"""
        if not self._generate_challenges_enabled:
            return []
        try:
            prompt = self._build_challenges_prompt(content)
            response = self._generate_with_quality_retry(
                prompt=prompt,
                max_tokens=650,
                temperature=0.5,
                validator=lambda t: self._validate_text(
                    t,
                    min_chars=120,
                    max_chars=8000,
                    allow_emoji=False,
                    allow_hype=False,
                    allow_placeholders=False,
                ),
                label="挑战与思考题",
                postprocess=lambda text: self._normalize_section_text(
                    text,
                    wrapper_headings={"思考题", "挑战与思考题"},
                    demote_headings=False,
                ),
            )
            challenges = [line.strip().lstrip('•-* 123456789.') for line in response.split('\n') if line.strip()]
            return challenges[:5]  # 最多5个挑战
        except Exception as e:
            logger.error(f"Failed to generate challenges: {e}")
            return []

    # ============ Prompt 构建方法 ============

    def _build_title_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        original_title = content.get('title', '')
        description = (content.get("description_translated") or content.get("description") or "").strip()
        language = (content.get("language") or "").strip()
        stars = (content.get("stars") or "").strip()

        context_lines = [
            f"source: {source}",
            f"original_title: {original_title}",
        ]
        if description:
            context_lines.append(f"description: {description[:240]}")
        if language:
            context_lines.append(f"language: {language}")
        if stars:
            context_lines.append(f"stars: {stars}")

        context = "\n".join(context_lines)

        return f"""你是中文科技编辑。请基于给定信息生成一个自然、准确、信息密度高的标题。

硬性规则：
1) 不要使用夸张/营销词（例如：最强、史上、震撼、引爆、颠覆、必看、神器、引人入胜、超级）。
2) 不要在标题里使用 emoji。
3) 不要用“！”或“？”结尾。
4) 标题尽量具体（点出对象+关键能力/主题），不写空泛概念。
5) 控制在 26 个中文字符以内。

只返回标题文本，不要包含引号、编号或其他解释。

输入：
{context}
"""

    def _build_intro_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        deepwiki_excerpt = (content.get('deepwiki_content') or '')[:1200]
        deepwiki_block = f"DeepWiki（节选）：\n{deepwiki_excerpt}" if deepwiki_excerpt.strip() else ""

        if source == 'github_trending':
            return f"""你是中文技术内容编辑。请为读者写一段“导语”（2-4 句），用于介绍这个 GitHub 项目。

写作要求：
1) 语气专业但自然，避免套话与口号式表达。
2) 不要出现“引人入胜/震撼/史上最/必看/神器/爆款”等词。
3) 不要使用 emoji。
4) 结构建议：它是什么；解决什么问题/适合谁；本文会覆盖哪些要点。
5) 控制在 120-180 字。

输入：
项目：{title}
描述：{content.get('description_translated') or content.get('description', '')}
语言：{content.get('language', '')}
星标：{content.get('stars', '')}
{deepwiki_block}

只返回导语文本，不要标题、不要列表。
"""
        elif source in ['hacker_news', 'juejin', 'blogs_podcasts']:
            return f"""你是中文技术内容编辑。请为这篇文章写一段“导语”（2-4 句）。

写作要求：
1) 语气专业但自然，避免套话与口号式表达。
2) 不要出现“引人入胜/震撼/史上最/必看/神器/爆款”等词。
3) 不要使用 emoji。
4) 结构建议：点出主题；说明为什么重要；说明读者能得到什么。
5) 控制在 120-180 字。

输入：
标题：{title}
摘要：{(content.get('description_translated') or content.get('description') or '')[:400]}

只返回导语文本，不要标题、不要列表。
"""
        elif source == 'arxiv':
            return f"""你是中文学术解读编辑。请为这篇论文写一段“导语”（2-4 句）。

写作要求：
1) 语气克制但不生硬，尽量用自然的学术解读口吻。
2) 不要夸大贡献；未知处明确写“无法从摘要确认”。
3) 不要使用 emoji。
4) 结构建议：研究问题；方法/贡献；可能影响的应用/研究方向。
5) 控制在 120-180 字。

输入：
标题：{title}
作者：{', '.join(content.get('authors', [])[:5])}
摘要：{(content.get('summary_translated') or content.get('summary') or '')[:500]}

只返回导语文本，不要标题、不要列表。
"""
        else:
            return f"""你是中文技术内容编辑。请为这条内容写一段“导语”（2-4 句）。

写作要求：
1) 语气专业但自然，避免套话与口号式表达。
2) 不要出现“引人入胜/震撼/史上最/必看/神器/爆款”等词。
3) 不要使用 emoji。
4) 控制在 120-180 字。

输入：
标题：{title}
摘要：{(content.get('description_translated') or content.get('description') or '')[:400]}

只返回导语文本，不要标题、不要列表。
"""

    def _build_comment_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        deepwiki_excerpt = (content.get('deepwiki_content') or '')[:1200]
        deepwiki_block = f"DeepWiki（节选）：\n{deepwiki_excerpt}" if deepwiki_excerpt.strip() else ""
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("评论")

        if source == 'github_trending':
            return f"""你是中文技术内容编辑。请从技术与实用角度写一段评论，控制在{self.comment_length}字以内。

仓库名称：{title}
描述：{content.get('description', '')}
语言：{content.get('language', '')}
星标数：{content.get('stars', '')}
{deepwiki_block}

要求：
- 先给总体判断，再展开依据、适用场景、局限与验证方式。
- 明确区分“事实 / 推断”，不要把猜测写成事实。
- 可以使用三级标题 `###` 组织内容，但不要输出一级、二级标题。
- 不要重复题目或区块名。
- {emoji_rule}
- 用中文写作
- {body_rule}
"""
        elif source in ['hacker_news', 'juejin', 'blogs_podcasts']:
            return f"""你是中文技术内容编辑。请从技术与行业角度写一段评论，控制在{self.comment_length}字以内。

文章标题：{title}
摘要：{content.get('description', '')[:300]}

要求：
- 先概括中心观点，再给出支撑理由、边界条件和实践启发。
- 明确区分“事实陈述 / 作者观点 / 你的推断”。
- 可以使用三级标题 `###`，不要输出一级、二级标题。
- {emoji_rule}
- 用中文写作
- {body_rule}
"""
        elif source == 'arxiv':
            return f"""你是中文学术解读编辑。请从学术与应用角度写一段评论，控制在{self.comment_length}字以内。

论文标题：{title}
作者：{', '.join(content.get('authors', [])[:3])}
摘要：{content.get('summary', '')[:300]}

要求：
- 明确区分：论文声称、证据、你的推断。
- 指出关键假设、潜在失效条件和可验证方式。
- 可以使用三级标题 `###`，不要输出一级、二级标题。
- {emoji_rule}
- 用中文写作
- {body_rule}
"""
        else:
            return f"""请深入评价以下内容，控制在{self.comment_length}字以内：

标题：{title}

要求：
- 多角度深入分析，给出依据与边界条件
- 可以使用三级标题 `###`，不要输出一级、二级标题
- {emoji_rule}
- 用中文写作
- {body_rule}
"""

        return ""

    def _build_analysis_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        deepwiki_excerpt = (content.get('deepwiki_content') or '')[:1500]
        deepwiki_block = f"DeepWiki（节选）：\n{deepwiki_excerpt}" if deepwiki_excerpt.strip() else ""
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("技术分析")

        if source == 'github_trending':
            return f"""你是中文技术分析编辑。请深入分析以下 GitHub 仓库的技术特点和潜在应用，用中文。

仓库名称：{title}
描述：{content.get('description', '')}
语言：{content.get('language', '')}
星标数：{content.get('stars', '')}
{deepwiki_block}

要求：
- 覆盖：架构、核心能力、技术实现、适用与不适用场景、学习与落地建议。
- 明确区分已知事实与基于仓库信息的推断。
- 可以使用三级标题 `###` 和四级标题 `####` 组织内容，但不要输出一级、二级标题。
- {emoji_rule}
- {body_rule}
- 控制在{self.analysis_length}字以内
"""
        elif source in ['hacker_news', 'juejin', 'blogs_podcasts']:
            return f"""你是中文技术分析编辑。请深入分析以下文章的核心观点和技术要点，用中文。

文章标题：{title}
摘要：{content.get('description', '')[:300]}

要求：
- 覆盖：核心观点、关键技术点、实际应用价值、行业影响、边界条件与实践建议。
- 给出论证地图：中心命题、支撑理由、反例或边界条件、可验证方式。
- 可以使用三级标题 `###` 和四级标题 `####`，不要输出一级、二级标题。
- {emoji_rule}
- {body_rule}
- 控制在{self.analysis_length}字以内
"""
        elif source == 'arxiv':
            return f"""你是中文学术解读编辑。请深入分析以下论文的研究内容和贡献，用中文。

论文标题：{title}
作者：{', '.join(content.get('authors', []))}
摘要：{content.get('summary', '')}

要求：
- 覆盖：研究背景、核心方法、理论基础、实验与结果、应用前景、研究启示、相关工作对比。
- 明确哪些内容来自摘要或可确认事实，哪些是你的推断。
- 指出关键假设、潜在失效条件和可证伪方式。
- 可以使用三级标题 `###` 和四级标题 `####`，不要输出一级、二级标题。
- {emoji_rule}
- {body_rule}
- 控制在{self.analysis_length}字以内
"""
        else:
            return f"""请深入分析以下内容，用中文：

标题：{title}

请从技术价值、实用性、创新性等角度进行全面深入分析。
可以使用三级标题 `###` 和四级标题 `####`，不要输出一级、二级标题。
{emoji_rule}
{body_rule}
控制在{self.analysis_length}字以内。
"""

        return ""

    def _build_code_examples_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        body_rule = self._body_only_rule("代码示例")

        return f"""请为以下内容生成 2-3 个实用的代码示例，用中文：

{title}

来源：{source}

要求：
- 代码要完整可运行
- 添加详细的中文注释
- 每个示例解决一个实际问题
- 使用代码块格式
- 每个示例先给一句简短说明，再给代码块
- 不要输出“## 代码示例”等包装标题
- 不要输出示例总标题，只保留正文
- {body_rule}

格式示例：

```python
# 示例 1：XXX功能
def example():
    # 代码实现
    pass
```

**说明**: 这个示例展示了...

```python
# 示例2：XXX功能
def example2():
    # 代码实现
    pass
```

**说明**: 这个示例展示了...

只返回代码示例和说明，不要其他内容。
"""

    def _build_case_studies_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("案例研究")

        return f"""请为以下内容生成 2-3 个真实的应用案例，用中文：

{title}

来源：{source}

要求：
- 案例要真实可信
- 说明背景、问题和解决方案
- 突出实际效果和价值
- 使用 markdown 格式
- 每个案例使用 `### 案例 N：标题`
- 不要输出“## 案例研究”等包装标题
- {emoji_rule}
- {body_rule}

格式示例：

### 案例 1：XX公司/项目

**背景**: ...

**问题**: ...

**解决方案**: 使用XXX工具/技术...

**效果**: ...

---

### 案例 2：XX公司/项目

**背景**: ...

**问题**: ...

**解决方案**: 使用XXX工具/技术...

**效果**: ...

只返回案例内容，不要其他内容。
"""

    def _build_comparison_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("对比分析")

        return f"""请为以下内容生成与同类方案的详细对比分析，用中文：

{title}

来源：{source}

要求：
- 列出 2-3 个同类方案
- 从多个维度进行对比
- 突出优势和不足
- 使用表格或列表格式
- 不要输出“## 与同类方案对比”等包装标题
- {emoji_rule}
- {body_rule}

格式示例：

| 维度 | {title[:10]} | 方案A | 方案B |
|------|------------|--------|--------|
| 性能 | ... | ... | ... |
| 易用性 | ... | ... | ... |
| 成本 | ... | ... | ... |

### 优势分析

- 优势1：...
- 优势2：...

### 不足分析

- 不足1：...
- 不足2：...

只返回对比内容，不要其他内容。
"""

    def _build_best_practices_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("最佳实践")

        return f"""请为以下内容生成最佳实践指南，用中文：

{title}

来源：{source}

要求：
- 列出 5-7 条最佳实践
- 每条实践要有具体说明
- 提供实施建议
- 使用 markdown 格式
- 每条实践使用 `### 实践 N：标题`
- 不要输出“## 最佳实践指南”等包装标题
- {emoji_rule}
- {body_rule}

格式示例：

### 实践 1：[标题]

**说明**: 详细说明...

**实施步骤**:
1. 步骤1
2. 步骤2

**注意事项**: ...

---

### 实践 2：[标题]

**说明**: 详细说明...

**实施步骤**:
1. 步骤1
2. 步骤2

**注意事项**: ...

只返回最佳实践内容，不要其他内容。
"""

    def _build_performance_tips_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("性能优化建议")

        return f"""请为以下内容生成性能优化建议，用中文：

{title}

来源：{source}

要求：
- 列出 4-6 条性能优化建议
- 每条建议要有具体说明
- 提供实施方法
- 量化优化效果（如可能）
- 使用 markdown 格式
- 每条建议使用 `### 优化 N：标题`
- 不要输出“## 性能优化建议”等包装标题
- {emoji_rule}
- {body_rule}

格式示例：

### 优化 1：[标题]

**说明**: 详细说明...

**实施方法**:
1. 方法1
2. 方法2

**预期效果**: 提升XX%

---

### 优化 2：[标题]

**说明**: 详细说明...

**实施方法**:
1. 方法1
2. 方法2

**预期效果**: 提升XX%

只返回性能优化内容，不要其他内容。
"""

    def _build_takeaways_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("学习要点", allow_subsections=False)

        return f"""请总结从以下内容中学到的 5-7 个关键要点，用中文：

{title}

来源：{source}

要求：
- 每个要点用一句话概括
- 突出最有价值的知识点
- 使用 • 开头
- {emoji_rule}
- 按重要性排序
- 不要输出“学习要点”标题或其他包装标题
- {body_rule}

格式示例：
• 要点一（最重要）
• 要点二
• 要点三
• 要点四
• 要点五
"""

    def _build_recommendations_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("实践建议")

        if source == 'github_trending':
            return f"""请为以下 GitHub 仓库提供 5-7 条实践建议，用中文：

仓库名称：{title}
描述：{content.get('description', '')}

要求：
- 针对实际使用场景
- 提供具体可操作的建议
- 包括最佳实践和常见陷阱
- {emoji_rule}
- 可以使用三级标题 `###`
- {body_rule}
"""
        elif source == 'arxiv':
            return f"""请为以下论文提供学习建议，用中文：

论文标题：{title}

要求：
- 适合的学习阶段
- 需要补充的背景知识
- 如何实践和验证
- 学习顺序建议
- {emoji_rule}
- 可以使用三级标题 `###`
- {body_rule}
"""
        else:
            return f"""请为以下内容提供实践建议，用中文：

{title}

要求：
- 提供具体可操作的建议
- {emoji_rule}
- 可以使用三级标题 `###`
- {body_rule}
"""

    def _build_resources_prompt(self, content: Dict) -> str:
        title = content.get('title', '')
        body_rule = self._body_only_rule("相关资源", allow_subsections=False)

        return f"""请推荐 5 个与以下内容相关的优质资源，用中文：

{title}

要求：
- 包括官方文档、教程、工具、博客等
- 资源要有价值和质量保证
- 说明每个资源的特点和适用场景
- 不要输出“相关资源/推荐资源”标题
- {body_rule}
- 格式：
  名称：xxx
  链接：xxx
  说明：xxx

只返回推荐资源，不要其他内容。
"""

    def _build_learning_path_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("学习路径")

        return f"""请为以下内容生成一个循序渐进的学习路径，用中文：

{title}

来源：{source}

要求：
- 从入门到精通分为 3-5 个阶段
- 每个阶段说明学习内容
- 提供学习建议和资源
- 标注每个阶段需要的时间
- {emoji_rule}
- 使用 markdown 格式
- 不要输出“## 学习路径”等包装标题
- 每个阶段使用 `### 阶段 N：标题`
- {body_rule}

格式示例：

### 阶段 1：入门基础

**学习内容**:
- 知识点1
- 知识点2

**学习时间**: 1-2周

**学习资源**:
- 资源1
- 资源2

**学习建议**: ...

---

### 阶段 2：进阶提升

**学习内容**:
- 知识点1
- 知识点2

**学习时间**: 2-4周

**学习资源**:
- 资源1
- 资源2

**学习建议**: ...

只返回学习路径内容，不要其他内容。
"""

    def _build_faq_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("常见问题")

        return f"""请为以下内容生成 5-7 个常见问题和解答，用中文：

{title}

来源：{source}

要求：
- 问题要真实常见
- 回答要详细准确
- 使用 markdown 格式
- 不要输出“## 常见问题”或“## 常见问题解答”标题
- 每个问题使用 `### Q1: 问题`
- 回答部分只写答案正文，不要重复“A:”标题之外的包装段
- {emoji_rule}
- {body_rule}

格式示例：

### Q1: [问题]

**A**: [详细解答]

---

### Q2: [问题]

**A**: [详细解答]

只返回FAQ内容，不要其他内容。
"""

    def _build_challenges_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')
        emoji_rule = "不要使用 emoji"
        body_rule = self._body_only_rule("挑战与思考题")

        return f"""请为以下内容生成 5 个挑战和思考题，用中文：

{title}

来源：{source}

要求：
- 难度递进（从简单到困难）
- 每个挑战都有实践价值
- 提供解答提示（不直接给答案）
- {emoji_rule}
- 不要输出“## 挑战与思考题”标题
- 每个挑战使用 `### 挑战 N：标题`
- {body_rule}

格式示例：

### 挑战 1: [简单]

**问题**: ...

**提示**: ...

---

### 挑战 2: [中等]

**问题**: ...

**提示**: ...

---

只返回挑战内容，不要其他内容。
"""

    # ============ 解析方法 ============

    def _parse_code_examples(self, response: str) -> List[Dict]:
        """解析代码示例响应"""
        examples: List[Dict] = []
        if not response:
            return examples

        lines = response.split('\n')
        current: Dict = {}
        in_code = False

        def flush_current():
            nonlocal current
            if current.get("code"):
                current["code"] = current["code"].strip() + "\n"
                if "description" in current and isinstance(current["description"], str):
                    current["description"] = current["description"].strip()
                examples.append(current)
            current = {}

        for raw in lines:
            line = raw.rstrip("\n")
            stripped = line.strip()

            if stripped.startswith("```"):
                if not in_code:
                    if current.get("code"):
                        flush_current()
                    current["code"] = line + "\n"
                    in_code = True
                else:
                    current["code"] = (current.get("code") or "") + line + "\n"
                    in_code = False
                continue

            if in_code:
                current["code"] = (current.get("code") or "") + line + "\n"
                continue

            if not stripped:
                continue

            if "示例" in stripped or "Example" in stripped:
                if current.get("code"):
                    flush_current()
                continue

            if stripped.startswith("**说明**"):
                desc = stripped.replace("**说明**", "", 1).lstrip(":： ").strip()
                current["description"] = desc
                continue

            if stripped.startswith("说明"):
                desc = stripped.split("说明", 1)[-1].lstrip(":： ").strip()
                current["description"] = desc
                continue

            if "description" not in current:
                current["description"] = stripped
            else:
                current["description"] = f"{current['description']}\n{stripped}"

        if current.get("code"):
            flush_current()

        return examples

    def _parse_case_studies(self, response: str) -> List[Dict]:
        """解析案例研究响应"""
        studies = []
        # 简化解析逻辑
        sections = response.split('### 案例')
        for section in sections[1:]:  # 跳过第一个空section
            study = {'title': section.split('\n')[0].strip()}
            study['content'] = section
            studies.append(study)
        return studies[:3]

    def _parse_resources(self, response: str) -> List[Dict]:
        """解析资源响应"""
        resources = []
        lines = response.split('\n')
        current_resource = {}

        field_pattern = re.compile(
            r"^(名称|title|链接|link|说明)\s*[:：]\s*(.*?)\s*$",
            re.IGNORECASE,
        )

        def flush_current():
            nonlocal current_resource
            if current_resource.get('title') and current_resource.get('link'):
                resources.append(current_resource)
            current_resource = {}

        for line in lines:
            line = line.strip()
            if not line:
                flush_current()
                continue
            match = field_pattern.match(line)
            if not match:
                continue
            field_name, value = match.groups()
            normalized_name = field_name.lower()
            if normalized_name in {'名称', 'title'}:
                flush_current()
                current_resource = {'title': value}
            elif normalized_name in {'链接', 'link'}:
                if current_resource:
                    current_resource['link'] = value
            elif normalized_name == '说明' and current_resource:
                current_resource['description'] = value
        flush_current()
        return resources[:5]

    def _parse_faq(self, response: str) -> List[Dict]:
        """解析FAQ响应"""
        faqs = []
        # 简化解析逻辑
        sections = response.split('### Q')
        for section in sections[1:]:  # 跳过第一个空section
            faq = {'question': section.split('\n')[0].strip()}
            faq['answer'] = section
            faqs.append(faq)
        return faqs[:7]

    # ============ 主处理方法 ============

    def process_content(self, content: Dict) -> Dict:
        """
        处理内容，生成所有增强内容（15次大模型调用）

        Args:
            content: 内容数据

        Returns:
            Dict: 包含所有生成内容的数据
        """
        try:
            logger.info(f"Processing content: {content.get('title', 'Untitled')}")

            # 基础内容（3次调用）
            logger.info("[1/15] Generating title...")
            content['catchy_title'] = self.generate_catchy_title(content)

            logger.info("[2/15] Generating intro...")
            content['engaging_intro'] = self.generate_engaging_intro(content)

            logger.info("[3/15] Generating comment...")
            content['deep_comment'] = self.generate_deep_comment(content)

            # 技术深度内容（3次调用）
            logger.info("[4/15] Generating comprehensive analysis...")
            content['comprehensive_analysis'] = self.generate_comprehensive_analysis(content)

            logger.info("[5/15] Generating code examples...")
            content['code_examples'] = self.generate_code_examples(content)

            logger.info("[6/15] Generating case studies...")
            content['case_studies'] = self.generate_case_studies(content)

            # 对比和最佳实践（3次调用）
            logger.info("[7/15] Generating comparison analysis...")
            content['comparison_analysis'] = self.generate_comparison_analysis(content)

            logger.info("[8/15] Generating best practices...")
            content['best_practices'] = self.generate_best_practices(content)

            logger.info("[9/15] Generating performance tips...")
            content['performance_tips'] = self.generate_performance_tips(content)

            # 学习资源（3次调用）
            logger.info("[10/15] Generating learning takeaways...")
            content['learning_takeaways'] = self.generate_learning_takeaways(content)

            logger.info("[11/15] Generating practical recommendations...")
            content['practical_recommendations'] = self.generate_practical_recommendations(content)

            logger.info("[12/15] Generating related resources...")
            content['related_resources'] = self.generate_related_resources(content)

            # 进阶内容（3次调用）
            logger.info("[13/15] Generating learning path...")
            content['learning_path'] = self.generate_learning_path(content)

            logger.info("[14/15] Generating FAQ...")
            content['faq'] = self.generate_faq(content)

            logger.info("[15/15] Generating challenges...")
            content['challenges'] = self.generate_challenges(content)

            content = self._repair_guarded_sections(content)
            logger.info("Processing completed successfully")
            return content

        except Exception as e:
            logger.error(f"Failed to process content: {e}")
            return content


# 向后兼容的别名
ContentGenerator = SuperEnhancedContentGenerator
EnhancedContentGenerator = SuperEnhancedContentGenerator


if __name__ == '__main__':
    # 测试代码
    from .anthropic_client import AnthropicClient

    client = AnthropicClient()
    config = {
        'intro_length': 500,
        'comment_length': 1200,
        'analysis_length': 2500,
        'use_emoji': False,
        'add_recommendations': True,
        'generate_code_examples': True,
        'generate_case_studies': True,
        'generate_faq': True,
        'generate_comparison': True,
        'generate_best_practices': True,
        'generate_performance_tips': True,
        'generate_learning_path': True,
        'generate_challenges': True,
    }
    generator = SuperEnhancedContentGenerator(client, config)

    test_content = {
        'source': 'github_trending',
        'title': 'test-repo',
        'description': 'A powerful tool for developers with advanced features and intuitive interface',
        'language': 'Python',
        'stars': '1234'
    }

    result = generator.process_content(test_content)

    print(f"Original Title: {test_content['title']}")
    print(f"Catchy Title: {result.get('catchy_title', 'N/A')}")
    print(f"\nEngaging Intro: {result.get('engaging_intro', 'N/A')}")
    print(f"\nDeep Comment: {result.get('deep_comment', 'N/A')}")
    print(f"\nCode Examples: {len(result.get('code_examples', []))} examples")
    print(f"\nCase Studies: {len(result.get('case_studies', []))} studies")
    print(f"\nTotal LLM calls: 15")
