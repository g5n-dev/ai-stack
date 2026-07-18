from __future__ import annotations

from crawler.historical_source_fetch import HistoricalSourceCapture


def _capture(
    source: str,
    *,
    title: str,
    source_text: str,
    metadata: dict | None = None,
) -> HistoricalSourceCapture:
    modes = {
        "arxiv": ("abstract", "abstract_only"),
        "github_trending": ("metadata_only", "metadata_only"),
        "hacker_news": ("metadata_only", "metadata_only"),
        "blogs_podcasts": ("excerpt", "partial"),
        "juejin": ("excerpt", "partial"),
    }
    mode, completeness = modes[source]
    return HistoricalSourceCapture(
        source=source,
        title=title,
        external_url="https://example.com/source",
        source_text=source_text,
        captured_at="2026-07-18T02:03:04Z",
        capture_mode=mode,
        source_completeness=completeness,
        source_is_truncated=mode == "excerpt",
        metadata=metadata or {},
    )


def test_arxiv_taxonomy_comes_only_from_title_abstract_and_category() -> None:
    from ai_stack.historical_taxonomy import infer_historical_taxonomy

    capture = _capture(
        "arxiv",
        title="Evaluating retrieval agents for large language models",
        source_text=(
            "We study agentic retrieval-augmented generation for LLM evaluation. "
            "The benchmark measures grounded answers and tool use."
        ),
        metadata={"category": "cs.AI"},
    )

    taxonomy = infer_historical_taxonomy(capture)

    assert taxonomy["tags"][:4] == ["ArXiv", "RAG", "AI Agent", "大语言模型"]
    assert taxonomy["categories"] == ["论文", "大模型"]
    assert taxonomy["scenarios"] == ["AI/ML项目", "大语言模型", "RAG应用"]


def test_github_taxonomy_uses_signed_topics_and_language_conservatively() -> None:
    from ai_stack.historical_taxonomy import infer_historical_taxonomy

    capture = _capture(
        "github_trending",
        title="octo/mcp-runtime",
        source_text="A Rust Model Context Protocol server and command-line toolkit.",
        metadata={
            "language": "Rust",
            "topics": ["model-context-protocol", "cli", "developer-tools"],
        },
    )

    taxonomy = infer_historical_taxonomy(capture)

    assert taxonomy["tags"][:3] == ["GitHub", "MCP", "Rust"]
    assert "命令行工具" in taxonomy["tags"]
    assert taxonomy["categories"] == ["开源生态", "开发工具"]
    assert taxonomy["scenarios"] == ["AI/ML项目", "命令行工具"]


def test_unrelated_hn_metadata_does_not_invent_ai_taxonomy() -> None:
    from ai_stack.historical_taxonomy import infer_historical_taxonomy

    capture = _capture(
        "hacker_news",
        title="A lament for a discontinued photo organizer",
        source_text="A lament for a discontinued photo organizer",
    )

    taxonomy = infer_historical_taxonomy(capture)

    assert taxonomy == {
        "tags": ["Hacker News"],
        "categories": [],
        "scenarios": [],
    }


def test_untrusted_topics_cannot_create_markup_urls_or_unbounded_tags() -> None:
    from ai_stack.historical_taxonomy import infer_historical_taxonomy

    capture = _capture(
        "github_trending",
        title="octo/safe-python-agent",
        source_text="A Python agent framework with Docker and Kubernetes deployment.",
        metadata={
            "language": "Python",
            "topics": [
                "agent",
                "https://evil.example",
                "<script>alert(1)</script>",
                "{{< unsafe >}}",
                "x" * 200,
                "docker",
                "kubernetes",
                "one",
                "two",
                "three",
                "four",
                "five",
                "six",
            ],
        },
    )

    first = infer_historical_taxonomy(capture)
    second = infer_historical_taxonomy(capture)

    assert first == second
    assert len(first["tags"]) <= 8
    assert "https://evil.example" not in first["tags"]
    assert all("<" not in tag and "{{" not in tag for tag in first["tags"])
    assert first["tags"][:3] == ["GitHub", "AI Agent", "Python"]
    assert first["scenarios"] == [
        "AI/ML项目",
        "Kubernetes",
        "云原生/容器",
    ]
