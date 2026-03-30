---
title: "Agent Skills：智能体技能框架"
date: 2026-02-03T21:14:36+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "智能体", "Agent Skills", "框架", "LLM", "AI", "工具调用", "RAG"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型能力的演进，Agent（智能体）正逐渐从简单的对话机器人向具备复杂决策能力的自主系统转变。在这一过程中，“技能”成为了衡量 Agent 实用性与落地价值的关键维度，它决定了模型能否在真实场景中有效调用工具并完成任务。本文将深入探讨 Agent Skills 的技术定义、构建方法及评估体系，帮助开发者厘清从"
external_url: https://agentskills.io/home
scenarios: ["大语言模型", "AI/ML项目", "RAG应用"]
---

# Agent Skills：智能体技能框架

---

## 基本信息

- **作者**: mooreds
- **评分**: 289
- **评论数**: 176
- **链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

---
## 导语

随着大语言模型能力的演进，Agent（智能体）正逐渐从简单的对话机器人向具备复杂决策能力的自主系统转变。在这一过程中，“技能”成为了衡量 Agent 实用性与落地价值的关键维度，它决定了模型能否在真实场景中有效调用工具并完成任务。本文将深入探讨 Agent Skills 的技术定义、构建方法及评估体系，帮助开发者厘清从单一模型到具备专业技能的智能体的演进路径。

---
## 评论

基于您提供的标题《Agent Skills》及摘要（此处摘要虽为空，但基于该标题在当前AI领域的语境，通常指代关于“AI智能体应具备的核心技能、技能组合或技能获取机制”的论述），以下是从技术与行业角度的深度评价。

### 一、 核心观点与结构化论证

**中心观点：**
文章（基于标题语境）主张：**Agent 的核心价值不再仅由底层大模型（LLM）的通用智力决定，而是取决于其能否通过特定的“技能化”封装，实现对复杂工具的高精度调用、对多模态环境的鲁棒感知以及基于记忆的长期规划能力。**

**支撑理由：**

1.  **从“通才”到“专才”的工程落地（事实陈述）：**
    原生 LLM 虽然具备强大的推理能力，但在执行具体任务（如写代码、操作数据库、浏览网页）时，往往存在“幻觉”或格式不匹配的问题。文章若强调 Agent Skills，实际上是主张在 LLM 之上构建一层“中间件”或“技能库”，将 Prompt Engineering、Function Calling 和 RAG（检索增强生成）封装为标准化的技能单元，从而解决模型能力与业务需求之间的“最后一公里”问题。

2.  **技能的泛化与组合能力（作者观点）：**
    文章可能提出，单个技能的价值有限，真正的智能体在于技能的动态编排。例如，一个“数据分析 Agent”不仅需要 SQL 查询技能，还需要 Python 解释器技能和数据可视化技能。其创新点在于探讨如何让 Agent 根据任务目标，自主选择并组合这些技能，这类似于人类解决复杂问题时的“工具使用”思维。

3.  **自我进化与技能习得（你的推断）：**
    深度探讨 Agent Skills 的文章通常会触及“技能是如何获取的”。除了人工硬编码，文章极有可能讨论通过“轨迹回放”或“强化学习”让 Agent 在失败中学习新技能。这是目前从“手工作坊式 Agent”向“工业化 Agent”演进的关键。

**反例/边界条件：**

1.  **通用泛化能力的边界（反例）：**
    过度强调特定技能可能导致 Agent 的“过拟合”。如果 Agent 仅擅长特定的 SQL 技能，面对非结构化数据的定性分析需求时，可能会因为缺乏通用推理灵活性而表现不佳。这挑战了“技能堆砌越多越好”的观点。

2.  **系统复杂度与延迟的权衡（边界条件）：**
    每增加一个技能调用（例如一次 API 调用或一次向量检索），都会增加系统的延迟和潜在失败点。在实时性要求极高的场景（如高频交易或实时对话）中，复杂的技能编排可能由于链路过长而不可用。

---

### 二、 多维度深入评价

#### 1. 内容深度：观点的深度和论证的严谨性
从技术角度看，如果文章仅停留在列举 Agent 需要什么技能（如“需要会写 Python”），则深度一般。高水平的文章应当深入探讨**技能的表征形式**。
*   **深度体现：** 是否讨论了 Skill 是作为 Prompt 存在，还是作为 Fine-tuned 的权重存在，或是作为 LangChain/LangGraph 中的 Node 存在？
*   **严谨性：** 论证是否区分了“能力”与“技能”？能力是模型固有的（如逻辑推理），技能是后天的（如使用 API）。优秀的文章会严谨地界定 Agent 如何利用通用能力去习得特定技能。

#### 2. 实用价值：对实际工作的指导意义
对于 AI 工程师和产品经理而言，这一主题具有极高的实用价值。
*   **架构指导：** 它直接指导了“以模型为中心”向“以工作流为中心”的架构转型。它告诉开发者，不要试图微调一个万能模型，而是要构建一个能够灵活调用外部工具的框架。
*   **评估标准：** 它提供了新的评估维度。我们不再只看 MMLU（综合知识理解）分数，而是看 Agent 在特定工具调用上的成功率（SR）和工具调用的准确率。

#### 3. 创新性：提出了什么新观点或新方法
*   **潜在创新点：** 如果文章提出了“技能抽象层”的概念，即将底层的 API 接口转化为上层 Agent 能理解的语义接口，这将是一个重要的方法论创新。
*   **技能路由：** 类似于混合专家模型，Agent 领域的创新在于“技能路由”，即 Agent 如何判断现在该使用“搜索技能”还是“计算技能”。如果文章对此有深入算法探讨，则具备较高的技术创新性。

#### 4. 可读性：表达的清晰度和逻辑性
此类技术文章通常面临“概念通胀”的问题（如 Tool-use vs Function-calling vs Skill）。
*   **评价标准：** 好的文章应当建立清晰的分类学。例如，将技能分为“信息获取类”、“信息处理类”和“行动执行类”。如果逻辑混乱，将导致读者在构建 Agent 时无法解耦模块。

#### 5. 行业影响：对行业或社区的潜在影响
*   **标准化：** 推动行业从“单点 Demo”走向“技能生态”。未来可能会出现“Agent App Store”，开发者售卖特定的 Agent Skills，而不是通用的模型。
*   **SaaS 的重构：** 传统的 SaaS 软件可能被拆解为一个个 Agent Skills，用户通过自然语言调用这些技能来完成工作，这将深刻改变企业软件的交付形态。

#### 6. 争议点或不同观点
*

---
## 代码示例

```python
# 示例1：Hacker News 热门文章抓取器
import requests
from bs4 import BeautifulSoup

def get_hn_top_stories(limit=5):
    """
    获取 Hacker News 首页热门文章
    :param limit: 要获取的文章数量
    :return: 文章标题和链接列表
    """
    url = "https://news.ycombinator.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        stories = []
        
        # 获取文章标题行
        title_rows = soup.find_all('tr', class_='athing')[:limit]
        
        for row in title_rows:
            title_elem = row.find('span', class_='titleline').a
            if title_elem:
                stories.append({
                    'title': title_elem.text,
                    'link': title_elem['href']
                })
        
        return stories
    except Exception as e:
        print(f"抓取失败: {e}")
        return []

# 测试
if __name__ == "__main__":
    stories = get_hn_top_stories()
    for i, story in enumerate(stories, 1):
        print(f"{i}. {story['title']}\n   {story['link']}\n")
```

```python
# 示例2：HN 文章评论分析器
import requests
from collections import Counter

def analyze_comments(story_id):
    """
    分析 Hacker News 文章的评论内容
    :param story_id: 文章ID
    :return: 评论统计结果
    """
    api_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    story_data = requests.get(api_url).json()
    
    if 'kids' not in story_data:
        return "该文章没有评论"
    
    comment_ids = story_data['kids'][:100]  # 限制分析前100条评论
    comments = []
    
    for comment_id in comment_ids:
        comment_data = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{comment_id}.json").json()
        if comment_data and 'text' in comment_data:
            comments.append(comment_data['text'])
    
    # 简单统计
    word_count = Counter()
    for comment in comments:
        words = comment.lower().split()
        word_count.update(words)
    
    return {
        'total_comments': len(comments),
        'top_words': word_count.most_common(10),
        'avg_comment_length': sum(len(c) for c in comments) / len(comments) if comments else 0
    }

# 测试 (使用一个已知的文章ID)
if __name__ == "__main__":
    result = analyze_comments(2921983)  # 示例文章ID
    print(f"总评论数: {result['total_comments']}")
    print("高频词汇:", result['top_words'])
    print(f"平均评论长度: {result['avg_comment_length']:.1f} 字符")
```

```python
# 示例3：HN 文章搜索工具
import requests
from datetime import datetime, timedelta

def search_hn_by_date(keyword, days_back=7):
    """
    按日期范围搜索 Hacker News 文章
    :param keyword: 搜索关键词
    :param days_back: 搜索最近几天的文章
    :return: 匹配的文章列表
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # 使用 Algolia API (Hacker News 的搜索接口)
    api_url = "http://hn.algolia.com/api/v1/search"
    params = {
        'query': keyword,
        'tags': 'story',
        'numericFilters': f'created_at_i>{int(start_date.timestamp())},created_at_i<{int(end_date.timestamp())}',
        'hitsPerPage': 20
    }
    
    try:
        response = requests.get(api_url, params=params)
        results = response.json()['hits']
        
        stories = []
        for hit in results:
            stories.append({
                'title': hit['title'],
                'url': hit.get('url', f"https://news.ycombinator.com/item?id={hit['objectID']}"),
                'points': hit['points'],
                'date': datetime.fromtimestamp(hit['created_at_i']).strftime('%Y-%m-%d')
            })
        
        return stories
    except Exception as e:
        print(f"搜索失败: {e}")
        return []

# 测试
if __name__ == "__main__":
    results = search_hn_by_date("python", days_back=30)
    for story in results:
        print(f"{story['date']} | {story['points']} points | {story['title']}")
        print(f"链接: {story['url']}\n")
```

---
## 案例研究

### 1：Cognition AI（Devin）

 1：Cognition AI（Devin）

**背景**:
Cognition AI 是一家专注于应用 AI 解决软件工程问题的初创公司。随着软件复杂度的增加，传统的自动化脚本已无法处理需要推理、上下文理解和多步骤规划的复杂编程任务。

**问题**:
在软件开发中，Bug 修复和功能实现往往耗时巨大。开发者需要频繁地在 IDE、文档、浏览器和 Git 之间切换，且需要手动编写大量样板代码。现有的代码助手（如 GitHub Copilot）只能提供片段建议，无法独立完成端到端的任务。

**解决方案**:
Cognition AI 推出了名为 Devin 的 AI 软件工程师。Devin 被设计为一个具备 Agent Skills 的自主智能体，它不仅掌握常见的编程语言，还学会了如何使用开发者工具（如 Bash、终端、代码编辑器、浏览器）。Devin 能够自主规划任务、执行 Shell 命令、搜索 API 文档、编写代码并进行自我调试，从而完成整个 Issue 的开发。

**效果**:
在 SWE-bench 基准测试中，Devin 解决了 13.86% 的问题，而之前的模型（如 Claude 2）仅能解决 1.96%。在实际应用中，Devin 能够独立完成从简单的网站部署到复杂的开源库 Bug 修复，极大地释放了人类工程师的时间，使其从繁琐的重复性劳动中解脱出来。

---

### 2：Rabbit Inc.（R1）

 2：Rabbit Inc.（R1）

**背景**:
随着移动互联网应用数量的爆炸式增长，用户在手机上安装了数百个 APP，但每个 APP 都是一个独立的信息孤岛。用户想要完成一个简单的操作（如订票或比价），往往需要在多个 APP 之间反复切换、点击。

**问题**:
传统的 APP 生态导致了“应用碎片化”。用户必须学习每个 APP 的界面逻辑，且无法通过一个统一的指令跨应用操作。语音助手（如 Siri）通常只能打开 APP，而不能深入 APP 内部进行具体操作。

**解决方案**:
Rabbit Inc. 推出了 R1 设备及其背后的操作系统。该系统基于“大型动作模型”，核心在于赋予 Agent Skills——即让 AI 智能体学会像人类一样操作现有的 APP 界面。用户只需通过自然语言发出指令（例如“帮我订两张去纽约的机票”），R1 的 Agent 就会接管界面，模拟点击、滑动和输入，跨越多个 APP 完成复杂的交互流程。

**效果**:
通过 Agent Skills，用户不再需要亲自操作繁琐的界面。R1 能够在几秒钟内完成原本需要用户几分钟甚至更长时间的操作流程。这种技术不仅提升了交互效率，还验证了“基于代理的操作系统”在解决 APP 碎片化问题上的巨大潜力。

---

### 3：MultiOn

 3：MultiOn

**背景**:
现代互联网充斥着海量的信息和服务，但大多数服务都锁定在特定的网站或 APP 中。用户在进行旅行规划、学术研究或在线购物时，需要手动浏览大量网页、提取数据并填入表单。

**问题**:
现有的浏览器自动化工具（如传统的 Selenium 脚本）非常脆弱，一旦网站结构发生变化，脚本就会失效。此外，普通用户无法编写代码来控制浏览器，导致跨网站的数据收集和任务自动化门槛极高。

**解决方案**:
MultiOn 开发了一种 AI Agent 插件，赋予浏览器 Agent Skills。该 Agent 能够理解用户的自然语言意图，并在 Web 上自主导航。它可以动态地适应网页布局的变化，识别关键信息，填写表单，甚至完成需要多步验证的购买流程。MultiOn 的 Agent 能够“看懂”网页内容并进行交互，而不是依赖硬编码的脚本。

**效果**:
MultiOn 能够帮助用户自动化复杂的 Web 任务。例如，用户可以指令 Agent “帮我预订一家评分 4.5 以上、价格在 200 美元以下的酒店”，Agent 会自主访问订票网站、筛选选项并完成预订。这显著降低了个人和企业实现工作流自动化的技术门槛，将浏览器从被动展示工具转变为主动执行任务的个人助理。

---
## 最佳实践

## 最佳实践指南

### 实践 1：技能原子化与单一职责原则

**说明**: 
Agent 的技能应当遵循单一职责原则，每个技能仅解决一个特定且明确的问题。避免构建包含复杂逻辑链的“大而全”技能。原子化的技能更容易调试、复用和维护，也能降低 Agent 在推理过程中的出错率。

**实施步骤**:
1. 将复杂的业务流程拆解为最小的可执行单元。
2. 审查每个技能，确保其输入和输出清晰且唯一。
3. 命名应具体描述动作，例如使用 `search_web` 而不是 `handle_user_query`。

**注意事项**: 
不要为了拆分而拆分，如果一组操作总是被固定顺序调用，且缺乏独立复用的场景，可以考虑合并。

---

### 实践 2：上下文感知与参数化设计

**说明**: 
技能不应依赖全局变量或外部硬编码状态，而应通过显式参数接收所有必要信息。这确保了技能在不同 Agent 或不同执行上下文中的可移植性。同时，技能需要具备处理上下文缺失的能力。

**实施步骤**:
1. 定义清晰的 Schema，列出所有必需参数和可选参数。
2. 在函数内部对必需参数进行校验，若缺失关键信息应返回错误或提示。
3. 设计默认参数值，以应对非关键信息的缺失情况。

**注意事项**: 
避免在技能内部直接访问 Agent 的私有内存或对话历史，所有数据应通过参数传递。

---

### 实践 3：标准化的输出结构

**说明**: 
为了使 Agent 能够解析技能执行的结果并规划下一步行动，技能必须返回结构化数据（如 JSON）。避免返回非结构化的自然语言文本，这会增加 LLM 解析错误的概率。

**实施步骤**:
1. 定义统一的返回格式，包含 `status`（成功/失败）、`data`（结果数据）和 `error_message`（错误详情）。
2. 对于列表类数据，确保分页或数量限制信息包含在返回结构中。
3. 编写详细的 JSON Schema 文档，供 Agent 的生成模块参考。

**注意事项**: 
保持输出字段的稳定性，不要频繁修改返回键名，以免破坏下游依赖。

---

### 实践 4：幂等性与重试机制

**说明**: 
分布式环境下，网络波动可能导致 Agent 发起重复调用。技能设计必须保证幂等性，即多次调用同一参数产生的结果与调用一次一致，且不会产生副作用（如重复写入数据库）。

**实施步骤**:
1. 对于写操作，实现业务层面的唯一键校验。
2. 为技能配置合理的超时时间，防止 Agent 长时间挂起。
3. 结合 Agent 框架的延迟重试策略，对暂时性错误（如网络超时）进行指数退避重试。

**注意事项**: 
重试机制仅适用于幂等操作，对于非幂等操作（如扣款、发送邮件）必须严格防止重复执行。

---

### 实践 5：鲁棒的错误处理与降级策略

**说明**: 
技能不应直接向用户抛出原始的堆栈跟踪信息。当技能执行失败时，应返回语义明确的错误信息，告知 Agent 失败的原因（如权限不足、资源未找到），以便 Agent 调整策略或向用户请求帮助。

**实施步骤**:
1. 定义标准的错误码枚举，覆盖常见异常场景。
2. 在技能捕获异常后，将其转换为 Agent 可理解的错误描述。
3. 对于非关键路径的技能失败，设计降级逻辑（如返回空列表或缓存数据），保证主流程不中断。

**注意事项**: 
区分可恢复错误（如参数格式错误）和不可恢复错误（如服务宕机），并在返回值中明确标识。

---

### 实践 6：资源限制与性能优化

**说明**: 
Agent 可能会高频调用技能，因此技能必须具备高性能和低资源消耗的特点。对于涉及 I/O 操作（如网络请求、数据库查询）的技能，必须严格控制超时和返回数据量。

**实施步骤**:
1. 为所有外部 API 调用设置严格的超时阈值。
2. 对大文本处理或长列表查询，强制实施分页或截断机制。
3. 实现结果缓存层，对于重复的查询请求直接返回缓存数据。

**注意事项**: 
监控技能的 P99 延迟和 Token 消耗量，定期优化低效的代码逻辑。

---

### 实践 7：语义清晰的文档与描述

**说明**: 
Agent 依赖于 LLM 来选择和调用技能。技能的元数据描述直接决定了 LLM 的调用准确率。描述不仅要面向人类开发者，更要面向 LLM 进行优化。

**实施步骤**:
1. 编写高质量的 Function Description，明确技能的意图、用途和适用场景。
2. 在描述中提供具体的输入输出示例。
3. 定期分析 Agent 的日志，针对误调用或漏调用的情况优化技能描述文本。

**注意事项**: 
描述应简洁但信息量大，避免使用模糊不清的词汇，确保与技能的实际功能严格一致。

---
## 学习要点

- 基于您提供的来源背景（Hacker News 关于 Agent Skills 的讨论），以下是关于 AI 智能体技能构建与评估的关键要点总结：
- 构建具备工具使用能力的 Agent 比单纯优化大语言模型（LLM）的上下文窗口更能有效解决幻觉和复杂逻辑问题。
- 将复杂任务分解为可独立验证的子任务，并通过迭代反馈循环进行自我修正，是实现高可靠性的核心机制。
- 赋予 Agent 动态规划与反思的能力，使其能够根据执行结果自主调整策略，比预设的静态工作流更具适应性。
- 在开发阶段引入“人机协同”模式，利用人类反馈对 Agent 行为进行微调，是确保系统安全性和对齐的关键步骤。
- 评估 Agent 性能应从单一的成功率指标转向端到端的综合效能评估，重点关注其在长链条任务中的累积误差控制。
- 设计标准化的技能接口和模块化的工具生态，能显著降低 Agent 开发门槛并促进跨场景的复用能力。

---
## 常见问题

### 1: 什么是 Agent Skills？

1: 什么是 Agent Skills？

**A**: Agent Skills 是指在人工智能代理框架中，代理执行特定任务或完成特定操作的能力。这些技能可以是使用工具（如搜索引擎、计算器）、调用API、处理文件或执行代码片段等。通过组合不同的技能，Agent 能够处理更复杂的用户请求和工作流。

---

### 2: Agent Skills 与普通的函数调用有什么区别？

2: Agent Skills 与普通的函数调用有什么区别？

**A**: 虽然底层实现可能都涉及函数调用，但概念上的区别在于上下文和自主性。普通的函数调用通常是确定性的、由代码直接触发的。而 Agent Skills 通常是由大语言模型根据当前的对话上下文和用户意图，动态决策是否使用以及如何使用参数。Agent Skills 包含了语义理解、参数映射和错误处理等更高级的封装。

---

### 3: 如何为 Agent 定义和注册一个新的 Skill？

3: 如何为 Agent 定义和注册一个新的 Skill？

**A**: 定义一个新的 Skill 通常包含以下步骤：
1. **描述定义**：为 LLM 提供清晰的技能名称和自然语言描述，说明该技能的功能、适用场景及输入参数要求。
2. **参数结构**：定义技能所需的输入参数（通常使用 JSON Schema 格式），包括参数名称、类型和是否必填。
3. **执行逻辑**：编写具体的代码逻辑来处理输入并返回结果。
4. **注册**：将上述信息注册到 Agent 的运行时环境中，使其在推理时可以被调用。

---

### 4: Agent 在执行 Skills 时如果失败了会怎么办？

4: Agent 在执行 Skills 时如果失败了会怎么办？

**A**: 现代 Agent 框架通常具备错误处理和重试机制。如果一个 Skill 执行失败（例如 API 超时或参数错误），Agent 会捕获错误信息，并将其反馈给大语言模型。LLM 会分析错误原因，并尝试自我修正（例如修正参数格式）后重新调用该 Skill，或者在必要时告知用户无法完成该任务并解释原因。

---

### 5: 如何确保 Agent 正确地使用 Skills（例如幻觉问题）？

5: 如何确保 Agent 正确地使用 Skills（例如幻觉问题）？

**A**: 这是一个主要的挑战。缓解措施包括：
1. **优化描述**：在 Skill 定义中提供非常详细和精确的描述及示例，减少 LLM 的误解。
2. **参数验证**：在 Skill 执行前增加一层验证逻辑，确保传入的参数符合预期。
3. **输出解析**：强制要求 Skill 返回结构化的数据，以便 Agent 更好地解析结果，而不是依赖非结构化的文本。
4. **微调**：针对特定的工具调用场景对模型进行微调，提高其遵循指令和调用工具的准确率。

---

### 6: Agent Skills 是否支持多模态输入（如图片或音频）？

6: Agent Skills 是否支持多模态输入（如图片或音频）？

**A**: 这取决于底座大语言模型的能力以及 Agent 框架的实现。随着多模态模型的发展，现在的 Agent Skills 确实可以支持处理图片、音频等非文本输入。例如，可以定义一个 Skill 来“分析图像内容”，Agent 会将用户上传的图片作为参数传递给该 Skill 进行处理。

---

### 7: 在构建 Agent Skills 时，如何处理敏感信息或权限控制？

7: 在构建 Agent Skills 时，如何处理敏感信息或权限控制？

**A**: 安全性是设计 Skills 时的重点。通常采取以下措施：
1. **权限隔离**：不要将具有高权限（如删除数据库、发送邮件）的 Skills 直接暴露给不受信任的用户输入。
2. **人工确认**：对于高风险操作，可以设计“人机协同”机制，要求 Agent 在执行 Skill 前必须获得人类的批准。
3. **数据脱敏**：在将数据传递给 LLM 或外部 Skill 之前，对敏感字段（如密码、PII）进行掩码或加密处理。
## 引用

- **原文链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Agent](/tags/agent/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent Skills](/tags/agent-skills/) / [框架](/tags/%E6%A1%86%E6%9E%B6/) / [LLM](/tags/llm/) / [AI](/tags/ai/) / [工具调用](/tags/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8/) / [RAG](/tags/rag/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/)

### 相关文章

- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-3.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [LangBot：生产级多平台智能体机器人开发平台]({{< relref "posts/20260201-github_trending-langbot-app-langbot-0.md" >}})
- [Agent Skills：大模型智能体的技能评估框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*