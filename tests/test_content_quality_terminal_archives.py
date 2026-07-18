from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_stack.content_quality import (
    build_content_quality_manifest,
    is_terminal_recovery_failure_archive,
)


def _terminal_metadata(**overrides: object) -> dict[str, object]:
    metadata: dict[str, object] = {
        "title": "Historical recovery record",
        "archived": True,
        "content_mode": "archived",
        "publication_tier": "ARCHIVED",
        "source": "blogs_podcasts",
        "source_provenance": "historical_recovery_failed",
        "source_support": 0.0,
        "external_url": "https://blog.example/unavailable",
        "archive_reason": "historical_source_recovery_failed",
        "recovery_failure_type": "source_fetch_error",
        "recovery_failure_reason": "source_access_interstitial",
        "recovery_attempted_at": "2026-07-18T02:03:04Z",
        "tags": [],
        "categories": [],
        "scenarios": [],
        "build": {"list": "never", "render": "always"},
    }
    metadata.update(overrides)
    return metadata


def _terminal_body(
    *,
    failure_type: str = "source_fetch_error",
    failure_reason: str = "source_access_interstitial",
    external_url: str = "https://blog.example/unavailable",
) -> str:
    return (
        "## 历史来源恢复说明\n\n"
        "该条目的公开来源恢复未能完成，旧正文未被保留。\n\n"
        f"- **恢复失败类型**: `{failure_type}`\n"
        f"- **恢复失败原因**: `{failure_reason}`\n"
        f"- **原始来源**: [查看公开来源](<{external_url}>)\n"
    )


def _write_post(
    posts: Path,
    name: str,
    metadata: dict[str, object],
    *,
    body: str | None = None,
) -> None:
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    (posts / name).write_text(
        f"---\n{frontmatter}\n---\n\n{body or _terminal_body()}",
        encoding="utf-8",
    )


def test_terminal_recovery_failure_archive_requires_a_strict_auditable_contract() -> None:
    assert is_terminal_recovery_failure_archive(_terminal_metadata(), _terminal_body())
    assert is_terminal_recovery_failure_archive(
        _terminal_metadata(recovery_attempted_at="2026-07-18T10:03:04+08:00"),
        _terminal_body(),
    )


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("archived", "true"),
        ("content_mode", "legacy_analysis"),
        ("archive_reason", "historical_content_quality_gate"),
        ("source", "manual"),
        ("external_url", "https://user:secret@blog.example/unavailable"),
        ("external_url", "http://127.0.0.1/unavailable"),
        ("external_url", "http://internal/unavailable"),
        ("recovery_failure_type", "Source Fetch Error"),
        ("recovery_failure_type", "source__fetch_error"),
        ("recovery_failure_type", "other_safe_error"),
        ("recovery_failure_reason", "source-access-interstitial"),
        ("recovery_failure_reason", "source_access_interstitial_"),
        ("recovery_attempted_at", "2026-07-18T02:03:04"),
        ("recovery_attempted_at", "not-a-time"),
        ("tags", ["未经核验旧标签"]),
        ("categories", ["未经核验旧分类"]),
        ("scenarios", ["未经核验旧场景"]),
        ("build", {"list": "always", "render": "always"}),
    ),
)
def test_terminal_recovery_failure_archive_rejects_forged_fields(
    field: str,
    value: object,
) -> None:
    assert not is_terminal_recovery_failure_archive(
        _terminal_metadata(**{field: value}),
        _terminal_body(),
    )


@pytest.mark.parametrize(
    "body",
    (
        "该条目只是普通归档。\n",
        _terminal_body().replace("`source_fetch_error`", "`dispatch_error`"),
        _terminal_body().replace("source_access_interstitial", "robots_disallowed"),
        _terminal_body().replace("https://blog.example/unavailable", "https://evil.example/"),
        _terminal_body() + ("填" * 4096),
    ),
)
def test_terminal_recovery_failure_archive_rejects_forged_body(body: str) -> None:
    assert not is_terminal_recovery_failure_archive(_terminal_metadata(), body)


def test_manifest_separates_terminal_failure_archives_from_pending_archives(
    tmp_path: Path,
) -> None:
    posts = tmp_path / "content" / "posts"
    posts.mkdir(parents=True)
    _write_post(posts, "terminal.md", _terminal_metadata())
    _write_post(
        posts,
        "ordinary.md",
        {
            "title": "Ordinary archive",
            "archived": True,
            "content_mode": "archived",
            "source": "arxiv",
        },
    )
    _write_post(
        posts,
        "forged-metadata.md",
        _terminal_metadata(
            source="hacker_news",
            recovery_attempted_at="2026-07-18T02:03:04",
        ),
    )
    _write_post(
        posts,
        "forged-body.md",
        _terminal_metadata(source="juejin"),
        body="该条目只是普通归档。\n",
    )

    manifest = build_content_quality_manifest(tmp_path / "content")

    assert manifest["archived_count"] == 4
    assert manifest["rehydration_terminal_count"] == 1
    assert manifest["rehydration_terminal_by_source"] == {"blogs_podcasts": 1}
    assert manifest["recovery_failure_type_counts"] == {"source_fetch_error": 1}
    assert manifest["recovery_failure_reason_counts"] == {
        "source_access_interstitial": 1
    }
    assert manifest["rehydration_pending_count"] == 3
    assert manifest["rehydration_pending_by_source"] == {
        "arxiv": 1,
        "hacker_news": 1,
        "juejin": 1,
    }
    assert manifest["pages"]["posts/terminal.md"]["recovery_failure"] == {
        "type": "source_fetch_error",
        "reason": "source_access_interstitial",
    }
    assert all(
        "recovery_failure" not in manifest["pages"][f"posts/{name}.md"]
        for name in ("ordinary", "forged-metadata", "forged-body")
    )
