from __future__ import annotations

import hashlib
import json
from urllib.parse import unquote, urlsplit

import pytest

from scripts.production_smoke import (
    RETRY_DELAYS_SECONDS,
    ProductionSmokeError,
    _cache_url,
    run_smoke,
)


SHA = "b" * 40


def _json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _rebind_marker(marker: dict[str, object], payloads: dict[str, bytes]) -> None:
    identity = {
        key: marker[key]
        for key in sorted(set(marker) - {"release_id", "generated_at"})
    }
    marker["release_id"] = "r-" + hashlib.sha256(_json(identity)).hexdigest()[:24]
    payloads["/ai_stack_release_v1.json"] = _json(marker)


def _rebind_product(
    payloads: dict[str, bytes],
    marker: dict[str, object],
    *,
    product: str,
    marker_field: str,
) -> None:
    index_path = f"/data/{product}/index.json"
    index = json.loads(payloads[index_path])
    records: list[tuple[str, str]] = []
    for record in index["files"]:
        path = record["path"]
        digest = hashlib.sha256(payloads[f"/data/{product}/{path}"]).hexdigest()
        record["sha256"] = digest
        records.append((path, digest))
    payloads[index_path] = _json(index)
    records.append(("index.json", hashlib.sha256(payloads[index_path]).hexdigest()))
    marker[marker_field] = hashlib.sha256(_json(sorted(records))).hexdigest()
    _rebind_marker(marker, payloads)


def _fixture(*, include_lineage: bool = True) -> tuple[dict[str, bytes], dict[str, object]]:
    quality = _json({"active_count": 2, "verified_provenance_count": 2})
    payloads: dict[str, bytes] = {
        "/": (
            '<header data-site-header></header>'
            '<link rel="stylesheet" href="/assets/site.css">'
            '<script src="/assets/site.js"></script>'
            '<a href="/posts/one/">article</a>'
        ).encode(),
        "/trends/": b"<header data-site-header></header><main>trends ready</main>",
        "/posts/": b"<header data-site-header></header><main>posts ready</main>",
        "/scenarios/": b"<header data-site-header></header><main>scenarios ready</main>",
        "/posts/one/": b"<header data-site-header></header><article>verified article</article>",
        "/assets/site.css": b"body{color:#fff}",
        "/assets/site.js": b"window.AI_STACK=true;",
        "/pagefind/pagefind.js": b"window.PagefindUI=true;",
        "/data/content-quality.json": quality,
    }
    hashes: dict[str, str] = {}
    products = ("lineage", "tag-graph", "stack-trends") if include_lineage else (
        "tag-graph",
        "stack-trends",
    )
    for product in products:
        if product == "lineage":
            shards = {
                "routes/a.json": {"routes": [{"event_id": "evt", "observation_id": "obs"}]},
                "clusters/a.json": {
                    "clusters": [
                        {
                            "event_id": "evt",
                            "representative_article_url": "/posts/one/",
                            "observations": [{"article_url": "/posts/one/"}],
                        }
                    ]
                },
            }
        else:
            shards = {"shards/a.json": {"product": product, "records": [{"id": "one"}]}}
        records: list[tuple[str, str]] = []
        file_records: list[dict[str, str]] = []
        for relative, value in shards.items():
            shard_path = f"/data/{product}/{relative}"
            payloads[shard_path] = _json(value)
            shard_hash = hashlib.sha256(payloads[shard_path]).hexdigest()
            records.append((relative, shard_hash))
            file_records.append({"path": relative, "sha256": shard_hash})
        index_path = f"/data/{product}/index.json"
        index: dict[str, object] = {
            "files": file_records
        }
        if product == "lineage":
            index["generated_at"] = "2026-07-20T09:00:00Z"
        if product == "stack-trends":
            index.update(
                {
                    "generated_at": "2026-07-20T08:00:00Z",
                    "data_as_of": "2026-07-20T08:00:00Z",
                    "lineage_mode": "lineage_index_v1",
                }
            )
        payloads[index_path] = _json(index)
        # The production implementation uses the same canonical reachable-tree hash.
        records.append(("index.json", hashlib.sha256(payloads[index_path]).hexdigest()))
        records.sort()
        hashes[product] = hashlib.sha256(_json(records)).hexdigest()
    marker: dict[str, object] = {
        "schema_version": "ai_stack_release_v1",
        "release_id": "",
        "exact_sha": SHA,
        "quality_hash": hashlib.sha256(quality).hexdigest(),
        "lineage_hash": hashes.get("lineage", "unavailable"),
        "graph_hash": hashes["tag-graph"],
        "trends_hash": hashes["stack-trends"],
        "generated_at": "2026-07-20T08:00:00Z",
        "lineage_mode": "lineage_index_v1" if include_lineage else "unavailable",
    }
    _rebind_marker(marker, payloads)
    return payloads, marker


def test_smoke_supports_pr1_without_lineage_but_still_verifies_graph_and_trends() -> None:
    payloads, marker = _fixture(include_lineage=False)
    requested: list[str] = []

    def fetch(url: str) -> bytes:
        path = urlsplit(url).path
        requested.append(path)
        return payloads[path]

    result = run_smoke(
        "https://example.test/",
        expected_sha=SHA,
        expected_release_id=str(marker["release_id"]),
        fetch=fetch,
        sleep=lambda _: None,
    )

    assert result["verified_products"] == 2
    assert not any(path.startswith("/data/lineage/") for path in requested)
    assert "/data/tag-graph/index.json" in requested
    assert "/data/stack-trends/index.json" in requested


def test_smoke_checks_routes_assets_marker_shards_and_internal_articles() -> None:
    payloads, marker = _fixture()
    requested: list[str] = []
    sleeps: list[int] = []

    def fetch(url: str) -> bytes:
        path = urlsplit(url).path
        requested.append(path)
        return payloads[path]

    result = run_smoke(
        "https://example.test/",
        expected_sha=SHA,
        expected_release_id=str(marker["release_id"]),
        fetch=fetch,
        sleep=sleeps.append,
    )

    assert result["exact_sha"] == SHA
    assert result["refresh_as_of"] == "2026-07-20T09:00:00Z"
    assert result["data_as_of"] == "2026-07-20T08:00:00Z"
    assert sleeps == [5]
    assert set(payloads).issubset(requested)
    assert RETRY_DELAYS_SECONDS == (5, 10, 20, 30, 45, 60)


@pytest.mark.parametrize("mutation", ["missing_refresh_clock", "event_clock_mismatch"])
def test_smoke_rejects_inconsistent_release_clocks(mutation: str) -> None:
    payloads, marker = _fixture()
    if mutation == "missing_refresh_clock":
        lineage = json.loads(payloads["/data/lineage/index.json"])
        del lineage["generated_at"]
        payloads["/data/lineage/index.json"] = _json(lineage)
        _rebind_product(
            payloads,
            marker,
            product="lineage",
            marker_field="lineage_hash",
        )
    else:
        trends = json.loads(payloads["/data/stack-trends/index.json"])
        trends["data_as_of"] = "2026-07-20T07:00:00Z"
        payloads["/data/stack-trends/index.json"] = _json(trends)
        _rebind_product(
            payloads,
            marker,
            product="stack-trends",
            marker_field="trends_hash",
        )

    with pytest.raises(ProductionSmokeError, match="clock"):
        run_smoke(
            "https://example.test/",
            expected_sha=SHA,
            expected_release_id=str(marker["release_id"]),
            fetch=lambda url: payloads[urlsplit(url).path],
            sleep=lambda _: None,
        )


def test_smoke_percent_encodes_unicode_lineage_article_route() -> None:
    payloads, marker = _fixture()
    unicode_path = "/posts/中文情报溯源/"
    payloads[unicode_path] = payloads["/posts/one/"]
    payloads["/data/lineage/clusters/a.json"] = _json(
        {
            "clusters": [
                {
                    "event_id": "evt",
                    "representative_article_url": unicode_path,
                    "observations": [{"article_url": unicode_path}],
                }
            ]
        }
    )
    _rebind_product(payloads, marker, product="lineage", marker_field="lineage_hash")
    requested: list[str] = []

    def fetch(url: str) -> bytes:
        requested.append(url)
        return payloads[unquote(urlsplit(url).path)]

    result = run_smoke(
        "https://example.test/",
        expected_sha=SHA,
        expected_release_id=str(marker["release_id"]),
        fetch=fetch,
        sleep=lambda _: None,
    )

    article_requests = [url for url in requested if "/posts/%" in url]
    assert result["status"] == "healthy"
    assert len(article_requests) == 1
    assert "%E4%B8%AD%E6%96%87%E6%83%85%E6%8A%A5%E6%BA%AF%E6%BA%90" in article_requests[0]
    assert "中文情报溯源" not in article_requests[0]


@pytest.mark.parametrize(
    ("path", "expected_path"),
    [
        ("/posts/%E4%B8%AD%E6%96%87/", "/posts/%E4%B8%AD%E6%96%87/"),
        ("/posts/100%完成/", "/posts/100%25%E5%AE%8C%E6%88%90/"),
        ("/posts/%ZZ/", "/posts/%25ZZ/"),
    ],
)
def test_cache_url_preserves_only_valid_percent_escapes(
    path: str,
    expected_path: str,
) -> None:
    result = _cache_url("https://example.test/", path, "release-token")

    assert urlsplit(result).path == expected_path


def test_cache_url_preserves_query_semantics_and_drops_fragment() -> None:
    result = _cache_url(
        "https://example.test/",
        "/posts/中文/?tag=人工智能&tag=&mode=full#section",
        "release-token",
    )
    parts = urlsplit(result)

    assert parts.path == "/posts/%E4%B8%AD%E6%96%87/"
    assert parts.query == (
        "tag=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&tag=&mode=full"
        "&__ai_stack_release=release-token"
    )
    assert parts.fragment == ""


def test_cache_url_rejects_cross_origin_reference() -> None:
    with pytest.raises(ProductionSmokeError, match="cross-origin"):
        _cache_url("https://example.test/", "https://attacker.test/posts/one/", "token")


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        ("no_css", "stylesheet"),
        ("no_js", "JavaScript"),
        ("no_article", "article"),
        ("no_pagefind", "Pagefind"),
        ("empty_quality", "quality"),
        ("empty_shard", "shard"),
        ("lineage_route", "route"),
        ("lineage_cluster", "cluster"),
        ("lineage_article", "article"),
    ],
)
def test_smoke_rejects_incomplete_delivery_components(
    mutation: str,
    reason: str,
) -> None:
    payloads, marker = _fixture()
    home = payloads["/"].decode()
    if mutation == "no_css":
        payloads["/"] = home.replace('<link rel="stylesheet" href="/assets/site.css">', "").encode()
    elif mutation == "no_js":
        payloads["/"] = home.replace('<script src="/assets/site.js"></script>', "").encode()
    elif mutation == "no_article":
        payloads["/"] = home.replace('<a href="/posts/one/">article</a>', "").encode()
    elif mutation == "no_pagefind":
        del payloads["/pagefind/pagefind.js"]
    elif mutation == "empty_quality":
        quality = _json({"active_count": 0, "verified_provenance_count": 0})
        payloads["/data/content-quality.json"] = quality
        marker["quality_hash"] = hashlib.sha256(quality).hexdigest()
    elif mutation == "empty_shard":
        index = _json({"files": []})
        payloads["/data/tag-graph/index.json"] = index
        marker["graph_hash"] = hashlib.sha256(
            _json([("index.json", hashlib.sha256(index).hexdigest())])
        ).hexdigest()
    elif mutation == "lineage_route":
        payloads["/data/lineage/routes/a.json"] = _json({"routes": []})
        _rebind_product(payloads, marker, product="lineage", marker_field="lineage_hash")
    elif mutation == "lineage_cluster":
        payloads["/data/lineage/clusters/a.json"] = _json({"clusters": []})
        _rebind_product(payloads, marker, product="lineage", marker_field="lineage_hash")
    else:
        payloads["/data/lineage/clusters/a.json"] = _json(
            {"clusters": [{"event_id": "evt", "observations": []}]}
        )
        _rebind_product(payloads, marker, product="lineage", marker_field="lineage_hash")

    # Recompute only the marker identity where the marker itself was intentionally changed.
    if mutation in {"empty_quality", "empty_shard"}:
        _rebind_marker(marker, payloads)

    with pytest.raises((KeyError, ProductionSmokeError), match=reason):
        run_smoke(
            "https://example.test/",
            expected_sha=SHA,
            expected_release_id=str(marker["release_id"]),
            fetch=lambda url: payloads[urlsplit(url).path],
            sleep=lambda _: None,
        )


def test_smoke_rejects_marker_with_extra_fields_or_invalid_release_identity() -> None:
    payloads, marker = _fixture()
    marker["unexpected"] = True
    payloads["/ai_stack_release_v1.json"] = _json(marker)
    with pytest.raises(ProductionSmokeError, match="fields"):
        run_smoke(
            "https://example.test/",
            expected_sha=SHA,
            expected_release_id=str(marker["release_id"]),
            fetch=lambda url: payloads[urlsplit(url).path],
            sleep=lambda _: None,
        )


def test_smoke_retries_with_cachebuster_and_rejects_degraded_placeholder() -> None:
    payloads, marker = _fixture()
    sleeps: list[int] = []
    attempts = 0

    def flaky(url: str) -> bytes:
        nonlocal attempts
        path = urlsplit(url).path
        if path == "/ai_stack_release_v1.json":
            attempts += 1
            if attempts < 3:
                raise OSError("cache has not converged")
        return payloads[path]

    run_smoke(
        "https://example.test/",
        expected_sha=SHA,
        expected_release_id=str(marker["release_id"]),
        fetch=flaky,
        sleep=sleeps.append,
    )
    assert sleeps == [5, 10, 20]

    payloads["/trends/"] = '<main data-degraded="true">暂无数据</main>'.encode()
    with pytest.raises(ProductionSmokeError, match="degraded"):
        run_smoke(
            "https://example.test/",
            expected_sha=SHA,
            expected_release_id=str(marker["release_id"]),
            fetch=lambda url: payloads[urlsplit(url).path],
            sleep=lambda _: None,
        )


def test_smoke_rejects_missing_shared_header_and_pending_graph_marker() -> None:
    payloads, marker = _fixture()
    payloads["/scenarios/"] = b"<main>missing shared header</main>"
    with pytest.raises(ProductionSmokeError, match="shared header"):
        run_smoke(
            "https://example.test/",
            expected_sha=SHA,
            expected_release_id=str(marker["release_id"]),
            fetch=lambda url: payloads[urlsplit(url).path],
            sleep=lambda _: None,
        )

    payloads, marker = _fixture()
    payloads["/trends/"] = (
        b"<header data-site-header></header><main>GRAPH_UI_PENDING_INTEGRATION</main>"
    )
    with pytest.raises(ProductionSmokeError, match="degraded"):
        run_smoke(
            "https://example.test/",
            expected_sha=SHA,
            expected_release_id=str(marker["release_id"]),
            fetch=lambda url: payloads[urlsplit(url).path],
            sleep=lambda _: None,
        )
