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
_DESCRIPTION_START_RE = re.compile(
    r"(?m)^(?:##\s+描述\s*|-\s*\*\*描述\*\*\s*[:：])"
)
_TRANSLATION_RESPONSE_RE = re.compile(
    r"(?:您好[！!，,\s]*)?(?:(?:我)?注意到|我发现)?"
    r"(?:您提供的)?(?:这段|以下)?内容.{0,40}"
    r"(?:已经是中文|本身已经是中文|翻译成英文|提供相应的英文版本)",
    re.IGNORECASE | re.DOTALL,
)
_HEADING_LINE_RE = re.compile(r"^(?P<marks>#{2,6})[ \t]+\S.*$")
_EXPLICIT_TRUNCATION_RE = re.compile(r"\[\s*\.{3}\s*truncated\s*\]", re.IGNORECASE)
_HTTP_SCHEMES = frozenset({"http", "https"})
_SOURCE_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_SOURCE_CAPTURE_MODES = frozenset(
    {"abstract", "excerpt", "metadata_only", "social_post"}
)
_STANDARD_FOOTER_PREFIXES = (
    "*本文由 AI Stack",
    "*这篇文章由 AI Stack",
    "**📚 更多精彩内容",
)
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


def synthetic_body_reasons(body: str) -> tuple[str, ...]:
    """Return deterministic high-confidence reasons for unverifiable synthesis."""
    raw_text = unicodedata.normalize("NFC", str(body or ""))
    if not raw_text.strip():
        return ("empty_body",)
    text = _prose_without_code(raw_text)

    reasons = {
        reason
        for reason, pattern in _SYNTHETIC_BODY_PATTERNS
        if pattern.search(text)
    }
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

    description_start = _DESCRIPTION_START_RE.search(prose[:1_800])
    if description_start is not None:
        window = prose[description_start.start() : description_start.start() + 700]
        if _TRANSLATION_RESPONSE_RE.search(window):
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


def remove_empty_section_headings(body: str) -> tuple[str, int]:
    """Remove empty shell headings without generating replacement prose."""

    cleaned = str(body or "")
    removed = 0
    while True:
        indexes = set(_empty_section_heading_indexes(cleaned))
        if not indexes:
            return cleaned, removed
        lines = cleaned.splitlines(keepends=True)
        cleaned = "".join(
            line for index, line in enumerate(lines) if index not in indexes
        )
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
        modern_provenance = (
            str(metadata.get("publication_tier") or "").strip() == "C"
            and str(metadata.get("source_capture_mode") or "").strip()
            in _SOURCE_CAPTURE_MODES
            and bool(
                _SOURCE_DIGEST_RE.fullmatch(
                    str(metadata.get("source_snapshot_sha256") or "").strip()
                )
            )
            and str(metadata.get("extractor_version") or "").strip()
            == "source-contract-v1"
            and bool(str(metadata.get("discovery_method") or "").strip())
            and isinstance(metadata.get("source_is_truncated"), bool)
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
    maximum_bytes = 32_000 if declared_mode == "source_brief" else 1_200
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


def _unterminated_legacy_hn_prose(metadata: Mapping[str, Any], body: str) -> bool:
    if str(metadata.get("source") or "").strip().casefold() != "hacker_news":
        return False
    if is_source_brief(metadata, body):
        return False
    lines = [
        line.strip()
        for line in _prose_without_code(body).splitlines()
        if line.strip() and line.strip() not in {"---", "***", "___"}
    ]
    while lines and lines[-1].startswith(_STANDARD_FOOTER_PREFIXES):
        lines.pop()
    if not lines:
        return False
    tail = lines[-1]
    if re.search(r"\]\([^)]*\)$", tail):
        return False
    plain = re.sub(r"[*_`]+$", "", tail).strip()
    if re.search(r"[。！？.!?；;：:）)】\]”’」』…]$", plain):
        return False
    if re.match(r"^(?:[-+*]|\d+[.)])\s+", tail):
        return bool(re.search(r"[，,:：、（(\[/=\\-]$", plain))
    return len(plain) >= 20 and bool(re.search(r"[\u3400-\u9fff]", plain))


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
    if _unterminated_legacy_hn_prose(metadata, body):
        fatal.add("unterminated_prose")

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
        "schema_version": "content_quality_manifest_v3",
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
