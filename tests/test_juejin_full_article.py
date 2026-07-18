from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from ai_stack.content_quality import analyze_post, markdown_frontmatter
from ai_stack.source_contract import (
    SourceContractError,
    apply_source_contract,
    promote_juejin_full_article,
    verify_source_contract,
)
from crawler import juejin_article
from crawler.juejin_article import (
    JuejinArticleAccessError,
    JuejinArticleCapture,
    extract_juejin_article_html,
    fetch_juejin_article,
)
from crawler.juejin_rss import JuejinRSSCrawler
from processor.evidence_rewriter import EvidenceBackedRewriter
from processor.main import ProcessorOrchestrator
from scripts import generate_content as content_script

ARTICLE_ID = "7663304647513718799"
ARTICLE_URL = f"https://juejin.cn/post/{ARTICLE_ID}"
START_SENTINEL = "START-SENTINEL：Harness 会改变模型看到的提示和工具。"
MIDDLE_SENTINEL = "MIDDLE-SENTINEL：ACP 通过标准输入输出承载会话。"
END_SENTINEL = "END-SENTINEL：上线前仍要检查权限与沙盒。"


def _article_html() -> str:
    filler = "这是一段用于验证完整正文提取的工程说明，包含足够的上下文和边界条件。" * 12
    return f"""
    <!doctype html>
    <html lang="zh-CN">
      <body>
        <article data-entry-id="{ARTICLE_ID}">
          <div id="article-root">
            <div class="article-viewer markdown-body">
              <h2>核心机制</h2>
              <p>{START_SENTINEL}</p>
              <p>{filler}</p>
              <h2>协议接入</h2>
              <p>{MIDDLE_SENTINEL}</p>
              <pre><code class="language-bash">interpreter acp</code></pre>
              <p>{filler}</p>
              <h2>安全边界</h2>
              <p>{END_SENTINEL}</p>
              <script>window.secret = "must-not-leak";</script>
            </div>
          </div>
        </article>
      </body>
    </html>
    """


def _rss_item() -> dict[str, object]:
    return {
        "title": "Open Interpreter：面向开源模型的编程 Agent",
        "link": ARTICLE_URL,
        "summary": "Open Interpreter 的 Rust 版本聚焦低成本模型的 Agent 使用体验。",
        "author": "冬奇Lab",
        "published": "Fri, 17 Jul 2026 21:50:00 +0800",
        "tags": [{"term": "人工智能"}, {"term": "Rust"}],
    }


def _contracted_excerpt() -> dict[str, object]:
    crawler = JuejinRSSCrawler(tags=[])
    crawled = crawler._extract_article_info(_rss_item())
    assert crawled is not None
    crawled["crawled_at"] = "2026-07-17T23:42:15+08:00"
    return apply_source_contract(crawled)


def test_juejin_rss_excerpt_is_explicitly_partial() -> None:
    crawler = JuejinRSSCrawler(tags=[])

    item = crawler._extract_article_info(_rss_item())

    assert item is not None
    assert item["discovery_method"] == "rss_excerpt"
    assert item["source_completeness"] == "partial"
    assert item["source_is_truncated"] is True
    assert item["source_truncation_reason"] == "rss_excerpt_only"
    contracted = apply_source_contract(item)
    assert contracted["source_capture_mode"] == "excerpt"
    assert contracted["content_mode"] == "source_brief"
    assert contracted["source_is_truncated"] is True
    assert contracted["source_truncation_reason"] == "rss_excerpt_only"
    verify_source_contract(contracted)


def test_extracts_complete_ssr_article_and_preserves_structure() -> None:
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )

    assert capture.article_id == ARTICLE_ID
    assert capture.heading_count == 3
    assert capture.code_block_count == 1
    assert START_SENTINEL in capture.markdown
    assert MIDDLE_SENTINEL in capture.markdown
    assert END_SENTINEL in capture.markdown
    assert "must-not-leak" not in capture.markdown
    assert capture.markdown.rstrip().endswith(END_SENTINEL)


@pytest.mark.parametrize(
    ("html", "reason"),
    [
        (
            '<html><script src="waf-jschallenge.js"></script><body>Please wait...</body></html>',
            "waf_challenge",
        ),
        ("<html><body>missing article</body></html>", "article_not_found"),
        (
            _article_html().replace(ARTICLE_ID, "999", 1),
            "article_id_mismatch",
        ),
    ],
)
def test_full_article_extractor_fails_closed(html: str, reason: str) -> None:
    with pytest.raises(JuejinArticleAccessError, match=reason):
        extract_juejin_article_html(
            html,
            expected_article_id=ARTICLE_ID,
            source_url=ARTICLE_URL,
        )


def test_full_article_extractor_rejects_an_eof_truncated_container() -> None:
    truncated = _article_html().replace(
        "</div>\n          </div>\n        </article>\n      </body>\n    </html>",
        "",
    )

    with pytest.raises(JuejinArticleAccessError, match="article_structure_incomplete"):
        extract_juejin_article_html(
            truncated,
            expected_article_id=ARTICLE_ID,
            source_url=ARTICLE_URL,
        )


def test_full_article_fetch_rejects_insecure_transport() -> None:
    with pytest.raises(JuejinArticleAccessError, match="invalid_source_url"):
        fetch_juejin_article(ARTICLE_URL.replace("https://", "http://"))


class _FakeResponse:
    def __init__(self, body: bytes, *, status: int = 200, content_type: str = "text/html"):
        self.body = body
        self.status_code = status
        self.headers = {"Content-Type": content_type}
        self.url = ARTICLE_URL
        self.encoding = "utf-8"
        self.closed = False

    def iter_content(self, chunk_size: int):
        for index in range(0, len(self.body), chunk_size):
            yield self.body[index : index + chunk_size]

    def close(self) -> None:
        self.closed = True


class _FakeSession:
    def __init__(self, response: _FakeResponse):
        self.response = response
        self.kwargs: dict[str, object] = {}

    def get(self, _url: str, **kwargs: object) -> _FakeResponse:
        self.kwargs = kwargs
        return self.response


def test_fetch_disables_redirects_and_bounds_the_untrusted_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = _FakeResponse(_article_html().encode())
    session = _FakeSession(response)

    capture = fetch_juejin_article(ARTICLE_URL, session=session)

    assert capture.article_id == ARTICLE_ID
    assert session.kwargs["allow_redirects"] is False
    assert session.kwargs["stream"] is True
    assert response.closed is True

    oversized = _FakeResponse(b"x" * 32)
    monkeypatch.setattr(juejin_article, "_MAX_RESPONSE_BYTES", 16)
    with pytest.raises(JuejinArticleAccessError, match="article_response_too_large"):
        fetch_juejin_article(ARTICLE_URL, session=_FakeSession(oversized))
    assert oversized.closed is True

    monkeypatch.setattr(juejin_article, "_MAX_RESPONSE_BYTES", 2 * 1024 * 1024)
    unknown_charset = _FakeResponse(_article_html().encode())
    unknown_charset.encoding = "x-not-a-codec"
    with pytest.raises(JuejinArticleAccessError, match="invalid_response_encoding"):
        fetch_juejin_article(ARTICLE_URL, session=_FakeSession(unknown_charset))
    assert unknown_charset.closed is True


def test_verified_full_article_promotes_contract_to_tier_b() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )

    promoted = promote_juejin_full_article(excerpt, capture.markdown)

    assert promoted["content_mode"] == "evidence_backed_rewrite"
    assert promoted["publication_tier"] == "B"
    assert promoted["source_capture_mode"] == "full_article"
    assert promoted["source_is_truncated"] is False
    assert promoted["extractor_version"] == "source-contract-v2"
    assert promoted["evidence"]["parent_snapshot_sha256"] == excerpt[
        "source_snapshot_sha256"
    ]
    assert promoted["source_text_original"].endswith(END_SENTINEL)
    verify_source_contract(promoted)


def test_tier_b_digest_signs_the_capture_timestamp() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    tampered = {**promoted, "evidence": dict(promoted["evidence"])}
    tampered["captured_at"] = "2099-01-01T00:00:00Z"
    tampered["evidence"]["captured_at"] = "2099-01-01T00:00:00Z"

    with pytest.raises(SourceContractError, match="digest"):
        verify_source_contract(tampered)


@dataclass
class _FakeClient:
    response: str
    prompt: str = ""

    def create_message(self, prompt: str, **_kwargs: object) -> str:
        self.prompt = prompt
        return self.response


def _valid_rewrite() -> str:
    return """
## 核心结论

Open Interpreter 把模型适配放在 Harness 层，运行时仍负责工具、权限和会话。

## 能力机制

Harness 同时约束提示结构、工具定义、消息转换与响应处理。
不同 provider 仍需匹配传输协议，不能只替换模型名。
这里补充足够的工程解释、验证条件和失败边界，确保内容不是标题扩写。

## 快速开始

先完成安装，再选择 provider 与 harness；首次运行只授予只读权限。
用一个小仓库验证工具调用、上下文恢复和审批流程。
生产接入前应固定版本并记录配置差异。

## 适用边界

它适合需要多模型与 Codex 兼容面的团队。
若必须完全离线，还要确认模型推理端也在本机，
不能把“配置保存在本地”误写成“数据永不出机”。

## 核验清单

- 核对 provider、wire API 与 harness 的组合。
- 验证沙盒、审批和文件写入边界。
- 记录版本、模型、提示与失败回退路径。
""".strip()


def test_evidence_rewriter_receives_the_entire_verified_capture() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    client = _FakeClient(_valid_rewrite())

    rewritten = EvidenceBackedRewriter(client).rewrite(promoted)

    assert rewritten["rewritten_body"] == _valid_rewrite()
    assert START_SENTINEL in client.prompt
    assert MIDDLE_SENTINEL in client.prompt
    assert END_SENTINEL in client.prompt
    verify_source_contract(rewritten)


def test_evidence_rewriter_rejects_large_verbatim_copy() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    copied = _valid_rewrite() + "\n\n" + capture.plain_text[:500]

    with pytest.raises(ValueError, match="verbatim overlap"):
        EvidenceBackedRewriter(_FakeClient(copied)).rewrite(promoted)


def test_evidence_rewriter_rejects_full_source_hidden_in_a_code_fence() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    copied = _valid_rewrite() + "\n\n```text\n" + capture.plain_text + "\n```"

    with pytest.raises(ValueError, match="verbatim overlap"):
        EvidenceBackedRewriter(_FakeClient(copied)).rewrite(promoted)


def test_evidence_rewriter_rejects_zero_width_obfuscated_source_copy() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    obfuscated = "\u200b".join(
        capture.plain_text[index : index + 80]
        for index in range(0, len(capture.plain_text), 80)
    )
    copied = _valid_rewrite() + "\n\n" + obfuscated

    with pytest.raises(ValueError, match="verbatim overlap"):
        EvidenceBackedRewriter(_FakeClient(copied)).rewrite(promoted)


def test_evidence_rewriter_rejects_unbounded_output() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    bloated = _valid_rewrite().replace(
        "## 核验清单",
        ("这是无来源支撑的重复扩写内容，不应被发布。" * 180) + "\n\n## 核验清单",
    )

    with pytest.raises(ValueError, match="too long"):
        EvidenceBackedRewriter(_FakeClient(bloated)).rewrite(promoted)


def test_evidence_rewriter_rejects_untrusted_html_and_links() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    unsafe = _valid_rewrite() + '\n\n<script src="https://evil.example/x.js"></script>'

    with pytest.raises(ValueError, match="raw HTML"):
        EvidenceBackedRewriter(_FakeClient(unsafe)).rewrite(promoted)


@pytest.mark.parametrize(
    "payload",
    [
        "[官方核验][evil]\n[evil]: https://phish.example/track",
        "![pixel][evil]\n[evil]: https://attacker.example/pixel.gif",
        "更多内容请访问 https://phish.example/track",
    ],
)
def test_evidence_rewriter_rejects_reference_and_bare_links(payload: str) -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    unsafe = _valid_rewrite() + "\n\n" + payload

    with pytest.raises(ValueError, match="untrusted link"):
        EvidenceBackedRewriter(_FakeClient(unsafe)).rewrite(promoted)


def test_selected_juejin_hydration_promotes_or_falls_back_without_bypass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    excerpt = _contracted_excerpt()
    generator = content_script.SuperEnhancedContentGenerator.__new__(
        content_script.SuperEnhancedContentGenerator
    )
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    monkeypatch.setattr(
        content_script,
        "fetch_selected_juejin_article",
        lambda *_args, **_kwargs: capture,
    )

    promoted = generator._hydrate_selected_juejin_articles({"juejin": [excerpt]})

    assert promoted["juejin"][0]["content_mode"] == "evidence_backed_rewrite"
    assert promoted["juejin"][0]["publication_tier"] == "B"

    def blocked(*_args: object, **_kwargs: object) -> JuejinArticleCapture:
        raise JuejinArticleAccessError("waf_challenge")

    monkeypatch.setattr(content_script, "fetch_selected_juejin_article", blocked)
    fallback = generator._hydrate_selected_juejin_articles({"juejin": [excerpt]})

    assert fallback["juejin"][0] == excerpt
    assert fallback["juejin"][0]["source_truncation_reason"] == "rss_excerpt_only"


class _PublishableEvidenceFilter:
    @staticmethod
    def filter_evidence_only(review: dict[str, object]) -> dict[str, object]:
        return {**review, "ai_related": True, "ai_confidence": 1.0}

    @staticmethod
    def moderate_evidence_only(review: dict[str, object]) -> dict[str, object]:
        return {**review, "should_publish": True, "moderation_flags": []}


class _RewriteStub:
    @staticmethod
    def rewrite(item: dict[str, object]) -> dict[str, object]:
        return {**item, "rewritten_body": _valid_rewrite()}


class _Explodes:
    def __getattr__(self, name: str) -> object:
        raise AssertionError(f"Tier-B rewrite must not call the legacy generator: {name}")


def test_processor_uses_one_pass_rewriter_instead_of_legacy_generator() -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    promoted = promote_juejin_full_article(excerpt, capture.markdown)
    processor = ProcessorOrchestrator.__new__(ProcessorOrchestrator)
    processor.ai_filter = _PublishableEvidenceFilter()
    processor.evidence_rewriter = _RewriteStub()
    processor.summarizer = _Explodes()
    processor.translator = _Explodes()
    processor.generator = _Explodes()
    processor.tagger = _Explodes()
    processor.scenario_analyzer = _Explodes()

    result = processor.process_single(promoted)

    assert result["rewritten_body"] == _valid_rewrite()
    assert result["publication_tier"] == "B"
    assert result["categories"] == ["AI 工程"]
    assert "工程实践" in result["tags"]
    verify_source_contract(result)


def test_tier_b_renderer_hides_full_capture_and_passes_public_gate(tmp_path: Path) -> None:
    excerpt = _contracted_excerpt()
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    item = promote_juejin_full_article(excerpt, capture.markdown)
    long_rewrite = _valid_rewrite().replace(
        "## 核验清单",
        ("工程验证需要固定版本、权限、模型和任务集，并保留可回溯的工具记录。" * 8)
        + "\n\n## 核验清单",
    )
    item.update(
        {
            "rewritten_body": long_rewrite,
            "tags": ["Open Interpreter", "工程实践"],
            "categories": ["AI工程"],
            "scenarios": [],
        }
    )
    generator = content_script.SuperEnhancedContentGenerator.__new__(
        content_script.SuperEnhancedContentGenerator
    )
    generator.posts_dir = tmp_path
    generator._post_index = []

    document = generator._format_super_enhanced_markdown(
        item,
        generated_at=datetime(2026, 7, 18, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert START_SENTINEL not in document
    assert "非原文转载" in document
    assert analyze_post(document).fatal_reasons == ()
    publication = generator._publication_payload(item)
    assert publication["content_mode"] == "evidence_backed_rewrite"
    assert publication["publication_tier"] == "B"


def test_tier_b_renderer_neutralizes_untrusted_source_metadata(tmp_path: Path) -> None:
    rss = _rss_item()
    rss["author"] = (
        "good\n\n[官方验证](https://phish.example) "
        "![pixel](https://attacker.example/pixel.gif)"
    )
    crawler = JuejinRSSCrawler(tags=[])
    crawled = crawler._extract_article_info(rss)
    assert crawled is not None
    crawled["crawled_at"] = "2026-07-17T23:42:15+08:00"
    excerpt = apply_source_contract(crawled)
    capture = extract_juejin_article_html(
        _article_html(),
        expected_article_id=ARTICLE_ID,
        source_url=ARTICLE_URL,
    )
    item = promote_juejin_full_article(excerpt, capture.markdown)
    item.update(
        {
            "rewritten_body": _valid_rewrite(),
            "tags": ["Open Interpreter", "工程实践"],
            "categories": ["AI工程"],
            "scenarios": [],
        }
    )
    generator = content_script.SuperEnhancedContentGenerator.__new__(
        content_script.SuperEnhancedContentGenerator
    )
    generator.posts_dir = tmp_path
    generator._post_index = []

    document = generator._format_super_enhanced_markdown(
        item,
        generated_at=datetime(2026, 7, 18, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert "good" in document
    assert "phish.example" not in document
    assert "attacker.example" not in document
    assert "![pixel]" not in document
    assert analyze_post(document).fatal_reasons == ()


def test_curated_open_interpreter_post_is_a_complete_labeled_rewrite() -> None:
    root = Path(__file__).resolve().parents[1]
    post = next((root / "blog/content/posts").glob("*72d10eb23e.md"))
    document = post.read_text(encoding="utf-8")
    metadata = markdown_frontmatter(document)
    analysis = analyze_post(document)

    assert metadata["entry_kind"] == "curated"
    assert metadata["content_mode"] == "evidence_backed_rewrite"
    assert metadata["publication_tier"] == "B"
    assert metadata["source_author"] == "冬奇Lab"
    assert "AI 工程" in metadata["categories"]
    assert "AI工程" not in metadata["categories"]
    assert "基于公开资料转写与事实核验，非原文转载" in document
    assert "https://github.com/openinterpreter/openinterpreter" in document
    assert "https://www.openinterpreter.com/docs/terminal/harness" in document
    assert len(document) >= 4_000
    assert analysis.fatal_reasons == ()
