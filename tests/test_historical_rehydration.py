from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import yaml

import ai_stack.historical_rehydration as historical_rehydration
from ai_stack.historical_rehydration import (
    HISTORICAL_REHYDRATION_SCHEMA,
    build_historical_rehydration_inventory,
)
from scripts.rehydrate_historical_content import main

SAFE_DESCRIPTION = "该条目用于验证纯离线历史来源恢复清单，不包含任何网络访问。"


def _document(
    *,
    source: str,
    external_url: str,
    body: str,
    **metadata: object,
) -> str:
    frontmatter: dict[str, object] = {
        "title": f"{source} inventory fixture",
        "description": SAFE_DESCRIPTION,
        "date": "2026-01-01T00:00:00+08:00",
        "draft": False,
        "entry_kind": "auto",
        "source": source,
        "external_url": external_url,
        "content_mode": "legacy_analysis",
        "publication_tier": "LEGACY",
        "source_provenance": "legacy_no_snapshot",
        "source_support": 0.0,
    }
    frontmatter.update(metadata)
    encoded = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).rstrip()
    return f"---\n{encoded}\n---\n\n{body.strip()}\n"


def _write_post(root: Path, name: str, document: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / name
    path.write_text(document, encoding="utf-8")
    return path


def _legacy_body(extra: str = "") -> str:
    return (
        "## 摘要\n\n"
        "当前文件是缺少来源快照的历史分析，只能进入来源恢复队列。"
        "清单不能根据这段正文补写或推测原始来源。\n\n"
        f"{extra}\n"
    )


def _source_brief() -> str:
    return _document(
        source="arxiv",
        external_url="http://arxiv.org/abs/2607.15273v1",
        body=(
            "## 基本信息\n\n- **来源**: arxiv\n\n"
            "## 来源摘要/节选\n\n> 这是 API 保存的论文摘要。\n\n"
            "## 来源说明\n\n当前保存的是来源摘要，不代表论文全文。"
        ),
        content_mode="source_brief",
        publication_tier="C",
        source_capture_mode="abstract",
        source_completeness="abstract_only",
        source_snapshot_sha256="sha256:" + "a" * 64,
        extractor_version="source-contract-v1",
        discovery_method="arxiv_api",
        source_is_truncated=False,
        source_support=1.0,
    )


def _curated_rewrite() -> str:
    return _document(
        source="juejin",
        external_url="https://juejin.cn/post/7663304647513718799",
        body=(
            "## 转写说明\n\n本文根据多个公开来源独立整理，非原文转载。\n\n"
            "## 核验结果\n\n这里记录已经人工核验的工程结论。"
            + "每项结论均对应公开的一手资料并保留适用边界。"
            * 40
        ),
        entry_kind="curated",
        content_mode="evidence_backed_rewrite",
        publication_tier="B",
        source_capture_mode="curated_sources",
        source_completeness="verified",
        source_is_truncated=False,
        editorial_sources=[
            "https://juejin.cn/post/7663304647513718799",
            "https://github.com/openinterpreter/openinterpreter",
        ],
    )


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _historical_hn_fixture(tmp_path: Path, *, historical_body: str) -> tuple[Path, Path, str]:
    repo = tmp_path / "repo"
    posts = repo / "blog/content/posts"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.name", "Historical Rehydration Test")
    _git(repo, "config", "user.email", "rehydration@example.com")
    target = _write_post(
        posts,
        "archived-hn.md",
        _document(
            source="hacker_news",
            external_url="https://example.com/original",
            body=historical_body,
        ),
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "historical body")
    historical_revision = _git(repo, "rev-parse", "HEAD")

    target.write_text(
        _document(
            source="hacker_news",
            external_url="https://example.com/original",
            body="## 历史条目归档说明\n\n该条目只保留透明归档记录。",
            archived=True,
            content_mode="archived",
            publication_tier="ARCHIVED",
        ),
        encoding="utf-8",
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "archive current body")
    return repo, posts, historical_revision


def test_inventory_is_stable_and_classifies_current_provenance(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    legacy = _write_post(
        posts,
        "legacy.md",
        _document(
            source="blogs_podcasts",
            external_url="https://openai.com/index/example",
            body=_legacy_body(),
        ),
    )
    _write_post(posts, "brief.md", _source_brief())
    _write_post(posts, "rewrite.md", _curated_rewrite())

    first = build_historical_rehydration_inventory(posts, repository_root=tmp_path)
    second = build_historical_rehydration_inventory(posts, repository_root=tmp_path)

    assert first == second
    assert first["schema"] == HISTORICAL_REHYDRATION_SCHEMA
    assert first["version"] == 1
    assert first["offline"] is True
    assert first["entry_count"] == 3
    assert first["classification_counts"] == {
        "needs_source_recovery": 1,
        "terminal_unrecoverable": 0,
        "verified_rewrite": 1,
        "verified_source_brief": 1,
    }
    assert [entry["path"] for entry in first["entries"]] == [
        "brief.md",
        "legacy.md",
        "rewrite.md",
    ]
    rows = {entry["path"]: entry for entry in first["entries"]}
    assert rows["legacy.md"]["target_sha256"] == hashlib.sha256(legacy.read_bytes()).hexdigest()
    assert rows["legacy.md"]["recovery_classification"] == "needs_source_recovery"
    assert rows["brief.md"]["recovery_classification"] == "verified_source_brief"
    assert rows["rewrite.md"]["recovery_classification"] == "verified_rewrite"


def test_inventory_classifies_strict_recovery_failure_archive_as_terminal(
    tmp_path: Path,
) -> None:
    posts = tmp_path / "posts"
    terminal = _document(
        source="blogs_podcasts",
        external_url="https://blog.example/unavailable",
        body=(
            "## 历史来源恢复说明\n\n"
            "该条目的公开来源恢复未能完成，旧正文未被保留。\n\n"
            "- **恢复失败类型**: `source_fetch_error`\n"
            "- **恢复失败原因**: `source_access_interstitial`\n"
            "- **原始来源**: <https://blog.example/unavailable>"
        ),
        archived=True,
        content_mode="archived",
        publication_tier="ARCHIVED",
        source_provenance="historical_recovery_failed",
        source_support=0.0,
        archive_reason="historical_source_recovery_failed",
        recovery_failure_type="source_fetch_error",
        recovery_failure_reason="source_access_interstitial",
        recovery_attempted_at="2026-07-18T02:03:04Z",
        tags=[],
        categories=[],
        scenarios=[],
        build={"list": "never", "render": "always"},
    )
    _write_post(posts, "terminal.md", terminal)

    report = build_historical_rehydration_inventory(posts, repository_root=tmp_path)

    assert report["classification_counts"] == {
        "needs_source_recovery": 0,
        "terminal_unrecoverable": 1,
        "verified_rewrite": 0,
        "verified_source_brief": 0,
    }
    assert report["entries"][0]["recovery_classification"] == "terminal_unrecoverable"


def test_inventory_extracts_stable_source_locators(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    fixtures = {
        "arxiv.md": (
            "arxiv",
            "http://arxiv.org/abs/2601.16194v1",
        ),
        "github.md": (
            "github_trending",
            "https://github.com/OpenInterpreter/open-interpreter.git",
        ),
        "juejin.md": (
            "juejin",
            "https://juejin.cn/post/7631425034263593014",
        ),
        "blog.md": (
            "blogs_podcasts",
            "https://huggingface.co/blog/example",
        ),
        "hn.md": (
            "hacker_news",
            "https://example.com/story",
        ),
    }
    for name, (source, url) in fixtures.items():
        extra = (
            "- **HN 讨论**: https://news.ycombinator.com/item?id=46746476\n\n"
            "```python\nexample = 'https://news.ycombinator.com/item?id=36984578'\n```"
            if source == "hacker_news"
            else ""
        )
        _write_post(
            posts,
            name,
            _document(source=source, external_url=url, body=_legacy_body(extra)),
        )

    report = build_historical_rehydration_inventory(posts, repository_root=tmp_path)
    locators = {entry["path"]: entry["source_locator"] for entry in report["entries"]}

    assert locators["arxiv.md"] == {
        "kind": "arxiv",
        "status": "resolved",
        "arxiv_id": "2601.16194v1",
        "origin": "canonical_url",
    }
    assert locators["github.md"] == {
        "kind": "github",
        "status": "resolved",
        "owner": "OpenInterpreter",
        "repo": "open-interpreter",
        "origin": "canonical_url",
    }
    assert locators["juejin.md"] == {
        "kind": "juejin",
        "status": "resolved",
        "article_id": "7631425034263593014",
        "origin": "canonical_url",
    }
    assert locators["blog.md"] == {
        "kind": "external_url",
        "status": "resolved",
        "origin": "canonical_url",
    }
    assert locators["hn.md"] == {
        "kind": "hacker_news",
        "status": "resolved",
        "hn_id": "46746476",
        "origin": "current_document",
    }


def test_archived_hn_locator_is_recovered_from_pinned_local_git_history(
    tmp_path: Path,
) -> None:
    repo, posts, revision = _historical_hn_fixture(
        tmp_path,
        historical_body=(
            _legacy_body() + "\n- **HN 讨论**: https://news.ycombinator.com/item?id=46746476\n"
        ),
    )

    report = build_historical_rehydration_inventory(
        posts,
        repository_root=repo,
        hn_git_revision=revision,
    )

    entry = report["entries"][0]
    assert entry["current_status"] == "archived"
    assert entry["source_locator"] == {
        "kind": "hacker_news",
        "status": "resolved",
        "hn_id": "46746476",
        "origin": "pinned_git_history",
        "git_revision": revision,
    }
    assert entry["recovery_classification"] == "needs_source_recovery"


def test_archived_hn_git_recovery_failures_are_typed_not_inferred(tmp_path: Path) -> None:
    repo, posts, revision = _historical_hn_fixture(
        tmp_path,
        historical_body=_legacy_body(),
    )

    missing_id = build_historical_rehydration_inventory(
        posts,
        repository_root=repo,
        hn_git_revision=revision,
    )["entries"][0]["source_locator"]
    missing_revision = build_historical_rehydration_inventory(
        posts,
        repository_root=repo,
        hn_git_revision="0" * 40,
    )["entries"][0]["source_locator"]

    assert missing_id == {
        "kind": "hacker_news",
        "status": "hn_id_missing_in_git_history",
        "origin": "pinned_git_history",
        "git_revision": revision,
    }
    assert missing_revision == {
        "kind": "hacker_news",
        "status": "hn_git_revision_unavailable",
        "origin": "pinned_git_history",
        "git_revision": "0" * 40,
    }


def test_archived_hn_git_lookup_disables_lazy_fetch_and_never_runs_network_verbs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    posts = tmp_path / "posts"
    _write_post(
        posts,
        "archived.md",
        _document(
            source="hacker_news",
            external_url="https://example.com/story",
            body="## 历史条目归档说明\n\n该条目只保留透明归档记录。",
            archived=True,
            content_mode="archived",
            publication_tier="ARCHIVED",
        ),
    )
    calls: list[tuple[list[str], dict[str, str]]] = []

    def reject_local_lookup(command, **kwargs):
        calls.append((command, kwargs["env"]))
        return subprocess.CompletedProcess(command, 1, stdout=b"", stderr=b"")

    monkeypatch.setattr(historical_rehydration.subprocess, "run", reject_local_lookup)

    locator = build_historical_rehydration_inventory(
        posts,
        repository_root=tmp_path,
        hn_git_revision="0" * 40,
    )["entries"][0]["source_locator"]

    assert locator["status"] == "hn_git_revision_unavailable"
    assert calls
    assert all(environment["GIT_NO_LAZY_FETCH"] == "1" for _command, environment in calls)
    assert all(environment["GIT_TERMINAL_PROMPT"] == "0" for _command, environment in calls)
    assert all(
        not {"fetch", "pull", "push", "ls-remote"}.intersection(command)
        for command, _environment in calls
    )


def test_hn_locator_rejects_ambiguous_current_ids_without_git_guessing(
    tmp_path: Path,
) -> None:
    posts = tmp_path / "posts"
    _write_post(
        posts,
        "ambiguous.md",
        _document(
            source="hacker_news",
            external_url="https://example.com/story",
            body=_legacy_body(
                "https://news.ycombinator.com/item?id=1\nhttps://news.ycombinator.com/item?id=2"
            ),
        ),
    )

    locator = build_historical_rehydration_inventory(
        posts,
        repository_root=tmp_path,
    )["entries"][0]["source_locator"]

    assert locator == {
        "kind": "hacker_news",
        "status": "hn_id_ambiguous_in_current_document",
        "origin": "current_document",
        "candidate_count": 2,
    }


def test_inventory_records_invalid_locator_as_a_typed_outcome(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    _write_post(
        posts,
        "bad-juejin.md",
        _document(
            source="juejin",
            external_url="https://juejin.cn/user/123",
            body=_legacy_body(),
        ),
    )

    report = build_historical_rehydration_inventory(posts, repository_root=tmp_path)

    assert report["entries"][0]["source_locator"] == {
        "kind": "juejin",
        "status": "juejin_article_id_missing",
        "origin": "canonical_url",
    }
    assert report["locator_status_counts"] == {"juejin_article_id_missing": 1}


def test_cli_is_dry_run_without_output_and_writes_only_an_explicit_audit_path(
    tmp_path: Path,
    capsys,
) -> None:
    posts = tmp_path / "posts"
    _write_post(
        posts,
        "entry.md",
        _document(
            source="blogs_podcasts",
            external_url="https://openai.com/index/example",
            body=_legacy_body(),
        ),
    )
    before = {path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")}

    assert (
        main(
            [
                "--inventory",
                "--content-root",
                str(posts),
                "--repository-root",
                str(tmp_path),
            ]
        )
        == 0
    )
    dry_report = json.loads(capsys.readouterr().out)
    after = {path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")}
    assert before == after

    output = tmp_path / "audit" / "historical-rehydration.json"
    assert (
        main(
            [
                "--inventory",
                "--content-root",
                str(posts),
                "--repository-root",
                str(tmp_path),
                "--output",
                str(output),
            ]
        )
        == 0
    )
    written_stdout = json.loads(capsys.readouterr().out)
    assert json.loads(output.read_text(encoding="utf-8")) == written_stdout == dry_report
    assert output.stat().st_mode & 0o777 == 0o600


def test_cli_rejects_writing_the_audit_inside_the_content_tree(
    tmp_path: Path,
    capsys,
) -> None:
    posts = tmp_path / "posts"
    _write_post(
        posts,
        "entry.md",
        _document(
            source="blogs_podcasts",
            external_url="https://openai.com/index/example",
            body=_legacy_body(),
        ),
    )
    output = posts / "inventory.json"

    assert (
        main(
            [
                "--inventory",
                "--content-root",
                str(posts),
                "--repository-root",
                str(tmp_path),
                "--output",
                str(output),
            ]
        )
        == 2
    )
    assert "outside --content-root" in capsys.readouterr().err
    assert not output.exists()


def test_cli_rejects_an_output_path_that_reenters_content_through_a_symlink(
    tmp_path: Path,
    capsys,
) -> None:
    posts = tmp_path / "posts"
    _write_post(
        posts,
        "entry.md",
        _document(
            source="blogs_podcasts",
            external_url="https://openai.com/index/example",
            body=_legacy_body(),
        ),
    )
    alias = tmp_path / "audit-alias"
    alias.symlink_to(posts, target_is_directory=True)
    output = alias / "nested" / "inventory.json"

    assert (
        main(
            [
                "--inventory",
                "--content-root",
                str(posts),
                "--repository-root",
                str(tmp_path),
                "--output",
                str(output),
            ]
        )
        == 2
    )
    assert "outside --content-root" in capsys.readouterr().err
    assert not (posts / "nested").exists()
