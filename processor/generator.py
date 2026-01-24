"""
Super Enhanced Content Generator - 超级深度内容生成模块
通过 15+ 次大模型调用，生成极其丰富、高质量、有吸引力的文章内容
"""

from typing import Dict, List
import logging

from .anthropic_client import AnthropicClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SuperEnhancedContentGenerator:
    """超级增强的内容生成器 - 极致质量模式（15+ 次大模型调用）"""

    def __init__(self, client: AnthropicClient, config: Dict = None):
        self.client = client
        self.config = config or {}
        self.intro_length = self.config.get('intro_length', 500)
        self.comment_length = self.config.get('comment_length', 1200)
        self.analysis_length = self.config.get('analysis_length', 2500)
        self.use_emoji = self.config.get('use_emoji', True)
        self.add_recommendations = self.config.get('add_recommendations', True)

        # 新增的内容生成开关
        self.generate_code_examples = self.config.get('generate_code_examples', True)
        self.generate_case_studies = self.config.get('generate_case_studies', True)
        self.generate_faq = self.config.get('generate_faq', True)
        self.generate_comparison = self.config.get('generate_comparison', True)
        self.generate_best_practices = self.config.get('generate_best_practices', True)
        self.generate_performance_tips = self.config.get('generate_performance_tips', True)
        self.generate_learning_path = self.config.get('generate_learning_path', True)
        self.generate_challenges = self.config.get('generate_challenges', True)

    # ============ 基础内容生成（3次调用） ============

    def generate_catchy_title(self, content: Dict) -> str:
        """1. 生成吸引人的标题"""
        try:
            prompt = self._build_title_prompt(content)
            title = self.client.create_message(prompt, max_tokens=200)
            return title.strip()
        except Exception as e:
            logger.error(f"Failed to generate catchy title: {e}")
            return content.get('title', '')

    def generate_engaging_intro(self, content: Dict) -> str:
        """2. 生成引人入胜的引言（故事化开头）"""
        try:
            prompt = self._build_intro_prompt(content)
            intro = self.client.create_message(prompt, max_tokens=self.intro_length)
            return intro.strip()
        except Exception as e:
            logger.error(f"Failed to generate engaging intro: {e}")
            return ""

    def generate_deep_comment(self, content: Dict) -> str:
        """3. 生成深度评论"""
        try:
            prompt = self._build_comment_prompt(content)
            comment = self.client.create_message(prompt, max_tokens=self.comment_length)
            return comment.strip()
        except Exception as e:
            logger.error(f"Failed to generate deep comment: {e}")
            return ""

    # ============ 技术深度内容（3次调用） ============

    def generate_comprehensive_analysis(self, content: Dict) -> str:
        """4. 生成全面的技术分析"""
        try:
            prompt = self._build_analysis_prompt(content)
            analysis = self.client.create_message(prompt, max_tokens=self.analysis_length)
            return analysis.strip()
        except Exception as e:
            logger.error(f"Failed to generate comprehensive analysis: {e}")
            return ""

    def generate_code_examples(self, content: Dict) -> List[Dict]:
        """5. 生成实用代码示例"""
        if not self.generate_code_examples:
            return []
        try:
            prompt = self._build_code_examples_prompt(content)
            response = self.client.create_message(prompt, max_tokens=1000)
            return self._parse_code_examples(response)
        except Exception as e:
            logger.error(f"Failed to generate code examples: {e}")
            return []

    def generate_case_studies(self, content: Dict) -> List[Dict]:
        """6. 生成真实案例研究"""
        if not self.generate_case_studies:
            return []
        try:
            prompt = self._build_case_studies_prompt(content)
            response = self.client.create_message(prompt, max_tokens=1200)
            return self._parse_case_studies(response)
        except Exception as e:
            logger.error(f"Failed to generate case studies: {e}")
            return []

    # ============ 对比和最佳实践（3次调用） ============

    def generate_comparison_analysis(self, content: Dict) -> str:
        """7. 生成与同类方案的对比分析"""
        if not self.generate_comparison:
            return ""
        try:
            prompt = self._build_comparison_prompt(content)
            comparison = self.client.create_message(prompt, max_tokens=800)
            return comparison.strip()
        except Exception as e:
            logger.error(f"Failed to generate comparison: {e}")
            return ""

    def generate_best_practices(self, content: Dict) -> str:
        """8. 生成最佳实践"""
        if not self.generate_best_practices:
            return ""
        try:
            prompt = self._build_best_practices_prompt(content)
            practices = self.client.create_message(prompt, max_tokens=1000)
            return practices.strip()
        except Exception as e:
            logger.error(f"Failed to generate best practices: {e}")
            return ""

    def generate_performance_tips(self, content: Dict) -> str:
        """9. 生成性能优化建议"""
        if not self.generate_performance_tips:
            return ""
        try:
            prompt = self._build_performance_tips_prompt(content)
            tips = self.client.create_message(prompt, max_tokens=800)
            return tips.strip()
        except Exception as e:
            logger.error(f"Failed to generate performance tips: {e}")
            return ""

    # ============ 学习资源（3次调用） ============

    def generate_learning_takeaways(self, content: Dict) -> List[str]:
        """10. 生成学习要点"""
        try:
            prompt = self._build_takeaways_prompt(content)
            response = self.client.create_message(prompt, max_tokens=400)
            takeaways = [line.strip().lstrip('•-* ') for line in response.split('\n') if line.strip()]
            return takeaways[:7]  # 最多7个要点
        except Exception as e:
            logger.error(f"Failed to generate learning takeaways: {e}")
            return []

    def generate_practical_recommendations(self, content: Dict) -> str:
        """11. 生成实践建议"""
        if not self.add_recommendations:
            return ""
        try:
            prompt = self._build_recommendations_prompt(content)
            recommendations = self.client.create_message(prompt, max_tokens=600)
            return recommendations.strip()
        except Exception as e:
            logger.error(f"Failed to generate practical recommendations: {e}")
            return ""

    def generate_related_resources(self, content: Dict) -> List[Dict]:
        """12. 生成相关资源推荐"""
        if not self.add_recommendations:
            return []
        try:
            prompt = self._build_resources_prompt(content)
            response = self.client.create_message(prompt, max_tokens=500)
            return self._parse_resources(response)
        except Exception as e:
            logger.error(f"Failed to generate related resources: {e}")
            return []

    # ============ 进阶内容（3次调用） ============

    def generate_learning_path(self, content: Dict) -> str:
        """13. 生成学习路径"""
        if not self.generate_learning_path:
            return ""
        try:
            prompt = self._build_learning_path_prompt(content)
            path = self.client.create_message(prompt, max_tokens=1000)
            return path.strip()
        except Exception as e:
            logger.error(f"Failed to generate learning path: {e}")
            return ""

    def generate_faq(self, content: Dict) -> List[Dict]:
        """14. 生成常见问题解答"""
        if not self.generate_faq:
            return []
        try:
            prompt = self._build_faq_prompt(content)
            response = self.client.create_message(prompt, max_tokens=1000)
            return self._parse_faq(response)
        except Exception as e:
            logger.error(f"Failed to generate FAQ: {e}")
            return []

    def generate_challenges(self, content: Dict) -> List[str]:
        """15. 生成挑战和思考题"""
        if not self.generate_challenges:
            return []
        try:
            prompt = self._build_challenges_prompt(content)
            response = self.client.create_message(prompt, max_tokens=600)
            challenges = [line.strip().lstrip('•-* 123456789.') for line in response.split('\n') if line.strip()]
            return challenges[:5]  # 最多5个挑战
        except Exception as e:
            logger.error(f"Failed to generate challenges: {e}")
            return []

    # ============ Prompt 构建方法 ============

    def _build_title_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        original_title = content.get('title', '')

        emoji_instruction = "适当使用emoji增加吸引力" if self.use_emoji else ""

        return f"""请基于以下内容，创作一个超级吸引人的标题，要求：
1. 保持专业性但极具吸引力
2. 突出核心价值和亮点
3. 使用中文，控制在30字以内
4. 可以使用感叹号或问号增加冲击力
5. {emoji_instruction}

原始标题：{original_title}
来源：{source}

直接返回新标题，不要其他内容。
"""

    def _build_intro_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        if source == 'github_trending':
            return f"""请为以下 GitHub 仓库写一个超级引人入胜的引言，控制在{self.intro_length}字以内：

仓库名称：{title}
描述：{content.get('description', '')}
语言：{content.get('language', '')}
星标数：{content.get('stars', '')}

要求：
1. 用一个引人入胜的故事或场景开头
2. 突出项目的独特价值和震撼点
3. 激发读者的好奇心和探索欲
4. 使用生动、有感染力的语言
5. 加入反问句或设问
6. {"适当使用emoji增加趣味性" if self.use_emoji else ""}
7. 最后一句话引导读者继续阅读

请用中文写作，要有强烈的吸引力！
"""
        elif source in ['hacker_news', 'juejin']:
            return f"""请为以下文章写一个超级引人入胜的引言，控制在{self.intro_length}字以内：

文章标题：{title}
摘要：{content.get('description', '')[:200]}

要求：
1. 用真实案例或震撼数据开头
2. 引出文章的核心问题和痛点
3. 制造强烈的悬念或提出颠覆性的观点
4. 使用生动、有感染力的语言
5. 加入反问句或设问
6. {"适当使用emoji增加趣味性" if self.use_emoji else ""}
7. 最后一句话引导读者继续阅读

请用中文写作，要有强烈的吸引力！
"""
        elif source == 'arxiv':
            return f"""请为以下论文写一个超级引人入胜的引言，控制在{self.intro_length}字以内：

论文标题：{title}
作者：{', '.join(content.get('authors', [])[:3])}
摘要：{content.get('summary', '')[:200]}

要求：
1. 用一个引人深思的问题或未来场景开头
2. 突出论文的创新点和颠覆性价值
3. 用通俗易懂的语言解释复杂概念
4. 激发读者的学术兴趣和好奇心
5. {"适当使用emoji增加趣味性" if self.use_emoji else ""}
6. 最后一句话引导读者继续阅读

请用中文写作，要有强烈的吸引力！
"""
        else:
            return f"""请为以下内容写一个超级引人入胜的引言，控制在{self.intro_length}字以内：

标题：{title}

要求：
1. 开头要有强烈的吸引力
2. 突出核心价值和震撼点
3. 使用生动、有感染力的语言
4. {"适当使用emoji增加趣味性" if self.use_emoji else ""}
5. 最后一句话引导读者继续阅读

请用中文写作，要有强烈的吸引力！
"""

    def _build_comment_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        if source == 'github_trending':
            return f"""请从技术和实用角度超级深度地评价以下 GitHub 仓库，控制在{self.comment_length}字以内：

仓库名称：{title}
描述：{content.get('description', '')}
语言：{content.get('language', '')}
星标数：{content.get('stars', '')}

请从以下维度进行评价：
1. 技术创新性：有什么独特、颠覆性的技术方案
2. 实用价值：解决了什么关键问题，应用场景有多广
3. 代码质量：架构设计、代码规范、文档完整性
4. 社区活跃度：开发者反馈、更新频率、贡献者数量
5. 学习价值：对开发者有什么启发和借鉴意义
6. 潜在问题或改进建议
7. 与同类工具的对比优势

要求：
- 深入分析，不要泛泛而谈
- 具体举例说明
- 保持专业性和客观性
- {"适当使用emoji增加可读性" if self.use_emoji else ""}
- 用中文写作
- 每个维度都要有实质性内容
"""
        elif source in ['hacker_news', 'juejin']:
            return f"""请从技术和行业角度超级深度地评价以下文章，控制在{self.comment_length}字以内：

文章标题：{title}
摘要：{content.get('description', '')[:300]}

请从以下维度进行评价：
1. 内容深度：观点的深度和论证的严谨性
2. 实用价值：对实际工作的指导意义
3. 创新性：提出了什么新观点或新方法
4. 可读性：表达的清晰度和逻辑性
5. 行业影响：对行业或社区的潜在影响
6. 争议点或不同观点
7. 实际应用建议

要求：
- 深入分析，要有自己的见解
- 批判性思考，不盲从
- 结合实际案例说明
- {"适当使用emoji增加可读性" if self.use_emoji else ""}
- 用中文写作
"""
        elif source == 'arxiv':
            return f"""请从学术和应用角度超级深度地评价以下论文，控制在{self.comment_length}字以内：

论文标题：{title}
作者：{', '.join(content.get('authors', [])[:3])}
摘要：{content.get('summary', '')[:300]}

请从以下维度进行评价：
1. 研究创新性：有什么新的发现或方法
2. 理论贡献：对现有理论有什么补充或突破
3. 实验验证：实验设计和结果的可靠性
4. 应用前景：在实际场景中的应用价值
5. 可复现性：方法是否清晰可复现
6. 相关工作对比：与同类研究的优劣
7. 局限性和未来方向

要求：
- 深入分析，要有学术眼光
- 结合具体技术细节
- 评价要有深度和广度
- {"适当使用emoji增加可读性" if self.use_emoji else ""}
- 用中文写作
"""
        else:
            return f"""请超级深度地评价以下内容，控制在{self.comment_length}字以内：

标题：{title}

要求：
- 多角度深入分析
- 提出有价值的见解
- {"适当使用emoji增加可读性" if self.use_emoji else ""}
- 用中文写作
"""

        return ""

    def _build_analysis_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        if source == 'github_trending':
            return f"""请超级深入地分析以下 GitHub 仓库的技术特点和潜在应用，用中文：

仓库名称：{title}
描述：{content.get('description', '')}
语言：{content.get('language', '')}
星标数：{content.get('stars', '')}

请从以下角度进行全面深入分析：

## 1. 技术架构深度剖析
- 采用了什么技术栈和架构模式
- 核心模块和关键设计
- 技术亮点和创新点
- 架构优势分析

## 2. 核心功能详细解读
- 主要功能和使用场景
- 解决了什么关键问题
- 与同类工具的详细对比
- 技术实现原理

## 3. 技术实现细节
- 关键算法或技术方案
- 代码组织结构和设计模式
- 性能优化和扩展性考虑
- 技术难点和解决方案

## 4. 适用场景分析
- 什么样的项目适合使用
- 在什么情况下最有效
- 不适合的场景和原因
- 集成方式和注意事项

## 5. 发展趋势展望
- 技术演进方向
- 社区反馈和改进空间
- 与前沿技术的结合
- 未来可能的发展方向

## 6. 学习建议
- 适合什么水平的开发者
- 可以从中学习到什么
- 推荐的学习路径
- 实践建议

## 7. 最佳实践建议
- 如何正确使用该工具
- 常见问题和解决方案
- 性能优化建议
- 最佳实践总结

要求：
- 深入技术细节，不要浅尝辄止
- 结合代码和架构进行分析
- 提供具体可操作的建议
- 使用markdown格式组织内容
- {"适当使用emoji增加可读性" if self.use_emoji else ""}
- 控制在{self.analysis_length}字以内
- 每个部分都要有实质性内容
"""
        elif source in ['hacker_news', 'juejin']:
            return f"""请超级深入地分析以下文章的核心观点和技术要点，用中文：

文章标题：{title}
摘要：{content.get('description', '')[:300]}

请从以下角度进行全面深入分析：

## 1. 核心观点深度解读
- 文章的主要观点是什么
- 作者想要传达的核心思想
- 观点的创新性和深度
- 为什么这个观点重要

## 2. 关键技术要点
- 涉及的关键技术或概念
- 技术原理和实现方式
- 技术难点和解决方案
- 技术创新点分析

## 3. 实际应用价值
- 对实际工作的指导意义
- 可以应用到哪些场景
- 需要注意的问题
- 实施建议

## 4. 行业影响分析
- 对行业的启示
- 可能带来的变革
- 相关领域的发展趋势
- 对行业格局的影响

## 5. 延伸思考
- 引发的其他思考
- 可以拓展的方向
- 需要进一步研究的问题
- 未来发展趋势

## 6. 实践建议
- 如何应用到自己的项目
- 具体的行动建议
- 需要补充的知识
- 实践中的注意事项

## 7. 案例分析
- 结合实际案例说明
- 成功案例分析
- 失败案例反思
- 经验教训总结

要求：
- 深入理解文章内容
- 结合实际场景分析
- 提供可操作的建议
- 使用markdown格式组织内容
- {"适当使用emoji增加可读性" if self.use_emoji else ""}
- 控制在{self.analysis_length}字以内
"""
        elif source == 'arxiv':
            return f"""请超级深入地分析以下论文的研究内容和贡献，用中文：

论文标题：{title}
作者：{', '.join(content.get('authors', []))}
摘要：{content.get('summary', '')}

请从以下角度进行全面深入分析：

## 1. 研究背景与问题
- 研究要解决的核心问题
- 问题的研究背景和意义
- 现有方法的局限性
- 为什么这个问题重要

## 2. 核心方法与创新
- 提出的核心方法是什么
- 技术创新点和贡献
- 方法的优势和特色
- 方法的理论依据

## 3. 理论基础
- 使用的理论基础或假设
- 数学模型或算法设计
- 理论分析和证明
- 理论贡献分析

## 4. 实验与结果
- 实验设计和数据集
- 主要实验结果和指标
- 结果分析和验证
- 实验的局限性

## 5. 应用前景
- 实际应用场景
- 产业化的可能性
- 与其他技术的结合
- 未来应用方向

## 6. 研究启示
- 对该领域的启示
- 可能的研究方向
- 需要进一步探索的问题
- 对后续研究的影响

## 7. 学习建议
- 适合什么背景的读者
- 需要哪些前置知识
- 推荐的阅读顺序
- 如何理解论文内容

## 8. 相关工作对比
- 与同类研究的对比
- 优势和不足分析
- 创新性评估
- 在该领域中的地位

要求：
- 深入理解论文内容
- 结合专业知识分析
- 使用markdown格式组织内容
- {"适当使用emoji增加可读性" if self.use_emoji else ""}
- 控制在{self.analysis_length}字以内
"""
        else:
            return f"""请超级深入地分析以下内容，用中文：

标题：{title}

请从技术价值、实用性、创新性等角度进行全面深入分析。
使用markdown格式组织内容，{"适当使用emoji" if self.use_emoji else ""}
控制在{self.analysis_length}字以内。
"""

        return ""

    def _build_code_examples_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请为以下内容生成 2-3 个实用的代码示例，用中文：

{title}

来源：{source}

要求：
- 代码要完整可运行
- 添加详细的中文注释
- 每个示例解决一个实际问题
- 使用代码块格式
- 简洁易懂，适合学习

格式示例：

```python
# 示例1：XXX功能
def example():
    # 代码实现
    pass
```

**说明**: 这个示例展示了...

```python
# 示例2：XXX功能
def example2():
    # 代码实现
    pass
```

**说明**: 这个示例展示了...

只返回代码示例和说明，不要其他内容。
"""

    def _build_case_studies_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请为以下内容生成 2-3 个真实的应用案例，用中文：

{title}

来源：{source}

要求：
- 案例要真实可信
- 说明背景、问题和解决方案
- 突出实际效果和价值
- 使用markdown格式
- {"适当使用emoji" if self.use_emoji else ""}

格式示例：

### 案例 1：XX公司/项目

**背景**: ...

**问题**: ...

**解决方案**: 使用XXX工具/技术...

**效果**: ...

---

### 案例 2：XX公司/项目

**背景**: ...

**问题**: ...

**解决方案**: 使用XXX工具/技术...

**效果**: ...

只返回案例内容，不要其他内容。
"""

    def _build_comparison_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请为以下内容生成与同类方案的详细对比分析，用中文：

{title}

来源：{source}

要求：
- 列出 2-3 个同类方案
- 从多个维度进行对比
- 突出优势和不足
- 使用表格或列表格式
- {"适当使用emoji" if self.use_emoji else ""}

格式示例：

## 与同类方案对比

| 维度 | {title[:10]} | 方案A | 方案B |
|------|------------|--------|--------|
| 性能 | ... | ... | ... |
| 易用性 | ... | ... | ... |
| 成本 | ... | ... | ... |

### 优势分析

- ✅ 优势1：...
- ✅ 优势2：...

### 不足分析

- ⚠️ 不足1：...
- ⚠️ 不足2：...

只返回对比内容，不要其他内容。
"""

    def _build_best_practices_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请为以下内容生成最佳实践指南，用中文：

{title}

来源：{source}

要求：
- 列出 5-7 条最佳实践
- 每条实践要有具体说明
- 提供实施建议
- 使用markdown格式
- {"适当使用emoji" if self.use_emoji else ""}

格式示例：

## 最佳实践指南

### ✅ 实践 1：[标题]

**说明**: 详细说明...

**实施步骤**:
1. 步骤1
2. 步骤2

**注意事项**: ...

---

### ✅ 实践 2：[标题]

**说明**: 详细说明...

**实施步骤**:
1. 步骤1
2. 步骤2

**注意事项**: ...

只返回最佳实践内容，不要其他内容。
"""

    def _build_performance_tips_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请为以下内容生成性能优化建议，用中文：

{title}

来源：{source}

要求：
- 列出 4-6 条性能优化建议
- 每条建议要有具体说明
- 提供实施方法
- 量化优化效果（如可能）
- 使用markdown格式
- {"适当使用emoji" if self.use_emoji else ""}

格式示例：

## 性能优化建议

### 🚀 优化 1：[标题]

**说明**: 详细说明...

**实施方法**:
1. 方法1
2. 方法2

**预期效果**: 提升XX%

---

### 🚀 优化 2：[标题]

**说明**: 详细说明...

**实施方法**:
1. 方法1
2. 方法2

**预期效果**: 提升XX%

只返回性能优化内容，不要其他内容。
"""

    def _build_takeaways_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请总结从以下内容中学到的 5-7 个关键要点，用中文：

{title}

来源：{source}

要求：
- 每个要点用一句话概括
- 突出最有价值的知识点
- 使用 • 开头
- {"可以适当使用emoji" if self.use_emoji else ""}
- 按重要性排序

格式示例：
• 要点一（最重要）
• 要点二
• 要点三
• 要点四
• 要点五
"""

    def _build_recommendations_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        if source == 'github_trending':
            return f"""请为以下 GitHub 仓库提供 5-7 条实践建议，用中文：

仓库名称：{title}
描述：{content.get('description', '')}

要求：
- 针对实际使用场景
- 提供具体可操作的建议
- 包括最佳实践和常见陷阱
- {"适当使用emoji" if self.use_emoji else ""}
"""
        elif source == 'arxiv':
            return f"""请为以下论文提供学习建议，用中文：

论文标题：{title}

要求：
- 适合的学习阶段
- 需要补充的背景知识
- 如何实践和验证
- 学习顺序建议
- {"适当使用emoji" if self.use_emoji else ""}
"""
        else:
            return f"""请为以下内容提供实践建议，用中文：

{title}

要求：
- 提供具体可操作的建议
- {"适当使用emoji" if self.use_emoji else ""}
"""

    def _build_resources_prompt(self, content: Dict) -> str:
        title = content.get('title', '')

        return f"""请推荐 5 个与以下内容相关的优质资源，用中文：

{title}

要求：
- 包括官方文档、教程、工具、博客等
- 资源要有价值和质量保证
- 说明每个资源的特点和适用场景
- 格式：
  名称：xxx
  链接：xxx
  说明：xxx

只返回推荐资源，不要其他内容。
"""

    def _build_learning_path_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请为以下内容生成一个循序渐进的学习路径，用中文：

{title}

来源：{source}

要求：
- 从入门到精通分为 3-5 个阶段
- 每个阶段说明学习内容
- 提供学习建议和资源
- 标注每个阶段需要的时间
- {"适当使用emoji" if self.use_emoji else ""}
- 使用markdown格式

格式示例：

## 学习路径

### 阶段 1：入门基础 📚

**学习内容**:
- 知识点1
- 知识点2

**学习时间**: 1-2周

**学习资源**:
- 资源1
- 资源2

**学习建议**: ...

---

### 阶段 2：进阶提升 🚀

**学习内容**:
- 知识点1
- 知识点2

**学习时间**: 2-4周

**学习资源**:
- 资源1
- 资源2

**学习建议**: ...

只返回学习路径内容，不要其他内容。
"""

    def _build_faq_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请为以下内容生成 5-7 个常见问题和解答，用中文：

{title}

来源：{source}

要求：
- 问题要真实常见
- 回答要详细准确
- 使用markdown格式
- {"适当使用emoji" if self.use_emoji else ""}

格式示例：

## 常见问题解答

### Q1: [问题]

**A**: [详细解答]

---

### Q2: [问题]

**A**: [详细解答]

只返回FAQ内容，不要其他内容。
"""

    def _build_challenges_prompt(self, content: Dict) -> str:
        source = content.get('source', '')
        title = content.get('title', '')

        return f"""请为以下内容生成 5 个挑战和思考题，用中文：

{title}

来源：{source}

要求：
- 难度递进（从简单到困难）
- 每个挑战都有实践价值
- 提供解答提示（不直接给答案）
- {"适当使用emoji" if self.use_emoji else ""}

格式示例：

## 挑战与思考题

### 挑战 1: [简单] 🌟

**问题**: ...

**提示**: ...

---

### 挑战 2: [中等] 🌟🌟

**问题**: ...

**提示**: ...

---

只返回挑战内容，不要其他内容。
"""

    # ============ 解析方法 ============

    def _parse_code_examples(self, response: str) -> List[Dict]:
        """解析代码示例响应"""
        examples = []
        lines = response.split('\n')
        current_example = {}
        for line in lines:
            if '示例' in line or 'Example' in line:
                if current_example:
                    examples.append(current_example)
                    current_example = {}
            elif line.strip().startswith('```'):
                current_example['code'] = ''
            elif line.strip() == '```' and 'code' in current_example:
                pass  # code end
            elif 'code' in current_example and current_example['code'] is not None:
                current_example['code'] += line + '\n'
            elif '说明' in line or '说明' in line:
                if 'description' in current_example:
                    examples.append(current_example)
                    current_example = {}
                current_example['description'] = line.split('说明', 1)[-1].strip()
        if current_example:
            examples.append(current_example)
        return examples

    def _parse_case_studies(self, response: str) -> List[Dict]:
        """解析案例研究响应"""
        studies = []
        # 简化解析逻辑
        sections = response.split('### 案例')
        for section in sections[1:]:  # 跳过第一个空section
            study = {'title': section.split('\n')[0].strip()}
            study['content'] = section
            studies.append(study)
        return studies[:3]

    def _parse_resources(self, response: str) -> List[Dict]:
        """解析资源响应"""
        resources = []
        lines = response.split('\n')
        current_resource = {}
        for line in lines:
            line = line.strip()
            if line.startswith('名称') or line.startswith('Title'):
                current_resource = {'title': line.split(':', 1)[1].strip()}
            elif line.startswith('链接') or line.startswith('Link'):
                if current_resource:
                    current_resource['link'] = line.split(':', 1)[1].strip()
                    resources.append(current_resource)
                    current_resource = {}
            elif line.startswith('说明') or line.startswith('说明'):
                if 'description' in current_resource:
                    resources.append(current_resource)
                    current_resource = {}
                current_resource['description'] = line.split(':', 1)[1].strip()
        return resources[:5]

    def _parse_faq(self, response: str) -> List[Dict]:
        """解析FAQ响应"""
        faqs = []
        # 简化解析逻辑
        sections = response.split('### Q')
        for section in sections[1:]:  # 跳过第一个空section
            faq = {'question': section.split('\n')[0].strip()}
            faq['answer'] = section
            faqs.append(faq)
        return faqs[:7]

    # ============ 主处理方法 ============

    def process_content(self, content: Dict) -> Dict:
        """
        处理内容，生成所有增强内容（15次大模型调用）

        Args:
            content: 内容数据

        Returns:
            Dict: 包含所有生成内容的数据
        """
        try:
            logger.info(f"🚀 Processing content with Super Enhanced Mode: {content.get('title', 'Untitled')}")

            # 基础内容（3次调用）
            logger.info("1️⃣  Generating catchy title...")
            content['catchy_title'] = self.generate_catchy_title(content)

            logger.info("2️⃣  Generating engaging intro...")
            content['engaging_intro'] = self.generate_engaging_intro(content)

            logger.info("3️⃣  Generating deep comment...")
            content['deep_comment'] = self.generate_deep_comment(content)

            # 技术深度内容（3次调用）
            logger.info("4️⃣  Generating comprehensive analysis...")
            content['comprehensive_analysis'] = self.generate_comprehensive_analysis(content)

            logger.info("5️⃣  Generating code examples...")
            content['code_examples'] = self.generate_code_examples(content)

            logger.info("6️⃣  Generating case studies...")
            content['case_studies'] = self.generate_case_studies(content)

            # 对比和最佳实践（3次调用）
            logger.info("7️⃣  Generating comparison analysis...")
            content['comparison_analysis'] = self.generate_comparison_analysis(content)

            logger.info("8️⃣  Generating best practices...")
            content['best_practices'] = self.generate_best_practices(content)

            logger.info("9️⃣  Generating performance tips...")
            content['performance_tips'] = self.generate_performance_tips(content)

            # 学习资源（3次调用）
            logger.info("🔟  Generating learning takeaways...")
            content['learning_takeaways'] = self.generate_learning_takeaways(content)

            logger.info("1️⃣1️⃣  Generating practical recommendations...")
            content['practical_recommendations'] = self.generate_practical_recommendations(content)

            logger.info("1️⃣2️⃣  Generating related resources...")
            content['related_resources'] = self.generate_related_resources(content)

            # 进阶内容（3次调用）
            logger.info("1️⃣3️⃣  Generating learning path...")
            content['learning_path'] = self.generate_learning_path(content)

            logger.info("1️⃣4️⃣  Generating FAQ...")
            content['faq'] = self.generate_faq(content)

            logger.info("1️⃣5️⃣  Generating challenges...")
            content['challenges'] = self.generate_challenges(content)

            logger.info("✅ Super Enhanced Mode processing completed successfully!")
            return content

        except Exception as e:
            logger.error(f"❌ Failed to process content: {e}")
            return content


# 向后兼容的别名
ContentGenerator = SuperEnhancedContentGenerator
EnhancedContentGenerator = SuperEnhancedContentGenerator


if __name__ == '__main__':
    # 测试代码
    from .anthropic_client import AnthropicClient

    client = AnthropicClient()
    config = {
        'intro_length': 500,
        'comment_length': 1200,
        'analysis_length': 2500,
        'use_emoji': True,
        'add_recommendations': True,
        'generate_code_examples': True,
        'generate_case_studies': True,
        'generate_faq': True,
        'generate_comparison': True,
        'generate_best_practices': True,
        'generate_performance_tips': True,
        'generate_learning_path': True,
        'generate_challenges': True,
    }
    generator = SuperEnhancedContentGenerator(client, config)

    test_content = {
        'source': 'github_trending',
        'title': 'test-repo',
        'description': 'A powerful tool for developers with advanced features and intuitive interface',
        'language': 'Python',
        'stars': '1234'
    }

    result = generator.process_content(test_content)

    print(f"Original Title: {test_content['title']}")
    print(f"Catchy Title: {result.get('catchy_title', 'N/A')}")
    print(f"\nEngaging Intro: {result.get('engaging_intro', 'N/A')}")
    print(f"\nDeep Comment: {result.get('deep_comment', 'N/A')}")
    print(f"\nCode Examples: {len(result.get('code_examples', []))} examples")
    print(f"\nCase Studies: {len(result.get('case_studies', []))} studies")
    print(f"\nTotal LLM calls: 15")
