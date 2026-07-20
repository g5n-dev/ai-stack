#!/usr/bin/env python3
"""生成并校验绑定精确提交与公开数据树的发布标记。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath


class ReleaseMarkerError(ValueError):
    """发布标记或其引用的数据树不可信。"""


_FULL_SHA = re.compile(r"[0-9a-f]{40}\Z")
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_MARKER_FIELDS = frozenset(
    {
        "schema_version",
        "release_id",
        "exact_sha",
        "quality_hash",
        "lineage_hash",
        "graph_hash",
        "trends_hash",
        "generated_at",
        "lineage_mode",
    }
)
_MAX_JSON_BYTES = 16 * 1024 * 1024
_MAX_PRODUCT_FILES = 10_000


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _regular_bytes(path: Path) -> bytes:
    try:
        details = path.lstat()
    except OSError as exc:
        raise ReleaseMarkerError(f"required release file is missing: {path.name}") from exc
    if (
        path.is_symlink()
        or not stat.S_ISREG(details.st_mode)
        or details.st_nlink != 1
        or details.st_size > _MAX_JSON_BYTES
    ):
        raise ReleaseMarkerError(f"release file is not a bounded regular file: {path.name}")
    return path.read_bytes()


def _json_object(path: Path) -> tuple[dict[str, object], bytes]:
    body = _regular_bytes(path)
    try:
        value = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseMarkerError(f"release JSON is invalid: {path.name}") from exc
    if not isinstance(value, dict):
        raise ReleaseMarkerError(f"release JSON object required: {path.name}")
    return value, body


def _safe_reference(value: str) -> str:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or "\\" in value
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.suffix.casefold() != ".json"
    ):
        raise ReleaseMarkerError("unsafe JSON asset reference")
    return path.as_posix()


def _references(value: object) -> list[tuple[str, str | None]]:
    found: list[tuple[str, str | None]] = []
    if isinstance(value, Mapping):
        path_value = value.get("path")
        digest_value = value.get("sha256")
        if isinstance(path_value, str) and path_value.casefold().endswith(".json"):
            digest = digest_value.removeprefix("sha256:") if isinstance(digest_value, str) else None
            found.append((_safe_reference(path_value), digest))
        for key, child in value.items():
            if key in {"path", "sha256"}:
                continue
            found.extend(_references(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_references(child))
    elif isinstance(value, str) and value.casefold().endswith(".json"):
        found.append((_safe_reference(value), None))
    return found


def reachable_product_records(
    root: Path | str, *, reject_unreferenced: bool = True
) -> list[tuple[str, str]]:
    """返回从 index.json 可达的完整 JSON 清单，并验证内嵌摘要。"""

    product_root = Path(root)
    if product_root.is_symlink() or not product_root.is_dir():
        raise ReleaseMarkerError("release product root is missing")
    pending: list[tuple[str, str | None]] = [("index.json", None)]
    records: dict[str, str] = {}
    while pending:
        relative, expected = pending.pop(0)
        if relative in records:
            if expected and records[relative] != expected:
                raise ReleaseMarkerError(f"conflicting hash for release asset: {relative}")
            continue
        if len(records) >= _MAX_PRODUCT_FILES:
            raise ReleaseMarkerError("release product file-count limit exceeded")
        payload, body = _json_object(product_root / relative)
        digest = hashlib.sha256(body).hexdigest()
        if expected is not None and (
            not _DIGEST.fullmatch(expected) or digest != expected
        ):
            raise ReleaseMarkerError(f"embedded hash mismatch: {relative}")
        records[relative] = digest
        pending.extend(_references(payload))

    all_json = {
        path.relative_to(product_root).as_posix()
        for path in product_root.rglob("*.json")
        if path.is_file() and not path.is_symlink()
    }
    unreferenced = sorted(all_json.difference(records))
    if unreferenced and reject_unreferenced:
        raise ReleaseMarkerError(
            f"unreferenced release shards are forbidden: {unreferenced[:3]}"
        )
    return sorted(records.items())


def prune_unreferenced_product(root: Path | str) -> tuple[str, ...]:
    """只删除产品目录内未被 index.json 引用的 JSON 旧分片。"""

    product_root = Path(root)
    reachable = {
        path for path, _ in reachable_product_records(product_root, reject_unreferenced=False)
    }
    all_json = {
        path.relative_to(product_root).as_posix()
        for path in product_root.rglob("*.json")
        if path.is_file() and not path.is_symlink()
    }
    stale = tuple(sorted(all_json.difference(reachable)))
    for relative in stale:
        target = product_root.joinpath(*PurePosixPath(relative).parts)
        if target.is_symlink() or not target.is_file():
            raise ReleaseMarkerError("stale release shard changed before pruning")
        target.unlink()
    for directory in sorted(product_root.rglob("*"), reverse=True):
        if directory.is_dir() and not directory.is_symlink():
            try:
                directory.rmdir()
            except OSError:
                pass
    return stale


def reachable_product_hash(root: Path | str) -> str:
    return hashlib.sha256(_canonical_bytes(reachable_product_records(root))).hexdigest()


def _release_id(marker: Mapping[str, object]) -> str:
    identity = {key: marker[key] for key in sorted(_MARKER_FIELDS - {"release_id", "generated_at"})}
    return "r-" + hashlib.sha256(_canonical_bytes(identity)).hexdigest()[:24]


def build_release_marker(
    public_root: Path | str,
    *,
    exact_sha: str,
    require_lineage: bool = False,
) -> dict[str, str]:
    root = Path(public_root)
    if not _FULL_SHA.fullmatch(exact_sha):
        raise ReleaseMarkerError("exact Git SHA must be 40 lowercase hexadecimal characters")
    quality = hashlib.sha256(_regular_bytes(root / "data/content-quality.json")).hexdigest()
    graph = reachable_product_hash(root / "data/tag-graph")
    trends_root = root / "data/stack-trends"
    trends = reachable_product_hash(trends_root)
    trends_index, _ = _json_object(trends_root / "index.json")
    generated_at = trends_index.get("generated_at")
    lineage_mode = trends_index.get("lineage_mode", "unavailable")
    if not isinstance(generated_at, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", generated_at
    ):
        raise ReleaseMarkerError("trend generated_at must be canonical UTC")
    if not isinstance(lineage_mode, str) or not lineage_mode:
        raise ReleaseMarkerError("lineage mode is invalid")
    lineage_root = root / "data/lineage"
    if lineage_root.is_dir() and not lineage_root.is_symlink():
        lineage = reachable_product_hash(lineage_root)
    elif require_lineage:
        raise ReleaseMarkerError("lineage product is required")
    else:
        lineage = "unavailable"
        lineage_mode = "unavailable"
    marker: dict[str, str] = {
        "schema_version": "ai_stack_release_v1",
        "release_id": "",
        "exact_sha": exact_sha,
        "quality_hash": quality,
        "lineage_hash": lineage,
        "graph_hash": graph,
        "trends_hash": trends,
        "generated_at": generated_at,
        "lineage_mode": lineage_mode,
    }
    marker["release_id"] = _release_id(marker)
    return marker


def verify_release_marker(
    public_root: Path | str,
    marker: Mapping[str, object],
    *,
    expected_sha: str,
    require_lineage: bool = False,
) -> dict[str, str]:
    if frozenset(marker) != _MARKER_FIELDS:
        raise ReleaseMarkerError("release marker fields do not match schema")
    if marker.get("schema_version") != "ai_stack_release_v1":
        raise ReleaseMarkerError("release marker schema is unsupported")
    expected = build_release_marker(
        public_root,
        exact_sha=expected_sha,
        require_lineage=require_lineage,
    )
    if dict(marker) != expected:
        raise ReleaseMarkerError("release marker hash or identity mismatch")
    return expected


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            temporary = handle.name
            os.chmod(handle.name, 0o600)
            handle.write(_canonical_bytes(value) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create")
    create.add_argument("--public-root", type=Path, required=True)
    create.add_argument("--exact-sha", required=True)
    create.add_argument("--output", type=Path, required=True)
    create.add_argument("--require-lineage", action="store_true")
    verify = commands.add_parser("verify")
    verify.add_argument("--public-root", type=Path, required=True)
    verify.add_argument("--marker", type=Path, required=True)
    verify.add_argument("--expected-sha", required=True)
    verify.add_argument("--require-lineage", action="store_true")
    prune = commands.add_parser("prune-product")
    prune.add_argument("--root", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "prune-product":
            removed = prune_unreferenced_product(args.root)
            marker = {"removed": len(removed)}
        elif args.command == "create":
            marker = build_release_marker(
                args.public_root,
                exact_sha=args.exact_sha,
                require_lineage=args.require_lineage,
            )
            _atomic_json(args.output, marker)
        else:
            marker, _ = _json_object(args.marker)
            marker = verify_release_marker(
                args.public_root,
                marker,
                expected_sha=args.expected_sha,
                require_lineage=args.require_lineage,
            )
    except (OSError, ReleaseMarkerError) as exc:
        print(f"release-marker: {exc}", file=os.sys.stderr)
        return 2
    print(_canonical_bytes(marker).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
