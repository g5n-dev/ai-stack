from processor.tagger import ContentTagger


class _FakeClient:
    def __init__(self, response=None):
        self.response = response
        self.calls = []

    def create_message(self, prompt, max_tokens=None, *, temperature=None, purpose="generation"):
        self.calls.append(prompt)
        if self.response is None:
            raise AssertionError("LLM must not be called")
        return self.response


def test_existing_tags_are_normalized_before_tagger_short_circuits():
    client = _FakeClient()
    tagger = ContentTagger(client, {"enabled": True, "max_tags": 8})
    content = {
        "tags": ["AI编程", " AI 编程 ", "H²RL", "ReAct", "React"],
        "categories": ["AI 工程"],
    }

    result = tagger.tag(content)

    assert result["tags"] == ["AI 编程", "H²RL", "ReAct", "React"]
    assert client.calls == []


def test_llm_tags_use_the_same_exact_alias_normalizer():
    client = _FakeClient(
        '{"categories":["AI 工程"],"tags":["GPT 5.4","GPT-5.4","C/C++"]}'
    )
    tagger = ContentTagger(client, {"enabled": True, "max_tags": 8})

    result = tagger.tag({"title": "Compiler agents"})

    assert result["tags"] == ["GPT-5.4", "C/C++"]
    assert result["categories"] == ["AI 工程"]
