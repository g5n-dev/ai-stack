from __future__ import annotations

import json
from pathlib import Path

from ai_stack.content_quality import (
    build_content_quality_manifest,
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
    assert "len .RawContent" in template
    assert ".WordCount" not in template
    assert 'data-content-mode="source-brief"' in template
    assert "来源快报" in template
    assert "以原始来源为准" in template
    assert "{{ .Content }}" in template
