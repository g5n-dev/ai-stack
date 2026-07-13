"""Offline related-post index with deterministic O(1) route lookup."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

import yaml  # type: ignore[import-untyped]


SCHEMA_VERSION = "related_index_v1"
CONTROL_CHARACTER_RE = re.compile(r"[\x00-\x1f\x7f]")
MAX_FRONTMATTER_BYTES = 65_536


class RelatedIndexValidationError(ValueError):
    """Raised when content metadata cannot safely produce a stable index."""


@dataclass(frozen=True)
class PostRecord:
    post_id: str
    route: str
    title: str
    published_at: datetime
    tags: tuple[str, ...]

    def identity_payload(self) -> dict[str, Any]:
        return {
            "id": self.post_id,
            "route": self.route,
            "title": self.title,
            "published_at": _format_timestamp(self.published_at),
            "tags": list(self.tags),
        }


def _stable_json_bytes(value: Any) -> bytes:
    try:
        serialized = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise RelatedIndexValidationError(f"index is not deterministic JSON: {exc}") from exc
    return f"{serialized}\n".encode("utf-8")


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_timestamp(value: Any, *, source: Path) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = f"{normalized[:-1]}+00:00"
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise RelatedIndexValidationError(f"invalid date in {source.name}") from exc
    else:
        raise RelatedIndexValidationError(f"missing date in {source.name}")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RelatedIndexValidationError(f"date requires timezone in {source.name}")
    return parsed.astimezone(timezone.utc)


def _read_frontmatter(path: Path) -> dict[str, Any]:
    frontmatter_lines: list[str] = []
    frontmatter_bytes = 0
    with path.open("r", encoding="utf-8") as source_file:
        if source_file.readline().strip() != "---":
            raise RelatedIndexValidationError(f"missing YAML frontmatter in {path.name}")
        for line in source_file:
            if line.strip() == "---":
                break
            frontmatter_bytes += len(line.encode("utf-8"))
            if frontmatter_bytes > MAX_FRONTMATTER_BYTES:
                raise RelatedIndexValidationError(f"frontmatter too large in {path.name}")
            frontmatter_lines.append(line)
        else:
            raise RelatedIndexValidationError(f"unterminated YAML frontmatter in {path.name}")
    try:
        metadata = yaml.safe_load("".join(frontmatter_lines)) or {}
    except yaml.YAMLError as exc:
        raise RelatedIndexValidationError(f"invalid YAML frontmatter in {path.name}") from exc
    if not isinstance(metadata, Mapping):
        raise RelatedIndexValidationError(f"frontmatter must be an object in {path.name}")
    return dict(metadata)


def _safe_text(value: Any, *, field: str, source: Path, maximum: int = 500) -> str:
    if not isinstance(value, str):
        raise RelatedIndexValidationError(f"{field} must be a string in {source.name}")
    normalized = unicodedata.normalize("NFKC", value).strip()
    if not normalized or len(normalized) > maximum or CONTROL_CHARACTER_RE.search(normalized):
        raise RelatedIndexValidationError(f"invalid {field} in {source.name}")
    return normalized


def _normalize_tags(value: Any, *, source: Path) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise RelatedIndexValidationError(f"tags must be an array in {source.name}")
    tags: set[str] = set()
    for raw_tag in value:
        tag = _safe_text(raw_tag, field="tag", source=source, maximum=100).casefold()
        tags.add(tag)
    return tuple(sorted(tags))


def _normalize_route(value: str, *, source: Path) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise RelatedIndexValidationError(f"route must be a local path in {source.name}")
    if "\\" in parsed.path or CONTROL_CHARACTER_RE.search(parsed.path):
        raise RelatedIndexValidationError(f"unsafe route in {source.name}")
    route = f"/{parsed.path.lstrip('/')}"
    parts = PurePosixPath(route).parts
    if ".." in parts:
        raise RelatedIndexValidationError(f"route traversal in {source.name}")
    route = re.sub(r"/{2,}", "/", route)
    if not PurePosixPath(route).suffix and not route.endswith("/"):
        route = f"{route}/"
    return route


def _derived_route(
    path: Path,
    content_dir: Path,
    metadata: Mapping[str, Any],
    *,
    section: str,
) -> str:
    explicit_route = metadata.get("url") or metadata.get("permalink")
    if explicit_route is not None:
        if not isinstance(explicit_route, str):
            raise RelatedIndexValidationError(f"url must be a string in {path.name}")
        return _normalize_route(explicit_route, source=path)

    relative = path.relative_to(content_dir)
    if relative.name == "index.md":
        route_parts = relative.parent.parts
    else:
        route_parts = relative.with_suffix("").parts
    slug = metadata.get("slug")
    if slug is not None:
        safe_slug = _safe_text(slug, field="slug", source=path, maximum=200)
        if "/" in safe_slug or "\\" in safe_slug or safe_slug in {".", ".."}:
            raise RelatedIndexValidationError(f"invalid slug in {path.name}")
        route_parts = (*relative.parent.parts, safe_slug)
    route = "/".join((section.strip("/"), *route_parts))
    return _normalize_route(route, source=path)


def _post_id(metadata: Mapping[str, Any], route: str, *, source: Path) -> str:
    for field in ("event_id", "article_revision_id", "item_id", "id"):
        if field in metadata and metadata[field] is not None:
            return _safe_text(metadata[field], field=field, source=source, maximum=300)
    return f"post-{hashlib.sha256(route.encode('utf-8')).hexdigest()[:20]}"


def _load_posts(content_dir: Path, *, section: str) -> list[PostRecord]:
    if not content_dir.is_dir():
        raise RelatedIndexValidationError(f"content directory not found: {content_dir}")
    records: list[PostRecord] = []
    seen_ids: set[str] = set()
    seen_routes: set[str] = set()
    for path in sorted(content_dir.rglob("*.md")):
        if path.name == "_index.md":
            continue
        metadata = _read_frontmatter(path)
        if metadata.get("draft", False) is True:
            continue
        route = _derived_route(path, content_dir, metadata, section=section)
        post_id = _post_id(metadata, route, source=path)
        if route in seen_routes:
            raise RelatedIndexValidationError(f"duplicate route: {route}")
        if post_id in seen_ids:
            raise RelatedIndexValidationError(f"duplicate post id: {post_id}")
        seen_routes.add(route)
        seen_ids.add(post_id)
        records.append(
            PostRecord(
                post_id=post_id,
                route=route,
                title=_safe_text(metadata.get("title"), field="title", source=path),
                published_at=_parse_timestamp(metadata.get("date"), source=path),
                tags=_normalize_tags(metadata.get("tags"), source=path),
            )
        )
    return sorted(records, key=lambda post: post.route)


def _candidate_sets(
    posts: list[PostRecord],
    *,
    candidate_window: int,
) -> dict[str, set[str]]:
    by_id = {post.post_id: post for post in posts}
    tag_buckets: defaultdict[str, list[str]] = defaultdict(list)
    for post in posts:
        for tag in post.tags:
            tag_buckets[tag].append(post.post_id)
    for tag in tag_buckets:
        tag_buckets[tag].sort(
            key=lambda post_id: (
                -by_id[post_id].published_at.timestamp(),
                by_id[post_id].route,
            )
        )

    candidates: dict[str, set[str]] = {post.post_id: set() for post in posts}
    for bucket in tag_buckets.values():
        for index, post_id in enumerate(bucket):
            start = max(0, index - candidate_window)
            end = min(len(bucket), index + candidate_window + 1)
            candidates[post_id].update(bucket[start:end])
            candidates[post_id].discard(post_id)
    return candidates


def _related_entries(
    posts: list[PostRecord],
    *,
    max_related: int,
    candidate_window: int,
) -> dict[str, list[dict[str, Any]]]:
    by_id = {post.post_id: post for post in posts}
    candidates = _candidate_sets(posts, candidate_window=candidate_window)
    result: dict[str, list[dict[str, Any]]] = {}
    for post in posts:
        ranked: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        post_tags = set(post.tags)
        for candidate_id in candidates[post.post_id]:
            candidate = by_id[candidate_id]
            shared_tags = sorted(post_tags.intersection(candidate.tags))
            if not shared_tags:
                continue
            distance_seconds = abs((post.published_at - candidate.published_at).total_seconds())
            entry = {
                "id": candidate.post_id,
                "route": candidate.route,
                "title": candidate.title,
                "published_at": _format_timestamp(candidate.published_at),
                "shared_tags": shared_tags,
                "shared_tag_count": len(shared_tags),
            }
            rank = (
                -len(shared_tags),
                distance_seconds,
                -candidate.published_at.timestamp(),
                candidate.route,
            )
            ranked.append((rank, entry))
        ranked.sort(key=lambda item: item[0])
        result[post.route] = [entry for _, entry in ranked[:max_related]]
    return result


def _write_atomic(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        os.fchmod(file_descriptor, 0o644)
        with os.fdopen(file_descriptor, "wb") as temporary_file:
            temporary_file.write(body)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def build_related_index(
    content_dir: str | Path,
    *,
    output_path: str | Path | None = None,
    section: str = "posts",
    max_related: int = 6,
    candidate_window: int = 100,
) -> dict[str, Any]:
    """Build related metadata without scanning every post for every page.

    Candidate discovery is bounded to neighboring posts in each inverted tag
    bucket, keeping generation proportional to posts × tags × candidate_window.
    """

    if not isinstance(max_related, int) or isinstance(max_related, bool) or max_related < 0:
        raise RelatedIndexValidationError("max_related must be a non-negative integer")
    if (
        not isinstance(candidate_window, int)
        or isinstance(candidate_window, bool)
        or candidate_window < 1
    ):
        raise RelatedIndexValidationError("candidate_window must be a positive integer")
    normalized_section = section.strip("/")
    if not normalized_section or "/" in normalized_section or "\\" in normalized_section:
        raise RelatedIndexValidationError("section must be one safe path segment")

    posts = _load_posts(Path(content_dir), section=normalized_section)
    identity = [post.identity_payload() for post in posts]
    content_digest = hashlib.sha256(_stable_json_bytes(identity)).hexdigest()
    related = _related_entries(
        posts,
        max_related=max_related,
        candidate_window=candidate_window,
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "content_sha256": content_digest,
        "data_as_of": _format_timestamp(max(post.published_at for post in posts)) if posts else None,
        "post_count": len(posts),
        "max_related": max_related,
        "candidate_window": candidate_window,
        "by_id": {post.post_id: post.route for post in posts},
        "by_route": related,
    }
    if output_path is not None:
        _write_atomic(Path(output_path), _stable_json_bytes(payload))
    return payload


__all__ = [
    "RelatedIndexValidationError",
    "SCHEMA_VERSION",
    "build_related_index",
]
