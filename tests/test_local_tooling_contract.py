from __future__ import annotations

from scripts import preflight


def test_supported_python_range_matches_project_metadata() -> None:
    assert preflight._is_supported_python(3, 11)
    assert preflight._is_supported_python(3, 12)
    assert preflight._is_supported_python(3, 13)
    assert not preflight._is_supported_python(3, 10)
    assert not preflight._is_supported_python(3, 14)
    assert not preflight._is_supported_python(4, 0)


def test_preflight_rejects_model_placeholders_and_reserved_example_hosts(
    monkeypatch,
) -> None:
    monkeypatch.setattr(preflight, "load_project_env", lambda _root: None)
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "replace_with_your_token")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://llm.example.com/anthropic")
    monkeypatch.setenv("ANTHROPIC_MODEL", "replace_with_your_model_id")
    monkeypatch.setenv("SEARXNG_BASE_URL", "https://search.example.com/search")

    checks = preflight._check_env()
    failures = [message for level, message in checks if level == "FAIL"]
    warnings = [message for level, message in checks if level == "WARN"]

    assert any("ANTHROPIC_AUTH_TOKEN" in message and "占位符" in message for message in failures)
    assert any("ANTHROPIC_BASE_URL" in message and "占位符" in message for message in failures)
    assert any("ANTHROPIC_MODEL" in message and "占位符" in message for message in failures)
    assert any("SEARXNG_BASE_URL" in message and "占位符" in message for message in warnings)


def test_preflight_accepts_non_placeholder_provider_configuration(monkeypatch) -> None:
    monkeypatch.setattr(preflight, "load_project_env", lambda _root: None)
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "local-test-token-value")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://gateway.company.test/anthropic")
    monkeypatch.setenv("ANTHROPIC_MODEL", "company-model-v1")
    monkeypatch.delenv("SEARXNG_BASE_URL", raising=False)

    checks = preflight._check_env()
    failures = [message for level, message in checks if level == "FAIL"]

    assert failures == []
