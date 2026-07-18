"""Conservative taxonomy derived only from newly captured source evidence."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping

from crawler.historical_source_fetch import HistoricalSourceCapture

from .tag_taxonomy import normalize_tags

_BASE_TAG = {
    "arxiv": "ArXiv",
    "github_trending": "GitHub",
    "hacker_news": "Hacker News",
    "blogs_podcasts": "博客与播客",
    "juejin": "掘金",
}
_SEMANTIC_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("MCP", re.compile(r"\b(?:mcp|model[ -]context[ -]protocol)\b", re.I)),
    ("RAG", re.compile(r"\b(?:rag|retrieval[ -]augmented(?:[ -]generation)?)\b", re.I)),
    ("AI Agent", re.compile(r"\b(?:agentic|ai[ -]agents?|agents?)\b|智能体", re.I)),
    ("大语言模型", re.compile(r"\b(?:llms?|large[ -]language[ -]models?)\b|大语言模型", re.I)),
    ("机器学习", re.compile(r"\bmachine[ -]learning\b|机器学习", re.I)),
    ("深度学习", re.compile(r"\bdeep[ -]learning\b|深度学习", re.I)),
    (
        "自然语言处理",
        re.compile(r"\b(?:nlp|natural[ -]language[ -]processing)\b|自然语言处理", re.I),
    ),
    ("计算机视觉", re.compile(r"\bcomputer[ -]vision\b|计算机视觉", re.I)),
    ("生成式 AI", re.compile(r"\bgenerative[ -]ai\b|生成式\s*AI", re.I)),
    ("AI 安全", re.compile(r"\b(?:ai[ -]safety|prompt[ -]injection|jailbreak)\b|AI\s*安全", re.I)),
)
_LANGUAGES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Python", re.compile(r"\bpython\b", re.I)),
    ("Rust", re.compile(r"\brust\b", re.I)),
    ("TypeScript", re.compile(r"\btypescript\b", re.I)),
    ("JavaScript", re.compile(r"\bjavascript\b", re.I)),
    ("Go", re.compile(r"\bgolang\b|\bgo[ -](?:language|runtime|module)\b", re.I)),
    ("Java", re.compile(r"\bjava\b", re.I)),
    ("Kotlin", re.compile(r"\bkotlin\b", re.I)),
    ("Swift", re.compile(r"\bswift\b", re.I)),
    ("C++", re.compile(r"\bc\+\+\b", re.I)),
)
_INFRA_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("命令行工具", re.compile(r"\b(?:cli|command[ -]line)\b|命令行", re.I)),
    ("Kubernetes", re.compile(r"\b(?:kubernetes|k8s)\b", re.I)),
    ("Docker", re.compile(r"\b(?:docker|container)\b|容器", re.I)),
    (
        "数据库",
        re.compile(
            r"\b(?:database|postgresql|mysql|sqlite|vector[ -]database)\b|数据库",
            re.I,
        ),
    ),
)
_SAFE_TOPIC = re.compile(r"^[A-Za-z0-9][A-Za-z0-9+_.-]{0,47}$")
_AI_TAGS = frozenset(tag for tag, _pattern in _SEMANTIC_RULES)


def _text(value: object) -> str:
    return " ".join(unicodedata.normalize("NFC", str(value or "")).split()).strip()


def _metadata(capture: HistoricalSourceCapture) -> Mapping[str, object]:
    return capture.metadata if isinstance(capture.metadata, Mapping) else {}


def _topic_text(metadata: Mapping[str, object]) -> str:
    topics = metadata.get("topics")
    if not isinstance(topics, (list, tuple)):
        return ""
    safe = [
        value
        for value in (_text(topic) for topic in topics[:20])
        if _SAFE_TOPIC.fullmatch(value)
    ]
    return " ".join(safe)


def _matches(corpus: str, rules: tuple[tuple[str, re.Pattern[str]], ...]) -> list[str]:
    return [tag for tag, pattern in rules if pattern.search(corpus)]


def infer_historical_taxonomy(
    capture: HistoricalSourceCapture,
) -> dict[str, list[str]]:
    """Infer bounded tags/categories/scenarios without consulting legacy prose."""

    if not isinstance(capture, HistoricalSourceCapture):
        raise TypeError("historical taxonomy requires a source capture")
    source = _text(capture.source).casefold()
    base = _BASE_TAG.get(source)
    if base is None:
        raise ValueError(f"unsupported historical taxonomy source: {source}")
    metadata = _metadata(capture)
    language = _text(metadata.get("language"))
    corpus = " ".join(
        part
        for part in (
            _text(capture.title),
            _text(capture.source_text),
            _topic_text(metadata),
            language,
        )
        if part
    )

    tags: list[str] = [base]
    tags.extend(_matches(corpus, _SEMANTIC_RULES))
    language_tags = _matches(corpus, _LANGUAGES)
    if language:
        exact_language = next(
            (tag for tag, _pattern in _LANGUAGES if tag.casefold() == language.casefold()),
            None,
        )
        if exact_language:
            language_tags = [exact_language, *language_tags]
    tags.extend(language_tags)
    tags.extend(_matches(corpus, _INFRA_RULES))
    tags = normalize_tags(tags, limit=8)

    categories: list[str] = []
    if source == "arxiv":
        categories.append("论文")
        if "大语言模型" in tags:
            categories.append("大模型")
    elif source == "github_trending":
        categories.append("开源生态")
        if any(
            tag in tags
            for tag in {
                "MCP",
                "AI Agent",
                "命令行工具",
                "Kubernetes",
                "Docker",
                *[language_tag for language_tag, _pattern in _LANGUAGES],
            }
        ):
            categories.append("开发工具")
    else:
        if "大语言模型" in tags:
            categories.append("大模型")
        elif any(tag in _AI_TAGS for tag in tags):
            categories.append("AI 工程")
        if "AI 安全" in tags:
            categories.append("安全")
        if "数据库" in tags:
            categories.append("数据")
    categories = list(dict.fromkeys(categories))[:2]

    scenarios: list[str] = []
    if any(tag in _AI_TAGS for tag in tags):
        scenarios.append("AI/ML项目")
    if "大语言模型" in tags:
        scenarios.append("大语言模型")
    if "RAG" in tags:
        scenarios.append("RAG应用")
    if "自然语言处理" in tags:
        scenarios.append("自然语言处理")
    if "计算机视觉" in tags:
        scenarios.append("计算机视觉")
    if "Kubernetes" in tags:
        scenarios.append("Kubernetes")
    if "Docker" in tags or "Kubernetes" in tags:
        scenarios.append("云原生/容器")
    if "命令行工具" in tags:
        scenarios.append("命令行工具")

    return {
        "tags": tags,
        "categories": categories,
        "scenarios": scenarios[:3],
    }


__all__ = ["infer_historical_taxonomy"]
