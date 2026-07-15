from processor.scenario_analyzer import ScenarioAnalyzer
from processor.scenarios import get_all_scenario_names


class _FakeClient:
    def __init__(self, response=None):
        self.response = response

    def create_message(self, prompt, max_tokens=None, *, temperature=None, purpose="generation"):
        if self.response is None:
            raise AssertionError("LLM must not be called")
        return self.response


def _names(items):
    return [item["name"] if isinstance(item, dict) else item for item in items]


def test_llm_scenarios_are_strictly_filtered_to_application_whitelist():
    analyzer = ScenarioAnalyzer(_FakeClient(), {"max_scenarios": 3})

    result = analyzer._normalize(
        [
            {"name": "工具", "confidence": 0.9},
            {"name": "Android", "confidence": 0.8},
            {"name": "大语言模型", "confidence": 0.7},
        ]
    )

    assert _names(result) == ["大语言模型"]
    assert set(_names(result)) <= set(get_all_scenario_names())


def test_latin_keywords_use_token_boundaries_instead_of_substrings():
    analyzer = ScenarioAnalyzer(_FakeClient(), {"max_scenarios": 3})

    assert analyzer._fallback(
        {"tags": ["Training", "Fairness"], "description": "A careful training study"}
    ) == []
    assert _names(analyzer._fallback({"tags": ["AI安全"]})) == ["AI/ML项目"]
    assert _names(analyzer._fallback({"tags": ["LLM推理"]})) == ["大语言模型"]


def test_fallback_never_emits_legacy_tool_or_android_values():
    analyzer = ScenarioAnalyzer(_FakeClient(), {"max_scenarios": 3})

    library_names = _names(analyzer._fallback({"description": "A reusable library"}))
    kotlin_names = _names(analyzer._fallback({"language": "Kotlin"}))

    assert library_names == ["效率工具"]
    assert kotlin_names == ["移动应用"]
    assert {"工具", "Android"}.isdisjoint(library_names + kotlin_names)


def test_no_evidence_no_longer_defaults_to_web_application():
    analyzer = ScenarioAnalyzer(_FakeClient(), {"max_scenarios": 3})

    assert analyzer._fallback({"source": "github_trending", "title": "Unknown"}) == []
    assert analyzer._fallback({"source": "arxiv", "title": "Unknown"}) == []


def test_existing_invalid_scenario_is_replaced_by_valid_fallback():
    analyzer = ScenarioAnalyzer(_FakeClient(), {"enabled": True, "max_scenarios": 3})

    result = analyzer.analyze(
        {
            "source": "blogs_podcasts",
            "tags": ["RAG"],
            "scenarios": ["工具"],
        }
    )

    assert _names(result["scenarios"]) == ["RAG应用"]
    assert set(_names(result["scenarios"])) <= set(get_all_scenario_names())
