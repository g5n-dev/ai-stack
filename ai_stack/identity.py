from __future__ import annotations

import posixpath
import re
import unicodedata
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from ._json import canonical_json_bytes, sha256_hex


CANONICALIZATION_VERSION = "url-v1"
_TRACKING_PARAMETERS = {
    "dclid",
    "fbclid",
    "gclid",
    "igshid",
    "mc_cid",
    "mc_eid",
    "msclkid",
    "ref_src",
}


def _normalized_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).strip().split()).casefold()


def canonicalize_url(url: str, *, version: str = CANONICALIZATION_VERSION) -> str:
    if version != CANONICALIZATION_VERSION:
        raise ValueError(f"unsupported canonicalization version: {version}")
    if not isinstance(url, str) or not url.strip() or len(url) > 4096:
        raise ValueError("URL must be a non-empty string no longer than 4096 characters")

    parsed = urlsplit(url.strip())
    scheme = parsed.scheme.casefold()
    if scheme not in {"http", "https"}:
        raise ValueError("only http and https URLs are supported")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URLs containing credentials are not allowed")
    if not parsed.hostname:
        raise ValueError("URL must include a host")

    try:
        hostname = parsed.hostname.encode("idna").decode("ascii").casefold()
        port = parsed.port
    except (UnicodeError, ValueError) as error:
        raise ValueError("URL contains an invalid host or port") from error
    host = f"[{hostname}]" if ":" in hostname else hostname
    if port is not None and not (
        (scheme == "http" and port == 80) or (scheme == "https" and port == 443)
    ):
        host = f"{host}:{port}"

    raw_path = re.sub(r"/{2,}", "/", parsed.path or "/")
    path = posixpath.normpath(raw_path)
    if not path.startswith("/"):
        path = "/" + path
    if path == "/":
        path = ""

    query_parts = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        folded = key.casefold()
        if folded.startswith("utm_") or folded in _TRACKING_PARAMETERS:
            continue
        query_parts.append((key, value))
    query_parts.sort(key=lambda pair: (pair[0], pair[1]))
    query = urlencode(query_parts, doseq=True)
    return urlunsplit((scheme, host, path, query, ""))


def _stable_id(prefix: str, payload: Any) -> str:
    return f"{prefix}_{sha256_hex(canonical_json_bytes(payload))}"


def make_item_id(
    source: str,
    native_id: str | None,
    canonical_url: str,
    *,
    canonicalization_version: str = CANONICALIZATION_VERSION,
) -> str:
    source_key = _normalized_text(source)
    if not source_key:
        raise ValueError("source must not be empty")
    identity = native_id.strip() if native_id and native_id.strip() else canonicalize_url(
        canonical_url, version=canonicalization_version
    )
    return _stable_id(
        "itm",
        {
            "canonicalization_version": canonicalization_version,
            "identity": identity,
            "source": source_key,
        },
    )


def make_revision_id(item_id: str, normalized_payload: Any) -> str:
    return _stable_id("rev", {"item_id": item_id, "payload": normalized_payload})


def make_generation_key(
    revision_id: str, model: str, prompt_version: str, policy_version: str
) -> str:
    return _stable_id(
        "gen",
        {
            "model": model,
            "policy_version": policy_version,
            "prompt_version": prompt_version,
            "revision_id": revision_id,
        },
    )


def make_article_revision_id(generation_key: str, generated_payload: Any) -> str:
    return _stable_id(
        "art", {"generated_payload": generated_payload, "generation_key": generation_key}
    )


def make_entity_id(kind: str, canonical_name: str) -> str:
    kind_key = _normalized_text(kind)
    name_key = _normalized_text(canonical_name)
    if not kind_key or not name_key:
        raise ValueError("entity kind and canonical name must not be empty")
    return _stable_id("ent", {"kind": kind_key, "name": name_key})


def make_event_id(seed_item_id: str) -> str:
    if not seed_item_id.strip():
        raise ValueError("event seed item must not be empty")
    return _stable_id("evt", {"seed_item_id": seed_item_id.strip()})


def make_evidence_id(
    source_url: str, snapshot_digest: str, locator: str, excerpt: str
) -> str:
    return _stable_id(
        "evd",
        {
            "excerpt": excerpt,
            "locator": locator,
            "snapshot_digest": snapshot_digest,
            "source_url": canonicalize_url(source_url),
        },
    )
