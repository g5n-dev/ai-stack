from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from urllib.parse import urlsplit

import pytest

from scripts import production_monitor
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


def _direct_product_hash(
    index: bytes,
    *,
    shard_path: str,
    shard_hash: str,
) -> str:
    records = sorted(
        [
            ("index.json", hashlib.sha256(index).hexdigest()),
            (shard_path, shard_hash),
        ]
    )
    return hashlib.sha256(
        json.dumps(
            records,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def test_monitor_accepts_recent_release_and_short_main_divergence() -> None:
    assert evaluate_production_state(
        _marker(),
        main_sha="a" * 40,
        main_committed_at="2026-07-20T07:00:00Z",
        refresh_as_of="2026-07-20T09:00:00Z",
        data_as_of="2026-07-20T08:00:00Z",
        now=NOW,
    )["status"] == "healthy"
    assert evaluate_production_state(
        _marker(),
        main_sha="b" * 40,
        main_committed_at="2026-07-20T10:00:01Z",
        refresh_as_of="2026-07-20T09:00:00Z",
        data_as_of="2026-07-20T08:00:00Z",
        now=NOW,
        live_is_main_ancestor=True,
    )["status"] == "converging"


def test_monitor_uses_refresh_clock_without_rewriting_event_time() -> None:
    report = evaluate_production_state(
        _marker(generated_at="2026-07-18T08:00:00Z"),
        main_sha="a" * 40,
        main_committed_at="2026-07-20T07:00:00Z",
        refresh_as_of="2026-07-20T11:00:00Z",
        data_as_of="2026-07-18T08:00:00Z",
        now=NOW,
    )

    assert report["status"] == "healthy"
    assert report["refresh_age_hours"] == 1.0
    assert report["data_age_hours"] == 52.0
    assert report["refresh_as_of"] == "2026-07-20T11:00:00Z"
    assert report["data_as_of"] == "2026-07-18T08:00:00Z"


def test_monitor_fails_after_three_hour_divergence_or_twelve_hour_refresh_staleness() -> None:
    with pytest.raises(MonitoringError, match="divergence"):
        evaluate_production_state(
            _marker(),
            main_sha="b" * 40,
            main_committed_at="2026-07-20T09:00:00Z",
            refresh_as_of="2026-07-20T09:00:00Z",
            data_as_of="2026-07-20T08:00:00Z",
            now=NOW,
            live_is_main_ancestor=True,
        )
    with pytest.raises(MonitoringError, match="content refresh is stale") as exc_info:
        evaluate_production_state(
            _marker(generated_at="2026-07-20T11:00:00Z"),
            main_sha="a" * 40,
            main_committed_at="2026-07-20T00:00:00Z",
            refresh_as_of="2026-07-20T00:00:00Z",
            data_as_of="2026-07-20T11:00:00Z",
            now=NOW,
        )
    assert "refresh_as_of=2026-07-20T00:00:00Z" in str(exc_info.value)
    assert "refresh_age_hours=12.000" in str(exc_info.value)
    assert "data_as_of=2026-07-20T11:00:00Z" in str(exc_info.value)
    assert "data_age_hours=1.000" in str(exc_info.value)
    assert "threshold_hours=12" in str(exc_info.value)
    with pytest.raises(MonitoringError, match="ancestor"):
        evaluate_production_state(
            _marker(),
            main_sha="b" * 40,
            main_committed_at="2026-07-20T11:59:00Z",
            refresh_as_of="2026-07-20T09:00:00Z",
            data_as_of="2026-07-20T08:00:00Z",
            now=NOW,
            live_is_main_ancestor=False,
        )


@pytest.mark.parametrize(
    ("refresh_as_of", "data_as_of", "reason"),
    [
        ("2026-07-20T12:00:01Z", "2026-07-20T08:00:00Z", "refresh"),
        ("2026-07-20T09:00:00Z", "2026-07-20T12:00:01Z", "data"),
    ],
)
def test_monitor_rejects_future_refresh_or_event_clock(
    refresh_as_of: str,
    data_as_of: str,
    reason: str,
) -> None:
    with pytest.raises(MonitoringError, match=reason):
        evaluate_production_state(
            _marker(generated_at=data_as_of),
            main_sha="a" * 40,
            main_committed_at="2026-07-20T07:00:00Z",
            refresh_as_of=refresh_as_of,
            data_as_of=data_as_of,
            now=NOW,
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
            refresh_as_of="2026-07-20T09:00:00Z",
            data_as_of="2026-07-20T08:00:00Z",
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
        index_payload: dict[str, object] = {
            "files": [{"path": "shards/one.json", "sha256": shard_hash}],
        }
        if product == "lineage":
            index_payload["generated_at"] = "2026-07-20T09:00:00Z"
        if product == "stack-trends":
            index_payload["generated_at"] = "2026-07-20T08:00:00Z"
            index_payload["data_as_of"] = "2026-07-20T08:00:00Z"
        index = json.dumps(index_payload).encode()
        payloads[f"/data/{product}/index.json"] = index
        payloads[f"/data/{product}/shards/one.json"] = shard
        marker[field] = _direct_product_hash(
            index,
            shard_path="shards/one.json",
            shard_hash=shard_hash,
        )
    identity = {
        key: marker[key]
        for key in sorted(set(marker) - {"release_id", "generated_at"})
    }
    marker["release_id"] = "r-" + hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:24]
    requested: list[str] = []
    cache_tokens: list[str] = []

    def fetch(url: str) -> bytes:
        parts = urlsplit(url)
        path = parts.path
        requested.append(path)
        cache_tokens.append(parts.query)
        return payloads[path]

    report = verify_production_sample("https://example.test/", marker, fetch=fetch)

    assert set(payloads) == set(requested)
    assert all(f"__ai_stack_release={marker['release_id']}" in item for item in cache_tokens)
    assert report["refresh_as_of"] == "2026-07-20T09:00:00Z"
    assert report["data_as_of"] == "2026-07-20T08:00:00Z"

    tampered_lineage = json.loads(payloads["/data/lineage/index.json"])
    tampered_lineage["generated_at"] = "2026-07-20T11:00:00Z"
    payloads["/data/lineage/index.json"] = json.dumps(tampered_lineage).encode()
    with pytest.raises(MonitoringError, match="sample"):
        verify_production_sample("https://example.test/", marker, fetch=fetch)


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
        index_payload: dict[str, object] = {
            "files": [{"path": "shards/one.json", "sha256": digest}],
        }
        if product == "stack-trends":
            index_payload["generated_at"] = "2026-07-20T08:00:00Z"
            index_payload["data_as_of"] = "2026-07-20T08:00:00Z"
        index = json.dumps(index_payload).encode()
        payloads[f"/data/{product}/index.json"] = index
        payloads[f"/data/{product}/shards/one.json"] = shard
        marker[field] = _direct_product_hash(
            index,
            shard_path="shards/one.json",
            shard_hash=digest,
        )
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
        refresh_as_of="2026-07-20T08:00:00Z",
        data_as_of="2026-07-20T08:00:00Z",
        now=NOW,
    )["status"] == "healthy"
    report = verify_production_sample("https://example.test/", marker, fetch=fetch)
    assert report["sampled_products"] == 2
    assert report["refresh_as_of"] == "2026-07-20T08:00:00Z"
    assert report["refresh_clock_source"] == "legacy_trend"
    assert not any(path.startswith("/data/lineage/") for path in requested)


def test_monitor_entrypoint_uses_sampled_refresh_and_event_clocks(
    monkeypatch,
    capsys,
) -> None:
    now = datetime.now(timezone.utc)
    refresh_as_of = (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    data_as_of = (now - timedelta(hours=52)).strftime("%Y-%m-%dT%H:%M:%SZ")
    marker = _marker(generated_at=data_as_of)
    monkeypatch.setattr(production_monitor, "_load_marker", lambda _url: marker)
    monkeypatch.setattr(
        production_monitor,
        "verify_production_sample",
        lambda _base_url, _marker: {
            "refresh_as_of": refresh_as_of,
            "data_as_of": data_as_of,
        },
    )
    monkeypatch.setattr(
        production_monitor.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0),
    )

    exit_code = production_monitor.main(
        [
            "--marker-url",
            "https://example.test/ai_stack_release_v1.json",
            "--main-sha",
            "a" * 40,
            "--main-committed-at",
            refresh_as_of,
        ]
    )

    assert exit_code == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "healthy"
    assert report["refresh_as_of"] == refresh_as_of
    assert report["data_as_of"] == data_as_of
