from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest

from ai_stack.models import (
    ArticleRevision,
    Event,
    Evidence,
    OperationKind,
    OperationRecord,
    OperationStatus,
    Revision,
    RunManifest,
    SourceItem,
    WorkflowStatus,
)
from ai_stack.stores import (
    ContentStore,
    FileContentStore,
    FileOpsStore,
    OpsStore,
    StoreConflictError,
    UnsafeStorePathError,
)


NOW = datetime(2026, 7, 13, tzinfo=timezone.utc)


def source(native_id: str = "repo-1") -> SourceItem:
    return SourceItem(
        source="github",
        native_id=native_id,
        canonical_url=f"https://github.com/example/{native_id}",
        fetched_at=NOW,
        payload={"name": native_id},
    )


def test_filesystem_stores_implement_protocols(tmp_path: Path) -> None:
    content: ContentStore = FileContentStore(tmp_path / "content")
    ops: OpsStore = FileOpsStore(tmp_path / "ops")

    assert content.base_revision().startswith("man_")
    assert ops.base_revision().startswith("man_")


def test_content_store_cas_round_trip_and_idempotent_retry(tmp_path: Path) -> None:
    store = FileContentStore(tmp_path / "content")
    initial = store.base_revision()
    item = source()

    first = store.put_source(item, expected_base=initial)
    retry = store.put_source(item, expected_base=initial)

    assert first.changed is True
    assert first.previous_base == initial
    assert retry.changed is False
    assert retry.base_revision == first.base_revision
    assert store.get_source(item.item_id) == item
    assert not list((tmp_path / "content").rglob("*.tmp"))


def test_semantically_identical_refetch_is_a_noop(tmp_path: Path) -> None:
    store = FileContentStore(tmp_path / "content")
    original = source()
    first = store.put_source(original, expected_base=store.base_revision())
    refetched = SourceItem(
        source=original.source,
        native_id=original.native_id,
        canonical_url=original.canonical_url,
        fetched_at=datetime(2026, 7, 14, tzinfo=timezone.utc),
        payload=original.payload,
    )

    retry = store.put_source(refetched, expected_base=first.previous_base)

    assert retry.changed is False
    assert retry.base_revision == first.base_revision
    assert store.get_source(original.item_id) == original


def test_content_store_rejects_stale_writer_without_losing_first_write(
    tmp_path: Path,
) -> None:
    store = FileContentStore(tmp_path / "content")
    shared_base = store.base_revision()
    accepted = source("accepted")
    rejected = source("rejected")

    store.put_source(accepted, expected_base=shared_base)
    with pytest.raises(StoreConflictError) as error:
        store.put_source(rejected, expected_base=shared_base)

    assert error.value.expected_base == shared_base
    assert store.get_source(accepted.item_id) == accepted
    assert store.get_source(rejected.item_id) is None


def test_content_store_handles_run_manifests_and_reports_counts(tmp_path: Path) -> None:
    store = FileContentStore(tmp_path / "content")
    run = RunManifest(
        run_id="run-001",
        code_sha="a" * 40,
        content_parent_sha="b" * 40,
        input_digest="sha256:" + "1" * 64,
        config_digest="sha256:" + "2" * 64,
        model="model-x",
        status=WorkflowStatus.DISCOVERED,
        created_at=NOW,
        updated_at=NOW,
    )

    store.put_run(run, expected_base=store.base_revision())

    assert store.get_run("run-001") == run
    assert store.status().record_counts == {"runs": 1}
    assert store.validate().valid is True


def test_content_store_round_trips_every_domain_record(tmp_path: Path) -> None:
    store = FileContentStore(tmp_path / "content")
    item = source()
    revision = Revision(
        item_id=item.item_id,
        normalized_payload={"title": "Release"},
        source_snapshot_digest="sha256:" + "1" * 64,
        observed_at=NOW,
    )
    event = Event(
        seed_item_id=item.item_id,
        member_item_ids=(item.item_id,),
        first_seen=NOW,
        last_seen=NOW,
    )
    evidence = Evidence(
        source_url=item.canonical_url,
        snapshot_digest="sha256:" + "2" * 64,
        locator="README:L1",
        excerpt="Release",
        claim_ids=("claim-1",),
        captured_at=NOW,
    )
    article = ArticleRevision(
        event_id=event.event_id,
        generation_key="gen_seed",
        title="Release",
        body="Release body",
        created_at=NOW,
        evidence_ids=(evidence.evidence_id,),
        source_support=1.0,
    )

    for write in (
        lambda: store.put_source(item, expected_base=store.base_revision()),
        lambda: store.put_revision(revision, expected_base=store.base_revision()),
        lambda: store.put_event(event, expected_base=store.base_revision()),
        lambda: store.put_evidence(evidence, expected_base=store.base_revision()),
        lambda: store.put_article(article, expected_base=store.base_revision()),
    ):
        assert write().changed is True

    assert store.root == (tmp_path / "content").absolute()
    assert store.get_revision(revision.revision_id) == revision
    assert store.get_event(event.event_id) == event
    assert store.get_evidence(evidence.evidence_id) == evidence
    assert store.get_article(article.article_revision_id) == article
    assert store.get_article("art_missing") is None
    assert store.status().record_counts == {
        "articles": 1,
        "events": 1,
        "evidence": 1,
        "revisions": 1,
        "sources": 1,
    }


def test_ops_store_persists_operation_and_never_exposes_delete(tmp_path: Path) -> None:
    store = FileOpsStore(tmp_path / "ops")
    operation = OperationRecord(
        operation_id="op-001",
        kind=OperationKind.OUTBOX,
        status=OperationStatus.PENDING,
        idempotency_key="event-1:telegram:v1",
        created_at=NOW,
        updated_at=NOW,
        metadata={"platform": "telegram"},
    )

    result = store.put_operation(operation, expected_base=store.base_revision())

    assert result.changed is True
    assert store.get_operation("op-001") == operation
    assert store.get_operation("op-missing") is None
    assert store.root == (tmp_path / "ops").absolute()
    assert store.status().record_counts == {"operations": 1}
    assert store.validate().valid is True
    assert not hasattr(store, "delete")


def test_store_rejects_path_traversal_ids_and_symlink_roots(tmp_path: Path) -> None:
    store = FileContentStore(tmp_path / "content")
    with pytest.raises(UnsafeStorePathError):
        store.get_run("../../outside")

    real = tmp_path / "real"
    real.mkdir()
    linked = tmp_path / "linked"
    linked.symlink_to(real, target_is_directory=True)
    with pytest.raises(UnsafeStorePathError):
        FileContentStore(linked)

    with pytest.raises(UnsafeStorePathError, match="expected base"):
        store.put_source(source(), expected_base="../../base")


def test_store_rejects_non_directory_paths_and_symlinked_parent(
    tmp_path: Path,
) -> None:
    root_file = tmp_path / "root-file"
    root_file.write_text("not a directory", encoding="utf-8")
    with pytest.raises(UnsafeStorePathError):
        FileContentStore(root_file)

    bad_child = tmp_path / "bad-child"
    bad_child.mkdir()
    (bad_child / "objects").write_text("not a directory", encoding="utf-8")
    with pytest.raises(UnsafeStorePathError):
        FileContentStore(bad_child)

    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    linked_parent = tmp_path / "linked-parent"
    linked_parent.symlink_to(real_parent, target_is_directory=True)
    with pytest.raises(UnsafeStorePathError):
        FileContentStore(linked_parent / "ledger")


def test_integrity_validation_detects_object_tampering(tmp_path: Path) -> None:
    store = FileContentStore(tmp_path / "content")
    store.put_source(source(), expected_base=store.base_revision())
    object_file = next((tmp_path / "content" / "objects").glob("obj_*.json"))
    object_file.write_text('{"tampered":true}\n', encoding="utf-8")

    report = store.validate()

    assert report.valid is False
    assert any("digest" in error for error in report.errors)


def test_head_is_an_atomic_plain_json_pointer(tmp_path: Path) -> None:
    root = tmp_path / "content"
    store = FileContentStore(root)
    before = json.loads((root / "HEAD.json").read_text(encoding="utf-8"))

    store.put_source(source(), expected_base=store.base_revision())

    after = json.loads((root / "HEAD.json").read_text(encoding="utf-8"))
    assert before["base"] != after["base"]
    assert os.stat(root / "HEAD.json").st_mode & 0o777 == 0o600


def test_integrity_validation_reports_corrupt_head_without_raising(tmp_path: Path) -> None:
    root = tmp_path / "content"
    store = FileContentStore(root)
    (root / "HEAD.json").write_text("not-json", encoding="utf-8")

    report = store.validate()

    assert report.valid is False
    assert report.base_revision is None
    assert any("HEAD" in error for error in report.errors)


def test_integrity_validation_reports_invalid_head_and_manifest_digest(
    tmp_path: Path,
) -> None:
    invalid_head_root = tmp_path / "invalid-head"
    invalid_head_store = FileContentStore(invalid_head_root)
    (invalid_head_root / "HEAD.json").write_text(
        '{"base":"../../manifest"}\n', encoding="utf-8"
    )
    assert invalid_head_store.validate().valid is False

    manifest_root = tmp_path / "manifest-tamper"
    manifest_store = FileContentStore(manifest_root)
    base = manifest_store.base_revision()
    (manifest_root / "manifests" / f"{base}.json").write_text(
        '{"parent":null,"records":{},"schema_version":2}\n', encoding="utf-8"
    )
    report = manifest_store.validate()
    assert report.valid is False
    assert any("manifest digest" in error for error in report.errors)

    invalid_json_root = tmp_path / "invalid-json"
    invalid_json_store = FileContentStore(invalid_json_root)
    invalid_json = b"not-json\n"
    invalid_base = "man_" + hashlib.sha256(invalid_json).hexdigest()
    (invalid_json_root / "manifests" / f"{invalid_base}.json").write_bytes(
        invalid_json
    )
    (invalid_json_root / "HEAD.json").write_text(
        json.dumps({"base": invalid_base}) + "\n", encoding="utf-8"
    )
    report = invalid_json_store.validate()
    assert report.valid is False
    assert any("valid JSON" in error for error in report.errors)
