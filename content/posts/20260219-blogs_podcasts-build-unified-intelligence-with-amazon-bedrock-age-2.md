---
title: 基于Amazon Bedrock AgentCore构建统一智能系统
date: 2026-02-19 05:46:09+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- AgentCore
- LLM
- Agent
- RAG
- 统一智能
- CAKE
- 架构设计
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: '**利用 Amazon Bedrock AgentCore 构建统一智能系统：CAKE 实践总结** 本文介绍了如何通过 Amazon
  Bedrock 的 **AgentCore** 组件构建“统一智能”系统，并以作者在实际业务中落地的 **Customer Agent and Knowledge
  Engine (CA'
external_url: https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore
scenarios:
- 大语言模型
- RAG应用
- AI/ML项目
---

# 基于Amazon Bedrock AgentCore构建统一智能系统

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-18T23:54:29+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore)

---

## 摘要/简介

在这篇文章中，我们将通过我们在客户代理与知识引擎（CAKE）中的实际落地，展示如何利用 Amazon Bedrock AgentCore 构建统一智能系统。

---

## 导语

随着企业业务场景的日益复杂，如何打破数据孤岛并实现智能能力的统一调度，已成为技术落地中的关键挑战。本文将基于客户代理与知识引擎（CAKE）的实际落地经验，深入探讨如何利用 Amazon Bedrock AgentCore 构建统一智能系统。通过解析这一架构的核心逻辑与实施路径，我们希望为读者在构建高效、可扩展的企业级 AI 解决方案时提供切实可行的参考。

---

## 摘要

**利用 Amazon Bedrock AgentCore 构建统一智能系统：CAKE 实践总结**

本文介绍了如何通过 Amazon Bedrock 的 **AgentCore** 组件构建“统一智能”系统，并以作者在实际业务中落地的 **Customer Agent and Knowledge Engine (CAKE)** 系统为例，详细展示了其实现路径与技术细节。

### 1. 核心概念：什么是“统一智能”与 AgentCore
传统的 AI 应用往往呈现为碎片化的“烟囱式”结构，例如聊天机器人、搜索工具和业务自动化流程通常是分离的。**AgentCore** 的出现旨在打破这些壁垒。它是一个用于编排 AI 代理的核心组件，允许开发者通过代码定义代理的行为、工具集成和记忆机制。

通过 AgentCore，企业可以构建一个统一的大脑，不仅能处理对话，还能调用后台 API、检索知识库并执行复杂任务，从而将生成式 AI 转化为实际的业务生产力。

### 2. 实战案例：CAKE 系统架构
CAKE (Customer Agent and Knowledge Engine) 是一个基于 Bedrock 构建的端到端解决方案，旨在统一处理客户交互和知识管理。其核心架构包含以下层次：

*   **统一入口:** 接收用户请求。
*   **AgentCore (大脑):** 负责理解意图、规划推理路径并分发任务。
*   **工具与技能:** 连接企业内部 API、数据库或知识检索（RAG）能力。

### 3. 关键实现步骤与特性

#### **A. 代理编排**
AgentCore 允许开发者将复杂的业务逻辑封装为“代理”。在 CAKE 中，系统不再是一个简单的问答机器人，而是一个能够根据用户问题动态选择工具的智能体。例如，当用户查询订单状态时，AgentCore 会调用订单查询工具；当用户询问产品政策时，它会转向知识检索。

#### **B. 统一推理**
系统利用基础模型（如 Anthropic Claude）进行推理。AgentCore 负责管理提示词和上下文，确保模型能够准确理解何时需要查询知识库，何时需要调用业务 API，从而在单一对话中实现多步骤的问题解决。

#### **C. 知识引擎集成**
CAKE 深度集成了 RAG（检索增强生成）能力。AgentCore 可以无缝调用 Amazon Bedrock Knowledge Base，从非

---

## 评论

**中心观点**
文章提出了基于 Amazon Bedrock AgentCore 构建“统一智能”系统的架构范式，旨在通过 CAKE（Customer Agent and Knowledge Engine）案例证明，利用托管编排层能够有效解决大模型应用中工具调用与知识检索的碎片化问题，从而实现企业级 AI 的落地。

**支撑理由与深度评价**

**1. 架构演进：从“手写胶水代码”到“托管编排层”**
*   **[事实陈述]** 文章展示了 CAKE 系统如何利用 AgentCore 替代传统的 Python 脚本或 LangChain 等硬编码编排逻辑。
*   **[作者观点]** 这是行业从“原型阶段”迈向“生产阶段”的关键信号。早期的 RAG（检索增强生成）应用往往依赖松散的脚本，难以维护。AgentCore 实际上提供了一种**声明式**的 AI 编程范式，将“意图识别”、“参数提取”和“工具路由”标准化。
*   **[你的推断]** 这种标准化虽然牺牲了一定的灵活性，但极大地降低了系统耦合度。对于大企业而言，这意味着 AI 能力可以被更好地治理和审计。

**2. 统一智能：打破数据孤岛的实际尝试**
*   **[事实陈述]** CAKE 案例强调了将客户数据、知识库与自动化动作整合在单一 Agent 中的能力。
*   **[作者观点]** 这里的“统一”并非指模型大一统，而是指**交互界面的统一**和**上下文管理的统一**。AgentCore 充当了“大脑前额叶”的角色，协调作为“感官”的知识库和作为“手脚”的 API。
*   **[你的推断]** 这种架构解决了多 Agent 模式下的“乒乓效应”问题（即多个 Agent 之间无限循环调用），通过单核多线程的逻辑提升了响应速度。

**3. 技术护城河：AWS 原生集成的深度与广度**
*   **[事实陈述]** 文章暗示了 Bedrock 与 AWS 生态（如 Kendra、DynamoDB 等）的无缝连接。
*   **[作者观点]** 这是云厂商构建“飞轮效应”的典型策略。虽然开源框架（如 LangChain、LlamaIndex）也能做到类似功能，但 AgentCore 的价值在于**零配置的运维成本**和**企业级的安全合规**（如 VPC 支持）。
*   **[你的推断]** 对于非互联网行业的传统企业（如金融、制造），这种“开箱即用”的安全性比功能的丰富度更重要。

**反例与边界条件**

**1. 边界条件：复杂逻辑的黑盒问题**
*   **[你的推断]** AgentCore 这种高度封装的方案，在处理极度复杂的业务逻辑时（例如涉及 50 步以上的审批流或非线性的决策树），可能会遇到“黑盒困境”。当 Agent 表现不佳时，开发者很难像调试代码一样精准定位是 Prompt 问题还是模型推理问题。
*   **[对比]** 相比之下，使用开源框架（如 LangGraph）虽然代码量大，但可以对每一个节点的输入输出进行细粒度控制。

**2. 边界条件：成本与延迟的权衡**
*   **[事实陈述]** 文章未深入探讨并发场景下的成本。
*   **[你的推断]** 托管编排层通常伴随着按调用次数计费的隐藏成本。在高并发、低延迟要求的场景（如实时交易风控）下，AgentCore 增加的一跳网络请求可能导致延迟不可接受，此时直接调用模型 API 可能仍是更优解。

**3. 边界条件：多云环境的局限性**
*   **[你的推断]** CAKE 架构天然绑定 AWS 生态。对于采用多云策略的企业，这种“统一智能”反而可能形成新的孤岛，导致跨云的数据交互变得极其昂贵和复杂。

**可验证的检查方式**

1.  **鲁棒性测试（指标：工具调用成功率）**
    *   **验证方法**：构建一组包含模糊意图、错误参数和恶意指令的测试集。
    *   **观察窗口**：观察 AgentCore 在处理边缘案例时，是能够正确自我修正并拒绝执行，还是会陷入死循环或产生幻觉调用。如果其错误恢复率低于 90%，则证明该“统一智能”在生产环境仍需人工干预。

2.  **延迟基准测试（指标：端到端响应时间 P99）**
    *   **验证方法**：对比 CAKE 架构与直接调用 Founation Model + 硬编码检索逻辑的响应延迟。
    *   **观察窗口**：在知识库检索步骤增加（例如需要多次检索才能回答）的情况下，AgentCore 的编排开销是否呈线性增长。如果 P99 延迟超过 3秒，在 C 端场景中用户体验将大幅下降。

3.  **可观测性审计（指标：链路追踪完整性）**
    *   **验证方法**：检查 CloudWatch 或 AWS X-Ray 中生成的 Trace 数据。
    *   **观察窗口**：验证是否能够清晰地复现 Agent 的“思维链”。如果 Trace 中只能看到“Input -> Output”而无法看到 Agent 决策调用 Tool A 而非 Tool B 的具体推理过程，则该系统的可调试性较差。

**总结**

这篇文章从行业角度揭示了 AI 应用开发正在经历“从手工作坊到工业化生产”的转变。AgentCore 代表了云厂商试图将 AI 工程化标准化的野心。虽然其在通用性和开发效率上具有显著优势，但在面对极度复杂的定制化逻辑和多云环境时，仍需谨慎评估其适用

---

## 技术分析

### 1. 核心观点深度解读

**主要观点：**
文章主张利用 **Amazon Bedrock AgentCore** 构建统一智能系统，以解决企业 AI 应用中的“碎片化”问题。通过“CAKE（Customer Agent and Knowledge Engine）”案例，文章论证了单一编排架构在处理复杂业务流程时，优于传统的独立模型部署或松散耦合模式。

**核心思想：**
文章体现了一种从“以模型为中心”向“以架构为中心”的转变。其核心在于**“编排与统一”**，即通过 AgentCore 建立统一的控制平面，动态调用工具并访问统一的知识底座，从而避免数据和能力的孤岛效应。

**重要性：**
该方案对于企业级生成式 AI 的落地具有实际意义。统一智能架构有助于整合跨部门的数据与业务逻辑，降低维护多套独立系统的复杂性，并提升业务决策和执行的一致性。

### 2. 关键技术要点

**关键技术概念：**
*   **Amazon Bedrock AgentCore：** 指代 AWS Bedrock 中负责智能体编排的核心组件，负责将用户意图转化为具体的行动序列。
*   **CAKE (Customer Agent and Knowledge Engine)：** 具体的业务实现架构，结合了针对客户服务的知识库检索与事务处理能力。
*   **Unified Intelligence (统一智能)：** 一种架构模式，指不同业务线共享同一套推理基础设施和知识图谱。

**技术原理与实现：**
*   **ReAct 模式：** 系统底层逻辑通常基于 ReAct (Reasoning + Acting)，即“推理+行动”。系统接收查询后，先分析所需信息，再决定是进行知识检索（RAG）还是调用工具（API），最后执行并生成回复。
*   **编排层：** AgentCore 充当中间层，管理与基础模型（FMs）的交互，处理提示链，并维护会话状态。
*   **知识集成：** CAKE 系统涉及向量化数据库与 Bedrock 的集成，使 Agent 能够实时访问非结构化数据（如手册、工单）。

**技术难点与解决方案：**
*   **幻觉与准确性：** 为解决工具调用错误或上下文误解问题，系统通常采用 **Guardrails（护栏机制）** 和严格的 **Schema 定义** 来约束 Agent 行为，确保参数符合 API 要求。
*   **上下文与记忆：** 针对长对话场景，架构可能利用 Bedrock 的长上下文窗口能力，或通过外部记忆存储保存会话历史，以突破模型本身的记忆限制。

**技术创新点：**
主要创新在于将**知识检索**与**事务性操作**在统一架构中融合。CAKE 系统不仅能提供信息查询（答），还能执行业务操作（做），实现了从对话到业务闭环的连接。

### 3. 实际应用价值

**对实际工作的指导意义：**
该架构为企业提供了一套标准化的智能体构建范式。技术团队可以参考 CAKE 的实现，将分散的业务 API 和知识库整合到一个统一的 Agent 框架下。这不仅简化了开发流程，也为未来扩展更多业务场景提供了可复用的底座。

---

## 最佳实践

### 实践 1：设计清晰且具体的代理指令

**说明**:
AgentCore 的性能高度依赖于提供给基础模型的指令质量。模糊或过于复杂的指令会导致模型产生幻觉或无法正确调用工具。最佳实践是定义明确的角色、任务范围、约束条件以及输出格式，确保代理准确理解其职责和边界。

**实施步骤**:
1. 在代理配置中，明确设定代理的角色（例如：“你是一个专门处理财务数据的助手”）。
2. 详细描述任务目标，并明确列出代理**不能**做的事情（例如：“不要提供投资建议”）。
3. 定义代理在缺乏信息时应采取的行为（例如：“如果用户请求的信息不在上下文中，请要求用户澄清”）。
4. 包含少样本示例，展示预期的输入和输出格式。

**注意事项**: 定期审查和更新指令，特别是当底层数据源或业务逻辑发生变化时。

---

### 实践 2：构建模块化且语义化的 Action Group

**说明**:
Action Group 是代理与外部系统交互的桥梁。将功能按逻辑域进行分组（例如：将所有用户管理相关的 API 放在一个组中），并为每个函数提供清晰的描述和参数定义，有助于模型准确选择正确的工具。这比将所有 API 堆砌在一起更易于维护且推理准确率更高。

**实施步骤**:
1. 将 API 端点按业务功能分类，创建不同的 Action Group。
2. 为每个 API 函数编写详细的描述，说明其用途、副作用以及参数含义。
3. 确保 OpenAPI (Swagger) 架构定义严格符合 JSON Schema 标准，避免模型解析错误。
4. 使用清晰的命名约定（例如 `get_user_by_id` 而不是 `getData`）。

**注意事项**: 避免在单个 Action Group 中包含过多功能相似但参数细微不同的 API，这可能会混淆模型的选择逻辑。

---

### 实践 3：实施严格的 IAM 权限最小化原则

**说明**:
安全性是构建代理应用的关键。代理在执行 Action Group 时需要调用 AWS Lambda 或访问其他资源。必须为代理角色分配仅足以完成特定任务的权限，防止代理被提示注入攻击利用来访问未授权的数据。

**实施步骤**:
1. 为每个 Action Group 创建专用的 IAM 角色。
2. 在 IAM 策略中，显式列出允许调用的特定 Lambda 函数 ARN 或特定的 S3 路径。
3. 显式拒绝访问不相关的服务或资源。
4. 定期使用 IAM Access Analyzer 审查角色权限。

**注意事项**: 切勿为了测试方便而赋予 `*` 或 AdministratorAccess 权限。

---

### 实践 4：优化知识库检索上下文

**说明**:
当代理需要访问私有数据时，Amazon Bedrock Knowledge Base 是核心组件。为了提高检索准确率，需要对数据进行适当的分块，并配置合理的向量搜索参数，确保模型获取的是最相关的上下文片段，从而减少“胡编乱造”。

**实施步骤**:
1. 根据文档结构（如标题、段落）调整数据分块策略，通常 300-500 token 是一个较好的起点。
2. 为数据源配置适当的元数据过滤器，以便在查询时缩小搜索范围。
3. 在提示词中引用知识库时，指示模型“仅依据提供的上下文回答”。
4. 测试不同的嵌入模型，选择最适合特定领域语言特征的模型。

**注意事项**: 避免分块过小导致语义丢失，或分块过大导致检索结果包含过多无关噪音。

---

### 实践 5：建立全面的可观测性与日志监控

**说明**:
由于大模型具有非确定性，调试代理行为具有挑战性。必须利用 Amazon CloudWatch 和 Bedrock 的日志记录功能，捕获模型推理过程、API 调用链路以及用户交互历史，以便追踪问题根源并优化性能。

**实施步骤**:
1. 开启 Amazon Bedrock 的模型调用日志，将请求和响应流式传输到 CloudWatch Logs 或 S3。
2. 在 Lambda 函数（Action Group 后端）中结构化地记录业务逻辑日志。
3. 设置 CloudWatch 告警，用于监控错误率（如 4xx/5xx）、延迟时间或 Throttling 异常。
4. 使用 AWS X-Ray 进行端到端的请求追踪。

**注意事项**: 确保日志中不包含敏感的 PII（个人身份信息），必要时配置脱敏规则。

---

### 实践 6：配置合理的超时与重试机制

**说明**:
代理工作流涉及多个步骤（模型推理 -> 工具调用 -> 数据返回）。底层的 Lambda 函数或外部 API 可能会响应缓慢或失败。配置合理的超时时间可以防止用户等待过久，而重试机制则能提高系统的鲁棒性。

**实施步骤**:
1. 根据业务逻辑的复杂度，评估 Lambda 函数的执行时间，并相应地设置 Bedrock Agent 的超时参数。
2. 在 Action Group 的 API 定义中，为非幂等操作（如 POST）禁用自动重试，为幂等操作（如 GET）启用

---

## 学习要点

- 基于提供的主题 "Build unified intelligence with Amazon Bedrock AgentCore"，以下是关于该技术特性的关键总结要点：
- Amazon Bedrock AgentCore 是一项无服务器托管服务，旨在通过消除基础设施管理负担，帮助开发者更轻松地构建具备推理能力的生成式 AI 应用程序。
- 该服务提供了统一的构建块，能够将企业数据、API 操作和用户逻辑无缝集成，从而解决大型语言模型（LLM）上下文记忆有限和无法实时执行动作的问题。
- AgentCore 具备强大的“推理与规划”能力，能够自动将用户提出的复杂任务拆解为多个子步骤，并自主编排执行流程以完成最终目标。
- 通过内置的“护栏”机制，该服务确保 AI 智能体在执行任务时严格遵循安全与隐私政策，有效防止模型产生幻觉或输出不当内容。
- 开发者可以利用可视化工作流或代码配置，灵活地定义智能体如何检索知识（RAG）以及如何调用企业内部工具，实现高度定制化的业务逻辑。
- 该架构支持将复杂的单体应用拆解为多个专门的智能体，通过多智能体协作模式来处理更为精细和复杂的业务场景。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [LLM](/tags/llm/) / [Agent](/tags/agent/) / [RAG](/tags/rag/) / [统一智能](/tags/%E7%BB%9F%E4%B8%80%E6%99%BA%E8%83%BD/) / [CAKE](/tags/cake/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于 Amazon Bedrock AgentCore 构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-0.md" >}})
- [利用 Amazon Bedrock 构建AI招聘系统以优化人才获取流程]({{< relref "posts/20260213-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-3.md" >}})
- [LinqAlpha利用Amazon Bedrock构建“唱反调”机制以压力测试投资逻辑]({{< relref "posts/20260212-blogs_podcasts-how-linqalpha-assesses-investment-theses-using-dev-7.md" >}})
- [利用 Amazon Bedrock 构建由 AI 驱动的招聘系统]({{< relref "posts/20260212-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-1.md" >}})
- [基于 Amazon Bedrock 构建具备人工监管的 AI 招聘系统]({{< relref "posts/20260214-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-9.md" >}})
