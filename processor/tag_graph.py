"""
标签图谱构建器
从博客文章中提取标签，构建标签关联图谱
支持基于现有内容挖掘标签和概念
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional
from collections import defaultdict
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off"}


def get_tag_graph_runtime_options() -> Dict[str, bool]:
    return {
        "enable_content_mining": _env_flag("TAG_GRAPH_ENABLE_CONTENT_MINING", True),
    }


class TagGraphBuilder:
    """标签图谱构建器 - 基于文章标签共现关系和内容挖掘构建图谱"""

    def __init__(self, content_dir: str = "blog/content/posts", enable_content_mining: bool = True):
        self.content_dir = Path(content_dir)
        self.tags: Dict[str, Dict] = {}
        self.tag_cooccurrence: Dict[Tuple[str, str], int] = defaultdict(int)
        self.article_tags: Dict[str, List[str]] = {}
        self.article_concepts: Dict[str, List[str]] = {}
        self.concept_cooccurrence: Dict[Tuple[str, str], int] = defaultdict(int)
        self.concepts: Dict[str, Dict] = {}
        self.enable_content_mining = enable_content_mining

    def extract_tags_from_articles(self) -> None:
        """从所有文章中提取标签和概念"""
        if not self.content_dir.exists():
            print(f"Content directory not found: {self.content_dir}")
            return

        md_files = list(self.content_dir.glob("**/*.md"))
        print(f"Found {len(md_files)} markdown files")

        for md_file in md_files:
            self._parse_article_tags(md_file)
            if self.enable_content_mining:
                self._mine_article_concepts(md_file)

        print(f"Extracted {len(self.tags)} unique tags from {len(self.article_tags)} articles")
        if self.enable_content_mining:
            print(f"Mined {len(self.concepts)} unique concepts from {len(self.article_concepts)} articles")

    def _parse_article_tags(self, md_file: Path) -> None:
        """解析单篇文章的标签"""
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r'^tags:\s*\[(.*?)\]', content, re.MULTILINE)
        if match:
            tags_str = match.group(1)
            tags = [tag.strip().strip('"\'') for tag in tags_str.split(",") if tag.strip()]
            
            article_title = self._extract_title(content)
            self.article_tags[article_title] = tags

            for tag in tags:
                if tag not in self.tags:
                    self.tags[tag] = {
                        "id": tag,
                        "name": tag,
                        "layer": "tag",
                        "category": "article_tag",
                        "description": f"文章标签: {tag}",
                        "article_count": 0,
                        "related_tags": set(),
                    }
                self.tags[tag]["article_count"] += 1

            self._update_cooccurrence(tags)

    def _extract_title(self, content: str) -> str:
        """提取文章标题"""
        match = re.search(r'^title:\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        return match.group(1) if match else "Untitled"

    def _mine_article_concepts(self, md_file: Path) -> None:
        """从文章内容中挖掘概念和关键词"""
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        article_title = self._extract_title(content)
        
        title_concepts = self._extract_concepts_from_text(article_title)
        body_concepts = self._extract_concepts_from_text(content)
        
        all_concepts = list(set(title_concepts + body_concepts))
        self.article_concepts[article_title] = all_concepts

        for concept in all_concepts:
            if concept not in self.concepts:
                self.concepts[concept] = {
                    "id": concept,
                    "name": concept,
                    "layer": "concept",
                    "category": "mined_concept",
                    "description": f"从内容挖掘的概念: {concept}",
                    "article_count": 0,
                    "related_concepts": set(),
                }
            self.concepts[concept]["article_count"] += 1

        self._update_concept_cooccurrence(all_concepts)

    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """从文本中提取概念和关键词"""
        concepts = []
        
        frontmatter_end = text.find("---", 3)
        if frontmatter_end != -1:
            text = text[frontmatter_end + 3:]
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            
            if line.startswith('#') or line.startswith('*') or line.startswith('-'):
                continue
            
            keywords = self._extract_keywords(line)
            concepts.extend(keywords)
        
        return concepts

    def _extract_keywords(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        keywords = []
        
        tech_patterns = [
            r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b',
            r'\b(?:AI|ML|LLM|GPT|API|SDK|REST|GraphQL|HTTP|HTTPS|TCP|UDP|DNS|URL|URI)\b',
            r'\b(?:Python|Java|JavaScript|TypeScript|Go|Rust|C\+\+|Swift|Kotlin|PHP|Ruby)\b',
            r'\b(?:React|Vue|Angular|Node\.js|Express|Django|Flask|Spring|Laravel)\b',
            r'\b(?:Docker|Kubernetes|K8s|AWS|Azure|GCP|Terraform|Ansible|Jenkins)\b',
            r'\b(?:TensorFlow|PyTorch|Keras|Scikit|Pandas|NumPy|Matplotlib)\b',
            r'\b(?:PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch|Cassandra|InfluxDB)\b',
            r'\b(?:Linux|Unix|Windows|macOS|Android|iOS)\b',
            r'\b(?:Git|GitHub|GitLab|Bitbucket|SVN)\b',
            r'\b(?:CI|CD|DevOps|Agile|Scrum|Kanban|TDD|BDD)\b',
            r'\b(?:Microservices|Serverless|Monolith|SOA|Event-driven)\b',
            r'\b(?:OAuth|JWT|SSL|TLS|HTTPS|SSH|SFTP)\b',
            r'\b(?:NoSQL|SQL|ORM|ODM)\b',
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            keywords.extend(matches)
        
        return keywords

    def _update_concept_cooccurrence(self, concepts: List[str]) -> None:
        """更新概念共现关系"""
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                pair = tuple(sorted([concept1, concept2]))
                self.concept_cooccurrence[pair] += 1
                self.concepts[concept1]["related_concepts"].add(concept2)
                self.concepts[concept2]["related_concepts"].add(concept1)

    def _update_cooccurrence(self, tags: List[str]) -> None:
        """更新标签共现关系"""
        for i, tag1 in enumerate(tags):
            for tag2 in tags[i+1:]:
                pair = tuple(sorted([tag1, tag2]))
                self.tag_cooccurrence[pair] += 1
                self.tags[tag1]["related_tags"].add(tag2)
                self.tags[tag2]["related_tags"].add(tag1)

    def get_tag_nodes(self) -> List[Dict]:
        """获取标签节点列表"""
        nodes = []
        for tag_id, tag_data in self.tags.items():
            nodes.append({
                "id": tag_id,
                "name": tag_data["name"],
                "layer": "tag",
                "layer_name": "标签层",
                "level": 6,
                "color": "#f59e0b",
                "category": tag_data["category"],
                "description": tag_data["description"],
                "article_count": tag_data["article_count"],
                "related_count": len(tag_data["related_tags"]),
                "related_tags": list(tag_data["related_tags"]),
            })
        return nodes

    def get_tag_links(self, min_cooccurrence: int = 1) -> List[Dict]:
        """获取标签间关联（基于共现）"""
        links = []
        for (tag1, tag2), count in self.tag_cooccurrence.items():
            if count >= min_cooccurrence:
                links.append({
                    "source": tag1,
                    "target": tag2,
                    "strength": min(count / 2, 1.0),
                    "type": "cooccurrence",
                })
        return links

    def get_concept_nodes(self) -> List[Dict]:
        """获取概念节点列表"""
        nodes = []
        for concept_id, concept_data in self.concepts.items():
            nodes.append({
                "id": concept_id,
                "name": concept_data["name"],
                "layer": "concept",
                "layer_name": "概念层",
                "level": 7,
                "color": "#6366f1",
                "category": concept_data["category"],
                "description": concept_data["description"],
                "article_count": concept_data["article_count"],
                "related_count": len(concept_data["related_concepts"]),
                "related_concepts": list(concept_data["related_concepts"]),
            })
        return nodes

    def get_concept_links(self, min_cooccurrence: int = 1) -> List[Dict]:
        """获取概念间关联（基于共现）"""
        links = []
        for (concept1, concept2), count in self.concept_cooccurrence.items():
            if count >= min_cooccurrence:
                links.append({
                    "source": concept1,
                    "target": concept2,
                    "strength": min(count / 2, 1.0),
                    "type": "cooccurrence",
                })
        return links

    def build_tag_to_tech_links(self, tech_nodes: List[Dict]) -> List[Dict]:
        """建立标签与技术栈节点的关联（基于名称匹配）"""
        links = []
        tech_names = {node["id"]: node for node in tech_nodes}

        for tag_name in self.tags.keys():
            for tech_id, tech_node in tech_names.items():
                if self._is_semantically_related(tag_name, tech_id, tech_node):
                    links.append({
                        "source": tag_name,
                        "target": tech_id,
                        "strength": 0.6,
                        "type": "semantic",
                    })
        return links

    def _is_semantically_related(self, tag: str, tech_id: str, tech_node: Dict) -> bool:
        """判断标签与技术节点是否语义相关"""
        tag_lower = tag.lower()
        
        exact_match = tag_lower == tech_id.lower()
        contains = tag_lower in tech_id.lower() or tech_id.lower() in tag_lower
        category_match = tag_lower == tech_node.get("category", "").lower()

        return exact_match or contains or category_match

    def get_stats(self) -> Dict:
        """获取统计数据"""
        most_used_tags = sorted(
            self.tags.items(),
            key=lambda x: x[1]["article_count"],
            reverse=True
        )[:5]

        most_used_concepts = sorted(
            self.concepts.items(),
            key=lambda x: x[1]["article_count"],
            reverse=True
        )[:5]
        
        return {
            "total_tags": len(self.tags),
            "total_concepts": len(self.concepts),
            "total_articles": len(self.article_tags),
            "total_tag_links": len(self.tag_cooccurrence),
            "total_concept_links": len(self.concept_cooccurrence),
            "avg_tags_per_article": sum(len(tags) for tags in self.article_tags.values()) / len(self.article_tags) if self.article_tags else 0,
            "avg_concepts_per_article": sum(len(concepts) for concepts in self.article_concepts.values()) / len(self.article_concepts) if self.article_concepts else 0,
            "most_used_tags": [
                (tag_name, {
                    **tag_data,
                    "related_tags": list(tag_data["related_tags"]),
                })
                for tag_name, tag_data in most_used_tags
            ],
            "most_used_concepts": [
                (concept_name, {
                    **concept_data,
                    "related_concepts": list(concept_data["related_concepts"]),
                })
                for concept_name, concept_data in most_used_concepts
            ],
        }


def export_tag_graph(
    output_path: str = "blog/static/data/tag-graph.json",
    min_cooccurrence: int = 1,
    enable_content_mining: bool = True,
    content_dir: str = "blog/content/posts",
) -> Path:
    """导出标签图谱数据（包含标签和概念层）"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from tech_stack import build_graph_data

    data = build_tag_graph_data(
        min_cooccurrence=min_cooccurrence,
        enable_content_mining=enable_content_mining,
        existing_output_path=output_path,
        content_dir=content_dir,
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(data["graph"], f, ensure_ascii=False, indent=2)

    return output


def build_tag_graph_data(
    min_cooccurrence: int = 1,
    enable_content_mining: Optional[bool] = None,
    existing_output_path: Optional[str] = None,
    content_dir: str = "blog/content/posts",
) -> Dict[str, Any]:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from tech_stack import build_graph_data

    existing_tag_descriptions: Dict[str, str] = {}
    if existing_output_path:
        output = Path(existing_output_path)
        if output.exists():
            try:
                with open(output, "r", encoding="utf-8") as f:
                    existing = json.load(f) or {}
                for node in existing.get("nodes", []) or []:
                    if node.get("layer") != "tag":
                        continue
                    node_id = node.get("id")
                    desc = (node.get("description") or "").strip()
                    if not node_id or not desc:
                        continue
                    existing_tag_descriptions[str(node_id)] = desc
            except Exception as e:
                logger.warning(f"Failed to load existing tag descriptions: {e}")

    runtime_options = get_tag_graph_runtime_options()
    if enable_content_mining is None:
        enable_content_mining = runtime_options["enable_content_mining"]

    builder = TagGraphBuilder(content_dir=content_dir, enable_content_mining=enable_content_mining)
    builder.extract_tags_from_articles()

    def is_default_tag_description(tag_name: str, desc: str) -> bool:
        d = (desc or "").strip()
        if not d:
            return True
        if d == f"文章标签: {tag_name}":
            return True
        if d == f"文章标签:{tag_name}":
            return True
        return d.startswith("文章标签:") and tag_name in d and len(d) <= len(f"文章标签: {tag_name}") + 2

    for tag_name, tag_data in builder.tags.items():
        existing_desc = existing_tag_descriptions.get(tag_name)
        if existing_desc and not is_default_tag_description(tag_name, existing_desc):
            tag_data["description"] = existing_desc

    enable_llm_intros = os.environ.get("TAG_INTRO_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}
    max_new_intros_raw = os.environ.get("TAG_INTRO_MAX_NEW", "80").strip()
    try:
        max_new_intros = max(0, int(max_new_intros_raw))
    except Exception:
        max_new_intros = 80

    client = None
    if enable_llm_intros and max_new_intros > 0:
        try:
            try:
                from processor.anthropic_client import AnthropicClient
            except Exception:
                from anthropic_client import AnthropicClient
            client = AnthropicClient()
        except Exception as e:
            logger.warning(f"Tag intro generation disabled: {e}")

    if client:
        tags_needing_intros = []
        for tag_name, tag_data in builder.tags.items():
            if is_default_tag_description(tag_name, tag_data.get("description", "")):
                tags_needing_intros.append(tag_name)

        tags_needing_intros.sort(
            key=lambda t: (-int(builder.tags[t].get("article_count", 0) or 0), t)
        )

        if tags_needing_intros:
            tag_to_articles: Dict[str, List[str]] = defaultdict(list)
            for title, tags in (builder.article_tags or {}).items():
                for tag in tags:
                    tag_to_articles[tag].append(title)

            for tag_name in tags_needing_intros[:max_new_intros]:
                tag_data = builder.tags.get(tag_name) or {}
                related = sorted(list(tag_data.get("related_tags") or []))[:10]
                titles = tag_to_articles.get(tag_name, [])[:8]
                article_count = int(tag_data.get("article_count", 0) or 0)

                context_lines = [
                    f"标签: {tag_name}",
                    f"出现文章数: {article_count}",
                ]
                if related:
                    context_lines.append(f"相关标签: {', '.join(related)}")
                if titles:
                    context_lines.append("出现文章标题样例:")
                    context_lines.extend([f"- {t}" for t in titles])
                context = "\n".join(context_lines)

                prompt = (
                    "你是一个技术内容策展人。请为给定“标签”写一段简介，用于知识图谱节点的介绍。\n"
                    "要求:\n"
                    "1) 用中文，1-2 句话即可\n"
                    "2) 解释它通常指什么、与什么相关\n"
                    "3) 不要列清单，不要加引号，不要输出 JSON\n"
                    "4) 字数尽量控制在 30-80 字\n\n"
                    f"{context}"
                )

                try:
                    raw = client.create_message(
                        prompt,
                        max_tokens=140,
                        temperature=0.3,
                        purpose="tag_intro",
                    )
                    intro = (raw or "").strip().strip('"').strip()
                    if intro:
                        tag_data["description"] = intro.replace("\r\n", "\n").strip()
                except Exception as e:
                    logger.warning(f"Failed to generate intro for tag '{tag_name}': {e}")

    tag_nodes = builder.get_tag_nodes()
    tag_links = builder.get_tag_links(min_cooccurrence)

    concept_nodes = builder.get_concept_nodes() if enable_content_mining else []
    concept_links = builder.get_concept_links(min_cooccurrence) if enable_content_mining else []

    tech_data = build_graph_data()
    tech_nodes = tech_data["nodes"]
    tech_links = tech_data["links"]

    tag_to_tech_links = builder.build_tag_to_tech_links(tech_nodes)

    all_nodes = tech_nodes + tag_nodes + concept_nodes
    all_links = tech_links + tag_links + tag_to_tech_links + concept_links

    layers = {
        "language": {"name": "编程语言", "level": 1, "color": "#4db6ac"},
        "framework": {"name": "框架层", "level": 2, "color": "#26a69a"},
        "model": {"name": "模型层", "level": 3, "color": "#d97706"},
        "application": {"name": "应用层", "level": 4, "color": "#8b5cf6"},
        "scenario": {"name": "场景层", "level": 5, "color": "#ec4899"},
        "tag": {"name": "标签层", "level": 6, "color": "#f59e0b"},
        "concept": {"name": "概念层", "level": 7, "color": "#6366f1"},
    }

    graph = {
        "nodes": all_nodes,
        "links": all_links,
        "layers": layers,
        "stats": {
            "total_nodes": len(all_nodes),
            "total_links": len(all_links),
            "tag_stats": builder.get_stats(),
        },
    }

    return {
        "graph": graph,
        "parts": {
            "tech_nodes": tech_nodes,
            "tech_links": tech_links,
            "tag_nodes": tag_nodes,
            "tag_links": tag_links,
            "tag_to_tech_links": tag_to_tech_links,
            "concept_nodes": concept_nodes,
            "concept_links": concept_links,
        },
        "layers": layers,
        "stats": graph["stats"],
    }


def export_tag_graph_split(
    output_dir: str = "blog/static/data/tag-graph",
    min_cooccurrence: int = 1,
    enable_content_mining: bool = True,
    hot_tag_limit: int = 250,
    hot_concept_limit: int = 150,
    content_dir: str = "blog/content/posts",
) -> Path:
    result = build_tag_graph_data(
        min_cooccurrence=min_cooccurrence,
        enable_content_mining=enable_content_mining,
        existing_output_path="blog/static/data/tag-graph/tag.json",
        content_dir=content_dir,
    )
    return write_tag_graph_split_from_result(
        result=result,
        output_dir=output_dir,
        hot_tag_limit=hot_tag_limit,
        hot_concept_limit=hot_concept_limit,
    )


def write_tag_graph_split_from_result(
    result: Dict[str, Any],
    output_dir: str = "blog/static/data/tag-graph",
    hot_tag_limit: int = 250,
    hot_concept_limit: int = 150,
) -> Path:

    layers = result["layers"]
    parts = result["parts"]
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tech_layers = {"language", "framework", "model", "application", "scenario"}
    core_nodes = [n for n in parts["tech_nodes"] if n.get("layer") in tech_layers]
    core_links = list(parts["tech_links"])

    tag_nodes = list(parts["tag_nodes"])
    concept_nodes = list(parts["concept_nodes"])
    tag_links = list(parts["tag_links"])
    tag_to_tech_links = list(parts["tag_to_tech_links"])
    concept_links = list(parts["concept_links"])

    tag_nodes_sorted = sorted(tag_nodes, key=lambda n: (-int(n.get("article_count", 0) or 0), str(n.get("id") or "")))
    hot_tag_ids = set([n["id"] for n in tag_nodes_sorted[:max(0, int(hot_tag_limit))] if n.get("id")])
    hot_tag_nodes = [n for n in tag_nodes if n.get("id") in hot_tag_ids]
    hot_tag_links = [l for l in tag_links if l.get("source") in hot_tag_ids and l.get("target") in hot_tag_ids]
    hot_tag_to_tech_links = [l for l in tag_to_tech_links if l.get("source") in hot_tag_ids]

    concept_nodes_sorted = sorted(concept_nodes, key=lambda n: (-int(n.get("article_count", 0) or 0), str(n.get("id") or "")))
    hot_concept_ids = set([n["id"] for n in concept_nodes_sorted[:max(0, int(hot_concept_limit))] if n.get("id")])
    hot_concept_nodes = [n for n in concept_nodes if n.get("id") in hot_concept_ids]
    hot_concept_links = [l for l in concept_links if l.get("source") in hot_concept_ids and l.get("target") in hot_concept_ids]

    def write_json(rel_path: str, payload: Dict[str, Any]) -> None:
        target = out_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    write_json("index.json", {
        "version": 1,
        "layers": layers,
        "files": {
            "core": "core.json",
            "tagHot": "tag.hot.json",
            "conceptHot": "concept.hot.json",
            "tag": "tag.json",
        },
        "defaults": {
            "hot_tag_limit": hot_tag_limit,
            "hot_concept_limit": hot_concept_limit,
            "initial_visible_layers": ["language", "framework", "model", "application", "scenario"],
        },
    })

    write_json("core.json", {
        "nodes": core_nodes,
        "links": core_links,
        "layers": layers,
        "stats": {
            "total_nodes": len(core_nodes),
            "total_links": len(core_links),
        },
    })

    write_json("tag.hot.json", {
        "nodes": hot_tag_nodes,
        "links": hot_tag_links + hot_tag_to_tech_links,
        "layer": "tag",
        "layers": layers,
        "stats": {
            "total_nodes": len(hot_tag_nodes),
            "total_links": len(hot_tag_links) + len(hot_tag_to_tech_links),
        },
    })

    write_json("concept.hot.json", {
        "nodes": hot_concept_nodes,
        "links": hot_concept_links,
        "layer": "concept",
        "layers": layers,
        "stats": {
            "total_nodes": len(hot_concept_nodes),
            "total_links": len(hot_concept_links),
        },
    })

    write_json("tag.json", {
        "nodes": tag_nodes,
        "links": tag_links + tag_to_tech_links,
        "layer": "tag",
        "layers": layers,
        "stats": {
            "total_nodes": len(tag_nodes),
            "total_links": len(tag_links) + len(tag_to_tech_links),
        },
    })

    return out_dir


if __name__ == "__main__":
    runtime_options = get_tag_graph_runtime_options()
    result = build_tag_graph_data(
        min_cooccurrence=1,
        enable_content_mining=runtime_options["enable_content_mining"],
        existing_output_path="blog/static/data/tag-graph/tag.json",
    )
    out_dir = write_tag_graph_split_from_result(result=result)
    print(f"\n已导出标签图谱到: {out_dir}")

    data = result["graph"]

    print(f"\n图谱统计:")
    print(f"  总节点数: {data['stats']['total_nodes']}")
    print(f"  总连线数: {data['stats']['total_links']}")
    print(f"\n标签统计:")
    tag_stats = data['stats']['tag_stats']
    print(f"  标签总数: {tag_stats['total_tags']}")
    print(f"  概念总数: {tag_stats['total_concepts']}")
    print(f"  文章总数: {tag_stats['total_articles']}")
    print(f"  标签间连线: {tag_stats['total_tag_links']}")
    print(f"  概念间连线: {tag_stats['total_concept_links']}")
    print(f"  平均每篇文章标签数: {tag_stats['avg_tags_per_article']:.1f}")
    print(f"  平均每篇文章概念数: {tag_stats['avg_concepts_per_article']:.1f}")
    print(f"\n最常用标签:")
    for tag_name, tag_data in tag_stats['most_used_tags']:
        print(f"  - {tag_name}: {tag_data['article_count']} 篇文章")
    print(f"\n最常用概念:")
    for concept_name, concept_data in tag_stats['most_used_concepts']:
        print(f"  - {concept_name}: {concept_data['article_count']} 篇文章")
