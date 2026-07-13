from __future__ import annotations

import fcntl
import json
import os
import re
import stat
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping, Protocol, cast, runtime_checkable

from ._json import canonical_json_bytes, sha256_hex
from .models import (
    ArticleRevision,
    Event,
    Evidence,
    OperationRecord,
    Revision,
    RunManifest,
    SourceItem,
    model_to_dict,
)


_RECORD_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,255}$")
_MANIFEST_ID = re.compile(r"^man_[0-9a-f]{64}$")
_OBJECT_ID = re.compile(r"^obj_[0-9a-f]{64}$")
_MAX_LEDGER_FILE_BYTES = 64 * 1024 * 1024


class StoreError(RuntimeError):
    """Base class for durable ledger failures."""


class UnsafeStorePathError(StoreError):
    """Raised when a symlink or traversal-like identifier reaches the ledger."""


class StoreIntegrityError(StoreError):
    """Raised when content-addressed data does not match its digest."""


class StoreConflictError(StoreError):
    def __init__(self, expected_base: str, actual_base: str) -> None:
        super().__init__(
            f"store base changed: expected {expected_base}, found {actual_base}"
        )
        self.expected_base = expected_base
        self.actual_base = actual_base


@dataclass(frozen=True, slots=True)
class StoreWrite:
    changed: bool
    base_revision: str
    previous_base: str
    object_digest: str


@dataclass(frozen=True, slots=True)
class StoreStatus:
    base_revision: str
    record_counts: Mapping[str, int]


@dataclass(frozen=True, slots=True)
class IntegrityReport:
    valid: bool
    base_revision: str | None
    record_counts: Mapping[str, int]
    errors: tuple[str, ...]


@runtime_checkable
class ContentStore(Protocol):
    def base_revision(self) -> str: ...

    def put_source(self, item: SourceItem, *, expected_base: str) -> StoreWrite: ...

    def get_source(self, item_id: str) -> SourceItem | None: ...

    def put_revision(self, revision: Revision, *, expected_base: str) -> StoreWrite: ...

    def get_revision(self, revision_id: str) -> Revision | None: ...

    def put_event(self, event: Event, *, expected_base: str) -> StoreWrite: ...

    def get_event(self, event_id: str) -> Event | None: ...

    def put_evidence(self, evidence: Evidence, *, expected_base: str) -> StoreWrite: ...

    def get_evidence(self, evidence_id: str) -> Evidence | None: ...

    def put_article(
        self, article: ArticleRevision, *, expected_base: str
    ) -> StoreWrite: ...

    def get_article(self, article_revision_id: str) -> ArticleRevision | None: ...

    def put_run(self, run: RunManifest, *, expected_base: str) -> StoreWrite: ...

    def get_run(self, run_id: str) -> RunManifest | None: ...

    def status(self) -> StoreStatus: ...

    def validate(self) -> IntegrityReport: ...


@runtime_checkable
class OpsStore(Protocol):
    def base_revision(self) -> str: ...

    def put_operation(
        self, operation: OperationRecord, *, expected_base: str
    ) -> StoreWrite: ...

    def get_operation(self, operation_id: str) -> OperationRecord | None: ...

    def status(self) -> StoreStatus: ...

    def validate(self) -> IntegrityReport: ...


def _safe_record_id(value: str) -> str:
    if not isinstance(value, str) or not _RECORD_ID.fullmatch(value):
        raise UnsafeStorePathError(f"unsafe record identifier: {value!r}")
    return value


def _file_payload(value: Any) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def _object_id(data: bytes) -> str:
    return "obj_" + sha256_hex(data)


def _manifest_id(data: bytes) -> str:
    return "man_" + sha256_hex(data)


def _reject_symlink(path: Path) -> None:
    if path.is_symlink():
        raise UnsafeStorePathError(f"symlink paths are not allowed: {path}")


def _reject_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        _reject_symlink(current)


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write(path: Path, data: bytes) -> None:
    _reject_symlink(path)
    _reject_symlink(path.parent)
    temporary = path.parent / f".{path.name}.{uuid.uuid4().hex}.tmp"
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    except BaseException:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def _read_bytes(path: Path) -> bytes:
    _reject_symlink(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        details = os.fstat(descriptor)
        if not stat.S_ISREG(details.st_mode):
            raise UnsafeStorePathError(f"ledger path is not a regular file: {path}")
        if details.st_size > _MAX_LEDGER_FILE_BYTES:
            raise StoreIntegrityError(f"ledger file exceeds size limit: {path.name}")
        with os.fdopen(descriptor, "rb") as stream:
            return stream.read()
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise


class _FileLedger:
    schema_version = 1

    def __init__(self, root: str | Path, collections: frozenset[str]) -> None:
        self.root = Path(root).absolute()
        self.collections = collections
        _reject_symlink_components(self.root)
        if self.root.exists() and not self.root.is_dir():
            raise UnsafeStorePathError(f"ledger root is not a directory: {self.root}")
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.objects = self.root / "objects"
        self.manifests = self.root / "manifests"
        self.head = self.root / "HEAD.json"
        self.lock = self.root / ".lock"
        for directory in (self.objects, self.manifests):
            _reject_symlink(directory)
            if directory.exists() and not directory.is_dir():
                raise UnsafeStorePathError(f"ledger path is not a directory: {directory}")
            directory.mkdir(mode=0o700, exist_ok=True)
        _reject_symlink(self.head)
        _reject_symlink(self.lock)
        with self._locked():
            if not self.head.exists():
                self._initialize()

    @contextmanager
    def _locked(self) -> Iterator[None]:
        _reject_symlink(self.lock)
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(self.lock, flags, 0o600)
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def _initialize(self) -> None:
        manifest: dict[str, Any] = {
            "parent": None,
            "records": {},
            "schema_version": self.schema_version,
        }
        data = _file_payload(manifest)
        base = _manifest_id(data)
        _atomic_write(self.manifests / f"{base}.json", data)
        _atomic_write(self.head, _file_payload({"base": base}))

    def _base(self) -> str:
        try:
            value = json.loads(_read_bytes(self.head))
            base = value["base"]
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
            raise StoreIntegrityError("HEAD.json is invalid") from error
        if not isinstance(base, str) or not _MANIFEST_ID.fullmatch(base):
            raise StoreIntegrityError("HEAD.json contains an invalid manifest id")
        return base

    def _manifest(self, base: str) -> dict[str, Any]:
        if not _MANIFEST_ID.fullmatch(base):
            raise StoreIntegrityError(f"invalid manifest id: {base!r}")
        data = _read_bytes(self.manifests / f"{base}.json")
        if _manifest_id(data) != base:
            raise StoreIntegrityError(f"manifest digest mismatch: {base}")
        try:
            value = json.loads(data)
        except json.JSONDecodeError as error:
            raise StoreIntegrityError(f"manifest is not valid JSON: {base}") from error
        if not isinstance(value, dict) or value.get("schema_version") != self.schema_version:
            raise StoreIntegrityError(f"manifest has an unsupported schema: {base}")
        records = value.get("records")
        if not isinstance(records, dict):
            raise StoreIntegrityError(f"manifest records are invalid: {base}")
        return value

    def _object(self, digest: str) -> dict[str, Any]:
        if not _OBJECT_ID.fullmatch(digest):
            raise StoreIntegrityError(f"invalid object id: {digest!r}")
        data = _read_bytes(self.objects / f"{digest}.json")
        if _object_id(data) != digest:
            raise StoreIntegrityError(f"object digest mismatch: {digest}")
        try:
            value = json.loads(data)
        except json.JSONDecodeError as error:
            raise StoreIntegrityError(f"object is not valid JSON: {digest}") from error
        if not isinstance(value, dict):
            raise StoreIntegrityError(f"object payload is invalid: {digest}")
        return value

    def base_revision(self) -> str:
        return self._base()

    def write(
        self,
        collection: str,
        record_id: str,
        payload: Mapping[str, Any],
        *,
        expected_base: str,
        ignore_for_idempotency: frozenset[str] = frozenset(),
    ) -> StoreWrite:
        if collection not in self.collections:
            raise ValueError(f"unsupported ledger collection: {collection}")
        record_id = _safe_record_id(record_id)
        if not _MANIFEST_ID.fullmatch(expected_base):
            raise UnsafeStorePathError(f"unsafe expected base: {expected_base!r}")
        envelope = {
            "collection": collection,
            "payload": payload,
            "record_id": record_id,
            "schema_version": self.schema_version,
        }
        object_data = _file_payload(envelope)
        digest = _object_id(object_data)

        with self._locked():
            current = self._base()
            manifest = self._manifest(current)
            records = manifest["records"]
            collection_records = records.get(collection, {})
            if not isinstance(collection_records, dict):
                raise StoreIntegrityError(f"invalid collection map: {collection}")
            existing_digest = collection_records.get(record_id)
            if existing_digest == digest:
                return StoreWrite(False, current, current, digest)
            if existing_digest is not None and ignore_for_idempotency:
                existing = self._object(existing_digest)
                existing_payload = existing.get("payload")
                if (
                    existing.get("schema_version") != self.schema_version
                    or existing.get("collection") != collection
                    or existing.get("record_id") != record_id
                    or not isinstance(existing_payload, dict)
                ):
                    raise StoreIntegrityError(f"record envelope mismatch: {record_id}")
                previous_identity = {
                    key: value
                    for key, value in existing_payload.items()
                    if key not in ignore_for_idempotency
                }
                proposed_identity = {
                    key: value
                    for key, value in payload.items()
                    if key not in ignore_for_idempotency
                }
                if canonical_json_bytes(previous_identity) == canonical_json_bytes(
                    proposed_identity
                ):
                    return StoreWrite(False, current, current, existing_digest)
            if current != expected_base:
                raise StoreConflictError(expected_base, current)

            object_path = self.objects / f"{digest}.json"
            if object_path.exists():
                if _read_bytes(object_path) != object_data:
                    raise StoreIntegrityError(f"object digest collision: {digest}")
            else:
                _atomic_write(object_path, object_data)

            next_records: dict[str, dict[str, str]] = {}
            for name, entries in records.items():
                if name not in self.collections or not isinstance(entries, dict):
                    raise StoreIntegrityError(f"invalid collection in manifest: {name}")
                next_records[name] = dict(entries)
            next_records.setdefault(collection, {})[record_id] = digest
            next_manifest = {
                "parent": current,
                "records": next_records,
                "schema_version": self.schema_version,
            }
            manifest_data = _file_payload(next_manifest)
            next_base = _manifest_id(manifest_data)
            manifest_path = self.manifests / f"{next_base}.json"
            if manifest_path.exists():
                if _read_bytes(manifest_path) != manifest_data:
                    raise StoreIntegrityError(f"manifest digest collision: {next_base}")
            else:
                _atomic_write(manifest_path, manifest_data)
            _atomic_write(self.head, _file_payload({"base": next_base}))
            return StoreWrite(True, next_base, current, digest)

    def read(self, collection: str, record_id: str) -> Mapping[str, Any] | None:
        if collection not in self.collections:
            raise ValueError(f"unsupported ledger collection: {collection}")
        record_id = _safe_record_id(record_id)
        base = self._base()
        manifest = self._manifest(base)
        digest = manifest["records"].get(collection, {}).get(record_id)
        if digest is None:
            return None
        envelope = self._object(digest)
        if (
            envelope.get("schema_version") != self.schema_version
            or envelope.get("collection") != collection
            or envelope.get("record_id") != record_id
            or not isinstance(envelope.get("payload"), dict)
        ):
            raise StoreIntegrityError(f"record envelope mismatch: {record_id}")
        return cast(Mapping[str, Any], envelope["payload"])

    def status(self) -> StoreStatus:
        base = self._base()
        records = self._manifest(base)["records"]
        counts = {
            collection: len(entries)
            for collection, entries in sorted(records.items())
            if entries
        }
        return StoreStatus(base, counts)

    def validate(self) -> IntegrityReport:
        errors: list[str] = []
        base: str | None = None
        counts: dict[str, int] = {}
        try:
            base = self._base()
            current: str | None = base
            seen_manifests: set[str] = set()
            seen_objects: set[str] = set()
            current_records: Mapping[str, Any] | None = None
            while current is not None:
                if current in seen_manifests:
                    raise StoreIntegrityError(f"manifest cycle detected: {current}")
                seen_manifests.add(current)
                manifest = self._manifest(current)
                if current_records is None:
                    current_records = manifest["records"]
                    counts = {
                        collection: len(entries)
                        for collection, entries in sorted(current_records.items())
                        if entries
                    }
                for collection, entries in manifest["records"].items():
                    if collection not in self.collections or not isinstance(entries, dict):
                        raise StoreIntegrityError(
                            f"invalid collection in manifest: {collection}"
                        )
                    for record_id, digest in entries.items():
                        _safe_record_id(record_id)
                        if digest not in seen_objects:
                            self._object(digest)
                            seen_objects.add(digest)
                parent = manifest.get("parent")
                if parent is not None and not isinstance(parent, str):
                    raise StoreIntegrityError(f"invalid manifest parent: {current}")
                current = parent
        except (OSError, StoreError, ValueError, TypeError) as error:
            errors.append(str(error))
        return IntegrityReport(not errors, base, counts, tuple(errors))


class FileContentStore:
    _collections = frozenset(
        {"articles", "events", "evidence", "revisions", "runs", "sources"}
    )

    def __init__(self, root: str | Path) -> None:
        self._ledger = _FileLedger(root, self._collections)

    @property
    def root(self) -> Path:
        return self._ledger.root

    def base_revision(self) -> str:
        return self._ledger.base_revision()

    def put_source(self, item: SourceItem, *, expected_base: str) -> StoreWrite:
        return self._ledger.write(
            "sources",
            item.item_id,
            model_to_dict(item),
            expected_base=expected_base,
            ignore_for_idempotency=frozenset({"fetched_at"}),
        )

    def get_source(self, item_id: str) -> SourceItem | None:
        value = self._ledger.read("sources", item_id)
        return SourceItem.from_dict(value) if value is not None else None

    def put_revision(self, revision: Revision, *, expected_base: str) -> StoreWrite:
        return self._ledger.write(
            "revisions",
            revision.revision_id,
            model_to_dict(revision),
            expected_base=expected_base,
            ignore_for_idempotency=frozenset({"observed_at"}),
        )

    def get_revision(self, revision_id: str) -> Revision | None:
        value = self._ledger.read("revisions", revision_id)
        return Revision.from_dict(value) if value is not None else None

    def put_event(self, event: Event, *, expected_base: str) -> StoreWrite:
        return self._ledger.write(
            "events", event.event_id, model_to_dict(event), expected_base=expected_base
        )

    def get_event(self, event_id: str) -> Event | None:
        value = self._ledger.read("events", event_id)
        return Event.from_dict(value) if value is not None else None

    def put_evidence(self, evidence: Evidence, *, expected_base: str) -> StoreWrite:
        return self._ledger.write(
            "evidence",
            evidence.evidence_id,
            model_to_dict(evidence),
            expected_base=expected_base,
            ignore_for_idempotency=frozenset({"captured_at"}),
        )

    def get_evidence(self, evidence_id: str) -> Evidence | None:
        value = self._ledger.read("evidence", evidence_id)
        return Evidence.from_dict(value) if value is not None else None

    def put_article(
        self, article: ArticleRevision, *, expected_base: str
    ) -> StoreWrite:
        return self._ledger.write(
            "articles",
            article.article_revision_id,
            model_to_dict(article),
            expected_base=expected_base,
            ignore_for_idempotency=frozenset({"created_at"}),
        )

    def get_article(self, article_revision_id: str) -> ArticleRevision | None:
        value = self._ledger.read("articles", article_revision_id)
        return ArticleRevision.from_dict(value) if value is not None else None

    def put_run(self, run: RunManifest, *, expected_base: str) -> StoreWrite:
        return self._ledger.write(
            "runs", run.run_id, model_to_dict(run), expected_base=expected_base
        )

    def get_run(self, run_id: str) -> RunManifest | None:
        value = self._ledger.read("runs", run_id)
        return RunManifest.from_dict(value) if value is not None else None

    def status(self) -> StoreStatus:
        return self._ledger.status()

    def validate(self) -> IntegrityReport:
        return self._ledger.validate()


class FileOpsStore:
    _collections = frozenset({"operations"})

    def __init__(self, root: str | Path) -> None:
        self._ledger = _FileLedger(root, self._collections)

    @property
    def root(self) -> Path:
        return self._ledger.root

    def base_revision(self) -> str:
        return self._ledger.base_revision()

    def put_operation(
        self, operation: OperationRecord, *, expected_base: str
    ) -> StoreWrite:
        return self._ledger.write(
            "operations",
            operation.operation_id,
            model_to_dict(operation),
            expected_base=expected_base,
        )

    def get_operation(self, operation_id: str) -> OperationRecord | None:
        value = self._ledger.read("operations", operation_id)
        return OperationRecord.from_dict(value) if value is not None else None

    def status(self) -> StoreStatus:
        return self._ledger.status()

    def validate(self) -> IntegrityReport:
        return self._ledger.validate()
