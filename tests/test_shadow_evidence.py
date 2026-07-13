from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path

import pytest

from ai_stack.cli import main as cli_main
from ai_stack.shadow_evidence import (
    ShadowEvidenceError,
    append_shadow_evidence,
    evaluate_shadow_gate,
    load_shadow_evidence,
)
from scripts.shadow_compare import compare_trees

CODE_SHA = "a" * 40
CONTENT_SHA = "b" * 40
NOW = datetime(2026, 7, 13, 12, tzinfo=UTC)


def _site(root: Path, *, text: str = "same") -> None:
    root.mkdir(parents=True)
    (root / "index.html").write_text(
        f'<a href="https://source.example/item">{text}</a>\n',
        encoding="utf-8",
    )


def _report(tmp_path: Path, name: str, *, matches: bool = True) -> dict[str, object]:
    baseline = tmp_path / name / "baseline"
    candidate = tmp_path / name / "candidate"
    _site(baseline)
    _site(candidate, text="same" if matches else "changed")
    return compare_trees(
        baseline,
        candidate,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
    )


def _append_successful_window(
    root: Path,
    report: dict[str, object],
    *,
    now: datetime = NOW,
    content_sha: str = CONTENT_SHA,
) -> str:
    previous: str | None = None
    started_at = now - timedelta(days=8)
    for index in range(24):
        previous = append_shadow_evidence(
            root,
            report=report,
            run_id=f"shadow-{index + 1:02d}",
            completed_at=started_at + timedelta(hours=index * 6),
            full_build=index in {0, 8, 16},
            code_sha=CODE_SHA,
            content_sha=content_sha,
            expected_previous_digest=previous,
            now=now,
        ).record_digest
    assert previous is not None
    return previous


def test_content_addressed_chain_unlocks_only_after_all_three_thresholds(
    tmp_path: Path,
) -> None:
    root = tmp_path / "evidence"
    report = _report(tmp_path, "match")
    head = _append_successful_window(root, report)

    records = load_shadow_evidence(root, as_of=NOW)
    gate = evaluate_shadow_gate(root, as_of=NOW, expected_content_sha=CONTENT_SHA)

    assert len(records) == 24
    assert records[-1].record_digest == head
    assert gate.ready is True
    assert gate.consecutive_successful_runs == 24
    assert gate.full_build_count == 3
    assert gate.soak_seconds >= 7 * 24 * 60 * 60
    assert gate.head_digest == head
    assert gate.reasons == ()

    report_files = list((root / "reports").glob("*.json"))
    record_files = sorted((root / "records").glob("*.json"))
    assert len(report_files) == 1
    assert len(record_files) == 24
    assert report_files[0].stem == records[0].report_digest.removeprefix("sha256:")
    assert record_files[-1].stem.endswith(head.removeprefix("sha256:"))


def test_duplicate_run_order_future_and_chain_forgery_are_rejected(tmp_path: Path) -> None:
    root = tmp_path / "evidence"
    report = _report(tmp_path, "match")
    completed = NOW - timedelta(days=1)
    first = append_shadow_evidence(
        root,
        report=report,
        run_id="shadow-1",
        completed_at=completed,
        full_build=True,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=None,
        now=NOW,
    )

    with pytest.raises(ShadowEvidenceError, match="duplicate run_id"):
        append_shadow_evidence(
            root,
            report=report,
            run_id="shadow-1",
            completed_at=completed + timedelta(hours=1),
            full_build=False,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=first.record_digest,
            now=NOW,
        )
    with pytest.raises(ShadowEvidenceError, match="strictly later"):
        append_shadow_evidence(
            root,
            report=report,
            run_id="shadow-2",
            completed_at=completed,
            full_build=False,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=first.record_digest,
            now=NOW,
        )
    with pytest.raises(ShadowEvidenceError, match="future"):
        append_shadow_evidence(
            root,
            report=report,
            run_id="shadow-2",
            completed_at=NOW + timedelta(seconds=1),
            full_build=False,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=first.record_digest,
            now=NOW,
        )
    with pytest.raises(ShadowEvidenceError, match="previous evidence digest"):
        append_shadow_evidence(
            root,
            report=report,
            run_id="shadow-2",
            completed_at=completed + timedelta(hours=1),
            full_build=False,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest="sha256:" + "f" * 64,
            now=NOW,
        )


def test_failure_resets_window_and_report_sha_binding_is_fail_closed(tmp_path: Path) -> None:
    root = tmp_path / "evidence"
    good = _report(tmp_path, "match")
    failed = _report(tmp_path, "mismatch", matches=False)
    previous = append_shadow_evidence(
        root,
        report=good,
        run_id="shadow-1",
        completed_at=NOW - timedelta(days=8),
        full_build=True,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=None,
        now=NOW,
    ).record_digest
    previous = append_shadow_evidence(
        root,
        report=failed,
        run_id="shadow-2",
        completed_at=NOW - timedelta(days=7),
        full_build=False,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=previous,
        now=NOW,
    ).record_digest
    append_shadow_evidence(
        root,
        report=good,
        run_id="shadow-3",
        completed_at=NOW - timedelta(days=6),
        full_build=True,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=previous,
        now=NOW,
    )

    gate = evaluate_shadow_gate(root, as_of=NOW, expected_content_sha=CONTENT_SHA)
    assert gate.ready is False
    assert gate.consecutive_successful_runs == 1
    assert "requires_24_consecutive_successful_runs" in gate.reasons
    assert "requires_3_full_shadow_builds" in gate.reasons
    assert "requires_7_day_soak" in gate.reasons

    with pytest.raises(ShadowEvidenceError, match="code_sha"):
        append_shadow_evidence(
            tmp_path / "wrong-sha",
            report=good,
            run_id="shadow-wrong",
            completed_at=NOW - timedelta(hours=1),
            full_build=False,
            code_sha="c" * 40,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )


def test_tampering_gaps_and_current_content_mismatch_are_rejected(tmp_path: Path) -> None:
    root = tmp_path / "evidence"
    report = _report(tmp_path, "match")
    _append_successful_window(root, report)

    gate = evaluate_shadow_gate(root, as_of=NOW, expected_content_sha="c" * 40)
    assert gate.ready is False
    assert "current_content_sha_mismatch" in gate.reasons

    first_report = next((root / "reports").glob("*.json"))
    payload = json.loads(first_report.read_text(encoding="utf-8"))
    payload["file_count"] = 999
    first_report.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ShadowEvidenceError, match="digest"):
        load_shadow_evidence(root, as_of=NOW)

    clean = tmp_path / "clean"
    _append_successful_window(clean, report)
    second = sorted((clean / "records").glob("*.json"))[1]
    second.rename(second.with_name("00000000000000000025-" + second.name.split("-", 1)[1]))
    with pytest.raises(ShadowEvidenceError, match="sequence"):
        load_shadow_evidence(clean, as_of=NOW)


def test_failed_full_build_is_recorded_and_resets_the_gate(tmp_path: Path) -> None:
    failed = _report(tmp_path, "mismatch", matches=False)
    root = tmp_path / "evidence"
    record = append_shadow_evidence(
        root,
        report=failed,
        run_id="failed-full",
        completed_at=NOW - timedelta(hours=1),
        full_build=True,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=None,
        now=NOW,
    )

    gate = evaluate_shadow_gate(root, as_of=NOW, expected_content_sha=CONTENT_SHA)
    assert record.status == "FAILED"
    assert record.full_build is True
    assert gate.consecutive_successful_runs == 0
    assert gate.full_build_count == 0
    assert "latest_shadow_run_failed" in gate.reasons


def test_successful_full_build_requires_a_nonempty_html_comparison(tmp_path: Path) -> None:
    baseline = tmp_path / "empty/baseline"
    candidate = tmp_path / "empty/candidate"
    baseline.mkdir(parents=True)
    candidate.mkdir(parents=True)
    empty = compare_trees(
        baseline,
        candidate,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
    )

    with pytest.raises(ShadowEvidenceError, match="full build"):
        append_shadow_evidence(
            tmp_path / "empty-evidence",
            report=empty,
            run_id="empty-full",
            completed_at=NOW - timedelta(hours=1),
            full_build=True,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )


def test_symlinks_hardlinks_and_rehashed_fake_predecessors_fail_closed(
    tmp_path: Path,
) -> None:
    report = _report(tmp_path, "match")
    root = tmp_path / "evidence"
    append_shadow_evidence(
        root,
        report=report,
        run_id="shadow-1",
        completed_at=NOW - timedelta(hours=1),
        full_build=False,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=None,
        now=NOW,
    )

    linked_root = tmp_path / "linked-evidence"
    linked_root.symlink_to(root, target_is_directory=True)
    with pytest.raises(ShadowEvidenceError, match="symlink"):
        load_shadow_evidence(linked_root, as_of=NOW)

    report_path = next((root / "reports").glob("*.json"))
    linked_report = report_path.with_name("f" * 64 + ".json")
    linked_report.hardlink_to(report_path)
    with pytest.raises(ShadowEvidenceError, match="unsafe"):
        load_shadow_evidence(root, as_of=NOW)
    linked_report.unlink()

    record_path = next((root / "records").glob("*.json"))
    value = json.loads(record_path.read_text(encoding="utf-8"))
    value["previous_evidence_digest"] = "sha256:" + "e" * 64
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    forged = record_path.with_name(f"{1:020d}-{sha256(data).hexdigest()}.json")
    record_path.unlink()
    forged.write_bytes(data)
    with pytest.raises(ShadowEvidenceError, match="previous digest"):
        load_shadow_evidence(root, as_of=NOW)


def test_gate_binds_optional_code_sha_and_rejects_noncanonical_inputs(
    tmp_path: Path,
) -> None:
    report = _report(tmp_path, "match")
    root = tmp_path / "evidence"
    append_shadow_evidence(
        root,
        report=report,
        run_id="shadow-1",
        completed_at=NOW - timedelta(hours=1),
        full_build=False,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=None,
        now=NOW,
    )
    gate = evaluate_shadow_gate(root, as_of=NOW, expected_code_sha="c" * 40)
    assert "current_code_sha_mismatch" in gate.reasons

    with pytest.raises(ShadowEvidenceError, match="timezone"):
        append_shadow_evidence(
            tmp_path / "naive",
            report=report,
            run_id="shadow-naive",
            completed_at=datetime(2026, 7, 13, 8),
            full_build=False,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )
    contradicted = dict(report)
    contradicted["changed_path_count"] = 1
    with pytest.raises(ShadowEvidenceError, match="contradicts"):
        append_shadow_evidence(
            tmp_path / "contradicted",
            report=contradicted,
            run_id="shadow-contradicted",
            completed_at=NOW - timedelta(hours=1),
            full_build=False,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )


def test_dedupe_execute_requires_gate_caps_batch_and_still_performs_no_mutation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    body = "---\ntitle: {title}\nexternal_url: https://example.com/same\n---\n\nBody\n"
    (posts / "one.md").write_text(body.format(title="One"), encoding="utf-8")
    (posts / "two.md").write_text(body.format(title="Two"), encoding="utf-8")
    (content / "seed-manifest.json").write_text(
        json.dumps({"expected_source_sha": CONTENT_SHA}), encoding="utf-8"
    )
    evidence = tmp_path / "ops/shadow"
    report = _report(tmp_path, "dedupe-match")
    checked_at = datetime.now(UTC)
    _append_successful_window(evidence, report, now=checked_at)
    original = {path.name: path.read_bytes() for path in posts.iterdir()}

    common = [
        "migrate",
        "dedupe",
        str(posts),
        "--execute",
        "--expected-source-sha",
        CONTENT_SHA,
        "--backup-id",
        "content-seed-a97135c9",
        "--shadow-evidence-root",
        str(evidence),
    ]
    assert cli_main([*common, "--max-changes", "101"]) == 2
    assert "between 1 and 100" in capsys.readouterr().err

    assert cli_main([*common, "--max-changes", "100"]) == 2
    assert "mutation engine is not implemented" in capsys.readouterr().err
    assert {path.name: path.read_bytes() for path in posts.iterdir()} == original


def test_dedupe_dry_run_reports_verified_gate_without_unlocking_mutation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "one.md").write_text(
        "---\ntitle: One\nexternal_url: https://example.com/one\n---\n",
        encoding="utf-8",
    )
    evidence = tmp_path / "ops/shadow"
    report = _report(tmp_path, "plan-match")
    _append_successful_window(evidence, report, now=datetime.now(UTC))

    assert (
        cli_main(
            [
                "migrate",
                "dedupe",
                str(posts),
                "--shadow-evidence-root",
                str(evidence),
                "--expected-source-sha",
                CONTENT_SHA,
            ]
        )
        == 0
    )
    plan = json.loads(capsys.readouterr().out)
    assert plan["shadow_gate"]["ready"] is True
    assert plan["execution_blocked"] == "dedupe_mutation_not_implemented"
    assert plan["mutation_performed"] is False
