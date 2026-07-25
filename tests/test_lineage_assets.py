from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from ai_stack.lineage import (
    LineageRegistry,
    LineageValidationError,
    ObservationInput,
    RelationKind,
    TimestampConfidence,
    apply_lineage_post_metadata,
    build_lineage_assets,
    parse_historical_post,
    verify_lineage_assets,
)
from ai_stack.lineage import _safe_asset_path


def _source_text(start: int, stop: int) -> str:
    return " ".join(f"evidence{index}" for index in range(start, stop))


def _post(
    *,
    title: str,
    url: str,
    excerpt: str,
    date: str,
    mode: str = "full_text",
    completeness: str = "complete",
    truncated: bool = False,
    body_prefix: str = "AI_REWRITTEN_SECRET must never become lineage evidence.",
) -> str:
    return f"""---
title: {json.dumps(title, ensure_ascii=False)}
date: {date}
draft: false
entry_kind: auto
source: fixture
external_url: {url}
source_capture_mode: {mode}
source_completeness: {completeness}
source_is_truncated: {str(truncated).lower()}
source_payload_sha256: sha256:{"a" * 64}
source_published_at: {date}
timestamp_confidence: publisher
---

## AI 转写正文

{body_prefix}

## 来源摘要/节选

> {excerpt}

## 来源说明

Only the bounded source excerpt above is evidence.
"""


def _write_fixture_posts(root: Path) -> list[Path]:
    posts = root / "posts"
    posts.mkdir(parents=True)
    exact = _source_text(0, 220)
    values = [
        (
            "a.md",
            _post(
                title="Agent Runtime launch",
                url="https://publisher.example/runtime",
                excerpt=exact,
                date="2026-07-01T08:00:00Z",
            ),
        ),
        (
            "b.md",
            _post(
                title="Agent Runtime launch",
                url="https://mirror.example/runtime",
                excerpt=exact,
                date="2026-07-01T09:00:00Z",
            ),
        ),
        (
            "metadata.md",
            _post(
                title="Independent metadata item",
                url="https://metadata.example/item",
                excerpt="metadata title only",
                date="2026-07-02T08:00:00Z",
                mode="metadata_only",
                completeness="metadata_only",
            ),
        ),
    ]
    paths = []
    for name, content in values:
        path = posts / name
        path.write_text(content, encoding="utf-8")
        paths.append(path)
    return paths


def _tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_historical_parser_uses_only_bounded_source_excerpt_and_source_metadata(
    tmp_path: Path,
) -> None:
    path = tmp_path / "post.md"
    path.write_text(
        _post(
            title="安全来源",
            url="HTTPS://Example.com:443/story/?utm_source=feed",
            excerpt="公开来源中的真实证据片段，人工智能推动工程实践。",
            date="2026-07-01T08:00:00Z",
        ),
        encoding="utf-8",
    )

    observation = parse_historical_post(
        path,
        content_root=tmp_path,
        first_seen_at="2026-07-03T10:00:00Z",
        last_seen_at="2026-07-20T00:00:00Z",
    )

    assert observation is not None
    assert observation.canonical_url == "https://example.com/story"
    assert observation.source_text == "公开来源中的真实证据片段，人工智能推动工程实践。"
    assert "AI_REWRITTEN_SECRET" not in observation.source_text
    assert observation.source_published_at == "2026-07-01T08:00:00Z"
    assert observation.first_seen_at == "2026-07-03T10:00:00Z"


def test_historical_archived_flag_is_audited_but_never_active(tmp_path: Path) -> None:
    path = tmp_path / "archived.md"
    path.write_text(
        _post(
            title="Archived evidence",
            url="https://example.com/archived",
            excerpt=_source_text(0, 100),
            date="2026-07-01T08:00:00Z",
        ).replace("draft: false\n", "draft: false\narchived: true\n"),
        encoding="utf-8",
    )

    observation = parse_historical_post(path, content_root=tmp_path)

    assert observation is not None
    assert observation.active is False


def test_archived_observation_stays_internal_and_is_absent_from_public_assets(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    paths = _write_fixture_posts(content_root)
    archived = paths[-1]
    archived.write_text(
        archived.read_text(encoding="utf-8").replace(
            "draft: false\n", "draft: false\narchived: true\n"
        ),
        encoding="utf-8",
    )
    internal = tmp_path / "internal"
    public = tmp_path / "public"

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )

    registry = LineageRegistry.load(internal)
    archived_record = next(record for record in registry._records.values() if not record["active"])
    index = json.loads((public / "index.json").read_text(encoding="utf-8"))
    public_ids: set[str] = set()
    for reference in index["route_buckets"]:
        shard = json.loads((public / reference["path"]).read_text(encoding="utf-8"))
        public_ids.update(route["observation_id"] for route in shard["routes"])

    assert len(registry._records) == 3
    assert index["stats"]["observations"] == 2
    assert archived_record["observation_id"] not in public_ids


def test_build_writes_128_deterministic_internal_and_content_addressed_public_shards(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    paths = _write_fixture_posts(content_root)
    first_seen = {
        path.resolve(): f"2026-07-0{index + 1}T10:00:00Z" for index, path in enumerate(paths)
    }
    internal_one = tmp_path / "internal-one"
    public_one = tmp_path / "public-one"
    internal_two = tmp_path / "internal-two"
    public_two = tmp_path / "public-two"

    first = build_lineage_assets(
        content_root=content_root,
        internal_dir=internal_one,
        public_dir=public_one,
        as_of="2026-07-20T00:00:00Z",
        first_seen_by_path=first_seen,
    )
    second = build_lineage_assets(
        content_root=content_root,
        internal_dir=internal_two,
        public_dir=public_two,
        as_of="2026-07-20T00:00:00Z",
        first_seen_by_path=first_seen,
    )

    assert first == second
    assert _tree_bytes(internal_one) == _tree_bytes(internal_two)
    assert _tree_bytes(public_one) == _tree_bytes(public_two)
    assert len(list((internal_one / "registry").glob("*.json"))) == 128

    index = json.loads((public_one / "index.json").read_text(encoding="utf-8"))
    assert index["schema"] == "lineage_index_v1"
    assert index["bucket_count"] == 128
    assert index["bucket_algorithm"] == "sha256_prefix32_mod_v1"
    assert len(index["route_buckets"]) == 128
    assert len(index["cluster_buckets"]) == 128
    assert all("-" in Path(item["path"]).stem for item in index["route_buckets"])
    assert index["stats"]["observations"] == 3
    assert index["stats"]["events"] == 2
    assert index["stats"]["exact_copies"] == 1

    routes = []
    for item in index["route_buckets"]:
        shard = json.loads((public_one / item["path"]).read_text(encoding="utf-8"))
        routes.extend(shard["routes"])
    assert routes
    assert all(set(route) == {"event_id", "observation_id"} for route in routes)

    all_public = b"".join(_tree_bytes(public_one).values())
    all_internal = b"".join(_tree_bytes(internal_one).values())
    assert b"AI_REWRITTEN_SECRET" not in all_public
    assert b"AI_REWRITTEN_SECRET" not in all_internal
    assert b"evidence100" not in all_public
    assert b"evidence100" not in all_internal

    report = verify_lineage_assets(
        public_one,
        internal_dir=internal_one,
        verify_hashes=True,
    )
    assert report["valid"] is True
    assert report["observations"] == 3


def test_existing_git_observation_time_survives_a_shallow_rebuild(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    post = content_root / "posts" / "historical.md"
    post.parent.mkdir(parents=True)
    post.write_text(
        """---
title: Historical signal
date: 2026-02-17T14:35:47Z
draft: false
source: fixture
external_url: https://example.com/historical-signal
source_capture_mode: metadata_only
source_completeness: metadata_only
source_is_truncated: false
---

## 来源摘要/节选

> Historical source metadata.
""",
        encoding="utf-8",
    )
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    git_seen = "2026-07-10T00:28:17Z"

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
        first_seen_by_path={post.resolve(): git_seen},
    )
    internal_before = _tree_bytes(internal)
    public_before = _tree_bytes(public)

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
        first_seen_by_path={},
    )

    assert _tree_bytes(internal) == internal_before
    assert _tree_bytes(public) == public_before
    record = next(iter(LineageRegistry.load(internal)._records.values()))
    assert record["first_seen_at"] == git_seen
    assert record["timestamp_confidence"] == TimestampConfidence.GIT.value


@pytest.mark.parametrize(
    ("confidence", "git_seen"),
    [
        (TimestampConfidence.UNKNOWN, "2026-07-20T08:00:00Z"),
        (TimestampConfidence.OBSERVED, "2026-07-20T08:00:00Z"),
        (TimestampConfidence.OBSERVED, "2026-07-20T09:00:00Z"),
    ],
)
def test_non_earlier_git_time_does_not_relabel_persisted_observation(
    tmp_path: Path,
    confidence: TimestampConfidence,
    git_seen: str,
) -> None:
    content_root = tmp_path / "content"
    post = content_root / "posts" / "new-signal.md"
    post.parent.mkdir(parents=True)
    first_seen = "2026-07-20T08:00:00Z"
    post.write_text(
        f"""---
title: Newly observed signal
date: {first_seen}
draft: false
source: fixture
external_url: https://example.com/new-signal
source_capture_mode: metadata_only
source_completeness: metadata_only
source_is_truncated: false
first_seen_at: {first_seen}
timestamp_confidence: {confidence.value}
---

## 来源摘要/节选

> Newly observed source metadata.
""",
        encoding="utf-8",
    )
    internal = tmp_path / "internal"
    public = tmp_path / "public"

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of=first_seen,
        first_seen_by_path={},
    )
    first_apply = apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )
    assert first_apply["changed"] == 1
    internal_before = _tree_bytes(internal)
    public_before = _tree_bytes(public)
    post_before = post.read_bytes()

    # The persist commit introduces the path only after the first build. Full
    # Git history must not make the committed validation build change again.
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of=first_seen,
        first_seen_by_path={post.resolve(): git_seen},
    )
    second_apply = apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )

    assert second_apply["changed"] == 0
    assert _tree_bytes(internal) == internal_before
    assert _tree_bytes(public) == public_before
    assert post.read_bytes() == post_before
    record = next(iter(LineageRegistry.load(internal)._records.values()))
    assert record["first_seen_at"] == first_seen
    assert record["timestamp_confidence"] == confidence.value


def test_public_cluster_schema_exposes_safe_timeline_and_duplicate_relation(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    _write_fixture_posts(content_root)
    internal = tmp_path / "internal"
    public = tmp_path / "public"

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )

    index = json.loads((public / "index.json").read_text(encoding="utf-8"))
    clusters = []
    for item in index["cluster_buckets"]:
        shard = json.loads((public / item["path"]).read_text(encoding="utf-8"))
        clusters.extend(shard["clusters"])
    duplicate_cluster = next(cluster for cluster in clusters if len(cluster["observations"]) == 2)
    relations = {entry["relation"] for entry in duplicate_cluster["observations"]}

    assert relations == {RelationKind.ORIGINAL.value, RelationKind.EXACT_COPY.value}
    assert duplicate_cluster["earliest_observed_id"]
    assert duplicate_cluster["probable_origin_id"]
    assert duplicate_cluster["representative_article_url"].startswith("/posts/")
    assert duplicate_cluster["lineage_links"] == []
    for entry in duplicate_cluster["observations"]:
        assert set(entry) == {
            "article_url",
            "first_seen_at",
            "observation_id",
            "parent_observation_id",
            "relation",
            "source",
            "source_published_at",
            "source_url",
            "timestamp_confidence",
            "title",
        }


def test_derivative_cluster_contains_bounded_cross_event_parent_preview(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    original_text = _source_text(0, 220)
    derivative_text = _source_text(0, 440)
    (posts / "original.md").write_text(
        _post(
            title="Agent Runtime architecture",
            url="https://publisher.example/agent-runtime",
            excerpt=original_text,
            date="2026-07-01T08:00:00Z",
        ),
        encoding="utf-8",
    )
    (posts / "derivative.md").write_text(
        _post(
            title="Agent Runtime architecture explained",
            url="https://analysis.example/agent-runtime",
            excerpt=derivative_text,
            date="2026-07-02T08:00:00Z",
        ),
        encoding="utf-8",
    )
    internal = tmp_path / "internal"
    public = tmp_path / "public"

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )

    index = json.loads((public / "index.json").read_text(encoding="utf-8"))
    clusters = []
    for reference in index["cluster_buckets"]:
        shard = json.loads((public / reference["path"]).read_text(encoding="utf-8"))
        clusters.extend(shard["clusters"])
    derivative_cluster = next(
        cluster
        for cluster in clusters
        if cluster["observations"][0]["relation"] == RelationKind.DERIVATIVE.value
    )
    derivative = derivative_cluster["observations"][0]
    link = derivative_cluster["lineage_links"][0]

    assert len(derivative_cluster["lineage_links"]) == 1
    assert link["from_observation_id"] == derivative["observation_id"]
    assert link["relation"] == RelationKind.DERIVATIVE.value
    assert link["target"]["source_url"] == "https://publisher.example/agent-runtime"
    assert link["target"]["observation_id"] == derivative["parent_observation_id"]


def test_verifier_rejects_tampered_or_oversized_referenced_shard(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    _write_fixture_posts(content_root)
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    index = json.loads((public / "index.json").read_text(encoding="utf-8"))
    shard = public / index["route_buckets"][0]["path"]
    shard.write_text('{"tampered":true}', encoding="utf-8")

    with pytest.raises(LineageValidationError, match="hash"):
        verify_lineage_assets(public, internal_dir=internal, verify_hashes=True)


def test_build_rejects_public_text_that_looks_like_a_secret(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    (posts / "leak.md").write_text(
        _post(
            title="Leaky key " + "sk-" + "abcdefghijklmnopqrstuvwxyz123456",
            url="https://example.com/leak",
            excerpt=_source_text(0, 100),
            date="2026-07-01T08:00:00Z",
        ),
        encoding="utf-8",
    )

    with pytest.raises(LineageValidationError, match="secret"):
        build_lineage_assets(
            content_root=content_root,
            internal_dir=tmp_path / "internal",
            public_dir=tmp_path / "public",
            as_of="2026-07-20T00:00:00Z",
        )


@pytest.mark.parametrize(
    "query",
    [
        "token=top-secret",
        "code=oauth-code",
        "key=private-key",
        "sig=signed-value",
        "session=session-value",
        "X-Amz-Credential=credential-value",
        "X-Amz-Signature=signature-value",
        "jwtToken=jwt-value",
        "sessionId=session-id-value",
        "accessToken=access-value",
        "authToken=auth-value",
        "AWSAccessKeyId=aws-key-value",
        "signedUrl=signed-url-value",
        "jwt-Token=mixed-delimiter-value",
        "signed.URL=mixed-signed-url-value",
    ],
)
def test_build_strips_secret_bearing_query_key_variants_everywhere(
    tmp_path: Path,
    query: str,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    (posts / "signed.md").write_text(
        _post(
            title="Signed source URL",
            url=f"https://example.com/story?{query}",
            excerpt=_source_text(0, 100),
            date="2026-07-01T08:00:00Z",
        )
        + f"\n[原始来源](https://example.com/story?view=full&{query})\n",
        encoding="utf-8",
    )

    internal = tmp_path / "internal"
    public = tmp_path / "public"
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )

    registry_payload = b"".join(path.read_bytes() for path in internal.rglob("*.json"))
    public_payload = b"".join(path.read_bytes() for path in public.rglob("*.json"))
    markdown = (posts / "signed.md").read_bytes()
    secret_value = query.split("=", 1)[1].encode()
    assert secret_value not in registry_payload
    assert secret_value not in public_payload
    assert secret_value not in markdown
    assert b"external_url: https://example.com/story" in markdown
    assert b"https://example.com/story?view=full" in markdown


def test_build_preserves_non_sensitive_source_query_parameters(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    source_url = (
        "https://example.com/story?id=42&v=3&post=agent&"
        "abstract_id=7&langVersion=zh-CN"
    )
    (posts / "ordinary-query.md").write_text(
        _post(
            title="Ordinary source query",
            url=source_url,
            excerpt=_source_text(0, 100),
            date="2026-07-01T08:00:00Z",
        )
        + f"\n[原始来源]({source_url})\n",
        encoding="utf-8",
    )

    internal = tmp_path / "internal"
    public = tmp_path / "public"
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )

    markdown = (posts / "ordinary-query.md").read_text(encoding="utf-8")
    assert source_url in markdown


def test_safe_asset_path_rejects_lexical_symlink_inside_root(tmp_path: Path) -> None:
    real = tmp_path / "real.json"
    alias = tmp_path / "alias.json"
    real.write_text("{}", encoding="utf-8")
    alias.symlink_to(real)

    with pytest.raises(LineageValidationError, match="symlink"):
        _safe_asset_path(tmp_path, "alias.json")


def test_build_preserves_newer_refresh_revision_and_last_seen(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    old_text = _source_text(0, 180)
    post = posts / "revision.md"
    post.write_text(
        _post(
            title="Agent revision",
            url="https://publisher.example/revision",
            excerpt=old_text,
            date="2026-07-01T08:00:00Z",
        ),
        encoding="utf-8",
    )
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    registry = LineageRegistry.load(internal)
    historical = parse_historical_post(post, content_root=content_root)
    assert historical is not None
    refreshed = replace(
        historical,
        source_text=_source_text(0, 240),
        last_seen_at="2026-07-21T00:00:00Z",
    )
    refreshed_result = registry.resolve_batch([refreshed]).items[0]
    registry.save(internal, generated_at="2026-07-21T12:00:00Z")

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-22T00:00:00Z",
    )

    rebuilt = LineageRegistry.load(internal)
    record = rebuilt._records[refreshed.observation_id]
    public_index = json.loads((public / "index.json").read_text(encoding="utf-8"))
    assert record["revision_id"] == refreshed_result.revision_id
    assert record["last_seen_at"] == "2026-07-21T00:00:00Z"
    assert public_index["generated_at"] == "2026-07-22T00:00:00Z"


def test_build_preserves_refresh_revision_after_equal_day_metadata_backfill(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    post = posts / "equal-day-revision.md"
    post.write_text(
        _post(
            title="Equal-day agent revision",
            url="https://publisher.example/equal-day-revision",
            excerpt=_source_text(0, 180),
            date="2026-07-01T08:00:00Z",
        ),
        encoding="utf-8",
    )
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    registry = LineageRegistry.load(internal)
    historical = parse_historical_post(post, content_root=content_root)
    assert historical is not None
    refreshed = replace(
        historical,
        source_text=_source_text(0, 240),
        source_payload_sha256="sha256:" + "b" * 64,
        last_seen_at="2026-07-21T00:00:00Z",
    )
    refreshed_result = registry.resolve_batch([refreshed]).items[0]
    registry.save(internal, generated_at="2026-07-21T12:00:00Z")

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-22T00:00:00Z",
    )
    first_apply = apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )
    assert first_apply["changed"] == 1
    first_internal = {
        path.relative_to(internal): path.read_bytes()
        for path in sorted(internal.rglob("*.json"))
    }
    first_public = {
        path.relative_to(public): path.read_bytes()
        for path in sorted(public.rglob("*.json"))
    }

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-22T00:00:00Z",
    )
    second_apply = apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )

    rebuilt = LineageRegistry.load(internal)
    record = rebuilt._records[refreshed.observation_id]
    assert record["revision_id"] == refreshed_result.revision_id
    assert record["source_payload_sha256"] == "sha256:" + "b" * 64
    assert record["last_seen_at"] == "2026-07-21T00:00:00Z"
    assert second_apply == {"changed": 0, "deleted": 0, "scanned": 1}
    assert {
        path.relative_to(internal): path.read_bytes()
        for path in sorted(internal.rglob("*.json"))
    } == first_internal
    assert {
        path.relative_to(public): path.read_bytes()
        for path in sorted(public.rglob("*.json"))
    } == first_public


def test_strictly_newer_posts_can_merge_events_and_keep_aliases_stable(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    first = ObservationInput(
        canonical_url="https://origin.example/a",
        title="Stable event merge",
        source_text=_source_text(0, 180),
        source="fixture",
        article_path="posts/a.md",
        capture_mode="full_text",
        source_completeness="complete",
        source_published_at="2026-07-01T00:00:00Z",
        first_seen_at="2026-07-01T01:00:00Z",
        last_seen_at="2026-07-01T01:00:00Z",
        timestamp_confidence=TimestampConfidence.PUBLISHER,
    )
    second = ObservationInput(
        canonical_url="https://origin.example/b",
        title="Stable event merge",
        source_text=_source_text(500, 680),
        source="fixture",
        article_path="posts/b.md",
        capture_mode="full_text",
        source_completeness="complete",
        source_published_at="2026-07-02T00:00:00Z",
        first_seen_at="2026-07-02T01:00:00Z",
        last_seen_at="2026-07-02T01:00:00Z",
        timestamp_confidence=TimestampConfidence.PUBLISHER,
    )
    registry = LineageRegistry()
    first_batch = registry.resolve_batch([first, second])
    first_event, second_event = (item.event_id for item in first_batch.items)
    assert first_event != second_event
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    registry.save(internal, generated_at="2026-07-02T02:00:00Z")
    merged_text = _source_text(0, 220)
    for name, url, date in (
        ("a.md", first.canonical_url, "2026-07-01T00:00:00Z"),
        ("b.md", second.canonical_url, "2026-07-02T00:00:00Z"),
    ):
        markdown = _post(title="Stable event merge", url=url, excerpt=merged_text, date=date)
        markdown = markdown.replace(
            "timestamp_confidence: publisher\n",
            "timestamp_confidence: publisher\nlast_seen_at: 2026-07-03T00:00:00Z\n",
        )
        (posts / name).write_text(
            markdown,
            encoding="utf-8",
        )

    for as_of in ("2026-07-20T00:00:00Z", "2026-07-21T00:00:00Z"):
        build_lineage_assets(
            content_root=content_root,
            internal_dir=internal,
            public_dir=public,
            as_of=as_of,
        )
        rebuilt = LineageRegistry.load(internal)
        assert {record["event_id"] for record in rebuilt._records.values()} == {first_event}
        assert all(
            record["event_aliases"] == [second_event]
            for record in rebuilt._records.values()
        )
        index = json.loads((public / "index.json").read_text(encoding="utf-8"))
        clusters = []
        for reference in index["cluster_buckets"]:
            shard = json.loads((public / reference["path"]).read_text(encoding="utf-8"))
            clusters.extend(shard["clusters"])
        cluster = next(item for item in clusters if item["event_id"] == first_event)
        assert cluster["event_aliases"] == [second_event]


def test_equal_day_registry_evidence_prevents_post_excerpt_topology_merge(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    first = ObservationInput(
        canonical_url="https://origin.example/equal-day-a",
        title="Equal-day topology",
        source_text=_source_text(0, 180),
        source="fixture",
        article_path="posts/a.md",
        capture_mode="full_text",
        source_completeness="complete",
        source_published_at="2026-07-01T00:00:00Z",
        first_seen_at="2026-07-01T01:00:00Z",
        last_seen_at="2026-07-01T01:00:00Z",
        timestamp_confidence=TimestampConfidence.PUBLISHER,
    )
    second = replace(
        first,
        canonical_url="https://origin.example/equal-day-b",
        source_text=_source_text(500, 680),
        article_path="posts/b.md",
        source_published_at="2026-07-02T00:00:00Z",
        first_seen_at="2026-07-02T01:00:00Z",
        last_seen_at="2026-07-02T01:00:00Z",
    )
    registry = LineageRegistry()
    first_batch = registry.resolve_batch([first, second])
    original_events = {item.observation_id: item.event_id for item in first_batch.items}
    original_relations = {
        item.observation_id: item.relation.value for item in first_batch.items
    }
    original_parents = {
        item.observation_id: item.parent_observation_id for item in first_batch.items
    }
    assert len(set(original_events.values())) == 2
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    registry.save(internal, generated_at="2026-07-02T02:00:00Z")
    publication_excerpt = _source_text(900, 1120)
    for name, observation in (("a.md", first), ("b.md", second)):
        (posts / name).write_text(
            _post(
                title=observation.title,
                url=observation.canonical_url,
                excerpt=publication_excerpt,
                date=observation.source_published_at or "",
            ),
            encoding="utf-8",
        )

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    first_internal = {
        path.relative_to(internal): path.read_bytes()
        for path in sorted(internal.rglob("*.json"))
    }
    first_public = {
        path.relative_to(public): path.read_bytes()
        for path in sorted(public.rglob("*.json"))
    }
    rebuilt = LineageRegistry.load(internal)
    assert {
        identifier: record["event_id"]
        for identifier, record in rebuilt._records.items()
    } == original_events
    assert {
        identifier: record["relation"]
        for identifier, record in rebuilt._records.items()
    } == original_relations
    assert {
        identifier: record["parent_observation_id"]
        for identifier, record in rebuilt._records.items()
    } == original_parents
    assert all(record["event_aliases"] == [] for record in rebuilt._records.values())

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    assert {
        path.relative_to(internal): path.read_bytes()
        for path in sorted(internal.rglob("*.json"))
    } == first_internal
    assert {
        path.relative_to(public): path.read_bytes()
        for path in sorted(public.rglob("*.json"))
    } == first_public


def test_existing_syndicated_edge_survives_a_new_exact_event_member(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    origin = ObservationInput(
        canonical_url="https://origin.example/growing-event",
        title="Growing intelligence event",
        source_text=_source_text(0, 220),
        source="fixture",
        article_path="posts/origin.md",
        capture_mode="full_text",
        source_completeness="complete",
        source_published_at="2026-07-01T08:00:00Z",
        first_seen_at="2026-07-01T08:30:00Z",
        last_seen_at="2026-07-20T00:00:00Z",
        timestamp_confidence=TimestampConfidence.PUBLISHER,
    )
    syndicated = replace(
        origin,
        canonical_url="https://syndicator.example/growing-event",
        source_text=_source_text(0, 223),
        article_path="posts/syndicated.md",
        source_published_at="2026-07-01T10:00:00Z",
        first_seen_at="2026-07-01T10:30:00Z",
    )
    registry = LineageRegistry()
    initial = registry.resolve_batch([syndicated], historical_baseline=[origin])
    syndicated_result = initial.items[0]
    assert syndicated_result.relation is RelationKind.SYNDICATED
    assert syndicated_result.parent_observation_id == origin.observation_id
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    registry.save(internal, generated_at="2026-07-20T00:00:00Z")

    for name, observation in (("origin.md", origin), ("syndicated.md", syndicated)):
        markdown = _post(
            title=observation.title,
            url=observation.canonical_url,
            excerpt=observation.source_text,
            date=observation.source_published_at or "",
        ).replace(
            "timestamp_confidence: publisher\n",
            "timestamp_confidence: publisher\nlast_seen_at: 2026-07-20T00:00:00Z\n",
        )
        (posts / name).write_text(markdown, encoding="utf-8")
    newcomer = replace(
        origin,
        canonical_url="https://mirror.example/growing-event",
        article_path="posts/new-exact.md",
        source_published_at="2026-07-01T12:00:00Z",
        first_seen_at="2026-07-01T12:30:00Z",
        last_seen_at="2026-07-01T12:30:00Z",
    )
    (posts / "new-exact.md").write_text(
        _post(
            title=newcomer.title,
            url=newcomer.canonical_url,
            excerpt=newcomer.source_text,
            date=newcomer.source_published_at or "",
        ),
        encoding="utf-8",
    )

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-21T00:00:00Z",
    )

    rebuilt = LineageRegistry.load(internal)._records
    assert rebuilt[syndicated.observation_id]["relation"] == "syndicated"
    assert (
        rebuilt[syndicated.observation_id]["parent_observation_id"]
        == origin.observation_id
    )
    assert rebuilt[newcomer.observation_id]["relation"] == "exact_copy"
    assert rebuilt[newcomer.observation_id]["event_id"] == rebuilt[origin.observation_id][
        "event_id"
    ]


def test_trusted_earlier_git_time_drives_authoritative_event_order(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    origin = ObservationInput(
        canonical_url="https://origin.example/git-ordered-event",
        title="Git ordered intelligence event",
        source_text=_source_text(0, 220),
        source="fixture",
        article_path="posts/origin.md",
        capture_mode="full_text",
        source_completeness="complete",
        source_published_at=None,
        first_seen_at="2026-07-05T00:00:00Z",
        last_seen_at="2026-07-20T00:00:00Z",
        timestamp_confidence=TimestampConfidence.OBSERVED,
    )
    registry = LineageRegistry()
    registry.resolve_batch([], historical_baseline=[origin])
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    registry.save(internal, generated_at="2026-07-20T00:00:00Z")

    origin_post = _post(
        title=origin.title,
        url=origin.canonical_url,
        excerpt=origin.source_text,
        date="2026-07-05T00:00:00Z",
    ).replace(
        "source_published_at: 2026-07-05T00:00:00Z\n"
        "timestamp_confidence: publisher\n",
        "source_published_at:\n"
        "timestamp_confidence: observed\n"
        "last_seen_at: 2026-07-20T00:00:00Z\n",
    )
    origin_path = posts / "origin.md"
    origin_path.write_text(origin_post, encoding="utf-8")
    mirror = replace(
        origin,
        canonical_url="https://mirror.example/git-ordered-event",
        article_path="posts/mirror.md",
        first_seen_at="2026-07-03T00:00:00Z",
        last_seen_at="2026-07-03T00:00:00Z",
    )
    mirror_post = _post(
        title=mirror.title,
        url=mirror.canonical_url,
        excerpt=mirror.source_text,
        date="2026-07-03T00:00:00Z",
    ).replace(
        "source_published_at: 2026-07-03T00:00:00Z\n"
        "timestamp_confidence: publisher\n",
        "source_published_at:\n"
        "timestamp_confidence: observed\n",
    )
    (posts / "mirror.md").write_text(mirror_post, encoding="utf-8")

    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-21T00:00:00Z",
        first_seen_by_path={origin_path.resolve(): "2026-07-01T00:00:00Z"},
    )

    rebuilt = LineageRegistry.load(internal)._records
    assert rebuilt[origin.observation_id]["first_seen_at"] == "2026-07-01T00:00:00Z"
    assert rebuilt[origin.observation_id]["timestamp_confidence"] == "git"
    assert rebuilt[origin.observation_id]["relation"] == "original"
    assert rebuilt[mirror.observation_id]["relation"] == "exact_copy"
    assert rebuilt[mirror.observation_id]["parent_observation_id"] == origin.observation_id


def test_explicit_post_metadata_apply_is_non_destructive_and_idempotent(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    paths = _write_fixture_posts(content_root)
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    before = _tree_bytes(content_root)

    dry_run = apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=False,
    )
    assert dry_run["changed"] == 3
    assert _tree_bytes(content_root) == before

    applied = apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )
    assert applied == {"changed": 3, "deleted": 0, "scanned": 3}
    assert {path.name for path in paths} == {
        path.name for path in (content_root / "posts").glob("*.md")
    }
    duplicate = (content_root / "posts" / "b.md").read_text(encoding="utf-8")
    assert "lineage_relation: exact_copy" in duplicate
    assert "lineage_noindex: true" in duplicate
    assert "lineage_canonical_url: /posts/a/" in duplicate
    assert "observation_id: obs_" in duplicate
    assert "event_id: evt_" in duplicate
    assert "parent_observation_id: obs_" in duplicate
    assert "revision_id: rev_" in duplicate
    assert "lineage_parent_id:" not in duplicate
    assert "lineage_revision_id:" not in duplicate

    first_fixed_point = _tree_bytes(content_root)
    second = apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )
    assert second == {"changed": 0, "deleted": 0, "scanned": 3}
    assert _tree_bytes(content_root) == first_fixed_point


def test_metadata_apply_refreshes_canonical_when_earlier_source_appears(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    excerpt = _source_text(0, 220)
    mirror = posts / "mirror.md"
    mirror.write_text(
        _post(
            title="Persistent event",
            url="https://mirror.example/persistent-event",
            excerpt=excerpt,
            date="2026-07-02T08:00:00Z",
        ),
        encoding="utf-8",
    )
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    apply_lineage_post_metadata(content_root=content_root, internal_dir=internal, apply=True)
    assert "lineage_noindex:" not in mirror.read_text(encoding="utf-8")

    (posts / "origin.md").write_text(
        _post(
            title="Persistent event",
            url="https://origin.example/persistent-event",
            excerpt=excerpt,
            date="2026-07-01T08:00:00Z",
        ),
        encoding="utf-8",
    )
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )
    apply_lineage_post_metadata(content_root=content_root, internal_dir=internal, apply=True)

    refreshed = mirror.read_text(encoding="utf-8")
    assert "lineage_relation: exact_copy" in refreshed
    assert "lineage_noindex: true" in refreshed
    assert "lineage_canonical_url: /posts/origin/" in refreshed


def test_post_metadata_apply_skips_archived_audit_records(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    paths = _write_fixture_posts(content_root)
    archived_path = paths[-1]
    archived_before = archived_path.read_text(encoding="utf-8").replace(
        "draft: false\n", "draft: false\narchived: true\n"
    )
    archived_path.write_text(archived_before, encoding="utf-8")
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )

    result = apply_lineage_post_metadata(
        content_root=content_root,
        internal_dir=internal,
        apply=True,
    )

    assert result == {"changed": 2, "deleted": 0, "scanned": 2}
    assert archived_path.read_text(encoding="utf-8") == archived_before


def test_build_merges_previously_suppressed_registry_observation_without_article_path(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    posts = content_root / "posts"
    posts.mkdir(parents=True)
    excerpt = _source_text(0, 220)
    (posts / "origin.md").write_text(
        _post(
            title="Persistent source",
            url="https://origin.example/persistent",
            excerpt=excerpt,
            date="2026-07-01T08:00:00Z",
        ),
        encoding="utf-8",
    )
    baseline = ObservationInput(
        canonical_url="https://origin.example/persistent",
        title="Persistent source",
        source_text=excerpt,
        source="fixture",
        article_path="posts/origin.md",
        capture_mode="full_text",
        source_completeness="complete",
        source_published_at="2026-07-01T08:00:00Z",
        first_seen_at="2026-07-01T09:00:00Z",
        timestamp_confidence=TimestampConfidence.PUBLISHER,
        article_url="/posts/origin/",
    )
    suppressed = ObservationInput(
        canonical_url="https://mirror.example/persistent",
        title="Persistent source",
        source_text=excerpt,
        source="fixture",
        article_path="",
        capture_mode="full_text",
        source_completeness="complete",
        source_published_at="2026-07-01T10:00:00Z",
        first_seen_at="2026-07-01T11:00:00Z",
        timestamp_confidence=TimestampConfidence.PUBLISHER,
        article_url=None,
    )
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    registry = LineageRegistry()
    resolution = registry.resolve_batch([suppressed], historical_baseline=[baseline])
    assert resolution.items[0].suppress is True
    registry.save(internal, generated_at="2026-07-20T00:00:00Z")

    result = build_lineage_assets(
        content_root=content_root,
        internal_dir=internal,
        public_dir=public,
        as_of="2026-07-20T00:00:00Z",
    )

    assert result["observations"] == 2
    reloaded = LineageRegistry.load(internal)
    assert len(reloaded._records) == 2
    index = json.loads((public / "index.json").read_text(encoding="utf-8"))
    timeline = []
    for reference in index["cluster_buckets"]:
        payload = json.loads((public / reference["path"]).read_text(encoding="utf-8"))
        for cluster in payload["clusters"]:
            timeline.extend(cluster["observations"])
    suppressed_public = next(
        item for item in timeline if item["source_url"] == "https://mirror.example/persistent"
    )
    assert suppressed_public["article_url"] is None
    assert suppressed_public["relation"] == "exact_copy"
