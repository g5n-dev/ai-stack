"""Deterministic, evidence-preserving repair plans for historical Markdown.

The planner is deliberately read-only.  Applying a plan is a separate operation
that reuses the repository's dedupe shadow/soak gate, takes an immutable backup,
checks file preconditions, and replaces each file atomically.
"""

from __future__ import annotations

import copy
import hashlib
import html
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unicodedata
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from ._json import sha256_digest
from .content_quality import (
    analyze_post,
    content_quality_reasons,
    description_is_truncated,
    is_source_brief,
    remove_empty_section_headings,
    remove_misplaced_strong_markers,
)
from .identity import canonicalize_url
from .migrations import (
    MigrationSafetyError,
    source_revision,
    validate_dedupe_execution_gate,
    validate_execution_gate,
)
from .stores import UnsafeStorePathError
from .tag_taxonomy import normalize_tags

DEFAULT_CATEGORY_WHITELIST = frozenset(
    {
        "AI 工程",
        "产品与创业",
        "前端",
        "后端",
        "大模型",
        "安全",
        "开发工具",
        "开源生态",
        "效率与方法论",
        "数据",
        "生活与杂谈",
        "系统与基础设施",
        "论文",
    }
)
DEFAULT_SCENARIO_WHITELIST = frozenset(
    {
        "Web应用开发",
        "前端开发",
        "后端开发",
        "全栈开发",
        "AI/ML项目",
        "自然语言处理",
        "计算机视觉",
        "数据科学",
        "大语言模型",
        "RAG应用",
        "DevOps/运维",
        "云原生/容器",
        "Kubernetes",
        "安全工具",
        "监控/日志",
        "数据库",
        "命令行工具",
        "自动化脚本",
        "测试工具",
        "文档工具",
        "编辑器/IDE",
        "效率工具",
        "移动应用",
        "游戏开发",
        "物联网",
        "区块链",
        "桌面应用",
        "嵌入式系统",
        "设计工具",
        "数据可视化",
        "动画/3D",
    }
)

_BACKUP_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA1_HEX = re.compile(r"^[0-9a-f]{40}$")
_GIT_RECOVERY_SCHEMA = "historical_git_recovery_manifest_v1"
_GIT_RECOVERY_AUDIT_SCHEMA = "historical_git_recovery_audit_v1"
_GIT_RECOVERY_BASES = frozenset(
    {
        "detected_truncation",
        "reviewed_complete_same_canonical_history",
    }
)
_MAX_MARKDOWN_BYTES = 2 * 1024 * 1024
_FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?(.*)\Z", re.DOTALL)
_RELREF = re.compile(
    r"(?P<prefix>\{\{[<%]\s*relref\s+)(?P<quote>['\"])(?P<target>.+?)(?P=quote)(?P<suffix>\s*[>%]\}\})"
)
_FENCE_LINE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<tail>.*)$")
_ATX_H1 = re.compile(r"^(?P<indent> {0,3})#[ \t]+(?P<title>.*?)[ \t]*$")
_ATX_SECTION_HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(?P<title>.*?)(?:[ \t]+#+)?[ \t]*$")
_ATX_HEADING_DETAILS = re.compile(
    r"^(?P<indent> {0,3})(?P<marks>#{1,6})[ \t]+"
    r"(?P<title>.*?)(?:[ \t]+#+)?[ \t]*$"
)
_INLINE_DESCRIPTION = re.compile(r"^ {0,3}[-+*][ \t]+\*\*描述\*\*[ \t]*[:：][ \t]*(?P<value>.*)$")
_SETEXT_H1_UNDERLINE = re.compile(r"^ {0,3}=+[ \t]*$")
_SETEXT_UNDERLINE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
_HORIZONTAL_RULE = re.compile(r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
_BLOCK_PREFIX = re.compile(
    r"^(?:[ \t]*>[ \t]?)+|^[ \t]*(?:[-+*]|\d+[.)])[ \t]+|"
    r"^[ \t]*\[[ xX]\][ \t]+"
)
_MARKDOWN_IMAGE = re.compile(r"!\[(?P<label>[^\]]*)\]\([^)]*\)")
_MARKDOWN_LINK = re.compile(r"\[(?P<label>[^\]]+)\]\([^)]*\)")
_MARKDOWN_REFERENCE_LINK = re.compile(r"\[(?P<label>[^\]]+)\](?:\[[^\]]*\])")
_AUTOLINK = re.compile(r"<https?://[^>]+>", re.IGNORECASE)
_RAW_URL = re.compile(r"https?://[^\s<>]+", re.IGNORECASE)
_HTML_TAG = re.compile(r"</?[A-Za-z][^>]*>")
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_REFERENCE_DEFINITION = re.compile(r"^[ \t]*\[[^\]]+\]:[ \t]+\S+")
_EDITORIAL_META_OPENING = re.compile(
    r"^\s*(?:这里(?:是|有)?(?:一个|一篇)?|这是(?:一个|一篇)?|以下是)"
    r"\s*为(?:你|您).{0,48}?(?:撰写|定制|打造|创作|编写|生成)"
    r".{0,48}?(?:引言|导语)",
    re.DOTALL,
)
_INTRO_DECORATION = re.compile(r"^[【\[]\s*(?:引言|导语)\s*[】\]]$")
_TRANSLATION_ASSISTANT_OPENING = re.compile(
    r"^(?:您好[！!，,。\s]*)?(?:(?:(?:我)?注意到|我发现).{0,24})?"
    r"(?:(?:您提供的)?(?:这段|以下)?"
    r"(?:内容|文字|文本)|这句话|该中文文本).{0,80}?(?:中文|无需翻译)",
    re.IGNORECASE,
)
_TRANSLATION_ASSISTANT_CLOSING = re.compile(
    r"(?:请(?:您)?(?:告诉我|提供)|如果您.{0,100}(?:告诉我|随时告诉我)|"
    r"我(?:可以|会).{0,80}(?:帮助|完成|处理)|"
    r"请问.{0,120}(?:需要|帮助|服务|翻译).{0,40}).{0,40}$",
    re.IGNORECASE,
)
_REPAIRABLE_FATAL_REASONS = frozenset(
    {
        "body_h1_heading",
        "consecutive_horizontal_rules",
        "editorial_meta_preamble",
        "missing_description",
        "truncated_description",
        "translation_response_leak",
    }
)
_INTEGRITY_FAILURE_REASONS = frozenset(
    {
        "encoding_replacement_character",
        "translation_response_leak",
        "truncated_pre_citation_tail",
        "unclosed_code_fence",
        "unterminated_prose",
    }
)
_PREFERRED_DESCRIPTION_HEADINGS = (
    "摘要",
    "简介",
    "导语",
    "概述",
    "内容提要",
    "核心要点",
)
_METADATA_DESCRIPTION_HEADINGS = (
    "基本信息",
    "来源信息",
    "原始来源",
    "参考资料",
    "元数据",
)
_DESCRIPTION_META_PREAMBLE = re.compile(
    r"^\s*(?:"
    r"以下(?:是)?(?:为您)?(?:对(?:该|这段|上述)?内容的?)?"
    r"(?:撰写|提供)?(?:的)?(?:主要)?(?:中文)?(?:内容)?"
    r"(?:总结|摘要|引言|导语)(?:，[^：:\n]{0,100})?"
    r"|(?:以下|这里)是(?:一个)?(?:为(?:您|你))?(?:精心)?"
    r"(?:定制|打造|撰写|提供)的?(?:“[^”\n]{0,40}”的?)?"
    r"(?:引言|导语|摘要|总结)(?:，[^：:\n]{0,100})?"
    r")[：:]\s*"
)


@dataclass(frozen=True, slots=True)
class PlannedWrite:
    """One compare-and-swap file replacement relative to the posts root."""

    path: str
    before_sha256: str | None
    after_sha256: str
    content: bytes


@dataclass(frozen=True, slots=True)
class PlannedDelete:
    """One compare-and-swap file deletion relative to the posts root."""

    path: str
    before_sha256: str


@dataclass(frozen=True, slots=True)
class HistoricalRepairPlan:
    """Public deterministic manifest plus private mutation payloads."""

    content_root: Path
    reference_root: Path
    manifest: dict[str, Any]
    writes: tuple[PlannedWrite, ...]
    deletes: tuple[PlannedDelete, ...]


@dataclass(frozen=True, slots=True)
class _Document:
    path: Path
    relative_path: str
    raw: bytes
    metadata: dict[str, Any]
    body: str
    normalized_metadata: dict[str, Any]
    normalized_body: str
    canonical_url: str
    contamination_reasons: tuple[str, ...]
    warning_reasons: tuple[str, ...]
    quality_score: int


@dataclass(frozen=True, slots=True)
class _GitRecoveryEntry:
    target_path: str
    target_file_sha256: str
    canonical_url: str
    recovery_basis: str
    source_commit: str
    source_path: str
    source_git_blob: str
    source_file_sha256: str


@dataclass(frozen=True, slots=True)
class _GitRecoveryManifest:
    audit_path: str
    audit_sha256: str
    file_sha256: str
    entries: Mapping[str, _GitRecoveryEntry]


@dataclass(frozen=True, slots=True)
class _BodyH1:
    start: int
    end: int
    title: str
    kind: str


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _regular_markdown_files(root: Path) -> list[Path]:
    if root.is_symlink() or not root.is_dir():
        raise UnsafeStorePathError(f"historical repair root must be a regular directory: {root}")
    paths: list[Path] = []
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained: list[str] = []
        for name in sorted(directory_names):
            candidate = current_path / name
            if candidate.is_symlink():
                raise UnsafeStorePathError(
                    f"historical repair root contains a symlink: {candidate}"
                )
            retained.append(name)
        directory_names[:] = retained
        for name in sorted(file_names):
            candidate = current_path / name
            details = candidate.lstat()
            if candidate.is_symlink() or not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
                raise UnsafeStorePathError(
                    f"historical repair root contains an unsafe file: {candidate}"
                )
            if candidate.suffix.casefold() == ".md":
                if details.st_size > _MAX_MARKDOWN_BYTES:
                    raise MigrationSafetyError(
                        f"historical repair Markdown is too large: {candidate}"
                    )
                paths.append(candidate)
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def _normalize_label(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(unicodedata.normalize("NFC", value).strip().split())


def _normalized_list(value: object, *, limit: int | None = None) -> list[str]:
    values: Iterable[object]
    if isinstance(value, list):
        values = value
    elif isinstance(value, str):
        values = (value,)
    else:
        values = ()
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        normalized = _normalize_label(item)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
        if limit is not None and len(result) >= limit:
            break
    return result


def _line_content(line: str) -> str:
    return line.rstrip("\r\n")


def _line_ending(line: str) -> str:
    content = _line_content(line)
    return line[len(content) :]


def _outside_fence_flags(lines: list[str]) -> list[bool]:
    """Return which Markdown lines are prose, treating fence markers as fenced."""

    flags: list[bool] = []
    open_character: str | None = None
    open_length = 0
    for line in lines:
        match = _FENCE_LINE.match(_line_content(line))
        if match is None:
            flags.append(open_character is None)
            continue
        fence = match.group("fence")
        character = fence[0]
        if open_character is None:
            flags.append(False)
            open_character = character
            open_length = len(fence)
            continue
        flags.append(False)
        if (
            character == open_character
            and len(fence) >= open_length
            and not match.group("tail").strip()
        ):
            open_character = None
            open_length = 0
    return flags


def _plain_inline_markdown(value: str) -> str:
    """Reduce inline Markdown to deterministic human-readable plain text."""

    text = unicodedata.normalize("NFC", str(value or ""))
    text = _HTML_COMMENT.sub(" ", text)
    text = _MARKDOWN_IMAGE.sub(lambda match: match.group("label"), text)
    text = _MARKDOWN_LINK.sub(lambda match: match.group("label"), text)
    text = _MARKDOWN_REFERENCE_LINK.sub(lambda match: match.group("label"), text)
    text = _AUTOLINK.sub(" ", text)
    text = _RAW_URL.sub(" ", text)
    text = _HTML_TAG.sub(" ", text)
    text = re.sub(r"`+([^`\n]+?)`+", r"\1", text)
    text = re.sub(r"\\([\\`*_[\]{}()#+.!<>~-])", r"\1", text)
    text = re.sub(r"[*_~]", "", text)
    text = text.replace("[", "").replace("]", "")
    return " ".join(html.unescape(text).split())


def _heading_title(value: str) -> str:
    without_closing_hashes = re.sub(r"[ \t]+#+[ \t]*$", "", value.strip())
    return _plain_inline_markdown(without_closing_hashes)


def _title_key(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(unicodedata.normalize("NFKC", _plain_inline_markdown(value)).casefold().split())


def _decorated_title_key(value: object) -> str:
    """Normalize a title after dropping leading symbol-only UI decorations."""

    normalized = unicodedata.normalize("NFKC", _plain_inline_markdown(str(value or "")))
    index = 0
    while index < len(normalized):
        character = normalized[index]
        category = unicodedata.category(character)
        if (
            character.isspace()
            or category.startswith("S")
            or category in {"Cf", "Mn"}
            or character in "·•|｜—–-"
        ):
            index += 1
            continue
        break
    return " ".join(normalized[index:].casefold().split())


def _clean_editorial_opening(value: str) -> tuple[str, bool]:
    """Remove one proven assistant-authored intro sentence from existing text."""

    text = unicodedata.normalize("NFC", str(value or ""))
    match = _EDITORIAL_META_OPENING.match(text[:320])
    if match is None:
        return value, False
    tail = text[match.end() :]
    delimiter = re.search(r"[：:。！？!?]", tail[:200])
    if delimiter is None:
        remainder = ""
    else:
        remainder = tail[delimiter.end() :]
    remainder = remainder.lstrip()
    while True:
        decoration = re.match(
            r"^(?:\*{1,3})?\s*[【\[]\s*(?:引言|导语)\s*[】\]]"
            r"\s*(?:\*{1,3})?\s*",
            remainder,
        )
        if decoration is not None:
            remainder = remainder[decoration.end() :].lstrip()
            continue
        rule = re.match(r"^(?:\*{3,}|-{3,}|_{3,})\s*", remainder)
        if rule is not None:
            remainder = remainder[rule.end() :].lstrip()
            continue
        break
    return remainder.strip(), True


def _clean_editorial_intro_sections(body: str) -> str:
    lines = str(body or "").splitlines(keepends=True)
    outside = _outside_fence_flags(lines)
    replacements: list[tuple[int, int, list[str]]] = []
    for heading_index, line in enumerate(lines):
        if not outside[heading_index]:
            continue
        heading = _ATX_HEADING_DETAILS.match(_line_content(line))
        if heading is None or len(heading.group("marks")) < 2:
            continue
        heading_title = _title_key(_heading_title(heading.group("title")))
        if "引言" not in heading_title and "导语" not in heading_title:
            continue

        opening_index = heading_index + 1
        while opening_index < len(lines):
            content = _line_content(lines[opening_index])
            if not outside[opening_index]:
                break
            if not content.strip() or _HORIZONTAL_RULE.fullmatch(content):
                opening_index += 1
                continue
            break
        if opening_index >= len(lines) or not outside[opening_index]:
            continue
        if _ATX_HEADING_DETAILS.match(_line_content(lines[opening_index])) is not None:
            continue

        paragraph_end = opening_index
        paragraph_lines: list[str] = []
        while paragraph_end < len(lines):
            content = _line_content(lines[paragraph_end])
            if not outside[paragraph_end] or not content.strip():
                break
            if _ATX_HEADING_DETAILS.match(content) is not None:
                break
            paragraph_lines.append(content.strip())
            paragraph_end += 1
        cleaned, matched = _clean_editorial_opening(" ".join(paragraph_lines))
        if not matched:
            continue
        if cleaned:
            replacements.append((heading_index + 1, paragraph_end, ["\n", f"{cleaned}\n"]))
            continue

        cursor = paragraph_end
        while cursor < len(lines):
            while cursor < len(lines) and not _line_content(lines[cursor]).strip():
                cursor += 1
            if cursor >= len(lines) or not outside[cursor]:
                break
            content = _line_content(lines[cursor])
            decoration = _plain_inline_markdown(content)
            if _HORIZONTAL_RULE.fullmatch(content) or _INTRO_DECORATION.fullmatch(decoration):
                cursor += 1
                continue
            break
        replacements.append((heading_index + 1, cursor, ["\n"]))

    for start, end, replacement in reversed(replacements):
        lines[start:end] = replacement
    return "".join(lines)


def _translation_only_description(section: str) -> bool:
    lines = str(section or "").splitlines()
    outside = _outside_fence_flags(lines)
    if not all(outside):
        return False
    paragraphs: list[list[str]] = []
    current: list[str] = []
    plain_lines: list[str] = []
    for line in lines:
        content = line.strip()
        if not content or _HORIZONTAL_RULE.fullmatch(line):
            if current:
                paragraphs.append(current)
                current = []
            continue
        if _ATX_HEADING_DETAILS.match(line) is not None:
            return False
        current.append(content)
        plain = _plain_inline_markdown(_BLOCK_PREFIX.sub("", content).strip())
        if plain:
            plain_lines.append(plain)
    if current:
        paragraphs.append(current)
    if not paragraphs:
        return False
    prose = " ".join(plain_lines)
    if len(prose) > 1_200:
        return False
    if "translation_response_leak" not in content_quality_reasons(f"## 描述\n\n{prose}\n"):
        return False
    if _TRANSLATION_ASSISTANT_OPENING.search(prose[:240]) is None:
        return False
    return len(paragraphs) == 1 or bool(_TRANSLATION_ASSISTANT_CLOSING.search(prose[-300:]))


def _translation_assistant_closes(section: str) -> bool:
    plain_lines: list[str] = []
    for line in str(section or "").splitlines():
        content = line.strip()
        if not content or _HORIZONTAL_RULE.fullmatch(content):
            continue
        plain = _plain_inline_markdown(_BLOCK_PREFIX.sub("", content).strip())
        if plain:
            plain_lines.append(plain)
    prose = " ".join(plain_lines)
    return bool(_TRANSLATION_ASSISTANT_CLOSING.search(prose[-300:]))


def _has_complete_later_article_section(
    lines: list[str],
    outside: list[bool],
    start: int,
) -> bool:
    """Require preserved non-footer prose after a removable assistant section."""

    index = start
    while index < len(lines):
        if not outside[index]:
            index += 1
            continue
        heading = _ATX_HEADING_DETAILS.match(_line_content(lines[index]))
        title = (
            _title_key(_heading_title(heading.group("title")))
            if heading is not None and len(heading.group("marks")) <= 2
            else ""
        )
        is_footer = any(
            title.startswith(prefix) for prefix in ("引用", "来源", "站内链接", "相关文章")
        )
        if not title or is_footer:
            index += 1
            continue

        cursor = index + 1
        while cursor < len(lines):
            content = _line_content(lines[cursor])
            next_heading = _ATX_HEADING_DETAILS.match(content)
            if (
                outside[cursor]
                and next_heading is not None
                and len(next_heading.group("marks")) <= 2
            ):
                break
            if (
                outside[cursor]
                and content.strip()
                and not _HORIZONTAL_RULE.fullmatch(content)
                and next_heading is None
            ):
                return True
            cursor += 1
        index = cursor
    return False


def _remove_translation_description_sections(body: str) -> str:
    lines = str(body or "").splitlines(keepends=True)
    outside = _outside_fence_flags(lines)
    replacements: list[tuple[int, int, list[str]]] = []
    index = 0
    while index < len(lines):
        if not outside[index]:
            index += 1
            continue
        heading = _ATX_HEADING_DETAILS.match(_line_content(lines[index]))
        if (
            heading is None
            or len(heading.group("marks")) != 2
            or _title_key(_heading_title(heading.group("title"))) != "描述"
        ):
            index += 1
            continue
        section_end = index + 1
        while section_end < len(lines):
            candidate = _ATX_HEADING_DETAILS.match(_line_content(lines[section_end]))
            if (
                outside[section_end]
                and candidate is not None
                and len(candidate.group("marks")) <= 2
            ):
                break
            section_end += 1
        section = "".join(lines[index + 1 : section_end])
        if not _translation_only_description(section) or not _has_complete_later_article_section(
            lines, outside, section_end
        ):
            index = section_end
            continue

        removal_start = index
        preceding = index - 1
        while preceding >= 0 and not _line_content(lines[preceding]).strip():
            preceding -= 1
        if (
            preceding >= 0
            and outside[preceding]
            and _HORIZONTAL_RULE.fullmatch(_line_content(lines[preceding]))
        ):
            removal_start = preceding
        replacements.append((removal_start, section_end, ["\n"]))
        index = section_end

    for start, end, replacement in reversed(replacements):
        lines[start:end] = replacement

    outside = _outside_fence_flags(lines)
    replacements = []
    index = 0
    while index < len(lines):
        if not outside[index]:
            index += 1
            continue
        marker = _INLINE_DESCRIPTION.match(_line_content(lines[index]))
        if marker is None:
            index += 1
            continue

        section_end = index + 1
        while section_end < len(lines):
            heading = _ATX_HEADING_DETAILS.match(_line_content(lines[section_end]))
            if outside[section_end] and heading is not None and len(heading.group("marks")) <= 2:
                break
            section_end += 1
        if not _has_complete_later_article_section(lines, outside, section_end):
            index = section_end
            continue

        removal_end: int | None = None
        for candidate_end in range(index + 1, section_end + 1):
            candidate = marker.group("value") + "\n" + "".join(lines[index + 1 : candidate_end])
            if _translation_only_description(candidate) and _translation_assistant_closes(
                candidate
            ):
                removal_end = candidate_end
                break
        if removal_end is None:
            index = section_end
            continue

        cursor = removal_end
        while cursor < section_end and not _line_content(lines[cursor]).strip():
            cursor += 1
        if (
            cursor < section_end
            and outside[cursor]
            and _HORIZONTAL_RULE.fullmatch(_line_content(lines[cursor]))
        ):
            cursor += 1
            while cursor < section_end and not _line_content(lines[cursor]).strip():
                cursor += 1
        replacements.append((index, cursor, ["\n"]))
        index = section_end

    for start, end, replacement in reversed(replacements):
        lines[start:end] = replacement
    return "".join(lines)


def _remove_decorated_leading_title(metadata: Mapping[str, Any], body: str) -> str:
    lines = str(body or "").splitlines(keepends=True)
    outside = _outside_fence_flags(lines)
    first = next(
        (index for index, line in enumerate(lines) if _line_content(line).strip()),
        None,
    )
    if first is None or not outside[first]:
        return body
    heading = _ATX_HEADING_DETAILS.match(_line_content(lines[first]))
    if heading is None or len(heading.group("marks")) not in {1, 2}:
        return body
    if not _decorated_title_key(metadata.get("title")) or _decorated_title_key(
        metadata.get("title")
    ) != _decorated_title_key(_heading_title(heading.group("title"))):
        return body

    end = first + 1
    while end < len(lines) and not _line_content(lines[end]).strip():
        end += 1
    if end < len(lines) and outside[end] and _HORIZONTAL_RULE.fullmatch(_line_content(lines[end])):
        end += 1
        while end < len(lines) and not _line_content(lines[end]).strip():
            end += 1
    return "".join(lines[:first] + lines[end:])


def _ordinary_echo_line(line: str) -> bool:
    content = _line_content(line)
    if not content.strip() or content.startswith(("    ", "\t")):
        return False
    return not bool(
        _ATX_HEADING_DETAILS.match(content)
        or _FENCE_LINE.match(content)
        or _HORIZONTAL_RULE.fullmatch(content)
        or re.match(r"^ {0,3}(?:>|[-+*][ \t]|\d+[.)][ \t]|<)", content)
    )


def _remove_heading_echoes(body: str) -> str:
    lines = str(body or "").splitlines(keepends=True)
    outside = _outside_fence_flags(lines)
    replacements: list[tuple[int, int, list[str]]] = []
    for index, line in enumerate(lines):
        if not outside[index]:
            continue
        heading = _ATX_HEADING_DETAILS.match(_line_content(line))
        if heading is None or not 2 <= len(heading.group("marks")) <= 6:
            continue
        following = index + 1
        while following < len(lines) and not _line_content(lines[following]).strip():
            following += 1
        if (
            following >= len(lines)
            or not outside[following]
            or not _ordinary_echo_line(lines[following])
        ):
            continue
        heading_text = re.sub(r"[ \t]+#+[ \t]*$", "", heading.group("title").strip())
        if _line_content(lines[following]).strip() != heading_text:
            continue
        end = following + 1
        while end < len(lines) and not _line_content(lines[end]).strip():
            end += 1
        replacements.append((index + 1, end, ["\n"] if end < len(lines) else []))

    for start, end, replacement in reversed(replacements):
        lines[start:end] = replacement
    return "".join(lines)


def _is_setext_title_line(line: str) -> bool:
    stripped = _line_content(line).strip()
    if not stripped:
        return False
    return not bool(
        re.match(
            r"^(?:#{1,6}[ \t]|>|[-+*][ \t]|\d+[.)][ \t]|`{3,}|~{3,})",
            stripped,
        )
    )


def _body_h1_headings(lines: list[str], outside: list[bool]) -> list[_BodyH1]:
    headings: list[_BodyH1] = []
    index = 0
    while index < len(lines):
        if not outside[index]:
            index += 1
            continue
        content = _line_content(lines[index])
        atx = _ATX_H1.match(content)
        if atx is not None:
            headings.append(
                _BodyH1(
                    start=index,
                    end=index,
                    title=_heading_title(atx.group("title")),
                    kind="atx",
                )
            )
            index += 1
            continue
        if (
            index + 1 < len(lines)
            and outside[index + 1]
            and _is_setext_title_line(lines[index])
            and _SETEXT_H1_UNDERLINE.fullmatch(_line_content(lines[index + 1]))
        ):
            headings.append(
                _BodyH1(
                    start=index,
                    end=index + 1,
                    title=_heading_title(content),
                    kind="setext",
                )
            )
            index += 2
            continue
        index += 1
    return headings


def _collapse_adjacent_horizontal_rules(body: str) -> str:
    lines = str(body or "").splitlines(keepends=True)
    outside = _outside_fence_flags(lines)
    result: list[str] = []
    previous_block_was_rule = False
    for index, line in enumerate(lines):
        content = _line_content(line)
        if not outside[index]:
            result.append(line)
            previous_block_was_rule = False
            continue
        if not content.strip():
            result.append(line)
            continue
        is_rule = bool(_HORIZONTAL_RULE.fullmatch(content))
        if is_rule and previous_block_was_rule:
            continue
        result.append(line)
        previous_block_was_rule = is_rule
    return "".join(result)


def _normalize_body_h1(metadata: dict[str, Any], body: str) -> str:
    lines = str(body or "").splitlines(keepends=True)
    if not lines:
        return body
    outside = _outside_fence_flags(lines)
    headings = _body_h1_headings(lines, outside)
    if not headings:
        return _collapse_adjacent_horizontal_rules(body)

    first_prose_index = next(
        (
            index
            for index, line in enumerate(lines)
            if outside[index] and _line_content(line).strip()
        ),
        None,
    )
    leading = next(
        (heading for heading in headings if heading.start == first_prose_index),
        None,
    )
    removed: set[int] = set()
    if leading is not None:
        frontmatter_title = _title_key(metadata.get("title"))
        body_title = _title_key(leading.title)
        equivalent = bool(frontmatter_title) and frontmatter_title == body_title
        strict_prefix = (
            bool(frontmatter_title)
            and len(frontmatter_title) < len(body_title)
            and body_title.startswith(frontmatter_title)
        )
        if equivalent or strict_prefix:
            removed.update(range(leading.start, leading.end + 1))
            if strict_prefix:
                metadata["title"] = leading.title
            following = leading.end + 1
            while following < len(lines) and not _line_content(lines[following]).strip():
                following += 1
            if (
                following < len(lines)
                and outside[following]
                and _HORIZONTAL_RULE.fullmatch(_line_content(lines[following]))
            ):
                removed.add(following)

    by_start = {heading.start: heading for heading in headings}
    normalized: list[str] = []
    index = 0
    while index < len(lines):
        if index in removed:
            index += 1
            continue
        heading = by_start.get(index)
        if heading is None:
            normalized.append(lines[index])
            index += 1
            continue
        if any(position in removed for position in range(heading.start, heading.end + 1)):
            index = heading.end + 1
            continue
        if heading.kind == "atx":
            match = _ATX_H1.match(_line_content(lines[index]))
            assert match is not None
            indent_length = len(match.group("indent"))
            normalized.append(
                lines[index][:indent_length] + "##" + lines[index][indent_length + 1 :]
            )
        else:
            source_title = _line_content(lines[index]).strip()
            ending = _line_ending(lines[index]) or _line_ending(lines[heading.end]) or "\n"
            normalized.append(f"## {source_title}{ending}")
        index = heading.end + 1
    return _collapse_adjacent_horizontal_rules("".join(normalized))


def _plain_description(body: str) -> str | None:
    """Extract an 80–200 character summary solely from existing prose."""

    lines = str(body or "").splitlines(keepends=True)
    outside = _outside_fence_flags(lines)
    preferred_lines: list[tuple[int, str]] = []
    fallback_lines: list[tuple[int, str]] = []
    preferred_section = False
    metadata_section = False
    index = 0
    while index < len(lines):
        line = lines[index]
        if not outside[index]:
            index += 1
            continue
        content = _line_content(line)
        stripped = content.strip()
        atx_heading = _ATX_SECTION_HEADING.match(content)
        if atx_heading is not None:
            heading = _title_key(_heading_title(atx_heading.group("title")))
            preferred_section = any(label in heading for label in _PREFERRED_DESCRIPTION_HEADINGS)
            metadata_section = any(label in heading for label in _METADATA_DESCRIPTION_HEADINGS)
            index += 1
            continue
        if (
            index + 1 < len(lines)
            and outside[index + 1]
            and _is_setext_title_line(line)
            and _SETEXT_UNDERLINE.fullmatch(_line_content(lines[index + 1]))
        ):
            heading = _title_key(_heading_title(content))
            preferred_section = any(label in heading for label in _PREFERRED_DESCRIPTION_HEADINGS)
            metadata_section = any(label in heading for label in _METADATA_DESCRIPTION_HEADINGS)
            index += 2
            continue
        if (
            not stripped
            or _SETEXT_UNDERLINE.fullmatch(content)
            or _HORIZONTAL_RULE.fullmatch(content)
            or _REFERENCE_DEFINITION.match(content)
        ):
            index += 1
            continue
        is_list_item = bool(re.match(r"^[ \t]*(?:[-+*]|\d+[.)])[ \t]+", content))
        stripped = _BLOCK_PREFIX.sub("", stripped).strip()
        plain = _plain_inline_markdown(stripped)
        plain = _DESCRIPTION_META_PREAMBLE.sub("", plain).strip()
        if plain:
            if not (metadata_section and is_list_item):
                fallback_lines.append((index, plain))
            if preferred_section:
                preferred_lines.append((index, plain))
        index += 1

    preferred = " ".join(value for _, value in preferred_lines)
    if len(preferred) >= 80:
        selected = preferred_lines
    elif preferred_lines:
        preferred_indexes = {line_index for line_index, _ in preferred_lines}
        selected = [
            *preferred_lines,
            *(item for item in fallback_lines if item[0] not in preferred_indexes),
        ]
    else:
        selected = fallback_lines
    prose = " ".join(value for _, value in selected)
    prose = " ".join(_HTML_COMMENT.sub(" ", prose).split())
    if len(prose) < 80:
        return None
    if len(prose) <= 200:
        if description_is_truncated(prose):
            candidate = prose.rstrip(" \t\r\n,，:：、/\\（([{=+-")
            return f"{candidate}…" if len(candidate) >= 80 else None
        return prose

    window = prose[:200]
    sentence_endings = [
        match.end()
        for match in re.finditer(
            r"(?:[。！？!?；;…]|(?<![\d.])\.(?=[\"'”’」』）)】\]]*(?:\s|$)))"
            r"[\"'”’」』）)】\]]*",
            window,
        )
    ]
    eligible_endings = [ending for ending in sentence_endings if ending >= 80]
    if eligible_endings:
        return window[: eligible_endings[-1]].rstrip()

    cut = 199
    ascii_word = re.compile(r"[A-Za-z0-9_+./-]")
    if ascii_word.fullmatch(prose[cut - 1]) and ascii_word.fullmatch(prose[cut]):
        while cut > 0 and ascii_word.fullmatch(prose[cut - 1]):
            cut -= 1
        if cut < 80:
            return None
    candidate = prose[:cut].rstrip(" \t\r\n,，:：、/\\（([{=+-")
    if len(candidate) < 80:
        return None
    return f"{candidate}…"


def _remove_misplaced_strong_markers(body: str) -> str:
    lines = str(body or "").splitlines(keepends=True)
    outside = _outside_fence_flags(lines)
    normalized: list[str] = []
    for index, line in enumerate(lines):
        if not outside[index]:
            normalized.append(line)
            continue
        content = _line_content(line)
        normalized.append(remove_misplaced_strong_markers(content) + _line_ending(line))
    return "".join(normalized)


def _normalize_active_post(
    metadata: Mapping[str, Any],
    body: str,
) -> tuple[dict[str, Any], str]:
    normalized_metadata = copy.deepcopy(dict(metadata))
    description = normalized_metadata.get("description")
    if isinstance(description, str):
        cleaned_description, matched = _clean_editorial_opening(description)
        if matched:
            if cleaned_description:
                normalized_metadata["description"] = cleaned_description
            else:
                normalized_metadata.pop("description", None)

    normalized_body = _clean_editorial_intro_sections(body)
    normalized_body = _remove_translation_description_sections(normalized_body)
    normalized_body = _remove_decorated_leading_title(
        normalized_metadata,
        normalized_body,
    )
    normalized_body = _normalize_body_h1(normalized_metadata, normalized_body)
    normalized_body = _remove_heading_echoes(normalized_body)
    normalized_body = _remove_misplaced_strong_markers(normalized_body)
    description = normalized_metadata.get("description")
    if (
        not isinstance(description, str)
        or not description.strip()
        or description_is_truncated(description)
    ):
        extracted = _plain_description(normalized_body)
        if extracted is not None:
            normalized_metadata["description"] = extracted
    return normalized_metadata, normalized_body


def _quality_score(body: str, warning_reasons: tuple[str, ...] = ()) -> int:
    compact_length = len(re.sub(r"\s+", "", body))
    headings = len(re.findall(r"(?m)^#{1,4}\s+\S", body))
    links = len(re.findall(r"https?://", body))
    fenced_blocks = body.count("```") // 2
    penalty = 0
    if "empty_section" in warning_reasons:
        penalty += 600
    if "source_excerpt_truncated" in warning_reasons:
        penalty += 300
    return (
        min(compact_length, 12_000)
        + min(headings, 20) * 120
        + min(links, 20) * 40
        + min(fenced_blocks, 10) * 100
        - penalty
    )


def _parse_document(path: Path, root: Path) -> _Document:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Markdown is not UTF-8: {path}") from exc
    match = _FRONTMATTER.match(text)
    if match is None:
        raise ValueError(f"Markdown has no closed YAML frontmatter: {path}")
    try:
        parsed = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Markdown frontmatter is invalid: {path}: {exc}") from exc
    if not isinstance(parsed, Mapping):
        raise ValueError(f"Markdown frontmatter must be a mapping: {path}")
    metadata = {str(key): copy.deepcopy(value) for key, value in parsed.items()}
    external_url = metadata.get("external_url")
    if not isinstance(external_url, str):
        raise ValueError(f"Markdown has no external_url: {path}")
    canonical_url = canonicalize_url(external_url)
    body = match.group(2)
    initial_analysis = analyze_post(text)
    initial_fatal = set(initial_analysis.fatal_reasons)

    normalized_metadata = metadata
    normalized_body = body
    can_repair = not (initial_fatal - _REPAIRABLE_FATAL_REASONS)
    if metadata.get("archived") is not True and can_repair:
        normalized_metadata, normalized_body = _normalize_active_post(metadata, body)
        normalized_document = _render_document(
            normalized_metadata,
            normalized_body,
        ).decode("utf-8")
        final_analysis = analyze_post(normalized_document)
        final_fatal = set(final_analysis.fatal_reasons)
        contamination_reasons = tuple(sorted(final_fatal))
        warning_reasons = final_analysis.warning_reasons
    else:
        contamination_reasons = tuple(sorted(initial_fatal))
        warning_reasons = initial_analysis.warning_reasons
    return _Document(
        path=path,
        relative_path=path.relative_to(root).as_posix(),
        raw=raw,
        metadata=metadata,
        body=body,
        normalized_metadata=normalized_metadata,
        normalized_body=normalized_body,
        canonical_url=canonical_url,
        contamination_reasons=contamination_reasons,
        warning_reasons=warning_reasons,
        quality_score=_quality_score(normalized_body, warning_reasons),
    )


def _date_key(document: _Document) -> tuple[str, str]:
    value = document.metadata.get("date")
    parsed: datetime | None = None
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime.combine(value, datetime.min.time())
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            parsed = None
    if parsed is None:
        return "9999-12-31T23:59:59.999999Z", document.relative_path
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    normalized = parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")
    return normalized, document.relative_path


def _hugo_route(relative_path: str) -> str:
    path = Path(relative_path)
    parts = list(path.with_suffix("").parts)
    if parts and parts[-1] in {"index", "_index"}:
        parts.pop()
    suffix = "/".join(parts)
    return f"/posts/{suffix}/" if suffix else "/posts/"


def _document_route(document: _Document) -> str:
    explicit = document.metadata.get("url")
    if isinstance(explicit, str) and explicit.strip().startswith("/"):
        normalized = "/" + explicit.strip().strip("/") + "/"
        if ".." not in Path(normalized).parts:
            return normalized
    slug = _normalize_label(document.metadata.get("slug"))
    if slug and "/" not in slug and ".." not in slug:
        return f"/posts/{slug.strip('/')}/"
    return _hugo_route(document.relative_path)


def _group_aliases(ordered: Iterable[_Document], route: _Document) -> list[str]:
    canonical_route = _document_route(route)
    aliases: set[str] = set()
    for document in ordered:
        if document.path == route.path:
            continue
        aliases.add(_document_route(document))
        aliases.update(_safe_aliases(document.metadata.get("aliases")))
    aliases.discard(canonical_route)
    return sorted(aliases)


def _safe_aliases(value: object) -> list[str]:
    aliases: list[str] = []
    for alias in _normalized_list(value):
        if not alias.startswith("/") or ".." in Path(alias).parts:
            continue
        normalized = "/" + alias.strip("/") + "/"
        if normalized not in aliases:
            aliases.append(normalized)
    return aliases


def _filtered_metadata(
    source: _Document,
    route: _Document,
    *,
    canonical_url: str,
    aliases: list[str],
    category_whitelist: frozenset[str],
    scenario_whitelist: frozenset[str],
) -> dict[str, Any]:
    metadata = copy.deepcopy(source.normalized_metadata)
    metadata["external_url"] = canonical_url
    metadata["tags"] = normalize_tags(source.normalized_metadata.get("tags"), limit=8)
    metadata["categories"] = [
        value
        for value in _normalized_list(source.normalized_metadata.get("categories"))
        if value in category_whitelist
    ]
    metadata["scenarios"] = [
        value
        for value in _normalized_list(source.normalized_metadata.get("scenarios"))
        if value in scenario_whitelist
    ]
    if "date" in route.metadata:
        metadata["date"] = copy.deepcopy(route.metadata["date"])
    for route_key in ("url", "slug"):
        if route_key in route.metadata:
            metadata[route_key] = copy.deepcopy(route.metadata[route_key])
        else:
            metadata.pop(route_key, None)
    existing_aliases = _safe_aliases(route.metadata.get("aliases"))
    metadata["aliases"] = sorted(set(existing_aliases + aliases))
    return _active_provenance_metadata(metadata, source.normalized_body)


def _active_provenance_metadata(metadata: Mapping[str, Any], body: str) -> dict[str, Any]:
    """Label legacy output honestly without claiming a missing source snapshot."""

    result = copy.deepcopy(dict(metadata))
    declared_mode = str(result.get("content_mode") or "").strip().casefold()
    if declared_mode == "source_brief" and is_source_brief(result, body):
        # Current source briefs already carry an immutable source snapshot and
        # support score.  Historical normalization must never downgrade that
        # evidence-backed provenance to ``legacy_no_snapshot``.
        result.pop("source_provenance", None)
        return result
    if is_source_brief(result, body):
        result["content_mode"] = "legacy_source_brief"
        result["publication_tier"] = "C"
    else:
        result["content_mode"] = "legacy_analysis"
        result["publication_tier"] = "LEGACY"
    result["source_provenance"] = "legacy_no_snapshot"
    result["source_support"] = 0.0
    return result


def _normalized_singleton(
    document: _Document,
    *,
    canonical_url: str,
) -> tuple[dict[str, Any], str] | None:
    """Return a minimal rewrite for one clean singleton article.

    Singleton normalization leaves categories, scenarios, routes, and all
    unrelated frontmatter untouched. Empty shell headings are removed without
    inventing prose so structural cleanup shares the same backup mechanism.
    """
    metadata = copy.deepcopy(document.normalized_metadata)
    metadata["external_url"] = canonical_url
    if document.metadata.get("archived") is True:
        metadata["title"] = (
            str(metadata.get("title") or "历史条目").replace("<", "＜").replace(">", "＞")
        )
        metadata["tags"] = []
        metadata["categories"] = []
        metadata["scenarios"] = []
        metadata.pop("_build", None)
        metadata["build"] = {"list": "never", "render": "always"}
        if metadata == document.metadata:
            return None
        return metadata, document.normalized_body

    normalized_tags = normalize_tags(document.normalized_metadata.get("tags"), limit=8)
    metadata["tags"] = normalized_tags
    metadata = _active_provenance_metadata(metadata, document.normalized_body)
    body, _ = remove_empty_section_headings(document.normalized_body)
    if metadata == document.metadata and body == document.body:
        return None
    return metadata, body


def _render_document(metadata: Mapping[str, Any], body: str) -> bytes:
    frontmatter = yaml.safe_dump(
        dict(metadata),
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip()
    normalized_body = body.strip()
    return f"---\n{frontmatter}\n---\n\n{normalized_body}\n".encode()


def _archive_stub(
    route: _Document,
    *,
    canonical_url: str,
    aliases: list[str],
    category_whitelist: frozenset[str],
    scenario_whitelist: frozenset[str],
) -> tuple[dict[str, Any], str]:
    metadata = _filtered_metadata(
        route,
        route,
        canonical_url=canonical_url,
        aliases=aliases,
        category_whitelist=category_whitelist,
        scenario_whitelist=scenario_whitelist,
    )
    metadata["archived"] = True
    metadata["content_mode"] = "archived"
    metadata["publication_tier"] = "ARCHIVED"
    metadata["source_provenance"] = "legacy_no_snapshot"
    metadata["source_support"] = 0.0
    metadata["archive_reason"] = "historical_content_quality_gate"
    metadata["description"] = "历史条目已归档：现有正文未通过内容质量门，请查阅原始来源。"
    metadata["title"] = (
        str(metadata.get("title") or "历史条目").replace("<", "＜").replace(">", "＞")
    )
    metadata["tags"] = []
    metadata["categories"] = []
    metadata["scenarios"] = []
    metadata["build"] = {"list": "never", "render": "always"}
    body = (
        "## 历史条目归档说明\n\n"
        "该条目的历史正文未通过内容质量门，可能包含基于标题推测的内容。"
        "为避免继续传播不可核验文本，本站仅保留透明归档记录。\n\n"
        f"- 历史内容质量门未通过\n- 原始来源：<{canonical_url}>\n"
    )
    return metadata, body


def _integrity_decision(
    ordered: Iterable[_Document],
    *,
    route: _Document,
    winner: _Document | None,
) -> dict[str, Any] | None:
    """Describe evidence-preserving recovery for structural integrity failures."""

    failures = [
        (
            document,
            sorted(set(document.contamination_reasons) & _INTEGRITY_FAILURE_REASONS),
        )
        for document in ordered
    ]
    failures = [(document, reasons) for document, reasons in failures if reasons]
    if not failures:
        return None
    failure_reasons = sorted({reason for _, reasons in failures for reason in reasons})
    if winner is None:
        action = "transparent_archive"
        source_path = None
        source_file_sha256 = None
    else:
        action = (
            "retain_complete_candidate"
            if winner.path == route.path
            else "restore_from_complete_sibling"
        )
        source_path = winner.relative_path
        source_file_sha256 = _sha256(winner.raw)
    return {
        "action": action,
        "failed_paths": [document.relative_path for document, _ in failures],
        "failure_reasons": failure_reasons,
        "source_file_sha256": source_file_sha256,
        "source_path": source_path,
    }


def _relative_operation_path(path: Path, content_root: Path) -> str:
    return Path(os.path.relpath(path, content_root)).as_posix()


def _relref_target_map(
    *, content_root: Path, canonical_path: str, delete_paths: Iterable[str]
) -> dict[str, str]:
    reference_root = content_root.parent
    canonical_absolute = content_root / canonical_path
    canonical_reference = canonical_absolute.relative_to(reference_root).as_posix()
    result: dict[str, str] = {}
    for relative in delete_paths:
        deleted_absolute = content_root / relative
        deleted_reference = deleted_absolute.relative_to(reference_root).as_posix()
        result[deleted_reference] = canonical_reference
        result[relative] = canonical_path
        result[f"/{deleted_reference}"] = f"/{canonical_reference}"
    return result


def _rewrite_relrefs(
    text: str, target_map: Mapping[str, str]
) -> tuple[str, list[tuple[str, str, int]]]:
    counts: dict[tuple[str, str], int] = defaultdict(int)

    def replace(match: re.Match[str]) -> str:
        old_target = match.group("target")
        new_target = target_map.get(old_target)
        if new_target is None:
            return match.group(0)
        counts[(old_target, new_target)] += 1
        return (
            f"{match.group('prefix')}{match.group('quote')}{new_target}"
            f"{match.group('quote')}{match.group('suffix')}"
        )

    rewritten = _RELREF.sub(replace, text)
    records = [(source, target, count) for (source, target), count in sorted(counts.items())]
    return rewritten, records


def _resolve_input_paths(root: Path, input_paths: Iterable[Path] | None) -> list[Path]:
    candidates = _regular_markdown_files(root) if input_paths is None else list(input_paths)
    result: list[Path] = []
    for value in candidates:
        path = Path(value).absolute()
        if not _is_within(path, root):
            raise UnsafeStorePathError(f"historical repair input escapes content root: {path}")
        details = path.lstat()
        if path.is_symlink() or not stat.S_ISREG(details.st_mode):
            raise UnsafeStorePathError(f"historical repair input is unsafe: {path}")
        if details.st_size > _MAX_MARKDOWN_BYTES:
            raise MigrationSafetyError(f"historical repair Markdown is too large: {path}")
        if path.suffix.casefold() == ".md":
            result.append(path)
    return sorted(set(result), key=lambda path: path.relative_to(root).as_posix())


def _recovery_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise MigrationSafetyError(f"Git recovery manifest has invalid {field}")
    return value


def _recovery_relative_path(value: object, field: str) -> str:
    text = _recovery_string(value, field)
    path = PurePosixPath(text)
    if (
        path.is_absolute()
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
        or "\\" in text
        or ":" in text
        or any(ord(character) < 32 for character in text)
        or path.suffix.casefold() != ".md"
    ):
        raise MigrationSafetyError(f"Git recovery manifest has unsafe {field}: {text}")
    return path.as_posix()


def _recovery_audit_path(value: object) -> str:
    text = _recovery_string(value, "audit_path")
    path = PurePosixPath(text)
    if (
        path.is_absolute()
        or not path.parts
        or len(path.parts) != 1
        or any(part in {"", ".", ".."} for part in path.parts)
        or "\\" in text
        or ":" in text
        or any(ord(character) < 32 for character in text)
        or path.suffix.casefold() != ".json"
    ):
        raise MigrationSafetyError(f"Git recovery manifest has unsafe audit_path: {text}")
    return path.as_posix()


def _recovery_hash(value: object, field: str, pattern: re.Pattern[str]) -> str:
    text = _recovery_string(value, field)
    if pattern.fullmatch(text) is None:
        raise MigrationSafetyError(f"Git recovery manifest has invalid {field}")
    return text


def _load_git_recovery_manifest(path: str | Path) -> _GitRecoveryManifest:
    manifest_path = Path(path).absolute()
    details = manifest_path.lstat()
    if manifest_path.is_symlink() or not stat.S_ISREG(details.st_mode):
        raise MigrationSafetyError("Git recovery manifest must be a regular file")
    if details.st_size > _MAX_MARKDOWN_BYTES:
        raise MigrationSafetyError("Git recovery manifest is too large")
    payload = manifest_path.read_bytes()
    try:
        parsed = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MigrationSafetyError("Git recovery manifest is not valid UTF-8 JSON") from exc
    if not isinstance(parsed, Mapping):
        raise MigrationSafetyError("Git recovery manifest root must be an object")
    expected_root_keys = {
        "schema_version",
        "audit_path",
        "audit_sha256",
        "entry_count",
        "entries",
    }
    if set(parsed) != expected_root_keys:
        raise MigrationSafetyError("Git recovery manifest has unexpected root fields")
    if parsed.get("schema_version") != _GIT_RECOVERY_SCHEMA:
        raise MigrationSafetyError("Git recovery manifest schema_version is unsupported")
    audit_sha256 = _recovery_hash(
        parsed.get("audit_sha256"),
        "audit_sha256",
        _SHA256_HEX,
    )
    audit_path = _recovery_audit_path(parsed.get("audit_path"))
    audit_file = manifest_path.parent.joinpath(*PurePosixPath(audit_path).parts)
    try:
        audit_details = audit_file.lstat()
    except OSError as exc:
        raise MigrationSafetyError("Git recovery audit cannot be read") from exc
    if audit_file.is_symlink() or not stat.S_ISREG(audit_details.st_mode):
        raise MigrationSafetyError("Git recovery audit must be a regular file")
    if audit_details.st_size > _MAX_MARKDOWN_BYTES:
        raise MigrationSafetyError("Git recovery audit is too large")
    audit_payload = audit_file.read_bytes()
    if _sha256(audit_payload) != audit_sha256:
        raise MigrationSafetyError("Git recovery audit SHA256 does not match manifest")
    try:
        audit = json.loads(audit_payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MigrationSafetyError("Git recovery audit is not valid UTF-8 JSON") from exc
    if not isinstance(audit, Mapping) or audit.get("schema_version") != _GIT_RECOVERY_AUDIT_SCHEMA:
        raise MigrationSafetyError("Git recovery audit schema_version is unsupported")
    entries_value = parsed.get("entries")
    if not isinstance(entries_value, list):
        raise MigrationSafetyError("Git recovery manifest entries must be an array")
    entry_count = parsed.get("entry_count")
    if (
        not isinstance(entry_count, int)
        or isinstance(entry_count, bool)
        or entry_count != len(entries_value)
    ):
        raise MigrationSafetyError("Git recovery manifest entry_count does not match entries")

    expected_entry_keys = {
        "target_path",
        "target_file_sha256",
        "canonical_url",
        "recovery_basis",
        "source_commit",
        "source_path",
        "source_git_blob",
        "source_file_sha256",
    }
    entries: dict[str, _GitRecoveryEntry] = {}
    for raw_entry in entries_value:
        if not isinstance(raw_entry, Mapping) or set(raw_entry) != expected_entry_keys:
            raise MigrationSafetyError("Git recovery manifest entry fields are invalid")
        target_path = _recovery_relative_path(raw_entry.get("target_path"), "target_path")
        source_path = _recovery_relative_path(raw_entry.get("source_path"), "source_path")
        canonical_url = _recovery_string(raw_entry.get("canonical_url"), "canonical_url")
        if canonicalize_url(canonical_url) != canonical_url:
            raise MigrationSafetyError("Git recovery manifest canonical URL is not canonical")
        recovery_basis = _recovery_string(
            raw_entry.get("recovery_basis"),
            "recovery_basis",
        )
        if recovery_basis not in _GIT_RECOVERY_BASES:
            raise MigrationSafetyError("Git recovery manifest has invalid recovery_basis")
        entry = _GitRecoveryEntry(
            target_path=target_path,
            target_file_sha256=_recovery_hash(
                raw_entry.get("target_file_sha256"),
                "target_file_sha256",
                _SHA256_HEX,
            ),
            canonical_url=canonical_url,
            recovery_basis=recovery_basis,
            source_commit=_recovery_hash(
                raw_entry.get("source_commit"),
                "source_commit",
                _GIT_SHA1_HEX,
            ),
            source_path=source_path,
            source_git_blob=_recovery_hash(
                raw_entry.get("source_git_blob"),
                "source_git_blob",
                _GIT_SHA1_HEX,
            ),
            source_file_sha256=_recovery_hash(
                raw_entry.get("source_file_sha256"),
                "source_file_sha256",
                _SHA256_HEX,
            ),
        )
        if target_path in entries:
            raise MigrationSafetyError(
                f"Git recovery manifest has duplicate target_path: {target_path}"
            )
        entries[target_path] = entry
    return _GitRecoveryManifest(
        audit_path=audit_path,
        audit_sha256=audit_sha256,
        file_sha256=_sha256(payload),
        entries=entries,
    )


def _git_repository_root(content_root: Path) -> Path:
    completed = subprocess.run(
        ["git", "-C", str(content_root), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise MigrationSafetyError("Git recovery content root is not inside a Git repository")
    try:
        repository = Path(completed.stdout.decode("utf-8").strip()).absolute()
        content_root.relative_to(repository)
    except (UnicodeDecodeError, ValueError) as exc:
        raise MigrationSafetyError("Git recovery repository root is invalid") from exc
    return repository


def _git_source_payload(
    repository: Path,
    *,
    content_root: Path,
    entry: _GitRecoveryEntry,
) -> bytes:
    content_prefix = PurePosixPath(content_root.relative_to(repository).as_posix())
    source_path = PurePosixPath(entry.source_path)
    if source_path.parts[: len(content_prefix.parts)] != content_prefix.parts:
        raise MigrationSafetyError(
            f"Git recovery source_path is outside content root: {entry.source_path}"
        )

    ancestor = subprocess.run(
        [
            "git",
            "-C",
            str(repository),
            "merge-base",
            "--is-ancestor",
            entry.source_commit,
            "HEAD",
        ],
        check=False,
        capture_output=True,
    )
    if ancestor.returncode != 0:
        raise MigrationSafetyError("Git recovery source commit is not an ancestor of HEAD")

    resolved = subprocess.run(
        [
            "git",
            "-C",
            str(repository),
            "rev-parse",
            "--verify",
            f"{entry.source_commit}:{entry.source_path}",
        ],
        check=False,
        capture_output=True,
    )
    try:
        resolved_blob = resolved.stdout.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise MigrationSafetyError("Git recovery commit:path blob is invalid") from exc
    if resolved.returncode != 0 or resolved_blob != entry.source_git_blob:
        raise MigrationSafetyError("Git recovery commit:path blob does not match manifest")

    blob_type = subprocess.run(
        ["git", "-C", str(repository), "cat-file", "-t", entry.source_git_blob],
        check=False,
        capture_output=True,
    )
    if blob_type.returncode != 0 or blob_type.stdout.strip() != b"blob":
        raise MigrationSafetyError("Git recovery source_git_blob is not a blob")
    blob = subprocess.run(
        ["git", "-C", str(repository), "cat-file", "blob", entry.source_git_blob],
        check=False,
        capture_output=True,
    )
    if blob.returncode != 0:
        raise MigrationSafetyError("Git recovery source blob cannot be read")
    payload = blob.stdout
    if len(payload) > _MAX_MARKDOWN_BYTES:
        raise MigrationSafetyError("Git recovery source blob is too large")
    if _sha256(payload) != entry.source_file_sha256:
        raise MigrationSafetyError("Git recovery source payload SHA256 does not match manifest")
    return payload


def _recovery_body(payload: bytes, entry: _GitRecoveryEntry) -> str:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationSafetyError("Git recovery source payload is not UTF-8") from exc
    match = _FRONTMATTER.match(text)
    if match is None:
        raise MigrationSafetyError("Git recovery source payload has invalid frontmatter")
    try:
        metadata = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise MigrationSafetyError("Git recovery source payload has invalid frontmatter") from exc
    if not isinstance(metadata, Mapping) or metadata.get("archived") is True:
        raise MigrationSafetyError("Git recovery source payload has invalid frontmatter")
    external_url = metadata.get("external_url")
    if not isinstance(external_url, str):
        raise MigrationSafetyError("Git recovery source payload has no canonical URL")
    if canonicalize_url(external_url) != entry.canonical_url:
        raise MigrationSafetyError("Git recovery source canonical URL does not match manifest")
    return match.group(2)


def _recover_document_from_git(
    document: _Document,
    *,
    content_root: Path,
    repository: Path,
    entry: _GitRecoveryEntry,
) -> tuple[_Document, dict[str, Any]]:
    if _sha256(document.raw) != entry.target_file_sha256:
        raise MigrationSafetyError(
            f"Git recovery target precondition SHA256 changed: {entry.target_path}"
        )
    if document.canonical_url != entry.canonical_url:
        raise MigrationSafetyError(
            f"Git recovery target canonical URL changed: {entry.target_path}"
        )
    if (
        entry.recovery_basis == "detected_truncation"
        and "truncated_pre_citation_tail" not in document.contamination_reasons
    ):
        raise MigrationSafetyError(
            f"Git recovery target no longer has the audited truncation: {entry.target_path}"
        )

    source_payload = _git_source_payload(
        repository,
        content_root=content_root,
        entry=entry,
    )
    source_body = _recovery_body(source_payload, entry)
    normalized_metadata, normalized_body = _normalize_active_post(
        document.metadata,
        source_body,
    )
    normalized_document = _render_document(normalized_metadata, normalized_body).decode("utf-8")
    final_analysis = analyze_post(normalized_document)
    if final_analysis.fatal_reasons:
        reasons = ", ".join(final_analysis.fatal_reasons)
        raise MigrationSafetyError(
            f"Git recovery source body still fails quality gate: {entry.target_path}: {reasons}"
        )

    recovered = _Document(
        path=document.path,
        relative_path=document.relative_path,
        raw=document.raw,
        metadata=document.metadata,
        body=document.body,
        normalized_metadata=normalized_metadata,
        normalized_body=normalized_body,
        canonical_url=document.canonical_url,
        contamination_reasons=(),
        warning_reasons=final_analysis.warning_reasons,
        quality_score=_quality_score(normalized_body, final_analysis.warning_reasons),
    )
    decision = {
        "action": "restore_from_git_history",
        "failed_paths": [entry.target_path],
        "failure_reasons": list(document.contamination_reasons),
        "recovery_basis": entry.recovery_basis,
        "source_commit": entry.source_commit,
        "source_file_sha256": entry.source_file_sha256,
        "source_git_blob": entry.source_git_blob,
        "source_path": entry.source_path,
        "target_file_sha256": entry.target_file_sha256,
    }
    return recovered, decision


def build_historical_repair_plan(
    *,
    content_root: str | Path,
    category_whitelist: Iterable[str] = DEFAULT_CATEGORY_WHITELIST,
    scenario_whitelist: Iterable[str] = DEFAULT_SCENARIO_WHITELIST,
    input_paths: Iterable[Path] | None = None,
    recovery_manifest_path: str | Path | None = None,
) -> HistoricalRepairPlan:
    """Build a deterministic plan for content repair and active metadata normalization."""

    root = Path(content_root).absolute()
    reference_root = root.parent
    paths = _resolve_input_paths(root, input_paths)
    recovery_manifest = (
        _load_git_recovery_manifest(recovery_manifest_path)
        if recovery_manifest_path is not None
        else None
    )
    selected_paths = {path.relative_to(root).as_posix() for path in paths}
    recovery_entries = recovery_manifest.entries if recovery_manifest is not None else {}
    unselected_recovery_targets = sorted(set(recovery_entries) - selected_paths)
    if unselected_recovery_targets:
        raise MigrationSafetyError(
            "Git recovery manifest targets are not in the selected input set: "
            + ", ".join(unselected_recovery_targets)
        )
    repository = _git_repository_root(root) if recovery_entries else None
    categories = frozenset(_normalize_label(value) for value in category_whitelist)
    scenarios = frozenset(_normalize_label(value) for value in scenario_whitelist)
    grouped: dict[str, list[_Document]] = defaultdict(list)
    recovery_decisions: dict[str, dict[str, Any]] = {}
    issues: list[dict[str, str]] = []
    for path in paths:
        relative_path = path.relative_to(root).as_posix()
        try:
            document = _parse_document(path, root)
        except (OSError, ValueError) as exc:
            issues.append({"path": relative_path, "reason": str(exc)})
            continue
        recovery_entry = recovery_entries.get(relative_path)
        if recovery_entry is not None:
            if repository is None:
                raise MigrationSafetyError("Git recovery repository was not resolved")
            document, decision = _recover_document_from_git(
                document,
                content_root=root,
                repository=repository,
                entry=recovery_entry,
            )
            recovery_decisions[relative_path] = decision
        grouped[document.canonical_url].append(document)

    if recovery_manifest is not None:
        unrecovered_targets = sorted(set(recovery_entries) - set(recovery_decisions))
        if unrecovered_targets:
            raise MigrationSafetyError(
                "Git recovery manifest targets were not recovered: "
                + ", ".join(unrecovered_targets)
            )

    replacement_bytes: dict[Path, bytes] = {}
    deletion_documents: dict[Path, _Document] = {}
    target_map: dict[str, str] = {}
    public_groups: list[dict[str, Any]] = []
    public_group_by_route: dict[Path, dict[str, Any]] = {}

    for canonical_url, candidates in sorted(grouped.items()):
        ordered = sorted(candidates, key=lambda document: document.relative_path)
        route = min(ordered, key=_date_key)
        is_clean_singleton = len(ordered) == 1 and not route.contamination_reasons
        if is_clean_singleton:
            normalized = _normalized_singleton(
                route,
                canonical_url=canonical_url,
            )
            if normalized is None:
                continue
            metadata, body = normalized
            winner: _Document | None = route
            disposition = "normalize_metadata"
            archive_reason: str | None = None
        else:
            clean = [
                document
                for document in ordered
                if not document.contamination_reasons
                and document.metadata.get("archived") is not True
            ]
            winner = (
                sorted(
                    clean,
                    key=lambda document: (
                        -document.quality_score,
                        document.relative_path,
                    ),
                )[0]
                if clean
                else None
            )
            if winner is None:
                metadata, body = _archive_stub(
                    route,
                    canonical_url=canonical_url,
                    aliases=_group_aliases(ordered, route),
                    category_whitelist=categories,
                    scenario_whitelist=scenarios,
                )
                disposition = "archive_stub"
                archive_reason = "all_candidates_failed_content_quality_gate"
            else:
                metadata = _filtered_metadata(
                    winner,
                    route,
                    canonical_url=canonical_url,
                    aliases=_group_aliases(ordered, route),
                    category_whitelist=categories,
                    scenario_whitelist=scenarios,
                )
                body, _ = remove_empty_section_headings(winner.normalized_body)
                disposition = "merge"
                archive_reason = None
        delete_paths = sorted(
            document.relative_path for document in ordered if document.path != route.path
        )
        aliases = _group_aliases(ordered, route)
        rendered = _render_document(metadata, body)
        replacement_bytes[route.path] = rendered
        for document in ordered:
            if document.path != route.path:
                deletion_documents[document.path] = document
        target_map.update(
            _relref_target_map(
                content_root=root,
                canonical_path=route.relative_path,
                delete_paths=delete_paths,
            )
        )
        public_group: dict[str, Any] = {
            "canonical_url": canonical_url,
            "canonical_path": route.relative_path,
            "body_source": winner.relative_path if winner is not None else None,
            "disposition": disposition,
            "source_file_count": len(ordered),
            "paths": [document.relative_path for document in ordered],
            "delete_paths": delete_paths,
            "aliases": aliases,
            "metadata": {
                "categories": list(metadata.get("categories", [])),
                "scenarios": list(metadata.get("scenarios", [])),
                "tags": list(metadata.get("tags", [])),
            },
            "candidates": [
                {
                    "path": document.relative_path,
                    "polluted": bool(document.contamination_reasons),
                    "contamination_reasons": list(document.contamination_reasons),
                    "warning_reasons": list(document.warning_reasons),
                    "quality_score": document.quality_score,
                }
                for document in ordered
            ],
            "output_sha256": _sha256(rendered),
        }
        if archive_reason is not None:
            public_group["archive_reason"] = archive_reason
        group_recovery_decisions = [
            recovery_decisions[document.relative_path]
            for document in ordered
            if document.relative_path in recovery_decisions
        ]
        if len(group_recovery_decisions) > 1:
            raise MigrationSafetyError(
                f"multiple Git recovery entries target one canonical URL: {canonical_url}"
            )
        integrity_decision = (
            group_recovery_decisions[0]
            if group_recovery_decisions
            else _integrity_decision(
                ordered,
                route=route,
                winner=winner,
            )
        )
        if integrity_decision is not None:
            public_group["integrity_decision"] = integrity_decision
        public_groups.append(public_group)
        public_group_by_route[route.path] = public_group

    reference_files = _regular_markdown_files(reference_root)
    writes: list[PlannedWrite] = []
    relref_records: list[dict[str, Any]] = []
    for path in reference_files:
        if path in deletion_documents:
            continue
        before = path.read_bytes()
        base = replacement_bytes.get(path, before)
        try:
            base_text = base.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Markdown is not UTF-8: {path}") from exc
        rewritten, replacements = _rewrite_relrefs(base_text, target_map)
        after = rewritten.encode("utf-8")
        if path in public_group_by_route:
            public_group_by_route[path]["output_sha256"] = _sha256(after)
        operation_path = _relative_operation_path(path, root)
        for source, target, count in replacements:
            relref_records.append(
                {
                    "document": operation_path,
                    "from": source,
                    "to": target,
                    "occurrences": count,
                }
            )
        if after != before:
            writes.append(
                PlannedWrite(
                    path=operation_path,
                    before_sha256=_sha256(before),
                    after_sha256=_sha256(after),
                    content=after,
                )
            )

    deletes = [
        PlannedDelete(path=document.relative_path, before_sha256=_sha256(document.raw))
        for document in deletion_documents.values()
    ]
    writes.sort(key=lambda operation: operation.path)
    deletes.sort(key=lambda operation: operation.path)
    relref_records.sort(
        key=lambda record: (
            str(record["document"]),
            str(record["from"]),
            str(record["to"]),
        )
    )
    base_manifest: dict[str, Any] = {
        "schema_version": "historical_repair_plan_v1",
        "source_root": str(root),
        "dry_run": True,
        "mutation_performed": False,
        "files_scanned": len(paths),
        "repair_group_count": len(public_groups),
        "normalization_group_count": sum(
            group["disposition"] == "normalize_metadata" for group in public_groups
        ),
        "duplicate_group_count": sum(
            int(group["source_file_count"]) > 1 for group in public_groups
        ),
        "duplicate_file_count": len(deletes),
        "planned_changes": len(writes) + len(deletes),
        "groups": public_groups,
        "relref_rewrites": relref_records,
        "issues": sorted(issues, key=lambda issue: (issue["path"], issue["reason"])),
        "git_history_recovery": (
            {
                "enabled": True,
                "audit_path": recovery_manifest.audit_path,
                "audit_sha256": recovery_manifest.audit_sha256,
                "manifest_sha256": recovery_manifest.file_sha256,
                "entry_count": len(recovery_manifest.entries),
                "recovered_count": len(recovery_decisions),
            }
            if recovery_manifest is not None
            else {"enabled": False}
        ),
        "writes": [
            {
                "path": operation.path,
                "before_sha256": operation.before_sha256,
                "after_sha256": operation.after_sha256,
            }
            for operation in writes
        ],
        "deletes": [
            {"path": operation.path, "before_sha256": operation.before_sha256}
            for operation in deletes
        ],
        "execution_policy": {
            "requires_expected_source_sha": True,
            "requires_backup_id": True,
            "requires_max_changes": True,
            "execution_profiles": [
                "shadow_soak_dedupe",
                "reviewed_git_repository",
            ],
            "shadow_soak_profile": "24_runs_3_full_builds_7_day_soak",
            "shadow_soak_batch_limit": 100,
            "reviewed_repository_profile": (
                "clean_codex_branch_exact_head_exact_plan_digest_with_backup"
            ),
            "repository_reviewed_batch_limit": 10_000,
            "atomic_strategy": "compare_and_swap_atomic_replace_with_rollback_backup",
        },
        "selection_policy": {
            "canonical_route": "oldest_frontmatter_date_then_lexical_path",
            "body_source": "clean_candidates_only_then_capped_structural_quality_score",
            "metadata": "body_source_only_with_whitelists_and_eight_tag_cap",
            "active_singletons": (
                "canonical_external_url_and_shared_tag_taxonomy_only; unrelated_metadata_preserved"
            ),
            "all_polluted": "transparent_archive_stub",
            "integrity_recovery": (
                "same_canonical_url_active_complete_candidate_or_transparent_archive"
            ),
            "active_provenance": (
                "legacy_analysis_without_source_snapshot_or_strict_source_brief_tier_c"
            ),
        },
        "execution_blocked": "requires_one_validated_execution_profile",
    }
    manifest = dict(base_manifest)
    manifest["plan_digest"] = sha256_digest(base_manifest)
    return HistoricalRepairPlan(
        content_root=root,
        reference_root=reference_root,
        manifest=manifest,
        writes=tuple(writes),
        deletes=tuple(deletes),
    )


def _with_batch_selection(
    plan: HistoricalRepairPlan,
    selection: Mapping[str, Any],
) -> HistoricalRepairPlan:
    manifest = copy.deepcopy(plan.manifest)
    manifest.pop("plan_digest", None)
    manifest["batch_selection"] = copy.deepcopy(dict(selection))
    manifest["plan_digest"] = sha256_digest(manifest)
    return HistoricalRepairPlan(
        content_root=plan.content_root,
        reference_root=plan.reference_root,
        manifest=manifest,
        writes=plan.writes,
        deletes=plan.deletes,
    )


def build_historical_repair_batch(
    *,
    content_root: str | Path,
    max_changes: int,
    category_whitelist: Iterable[str] = DEFAULT_CATEGORY_WHITELIST,
    scenario_whitelist: Iterable[str] = DEFAULT_SCENARIO_WHITELIST,
) -> HistoricalRepairPlan:
    """Select the largest deterministic canonical-group prefix within one gate.

    The caller repeats this operation after each committed batch. Completed groups
    disappear from the next inventory, while every selected canonical URL is always
    planned with its complete candidate set. This keeps shared relref rewrites based
    on the current filesystem snapshot instead of precomputing stale future batches.
    """

    if (
        not isinstance(max_changes, int)
        or isinstance(max_changes, bool)
        or not 1 <= max_changes <= 100
    ):
        raise MigrationSafetyError("batch --max-changes must be between 1 and 100")

    categories = tuple(category_whitelist)
    scenarios = tuple(scenario_whitelist)
    full_plan = build_historical_repair_plan(
        content_root=content_root,
        category_whitelist=categories,
        scenario_whitelist=scenarios,
    )
    groups = sorted(
        full_plan.manifest["groups"],
        key=lambda group: str(group["canonical_url"]),
    )
    if not groups:
        return _with_batch_selection(
            full_plan,
            {
                "mode": "largest_safe_prefix",
                "atomic_unit": "canonical_url_group",
                "max_changes": max_changes,
                "total_group_count": 0,
                "selected_group_count": 0,
                "remaining_group_count": 0,
                "selected_canonical_urls": [],
                "next_canonical_url": None,
                "full_plan_digest": full_plan.manifest["plan_digest"],
            },
        )

    root = full_plan.content_root
    cache: dict[int, HistoricalRepairPlan] = {}

    def prefix_plan(group_count: int) -> HistoricalRepairPlan:
        cached = cache.get(group_count)
        if cached is not None:
            return cached
        selected_paths = [
            root / relative_path
            for group in groups[:group_count]
            for relative_path in group["paths"]
        ]
        candidate = build_historical_repair_plan(
            content_root=root,
            category_whitelist=categories,
            scenario_whitelist=scenarios,
            input_paths=selected_paths,
        )
        cache[group_count] = candidate
        return candidate

    first = prefix_plan(1)
    first_change_count = int(first.manifest["planned_changes"])
    if first_change_count > max_changes:
        raise MigrationSafetyError(
            "canonical group exceeds --max-changes and cannot be split: "
            f"{groups[0]['canonical_url']} ({first_change_count}>{max_changes})"
        )

    lower = 1
    upper = len(groups)
    while lower < upper:
        middle = (lower + upper + 1) // 2
        candidate = prefix_plan(middle)
        if int(candidate.manifest["planned_changes"]) <= max_changes:
            lower = middle
        else:
            upper = middle - 1

    selected = prefix_plan(lower)
    selected_urls = [str(group["canonical_url"]) for group in groups[:lower]]
    return _with_batch_selection(
        selected,
        {
            "mode": "largest_safe_prefix",
            "atomic_unit": "canonical_url_group",
            "max_changes": max_changes,
            "total_group_count": len(groups),
            "selected_group_count": lower,
            "remaining_group_count": len(groups) - lower,
            "selected_canonical_urls": selected_urls,
            "next_canonical_url": (
                str(groups[lower]["canonical_url"]) if lower < len(groups) else None
            ),
            "full_plan_digest": full_plan.manifest["plan_digest"],
        },
    )


def _operation_path(plan: HistoricalRepairPlan, relative: str) -> Path:
    path = (plan.content_root / relative).absolute()
    if not _is_within(path, plan.reference_root):
        raise UnsafeStorePathError(
            f"historical repair operation escapes reference root: {relative}"
        )
    return path


def _verify_preconditions(plan: HistoricalRepairPlan) -> None:
    for write in plan.writes:
        path = _operation_path(plan, write.path)
        if path.is_symlink() or not path.is_file():
            raise MigrationSafetyError(f"stale repair plan: write source changed: {write.path}")
        if _sha256(path.read_bytes()) != write.before_sha256:
            raise MigrationSafetyError(f"stale repair plan: write source changed: {write.path}")
    for deletion in plan.deletes:
        path = _operation_path(plan, deletion.path)
        if path.is_symlink() or not path.is_file():
            raise MigrationSafetyError(f"stale repair plan: delete source changed: {deletion.path}")
        if _sha256(path.read_bytes()) != deletion.before_sha256:
            raise MigrationSafetyError(f"stale repair plan: delete source changed: {deletion.path}")


def _atomic_write(path: Path, payload: bytes, *, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    finally:
        Path(temporary_name).unlink(missing_ok=True)


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    payload = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    _atomic_write(path, payload, mode=0o600)


def _backup_relative_path(plan: HistoricalRepairPlan, path: Path) -> Path:
    try:
        return path.relative_to(plan.reference_root)
    except ValueError as exc:
        raise UnsafeStorePathError(f"backup source escapes reference root: {path}") from exc


def _verify_applied(plan: HistoricalRepairPlan) -> None:
    for write in plan.writes:
        path = _operation_path(plan, write.path)
        if not path.is_file() or _sha256(path.read_bytes()) != write.after_sha256:
            raise MigrationSafetyError(f"applied repair receipt does not match: {write.path}")
    for deletion in plan.deletes:
        if _operation_path(plan, deletion.path).exists():
            raise MigrationSafetyError(f"applied repair receipt does not match: {deletion.path}")


def _repository_review_state(reference_root: Path) -> tuple[str, str]:
    branch_result = subprocess.run(
        ["git", "-C", str(reference_root), "symbolic-ref", "--quiet", "--short", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if branch_result.returncode != 0:
        raise MigrationSafetyError("reviewed repository repair requires an attached branch")
    status_result = subprocess.run(
        [
            "git",
            "-C",
            str(reference_root),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if status_result.returncode != 0:
        raise MigrationSafetyError("reviewed repository repair cannot read Git worktree state")
    return branch_result.stdout.strip(), status_result.stdout.strip()


def _restore_from_backup(
    plan: HistoricalRepairPlan,
    *,
    backup_directory: Path,
    affected_paths: Iterable[Path],
) -> None:
    before_root = backup_directory / "before"
    for path in sorted(set(affected_paths), key=lambda candidate: str(candidate)):
        backup = before_root / _backup_relative_path(plan, path)
        if backup.is_file():
            _atomic_write(path, backup.read_bytes(), mode=backup.stat().st_mode & 0o777)
        else:
            path.unlink(missing_ok=True)


def apply_historical_repair_plan(
    plan: HistoricalRepairPlan,
    *,
    expected_source_sha: str | None,
    expected_code_sha: str | None,
    backup_id: str | None,
    max_changes: int | None,
    shadow_evidence_root: Path | None,
    backup_root: Path,
    expected_plan_digest: str | None = None,
    repository_reviewed: bool = False,
) -> dict[str, Any]:
    """Apply a reviewed plan after one explicit safety profile validates it."""

    issues = plan.manifest.get("issues")
    if not isinstance(issues, list) or issues:
        issue_count = len(issues) if isinstance(issues, list) else "unknown"
        raise MigrationSafetyError(f"historical repair plan has unresolved issues: {issue_count}")

    safety_profile = "shadow_soak_dedupe"
    if repository_reviewed:
        validate_execution_gate(
            execute=True,
            expected_source_sha=expected_source_sha,
            backup_id=backup_id,
            max_changes=max_changes,
            actual_source_sha=source_revision(plan.content_root),
        )
        if expected_plan_digest != plan.manifest["plan_digest"]:
            raise MigrationSafetyError("reviewed repository repair plan digest mismatch")
        branch, worktree_status = _repository_review_state(plan.reference_root)
        if not branch.startswith("codex/"):
            raise MigrationSafetyError("reviewed repository repair requires a codex/ branch")
        if worktree_status:
            raise MigrationSafetyError("reviewed repository repair requires a clean Git worktree")
        safety_profile = "reviewed_git_repository"
    else:
        validate_dedupe_execution_gate(
            content_root=plan.content_root,
            expected_source_sha=expected_source_sha,
            expected_code_sha=expected_code_sha,
            backup_id=backup_id,
            max_changes=max_changes,
            shadow_evidence_root=shadow_evidence_root,
        )
    if backup_id is None or not _BACKUP_ID.fullmatch(backup_id):
        raise MigrationSafetyError("--backup-id must be a safe identifier")
    if not isinstance(max_changes, int) or isinstance(max_changes, bool):
        raise MigrationSafetyError("--max-changes must be an integer")
    planned_changes = int(plan.manifest["planned_changes"])
    if planned_changes > max_changes:
        raise MigrationSafetyError(
            f"planned changes exceed --max-changes: {planned_changes}>{max_changes}"
        )

    backup_root = Path(backup_root).absolute()
    if backup_root.is_symlink() or (backup_root.exists() and not backup_root.is_dir()):
        raise UnsafeStorePathError(f"repair backup root is unsafe: {backup_root}")
    backup_directory = backup_root / backup_id
    receipt_path = backup_directory / "receipt.json"
    if receipt_path.is_file():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MigrationSafetyError(f"repair receipt is unreadable: {receipt_path}") from exc
        if receipt.get("plan_digest") != plan.manifest["plan_digest"]:
            raise MigrationSafetyError("backup id already belongs to a different repair plan")
        _verify_applied(plan)
        return {
            "schema_version": "historical_repair_result_v1",
            "plan_digest": plan.manifest["plan_digest"],
            "backup_id": backup_id,
            "already_applied": True,
            "mutation_performed": False,
            "changed_files": 0,
            "safety_profile": receipt.get("safety_profile", safety_profile),
        }
    if backup_directory.exists() or backup_directory.is_symlink():
        raise MigrationSafetyError(
            f"incomplete or conflicting repair backup exists: {backup_directory}"
        )

    _verify_preconditions(plan)
    affected_paths = [
        *(_operation_path(plan, operation.path) for operation in plan.writes),
        *(_operation_path(plan, operation.path) for operation in plan.deletes),
    ]
    backup_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    staging = Path(tempfile.mkdtemp(prefix=f".{backup_id}.", dir=backup_root))
    try:
        before_root = staging / "before"
        for path in sorted(set(affected_paths), key=lambda candidate: str(candidate)):
            relative = _backup_relative_path(plan, path)
            destination = before_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        _atomic_json(staging / "plan.json", plan.manifest)
        os.replace(staging, backup_directory)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    receipt = {
        "schema_version": "historical_repair_receipt_v1",
        "plan_digest": plan.manifest["plan_digest"],
        "backup_id": backup_id,
        "expected_source_sha": expected_source_sha,
        "expected_code_sha": expected_code_sha,
        "planned_changes": planned_changes,
        "safety_profile": safety_profile,
        "state": "applied",
    }
    try:
        for write in plan.writes:
            path = _operation_path(plan, write.path)
            mode = path.stat().st_mode & 0o777
            _atomic_write(path, write.content, mode=mode)
        for deletion in plan.deletes:
            _operation_path(plan, deletion.path).unlink()
        _verify_applied(plan)
        _atomic_json(receipt_path, receipt)
    except BaseException:
        receipt_path.unlink(missing_ok=True)
        _restore_from_backup(
            plan,
            backup_directory=backup_directory,
            affected_paths=affected_paths,
        )
        raise

    return {
        "schema_version": "historical_repair_result_v1",
        "plan_digest": plan.manifest["plan_digest"],
        "backup_id": backup_id,
        "already_applied": False,
        "mutation_performed": bool(planned_changes),
        "changed_files": planned_changes,
        "safety_profile": safety_profile,
    }


def write_repair_manifest(path: str | Path, manifest: Mapping[str, Any]) -> None:
    """Write an explicitly requested audit manifest with an atomic replacement."""

    destination = Path(path).absolute()
    if destination.is_symlink() or destination.parent.is_symlink():
        raise UnsafeStorePathError(f"repair manifest path must not be a symlink: {destination}")
    _atomic_json(destination, manifest)


__all__ = [
    "DEFAULT_CATEGORY_WHITELIST",
    "DEFAULT_SCENARIO_WHITELIST",
    "HistoricalRepairPlan",
    "PlannedDelete",
    "PlannedWrite",
    "apply_historical_repair_plan",
    "build_historical_repair_batch",
    "build_historical_repair_plan",
    "write_repair_manifest",
]
