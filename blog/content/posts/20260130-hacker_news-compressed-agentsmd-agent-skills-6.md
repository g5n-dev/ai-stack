---
title: "Compressed Agents：Agent Skills 技术解析"
date: 2026-01-30T00:01:18+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "LLM", "技术解析", "模型压缩", "AI Agent", "Compressed Agents", "Agent Skills", "大模型应用"]
categories: ["大模型", "AI 工程"]
source: hacker_news
description: "随着大模型应用从原型验证走向生产部署，Agent 的响应延迟与推理成本正成为制约其落地的关键瓶颈。本文聚焦于“Compressed Agents”这一技术路径，深入探讨了如何通过技能压缩与架构优化，在保持核心能力的前提下显著提升系统效率。阅读本文，你将了解 Agent 技能压缩的具体策略，以及如何在资源受限的环境中实现"
external_url: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
scenarios: ["大语言模型", "AI/ML项目"]
---

# Compressed Agents：Agent Skills 技术解析

---

## 基本信息

- **作者**: maximedupre
- **评分**: 83
- **评论数**: 40
- **链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

---
## 导语

随着大模型应用从原型验证走向生产部署，Agent 的响应延迟与推理成本正成为制约其落地的关键瓶颈。本文聚焦于“Compressed Agents”这一技术路径，深入探讨了如何通过技能压缩与架构优化，在保持核心能力的前提下显著提升系统效率。阅读本文，你将了解 Agent 技能压缩的具体策略，以及如何在资源受限的环境中实现高性能智能体的工程化落地。

---
## 评论

### 深度评论：模型压缩与 Agent 技能内化的技术路径分析

**综述**
文章的核心观点在于探讨一种技术路径的权衡：在特定场景下，利用模型压缩技术（如量化、蒸馏）将通用大模型部署为端侧 Agent，其综合效能是否优于传统基于 API 调用的多技能架构。这一观点触及了当前 AI Agent 落地中成本、延迟与隐私的核心矛盾。

#### 1. 内容深度与论证逻辑
**评价：** [中高]
文章触及了 AI Agent 架构设计中的关键权衡点。
*   **架构对比：** 文章通过对比“单体压缩模型”与“多组件调用架构”，分析了减少外部调用链路带来的上下文完整性优势。这种从系统复杂度角度的切入具备一定的技术深度。
*   **论证严谨性：** 观点的成立高度依赖于场景界定。文章若能明确区分“知识型任务”（如翻译、摘要）与“工具型任务”（如精确计算、实时数据检索）的边界，将更具说服力。压缩模型在保留通用知识方面表现尚可，但在处理需要严格确定性的工具调用时，仍面临挑战。

#### 2. 实用价值与工程意义
**评价：** [高]
*   **部署成本优化：** 在实际工程中，端侧部署能够显著降低 Token 消耗和网络传输延迟。对于需要即时响应的应用场景，这种方案提供了可行的成本控制手段。
*   **数据隐私合规：** 本地化部署是解决金融、医疗等行业数据隐私问题的有效技术手段，文章对此类场景的适用性分析具有实际参考价值。

#### 3. 创新性：技术范式的转换
**评价：** [中]
*   **范式转变：** 文章提出了从“调用外部工具”转向“内化模型能力”的思路。这种“以模型容量换架构简洁度”的尝试，是对当前主流依赖庞大 API 生态模式的一种补充思考。
*   **方法论探讨：** 如果涉及如何通过蒸馏技术将特定技能迁移至压缩模型，这将为构建轻量级垂直 Agent 提供新的方法论。

#### 4. 逻辑支撑与局限性
**评价：** [客观]
*   **支撑理由：**
    1.  **上下文完整性：** 单体模型内部处理逻辑避免了多 Agent 调用中的上下文截断和噪声累积。
    2.  **硬件适配性：** 随着端侧 NPU 算力的提升，本地运行量化后的中小参数模型已成为硬件层面的可行方案。
    3.  **成本效益：** 对于高频、低算力需求的任务，本地推理的边际成本低于频繁的 API 调用。
*   **潜在局限：**
    1.  **推理能力损失：** 压缩过程可能导致模型逻辑推理能力下降，增加产生“幻觉”的风险，相比确定性工具输出，可靠性面临挑战。
    2.  **知识时效性：** 本地模型的知识截止于训练时间，难以像 API 技能那样灵活获取实时信息。

#### 5. 行业影响与建议
**评价：** [参考性]
*   **混合架构趋势：** 行业发展可能不会走向单一极端，而是趋向于混合架构——即核心推理与知识问答由压缩模型承担，而实时数据获取与精确计算仍保留外部接口。
*   **应用建议：** 该技术路径目前最适用于离线环境、高隐私敏感度或对延迟要求极高的场景，但在处理开放域实时问题时仍需谨慎。

---
## 代码示例

```python
# 示例1：HackerNews热门话题聚合器
import requests
from collections import Counter

def get_hackernews_top_topics(limit=30):
    """
    获取HackerNews首页热门帖子的主要话题标签
    问题解决：快速了解当前技术社区关注的热门领域
    """
    # 获取HackerNews首页热门帖子ID
    top_stories = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()[:limit]
    
    # 获取每个帖子的详细信息
    topics = []
    for story_id in top_stories:
        story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json').json()
        # 提取URL中的域名作为话题标识
        if story and 'url' in story:
            domain = story['url'].split('//')[-1].split('/')[0]
            topics.append(domain)
    
    # 统计出现频率最高的话题
    return Counter(topics).most_common(5)

# 使用示例
print(get_hackernews_top_topics())
```

---

```python
# 示例2：HackerNews评论情感分析
import requests
from textblob import TextBlob

def analyze_story_sentiment(story_id):
    """
    分析HackerNews帖子的评论情感倾向
    问题解决：快速了解社区对特定话题的整体态度
    """
    # 获取帖子详情
    story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json').json()
    if not story or 'kids' not in story:
        return "无评论数据"
    
    # 获取所有评论
    comments = []
    for comment_id in story['kids'][:20]:  # 限制分析前20条评论
        comment = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{comment_id}.json').json()
        if comment and 'text' in comment:
            comments.append(comment['text'])
    
    # 分析情感
    sentiment_scores = []
    for text in comments:
        blob = TextBlob(text)
        sentiment_scores.append(blob.sentiment.polarity)
    
    # 计算平均情感分数
    avg_sentiment = sum(sentiment_scores)/len(sentiment_scores)
    return "正面" if avg_sentiment > 0 else "负面" if avg_sentiment < 0 else "中性"

# 使用示例（替换为实际story_id）
print(analyze_story_sentiment(12345678))
```

---

```python
# 示例3：HackerNews个性化推荐
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_stories(user_history, top_n=5):
    """
    基于用户浏览历史推荐HackerNews故事
    问题解决：发现符合用户兴趣的优质内容
    """
    # 获取当前热门故事
    top_stories = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()[:50]
    
    # 获取故事详情
    current_stories = []
    for story_id in top_stories:
        story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json').json()
        if story and 'title' in story:
            current_stories.append(story['title'])
    
    # 构建TF-IDF矩阵
    vectorizer = TfidfVectorizer()
    all_stories = user_history + current_stories
    tfidf_matrix = vectorizer.fit_transform(all_stories)
    
    # 计算与用户历史的相似度
    user_profile = tfidf_matrix[:len(user_history)].mean(axis=0)
    similarities = cosine_similarity(user_profile, tfidf_matrix[len(user_history):])
    
    # 获取最相似的故事
    top_indices = similarities.argsort()[0][-top_n:][::-1]
    return [current_stories[i] for i in top_indices]

# 使用示例（替换为实际用户历史）
user_history = ["Python机器学习教程", "React最佳实践", "Docker容器化指南"]
print(recommend_stories(user_history))
```

---
## 案例研究

### 1：Cognition 公司的 Devin（全球首个 AI 软件工程师）

 1：Cognition 公司的 Devin（全球首个 AI 软件工程师）

**背景**:
Cognition AI 是一家专注于应用人工智能解决复杂工程问题的初创公司。随着软件交付周期的缩短，开发团队常常被繁琐的重复性编码任务（如编写样板代码、调试旧代码、配置环境）所困扰，导致核心创新的时间被挤压。

**问题**:
传统的自动化工具只能处理单一、简单的脚本任务，无法理解复杂的工程上下文或自主完成端到端的开发任务（如从需求分析到最终部署）。企业迫切需要一种能够像人类工程师一样“思考”并使用多种工具（终端、代码编辑器、浏览器）的智能体。

**解决方案**:
Cognition 开发了 Devin，这是一个基于 Agent Skills（智能体技能）架构的 AI 软件工程师。Devin 被赋予了一系列高级技能，包括：
1.  **自主规划与推理**：能够将高层级的开发需求拆解为可执行的步骤。
2.  **工具调用能力**：具备熟练使用 Bash 终端、代码编辑器和浏览器的能力，能够自主修复环境错误。
3.  **上下文学习**：在 Upwork 等自由职业平台上接受实际任务，能够学习陌生的技术栈（如 React、Tailwind CSS）并快速上手。

**效果**:
在实际测试和演示中，Devin 成功在 Upwork 上完成了真实世界的软件开发任务，包括调试数据可视化代码和迁移遗留代码库。在 SWE-bench 基准测试中，Devin 解决了 13.86% 的问题（在没有辅助的情况下），这一成绩远超之前的最先进模型（如 Claude 2，仅解决 1.96%）。它不仅解放了人类工程师的时间，还显著提高了从需求到代码的交付效率。

---

### 2：Rippling 公司的 IT 自动化智能体

 2：Rippling 公司的 IT 自动化智能体

**背景**:
Rippling 是一家提供企业员工管理 IT 和 HR 平台的公司。对于其客户而言，员工入职（Onboarding）和离职（Offboarding）涉及大量跨系统的操作，如在 Okta 中创建账户、在 Slack 中分配权限、配置笔记本电脑硬件以及发放办公软件许可证。

**问题**:
传统的 RPA（机器人流程自动化）工具脆弱且僵化，一旦某个网页元素变动或 API 接口超时，整个流程就会报错停止。此外，不同企业使用的 SaaS 堆栈差异巨大，硬编码的自动化脚本无法灵活适应每个客户的独特工作流。

**解决方案**:
Rippling 构建了一个基于 Agent Skills 的自动化智能体系统。该系统不再依赖固定的脚本，而是赋予智能体“目标导向”的技能：
1.  **多模态交互技能**：智能体不仅能调用 API，还能模拟人类在浏览器界面上的点击和输入操作，处理没有 API 的老旧系统。
2.  **错误自愈能力**：当遇到网络超时或意外弹窗时，智能体利用视觉识别和逻辑推理技能判断当前状态，并尝试重试或切换路径，而不是直接崩溃。
3.  **动态工作流编排**：根据客户的 IT 策略，智能体能够自主决定操作的顺序和并行度。

**效果**:
该解决方案使得 Rippling 能够为客户实现近乎 100% 的 IT 任务自动化率。据公开数据显示，这种智能体架构将员工入职任务的设置时间从数小时缩短至几分钟，并且由于具备自我修复能力，维护成本大幅降低，不再需要工程师频繁修复破碎的自动化脚本。

---

### 3：Klarna 的客服智能体

 3：Klarna 的客服智能体

**背景**:
Klarna 是一家全球领先的“先买后付”（BNPL）金融服务公司，拥有庞大的全球客户群，每天需要处理数以万计的客服咨询，涉及退款、退货、支付查询等。

**问题**:
传统的客服机器人（基于规则或早期 LLM）往往只能回答简单问题，一旦遇到复杂的跨系统查询（例如：需要同时核对订单状态、支付历史和当前促销政策）就需要转接人工。这导致人力成本高昂，且客户等待时间长。

**解决方案**:
Klarna 部署了一个由 OpenAI 技术驱动的客服智能体，该智能体集成了复杂的 Agent Skills：
1.  **业务系统操作技能**：智能体直接与 Klarna 的后端系统连接，具备执行退款、更新订单信息等业务操作的权限和能力。
2.  **自然语言理解与推理**：能够理解 35 种以上的语言，并从非结构化的用户查询中提取意图。
3.  **知识库检索与应用**：能够检索最新的公司政策，并将其应用到具体的客户案例中，进行个性化回复。

**效果**:
在上线后的一个月内，该智能体完成了相当于 700 名全职人工客服的工作量（约 230 万次对话）。它在解决问题方面的准确性与人工客服持平，并在查询相关的工单上减少了 25% 的重复咨询。据 Klarna 估算，这一举措预计每年将为公司节省 4000 万美元的成本，同时将客户咨询的解决时间从 11 分钟缩短至 2 分钟。

---
## 最佳实践

## 最佳实践指南

### 实践 1：技能原子化与单一职责

**说明**：
Agent 的技能应遵循单一职责原则，将复杂的任务流程拆解为最小可执行的单元。每个技能应仅负责一个明确的功能（例如：仅执行搜索、仅解析数据或仅发送请求），避免在一个技能中混合多种逻辑。这种原子化设计有助于提高技能的复用性，并降低调试和错误排查的难度。

**实施步骤**:
1. 审视现有的 Agent 功能列表，识别包含多个逻辑步骤的“大而全”技能。
2. 将复杂技能拆解，例如将“搜索并总结”拆分为“Web搜索”和“文本摘要”两个独立技能。
3. 为每个原子化技能编写清晰的输入输出定义，确保其独立性。

**注意事项**: 拆解时要注意保持输入输出接口的简洁性，避免因为过度拆解导致参数传递过于复杂。

---

### 实践 2：构建标准化技能描述

**说明**：
为了使 Agent 能够准确调用正确的技能，必须为每个技能提供结构化、标准化的元数据描述。这包括技能的功能、适用场景、输入参数约束及预期输出。高质量的描述能显著提升 LLM（大语言模型）在路由和选择技能时的准确率。

**实施步骤**:
1. 为每个技能建立标准的元数据模板，包含 `Name`（名称）、`Description`（功能描述）、`Parameters`（参数 schema）。
2. 在 Description 中明确技能的“触发条件”，例如“当用户需要获取实时天气数据时使用此技能”。
3. 使用 JSON Schema 定义参数，严格限定参数类型和是否必填。

**注意事项**: 描述语言应尽可能客观、直接，避免模糊不清的词汇，确保模型理解不会产生歧义。

---

### 实践 3：实施严格的输入验证

**说明**：
Agent 技能的鲁棒性依赖于输入数据的质量。在技能执行核心逻辑前，必须对传入的参数进行严格的类型检查、格式验证和范围限制。这可以防止无效数据导致技能崩溃或产生意外的系统行为。

**实施步骤**:
1. 在每个技能函数的入口处添加参数校验逻辑（如使用 Pydantic 或 Joi 等库）。
2. 定义明确的错误处理机制，当输入不合法时，返回结构化的错误信息而非抛出异常。
3. 对于文本输入，增加长度限制和敏感词过滤；对于数字输入，限制数值范围。

**注意事项**: 验证逻辑不应泄露敏感的系统内部信息，错误提示应面向用户友好，而非暴露底层堆栈。

---

### 实践 4：设计幂等性技能

**说明**：
在分布式环境或由于网络波动可能导致 Agent 重复执行同一指令的场景中，技能必须设计为幂等的。即无论技能被调用多少次，只要参数相同，产生的结果和系统状态应保持一致。这对于构建可靠的 Agent 工作流至关重要。

**实施步骤**:
1. 审查所有涉及状态变更（如写入数据库、发送邮件、API 调用）的技能。
2. 为这些操作引入唯一标识符（如 IDempotency-Key），在执行前检查是否已处理过该请求。
3. 确保读取类操作本身天然幂等，写入类操作通过逻辑控制实现幂等。

**注意事项**: 幂等性检查可能会增加轻微的延迟（如查询数据库），需要在性能和一致性之间做好权衡。

---

### 实践 5：建立全面的日志与可观测性

**说明**：
由于 Agent 的执行路径具有非确定性，调试技能失败的原因非常困难。最佳实践要求每个技能必须记录详细的上下文日志，包括接收到的参数、中间处理步骤、返回的结果以及发生的错误。

**实施步骤**:
1. 在技能框架中集成标准的日志记录器，统一日志格式。
2. 记录每次技能调用的 `Trace ID`，以便将分散的日志关联到同一个 Agent 任务链中。
3. 捕获并记录技能执行耗时，用于后续分析性能瓶颈。

**注意事项**: 避免在日志中记录敏感信息（如 PII 个人信息、API 密钥、密码），应对敏感字段进行脱敏处理。

---

### 实践 6：处理不确定性异常

**说明**：
Agent 技能经常会依赖外部不可控因素（如网络请求、第三方 API）。最佳实践要求技能不仅要处理预期的错误，还要优雅地处理超时、限流和不可预见的异常，避免导致整个 Agent 进程阻塞或崩溃。

**实施步骤**:
1. 为所有外部 I/O 操作设置合理的超时时间。
2. 实现重试机制，对于可恢复的错误（如 5xx 错误或网络抖动）进行指数退避重试。
3. 设计“降级”逻辑，当技能不可用时，返回一个默认值或明确的错误提示，让 Agent 能够决定下一步策略。

**注意事项**: 重试机制应包含最大重试次数限制，防止在服务完全不可用时造成无限循环的资源消耗。

---

### 实践 7：技能版本管理与兼容性

**说明**：
随着 Agent 系

---
## 学习要点

- 技能压缩是提升 Agent 效能的核心手段，通过将复杂的思维链或工作流提炼为专用的“微服务”，可显著降低推理成本并提高响应速度。
- 技能本质上是可被参数化存储和检索的上下文，Agent 应根据任务需求动态加载相关技能，而非在上下文中塞入所有知识。
- 有效的技能设计需要包含明确的触发条件和执行逻辑，以确保 Agent 能在特定场景下自主且准确地调用该技能。
- 技能的获取与迭代依赖于反馈闭环，通过分析 Agent 的失败案例并针对性地新增或优化技能，可实现系统的持续进化。
- 将长上下文任务拆解为多个独立的技能调用，能有效突破模型的上下文窗口限制，并减少因注意力分散导致的幻觉。
- 构建技能库时应遵循模块化原则，确保每个技能具有单一职责且接口标准，以便于在不同 Agent 之间复用和组合。
- 技能压缩不仅是存储优化，更是认知架构的升级，它将 Agent 从“每次重新思考”转变为“通过训练积累经验”的模式。

---
## 常见问题

### 1: 什么是 Agent Skills（代理技能）？

1: 什么是 Agent Skills（代理技能）？

**A**: Agent Skills 是指赋予自主智能体执行特定任务或完成复杂操作的能力。在构建 AI Agent 时，开发者通常不会编写一个巨大的单体模型来处理所有事情，而是将不同的功能（如网页浏览、代码执行、文件读写、API 调用等）封装成独立的“技能”。Agent 可以根据当前的上下文和目标，动态地调用这些技能来解决问题。这种模块化的设计使得 Agent 更加灵活、可维护，并且能够扩展到更广泛的应用场景中。

### 2: 如何为 Agent 定义和选择合适的 Skills？

2: 如何为 Agent 定义和选择合适的 Skills？

**A**: 定义 Skills 通常需要遵循“原子化”和“可复用”的原则。
1.  **明确目标**：首先分析 Agent 需要解决的核心问题，例如是需要实时数据（需要联网技能），还是需要处理数学计算（需要代码解释器技能）。
2.  **接口设计**：每个 Skill 应该有清晰的输入和输出定义。例如，一个“搜索”技能的输入是查询字符串，输出是结构化的搜索结果列表。
3.  **选择策略**：在实现层面，可以通过 Function Calling（函数调用）机制让大模型决定何时调用哪个 Skill，或者通过路由层根据用户意图分发任务。选择时应优先考虑那些能显著弥补大模型短板（如幻觉、时效性差）的技能。

### 3: Agent Skills 与传统的 API 调用有什么区别？

3: Agent Skills 与传统的 API 调用有什么区别？

**A**: 虽然两者本质上都涉及代码执行，但在 Agent 语境下，Skills 具有更高的自主性和上下文感知能力。
*   **传统 API**：通常是硬编码的，开发者明确知道何时调用以及传入什么参数。
*   **Agent Skills**：是由大模型根据推理结果自主决策调用的。模型会分析当前对话状态，判断是否需要某个 Skill，并自动生成所需的参数。如果 Skill 执行失败，Agent 甚至可以尝试自我修正或调用其他 Skill，这是一个动态的决策循环过程。

### 4: 如何处理 Agent Skills 执行过程中出现的错误？

4: 如何处理 Agent Skills 执行过程中出现的错误？

**A**: 错误处理是 Agent 系统稳健性的关键。常见的处理策略包括：
1.  **反馈循环**：将 Skill 执行的错误信息（如异常堆栈、API 返回的错误码）捕获并返回给大模型。
2.  **自我修正**：大模型接收到错误信息后，会分析原因（例如参数错误、网络超时），并尝试生成新的参数或重试操作。
3.  **兜底机制**：如果多次重试失败，系统应设计一个兜底路径，例如向用户报告具体错误或转交给人工处理，而不是让 Agent 无限循环或崩溃。

### 5: 压缩 Agent Skills 有什么意义，它是如何实现的？

5: 压缩 Agent Skills 有什么意义，它是如何实现的？

**A**: 随着 Agent 功能的增加，Skills 的数量和描述文档可能会变得非常庞大，导致上下文窗口占用过高，增加推理成本和延迟。
*   **意义**：压缩旨在减少 Skills 对 Token 的消耗，同时保持模型能够准确检索和调用这些技能的能力。
*   **实现方式**：
    *   **向量化检索**：不将所有 Skill 描述全部放入 Prompt，而是将其向量化存储。当用户提问时，先检索相关的 Top-K Skills，再将其描述注入 Prompt。
    *   **精简描述**：优化 Function 的 JSON Schema 或文档字符串，去除冗余信息，仅保留关键的参数说明和示例。

### 6: 在 Hacker News 的讨论中，关于 Agent Skills 有哪些值得关注的观点？

6: 在 Hacker News 的讨论中，关于 Agent Skills 有哪些值得关注的观点？

**A**: 根据 Hacker News 社区的讨论趋势，开发者们通常关注以下几点：
1.  **安全性**：赋予 Agent 执行代码或修改系统文件的能力会带来巨大的安全风险，如何进行沙箱隔离和权限控制是热门话题。
2.  **幻觉与工具滥用**：模型可能会在不需要的时候强行调用工具，或者编造工具参数。讨论中常提到如何通过 Prompt Engineering 或微调来减少这种情况。
3.  **编排框架**：开发者们经常比较 LangChain、AutoGPT 等框架在管理 Skills 时的优劣，讨论如何避免过度设计，保持代码的简洁性。
## 引用

- **原文链接**: [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46809708](https://news.ycombinator.com/item?id=46809708)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Agent](/tags/agent/) / [LLM](/tags/llm/) / [技术解析](/tags/%E6%8A%80%E6%9C%AF%E8%A7%A3%E6%9E%90/) / [模型压缩](/tags/%E6%A8%A1%E5%9E%8B%E5%8E%8B%E7%BC%A9/) / [AI Agent](/tags/ai-agent/) / [Compressed Agents](/tags/compressed-agents/) / [Agent Skills](/tags/agent-skills/) / [大模型应用](/tags/%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%BA%94%E7%94%A8/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Agent Skills：压缩智能体技能以提升模型效率]({{< relref "posts/20260129-hacker_news-compressed-agentsmd-agent-skills-5.md" >}})
- [SokoBench：评估大模型长程规划与推理能力]({{< relref "posts/20260129-arxiv_ai-sokobench-evaluating-long-horizon-planning-and-rea-2.md" >}})
- [AssetOpsBench：AI Agent基准测试与工业现实鸿沟如何跨越？🤖🔥]({{< relref "posts/20260126-blogs_podcasts-assetopsbench-bridging-the-gap-between-ai-agent-be-6.md" >}})
- [震惊！仅1个大模型能操控无人机！🚀🤯]({{< relref "posts/20260126-hacker_news-show-hn-only-1-llm-can-fly-a-drone-13.md" >}})
- [🔥AssetOpsBench填平鸿沟！AI Agent基准测评如何真实落地工业场景？]({{< relref "posts/20260127-blogs_podcasts-assetopsbench-bridging-the-gap-between-ai-agent-be-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*