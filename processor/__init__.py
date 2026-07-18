"""Content processors with lazy public exports.

Deterministic submodules such as :mod:`processor.stack_trends` must remain
usable without importing the optional model runtime.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .anthropic_client import AnthropicClient as AnthropicClient
    from .generator import ContentGenerator as ContentGenerator
    from .main import ProcessorOrchestrator as ProcessorOrchestrator
    from .summarizer import ContentSummarizer as ContentSummarizer
    from .tagger import ContentTagger as ContentTagger
    from .translator import ContentTranslator as ContentTranslator


_EXPORTS = {
    "AnthropicClient": (".anthropic_client", "AnthropicClient"),
    "ContentSummarizer": (".summarizer", "ContentSummarizer"),
    "ContentTranslator": (".translator", "ContentTranslator"),
    "ContentGenerator": (".generator", "ContentGenerator"),
    "ContentTagger": (".tagger", "ContentTagger"),
    "ProcessorOrchestrator": (".main", "ProcessorOrchestrator"),
}

__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    """Resolve compatibility exports only when callers explicitly use them."""

    try:
        module_name, attribute_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc
    value = getattr(import_module(module_name, __name__), attribute_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
