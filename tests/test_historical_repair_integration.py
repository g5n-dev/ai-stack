from __future__ import annotations

import json
import os
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest
import yaml

from ai_stack.content_quality import write_content_quality_manifest
from ai_stack.historical_repair import (
    apply_historical_repair_plan,
    build_historical_repair_plan,
)
from ai_stack.migrations import MigrationSafetyError, source_revision
from ai_stack.pagefind_catalog import convert_pagefind_fragments
from processor.tag_graph import build_tag_graph_data

ROOT = Path(__file__).resolve().parents[1]
THEMES = ROOT / "blog/themes"
PAGEFIND = ROOT / "node_modules/.bin/pagefind"


def _write_post(
    posts: Path,
    name: str,
    *,
    title: str,
    external_url: str,
    body: str,
    tags: list[str],
) -> Path:
    posts.mkdir(parents=True, exist_ok=True)
    metadata = {
        "title": title,
        "description": "用于历史修复集成测试的可核验固定摘要。",
        "date": "2026-07-15T00:00:00+08:00",
        "draft": False,
        "source": "fixture",
        "external_url": external_url,
        "tags": tags,
        "categories": ["AI 工程"],
        "scenarios": ["AI/ML项目"],
    }
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    path = posts / name
    path.write_text(f"---\n{frontmatter}\n---\n\n{body.strip()}\n", encoding="utf-8")
    return path


def _plan(posts: Path):
    return build_historical_repair_plan(
        content_root=posts,
        category_whitelist=frozenset({"AI 工程"}),
        scenario_whitelist=frozenset({"AI/ML项目"}),
    )


def _git(repo: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _reviewed_repository(tmp_path: Path, *, branch: str) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    posts = repo / "content/posts"
    _write_post(
        posts,
        "canonical.md",
        title="Stable route",
        external_url="https://example.com/reviewed",
        body="可核验的短正文。",
        tags=["Stable"],
    )
    _write_post(
        posts,
        "duplicate.md",
        title="Richer body",
        external_url="https://example.com/reviewed",
        body="# 完整正文\n\n" + "可核验事实。" * 80,
        tags=["Reviewed"],
    )
    _git(repo, "init", "-b", branch)
    _git(repo, "config", "user.name", "Historical Repair Fixture")
    _git(repo, "config", "user.email", "fixture@example.com")
    _git(repo, "add", "content/posts")
    _git(repo, "commit", "-m", "fixture")
    return repo, posts


def _apply_reviewed(repo: Path, posts: Path, tmp_path: Path, *, digest: str):
    plan = _plan(posts)
    revision = source_revision(posts)
    assert revision == _git(repo, "rev-parse", "HEAD")
    return apply_historical_repair_plan(
        plan,
        expected_source_sha=revision,
        expected_code_sha=None,
        expected_plan_digest=digest,
        backup_id="reviewed-repair",
        max_changes=10,
        shadow_evidence_root=None,
        backup_root=tmp_path / "backups",
        repository_reviewed=True,
    )


def test_reviewed_repository_gate_accepts_a_real_clean_codex_branch(
    tmp_path: Path,
) -> None:
    repo, posts = _reviewed_repository(tmp_path, branch="codex/history-repair")
    plan = _plan(posts)

    result = _apply_reviewed(
        repo,
        posts,
        tmp_path,
        digest=plan.manifest["plan_digest"],
    )

    assert result["safety_profile"] == "reviewed_git_repository"
    assert result["mutation_performed"] is True
    assert (posts / "canonical.md").is_file()
    assert not (posts / "duplicate.md").exists()


def test_reviewed_repository_gate_rejects_a_real_dirty_codex_branch(
    tmp_path: Path,
) -> None:
    repo, posts = _reviewed_repository(tmp_path, branch="codex/history-repair")
    plan = _plan(posts)
    (repo / "unreviewed.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(MigrationSafetyError, match="clean Git worktree"):
        _apply_reviewed(
            repo,
            posts,
            tmp_path,
            digest=plan.manifest["plan_digest"],
        )

    assert (posts / "duplicate.md").is_file()
    assert not (tmp_path / "backups").exists()


def test_reviewed_repository_gate_rejects_a_real_main_branch(tmp_path: Path) -> None:
    repo, posts = _reviewed_repository(tmp_path, branch="main")
    plan = _plan(posts)

    with pytest.raises(MigrationSafetyError, match="codex/ branch"):
        _apply_reviewed(
            repo,
            posts,
            tmp_path,
            digest=plan.manifest["plan_digest"],
        )

    assert (posts / "duplicate.md").is_file()
    assert not (tmp_path / "backups").exists()


def test_reviewed_repository_gate_rejects_a_real_plan_digest_mismatch(
    tmp_path: Path,
) -> None:
    repo, posts = _reviewed_repository(tmp_path, branch="codex/history-repair")

    with pytest.raises(MigrationSafetyError, match="plan digest mismatch"):
        _apply_reviewed(
            repo,
            posts,
            tmp_path,
            digest="sha256:" + "0" * 64,
        )

    assert (posts / "duplicate.md").is_file()
    assert not (tmp_path / "backups").exists()


@pytest.mark.skipif(shutil.which("hugo") is None, reason="Hugo is not installed")
@pytest.mark.skipif(not PAGEFIND.is_file(), reason="Pagefind is not installed")
def test_archive_stub_is_excluded_from_active_manifest_graph_and_pagefind(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    site = tmp_path / "site"
    posts = site / "content/posts"
    clean = _write_post(
        posts,
        "clean.md",
        title="Trusted intelligence",
        external_url="https://example.com/clean",
        body="TRUSTED_PAGEFIND_TOKEN 可核验来源正文。",
        tags=["TrustedGraphTag"],
    )
    archived = _write_post(
        posts,
        "archived.md",
        title="Unverifiable archive",
        external_url="https://example.com/archived",
        body="由于您没有提供原始正文，我将根据标题推测完整细节。",
        tags=["ArchivedGraphPollution"],
    )

    plan = _plan(posts)
    archive_write = next(
        operation
        for operation in plan.writes
        if operation.path == archived.relative_to(posts).as_posix()
    )
    archived.write_bytes(archive_write.content)

    quality_manifest = write_content_quality_manifest(
        site / "content",
        site / "data/content_quality.json",
    )
    archived_record = quality_manifest["pages"]["posts/archived.md"]
    assert archived_record["status"] == "archived"
    assert "posts/clean.md" not in quality_manifest["pages"]
    assert (
        quality_manifest["source_file_count"]
        - quality_manifest["quarantined_count"]
        - quality_manifest["archived_count"]
        == 1
    )

    monkeypatch.setenv("TAG_INTRO_ENABLED", "0")
    graph = build_tag_graph_data(
        enable_content_mining=False,
        existing_output_path=None,
        content_dir=str(posts),
    )
    graph_node_ids = {node["id"] for node in graph["graph"]["nodes"]}
    assert graph["stats"]["tag_stats"]["total_articles"] == 1
    assert "tag:TrustedGraphTag" in graph_node_ids
    assert "tag:ArchivedGraphPollution" not in graph_node_ids

    (site / "hugo.toml").write_text(
        textwrap.dedent(
            f"""\
            baseURL = "https://fixture.example/"
            languageCode = "zh-CN"
            title = "Historical Repair Fixture"
            theme = "terminal-theme"
            themesDir = "{THEMES.as_posix()}"
            disableKinds = ["home", "taxonomy", "term", "RSS", "sitemap", "robotsTXT", "404"]

            [params]
            description = "historical repair fixture"
            author = "fixture"
            github = "https://github.com/example/example"
            profile_image = "/img/profile-holo.png"
            """
        ),
        encoding="utf-8",
    )
    public = site / "public"
    hugo = subprocess.run(
        [
            "hugo",
            "--source",
            str(site),
            "--destination",
            str(public),
            "--quiet",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert hugo.returncode == 0, hugo.stderr

    archived_html = next(
        path
        for path in public.rglob("index.html")
        if 'data-content-quality-status="archived"' in path.read_text(encoding="utf-8")
    )
    archived_render = archived_html.read_text(encoding="utf-8")
    assert archived_html.is_file()
    assert "data-pagefind-body" not in archived_render
    assert 'data-pagefind-ignore="all"' in archived_render
    assert 'content="noindex, nofollow"' in archived_render
    posts_index = (public / "posts/index.html").read_text(encoding="utf-8")
    assert "Trusted intelligence" in posts_index
    assert "Unverifiable archive" not in posts_index

    pagefind = subprocess.run(
        [str(PAGEFIND), "--site", str(public)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
        env={**os.environ, "NO_COLOR": "1"},
    )
    assert pagefind.returncode == 0, pagefind.stderr
    report = convert_pagefind_fragments(
        public,
        code_sha="a" * 40,
        content_sha="b" * 40,
    )
    catalog = json.loads((public / "pagefind/catalog.json").read_text(encoding="utf-8"))
    records = catalog["records"].values()
    urls = {record["url"] for record in records}
    titles = {record["title"] for record in catalog["records"].values()}

    assert report.record_count == 1
    assert "Trusted intelligence" in titles
    assert "Unverifiable archive" not in titles
    assert all("archived" not in url for url in urls)
    assert clean.is_file()
