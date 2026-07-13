from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, cast

from ._json import freeze_json, json_ready, parse_datetime, sha256_digest
from .identity import (
    CANONICALIZATION_VERSION,
    canonicalize_url,
    make_article_revision_id,
    make_event_id,
    make_evidence_id,
    make_item_id,
    make_revision_id,
)


class WorkflowStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    GENERATED = "GENERATED"
    VALIDATED = "VALIDATED"
    PERSISTED = "PERSISTED"
    BUILT = "BUILT"
    DEPLOYED = "DEPLOYED"
    HEALTHY = "HEALTHY"
    NOTIFIED = "NOTIFIED"
    REJECTED = "REJECTED"
    QUARANTINED = "QUARANTINED"
    DEAD_LETTER = "DEAD_LETTER"
    UNKNOWN = "UNKNOWN"


class StepStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"
    QUARANTINED = "QUARANTINED"
    UNKNOWN = "UNKNOWN"


class EventStatus(str, Enum):
    ACTIVE = "ACTIVE"
    UPDATED = "UPDATED"
    MERGED = "MERGED"
    CORRECTED = "CORRECTED"
    STALE = "STALE"
    RETRACTED = "RETRACTED"


class OperationKind(str, Enum):
    BUDGET_RESERVATION = "BUDGET_RESERVATION"
    BUDGET_RECONCILIATION = "BUDGET_RECONCILIATION"
    OUTBOX = "OUTBOX"
    PUBLISH_RECEIPT = "PUBLISH_RECEIPT"
    RELEASE_SEQUENCE = "RELEASE_SEQUENCE"


class OperationStatus(str, Enum):
    PENDING = "PENDING"
    RESERVED = "RESERVED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"


def _utc(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC)


def _required(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _digest(value: str, field_name: str) -> str:
    if not value.startswith("sha256:") or len(value) != 71:
        raise ValueError(f"{field_name} must be a sha256 digest")
    try:
        int(value[7:], 16)
    except ValueError as error:
        raise ValueError(f"{field_name} must be a sha256 digest") from error
    return value.casefold()


def _tuple_strings(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(_required(value, "identifier") for value in values)


@dataclass(frozen=True, slots=True)
class SourceItem:
    source: str
    native_id: str | None
    canonical_url: str
    fetched_at: datetime
    payload: Mapping[str, Any]
    canonicalization_version: str = CANONICALIZATION_VERSION
    item_id: str = ""

    def __post_init__(self) -> None:
        source = _required(self.source, "source").casefold()
        native_id = self.native_id.strip() if self.native_id and self.native_id.strip() else None
        url = canonicalize_url(
            self.canonical_url, version=self.canonicalization_version
        )
        expected = make_item_id(
            source,
            native_id,
            url,
            canonicalization_version=self.canonicalization_version,
        )
        if self.item_id and self.item_id != expected:
            raise ValueError("item_id does not match the canonical source identity")
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "native_id", native_id)
        object.__setattr__(self, "canonical_url", url)
        object.__setattr__(self, "fetched_at", _utc(self.fetched_at, "fetched_at"))
        object.__setattr__(self, "payload", freeze_json(self.payload))
        object.__setattr__(self, "item_id", expected)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> SourceItem:
        return cls(
            source=value["source"],
            native_id=value.get("native_id"),
            canonical_url=value["canonical_url"],
            fetched_at=parse_datetime(value["fetched_at"]),
            payload=value["payload"],
            canonicalization_version=value["canonicalization_version"],
            item_id=value["item_id"],
        )


@dataclass(frozen=True, slots=True)
class Revision:
    item_id: str
    normalized_payload: Mapping[str, Any]
    source_snapshot_digest: str
    observed_at: datetime
    revision_id: str = ""
    content_digest: str = ""

    def __post_init__(self) -> None:
        item_id = _required(self.item_id, "item_id")
        payload = freeze_json(self.normalized_payload)
        expected_id = make_revision_id(item_id, payload)
        expected_digest = sha256_digest(payload)
        if self.revision_id and self.revision_id != expected_id:
            raise ValueError("revision_id does not match normalized payload")
        if self.content_digest and self.content_digest != expected_digest:
            raise ValueError("content_digest does not match normalized payload")
        object.__setattr__(self, "item_id", item_id)
        object.__setattr__(self, "normalized_payload", payload)
        object.__setattr__(
            self,
            "source_snapshot_digest",
            _digest(self.source_snapshot_digest, "source_snapshot_digest"),
        )
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        object.__setattr__(self, "revision_id", expected_id)
        object.__setattr__(self, "content_digest", expected_digest)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> Revision:
        return cls(
            item_id=value["item_id"],
            normalized_payload=value["normalized_payload"],
            source_snapshot_digest=value["source_snapshot_digest"],
            observed_at=parse_datetime(value["observed_at"]),
            revision_id=value["revision_id"],
            content_digest=value["content_digest"],
        )


@dataclass(frozen=True, slots=True)
class Event:
    seed_item_id: str
    member_item_ids: tuple[str, ...]
    first_seen: datetime
    last_seen: datetime
    status: EventStatus = EventStatus.ACTIVE
    alias_event_ids: tuple[str, ...] = ()
    event_id: str = ""

    def __post_init__(self) -> None:
        seed = _required(self.seed_item_id, "seed_item_id")
        members = _tuple_strings(self.member_item_ids)
        if seed not in members:
            raise ValueError("seed_item_id must be included in member_item_ids")
        first = _utc(self.first_seen, "first_seen")
        last = _utc(self.last_seen, "last_seen")
        if last < first:
            raise ValueError("last_seen must be greater than or equal to first_seen")
        expected = make_event_id(seed)
        if self.event_id and self.event_id != expected:
            raise ValueError("event_id does not match immutable event seed")
        object.__setattr__(self, "seed_item_id", seed)
        object.__setattr__(self, "member_item_ids", tuple(dict.fromkeys(members)))
        object.__setattr__(self, "alias_event_ids", _tuple_strings(self.alias_event_ids))
        object.__setattr__(self, "first_seen", first)
        object.__setattr__(self, "last_seen", last)
        object.__setattr__(self, "status", EventStatus(self.status))
        object.__setattr__(self, "event_id", expected)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> Event:
        return cls(
            seed_item_id=value["seed_item_id"],
            member_item_ids=tuple(value["member_item_ids"]),
            first_seen=parse_datetime(value["first_seen"]),
            last_seen=parse_datetime(value["last_seen"]),
            status=EventStatus(value["status"]),
            alias_event_ids=tuple(value.get("alias_event_ids", ())),
            event_id=value["event_id"],
        )


@dataclass(frozen=True, slots=True)
class Evidence:
    source_url: str
    snapshot_digest: str
    locator: str
    excerpt: str
    claim_ids: tuple[str, ...]
    captured_at: datetime
    evidence_id: str = ""

    def __post_init__(self) -> None:
        source_url = canonicalize_url(self.source_url)
        snapshot = _digest(self.snapshot_digest, "snapshot_digest")
        locator = _required(self.locator, "locator")
        excerpt = _required(self.excerpt, "excerpt")
        claims = _tuple_strings(self.claim_ids)
        if not claims:
            raise ValueError("claim_ids must not be empty")
        expected = make_evidence_id(source_url, snapshot, locator, excerpt)
        if self.evidence_id and self.evidence_id != expected:
            raise ValueError("evidence_id does not match evidence payload")
        object.__setattr__(self, "source_url", source_url)
        object.__setattr__(self, "snapshot_digest", snapshot)
        object.__setattr__(self, "locator", locator)
        object.__setattr__(self, "excerpt", excerpt)
        object.__setattr__(self, "claim_ids", claims)
        object.__setattr__(self, "captured_at", _utc(self.captured_at, "captured_at"))
        object.__setattr__(self, "evidence_id", expected)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> Evidence:
        return cls(
            source_url=value["source_url"],
            snapshot_digest=value["snapshot_digest"],
            locator=value["locator"],
            excerpt=value["excerpt"],
            claim_ids=tuple(value["claim_ids"]),
            captured_at=parse_datetime(value["captured_at"]),
            evidence_id=value["evidence_id"],
        )


@dataclass(frozen=True, slots=True)
class ArticleRevision:
    event_id: str
    generation_key: str
    title: str
    body: str
    created_at: datetime
    claims: tuple[Mapping[str, Any], ...] = ()
    inferences: tuple[Mapping[str, Any], ...] = ()
    evidence_ids: tuple[str, ...] = ()
    source_support: float = 0.0
    tags: tuple[str, ...] = ()
    entity_ids: tuple[str, ...] = ()
    article_revision_id: str = ""

    def __post_init__(self) -> None:
        event_id = _required(self.event_id, "event_id")
        generation_key = _required(self.generation_key, "generation_key")
        title = _required(self.title, "title")
        body = _required(self.body, "body")
        if not 0.0 <= self.source_support <= 1.0:
            raise ValueError("source_support must be between 0 and 1")
        claims = tuple(freeze_json(claim) for claim in self.claims)
        inferences = tuple(freeze_json(item) for item in self.inferences)
        object.__setattr__(self, "event_id", event_id)
        object.__setattr__(self, "generation_key", generation_key)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "body", body)
        object.__setattr__(self, "created_at", _utc(self.created_at, "created_at"))
        object.__setattr__(self, "claims", claims)
        object.__setattr__(self, "inferences", inferences)
        object.__setattr__(self, "evidence_ids", _tuple_strings(self.evidence_ids))
        object.__setattr__(self, "tags", _tuple_strings(self.tags))
        object.__setattr__(self, "entity_ids", _tuple_strings(self.entity_ids))
        expected = make_article_revision_id(generation_key, self.generated_payload)
        if self.article_revision_id and self.article_revision_id != expected:
            raise ValueError("article_revision_id does not match generated payload")
        object.__setattr__(self, "article_revision_id", expected)

    @property
    def generated_payload(self) -> Mapping[str, Any]:
        return cast(
            Mapping[str, Any],
            freeze_json(
                {
                    "body": self.body,
                    "claims": self.claims,
                    "entity_ids": self.entity_ids,
                    "evidence_ids": self.evidence_ids,
                    "inferences": self.inferences,
                    "source_support": self.source_support,
                    "tags": self.tags,
                    "title": self.title,
                }
            ),
        )

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> ArticleRevision:
        return cls(
            event_id=value["event_id"],
            generation_key=value["generation_key"],
            title=value["title"],
            body=value["body"],
            created_at=parse_datetime(value["created_at"]),
            claims=tuple(value.get("claims", ())),
            inferences=tuple(value.get("inferences", ())),
            evidence_ids=tuple(value.get("evidence_ids", ())),
            source_support=float(value.get("source_support", 0.0)),
            tags=tuple(value.get("tags", ())),
            entity_ids=tuple(value.get("entity_ids", ())),
            article_revision_id=value["article_revision_id"],
        )


@dataclass(frozen=True, slots=True)
class StepResult:
    step: str
    status: StepStatus
    started_at: datetime
    finished_at: datetime | None = None
    output_digest: str | None = None
    error_code: str | None = None
    error_message: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        started = _utc(self.started_at, "started_at")
        finished = _utc(self.finished_at, "finished_at") if self.finished_at else None
        if finished is not None and finished < started:
            raise ValueError("finished_at must be greater than or equal to started_at")
        if self.output_digest is not None:
            _digest(self.output_digest, "output_digest")
        object.__setattr__(self, "step", _required(self.step, "step"))
        object.__setattr__(self, "status", StepStatus(self.status))
        object.__setattr__(self, "started_at", started)
        object.__setattr__(self, "finished_at", finished)
        object.__setattr__(self, "metadata", freeze_json(self.metadata))

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> StepResult:
        return cls(
            step=value["step"],
            status=StepStatus(value["status"]),
            started_at=parse_datetime(value["started_at"]),
            finished_at=(
                parse_datetime(value["finished_at"]) if value.get("finished_at") else None
            ),
            output_digest=value.get("output_digest"),
            error_code=value.get("error_code"),
            error_message=value.get("error_message"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True, slots=True)
class RunManifest:
    run_id: str
    code_sha: str
    content_parent_sha: str
    input_digest: str
    config_digest: str
    model: str
    status: WorkflowStatus
    created_at: datetime
    updated_at: datetime
    steps: tuple[StepResult, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        created = _utc(self.created_at, "created_at")
        updated = _utc(self.updated_at, "updated_at")
        if updated < created:
            raise ValueError("updated_at must be greater than or equal to created_at")
        object.__setattr__(self, "run_id", _required(self.run_id, "run_id"))
        object.__setattr__(self, "code_sha", _required(self.code_sha, "code_sha"))
        object.__setattr__(
            self, "content_parent_sha", _required(self.content_parent_sha, "content_parent_sha")
        )
        object.__setattr__(self, "input_digest", _digest(self.input_digest, "input_digest"))
        object.__setattr__(self, "config_digest", _digest(self.config_digest, "config_digest"))
        object.__setattr__(self, "model", _required(self.model, "model"))
        object.__setattr__(self, "status", WorkflowStatus(self.status))
        object.__setattr__(self, "created_at", created)
        object.__setattr__(self, "updated_at", updated)
        object.__setattr__(self, "steps", tuple(self.steps))
        object.__setattr__(self, "metadata", freeze_json(self.metadata))

    def next_incomplete_step(self, ordered_steps: Sequence[str]) -> str | None:
        completed = {
            step.step
            for step in self.steps
            if step.status in {StepStatus.SUCCEEDED, StepStatus.SKIPPED}
        }
        return next((step for step in ordered_steps if step not in completed), None)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> RunManifest:
        return cls(
            run_id=value["run_id"],
            code_sha=value["code_sha"],
            content_parent_sha=value["content_parent_sha"],
            input_digest=value["input_digest"],
            config_digest=value["config_digest"],
            model=value["model"],
            status=WorkflowStatus(value["status"]),
            created_at=parse_datetime(value["created_at"]),
            updated_at=parse_datetime(value["updated_at"]),
            steps=tuple(StepResult.from_dict(step) for step in value.get("steps", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True, slots=True)
class OperationRecord:
    operation_id: str
    kind: OperationKind
    status: OperationStatus
    idempotency_key: str
    created_at: datetime
    updated_at: datetime
    token_limit: int = 0
    token_used: int = 0
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        created = _utc(self.created_at, "created_at")
        updated = _utc(self.updated_at, "updated_at")
        if updated < created:
            raise ValueError("updated_at must be greater than or equal to created_at")
        if self.token_limit < 0 or self.token_used < 0:
            raise ValueError("token counts must not be negative")
        if self.token_limit and self.token_used > self.token_limit:
            raise ValueError("token_used must not exceed token_limit")
        object.__setattr__(self, "operation_id", _required(self.operation_id, "operation_id"))
        object.__setattr__(
            self, "idempotency_key", _required(self.idempotency_key, "idempotency_key")
        )
        object.__setattr__(self, "kind", OperationKind(self.kind))
        object.__setattr__(self, "status", OperationStatus(self.status))
        object.__setattr__(self, "created_at", created)
        object.__setattr__(self, "updated_at", updated)
        object.__setattr__(self, "metadata", freeze_json(self.metadata))

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> OperationRecord:
        return cls(
            operation_id=value["operation_id"],
            kind=OperationKind(value["kind"]),
            status=OperationStatus(value["status"]),
            idempotency_key=value["idempotency_key"],
            created_at=parse_datetime(value["created_at"]),
            updated_at=parse_datetime(value["updated_at"]),
            token_limit=int(value.get("token_limit", 0)),
            token_used=int(value.get("token_used", 0)),
            metadata=value.get("metadata", {}),
        )


def model_to_dict(model: Any) -> dict[str, Any]:
    result = json_ready(model)
    if not isinstance(result, dict):
        raise TypeError("domain model must serialize to an object")
    return result
