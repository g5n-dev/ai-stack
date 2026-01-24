"""
ArXiv papers crawler
爬取 ArXiv AI 论文
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArxivPapersCrawler:
    """爬取 ArXiv AI 论文"""

    def __init__(self, categories=None, limit=3, sort_by='submittedDate'):
        self.categories = categories or ['cs.AI', 'cs.LG', 'cs.CL']
        self.limit = limit
        self.sort_by = sort_by
        self.base_url = 'http://export.arxiv.org/api/query'

    def fetch(self) -> List[Dict]:
        """
        获取论文列表

        Returns:
            List[Dict]: 论文信息列表
        """
        try:
            # 构建查询
            query = ' OR '.join([f'cat:{cat}' for cat in self.categories])

            params = {
                'search_query': query,
                'start': 0,
                'max_results': self.limit * 2,  # 获取更多以进行过滤
                'sortBy': self.sort_by,
                'sortOrder': 'descending'
            }

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            papers = self.parse(response.text)
            return papers[:self.limit]

        except Exception as e:
            logger.error(f"Failed to fetch ArXiv papers: {e}")
            return []

    def parse(self, xml_content: str) -> List[Dict]:
        """
        解析 ArXiv XML 响应

        Args:
            xml_content: XML 内容

        Returns:
            List[Dict]: 解析后的论文信息
        """
        soup = BeautifulSoup(xml_content, 'xml')
        papers = []

        entries = soup.find_all('entry')
        for entry in entries:
            try:
                paper_info = self._extract_paper_info(entry)
                if paper_info:
                    papers.append(paper_info)
            except Exception as e:
                logger.warning(f"Failed to parse paper: {e}")
                continue

        return papers

    def _extract_paper_info(self, entry) -> Dict:
        """从条目元素中提取论文信息"""
        # 基本信息
        paper_id = entry.find('id').text
        title = entry.find('title').text.strip()
        summary = entry.find('summary').text.strip()

        # 提取 arXiv ID
        arxiv_id = paper_id.split('/')[-1]

        # 提取作者
        authors = []
        author_elems = entry.find_all('author')
        for author_elem in author_elems:
            name = author_elem.find('name').text
            authors.append(name)

        # 提取分类
        primary_category = entry.find('primary_category')
        category = primary_category['term'] if primary_category else ''

        # 提取发布日期
        published = entry.find('published').text if entry.find('published') else ''

        # 提取 PDF 链接
        pdf_link = f'https://arxiv.org/pdf/{arxiv_id}.pdf'

        return {
            'title': title,
            'arxiv_id': arxiv_id,
            'url': paper_id,
            'pdf_url': pdf_link,
            'summary': summary,
            'authors': authors,
            'category': category,
            'published': published,
            'source': 'arxiv',
            'crawled_at': datetime.now().isoformat()
        }


if __name__ == '__main__':
    crawler = ArxivPapersCrawler(limit=3)
    papers = crawler.fetch()
    print(f"Found {len(papers)} ArXiv papers:")
    for paper in papers:
        print(f"\n{paper['title']}")
        print(f"  Category: {paper['category']}")
        print(f"  Authors: {', '.join(paper['authors'][:3])}...")
        print(f"  Summary: {paper['summary'][:150]}...")
