---
title: "Agent Skills：大模型智能体的技能评估框架"
date: 2026-02-03T16:31:07+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "LLM", "评估框架", "智能体", "Agent Skills", "Benchmark", "AI 评测", "多模态"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大语言模型能力的演进，Agent 正从简单的对话机器人向能够自主规划、执行复杂任务的智能体转变，而“技能”正是实现这一跨越的核心组件。本文将深入探讨 Agent Skills 的定义、设计模式及其在工具调用中的关键作用，解析如何通过技能封装提升系统的通用性与扩展性。无论你是构建自动化工作流还是优化人机协作体验，这篇"
external_url: https://agentskills.io/home
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent Skills：大模型智能体的技能评估框架

---

## 基本信息

- **作者**: mooreds
- **评分**: 117
- **评论数**: 97
- **链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

---
## 导语

随着大语言模型能力的演进，Agent 正从简单的对话机器人向能够自主规划、执行复杂任务的智能体转变，而“技能”正是实现这一跨越的核心组件。本文将深入探讨 Agent Skills 的定义、设计模式及其在工具调用中的关键作用，解析如何通过技能封装提升系统的通用性与扩展性。无论你是构建自动化工作流还是优化人机协作体验，这篇文章都能为你提供关于构建高效 Agent 架构的实用视角与技术细节。

---
## 评论

**中心观点**
文章《Agent Skills》提出了一种模块化与技能解耦的智能体构建范式，主张通过精细化定义、动态组合与严格验证“原子技能”来构建高可靠性的 AI 智能体，而非依赖单一的大模型端到端能力。

**支撑理由与边界条件**

1.  **复杂系统的可控性需求**
    *   **事实陈述**：随着 Agent 任务复杂度的提升（如从简单的问答转向多步骤的自动化运维），端到端模型的黑盒特性导致错误难以定位和调试。
    *   **支撑理由**：文章主张将 Agent 拆解为独立的技能模块。这种“软件工程化”的思维方式（SOP + 代码执行）能够显著提升系统的可维护性。当某个环节出错时，只需替换或升级特定技能，而无需重新训练整个模型。
    *   **反例/边界条件**：**过度碎片化导致上下文丢失**。如果技能划分过细，Agent 在技能切换时可能会丢失关键的上下文信息，导致任务连贯性下降。此外，对于创意写作或开放式对话这类需要“模糊美感”的任务，机械的技能拼接可能会破坏输出的自然度。

2.  **技能验证与鲁棒性**
    *   **作者观点**：文章强调了“技能验证”的重要性，即每个技能在投入使用前必须经过严格的单元测试。
    *   **支撑理由**：在工业级应用中，确定性比上限更重要。一个能稳定完成 80% 需求但绝不崩溃的 Agent，远优于一个平均分 90% 但偶尔会产出灾难性结果的 Agent。通过沙箱测试和输出校验，可以确保 Agent 在执行高风险操作（如交易、删库）时的安全性。
    *   **反例/边界条件**：**组合爆炸带来的测试难题**。虽然单个技能可能通过了测试，但技能之间的组合交互（Skill A 的输出作为 Skill B 的输入）可能会产生未预期的“涌现效应”。验证所有可能的技能组合路径在计算上可能是不可行的。

3.  **动态规划与工具调用**
    *   **你的推断**：文章暗示了 Agent 应具备根据任务动态选择和编排技能的能力，类似于人类大脑根据不同场景调用肌肉记忆。
    *   **支撑理由**：这解决了模型知识截止和幻觉问题。通过将 RAG（检索增强生成）和 Code Interpreter（代码解释器）封装为标准技能，Agent 可以实时获取准确信息并进行精确计算，弥补了 LLM（大语言模型）在逻辑推理和事实记忆上的短板。
    *   **反例/边界条件**：**路由决策的准确率瓶颈**。系统的整体表现受限于“调度器”的智能程度。如果负责选择技能的模型无法准确理解用户意图，调用错误的技能会导致结果比直接使用端到端模型更差。

**评价维度深入分析**

1.  **内容深度与严谨性**
    文章超越了单纯的 Prompt Engineering 层面，触及了 AI 系统架构的核心。其论证逻辑严密，清晰地界定了“技能”与“模型能力”的边界。然而，文章在“如何自动化构建技能库”方面略显薄弱，更多依赖人工定义，这在面对海量长尾需求时可能存在扩展性瓶颈。

2.  **实用价值**
    对于企业级 AI 应用开发者而言，该文章具有极高的指导意义。它提供了一套从“Demo 玩具”向“生产级工具”转型的标准作业程序（SOP）。特别是关于错误处理和回滚机制的讨论，直接击中了当前 Agent 落地中的痛点。

3.  **创新性**
    虽然模块化思想并非全新（如 LangChain 的 Chain 概念），但文章将“技能”作为一等公民进行原子化管理和验证，是一种视角的微创新。它推动了行业从“大模型万能论”向“大模型作为操作系统内核调度各种专用技能”的认知转变。

4.  **可读性**
    结构清晰，术语使用规范。作者成功地将复杂的系统架构概念通过类比和分层结构表达出来，降低了技术决策者的理解门槛。

5.  **行业影响**
    该观点如果被广泛采纳，将催生新的“技能交易所”或中间件市场。未来，AI 公司可能不再售卖单一的 Agent，而是售卖经过认证的高精度技能包。这将加速 AI 产业链的垂直分工。

6.  **争议点**
    *   **MoE（混合专家）与 Skill-based Agent 的界限**：有观点认为，随着模型越来越大，模型内部自然会形成处理不同任务的“专家”，无需外显的技能拆分。
    *   **硬编码 vs 生成式**：过度依赖预定义的技能可能会限制 Agent 的创造性。真正的 AGI（通用人工智能）应该具备“即兴发挥”的能力，而不是机械地调用函数。

**实际应用建议**

1.  **建立技能分层体系**：将 Agent 的能力分为感知、规划、行动和反馈。优先将“行动”层中高频、高确定性的逻辑（如 SQL 查询、API 调用）封装为原子技能。
2.  **引入金丝雀发布**：在上线新技能或更新技能 Prompt 时，先让小流量用户使用，观察技能的调用成功率和输出质量，避免全量发布导致系统瘫痪。
3.  **监控技能调用链**：建立可观测性工具，记录每次任务调用了哪些技能、耗时多少、输入输出是什么。这是优化 Agent 性能和调试失败案例的关键数据源。

**可验证的检查方式**

1.  **技能复用率指标**：
    *   *指标*：统计平均

---
## 代码示例




```python
# 示例1：获取Hacker News热门新闻标题
import requests
from bs4 import BeautifulSoup

def get_hn_top_stories():
    """
    获取Hacker News首页热门新闻标题和链接
    解决问题：快速获取最新科技资讯，无需手动访问网站
    """
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stories = []
        for item in soup.select('.titleline')[:10]:  # 获取前10条
            title = item.a.text
            link = item.a['href']
            stories.append({'title': title, 'link': link})
            
        return stories
    except Exception as e:
        print(f"Error: {e}")
        return []

# 使用示例
if __name__ == "__main__":
    stories = get_hn_top_stories()
    for i, story in enumerate(stories, 1):
        print(f"{i}. {story['title']}\n   {story['link']}\n")
```




```python
# 示例2：搜索Hacker News历史文章
import requests

def search_hn(query, limit=5):
    """
    使用Hacker Search API搜索历史文章
    解决问题：快速查找特定主题的历史讨论
    """
    url = f"https://hn.algolia.com/api/v1/search"
    params = {'query': query, 'hitsPerPage': limit}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()['hits']
        
        articles = []
        for item in results:
            articles.append({
                'title': item['title'],
                'url': item.get('url', f"https://news.ycombinator.com/item?id={item['objectID']}"),
                'points': item['points'],
                'author': item['author']
            })
        return articles
    except Exception as e:
        print(f"Error: {e}")
        return []

# 使用示例
if __name__ == "__main__":
    results = search_hn("python tutorial")
    for i, article in enumerate(results, 1):
        print(f"{i}. {article['title']} ({article['points']} points)")
        print(f"   By {article['author']}")
        print(f"   {article['url']}\n")
```




```python
# 示例3：监控Hacker News关键词
import time
from datetime import datetime

def monitor_hn_keywords(keywords, interval=300):
    """
    持续监控Hacker News新出现的关键词
    解决问题：自动追踪特定主题的最新讨论
    """
    seen_ids = set()
    
    while True:
        try:
            stories = get_hn_top_stories()  # 使用示例1的函数
            new_matches = []
            
            for story in stories:
                story_id = story['link'].split('=')[-1]
                if story_id not in seen_ids:
                    seen_ids.add(story_id)
                    if any(kw.lower() in story['title'].lower() for kw in keywords):
                        new_matches.append(story)
            
            if new_matches:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 发现 {len(new_matches)} 条新匹配:")
                for story in new_matches:
                    print(f"- {story['title']}\n  {story['link']}\n")
            
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n监控已停止")
            break
        except Exception as e:
            print(f"监控出错: {e}")
            time.sleep(60)

# 使用示例
if __name__ == "__main__":
    print("开始监控关键词: ['python', 'AI', 'machine learning']")
    monitor_hn_keywords(['python', 'AI', 'machine learning'])
```


---
## 案例研究


### 1：Cognition AI (Devin)

 1：Cognition AI (Devin)

**背景**: Cognition AI 是一家致力于通过 AI 改变软件工程方式的初创公司。随着软件复杂度的增加，传统的自动化脚本已无法处理需要推理、上下文理解的长链任务。

**问题**: 传统的 AI 编程助手（如 Copilot）只能提供代码片段补全，无法独立完成一个完整的工程任务（如修复 Bug 或部署应用）。开发者仍需花费大量时间在上下文切换、查阅文档和调试环境上。

**解决方案**: Cognition AI 开发了 Devin，这是一个具备“Agent Skills”的自主 AI 软件工程师。Devin 被赋予了规划复杂任务、使用开发者工具（如终端、代码编辑器、浏览器）以及从错误中学习的能力。它不仅能写代码，还能像人类工程师一样端到端地解决工单。

**效果**: 在实际测试中， Devin 成功通过了 Upwork 的真实工程面试，并完成了包括调试 Django 模型、迁移数据存储以及构建 HTML 游戏在内的多项任务。这标志着 AI Agent 从辅助工具进化为具备独立解决问题能力的虚拟工程师。

---



### 2：Rabbit (R1)

 2：Rabbit (R1)

**背景**: Rabbit 是一家硬件初创公司，致力于解决现代用户在智能手机上面对海量 App 时的操作疲劳问题。

**问题**: 用户在执行简单操作（如订咖啡、叫车或播放音乐）时，往往需要解锁手机、找到特定 App、点击多次按钮。现有的语音助手通常局限于单一生态或只能回答简单问题，无法跨 App 执行复杂操作。

**解决方案**: Rabbit 推出了 R1 设备及其背后的“Large Action Model”（LAM）。该系统通过基于神经网络的 Agent Skills，学习用户在现有 App 上的操作界面和交互逻辑。用户只需发出自然语言指令，Agent 便能通过模拟点击和滑动，代为操控各种 App 服务。

**效果**: R1 在 CES 2024 上引发了广泛关注。通过赋予 Agent 操纵现有 App 的技能，用户无需下载新的插件或等待 API 接口，即可通过语音指令完成复杂的跨应用服务预订，极大地简化了人机交互流程。

---



### 3：Imbue

 3：Imbue

**背景**: Imbue（原 Generally Intelligent）是一家专注于构建具备实用推理能力的 AI 系统的研究型公司，旨在让 AI 能够处理复杂的现实世界问题。

**问题**: 大多数大语言模型（LLM）虽然在对话和写作上表现出色，但在需要多步骤逻辑推理、代码执行和长期规划的任务中表现不佳，难以胜任实质性的“代理”角色。

**解决方案**: Imbue 开发了一套专注于“Agent Skills”的训练架构。他们通过让 AI 在包含代码解释器的沙盒环境中进行强化学习，训练模型具备自我纠错、调试代码以及通过工具调用解决复杂逻辑谜题的能力。

**效果**: Imbue 的模型在 ARC benchmark（一种衡量抽象推理和数据效率的基准测试）中表现优异，甚至在某些任务上超越了参数规模大得多的模型。这证明了通过强化特定的推理和工具使用技能，AI Agent 可以更可靠地完成复杂的现实世界任务。

---
## 最佳实践

## 最佳实践指南

### 实践 1：技能原子化与单一职责原则

**说明**：将 Agent 的能力拆解为最小可执行单元，每个 Skill 应仅负责一个明确的任务。避免创建“全能型”复杂 Skill，以提高复用性和维护性。例如，将“搜索并总结”拆分为“Web搜索”和“文本摘要”两个独立技能。

**实施步骤**:
1. 审视现有功能，识别逻辑边界，将复合操作拆解。
2. 为每个 Skill 定义清晰的输入 Schema 和输出 Schema。
3. 确保单个 Skill 的代码行数或逻辑复杂度保持在可控范围内。

**注意事项**: 拆解粒度并非越细越好，需避免过度拆解导致上下文传递成本过高。

---

### 实践 2：标准化的元数据描述

**说明**：为每个 Skill 提供高质量的元数据，包括名称、描述、输入输出参数定义。这些元数据是 LLM 理解并准确调用该 Skill 的关键依据，直接影响路由规划的准确性。

**实施步骤**:
1. 编写简洁且语义明确的描述文本，说明 Skill 的功能和适用场景。
2. 使用 JSON Schema 或 Pydantic 严格定义参数类型和必填项。
3. 在描述中包含具体的输入输出示例。

**注意事项**: 描述文本应针对 LLM 的理解能力进行优化，避免模糊不清或过于技术化的黑话。

---

### 实践 3：构建鲁棒的错误处理与重试机制

**说明**：外部工具调用往往存在不稳定性。Agent Skills 必须具备优雅的错误处理能力，能够区分可重试错误（如网络超时）和不可重试错误（如参数校验失败），并返回标准化的错误信息给 Agent。

**实施步骤**:
1. 为每个 Skill 定义标准的异常类和错误码。
2. 对非幂等操作实施谨慎的重试策略（如指数退避算法）。
3. 捕获底层异常并向上层返回语义明确的错误描述，而非直接抛出堆栈信息。

**注意事项**: 避免无限重试导致系统资源耗尽，务必设置最大重试次数和超时时间。

---

### 实践 4：实现可观测性与日志记录

**说明**：Agent 的执行路径具有随机性，调试难度大。每个 Skill 必须记录详细的调用日志，包括输入参数、执行耗时、中间结果和最终输出，以便于追踪问题链路。

**实施步骤**:
1. 在 Skill 入口和出口处记录结构化日志。
2. 为每个请求分配唯一的 Trace ID，以便串联多个 Skill 的调用链。
3. 记录关键步骤的时间戳，用于性能瓶颈分析。

**注意事项**: 脱敏处理敏感数据（如 PII、API Key），避免将机密信息直接打印在日志中。

---

### 实践 5：严格的输入验证与安全沙箱

**说明**：Agent 可能会生成不可预测的参数。Skills 不能盲目信任输入，必须在执行前进行严格校验，防止注入攻击或非法操作导致系统崩溃。

**实施步骤**:
1. 使用 Pydantic 或类似库对输入参数进行类型强制检查和格式验证。
2. 对涉及文件系统、数据库或 Shell 的操作实施严格的权限控制。
3. 限制单个 Skill 的资源使用（如 CPU、内存、执行时间）。

**注意事项**: 特别注意处理 Prompt Injection 风格的输入，防止通过 Skill 参数绕过安全限制。

---

### 实践 6：输出结构化与语义一致性

**说明**：Agent 的规划依赖于前序 Skill 的反馈。Skills 的输出应保持格式统一（通常是 JSON 或 Markdown），且包含明确的执行状态字段，以便 LLM 解析。

**实施步骤**:
1. 定义统一的响应基类，包含 `status` (success/failure), `data`, `error_message` 等字段。
2. 确保输出内容经过清洗，去除多余的 HTML 标签或乱码。
3. 对于长文本输出，提供摘要或关键信息提取。

**注意事项**: 避免输出非结构化的自然语言段落，这会增加 LLM 解析错误的风险。

---

### 实践 7：基于语义的版本控制与兼容性管理

**说明**：随着 Agent 的迭代，Skills 会频繁更新。需要建立版本管理策略，确保旧版 Agent 不会因为 Skill 接口变更而失效，同时支持灰度发布新能力。

**实施步骤**:
1. 在 Skill 注册表中包含版本号字段。
2. 修改 Skill 接口时，保持向后兼容，或创建新的 Skill 版本而非直接覆盖。
3. 在元数据中标记 Skill 的稳定性状态（如 Experimental, Stable, Deprecated）。

**注意事项**: 当废弃某个 Skill 时，应保留一段时间的存根逻辑，返回明确的迁移指引。

---
## 学习要点

- 基于您提供的来源背景（Hacker News 关于 Agent Skills 的讨论），以下是关于构建高性能 AI Agent 的关键总结：
- 工具使用能力是 Agent 的核心基础**，Agent 必须能够可靠地调用外部 API、执行代码或访问数据库，以突破模型本身的知识和时效限制。
- 规划与推理能力决定了 Agent 的上限**，通过思维链或 ReAct（推理+行动）模式，Agent 能将复杂任务拆解为可执行的子步骤并处理中间错误。
- 上下文记忆与状态管理至关重要**，Agent 需要具备长期记忆机制来读取历史信息并保持对话状态，从而在多轮交互中维持连贯性。
- 自我纠错与反思机制是可靠性的保障**，顶尖的 Agent 不仅能执行任务，还能在执行失败或结果不理想时自主分析原因并尝试修正。
- 人机协作与监督能有效降低幻觉风险**，在关键决策点引入人工确认，或在不确定时主动寻求人类帮助，是当前落地最稳妥的方案。
- 将复杂流程模块化为微服务架构**，将感知、大脑和行动分离，并针对特定任务（如搜索、解析）训练专用的“技能”组件，比单一端到端模型更有效。

---
## 常见问题


### 1: 什么是 Agent Skills？

1: 什么是 Agent Skills？

**A**: Agent Skills 通常指在人工智能代理框架中，为智能体赋予的特定能力或工具。在 Hacker News 等技术社区的讨论语境下，这通常涉及如何让 LLM（大语言模型）驱动的 Agent 不再仅限于生成文本，而是能够通过调用外部 API、执行代码、使用搜索引擎或操作特定软件来完成复杂任务。简单来说，"Skills" 就是 Agent 解决具体问题所掌握的具体“招式”或“插件”。

---



### 2: Agent Skills 与普通的 Function Calling 有什么区别？

2: Agent Skills 与普通的 Function Calling 有什么区别？

**A**: 虽然 Agent Skills 的底层实现往往依赖于 Function Calling，但两者的侧重点不同。Function Calling 更多是一种技术机制，允许模型将输出转化为结构化的参数以调用函数；而 Agent Skills 是一种更高层的抽象概念。它不仅包含函数调用，还包含了技能的发现、编排、生命周期管理以及上下文记忆。例如，一个 Agent 可能需要动态决定在特定时刻使用“搜索”技能还是“代码执行”技能，并处理技能之间的依赖关系，这属于 Agent Skills 的范畴。

---



### 3: 如何为 Agent 开发或定义一个新的 Skill？

3: 如何为 Agent 开发或定义一个新的 Skill？

**A**: 开发一个新的 Skill 通常包含以下几个步骤：
1. **定义接口与描述**：你需要清晰地定义该 Skill 的功能，并用自然语言（Prompt）描述给 Agent，告诉它何时以及如何使用这个 Skill。
2. **参数标准化**：设定输入和输出的标准格式（通常是 JSON Schema），确保 Agent 能正确生成参数。
3. **实现逻辑**：编写后端代码处理具体的业务逻辑（如连接数据库、调用 API 等）。
4. **测试与迭代**：在沙盒环境中测试 Agent 是否能正确触发该 Skill，并根据结果调整描述或参数限制，以减少幻觉或误用。

---



### 4: Hacker News 上关于 Agent Skills 讨论的热点技术栈有哪些？

4: Hacker News 上关于 Agent Skills 讨论的热点技术栈有哪些？

**A**: 根据近期 Hacker News 的讨论趋势，关于 Agent Skills 的热点主要集中在以下几个方向：
1. **LangChain / LangGraph**：用于构建复杂 Agent 逻辑和工具调用的流行框架。
2. **OpenAI Swarm**：轻量级的多智能体编排框架，强调手部工具和技能的切换。
3. **MCP (Model Context Protocol)**：由 Anthropic 提出的协议，旨在标准化 AI 模型与本地数据/工具之间的连接，使得 Skills 的开发更加通用。
4. **AutoGPT / BabyAGI**：早期探索自主 Agent 和任务分解的经典项目，常被作为技能自主规划的参考。

---



### 5: 在实际应用中，Agent Skills 面临的最大挑战是什么？

5: 在实际应用中，Agent Skills 面临的最大挑战是什么？

**A**: 最大的挑战通常不是“调用”某个工具，而是“选择”和“编排”工具。具体表现为：
1. **幻觉与误用**：Agent 可能会在不需要的时候强行调用某个 Skill，或者传递错误的参数。
2. **上下文窗口限制**：随着 Skills 数量的增加，描述这些 Skills 的 Prompt 会占用大量 Token，甚至超过模型的上下文限制。
3. **错误恢复**：当一个 Skill 执行失败（如 API 超时）时，Agent 往往缺乏有效的重试或回退机制，导致任务直接失败。

---



### 6: Agent Skills 的未来发展方向是什么？

6: Agent Skills 的未来发展方向是什么？

**A**: 业界普遍认为 Agent Skills 正在从“硬编码的工具列表”向“动态学习的技能集”演进。未来的 Agent 可能不再需要开发者手动定义每一个 Skill 的 JSON Schema，而是能够通过阅读文档或观察人类操作，自动学习并掌握新的工具。此外，标准化协议（如 MCP）的推广将使得不同 AI 应用之间的技能互通成为可能，形成一个类似于“App Store”的 Agent Skills 生态系统。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 编写一个简单的 Agent，能够自动访问 Hacker News (https://news.ycombinator.com/) 首页，提取当前排名前 5 的文章标题和对应的链接，并将其格式化为 JSON 字符串输出。

### 提示**: 你需要使用 HTTP 请求工具（如 Python 的 `requests` 或 `httpx`）获取页面内容。Hacker News 的 HTML 结构非常规范，标题通常位于 `<span>` 标签中，且 class 包含 `titleline`。你可以使用 `BeautifulSoup` 或 `lxml` 进行解析。注意处理可能出现的网络超时或非 200 状态码。

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
- 标签： [Agent](/tags/agent/) / [LLM](/tags/llm/) / [评估框架](/tags/%E8%AF%84%E4%BC%B0%E6%A1%86%E6%9E%B6/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent Skills](/tags/agent-skills/) / [Benchmark](/tags/benchmark/) / [AI 评测](/tags/ai-%E8%AF%84%E6%B5%8B/) / [多模态](/tags/%E5%A4%9A%E6%A8%A1%E6%80%81/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [Compressed Agents：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-6.md" >}})
- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-8.md" >}})
- [2026年AI展望：LLM、智能体、缩放定律与中国发展]({{< relref "posts/20260201-blogs_podcasts-490-state-of-ai-in-2026-llms-coding-scaling-laws-c-0.md" >}})
- [AI 基准测试新进展：Game Arena 推进评估方法]({{< relref "posts/20260203-hacker_news-advancing-ai-benchmarking-with-game-arena-14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*