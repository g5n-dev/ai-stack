#!/usr/bin/env python3
"""对 GitHub Pages 生产站执行缓存收敛后的全链路烟测。"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from html.parser import HTMLParser


class ProductionSmokeError(RuntimeError):
    """线上发布未满足完整性契约。"""


RETRY_DELAYS_SECONDS = (5, 10, 20, 30, 45, 60)
_FULL_SHA = re.compile(r"[0-9a-f]{40}\Z")
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_RELEASE_ID = re.compile(r"r-[0-9a-f]{24}\Z")
_CANONICAL_UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
_MARKER_FIELDS = frozenset(
    {
        "schema_version",
        "release_id",
        "exact_sha",
        "quality_hash",
        "lineage_hash",
        "graph_hash",
        "trends_hash",
        "generated_at",
        "lineage_mode",
    }
)
_MAX_RESPONSE_BYTES = 20 * 1024 * 1024
_DEGRADED_MARKERS = (
    "data-degraded",
    "degraded-placeholder",
    "暂无数据",
    "数据加载失败",
    "加载失败",
    "GRAPH_UI_PENDING",
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stylesheets: set[str] = set()
        self.scripts: set[str] = set()
        self.articles: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        candidate = values.get("src") if tag == "script" else values.get("href")
        if not candidate:
            return
        path = urllib.parse.urlsplit(candidate).path.casefold()
        if tag == "link" and path.endswith(".css"):
            self.stylesheets.add(candidate)
        if tag == "script" and path.endswith(".js"):
            self.scripts.add(candidate)
        if path.startswith("/posts/") or "/posts/" in path:
            self.articles.add(candidate)


def _default_fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json,text/html,*/*;q=0.5",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "ai-stack-production-smoke/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status != 200:
                raise ProductionSmokeError("production response status is not 200")
            body = response.read(_MAX_RESPONSE_BYTES + 1)
    except (OSError, urllib.error.URLError) as exc:
        raise ProductionSmokeError("production endpoint is unavailable") from exc
    if len(body) > _MAX_RESPONSE_BYTES:
        raise ProductionSmokeError("production response exceeds size limit")
    return body


def _cache_url(base_url: str, path: str, token: str) -> str:
    absolute = urllib.parse.urljoin(base_url, path)
    parts = urllib.parse.urlsplit(absolute)
    base_parts = urllib.parse.urlsplit(base_url)
    if parts.scheme != "https" or parts.netloc != base_parts.netloc:
        raise ProductionSmokeError("cross-origin production reference is forbidden")
    # urllib.request requires an ASCII request target. Hugo keeps Unicode slugs
    # readable in lineage JSON, so encode only non-ASCII/path-unsafe bytes while
    # preserving existing percent escapes instead of turning ``%E4`` into
    # ``%25E4``.
    path = re.sub(r"%(?![0-9A-Fa-f]{2})", "%25", parts.path or "/")
    encoded_path = urllib.parse.quote(
        path,
        safe="/%:@!$&'()*+,;=-._~",
    )
    query = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    query.append(("__ai_stack_release", token))
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, encoded_path, urllib.parse.urlencode(query), "")
    )


def _fetch_path(
    base_url: str,
    path: str,
    token: str,
    fetch: Callable[[str], bytes],
) -> bytes:
    return fetch(_cache_url(base_url, path, token))


def _json_object(body: bytes) -> dict[str, object]:
    try:
        value = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProductionSmokeError("production JSON is invalid") from exc
    if not isinstance(value, dict):
        raise ProductionSmokeError("production JSON object required")
    return value


def validate_release_marker_payload(
    marker: Mapping[str, object],
    *,
    expected_sha: str | None = None,
    expected_release_id: str | None = None,
) -> dict[str, object]:
    """严格验证远端 marker 的字段、摘要格式与确定性 release_id。"""

    if frozenset(marker) != _MARKER_FIELDS:
        raise ProductionSmokeError("production release marker fields do not match schema")
    exact_sha = marker.get("exact_sha")
    release_id = marker.get("release_id")
    if marker.get("schema_version") != "ai_stack_release_v1":
        raise ProductionSmokeError("production release marker schema is invalid")
    if not isinstance(exact_sha, str) or not _FULL_SHA.fullmatch(exact_sha):
        raise ProductionSmokeError("production release marker SHA is invalid")
    if expected_sha is not None and exact_sha != expected_sha:
        raise ProductionSmokeError("production release marker SHA mismatch")
    for field in ("quality_hash", "graph_hash", "trends_hash"):
        value = marker.get(field)
        if not isinstance(value, str) or not _DIGEST.fullmatch(value):
            raise ProductionSmokeError("production release marker hash is invalid")
    lineage_hash = marker.get("lineage_hash")
    lineage_mode = marker.get("lineage_mode")
    if not isinstance(lineage_mode, str) or not lineage_mode:
        raise ProductionSmokeError("production release marker lineage mode is invalid")
    if lineage_hash == "unavailable":
        if lineage_mode != "unavailable":
            raise ProductionSmokeError("production release marker lineage state is invalid")
    elif not isinstance(lineage_hash, str) or not _DIGEST.fullmatch(lineage_hash):
        raise ProductionSmokeError("production release marker hash is invalid")
    generated_at = marker.get("generated_at")
    if not isinstance(generated_at, str) or not _CANONICAL_UTC.fullmatch(generated_at):
        raise ProductionSmokeError("production release marker timestamp is invalid")
    identity = {
        key: marker[key]
        for key in sorted(_MARKER_FIELDS - {"release_id", "generated_at"})
    }
    computed = "r-" + hashlib.sha256(_canonical_bytes(identity)).hexdigest()[:24]
    if (
        not isinstance(release_id, str)
        or not _RELEASE_ID.fullmatch(release_id)
        or not hmac.compare_digest(release_id, computed)
        or (expected_release_id is not None and release_id != expected_release_id)
    ):
        raise ProductionSmokeError("production release marker identity is invalid")
    return dict(marker)


def _safe_reference(value: str) -> str:
    path = urllib.parse.urlsplit(value).path
    if (
        not path
        or path.startswith("/")
        or "\\" in path
        or any(part in {"", ".", ".."} for part in path.split("/"))
        or not path.casefold().endswith(".json")
    ):
        raise ProductionSmokeError("unsafe production asset reference")
    return path


def _references(value: object) -> list[tuple[str, str | None]]:
    found: list[tuple[str, str | None]] = []
    if isinstance(value, Mapping):
        raw_path = value.get("path")
        raw_digest = value.get("sha256")
        if isinstance(raw_path, str) and raw_path.casefold().endswith(".json"):
            digest = raw_digest.removeprefix("sha256:") if isinstance(raw_digest, str) else None
            found.append((_safe_reference(raw_path), digest))
        for key, child in value.items():
            if key not in {"path", "sha256"}:
                found.extend(_references(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_references(child))
    elif isinstance(value, str) and value.casefold().endswith(".json"):
        found.append((_safe_reference(value), None))
    return found


def _remote_product_tree(
    base_url: str,
    product: str,
    token: str,
    fetch: Callable[[str], bytes],
) -> tuple[str, dict[str, dict[str, object]]]:
    pending: list[tuple[str, str | None]] = [("index.json", None)]
    records: dict[str, str] = {}
    payloads: dict[str, dict[str, object]] = {}
    while pending:
        relative, expected = pending.pop(0)
        if relative in records:
            if expected and records[relative] != expected:
                raise ProductionSmokeError("conflicting production shard hash")
            continue
        if len(records) >= 10_000:
            raise ProductionSmokeError("production shard count limit exceeded")
        body = _fetch_path(base_url, f"/data/{product}/{relative}", token, fetch)
        digest = hashlib.sha256(body).hexdigest()
        if expected is not None and (
            not _DIGEST.fullmatch(expected) or digest != expected
        ):
            raise ProductionSmokeError("production shard hash mismatch")
        payload = _json_object(body)
        records[relative] = digest
        payloads[relative] = payload
        pending.extend(_references(payload))
    return hashlib.sha256(_canonical_bytes(sorted(records.items()))).hexdigest(), payloads


def _remote_product_hash(
    base_url: str,
    product: str,
    token: str,
    fetch: Callable[[str], bytes],
) -> str:
    return _remote_product_tree(base_url, product, token, fetch)[0]


def _validate_quality_payload(body: bytes) -> dict[str, object]:
    quality = _json_object(body)
    for field in ("active_count", "verified_provenance_count"):
        value = quality.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ProductionSmokeError("production quality active/verified counts must be non-empty")
    return quality


def _first_internal_article(value: object) -> str | None:
    if isinstance(value, Mapping):
        for key in ("article_url", "representative_article_url"):
            candidate = value.get(key)
            if isinstance(candidate, str):
                path = urllib.parse.urlsplit(candidate).path
                if path.startswith("/posts/") and path != "/posts/":
                    return candidate
        for child in value.values():
            found = _first_internal_article(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _first_internal_article(child)
            if found is not None:
                return found
    return None


def _validate_product_tree(
    product: str,
    payloads: Mapping[str, Mapping[str, object]],
) -> str | None:
    shards = {path: value for path, value in payloads.items() if path != "index.json"}
    if not shards or not any(bool(value) for value in shards.values()):
        raise ProductionSmokeError(f"production {product} requires a real shard")
    if product != "lineage":
        return None
    routes = [
        value
        for path, value in shards.items()
        if path.startswith("routes/") and isinstance(value.get("routes"), list)
        and bool(value["routes"])
    ]
    if not routes:
        raise ProductionSmokeError("production lineage requires a non-empty route shard")
    clusters = [
        value
        for path, value in shards.items()
        if path.startswith("clusters/") and isinstance(value.get("clusters"), list)
        and bool(value["clusters"])
    ]
    if not clusters:
        raise ProductionSmokeError("production lineage requires a non-empty cluster shard")
    article = _first_internal_article(clusters)
    if article is None:
        raise ProductionSmokeError("production lineage requires an internal article")
    return article


def verify_production_sample(
    base_url: str,
    marker: Mapping[str, object],
    *,
    fetch: Callable[[str], bytes] = _default_fetch,
    token: str = "monitor",
) -> dict[str, object]:
    """供小时监控复用的轻量远端抽查：quality、各 index 与一个分片。"""

    checked = validate_release_marker_payload(marker)
    quality = _fetch_path(base_url, "/data/content-quality.json", token, fetch)
    if hashlib.sha256(quality).hexdigest() != checked["quality_hash"]:
        raise ProductionSmokeError("production quality hash mismatch")
    _validate_quality_payload(quality)
    sampled = 0
    for field, product in (
        ("lineage_hash", "lineage"),
        ("graph_hash", "tag-graph"),
        ("trends_hash", "stack-trends"),
    ):
        if field == "lineage_hash" and checked[field] == "unavailable":
            continue
        index = _json_object(_fetch_path(base_url, f"/data/{product}/index.json", token, fetch))
        references = _references(index)
        if not references:
            raise ProductionSmokeError(f"production {product} index has no shard")
        relative, expected = references[0]
        shard = _fetch_path(base_url, f"/data/{product}/{relative}", token, fetch)
        if not shard:
            raise ProductionSmokeError(f"production {product} shard is empty")
        digest = hashlib.sha256(shard).hexdigest()
        if expected is not None and (
            not _DIGEST.fullmatch(expected) or not hmac.compare_digest(digest, expected)
        ):
            raise ProductionSmokeError(f"production {product} sample hash mismatch")
        _json_object(shard)
        sampled += 1
    return {"sampled_products": sampled, "quality": "verified"}


def _verify_once(
    base_url: str,
    *,
    expected_sha: str,
    expected_release_id: str,
    token: str,
    fetch: Callable[[str], bytes],
) -> dict[str, object]:
    marker = _json_object(
        _fetch_path(base_url, "/ai_stack_release_v1.json", token, fetch)
    )
    marker = validate_release_marker_payload(
        marker,
        expected_sha=expected_sha,
        expected_release_id=expected_release_id,
    )

    links = _Links()
    route_count = 0
    for route in ("/", "/posts/", "/trends/?window=30d", "/scenarios/"):
        body = _fetch_path(base_url, route, token, fetch)
        text = body.decode("utf-8", errors="replace")
        if any(item in text for item in _DEGRADED_MARKERS):
            raise ProductionSmokeError("degraded production placeholder detected")
        if "data-site-header" not in text:
            raise ProductionSmokeError("production page is missing shared header")
        links.feed(text)
        route_count += 1
    if not links.stylesheets:
        raise ProductionSmokeError("production route set has no stylesheet")
    if not links.scripts:
        raise ProductionSmokeError("production route set has no JavaScript asset")
    if not links.articles:
        raise ProductionSmokeError("production route set has no internal article")
    assets = links.stylesheets | links.scripts
    for target in sorted(assets):
        body = _fetch_path(base_url, target, token, fetch)
        if not body:
            raise ProductionSmokeError("empty production asset")
    try:
        pagefind = _fetch_path(base_url, "/pagefind/pagefind.js", token, fetch)
    except (KeyError, OSError, ProductionSmokeError) as exc:
        raise ProductionSmokeError("production Pagefind asset is missing") from exc
    if not pagefind:
        raise ProductionSmokeError("production Pagefind asset is empty")
    for target in sorted(links.articles):
        body = _fetch_path(base_url, target, token, fetch)
        text = body.decode("utf-8", errors="replace")
        if not body or "data-site-header" not in text:
            raise ProductionSmokeError("production article is missing shared header")
        if any(item in text for item in _DEGRADED_MARKERS):
            raise ProductionSmokeError("degraded production placeholder detected")

    quality = _fetch_path(base_url, "/data/content-quality.json", token, fetch)
    if hashlib.sha256(quality).hexdigest() != marker.get("quality_hash"):
        raise ProductionSmokeError("production quality hash mismatch")
    _validate_quality_payload(quality)
    products = {
        "lineage_hash": "lineage",
        "graph_hash": "tag-graph",
        "trends_hash": "stack-trends",
    }
    shard_products = 0
    lineage_article: str | None = None
    for field, product in products.items():
        expected = marker.get(field)
        if expected == "unavailable" and field == "lineage_hash":
            continue
        if not isinstance(expected, str) or not _DIGEST.fullmatch(expected):
            raise ProductionSmokeError("production marker product hash is invalid")
        product_hash, payloads = _remote_product_tree(base_url, product, token, fetch)
        if product_hash != expected:
            raise ProductionSmokeError("production product tree hash mismatch")
        article = _validate_product_tree(product, payloads)
        if article is not None:
            lineage_article = article
        shard_products += 1
    if lineage_article is not None:
        body = _fetch_path(base_url, lineage_article, token, fetch)
        text = body.decode("utf-8", errors="replace")
        if not body or "data-site-header" not in text:
            raise ProductionSmokeError("production lineage article is unavailable")
        if any(item in text for item in _DEGRADED_MARKERS):
            raise ProductionSmokeError("degraded production placeholder detected")
    return {
        "status": "healthy",
        "release_id": expected_release_id,
        "exact_sha": expected_sha,
        "critical_routes": route_count,
        "assets": len(assets) + 1,
        "internal_articles": len(links.articles),
        "verified_products": shard_products,
    }


def run_smoke(
    base_url: str,
    *,
    expected_sha: str,
    expected_release_id: str,
    fetch: Callable[[str], bytes] = _default_fetch,
    sleep: Callable[[int], object] = time.sleep,
) -> dict[str, object]:
    if not _FULL_SHA.fullmatch(expected_sha):
        raise ProductionSmokeError("expected release SHA is invalid")
    parsed = urllib.parse.urlsplit(base_url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ProductionSmokeError("production base URL must be public HTTPS")
    last_error: ProductionSmokeError | None = None
    for attempt, delay in enumerate(RETRY_DELAYS_SECONDS, start=1):
        sleep(delay)
        try:
            return _verify_once(
                base_url,
                expected_sha=expected_sha,
                expected_release_id=expected_release_id,
                token=f"{attempt}-{delay}",
                fetch=fetch,
            )
        except (KeyError, OSError, ProductionSmokeError) as exc:
            last_error = exc if isinstance(exc, ProductionSmokeError) else ProductionSmokeError(
                "production resource is missing"
            )
    assert last_error is not None
    raise last_error


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--expected-release-id", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        report = run_smoke(
            args.base_url,
            expected_sha=args.expected_sha,
            expected_release_id=args.expected_release_id,
        )
    except ProductionSmokeError as exc:
        print(f"production-smoke: {exc}", file=__import__("sys").stderr)
        return 2
    print(_canonical_bytes(report).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
