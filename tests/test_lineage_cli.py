from __future__ import annotations

import json
from pathlib import Path

from scripts import build_lineage, verify_lineage


def _fixture_post() -> str:
    excerpt = " ".join(f"signal{index}" for index in range(100))
    return f"""---
title: CLI lineage
date: 2026-07-01T08:00:00Z
draft: false
source: fixture
external_url: https://example.com/cli-lineage
source_capture_mode: full_text
source_completeness: complete
source_is_truncated: false
source_published_at: 2026-07-01T08:00:00Z
timestamp_confidence: publisher
---

## 来源摘要/节选

> {excerpt}
"""


def test_build_and_verify_cli_return_machine_readable_success(
    tmp_path: Path, capsys: object
) -> None:
    del capsys
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    post = posts / "cli.md"
    post.write_text(_fixture_post(), encoding="utf-8")
    internal = tmp_path / "data" / "lineage"
    public = tmp_path / "static" / "lineage"

    exit_code = build_lineage.main(
        [
            "--content-root",
            str(content),
            "--internal-output",
            str(internal),
            "--public-output",
            str(public),
            "--as-of",
            "2026-07-20T00:00:00Z",
            "--apply-post-metadata",
        ]
    )
    assert exit_code == 0
    assert "observation_id: obs_" in post.read_text(encoding="utf-8")

    verify_code = verify_lineage.main(
        [
            "--public-root",
            str(public),
            "--internal-root",
            str(internal),
            "--verify-hashes",
        ]
    )
    assert verify_code == 0


def test_build_cli_is_generate_only_without_explicit_apply(tmp_path: Path) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    post = posts / "cli.md"
    original = _fixture_post()
    post.write_text(original, encoding="utf-8")

    assert (
        build_lineage.main(
            [
                "--content-root",
                str(content),
                "--internal-output",
                str(tmp_path / "internal"),
                "--public-output",
                str(tmp_path / "public"),
                "--as-of",
                "2026-07-20T00:00:00Z",
            ]
        )
        == 0
    )
    assert post.read_text(encoding="utf-8") == original


def test_verify_cli_fails_nonzero_after_tamper(tmp_path: Path) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "cli.md").write_text(_fixture_post(), encoding="utf-8")
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    assert (
        build_lineage.main(
            [
                "--content-root",
                str(content),
                "--internal-output",
                str(internal),
                "--public-output",
                str(public),
                "--as-of",
                "2026-07-20T00:00:00Z",
            ]
        )
        == 0
    )
    index = json.loads((public / "index.json").read_text(encoding="utf-8"))
    (public / index["route_buckets"][0]["path"]).write_text("{}", encoding="utf-8")

    assert (
        verify_lineage.main(
            [
                "--public-root",
                str(public),
                "--internal-root",
                str(internal),
                "--verify-hashes",
            ]
        )
        == 2
    )


def test_verify_cli_rejects_persisted_exact_shingle_hashes(tmp_path: Path) -> None:
    content = tmp_path / "content"
    posts = content / "posts"
    posts.mkdir(parents=True)
    (posts / "cli.md").write_text(_fixture_post(), encoding="utf-8")
    internal = tmp_path / "internal"
    public = tmp_path / "public"
    assert (
        build_lineage.main(
            [
                "--content-root",
                str(content),
                "--internal-output",
                str(internal),
                "--public-output",
                str(public),
                "--as-of",
                "2026-07-20T00:00:00Z",
            ]
        )
        == 0
    )
    index_path = internal / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    reference = next(
        item
        for item in index["registry_buckets"]
        if json.loads((internal / item["path"]).read_text(encoding="utf-8"))["observations"]
    )
    shard_path = internal / reference["path"]
    shard = json.loads(shard_path.read_text(encoding="utf-8"))
    shard["observations"][0]["fingerprint"]["shingle_hashes"] = ["0123456789abcdef"]
    payload = (
        json.dumps(shard, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    )
    shard_path.write_text(payload, encoding="utf-8")
    reference["bytes"] = len(payload.encode("utf-8"))
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    assert (
        verify_lineage.main(
            [
                "--public-root",
                str(public),
                "--internal-root",
                str(internal),
            ]
        )
        == 2
    )
