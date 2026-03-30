"""
Scenario Analyzer
场景分析器 - 使用 Claude 分析 GitHub 项目的应用场景
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .anthropic_client import AnthropicClient
from .scenarios import format_scenarios_for_prompt, get_scenario_icon, get_scenario_description

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ScenarioResult:
    """场景分析结果"""
    scenarios: List[Dict[str, Any]]

    def to_list(self) -> List[Dict[str, Any]]:
        """转换为列表格式，用于 frontmatter"""
        return [
            {
                "name": s["name"],
                "confidence": s["confidence"],
                "icon": s.get("icon", get_scenario_icon(s["name"])),
                "description": s.get("description", get_scenario_description(s["name"])),
            }
            for s in self.scenarios
        ]


class ScenarioAnalyzer:
    """场景分析器 - 使用 Claude 分析项目应用场景"""

    def __init__(self, client: AnthropicClient, config: Optional[Dict[str, Any]] = None):
        self.client = client
        self.config = config or {}
        self.enabled = bool(self.config.get("enabled", True))
        self.max_scenarios = int(self.config.get("max_scenarios", 3))
        self.temperature = float(self.config.get("temperature", 0.2))

    def analyze(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析内容并添加应用场景

        Args:
            content: 内容数据

        Returns:
            Dict: 添加了 scenarios 字段的内容
        """
        if not self.enabled:
            return content

        # 如果已有场景数据，跳过
        existing_scenarios = content.get("scenarios")
        if isinstance(existing_scenarios, list) and len(existing_scenarios) > 0:
            return content

        # 只分析 GitHub 项目
        source = content.get("source", "")
        if source != "github_trending":
            # 对于非 GitHub 项目，使用 fallback
            content["scenarios"] = self._fallback(content)
            return content

        try:
            prompt = self._build_prompt(content)
            raw = self.client.create_message(
                prompt,
                max_tokens=800,
                temperature=self.temperature,
                purpose="metadata",
            )
            result = self._parse_result(raw)

            if not result:
                content["scenarios"] = self._fallback(content)
                return content

            # 规范化结果并添加图标和描述
            scenarios = self._normalize(result.scenarios)
            content["scenarios"] = scenarios
            return content

        except Exception as e:
            logger.error(f"Failed to analyze scenarios: {e}")
            content["scenarios"] = self._fallback(content)
            return content

    def _build_prompt(self, content: Dict[str, Any]) -> str:
        """构建分析提示词"""
        title = (content.get("catchy_title") or content.get("title") or "").strip()
        description = (content.get("description_translated") or content.get("description") or "").strip()
        summary = (content.get("summary_translated") or content.get("summary") or "").strip()
        language = (content.get("language") or "").strip()
        tags = content.get("tags", [])
        categories = content.get("categories", [])

        # 获取 DeepWiki 内容（如果有）
        deepwiki_excerpt = (content.get("deepwiki_content") or "").strip()
        if deepwiki_excerpt:
            deepwiki_excerpt = deepwiki_excerpt[:800]

        # 构建上下文
        context_lines = [
            f"项目名称: {title}",
        ]
        if description:
            context_lines.append(f"描述: {description[:500]}")
        if summary:
            context_lines.append(f"摘要: {summary[:500]}")
        if language:
            context_lines.append(f"编程语言: {language}")
        if tags:
            context_lines.append(f"标签: {', '.join(tags[:10])}")
        if categories:
            context_lines.append(f"分类: {', '.join(categories)}")
        if deepwiki_excerpt:
            context_lines.append(f"深度分析: {deepwiki_excerpt}")

        context = "\n".join(context_lines)

        scenarios_list = format_scenarios_for_prompt()

        return f"""你是一个技术架构分析师。请分析以下 GitHub 项目，从预定义场景列表中选择 1-3 个最合适的应用场景。

{context}

可选场景（请从中选择）:
{scenarios_list}

选择标准:
1. 场景必须与项目的主要用途高度相关
2. confidence 表示相关性程度 (0.5-1.0)，越相关值越高
3. reason 简要说明选择理由 (10-20字)

请返回严格的 JSON 格式（不要 Markdown，不要解释）:
{{"scenarios": [{{"name": "场景名", "confidence": 0.95, "reason": "选择理由"}}]}}

注意:
- 场景名称必须严格匹配上述列表中的名称
- 最多选择 {self.max_scenarios} 个场景
- confidence 范围 0.5-1.0
"""

    def _parse_result(self, raw: str) -> Optional[ScenarioResult]:
        """解析 API 返回结果"""
        if not raw or not raw.strip():
            return None

        text = raw.strip()

        # 首先尝试直接解析 JSON
        parsed = self._try_json(text)
        if parsed is None:
            # 尝试提取第一个 JSON 对象
            m = re.search(r"\{[\s\S]*\}", text)
            if m:
                parsed = self._try_json(m.group(0))

        if not isinstance(parsed, dict):
            return None

        scenarios = parsed.get("scenarios")
        if not isinstance(scenarios, list):
            return None

        # 验证每个场景
        valid_scenarios = []
        for s in scenarios:
            if isinstance(s, dict) and "name" in s:
                valid_scenarios.append({
                    "name": str(s["name"]),
                    "confidence": float(s.get("confidence", 0.7)),
                    "reason": str(s.get("reason", "")),
                })

        if not valid_scenarios:
            return None

        return ScenarioResult(scenarios=valid_scenarios)

    def _try_json(self, text: str) -> Optional[Dict[str, Any]]:
        """尝试解析 JSON"""
        try:
            return json.loads(text)
        except Exception:
            return None

    def _normalize(self, scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """规范化和完善场景数据"""
        normalized = []
        seen = set()

        for s in scenarios:
            name = s.get("name", "").strip()
            if not name or name in seen:
                continue

            # 获取置信度
            confidence = float(s.get("confidence", 0.7))
            confidence = max(0.5, min(1.0, confidence))

            # 获取图标和描述
            icon = get_scenario_icon(name)
            description = s.get("reason", "") or get_scenario_description(name)

            normalized.append({
                "name": name,
                "confidence": confidence,
                "icon": icon,
                "description": description,
            })
            seen.add(name)

            if len(normalized) >= self.max_scenarios:
                break

        return normalized

    def _fallback(self, content: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """回退策略 - 基于简单规则推断场景"""
        content = content or {}
        source = content.get("source", "")
        language = (content.get("language") or "").lower()
        tags = content.get("tags", [])
        description = (content.get("description") or "").lower()

        scenarios = []
        seen = set()

        def add_scenario(name: str, confidence: float = 0.7):
            if name in seen:
                return
            scenarios.append({
                "name": name,
                "confidence": confidence,
                "icon": get_scenario_icon(name),
                "description": get_scenario_description(name),
            })
            seen.add(name)

        # 基于 source 的规则
        if source == "github_trending":
            add_scenario("Web应用开发", 0.75)

        # 基于编程语言的规则
        lang_scenarios = {
            "python": ["AI/ML项目", "数据科学", "命令行工具"],
            "javascript": ["Web应用开发", "前端开发", "全栈开发"],
            "typescript": ["Web应用开发", "前端开发", "全栈开发"],
            "java": ["后端开发", "Web应用开发"],
            "go": ["云原生/容器", "后端开发", "命令行工具"],
            "rust": ["命令行工具", "Web应用开发", "区块链"],
            "cpp": ["游戏开发", "嵌入式系统", "桌面应用"],
            "c#": ["游戏开发", "桌面应用"],
            "swift": ["移动应用"],
            "kotlin": ["移动应用", "Android"],
            "dart": ["移动应用"],
        }

        for lang, scenario_names in lang_scenarios.items():
            if lang in language or lang in language.replace("#", "").replace(" ", ""):
                for name in scenario_names[:2]:
                    add_scenario(name, 0.8)
                break

        # 基于标签的规则
        tag_keywords = {
            "ai": ["AI/ML项目", "大语言模型"],
            "ml": ["AI/ML项目", "数据科学"],
            "llm": ["大语言模型", "RAG应用"],
            "rag": ["RAG应用"],
            "nlp": ["自然语言处理"],
            "cv": ["计算机视觉"],
            "web": ["Web应用开发", "前端开发"],
            "frontend": ["前端开发"],
            "backend": ["后端开发"],
            "devops": ["DevOps/运维", "云原生/容器"],
            "kubernetes": ["Kubernetes", "云原生/容器"],
            "k8s": ["Kubernetes", "云原生/容器"],
            "docker": ["云原生/容器"],
            "security": ["安全工具"],
            "monitoring": ["监控/日志"],
            "testing": ["测试工具"],
            "cli": ["命令行工具"],
            "mobile": ["移动应用"],
            "game": ["游戏开发"],
            "iot": ["物联网"],
            "blockchain": ["区块链"],
        }

        for tag in tags:
            tag_lower = str(tag).lower()
            for keyword, scenario_names in tag_keywords.items():
                if keyword in tag_lower:
                    for name in scenario_names[:1]:
                        add_scenario(name, 0.85)
                    break

        # 基于描述的关键词
        desc_keywords = {
            "api": ["后端开发", "Web应用开发"],
            "framework": ["Web应用开发", "前端开发"],
            "library": ["工具"],
            "tool": ["命令行工具", "效率工具"],
            "database": ["数据库"],
            "agent": ["AI/ML项目", "大语言模型"],
            "chatbot": ["自然语言处理", "大语言模型"],
        }

        for keyword, scenario_names in desc_keywords.items():
            if keyword in description:
                for name in scenario_names[:1]:
                    add_scenario(name, 0.75)
                break

        # 如果没有匹配到任何场景，添加默认场景
        if not scenarios:
            add_scenario("Web应用开发", 0.6)

        return scenarios[: self.max_scenarios]


if __name__ == "__main__":
    # 测试代码
    from .anthropic_client import AnthropicClient

    client = AnthropicClient()
    analyzer = ScenarioAnalyzer(client)

    test_content = {
        "source": "github_trending",
        "title": "langflow",
        "description": "LangFlow is a UI for LangChain, built with React and Python",
        "language": "Python",
        "tags": ["ai", "llm", "langchain"],
    }

    result = analyzer.analyze(test_content)
    print(f"Scenarios: {result.get('scenarios')}")
