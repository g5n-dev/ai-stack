from __future__ import annotations

import hashlib
import json
import stat
import subprocess
from pathlib import Path

import pytest
import yaml

from ai_stack._json import sha256_digest
from ai_stack.historical_capture_job import CAPTURE_AUDIT_SCHEMA, CAPTURE_AUDIT_VERSION
from ai_stack.historical_rehydration import (
    HISTORICAL_REHYDRATION_SCHEMA,
    HISTORICAL_REHYDRATION_VERSION,
)

ATTEMPTED_AT = "2026-07-18T02:03:04Z"
SECRET_EVIDENCE = "SOURCE_EVIDENCE_MUST_NEVER_REACH_STDOUT"
SOURCE_URL = "https://arxiv.org/abs/2601.00001v1"


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _document(*, source: str, external_url: str) -> str:
    metadata = {
        "title": "未经核验的旧标题",
        "date": "2026-01-02T03:04:05+08:00",
        "draft": False,
        "entry_kind": "auto",
        "tags": ["旧标签"],
        "categories": ["旧分类"],
        "scenarios": [],
        "source": source,
        "external_url": external_url,
        "content_mode": "legacy_analysis",
        "publication_tier": "LEGACY",
        "source_provenance": "legacy_no_snapshot",
        "source_support": 0.0,
    }
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    return f"---\n{frontmatter}\n---\n\n旧正文必须被替换。\n"


def _write_post(posts: Path, *, source: str = "arxiv", url: str = SOURCE_URL) -> Path:
    target = posts / "article.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_document(source=source, external_url=url), encoding="utf-8")
    return target


def _entry(
    posts: Path,
    *,
    source: str = "arxiv",
    url: str = SOURCE_URL,
) -> dict[str, object]:
    locator: dict[str, object]
    if source == "arxiv":
        locator = {
            "kind": "arxiv",
            "status": "resolved",
            "arxiv_id": "2601.00001v1",
        }
    else:
        locator = {"kind": "external_url", "status": "resolved"}
    return {
        "path": "article.md",
        "target_sha256": _sha256((posts / "article.md").read_bytes()),
        "source": source,
        "canonical_url": url,
        "current_status": "legacy_analysis",
        "current_mode": "legacy_analysis",
        "recovery_classification": "needs_source_recovery",
        "source_locator": locator,
    }


def _inventory(posts: Path, entry: dict[str, object]) -> dict[str, object]:
    entries = [entry]
    return {
        "schema": HISTORICAL_REHYDRATION_SCHEMA,
        "version": HISTORICAL_REHYDRATION_VERSION,
        "offline": True,
        "content_root": str(posts.absolute()),
        "entry_count": 1,
        "entries_sha256": sha256_digest(entries),
        "entries": entries,
    }


def _capture_result(entry: dict[str, object]) -> dict[str, object]:
    return {
        "path": entry["path"],
        "target_sha256": entry["target_sha256"],
        "source": entry["source"],
        "canonical_url": entry["canonical_url"],
        "source_locator": entry["source_locator"],
        "attempt_count": 1,
        "attempted_at": ATTEMPTED_AT,
        "status": "captured",
        "capture": {
            "source": "arxiv",
            "title": "Evidence-aware agent systems",
            "external_url": SOURCE_URL,
            "source_text": SECRET_EVIDENCE + " with a bounded official abstract.",
            "captured_at": "2026-07-18T02:02:00Z",
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
    }


def _failed_result(
    entry: dict[str, object], *, failure_type: str = "robots_disallowed"
) -> dict[str, object]:
    return {
        "path": entry["path"],
        "target_sha256": entry["target_sha256"],
        "source": entry["source"],
        "canonical_url": entry["canonical_url"],
        "source_locator": entry["source_locator"],
        "attempt_count": 2,
        "attempted_at": ATTEMPTED_AT,
        "status": "failed",
        "failure": {"type": failure_type, "reason": "robots_disallowed"},
    }


def _audit(inventory: dict[str, object], results: list[dict[str, object]]) -> dict[str, object]:
    captured_count = sum(result["status"] == "captured" for result in results)
    return {
        "schema": CAPTURE_AUDIT_SCHEMA,
        "version": CAPTURE_AUDIT_VERSION,
        "generated_at": "2026-07-18T09:09:09Z",
        "inventory_schema": inventory["schema"],
        "inventory_version": inventory["version"],
        "inventory_entries_sha256": inventory["entries_sha256"],
        "captured_count": captured_count,
        "failed_count": len(results) - captured_count,
        "results_sha256": sha256_digest(results),
        "results": results,
    }


def _write_json(path: Path, payload: object, *, mode: int = 0o600) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")
    path.chmod(mode)


def _fixture(
    tmp_path: Path,
    *,
    failed: bool = False,
) -> tuple[Path, Path, Path, dict[str, object], dict[str, object]]:
    posts = tmp_path / "posts"
    if failed:
        source = "blogs_podcasts"
        url = "https://blog.example/article"
    else:
        source = "arxiv"
        url = SOURCE_URL
    _write_post(posts, source=source, url=url)
    entry = _entry(posts, source=source, url=url)
    inventory = _inventory(posts, entry)
    result = _failed_result(entry) if failed else _capture_result(entry)
    audit = _audit(inventory, [result])
    inventory_path = tmp_path / "inventory.json"
    audit_path = tmp_path / "capture-audit.json"
    _write_json(inventory_path, inventory)
    _write_json(audit_path, audit)
    return posts, inventory_path, audit_path, inventory, audit


def _base_arguments(posts: Path, inventory: Path, audit: Path) -> list[str]:
    return [
        "--inventory",
        str(inventory),
        "--capture-audit",
        str(audit),
        "--content-root",
        str(posts),
    ]


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def test_default_is_body_free_url_free_zero_write_dry_run(tmp_path: Path, capsys) -> None:
    from scripts.apply_historical_rehydration import main

    posts, inventory, audit, _inventory_payload, _audit_payload = _fixture(tmp_path)
    before = (posts / "article.md").read_bytes()

    assert main(_base_arguments(posts, inventory, audit)) == 0

    captured = capsys.readouterr()
    summary = json.loads(captured.out)
    assert summary["dry_run"] is True
    assert summary["apply_performed"] is False
    assert summary["planned_changes"] == 1
    assert summary["outcome_counts"] == {"source_brief": 1}
    assert (posts / "article.md").read_bytes() == before
    assert SECRET_EVIDENCE not in captured.out + captured.err
    assert SOURCE_URL not in captured.out + captured.err
    assert "article.md" not in captured.out + captured.err


def test_failure_archival_is_explicit_maps_robots_and_uses_result_timestamp(
    tmp_path: Path, capsys
) -> None:
    from scripts.apply_historical_rehydration import (
        load_historical_rehydration_outcomes,
        main,
    )

    posts, inventory_path, audit_path, _inventory_payload, _audit_payload = _fixture(
        tmp_path, failed=True
    )
    arguments = _base_arguments(posts, inventory_path, audit_path)

    assert main(arguments) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["planned_changes"] == 0
    assert summary["excluded_failure_count"] == 1

    outcomes = load_historical_rehydration_outcomes(
        inventory_path,
        audit_path,
        archive_failures=True,
    )
    failure = outcomes.failures["article.md"]
    assert failure.failure_type == "source_fetch_error"
    assert failure.reason == "robots_disallowed"
    assert failure.attempted_at == ATTEMPTED_AT

    assert main([*arguments, "--archive-failures"]) == 0
    archived_summary = json.loads(capsys.readouterr().out)
    assert archived_summary["planned_changes"] == 1
    assert archived_summary["outcome_counts"] == {"terminal_unrecoverable": 1}


def test_invalid_captured_evidence_is_archived_only_with_explicit_consent(
    tmp_path: Path,
) -> None:
    from scripts.apply_historical_rehydration import (
        HistoricalRehydrationCLIError,
        load_historical_rehydration_outcomes,
    )

    _posts, inventory_path, audit_path, _inventory_payload, audit_payload = _fixture(tmp_path)
    capture = audit_payload["results"][0]["capture"]  # type: ignore[index]
    capture["source_text"] = "来源正文包含损坏字符：�"  # type: ignore[index]
    audit_payload["results_sha256"] = sha256_digest(audit_payload["results"])
    _write_json(audit_path, audit_payload)

    with pytest.raises(HistoricalRehydrationCLIError, match="capture_payload_invalid"):
        load_historical_rehydration_outcomes(
            inventory_path,
            audit_path,
            archive_failures=False,
        )

    outcomes = load_historical_rehydration_outcomes(
        inventory_path,
        audit_path,
        archive_failures=True,
    )

    assert outcomes.captures == {}
    failure = outcomes.failures["article.md"]
    assert failure.failure_type == "capture_validation_error"
    assert failure.reason == "capture_encoding_replacement_character"
    assert failure.attempted_at == ATTEMPTED_AT
    assert outcomes.captured_result_count == 1
    assert outcomes.failed_result_count == 0
    assert outcomes.excluded_failure_count == 0


def test_capture_validation_does_not_reject_excerpt_shape_that_renderer_can_wrap(
    tmp_path: Path,
) -> None:
    from scripts.apply_historical_rehydration import load_historical_rehydration_outcomes

    _posts, inventory_path, audit_path, _inventory_payload, audit_payload = _fixture(tmp_path)
    capture = audit_payload["results"][0]["capture"]  # type: ignore[index]
    capture["source_text"] = "A bounded official excerpt that naturally ends,"  # type: ignore[index]
    audit_payload["results_sha256"] = sha256_digest(audit_payload["results"])
    _write_json(audit_path, audit_payload)

    outcomes = load_historical_rehydration_outcomes(
        inventory_path,
        audit_path,
        archive_failures=False,
    )

    assert set(outcomes.captures) == {"article.md"}
    assert outcomes.failures == {}


def test_rejects_capture_audit_inventory_digest_mismatch_without_secret_logging(
    tmp_path: Path, capsys
) -> None:
    from scripts.apply_historical_rehydration import main

    posts, inventory, audit, _inventory_payload, audit_payload = _fixture(tmp_path)
    audit_payload["inventory_entries_sha256"] = "sha256:" + "0" * 64
    capture = audit_payload["results"][0]["capture"]  # type: ignore[index]
    capture["source_text"] = SECRET_EVIDENCE  # type: ignore[index]
    audit_payload["results_sha256"] = sha256_digest(audit_payload["results"])
    _write_json(audit, audit_payload)

    assert main(_base_arguments(posts, inventory, audit)) == 2
    output = capsys.readouterr()
    assert "inventory_digest_mismatch" in output.err
    assert SECRET_EVIDENCE not in output.out + output.err
    assert SOURCE_URL not in output.out + output.err


def test_rejects_non_0600_audit_symlinks_and_same_input_path(tmp_path: Path, capsys) -> None:
    from scripts.apply_historical_rehydration import main

    posts, inventory, audit, _inventory_payload, _audit_payload = _fixture(tmp_path)
    arguments = _base_arguments(posts, inventory, audit)

    audit.chmod(0o644)
    assert main(arguments) == 2
    assert "capture_audit_mode_invalid" in capsys.readouterr().err

    audit.chmod(0o600)
    linked = tmp_path / "linked-audit.json"
    linked.symlink_to(audit)
    assert main(_base_arguments(posts, inventory, linked)) == 2
    assert "input_rejected" in capsys.readouterr().err

    inventory.chmod(0o600)
    assert main(_base_arguments(posts, inventory, inventory)) == 2
    assert "input_paths_must_differ" in capsys.readouterr().err


@pytest.mark.parametrize(
    "missing_option",
    (
        "--expected-head",
        "--expected-plan-digest",
        "--max-changes",
        "--backup-id",
        "--backup-root",
    ),
)
def test_apply_requires_every_transaction_guard(
    tmp_path: Path,
    capsys,
    monkeypatch: pytest.MonkeyPatch,
    missing_option: str,
) -> None:
    import scripts.apply_historical_rehydration as cli

    posts, inventory, audit, _inventory_payload, _audit_payload = _fixture(tmp_path)
    guarded = {
        "--expected-head": "0" * 40,
        "--expected-plan-digest": "sha256:" + "0" * 64,
        "--max-changes": "1",
        "--backup-id": "reviewed-batch",
        "--backup-root": str(tmp_path / "backups"),
    }
    arguments = [*_base_arguments(posts, inventory, audit), "--apply"]
    for option, value in guarded.items():
        if option != missing_option:
            arguments.extend((option, value))
    monkeypatch.setattr(
        cli,
        "apply_historical_rehydration_plan",
        lambda *_args, **_kwargs: pytest.fail("transaction must not run"),
    )

    assert cli.main(arguments) == 2
    assert "apply_guards_incomplete" in capsys.readouterr().err


def test_real_apply_delegates_to_transaction_and_writes_0600_receipts(
    tmp_path: Path, capsys
) -> None:
    from scripts.apply_historical_rehydration import main

    repository = tmp_path / "repository"
    repository.mkdir()
    posts = repository / "blog/content/posts"
    _write_post(posts)
    _git(repository, "init", "-q")
    _git(repository, "config", "user.name", "Historical CLI Test")
    _git(repository, "config", "user.email", "historical-cli@example.com")
    _git(repository, "add", "-A")
    _git(repository, "commit", "-q", "-m", "fixture")
    _git(repository, "switch", "-q", "-c", "codex/historical-cli-test")

    entry = _entry(posts)
    inventory_payload = _inventory(posts, entry)
    audit_payload = _audit(inventory_payload, [_capture_result(entry)])
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    inventory = inputs / "inventory.json"
    audit = inputs / "capture-audit.json"
    _write_json(inventory, inventory_payload)
    _write_json(audit, audit_payload)
    base = _base_arguments(posts, inventory, audit)

    assert main(base) == 0
    dry_summary = json.loads(capsys.readouterr().out)
    plan_digest = dry_summary["plan_digest"]
    backup_root = tmp_path / "backups"
    arguments = [
        *base,
        "--apply",
        "--expected-head",
        _git(repository, "rev-parse", "HEAD"),
        "--expected-plan-digest",
        plan_digest,
        "--max-changes",
        "1",
        "--backup-id",
        "reviewed-batch",
        "--backup-root",
        str(backup_root),
    ]

    assert main(arguments) == 0

    output = capsys.readouterr()
    summary = json.loads(output.out)
    assert summary["dry_run"] is False
    assert summary["apply_performed"] is True
    assert summary["applied_count"] == 1
    assert SECRET_EVIDENCE not in output.out + output.err
    assert SOURCE_URL not in output.out + output.err
    assert stat.S_IMODE((backup_root / "reviewed-batch/receipt.json").stat().st_mode) == 0o600
    assert stat.S_IMODE((backup_root / "reviewed-batch/plan.json").stat().st_mode) == 0o600
    rendered = (posts / "article.md").read_text(encoding="utf-8")
    assert "bounded official abstract" in rendered
    assert "旧正文必须被替换" not in rendered


def test_apply_rejects_symlinked_backup_parent_before_transaction(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    import scripts.apply_historical_rehydration as cli

    posts, inventory, audit, _inventory_payload, _audit_payload = _fixture(tmp_path)
    actual = tmp_path / "actual-backups"
    actual.mkdir()
    linked_parent = tmp_path / "linked-backups"
    linked_parent.symlink_to(actual, target_is_directory=True)
    arguments = [
        *_base_arguments(posts, inventory, audit),
        "--apply",
        "--expected-head",
        "0" * 40,
        "--expected-plan-digest",
        "sha256:" + "0" * 64,
        "--max-changes",
        "1",
        "--backup-id",
        "reviewed-batch",
        "--backup-root",
        str(linked_parent / "nested"),
    ]
    monkeypatch.setattr(
        cli,
        "apply_historical_rehydration_plan",
        lambda *_args, **_kwargs: pytest.fail("transaction must not run"),
    )

    assert cli.main(arguments) == 2
    assert "backup_path_rejected" in capsys.readouterr().err


def test_apply_guard_arguments_are_rejected_without_apply_flag(tmp_path: Path, capsys) -> None:
    from scripts.apply_historical_rehydration import main

    posts, inventory, audit, _inventory_payload, _audit_payload = _fixture(tmp_path)

    assert main([*_base_arguments(posts, inventory, audit), "--max-changes", "1"]) == 2
    assert "apply_flag_required" in capsys.readouterr().err
