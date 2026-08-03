"""Anti-fabrication invariants for editorial readings of bounded evidence."""

from __future__ import annotations

from typing import Any

import pytest

from ai_stack.content_quality import (
    analyze_post,
    is_interpreted_brief,
    markdown_body,
    markdown_frontmatter,
)
from ai_stack.source_contract import (
    SourceContractError,
    apply_source_contract,
    promote_interpreted_brief,
    verify_source_contract,
)
from processor.source_interpreter import _META_NARRATION_RE, SourceInterpreter
from scripts.generate_content import SuperEnhancedContentGenerator

_ABSTRACT = (
    "We present a method for verifying agent tool outputs under adversarial conditions. "
    "Our approach uses a state machine to validate event streams from large language models. "
    "Experiments on 12 benchmark tasks show the method detects malformed sequences reliably "
    "while adding little overhead. The technique applies to production agent runtimes that "
    "must reject untrusted tool responses before acting on them. We further analyse failure "
    "cases and describe how the validator degrades when the event schema drifts over time. "
    "A companion study measures validation cost across three deployment settings."
)

_READING = """### 这是什么

一种在对抗条件下校验智能体工具输出的方法，用状态机验证模型产生的事件流。

### 用在哪里

适合需要在执行前拒绝不可信工具响应的生产环境运行时。

### 可以推断的

- 推测：工具生态越复杂的系统，这类校验的价值越高。"""


class _Fake:
    def __init__(self, text: str) -> None:
        self.text = text
        self.calls = 0

    def create_message(self, prompt: str, **kwargs: object) -> str:
        self.calls += 1
        return self.text


class _Explodes:
    def create_message(self, prompt: str, **kwargs: object) -> str:
        raise AssertionError("no model call is allowed for this capture")


def _arxiv(summary: str = _ABSTRACT) -> dict[str, Any]:
    return apply_source_contract(
        {
            "source": "arxiv",
            "title": "Verifying Agent Tool Outputs",
            "url": "https://arxiv.org/abs/2601.00010",
            "summary": summary,
            "crawled_at": "2026-07-01T08:00:00Z",
            "captured_at": "2026-07-01T08:00:00Z",
            "published": "2026-07-01T08:00:00Z",
        }
    )


def _hacker_news() -> dict[str, Any]:
    return apply_source_contract(
        {
            "source": "hacker_news",
            "title": "A new AI runtime",
            "url": "https://example.com/story",
            "author": "ada",
            "score": 42,
            "descendants": 7,
            "hn_id": 123,
            "crawled_at": "2026-07-15T12:00:00+00:00",
        }
    )


def test_metadata_only_capture_is_never_sent_to_the_model() -> None:
    item = _hacker_news()

    assert SourceInterpreter.depth_for(item) == "skip"
    # A bare title cannot ground a reading, so the client must not be touched.
    result = SourceInterpreter(_Explodes()).interpret(item)

    assert result["content_mode"] == "source_brief"
    assert "interpretation_text" not in result


def test_thin_evidence_is_skipped_before_spending_a_call() -> None:
    item = _arxiv("Short abstract about agents. " * 3)

    assert SourceInterpreter.depth_for(item) == "skip"
    assert SourceInterpreter(_Explodes()).interpret(item)["content_mode"] == "source_brief"


def test_grounded_reading_is_promoted_without_touching_the_evidence() -> None:
    item = _arxiv()
    client = _Fake(_READING)

    result = SourceInterpreter(client).interpret(item)

    assert client.calls == 1
    assert result["content_mode"] == "interpreted_brief"
    assert result["publication_tier"] == "C+"
    # The snapshot digest is what lineage fingerprints bind to: a reading must
    # never change it, or the same capture would look like a different source.
    assert result["evidence"]["digest"] == item["evidence"]["digest"]
    assert result["evidence"] == item["evidence"]
    verify_source_contract(result)


@pytest.mark.parametrize(
    ("reason", "reading"),
    [
        ("fabricated number", _READING.replace("复杂的系统", "准确率 97% 的系统")),
        ("fabricated name", _READING.replace("用状态机", "用 LangGraph 状态机")),
        ("meta narration", _READING.replace("一种在", "由于未提供原文，推断这是一种在")),
        ("unmarked inference", _READING.replace("- 推测：工具生态", "- 工具生态")),
        ("injected link", _READING.replace("的事件流。", "的事件流，见 https://evil.example/x。")),
        ("raw markup", _READING.replace("状态机", "<script>alert(1)</script>状态机")),
        ("template syntax", _READING.replace("状态机", "{{ .Site.Title }}状态机")),
        ("promoted heading", _READING.replace("### 这是什么", "## 这是什么")),
    ],
)
def test_ungrounded_reading_falls_back_to_the_source_brief(reason: str, reading: str) -> None:
    item = _arxiv()

    result = SourceInterpreter(_Fake(reading)).interpret(item)

    assert result["content_mode"] == "source_brief", reason
    assert "interpretation_text" not in result, reason


@pytest.mark.parametrize(
    "sentence",
    [
        # Domain vocabulary that a word-level blocklist wrongly rejected on the
        # first production run, taking the pass rate to zero.
        "适合需要长上下文的生产环境运行时。",
        "该方法在上下文窗口受限时仍然可用。",
        "论文摘要指出该方法提升了稳定性。",
        "标题所述的校验机制用于事件流。",
    ],
)
def test_domain_vocabulary_is_not_treated_as_meta_narration(sentence: str) -> None:
    assert _META_NARRATION_RE.search(sentence) is None


@pytest.mark.parametrize(
    "sentence",
    [
        "由于未提供原文，只能基于标题推断。",
        "根据摘要来看，该方法应该有效。",
        "原文中没有给出实验细节。",
        "本文将从三个方面分析。",
        "我将为你分析这项工作。",
        "受限于有限的信息，暂无法判断。",
        "无法获取完整内容。",
    ],
)
def test_claims_about_what_the_writer_could_see_are_rejected(sentence: str) -> None:
    assert _META_NARRATION_RE.search(sentence) is not None


def test_rejection_names_the_offending_phrase() -> None:
    reading = _READING.replace("一种在", "由于未提供原文，推断这是一种在")

    with pytest.raises(ValueError) as excinfo:
        SourceInterpreter._validate(_arxiv(), body=reading, depth="full", budget=600)

    # A rejection that cannot be tuned from CI logs is why the first run was opaque.
    assert "未提供" in str(excinfo.value)


def test_verbatim_republication_is_rejected() -> None:
    item = _arxiv()
    copied = (
        "### 这是什么\n\n"
        + _ABSTRACT[:160]
        + "\n\n### 用在哪里\n\n适合生产环境运行时。\n\n"
        "### 可以推断的\n\n- 推测：这类校验值得关注。"
    )

    assert SourceInterpreter(_Fake(copied)).interpret(item)["content_mode"] == "source_brief"


def test_speculation_requires_a_sufficient_evidence_budget() -> None:
    # Enough prose to interpret, not enough to speculate from.
    item = _arxiv(_ABSTRACT[:330])

    assert SourceInterpreter.depth_for(item) == "framing"
    assert SourceInterpreter(_Fake(_READING)).interpret(item)["content_mode"] == "source_brief"


def test_model_failure_keeps_the_brief_publishable() -> None:
    class _Fails:
        def create_message(self, prompt: str, **kwargs: object) -> str:
            raise RuntimeError("upstream unavailable")

    result = SourceInterpreter(_Fails()).interpret(_arxiv())

    assert result["content_mode"] == "source_brief"


def test_tampered_interpretation_fails_the_contract() -> None:
    promoted = promote_interpreted_brief(_arxiv(), _READING)
    promoted["interpretation_text"] = "被替换的解读"

    with pytest.raises(SourceContractError):
        verify_source_contract(promoted)


def test_rendered_interpreted_brief_passes_the_quality_gate() -> None:
    item = SourceInterpreter(_Fake(_READING)).interpret(_arxiv())
    item.setdefault("tags", ["大语言模型"])
    item.setdefault("categories", [])
    generator = SuperEnhancedContentGenerator.__new__(SuperEnhancedContentGenerator)

    markdown = SuperEnhancedContentGenerator._format_super_enhanced_markdown(
        generator, item, current_filename="post.md"
    )
    metadata = markdown_frontmatter(markdown)
    body = markdown_body(markdown)
    analysis = analyze_post(markdown)

    assert is_interpreted_brief(metadata, body)
    assert analysis.status == "interpreted_brief"
    assert analysis.fatal_reasons == ()
    # The captured evidence and the reading are both present and separated.
    assert "## 要点解读" in body
    assert "## 来源摘要/节选" in body
    # The Tier-C promise must not be repeated on a page that carries inference.
    assert "不包含基于缺失正文的扩展推断" not in body
    # The description leads with what the work is, not with a disclaimer.
    assert str(metadata.get("description", "")).startswith("一种在对抗条件下")
