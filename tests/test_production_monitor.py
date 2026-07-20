from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from urllib.parse import urlsplit

import pytest

from scripts.production_monitor import (
    MonitoringError,
    evaluate_production_state,
    verify_production_sample,
)


NOW = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)


def _marker(*, sha: str = "a" * 40, generated_at: str = "2026-07-20T08:00:00Z") -> dict[str, str]:
    marker = {
        "schema_version": "ai_stack_release_v1",
        "release_id": "",
        "exact_sha": sha,
        "quality_hash": "1" * 64,
        "lineage_hash": "2" * 64,
        "graph_hash": "3" * 64,
        "trends_hash": "4" * 64,
        "generated_at": generated_at,
        "lineage_mode": "lineage_index_v1",
    }
    identity = {
        key: marker[key]
        for key in sorted(set(marker) - {"release_id", "generated_at"})
    }
    marker["release_id"] = "r-" + hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:24]
    return marker


def test_monitor_accepts_recent_release_and_short_main_divergence() -> None:
    assert evaluate_production_state(
        _marker(),
        main_sha="a" * 40,
        main_committed_at="2026-07-20T07:00:00Z",
        now=NOW,
    )["status"] == "healthy"
    assert evaluate_production_state(
        _marker(),
        main_sha="b" * 40,
        main_committed_at="2026-07-20T10:00:01Z",
        now=NOW,
        live_is_main_ancestor=True,
    )["status"] == "converging"


def test_monitor_fails_after_three_hour_divergence_or_twelve_hour_staleness() -> None:
    with pytest.raises(MonitoringError, match="divergence"):
        evaluate_production_state(
            _marker(),
            main_sha="b" * 40,
            main_committed_at="2026-07-20T09:00:00Z",
            now=NOW,
            live_is_main_ancestor=True,
        )
    with pytest.raises(MonitoringError, match="stale"):
        evaluate_production_state(
            _marker(generated_at="2026-07-20T00:00:00Z"),
            main_sha="a" * 40,
            main_committed_at="2026-07-20T00:00:00Z",
            now=NOW,
        )
    with pytest.raises(MonitoringError, match="ancestor"):
        evaluate_production_state(
            _marker(),
            main_sha="b" * 40,
            main_committed_at="2026-07-20T11:59:00Z",
            now=NOW,
            live_is_main_ancestor=False,
        )


@pytest.mark.parametrize("mutation", ["missing", "extra", "release_id", "hash"])
def test_monitor_rejects_incomplete_or_forged_marker(mutation: str) -> None:
    marker = _marker()
    if mutation == "missing":
        del marker["quality_hash"]
    elif mutation == "extra":
        marker["unexpected"] = "field"
    elif mutation == "release_id":
        marker["release_id"] = "r-" + "0" * 24
    else:
        marker["graph_hash"] = "not-a-digest"

    with pytest.raises(MonitoringError, match="marker"):
        evaluate_production_state(
            marker,
            main_sha="a" * 40,
            main_committed_at="2026-07-20T07:00:00Z",
            now=NOW,
        )


def test_monitor_samples_quality_indexes_and_one_verified_shard_each() -> None:
    marker = _marker()
    quality = json.dumps(
        {"active_count": 1, "verified_provenance_count": 1},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    marker["quality_hash"] = hashlib.sha256(quality).hexdigest()
    payloads: dict[str, bytes] = {"/data/content-quality.json": quality}
    for field, product in (
        ("lineage_hash", "lineage"),
        ("graph_hash", "tag-graph"),
        ("trends_hash", "stack-trends"),
    ):
        shard = json.dumps({"records": [{"id": product}]}).encode()
        shard_hash = hashlib.sha256(shard).hexdigest()
        index = json.dumps(
            {"files": [{"path": "shards/one.json", "sha256": shard_hash}]}
        ).encode()
        payloads[f"/data/{product}/index.json"] = index
        payloads[f"/data/{product}/shards/one.json"] = shard
        marker[field] = "5" * 64
    identity = {
        key: marker[key]
        for key in sorted(set(marker) - {"release_id", "generated_at"})
    }
    marker["release_id"] = "r-" + hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:24]
    requested: list[str] = []

    def fetch(url: str) -> bytes:
        path = urlsplit(url).path
        requested.append(path)
        return payloads[path]

    verify_production_sample("https://example.test/", marker, fetch=fetch)

    assert set(payloads) == set(requested)


def test_monitor_accepts_and_samples_a_complete_pr1_no_lineage_marker() -> None:
    marker = _marker()
    marker["lineage_hash"] = "unavailable"
    marker["lineage_mode"] = "unavailable"
    quality = json.dumps(
        {"active_count": 1, "verified_provenance_count": 1},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    marker["quality_hash"] = hashlib.sha256(quality).hexdigest()
    payloads: dict[str, bytes] = {"/data/content-quality.json": quality}
    for field, product in (
        ("graph_hash", "tag-graph"),
        ("trends_hash", "stack-trends"),
    ):
        shard = json.dumps({"records": [{"id": product}]}).encode()
        digest = hashlib.sha256(shard).hexdigest()
        payloads[f"/data/{product}/index.json"] = json.dumps(
            {"files": [{"path": "shards/one.json", "sha256": digest}]}
        ).encode()
        payloads[f"/data/{product}/shards/one.json"] = shard
        marker[field] = digest
    identity = {
        key: marker[key]
        for key in sorted(set(marker) - {"release_id", "generated_at"})
    }
    marker["release_id"] = "r-" + hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:24]
    requested: list[str] = []

    def fetch(url: str) -> bytes:
        path = urlsplit(url).path
        requested.append(path)
        return payloads[path]

    assert evaluate_production_state(
        marker,
        main_sha="a" * 40,
        main_committed_at="2026-07-20T07:00:00Z",
        now=NOW,
    )["status"] == "healthy"
    assert verify_production_sample(
        "https://example.test/", marker, fetch=fetch
    )["sampled_products"] == 2
    assert not any(path.startswith("/data/lineage/") for path in requested)
