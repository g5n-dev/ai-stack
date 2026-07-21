from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

from ai_stack.content_quality import write_content_quality_manifest
from ai_stack.identity import canonicalize_url
from processor.intelligence import calculate_trends
from processor.stack_trends import (
    INDEX_SCHEMA_VERSION_V2,
    StackTrendsValidationError,
    TOPIC_SCHEMA_VERSION_V2,
    WINDOW_SCHEMA_VERSION_V2,
    adapt_posts_to_events,
    build_stack_trends,
    load_stack_trends_config,
    verify_stack_trends,
)
from scripts.build_stack_trends import main as build_cli_main
from scripts.verify_stack_trends import main as verify_cli_main

AS_OF = "2026-07-16T12:00:00Z"


def _write_post(
    content_root: Path,
    name: str,
    *,
    date: str,
    tags: list[str],
    source: str = "blogs_podcasts",
    external_url: str | None = None,
    title: str | None = None,
    description: str | None = None,
    draft: bool = False,
    archived: bool = False,
    scenarios: list[str] | None = None,
    categories: list[str] | None = None,
    slug: str | None = None,
    url: str | None = None,
    body: str | None = None,
) -> Path:
    posts = content_root / "posts"
    posts.mkdir(parents=True, exist_ok=True)
    metadata = {
        "title": title or f"Evidence {name}",
        "date": date,
        "draft": draft,
        "tags": tags,
        "categories": categories or ["工程"],
        "scenarios": scenarios or ["AI 开发"],
        "source": source,
        "description": description or f"{name} 的公开证据摘要，内容完整且可核验。",
        "external_url": external_url or f"https://example.com/{name}",
    }
    if archived:
        metadata["archived"] = True
    if slug is not None:
        metadata["slug"] = slug
    if url is not None:
        metadata["url"] = url
    rendered = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    prose = body or (
        "## 摘要\n\n"
        f"{name} 提供了足够长度的公开技术证据，用于验证趋势聚合与下钻展示。"
    )
    path = posts / f"{name}.md"
    path.write_text(f"---\n{rendered}\n---\n\n{prose}\n", encoding="utf-8")
    return path


def _fixture_site(
    root: Path,
    *,
    secret_description: bool = False,
    unsafe_description: bool = False,
) -> tuple[Path, Path]:
    content_root = root / "content"
    # Current, previous and pre-previous 24-hour buckets for a rising LLM signal.
    current = (
        ("current-a", "2026-07-16T10:00:00Z", "arxiv"),
        ("current-b", "2026-07-16T08:00:00Z", "hacker_news"),
        ("current-c", "2026-07-15T18:00:00Z", "blogs_podcasts"),
    )
    for index, (name, date, source) in enumerate(current):
        _write_post(
            content_root,
            name,
            date=date,
            tags=["LLM", "来源快报", "ArXiv" if source == "arxiv" else "博客与播客"],
            source=source,
            title=f"LLM evidence {index}",
            description=(
                "泄漏 " + "sk-" + "test_abcdefghijklmnopqrstuvwxyz"
                if secret_description and index == 0
                else "<img src=x onerror=alert(1)>"
                if unsafe_description and index == 0
                else f"LLM 证据 {index} 展示近期模型工程变化。"
            ),
            scenarios=["模型工程"],
            categories=["模型"],
            slug="llm-current-a" if index == 0 else None,
        )
    for name, date in (
        ("previous-a", "2026-07-15T10:00:00Z"),
        ("previous-b", "2026-07-14T18:00:00Z"),
        ("pre-previous", "2026-07-13T18:00:00Z"),
    ):
        _write_post(content_root, name, date=date, tags=["LLM"], source="arxiv")

    # Co-occurs twice, so it is related but below the trend minimum.
    for name in ("current-a", "current-b"):
        path = content_root / "posts" / f"{name}.md"
        document = path.read_text(encoding="utf-8")
        path.write_text(document.replace("- LLM\n", "- LLM\n- AI Agent\n", 1), encoding="utf-8")

    # Exact alias is normalized, but source/format labels never become topics.
    for index in range(3):
        _write_post(
            content_root,
            f"coding-{index}",
            date=f"2026-07-16T0{index + 1}:00:00Z",
            tags=["AI编程", "掘金", "Intermediate (200)"],
            source="juejin",
        )

    # Same canonical source is counted once.
    _write_post(
        content_root,
        "duplicate-a",
        date="2026-07-16T09:00:00Z",
        tags=["Duplicate Topic"],
        external_url="https://example.com/duplicate?utm_source=one",
    )
    _write_post(
        content_root,
        "duplicate-b",
        date="2026-07-16T09:30:00Z",
        tags=["Duplicate Topic"],
        external_url="https://example.com/duplicate?utm_source=two",
    )
    _write_post(
        content_root,
        "draft",
        date="2026-07-16T11:00:00Z",
        tags=["LLM"],
        draft=True,
    )
    _write_post(
        content_root,
        "future",
        date="2026-07-17T11:00:00Z",
        tags=["LLM"],
    )
    _write_post(
        content_root,
        "archived",
        date="2026-07-16T11:00:00Z",
        tags=["LLM"],
        archived=True,
    )

    manifest_path = root / "content_quality.json"
    write_content_quality_manifest(content_root, manifest_path)
    return content_root, manifest_path


def _tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _write_lineage_assets(
    root: Path,
    *,
    observations: list[dict[str, object]],
    event_id: str,
) -> Path:
    """Write the public lineage contract consumed by trend builds."""

    lineage_root = root / "lineage"
    route_payload = {
        "version": 1,
        "bucket": "00",
        "routes": [
            {
                "observation_id": item["observation_id"],
                "event_id": event_id,
            }
            for item in observations
        ],
    }
    cluster_payload = {
        "version": 1,
        "bucket": "00",
        "clusters": [
            {
                "event_id": event_id,
                "event_aliases": [],
                "earliest_observed_id": observations[0]["observation_id"],
                "probable_origin_id": observations[0]["observation_id"],
                "representative_article_url": observations[0]["article_url"],
                "observations": observations,
            }
        ],
    }

    def write_shard(kind: str, payload: dict[str, object]) -> dict[str, object]:
        body = (
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode()
        digest = hashlib.sha256(body).hexdigest()
        relative = f"{kind}/00-{digest[:16]}.json"
        path = lineage_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        return {"bucket": "00", "path": relative, "sha256": digest, "bytes": len(body)}

    route_ref = write_shard("routes", route_payload)
    cluster_ref = write_shard("clusters", cluster_payload)
    index = {
        "version": 1,
        "schema": "lineage_index_v1",
        "generated_at": AS_OF,
        "bucket_count": 128,
        "bucket_algorithm": "sha256_prefix32_mod_v1",
        "stats": {
            "observations": len(observations),
            "events": 1,
            "exact_copies": sum(item["relation"] == "exact_copy" for item in observations),
            "syndicated": sum(item["relation"] == "syndicated" for item in observations),
            "derivatives": sum(item["relation"] == "derivative" for item in observations),
            "same_event": sum(item["relation"] == "same_event" for item in observations),
            "related_only": sum(item["relation"] == "related_only" for item in observations),
        },
        "route_buckets": [route_ref],
        "cluster_buckets": [cluster_ref],
    }
    (lineage_root / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return lineage_root


def _observation_id(url: str) -> str:
    canonical = canonicalize_url(url)
    return f"obs_{hashlib.sha256(canonical.encode()).hexdigest()}"


def _rewrite_referenced_asset(
    output: Path,
    *,
    collection: str,
    identity: str,
    mutate: Callable[[dict[str, object]], None],
) -> tuple[dict[str, object], dict[str, object]]:
    """Rewrite one content-addressed fixture and keep only its index hash valid."""

    index_path = output / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    reference = index[collection][identity]
    old_path = output / reference["path"]
    payload = json.loads(old_path.read_text(encoding="utf-8"))
    mutate(payload)
    body = (
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    digest = hashlib.sha256(body).hexdigest()
    prefix = "windows" if collection == "windows" else "topics"
    stem = Path(reference["path"]).stem.rsplit("-", 1)[0]
    new_relative = f"{prefix}/{stem}-{digest[:12]}.json"
    new_path = output / new_relative
    new_path.write_bytes(body)
    old_path.unlink()
    reference.update(path=new_relative, bytes=len(body), sha256=digest)
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n",
        encoding="utf-8",
    )
    return index, payload


def test_config_uses_versioned_exact_denylist() -> None:
    config = load_stack_trends_config()

    assert config.version == 1
    assert config.same_event_promotions == ()
    assert "来源快报" in config.excluded_tags
    assert "ArXiv" in config.excluded_tags
    assert "Intermediate (200)" in config.excluded_tags
    assert "arXiv" not in config.excluded_tags
    assert "ARXIV" not in config.excluded_tags


@pytest.mark.parametrize(
    ("payload", "reason"),
    [
        ({"version": 2, "excluded_tags": [], "source_weight": 0.5}, "version"),
        (
            {"version": 1, "excluded_tags": ["source", "source"], "source_weight": 0.5},
            "duplicates",
        ),
        ({"version": 1, "excluded_tags": [], "source_weight": 2}, "source_weight"),
    ],
)
def test_config_rejects_unreviewed_or_ambiguous_policy(
    tmp_path: Path,
    payload: dict[str, object],
    reason: str,
) -> None:
    path = tmp_path / "stack_trends.yaml"
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")

    with pytest.raises(StackTrendsValidationError, match=reason):
        load_stack_trends_config(path)


def _reviewed_same_event_promotion(
    *,
    event_id: str | None = None,
    observation_id: str | None = None,
    parent_observation_id: str | None = None,
) -> dict[str, object]:
    return {
        "event_id": event_id or f"evt_{'1' * 64}",
        "observation_id": observation_id or f"obs_{'2' * 64}",
        "parent_observation_id": parent_observation_id or f"obs_{'3' * 64}",
        "successful_refreshes": 24,
        "deterministic_full_builds": 3,
        "stable_since": "2026-07-01T00:00:00Z",
        "reviewed_at": "2026-07-10T00:00:00Z",
        "false_merge_rate": 0.004,
    }


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("successful_refreshes", 23, "successful_refreshes"),
        ("deterministic_full_builds", 2, "deterministic_full_builds"),
        ("false_merge_rate", 0.005, "false_merge_rate"),
        ("stable_since", "2026-07-04T00:00:01Z", "seven full days"),
        ("observation_id", f"evt_{'2' * 64}", "observation_id"),
    ],
)
def test_same_event_promotion_policy_rejects_unqualified_entries(
    tmp_path: Path,
    field: str,
    value: object,
    reason: str,
) -> None:
    payload = yaml.safe_load(Path("config/stack_trends.yaml").read_text(encoding="utf-8"))
    promotion = _reviewed_same_event_promotion()
    promotion[field] = value
    payload["same_event_promotions"] = [promotion]
    path = tmp_path / "stack_trends.yaml"
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")

    with pytest.raises(StackTrendsValidationError, match=reason):
        load_stack_trends_config(path)


def test_same_event_promotion_policy_rejects_unknown_or_duplicate_pairs(
    tmp_path: Path,
) -> None:
    payload = yaml.safe_load(Path("config/stack_trends.yaml").read_text(encoding="utf-8"))
    promotion = _reviewed_same_event_promotion()
    promotion["approval_note"] = "not part of the reviewed schema"
    payload["same_event_promotions"] = [promotion]
    path = tmp_path / "unknown.yaml"
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")
    with pytest.raises(StackTrendsValidationError, match="unknown fields"):
        load_stack_trends_config(path)

    promotion.pop("approval_note")
    payload["same_event_promotions"] = [promotion, promotion]
    path = tmp_path / "duplicate.yaml"
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")
    with pytest.raises(StackTrendsValidationError, match="duplicate same_event"):
        load_stack_trends_config(path)


def test_adapter_applies_quality_canonicalization_aliases_and_cutoff(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)

    dataset = adapt_posts_to_events(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        as_of=AS_OF,
    )

    events = dataset["events"]
    assert dataset["data_as_of"] == "2026-07-16T10:00:00Z"
    assert sum("Duplicate Topic" in event["topics"] for event in events) == 1
    assert all(event["occurred_at"] <= AS_OF for event in events)
    assert all("来源快报" not in event["topics"] for event in events)
    assert all("ArXiv" not in event["topics"] for event in events)
    assert any("AI 编程" in event["topics"] for event in events)
    assert all("external_url" not in event for event in events)
    assert all("path" not in key for event in events for key in event)
    assert not any(event["title"] == "Evidence draft" for event in events)
    assert not any(event["title"] == "Evidence future" for event in events)
    assert not any(event["title"] == "Evidence archived" for event in events)


def test_adapter_consumes_lineage_without_merging_derivative_reports(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    urls = {
        "origin": "https://source.example/launch",
        "syndicated": "https://wire.example/reprint",
        "derivative": "https://analysis.example/deep-dive",
        "suppressed": "https://mirror.example/exact-copy",
    }
    routes = {}
    for index, (name, url) in enumerate(
        (item for item in urls.items() if item[0] != "suppressed")
    ):
        path = _write_post(
            content_root,
            name,
            date=f"2026-07-16T{index + 7:02d}:00:00Z",
            tags=["Lineage"],
            source=name,
            external_url=url,
        )
        routes[name] = f"/posts/{path.stem}/"
    manifest_path = tmp_path / "quality.json"
    write_content_quality_manifest(content_root, manifest_path)

    origin_id = _observation_id(urls["origin"])
    event_id = f"evt_{origin_id.removeprefix('obs_')}"
    observations = [
        {
            "observation_id": origin_id,
            "title": "Original launch",
            "source": "origin",
            "source_url": urls["origin"],
            "article_url": routes["origin"],
            "relation": "original",
            "parent_observation_id": None,
            "source_published_at": "2026-07-16T07:00:00Z",
            "first_seen_at": "2026-07-16T07:05:00Z",
            "timestamp_confidence": "publisher",
        },
        {
            "observation_id": _observation_id(urls["syndicated"]),
            "title": "Syndicated launch",
            "source": "syndicated",
            "source_url": urls["syndicated"],
            "article_url": routes["syndicated"],
            "relation": "syndicated",
            "parent_observation_id": origin_id,
            "source_published_at": "2026-07-16T08:00:00Z",
            "first_seen_at": "2026-07-16T08:05:00Z",
            "timestamp_confidence": "feed",
        },
        {
            "observation_id": _observation_id(urls["derivative"]),
            "title": "Independent analysis",
            "source": "derivative",
            "source_url": urls["derivative"],
            "article_url": routes["derivative"],
            "relation": "derivative",
            "parent_observation_id": origin_id,
            "source_published_at": "2026-07-16T09:00:00Z",
            "first_seen_at": "2026-07-16T09:05:00Z",
            "timestamp_confidence": "publisher",
        },
        {
            "observation_id": _observation_id(urls["suppressed"]),
            "title": "Exact mirror without a local Post",
            "source": "mirror",
            "source_url": urls["suppressed"],
            "article_url": None,
            "relation": "exact_copy",
            "parent_observation_id": origin_id,
            "source_published_at": "2026-07-16T08:30:00Z",
            "first_seen_at": "2026-07-16T08:35:00Z",
            "timestamp_confidence": "feed",
        },
    ]
    lineage_root = _write_lineage_assets(
        tmp_path,
        observations=observations,
        event_id=event_id,
    )

    dataset = adapt_posts_to_events(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        lineage_root=lineage_root,
        as_of=AS_OF,
    )
    by_relation = {event["lineage_relation"]: event for event in dataset["events"]}

    assert by_relation["original"]["canonical_event_id"] == event_id
    assert by_relation["syndicated"]["canonical_event_id"] == event_id
    assert by_relation["exact_copy"]["canonical_event_id"] == event_id
    assert by_relation["exact_copy"]["internal_url"] == routes["origin"]
    assert by_relation["derivative"]["canonical_event_id"] == by_relation["derivative"]["event_id"]
    assert len({event["canonical_event_id"] for event in dataset["events"]}) == 2
    assert len(dataset["events"]) == 4
    assert dataset["lineage_mode"] == "lineage_index_v1"


def test_trends_merge_same_event_only_after_reviewed_promotion_gate(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    urls = {
        "origin": "https://source.example/model-launch",
        "same": "https://news.example/model-launch-report",
        "independent-a": "https://other.example/independent-a",
        "independent-b": "https://other.example/independent-b",
    }
    routes: dict[str, str] = {}
    for index, (name, url) in enumerate(urls.items()):
        path = _write_post(
            content_root,
            name,
            date=f"2026-07-16T{index + 7:02d}:00:00Z",
            tags=["Promotion Gate"],
            source=name,
            external_url=url,
        )
        routes[name] = f"/posts/{path.stem}/"
    manifest_path = tmp_path / "quality.json"
    write_content_quality_manifest(content_root, manifest_path)

    origin_id = _observation_id(urls["origin"])
    same_id = _observation_id(urls["same"])
    event_id = f"evt_{origin_id.removeprefix('obs_')}"
    observations = [
        {
            "observation_id": origin_id,
            "title": "Original model launch",
            "source": "origin",
            "source_url": urls["origin"],
            "article_url": routes["origin"],
            "relation": "original",
            "parent_observation_id": None,
            "source_published_at": "2026-07-16T07:00:00Z",
            "first_seen_at": "2026-07-16T07:05:00Z",
            "timestamp_confidence": "publisher",
        },
        {
            "observation_id": same_id,
            "title": "Independent report about the launch",
            "source": "same",
            "source_url": urls["same"],
            "article_url": routes["same"],
            "relation": "same_event",
            "parent_observation_id": origin_id,
            "source_published_at": "2026-07-16T08:00:00Z",
            "first_seen_at": "2026-07-16T08:05:00Z",
            "timestamp_confidence": "feed",
        },
    ]
    lineage_root = _write_lineage_assets(
        tmp_path,
        observations=observations,
        event_id=event_id,
    )

    unreviewed_output = tmp_path / "unreviewed"
    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        lineage_root=lineage_root,
        output_dir=unreviewed_output,
        as_of=AS_OF,
    )
    unreviewed_index = json.loads(
        (unreviewed_output / "index.json").read_text(encoding="utf-8")
    )
    unreviewed_window = json.loads(
        (unreviewed_output / unreviewed_index["windows"]["24h"]["path"]).read_text(
            encoding="utf-8"
        )
    )
    unreviewed = next(
        item for item in unreviewed_window["trends"] if item["id"] == "tag:Promotion Gate"
    )
    assert unreviewed["unique_events"] == 4
    assert unreviewed["observations"] == 4
    assert unreviewed_index["stats"]["promoted_same_event_pairs"] == 0

    config_payload = yaml.safe_load(
        Path("config/stack_trends.yaml").read_text(encoding="utf-8")
    )
    config_payload["same_event_promotions"] = [
        _reviewed_same_event_promotion(
            event_id=event_id,
            observation_id=same_id,
            parent_observation_id=origin_id,
        )
    ]
    config_path = tmp_path / "reviewed.yaml"
    config_path.write_text(yaml.safe_dump(config_payload), encoding="utf-8")

    reviewed_output = tmp_path / "reviewed"
    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        lineage_root=lineage_root,
        config_path=config_path,
        output_dir=reviewed_output,
        as_of=AS_OF,
    )
    reviewed_index = json.loads(
        (reviewed_output / "index.json").read_text(encoding="utf-8")
    )
    reviewed_window = json.loads(
        (reviewed_output / reviewed_index["windows"]["24h"]["path"]).read_text(
            encoding="utf-8"
        )
    )
    reviewed = next(
        item for item in reviewed_window["trends"] if item["id"] == "tag:Promotion Gate"
    )
    assert reviewed["unique_events"] == 3
    assert reviewed["observations"] == 4
    assert reviewed["redundant_observations"] == 1
    assert reviewed_index["stats"]["promoted_same_event_pairs"] == 1

    # A structurally qualified allowlist entry is still inactive before its
    # reviewed timestamp reaches this deterministic data snapshot.
    future_promotion = _reviewed_same_event_promotion(
        event_id=event_id,
        observation_id=same_id,
        parent_observation_id=origin_id,
    )
    future_promotion["reviewed_at"] = "2026-07-17T00:00:00Z"
    config_payload["same_event_promotions"] = [future_promotion]
    future_config_path = tmp_path / "future-reviewed.yaml"
    future_config_path.write_text(yaml.safe_dump(config_payload), encoding="utf-8")
    future_output = tmp_path / "future-reviewed"
    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        lineage_root=lineage_root,
        config_path=future_config_path,
        output_dir=future_output,
        as_of=AS_OF,
    )
    future_index = json.loads((future_output / "index.json").read_text(encoding="utf-8"))
    future_window = json.loads(
        (future_output / future_index["windows"]["24h"]["path"]).read_text(
            encoding="utf-8"
        )
    )
    future = next(
        item for item in future_window["trends"] if item["id"] == "tag:Promotion Gate"
    )
    assert future["unique_events"] == 4
    assert future["observations"] == 4
    assert future_index["stats"]["promoted_same_event_pairs"] == 0


def test_build_emits_v2_event_observation_metrics_and_verifier_accepts_v1(
    tmp_path: Path,
) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    output = tmp_path / "stack-trends"

    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=output,
        as_of=AS_OF,
    )
    index = json.loads((output / "index.json").read_text(encoding="utf-8"))
    window = json.loads(
        (output / index["windows"]["24h"]["path"]).read_text(encoding="utf-8")
    )
    topic = json.loads(
        (output / index["topics"]["tag:LLM"]["path"]).read_text(encoding="utf-8")
    )
    llm = next(item for item in window["trends"] if item["id"] == "tag:LLM")

    assert index["schema_version"] == INDEX_SCHEMA_VERSION_V2
    assert window["schema_version"] == WINDOW_SCHEMA_VERSION_V2
    assert topic["schema_version"] == TOPIC_SCHEMA_VERSION_V2
    assert llm["observations"] >= llm["unique_events"]
    assert llm["redundant_observations"] == llm["observations"] - llm["unique_events"]
    assert llm["source_diversity"] >= 1
    assert topic["evidence"][0]["associated_observations"] >= 1
    assert isinstance(topic["evidence"][0]["related_reports"], list)

    # Rollout fallback: the verifier must continue to accept committed v1 assets.
    committed = Path("blog/static/data/stack-trends")
    assert verify_stack_trends(committed, verify_hashes=True)["schema_version"] in {
        "stack_trends_index_v1",
        INDEX_SCHEMA_VERSION_V2,
    }


def test_adapter_rejects_a_stale_quality_manifest(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    _write_post(
        content_root,
        "after-manifest",
        date="2026-07-16T11:00:00Z",
        tags=["LLM"],
    )

    with pytest.raises(StackTrendsValidationError, match="stale"):
        adapt_posts_to_events(
            content_root=content_root,
            quality_manifest_path=manifest_path,
            as_of=AS_OF,
        )


def test_adapter_rejects_a_missing_noncomplete_quality_record(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    del manifest["pages"]["posts/archived.md"]
    manifest["archived_count"] -= 1
    manifest["complete_count"] += 1
    manifest["active_count"] += 1
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(StackTrendsValidationError, match="missing quality record"):
        adapt_posts_to_events(
            content_root=content_root,
            quality_manifest_path=manifest_path,
            as_of=AS_OF,
        )


def test_adapter_rejects_encoded_internal_route_traversal(tmp_path: Path) -> None:
    content_root, _manifest_path = _fixture_site(tmp_path)
    _write_post(
        content_root,
        "unsafe-route",
        date="2026-07-16T11:00:00Z",
        tags=["LLM"],
        url="/posts/%2e%2e/private/",
    )
    manifest_path = tmp_path / "content_quality.json"
    write_content_quality_manifest(content_root, manifest_path)

    with pytest.raises(StackTrendsValidationError, match="unsafe internal url"):
        adapt_posts_to_events(
            content_root=content_root,
            quality_manifest_path=manifest_path,
            as_of=AS_OF,
        )


def test_build_reuses_trend_formula_and_emits_v2_drilldown_contract(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    output = tmp_path / "stack-trends"

    result = build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=output,
        as_of=AS_OF,
    )
    index = json.loads((output / "index.json").read_text(encoding="utf-8"))
    window_ref = index["windows"]["24h"]
    window = json.loads((output / window_ref["path"]).read_text(encoding="utf-8"))
    llm = next(trend for trend in window["trends"] if trend["id"] == "tag:LLM")
    topic_ref = index["topics"]["tag:LLM"]
    topic = json.loads((output / topic_ref["path"]).read_text(encoding="utf-8"))

    dataset = adapt_posts_to_events(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        as_of=AS_OF,
    )
    expected = next(
        trend
        for trend in calculate_trends(dataset["events"], as_of=AS_OF)["windows"]["24h"]["trends"]
        if trend["topic"] == "LLM"
    )

    assert result["index_path"] == "index.json"
    assert index["schema_version"] == INDEX_SCHEMA_VERSION_V2
    assert index["default_window"] == "30d"
    assert index["realtime"] is False
    assert index["data_as_of"] == "2026-07-16T10:00:00Z"
    assert window["formula"] == index["formula"]
    assert llm["score"] == expected["score"]
    assert llm["components"] == expected["components"]
    assert llm["observations"] == expected["observations"]
    assert llm["duplicate_rate"] == expected["duplicate_rate"]
    assert llm["score"] == round(
        100
        * (
            0.25 * llm["components"]["quantity"]
            + 0.25 * llm["components"]["growth"]
            + 0.15 * llm["components"]["acceleration"]
            + 0.15 * llm["components"]["source_diversity"]
            + 0.10 * llm["components"]["novelty"]
            + 0.10 * llm["components"]["source_weight"]
        )
        * (1 - 0.5 * llm["duplicate_rate"]),
        6,
    )
    assert llm["counts"] == {"current": 3, "previous": 2, "pre_previous": 1}
    assert llm["state"] == "rising"
    assert llm["confidence"] == "medium"
    assert llm["graph_node_id"] == "tag:LLM"
    assert llm["detail_path"] == topic_ref["path"]
    assert all(item["topic"] != "ArXiv" for item in window["trends"])
    assert len(llm["sparkline"]) == 12
    assert sum(llm["sparkline"]) == 3

    assert topic["schema_version"] == TOPIC_SCHEMA_VERSION_V2
    assert topic["id"] == topic["graph_node_id"] == "tag:LLM"
    assert topic["related_topics"][0]["id"] == "tag:AI Agent"
    assert topic["related_topics"][0]["cooccurrence"] == 2
    assert set(topic["related_topics"][0]) == {
        "id",
        "topic",
        "graph_node_id",
        "cooccurrence",
        "jaccard",
    }
    assert topic["sources"][0]["count"] >= 1
    assert {item["name"]: item["count"] for item in topic["scenarios"]}["模型工程"] == 3
    evidence = topic["evidence"][0]
    assert set(evidence) == {
        "id",
        "observation_id",
        "title",
        "summary",
        "source",
        "published_at",
        "internal_url",
        "relation",
        "associated_observations",
        "related_reports",
    }
    assert evidence["internal_url"] == "/posts/llm-current-a/"
    assert all("example.com" not in json.dumps(item) for item in topic["evidence"])


def test_build_is_byte_stable_content_addressed_and_within_budgets(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    first = tmp_path / "first"
    second = tmp_path / "second"

    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=first,
        as_of=AS_OF,
    )
    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=second,
        as_of=AS_OF,
    )

    assert _tree_bytes(first) == _tree_bytes(second)
    index = json.loads((first / "index.json").read_text(encoding="utf-8"))
    assert (first / "index.json").stat().st_size <= 64 * 1024
    assert len(_tree_bytes(first)) <= 100
    assert sum(map(len, _tree_bytes(first).values())) <= 2 * 1024 * 1024
    for ref in [*index["windows"].values(), *index["topics"].values()]:
        body = (first / ref["path"]).read_bytes()
        assert ref["bytes"] == len(body)
        assert ref["sha256"] == hashlib.sha256(body).hexdigest()
        limit = 128 * 1024 if ref["path"].startswith("windows/") else 96 * 1024
        assert len(body) <= limit
        assert Path(ref["path"]).name.endswith(f"-{ref['sha256'][:12]}.json")


def test_build_rejects_secret_like_public_text_before_writing(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path, secret_description=True)
    output = tmp_path / "stack-trends"

    with pytest.raises(StackTrendsValidationError, match="sensitive"):
        build_stack_trends(
            content_root=content_root,
            quality_manifest_path=manifest_path,
            output_dir=output,
            as_of=AS_OF,
        )

    assert not (output / "index.json").exists()


def test_build_rejects_markup_like_public_text_before_writing(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path, unsafe_description=True)
    output = tmp_path / "stack-trends"

    with pytest.raises(StackTrendsValidationError, match="unsafe public text"):
        build_stack_trends(
            content_root=content_root,
            quality_manifest_path=manifest_path,
            output_dir=output,
            as_of=AS_OF,
        )

    assert not (output / "index.json").exists()


def test_verifier_rejects_hash_mismatch_and_orphans(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    output = tmp_path / "stack-trends"
    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=output,
        as_of=AS_OF,
    )

    verified = verify_stack_trends(output, verify_hashes=True)
    assert verified["file_count"] == len(_tree_bytes(output))

    index = json.loads((output / "index.json").read_text(encoding="utf-8"))
    window_path = output / index["windows"]["30d"]["path"]
    window_path.write_text("{}\n", encoding="utf-8")
    with pytest.raises(StackTrendsValidationError, match="sha256|byte size"):
        verify_stack_trends(output, verify_hashes=True)

    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=output,
        as_of=AS_OF,
    )
    (output / "topics" / "orphan.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(StackTrendsValidationError, match="orphan"):
        verify_stack_trends(output, verify_hashes=True)


@pytest.mark.parametrize(
    ("collection", "identity", "mutate", "reason"),
    [
        (
            "windows",
            "30d",
            lambda payload: payload.__setitem__("window", "7d"),
            "window identity",
        ),
        (
            "windows",
            "30d",
            lambda payload: payload.__setitem__("data_as_of", "2026-07-15T10:00:00Z"),
            "data_as_of",
        ),
        (
            "windows",
            "30d",
            lambda payload: payload["trends"][0].__setitem__(
                "detail_path", "topics/not-indexed.json"
            ),
            "detail_path",
        ),
        (
            "topics",
            "tag:LLM",
            lambda payload: payload.__setitem__("id", "tag:Wrong"),
            "topic identity",
        ),
        (
            "topics",
            "tag:LLM",
            lambda payload: payload.__setitem__("data_as_of", "2026-07-15T10:00:00Z"),
            "data_as_of",
        ),
    ],
)
def test_verifier_rejects_semantically_swapped_or_detached_shards(
    tmp_path: Path,
    collection: str,
    identity: str,
    mutate: Callable[[dict[str, object]], None],
    reason: str,
) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    output = tmp_path / "stack-trends"
    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=output,
        as_of=AS_OF,
    )
    _rewrite_referenced_asset(
        output,
        collection=collection,
        identity=identity,
        mutate=mutate,
    )

    with pytest.raises(StackTrendsValidationError, match=reason):
        verify_stack_trends(output, verify_hashes=True)


@pytest.mark.parametrize("tamper", ["reference", "stats"])
def test_verifier_cross_checks_window_trend_count(
    tmp_path: Path,
    tamper: str,
) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    output = tmp_path / "stack-trends"
    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=output,
        as_of=AS_OF,
    )
    index_path = output / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if tamper == "reference":
        index["windows"]["30d"]["trend_count"] += 1
    else:
        index["stats"]["windows"]["30d"]["trend_count"] += 1
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(StackTrendsValidationError, match="trend_count"):
        verify_stack_trends(output, verify_hashes=True)


def test_verifier_requires_deterministic_release_timestamp_identity(tmp_path: Path) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    output = tmp_path / "stack-trends"
    build_stack_trends(
        content_root=content_root,
        quality_manifest_path=manifest_path,
        output_dir=output,
        as_of=AS_OF,
    )
    index_path = output / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["generated_at"] = "2026-07-16T12:00:00Z"
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(StackTrendsValidationError, match="generated_at.*data_as_of"):
        verify_stack_trends(output, verify_hashes=True)


def test_build_and_verify_cli_contract(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    content_root, manifest_path = _fixture_site(tmp_path)
    output = tmp_path / "stack-trends"

    build_exit = build_cli_main(
        [
            "--content-root",
            str(content_root),
            "--quality-manifest",
            str(manifest_path),
            "--output",
            str(output),
            "--as-of",
            AS_OF,
        ]
    )
    build_result = json.loads(capsys.readouterr().out)
    verify_exit = verify_cli_main(
        ["--root", str(output), "--verify-hashes"]
    )
    verify_result = json.loads(capsys.readouterr().out)

    assert build_exit == 0
    assert build_result["index_path"] == "index.json"
    assert verify_exit == 0
    assert verify_result["schema_version"] == INDEX_SCHEMA_VERSION_V2
