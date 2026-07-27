"""
Runtime profiles
为不同运行场景（本地、CI）提供轻量配置覆盖，避免 GitHub Actions 跑进重型内容管线。
"""

from __future__ import annotations

from copy import deepcopy
import os
from typing import Any, Dict


CI_CANDIDATE_POOL_MIN = 20
CI_CANDIDATE_POOL_MAX = 30


def get_runtime_profile(profile: str | None = None) -> str:
    value = str(profile or os.environ.get("AI_STACK_RUNTIME_PROFILE") or "default").strip().lower()
    return value or "default"


def apply_sources_runtime_profile(config: Dict[str, Any] | None, profile: str | None = None) -> Dict[str, Any]:
    result: Dict[str, Any] = deepcopy(config or {})
    if get_runtime_profile(profile) != "ci":
        return result

    search_fallback = result.setdefault("search_fallback", {})
    search_fallback["enabled"] = False
    search_fallback["timeout"] = 5

    sources = result.setdefault("sources", {})
    # CI still limits expensive LLM processing downstream, but deterministic
    # archive and policy checks need a wider metadata pool.  A small crawler
    # limit can otherwise discard every eligible candidate before the
    # per-source generation quota is applied.
    for source_name in ["github_trending", "hacker_news", "arxiv_ai", "juejin", "blogs_podcasts"]:
        source = sources.setdefault(source_name, {})
        source["enabled"] = True
        configured_limit = int(source.get("limit", 8) or 8)
        source["limit"] = max(
            CI_CANDIDATE_POOL_MIN,
            min(configured_limit, CI_CANDIDATE_POOL_MAX),
        )

    blogs = sources.setdefault("blogs_podcasts", {})
    blogs["timeout"] = min(int(blogs.get("timeout", 30) or 30), 10)

    reddit = sources.setdefault("reddit", {})
    reddit["enabled"] = False

    twitter = sources.setdefault("twitter", {})
    twitter["enabled"] = False

    return result


def apply_anthropic_runtime_profile(config: Dict[str, Any] | None, profile: str | None = None) -> Dict[str, Any]:
    result: Dict[str, Any] = deepcopy(config or {})
    if get_runtime_profile(profile) != "ci":
        return result

    result["llm_concurrency"] = 2
    result["llm_max_retries"] = 1
    result["disable_thinking"] = True

    ai_filter = result.setdefault("ai_filter", {})
    ai_filter["strict_mode"] = False
    ai_filter["min_confidence"] = 0.5

    generation = result.setdefault("generation", {})
    generation["intro_length"] = 220
    generation["comment_length"] = 500
    generation["analysis_length"] = 900
    generation["generate_code_examples"] = False
    generation["generate_case_studies"] = False
    generation["generate_faq"] = False
    generation["generate_comparison"] = False
    generation["generate_best_practices"] = False
    generation["generate_performance_tips"] = False
    generation["generate_learning_path"] = False
    generation["generate_challenges"] = False
    generation["add_recommendations"] = False
    generation["quality_retries"] = 0

    return result
