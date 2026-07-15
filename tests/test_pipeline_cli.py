from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from ai_stack.cli import main
from scripts.release_guard import load_release_descriptor
from scripts.release_guard import main as release_guard_main

CODE_SHA = "a" * 40
CONTENT_SHA = "b" * 40
OPS_SHA = "c" * 40


def _read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _mock_sources() -> dict[str, list[dict[str, object]]]:
    return {
        "github_trending": [
            {
                "native_id": "g5n-dev/ai-stack",
                "title": "AI Stack",
                "description": "Evidence-oriented static AI intelligence.",
                "url": "https://github.com/g5n-dev/ai-stack?utm_source=test",
                "tags": ["AI编程", " AI 编程 ", "VibeCoding", "Vibe Coding"],
            }
        ]
    }


def test_pipeline_cli_runs_a_fail_closed_static_source_brief_round_trip(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("ai_stack.pipeline._crawl_sources", lambda **_kwargs: _mock_sources())
    monkeypatch.setattr("ai_stack.pipeline._code_sha", lambda: CODE_SHA)

    discovery = tmp_path / "discovery"
    validated_discovery = tmp_path / "validated-discovery"
    content_ledger = tmp_path / "content-ledger"
    ops_ledger = tmp_path / "ops-ledger"
    generated = tmp_path / "generated"
    validated_result = tmp_path / "validated-result"
    build_handoff = tmp_path / "build-handoff"
    static_root = tmp_path / "site-static"
    receipts = tmp_path / "receipts"
    publisher_config = tmp_path / "publisher.yaml"
    publisher_config.write_text("publishers: {}\n", encoding="utf-8")

    assert main(["crawl", "--run-id", "run-100-1", "--output", str(discovery)]) == 0
    crawl_result = json.loads(capsys.readouterr().out)
    assert crawl_result["item_count"] == 1
    event_files = list((discovery / "content" / "events").glob("*.json"))
    assert len(event_files) == 1
    assert _read_json(event_files[0])["schema_version"] == "discovery_event_v1"

    assert (
        main(
            [
                "validate",
                "--kind",
                "discovery",
                "--input",
                str(discovery),
                "--output",
                str(validated_discovery),
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        main(
            [
                "process",
                "--phase",
                "persist-discovery",
                "--run-id",
                "run-100-1",
                "--input",
                str(validated_discovery),
                "--state-root",
                str(content_ledger),
            ]
        )
        == 0
    )
    persisted = json.loads(capsys.readouterr().out)
    assert persisted["changed_items"] == 1
    assert list((content_ledger / "content" / "events").glob("*.json"))

    assert (
        main(
            [
                "process",
                "--phase",
                "reserve-budget",
                "--run-id",
                "run-100-1",
                "--input",
                str(content_ledger),
                "--state-root",
                str(ops_ledger),
            ]
        )
        == 0
    )
    reservation = json.loads(capsys.readouterr().out)
    assert reservation["status"] == "RESERVED"
    assert reservation["token_limit"] <= 200_000

    assert (
        main(
            [
                "process",
                "--phase",
                "generate",
                "--run-id",
                "run-100-1",
                "--input",
                str(content_ledger),
                "--ops-root",
                str(ops_ledger),
                "--output",
                str(generated),
            ]
        )
        == 0
    )
    generation = json.loads(capsys.readouterr().out)
    assert generation == {
        "candidate_count": 1,
        "generator": "deterministic-source-brief-v1",
        "run_id": "run-100-1",
    }

    assert (
        main(
            [
                "validate",
                "--kind",
                "generated",
                "--input",
                str(generated),
                "--output",
                str(validated_result),
            ]
        )
        == 0
    )
    validation = json.loads(capsys.readouterr().out)
    assert validation["publishable"] == 1
    assert validation["quarantined"] == 0
    validated_post = next((validated_result / "content" / "posts").glob("*.md"))
    validated_frontmatter = yaml.safe_load(
        validated_post.read_text(encoding="utf-8").split("---", 2)[1]
    )
    assert validated_frontmatter["tags"] == ["AI 编程", "Vibe Coding"]

    assert (
        main(
            [
                "process",
                "--phase",
                "persist-result",
                "--run-id",
                "run-100-1",
                "--input",
                str(validated_result),
                "--state-root",
                str(content_ledger),
            ]
        )
        == 0
    )
    result_persistence = json.loads(capsys.readouterr().out)
    assert result_persistence["persisted_articles"] == 1
    post = next((content_ledger / "content" / "posts").glob("*.md"))
    assert 'publication_tier: "C"' in post.read_text(encoding="utf-8")

    assert main(["validate", "--state-root", str(content_ledger / "state")]) == 0
    assert json.loads(capsys.readouterr().out)["valid"] is True
    assert main(["validate", "--state-root", str(ops_ledger / "state")]) == 0
    assert json.loads(capsys.readouterr().out)["valid"] is True

    assert (
        main(
            [
                "render",
                "--run-id",
                "run-100-1",
                "--code-sha",
                CODE_SHA,
                "--content-sha",
                CONTENT_SHA,
                "--ops-sha",
                OPS_SHA,
                "--content-root",
                str(content_ledger),
                "--ops-root",
                str(ops_ledger),
                "--site-static-root",
                str(static_root),
                "--output",
                str(build_handoff),
            ]
        )
        == 0
    )
    release = json.loads(capsys.readouterr().out)
    basis = _read_json(build_handoff / "state" / "release-basis.json")
    assert release["release_id"] == basis["release_id"]
    assert basis["code_sha"] == CODE_SHA
    assert release["public_tree_digest"] is None
    assert not (build_handoff / "state" / "release.json").exists()
    assert (static_root / "api" / "v1" / "manifest.json").is_file()

    # Hugo/Pagefind/DOM validation runs between render and release creation.
    # The guard hashes that completed public tree, never its transport tar.
    public_root = tmp_path / "public"
    shutil.copytree(static_root / "api", public_root / "api")
    (public_root / "index.html").write_text("<h1>AI Stack</h1>\n", encoding="utf-8")
    descriptor_path = build_handoff / "state" / "release.json"
    assert (
        release_guard_main(
            [
                "create",
                "--public-root",
                str(public_root),
                "--basis",
                str(build_handoff / "state" / "release-basis.json"),
                "--output",
                str(descriptor_path),
            ]
        )
        == 0
    )
    capsys.readouterr()
    descriptor = load_release_descriptor(descriptor_path)
    assert descriptor.release_id == release["release_id"]
    assert descriptor.artifact_digest_kind == "public_tree_manifest_v2"
    assert len(descriptor.artifact_digest) == 64

    assert (
        main(
            [
                "process",
                "--phase",
                "persist-release",
                "--run-id",
                "run-100-1",
                "--input",
                str(build_handoff),
                "--state-root",
                str(ops_ledger),
                "--expected-release-id",
                descriptor.release_id,
                "--expected-code-sha",
                descriptor.code_sha,
                "--expected-content-sha",
                descriptor.content_sha,
                "--expected-artifact-digest",
                descriptor.artifact_digest,
            ]
        )
        == 0
    )
    healthy = json.loads(capsys.readouterr().out)
    assert healthy["persisted"] is True
    assert _read_json(ops_ledger / "ops/releases/current-healthy.json") == descriptor.to_dict()

    assert (
        main(
            [
                "publish",
                "--run-id",
                "run-100-1",
                "--input",
                str(build_handoff / "content" / "outbox"),
                "--output",
                str(receipts),
                "--config",
                str(publisher_config),
            ]
        )
        == 0
    )
    publish_result = json.loads(capsys.readouterr().out)
    assert publish_result["receipt_count"] == 0
    assert publish_result["status"] == "NOTIFIED"

    assert (
        main(
            [
                "process",
                "--phase",
                "persist-receipt",
                "--run-id",
                "run-100-1",
                "--input",
                str(receipts),
                "--state-root",
                str(ops_ledger),
            ]
        )
        == 0
    )
    receipt_persistence = json.loads(capsys.readouterr().out)
    assert receipt_persistence["persisted_receipts"] == 0


def test_persist_release_cli_requires_all_exact_workflow_inputs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        main(
            [
                "process",
                "--phase",
                "persist-release",
                "--run-id",
                "run-missing",
                "--input",
                str(tmp_path / "release"),
                "--state-root",
                str(tmp_path / "ops"),
            ]
        )
        == 1
    )
    assert "--expected-release-id" in capsys.readouterr().err


def test_crawl_fails_closed_when_every_source_is_empty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("ai_stack.pipeline._crawl_sources", lambda **_kwargs: {"one": []})
    output = tmp_path / "output"

    assert main(["crawl", "--run-id", "run-empty", "--output", str(output)]) == 1

    assert "no valid source items" in capsys.readouterr().err
    assert not output.exists()


def test_discovery_validator_rejects_unexpected_files_without_partial_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("ai_stack.pipeline._crawl_sources", lambda **_kwargs: _mock_sources())
    monkeypatch.setattr("ai_stack.pipeline._code_sha", lambda: CODE_SHA)
    source = tmp_path / "source"
    output = tmp_path / "output"
    assert main(["crawl", "--run-id", "run-tamper", "--output", str(source)]) == 0
    capsys.readouterr()
    (source / "content" / "unexpected.py").write_text("print('bad')", encoding="utf-8")

    assert (
        main(
            [
                "validate",
                "--kind",
                "discovery",
                "--input",
                str(source),
                "--output",
                str(output),
            ]
        )
        == 1
    )

    assert "unexpected handoff path" in capsys.readouterr().err
    assert not output.exists()


def test_generate_requires_a_persisted_budget_reservation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("ai_stack.pipeline._crawl_sources", lambda **_kwargs: _mock_sources())
    monkeypatch.setattr("ai_stack.pipeline._code_sha", lambda: CODE_SHA)
    discovery = tmp_path / "discovery"
    content_ledger = tmp_path / "content"
    assert main(["crawl", "--run-id", "run-budget", "--output", str(discovery)]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "process",
                "--phase",
                "persist-discovery",
                "--run-id",
                "run-budget",
                "--input",
                str(discovery),
                "--state-root",
                str(content_ledger),
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        main(
            [
                "process",
                "--phase",
                "generate",
                "--run-id",
                "run-budget",
                "--input",
                str(content_ledger),
                "--ops-root",
                str(tmp_path / "missing-ops"),
                "--output",
                str(tmp_path / "generated"),
            ]
        )
        == 1
    )
    assert "budget reservation" in capsys.readouterr().err


def _git_repository(path: Path) -> str:
    path.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Tests"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "tests@example.com"], cwd=path, check=True)
    (path / "posts").mkdir()
    (path / "posts" / "one.md").write_text(
        "---\ntitle: One\nexternal_url: https://example.com/one\n---\n\nBody\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "posts/one.md"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-qm", "seed"], cwd=path, check=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_seed_and_restore_migrations_are_dry_run_by_default_and_bounded(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source = tmp_path / "source"
    source_sha = _git_repository(source)
    seed_target = tmp_path / "seed-target"

    assert (
        main(
            [
                "migrate",
                "seed-content",
                str(source / "posts"),
                "--target-root",
                str(seed_target),
            ]
        )
        == 0
    )
    plan = json.loads(capsys.readouterr().out)
    assert plan["dry_run"] is True
    assert plan["planned_changes"] == 1
    assert not seed_target.exists()

    assert (
        main(
            [
                "migrate",
                "seed-content",
                str(source / "posts"),
                "--target-root",
                str(seed_target),
                "--execute",
            ]
        )
        == 2
    )
    assert "--expected-source-sha" in capsys.readouterr().err

    assert (
        main(
            [
                "migrate",
                "seed-content",
                str(source / "posts"),
                "--target-root",
                str(seed_target),
                "--execute",
                "--expected-source-sha",
                source_sha,
                "--backup-id",
                "backup-20260713",
                "--max-changes",
                "1",
            ]
        )
        == 0
    )
    executed = json.loads(capsys.readouterr().out)
    assert executed["mutation_performed"] is True
    assert (seed_target / "content" / "posts" / "one.md").is_file()

    restore_target = tmp_path / "restore-target"
    assert (
        main(
            [
                "migrate",
                "restore",
                str(seed_target / "content" / "posts"),
                "--target-root",
                str(restore_target),
                "--execute",
                "--expected-source-sha",
                source_sha,
                "--backup-id",
                "backup-20260713",
                "--max-changes",
                "1",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (restore_target / "content" / "posts" / "one.md").read_bytes() == (
        source / "posts" / "one.md"
    ).read_bytes()


def test_dedupe_migration_is_report_only_until_shadow_and_soak_gates_complete(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    posts = tmp_path / "posts"
    posts.mkdir()
    body = "---\ntitle: {title}\nexternal_url: https://example.com/same\n---\n\nBody\n"
    (posts / "one.md").write_text(body.format(title="One"), encoding="utf-8")
    (posts / "two.md").write_text(body.format(title="Two"), encoding="utf-8")

    assert main(["migrate", "dedupe", str(posts)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["dry_run"] is True
    assert report["duplicate_file_count"] == 1
    assert report["execution_blocked"] == "requires_24_shadow_runs_and_7_day_soak"


def test_legacy_generate_content_entry_can_delegate_unified_commands(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from scripts import generate_content

    received: list[str] = []

    def fake_cli(argv: list[str]) -> int:
        received.extend(argv)
        return 7

    monkeypatch.setattr("ai_stack.cli.main", fake_cli)

    assert generate_content.main(["status", "--state-root", ".state"]) == 7
    assert received == ["status", "--state-root", ".state"]
