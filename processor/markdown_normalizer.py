"""
Markdown normalization helpers for generated content and post repair.
"""

from __future__ import annotations

from typing import Iterable
import re


DEFAULT_WRAPPER_HEADINGS = {
    "导语",
    "摘要",
    "摘要简介",
    "摘要/简介",
    "评论",
    "深度评论",
    "技术分析",
    "深度分析",
    "研究最佳实践",
    "最佳实践",
    "最佳实践指南",
    "性能优化建议",
    "学习要点",
    "学习路径",
    "常见问题",
    "常见问题解答",
    "faq",
    "对比分析",
    "与同类方案对比",
    "相关资源",
    "推荐资源",
    "代码示例",
    "案例研究",
    "实践建议",
    "描述",
    "思考题",
    "挑战与思考题",
}

PROMPT_LEAK_KEYWORDS = {
    "只返回",
    "只输出",
    "不要其他内容",
    "使用markdown格式",
    "评价对象",
    "评价视角",
    "字数控制",
    "输出要求",
    "结构要求",
    "格式要求",
    "写作要求",
    "请提供您想要",
    "我才能根据",
}

_PLACEHOLDER_PATTERNS = (
    re.compile(r"\[(标题|问题|详细解答|说明|简单|中等|困难)\]"),
    re.compile(r"^\s*(?:标题|问题|提示|说明)\s*[:：]\s*\.\.\.\s*$"),
)
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_REPEATED_HEADING_RE = re.compile(r"^(#{1,6})(?:\s+#{1,6})+\s*(.*)$")
_LEADING_Q_RE = re.compile(r"^(?:q|问题)\s*\d*\s*[:：.\-]?\s*", re.IGNORECASE)
_LEADING_ENUM_RE = re.compile(r"^\d+\s*[:：.\-]\s*")
_LEADING_A_RE = re.compile(r"^(?:\*\*A\*\*|A|答案|答)\s*[:：]\s*", re.IGNORECASE)
_INCOMPLETE_TAIL_RE = re.compile(
    r"(通过|以及|并|并且|或|与|在|对|向|从|将|使|让|为|由|基于|关于|包括|支持|用于|实现|进行|提供|提升|优化|改进|减少|增加|如果|但|然而|因此|所以|从而|例如|比如|尤其|其|该|这一|这种|这个|a|an|and|as|at|by|for|from|in|into|of|on|or|the|to|via|with)$",
    re.IGNORECASE,
)
_SECTION_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")


def normalize_heading_text(text: str) -> str:
    t = str(text or "").strip().lower()
    t = re.sub(r"`+", "", t)
    t = re.sub(r"[*_~]+", "", t)
    t = re.sub(r"^[\W_]+|[\W_]+$", "", t, flags=re.UNICODE)
    t = re.sub(r"[\s:：·、/（）()\[\]\-]+", "", t, flags=re.UNICODE)
    return t


def collapse_repeated_heading_markers(line: str) -> str:
    match = _REPEATED_HEADING_RE.match(str(line or "").strip())
    if not match:
        return str(line or "")
    hashes = match.group(1)
    text = match.group(2).strip()
    return f"{hashes} {text}".rstrip()


def looks_like_placeholder_line(line: str) -> bool:
    s = str(line or "").strip()
    if not s:
        return False
    for pattern in _PLACEHOLDER_PATTERNS:
        if pattern.search(s):
            return True
    return False


def looks_like_prompt_leak_line(line: str) -> bool:
    s = str(line or "").strip()
    if not s:
        return False
    lowered = s.lower()
    if any(keyword in lowered for keyword in {"json", "markdown"}) and "只" in s:
        return True
    return any(keyword in s for keyword in PROMPT_LEAK_KEYWORDS)


def normalize_generated_markdown(
    text: str,
    *,
    wrapper_headings: Iterable[str] | None = None,
    strip_first_heading: bool = True,
    demote_headings: bool = True,
) -> str:
    if not text:
        return ""

    wrapper_set = {normalize_heading_text(h) for h in (wrapper_headings or DEFAULT_WRAPPER_HEADINGS)}
    lines = str(text).replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    in_code_fence = False
    first_content_seen = False
    last_heading_norm = ""

    for raw in lines:
        line = collapse_repeated_heading_markers(raw.rstrip())
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            out.append(line)
            first_content_seen = True
            continue

        if not stripped:
            if out and out[-1] == "":
                continue
            out.append("")
            continue

        if looks_like_placeholder_line(stripped) or looks_like_prompt_leak_line(stripped):
            continue

        if not in_code_fence:
            heading_match = _HEADING_RE.match(stripped)
            if heading_match:
                hashes, heading_text = heading_match.groups()
                heading_text = heading_text.strip()
                heading_norm = normalize_heading_text(heading_text)
                if not heading_text:
                    continue
                if heading_norm in wrapper_set:
                    if not first_content_seen or len(hashes) <= 2:
                        continue
                if strip_first_heading and not first_content_seen and len(hashes) <= 2:
                    continue
                if heading_norm and heading_norm == last_heading_norm:
                    continue
                if demote_headings:
                    level = min(6, len(hashes) + 1)
                    line = f"{'#' * level} {heading_text}"
                last_heading_norm = heading_norm
                out.append(line)
                first_content_seen = True
                continue

        out.append(line)
        first_content_seen = True
        last_heading_norm = ""

    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()

    normalized = "\n".join(out)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def extract_bulleted_items(text: str, *, max_items: int = 7) -> list[str]:
    cleaned = normalize_generated_markdown(
        text,
        wrapper_headings={"学习要点", "核心学习要点", "关键要点", *DEFAULT_WRAPPER_HEADINGS},
        strip_first_heading=True,
        demote_headings=False,
    )
    items: list[str] = []
    for raw in cleaned.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        if _HEADING_RE.match(stripped) or stripped == "---":
            continue
        item = re.sub(r"^(?:[-*•]\s*|\d+[.)]\s*)", "", stripped).strip()
        if not item:
            continue
        if item not in items:
            items.append(item)
        if len(items) >= max_items:
            break
    return items


def parse_faq_markdown(text: str, *, max_items: int = 7) -> list[dict]:
    cleaned = normalize_generated_markdown(
        text,
        wrapper_headings={"常见问题", "常见问题解答", "faq", *DEFAULT_WRAPPER_HEADINGS},
        strip_first_heading=True,
        demote_headings=False,
    )
    if not cleaned:
        return []

    lines = cleaned.splitlines()
    entries: list[dict] = []
    current_question = ""
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_question, current_body
        if not current_question:
            current_body = []
            return
        answer = "\n".join(current_body).strip()
        answer = _LEADING_A_RE.sub("", answer)
        answer = re.sub(r"^\*\*A\*\*\s*$", "", answer).strip()
        if current_question and answer:
            entries.append(
                {
                    "question": current_question,
                    "answer": answer,
                }
            )
        current_question = ""
        current_body = []

    for raw in lines:
        stripped = raw.strip()
        heading_match = _HEADING_RE.match(stripped)
        if heading_match and len(heading_match.group(1)) >= 3:
            flush()
            question = _LEADING_Q_RE.sub("", heading_match.group(2).strip())
            question = _LEADING_ENUM_RE.sub("", question).strip()
            current_question = question.strip()
            continue
        if stripped == "---":
            continue
        if current_question and not any(line.strip() for line in current_body):
            if not stripped:
                continue
            normalized_body_head = _LEADING_ENUM_RE.sub("", stripped).strip()
            if normalize_heading_text(normalized_body_head) == normalize_heading_text(current_question):
                continue
        current_body.append(raw.rstrip())

    flush()
    return entries[:max_items]


def filter_related_resources(resources: list[dict], *, max_items: int = 5) -> list[dict]:
    out: list[dict] = []
    for resource in resources or []:
        if not isinstance(resource, dict):
            continue
        title = str(resource.get("title") or "").strip()
        link = str(resource.get("link") or "").strip()
        description = str(resource.get("description") or "").strip()
        if not title or not link:
            continue
        out.append({"title": title, "link": link, "description": description})
        if len(out) >= max_items:
            break
    return out


def looks_incomplete_text(text: str) -> bool:
    t = str(text or "").strip()
    if not t:
        return False

    if t.count("```") % 2 != 0:
        return True

    if re.search(r"[:：(\[（\-]\s*$", t):
        return True

    if re.search(r"(?:^|\n)\s*[-*•]\s*$", t):
        return True

    if re.search(r"(?:^|\n)\s*#{1,6}\s*$", t):
        return True

    if re.search(r"(?:^|\n)\s*\*\*[^*]+\*\*\s*$", t):
        return True

    if re.search(r"[。！？.!?）)]\s*$", t):
        return False

    last_line = next((line.strip() for line in reversed(t.splitlines()) if line.strip()), "")
    if len(last_line) <= 10:
        return True

    if _INCOMPLETE_TAIL_RE.search(last_line):
        return True

    return False


def remove_markdown_sections_by_heading(text: str, headings: Iterable[str]) -> tuple[str, int]:
    if not text:
        return text, 0

    target_headings = {normalize_heading_text(h) for h in headings}
    removed = 0
    lines = str(text).splitlines()
    out: list[str] = []
    in_frontmatter = False
    frontmatter_done = False
    in_code_fence = False
    skipping = False

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if idx == 0 and stripped == "---":
            in_frontmatter = True
            out.append(line)
            idx += 1
            continue

        if in_frontmatter:
            out.append(line)
            if stripped == "---":
                in_frontmatter = False
                frontmatter_done = True
            idx += 1
            continue

        if stripped.startswith("```"):
            in_code_fence = not in_code_fence

        heading_match = None if in_code_fence else _SECTION_HEADING_RE.match(stripped)
        if heading_match and frontmatter_done:
            heading_norm = normalize_heading_text(heading_match.group(1))
            if heading_norm in target_headings:
                removed += 1
                if out and out[-1].strip() == "---":
                    out.pop()
                    while out and out[-1] == "":
                        out.pop()
                idx += 1
                while idx < len(lines):
                    next_line = lines[idx]
                    next_stripped = next_line.strip()
                    if next_stripped.startswith("```"):
                        in_code_fence = not in_code_fence
                    if not in_code_fence and _SECTION_HEADING_RE.match(next_stripped):
                        break
                    idx += 1
                continue

        out.append(line)
        idx += 1

    normalized = "\n".join(out)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized).strip()
    if text.endswith("\n"):
        normalized += "\n"
    return normalized, removed
