"""Budgeted, cache-aware gateway for all model calls."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from threading import Lock
from typing import Protocol
from uuid import uuid4


class BudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class BudgetPolicy:
    max_calls_per_item: int = 4
    max_calls_per_run: int = 20
    max_calls_per_day: int = 240
    max_tokens_per_item: int = 40_000
    max_tokens_per_run: int = 200_000
    max_tokens_per_day: int = 2_000_000


@dataclass
class BudgetReservation:
    reservation_id: str
    run_id: str
    item_id: str
    reserved_tokens: int
    created_at: datetime
    status: str = "reserved"
    actual_tokens: int | None = None
    cache_key: str = ""


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cache_hit: bool = False


class Provider(Protocol):
    def generate(self, *, purpose: str, payload: str, max_tokens: int) -> ProviderResponse: ...


class ResponseCache(Protocol):
    def get(self, key: str) -> ProviderResponse | None: ...

    def put(self, key: str, response: ProviderResponse) -> None: ...


class InMemoryResponseCache:
    def __init__(self) -> None:
        self._values: dict[str, ProviderResponse] = {}
        self._lock = Lock()

    def get(self, key: str) -> ProviderResponse | None:
        with self._lock:
            return self._values.get(key)

    def put(self, key: str, response: ProviderResponse) -> None:
        with self._lock:
            self._values.setdefault(key, replace(response, cache_hit=False))


class InMemoryBudgetStore:
    """Reference CAS boundary used by tests and local dry-runs.

    Production adapters persist the same reservation before exposing model
    credentials to the generation job.
    """

    def __init__(self) -> None:
        self._items: list[BudgetReservation] = []
        self._lock = Lock()

    def reserve(
        self,
        *,
        run_id: str,
        item_id: str,
        reserved_tokens: int,
        cache_key: str,
        policy: BudgetPolicy,
        now: datetime,
    ) -> BudgetReservation:
        with self._lock:
            day = now.astimezone(UTC).date()
            daily = [item for item in self._items if item.created_at.astimezone(UTC).date() == day]
            run_items = [item for item in self._items if item.run_id == run_id]
            item_items = [item for item in self._items if item.item_id == item_id]
            limits = (
                (len(item_items) + 1, policy.max_calls_per_item, "item call"),
                (len(run_items) + 1, policy.max_calls_per_run, "run call"),
                (len(daily) + 1, policy.max_calls_per_day, "daily call"),
                (
                    sum(item.reserved_tokens for item in item_items)
                    + reserved_tokens,
                    policy.max_tokens_per_item,
                    "item token",
                ),
                (
                    sum(item.reserved_tokens for item in run_items)
                    + reserved_tokens,
                    policy.max_tokens_per_run,
                    "run token",
                ),
                (
                    sum(item.reserved_tokens for item in daily) + reserved_tokens,
                    policy.max_tokens_per_day,
                    "daily token",
                ),
            )
            for actual, maximum, label in limits:
                if actual > maximum:
                    raise BudgetExceeded(f"{label} budget exceeded: {actual}>{maximum}")
            reservation = BudgetReservation(
                reservation_id=f"budget-{uuid4().hex}",
                run_id=run_id,
                item_id=item_id,
                reserved_tokens=reserved_tokens,
                created_at=now,
                cache_key=cache_key,
            )
            self._items.append(reservation)
            return reservation

    def reconcile(self, reservation_id: str, actual_tokens: int) -> None:
        with self._lock:
            item = self._find(reservation_id)
            item.status = "reconciled"
            item.actual_tokens = actual_tokens

    def mark_unknown(self, reservation_id: str) -> None:
        with self._lock:
            self._find(reservation_id).status = "unknown"

    def _find(self, reservation_id: str) -> BudgetReservation:
        for item in self._items:
            if item.reservation_id == reservation_id:
                return item
        raise KeyError(reservation_id)

    def reservations(self) -> tuple[BudgetReservation, ...]:
        with self._lock:
            return tuple(replace(item) for item in self._items)


class LLMGateway:
    def __init__(
        self,
        *,
        provider: Provider,
        budget_store: InMemoryBudgetStore,
        cache: ResponseCache,
        policy: BudgetPolicy | None = None,
    ) -> None:
        self.provider = provider
        self.budget_store = budget_store
        self.cache = cache
        self.policy = policy or BudgetPolicy()

    @staticmethod
    def cache_key(
        *,
        purpose: str,
        payload: str,
        model: str,
        prompt_version: str,
        policy_version: str,
    ) -> str:
        encoded = json.dumps(
            {
                "model": model,
                "payload": payload,
                "policy_version": policy_version,
                "prompt_version": prompt_version,
                "purpose": purpose,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def generate(
        self,
        *,
        run_id: str,
        item_id: str,
        purpose: str,
        payload: str,
        model: str,
        prompt_version: str,
        policy_version: str,
        max_tokens: int,
    ) -> ProviderResponse:
        key = self.cache_key(
            purpose=purpose,
            payload=payload,
            model=model,
            prompt_version=prompt_version,
            policy_version=policy_version,
        )
        cached = self.cache.get(key)
        if cached is not None:
            return replace(cached, cache_hit=True)

        estimated_input_tokens = max(1, (len(payload) + 3) // 4)
        reservation = self.budget_store.reserve(
            run_id=run_id,
            item_id=item_id,
            reserved_tokens=estimated_input_tokens + max_tokens,
            cache_key=key,
            policy=self.policy,
            now=datetime.now(UTC),
        )
        try:
            response = self.provider.generate(
                purpose=purpose,
                payload=payload,
                max_tokens=max_tokens,
            )
        except Exception:
            self.budget_store.mark_unknown(reservation.reservation_id)
            raise
        self.budget_store.reconcile(
            reservation.reservation_id,
            response.input_tokens + response.output_tokens,
        )
        self.cache.put(key, response)
        return response
