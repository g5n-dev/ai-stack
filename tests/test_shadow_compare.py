from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.shadow_compare as shadow
from ai_stack.shadow_evidence import load_shadow_evidence
from scripts.shadow_compare import ShadowComparisonError, compare_trees, main


def _site(root: Path, *, title: str = "same") -> None:
    (root / "posts" / "one").mkdir(parents=True)
    (root / "index.html").write_text(
        f'<a href="https://source.example/item">{title}</a>\n',
        encoding="utf-8",
    )
    (root / "posts" / "one" / "index.html").write_text(
        '<img src="//cdn.example/image.png" alt="image">\n',
        encoding="utf-8",
    )
    (root / "asset.css").write_text("body{}\n", encoding="utf-8")


def test_identical_trees_match_byte_for_byte(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate)

    report = compare_trees(baseline, candidate)

    assert report["matches"] is True
    assert report["file_count"] == 3
    assert report["html_count"] == 2
    assert report["baseline_tree_sha256"] == report["candidate_tree_sha256"]
    assert report["external_links"] == [
        "//cdn.example/image.png",
        "https://source.example/item",
    ]
    assert report["missing_paths"] == []
    assert report["extra_paths"] == []
    assert report["changed_paths"] == []


def test_reports_route_hash_and_external_link_differences(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate, title="changed")
    (candidate / "posts" / "one" / "index.html").unlink()
    (candidate / "new.html").write_text(
        '<a href="https://different.example/">new</a>',
        encoding="utf-8",
    )

    report = compare_trees(baseline, candidate)

    assert report["matches"] is False
    assert report["missing_paths"] == ["posts/one/index.html"]
    assert report["extra_paths"] == ["new.html"]
    assert report["changed_paths"] == ["index.html"]
    assert report["external_links_match"] is False
    assert report["baseline_html_count"] == 2
    assert report["candidate_html_count"] == 2


def test_rejects_symlinks_and_non_directories(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate)
    (candidate / "linked.html").symlink_to(candidate / "index.html")

    with pytest.raises(ShadowComparisonError, match="symlink"):
        compare_trees(baseline, candidate)
    with pytest.raises(ShadowComparisonError, match="regular directory"):
        compare_trees(baseline / "index.html", baseline)


def test_cli_writes_canonical_report_and_returns_two_for_mismatch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate, title="changed")
    output = tmp_path / "report.json"

    assert (
        main(
            [
                "--baseline",
                str(baseline),
                "--candidate",
                str(candidate),
                "--report",
                str(output),
                "--code-sha",
                "a" * 40,
                "--content-sha",
                "b" * 40,
            ]
        )
        == 2
    )
    written = json.loads(output.read_text(encoding="utf-8"))
    printed = json.loads(capsys.readouterr().out)
    assert written["matches"] is False
    assert written["code_sha"] == "a" * 40
    assert written["content_sha"] == "b" * 40
    assert printed["schema_version"] == "shadow_compare_summary_v1"
    assert printed["matches"] is False
    assert printed["changed_paths"] == ["index.html"]
    assert printed["record_digest"] is None
    assert "external_links" not in printed


def test_cli_fails_closed_without_writing_report(tmp_path: Path) -> None:
    output = tmp_path / "report.json"

    assert (
        main(
            [
                "--baseline",
                str(tmp_path / "missing"),
                "--candidate",
                str(tmp_path / "also-missing"),
                "--report",
                str(output),
            ]
        )
        == 1
    )
    assert not output.exists()


def test_plain_compare_cli_cannot_claim_a_provenance_full_build(
    tmp_path: Path,
) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate)
    output = tmp_path / "report.json"
    evidence = tmp_path / "ops/shadow"

    assert (
        main(
            [
                "--baseline",
                str(baseline),
                "--candidate",
                str(candidate),
                "--report",
                str(output),
                "--code-sha",
                "a" * 40,
                "--content-sha",
                "b" * 40,
                "--evidence-root",
                str(evidence),
                "--run-id",
                "shadow-build-1",
                "--completed-at",
                "2026-07-13T08:00:00Z",
                "--full-build",
            ]
        )
        == 1
    )
    assert json.loads(output.read_text(encoding="utf-8"))["matches"] is True
    assert load_shadow_evidence(evidence) == ()


def test_cli_records_a_failed_full_build_before_returning_mismatch(
    tmp_path: Path,
) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate, title="changed")
    evidence = tmp_path / "ops/shadow"

    assert (
        main(
            [
                "--baseline",
                str(baseline),
                "--candidate",
                str(candidate),
                "--report",
                str(tmp_path / "report.json"),
                "--code-sha",
                "a" * 40,
                "--content-sha",
                "b" * 40,
                "--evidence-root",
                str(evidence),
                "--run-id",
                "failed-full-build",
                "--completed-at",
                "2026-07-13T08:00:00Z",
                "--full-build",
            ]
        )
        == 2
    )
    records = load_shadow_evidence(evidence)
    assert len(records) == 1
    assert records[0].status == "FAILED"
    assert records[0].full_build is True


def test_cli_requires_complete_evidence_identity_and_rejects_replay(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate)
    evidence = tmp_path / "ops/shadow"
    common = [
        "--baseline",
        str(baseline),
        "--candidate",
        str(candidate),
        "--report",
        str(tmp_path / "report.json"),
        "--code-sha",
        "a" * 40,
        "--content-sha",
        "b" * 40,
        "--evidence-root",
        str(evidence),
        "--run-id",
        "shadow-build-1",
        "--completed-at",
        "2026-07-13T08:00:00Z",
    ]
    assert main(common) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["schema_version"] == "shadow_compare_summary_v1"
    assert summary["record_digest"].startswith("sha256:")
    assert summary["report_digest"].startswith("sha256:")
    records = load_shadow_evidence(evidence)
    assert summary["record_digest"] == records[0].record_digest
    assert summary["report_digest"] == records[0].report_digest
    assert main(common) == 1

    incomplete = common.copy()
    del incomplete[incomplete.index("--run-id") : incomplete.index("--run-id") + 2]
    incomplete[incomplete.index("--evidence-root") + 1] = str(tmp_path / "other")
    assert main(incomplete) == 1


def test_rejects_invalid_identity_non_utf8_html_and_hardlinks(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate)
    with pytest.raises(ShadowComparisonError, match="code_sha"):
        compare_trees(baseline, candidate, code_sha="main")

    (candidate / "index.html").write_bytes(b"\xff")
    with pytest.raises(ShadowComparisonError, match="not UTF-8"):
        compare_trees(baseline, candidate)

    (candidate / "index.html").write_text("safe", encoding="utf-8")
    (candidate / "hardlink.css").hardlink_to(candidate / "asset.css")
    with pytest.raises(ShadowComparisonError, match="non-regular file"):
        compare_trees(baseline, candidate)


@pytest.mark.parametrize(
    ("constant", "value", "reason"),
    [
        ("_MAX_FILE_BYTES", 1, "file exceeds"),
        ("_MAX_FILES", 0, "file-count"),
        ("_MAX_TOTAL_BYTES", 1, "total-size"),
    ],
)
def test_enforces_bounded_tree_limits(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    constant: str,
    value: int,
    reason: str,
) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate)
    monkeypatch.setattr(shadow, constant, value)

    with pytest.raises(ShadowComparisonError, match=reason):
        compare_trees(baseline, candidate)


def test_cli_stdout_is_bounded_while_report_keeps_complete_external_links(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    baseline.mkdir()
    candidate.mkdir()
    links = "".join(
        f'<a href="https://source.example/items/{index}">item</a>'
        for index in range(2_000)
    )
    (baseline / "index.html").write_text(links, encoding="utf-8")
    (candidate / "index.html").write_text(links, encoding="utf-8")
    output = tmp_path / "report.json"

    assert (
        main(
            [
                "--baseline",
                str(baseline),
                "--candidate",
                str(candidate),
                "--report",
                str(output),
                "--code-sha",
                "a" * 40,
                "--content-sha",
                "b" * 40,
            ]
        )
        == 0
    )
    stdout = capsys.readouterr().out
    summary = json.loads(stdout)
    report = json.loads(output.read_text(encoding="utf-8"))
    assert len(report["external_links"]) == 2_000
    assert summary["external_link_count"] == 2_000
    assert "external_links" not in summary
    assert len(stdout.encode("utf-8")) < 16_000
