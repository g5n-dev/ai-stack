#!/usr/bin/env python3
"""
Super Enhanced Content generation script
超级增强版内容生成主脚本 - 整合爬虫、处理和推送
15+ 次大模型调用，生成极致高质量的文章内容
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import logging
import argparse

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from crawler.main import CrawlerOrchestrator
from processor.main import ProcessorOrchestrator
from publisher.main import PublisherOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SuperEnhancedContentGenerator:
    """超级增强版内容生成器 - 极致质量模式"""

    def __init__(self, *, dedupe: bool = True, dedupe_scope: str = "global"):
        self.crawler = CrawlerOrchestrator(dedupe=dedupe, dedupe_scope=dedupe_scope)
        self.processor = ProcessorOrchestrator()
        self.publisher = PublisherOrchestrator()
        self.posts_dir = project_root / 'blog' / 'content' / 'posts'

        # 确保 posts 目录存在
        self.posts_dir.mkdir(parents=True, exist_ok=True)

    def run(self, *, crawl_duration_hours: float = 0, crawl_interval_minutes: int = 30):
        """运行完整的超级增强内容生成流程"""
        try:
            logger.info("=" * 80)
            logger.info("🚀🚀🚀 Starting SUPER ENHANCED content generation process 🚀🚀🚀")
            logger.info("Mode: 15+ LLM calls per article for maximum quality!")
            logger.info("=" * 80)

            # 1. 爬取内容
            logger.info("\n[1/4] 🕷️  Crawling content from sources...")
            if crawl_duration_hours and crawl_duration_hours > 0:
                crawled_data = self.crawler.crawl_for_duration(
                    duration_hours=crawl_duration_hours,
                    interval_minutes=crawl_interval_minutes,
                )
            else:
                crawled_data = self.crawler.crawl_all()

            total_items = sum(len(items) for items in crawled_data.values())
            logger.info(f"✓ Crawled {total_items} items from {len(crawled_data)} sources")

            # 2. 超级增强处理（15次大模型调用）
            logger.info("\n[2/4] 🤖🤖🤖  Processing content with AI (15+ LLM calls)...")
            logger.info("    This may take a while, but the result will be amazing! 🔥")
            processed_data = self.processor.process_by_source(crawled_data)
            logger.info(f"✓ Super enhanced content from {len(processed_data)} sources")

            # 3. 生成超级增强版 Markdown 文章
            logger.info("\n[3/4] 📝📝📝  Generating Super Enhanced Markdown posts...")
            posts_created = self._generate_posts(processed_data)
            logger.info(f"✓ Created {posts_created} Super Enhanced Markdown posts")

            # 4. 推送内容
            logger.info("\n[4/4] 📢  Publishing to social platforms...")
            self._publish_content(processed_data)

            logger.info("\n" + "=" * 80)
            logger.info("✅✅✅ Super Enhanced content generation completed successfully! ✅✅✅")
            logger.info("Each article contains 15+ AI-generated sections! 🎉")
            logger.info("=" * 80)

            return True

        except Exception as e:
            logger.error(f"❌ Content generation failed: {e}", exc_info=True)
            return False

    def _generate_posts(self, processed_data: dict) -> int:
        """
        生成超级增强版 Markdown 文章文件

        Args:
            processed_data: 处理后的数据

        Returns:
            int: 创建的文章数量
        """
        created_count = 0
        timestamp = datetime.now().strftime('%Y%m%d')

        for source, items in processed_data.items():
            for idx, item in enumerate(items):
                try:
                    # 生成文件名
                    slug = self._generate_slug(item.get('title', ''), idx)
                    filename = f"{timestamp}-{source}-{slug}.md"
                    filepath = self.posts_dir / filename

                    # 生成 Markdown 内容
                    markdown_content = self._format_super_enhanced_markdown(item)

                    # 写入文件
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)

                    logger.info(f"✓ Created super enhanced post: {filename}")
                    created_count += 1

                except Exception as e:
                    logger.error(f"Failed to generate post for {item.get('title', 'Unknown')}: {e}")
                    continue

        return created_count

    def _generate_slug(self, title: str, index: int) -> str:
        """生成 URL 友好的 slug"""
        import re
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')[:50]
        return f"{slug}-{index}"

    def _format_super_enhanced_markdown(self, item: dict) -> str:
        """
        格式化内容为超级增强版 Markdown（15+ 个章节）

        Args:
            item: 内容项

        Returns:
            str: Markdown 内容
        """
        source = item.get('source', 'unknown')
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', 'Untitled')
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

        # 构建标签
        tags = item.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        tags_str = ', '.join([f'"{tag}"' for tag in tags])

        # 构建分类
        categories = item.get('categories', [])
        if isinstance(categories, str):
            categories = [categories]
        categories_str = ', '.join([f'"{cat}"' for cat in categories])

        # 获取 URL
        url = item.get('url', '')
        if not url and source == 'github_trending':
            url = item.get('repo_url', '')

        # 开始构建 Markdown
        lines = [
            '---',
            f'title: "{title}"',
            f'date: {date}',
            'draft: false',
            'entry_kind: "auto"',
            f'tags: [{tags_str}]',
            f'categories: [{categories_str}]',
            f'source: {source}',
        ]

        if url:
            lines.append(f'external_url: {url}')

        lines.append('---')
        lines.append('')

        # 根据来源生成不同格式
        if source == 'github_trending':
            lines.extend(self._format_github_repo_super_enhanced(item))
        elif source == 'hacker_news':
            lines.extend(self._format_hacker_news_super_enhanced(item))
        elif source == 'arxiv':
            lines.extend(self._format_arxiv_paper_super_enhanced(item))
        elif source == 'juejin':
            lines.extend(self._format_juejin_article_super_enhanced(item))
        elif source == 'blogs_podcasts':
            lines.extend(self._format_blogs_podcasts_super_enhanced(item))
        elif source == 'twitter':
            lines.extend(self._format_twitter_brief(item))
        else:
            lines.extend(self._format_generic_super_enhanced(item))

        return '\n'.join(lines)

    def _format_twitter_brief(self, item: dict) -> list:
        account = item.get("account", "unknown")
        account_url = item.get("account_url") or item.get("url") or ""
        tweets = item.get("tweets") or []

        lines = [
            f'# 🐦 Twitter 简讯：@{account}',
            '',
            '---',
            '',
            '## 📌 信息',
            '',
            f'- **账号**: @{account}',
        ]

        if account_url:
            lines.append(f'- **主页**: [{account_url}]({account_url})')

        lines.extend([
            f'- **收录条数**: {len(tweets)}',
            '',
        ])

        if not tweets:
            lines.extend([
                '暂无可用推文。',
            ])
            self._append_references(lines, item)
            lines.extend([
                '',
                '---',
                '',
                '*本文由 AI Stack 自动生成，观点为 AI 分析，事实以引用链接为准。*',
            ])
            return lines

        lines.extend([
            '---',
            '## 📰 简讯',
        ])

        for idx, t in enumerate(tweets, 1):
            brief = t.get("brief") or {}
            headline = (brief.get("headline") or "").strip()
            url = (t.get("url") or "").strip()
            screenshot = (t.get("screenshot") or "").strip()
            text = (t.get("text") or "").strip()
            timestamp = (t.get("timestamp") or "").strip()

            lines.extend([
                '',
                '---',
                f'### {idx}. {headline or "推文更新"}',
                '',
            ])

            if timestamp:
                lines.append(f'- **时间**: {timestamp}')
            if url:
                lines.append(f'- **原推文**: [{url}]({url})')

            if screenshot:
                lines.extend([
                    '',
                    f'![tweet]({screenshot})',
                ])

            if text:
                quoted_text = text.replace("\n", " ")
                lines.extend([
                    '',
                    '#### 原话',
                    '',
                    f'> {quoted_text}',
                ])

            evidence = brief.get("evidence_snippets") or []
            if isinstance(evidence, list) and evidence:
                lines.extend([
                    '',
                    '#### 证据片段（原文摘录）',
                    '',
                ])
                for s in evidence[:5]:
                    if isinstance(s, str) and s.strip():
                        lines.append(f'- "{s.strip()}"')

            commentary = (brief.get("commentary") or "").strip()
            if commentary:
                lines.extend([
                    '',
                    '#### 点评',
                    '',
                    commentary,
                ])

            background = brief.get("background") or []
            if isinstance(background, list) and background:
                lines.extend([
                    '',
                    '#### 背景',
                    '',
                ])
                for b in background[:6]:
                    if isinstance(b, str) and b.strip():
                        lines.append(f'- {b.strip()}')

            to_verify = brief.get("to_verify") or []
            if isinstance(to_verify, list) and to_verify:
                lines.extend([
                    '',
                    '#### 待核实',
                    '',
                ])
                for v in to_verify[:6]:
                    if isinstance(v, str) and v.strip():
                        lines.append(f'- {v.strip()}')

        self._append_references(lines, item)

        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，观点为 AI 分析，事实以引用链接为准。*',
        ])

        return lines

    def _append_references(self, lines: list, item: dict) -> None:
        """追加引用信息（最小可用：原文/讨论/PDF/DeepWiki/RSS/音频）。"""
        source = item.get("source", "")

        refs: list[tuple[str, str]] = []

        url = item.get("url") or item.get("repo_url") or item.get("external_url") or ""
        if isinstance(url, str):
            url = url.strip()

        if source == "github_trending":
            if url:
                refs.append(("GitHub 仓库", url))
            deepwiki_url = (item.get("deepwiki_url") or "").strip()
            if deepwiki_url:
                refs.append(("DeepWiki", deepwiki_url))
        elif source == "hacker_news":
            if url:
                refs.append(("原文链接", url))
            hn_id = item.get("hn_id")
            if hn_id:
                refs.append(("HN 讨论", f"https://news.ycombinator.com/item?id={hn_id}"))
        elif source == "arxiv":
            if url:
                refs.append(("ArXiv", url))
            pdf_url = (item.get("pdf_url") or "").strip()
            if pdf_url:
                refs.append(("PDF", pdf_url))
        elif source == "blogs_podcasts":
            if url:
                refs.append(("文章/节目", url))
            audio_url = (item.get("audio_url") or "").strip()
            if audio_url:
                refs.append(("音频", audio_url))
            feed_url = (item.get("feed_url") or "").strip()
            if feed_url:
                refs.append(("RSS 源", feed_url))
        elif source == "juejin":
            if url:
                refs.append(("掘金原文", url))
        else:
            if url:
                refs.append(("原文链接", url))

        if not refs:
            return

        lines.extend([
            '',
            '---',
            '## 🔗 引用',
            '',
        ])

        for label, link in refs:
            lines.append(f'- **{label}**: [{link}]({link})')

        lines.extend([
            '',
            '> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。',
        ])

    def _format_github_repo_super_enhanced(self, item: dict) -> list:
        """格式化 GitHub 仓库（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')
        original_title = item.get('title', '')
        description = item.get("description_translated") or item.get("description", "")

        lines = [
            f'# 🚀 {title}',
            '',
            f'> 💡 **原名**: {original_title}',
            '',
            '---',
            '',
            '## 📋 基本信息',
            '',
            f'- **描述**: {description}',
            f'- **语言**: {item.get("language", "Unknown")}',
            f'- **星标**: {item.get("stars", "0")} (+{item.get("today_stars", "0")})',
        ]

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        if item.get('deepwiki_url'):
            lines.append(f'- **DeepWiki**: [{item.get("deepwiki_url", "")}]({item.get("deepwiki_url", "")})')

        if item.get('deepwiki_content'):
            lines.extend([
                '',
                '---',
                '## 📚 DeepWiki 速览（节选）',
                '',
                item.get('deepwiki_content', ''),
            ])

        # 1. 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## ✨ 引人入胜的引言',
                '',
                item.get('engaging_intro', ''),
            ])

        # 2. AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 📝 AI 总结',
                '',
                item.get('summary', ''),
            ])

        # 3. 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 🎯 深度评价',
                '',
                item.get('deep_comment', ''),
            ])

        # 4. 全面技术分析
        if item.get('comprehensive_analysis'):
            lines.extend([
                '',
                '---',
                '## 🔍 全面技术分析',
                '',
                item.get('comprehensive_analysis', ''),
            ])

        # 5. 代码示例
        if item.get('code_examples'):
            lines.extend([
                '',
                '---',
                '## 💻 实用代码示例',
                '',
            ])
            for example in item.get('code_examples', []):
                lines.extend([
                    '',
                    example.get('description', ''),
                    '',
                    example.get('code', ''),
                ])

        # 6. 案例研究
        if item.get('case_studies'):
            lines.extend([
                '',
                '---',
                '## 📚 真实案例研究',
                '',
            ])
            for study in item.get('case_studies', []):
                lines.extend([
                    '',
                    f"### {study.get('title', '案例')}",
                    '',
                    study.get('content', ''),
                ])

        # 7. 对比分析
        if item.get('comparison_analysis'):
            lines.extend([
                '',
                '---',
                '## ⚖️ 与同类方案对比',
                '',
                item.get('comparison_analysis', ''),
            ])

        # 8. 最佳实践
        if item.get('best_practices'):
            lines.extend([
                '',
                '---',
                '## ✅ 最佳实践指南',
                '',
                item.get('best_practices', ''),
            ])

        # 9. 性能优化
        if item.get('performance_tips'):
            lines.extend([
                '',
                '---',
                '## 🚀 性能优化建议',
                '',
                item.get('performance_tips', ''),
            ])

        # 10. 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 🎓 核心学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # 11. 学习路径
        if item.get('learning_path'):
            lines.extend([
                '',
                '',
                '---',
                '## 🗺️ 循序渐进的学习路径',
                '',
                item.get('learning_path', ''),
            ])

        # 12. FAQ
        if item.get('faq'):
            lines.extend([
                '',
                '---',
                '## ❓ 常见问题解答',
                '',
            ])
            for faq in item.get('faq', []):
                lines.extend([
                    '',
                    f"### {faq.get('question', 'Question')}",
                    '',
                    faq.get('answer', 'Answer'),
                ])

        # 13. 挑战和思考
        if item.get('challenges'):
            lines.extend([
                '',
                '---',
                '## 🎯 挑战与思考题',
                '',
            ])
            for challenge in item.get('challenges', []):
                lines.extend([
                    '',
                    f"### {challenge}",
                ])

        # 14. 实践建议
        if item.get('practical_recommendations'):
            lines.extend([
                '',
                '---',
                '## 💡 实践建议',
                '',
                item.get('practical_recommendations', ''),
            ])

        # 15. 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 🔗 推荐学习资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**",
                    f"  - 链接: {resource.get('link', '')}",
                    f"  - 说明: {resource.get('description', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*',
            '',
            '**📚 更多精彩内容，敬请关注！**',
        ])

        return lines

    def _format_hacker_news_super_enhanced(self, item: dict) -> list:
        """格式化 Hacker News 故事（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')

        lines = [
            f'# 📰 {title}',
            '',
            '---',
            '',
            '## 📋 基本信息',
            '',
            f'- **作者**: {item.get("author", "")}',
            f'- **评分**: {item.get("score", "0")}',
            f'- **评论数**: {item.get("descendants", "0")}',
        ]

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        if item.get("hn_id"):
            hn_url = f'https://news.ycombinator.com/item?id={item.get("hn_id")}'
            lines.append(f'- **HN 讨论**: [{hn_url}]({hn_url})')

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## ✨ 引人入胜的引言',
                '',
                item.get('engaging_intro', ''),
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 📝 AI 总结',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 🎯 深度评价',
                '',
                item.get('deep_comment', ''),
            ])

        # 代码示例
        if item.get('code_examples'):
            lines.extend([
                '',
                '---',
                '## 💻 代码示例',
                '',
            ])
            for example in item.get('code_examples', []):
                lines.extend([
                    '',
                    example.get('description', ''),
                    '',
                    example.get('code', ''),
                ])

        # 案例研究
        if item.get('case_studies'):
            lines.extend([
                '',
                '---',
                '## 📚 案例研究',
                '',
            ])
            for study in item.get('case_studies', []):
                lines.extend([
                    '',
                    f"### {study.get('title', '案例')}",
                    '',
                    study.get('content', ''),
                ])

        # 最佳实践
        if item.get('best_practices'):
            lines.extend([
                '',
                '---',
                '## ✅ 最佳实践',
                '',
                item.get('best_practices', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 🎓 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # FAQ
        if item.get('faq'):
            lines.extend([
                '',
                '---',
                '## ❓ 常见问题',
                '',
            ])
            for faq in item.get('faq', []):
                lines.extend([
                    '',
                    f"### {faq.get('question', 'Q')}",
                    '',
                    faq.get('answer', 'A'),
                ])

        # 挑战
        if item.get('challenges'):
            lines.extend([
                '',
                '---',
                '## 🎯 思考题',
                '',
            ])
            for challenge in item.get('challenges', []):
                lines.extend([
                    '',
                    f"### {challenge}",
                ])

        # 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 🔗 推荐资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**: {resource.get('link', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*',
        ])

        return lines

    def _format_blogs_podcasts_super_enhanced(self, item: dict) -> list:
        """格式化博客/播客条目（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')
        description = item.get("description_translated") or item.get("description", "")

        lines = [
            f'# 🎙️ {title}',
            '',
            '---',
            '',
            '## 📋 基本信息',
            '',
            f'- **来源**: {item.get("feed_name", "")} ({item.get("feed_type", "")})',
            f'- **发布时间**: {item.get("published_at") or item.get("published") or ""}',
        ]

        if item.get('url'):
            lines.append(f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})')

        if item.get('audio_url'):
            lines.append(f'- **音频**: [{item.get("audio_url", "")}]({item.get("audio_url", "")})')

        if description:
            lines.extend([
                '',
                '---',
                '## 📄 摘要/简介',
                '',
                description,
            ])

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## ✨ 引人入胜的引言',
                '',
                item.get('engaging_intro', ''),
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 📝 AI 总结',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 🎯 深度评价',
                '',
                item.get('deep_comment', ''),
            ])

        # 全面分析
        if item.get('comprehensive_analysis'):
            lines.extend([
                '',
                '---',
                '## 🔍 全面分析',
                '',
                item.get('comprehensive_analysis', ''),
            ])

        # 最佳实践
        if item.get('best_practices'):
            lines.extend([
                '',
                '---',
                '## ✅ 最佳实践',
                '',
                item.get('best_practices', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 🎓 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 🔗 推荐资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**: {resource.get('link', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*',
        ])

        return lines

    def _format_arxiv_paper_super_enhanced(self, item: dict) -> list:
        """格式化 ArXiv 论文（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')

        lines = [
            f'# 📚 {title}',
            '',
            '---',
            '',
            '## 📋 基本信息',
            '',
            f'- **ArXiv ID**: {item.get("arxiv_id", "")}',
            f'- **分类**: {item.get("category", "")}',
            f'- **作者**: {", ".join(item.get("authors", [])[:5])}',
        ]

        if item.get('pdf_url'):
            lines.extend([
                f'- **PDF**: [{item.get("pdf_url", "")}]({item.get("pdf_url", "")})',
            ])

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## ✨ 引人入胜的引言',
                '',
                item.get('engaging_intro', ''),
            ])

        # 摘要
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 📄 摘要',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 🎯 深度评价',
                '',
                item.get('deep_comment', ''),
            ])

        # 全面分析
        if item.get('comprehensive_analysis'):
            lines.extend([
                '',
                '---',
                '## 🔍 全面分析',
                '',
                item.get('comprehensive_analysis', ''),
            ])

        # 最佳实践
        if item.get('best_practices'):
            lines.extend([
                '',
                '---',
                '## ✅ 研究最佳实践',
                '',
                item.get('best_practices', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 🎓 核心学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # 学习路径
        if item.get('learning_path'):
            lines.extend([
                '',
                '',
                '---',
                '## 🗺️ 学习路径',
                '',
                item.get('learning_path', ''),
            ])

        # FAQ
        if item.get('faq'):
            lines.extend([
                '',
                '---',
                '## ❓ 常见问题',
                '',
            ])
            for faq in item.get('faq', []):
                lines.extend([
                    '',
                    f"### {faq.get('question', 'Q')}",
                    '',
                    faq.get('answer', 'A'),
                ])

        # 挑战
        if item.get('challenges'):
            lines.extend([
                '',
                '---',
                '## 🎯 思考题',
                '',
            ])
            for challenge in item.get('challenges', []):
                lines.extend([
                    '',
                    f"### {challenge}",
                ])

        # 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 🔗 推荐资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**: {resource.get('link', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，深度解读学术研究。*',
        ])

        return lines

    def _format_juejin_article_super_enhanced(self, item: dict) -> list:
        """格式化掘金文章（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')
        description = item.get("description_translated") or item.get("description", "")

        lines = [
            f'# 📝 {title}',
            '',
            '---',
            '',
            '## 📋 基本信息',
            '',
            f'- **作者**: {item.get("author", "")}',
        ]

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## ✨ 引人入胜的引言',
                '',
                item.get('engaging_intro', ''),
            ])

        # 描述
        if description:
            lines.extend([
                '',
                '---',
                '## 📄 描述',
                '',
                description,
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 📝 AI 总结',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 🎯 深度评价',
                '',
                item.get('deep_comment', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 🎓 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # FAQ
        if item.get('faq'):
            lines.extend([
                '',
                '---',
                '## ❓ 常见问题',
                '',
            ])
            for faq in item.get('faq', []):
                lines.extend([
                    '',
                    f"### {faq.get('question', 'Q')}",
                    '',
                    faq.get('answer', 'A'),
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成，提供深度内容分析。*',
        ])

        return lines

    def _format_generic_super_enhanced(self, item: dict) -> list:
        """格式化通用内容（超级增强版）"""
        title = item.get('catchy_title') or item.get('title_translated') or item.get('title', '')

        lines = [
            f'# 📖 {title}',
            '',
            '---',
            '',
            '## 📋 基本信息',
            '',
        ]

        if item.get('url'):
            lines.extend([
                f'- **链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # 引人入胜的引言
        if item.get('engaging_intro'):
            lines.extend([
                '',
                '---',
                '## ✨ 引人入胜的引言',
                '',
                item.get('engaging_intro', ''),
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '---',
                '## 📝 AI 总结',
                '',
                item.get('summary', ''),
            ])

        # 深度评价
        if item.get('deep_comment'):
            lines.extend([
                '',
                '---',
                '## 🎯 深度评价',
                '',
                item.get('deep_comment', ''),
            ])

        # 学习要点
        if item.get('learning_takeaways'):
            lines.extend([
                '',
                '---',
                '## 🎓 学习要点',
                '',
            ])
            for takeaway in item.get('learning_takeaways', []):
                lines.append(f'- {takeaway}')

        # 相关资源
        if item.get('related_resources'):
            lines.extend([
                '',
                '---',
                '## 🔗 推荐资源',
                '',
            ])
            for resource in item.get('related_resources', []):
                lines.extend([
                    '',
                    f"- **{resource.get('title', '')}**: {resource.get('link', '')}",
                ])

        self._append_references(lines, item)

        # 底部
        lines.extend([
            '',
            '---',
            '',
            '*本文由 AI Stack 自动生成。*',
        ])

        return lines

    def _publish_content(self, processed_data: dict):
        """
        推送内容到社交平台

        Args:
            processed_data: 处理后的数据
        """
        enabled_platforms = self.publisher.get_enabled_platforms()

        if not enabled_platforms:
            logger.info("ℹ️  No publishing platforms enabled")
            return

        # 只推送每个来源的前几篇内容
        for source, items in processed_data.items():
            for item in items[:2]:  # 每个来源最多推送2篇
                try:
                    logger.info(f"📤 Publishing {source} item to {enabled_platforms}...")
                    results = self.publisher.publish_all(item)

                    for platform, success in results.items():
                        if success:
                            logger.info(f"✅ Successfully published to {platform}")
                        else:
                            logger.warning(f"⚠️  Failed to publish to {platform}")

                except Exception as e:
                    logger.error(f"❌ Failed to publish item: {e}")
                    continue


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AI Stack content generator")
    parser.add_argument("--crawl-duration-hours", type=float, default=0, help="长时间抓取（小时），0 表示单次抓取")
    parser.add_argument("--crawl-interval-minutes", type=int, default=30, help="长时间抓取时的间隔（分钟）")
    parser.add_argument("--no-dedupe", action="store_true", help="关闭去重")
    parser.add_argument(
        "--dedupe-scope",
        choices=["global", "per_source"],
        default="global",
        help="去重范围：global=跨数据源去重，per_source=仅同数据源去重",
    )

    args = parser.parse_args()

    generator = SuperEnhancedContentGenerator(dedupe=not args.no_dedupe, dedupe_scope=args.dedupe_scope)
    success = generator.run(
        crawl_duration_hours=args.crawl_duration_hours,
        crawl_interval_minutes=args.crawl_interval_minutes,
    )

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
