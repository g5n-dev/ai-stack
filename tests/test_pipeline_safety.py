from __future__ import annotations

import json
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from ai_stack import pipeline
from ai_stack.models import (
    OperationKind,
    OperationRecord,
    OperationStatus,
)
from ai_stack.pipeline import PipelineError
from ai_stack.stores import FileOpsStore
from scripts.release_guard import ReleaseDescriptor, write_release_descriptor

CODE_SHA = "a" * 40


def _source() -> dict[str, list[dict[str, object]]]:
    return {
        "github_trending": [
            {
                "id": 42,
                "title": "Safe title",
                "summary": "A saved source field.",
                "url": "https://example.com/item",
                "tags": "not-an-array",
            }
        ]
    }


def _generated_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, run_id: str = "run-safety"
) -> tuple[Path, Path, Path]:
    monkeypatch.setattr(pipeline, "_crawl_sources", lambda **_kwargs: _source())
    monkeypatch.setattr(pipeline, "_code_sha", lambda: CODE_SHA)
    discovery = tmp_path / "discovery"
    validated = tmp_path / "validated"
    content = tmp_path / "content-ledger"
    ops = tmp_path / "ops-ledger"
    generated = tmp_path / "generated"
    pipeline.crawl(run_id=run_id, output=discovery)
    pipeline.validate_discovery(input_root=discovery, output=validated)
    pipeline.persist_discovery(run_id=run_id, input_root=validated, state_root=content)
    pipeline.reserve_budget(run_id=run_id, input_root=content, state_root=ops)
    pipeline.generate(run_id=run_id, input_root=content, ops_root=ops, output=generated)
    return generated, content, ops


@pytest.mark.parametrize(
    "value",
    ["", "/absolute", "content\\bad", "content/../bad", "other/file.json"],
)
def test_output_paths_are_strictly_allowlisted(value: str) -> None:
    with pytest.raises(PipelineError):
        pipeline._safe_relative(value)


def test_materialization_is_atomic_bounded_and_never_overwrites(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "handoff"
    destination.mkdir()
    with pytest.raises(PipelineError, match="already exist"):
        pipeline._materialize_tree(destination, {"state/run.json": b"{}"})

    parent_target = tmp_path / "real-parent"
    parent_target.mkdir()
    linked_parent = tmp_path / "linked-parent"
    linked_parent.symlink_to(parent_target, target_is_directory=True)
    with pytest.raises(PipelineError, match="parent"):
        pipeline._materialize_tree(linked_parent / "output", {"state/run.json": b"{}"})

    monkeypatch.setattr(pipeline, "MAX_HANDOFF_FILES", 0)
    with pytest.raises(PipelineError, match="too many"):
        pipeline._materialize_tree(tmp_path / "too-many", {"state/run.json": b"{}"})
    assert not (tmp_path / "too-many").exists()
    monkeypatch.setattr(pipeline, "MAX_HANDOFF_FILES", 2_000)
    monkeypatch.setattr(pipeline, "MAX_HANDOFF_FILE_BYTES", 1)
    with pytest.raises(PipelineError, match="too large"):
        pipeline._materialize_tree(tmp_path / "too-large", {"state/run.json": b"{}"})
    monkeypatch.setattr(pipeline, "MAX_HANDOFF_FILE_BYTES", 2 * 1024 * 1024)
    monkeypatch.setattr(pipeline, "MAX_HANDOFF_BYTES", 1)
    with pytest.raises(PipelineError, match="total size"):
        pipeline._materialize_tree(tmp_path / "too-total", {"state/run.json": b"{}"})


def test_materialization_cleans_staged_files_when_final_rename_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original_replace = pipeline.os.replace

    def fail_final(source: str | Path, destination: str | Path) -> None:
        if Path(destination) == tmp_path / "output":
            raise OSError("rename failed")
        original_replace(source, destination)

    monkeypatch.setattr(pipeline.os, "replace", fail_final)
    with pytest.raises(OSError, match="rename failed"):
        pipeline._materialize_tree(tmp_path / "output", {"content/nested/file.json": b"{}"})
    assert not list(tmp_path.glob(".output.*"))


def test_dynamic_crawler_adapter_and_git_identity_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Crawler:
        result: object = {"source": []}

        def __init__(self, **_kwargs: object) -> None:
            pass

        def crawl_all(self) -> object:
            return self.result

    real_import = pipeline.importlib.import_module

    def fake_import(name: str) -> object:
        if name == "crawler.main":
            return SimpleNamespace(CrawlerOrchestrator=Crawler)
        return real_import(name)

    monkeypatch.setattr(pipeline.importlib, "import_module", fake_import)
    assert pipeline._crawl_sources(config_path=Path("sources.yaml"), runtime_profile="ci") == {
        "source": []
    }
    Crawler.result = []
    with pytest.raises(PipelineError, match="invalid root"):
        pipeline._crawl_sources(config_path=Path("sources.yaml"), runtime_profile=None)

    with pytest.raises(PipelineError, match="full 40"):
        pipeline._require_git_sha("main", "code_sha")
    monkeypatch.setattr(
        pipeline.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=1, stdout=""),
    )
    with pytest.raises(PipelineError, match="current code SHA"):
        pipeline._code_sha()


def test_handoff_readers_reject_missing_non_json_non_object_symlink_and_extra(
    tmp_path: Path,
) -> None:
    with pytest.raises(PipelineError, match="missing"):
        pipeline._read_regular(tmp_path / "missing")

    target = tmp_path / "target.json"
    target.write_text("{}", encoding="utf-8")
    link = tmp_path / "link.json"
    link.symlink_to(target)
    with pytest.raises(PipelineError, match="safe regular"):
        pipeline._read_regular(link)

    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(PipelineError, match="invalid JSON"):
        pipeline._read_json(bad)
    bad.write_text("[]", encoding="utf-8")
    with pytest.raises(PipelineError, match="object"):
        pipeline._read_json(bad)

    root = tmp_path / "root"
    root.mkdir()
    (root / "unexpected.txt").write_text("bad", encoding="utf-8")
    with pytest.raises(PipelineError, match="unexpected"):
        pipeline._scan_tree(root, ("state/*.json",))
    (root / "unexpected.txt").unlink()
    nested_target = tmp_path / "outside"
    nested_target.mkdir()
    (root / "state").symlink_to(nested_target, target_is_directory=True)
    with pytest.raises(PipelineError, match="symlink"):
        pipeline._scan_tree(root, ("state/*.json",))

    with pytest.raises(PipelineError, match="regular directory"):
        pipeline._scan_tree(tmp_path / "absent", ("state/*.json",))


def test_tree_scanner_enforces_total_limits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "root"
    (root / "state").mkdir(parents=True)
    (root / "state/one.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(pipeline, "MAX_HANDOFF_FILES", 0)
    with pytest.raises(PipelineError, match="limits"):
        pipeline._scan_tree(root, ("state/*.json",))


def test_atomic_ledger_writer_rejects_escape_symlink_and_directory_and_is_idempotent(
    tmp_path: Path,
) -> None:
    with pytest.raises(PipelineError, match="escapes"):
        pipeline._atomic_ledger_write(tmp_path, "../outside.json", b"{}")

    outside = tmp_path / "outside"
    outside.mkdir()
    linked = tmp_path / "linked"
    linked.symlink_to(outside, target_is_directory=True)
    with pytest.raises(PipelineError, match="symlink"):
        pipeline._atomic_ledger_write(tmp_path, "linked/file.json", b"{}")

    directory = tmp_path / "content/value.json"
    directory.mkdir(parents=True)
    with pytest.raises(PipelineError, match="regular file"):
        pipeline._atomic_ledger_write(tmp_path, "content/value.json", b"{}")

    target = tmp_path / "state/value.json"
    assert pipeline._atomic_ledger_write(tmp_path, "state/value.json", b"{}") is True
    assert pipeline._atomic_ledger_write(tmp_path, "state/value.json", b"{}") is False
    assert target.read_bytes() == b"{}"


def test_crawl_counts_malformed_records_and_rejects_unsafe_run_id(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    values: dict[Any, Any] = {
        7: [],
        "bad-root": "not-an-array",
        "mixed": [None, {"title": "missing URL"}, {"url": "javascript:bad"}],
        **_source(),
    }
    monkeypatch.setattr(pipeline, "_crawl_sources", lambda **_kwargs: values)
    monkeypatch.setattr(pipeline, "_code_sha", lambda: CODE_SHA)

    result = pipeline.crawl(run_id="run-mixed", output=tmp_path / "output")

    assert result["item_count"] == 1
    assert result["rejected_count"] == 5
    with pytest.raises(PipelineError, match="safe identifier"):
        pipeline.crawl(run_id="../bad", output=tmp_path / "bad-output")


def test_discovery_validation_rejects_state_identity_snapshot_and_count_tampering(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(pipeline, "_crawl_sources", lambda **_kwargs: _source())
    monkeypatch.setattr(pipeline, "_code_sha", lambda: CODE_SHA)
    base = tmp_path / "base"
    pipeline.crawl(run_id="run-tamper", output=base)

    cases: list[tuple[str, Any, str]] = [
        (
            "state",
            lambda root: (root / "state/run.json").write_text("{}", encoding="utf-8"),
            "schema or stage",
        ),
        (
            "count",
            lambda root: _rewrite_json(root / "state/run.json", {"item_count": 99}),
            "item count",
        ),
        (
            "snapshot",
            lambda root: next((root / "content/snapshots").glob("*.txt")).write_text(
                "tampered", encoding="utf-8"
            ),
            "digest mismatch",
        ),
        (
            "event-schema",
            lambda root: _rewrite_json(
                next((root / "content/events").glob("*.json")),
                {"schema_version": "future"},
            ),
            "unsupported",
        ),
    ]
    for name, mutate, expected in cases:
        root = tmp_path / name
        shutil.copytree(base, root)
        mutate(root)
        with pytest.raises(PipelineError, match=expected):
            pipeline.validate_discovery(input_root=root, output=tmp_path / f"out-{name}")


def test_discovery_validation_rejects_missing_events_and_identity_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(pipeline, "_crawl_sources", lambda **_kwargs: _source())
    monkeypatch.setattr(pipeline, "_code_sha", lambda: CODE_SHA)
    base = tmp_path / "base"
    pipeline.crawl(run_id="run-more-tamper", output=base)

    no_events = tmp_path / "no-events"
    shutil.copytree(base, no_events)
    shutil.rmtree(no_events / "content/events")
    with pytest.raises(PipelineError, match="no event"):
        pipeline.validate_discovery(input_root=no_events, output=tmp_path / "out-no-events")

    identity = tmp_path / "identity"
    shutil.copytree(base, identity)
    event_path = next((identity / "content/events").glob("*.json"))
    _rewrite_json(event_path, {"event_id": "evt_" + "0" * 64})
    with pytest.raises(PipelineError, match="identity mismatch"):
        pipeline.validate_discovery(input_root=identity, output=tmp_path / "out-id")

    bad_snapshot_path = tmp_path / "snapshot-path"
    shutil.copytree(base, bad_snapshot_path)
    event_path = next((bad_snapshot_path / "content/events").glob("*.json"))
    _rewrite_json(event_path, {"snapshot_path": 7})
    with pytest.raises(PipelineError, match="snapshot path"):
        pipeline.validate_discovery(
            input_root=bad_snapshot_path, output=tmp_path / "out-snapshot-path"
        )


def test_persist_discovery_is_idempotent_and_rejects_run_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(pipeline, "_crawl_sources", lambda **_kwargs: _source())
    monkeypatch.setattr(pipeline, "_code_sha", lambda: CODE_SHA)
    discovery = tmp_path / "discovery"
    pipeline.crawl(run_id="run-persist", output=discovery)
    content = tmp_path / "content"

    first = pipeline.persist_discovery(
        run_id="run-persist", input_root=discovery, state_root=content
    )
    second = pipeline.persist_discovery(
        run_id="run-persist", input_root=discovery, state_root=content
    )
    assert first["changed_items"] == 1
    assert second["changed_items"] == 0
    with pytest.raises(PipelineError, match="run_id"):
        pipeline.persist_discovery(
            run_id="other-run", input_root=discovery, state_root=tmp_path / "other"
        )


def test_event_loader_and_release_sequence_reject_corrupt_or_empty_ledgers(
    tmp_path: Path,
) -> None:
    with pytest.raises(PipelineError, match="event directory"):
        pipeline._load_event_envelopes(tmp_path)
    events = tmp_path / "content/events"
    events.mkdir(parents=True)
    with pytest.raises(PipelineError, match="no canonical events"):
        pipeline._load_event_envelopes(tmp_path)
    (events / "bad.json").write_text(json.dumps({"schema_version": "bad"}), encoding="utf-8")
    with pytest.raises(PipelineError, match="invalid canonical"):
        pipeline._load_event_envelopes(tmp_path)

    ops = tmp_path / "ops"
    releases = ops / "ops/releases"
    releases.mkdir(parents=True)
    (releases / "old.json").write_text(json.dumps({"release_seq": 4}), encoding="utf-8")
    assert pipeline._next_release_sequence(ops, "new-run") == 5
    (releases / "bad.json").write_text(json.dumps({"release_seq": 0}), encoding="utf-8")
    with pytest.raises(PipelineError, match="invalid release"):
        pipeline._next_release_sequence(ops, "new-run")


def test_reserve_budget_is_idempotent_and_rejects_non_reserved_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generated, content, ops = _generated_fixture(tmp_path, monkeypatch, run_id="run-reserve")
    assert generated.is_dir()
    again = pipeline.reserve_budget(run_id="run-reserve", input_root=content, state_root=ops)
    assert again["release_seq"] == 1

    store = FileOpsStore(ops / "state/ops")
    operation_id = pipeline._operation_id("budget", "run-reserve")
    existing = store.get_operation(operation_id)
    assert existing is not None
    cancelled = OperationRecord(
        operation_id=existing.operation_id,
        kind=existing.kind,
        status=OperationStatus.CANCELLED,
        idempotency_key=existing.idempotency_key,
        created_at=existing.created_at,
        updated_at=existing.updated_at,
        token_limit=existing.token_limit,
        metadata=dict(existing.metadata),
    )
    store.put_operation(cancelled, expected_base=store.base_revision())
    with pytest.raises(PipelineError, match="RESERVED"):
        pipeline.reserve_budget(run_id="run-reserve", input_root=content, state_root=ops)


def _rewrite_json(path: Path, changes: dict[str, object]) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    value.update(changes)
    path.write_text(json.dumps(value), encoding="utf-8")


class _Tier:
    value = "A"


class _Decision:
    def __init__(self, *, publishable: bool, reasons: tuple[str, ...] = ()) -> None:
        self.publishable = publishable
        self.reasons = reasons
        self.tier = _Tier()


class _Gate:
    def __init__(self, decision: _Decision) -> None:
        self.decision = decision

    def evaluate(self, _article: object, _snapshots: object) -> _Decision:
        return self.decision


def test_generated_validator_quarantines_evidence_and_markdown_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generated, _content, _ops = _generated_fixture(tmp_path, monkeypatch)

    monkeypatch.setattr(
        pipeline,
        "_evidence_gate",
        lambda: _Gate(_Decision(publishable=False, reasons=("unsupported",))),
    )
    evidence_output = tmp_path / "evidence-quarantine"
    result = pipeline.validate_generated(
        input_root=generated,
        output=evidence_output,
        publisher_config=Path("config/publisher.yaml"),
    )
    assert result == {"run_id": "run-safety", "publishable": 0, "quarantined": 1}
    assert list((evidence_output / "content/quarantine").glob("*.json"))

    monkeypatch.setattr(
        pipeline,
        "_evidence_gate",
        lambda: _Gate(_Decision(publishable=True)),
    )
    monkeypatch.setattr(
        pipeline,
        "_validate_markdown",
        lambda _document: (_ for _ in ()).throw(ValueError("unsafe")),
    )
    markdown_output = tmp_path / "markdown-quarantine"
    result = pipeline.validate_generated(
        input_root=generated,
        output=markdown_output,
        publisher_config=Path("config/publisher.yaml"),
    )
    assert result["quarantined"] == 1


@pytest.mark.parametrize("field", ["body", "claims", "inferences", "evidence"])
def test_generated_validator_rejects_gate_payload_not_bound_to_candidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    generated, _content, _ops = _generated_fixture(
        tmp_path,
        monkeypatch,
        run_id=f"run-gate-binding-{field}",
    )
    candidate_path = next((generated / "content/candidates").glob("*.json"))
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    gate_payload = candidate["gate_payload"]
    replacements: dict[str, object] = {
        "body": "## 已通过门禁的替代正文\n\n这不是最终落盘正文。",
        "claims": [],
        "inferences": [{"id": "inf_unbound", "text": "未绑定推断"}],
        "evidence": [],
    }
    gate_payload[field] = replacements[field]
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")

    monkeypatch.setattr(
        pipeline,
        "_evidence_gate",
        lambda: _Gate(_Decision(publishable=True)),
    )
    with pytest.raises(PipelineError, match=f"gate payload {field} mismatch"):
        pipeline.validate_generated(
            input_root=generated,
            output=tmp_path / "validated-result",
            publisher_config=Path("config/publisher.yaml"),
        )


def test_generated_loader_and_candidate_locator_fail_closed_on_tampering(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generated, _content, _ops = _generated_fixture(
        tmp_path, monkeypatch, run_id="run-generated-tamper"
    )
    candidate_path = next((generated / "content/candidates").glob("*.json"))
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    with pytest.raises(PipelineError, match="not locatable"):
        pipeline._candidate_from_envelope(candidate, "different snapshot", "run-x")

    cases = [
        ("state", generated / "state/run.json", {"stage": "UNKNOWN"}, "schema or stage"),
        (
            "schema",
            candidate_path,
            {"schema_version": "future"},
            "candidate schema",
        ),
        ("identity", candidate_path, {"run_id": "other"}, "identity mismatch"),
    ]
    for name, original_path, changes, message in cases:
        root = tmp_path / f"generated-{name}"
        shutil.copytree(generated, root)
        relative = original_path.relative_to(generated)
        _rewrite_json(root / relative, changes)
        with pytest.raises(PipelineError, match=message):
            pipeline._load_generated(root)

    count = tmp_path / "generated-count"
    shutil.copytree(generated, count)
    _rewrite_json(count / "state/run.json", {"candidate_count": 99})
    with pytest.raises(PipelineError, match="count"):
        pipeline._load_generated(count)


@pytest.mark.parametrize(
    ("body", "message"),
    [
        ("[", "invalid YAML"),
        ("[]", "must be an object"),
        ("publishers: []", "publishers must be an object"),
        ("publishers:\n  telegram: true", "invalid: telegram"),
    ],
)
def test_publisher_config_rejects_ambiguous_shapes(tmp_path: Path, body: str, message: str) -> None:
    config = tmp_path / "publisher.yaml"
    config.write_text(body, encoding="utf-8")
    with pytest.raises(PipelineError, match=message):
        pipeline._publisher_platforms(config)


def test_publisher_config_ignores_unknown_disabled_channels_and_sorts_enabled(
    tmp_path: Path,
) -> None:
    config = tmp_path / "publisher.yaml"
    config.write_text(
        "publishers:\n"
        "  unknown:\n    enabled: true\n"
        "  wechat:\n    enabled: true\n"
        "  telegram:\n    enabled: true\n"
        "  twitter:\n    enabled: false\n",
        encoding="utf-8",
    )
    assert pipeline._publisher_platforms(config) == ("telegram", "wechat")


def _validated_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, run_id: str
) -> tuple[Path, Path, Path]:
    generated, content, ops = _generated_fixture(tmp_path, monkeypatch, run_id=run_id)
    validated = tmp_path / "validated-result"
    publisher_config = tmp_path / "validated-publisher.yaml"
    publisher_config.write_text(
        "publishers:\n  telegram:\n    enabled: true\n",
        encoding="utf-8",
    )
    pipeline.validate_generated(
        input_root=generated,
        output=validated,
        publisher_config=publisher_config,
    )
    return validated, content, ops


def test_validated_loader_and_persistence_reject_tampered_contracts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    validated, content, _ops = _validated_fixture(tmp_path, monkeypatch, "run-validated")
    article_path = next((validated / "content/articles").glob("*.json"))
    cases = [
        ("state", validated / "state/run.json", {"stage": "UNKNOWN"}, "schema or stage"),
        (
            "schema",
            article_path,
            {"schema_version": "future"},
            "article schema",
        ),
    ]
    for name, original_path, changes, message in cases:
        root = tmp_path / f"validated-{name}"
        shutil.copytree(validated, root)
        _rewrite_json(root / original_path.relative_to(validated), changes)
        with pytest.raises(PipelineError, match=message):
            pipeline._load_validated(root)

    missing_markdown = tmp_path / "validated-missing-markdown"
    shutil.copytree(validated, missing_markdown)
    next((missing_markdown / "content/posts").glob("*.md")).unlink()
    with pytest.raises(PipelineError, match="Markdown"):
        pipeline._load_validated(missing_markdown)

    wrong_count = tmp_path / "validated-count"
    shutil.copytree(validated, wrong_count)
    _rewrite_json(wrong_count / "state/run.json", {"publishable": 99})
    with pytest.raises(PipelineError, match="count"):
        pipeline._load_validated(wrong_count)

    tampered_markdown = tmp_path / "validated-markdown-digest"
    shutil.copytree(validated, tampered_markdown)
    markdown_path = next((tampered_markdown / "content/posts").glob("*.md"))
    markdown_path.write_text(
        markdown_path.read_text(encoding="utf-8").replace(
            "这是自动生成的来源简讯",
            "这是被验证后替换的来源简讯",
        ),
        encoding="utf-8",
    )
    with pytest.raises(PipelineError, match="digest"):
        pipeline._load_validated(tampered_markdown)

    tampered_outbox = tmp_path / "validated-outbox-payload"
    shutil.copytree(validated, tampered_outbox)
    outbox_path = next(
        path
        for path in (tampered_outbox / "content/outbox").glob("*.json")
        if path.name != "index.json"
    )
    _rewrite_json(outbox_path, {"payload": {"title": "tampered"}})
    with pytest.raises(PipelineError, match="outbox"):
        pipeline._load_validated(tampered_outbox)

    with pytest.raises(PipelineError, match="run_id"):
        pipeline.persist_result(run_id="other-run", input_root=validated, state_root=content)
    with pytest.raises(PipelineError, match="state is missing"):
        pipeline.persist_result(
            run_id="run-validated",
            input_root=validated,
            state_root=tmp_path / "missing-content",
        )


def test_render_rejects_missing_state_unpersisted_runs_and_invalid_release_sequence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(PipelineError, match="both required"):
        pipeline.render(
            run_id="run-render",
            code_sha="a" * 40,
            content_sha="b" * 40,
            ops_sha="c" * 40,
            content_root=tmp_path / "missing-content",
            ops_root=tmp_path / "missing-ops",
            output=tmp_path / "output",
            site_static_root=tmp_path / "static",
        )

    _generated, content, ops = _generated_fixture(tmp_path, monkeypatch, run_id="run-render")
    with pytest.raises(PipelineError, match="PERSISTED"):
        pipeline.render(
            run_id="run-render",
            code_sha="a" * 40,
            content_sha="b" * 40,
            ops_sha="c" * 40,
            content_root=content,
            ops_root=ops,
            output=tmp_path / "unpersisted",
            site_static_root=tmp_path / "static-unpersisted",
        )

    validated = tmp_path / "validated-render"
    pipeline.validate_generated(
        input_root=_generated,
        output=validated,
        publisher_config=Path("config/publisher.yaml"),
    )
    pipeline.persist_result(run_id="run-render", input_root=validated, state_root=content)
    release_record = ops / "ops/releases/run-render.json"
    _rewrite_json(release_record, {"release_seq": 0})
    with pytest.raises(PipelineError, match="release sequence"):
        pipeline.render(
            run_id="run-render",
            code_sha="a" * 40,
            content_sha="b" * 40,
            ops_sha="c" * 40,
            content_root=content,
            ops_root=ops,
            output=tmp_path / "bad-sequence",
            site_static_root=tmp_path / "static-bad-sequence",
        )


def test_outbox_loader_rejects_missing_index_schema_record_shape_and_identity(
    tmp_path: Path,
) -> None:
    with pytest.raises(PipelineError, match="regular directory"):
        pipeline._load_outbox(tmp_path / "missing", "run-outbox")
    root = tmp_path / "outbox"
    key = _outbox(root, "run-outbox")

    _rewrite_json(root / "index.json", {"schema_version": "future"})
    with pytest.raises(PipelineError, match="index schema"):
        pipeline._load_outbox(root, "run-outbox")
    (root / "index.json").unlink()

    record = root / f"{key}.json"
    _rewrite_json(record, {"extra": True})
    with pytest.raises(PipelineError, match="record schema"):
        pipeline._load_outbox(root, "run-outbox")
    value = json.loads(record.read_text(encoding="utf-8"))
    value.pop("extra")
    value["run_id"] = "other"
    record.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(PipelineError, match="identity mismatch"):
        pipeline._load_outbox(root, "run-outbox")

    value["run_id"] = "run-outbox"
    value["event_revision"] = "changed"
    record.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(PipelineError, match="key mismatch"):
        pipeline._load_outbox(root, "run-outbox")


class _FakePublisher:
    def __init__(self, outcome: object) -> None:
        self.outcome = outcome

    def publish_content(self, _content: dict[str, Any]) -> bool:
        if isinstance(self.outcome, BaseException):
            raise self.outcome
        return bool(self.outcome)


class _FakeOrchestrator:
    outcome: object = True

    def __init__(self, **_kwargs: object) -> None:
        self.publishers = {"telegram": _FakePublisher(self.outcome)}


def _outbox(root: Path, run_id: str) -> str:
    root.mkdir(parents=True)
    key = pipeline._outbox_key("article-1", "telegram", "v1")
    (root / f"{key}.json").write_text(
        json.dumps(
            {
                "schema_version": pipeline.OUTBOX_SCHEMA,
                "run_id": run_id,
                "idempotency_key": key,
                "event_revision": "article-1",
                "platform": "telegram",
                "template_version": "v1",
                "payload": {"title": "Safe"},
            }
        ),
        encoding="utf-8",
    )
    (root / "index.json").write_text(
        json.dumps(
            {
                "schema_version": pipeline.OUTBOX_SCHEMA,
                "run_id": run_id,
                "record_count": 1,
            }
        ),
        encoding="utf-8",
    )
    return key


def test_publish_records_sent_failed_and_unknown_without_blind_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = tmp_path / "publisher.yaml"
    config.write_text("publishers:\n  telegram:\n    enabled: true\n", encoding="utf-8")
    outbox = tmp_path / "outbox"
    key = _outbox(outbox, "run-publish")
    real_import = pipeline.importlib.import_module

    def fake_import(name: str) -> object:
        if name == "publisher.main":
            return SimpleNamespace(PublisherOrchestrator=_FakeOrchestrator)
        return real_import(name)

    monkeypatch.setattr(pipeline.importlib, "import_module", fake_import)
    statuses = [(True, "sent", 0), (False, "failed", 0), (TimeoutError(), "unknown", 1)]
    for index, (outcome, status, unknown) in enumerate(statuses):
        _FakeOrchestrator.outcome = outcome
        output = tmp_path / f"receipts-{index}"
        result = pipeline.publish(
            run_id="run-publish",
            input_root=outbox,
            output=output,
            config_path=config,
        )
        receipt = json.loads((output / f"ops/receipts/{key}.json").read_text(encoding="utf-8"))
        assert receipt["status"] == status
        assert result["unknown_count"] == unknown


def test_default_disabled_channels_never_initialize_or_send(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    outbox = tmp_path / "outbox"
    key = _outbox(outbox, "run-disabled")
    real_import = pipeline.importlib.import_module

    def reject_publisher_import(name: str) -> object:
        if name == "publisher.main":
            raise AssertionError("disabled channel attempted to initialize a publisher")
        return real_import(name)

    monkeypatch.setattr(pipeline.importlib, "import_module", reject_publisher_import)
    output = tmp_path / "receipts"
    result = pipeline.publish(
        run_id="run-disabled",
        input_root=outbox,
        output=output,
        config_path=Path(__file__).resolve().parents[1] / "config/publisher.yaml",
    )

    receipt = json.loads((output / f"ops/receipts/{key}.json").read_text(encoding="utf-8"))
    assert result["unknown_count"] == 0
    assert receipt["status"] == "disabled"
    assert receipt["attempts"] == 0


def test_persist_receipt_maps_every_terminal_status_and_is_idempotent(
    tmp_path: Path,
) -> None:
    handoff = tmp_path / "handoff"
    (handoff / "ops/receipts").mkdir(parents=True)
    (handoff / "state").mkdir()
    statuses = ("sent", "failed", "disabled", "unknown")
    for index, status in enumerate(statuses):
        key = f"{index}" * 64
        (handoff / f"ops/receipts/{key}.json").write_text(
            json.dumps(
                {
                    "schema_version": pipeline.RECEIPT_SCHEMA,
                    "run_id": "run-receipts",
                    "idempotency_key": key,
                    "platform": "telegram",
                    "status": status,
                    "detail": status,
                    "attempts": 1,
                }
            ),
            encoding="utf-8",
        )
    (handoff / "ops/receipts/index.json").write_text(
        json.dumps(
            {
                "schema_version": pipeline.RECEIPT_SCHEMA,
                "run_id": "run-receipts",
                "record_count": 4,
                "unknown_count": 1,
            }
        ),
        encoding="utf-8",
    )
    (handoff / "state/receipt.json").write_text(
        json.dumps(
            {
                "schema_version": pipeline.RUN_SCHEMA,
                "run_id": "run-receipts",
                "stage": "NOTIFIED",
                "receipt_count": 4,
                "unknown_count": 1,
            }
        ),
        encoding="utf-8",
    )
    ops = tmp_path / "ops"

    first = pipeline.persist_receipt(run_id="run-receipts", input_root=handoff, state_root=ops)
    second = pipeline.persist_receipt(run_id="run-receipts", input_root=handoff, state_root=ops)

    assert first["persisted_receipts"] == 4
    assert second["persisted_receipts"] == 0


def test_persist_receipt_rejects_bad_status_and_operation_collision(tmp_path: Path) -> None:
    handoff = tmp_path / "handoff"
    key = _outbox(handoff / "ops/receipts", "run-bad")
    # Replace the outbox record with a receipt-shaped record.
    receipt_path = handoff / f"ops/receipts/{key}.json"
    receipt_path.write_text(
        json.dumps(
            {
                "schema_version": pipeline.RECEIPT_SCHEMA,
                "run_id": "run-bad",
                "idempotency_key": key,
                "platform": "telegram",
                "status": "invalid",
                "detail": "bad",
                "attempts": 1,
            }
        ),
        encoding="utf-8",
    )
    (handoff / "ops/receipts/index.json").write_text(
        json.dumps({"schema_version": pipeline.RECEIPT_SCHEMA}), encoding="utf-8"
    )
    (handoff / "state").mkdir()
    (handoff / "state/receipt.json").write_text(
        json.dumps(
            {
                "schema_version": pipeline.RUN_SCHEMA,
                "run_id": "run-bad",
                "stage": "NOTIFIED",
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(PipelineError, match="status"):
        pipeline.persist_receipt(run_id="run-bad", input_root=handoff, state_root=tmp_path / "ops")

    receipt_path_data = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt_path_data["status"] = "sent"
    receipt_path.write_text(json.dumps(receipt_path_data), encoding="utf-8")
    store = FileOpsStore(tmp_path / "collision/state/ops")
    now = pipeline._utc_now()
    collision = OperationRecord(
        operation_id=f"op_receipt_{key}",
        kind=OperationKind.PUBLISH_RECEIPT,
        status=OperationStatus.COMPLETED,
        idempotency_key="different",
        created_at=now,
        updated_at=now,
    )
    store.put_operation(collision, expected_base=store.base_revision())
    with pytest.raises(PipelineError, match="collision"):
        pipeline.persist_receipt(
            run_id="run-bad",
            input_root=handoff,
            state_root=tmp_path / "collision",
        )


def _release_handoff(
    root: Path,
    *,
    sequence: int,
    code_sha: str = "a" * 40,
    content_sha: str = "b" * 40,
) -> ReleaseDescriptor:
    tree = {
        "schema_version": "public_tree_manifest_v1",
        "file_count": 1,
        "total_bytes": 4,
        "files": [
            {
                "path": "index.html",
                "bytes": 4,
                "sha256": pipeline._sha256_bytes(b"safe"),
            }
        ],
    }
    digest = pipeline._sha256_bytes(
        json.dumps(tree, sort_keys=True, separators=(",", ":")).encode()
    )
    descriptor = ReleaseDescriptor(
        code_sha=code_sha,
        content_sha=content_sha,
        schema_version="1.0",
        release_seq=sequence,
        artifact_digest=digest,
        artifact_digest_kind="public_tree_manifest_v1",
        generated_at="2026-07-13T08:00:00Z",
    )
    (root / "state").mkdir(parents=True)
    (root / "content/outbox").mkdir(parents=True)
    write_release_descriptor(root / "state/release.json", descriptor)
    (root / "state/public-tree-manifest.json").write_text(
        json.dumps(tree), encoding="utf-8"
    )
    (root / "state/release-basis.json").write_text("{}", encoding="utf-8")
    (root / "content/outbox/index.json").write_text("{}", encoding="utf-8")
    return descriptor


def test_persist_healthy_release_is_append_only_monotonic_and_idempotent(
    tmp_path: Path,
) -> None:
    handoff = tmp_path / "release"
    descriptor = _release_handoff(handoff, sequence=7)
    ops = tmp_path / "ops"

    first = pipeline.persist_release(
        run_id="run-release",
        input_root=handoff,
        state_root=ops,
        expected_release_id=descriptor.release_id,
        expected_code_sha=descriptor.code_sha,
        expected_content_sha=descriptor.content_sha,
        expected_artifact_digest=descriptor.artifact_digest,
    )
    second = pipeline.persist_release(
        run_id="run-release",
        input_root=handoff,
        state_root=ops,
        expected_release_id=descriptor.release_id,
        expected_code_sha=descriptor.code_sha,
        expected_content_sha=descriptor.content_sha,
        expected_artifact_digest=descriptor.artifact_digest,
    )

    current = ops / "ops/releases/current-healthy.json"
    archive = ops / (
        f"ops/releases/healthy/{descriptor.release_seq:020d}-{descriptor.release_id}.json"
    )
    assert first["persisted"] is True
    assert second["persisted"] is False
    assert json.loads(current.read_text(encoding="utf-8")) == descriptor.to_dict()
    assert current.read_bytes() == archive.read_bytes()

    stale = tmp_path / "stale"
    stale_descriptor = _release_handoff(stale, sequence=6, code_sha="c" * 40)
    with pytest.raises(PipelineError, match="stale release sequence"):
        pipeline.persist_release(
            run_id="run-stale",
            input_root=stale,
            state_root=ops,
            expected_release_id=stale_descriptor.release_id,
            expected_code_sha=stale_descriptor.code_sha,
            expected_content_sha=stale_descriptor.content_sha,
            expected_artifact_digest=stale_descriptor.artifact_digest,
        )


def test_persist_healthy_release_rejects_forged_identity_tree_and_extra_files(
    tmp_path: Path,
) -> None:
    base = tmp_path / "base"
    descriptor = _release_handoff(base, sequence=1)

    with pytest.raises(PipelineError, match="workflow input"):
        pipeline.persist_release(
            run_id="run-forged",
            input_root=base,
            state_root=tmp_path / "ops-forged",
            expected_release_id=descriptor.release_id,
            expected_code_sha="f" * 40,
            expected_content_sha=descriptor.content_sha,
            expected_artifact_digest=descriptor.artifact_digest,
        )

    tree_tamper = tmp_path / "tree-tamper"
    shutil.copytree(base, tree_tamper)
    _rewrite_json(tree_tamper / "state/public-tree-manifest.json", {"total_bytes": 9})
    with pytest.raises(PipelineError, match="public tree manifest"):
        pipeline.persist_release(
            run_id="run-tree",
            input_root=tree_tamper,
            state_root=tmp_path / "ops-tree",
            expected_release_id=descriptor.release_id,
            expected_code_sha=descriptor.code_sha,
            expected_content_sha=descriptor.content_sha,
            expected_artifact_digest=descriptor.artifact_digest,
        )

    extra = tmp_path / "extra"
    shutil.copytree(base, extra)
    (extra / "state/unexpected.json").write_text("{}", encoding="utf-8")
    with pytest.raises(PipelineError, match="unexpected handoff path"):
        pipeline.persist_release(
            run_id="run-extra",
            input_root=extra,
            state_root=tmp_path / "ops-extra",
            expected_release_id=descriptor.release_id,
            expected_code_sha=descriptor.code_sha,
            expected_content_sha=descriptor.content_sha,
            expected_artifact_digest=descriptor.artifact_digest,
        )
