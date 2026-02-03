---
title: "Agent Skills：AI 智能体的技能框架"
date: 2026-02-03T22:14:34+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "智能体", "技能框架", "LLM", "AI 架构", "Agent Skills", "多智能体", "AI 开发"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "在 AI Agent 的开发中，如何让模型精准调用外部工具并执行复杂任务，是当前工程化落地的关键瓶颈。Agent Skills 作为连接大模型与具体业务场景的桥梁，其设计质量直接决定了系统的执行效率与可靠性。本文将梳理 Agent Skills 的核心定义与构建方法，并分享提升工具调用稳定性的实践经验，帮助开发者构建更"
external_url: https://agentskills.io/home
scenarios: ["大语言模型", "AI/ML项目"]
---

# Agent Skills：AI 智能体的技能框架

---

## 基本信息

- **作者**: mooreds
- **评分**: 309
- **评论数**: 182
- **链接**: [https://agentskills.io/home](https://agentskills.io/home)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46871173](https://news.ycombinator.com/item?id=46871173)

---
## 导语

在 AI Agent 的开发中，如何让模型精准调用外部工具并执行复杂任务，是当前工程化落地的关键瓶颈。Agent Skills 作为连接大模型与具体业务场景的桥梁，其设计质量直接决定了系统的执行效率与可靠性。本文将梳理 Agent Skills 的核心定义与构建方法，并分享提升工具调用稳定性的实践经验，帮助开发者构建更健壮的智能体应用。

---
## 评论

### 深度评论：从“全能模型”到“技能编排”——AI Agent 进化的必经之路

#### 一、 核心观点与论证逻辑

**中心论点：**
AI Agent 的技术演进正经历从“依赖大模型通用能力”向“依赖特定技能编排能力”的范式转移。解决大模型幻觉、上下文遗忘及逻辑不可控等核心痛点的关键，不在于无限堆叠参数，而在于构建结构化、可组合的 Agent Skills（技能）体系。

**论证支撑：**
1.  **工程解耦提升确定性：** 大模型本质是概率预测系统，直接处理长链路任务容易产生累积误差。通过将复杂任务拆解为“检索”、“推理”、“执行”等独立技能模块，每个模块可配置专用的 Prompt 或微调模型，从而显著降低单一环节的失败率，将“黑盒”转化为可管理的“白盒”组件。
2.  **突破上下文与成本瓶颈：** 依赖无限长的上下文窗口既昂贵又低效。技能本质上是一种固化的“长时记忆”或“领域知识”。通过技能调用，Agent 可以低成本地复用特定领域的专业知识，避免了每次推理都需要重新灌输背景信息的低效模式。
3.  **满足企业级可控需求：** 在 B 端应用中，业务流程要求可解释、可干预。模块化的技能架构允许人类对关键节点（如“审批”、“支付”）进行监控和接管，这是通用模型无法满足的安全合规要求。

**反面视角与边界：**
*   **过度拆解的风险：** 随着基座模型智商的提升，对于简单任务（如翻译、摘要），过度拆解可能破坏模型的整体直觉，导致效果不如直接调用。
*   **适用性阈值：** 技能化架构主要适用于多步骤、高复杂度的长链路任务。对于单轮、低延迟要求的简单交互，复杂的技能编排可能带来不必要的工程开销和响应延迟。

#### 二、 多维度深入评价

**1. 技术深度：认知架构的范式革命**
该观点深刻触及了 AI 工程化的核心矛盾——通用性与精准性的博弈。它不再将 Agent 视为简单的“聊天机器人 + 插件”，而是将其类比为操作系统，论证了如何通过“认知架构”将感知、记忆、规划封装为具体的 Skill。然而，现有讨论往往低估了技能标准化的难度，例如如何统一不同技能的输入输出接口，这在技术上仍具挑战性。

**2. 实用价值：打通企业落地的“最后一公里”**
强调“Agent Skills”具有极高的落地指导意义。它迫使开发者从“拿着模型找场景”转变为“定义业务能力”。这种视角构建了**可观测、可调试**的系统：当 Agent 出错时，工程师可以精准定位是“检索技能”还是“代码生成技能”的问题，而非盲目调整全局 Prompt，极大地降低了运维成本。

**3. 创新性：AI 领域的“面向对象”思想**
虽然模块化并非新概念，但将其引入 LLM 时代具有里程碑意义。这类似于软件工程从“面向过程”到“面向对象（OOP）”的跃迁。Agent 是对象，Skills 是方法。这一思想推动了 **LangChain、AutoGPT、CrewAI** 等主流框架的发展，并催生了“技能注册表”等新标准，试图建立 AI 时代的 API 协议。

**4. 行业影响：催生“技能经济”生态**
如果这一架构成为主流，未来 AI 行业的商业模式将发生重构。市场可能不再仅仅售卖模型 API，而是涌现出类似 App Store 的**“技能商店”**。开发者将封装特定的垂直能力（如“税务合规审查技能”、“SQL 优化技能”）进行售卖，这将极大地丰富 AI 的应用生态，并加速 SaaS 软件的智能化重构。

---
## 代码示例




```python
# 示例1：获取Hacker News热门文章标题
import requests

def get_hn_top_stories(limit=5):
    """
    获取Hacker News当前热门文章标题
    :param limit: 要获取的文章数量，默认5篇
    :return: 包含标题和链接的字典列表
    """
    # 获取热门文章ID列表
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    story_ids = response.json()[:limit]
    
    stories = []
    for story_id in story_ids:
        # 获取每篇文章的详细信息
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_response = requests.get(story_url)
        story_data = story_response.json()
        
        stories.append({
            "title": story_data.get("title", "无标题"),
            "url": story_data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
            "score": story_data.get("score", 0)
        })
    
    return stories

# 使用示例
if __name__ == "__main__":
    top_stories = get_hn_top_stories()
    for i, story in enumerate(top_stories, 1):
        print(f"{i}. {story['title']} (评分: {story['score']})")
        print(f"   链接: {story['url']}\n")
```




```python
# 示例2：搜索Hacker News文章
import requests

def search_hn_stories(keyword, limit=5):
    """
    在Hacker News中搜索包含特定关键词的文章
    :param keyword: 搜索关键词
    :param limit: 返回结果数量限制
    :return: 匹配的文章列表
    """
    # 使用Algolia API进行搜索
    search_url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": keyword,
        "tags": "story",
        "hitsPerPage": limit
    }
    
    response = requests.get(search_url, params=params)
    results = response.json().get("hits", [])
    
    stories = []
    for result in results:
        stories.append({
            "title": result.get("title", "无标题"),
            "url": result.get("url", f"https://news.ycombinator.com/item?id={result['objectID']}"),
            "author": result.get("author", "匿名"),
            "points": result.get("points", 0)
        })
    
    return stories

# 使用示例
if __name__ == "__main__":
    search_results = search_hn_stories("Python", limit=3)
    for i, story in enumerate(search_results, 1):
        print(f"{i}. {story['title']} (作者: {story['author']}, 评分: {story['points']})")
        print(f"   链接: {story['url']}\n")
```




```python
# 示例3：获取Hacker News评论
import requests

def get_hn_comments(story_id, limit=10):
    """
    获取指定Hacker News文章的评论
    :param story_id: 文章ID
    :param limit: 要获取的评论数量
    :return: 评论列表
    """
    # 获取文章详情（包含评论ID）
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    story_response = requests.get(story_url)
    story_data = story_response.json()
    
    comments = []
    comment_ids = story_data.get("kids", [])[:limit]
    
    for comment_id in comment_ids:
        # 获取每条评论的详细信息
        comment_url = f"https://hacker-news.firebaseio.com/v0/item/{comment_id}.json"
        comment_response = requests.get(comment_url)
        comment_data = comment_response.json()
        
        if comment_data and not comment_data.get("deleted"):
            comments.append({
                "author": comment_data.get("by", "匿名"),
                "text": comment_data.get("text", ""),
                "time": comment_data.get("time", 0)
            })
    
    return comments

# 使用示例
if __name__ == "__main__":
    # 使用示例文章ID（Hacker News首页第一篇文章的ID）
    comments = get_hn_comments(38675228, limit=3)
    for i, comment in enumerate(comments, 1):
        print(f"{i}. {comment['author']} 说:")
        print(f"   {comment['text'][:100]}...")  # 只显示前100个字符
        print()
```


---
## 案例研究


### 1：Cognition AI（Devin 开发团队）

 1：Cognition AI（Devin 开发团队）

**背景**: Cognition AI 致力于构建完全自主的 AI 软件工程师。在开发 Devin（世界上第一个 AI 软件工程师）的过程中，团队面临着一个核心挑战：如何让 LLM 不仅仅是生成代码片段，而是像人类工程师一样处理整个软件开发生命周期（SDLC）。

**问题**: 传统的 LLM 聊天窗口无法胜任复杂的工程任务。当面对一个模糊的 Bug 报告或一个新功能需求时，模型需要具备规划、使用终端、编写代码、运行测试并自我修正的能力。单一的 Prompt 无法维持长时间上下文，也无法处理“尝试-失败-修正”的循环，导致 LLM 在实际工程任务中经常“产生幻觉”或陷入死循环。

**解决方案**: 团队构建了一套基于“Agent Skills”的架构。Devin 被赋予了一系列具体的技能工具，如 Shell Command（终端执行）、Browser（浏览器操作）、Code Editor（文件编辑）和 Planner（任务规划）。关键在于，Devin 能够根据当前的错误状态，自主决定调用哪个特定的 Skill。例如，当测试失败时，它会自动调用“搜索文档”技能查找解决方案，然后调用“编辑代码”技能进行修复，最后调用“运行测试”技能进行验证。这种架构让 AI 拥有了“手”和“眼”，而不仅仅是“脑”。

**效果**: Devin 能够成功完成 Upwork 上的真实外包任务，从简单的网站迁移到复杂的 Bug 修复。在 SWE-bench 基准测试中，它解决了 13.86% 的问题（远超之前模型的 1.96%）。这证明了将 LLM 与具体的 Agent Skills（工具调用能力）结合，可以将 AI 从“聊天机器人”转变为具备实际生产力的“劳动力”。

---



### 2：Rabbit R1（基于 Large Action Model 的个人助理）

 2：Rabbit R1（基于 Large Action Model 的个人助理）

**背景**: 硬件初创公司 Rabbit Inc 推出了 R1 设备，旨在通过 AI 替代用户在手机上繁琐的 App 操作。其核心目标是让用户通过自然语言直接完成服务（如订票、播放音乐），而不是在屏幕上点击多次。

**问题**: 现有的 AI 助手通常依赖特定的 API 集成。如果 Uber 更新了 API，或者某个服务没有开放接口，AI 助手就会失效。此外，基于 API 的方式无法处理复杂的用户界面交互，例如在网站上填写复杂的表单或通过两步验证登录。这导致 AI 能够理解意图，却无法在现有的软件生态中执行操作。

**解决方案**: Rabbit 开发了一种名为“Large Action Model”（LAM）的技术，本质上是一种高级的 Agent Skills 系统。他们不依赖官方 API，而是训练 AI 学习现有 App 的“操作逻辑”。R1 的 Agent Skills 包括“UI 导航”、“元素识别”和“点击逻辑”。当用户说“帮我订一杯咖啡”时，Agent 会激活相应的 Skill，模拟人类在 App 界面上的点击、滑动和输入行为，直接与前端界面交互。

**效果**: Rabbit R1 在发布初期售出 10 万台。用户可以通过语音指令完成在 Spotify 播放音乐、在 Uber 上叫车或在 DoorDash 上点餐，而无需打开手机操作。这展示了 Agent Skills 在“跨应用操作”层面的巨大价值，即 AI 学会了使用人类使用的工具（UI），而不是等待专门为 AI 准备的接口。

---



### 3：Klarna（客服自动化 Agent）

 3：Klarna（客服自动化 Agent）

**背景**: Klarna 是全球领先的支付与购物服务公司，拥有庞大的全球客户群，每天需要处理数以万计的客服咨询，涉及退款、退货、账户管理等重复性任务。

**问题**: 传统的客服机器人（基于关键词或简单意图识别）体验极差，经常无法理解用户意图，只能转接人工，导致人力成本高昂且客户满意度下降。同时，训练大模型处理客服场景存在风险，因为模型可能会胡乱承诺退款政策或给出错误信息。

**解决方案**: Klarna 部署了一个由 OpenAI 技术驱动的 AI 客服 Agent。该 Agent 被集成了特定的“业务技能工具包”。这些 Skills 包括：查询订单状态数据库、读取退货政策文档、执行退款操作接口等。与普通聊天机器人不同，该 Agent 在执行“退款”这个动作时，不是在生成文本，而是严格调用后台的 API Skill。它能够判断用户是否符合退款条件（逻辑判断 Skill），然后执行操作（执行 Skill）。

**效果**: 该 AI Agent 在上线一个月内处理了 230 万次对话（占总量的 2/3），直接相当于 700 名全职客服的工作量。客户解决问题的时效从 11 分钟缩短至 2 分钟，且重复误工率下降了 25%。预计每年将为 Klarna 节省 4000 万美元的成本。这一案例证明了在特定业务流程中，赋予 Agent 明确的“操作权限”和“业务知识技能”比单纯的对话能力更具商业价值。

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确技能边界与单一职责原则

**说明**: Agent Skills（智能体技能）的设计应遵循单一职责原则。每个技能应专注于解决一个特定类型的问题或执行一个明确的任务。避免创建“万能技能”，这会导致模型决策混乱、幻觉增加以及调试困难。清晰的边界有助于 Agent 在规划阶段更准确地选择合适的工具。

**实施步骤**:
1. 对每个技能编写精确的简短描述，定义其输入和输出。
2. 审查现有技能，如果一个技能包含多个不相关的逻辑分支，应将其拆分。
3. 为技能设置严格的参数校验，确保输入符合预期。

**注意事项**: 不要试图在一个技能中处理过多的异常情况，如果任务复杂，应将其拆解为由主控 Agent 调度的子任务。

---

### 实践 2：构建高质量的上下文注入机制

**说明**: 技能的执行效果极大程度上依赖于上下文信息。最佳实践要求在调用技能时，不仅要传递用户指令，还要注入相关的元数据、历史会话摘要或特定的知识库片段。这能减少 Agent 的“幻觉”，提高输出的相关性。

**实施步骤**:
1. 设计标准化的输入模板，包含 `user_query`、`context`、`history` 等字段。
2. 在技能执行前，通过 RAG（检索增强生成）技术检索最相关的文档片段。
3. 限制上下文窗口的长度，只保留最关键的信息以避免干扰模型判断。

**注意事项**: 注意上下文的时效性，确保注入的信息不是过时的。

---

### 实践 3：实现结构化输出与标准化接口

**说明**: 为了让 Agent 能够有效地解析技能执行的结果并将其用于后续步骤，技能必须返回结构化的数据（如 JSON），而非纯文本流。结构化输出便于程序自动处理错误、提取关键信息或进行条件判断。

**实施步骤**:
1. 定义严格的输出 Schema（例如 JSON Schema），包含必需字段和可选字段。
2. 在 Prompt 中明确要求模型按照指定格式输出，并使用 Output Parsing 进行验证。
3. 对于解析失败的输出，实施自动重试或回退机制。

**注意事项**: 输出结构应保持向后兼容，频繁变更接口结构会导致整个 Agent 链路崩溃。

---

### 实践 4：设计原子性与可重试的错误处理

**说明**: 网络波动或外部 API 不可用是常态。技能设计必须具备幂等性和健壮的错误处理机制。当技能执行失败时，应返回明确的错误代码和描述，而不是抛出未捕获的异常，以便 Agent 决定是重试、回滚还是终止任务。

**实施步骤**:
1. 为每个技能定义特定的错误代码（如 `RATE_LIMIT_ERROR`, `INVALID_INPUT`）。
2. 实现指数退避的重试策略，特别是在调用外部 API 时。
3. 记录详细的错误日志，包括触发错误的输入参数堆栈信息。

**注意事项**: 避免无限重试，设置最大重试次数以防止资源耗尽。

---

### 实践 5：基于反馈的持续评估与迭代

**说明**: 技能上线不是开发的终点。必须建立一套评估体系，利用“黄金数据集”或真实用户反馈来监控技能的表现。通过分析失败案例，不断优化 Prompt 或调整底层逻辑。

**实施步骤**:
1. 构建包含边缘案例和常见场景的测试集。
2. 定期运行自动化测试，计算技能的成功率和准确率指标。
3. 建立“坏案例”收集机制，将用户纠正过的输入输出对作为微调数据或 Few-shot 示例。

**注意事项**: 在调整 Prompt 时采用 A/B 测试，确保改动确实提升了性能而非引入了新的问题。

---

### 实践 6：利用 Few-Shot 示例增强指令遵循

**说明**: 对于复杂的技能，仅依靠指令往往难以让模型完全理解意图。在技能的 System Prompt 或用户输入中提供 Few-Shot（少样本）示例，可以显著提高模型对输出格式、风格和逻辑的遵循能力。

**实施步骤**:
1. 收集 3-5 个高质量的典型输入输出对。
2. 将示例嵌入到技能定义的 Prompt 模板中。
3. 动态选择示例，根据用户的查询类型匹配最相似的示例作为参考。

**注意事项**: 示例必须准确且具有代表性，错误的示例会直接误导模型。

---
## 学习要点

- ### 学习要点
- 任务规划与分解**：智能体设计的核心在于将复杂的宏观目标拆解为可执行的原子化子任务，并利用反馈循环不断修正执行路径。
- 工具调用能力**：赋予模型使用外部工具（如联网搜索、代码解释器、文件读写）的能力，是突破大模型知识时效性与能力边界的关键。
- 记忆机制构建**：建立高质量的短期记忆与长期记忆机制，对于解决大模型上下文窗口限制及保持多轮对话连贯性至关重要。
- 思维链与反思**：采用思维链提示或让模型在行动前进行自我反思，能显著降低推理错误率并提升复杂逻辑问题的解决能力。
- 提示词工程**：智能体的有效性往往取决于提示词工程的质量，清晰的角色定义和任务指令是发挥模型性能的基础。
- 人机协作模式**：在生产环境中实施人机协作，让人类在关键决策点进行干预，是平衡自动化效率与安全性的最佳实践。

---
## 常见问题


### 1: 什么是 Agent Skills，它与传统的 AI 提示词有何不同？

1: 什么是 Agent Skills，它与传统的 AI 提示词有何不同？

**A**: Agent Skills（智能体技能）是指 AI 智能体在执行任务时所具备的特定能力或工具。与传统的 AI 提示词不同，Agent Skills 通常不仅仅是基于文本生成的指令，而是结合了外部工具、API 调用、代码执行或结构化的工作流。提示词更多是引导模型生成文本，而 Agent Skills 则允许模型“行动”，例如查询实时数据、操作软件或访问私有数据库。简单来说，提示词是“说话”，而 Agent Skills 是“做事”。

---



### 2: 开发 Agent Skills 时主要的技术挑战是什么？

2: 开发 Agent Skills 时主要的技术挑战是什么？

**A**: 开发 Agent Skills 面临的主要挑战包括上下文管理、工具调用的可靠性以及错误处理。
首先，智能体需要知道何时以及如何调用特定的工具，这需要精确的上下文理解。
其次，工具调用的结果（如 API 返回的错误或非结构化数据）需要被智能体正确解析并整合回对话流中。
最后，处理“幻觉”问题也是一大挑战，即智能体可能会尝试调用不存在的工具或误解工具的参数，导致任务失败。开发者需要通过严格的验证和反馈循环来解决这些问题。

---



### 3: Agent Skills 如何与 RAG（检索增强生成）技术结合使用？

3: Agent Skills 如何与 RAG（检索增强生成）技术结合使用？

**A**: Agent Skills 与 RAG 的结合可以显著提升智能体的专业性和准确性。RAG 技术允许智能体从外部知识库中检索相关信息，作为生成回答的基础。
在这种结合模式下，Agent Skills 负责定义智能体可以执行的动作（如搜索数据库、读取文件），而 RAG 则确保这些动作基于最新的、特定领域的数据。
例如，一个企业客服智能体可以使用“搜索知识库”这一 Skill 来调用 RAG 系统，从而根据公司内部文档回答用户的复杂问题，而不是仅依赖模型预训练的知识。

---



### 4: 如何评估一个 Agent Skill 的性能是否达标？

4: 如何评估一个 Agent Skill 的性能是否达标？

**A**: 评估 Agent Skill 性能通常需要从以下几个维度进行：
1. **成功率**：Skill 在执行任务时是否能在没有人工干预的情况下完成。
2. **准确性**：Skill 返回的结果是否正确，是否解决了用户的意图。
3. **延迟与效率**：执行 Skill 所需的时间是否在可接受范围内，特别是在涉及多步推理或多次 API 调用时。
4. **鲁棒性**：当遇到边缘情况或 API 错误时，Skill 是否能优雅降级或提供有用的反馈，而不是直接崩溃。
开发者通常会建立一套自动化测试集，模拟各种用户输入来验证这些指标。

---



### 5: 在构建 Agent Skills 时，如何确保数据安全和隐私？

5: 在构建 Agent Skills 时，如何确保数据安全和隐私？

**A**: 数据安全是构建 Agent Skills 时的重中之重。首先，必须实施严格的权限控制，确保智能体只能访问其完成任务所需的最小数据范围。
其次，对于涉及敏感操作的 Skills（如发送邮件、修改数据库），应引入“人机协同”机制，即关键操作需要人类审核后才能执行。
此外，所有的 API 通信都应经过加密，并且应避免在提示词或 Skill 的上下文中直接硬编码密钥或敏感信息，使用安全的密钥管理服务（如 AWS Secrets Manager 或 HashiCorp Vault）是最佳实践。

---



### 6: 开源框架（如 LangChain 或 AutoGPT）在构建 Agent Skills 中扮演什么角色？

6: 开源框架（如 LangChain 或 AutoGPT）在构建 Agent Skills 中扮演什么角色？

**A**: 开源框架为构建 Agent Skills 提供了基础设施和标准化的接口。以 LangChain 为例，它提供了丰富的工具抽象，允许开发者轻松地将外部 API 或函数封装成 LLM（大语言模型）可以调用的 Skill。
这些框架通常内置了“代理”逻辑，负责处理 LLM 与工具之间的交互循环，包括解析工具的输入参数、执行工具以及将输出反馈给 LLM。使用这些框架可以大大降低开发门槛，让开发者专注于业务逻辑的实现，而不是从零开始处理复杂的通信协议。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 设计一个 Agent，能够根据用户输入的自然语言描述（例如“帮我查一下今天的天气”），自动调用对应的工具函数（如 `get_weather`）。你需要定义一套简单的工具模式，并实现一个基础的映射逻辑，将用户意图与工具名称进行匹配。

### 提示**: 可以尝试使用关键词匹配作为最基础的实现，或者思考如何定义工具的元数据（如名称、描述），以便 Agent 能够理解每个工具的功能。

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
- 标签： [Agent](/tags/agent/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [技能框架](/tags/%E6%8A%80%E8%83%BD%E6%A1%86%E6%9E%B6/) / [LLM](/tags/llm/) / [AI 架构](/tags/ai-%E6%9E%B6%E6%9E%84/) / [Agent Skills](/tags/agent-skills/) / [多智能体](/tags/%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93/) / [AI 开发](/tags/ai-%E5%BC%80%E5%8F%91/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [压缩智能体：Agent Skills 技术解析]({{< relref "posts/20260130-hacker_news-compressed-agentsmd-agent-skills-8.md" >}})
- [Agent Skills：大模型智能体的技能评估框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-4.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*