"""Shared, conservative quality gates for generated historical content."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any

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
)


def synthetic_body_reasons(body: str) -> tuple[str, ...]:
    """Return deterministic high-confidence reasons for unverifiable synthesis."""
    text = unicodedata.normalize("NFC", str(body or ""))
    if not text.strip():
        return ("empty_body",)

    reasons = {
        reason
        for reason, pattern in _SYNTHETIC_BODY_PATTERNS
        if pattern.search(text)
    }
    return tuple(sorted(reasons))


def is_synthetic_body(body: str) -> bool:
    """Return whether the body fails the high-confidence provenance gate."""
    return bool(synthetic_body_reasons(body))


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


def build_content_quality_manifest(content_root: Path | str) -> dict[str, Any]:
    """Build a deterministic Hugo data manifest for quarantined archive pages."""
    root = Path(content_root).resolve()
    pages: dict[str, dict[str, Any]] = {}
    reason_counts: Counter[str] = Counter()
    source_hash = hashlib.sha256()
    source_file_count = 0
    quarantined_count = 0
    archived_count = 0

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
        if metadata.get("archived") is True:
            status = "archived"
            reasons = ("archived_content",)
            archived_count += 1
        else:
            status = "quarantined"
            reasons = synthetic_body_reasons(markdown_body(document))
            if reasons:
                quarantined_count += 1
        if not reasons:
            continue
        reason_counts.update(reasons)
        pages[relative] = {
            "status": status,
            "reasons": list(reasons),
        }

    return {
        "schema_version": "content_quality_manifest_v1",
        "source_tree_sha256": source_hash.hexdigest(),
        "source_file_count": source_file_count,
        "quarantined_count": quarantined_count,
        "archived_count": archived_count,
        "reason_counts": dict(sorted(reason_counts.items())),
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
