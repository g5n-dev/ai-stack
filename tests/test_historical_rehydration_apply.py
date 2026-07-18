from __future__ import annotations

import hashlib
import json
import os
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from ai_stack._json import sha256_digest
from ai_stack.historical_rehydration import (
    HISTORICAL_REHYDRATION_SCHEMA,
    HISTORICAL_REHYDRATION_VERSION,
)
from crawler.historical_source_fetch import HistoricalSourceCapture

HISTORICAL_DATE = "2026-01-02T03:04:05+08:00"
CAPTURED_AT = "2026-07-18T02:03:04Z"
OLD_SECRET = "OLD_UNVERIFIED_BODY_MUST_NOT_SURVIVE"


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _document(*, source: str, external_url: str) -> str:
    metadata = {
        "title": "未经核验的旧标题",
        "date": HISTORICAL_DATE,
        "draft": False,
        "entry_kind": "auto",
        "tags": ["未经核验旧标签"],
        "categories": ["未经核验旧分类"],
        "scenarios": ["未经核验旧场景"],
        "source": source,
        "external_url": external_url,
        "aliases": ["/posts/stable-route/"],
        "content_mode": "legacy_analysis",
        "publication_tier": "LEGACY",
        "source_provenance": "legacy_no_snapshot",
        "source_support": 0.0,
    }
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    return f"---\n{frontmatter}\n---\n\n## 旧正文\n\n{OLD_SECRET}\n"


def _write_post(root: Path, path: str, *, source: str, external_url: str) -> Path:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _document(source=source, external_url=external_url),
        encoding="utf-8",
    )
    return target


def _entry(
    root: Path,
    path: str,
    *,
    source: str,
    canonical_url: str,
    locator: dict[str, object],
) -> dict[str, object]:
    return {
        "path": path,
        "target_sha256": _sha256((root / path).read_bytes()),
        "source": source,
        "canonical_url": canonical_url,
        "current_status": "legacy_analysis",
        "current_mode": "legacy_analysis",
        "recovery_classification": "needs_source_recovery",
        "source_locator": locator,
    }


def _inventory(root: Path, entries: list[dict[str, object]]) -> dict[str, object]:
    ordered = sorted(entries, key=lambda entry: str(entry["path"]))
    return {
        "schema": HISTORICAL_REHYDRATION_SCHEMA,
        "version": HISTORICAL_REHYDRATION_VERSION,
        "offline": True,
        "content_root": str(root.absolute()),
        "entry_count": len(ordered),
        "entries_sha256": sha256_digest(ordered),
        "entries": ordered,
    }


def _capture(source: str, *, external_url: str) -> HistoricalSourceCapture:
    values: dict[str, dict[str, object]] = {
        "arxiv": {
            "title": "Evidence-aware agent systems",
            "source_text": "A bounded official abstract with verifiable evidence.",
            "capture_mode": "abstract",
            "source_completeness": "abstract_only",
            "source_is_truncated": False,
            "metadata": {
                "arxiv_id": "2601.00001v1",
                "authors": ["Ada"],
                "category": "cs.AI",
                "published": "2026-01-01T00:00:00Z",
            },
        },
        "github_trending": {
            "title": "OpenInterpreter/open-interpreter",
            "source_text": "A repository for evidence-aware agent execution.",
            "capture_mode": "metadata_only",
            "source_completeness": "metadata_only",
            "source_is_truncated": False,
            "metadata": {"language": "Python", "stars": 100, "today_stars": 2},
        },
        "hacker_news": {
            "title": "Evidence-aware AI runtime",
            "source_text": "Evidence-aware AI runtime",
            "capture_mode": "metadata_only",
            "source_completeness": "metadata_only",
            "source_is_truncated": False,
            "metadata": {
                "hn_id": 47158975,
                "author": "ada",
                "score": 100,
                "descendants": 20,
                "published": "2026-01-01T00:00:00Z",
            },
        },
        "juejin": {
            "title": "用 Rust 构建可验证 AI Agent",
            "source_text": "这是经过来源校验后保存的公开页面正文节选。",
            "capture_mode": "excerpt",
            "source_completeness": "partial",
            "source_is_truncated": True,
            "metadata": {
                "article_id": "7631425034263593014",
                "heading_count": 3,
                "code_block_count": 2,
                "source_truncation_reason": "historical_excerpt_only",
            },
        },
        "blogs_podcasts": {
            "title": "Building evidence-aware agents",
            "source_text": ("The public source describes a concrete architecture and its limits."),
            "capture_mode": "excerpt",
            "source_completeness": "partial",
            "source_is_truncated": False,
            "metadata": {
                "origin_url": "https://blog.example/old",
                "redirect_count": 1,
            },
        },
    }
    fixture = values[source]
    return HistoricalSourceCapture(
        source=source,
        title=str(fixture["title"]),
        external_url=external_url,
        source_text=str(fixture["source_text"]),
        captured_at=CAPTURED_AT,
        capture_mode=str(fixture["capture_mode"]),
        source_completeness=str(fixture["source_completeness"]),
        source_is_truncated=bool(fixture["source_is_truncated"]),
        metadata=dict(fixture["metadata"]),
    )


def _frontmatter(document: str) -> dict[str, object]:
    parsed = yaml.safe_load(document.split("---\n", 2)[1])
    assert isinstance(parsed, dict)
    return parsed


def _git(repo: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_repository(tmp_path: Path, *, paths: tuple[str, ...] = ("a.md",)) -> tuple[Path, Path]:
    repository = tmp_path / "repository"
    posts = repository / "blog/content/posts"
    repository.mkdir()
    _git(repository, "init", "-q")
    _git(repository, "config", "user.name", "Historical Apply Test")
    _git(repository, "config", "user.email", "historical-apply@example.com")
    for path in paths:
        _write_post(
            posts,
            path,
            source="arxiv",
            external_url="http://arxiv.org/abs/2601.00001v1",
        )
    _git(repository, "add", "-A")
    _git(repository, "commit", "-q", "-m", "historical fixtures")
    _git(repository, "switch", "-q", "-c", "codex/historical-apply-test")
    return repository, posts


def _arxiv_plan(posts: Path, paths: tuple[str, ...] = ("a.md",)):
    from ai_stack.historical_rehydration_apply import (
        build_historical_rehydration_apply_plan,
    )

    entries = [
        _entry(
            posts,
            path,
            source="arxiv",
            canonical_url="http://arxiv.org/abs/2601.00001v1",
            locator={
                "kind": "arxiv",
                "status": "resolved",
                "arxiv_id": "2601.00001v1",
            },
        )
        for path in paths
    ]
    captures = {
        path: _capture("arxiv", external_url="https://arxiv.org/abs/2601.00001v1") for path in paths
    }
    return build_historical_rehydration_apply_plan(
        _inventory(posts, entries), captures, content_root=posts
    )


def test_plan_is_pure_deterministic_and_records_input_output_sha(tmp_path: Path) -> None:
    from ai_stack.historical_rehydration_apply import (
        HISTORICAL_REHYDRATION_APPLY_PLAN_SCHEMA,
        build_historical_rehydration_apply_plan,
    )

    posts = tmp_path / "posts"
    target = _write_post(
        posts,
        "a.md",
        source="arxiv",
        external_url="http://arxiv.org/abs/2601.00001v1",
    )
    original = target.read_bytes()
    inventory = _inventory(
        posts,
        [
            _entry(
                posts,
                "a.md",
                source="arxiv",
                canonical_url="http://arxiv.org/abs/2601.00001v1",
                locator={
                    "kind": "arxiv",
                    "status": "resolved",
                    "arxiv_id": "2601.00001v1",
                },
            )
        ],
    )
    captures = {"a.md": _capture("arxiv", external_url="https://arxiv.org/abs/2601.00001v1")}

    first = build_historical_rehydration_apply_plan(inventory, captures, content_root=posts)
    second = build_historical_rehydration_apply_plan(inventory, captures, content_root=posts)

    assert target.read_bytes() == original
    assert first.manifest == second.manifest
    assert first.writes == second.writes
    assert first.manifest["schema"] == HISTORICAL_REHYDRATION_APPLY_PLAN_SCHEMA
    base_manifest = dict(first.manifest)
    plan_digest = base_manifest.pop("plan_digest")
    assert plan_digest == sha256_digest(base_manifest)
    assert first.manifest["planned_changes"] == 1
    public_write = first.manifest["writes"][0]
    operation = first.writes[0]
    assert public_write["path"] == "a.md"
    assert public_write["input_sha256"] == _sha256(original)
    assert public_write["output_sha256"] == _sha256(operation.content)
    assert operation.input_sha256 == public_write["input_sha256"]
    assert operation.output_sha256 == public_write["output_sha256"]
    rendered = operation.content.decode("utf-8")
    metadata = _frontmatter(rendered)
    assert str(metadata["date"]) == HISTORICAL_DATE
    assert metadata["aliases"] == ["/posts/stable-route/"]
    assert metadata["content_mode"] == "source_brief"
    assert metadata["publication_tier"] == "C"
    assert OLD_SECRET not in rendered
    serialized_manifest = json.dumps(first.manifest, ensure_ascii=False)
    assert "bounded official abstract" not in serialized_manifest


def test_explicit_typed_failure_plans_a_minimal_transparent_archive(tmp_path: Path) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRecoveryFailure,
        build_historical_rehydration_apply_plan,
    )

    posts = tmp_path / "posts"
    target = _write_post(
        posts,
        "failed.md",
        source="blogs_podcasts",
        external_url="https://blog.example/article",
    )
    original = target.read_bytes()
    inventory = _inventory(
        posts,
        [
            _entry(
                posts,
                "failed.md",
                source="blogs_podcasts",
                canonical_url="https://blog.example/article",
                locator={"kind": "external_url", "status": "resolved"},
            )
        ],
    )

    plan = build_historical_rehydration_apply_plan(
        inventory,
        {},
        failures={
            "failed.md": HistoricalRecoveryFailure(
                failure_type="source_fetch_error",
                reason="source_access_interstitial",
                attempted_at=CAPTURED_AT,
            )
        },
        content_root=posts,
    )

    assert target.read_bytes() == original
    rendered = plan.writes[0].content.decode("utf-8")
    metadata = _frontmatter(rendered)
    assert metadata["archived"] is True
    assert metadata["content_mode"] == "archived"
    assert metadata["publication_tier"] == "ARCHIVED"
    assert metadata["archive_reason"] == "historical_source_recovery_failed"
    assert metadata["recovery_failure_type"] == "source_fetch_error"
    assert metadata["recovery_failure_reason"] == "source_access_interstitial"
    assert metadata["recovery_attempted_at"] == CAPTURED_AT
    assert str(metadata["date"]) == HISTORICAL_DATE
    assert metadata["aliases"] == ["/posts/stable-route/"]
    assert metadata["tags"] == []
    assert metadata["categories"] == []
    assert metadata["scenarios"] == []
    assert metadata["build"] == {"list": "never", "render": "always"}
    assert "未经核验的旧标题" not in rendered
    assert "未经核验旧标签" not in rendered
    assert OLD_SECRET not in rendered
    assert "source_access_interstitial" in rendered
    assert "https://blog.example/article" in rendered

    target.write_bytes(plan.writes[0].content)
    refreshed = build_inventory_for_assertion(posts, tmp_path)
    assert refreshed["entries"][0]["recovery_classification"] == "terminal_unrecoverable"


def build_inventory_for_assertion(posts: Path, repository_root: Path) -> dict[str, object]:
    from ai_stack.historical_rehydration import build_historical_rehydration_inventory

    return build_historical_rehydration_inventory(
        posts,
        repository_root=repository_root,
        hn_git_revision="0" * 40,
    )


@pytest.mark.parametrize(
    ("source", "inventory_url", "locator", "capture"),
    (
        (
            "arxiv",
            "http://arxiv.org/abs/2601.00001v1",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00001v1"},
            _capture("arxiv", external_url="https://arxiv.org/abs/2601.00001v1"),
        ),
        (
            "github_trending",
            "https://github.com/OpenInterpreter/open-interpreter.git",
            {
                "kind": "github",
                "status": "resolved",
                "owner": "OpenInterpreter",
                "repo": "open-interpreter",
            },
            _capture(
                "github_trending",
                external_url="https://github.com/OpenInterpreter/open-interpreter",
            ),
        ),
        (
            "hacker_news",
            "https://example.com/original-story",
            {"kind": "hacker_news", "status": "resolved", "hn_id": "47158975"},
            _capture("hacker_news", external_url="https://example.com/current-story-location"),
        ),
        (
            "juejin",
            "https://juejin.cn/post/7631425034263593014",
            {
                "kind": "juejin",
                "status": "resolved",
                "article_id": "7631425034263593014",
            },
            _capture("juejin", external_url="https://juejin.cn/post/7631425034263593014"),
        ),
        (
            "blogs_podcasts",
            "https://blog.example/old",
            {"kind": "external_url", "status": "resolved"},
            _capture("blogs_podcasts", external_url="https://docs.example/new"),
        ),
        (
            "blogs_podcasts",
            "http://blog.example/old?article=1",
            {"kind": "external_url", "status": "resolved"},
            replace(
                _capture(
                    "blogs_podcasts",
                    external_url="https://blog.example/old?article=1",
                ),
                metadata={
                    "origin_url": "http://blog.example/old?article=1",
                    "redirect_count": 0,
                },
            ),
        ),
    ),
)
def test_plan_matches_capture_identity_by_source_locator(
    tmp_path: Path,
    source: str,
    inventory_url: str,
    locator: dict[str, object],
    capture: HistoricalSourceCapture,
) -> None:
    from ai_stack.historical_rehydration_apply import (
        build_historical_rehydration_apply_plan,
    )

    posts = tmp_path / "posts"
    _write_post(posts, "a.md", source=source, external_url=inventory_url)
    inventory = _inventory(
        posts,
        [
            _entry(
                posts,
                "a.md",
                source=source,
                canonical_url=inventory_url,
                locator=locator,
            )
        ],
    )

    plan = build_historical_rehydration_apply_plan(inventory, {"a.md": capture}, content_root=posts)

    assert plan.manifest["planned_changes"] == 1
    assert plan.manifest["writes"][0]["source"] == source


@pytest.mark.parametrize(
    ("mutator", "message"),
    (
        (
            lambda capture: replace(capture, source="github_trending"),
            "capture source",
        ),
        (
            lambda capture: replace(
                capture, metadata={**capture.metadata, "arxiv_id": "2601.99999v1"}
            ),
            "capture identity",
        ),
    ),
)
def test_plan_rejects_capture_source_or_locator_identity_mismatch(
    tmp_path: Path, mutator, message: str
) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRehydrationApplyError,
        build_historical_rehydration_apply_plan,
    )

    posts = tmp_path / "posts"
    _write_post(
        posts,
        "a.md",
        source="arxiv",
        external_url="http://arxiv.org/abs/2601.00001v1",
    )
    entry = _entry(
        posts,
        "a.md",
        source="arxiv",
        canonical_url="http://arxiv.org/abs/2601.00001v1",
        locator={
            "kind": "arxiv",
            "status": "resolved",
            "arxiv_id": "2601.00001v1",
        },
    )
    capture = mutator(_capture("arxiv", external_url="https://arxiv.org/abs/2601.00001v1"))

    with pytest.raises(HistoricalRehydrationApplyError, match=message):
        build_historical_rehydration_apply_plan(
            _inventory(posts, [entry]), {"a.md": capture}, content_root=posts
        )


def test_plan_rejects_blog_capture_when_origin_does_not_match_inventory(
    tmp_path: Path,
) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRehydrationApplyError,
        build_historical_rehydration_apply_plan,
    )

    posts = tmp_path / "posts"
    _write_post(
        posts,
        "a.md",
        source="blogs_podcasts",
        external_url="https://blog.example/old",
    )
    entry = _entry(
        posts,
        "a.md",
        source="blogs_podcasts",
        canonical_url="https://blog.example/old",
        locator={"kind": "external_url", "status": "resolved"},
    )
    capture = _capture("blogs_podcasts", external_url="https://docs.example/new")
    capture = replace(
        capture, metadata={**capture.metadata, "origin_url": "https://evil.example/other"}
    )

    with pytest.raises(HistoricalRehydrationApplyError, match="capture identity"):
        build_historical_rehydration_apply_plan(
            _inventory(posts, [entry]), {"a.md": capture}, content_root=posts
        )

    capture = replace(
        capture,
        metadata={
            "origin_url": "https://blog.example/old",
            "redirect_count": 0,
        },
    )
    with pytest.raises(HistoricalRehydrationApplyError, match="capture identity"):
        build_historical_rehydration_apply_plan(
            _inventory(posts, [entry]), {"a.md": capture}, content_root=posts
        )


@pytest.mark.parametrize(
    "failure",
    (
        pytest.param(
            ("unknown_failure", "source_http_404", CAPTURED_AT),
            id="unknown-type",
        ),
        pytest.param(
            ("source_fetch_error", "HTTP 404", CAPTURED_AT),
            id="unsafe-reason",
        ),
        pytest.param(
            ("source_fetch_error", "source_http_404", "2026-07-18T02:03:04"),
            id="attempt-without-timezone",
        ),
    ),
)
def test_failure_archive_requires_strict_typed_fields(
    tmp_path: Path, failure: tuple[str, str, str]
) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRecoveryFailure,
        HistoricalRehydrationApplyError,
        build_historical_rehydration_apply_plan,
    )

    posts = tmp_path / "posts"
    _write_post(
        posts,
        "a.md",
        source="blogs_podcasts",
        external_url="https://blog.example/old",
    )
    entry = _entry(
        posts,
        "a.md",
        source="blogs_podcasts",
        canonical_url="https://blog.example/old",
        locator={"kind": "external_url", "status": "resolved"},
    )
    failure_type, reason, attempted_at = failure

    with pytest.raises(HistoricalRehydrationApplyError, match="failure|timezone"):
        build_historical_rehydration_apply_plan(
            _inventory(posts, [entry]),
            {},
            failures={
                "a.md": HistoricalRecoveryFailure(
                    failure_type=failure_type,
                    reason=reason,
                    attempted_at=attempted_at,
                )
            },
            content_root=posts,
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        (lambda inventory: inventory.update(schema="wrong"), "inventory contract"),
        (
            lambda inventory: inventory.update(entries_sha256="sha256:" + "0" * 64),
            "inventory digest",
        ),
        (lambda inventory: inventory.update(entry_count=99), "inventory count"),
    ),
)
def test_plan_authenticates_inventory_contract_and_entries_digest(
    tmp_path: Path, mutation, message: str
) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRehydrationApplyError,
        build_historical_rehydration_apply_plan,
    )

    posts = tmp_path / "posts"
    _write_post(
        posts,
        "a.md",
        source="arxiv",
        external_url="http://arxiv.org/abs/2601.00001v1",
    )
    inventory = _inventory(
        posts,
        [
            _entry(
                posts,
                "a.md",
                source="arxiv",
                canonical_url="http://arxiv.org/abs/2601.00001v1",
                locator={
                    "kind": "arxiv",
                    "status": "resolved",
                    "arxiv_id": "2601.00001v1",
                },
            )
        ],
    )
    mutation(inventory)

    with pytest.raises(HistoricalRehydrationApplyError, match=message):
        build_historical_rehydration_apply_plan(
            inventory,
            {"a.md": _capture("arxiv", external_url="https://arxiv.org/abs/2601.00001v1")},
            content_root=posts,
        )


def test_plan_rejects_path_escape_symlink_and_stale_target_cas(tmp_path: Path) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRehydrationApplyError,
        build_historical_rehydration_apply_plan,
    )

    posts = tmp_path / "posts"
    target = _write_post(
        posts,
        "a.md",
        source="arxiv",
        external_url="http://arxiv.org/abs/2601.00001v1",
    )
    capture = _capture("arxiv", external_url="https://arxiv.org/abs/2601.00001v1")
    entry = _entry(
        posts,
        "a.md",
        source="arxiv",
        canonical_url="http://arxiv.org/abs/2601.00001v1",
        locator={
            "kind": "arxiv",
            "status": "resolved",
            "arxiv_id": "2601.00001v1",
        },
    )

    escaped = dict(entry)
    escaped["path"] = "../outside.md"
    escaped_inventory = _inventory(posts, [escaped])
    with pytest.raises(HistoricalRehydrationApplyError, match="path"):
        build_historical_rehydration_apply_plan(
            escaped_inventory, {"../outside.md": capture}, content_root=posts
        )

    symlink = posts / "linked.md"
    symlink.symlink_to(target)
    linked = dict(entry)
    linked["path"] = "linked.md"
    linked["target_sha256"] = _sha256(target.read_bytes())
    with pytest.raises(HistoricalRehydrationApplyError, match="symlink|unsafe"):
        build_historical_rehydration_apply_plan(
            _inventory(posts, [linked]), {"linked.md": capture}, content_root=posts
        )

    inventory = _inventory(posts, [entry])
    target.write_text(target.read_text(encoding="utf-8") + "\nmanual edit\n", encoding="utf-8")
    with pytest.raises(HistoricalRehydrationApplyError, match="target SHA|stale"):
        build_historical_rehydration_apply_plan(inventory, {"a.md": capture}, content_root=posts)


def test_apply_requires_clean_codex_branch_exact_head_plan_digest_and_bound(
    tmp_path: Path,
) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRehydrationApplyError,
        apply_historical_rehydration_plan,
    )

    repository, posts = _git_repository(tmp_path)
    plan = _arxiv_plan(posts)
    head = _git(repository, "rev-parse", "HEAD")
    backup_root = tmp_path / "backups"
    original = (posts / "a.md").read_bytes()

    attempts = (
        ({"expected_head": "0" * 40}, "HEAD mismatch"),
        ({"expected_plan_digest": "sha256:" + "0" * 64}, "plan digest"),
        ({"max_changes": 0}, "max_changes"),
    )
    base = {
        "expected_head": head,
        "expected_plan_digest": plan.manifest["plan_digest"],
        "max_changes": 1,
        "backup_id": "apply-guard",
        "backup_root": backup_root,
    }
    for override, message in attempts:
        arguments = {**base, **override}
        with pytest.raises(HistoricalRehydrationApplyError, match=message):
            apply_historical_rehydration_plan(plan, **arguments)
        assert (posts / "a.md").read_bytes() == original
        assert not backup_root.exists()

    _git(repository, "switch", "-q", "-c", "main-test")
    with pytest.raises(HistoricalRehydrationApplyError, match="codex/ branch"):
        apply_historical_rehydration_plan(plan, **base)
    _git(repository, "switch", "-q", "codex/historical-apply-test")

    (repository / "untracked.txt").write_text("dirty", encoding="utf-8")
    with pytest.raises(HistoricalRehydrationApplyError, match="clean Git worktree"):
        apply_historical_rehydration_plan(plan, **base)
    assert (posts / "a.md").read_bytes() == original
    assert not backup_root.exists()


def test_apply_backs_up_every_input_then_writes_receipt_with_item_digests(
    tmp_path: Path,
) -> None:
    from ai_stack.historical_rehydration_apply import (
        HISTORICAL_REHYDRATION_APPLY_RECEIPT_SCHEMA,
        apply_historical_rehydration_plan,
    )

    repository, posts = _git_repository(tmp_path, paths=("a.md", "b.md"))
    originals = {path: (posts / path).read_bytes() for path in ("a.md", "b.md")}
    plan = _arxiv_plan(posts, paths=("a.md", "b.md"))
    head = _git(repository, "rev-parse", "HEAD")
    backup_root = tmp_path / "backups"

    receipt = apply_historical_rehydration_plan(
        plan,
        expected_head=head,
        expected_plan_digest=plan.manifest["plan_digest"],
        max_changes=2,
        backup_id="rehydration-001",
        backup_root=backup_root,
    )

    backup = backup_root / "rehydration-001"
    assert receipt["schema"] == HISTORICAL_REHYDRATION_APPLY_RECEIPT_SCHEMA
    assert receipt["state"] == "applied"
    assert receipt["plan_digest"] == plan.manifest["plan_digest"]
    assert receipt["expected_head"] == head
    assert receipt["applied_count"] == 2
    assert receipt["items"] == plan.manifest["writes"]
    disk_receipt = json.loads((backup / "receipt.json").read_text(encoding="utf-8"))
    assert disk_receipt == receipt
    assert json.loads((backup / "plan.json").read_text(encoding="utf-8")) == plan.manifest
    for operation in plan.writes:
        assert (backup / "before" / operation.path).read_bytes() == originals[operation.path]
        assert (posts / operation.path).read_bytes() == operation.content
        assert _sha256((posts / operation.path).read_bytes()) == operation.output_sha256
    assert stat_mode(backup / "receipt.json") == 0o600


def test_apply_rejects_a_backup_root_inside_the_repository(tmp_path: Path) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRehydrationApplyError,
        apply_historical_rehydration_plan,
    )

    repository, posts = _git_repository(tmp_path)
    original = (posts / "a.md").read_bytes()
    plan = _arxiv_plan(posts)

    with pytest.raises(HistoricalRehydrationApplyError, match="outside the Git repository"):
        apply_historical_rehydration_plan(
            plan,
            expected_head=_git(repository, "rev-parse", "HEAD"),
            expected_plan_digest=plan.manifest["plan_digest"],
            max_changes=1,
            backup_id="unsafe-backup",
            backup_root=repository / "backups",
        )

    assert (posts / "a.md").read_bytes() == original
    assert not (repository / "backups").exists()


def stat_mode(path: Path) -> int:
    return os.stat(path).st_mode & 0o777


def test_apply_rolls_back_all_targets_when_one_atomic_replace_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import ai_stack.historical_rehydration_apply as apply_module

    repository, posts = _git_repository(tmp_path, paths=("a.md", "b.md"))
    originals = {path: (posts / path).read_bytes() for path in ("a.md", "b.md")}
    plan = _arxiv_plan(posts, paths=("a.md", "b.md"))
    head = _git(repository, "rev-parse", "HEAD")
    original_replace = apply_module._replace_target_atomically
    failed = False

    def fail_second(path: Path, payload: bytes, *, mode: int) -> None:
        nonlocal failed
        if path.name == "b.md" and payload == plan.writes[1].content and not failed:
            failed = True
            raise OSError("simulated target replacement failure")
        original_replace(path, payload, mode=mode)

    monkeypatch.setattr(apply_module, "_replace_target_atomically", fail_second)
    backup_root = tmp_path / "backups"

    with pytest.raises(OSError, match="simulated target replacement"):
        apply_module.apply_historical_rehydration_plan(
            plan,
            expected_head=head,
            expected_plan_digest=plan.manifest["plan_digest"],
            max_changes=2,
            backup_id="rollback-target",
            backup_root=backup_root,
        )

    assert failed is True
    assert {path: (posts / path).read_bytes() for path in originals} == originals
    assert not (backup_root / "rollback-target/receipt.json").exists()
    assert (backup_root / "rollback-target/plan.json").is_file()


def test_apply_rolls_back_when_receipt_commit_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import ai_stack.historical_rehydration_apply as apply_module

    repository, posts = _git_repository(tmp_path)
    original = (posts / "a.md").read_bytes()
    plan = _arxiv_plan(posts)
    head = _git(repository, "rev-parse", "HEAD")
    original_json_write = apply_module._write_json_atomically

    def fail_receipt(path: Path, value) -> None:
        if path.name == "receipt.json":
            raise OSError("simulated receipt failure")
        original_json_write(path, value)

    monkeypatch.setattr(apply_module, "_write_json_atomically", fail_receipt)
    backup_root = tmp_path / "backups"

    with pytest.raises(OSError, match="simulated receipt"):
        apply_module.apply_historical_rehydration_plan(
            plan,
            expected_head=head,
            expected_plan_digest=plan.manifest["plan_digest"],
            max_changes=1,
            backup_id="rollback-receipt",
            backup_root=backup_root,
        )

    assert (posts / "a.md").read_bytes() == original
    assert not (backup_root / "rollback-receipt/receipt.json").exists()


def test_apply_rejects_mutated_plan_before_git_or_backup(tmp_path: Path) -> None:
    from ai_stack.historical_rehydration_apply import (
        HistoricalRehydrationApplyError,
        apply_historical_rehydration_plan,
    )

    _repository, posts = _git_repository(tmp_path)
    plan = _arxiv_plan(posts)
    plan.manifest["planned_changes"] = 99

    with pytest.raises(HistoricalRehydrationApplyError, match="plan integrity"):
        apply_historical_rehydration_plan(
            plan,
            expected_head="0" * 40,
            expected_plan_digest=plan.manifest["plan_digest"],
            max_changes=100,
            backup_id="tampered-plan",
            backup_root=tmp_path / "backups",
        )

    assert not (tmp_path / "backups").exists()
