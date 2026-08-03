"""Delivery guarantees for the operational alert channel.

The outage this channel exists for ran four days because the only signal was a
red Actions job.  The two properties that matter are therefore: a failure must
produce a notification, and a *recurring* failure must not produce ninety-six.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from scripts.ops_alert import OpsAlertError, find_open_alert, sync_alert

REPO = "g5n-dev/ai-stack"
KEY = "publish-heartbeat"


class _FakeApi:
    """Records every call so notification behaviour can be asserted exactly."""

    def __init__(self, issues: list[dict[str, Any]] | None = None) -> None:
        self.issues = issues or []
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []
        self.next_number = 100

    def request(
        self,
        method: str,
        endpoint: str,
        body: dict[str, object] | None = None,
    ) -> object | None:
        self.calls.append((method, endpoint, dict(body) if body else None))
        if method == "GET":
            return list(self.issues)
        if method == "POST" and endpoint.endswith("/issues"):
            number = self.next_number
            self.next_number += 1
            created = {
                "number": number,
                "body": str((body or {}).get("body", "")),
                "pull_request": None,
            }
            self.issues.append(created)
            return created
        return {}

    def methods(self) -> list[str]:
        return [f"{method} {endpoint.rsplit('/', 1)[-1]}" for method, endpoint, _ in self.calls]


def _bodies_written(api: _FakeApi) -> list[str]:
    return [
        str(body.get("body", ""))
        for method, _endpoint, body in api.calls
        if method in {"POST", "PATCH"} and body and "body" in body
    ]


def test_first_failure_opens_an_issue() -> None:
    api = _FakeApi()

    result = sync_alert(
        api,
        repository=REPO,
        key="content-stalled",
        title="内容生产停滞",
        summary="refresh_age_hours=33.1",
        failing=True,
    )

    assert result["action"] == "opened"
    created = [call for call in api.calls if call[0] == "POST"]
    assert len(created) == 1, "opening an alert must notify exactly once"
    assert created[0][2]["title"] == "[ops] 内容生产停滞"
    assert "refresh_age_hours=33.1" in created[0][2]["body"]


def test_recurring_failure_edits_instead_of_commenting() -> None:
    api = _FakeApi()
    sync_alert(api, repository=REPO, key="content-stalled", title="停滞",
               summary="first", failing=True)
    api.calls.clear()

    result = sync_alert(api, repository=REPO, key="content-stalled", title="停滞",
                        summary="second", failing=True)

    assert result["action"] == "updated"
    assert result["occurrences"] == 2
    # A comment would notify; an edit must not. This is what keeps a four-day
    # outage at two notifications rather than ninety-six.
    assert not [call for call in api.calls if call[0] == "POST"]
    assert [call for call in api.calls if call[0] == "PATCH"]


def test_repeated_failures_preserve_the_first_seen_time() -> None:
    api = _FakeApi()
    sync_alert(api, repository=REPO, key=KEY, title="t", summary="s", failing=True)
    first_body = _bodies_written(api)[0]
    first_seen = json.loads(first_body.split("<!-- ops-state:")[1].split(" -->")[0])["first_seen"]

    for _ in range(3):
        api.issues[0]["body"] = _bodies_written(api)[-1]
        sync_alert(api, repository=REPO, key=KEY, title="t", summary="s", failing=True)

    latest = json.loads(_bodies_written(api)[-1].split("<!-- ops-state:")[1].split(" -->")[0])
    assert latest["first_seen"] == first_seen
    assert latest["occurrences"] == 4


def test_recovery_comments_and_closes() -> None:
    api = _FakeApi()
    sync_alert(api, repository=REPO, key=KEY, title="t", summary="s", failing=True)
    api.calls.clear()

    result = sync_alert(api, repository=REPO, key=KEY, title="t", summary="", failing=False)

    assert result["action"] == "resolved"
    assert "POST comments" in api.methods()
    closed = [body for method, _e, body in api.calls if method == "PATCH"]
    assert closed and closed[0]["state"] == "closed"


def test_healthy_without_an_open_alert_does_nothing() -> None:
    api = _FakeApi()

    result = sync_alert(api, repository=REPO, key=KEY, title="t", summary="", failing=False)

    assert result["action"] == "noop"
    assert not [call for call in api.calls if call[0] in {"POST", "PATCH"}]


def test_alerts_are_isolated_by_key() -> None:
    api = _FakeApi()
    sync_alert(api, repository=REPO, key="content-stalled", title="a", summary="s", failing=True)
    api.issues[0]["body"] = _bodies_written(api)[0]

    result = sync_alert(api, repository=REPO, key="capacity-ceiling", title="b",
                        summary="s", failing=True)

    # A second, different problem must raise its own notification rather than
    # being absorbed into the open tracker for an unrelated one.
    assert result["action"] == "opened"


def test_pull_requests_are_never_mistaken_for_trackers() -> None:
    api = _FakeApi(
        issues=[
            {"number": 7, "body": f"<!-- ops-alert:{KEY} -->", "pull_request": {"url": "x"}}
        ]
    )

    assert find_open_alert(api, repository=REPO, key=KEY) is None


def test_transport_failure_is_not_swallowed() -> None:
    class _Broken:
        def request(self, method: str, endpoint: str, body: dict[str, object] | None = None):
            raise OpsAlertError("GitHub API request failed (HTTP 403)")

    # A silent alerter is indistinguishable from a healthy system.
    with pytest.raises(OpsAlertError):
        sync_alert(_Broken(), repository=REPO, key=KEY, title="t", summary="s", failing=True)


def test_alert_key_must_be_machine_safe() -> None:
    with pytest.raises(OpsAlertError):
        sync_alert(_FakeApi(), repository=REPO, key="Bad Key!", title="t",
                   summary="s", failing=True)
