"""Deterministic, evidence-only intelligence lineage primitives and assets.

The module deliberately fingerprints the bounded source excerpt captured by the
source contract.  It never fingerprints generated article prose and never writes
source text to either the internal registry or public lineage assets.
"""

from __future__ import annotations

import hashlib
import html
import json
import math
import os
import re
import unicodedata
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from difflib import SequenceMatcher
from enum import StrEnum
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml

from ._json import canonical_json_bytes, sha256_hex
from .identity import canonicalize_url

LINEAGE_SCHEMA = "lineage_index_v1"
LINEAGE_VERSION = 1
BUCKET_ALGORITHM = "sha256_prefix32_mod_v1"
DEFAULT_CONFIG_PATH = Path("config/lineage.yaml")

_URL_PATTERN = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
_EMBEDDED_HTTP_URL_PATTERN = re.compile(r"https?://[^\s<>\])]+", re.IGNORECASE)
_MARKDOWN_LINK_PATTERN = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
_NON_TEXT_PATTERN = re.compile(r"[^\w\u3400-\u9fff]+", re.UNICODE)
_CHINESE_SEQUENCE_PATTERN = re.compile(r"[\u3400-\u9fff]+")
_ENGLISH_TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:[.+#_-][a-z0-9]+)*")
_SECRET_PATTERNS = (
    re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(rb"\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]", re.I),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
_SENSITIVE_QUERY_TOKENS = frozenset(
    {
        "auth",
        "authorization",
        "code",
        "credential",
        "jwt",
        "key",
        "password",
        "secret",
        "session",
        "sig",
        "signature",
        "sk",
        "token",
    }
)
_SENSITIVE_QUERY_COMPOUNDS = frozenset(
    {
        "accesstoken",
        "apikey",
        "authtoken",
        "awsaccesskeyid",
        "jwttoken",
        "sessionid",
        "signedurl",
    }
)
_PERSISTED_FINGERPRINT_FIELDS = frozenset(
    {
        "bitmap",
        "kmv",
        "normalized_chars",
        "normalized_digest",
        "shingle_count",
        "simhash",
    }
)
_DEFAULT_BOILERPLATE_PATTERNS = (
    re.compile(r"^(?:home|about|rss|menu|navigation)(?:\s*/\s*(?:home|about|rss|menu))*$", re.I),
    re.compile(r"^(?:免责声明|版权声明|责任编辑|本文仅代表作者观点|点击查看原文)"),
    re.compile(r"^(?:copyright|all rights reserved|read the original|share this article)\b", re.I),
    re.compile(r"^(?:公开展示已截断|当前只保存了|请访问原始来源|本页只呈现已做哈希绑定)"),
)
_TITLE_STOPWORDS = {
    "about",
    "after",
    "from",
    "into",
    "model",
    "news",
    "release",
    "releases",
    "the",
    "this",
    "using",
    "with",
    "发布",
    "模型",
    "正式",
}


class LineageValidationError(ValueError):
    """Raised when lineage input or generated assets violate the contract."""


class RelationKind(StrEnum):
    ORIGINAL = "original"
    EXACT_COPY = "exact_copy"
    SYNDICATED = "syndicated"
    DERIVATIVE = "derivative"
    SAME_EVENT = "same_event"
    RELATED_ONLY = "related_only"


class TimestampConfidence(StrEnum):
    PUBLISHER = "publisher"
    FEED = "feed"
    PLATFORM = "platform"
    GIT = "git"
    OBSERVED = "observed"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class LineageConfig:
    shard_count: int = 128
    max_source_chars: int = 24 * 1024
    max_shingles: int = 4096
    kmv_size: int = 256
    max_candidates: int = 50
    exact_min_chars: int = 160
    exact_min_shingles: int = 48
    syndicated_min_chars: int = 300
    syndicated_min_shingles: int = 80
    syndicated_jaccard: float = 0.92
    syndicated_containment: float = 0.96
    syndicated_confidence: float = 0.98
    derivative_jaccard: float = 0.35
    derivative_containment: float = 0.72
    derivative_common_shingles: int = 80
    same_event_hours: int = 72
    same_event_title_similarity: float = 0.85
    same_event_shared_signals: int = 2
    suppression_absolute_limit: int = 10
    suppression_ratio_limit: float = 0.35
    suppression_ratio_min_count: int = 4
    index_max_bytes: int = 64 * 1024
    shard_max_bytes: int = 64 * 1024
    public_max_bytes: int = 3 * 1024 * 1024
    public_max_files: int = 300
    boilerplate_patterns: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.shard_count <= 0 or self.shard_count > 256:
            raise ValueError("shard_count must be between 1 and 256")
        for name in (
            "max_source_chars",
            "max_shingles",
            "kmv_size",
            "max_candidates",
            "exact_min_chars",
            "exact_min_shingles",
            "syndicated_min_chars",
            "syndicated_min_shingles",
            "derivative_common_shingles",
            "same_event_hours",
            "same_event_shared_signals",
            "suppression_ratio_min_count",
            "index_max_bytes",
            "shard_max_bytes",
            "public_max_bytes",
            "public_max_files",
        ):
            if int(getattr(self, name)) <= 0:
                raise ValueError(f"{name} must be positive")
        for name in (
            "syndicated_jaccard",
            "syndicated_containment",
            "syndicated_confidence",
            "derivative_jaccard",
            "derivative_containment",
            "same_event_title_similarity",
            "suppression_ratio_limit",
        ):
            value = float(getattr(self, name))
            if not 0 < value <= 1:
                raise ValueError(f"{name} must be in (0, 1]")
        if self.suppression_absolute_limit < 0:
            raise ValueError("suppression_absolute_limit must not be negative")


@dataclass(frozen=True)
class Fingerprint:
    normalized_digest: str
    normalized_chars: int
    shingle_count: int
    bitmap_hex: str
    simhash_hex: str
    kmv: tuple[int, ...] = field(repr=False)
    shingle_hashes: frozenset[int] = field(repr=False)


@dataclass(frozen=True)
class ObservationInput:
    canonical_url: str
    title: str
    source_text: str
    source: str
    article_path: str
    capture_mode: str = "full_text"
    source_completeness: str = "complete"
    source_is_truncated: bool = False
    source_published_at: str | None = None
    first_seen_at: str | None = None
    last_seen_at: str | None = None
    timestamp_confidence: TimestampConfidence = TimestampConfidence.UNKNOWN
    active: bool = True
    article_url: str | None = None
    source_payload_sha256: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "canonical_url", _safe_source_url(self.canonical_url))
        title = " ".join(str(self.title).split()).strip()
        if not title:
            raise ValueError("title must not be empty")
        object.__setattr__(self, "title", title[:500])
        try:
            confidence = TimestampConfidence(str(self.timestamp_confidence))
        except ValueError as exc:
            raise ValueError("invalid timestamp_confidence") from exc
        object.__setattr__(self, "timestamp_confidence", confidence)
        for name in ("source_published_at", "first_seen_at", "last_seen_at"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _canonical_timestamp(value))

    @property
    def observation_id(self) -> str:
        return make_observation_id(self.canonical_url)

    @property
    def fingerprint(self) -> Fingerprint:
        return fingerprint_text(self.source_text)


@dataclass(frozen=True)
class RelationshipDecision:
    relation: RelationKind
    confidence: float
    jaccard: float
    left_containment: float
    right_containment: float
    common_shingles: int
    shared_signals: int
    parent_observation_id: str | None
    suppression_eligible: bool
    reason: str


@dataclass(frozen=True)
class CircuitBreakerResult:
    decisions: tuple[RelationshipDecision, ...]
    tripped: bool
    reason: str | None
    suppression_count: int


@dataclass(frozen=True)
class ResolutionItem:
    observation_id: str
    revision_id: str
    event_id: str
    relation: RelationKind
    parent_observation_id: str | None
    suppress: bool
    confidence: float


@dataclass(frozen=True)
class BatchResolution:
    items: tuple[ResolutionItem, ...]
    circuit_breaker: CircuitBreakerResult
    stats: Mapping[str, int]


class _EvidenceHTMLParser(HTMLParser):
    _SKIP_TAGS = {"script", "style", "nav", "header", "footer", "aside", "form"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag.casefold() in self._SKIP_TAGS:
            self._skip_depth += 1
        elif not self._skip_depth and tag.casefold() in {"br", "p", "div", "li", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        folded = tag.casefold()
        if folded in self._SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
        elif not self._skip_depth and folded in {"p", "div", "li", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self.parts.append(data)


def load_lineage_config(path: Path = DEFAULT_CONFIG_PATH) -> LineageConfig:
    if not path.exists():
        return LineageConfig()
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return LineageConfig()
    if not isinstance(raw, Mapping):
        raise LineageValidationError("lineage config must be a mapping")
    version = raw.get("version")
    if version != 1:
        raise LineageValidationError("lineage config version must be 1")
    allowed = {field_.name for field_ in LineageConfig.__dataclass_fields__.values()}
    values = {str(key): value for key, value in raw.items() if key != "version"}
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise LineageValidationError(f"unknown lineage config keys: {', '.join(unknown)}")
    patterns = values.get("boilerplate_patterns")
    if isinstance(patterns, list):
        values["boilerplate_patterns"] = tuple(str(item) for item in patterns)
    try:
        return LineageConfig(**values)
    except (TypeError, ValueError) as exc:
        raise LineageValidationError(f"invalid lineage config: {exc}") from exc


def make_observation_id(url: str) -> str:
    canonical_url = _safe_source_url(url)
    return "obs_" + hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()


def make_lineage_revision_id(observation_id: str, normalized_source_digest: str) -> str:
    if not re.fullmatch(r"obs_[0-9a-f]{64}", observation_id):
        raise ValueError("invalid observation_id")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", normalized_source_digest):
        raise ValueError("invalid normalized_source_digest")
    payload = (observation_id + normalized_source_digest).encode("utf-8")
    return "rev_" + hashlib.sha256(payload).hexdigest()


def make_lineage_event_id(seed_observation_id: str) -> str:
    if not re.fullmatch(r"obs_[0-9a-f]{64}", seed_observation_id):
        raise ValueError("invalid seed observation_id")
    return "evt_" + hashlib.sha256(seed_observation_id.encode("utf-8")).hexdigest()


def normalize_source_text(
    value: str,
    *,
    max_chars: int = 24 * 1024,
    boilerplate_patterns: Sequence[str] = (),
) -> str:
    """Normalize bounded source evidence without retaining generated prose."""
    if not isinstance(value, str):
        raise TypeError("source text must be a string")
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    bounded = value[:max_chars]
    parser = _EvidenceHTMLParser()
    try:
        parser.feed(bounded)
        parser.close()
        extracted = "".join(parser.parts)
    except Exception:
        extracted = re.sub(r"<[^>]*>", " ", bounded)
    extracted = html.unescape(extracted)
    extracted = _MARKDOWN_LINK_PATTERN.sub(r"\1", extracted)
    extracted = _URL_PATTERN.sub(" ", extracted)
    custom_patterns = tuple(re.compile(pattern, re.I) for pattern in boilerplate_patterns)
    lines: list[str] = []
    for raw_line in extracted.splitlines():
        line = " ".join(raw_line.strip().split())
        if not line:
            continue
        if any(
            pattern.search(line) for pattern in (*_DEFAULT_BOILERPLATE_PATTERNS, *custom_patterns)
        ):
            continue
        lines.append(line)
    normalized = unicodedata.normalize("NFKC", " ".join(lines)).casefold()
    normalized = normalized.replace("_", " ")
    normalized = _NON_TEXT_PATTERN.sub(" ", normalized)
    return " ".join(normalized.split())


def _shingle_sample(values: Iterable[str], limit: int) -> frozenset[str]:
    unique = set(values)
    if len(unique) <= limit:
        return frozenset(unique)
    ordered = sorted(
        unique,
        key=lambda value: (hashlib.blake2b(value.encode("utf-8"), digest_size=8).digest(), value),
    )
    return frozenset(ordered[:limit])


def build_shingles(value: str, *, max_shingles: int = 4096) -> frozenset[str]:
    if max_shingles <= 0:
        raise ValueError("max_shingles must be positive")
    normalized = normalize_source_text(value)
    shingles: list[str] = []
    for sequence in _CHINESE_SEQUENCE_PATTERN.findall(normalized):
        shingles.extend(f"zh:{sequence[index : index + 4]}" for index in range(len(sequence) - 3))
    english = _ENGLISH_TOKEN_PATTERN.findall(normalized)
    shingles.extend(
        "en:" + "\x1f".join(english[index : index + 3]) for index in range(len(english) - 2)
    )
    return _shingle_sample(shingles, max_shingles)


def _hash_shingle(value: str) -> int:
    return int.from_bytes(hashlib.blake2b(value.encode("utf-8"), digest_size=8).digest(), "big")


def _simhash256(hashed_shingles: Sequence[int]) -> int:
    if not hashed_shingles:
        return 0
    counts = [0] * 256
    for shingle_hash in hashed_shingles[:256]:
        digest = int.from_bytes(hashlib.sha256(shingle_hash.to_bytes(8, "big")).digest(), "big")
        for bit in range(256):
            counts[bit] += 1 if digest & (1 << bit) else -1
    result = 0
    for bit, count in enumerate(counts):
        if count >= 0:
            result |= 1 << bit
    return result


def _fingerprint_from_normalized_shingles(
    normalized: str,
    shingles: Iterable[str],
    *,
    kmv_size: int = 256,
) -> Fingerprint:
    hashed = frozenset(_hash_shingle(value) for value in shingles)
    ordered = tuple(sorted(hashed))
    bitmap = 0
    for value in hashed:
        bitmap |= 1 << (value % 4096)
    return Fingerprint(
        normalized_digest="sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
        normalized_chars=len(normalized),
        shingle_count=len(hashed),
        bitmap_hex=bitmap.to_bytes(512, "big").hex(),
        simhash_hex=f"{_simhash256(ordered):064x}",
        kmv=ordered[:kmv_size],
        shingle_hashes=hashed,
    )


def fingerprint_text(value: str, *, config: LineageConfig | None = None) -> Fingerprint:
    resolved = config or LineageConfig()
    normalized = normalize_source_text(
        value,
        max_chars=resolved.max_source_chars,
        boilerplate_patterns=resolved.boilerplate_patterns,
    )
    shingles = build_shingles(normalized, max_shingles=resolved.max_shingles)
    return _fingerprint_from_normalized_shingles(
        normalized,
        shingles,
        kmv_size=resolved.kmv_size,
    )


def _canonical_timestamp(value: str | datetime) -> str:
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError as exc:
            raise ValueError(f"invalid ISO-8601 timestamp: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _parsed_timestamp(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _effective_timestamp(observation: ObservationInput) -> datetime | None:
    return _parsed_timestamp(observation.source_published_at or observation.first_seen_at)


def _earlier(left: ObservationInput, right: ObservationInput) -> ObservationInput:
    left_time = _effective_timestamp(left) or datetime.max.replace(tzinfo=UTC)
    right_time = _effective_timestamp(right) or datetime.max.replace(tzinfo=UTC)
    return min(
        (left, right),
        key=lambda item: (left_time if item is left else right_time, item.observation_id),
    )


def _normalized_title(value: str) -> str:
    return normalize_source_text(value, max_chars=500)


def _title_signals(value: str) -> frozenset[str]:
    normalized = _normalized_title(value)
    signals = {
        token
        for token in _ENGLISH_TOKEN_PATTERN.findall(normalized)
        if (len(token) >= 4 or any(character.isdigit() for character in token))
        and token not in _TITLE_STOPWORDS
    }
    for sequence in _CHINESE_SEQUENCE_PATTERN.findall(normalized):
        signals.update(sequence[index : index + 2] for index in range(len(sequence) - 1))
    return frozenset(signals)


def _title_similarity(left: str, right: str) -> float:
    left_normalized = _normalized_title(left)
    right_normalized = _normalized_title(right)
    if not left_normalized or not right_normalized:
        return 0.0
    return SequenceMatcher(None, left_normalized, right_normalized).ratio()


def _approximate_evidence_eligible(observation: ObservationInput) -> bool:
    mode = observation.capture_mode.casefold()
    completeness = observation.source_completeness.casefold()
    return (
        mode not in {"metadata_only", "title_only", "excerpt"}
        and completeness not in {"metadata_only", "partial", "title_only"}
        and not observation.source_is_truncated
    )


def _non_metadata_evidence(observation: ObservationInput) -> bool:
    return observation.capture_mode.casefold() not in {"metadata_only", "title_only"} and (
        observation.source_completeness.casefold() not in {"metadata_only", "title_only"}
    )


def classify_relationship(
    left: ObservationInput,
    right: ObservationInput,
    *,
    config: LineageConfig | None = None,
    left_fingerprint: Fingerprint | None = None,
    right_fingerprint: Fingerprint | None = None,
) -> RelationshipDecision:
    resolved = config or LineageConfig()
    left_fp = left_fingerprint or fingerprint_text(left.source_text, config=resolved)
    right_fp = right_fingerprint or fingerprint_text(right.source_text, config=resolved)
    common = len(left_fp.shingle_hashes & right_fp.shingle_hashes)
    union = len(left_fp.shingle_hashes | right_fp.shingle_hashes)
    jaccard = common / union if union else 0.0
    left_containment = common / left_fp.shingle_count if left_fp.shingle_count else 0.0
    right_containment = common / right_fp.shingle_count if right_fp.shingle_count else 0.0
    shared_signals = len(_title_signals(left.title) & _title_signals(right.title))
    title_similarity = _title_similarity(left.title, right.title)
    earlier = _earlier(left, right)
    parent_id = earlier.observation_id

    substantial = (
        min(left_fp.normalized_chars, right_fp.normalized_chars) >= resolved.exact_min_chars
        and min(left_fp.shingle_count, right_fp.shingle_count) >= resolved.exact_min_shingles
    )
    title_aligned = title_similarity >= 0.6 or shared_signals >= 1
    if (
        left_fp.normalized_digest == right_fp.normalized_digest
        and substantial
        and title_aligned
        and _non_metadata_evidence(left)
        and _non_metadata_evidence(right)
    ):
        return RelationshipDecision(
            relation=RelationKind.EXACT_COPY,
            confidence=1.0,
            jaccard=jaccard,
            left_containment=left_containment,
            right_containment=right_containment,
            common_shingles=common,
            shared_signals=shared_signals,
            parent_observation_id=parent_id,
            suppression_eligible=True,
            reason="normalized_digest_and_title_or_signal_match",
        )

    confidence = 0.4 * jaccard + 0.3 * left_containment + 0.3 * right_containment
    approximate_eligible = _approximate_evidence_eligible(left) and _approximate_evidence_eligible(
        right
    )
    if (
        approximate_eligible
        and min(left_fp.normalized_chars, right_fp.normalized_chars)
        >= resolved.syndicated_min_chars
        and min(left_fp.shingle_count, right_fp.shingle_count) >= resolved.syndicated_min_shingles
        and jaccard >= resolved.syndicated_jaccard
        and min(left_containment, right_containment) >= resolved.syndicated_containment
        and confidence >= resolved.syndicated_confidence
    ):
        return RelationshipDecision(
            relation=RelationKind.SYNDICATED,
            confidence=confidence,
            jaccard=jaccard,
            left_containment=left_containment,
            right_containment=right_containment,
            common_shingles=common,
            shared_signals=shared_signals,
            parent_observation_id=parent_id,
            suppression_eligible=True,
            reason="high_bidirectional_source_overlap",
        )

    left_time = _effective_timestamp(left)
    right_time = _effective_timestamp(right)
    reliable_time = (
        left_time is not None
        and right_time is not None
        and left.timestamp_confidence is not TimestampConfidence.UNKNOWN
        and right.timestamp_confidence is not TimestampConfidence.UNKNOWN
        and left_time != right_time
    )
    asymmetric = (
        max(left_containment, right_containment) >= resolved.derivative_containment
        and min(left_containment, right_containment) < resolved.derivative_containment
    )
    if (
        approximate_eligible
        and reliable_time
        and jaccard >= resolved.derivative_jaccard
        and asymmetric
        and common >= resolved.derivative_common_shingles
    ):
        return RelationshipDecision(
            relation=RelationKind.DERIVATIVE,
            confidence=min(0.97, 0.45 * jaccard + 0.55 * max(left_containment, right_containment)),
            jaccard=jaccard,
            left_containment=left_containment,
            right_containment=right_containment,
            common_shingles=common,
            shared_signals=shared_signals,
            parent_observation_id=parent_id,
            suppression_eligible=False,
            reason="asymmetric_overlap_with_reliable_time_direction",
        )

    within_window = False
    if left_time is not None and right_time is not None:
        delta_hours = abs((left_time - right_time).total_seconds()) / 3600
        within_window = delta_hours <= resolved.same_event_hours
    if (
        within_window
        and title_similarity >= resolved.same_event_title_similarity
        and shared_signals >= resolved.same_event_shared_signals
    ):
        return RelationshipDecision(
            relation=RelationKind.SAME_EVENT,
            confidence=min(0.95, 0.65 * title_similarity + 0.05 * min(shared_signals, 6)),
            jaccard=jaccard,
            left_containment=left_containment,
            right_containment=right_containment,
            common_shingles=common,
            shared_signals=shared_signals,
            parent_observation_id=parent_id,
            suppression_eligible=False,
            reason="time_bounded_title_and_signal_match_shadow_only",
        )

    return RelationshipDecision(
        relation=RelationKind.RELATED_ONLY,
        confidence=min(0.79, max(jaccard, title_similarity * 0.5)),
        jaccard=jaccard,
        left_containment=left_containment,
        right_containment=right_containment,
        common_shingles=common,
        shared_signals=shared_signals,
        parent_observation_id=parent_id if common or shared_signals else None,
        suppression_eligible=False,
        reason="insufficient_evidence_for_stronger_relation",
    )


def apply_suppression_circuit_breaker(
    decisions: Sequence[RelationshipDecision],
    *,
    new_observation_count: int,
    config: LineageConfig | None = None,
) -> CircuitBreakerResult:
    if new_observation_count < 0:
        raise ValueError("new_observation_count must not be negative")
    resolved = config or LineageConfig()
    count = sum(1 for decision in decisions if decision.suppression_eligible)
    reason: str | None = None
    if count > resolved.suppression_absolute_limit:
        reason = "absolute_limit"
    elif (
        new_observation_count
        and count >= resolved.suppression_ratio_min_count
        and count / new_observation_count > resolved.suppression_ratio_limit
    ):
        reason = "ratio_limit"
    if reason is None:
        return CircuitBreakerResult(tuple(decisions), False, None, count)
    disabled = tuple(
        replace(
            decision,
            suppression_eligible=False,
            reason=f"{decision.reason};circuit_breaker={reason}",
        )
        if decision.suppression_eligible
        else decision
        for decision in decisions
    )
    return CircuitBreakerResult(disabled, True, reason, count)


def _split_frontmatter(value: str) -> tuple[dict[str, Any], str]:
    if not value.startswith("---"):
        raise LineageValidationError("Post has no YAML frontmatter")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)(.*)$", value, flags=re.DOTALL)
    if match is None:
        raise LineageValidationError("Post has malformed YAML frontmatter")
    raw = yaml.safe_load(match.group(1)) or {}
    if not isinstance(raw, dict):
        raise LineageValidationError("Post frontmatter must be a mapping")
    return raw, match.group(2)


def _source_excerpt(body: str) -> str:
    heading = re.search(
        r"(?im)^##\s*(?:来源摘要\s*/\s*节选|来源摘要|source summary\s*/\s*excerpt)\s*$",
        body,
    )
    if heading is None:
        return ""
    tail = body[heading.end() :]
    next_heading = re.search(r"(?m)^##\s+", tail)
    section = tail[: next_heading.start()] if next_heading else tail
    quoted: list[str] = []
    plain: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(">"):
            quoted.append(stripped.removeprefix(">").strip())
        else:
            plain.append(stripped)
    selected = quoted if quoted else plain
    return "\n".join(line for line in selected if line)


def _frontmatter_string(metadata: Mapping[str, Any], *names: str) -> str | None:
    for name in names:
        value = metadata.get(name)
        if value is None:
            continue
        if isinstance(value, datetime):
            return _canonical_timestamp(value)
        text = str(value).strip()
        if text:
            return text
    return None


def _day_timestamp(value: str) -> str:
    parsed = _parsed_timestamp(_canonical_timestamp(value))
    assert parsed is not None
    return (
        parsed.replace(hour=0, minute=0, second=0, microsecond=0).isoformat().replace("+00:00", "Z")
    )


def _article_url(path: Path, metadata: Mapping[str, Any]) -> str:
    explicit = metadata.get("url")
    if isinstance(explicit, str) and explicit.strip().startswith("/"):
        value = explicit.strip()
        return value if value.endswith("/") else value + "/"
    return f"/posts/{path.stem}/"


def observation_from_contract(
    item: Mapping[str, Any],
    *,
    article_path: str = "",
    article_url: str | None = None,
    first_seen_at: str | None = None,
    last_seen_at: str | None = None,
    active: bool = True,
) -> ObservationInput:
    """Map an already-verified source contract to lineage input.

    Callers remain responsible for invoking ``verify_source_contract`` before
    this adapter.  The adapter intentionally reads only the immutable original
    source evidence and never downstream summaries or generated article prose.
    """
    raw_url = item.get("url") or item.get("repo_url") or item.get("external_url")
    title = item.get("title")
    source_text = item.get("source_text_original")
    evidence = item.get("source_evidence")
    if not isinstance(source_text, str) and isinstance(evidence, Mapping):
        fields = evidence.get("fields")
        if isinstance(fields, Mapping):
            source_text = fields.get("source_text")
    if not isinstance(raw_url, str) or not raw_url.strip():
        raise LineageValidationError("contracted observation has no canonical source URL")
    if not isinstance(title, str) or not title.strip():
        raise LineageValidationError("contracted observation has no title")
    if not isinstance(source_text, str):
        raise LineageValidationError("contracted observation has no original source text")
    raw_confidence = str(item.get("timestamp_confidence") or "unknown").casefold()
    try:
        confidence = TimestampConfidence(raw_confidence)
    except ValueError as exc:
        raise LineageValidationError(
            "contracted observation has invalid timestamp confidence"
        ) from exc
    resolved_article_url = article_url
    if resolved_article_url is None and article_path:
        resolved_article_url = f"/posts/{Path(article_path).stem}/"
    return ObservationInput(
        canonical_url=raw_url,
        title=title,
        source_text=source_text,
        source=str(item.get("source") or "unknown"),
        article_path=article_path,
        capture_mode=str(item.get("source_capture_mode") or "metadata_only"),
        source_completeness=str(item.get("source_completeness") or "metadata_only"),
        source_is_truncated=bool(item.get("source_is_truncated", False)),
        source_published_at=_frontmatter_string(item, "source_published_at"),
        first_seen_at=first_seen_at or _frontmatter_string(item, "first_seen_at", "captured_at"),
        last_seen_at=last_seen_at or _frontmatter_string(item, "last_seen_at"),
        timestamp_confidence=confidence,
        active=active,
        article_url=resolved_article_url,
        source_payload_sha256=_frontmatter_string(item, "source_payload_sha256"),
    )


def parse_historical_post(
    path: Path,
    *,
    content_root: Path,
    first_seen_at: str | None = None,
    last_seen_at: str | None = None,
) -> ObservationInput | None:
    metadata, body = _split_frontmatter(path.read_text(encoding="utf-8"))
    external_url = metadata.get("external_url")
    title = metadata.get("title")
    if not isinstance(external_url, str) or not external_url.strip():
        return None
    if not isinstance(title, str) or not title.strip():
        return None
    source_text = _source_excerpt(body)
    source_published_at = _frontmatter_string(
        metadata,
        "source_published_at",
        "published_at",
        "source_date",
    )
    if source_published_at is not None:
        source_published_at = _canonical_timestamp(source_published_at)
    fallback_seen = first_seen_at or _frontmatter_string(metadata, "first_seen_at", "date")
    if fallback_seen is not None:
        fallback_seen = _canonical_timestamp(fallback_seen)
    seen_last = last_seen_at or _frontmatter_string(metadata, "last_seen_at") or fallback_seen
    if seen_last is not None:
        seen_last = _canonical_timestamp(seen_last)
    raw_confidence = _frontmatter_string(metadata, "timestamp_confidence")
    if raw_confidence is not None:
        try:
            confidence = TimestampConfidence(raw_confidence)
        except ValueError:
            confidence = TimestampConfidence.UNKNOWN
    elif source_published_at is not None:
        confidence = TimestampConfidence.PUBLISHER
    elif first_seen_at is not None:
        confidence = TimestampConfidence.GIT
    elif fallback_seen is not None:
        confidence = TimestampConfidence.OBSERVED
    else:
        confidence = TimestampConfidence.UNKNOWN
    capture_mode = str(metadata.get("source_capture_mode") or "metadata_only")
    completeness = str(metadata.get("source_completeness") or "metadata_only")
    if not source_text:
        capture_mode = "metadata_only"
        completeness = "metadata_only"
    draft = metadata.get("draft") is True
    archived = (
        metadata.get("archived") is True
        or str(metadata.get("publication_state") or "").casefold() == "archived"
        or str(metadata.get("content_mode") or "").casefold() == "terminal_archive"
    )
    try:
        relative_path = path.resolve().relative_to(content_root.resolve()).as_posix()
    except ValueError:
        relative_path = path.resolve().as_posix()
    return ObservationInput(
        canonical_url=external_url,
        title=title,
        source_text=source_text,
        source=str(metadata.get("source") or "unknown"),
        article_path=relative_path,
        capture_mode=capture_mode,
        source_completeness=completeness,
        source_is_truncated=bool(metadata.get("source_is_truncated", False)),
        source_published_at=source_published_at,
        first_seen_at=fallback_seen,
        last_seen_at=seen_last,
        timestamp_confidence=confidence,
        active=not draft and not archived,
        article_url=_article_url(path, metadata),
        source_payload_sha256=_frontmatter_string(
            metadata, "source_payload_sha256", "source_snapshot_sha256", "source_capture_sha256"
        ),
    )


def _bucket_for_id(identifier: str, shard_count: int) -> str:
    if not re.fullmatch(r"(?:obs|evt)_[0-9a-f]{64}", identifier):
        raise LineageValidationError(f"invalid lineage identifier: {identifier}")
    prefix = identifier.split("_", 1)[1][:8]
    width = max(2, len(f"{shard_count - 1:x}"))
    return f"{int(prefix, 16) % shard_count:0{width}x}"


def lineage_bucket(identifier: str, *, shard_count: int = 128) -> str:
    """Return the browser-compatible deterministic bucket for a lineage ID."""
    return _bucket_for_id(identifier, shard_count)


def _json_bytes(value: Any) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def _secret_match(payload: bytes) -> bool:
    return any(pattern.search(payload) for pattern in _SECRET_PATTERNS)


def _is_sensitive_query_key(key: str) -> bool:
    segmented_key = unicodedata.normalize("NFKC", key)
    segmented_key = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", segmented_key)
    segmented_key = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", segmented_key)
    normalized_key = re.sub(
        r"[^a-z0-9]+",
        "_",
        segmented_key.casefold(),
    ).strip("_")
    tokens = set(normalized_key.split("_"))
    compact = normalized_key.replace("_", "")
    return bool(_SENSITIVE_QUERY_TOKENS.intersection(tokens)) or (
        compact in _SENSITIVE_QUERY_COMPOUNDS
    )


def _safe_source_url(url: str) -> str:
    parsed = urlsplit(canonicalize_url(url))
    safe_query: list[tuple[str, str]] = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        if _is_sensitive_query_key(key):
            continue
        safe_query.append((key, value))
    return urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, urlencode(safe_query), "")
    )


def _sanitize_embedded_source_urls(value: str) -> str:
    def replace_url(match: re.Match[str]) -> str:
        raw_url = match.group(0)
        try:
            parsed = urlsplit(raw_url)
            if not any(
                _is_sensitive_query_key(key)
                for key, _value in parse_qsl(parsed.query, keep_blank_values=True)
            ):
                return raw_url
            return _safe_source_url(raw_url)
        except ValueError:
            return raw_url

    return _EMBEDDED_HTTP_URL_PATTERN.sub(replace_url, value)


def _time_sort_key(observation: ObservationInput) -> tuple[str, str]:
    return (
        observation.source_published_at or observation.first_seen_at or "9999-12-31T23:59:59Z",
        observation.observation_id,
    )


def _event_created_at_from_observation(observation: ObservationInput) -> str:
    return (
        observation.first_seen_at
        or observation.last_seen_at
        or observation.source_published_at
        or "9999-12-31T23:59:59Z"
    )


def _event_state_from_record(record: Mapping[str, Any]) -> tuple[str, tuple[str, ...]]:
    event_id = str(record.get("event_id") or "")
    if not re.fullmatch(r"evt_[0-9a-f]{64}", event_id):
        raise LineageValidationError("registry observation has invalid event_id")
    created_at = str(
        record.get("event_created_at")
        or record.get("first_seen_at")
        or record.get("last_seen_at")
        or record.get("source_published_at")
        or "9999-12-31T23:59:59Z"
    )
    if created_at != "9999-12-31T23:59:59Z":
        created_at = _canonical_timestamp(created_at)
    raw_aliases = record.get("event_aliases", [])
    if not isinstance(raw_aliases, list):
        raise LineageValidationError("registry event aliases must be a list")
    aliases = tuple(sorted({str(value) for value in raw_aliases if str(value) != event_id}))
    if any(not re.fullmatch(r"evt_[0-9a-f]{64}", value) for value in aliases):
        raise LineageValidationError("registry event alias is invalid")
    return created_at, aliases


def _existing_event_states(
    records: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    states: dict[str, dict[str, Any]] = {}
    for record in records.values():
        event_id = str(record.get("event_id") or "")
        created_at, aliases = _event_state_from_record(record)
        state = states.setdefault(
            event_id,
            {"created_at": created_at, "aliases": set()},
        )
        state["created_at"] = min(str(state["created_at"]), created_at)
        state["aliases"].update(aliases)
    return {
        event_id: {
            "created_at": str(state["created_at"]),
            "aliases": tuple(sorted(state["aliases"])),
        }
        for event_id, state in sorted(states.items())
    }


def _existing_event_map(internal_dir: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    registry = internal_dir / "registry"
    if not registry.exists():
        return result
    for path in sorted(registry.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for item in payload.get("observations", []):
            observation_id = item.get("observation_id")
            event_id = item.get("event_id")
            if isinstance(observation_id, str) and isinstance(event_id, str):
                result[observation_id] = event_id
    return result


class _UnionFind:
    def __init__(self, values: Iterable[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            first, second = sorted((left_root, right_root))
            self.parent[second] = first


@dataclass(frozen=True)
class _Prepared:
    observation: ObservationInput
    fingerprint: Fingerprint


def _candidate_score(left: Fingerprint, right: Fingerprint) -> float:
    left_bitmap = int(left.bitmap_hex, 16)
    right_bitmap = int(right.bitmap_hex, 16)
    union = (left_bitmap | right_bitmap).bit_count()
    bitmap_similarity = (left_bitmap & right_bitmap).bit_count() / union if union else 0.0
    hamming = (int(left.simhash_hex, 16) ^ int(right.simhash_hex, 16)).bit_count()
    return 0.7 * bitmap_similarity + 0.3 * (1 - hamming / 256)


def _candidate_keys(prepared: _Prepared) -> tuple[tuple[str, str], ...]:
    fp = prepared.fingerprint
    keys: list[tuple[str, str]] = [("digest", fp.normalized_digest)]
    simhash = fp.simhash_hex
    keys.extend((f"sim{index}", simhash[index * 8 : (index + 1) * 8]) for index in range(8))
    keys.extend(("kmv", f"{value:016x}") for value in fp.kmv[:12])
    title_signals = sorted(_title_signals(prepared.observation.title))
    keys.extend(("title", value) for value in title_signals[:8])
    return tuple(keys)


def _build_prepared(
    observations: Sequence[ObservationInput], config: LineageConfig
) -> list[_Prepared]:
    normalized_by_id: dict[str, str] = {}
    shingles_by_id: dict[str, frozenset[str]] = {}
    document_frequency: Counter[str] = Counter()
    for observation in observations:
        normalized = normalize_source_text(
            observation.source_text,
            max_chars=config.max_source_chars,
            boilerplate_patterns=config.boilerplate_patterns,
        )
        shingles = build_shingles(normalized, max_shingles=config.max_shingles)
        normalized_by_id[observation.observation_id] = normalized
        shingles_by_id[observation.observation_id] = shingles
        document_frequency.update(shingles)
    threshold = max(20, math.ceil(len(observations) * 0.01))
    boilerplate = {shingle for shingle, count in document_frequency.items() if count >= threshold}
    prepared: list[_Prepared] = []
    for observation in observations:
        identifier = observation.observation_id
        filtered = shingles_by_id[identifier] - boilerplate
        prepared.append(
            _Prepared(
                observation,
                _fingerprint_from_normalized_shingles(
                    normalized_by_id[identifier],
                    filtered,
                    kmv_size=config.kmv_size,
                ),
            )
        )
    return prepared


def _relation_priority(value: RelationKind) -> int:
    return {
        RelationKind.EXACT_COPY: 5,
        RelationKind.SYNDICATED: 4,
        RelationKind.DERIVATIVE: 3,
        RelationKind.SAME_EVENT: 2,
        RelationKind.RELATED_ONLY: 1,
        RelationKind.ORIGINAL: 0,
    }[value]


def _fingerprint_from_record(record: Mapping[str, Any]) -> Fingerprint:
    raw = record.get("fingerprint")
    if not isinstance(raw, Mapping):
        raise LineageValidationError("registry observation has no fingerprint")
    if set(raw) != _PERSISTED_FINGERPRINT_FIELDS:
        raise LineageValidationError(
            "registry fingerprint must contain compact candidate signatures only"
        )
    try:
        kmv = tuple(int(str(value), 16) for value in raw["kmv"])
        fingerprint = Fingerprint(
            normalized_digest=str(raw["normalized_digest"]),
            normalized_chars=int(raw["normalized_chars"]),
            shingle_count=int(raw["shingle_count"]),
            bitmap_hex=str(raw["bitmap"]),
            simhash_hex=str(raw["simhash"]),
            kmv=kmv,
            # Exact shingles are deliberately ephemeral.  Persisted Bitmap,
            # SimHash and bottom-K KMV values are candidate-recall aids only;
            # they must never become the final proof for approximate
            # suppression after a registry reload.
            shingle_hashes=frozenset(),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise LineageValidationError("registry observation has an invalid fingerprint") from exc
    if (
        not re.fullmatch(r"sha256:[0-9a-f]{64}", fingerprint.normalized_digest)
        or not re.fullmatch(r"[0-9a-f]{1024}", fingerprint.bitmap_hex)
        or not re.fullmatch(r"[0-9a-f]{64}", fingerprint.simhash_hex)
        or fingerprint.normalized_chars < 0
        or fingerprint.shingle_count < 0
        or len(fingerprint.kmv) > 256
        or len(fingerprint.kmv) > fingerprint.shingle_count
        or tuple(sorted(set(fingerprint.kmv))) != fingerprint.kmv
    ):
        raise LineageValidationError("registry observation fingerprint violates the schema")
    return fingerprint


def _prepared_from_record(record: Mapping[str, Any]) -> _Prepared:
    try:
        confidence = TimestampConfidence(str(record.get("timestamp_confidence") or "unknown"))
        observation = ObservationInput(
            canonical_url=str(record["canonical_url"]),
            title=str(record["title"]),
            source_text="",
            source=str(record.get("source") or "unknown"),
            article_path=str(record.get("article_path") or ""),
            capture_mode=str(record.get("capture_mode") or "metadata_only"),
            source_completeness=str(record.get("source_completeness") or "metadata_only"),
            source_is_truncated=bool(record.get("source_is_truncated", False)),
            source_published_at=record.get("source_published_at"),
            first_seen_at=record.get("first_seen_at"),
            last_seen_at=record.get("last_seen_at"),
            timestamp_confidence=confidence,
            active=bool(record.get("active", True)),
            article_url=str(record.get("article_url") or "") or None,
            source_payload_sha256=str(record.get("source_payload_sha256") or "") or None,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise LineageValidationError("registry observation has invalid metadata") from exc
    if observation.observation_id != record.get("observation_id"):
        raise LineageValidationError("registry observation ID does not match its canonical URL")
    _event_state_from_record(record)
    return _Prepared(observation, _fingerprint_from_record(record))


def _record_from_prepared(
    prepared: _Prepared,
    *,
    event_id: str,
    relation: RelationKind,
    parent_observation_id: str | None,
    event_created_at: str | None = None,
    event_aliases: Sequence[str] = (),
) -> dict[str, Any]:
    observation = prepared.observation
    fingerprint = prepared.fingerprint
    identifier = observation.observation_id
    return {
        "active": observation.active,
        "article_path": observation.article_path,
        "article_url": observation.article_url
        or (f"/posts/{Path(observation.article_path).stem}/" if observation.article_path else None),
        "canonical_url": _safe_source_url(observation.canonical_url),
        "capture_mode": observation.capture_mode,
        "event_aliases": sorted({str(value) for value in event_aliases if value != event_id}),
        "event_created_at": event_created_at or _event_created_at_from_observation(observation),
        "event_id": event_id,
        "fingerprint": {
            "bitmap": fingerprint.bitmap_hex,
            "kmv": [f"{value:016x}" for value in fingerprint.kmv],
            "normalized_chars": fingerprint.normalized_chars,
            "normalized_digest": fingerprint.normalized_digest,
            "shingle_count": fingerprint.shingle_count,
            "simhash": fingerprint.simhash_hex,
        },
        "first_seen_at": observation.first_seen_at,
        "last_seen_at": observation.last_seen_at,
        "observation_id": identifier,
        "parent_observation_id": parent_observation_id,
        "relation": relation.value,
        "revision_id": make_lineage_revision_id(identifier, fingerprint.normalized_digest),
        "source": observation.source,
        "source_completeness": observation.source_completeness,
        "source_is_truncated": observation.source_is_truncated,
        "source_payload_sha256": observation.source_payload_sha256,
        "source_published_at": observation.source_published_at,
        "timestamp_confidence": observation.timestamp_confidence.value,
        "title": observation.title,
    }


class LineageRegistry:
    """Mutable in-memory registry with deterministic, secret-free persistence."""

    def __init__(
        self,
        *,
        config: LineageConfig | None = None,
        records: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> None:
        self.config = config or LineageConfig()
        self._records: dict[str, dict[str, Any]] = {
            identifier: dict(record) for identifier, record in (records or {}).items()
        }

    @classmethod
    def load(
        cls,
        internal_dir: Path,
        *,
        config: LineageConfig | None = None,
    ) -> LineageRegistry:
        resolved = config or LineageConfig()
        index_path = internal_dir / "index.json"
        if not index_path.exists():
            return cls(config=resolved)
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise LineageValidationError("internal registry index is unreadable") from exc
        if index.get("schema") != "lineage_registry_v1":
            raise LineageValidationError("unsupported internal registry schema")
        if index.get("bucket_algorithm") != BUCKET_ALGORITHM:
            raise LineageValidationError("unsupported internal registry bucket algorithm")
        refs = index.get("registry_buckets")
        if not isinstance(refs, list) or len(refs) != resolved.shard_count:
            raise LineageValidationError("internal registry must reference every bucket")
        pending_records: list[dict[str, Any]] = []
        migrated_ids: dict[str, str] = {}
        for reference in refs:
            if not isinstance(reference, Mapping):
                raise LineageValidationError("invalid internal registry reference")
            target = _safe_asset_path(internal_dir, reference.get("path"))
            payload = target.read_bytes()
            if reference.get("bytes") != len(payload):
                raise LineageValidationError("internal registry byte count mismatch")
            if reference.get("sha256") != "sha256:" + sha256_hex(payload):
                raise LineageValidationError("internal registry hash mismatch")
            if _secret_match(payload):
                raise LineageValidationError("secret-like value detected in internal registry")
            shard = json.loads(payload)
            bucket = reference.get("bucket")
            if shard.get("bucket") != bucket:
                raise LineageValidationError("internal registry bucket mismatch")
            for record in shard.get("observations", []):
                if not isinstance(record, Mapping):
                    raise LineageValidationError("invalid internal registry observation")
                stored_identifier = str(record.get("observation_id") or "")
                if _bucket_for_id(stored_identifier, resolved.shard_count) != bucket:
                    raise LineageValidationError("internal observation is stored in wrong bucket")
                migrated = dict(record)
                sanitized_url = _safe_source_url(str(record.get("canonical_url") or ""))
                identifier = make_observation_id(sanitized_url)
                migrated["canonical_url"] = sanitized_url
                migrated["observation_id"] = identifier
                fingerprint = _fingerprint_from_record(migrated)
                migrated["revision_id"] = make_lineage_revision_id(
                    identifier,
                    fingerprint.normalized_digest,
                )
                migrated_ids[stored_identifier] = identifier
                pending_records.append(migrated)
        records: dict[str, dict[str, Any]] = {}
        for migrated in pending_records:
            parent_id = migrated.get("parent_observation_id")
            if isinstance(parent_id, str) and parent_id in migrated_ids:
                migrated["parent_observation_id"] = migrated_ids[parent_id]
            prepared = _prepared_from_record(migrated)
            identifier = prepared.observation.observation_id
            previous = records.get(identifier)
            if previous is None:
                records[identifier] = migrated
                continue
            previous_state = _event_state_from_record(previous)
            migrated_state = _event_state_from_record(migrated)
            primary, secondary = min(
                ((previous, previous_state), (migrated, migrated_state)),
                key=lambda item: (item[1][0], str(item[0]["event_id"])),
            ), max(
                ((previous, previous_state), (migrated, migrated_state)),
                key=lambda item: (item[1][0], str(item[0]["event_id"])),
            )
            latest = max(
                (previous, migrated),
                key=lambda item: (str(item.get("last_seen_at") or ""), str(item["revision_id"])),
            )
            merged = dict(latest)
            primary_record, primary_state = primary
            secondary_record, secondary_state = secondary
            merged["event_id"] = primary_record["event_id"]
            merged["event_created_at"] = primary_state[0]
            aliases = {
                *primary_state[1],
                *secondary_state[1],
                str(secondary_record["event_id"]),
            }
            aliases.discard(str(primary_record["event_id"]))
            merged["event_aliases"] = sorted(aliases)
            merged["first_seen_at"] = min(
                (
                    value
                    for value in (previous.get("first_seen_at"), migrated.get("first_seen_at"))
                    if isinstance(value, str)
                ),
                default=None,
            )
            merged["last_seen_at"] = max(
                (
                    value
                    for value in (previous.get("last_seen_at"), migrated.get("last_seen_at"))
                    if isinstance(value, str)
                ),
                default=None,
            )
            records[identifier] = merged
        return cls(config=resolved, records=records)

    def _prepared_records(self) -> dict[str, _Prepared]:
        return {
            identifier: _prepared_from_record(record)
            for identifier, record in sorted(self._records.items())
        }

    def resolve_batch(
        self,
        observations: Sequence[ObservationInput],
        *,
        historical_baseline: Sequence[ObservationInput] = (),
    ) -> BatchResolution:
        new_ids = [observation.observation_id for observation in observations]
        if len(set(new_ids)) != len(new_ids):
            raise LineageValidationError("resolve_batch received duplicate canonical URLs")

        baseline_prepared_by_id: dict[str, _Prepared] = {}
        prepared_new: dict[str, _Prepared]
        if historical_baseline:
            baseline_ids = [observation.observation_id for observation in historical_baseline]
            if len(set(baseline_ids)) != len(baseline_ids):
                raise LineageValidationError(
                    "resolve_batch received duplicate historical canonical URLs"
                )
            if set(baseline_ids) & set(new_ids):
                raise LineageValidationError(
                    "historical baseline must not duplicate current observations"
                )
            # Build one in-memory corpus so high-frequency template shingles
            # are removed consistently from historical and current evidence.
            combined = _build_prepared(
                [*historical_baseline, *observations], self.config
            )
            baseline_prepared_by_id = {
                item.observation.observation_id: item
                for item in combined[: len(historical_baseline)]
            }
            prepared_new = {
                item.observation.observation_id: item
                for item in combined[len(historical_baseline) :]
            }
            baseline_prepared = list(baseline_prepared_by_id.values())
            existing_events = {
                identifier: str(record["event_id"])
                for identifier, record in self._records.items()
                if isinstance(record.get("event_id"), str)
            }
            baseline_records, _events = _analyze_observations(
                baseline_prepared,
                self.config,
                existing_events,
                _existing_event_states(self._records),
            )
            self._records.update(baseline_records)
        else:
            prepared_new = {
                item.observation.observation_id: item
                for item in _build_prepared(observations, self.config)
            }

        prepared_existing = self._prepared_records()
        # Overlay exact, current-run source shingles on compact persisted
        # records.  Approximate suppression is therefore possible only when
        # the exact source evidence was reconstructed in this process.
        prepared_existing.update(baseline_prepared_by_id)
        lookup: dict[str, _Prepared] = dict(prepared_existing)
        candidate_index: dict[tuple[str, str], list[str]] = defaultdict(list)
        for identifier, prepared in sorted(
            prepared_existing.items(), key=lambda pair: _time_sort_key(pair[1].observation)
        ):
            if prepared.observation.active:
                for key in _candidate_keys(prepared):
                    candidate_index[key].append(identifier)

        provisional: dict[str, tuple[ResolutionItem, RelationshipDecision]] = {}
        for observation in sorted(observations, key=_time_sort_key):
            identifier = observation.observation_id
            current = prepared_new[identifier]
            existing_record = self._records.get(identifier)
            if existing_record is not None:
                try:
                    existing_relation = RelationKind(str(existing_record["relation"]))
                    event_id = str(existing_record["event_id"])
                    parent_id = existing_record.get("parent_observation_id")
                    parent_id = str(parent_id) if parent_id is not None else None
                except (KeyError, ValueError) as exc:
                    raise LineageValidationError(
                        "existing registry relationship is invalid"
                    ) from exc
                revision_id = make_lineage_revision_id(
                    identifier, current.fingerprint.normalized_digest
                )
                unchanged_url_decision = RelationshipDecision(
                    relation=existing_relation,
                    confidence=1.0,
                    jaccard=0.0,
                    left_containment=0.0,
                    right_containment=0.0,
                    common_shingles=0,
                    shared_signals=0,
                    parent_observation_id=parent_id,
                    suppression_eligible=False,
                    reason="existing_observation_new_revision",
                )
                provisional[identifier] = (
                    ResolutionItem(
                        observation_id=identifier,
                        revision_id=revision_id,
                        event_id=event_id,
                        relation=existing_relation,
                        parent_observation_id=parent_id,
                        suppress=False,
                        confidence=1.0,
                    ),
                    unchanged_url_decision,
                )
                self._records[identifier] = _record_from_prepared(
                    current,
                    event_id=event_id,
                    relation=existing_relation,
                    parent_observation_id=parent_id,
                    event_created_at=_event_state_from_record(existing_record)[0],
                    event_aliases=_event_state_from_record(existing_record)[1],
                )
                lookup[identifier] = current
                continue
            candidates: set[str] = set()
            for key in _candidate_keys(current):
                candidates.update(candidate_index.get(key, ()))
            candidates.discard(identifier)
            ranked = sorted(
                candidates,
                key=lambda candidate_id: (
                    -_candidate_score(current.fingerprint, lookup[candidate_id].fingerprint),
                    candidate_id,
                ),
            )[: self.config.max_candidates]
            best: RelationshipDecision | None = None
            best_candidate_id: str | None = None
            for candidate_id in ranked:
                candidate = lookup[candidate_id]
                decision = classify_relationship(
                    candidate.observation,
                    observation,
                    config=self.config,
                    left_fingerprint=candidate.fingerprint,
                    right_fingerprint=current.fingerprint,
                )
                if best is None or (_relation_priority(decision.relation), decision.confidence) > (
                    _relation_priority(best.relation),
                    best.confidence,
                ):
                    best = decision
                    best_candidate_id = candidate_id
            if best is None or best.relation is RelationKind.RELATED_ONLY:
                best = RelationshipDecision(
                    relation=RelationKind.ORIGINAL,
                    confidence=1.0,
                    jaccard=0.0,
                    left_containment=0.0,
                    right_containment=0.0,
                    common_shingles=0,
                    shared_signals=0,
                    parent_observation_id=None,
                    suppression_eligible=False,
                    reason="new_event",
                )
                best_candidate_id = None
            if best.relation in {RelationKind.EXACT_COPY, RelationKind.SYNDICATED} and (
                best_candidate_id is not None
            ):
                candidate_record = self._records[best_candidate_id]
                event_id = str(candidate_record["event_id"])
                event_created_at, event_aliases = _event_state_from_record(candidate_record)
            else:
                event_id = make_lineage_event_id(identifier)
                event_created_at = _event_created_at_from_observation(observation)
                event_aliases = ()
            revision_id = make_lineage_revision_id(
                identifier, current.fingerprint.normalized_digest
            )
            item = ResolutionItem(
                observation_id=identifier,
                revision_id=revision_id,
                event_id=event_id,
                relation=best.relation,
                parent_observation_id=best.parent_observation_id,
                suppress=best.suppression_eligible,
                confidence=best.confidence,
            )
            provisional[identifier] = (item, best)
            self._records[identifier] = _record_from_prepared(
                current,
                event_id=event_id,
                relation=best.relation,
                parent_observation_id=best.parent_observation_id,
                event_created_at=event_created_at,
                event_aliases=event_aliases,
            )
            lookup[identifier] = current
            if observation.active:
                for key in _candidate_keys(current):
                    candidate_index[key].append(identifier)

        ordered_decisions = [provisional[identifier][1] for identifier in new_ids]
        breaker = apply_suppression_circuit_breaker(
            ordered_decisions,
            new_observation_count=len(observations),
            config=self.config,
        )
        items: list[ResolutionItem] = []
        for identifier, effective_decision in zip(new_ids, breaker.decisions, strict=True):
            provisional_item, _decision = provisional[identifier]
            item = replace(
                provisional_item,
                suppress=effective_decision.suppression_eligible,
            )
            items.append(item)
        counts = Counter(item.relation.value for item in items)
        stats = {
            "derivatives": counts[RelationKind.DERIVATIVE.value],
            "exact_copies": counts[RelationKind.EXACT_COPY.value],
            "observations": len(items),
            "same_event": counts[RelationKind.SAME_EVENT.value],
            "suppressed": sum(1 for item in items if item.suppress),
            "syndicated": counts[RelationKind.SYNDICATED.value],
        }
        return BatchResolution(tuple(items), breaker, stats)

    def save(self, internal_dir: Path, *, generated_at: str) -> dict[str, Any]:
        timestamp = _canonical_timestamp(generated_at)
        buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for identifier, record in sorted(self._records.items()):
            buckets[_bucket_for_id(identifier, self.config.shard_count)].append(record)
        references: list[dict[str, Any]] = []
        keep: set[Path] = set()
        for number in range(self.config.shard_count):
            bucket = f"{number:02x}"
            payload = _json_bytes(
                {
                    "bucket": bucket,
                    "observations": buckets.get(bucket, []),
                    "version": LINEAGE_VERSION,
                }
            )
            if _secret_match(payload):
                raise LineageValidationError(
                    "secret-like value detected in internal lineage registry"
                )
            relative = Path("registry") / f"{bucket}.json"
            target = internal_dir / relative
            _atomic_write(target, payload)
            keep.add(target.resolve())
            references.append(
                {
                    "bucket": bucket,
                    "bytes": len(payload),
                    "path": relative.as_posix(),
                    "sha256": "sha256:" + sha256_hex(payload),
                }
            )
        index_payload = _json_bytes(
            {
                "bucket_algorithm": BUCKET_ALGORITHM,
                "bucket_count": self.config.shard_count,
                "generated_at": timestamp,
                "registry_buckets": references,
                "schema": "lineage_registry_v1",
                "stats": {"observations": len(self._records)},
                "version": LINEAGE_VERSION,
            }
        )
        _atomic_write(internal_dir / "index.json", index_payload)
        keep.add((internal_dir / "index.json").resolve())
        for stale in sorted(internal_dir.rglob("*.json")):
            if stale.resolve() not in keep:
                stale.unlink()
        return {"generated_at": timestamp, "observations": len(self._records)}


_DELETE_METADATA = object()


def _metadata_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    text = str(value)
    if re.fullmatch(r"[A-Za-z0-9_./:+-]+", text):
        return text
    return json.dumps(text, ensure_ascii=False)


def _updated_frontmatter(value: str, updates: Mapping[str, Any]) -> str:
    match = re.match(r"^(---\s*\n)(.*?)(\n---\s*(?:\n|$).*)$", value, flags=re.DOTALL)
    if match is None:
        raise LineageValidationError("Post has malformed YAML frontmatter")
    lines = match.group(2).splitlines()
    positions: dict[str, int] = {}
    for index, line in enumerate(lines):
        key_match = re.match(r"^([A-Za-z0-9_-]+)\s*:", line)
        if key_match is not None and key_match.group(1) not in positions:
            positions[key_match.group(1)] = index
    removals = {
        positions[key]
        for key, value_ in updates.items()
        if value_ is _DELETE_METADATA and key in positions
    }
    lines = [line for index, line in enumerate(lines) if index not in removals]
    positions.clear()
    for index, line in enumerate(lines):
        key_match = re.match(r"^([A-Za-z0-9_-]+)\s*:", line)
        if key_match is not None and key_match.group(1) not in positions:
            positions[key_match.group(1)] = index
    for key, value_ in updates.items():
        if value_ is _DELETE_METADATA:
            continue
        rendered = f"{key}: {_metadata_scalar(value_)}"
        if key in positions:
            lines[positions[key]] = rendered
        else:
            positions[key] = len(lines)
            lines.append(rendered)
    return match.group(1) + "\n".join(lines) + match.group(3)


def apply_lineage_post_metadata(
    *,
    content_root: Path,
    internal_dir: Path,
    apply: bool = False,
    config: LineageConfig | None = None,
) -> dict[str, int]:
    """Backfill active Post lineage metadata without deleting or renaming routes."""
    registry = LineageRegistry.load(internal_dir, config=config)
    records = registry._records
    originals: dict[str, Mapping[str, Any]] = {}
    for record in records.values():
        event_id = str(record.get("event_id") or "")
        if not event_id:
            continue
        current = originals.get(event_id)
        record_key = (
            0 if record.get("relation") == RelationKind.ORIGINAL.value else 1,
            str(record.get("source_published_at") or record.get("first_seen_at") or "9999"),
            str(record.get("observation_id")),
        )
        current_key = (
            0 if current and current.get("relation") == RelationKind.ORIGINAL.value else 1,
            str(current.get("source_published_at") or current.get("first_seen_at") or "9999")
            if current
            else "9999",
            str(current.get("observation_id")) if current else "",
        )
        if current is None or record_key < current_key:
            originals[event_id] = record
    changed = 0
    scanned = 0
    for identifier, record in sorted(records.items()):
        relative = record.get("article_path")
        if not isinstance(relative, str) or not relative:
            continue
        path = _safe_asset_path(content_root, relative)
        if not path.is_file():
            if record.get("active", True):
                raise LineageValidationError(f"active lineage Post is missing: {relative}")
            continue
        before = path.read_text(encoding="utf-8")
        metadata, _body = _split_frontmatter(before)
        external_url = metadata.get("external_url")
        if not isinstance(external_url, str) or make_observation_id(external_url) != identifier:
            raise LineageValidationError(
                f"Post canonical URL no longer matches registry: {relative}"
            )
        sanitized_external_url = _safe_source_url(external_url)
        url_updates: dict[str, Any] = {}
        if external_url != sanitized_external_url:
            url_updates["external_url"] = sanitized_external_url
        if not record.get("active", True):
            after = _updated_frontmatter(before, url_updates) if url_updates else before
            after = _sanitize_embedded_source_urls(after)
            if after != before:
                changed += 1
                if apply:
                    _atomic_write(path, after.encode("utf-8"))
            continue
        scanned += 1
        relation = RelationKind(str(record["relation"]))
        event_id = str(record["event_id"])
        duplicate = relation in {RelationKind.EXACT_COPY, RelationKind.SYNDICATED}
        canonical_record = originals[event_id]
        canonical_url = canonical_record.get("article_url")
        updates: dict[str, Any] = {
            **url_updates,
            "observation_id": identifier,
            "revision_id": record["revision_id"],
            "event_id": event_id,
            "lineage_relation": relation.value,
            "parent_observation_id": record.get("parent_observation_id"),
            "source_published_at": record.get("source_published_at"),
            "first_seen_at": record.get("first_seen_at"),
            "last_seen_at": record.get("last_seen_at"),
            "timestamp_confidence": record.get("timestamp_confidence"),
            "lineage_canonical_url": canonical_url if duplicate else _DELETE_METADATA,
            "lineage_noindex": True if duplicate else _DELETE_METADATA,
            "lineage_revision_id": _DELETE_METADATA,
            "lineage_parent_id": _DELETE_METADATA,
        }
        after = _updated_frontmatter(before, updates)
        after = _sanitize_embedded_source_urls(after)
        if after != before:
            changed += 1
            if apply:
                _atomic_write(path, after.encode("utf-8"))
    return {"changed": changed, "deleted": 0, "scanned": scanned}


def _analyze_observations(
    prepared: Sequence[_Prepared],
    config: LineageConfig,
    existing_events: Mapping[str, str],
    existing_event_states: Mapping[str, Mapping[str, Any]] | None = None,
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    by_id = {item.observation.observation_id: item for item in prepared}
    union_find = _UnionFind(by_id)
    relations: dict[str, RelationshipDecision] = {}
    index: dict[tuple[str, str], list[str]] = defaultdict(list)
    ordered = sorted(prepared, key=lambda item: _time_sort_key(item.observation))

    for current in ordered:
        observation = current.observation
        candidates: set[str] = set()
        if observation.active:
            for key in _candidate_keys(current):
                candidates.update(index.get(key, ()))
        ranked = sorted(
            (identifier for identifier in candidates if by_id[identifier].observation.active),
            key=lambda identifier: (
                -_candidate_score(current.fingerprint, by_id[identifier].fingerprint),
                identifier,
            ),
        )[: config.max_candidates]
        best: RelationshipDecision | None = None
        for identifier in ranked:
            candidate = by_id[identifier]
            candidate_decision = classify_relationship(
                candidate.observation,
                observation,
                config=config,
                left_fingerprint=candidate.fingerprint,
                right_fingerprint=current.fingerprint,
            )
            if candidate_decision.relation in {
                RelationKind.EXACT_COPY,
                RelationKind.SYNDICATED,
            }:
                union_find.union(identifier, observation.observation_id)
            if best is None or (
                _relation_priority(candidate_decision.relation),
                candidate_decision.confidence,
                identifier,
            ) > (
                _relation_priority(best.relation),
                best.confidence,
                best.parent_observation_id or "",
            ):
                best = candidate_decision
        if best is not None and best.relation is not RelationKind.RELATED_ONLY:
            relations[observation.observation_id] = best
        for key in _candidate_keys(current):
            index[key].append(observation.observation_id)

    components: dict[str, list[str]] = defaultdict(list)
    for identifier in sorted(by_id):
        components[union_find.find(identifier)].append(identifier)
    event_for_observation: dict[str, str] = {}
    aliases_for_event: dict[str, list[str]] = {}
    component_details: dict[str, tuple[str, str, str, list[str]]] = {}
    created_at_for_event: dict[str, str] = {}
    states = existing_event_states or {}
    for members in components.values():
        members.sort(key=lambda identifier: _time_sort_key(by_id[identifier].observation))
        existing = {existing_events[item] for item in members if item in existing_events}
        if existing:
            event_id = min(
                existing,
                key=lambda value: (
                    str(states.get(value, {}).get("created_at") or "9999-12-31T23:59:59Z"),
                    value,
                ),
            )
            event_created_at = str(
                states.get(event_id, {}).get("created_at") or "9999-12-31T23:59:59Z"
            )
        else:
            event_id = make_lineage_event_id(members[0])
            event_created_at = _event_created_at_from_observation(by_id[members[0]].observation)
        aliases = set(existing) - {event_id}
        for existing_event in existing:
            raw_aliases = states.get(existing_event, {}).get("aliases", ())
            if isinstance(raw_aliases, (list, tuple, set, frozenset)):
                aliases.update(str(value) for value in raw_aliases)
        aliases.discard(event_id)
        aliases_for_event[event_id] = sorted(aliases)
        created_at_for_event[event_id] = event_created_at
        earliest = members[0]
        component_details[event_id] = (earliest, earliest, members[0], members)
        for member in members:
            event_for_observation[member] = event_id

    observations_out: dict[str, dict[str, Any]] = {}
    for identifier, item in sorted(by_id.items()):
        observation = item.observation
        event_id = event_for_observation[identifier]
        earliest = component_details[event_id][0]
        selected_decision = relations.get(identifier)
        relation = (
            selected_decision.relation
            if selected_decision is not None
            else (RelationKind.ORIGINAL if identifier == earliest else RelationKind.RELATED_ONLY)
        )
        parent = selected_decision.parent_observation_id if selected_decision is not None else None
        if (
            identifier != earliest
            and relation is RelationKind.RELATED_ONLY
            and len(component_details[event_id][3]) > 1
        ):
            relation = RelationKind.SYNDICATED
            parent = earliest
        observations_out[identifier] = {
            "active": observation.active,
            "article_path": observation.article_path,
            "article_url": observation.article_url
            or f"/posts/{Path(observation.article_path).stem}/",
            "canonical_url": _safe_source_url(observation.canonical_url),
            "capture_mode": observation.capture_mode,
            "event_aliases": aliases_for_event[event_id],
            "event_created_at": created_at_for_event[event_id],
            "event_id": event_id,
            "fingerprint": {
                "bitmap": item.fingerprint.bitmap_hex,
                "kmv": [f"{value:016x}" for value in item.fingerprint.kmv],
                "normalized_chars": item.fingerprint.normalized_chars,
                "normalized_digest": item.fingerprint.normalized_digest,
                "shingle_count": item.fingerprint.shingle_count,
                "simhash": item.fingerprint.simhash_hex,
            },
            "first_seen_at": observation.first_seen_at,
            "last_seen_at": observation.last_seen_at,
            "observation_id": identifier,
            "parent_observation_id": parent,
            "relation": relation.value,
            "revision_id": make_lineage_revision_id(identifier, item.fingerprint.normalized_digest),
            "source": observation.source,
            "source_completeness": observation.source_completeness,
            "source_is_truncated": observation.source_is_truncated,
            "source_payload_sha256": observation.source_payload_sha256,
            "source_published_at": observation.source_published_at,
            "timestamp_confidence": observation.timestamp_confidence.value,
            "title": observation.title,
        }

    events_out: dict[str, dict[str, Any]] = {}
    for event_id, (earliest, probable, representative, members) in sorted(
        component_details.items()
    ):
        events_out[event_id] = {
            "event_aliases": aliases_for_event[event_id],
            "event_id": event_id,
            "earliest_observed_id": earliest,
            "probable_origin_id": probable,
            "representative_observation_id": representative,
            "members": members,
        }
    return observations_out, events_out


def _public_observation(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "article_url": record["article_url"],
        "first_seen_at": record["first_seen_at"],
        "observation_id": record["observation_id"],
        "parent_observation_id": record["parent_observation_id"],
        "relation": record["relation"],
        "source": record["source"],
        "source_published_at": record["source_published_at"],
        "source_url": record["canonical_url"],
        "timestamp_confidence": record["timestamp_confidence"],
        "title": record["title"],
    }


def _event_records_from_observations(
    records: Mapping[str, Mapping[str, Any]],
    analyzed_events: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for identifier, record in sorted(records.items()):
        event_id = record.get("event_id")
        if not isinstance(event_id, str) or not re.fullmatch(r"evt_[0-9a-f]{64}", event_id):
            raise LineageValidationError("registry observation has invalid event_id")
        grouped[event_id].append(identifier)
    result: dict[str, dict[str, Any]] = {}
    for event_id, members in sorted(grouped.items()):
        members.sort(
            key=lambda identifier: (
                records[identifier].get("source_published_at")
                or records[identifier].get("first_seen_at")
                or "9999-12-31T23:59:59Z",
                identifier,
            )
        )
        earliest = members[0]
        originals = [
            identifier
            for identifier in members
            if records[identifier].get("relation") == RelationKind.ORIGINAL.value
        ]
        representative_candidates = [
            identifier
            for identifier in (*originals, *members)
            if records[identifier].get("article_url")
        ]
        representative = representative_candidates[0] if representative_candidates else earliest
        analyzed = analyzed_events.get(event_id, {})
        raw_aliases = analyzed.get("event_aliases", [])
        aliases = (
            {str(value) for value in raw_aliases if str(value) != event_id}
            if isinstance(raw_aliases, list)
            else set()
        )
        for identifier in members:
            record_aliases = records[identifier].get("event_aliases", [])
            if isinstance(record_aliases, list):
                aliases.update(str(value) for value in record_aliases if str(value) != event_id)
        result[event_id] = {
            "event_aliases": sorted(aliases),
            "event_id": event_id,
            "earliest_observed_id": earliest,
            "probable_origin_id": earliest,
            "representative_observation_id": representative,
            "members": members,
        }
    return result


def _write_content_addressed_shards(
    *,
    public_dir: Path,
    directory: str,
    field_name: str,
    buckets: Mapping[str, list[dict[str, Any]]],
    config: LineageConfig,
) -> tuple[list[dict[str, Any]], set[Path]]:
    references: list[dict[str, Any]] = []
    paths: set[Path] = set()
    for number in range(config.shard_count):
        bucket = f"{number:02x}"
        payload = _json_bytes(
            {"bucket": bucket, field_name: buckets.get(bucket, []), "version": LINEAGE_VERSION}
        )
        if len(payload) > config.shard_max_bytes:
            raise LineageValidationError(f"public {directory} shard {bucket} exceeds size limit")
        digest = sha256_hex(payload)
        relative = Path(directory) / f"{bucket}-{digest[:16]}.json"
        target = public_dir / relative
        _atomic_write(target, payload)
        paths.add(target.resolve())
        references.append(
            {
                "bucket": bucket,
                "bytes": len(payload),
                "path": relative.as_posix(),
                "sha256": "sha256:" + digest,
            }
        )
    return references, paths


def build_lineage_assets(
    *,
    content_root: Path,
    internal_dir: Path,
    public_dir: Path,
    config_path: Path = DEFAULT_CONFIG_PATH,
    config: LineageConfig | None = None,
    as_of: str | None = None,
    first_seen_by_path: Mapping[Path, str] | None = None,
) -> dict[str, Any]:
    resolved = config or load_lineage_config(config_path)
    paths = sorted((content_root / "posts").rglob("*.md"))
    first_seen = {path.resolve(): value for path, value in (first_seen_by_path or {}).items()}
    existing_registry = LineageRegistry.load(internal_dir, config=resolved)
    existing_records = existing_registry._records
    if as_of is None:
        candidate_dates: list[str] = []
        for path in paths:
            try:
                metadata, _body = _split_frontmatter(path.read_text(encoding="utf-8"))
            except (OSError, LineageValidationError, yaml.YAMLError):
                continue
            date = _frontmatter_string(metadata, "date")
            if date:
                candidate_dates.append(_canonical_timestamp(date))
        existing_index = internal_dir / "index.json"
        if existing_index.is_file():
            try:
                existing_generated_at = json.loads(
                    existing_index.read_text(encoding="utf-8")
                ).get("generated_at")
            except (OSError, json.JSONDecodeError):
                existing_generated_at = None
            if isinstance(existing_generated_at, str):
                candidate_dates.append(_canonical_timestamp(existing_generated_at))
        as_of = max(candidate_dates, default="1970-01-01T00:00:00Z")
    generated_at = _canonical_timestamp(as_of)
    observations: list[ObservationInput] = []
    errors: list[str] = []
    for path in paths:
        try:
            observation = parse_historical_post(
                path,
                content_root=content_root,
                first_seen_at=first_seen.get(path.resolve()),
            )
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{path.as_posix()}: {exc}")
            continue
        if observation is not None:
            observations.append(observation)
    if errors:
        raise LineageValidationError("failed to parse Posts: " + "; ".join(errors[:5]))
    observations.sort(key=_time_sort_key)
    prepared = _build_prepared(observations, resolved)
    existing = {
        identifier: str(record["event_id"])
        for identifier, record in existing_records.items()
        if isinstance(record.get("event_id"), str)
    }
    observation_records, analyzed_events = _analyze_observations(
        prepared,
        resolved,
        existing,
        _existing_event_states(existing_records),
    )
    for identifier, record in sorted(existing_records.items()):
        rebuilt = observation_records.get(identifier)
        if rebuilt is None:
            observation_records[identifier] = dict(record)
            continue
        rebuilt_first = rebuilt.get("first_seen_at")
        existing_first = record.get("first_seen_at")
        rebuilt["first_seen_at"] = min(
            (value for value in (rebuilt_first, existing_first) if isinstance(value, str)),
            default=None,
        )
        rebuilt_last = rebuilt.get("last_seen_at")
        existing_last = record.get("last_seen_at")
        rebuilt["last_seen_at"] = max(
            (value for value in (rebuilt_last, existing_last) if isinstance(value, str)),
            default=None,
        )
        if isinstance(existing_last, str) and (
            not isinstance(rebuilt_last, str) or existing_last > rebuilt_last
        ):
            for field_name in (
                "capture_mode",
                "fingerprint",
                "revision_id",
                "source_completeness",
                "source_is_truncated",
                "source_payload_sha256",
            ):
                rebuilt[field_name] = record.get(field_name)
    event_records = _event_records_from_observations(observation_records, analyzed_events)
    public_observation_records = {
        identifier: record
        for identifier, record in observation_records.items()
        if bool(record.get("active", True))
    }
    public_event_records = _event_records_from_observations(
        public_observation_records,
        analyzed_events,
    )

    internal_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for identifier, record in sorted(observation_records.items()):
        internal_buckets[_bucket_for_id(identifier, resolved.shard_count)].append(record)
    internal_refs: list[dict[str, Any]] = []
    internal_paths: set[Path] = set()
    for number in range(resolved.shard_count):
        bucket = f"{number:02x}"
        payload = _json_bytes(
            {
                "bucket": bucket,
                "observations": internal_buckets.get(bucket, []),
                "version": LINEAGE_VERSION,
            }
        )
        if _secret_match(payload):
            raise LineageValidationError("secret-like value detected in internal lineage registry")
        relative = Path("registry") / f"{bucket}.json"
        target = internal_dir / relative
        _atomic_write(target, payload)
        internal_paths.add(target.resolve())
        internal_refs.append(
            {
                "bucket": bucket,
                "bytes": len(payload),
                "path": relative.as_posix(),
                "sha256": "sha256:" + sha256_hex(payload),
            }
        )
    internal_index = _json_bytes(
        {
            "bucket_algorithm": BUCKET_ALGORITHM,
            "bucket_count": resolved.shard_count,
            "generated_at": generated_at,
            "registry_buckets": internal_refs,
            "schema": "lineage_registry_v1",
            "stats": {"events": len(event_records), "observations": len(observation_records)},
            "version": LINEAGE_VERSION,
        }
    )
    _atomic_write(internal_dir / "index.json", internal_index)
    internal_paths.add((internal_dir / "index.json").resolve())

    route_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for identifier, record in sorted(public_observation_records.items()):
        route_buckets[_bucket_for_id(identifier, resolved.shard_count)].append(
            {
                "event_id": record["event_id"],
                "observation_id": identifier,
            }
        )
    cluster_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event_id, event in sorted(public_event_records.items()):
        members = sorted(
            (public_observation_records[identifier] for identifier in event["members"]),
            key=lambda record: (
                record["source_published_at"] or record["first_seen_at"] or "9999",
                record["observation_id"],
            ),
        )
        representative = public_observation_records[event["representative_observation_id"]]
        lineage_links: list[dict[str, Any]] = []
        for member in members:
            parent_id = member.get("parent_observation_id")
            if not isinstance(parent_id, str):
                continue
            parent = public_observation_records.get(parent_id)
            if parent is None or parent.get("event_id") == event_id:
                continue
            lineage_links.append(
                {
                    "from_observation_id": member["observation_id"],
                    "relation": member["relation"],
                    "target": _public_observation(parent),
                }
            )
        lineage_links.sort(
            key=lambda item: (
                item["from_observation_id"],
                item["target"]["observation_id"],
            )
        )
        cluster_buckets[_bucket_for_id(event_id, resolved.shard_count)].append(
            {
                "earliest_observed_id": event["earliest_observed_id"],
                "event_aliases": event["event_aliases"],
                "event_id": event_id,
                "lineage_links": lineage_links[:6],
                "observations": [_public_observation(member) for member in members],
                "probable_origin_id": event["probable_origin_id"],
                "representative_article_url": representative["article_url"],
            }
        )
    route_refs, public_paths = _write_content_addressed_shards(
        public_dir=public_dir,
        directory="routes",
        field_name="routes",
        buckets=route_buckets,
        config=resolved,
    )
    cluster_refs, cluster_paths = _write_content_addressed_shards(
        public_dir=public_dir,
        directory="clusters",
        field_name="clusters",
        buckets=cluster_buckets,
        config=resolved,
    )
    public_paths.update(cluster_paths)
    relation_counts = Counter(
        record["relation"] for record in public_observation_records.values()
    )
    stats = {
        "derivatives": relation_counts[RelationKind.DERIVATIVE.value],
        "events": len(public_event_records),
        "exact_copies": relation_counts[RelationKind.EXACT_COPY.value],
        "observations": len(public_observation_records),
        "related_only": relation_counts[RelationKind.RELATED_ONLY.value],
        "same_event": relation_counts[RelationKind.SAME_EVENT.value],
        "syndicated": relation_counts[RelationKind.SYNDICATED.value],
    }
    public_index = _json_bytes(
        {
            "bucket_algorithm": BUCKET_ALGORITHM,
            "bucket_count": resolved.shard_count,
            "cluster_buckets": cluster_refs,
            "generated_at": generated_at,
            "route_buckets": route_refs,
            "schema": LINEAGE_SCHEMA,
            "stats": stats,
            "version": LINEAGE_VERSION,
        }
    )
    if len(public_index) > resolved.index_max_bytes:
        raise LineageValidationError("public lineage index exceeds size limit")
    if _secret_match(public_index) or any(
        _secret_match(path.read_bytes()) for path in public_paths
    ):
        raise LineageValidationError("secret-like value detected in public lineage assets")
    _atomic_write(public_dir / "index.json", public_index)
    public_paths.add((public_dir / "index.json").resolve())

    for root, keep in ((internal_dir, internal_paths), (public_dir, public_paths)):
        if root.exists():
            for stale in sorted(root.rglob("*.json")):
                if stale.resolve() not in keep:
                    stale.unlink()
    report = verify_lineage_assets(
        public_dir,
        internal_dir=internal_dir,
        verify_hashes=True,
        config=resolved,
    )
    return {
        "events": report["events"],
        "generated_at": generated_at,
        "observations": report["observations"],
        "public_files": report["public_files"],
        "schema": LINEAGE_SCHEMA,
    }


def _safe_asset_path(root: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise LineageValidationError("invalid lineage asset path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise LineageValidationError("lineage asset path escapes its root")
    lexical_root = root.absolute()
    lexical_target = lexical_root / relative
    current = lexical_target
    while True:
        if current.is_symlink():
            raise LineageValidationError("lineage asset path contains a symlink")
        if current == lexical_root:
            break
        if lexical_root not in current.parents:
            raise LineageValidationError("lineage asset path escapes its root")
        current = current.parent
    target = lexical_target.resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise LineageValidationError("lineage asset path escapes its root") from exc
    return target


def verify_lineage_assets(
    public_dir: Path,
    *,
    internal_dir: Path | None = None,
    verify_hashes: bool = False,
    config: LineageConfig | None = None,
) -> dict[str, Any]:
    resolved = config or LineageConfig()
    index_path = public_dir / "index.json"
    if not index_path.is_file():
        raise LineageValidationError("lineage index is missing")
    index_bytes = index_path.read_bytes()
    if len(index_bytes) > resolved.index_max_bytes:
        raise LineageValidationError("lineage index exceeds size limit")
    if _secret_match(index_bytes):
        raise LineageValidationError("secret-like value detected in lineage index")
    try:
        index = json.loads(index_bytes)
    except json.JSONDecodeError as exc:
        raise LineageValidationError("lineage index is invalid JSON") from exc
    if index.get("schema") != LINEAGE_SCHEMA or index.get("version") != LINEAGE_VERSION:
        raise LineageValidationError("unsupported lineage index schema")
    if index.get("bucket_algorithm") != BUCKET_ALGORITHM:
        raise LineageValidationError("unsupported lineage bucket algorithm")
    bucket_count = index.get("bucket_count")
    if bucket_count != resolved.shard_count:
        raise LineageValidationError("lineage bucket count does not match policy")
    route_refs = index.get("route_buckets")
    cluster_refs = index.get("cluster_buckets")
    if not isinstance(route_refs, list) or not isinstance(cluster_refs, list):
        raise LineageValidationError("lineage index shard references are invalid")
    if len(route_refs) != bucket_count or len(cluster_refs) != bucket_count:
        raise LineageValidationError("lineage index must reference every deterministic bucket")
    expected_buckets = {f"{value:02x}" for value in range(bucket_count)}
    route_count = 0
    events: set[str] = set()
    observations: set[str] = set()
    referenced_paths: set[Path] = {index_path.resolve()}
    total_bytes = len(index_bytes)
    for refs, field_name in ((route_refs, "routes"), (cluster_refs, "clusters")):
        seen_buckets: set[str] = set()
        for reference in refs:
            if not isinstance(reference, dict):
                raise LineageValidationError("lineage shard reference must be an object")
            bucket = reference.get("bucket")
            if bucket not in expected_buckets or bucket in seen_buckets:
                raise LineageValidationError("lineage shard bucket is invalid or duplicated")
            seen_buckets.add(bucket)
            target = _safe_asset_path(public_dir, reference.get("path"))
            if not target.is_file():
                raise LineageValidationError(f"referenced lineage shard is missing: {target}")
            payload = target.read_bytes()
            referenced_paths.add(target.resolve())
            total_bytes += len(payload)
            if len(payload) > resolved.shard_max_bytes:
                raise LineageValidationError("referenced lineage shard exceeds size limit")
            if _secret_match(payload):
                raise LineageValidationError("secret-like value detected in lineage shard")
            if verify_hashes:
                actual = "sha256:" + sha256_hex(payload)
                if reference.get("sha256") != actual:
                    raise LineageValidationError("lineage shard hash does not match index")
            if reference.get("bytes") != len(payload):
                raise LineageValidationError("lineage shard byte count does not match index")
            try:
                shard = json.loads(payload)
            except json.JSONDecodeError as exc:
                raise LineageValidationError("lineage shard is invalid JSON") from exc
            if shard.get("version") != LINEAGE_VERSION or shard.get("bucket") != bucket:
                raise LineageValidationError("lineage shard metadata does not match index")
            values = shard.get(field_name)
            if not isinstance(values, list):
                raise LineageValidationError(f"lineage shard has no {field_name} list")
            if field_name == "routes":
                route_count += len(values)
                for route in values:
                    observation_id = route.get("observation_id")
                    event_id = route.get("event_id")
                    if _bucket_for_id(observation_id, bucket_count) != bucket:
                        raise LineageValidationError("route is stored in the wrong bucket")
                    observations.add(observation_id)
                    if not re.fullmatch(r"evt_[0-9a-f]{64}", str(event_id)):
                        raise LineageValidationError("route has invalid event_id")
            else:
                for cluster in values:
                    event_id = cluster.get("event_id")
                    if _bucket_for_id(event_id, bucket_count) != bucket:
                        raise LineageValidationError("cluster is stored in the wrong bucket")
                    events.add(event_id)
                    timeline = cluster.get("observations")
                    if not isinstance(timeline, list) or not timeline:
                        raise LineageValidationError("cluster timeline must not be empty")
                    timeline_ids = {
                        item.get("observation_id")
                        for item in timeline
                        if isinstance(item, Mapping)
                    }
                    for item in timeline:
                        if item.get("relation") not in {kind.value for kind in RelationKind}:
                            raise LineageValidationError("cluster contains an invalid relation")
                        if "source_text" in item or "fingerprint" in item:
                            raise LineageValidationError("public cluster leaks source evidence")
                    lineage_links = cluster.get("lineage_links")
                    if not isinstance(lineage_links, list) or len(lineage_links) > 6:
                        raise LineageValidationError("cluster lineage links are invalid")
                    for link in lineage_links:
                        if not isinstance(link, Mapping):
                            raise LineageValidationError("cluster lineage link must be an object")
                        if set(link) != {"from_observation_id", "relation", "target"}:
                            raise LineageValidationError("cluster lineage link fields are invalid")
                        if link.get("from_observation_id") not in timeline_ids:
                            raise LineageValidationError("cluster lineage link source is missing")
                        if link.get("relation") not in {
                            RelationKind.DERIVATIVE.value,
                            RelationKind.SAME_EVENT.value,
                            RelationKind.RELATED_ONLY.value,
                        }:
                            raise LineageValidationError("cluster lineage link relation is invalid")
                        target_observation = link.get("target")
                        if not isinstance(target_observation, Mapping):
                            raise LineageValidationError("cluster lineage target is invalid")
                        if "source_text" in target_observation or "fingerprint" in target_observation:
                            raise LineageValidationError("public lineage link leaks source evidence")
    actual_public = {path.resolve() for path in public_dir.rglob("*.json") if path.is_file()}
    if actual_public != referenced_paths:
        raise LineageValidationError("public lineage directory contains unreferenced JSON assets")
    if len(actual_public) > resolved.public_max_files:
        raise LineageValidationError("public lineage asset count exceeds limit")
    if total_bytes > resolved.public_max_bytes:
        raise LineageValidationError("public lineage assets exceed total size limit")
    stats = index.get("stats")
    if not isinstance(stats, dict):
        raise LineageValidationError("lineage stats are missing")
    if route_count != stats.get("observations") or len(observations) != route_count:
        raise LineageValidationError("lineage observation stats do not match routes")
    if len(events) != stats.get("events"):
        raise LineageValidationError("lineage event stats do not match clusters")

    if internal_dir is not None:
        internal_index_path = internal_dir / "index.json"
        if not internal_index_path.is_file():
            raise LineageValidationError("internal lineage registry index is missing")
        internal_index = json.loads(internal_index_path.read_text(encoding="utf-8"))
        refs = internal_index.get("registry_buckets")
        if not isinstance(refs, list) or len(refs) != bucket_count:
            raise LineageValidationError("internal lineage registry must have 128 buckets")
        internal_observations = 0
        active_internal_observations = 0
        for reference in refs:
            target = _safe_asset_path(internal_dir, reference.get("path"))
            payload = target.read_bytes()
            if _secret_match(payload):
                raise LineageValidationError("secret-like value detected in internal registry")
            if reference.get("bytes") != len(payload):
                raise LineageValidationError("internal lineage shard byte count mismatch")
            if verify_hashes and reference.get("sha256") != "sha256:" + sha256_hex(payload):
                raise LineageValidationError("internal lineage shard hash mismatch")
            shard = json.loads(payload)
            records = shard.get("observations")
            if not isinstance(records, list):
                raise LineageValidationError("internal registry shard has no observations")
            internal_observations += len(records)
            for record in records:
                if "source_text" in record or "normalized_text" in record:
                    raise LineageValidationError("internal registry leaks source evidence")
                _fingerprint_from_record(record)
                if bool(record.get("active", True)):
                    active_internal_observations += 1
        if active_internal_observations != route_count:
            raise LineageValidationError("internal and public observation counts diverge")
    return {
        "events": len(events),
        "observations": route_count,
        "public_bytes": total_bytes,
        "public_files": len(referenced_paths),
        "valid": True,
    }


__all__ = [
    "BUCKET_ALGORITHM",
    "DEFAULT_CONFIG_PATH",
    "LINEAGE_SCHEMA",
    "BatchResolution",
    "CircuitBreakerResult",
    "Fingerprint",
    "LineageConfig",
    "LineageRegistry",
    "LineageValidationError",
    "ObservationInput",
    "RelationKind",
    "RelationshipDecision",
    "ResolutionItem",
    "TimestampConfidence",
    "apply_lineage_post_metadata",
    "apply_suppression_circuit_breaker",
    "build_lineage_assets",
    "build_shingles",
    "classify_relationship",
    "fingerprint_text",
    "lineage_bucket",
    "load_lineage_config",
    "make_lineage_event_id",
    "make_lineage_revision_id",
    "make_observation_id",
    "normalize_source_text",
    "observation_from_contract",
    "parse_historical_post",
    "verify_lineage_assets",
]
