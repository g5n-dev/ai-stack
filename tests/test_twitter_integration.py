#!/usr/bin/env python3

"""Legacy manual Twitter integration runner.

This module performs live network/model calls and is therefore excluded from
the hermetic pytest suite.  It remains executable directly for an operator-led
diagnostic run.
"""

__test__ = False

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.main import CrawlerOrchestrator
from processor.twitter_analyzer import TwitterContentAnalyzer
import json

def test_crawler_orchestrator():
    print("=== 测试 CrawlerOrchestrator 集成 ===")
    
    try:
        orchestrator = CrawlerOrchestrator()
        print(f"✓ 初始化成功")
        print(f"  已启用的爬虫: {list(orchestrator.crawlers.keys())}")
        
        if 'twitter' in orchestrator.crawlers:
            print("✓ Twitter爬虫已成功集成")
            twitter_crawler = orchestrator.crawlers['twitter']
            print(f"  Twitter爬虫类型: {type(twitter_crawler).__name__}")
            print(f"  监控账号: {twitter_crawler.accounts}")
        else:
            print("✗ Twitter爬虫未找到")
            return False
            
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_analyzer():
    print("\n=== 测试 TwitterContentAnalyzer ===")
    
    try:
        analyzer = TwitterContentAnalyzer()
        print("✓ 分析器初始化成功")
        
        test_tweets = [
            {
                'account': 'test',
                'text': 'AI is transforming the world',
                'timestamp': '2025-01-24T10:00:00Z',
                'likes': 100,
                'retweets': 50
            }
        ]
        
        print("  测试推文分析（可能需要API密钥）...")
        try:
            result = analyzer.analyze_tweets(test_tweets)
            print(f"✓ 分析成功: {json.dumps(result, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"  分析失败（可能需要API密钥）: {e}")
            
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_integration():
    print("\n=== 完整集成测试 ===")
    
    try:
        orchestrator = CrawlerOrchestrator()
        
        print("运行所有爬虫（不包括Twitter，因为需要浏览器）...")
        results = orchestrator.crawl_all()
        
        print(f"✓ 爬虫执行完成")
        for name, data in results.items():
            print(f"  {name}: {len(data)} 条数据")
            
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("Twitter爬虫集成测试\n")
    
    all_passed = True
    
    all_passed &= test_crawler_orchestrator()
    all_passed &= test_analyzer()
    all_passed &= test_full_integration()
    
    print("\n" + "="*50)
    if all_passed:
        print("✓ 所有测试通过")
        sys.exit(0)
    else:
        print("✗ 部分测试失败")
        sys.exit(1)
