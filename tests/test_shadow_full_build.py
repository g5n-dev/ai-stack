from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path

import pytest

from ai_stack._json import canonical_json_bytes
from ai_stack.shadow_evidence import (
    FULL_BUILD_PROFILE,
    ShadowEvidenceError,
    append_shadow_evidence,
    evaluate_shadow_gate,
    load_shadow_evidence,
)
from scripts.shadow_compare import compare_trees
from scripts.shadow_full_build import (
    ShadowFullBuildError,
    build_shared_pagefind_report,
    main,
)

CODE_SHA = "a" * 40
CONTENT_SHA = "b" * 40
NOW = datetime(2026, 7, 13, 12, tzinfo=UTC)
PLATFORM_PACKAGE = "@pagefind/darwin-arm64"
PAGEFIND_INTEGRITY = (
    "sha512-XTUaK0hXMCu2jszWE584JGQT7y284TmMV9l/HX3rnG5uo3rHI/"
    "uHU56XTyyyPFjeWEBxECbAi0CaFDJOONtG0Q=="
)
PLATFORM_INTEGRITY = (
    "sha512-MXpI+7HsAdPkvJ0gk9xj9g541BCqBZOBbdwj9g6lB5LCj6kSV6"
    "nqDSjzcAJwvOsfu0fjwvC8hQU+ecfhp+MpiQ=="
)


def _site(root: Path, *, title: str = "same") -> None:
    root.mkdir(parents=True)
    (root / "index.html").write_text(
        f'<a href="https://source.example/item">{title}</a>\n',
        encoding="utf-8",
    )
    (root / "asset.css").write_text("body{}\n", encoding="utf-8")


def _toolchain(root: Path) -> tuple[Path, Path]:
    package_lock = root / "package-lock.json"
    package_lock.write_text(
        json.dumps(
            {
                "lockfileVersion": 3,
                "packages": {
                    "node_modules/pagefind": {
                        "version": "1.5.2",
                        "integrity": PAGEFIND_INTEGRITY,
                    },
                    f"node_modules/{PLATFORM_PACKAGE}": {
                        "version": "1.5.2",
                        "integrity": PLATFORM_INTEGRITY,
                    },
                },
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    runner = root / "pagefind-runner.cjs"
    runner.write_text("#!/usr/bin/env node\n// pinned Pagefind runner\n", encoding="utf-8")
    return package_lock, runner


def _full_build_fixture(tmp_path: Path) -> dict[str, Path]:
    hugo_baseline = tmp_path / "hugo-baseline"
    hugo_candidate = tmp_path / "hugo-candidate"
    _site(hugo_baseline)
    _site(hugo_candidate)

    pagefind_bundle = tmp_path / "pagefind-bundle"
    pagefind_bundle.mkdir()
    (pagefind_bundle / "pagefind.js").write_text("export const index = 1;\n", encoding="utf-8")
    (pagefind_bundle / "pagefind-entry.json").write_text(
        '{"version":"1.5.2"}\n', encoding="utf-8"
    )

    final_baseline = tmp_path / "final-baseline"
    final_candidate = tmp_path / "final-candidate"
    shutil.copytree(hugo_baseline, final_baseline)
    shutil.copytree(hugo_candidate, final_candidate)
    shutil.copytree(pagefind_bundle, final_baseline / "pagefind")
    shutil.copytree(pagefind_bundle, final_candidate / "pagefind")
    package_lock, pagefind_runner = _toolchain(tmp_path)
    return {
        "hugo_baseline": hugo_baseline,
        "hugo_candidate": hugo_candidate,
        "final_baseline": final_baseline,
        "final_candidate": final_candidate,
        "pagefind_bundle": pagefind_bundle,
        "package_lock": package_lock,
        "pagefind_runner": pagefind_runner,
    }


def _build(paths: dict[str, Path]):
    return build_shared_pagefind_report(
        hugo_baseline=paths["hugo_baseline"],
        hugo_candidate=paths["hugo_candidate"],
        final_baseline=paths["final_baseline"],
        final_candidate=paths["final_candidate"],
        pagefind_bundle=paths["pagefind_bundle"],
        package_lock=paths["package_lock"],
        pagefind_runner=paths["pagefind_runner"],
        platform_package=PLATFORM_PACKAGE,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
    )


def _write_legacy_full_build(root: Path, report: dict[str, object]) -> str:
    reports = root / "reports"
    records = root / "records"
    reports.mkdir(parents=True)
    records.mkdir()
    report_data = canonical_json_bytes(report) + b"\n"
    report_digest = "sha256:" + sha256(report_data).hexdigest()
    (reports / f"{report_digest.removeprefix('sha256:')}.json").write_bytes(report_data)
    record = {
        "schema_version": "shadow_migration_evidence_v1",
        "sequence": 1,
        "run_id": "legacy-full",
        "completed_at": "2026-07-13T10:00:00Z",
        "status": "SUCCEEDED",
        "full_build": True,
        "code_sha": CODE_SHA,
        "content_sha": CONTENT_SHA,
        "report_digest": report_digest,
        "previous_evidence_digest": None,
    }
    record_data = canonical_json_bytes(record) + b"\n"
    record_digest = "sha256:" + sha256(record_data).hexdigest()
    (records / f"{1:020d}-{record_digest.removeprefix('sha256:')}.json").write_bytes(
        record_data
    )
    return record_digest


def test_shared_pagefind_full_build_is_content_addressed_and_qualifies(
    tmp_path: Path,
) -> None:
    bundle = _build(_full_build_fixture(tmp_path))
    assert bundle.report["schema_version"] == "shadow_full_build_v1"
    assert bundle.report["comparison_profile"] == FULL_BUILD_PROFILE
    assert bundle.report["matches"] is True

    root = tmp_path / "evidence"
    record = append_shadow_evidence(
        root,
        report=bundle.report,
        supporting_reports=bundle.supporting_reports,
        run_id="shared-pagefind-1",
        completed_at=NOW - timedelta(hours=1),
        full_build=True,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=None,
        now=NOW,
    )

    loaded = load_shadow_evidence(root, as_of=NOW)
    gate = evaluate_shadow_gate(root, as_of=NOW, expected_content_sha=CONTENT_SHA)
    assert record.full_build_profile == FULL_BUILD_PROFILE
    assert loaded[0].full_build_profile == FULL_BUILD_PROFILE
    assert gate.full_build_count == 1
    assert len(list((root / "reports").glob("*.json"))) == 3


def test_compare_trees_still_rejects_independently_different_pagefind_bytes(
    tmp_path: Path,
) -> None:
    paths = _full_build_fixture(tmp_path)
    (paths["final_candidate"] / "pagefind/pagefind-entry.json").write_text(
        '{"version":"random-other-hash"}\n', encoding="utf-8"
    )

    report = compare_trees(paths["final_baseline"], paths["final_candidate"])
    assert report["matches"] is False
    assert report["changed_paths"] == ["pagefind/pagefind-entry.json"]


def test_non_pagefind_change_produces_failed_evidence_and_resets_gate(
    tmp_path: Path,
) -> None:
    paths = _full_build_fixture(tmp_path)
    (paths["final_candidate"] / "asset.css").write_text("tampered{}\n", encoding="utf-8")
    bundle = _build(paths)
    assert bundle.report["matches"] is False

    root = tmp_path / "evidence"
    record = append_shadow_evidence(
        root,
        report=bundle.report,
        supporting_reports=bundle.supporting_reports,
        run_id="shared-pagefind-failed",
        completed_at=NOW - timedelta(hours=1),
        full_build=True,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=None,
        now=NOW,
    )
    gate = evaluate_shadow_gate(root, as_of=NOW, expected_content_sha=CONTENT_SHA)
    assert record.status == "FAILED"
    assert gate.consecutive_successful_runs == 0
    assert gate.full_build_count == 0
    assert "latest_shadow_run_failed" in gate.reasons


@pytest.mark.parametrize(
    ("path", "value", "reason"),
    [
        (("pagefind", "strategy"), "independent_deterministic_builds", "strategy"),
        (("pagefind", "output_prefix"), "../pagefind/", "output prefix"),
        (("pagefind", "bundle_tree_sha256"), "sha256:" + "0" * 64, "contradicts"),
        (("pagefind", "tool", "version"), "latest", "version"),
    ],
)
def test_successful_composite_report_rejects_tampered_provenance(
    tmp_path: Path,
    path: tuple[str, ...],
    value: object,
    reason: str,
) -> None:
    bundle = _build(_full_build_fixture(tmp_path))
    report = json.loads(json.dumps(bundle.report))
    target = report
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value

    with pytest.raises(ShadowEvidenceError, match=reason):
        append_shadow_evidence(
            tmp_path / "evidence",
            report=report,
            supporting_reports=bundle.supporting_reports,
            run_id="tampered",
            completed_at=NOW - timedelta(hours=1),
            full_build=True,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )


def test_supporting_report_is_required_and_unknown_fields_fail_closed(tmp_path: Path) -> None:
    bundle = _build(_full_build_fixture(tmp_path))
    with pytest.raises(ShadowEvidenceError, match="supporting report"):
        append_shadow_evidence(
            tmp_path / "missing-support",
            report=bundle.report,
            run_id="missing-support",
            completed_at=NOW - timedelta(hours=1),
            full_build=True,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )

    report = dict(bundle.report)
    report["untrusted_claim"] = "pagefind is deterministic"
    with pytest.raises(ShadowEvidenceError, match="schema"):
        append_shadow_evidence(
            tmp_path / "extra-field",
            report=report,
            supporting_reports=bundle.supporting_reports,
            run_id="extra-field",
            completed_at=NOW - timedelta(hours=1),
            full_build=True,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )


def test_legacy_chain_loads_but_old_full_flag_does_not_unlock_new_gate(
    tmp_path: Path,
) -> None:
    legacy_baseline = tmp_path / "legacy/baseline"
    legacy_candidate = tmp_path / "legacy/candidate"
    _site(legacy_baseline)
    _site(legacy_candidate)
    legacy_report = compare_trees(
        legacy_baseline,
        legacy_candidate,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
    )
    root = tmp_path / "evidence"
    previous = _write_legacy_full_build(root, legacy_report)

    old = load_shadow_evidence(root, as_of=NOW)
    assert old[0].full_build is True
    assert old[0].full_build_profile is None
    assert evaluate_shadow_gate(root, as_of=NOW).full_build_count == 0

    bundle = _build(_full_build_fixture(tmp_path / "new"))
    append_shadow_evidence(
        root,
        report=bundle.report,
        supporting_reports=bundle.supporting_reports,
        run_id="new-full",
        completed_at=NOW - timedelta(hours=1),
        full_build=True,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=previous,
        now=NOW,
    )
    loaded = load_shadow_evidence(root, as_of=NOW)
    assert [record.full_build_profile for record in loaded] == [None, FULL_BUILD_PROFILE]
    assert evaluate_shadow_gate(root, as_of=NOW).full_build_count == 1


def test_new_successful_full_build_rejects_plain_v1_report(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "candidate"
    _site(baseline)
    _site(candidate)
    report = compare_trees(
        baseline,
        candidate,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
    )

    with pytest.raises(ShadowEvidenceError, match="provenance"):
        append_shadow_evidence(
            tmp_path / "evidence",
            report=report,
            run_id="plain-v1-full",
            completed_at=NOW - timedelta(hours=1),
            full_build=True,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )


def test_full_build_cli_writes_report_and_appends_chain(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    paths = _full_build_fixture(tmp_path)
    pagefind_config = tmp_path / "pagefind.yml"
    wrapper = tmp_path / "scripts/build_search.mjs"
    catalog = tmp_path / "scripts/build_search_catalog.mjs"
    pagefind_config.write_text("site: final-candidate\n", encoding="utf-8")
    wrapper.parent.mkdir()
    wrapper.write_text("// run Pagefind then compact\n", encoding="utf-8")
    catalog.write_text("// build result catalog\n", encoding="utf-8")
    report_path = tmp_path / "full-report.json"
    evidence = tmp_path / "evidence"
    args = [
        "--hugo-baseline",
        str(paths["hugo_baseline"]),
        "--hugo-candidate",
        str(paths["hugo_candidate"]),
        "--final-baseline",
        str(paths["final_baseline"]),
        "--final-candidate",
        str(paths["final_candidate"]),
        "--pagefind-bundle",
        str(paths["pagefind_bundle"]),
        "--package-lock",
        str(paths["package_lock"]),
        "--pagefind-runner",
        str(paths["pagefind_runner"]),
        "--platform-package",
        PLATFORM_PACKAGE,
        "--pagefind-command",
        "npm",
        "run",
        "build:search",
        "--command-input",
        f"pagefind_config={pagefind_config}",
        "--command-input",
        f"wrapper={wrapper}",
        "--command-input",
        f"catalog={catalog}",
        "--report",
        str(report_path),
        "--code-sha",
        CODE_SHA,
        "--content-sha",
        CONTENT_SHA,
        "--evidence-root",
        str(evidence),
        "--run-id",
        "cli-full-1",
        "--completed-at",
        "2026-07-13T08:00:00Z",
    ]

    assert main(args) == 0
    summary = json.loads(capsys.readouterr().out)
    written = json.loads(report_path.read_text(encoding="utf-8"))
    assert summary["schema_version"] == "shadow_full_build_summary_v1"
    assert summary["record_digest"].startswith("sha256:")
    assert summary["report_digest"].startswith("sha256:")
    assert written["matches"] is True
    tool = written["pagefind"]["tool"]
    assert tool["command"] == ["npm", "run", "build:search"]
    assert [item["name"] for item in tool["command_inputs"]] == [
        "catalog",
        "pagefind_config",
        "wrapper",
    ]
    assert load_shadow_evidence(evidence)[0].full_build_profile == FULL_BUILD_PROFILE


def test_expected_code_and_content_sha_each_start_a_new_consecutive_window(
    tmp_path: Path,
) -> None:
    old_code = "c" * 40
    old_content = "d" * 40
    baseline = tmp_path / "identity/baseline"
    candidate = tmp_path / "identity/candidate"
    _site(baseline)
    _site(candidate)
    old_report = compare_trees(
        baseline,
        candidate,
        code_sha=old_code,
        content_sha=old_content,
    )
    current_report = compare_trees(
        baseline,
        candidate,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
    )
    root = tmp_path / "identity-evidence"
    previous: str | None = None
    started_at = NOW - timedelta(days=8)
    for index in range(23):
        previous = append_shadow_evidence(
            root,
            report=old_report,
            run_id=f"old-identity-{index:02d}",
            completed_at=started_at + timedelta(hours=index),
            full_build=False,
            code_sha=old_code,
            content_sha=old_content,
            expected_previous_digest=previous,
            now=NOW,
        ).record_digest
    append_shadow_evidence(
        root,
        report=current_report,
        run_id="current-identity",
        completed_at=started_at + timedelta(hours=23),
        full_build=False,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=previous,
        now=NOW,
    )

    unbound = evaluate_shadow_gate(root, as_of=NOW)
    bound = evaluate_shadow_gate(
        root,
        as_of=NOW,
        expected_code_sha=CODE_SHA,
        expected_content_sha=CONTENT_SHA,
    )
    assert unbound.consecutive_successful_runs == 24
    assert bound.consecutive_successful_runs == 1
    assert "current_code_sha_mismatch" not in bound.reasons
    assert "current_content_sha_mismatch" not in bound.reasons


def test_toolchain_rejects_invalid_integrity_and_symlinked_parent_components(
    tmp_path: Path,
) -> None:
    paths = _full_build_fixture(tmp_path / "invalid-integrity")
    lock = json.loads(paths["package_lock"].read_text(encoding="utf-8"))
    lock["packages"]["node_modules/pagefind"]["integrity"] = "sha512-QUJDRA=="
    paths["package_lock"].write_text(json.dumps(lock), encoding="utf-8")
    with pytest.raises(ShadowFullBuildError, match="integrity"):
        _build(paths)

    linked_paths = _full_build_fixture(tmp_path / "linked-parent")
    tool_root = tmp_path / "linked-parent/tool-root"
    tool_root.mkdir()
    real_lock = tool_root / "package-lock.json"
    real_runner = tool_root / "pagefind-runner.cjs"
    shutil.copyfile(linked_paths["package_lock"], real_lock)
    shutil.copyfile(linked_paths["pagefind_runner"], real_runner)
    linked_tool_root = tmp_path / "linked-parent/linked-tool-root"
    linked_tool_root.symlink_to(tool_root, target_is_directory=True)
    linked_paths["package_lock"] = linked_tool_root / "package-lock.json"
    linked_paths["pagefind_runner"] = linked_tool_root / "pagefind-runner.cjs"
    with pytest.raises(ShadowFullBuildError, match="symlink"):
        _build(linked_paths)

    invalid_platform = _full_build_fixture(tmp_path / "invalid-platform")
    invalid_lock = json.loads(
        invalid_platform["package_lock"].read_text(encoding="utf-8")
    )
    invalid_lock["packages"]["node_modules/@pagefind/custom-x64"] = {
        "version": "1.5.2",
        "integrity": PLATFORM_INTEGRITY,
    }
    invalid_platform["package_lock"].write_text(
        json.dumps(invalid_lock), encoding="utf-8"
    )
    with pytest.raises(ShadowFullBuildError, match="platform package"):
        build_shared_pagefind_report(
            hugo_baseline=invalid_platform["hugo_baseline"],
            hugo_candidate=invalid_platform["hugo_candidate"],
            final_baseline=invalid_platform["final_baseline"],
            final_candidate=invalid_platform["final_candidate"],
            pagefind_bundle=invalid_platform["pagefind_bundle"],
            package_lock=invalid_platform["package_lock"],
            pagefind_runner=invalid_platform["pagefind_runner"],
            platform_package="@pagefind/custom-x64",
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
        )


def test_preexisting_pagefind_prefix_and_different_injected_bundle_fail_closed(
    tmp_path: Path,
) -> None:
    paths = _full_build_fixture(tmp_path)
    for key in ("hugo_baseline", "hugo_candidate", "final_baseline", "final_candidate"):
        existing = paths[key] / "pagefind/preexisting.js"
        existing.parent.mkdir(exist_ok=True)
        existing.write_text("preexisting\n", encoding="utf-8")
    (paths["final_candidate"] / "pagefind/pagefind.js").write_text(
        "candidate-only-random-output\n", encoding="utf-8"
    )

    bundle = _build(paths)
    assert bundle.report["matches"] is False
    pagefind = bundle.report["pagefind"]
    assert isinstance(pagefind, dict)
    assert pagefind["preexisting_output_path_count"] == 1


def test_outside_prefix_addition_cannot_collide_with_a_crafted_bundle_path(
    tmp_path: Path,
) -> None:
    paths = _full_build_fixture(tmp_path)
    crafted = paths["pagefind_bundle"] / "__outside_pagefind__/unexpected.js"
    crafted.parent.mkdir()
    crafted.write_text("same bytes\n", encoding="utf-8")
    for key in ("final_baseline", "final_candidate"):
        (paths[key] / "unexpected.js").write_text("same bytes\n", encoding="utf-8")

    bundle = _build(paths)
    assert bundle.report["matches"] is False
    pagefind = bundle.report["pagefind"]
    assert isinstance(pagefind, dict)
    for side in ("baseline_delta", "candidate_delta"):
        assert pagefind[side]["outside_prefix_path_count"] == 1


def test_support_report_tampering_is_detected_by_digest(tmp_path: Path) -> None:
    bundle = _build(_full_build_fixture(tmp_path))
    root = tmp_path / "evidence"
    append_shadow_evidence(
        root,
        report=bundle.report,
        supporting_reports=bundle.supporting_reports,
        run_id="tamper-support",
        completed_at=NOW - timedelta(hours=1),
        full_build=True,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
        expected_previous_digest=None,
        now=NOW,
    )
    hugo_digest = str(bundle.report["hugo_report_digest"]).removeprefix("sha256:")
    support_path = root / "reports" / f"{hugo_digest}.json"
    payload = json.loads(support_path.read_text(encoding="utf-8"))
    payload["file_count"] = 99
    support_path.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ShadowEvidenceError, match="digest"):
        load_shadow_evidence(root, as_of=NOW)


def test_compacted_bundle_binds_command_config_wrapper_and_catalog_inputs(
    tmp_path: Path,
) -> None:
    paths = _full_build_fixture(tmp_path)
    config = tmp_path / "pagefind.yml"
    wrapper = tmp_path / "build_search.mjs"
    catalog = tmp_path / "build_catalog.mjs"
    config.write_text("site: public\n", encoding="utf-8")
    wrapper.write_text("// pagefind then remove fragments\n", encoding="utf-8")
    catalog.write_text("// compact search result catalog\n", encoding="utf-8")
    bundle = build_shared_pagefind_report(
        hugo_baseline=paths["hugo_baseline"],
        hugo_candidate=paths["hugo_candidate"],
        final_baseline=paths["final_baseline"],
        final_candidate=paths["final_candidate"],
        pagefind_bundle=paths["pagefind_bundle"],
        package_lock=paths["package_lock"],
        pagefind_runner=paths["pagefind_runner"],
        platform_package=PLATFORM_PACKAGE,
        pagefind_command=("npm", "run", "build:search"),
        command_inputs={
            "pagefind_config": config,
            "wrapper": wrapper,
            "catalog": catalog,
        },
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
    )
    assert bundle.report["matches"] is True
    pagefind = bundle.report["pagefind"]
    assert isinstance(pagefind, dict)
    tool = pagefind["tool"]
    assert isinstance(tool, dict)
    assert tool["command"] == ["npm", "run", "build:search"]
    assert len(tool["command_inputs"]) == 3

    tampered = json.loads(json.dumps(bundle.report))
    tampered["pagefind"]["tool"]["command_inputs"][0]["sha256"] = (
        "sha256:" + "0" * 64
    )
    with pytest.raises(ShadowEvidenceError, match="command identity"):
        append_shadow_evidence(
            tmp_path / "tampered-command",
            report=tampered,
            supporting_reports=bundle.supporting_reports,
            run_id="tampered-command",
            completed_at=NOW - timedelta(hours=1),
            full_build=True,
            code_sha=CODE_SHA,
            content_sha=CONTENT_SHA,
            expected_previous_digest=None,
            now=NOW,
        )
