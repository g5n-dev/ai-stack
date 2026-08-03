"""Editorial readings of bounded source evidence, for captures without a full text.

A source brief records what the crawler saved and nothing more, which leaves a
reader unable to tell whether the linked work is worth opening.  This module
adds a short reading of that evidence — what the work is, where it applies, and
what can be inferred — under rules that make invention detectable rather than
merely discouraged:

* only prose captures (an abstract or an excerpt) are eligible at all, because
  nothing honest can be said about a bare title;
* the depth allowed scales with how much evidence exists, so a two-sentence
  excerpt cannot justify a speculation section;
* every Arabic number and every Latin identifier in the reading must already
  appear in the evidence, which is what catches an invented benchmark score or
  a model name the source never mentions;
* the reading may not narrate its own limitations, because that phrasing is how
  a model signals it is working past the end of its evidence.

Any failure returns the original source brief unchanged.  A thinner card is a
better outcome than a confident one that cannot be checked.
"""

from __future__ import annotations

import html
import logging
import re
import unicodedata
from collections.abc import Mapping
from typing import Any, Protocol

from ai_stack.content_quality import synthetic_body_reasons
from ai_stack.source_contract import (
    INTERPRETABLE_CAPTURE_MODES,
    SourceContractError,
    promote_interpreted_brief,
)

logger = logging.getLogger(__name__)

WHAT_HEADING = "这是什么"
WHERE_HEADING = "用在哪里"
INFERENCE_HEADING = "可以推断的"
INFERENCE_PREFIX = "推测："

# Below this there is not enough prose to say anything a title would not.
_MIN_EVIDENCE_CHARS = 200
# Speculation requires evidence substantial enough to reason from.
_INFERENCE_EVIDENCE_CHARS = 500
_MAX_INTERPRETATION_CHARS = 600
_INTERPRETATION_CHARS_PER_EVIDENCE_CHAR = 0.55
_MAX_EVIDENCE_PROMPT_CHARS = 6_000
# Shorter than the Tier-B rewriter's window: the evidence itself is short here,
# so a long shared run means the reading is republishing rather than reading.
_MAX_VERBATIM_RUN = 30

# Phrases in which a model narrates its own missing context.  These are also
# what ``synthetic_body_reasons`` quarantines, so producing them wastes a call.
_META_NARRATION_RE = re.compile(
    r"原文|全文|正文|摘要|标题|节选|未提供|没有提供|无法获取|无法访问|提示词|上下文|截断|本文将|以下内容"
)
_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
_LATIN_RE = re.compile(r"[A-Za-z][A-Za-z0-9+#.\-]*")
# Generic technical vocabulary a Chinese reading may use without the source
# having named it.  Anything outside this set must be traceable to the evidence.
_GENERIC_LATIN = frozenset(
    {
        "agent",
        "agents",
        "ai",
        "api",
        "apis",
        "app",
        "cli",
        "cpu",
        "gpu",
        "http",
        "https",
        "llm",
        "llms",
        "ml",
        "rag",
        "sdk",
        "token",
        "tokens",
        "ui",
        "web",
    }
)


class _MessageClient(Protocol):
    def create_message(
        self,
        prompt: str,
        max_tokens: int | None = ...,
        *,
        temperature: float | None = ...,
        purpose: str = ...,
    ) -> str: ...


def _normalized_overlap_text(value: object) -> str:
    text = html.unescape(unicodedata.normalize("NFKC", str(value or "")))
    text = "".join(character for character in text if unicodedata.category(character) != "Cf")
    text = re.sub(r"[`*_>#\[\](){}|\-]", "", text)
    return re.sub(r"\s+", "", text).casefold()


def _contains_verbatim_run(source: str, candidate: str, *, window: int = _MAX_VERBATIM_RUN) -> bool:
    source_text = _normalized_overlap_text(source)
    candidate_text = _normalized_overlap_text(candidate)
    if len(source_text) < window or len(candidate_text) < window:
        return False
    return any(
        candidate_text[index : index + window] in source_text
        for index in range(0, len(candidate_text) - window + 1)
    )


def _evidence_text(item: Mapping[str, Any]) -> str:
    """Return the captured prose a reading may draw on, excluding the title."""

    for key in ("source_display_excerpt", "source_text_original", "source_summary_original"):
        value = str(item.get(key) or "").strip()
        if value:
            return value
    return ""


def _compact(value: str) -> str:
    return re.sub(r"\s+", "", str(value or ""))


def _prose_only(value: str) -> str:
    """Strip Markdown scaffolding so checks see the words, not the structure."""

    text = re.sub(r"(?m)^#{1,6}\s*", "", str(value or ""))
    text = re.sub(r"(?m)^\s*[-*+]\s+", "", text)
    text = re.sub(r"(?m)^\s*\d+[.)]\s+", "", text)
    return text


class SourceInterpreter:
    """Promote eligible source briefs to Tier-C+ readings of their evidence."""

    def __init__(self, client: _MessageClient | None, *, enabled: bool = True):
        self.client = client
        self.enabled = bool(enabled and client is not None)

    @staticmethod
    def depth_for(item: Mapping[str, Any]) -> str:
        """Return ``skip``, ``framing`` or ``full`` for one candidate."""

        if str(item.get("content_mode") or "") != "source_brief":
            return "skip"
        if str(item.get("source_capture_mode") or "") not in INTERPRETABLE_CAPTURE_MODES:
            return "skip"
        evidence_chars = len(_compact(_evidence_text(item)))
        if evidence_chars < _MIN_EVIDENCE_CHARS:
            return "skip"
        return "full" if evidence_chars >= _INFERENCE_EVIDENCE_CHARS else "framing"

    @staticmethod
    def _budget(evidence_chars: int) -> int:
        return min(
            _MAX_INTERPRETATION_CHARS,
            int(evidence_chars * _INTERPRETATION_CHARS_PER_EVIDENCE_CHAR),
        )

    @classmethod
    def _prompt(cls, item: Mapping[str, Any], *, depth: str, budget: int) -> str:
        evidence = _evidence_text(item)[:_MAX_EVIDENCE_PROMPT_CHARS]
        title = str(item.get("source_display_title") or item.get("title") or "").strip()
        source = str(item.get("source") or "").strip()
        sections = [
            f"### {WHAT_HEADING}",
            f"### {WHERE_HEADING}",
        ]
        if depth == "full":
            sections.append(f"### {INFERENCE_HEADING}")
        layout = "\n".join(sections)
        inference_rule = (
            f"- 「{INFERENCE_HEADING}」写 1-2 条，每条以「{INFERENCE_PREFIX}」开头，"
            "只能是基于领域常识的判断，不得写成既定事实。\n"
            if depth == "full"
            else ""
        )
        return f"""你是 AI Stack 的技术编辑。下面是一条已保存的来源记录。
请据此写一段简短解读，帮助读者判断这条内容是否值得点开。

来源：{source}
标题：{title}
已保存的内容：
{evidence}

写作要求：
- 使用简体中文，直接输出 Markdown，只包含下列小节，不要写标题以外的任何前言或结语：
{layout}
- 「{WHAT_HEADING}」用 1-2 句说明这条内容讲的是什么。
- 「{WHERE_HEADING}」用 1-2 句说明它适用于什么场景或什么人会用到。
{inference_rule}- 全部内容不超过 {budget} 字。
- 只能使用上面已保存内容里出现的事实。禁止引入其中没有的数字、比例、产品名、模型名、机构名或结论。
- 不确定的地方就不写，不要猜测具体细节。
- 不得整句照抄上面的内容，用你自己的话表达。
- 不要提及你掌握的信息是否完整。
- 不要出现「原文」「全文」「摘要」「标题」「未提供」「无法获取」这类字样。"""

    @classmethod
    def _validate(cls, item: Mapping[str, Any], *, body: str, depth: str, budget: int) -> None:
        text = str(body or "").strip()
        if not text:
            raise ValueError("interpretation is empty")
        if len(_compact(text)) > budget:
            raise ValueError("interpretation exceeds its evidence-scaled budget")
        if re.search(r"(?m)^#\s", text) or re.search(r"(?m)^##\s", text):
            raise ValueError("interpretation must not introduce top-level headings")
        # The reading is rendered as Markdown without escaping, so it must not
        # be able to inject raw markup or Hugo template syntax into the page.
        if "<" in text or ">" in text.replace("> ", ""):
            raise ValueError("interpretation contains raw markup")
        if "{{" in text or "}}" in text:
            raise ValueError("interpretation contains template syntax")
        if "](" in text or "http://" in text or "https://" in text:
            raise ValueError("interpretation must not introduce links")
        required = [WHAT_HEADING, WHERE_HEADING]
        if depth == "full":
            required.append(INFERENCE_HEADING)
        for heading in required:
            if not re.search(rf"(?m)^###[ \t]+{re.escape(heading)}[ \t]*$", text):
                raise ValueError(f"interpretation is missing section: {heading}")
        if depth != "full" and INFERENCE_HEADING in text:
            raise ValueError("interpretation speculates beyond its evidence budget")
        if depth == "full":
            block = text.split(f"### {INFERENCE_HEADING}", 1)[1]
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if not lines:
                raise ValueError("interpretation has an empty inference section")
            for line in lines:
                if not line.lstrip("-*+ ").startswith(INFERENCE_PREFIX):
                    raise ValueError("every inference must be marked as speculation")

        prose = _prose_only(text)
        if _META_NARRATION_RE.search(prose):
            raise ValueError("interpretation narrates its own missing context")
        reasons = synthetic_body_reasons(prose)
        if reasons:
            raise ValueError(f"interpretation looks synthetic: {', '.join(sorted(reasons))}")

        evidence = _evidence_text(item)
        title = str(item.get("source_display_title") or item.get("title") or "")
        grounding = f"{evidence}\n{title}"
        evidence_numbers = set(_NUMBER_RE.findall(grounding))
        for number in _NUMBER_RE.findall(prose):
            if number not in evidence_numbers:
                raise ValueError(f"interpretation introduces an unsupported number: {number}")
        grounding_latin = {value.casefold() for value in _LATIN_RE.findall(grounding)}
        for word in _LATIN_RE.findall(prose):
            folded = word.casefold()
            if folded in _GENERIC_LATIN or folded in grounding_latin:
                continue
            raise ValueError(f"interpretation introduces an unsupported name: {word}")
        if _contains_verbatim_run(evidence, text):
            raise ValueError("interpretation republishes the evidence verbatim")

    def interpret(self, item: Mapping[str, Any]) -> dict[str, Any]:
        """Return an interpreted brief, or the unchanged item if anything fails."""

        original = dict(item)
        depth = self.depth_for(original)
        if not self.enabled or depth == "skip":
            return original
        evidence_chars = len(_compact(_evidence_text(original)))
        budget = self._budget(evidence_chars)
        title = str(original.get("title") or "")
        try:
            raw = self.client.create_message(  # type: ignore[union-attr]
                self._prompt(original, depth=depth, budget=budget),
                max_tokens=900,
                temperature=0.2,
                purpose="generation",
            )
        except Exception as exc:  # noqa: BLE001 - a reading is always optional
            logger.warning("Interpretation unavailable; keeping the source brief: %s (%s)",
                           title, exc)
            return original
        body = str(raw or "").strip()
        try:
            self._validate(original, body=body, depth=depth, budget=budget)
            promoted = promote_interpreted_brief(original, body)
        except (ValueError, SourceContractError) as exc:
            logger.warning("Interpretation rejected; keeping the source brief: %s (%s)",
                           title, exc)
            return original
        logger.info("Interpretation attached: depth=%s evidence_chars=%s title=%s",
                    depth, evidence_chars, title)
        return promoted


__all__ = [
    "INFERENCE_HEADING",
    "INFERENCE_PREFIX",
    "SourceInterpreter",
    "WHAT_HEADING",
    "WHERE_HEADING",
]
