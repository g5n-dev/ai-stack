#!/usr/bin/env python3

import unittest

from runtime_profile import apply_anthropic_runtime_profile, apply_sources_runtime_profile


class RuntimeProfileTest(unittest.TestCase):
    def test_apply_sources_runtime_profile_ci_reduces_workload(self):
        config = {
            "search_fallback": {
                "enabled": True,
                "timeout": 12,
            },
            "sources": {
                "github_trending": {"enabled": True, "limit": 10},
                "hacker_news": {"enabled": True, "limit": 20},
                "arxiv_ai": {"enabled": True, "limit": 10},
                "juejin": {"enabled": True, "limit": 5},
                "blogs_podcasts": {"enabled": True, "limit": 15, "timeout": 30},
                "reddit": {"enabled": True, "limit_per_subreddit": 10, "timeout": 15},
                "twitter": {"enabled": True, "tweets_per_account": 30, "accounts": ["a", "b"]},
            },
        }

        profiled = apply_sources_runtime_profile(config, "ci")

        self.assertFalse(profiled["search_fallback"]["enabled"])
        self.assertEqual(profiled["search_fallback"]["timeout"], 5)
        self.assertEqual(profiled["sources"]["github_trending"]["limit"], 1)
        self.assertEqual(profiled["sources"]["hacker_news"]["limit"], 1)
        self.assertEqual(profiled["sources"]["arxiv_ai"]["limit"], 1)
        self.assertEqual(profiled["sources"]["juejin"]["limit"], 1)
        self.assertEqual(profiled["sources"]["blogs_podcasts"]["limit"], 1)
        self.assertEqual(profiled["sources"]["blogs_podcasts"]["timeout"], 10)
        self.assertFalse(profiled["sources"]["reddit"]["enabled"])
        self.assertFalse(profiled["sources"]["twitter"]["enabled"])

    def test_apply_sources_runtime_profile_default_keeps_config(self):
        config = {
            "search_fallback": {"enabled": True, "timeout": 12},
            "sources": {"github_trending": {"enabled": True, "limit": 10}},
        }

        profiled = apply_sources_runtime_profile(config, "default")

        self.assertEqual(profiled, config)

    def test_apply_anthropic_runtime_profile_ci_disables_heavy_generation(self):
        config = {
            "llm_concurrency": 3,
            "llm_max_retries": 3,
            "generation": {
                "intro_length": 500,
                "comment_length": 1200,
                "analysis_length": 2500,
                "generate_code_examples": True,
                "generate_case_studies": True,
                "generate_faq": True,
                "generate_comparison": True,
                "generate_best_practices": True,
                "generate_performance_tips": True,
                "generate_learning_path": True,
            },
        }

        profiled = apply_anthropic_runtime_profile(config, "ci")

        self.assertEqual(profiled["llm_concurrency"], 2)
        self.assertEqual(profiled["llm_max_retries"], 1)
        self.assertEqual(profiled["generation"]["intro_length"], 220)
        self.assertEqual(profiled["generation"]["comment_length"], 500)
        self.assertEqual(profiled["generation"]["analysis_length"], 900)
        self.assertFalse(profiled["generation"]["generate_code_examples"])
        self.assertFalse(profiled["generation"]["generate_case_studies"])
        self.assertFalse(profiled["generation"]["generate_faq"])
        self.assertFalse(profiled["generation"]["generate_comparison"])
        self.assertFalse(profiled["generation"]["generate_best_practices"])
        self.assertFalse(profiled["generation"]["generate_performance_tips"])
        self.assertFalse(profiled["generation"]["generate_learning_path"])
        self.assertFalse(profiled["generation"]["add_recommendations"])
        self.assertEqual(profiled["generation"]["quality_retries"], 0)


if __name__ == "__main__":
    unittest.main()
