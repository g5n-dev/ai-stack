"""Conservative secret and privacy gates for text that will become public."""

from __future__ import annotations

import ipaddress
import re
import unicodedata

_CREDENTIAL_TOKEN_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
_CREDENTIAL_ASSIGNMENT = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|auth(?:orization)?|credential|"
    r"password|secret|token)\b\s*[:=]\s*[\"']?"
    r"(?P<value>[A-Za-z0-9][A-Za-z0-9_./+@=-]{15,})"
)
_OBVIOUS_PLACEHOLDER = re.compile(
    r"(?i)(?:example|placeholder|replace[_-]?me|your[_-]|sample|dummy|"
    r"x{8,}|\*{8,}|<[^>]+>|\$\{[^}]+\})"
)
_EMAIL_ADDRESS = re.compile(
    r"(?i)(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]{1,64}"
    r"@[A-Za-z0-9.-]{1,190}\.[A-Za-z]{2,24}(?![A-Za-z0-9.-])"
)
_USER_HOME_PATH = re.compile(
    r"(?:^|[\s\"'`])(?:/(?:Users|home)/[^\s\"'`]+|"
    r"[A-Za-z]:\\Users\\[^\s\"'`]+)",
    re.IGNORECASE,
)
_IPV4_CANDIDATE = re.compile(
    r"(?<![0-9.])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9.])"
)
_IPV6_CANDIDATE = re.compile(
    r"(?<![0-9A-Fa-f:])(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}"
    r"(?![0-9A-Fa-f:])"
)
_NON_PUBLIC_NETWORKS = tuple(
    ipaddress.ip_network(value)
    for value in (
        "10.0.0.0/8",
        "100.64.0.0/10",
        "127.0.0.0/8",
        "169.254.0.0/16",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "::1/128",
        "fc00::/7",
        "fe80::/10",
    )
)


def sensitive_publication_reasons(value: object) -> tuple[str, ...]:
    """Return stable reason codes without ever returning the matched value."""

    text = unicodedata.normalize("NFC", str(value or ""))
    reasons: set[str] = set()
    if any(pattern.search(text) for pattern in _CREDENTIAL_TOKEN_PATTERNS):
        reasons.add("credential_token")
    for match in _CREDENTIAL_ASSIGNMENT.finditer(text):
        if _OBVIOUS_PLACEHOLDER.search(match.group("value")) is None:
            reasons.add("credential_assignment")
            break
    if _EMAIL_ADDRESS.search(text):
        reasons.add("email_address")
    if _USER_HOME_PATH.search(text):
        reasons.add("user_home_path")
    for candidate in (*_IPV4_CANDIDATE.findall(text), *_IPV6_CANDIDATE.findall(text)):
        try:
            address = ipaddress.ip_address(candidate)
        except ValueError:
            continue
        if any(
            address.version == network.version and address in network
            for network in _NON_PUBLIC_NETWORKS
        ):
            reasons.add("private_network_address")
            break
    return tuple(sorted(reasons))


__all__ = ["sensitive_publication_reasons"]
