"""A recovered archive may have no trend topics at all.

After a 30-day publication gap only four new observations fall inside every
window; all older Posts have aged out. The trend builder correctly emits zero
topics instead of inventing evidence, but the frontend validator, the JS
"committed data" tests and the Chromium e2e suite all treated an empty topic
list as corrupt data. That blocked the first recovery release at persist.

Empty is a legitimate evidence-shortage state. These contracts keep it that way
without lowering the minimum-unique-events threshold or fabricating trends.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_frontend_index_validation_accepts_zero_topics() -> None:
    source = (ROOT / "blog" / "static" / "js" / "trends.js").read_text(encoding="utf-8")

    assert "topicEntries.length > MAX_TOPICS" in source
    assert "topicEntries.length === 0" not in source
    assert "evidence-shortage state" in source
    # The existing empty-state copy is a contract of its own (shard recovery
    # test asserts it verbatim); do not replace it with a "found 0" variant.
    assert '"当前筛选没有趋势信号。"' in source


def test_js_window_contract_tolerates_empty_or_identical_windows() -> None:
    source = (ROOT / "tests" / "js" / "test_trends.mjs").read_text(encoding="utf-8")

    assert "if (dayIds.length > 0 || monthIds.length > 0)" in source
    assert "assert.notDeepEqual(dayIds, monthIds)" in source


def test_e2e_tolerates_a_window_without_topic_cards() -> None:
    source = (ROOT / "tests" / "e2e" / "test_static_site.py").read_text(encoding="utf-8")

    assert "evidence_shortage = topic_cards.count() == 0" in source
    assert "if not evidence_shortage:" in source
    assert "_STATUS_READY_OR_EMPTY = re.compile" in source
    assert "def _skip_when_no_trend_evidence" in source
    assert source.count("_skip_when_no_trend_evidence(page)") >= 3


def test_fail_closed_security_case_is_not_relaxed() -> None:
    """Rejecting a malformed index must still look like an error, not an empty state."""

    source = (ROOT / "tests" / "e2e" / "test_static_site.py").read_text(encoding="utf-8")

    assert "def test_trends_fails_closed_without_presenting_phantom_data_controls" in source
    assert "to_have_class(re.compile" in source
    assert "is-error" in source


def test_empty_state_contract_is_registered_in_ci() -> None:
    source = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "tests/test_trends_empty_state_contract.py" in source


def test_evidence_threshold_is_not_silently_lowered() -> None:
    """Empty is allowed; weak single-observation trends are still not published."""

    source = (ROOT / "processor" / "stack_trends.py").read_text(encoding="utf-8")

    assert "MINIMUM_UNIQUE_EVENTS = 3" in source
