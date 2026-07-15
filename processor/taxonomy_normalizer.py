"""Deterministic, conservative taxonomy normalization.

Normalization deliberately stops at NFC, surrounding/internal whitespace, and
reviewed exact aliases. It must not guess semantic equivalence from casing or
punctuation because many technical labels differ only by those characters.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

TAG_ALIAS_CONFIG_VERSION = 1
DEFAULT_TAG_ALIAS_PATH = Path(__file__).resolve().parent.parent / "config" / "tag_aliases.yaml"


class TaxonomyAliasError(ValueError):
    """Raised when the reviewed alias registry is ambiguous or invalid."""


@dataclass(frozen=True)
class TagAliases:
    """A compiled alias registry whose values are terminal canonical labels."""

    version: int
    mapping: dict[str, str]


def _normalize_surface(value: Any) -> str:
    text = unicodedata.normalize("NFC", str(value or ""))
    return re.sub(r"\s+", " ", text).strip()


def compile_tag_aliases(
    raw_aliases: Mapping[str, str],
    *,
    version: int = TAG_ALIAS_CONFIG_VERSION,
) -> TagAliases:
    """Validate aliases and flatten chains to one deterministic terminal target."""
    if version != TAG_ALIAS_CONFIG_VERSION:
        raise TaxonomyAliasError(
            f"unsupported tag alias config version: {version}; "
            f"expected {TAG_ALIAS_CONFIG_VERSION}"
        )
    if not isinstance(raw_aliases, Mapping):
        raise TaxonomyAliasError("tag aliases must be a mapping")

    normalized: dict[str, str] = {}
    for raw_source, raw_target in raw_aliases.items():
        if not isinstance(raw_source, str) or not isinstance(raw_target, str):
            raise TaxonomyAliasError("tag alias sources and targets must be strings")
        source = _normalize_surface(raw_source)
        target = _normalize_surface(raw_target)
        if not source or not target:
            raise TaxonomyAliasError("tag alias sources and targets must be non-empty")
        previous = normalized.get(source)
        if previous is not None and previous != target:
            raise TaxonomyAliasError(
                f"tag alias {source!r} resolves to multiple targets: "
                f"{previous!r} and {target!r}"
            )
        normalized[source] = target

    resolved: dict[str, str] = {}

    def resolve(source: str, path: tuple[str, ...]) -> str:
        if source in resolved:
            return resolved[source]
        if source in path:
            cycle = " -> ".join((*path, source))
            raise TaxonomyAliasError(f"tag alias cycle detected: {cycle}")
        target = normalized[source]
        terminal = resolve(target, (*path, source)) if target in normalized else target
        resolved[source] = terminal
        return terminal

    for source in normalized:
        resolve(source, ())

    return TagAliases(version=version, mapping=resolved)


@lru_cache(maxsize=8)
def _load_tag_aliases_cached(path_text: str) -> TagAliases:
    path = Path(path_text)
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise TaxonomyAliasError(f"failed to load tag aliases from {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise TaxonomyAliasError("tag alias config must be a mapping")

    version = payload.get("version")
    aliases = payload.get("aliases") or {}
    exact = aliases.get("exact") if isinstance(aliases, dict) else None
    if not isinstance(version, int):
        raise TaxonomyAliasError("tag alias config requires an integer version")
    if not isinstance(exact, dict):
        raise TaxonomyAliasError("tag alias config requires aliases.exact mapping")
    return compile_tag_aliases(exact, version=version)


def load_tag_aliases(path: str | Path = DEFAULT_TAG_ALIAS_PATH) -> TagAliases:
    """Load and validate a versioned exact-alias registry."""
    return _load_tag_aliases_cached(str(Path(path).resolve()))


def _coerce_aliases(aliases: TagAliases | Mapping[str, str] | None) -> TagAliases:
    if aliases is None:
        return load_tag_aliases()
    if isinstance(aliases, TagAliases):
        return aliases
    return compile_tag_aliases(aliases)


def normalize_tag(
    value: Any,
    *,
    aliases: TagAliases | Mapping[str, str] | None = None,
) -> str:
    """Normalize one tag without case-folding or punctuation rewriting."""
    label = _normalize_surface(value)
    if not label:
        return ""
    registry = _coerce_aliases(aliases)
    return registry.mapping.get(label, label)


def normalize_tags(
    values: Any,
    *,
    aliases: TagAliases | Mapping[str, str] | None = None,
    limit: int | None = None,
) -> list[str]:
    """Normalize a tag list and stably de-duplicate after alias resolution."""
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, (list, tuple, set)):
        return []

    registry = _coerce_aliases(aliases)
    normalized: list[str] = []
    seen: set[str] = set()
    max_items = None if limit is None else max(0, int(limit))
    for value in values:
        label = normalize_tag(value, aliases=registry)
        if not label or label in seen:
            continue
        normalized.append(label)
        seen.add(label)
        if max_items is not None and len(normalized) >= max_items:
            break
    return normalized
