from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.release_marker import (
    ReleaseMarkerError,
    build_release_marker,
    prune_unreferenced_product,
    verify_release_marker,
)
from scripts import release_guard


SHA = "a" * 40
ROOT = Path(__file__).resolve().parents[1]


def _write_json(path: Path, payload: object) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    path.write_bytes(body)
    return hashlib.sha256(body).hexdigest()


def _public_tree(root: Path, *, include_lineage: bool = True) -> None:
    _write_json(root / "data/content-quality.json", {"schema": "quality_v1"})
    products = ("lineage", "tag-graph", "stack-trends") if include_lineage else (
        "tag-graph",
        "stack-trends",
    )
    for product in products:
        shard = _write_json(root / f"data/{product}/shards/a.json", {"ok": True})
        _write_json(
            root / f"data/{product}/index.json",
            {"files": [{"path": "shards/a.json", "sha256": shard}]},
        )
    trends = json.loads((root / "data/stack-trends/index.json").read_text())
    trends.update(
        {
            "generated_at": "2026-07-20T08:00:00Z",
            "lineage_mode": "lineage_index_v1",
        }
    )
    _write_json(root / "data/stack-trends/index.json", trends)


def test_release_marker_supports_the_pr1_no_lineage_rollout_state(tmp_path: Path) -> None:
    _public_tree(tmp_path, include_lineage=False)

    marker = build_release_marker(tmp_path, exact_sha=SHA)

    assert marker["lineage_hash"] == "unavailable"
    assert marker["lineage_mode"] == "unavailable"
    assert verify_release_marker(tmp_path, marker, expected_sha=SHA) == marker
    with pytest.raises(ReleaseMarkerError, match="lineage"):
        build_release_marker(tmp_path, exact_sha=SHA, require_lineage=True)


def test_release_marker_binds_exact_sha_and_all_delivery_hashes(tmp_path: Path) -> None:
    _public_tree(tmp_path)

    marker = build_release_marker(tmp_path, exact_sha=SHA)

    assert marker["schema_version"] == "ai_stack_release_v1"
    assert marker["exact_sha"] == SHA
    assert marker["generated_at"] == "2026-07-20T08:00:00Z"
    assert marker["lineage_mode"] == "lineage_index_v1"
    assert marker["release_id"].startswith("r-")
    assert set(marker) == {
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
    for field in ("quality_hash", "lineage_hash", "graph_hash", "trends_hash"):
        assert len(marker[field]) == 64
    assert verify_release_marker(tmp_path, marker, expected_sha=SHA) == marker


def test_release_marker_fails_closed_on_mutation_or_unreachable_shard(
    tmp_path: Path,
) -> None:
    _public_tree(tmp_path)
    marker = build_release_marker(tmp_path, exact_sha=SHA)
    (tmp_path / "data/lineage/shards/a.json").write_text('{"changed":true}')

    with pytest.raises(ReleaseMarkerError, match="hash"):
        verify_release_marker(tmp_path, marker, expected_sha=SHA)

    _public_tree(tmp_path)
    (tmp_path / "data/tag-graph/unreferenced.json").write_text("{}")
    with pytest.raises(ReleaseMarkerError, match="unreferenced"):
        build_release_marker(tmp_path, exact_sha=SHA)

    assert prune_unreferenced_product(tmp_path / "data/tag-graph") == (
        "unreferenced.json",
    )
    assert not (tmp_path / "data/tag-graph/unreferenced.json").exists()
    assert build_release_marker(tmp_path, exact_sha=SHA)["graph_hash"]


@pytest.mark.parametrize("sha", ["main", "a" * 39, "A" * 40])
def test_release_marker_rejects_non_exact_git_sha(tmp_path: Path, sha: str) -> None:
    _public_tree(tmp_path)
    with pytest.raises(ReleaseMarkerError, match="SHA"):
        build_release_marker(tmp_path, exact_sha=sha)


def test_release_guard_binds_marker_to_the_complete_pages_tree(tmp_path: Path) -> None:
    _public_tree(tmp_path)
    (tmp_path / "index.html").write_text("<h1>ready</h1>", encoding="utf-8")
    marker = build_release_marker(tmp_path, exact_sha=SHA)
    marker_path = tmp_path / "ai_stack_release_v1.json"
    marker_path.write_text(json.dumps(marker), encoding="utf-8")
    tree = tmp_path.parent / "public-tree-manifest.json"

    assert release_guard.main(
        [
            "guard-marker",
            "--public-root",
            str(tmp_path),
            "--marker",
            str(marker_path),
            "--expected-sha",
            SHA,
            "--tree-manifest-output",
            str(tree),
        ]
    ) == 0
    payload = json.loads(tree.read_text(encoding="utf-8"))
    assert "ai_stack_release_v1.json" in {item["path"] for item in payload["files"]}


def test_release_guard_script_entrypoint_can_import_release_marker(tmp_path: Path) -> None:
    public = tmp_path / "public"
    _public_tree(public)
    (public / "index.html").write_text("<h1>ready</h1>", encoding="utf-8")
    marker = build_release_marker(public, exact_sha=SHA)
    marker_path = public / "ai_stack_release_v1.json"
    marker_path.write_text(json.dumps(marker), encoding="utf-8")
    tree = tmp_path / "public-tree-manifest.json"

    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "release_guard.py"),
            "guard-marker",
            "--public-root",
            str(public),
            "--marker",
            str(marker_path),
            "--expected-sha",
            SHA,
            "--tree-manifest-output",
            str(tree),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert tree.is_file()
