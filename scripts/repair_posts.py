#!/usr/bin/env python3
"""
Batch repair historical posts by normalizing public markdown structure.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

import yaml


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from processor.markdown_normalizer import (  # noqa: E402
    extract_bulleted_items,
    filter_related_resources,
    looks_incomplete_text,
    normalize_generated_markdown,
    normalize_heading_text,
    parse_faq_markdown,
    remove_markdown_sections_by_heading,
)


SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
URL_RE = re.compile(r"https?://[^\s)]+")
DATE_PREFIX_RE = re.compile(r"^(?P<stamp>\d{8})-")

STRICT_TEMPLATES: dict[str, list[str]] = {
    "arxiv": [
        "基本信息",
        "导语",
        "摘要",
        "评论",
        "技术分析",
        "研究最佳实践",
        "学习要点",
        "学习路径",
        "常见问题",
        "相关资源",
        "引用",
        "站内链接",
    ],
    "hacker_news": [
        "基本信息",
        "导语",
        "摘要",
        "评论",
        "代码示例",
        "案例研究",
        "最佳实践",
        "学习要点",
        "常见问题",
        "相关资源",
        "引用",
        "站内链接",
    ],
    "github_trending": [
        "基本信息",
        "DeepWiki 速览（节选）",
        "导语",
        "摘要",
        "评论",
        "技术分析",
        "代码示例",
        "案例研究",
        "对比分析",
        "最佳实践",
        "性能优化建议",
        "学习要点",
        "学习路径",
        "常见问题",
        "推荐资源",
        "引用",
        "站内链接",
    ],
}

NORMALIZE_TEMPLATES: dict[str, list[str]] = {
    "blogs_podcasts": [
        "基本信息",
        "摘要/简介",
        "导语",
        "摘要",
        "评论",
        "技术分析",
        "最佳实践",
        "学习要点",
        "相关资源",
        "引用",
        "站内链接",
    ],
    "juejin": [
        "基本信息",
        "导语",
        "描述",
        "摘要",
        "评论",
        "学习要点",
        "常见问题",
        "引用",
        "站内链接",
    ],
}

ALL_KNOWN_SECTION_TITLES = set()
for template_titles in list(STRICT_TEMPLATES.values()) + list(NORMALIZE_TEMPLATES.values()):
    ALL_KNOWN_SECTION_TITLES.update(template_titles)

AUTO_FOOTER_LINE_RE = re.compile(r"^\*?(?:本文|这篇文章).{0,40}AI Stack 自动生成.*\*?$")


def parse_csv(value: str) -> set[str]:
    if not value:
        return set()
    return {part.strip() for part in value.split(",") if part.strip()}


def split_frontmatter(text: str) -> tuple[str, dict, str]:
    if not text.startswith("---\n"):
        return "", {}, text

    lines = text.splitlines()
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return "", {}, text

    fm_text = "\n".join(lines[1:end_idx]).strip()
    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")
    try:
        frontmatter = yaml.safe_load(fm_text) or {}
    except Exception:
        frontmatter = {}
    return fm_text, frontmatter, body


def parse_post_date(path: Path, frontmatter: dict) -> date | None:
    raw = frontmatter.get("date")
    if raw:
        try:
            if isinstance(raw, datetime):
                return raw.date()
            return datetime.fromisoformat(str(raw)).date()
        except Exception:
            pass

    match = DATE_PREFIX_RE.match(path.name)
    if not match:
        return None
    return datetime.strptime(match.group("stamp"), "%Y%m%d").date()


def split_top_level_sections(body: str, source: str) -> tuple[list[str], list[tuple[str, str]]]:
    header_lines: list[str] = []
    sections: list[tuple[str, str]] = []
    current_title = ""
    current_lines: list[str] = []
    in_code_fence = False
    started = False

    for raw in body.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence

        match = None if in_code_fence else SECTION_RE.match(stripped)
        if match:
            started = True
            if current_title:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = match.group(1).strip()
            current_lines = []
            continue

        if not started:
            header_lines.append(raw.rstrip())
        else:
            current_lines.append(raw.rstrip())

    if current_title:
        sections.append((current_title, "\n".join(current_lines).strip()))

    return header_lines, sections


def canonical_section_title(source: str, title: str) -> str | None:
    norm = normalize_heading_text(title)
    if not norm:
        return None

    if norm in {"思考题", "挑战与思考题"}:
        return None
    if norm == "基本信息":
        return "基本信息"
    if norm in {"deepwiki速览节选", "deepwiki速览", "deepwiki"}:
        return "DeepWiki 速览（节选）"
    if norm == "导语":
        return "导语"
    if norm == "描述":
        return "描述"
    if norm in {"摘要简介", "摘要/简介"}:
        return "摘要/简介"
    if norm == "摘要":
        return "摘要"
    if norm in {"评论", "深度评论"}:
        return "评论"
    if norm in {"技术分析", "深度分析"}:
        return "技术分析"
    if norm == "代码示例":
        return "代码示例"
    if norm == "案例研究":
        return "案例研究"
    if norm in {"对比分析", "与同类方案对比"}:
        return "对比分析"
    if norm in {"最佳实践", "最佳实践指南"}:
        return "研究最佳实践" if source == "arxiv" else "最佳实践"
    if norm == "研究最佳实践":
        return "研究最佳实践"
    if norm == "性能优化建议":
        return "性能优化建议"
    if norm in {"学习要点", "核心学习要点", "关键要点"}:
        return "学习要点"
    if norm == "学习路径":
        return "学习路径"
    if norm in {"常见问题", "常见问题解答", "faq"}:
        return "常见问题"
    if norm in {"推荐资源", "相关资源"}:
        return "推荐资源" if source == "github_trending" else "相关资源"
    if norm == "引用":
        return "引用"
    if norm == "站内链接":
        return "站内链接"
    return title.strip()


def cleanup_thematic_breaks(text: str) -> str:
    lines = [line.rstrip() for line in str(text or "").splitlines()]
    while lines and lines[0].strip() in {"", "---"}:
        lines.pop(0)
    while lines and lines[-1].strip() in {"", "---"}:
        lines.pop()
    return "\n".join(lines).strip()


def strip_auto_footer_lines(text: str) -> str:
    out: list[str] = []
    for raw in str(text or "").splitlines():
        if AUTO_FOOTER_LINE_RE.match(raw.strip()):
            continue
        out.append(raw.rstrip())
    return "\n".join(out).strip()


def rebase_inner_headings(text: str) -> str:
    if not text:
        return ""
    out: list[str] = []
    in_code_fence = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            out.append(raw.rstrip())
            continue
        if not in_code_fence:
            match = HEADING_RE.match(stripped)
            if match:
                level = max(3, len(match.group(1)))
                out.append(f"{'#' * level} {match.group(2).strip()}".rstrip())
                continue
        out.append(raw.rstrip())
    return "\n".join(out).strip()


def drop_heading_echo_lines(text: str) -> str:
    if not text:
        return ""
    out: list[str] = []
    pending_heading_norm = ""
    in_code_fence = False

    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            pending_heading_norm = ""
            out.append(raw.rstrip())
            continue
        if in_code_fence:
            out.append(raw.rstrip())
            continue

        match = HEADING_RE.match(stripped)
        if match:
            pending_heading_norm = normalize_heading_text(match.group(2))
            out.append(raw.rstrip())
            continue

        if not stripped:
            out.append("")
            continue

        if pending_heading_norm and normalize_heading_text(stripped) == pending_heading_norm:
            pending_heading_norm = ""
            continue

        pending_heading_norm = ""
        out.append(raw.rstrip())

    return "\n".join(out).strip()


def drop_trailing_incomplete_blocks(text: str) -> str:
    cleaned = str(text or "").strip()
    if not cleaned:
        return ""
    while cleaned and looks_incomplete_text(cleaned):
        blocks = re.split(r"\n\s*\n", cleaned)
        if len(blocks) <= 1:
            break
        blocks.pop()
        cleaned = "\n\n".join(blocks).strip()
        while cleaned:
            lines = cleaned.splitlines()
            last_line = next((line for line in reversed(lines) if line.strip()), "")
            if HEADING_RE.match(last_line.strip()):
                lines.pop()
                cleaned = "\n".join(lines).rstrip()
                continue
            break
    return cleaned.strip()


def parse_resources_from_markdown(text: str) -> list[dict]:
    resources: list[dict] = []
    lines = [line.rstrip() for line in str(text or "").splitlines()]
    current: dict[str, str] = {}

    def flush() -> None:
        nonlocal current
        if current.get("title") and current.get("link"):
            resources.append(
                {
                    "title": current.get("title", "").strip(),
                    "link": current.get("link", "").strip(),
                    "description": current.get("description", "").strip(),
                }
            )
        current = {}

    for raw in lines:
        line = raw.strip()
        if not line:
            flush()
            continue

        bold_match = re.match(r"^-?\s*\*\*(.+?)\*\*(?::\s*(https?://\S+))?$", line)
        if bold_match:
            flush()
            current["title"] = bold_match.group(1).strip()
            link = bold_match.group(2)
            if link:
                current["link"] = link.strip()
            continue

        if line.startswith(("名称：", "名称:", "Title:", "Title：")):
            flush()
            current["title"] = line.split(":", 1)[-1].split("：", 1)[-1].strip()
            continue
        if line.startswith(("链接：", "链接:", "Link:", "Link：")):
            current["link"] = line.split(":", 1)[-1].split("：", 1)[-1].strip()
            continue
        if line.startswith(("说明：", "说明:", "描述：", "描述:")):
            current["description"] = line.split(":", 1)[-1].split("：", 1)[-1].strip()
            continue

        url_match = URL_RE.search(line)
        if url_match:
            if not current:
                title = re.sub(r"^-+\s*", "", line[: url_match.start()]).strip(" :：-*")
                current["title"] = title or url_match.group(0)
            current["link"] = url_match.group(0)
            desc = line.replace(url_match.group(0), "").strip(" -:：")
            if desc and not current.get("description"):
                current["description"] = desc

    flush()
    return filter_related_resources(resources)


def render_resources(resources: list[dict]) -> str:
    lines: list[str] = []
    for resource in resources:
        lines.append(f"- **{resource['title']}**")
        lines.append(f"  - 链接: {resource['link']}")
        if resource.get("description"):
            lines.append(f"  - 说明: {resource['description']}")
        lines.append("")
    return "\n".join(lines).strip()


def render_faq(entries: list[dict]) -> str:
    lines: list[str] = []
    for faq in entries:
        question = str(faq.get("question") or "").strip()
        answer = str(faq.get("answer") or "").strip()
        if not question or not answer:
            continue
        lines.extend([f"### {question}", "", answer, ""])
    return "\n".join(lines).strip()


def normalize_generic_section(title: str, body: str) -> str:
    cleaned = strip_auto_footer_lines(cleanup_thematic_breaks(body))
    cleaned, _ = remove_markdown_sections_by_heading(cleaned, {"思考题", "挑战与思考题"})
    cleaned = normalize_generated_markdown(
        cleaned,
        wrapper_headings={title},
        strip_first_heading=True,
        demote_headings=False,
    )
    cleaned = rebase_inner_headings(cleaned)
    cleaned = drop_heading_echo_lines(cleaned)
    cleaned = drop_trailing_incomplete_blocks(cleaned)
    return cleaned.strip()


def normalize_section_body(source: str, title: str, body: str) -> str:
    raw = strip_auto_footer_lines(cleanup_thematic_breaks(body))
    if not raw:
        return ""

    if title in {"基本信息", "引用", "站内链接"}:
        return normalize_generated_markdown(
            raw,
            wrapper_headings={title},
            strip_first_heading=False,
            demote_headings=False,
        ).strip()

    if title == "学习要点":
        items = [
            item
            for item in extract_bulleted_items(raw)
            if "请提供您想要" not in item and "我才能根据" not in item and "谢谢" not in item
        ]
        return "\n".join(f"- {item}" for item in items).strip()

    if title == "常见问题":
        entries = parse_faq_markdown(raw)
        return render_faq(entries)

    if title in {"相关资源", "推荐资源"}:
        resources = parse_resources_from_markdown(raw)
        if resources:
            return render_resources(resources)
        return normalize_generic_section(title, raw)

    if title == "导语":
        cleaned = normalize_generated_markdown(
            raw,
            wrapper_headings={title},
            strip_first_heading=True,
            demote_headings=False,
        )
        cleaned = drop_trailing_incomplete_blocks(cleaned)
        return cleaned.strip()

    if title == "DeepWiki 速览（节选）":
        cleaned = normalize_generated_markdown(
            raw,
            wrapper_headings={title},
            strip_first_heading=True,
            demote_headings=False,
        )
        return rebase_inner_headings(cleaned).strip()

    cleaned = normalize_generic_section(title, raw)
    if title == "摘要" and not cleaned:
        return ""
    if title == "摘要" and looks_incomplete_text(cleaned):
        cleaned = drop_trailing_incomplete_blocks(cleaned)
    if title in {"代码示例", "案例研究"} and (cleaned.count("```") % 2 != 0):
        return ""
    if title in {"代码示例", "案例研究"} and looks_incomplete_text(cleaned):
        cleaned = drop_trailing_incomplete_blocks(cleaned)
    if title in {"代码示例", "案例研究"} and looks_incomplete_text(cleaned):
        return ""
    if source == "arxiv" and title == "最佳实践":
        title = "研究最佳实践"
    return cleaned.strip()


def pick_template(source: str, rewrite_sources: set[str], normalize_sources: set[str]) -> list[str]:
    if source in rewrite_sources:
        return STRICT_TEMPLATES.get(source, [])
    if source in normalize_sources:
        return NORMALIZE_TEMPLATES.get(source, [])
    return STRICT_TEMPLATES.get(source, NORMALIZE_TEMPLATES.get(source, []))


def preferred_parent_for_unknown(
    *,
    source: str,
    title: str,
    post_title: str,
    template: list[str],
    current_parent: str,
) -> str | None:
    norm = normalize_heading_text(title)
    post_title_norm = normalize_heading_text(post_title)

    summary_keywords = {
        "核心问题",
        "核心方案",
        "训练方法",
        "实验结果",
        "项目概述",
        "核心功能",
        "技术架构",
        "适用场景",
        "总结",
    }
    comment_keywords = {
        "研究创新性",
        "理论贡献",
        "实验验证",
        "可复现性",
        "综合评价",
        "核心观点评析",
        "论证逻辑审视",
        "关键案例评估",
        "价值与局限",
        "实践意义",
        "文章评价",
        "深度评价",
    }
    analysis_keywords = {
        "研究背景与问题",
        "核心方法与创新",
        "理论基础",
        "关键技术要点",
        "实际应用价值",
        "行业影响分析",
        "延伸思考",
        "学习建议",
        "案例分析",
        "哲学与逻辑",
        "核心观点深度解读",
        "技术架构深度剖析",
        "核心功能详细解读",
        "技术实现细节",
        "适用场景分析",
        "发展趋势展望",
    }

    if any(keyword in norm for keyword in summary_keywords):
        return "摘要" if "摘要" in template else None
    if post_title_norm and (norm in post_title_norm or post_title_norm in norm):
        return "摘要" if "摘要" in template else None
    if any(keyword in norm for keyword in comment_keywords) or ("评价" in norm and "评论" in template):
        return "评论" if "评论" in template else None
    if any(keyword in norm for keyword in analysis_keywords) or ("分析" in norm and "技术分析" in template):
        return "技术分析" if "技术分析" in template else None
    if norm.startswith("阶段") and "学习路径" in template:
        return "学习路径"
    if norm.startswith("实践"):
        if source == "arxiv" and "研究最佳实践" in template:
            return "研究最佳实践"
        if "最佳实践" in template:
            return "最佳实践"
    if norm.startswith("优化") and "性能优化建议" in template:
        return "性能优化建议"
    if current_parent and current_parent not in {"引用", "站内链接", "基本信息"}:
        return current_parent
    return None


def merge_sections(
    source: str,
    sections: list[tuple[str, str]],
    *,
    template: list[str],
    post_title: str,
) -> tuple[dict[str, str], list[str]]:
    merged: dict[str, str] = {}
    extras: list[str] = []
    current_parent = ""

    for original_title, body in sections:
        canonical_title = canonical_section_title(source, original_title)
        if canonical_title is None:
            continue
        if canonical_title not in ALL_KNOWN_SECTION_TITLES:
            parent = preferred_parent_for_unknown(
                source=source,
                title=original_title,
                post_title=post_title,
                template=template,
                current_parent=current_parent,
            )
            if not parent:
                continue
            nested_body = normalize_generic_section(original_title, body)
            if not nested_body:
                continue
            fragment = f"### {original_title.strip()}\n\n{nested_body}".strip()
            merged[parent] = f"{merged.get(parent, '').strip()}\n\n{fragment}".strip()
            if parent not in extras:
                extras.append(parent)
            continue
        normalized_body = normalize_section_body(source, canonical_title, body)
        if not normalized_body:
            continue
        if canonical_title in merged:
            merged[canonical_title] = f"{merged[canonical_title]}\n\n{normalized_body}".strip()
        else:
            merged[canonical_title] = normalized_body
            extras.append(canonical_title)
        current_parent = canonical_title

    return merged, extras


def rebuild_body(frontmatter: dict, source: str, merged: dict[str, str], ordered_titles: list[str], extras: list[str]) -> str:
    title = str(frontmatter.get("title") or "").strip() or "Untitled"
    lines = [f"# {title}", ""]

    titles_to_render: list[str] = []
    for title_name in ordered_titles:
        if merged.get(title_name):
            titles_to_render.append(title_name)

    for title_name in extras:
        if title_name in titles_to_render:
            continue
        if title_name in {"思考题", "挑战与思考题"}:
            continue
        titles_to_render.append(title_name)

    if titles_to_render:
        lines.append("---")

    for title_name in titles_to_render:
        body = merged.get(title_name, "").strip()
        if not body:
            continue
        lines.extend(["", f"## {title_name}", "", body, "", "---"])

    if lines and lines[-1] == "---":
        lines.pop()

    body_text = "\n".join(lines).strip() + "\n"
    body_text, _ = remove_markdown_sections_by_heading(body_text, {"思考题", "挑战与思考题"})
    return body_text


def dump_frontmatter(frontmatter: dict) -> str:
    return yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()


def repair_post(
    path: Path,
    *,
    start_date: date,
    end_date: date,
    rewrite_sources: set[str],
    normalize_sources: set[str],
    dry_run: bool,
) -> bool:
    original = path.read_text(encoding="utf-8")
    _, frontmatter, body = split_frontmatter(original)
    if not frontmatter:
        return False

    source = str(frontmatter.get("source") or "").strip()
    if source not in rewrite_sources and source not in normalize_sources:
        return False

    post_date = parse_post_date(path, frontmatter)
    if post_date is None or post_date < start_date or post_date > end_date:
        return False

    template = pick_template(source, rewrite_sources, normalize_sources)
    _, sections = split_top_level_sections(body, source)
    merged, extras = merge_sections(
        source,
        sections,
        template=template,
        post_title=str(frontmatter.get("title") or ""),
    )
    normalized_merged: dict[str, str] = {}
    for title, body in merged.items():
        normalized_body = normalize_section_body(source, title, body)
        if normalized_body:
            normalized_merged[title] = normalized_body
    merged = normalized_merged
    rebuilt_body = rebuild_body(frontmatter, source, merged, template, extras)
    rebuilt = f"---\n{dump_frontmatter(frontmatter)}\n---\n\n{rebuilt_body}"

    if rebuilt == original:
        return False

    if not dry_run:
        path.write_text(rebuilt, encoding="utf-8")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Repair historical Markdown posts")
    parser.add_argument("--date-from", required=True, help="开始日期，格式 YYYY-MM-DD")
    parser.add_argument("--date-to", required=True, help="结束日期，格式 YYYY-MM-DD")
    parser.add_argument("--rewrite-sources", default="", help="逗号分隔，需要严格模板重组的 source")
    parser.add_argument("--normalize-sources", default="", help="逗号分隔，只做结构归一的 source")
    parser.add_argument("--template", default="rich", help="保留的参数，当前用于兼容修复入口")
    parser.add_argument("--preserve-facts", action="store_true", help="保留历史事实上下文（默认行为）")
    parser.add_argument("--posts-dir", default=str(project_root / "blog" / "content" / "posts"))
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    start_date = datetime.strptime(args.date_from, "%Y-%m-%d").date()
    end_date = datetime.strptime(args.date_to, "%Y-%m-%d").date()
    rewrite_sources = parse_csv(args.rewrite_sources)
    normalize_sources = parse_csv(args.normalize_sources)
    posts_dir = Path(args.posts_dir)

    changed = 0
    for path in sorted(posts_dir.glob("*.md")):
        if repair_post(
            path,
            start_date=start_date,
            end_date=end_date,
            rewrite_sources=rewrite_sources,
            normalize_sources=normalize_sources,
            dry_run=args.dry_run,
        ):
            changed += 1

    print(f"repaired_posts={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
