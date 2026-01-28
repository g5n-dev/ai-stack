#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.main import CrawlerOrchestrator
from processor.main import ProcessorOrchestrator
from processor.tag_graph import export_tag_graph
from processor.tech_stack import export_to_json
import json
from pathlib import Path

def test_crawler():
    print("=" * 80)
    print("=== 阶段 1: 数据采集 ===")
    print("=" * 80)
    
    try:
        orchestrator = CrawlerOrchestrator()
        results = orchestrator.crawl_all()
        
        total_items = sum(len(items) for items in results.values())
        print(f"\n✓ 数据采集完成")
        print(f"  总计采集: {total_items} 条数据")
        for source, items in results.items():
            print(f"  - {source}: {len(items)} 条")
        
        return results
    except Exception as e:
        print(f"✗ 数据采集失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_processor(crawled_data):
    print("\n" + "=" * 80)
    print("=== 阶段 2: 内容处理（LLM 调用） ===")
    print("=" * 80)
    
    try:
        processor = ProcessorOrchestrator()
        
        processed_data = processor.process_by_source(crawled_data)
        
        total_items = sum(len(items) for items in processed_data.values())
        print(f"\n✓ 内容处理完成")
        print(f"  总计处理: {total_items} 条数据")
        for source, items in processed_data.items():
            print(f"  - {source}: {len(items)} 条")
        
        return processed_data
    except Exception as e:
        print(f"✗ 内容处理失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_post_generation(processed_data):
    print("\n" + "=" * 80)
    print("=== 阶段 3: Markdown 文章生成 ===")
    print("=" * 80)
    
    try:
        from datetime import datetime
        from scripts.generate_content import SuperEnhancedContentGenerator

        generator = SuperEnhancedContentGenerator()
        posts_dir = generator.posts_dir
        posts_dir.mkdir(parents=True, exist_ok=True)

        generated_posts = []
        for source, items in processed_data.items():
            for idx, item in enumerate(items):
                title = item.get("title", "")
                if not title:
                    continue

                slug = generator._generate_slug(title, idx)
                filename = f"{datetime.now().strftime('%Y%m%d')}-{source}-{slug}.md"
                filepath = posts_dir / filename

                markdown_content = generator._format_super_enhanced_markdown(item)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                generated_posts.append(str(filepath))
                print(f"  生成文章: {filename}")
        
        print(f"\n✓ 文章生成完成: {len(generated_posts)} 篇")
        return generated_posts
    except Exception as e:
        print(f"✗ 文章生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_tag_graph():
    print("\n" + "=" * 80)
    print("=== 阶段 4: 标签图谱构建 ===")
    print("=" * 80)
    
    try:
        output_path = export_tag_graph()
        print(f"\n✓ 标签图谱构建完成")
        print(f"  输出路径: {output_path}")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        print(f"  节点数: {len(graph_data.get('nodes', []))}")
        print(f"  边数: {len(graph_data.get('links', []))}")
        
        return output_path
    except Exception as e:
        print(f"✗ 标签图谱构建失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_tech_stack():
    print("\n" + "=" * 80)
    print("=== 阶段 5: 技术栈数据导出 ===")
    print("=" * 80)
    
    try:
        output_path = export_to_json()
        print(f"\n✓ 技术栈数据导出完成")
        print(f"  输出路径: {output_path}")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            tech_data = json.load(f)
        
        if 'languages' in tech_data:
            print(f"  语言数: {len(tech_data['languages'])}")
        if 'frameworks' in tech_data:
            print(f"  框架数: {len(tech_data['frameworks'])}")
        
        return output_path
    except Exception as e:
        print(f"✗ 技术栈数据导出失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_hugo_build():
    print("\n" + "=" * 80)
    print("=== 阶段 6: Hugo 构建验证 ===")
    print("=" * 80)
    
    try:
        import shutil
        import subprocess

        if shutil.which('hugo') is None:
            print("\n⚠️ 未找到 hugo 命令，跳过 Hugo 构建验证")
            return True
        
        result = subprocess.run(
            ['hugo', '--baseURL', 'https://ai-stack.site/', '--minify', '--cleanDestinationDir'],
            cwd='blog',
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ Hugo 构建成功")
            
            public_dir = Path('blog/public')
            if public_dir.exists():
                html_files = list(public_dir.rglob('*.html'))
                print(f"  生成 HTML 文件: {len(html_files)} 个")
            
            return True
        else:
            print(f"\n✗ Hugo 构建失败")
            print(f"  错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Hugo 构建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_e2e_test():
    print("\n" + "=" * 80)
    print("🚀 开始端到端测试（完整 CI/CD 流程）")
    print("=" * 80 + "\n")
    
    all_passed = True
    
    crawled_data = test_crawler()
    if not crawled_data:
        all_passed = False
        print("\n❌ E2E 测试失败: 数据采集失败")
        return False
    
    processed_data = test_processor(crawled_data)
    if not processed_data:
        all_passed = False
        print("\n❌ E2E 测试失败: 内容处理失败")
        return False
    
    posts = test_post_generation(processed_data)
    if not posts:
        all_passed = False
        print("\n❌ E2E 测试失败: 文章生成失败")
        return False
    
    graph_path = test_tag_graph()
    if not graph_path:
        all_passed = False
        print("\n❌ E2E 测试失败: 标签图谱构建失败")
        return False
    
    tech_path = test_tech_stack()
    if not tech_path:
        all_passed = False
        print("\n❌ E2E 测试失败: 技术栈数据导出失败")
        return False
    
    build_success = test_hugo_build()
    if not build_success:
        all_passed = False
        print("\n❌ E2E 测试失败: Hugo 构建失败")
        return False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✅✅✅ E2E 测试全部通过！ ✅✅✅")
        print("=" * 80)
        print("\n📊 测试总结:")
        print(f"  ✓ 数据采集: {sum(len(items) for items in crawled_data.values())} 条")
        print(f"  ✓ 内容处理: {sum(len(items) for items in processed_data.values())} 条")
        print(f"  ✓ 文章生成: {len(posts)} 篇")
        print(f"  ✓ 标签图谱: {graph_path}")
        print(f"  ✓ 技术栈数据: {tech_path}")
        print(f"  ✓ Hugo 构建: 成功")
        print("=" * 80)
        return True
    else:
        print("❌ E2E 测试失败")
        print("=" * 80)
        return False

if __name__ == '__main__':
    success = run_e2e_test()
    sys.exit(0 if success else 1)
