from pathlib import Path

import pytest

from ai_stack.tag_taxonomy import (
    TaxonomyAliasError,
    compile_tag_aliases,
    load_tag_aliases,
    normalize_tag,
    normalize_tags,
)
from processor import taxonomy_normalizer as processor_compatibility

ROOT = Path(__file__).resolve().parent.parent


def test_processor_namespace_is_a_compatibility_forwarder():
    assert processor_compatibility.normalize_tag is normalize_tag
    assert processor_compatibility.normalize_tags is normalize_tags


def test_default_alias_config_is_versioned_and_applies_exact_aliases():
    aliases = load_tag_aliases(ROOT / "config" / "tag_aliases.yaml")

    assert aliases.version == 1
    assert normalize_tag("AI编程", aliases=aliases) == "AI 编程"
    assert normalize_tag("GPT 5.4", aliases=aliases) == "GPT-5.4"
    assert normalize_tag("Llama3.1", aliases=aliases) == "Llama 3.1"
    assert normalize_tag("arXiv", aliases=aliases) == "ArXiv"
    assert normalize_tags(["arXiv", "ArXiv"], aliases=aliases) == ["ArXiv"]


def test_normalization_is_nfc_whitespace_only_before_exact_alias_lookup():
    aliases = compile_tag_aliases({"AI 编程": "AI Engineering"})

    assert normalize_tag("  AI\t \n编程  ", aliases=aliases) == "AI Engineering"
    assert normalize_tag("Cafe\u0301", aliases={}) == "Café"


@pytest.mark.parametrize(
    "label",
    [
        "H²RL",
        "C",
        "C++",
        "C/C++",
        "CI/CD",
        "HTTP/2",
        "SE(3)",
        ".NET",
        "ReAct",
        "React",
    ],
)
def test_semantic_and_punctuation_exceptions_are_preserved(label):
    assert normalize_tag(label, aliases={}) == label


def test_normalize_tags_deduplicates_after_aliasing_and_is_idempotent():
    aliases = compile_tag_aliases(
        {
            "AI编程": "AI 编程",
            "AI Coding": "AI编程",
        }
    )

    normalized = normalize_tags(
        ["AI Coding", " AI编程 ", "AI 编程", "H²RL"],
        aliases=aliases,
    )

    assert normalized == ["AI 编程", "H²RL"]
    assert normalize_tags(normalized, aliases=aliases) == normalized


def test_semantically_distinct_case_variants_are_not_merged_by_default():
    aliases = load_tag_aliases(ROOT / "config" / "tag_aliases.yaml")

    assert normalize_tags(["XAI", "xAI"], aliases=aliases) == ["XAI", "xAI"]
    assert normalize_tags(["SWE-bench", "SWE-Bench"], aliases=aliases) == [
        "SWE-bench",
        "SWE-Bench",
    ]


def test_alias_compilation_rejects_cycles():
    with pytest.raises(TaxonomyAliasError, match="cycle"):
        compile_tag_aliases({"A": "B", "B": "A"})


def test_alias_compilation_rejects_ambiguous_normalized_sources():
    with pytest.raises(TaxonomyAliasError, match="multiple targets"):
        compile_tag_aliases({"Alias": "First", " Alias ": "Second"})


def test_alias_chains_resolve_to_one_terminal_target():
    aliases = compile_tag_aliases({"A": "B", "B": "Canonical"})

    assert aliases.mapping == {"A": "Canonical", "B": "Canonical"}
    assert normalize_tag(normalize_tag("A", aliases=aliases), aliases=aliases) == "Canonical"
