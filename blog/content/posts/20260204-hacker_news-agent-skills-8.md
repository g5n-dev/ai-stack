---
title: "Agent Skills：AI 智能体技能框架与训练方法"
date: 2026-02-04T08:42:12+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "智能体", "技能框架", "训练方法", "LLM", "AI Agent", "微调", "强化学习"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大模型应用从单一对话向复杂任务演进，Agent 的“技能”正成为决定其落地效果的关键变量。如何让智能体精准调用工具、处理多步推理，是当前工程化落地中的核心挑战。本文将梳理 Agent Skills 的技术架构与实现路径，帮助开发者理解如何构建具备专业能力的智能体，从而在实际业务中实现更高效的自动化协作。"
external_url: https://agentskills.io/home
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent Skills：AI 智能体技能框架与训练方法

---

## 基本信息

- **作者**: mooreds
- **评分**: 434
- **评论数**: 221
- **链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

---
## 导语

随着大模型应用从单一对话向复杂任务演进，Agent 的“技能”正成为决定其落地效果的关键变量。如何让智能体精准调用工具、处理多步推理，是当前工程化落地中的核心挑战。本文将梳理 Agent Skills 的技术架构与实现路径，帮助开发者理解如何构建具备专业能力的智能体，从而在实际业务中实现更高效的自动化协作。

---
## 评论

### 深度评论

#### 中心观点
文章的核心论点在于，AI智能体的工程化瓶颈已从模型参数规模转向“技能”系统的架构设计。即如何通过结构化的方法，将大模型的通用推理能力转化为解决特定任务的确定性工具，并实现技能的有效组合与泛化。

#### 支撑理由与边界条件

**1. 技能的模块化是任务规划的基础**
*   **事实陈述**：主流Agent框架（如LangGraph、AutoGen）倾向于将Prompt、工具和记忆封装为独立的“Skill”单元。
*   **观点推断**：这种模块化使智能体能够以分而治之的方式处理长链条任务。相比于单体Prompt，技能化设计在处理复合任务时，通过步骤解耦降低了Token消耗和幻觉累积的风险。
*   **边界条件**：然而，对于强推理任务（如数学证明），过度的显式拆分可能会打断思维链的连贯性。OpenAI o1模型表明，在某些场景下，内部的隐式推理比显式的技能调用更有效。

**2. 技能定义需包含决策闭环**
*   **观点**：Agent Skill不应仅定义为简单的API映射，而应包含“感知-决策-行动-反思”的闭环。鲁棒的技能设计必须包含错误处理和自我修正机制。
*   **案例**：一个基础的“搜索”技能若只包含执行动作，在遇到异常数据时会中断；而完善的技能会评估结果质量，并决定是否重试或更换策略。
*   **边界条件**：在低延迟要求的实时系统中（如高频交易辅助），复杂的反思回路会导致响应延迟，此时需在决策深度和响应速度之间做权衡。

**3. 泛化能力依赖元认知机制**
*   **推断**：文章可能强调了技能库的可扩展性。未来的技能不再是硬编码规则，而是通过Few-Shot示例或向量检索动态加载。
*   **行业影响**：这预示着开发重心正从Prompt Engineering转向Skill Engineering，行业需要建立标准化的技能描述协议。
*   **边界条件**：在医疗、法律等高风险领域，过度依赖概率性的泛化能力存在风险，这些领域的技能必须严格绑定在确定性规则或RAG（检索增强生成）之上。

#### 深度评价

**1. 内容深度：从概率生成到确定性执行的转化**
关于Agent Skills的讨论触及了LLM落地的核心难点——如何将概率性的文本生成转化为确定性的函数执行。
*   **论证严谨性**：若文章仅停留在“如何编写Prompt”层面，则深度有限；若能引入ReAct（推理+行动）范式、反思机制或多智能体协作，则具备较高的工程参考价值。
*   **批判性视角**：当前行业存在一种过度设计的倾向，即试图用Agent解决所有问题。实际上，许多业务场景只需要确定性的工作流而非具备自主规划能力的Agent。清晰区分“工作流自动化”与“智能体自主性”是避免架构复杂度过高的关键。

**2. 实用价值：工程化落地的标准化路径**
对于开发者而言，Agent Skills提供了一种必要的抽象层。
*   **指导意义**：它指导开发者采用“分而治之”的策略。例如，将“代码生成”拆分为“需求分析”、“骨架构建”、“函数编写”、“单元测试”四个独立技能，可以显著提升生成结果的通过率和可维护性。
*   **局限性**：目前的技能库管理仍处于早期阶段，缺乏成熟的包管理和依赖注入机制，导致技能复用的成本较高，标准化程度不足。

**3. 创新性：从“工具调用”到“技能编排”**
*   **新观点**：传统观点将Tool视为被动的执行端，而文章强调的“技能编排”则赋予了Agent一定的自主决策权。这种视角的转变推动了开发模式从“硬编码逻辑”向“定义目标与约束”演变。
*   **趋势判断**：随着模型推理能力的提升（如OpenAI o1），未来的技能系统将不再仅仅依赖外部工具调用，而是更多地利用模型内部的“系统2”能力进行隐式思考与显式技能调用的协同。

---
## 代码示例




```python
# 示例1：获取Hacker News热门故事标题
import requests
from bs4 import BeautifulSoup

def get_hn_top_stories(num=5):
    """
    获取Hacker News首页热门故事标题
    :param num: 要获取的故事数量，默认5个
    :return: 包含标题和链接的列表
    """
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}  # 添加请求头避免被拦截
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        soup = BeautifulSoup(response.text, 'html.parser')
        stories = []
        
        # HN的故事标题在span.titleline>a标签中
        for item in soup.select('span.titleline > a')[:num]:
            title = item.get_text()
            link = item['href']
            stories.append({'title': title, 'link': link})
            
        return stories
    
    except Exception as e:
        print(f"获取失败: {e}")
        return []

# 测试
if __name__ == "__main__":
    top_stories = get_hn_top_stories()
    for i, story in enumerate(top_stories, 1):
        print(f"{i}. {story['title']}\n   {story['link']}\n")
```




```python
# 示例2：Hacker News故事搜索功能
import requests

def search_hn_stories(query, num=5):
    """
    使用Hacker Search API搜索故事
    :param query: 搜索关键词
    :param num: 返回结果数量，默认5个
    :return: 匹配的故事列表
    """
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        'query': query,
        'hitsPerPage': num,
        'tags': 'story'  # 只搜索故事类型
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for hit in data['hits']:
            results.append({
                'title': hit['title'],
                'points': hit['points'],
                'url': hit.get('url', 'https://news.ycombinator.com/item?id=' + hit['objectID'])
            })
            
        return results
    
    except Exception as e:
        print(f"搜索失败: {e}")
        return []

# 测试
if __name__ == "__main__":
    results = search_hn_stories("python")
    for i, story in enumerate(results, 1):
        print(f"{i}. {story['title']} ({story['points']} points)\n   {story['url']}\n")
```




```python
# 示例3：Hacker News评论分析
import requests
from collections import Counter
import re

def analyze_hn_comments(story_id):
    """
    分析Hacker News故事的评论
    :param story_id: 故事ID
    :return: 评论统计信息
    """
    url = f"https://hn.algolia.com/api/v1/items/{story_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 提取所有评论文本
        comments = []
        for comment in data.get('children', []):
            if comment.get('text'):
                comments.append(comment['text'])
        
        # 简单的文本分析
        all_text = ' '.join(comments)
        words = re.findall(r'\b\w+\b', all_text.lower())
        top_words = Counter(words).most_common(5)
        
        return {
            'total_comments': len(comments),
            'top_words': top_words,
            'avg_comment_length': sum(len(c.split()) for c in comments) / len(comments) if comments else 0
        }
    
    except Exception as e:
        print(f"分析失败: {e}")
        return {}

# 测试
if __name__ == "__main__":
    # 使用一个已知的故事ID (例如: https://news.ycombinator.com/item?id=35184100)
    analysis = analyze_hn_comments(35184100)
    print(f"总评论数: {analysis['total_comments']}")
    print("高频词:", analysis['top_words'])
    print(f"平均评论长度: {analysis['avg_comment_length']:.1f}词")
```


---
## 案例研究


### 1：Cognition AI 公司的 Devin

 1：Cognition AI 公司的 Devin

**背景**:
Cognition AI 致力于通过 AI 改变软件工程领域。随着 AI 大模型能力的提升，市场上出现了大量能够辅助编写代码片段的工具（如 GitHub Copilot），但在处理端到端的复杂工程任务时，现有工具仍需频繁的人工干预。

**问题**:
传统的 AI 编程助手大多局限于“自动补全”或“聊天生成代码”，无法像真正的工程师一样规划整个项目的架构、自主调试错误、部署应用或学习陌生的技术文档。这导致开发者仍需花费大量时间在琐碎的上下文切换和调试上，无法从重复劳动中彻底解脱。

**解决方案**:
Devin 被设计为世界上第一个完全自主的 AI 软件工程师。它不仅仅是一个代码生成模型，而是一个具备“Agent Skills”的智能体。Devin 被赋予了规划复杂任务、递归调用搜索工具查阅文档、主动编写代码并运行测试、以及在测试失败时自动定位 Bug 并修复代码的能力。它拥有自己的命令行、代码编辑器和浏览器，能够独立完成从需求分析到最终部署的全过程。

**效果**:
在实际演示和测试中，Devin 成功通过了 Upwork 的真实工程测试任务，能够独立完成并部署一个网站。在 SWE-bench 基准测试中，它解决了 13.86% 的问题，远超之前模型 1.96% 的记录。这证明了具备自主规划和工具调用能力的 Agent 能够在真实工作流中承担初级工程师的职责，极大地提升了开发效率。

---



### 2：Rabbit R1 个人助理设备

 2：Rabbit R1 个人助理设备

**背景**:
随着移动互联网应用爆发，用户每天需要在数十个不同的 App 之间切换来完成生活琐事（如订餐、打车、播放音乐）。现有的语音助手（如 Siri 或 Google Assistant）往往只能完成单一指令，无法跨应用执行复杂的“意图”。

**问题**:
用户面临“App 疲劳”，必须手动点击界面进行交互。现有的 AI 助手缺乏对第三方 App 的深度操作能力，只能调用系统级接口，无法模拟人类在 App 内部的点击、滑动和输入操作，导致很多需要多步骤完成的任务无法自动化。

**解决方案**:
Rabbit 开发了基于“Large Action Model”（LAM）的操作系统和 R1 设备。该系统的核心在于赋予 Agent 强大的“UI 导航技能”。Agent 不需要依赖第三方 API 接口，而是通过学习主流 App 的界面交互逻辑，像人类一样通过“看”界面并模拟点击来操作 App。用户只需发出自然语言指令（例如“帮我订一杯去公司的咖啡”），Agent 即可自主规划步骤，打开咖啡 App、选择口味、支付并下单。

**效果**:
Rabbit R1 在 CES 展会上引起了巨大轰动，首发即售罄数万台。其实际价值在于打破了 App 之间的壁垒，用户不再需要下载和打开特定的 App，只需通过 Agent 即可完成跨应用的服务调用。这种基于 UI 交互的 Agent 技能展示了一种无需 API 生态即可实现 AI 自动化的新路径。

---



### 3：UiPath 文档理解自动化

 3：UiPath 文档理解自动化

**背景**:
大型企业和金融机构每天需要处理成千上万份格式各异的文档，如发票、合同、采购订单等。传统的光学字符识别（OCR）技术只能将图像转为文字，无法理解文档的语义和逻辑结构。

**问题**:
传统 RPA（机器人流程自动化）只能处理结构化、固定格式的数据。面对版式复杂、字段位置不固定的非结构化文档，传统方案需要人工编写大量规则，维护成本极高且极易出错，导致业务流程无法完全自动化。

**解决方案**:
UiPath 引入了“Communications Mining”和“Document Understanding”等 AI Agent 技能。这些 Agent 结合了大语言模型（LLM）的语义理解能力和传统 RPA 的执行能力。Agent 能够像人类一样“阅读”文档，理解上下文（例如区分“总价”和“单价”），识别关键信息，并将其提取为结构化数据。随后，Agent 可以直接操作 ERP 或 CRM 系统将这些数据录入。

**效果**:
通过部署具备 AI 技能的 Agent，某大型航空公司实现了发票处理流程的 90% 自动化，处理时间从数天缩短至数分钟。这不仅大幅降低了人工审核的成本，还减少了数据录入的错误率，展示了 Agent 技能在企业数字化转型中处理非结构化数据的巨大价值。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建原子化与可组合的技能单元

**说明**: 
Agent 的技能应当被设计为高内聚、低耦合的原子单元。每个技能应专注于解决一个特定的问题或执行一个明确的任务（例如：仅执行网络搜索、仅解析 HTML 或仅执行代码）。这种设计允许 Agent 在复杂的工作流中灵活地动态组合这些技能，而不是依赖庞大且僵硬的单体函数。

**实施步骤**:
1. 将复杂的业务逻辑拆解为最小的可执行单元。
2. 确保每个技能只接受必要的输入参数，并返回结构化的输出。
3. 建立技能注册机制，允许 Agent 根据上下文动态调用和组合技能。

**注意事项**: 
避免设计“万能技能”。如果一个技能的名称包含“并且”（如“搜索并总结”），通常意味着它需要被进一步拆分。

---

### 实践 2：实施严格的输入输出 Schema 定义

**说明**: 
为了确保 Agent 能够准确地传递参数并理解返回结果，必须为每个技能定义严格的 Schema（如 JSON Schema 或 Pydantic 模型）。明确的类型约束和描述不仅能减少 LLM 产生的幻觉，还能提高工具调用的成功率。

**实施步骤**:
1. 为每个技能的输入参数定义类型、必填项和详细描述。
2. 约定统一的输出数据结构，确保输出是可解析的（如 JSON 对象而非纯文本）。
3. 在技能描述中明确声明输入数据的边界条件（如字符串长度限制或枚举值）。

**注意事项**: 
在 Prompt 中对工具的描述必须与代码中的 Schema 定义严格一致，否则会导致模型调用失败。

---

### 实践 3：设计语义清晰的技能描述

**说明**: 
LLM 依赖于自然语言描述来决定何时调用哪个技能。技能的描述不应仅是函数名的重复，而应详细说明该技能的功能、适用场景以及预期的副作用。高质量的描述能显著减少 Agent 的错误调用。

**实施步骤**:
1. 编写详细的技能文档，包含“何时使用”与“何时不使用”的示例。
2. 在描述中明确技能的能力边界，防止 Agent 在不具备相应能力时强行调用。
3. 使用领域特定的术语来提高检索和匹配的精确度。

**注意事项**: 
描述应保持客观，避免使用营销性语言。描述越长并不总是越好，关键在于信息的密度和准确性。

---

### 实践 4：建立标准化的错误处理与重试机制

**说明**: 
外部工具调用（如 API 请求或代码执行）经常会遇到网络波动或不可预见的错误。Agent 技能层必须具备健壮的错误处理能力，能够区分可重试的错误（如超时）和不可重试的错误（如权限拒绝），并向 Agent 返回有意义的反馈。

**实施步骤**:
1. 为每个技能实现 Try-Catch 包裹层，捕获底层异常。
2. 定义标准化的错误码和错误消息返回格式，以便 LLM 理解发生了什么。
3. 对幂等的操作实施指数退避重试策略。

**注意事项**: 
不要直接将底层堆栈信息返回给 Agent，这可能会干扰模型的推理过程。应将技术错误翻译为自然语言描述。

---

### 实践 5：实现全面的可观测性与日志记录

**说明**: 
Agent 的执行路径具有随机性和非确定性。为了调试和优化技能，必须记录每次技能调用的完整上下文，包括输入参数、输出结果、耗时以及 Token 消耗情况。

**实施步骤**:
1. 在技能执行的关键节点植入日志探针。
2. 记录每一次调用的 Trace ID，以便关联整个 Agent 链路。
3. 建立仪表盘监控技能的成功率、平均响应时间和失败分布。

**注意事项**: 
在记录涉及用户隐私的输入输出时，必须进行脱敏处理，确保数据合规。

---

### 实践 6：优化技能的延迟与性能

**说明**: 
Agent 的思考过程通常包含多轮串行调用，如果单个技能响应缓慢，将导致整个交互体验极差。技能设计必须追求低延迟，对于耗时操作应采用异步处理模式。

**实施步骤**:
1. 对技能进行性能剖析，识别并优化计算密集型或 I/O 密集型瓶颈。
2. 对于长时间运行的任务（如生成大文件），设计异步工作流：立即返回 Job ID，让 Agent 后续轮询结果。
3. 缓存高频调用的静态结果，减少重复计算。

**注意事项**: 
在实现异步模式时，需要确保 Agent 能够理解并正确处理“等待”或“轮询”的逻辑。

---
## 学习要点

- 基于您提供的来源背景（Hacker News 关于 Agent Skills 的讨论），以下是关于构建和评估 AI 智能体能力的关键要点总结：
- 智能体的核心价值在于将复杂的长链任务拆解为可执行的子任务，并具备在执行失败时进行自我纠错和重试的韧性。
- 赋予智能体使用工具（如代码解释器、搜索 API）的能力是突破大模型知识时效性和计算能力限制的关键。
- 在构建工作流时，应优先采用“人机协作”模式，让人类负责关键决策与监督，而将重复性操作交给智能体以提高效率。
- 智能体的短期记忆能力受限于上下文窗口，使用向量数据库或 RAG（检索增强生成）技术是实现长期记忆和知识积累的必要手段。
- 评估智能体性能的最佳方式不是看单次成功率，而是看其在完成整个闭环任务中的总成本和最终效果。
- 提示工程正在向更高级的“规划”技术演进，通过反思和思维链机制能显著提升智能体处理逻辑问题的准确性。

---
## 常见问题


### 1: 什么是 Agent Skills（代理技能）？

1: 什么是 Agent Skills（代理技能）？

**A**: Agent Skills 是指在人工智能代理框架中，赋予 AI 模型执行特定任务或操作的能力。与单纯的语言生成不同，Skills 允许 AI 代理与外部环境进行交互。这些技能通常被定义为具体的函数或工具，例如搜索互联网、查询数据库、执行代码、通过 API 访问其他软件服务等。通过组合不同的 Skills，AI 代理可以从简单的对话机器人转变为能够解决复杂问题的智能助手。

---



### 2: Agent Skills 与传统的 Function Calling 有什么区别？

2: Agent Skills 与传统的 Function Calling 有什么区别？

**A**: 虽然 Agent Skills 和 Function Calling（函数调用）都涉及让模型执行特定的代码逻辑，但概念层级和侧重点不同。Function Calling 通常指模型生成参数以调用特定函数的机制，是底层的接口能力。而 Agent Skills 是更高层的抽象概念，它不仅包含函数调用，还包含了技能的发现、选择、组合以及执行后的结果处理。在 Agent 系统中，Skills 往往是模块化的，代理可以根据任务动态决定使用哪个 Skill，甚至可以将多个 Skills 串联起来使用（例如：先搜索信息，再写入文件）。

---



### 3: 如何为 AI 代理定义和注册一个新的 Skill？

3: 如何为 AI 代理定义和注册一个新的 Skill？

**A**: 定义一个新的 Skill 通常需要包含以下几个关键部分：
1.  **描述与元数据**：清晰地告诉模型这个 Skill 的作用、适用场景以及输入输出格式。
2.  **函数实现**：具体的代码逻辑（如 Python 函数），用于执行实际操作。
3.  **注册机制**：在 Agent 运行时环境中注册该函数，使其成为工具列表的一部分。
在开发中，开发者通常需要编写 Schema（如 JSON Schema）来描述参数，并将这些信息注入到系统的提示词或上下文中，以便大模型理解何时以及如何调用该 Skill。

---



### 4: Agent Skills 的主要应用场景有哪些？

4: Agent Skills 的主要应用场景有哪些？

**A**: Agent Skills 广泛应用于需要 AI 代理自主完成复杂任务的场景，主要包括：
*   **数据分析与研究**：自动编写 SQL 查询数据库、执行 Python 脚本进行数据清洗和可视化。
*   **企业办公自动化**：读取邮件、自动回复、创建日历事件、更新 CRM 系统记录。
*   **互联网交互**：实时搜索新闻、抓取网页内容、总结长文章。
*   **运维与开发**：执行服务器命令、检索代码库、自动运行测试用例。
*   **智能家居控制**：通过 API 控制灯光、温度等家庭设备。

---



### 5: 在 Hacker News 的讨论中，关于 Agent Skills 有哪些技术挑战或关注点？

5: 在 Hacker News 的讨论中，关于 Agent Skills 有哪些技术挑战或关注点？

**A**: 根据 Hacker News 社区的讨论，关于 Agent Skills 的常见关注点包括：
*   **安全性**：赋予 AI 执行代码或修改数据的权限带来了巨大的安全风险，如何进行沙箱隔离和权限控制是核心难点。
*   **幻觉与错误**：模型可能会错误地调用不需要的 Skill，或者传递错误的参数导致执行失败，如何优化 Tool Use 的准确率是研究热点。
*   **上下文限制**：大量的 Skill 描述会占用模型的上下文窗口，如何高效地管理和检索 Skills 是工程上的挑战。
*   **调试困难**：当 Agent 调用多个 Skills 失败时，追踪具体的错误原因比传统编程更复杂。

---



### 6: 未来 Agent Skills 的发展趋势是什么？

6: 未来 Agent Skills 的发展趋势是什么？

**A**: 未来的发展趋势主要集中在以下几个方面：
*   **自主性增强**：从被动等待指令调用，转向代理主动规划和请求所需的 Skills。
*   **多代理协作**：不同的 Agent 拥有不同的专业技能，通过协作解决更宏大的问题。
*   **标准化**：类似于 OpenAPI 或 MCP（Model Context Protocol）等标准的出现，使得 Skills 可以跨平台、跨模型复用。
*   **自学习能力**：代理能够根据执行结果反馈，自动优化其使用 Skills 的策略，甚至通过学习生成新的 Skills。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 编写一个 Agent Skill，能够接收一个 URL 作为输入参数，访问该网页并提取页面的标题和正文文本（去除 HTML 标签）。

### 提示**: 可以使用 Python 的 `requests` 库获取网页内容，并结合 `BeautifulSoup` 来解析 HTML 结构。注意处理网络请求可能出现的超时或非 200 状态码异常。

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
- 标签： [Agent](/tags/agent/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [技能框架](/tags/%E6%8A%80%E8%83%BD%E6%A1%86%E6%9E%B6/) / [训练方法](/tags/%E8%AE%AD%E7%BB%83%E6%96%B9%E6%B3%95/) / [LLM](/tags/llm/) / [AI Agent](/tags/ai-agent/) / [微调](/tags/%E5%BE%AE%E8%B0%83/) / [强化学习](/tags/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent Skills：智能体技能框架与开发指南]({{< relref "posts/20260203-hacker_news-agent-skills-5.md" >}})
- [Agent Skills：AI 智能体的技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-3.md" >}})
- [DynaWeb：基于模型的强化学习网页智能体框架]({{< relref "posts/20260131-arxiv_ai-dynaweb-model-based-reinforcement-learning-of-web--6.md" >}})
- [探索面向智能体的推理奖励模型]({{< relref "posts/20260201-arxiv_ai-exploring-reasoning-reward-model-for-agents-4.md" >}})
- [DynaWeb：基于模型的强化学习网页智能体]({{< relref "posts/20260202-arxiv_ai-dynaweb-model-based-reinforcement-learning-of-web--6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*