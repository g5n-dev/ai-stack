"""
Processor orchestrator
内容处理调度器 - 统一管理内容处理流程
"""

import yaml
import logging
from typing import List, Dict, Optional
from pathlib import Path
import json
from collections import defaultdict
from datetime import datetime

from processor.anthropic_client import AnthropicClient
from processor.summarizer import ContentSummarizer
from processor.translator import ContentTranslator
from processor.generator import SuperEnhancedContentGenerator
from processor.tagger import ContentTagger
from processor.enricher import enrich_github_repo
from processor.scenario_analyzer import ScenarioAnalyzer
from processor.tech_stack import export_to_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessorOrchestrator:
    """内容处理调度器"""

    def __init__(self, config_path='config/anthropic.yaml'):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.client = AnthropicClient(config_path)

        # 初始化处理器
        summary_config = self.config.get('summary', {})
        self.summarizer = ContentSummarizer(
            self.client,
            max_length=summary_config.get('max_length', 200)
        )

        translation_config = self.config.get('translation', {})
        self.translator = ContentTranslator(
            self.client,
            default_target_lang=translation_config.get('default_target_lang', 'zh')
        )

        generation_config = self.config.get('generation', {})
        self.generator = SuperEnhancedContentGenerator(
            self.client,
            config=generation_config
        )

        tagging_config = self.config.get('tagging', {})
        self.tagger = ContentTagger(
            self.client,
            config=tagging_config
        )

        scenario_config = self.config.get('scenarios', {})
        self.scenario_analyzer = ScenarioAnalyzer(
            self.client,
            config=scenario_config
        )

    def _extract_json(self, text: str) -> Optional[dict]:
        if not text:
            return None

        candidate = None
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            if end != -1:
                candidate = text[start:end].strip()
        if candidate is None and "[" in text and "]" in text:
            start = text.find("[")
            end = text.rfind("]") + 1
            candidate = text[start:end].strip()
        if candidate is None and "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            candidate = text[start:end].strip()

        if not candidate:
            return None

        try:
            return json.loads(candidate)
        except Exception:
            return None

    def _analyze_twitter_account(self, account: str, tweets: List[Dict]) -> Dict[str, Dict]:
        if not tweets:
            return {}

        prompt_lines = [
            "你是一个严格事实约束的科技简讯编辑。",
            "你将收到若干条来自同一账号的推文（仅包含：原文、时间、互动数、URL）。",
            "请输出 JSON 数组，每个元素对应一条推文，用于生成“简讯”文章。",
            "",
            "硬性规则：",
            "1) 不要编造任何推文中没有的信息；如果需要背景但无法确认，写“无法从推文确认”。",
            "2) 只基于推文原文做解读；允许提出推测，但必须标记为“推测”。",
            "3) 所有结论必须给出 evidence_snippets（直接引用推文中的短句/片段）。",
            "4) 输出只允许 JSON，不要额外说明。",
            "",
            "输出格式：",
            "[",
            "  {",
            "    \"url\": \"推文URL（原样回填）\",",
            "    \"headline\": \"一句话标题（<=28字）\",",
            "    \"commentary\": \"点评（<=160字，中文）\",",
            "    \"background\": [\"可确认背景点1（若无则用'无法从推文确认'）\"],",
            "    \"to_verify\": [\"需要进一步核实的问题1（若无可空数组）\"],",
            "    \"evidence_snippets\": [\"原文引用片段1\", \"原文引用片段2\"],",
            "    \"tags\": [\"建议标签1\", \"建议标签2\"]",
            "  }",
            "]",
            "",
            "推文数据：",
        ]

        for idx, t in enumerate(tweets, 1):
            prompt_lines.extend([
                f"",
                f"推文 {idx}:",
                f"url: {t.get('url', '')}",
                f"time: {t.get('timestamp', '')}",
                f"likes: {t.get('likes', '')}, retweets: {t.get('retweets', '')}, replies: {t.get('replies', '')}",
                f"text: {t.get('text', '')}",
            ])

        response = self.client.create_message("\n".join(prompt_lines), max_tokens=2048, temperature=0.2)
        parsed = self._extract_json(response)
        if not isinstance(parsed, list):
            return {}

        by_url: Dict[str, Dict] = {}
        for entry in parsed:
            if not isinstance(entry, dict):
                continue
            url = (entry.get("url") or "").strip()
            if not url:
                continue
            by_url[url] = entry
        return by_url

    def _process_twitter_source(self, tweets: List[Dict]) -> List[Dict]:
        by_account: Dict[str, List[Dict]] = defaultdict(list)
        for t in tweets:
            account = (t.get("account") or "unknown").strip()
            by_account[account].append(t)

        digests: List[Dict] = []
        now_cn = datetime.now().strftime("%Y-%m-%d %H:%M")

        for account, account_tweets in by_account.items():
            account_url = f"https://twitter.com/{account}" if account != "unknown" else ""

            analysis_by_url = {}
            try:
                analysis_by_url = self._analyze_twitter_account(account, account_tweets)
            except Exception as e:
                logger.error(f"Twitter brief analysis failed for @{account}: {e}")

            enriched_tweets: List[Dict] = []
            for t in account_tweets:
                url = (t.get("url") or "").strip()
                analysis = analysis_by_url.get(url, {}) if url else {}

                enriched = dict(t)
                enriched["brief"] = {
                    "headline": analysis.get("headline", ""),
                    "commentary": analysis.get("commentary", ""),
                    "background": analysis.get("background", []) if isinstance(analysis.get("background", []), list) else [],
                    "to_verify": analysis.get("to_verify", []) if isinstance(analysis.get("to_verify", []), list) else [],
                    "evidence_snippets": analysis.get("evidence_snippets", []) if isinstance(analysis.get("evidence_snippets", []), list) else [],
                    "tags": analysis.get("tags", []) if isinstance(analysis.get("tags", []), list) else [],
                }
                enriched_tweets.append(enriched)

            tags = ["twitter", "简讯", account]
            extra_tags: List[str] = []
            for t in enriched_tweets:
                for tag in t.get("brief", {}).get("tags", []):
                    if isinstance(tag, str) and tag.strip():
                        extra_tags.append(tag.strip())
            for tag in extra_tags[:5]:
                if tag not in tags:
                    tags.append(tag)

            digests.append({
                "source": "twitter",
                "title": f"Twitter 简讯：@{account}（{now_cn}）",
                "account": account,
                "account_url": account_url,
                "url": account_url,
                "tweets": enriched_tweets,
                "tags": tags,
                "categories": ["twitter"],
            })

        return digests

    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f).get('anthropic', {})
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}

    def process_single(self, content: Dict) -> Dict:
        """
        处理单个内容

        Args:
            content: 内容数据

        Returns:
            Dict: 处理后的内容
        """
        try:
            source = content.get('source', '')

            logger.info(f"Processing content from {source}: {content.get('title', 'N/A')}")

            # 内容增强（如 DeepWiki）
            if source == 'github_trending':
                content = enrich_github_repo(content)

            # 总结
            if source == 'github_trending':
                content = self.summarizer.summarize_repository(content)
            else:
                content = self.summarizer.summarize_article(content)

            # 翻译
            if source == 'github_trending':
                content = self.translator.translate_repository(content, target_lang='zh')
            else:
                content = self.translator.translate_article(content, target_lang='zh')

            # 生成
            content = self.generator.process_content(content)

            # 打标归类（tags + categories）
            content = self.tagger.tag(content)

            # 场景分析
            content = self.scenario_analyzer.analyze(content)

            logger.info(f"Successfully processed content from {source}")
            return content

        except Exception as e:
            logger.error(f"Failed to process content: {e}")
            return content

    def process_batch(self, contents: List[Dict]) -> List[Dict]:
        """
        批量处理内容

        Args:
            contents: 内容列表

        Returns:
            List[Dict]: 处理后的内容列表
        """
        processed = []

        for content in contents:
            try:
                processed_content = self.process_single(content)
                processed.append(processed_content)
            except Exception as e:
                logger.error(f"Failed to process content: {e}")
                # 失败的内容也保留，只是没有处理
                processed.append(content)

        logger.info(f"Processed {len(processed)} contents")
        return processed

    def process_by_source(self, results: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """
        按来源处理内容

        Args:
            results: 按来源分组的内容字典

        Returns:
            Dict[str, List[Dict]]: 处理后的内容字典
        """
        processed_results = {}

        for source, contents in results.items():
            logger.info(f"Processing {len(contents)} contents from {source}")
            if source == "twitter":
                processed_results[source] = self._process_twitter_source(contents)
            else:
                processed_results[source] = self.process_batch(contents)

        return processed_results

    def get_all_processed(self, results: Dict[str, List[Dict]]) -> List[Dict]:
        """
        获取所有处理后的内容

        Args:
            results: 按来源分组的内容字典

        Returns:
            List[Dict]: 所有处理后的内容
        """
        processed_results = self.process_by_source(results)
        all_processed = []

        for source, contents in processed_results.items():
            all_processed.extend(contents)

        return all_processed

    def export_tech_stack_data(self, output_path: str = 'blog/static/data/tech-stack.json') -> Dict:
        """
        导出技术栈图谱数据

        Args:
            output_path: 输出文件路径

        Returns:
            Dict: 技术栈数据
        """
        try:
            json_path = export_to_json(output_path)
            logger.info(f"Tech stack data exported to: {json_path}")

            # 读取并返回数据
            import json
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to export tech stack data: {e}")
            return {}


if __name__ == '__main__':
    # 测试处理器
    orchestrator = ProcessorOrchestrator()

    test_content = {
        'source': 'github_trending',
        'title': 'test-repo',
        'description': 'A powerful tool for developers',
        'language': 'Python',
        'stars': '1234',
        'today_stars': '56'
    }

    processed = orchestrator.process_single(test_content)

    print("\n=== Processed Content ===")
    print(f"Title: {processed.get('title', 'N/A')}")
    print(f"Summary: {processed.get('summary', 'N/A')}")
    print(f"Intro: {processed.get('generated_intro', 'N/A')}")
    print(f"Comment: {processed.get('generated_comment', 'N/A')[:100]}...")
