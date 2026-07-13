from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from content_security import ContentSecurityError
from publisher.main import PublisherOrchestrator
from publisher.telegram_publisher import TelegramPublisher
from publisher.twitter_publisher import TwitterPublisher
from publisher.wechat_publisher import WeChatPublisher


def _write_config(path: Path) -> None:
    path.write_text(
        """publishers:
  twitter:
    enabled: true
    max_length: 240
    api_key: explicit-key
    api_secret: explicit-secret
    access_token: explicit-access
    access_token_secret: explicit-access-secret
    bearer_token: explicit-bearer
  telegram:
    enabled: true
    bot_token: explicit-bot
    chat_id: explicit-chat
    parse_mode: HTML
    disable_web_page_preview: true
  wechat:
    enabled: true
    app_id: explicit-app
    app_secret: explicit-app-secret
    media_id: explicit-media
""",
        encoding="utf-8",
    )


@patch("publisher.main.WeChatPublisher")
@patch("publisher.main.TelegramPublisher")
@patch("publisher.main.TwitterPublisher")
def test_orchestrator_passes_platform_configuration_to_publishers(
    twitter_cls, telegram_cls, wechat_cls, tmp_path: Path
) -> None:
    config = tmp_path / "publisher.yaml"
    _write_config(config)

    PublisherOrchestrator(config)

    twitter_cls.assert_called_once_with(
        api_key="explicit-key",
        api_secret="explicit-secret",
        access_token="explicit-access",
        access_token_secret="explicit-access-secret",
        bearer_token="explicit-bearer",
        max_length=240,
    )
    telegram_cls.assert_called_once_with(
        bot_token="explicit-bot",
        chat_id="explicit-chat",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    wechat_cls.assert_called_once_with(
        app_id="explicit-app",
        app_secret="explicit-app-secret",
        media_id="explicit-media",
    )


def test_orchestrator_batch_statistics_use_the_actual_input_length(tmp_path: Path) -> None:
    config = tmp_path / "publisher.yaml"
    config.write_text("publishers: {}\n", encoding="utf-8")
    orchestrator = PublisherOrchestrator(config)
    publisher = type("Publisher", (), {"publish_content": lambda self, content: True})()
    orchestrator.publishers = {"test": publisher}

    assert orchestrator.publish_batch([{"title": "one"}, {"title": "two"}]) == {
        "test": [True, True]
    }


def test_telegram_escapes_html_and_attribute_values() -> None:
    publisher = TelegramPublisher(bot_token="bot", chat_id="chat")

    message = publisher.format_message(
        {
            "title": "<img src=x onerror=alert(1)>",
            "source": "a&b",
            "summary": "<b>not trusted</b>",
            "url": "https://example.com/?q='x'&ok=1",
            "generated_comment": "<script>alert(1)</script>",
        }
    )

    assert "<img" not in message
    assert "<script" not in message
    assert "&lt;b&gt;not trusted&lt;/b&gt;" in message
    assert "&#x27;" in message
    assert "A&amp;B" in message


def test_telegram_rejects_dangerous_link_scheme() -> None:
    publisher = TelegramPublisher(bot_token="bot", chat_id="chat")

    with pytest.raises(ContentSecurityError):
        publisher.format_message({"title": "x", "url": "javascript:alert(1)"})


def test_wechat_escapes_all_dynamic_html_and_rejects_dangerous_url() -> None:
    publisher = WeChatPublisher(app_id="id", app_secret="secret", media_id="media")
    article = publisher.format_article(
        {
            "title": "<img src=x onerror=alert(1)>",
            "source": "a&b",
            "summary": "<b>summary</b>",
            "url": "https://example.com/?q='x'&ok=1",
            "generated_comment": "<script>alert(1)</script>",
            "generated_analysis": "<svg onload=alert(1)></svg>",
        }
    )

    assert "<img" not in article["content"]
    assert "<script" not in article["content"]
    assert "<svg" not in article["content"]
    assert "&lt;b&gt;summary&lt;/b&gt;" in article["content"]
    assert article["thumb_media_id"] == "media"

    with pytest.raises(ContentSecurityError):
        publisher.format_article({"title": "x", "url": "data:text/html,x"})


def test_twitter_uses_configured_max_length_and_rejects_dangerous_url() -> None:
    publisher = TwitterPublisher(bearer_token="token", max_length=40)

    text = publisher.format_tweet(
        {"title": "a" * 80, "summary": "b" * 80, "url": "https://example.com"}
    )

    assert len(text) <= 40
    with pytest.raises(ContentSecurityError):
        publisher.format_tweet({"title": "x", "url": "javascript:alert(1)"})
