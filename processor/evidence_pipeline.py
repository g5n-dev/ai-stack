"""Deterministic evidence gates for automatically published content.

The gate intentionally proves only that a generated claim is supported by a
saved source snapshot.  It does not claim that the source itself is true.
"""

from __future__ import annotations

import hmac
import html
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from urllib.parse import urlsplit


class PublicationTier(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    QUARANTINED = "QUARANTINED"


@dataclass(frozen=True)
class GateDecision:
    publishable: bool
    tier: PublicationTier
    coverage: float
    supported_claims: int
    factual_claims: int
    reasons: tuple[str, ...]


def _normalized_text(value: object) -> str:
    text = html.unescape(str(value or ""))
    return re.sub(r"\s+", " ", text).strip().casefold()


class EvidenceGate:
    """Fail-closed publication gate for generated article payloads."""

    _MANDATORY_KINDS = frozenset({"numeric", "direct_quote", "security"})
    _FACTUAL_KINDS = frozenset({"fact", "numeric", "direct_quote", "security", "source_claim"})
    _HIGH_RISK_DOMAINS = frozenset({"medical", "legal", "financial"})

    def __init__(
        self,
        minimum_coverage: float = 0.9,
        long_body_threshold: int = 200,
        maximum_evidence_bytes: int = 500,
    ):
        if not 0 < minimum_coverage <= 1:
            raise ValueError("minimum_coverage must be in (0, 1]")
        if long_body_threshold <= 0 or maximum_evidence_bytes <= 0:
            raise ValueError("evidence gate limits must be positive")
        self.minimum_coverage = minimum_coverage
        self.long_body_threshold = long_body_threshold
        self.maximum_evidence_bytes = maximum_evidence_bytes

    def evaluate(
        self,
        article: Mapping[str, object],
        snapshots: Mapping[str, object],
    ) -> GateDecision:
        reasons: list[str] = []
        risk_domain = str(article.get("risk_domain") or "").strip().casefold()
        if risk_domain in self._HIGH_RISK_DOMAINS:
            reasons.append(f"high_risk_domain:{risk_domain}")
        if bool(article.get("contradictory_evidence")):
            reasons.append("contradictory_evidence")

        evidence_by_id: dict[str, Mapping[str, object]] = {}
        valid_evidence: set[str] = set()
        evidence_items = article.get("evidence")
        if isinstance(evidence_items, Sequence) and not isinstance(evidence_items, (str, bytes)):
            for raw in evidence_items:
                if not isinstance(raw, Mapping):
                    reasons.append("invalid_evidence_record")
                    continue
                evidence_id = str(raw.get("id") or "").strip()
                snapshot_id = str(raw.get("snapshot_id") or "").strip()
                if not evidence_id or evidence_id in evidence_by_id:
                    reasons.append("invalid_or_duplicate_evidence_id")
                    continue
                evidence_by_id[evidence_id] = raw

                source_url = str(raw.get("url") or "").strip()
                parsed_url = urlsplit(source_url)
                if parsed_url.scheme not in {"http", "https"} or not parsed_url.hostname:
                    reasons.append(f"invalid_evidence_url:{evidence_id}")
                    continue

                snapshot_value = snapshots.get(snapshot_id, "")
                if isinstance(snapshot_value, Mapping):
                    snapshot_text = str(snapshot_value.get("content") or "")
                else:
                    snapshot_text = str(snapshot_value or "")
                snapshot_bytes = snapshot_text.encode("utf-8")
                expected_snapshot_hash = str(raw.get("snapshot_sha256") or "").casefold()
                actual_snapshot_hash = sha256(snapshot_bytes).hexdigest()
                if not hmac.compare_digest(actual_snapshot_hash, expected_snapshot_hash):
                    reasons.append(f"snapshot_hash_mismatch:{evidence_id}")
                    continue

                snippet_text = str(raw.get("snippet") or "")
                snippet_bytes = snippet_text.encode("utf-8")
                start = raw.get("start_byte")
                end = raw.get("end_byte")
                valid_offsets = (
                    isinstance(start, int)
                    and not isinstance(start, bool)
                    and isinstance(end, int)
                    and not isinstance(end, bool)
                    and 0 <= start < end <= len(snapshot_bytes)
                )
                if (
                    not snippet_bytes
                    or len(snippet_bytes) > self.maximum_evidence_bytes
                    or not valid_offsets
                    or snapshot_bytes[start:end] != snippet_bytes
                ):
                    reasons.append(f"unlocatable_evidence:{evidence_id}")
                    continue
                valid_evidence.add(evidence_id)

        claims_raw = article.get("claims")
        claims: list[Mapping[str, object]] = []
        if isinstance(claims_raw, Sequence) and not isinstance(claims_raw, (str, bytes)):
            claims = [claim for claim in claims_raw if isinstance(claim, Mapping)]
            if len(claims) != len(claims_raw):
                reasons.append("invalid_claim_record")

        factual_claims = [
            claim
            for claim in claims
            if str(claim.get("kind") or "fact").strip().casefold() in self._FACTUAL_KINDS
        ]
        inference_claims = [
            claim
            for claim in claims
            if str(claim.get("kind") or "").strip().casefold() == "inference"
        ]
        body = str(article.get("body") or "")
        mode = str(article.get("content_mode") or "article").strip().casefold()

        if len(body) > self.long_body_threshold and not factual_claims:
            reasons.append("no_factual_claims")

        supported = 0
        seen_claim_ids: set[str] = set()
        for claim in factual_claims:
            claim_id = str(claim.get("id") or "").strip()
            kind = str(claim.get("kind") or "fact").strip().casefold()
            if not claim_id or claim_id in seen_claim_ids:
                reasons.append("invalid_or_duplicate_claim_id")
                continue
            seen_claim_ids.add(claim_id)
            raw_refs = claim.get("evidence_ids")
            refs = (
                [str(ref).strip() for ref in raw_refs if str(ref).strip()]
                if isinstance(raw_refs, Sequence) and not isinstance(raw_refs, (str, bytes))
                else []
            )
            is_supported = bool(refs) and all(ref in valid_evidence for ref in refs)
            if is_supported:
                supported += 1
            elif kind in self._MANDATORY_KINDS:
                reasons.append(f"mandatory_claim_unsupported:{claim_id}")

        for claim in inference_claims:
            claim_id = str(claim.get("id") or "").strip()
            raw_refs = claim.get("evidence_ids")
            refs = (
                [str(ref).strip() for ref in raw_refs if str(ref).strip()]
                if isinstance(raw_refs, Sequence) and not isinstance(raw_refs, (str, bytes))
                else []
            )
            if not refs or not all(ref in valid_evidence for ref in refs):
                reasons.append(f"inference_without_supported_premise:{claim_id or 'unknown'}")

        denominator = len(factual_claims)
        coverage = supported / denominator if denominator else 0.0
        if denominator and coverage < self.minimum_coverage:
            reasons.append("insufficient_evidence_coverage")

        brief_allowed = (
            mode == "source_brief"
            and len(body) <= self.long_body_threshold
            and bool(valid_evidence)
            and not factual_claims
            and not inference_claims
        )
        fatal = bool(reasons)
        if brief_allowed and not fatal:
            return GateDecision(True, PublicationTier.C, 1.0, 0, 0, ())
        if fatal or not denominator:
            return GateDecision(
                False,
                PublicationTier.QUARANTINED,
                coverage,
                supported,
                denominator,
                tuple(dict.fromkeys(reasons or ["no_publishable_claims"])),
            )

        tier = PublicationTier.B if inference_claims or coverage < 1 else PublicationTier.A
        return GateDecision(True, tier, coverage, supported, denominator, ())
