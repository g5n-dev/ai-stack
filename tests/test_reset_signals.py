from __future__ import annotations

import pytest

from ai_stack.reset_signals import classify_reset_signal, signal_title_prefix


@pytest.mark.parametrize(
    ("text", "expected_kind", "expected_status", "expected_horizon"),
    [
        (
            "We have reset Codex usage limits for all paid users.",
            "hard_reset",
            "confirmed",
            "already_announced",
        ),
        (
            "The Codex usage limits have now been reset across all paid plans.",
            "hard_reset",
            "confirmed",
            "already_announced",
        ),
        (
            "Back at the laptop: usage limits reset for all paid users of Codex.",
            "hard_reset",
            "confirmed",
            "already_announced",
        ),
        (
            "I'll do another performative reset on Monday.",
            "hard_reset",
            "promised",
            "monday",
        ),
        (
            "I'm feeling like a limit reset. Hold on tight.",
            "forecast_signal",
            "watch",
            "unknown",
        ),
        (
            "We added a banked reset to every Codex account.",
            "banked_reset",
            "confirmed",
            "already_announced",
        ),
        (
            "Codex gets 2X the usual usage limits through the weekend.",
            "temp_boost",
            "confirmed",
            "weekend",
        ),
        (
            "There will be no Codex usage-limit reset today.",
            "hard_reset",
            "negated",
            "today",
        ),
    ],
)
def test_reset_signal_taxonomy(
    text: str,
    expected_kind: str,
    expected_status: str,
    expected_horizon: str,
) -> None:
    result = classify_reset_signal(text)

    assert result["kind"] == expected_kind
    assert result["status"] == expected_status
    assert result["horizon"] == expected_horizon


def test_short_confirmation_uses_parent_context_without_inventing_scope() -> None:
    result = classify_reset_signal("It is done.", context="So what about our Codex reset?")

    assert result["kind"] == "hard_reset"
    assert result["status"] == "confirmed"
    assert result["products"] == ["Codex"]
    assert result["confidence"] >= 0.9


def test_mirrored_reply_confirmation_uses_the_embedded_parent_question() -> None:
    result = classify_reset_signal(
        "Hi. It is done. User asked: So what about our reset?"
    )

    assert result["kind"] == "hard_reset"
    assert result["status"] == "confirmed"
    assert result["products"] == []
    assert result["confidence"] >= 0.9


def test_parent_question_does_not_become_the_authors_promise() -> None:
    result = classify_reset_signal(
        "No.",
        context="Will you reset Codex usage limits tomorrow?",
    )

    assert result["kind"] == "hard_reset"
    assert result["status"] == "negated"
    assert result["notify"] is False


def test_parent_promise_is_not_inherited_by_an_uncommitted_reply() -> None:
    result = classify_reset_signal(
        "Thanks for asking.",
        context="I promise I will reset Codex usage limits tomorrow.",
    )

    assert result["status"] == "insufficient_evidence"
    assert result["notify"] is False


def test_question_is_not_treated_as_a_reset_commitment() -> None:
    result = classify_reset_signal("Will Codex usage limits reset today?")

    assert result["status"] == "insufficient_evidence"
    assert result["notify"] is False


def test_done_reply_rejects_non_quota_parent_scope() -> None:
    result = classify_reset_signal(
        "It is done.",
        context="Did you reset the Codex demo password?",
    )

    assert result["status"] == "insufficient_evidence"
    assert result["notify"] is False


@pytest.mark.parametrize(
    ("text", "context"),
    [
        ("The database reset button has been pressed.", ""),
        ("The reset button has been pressed for the demo.", ""),
        ("It is done.", "Did you reset the Codex database?"),
        (
            "Hi. It is done. User asked: what about our database reset?",
            "",
        ),
        ("We added a banked reset to the game economy.", ""),
        ("I have reset the server rate limits.", ""),
        ("The API server rate limits have been reset after the incident.", ""),
    ],
)
def test_non_quota_reset_domains_never_trigger_notifications(
    text: str,
    context: str,
) -> None:
    result = classify_reset_signal(text, context=context)

    assert result["status"] == "insufficient_evidence"
    assert result["notify"] is False


def test_announced_reset_that_is_still_propagating_is_treated_as_promised() -> None:
    result = classify_reset_signal(
        "Enjoy a nice reset everyone. Landing in the next hour or so, go /fast."
    )

    assert result["kind"] == "hard_reset"
    assert result["status"] == "promised"
    assert result["horizon"] == "next_hour"
    assert result["notify"] is True


@pytest.mark.parametrize(
    "text",
    [
        "I have a filter on the word reset, worry not.",
        "I feel Theo is in need of a reset.",
        "One day we created the reset button and the rest is history.",
        "I have reset my account password.",
        "We have reset your password for the Codex account.",
        "I'll reset the demo tomorrow. Codex is looking great.",
        "The Codex demo is fixed. It is done.",
        "Codex is 2X faster after today's optimization.",
        "Ask ChatGPT to roast your computer usage after a day.",
        "",
    ],
)
def test_reset_word_or_product_mention_alone_is_not_a_prediction(text: str) -> None:
    result = classify_reset_signal(text)

    assert result["kind"] == "irrelevant"
    assert result["status"] == "insufficient_evidence"
    assert result["notify"] is False


def test_recovered_incident_is_a_watch_signal_not_a_reset_claim() -> None:
    result = classify_reset_signal(
        "Codex is back and stable after the outage. Apologies for the disruption."
    )

    assert result["kind"] == "forecast_signal"
    assert result["status"] == "watch"
    assert 0.5 <= result["confidence"] < 0.8
    assert result["notify"] is False


@pytest.mark.parametrize(
    "text",
    [
        "After fixing the server, I have reset Codex usage limits for all paid users.",
        "The database is stable, and usage limits have been reset for Codex users.",
    ],
)
def test_explicit_usage_limit_reset_wins_over_incidental_system_words(
    text: str,
) -> None:
    result = classify_reset_signal(text)

    assert result["kind"] == "hard_reset"
    assert result["status"] == "confirmed"
    assert result["notify"] is True


def test_only_confirmed_or_promised_reset_events_trigger_immediate_notification() -> None:
    confirmed = classify_reset_signal("I have reset usage limits for Codex users.")
    promised = classify_reset_signal("Codex reset incoming tomorrow.")
    watch = classify_reset_signal("I am feeling like a Codex reset.")
    boost = classify_reset_signal("Codex usage limits are 2X this weekend.")

    assert confirmed["notify"] is True
    assert promised["notify"] is True
    assert watch["notify"] is False
    assert boost["notify"] is False


def test_hard_reset_is_distinguished_from_banked_reset_and_policy_changes() -> None:
    hard = classify_reset_signal("Everyone's Codex weekly limits have been reset.")
    banked = classify_reset_signal("A banked reset was added to every account.")
    policy = classify_reset_signal("We removed the 5h rate limit for Codex.")

    assert hard["kind"] == "hard_reset"
    assert banked["kind"] == "banked_reset"
    assert policy["kind"] == "policy_change"


def test_title_prefix_exposes_actionable_state_without_false_precision() -> None:
    promised = classify_reset_signal("I'll reset Codex limits tomorrow.")
    insufficient = classify_reset_signal("Don't say reset.")

    assert signal_title_prefix(promised) == "[额度重置已预告]"
    assert signal_title_prefix(insufficient) == ""
