"""Deterministic, evidence-preserving repair plans for historical Markdown.

The planner is deliberately read-only.  Applying a plan is a separate operation
that reuses the repository's dedupe shadow/soak gate, takes an immutable backup,
checks file preconditions, and replaces each file atomically.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unicodedata
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

from ._json import sha256_digest
from .content_quality import (
    analyze_post,
    is_source_brief,
    remove_empty_section_headings,
)
from .identity import canonicalize_url
from .migrations import (
    MigrationSafetyError,
    source_revision,
    validate_dedupe_execution_gate,
    validate_execution_gate,
)
from .stores import UnsafeStorePathError
from .tag_taxonomy import normalize_tags

DEFAULT_CATEGORY_WHITELIST = frozenset(
    {
        "AI 工程",
        "产品与创业",
        "前端",
        "后端",
        "大模型",
        "安全",
        "开发工具",
        "开源生态",
        "效率与方法论",
        "数据",
        "生活与杂谈",
        "系统与基础设施",
        "论文",
    }
)
DEFAULT_SCENARIO_WHITELIST = frozenset(
    {
        "Web应用开发",
        "前端开发",
        "后端开发",
        "全栈开发",
        "AI/ML项目",
        "自然语言处理",
        "计算机视觉",
        "数据科学",
        "大语言模型",
        "RAG应用",
        "DevOps/运维",
        "云原生/容器",
        "Kubernetes",
        "安全工具",
        "监控/日志",
        "数据库",
        "命令行工具",
        "自动化脚本",
        "测试工具",
        "文档工具",
        "编辑器/IDE",
        "效率工具",
        "移动应用",
        "游戏开发",
        "物联网",
        "区块链",
        "桌面应用",
        "嵌入式系统",
        "设计工具",
        "数据可视化",
        "动画/3D",
    }
)

_BACKUP_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_MAX_MARKDOWN_BYTES = 2 * 1024 * 1024
_FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?(.*)\Z", re.DOTALL)
_RELREF = re.compile(
    r"(?P<prefix>\{\{[<%]\s*relref\s+)(?P<quote>['\"])(?P<target>.+?)(?P=quote)(?P<suffix>\s*[>%]\}\})"
)
@dataclass(frozen=True, slots=True)
class PlannedWrite:
    """One compare-and-swap file replacement relative to the posts root."""

    path: str
    before_sha256: str | None
    after_sha256: str
    content: bytes


@dataclass(frozen=True, slots=True)
class PlannedDelete:
    """One compare-and-swap file deletion relative to the posts root."""

    path: str
    before_sha256: str


@dataclass(frozen=True, slots=True)
class HistoricalRepairPlan:
    """Public deterministic manifest plus private mutation payloads."""

    content_root: Path
    reference_root: Path
    manifest: dict[str, Any]
    writes: tuple[PlannedWrite, ...]
    deletes: tuple[PlannedDelete, ...]


@dataclass(frozen=True, slots=True)
class _Document:
    path: Path
    relative_path: str
    raw: bytes
    metadata: dict[str, Any]
    body: str
    canonical_url: str
    contamination_reasons: tuple[str, ...]
    warning_reasons: tuple[str, ...]
    quality_score: int


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _regular_markdown_files(root: Path) -> list[Path]:
    if root.is_symlink() or not root.is_dir():
        raise UnsafeStorePathError(f"historical repair root must be a regular directory: {root}")
    paths: list[Path] = []
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        retained: list[str] = []
        for name in sorted(directory_names):
            candidate = current_path / name
            if candidate.is_symlink():
                raise UnsafeStorePathError(
                    f"historical repair root contains a symlink: {candidate}"
                )
            retained.append(name)
        directory_names[:] = retained
        for name in sorted(file_names):
            candidate = current_path / name
            details = candidate.lstat()
            if (
                candidate.is_symlink()
                or not stat.S_ISREG(details.st_mode)
                or details.st_nlink != 1
            ):
                raise UnsafeStorePathError(
                    f"historical repair root contains an unsafe file: {candidate}"
                )
            if candidate.suffix.casefold() == ".md":
                if details.st_size > _MAX_MARKDOWN_BYTES:
                    raise MigrationSafetyError(
                        f"historical repair Markdown is too large: {candidate}"
                    )
                paths.append(candidate)
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def _normalize_label(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(unicodedata.normalize("NFC", value).strip().split())


def _normalized_list(value: object, *, limit: int | None = None) -> list[str]:
    values: Iterable[object]
    if isinstance(value, list):
        values = value
    elif isinstance(value, str):
        values = (value,)
    else:
        values = ()
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        normalized = _normalize_label(item)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
        if limit is not None and len(result) >= limit:
            break
    return result


def _quality_score(body: str, warning_reasons: tuple[str, ...] = ()) -> int:
    compact_length = len(re.sub(r"\s+", "", body))
    headings = len(re.findall(r"(?m)^#{1,4}\s+\S", body))
    links = len(re.findall(r"https?://", body))
    fenced_blocks = body.count("```") // 2
    penalty = 0
    if "empty_section" in warning_reasons:
        penalty += 600
    if "source_excerpt_truncated" in warning_reasons:
        penalty += 300
    return (
        min(compact_length, 12_000)
        + min(headings, 20) * 120
        + min(links, 20) * 40
        + min(fenced_blocks, 10) * 100
        - penalty
    )


def _parse_document(path: Path, root: Path) -> _Document:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Markdown is not UTF-8: {path}") from exc
    match = _FRONTMATTER.match(text)
    if match is None:
        raise ValueError(f"Markdown has no closed YAML frontmatter: {path}")
    try:
        parsed = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Markdown frontmatter is invalid: {path}: {exc}") from exc
    if not isinstance(parsed, Mapping):
        raise ValueError(f"Markdown frontmatter must be a mapping: {path}")
    metadata = {str(key): copy.deepcopy(value) for key, value in parsed.items()}
    external_url = metadata.get("external_url")
    if not isinstance(external_url, str):
        raise ValueError(f"Markdown has no external_url: {path}")
    canonical_url = canonicalize_url(external_url)
    body = match.group(2)
    analysis = analyze_post(text)
    return _Document(
        path=path,
        relative_path=path.relative_to(root).as_posix(),
        raw=raw,
        metadata=metadata,
        body=body,
        canonical_url=canonical_url,
        contamination_reasons=analysis.fatal_reasons,
        warning_reasons=analysis.warning_reasons,
        quality_score=_quality_score(body, analysis.warning_reasons),
    )


def _date_key(document: _Document) -> tuple[str, str]:
    value = document.metadata.get("date")
    parsed: datetime | None = None
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime.combine(value, datetime.min.time())
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            parsed = None
    if parsed is None:
        return "9999-12-31T23:59:59.999999Z", document.relative_path
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    normalized = parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")
    return normalized, document.relative_path


def _hugo_route(relative_path: str) -> str:
    path = Path(relative_path)
    parts = list(path.with_suffix("").parts)
    if parts and parts[-1] in {"index", "_index"}:
        parts.pop()
    suffix = "/".join(parts)
    return f"/posts/{suffix}/" if suffix else "/posts/"


def _document_route(document: _Document) -> str:
    explicit = document.metadata.get("url")
    if isinstance(explicit, str) and explicit.strip().startswith("/"):
        normalized = "/" + explicit.strip().strip("/") + "/"
        if ".." not in Path(normalized).parts:
            return normalized
    slug = _normalize_label(document.metadata.get("slug"))
    if slug and "/" not in slug and ".." not in slug:
        return f"/posts/{slug.strip('/')}/"
    return _hugo_route(document.relative_path)


def _group_aliases(ordered: Iterable[_Document], route: _Document) -> list[str]:
    canonical_route = _document_route(route)
    aliases: set[str] = set()
    for document in ordered:
        if document.path == route.path:
            continue
        aliases.add(_document_route(document))
        aliases.update(_safe_aliases(document.metadata.get("aliases")))
    aliases.discard(canonical_route)
    return sorted(aliases)


def _safe_aliases(value: object) -> list[str]:
    aliases: list[str] = []
    for alias in _normalized_list(value):
        if not alias.startswith("/") or ".." in Path(alias).parts:
            continue
        normalized = "/" + alias.strip("/") + "/"
        if normalized not in aliases:
            aliases.append(normalized)
    return aliases


def _filtered_metadata(
    source: _Document,
    route: _Document,
    *,
    canonical_url: str,
    aliases: list[str],
    category_whitelist: frozenset[str],
    scenario_whitelist: frozenset[str],
) -> dict[str, Any]:
    metadata = copy.deepcopy(source.metadata)
    metadata["external_url"] = canonical_url
    metadata["tags"] = normalize_tags(source.metadata.get("tags"), limit=8)
    metadata["categories"] = [
        value
        for value in _normalized_list(source.metadata.get("categories"))
        if value in category_whitelist
    ]
    metadata["scenarios"] = [
        value
        for value in _normalized_list(source.metadata.get("scenarios"))
        if value in scenario_whitelist
    ]
    if "date" in route.metadata:
        metadata["date"] = copy.deepcopy(route.metadata["date"])
    for route_key in ("url", "slug"):
        if route_key in route.metadata:
            metadata[route_key] = copy.deepcopy(route.metadata[route_key])
        else:
            metadata.pop(route_key, None)
    existing_aliases = _safe_aliases(route.metadata.get("aliases"))
    metadata["aliases"] = sorted(set(existing_aliases + aliases))
    return _active_provenance_metadata(metadata, source.body)


def _active_provenance_metadata(
    metadata: Mapping[str, Any], body: str
) -> dict[str, Any]:
    """Label legacy output honestly without claiming a missing source snapshot."""

    result = copy.deepcopy(dict(metadata))
    if is_source_brief(result, body):
        result["content_mode"] = "legacy_source_brief"
        result["publication_tier"] = "C"
    else:
        result["content_mode"] = "legacy_analysis"
        result["publication_tier"] = "LEGACY"
    result["source_provenance"] = "legacy_no_snapshot"
    result["source_support"] = 0.0
    return result


def _normalized_active_singleton(
    document: _Document,
    *,
    canonical_url: str,
) -> tuple[dict[str, Any], str] | None:
    """Return a minimal rewrite for one active clean article.

    Singleton normalization leaves categories, scenarios, routes, and all
    unrelated frontmatter untouched. Empty shell headings are removed without
    inventing prose so structural cleanup shares the same backup mechanism.
    """
    if document.metadata.get("archived") is True:
        return None
    normalized_tags = normalize_tags(document.metadata.get("tags"), limit=8)
    metadata = copy.deepcopy(document.metadata)
    metadata["external_url"] = canonical_url
    metadata["tags"] = normalized_tags
    metadata = _active_provenance_metadata(metadata, document.body)
    body, _ = remove_empty_section_headings(document.body)
    if metadata == document.metadata and body == document.body:
        return None
    return metadata, body


def _render_document(metadata: Mapping[str, Any], body: str) -> bytes:
    frontmatter = yaml.safe_dump(
        dict(metadata),
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip()
    normalized_body = body.strip()
    return f"---\n{frontmatter}\n---\n\n{normalized_body}\n".encode()


def _archive_stub(
    route: _Document,
    *,
    canonical_url: str,
    aliases: list[str],
    category_whitelist: frozenset[str],
    scenario_whitelist: frozenset[str],
) -> tuple[dict[str, Any], str]:
    metadata = _filtered_metadata(
        route,
        route,
        canonical_url=canonical_url,
        aliases=aliases,
        category_whitelist=category_whitelist,
        scenario_whitelist=scenario_whitelist,
    )
    metadata["archived"] = True
    metadata["content_mode"] = "archived"
    metadata["publication_tier"] = "ARCHIVED"
    metadata["source_provenance"] = "legacy_no_snapshot"
    metadata["source_support"] = 0.0
    metadata["archive_reason"] = "historical_content_quality_gate"
    metadata["description"] = "历史条目已归档：现有正文未通过内容质量门，请查阅原始来源。"
    metadata["title"] = str(metadata.get("title") or "历史条目").replace(
        "<", "＜"
    ).replace(">", "＞")
    metadata["tags"] = []
    metadata["categories"] = []
    metadata["scenarios"] = []
    metadata["_build"] = {"list": "never", "render": "always"}
    body = (
        "## 历史条目归档说明\n\n"
        "该条目的历史正文未通过内容质量门，可能包含基于标题推测的内容。"
        "为避免继续传播不可核验文本，本站仅保留透明归档记录。\n\n"
        f"- 历史内容质量门未通过\n- 原始来源：<{canonical_url}>\n"
    )
    return metadata, body


def _relative_operation_path(path: Path, content_root: Path) -> str:
    return Path(os.path.relpath(path, content_root)).as_posix()


def _relref_target_map(
    *, content_root: Path, canonical_path: str, delete_paths: Iterable[str]
) -> dict[str, str]:
    reference_root = content_root.parent
    canonical_absolute = content_root / canonical_path
    canonical_reference = canonical_absolute.relative_to(reference_root).as_posix()
    result: dict[str, str] = {}
    for relative in delete_paths:
        deleted_absolute = content_root / relative
        deleted_reference = deleted_absolute.relative_to(reference_root).as_posix()
        result[deleted_reference] = canonical_reference
        result[relative] = canonical_path
        result[f"/{deleted_reference}"] = f"/{canonical_reference}"
    return result


def _rewrite_relrefs(
    text: str, target_map: Mapping[str, str]
) -> tuple[str, list[tuple[str, str, int]]]:
    counts: dict[tuple[str, str], int] = defaultdict(int)

    def replace(match: re.Match[str]) -> str:
        old_target = match.group("target")
        new_target = target_map.get(old_target)
        if new_target is None:
            return match.group(0)
        counts[(old_target, new_target)] += 1
        return (
            f"{match.group('prefix')}{match.group('quote')}{new_target}"
            f"{match.group('quote')}{match.group('suffix')}"
        )

    rewritten = _RELREF.sub(replace, text)
    records = [
        (source, target, count)
        for (source, target), count in sorted(counts.items())
    ]
    return rewritten, records


def _resolve_input_paths(root: Path, input_paths: Iterable[Path] | None) -> list[Path]:
    candidates = _regular_markdown_files(root) if input_paths is None else list(input_paths)
    result: list[Path] = []
    for value in candidates:
        path = Path(value).absolute()
        if not _is_within(path, root):
            raise UnsafeStorePathError(f"historical repair input escapes content root: {path}")
        details = path.lstat()
        if path.is_symlink() or not stat.S_ISREG(details.st_mode):
            raise UnsafeStorePathError(f"historical repair input is unsafe: {path}")
        if details.st_size > _MAX_MARKDOWN_BYTES:
            raise MigrationSafetyError(f"historical repair Markdown is too large: {path}")
        if path.suffix.casefold() == ".md":
            result.append(path)
    return sorted(set(result), key=lambda path: path.relative_to(root).as_posix())


def build_historical_repair_plan(
    *,
    content_root: str | Path,
    category_whitelist: Iterable[str] = DEFAULT_CATEGORY_WHITELIST,
    scenario_whitelist: Iterable[str] = DEFAULT_SCENARIO_WHITELIST,
    input_paths: Iterable[Path] | None = None,
) -> HistoricalRepairPlan:
    """Build a deterministic plan for content repair and active metadata normalization."""

    root = Path(content_root).absolute()
    reference_root = root.parent
    paths = _resolve_input_paths(root, input_paths)
    categories = frozenset(_normalize_label(value) for value in category_whitelist)
    scenarios = frozenset(_normalize_label(value) for value in scenario_whitelist)
    grouped: dict[str, list[_Document]] = defaultdict(list)
    issues: list[dict[str, str]] = []
    for path in paths:
        try:
            document = _parse_document(path, root)
        except (OSError, ValueError) as exc:
            issues.append(
                {"path": path.relative_to(root).as_posix(), "reason": str(exc)}
            )
            continue
        grouped[document.canonical_url].append(document)

    replacement_bytes: dict[Path, bytes] = {}
    deletion_documents: dict[Path, _Document] = {}
    target_map: dict[str, str] = {}
    public_groups: list[dict[str, Any]] = []
    public_group_by_route: dict[Path, dict[str, Any]] = {}

    for canonical_url, candidates in sorted(grouped.items()):
        ordered = sorted(candidates, key=lambda document: document.relative_path)
        route = min(ordered, key=_date_key)
        is_clean_singleton = len(ordered) == 1 and not route.contamination_reasons
        if is_clean_singleton:
            normalized = _normalized_active_singleton(
                route,
                canonical_url=canonical_url,
            )
            if normalized is None:
                continue
            metadata, body = normalized
            winner: _Document | None = route
            disposition = "normalize_metadata"
            archive_reason: str | None = None
        else:
            clean = [document for document in ordered if not document.contamination_reasons]
            winner = (
                sorted(
                    clean,
                    key=lambda document: (
                        -document.quality_score,
                        document.relative_path,
                    ),
                )[0]
                if clean
                else None
            )
            if winner is None:
                metadata, body = _archive_stub(
                    route,
                    canonical_url=canonical_url,
                    aliases=_group_aliases(ordered, route),
                    category_whitelist=categories,
                    scenario_whitelist=scenarios,
                )
                disposition = "archive_stub"
                archive_reason = "all_candidates_failed_content_quality_gate"
            else:
                metadata = _filtered_metadata(
                    winner,
                    route,
                    canonical_url=canonical_url,
                    aliases=_group_aliases(ordered, route),
                    category_whitelist=categories,
                    scenario_whitelist=scenarios,
                )
                body, _ = remove_empty_section_headings(winner.body)
                disposition = "merge"
                archive_reason = None
        delete_paths = sorted(
            document.relative_path for document in ordered if document.path != route.path
        )
        aliases = _group_aliases(ordered, route)
        rendered = _render_document(metadata, body)
        replacement_bytes[route.path] = rendered
        for document in ordered:
            if document.path != route.path:
                deletion_documents[document.path] = document
        target_map.update(
            _relref_target_map(
                content_root=root,
                canonical_path=route.relative_path,
                delete_paths=delete_paths,
            )
        )
        public_group: dict[str, Any] = {
            "canonical_url": canonical_url,
            "canonical_path": route.relative_path,
            "body_source": winner.relative_path if winner is not None else None,
            "disposition": disposition,
            "source_file_count": len(ordered),
            "paths": [document.relative_path for document in ordered],
            "delete_paths": delete_paths,
            "aliases": aliases,
            "metadata": {
                "categories": list(metadata.get("categories", [])),
                "scenarios": list(metadata.get("scenarios", [])),
                "tags": list(metadata.get("tags", [])),
            },
            "candidates": [
                {
                    "path": document.relative_path,
                    "polluted": bool(document.contamination_reasons),
                    "contamination_reasons": list(document.contamination_reasons),
                    "warning_reasons": list(document.warning_reasons),
                    "quality_score": document.quality_score,
                }
                for document in ordered
            ],
            "output_sha256": _sha256(rendered),
        }
        if archive_reason is not None:
            public_group["archive_reason"] = archive_reason
        public_groups.append(public_group)
        public_group_by_route[route.path] = public_group

    reference_files = _regular_markdown_files(reference_root)
    writes: list[PlannedWrite] = []
    relref_records: list[dict[str, Any]] = []
    for path in reference_files:
        if path in deletion_documents:
            continue
        before = path.read_bytes()
        base = replacement_bytes.get(path, before)
        try:
            base_text = base.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Markdown is not UTF-8: {path}") from exc
        rewritten, replacements = _rewrite_relrefs(base_text, target_map)
        after = rewritten.encode("utf-8")
        if path in public_group_by_route:
            public_group_by_route[path]["output_sha256"] = _sha256(after)
        operation_path = _relative_operation_path(path, root)
        for source, target, count in replacements:
            relref_records.append(
                {
                    "document": operation_path,
                    "from": source,
                    "to": target,
                    "occurrences": count,
                }
            )
        if after != before:
            writes.append(
                PlannedWrite(
                    path=operation_path,
                    before_sha256=_sha256(before),
                    after_sha256=_sha256(after),
                    content=after,
                )
            )

    deletes = [
        PlannedDelete(path=document.relative_path, before_sha256=_sha256(document.raw))
        for document in deletion_documents.values()
    ]
    writes.sort(key=lambda operation: operation.path)
    deletes.sort(key=lambda operation: operation.path)
    relref_records.sort(
        key=lambda record: (
            str(record["document"]),
            str(record["from"]),
            str(record["to"]),
        )
    )
    base_manifest: dict[str, Any] = {
        "schema_version": "historical_repair_plan_v1",
        "source_root": str(root),
        "dry_run": True,
        "mutation_performed": False,
        "files_scanned": len(paths),
        "repair_group_count": len(public_groups),
        "normalization_group_count": sum(
            group["disposition"] == "normalize_metadata" for group in public_groups
        ),
        "duplicate_group_count": sum(
            int(group["source_file_count"]) > 1 for group in public_groups
        ),
        "duplicate_file_count": len(deletes),
        "planned_changes": len(writes) + len(deletes),
        "groups": public_groups,
        "relref_rewrites": relref_records,
        "issues": sorted(issues, key=lambda issue: (issue["path"], issue["reason"])),
        "writes": [
            {
                "path": operation.path,
                "before_sha256": operation.before_sha256,
                "after_sha256": operation.after_sha256,
            }
            for operation in writes
        ],
        "deletes": [
            {"path": operation.path, "before_sha256": operation.before_sha256}
            for operation in deletes
        ],
        "execution_policy": {
            "requires_expected_source_sha": True,
            "requires_backup_id": True,
            "requires_max_changes": True,
            "execution_profiles": [
                "shadow_soak_dedupe",
                "reviewed_git_repository",
            ],
            "shadow_soak_profile": "24_runs_3_full_builds_7_day_soak",
            "shadow_soak_batch_limit": 100,
            "reviewed_repository_profile": (
                "clean_codex_branch_exact_head_exact_plan_digest_with_backup"
            ),
            "repository_reviewed_batch_limit": 10_000,
            "atomic_strategy": "compare_and_swap_atomic_replace_with_rollback_backup",
        },
        "selection_policy": {
            "canonical_route": "oldest_frontmatter_date_then_lexical_path",
            "body_source": "clean_candidates_only_then_capped_structural_quality_score",
            "metadata": "body_source_only_with_whitelists_and_eight_tag_cap",
            "active_singletons": (
                "canonical_external_url_and_shared_tag_taxonomy_only; "
                "unrelated_metadata_preserved"
            ),
            "all_polluted": "transparent_archive_stub",
            "active_provenance": (
                "legacy_analysis_without_source_snapshot_or_strict_source_brief_tier_c"
            ),
        },
        "execution_blocked": "requires_one_validated_execution_profile",
    }
    manifest = dict(base_manifest)
    manifest["plan_digest"] = sha256_digest(base_manifest)
    return HistoricalRepairPlan(
        content_root=root,
        reference_root=reference_root,
        manifest=manifest,
        writes=tuple(writes),
        deletes=tuple(deletes),
    )


def _with_batch_selection(
    plan: HistoricalRepairPlan,
    selection: Mapping[str, Any],
) -> HistoricalRepairPlan:
    manifest = copy.deepcopy(plan.manifest)
    manifest.pop("plan_digest", None)
    manifest["batch_selection"] = copy.deepcopy(dict(selection))
    manifest["plan_digest"] = sha256_digest(manifest)
    return HistoricalRepairPlan(
        content_root=plan.content_root,
        reference_root=plan.reference_root,
        manifest=manifest,
        writes=plan.writes,
        deletes=plan.deletes,
    )


def build_historical_repair_batch(
    *,
    content_root: str | Path,
    max_changes: int,
    category_whitelist: Iterable[str] = DEFAULT_CATEGORY_WHITELIST,
    scenario_whitelist: Iterable[str] = DEFAULT_SCENARIO_WHITELIST,
) -> HistoricalRepairPlan:
    """Select the largest deterministic canonical-group prefix within one gate.

    The caller repeats this operation after each committed batch. Completed groups
    disappear from the next inventory, while every selected canonical URL is always
    planned with its complete candidate set. This keeps shared relref rewrites based
    on the current filesystem snapshot instead of precomputing stale future batches.
    """

    if (
        not isinstance(max_changes, int)
        or isinstance(max_changes, bool)
        or not 1 <= max_changes <= 100
    ):
        raise MigrationSafetyError("batch --max-changes must be between 1 and 100")

    categories = tuple(category_whitelist)
    scenarios = tuple(scenario_whitelist)
    full_plan = build_historical_repair_plan(
        content_root=content_root,
        category_whitelist=categories,
        scenario_whitelist=scenarios,
    )
    groups = sorted(
        full_plan.manifest["groups"],
        key=lambda group: str(group["canonical_url"]),
    )
    if not groups:
        return _with_batch_selection(
            full_plan,
            {
                "mode": "largest_safe_prefix",
                "atomic_unit": "canonical_url_group",
                "max_changes": max_changes,
                "total_group_count": 0,
                "selected_group_count": 0,
                "remaining_group_count": 0,
                "selected_canonical_urls": [],
                "next_canonical_url": None,
                "full_plan_digest": full_plan.manifest["plan_digest"],
            },
        )

    root = full_plan.content_root
    cache: dict[int, HistoricalRepairPlan] = {}

    def prefix_plan(group_count: int) -> HistoricalRepairPlan:
        cached = cache.get(group_count)
        if cached is not None:
            return cached
        selected_paths = [
            root / relative_path
            for group in groups[:group_count]
            for relative_path in group["paths"]
        ]
        candidate = build_historical_repair_plan(
            content_root=root,
            category_whitelist=categories,
            scenario_whitelist=scenarios,
            input_paths=selected_paths,
        )
        cache[group_count] = candidate
        return candidate

    first = prefix_plan(1)
    first_change_count = int(first.manifest["planned_changes"])
    if first_change_count > max_changes:
        raise MigrationSafetyError(
            "canonical group exceeds --max-changes and cannot be split: "
            f"{groups[0]['canonical_url']} ({first_change_count}>{max_changes})"
        )

    lower = 1
    upper = len(groups)
    while lower < upper:
        middle = (lower + upper + 1) // 2
        candidate = prefix_plan(middle)
        if int(candidate.manifest["planned_changes"]) <= max_changes:
            lower = middle
        else:
            upper = middle - 1

    selected = prefix_plan(lower)
    selected_urls = [str(group["canonical_url"]) for group in groups[:lower]]
    return _with_batch_selection(
        selected,
        {
            "mode": "largest_safe_prefix",
            "atomic_unit": "canonical_url_group",
            "max_changes": max_changes,
            "total_group_count": len(groups),
            "selected_group_count": lower,
            "remaining_group_count": len(groups) - lower,
            "selected_canonical_urls": selected_urls,
            "next_canonical_url": (
                str(groups[lower]["canonical_url"]) if lower < len(groups) else None
            ),
            "full_plan_digest": full_plan.manifest["plan_digest"],
        },
    )


def _operation_path(plan: HistoricalRepairPlan, relative: str) -> Path:
    path = (plan.content_root / relative).absolute()
    if not _is_within(path, plan.reference_root):
        raise UnsafeStorePathError(
            f"historical repair operation escapes reference root: {relative}"
        )
    return path


def _verify_preconditions(plan: HistoricalRepairPlan) -> None:
    for write in plan.writes:
        path = _operation_path(plan, write.path)
        if path.is_symlink() or not path.is_file():
            raise MigrationSafetyError(f"stale repair plan: write source changed: {write.path}")
        if _sha256(path.read_bytes()) != write.before_sha256:
            raise MigrationSafetyError(f"stale repair plan: write source changed: {write.path}")
    for deletion in plan.deletes:
        path = _operation_path(plan, deletion.path)
        if path.is_symlink() or not path.is_file():
            raise MigrationSafetyError(
                f"stale repair plan: delete source changed: {deletion.path}"
            )
        if _sha256(path.read_bytes()) != deletion.before_sha256:
            raise MigrationSafetyError(
                f"stale repair plan: delete source changed: {deletion.path}"
            )


def _atomic_write(path: Path, payload: bytes, *, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    finally:
        Path(temporary_name).unlink(missing_ok=True)


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    payload = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    _atomic_write(path, payload, mode=0o600)


def _backup_relative_path(plan: HistoricalRepairPlan, path: Path) -> Path:
    try:
        return path.relative_to(plan.reference_root)
    except ValueError as exc:
        raise UnsafeStorePathError(f"backup source escapes reference root: {path}") from exc


def _verify_applied(plan: HistoricalRepairPlan) -> None:
    for write in plan.writes:
        path = _operation_path(plan, write.path)
        if not path.is_file() or _sha256(path.read_bytes()) != write.after_sha256:
            raise MigrationSafetyError(f"applied repair receipt does not match: {write.path}")
    for deletion in plan.deletes:
        if _operation_path(plan, deletion.path).exists():
            raise MigrationSafetyError(f"applied repair receipt does not match: {deletion.path}")


def _repository_review_state(reference_root: Path) -> tuple[str, str]:
    branch_result = subprocess.run(
        ["git", "-C", str(reference_root), "symbolic-ref", "--quiet", "--short", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if branch_result.returncode != 0:
        raise MigrationSafetyError("reviewed repository repair requires an attached branch")
    status_result = subprocess.run(
        [
            "git",
            "-C",
            str(reference_root),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if status_result.returncode != 0:
        raise MigrationSafetyError("reviewed repository repair cannot read Git worktree state")
    return branch_result.stdout.strip(), status_result.stdout.strip()


def _restore_from_backup(
    plan: HistoricalRepairPlan,
    *,
    backup_directory: Path,
    affected_paths: Iterable[Path],
) -> None:
    before_root = backup_directory / "before"
    for path in sorted(set(affected_paths), key=lambda candidate: str(candidate)):
        backup = before_root / _backup_relative_path(plan, path)
        if backup.is_file():
            _atomic_write(path, backup.read_bytes(), mode=backup.stat().st_mode & 0o777)
        else:
            path.unlink(missing_ok=True)


def apply_historical_repair_plan(
    plan: HistoricalRepairPlan,
    *,
    expected_source_sha: str | None,
    expected_code_sha: str | None,
    backup_id: str | None,
    max_changes: int | None,
    shadow_evidence_root: Path | None,
    backup_root: Path,
    expected_plan_digest: str | None = None,
    repository_reviewed: bool = False,
) -> dict[str, Any]:
    """Apply a reviewed plan after one explicit safety profile validates it."""

    issues = plan.manifest.get("issues")
    if not isinstance(issues, list) or issues:
        issue_count = len(issues) if isinstance(issues, list) else "unknown"
        raise MigrationSafetyError(
            f"historical repair plan has unresolved issues: {issue_count}"
        )

    safety_profile = "shadow_soak_dedupe"
    if repository_reviewed:
        validate_execution_gate(
            execute=True,
            expected_source_sha=expected_source_sha,
            backup_id=backup_id,
            max_changes=max_changes,
            actual_source_sha=source_revision(plan.content_root),
        )
        if expected_plan_digest != plan.manifest["plan_digest"]:
            raise MigrationSafetyError("reviewed repository repair plan digest mismatch")
        branch, worktree_status = _repository_review_state(plan.reference_root)
        if not branch.startswith("codex/"):
            raise MigrationSafetyError(
                "reviewed repository repair requires a codex/ branch"
            )
        if worktree_status:
            raise MigrationSafetyError(
                "reviewed repository repair requires a clean Git worktree"
            )
        safety_profile = "reviewed_git_repository"
    else:
        validate_dedupe_execution_gate(
            content_root=plan.content_root,
            expected_source_sha=expected_source_sha,
            expected_code_sha=expected_code_sha,
            backup_id=backup_id,
            max_changes=max_changes,
            shadow_evidence_root=shadow_evidence_root,
        )
    if backup_id is None or not _BACKUP_ID.fullmatch(backup_id):
        raise MigrationSafetyError("--backup-id must be a safe identifier")
    if not isinstance(max_changes, int) or isinstance(max_changes, bool):
        raise MigrationSafetyError("--max-changes must be an integer")
    planned_changes = int(plan.manifest["planned_changes"])
    if planned_changes > max_changes:
        raise MigrationSafetyError(
            f"planned changes exceed --max-changes: {planned_changes}>{max_changes}"
        )

    backup_root = Path(backup_root).absolute()
    if backup_root.is_symlink() or (backup_root.exists() and not backup_root.is_dir()):
        raise UnsafeStorePathError(f"repair backup root is unsafe: {backup_root}")
    backup_directory = backup_root / backup_id
    receipt_path = backup_directory / "receipt.json"
    if receipt_path.is_file():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MigrationSafetyError(f"repair receipt is unreadable: {receipt_path}") from exc
        if receipt.get("plan_digest") != plan.manifest["plan_digest"]:
            raise MigrationSafetyError("backup id already belongs to a different repair plan")
        _verify_applied(plan)
        return {
            "schema_version": "historical_repair_result_v1",
            "plan_digest": plan.manifest["plan_digest"],
            "backup_id": backup_id,
            "already_applied": True,
            "mutation_performed": False,
            "changed_files": 0,
            "safety_profile": receipt.get("safety_profile", safety_profile),
        }
    if backup_directory.exists() or backup_directory.is_symlink():
        raise MigrationSafetyError(
            f"incomplete or conflicting repair backup exists: {backup_directory}"
        )

    _verify_preconditions(plan)
    affected_paths = [
        *(_operation_path(plan, operation.path) for operation in plan.writes),
        *(_operation_path(plan, operation.path) for operation in plan.deletes),
    ]
    backup_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    staging = Path(tempfile.mkdtemp(prefix=f".{backup_id}.", dir=backup_root))
    try:
        before_root = staging / "before"
        for path in sorted(set(affected_paths), key=lambda candidate: str(candidate)):
            relative = _backup_relative_path(plan, path)
            destination = before_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        _atomic_json(staging / "plan.json", plan.manifest)
        os.replace(staging, backup_directory)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    receipt = {
        "schema_version": "historical_repair_receipt_v1",
        "plan_digest": plan.manifest["plan_digest"],
        "backup_id": backup_id,
        "expected_source_sha": expected_source_sha,
        "expected_code_sha": expected_code_sha,
        "planned_changes": planned_changes,
        "safety_profile": safety_profile,
        "state": "applied",
    }
    try:
        for write in plan.writes:
            path = _operation_path(plan, write.path)
            mode = path.stat().st_mode & 0o777
            _atomic_write(path, write.content, mode=mode)
        for deletion in plan.deletes:
            _operation_path(plan, deletion.path).unlink()
        _verify_applied(plan)
        _atomic_json(receipt_path, receipt)
    except BaseException:
        receipt_path.unlink(missing_ok=True)
        _restore_from_backup(
            plan,
            backup_directory=backup_directory,
            affected_paths=affected_paths,
        )
        raise

    return {
        "schema_version": "historical_repair_result_v1",
        "plan_digest": plan.manifest["plan_digest"],
        "backup_id": backup_id,
        "already_applied": False,
        "mutation_performed": bool(planned_changes),
        "changed_files": planned_changes,
        "safety_profile": safety_profile,
    }


def write_repair_manifest(path: str | Path, manifest: Mapping[str, Any]) -> None:
    """Write an explicitly requested audit manifest with an atomic replacement."""

    destination = Path(path).absolute()
    if destination.is_symlink() or destination.parent.is_symlink():
        raise UnsafeStorePathError(f"repair manifest path must not be a symlink: {destination}")
    _atomic_json(destination, manifest)


__all__ = [
    "DEFAULT_CATEGORY_WHITELIST",
    "DEFAULT_SCENARIO_WHITELIST",
    "HistoricalRepairPlan",
    "PlannedDelete",
    "PlannedWrite",
    "apply_historical_repair_plan",
    "build_historical_repair_batch",
    "build_historical_repair_plan",
    "write_repair_manifest",
]
