"""Public lineage assets must stay a closed graph after budget retention.

INCIDENT-2026-10-05 backfill: a month of new Posts pushed the public lineage
assets close to their byte ceiling. Retiring the oldest events left surviving
members pointing at parents that were no longer published. Hash verification
passed, but build_stack_trends (correctly) failed the release with
"lineage parent is missing". The fix belongs in the generator and the verifier,
not in weakening the trend validator.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_stack.lineage import (
    LineageValidationError,
    RelationKind,
    _public_cluster_entry,
    _verify_published_parents,
)

ROOT = Path(__file__).resolve().parent.parent


def _record(observation_id: str, *, parent: str | None = None) -> dict[str, object]:
    return {
        "article_url": "/posts/fixture/",
        "canonical_url": "https://example.com/fixture",
        "event_id": "evt_fixture",
        "first_seen_at": "2026-01-01T00:00:00Z",
        "observation_id": observation_id,
        "parent_observation_id": parent,
        "relation": RelationKind.RELATED_ONLY.value,
        "source": "fixture",
        "source_published_at": "2026-01-01T00:00:00Z",
        "timestamp_confidence": "publisher",
        "title": "fixture",
    }


def _event(members: list[str]) -> dict[str, object]:
    return {
        "earliest_observed_id": members[0],
        "event_aliases": [],
        "event_id": "evt_fixture",
        "members": members,
        "probable_origin_id": members[0],
        "representative_observation_id": members[0],
    }


def test_retired_parent_is_degraded_to_a_root() -> None:
    records = {
        "obs_a": _record("obs_a"),
        "obs_b": _record("obs_b", parent="obs_retired"),
    }

    entry = _public_cluster_entry("evt_fixture", _event(["obs_a", "obs_b"]), records)

    parents = {item["observation_id"]: item["parent_observation_id"] for item in entry["observations"]}
    assert parents == {"obs_a": None, "obs_b": None}
    # A retired parent must not be offered as a visible lineage link either.
    assert entry["lineage_links"] == []


def test_a_published_parent_is_preserved() -> None:
    records = {
        "obs_a": _record("obs_a"),
        "obs_b": _record("obs_b", parent="obs_a"),
    }

    entry = _public_cluster_entry("evt_fixture", _event(["obs_a", "obs_b"]), records)

    parents = {item["observation_id"]: item["parent_observation_id"] for item in entry["observations"]}
    assert parents["obs_b"] == "obs_a"


def test_verifier_rejects_a_dangling_parent() -> None:
    with pytest.raises(LineageValidationError, match="lineage parent is not published"):
        _verify_published_parents([("obs_b", "obs_retired")], {"obs_a", "obs_b"})


def test_verifier_accepts_a_closed_graph() -> None:
    _verify_published_parents([("obs_b", "obs_a")], {"obs_a", "obs_b"})


def test_hash_only_verification_is_no_longer_the_only_guard() -> None:
    source = (ROOT / "ai_stack" / "lineage.py").read_text(encoding="utf-8")

    assert "def _verify_published_parents" in source
    assert "lineage parent is not published" in source
    assert "_verify_published_parents(parent_references, observations)" in source


def test_downstream_trend_validation_stays_fail_closed() -> None:
    """Do not 'fix' this by relaxing the consumer of the public assets."""

    source = (ROOT / "processor" / "stack_trends.py").read_text(encoding="utf-8")

    assert "lineage parent is missing" in source


def test_new_guard_is_registered_in_ci() -> None:
    source = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "tests/test_lineage_retention_parents.py" in source
