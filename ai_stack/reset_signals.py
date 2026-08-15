"""Deterministic classification for Codex usage-limit reset signals.

The classifier deliberately reports a signal state, not a calibrated event
probability.  It separates an explicit reset, a future commitment, a weak
precursor, and missing evidence so downstream code never turns silence into a
negative prediction.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping
from typing import Literal, TypedDict

ResetKind = Literal[
    "hard_reset",
    "banked_reset",
    "temp_boost",
    "policy_change",
    "forecast_signal",
    "irrelevant",
]
ResetStatus = Literal[
    "confirmed",
    "promised",
    "watch",
    "negated",
    "insufficient_evidence",
]


class ResetSignal(TypedDict):
    monitor: str
    kind: ResetKind
    status: ResetStatus
    products: list[str]
    plans: list[str]
    horizon: str
    confidence: float
    evidence: list[str]
    reason: str
    notify: bool


_RESET_RE = re.compile(r"\breset(?:s|ting|ted)?\b", re.IGNORECASE)
_QUOTA_RESET_SCOPE_RE = re.compile(
    r"(?:\b(?:usage|rate|weekly|hourly)\s*[- ]?limits?\b|"
    r"\b(?:limit|quota)\s+reset\b|"
    r"\breset\b[^.!?;\n]{0,32}\b(?:codex|chatgpt\s+work)\b|"
    r"\b(?:codex|chatgpt\s+work)\b[^.!?;\n]{0,32}\breset\b|"
    r"/fast\b)",
    re.IGNORECASE,
)
_EXPLICIT_LIMIT_SCOPE_RE = re.compile(
    r"\b(?:usage|rate|weekly|hourly)\s*[- ]?limits?\b",
    re.IGNORECASE,
)
_USER_QUOTA_OWNER_RE = re.compile(
    r"\b(?:codex|chatgpt\s+work|paid\s+(?:users?|plans?)|"
    r"user\s+accounts?|plus|pro|business|enterprise)\b",
    re.IGNORECASE,
)
_NON_QUOTA_RESET_TARGET_RE = re.compile(
    r"\b(?:password|passcode|credential|demo|tutorial|view|layout|"
    r"conversation|chat\s+history|session|device|factory\s+settings?|"
    r"database|cache|repository|repo|test|build|server|game|economy|"
    r"deployment|cluster)\b",
    re.IGNORECASE,
)
_CLAUSE_RE = re.compile(r"[^.!?;\n]+(?:[.!?;]|$)")
_SHORT_NO_RE = re.compile(r"^(?:no|nope)[.!]?$", re.IGNORECASE)
_NEGATED_RESET_RE = re.compile(
    r"\b(?:there\s+(?:will|is)\s+be\s+no\b[^.!?\n]{0,48}|"
    r"no\s+(?:codex\s+|usage[-\s]+limit\s+)?|"
    r"won['’]?t\s+(?:be\s+)?|will\s+not\s+|not\s+going\s+to\s+)"
    r"reset(?:s|ting|ted)?\b",
    re.IGNORECASE,
)
_FUTURE_RESET_RE = re.compile(
    r"(?:\b(?:i(?:'|’)ll|we(?:'|’)ll|i\s+will|we\s+will|will|going\s+to)\b"
    r"[^.!?\n]{0,48}\breset\b|"
    r"\breset\b[^.!?\n]{0,48}\b(?:incoming|tomorrow|later\s+(?:today|in\s+the\s+day)|"
    r"on\s+monday|this\s+evening|within\s+(?:the\s+)?(?:next\s+)?(?:hour|few\s+hours)|"
    r"next\s+(?:hour|few\s+hours))\b|"
    r"\b(?:landing|propagating)\b[^.!?\n]{0,40}\b(?:hour|minutes?|today)\b)",
    re.IGNORECASE,
)
_CONFIRMED_RESET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(?:i|we)\s+(?:have|'ve|’ve)\s+reset\b", re.IGNORECASE),
    re.compile(
        r"\b(?:(?:codex|chatgpt\s+work)\s+)?"
        r"(?:(?:usage|rate|weekly|hourly)\s+)?limits?\s+"
        r"(?:have|has)\s+(?:now\s+)?been\s+reset\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:(?:codex|chatgpt\s+work)\s+)?"
        r"(?:(?:usage|rate|weekly|hourly)\s+)?limits?\s+"
        r"(?:are|is|were)\s+(?:now\s+)?reset\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:(?:codex|chatgpt\s+work)\s+)?"
        r"(?:usage|rate|weekly|hourly)\s+limits?\s+(?:now\s+)?reset\b",
        re.IGNORECASE,
    ),
    re.compile(r"\breset\s+button\s+(?:has\s+been\s+)?pressed\b", re.IGNORECASE),
    re.compile(r"\benjoy\s+(?:a\s+|another\s+|a\s+nice\s+|a\s+full\s+)?reset\b", re.IGNORECASE),
)
_HINT_RESET_RE = re.compile(
    r"(?:\bfeeling\s+like\b[^.!?\n]{0,40}\breset\b|"
    r"\b(?:might|may|could|maybe)\b[^.!?\n]{0,40}\breset\b|"
    r"\bresets?\s+will\s+continue\b|"
    r"\byou\s+know\s+what\s+comes\s+next\b)",
    re.IGNORECASE,
)
_TEMP_BOOST_RE = re.compile(
    r"(?:(?:\b2\s*[x×](?!\w)|\bdouble(?:d)?\b|\btwice\b)"
    r"[^.!?;\n]{0,48}\b(?:usage|rate|weekly|hourly)\s*[- ]?limits?\b|"
    r"\b(?:usage|rate|weekly|hourly)\s*[- ]?limits?\b"
    r"[^.!?;\n]{0,48}(?:\b2\s*[x×](?!\w)|\bdouble(?:d)?\b|\btwice\b)|"
    r"\blift(?:ed|ing)?\b[^.!?;\n]{0,30}\busage\s+limits?\b)",
    re.IGNORECASE,
)
_POLICY_CHANGE_RE = re.compile(
    r"(?:\b(?:remove(?:d)?|restore(?:d)?|pause(?:d)?|resume(?:d)?)\b"
    r"[^.!?\n]{0,36}\b(?:5\s*h|five[-\s]+hour|rate\s+limit)\b|"
    r"\b(?:5\s*h|five[-\s]+hour)\b[^.!?\n]{0,36}\b(?:limit|restriction)\b)",
    re.IGNORECASE,
)
_INCIDENT_PRECURSOR_RE = re.compile(
    r"\b(?:back\s+and\s+stable|recover(?:ed|y)|mitigat(?:ed|ion)|fix(?:ed)?|"
    r"resolv(?:ed|ing)|root\s+caused|rolled\s+back)\b",
    re.IGNORECASE,
)
_INCIDENT_CONTEXT_RE = re.compile(
    r"\b(?:outage|incident|disruption|reliability|drain(?:ed|ing)?|slowdown|"
    r"blocked|rejected|limit|limits)\b",
    re.IGNORECASE,
)
_MILESTONE_PRECURSOR_RE = re.compile(
    r"(?:\b\d+\s*m\b|\bmillion\b|\bactive\s+users?\b|\bcrossed\b[^.!?\n]{0,20}\b\d+\s*m\b)",
    re.IGNORECASE,
)
_MILESTONE_CONTEXT_RE = re.compile(
    r"\b(?:celebrat(?:e|ing|ion)|surprise|milestone|enjoy|weekend)\b",
    re.IGNORECASE,
)
_PERSONAL_RESET_RE = re.compile(
    r"\b(?:theo|he|she|him|her|myself|yourself)\b[^.!?\n]{0,32}\breset\b",
    re.IGNORECASE,
)


def _normalize(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or ""))
    text = text.replace("’", "'")
    return re.sub(r"\s+", " ", text).strip()


def _products(text: str) -> list[str]:
    products: list[str] = []
    if re.search(r"\bcodex\b", text, re.IGNORECASE):
        products.append("Codex")
    if re.search(r"\bchatgpt\s+work\b", text, re.IGNORECASE):
        products.append("ChatGPT Work")
    return products


def _plans(text: str) -> list[str]:
    labels = (
        ("all_paid", r"\b(?:all\s+)?paid\s+(?:users?|plans?|subscriptions?)\b"),
        ("Plus", r"\bplus\b"),
        ("Pro", r"\bpro\b"),
        ("Business", r"\bbusiness\b"),
        ("Enterprise", r"\benterprise\b"),
    )
    return [label for label, pattern in labels if re.search(pattern, text, re.IGNORECASE)]


def _horizon(text: str, *, default: str = "unknown") -> str:
    patterns = (
        ("next_30_minutes", r"\b(?:next|within)\s+(?:the\s+)?30\s+minutes?\b"),
        ("next_hour", r"\b(?:next|within)\s+(?:the\s+)?(?:next\s+)?hour\b"),
        ("next_few_hours", r"\b(?:next|within)\s+(?:the\s+)?(?:next\s+)?few\s+hours\b"),
        ("tomorrow", r"\btomorrow\b"),
        ("monday", r"\b(?:on\s+)?monday\b"),
        ("later_today", r"\blater\s+(?:today|in\s+the\s+day)\b"),
        ("today", r"\btoday\b"),
        ("weekend", r"\bweekend\b"),
    )
    for label, pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return label
    return default


def _matched(pattern: re.Pattern[str], text: str) -> list[str]:
    match = pattern.search(text)
    return [match.group(0).strip()] if match is not None else []


def _clauses(text: str) -> list[str]:
    return [match.group(0).strip() for match in _CLAUSE_RE.finditer(text) if match.group(0).strip()]


def _is_question(clause: str) -> bool:
    return clause.rstrip().endswith("?")


def _has_disqualifying_reset_target(clause: str) -> bool:
    return bool(
        _NON_QUOTA_RESET_TARGET_RE.search(clause)
        and not (
            _EXPLICIT_LIMIT_SCOPE_RE.search(clause)
            and _USER_QUOTA_OWNER_RE.search(clause)
        )
    )


def _has_quota_reset_scope(text: str) -> bool:
    for clause in _clauses(text):
        if (
            _RESET_RE.search(clause)
            and _QUOTA_RESET_SCOPE_RE.search(clause)
            and not _has_disqualifying_reset_target(clause)
        ):
            return True
    return False


def _scoped_reset_clauses(text: str) -> list[str]:
    return [
        clause
        for clause in _clauses(text)
        if _RESET_RE.search(clause)
        and _QUOTA_RESET_SCOPE_RE.search(clause)
        and not _has_disqualifying_reset_target(clause)
    ]


def _result(
    *,
    kind: ResetKind,
    status: ResetStatus,
    text: str,
    confidence: float,
    evidence: list[str],
    reason: str,
    horizon: str = "unknown",
) -> ResetSignal:
    notify = kind in {"hard_reset", "banked_reset"} and status in {
        "confirmed",
        "promised",
    }
    return {
        "monitor": "codex_usage_reset",
        "kind": kind,
        "status": status,
        "products": _products(text),
        "plans": _plans(text),
        "horizon": horizon,
        "confidence": round(max(0.0, min(1.0, confidence)), 2),
        "evidence": evidence[:5],
        "reason": reason,
        "notify": notify,
    }


def classify_reset_signal(text: object, *, context: object = "") -> ResetSignal:
    """Classify one public post about Codex/ChatGPT Work usage limits.

    ``confidence`` describes confidence in the textual classification.  It is
    intentionally not presented as the probability that a future reset will
    happen.  Missing evidence stays ``insufficient_evidence`` instead of being
    converted into a negative forecast.
    """

    current = _normalize(text)
    parent = _normalize(context)
    combined = " ".join(part for part in (parent, current) if part)
    if not combined:
        return _result(
            kind="irrelevant",
            status="insufficient_evidence",
            text="",
            confidence=0.0,
            evidence=[],
            reason="没有可用于判断的文本证据",
        )

    current_reset_clauses = _scoped_reset_clauses(current)
    parent_has_reset_scope = _has_quota_reset_scope(parent)
    embedded_reset_request = bool(
        re.search(
            r"\bit\s+is\s+done\b[^\n]{0,240}"
            r"\b(?:what\s+about|our)\b[^\n]{0,40}\breset\b",
            current,
            re.IGNORECASE,
        )
        and not _has_disqualifying_reset_target(current)
    )

    if (
        _SHORT_NO_RE.fullmatch(current)
        and parent_has_reset_scope
        and any(_is_question(clause) for clause in _clauses(parent))
    ):
        return _result(
            kind="hard_reset",
            status="negated",
            text=combined,
            confidence=0.92,
            evidence=[current],
            reason="作者以简短否定回复了明确的额度重置问题",
        )

    contextual_done = bool(
        re.search(r"\bit\s+is\s+done\b", current, re.IGNORECASE)
        and (parent_has_reset_scope or embedded_reset_request)
    )
    if contextual_done:
        return _result(
            kind="hard_reset",
            status="confirmed",
            text=combined,
            confidence=0.94,
            evidence=["It is done"],
            reason="作者以完成态回复了明确的额度重置问题",
            horizon="already_announced",
        )

    negated_match = next(
        (
            match
            for clause in current_reset_clauses
            if not _is_question(clause)
            for match in [_NEGATED_RESET_RE.search(clause)]
            if match is not None
        ),
        None,
    )
    if negated_match is not None:
        return _result(
            kind="hard_reset",
            status="negated",
            text=combined,
            confidence=0.96,
            evidence=[negated_match.group(0).strip()],
            reason="作者正文明确否定额度重置",
            horizon=_horizon(current),
        )

    banked = re.search(r"\b(?:banked\s+reset|reset\s+bank)\b", current, re.IGNORECASE)
    if banked is not None:
        containing_clause = next(
            (clause for clause in _clauses(current) if banked.group(0) in clause),
            current,
        )
        account_delivery = bool(
            re.search(
                r"\b(?:add(?:ed)?|issu(?:e|ed)|credit(?:ed)?|grant(?:ed)?)\b"
                r"[^.!?;\n]{0,48}\b(?:every|all)\s+(?:codex\s+)?accounts?\b",
                containing_clause,
                re.IGNORECASE,
            )
        )
        if (
            _is_question(containing_clause)
            or _has_disqualifying_reset_target(containing_clause)
            or not (_has_quota_reset_scope(containing_clause) or account_delivery)
        ):
            banked = None
    if banked is not None:
        future = _FUTURE_RESET_RE.search(containing_clause) is not None
        return _result(
            kind="banked_reset",
            status="promised" if future else "confirmed",
            text=combined,
            confidence=0.98 if not future else 0.92,
            evidence=[banked.group(0)],
            reason="文本指向可手动兑换的 banked reset，而非自动全局重置",
            horizon=_horizon(
                current,
                default="unknown" if future else "already_announced",
            ),
        )

    future_match: re.Match[str] | None = None
    for clause in _clauses(current):
        if _is_question(clause) or _has_disqualifying_reset_target(clause):
            continue
        candidate = _FUTURE_RESET_RE.search(clause)
        if candidate is not None and (
            _has_quota_reset_scope(clause)
            or re.search(r"\bperformative\s+reset\b", clause, re.IGNORECASE)
        ):
            future_match = candidate
            break
    if future_match is None:
        celebratory_reset = re.search(
            r"\benjoy\s+(?:a\s+|another\s+|a\s+nice\s+|a\s+full\s+)?reset\b",
            current,
            re.IGNORECASE,
        )
        propagation = re.search(
            r"\b(?:landing|propagating)\b[^.!?\n]{0,40}\b(?:hour|minutes?|today)\b",
            current,
            re.IGNORECASE,
        )
        if celebratory_reset is not None and propagation is not None:
            future_match = propagation
    if future_match is not None:
        return _result(
            kind="hard_reset",
            status="promised",
            text=combined,
            confidence=0.92,
            evidence=[future_match.group(0)],
            reason="文本给出了未来重置承诺或生效窗口",
            horizon=_horizon(current),
        )

    confirmed_evidence: list[str] = []
    for clause in current_reset_clauses:
        if _is_question(clause):
            continue
        for pattern in _CONFIRMED_RESET_PATTERNS:
            confirmed_evidence.extend(_matched(pattern, clause))
    if confirmed_evidence:
        return _result(
            kind="hard_reset",
            status="confirmed",
            text=combined,
            confidence=0.99,
            evidence=confirmed_evidence,
            reason="文本明确声明额度已经重置",
            horizon=_horizon(current, default="already_announced"),
        )

    if _TEMP_BOOST_RE.search(current):
        match = _TEMP_BOOST_RE.search(current)
        assert match is not None
        return _result(
            kind="temp_boost",
            status="confirmed",
            text=combined,
            confidence=0.98,
            evidence=[match.group(0)],
            reason="文本只说明临时额度提升，不等于 hard reset",
            horizon=_horizon(current),
        )

    if _POLICY_CHANGE_RE.search(current) and re.search(
        r"\b(?:codex|chatgpt\s+work|usage|rate\s+limit)\b",
        current,
        re.IGNORECASE,
    ):
        match = _POLICY_CHANGE_RE.search(current)
        assert match is not None
        return _result(
            kind="policy_change",
            status="confirmed",
            text=combined,
            confidence=0.98,
            evidence=[match.group(0)],
            reason="文本说明限额策略变化，不等于全局额度重置",
            horizon=_horizon(current),
        )

    hint = next(
        (
            match
            for clause in current_reset_clauses
            if not _is_question(clause)
            for match in [_HINT_RESET_RE.search(clause)]
            if match is not None
        ),
        None,
    )
    if hint is not None and not (
        _PERSONAL_RESET_RE.search(current) and not current_reset_clauses
    ):
        return _result(
            kind="forecast_signal",
            status="watch",
            text=combined,
            confidence=0.72,
            evidence=[hint.group(0)],
            reason="文本含重置暗示，但没有形成可核验承诺",
            horizon=_horizon(current),
        )

    incident_signal = bool(
        re.search(r"\bcodex\b", current, re.IGNORECASE)
        and _INCIDENT_PRECURSOR_RE.search(current)
        and _INCIDENT_CONTEXT_RE.search(current)
    )
    milestone_signal = bool(
        re.search(r"\bcodex\b", current, re.IGNORECASE)
        and _MILESTONE_PRECURSOR_RE.search(current)
        and _MILESTONE_CONTEXT_RE.search(current)
    )
    if incident_signal or milestone_signal:
        evidence: list[str] = []
        if incident_signal:
            evidence.extend(_matched(_INCIDENT_PRECURSOR_RE, current))
            evidence.extend(_matched(_INCIDENT_CONTEXT_RE, current))
        if milestone_signal:
            evidence.extend(_matched(_MILESTONE_PRECURSOR_RE, current))
            evidence.extend(_matched(_MILESTONE_CONTEXT_RE, current))
        return _result(
            kind="forecast_signal",
            status="watch",
            text=combined,
            confidence=0.64,
            evidence=evidence,
            reason="事故恢复或用户里程碑属于历史前兆，但不是重置承诺",
            horizon=_horizon(current),
        )

    return _result(
        kind="irrelevant",
        status="insufficient_evidence",
        text=combined,
        confidence=0.0,
        evidence=[],
        reason="没有足够证据判断是否会发生额度重置",
    )


def signal_title_prefix(signal: Mapping[str, object]) -> str:
    """Return a compact, non-probabilistic label for a classified post."""

    kind = str(signal.get("kind") or "")
    status = str(signal.get("status") or "")
    labels = {
        ("hard_reset", "confirmed"): "[额度已重置]",
        ("hard_reset", "promised"): "[额度重置已预告]",
        ("hard_reset", "negated"): "[额度重置被否定]",
        ("banked_reset", "confirmed"): "[已发放重置卡]",
        ("banked_reset", "promised"): "[重置卡已预告]",
        ("temp_boost", "confirmed"): "[临时额度提升]",
        ("policy_change", "confirmed"): "[额度政策变化]",
        ("forecast_signal", "watch"): "[额度重置观察]",
    }
    return labels.get((kind, status), "")


__all__ = ["ResetSignal", "classify_reset_signal", "signal_title_prefix"]
