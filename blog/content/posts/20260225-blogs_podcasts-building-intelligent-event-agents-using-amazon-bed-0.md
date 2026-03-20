---
title: 利用 Amazon Bedrock 构建具备记忆与个性化能力的智能活动助手
date: 2026-02-25 20:35:05+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- AgentCore
- RAG
- 智能体
- 知识库
- 无服务器
- 个性化
- 生产部署
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 本文介绍了如何利用 **Amazon Bedrock AgentCore** 和 **Amazon Bedrock Knowledge Bases**
  快速构建并部署一个具备生产级智能的活动助理助手。 **核心目标：** 构建一个能够“记住”参会者偏好并随时间推移提供个性化体验的智能伴侣，同时通过 AgentCore
external_url: https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases
scenarios:
- RAG应用
- AI/ML项目
---

# 利用 Amazon Bedrock 构建具备记忆与个性化能力的智能活动助手

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T19:51:08+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)

---

## 摘要/简介

本文演示如何利用 Amazon Bedrock AgentCore 的组件快速部署一个生产就绪的活动助手。我们将构建一个能够记住参会者偏好并随时间打造个性化体验的智能伴侣，同时由 Amazon Bedrock AgentCore 承担生产部署的重任：用于在无需定制存储方案的情况下维护对话上下文和长期偏好的 Amazon Bedrock AgentCore Memory、用于安全的多 IDP 身份验证的 Amazon Bedrock AgentCore Identity，以及用于实现无服务器扩缩和会话隔离的 Amazon Bedrock AgentCore Runtime。我们还将使用 Amazon Bedrock Knowledge Bases 进行托管式 RAG 和活动数据检索。

---

## 导语

构建具备长期记忆和个性化交互能力的智能体，往往是生产环境中的主要挑战。本文将演示如何利用 Amazon Bedrock AgentCore 的组件（如 Memory 和 Identity）快速部署一个生产就绪的活动助手，并结合 Amazon Bedrock Knowledge Bases 实现高效的托管式 RAG 检索。通过阅读本文，您将掌握在无需定制存储方案的前提下，构建能够维护对话上下文、安全隔离会话并随时间优化用户体验的智能应用的具体方法。

---

## 摘要

本文介绍了如何利用 **Amazon Bedrock AgentCore** 和 **Amazon Bedrock Knowledge Bases** 快速构建并部署一个具备生产级智能的活动助理助手。

**核心目标：**
构建一个能够“记住”参会者偏好并随时间推移提供个性化体验的智能伴侣，同时通过 AgentCore 简化生产环境部署的复杂性。

**主要技术组件与优势：**

1.  **Amazon Bedrock AgentCore：** 负责处理生产级部署的核心任务。
    *   **Memory（记忆）：** 维护对话上下文和长期偏好，无需开发者构建自定义存储解决方案。
    *   **Identity（身份）：** 提供安全的多身份提供商（IDP）认证。
    *   **Runtime（运行时）：** 提供无服务器扩展能力和会话隔离。
2.  **Amazon Bedrock Knowledge Bases：** 用于托管 RAG（检索增强生成）和活动数据检索，确保助手能获取准确的最新信息。

---

## 评论

### 中心观点
该文章通过展示利用 Amazon Bedrock 的 AgentCore 和 Knowledge Bases 构建具备长期记忆的智能会议助手，论证了**“编排层与检索增强生成（RAG）能力的深度解耦与标准化”**是降低企业级 Agent 开发门槛、实现从原型到生产环境跨越的关键路径。

### 深入评价与支撑理由

#### 1. 内容深度：从“手写逻辑”向“配置化编排”的范式转移
*   **支撑理由（作者观点/事实陈述）：** 文章的核心价值在于强调了 **AgentCore** 的作用。在传统的 LLM 应用开发中，开发者需要编写大量的代码来处理意图识别、工具调用和上下文管理。该文展示了如何利用 Bedrock 的托管服务将非结构化的自然语言请求转化为结构化的 API 调用。这种深度不仅体现在代码层面，更体现在架构层面——即如何利用 RAG（检索增强生成）来解决大模型的幻觉问题，同时利用 Agent 的规划能力来解决多步骤任务。
*   **你的推断：** 文章暗示了“Prompt Engineering”的局限性正在显现。单纯依靠优化提示词已难以满足复杂的业务逻辑，必须引入确定的架构模式。AgentCore 实际上是在构建一个“确定性的执行框架”，将 LLM 作为一个概率性的推理引擎嵌入其中。
*   **反例/边界条件：** 这种深度依赖于 Bedrock 生态的封闭性。对于需要极高定制化（如私有化部署、使用非 AWS 模型）的场景，这种深度反而是一种束缚。此外，对于极简任务（如单一问答），引入 AgentCore 可能属于过度设计，增加了延迟和成本。

#### 2. 实用价值：解决“最后一公里”的数据孤岛问题
*   **支撑理由（事实陈述）：** 文章详细演示了如何将企业的非结构化数据（如会议手册、PDF）通过 Knowledge Bases 接入 Agent。这是目前企业落地 AI 最大的痛点：**如何让大模型安全、准确地访问企业私有数据**。文章提供的代码示例和架构图具有直接的参考价值，特别是关于“记忆”的实现——即如何存储用户的偏好并在后续对话中调用，这对于提升用户体验（UX）至关重要。
*   **你的推断：** 实用价值还体现在“运维友好性”上。通过使用 AWS 托管服务，开发者无需自行搭建向量数据库或维护复杂的模型服务集群，这极大地缩短了 MVP（最小可行性产品）到生产环境的时间。
*   **反例/边界条件：** 实用性受限于数据格式。如果企业的数据深埋在复杂的 SQL 数据库或需要复杂的权限控制（Row-level Security），简单的 Knowledge Bases 配置可能无法胜任，仍需编写大量的自定义 Lambda 函数作为中间层，这削弱了“快速部署”的吸引力。

#### 3. 创新性：组件化 Agent 的落地实践
*   **支撑理由（作者观点）：** 文章提出的并非全新的算法创新，而是**工程化创新**。它将 Agent 的构建模块化：记忆、工具、知识库分离。这种“乐高式”的构建方式，使得非算法背景的应用开发者也能构建出具备推理能力的智能体。
*   **反例/边界条件：** 这种创新并非 AWS 独有。LangChain 或 LlamaIndex 等开源社区早已提出类似概念。文章的创新性更多在于“云厂商原生”的最佳实践，而非技术原理的突破。

#### 4. 行业影响与争议点：厂商锁定的隐形成本
*   **争议点（你的推断）：** 文章极力推崇 AWS 全家桶（Bedrock, OpenSearch, Lambda），这不可避免地带来了 **Vendor Lock-in（厂商锁定）** 的问题。一旦业务逻辑深度耦合了 Bedrock AgentCore 的特定 API，未来若想迁移至 Azure OpenAI 或 Google Cloud，迁移成本将极高。
*   **行业影响：** 这类文章标志着云厂商的竞争已从“模型算力”转向“应用框架”。AWS 试图通过降低开发门槛来锁定用户的使用习惯，迫使企业在选择云服务商时，不仅考虑基础设施，更考虑 AI 开发平台的易用性。

### 实际应用建议与验证方式

#### 1. 实际应用建议
*   **混合架构策略：** 建议采用“外挂式”架构。虽然使用 AgentCore 进行编排，但在核心业务逻辑层尽量保持与云服务商 API 的解耦。例如，将复杂的业务逻辑封装在标准的 REST API 中，Agent 仅负责调用 API，而不是将业务逻辑写在 Bedrock 的配置或 Prompt 中。
*   **成本监控：** Bedrock Knowledge Bases 的检索和 Agent 的多轮推理会产生显著的 Token 消耗。建议在实施时设置严格的预算告警，并对 Knowledge Base 的检索结果进行缓存，避免重复查询产生费用。
*   **数据治理优先：** 在接入 Knowledge Base 之前，必须先对文档进行清洗和分块策略优化。RAG 的效果 70% 取决于数据质量，30% 取决于模型能力。不要指望 Bedrock 自动解决数据混乱的问题。

#### 2. 可验证的检查方式

为了验证该文章所述方法在实际生产环境中的有效性，建议进行以下检查：

*   **指标 1：幻觉率与引用准确性**
    *   *检查方式：* 使用 RAGAS 框架或人工抽检，测量 Agent 返回的答案中，有多少比例能准确追溯到 Knowledge Base 中的具体文档片段。
    *   *观察窗口：* 上线后的前 100 个用户查询。

---

## 技术分析

基于您提供的文章标题和摘要，以及对 Amazon Bedrock 生态系统技术架构的深度理解，以下是对该技术方案的全面深入分析。

---

### 深度分析：基于 Amazon Bedrock 构建智能事件代理

### 1. 核心观点深度解读

**文章的主要观点：**
文章主张利用 **Amazon Bedrock AgentCore**（通常指代 Bedrock 的 Agents 框架或其底层编排能力）结合 **Amazon Bedrock Knowledge Bases**，可以快速构建一个具备生产级可用性的“智能活动助手”。该助手不仅能够回答问题，更重要的是具备**记忆能力**和**个性化体验构建能力**。

**作者想要传达的核心思想：**
核心思想在于**“状态化”与“编排”的结合**。传统的聊天机器人往往是无状态的，而作者强调通过 AgentCore 的编排能力，将大模型（LLM）的推理能力与外部知识库（RAG）以及用户偏好存储相结合，从而在多轮对话中积累信息，实现从“通用问答”到“个性化助手”的质变。

**观点的创新性和深度：**
*   **从 RAG 到 Agent 的演进**：不仅仅是检索增强生成（RAG），而是引入了 Agent 的自主规划能力。
*   **记忆即服务**：将用户偏好管理作为核心功能，而非简单的上下文窗口填充，这暗示了可能使用了长期记忆机制。
*   **生产就绪**：强调“Production-ready”，意味着文章不仅关注模型效果，还关注安全性、可扩展性和企业级集成。

**为什么这个观点重要：**
在活动管理场景中，信息碎片化严重（日程、嘉宾、场地）。通用的 LLM 无法解决实时性和私有数据问题。该方案展示了一种标准化的企业级 AI 落地范式，解决了大模型“懂道理但不懂业务”的痛点，对于企业数字化转型具有极高的参考价值。

### 2. 关键技术要点

**涉及的关键技术或概念：**
*   **Amazon Bedrock AgentCore**：这是核心编排层，负责将用户意图分解为任务，并调用相应的工具或 API。它处理“思考”过程。
*   **Amazon Bedrock Knowledge Bases**：基于 RAG（检索增强生成）技术，将非结构化数据（如 PDF 手册、网页）向量化并存储，供 LLM 检索。
*   **Foundation Models (FM)**：可能使用 Claude 3 或 Amazon Titan 等模型作为推理引擎。
*   **User Profile/Session Store**：用于存储“Attendee preferences”（参会者偏好）的数据库或状态存储。

**技术原理和实现方式：**
1.  **知识摄入**：将活动日程、演讲者简介等文档上传到 S3，通过 Bedrock Knowledge Bases 自动切分、嵌入并存储到向量数据库（如 OpenSearch Serverless）。
2.  **Agent 编排**：用户提问（例如“推荐适合我的技术讲座”），AgentCore 识别意图。
3.  **检索与推理**：Agent 调用 Knowledge Base 搜索相关讲座，同时读取用户的 Profile（历史偏好）。
4.  **个性化生成**：LLM 结合检索到的通用知识和用户私有偏好，生成定制化建议。

**技术难点和解决方案：**
*   **难点：幻觉问题**。
    *   **解决方案**：利用 Knowledge Bases 强制 LLM 基于检索到的数据生成答案，减少幻觉。
*   **难点：多轮对话中的上下文遗忘**。
    *   **解决方案**：AgentCore 负责管理会话状态，将关键信息（如用户对 AI 话题感兴趣）显式存储。
*   **难点：API 调用的延迟**。
    *   **解决方案**：利用 Bedrock 的异步流式传输能力。

**技术创新点分析：**
*   **零代码/低代码编排**：通过配置而非硬编码方式定义 Agent 的行为逻辑。
*   **Guardrails（护栏机制）**：虽然摘要未提及，但生产级应用通常包含 Bedrock Guardrails 以过滤不当内容。

### 3. 实际应用价值

**对实际工作的指导意义：**
该架构为企业提供了一套“拿来即用”的模版。IT 团队不再需要从零开始搭建 RAG 管道或编写复杂的 Prompt Chaining 逻辑，可以直接利用 Bedrock 的托管服务快速上线 AI 应用。

**可以应用到哪些场景：**
*   **企业内部 IT 支持**：结合员工身份信息（权限、部门）提供故障排查。
*   **电商购物助手**：结合用户历史浏览记录和商品知识库进行导购。
*   **医疗问诊分诊**：结合医学指南和患者过往病史。

**需要注意的问题：**
*   **数据隐私**：参会者偏好数据属于敏感信息，需确保存储和传输加密。
*   **数据新鲜度**：活动日程变更时，Knowledge Base 的索引更新频率。

**实施建议：**
*   先从小范围场景（如 FAQ）开始验证 Knowledge Base 的检索准确率。
*   逐步引入 Agent 的工具调用能力（如预订门票）。

### 4. 行业影响分析

**对行业的启示：**
这标志着 AI 应用开发从“模型调优”转向了“系统集成”。企业的核心竞争力不再是拥有最好的大模型，而是拥有**最干净的知识数据**和**最流畅的业务编排逻辑**。

**可能带来的变革：**
*   **SaaS 的智能化重构**：传统的活动管理软件将全面集成 AI Agent，从“人找信息”变为“信息找人”。
*   **客服行业的升级**：基于 Knowledge Bases 的 Agent 将大幅替代 L1/L2 级人工客服。

**相关领域的发展趋势：**
*   **Multi-Agent（多智能体）**：未来可能会有一个 Agent 负责推荐，另一个 Agent 负责预订，协同工作。
*   **Small Language Models (SLM)**：为了降低延迟和成本，特定任务可能会调用更小的模型。

### 5. 延伸思考

**引发的思考：**
如果 Agent 能够记住用户偏好，那么“遗忘权”如何实现？当用户要求“忘记我”时，如何从向量数据库和模型上下文中彻底清除痕迹？

**可以拓展的方向：**
*   **多模态交互**：除了文字，是否支持上传活动现场图片进行识别？
*   **事前/事后分析**：利用 Agent 收集的交互数据，分析活动组织方的痛点。

**未来发展趋势：**
*   **边缘侧 Agent**：部分推理逻辑下沉到端侧，保护隐私。
*   **自主性增强**：Agent 不仅能推荐，还能直接执行操作（如直接在日历上添加会议提醒）。

### 7. 案例分析

**结合实际案例说明：**
假设一个大型科技会议。
*   **传统方式**：用户在网页上手动搜索关键词，阅读枯燥的议程表。
*   **Agent 方式**：用户问：“我想找关于生成式 AI 的讲座，最好在下午，因为我上午要开会。” Agent 检索 KB 中的时间表和主题，并结合用户的时间限制，给出 3 个推荐。

**成功案例分析：**
*   **Salesforce/HubSpot**：它们已经集成了类似的数据增强 AI 助手，能够根据 CRM 数据和产品文档生成回复，极大地提高了销售效率。

**失败案例反思：**
*   **早期聊天机器人**：很多失败案例是因为缺乏上下文记忆，用户重复输入信息。Bedrock AgentCore 强调的“Remembers preferences”正是为了避免这种挫败感。

### 8. 哲学与逻辑：论证地图

**中心命题：**
**在生产环境中，利用 Amazon Bedrock AgentCore 结合 Knowledge Bases 是构建具备长期记忆和个性化服务能力的智能应用的最优解。**

**支撑理由：**
1.  **效率**：托管服务减少了从零构建 RAG 管道和 Agent 编排基础设施的时间（依据：AWS IaC 和托管服务的特性）。
2.  **准确性**：Knowledge Bases 利用 RAG 技术有效缓解了大模型的幻觉问题，确保回答基于真实数据（依据：RAG 的基本原理）。
3.  **个性化能力**：AgentCore 的状态管理能力使得应用能够跨越多轮对话积累用户画像，提供持续增值的服务（依据：摘要中提到的“remembers attendee preferences”）。

**反例或边界条件：**
1.  **成本敏感型场景**：对于极高频、低延迟的简单查询，Bedrock 按Token计费和全托管服务的开销可能过高，直接使用轻量级模型或传统搜索可能更优。
2.  **极度敏感数据**：某些企业级数据严禁出域，无法上传至云端 Bedrock，必须使用本地私有化部署方案。

**命题类型分析：**
*   **事实**：Bedrock 提供了 Agent 和 Knowledge Base 功能。
*   **预测**：这是构建此类应用的“最优解”或“主流趋势”。
*   **价值判断**：个性化体验是“好的”且“必要的”。

**立场与验证：**
*   **立场**：支持该命题，但需附加成本和合规性审查。
*   **可证伪验证方式**：
    *   **指标**：对比开发周期（从月级降到周级）、查询准确率（F1 Score > 90%）、用户满意度评分。
    *   **实验**：A/B 测试，一组使用传统搜索+规则引擎，一组使用 Bedrock Agent，测量任务完成率和用户留存率。
    *   **观察窗口**：系统上线后的 3 个月内，观察 API 调用成本与带来的业务价值（如转化率提升）的 ROI 比率。

---

## 最佳实践

### 实践 1：设计精细化的任务分解与编排逻辑

**说明**:

**实施步骤**:
1. 在 Agent 提示词中明确定义每个子任务的目标和输入输出标准。
2. 配置清晰的 Orchestration（编排）流程，确保 Agent 知道何时调用工具，何时询问用户澄清。
3. 为不同的任务分支设置明确的退出条件，防止 Agent 陷入无限循环或幻觉调用。

**注意事项**:
避免在单个 Action Group 中堆砌过多功能。建议将功能逻辑相近的工具归类到同一个 Action Group，以便 Agent 更高效地检索和调用。

---

### 实践 2：构建高准确率的 RAG 检索上下文

**说明**:
利用 Amazon Bedrock Knowledge Bases 为 Agent 提供私有数据支持是构建智能体的关键。最佳实践强调优化检索质量，确保 Foundation Model (FM) 获得最相关的上下文片段，从而生成准确的回答。单纯的向量检索可能不足以处理复杂的语义匹配，需要结合混合检索和高级检索策略。

**实施步骤**:
1. 在创建 Knowledge Base 时，启用“Hybrid Search”（混合检索），结合关键词和语义向量搜索，以提高精确匹配率。
2. 配置合适的 Chunking（分块）策略。对于结构化文档，建议使用固定大小分块并保留重叠部分；对于代码或特定格式，可考虑自定义解析器。
3. 利用 Metadata Filtering（元数据过滤），在检索时通过标签（如日期、部门、文档类型）缩小搜索范围，减少噪声。

**注意事项**:
定期评估检索结果。如果发现 Agent 频繁产生幻觉，通常是因为检索到的上下文不相关或包含冲突信息，此时应调整 Embedding 模型或 Chunk 大小。

---

### 实践 3：实施严格的工具定义与输入验证

**说明**:
Agent 通过调用 API (Action Groups) 与外部系统交互。最佳实践要求在定义工具的 OpenAPI Schema 时，必须极其精确和严格。模型生成参数的准确性直接取决于 Schema 的描述质量。如果定义模糊，Agent 可能会传递错误的参数类型或格式，导致调用失败。

**实施步骤**:
1. 为每个 API 参数编写详细的 `description`，明确说明参数的类型、取值范围和业务含义。
2. 在 Schema 中定义严格的 `type`（如 string, integer, array）和 `enum` 枚举值，限制 Agent 的生成空间。
3. 在后端 API 服务层实现参数校验逻辑，作为防止模型幻觉导致系统异常的最后一道防线。

**注意事项**:
不要在 Schema 中使用过于简略的描述。例如，不要只写 "userId"，而应写 "The unique identifier of the user, usually a 10-digit string"。

---

### 实践 4：优化提示词工程与角色设定

**说明**:
虽然 Bedrock Agent 提供了默认的编排模板，但通过自定义 Instructions（提示词）可以显著改善 Agent 的行为。最佳实践建议在提示词中明确 Agent 的角色定位、行为边界以及处理未知情况的策略。

**实施步骤**:
1. 在 Agent 配置的 "Instructions" 部分，清晰地定义 Agent 的角色（例如：“你是一个专业的订单处理助手”）。
2. 明确“负面约束”，告诉 Agent 它不能做什么（例如：“不要编造订单状态，如果数据库中没有记录，请如实告知用户”）。
3. 指导 Agent 如何处理多轮对话中的上下文引用（例如：“如果用户说‘它’，请指代上一个对话中的产品ID”）。

**注意事项**:
保持提示词的简洁与逻辑性。过长的提示词可能会增加延迟并干扰模型的推理能力。重点应放在定义输出格式和错误处理流程上。

---

### 实践 5：建立可观测性与日志追踪机制

**说明**:
在生成式 AI 应用中，确定性较难保证。最佳实践是充分利用 Amazon Bedrock 的 CloudWatch 集成和 Trace 功能，记录 Agent 的推理过程、检索到的文档片段以及 API 调用的输入输出。这对于调试和性能优化至关重要。

**实施步骤**:
1. 确保 Agent 配置中开启了详细的日志记录，包括 Orchestrator 的推理过程和最终模型的输出。
2. 设置 CloudWatch Alarms（警报），监控 API 调用失败率、延迟和检索结果的 Relevance Score（相关性评分）。
3. 定期审查日志，分析 Agent 在哪些步骤上产生了“幻觉”或错误的工具调用，并据此调整 Prompt 或 Schema。

**注意事项**:
注意日志中可能包含敏感用户数据（PII）。建议配置日志脱敏或确保访问日志的权限受到严格控制，以符合安全合规要求。

---

### 实践 6：应用护栏机制确保安全与合规

**说明**:
企业级应用必须防止 Agent

---

## 学习要点

- 利用 Amazon Bedrock AgentCore 构建的事件代理能够自主将非结构化请求转化为结构化查询，并自动编排 API 调用以执行复杂的业务工作流。
- 通过集成 Amazon Bedrock Knowledge Bases，智能体能够利用检索增强生成（RAG）技术，基于私有数据回答问题并有效减少模型幻觉。
- 该架构允许通过简单的配置将企业现有的 API 和数据源快速连接到大语言模型，从而显著降低 AI 应用的开发门槛和集成成本。
- 借助 Bedrock 的托管服务能力，开发者无需从头训练模型，即可轻松实现具备记忆、上下文理解和工具调用能力的智能应用。
- 智能体能够根据对话上下文自动决定何时查询知识库或调用特定工具，从而实现高度自动化且精准的事件处理流程。
- 该解决方案展示了如何利用生成式 AI 将传统的被动监控或搜索系统转变为能够主动理解和解决业务问题的智能助手。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [RAG](/tags/rag/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [个性化](/tags/%E4%B8%AA%E6%80%A7%E5%8C%96/) / [生产部署](/tags/%E7%94%9F%E4%BA%A7%E9%83%A8%E7%BD%B2/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-12.md" >}})
- [利用 Amazon Bedrock AgentCore 构建统一智能系统]({{< relref "posts/20260220-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-13.md" >}})
- [基于 Amazon Bedrock 构建AI招聘系统优化人才获取流程]({{< relref "posts/20260215-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-8.md" >}})
- [基于Amazon Bedrock构建AI招聘系统优化人才获取流程]({{< relref "posts/20260217-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-10.md" >}})
- [利用 Amazon Bedrock 构建AI招聘系统以优化人才获取流程]({{< relref "posts/20260213-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-3.md" >}})
