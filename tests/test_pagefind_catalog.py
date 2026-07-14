from __future__ import annotations

import gzip
import hashlib
import json
import os
import zipfile
from pathlib import Path
from typing import Any

import pytest

from ai_stack import pagefind_catalog
from ai_stack.pagefind_catalog import (
    CatalogBasis,
    CatalogRecord,
    PagefindCatalogError,
    convert_pagefind_fragments,
    main,
    make_catalog_payload,
    verify_catalog_artifact,
)

CODE_SHA = "a" * 40
CONTENT_SHA = "b" * 40
FRAGMENT_ID = "zh-cn_123abcd"


def _release_id(*, code_sha: str = CODE_SHA, content_sha: str = CONTENT_SHA) -> str:
    identity = json.dumps(
        {
            "code_sha": code_sha,
            "content_sha": content_sha,
            "release_seq": 7,
            "schema_version": "1.0",
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return "r-" + hashlib.sha256(identity).hexdigest()[:24]


def _write_release_basis(root: Path, *, release_id: str | None = None) -> Path:
    path = root / "build-handoff/state/release-basis.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "basis_schema_version": "release_basis_v1",
                "release_id": release_id or _release_id(),
                "code_sha": CODE_SHA,
                "content_sha": CONTENT_SHA,
                "schema_version": "1.0",
                "release_seq": 7,
                "generated_at": "2026-07-13T08:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    return path


def _fragment_payload(
    *,
    url: str = "/posts/safe/",
    title: str = "安全标题",
    source: str = "arxiv",
    date: str = "2026-07-13",
    content: str = "第一句。\u200b第二句。 <script>只应作为文本</script>",
) -> dict[str, Any]:
    return {
        "url": url,
        "content": content,
        "meta": {"title": title, "source": source, "date": date},
        "filters": {"source": [source], "date": [date]},
        "anchors": [],
        "word_count": 10,
    }


def _write_fragment(
    public_root: Path,
    *,
    fragment_id: str = FRAGMENT_ID,
    payload: dict[str, Any] | None = None,
    raw: bytes | None = None,
) -> Path:
    directory = public_root / "pagefind/fragment"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{fragment_id}.pf_fragment"
    if raw is None:
        encoded = json.dumps(payload or _fragment_payload(), ensure_ascii=False).encode()
        raw = gzip.compress(b"pagefind_dcd" + encoded, compresslevel=9, mtime=0)
    path.write_bytes(raw)
    return path


def test_converts_complete_catalog_binds_basis_then_removes_only_fragments(
    tmp_path: Path,
) -> None:
    public = tmp_path / "public"
    fragment = _write_fragment(public)
    basis_path = _write_release_basis(tmp_path)
    keep = public / "pagefind/index/zh-cn_test.pf_index"
    keep.parent.mkdir(parents=True)
    keep.write_bytes(b"index")

    report = convert_pagefind_fragments(public, release_basis_path=basis_path)

    catalog_path = public / "pagefind/catalog.json"
    manifest_path = public / "pagefind/catalog.manifest.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert report.record_count == 1
    assert not fragment.parent.exists()
    assert keep.read_bytes() == b"index"
    assert list((public / "pagefind").rglob("*.pf_fragment")) == []
    assert catalog["schema_version"] == "pagefind_result_catalog_v1"
    assert catalog["record_count"] == 1
    assert catalog["source_fragment_tree_sha256"] == report.source_fragment_tree_sha256
    assert catalog["basis"] == {
        "basis_schema_version": "release_basis_v1",
        "code_sha": CODE_SHA,
        "content_sha": CONTENT_SHA,
        "generated_at": "2026-07-13T08:00:00Z",
        "release_basis_sha256": report.release_basis_sha256,
        "release_seq": 7,
        "schema_version": "1.0",
    }
    assert "release_id" not in json.dumps(catalog, sort_keys=True)
    assert catalog["records"][FRAGMENT_ID] == {
        "date": "2026-07-13",
        "source": "arxiv",
        "summary": "第一句。第二句。 <script>只应作为文本</script>",
        "title": "安全标题",
        "url": "/posts/safe/",
    }
    assert manifest["catalog_sha256"] == hashlib.sha256(catalog_path.read_bytes()).hexdigest()
    assert manifest["catalog_gzip_bytes"] <= 1024 * 1024
    assert verify_catalog_artifact(catalog_path, manifest_path) == report


def test_accepts_pagefind_hashes_extended_after_a_short_hash_collision(
    tmp_path: Path,
) -> None:
    public = tmp_path / "public"
    extended_id = "zh-cn_123abcde"
    _write_fragment(public, fragment_id=extended_id)

    convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)

    catalog = json.loads((public / "pagefind/catalog.json").read_text(encoding="utf-8"))
    assert extended_id in catalog["records"]


@pytest.mark.parametrize(
    "url",
    [
        "https://evil.example/post/",
        "//evil.example/post/",
        "javascript:alert(1)",
        "data:text/html,boom",
        "/safe\\@evil.example/post/",
        "/safe/\u0000post/",
    ],
)
def test_rejects_dangerous_urls_without_deleting_source(tmp_path: Path, url: str) -> None:
    public = tmp_path / "public"
    fragment = _write_fragment(public, payload=_fragment_payload(url=url))

    with pytest.raises(PagefindCatalogError, match="URL"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)

    assert fragment.exists()
    assert not (public / "pagefind/catalog.json").exists()


def test_rejects_gzip_bomb_before_json_parse_and_keeps_fragments(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    public = tmp_path / "public"
    monkeypatch.setattr(pagefind_catalog, "MAX_FRAGMENT_UNCOMPRESSED_BYTES", 128)
    fragment = _write_fragment(
        public,
        payload=_fragment_payload(content="x" * 10_000),
    )

    with pytest.raises(PagefindCatalogError, match="decompressed size"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)

    assert fragment.exists()


def test_rejects_zip_or_trailing_gzip_members_and_keeps_fragments(tmp_path: Path) -> None:
    public = tmp_path / "public"
    archive = tmp_path / "payload.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        zipped.writestr("fragment.json", "{}")
    fragment = _write_fragment(public, raw=archive.read_bytes())

    with pytest.raises(PagefindCatalogError, match="gzip"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert fragment.exists()

    fragment.write_bytes(
        gzip.compress(b"pagefind_dcd{}", mtime=0)
        + gzip.compress(b"pagefind_dcd{}", mtime=0)
    )
    with pytest.raises(PagefindCatalogError, match="single gzip member"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert fragment.exists()


@pytest.mark.parametrize("link_kind", ["symlink", "hardlink"])
def test_rejects_linked_fragments_without_deletion(tmp_path: Path, link_kind: str) -> None:
    public = tmp_path / "public"
    target = _write_fragment(public)
    linked = target.with_name("zh-cn_7654321.pf_fragment")
    if link_kind == "symlink":
        linked.symlink_to(target)
    else:
        os.link(target, linked)

    with pytest.raises(PagefindCatalogError, match="link|regular"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)

    assert target.exists()
    assert linked.exists()


def test_rejects_invalid_and_duplicate_ids(tmp_path: Path) -> None:
    public = tmp_path / "public"
    invalid = _write_fragment(public, fragment_id="unsafe")

    with pytest.raises(PagefindCatalogError, match="fragment ID"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert invalid.exists()

    basis = CatalogBasis.repository(code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    duplicate = CatalogRecord(
        fragment_id=FRAGMENT_ID,
        url="/safe/",
        title="title",
        source="arxiv",
        date="2026-07-13",
        summary="summary",
    )
    with pytest.raises(PagefindCatalogError, match="duplicate fragment ID"):
        make_catalog_payload(
            [duplicate, duplicate],
            basis=basis,
            source_fragment_tree_sha256="c" * 64,
        )


def test_enforces_file_count_compressed_and_catalog_gzip_limits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    public = tmp_path / "count/public"
    first = _write_fragment(public)
    _write_fragment(public, fragment_id="zh-cn_7654321")
    monkeypatch.setattr(pagefind_catalog, "MAX_FRAGMENT_COUNT", 1)
    with pytest.raises(PagefindCatalogError, match="fragment count"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert first.exists()

    public = tmp_path / "compressed/public"
    compressed = _write_fragment(public)
    monkeypatch.setattr(pagefind_catalog, "MAX_FRAGMENT_COUNT", 20_000)
    monkeypatch.setattr(pagefind_catalog, "MAX_FRAGMENT_COMPRESSED_BYTES", 8)
    with pytest.raises(PagefindCatalogError, match="compressed size"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert compressed.exists()

    public = tmp_path / "catalog/public"
    catalog_fragment = _write_fragment(public)
    monkeypatch.setattr(pagefind_catalog, "MAX_FRAGMENT_COMPRESSED_BYTES", 1024 * 1024)
    monkeypatch.setattr(pagefind_catalog, "MAX_CATALOG_GZIP_BYTES", 8)
    with pytest.raises(PagefindCatalogError, match="catalog gzip size"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert catalog_fragment.exists()


def test_output_failure_and_invalid_release_basis_never_delete_fragments(tmp_path: Path) -> None:
    public = tmp_path / "output/public"
    fragment = _write_fragment(public)
    (public / "pagefind/catalog.json").mkdir()
    with pytest.raises(PagefindCatalogError, match="catalog output"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert fragment.exists()

    public = tmp_path / "basis/public"
    fragment = _write_fragment(public)
    forged = _write_release_basis(tmp_path / "basis", release_id="r-" + "0" * 24)
    with pytest.raises(PagefindCatalogError, match="release basis"):
        convert_pagefind_fragments(public, release_basis_path=forged)
    assert fragment.exists()


def test_catalog_manifest_detects_tampering(tmp_path: Path) -> None:
    public = tmp_path / "public"
    _write_fragment(public)
    report = convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    catalog_path = public / "pagefind/catalog.json"
    manifest_path = public / "pagefind/catalog.manifest.json"
    assert verify_catalog_artifact(catalog_path, manifest_path) == report

    catalog_path.write_bytes(catalog_path.read_bytes() + b"\n")
    with pytest.raises(PagefindCatalogError, match="digest"):
        verify_catalog_artifact(catalog_path, manifest_path)


def test_long_summary_is_truncated_to_a_canonical_safe_boundary(tmp_path: Path) -> None:
    public = tmp_path / "public"
    _write_fragment(public, payload=_fragment_payload(content="word " * 1_000))

    report = convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)

    catalog = json.loads((public / "pagefind/catalog.json").read_text(encoding="utf-8"))
    summary = catalog["records"][FRAGMENT_ID]["summary"]
    assert report.record_count == 1
    assert len(summary) <= pagefind_catalog.SUMMARY_CODEPOINTS
    assert summary == summary.strip()
    assert "\u200b" not in summary


def test_rejects_release_basis_symlinks_and_fragments_outside_canonical_directory(
    tmp_path: Path,
) -> None:
    public = tmp_path / "public"
    fragment = _write_fragment(public)
    outside = public / "pagefind/unexpected.pf_fragment"
    outside.write_bytes(fragment.read_bytes())
    with pytest.raises(PagefindCatalogError, match="canonical fragment directory"):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert fragment.exists() and outside.exists()

    outside.unlink()
    basis = _write_release_basis(tmp_path)
    linked_basis = tmp_path / "linked-basis.json"
    linked_basis.symlink_to(basis)
    with pytest.raises(PagefindCatalogError, match="release basis"):
        convert_pagefind_fragments(public, release_basis_path=linked_basis)
    assert fragment.exists()


def test_cli_and_automatic_repository_basis_are_executable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    public = tmp_path / "cli/public"
    _write_fragment(public)
    assert main(
        [
            "--public-root",
            str(public),
            "--code-sha",
            CODE_SHA,
            "--content-sha",
            CONTENT_SHA,
        ]
    ) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["code_sha"] == CODE_SHA
    assert output["record_count"] == 1

    public = tmp_path / "auto/public"
    _write_fragment(public)
    monkeypatch.setattr(pagefind_catalog, "_git_head", lambda _directory: CODE_SHA)
    report = convert_pagefind_fragments(public)
    assert report.code_sha == CODE_SHA
    assert report.content_sha == CODE_SHA


def test_catalog_basis_rejects_invalid_schema_and_cross_mode_fields() -> None:
    with pytest.raises(PagefindCatalogError, match="basis schema"):
        CatalogBasis("unknown", CODE_SHA, CONTENT_SHA)
    with pytest.raises(PagefindCatalogError, match="release-only"):
        CatalogBasis(
            pagefind_catalog.REPOSITORY_BASIS_SCHEMA_VERSION,
            CODE_SHA,
            CONTENT_SHA,
            schema_version="1.0",
        )
    with pytest.raises(PagefindCatalogError, match="schema_version"):
        CatalogBasis(
            pagefind_catalog.RELEASE_BASIS_SCHEMA_VERSION,
            CODE_SHA,
            CONTENT_SHA,
            schema_version="latest",
            release_seq=1,
            generated_at="2026-07-13T08:00:00Z",
            release_basis_sha256="c" * 64,
        )
    with pytest.raises(PagefindCatalogError, match="repository catalog basis fields"):
        CatalogBasis.from_mapping(
            {
                "basis_schema_version": pagefind_catalog.REPOSITORY_BASIS_SCHEMA_VERSION,
                "code_sha": CODE_SHA,
                "content_sha": CONTENT_SHA,
                "unexpected": True,
            }
        )


def test_release_basis_must_match_explicit_code_and_content_shas(tmp_path: Path) -> None:
    basis = _write_release_basis(tmp_path)
    public = tmp_path / "matching/public"
    _write_fragment(public)
    report = convert_pagefind_fragments(
        public,
        release_basis_path=basis,
        code_sha=CODE_SHA,
        content_sha=CONTENT_SHA,
    )
    assert report.release_basis_sha256 is not None

    public = tmp_path / "code/public"
    fragment = _write_fragment(public)
    with pytest.raises(PagefindCatalogError, match="code_sha does not match"):
        convert_pagefind_fragments(
            public,
            release_basis_path=basis,
            code_sha="c" * 40,
            content_sha=CONTENT_SHA,
        )
    assert fragment.exists()

    with pytest.raises(PagefindCatalogError, match="content_sha does not match"):
        convert_pagefind_fragments(
            public,
            release_basis_path=basis,
            code_sha=CODE_SHA,
            content_sha="d" * 40,
        )
    assert fragment.exists()


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        (gzip.compress(b"wrong_prefix{}", mtime=0), "Pagefind prefix"),
        (
            gzip.compress(
                b'pagefind_dcd{"url":"/one/","url":"/two/","meta":{}}',
                mtime=0,
            ),
            "duplicate JSON key",
        ),
        (gzip.compress(b"pagefind_dcd{", mtime=0), "invalid JSON"),
    ],
)
def test_rejects_invalid_fragment_envelopes_without_deletion(
    tmp_path: Path, raw: bytes, message: str
) -> None:
    public = tmp_path / message.replace(" ", "_") / "public"
    fragment = _write_fragment(public, raw=raw)
    with pytest.raises(PagefindCatalogError, match=message):
        convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    assert fragment.exists()


def test_manifest_field_tampering_is_rejected(tmp_path: Path) -> None:
    public = tmp_path / "public"
    _write_fragment(public)
    convert_pagefind_fragments(public, code_sha=CODE_SHA, content_sha=CONTENT_SHA)
    catalog_path = public / "pagefind/catalog.json"
    manifest_path = public / "pagefind/catalog.manifest.json"
    original = json.loads(manifest_path.read_text(encoding="utf-8"))
    mutations = [
        ("schema_version", "unknown", "fields or schema"),
        ("catalog_sha256", "0" * 64, "digest"),
        ("catalog_bytes", original["catalog_bytes"] + 1, "byte count"),
        ("catalog_gzip_bytes", original["catalog_gzip_bytes"] + 1, "gzip size"),
        ("source_fragment_tree_sha256", "0" * 64, "fragment tree digest"),
        ("record_count", original["record_count"] + 1, "record count"),
    ]
    for field_name, value, message in mutations:
        changed = dict(original)
        changed[field_name] = value
        manifest_path.write_text(json.dumps(changed), encoding="utf-8")
        with pytest.raises(PagefindCatalogError, match=message):
            verify_catalog_artifact(catalog_path, manifest_path)
