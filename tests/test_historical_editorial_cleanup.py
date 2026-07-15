from __future__ import annotations

from pathlib import Path

import yaml

from ai_stack.content_quality import analyze_post, markdown_body, markdown_frontmatter
from ai_stack.historical_repair import build_historical_repair_plan

SAFE_DESCRIPTION = "该摘要来自现有正文，完整说明文章主题、工程背景与主要结论。"
SAFE_BODY = (
    "## 摘要\n\n"
    "这是已经保存且结构完整的正文，包含足够的事实上下文、工程约束和闭合结论。"
    "历史修复只能对明确的编辑助手前导语执行确定性清理，不能改写文章观点，也不能"
    "根据标题或残缺片段生成新的内容。\n\n"
    "## 结论\n\n现有证据支持这一结论。"
)


def _write_post(
    root: Path,
    name: str,
    *,
    title: str = "历史编辑清理测试",
    description: str = SAFE_DESCRIPTION,
    body: str = SAFE_BODY,
    external_url: str | None = None,
    date: str = "2026-07-15T00:00:00+08:00",
    source: str = "fixture",
    tags: list[str] | None = None,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, object] = {
        "title": title,
        "description": description,
        "date": date,
        "draft": False,
        "source": source,
        "external_url": external_url or f"https://example.com/{name.removesuffix('.md')}",
        "tags": tags or ["AI 工程"],
        "categories": ["AI 工程"],
        "scenarios": ["AI/ML项目"],
        "content_mode": "legacy_analysis",
        "publication_tier": "LEGACY",
        "source_provenance": "legacy_no_snapshot",
        "source_support": 0.0,
    }
    if source == "hacker_news":
        metadata["entry_kind"] = "auto"
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    path = root / name
    path.write_text(f"---\n{frontmatter}\n---\n\n{body.strip()}\n", encoding="utf-8")
    return path


def _plan(root: Path):
    return build_historical_repair_plan(content_root=root)


def _rendered(plan, relative_path: str) -> str:
    return next(write.content for write in plan.writes if write.path == relative_path).decode(
        "utf-8"
    )


def test_intro_editorial_preamble_and_following_decorations_are_removed(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    meta = "这里为您撰写了一个极具吸引力的引言，融合了工程痛点和明确悬念："
    actual_intro = (
        "真正的引言从已经保存的任务事实开始，解释系统为什么失败、团队如何定位"
        "根因，以及哪些遥测证据能够支持最终结论。"
    )
    path = _write_post(
        root,
        "intro.md",
        body=(
            "## ✨ 引人入胜的引言\n\n"
            f"{meta}\n\n***\n\n**【引言】**\n\n{actual_intro}\n\n"
            "## 摘要\n\n后续正文保持原样并以完整标点结束。"
        ),
    )

    assert "editorial_meta_preamble" in analyze_post(path.read_text(encoding="utf-8")).fatal_reasons
    rendered = _rendered(_plan(root), path.name)
    body = markdown_body(rendered)

    assert meta not in body
    assert "【引言】" not in body
    assert "***" not in body
    assert actual_intro in body
    assert "## ✨ 引人入胜的引言" in body
    assert analyze_post(rendered).fatal_reasons == ()


def test_frontmatter_description_editorial_preamble_is_removed(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    actual = "真正的描述保留了任务背景、失败事实和可核验结论。"
    path = _write_post(
        root,
        "description.md",
        description=(
            f"这里为你撰写了一个极具吸引力的引言，融合了惊险开场与工程悬念： **【引言】** {actual}"
        ),
    )

    assert "editorial_meta_preamble" in analyze_post(path.read_text(encoding="utf-8")).fatal_reasons
    rendered = _rendered(_plan(root), path.name)

    assert markdown_frontmatter(rendered)["description"] == actual
    assert markdown_body(rendered).strip() == SAFE_BODY
    assert analyze_post(rendered).fatal_reasons == ()


def test_normal_intro_and_meta_like_text_outside_intro_are_preserved(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    normal_intro = "这里介绍系统的真实约束、故障现象与已有证据，不是助手编辑说明。"
    outside_intro = "这里为您撰写了一个引言模板：该句位于方法章节，不能静默删除。"
    body = (
        f"## 导语\n\n{normal_intro}\n\n"
        f"## 方法\n\n{outside_intro}\n\n"
        "## 摘要\n\n正文以完整事实和闭合结论结束。"
    )
    path = _write_post(
        root,
        "normal-boundary.md",
        body=body,
        tags=["AI编程"],
    )

    rendered = _rendered(_plan(root), path.name)

    assert markdown_body(rendered).strip() == body
    assert normal_intro in rendered
    assert outside_intro in rendered


def test_editorial_preamble_inside_fenced_code_is_preserved(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    fenced = "这里为您撰写了一个极具吸引力的引言："
    body = (
        "## 导语\n\n```markdown\n"
        f"{fenced}\n**【引言】**\n***\n```\n\n"
        "围栏之后是真实且完整的导语。\n\n## 摘要\n\n正文完整结束。"
    )
    path = _write_post(root, "fenced.md", body=body, tags=["AI编程"])

    rendered = _rendered(_plan(root), path.name)

    assert markdown_body(rendered).strip() == body
    assert fenced in rendered


def test_entire_translation_response_description_section_is_removed(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    assistant_text = (
        "这段文字已经是中文。请您确认一下，您是想把它翻译成英文，还是希望对原中文内容进行润色？"
    )
    body = (
        "## 导语\n\n真实导语完整保留。\n\n---\n"
        f"## 描述\n\n{assistant_text}\n\n---\n"
        "## 摘要\n\n这里是结构完整且可核验的实际摘要。"
    )
    path = _write_post(root, "translation.md", body=body)

    assert (
        "translation_response_leak" in analyze_post(path.read_text(encoding="utf-8")).fatal_reasons
    )
    rendered = _rendered(_plan(root), path.name)
    cleaned = markdown_body(rendered)

    assert assistant_text not in cleaned
    assert "## 描述" not in cleaned
    assert "## 导语" in cleaned
    assert "## 摘要" in cleaned
    assert "\n---\n" not in cleaned
    assert analyze_post(rendered).fatal_reasons == ()


def test_entire_multiblock_translation_assistant_section_is_removed(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    assistant_text = (
        "您好，您提供的文本已经是中文了。\n\n"
        "这段文字是：\n\n"
        "> 本文探讨可安装 Skill 的工程化价值。\n\n"
        "请问您是否需要：\n\n"
        "1. 将英文文本翻译成中文？\n"
        "2. 将这段中文改写或润色？\n\n"
        "请告诉我，我可以更好地帮助您！"
    )
    body = f"## 描述\n\n{assistant_text}\n\n---\n## 评论\n\n这里是结构完整且可核验的实际评论。"
    path = _write_post(root, "translation-multiblock.md", body=body)

    assert (
        "translation_response_leak" in analyze_post(path.read_text(encoding="utf-8")).fatal_reasons
    )
    rendered = _rendered(_plan(root), path.name)
    cleaned = markdown_body(rendered)

    assert assistant_text not in cleaned
    assert "## 描述" not in cleaned
    assert "## 评论" in cleaned
    assert analyze_post(rendered).fatal_reasons == ()


def test_translation_section_can_precede_complete_learning_points(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    assistant_text = (
        "这段文字已经是中文，不需要翻译。如果您需要其他语言的翻译，"
        "或者对中文表达有其他优化需求，请告诉我！"
    )
    body = (
        f"## 描述\n\n{assistant_text}\n\n---\n## 学习要点\n\n这里保留了可核验的工程要点和原始结论。"
    )
    path = _write_post(root, "translation-before-learning.md", body=body)

    rendered = _rendered(_plan(root), path.name)
    cleaned = markdown_body(rendered)

    assert assistant_text not in cleaned
    assert "## 描述" not in cleaned
    assert "## 学习要点" in cleaned
    assert analyze_post(rendered).fatal_reasons == ()


def test_attention_translation_assistant_description_is_removed(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    assistant_text = (
        "您好，我注意到您提供的这段内容本身就是中文的。如果您需要我帮忙，"
        "可以选择翻译、润色或改写。请问您具体需要什么样的帮助呢？"
    )
    body = f"## 描述\n\n{assistant_text}\n\n---\n## 评论\n\n这里保留了可核验的原始评论和工程结论。"
    path = _write_post(root, "translation-attention.md", body=body)

    rendered = _rendered(_plan(root), path.name)
    cleaned = markdown_body(rendered)

    assert assistant_text not in cleaned
    assert "## 描述" not in cleaned
    assert "## 评论" in cleaned
    assert analyze_post(rendered).fatal_reasons == ()


def test_inline_translation_description_preserves_following_metadata(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    assistant_text = (
        "这段内容本身就是中文，不需要翻译。我可以提供润色版本供您参考。\n\n"
        "> 这里是助手生成的改写版本。\n\n"
        "请问您是需要润色中文内容，还是有其他语言的原文需要翻译？"
    )
    body = (
        "## 基本信息\n\n"
        f"- **描述**: {assistant_text}\n"
        "- **语言**: Java\n"
        "- **星标**: 36,666\n\n"
        "## 摘要\n\n这里保留了真实项目摘要。"
    )
    path = _write_post(root, "translation-inline.md", body=body)

    rendered = _rendered(_plan(root), path.name)
    cleaned = markdown_body(rendered)

    assert assistant_text not in cleaned
    assert "- **描述**" not in cleaned
    assert "- **语言**: Java" in cleaned
    assert "- **星标**: 36,666" in cleaned
    assert "## 摘要" in cleaned
    assert analyze_post(rendered).fatal_reasons == ()


def test_normal_or_mixed_description_section_is_never_silently_deleted(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    normal_body = (
        "## 描述\n\n该段直接描述系统架构、运行约束和验证结果。\n\n## 摘要\n\n正文完整结束。"
    )
    normal = _write_post(
        root,
        "normal-description.md",
        body=normal_body,
        tags=["AI编程"],
    )
    normal_rendered = _rendered(_plan(root), normal.name)

    assert markdown_body(normal_rendered).strip() == normal_body

    inline_body = (
        "## 基本信息\n\n"
        "- **描述**: 该段直接描述系统架构、运行约束和验证结果。\n"
        "- **语言**: Python\n\n"
        "## 摘要\n\n正文完整结束。"
    )
    inline = _write_post(
        root,
        "normal-inline-description.md",
        body=inline_body,
        tags=["AI编程"],
    )
    inline_rendered = _rendered(_plan(root), inline.name)

    assert markdown_body(inline_rendered).strip() == inline_body

    mixed_root = tmp_path / "mixed/content/posts"
    mixed = _write_post(
        mixed_root,
        "mixed-description.md",
        body=(
            "## 描述\n\n这段文字已经是中文。\n\n"
            "第二段包含真实架构事实、运行数据和不可丢失的人工结论。\n\n"
            "## 摘要\n\n正文完整结束。"
        ),
    )
    mixed_plan = _plan(mixed_root)

    assert mixed_plan.manifest["groups"][0]["disposition"] == "archive_stub"
    assert mixed_plan.manifest["groups"][0]["body_source"] is None
    assert mixed.name in mixed_plan.manifest["groups"][0]["paths"]


def test_decorated_leading_h2_equivalent_to_frontmatter_title_is_removed_once(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    title = "🛰️首颗 VLEO 卫星任务复盘"
    repeated = "## 📰 🛰️首颗 VLEO 卫星任务复盘"
    path = _write_post(
        root,
        "decorated-title.md",
        title=title,
        body=(
            f"{repeated}\n\n---\n\n真实正文从任务背景开始。\n\n{repeated}\n\n后续同名章节必须保留。"
        ),
    )

    body = markdown_body(_rendered(_plan(root), path.name))

    assert body.count(repeated) == 1
    assert body.startswith("真实正文从任务背景开始。")
    assert not body.startswith("---")
    assert "后续同名章节必须保留。" in body


def test_heading_echo_line_is_removed_only_when_immediately_and_exactly_equal(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    echo = "1: 为什么需要渐进加载"
    near_but_not_equal = "2: 为什么需要缓存？"
    body = (
        f"### {echo}\n\n{echo}\n\n真实答案保留。\n\n"
        f"### {near_but_not_equal}\n\n2: 为什么需要缓存\n\n近似文本不能删除。\n\n"
        "```markdown\n### 3: 围栏示例\n\n3: 围栏示例\n```\n\n"
        f"普通段落再次提到 {echo}，不能删除。"
    )
    path = _write_post(root, "heading-echo.md", body=body)

    rendered = markdown_body(_rendered(_plan(root), path.name))

    assert rendered.count(echo) == 2  # heading + 后续普通段落。
    assert f"### {echo}\n\n真实答案保留。" in rendered
    assert f"### {near_but_not_equal}\n\n2: 为什么需要缓存" in rendered
    assert "### 3: 围栏示例\n\n3: 围栏示例" in rendered


def test_truncated_pre_citation_tail_uses_sibling_or_transparent_archive(
    tmp_path: Path,
) -> None:
    truncated_body = (
        "## 摘要\n\n"
        "这段 Hacker News 历史正文在引用之前突然停止，最后一个技术判断包含足够长的"
        "中文内容但没有形成闭合句子并且仍然停留在未完成的推理链条中，\n\n"
        "## 🔗 引用\n\n- [原始来源](https://example.com/source)"
    )
    external_url = "https://example.com/truncated-before-citation"
    root = tmp_path / "recover/content/posts"
    broken = _write_post(
        root,
        "20260101-broken.md",
        body=truncated_body,
        external_url=external_url,
        date="2026-01-01T00:00:00+08:00",
        source="hacker_news",
    )
    trusted = _write_post(
        root,
        "20260201-trusted.md",
        body=SAFE_BODY,
        external_url=external_url,
        date="2026-02-01T00:00:00+08:00",
        source="hacker_news",
    )

    assert (
        "truncated_pre_citation_tail"
        in analyze_post(broken.read_text(encoding="utf-8")).fatal_reasons
    )
    group = _plan(root).manifest["groups"][0]

    assert group["body_source"] == trusted.name
    assert group["integrity_decision"]["action"] == "restore_from_complete_sibling"
    assert group["integrity_decision"]["failure_reasons"] == ["truncated_pre_citation_tail"]

    archive_root = tmp_path / "archive/content/posts"
    singleton = _write_post(
        archive_root,
        "singleton.md",
        body=truncated_body,
        external_url="https://example.com/archive-truncated-before-citation",
        source="hacker_news",
    )
    archived_group = _plan(archive_root).manifest["groups"][0]

    assert archived_group["body_source"] is None
    assert archived_group["disposition"] == "archive_stub"
    assert archived_group["integrity_decision"]["action"] == "transparent_archive"
    assert singleton.name in archived_group["integrity_decision"]["failed_paths"]
