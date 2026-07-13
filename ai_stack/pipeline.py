from __future__ import annotations

import hashlib
import importlib
import json
import os
import re
import stat
import subprocess
import tempfile
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Protocol, cast

import yaml

from ._json import canonical_json_bytes, json_ready, sha256_digest
from .identity import make_generation_key
from .models import (
    ArticleRevision,
    Event,
    Evidence,
    OperationKind,
    OperationRecord,
    OperationStatus,
    Revision,
    RunManifest,
    SourceItem,
    StepResult,
    StepStatus,
    WorkflowStatus,
    model_to_dict,
)
from .stores import FileContentStore, FileOpsStore

DISCOVERY_SCHEMA = "discovery_event_v1"
GENERATED_SCHEMA = "generated_candidate_v1"
VALIDATED_SCHEMA = "validated_article_v1"
RUN_SCHEMA = "run_handoff_v1"
OUTBOX_SCHEMA = "outbox_v1"
RECEIPT_SCHEMA = "publish_receipt_v1"
RELEASE_SCHEMA_VERSION = "1.0"
GENERATOR = "deterministic-source-brief-v1"
PROMPT_VERSION = "source-brief-v1"
POLICY_VERSION = "evidence-policy-v1"
MAX_HANDOFF_FILES = 2_000
MAX_HANDOFF_FILE_BYTES = 2 * 1024 * 1024
MAX_HANDOFF_BYTES = 64 * 1024 * 1024
MAX_RELEASE_STATE_FILE_BYTES = 8 * 1024 * 1024
MAX_GENERATED_ITEMS = 5

_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
_SAFE_FILE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,255}$")


class PipelineError(RuntimeError):
    """Raised when a pipeline boundary cannot be proven safe."""


class _Crawler(Protocol):
    def crawl_all(self) -> Mapping[str, Any]: ...


class _EvidenceTier(Protocol):
    value: str


class _GateDecision(Protocol):
    publishable: bool
    reasons: tuple[str, ...]
    tier: _EvidenceTier


class _EvidenceGate(Protocol):
    def evaluate(
        self, article: Mapping[str, object], snapshots: Mapping[str, object]
    ) -> _GateDecision: ...


class _BuildIntelligence(Protocol):
    def __call__(
        self,
        *,
        output_dir: str | Path,
        events: Sequence[Mapping[str, Any]],
        as_of: datetime | str,
        release_id: str | None = None,
    ) -> dict[str, Any]: ...


class _Publisher(Protocol):
    def publish_content(self, content: dict[str, Any]) -> bool: ...


class _PublisherOrchestrator(Protocol):
    publishers: Mapping[str, _Publisher]


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _utc_text(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _require_run_id(value: str) -> str:
    if not _RUN_ID.fullmatch(value):
        raise PipelineError("run_id must be a safe identifier")
    return value


def _require_git_sha(value: str, field: str) -> str:
    normalized = value.casefold()
    if not _GIT_SHA.fullmatch(normalized):
        raise PipelineError(f"{field} must be a full 40-character Git SHA")
    return normalized


def _code_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip().casefold()
    if result.returncode != 0 or not _GIT_SHA.fullmatch(value):
        raise PipelineError("cannot bind pipeline run to the current code SHA")
    return value


def _crawl_sources(*, config_path: Path, runtime_profile: str | None) -> Mapping[str, Any]:
    factory = cast(
        Callable[..., _Crawler],
        importlib.import_module("crawler.main").CrawlerOrchestrator,
    )
    crawler = factory(
        config_path=str(config_path),
        dedupe=True,
        dedupe_scope="global",
        runtime_profile=runtime_profile,
    )
    result = crawler.crawl_all()
    if not isinstance(result, Mapping):
        raise PipelineError("crawler returned an invalid root value")
    return result


def _evidence_gate() -> _EvidenceGate:
    factory = cast(
        Callable[[], _EvidenceGate],
        importlib.import_module("processor.evidence_pipeline").EvidenceGate,
    )
    return factory()


def _validate_markdown(document: str) -> None:
    validator = cast(
        Callable[[str], object],
        importlib.import_module("content_security").validate_markdown_document,
    )
    validator(document)


def _build_intelligence() -> _BuildIntelligence:
    return cast(
        _BuildIntelligence,
        importlib.import_module("processor.intelligence").build_static_intelligence,
    )


def _outbox_key(event_revision: str, platform: str, template_version: str) -> str:
    raw = f"{event_revision}\x1f{platform}\x1f{template_version}".encode()
    return hashlib.sha256(raw).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_relative(relative: str) -> PurePosixPath:
    if not relative or relative.startswith("/") or "\\" in relative or "\x00" in relative:
        raise PipelineError(f"unsafe output path: {relative!r}")
    path = PurePosixPath(relative)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise PipelineError(f"unsafe output path: {relative!r}")
    if path.parts[0] not in {"content", "ops", "state"}:
        raise PipelineError(f"output path is outside an allowed root: {relative}")
    return path


def _materialize_tree(destination: Path, files: Mapping[str, bytes]) -> None:
    destination = destination.absolute()
    if destination.is_symlink() or destination.exists():
        raise PipelineError(f"output path must not already exist: {destination}")
    if destination.parent.is_symlink():
        raise PipelineError(f"output parent must not be a symlink: {destination.parent}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    try:
        total_bytes = 0
        if len(files) > MAX_HANDOFF_FILES:
            raise PipelineError("handoff contains too many files")
        for relative, payload in sorted(files.items()):
            _safe_relative(relative)
            if len(payload) > MAX_HANDOFF_FILE_BYTES:
                raise PipelineError(f"handoff file is too large: {relative}")
            total_bytes += len(payload)
            if total_bytes > MAX_HANDOFF_BYTES:
                raise PipelineError("handoff exceeds the total size limit")
            target = temporary / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except BaseException:
        for path in sorted(temporary.rglob("*"), reverse=True):
            if path.is_file() and not path.is_symlink():
                path.unlink(missing_ok=True)
            elif path.is_dir() and not path.is_symlink():
                path.rmdir()
        temporary.rmdir()
        raise


def _read_regular(path: Path, *, max_file_bytes: int | None = None) -> bytes:
    limit = MAX_HANDOFF_FILE_BYTES if max_file_bytes is None else max_file_bytes
    try:
        details = path.lstat()
    except OSError as exc:
        raise PipelineError(f"required handoff file is missing: {path}") from exc
    if (
        path.is_symlink()
        or not stat.S_ISREG(details.st_mode)
        or details.st_nlink != 1
        or details.st_size > limit
    ):
        raise PipelineError(f"handoff path is not a safe regular file: {path}")
    return path.read_bytes()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(_read_regular(path))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PipelineError(f"invalid JSON handoff file: {path}") from exc
    if not isinstance(value, dict):
        raise PipelineError(f"JSON handoff file must contain an object: {path}")
    return cast(dict[str, Any], value)


def _scan_tree(
    root: Path,
    allowed: Sequence[str],
    *,
    max_file_bytes: int | None = None,
) -> dict[str, bytes]:
    if root.is_symlink() or not root.is_dir():
        raise PipelineError(f"handoff root must be a regular directory: {root}")
    result: dict[str, bytes] = {}
    total = 0
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in directory_names:
            if (current_path / name).is_symlink():
                raise PipelineError(f"symlink in handoff tree: {current_path / name}")
        for name in file_names:
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            if not any(PurePosixPath(relative).match(pattern) for pattern in allowed):
                raise PipelineError(f"unexpected handoff path: {relative}")
            payload = _read_regular(path, max_file_bytes=max_file_bytes)
            result[relative] = payload
            total += len(payload)
            if len(result) > MAX_HANDOFF_FILES or total > MAX_HANDOFF_BYTES:
                raise PipelineError("handoff exceeds file or byte limits")
    return result


def _source_url(payload: Mapping[str, Any]) -> str | None:
    for field in ("url", "repo_url", "paper_url", "link", "external_url"):
        value = payload.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _native_id(payload: Mapping[str, Any]) -> str | None:
    for field in ("native_id", "id", "arxiv_id", "full_name", "repo_full_name"):
        value = payload.get(field)
        if isinstance(value, (str, int)) and not isinstance(value, bool):
            normalized = str(value).strip()
            if normalized:
                return normalized[:512]
    return None


def _plain_field(payload: Mapping[str, Any], fields: Sequence[str], fallback: str) -> str:
    for field in fields:
        value = payload.get(field)
        if isinstance(value, str) and value.strip():
            return " ".join(value.strip().split())[:2_000]
    return fallback


def _snapshot_text(item: SourceItem) -> str:
    title = _plain_field(item.payload, ("title", "name", "headline"), item.canonical_url)
    summary = _plain_field(
        item.payload,
        ("description", "summary", "abstract", "selftext"),
        "",
    )
    return f"Source: {item.source}\nURL: {item.canonical_url}\nTitle: {title}\nSummary: {summary}\n"


def _discovery_envelope(
    item: SourceItem,
    revision: Revision,
    event: Event,
    snapshot_path: str,
) -> dict[str, Any]:
    return {
        "schema_version": DISCOVERY_SCHEMA,
        "event_id": event.event_id,
        "source_item": model_to_dict(item),
        "revision": model_to_dict(revision),
        "event": model_to_dict(event),
        "snapshot_path": snapshot_path,
    }


def crawl(
    *,
    run_id: str,
    output: Path,
    config_path: Path = Path("config/sources.yaml"),
    runtime_profile: str | None = None,
) -> dict[str, Any]:
    run_id = _require_run_id(run_id)
    raw_sources = _crawl_sources(
        config_path=config_path,
        runtime_profile=runtime_profile,
    )
    observed_at = _utc_now()
    files: dict[str, bytes] = {}
    accepted: dict[str, tuple[SourceItem, Revision, Event, str]] = {}
    rejected = 0
    for source, raw_items in sorted(raw_sources.items(), key=lambda pair: str(pair[0])):
        if (
            not isinstance(source, str)
            or not isinstance(raw_items, Sequence)
            or isinstance(raw_items, (str, bytes))
        ):
            rejected += 1
            continue
        for raw in raw_items:
            if not isinstance(raw, Mapping):
                rejected += 1
                continue
            try:
                normalized = json_ready(raw)
                if not isinstance(normalized, dict):
                    raise TypeError("source payload must be an object")
                url = _source_url(normalized)
                if url is None:
                    raise ValueError("source item requires a canonical URL")
                normalized["source"] = source
                item = SourceItem(
                    source=source,
                    native_id=_native_id(normalized),
                    canonical_url=url,
                    fetched_at=observed_at,
                    payload=normalized,
                )
                snapshot = _snapshot_text(item)
                snapshot_bytes = snapshot.encode("utf-8")
                revision = Revision(
                    item_id=item.item_id,
                    normalized_payload=item.payload,
                    source_snapshot_digest="sha256:" + _sha256_bytes(snapshot_bytes),
                    observed_at=observed_at,
                )
                event = Event(
                    seed_item_id=item.item_id,
                    member_item_ids=(item.item_id,),
                    first_seen=observed_at,
                    last_seen=observed_at,
                )
                accepted[revision.revision_id] = (item, revision, event, snapshot)
            except (TypeError, ValueError):
                rejected += 1

    if not accepted:
        raise PipelineError("no valid source items were discovered; refusing empty success")

    for item, revision, event, snapshot in accepted.values():
        snapshot_path = f"content/snapshots/{revision.revision_id}.txt"
        files[snapshot_path] = snapshot.encode("utf-8")
        files[f"content/events/{event.event_id}.json"] = _json_bytes(
            _discovery_envelope(item, revision, event, snapshot_path)
        )
    state = {
        "schema_version": RUN_SCHEMA,
        "run_id": run_id,
        "stage": WorkflowStatus.DISCOVERED.value,
        "code_sha": _code_sha(),
        "created_at": _utc_text(observed_at),
        "item_count": len(accepted),
        "rejected_count": rejected,
    }
    files["state/run.json"] = _json_bytes(state)
    _materialize_tree(output, files)
    return {
        "run_id": run_id,
        "item_count": len(accepted),
        "rejected_count": rejected,
    }


def _load_discovery(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    files = _scan_tree(
        root,
        ("state/run.json", "content/events/*.json", "content/snapshots/*.txt"),
    )
    if "state/run.json" not in files:
        raise PipelineError("discovery handoff is missing state/run.json")
    state = _read_json(root / "state/run.json")
    if state.get("schema_version") != RUN_SCHEMA or state.get("stage") != "DISCOVERED":
        raise PipelineError("discovery run state has an unsupported schema or stage")
    _require_run_id(str(state.get("run_id", "")))
    _require_git_sha(str(state.get("code_sha", "")), "code_sha")
    envelopes: list[dict[str, Any]] = []
    event_paths = sorted((root / "content/events").glob("*.json"))
    if not event_paths:
        raise PipelineError("discovery handoff contains no event records")
    for path in event_paths:
        envelope = _read_json(path)
        if envelope.get("schema_version") != DISCOVERY_SCHEMA:
            raise PipelineError(f"unsupported discovery event schema: {path.name}")
        item = SourceItem.from_dict(envelope["source_item"])
        revision = Revision.from_dict(envelope["revision"])
        event = Event.from_dict(envelope["event"])
        if (
            event.event_id != envelope.get("event_id")
            or path.stem != event.event_id
            or revision.item_id != item.item_id
            or item.item_id not in event.member_item_ids
        ):
            raise PipelineError(f"discovery identity mismatch: {path.name}")
        snapshot_path = envelope.get("snapshot_path")
        if not isinstance(snapshot_path, str):
            raise PipelineError(f"discovery snapshot path is invalid: {path.name}")
        expected_snapshot = f"content/snapshots/{revision.revision_id}.txt"
        if snapshot_path != expected_snapshot or snapshot_path not in files:
            raise PipelineError(f"discovery snapshot path mismatch: {path.name}")
        actual_digest = "sha256:" + _sha256_bytes(files[snapshot_path])
        if actual_digest != revision.source_snapshot_digest:
            raise PipelineError(f"discovery snapshot digest mismatch: {path.name}")
        envelopes.append(envelope)
    expected_count = state.get("item_count")
    if expected_count != len(envelopes):
        raise PipelineError("discovery item count does not match event records")
    return state, envelopes


def validate_discovery(*, input_root: Path, output: Path) -> dict[str, Any]:
    state, envelopes = _load_discovery(input_root)
    files: dict[str, bytes] = {"state/run.json": _json_bytes(state)}
    for envelope in envelopes:
        event_id = str(envelope["event_id"])
        snapshot_path = str(envelope["snapshot_path"])
        files[f"content/events/{event_id}.json"] = _json_bytes(envelope)
        files[snapshot_path] = _read_regular(input_root / snapshot_path)
    _materialize_tree(output, files)
    return {"run_id": state["run_id"], "validated_items": len(envelopes)}


def _atomic_ledger_write(root: Path, relative: str, payload: bytes) -> bool:
    path = root / relative
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError as exc:
        raise PipelineError(f"ledger write escapes root: {relative}") from exc
    if any(component.is_symlink() for component in [root, *path.parents] if component.exists()):
        raise PipelineError(f"ledger write crosses a symlink: {relative}")
    if path.exists():
        if path.is_symlink() or not path.is_file():
            raise PipelineError(f"ledger destination is not a regular file: {relative}")
        if path.read_bytes() == payload:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    finally:
        Path(temporary_name).unlink(missing_ok=True)
    return True


def _content_store(ledger_root: Path) -> FileContentStore:
    return FileContentStore(ledger_root / "state/content")


def _ops_store(ledger_root: Path) -> FileOpsStore:
    return FileOpsStore(ledger_root / "state/ops")


def _step(name: str, now: datetime, *, metadata: Mapping[str, Any] | None = None) -> StepResult:
    return StepResult(
        step=name,
        status=StepStatus.SUCCEEDED,
        started_at=now,
        finished_at=now,
        metadata=metadata or {},
    )


def persist_discovery(*, run_id: str, input_root: Path, state_root: Path) -> dict[str, Any]:
    run_id = _require_run_id(run_id)
    state, envelopes = _load_discovery(input_root)
    if state["run_id"] != run_id:
        raise PipelineError("run_id does not match discovery handoff")
    store = _content_store(state_root)
    base = store.base_revision()
    changed_items = 0
    for envelope in envelopes:
        item = SourceItem.from_dict(envelope["source_item"])
        revision = Revision.from_dict(envelope["revision"])
        event = Event.from_dict(envelope["event"])
        existing = store.get_revision(revision.revision_id)
        write = store.put_source(item, expected_base=base)
        base = write.base_revision
        write = store.put_revision(revision, expected_base=base)
        base = write.base_revision
        write = store.put_event(event, expected_base=base)
        base = write.base_revision
        if existing is None:
            changed_items += 1
        snapshot_path = str(envelope["snapshot_path"])
        _atomic_ledger_write(
            state_root,
            snapshot_path,
            _read_regular(input_root / snapshot_path),
        )
        _atomic_ledger_write(
            state_root,
            f"content/events/{event.event_id}.json",
            _json_bytes(envelope),
        )

    now = _utc_now()
    run = RunManifest(
        run_id=run_id,
        code_sha=str(state["code_sha"]),
        content_parent_sha="0" * 40,
        input_digest=sha256_digest(envelopes),
        config_digest=sha256_digest({"policy": POLICY_VERSION}),
        model=GENERATOR,
        status=WorkflowStatus.DISCOVERED,
        steps=(_step("discover", now),),
        created_at=now,
        updated_at=now,
        metadata={"event_count": len(envelopes)},
    )
    write = store.put_run(run, expected_base=base)
    return {
        "run_id": run_id,
        "changed_items": changed_items,
        "content_base": write.base_revision,
    }


def _operation_id(prefix: str, run_id: str) -> str:
    return f"op_{prefix}_{hashlib.sha256(run_id.encode()).hexdigest()}"


def _load_event_envelopes(ledger_root: Path) -> list[dict[str, Any]]:
    root = ledger_root / "content/events"
    if root.is_symlink() or not root.is_dir():
        raise PipelineError("content ledger contains no canonical event directory")
    result: list[dict[str, Any]] = []
    for path in sorted(root.glob("*.json")):
        envelope = _read_json(path)
        if envelope.get("schema_version") != DISCOVERY_SCHEMA:
            raise PipelineError(f"invalid canonical event record: {path.name}")
        Event.from_dict(envelope["event"])
        Revision.from_dict(envelope["revision"])
        SourceItem.from_dict(envelope["source_item"])
        result.append(envelope)
    if not result:
        raise PipelineError("content ledger contains no canonical events")
    return result


def _next_release_sequence(ops_root: Path, run_id: str) -> int:
    existing = ops_root / f"ops/releases/{run_id}.json"
    if existing.is_file() and not existing.is_symlink():
        value = _read_json(existing)
        sequence = value.get("release_seq")
        if isinstance(sequence, int) and not isinstance(sequence, bool) and sequence > 0:
            return sequence
        raise PipelineError("existing release sequence record is invalid")
    release_directory = ops_root / "ops/releases"
    maximum = 0
    if release_directory.exists():
        if release_directory.is_symlink() or not release_directory.is_dir():
            raise PipelineError("ops release directory is unsafe")
        for path in release_directory.glob("*.json"):
            value = _read_json(path)
            sequence = value.get("release_seq")
            if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence <= 0:
                raise PipelineError(f"invalid release sequence record: {path.name}")
            maximum = max(maximum, sequence)
    return maximum + 1


def reserve_budget(*, run_id: str, input_root: Path, state_root: Path) -> dict[str, Any]:
    run_id = _require_run_id(run_id)
    content_state = input_root / "state/content"
    if not content_state.is_dir() or content_state.is_symlink():
        raise PipelineError("content ledger state is missing")
    run = FileContentStore(content_state).get_run(run_id)
    if run is None:
        raise PipelineError(f"run not found in content ledger: {run_id}")
    envelopes = _load_event_envelopes(input_root)
    selected = envelopes[:MAX_GENERATED_ITEMS]
    selected_event_ids = [str(item["event_id"]) for item in selected]
    selected_revision_ids = [str(item["revision"]["revision_id"]) for item in selected]
    token_limit = min(200_000, 40_000 * len(selected))
    now = run.created_at
    store = _ops_store(state_root)
    base = store.base_revision()
    operation_id = _operation_id("budget", run_id)
    existing = store.get_operation(operation_id)
    if existing is None:
        operation = OperationRecord(
            operation_id=operation_id,
            kind=OperationKind.BUDGET_RESERVATION,
            status=OperationStatus.RESERVED,
            idempotency_key=f"budget:{run_id}",
            created_at=now,
            updated_at=now,
            token_limit=token_limit,
            metadata={
                "run_id": run_id,
                "generator": GENERATOR,
                "selected_event_ids": selected_event_ids,
                "selected_revision_ids": selected_revision_ids,
                "maximum_model_calls": min(20, len(selected) * 4),
            },
        )
        write = store.put_operation(operation, expected_base=base)
        base = write.base_revision
    else:
        operation = existing
        if operation.status is not OperationStatus.RESERVED:
            raise PipelineError("budget reservation is not in RESERVED state")

    release_seq = _next_release_sequence(state_root, run_id)
    release_operation_id = _operation_id("release", run_id)
    release_operation = store.get_operation(release_operation_id)
    if release_operation is None:
        release_operation = OperationRecord(
            operation_id=release_operation_id,
            kind=OperationKind.RELEASE_SEQUENCE,
            status=OperationStatus.RESERVED,
            idempotency_key=f"release-sequence:{run_id}",
            created_at=now,
            updated_at=now,
            metadata={"run_id": run_id, "release_seq": release_seq},
        )
        store.put_operation(release_operation, expected_base=base)
    elif release_operation.metadata.get("release_seq") != release_seq:
        raise PipelineError("release sequence idempotency record changed")

    budget_payload = model_to_dict(operation)
    _atomic_ledger_write(
        state_root,
        f"ops/budget/{operation_id}.json",
        _json_bytes({"schema_version": "budget_reservation_v1", **budget_payload}),
    )
    _atomic_ledger_write(
        state_root,
        f"ops/releases/{run_id}.json",
        _json_bytes(
            {
                "schema_version": "release_sequence_v1",
                "run_id": run_id,
                "operation_id": release_operation_id,
                "release_seq": release_seq,
            }
        ),
    )
    return {
        "run_id": run_id,
        "operation_id": operation_id,
        "status": operation.status.value,
        "token_limit": operation.token_limit,
        "release_seq": release_seq,
    }


def _safe_title(payload: Mapping[str, Any], fallback: str) -> str:
    title = _plain_field(payload, ("title", "name", "headline"), fallback)
    title = "".join(character for character in title if ord(character) >= 32)
    return title[:160] or "来源简讯"


def _markdown_text(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("[", "\\[")
        .replace("]", "\\]")
    )


def _candidate_from_envelope(
    envelope: Mapping[str, Any], snapshot: str, run_id: str
) -> dict[str, Any]:
    item = SourceItem.from_dict(envelope["source_item"])
    revision = Revision.from_dict(envelope["revision"])
    event = Event.from_dict(envelope["event"])
    title = _safe_title(item.payload, item.canonical_url)
    excerpt_bytes = title.encode("utf-8")
    snapshot_bytes = snapshot.encode("utf-8")
    start = snapshot_bytes.find(excerpt_bytes)
    if start < 0:
        raise PipelineError(f"source title is not locatable in snapshot: {revision.revision_id}")
    end = start + len(excerpt_bytes)
    claim_id = "clm_" + hashlib.sha256(f"{revision.revision_id}\x1f{title}".encode()).hexdigest()
    evidence = Evidence(
        source_url=item.canonical_url,
        snapshot_digest=revision.source_snapshot_digest,
        locator=f"bytes:{start}-{end}",
        excerpt=title,
        claim_ids=(claim_id,),
        captured_at=revision.observed_at,
    )
    generation_key = make_generation_key(
        revision.revision_id,
        GENERATOR,
        PROMPT_VERSION,
        POLICY_VERSION,
    )
    claim = {
        "id": claim_id,
        "kind": "source_claim",
        "text": f"原始来源记录的标题为：{title}",
        "evidence_ids": [evidence.evidence_id],
    }
    body = (
        "这是自动生成的来源简讯，只复述已保存快照中可定位的字段，不包含扩展推断。\n\n"
        f"**来源标题：** {_markdown_text(title)}\n\n"
        f"[查看原始来源]({item.canonical_url})"
    )
    raw_tags = item.payload.get("tags", ())
    tags = (
        tuple(str(tag).strip()[:80] for tag in raw_tags if str(tag).strip())
        if isinstance(raw_tags, (list, tuple))
        else ()
    )
    article = ArticleRevision(
        event_id=event.event_id,
        generation_key=generation_key,
        title=title,
        body=body,
        created_at=revision.observed_at,
        claims=(claim,),
        evidence_ids=(evidence.evidence_id,),
        source_support=1.0,
        tags=tags,
    )
    gate_evidence = {
        "id": evidence.evidence_id,
        "snapshot_id": revision.revision_id,
        "url": item.canonical_url,
        "snapshot_sha256": revision.source_snapshot_digest.removeprefix("sha256:"),
        "snippet": title,
        "start_byte": start,
        "end_byte": end,
    }
    return {
        "schema_version": GENERATED_SCHEMA,
        "run_id": run_id,
        "generator": GENERATOR,
        "source_item": model_to_dict(item),
        "revision": model_to_dict(revision),
        "event": model_to_dict(event),
        "evidence": model_to_dict(evidence),
        "article": model_to_dict(article),
        "gate_payload": {
            "body": body,
            "content_mode": "source_brief",
            "claims": [claim],
            "evidence": [gate_evidence],
            "inferences": [],
            "risk_domain": "technology",
        },
        "snapshots": {revision.revision_id: snapshot},
    }


def generate(*, run_id: str, input_root: Path, ops_root: Path, output: Path) -> dict[str, Any]:
    run_id = _require_run_id(run_id)
    content_state = input_root / "state/content"
    ops_state = ops_root / "state/ops"
    if not content_state.is_dir() or content_state.is_symlink():
        raise PipelineError("content ledger state is missing")
    if not ops_state.is_dir() or ops_state.is_symlink():
        raise PipelineError("budget reservation state is missing")
    content_store = FileContentStore(content_state)
    if content_store.get_run(run_id) is None:
        raise PipelineError(f"run not found in content ledger: {run_id}")
    operation = FileOpsStore(ops_state).get_operation(_operation_id("budget", run_id))
    if operation is None or operation.status is not OperationStatus.RESERVED:
        raise PipelineError("a RESERVED budget reservation is required before generation")
    selected = operation.metadata.get("selected_event_ids")
    if not isinstance(selected, (list, tuple)) or not selected:
        raise PipelineError("budget reservation selected no event identities")
    selected_ids = {str(value) for value in selected}
    envelopes = [
        envelope
        for envelope in _load_event_envelopes(input_root)
        if str(envelope["event_id"]) in selected_ids
    ]
    if len(envelopes) != len(selected_ids):
        raise PipelineError("budget reservation references missing content events")
    files: dict[str, bytes] = {}
    for envelope in envelopes:
        revision_id = str(envelope["revision"]["revision_id"])
        snapshot = _read_regular(input_root / f"content/snapshots/{revision_id}.txt").decode(
            "utf-8"
        )
        candidate = _candidate_from_envelope(envelope, snapshot, run_id)
        article_id = str(candidate["article"]["article_revision_id"])
        files[f"content/candidates/{article_id}.json"] = _json_bytes(candidate)
    state = {
        "schema_version": RUN_SCHEMA,
        "run_id": run_id,
        "stage": WorkflowStatus.GENERATED.value,
        "generator": GENERATOR,
        "candidate_count": len(envelopes),
    }
    files["state/run.json"] = _json_bytes(state)
    _materialize_tree(output, files)
    return {
        "run_id": run_id,
        "generator": GENERATOR,
        "candidate_count": len(envelopes),
    }


def _load_generated(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    _scan_tree(root, ("state/run.json", "content/candidates/*.json"))
    state = _read_json(root / "state/run.json")
    if state.get("schema_version") != RUN_SCHEMA or state.get("stage") != "GENERATED":
        raise PipelineError("generated handoff has an unsupported schema or stage")
    run_id = _require_run_id(str(state.get("run_id", "")))
    candidates: list[dict[str, Any]] = []
    for path in sorted((root / "content/candidates").glob("*.json")):
        candidate = _read_json(path)
        if candidate.get("schema_version") != GENERATED_SCHEMA:
            raise PipelineError(f"invalid generated candidate schema: {path.name}")
        if candidate.get("run_id") != run_id or candidate.get("generator") != GENERATOR:
            raise PipelineError(f"generated candidate identity mismatch: {path.name}")
        article = ArticleRevision.from_dict(candidate["article"])
        Evidence.from_dict(candidate["evidence"])
        Revision.from_dict(candidate["revision"])
        Event.from_dict(candidate["event"])
        SourceItem.from_dict(candidate["source_item"])
        if path.stem != article.article_revision_id:
            raise PipelineError(f"generated article filename mismatch: {path.name}")
        candidates.append(candidate)
    if state.get("candidate_count") != len(candidates) or not candidates:
        raise PipelineError("generated candidate count is empty or inconsistent")
    return state, candidates


def _publisher_platforms(config_path: Path) -> tuple[str, ...]:
    try:
        loaded = yaml.safe_load(_read_regular(config_path).decode("utf-8"))
    except yaml.YAMLError as exc:
        raise PipelineError("publisher configuration is invalid YAML") from exc
    raw = {} if loaded is None else loaded
    if not isinstance(raw, dict):
        raise PipelineError("publisher configuration must be an object")
    publishers = raw.get("publishers", {})
    if not isinstance(publishers, dict):
        raise PipelineError("publisher configuration publishers must be an object")
    supported = {"telegram", "twitter", "wechat"}
    result: list[str] = []
    for platform, config in publishers.items():
        if platform not in supported:
            continue
        if not isinstance(config, dict):
            raise PipelineError(f"publisher configuration is invalid: {platform}")
        if config.get("enabled") is True:
            result.append(platform)
    return tuple(sorted(result))


def _markdown_document(
    article: ArticleRevision,
    item: SourceItem,
    event: Event,
    tier: str,
) -> str:
    title = json.dumps(article.title, ensure_ascii=False)
    source_url = json.dumps(item.canonical_url, ensure_ascii=False)
    tags = json.dumps(list(article.tags), ensure_ascii=False)
    return (
        "---\n"
        f"title: {title}\n"
        f"date: {_utc_text(article.created_at)}\n"
        "draft: false\n"
        'entry_kind: "auto"\n'
        f'event_id: "{event.event_id}"\n'
        f'article_revision_id: "{article.article_revision_id}"\n'
        f"external_url: {source_url}\n"
        f'publication_tier: "{tier}"\n'
        f"source_support: {article.source_support}\n"
        f"tags: {tags}\n"
        "---\n\n"
        f"{article.body}\n"
    )


def validate_generated(
    *,
    input_root: Path,
    output: Path,
    publisher_config: Path = Path("config/publisher.yaml"),
) -> dict[str, Any]:
    state, candidates = _load_generated(input_root)
    files: dict[str, bytes] = {}
    publishable = 0
    quarantined = 0
    platforms = _publisher_platforms(publisher_config)
    gate = _evidence_gate()
    for candidate in candidates:
        article = ArticleRevision.from_dict(candidate["article"])
        evidence = Evidence.from_dict(candidate["evidence"])
        item = SourceItem.from_dict(candidate["source_item"])
        event = Event.from_dict(candidate["event"])
        gate_payload = candidate.get("gate_payload")
        snapshots = candidate.get("snapshots")
        if not isinstance(gate_payload, Mapping) or not isinstance(snapshots, Mapping):
            raise PipelineError("generated candidate gate payload is invalid")
        decision = gate.evaluate(gate_payload, snapshots)
        if not decision.publishable:
            quarantined += 1
            files[f"content/quarantine/{article.article_revision_id}.json"] = _json_bytes(
                {
                    "schema_version": "quarantine_v1",
                    "run_id": state["run_id"],
                    "article_revision_id": article.article_revision_id,
                    "reasons": list(decision.reasons),
                    "candidate_digest": _sha256_bytes(_json_bytes(candidate)),
                }
            )
            continue
        # Source briefs are deliberately downgraded to C even when their single
        # source claim has complete evidence.  C means "no added analysis".
        tier = "C" if gate_payload.get("content_mode") == "source_brief" else decision.tier.value
        document = _markdown_document(article, item, event, tier)
        try:
            _validate_markdown(document)
        except ValueError as exc:
            quarantined += 1
            files[f"content/quarantine/{article.article_revision_id}.json"] = _json_bytes(
                {
                    "schema_version": "quarantine_v1",
                    "run_id": state["run_id"],
                    "article_revision_id": article.article_revision_id,
                    "reasons": [f"content_security:{type(exc).__name__}"],
                    "candidate_digest": _sha256_bytes(_json_bytes(candidate)),
                }
            )
            continue
        publishable += 1
        validated = {
            "schema_version": VALIDATED_SCHEMA,
            "run_id": state["run_id"],
            "publication_tier": tier,
            "article": model_to_dict(article),
            "evidence": model_to_dict(evidence),
            "event_id": event.event_id,
            "source_item_id": item.item_id,
            "markdown_path": f"content/posts/{article.article_revision_id}.md",
        }
        files[f"content/articles/{article.article_revision_id}.json"] = _json_bytes(validated)
        files[str(validated["markdown_path"])] = document.encode("utf-8")
        for platform in platforms:
            key = _outbox_key(
                article.article_revision_id,
                platform,
                "source-brief-v1",
            )
            files[f"content/outbox/{key}.json"] = _json_bytes(
                {
                    "schema_version": OUTBOX_SCHEMA,
                    "run_id": state["run_id"],
                    "idempotency_key": key,
                    "event_revision": article.article_revision_id,
                    "platform": platform,
                    "template_version": "source-brief-v1",
                    "payload": {
                        "title": article.title,
                        "summary": article.body,
                        "url": item.canonical_url,
                        "source": item.source,
                        "tags": list(article.tags),
                    },
                }
            )
    files["content/outbox/index.json"] = _json_bytes(
        {
            "schema_version": OUTBOX_SCHEMA,
            "run_id": state["run_id"],
            "record_count": sum(1 for path in files if path.startswith("content/outbox/")),
        }
    )
    files["state/run.json"] = _json_bytes(
        {
            "schema_version": RUN_SCHEMA,
            "run_id": state["run_id"],
            "stage": WorkflowStatus.VALIDATED.value,
            "publishable": publishable,
            "quarantined": quarantined,
        }
    )
    _materialize_tree(output, files)
    return {
        "run_id": state["run_id"],
        "publishable": publishable,
        "quarantined": quarantined,
    }


def _load_validated(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    files = _scan_tree(
        root,
        (
            "state/run.json",
            "content/articles/*.json",
            "content/posts/*.md",
            "content/outbox/*.json",
            "content/quarantine/*.json",
        ),
    )
    state = _read_json(root / "state/run.json")
    if state.get("schema_version") != RUN_SCHEMA or state.get("stage") != "VALIDATED":
        raise PipelineError("validated handoff has an unsupported schema or stage")
    records: list[dict[str, Any]] = []
    for path in sorted((root / "content/articles").glob("*.json")):
        record = _read_json(path)
        if record.get("schema_version") != VALIDATED_SCHEMA:
            raise PipelineError(f"invalid validated article schema: {path.name}")
        article = ArticleRevision.from_dict(record["article"])
        Evidence.from_dict(record["evidence"])
        if article.article_revision_id != path.stem:
            raise PipelineError(f"validated article filename mismatch: {path.name}")
        markdown_path = str(record.get("markdown_path", ""))
        if markdown_path not in files:
            raise PipelineError(f"validated article Markdown is missing: {path.name}")
        _validate_markdown(files[markdown_path].decode("utf-8"))
        records.append(record)
    expected = state.get("publishable")
    if expected != len(records):
        raise PipelineError("validated article count is inconsistent")
    return state, records


def persist_result(*, run_id: str, input_root: Path, state_root: Path) -> dict[str, Any]:
    run_id = _require_run_id(run_id)
    state, records = _load_validated(input_root)
    if state.get("run_id") != run_id:
        raise PipelineError("run_id does not match validated handoff")
    content_state = state_root / "state/content"
    if not content_state.is_dir() or content_state.is_symlink():
        raise PipelineError("content ledger state is missing")
    store = FileContentStore(content_state)
    run = store.get_run(run_id)
    if run is None:
        raise PipelineError(f"run not found in content ledger: {run_id}")
    base = store.base_revision()
    persisted = 0
    for record in records:
        article = ArticleRevision.from_dict(record["article"])
        evidence = Evidence.from_dict(record["evidence"])
        existing = store.get_article(article.article_revision_id)
        write = store.put_evidence(evidence, expected_base=base)
        base = write.base_revision
        write = store.put_article(article, expected_base=base)
        base = write.base_revision
        if existing is None:
            persisted += 1
        markdown_path = str(record["markdown_path"])
        _atomic_ledger_write(
            state_root,
            markdown_path,
            _read_regular(input_root / markdown_path),
        )
        _atomic_ledger_write(
            state_root,
            f"content/articles/{article.article_revision_id}.json",
            _json_bytes(record),
        )
    for directory in ("content/outbox", "content/quarantine"):
        source = input_root / directory
        if source.is_dir() and not source.is_symlink():
            for path in sorted(source.glob("*.json")):
                _atomic_ledger_write(
                    state_root,
                    f"{directory}/{path.name}",
                    _read_regular(path),
                )
    now = _utc_now()
    updated = RunManifest(
        run_id=run.run_id,
        code_sha=run.code_sha,
        content_parent_sha=run.content_parent_sha,
        input_digest=run.input_digest,
        config_digest=run.config_digest,
        model=run.model,
        status=WorkflowStatus.PERSISTED,
        steps=run.steps
        + (
            _step("generate", now),
            _step("validate", now),
            _step("persist", now),
        ),
        created_at=run.created_at,
        updated_at=now,
        metadata={**dict(run.metadata), "article_count": len(records)},
    )
    write = store.put_run(updated, expected_base=base)
    return {
        "run_id": run_id,
        "persisted_articles": persisted,
        "content_base": write.base_revision,
    }


def _release_identity(*, release_seq: int, code_sha: str, content_sha: str) -> str:
    digest = _sha256_bytes(
        canonical_json_bytes(
            {
                "schema_version": RELEASE_SCHEMA_VERSION,
                "release_seq": release_seq,
                "code_sha": code_sha,
                "content_sha": content_sha,
            }
        )
    )
    return f"r-{digest[:24]}"


def _intelligence_events(envelopes: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for envelope in envelopes:
        event = Event.from_dict(envelope["event"])
        item = SourceItem.from_dict(envelope["source_item"])
        title = _safe_title(item.payload, item.canonical_url)
        tags_raw = item.payload.get("tags", [])
        tags = (
            [str(tag).strip() for tag in tags_raw if str(tag).strip()]
            if isinstance(tags_raw, (list, tuple))
            else []
        )
        result.append(
            {
                "event_id": event.event_id,
                "canonical_event_id": event.event_id,
                "status": event.status.value,
                "source": item.source,
                "title": title,
                "url": item.canonical_url,
                "first_seen": _utc_text(event.first_seen),
                "updated_at": _utc_text(event.last_seen),
                "topics": tags,
                "tags": tags,
                "entities": [],
                "source_weight": 0.5,
                "public": True,
            }
        )
    return result


def render(
    *,
    run_id: str,
    code_sha: str,
    content_sha: str,
    ops_sha: str,
    content_root: Path,
    ops_root: Path,
    output: Path,
    site_static_root: Path = Path("blog/static"),
) -> dict[str, Any]:
    run_id = _require_run_id(run_id)
    code_sha = _require_git_sha(code_sha, "code_sha")
    content_sha = _require_git_sha(content_sha, "content_sha")
    ops_sha = _require_git_sha(ops_sha, "ops_sha")
    content_state = content_root / "state/content"
    ops_state = ops_root / "state/ops"
    if not content_state.is_dir() or not ops_state.is_dir():
        raise PipelineError("content and ops ledger state are both required")
    content_report = FileContentStore(content_state).validate()
    ops_report = FileOpsStore(ops_state).validate()
    if not content_report.valid or not ops_report.valid:
        raise PipelineError("content or ops ledger integrity validation failed")
    run = FileContentStore(content_state).get_run(run_id)
    if run is None or run.status is not WorkflowStatus.PERSISTED:
        raise PipelineError("render requires a PERSISTED run manifest")
    release_record = _read_json(ops_root / f"ops/releases/{run_id}.json")
    release_seq = release_record.get("release_seq")
    if not isinstance(release_seq, int) or isinstance(release_seq, bool) or release_seq <= 0:
        raise PipelineError("render requires a valid reserved release sequence")
    release_id = _release_identity(
        release_seq=release_seq,
        code_sha=code_sha,
        content_sha=content_sha,
    )
    envelopes = _load_event_envelopes(content_root)
    public_events = _intelligence_events(envelopes)
    as_of = max(Event.from_dict(item["event"]).last_seen for item in envelopes)
    _build_intelligence()(
        output_dir=site_static_root,
        events=public_events,
        as_of=as_of,
        release_id=release_id,
    )
    root_manifest_path = site_static_root / "api/v1/manifest.json"
    root_manifest = _read_json(root_manifest_path)
    root_manifest["build"] = {
        "release_id": release_id,
        "code_sha": code_sha,
        "content_sha": content_sha,
        "refreshed_at": _utc_text(as_of),
        "source_status": "healthy",
    }
    _atomic_ledger_write(site_static_root, "api/v1/manifest.json", _json_bytes(root_manifest))

    generated_at = _utc_text(_utc_now())
    basis = {
        "basis_schema_version": "release_basis_v1",
        "release_id": release_id,
        "code_sha": code_sha,
        "content_sha": content_sha,
        "schema_version": RELEASE_SCHEMA_VERSION,
        "release_seq": release_seq,
        "generated_at": generated_at,
    }
    files: dict[str, bytes] = {
        # The final descriptor cannot exist until Hugo, Pagefind and the DOM
        # validator finish.  release_guard create hashes blog/public later.
        "state/release-basis.json": _json_bytes(basis),
    }
    outbox = content_root / "content/outbox"
    if outbox.is_dir() and not outbox.is_symlink():
        for path in sorted(outbox.glob("*.json")):
            files[f"content/outbox/{path.name}"] = _read_regular(path)
    if not any(path.startswith("content/outbox/") for path in files):
        files["content/outbox/index.json"] = _json_bytes(
            {
                "schema_version": OUTBOX_SCHEMA,
                "run_id": run_id,
                "record_count": 0,
            }
        )
    _materialize_tree(output, files)
    return {
        "run_id": run_id,
        "release_id": release_id,
        "release_basis": "state/release-basis.json",
        "public_tree_digest": None,
        "transport_archive_digest": None,
    }


def _load_outbox(input_root: Path, run_id: str) -> list[dict[str, Any]]:
    if input_root.is_symlink() or not input_root.is_dir():
        raise PipelineError("outbox input must be a regular directory")
    records: list[dict[str, Any]] = []
    for path in sorted(input_root.glob("*.json")):
        value = _read_json(path)
        if path.name == "index.json":
            if value.get("schema_version") != OUTBOX_SCHEMA:
                raise PipelineError("outbox index schema is invalid")
            continue
        required = {
            "schema_version",
            "run_id",
            "idempotency_key",
            "event_revision",
            "platform",
            "template_version",
            "payload",
        }
        if set(value) != required or value.get("schema_version") != OUTBOX_SCHEMA:
            raise PipelineError(f"outbox record schema is invalid: {path.name}")
        if value["run_id"] != run_id or value["idempotency_key"] != path.stem:
            raise PipelineError(f"outbox record identity mismatch: {path.name}")
        expected = _outbox_key(
            str(value["event_revision"]),
            str(value["platform"]),
            str(value["template_version"]),
        )
        if expected != value["idempotency_key"] or not isinstance(value["payload"], dict):
            raise PipelineError(f"outbox idempotency key mismatch: {path.name}")
        records.append(value)
    return records


def publish(*, run_id: str, input_root: Path, output: Path, config_path: Path) -> dict[str, Any]:
    run_id = _require_run_id(run_id)
    records = _load_outbox(input_root, run_id)
    enabled = set(_publisher_platforms(config_path))
    orchestrator: _PublisherOrchestrator | None = None
    files: dict[str, bytes] = {}
    unknown = 0
    for record in records:
        platform = str(record["platform"])
        status = "disabled"
        detail = "platform_disabled"
        if platform in enabled:
            if orchestrator is None:
                factory = cast(
                    Callable[..., _PublisherOrchestrator],
                    importlib.import_module("publisher.main").PublisherOrchestrator,
                )
                orchestrator = factory(config_path=config_path)
            publisher = orchestrator.publishers.get(platform)
            if publisher is None:
                raise PipelineError(f"enabled publisher was not initialized: {platform}")
            try:
                success = publisher.publish_content(record["payload"])
            except Exception as exc:  # uncertain remote outcome must not be retried blindly
                status = "unknown"
                detail = type(exc).__name__
                unknown += 1
            else:
                status = "sent" if success else "failed"
                detail = "provider_acknowledged" if success else "provider_rejected"
        receipt = {
            "schema_version": RECEIPT_SCHEMA,
            "run_id": run_id,
            "idempotency_key": record["idempotency_key"],
            "platform": platform,
            "status": status,
            "detail": detail,
            "attempts": 1 if platform in enabled else 0,
        }
        files[f"ops/receipts/{record['idempotency_key']}.json"] = _json_bytes(receipt)
    files["ops/receipts/index.json"] = _json_bytes(
        {
            "schema_version": RECEIPT_SCHEMA,
            "run_id": run_id,
            "record_count": len(records),
            "unknown_count": unknown,
        }
    )
    files["state/receipt.json"] = _json_bytes(
        {
            "schema_version": RUN_SCHEMA,
            "run_id": run_id,
            "stage": WorkflowStatus.NOTIFIED.value,
            "receipt_count": len(records),
            "unknown_count": unknown,
        }
    )
    _materialize_tree(output, files)
    return {
        "run_id": run_id,
        "status": WorkflowStatus.NOTIFIED.value,
        "receipt_count": len(records),
        "unknown_count": unknown,
    }


def persist_release(
    *,
    run_id: str,
    input_root: Path,
    state_root: Path,
    expected_release_id: str,
    expected_code_sha: str,
    expected_content_sha: str,
    expected_artifact_digest: str,
) -> dict[str, Any]:
    """Append and advance the current healthy release after production health.

    The per-release record is immutable.  ``current-healthy.json`` may only
    advance to a higher sequence or be replayed with the exact same descriptor.
    Git CAS supplies the branch-level compare-and-swap around these file writes.
    """

    from scripts.release_guard import (
        ReleaseValidationError,
        assert_release_is_fresh,
        load_release_descriptor,
        validate_public_tree_manifest_digest,
    )

    run_id = _require_run_id(run_id)
    _scan_tree(
        input_root,
        (
            "state/release-basis.json",
            "state/release.json",
            "state/public-tree-manifest.json",
            "content/outbox/*.json",
        ),
        max_file_bytes=MAX_RELEASE_STATE_FILE_BYTES,
    )
    try:
        candidate = load_release_descriptor(input_root / "state/release.json")
        validate_public_tree_manifest_digest(
            candidate,
            input_root / "state/public-tree-manifest.json",
        )
        expected = {
            "release_id": expected_release_id,
            "code_sha": expected_code_sha,
            "content_sha": expected_content_sha,
            "artifact_digest": expected_artifact_digest,
        }
        for field, value in expected.items():
            if getattr(candidate, field) != value:
                raise ReleaseValidationError(f"{field} does not match workflow input")

        current_path = state_root / "ops/releases/current-healthy.json"
        current = (
            load_release_descriptor(current_path)
            if current_path.exists() or current_path.is_symlink()
            else None
        )
        if current != candidate:
            assert_release_is_fresh(candidate, current)

        archive_relative = (
            f"ops/releases/healthy/{candidate.release_seq:020d}-{candidate.release_id}.json"
        )
        archive_path = state_root / archive_relative
        if archive_path.exists() or archive_path.is_symlink():
            existing_archive = load_release_descriptor(archive_path)
            if existing_archive != candidate:
                raise ReleaseValidationError("healthy release archive collision")
    except ReleaseValidationError as exc:
        raise PipelineError(str(exc)) from exc

    payload = _json_bytes(candidate.to_dict())
    archive_changed = _atomic_ledger_write(state_root, archive_relative, payload)
    advanced = _atomic_ledger_write(
        state_root,
        "ops/releases/current-healthy.json",
        payload,
    )
    return {
        "run_id": run_id,
        "release_id": candidate.release_id,
        "release_seq": candidate.release_seq,
        "persisted": bool(archive_changed or advanced),
    }


def persist_receipt(*, run_id: str, input_root: Path, state_root: Path) -> dict[str, Any]:
    run_id = _require_run_id(run_id)
    _scan_tree(input_root, ("state/receipt.json", "ops/receipts/*.json"))
    state = _read_json(input_root / "state/receipt.json")
    if (
        state.get("schema_version") != RUN_SCHEMA
        or state.get("stage") != "NOTIFIED"
        or state.get("run_id") != run_id
    ):
        raise PipelineError("receipt handoff state is invalid")
    store = _ops_store(state_root)
    base = store.base_revision()
    persisted = 0
    for path in sorted((input_root / "ops/receipts").glob("*.json")):
        receipt = _read_json(path)
        if path.name == "index.json":
            _atomic_ledger_write(
                state_root,
                "ops/receipts/index.json",
                _read_regular(path),
            )
            continue
        if receipt.get("schema_version") != RECEIPT_SCHEMA:
            raise PipelineError(f"receipt schema is invalid: {path.name}")
        key = str(receipt.get("idempotency_key", ""))
        if key != path.stem:
            raise PipelineError(f"receipt identity mismatch: {path.name}")
        status_map = {
            "sent": OperationStatus.COMPLETED,
            "failed": OperationStatus.FAILED,
            "disabled": OperationStatus.CANCELLED,
            "unknown": OperationStatus.UNKNOWN,
        }
        try:
            operation_status = status_map[str(receipt["status"])]
        except KeyError as exc:
            raise PipelineError(f"receipt status is invalid: {path.name}") from exc
        now = _utc_now()
        operation = OperationRecord(
            operation_id=f"op_receipt_{key}",
            kind=OperationKind.PUBLISH_RECEIPT,
            status=operation_status,
            idempotency_key=key,
            created_at=now,
            updated_at=now,
            metadata={
                "run_id": run_id,
                "platform": receipt["platform"],
                "detail": receipt["detail"],
            },
        )
        existing = store.get_operation(operation.operation_id)
        if existing is None:
            write = store.put_operation(operation, expected_base=base)
            base = write.base_revision
            persisted += 1
        elif existing.idempotency_key != key:
            raise PipelineError("receipt operation id collision")
        _atomic_ledger_write(
            state_root,
            f"ops/receipts/{path.name}",
            _read_regular(path),
        )
    return {"run_id": run_id, "persisted_receipts": persisted}


__all__ = [
    "PipelineError",
    "crawl",
    "generate",
    "persist_discovery",
    "persist_release",
    "persist_receipt",
    "persist_result",
    "publish",
    "render",
    "reserve_budget",
    "validate_discovery",
    "validate_generated",
]
