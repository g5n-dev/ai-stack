from __future__ import annotations

import re
from pathlib import Path

import yaml

from ai_stack.content_quality import analyze_post, markdown_body
from ai_stack.historical_repair import _plain_description, build_historical_repair_plan


def _write_post(
    root: Path,
    name: str,
    *,
    title: str,
    body: str,
    description: str | None = None,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, object] = {
        "title": title,
        "date": "2026-07-15T00:00:00+08:00",
        "draft": False,
        "source": "fixture",
        "external_url": f"https://example.com/{name.removesuffix('.md')}",
        "tags": ["AI 工程"],
        "categories": ["AI 工程"],
        "scenarios": ["AI/ML项目"],
        "content_mode": "legacy_analysis",
        "publication_tier": "LEGACY",
        "source_provenance": "legacy_no_snapshot",
        "source_support": 0.0,
    }
    if description is not None:
        metadata["description"] = description
    frontmatter = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
    ).rstrip()
    path = root / name
    path.write_text(f"---\n{frontmatter}\n---\n\n{body.strip()}\n", encoding="utf-8")
    return path


def _planned_document(root: Path, path: Path) -> str:
    plan = build_historical_repair_plan(content_root=root)
    operation = next(write for write in plan.writes if write.path == path.name)
    return operation.content.decode("utf-8")


def _metadata(document: str) -> dict[str, object]:
    parsed = yaml.safe_load(document.split("---", 2)[1])
    assert isinstance(parsed, dict)
    return parsed


def test_current_source_brief_provenance_is_preserved_idempotently(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    root.mkdir(parents=True)
    metadata = {
        "title": "Complete current source brief",
        "date": "2026-07-15T20:45:47+08:00",
        "draft": False,
        "entry_kind": "auto",
        "tags": ["AI"],
        "categories": [],
        "source": "blogs_podcasts",
        "content_mode": "source_brief",
        "publication_tier": "C",
        "source_capture_mode": "excerpt",
        "source_snapshot_sha256": "sha256:" + "a" * 64,
        "extractor_version": "source-contract-v1",
        "discovery_method": "rss_excerpt",
        "source_is_truncated": False,
        "source_support": 1.0,
        "description": "完整呈现已经保存的 RSS 来源证据，并明确说明证据边界。",
        "external_url": "https://example.com/current-source-brief",
    }
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    body = (
        "## 基本信息\n\n- **来源**: RSS\n\n"
        "## 来源摘要/节选\n\n> 这是完整保存的来源内容。\n\n"
        "## 来源说明\n\n本页只呈现已保存的来源证据，不包含扩展推断。\n"
    )
    (root / "current-source-brief.md").write_text(
        f"---\n{frontmatter}\n---\n\n{body}",
        encoding="utf-8",
    )

    plan = build_historical_repair_plan(content_root=root)

    assert plan.writes == ()
    assert plan.deletes == ()


def test_atx_h1_and_missing_description_are_repaired_without_touching_fences(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "atx.md",
        title="AI Stack 深度观察",
        body=(
            "# **AI Stack** 深度观察\n\n"
            "---\n\n"
            "这篇分析梳理了 [动态知识图谱](https://example.com/graph) 的数据来源、"
            "聚类逻辑与渐进加载策略，并依据已经保存在正文中的工程事实解释为何"
            "首屏只展示核心节点，搜索后再加载社区，最后按需展开节点邻域。"
            "这种设计同时降低网络传输、布局计算和浏览器绘制成本，也让读者更容易"
            "理解关系强度、社区边界与文章证据之间的对应关系。\n\n"
            "# 工程影响\n\n"
            "正文中的第二个一级标题必须降级，但语义和内容保持不变。\n\n"
            "```markdown\n# 围栏内标题\n---\n```"
        ),
    )

    document = _planned_document(root, path)
    metadata = _metadata(document)
    body = markdown_body(document)

    assert not body.startswith("# **AI Stack** 深度观察")
    assert not body.startswith("---")
    assert "## 工程影响" in body
    assert "\n# 工程影响\n" not in body
    assert "```markdown\n# 围栏内标题\n---\n```" in body
    description = metadata["description"]
    assert isinstance(description, str)
    assert 80 <= len(description) <= 200
    assert "动态知识图谱" in description
    assert "https://" not in description
    assert not re.search(r"[*_`#\[\]]", description)


def test_setext_leading_h1_backfills_a_strictly_truncated_title(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "setext.md",
        title="从信息流到知识",
        description="已有摘要必须原样保留，不应被结构迁移覆盖。",
        body=(
            "从信息流到知识图谱：完整工程路径\n"
            "================================\n\n"
            "***\n\n"
            "正文基于已经保存的实现细节，依次解释采集、规范化、社区切分与邻域加载。\n\n"
            "社区关系\n"
            "========\n\n"
            "这一节继续说明社区之间的加权连接。\n\n"
            "~~~markdown\n围栏中的演示标题\n================\n~~~"
        ),
    )

    document = _planned_document(root, path)
    metadata = _metadata(document)
    body = markdown_body(document)

    assert metadata["title"] == "从信息流到知识图谱：完整工程路径"
    assert metadata["description"] == "已有摘要必须原样保留，不应被结构迁移覆盖。"
    assert not body.startswith("从信息流到知识图谱")
    assert not body.startswith("***")
    assert "## 社区关系" in body
    assert "社区关系\n========" not in body
    assert "~~~markdown\n围栏中的演示标题\n================\n~~~" in body


def test_non_equivalent_leading_h1_is_demoted_without_replacing_title(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "different-title.md",
        title="编辑标题",
        description="这是一段已经存在且经过人工编辑的摘要，因此迁移时必须完整保留。",
        body="# 正文原标题\n\n这里保留来源中已有的标题语义与正文事实。",
    )

    document = _planned_document(root, path)

    assert _metadata(document)["title"] == "编辑标题"
    assert markdown_body(document).startswith("## 正文原标题")


def test_missing_description_prefers_intro_prose_over_basic_information(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "intro-description.md",
        title="摘要来源优先级",
        body=(
            "## 基本信息\n\n"
            "- **作者**: Fixture Author\n"
            "- **来源**: Example Feed\n"
            "- **编号**: 2026-0715\n\n"
            "## 导语\n\n"
            "以下为您撰写的导语，旨在帮助读者快速理解主题：\n\n"
            "这里是一个为你精心打造的“超级引人入胜”的引言，旨在瞬间抓住读者的眼球：\n\n"
            "本文从已保存的正文证据出发，说明历史文章为什么需要同时修复标题层级、"
            "重复分隔线和摘要字段。迁移只重组已有文本，不调用模型补写，也不会把"
            "作者、来源、编号等元数据列表误当成文章摘要，从而确保搜索结果中的简介"
            "可以准确表达文章主题，并在重复运行时保持完全稳定。\n\n"
            "## 详细分析\n\n"
            "后续段落继续展开实现细节。"
        ),
    )

    description = _metadata(_planned_document(root, path))["description"]

    assert isinstance(description, str)
    assert description.startswith("本文从已保存的正文证据出发")
    assert "以下为您撰写" not in description
    assert "精心打造" not in description
    assert "Fixture Author" not in description
    assert "Example Feed" not in description
    assert 80 <= len(description) <= 200


def test_adjacent_horizontal_rules_collapse_outside_fenced_code(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "rules.md",
        title="分隔线整理",
        description="该摘要已经存在，测试只验证相邻分隔线会折叠且代码围栏中的示例保持原样。",
        body=(
            "第一段是已保存的可核验事实。\n\n"
            "---\n\n"
            "***\n\n"
            "___\n\n"
            "第二段继续提供上下文。\n\n"
            "```markdown\n---\n***\n___\n```"
        ),
    )

    body = markdown_body(_planned_document(root, path))

    assert body.count("\n---\n") == 2  # 正文一个，围栏一个。
    assert "\n***\n" not in body.removesuffix("```\n")[: -len("```markdown\n---\n***\n___\n")]
    assert "```markdown\n---\n***\n___\n```" in body


def test_title_generation_prompt_leak_is_archived_instead_of_rewritten(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "prompt-leak.md",
        title="根据标题生成文章",
        body=(
            "请根据以下标题生成一篇完整文章，并补充看似合理的案例和结论："
            "《动态图谱工程》。这些文字属于标题生成提示，不是可核验的来源正文。"
        ),
    )

    document = _planned_document(root, path)
    metadata = _metadata(document)

    assert metadata["archived"] is True
    assert metadata["content_mode"] == "archived"
    assert metadata["archive_reason"] == "historical_content_quality_gate"
    assert "description" in metadata
    assert "请根据以下标题生成" not in markdown_body(document)


def test_truncated_description_is_rebuilt_only_from_existing_body_evidence(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    stale_description = "旧" * 160
    evidence = (
        "本文依据已经保存在正文中的日志、边界条件和验证结果，说明系统为何失败、"
        "修复如何完成，以及哪些事实能够支持最终结论。迁移过程不会调用模型补写，"
        "也不会根据标题猜测任何缺失内容。"
    )
    path = _write_post(
        root,
        "truncated-description.md",
        title="历史描述重建",
        description=stale_description,
        body=f"## 摘要\n\n{evidence}\n\n## 结论\n\n现有证据支持该结论。",
    )

    document = _planned_document(root, path)
    description = _metadata(document)["description"]

    assert description == evidence
    assert description != stale_description
    assert "truncated_description" not in analyze_post(document).fatal_reasons


def test_plain_description_marks_a_word_safe_summary_cut_with_ellipsis() -> None:
    prose = "甲" * 190 + " deploymentPipelineSafety 后续正文继续提供已保存的证据"

    description = _plain_description(f"## 摘要\n\n{prose}")

    assert description == "甲" * 190 + "…"
    assert len(description) <= 200
    assert description.encode("utf-8").decode("utf-8") == description


def test_complete_160_character_description_is_preserved(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    complete_description = "甲" * 159 + "。"
    path = _write_post(
        root,
        "complete-description.md",
        title="完整描述边界",
        description=complete_description,
        body="# 摘要\n\n正文完整记录了事实依据、工程约束与最终结论。",
    )

    document = _planned_document(root, path)

    assert _metadata(document)["description"] == complete_description
    assert "truncated_description" not in analyze_post(document).fatal_reasons


def test_truncated_description_without_body_evidence_is_transparently_archived(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "no-description-evidence.md",
        title="无摘要证据",
        description="旧" * 160,
        body="## 摘要\n\n证据太短。",
    )

    plan = build_historical_repair_plan(content_root=root)
    group = plan.manifest["groups"][0]
    rendered = next(write.content for write in plan.writes if write.path == path.name).decode()

    assert group["disposition"] == "archive_stub"
    assert group["body_source"] is None
    assert _metadata(rendered)["archived"] is True


def test_misplaced_strong_marker_before_emoji_is_removed_without_touching_valid_bold(
    tmp_path: Path,
) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "misplaced-strong.md",
        title="学习要点格式修复",
        description="正文已经完整保存，只需要清理误置的 Markdown 标记。",
        body=(
            "## 学习要点\n\n"
            "- 核心差异化：现有证据支持这一完整结论。** 🤖✨\n"
            "- 高可用与容灾是系统地基** 🛡️：现有证据支持服务连续性。\n"
            "- 📝 隐式状态管理**：历史结果能够作为上下文记忆。\n"
            "- **完整加粗句。** 🚀\n\n"
            "## 引用\n\n- [原文](https://example.com)"
        ),
    )

    document = _planned_document(root, path)
    body = markdown_body(document)

    assert "完整结论。 🤖✨" in body
    assert "完整结论。** 🤖✨" not in body
    assert "系统地基 🛡️：现有证据" in body
    assert "系统地基** 🛡️：现有证据" not in body
    assert "📝 隐式状态管理：历史结果" in body
    assert "📝 隐式状态管理**：历史结果" not in body
    assert "**完整加粗句。** 🚀" in body

    path.write_text(document, encoding="utf-8")
    assert not build_historical_repair_plan(content_root=root).writes


def test_structural_repair_plan_is_idempotent(tmp_path: Path) -> None:
    root = tmp_path / "content/posts"
    path = _write_post(
        root,
        "idempotent.md",
        title="幂等迁移",
        body=(
            "# 幂等迁移\n\n---\n\n"
            "正文保存了足够多的可核验信息，用于生成稳定摘要。"
            "迁移第一次运行时会移除重复标题、补齐摘要并整理分隔线；"
            "第二次运行必须产生完全相同的字节，不得继续增加标题标记、"
            "修改摘要或产生新的计划操作。这条约束保证 dry-run 结果可信，"
            "也保证正式批次可以安全重试而不会积累格式漂移。"
        ),
    )

    first = build_historical_repair_plan(content_root=root)
    operation = next(write for write in first.writes if write.path == path.name)
    path.write_bytes(operation.content)

    second = build_historical_repair_plan(content_root=root)

    assert second.manifest["dry_run"] is True
    assert second.manifest["planned_changes"] == 0
    assert second.writes == ()
