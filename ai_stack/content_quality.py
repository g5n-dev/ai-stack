"""Shared, conservative quality gates for generated historical content."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml

_FRONTMATTER_RE = re.compile(
    r"\A(?:\ufeff)?---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)",
    re.DOTALL,
)
_FRONTMATTER_METADATA_RE = re.compile(
    r"\A(?:\ufeff)?---[ \t]*\r?\n(?P<metadata>.*?)\r?\n---[ \t]*(?:\r?\n|\Z)",
    re.DOTALL,
)

_SYNTHETIC_BODY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "prompt_context_leak",
        re.compile(
            r"(?:您|你)(?:在提示词中)?.{0,16}(?:提供|未提供|没有提供)"
            r".{0,140}(?:标题|摘要|简介|导语|原文|正文|全文|文章内容)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "missing_source_content",
        re.compile(
            r"(?:由于|鉴于|考虑到).{0,40}(?:您|你|用户).{0,20}"
            r"(?:未|没有|并未|无法).{0,30}(?:提供|获取|访问|读取)"
            r".{0,30}(?:原文|正文|完整内容|文章内容)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "missing_source_content",
        re.compile(
            r"(?:无法|未能|不能).{0,20}(?:访问|获取|读取)"
            r".{0,20}(?:原文|正文|完整文章)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "title_only_generation",
        re.compile(
            r"(?:仅|只).{0,10}(?:是|有|为|提供|包含).{0,10}(?:标题|摘要)"
            r".{0,100}(?:推演|推断|推测|猜测|生成|模拟|补全)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "missing_source_content",
        re.compile(
            r"(?:您|你|用户).{0,18}(?:未|没有|并未|无法|不能|没能)"
            r".{0,24}(?:提供|获取|访问|读取|看到).{0,35}"
            r"(?:原文|正文|全文|完整内容|文章内容|详细内容)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "absent_source_inference",
        re.compile(
            r"(?:未获得全文|未见原文全篇|因原文未提供|由于未提供原文|"
            r"鉴于未提供原文|未拿到原文|原文未提供).{0,180}"
            r"(?:基于|结合|根据|推断|推测|推演|重构|还原|生成|构建|"
            r"模拟|评价|分析)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "truncated_source_inference",
        re.compile(
            r"(?:原文|正文|全文|摘要(?:内容)?|文章内容)"
            r"(?:[^。！？!\n]|\n(?!\s*\n)){0,45}"
            r"(?:(?:被|已|似乎|可能)?截断|不完整|未完成)"
            r"(?:[^。！？!\n]|\n(?!\s*\n)){0,180}"
            r"(?:(?:以下|以上)(?:总结|分析|评价)|本(?:分析|评价)|"
            r"我(?:将|只能|无法)|我们(?:将|只能)|"
            r"(?:但|因此|所以).{0,20}(?:只能|仅能)?)"
            r"(?:[^。！？!\n]|\n(?!\s*\n)){0,50}"
            r"(?:基于|结合|根据|推断|推测|推演|重构|还原|构建|"
            r"无法得知|请提供)",
            re.IGNORECASE,
        ),
    ),
    (
        "source_request_leak",
        re.compile(
            r"(?:如果|若|请)(?:您|你).{0,30}(?:提供|补充|发送|粘贴)"
            r".{0,30}(?:完整|具体|详细)?(?:原文|正文|全文|后续内容)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "title_only_generation",
        re.compile(
            r"(?:我将|本文将|以下).{0,30}(?:基于|根据)"
            r".{0,40}(?:标题|有限信息).{0,80}"
            r"(?:推演|推断|推测|猜测|生成|模拟|补全|分析)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "missing_source_content",
        re.compile(
            r"(?:the (?:source|original) (?:article|content) (?:was not|wasn't) provided|"
            r"unable to (?:access|retrieve|read) the (?:source|original) (?:article|content))",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "title_only_generation",
        re.compile(
            r"based only on (?:the )?(?:headline|title).{0,80}"
            r"(?:infer|speculat|generat|simulat)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "model_reasoning_leak",
        re.compile(
            r"\b(?:analy[sz]e|understand)\s+the\s+"
            r"(?:user(?:['’]s)?\s+)?request\s*:\**",
            re.IGNORECASE,
        ),
    ),
)

_FENCE_LINE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<tail>.*)$")
_TRAILING_HEADING_RE = re.compile(r"^#{1,6}(?:[ \t]+.*)?$")
_TRUNCATED_SUFFIX_RE = re.compile(r"[,，:：（(\[{]$")
_PLACEHOLDER_LINE_RE = re.compile(
    r"(?im)^\s*(?:待补充|待完善|暂无内容|内容缺失|TODO|TBD)[。.]?\s*$"
)
_DESCRIPTION_HEADING_RE = re.compile(r"^ {0,3}##[ \t]+描述[ \t]*$")
_DESCRIPTION_INLINE_RE = re.compile(r"^ {0,3}[-+*][ \t]+\*\*描述\*\*[ \t]*[:：]")
_H2_HEADING_RE = re.compile(r"^ {0,3}##(?:[ \t]+|$)")
_TRANSLATION_RESPONSE_RE = re.compile(
    r"(?:"
    r"(?:您好[！!，,\s]*)?(?:"
    r"(?:(?:我)?注意到|我发现).{0,16}(?:您提供的)?"
    r"(?:这段|以下)?(?:内容|文字|文本)|"
    r"您提供的(?:这段|以下)?(?:内容|文字|文本)|"
    r"(?:这段|以下)(?:内容|文字|文本)|这句话"
    r")[ \t*_]*(?:本身)?(?:已经|已|就)?是中文|"
    r"(?:如果|若)您(?:是想|需要|希望).{0,24}"
    r"(?:这段中文|中文(?:内容|文本)?|将其|其).{0,16}翻译成英文"
    r".{0,48}(?:以下是|翻译版本|请告诉我|我可以|请提供)|"
    r"该中文文本.{0,16}(?:已符合要求|无需翻译)"
    r")",
    re.IGNORECASE | re.DOTALL,
)
_HEADING_LINE_RE = re.compile(r"^(?P<marks>#{2,6})[ \t]+\S.*$")
_ATX_H1_LINE_RE = re.compile(r"^ {0,3}#[ \t]+\S.*$")
_SETEXT_H1_UNDERLINE_RE = re.compile(r"^ {0,3}=+[ \t]*$")
_HORIZONTAL_RULE_LINE_RE = re.compile(
    r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$"
)
_TITLE_GENERATION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"基于.{0,24}(?:描述|内容|信息).{0,28}(?:我将|将为您|将)"
        r".{0,20}(?:创建|生成|拟定|推荐|提供).{0,24}(?:中文|文章)?标题",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"请(?:你|您)?(?:根据|基于).{0,24}(?:"
        r"标题.{0,24}(?:生成|创建|拟定|推荐|撰写)|"
        r"(?:描述|内容).{0,24}(?:生成|创建|拟定|推荐|撰写)"
        r".{0,24}(?:中文|文章)?标题)",
        re.IGNORECASE | re.DOTALL,
    ),
)
_RECOMMENDED_TITLE_LINE_RE = re.compile(
    r"(?im)^ {0,3}(?:#{1,6}[ \t]+)?(?:\*{1,2})?推荐标题"
    r"(?:\*{1,2})?[ \t]*[：:]"
)
_RECOMMENDED_TITLE_VALUE_RE = re.compile(r"^\s*推荐标题\s*[：:]", re.IGNORECASE)
_EDITORIAL_META_PREAMBLE_RE = re.compile(
    r"^\s*(?:这里(?:是|有)?(?:一个|一篇)?|这是(?:一个|一篇)?|以下是)"
    r"\s*为(?:你|您).{0,48}(?:撰写|定制|打造|创作|编写|生成)"
    r".{0,48}(?:引言|导语)",
    re.DOTALL,
)
_INTRO_HEADING_RE = re.compile(r"^ {0,3}#{2,6}[ \t]+[^\n]*(?:引言|导语)[^\n]*$")
_CITATION_HEADING_RE = re.compile(r"^ {0,3}##[ \t]+(?:🔗[ \t]*)?(?:引用|来源(?:链接)?)[ \t]*$")
_LIST_ITEM_LINE_RE = re.compile(r"^(?P<indent> {0,3})(?P<marker>[-+*]|\d+[.)])[ \t]+(?P<body>.*)$")
_QA_ANSWER_MARKER_RE = re.compile(r"^(?:\*\*A(?:\*\*[：:]|[：:]\*\*)|A[：:])[ \t]*")
_BARE_MARKDOWN_MARKER_RE = re.compile(r"^[#*_~`>\\-]+$")
_UNESCAPED_STRONG_MARKER_RE = re.compile(r"(?<!\\)\*\*")
_MISPLACED_STRONG_BEFORE_EMOJI_RE = re.compile(
    r"(?:[。！？!?；;]|(?<!\d)\.)[\"'”’」』）)】\]]*"
    r"(?P<marker>(?<!\\)\*\*)(?P<spacing>[ \t]+)"
    r"(?=[\u2600-\u27bf\U0001f300-\U0001faff])"
)
_MISPLACED_LABEL_STRONG_RE = re.compile(
    r"^(?: {0,3}(?:[-+*]|\d+[.)])[ \t]+).{1,48}?"
    r"(?P<marker>(?<!\\)\*\*)"
    r"(?=[ \t]*(?:[\u2600-\u27bf\U0001f300-\U0001faff][\ufe0f\u200d]*)*"
    r"[ \t]*[：:])"
)
_PRE_CITATION_DANGLING_SUFFIX_RE = re.compile(r"[,，、（(\[{/＝=\\-]$")
_PRE_CITATION_NATURAL_END_RE = re.compile(r"[。！？.!?；;）)】\]”’」』…](?:[^\w\u3400-\u9fff]|_)*$")
_SENTENCE_TERMINATION_RE = re.compile(r"[。！？.!?；;](?:[^\w\u3400-\u9fff]|_)*$")
_DESCRIPTION_DANGLING_SUFFIX_RE = re.compile(r"[,，:：、/\\（(\[{=+\-](?:[\"'”’」』）)】\]\s])*$")
_DESCRIPTION_NATURAL_END_RE = re.compile(
    r"(?:[。！？!?；;…]|(?<!\d)\.)(?:[\"'”’」』）)】\]》〉*_~\s]|\ufe0f|"
    r"[\u2600-\u27bf]|[\U0001f300-\U0001faff])*$"
)
_EXPLICIT_TRUNCATION_RE = re.compile(r"\[\s*\.{3}\s*truncated\s*\]", re.IGNORECASE)
_HTTP_SCHEMES = frozenset({"http", "https"})
_SOURCE_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_SOURCE_CAPTURE_MODES = frozenset({"abstract", "excerpt", "metadata_only", "social_post"})
_MAX_MODERN_SOURCE_BRIEF_BODY_BYTES = 192 * 1024
_STANDARD_FOOTER_PREFIXES = (
    "*本文由 AI Stack",
    "*这篇文章由 AI Stack",
    "**📚 更多精彩内容",
)
_CONTENT_QUALITY_MANIFEST_SCHEMA = "content_quality_manifest_v4"


@dataclass(frozen=True, slots=True)
class PostQualityAnalysis:
    """One deterministic Post-level publication decision."""

    status: str
    content_mode: str
    fatal_reasons: tuple[str, ...]
    warning_reasons: tuple[str, ...]


def _prose_without_code(text: str) -> str:
    """Remove fenced and inline code before scanning for assistant language."""

    result: list[str] = []
    open_character: str | None = None
    open_length = 0
    for line in str(text or "").splitlines():
        match = _FENCE_LINE_RE.match(line)
        if match is not None:
            fence = match.group("fence")
            character = fence[0]
            if open_character is None:
                open_character = character
                open_length = len(fence)
            elif (
                character == open_character
                and len(fence) >= open_length
                and not match.group("tail").strip()
            ):
                open_character = None
                open_length = 0
            result.append("")
            continue
        if open_character is not None:
            result.append("")
            continue
        result.append(re.sub(r"`+[^`\n]*`+", " ", line))
    return "\n".join(result)


def _description_sections(prose: str) -> tuple[str, ...]:
    """Return fenced-code-free description sections bounded by sibling H2s."""

    lines = str(prose or "").splitlines()
    sections: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not (_DESCRIPTION_HEADING_RE.fullmatch(line) or _DESCRIPTION_INLINE_RE.match(line)):
            index += 1
            continue

        end = index + 1
        while end < len(lines) and _H2_HEADING_RE.match(lines[end]) is None:
            end += 1
        sections.append("\n".join(lines[index:end]))
        index = end
    return tuple(sections)


def synthetic_body_reasons(body: str) -> tuple[str, ...]:
    """Return deterministic high-confidence reasons for unverifiable synthesis."""
    raw_text = unicodedata.normalize("NFC", str(body or ""))
    if not raw_text.strip():
        return ("empty_body",)
    text = _prose_without_code(raw_text)

    reasons = {reason for reason, pattern in _SYNTHETIC_BODY_PATTERNS if pattern.search(text)}
    if text.casefold().count("</think>") >= 2:
        reasons.add("model_reasoning_leak")
    return tuple(sorted(reasons))


def is_synthetic_body(body: str) -> bool:
    """Return whether the body fails the high-confidence provenance gate."""
    return bool(synthetic_body_reasons(body))


def body_completeness_reasons(body: str) -> tuple[str, ...]:
    """Return high-confidence structural reasons that a body is incomplete.

    Short text is deliberately not a failure signal. A concise source card may
    be complete, while a very long article can still be cut inside a code fence.
    """

    text = unicodedata.normalize("NFC", str(body or ""))
    open_fence_character: str | None = None
    open_fence_length = 0
    for line in text.splitlines():
        match = _FENCE_LINE_RE.match(line)
        if match is None:
            continue
        fence = match.group("fence")
        character = fence[0]
        if open_fence_character is None:
            open_fence_character = character
            open_fence_length = len(fence)
            continue
        if (
            character == open_fence_character
            and len(fence) >= open_fence_length
            and not match.group("tail").strip()
        ):
            open_fence_character = None
            open_fence_length = 0

    reasons: set[str] = set()
    if open_fence_character is not None:
        reasons.add("unclosed_code_fence")

    prose = _prose_without_code(text)
    if "\ufffd" in text:
        reasons.add("encoding_replacement_character")
    if _PLACEHOLDER_LINE_RE.search(prose):
        reasons.add("placeholder_content")

    if any(_TRANSLATION_RESPONSE_RE.search(section) for section in _description_sections(prose)):
        reasons.add("translation_response_leak")

    non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not non_empty_lines:
        return tuple(sorted(reasons))
    final_line = non_empty_lines[-1]
    if (
        _TRAILING_HEADING_RE.fullmatch(final_line)
        or final_line in {"---", "***", "___"}
        or _TRUNCATED_SUFFIX_RE.search(final_line)
    ):
        reasons.add("truncated_ending")
    return tuple(sorted(reasons))


def _empty_section_heading_indexes(body: str) -> tuple[int, ...]:
    """Return empty sibling-heading line indexes, ignoring nested containers."""

    lines = _prose_without_code(body).splitlines()
    indexes: list[int] = []
    for index, line in enumerate(lines):
        heading = _HEADING_LINE_RE.match(line)
        if heading is None:
            continue
        following_index = index + 1
        while following_index < len(lines) and not lines[following_index].strip():
            following_index += 1
        if following_index >= len(lines):
            indexes.append(index)
            continue
        following_heading = _HEADING_LINE_RE.match(lines[following_index])
        if following_heading is None:
            continue
        if len(following_heading.group("marks")) <= len(heading.group("marks")):
            indexes.append(index)
    return tuple(indexes)


def _has_empty_section(body: str) -> bool:
    """Detect empty sibling sections without flagging heading containers."""

    return bool(_empty_section_heading_indexes(body))


def _has_body_h1(body: str) -> bool:
    """Detect rendered H1 headings outside fenced code blocks."""

    lines = _prose_without_code(body).splitlines()
    for index, line in enumerate(lines):
        if _ATX_H1_LINE_RE.match(line):
            return True
        if not _SETEXT_H1_UNDERLINE_RE.fullmatch(line) or index == 0:
            continue
        previous = lines[index - 1]
        if not previous.strip():
            continue
        if re.match(
            r"^ {0,3}(?:#{1,6}(?:[ \t]+|$)|>|(?:[-+*]|\d+[.)])[ \t]+|<)",
            previous,
        ):
            continue
        return True
    return False


def _has_consecutive_horizontal_rules(body: str) -> bool:
    """Detect adjacent thematic breaks while treating code as real content."""

    previous_was_rule = False
    open_character: str | None = None
    open_length = 0
    for line in str(body or "").splitlines():
        fence_match = _FENCE_LINE_RE.match(line)
        if fence_match is not None:
            fence = fence_match.group("fence")
            character = fence[0]
            if open_character is None:
                open_character = character
                open_length = len(fence)
                previous_was_rule = False
            elif (
                character == open_character
                and len(fence) >= open_length
                and not fence_match.group("tail").strip()
            ):
                open_character = None
                open_length = 0
            continue
        if open_character is not None:
            continue
        if not line.strip():
            continue
        is_rule = _HORIZONTAL_RULE_LINE_RE.fullmatch(line) is not None
        if is_rule and previous_was_rule:
            return True
        previous_was_rule = is_rule
    return False


def _has_title_generation_prompt_leak(title: str, body: str) -> bool:
    """Detect high-confidence title-generator instructions outside code."""

    normalized_title = unicodedata.normalize("NFC", str(title or ""))
    prose = _prose_without_code(unicodedata.normalize("NFC", str(body or "")))
    if _RECOMMENDED_TITLE_VALUE_RE.match(normalized_title):
        return True
    if _RECOMMENDED_TITLE_LINE_RE.search(prose):
        return True
    return any(
        pattern.search(candidate)
        for pattern in _TITLE_GENERATION_PATTERNS
        for candidate in (normalized_title, prose)
    )


def _body_intro_openings(body: str) -> tuple[str, ...]:
    """Return only the body opening and named introduction-section openings."""

    lines = _prose_without_code(body).splitlines()
    openings: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped or _HORIZONTAL_RULE_LINE_RE.fullmatch(line):
            continue
        if not re.match(r"^ {0,3}#{1,6}(?:[ \t]+|$)", line):
            openings.append(stripped)
        break

    for index, line in enumerate(lines):
        if _INTRO_HEADING_RE.fullmatch(line) is None:
            continue
        for candidate in lines[index + 1 :]:
            if re.match(r"^ {0,3}#{1,6}(?:[ \t]+|$)", candidate):
                break
            stripped = candidate.strip()
            if not stripped or _HORIZONTAL_RULE_LINE_RE.fullmatch(candidate):
                continue
            openings.append(stripped)
            break
    return tuple(openings)


def _has_editorial_meta_preamble(description: str, body: str) -> bool:
    candidates = (
        unicodedata.normalize("NFC", str(description or "")).lstrip(),
        *_body_intro_openings(body),
    )
    return any(_EDITORIAL_META_PREAMBLE_RE.match(value[:320]) for value in candidates)


def _semantic_lines_before_citation(body: str) -> tuple[tuple[str, str], ...]:
    """Return prose/code markers before the first citation footer heading."""

    prefix: list[str] = []
    open_character: str | None = None
    open_length = 0
    for line in str(body or "").splitlines():
        fence_match = _FENCE_LINE_RE.match(line)
        if fence_match is not None:
            fence = fence_match.group("fence")
            character = fence[0]
            if open_character is None:
                open_character = character
                open_length = len(fence)
            elif (
                character == open_character
                and len(fence) >= open_length
                and not fence_match.group("tail").strip()
            ):
                open_character = None
                open_length = 0
            prefix.append(line)
            continue
        if open_character is None and _CITATION_HEADING_RE.fullmatch(line):
            break
        prefix.append(line)
    else:
        return ()

    semantic: list[tuple[str, str]] = []
    open_character = None
    open_length = 0
    for line in prefix:
        fence_match = _FENCE_LINE_RE.match(line)
        if fence_match is not None:
            fence = fence_match.group("fence")
            character = fence[0]
            if open_character is None:
                open_character = character
                open_length = len(fence)
                semantic.append(("code", ""))
            elif (
                character == open_character
                and len(fence) >= open_length
                and not fence_match.group("tail").strip()
            ):
                open_character = None
                open_length = 0
            continue
        if open_character is not None:
            continue
        if not line.strip() or _HORIZONTAL_RULE_LINE_RE.fullmatch(line):
            continue
        semantic.append(("text", line.rstrip()))
    return tuple(semantic)


def _has_unclosed_markdown_emphasis(line: str) -> bool:
    text = re.sub(r"\\([*_])", "", str(line or ""))
    text = re.sub(r"(?<=\d)\*{1,2}(?=\d)", "", text)

    strong_stars = len(re.findall(r"(?<!\\)\*\*", text))
    if strong_stars % 2:
        return True
    without_strong_stars = re.sub(r"(?<!\\)\*\*", "", text)
    single_stars = len(
        re.findall(
            r"(?<!\\)\*(?=\S)|(?<=\S)(?<!\\)\*",
            without_strong_stars,
        )
    )
    if single_stars % 2:
        return True

    strong_underscores = len(re.findall(r"(?<![\w\\])__(?=\S)|(?<=\S)__(?!\w)", text))
    if strong_underscores % 2:
        return True
    without_strong_underscores = re.sub(r"(?<![\w\\])__(?=\S)|(?<=\S)__(?!\w)", "", text)
    single_underscores = len(
        re.findall(
            r"(?<![\w\\])_(?=\S)|(?<=\S)_(?!\w)",
            without_strong_underscores,
        )
    )
    return single_underscores % 2 == 1


def _without_closed_inline_code(line: str) -> str:
    return re.sub(r"(?<!\\)`+[^`\n]*`+", "", str(line or ""))


def _has_unbalanced_inline_code(line: str) -> bool:
    return len(re.findall(r"(?<!\\)`", str(line or ""))) % 2 == 1


def _has_unbalanced_bracket(line: str) -> bool:
    text = _without_closed_inline_code(line)
    return any(
        text.count(opening) > text.count(closing)
        for opening, closing in (("(", ")"), ("（", "）"), ("[", "]"), ("【", "】"))
    )


def _nearest_section_lines(
    semantic: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    for index in range(len(semantic) - 2, -1, -1):
        kind, value = semantic[index]
        if kind == "text" and re.match(r"^ {0,3}#{2,6}(?:[ \t]+|$)", value):
            return semantic[index:]
    return semantic


def _has_explicit_qa_context(semantic: list[tuple[str, str]], tail: str) -> bool:
    if _QA_ANSWER_MARKER_RE.match(tail):
        return True
    section = _nearest_section_lines(semantic)
    if any(kind == "text" and _QA_ANSWER_MARKER_RE.match(value.strip()) for kind, value in section):
        return True
    if section and section[0][0] == "text":
        heading = section[0][1]
        if re.match(r"^ {0,3}#{2,6}[ \t]+", heading) and re.search(r"[?？]", heading):
            return True
    return False


def _is_repeated_question_without_answer(semantic: list[tuple[str, str]], tail: str) -> bool:
    normalized_tail = re.sub(r"\s+", "", tail)
    for kind, value in reversed(semantic[:-1]):
        if kind != "text":
            continue
        heading = re.match(r"^ {0,3}#{2,6}[ \t]+(?P<text>.+?)\s*$", value)
        if heading is None:
            continue
        normalized_heading = re.sub(r"\s+", "", heading.group("text"))
        return normalized_tail == normalized_heading
    return False


def _is_answer_fragment(tail: str) -> bool:
    marker = _QA_ANSWER_MARKER_RE.match(tail)
    if marker is None:
        return False
    answer = re.sub(r"[*_`]+", "", tail[marker.end() :]).strip()
    characters = re.findall(r"[A-Za-z0-9\u3400-\u9fff]", answer)
    return bool(characters) and len(characters) <= 3 and not _SENTENCE_TERMINATION_RE.search(answer)


def remove_misplaced_strong_markers(line: str) -> str:
    """Remove provably orphaned ``**`` markers from one Markdown list line."""

    cleaned = str(line or "")
    if _LIST_ITEM_LINE_RE.match(cleaned) is None:
        return cleaned
    offset = 0
    while match := _MISPLACED_STRONG_BEFORE_EMOJI_RE.search(cleaned, offset):
        marker_start, marker_end = match.span("marker")
        markers_before = _UNESCAPED_STRONG_MARKER_RE.findall(cleaned[:marker_start])
        if len(markers_before) % 2:
            offset = marker_end
            continue
        cleaned = cleaned[:marker_start] + cleaned[marker_end:]
        offset = marker_start
    markers = tuple(_UNESCAPED_STRONG_MARKER_RE.finditer(cleaned))
    if len(markers) == 1 and (match := _MISPLACED_LABEL_STRONG_RE.match(cleaned)):
        marker_start, marker_end = match.span("marker")
        cleaned = cleaned[:marker_start] + cleaned[marker_end:]
    return cleaned


def _has_truncated_pre_citation_tail(metadata: Mapping[str, Any], body: str) -> bool:
    if str(metadata.get("entry_kind") or "").strip().casefold() != "auto":
        return False
    if str(metadata.get("content_mode") or "").strip().casefold() != "legacy_analysis":
        return False

    semantic = list(_semantic_lines_before_citation(body))
    while (
        semantic
        and semantic[-1][0] == "text"
        and semantic[-1][1].startswith(_STANDARD_FOOTER_PREFIXES)
    ):
        semantic.pop()
    if not semantic or semantic[-1][0] == "code":
        return False
    tail = semantic[-1][1].strip()
    if not tail:
        return False
    tail = remove_misplaced_strong_markers(tail)
    if re.search(r"\]\([^)]*\)$", tail) or re.fullmatch(r"https?://\S+", tail):
        return False
    if _BARE_MARKDOWN_MARKER_RE.fullmatch(tail):
        return True
    if re.match(r"^ {0,3}#{1,6}(?:[ \t]+|$)", tail):
        return True
    if _PRE_CITATION_NATURAL_END_RE.search(tail):
        return False

    without_inline_code = _without_closed_inline_code(tail)
    if _has_unbalanced_inline_code(tail):
        return True
    if _has_unclosed_markdown_emphasis(without_inline_code):
        return True
    if _has_unbalanced_bracket(tail):
        return True

    plain = re.sub(r"[*_`]+$", "", without_inline_code).strip()
    if _PRE_CITATION_DANGLING_SUFFIX_RE.search(plain):
        return True
    qa_context = _has_explicit_qa_context(semantic, tail)
    tail_match = _LIST_ITEM_LINE_RE.match(semantic[-1][1])
    if plain.endswith((":", "：")):
        if not qa_context or tail_match is not None:
            return True
        return False
    if _is_answer_fragment(tail):
        return True
    if _is_repeated_question_without_answer(semantic, tail):
        return True
    if tail_match is not None:
        return False
    if tail.startswith(">"):
        return False
    if _PRE_CITATION_NATURAL_END_RE.search(plain):
        return False
    return False


def description_is_truncated(value: object) -> bool:
    """Detect high-confidence mechanical truncation in a post description."""

    if not isinstance(value, str):
        return False
    text = unicodedata.normalize("NFC", value).strip()
    if not text:
        return False
    if _DESCRIPTION_DANGLING_SUFFIX_RE.search(text):
        return True
    return len(text) in {159, 160} and _DESCRIPTION_NATURAL_END_RE.search(text) is None


def remove_empty_section_headings(body: str) -> tuple[str, int]:
    """Remove empty shell headings without generating replacement prose."""

    cleaned = str(body or "")
    removed = 0
    while True:
        indexes = set(_empty_section_heading_indexes(cleaned))
        if not indexes:
            return cleaned, removed
        lines = cleaned.splitlines(keepends=True)
        cleaned = "".join(line for index, line in enumerate(lines) if index not in indexes)
        removed += len(indexes)


def content_quality_reasons(body: str) -> tuple[str, ...]:
    """Return deterministic provenance and structural completeness failures."""

    return tuple(
        sorted(
            {
                *synthetic_body_reasons(body),
                *body_completeness_reasons(body),
            }
        )
    )


def markdown_body(document: str) -> str:
    """Return Markdown body without interpreting untrusted frontmatter as content."""
    text = str(document or "")
    match = _FRONTMATTER_RE.match(text)
    return text[match.end() :].lstrip("\r\n") if match else text


def markdown_frontmatter(document: str) -> dict[str, Any]:
    """Return a conservative frontmatter mapping without interpreting the body."""
    match = _FRONTMATTER_METADATA_RE.match(str(document or ""))
    if match is None:
        return {}
    try:
        parsed = yaml.safe_load(match.group("metadata")) or {}
    except yaml.YAMLError:
        return {}
    if not isinstance(parsed, Mapping):
        return {}
    return {str(key): value for key, value in parsed.items()}


def is_source_brief(metadata: Mapping[str, Any], body: str) -> bool:
    """Return whether a safe post satisfies the structural source-card contract."""

    source = str(metadata.get("source") or "").strip().casefold()
    declared_mode = str(metadata.get("content_mode") or "").strip().casefold()
    if declared_mode == "source_brief":
        source_is_truncated = metadata.get("source_is_truncated")
        truncation_reason = str(
            metadata.get("source_truncation_reason") or ""
        ).strip()
        modern_provenance = (
            str(metadata.get("publication_tier") or "").strip() == "C"
            and str(metadata.get("source_capture_mode") or "").strip() in _SOURCE_CAPTURE_MODES
            and bool(
                _SOURCE_DIGEST_RE.fullmatch(
                    str(metadata.get("source_snapshot_sha256") or "").strip()
                )
            )
            and str(metadata.get("extractor_version") or "").strip() == "source-contract-v1"
            and bool(str(metadata.get("discovery_method") or "").strip())
            and isinstance(source_is_truncated, bool)
            and bool(truncation_reason) is source_is_truncated
            and metadata.get("source_support") == 1.0
        )
        if not modern_provenance:
            return False
    elif declared_mode == "legacy_source_brief":
        if not (
            source == "hacker_news"
            and metadata.get("entry_kind") == "auto"
            and metadata.get("source_provenance") == "legacy_no_snapshot"
            and metadata.get("source_support") == 0.0
        ):
            return False
    else:
        if source != "hacker_news" or metadata.get("entry_kind") != "auto":
            return False
    external_url = metadata.get("external_url")
    if not isinstance(external_url, str):
        return False
    parsed = urlsplit(external_url.strip())
    if parsed.scheme.casefold() not in _HTTP_SCHEMES or not parsed.hostname:
        return False
    text = str(body or "")
    maximum_bytes = (
        _MAX_MODERN_SOURCE_BRIEF_BODY_BYTES
        if declared_mode == "source_brief"
        else 1_200
    )
    if len(text.encode("utf-8")) >= maximum_bytes:
        return False
    basic = re.search(
        r"(?ms)^##\s+基本信息\s*$\n(?P<section>.*?)(?=^##\s+|\Z)",
        text,
    )
    if basic is None or not basic.group("section").strip():
        return False
    narrative_lines = [
        line.strip()
        for line in _prose_without_code(text).splitlines()
        if line.strip()
        and not line.lstrip().startswith(("#", "-", "*", ">"))
        and line.strip() not in {"---", "***", "___"}
    ]
    return any(len(re.sub(r"\s+", "", line)) >= 12 for line in narrative_lines)


def analyze_post(document: str) -> PostQualityAnalysis:
    """Analyze one complete Markdown document through the shared Post gate."""

    metadata = markdown_frontmatter(document)
    body = markdown_body(document)
    if metadata.get("archived") is True:
        return PostQualityAnalysis("archived", "archived", (), ())

    fatal = set(content_quality_reasons(body))
    title = str(metadata.get("title") or "").strip()
    if not title:
        fatal.add("missing_title")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        fatal.add("missing_description")
    else:
        if _TRANSLATION_RESPONSE_RE.search(unicodedata.normalize("NFC", description)):
            fatal.add("translation_response_leak")
        if description_is_truncated(description):
            fatal.add("truncated_description")
    if _has_editorial_meta_preamble(description if isinstance(description, str) else "", body):
        fatal.add("editorial_meta_preamble")
    if _has_body_h1(body):
        fatal.add("body_h1_heading")
    if _has_consecutive_horizontal_rules(body):
        fatal.add("consecutive_horizontal_rules")
    if _has_title_generation_prompt_leak(title, body):
        fatal.add("title_generation_prompt_leak")

    source_brief = is_source_brief(metadata, body)
    declared_mode = str(metadata.get("content_mode") or "").strip().casefold()
    entry_kind = str(metadata.get("entry_kind") or "").strip().casefold()
    substantive_length = len(re.sub(r"\s+", "", _prose_without_code(body)))
    if entry_kind == "auto" and not source_brief and substantive_length < 80:
        fatal.add("insufficient_substantive_content")
    if declared_mode == "source_brief" and not source_brief:
        fatal.add("invalid_source_brief")
    if declared_mode == "legacy_source_brief" and not source_brief:
        fatal.add("invalid_source_brief")
    if entry_kind == "auto" and not declared_mode:
        fatal.add("missing_source_contract")
    if _has_truncated_pre_citation_tail(metadata, body):
        fatal.add("truncated_pre_citation_tail")

    warnings: set[str] = set()
    if _has_empty_section(body):
        warnings.add("empty_section")
    if _EXPLICIT_TRUNCATION_RE.search(_prose_without_code(body)):
        warnings.add("source_excerpt_truncated")
    if metadata.get("source_is_truncated") is True:
        warnings.add("source_excerpt_truncated")
    if entry_kind == "auto" and not declared_mode and not source_brief:
        warnings.add("legacy_source_snapshot_unavailable")

    if fatal:
        warnings.clear()

    if fatal:
        status = "quarantined"
    elif source_brief:
        status = "source_brief"
    elif declared_mode == "legacy_analysis" or (entry_kind == "auto" and not declared_mode):
        status = "legacy_analysis"
    else:
        status = "complete"
    content_mode = declared_mode or ("source_brief" if source_brief else status)
    return PostQualityAnalysis(
        status=status,
        content_mode=content_mode,
        fatal_reasons=tuple(sorted(fatal)),
        warning_reasons=tuple(sorted(warnings)),
    )


def build_content_quality_manifest(content_root: Path | str) -> dict[str, Any]:
    """Build a deterministic Hugo data manifest for quarantined archive pages."""
    root = Path(content_root).resolve()
    pages: dict[str, dict[str, Any]] = {}
    reason_counts: Counter[str] = Counter()
    source_hash = hashlib.sha256()
    source_file_count = 0
    quarantined_count = 0
    archived_count = 0
    source_brief_count = 0
    complete_count = 0
    legacy_analysis_count = 0
    warning_counts: Counter[str] = Counter()

    for path in sorted(root.rglob("*.md"), key=lambda item: item.as_posix()):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root)
        if not relative_path.parts or relative_path.parts[0] != "posts":
            continue
        relative = relative_path.as_posix()
        payload = path.read_bytes()
        source_file_count += 1
        source_hash.update(relative.encode("utf-8"))
        source_hash.update(b"\0")
        source_hash.update(hashlib.sha256(payload).digest())

        document = payload.decode("utf-8", errors="replace")
        metadata = markdown_frontmatter(document)
        status: str
        reasons: tuple[str, ...]
        warnings: tuple[str, ...]
        if metadata.get("archived") is True:
            status = "archived"
            reasons = ("archived_content",)
            warnings = ()
            archived_count += 1
        else:
            analysis = analyze_post(document)
            status = analysis.status
            reasons = analysis.fatal_reasons
            warnings = analysis.warning_reasons
            warning_counts.update(warnings)
            if status == "quarantined":
                quarantined_count += 1
            elif status == "source_brief":
                reasons = ("concise_source_card",)
                source_brief_count += 1
            elif status == "legacy_analysis":
                legacy_analysis_count += 1
            else:
                complete_count += 1
        if not reasons and not warnings and status == "complete":
            continue
        if status != "source_brief":
            reason_counts.update(reasons)
        pages[relative] = {
            "status": status,
            "reasons": list(reasons),
            **({"warnings": list(warnings)} if warnings else {}),
        }

    return {
        "schema_version": _CONTENT_QUALITY_MANIFEST_SCHEMA,
        "source_tree_sha256": source_hash.hexdigest(),
        "source_file_count": source_file_count,
        "active_count": complete_count + source_brief_count + legacy_analysis_count,
        "complete_count": complete_count,
        "source_brief_count": source_brief_count,
        "legacy_analysis_count": legacy_analysis_count,
        "quarantined_count": quarantined_count,
        "archived_count": archived_count,
        "reason_counts": dict(sorted(reason_counts.items())),
        "warning_counts": dict(sorted(warning_counts.items())),
        "pages": pages,
    }


def write_content_quality_manifest(
    content_root: Path | str,
    output_path: Path | str,
) -> dict[str, Any]:
    """Atomically write the deterministic content-quality manifest."""
    manifest = build_content_quality_manifest(content_root)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(f"{output.suffix}.tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(output)
    return manifest
