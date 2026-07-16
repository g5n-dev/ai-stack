from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

from ai_stack.content_quality import write_content_quality_manifest
from processor.intelligence import calculate_trends
from processor.stack_trends import (
    StackTrendsValidationError,
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
            tags=["LLM", "来源快报", "arXiv" if source == "arxiv" else "博客与播客"],
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
    assert "来源快报" in config.excluded_tags
    assert "arXiv" in config.excluded_tags
    assert "Intermediate (200)" in config.excluded_tags
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
    assert all("arXiv" not in event["topics"] for event in events)
    assert any("AI 编程" in event["topics"] for event in events)
    assert all("external_url" not in event for event in events)
    assert all("path" not in key for event in events for key in event)
    assert not any(event["title"] == "Evidence draft" for event in events)
    assert not any(event["title"] == "Evidence future" for event in events)
    assert not any(event["title"] == "Evidence archived" for event in events)


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


def test_build_reuses_trend_v1_and_emits_drilldown_contract(tmp_path: Path) -> None:
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
    assert index["schema_version"] == "stack_trends_index_v1"
    assert index["default_window"] == "30d"
    assert index["realtime"] is False
    assert index["data_as_of"] == "2026-07-16T10:00:00Z"
    assert llm["score"] == expected["score"]
    assert llm["components"] == expected["components"]
    assert llm["counts"] == {"current": 3, "previous": 2, "pre_previous": 1}
    assert llm["state"] == "rising"
    assert llm["confidence"] == "medium"
    assert llm["graph_node_id"] == "tag:LLM"
    assert llm["detail_path"] == topic_ref["path"]
    assert len(llm["sparkline"]) == 12
    assert sum(llm["sparkline"]) == 3

    assert topic["schema_version"] == "stack_trends_topic_v1"
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
        "title",
        "summary",
        "source",
        "published_at",
        "internal_url",
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
    assert verify_result["schema_version"] == "stack_trends_index_v1"
