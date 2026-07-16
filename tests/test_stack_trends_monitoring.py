from __future__ import annotations

import hashlib
import json
import urllib.error
from datetime import UTC, datetime

import pytest

from scripts import verify_stack_trends_live


NOW = datetime(2026, 7, 16, 4, 0, tzinfo=UTC)


def _json_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _ref(path: str, raw: bytes) -> dict[str, object]:
    return {
        "path": path,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def _release() -> tuple[dict[str, object], dict[str, bytes]]:
    data_as_of = "2026-07-16T03:30:00Z"
    detail_path = "topics/fixture.json"
    topic = _json_bytes(
        {
            "schema_version": "stack_trends_topic_v1",
            "id": "tag:LLM",
            "topic": "LLM",
            "graph_node_id": "tag:LLM",
            "data_as_of": data_as_of,
            "windows": {name: {"score": 1.0} for name in ("24h", "7d", "30d")},
        }
    )
    assets = {"topics/fixture.json": topic}
    window_refs: dict[str, object] = {}
    for name in ("24h", "7d", "30d"):
        path = f"windows/{name}-fixture.json"
        window = _json_bytes(
            {
                "schema_version": "stack_trends_window_v1",
                "window": name,
                "data_as_of": data_as_of,
                "trends": [
                    {
                        "id": "tag:LLM",
                        "topic": "LLM",
                        "graph_node_id": "tag:LLM",
                        "detail_path": detail_path,
                    }
                ],
            }
        )
        assets[path] = window
        window_refs[name] = {**_ref(path, window), "trend_count": 1}
    index = {
        "schema_version": "stack_trends_index_v1",
        "generated_at": data_as_of,
        "data_as_of": data_as_of,
        "default_window": "30d",
        "stats": {
            "topic_count": 1,
            "windows": {
                name: {"trend_count": 1} for name in ("24h", "7d", "30d")
            },
        },
        "windows": window_refs,
        "topics": {"tag:LLM": _ref(detail_path, topic)},
    }
    return index, assets


def _rehash_asset(
    index: dict[str, object],
    assets: dict[str, bytes],
    path: str,
    payload: dict[str, object],
) -> None:
    raw = _json_bytes(payload)
    assets[path] = raw
    collections = (index["windows"], index["topics"])
    for collection in collections:
        assert isinstance(collection, dict)
        for reference in collection.values():
            assert isinstance(reference, dict)
            if reference.get("path") == path:
                reference.update(_ref(path, raw))
                return
    raise AssertionError(f"missing fixture reference: {path}")


def test_live_release_verifies_freshness_and_every_content_addressed_asset() -> None:
    index, assets = _release()
    base = "https://ai-stack.site/data/stack-trends/"
    requested: list[tuple[str, int]] = []

    def loader(url: str, max_bytes: int) -> bytes:
        requested.append((url, max_bytes))
        if url == f"{base}index.json":
            return _json_bytes(index)
        return assets[url.removeprefix(base)]

    report = verify_stack_trends_live.verify_live_release(
        f"{base}index.json",
        now=NOW,
        max_age_hours=12,
        loader=loader,
    )

    assert report["status"] == "ok"
    assert report["asset_count"] == 4
    assert report["data_as_of"] == "2026-07-16T03:30:00Z"
    assert report["age_hours"] == 0.5
    assert [url for url, _limit in requested] == [
        f"{base}index.json",
        f"{base}topics/fixture.json",
        f"{base}windows/24h-fixture.json",
        f"{base}windows/30d-fixture.json",
        f"{base}windows/7d-fixture.json",
    ]


def test_live_release_fails_closed_for_tampered_or_missing_asset() -> None:
    index, assets = _release()
    base = "https://ai-stack.site/data/stack-trends/"

    def tampered(url: str, _max_bytes: int) -> bytes:
        if url.endswith("index.json"):
            return _json_bytes(index)
        if url.endswith("topics/fixture.json"):
            return b"x" * len(assets["topics/fixture.json"])
        return assets[url.removeprefix(base)]

    with pytest.raises(verify_stack_trends_live.TrendMonitoringError, match="hash"):
        verify_stack_trends_live.verify_live_release(
            f"{base}index.json",
            now=NOW,
            max_age_hours=12,
            loader=tampered,
        )

    def missing(url: str, _max_bytes: int) -> bytes:
        if url.endswith("index.json"):
            return _json_bytes(index)
        raise verify_stack_trends_live.TrendMonitoringError("network error: 404")

    with pytest.raises(verify_stack_trends_live.TrendMonitoringError, match="404"):
        verify_stack_trends_live.verify_live_release(
            f"{base}index.json",
            now=NOW,
            max_age_hours=12,
            loader=missing,
        )


@pytest.mark.parametrize(
    ("target", "reason"),
    [
        ("window_identity", "window identity"),
        ("window_data_as_of", "data_as_of"),
        ("detail_path", "detail_path"),
        ("topic_identity", "topic identity"),
        ("topic_graph_node", "topic identity"),
        ("topic_data_as_of", "data_as_of"),
        ("trend_identity", "topic identity"),
        ("missing_topic_reference", "topic reference"),
        ("duplicate_trend", "duplicate trend"),
        ("reference_trend_count", "trend_count"),
        ("stats_trend_count", "trend_count"),
        ("topic_count", "topic_count"),
        ("default_window", "default_window"),
        ("stats_window_identity", "stats.windows identity"),
        ("generated_at", "generated_at.*data_as_of"),
    ],
)
def test_live_release_cross_checks_shard_semantics(target: str, reason: str) -> None:
    index, assets = _release()
    base = "https://ai-stack.site/data/stack-trends/"
    if target.startswith("window_") or target in {
        "detail_path",
        "trend_identity",
        "missing_topic_reference",
        "duplicate_trend",
    }:
        path = "windows/30d-fixture.json"
        payload = json.loads(assets[path])
        if target == "window_identity":
            payload["window"] = "7d"
        elif target == "window_data_as_of":
            payload["data_as_of"] = "2026-07-15T03:30:00Z"
        elif target == "detail_path":
            payload["trends"][0]["detail_path"] = "topics/not-indexed.json"
        elif target == "trend_identity":
            payload["trends"][0]["topic"] = "Wrong"
        elif target == "missing_topic_reference":
            payload["trends"][0].update(
                id="tag:Unknown",
                topic="Unknown",
                graph_node_id="tag:Unknown",
            )
        else:
            payload["trends"].append(dict(payload["trends"][0]))
            index["windows"]["30d"]["trend_count"] = 2
            index["stats"]["windows"]["30d"]["trend_count"] = 2
        _rehash_asset(index, assets, path, payload)
    elif target in {"topic_identity", "topic_graph_node", "topic_data_as_of"}:
        path = "topics/fixture.json"
        payload = json.loads(assets[path])
        if target == "topic_identity":
            payload["id"] = "tag:Wrong"
        elif target == "topic_graph_node":
            payload["graph_node_id"] = "tag:Wrong"
        else:
            payload["data_as_of"] = "2026-07-15T03:30:00Z"
        _rehash_asset(index, assets, path, payload)
    elif target == "reference_trend_count":
        index["windows"]["30d"]["trend_count"] = 2
    elif target == "stats_trend_count":
        index["stats"]["windows"]["30d"]["trend_count"] = 2
    elif target == "topic_count":
        index["stats"]["topic_count"] = 2
    elif target == "default_window":
        index["default_window"] = "90d"
    elif target == "stats_window_identity":
        del index["stats"]["windows"]["24h"]
    else:
        index["generated_at"] = "2026-07-16T03:31:00Z"

    def loader(url: str, _max_bytes: int) -> bytes:
        if url == f"{base}index.json":
            return _json_bytes(index)
        return assets[url.removeprefix(base)]

    with pytest.raises(verify_stack_trends_live.TrendMonitoringError, match=reason):
        verify_stack_trends_live.verify_live_release(
            f"{base}index.json",
            now=NOW,
            max_age_hours=12,
            loader=loader,
        )


def test_live_semantic_error_does_not_echo_shard_content() -> None:
    index, assets = _release()
    base = "https://ai-stack.site/data/stack-trends/"
    sensitive = "sk-test_abcdefghijklmnopqrstuvwxyz"
    path = "topics/fixture.json"
    payload = json.loads(assets[path])
    payload["id"] = sensitive
    _rehash_asset(index, assets, path, payload)

    def loader(url: str, _max_bytes: int) -> bytes:
        if url == f"{base}index.json":
            return _json_bytes(index)
        return assets[url.removeprefix(base)]

    with pytest.raises(verify_stack_trends_live.TrendMonitoringError) as raised:
        verify_stack_trends_live.verify_live_release(
            f"{base}index.json",
            now=NOW,
            max_age_hours=12,
            loader=loader,
        )

    assert sensitive not in str(raised.value)


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("schema_version", "trend_v1", "schema"),
        ("generated_at", "2026-07-16 03:30:00", "RFC3339"),
        ("data_as_of", "2026-07-15T12:00:00Z", "stale"),
        ("data_as_of", "2026-07-16T04:00:01Z", "future"),
    ],
)
def test_live_release_rejects_invalid_or_stale_index(
    field: str,
    value: object,
    reason: str,
) -> None:
    index, _assets = _release()
    index[field] = value

    with pytest.raises(verify_stack_trends_live.TrendMonitoringError, match=reason):
        verify_stack_trends_live.verify_live_release(
            "https://ai-stack.site/data/stack-trends/index.json",
            now=NOW,
            max_age_hours=12,
            loader=lambda _url, _limit: _json_bytes(index),
        )


@pytest.mark.parametrize(
    "path",
    [
        "../secrets.json",
        "/data/stack-trends/topics/fixture.json",
        "https://attacker.test/fixture.json",
        "topics/%2e%2e/secrets.json",
    ],
)
def test_live_release_rejects_unsafe_manifest_paths_without_fetching(path: str) -> None:
    index, _assets = _release()
    topic = index["topics"]
    assert isinstance(topic, dict)
    ref = topic["tag:LLM"]
    assert isinstance(ref, dict)
    ref["path"] = path
    calls = 0

    def loader(_url: str, _limit: int) -> bytes:
        nonlocal calls
        calls += 1
        return _json_bytes(index)

    with pytest.raises(verify_stack_trends_live.TrendMonitoringError, match="path"):
        verify_stack_trends_live.verify_live_release(
            "https://ai-stack.site/data/stack-trends/index.json",
            now=NOW,
            max_age_hours=12,
            loader=loader,
        )

    assert calls == 1


def test_cli_returns_nonzero_without_echoing_asset_content(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        verify_stack_trends_live,
        "verify_live_release",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            verify_stack_trends_live.TrendMonitoringError("asset hash mismatch")
        ),
    )

    status = verify_stack_trends_live.main(
        [
            "--live-index-url",
            "https://ai-stack.site/data/stack-trends/index.json",
            "--max-age-hours",
            "12",
        ],
        now=NOW,
    )

    output = json.loads(capsys.readouterr().out)
    assert status == 1
    assert output == {"error": "asset hash mismatch", "status": "error"}


def test_network_loader_rejects_cross_origin_redirect_and_oversized_body(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Response:
        def __init__(self, body: bytes, final_url: str):
            self.body = body
            self.final_url = final_url

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def geturl(self) -> str:
            return self.final_url

        def read(self, limit: int) -> bytes:
            return self.body[:limit]

    monkeypatch.setattr(
        verify_stack_trends_live.urllib.request,
        "urlopen",
        lambda _request, timeout: Response(
            b"{}", "https://attacker.test/data/stack-trends/index.json"
        ),
    )
    with pytest.raises(verify_stack_trends_live.TrendMonitoringError, match="redirect"):
        verify_stack_trends_live.load_url(
            "https://ai-stack.site/data/stack-trends/index.json", 64
        )

    monkeypatch.setattr(
        verify_stack_trends_live.urllib.request,
        "urlopen",
        lambda _request, timeout: Response(
            b"x" * 65, "https://ai-stack.site/data/stack-trends/index.json"
        ),
    )
    with pytest.raises(verify_stack_trends_live.TrendMonitoringError, match="size"):
        verify_stack_trends_live.load_url(
            "https://ai-stack.site/data/stack-trends/index.json", 64
        )

    def offline(_request: object, timeout: int) -> object:
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(verify_stack_trends_live.urllib.request, "urlopen", offline)
    with pytest.raises(verify_stack_trends_live.TrendMonitoringError, match="network"):
        verify_stack_trends_live.load_url(
            "https://ai-stack.site/data/stack-trends/index.json", 64
        )
