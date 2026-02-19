---
title: "使用 Amazon Bedrock AgentCore 构建统一智能系统"
date: 2026-02-19T17:46:17+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "智能体", "统一智能", "CAKE", "知识引擎", "AWS", "LLM"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "随着企业业务场景日益复杂，构建能够跨系统协同的统一智能体已成为技术演进的关键方向。本文将深入探讨如何利用 Amazon Bedrock AgentCore，基于客户代理与知识引擎（CAKE）的实际落地案例，构建高效且统一的智能系统。通过解析这一技术实现，读者将掌握连接数据与决策的核心逻辑，从而优化自身架构设计。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore
scenarios: ["大语言模型", "AI/ML项目"]
---

# 使用 Amazon Bedrock AgentCore 构建统一智能系统

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-18T23:54:29+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore)

---
## 摘要/简介

在本文中，我们将通过客户代理与知识引擎（CAKE）的实际实现，演示如何使用 Amazon Bedrock AgentCore 构建统一智能系统。

---
## 导语

随着企业业务场景日益复杂，构建能够跨系统协同的统一智能体已成为技术演进的关键方向。本文将深入探讨如何利用 Amazon Bedrock AgentCore，基于客户代理与知识引擎（CAKE）的实际落地案例，构建高效且统一的智能系统。通过解析这一技术实现，读者将掌握连接数据与决策的核心逻辑，从而优化自身架构设计。

---
## 评论

**中心观点**
文章提出了一种基于 Amazon Bedrock AgentCore 的“统一智能”架构范式（CAKE），主张通过在基础设施层实现工具调用与企业知识的深度耦合，来解决当前生成式 AI 应用中普遍存在的“最后一公里”落地与幻觉问题。

**支撑理由与深度评价**

**1. 从“提示工程”向“工程化编排”的范式转移**
*   **事实陈述**：文章详细介绍了 CAKE（Customer Agent and Knowledge Engine）系统，利用 Bedrock AgentCore 作为编排核心，连接了 RAG（检索增强生成）系统和 API 工具链。
*   **深度分析**：这是目前行业从 POC（概念验证）走向生产环境的关键转折。传统的 LangChain 或直接调用 API 模式在处理复杂业务逻辑时往往面临“上下文遗忘”或“工具调用死循环”的问题。AgentCore 提供的托管式编排，实际上是将 LLM 从一个“聊天机器人”提升为“任务调度器”。这种架构的严谨性在于它承认了 LLM 的不可控性，并通过确定性的工具框架来约束其行为。
*   **反例/边界条件**：对于极其简单的问答场景（如 FAQ），引入 AgentCore 的编排层属于过度设计，增加了延迟和成本；此外，对于强逻辑推理任务（如数学证明），仅靠 AgentCore 的编排无法弥补模型本身的推理缺陷。

**2. 知识引擎的“私有化”与“非结构化”统一处理**
*   **事实陈述**：CAKE 系统展示了如何将企业内部的结构化数据（API）与非结构化知识（文档）统一接入 Agent。
*   **作者观点**：文章暗示这种统一能够打破企业内部的数据孤岛。
*   **你的推断**：这是企业级 AI 最具价值但也最难实施的点。Bedrock AgentCore 的价值在于提供了一套标准的“翻译层”，将企业异构数据源转化为 LLM 可理解的 Function Calling 或 Context。这种设计极大地降低了 RAG 系统接入传统 IT 架构的门槛。
*   **反例/边界条件**：当企业数据源存在频繁更新或高并发写入时，RAG 的索引滞后性会导致 Agent 做出基于旧数据的错误决策，这在金融或交易类场景中是不可接受的。

**3. 技术栈的“锁定”与“效率”博弈**
*   **事实陈述**：文章完全基于 AWS 生态构建。
*   **实用价值**：对于已经是 AWS 重度用户的企业，该方案具有极高的实用价值。它利用 AWS 的 IAM 权限管理、VPC 网络隔离等原生能力，解决了 AI 落地中最头疼的安全与合规问题。
*   **反例/边界条件**：这导致了极高的厂商锁定风险。如果未来 Anthropic (Claude) 或其他模型提供商在 Bedrock 上的价格劣势扩大，或者企业需要迁移至私有云，迁移成本将非常高昂。

**争议点与不同观点**

**1. “统一智能”的边界模糊**
文章标题虽为“统一智能”，但内容主要聚焦于客服或知识检索场景。**争议点在于**，AgentCore 目前展现的能力更多是“统一任务执行”，而非“统一认知”。真正的统一智能应包含自主规划和长期记忆能力，而 Bedrock AgentCore 在处理跨天、多步骤的复杂工作流时，目前的 State Management（状态管理）能力仍显生硬。

**2. 幻觉问题的真实解决程度**
文章声称通过 CAKE 解决了幻觉问题。**批判性观点**：RAG 只能通过提供上下文来*降低*幻觉，无法根除。当检索到的文档本身存在矛盾，或者 LLM 在进行推理时忽略了检索内容，AgentCore 并没有提供比传统 RAG 更本质的解决方案。它只是让“找借口”变得更难了，但并没有让模型变“诚实”。

**实际应用建议**

1.  **不要直接照搬架构**：CAKE 是一个很好的参考架构，但在实施前，必须先梳理企业的数据资产。如果你的数据主要存在于 SaaS 软件（如 Salesforce, Jira）而非自建数据库，优先考虑现成的 Connector，而非从零开发 API 接口。
2.  **关注“可观测性”**：在生产环境中，Agent 的决策过程是黑盒。建议在接入 AgentCore 的同时，强制启用 AWS CloudWatch 或第三方 Trace 工具（如 LangSmith），记录每一个 Thought 过程，否则调试将是一场噩梦。
3.  **混合模型策略**：不要迷信 Bedrock 上的单一模型。建议在 AgentCore 中配置路由逻辑，对于简单任务使用便宜快速的模型（如 Haiku），对于复杂推理任务使用强力模型（如 Sonnet/Opus），以优化成本。

**可验证的检查方式**

1.  **指标检测**：**Tool Call Success Rate（工具调用成功率）**。在 CAKE 系统运行两周后，统计 Agent 调用 API 后成功返回结果且未触发重试的比例。如果低于 85%，说明 Prompt 或 API Schema 设计存在问题。
2.  **实验测试**：**对抗性幻觉测试**。故意向 Agent 提问一个完全不在知识库中的问题，观察其是回答“我不知道”还是编造答案。这是验证 RAG 系统是否真正生效的“金标准”。
3.  **观察窗口**：**端到端延迟**。测量从用户发送问题到 Agent 最终生成回复的总耗时。如果超过 5-8 秒（包含 RAG 检索 + LLM 推理 + 多次 Tool Call），在实时客服场景中用户体验将大幅下降

---
## 技术分析

# 技术分析：基于 Amazon Bedrock AgentCore 的统一智能架构

## 1. 核心架构理念

文章阐述了从单一模型调用向结构化智能体架构演进的技术路径。核心在于利用 Amazon Bedrock AgentCore 构建一个名为 CAKE（Customer Agent and Knowledge Engine）的系统，该系统将大语言模型（LLM）定位为编排层，而非单纯的交互接口。

**架构转变**
*   **从碎片化到统一化**：传统开发常面临模型、知识库与业务 API 各自独立的问题。AgentCore 旨在提供一个统一的控制平面，将推理能力与企业现有的数据层和执行层连接。
*   **职责分离**：LLM 负责理解意图、规划步骤和生成响应，而 AgentCore 负责流程控制、工具调用和状态管理。这种分离使得系统行为更加可预测。

## 2. 关键技术组件

**Amazon Bedrock AgentCore**
作为核心框架，AgentCore 提供了构建代理所需的基础设施。它不仅处理与基础模型的交互，还负责管理对话状态、工具定义以及执行逻辑。它允许开发者通过配置而非硬编码的方式来定义 Agent 的行为边界。

**CAKE (Customer Agent and Knowledge Engine)**
CAKE 是基于 AgentCore 构建的具体实现案例，展示了如何将技术框架应用于客户服务领域。
*   **知识检索**：利用 RAG 技术连接企业私有数据源，确保回答的准确性。
*   **任务执行**：通过 Function Calling 机制，允许 LLM 在必要时调用外部 API 来执行具体操作（如查询订单状态），而非仅生成文本。

## 3. 技术实现逻辑

系统的工作流程主要包含以下三个阶段：

1.  **推理与规划**：AgentCore 接收用户输入后，利用基础模型分析意图。系统并非直接生成答案，而是先判断是需要检索知识、调用工具，还是进行普通对话。
2.  **工具编排**：如果需要执行操作，AgentCore 会根据预定义的 Schema 选择合适的工具（API），并生成必要的参数。这一过程包含了严格的参数校验，以确保执行的安全性。
3.  **响应生成**：系统将工具执行的结果或检索到的文档片段重新注入上下文，由 LLM 生成最终的自然语言回复。

## 4. 工程化挑战与应对

在构建此类企业级应用时，文章主要涉及了以下两个技术难点：

*   **状态管理与上下文保持**：在多轮对话中，系统需要维护跨请求的上下文信息。AgentCore 通过持久化会话状态解决了这一问题，确保 Agent 能够记住之前的交互历史和关键参数。
*   **执行确定性与错误处理**：为了防止模型幻觉导致的错误操作，AgentCore 引入了结构化的输出约束。如果模型生成的参数不符合 API 的定义要求，系统会拦截并要求重新生成，而非直接报错。

## 5. 应用价值总结

该技术方案的主要价值在于提供了一套标准化的开发模式。它降低了将生成式 AI 集成到复杂业务系统中的门槛，使得开发者能够更专注于业务逻辑的实现，而非底层的模型交互细节。通过将推理能力与执行能力解耦，企业能够构建出既具备自然语言理解能力，又能实际执行业务任务的自动化系统。

---
## 最佳实践

## 最佳实践指南

### 实践 1：设计清晰且专注的代理职责范围

**说明**:
单一代理试图处理所有任务会导致上下文混乱和推理能力下降。最佳实践是遵循“单一职责原则”，为特定的业务领域或任务类型（如“订单查询”、“技术支持”、“财务分析”）创建专门的代理。Amazon Bedrock AgentCore 依赖于编排层来协调这些代理，因此明确的边界能确保每个代理在其知识范围内提供最准确的响应。

**实施步骤**:
1. 识别业务流程中的关键节点，将其拆分为独立的领域。
2. 为每个代理定义具体的“Persona”和“目标”，并在系统提示词中明确其不负责的领域。
3. 利用 AgentCore 的编排能力，将特定意图路由到正确的代理，而不是让一个通用代理处理所有请求。

**注意事项**:
避免代理职责重叠。如果两个代理的职责边界模糊，编排层可能会频繁路由错误，导致用户体验下降。

---

### 实践 2：构建结构化且高质量的上下文源

**说明**:
AgentCore 的强大之处在于能够动态调用外部知识库。如果输入的数据源（如向量数据库、API 响应）充满噪声或格式不统一，模型生成的答案将缺乏准确性。建立统一的数据接入层，确保信息经过清洗、分块且富含元数据，是构建统一智能的基础。

**实施步骤**:
1. 在将文档存入 Knowledge Base 之前，实施标准化的 ETL 流程（清洗、去重、格式化）。
2. 为数据块添加丰富的元数据（如日期、部门、标签），以便代理在进行检索时能够过滤掉不相关的信息。
3. 定期审查和更新知识库内容，移除过时信息。

**注意事项**:
不要直接将原始数据转储给代理。未经处理的长文本会导致检索命中率降低（Lost-in-the-Middle 现象）。

---

### 实践 3：实施严谨的 Guardrails（护栏）与安全策略

**说明**:
统一智能不仅意味着能力强，还意味着输出安全可控。在多代理环境中，必须确保所有代理都遵守统一的安全标准、品牌准则和合规要求。利用 Amazon Bedrock Guardrails 可以在模型生成内容之前或之后进行拦截，防止有害内容、PII（个人身份信息）泄露或越狱攻击。

**实施步骤**:
1. 定义敏感词列表、拒绝话题和 PII 过滤规则。
2. 将 Guardrails 策略应用到所有相关的代理配置中，确保安全策略的一致性。
3. 针对特定代理（如金融顾问）设置额外的上下文 groundedness（依据性）检查，防止幻觉。

**注意事项**:
不要仅依赖模型的内置安全性。企业级的统一智能需要显式的、可审计的护栏层。

---

### 实践 4：优化提示词工程以增强工具使用能力

**说明**:
AgentCore 的核心功能是能够调用 Action Groups（API/工具）。如果提示词未能清晰地描述工具的用途或所需的参数，代理将无法有效地编排这些工具。说明性越强的提示词，能显著提高工具调用的成功率。

**实施步骤**:
1. 在系统提示词中明确列出代理可用的工具及其具体用途。
2. 提供具体的示例，展示在何种情况下应调用哪个工具以及期望的参数格式。
3. 要求代理在缺少必要参数时主动向用户提问，而不是编造参数值。

**注意事项**:
避免在提示词中频繁更改工具定义。工具接口的变更应与提示词的更新同步进行，否则会导致调用失败。

---

### 实践 5：建立全面的可观测性与反馈循环

**说明**:
要构建“统一智能”，必须能够看到整个系统的运行状态。仅关注单个请求的成功率是不够的。你需要监控代理的推理轨迹、工具调用链路、检索准确率以及最终的用户满意度。利用 Amazon CloudWatch 或 Bedrock 的内置观察功能来捕捉这些指标。

**实施步骤**:
1. 启用 Amazon Bedrock 的 Trace 功能，记录每个请求的完整执行路径（Orchestration, Knowledge Base, Response）。
2. 设置关键指标告警，如“工具调用失败率”、“检索返回空结果的比例”或“拒绝响应的频率”。
3. 建立“人机协同”机制，允许专家对代理的输出进行评分，并将这些数据用于未来的微调或提示词优化。

**注意事项**:
忽视日志记录将导致调试困难。特别是在多代理协作中，无法追踪错误发生在哪个节点（是路由错误、检索错误还是工具错误）是系统维护的最大障碍。

---

### 实践 6：利用延迟推理处理复杂任务链

**说明**:
对于复杂的多步骤任务，一次性生成完整的计划往往容易出错。AgentCore 支持延迟推理模式，允许代理在执行每一步后重新评估上下文，决定下一步行动。这种“思考-行动-观察”的循环能显著提高复杂任务的完成率。

**实施步骤**:
1. 在代理配置中启用高级推理功能（如果使用支持此功能的模型，如 Claude 3）。
2. 设计 Action Groups 时，确保每个工具的输出都能被下一个步骤清晰地解析和利用

---
## 学习要点

- 基于对 Amazon Bedrock AgentCore 及其构建统一智能相关内容的分析，以下是总结出的关键要点：
- Amazon Bedrock AgentCore 提供了一个无服务器编排框架，能够无缝协调多个 Agent 和系统，从而将分散的自动化工作流统一为连贯的解决方案。
- 该框架允许开发者通过声明式的方式定义复杂的多 Agent 协作逻辑，无需管理底层基础设施，显著降低了构建高级生成式 AI 应用的门槛。
- AgentCore 原生集成了 Amazon Bedrock 的模型托管能力，支持灵活调用不同的基础模型，并利用企业私有数据增强生成结果的准确性和时效性。
- 通过内置的增强型可观测性功能，开发者可以实时追踪 Agent 的推理过程和执行链路，便于调试、优化以及确保 AI 行为的透明度。
- 它具备强大的工具调用（Tool Use）和 API 集成能力，使得 AI Agent 能够安全可靠地连接企业现有系统，执行实际业务操作而不仅仅是生成文本。
- 统一智能架构解决了传统 AI 应用中存在的“孤岛效应”，确保不同领域的 Agent 能够共享上下文信息，协同完成跨部门的复杂任务。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [统一智能](/tags/%E7%BB%9F%E4%B8%80%E6%99%BA%E8%83%BD/) / [CAKE](/tags/cake/) / [知识引擎](/tags/%E7%9F%A5%E8%AF%86%E5%BC%95%E6%93%8E/) / [AWS](/tags/aws/) / [LLM](/tags/llm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [利用 Amazon Bedrock AgentCore 构建统一智能系统]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-4.md" >}})
- [基于 Amazon Bedrock AgentCore 构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-0.md" >}})
- [基于Amazon Bedrock AgentCore构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-3.md" >}})
- [基于Amazon Bedrock AgentCore构建统一智能系统]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-2.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*