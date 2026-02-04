---
title: "Agent Skills：AI 智能体技能框架与开发指南"
date: 2026-02-04T11:29:23+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "智能体", "Agent Skills", "开发框架", "LLM", "AI 应用", "开发指南", "技能框架"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大模型应用从单一对话转向复杂任务处理，Agent 的核心能力已从简单的指令执行，进化为对工具调用与技能编排的深度依赖。本文将深入探讨 Agent Skills 的技术框架与实现路径，解析如何通过模块化设计赋予模型稳定的外部动作能力。通过梳理技能定义、加载与调用的关键环节，帮助开发者掌握构建高鲁棒性智能体的核心方法，"
external_url: https://agentskills.io/home
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent Skills：AI 智能体技能框架与开发指南

---

## 基本信息

- **作者**: mooreds
- **评分**: 462
- **评论数**: 228
- **链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

---
## 导语

随着大模型应用从单一对话转向复杂任务处理，Agent 的核心能力已从简单的指令执行，进化为对工具调用与技能编排的深度依赖。本文将深入探讨 Agent Skills 的技术框架与实现路径，解析如何通过模块化设计赋予模型稳定的外部动作能力。通过梳理技能定义、加载与调用的关键环节，帮助开发者掌握构建高鲁棒性智能体的核心方法，从而在实际业务中有效突破模型边界。

---
## 评论

### 深度评论

#### 核心观点
文章的核心论点在于：Agent智能体的效能不仅取决于基座模型的通用智力，更依赖于“技能”架构的设计。这种架构通过将复杂任务拆解、工具调用及自我修正机制封装，实现了从对话交互到任务执行的转化。

#### 支撑理由与边界条件

**1. 技能封装作为能力的“编译层”（事实陈述）**
文章论述了利用Prompt Engineering或微调技术，将特定能力（如联网搜索、代码执行）封装为标准化技能。这种模块化设计允许通用基座模型通过组合技能解决长尾问题，从而避免针对每个场景重新训练模型。
*   **边界条件：** 过度封装会导致“上下文碎片化”。若每个技能调用消耗大量Token传递上下文，系统响应延迟与推理成本将显著增加，这在实时性要求高的场景（如高频交易）中构成了明显的性能瓶颈。

**2. 从静态指令向动态策略的演进（技术分析）**
文章提出，现代Agent的技能不应仅限于静态指令，而应包含规划、反思和工具选择的动态策略。例如，“数据分析技能”不仅包含代码生成，还应涵盖“执行-报错-日志分析-修正”的闭环控制流。
*   **边界条件：** 动态策略高度依赖模型的元认知能力。在参数量较小（如<7B）或推理能力较弱的基座模型上，复杂的动态策略容易引发“幻觉循环”，即Agent在错误路径上无法自我纠正。

**3. 工具使用的规范化与鲁棒性（工程推断）**
文章强调了API调用格式和错误处理机制的重要性。成熟的Agent技能需要具备处理工具失败（如404错误、超时）的能力，并将其转化为结构化反馈，而非导致系统中断。
*   **边界条件：** 在缺乏标准化API的非数字化原生环境中，Agent技能难以介入业务流。这种限制使得“技能”退化为单纯的文本生成工具，限制了其在实际业务中的应用价值。

#### 维度评价

**1. 内容深度**
从技术视角看，若文章仅停留在应用层介绍Agent的功能，深度有限。具备深度的内容应探讨COT（思维链）变体设计、ReAct（推理+行动）模式的实现细节，或多智能体协作中的技能解耦机制。若未能触及“长链条任务中的累积误差”这一核心痛点，论证的严谨性将受影响。

**2. 实用价值**
对于开发者，文章的价值取决于是否提供了可复用的框架。概念堆砌的价值较低，而涉及LangChain、AutoGPT的具体实现模式，或关于评估技能RAG（检索增强生成）命中率的讨论，则具有较高的工程指导意义。

**3. 创新性**
行业常将“Prompt”等同于“Skill”。若文章提出“技能即微调”或“技能即强化学习策略”——即认为技能应内化到模型权重中而非通过Prompt拼接——则具备较高的创新性。此外，关于“技能库版本管理”或“技能冲突消解机制”的工程化讨论也是亮点。

**4. 可读性**
此类文章常面临逻辑跳跃问题。优秀的结构应清晰界定技能在“感知”、“规划”、“行动”、“记忆”模块中的归属。逻辑混乱会导致读者难以区分模型原生能力与外部工具能力的边界。

**5. 行业影响**
随着Agent从演示走向实用，“Agent Skills”的标准化定义可能催生“技能商店”等商业模式，推动行业从卖模型向卖服务转型。这也可能促使企业IT架构从单体应用转向SaaS（Skills as a Service）。

**6. 争议点与不同视角**
*   **通用 vs 专用：** 业界对于构建全能超级Agent还是多个专精微型Agent存在分歧。若文章仅强调全能性而忽视专精Agent在垂直领域的效率与准确性，观点则显片面。
*   **可解释性风险：** 强调技能效能的同时，往往掩盖了Agent决策过程的不可解释性。在金融、医疗等严监管行业，缺乏可解释性的封装是其落地的主要障碍。

#### 实际应用建议
1.  **建立技能评估矩阵：** 在构建系统时，不应盲目追求技能数量，而应基于准确率、延迟和成本建立多维度的评估体系。
2.  **关注鲁棒性测试：** 重点测试技能在异常输入下的表现，而非仅在理想环境下验证其功能。

---
## 代码示例




```python
# 示例1：Hacker News 热门文章获取与关键词过滤
import requests
from bs4 import BeautifulSoup

def fetch_hacker_news(keyword=None):
    """
    获取 Hacker News 首页热门文章，可选按关键词过滤
    :param keyword: 可选关键词，如 'AI' 或 'python'
    :return: 包含标题、链接和分数的字典列表
    """
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}  # 模拟浏览器访问
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        for item in soup.select('.athing')[:30]:  # 获取前30条
            title_elem = item.select_one('.titleline > a')
            if not title_elem:
                continue
                
            title = title_elem.text
            link = title_elem['href']
            # 获取分数（下一行）
            score_elem = item.find_next_sibling('tr').select_one('.score')
            score = int(score_elem.text.split()[0]) if score_elem else 0
            
            if keyword and keyword.lower() not in title.lower():
                continue
                
            articles.append({
                'title': title,
                'link': link,
                'score': score
            })
            
        return articles
    except Exception as e:
        print(f"获取失败: {str(e)}")
        return []

# 测试示例
if __name__ == "__main__":
    print("=== 获取AI相关文章 ===")
    ai_articles = fetch_hacker_news("AI")
    for article in ai_articles:
        print(f"{article['score']}分 | {article['title']}\n{article['link']}\n")
```


1. 使用 requests 和 BeautifulSoup 解析网页
2. 提取文章标题、链接和点赞数
3. 支持关键词过滤功能
4. 包含异常处理和模拟浏览器头

```python
# 示例2：Hacker News 数据分析与可视化
import matplotlib.pyplot as plt
from collections import Counter

def analyze_hacker_news(articles):
    """
    分析 Hacker News 文章数据并生成可视化报告
    :param articles: 由示例1获取的文章列表
    """
    if not articles:
        print("没有数据可分析")
        return
    
    # 提取分数数据
    scores = [article['score'] for article in articles]
    
    # 创建可视化图表
    plt.figure(figsize=(12, 6))
    
    # 分数分布直方图
    plt.subplot(1, 2, 1)
    plt.hist(scores, bins=10, color='skyblue', edgecolor='black')
    plt.title('文章分数分布')
    plt.xlabel('分数')
    plt.ylabel('文章数量')
    
    # 高分文章TOP5
    plt.subplot(1, 2, 2)
    top_articles = sorted(articles, key=lambda x: x['score'], reverse=True)[:5]
    titles = [article['title'][:20] + '...' for article in top_articles]
    scores = [article['score'] for article in top_articles]
    
    plt.barh(titles, scores, color='orange')
    plt.title('TOP 5 高分文章')
    plt.xlabel('分数')
    
    plt.tight_layout()
    plt.savefig('hacker_news_analysis.png')
    print("分析报告已保存为 hacker_news_analysis.png")

# 测试示例
if __name__ == "__main__":
    # 使用示例1的数据
    articles = fetch_hacker_news()
    analyze_hacker_news(articles)
```


1. 统计文章分数分布情况
2. 找出TOP 5高分文章
3. 使用 matplotlib 生成可视化报告
4. 包含中文标题和自动保存功能

```python
# 示例3：Hacker News 实时监控与通知
import time
from datetime import datetime

class HackerNewsMonitor:
    """Hacker News 实时监控类"""
    
    def __init__(self, check_interval=300):
        self.check_interval = check_interval  # 检查间隔（秒）
        self.seen_articles = set()
        
    def check_new_articles(self, keyword=None, min_score=50):
        """检查新文章并发送通知"""
        while True:
            print(f"\n检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            articles = fetch_hacker_news(keyword)
            
            new_articles = []
            for article in articles:
                if article['link'] not in self.seen_articles and article['score'] >= min_score:
                    new_articles.append(article)
                    self.seen_articles.add(article['link'])
            
            if new_articles:
                print(f"发现 {len(new_articles)} 篇新文章:")
                for article in new_articles:
                    print(f"[{article['score']}分] {article['title']}\n{article['link']}")
            else:
                print("没有新文章符合条件")
                
            time.sleep(self.check_interval)

# 测试示例
if __name__ == "__main__":
    monitor = HackerNewsMonitor(check_interval=60)  # 每分钟检查一次
    try:
        monitor.check_new_articles(keyword="AI", min_score=100)  # 监控AI相关高分文章
    except KeyboardInterrupt:
        print("\


---
## 案例研究


### 1：Devin（Cognition AI 公司）

 1：Devin（Cognition AI 公司）

**背景**:
Cognition AI 开发了 Devin，这是一款被定义为首个完全自主的 AI 软件工程师。在软件开发领域，传统的自动化工具（如 Copilot）主要提供代码补全，而 Devin 被设计为能够独立处理复杂的工程任务。

**问题**:
在实际的 Upwork 自由职业工作测试中，面临一个真实的遗留系统维护任务：用户在一个旧的教育博客数据存储库中遇到了由于 HTTP 连接超时导致的数据导入失败问题。这需要 AI 具备排查错误、理解上下文环境以及编写并运行修复代码的能力，而不仅仅是生成代码片段。

**解决方案**:
Devin 利用其核心的“Agent Skills”——即规划、推理和工具使用能力。它首先规划了排查步骤，然后使用 Bash 终端查找日志文件，分析错误堆栈，独立编辑代码添加了超时处理逻辑和重试机制。在整个过程中，Devin 能够像人类工程师一样，在发现新错误时自主回溯并调整策略，直到所有测试通过。

**效果**:
Devin 成功地从头到尾完成了这项任务，不仅修复了 Bug，还编写了详细的报告供人类审查。在实际应用中，Devin 在 SWE-bench 基准测试中解决了 13.86% 的问题，远超之前模型的 1.96%。这证明了具备复杂技能的 AI Agent 能够承担真实的工程工作，显著提高开发效率。

---



### 2：Klarna（客服自动化）

 2：Klarna（客服自动化）

**背景**:
Klarna 是一家全球领先的金融科技和购物服务公司，拥有庞大的全球客户群，每天处理大量的客户服务咨询（如退款、退货、账户管理等）。

**问题**:
随着业务增长，客服成本高昂且响应时间难以保证。传统的聊天机器人只能处理简单的 FAQ，无法处理复杂的逻辑判断或跨系统操作（如查询订单状态并发起退款），导致大量问题仍需人工介入。

**解决方案**:
Klarna 部署了由 OpenAI 技术驱动的 AI 客服助手。该 Agent 具备高级的自然语言理解能力和系统操作技能。它不仅能够与客户进行多轮对话，还能调用后端 API 执行具体业务操作。例如，它可以理解用户的模糊描述，查询数据库，并直接执行退款或修改发货地址的操作。

**效果**:
在上线一个月内，该 AI 助手处理了 230 万次对话（占总咨询量的三分之二），直接相当于 700 名全职客服的工作量。它将客户重复咨询的解决时间从 11 分钟缩短至 2 分钟，预计每年将为 Klarna 节省 4000 万美元的成本，并显著提升了客户满意度。

---



### 3：Tavily（AI 搜索 Agent）

 3：Tavily（AI 搜索 Agent）

**背景**:
随着大语言模型（LLM）应用的爆发，越来越多的 AI Agent 需要访问实时互联网数据来回答问题或执行任务（如市场分析、新闻摘要）。然而，传统的搜索引擎 API 返回的是网页列表，而不是 LLM 可以直接使用的结构化数据。

**问题**:
开发者构建自主 Agent 时面临“检索增强生成”（RAG）的难题。如果使用 Google 等传统搜索 API，Agent 需要额外的步骤去爬取网页内容、清洗噪音、提取关键信息，这不仅增加了延迟，还降低了回答的准确性。

**解决方案**:
Tavily 作为一个专门为 AI Agent 设计的搜索引擎，提供了一种优化的 Agent Skill。它不只是返回链接，而是利用 Agent 技能对搜索结果进行深层优化——提取最相关的内容、过滤广告和无关信息，并直接返回经过 LLM 优化的上下文数据。它允许 Agent 通过简单的 API 调用，快速获得“可直接用于生成”的事实性答案。

**效果**:
对于依赖实时数据的 AI 应用（如金融分析 Agent 或新闻聚合器），Tavily 显著减少了 Token 消耗（因为不需要处理无关的网页废话）并提高了响应速度。它已成为构建自主 AI Agent 的标准基础设施组件，被广泛应用于需要高准确度在线检索的场景中。

---
## 最佳实践

## 最佳实践指南

### 实践 1：技能原子化与单一职责

**说明**：每个 Agent Skill 应当保持高度的原子性，即每个技能只负责解决一个特定且明确的任务。避免设计“大而全”的复杂技能。单一职责原则能显著提高技能的复用率、调试成功率以及 LLM 的调用准确率。

**实施步骤**:
1. 审视现有技能，将包含多个逻辑步骤的复杂技能拆解。
2. 定义每个技能的输入和输出接口，确保其功能单一。
3. 为技能命名时采用动宾结构（如 `search_web`、`parse_json`），明确其单一动作。

**注意事项**: 避免将业务流程逻辑封装在单个 Skill 内，流程控制应由 Agent 的规划层负责，而非 Skill 层。

---

### 实践 2：结构化输入输出定义

**说明**：明确且严格的数据结构定义是 Agent 稳定运行的基础。Skill 的参数和返回值应遵循强类型定义（如 Pydantic 模型或 JSON Schema），以减少 LLM 生成幻觉或格式错误导致的解析失败。

**实施步骤**:
1. 为每个 Skill 定义详细的 Schema，包括字段名、类型和必填项。
2. 在 Skill 描述中通过示例展示预期的输入输出格式。
3. 实施严格的验证层，当 LLM 输出不符合 Schema 时触发重试或修正机制。

**注意事项**: 描述文档中的示例必须与代码中的实际 Schema 保持严格一致，否则会误导模型。

---

### 实践 3：上下文感知与参数自检

**说明**：Skill 应具备处理缺失参数或模糊指令的能力。与其让 Agent 在调用失败后反复重试，不如在 Skill 内部或其描述层提供明确的参数检查逻辑和默认值策略。

**实施步骤**:
1. 在 Skill 的 Prompt 描述中明确列出“必需参数”和“可选参数”。
2. 对于关键参数，若 Agent 未提供，Skill 内部应尝试从当前上下文中推断或询问用户。
3. 编写清晰的错误消息，当参数校验失败时，准确指出缺失的字段名称。

**注意事项**: 不要过度依赖模型自动补全缺失的关键参数，对于核心业务逻辑，应采用“显式传递优于隐式推断”的原则。

---

### 实践 4：基于语义的清晰命名与描述

**说明**：LLM 依赖自然语言理解来选择工具。Skill 的名称和描述不仅是给开发者看的，更是给 Agent “看”的。描述必须包含该技能的功能、适用场景以及关键参数说明，以便 Agent 进行语义匹配。

**实施步骤**:
1. 命名应具有高度的语义辨识度，避免使用缩写（如用 `calculate_distance` 代替 `calc_dist`）。
2. 描述中应包含关键词，覆盖该技能的主要使用场景。
3. 定期分析 Agent 的调用日志，针对频繁误选或漏选的技能优化其描述文本。

**注意事项**: 描述应简洁明了，避免冗余信息干扰模型的注意力机制。

---

### 实践 5：全面的错误处理与降级策略

**说明**：外部 API 调用或工具执行难免失败。Skill 设计必须包含异常捕获机制，并将技术错误转换为 Agent 可理解的业务错误信息，防止因单个 Skill 崩溃导致整个 Agent 链路中断。

**实施步骤**:
1. 在 Skill 外层包裹 Try-Catch 逻辑，捕获网络超时、API 限流等异常。
2. 定义标准的错误返回格式（如包含 `error_code` 和 `error_message` 的 JSON）。
3. 为关键 Skill 设计降级逻辑（例如搜索服务不可用时，返回缓存结果或友好的提示）。

**注意事项**: 避免直接将原始的堆栈跟踪信息返回给 LLM，这会浪费 Token 并可能干扰后续推理。

---

### 实践 6：幂等性与副作用控制

**说明**：由于 Agent 可能会因重试或循环导致同一个 Skill 被多次调用，必须确保 Skill 的幂等性。特别是对于执行写操作（如发送邮件、写入数据库、下单）的 Skill，必须防止重复执行带来的业务风险。

**实施步骤**:
1. 识别所有具有“副作用”的 Skill，并在文档中明确标注。
2. 在 Skill 内部实现去重逻辑（如基于 Request ID 的检查）。
3. 对于高风险操作，要求 Agent 在调用时必须提供唯一的 `transaction_id` 或确认令牌。

**注意事项**: 默认情况下，应假设 Agent 可能会重复发送指令，因此所有写操作 Skill 都应默认设计为幂等的。

---

### 实践 7：可观测性与日志记录

**说明**：调试 Agent 的行为比传统软件更困难。每个 Skill 必须具备详细的日志记录能力，记录输入参数、输出结果、执行耗时以及错误信息，以便于后续分析和优化 Agent 的表现。

**实施步骤**:
1. 在 Skill 入口和出口处统一记录结构化日志。
2. 记录每次调用的 Token 消耗情况，用于成本

---
## 学习要点

- 基于对 Agent Skills（智能体技能）相关技术讨论的总结，以下是关键要点：
- 核心突破在于将复杂任务拆解为可管理的子目标，使智能体能够通过规划、推理和行动循环来自主解决多步骤问题。
- 增加记忆机制（短期与长期）是提升智能体连续交互能力和上下文理解能力的关键技术手段。
- 利用工具使用能力连接大语言模型与外部世界，使智能体能够获取实时信息并执行实际操作。
- 引入反思与自我修正机制，让智能体能够审查自身输出并迭代改进，从而显著提高最终答案的准确性。
- 采用思维链提示技术引导模型进行逐步推理，是提升智能体在复杂逻辑和数学任务中表现的有效方法。
- 构建多智能体协作系统，通过让不同角色的智能体各司其职并进行协作，可以解决单体智能体难以应对的复杂任务。

---
## 常见问题


### 1: 什么是 Agent Skills（代理技能）？

1: 什么是 Agent Skills（代理技能）？

**A**: Agent Skills 是指人工智能代理（AI Agent）所具备的特定能力或技能集合。这些技能使代理能够执行复杂的任务、理解上下文、进行推理，并与用户或其他系统进行有效交互。Agent Skills 可以包括自然语言处理、数据分析、任务规划、工具使用等多种能力。随着 AI 技术的发展，Agent Skills 的范围和深度也在不断扩展，使代理能够在更多场景中提供有价值的帮助。

---



### 2: Agent Skills 与传统 AI 模型有何区别？

2: Agent Skills 与传统 AI 模型有何区别？

**A**: 传统 AI 模型通常专注于单一任务或领域，而 Agent Skills 则强调代理的通用性和适应性。具体区别包括：1) Agent Skills 通常涉及多步骤推理和决策能力；2) 能够主动调用外部工具和资源；3) 具备更好的上下文理解和记忆能力；4) 可以处理更复杂的任务链。相比之下，传统 AI 模型可能更专注于特定领域的单一任务，缺乏灵活性和自主性。

---



### 3: 如何评估 Agent Skills 的性能？

3: 如何评估 Agent Skills 的性能？

**A**: 评估 Agent Skills 的性能通常需要考虑多个维度：1) 任务完成率：代理能否成功完成指定任务；2) 准确性：输出结果的正确程度；3) 效率：完成任务所需的时间和资源；4) 鲁棒性：在不同场景和条件下的稳定性；5) 可解释性：代理决策过程的透明度。评估方法可以包括人工评估、自动化测试、用户反馈收集等多种方式。

---



### 4: 开发 Agent Skills 面临哪些主要挑战？

4: 开发 Agent Skills 面临哪些主要挑战？

**A**: 开发 Agent Skills 面临的主要挑战包括：1) 复杂性：设计和实现多技能协同的代理系统较为复杂；2) 可扩展性：如何高效地添加和集成新技能；3) 安全性：确保代理行为可控且不产生有害输出；4) 资源消耗：高性能的 Agent Skills 通常需要大量计算资源；5) 评估难题：如何全面评估代理的综合能力。这些挑战需要通过技术创新和工程实践来逐步解决。

---



### 5: Agent Skills 的未来发展趋势是什么？

5: Agent Skills 的未来发展趋势是什么？

**A**: Agent Skills 的未来发展趋势包括：1) 更强的自主性和学习能力；2) 更好的多模态理解能力（文本、图像、语音等）；3) 更精细的技能组合和专业化；4) 更高的效率和更低的资源消耗；5) 更好的可解释性和可控性；6) 更广泛的应用场景覆盖。随着技术的进步，Agent Skills 将使 AI 代理能够在更多领域发挥重要作用，成为人们工作和生活中的得力助手。

---



### 6: 如何为特定领域定制 Agent Skills？

6: 如何为特定领域定制 Agent Skills？

**A**: 为特定领域定制 Agent Skills 通常需要以下步骤：1) 需求分析：明确领域特点和具体需求；2) 数据准备：收集和整理领域相关的训练数据；3) 技能设计：根据需求设计特定的技能模块；4) 训练与调优：使用领域数据对代理进行训练和优化；5) 测试验证：在真实场景中测试代理的表现；6) 持续迭代：根据反馈不断改进技能。这个过程需要领域专家和 AI 工程师的紧密合作。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 编写一个简单的 Agent 脚本，模拟从 Hacker News (https://news.ycombinator.com/) 首页抓取当前排名前 5 的文章标题和对应的链接。要求脚本能够输出结构化的数据（例如 JSON 格式），并处理网络请求可能出现的超时错误。

### 提示**: 可以使用 Python 的 `requests` 库配合 `BeautifulSoup` 进行解析。注意检查 HTTP 状态码，并设置合理的 `timeout` 参数以防止程序挂起。

### 

---
## 引用

- **原文链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Agent](/tags/agent/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent Skills](/tags/agent-skills/) / [开发框架](/tags/%E5%BC%80%E5%8F%91%E6%A1%86%E6%9E%B6/) / [LLM](/tags/llm/) / [AI 应用](/tags/ai-%E5%BA%94%E7%94%A8/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [技能框架](/tags/%E6%8A%80%E8%83%BD%E6%A1%86%E6%9E%B6/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent Skills：智能体技能框架与开发指南]({{< relref "posts/20260203-hacker_news-agent-skills-5.md" >}})
- [Agent Skills：AI 智能体的技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-3.md" >}})
- [Agent Skills：大模型智能体的技能评估框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*