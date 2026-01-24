"""
Processor orchestrator
内容处理调度器 - 统一管理内容处理流程
"""

import yaml
import logging
from typing import List, Dict
from pathlib import Path

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
