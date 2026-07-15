"""Backward-compatible import surface for the shared tag taxonomy."""

from ai_stack.tag_taxonomy import (
    DEFAULT_TAG_ALIAS_PATH,
    TAG_ALIAS_CONFIG_VERSION,
    TagAliases,
    TaxonomyAliasError,
    compile_tag_aliases,
    load_tag_aliases,
    normalize_tag,
    normalize_tags,
)

__all__ = [
    "DEFAULT_TAG_ALIAS_PATH",
    "TAG_ALIAS_CONFIG_VERSION",
    "TagAliases",
    "TaxonomyAliasError",
    "compile_tag_aliases",
    "load_tag_aliases",
    "normalize_tag",
    "normalize_tags",
]
