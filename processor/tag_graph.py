"""
标签图谱构建器
从博客文章中提取标签，构建标签关联图谱
支持基于现有内容挖掘标签和概念
"""

import hashlib
import json
import logging
import math
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from ai_stack.content_quality import (
    analyze_post,
    body_completeness_reasons,
    synthetic_body_reasons,
)
from ai_stack.identity import canonicalize_url
from ai_stack.tag_taxonomy import normalize_tags

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GRAPH_VERSION = 2
DEFAULT_GENERATED_AT = "1970-01-01T00:00:00Z"
DEFAULT_COMMUNITY_LIMIT = 11
COMMUNITY_HOTSPOT_LIMIT = 24
COMMUNITY_HOTSPOT_LINK_LIMIT = 32
FOCUS_SHARD_COUNT = 128
FOCUS_NEIGHBOR_LIMIT = 24
FOCUS_SHARD_ALGORITHM = "fnv1a32"
TECH_LAYERS = {"language", "framework", "model", "application", "scenario"}
NODE_NAMESPACES = {"tech", "tag", "concept"}
GRAPH_NODE_V2_FIELDS = [
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
]

def _stable_text_key(value: Any) -> Tuple[str, str]:
    text = str(value or "")
    return text.casefold(), text


def _normalize_generated_at(value: Any) -> Optional[str]:
    """Normalize a source timestamp to a stable UTC ISO-8601 string."""
    raw = str(value or "").strip().strip('"\'')
    if not raw:
        return None

    candidate = raw.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    parsed = parsed.astimezone(timezone.utc).replace(microsecond=0)
    return parsed.isoformat().replace("+00:00", "Z")


def _namespace_for_layer(layer: Any) -> str:
    normalized = str(layer or "").strip().lower()
    if normalized == "tag":
        return "tag"
    if normalized == "concept":
        return "concept"
    return "tech"


def _namespace_node_id(
    node_id: Any,
    layer: Any,
    *,
    already_namespaced: bool = False,
) -> str:
    raw = str(node_id or "").strip()
    expected_namespace = _namespace_for_layer(layer)
    if not already_namespaced:
        return f"{expected_namespace}:{raw}"

    prefix = raw.split(":", 1)[0] if ":" in raw else ""
    if prefix != expected_namespace:
        raise ValueError(
            f"node namespace '{prefix or '<missing>'}' does not match layer '{layer}'"
        )
    return raw


def _legacy_node_id(node_id: Any) -> str:
    raw = str(node_id or "")
    prefix, separator, remainder = raw.partition(":")
    if separator and prefix in NODE_NAMESPACES:
        return remainder
    return raw


def _numeric_weight(value: Any, default: float = 1.0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(result):
        return default
    if result < 0:
        return 0.0
    return result


def _compact_number(value: float) -> Any:
    rounded = round(float(value), 6)
    if rounded.is_integer():
        return int(rounded)
    return rounded


def _edge_sort_key(link: Dict[str, Any]) -> Tuple[str, str, str, str]:
    return (
        str(link.get("source") or ""),
        str(link.get("target") or ""),
        str(link.get("type") or ""),
        str(link.get("id") or ""),
    )


def _graph_stats(
    nodes: List[Dict[str, Any]],
    links: List[Dict[str, Any]],
    *,
    tag_stats: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    nodes_by_layer: Dict[str, int] = defaultdict(int)
    links_by_type: Dict[str, int] = defaultdict(int)
    for node in nodes:
        nodes_by_layer[str(node.get("layer") or "unknown")] += 1
    for link in links:
        links_by_type[str(link.get("type") or "relation")] += 1

    stats: Dict[str, Any] = {
        "total_nodes": len(nodes),
        "total_links": len(links),
        "nodes_by_layer": dict(sorted(nodes_by_layer.items())),
        "links_by_type": dict(sorted(links_by_type.items())),
    }
    if tag_stats is not None:
        stats["tag_stats"] = tag_stats
        stats["total_articles"] = int(tag_stats.get("total_articles", 0) or 0)
    return stats


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
        self.article_titles: Dict[str, str] = {}
        self.article_concepts: Dict[str, List[str]] = {}
        self.concept_cooccurrence: Dict[Tuple[str, str], int] = defaultdict(int)
        self.concepts: Dict[str, Dict] = {}
        self.source_dates: List[str] = []
        self.enable_content_mining = enable_content_mining
        self.canonical_duplicate_files_skipped = 0
        self.archived_article_groups_skipped = 0
        self.archived_article_files_skipped = 0
        self.incomplete_article_groups_skipped = 0
        self.incomplete_article_files_skipped = 0
        self.synthetic_article_groups_skipped = 0
        self.synthetic_article_files_skipped = 0

    @property
    def generated_at(self) -> str:
        return max(self.source_dates, default=DEFAULT_GENERATED_AT)

    def _article_key(self, md_file: Path) -> str:
        try:
            return md_file.relative_to(self.content_dir).as_posix()
        except ValueError:
            return md_file.as_posix()

    def extract_tags_from_articles(self) -> None:
        """从所有文章中提取标签和概念"""
        if not self.content_dir.exists():
            print(f"Content directory not found: {self.content_dir}")
            return

        md_files = sorted(
            self.content_dir.glob("**/*.md"),
            key=lambda path: _stable_text_key(path.as_posix()),
        )
        print(f"Found {len(md_files)} markdown files")

        grouped_articles: Dict[str, List[Tuple[Path, str, Dict[str, Any]]]] = defaultdict(list)
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            frontmatter = self._extract_frontmatter(content)
            identity = self._canonical_article_identity(md_file, frontmatter)
            grouped_articles[identity].append((md_file, content, frontmatter))

        selected_articles: List[Tuple[Path, str, Dict[str, Any]]] = []
        for identity in sorted(grouped_articles, key=_stable_text_key):
            candidates = grouped_articles[identity]
            exclusions = [
                (candidate, self._candidate_exclusion_reason(candidate))
                for candidate in candidates
            ]
            clean_candidates = [
                candidate
                for candidate, exclusion_reason in exclusions
                if exclusion_reason is None
            ]
            archived_files = sum(
                exclusion_reason == "archived"
                for _, exclusion_reason in exclusions
            )
            synthetic_files = sum(
                exclusion_reason == "synthetic"
                for _, exclusion_reason in exclusions
            )
            incomplete_files = sum(
                exclusion_reason == "incomplete"
                for _, exclusion_reason in exclusions
            )
            self.archived_article_files_skipped += archived_files
            self.incomplete_article_files_skipped += incomplete_files
            self.synthetic_article_files_skipped += synthetic_files
            if clean_candidates:
                selected_articles.append(
                    min(clean_candidates, key=self._article_candidate_sort_key)
                )
            else:
                if archived_files:
                    self.archived_article_groups_skipped += 1
                if incomplete_files:
                    self.incomplete_article_groups_skipped += 1
                if synthetic_files:
                    self.synthetic_article_groups_skipped += 1
            self.canonical_duplicate_files_skipped += max(0, len(candidates) - 1)

        selected_articles.sort(key=lambda item: _stable_text_key(item[0].as_posix()))
        for md_file, content, frontmatter in selected_articles:
            self._parse_article_tags(md_file, content=content, frontmatter=frontmatter)
            # Interpreted briefs are excluded alongside source briefs: mining an
            # editorial reading would promote one page's inference into the
            # site-wide tech graph, where it would read as an established fact.
            if (
                self.enable_content_mining
                and str(frontmatter.get("content_mode") or "").casefold()
                not in {"source_brief", "interpreted_brief"}
            ):
                self._mine_article_concepts(
                    md_file,
                    content=content,
                    frontmatter=frontmatter,
                )

        print(f"Extracted {len(self.tags)} unique tags from {len(self.article_tags)} articles")
        if self.enable_content_mining:
            print(f"Mined {len(self.concepts)} unique concepts from {len(self.article_concepts)} articles")

    def _canonical_article_identity(
        self,
        md_file: Path,
        frontmatter: Dict[str, Any],
    ) -> str:
        raw_url = next(
            (
                frontmatter.get(key)
                for key in ("external_url", "externalUrl", "external-url")
                if frontmatter.get(key)
            ),
            None,
        )
        if raw_url:
            try:
                return f"url:{canonicalize_url(str(raw_url))}"
            except ValueError:
                logger.warning("Ignoring invalid external URL in %s", md_file)
        return f"path:{self._article_key(md_file)}"

    def _article_candidate_sort_key(
        self,
        candidate: Tuple[Path, str, Dict[str, Any]],
    ) -> Tuple[Any, ...]:
        """Rank duplicate article candidates without letting synthetic length win."""
        md_file, content, frontmatter = candidate
        body = re.sub(
            r"\A(?:\ufeff)?---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)",
            "",
            content,
            count=1,
            flags=re.DOTALL,
        )
        visible = re.sub(r"[`*_>#\[\](){}|~-]+", " ", body)
        visible_length = len(re.sub(r"\s+", "", visible))
        empty_headings = len(
            re.findall(r"(?m)^#{1,6}\s+[^\n]+\n\s*(?=^#{1,6}\s+|\Z)", body)
        )
        has_source = bool(
            frontmatter.get("external_url")
            or frontmatter.get("externalUrl")
            or frontmatter.get("external-url")
        )
        return (
            visible_length < 300,
            not has_source,
            empty_headings,
            -min(visible_length, 12_000),
            *_stable_text_key(self._article_key(md_file)),
        )

    def _candidate_exclusion_reason(
        self,
        candidate: Tuple[Path, str, Dict[str, Any]],
    ) -> str | None:
        _, content, frontmatter = candidate
        if frontmatter.get("archived") is True:
            return "archived"
        body = re.sub(
            r"\A(?:\ufeff)?---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)",
            "",
            content,
            count=1,
            flags=re.DOTALL,
        )
        if synthetic_body_reasons(body):
            return "synthetic"
        if body_completeness_reasons(body) or analyze_post(content).fatal_reasons:
            return "incomplete"
        return None

    def _candidate_is_synthetic(
        self,
        candidate: Tuple[Path, str, Dict[str, Any]],
    ) -> bool:
        """Backward-compatible predicate for callers that only need exclusion."""
        return self._candidate_exclusion_reason(candidate) is not None

    def _parse_article_tags(
        self,
        md_file: Path,
        *,
        content: Optional[str] = None,
        frontmatter: Optional[Dict[str, Any]] = None,
    ) -> None:
        """解析单篇文章的标签"""
        if content is None:
            content = md_file.read_text(encoding="utf-8")
        if frontmatter is None:
            frontmatter = self._extract_frontmatter(content)
        raw_tags = frontmatter.get("tags")
        if isinstance(raw_tags, str):
            raw_tags = raw_tags.split(",")
        if not isinstance(raw_tags, (list, tuple, set)):
            return

        tags = sorted(set(normalize_tags(raw_tags, limit=8)), key=_stable_text_key)
        if not tags:
            return

        article_title = str(frontmatter.get("title") or self._extract_title(content))
        article_key = self._article_key(md_file)
        self.article_tags[article_key] = tags
        self.article_titles[article_key] = article_title

        article_date = _normalize_generated_at(frontmatter.get("date"))
        if article_date:
            self.source_dates.append(article_date)

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

    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Parse YAML frontmatter without treating the Markdown body as YAML."""
        match = re.match(
            r"\A(?:\ufeff)?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)",
            content,
            re.DOTALL,
        )
        if not match:
            return {}
        try:
            parsed = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            logger.warning("Failed to parse frontmatter: %s", exc)
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def _extract_title(self, content: str) -> str:
        """提取文章标题"""
        frontmatter = self._extract_frontmatter(content)
        if frontmatter.get("title"):
            return str(frontmatter["title"])
        match = re.search(r'^title:\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        return match.group(1) if match else "Untitled"

    def _extract_date(self, content: str) -> Optional[str]:
        """Extract and normalize an article date for deterministic graph metadata."""
        frontmatter = self._extract_frontmatter(content)
        if frontmatter.get("date"):
            return _normalize_generated_at(frontmatter["date"])
        match = re.search(r'^date:\s*([^\n]+)', content, re.MULTILINE)
        if not match:
            return None
        return _normalize_generated_at(match.group(1))

    def _mine_article_concepts(
        self,
        md_file: Path,
        *,
        content: Optional[str] = None,
        frontmatter: Optional[Dict[str, Any]] = None,
    ) -> None:
        """从文章内容中挖掘概念和关键词"""
        if content is None:
            content = md_file.read_text(encoding="utf-8")

        article_key = self._article_key(md_file)
        if frontmatter is None:
            frontmatter = self._extract_frontmatter(content)
        article_title = str(frontmatter.get("title") or self._extract_title(content))
        
        title_concepts = self._extract_concepts_from_text(article_title)
        body_concepts = self._extract_concepts_from_text(content)
        
        all_concepts = sorted(set(title_concepts + body_concepts), key=_stable_text_key)
        self.article_concepts[article_key] = all_concepts

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
            (r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', 0),
            (r'\b(?:AI|ML|LLM|GPT|API|SDK|REST|GraphQL|HTTP|HTTPS|TCP|UDP|DNS|URL|URI)\b', re.IGNORECASE),
            (r'\b(?:Python|Java|JavaScript|TypeScript|Go|Rust|C\+\+|Swift|Kotlin|PHP|Ruby)\b', re.IGNORECASE),
            (r'\b(?:React|Vue|Angular|Node\.js|Express|Django|Flask|Spring|Laravel)\b', re.IGNORECASE),
            (r'\b(?:Docker|Kubernetes|K8s|AWS|Azure|GCP|Terraform|Ansible|Jenkins)\b', re.IGNORECASE),
            (r'\b(?:TensorFlow|PyTorch|Keras|Scikit|Pandas|NumPy|Matplotlib)\b', re.IGNORECASE),
            (r'\b(?:PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch|Cassandra|InfluxDB)\b', re.IGNORECASE),
            (r'\b(?:Linux|Unix|Windows|macOS|Android|iOS)\b', re.IGNORECASE),
            (r'\b(?:Git|GitHub|GitLab|Bitbucket|SVN)\b', re.IGNORECASE),
            (r'\b(?:CI|CD|DevOps|Agile|Scrum|Kanban|TDD|BDD)\b', re.IGNORECASE),
            (r'\b(?:Microservices|Serverless|Monolith|SOA|Event-driven)\b', re.IGNORECASE),
            (r'\b(?:OAuth|JWT|SSL|TLS|HTTPS|SSH|SFTP)\b', re.IGNORECASE),
            (r'\b(?:NoSQL|SQL|ORM|ODM)\b', re.IGNORECASE),
        ]
        
        for pattern, flags in tech_patterns:
            matches = re.findall(pattern, text, flags)
            keywords.extend(matches)
        
        return keywords

    def _update_concept_cooccurrence(self, concepts: List[str]) -> None:
        """更新概念共现关系"""
        unique_concepts = sorted(set(concepts), key=_stable_text_key)
        for i, concept1 in enumerate(unique_concepts):
            for concept2 in unique_concepts[i+1:]:
                pair = tuple(sorted([concept1, concept2]))
                self.concept_cooccurrence[pair] += 1
                self.concepts[concept1]["related_concepts"].add(concept2)
                self.concepts[concept2]["related_concepts"].add(concept1)

    def _update_cooccurrence(self, tags: List[str]) -> None:
        """更新标签共现关系"""
        unique_tags = sorted(set(tags), key=_stable_text_key)
        for i, tag1 in enumerate(unique_tags):
            for tag2 in unique_tags[i+1:]:
                pair = tuple(sorted([tag1, tag2]))
                self.tag_cooccurrence[pair] += 1
                self.tags[tag1]["related_tags"].add(tag2)
                self.tags[tag2]["related_tags"].add(tag1)

    def get_tag_nodes(self) -> List[Dict]:
        """获取标签节点列表"""
        nodes = []
        for tag_id, tag_data in sorted(self.tags.items(), key=lambda item: _stable_text_key(item[0])):
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
            })
        return nodes

    def get_tag_links(self, min_cooccurrence: int = 1) -> List[Dict]:
        """获取标签间关联（基于共现）"""
        links = []
        for (tag1, tag2), count in sorted(self.tag_cooccurrence.items()):
            if count >= min_cooccurrence:
                links.append({
                    "source": tag1,
                    "target": tag2,
                    "source_layer": "tag",
                    "target_layer": "tag",
                    "weight": count,
                    "strength": min(count / 2, 1.0),
                    "type": "cooccurrence",
                })
        return links

    def get_concept_nodes(self) -> List[Dict]:
        """获取概念节点列表"""
        nodes = []
        for concept_id, concept_data in sorted(self.concepts.items(), key=lambda item: _stable_text_key(item[0])):
            nodes.append({
                "id": concept_id,
                "name": concept_data["name"],
                "layer": "concept",
                "layer_name": "概念层",
                "level": 7,
                "color": "#67e8f9",
                "category": concept_data["category"],
                "description": concept_data["description"],
                "article_count": concept_data["article_count"],
                "related_count": len(concept_data["related_concepts"]),
            })
        return nodes

    def get_concept_links(self, min_cooccurrence: int = 1) -> List[Dict]:
        """获取概念间关联（基于共现）"""
        links = []
        for (concept1, concept2), count in sorted(self.concept_cooccurrence.items()):
            if count >= min_cooccurrence:
                links.append({
                    "source": concept1,
                    "target": concept2,
                    "source_layer": "concept",
                    "target_layer": "concept",
                    "weight": count,
                    "strength": min(count / 2, 1.0),
                    "type": "cooccurrence",
                })
        return links

    def build_tag_to_tech_links(self, tech_nodes: List[Dict]) -> List[Dict]:
        """建立标签与技术栈节点的关联（基于名称匹配）"""
        links = []
        tech_names = {node["id"]: node for node in tech_nodes}

        for tag_name in sorted(self.tags, key=_stable_text_key):
            for tech_id, tech_node in sorted(tech_names.items(), key=lambda item: _stable_text_key(item[0])):
                if self._is_semantically_related(tag_name, tech_id, tech_node):
                    links.append({
                        "source": tag_name,
                        "target": tech_id,
                        "source_layer": "tag",
                        "target_layer": tech_node.get("layer"),
                        "weight": 0.6,
                        "strength": 0.6,
                        "type": "semantic",
                    })
        return links

    def _is_semantically_related(self, tag: str, tech_id: str, tech_node: Dict) -> bool:
        """判断标签与技术节点是否语义相关"""
        def compact(value: Any) -> str:
            return "".join(
                character
                for character in str(value or "").casefold()
                if character.isalnum() or character in {"+", "#"}
            )

        tag_text = str(tag or "").strip().casefold()
        if not tag_text:
            return False

        tag_compact = compact(tag_text)
        exact_aliases = {
            compact(tech_id),
            compact(tech_node.get("name")),
        }
        if tag_compact and tag_compact in exact_aliases:
            return True

        tag_tokens = set(re.findall(r"[a-z0-9]+(?:\+\+|#)?", tag_text))
        tech_tokens = set(
            re.findall(r"[a-z0-9]+(?:\+\+|#)?", str(tech_id or "").casefold())
        )
        for alias in tech_tokens:
            if len(alias) >= 3 and alias in tag_tokens:
                return True
            if len(alias) <= 2 and tag_text.startswith(alias):
                suffix = tag_text[len(alias):len(alias) + 1]
                if not suffix or not suffix.isascii() or not suffix.isalnum():
                    return True
        return False

    def get_stats(self) -> Dict:
        """获取统计数据"""
        most_used_tags = sorted(
            self.tags.items(),
            key=lambda item: (-item[1]["article_count"], *_stable_text_key(item[0])),
        )[:5]

        most_used_concepts = sorted(
            self.concepts.items(),
            key=lambda item: (-item[1]["article_count"], *_stable_text_key(item[0])),
        )[:5]
        
        return {
            "total_tags": len(self.tags),
            "total_concepts": len(self.concepts),
            "total_articles": len(self.article_tags),
            "canonical_duplicate_files_skipped": self.canonical_duplicate_files_skipped,
            "archived_article_groups_skipped": self.archived_article_groups_skipped,
            "archived_article_files_skipped": self.archived_article_files_skipped,
            "incomplete_article_groups_skipped": self.incomplete_article_groups_skipped,
            "incomplete_article_files_skipped": self.incomplete_article_files_skipped,
            "synthetic_article_groups_skipped": self.synthetic_article_groups_skipped,
            "synthetic_article_files_skipped": self.synthetic_article_files_skipped,
            "total_tag_links": len(self.tag_cooccurrence),
            "total_concept_links": len(self.concept_cooccurrence),
            "avg_tags_per_article": sum(len(tags) for tags in self.article_tags.values()) / len(self.article_tags) if self.article_tags else 0,
            "avg_concepts_per_article": sum(len(concepts) for concepts in self.article_concepts.values()) / len(self.article_concepts) if self.article_concepts else 0,
            "most_used_tags": [
                (tag_name, {
                    **{key: value for key, value in tag_data.items() if key != "related_tags"},
                    "related_count": len(tag_data["related_tags"]),
                })
                for tag_name, tag_data in most_used_tags
            ],
            "most_used_concepts": [
                (concept_name, {
                    **{key: value for key, value in concept_data.items() if key != "related_concepts"},
                    "related_count": len(concept_data["related_concepts"]),
                })
                for concept_name, concept_data in most_used_concepts
            ],
        }


def _without_related_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_related_fields(item)
            for key, item in value.items()
            if key not in {"related_tags", "related_concepts"}
        }
    if isinstance(value, (list, tuple)):
        return [_without_related_fields(item) for item in value]
    if isinstance(value, set):
        return [_without_related_fields(item) for item in sorted(value, key=_stable_text_key)]
    return value


def convert_v1_graph_to_v2(
    payload: Dict[str, Any],
    *,
    generated_at: Optional[str] = None,
) -> Dict[str, Any]:
    """Convert legacy/raw graph data into the canonical deterministic v2 contract."""
    source = payload or {}
    source_is_v2 = source.get("version") == GRAPH_VERSION
    raw_nodes = list(source.get("nodes") or [])
    legacy_to_ids: Dict[str, List[str]] = defaultdict(list)
    nodes_by_id: Dict[str, Dict[str, Any]] = {}

    for raw_node in raw_nodes:
        if not isinstance(raw_node, dict) or not raw_node.get("id"):
            continue
        clean_node = _without_related_fields(dict(raw_node))
        original_id = str(raw_node["id"])
        layer = str(raw_node.get("layer") or "unknown")
        legacy_id = str(
            raw_node.get("legacy_id")
            or (_legacy_node_id(original_id) if source_is_v2 else original_id)
        )
        node_id = _namespace_node_id(
            original_id,
            layer,
            already_namespaced=source_is_v2,
        )

        clean_node["id"] = node_id
        clean_node["legacy_id"] = legacy_id
        clean_node["layer"] = layer
        clean_node["article_count"] = int(clean_node.get("article_count", 0) or 0)
        legacy_community = clean_node.pop("community", None)
        if legacy_community and not clean_node.get("community_id"):
            clean_node["community_id"] = str(legacy_community)
        clean_node.setdefault("community_id", None)
        clean_node.pop("degree", None)
        clean_node.pop("weighted_degree", None)
        clean_node.pop("rank", None)
        existing_node = nodes_by_id.get(node_id)
        if existing_node is None:
            nodes_by_id[node_id] = clean_node
        else:
            def merge_preference(node: Dict[str, Any]) -> Tuple[int, int, str]:
                populated_fields = sum(
                    value not in (None, "", [], {}) for value in node.values()
                )
                stable_record = json.dumps(
                    node,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                return (
                    -int(node.get("article_count", 0) or 0),
                    -populated_fields,
                    stable_record,
                )

            nodes_by_id[node_id] = min(
                (existing_node, clean_node),
                key=merge_preference,
            )

        aliases = {original_id, legacy_id}
        if source_is_v2:
            aliases.add(node_id)
        for alias in aliases:
            if node_id not in legacy_to_ids[alias]:
                legacy_to_ids[alias].append(node_id)

    for aliases in legacy_to_ids.values():
        aliases.sort(key=_stable_text_key)

    def endpoint_candidates(endpoint: Any) -> List[str]:
        raw = str(endpoint or "")
        if source_is_v2 and raw in nodes_by_id:
            return [raw]
        legacy_candidates = list(legacy_to_ids.get(raw) or [])
        if legacy_candidates:
            return legacy_candidates
        if raw in nodes_by_id:
            return [raw]
        return []

    def resolve_endpoint(
        endpoint: Any,
        *,
        layer_hint: Any = None,
        preferred_namespace: Optional[str] = None,
    ) -> Optional[str]:
        raw = str(endpoint or "")
        if source_is_v2 and raw in nodes_by_id:
            return raw
        candidates = endpoint_candidates(raw)
        if not candidates:
            return None

        if layer_hint:
            hinted = [
                node_id
                for node_id in candidates
                if nodes_by_id[node_id].get("layer") == str(layer_hint)
            ]
            if hinted:
                candidates = hinted
        if preferred_namespace:
            preferred = [
                node_id for node_id in candidates if node_id.startswith(f"{preferred_namespace}:")
            ]
            if preferred:
                candidates = preferred
        return sorted(candidates, key=_stable_text_key)[0]

    aggregated_links: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for raw_link in list(source.get("links") or []):
        if not isinstance(raw_link, dict):
            continue
        edge_type = str(raw_link.get("type") or "relation")
        source_namespace = "tag" if edge_type == "semantic" else None
        target_namespace = "tech" if edge_type == "semantic" else None
        if edge_type == "relation":
            source_namespace = target_namespace = "tech"
        elif (
            edge_type == "cooccurrence"
            and not raw_link.get("source_layer")
            and not raw_link.get("target_layer")
        ):
            source_candidates = endpoint_candidates(raw_link.get("source"))
            target_candidates = endpoint_candidates(raw_link.get("target"))
            shared_namespaces = {
                node_id.split(":", 1)[0] for node_id in source_candidates
            }.intersection(
                node_id.split(":", 1)[0] for node_id in target_candidates
            )
            if len(shared_namespaces) == 1:
                source_namespace = target_namespace = next(iter(shared_namespaces))
            elif len(shared_namespaces) > 1:
                raise ValueError(
                    "ambiguous cooccurrence endpoints require source_layer/target_layer"
                )

        source_id = resolve_endpoint(
            raw_link.get("source"),
            layer_hint=raw_link.get("source_layer"),
            preferred_namespace=source_namespace,
        )
        target_id = resolve_endpoint(
            raw_link.get("target"),
            layer_hint=raw_link.get("target_layer"),
            preferred_namespace=target_namespace,
        )
        if not source_id or not target_id or source_id == target_id:
            continue

        if edge_type == "cooccurrence" and source_id.split(":", 1)[0] == target_id.split(":", 1)[0]:
            source_id, target_id = sorted((source_id, target_id), key=_stable_text_key)

        raw_weight = raw_link.get("weight")
        if raw_weight is None:
            raw_weight = raw_link.get("strength", 1.0)
        weight = _numeric_weight(raw_weight)
        if weight <= 0:
            continue
        strength = _numeric_weight(raw_link.get("strength"), min(weight, 1.0))
        key = (source_id, target_id, edge_type)

        if key not in aggregated_links:
            aggregated_links[key] = {
                "id": f"edge:{edge_type}:{source_id}->{target_id}",
                "source": source_id,
                "target": target_id,
                "type": edge_type,
                "weight": weight,
                "strength": strength,
            }
        else:
            aggregated_links[key]["weight"] += weight
            aggregated_links[key]["strength"] = max(
                aggregated_links[key]["strength"], strength
            )

    links: List[Dict[str, Any]] = []
    for link in aggregated_links.values():
        link["weight"] = _compact_number(link["weight"])
        link["strength"] = _compact_number(link["strength"])
        links.append(link)
    links.sort(key=_edge_sort_key)

    derived_tech_articles: Dict[str, int] = defaultdict(int)
    for link in links:
        if link.get("type") != "semantic":
            continue
        source_id = str(link["source"])
        target_id = str(link["target"])
        if source_id.startswith("tag:") and target_id.startswith("tech:"):
            derived_tech_articles[target_id] += int(
                nodes_by_id[source_id].get("article_count", 0) or 0
            )
        elif target_id.startswith("tag:") and source_id.startswith("tech:"):
            derived_tech_articles[source_id] += int(
                nodes_by_id[target_id].get("article_count", 0) or 0
            )
    for node_id, article_count in derived_tech_articles.items():
        if int(nodes_by_id[node_id].get("article_count", 0) or 0) <= 0:
            nodes_by_id[node_id]["article_count"] = article_count

    degree: Dict[str, int] = defaultdict(int)
    weighted_degree: Dict[str, float] = defaultdict(float)
    for link in links:
        source_id = str(link["source"])
        target_id = str(link["target"])
        weight = _numeric_weight(link.get("weight"))
        degree[source_id] += 1
        degree[target_id] += 1
        weighted_degree[source_id] += weight
        weighted_degree[target_id] += weight

    nodes = sorted(nodes_by_id.values(), key=lambda node: _stable_text_key(node["id"]))
    for node in nodes:
        node_id = str(node["id"])
        node["degree"] = degree[node_id]
        node["weighted_degree"] = _compact_number(weighted_degree[node_id])

    ranked_nodes = sorted(
        nodes,
        key=lambda node: (
            -float(node.get("weighted_degree", 0) or 0),
            -int(node.get("article_count", 0) or 0),
            -int(node.get("degree", 0) or 0),
            *_stable_text_key(node.get("id")),
        ),
    )
    for rank, node in enumerate(ranked_nodes, start=1):
        node["rank"] = rank

    source_stats = source.get("stats") if isinstance(source.get("stats"), dict) else {}
    tag_stats = source_stats.get("tag_stats") if isinstance(source_stats, dict) else None
    canonical_tag_stats = _without_related_fields(tag_stats) if tag_stats is not None else None
    normalized_generated_at = (
        _normalize_generated_at(generated_at)
        or _normalize_generated_at(source.get("generated_at"))
        or DEFAULT_GENERATED_AT
    )

    return {
        "version": GRAPH_VERSION,
        "generated_at": normalized_generated_at,
        "nodes": nodes,
        "links": links,
        "layers": dict(sorted((source.get("layers") or {}).items())),
        "stats": _graph_stats(nodes, links, tag_stats=canonical_tag_stats),
    }


def build_weighted_tag_communities(
    nodes: List[Dict[str, Any]],
    links: List[Dict[str, Any]],
    *,
    max_communities: int = DEFAULT_COMMUNITY_LIMIT,
    generated_at: Optional[str] = None,
    max_iterations: int = 50,
    article_memberships: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build deterministic weighted label-propagation communities for tag nodes."""
    tag_nodes = sorted(
        [node for node in nodes if str(node.get("id") or "").startswith("tag:")],
        key=lambda node: _stable_text_key(node.get("id")),
    )
    node_lookup = {str(node["id"]): node for node in tag_nodes}
    adjacency: Dict[str, Dict[str, float]] = {
        node_id: defaultdict(float) for node_id in node_lookup
    }

    for link in sorted(links, key=_edge_sort_key):
        if str(link.get("type") or "") != "cooccurrence":
            continue
        source_id = str(link.get("source") or "")
        target_id = str(link.get("target") or "")
        if source_id not in adjacency or target_id not in adjacency or source_id == target_id:
            continue
        raw_weight = _numeric_weight(link.get("weight", link.get("strength", 1.0)))
        if raw_weight <= 0:
            continue
        source_frequency = max(
            raw_weight,
            float(node_lookup[source_id].get("article_count", 0) or 0),
            1.0,
        )
        target_frequency = max(
            raw_weight,
            float(node_lookup[target_id].get("article_count", 0) or 0),
            1.0,
        )
        association_weight = raw_weight / (source_frequency * target_frequency) ** 0.5
        adjacency[source_id][target_id] += association_weight
        adjacency[target_id][source_id] += association_weight

    ordered_ids = sorted(node_lookup, key=_stable_text_key)
    labels = {node_id: node_id for node_id in ordered_ids}
    iterations = 0
    for iteration in range(max(0, int(max_iterations))):
        changes = 0
        for node_id in ordered_ids:
            label_weights: Dict[str, float] = defaultdict(float)
            for neighbor_id, weight in sorted(
                adjacency[node_id].items(), key=lambda item: _stable_text_key(item[0])
            ):
                label_weights[labels[neighbor_id]] += weight
            if not label_weights:
                continue
            selected_label = min(
                label_weights,
                key=lambda label: (-label_weights[label], *_stable_text_key(label)),
            )
            if selected_label != labels[node_id]:
                labels[node_id] = selected_label
                changes += 1
        iterations = iteration + 1
        if changes == 0:
            break

    grouped: Dict[str, List[str]] = defaultdict(list)
    for node_id in ordered_ids:
        grouped[labels[node_id]].append(node_id)

    normalized_memberships: Optional[Dict[str, set[str]]] = None
    if article_memberships is not None:
        normalized_memberships = {
            str(node_id): {str(article_id) for article_id in (article_ids or [])}
            for node_id, article_ids in article_memberships.items()
        }

    raw_communities: List[Dict[str, Any]] = []
    for label, member_ids in sorted(grouped.items(), key=lambda item: _stable_text_key(item[0])):
        member_ids = sorted(member_ids, key=_stable_text_key)
        leader_id = min(
            member_ids,
            key=lambda node_id: (
                -int(node_lookup[node_id].get("article_count", 0) or 0),
                -float(node_lookup[node_id].get("weighted_degree", 0) or 0),
                *_stable_text_key(node_lookup[node_id].get("name") or node_id),
                *_stable_text_key(node_id),
            ),
        )
        community_weight = sum(
            float(
                node_lookup[node_id].get("weighted_degree")
                if node_lookup[node_id].get("weighted_degree") is not None
                else sum(adjacency[node_id].values())
            )
            for node_id in member_ids
        )
        tag_occurrences = sum(
            int(node_lookup[node_id].get("article_count", 0) or 0)
            for node_id in member_ids
        )
        community = {
            "id": f"community:{label}",
            "name": str(node_lookup[leader_id].get("name") or _legacy_node_id(leader_id)),
            "leader_id": leader_id,
            "node_count": len(member_ids),
            "tag_occurrences": tag_occurrences,
            "weighted_degree": _compact_number(community_weight),
            "node_ids": member_ids,
        }
        if normalized_memberships is not None:
            community["article_count"] = len(
                {
                    article_id
                    for node_id in member_ids
                    for article_id in normalized_memberships.get(node_id, set())
                }
            )
        raw_communities.append(community)

    raw_communities.sort(
        key=lambda community: (
            -int(community["node_count"]),
            -int(community.get("article_count", community["tag_occurrences"])),
            -float(community["weighted_degree"]),
            *_stable_text_key(community["id"]),
        )
    )

    limit = max(0, int(max_communities))
    primary = raw_communities[:limit]
    overflow = raw_communities[limit:]
    communities: List[Dict[str, Any]] = []
    assignments: Dict[str, str] = {}

    for rank, community in enumerate(primary, start=1):
        item = dict(community)
        item["rank"] = rank
        communities.append(item)
        for node_id in item["node_ids"]:
            assignments[node_id] = str(item["id"])

    if overflow:
        overflow_ids = sorted(
            [node_id for community in overflow for node_id in community["node_ids"]],
            key=_stable_text_key,
        )
        other = {
            "id": "community:other",
            "name": "其他",
            "leader_id": None,
            "node_count": len(overflow_ids),
            "tag_occurrences": sum(int(item["tag_occurrences"]) for item in overflow),
            "weighted_degree": _compact_number(
                sum(float(item["weighted_degree"]) for item in overflow)
            ),
            "node_ids": overflow_ids,
            "rank": len(communities) + 1,
        }
        if normalized_memberships is not None:
            other["article_count"] = len(
                {
                    article_id
                    for node_id in overflow_ids
                    for article_id in normalized_memberships.get(node_id, set())
                }
            )
        communities.append(other)
        for node_id in overflow_ids:
            assignments[node_id] = "community:other"

    ordered_assignments = {
        node_id: assignments[node_id] for node_id in sorted(assignments, key=_stable_text_key)
    }
    community_link_weights: Dict[Tuple[str, str], float] = defaultdict(float)
    for link in sorted(links, key=_edge_sort_key):
        if str(link.get("type") or "") != "cooccurrence":
            continue
        source_community = ordered_assignments.get(str(link.get("source") or ""))
        target_community = ordered_assignments.get(str(link.get("target") or ""))
        if not source_community or not target_community or source_community == target_community:
            continue
        community_pair = tuple(
            sorted((source_community, target_community), key=_stable_text_key)
        )
        link_weight = _numeric_weight(link.get("weight"))
        if link_weight <= 0:
            continue
        community_link_weights[community_pair] += link_weight

    community_links: List[Dict[str, Any]] = []
    for (source_id, target_id), weight in sorted(community_link_weights.items()):
        compact_weight = _compact_number(weight)
        community_links.append(
            {
                "id": f"edge:community:{source_id}->{target_id}",
                "source": source_id,
                "target": target_id,
                "type": "community",
                "weight": compact_weight,
                "strength": _compact_number(min(weight, 1.0)),
            }
        )

    normalized_generated_at = _normalize_generated_at(generated_at) or DEFAULT_GENERATED_AT
    return {
        "version": GRAPH_VERSION,
        "generated_at": normalized_generated_at,
        "algorithm": "deterministic-weighted-label-propagation",
        "limit": limit,
        "iterations": iterations,
        "communities": communities,
        "assignments": ordered_assignments,
        "links": community_links,
        "stats": {
            "total_communities": len(communities),
            "detected_communities": len(raw_communities),
            "emitted_communities": len(communities),
            "assigned_nodes": len(ordered_assignments),
            "total_links": len(community_links),
            "weighting": "cosine-association",
        },
    }


def build_search_index(
    nodes: List[Dict[str, Any]],
    *,
    generated_at: Optional[str] = None,
) -> Dict[str, Any]:
    """Build deterministic searchable GraphNodeV2 metadata for every node."""
    items: List[Dict[str, Any]] = []
    for node in sorted(
        nodes,
        key=lambda item: (
            int(item.get("rank", 2**31 - 1) or 2**31 - 1),
            *_stable_text_key(item.get("id")),
        ),
    ):
        node_id = str(node.get("id") or "")
        community_id = node.get("community_id")
        items.append(
            {
                "id": node_id,
                "legacy_id": str(node.get("legacy_id") or _legacy_node_id(node_id)),
                "name": str(node.get("name") or ""),
                "layer": str(node.get("layer") or ""),
                "category": str(node.get("category") or ""),
                "description": str(node.get("description") or ""),
                "article_count": int(_numeric_weight(node.get("article_count"), 0)),
                "degree": int(_numeric_weight(node.get("degree"), 0)),
                "weighted_degree": _compact_number(
                    _numeric_weight(node.get("weighted_degree"), 0)
                ),
                "community_id": (
                    str(community_id) if community_id not in {None, ""} else None
                ),
                "rank": int(node.get("rank", 0) or 0),
            }
        )

    return {
        "version": GRAPH_VERSION,
        "generated_at": _normalize_generated_at(generated_at) or DEFAULT_GENERATED_AT,
        "fields": list(GRAPH_NODE_V2_FIELDS),
        "items": items,
        "stats": {"total_items": len(items)},
    }


def _fnv1a32(value: Any) -> int:
    """Return the unsigned FNV-1a 32-bit hash of the value's UTF-8 bytes."""
    result = 0x811C9DC5
    for byte in str(value or "").encode("utf-8"):
        result ^= byte
        result = (result * 0x01000193) & 0xFFFFFFFF
    return result


def _focus_shard_bucket(
    node_id: Any,
    bucket_count: int = FOCUS_SHARD_COUNT,
) -> int:
    count = int(bucket_count)
    if count <= 0:
        raise ValueError("focus shard bucket count must be positive")
    return _fnv1a32(node_id) % count


def _build_focus_shard_payloads(
    nodes: List[Dict[str, Any]],
    links: List[Dict[str, Any]],
    *,
    bucket_count: int = FOCUS_SHARD_COUNT,
    neighbor_limit: int = FOCUS_NEIGHBOR_LIMIT,
) -> List[Tuple[str, Dict[str, Any]]]:
    """Build compact, deterministic direct-neighbor shards for lazy focus views."""
    count = int(bucket_count)
    if count <= 0:
        raise ValueError("focus shard bucket count must be positive")
    limit = max(0, int(neighbor_limit))
    node_ids = {
        str(node.get("id") or "")
        for node in nodes
        if str(node.get("id") or "")
    }
    neighbors_by_node: Dict[
        str,
        Dict[str, Tuple[Tuple[Any, ...], List[Any]]],
    ] = {node_id: {} for node_id in node_ids}

    for link in sorted(links, key=_edge_sort_key):
        source_id = str(link.get("source") or "")
        target_id = str(link.get("target") or "")
        if (
            not source_id
            or not target_id
            or source_id == target_id
            or source_id not in node_ids
            or target_id not in node_ids
        ):
            continue

        weight = _compact_number(_numeric_weight(link.get("weight", link.get("strength", 1))))
        link_type = str(link.get("type") or "relation")
        link_id = str(link.get("id") or "")
        for node_id, neighbor_id, direction in (
            (source_id, target_id, 1),
            (target_id, source_id, -1),
        ):
            choice_key = (
                -float(weight),
                *_stable_text_key(link_type),
                *_stable_text_key(link_id),
                direction,
            )
            existing = neighbors_by_node[node_id].get(neighbor_id)
            if existing is None or choice_key < existing[0]:
                neighbors_by_node[node_id][neighbor_id] = (
                    choice_key,
                    [neighbor_id, weight, link_type, direction],
                )

    payloads: List[Dict[str, Any]] = [
        {
            "version": GRAPH_VERSION,
            "bucket": bucket,
            "algorithm": FOCUS_SHARD_ALGORITHM,
            "entries": {},
        }
        for bucket in range(count)
    ]
    for node_id in sorted(node_ids, key=_stable_text_key):
        candidates = [
            entry
            for _neighbor_id, (_choice_key, entry) in neighbors_by_node[node_id].items()
        ]
        candidates.sort(
            key=lambda entry: (
                -float(entry[1]),
                *_stable_text_key(entry[0]),
                *_stable_text_key(entry[2]),
                int(entry[3]),
            )
        )
        bucket = _focus_shard_bucket(node_id, count)
        payloads[bucket]["entries"][node_id] = candidates[:limit]

    files: List[Tuple[str, Dict[str, Any]]] = []
    for bucket, payload in enumerate(payloads):
        payload_hash = hashlib.sha256(
            _stable_compact_json_text(payload).encode("utf-8")
        ).hexdigest()[:12]
        files.append(
            (
                f"focus-shards/{bucket:03d}-{payload_hash}.json",
                payload,
            )
        )
    return files


def _build_runtime_community_payloads(
    community: Dict[str, Any],
    nodes: List[Dict[str, Any]],
    links: List[Dict[str, Any]],
    *,
    hotspot_limit: int = COMMUNITY_HOTSPOT_LIMIT,
    hotspot_link_limit: int = COMMUNITY_HOTSPOT_LINK_LIMIT,
) -> Tuple[Dict[str, Any], List[Tuple[str, Dict[str, Any]]]]:
    """Split community metadata into one tiny, lazily loaded file per community."""
    node_lookup = {
        str(node.get("id") or ""): node
        for node in nodes
        if str(node.get("id") or "").startswith("tag:")
    }
    limit = max(0, int(hotspot_limit))
    link_limit = max(0, int(hotspot_link_limit))
    summary_communities: List[Dict[str, Any]] = []
    hotspot_files: List[Tuple[str, Dict[str, Any]]] = []

    for raw_community in community.get("communities") or []:
        community_id = str(raw_community.get("id") or "")
        member_ids = [
            str(node_id)
            for node_id in (raw_community.get("node_ids") or [])
            if str(node_id) in node_lookup
        ]
        candidates = sorted(
            (node_lookup[node_id] for node_id in member_ids),
            key=lambda node: (
                int(node.get("rank", 2**31 - 1) or 2**31 - 1),
                -float(node.get("weighted_degree", 0) or 0),
                -int(node.get("article_count", 0) or 0),
                -int(node.get("degree", 0) or 0),
                *_stable_text_key(node.get("id")),
            ),
        )
        selected_nodes = [dict(node) for node in candidates[:limit]]
        summary = {
            key: value
            for key, value in raw_community.items()
            if key != "node_ids"
        }
        summary["hotspot_count"] = len(selected_nodes)

        if community_id == "community:other":
            summary["hotspot_count"] = 0
            summary_communities.append(summary)
            continue
        selected_ids = {str(node.get("id") or "") for node in selected_nodes}
        selected_links = sorted(
            (
                dict(link)
                for link in links
                if str(link.get("type") or "") == "cooccurrence"
                and str(link.get("source") or "") in selected_ids
                and str(link.get("target") or "") in selected_ids
            ),
            key=lambda link: (
                -_numeric_weight(link.get("weight", link.get("strength", 1))),
                *_edge_sort_key(link),
            ),
        )[:link_limit]
        payload = {
            "version": GRAPH_VERSION,
            "generated_at": str(
                community.get("generated_at") or DEFAULT_GENERATED_AT
            ),
            "community_id": community_id,
            "hotspot_limit": limit,
            "link_limit": link_limit,
            "nodes": selected_nodes,
            "links": selected_links,
            "stats": {
                "total_nodes": len(selected_nodes),
                "total_links": len(selected_links),
            },
        }
        rank = int(raw_community.get("rank", len(hotspot_files) + 1) or 0)
        payload_hash = hashlib.sha256(
            _stable_json_text(payload).encode("utf-8")
        ).hexdigest()[:12]
        relative_path = f"community-hotspots/{rank:02d}-{payload_hash}.json"
        summary["hotspot_file"] = relative_path
        summary_communities.append(summary)
        hotspot_files.append(
            (
                relative_path,
                payload,
            )
        )

    summary_payload = {
        key: value
        for key, value in community.items()
        if key not in {"assignments", "communities"}
    }
    summary_payload["communities"] = summary_communities

    return summary_payload, hotspot_files


def _stable_json_text(payload: Dict[str, Any]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
        allow_nan=False,
    ) + "\n"


def _stable_compact_json_text(payload: Dict[str, Any]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ) + "\n"


def _write_stable_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_stable_json_text(payload), encoding="utf-8")


def _write_stable_compact_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_stable_compact_json_text(payload), encoding="utf-8")


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
    _write_stable_json(output, data["graph"])

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
                    node_id = node.get("legacy_id") or _legacy_node_id(node.get("id"))
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
            for article_key, tags in (builder.article_tags or {}).items():
                title = builder.article_titles.get(article_key, article_key)
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

    matched_tags_by_tech: Dict[str, set[str]] = defaultdict(set)
    for link in tag_to_tech_links:
        matched_tags_by_tech[str(link["target"])].add(str(link["source"]))
    for tech_node in tech_nodes:
        matching_tags = matched_tags_by_tech.get(str(tech_node["id"]), set())
        tech_node["article_count"] = sum(
            1
            for article_tags in builder.article_tags.values()
            if matching_tags.intersection(article_tags)
        )

    all_nodes = tech_nodes + tag_nodes + concept_nodes
    all_links = tech_links + tag_links + tag_to_tech_links + concept_links

    layers = {
        "language": {"name": "编程语言", "level": 1, "color": "#4db6ac"},
        "framework": {"name": "框架层", "level": 2, "color": "#26a69a"},
        "model": {"name": "模型层", "level": 3, "color": "#d97706"},
        "application": {"name": "应用层", "level": 4, "color": "#7aa6b8"},
        "scenario": {"name": "场景层", "level": 5, "color": "#cbd5e1"},
        "tag": {"name": "标签层", "level": 6, "color": "#f59e0b"},
        "concept": {"name": "概念层", "level": 7, "color": "#67e8f9"},
    }

    raw_graph = {
        "nodes": all_nodes,
        "links": all_links,
        "layers": layers,
        "stats": {
            "total_nodes": len(all_nodes),
            "total_links": len(all_links),
            "tag_stats": builder.get_stats(),
        },
    }

    graph = convert_v1_graph_to_v2(raw_graph, generated_at=builder.generated_at)
    tag_ids_by_legacy = {
        str(node.get("legacy_id") or _legacy_node_id(node["id"])): str(node["id"])
        for node in graph["nodes"]
        if node.get("layer") == "tag"
    }
    tag_article_memberships: Dict[str, List[str]] = defaultdict(list)
    for article_id, article_tags in builder.article_tags.items():
        for tag in article_tags:
            node_id = tag_ids_by_legacy.get(tag)
            if node_id:
                tag_article_memberships[node_id].append(article_id)
    stable_tag_article_memberships = {
        node_id: sorted(article_ids, key=_stable_text_key)
        for node_id, article_ids in sorted(tag_article_memberships.items())
    }
    community = build_weighted_tag_communities(
        graph["nodes"],
        graph["links"],
        max_communities=DEFAULT_COMMUNITY_LIMIT,
        generated_at=graph["generated_at"],
        article_memberships=stable_tag_article_memberships,
    )
    assignments = community["assignments"]
    for node in graph["nodes"]:
        if node["id"] in assignments:
            node["community_id"] = assignments[node["id"]]
    graph["stats"]["total_communities"] = len(community["communities"])

    tech_nodes_v2 = [node for node in graph["nodes"] if node.get("layer") in TECH_LAYERS]
    tag_nodes_v2 = [node for node in graph["nodes"] if node.get("layer") == "tag"]
    concept_nodes_v2 = [node for node in graph["nodes"] if node.get("layer") == "concept"]

    def both_in_namespace(link: Dict[str, Any], namespace: str) -> bool:
        prefix = f"{namespace}:"
        return str(link.get("source") or "").startswith(prefix) and str(
            link.get("target") or ""
        ).startswith(prefix)

    tech_links_v2 = [link for link in graph["links"] if both_in_namespace(link, "tech")]
    tag_links_v2 = [
        link
        for link in graph["links"]
        if both_in_namespace(link, "tag") and link.get("type") == "cooccurrence"
    ]
    tag_to_tech_links_v2 = [
        link for link in graph["links"] if link.get("type") == "semantic"
    ]
    concept_links_v2 = [
        link
        for link in graph["links"]
        if both_in_namespace(link, "concept") and link.get("type") == "cooccurrence"
    ]

    return {
        "version": GRAPH_VERSION,
        "generated_at": graph["generated_at"],
        "graph": graph,
        "parts": {
            "tech_nodes": tech_nodes_v2,
            "tech_links": tech_links_v2,
            "tag_nodes": tag_nodes_v2,
            "tag_links": tag_links_v2,
            "tag_to_tech_links": tag_to_tech_links_v2,
            "concept_nodes": concept_nodes_v2,
            "concept_links": concept_links_v2,
        },
        "layers": layers,
        "stats": graph["stats"],
        "community": community,
        "_tag_article_memberships": stable_tag_article_memberships,
    }


def export_tag_graph_split(
    output_dir: str = "blog/static/data/tag-graph",
    min_cooccurrence: int = 1,
    enable_content_mining: bool = True,
    hot_tag_limit: int = 250,
    hot_concept_limit: int = 150,
    content_dir: str = "blog/content/posts",
    community_limit: int = DEFAULT_COMMUNITY_LIMIT,
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
        community_limit=community_limit,
    )


def write_tag_graph_split_from_result(
    result: Dict[str, Any],
    output_dir: str = "blog/static/data/tag-graph",
    hot_tag_limit: int = 250,
    hot_concept_limit: int = 150,
    community_limit: int = DEFAULT_COMMUNITY_LIMIT,
) -> Path:
    source_graph = result.get("graph") or {}
    if source_graph.get("version") != GRAPH_VERSION:
        source_graph = convert_v1_graph_to_v2(
            source_graph,
            generated_at=result.get("generated_at"),
        )

    generated_at = (
        _normalize_generated_at(source_graph.get("generated_at")) or DEFAULT_GENERATED_AT
    )
    layers = dict(sorted((source_graph.get("layers") or result.get("layers") or {}).items()))
    nodes = sorted(
        [dict(node) for node in source_graph.get("nodes") or []],
        key=lambda node: _stable_text_key(node.get("id")),
    )
    links = sorted(
        [dict(link) for link in source_graph.get("links") or []],
        key=_edge_sort_key,
    )

    community = build_weighted_tag_communities(
        nodes,
        links,
        max_communities=community_limit,
        generated_at=generated_at,
        article_memberships=(
            result.get("_tag_article_memberships")
            if isinstance(result.get("_tag_article_memberships"), dict)
            else None
        ),
    )
    assignments = community["assignments"]
    for node in nodes:
        node_id = str(node.get("id") or "")
        if node_id in assignments:
            node["community_id"] = assignments[node_id]
        node.pop("community", None)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    previous_hotspot_files: set[str] = set()
    previous_focus_shard_files: set[str] = set()
    previous_community_path = out_dir / "community.json"
    if previous_community_path.exists():
        try:
            previous_community = json.loads(
                previous_community_path.read_text(encoding="utf-8")
            )
            for item in previous_community.get("communities") or []:
                parts = str(item.get("hotspot_file") or "").split("/")
                if (
                    len(parts) == 2
                    and parts[0] == "community-hotspots"
                    and re.fullmatch(r"\d{2}-[0-9a-f]{12}\.json", parts[1])
                ):
                    previous_hotspot_files.add(parts[1])
        except (AttributeError, OSError, TypeError, ValueError, json.JSONDecodeError):
            previous_hotspot_files = set()
    previous_index_path = out_dir / "index.json"
    if previous_index_path.exists():
        try:
            previous_index = json.loads(
                previous_index_path.read_text(encoding="utf-8")
            )
            for relative_path in (
                (previous_index.get("files") or {}).get("focusShards") or []
            ):
                parts = str(relative_path or "").split("/")
                if (
                    len(parts) == 2
                    and parts[0] == "focus-shards"
                    and re.fullmatch(r"\d{3}-[0-9a-f]{12}\.json", parts[1])
                ):
                    previous_focus_shard_files.add(parts[1])
        except (AttributeError, OSError, TypeError, ValueError, json.JSONDecodeError):
            previous_focus_shard_files = set()

    core_nodes = [node for node in nodes if node.get("layer") in TECH_LAYERS]
    tag_nodes = [node for node in nodes if node.get("layer") == "tag"]
    concept_nodes = [node for node in nodes if node.get("layer") == "concept"]
    core_ids = {node["id"] for node in core_nodes}
    tag_ids = {node["id"] for node in tag_nodes}
    concept_ids = {node["id"] for node in concept_nodes}

    core_links = [
        link
        for link in links
        if link.get("source") in core_ids and link.get("target") in core_ids
    ]
    tag_links = [
        link
        for link in links
        if link.get("source") in tag_ids and link.get("target") in tag_ids
    ]
    tag_to_tech_links = [
        link
        for link in links
        if link.get("type") == "semantic"
        and ({link.get("source"), link.get("target")} & tag_ids)
        and ({link.get("source"), link.get("target")} & core_ids)
    ]
    concept_links = [
        link
        for link in links
        if link.get("source") in concept_ids and link.get("target") in concept_ids
    ]

    tag_nodes_by_hotness = sorted(
        tag_nodes,
        key=lambda node: (
            -int(node.get("article_count", 0) or 0),
            -float(node.get("weighted_degree", 0) or 0),
            -int(node.get("degree", 0) or 0),
            *_stable_text_key(node.get("id")),
        ),
    )
    hot_tag_ids = {
        node["id"]
        for node in tag_nodes_by_hotness[: max(0, int(hot_tag_limit))]
        if node.get("id")
    }
    hot_tag_nodes = [n for n in tag_nodes if n.get("id") in hot_tag_ids]
    hot_tag_links = [l for l in tag_links if l.get("source") in hot_tag_ids and l.get("target") in hot_tag_ids]
    hot_tag_to_tech_links = [
        link
        for link in tag_to_tech_links
        if link.get("source") in hot_tag_ids or link.get("target") in hot_tag_ids
    ]

    concept_nodes_by_hotness = sorted(
        concept_nodes,
        key=lambda node: (
            -int(node.get("article_count", 0) or 0),
            -float(node.get("weighted_degree", 0) or 0),
            *_stable_text_key(node.get("id")),
        ),
    )
    hot_concept_ids = {
        node["id"]
        for node in concept_nodes_by_hotness[: max(0, int(hot_concept_limit))]
        if node.get("id")
    }
    hot_concept_nodes = [n for n in concept_nodes if n.get("id") in hot_concept_ids]
    hot_concept_links = [l for l in concept_links if l.get("source") in hot_concept_ids and l.get("target") in hot_concept_ids]

    source_stats = source_graph.get("stats") if isinstance(source_graph.get("stats"), dict) else {}
    tag_stats = source_stats.get("tag_stats") if isinstance(source_stats, dict) else None
    global_stats = _graph_stats(nodes, links, tag_stats=tag_stats)
    global_stats["total_communities"] = len(community["communities"])
    community_summary, community_hotspot_files = _build_runtime_community_payloads(
        community,
        nodes,
        links,
    )
    focus_shard_files = _build_focus_shard_payloads(nodes, links)
    files = {
        "core": "core.json",
        "tagHot": "tag.hot.json",
        "conceptHot": "concept.hot.json",
        "tag": "tag.json",
        "community": "community.json",
        "communityHotspots": "community-hotspots/",
        "search": "search.json",
        "focusShards": [
            relative_path for relative_path, _payload in focus_shard_files
        ],
    }
    defaults = {
        "mode": "overview",
        "hot_tag_limit": hot_tag_limit,
        "hot_concept_limit": hot_concept_limit,
        "community_limit": community_limit,
        "community_hotspot_limit": COMMUNITY_HOTSPOT_LIMIT,
        "community_hotspot_link_limit": COMMUNITY_HOTSPOT_LINK_LIMIT,
        "initial_visible_layers": [
            "language",
            "framework",
            "model",
            "application",
            "scenario",
        ],
    }

    _write_stable_json(out_dir / "core.json", {
        "version": GRAPH_VERSION,
        "generated_at": generated_at,
        "nodes": core_nodes,
        "links": core_links,
        "layers": layers,
        "stats": _graph_stats(core_nodes, core_links),
    })

    hot_tag_payload_links = sorted(hot_tag_links + hot_tag_to_tech_links, key=_edge_sort_key)
    _write_stable_json(out_dir / "tag.hot.json", {
        "version": GRAPH_VERSION,
        "generated_at": generated_at,
        "nodes": hot_tag_nodes,
        "links": hot_tag_payload_links,
        "layer": "tag",
        "layers": layers,
        "stats": _graph_stats(hot_tag_nodes, hot_tag_payload_links),
    })

    _write_stable_json(out_dir / "concept.hot.json", {
        "version": GRAPH_VERSION,
        "generated_at": generated_at,
        "nodes": hot_concept_nodes,
        "links": hot_concept_links,
        "layer": "concept",
        "layers": layers,
        "stats": _graph_stats(hot_concept_nodes, hot_concept_links),
    })

    tag_payload_links = sorted(tag_links + tag_to_tech_links, key=_edge_sort_key)
    _write_stable_json(out_dir / "tag.json", {
        "version": GRAPH_VERSION,
        "generated_at": generated_at,
        "nodes": tag_nodes,
        "links": tag_payload_links,
        "layer": "tag",
        "layers": layers,
        "stats": _graph_stats(tag_nodes, tag_payload_links),
    })

    legacy_hotspot_file = out_dir / "community.hotspots.json"
    if legacy_hotspot_file.exists():
        legacy_hotspot_file.unlink()
    hotspot_dir = out_dir / "community-hotspots"
    hotspot_dir.mkdir(parents=True, exist_ok=True)
    for relative_path, payload in community_hotspot_files:
        _write_stable_json(out_dir / relative_path, payload)
    current_hotspot_files = {
        Path(relative_path).name
        for relative_path, _payload in community_hotspot_files
    }
    retained_hotspot_files = current_hotspot_files | previous_hotspot_files
    for stale_file in hotspot_dir.glob("*.json"):
        if stale_file.name not in retained_hotspot_files:
            stale_file.unlink()
    _write_stable_json(out_dir / "community.json", community_summary)
    focus_shard_dir = out_dir / "focus-shards"
    focus_shard_dir.mkdir(parents=True, exist_ok=True)
    for relative_path, payload in focus_shard_files:
        _write_stable_compact_json(out_dir / relative_path, payload)
    current_focus_shard_files = {
        Path(relative_path).name
        for relative_path, _payload in focus_shard_files
    }
    retained_focus_shard_files = (
        current_focus_shard_files | previous_focus_shard_files
    )
    for stale_file in focus_shard_dir.glob("*.json"):
        if stale_file.name not in retained_focus_shard_files:
            stale_file.unlink()
    _write_stable_json(
        out_dir / "search.json",
        build_search_index(nodes, generated_at=generated_at),
    )
    _write_stable_json(out_dir / "index.json", {
        "version": GRAPH_VERSION,
        "generated_at": generated_at,
        "layers": layers,
        "files": files,
        "defaults": defaults,
        "stats": global_stats,
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
