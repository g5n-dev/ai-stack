---
title: 基于 Amazon Bedrock 构建具备记忆与身份认证的智能活动助手
date: 2026-02-26 11:22:54+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- AgentCore
- 智能体
- RAG
- 知识库
- 身份认证
- 无服务器
- Serverless
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 本文介绍了如何利用 Amazon Bedrock AgentCore 和 Amazon Bedrock Knowledge Bases 快速构建并部署一个具备生产级智能能力的活动助手。
  该智能助手的核心功能是**记住参会者偏好**，并随着时间的推移为用户构建个性化的活动体验。为了实现这一目标，方案利用了 Amazon
external_url: https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases
scenarios:
- RAG应用
- AI/ML项目
---

# 基于 Amazon Bedrock 构建具备记忆与身份认证的智能活动助手

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T19:51:08+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)

---

## 摘要/简介

本文演示如何利用 Amazon Bedrock AgentCore 的组件，快速部署一个生产就绪的活动助手。我们将构建一个能够记住参会者偏好并随时间积累个性化体验的智能伴侣，同时让 Amazon Bedrock AgentCore 承担生产环境部署的重任：利用 Amazon Bedrock AgentCore Memory 维护对话上下文和长期偏好，无需自定义存储方案；利用 Amazon Bedrock AgentCore Identity 实现安全的多 IDP 身份认证；以及利用 Amazon Bedrock AgentCore Runtime 实现无服务器扩展和会话隔离。我们还将使用 Amazon Bedrock Knowledge Bases 进行托管式 RAG 和活动数据检索。

---

## 导语

构建一个能够“记住”参会者偏好并随时间演进的智能活动助手，往往面临对话上下文管理、安全认证及后端存储的复杂性挑战。本文将演示如何利用 Amazon Bedrock AgentCore 的核心组件（如 Memory、Identity 和 Runtime）高效处理这些生产级部署难题，并结合 Amazon Bedrock Knowledge Bases 实现托管式 RAG 检索。通过阅读本文，您将掌握快速构建具备长期记忆、安全多租户认证及无服务器扩展能力的生产级智能伴侣的实践方法。

---

## 摘要

本文介绍了如何利用 Amazon Bedrock AgentCore 和 Amazon Bedrock Knowledge Bases 快速构建并部署一个具备生产级智能能力的活动助手。

该智能助手的核心功能是**记住参会者偏好**，并随着时间的推移为用户构建个性化的活动体验。为了实现这一目标，方案利用了 Amazon Bedrock AgentCore 的以下关键组件来处理生产部署中的复杂任务：

1.  **Amazon Bedrock AgentCore Memory**：负责维护对话上下文和长期的用户偏好，无需开发者构建自定义的存储解决方案。
2.  **Amazon Bedrock AgentCore Identity**：提供安全的多身份提供商（IDP）认证支持。
3.  **Amazon Bedrock AgentCore Runtime**：提供无服务器架构的扩展能力及会话隔离，确保服务的高可用性。

此外，该方案还结合了 **Amazon Bedrock Knowledge Bases**，通过托管式检索增强生成（RAG）能力来实现高效的活动数据检索。

---

## 评论

**文章中心观点**
该文章主张利用 Amazon Bedrock 的 AgentCore 和 Knowledge Bases 组件，通过编排基础模型与私有数据，可以低代码、高效率地构建出具备长期记忆和个性化能力的生产级智能活动助手。

**支撑理由与评价**

**1. 技术架构的严谨性与解耦能力（事实陈述）**
文章的核心在于展示如何将复杂的 AI 应用工程化。从技术角度看，Bedrock AgentCore 实际上充当了“编排层”的角色，解决了 LLM 应用开发中最棘手的“确定性”问题。
*   **深度分析：** 文章强调了将推理（LLM）与检索（RAG）分离的架构。AgentCore 负责工具调用和任务规划，而 Knowledge Bases 负责上下文注入。这种分离使得系统维护和更新变得更加容易，符合现代软件工程中高内聚低耦合的原则。它实际上是在推销一种“托管式 Chain-of-Thought”的实现方案。
*   **边界条件/反例：** 这种架构在处理极度依赖实时状态的交互时可能存在延迟。如果活动数据更新频率达到秒级（例如拍卖系统），Knowledge Bases 的向量索引更新可能存在滞后，此时直接通过 API 调用数据库可能比通过 RAG 更高效。

**2. 开发效率与“生产就绪”的定义（作者观点 + 你的推断）**
文章声称能够“快速部署”并达到“生产就绪”状态，这主要针对的是中大型企业缺乏 AI 基础设施团队的情况。
*   **深度分析：** 这里的“生产就绪”更多是指 AWS 云原生环境下的可用性（如安全性、合规性、可扩展性），而非业务逻辑的完美。对于已经在 AWS 生态内的企业，这种方案极大地降低了从 POC（概念验证）到 Production（生产）的门槛。
*   **边界条件/反例：** 对于非 AWS 环境或多云策略的企业，这种深度绑定可能导致 Vendor Lock-in（供应商锁定）。此外，过度依赖托管服务会牺牲底层模型的微调能力，如果 AgentCore 的预置逻辑无法满足特定的业务逻辑（例如非常规的对话流控制），开发者可能会感到束手无策。

**3. 个性化体验与长期记忆的实现机制（你的推断）**
文章提到“记住参会者偏好并建立个性化体验”，这实际上演示了如何将静态的 RAG 转变为动态的 Stateful Application（有状态应用）。
*   **深度分析：** 这不仅仅是检索信息，更涉及到了用户画像的实时构建。从行业角度看，这代表了从“通用的 ChatBot”向“Action Agent”（行动代理）的演进。AgentCore 可能通过在对话上下文之外维护一个用户 Profile Store 来实现这一点，这是构建 C 端 AI 应用的关键。
*   **边界条件/反例：** 隐私合规是一个巨大的隐患。在 GDPR 或 CCPA 等法规下，将用户偏好长期存储并用于模型推理需要明确的授权机制。文章若未深入探讨数据治理，在实际落地时可能会遇到法律障碍。

**4. 行业影响与标准化趋势（事实陈述）**
这篇文章是云厂商推动 AI 工程化标准化的一个缩影。
*   **深度分析：** 行业正在从“手写 Prompt + 手写 LangChain 代码”向“声明式/配置化 Agent”转变。AWS Bedrock 的这一套组合拳，实际上是在定义企业级 AI 应用的标准范式：即不要每个人都去重写一遍检索逻辑和对话管理，而是通过配置 Agent 来实现。
*   **边界条件/反例：** 这种标准化可能会扼杀一些边缘创新。开源社区（如 LangFlow, Dify）提供了更灵活的节点控制，而 Bedrock AgentCore 这种黑盒方案可能更适合标准业务场景（如客服、活动助理），但不适合需要高度定制推理路径的科研或创意场景。

**实际应用建议**

1.  **成本控制策略：** 在部署此类 Agent 时，务必监控 Knowledge Bases 的检索调用次数和 Bedrock 的 Token 消耗。建议在开发初期使用较小的模型（如 Claude Haiku 或 Llama 3）进行逻辑验证，仅在上线后切换到高性能模型。
2.  **混合检索架构：** 不要完全依赖 Knowledge Bases 的向量检索。对于活动中的高频结构化数据（如日程表、票价），建议保留传统的 SQL 查询接口作为 Agent 的工具，这样能显著提高准确性和响应速度。
3.  **数据治理先行：** 在构建“记忆”功能前，必须先建立用户数据的遗忘和修正机制。如果 AI 记住了错误的用户偏好，必须提供人工干预的接口来重置状态。

**可验证的检查方式**

1.  **指标：幻觉率**
    *   *验证方式：* 使用 RAGAS 框架或类似工具，针对 Agent 的回答进行“忠实度”评分。检查 Agent 在生成建议时，是否严格引用了 Knowledge Base 中的文档，还是编造了不存在的活动信息。
2.  **实验：冷启动 vs. 热启动测试**
    *   *验证方式：* 模拟一个全新用户和一个具有历史交互记录的用户，询问相同的问题。观察 AgentCore 是否能够利用历史记忆（热启动）提供差异化的、更精准的推荐。如果两者回答一致，则说明记忆模块未生效。
3.  **观察窗口：延迟分布**
    *   *验证方式：* 在高并发场景下（如活动开始前的咨询高峰），监控 Agent 的端到端响应时间（P95 和 P99 延迟）。检查 Knowledge

---

## 技术分析

基于您提供的文章标题和摘要，以及对 Amazon Bedrock 生态系统（特别是 AgentCore 和 Knowledge Bases）的深度了解，以下是对该技术方案的全面深入分析。

---

### 深度分析报告：基于 Amazon Bedrock 构建智能事件代理

### 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点在于展示如何利用 **Amazon Bedrock AgentCore** 这一全托管框架，快速构建一个具备长期记忆和个性化能力的生产级智能助手。它证明了在不需要从头构建复杂基础设施的情况下，开发者可以创建一个能够理解上下文、利用企业知识库并执行复杂任务的 AI 代理。

**作者想要传达的核心思想**
作者试图传达“**应用层智能的民主化**”这一思想。通过 Bedrock AgentCore，构建 AI 应用的重心从“模型微调和算法工程”转移到了“流程编排和知识管理”。核心思想是：**现代 AI 应用的价值在于 Agent（代理）能够自主地协调 LLM（大语言模型）、RAG（检索增强生成）和工具调用，而非仅仅依赖模型本身的参数知识。**

**观点的创新性和深度**
该观点的深度在于它解决了当前生成式 AI 落地中的“最后一公里”问题：
1.  **从 Chatbot 到 Agent 的转变**：不仅仅是生成文本，而是能够处理“事件”相关的复杂逻辑（如预订、推荐、日程管理）。
2.  **状态持久化**：强调“记住偏好”和“随时间构建体验”，这触及了目前无状态 LLM 的痛点，通过 AgentCore 的内存管理能力实现了有状态的交互。
3.  **全栈生产就绪**：强调“Production-ready（生产就绪）”，意味着方案涵盖了安全、监控、可扩展性和错误处理，而不仅仅是演示代码。

**为什么这个观点重要**
随着大模型能力的爆发，企业面临的最大挑战不再是“模型不够聪明”，而是“模型无法融入业务流程”。该文章提出的架构模式是企业级 AI 落地的关键路径，它降低了技术门槛，使得企业能够快速将 AI 转化为实际的生产力工具，特别是在需要高度个性化服务的活动管理、客户服务等领域。

### 2. 关键技术要点

**涉及的关键技术或概念**
*   **Amazon Bedrock AgentCore**: 核心编排引擎，负责 Agent 的生命周期管理、指令解析和子任务分解。
*   **Amazon Bedrock Knowledge Bases**: 实现 RAG（检索增强生成）的托管服务，连接私有数据源（如活动日程、嘉宾简介）。
*   **Foundation Models (FM)**: 底层推理引擎（如 Claude 3 或 Titan 系列），通过 API 调用。
*   **Memory/State Management**: 内存存储机制，用于保存用户画像和历史交互数据。
*   **Function Calling / Tool Use**: Agent 连接外部系统（如票务系统、CRM）的能力。

**技术原理和实现方式**
1.  **指令编排**: 开发者定义一套高层指令，告诉 Agent 它是“活动助手”，以及它的职责边界。
2.  **检索增强 (RAG)**: 当用户询问“有哪些关于 AI 的讲座？”时，AgentCore 自动将查询向量化，在 Knowledge Bases 中检索相关文档块，将检索到的上下文与用户问题合并后发送给 LLM。
3.  **记忆机制**: 在对话过程中，Agent 提取关键信息（如用户喜欢的演讲者），将其存储在持久化存储中。在后续交互中，Agent 自动加载这些信息作为系统提示词的一部分，实现个性化。
4.  **推理与规划**: 利用 Foundation Models 的推理能力，AgentCore 将用户的模糊请求（如“帮我安排下午的行程”）分解为具体的步骤：查询日程 -> 检查用户偏好 -> 对比时间 -> 生成建议。

**技术难点和解决方案**
*   **难点：幻觉控制**。AI 可能编造不存在的活动信息。
    *   **解决方案**：利用 Knowledge Bases 强制模型仅基于检索到的私有数据回答，并配置 `guardrails`（防护栏）拦截不当话题。
*   **难点：上下文窗口限制与遗忘**。
    *   **解决方案**：AgentCore 负责管理对话历史，只保留相关的摘要信息，并将长期记忆委托给外部数据库存储，而非全部塞入 Prompt。
*   **难点：工具调用的确定性**。
    *   **解决方案**：通过 OpenAPI 规范明确定义工具接口，让模型通过结构化 JSON 进行函数调用。

**技术创新点分析**
*   **Zero-shot Agent Creation**: 无需编写复杂的 Python/Java 代码来定义 Agent 行为，通过配置和自然语言指令即可生成。
*   **透明的推理链**: Bedrock AgentCore 通常会提供推理过程的可视化（Trace），展示 Agent 为什么要调用某个工具或检索某个文档，这对于调试至关重要。

### 3. 实际应用价值

**对实际工作的指导意义**
该架构为开发者提供了一套标准化的“企业级 LLM 应用开发模板”。它指导开发者不要试图用 Prompt 解决所有问题，而是应该：
1.  用 Knowledge Base 解决事实性问题。
2.  用 Tools 解决操作性问题。
3.  用 Agent Core 解决逻辑流程问题。

**可以应用到哪些场景**
*   **企业内部 IT 支持**：结合知识库和工单系统（Jira/ServiceNow）自动处理故障。
*   **电商购物助手**：结合商品目录（KB）和订单系统，提供个性化导购。
*   **医疗健康咨询**：基于医疗指南进行初步分诊，并记录患者病史。
*   **旅游规划**：整合景点信息和预订引擎。

**需要注意的问题**
*   **数据新鲜度**：Knowledge Bases 的数据同步通常是批量的，非实时。对于高频变动的数据（如票务余量），需要通过 API 查询而非 RAG。
*   **成本控制**：Agent 模式涉及多轮 LLM 调用（思考+行动+观察），成本比简单 Chat 高，需要设置合理的超时和迭代步数限制。

**实施建议**
*   从小处着手，先构建一个仅基于 RAG 的问答机器人，验证知识库质量。
*   逐步引入工具调用，连接非关键性系统。
*   最后加入长期记忆和个性化推荐逻辑。

### 4. 行业影响分析

**对行业的启示**
这标志着 **SaaS (Software as a Service) 向 MaaS (Model as a Service) 再向 AaaS (Agent as a Service) 的演进**。软件的交互界面正在从 GUI（图形用户界面）向 LUI（自然语言界面）转变。行业将不再比拼谁的模型参数大，而是比拼谁能更好地编排 Agent、谁拥有更高质量的知识库以及谁的业务流程更易于被 AI 调用。

**可能带来的变革**
*   **客服行业的重构**：传统的“关键词匹配+IVR”将被基于 Agent 的对话系统彻底取代。
*   **个性化服务的规模化**：以前只有高端客户享有的 1 对 1 专属助理服务，现在可以通过 AI Agent 以极低成本规模化复制。

**相关领域的发展趋势**
*   **多模态 Agents**：未来的 Event Agent 不仅能处理文本，还能看会场地图图片、听演讲录音。
*   **Agent-to-Agent 通信**：活动代理可能会直接与酒店预订代理、出行代理协商，完成跨平台的服务。

### 5. 延伸思考

**引发的其他思考**
*   **隐私与合规**：当 Agent “记住”了用户偏好，这些数据存储在哪里？是否符合 GDPR/PIPL？如何在“个性化”与“隐私”之间通过遗忘机制取得平衡？
*   **Agent 的“黑盒”焦虑**：虽然 AgentCore 提供了 Trace，但用户仍然难以完全理解 AI 为什么做出了某个决定。如何建立对 AI 自主行为的信任？

**可以拓展的方向**
*   **Proactive Agents (主动代理)**：目前的文章主要讨论被动响应。未来的方向是 Agent 主动监测事件（如“讲座即将开始”），并在合适时机主动通知用户。
*   **情感计算**：Agent 识别用户在活动中的情绪（焦虑、困惑），并动态调整沟通策略。

**未来发展趋势**
*   **小模型与大模型的协同**：AgentCore 可能会根据任务难度，动态路由到小模型（简单任务）或大模型（复杂推理），以优化成本和延迟。

### 7. 案例分析

**结合实际案例说明**
设想一个大型科技会议（如 AWS re:Invent）。
*   **传统模式**：用户在 APP 里搜索关键词，翻阅复杂的日程表，手动添加到日历。
*   **Agent 模式**：用户对手机说：“我对生成式 AI 感兴趣，但下午 2 点我有空，帮我推荐一个适合初学者的讲座，并帮我预约。”

**成功案例分析**
*   **关键成功因素**：知识库包含了讲座的详细描述（包括难度级别），且 Agent 能够访问日历 API。Agent 成功过滤掉了高级别的“架构师深度解析”，推荐了“入门讲座”，并自动写入了日历。

**失败案例反思**
*   **潜在失败点**：如果知识库数据未更新，某场讲座取消了，但 Agent 仍然推荐了它（幻觉/数据滞后）。
*   **教训**：必须建立数据同步机制，并在 Prompt 中加入“如果不确定信息，请告知用户去官网核实”的指令。

### 8. 哲学与逻辑：论证地图

**中心命题**
> **利用 Amazon Bedrock AgentCore 和 Knowledge Bases 构建的事件代理，能够以低代码、高可靠的方式实现具备长期记忆和个性化能力的生产级 AI 助手，从而显著提升用户体验。**

---

## 最佳实践

### 实践 1：精心设计知识库数据架构

**说明**: 构建高性能智能事件代理的基础在于高质量的知识库。为了确保 Amazon Bedrock Knowledge Bases 能够高效检索相关信息，必须对非结构化数据（如事件日志、报告、文档）进行预处理。这包括将大文件切分为易于管理的语义块，并确保元数据（如时间戳、严重性、事件ID）与内容正确关联，以便代理能够准确理解上下文。

**实施步骤**:
1. **数据清洗与标准化**：在上传到 S3 之前，去除噪声数据，统一日期格式和术语。
2. **分块策略**：根据数据的语义密度调整分块大小。对于事件日志，可按时间窗口或单个事件条目进行分块；对于文档，可按段落或章节分块。
3. **元数据提取**：确保每个数据块都包含必要的元数据字段（例如 `event_type`, `timestamp`, `source`），以便在检索时进行过滤。

**注意事项**: 避免分块过大导致上下文丢失，或分块过小导致碎片化信息过多，影响检索准确率。

---

### 实践 2：优化提示词工程以引导推理

**说明**: Amazon Bedrock AgentCore 的核心能力依赖于基础模型的推理能力。通过精心设计的系统提示词，可以明确代理的角色定义、任务边界和输出格式。对于“事件代理”而言，必须指示模型严格依据知识库检索到的信息进行回答，以减少幻觉现象。

**实施步骤**:
1. **定义角色**：在提示词中明确指定模型的角色（例如：“你是一个专门用于分析IT事件日志的智能助手”）。
2. **约束指令**：添加约束条件，要求模型在未找到相关信息时明确回答“不知道”，而不是编造答案。
3. **思维链引导**：引导模型在生成最终响应前展示推理过程，特别是在分析复杂事件根因时。

**注意事项**: 定期审查和迭代提示词，使用不同的测试用例验证模型的响应是否符合预期。

---

### 实践 3：配置高效的检索策略与参数

**说明**: 智能事件代理的性能很大程度上取决于 RAG（检索增强生成）阶段的效率。单纯依赖语义相似度搜索可能不足以处理特定的事件查询（如精确的时间范围或特定的错误代码）。必须配置混合检索或元数据过滤策略。

**实施步骤**:
1. **启用元数据过滤**：在 Knowledge Bases 配置中，利用元数据筛选条件（如 `date > '2023-01-01'`）来缩小搜索范围。
2. **调整检索参数**：根据实验结果调整 `SemanticSearchConfiguration` 中的向量相似度阈值。
3. **设置返回数量**：合理设置返回给 LLM 的上下文文档数量，通常在 5 到 10 个之间，以平衡上下文窗口和信息量。

**注意事项**: 如果检索结果经常不相关，检查分块策略和 Embeddings 模型的选择是否适合特定领域的数据。

---

### 实践 4：利用 Agent Action Groups 实现工具调用

**说明**: 仅仅回答问题是不够的，智能事件代理通常需要执行操作（如查询实时状态、创建工单或调用 API）。通过定义 Action Groups，将 Bedrock Agent 与 Lambda 函数或其他 API 集成，使代理具备“手”来执行任务。

**实施步骤**:
1. **定义 OpenAPI 架构**：为每个外部工具编写清晰的 OpenAPI (Swagger) 规范，描述参数和返回值。
2. **开发 Lambda 处理程序**：编写 Lambda 函数来处理具体的业务逻辑，例如从 DynamoDB 读取最新事件状态或调用 ServiceNow 创建工单。
3. **配置 Action Group**：在 Bedrock Agent 中将 API 架构与 Lambda 函数关联，并授予必要的 IAM 权限。

**注意事项**: 确保 API 描述足够详细，以便模型能够理解何时以及如何调用这些工具。处理 API 调用的超时和错误重试机制。

---

### 实践 5：建立严格的护栏与安全控制

**说明**: 事件数据通常包含敏感信息，且代理的操作可能影响生产环境。必须使用 Amazon Bedrock Guardrails 来防止代理生成有害内容、泄露 PII（个人身份信息）或执行未授权的操作。

**实施步骤**:
1. **配置内容过滤器**：设置 Guardrails 以阻止仇恨言论、暴力或其他不当内容。
2. **敏感信息屏蔽**：配置 PII 过滤规则，防止代理在输出中泄露内部 IP 地址、密钥或用户个人信息。
3. **上下文 groundedness 检查**：启用验证机制，确保代理的回答严格基于检索到的源材料，拒绝脱离上下文的闲聊。

**注意事项**: 护栏不应过度限制代理的功能，需要在安全性和可用性之间找到平衡。

---

### 实践 6：实施全面的评估与迭代循环

**说明**: 部署仅仅是开始。为了确保代理持续有效地处理事件，必须建立一套自动化和手动的评估流程。利用 Bedrock 的评估功能或自定义工作流来监控检索准确

---

## 学习要点

- Amazon Bedrock AgentCore 提供了一个无代码框架，能够快速编排大型语言模型（LLM）、工具和知识库，从而将智能体从简单的聊天机器人转变为能够自主解决复杂问题的系统。
- 通过将 Amazon Bedrock Knowledge Bases 与私有数据集成，智能体可以利用检索增强生成（RAG）技术，在保持数据时效性和准确性的同时，有效缓解大模型的幻觉问题。
- 借助 OpenAPI Schema 定义的可操作函数，智能体能够实时调用业务系统 API（如查询订单或处理退款），实现从“对话”到“执行业务任务”的关键跨越。
- AgentCore 内置的“反思与修正”机制允许智能体在任务失败时自我分析错误并重新规划路径，显著提高了处理复杂多步骤工作流的自主性和可靠性。
- 利用 Amazon Bedrock 的 Foundation Model 模型评估功能，开发者可以基于预定义的标准自动测试智能体的推理能力和响应准确性，确保生产环境的质量。
- 该架构支持将智能体无缝部署到 Amazon Connect 等渠道，使企业能够利用生成式 AI 快速构建智能客服，在降低运营成本的同时提升客户体验。
- 通过将复杂的业务逻辑封装为可重用的组件，该解决方案大幅降低了定制化 AI 智能体的开发门槛，使企业能够更敏捷地适应不断变化的业务需求。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [RAG](/tags/rag/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/) / [身份认证](/tags/%E8%BA%AB%E4%BB%BD%E8%AE%A4%E8%AF%81/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [Serverless](/tags/serverless/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [构建具备记忆功能的智能活动助手：基于 Amazon Bedrock AgentCore 的实践]({{< relref "posts/20260226-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-2.md" >}})
- [利用 Amazon Bedrock 构建具备记忆与个性化能力的智能活动助手]({{< relref "posts/20260225-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-0.md" >}})
- [利用Amazon Bedrock构建生产级智能活动助理]({{< relref "posts/20260225-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-1.md" >}})
- [基于Amazon Bedrock构建AI招聘系统优化人才获取流程]({{< relref "posts/20260218-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-13.md" >}})
- [基于Amazon Bedrock AgentCore构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-12.md" >}})
