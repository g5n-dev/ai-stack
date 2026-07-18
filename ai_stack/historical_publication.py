"""Pure, evidence-only publication helpers for historical source captures.

The adapter deliberately accepts no historical body.  Only the caller-owned
route metadata (``date`` and ``aliases``) can cross the boundary; every factual
field is rebuilt from a bounded :class:`HistoricalSourceCapture`, hash-bound by
the shared source contract, and rendered as a Tier-C source brief.
"""

from __future__ import annotations

import hashlib
import html
import re
import unicodedata
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import urlsplit

import yaml

from content_security import ContentSecurityError, validate_markdown_document
from crawler.historical_source_fetch import HistoricalSourceCapture

from .content_quality import analyze_post
from .historical_taxonomy import infer_historical_taxonomy
from .publication_security import sensitive_publication_reasons
from .source_contract import (
    SourceContractError,
    apply_source_contract,
    publication_title_from_contract,
    verify_source_contract,
)

_CAPTURE_SPECS: dict[str, tuple[str, str, str]] = {
    "arxiv": ("abstract", "abstract_only", "arxiv_api"),
    "github_trending": (
        "metadata_only",
        "metadata_only",
        "repository_metadata",
    ),
    "hacker_news": ("metadata_only", "metadata_only", "api_metadata"),
    "blogs_podcasts": ("excerpt", "partial", "article_html_excerpt"),
    "juejin": ("excerpt", "partial", "article_html_excerpt"),
}
_MAX_CAPTURE_TITLE_CHARS = 300
_MAX_CAPTURE_TEXT_BYTES = 24 * 1024
_MAX_PUBLICATION_EXCERPT_CHARS = 800
_MIN_PUBLICATION_EXCERPT_BOUNDARY = 480
_MAX_ALIAS_CHARS = 512
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]")
_MARKDOWN_SPECIAL = re.compile(r"([\\`*{}\[\]()_])")
_JUEJIN_ARTICLE_PATH = re.compile(r"^/post/([1-9]\d{5,24})/?$")


class HistoricalPublicationError(ValueError):
    """Raised when recovered evidence cannot produce a safe Tier-C Post."""


def _one_line(value: object) -> str:
    return " ".join(str(value or "").split()).strip()


def _capture_timestamp(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        raise HistoricalPublicationError("capture time is missing")
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise HistoricalPublicationError("capture time is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise HistoricalPublicationError("capture time requires a timezone")
    return text


def _route_date(value: object) -> object:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise HistoricalPublicationError("historical date requires a timezone")
        return value
    if not isinstance(value, str):
        raise HistoricalPublicationError("historical date must be a string or datetime")
    text = value.strip()
    if not text or text != value:
        raise HistoricalPublicationError("historical date is missing")
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise HistoricalPublicationError("historical date is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise HistoricalPublicationError("historical date requires a timezone")
    return value


def _route_aliases(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise HistoricalPublicationError("historical aliases must be a list")
    aliases: list[str] = []
    for raw in value:
        if not isinstance(raw, str):
            raise HistoricalPublicationError("historical alias must be a string")
        alias = raw.strip()
        try:
            parsed = urlsplit(alias)
        except ValueError as exc:
            raise HistoricalPublicationError("historical alias is unsafe") from exc
        if (
            raw != alias
            or not alias.startswith("/")
            or len(alias) > _MAX_ALIAS_CHARS
            or _CONTROL_CHARACTERS.search(alias)
            or "\\" in alias
            or parsed.scheme
            or parsed.netloc
            or parsed.query
            or parsed.fragment
            or ".." in PurePosixPath(parsed.path).parts
        ):
            raise HistoricalPublicationError("historical alias is unsafe")
        aliases.append(alias)
    return aliases


def _metadata_mapping(capture: HistoricalSourceCapture) -> Mapping[str, Any]:
    if not isinstance(capture.metadata, Mapping):
        raise HistoricalPublicationError("capture metadata must be a mapping")
    return capture.metadata


def _string_list(value: object, *, field: str, maximum_items: int = 20) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise HistoricalPublicationError(f"capture {field} must be a list")
    result = [_one_line(item) for item in value]
    if any(not item for item in result) or len(result) > maximum_items:
        raise HistoricalPublicationError(f"capture {field} is invalid")
    return result


def _integer(value: object, *, field: str) -> int:
    if isinstance(value, bool):
        raise HistoricalPublicationError(f"capture {field} is invalid")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise HistoricalPublicationError(f"capture {field} is invalid") from exc
    if number < 0:
        raise HistoricalPublicationError(f"capture {field} is invalid")
    return number


def _bounded_publication_excerpt(source: str, source_text: str) -> tuple[str, bool]:
    text = unicodedata.normalize("NFC", source_text).strip()
    if source not in {"blogs_podcasts", "juejin"} or len(text) <= (
        _MAX_PUBLICATION_EXCERPT_CHARS
    ):
        return text, False
    prefix = text[: _MAX_PUBLICATION_EXCERPT_CHARS - 1]
    boundary = max(
        prefix.rfind(marker) + len(marker)
        for marker in ("\n\n", "。", "！", "？", ". ", "! ", "? ")
    )
    if boundary < _MIN_PUBLICATION_EXCERPT_BOUNDARY:
        boundary = len(prefix)
    return f"{prefix[:boundary].rstrip()}…", True


def _public_text_values(value: object) -> list[str]:
    if isinstance(value, Mapping):
        return [
            text
            for key, child in value.items()
            if str(key) not in {"captured_at", "crawled_at"}
            for text in _public_text_values(child)
        ]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [text for child in value for text in _public_text_values(child)]
    return [value] if isinstance(value, str) else []


def _reject_sensitive_publication_fields(value: Mapping[str, Any]) -> None:
    reasons = sensitive_publication_reasons("\n".join(_public_text_values(value)))
    if reasons:
        raise HistoricalPublicationError(
            f"capture public fields contain sensitive content: {reasons[0]}"
        )


def capture_to_source_contract_item(
    capture: HistoricalSourceCapture,
) -> dict[str, Any]:
    """Convert one bounded capture into a verified source-contract item."""

    if not isinstance(capture, HistoricalSourceCapture):
        raise HistoricalPublicationError("historical capture type is invalid")
    source = _one_line(capture.source).casefold()
    spec = _CAPTURE_SPECS.get(source)
    if spec is None:
        raise HistoricalPublicationError(f"historical source is unsupported: {source}")
    expected_mode, expected_completeness, discovery_method = spec
    if capture.capture_mode != expected_mode:
        raise HistoricalPublicationError("capture mode does not match the source")
    if capture.source_completeness != expected_completeness:
        raise HistoricalPublicationError("capture completeness does not match the mode")
    if not isinstance(capture.source_is_truncated, bool):
        raise HistoricalPublicationError("capture truncation flag must be boolean")

    title = _one_line(capture.title)
    captured_source_text = str(capture.source_text or "").strip()
    if not title:
        raise HistoricalPublicationError("capture title is missing")
    if len(title) > _MAX_CAPTURE_TITLE_CHARS:
        raise HistoricalPublicationError("capture title exceeds the publication limit")
    if not captured_source_text:
        raise HistoricalPublicationError("capture source text is missing")
    if len(captured_source_text.encode("utf-8")) > _MAX_CAPTURE_TEXT_BYTES:
        raise HistoricalPublicationError("capture source text exceeds the evidence limit")
    source_text, publication_excerpt_truncated = _bounded_publication_excerpt(
        source, captured_source_text
    )
    captured_at = _capture_timestamp(capture.captured_at)
    metadata = _metadata_mapping(capture)
    external_url = str(capture.external_url or "").strip()
    try:
        parsed_url = urlsplit(external_url)
    except ValueError as exc:
        raise HistoricalPublicationError("capture external URL is unsafe") from exc
    if (
        not external_url
        or len(external_url) > 4096
        or any(character.isspace() or character in '<>"\'' for character in external_url)
        or parsed_url.scheme.casefold() not in {"http", "https"}
        or not parsed_url.hostname
        or parsed_url.username is not None
        or parsed_url.password is not None
    ):
        raise HistoricalPublicationError("capture external URL is unsafe")

    truncation_reasons = (
        ["historical_capture_limit"] if capture.source_is_truncated else []
    )
    if source == "juejin":
        article_id = _one_line(metadata.get("article_id"))
        article_match = _JUEJIN_ARTICLE_PATH.fullmatch(parsed_url.path)
        if (
            parsed_url.hostname not in {"juejin.cn", "www.juejin.cn"}
            or article_match is None
            or not article_id
            or article_match.group(1) != article_id
        ):
            raise HistoricalPublicationError(
                "capture Juejin article_id does not match its source URL"
            )
        if not capture.source_is_truncated:
            raise HistoricalPublicationError(
                "capture Juejin excerpt must be marked truncated"
            )
        if _one_line(metadata.get("source_truncation_reason")) != (
            "historical_excerpt_only"
        ):
            raise HistoricalPublicationError(
                "capture Juejin truncation reason is invalid"
            )
        truncation_reasons = ["historical_excerpt_only"]
    if publication_excerpt_truncated:
        truncation_reasons.append("historical_publication_excerpt_limit")
    source_is_truncated = capture.source_is_truncated or publication_excerpt_truncated
    truncation_reason = ",".join(dict.fromkeys(truncation_reasons))

    raw: dict[str, Any] = {
        "source": source,
        "title": title,
        "url": external_url,
        "captured_at": captured_at,
        "crawled_at": captured_at,
        "discovery_method": discovery_method,
        "fetch_status": "captured",
        "source_completeness": expected_completeness,
        "source_is_truncated": source_is_truncated,
        "source_truncation_reason": truncation_reason,
        "tags": ["掘金"] if source == "juejin" else [],
        "source_capture_sha256": (
            "sha256:"
            + hashlib.sha256(captured_source_text.encode("utf-8")).hexdigest()
        ),
        "source_capture_chars_original": len(captured_source_text),
        "source_publication_excerpt_chars": len(source_text),
    }
    if source == "arxiv":
        arxiv_id = _one_line(metadata.get("arxiv_id"))
        if not arxiv_id:
            raise HistoricalPublicationError("capture arxiv_id is missing")
        pdf_url = _one_line(metadata.get("pdf_url"))
        if pdf_url:
            try:
                parsed_pdf_url = urlsplit(pdf_url)
            except ValueError as exc:
                raise HistoricalPublicationError("capture ArXiv PDF URL is invalid") from exc
            if (
                parsed_pdf_url.scheme.casefold() != "https"
                or parsed_pdf_url.hostname != "arxiv.org"
                or parsed_pdf_url.path != f"/pdf/{arxiv_id}.pdf"
                or parsed_pdf_url.query
                or parsed_pdf_url.fragment
                or parsed_pdf_url.username is not None
                or parsed_pdf_url.password is not None
            ):
                raise HistoricalPublicationError("capture ArXiv PDF URL is invalid")
        raw.update(
            {
                "summary": source_text,
                "arxiv_id": arxiv_id,
                "authors": _string_list(
                    metadata.get("authors"), field="authors", maximum_items=100
                ),
                "category": _one_line(metadata.get("category")),
                "published": _one_line(metadata.get("published")),
                "pdf_url": pdf_url,
            }
        )
    elif source == "github_trending":
        raw.update(
            {
                "description": source_text,
                "language": _one_line(metadata.get("language")),
                "stars": _integer(metadata.get("stars", 0), field="stars"),
                "today_stars": _integer(
                    metadata.get("today_stars", 0), field="today_stars"
                ),
                "forks": _integer(metadata.get("forks", 0), field="forks"),
                "license": _one_line(metadata.get("license")),
                "topics": _string_list(
                    metadata.get("topics"), field="topics", maximum_items=20
                ),
            }
        )
    elif source == "hacker_news":
        if _one_line(source_text) != title:
            raise HistoricalPublicationError(
                "capture Hacker News source text must match its metadata title"
            )
        hn_id = _integer(metadata.get("hn_id"), field="hn_id")
        if hn_id <= 0:
            raise HistoricalPublicationError("capture hn_id is invalid")
        raw.update(
            {
                "hn_id": hn_id,
                "author": _one_line(metadata.get("author")),
                "score": _integer(metadata.get("score", 0), field="score"),
                "descendants": _integer(
                    metadata.get("descendants", 0), field="descendants"
                ),
                "published": _one_line(metadata.get("published")),
            }
        )
    elif source in {"blogs_podcasts", "juejin"}:
        raw.update(
            {
                "summary": source_text,
                "author": _one_line(metadata.get("author")),
                "published": _one_line(metadata.get("published")),
            }
        )

    _reject_sensitive_publication_fields(raw)

    try:
        contracted = apply_source_contract(raw)
        verify_source_contract(contracted)
    except SourceContractError as exc:
        raise HistoricalPublicationError(f"source contract rejected capture: {exc}") from exc
    if contracted.get("content_mode") != "source_brief":
        raise HistoricalPublicationError("historical capture did not produce a source brief")
    if contracted.get("publication_tier") != "C":
        raise HistoricalPublicationError("historical capture did not produce Tier C")
    if contracted.get("source_capture_mode") != expected_mode:
        raise HistoricalPublicationError("source contract changed the capture mode")
    if contracted.get("source_completeness") != expected_completeness:
        raise HistoricalPublicationError("source contract changed capture completeness")
    if contracted.get("source_is_truncated") is not source_is_truncated:
        raise HistoricalPublicationError("source contract changed capture truncation")
    return contracted


def _markdown_text(value: object) -> str:
    text = unicodedata.normalize("NFC", str(value or ""))
    text = html.escape(text, quote=False)
    text = text.replace("{{", "&#123;&#123;").replace("}}", "&#125;&#125;")
    return _MARKDOWN_SPECIAL.sub(r"\\\1", text)


def _frontmatter_text(value: object) -> str:
    text = unicodedata.normalize("NFC", _one_line(value))
    return (
        text.replace("{{", "｛｛")
        .replace("}}", "｝｝")
        .replace("<", "＜")
        .replace(">", "＞")
    )


def _source_note(capture_mode: str, source: str) -> str:
    if capture_mode == "abstract":
        return "当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。"
    if capture_mode == "excerpt":
        return "当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。"
    if source == "hacker_news":
        return "当前只保存了来源元数据，未抓取外链全文。请以原始来源和 Hacker News 讨论为准。"
    return "当前只保存了来源元数据，未抓取完整正文。请以原始来源为准。"


def _render_body(item: Mapping[str, Any]) -> str:
    evidence = item.get("evidence")
    if not isinstance(evidence, Mapping):
        raise HistoricalPublicationError("source evidence is missing during render")
    fields = evidence.get("fields")
    if not isinstance(fields, Mapping):
        raise HistoricalPublicationError("source evidence fields are missing during render")
    source = str(evidence.get("source") or "").strip()
    capture_mode = str(evidence.get("capture_mode") or "").strip()
    url = str(evidence.get("external_url") or "").strip()
    lines = [
        "## 基本信息",
        "",
        f"- **来源**: {_markdown_text(source)}",
        f"- **原始来源**: [{_markdown_text(url)}](<{url}>)",
    ]
    if source == "arxiv":
        authors = fields.get("authors")
        if isinstance(authors, list) and authors:
            lines.append(f"- **作者**: {_markdown_text(', '.join(map(str, authors)))}")
        if fields.get("category"):
            lines.append(f"- **分类**: {_markdown_text(fields.get('category'))}")
        if fields.get("published"):
            lines.append(f"- **论文时间**: {_markdown_text(fields.get('published'))}")
        pdf_url = str(fields.get("pdf_url") or "").strip()
        if pdf_url:
            lines.append(f"- **论文 PDF**: [{_markdown_text(pdf_url)}](<{pdf_url}>)")
    elif source == "github_trending":
        if fields.get("language"):
            lines.append(f"- **主要语言**: {_markdown_text(fields.get('language'))}")
        lines.append(f"- **Stars**: {_markdown_text(fields.get('stars', 0))}")
        if fields.get("forks"):
            lines.append(f"- **Forks**: {_markdown_text(fields.get('forks'))}")
        if fields.get("license"):
            lines.append(f"- **许可证**: {_markdown_text(fields.get('license'))}")
        topics = fields.get("topics")
        if isinstance(topics, list) and topics:
            lines.append(f"- **Topics**: {_markdown_text(', '.join(map(str, topics)))}")
    elif source == "hacker_news":
        if fields.get("author"):
            lines.append(f"- **作者**: {_markdown_text(fields.get('author'))}")
        lines.extend(
            [
                f"- **评分**: {_markdown_text(fields.get('score', 0))}",
                f"- **评论数**: {_markdown_text(fields.get('descendants', 0))}",
            ]
        )
        hn_id = fields.get("hn_id")
        if hn_id:
            hn_url = f"https://news.ycombinator.com/item?id={int(hn_id)}"
            lines.append(f"- **HN 讨论**: [{hn_url}](<{hn_url}>)")
    else:
        if fields.get("author"):
            lines.append(f"- **作者**: {_markdown_text(fields.get('author'))}")
        if fields.get("published"):
            lines.append(f"- **来源时间**: {_markdown_text(fields.get('published'))}")

    source_text = str(item.get("source_display_excerpt") or "").strip()
    if capture_mode != "metadata_only" and source_text:
        truncation_reason = str(item.get("source_truncation_reason") or "")
        lines.extend(["", "## 来源摘要/节选", ""])
        if "historical_publication_excerpt_limit" in truncation_reason.split(","):
            lines.extend(
                [
                    "公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。",
                    "",
                ]
            )
        lines.extend(
            f"> {_markdown_text(line)}" if line.strip() else ">"
            for line in source_text.splitlines()
        )
    elif source == "github_trending" and source_text:
        lines.extend(
            [
                "",
                "## 已保存元数据",
                "",
                _markdown_text(source_text),
            ]
        )

    lines.extend(
        [
            "",
            "## 来源说明",
            "",
            _source_note(capture_mode, source),
            "",
            "> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。",
        ]
    )
    return "\n".join(lines).strip()


def render_historical_tier_c_markdown(
    capture: HistoricalSourceCapture,
    *,
    prior_metadata: Mapping[str, Any],
) -> str:
    """Render a safe Tier-C Post while preserving only date and aliases."""

    if not isinstance(prior_metadata, Mapping):
        raise HistoricalPublicationError("prior metadata must be a mapping")
    date = _route_date(prior_metadata.get("date"))
    aliases = _route_aliases(prior_metadata.get("aliases"))
    item = capture_to_source_contract_item(capture)
    verify_source_contract(item)
    taxonomy = infer_historical_taxonomy(capture)
    evidence = item["evidence"]
    source = str(evidence["source"])
    title = _frontmatter_text(publication_title_from_contract(item))
    capture_mode = str(item["source_capture_mode"])
    frontmatter: dict[str, Any] = {
        "title": title,
        "date": date,
        "draft": False,
        "entry_kind": "auto",
        "tags": list(taxonomy["tags"]),
        "categories": list(taxonomy["categories"]),
        "scenarios": list(taxonomy["scenarios"]),
        "source": source,
        "description": _source_note(capture_mode, source),
        "external_url": str(evidence["external_url"]),
        "aliases": aliases,
        "content_mode": "source_brief",
        "publication_tier": "C",
        "source_capture_mode": capture_mode,
        "source_snapshot_sha256": str(item["source_snapshot_sha256"]),
        "extractor_version": str(item["extractor_version"]),
        "discovery_method": str(item["discovery_method"]),
        "fetch_status": str(item["fetch_status"]),
        "source_completeness": str(item["source_completeness"]),
        "source_is_truncated": bool(item["source_is_truncated"]),
        "source_support": 1.0,
        "source_title_chars_original": int(item["source_title_chars_original"]),
        "captured_at": str(item["captured_at"]),
        "source_capture_sha256": str(item["source_capture_sha256"]),
        "source_capture_chars_original": int(item["source_capture_chars_original"]),
        "source_publication_excerpt_chars": int(
            item["source_publication_excerpt_chars"]
        ),
    }
    truncation_reason = str(item.get("source_truncation_reason") or "").strip()
    if truncation_reason:
        frontmatter["source_truncation_reason"] = truncation_reason
    encoded = yaml.safe_dump(
        frontmatter,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip()
    document = f"---\n{encoded}\n---\n\n{_render_body(item)}\n"
    try:
        validate_markdown_document(document)
    except ContentSecurityError as exc:
        raise HistoricalPublicationError(
            "rendered historical source brief failed security gate"
        ) from exc
    analysis = analyze_post(document)
    if analysis.status != "source_brief" or analysis.fatal_reasons:
        reasons = ", ".join(analysis.fatal_reasons) or analysis.status
        raise HistoricalPublicationError(
            f"rendered historical source brief failed quality gate: {reasons}"
        )
    return document


__all__ = [
    "HistoricalPublicationError",
    "capture_to_source_contract_item",
    "render_historical_tier_c_markdown",
]
