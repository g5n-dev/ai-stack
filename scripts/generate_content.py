#!/usr/bin/env python3
"""
Content generation script
内容生成主脚本 - 整合爬虫、处理和推送
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import logging

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


class ContentGenerator:
    """内容生成器"""

    def __init__(self):
        self.crawler = CrawlerOrchestrator()
        self.processor = ProcessorOrchestrator()
        self.publisher = PublisherOrchestrator()
        self.posts_dir = project_root / 'blog' / 'content' / 'posts'

        # 确保 posts 目录存在
        self.posts_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        """运行完整的内容生成流程"""
        try:
            logger.info("=" * 50)
            logger.info("Starting content generation process")
            logger.info("=" * 50)

            # 1. 爬取内容
            logger.info("\n[1/4] Crawling content from sources...")
            crawled_data = self.crawler.crawl_all()

            total_items = sum(len(items) for items in crawled_data.values())
            logger.info(f"Crawled {total_items} items from {len(crawled_data)} sources")

            # 2. 处理内容
            logger.info("\n[2/4] Processing content with AI...")
            processed_data = self.processor.process_by_source(crawled_data)
            logger.info(f"Processed content from {len(processed_data)} sources")

            # 3. 生成 Markdown 文章
            logger.info("\n[3/4] Generating Markdown posts...")
            posts_created = self._generate_posts(processed_data)
            logger.info(f"Created {posts_created} Markdown posts")

            # 4. 推送内容
            logger.info("\n[4/4] Publishing to social platforms...")
            self._publish_content(processed_data)

            logger.info("\n" + "=" * 50)
            logger.info("Content generation process completed successfully!")
            logger.info("=" * 50)

            return True

        except Exception as e:
            logger.error(f"Content generation failed: {e}", exc_info=True)
            return False

    def _generate_posts(self, processed_data: dict) -> int:
        """
        生成 Markdown 文章文件

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
                    markdown_content = self._format_markdown(item)

                    # 写入文件
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)

                    logger.info(f"Created post: {filename}")
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

    def _format_markdown(self, item: dict) -> str:
        """
        格式化内容为 Markdown

        Args:
            item: 内容项

        Returns:
            str: Markdown 内容
        """
        source = item.get('source', 'unknown')
        title = item.get('title', 'Untitled')
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

        # 构建标签
        tags = item.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        tags_str = ', '.join([f'"{tag}"' for tag in tags])

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
            f'tags: [{tags_str}]',
            f'source: {source}',
        ]

        if url:
            lines.append(f'external_url: {url}')

        lines.append('---')
        lines.append('')

        # 根据来源生成不同格式
        if source == 'github_trending':
            lines.extend(self._format_github_repo(item))
        elif source == 'hacker_news':
            lines.extend(self._format_hacker_news(item))
        elif source == 'arxiv':
            lines.extend(self._format_arxiv_paper(item))
        elif source == 'juejin':
            lines.extend(self._format_juejin_article(item))
        else:
            lines.extend(self._format_generic(item))

        return '\n'.join(lines)

    def _format_github_repo(self, item: dict) -> list:
        """格式化 GitHub 仓库"""
        lines = [
            '## ➜ 仓库信息',
            '',
            f'**仓库名称**: {item.get("title", "")}',
            '',
            f'**描述**: {item.get("description", "")}',
            '',
            f'**语言**: {item.get("language", "Unknown")}',
            '',
            f'**星标**: {item.get("stars", "0")} (+{item.get("today_stars", "0")})',
        ]

        if item.get('url'):
            lines.extend([
                '',
                f'**链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # AI 总结
        if item.get('summary'):
            lines.extend([
                '',
                '## ➜ AI 总结',
                '',
                item.get('summary', ''),
            ])

        # AI 评论
        if item.get('generated_comment'):
            lines.extend([
                '',
                '## ➜ AI 评价',
                '',
                item.get('generated_comment', ''),
            ])

        # 深度分析
        if item.get('generated_analysis'):
            lines.extend([
                '',
                '## ➜ 深度分析',
                '',
                item.get('generated_analysis', ''),
            ])

        return lines

    def _format_hacker_news(self, item: dict) -> list:
        """格式化 Hacker News 故事"""
        lines = [
            '## ➜ 故事信息',
            '',
            f'**标题**: {item.get("title", "")}',
            '',
            f'**作者**: {item.get("author", "")}',
            '',
            f'**评分**: {item.get("score", "0")}',
            '',
            f'**评论数**: {item.get("descendants", "0")}',
        ]

        if item.get('url'):
            lines.extend([
                '',
                f'**链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # AI 内容
        if item.get('summary'):
            lines.extend([
                '',
                '## ➜ AI 总结',
                '',
                item.get('summary', ''),
            ])

        if item.get('generated_comment'):
            lines.extend([
                '',
                '## ➜ AI 评论',
                '',
                item.get('generated_comment', ''),
            ])

        return lines

    def _format_arxiv_paper(self, item: dict) -> list:
        """格式化 ArXiv 论文"""
        lines = [
            '## ➜ 论文信息',
            '',
            f'**标题**: {item.get("title", "")}',
            '',
            f'**ArXiv ID**: {item.get("arxiv_id", "")}',
            '',
            f'**分类**: {item.get("category", "")}',
            '',
            f'**作者**: {", ".join(item.get("authors", [])[:5])}',
        ]

        if item.get('pdf_url'):
            lines.extend([
                '',
                f'**PDF**: [{item.get("pdf_url", "")}]({item.get("pdf_url", "")})',
            ])

        if item.get('url'):
            lines.extend([
                '',
                f'**链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # 摘要
        if item.get('summary'):
            lines.extend([
                '',
                '## ➜ 摘要',
                '',
                item.get('summary', ''),
            ])

        # AI 内容
        if item.get('generated_comment'):
            lines.extend([
                '',
                '## ➜ AI 评论',
                '',
                item.get('generated_comment', ''),
            ])

        if item.get('generated_analysis'):
            lines.extend([
                '',
                '## ➜ 深度分析',
                '',
                item.get('generated_analysis', ''),
            ])

        return lines

    def _format_juejin_article(self, item: dict) -> list:
        """格式化掘金文章"""
        lines = [
            '## ➜ 文章信息',
            '',
            f'**标题**: {item.get("title", "")}',
            '',
            f'**作者**: {item.get("author", "")}',
        ]

        if item.get('url'):
            lines.extend([
                '',
                f'**链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # 描述
        if item.get('description'):
            lines.extend([
                '',
                '## ➜ 描述',
                '',
                item.get('description', ''),
            ])

        # AI 内容
        if item.get('summary'):
            lines.extend([
                '',
                '## ➜ AI 总结',
                '',
                item.get('summary', ''),
            ])

        if item.get('generated_comment'):
            lines.extend([
                '',
                '## ➜ AI 评论',
                '',
                item.get('generated_comment', ''),
            ])

        return lines

    def _format_generic(self, item: dict) -> list:
        """格式化通用内容"""
        lines = [
            '## ➜ 内容信息',
            '',
            f'**标题**: {item.get("title", "")}',
        ]

        if item.get('url'):
            lines.extend([
                '',
                f'**链接**: [{item.get("url", "")}]({item.get("url", "")})',
            ])

        # AI 内容
        if item.get('summary'):
            lines.extend([
                '',
                '## ➜ AI 总结',
                '',
                item.get('summary', ''),
            ])

        if item.get('generated_comment'):
            lines.extend([
                '',
                '## ➜ AI 评论',
                '',
                item.get('generated_comment', ''),
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
            logger.info("No publishing platforms enabled")
            return

        # 只推送每个来源的前几篇内容
        for source, items in processed_data.items():
            for item in items[:2]:  # 每个来源最多推送2篇
                try:
                    logger.info(f"Publishing {source} item to {enabled_platforms}...")
                    results = self.publisher.publish_all(item)

                    for platform, success in results.items():
                        if success:
                            logger.info(f"Successfully published to {platform}")
                        else:
                            logger.warning(f"Failed to publish to {platform}")

                except Exception as e:
                    logger.error(f"Failed to publish item: {e}")
                    continue


def main():
    """主函数"""
    generator = ContentGenerator()
    success = generator.run()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
