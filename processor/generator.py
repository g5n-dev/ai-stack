"""
Content generator
内容生成模块
"""

from typing import Dict, List
import logging

from .anthropic_client import AnthropicClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentGenerator:
    """内容生成器"""

    def __init__(self, client: AnthropicClient, intro_length=100, comment_length=300):
        self.client = client
        self.intro_length = intro_length
        self.comment_length = comment_length

    def generate_intro(self, content: Dict) -> str:
        """
        生成内容引言

        Args:
            content: 内容数据

        Returns:
            str: 生成的引言
        """
        try:
            prompt = self._build_intro_prompt(content)
            intro = self.client.create_message(prompt, max_tokens=200)
            return intro.strip()

        except Exception as e:
            logger.error(f"Failed to generate intro: {e}")
            return ""

    def generate_comment(self, content: Dict) -> str:
        """
        生成内容评论

        Args:
            content: 内容数据

        Returns:
            str: 生成的评论
        """
        try:
            prompt = self._build_comment_prompt(content)
            comment = self.client.create_message(prompt, max_tokens=500)
            return comment.strip()

        except Exception as e:
            logger.error(f"Failed to generate comment: {e}")
            return ""

    def generate_analysis(self, content: Dict) -> str:
        """
        生成深度分析

        Args:
            content: 内容数据

        Returns:
            str: 生成的分析
        """
        try:
            prompt = self._build_analysis_prompt(content)
            analysis = self.client.create_message(prompt, max_tokens=800)
            return analysis.strip()

        except Exception as e:
            logger.error(f"Failed to generate analysis: {e}")
            return ""

    def _build_intro_prompt(self, content: Dict) -> str:
        """构建引言生成提示词"""
        source = content.get('source', '')
        title = content.get('title', '')

        if source == 'github_trending':
            prompt = f"""请为以下 GitHub 仓库写一个简短的引言，不超过{self.intro_length}字，用中文：

仓库名称：{title}
描述：{content.get('description', '')}
语言：{content.get('language', '')}
"""
        elif source in ['hacker_news', 'juejin']:
            prompt = f"""请为以下文章写一个简短的引言，不超过{self.intro_length}字，用中文：

文章标题：{title}
描述：{content.get('description', '')[:100]}
"""
        elif source == 'arxiv':
            prompt = f"""请为以下论文写一个简短的引言，不超过{self.intro_length}字，用中文：

论文标题：{title}
摘要：{content.get('summary', '')[:150]}
"""
        else:
            prompt = f"""请为以下内容写一个简短的引言，不超过{self.intro_length}字，用中文：

标题：{title}
"""

        return prompt

    def _build_comment_prompt(self, content: Dict) -> str:
        """构建评论生成提示词"""
        source = content.get('source', '')
        title = content.get('title', '')

        if source == 'github_trending':
            prompt = f"""请从技术角度评价以下 GitHub 仓库，不超过{self.comment_length}字，用中文：

仓库名称：{title}
描述：{content.get('description', '')}
星标数：{content.get('stars', '')}
请从实用性、创新性、社区活跃度等方面进行评价。
"""
        elif source in ['hacker_news', 'juejin']:
            prompt = f"""请评价以下文章的技术价值，不超过{self.comment_length}字，用中文：

文章标题：{title}
请从内容的深度、实用性、创新性等方面进行评价。
"""
        elif source == 'arxiv':
            prompt = f"""请评价以下论文的研究价值，不超过{self.comment_length}字，用中文：

论文标题：{title}
作者：{', '.join(content.get('authors', [])[:3])}
摘要：{content.get('summary', '')[:200]}
请从研究创新性、实际应用价值、研究方法等方面进行评价。
"""
        else:
            prompt = f"""请评价以下内容，不超过{self.comment_length}字，用中文：

标题：{title}
"""

        return prompt

    def _build_analysis_prompt(self, content: Dict) -> str:
        """构建分析生成提示词"""
        source = content.get('source', '')
        title = content.get('title', '')

        if source == 'github_trending':
            prompt = f"""请深入分析以下 GitHub 仓库的技术特点和潜在应用，用中文：

仓库名称：{title}
描述：{content.get('description', '')}
语言：{content.get('language', '')}
星标数：{content.get('stars', '')}

请从以下角度进行分析：
1. 技术架构和设计理念
2. 适用场景和使用建议
3. 与同类项目的对比
4. 发展趋势和前景
"""
        elif source in ['hacker_news', 'juejin']:
            prompt = f"""请深入分析以下文章的核心观点和技术要点，用中文：

文章标题：{title}
摘要：{content.get('description', '')[:200]}

请从以下角度进行分析：
1. 核心观点和关键技术
2. 对行业的启示
3. 实际应用价值
4. 延伸思考和建议
"""
        elif source == 'arxiv':
            prompt = f"""请深入分析以下论文的研究内容和贡献，用中文：

论文标题：{title}
作者：{', '.join(content.get('authors', []))}
摘要：{content.get('summary', '')}

请从以下角度进行分析：
1. 研究背景和问题
2. 核心方法和技术创新
3. 实验结果和效果
4. 对该领域的影响和启示
"""
        else:
            prompt = f"""请深入分析以下内容，用中文：

标题：{title}
"""

        return prompt

    def process_content(self, content: Dict) -> Dict:
        """
        处理内容，生成引言、评论和分析

        Args:
            content: 内容数据

        Returns:
            Dict: 包含生成内容的数据
        """
        try:
            # 生成引言
            content['generated_intro'] = self.generate_intro(content)

            # 生成评论
            content['generated_comment'] = self.generate_comment(content)

            # 生成分析
            content['generated_analysis'] = self.generate_analysis(content)

            return content

        except Exception as e:
            logger.error(f"Failed to process content: {e}")
            return content


if __name__ == '__main__':
    client = AnthropicClient()
    generator = ContentGenerator(client)

    test_content = {
        'source': 'github_trending',
        'title': 'test-repo',
        'description': 'A powerful tool for developers',
        'language': 'Python',
        'stars': '1234'
    }

    intro = generator.generate_intro(test_content)
    comment = generator.generate_comment(test_content)
    analysis = generator.generate_analysis(test_content)

    print(f"Intro: {intro}")
    print(f"\nComment: {comment}")
    print(f"\nAnalysis: {analysis[:200]}...")
