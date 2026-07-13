from __future__ import annotations

from datetime import datetime, timezone

import pytest

from ai_stack.identity import (
    CANONICALIZATION_VERSION,
    canonicalize_url,
    make_article_revision_id,
    make_entity_id,
    make_event_id,
    make_generation_key,
    make_item_id,
    make_revision_id,
)
from ai_stack.models import (
    ArticleRevision,
    Event,
    EventStatus,
    Evidence,
    OperationKind,
    OperationRecord,
    OperationStatus,
    Revision,
    RunManifest,
    SourceItem,
    StepResult,
    StepStatus,
    WorkflowStatus,
)


NOW = datetime(2026, 7, 13, 8, 0, tzinfo=timezone.utc)


def test_canonical_url_and_stable_ids_are_order_independent() -> None:
    first = "HTTPS://Example.COM:443/a/?b=2&utm_source=x&a=1#fragment"
    second = "https://example.com/a?a=1&b=2"

    assert canonicalize_url(first) == second
    assert make_item_id("GitHub", None, first) == make_item_id(
        "github", None, second
    )
    assert make_revision_id("itm_abc", {"b": 2, "a": 1}) == make_revision_id(
        "itm_abc", {"a": 1, "b": 2}
    )


def test_canonical_url_rejects_unsafe_or_ambiguous_inputs() -> None:
    for value in (
        "javascript:alert(1)",
        "ftp://example.com/file",
        "https://user:pass@example.com/private",
        "https:///missing-host",
    ):
        with pytest.raises(ValueError):
            canonicalize_url(value)

    with pytest.raises(ValueError, match="version"):
        canonicalize_url("https://example.com", version="future-v2")
    with pytest.raises(ValueError, match="port"):
        canonicalize_url("https://example.com:invalid")


def test_canonical_url_supports_idn_ipv6_and_non_default_ports() -> None:
    assert canonicalize_url("http://例子.测试:8080//a/../b") == (
        "http://xn--fsqu00a.xn--0zwm56d:8080/b"
    )
    assert canonicalize_url("https://[2001:db8::1]/") == "https://[2001:db8::1]"
    with pytest.raises(ValueError, match="source"):
        make_item_id("  ", None, "https://example.com")
    with pytest.raises(ValueError, match="entity"):
        make_entity_id("company", " ")
    with pytest.raises(ValueError, match="seed"):
        make_event_id(" ")


def test_all_identity_functions_are_deterministic_and_namespaced() -> None:
    revision_id = make_revision_id("itm_abc", {"title": "A"})
    generation_key = make_generation_key(revision_id, "model-x", "p1", "policy1")

    assert revision_id.startswith("rev_")
    assert generation_key.startswith("gen_")
    assert generation_key == make_generation_key(
        revision_id, "model-x", "p1", "policy1"
    )
    assert make_article_revision_id(generation_key, {"body": "text"}).startswith(
        "art_"
    )
    assert make_entity_id("company", " OpenAI  ") == make_entity_id(
        "COMPANY", "openai"
    )
    assert make_event_id("itm_seed") == make_event_id("itm_seed")


def test_source_item_normalizes_and_validates_derived_identity() -> None:
    item = SourceItem(
        source=" GitHub ",
        native_id=None,
        canonical_url="HTTPS://EXAMPLE.COM:443/repo/?utm_medium=social",
        fetched_at=NOW,
        payload={"stars": 42},
    )

    assert item.source == "github"
    assert item.canonical_url == "https://example.com/repo"
    assert item.canonicalization_version == CANONICALIZATION_VERSION
    assert item.item_id == make_item_id("github", None, item.canonical_url)
    with pytest.raises(TypeError):
        item.payload["stars"] = 43  # type: ignore[index]

    with pytest.raises(ValueError, match="item_id"):
        SourceItem(
            source="github",
            native_id=None,
            canonical_url="https://example.com/repo",
            fetched_at=NOW,
            payload={},
            item_id="itm_tampered",
        )


def test_domain_records_compute_ids_and_freeze_nested_payloads() -> None:
    revision = Revision(
        item_id="itm_seed",
        normalized_payload={"title": "Release", "tags": ["ai", "agent"]},
        source_snapshot_digest="sha256:" + "1" * 64,
        observed_at=NOW,
    )
    evidence = Evidence(
        source_url="https://example.com/release",
        snapshot_digest="sha256:" + "2" * 64,
        locator="README.md:L10-L12",
        excerpt="Version 2 was released.",
        claim_ids=("claim-1",),
        captured_at=NOW,
    )
    event = Event(
        seed_item_id="itm_seed",
        member_item_ids=("itm_seed",),
        first_seen=NOW,
        last_seen=NOW,
        status=EventStatus.ACTIVE,
    )
    generation_key = make_generation_key(revision.revision_id, "model", "p1", "v1")
    article = ArticleRevision(
        event_id=event.event_id,
        generation_key=generation_key,
        title="Release",
        body="Version 2 was released.",
        claims=({"claim_id": "claim-1", "evidence_ids": [evidence.evidence_id]},),
        inferences=(),
        evidence_ids=(evidence.evidence_id,),
        source_support=1.0,
        created_at=NOW,
    )

    assert revision.revision_id.startswith("rev_")
    assert revision.content_digest.startswith("sha256:")
    assert evidence.evidence_id.startswith("evd_")
    assert event.event_id == make_event_id("itm_seed")
    assert article.article_revision_id == make_article_revision_id(
        generation_key, article.generated_payload
    )
    with pytest.raises(TypeError):
        revision.normalized_payload["title"] = "Changed"  # type: ignore[index]


def test_domain_records_reject_invalid_time_ranges_and_support_score() -> None:
    naive = datetime(2026, 7, 13, 8, 0)
    with pytest.raises(ValueError, match="timezone"):
        Revision(
            item_id="itm_seed",
            normalized_payload={},
            source_snapshot_digest="sha256:" + "1" * 64,
            observed_at=naive,
        )
    with pytest.raises(ValueError, match="last_seen"):
        Event(
            seed_item_id="itm_seed",
            member_item_ids=("itm_seed",),
            first_seen=NOW,
            last_seen=datetime(2026, 7, 12, tzinfo=timezone.utc),
        )
    with pytest.raises(ValueError, match="source_support"):
        ArticleRevision(
            event_id="evt_seed",
            generation_key="gen_seed",
            title="Title",
            body="Body",
            source_support=1.01,
            created_at=NOW,
        )


def test_step_run_and_operation_records_use_explicit_states() -> None:
    step = StepResult(
        step="validate",
        status=StepStatus.SUCCEEDED,
        started_at=NOW,
        finished_at=NOW,
        output_digest="sha256:" + "3" * 64,
    )
    run = RunManifest(
        run_id="run-001",
        code_sha="a" * 40,
        content_parent_sha="b" * 40,
        input_digest="sha256:" + "4" * 64,
        config_digest="sha256:" + "5" * 64,
        model="model-x",
        status=WorkflowStatus.VALIDATED,
        steps=(step,),
        created_at=NOW,
        updated_at=NOW,
    )
    operation = OperationRecord(
        operation_id="op-001",
        kind=OperationKind.BUDGET_RESERVATION,
        status=OperationStatus.RESERVED,
        idempotency_key="generation-001",
        created_at=NOW,
        updated_at=NOW,
        token_limit=40_000,
        token_used=0,
        metadata={"run_id": run.run_id},
    )

    assert run.next_incomplete_step(("discover", "validate", "persist")) == "discover"
    assert operation.status is OperationStatus.RESERVED
    assert operation.metadata["run_id"] == "run-001"


def test_models_reject_tampered_digests_and_invalid_operation_counts() -> None:
    with pytest.raises(ValueError, match="source_snapshot_digest"):
        Revision(
            item_id="itm_seed",
            normalized_payload={},
            source_snapshot_digest="bad",
            observed_at=NOW,
        )
    with pytest.raises(ValueError, match="token_used"):
        OperationRecord(
            operation_id="op",
            kind=OperationKind.BUDGET_RESERVATION,
            status=OperationStatus.RESERVED,
            idempotency_key="key",
            created_at=NOW,
            updated_at=NOW,
            token_limit=1,
            token_used=2,
        )


def test_models_normalize_string_states_to_enums() -> None:
    event = Event(
        seed_item_id="itm_seed",
        member_item_ids=("itm_seed",),
        first_seen=NOW,
        last_seen=NOW,
        status="ACTIVE",  # type: ignore[arg-type]
    )
    step = StepResult(
        step="discover",
        status="SUCCEEDED",  # type: ignore[arg-type]
        started_at=NOW,
    )

    assert event.status is EventStatus.ACTIVE
    assert step.status is StepStatus.SUCCEEDED
