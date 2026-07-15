from __future__ import annotations

import json
from pathlib import Path

from ai_stack.content_quality import (
    analyze_post,
    body_completeness_reasons,
    build_content_quality_manifest,
    content_quality_reasons,
    markdown_body,
    write_content_quality_manifest,
)

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_quarantines_only_high_confidence_synthetic_bodies(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "safe.md").write_text(
        "---\ntitle: Safe\n---\n\n这是来自原始来源的完整技术记录。\n",
        encoding="utf-8",
    )
    (posts / "unsafe.md").write_text(
        "---\ntitle: Unsafe\n---\n\n"
        "你在提示词中没有提供完整正文，因此以下内容只能根据标题推演。\n",
        encoding="utf-8",
    )

    first = build_content_quality_manifest(content)
    second = build_content_quality_manifest(content)

    assert first == second
    assert first["source_file_count"] == 2
    assert first["quarantined_count"] == 1
    assert first["pages"]["posts/unsafe.md"]["status"] == "quarantined"
    assert set(first["pages"]["posts/unsafe.md"]["reasons"]) == {
        "missing_source_content",
        "prompt_context_leak",
        "title_only_generation",
    }


def test_manifest_writer_is_stable_and_frontmatter_is_not_scanned(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    document = (
        "---\n"
        "title: 您没有提供正文只是标题字段中的文字\n"
        "---\n\n"
        "正文包含可核验的来源事实。\n"
    )
    (posts / "entry.md").write_text(document, encoding="utf-8")
    output = tmp_path / "data" / "content_quality.json"

    manifest = write_content_quality_manifest(content, output)

    assert markdown_body(document) == "正文包含可核验的来源事实。\n"
    assert manifest["quarantined_count"] == 0
    assert json.loads(output.read_text(encoding="utf-8")) == manifest
    assert not output.with_suffix(".json.tmp").exists()


def test_manifest_tracks_transparent_archives_without_counting_them_as_quarantine(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "archived.md").write_text(
        "---\ntitle: Archived\narchived: true\n---\n\n"
        "该条目仅保留原始来源入口。\n",
        encoding="utf-8",
    )

    manifest = build_content_quality_manifest(content)

    assert manifest["source_file_count"] == 1
    assert manifest["quarantined_count"] == 0
    assert manifest["archived_count"] == 1
    assert manifest["pages"]["posts/archived.md"] == {
        "status": "archived",
        "reasons": ["archived_content"],
    }


def test_completeness_gate_detects_unclosed_fences_and_truncated_endings() -> None:
    assert body_completeness_reasons(
        "## 示例\n\n```python\nprint('ok')\n```\n\n完整结论。\n"
    ) == ()
    assert body_completeness_reasons(
        "## 示例\n\n```python\nprint('truncated')\n"
    ) == ("unclosed_code_fence",)
    assert body_completeness_reasons("## 行动建议\n") == ("truncated_ending",)
    assert body_completeness_reasons("## 结论\n\n分析在这里中断，\n") == (
        "truncated_ending",
    )
    assert body_completeness_reasons("## 结论\n\n完整但无需句号的来源说明\n") == ()
    assert content_quality_reasons("```python\nprint('truncated')\n") == (
        "unclosed_code_fence",
    )


def test_provenance_gate_detects_missing_or_truncated_source_assistant_responses() -> None:
    cases = {
        "missing_source_content": "用户没能提供完整原文，因此只能先给出框架。",
        "absent_source_inference": "未获得全文，以下分析只能基于标题进行推断。",
        "truncated_source_inference": (
            "原文似乎被截断，因此本分析只能基于现有片段进行推演。"
        ),
        "source_request_leak": "如果您能补充完整正文，我可以继续完善分析。",
    }

    for reason, body in cases.items():
        assert reason in content_quality_reasons(body)


def test_provenance_gate_ignores_assistant_language_inside_code_examples() -> None:
    body = (
        "## 规则示例\n\n"
        "```text\n如果您能提供完整原文，我可以继续分析。\n```\n\n"
        "该字符串只是测试夹具中的输入样例。\n"
    )

    assert content_quality_reasons(body) == ()


def test_completeness_gate_detects_encoding_loss_translation_leak_and_placeholders() -> None:
    assert "encoding_replacement_character" in content_quality_reasons(
        "## 摘要\n\n模型输出中出现了不可恢复字符 �。\n"
    )
    assert "translation_response_leak" in content_quality_reasons(
        "## 描述\n\n这段内容已经是中文，无需再翻译成中文。是否需要我翻译成英文？\n"
    )
    assert "placeholder_content" in content_quality_reasons(
        "## 技术分析\n\n待补充\n"
    )


def test_analyze_post_uses_body_only_and_requires_a_structural_source_brief() -> None:
    valid = (
        "---\n"
        "title: Brief\n"
        "entry_kind: auto\n"
        "source: hacker_news\n"
        "external_url: https://example.com/brief\n"
        "---\n\n"
        "## 基本信息\n\n- **作者**: Ada\n\n"
        "这是一段完整、非空的来源叙述。\n"
    )
    missing_narrative = valid.replace(
        "这是一段完整、非空的来源叙述。\n", ""
    )

    analysis = analyze_post(valid)
    assert analysis.status == "source_brief"
    assert analysis.fatal_reasons == ()
    assert analyze_post(missing_narrative).status != "source_brief"


def test_declared_modern_source_brief_requires_provenance_frontmatter() -> None:
    body = (
        "## 基本信息\n\n- **来源**: arXiv\n\n"
        "这是一段完整、非空的来源叙述。\n"
    )
    incomplete = (
        "---\n"
        "title: Brief\n"
        "entry_kind: auto\n"
        "source: arxiv\n"
        "content_mode: source_brief\n"
        "external_url: https://arxiv.org/abs/2607.12345\n"
        "---\n\n"
        + body
    )
    complete = incomplete.replace(
        "external_url: https://arxiv.org/abs/2607.12345\n",
        "external_url: https://arxiv.org/abs/2607.12345\n"
        "publication_tier: C\n"
        "source_capture_mode: abstract\n"
        "source_snapshot_sha256: sha256:"
        + "a" * 64
        + "\n"
        "extractor_version: source-contract-v1\n"
        "discovery_method: arxiv_api\n"
        "source_is_truncated: false\n"
        "source_support: 1.0\n",
    )

    assert "invalid_source_brief" in analyze_post(incomplete).fatal_reasons
    assert analyze_post(complete).status == "source_brief"


def test_uncontracted_auto_posts_after_the_reviewed_legacy_cutoff_fail_closed() -> None:
    body = (
        "## 技术分析\n\n"
        "这是一段结构完整的自动生成内容，用于验证已评审历史边界。"
        "内容包含足够的实质性文字、清晰的技术背景和可读的结论。"
        "文档的段落、标点和结束位置都完整，可以作为稳定的回归测试样本。\n"
    )
    old = (
        "---\ntitle: Reviewed legacy\nentry_kind: auto\nsource: arxiv\n"
        "date: 2026-07-15T14:00:41+08:00\n"
        "external_url: https://example.com/legacy\n---\n\n"
        + body
    )
    new = old.replace(
        "title: Reviewed legacy",
        "title: Uncontracted future post",
    ).replace(
        "2026-07-15T14:00:41+08:00",
        "2026-07-15T16:55:26+08:00",
    )

    assert analyze_post(old).status == "legacy_analysis"
    assert "missing_source_contract" in analyze_post(new).fatal_reasons


def test_model_reasoning_trace_is_fatal_outside_code_but_not_in_examples() -> None:
    leaked = (
        "---\ntitle: Leaked\nentry_kind: auto\nsource: arxiv\n---\n\n"
        "## 评论\n\n翻译残片 1. **Analyze the User's Request:**\n\n"
        "这里错误保留了模型内部处理步骤和后续生成正文。"
    )
    repeated_think = (
        "---\ntitle: Think leak\nentry_kind: auto\nsource: blogs_podcasts\n---\n\n"
        "## 评论\n\n1. </think> 2. </think>\n\n这里还有看似完整的正文。"
    )
    fenced_example = (
        "---\ntitle: Safe example\nentry_kind: manual\nsource: manual\n---\n\n"
        "## 示例\n\n```text\nUnderstand the User's Request:\n</think></think>\n```\n\n"
        "正文明确说明这只是代码块里的测试样例，因此不应被误判。"
    )

    assert "model_reasoning_leak" in analyze_post(leaked).fatal_reasons
    assert "model_reasoning_leak" in analyze_post(repeated_think).fatal_reasons
    assert "model_reasoning_leak" not in analyze_post(fenced_example).fatal_reasons


def test_empty_section_warning_distinguishes_container_from_empty_sibling() -> None:
    container = (
        "---\ntitle: Container\nentry_kind: manual\n---\n\n"
        "## 常见问题\n\n### 如何部署\n\n这里有完整答案。\n"
    )
    empty_sibling = (
        "---\ntitle: Empty sibling\nentry_kind: manual\n---\n\n"
        "## 最佳实践\n\n## 最佳实践指南\n\n这里有完整内容。\n"
    )

    assert "empty_section" not in analyze_post(container).warning_reasons
    assert "empty_section" in analyze_post(empty_sibling).warning_reasons


def test_legacy_hn_gate_detects_unterminated_prose_without_flagging_other_sources() -> None:
    body = (
        "## 分析\n\n"
        "这一段旧生成内容在解释模型架构时突然停在高带宽显存和矩阵"
    )
    hn = (
        "---\ntitle: HN\nentry_kind: auto\nsource: hacker_news\n"
        "external_url: https://example.com/hn\n---\n\n" + body
    )
    manual = (
        "---\ntitle: Manual\nentry_kind: manual\nsource: manual\n"
        "external_url: https://example.com/manual\n---\n\n" + body
    )

    assert "unterminated_prose" in analyze_post(hn).fatal_reasons
    assert "unterminated_prose" not in analyze_post(manual).fatal_reasons


def test_manifest_quarantines_structurally_incomplete_active_posts(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "truncated.md").write_text(
        "---\ntitle: Truncated\n---\n\n## 示例\n\n```python\nprint('cut')\n",
        encoding="utf-8",
    )

    manifest = build_content_quality_manifest(content)

    assert manifest["quarantined_count"] == 1
    assert manifest["reason_counts"] == {"unclosed_code_fence": 1}
    assert manifest["pages"]["posts/truncated.md"] == {
        "status": "quarantined",
        "reasons": ["unclosed_code_fence"],
    }


def test_manifest_separates_concise_source_briefs_from_incomplete_posts(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "brief.md").write_text(
        "---\n"
        "title: Brief\n"
        "entry_kind: auto\n"
        "source: hacker_news\n"
        "external_url: https://example.com/brief\n"
        "---\n\n"
        "## 基本信息\n\n这是来源卡片中的可核验摘要。\n",
        encoding="utf-8",
    )
    (posts / "complete.md").write_text(
        "---\n"
        "title: Complete\n"
        "source: manual\n"
        "external_url: https://example.com/complete\n"
        "---\n\n"
        "## 完整记录\n\n这是简短但不应误判为来源快报的手工记录。\n",
        encoding="utf-8",
    )

    manifest = build_content_quality_manifest(content)

    assert manifest["schema_version"] == "content_quality_manifest_v3"
    assert manifest["source_brief_count"] == 1
    assert manifest["complete_count"] == 1
    assert manifest["active_count"] == 2
    assert manifest["pages"]["posts/brief.md"] == {
        "status": "source_brief",
        "reasons": ["concise_source_card"],
    }
    assert "posts/complete.md" not in manifest["pages"]


def test_article_template_quarantines_manifest_entries_from_body_and_search() -> None:
    template = (
        ROOT
        / "blog/themes/terminal-theme/layouts/_default/single.html"
    ).read_text(encoding="utf-8")

    assert ".Site.Data.content_quality" in template
    assert 'data-pagefind-ignore="all"' in template
    assert 'data-content-quality-status="quarantined"' in template
    assert ".Params.archived" in template
    assert "$isQualityBlocked" in template
    assert 'content="noindex, nofollow"' in template
    assert "历史正文已隔离" in template
    assert "{{ .Content }}" in template


def test_article_template_labels_short_source_cards_without_hiding_the_body() -> None:
    template = (
        ROOT
        / "blog/themes/terminal-theme/layouts/_default/single.html"
    ).read_text(encoding="utf-8")

    assert "$isSourceBrief" in template
    assert '"source_brief"' in template
    assert "len .RawContent" in template
    assert ".WordCount" not in template
    assert 'data-content-mode="source-brief"' in template
    assert "来源快报" in template
    assert "以原始来源为准" in template
    assert "{{ .Content }}" in template


def test_article_template_labels_legacy_analysis_without_claiming_source_completeness() -> None:
    template = (
        ROOT / "blog/themes/terminal-theme/layouts/_default/single.html"
    ).read_text(encoding="utf-8")

    assert "$isLegacyAnalysis" in template
    assert 'data-content-mode="legacy-analysis"' in template
    assert "不等同于原文全文" in template


def test_manifest_cli_can_fail_closed_on_active_quarantine(tmp_path: Path) -> None:
    from scripts.build_content_quality_manifest import main

    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "bad.md").write_text(
        "---\ntitle: Bad\nentry_kind: auto\n---\n\n## 未完成\n",
        encoding="utf-8",
    )

    assert main(
        [
            "--content-root",
            str(content),
            "--output",
            str(tmp_path / "quality.json"),
            "--fail-on-quarantine",
        ]
    ) == 1
