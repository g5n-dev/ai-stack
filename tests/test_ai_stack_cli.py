from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from ai_stack.cli import main
from ai_stack.models import RunManifest, StepResult, StepStatus, WorkflowStatus
from ai_stack.stores import FileContentStore

NOW = datetime(2026, 7, 13, tzinfo=UTC)


def write_post(path: Path, external_url: str | None, *, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    url_line = f'external_url: "{external_url}"\n' if external_url else ""
    path.write_text(
        f"---\ntitle: \"{title}\"\n{url_line}---\n\nBody\n",
        encoding="utf-8",
    )


def test_inventory_defaults_to_dry_run_and_reports_exact_url_duplicates(
    tmp_path: Path, capsys
) -> None:
    content = tmp_path / "posts"
    write_post(content / "one.md", "HTTPS://Example.com/a?utm_source=x", title="One")
    write_post(content / "two.md", "https://example.com/a", title="Two")
    write_post(content / "three.md", "https://example.com/b", title="Three")
    write_post(content / "missing.md", None, title="Missing")
    before = {path: path.read_bytes() for path in content.rglob("*.md")}

    exit_code = main(["migrate", "inventory", str(content)])
    report = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert report["dry_run"] is True
    assert report["files_scanned"] == 4
    assert report["unique_external_urls"] == 2
    assert report["duplicate_file_count"] == 1
    assert report["missing_external_url"] == 1
    assert len(report["duplicate_groups"]) == 1
    assert {path: path.read_bytes() for path in content.rglob("*.md")} == before


def test_inventory_skips_symlinks_and_can_atomically_write_report(
    tmp_path: Path, capsys
) -> None:
    content = tmp_path / "posts"
    write_post(content / "real.md", "https://example.com/real", title="Real")
    outside = tmp_path / "outside.md"
    write_post(outside, "https://example.com/outside", title="Outside")
    (content / "linked.md").symlink_to(outside)
    outside_directory = tmp_path / "outside-directory"
    write_post(
        outside_directory / "hidden.md",
        "https://example.com/hidden",
        title="Hidden",
    )
    (content / "linked-directory").symlink_to(
        outside_directory, target_is_directory=True
    )
    output = tmp_path / "reports" / "inventory.json"

    exit_code = main(
        ["migrate", "inventory", str(content), "--output", str(output)]
    )
    stdout_report = json.loads(capsys.readouterr().out)
    file_report = json.loads(output.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert stdout_report == file_report
    assert file_report["files_scanned"] == 1
    assert file_report["symlinks_skipped"] == 2
    assert not list(output.parent.glob("*.tmp"))


def test_inventory_rejects_symlink_root_and_reports_invalid_urls(
    tmp_path: Path, capsys
) -> None:
    content = tmp_path / "posts"
    write_post(content / "invalid.md", "javascript:alert(1)", title="Invalid")
    (content / "plain.md").write_text("No frontmatter\n", encoding="utf-8")

    assert main(["migrate", "inventory", str(content)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert len(report["invalid_external_urls"]) == 1
    assert report["missing_external_url"] == 1

    linked_root = tmp_path / "linked-root"
    linked_root.symlink_to(content, target_is_directory=True)
    assert main(["migrate", "inventory", str(linked_root)]) == 1
    assert "symlink" in capsys.readouterr().err


def test_inventory_execute_requires_all_safety_gates(tmp_path: Path, capsys) -> None:
    content = tmp_path / "posts"
    content.mkdir()

    exit_code = main(["migrate", "inventory", str(content), "--execute"])

    assert exit_code == 2
    assert "--expected-source-sha" in capsys.readouterr().err


def test_inventory_execute_validates_bounds_and_source_sha(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    content = tmp_path / "posts"
    content.mkdir()

    assert (
        main(
            [
                "migrate",
                "inventory",
                str(content),
                "--execute",
                "--expected-source-sha",
                "abc",
                "--backup-id",
                "backup-1",
                "--max-changes",
                "0",
            ]
        )
        == 2
    )
    assert "greater than zero" in capsys.readouterr().err

    monkeypatch.setattr("ai_stack.cli._git_head", lambda path: "different")
    assert (
        main(
            [
                "migrate",
                "inventory",
                str(content),
                "--execute",
                "--expected-source-sha",
                "abc",
                "--backup-id",
                "backup-1",
                "--max-changes",
                "1",
            ]
        )
        == 3
    )
    assert "source SHA mismatch" in capsys.readouterr().err


def test_inventory_execute_with_all_gates_remains_non_mutating(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    content = tmp_path / "posts"
    write_post(content / "one.md", "https://example.com/one", title="One")
    before = (content / "one.md").read_bytes()
    monkeypatch.setattr("ai_stack.cli._git_head", lambda path: "abc")

    exit_code = main(
        [
            "migrate",
            "inventory",
            str(content),
            "--execute",
            "--expected-source-sha",
            "abc",
            "--backup-id",
            "backup-1",
            "--max-changes",
            "1",
        ]
    )
    report = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert report["dry_run"] is False
    assert report["mutation_performed"] is False
    assert report["safety_gate"]["backup_id"] == "backup-1"
    assert (content / "one.md").read_bytes() == before


def test_cli_absent_state_and_errors_are_reported(tmp_path: Path, capsys) -> None:
    state = tmp_path / "missing-state"
    assert main(["status", "--state-root", str(state)]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["content"]["present"] is False

    assert main(["validate", "--state-root", str(state)]) == 0
    validation = json.loads(capsys.readouterr().out)
    assert validation["valid"] is True

    assert (
        main(
            ["resume", "--state-root", str(state), "--run-id", "missing"]
        )
        == 1
    )
    assert "does not exist" in capsys.readouterr().err

    assert main(["migrate", "inventory", str(tmp_path / "absent")]) == 1
    assert "not a directory" in capsys.readouterr().err


def test_status_validate_and_resume_are_read_only(tmp_path: Path, capsys) -> None:
    state = tmp_path / "state"
    store = FileContentStore(state / "content")
    run = RunManifest(
        run_id="run-resume",
        code_sha="a" * 40,
        content_parent_sha="b" * 40,
        input_digest="sha256:" + "1" * 64,
        config_digest="sha256:" + "2" * 64,
        model="model-x",
        status=WorkflowStatus.GENERATED,
        steps=(
            StepResult(
                step="discover",
                status=StepStatus.SUCCEEDED,
                started_at=NOW,
                finished_at=NOW,
            ),
        ),
        created_at=NOW,
        updated_at=NOW,
    )
    store.put_run(run, expected_base=store.base_revision())
    head_before = (state / "content" / "HEAD.json").read_bytes()

    assert main(["status", "--state-root", str(state)]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["content"]["record_counts"] == {"runs": 1}

    assert main(["validate", "--state-root", str(state)]) == 0
    validation = json.loads(capsys.readouterr().out)
    assert validation["valid"] is True

    assert (
        main(
            [
                "resume",
                "--state-root",
                str(state),
                "--run-id",
                "run-resume",
            ]
        )
        == 0
    )
    resume = json.loads(capsys.readouterr().out)
    assert resume["run_id"] == "run-resume"
    assert resume["next_step"] == "generate"
    assert (state / "content" / "HEAD.json").read_bytes() == head_before

    assert (
        main(
            [
                "resume",
                "--state-root",
                str(state),
                "--run-id",
                "missing",
            ]
        )
        == 1
    )
    assert "run not found" in capsys.readouterr().err
