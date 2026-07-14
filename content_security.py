"""Fail-closed validation for generated public content.

The crawler and language model output are untrusted.  This module deliberately
validates at two different boundaries:

* Markdown/front matter before it is persisted or handed to Hugo.
* The rendered ``.post-content`` DOM before the site artifact is published.

It does not attempt to turn arbitrary HTML into safe HTML.  Public posts are a
Markdown-only format; active content is rejected so that a validator failure can
never silently widen the publishing policy.
"""

from __future__ import annotations

import html
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, NoReturn, cast
from urllib.parse import unquote, urlsplit

import yaml
from bs4 import BeautifulSoup, Tag

MAX_DOCUMENT_BYTES = 2 * 1024 * 1024
MAX_FRONTMATTER_BYTES = 64 * 1024
MAX_NESTED_VALUES = 10_000

_SHORTCODE_RE = re.compile(r"\{\{\s*[<%]", re.IGNORECASE)
_FENCED_CODE_RE = re.compile(r"(?ms)^\s*(```|~~~).*?^\s*\1\s*$")
_INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
_MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))", re.IGNORECASE)
_REFERENCE_LINK_RE = re.compile(r"(?m)^[ \t]{0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|([^\s]+))")
_AUTOLINK_RE = re.compile(r"<((?:https?://|mailto:)[^<>\s]+)>", re.IGNORECASE)
_RAW_HTML_RE = re.compile(r"(?is)<!--|<\s*/?\s*[a-z][a-z0-9-]*\b(?:[^>'\"]|'[^']*'|\"[^\"]*\")*>")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
_YAML_TAG_OR_ALIAS_RE = re.compile(
    r"(?m)(?:^|[\s\[{,])(?:!!|![A-Za-z]|&[A-Za-z0-9_-]+|\*[A-Za-z0-9_-]+)"
)
_URL_KEY_RE = re.compile(r"(?:^|_)(?:url|uri|link|image)$", re.IGNORECASE)

_BLOCKED_DOM_TAGS = {
    "applet",
    "base",
    "embed",
    "form",
    "frame",
    "frameset",
    "iframe",
    "link",
    "math",
    "meta",
    "object",
    "script",
    "style",
    "svg",
    "template",
}
_URL_ATTRIBUTES = {
    "action",
    "background",
    "cite",
    "data",
    "formaction",
    "href",
    "longdesc",
    "poster",
    "src",
    "xlink:href",
}


@dataclass(frozen=True, slots=True)
class SecurityFinding:
    """A machine-readable reason why public content was rejected."""

    code: str
    message: str
    line: int | None = None


class ContentSecurityError(ValueError):
    """Raised when untrusted content cannot be proven safe for publication."""

    def __init__(self, findings: SecurityFinding | Sequence[SecurityFinding]):
        items: list[SecurityFinding]
        if isinstance(findings, SecurityFinding):
            items = [findings]
        else:
            items = list(findings)
        if not items:
            items.append(SecurityFinding("unknown", "content validation failed"))
        normalized = tuple(items)
        self.findings = normalized
        detail = "; ".join(
            f"{finding.code}: {finding.message}"
            + (f" (line {finding.line})" if finding.line is not None else "")
            for finding in normalized
        )
        super().__init__(detail)


@dataclass(frozen=True, slots=True)
class ValidatedMarkdown:
    """Parsed output returned only after every public-content guard passes."""

    frontmatter: Mapping[str, Any]
    body: str


def _reject(code: str, message: str, *, line: int | None = None) -> NoReturn:
    raise ContentSecurityError(SecurityFinding(code, message, line))


def _fully_decode_url(value: str) -> str:
    decoded = html.unescape(value).strip()
    for _ in range(3):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    return decoded


def validate_public_url(
    value: str,
    *,
    allow_relative: bool = False,
    allowed_schemes: Iterable[str] = ("http", "https"),
) -> str:
    """Return the original URL after strict scheme and control-char checks.

    Protocol-relative URLs are intentionally rejected: their destination is
    external while their scheme is inherited, which makes allow-list decisions
    ambiguous.  Encodings are decoded repeatedly before the scheme check to
    catch values such as ``java%73cript:``.
    """

    if not isinstance(value, str) or not value.strip():
        _reject("unsafe-url", "URL must be a non-empty string")
    if _CONTROL_RE.search(value):
        _reject("unsafe-url", "URL contains control characters")

    decoded = _fully_decode_url(value)
    if _CONTROL_RE.search(decoded) or any(char in decoded for char in ("\r", "\n", "\x00")):
        _reject("unsafe-url", "decoded URL contains control characters")
    if decoded.startswith("//"):
        _reject("unsafe-url", "protocol-relative URLs are not allowed")

    compact_prefix = re.sub(r"[\s\x00-\x1f\x7f]+", "", decoded.split("/", 1)[0]).lower()
    parsed = urlsplit(decoded)
    scheme = parsed.scheme.lower()
    allowed = {candidate.lower() for candidate in allowed_schemes}

    if scheme:
        if scheme not in allowed or compact_prefix.split(":", 1)[0] not in allowed:
            _reject("unsafe-url", f"URL scheme {scheme!r} is not allowed")
        if scheme in {"http", "https"} and not parsed.netloc:
            _reject("unsafe-url", "HTTP(S) URL must include a host")
        return value

    if not allow_relative:
        _reject("unsafe-url", "absolute HTTP(S) URL required")
    if ":" in compact_prefix:
        _reject("unsafe-url", "ambiguous relative URL contains a scheme delimiter")
    return value


def _mask_inert_markdown_code(body: str) -> str:
    def preserve_lines(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")

    masked = _FENCED_CODE_RE.sub(preserve_lines, body)
    return _INLINE_CODE_RE.sub("", masked)


def _split_frontmatter(document: str) -> tuple[str, str]:
    if not document.startswith("---\n"):
        _reject("frontmatter", "document must start with YAML frontmatter")
    end = re.search(r"(?m)^---[ \t]*\r?$", document[4:])
    if end is None:
        _reject("frontmatter", "frontmatter closing delimiter is missing")
    frontmatter_end = 4 + end.start()
    body_start = 4 + end.end()
    frontmatter = document[4:frontmatter_end]
    body = document[body_start:]
    if body.startswith("\r\n"):
        body = body[2:]
    elif body.startswith("\n"):
        body = body[1:]
    return frontmatter, body


def _load_unique_yaml(frontmatter: str) -> Mapping[str, Any]:
    if len(frontmatter.encode("utf-8")) > MAX_FRONTMATTER_BYTES:
        _reject("frontmatter", "frontmatter exceeds the 64 KiB limit")
    if _YAML_TAG_OR_ALIAS_RE.search(frontmatter):
        _reject("frontmatter", "YAML tags, anchors and aliases are not allowed")

    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(
        loader: UniqueKeyLoader,
        node: yaml.MappingNode,
        deep: bool = False,
    ) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "frontmatter mapping keys must be scalar values",
                    key_node.start_mark,
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"duplicate key: {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping,
    )
    try:
        loaded = yaml.load(frontmatter, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        _reject("frontmatter", f"invalid or ambiguous YAML: {exc}")

    if not isinstance(loaded, Mapping):
        _reject("frontmatter", "frontmatter must be a mapping")
    return cast(Mapping[str, Any], loaded)


def _walk_frontmatter(value: Any, *, key: str = "", seen: list[int] | None = None) -> None:
    counter = seen if seen is not None else [0]
    counter[0] += 1
    if counter[0] > MAX_NESTED_VALUES:
        _reject("frontmatter", "frontmatter contains too many values")

    if isinstance(value, Mapping):
        for child_key, child_value in value.items():
            if not isinstance(child_key, str) or not child_key.strip():
                _reject("frontmatter", "frontmatter keys must be non-empty strings")
            if _CONTROL_RE.search(child_key) or _SHORTCODE_RE.search(child_key):
                _reject("frontmatter", "frontmatter key contains active or control content")
            _walk_frontmatter(child_value, key=child_key, seen=counter)
        return
    if isinstance(value, list):
        for child in value:
            _walk_frontmatter(child, key=key, seen=counter)
        return
    if isinstance(value, str):
        if _CONTROL_RE.search(value):
            _reject("frontmatter", f"frontmatter field {key!r} contains control characters")
        if _SHORTCODE_RE.search(value) or _RAW_HTML_RE.search(_AUTOLINK_RE.sub("", value)):
            _reject("frontmatter", f"frontmatter field {key!r} contains active content")
        if _URL_KEY_RE.search(key) and value:
            validate_public_url(value, allow_relative=True)
        return
    if value is None or isinstance(value, (bool, int, float, date, datetime)):
        return
    _reject("frontmatter", f"frontmatter field {key!r} has unsupported type")


def _validate_markdown_body(body: str) -> None:
    if _SHORTCODE_RE.search(body):
        _reject("shortcode", "Hugo shortcodes are not allowed in generated content")

    active_body = _mask_inert_markdown_code(body)
    for link_re in (_MARKDOWN_LINK_RE, _REFERENCE_LINK_RE):
        for match in link_re.finditer(active_body):
            destination = match.group(1) or match.group(2) or ""
            try:
                validate_public_url(
                    destination,
                    allow_relative=True,
                    allowed_schemes=("http", "https", "mailto"),
                )
            except ContentSecurityError as exc:
                line = active_body.count("\n", 0, match.start()) + 1
                raise ContentSecurityError(
                    SecurityFinding("unsafe-url", str(exc), line=line)
                ) from exc

    for match in _AUTOLINK_RE.finditer(active_body):
        validate_public_url(
            match.group(1),
            allow_relative=False,
            allowed_schemes=("http", "https", "mailto"),
        )

    without_autolinks = _AUTOLINK_RE.sub("", active_body)
    raw_match = _RAW_HTML_RE.search(without_autolinks)
    if raw_match:
        line = without_autolinks.count("\n", 0, raw_match.start()) + 1
        _reject("raw-html", "raw HTML is not allowed in generated Markdown", line=line)


def validate_markdown_document(document: str) -> ValidatedMarkdown:
    """Validate one complete Hugo Markdown document and return parsed data."""

    if not isinstance(document, str):
        _reject("document", "Markdown document must be text")
    if len(document.encode("utf-8")) > MAX_DOCUMENT_BYTES:
        _reject("document", "Markdown document exceeds the 2 MiB limit")
    if _CONTROL_RE.search(document):
        _reject("document", "Markdown document contains control characters")

    frontmatter_text, body = _split_frontmatter(document)
    frontmatter = _load_unique_yaml(frontmatter_text)
    _walk_frontmatter(frontmatter)
    _validate_markdown_body(body)
    return ValidatedMarkdown(frontmatter=frontmatter, body=body)


def _iter_tags(roots: Sequence[Tag]) -> Iterable[Tag]:
    for root in roots:
        yield root
        yield from root.find_all(True)


def scan_rendered_html(html_text: str, *, content_selector: str | None = None) -> None:
    """Reject executable DOM in a fragment or selected rendered post bodies.

    When ``content_selector`` is supplied, scripts and metadata owned by the
    trusted site shell are outside this validator's boundary.  The complete site
    shell is separately constrained by the checked-in CSP and template tests.
    """

    if not isinstance(html_text, str) or len(html_text.encode("utf-8")) > 8 * MAX_DOCUMENT_BYTES:
        _reject("rendered-html", "rendered HTML is missing or exceeds 16 MiB")
    soup = BeautifulSoup(html_text, "html.parser")
    if content_selector:
        roots = [node for node in soup.select(content_selector) if isinstance(node, Tag)]
        if not roots:
            _reject(
                "rendered-html",
                f"required content selector {content_selector!r} was not found",
            )
    else:
        roots = [node for node in soup.find_all(True) if isinstance(node, Tag)]

    for tag in _iter_tags(roots):
        name = (tag.name or "").lower()
        if name in _BLOCKED_DOM_TAGS:
            _reject("blocked-dom-tag", f"rendered content contains blocked <{name}> element")

        for raw_name, raw_value in tag.attrs.items():
            attribute = str(raw_name).lower()
            values = raw_value if isinstance(raw_value, list) else [raw_value]
            value = " ".join(str(candidate) for candidate in values if candidate is not None)
            if attribute.startswith("on") or attribute in {"srcdoc", "xmlns", "formaction"}:
                _reject(
                    "blocked-dom-attribute",
                    f"rendered content contains blocked {attribute!r} attribute",
                )
            if attribute == "style" and re.search(
                r"(?i)(?:expression\s*\(|url\s*\(|@import|-moz-binding)", value
            ):
                _reject("blocked-dom-style", "rendered content contains an active style value")
            if attribute in _URL_ATTRIBUTES and value:
                validate_public_url(
                    value,
                    allow_relative=True,
                    allowed_schemes=("http", "https", "mailto"),
                )
            if attribute == "srcset":
                for candidate in value.split(","):
                    url = candidate.strip().split(maxsplit=1)[0] if candidate.strip() else ""
                    if url:
                        validate_public_url(url, allow_relative=True)
