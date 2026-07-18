from __future__ import annotations

import json
from dataclasses import dataclass

import pytest


@dataclass
class _Response:
    status_code: int
    body: bytes
    content_type: str
    url: str
    location: str = ""

    @property
    def content(self) -> bytes:
        return self.body

    @property
    def text(self) -> str:
        return self.body.decode("utf-8")

    @property
    def headers(self) -> dict[str, str]:
        headers = {"Content-Type": self.content_type}
        if self.location:
            headers["Location"] = self.location
        return headers

    def json(self):
        return json.loads(self.text)

    def close(self) -> None:
        return None


class _Session:
    def __init__(self, responses: list[_Response]) -> None:
        self.responses = list(responses)
        self.requests: list[tuple[str, dict]] = []

    def get(self, url: str, **kwargs):
        self.requests.append((url, kwargs))
        assert self.responses, f"unexpected request: {url}"
        return self.responses.pop(0)


def test_arxiv_fetch_uses_official_api_and_preserves_abstract() -> None:
    from crawler.historical_source_fetch import fetch_arxiv_source

    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom"
          xmlns:arxiv="http://arxiv.org/schemas/atom">
      <entry>
        <id>http://arxiv.org/abs/2601.16210v1</id>
        <updated>2026-01-24T01:02:03Z</updated>
        <published>2026-01-23T01:02:03Z</published>
        <title>  Verified   Paper Title </title>
        <summary>First evidence paragraph.\nSecond evidence paragraph.</summary>
        <author><name>Ada Lovelace</name></author>
        <author><name>Alan Turing</name></author>
        <arxiv:primary_category term="cs.AI" />
      </entry>
    </feed>"""
    session = _Session(
        [_Response(200, xml, "application/atom+xml; charset=utf-8", "https://export.arxiv.org/api/query")]
    )

    capture = fetch_arxiv_source("2601.16210v1", session=session, timeout=3)

    assert capture.source == "arxiv"
    assert capture.title == "Verified Paper Title"
    assert capture.external_url == "https://arxiv.org/abs/2601.16210v1"
    assert capture.source_text == "First evidence paragraph. Second evidence paragraph."
    assert capture.metadata["authors"] == ["Ada Lovelace", "Alan Turing"]
    assert capture.metadata["category"] == "cs.AI"
    assert session.requests[0][0].startswith("https://export.arxiv.org/api/query?")


def test_arxiv_batch_fetch_is_one_request_and_keeps_requested_order() -> None:
    from crawler.historical_source_fetch import fetch_arxiv_sources

    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom"
          xmlns:arxiv="http://arxiv.org/schemas/atom">
      <entry><id>http://arxiv.org/abs/2601.00002v1</id><title>Second</title>
        <summary>Second verified abstract.</summary><published>2026-01-02T00:00:00Z</published>
        <author><name>Second Author</name></author><arxiv:primary_category term="cs.LG" /></entry>
      <entry><id>http://arxiv.org/abs/2601.00001v1</id><title>First</title>
        <summary>First verified abstract.</summary><published>2026-01-01T00:00:00Z</published>
        <author><name>First Author</name></author><arxiv:primary_category term="cs.AI" /></entry>
    </feed>"""
    session = _Session(
        [_Response(200, xml, "application/atom+xml", "https://export.arxiv.org/api/query")]
    )

    captures = fetch_arxiv_sources(
        ["2601.00001v1", "2601.00002v1"], session=session, timeout=3
    )

    assert [capture.title for capture in captures] == ["First", "Second"]
    assert len(session.requests) == 1
    assert "2601.00001v1%2C2601.00002v1" in session.requests[0][0]


def test_github_fetch_accepts_only_a_repo_locator_and_returns_metadata() -> None:
    from crawler.historical_source_fetch import HistoricalSourceFetchError, fetch_github_source

    payload = {
        "full_name": "octo/example",
        "html_url": "https://github.com/octo/example",
        "description": "A verified repository description.",
        "language": "Rust",
        "stargazers_count": 123,
        "forks_count": 7,
        "license": {"spdx_id": "Apache-2.0"},
        "topics": ["agent", "rust"],
        "updated_at": "2026-07-18T01:02:03Z",
    }
    session = _Session(
        [_Response(200, json.dumps(payload).encode(), "application/json", "https://api.github.com/repos/octo/example")]
    )

    capture = fetch_github_source("octo", "example", session=session, timeout=3)

    assert capture.title == "octo/example"
    assert capture.external_url == "https://github.com/octo/example"
    assert capture.metadata["license"] == "Apache-2.0"
    assert capture.metadata["stars"] == 123
    assert capture.metadata["topics"] == ["agent", "rust"]
    assert session.requests[0][0] == "https://api.github.com/repos/octo/example"
    with pytest.raises(HistoricalSourceFetchError, match="invalid_github_locator"):
        fetch_github_source("..", "metadata", session=_Session([]))


def test_hacker_news_fetch_is_metadata_only_and_requires_matching_id() -> None:
    from crawler.historical_source_fetch import HistoricalSourceFetchError, fetch_hacker_news_source

    payload = {
        "id": 47158975,
        "type": "story",
        "title": "How will OpenAI compete?",
        "url": "https://www.ben-evans.com/example",
        "by": "iamskeole",
        "score": 284,
        "descendants": 385,
        "time": 1772100000,
    }
    session = _Session(
        [_Response(200, json.dumps(payload).encode(), "application/json", "https://hacker-news.firebaseio.com/v0/item/47158975.json")]
    )

    capture = fetch_hacker_news_source("47158975", session=session, timeout=3)

    assert capture.source == "hacker_news"
    assert capture.source_text == "How will OpenAI compete?"
    assert capture.metadata["hn_id"] == 47158975
    assert capture.metadata["score"] == 284
    assert capture.external_url == "https://www.ben-evans.com/example"
    with pytest.raises(HistoricalSourceFetchError, match="invalid_hn_id"):
        fetch_hacker_news_source("1/../../etc", session=_Session([]))


def test_public_article_excerpt_revalidates_allowlisted_redirects() -> None:
    from crawler.historical_source_fetch import (
        HistoricalSourceFetchError,
        fetch_public_article_excerpt,
    )

    redirect = _Response(
        301,
        b"",
        "text/html",
        "https://openai.com/old",
        location="https://openai.com/new",
    )
    html = (
        "<html><head><title>Verified source page</title></head><body><article>"
        + "<p>First complete source paragraph with concrete implementation facts.</p>" * 20
        + "</article></body></html>"
    ).encode()
    session = _Session(
        [redirect, _Response(200, html, "text/html; charset=utf-8", "https://openai.com/new")]
    )

    capture = fetch_public_article_excerpt(
        "https://openai.com/old",
        allowed_hosts={"openai.com"},
        session=session,
        resolver=lambda _host: {"104.18.33.45"},
        timeout=3,
    )

    assert capture.title == "Verified source page"
    assert capture.external_url == "https://openai.com/new"
    assert "implementation facts" in capture.source_text
    assert len(session.requests) == 2

    bad_redirect = _Session(
        [
            _Response(
                302,
                b"",
                "text/html",
                "https://openai.com/old",
                location="http://127.0.0.1/admin",
            )
        ]
    )
    with pytest.raises(HistoricalSourceFetchError, match="source_url_not_allowed"):
        fetch_public_article_excerpt(
            "https://openai.com/old",
            allowed_hosts={"openai.com"},
            session=bad_redirect,
            resolver=lambda _host: {"104.18.33.45"},
        )


def test_public_article_excerpt_rejects_private_dns_and_oversized_pages() -> None:
    from crawler.historical_source_fetch import (
        HistoricalSourceFetchError,
        fetch_public_article_excerpt,
    )

    with pytest.raises(HistoricalSourceFetchError, match="source_host_not_public"):
        fetch_public_article_excerpt(
            "https://openai.com/private",
            allowed_hosts={"openai.com"},
            session=_Session([]),
            resolver=lambda _host: {"127.0.0.1"},
        )

    session = _Session(
        [
            _Response(
                200,
                b"<html>" + b"x" * (2 * 1024 * 1024 + 1) + b"</html>",
                "text/html",
                "https://openai.com/huge",
            )
        ]
    )
    with pytest.raises(HistoricalSourceFetchError, match="source_response_too_large"):
        fetch_public_article_excerpt(
            "https://openai.com/huge",
            allowed_hosts={"openai.com"},
            session=session,
            resolver=lambda _host: {"104.18.33.45"},
        )


def test_juejin_recovery_publishes_only_a_bounded_tier_c_excerpt() -> None:
    from crawler.historical_source_fetch import fetch_juejin_source_excerpt
    from crawler.juejin_article import JuejinArticleCapture

    body = "这是已经通过 SSR 结构校验的来源正文段落。" * 500
    source_url = "https://juejin.cn/post/7663304647513718799"

    def fetcher(url: str, *, timeout: int):
        assert url == source_url
        assert timeout == 3
        return JuejinArticleCapture(
            article_id="7663304647513718799",
            source_url=url,
            markdown="## 来源正文\n\n" + body,
            plain_text=body,
            heading_count=3,
            code_block_count=2,
        )

    capture = fetch_juejin_source_excerpt(
        source_url,
        discovery_title="历史索引保留的标题",
        fetcher=fetcher,
        timeout=3,
    )

    assert capture.source == "juejin"
    assert capture.title == "历史索引保留的标题"
    assert capture.capture_mode == "excerpt"
    assert capture.source_completeness == "partial"
    assert capture.source_is_truncated is True
    assert len(capture.source_text) <= 6_000
    assert capture.metadata["article_id"] == "7663304647513718799"
    assert capture.metadata["source_truncation_reason"] == "historical_excerpt_only"
