"""Attest an exact Hugo migration plus one shared Pagefind 1.5.2 bundle.

This command does not claim that two independent Pagefind runs are
deterministic. It verifies that both byte-identical Hugo trees received the
same content-addressed, add-only ``pagefind/`` subtree and then compares the
two complete final trees without exclusions.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import re
import stat
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from ai_stack._json import canonical_json_bytes
from ai_stack.shadow_evidence import (
    FULL_BUILD_PROFILE,
    FULL_BUILD_REPORT_SCHEMA,
    PAGEFIND_STRATEGY,
    ShadowEvidenceError,
    append_shadow_evidence,
)
from scripts.shadow_compare import (
    ShadowComparisonError,
    _atomic_json,
    _evidence_time,
    _inspect_tree,
    _Tree,
    compare_trees,
)

_PAGEFIND_VERSION = "1.5.2"
_OUTPUT_PREFIX = "pagefind/"
_MAX_TOOL_FILE_BYTES = 32 * 1024 * 1024
_COMMAND_INPUT_NAME = re.compile(r"[a-z][a-z0-9_.-]{0,63}\Z")
_PAGEFIND_PLATFORM = re.compile(
    r"@pagefind/(?:darwin|freebsd|linux|windows)-(?:arm64|x64)\Z"
)
_DEFAULT_PAGEFIND_COMMAND = ("pagefind", "--site", "COMMON_HUGO_TREE")


class ShadowFullBuildError(RuntimeError):
    """Raised when Pagefind provenance cannot be safely constructed."""


@dataclass(frozen=True, slots=True)
class ShadowFullBuildBundle:
    report: dict[str, object]
    supporting_reports: tuple[dict[str, object], dict[str, object]]


def _check_path_components(path: Path | str, field: str) -> None:
    absolute = Path(path).absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            raise ShadowFullBuildError(f"{field} crosses a symlink: {current}")


def _read_regular_file(path: Path | str, field: str) -> bytes:
    source = Path(path).absolute()
    _check_path_components(source, field)
    try:
        details = source.lstat()
    except OSError as exc:
        raise ShadowFullBuildError(f"{field} is unreadable: {source}") from exc
    if source.is_symlink() or not stat.S_ISREG(details.st_mode) or details.st_nlink != 1:
        raise ShadowFullBuildError(f"{field} must be a regular, non-linked file")
    if details.st_size > _MAX_TOOL_FILE_BYTES:
        raise ShadowFullBuildError(f"{field} exceeds the size limit")
    descriptor = os.open(source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
            raise ShadowFullBuildError(f"{field} must be a regular, non-linked file")
        if opened.st_size > _MAX_TOOL_FILE_BYTES:
            raise ShadowFullBuildError(f"{field} exceeds the size limit")
        with os.fdopen(descriptor, "rb") as stream:
            payload = stream.read()
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise
    if len(payload) != opened.st_size:
        raise ShadowFullBuildError(f"{field} changed while reading")
    return payload


def _digest_bytes(payload: bytes) -> str:
    return "sha256:" + sha256(payload).hexdigest()


def _report_digest(report: Mapping[str, Any]) -> str:
    return _digest_bytes(canonical_json_bytes(report) + b"\n")


def _tree_digest(files: Mapping[str, tuple[int, str]]) -> str:
    manifest = {
        "schema_version": "shadow_tree_v1",
        "files": [
            {"path": path, "bytes": size, "sha256": digest}
            for path, (size, digest) in sorted(files.items())
        ],
    }
    canonical = json.dumps(
        manifest,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _digest_bytes(canonical)


def _delta(before: _Tree, after: _Tree) -> dict[str, object]:
    before_paths = set(before.files)
    after_paths = set(after.files)
    added_paths = after_paths.difference(before_paths)
    removed_paths = before_paths.difference(after_paths)
    changed_paths = {
        path
        for path in before_paths.intersection(after_paths)
        if before.files[path] != after.files[path]
    }
    normalized_added: dict[str, tuple[int, str]] = {}
    for path in sorted(added_paths):
        normalized = (
            path.removeprefix(_OUTPUT_PREFIX)
            if path.startswith(_OUTPUT_PREFIX)
            else f"__outside_pagefind__/{path}"
        )
        normalized_added[normalized] = after.files[path]
    return {
        "added_tree_sha256": _tree_digest(normalized_added),
        "added_path_count": len(added_paths),
        "removed_path_count": len(removed_paths),
        "changed_path_count": len(changed_paths),
        "outside_prefix_path_count": sum(
            not path.startswith(_OUTPUT_PREFIX) for path in added_paths
        ),
    }


def _lock_entry(
    packages: Mapping[str, Any],
    package: str,
) -> tuple[str, str]:
    value = packages.get(f"node_modules/{package}")
    if not isinstance(value, Mapping):
        raise ShadowFullBuildError(f"package-lock is missing {package}")
    version = value.get("version")
    integrity = value.get("integrity")
    if version != _PAGEFIND_VERSION:
        raise ShadowFullBuildError(f"{package} must be pinned to Pagefind 1.5.2")
    if not isinstance(integrity, str) or not integrity.startswith("sha512-"):
        raise ShadowFullBuildError(f"{package} integrity is missing")
    try:
        decoded = base64.b64decode(integrity.removeprefix("sha512-"), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ShadowFullBuildError(f"{package} integrity is invalid") from exc
    if len(decoded) != 64:
        raise ShadowFullBuildError(f"{package} integrity is invalid")
    return version, integrity


def _tool_identity(
    *,
    package_lock: Path | str,
    pagefind_runner: Path | str,
    platform_package: str,
    pagefind_command: Sequence[str],
    command_inputs: Mapping[str, Path | str],
) -> dict[str, object]:
    if not _PAGEFIND_PLATFORM.fullmatch(platform_package):
        raise ShadowFullBuildError("Pagefind platform package is invalid")
    if len(command_inputs) > 32:
        raise ShadowFullBuildError("Pagefind command inputs exceed the limit")
    lock_payload = _read_regular_file(package_lock, "package-lock")
    runner_payload = _read_regular_file(pagefind_runner, "Pagefind runner")
    try:
        lock = json.loads(lock_payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ShadowFullBuildError("package-lock is not valid UTF-8 JSON") from exc
    if not isinstance(lock, Mapping):
        raise ShadowFullBuildError("package-lock root must be an object")
    packages = lock.get("packages")
    if not isinstance(packages, Mapping):
        raise ShadowFullBuildError("package-lock packages map is missing")
    version, npm_integrity = _lock_entry(packages, "pagefind")
    platform_version, platform_integrity = _lock_entry(packages, platform_package)
    if platform_version != version:
        raise ShadowFullBuildError("Pagefind platform package version mismatch")
    if (
        isinstance(pagefind_command, (str, bytes))
        or not 1 <= len(pagefind_command) <= 32
        or any(
            not isinstance(argument, str)
            or not argument
            or len(argument) > 256
            or any(ord(character) < 32 for character in argument)
            for argument in pagefind_command
        )
    ):
        raise ShadowFullBuildError("Pagefind command identity is invalid")
    normalized_inputs: list[dict[str, str]] = []
    for name, path in sorted(command_inputs.items()):
        if not _COMMAND_INPUT_NAME.fullmatch(name):
            raise ShadowFullBuildError(f"Pagefind command input name is invalid: {name}")
        normalized_inputs.append(
            {
                "name": name,
                "sha256": _digest_bytes(
                    _read_regular_file(path, f"Pagefind command input {name}")
                ),
            }
        )
    command = list(pagefind_command)
    command_identity = {
        "schema_version": "shared_pagefind_command_v1",
        "command": command,
        "inputs": normalized_inputs,
    }
    return {
        "name": "pagefind",
        "version": version,
        "package_lock_sha256": _digest_bytes(lock_payload),
        "npm_integrity": npm_integrity,
        "platform_package": platform_package,
        "platform_integrity": platform_integrity,
        "runner_sha256": _digest_bytes(runner_payload),
        "command": command,
        "command_inputs": normalized_inputs,
        "command_sha256": _digest_bytes(canonical_json_bytes(command_identity)),
    }


def build_shared_pagefind_report(
    *,
    hugo_baseline: Path | str,
    hugo_candidate: Path | str,
    final_baseline: Path | str,
    final_candidate: Path | str,
    pagefind_bundle: Path | str,
    package_lock: Path | str,
    pagefind_runner: Path | str,
    platform_package: str,
    code_sha: str,
    content_sha: str,
    pagefind_command: Sequence[str] = _DEFAULT_PAGEFIND_COMMAND,
    command_inputs: Mapping[str, Path | str] | None = None,
) -> ShadowFullBuildBundle:
    """Build a composite report without weakening either exact tree comparison."""

    for path, field in (
        (hugo_baseline, "Hugo baseline"),
        (hugo_candidate, "Hugo candidate"),
        (final_baseline, "final baseline"),
        (final_candidate, "final candidate"),
        (pagefind_bundle, "Pagefind bundle"),
    ):
        _check_path_components(path, field)

    hugo_report = compare_trees(
        hugo_baseline,
        hugo_candidate,
        code_sha=code_sha,
        content_sha=content_sha,
    )
    final_report = compare_trees(
        final_baseline,
        final_candidate,
        code_sha=code_sha,
        content_sha=content_sha,
    )
    baseline_hugo_tree = _inspect_tree(hugo_baseline)
    candidate_hugo_tree = _inspect_tree(hugo_candidate)
    baseline_final_tree = _inspect_tree(final_baseline)
    candidate_final_tree = _inspect_tree(final_candidate)
    bundle_tree = _inspect_tree(pagefind_bundle)
    bundle_digest = "sha256:" + bundle_tree.tree_sha256
    baseline_delta = _delta(baseline_hugo_tree, baseline_final_tree)
    candidate_delta = _delta(candidate_hugo_tree, candidate_final_tree)
    preexisting = sum(
        path.startswith(_OUTPUT_PREFIX)
        for path in set(baseline_hugo_tree.files).union(candidate_hugo_tree.files)
    )
    bundle_files = len(bundle_tree.files)
    bundle_html = sum(path.casefold().endswith(".html") for path in bundle_tree.files)
    expected_delta = {
        "added_tree_sha256": bundle_digest,
        "added_path_count": bundle_files,
        "removed_path_count": 0,
        "changed_path_count": 0,
        "outside_prefix_path_count": 0,
    }
    hugo_file_count = hugo_report["file_count"]
    hugo_html_count = hugo_report["html_count"]
    final_file_count = final_report["file_count"]
    final_html_count = final_report["html_count"]
    count_relation_matches = (
        isinstance(hugo_file_count, int)
        and not isinstance(hugo_file_count, bool)
        and isinstance(hugo_html_count, int)
        and not isinstance(hugo_html_count, bool)
        and final_file_count == hugo_file_count + bundle_files
        and final_html_count == hugo_html_count + bundle_html
    )
    matches = (
        hugo_report["matches"] is True
        and final_report["matches"] is True
        and bundle_files > 0
        and preexisting == 0
        and baseline_delta == expected_delta
        and candidate_delta == expected_delta
        and count_relation_matches
    )
    report: dict[str, object] = {
        "schema_version": FULL_BUILD_REPORT_SCHEMA,
        "matches": matches,
        "code_sha": code_sha,
        "content_sha": content_sha,
        "comparison_profile": FULL_BUILD_PROFILE,
        "hugo_report_digest": _report_digest(hugo_report),
        "final_report_digest": _report_digest(final_report),
        "pagefind": {
            "strategy": PAGEFIND_STRATEGY,
            "input_tree_sha256": "sha256:" + candidate_hugo_tree.tree_sha256,
            "output_prefix": _OUTPUT_PREFIX,
            "bundle_tree_sha256": bundle_digest,
            "bundle_file_count": bundle_files,
            "bundle_total_bytes": sum(size for size, _digest in bundle_tree.files.values()),
            "bundle_html_count": bundle_html,
            "preexisting_output_path_count": preexisting,
            "baseline_delta": baseline_delta,
            "candidate_delta": candidate_delta,
            "tool": _tool_identity(
                package_lock=package_lock,
                pagefind_runner=pagefind_runner,
                platform_package=platform_package,
                pagefind_command=pagefind_command,
                command_inputs=command_inputs or {},
            ),
        },
    }
    return ShadowFullBuildBundle(
        report=report,
        supporting_reports=(hugo_report, final_report),
    )


def summarize_full_build(
    report: Mapping[str, object],
    *,
    record_digest: str | None,
) -> dict[str, object]:
    """Return a bounded operational summary for Actions logs."""

    pagefind_value = report.get("pagefind")
    pagefind = pagefind_value if isinstance(pagefind_value, Mapping) else {}
    tool_value = pagefind.get("tool")
    tool = tool_value if isinstance(tool_value, Mapping) else {}
    inputs_value = tool.get("command_inputs")
    input_names = [
        item.get("name")
        for item in inputs_value
        if isinstance(item, Mapping) and isinstance(item.get("name"), str)
    ] if isinstance(inputs_value, list) else []
    return {
        "schema_version": "shadow_full_build_summary_v1",
        "report_schema_version": report.get("schema_version"),
        "matches": report.get("matches"),
        "code_sha": report.get("code_sha"),
        "content_sha": report.get("content_sha"),
        "comparison_profile": report.get("comparison_profile"),
        "hugo_report_digest": report.get("hugo_report_digest"),
        "final_report_digest": report.get("final_report_digest"),
        "pagefind_strategy": pagefind.get("strategy"),
        "pagefind_input_tree_sha256": pagefind.get("input_tree_sha256"),
        "pagefind_bundle_tree_sha256": pagefind.get("bundle_tree_sha256"),
        "pagefind_bundle_file_count": pagefind.get("bundle_file_count"),
        "pagefind_bundle_total_bytes": pagefind.get("bundle_total_bytes"),
        "baseline_delta": pagefind.get("baseline_delta"),
        "candidate_delta": pagefind.get("candidate_delta"),
        "pagefind_version": tool.get("version"),
        "pagefind_platform_package": tool.get("platform_package"),
        "pagefind_package_lock_sha256": tool.get("package_lock_sha256"),
        "pagefind_runner_sha256": tool.get("runner_sha256"),
        "pagefind_command_sha256": tool.get("command_sha256"),
        "pagefind_command_input_names": input_names,
        "report_digest": _report_digest(report),
        "record_digest": record_digest,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hugo-baseline", type=Path, required=True)
    parser.add_argument("--hugo-candidate", type=Path, required=True)
    parser.add_argument("--final-baseline", type=Path, required=True)
    parser.add_argument("--final-candidate", type=Path, required=True)
    parser.add_argument("--pagefind-bundle", type=Path, required=True)
    parser.add_argument("--package-lock", type=Path, required=True)
    parser.add_argument("--pagefind-runner", type=Path, required=True)
    parser.add_argument("--platform-package", required=True)
    parser.add_argument(
        "--pagefind-command",
        nargs="+",
        default=list(_DEFAULT_PAGEFIND_COMMAND),
        metavar="ARG",
    )
    parser.add_argument("--command-input", action="append", default=[], metavar="NAME=PATH")
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--code-sha", required=True)
    parser.add_argument("--content-sha", required=True)
    parser.add_argument("--evidence-root", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--completed-at")
    parser.add_argument("--expected-previous-digest")
    return parser


def _validate_evidence_args(args: argparse.Namespace) -> datetime | None:
    optional = (args.run_id, args.completed_at, args.expected_previous_digest)
    if args.evidence_root is None:
        if any(optional):
            raise ShadowFullBuildError("shadow evidence options require --evidence-root")
        return None
    missing = [
        flag
        for flag, value in (
            ("--run-id", args.run_id),
            ("--completed-at", args.completed_at),
        )
        if value is None
    ]
    if missing:
        raise ShadowFullBuildError("--evidence-root requires " + ", ".join(missing))
    assert isinstance(args.completed_at, str)
    return _evidence_time(args.completed_at)


def _command_inputs(values: Sequence[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        name, separator, path = value.partition("=")
        if (
            separator != "="
            or not _COMMAND_INPUT_NAME.fullmatch(name)
            or not path
            or name in result
        ):
            raise ShadowFullBuildError(f"invalid --command-input: {value}")
        result[name] = Path(path)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    record_digest: str | None = None
    try:
        completed_at = _validate_evidence_args(args)
        bundle = build_shared_pagefind_report(
            hugo_baseline=args.hugo_baseline,
            hugo_candidate=args.hugo_candidate,
            final_baseline=args.final_baseline,
            final_candidate=args.final_candidate,
            pagefind_bundle=args.pagefind_bundle,
            package_lock=args.package_lock,
            pagefind_runner=args.pagefind_runner,
            platform_package=args.platform_package,
            pagefind_command=args.pagefind_command,
            command_inputs=_command_inputs(args.command_input),
            code_sha=args.code_sha,
            content_sha=args.content_sha,
        )
        _atomic_json(args.report, bundle.report)
        if args.evidence_root is not None:
            assert completed_at is not None
            assert isinstance(args.run_id, str)
            record = append_shadow_evidence(
                args.evidence_root,
                report=bundle.report,
                supporting_reports=bundle.supporting_reports,
                run_id=args.run_id,
                completed_at=completed_at,
                full_build=True,
                code_sha=args.code_sha,
                content_sha=args.content_sha,
                expected_previous_digest=args.expected_previous_digest,
            )
            record_digest = record.record_digest
    except (
        OSError,
        ShadowComparisonError,
        ShadowEvidenceError,
        ShadowFullBuildError,
    ) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1
    print(
        json.dumps(
            summarize_full_build(bundle.report, record_digest=record_digest),
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if bundle.report["matches"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
