from __future__ import annotations

import json
import urllib.error
from datetime import UTC, datetime
from pathlib import Path

import pytest

from scripts import verify_content_freshness

NOW = datetime(2026, 7, 15, 4, 0, tzinfo=UTC)


def _index(
    *,
    generated_at: str = "2026-07-15T03:00:00Z",
    version: object = 2,
    total_articles: object = 42,
) -> dict[str, object]:
    return {
        "version": version,
        "generated_at": generated_at,
        "stats": {"total_articles": total_articles},
    }


def _write_index(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_validate_index_accepts_fresh_v2_metadata() -> None:
    result = verify_content_freshness.validate_index(
        _index(),
        source="local",
        now=NOW,
        max_age_hours=2,
    )

    assert result == {
        "source": "local",
        "status": "ok",
        "version": 2,
        "generated_at": "2026-07-15T03:00:00Z",
        "age_hours": 1.0,
        "total_articles": 42,
    }


@pytest.mark.parametrize(
    ("payload", "reason"),
    [
        (_index(version=1), "version"),
        (_index(generated_at="2026-07-15T03:00:00"), "RFC3339"),
        (_index(generated_at="not-a-date"), "RFC3339"),
        (_index(total_articles=0), "total_articles"),
        (_index(total_articles=True), "total_articles"),
        ({"version": 2, "generated_at": "2026-07-15T03:00:00Z"}, "stats"),
    ],
)
def test_validate_index_fails_closed_on_invalid_contract(
    payload: dict[str, object],
    reason: str,
) -> None:
    with pytest.raises(verify_content_freshness.FreshnessError, match=reason):
        verify_content_freshness.validate_index(
            payload,
            source="local",
            now=NOW,
            max_age_hours=2,
        )


def test_validate_index_fails_closed_when_stale_or_from_the_future() -> None:
    with pytest.raises(verify_content_freshness.FreshnessError, match="stale"):
        verify_content_freshness.validate_index(
            _index(generated_at="2026-07-15T01:59:59Z"),
            source="local",
            now=NOW,
            max_age_hours=2,
        )

    with pytest.raises(verify_content_freshness.FreshnessError, match="future"):
        verify_content_freshness.validate_index(
            _index(generated_at="2026-07-15T04:00:01Z"),
            source="live",
            now=NOW,
            max_age_hours=2,
        )


def test_validate_index_requires_explicit_aware_now_and_positive_max_age() -> None:
    with pytest.raises(verify_content_freshness.FreshnessError, match="now"):
        verify_content_freshness.validate_index(
            _index(),
            source="local",
            now=datetime(2026, 7, 15, 4, 0),
            max_age_hours=2,
        )

    with pytest.raises(verify_content_freshness.FreshnessError, match="max_age_hours"):
        verify_content_freshness.validate_index(
            _index(),
            source="local",
            now=NOW,
            max_age_hours=0,
        )


def test_cli_checks_local_and_live_independently_and_writes_summary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    local_index = tmp_path / "index.json"
    summary = tmp_path / "summary.md"
    _write_index(local_index, _index())
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    monkeypatch.setattr(
        verify_content_freshness,
        "load_live_index",
        lambda _url: _index(generated_at="2026-07-15T02:30:00+00:00", total_articles=43),
    )

    exit_code = verify_content_freshness.main(
        [
            "--local-index",
            str(local_index),
            "--live-index-url",
            "https://example.test/data/tag-graph/index.json",
            "--max-age-hours",
            "2",
        ],
        now=NOW,
    )

    report = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert report["status"] == "ok"
    assert [check["source"] for check in report["checks"]] == ["local", "live"]
    assert "Content freshness: ok" in summary.read_text(encoding="utf-8")
    assert "local: ok" in summary.read_text(encoding="utf-8")
    assert "live: ok" in summary.read_text(encoding="utf-8")


def test_cli_returns_nonzero_for_local_staleness(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    local_index = tmp_path / "index.json"
    _write_index(local_index, _index(generated_at="2026-07-15T00:00:00Z"))

    exit_code = verify_content_freshness.main(
        [
            "--local-index",
            str(local_index),
            "--max-age-hours",
            "2",
        ],
        now=NOW,
    )

    report = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert report["status"] == "error"
    assert report["checks"][0]["source"] == "local"
    assert report["checks"][0]["status"] == "error"
    assert "stale" in report["checks"][0]["error"]


@pytest.mark.parametrize(
    "live_failure",
    [
        verify_content_freshness.FreshnessError("live: network error"),
        verify_content_freshness.FreshnessError("live: invalid JSON"),
    ],
)
def test_cli_returns_nonzero_for_live_network_or_json_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    live_failure: Exception,
) -> None:
    local_index = tmp_path / "index.json"
    _write_index(local_index, _index())

    def fail_live(_url: str) -> dict[str, object]:
        raise live_failure

    monkeypatch.setattr(verify_content_freshness, "load_live_index", fail_live)

    exit_code = verify_content_freshness.main(
        [
            "--local-index",
            str(local_index),
            "--live-index-url",
            "https://example.test/data/tag-graph/index.json",
            "--max-age-hours",
            "2",
        ],
        now=NOW,
    )

    report = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert report["status"] == "error"
    assert report["checks"][0]["status"] == "ok"
    assert report["checks"][1]["source"] == "live"
    assert report["checks"][1]["status"] == "error"


def test_load_local_index_fails_closed_on_missing_or_invalid_json(tmp_path: Path) -> None:
    with pytest.raises(verify_content_freshness.FreshnessError, match="local"):
        verify_content_freshness.load_local_index(tmp_path / "missing.json")

    invalid = tmp_path / "invalid.json"
    invalid.write_text("{", encoding="utf-8")
    with pytest.raises(verify_content_freshness.FreshnessError, match="JSON"):
        verify_content_freshness.load_local_index(invalid)


def test_load_live_index_reads_json_and_fails_closed_on_transport_or_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Response:
        def __init__(self, body: bytes):
            self.body = body

        def __enter__(self) -> Response:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self, _limit: int) -> bytes:
            return self.body

    monkeypatch.setattr(
        verify_content_freshness.urllib.request,
        "urlopen",
        lambda _request, timeout: Response(json.dumps(_index()).encode("utf-8")),
    )
    assert verify_content_freshness.load_live_index("https://example.test/index.json") == _index()

    monkeypatch.setattr(
        verify_content_freshness.urllib.request,
        "urlopen",
        lambda _request, timeout: Response(b"{"),
    )
    with pytest.raises(verify_content_freshness.FreshnessError, match="JSON"):
        verify_content_freshness.load_live_index("https://example.test/index.json")

    def network_error(_request: object, timeout: int) -> object:
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(verify_content_freshness.urllib.request, "urlopen", network_error)
    with pytest.raises(verify_content_freshness.FreshnessError, match="network"):
        verify_content_freshness.load_live_index("https://example.test/index.json")

    with pytest.raises(verify_content_freshness.FreshnessError, match="http or https"):
        verify_content_freshness.load_live_index("file:///tmp/index.json")
