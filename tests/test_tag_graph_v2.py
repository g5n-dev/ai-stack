#!/usr/bin/env python3

import json
import re
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from processor.tag_graph import (
    TagGraphBuilder,
    _build_focus_shard_payloads,
    _focus_shard_bucket,
    build_search_index,
    build_tag_graph_data,
    build_weighted_tag_communities,
    convert_v1_graph_to_v2,
    write_tag_graph_split_from_result,
)
from processor.tech_stack import TECH_LAYERS


class TagGraphV2Test(unittest.TestCase):
    def _write_post(
        self,
        directory: Path,
        filename: str,
        *,
        title: str,
        date: str,
        tags: list[str],
        body: str,
        external_url: str | None = None,
    ) -> None:
        quoted_tags = ", ".join(json.dumps(tag, ensure_ascii=False) for tag in tags)
        frontmatter_lines = [
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"date: {date}",
            f"tags: [{quoted_tags}]",
        ]
        if external_url:
            frontmatter_lines.append(
                f"external_url: {json.dumps(external_url, ensure_ascii=False)}"
            )
        frontmatter_lines.extend(["---", "", body, ""])
        (directory / filename).write_text(
            "\n".join(frontmatter_lines),
            encoding="utf-8",
        )

    def _build_sample(self, posts_dir: Path, *, reverse: bool = False):
        posts = [
            {
                "filename": "01-alpha.md",
                "title": "Alpha Agent",
                "date": "2026-01-01T08:00:00+08:00",
                "tags": ["Python", "LLM", "Agent", "AI"],
                "body": "Python works with Kubernetes for AI systems.",
            },
            {
                "filename": "02-beta.md",
                "title": "Beta Runtime",
                "date": "2026-01-03T00:00:00Z",
                "tags": ["Python", "LLM"],
                "body": "Python and React power this API runtime.",
            },
            {
                "filename": "03-gamma.md",
                "title": "Gamma Retrieval",
                "date": "2026-01-02",
                "tags": ["Agent", "RAG"],
                "body": "RAG connects an LLM with an API.",
            },
        ]
        for post in reversed(posts) if reverse else posts:
            self._write_post(posts_dir, **post)

        with mock.patch.dict(
            "os.environ",
            {"TAG_INTRO_ENABLED": "0", "TAG_GRAPH_ENABLE_CONTENT_MINING": "1"},
            clear=False,
        ):
            return build_tag_graph_data(
                enable_content_mining=True,
                existing_output_path=None,
                content_dir=str(posts_dir),
            )

    def test_v2_namespaces_nodes_and_computes_real_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir) / "posts"
            posts_dir.mkdir()
            result = self._build_sample(posts_dir)

        graph = result["graph"]
        self.assertEqual(graph["version"], 2)
        self.assertEqual(graph["generated_at"], "2026-01-03T00:00:00Z")
        self.assertEqual(graph["layers"]["application"]["color"], "#7aa6b8")
        self.assertEqual(graph["layers"]["scenario"]["color"], "#cbd5e1")
        self.assertEqual(graph["layers"]["concept"]["color"], "#67e8f9")
        self.assertEqual(TECH_LAYERS["application"]["color"], "#7aa6b8")
        self.assertEqual(TECH_LAYERS["scenario"]["color"], "#cbd5e1")

        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertIn("tech:python", nodes)
        self.assertIn("tag:Python", nodes)
        self.assertIn("concept:Python", nodes)
        self.assertEqual(nodes["tag:Python"]["article_count"], 2)
        self.assertEqual(nodes["tech:python"]["article_count"], 2)
        self.assertEqual(nodes["tech:agent"]["article_count"], 2)
        self.assertGreaterEqual(nodes["tag:Python"]["degree"], 3)
        self.assertGreater(nodes["tag:Python"]["weighted_degree"], 0)

        python_kubernetes = next(
            link
            for link in graph["links"]
            if {link["source"], link["target"]}
            == {"concept:Python", "concept:Kubernetes"}
        )
        self.assertEqual(python_kubernetes["weight"], 1)

        ranks = [node["rank"] for node in graph["nodes"]]
        self.assertEqual(sorted(ranks), list(range(1, len(ranks) + 1)))
        required_fields = {
            "id",
            "legacy_id",
            "name",
            "layer",
            "category",
            "description",
            "article_count",
            "degree",
            "weighted_degree",
            "community_id",
            "rank",
        }
        self.assertTrue(
            all(required_fields <= set(node) for node in graph["nodes"]),
            "GraphNodeV2 fields must be present even when community_id is null",
        )
        self.assertTrue(all(link["source"].split(":", 1)[0] in {"tech", "tag", "concept"} for link in graph["links"]))
        self.assertTrue(all(link["target"].split(":", 1)[0] in {"tech", "tag", "concept"} for link in graph["links"]))
        self.assertTrue(all("related_tags" not in node for node in graph["nodes"]))
        self.assertTrue(all("related_concepts" not in node for node in graph["nodes"]))
        self.assertTrue(all("community" not in node for node in graph["nodes"]))
        self.assertTrue(
            all("community_id" in node for node in graph["nodes"] if node["layer"] == "tag")
        )

    def test_yaml_block_tags_are_included_in_counts_and_generated_at(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir) / "posts"
            posts_dir.mkdir()
            self._write_post(
                posts_dir,
                "inline.md",
                title="Inline",
                date="2026-01-01",
                tags=["Python"],
                body="Inline article.",
            )
            (posts_dir / "block.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: Block list
                    date: 2026-01-02T08:00:00+08:00
                    tags:
                      - Python
                      - "LLM"
                    ---

                    Block-list article.
                    """
                ),
                encoding="utf-8",
            )

            with mock.patch.dict("os.environ", {"TAG_INTRO_ENABLED": "0"}, clear=False):
                result = build_tag_graph_data(
                    enable_content_mining=False,
                    existing_output_path=None,
                    content_dir=str(posts_dir),
                )

        nodes = {node["id"]: node for node in result["graph"]["nodes"]}
        self.assertEqual(result["graph"]["generated_at"], "2026-01-02T00:00:00Z")
        self.assertEqual(result["stats"]["tag_stats"]["total_articles"], 2)
        self.assertEqual(nodes["tag:Python"]["article_count"], 2)
        self.assertEqual(nodes["tag:LLM"]["article_count"], 1)

    def test_canonical_external_url_is_counted_once_and_clean_copy_wins(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir) / "posts"
            posts_dir.mkdir()
            self._write_post(
                posts_dir,
                "01-polluted.md",
                title="Duplicate placeholder",
                date="2026-01-02",
                tags=["Polluted", "Duplicate"],
                external_url="https://example.com/news?id=42&utm_source=feed#fragment",
                body="由于您没有提供原始正文，我将基于标题推演这篇文章。",
            )
            self._write_post(
                posts_dir,
                "02-clean.md",
                title="Canonical article",
                date="2026-01-01",
                tags=["Python", "LLM"],
                external_url="https://example.com/news?id=42",
                body=(
                    "这是一篇包含真实技术上下文的文章。Python 与 LLM 共同构成服务层，"
                    "并通过可观测性、测试和明确的数据边界保证可靠运行。" * 8
                ),
            )

            with mock.patch.dict("os.environ", {"TAG_INTRO_ENABLED": "0"}, clear=False):
                result = build_tag_graph_data(
                    enable_content_mining=False,
                    existing_output_path=None,
                    content_dir=str(posts_dir),
                )

        nodes = {node["id"]: node for node in result["graph"]["nodes"]}
        self.assertEqual(result["stats"]["tag_stats"]["total_articles"], 1)
        self.assertEqual(nodes["tag:Python"]["article_count"], 1)
        self.assertEqual(nodes["tag:LLM"]["article_count"], 1)
        self.assertNotIn("tag:Polluted", nodes)
        self.assertNotIn("tag:Duplicate", nodes)
        self.assertEqual(
            result["stats"]["tag_stats"]["canonical_duplicate_files_skipped"], 1
        )

    def test_graph_applies_reviewed_tag_aliases_without_casefolding(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir) / "posts"
            posts_dir.mkdir()
            self._write_post(
                posts_dir,
                "01-first.md",
                title="First",
                date="2026-01-01",
                tags=["AI编程", "XAI", "SWE-bench"],
                body="First article.",
            )
            self._write_post(
                posts_dir,
                "02-second.md",
                title="Second",
                date="2026-01-02",
                tags=["AI 编程", "xAI", "SWE-Bench"],
                body="Second article.",
            )

            with mock.patch.dict("os.environ", {"TAG_INTRO_ENABLED": "0"}, clear=False):
                result = build_tag_graph_data(
                    enable_content_mining=False,
                    existing_output_path=None,
                    content_dir=str(posts_dir),
                )

        nodes = {node["id"]: node for node in result["graph"]["nodes"]}
        self.assertEqual(nodes["tag:AI 编程"]["article_count"], 2)
        self.assertNotIn("tag:AI编程", nodes)
        self.assertIn("tag:XAI", nodes)
        self.assertIn("tag:xAI", nodes)
        self.assertIn("tag:SWE-bench", nodes)
        self.assertIn("tag:SWE-Bench", nodes)

    def test_unverifiable_synthetic_article_is_excluded_from_graph_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir) / "posts"
            posts_dir.mkdir()
            self._write_post(
                posts_dir,
                "synthetic.md",
                title="Synthetic",
                date="2026-01-01",
                tags=["Hallucinated", "Graph Pollution"],
                external_url="https://example.com/synthetic",
                body=(
                    "您没有提供需要总结的具体文章正文，仅提供了标题。"
                    "我将基于标题推测完整技术细节。"
                ),
            )

            with mock.patch.dict("os.environ", {"TAG_INTRO_ENABLED": "0"}, clear=False):
                result = build_tag_graph_data(
                    enable_content_mining=False,
                    existing_output_path=None,
                    content_dir=str(posts_dir),
                )

        nodes = {node["id"]: node for node in result["graph"]["nodes"]}
        stats = result["stats"]["tag_stats"]
        self.assertEqual(stats["total_articles"], 0)
        self.assertEqual(stats["synthetic_article_groups_skipped"], 1)
        self.assertEqual(stats["synthetic_article_files_skipped"], 1)
        self.assertNotIn("tag:Hallucinated", nodes)
        self.assertNotIn("tag:Graph Pollution", nodes)

    def test_transparent_archived_article_is_excluded_from_graph_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir) / "posts"
            posts_dir.mkdir()
            (posts_dir / "archived.md").write_text(
                "---\n"
                "title: Archived\n"
                "date: 2026-01-01\n"
                "external_url: https://example.com/archived\n"
                "archived: true\n"
                "tags: [Hallucinated, Archive Pollution]\n"
                "---\n\n"
                "该条目仅保留原始来源入口。\n",
                encoding="utf-8",
            )

            with mock.patch.dict("os.environ", {"TAG_INTRO_ENABLED": "0"}, clear=False):
                result = build_tag_graph_data(
                    enable_content_mining=False,
                    existing_output_path=None,
                    content_dir=str(posts_dir),
                )

        nodes = {node["id"]: node for node in result["graph"]["nodes"]}
        stats = result["stats"]["tag_stats"]
        self.assertEqual(stats["total_articles"], 0)
        self.assertEqual(stats["synthetic_article_groups_skipped"], 1)
        self.assertEqual(stats["synthetic_article_files_skipped"], 1)
        self.assertNotIn("tag:Hallucinated", nodes)
        self.assertNotIn("tag:Archive Pollution", nodes)

    def test_semantic_matching_uses_tokens_not_arbitrary_substrings_or_category(self):
        builder = TagGraphBuilder(enable_content_mining=False)
        gin = {"id": "gin", "name": "Gin", "layer": "framework", "category": "backend"}
        go = {"id": "go", "name": "Go", "layer": "language", "category": "language"}
        javascript = {
            "id": "javascript",
            "name": "JavaScript",
            "layer": "language",
            "category": "language",
        }
        agent = {"id": "agent", "name": "AI Agent", "layer": "application", "category": "ai"}
        ai_ml = {"id": "ai_ml", "name": "AI/ML项目", "layer": "scenario", "category": "ai"}

        self.assertFalse(builder._is_semantically_related("Engineering", "gin", gin))
        self.assertFalse(builder._is_semantically_related("Ginkgo Bioworks", "gin", gin))
        self.assertFalse(builder._is_semantically_related("Google", "go", go))
        self.assertFalse(builder._is_semantically_related("C", "javascript", javascript))
        self.assertFalse(builder._is_semantically_related("AI", "agent", agent))
        self.assertTrue(builder._is_semantically_related("Go语言", "go", go))
        self.assertTrue(builder._is_semantically_related("Multi-Agent", "agent", agent))
        self.assertTrue(builder._is_semantically_related("AI", "ai_ml", ai_ml))

    def test_concept_mining_rejects_plain_english_but_keeps_technical_terms(self):
        builder = TagGraphBuilder(enable_content_mining=True)

        self.assertEqual(
            builder._extract_keywords(
                "This is an ordinary sentence about nothing technical."
            ),
            [],
        )
        self.assertEqual(
            set(builder._extract_keywords("GraphWorkbench uses python and Kubernetes.")),
            {"GraphWorkbench", "python", "Kubernetes"},
        )

    def test_weighted_label_propagation_is_order_independent_and_caps_top_11_plus_other(self):
        nodes = []
        links = []
        for index in range(13):
            left = f"tag:a{index:02d}"
            right = f"tag:b{index:02d}"
            nodes.extend(
                [
                    {"id": left, "name": left, "layer": "tag", "article_count": 1},
                    {"id": right, "name": right, "layer": "tag", "article_count": 1},
                ]
            )
            links.append(
                {
                    "id": f"edge:{index:02d}",
                    "source": left,
                    "target": right,
                    "type": "cooccurrence",
                    "weight": index + 1,
                }
            )

        first = build_weighted_tag_communities(nodes, links, max_communities=11)
        second = build_weighted_tag_communities(
            list(reversed(nodes)), list(reversed(links)), max_communities=11
        )

        self.assertEqual(first, second)
        self.assertEqual(first["algorithm"], "deterministic-weighted-label-propagation")
        self.assertEqual(len(first["communities"]), 12)
        self.assertEqual(first["communities"][-1]["id"], "community:other")
        self.assertEqual(first["communities"][-1]["name"], "其他")
        self.assertEqual(first["communities"][-1]["node_count"], 4)
        self.assertEqual(len(first["assignments"]), 26)
        self.assertEqual(
            len({community_id for community_id in first["assignments"].values()}), 12
        )

    def test_community_contract_aggregates_links_after_other_is_folded(self):
        nodes = [
            {"id": "tag:a", "name": "A", "layer": "tag", "article_count": 3},
            {"id": "tag:b", "name": "B", "layer": "tag", "article_count": 2},
            {"id": "tag:c", "name": "C", "layer": "tag", "article_count": 1},
        ]
        links = [
            {
                "source": "tag:a",
                "target": "tag:b",
                "type": "cooccurrence",
                "weight": 4,
            },
            {
                "source": "tag:b",
                "target": "tag:c",
                "type": "cooccurrence",
                "weight": 2,
            },
        ]

        result = build_weighted_tag_communities(
            nodes,
            links,
            max_communities=1,
            max_iterations=0,
        )

        self.assertEqual(
            result["links"],
            [
                {
                    "id": "edge:community:community:other->community:tag:a",
                    "source": "community:other",
                    "target": "community:tag:a",
                    "type": "community",
                    "weight": 4,
                    "strength": 1,
                }
            ],
        )
        self.assertTrue(
            all(link["source"] != link["target"] for link in result["links"])
        )

    def test_community_detection_normalizes_hub_edges_with_cosine_association(self):
        nodes = [
            {"id": "tag:a1", "name": "A1", "layer": "tag", "article_count": 5},
            {"id": "tag:a2", "name": "A2", "layer": "tag", "article_count": 5},
            {"id": "tag:b1", "name": "B1", "layer": "tag", "article_count": 5},
            {"id": "tag:b2", "name": "B2", "layer": "tag", "article_count": 5},
            {"id": "tag:hub", "name": "Hub", "layer": "tag", "article_count": 100},
        ]
        links = [
            {"source": "tag:a1", "target": "tag:a2", "type": "cooccurrence", "weight": 5},
            {"source": "tag:b1", "target": "tag:b2", "type": "cooccurrence", "weight": 5},
            {"source": "tag:hub", "target": "tag:a1", "type": "cooccurrence", "weight": 5},
            {"source": "tag:hub", "target": "tag:b1", "type": "cooccurrence", "weight": 5},
        ]

        result = build_weighted_tag_communities(nodes, links)

        assignments = result["assignments"]
        self.assertEqual(assignments["tag:a1"], assignments["tag:a2"])
        self.assertEqual(assignments["tag:b1"], assignments["tag:b2"])
        self.assertNotEqual(assignments["tag:a1"], assignments["tag:b1"])
        self.assertEqual(result["stats"]["weighting"], "cosine-association")
        self.assertGreaterEqual(result["stats"]["detected_communities"], 2)

    def test_community_article_count_uses_article_union_not_tag_occurrences(self):
        nodes = [
            {"id": "tag:a", "name": "A", "layer": "tag", "article_count": 2},
            {"id": "tag:b", "name": "B", "layer": "tag", "article_count": 2},
        ]
        links = [
            {"source": "tag:a", "target": "tag:b", "type": "cooccurrence", "weight": 2}
        ]

        result = build_weighted_tag_communities(
            nodes,
            links,
            article_memberships={
                "tag:a": {"article:1", "article:2"},
                "tag:b": {"article:1", "article:2"},
            },
        )

        self.assertEqual(len(result["communities"]), 1)
        self.assertEqual(result["communities"][0]["article_count"], 2)
        self.assertEqual(result["communities"][0]["tag_occurrences"], 4)

    def test_zero_weight_edges_do_not_join_communities(self):
        result = build_weighted_tag_communities(
            [
                {"id": "tag:a", "name": "A", "layer": "tag"},
                {"id": "tag:b", "name": "B", "layer": "tag"},
            ],
            [
                {
                    "source": "tag:a",
                    "target": "tag:b",
                    "type": "cooccurrence",
                    "weight": 0,
                }
            ],
        )

        self.assertNotEqual(
            result["assignments"]["tag:a"],
            result["assignments"]["tag:b"],
        )

    def test_v1_conversion_namespaces_endpoints_and_is_idempotent(self):
        v1 = {
            "nodes": [
                {"id": "python", "name": "Python", "layer": "language"},
                {
                    "id": "LLM",
                    "name": "LLM",
                    "layer": "tag",
                    "article_count": 3,
                    "community": "legacy-community",
                    "related_tags": ["Python"],
                },
                {
                    "id": "Kubernetes",
                    "name": "Kubernetes",
                    "layer": "concept",
                    "article_count": 2,
                    "related_concepts": ["LLM"],
                },
            ],
            "links": [
                {"source": "python", "target": "LLM", "strength": 0.6, "type": "semantic"},
                {"source": "LLM", "target": "Kubernetes", "weight": 2, "type": "cooccurrence"},
            ],
            "layers": {
                "language": {"name": "编程语言", "level": 1},
                "tag": {"name": "标签层", "level": 6},
                "concept": {"name": "概念层", "level": 7},
            },
        }

        converted = convert_v1_graph_to_v2(v1, generated_at="2026-01-01T00:00:00Z")
        converted_again = convert_v1_graph_to_v2(converted)

        self.assertEqual(converted, converted_again)
        self.assertEqual(converted["version"], 2)
        self.assertEqual(
            [node["id"] for node in converted["nodes"]],
            ["concept:Kubernetes", "tag:LLM", "tech:python"],
        )
        self.assertEqual(
            [(link["source"], link["target"]) for link in converted["links"]],
            [
                ("tag:LLM", "concept:Kubernetes"),
                ("tech:python", "tag:LLM"),
            ],
        )
        llm = next(node for node in converted["nodes"] if node["id"] == "tag:LLM")
        self.assertEqual(llm["degree"], 2)
        self.assertAlmostEqual(llm["weighted_degree"], 2.6)
        self.assertNotIn("related_tags", llm)
        self.assertNotIn("community", llm)
        self.assertEqual(llm["community_id"], "legacy-community")

    def test_v1_namespace_like_tag_text_is_preserved_without_collision(self):
        converted = convert_v1_graph_to_v2(
            {
                "nodes": [
                    {"id": "foo", "name": "Foo", "layer": "tag"},
                    {"id": "tag:foo", "name": "Literal tag:foo", "layer": "tag"},
                    {"id": "Y", "name": "Y", "layer": "tag"},
                ],
                "links": [
                    {
                        "source": "tag:foo",
                        "target": "Y",
                        "source_layer": "tag",
                        "target_layer": "tag",
                        "type": "cooccurrence",
                    }
                ],
            }
        )

        self.assertEqual(
            [node["id"] for node in converted["nodes"]],
            ["tag:foo", "tag:tag:foo", "tag:Y"],
        )
        self.assertEqual(
            (converted["links"][0]["source"], converted["links"][0]["target"]),
            ("tag:tag:foo", "tag:Y"),
        )

    def test_v2_namespace_layer_mismatch_fails_fast(self):
        with self.assertRaisesRegex(ValueError, "namespace.*layer"):
            convert_v1_graph_to_v2(
                {
                    "version": 2,
                    "nodes": [
                        {"id": "tech:X", "name": "X", "layer": "tag"},
                    ],
                    "links": [],
                }
            )

    def test_v1_duplicate_nodes_merge_deterministically(self):
        nodes = [
            {
                "id": "X",
                "name": "X",
                "layer": "tag",
                "description": "short",
                "article_count": 1,
            },
            {
                "id": "X",
                "name": "X",
                "layer": "tag",
                "description": "richer deterministic record",
                "article_count": 2,
            },
        ]

        first = convert_v1_graph_to_v2({"nodes": nodes, "links": []})
        second = convert_v1_graph_to_v2(
            {"nodes": list(reversed(nodes)), "links": []}
        )

        self.assertEqual(first, second)
        self.assertEqual(first["nodes"][0]["article_count"], 2)

    def test_v1_cooccurrence_resolves_the_only_shared_namespace(self):
        converted = convert_v1_graph_to_v2(
            {
                "nodes": [
                    {"id": "X", "name": "Tag X", "layer": "tag"},
                    {"id": "X", "name": "Concept X", "layer": "concept"},
                    {"id": "Y", "name": "Tag Y", "layer": "tag"},
                ],
                "links": [
                    {"source": "X", "target": "Y", "type": "cooccurrence"}
                ],
            }
        )

        self.assertEqual(
            (converted["links"][0]["source"], converted["links"][0]["target"]),
            ("tag:X", "tag:Y"),
        )

    def test_v1_ambiguous_cooccurrence_requires_layer_hints(self):
        with self.assertRaisesRegex(ValueError, "ambiguous cooccurrence"):
            convert_v1_graph_to_v2(
                {
                    "nodes": [
                        {"id": "X", "name": "Tag X", "layer": "tag"},
                        {"id": "X", "name": "Concept X", "layer": "concept"},
                        {"id": "Y", "name": "Tag Y", "layer": "tag"},
                        {"id": "Y", "name": "Concept Y", "layer": "concept"},
                    ],
                    "links": [
                        {"source": "X", "target": "Y", "type": "cooccurrence"}
                    ],
                }
            )

    def test_v1_non_finite_weight_falls_back_to_standard_json_number(self):
        converted = convert_v1_graph_to_v2(
            {
                "nodes": [
                    {"id": "A", "name": "A", "layer": "tag"},
                    {"id": "B", "name": "B", "layer": "tag"},
                ],
                "links": [
                    {
                        "source": "A",
                        "target": "B",
                        "type": "cooccurrence",
                        "weight": float("nan"),
                    }
                ],
            }
        )

        self.assertEqual(converted["links"][0]["weight"], 1)
        json.dumps(converted, allow_nan=False)

    def test_split_contract_writes_metadata_community_and_focus_shards(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            posts_dir = root / "posts"
            posts_dir.mkdir()
            result = self._build_sample(posts_dir)
            output_dir = write_tag_graph_split_from_result(
                result,
                output_dir=str(root / "out"),
                hot_tag_limit=3,
                hot_concept_limit=2,
            )

            index = json.loads((output_dir / "index.json").read_text(encoding="utf-8"))
            community = json.loads(
                (output_dir / "community.json").read_text(encoding="utf-8")
            )
            first_hotspot_file = community["communities"][0]["hotspot_file"]
            community_hotspots = json.loads(
                (output_dir / first_hotspot_file).read_text(encoding="utf-8")
            )
            hotspot_payloads = [
                json.loads((output_dir / item["hotspot_file"]).read_text(encoding="utf-8"))
                for item in community["communities"]
                if item.get("hotspot_file")
            ]
            search = json.loads((output_dir / "search.json").read_text(encoding="utf-8"))
            focus_shards = [
                json.loads((output_dir / filename).read_text(encoding="utf-8"))
                for filename in index["files"]["focusShards"]
            ]

        self.assertEqual(index["version"], 2)
        self.assertEqual(index["generated_at"], "2026-01-03T00:00:00Z")
        self.assertEqual(index["defaults"]["community_limit"], 11)
        self.assertEqual(index["defaults"]["community_hotspot_limit"], 24)
        self.assertEqual(index["defaults"]["community_hotspot_link_limit"], 32)
        self.assertEqual(index["defaults"]["mode"], "overview")
        self.assertEqual(index["files"]["community"], "community.json")
        self.assertEqual(
            index["files"]["communityHotspots"], "community-hotspots/"
        )
        self.assertEqual(index["files"]["search"], "search.json")
        self.assertEqual(len(index["files"]["focusShards"]), 128)
        self.assertTrue(
            all(
                re.fullmatch(
                    r"focus-shards/\d{3}-[0-9a-f]{12}\.json",
                    filename,
                )
                for filename in index["files"]["focusShards"]
            )
        )
        self.assertEqual(index["stats"]["total_nodes"], len(result["graph"]["nodes"]))

        self.assertEqual(community["version"], 2)
        self.assertNotIn("assignments", community)
        self.assertTrue(
            all("node_ids" not in item for item in community["communities"])
        )
        self.assertTrue(
            all(
                re.fullmatch(
                    r"community-hotspots/\d{2}-[0-9a-f]{12}\.json",
                    item["hotspot_file"],
                )
                for item in community["communities"]
                if item["id"] != "community:other"
            )
        )
        visible_communities = [
            item for item in community["communities"] if item["id"] != "community:other"
        ]
        self.assertEqual(
            {item["id"] for item in visible_communities},
            {payload["community_id"] for payload in hotspot_payloads},
        )
        self.assertTrue(
            all("hotspot_file" not in item for item in community["communities"] if item["id"] == "community:other")
        )
        for summary, payload in zip(visible_communities, hotspot_payloads):
            self.assertEqual(payload["community_id"], summary["id"])
            self.assertEqual(len(payload["nodes"]), min(summary["node_count"], 24))
            self.assertLessEqual(len(payload["links"]), 32)
            node_ids = {node["id"] for node in payload["nodes"]}
            self.assertTrue(
                all(
                    link["source"] in node_ids and link["target"] in node_ids
                    for link in payload["links"]
                )
            )
            self.assertEqual(
                [node["rank"] for node in payload["nodes"]],
                sorted(node["rank"] for node in payload["nodes"]),
            )
        all_hotspot_ids = [
            node["id"] for payload in hotspot_payloads for node in payload["nodes"]
        ]
        self.assertEqual(len(all_hotspot_ids), len(set(all_hotspot_ids)))
        self.assertEqual(community_hotspots["version"], 2)
        self.assertEqual(community_hotspots["hotspot_limit"], 24)
        self.assertEqual(
            community_hotspots["community_id"], community["communities"][0]["id"]
        )
        self.assertTrue(community_hotspots["nodes"])
        self.assertTrue(
            len(community_hotspots["nodes"]) <= 24
        )
        self.assertTrue(
            all(
                node["community_id"] == community_hotspots["community_id"]
                for node in community_hotspots["nodes"]
            )
        )
        self.assertTrue(
            all(
                {
                    "id",
                    "legacy_id",
                    "name",
                    "layer",
                    "category",
                    "description",
                    "article_count",
                    "degree",
                    "weighted_degree",
                    "community_id",
                    "rank",
                }
                <= set(node)
                for node in community_hotspots["nodes"]
            )
        )
        self.assertEqual(search["version"], 2)
        self.assertEqual(
            search["fields"],
            [
                "id",
                "legacy_id",
                "name",
                "layer",
                "category",
                "description",
                "article_count",
                "degree",
                "weighted_degree",
                "community_id",
                "rank",
            ],
        )
        self.assertTrue(search["items"])
        self.assertTrue(all(set(item) == set(search["fields"]) for item in search["items"]))
        self.assertTrue(all("community" not in item for item in search["items"]))
        self.assertTrue(all("text" not in item for item in search["items"]))
        self.assertEqual(
            [payload["bucket"] for payload in focus_shards], list(range(128))
        )
        self.assertTrue(
            all(
                set(payload) == {"version", "bucket", "algorithm", "entries"}
                and payload["version"] == 2
                and payload["algorithm"] == "fnv1a32"
                for payload in focus_shards
            )
        )
        emitted_focus_ids = [
            node_id
            for payload in focus_shards
            for node_id in payload["entries"]
        ]
        expected_focus_ids = {node["id"] for node in result["graph"]["nodes"]}
        self.assertEqual(set(emitted_focus_ids), expected_focus_ids)
        self.assertEqual(len(emitted_focus_ids), len(expected_focus_ids))
        self.assertTrue(
            all(
                _focus_shard_bucket(node_id) == payload["bucket"]
                for payload in focus_shards
                for node_id in payload["entries"]
            )
        )

    def test_focus_shards_use_stable_fnv_buckets_and_rank_strong_neighbors(self):
        def node(node_id: str, rank: int) -> dict:
            legacy_id = node_id.split(":", 1)[1]
            return {
                "id": node_id,
                "legacy_id": legacy_id,
                "name": legacy_id,
                "layer": node_id.split(":", 1)[0],
                "category": "fixture",
                "description": f"{legacy_id} description",
                "article_count": 1,
                "degree": 3,
                "weighted_degree": 9,
                "community_id": None,
                "rank": rank,
            }

        nodes = [
            node("tag:center", 1),
            node("tag:alpha", 2),
            node("tag:beta", 3),
            node("concept:gamma", 4),
        ]
        links = [
            {
                "id": "edge:beta-center",
                "source": "tag:beta",
                "target": "tag:center",
                "type": "cooccurrence",
                "weight": 7,
            },
            {
                "id": "edge:center-gamma",
                "source": "tag:center",
                "target": "concept:gamma",
                "type": "semantic",
                "weight": 9,
            },
            {
                "id": "edge:center-alpha",
                "source": "tag:center",
                "target": "tag:alpha",
                "type": "cooccurrence",
                "weight": 7,
            },
            {
                "id": "edge:center-alpha-weaker",
                "source": "tag:center",
                "target": "tag:alpha",
                "type": "semantic",
                "weight": 2,
            },
        ]

        first = _build_focus_shard_payloads(nodes, links)
        second = _build_focus_shard_payloads(
            list(reversed(nodes)), list(reversed(links))
        )

        self.assertEqual(first, second)
        self.assertEqual(len(first), 128)
        self.assertEqual(_focus_shard_bucket("hello"), 43)
        self.assertEqual(_focus_shard_bucket("tag:center"), 126)
        center_payload = first[_focus_shard_bucket("tag:center")][1]
        self.assertEqual(
            center_payload,
            {
                "version": 2,
                "bucket": 126,
                "algorithm": "fnv1a32",
                "entries": {
                    "tag:center": [
                        ["concept:gamma", 9, "semantic", 1],
                        ["tag:alpha", 7, "cooccurrence", 1],
                        ["tag:beta", 7, "cooccurrence", -1],
                    ]
                },
            },
        )
        alpha_payload = first[_focus_shard_bucket("tag:alpha")][1]
        self.assertEqual(
            alpha_payload["entries"]["tag:alpha"][0],
            ["tag:center", 7, "cooccurrence", -1],
        )
        self.assertTrue(
            all(
                len(neighbors) <= 24
                for _path, payload in first
                for neighbors in payload["entries"].values()
            )
        )

    def test_focus_shards_cap_each_node_at_24_unique_strongest_neighbors(self):
        nodes = [
            {"id": "tag:center"},
            *({"id": f"tag:n-{index:02d}"} for index in range(30)),
        ]
        links = [
            {
                "id": f"edge:{index:02d}",
                "source": "tag:center",
                "target": f"tag:n-{index:02d}",
                "type": "cooccurrence",
                "weight": index + 1,
            }
            for index in range(30)
        ]
        links.extend(
            [
                {
                    "id": "edge:duplicate-weaker",
                    "source": "tag:center",
                    "target": "tag:n-29",
                    "type": "semantic",
                    "weight": 1,
                },
                {
                    "id": "edge:self",
                    "source": "tag:center",
                    "target": "tag:center",
                    "type": "cooccurrence",
                    "weight": 100,
                },
                {
                    "id": "edge:dangling",
                    "source": "tag:center",
                    "target": "tag:missing",
                    "type": "cooccurrence",
                    "weight": 100,
                },
            ]
        )

        shards = _build_focus_shard_payloads(nodes, links)
        center = shards[_focus_shard_bucket("tag:center")][1]["entries"][
            "tag:center"
        ]

        self.assertEqual(len(center), 24)
        self.assertEqual(
            [entry[0] for entry in center],
            [f"tag:n-{index:02d}" for index in range(29, 5, -1)],
        )
        self.assertEqual([entry[1] for entry in center], list(range(30, 6, -1)))
        self.assertEqual(len({entry[0] for entry in center}), 24)

    def test_focus_shards_keep_one_previous_content_hash_generation(self):
        result = {
            "graph": {
                "version": 2,
                "generated_at": "2026-01-03T00:00:00Z",
                "nodes": [
                    {"id": "tag:alpha", "name": "Alpha", "layer": "tag"},
                    {"id": "tag:beta", "name": "Beta", "layer": "tag"},
                ],
                "links": [
                    {
                        "id": "edge:alpha-beta",
                        "source": "tag:alpha",
                        "target": "tag:beta",
                        "type": "cooccurrence",
                        "weight": 1,
                    }
                ],
                "layers": {"tag": {"name": "标签层", "level": 6}},
                "stats": {},
            }
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "out"
            write_tag_graph_split_from_result(result, output_dir=str(output))
            first_index = json.loads(
                (output / "index.json").read_text(encoding="utf-8")
            )
            first_paths = set(first_index["files"]["focusShards"])

            result["graph"]["links"][0]["weight"] = 2
            write_tag_graph_split_from_result(result, output_dir=str(output))
            second_index = json.loads(
                (output / "index.json").read_text(encoding="utf-8")
            )
            second_paths = set(second_index["files"]["focusShards"])
            first_changed_paths = first_paths - second_paths
            first_generation_retained = all(
                (output / path).exists() for path in first_changed_paths
            )

            result["graph"]["links"][0]["weight"] = 3
            write_tag_graph_split_from_result(result, output_dir=str(output))
            third_index = json.loads(
                (output / "index.json").read_text(encoding="utf-8")
            )
            third_paths = set(third_index["files"]["focusShards"])
            second_changed_paths = second_paths - third_paths
            first_generation_removed = all(
                not (output / path).exists() for path in first_changed_paths
            )
            second_generation_retained = all(
                (output / path).exists() for path in second_changed_paths
            )

        self.assertTrue(first_changed_paths)
        self.assertTrue(second_changed_paths)
        self.assertTrue(first_generation_retained)
        self.assertTrue(first_generation_removed)
        self.assertTrue(second_generation_retained)

    def test_community_hotspot_shards_apply_exact_node_and_edge_budgets(self):
        nodes = [
            {
                "id": f"tag:n-{index:02d}",
                "legacy_id": f"n-{index:02d}",
                "name": f"Node {index:02d}",
                "layer": "tag",
                "category": "article_tag",
                "description": f"Node {index:02d} description",
                "article_count": 1,
                "degree": 29,
                "weighted_degree": 29,
                "community_id": None,
                "rank": index + 1,
            }
            for index in range(30)
        ]
        links = [
            {
                "id": f"edge:{source:02d}:{target:02d}",
                "source": f"tag:n-{source:02d}",
                "target": f"tag:n-{target:02d}",
                "type": "cooccurrence",
                "weight": 1,
                "strength": 1,
            }
            for source in range(30)
            for target in range(source + 1, 30)
        ]
        result = {
            "graph": {
                "version": 2,
                "generated_at": "2026-01-03T00:00:00Z",
                "nodes": nodes,
                "links": links,
                "layers": {"tag": {"name": "标签层", "level": 6}},
                "stats": {},
            }
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            output = write_tag_graph_split_from_result(
                result,
                output_dir=str(Path(tmp_dir) / "out"),
            )
            summary = json.loads((output / "community.json").read_text(encoding="utf-8"))
            shard = json.loads(
                (output / summary["communities"][0]["hotspot_file"]).read_text(
                    encoding="utf-8"
                )
            )
            changed_result = json.loads(json.dumps(result))
            changed_result["graph"]["nodes"][0]["description"] = "Changed payload"
            changed_output = write_tag_graph_split_from_result(
                changed_result,
                output_dir=str(output),
            )
            changed_summary = json.loads(
                (changed_output / "community.json").read_text(encoding="utf-8")
            )
            first_hotspot_file = summary["communities"][0]["hotspot_file"]
            second_hotspot_file = changed_summary["communities"][0]["hotspot_file"]
            first_retained_for_rolling_clients = (output / first_hotspot_file).exists()
            third_result = json.loads(json.dumps(changed_result))
            third_result["graph"]["nodes"][1]["description"] = "Third payload"
            write_tag_graph_split_from_result(third_result, output_dir=str(output))
            first_removed_after_grace_generation = not (output / first_hotspot_file).exists()
            second_retained_for_rolling_clients = (output / second_hotspot_file).exists()

        self.assertEqual(summary["communities"][0]["node_count"], 30)
        self.assertEqual(summary["communities"][0]["hotspot_count"], 24)
        self.assertEqual(
            [node["id"] for node in shard["nodes"]],
            [f"tag:n-{index:02d}" for index in range(24)],
        )
        self.assertEqual(len(shard["links"]), 32)
        expected_ids = [link["id"] for link in links if link["target"] <= "tag:n-23"][:32]
        self.assertEqual([link["id"] for link in shard["links"]], expected_ids)
        self.assertEqual(shard["stats"], {"total_nodes": 24, "total_links": 32})
        self.assertEqual(shard["generated_at"], "2026-01-03T00:00:00Z")
        self.assertNotEqual(
            summary["communities"][0]["hotspot_file"],
            changed_summary["communities"][0]["hotspot_file"],
        )
        self.assertTrue(first_retained_for_rolling_clients)
        self.assertTrue(first_removed_after_grace_generation)
        self.assertTrue(second_retained_for_rolling_clients)

    def test_search_index_is_stable_and_rank_ordered(self):
        nodes = [
            {
                "id": "tag:Beta",
                "name": "Beta",
                "layer": "tag",
                "rank": 2,
                "category": "article_tag",
                "description": "  SECOND   description  ",
                "community_id": "community:beta",
            },
            {
                "id": "tech:alpha",
                "name": "Alpha",
                "layer": "language",
                "rank": 1,
                "category": "language",
                "description": "First description",
            },
        ]

        first = build_search_index(nodes, generated_at="2026-01-01T00:00:00Z")
        second = build_search_index(
            list(reversed(nodes)), generated_at="2026-01-01T00:00:00Z"
        )

        self.assertEqual(first, second)
        self.assertEqual([item["id"] for item in first["items"]], ["tech:alpha", "tag:Beta"])
        self.assertEqual(
            first["items"][1]["description"], "  SECOND   description  "
        )
        self.assertEqual(first["items"][1]["legacy_id"], "Beta")
        self.assertNotIn("text", first["items"][1])

    def test_same_content_produces_byte_identical_split_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            first_posts = root / "posts-a"
            second_posts = root / "posts-b"
            first_posts.mkdir()
            second_posts.mkdir()

            first_result = self._build_sample(first_posts)
            second_result = self._build_sample(second_posts, reverse=True)
            first_out = write_tag_graph_split_from_result(
                first_result, output_dir=str(root / "out-a"), hot_tag_limit=3
            )
            second_out = write_tag_graph_split_from_result(
                second_result, output_dir=str(root / "out-b"), hot_tag_limit=3
            )

            first_files = sorted(
                path.relative_to(first_out) for path in first_out.rglob("*.json")
            )
            second_files = sorted(
                path.relative_to(second_out) for path in second_out.rglob("*.json")
            )
            self.assertEqual(first_files, second_files)
            for filename in first_files:
                self.assertEqual(
                    (first_out / filename).read_bytes(),
                    (second_out / filename).read_bytes(),
                    filename,
                )


if __name__ == "__main__":
    unittest.main()
