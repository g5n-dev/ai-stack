"""At-least-once publisher outbox with explicit unknown outcomes."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass, replace
from threading import Lock


@dataclass(frozen=True)
class PublishResult:
    status: str
    provider_message_id: str | None = None
    detail: str = ""
    retryable: bool = False

    def __post_init__(self) -> None:
        if self.status not in {"sent", "unknown", "failed"}:
            raise ValueError(f"invalid publish result status: {self.status}")
        if self.status == "sent" and not self.provider_message_id:
            raise ValueError("sent result requires provider_message_id")
        if self.status != "sent" and self.provider_message_id is not None:
            raise ValueError("only sent results may contain provider_message_id")
        if self.status != "failed" and self.retryable:
            raise ValueError("only failed results may be retryable")

    @classmethod
    def sent(cls, provider_message_id: str) -> PublishResult:
        return cls(status="sent", provider_message_id=provider_message_id)

    @classmethod
    def unknown(cls, detail: str) -> PublishResult:
        return cls(status="unknown", detail=detail)

    @classmethod
    def failed(cls, detail: str, *, retryable: bool) -> PublishResult:
        return cls(status="failed", detail=detail, retryable=retryable)


@dataclass
class OutboxRecord:
    idempotency_key: str
    event_revision: str
    platform: str
    template_version: str
    payload: str
    status: str = "pending"
    attempts: int = 0
    provider_message_id: str | None = None
    detail: str = ""
    retryable: bool = False


class InMemoryOutboxStore:
    def __init__(self) -> None:
        self._values: dict[str, OutboxRecord] = {}
        self._lock = Lock()

    def put_if_absent(self, record: OutboxRecord) -> OutboxRecord:
        with self._lock:
            existing = self._values.get(record.idempotency_key)
            if existing is not None:
                comparable = (
                    existing.event_revision,
                    existing.platform,
                    existing.template_version,
                    existing.payload,
                )
                incoming = (
                    record.event_revision,
                    record.platform,
                    record.template_version,
                    record.payload,
                )
                if comparable != incoming:
                    raise ValueError("idempotency key collision with different payload")
                return replace(existing)
            self._values[record.idempotency_key] = replace(record)
            return replace(record)

    def get(self, key: str) -> OutboxRecord:
        with self._lock:
            return replace(self._values[key])

    def save(self, record: OutboxRecord) -> None:
        with self._lock:
            if record.idempotency_key not in self._values:
                raise KeyError(record.idempotency_key)
            self._values[record.idempotency_key] = replace(record)

    def records(self) -> tuple[OutboxRecord, ...]:
        with self._lock:
            return tuple(replace(value) for value in self._values.values())


class OutboxDispatcher:
    def __init__(
        self,
        *,
        store: InMemoryOutboxStore,
        sender: Callable[[str, str], PublishResult],
        max_attempts: int = 5,
    ) -> None:
        self.store = store
        self.sender = sender
        self.max_attempts = max_attempts

    @staticmethod
    def make_key(event_revision: str, platform: str, template_version: str) -> str:
        raw = f"{event_revision}\x1f{platform}\x1f{template_version}".encode()
        return hashlib.sha256(raw).hexdigest()

    def enqueue(
        self,
        event_revision: str,
        platform: str,
        template_version: str,
        payload: str,
    ) -> str:
        key = self.make_key(event_revision, platform, template_version)
        self.store.put_if_absent(
            OutboxRecord(
                idempotency_key=key,
                event_revision=event_revision,
                platform=platform,
                template_version=template_version,
                payload=payload,
            )
        )
        return key

    def dispatch(self, key: str) -> OutboxRecord:
        record = self.store.get(key)
        if record.status in {"sent", "unknown", "dead_letter"}:
            return record
        if record.status == "failed" and not record.retryable:
            record.status = "dead_letter"
            self.store.save(record)
            return record
        if record.attempts >= self.max_attempts:
            record.status = "dead_letter"
            self.store.save(record)
            return record

        record.attempts += 1
        record.status = "in_flight"
        self.store.save(record)
        try:
            result = self.sender(record.payload, record.idempotency_key)
        except Exception as exc:
            result = PublishResult.unknown(type(exc).__name__)
        record.status = result.status
        record.provider_message_id = result.provider_message_id
        record.detail = result.detail
        record.retryable = result.retryable
        self.store.save(record)
        return self.store.get(key)
