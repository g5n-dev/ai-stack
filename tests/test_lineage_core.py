from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from ai_stack.lineage import (
    Fingerprint,
    LineageConfig,
    LineageRegistry,
    ObservationInput,
    RelationKind,
    RelationshipDecision,
    TimestampConfidence,
    apply_suppression_circuit_breaker,
    build_shingles,
    classify_relationship,
    fingerprint_text,
    make_lineage_event_id,
    make_lineage_revision_id,
    make_observation_id,
    normalize_source_text,
    observation_from_contract,
)


def _words(start: int, stop: int) -> str:
    return " ".join(f"signal{index}" for index in range(start, stop))


def _observation(
    *,
    url: str,
    title: str,
    text: str,
    published_at: str | None = "2026-07-01T08:00:00Z",
    first_seen_at: str = "2026-07-01T09:00:00Z",
    capture_mode: str = "full_text",
    completeness: str = "complete",
    truncated: bool = False,
    confidence: TimestampConfidence = TimestampConfidence.PUBLISHER,
) -> ObservationInput:
    return ObservationInput(
        canonical_url=url,
        title=title,
        source_text=text,
        source="fixture",
        article_path="blog/content/posts/fixture.md",
        capture_mode=capture_mode,
        source_completeness=completeness,
        source_is_truncated=truncated,
        source_published_at=published_at,
        first_seen_at=first_seen_at,
        last_seen_at="2026-07-01T00:00:00Z",
        timestamp_confidence=confidence,
    )


def test_stable_lineage_ids_use_canonical_url_and_normalized_source_digest() -> None:
    first = make_observation_id("HTTPS://Example.com:443/news/?utm_source=feed&b=2&a=1#x")
    second = make_observation_id("https://example.com/news?a=1&b=2")

    assert first == second
    assert first.startswith("obs_")
    assert len(first) == 68

    revision = make_lineage_revision_id(first, "sha256:" + "a" * 64)
    assert revision == make_lineage_revision_id(first, "sha256:" + "a" * 64)
    assert revision != make_lineage_revision_id(first, "sha256:" + "b" * 64)
    assert make_lineage_event_id(first) == make_lineage_event_id(first)


def test_source_normalization_is_unicode_html_url_and_boilerplate_stable() -> None:
    raw = """
    <nav>HOME / About / RSS</nav>
    <p>ＡＩ&nbsp;Agent 访问 HTTPS://EXAMPLE.COM/a?utm_source=x。</p>
    <p>OpenAI BUILDS Reliable Agents.</p>
    免责声明：本文仅代表作者观点
    """

    normalized = normalize_source_text(raw)

    assert "ai agent" in normalized
    assert "openai builds reliable agents" in normalized
    assert "http" not in normalized
    assert "免责声明" not in normalized
    assert "home" not in normalized


def test_shingles_use_chinese_four_grams_and_english_word_three_grams() -> None:
    shingles = build_shingles("人工智能推动软件工程 OpenAI builds reliable agents safely")

    assert "zh:人工智能" in shingles
    assert "zh:工智能推" in shingles
    assert "en:openai\x1fbuilds\x1freliable" in shingles
    assert "en:reliable\x1fagents\x1fsafely" in shingles


def test_fingerprint_has_fixed_bitmap_simhash_and_bounded_kmv() -> None:
    fingerprint = fingerprint_text(_words(0, 600))

    assert isinstance(fingerprint, Fingerprint)
    assert fingerprint.normalized_digest.startswith("sha256:")
    assert len(fingerprint.bitmap_hex) == 1024
    assert len(fingerprint.simhash_hex) == 64
    assert len(fingerprint.kmv) == 256
    assert fingerprint.shingle_count <= 4096
    assert "signal" not in repr(fingerprint)


def test_exact_copy_requires_substantial_non_metadata_evidence_and_title_alignment() -> None:
    text = _words(0, 180)
    left = _observation(
        url="https://publisher.example/launch",
        title="OpenAI Agent 平台正式发布",
        text=text,
    )
    right = _observation(
        url="https://mirror.example/launch",
        title="OpenAI Agent 平台正式发布",
        text=text,
        published_at="2026-07-01T08:10:00Z",
    )

    decision = classify_relationship(left, right)

    assert decision.relation is RelationKind.EXACT_COPY
    assert decision.suppression_eligible is True
    assert decision.parent_observation_id == left.observation_id
    assert decision.jaccard == pytest.approx(1.0)


def test_syndicated_copy_is_high_confidence_bidirectional_overlap() -> None:
    left = _observation(
        url="https://publisher.example/story",
        title="Agent Runtime reaches production",
        text=_words(0, 220),
    )
    right = _observation(
        url="https://syndicator.example/story",
        title="Agent Runtime reaches production",
        text=_words(0, 223),
        published_at="2026-07-01T10:00:00Z",
    )

    decision = classify_relationship(left, right)

    assert decision.relation is RelationKind.SYNDICATED
    assert decision.suppression_eligible is True
    assert decision.jaccard >= 0.92
    assert min(decision.left_containment, decision.right_containment) >= 0.96
    assert decision.confidence >= 0.98


def test_derivative_keeps_its_own_event_and_points_to_reliable_earlier_parent() -> None:
    original = _observation(
        url="https://publisher.example/research",
        title="Research Agent architecture",
        text=_words(0, 150),
        published_at="2026-07-01T08:00:00Z",
    )
    analysis = _observation(
        url="https://analyst.example/research-explained",
        title="Research Agent architecture explained",
        text=_words(0, 300),
        published_at="2026-07-02T08:00:00Z",
    )

    decision = classify_relationship(original, analysis)

    assert decision.relation is RelationKind.DERIVATIVE
    assert decision.suppression_eligible is False
    assert decision.parent_observation_id == original.observation_id
    assert decision.common_shingles >= 80
    assert decision.left_containment >= 0.72
    assert decision.right_containment < 0.72


def test_same_event_is_shadow_only_and_requires_time_title_and_two_signals() -> None:
    first = _observation(
        url="https://news-a.example/gpt6",
        title="OpenAI 发布 GPT-6 模型，性能提升 2 倍",
        text="alpha beta gamma delta epsilon",
    )
    second = _observation(
        url="https://news-b.example/gpt6",
        title="OpenAI 发布 GPT-6 模型：性能提升 2倍",
        text="different reporting with independent interviews and context",
        published_at="2026-07-03T07:00:00Z",
    )

    decision = classify_relationship(first, second)

    assert decision.relation is RelationKind.SAME_EVENT
    assert decision.suppression_eligible is False
    assert decision.shared_signals >= 2


@pytest.mark.parametrize(
    ("capture_mode", "completeness", "truncated"),
    [
        ("metadata_only", "metadata_only", False),
        ("excerpt", "partial", True),
        ("title_only", "metadata_only", False),
    ],
)
def test_incomplete_evidence_never_triggers_approximate_suppression(
    capture_mode: str, completeness: str, truncated: bool
) -> None:
    left = _observation(
        url="https://one.example/story",
        title="One source",
        text=_words(0, 220),
    )
    right = _observation(
        url="https://two.example/story",
        title="Another source",
        text=_words(0, 223),
        capture_mode=capture_mode,
        completeness=completeness,
        truncated=truncated,
    )

    decision = classify_relationship(left, right)

    assert decision.relation is not RelationKind.SYNDICATED
    assert decision.suppression_eligible is False


def test_circuit_breaker_disables_cross_url_suppression_for_absolute_or_ratio_burst() -> None:
    template = RelationshipDecision(
        relation=RelationKind.SYNDICATED,
        confidence=0.99,
        jaccard=0.99,
        left_containment=1.0,
        right_containment=0.99,
        common_shingles=100,
        shared_signals=2,
        parent_observation_id="obs_parent",
        suppression_eligible=True,
        reason="fixture",
    )
    decisions = [replace(template, reason=f"fixture-{index}") for index in range(11)]

    result = apply_suppression_circuit_breaker(decisions, new_observation_count=40)

    assert result.tripped is True
    assert result.reason == "absolute_limit"
    assert all(not decision.suppression_eligible for decision in result.decisions)

    ratio = apply_suppression_circuit_breaker(decisions[:4], new_observation_count=10)
    assert ratio.tripped is True
    assert ratio.reason == "ratio_limit"


def test_config_rejects_unsafe_limits() -> None:
    with pytest.raises(ValueError, match="shard_count"):
        LineageConfig(shard_count=0)


def test_contract_adapter_uses_verified_original_source_text_and_timestamps() -> None:
    contracted = {
        "source": "blogs_podcasts",
        "title": "Agent evidence",
        "url": "https://example.com/agent?utm_source=feed",
        "source_text_original": "Verified source evidence only.",
        "source_capture_mode": "full_article",
        "source_completeness": "complete",
        "source_is_truncated": False,
        "source_payload_sha256": "sha256:" + "a" * 64,
        "source_published_at": "2026-07-01T08:00:00Z",
        "timestamp_confidence": "publisher",
        "first_seen_at": "2026-07-01T09:00:00Z",
    }

    observation = observation_from_contract(
        contracted,
        article_path="blog/content/posts/agent.md",
        last_seen_at="2026-07-20T00:00:00Z",
    )

    assert observation.canonical_url == "https://example.com/agent"
    assert observation.source_text == "Verified source evidence only."
    assert observation.source_published_at == "2026-07-01T08:00:00Z"
    assert observation.timestamp_confidence is TimestampConfidence.PUBLISHER
    assert observation.article_url == "/posts/agent/"


def test_registry_resolves_baseline_suppression_derivative_and_stable_event() -> None:
    original = _observation(
        url="https://origin.example/agent",
        title="Agent Runtime architecture",
        text=_words(0, 150),
    )
    copy = _observation(
        url="https://mirror.example/agent",
        title="Agent Runtime architecture",
        text=_words(0, 150),
        published_at="2026-07-01T10:00:00Z",
    )
    derivative = _observation(
        url="https://analysis.example/agent",
        title="Agent Runtime architecture explained",
        text=_words(0, 300),
        published_at="2026-07-02T10:00:00Z",
    )
    registry = LineageRegistry()

    batch = registry.resolve_batch(
        [copy, derivative],
        historical_baseline=[original],
    )

    copy_result, derivative_result = batch.items
    assert copy_result.relation is RelationKind.EXACT_COPY
    assert copy_result.suppress is True
    assert copy_result.event_id == make_lineage_event_id(original.observation_id)
    assert copy_result.parent_observation_id == original.observation_id
    assert derivative_result.relation is RelationKind.DERIVATIVE
    assert derivative_result.suppress is False
    assert derivative_result.event_id == make_lineage_event_id(derivative.observation_id)
    assert batch.stats["suppressed"] == 1
    assert batch.circuit_breaker.tripped is False


def test_registry_persists_suppressed_observation_without_source_text_and_reloads(
    tmp_path: Path,
) -> None:
    root = tmp_path / "registry"
    original = _observation(
        url="https://origin.example/persisted",
        title="Persistent Agent source",
        text=_words(0, 180),
    )
    copy = _observation(
        url="https://mirror.example/persisted",
        title="Persistent Agent source",
        text=_words(0, 180),
        published_at="2026-07-01T10:00:00Z",
    )
    registry = LineageRegistry()
    registry.resolve_batch([copy], historical_baseline=[original])
    registry.save(root, generated_at="2026-07-20T00:00:00Z")

    payload = b"".join(path.read_bytes() for path in root.rglob("*.json"))
    assert b"signal100" not in payload
    assert b"shingle_hashes" not in payload

    reloaded = LineageRegistry.load(root)
    later = _observation(
        url="https://later.example/persisted",
        title="Persistent Agent source",
        text=_words(0, 180),
        published_at="2026-07-02T10:00:00Z",
    )
    result = reloaded.resolve_batch([later]).items[0]
    assert result.relation is RelationKind.EXACT_COPY
    assert result.suppress is True
    assert result.event_id == make_lineage_event_id(original.observation_id)


def test_registry_requires_current_memory_exact_shingles_for_approximate_suppression(
    tmp_path: Path,
) -> None:
    root = tmp_path / "registry"
    original = _observation(
        url="https://origin.example/compact-fingerprint",
        title="Agent Runtime reaches production",
        text=_words(0, 220),
    )
    registry = LineageRegistry()
    registry.resolve_batch([], historical_baseline=[original])
    registry.save(root, generated_at="2026-07-20T00:00:00Z")

    syndicated = _observation(
        url="https://mirror.example/compact-fingerprint",
        title="Agent Runtime reaches production",
        text=_words(0, 223),
        published_at="2026-07-01T10:00:00Z",
    )
    compact_only = LineageRegistry.load(root).resolve_batch([syndicated]).items[0]
    with_exact_baseline = LineageRegistry.load(root).resolve_batch(
        [syndicated], historical_baseline=[original]
    ).items[0]

    assert compact_only.relation is not RelationKind.SYNDICATED
    assert compact_only.suppress is False
    assert with_exact_baseline.relation is RelationKind.SYNDICATED
    assert with_exact_baseline.suppress is True


def test_batch_removes_high_frequency_template_shingles_before_final_classification() -> None:
    shared_template = _words(0, 180)
    baseline = [
        _observation(
            url=f"https://publisher{index}.example/template",
            title="Agent Runtime template report",
            text=f"{shared_template} unique publisher tail {index}",
        )
        for index in range(20)
    ]
    new_observation = _observation(
        url="https://new.example/template",
        title="Agent Runtime template report",
        text=f"{shared_template} independent reporting tail latest",
        published_at="2026-07-01T10:00:00Z",
    )

    result = LineageRegistry().resolve_batch(
        [new_observation], historical_baseline=baseline
    ).items[0]

    assert result.relation not in {RelationKind.EXACT_COPY, RelationKind.SYNDICATED}
    assert result.suppress is False


def test_registry_circuit_breaker_keeps_relationship_but_disables_suppression() -> None:
    original = _observation(
        url="https://origin.example/burst",
        title="Agent burst",
        text=_words(0, 180),
    )
    copies = [
        _observation(
            url=f"https://mirror{index}.example/burst",
            title="Agent burst",
            text=_words(0, 180),
            published_at=f"2026-07-01T{10 + index:02d}:00:00Z",
        )
        for index in range(2)
    ]
    registry = LineageRegistry(
        config=LineageConfig(suppression_absolute_limit=1, suppression_ratio_limit=1.0)
    )

    batch = registry.resolve_batch(copies, historical_baseline=[original])

    assert batch.circuit_breaker.tripped is True
    assert batch.circuit_breaker.reason == "absolute_limit"
    assert all(item.relation is RelationKind.EXACT_COPY for item in batch.items)
    assert all(item.suppress is False for item in batch.items)
    assert batch.stats["suppressed"] == 0


def test_registry_same_url_new_revision_updates_without_self_duplicate_or_suppression(
    tmp_path: Path,
) -> None:
    root = tmp_path / "registry"
    original = _observation(
        url="https://origin.example/revision",
        title="Agent revision",
        text=_words(0, 180),
    )
    registry = LineageRegistry()
    first = registry.resolve_batch([original]).items[0]
    registry.save(root, generated_at="2026-07-20T00:00:00Z")
    reloaded = LineageRegistry.load(root)
    revised = replace(
        original,
        source_text=_words(0, 200),
        last_seen_at="2026-07-21T00:00:00Z",
    )

    result = reloaded.resolve_batch([revised]).items[0]

    assert result.observation_id == first.observation_id
    assert result.event_id == first.event_id
    assert result.revision_id != first.revision_id
    assert result.relation is RelationKind.ORIGINAL
    assert result.parent_observation_id is None
    assert result.suppress is False
