from __future__ import annotations

import json
import stat
import threading
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

import pytest

from ai_stack._json import sha256_digest
from ai_stack.historical_capture_job import (
    BLOG_ALLOWLIST_SCHEMA,
    CAPTURE_AUDIT_SCHEMA,
    HistoricalCaptureJobError,
    load_blog_allowlist,
    load_blog_robots_policy,
    run_historical_capture_job,
    select_capture_targets,
)
from crawler.historical_source_fetch import (
    HistoricalSourceCapture,
    HistoricalSourceFetchError,
)
from scripts.capture_historical_sources import main


def _entry(
    path: str,
    source: str,
    canonical_url: str,
    locator: dict[str, object],
    *,
    classification: str = "needs_source_recovery",
    target_character: str = "a",
) -> dict[str, object]:
    return {
        "path": path,
        "target_sha256": target_character * 64,
        "source": source,
        "canonical_url": canonical_url,
        "current_status": "legacy_analysis",
        "current_mode": "legacy_analysis",
        "recovery_classification": classification,
        "source_locator": locator,
    }


def _inventory(entries: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema": "ai_stack.historical_rehydration.inventory",
        "version": 1,
        "offline": True,
        "entry_count": len(entries),
        "entries_sha256": sha256_digest(entries),
        "entries": entries,
    }


def _capture(target, *, text: str = "verified source evidence") -> HistoricalSourceCapture:
    return HistoricalSourceCapture(
        source=target.source,
        title=f"Captured {target.path}",
        external_url=target.canonical_url,
        source_text=text,
        captured_at="2026-07-18T02:03:04Z",
        capture_mode="metadata_only",
        source_completeness="metadata_only",
        source_is_truncated=False,
        metadata={"fixture": True},
    )


def test_selection_is_stable_and_applies_source_filter_and_limit() -> None:
    inventory = _inventory(
        [
            _entry(
                "z-github.md",
                "github_trending",
                "https://github.com/octo/repo",
                {"kind": "github", "status": "resolved", "owner": "octo", "repo": "repo"},
                target_character="b",
            ),
            _entry(
                "skip-verified.md",
                "arxiv",
                "https://arxiv.org/abs/2601.00003",
                {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00003"},
                classification="verified_rewrite",
                target_character="c",
            ),
            _entry(
                "skip-unresolved.md",
                "arxiv",
                "https://arxiv.org/abs/2601.00002",
                {"kind": "arxiv", "status": "arxiv_id_missing"},
                target_character="d",
            ),
            _entry(
                "a-arxiv.md",
                "arxiv",
                "https://arxiv.org/abs/2601.00001",
                {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00001"},
                target_character="e",
            ),
        ]
    )

    targets = select_capture_targets(
        inventory,
        sources={"arxiv", "github_trending"},
        filter_text=".md",
        limit=2,
    )

    assert [target.path for target in targets] == ["a-arxiv.md", "z-github.md"]


def test_all_supported_sources_dispatch_and_one_failure_does_not_abort_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    entries = [
        _entry(
            "01-arxiv.md",
            "arxiv",
            "https://arxiv.org/abs/2601.00001",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00001"},
            target_character="1",
        ),
        _entry(
            "02-github.md",
            "github_trending",
            "https://github.com/octo/repo",
            {"kind": "github", "status": "resolved", "owner": "octo", "repo": "repo"},
            target_character="2",
        ),
        _entry(
            "03-hn.md",
            "hacker_news",
            "https://example.com/story",
            {"kind": "hacker_news", "status": "resolved", "hn_id": "47158975"},
            target_character="3",
        ),
        _entry(
            "04-juejin.md",
            "juejin",
            "https://juejin.cn/post/7631425034263593014",
            {"kind": "juejin", "status": "resolved", "article_id": "7631425034263593014"},
            target_character="4",
        ),
        _entry(
            "05-blog.md",
            "blogs_podcasts",
            "https://blog.example/article",
            {"kind": "external_url", "status": "resolved"},
            target_character="5",
        ),
    ]
    calls: list[tuple[str, tuple[object, ...]]] = []

    def captured(source: str, url: str) -> HistoricalSourceCapture:
        return HistoricalSourceCapture(
            source=source,
            title="Verified title",
            external_url=url,
            source_text="bounded evidence",
            captured_at="2026-07-18T02:03:04Z",
            capture_mode="metadata_only",
            source_completeness="metadata_only",
            source_is_truncated=False,
            metadata={},
        )

    monkeypatch.setattr(
        job,
        "fetch_arxiv_sources",
        lambda identifiers, **kwargs: [
            (
                calls.append(("arxiv", (identifier,))),
                captured("arxiv", f"https://arxiv.org/abs/{identifier}"),
            )[1]
            for identifier in identifiers
        ],
    )
    monkeypatch.setattr(
        job,
        "fetch_github_source",
        lambda owner, repo, **kwargs: (
            calls.append(("github", (owner, repo))),
            captured("github_trending", f"https://github.com/{owner}/{repo}"),
        )[1],
    )

    def fail_hn(identifier: str, **kwargs) -> HistoricalSourceCapture:
        calls.append(("hacker_news", (identifier,)))
        raise HistoricalSourceFetchError("source_http_503")

    monkeypatch.setattr(job, "fetch_hacker_news_source", fail_hn)
    monkeypatch.setattr(
        job,
        "fetch_juejin_source_excerpt",
        lambda url, **kwargs: (
            calls.append(("juejin", (url, kwargs["discovery_title"]))),
            captured("juejin", url),
        )[1],
    )
    monkeypatch.setattr(
        job,
        "fetch_public_article_excerpt",
        lambda url, **kwargs: (
            calls.append(("blog", (url, tuple(sorted(kwargs["allowed_hosts"]))))),
            captured("blogs_podcasts", url),
        )[1],
    )

    audit = run_historical_capture_job(
        _inventory(entries),
        limit=10,
        blog_allowed_hosts={"blog.example"},
        concurrency=2,
        per_host_concurrency=1,
        timeout=3,
        robots_checker=lambda _url, _hosts, _timeout: True,
    )

    assert audit["schema"] == CAPTURE_AUDIT_SCHEMA
    assert audit["captured_count"] == 4
    assert audit["failed_count"] == 1
    assert [result["target_sha256"] for result in audit["results"]] == [
        character * 64 for character in "12345"
    ]
    hn = audit["results"][2]
    assert hn["status"] == "failed"
    assert hn["failure"] == {
        "type": "source_fetch_error",
        "reason": "source_http_503",
    }
    assert {name for name, _arguments in calls} == {
        "arxiv",
        "github",
        "hacker_news",
        "juejin",
        "blog",
    }


def test_resume_keeps_successful_evidence_and_retries_only_failures() -> None:
    entries = [
        _entry(
            "a.md",
            "arxiv",
            "https://arxiv.org/abs/2601.00001",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00001"},
            target_character="a",
        ),
        _entry(
            "b.md",
            "arxiv",
            "https://arxiv.org/abs/2601.00002",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00002"},
            target_character="b",
        ),
    ]
    first_calls: list[str] = []

    def first_dispatch(target, _hosts, _timeout):
        first_calls.append(target.path)
        if target.path == "b.md":
            raise HistoricalSourceFetchError("source_http_503")
        return _capture(target, text="retained evidence")

    first = run_historical_capture_job(
        _inventory(entries),
        limit=2,
        concurrency=1,
        per_host_concurrency=1,
        dispatcher=first_dispatch,
    )
    for result in first["results"]:
        result.pop("attempt_count")
    first["results_sha256"] = sha256_digest(first["results"])
    second_calls: list[str] = []

    def second_dispatch(target, _hosts, _timeout):
        second_calls.append(target.path)
        return _capture(target, text="recovered evidence")

    second = run_historical_capture_job(
        _inventory(entries),
        limit=2,
        concurrency=1,
        per_host_concurrency=1,
        resume_audit=first,
        dispatcher=second_dispatch,
    )

    assert first_calls == ["a.md", "b.md"]
    assert second_calls == ["b.md"]
    assert second["skipped_success_count"] == 1
    assert second["attempted_count"] == 1
    assert second["captured_count"] == 2
    assert second["results"][0]["capture"]["source_text"] == "retained evidence"
    assert [result["attempt_count"] for result in second["results"]] == [1, 2]


def test_attempted_at_is_run_stable_and_retry_refreshes_only_failed_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    entries = [
        _entry(
            "a.md",
            "arxiv",
            "https://arxiv.org/abs/2601.00001",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00001"},
            target_character="a",
        ),
        _entry(
            "b.md",
            "arxiv",
            "https://arxiv.org/abs/2601.00002",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00002"},
            target_character="b",
        ),
    ]
    timestamps = iter(
        (
            "2026-07-18T03:00:00Z",
            "2026-07-18T03:00:01Z",
            "2026-07-18T04:00:00+00:00",
            "2026-07-18T04:00:01+00:00",
        )
    )
    monkeypatch.setattr(job, "_now_iso", lambda: next(timestamps))

    def initial_dispatch(target, _hosts, _timeout):
        if target.path == "b.md":
            raise HistoricalSourceFetchError("source_http_503")
        return _capture(target)

    first = run_historical_capture_job(
        _inventory(entries),
        limit=2,
        concurrency=1,
        per_host_concurrency=1,
        dispatcher=initial_dispatch,
    )
    second = run_historical_capture_job(
        _inventory(entries),
        limit=2,
        concurrency=1,
        per_host_concurrency=1,
        resume_audit=first,
        dispatcher=lambda target, _hosts, _timeout: _capture(target),
    )

    assert [result["attempted_at"] for result in first["results"]] == [
        "2026-07-18T03:00:00Z",
        "2026-07-18T03:00:00Z",
    ]
    assert [result["attempted_at"] for result in second["results"]] == [
        "2026-07-18T03:00:00Z",
        "2026-07-18T04:00:00+00:00",
    ]
    for result in first["results"] + second["results"]:
        parsed = datetime.fromisoformat(result["attempted_at"].replace("Z", "+00:00"))
        assert parsed.utcoffset() is not None

    invalid_resume = json.loads(json.dumps(second))
    invalid_resume["results"][0]["attempted_at"] = "2026-07-18T03:00:00"
    invalid_resume["results_sha256"] = sha256_digest(invalid_resume["results"])
    monkeypatch.setattr(job, "_now_iso", lambda: "2026-07-18T05:00:00Z")
    with pytest.raises(HistoricalCaptureJobError, match="resume_audit_invalid"):
        run_historical_capture_job(
            _inventory(entries),
            limit=1,
            resume_audit=invalid_resume,
            dispatcher=lambda target, _hosts, _timeout: _capture(target),
        )


def test_resume_limit_advances_beyond_a_successful_prefix() -> None:
    entries = [
        _entry(
            f"{name}.md",
            "arxiv",
            f"https://arxiv.org/abs/2601.0000{index}",
            {
                "kind": "arxiv",
                "status": "resolved",
                "arxiv_id": f"2601.0000{index}",
            },
            target_character=name,
        )
        for index, name in enumerate(("a", "b", "c"), start=1)
    ]
    inventory = _inventory(entries)
    first = run_historical_capture_job(
        inventory,
        limit=2,
        concurrency=1,
        per_host_concurrency=1,
        dispatcher=lambda target, _hosts, _timeout: _capture(target),
    )
    calls: list[str] = []

    def dispatch(target, _hosts, _timeout):
        calls.append(target.path)
        return _capture(target)

    resumed = run_historical_capture_job(
        inventory,
        limit=1,
        concurrency=1,
        per_host_concurrency=1,
        resume_audit=first,
        dispatcher=dispatch,
    )

    assert calls == ["c.md"]
    assert resumed["attempted_count"] == 1
    assert resumed["skipped_success_count"] == 2
    assert resumed["captured_count"] == 3
    assert [result["path"] for result in resumed["results"]] == [
        "a.md",
        "b.md",
        "c.md",
    ]


def test_resume_prioritizes_unseen_targets_and_keeps_prior_failures() -> None:
    entries = [
        _entry(
            f"{name}.md",
            "arxiv",
            f"https://arxiv.org/abs/2601.1000{index}",
            {
                "kind": "arxiv",
                "status": "resolved",
                "arxiv_id": f"2601.1000{index}",
            },
            target_character=name,
        )
        for index, name in enumerate(("a", "b", "c"), start=1)
    ]
    inventory = _inventory(entries)

    def fail_first(target, _hosts, _timeout):
        raise HistoricalSourceFetchError("source_http_503")

    first = run_historical_capture_job(
        inventory,
        limit=1,
        concurrency=1,
        per_host_concurrency=1,
        dispatcher=fail_first,
    )
    calls: list[str] = []

    def capture_next(target, _hosts, _timeout):
        calls.append(target.path)
        return _capture(target)

    second = run_historical_capture_job(
        inventory,
        limit=1,
        concurrency=1,
        per_host_concurrency=1,
        resume_audit=first,
        dispatcher=capture_next,
    )

    assert calls == ["b.md"]
    assert [result["path"] for result in second["results"]] == ["a.md", "b.md"]
    assert second["results"][0]["status"] == "failed"
    assert second["results"][1]["status"] == "captured"


def test_failed_resume_queue_rotates_by_attempt_count() -> None:
    entries = [
        _entry(
            f"{name}.md",
            "arxiv",
            f"https://arxiv.org/abs/2601.4000{index}",
            {
                "kind": "arxiv",
                "status": "resolved",
                "arxiv_id": f"2601.4000{index}",
            },
            target_character=name,
        )
        for index, name in enumerate(("a", "b", "c"), start=1)
    ]
    inventory = _inventory(entries)

    def fail(_target, _hosts, _timeout):
        raise HistoricalSourceFetchError("source_http_503")

    initial = run_historical_capture_job(
        inventory,
        limit=3,
        concurrency=1,
        per_host_concurrency=1,
        dispatcher=fail,
    )
    first_calls: list[str] = []

    def first_retry(target, _hosts, _timeout):
        first_calls.append(target.path)
        raise HistoricalSourceFetchError("source_http_503")

    first_resume = run_historical_capture_job(
        inventory,
        limit=2,
        concurrency=1,
        per_host_concurrency=1,
        resume_audit=initial,
        dispatcher=first_retry,
    )
    second_calls: list[str] = []

    def second_retry(target, _hosts, _timeout):
        second_calls.append(target.path)
        raise HistoricalSourceFetchError("source_http_503")

    second_resume = run_historical_capture_job(
        inventory,
        limit=2,
        concurrency=1,
        per_host_concurrency=1,
        resume_audit=first_resume,
        dispatcher=second_retry,
    )

    assert first_calls == ["a.md", "b.md"]
    assert second_calls == ["c.md", "a.md"]
    assert [result["attempt_count"] for result in second_resume["results"]] == [
        3,
        2,
        2,
    ]


def test_resume_accumulates_evidence_across_all_supported_source_filters() -> None:
    entries = [
        _entry(
            "a-arxiv.md",
            "arxiv",
            "https://arxiv.org/abs/2601.30001",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.30001"},
            target_character="a",
        ),
        _entry(
            "b-github.md",
            "github_trending",
            "https://github.com/octo/repo",
            {"kind": "github", "status": "resolved", "owner": "octo", "repo": "repo"},
            target_character="b",
        ),
        _entry(
            "c-hn.md",
            "hacker_news",
            "https://example.com/story",
            {"kind": "hacker_news", "status": "resolved", "hn_id": "47158975"},
            target_character="c",
        ),
    ]
    inventory = _inventory(entries)
    first = run_historical_capture_job(
        inventory,
        limit=2,
        concurrency=2,
        per_host_concurrency=1,
        dispatcher=lambda target, _hosts, _timeout: _capture(target),
    )
    calls: list[str] = []

    def capture_remaining(target, _hosts, _timeout):
        calls.append(target.source)
        return _capture(target)

    resumed = run_historical_capture_job(
        inventory,
        limit=1,
        concurrency=2,
        per_host_concurrency=1,
        resume_audit=first,
        dispatcher=capture_remaining,
    )

    assert calls == ["hacker_news"]
    assert resumed["captured_count"] == 3
    assert [result["source"] for result in resumed["results"]] == [
        "arxiv",
        "github_trending",
        "hacker_news",
    ]


def test_resume_source_filter_preserves_results_from_other_sources() -> None:
    entries = [
        _entry(
            "a-arxiv.md",
            "arxiv",
            "https://arxiv.org/abs/2601.30001",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.30001"},
            target_character="a",
        ),
        _entry(
            "b-github.md",
            "github_trending",
            "https://github.com/octo/repo",
            {"kind": "github", "status": "resolved", "owner": "octo", "repo": "repo"},
            target_character="b",
        ),
    ]
    inventory = _inventory(entries)
    first = run_historical_capture_job(
        inventory,
        sources={"github_trending"},
        limit=1,
        concurrency=1,
        per_host_concurrency=1,
        dispatcher=lambda target, _hosts, _timeout: _capture(target),
    )
    calls: list[str] = []

    def capture_arxiv(target, _hosts, _timeout):
        calls.append(target.source)
        return _capture(target)

    resumed = run_historical_capture_job(
        inventory,
        sources={"arxiv"},
        limit=1,
        concurrency=1,
        per_host_concurrency=1,
        resume_audit=first,
        dispatcher=capture_arxiv,
    )

    assert calls == ["arxiv"]
    assert resumed["captured_count"] == 2
    assert [result["source"] for result in resumed["results"]] == [
        "arxiv",
        "github_trending",
    ]


def test_resume_rejects_audit_bound_to_another_inventory() -> None:
    inventory = _inventory(
        [
            _entry(
                "a.md",
                "arxiv",
                "https://arxiv.org/abs/2601.30001",
                {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.30001"},
                target_character="a",
            )
        ]
    )
    audit = run_historical_capture_job(
        inventory,
        limit=1,
        concurrency=1,
        per_host_concurrency=1,
        dispatcher=lambda target, _hosts, _timeout: _capture(target),
    )
    audit["inventory_entries_sha256"] = "sha256:" + "f" * 64

    with pytest.raises(HistoricalCaptureJobError, match="resume_audit_invalid"):
        run_historical_capture_job(
            inventory,
            limit=1,
            concurrency=1,
            per_host_concurrency=1,
            resume_audit=audit,
            dispatcher=lambda target, _hosts, _timeout: _capture(target),
        )


def test_arxiv_uses_bounded_batches_and_rate_limits_between_requests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    entries = [
        _entry(
            f"{index:03d}.md",
            "arxiv",
            f"https://arxiv.org/abs/2601.{index:05d}",
            {
                "kind": "arxiv",
                "status": "resolved",
                "arxiv_id": f"2601.{index:05d}",
            },
            target_character=f"{index % 10}",
        )
        for index in range(51)
    ]
    batch_sizes: list[int] = []
    sleeps: list[float] = []

    def batch_fetch(identifiers, **kwargs):
        batch_sizes.append(len(identifiers))
        return [
            HistoricalSourceCapture(
                source="arxiv",
                title=f"Paper {identifier}",
                external_url=f"https://arxiv.org/abs/{identifier}",
                source_text="Verified abstract evidence.",
                captured_at="2026-07-18T02:03:04Z",
                capture_mode="abstract",
                source_completeness="abstract_only",
                source_is_truncated=False,
                metadata={"arxiv_id": identifier},
            )
            for identifier in identifiers
        ]

    monkeypatch.setattr(job, "fetch_arxiv_sources", batch_fetch)
    monkeypatch.setattr(job.time, "sleep", lambda seconds: sleeps.append(seconds))

    audit = run_historical_capture_job(
        _inventory(entries),
        limit=51,
        concurrency=4,
        per_host_concurrency=2,
    )

    assert audit["captured_count"] == 51
    assert batch_sizes == [50, 1]
    assert sleeps == [3.0]


def test_arxiv_bisects_identity_failures_to_isolate_one_bad_record(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    identifiers = ("2601.50001", "2601.59999", "2601.50003")
    entries = [
        _entry(
            f"{index}.md",
            "arxiv",
            f"https://arxiv.org/abs/{identifier}",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": identifier},
            target_character=str(index),
        )
        for index, identifier in enumerate(identifiers, start=1)
    ]
    requests: list[tuple[str, ...]] = []
    sleeps: list[float] = []

    def batch_fetch(requested, **kwargs):
        requested = tuple(requested)
        requests.append(requested)
        if "2601.59999" in requested:
            raise HistoricalSourceFetchError("source_record_not_found")
        return [
            HistoricalSourceCapture(
                source="arxiv",
                title=f"Paper {identifier}",
                external_url=f"https://arxiv.org/abs/{identifier}",
                source_text="Verified abstract evidence.",
                captured_at="2026-07-18T02:03:04Z",
                capture_mode="abstract",
                source_completeness="abstract_only",
                source_is_truncated=False,
                metadata={"arxiv_id": identifier},
            )
            for identifier in requested
        ]

    monkeypatch.setattr(job, "fetch_arxiv_sources", batch_fetch)
    monkeypatch.setattr(job.time, "sleep", lambda seconds: sleeps.append(seconds))

    audit = run_historical_capture_job(
        _inventory(entries),
        limit=3,
        concurrency=2,
        per_host_concurrency=1,
    )

    assert requests == [
        identifiers,
        ("2601.50001",),
        ("2601.59999", "2601.50003"),
        ("2601.59999",),
        ("2601.50003",),
    ]
    assert sleeps == [3.0, 3.0, 3.0, 3.0]
    assert audit["captured_count"] == 2
    assert audit["failed_count"] == 1
    assert audit["results"][1]["failure"] == {
        "type": "source_fetch_error",
        "reason": "source_record_not_found",
    }


def test_concurrency_is_bounded_globally_and_per_host() -> None:
    entries = []
    for index in range(8):
        host = "a.example" if index % 2 == 0 else "b.example"
        entries.append(
            _entry(
                f"{index:02d}.md",
                "blogs_podcasts",
                f"https://{host}/article-{index}",
                {"kind": "external_url", "status": "resolved"},
                target_character=f"{index:x}",
            )
        )
    lock = threading.Lock()
    active_total = 0
    active_hosts: Counter[str] = Counter()
    maximum_total = 0
    maximum_hosts: Counter[str] = Counter()

    def dispatch(target, _hosts, _timeout):
        nonlocal active_total, maximum_total
        host = urlsplit(target.canonical_url).hostname or ""
        with lock:
            active_total += 1
            active_hosts[host] += 1
            maximum_total = max(maximum_total, active_total)
            maximum_hosts[host] = max(maximum_hosts[host], active_hosts[host])
        time.sleep(0.03)
        with lock:
            active_total -= 1
            active_hosts[host] -= 1
        return _capture(target)

    audit = run_historical_capture_job(
        _inventory(entries),
        limit=8,
        blog_allowed_hosts={"a.example", "b.example"},
        concurrency=3,
        per_host_concurrency=1,
        dispatcher=dispatch,
        robots_checker=lambda _url, _hosts, _timeout: True,
    )

    assert audit["captured_count"] == 8
    assert 2 <= maximum_total <= 3
    assert maximum_hosts == {"a.example": 1, "b.example": 1}


def test_blog_requires_an_explicit_exact_host_allowlist_but_other_sources_continue() -> None:
    entries = [
        _entry(
            "a-arxiv.md",
            "arxiv",
            "https://arxiv.org/abs/2601.00001",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00001"},
            target_character="a",
        ),
        _entry(
            "b-blog.md",
            "blogs_podcasts",
            "https://blog.example/article",
            {"kind": "external_url", "status": "resolved"},
            target_character="b",
        ),
    ]
    called: list[str] = []

    def dispatch(target, _hosts, _timeout):
        called.append(target.path)
        return _capture(target)

    audit = run_historical_capture_job(
        _inventory(entries),
        limit=2,
        concurrency=2,
        per_host_concurrency=1,
        dispatcher=dispatch,
    )

    assert called == ["a-arxiv.md"]
    assert audit["captured_count"] == 1
    assert audit["failed_count"] == 1
    assert audit["results"][1]["failure"] == {
        "type": "dispatch_error",
        "reason": "blog_host_not_allowlisted",
    }


def test_blog_robots_disallow_is_typed_and_cached_once_per_host() -> None:
    entries = [
        _entry(
            f"{index}.md",
            "blogs_podcasts",
            f"https://blog.example/article-{index}",
            {"kind": "external_url", "status": "resolved"},
            target_character=str(index),
        )
        for index in (1, 2)
    ]
    robots_calls: list[str] = []
    dispatch_calls: list[str] = []

    def robots_checker(url, _hosts, _timeout):
        robots_calls.append(url)
        return False

    def dispatch(target, _hosts, _timeout):
        dispatch_calls.append(target.path)
        return _capture(target)

    audit = run_historical_capture_job(
        _inventory(entries),
        limit=2,
        blog_allowed_hosts={"blog.example"},
        concurrency=2,
        per_host_concurrency=2,
        dispatcher=dispatch,
        robots_checker=robots_checker,
    )

    assert len(robots_calls) == 1
    assert dispatch_calls == []
    assert [result["failure"] for result in audit["results"]] == [
        {"type": "robots_disallowed", "reason": "robots_disallowed"},
        {"type": "robots_disallowed", "reason": "robots_disallowed"},
    ]


def test_blog_robots_fetch_failure_is_fail_closed_without_stopping_official_sources() -> None:
    entries = [
        _entry(
            "a-arxiv.md",
            "arxiv",
            "https://arxiv.org/abs/2601.00001",
            {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00001"},
            target_character="a",
        ),
        _entry(
            "b-blog.md",
            "blogs_podcasts",
            "https://blog.example/article",
            {"kind": "external_url", "status": "resolved"},
            target_character="b",
        ),
    ]
    dispatch_calls: list[str] = []

    def robots_checker(_url, _hosts, _timeout):
        raise HistoricalSourceFetchError("source_dns_failed")

    def dispatch(target, _hosts, _timeout):
        dispatch_calls.append(target.path)
        return _capture(target)

    audit = run_historical_capture_job(
        _inventory(entries),
        limit=2,
        blog_allowed_hosts={"blog.example"},
        concurrency=2,
        per_host_concurrency=1,
        dispatcher=dispatch,
        robots_checker=robots_checker,
    )

    assert dispatch_calls == ["a-arxiv.md"]
    assert audit["captured_count"] == 1
    assert audit["results"][1]["failure"] == {
        "type": "robots_fetch_error",
        "reason": "robots_fetch_failed",
    }


def test_default_robots_adapter_uses_allowlist_for_redirects_and_path_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    class Response:
        def __init__(self, status: int, *, location: str = "") -> None:
            self.status_code = status
            self.headers = {"Content-Type": "text/plain"}
            if location:
                self.headers["Location"] = location

        def close(self) -> None:
            return None

    monkeypatch.setattr(
        job.source_fetch_adapter,
        "_default_resolver",
        lambda _host: {"104.18.33.45"},
    )
    monkeypatch.setattr(
        job.source_fetch_adapter,
        "_request",
        lambda *_args, **_kwargs: (
            Response(200),
            b"User-agent: *\nDisallow: /private\nAllow: /public\n",
        ),
    )

    policy = load_blog_robots_policy(
        "https://blog.example/public/article",
        frozenset({"blog.example"}),
        3,
    )

    assert policy("https://blog.example/public/article") is True
    assert policy("https://blog.example/private/article") is False

    monkeypatch.setattr(
        job.source_fetch_adapter,
        "_request",
        lambda *_args, **_kwargs: (
            Response(302, location="https://evil.example/robots.txt"),
            b"",
        ),
    )
    with pytest.raises(HistoricalSourceFetchError, match="source_url_not_allowed"):
        load_blog_robots_policy(
            "https://blog.example/public/article",
            frozenset({"blog.example"}),
            3,
        )


def test_allowlisted_http_blog_is_upgraded_to_https_without_losing_origin_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    origin_url = "http://karpathy.github.io/neuralnets/"
    requested_urls: list[str] = []
    robots_urls: list[str] = []

    def fetch(url, **kwargs):
        requested_urls.append(url)
        return HistoricalSourceCapture(
            source="blogs_podcasts",
            title="Neural networks",
            external_url="https://karpathy.github.io/neuralnets/",
            source_text="Verified public article evidence.",
            captured_at="2026-07-18T02:03:04Z",
            capture_mode="excerpt",
            source_completeness="partial",
            source_is_truncated=False,
            metadata={"origin_url": "https://karpathy.github.io/neuralnets/"},
        )

    def robots_checker(url, _hosts, _timeout):
        robots_urls.append(url)
        return True

    monkeypatch.setattr(job, "fetch_public_article_excerpt", fetch)
    audit = run_historical_capture_job(
        _inventory(
            [
                _entry(
                    "karpathy.md",
                    "blogs_podcasts",
                    origin_url,
                    {"kind": "external_url", "status": "resolved"},
                )
            ]
        ),
        limit=1,
        blog_allowed_hosts={"karpathy.github.io"},
        concurrency=1,
        per_host_concurrency=1,
        robots_checker=robots_checker,
    )

    assert requested_urls == ["https://karpathy.github.io/neuralnets"]
    assert robots_urls == ["https://karpathy.github.io/neuralnets"]
    capture = audit["results"][0]["capture"]
    assert capture["external_url"] == "https://karpathy.github.io/neuralnets"
    assert capture["metadata"]["origin_url"] == "http://karpathy.github.io/neuralnets"


def test_blog_allowlist_config_rejects_wildcards_and_urls(tmp_path: Path) -> None:
    config = tmp_path / "allowlist.json"
    config.write_text(
        json.dumps(
            {
                "schema": BLOG_ALLOWLIST_SCHEMA,
                "version": 1,
                "allowed_hosts": ["blog.example", "docs.example"],
            }
        ),
        encoding="utf-8",
    )

    assert load_blog_allowlist(config) == frozenset({"blog.example", "docs.example"})

    for invalid in ("*.example.com", "https://example.com", "127.0.0.1"):
        config.write_text(
            json.dumps(
                {
                    "schema": BLOG_ALLOWLIST_SCHEMA,
                    "version": 1,
                    "allowed_hosts": [invalid],
                }
            ),
            encoding="utf-8",
        )
        with pytest.raises(HistoricalCaptureJobError, match="blog_allowlist_invalid"):
            load_blog_allowlist(config)


def test_cli_writes_only_explicit_0600_audit_and_never_logs_evidence(
    tmp_path: Path,
    capsys,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(
        json.dumps(
            _inventory(
                [
                    _entry(
                        "article.md",
                        "arxiv",
                        "https://arxiv.org/abs/2601.00001",
                        {"kind": "arxiv", "status": "resolved", "arxiv_id": "2601.00001"},
                    )
                ]
            )
        ),
        encoding="utf-8",
    )
    secret_evidence = "SUPER_SECRET_SOURCE_BODY"
    monkeypatch.setattr(
        job,
        "fetch_arxiv_sources",
        lambda identifiers, **kwargs: [
            HistoricalSourceCapture(
                source="arxiv",
                title="Captured paper",
                external_url=f"https://arxiv.org/abs/{identifier}",
                source_text=secret_evidence,
                captured_at="2026-07-18T02:03:04Z",
                capture_mode="abstract",
                source_completeness="abstract_only",
                source_is_truncated=False,
                metadata={},
            )
            for identifier in identifiers
        ],
    )

    assert main(["--inventory", str(inventory_path), "--concurrency", "1"]) == 0
    dry_output = capsys.readouterr()
    assert secret_evidence not in dry_output.out + dry_output.err
    assert sorted(path.name for path in tmp_path.iterdir()) == ["inventory.json"]

    output = tmp_path / "capture-audit.json"
    assert main(
        [
            "--inventory",
            str(inventory_path),
            "--output",
            str(output),
            "--concurrency",
            "1",
        ]
    ) == 0
    written_output = capsys.readouterr()
    assert secret_evidence not in written_output.out + written_output.err
    assert stat.S_IMODE(output.stat().st_mode) == 0o600
    audit = json.loads(output.read_text(encoding="utf-8"))
    assert audit["results"][0]["capture"]["source_text"] == secret_evidence
    assert inventory_path.read_text(encoding="utf-8").startswith("{")


def test_cli_rejects_capture_audit_output_inside_the_repository(
    tmp_path: Path,
    capsys,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import scripts.capture_historical_sources as cli

    repository = tmp_path / "repository"
    repository.mkdir()
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(json.dumps(_inventory([])), encoding="utf-8")
    output = repository / "capture-audit.json"
    monkeypatch.setattr(cli, "PROJECT_ROOT", repository)
    monkeypatch.setattr(
        cli,
        "run_historical_capture_job",
        lambda *_args, **_kwargs: pytest.fail("network job must not start"),
    )

    assert cli.main(["--inventory", str(inventory_path), "--output", str(output)]) == 2
    assert "capture_output_repository_path_rejected" in capsys.readouterr().err
    assert not output.exists()


def test_capture_audit_library_rejects_repository_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    repository = tmp_path / "repository"
    repository.mkdir()
    destination = repository / "capture-audit.json"
    audit = run_historical_capture_job(_inventory([]), limit=1)
    monkeypatch.setattr(job, "_PROJECT_ROOT", repository, raising=False)

    with pytest.raises(HistoricalCaptureJobError, match="repository_path_rejected"):
        job.write_capture_audit(destination, audit)

    destination.write_text(json.dumps(audit), encoding="utf-8")
    destination.chmod(0o600)
    with pytest.raises(HistoricalCaptureJobError, match="repository_path_rejected"):
        job.load_capture_audit(destination)


def test_cli_resume_limit_moves_to_the_next_unseen_inventory_rows(
    tmp_path: Path,
    capsys,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import ai_stack.historical_capture_job as job

    entries = [
        _entry(
            f"{name}.md",
            "arxiv",
            f"https://arxiv.org/abs/2601.2000{index}",
            {
                "kind": "arxiv",
                "status": "resolved",
                "arxiv_id": f"2601.2000{index}",
            },
            target_character=name,
        )
        for index, name in enumerate(("a", "b", "c"), start=1)
    ]
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(json.dumps(_inventory(entries)), encoding="utf-8")
    output = tmp_path / "capture-audit.json"
    calls: list[tuple[str, ...]] = []

    def batch_fetch(identifiers, **kwargs):
        calls.append(tuple(identifiers))
        return [
            HistoricalSourceCapture(
                source="arxiv",
                title=f"Paper {identifier}",
                external_url=f"https://arxiv.org/abs/{identifier}",
                source_text="Verified abstract evidence.",
                captured_at="2026-07-18T02:03:04Z",
                capture_mode="abstract",
                source_completeness="abstract_only",
                source_is_truncated=False,
                metadata={},
            )
            for identifier in identifiers
        ]

    monkeypatch.setattr(job, "fetch_arxiv_sources", batch_fetch)

    assert main(
        [
            "--inventory",
            str(inventory_path),
            "--output",
            str(output),
            "--limit",
            "2",
            "--concurrency",
            "1",
        ]
    ) == 0
    capsys.readouterr()
    assert main(
        [
            "--inventory",
            str(inventory_path),
            "--output",
            str(output),
            "--resume",
            "--limit",
            "1",
            "--concurrency",
            "1",
        ]
    ) == 0
    capsys.readouterr()

    assert calls == [("2601.20001", "2601.20002"), ("2601.20003",)]
    audit = json.loads(output.read_text(encoding="utf-8"))
    assert [result["path"] for result in audit["results"]] == [
        "a.md",
        "b.md",
        "c.md",
    ]
