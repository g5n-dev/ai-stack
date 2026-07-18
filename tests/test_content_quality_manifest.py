from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_stack.content_quality import (
    analyze_post,
    body_completeness_reasons,
    build_content_quality_manifest,
    content_quality_reasons,
    markdown_body,
    remove_empty_section_headings,
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
        "---\ntitle: Safe\ndescription: Safe description.\n---\n\n"
        "这是来自原始来源的完整技术记录。\n",
        encoding="utf-8",
    )
    (posts / "unsafe.md").write_text(
        "---\ntitle: Unsafe\ndescription: Unsafe description.\n---\n\n"
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


def test_prompt_gate_does_not_bridge_a_marketing_phrase_to_a_renderer_note() -> None:
    body = (
        "如果本知识库能为您提供帮助，别忘了给予支持哦（关注、点赞、分享）。\n\n"
        "## 来源说明\n\n当前只保存了来源元数据，未抓取完整正文。"
    )

    assert "prompt_context_leak" not in content_quality_reasons(body)


@pytest.mark.parametrize(
    ("body", "reason"),
    (
        ("凭据 " + "sk-" + "test_" + "x" * 24, "credential_token"),
        ('password = "' + "b" * 32 + '"', "credential_assignment"),
        ("联系 privacy@example.com", "email_address"),
        ("调试文件 /home/example/private.log", "user_home_path"),
        ("内网地址 10.20.30.40", "private_network_address"),
        ("内网 IPv6 fd00::1234", "private_network_address"),
    ),
)
def test_content_quality_rejects_sensitive_public_text(body: str, reason: str) -> None:
    assert reason in content_quality_reasons(body)


def test_content_quality_allows_environment_credential_references() -> None:
    body = 'api_key = os.getenv("OPENAI_API_KEY"); docs use 192.0.2.10'

    assert "credential_assignment" not in content_quality_reasons(body)
    assert "private_network_address" not in content_quality_reasons(body)


def test_manifest_writer_is_stable_and_frontmatter_is_not_scanned(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    document = (
        "---\n"
        "title: 您没有提供正文只是标题字段中的文字\n"
        "description: Frontmatter is not body content.\n"
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
        "---\ntitle: Archived\narchived: true\n---\n\n该条目仅保留原始来源入口。\n",
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


def test_active_post_rejects_atx_and_setext_h1_outside_fenced_code() -> None:
    base = (
        "---\n"
        "title: Render-safe article\n"
        "description: A complete render-safe description.\n"
        "entry_kind: manual\n"
        "---\n\n"
    )
    atx = base + "## 开始\n\n正常内容。\n\n# 重复页面标题\n\n后续内容。\n"
    setext = base + "## 开始\n\n正常内容。\n\n重复页面标题\n===\n\n后续内容。\n"
    fenced = base + "## 示例\n\n```markdown\n# 代码示例标题\n\n示例标题\n===\n```\n\n正文。\n"

    assert "body_h1_heading" in analyze_post(atx).fatal_reasons
    assert "body_h1_heading" in analyze_post(setext).fatal_reasons
    assert "body_h1_heading" not in analyze_post(fenced).fatal_reasons


def test_active_post_rejects_title_generation_prompt_leaks_with_tight_boundaries() -> None:
    base = (
        "---\n"
        "title: Normal title\n"
        "description: A complete description.\n"
        "entry_kind: manual\n"
        "---\n\n"
    )
    leaked_title = (
        base.replace(
            "title: Normal title",
            "title: 基于描述内容，我将创建一个精准、具体的中文标题",
        )
        + "## 正文\n\n这里是完整正文。\n"
    )
    leaked_body = base + "## 标题建议\n\n推荐标题：\n\n**一篇正常标题**\n\n这里是正文。\n"
    imperative = base + "## 输入残片\n\n请根据以下标题生成一个精准的中文标题。\n\n这里是正文。\n"
    legitimate = (
        base + "## 编辑系统\n\n在文章发布前，让 AI 基于内容分析推荐 3-5 个标题选项。\n\n"
        "请根据以下文本内容生成一份简明扼要的中文摘要。\n"
    )
    fenced = (
        base + "## 反例\n\n```text\n推荐标题：\n请根据以下标题生成标题\n```\n\n"
        "这些字符串只是代码示例。\n"
    )

    assert "title_generation_prompt_leak" in analyze_post(leaked_title).fatal_reasons
    assert "title_generation_prompt_leak" in analyze_post(leaked_body).fatal_reasons
    assert "title_generation_prompt_leak" in analyze_post(imperative).fatal_reasons
    assert "title_generation_prompt_leak" not in analyze_post(legitimate).fatal_reasons
    assert "title_generation_prompt_leak" not in analyze_post(fenced).fatal_reasons


def test_active_post_requires_a_non_empty_string_description() -> None:
    body = "## 正文\n\n这里是完整正文。\n"
    missing = "---\ntitle: Missing\nentry_kind: manual\n---\n\n" + body
    blank = "---\ntitle: Blank\ndescription: '   '\nentry_kind: manual\n---\n\n" + body
    present = "---\ntitle: Present\ndescription: 有效描述。\nentry_kind: manual\n---\n\n" + body

    assert "missing_description" in analyze_post(missing).fatal_reasons
    assert "missing_description" in analyze_post(blank).fatal_reasons
    assert "missing_description" not in analyze_post(present).fatal_reasons


def test_post_gate_rejects_mechanically_truncated_descriptions() -> None:
    body = "## 正文\n\n这里是完整且可核验的正文。\n"

    def document(description: str) -> str:
        return (
            "---\n"
            "title: Description boundary\n"
            f"description: {json.dumps(description, ensure_ascii=False)}\n"
            "entry_kind: manual\n"
            "---\n\n" + body
        )

    mechanically_160 = "甲" * 160
    mechanically_159 = "乙" * 150 + " observab"
    mechanically_cut_list_item = "甲" * 157 + " 1."
    complete_160 = "甲" * 159 + "。"
    complete_english = "a" * 159 + "."
    complete_with_quote = "甲" * 157 + "结论。”"
    translation_prefix = "您提供的文本已经是中文"
    translation_and_truncated = translation_prefix + "甲" * (160 - len(translation_prefix))
    dangling = (
        "该摘要概括了现有正文中的部署证据，但机械截断后停在 CI/",
        "该摘要概括了现有正文中的部署证据，但最后停在逗号，",
        "该摘要概括了现有正文中的部署证据，但最后停在冒号：",
    )

    assert len(mechanically_160) == 160
    assert len(mechanically_159) == 159
    assert len(complete_160) == 160
    assert "truncated_description" in analyze_post(document(mechanically_160)).fatal_reasons
    assert "truncated_description" in analyze_post(document(mechanically_159)).fatal_reasons
    assert (
        "truncated_description" in analyze_post(document(mechanically_cut_list_item)).fatal_reasons
    )
    assert "truncated_description" not in analyze_post(document(complete_160)).fatal_reasons
    assert "truncated_description" not in analyze_post(document(complete_english)).fatal_reasons
    assert "truncated_description" not in analyze_post(document(complete_with_quote)).fatal_reasons
    combined_reasons = analyze_post(document(translation_and_truncated)).fatal_reasons
    assert "translation_response_leak" in combined_reasons
    assert "truncated_description" in combined_reasons
    assert all(
        "truncated_description" in analyze_post(document(value)).fatal_reasons for value in dangling
    )
    assert (
        "truncated_description"
        not in analyze_post(document("简短描述虽然没有句号，但并非机械长度边界。")).fatal_reasons
    )


def test_active_post_rejects_consecutive_horizontal_rules_outside_fences() -> None:
    base = (
        "---\n"
        "title: Horizontal rules\n"
        "description: A complete description.\n"
        "entry_kind: manual\n"
        "---\n\n"
    )
    consecutive = base + "## 正文\n\n内容。\n\n---\n\n* * *\n\n继续。\n"
    separated = base + "## 正文\n\n内容。\n\n---\n\n补充内容。\n\n***\n\n继续。\n"
    fenced = base + "## 示例\n\n```markdown\n---\n\n***\n```\n\n这些分隔符只是代码示例。\n"

    assert "consecutive_horizontal_rules" in analyze_post(consecutive).fatal_reasons
    assert "consecutive_horizontal_rules" not in analyze_post(separated).fatal_reasons
    assert "consecutive_horizontal_rules" not in analyze_post(fenced).fatal_reasons


def test_archived_posts_are_exempt_from_render_structure_gates() -> None:
    archived = (
        "---\n"
        "title: 推荐标题：请根据描述生成标题\n"
        "archived: true\n"
        "---\n\n"
        "# 重复标题\n\n---\n\n***\n"
    )

    analysis = analyze_post(archived)

    assert analysis.status == "archived"
    assert analysis.fatal_reasons == ()


def test_completeness_gate_detects_unclosed_fences_and_truncated_endings() -> None:
    assert body_completeness_reasons("## 示例\n\n```python\nprint('ok')\n```\n\n完整结论。\n") == ()
    assert body_completeness_reasons("## 示例\n\n```python\nprint('truncated')\n") == (
        "unclosed_code_fence",
    )
    assert body_completeness_reasons("## 行动建议\n") == ("truncated_ending",)
    assert body_completeness_reasons("## 结论\n\n分析在这里中断，\n") == ("truncated_ending",)
    assert body_completeness_reasons("## 结论\n\n完整但无需句号的来源说明\n") == ()
    assert content_quality_reasons("```python\nprint('truncated')\n") == ("unclosed_code_fence",)


def test_provenance_gate_detects_missing_or_truncated_source_assistant_responses() -> None:
    cases = {
        "missing_source_content": "用户没能提供完整原文，因此只能先给出框架。",
        "absent_source_inference": "未获得全文，以下分析只能基于标题进行推断。",
        "truncated_source_inference": ("原文似乎被截断，因此本分析只能基于现有片段进行推演。"),
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
    assert "placeholder_content" in content_quality_reasons("## 技术分析\n\n待补充\n")


def test_post_gate_scans_frontmatter_description_for_translation_response_leak() -> None:
    leaked = (
        "---\n"
        "title: Translation residue\n"
        "description: 您好，注意到您提供的内容已经是中文，无需再次翻译。\n"
        "entry_kind: manual\n"
        "---\n\n"
        "## 正文\n\n这里是完整且可独立阅读的正文。\n"
    )
    legitimate = leaked.replace(
        "您好，注意到您提供的内容已经是中文，无需再次翻译。",
        "本文分析翻译模型为何偶尔声称输入内容已经是中文。",
    )

    assert "translation_response_leak" in analyze_post(leaked).fatal_reasons
    assert "translation_response_leak" not in analyze_post(legitimate).fatal_reasons


def test_translation_response_gate_catches_high_confidence_wording_variants() -> None:
    variants = (
        "这段文字本身已经是中文了。如果您需要，我可以帮您润色。",
        "您好，您提供的文本**已经是中文**了。",
        "这句话已经是中文了，不过我可以帮助您优化表达。",
        "如果您是想把这段中文翻译成英文，以下是翻译版本。",
        "该中文文本已符合要求，无需翻译。如需翻译成英文，请提供相应内容。",
    )

    for text in variants:
        assert "translation_response_leak" in content_quality_reasons(f"## 描述\n\n{text}\n")


def test_translation_response_gate_does_not_flag_translation_discussion() -> None:
    body = (
        "## 描述\n\n"
        "本文研究模型在收到“把这句话翻译成英文”的提示后如何保持术语一致，"
        "并讨论系统偶尔声称输入内容已经是中文这一错误现象。\n"
    )

    assert "translation_response_leak" not in content_quality_reasons(body)


def test_translation_response_gate_scans_every_description_section() -> None:
    late_leak = (
        "## 正文\n\n" + ("这是用于验证深层区块扫描的正常正文。" * 120) + "\n\n## 描述\n\n"
        "您好，这段内容本身就是中文的，不需要翻译成中文。"
        "如果您需要英译或润色，请告诉我。\n\n"
        "## 评论\n\n这里是正常评论。\n"
    )
    code_example = (
        "## 正文\n\n"
        + ("这是用于验证代码围栏边界的正常正文。" * 120)
        + "\n\n```markdown\n## 描述\n\n"
        "这段内容本身就是中文，无需翻译，请告诉我。\n```\n"
    )
    other_section = (
        "## 正文\n\n" + ("这是用于验证标题边界的正常正文。" * 120) + "\n\n## 评论\n\n"
        "这段内容本身就是中文，无需翻译，请告诉我。\n"
    )

    assert "translation_response_leak" in content_quality_reasons(late_leak)
    assert "translation_response_leak" not in content_quality_reasons(code_example)
    assert "translation_response_leak" not in content_quality_reasons(other_section)


def test_post_gate_rejects_editorial_meta_preamble_in_description_or_intro() -> None:
    base = (
        "---\ntitle: Editorial residue\ndescription: 正常的文章描述。\nentry_kind: manual\n---\n\n"
    )
    leaked_description = (
        base.replace(
            "description: 正常的文章描述。",
            "description: 这是一个为您量身定制的引言，旨在抓住读者注意力。",
        )
        + "## 正文\n\n文章从这里开始。\n"
    )
    leaked_intro = (
        base + "## ✨ 引人入胜的引言\n\n这里为你撰写了一个极具吸引力的导语：\n\n文章从这里开始。\n"
    )

    assert "editorial_meta_preamble" in analyze_post(leaked_description).fatal_reasons
    assert "editorial_meta_preamble" in analyze_post(leaked_intro).fatal_reasons


def test_editorial_meta_preamble_gate_has_tight_position_and_voice_boundaries() -> None:
    base = (
        "---\n"
        "title: Editorial boundaries\n"
        "description: 这里是我为团队撰写导语时总结的编辑规范。\n"
        "entry_kind: manual\n"
        "---\n\n"
    )
    first_person = base + "## 导语\n\n这里是我为团队撰写的项目背景。\n"
    product_discussion = (
        base + "## 导语\n\n这是一个为用户打造导语编辑器的技术方案。\n\n"
        "## 评论\n\n原始模型曾回答：这是一个为您定制的引言。\n"
    )
    fenced = base + "## 导语\n\n```text\n这是一个为您定制的引言\n```\n\n正文自然开始。\n"

    for document in (first_person, product_discussion, fenced):
        assert "editorial_meta_preamble" not in analyze_post(document).fatal_reasons


def test_auto_legacy_gate_detects_truncation_before_citation_footer() -> None:
    base = (
        "---\n"
        "title: Pre-citation truncation\n"
        "description: HN legacy analysis fixture.\n"
        "entry_kind: auto\n"
        "source: hacker_news\n"
        "content_mode: legacy_analysis\n"
        "external_url: https://example.com/hn\n"
        "---\n\n"
        "## 分析\n\n"
    )
    cases = (
        base + "这段结论具有极高的**信号价值\n\n## 🔗 引用\n\n- [原文](https://example.com)\n",
        base + "这段结论停在关键的*信号价值\n\n## 引用\n\n- [原文](https://example.com)\n",
        base + "这个方案的关键限制仍然在于，\n\n## 引用\n\n- [原文](https://example.com)\n",
        base + "部署前必须重新检查输入边界（\n\n## 来源\n\n- [原文](https://example.com)\n",
        base + "这一段旧生成内容在解释模型架构时突然停在高带宽显存和矩阵，\n\n"
        "## 🔗 引用\n\n- [原文](https://example.com)\n",
    )

    for document in cases:
        assert "truncated_pre_citation_tail" in analyze_post(document).fatal_reasons

    for source in ("arxiv", "juejin", "blogs_podcasts", "github_trending"):
        document = (
            base.replace("source: hacker_news", f"source: {source}")
            + "这一段正文突然停在尚未完成的模型部署流程和高带宽矩阵计算，\n\n"
            "## 引用\n\n- [原文](https://example.com)\n"
        )
        assert "truncated_pre_citation_tail" in analyze_post(document).fatal_reasons


def test_pre_citation_tail_gate_excludes_complete_or_structural_endings() -> None:
    base = (
        "---\n"
        "title: Pre-citation boundary\n"
        "description: HN legacy analysis fixture.\n"
        "entry_kind: auto\n"
        "source: hacker_news\n"
        "content_mode: legacy_analysis\n"
        "external_url: https://example.com/hn\n"
        "---\n\n"
        "## 分析\n\n"
    )
    complete = base + "这是自然结束的完整结论。⚡️\n\n## 引用\n\n- [原文](https://example.com)\n"
    list_tail = (
        base + "- 第一项无需句号\n- 第二项无需句号\n\n## 引用\n\n- [原文](https://example.com)\n"
    )
    link_tail = (
        base
        + "[查看完整来源](https://example.com/source)\n\n## 引用\n\n- [原文](https://example.com)\n"
    )
    code_tail = (
        base + "```python\nvalue = '代码块无需句号'\n```\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    inline_math = base + "示例矩阵尺寸为 2*3\n\n## 引用\n\n- [原文](https://example.com)\n"
    complete_without_period = (
        base + "能够自动将流量切换到备用区域是保证业务连续性的关键\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    misplaced_strong_before_emoji = (
        base + "- 核心差异化：现有证据支持这一完整结论。** 🤖✨\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    misplaced_label_strong = (
        base + "- 高可用与容灾是支撑 8 亿用户的地基** 🛡️：虽然原文没有详细展开，"
        "但现有证据足以说明服务连续性。\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    misplaced_label_strong_without_emoji = (
        base + "- 📝 隐式状态管理**：循环会利用历史结果作为上下文记忆，从而保持连贯性。\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    mixed_punctuation_list = (
        base + "- 第一项已经形成完整结论。\n"
        "- 尊重用户隐私，仅将已同意接收定向内容的用户加入列表\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    other_source = (
        base.replace("source: hacker_news", "source: blogs_podcasts")
        + "这一段正文突然停在尚未完成的模型部署流程和高带宽矩阵计算，\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    manual = (
        base.replace("entry_kind: auto", "entry_kind: manual")
        + "正文突然停在未完成的模型部署和矩阵\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    other_mode = (
        base.replace("content_mode: legacy_analysis", "content_mode: source_brief")
        + "正文突然停在未完成的模型部署和矩阵\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )

    assert "truncated_pre_citation_tail" in analyze_post(other_source).fatal_reasons
    for document in (
        complete,
        complete_without_period,
        misplaced_strong_before_emoji,
        misplaced_label_strong,
        misplaced_label_strong_without_emoji,
        mixed_punctuation_list,
        list_tail,
        link_tail,
        code_tail,
        inline_math,
        manual,
        other_mode,
    ):
        assert "truncated_pre_citation_tail" not in analyze_post(document).fatal_reasons


def test_pre_citation_gate_uses_peer_punctuation_for_final_list_item() -> None:
    base = (
        "---\ntitle: List truncation\ndescription: Fixture.\n"
        "entry_kind: auto\nsource: hacker_news\ncontent_mode: legacy_analysis\n"
        "external_url: https://example.com/hn\n---\n\n"
        "## 问答\n\n**A**: 建议包括：\n\n"
    )
    ambiguous_without_punctuation = (
        base + "1. **第一项**：这是完整的第一项。\n"
        "2. **第二项**：这一项在生成途中突然停止\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    structurally_truncated = (
        base + "1. **第一项**：这是完整的第一项。\n"
        "2. **第二项**：这一项在生成途中突然停止，\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    consistent = (
        base + "- 安装依赖\n- 运行测试\n- 发布构建\n\n## 引用\n\n- [原文](https://example.com)\n"
    )

    assert (
        "truncated_pre_citation_tail"
        not in analyze_post(ambiguous_without_punctuation).fatal_reasons
    )
    assert "truncated_pre_citation_tail" in analyze_post(structurally_truncated).fatal_reasons
    assert "truncated_pre_citation_tail" not in analyze_post(consistent).fatal_reasons


def test_pre_citation_gate_detects_explicit_qa_tail_structures() -> None:
    base = (
        "---\ntitle: Q&A truncation\ndescription: Fixture.\n"
        "entry_kind: auto\nsource: hacker_news\ncontent_mode: legacy_analysis\n"
        "external_url: https://example.com/hn\n---\n\n"
    )
    unterminated = (
        base + "### 6: 这个方案是否可行？\n\n6: 这个方案是否可行？\n\n"
        "**A**: 这一答案在解释关键限制时突然停止，\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    answer_fragment = (
        base + "### 7: 最终答案是什么？\n\n7: 最终答案是什么？\n\n"
        "**A**: 这\n\n## 引用\n\n- [原文](https://example.com)\n"
    )
    repeated_question = (
        base + "### 7: 如何维护\n\n7: 如何维护\n\n## 引用\n\n- [原文](https://example.com)\n"
    )

    for document in (unterminated, answer_fragment, repeated_question):
        assert "truncated_pre_citation_tail" in analyze_post(document).fatal_reasons


def test_pre_citation_gate_detects_unbalanced_markup_and_bare_markers() -> None:
    base = (
        "---\ntitle: Markup truncation\ndescription: Fixture.\n"
        "entry_kind: auto\nsource: hacker_news\ncontent_mode: legacy_analysis\n"
        "external_url: https://example.com/hn\n---\n\n"
    )
    cases = (
        "* **配置**：请检查部署参数（生产环境",
        "* **路径**：配置文件位于 `/.config",
        "*",
        "###",
    )

    for tail in cases:
        document = base + tail + "\n\n## 引用\n\n- [原文](https://example.com)\n"
        assert "truncated_pre_citation_tail" in analyze_post(document).fatal_reasons


def test_pre_citation_gate_does_not_apply_qa_rule_to_generic_short_prose() -> None:
    base = (
        "---\ntitle: Generic prose\ndescription: Fixture.\n"
        "entry_kind: auto\nsource: hacker_news\ncontent_mode: legacy_analysis\n"
        "external_url: https://example.com/hn\n---\n\n"
    )
    generic = (
        base + "## 摘要\n\n这是一个没有句号的简短栏目名称\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )
    command_list = (
        base + "## 命令\n\n- npm install\n- npm test\n- npm run build\n\n"
        "## 引用\n\n- [原文](https://example.com)\n"
    )

    for document in (generic, command_list):
        assert "truncated_pre_citation_tail" not in analyze_post(document).fatal_reasons


def test_completeness_signals_handle_fence_and_replacement_boundaries() -> None:
    mismatched = "## 示例\n\n```python\nprint('cut')\n~~~\n"
    longer_closer = "## 示例\n\n```python\nprint('complete')\n````\n\n结论。\n"
    replacement_in_code = "## 样例\n\n```text\ncorrupt � byte\n```\n\n结论。\n"

    assert "unclosed_code_fence" in body_completeness_reasons(mismatched)
    assert "unclosed_code_fence" not in body_completeness_reasons(longer_closer)
    assert "encoding_replacement_character" in body_completeness_reasons(replacement_in_code)


def test_archived_post_bypasses_completeness_and_translation_gates() -> None:
    archived = (
        "---\n"
        "title: Archived damaged source\n"
        "description: 您提供的内容已经是中文，无需翻译。\n"
        "archived: true\n"
        "source: hacker_news\n"
        "entry_kind: auto\n"
        "content_mode: legacy_analysis\n"
        "---\n\n"
        "## 描述\n\n这段内容已经是中文。\n\n```text\n损坏字符 �\n"
    )

    analysis = analyze_post(archived)

    assert analysis.status == "archived"
    assert analysis.fatal_reasons == ()


def test_analyze_post_uses_body_only_and_requires_a_structural_source_brief() -> None:
    valid = (
        "---\n"
        "title: Brief\n"
        "description: A concise source card.\n"
        "entry_kind: auto\n"
        "source: hacker_news\n"
        "content_mode: legacy_source_brief\n"
        "source_provenance: legacy_no_snapshot\n"
        "source_support: 0.0\n"
        "external_url: https://example.com/brief\n"
        "---\n\n"
        "## 基本信息\n\n- **作者**: Ada\n\n"
        "这是一段完整、非空的来源叙述。\n"
    )
    missing_narrative = valid.replace("这是一段完整、非空的来源叙述。\n", "")

    analysis = analyze_post(valid)
    assert analysis.status == "source_brief"
    assert analysis.fatal_reasons == ()
    assert analyze_post(missing_narrative).status != "source_brief"


def test_declared_modern_source_brief_requires_provenance_frontmatter() -> None:
    body = "## 基本信息\n\n- **来源**: arXiv\n\n这是一段完整、非空的来源叙述。\n"
    incomplete = (
        "---\n"
        "title: Brief\n"
        "description: A concise source card.\n"
        "entry_kind: auto\n"
        "source: arxiv\n"
        "content_mode: source_brief\n"
        "external_url: https://arxiv.org/abs/2607.12345\n"
        "---\n\n" + body
    )
    missing_completeness = incomplete.replace(
        "external_url: https://arxiv.org/abs/2607.12345\n",
        "external_url: https://arxiv.org/abs/2607.12345\n"
        "publication_tier: C\n"
        "source_capture_mode: abstract\n"
        "source_snapshot_sha256: sha256:" + "a" * 64 + "\n"
        "extractor_version: source-contract-v1\n"
        "discovery_method: arxiv_api\n"
        "source_is_truncated: false\n"
        "source_support: 1.0\n",
    )
    complete = missing_completeness.replace(
        "source_capture_mode: abstract\n",
        "source_capture_mode: abstract\nsource_completeness: abstract_only\n",
    )
    wrong_completeness = missing_completeness.replace(
        "source_capture_mode: abstract\n",
        "source_capture_mode: abstract\nsource_completeness: complete\n",
    )

    assert "invalid_source_brief" in analyze_post(incomplete).fatal_reasons
    assert "invalid_source_brief" in analyze_post(missing_completeness).fatal_reasons
    assert "invalid_source_brief" in analyze_post(wrong_completeness).fatal_reasons
    assert analyze_post(complete).status == "source_brief"


def test_truncated_source_brief_requires_an_explicit_reason() -> None:
    base = (
        "---\n"
        "title: Brief\n"
        "description: A concise source card.\n"
        "entry_kind: auto\n"
        "source: blogs_podcasts\n"
        "content_mode: source_brief\n"
        "external_url: https://example.com/source\n"
        "publication_tier: C\n"
        "source_capture_mode: excerpt\n"
        "source_completeness: partial\n"
        "source_snapshot_sha256: sha256:" + "a" * 64 + "\n"
        "extractor_version: source-contract-v1\n"
        "discovery_method: rss_excerpt\n"
        "source_support: 1.0\n"
        "{truncation}\n"
        "---\n\n"
        "## 基本信息\n\n- **来源**: RSS\n\n"
        "这是一段结构完整、来源边界清晰且足够长的证据正文。\n"
    )
    missing_reason = base.format(truncation="source_is_truncated: true")
    explicit_reason = base.format(
        truncation=(
            "source_is_truncated: true\n"
            'source_truncation_reason: "crawler_feed_content_limit"'
        )
    )

    assert "invalid_source_brief" in analyze_post(missing_reason).fatal_reasons
    assert analyze_post(explicit_reason).status == "source_brief"


def test_modern_source_brief_accepts_a_fully_escaped_stored_capture() -> None:
    body = (
        "## 基本信息\n\n- **来源**: RSS\n\n"
        "## 来源摘要/节选\n\n"
        + ("> &amp; complete captured evidence\n" * 1_200)
        + "\n## 来源说明\n\n本页完整呈现已经保存的来源证据。\n"
    )
    document = (
        "---\n"
        "title: Complete stored capture\n"
        "description: Complete stored source evidence.\n"
        "entry_kind: auto\n"
        "source: blogs_podcasts\n"
        "content_mode: source_brief\n"
        "external_url: https://example.com/complete-source\n"
        "publication_tier: C\n"
        "source_capture_mode: excerpt\n"
        "source_completeness: partial\n"
        "source_snapshot_sha256: sha256:" + "a" * 64 + "\n"
        "extractor_version: source-contract-v1\n"
        "discovery_method: rss_excerpt\n"
        "source_is_truncated: false\n"
        "source_support: 1.0\n"
        "---\n\n"
        + body
    )

    assert len(body.encode("utf-8")) > 32_000
    assert analyze_post(document).status == "source_brief"


def test_uncontracted_auto_posts_fail_closed_after_legacy_migration() -> None:
    body = (
        "## 技术分析\n\n"
        "这是一段结构完整的自动生成内容，用于验证已评审历史边界。"
        "内容包含足够的实质性文字、清晰的技术背景和可读的结论。"
        "文档的段落、标点和结束位置都完整，可以作为稳定的回归测试样本。\n"
    )
    old = (
        "---\ntitle: Reviewed legacy\nentry_kind: auto\nsource: arxiv\n"
        "date: 2026-07-15T14:00:41+08:00\n"
        "external_url: https://example.com/legacy\n---\n\n" + body
    )
    new = old.replace(
        "title: Reviewed legacy",
        "title: Uncontracted future post",
    ).replace(
        "2026-07-15T14:00:41+08:00",
        "2026-07-15T16:55:26+08:00",
    )

    assert "missing_source_contract" in analyze_post(old).fatal_reasons
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
        "---\ntitle: Container\ndescription: Container description.\n"
        "entry_kind: manual\n---\n\n"
        "## 常见问题\n\n### 如何部署\n\n这里有完整答案。\n"
    )
    empty_sibling = (
        "---\ntitle: Empty sibling\ndescription: Empty sibling description.\n"
        "entry_kind: manual\n---\n\n"
        "## 最佳实践\n\n## 最佳实践指南\n\n这里有完整内容。\n"
    )

    assert "empty_section" not in analyze_post(container).warning_reasons
    assert "empty_section" in analyze_post(empty_sibling).warning_reasons


def test_empty_section_cleanup_removes_only_empty_sibling_headings() -> None:
    body = (
        "## 常见问题\n\n### 如何部署\n\n这里有完整答案。\n\n"
        "## 最佳实践\n\n## 最佳实践指南\n\n这里也有完整内容。\n\n"
        "## 空容器\n\n### 空子标题\n\n## 最终章节\n\n这里仍有内容。\n\n"
        "```markdown\n## 代码块标题\n\n## 代码块中的相邻标题\n```\n"
    )

    cleaned, removed = remove_empty_section_headings(body)

    assert removed == 3
    assert "## 常见问题" in cleaned
    assert "## 最佳实践\n" not in cleaned
    assert "## 最佳实践指南" in cleaned
    assert "## 空容器" not in cleaned
    assert "### 空子标题" not in cleaned
    assert "## 最终章节" in cleaned
    assert "## 代码块标题" in cleaned


def test_legacy_hn_uses_the_shared_structural_tail_gate() -> None:
    body = (
        "## 分析\n\n这一段旧生成内容在解释模型架构时突然停在高带宽显存和矩阵，"
        "\n\n## 引用\n\n- [原文](https://example.com)\n"
    )
    hn = (
        "---\ntitle: HN\nentry_kind: auto\nsource: hacker_news\ncontent_mode: legacy_analysis\n"
        "external_url: https://example.com/hn\n---\n\n" + body
    )
    manual = (
        "---\ntitle: Manual\nentry_kind: manual\nsource: manual\n"
        "external_url: https://example.com/manual\n---\n\n" + body
    )

    assert "truncated_pre_citation_tail" in analyze_post(hn).fatal_reasons
    assert "unterminated_prose" not in analyze_post(hn).fatal_reasons
    assert "truncated_pre_citation_tail" not in analyze_post(manual).fatal_reasons


def test_shared_structural_tail_gate_is_limited_to_auto_legacy_analysis() -> None:
    body = (
        "## 分析\n\n这一段旧生成内容在解释模型架构时突然停在高带宽显存和矩阵，"
        "\n\n## 引用\n\n- [原文](https://example.com)\n"
    )
    legacy = (
        "---\ntitle: Legacy HN\ndescription: Legacy analysis.\n"
        "entry_kind: auto\nsource: hacker_news\ncontent_mode: legacy_analysis\n"
        "external_url: https://example.com/legacy\n---\n\n" + body
    )
    manual_hn = legacy.replace("entry_kind: auto", "entry_kind: manual")
    modern_analysis = legacy.replace("content_mode: legacy_analysis", "content_mode: complete")
    other_source = legacy.replace("source: hacker_news", "source: blogs_podcasts")

    assert "truncated_pre_citation_tail" in analyze_post(legacy).fatal_reasons
    assert "truncated_pre_citation_tail" not in analyze_post(manual_hn).fatal_reasons
    assert "truncated_pre_citation_tail" not in analyze_post(modern_analysis).fatal_reasons
    assert "truncated_pre_citation_tail" in analyze_post(other_source).fatal_reasons
    for document in (legacy, manual_hn, modern_analysis, other_source):
        assert "unterminated_prose" not in analyze_post(document).fatal_reasons


def test_unterminated_prose_exempts_source_briefs_footers_lists_and_links() -> None:
    prefix = (
        "---\ntitle: HN boundary\ndescription: Boundary fixture.\n"
        "entry_kind: auto\nsource: hacker_news\ncontent_mode: legacy_analysis\n"
        "external_url: https://example.com/hn\n---\n\n"
    )
    footer = prefix + "## 结论\n\n正文自然结束。\n\n*本文由 AI Stack 自动整理*\n"
    list_tail = prefix + "## 清单\n\n- 第一项无句号\n- 第二项无句号\n"
    link_tail = prefix + "## 来源\n\n[查看完整来源](https://example.com/source)\n"
    source_brief = (
        "---\ntitle: Brief\ndescription: Brief fixture.\n"
        "entry_kind: auto\nsource: hacker_news\ncontent_mode: legacy_source_brief\n"
        "source_provenance: legacy_no_snapshot\nsource_support: 0.0\n"
        "external_url: https://example.com/brief\n---\n\n"
        "## 基本信息\n\n- **来源**: Hacker News\n\n"
        "这是一段足够完整但末尾没有句号的来源叙述\n"
    )

    for document in (footer, list_tail, link_tail, source_brief):
        assert "unterminated_prose" not in analyze_post(document).fatal_reasons


def test_manifest_quarantines_structurally_incomplete_active_posts(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "truncated.md").write_text(
        "---\ntitle: Truncated\ndescription: Truncated description.\n---\n\n"
        "## 示例\n\n```python\nprint('cut')\n",
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
        "description: A concise source card.\n"
        "entry_kind: auto\n"
        "source: hacker_news\n"
        "content_mode: legacy_source_brief\n"
        "source_provenance: legacy_no_snapshot\n"
        "source_support: 0.0\n"
        "external_url: https://example.com/brief\n"
        "---\n\n"
        "## 基本信息\n\n这是来源卡片中的可核验摘要。\n",
        encoding="utf-8",
    )
    (posts / "complete.md").write_text(
        "---\n"
        "title: Complete\n"
        "description: A complete manual record.\n"
        "source: manual\n"
        "external_url: https://example.com/complete\n"
        "---\n\n"
        "## 完整记录\n\n这是简短但不应误判为来源快报的手工记录。\n",
        encoding="utf-8",
    )

    manifest = build_content_quality_manifest(content)

    assert manifest["schema_version"] == "content_quality_manifest_v4"
    assert manifest["source_brief_count"] == 1
    assert manifest["complete_count"] == 1
    assert manifest["active_count"] == 2
    assert manifest["pages"]["posts/brief.md"] == {
        "status": "source_brief",
        "reasons": ["concise_source_card"],
    }
    assert "posts/complete.md" not in manifest["pages"]


def test_manifest_tracks_verified_provenance_and_rehydration_backlog(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    digest_a = "sha256:" + "a" * 64
    digest_b = "sha256:" + "b" * 64
    sentence = "这段内容只陈述来源能够直接支持且可以复核的工程事实。"
    required_headings = (
        "转写说明",
        "核心结论",
        "能力机制",
        "快速开始",
        "适用边界",
        "核验清单",
        "来源与核验",
    )
    rewrite_body = "\n\n".join(
        f"## {heading}\n\n{sentence * 6}" for heading in required_headings
    )
    documents = {
        "modern-brief.md": (
            "---\n"
            "title: Modern brief\n"
            "description: Signed source excerpt.\n"
            "entry_kind: auto\n"
            "source: blogs_podcasts\n"
            "content_mode: source_brief\n"
            "publication_tier: C\n"
            "source_capture_mode: excerpt\n"
            "source_completeness: partial\n"
            f"source_snapshot_sha256: {digest_a}\n"
            "extractor_version: source-contract-v1\n"
            "discovery_method: rss_excerpt\n"
            "source_is_truncated: false\n"
            "source_support: 1.0\n"
            "external_url: https://example.com/brief\n"
            "---\n\n"
            "## 基本信息\n\n- **来源**: RSS\n\n这是来源中保存的可核验摘要。\n"
        ),
        "modern-rewrite.md": (
            "---\n"
            "title: Modern rewrite\n"
            "description: Signed evidence-backed rewrite.\n"
            "entry_kind: auto\n"
            "source: juejin\n"
            "content_mode: evidence_backed_rewrite\n"
            "publication_tier: B\n"
            "source_capture_mode: full_article\n"
            "source_completeness: complete\n"
            "source_is_truncated: false\n"
            f"source_snapshot_sha256: {digest_a}\n"
            f"parent_snapshot_sha256: {digest_b}\n"
            "extractor_version: source-contract-v2\n"
            "discovery_method: article_html\n"
            "source_support: 1.0\n"
            "external_url: https://juejin.cn/post/1234567890\n"
            f"---\n\n{rewrite_body}\n"
        ),
        "curated-rewrite.md": (
            "---\n"
            "title: Curated rewrite\n"
            "description: Independently verified editorial rewrite.\n"
            "entry_kind: curated\n"
            "source: blogs_podcasts\n"
            "content_mode: evidence_backed_rewrite\n"
            "publication_tier: B\n"
            "source_capture_mode: curated_sources\n"
            "source_completeness: verified\n"
            "source_is_truncated: false\n"
            "external_url: https://example.com/original\n"
            "editorial_sources:\n"
            "  - https://example.com/original\n"
            "  - https://docs.example.com/primary\n"
            f"---\n\n## 独立核验\n\n{sentence * 40}\n"
        ),
        "legacy-analysis.md": (
            "---\n"
            "title: Legacy analysis\n"
            "description: No retained source snapshot.\n"
            "entry_kind: auto\n"
            "source: hacker_news\n"
            "content_mode: legacy_analysis\n"
            "publication_tier: LEGACY\n"
            "source_provenance: legacy_no_snapshot\n"
            "source_support: 0.0\n"
            "external_url: https://example.com/legacy\n"
            f"---\n\n## 历史分析\n\n{sentence * 4}\n"
        ),
        "legacy-brief.md": (
            "---\n"
            "title: Legacy brief\n"
            "description: No retained source snapshot.\n"
            "entry_kind: auto\n"
            "source: hacker_news\n"
            "content_mode: legacy_source_brief\n"
            "publication_tier: C\n"
            "source_provenance: legacy_no_snapshot\n"
            "source_support: 0.0\n"
            "external_url: https://example.com/legacy-brief\n"
            "---\n\n## 基本信息\n\n这是历史来源卡片中的简短记录。\n"
        ),
        "archived.md": (
            "---\n"
            "title: Archived\n"
            "archived: true\n"
            "source: arxiv\n"
            "content_mode: archived\n"
            "---\n\n该条目只保留透明归档入口。\n"
        ),
        "manual.md": (
            "---\n"
            "title: Manual record\n"
            "description: Manual record without a crawler source contract.\n"
            "entry_kind: manual\n"
            "source: manual\n"
            "external_url: https://example.com/manual\n"
            "---\n\n## 手工记录\n\n这是手工维护的完整记录。\n"
        ),
    }
    for name, document in documents.items():
        (posts / name).write_text(document, encoding="utf-8")

    manifest = build_content_quality_manifest(content)

    assert manifest["verified_provenance_count"] == 3
    assert manifest["rehydration_pending_count"] == 3
    assert manifest["rehydration_pending_by_source"] == {
        "arxiv": 1,
        "hacker_news": 2,
    }


def test_manifest_does_not_verify_invalid_modern_source_contracts(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "invalid-brief.md").write_text(
        "---\n"
        "title: Invalid brief\n"
        "description: Missing an immutable source digest.\n"
        "entry_kind: auto\n"
        "source: blogs_podcasts\n"
        "content_mode: source_brief\n"
        "publication_tier: C\n"
        "source_capture_mode: excerpt\n"
        "extractor_version: source-contract-v1\n"
        "discovery_method: rss_excerpt\n"
        "source_is_truncated: false\n"
        "source_support: 1.0\n"
        "external_url: https://example.com/invalid-brief\n"
        "---\n\n## 基本信息\n\n这是没有来源摘要签名的卡片。\n",
        encoding="utf-8",
    )
    (posts / "invalid-rewrite.md").write_text(
        "---\n"
        "title: Invalid rewrite\n"
        "description: Missing the required evidence sections.\n"
        "entry_kind: auto\n"
        "source: juejin\n"
        "content_mode: evidence_backed_rewrite\n"
        "publication_tier: B\n"
        "source_capture_mode: full_article\n"
        "source_completeness: complete\n"
        "source_is_truncated: false\n"
        f"source_snapshot_sha256: {('sha256:' + 'a' * 64)}\n"
        f"parent_snapshot_sha256: {('sha256:' + 'b' * 64)}\n"
        "extractor_version: source-contract-v2\n"
        "discovery_method: article_html\n"
        "source_support: 1.0\n"
        "external_url: https://juejin.cn/post/1234567890\n"
        "---\n\n## 不完整\n\n缺少来源转写所要求的完整结构。\n",
        encoding="utf-8",
    )

    manifest = build_content_quality_manifest(content)

    assert manifest["verified_provenance_count"] == 0
    assert manifest["rehydration_pending_count"] == 0
    assert manifest["rehydration_pending_by_source"] == {}
    assert manifest["quarantined_count"] == 2


def test_manifest_keeps_pending_archives_with_unknown_source_visible(
    tmp_path: Path,
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "archived.md").write_text(
        "---\ntitle: Archived\narchived: true\n---\n\n透明归档记录。\n",
        encoding="utf-8",
    )

    manifest = build_content_quality_manifest(content)

    assert manifest["verified_provenance_count"] == 0
    assert manifest["rehydration_pending_count"] == 1
    assert manifest["rehydration_pending_by_source"] == {"unknown": 1}


def test_article_template_quarantines_manifest_entries_from_body_and_search() -> None:
    template = (ROOT / "blog/themes/terminal-theme/layouts/_default/single.html").read_text(
        encoding="utf-8"
    )

    assert ".Site.Data.content_quality" in template
    assert 'data-pagefind-ignore="all"' in template
    assert 'data-content-quality-status="quarantined"' in template
    assert ".Params.archived" in template
    assert "$isQualityBlocked" in template
    assert 'content="noindex, nofollow"' in template
    assert "历史正文已隔离" in template
    assert "{{ .Content }}" in template


def test_article_template_labels_short_source_cards_without_hiding_the_body() -> None:
    template = (ROOT / "blog/themes/terminal-theme/layouts/_default/single.html").read_text(
        encoding="utf-8"
    )

    assert "$isSourceBrief" in template
    assert '"source_brief"' in template
    assert "len .RawContent" in template
    assert ".WordCount" not in template
    assert 'data-content-mode="source-brief"' in template
    assert "来源快报" in template
    assert "以原始来源为准" in template
    assert "{{ .Content }}" in template


def test_article_template_labels_legacy_analysis_without_claiming_source_completeness() -> None:
    template = (ROOT / "blog/themes/terminal-theme/layouts/_default/single.html").read_text(
        encoding="utf-8"
    )

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

    assert (
        main(
            [
                "--content-root",
                str(content),
                "--output",
                str(tmp_path / "quality.json"),
                "--fail-on-quarantine",
            ]
        )
        == 1
    )


def test_manifest_cli_can_fail_closed_on_empty_section_warnings(
    tmp_path: Path,
) -> None:
    from scripts.build_content_quality_manifest import main

    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "empty-section.md").write_text(
        "---\ntitle: Empty section\ndescription: Empty section description.\n"
        "entry_kind: manual\n---\n\n"
        "## 空标题\n\n## 有内容的标题\n\n这里有完整内容。\n",
        encoding="utf-8",
    )

    assert (
        main(
            [
                "--content-root",
                str(content),
                "--output",
                str(tmp_path / "quality.json"),
                "--fail-on-structural-warning",
            ]
        )
        == 1
    )


def test_manifest_cli_can_fail_closed_on_unverified_active_provenance(
    tmp_path: Path,
) -> None:
    from scripts.build_content_quality_manifest import main

    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "manual.md").write_text(
        "---\n"
        "title: Manual note\n"
        "description: A readable but unverified manual note.\n"
        "entry_kind: manual\n"
        "---\n\n"
        "## 研究记录\n\n这是一段结构完整、但没有可核验来源契约的人工记录。\n",
        encoding="utf-8",
    )

    output = tmp_path / "quality.json"
    assert (
        main(
            [
                "--content-root",
                str(content),
                "--output",
                str(output),
                "--fail-on-unverified-provenance",
            ]
        )
        == 1
    )

    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["active_count"] == 1
    assert manifest["verified_provenance_count"] == 0
