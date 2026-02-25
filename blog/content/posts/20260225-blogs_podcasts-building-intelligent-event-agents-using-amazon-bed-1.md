---
title: "基于 Amazon Bedrock AgentCore 构建具备记忆与个性化能力的活动助手"
date: 2026-02-25T22:01:33+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "RAG", "智能体", "知识库", "无服务器", "个性化", "身份验证"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何利用 **Amazon Bedrock AgentCore** 和 **Amazon Bedrock Knowledge Bases** 快速构建一个生产级的智能活动助理。 该智能助理能够记录参会者的偏好，并随着时间的推移提供个性化体验。在部署过程中，主要依赖 Amazon Bedrock AgentCo"
external_url: https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases
scenarios: ["RAG应用", "AI/ML项目"]
---

# 基于 Amazon Bedrock AgentCore 构建具备记忆与个性化能力的活动助手

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T19:51:08+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)

---
## 摘要/简介

本文介绍如何利用 Amazon Bedrock AgentCore 的组件，快速部署一个可投入生产环境的活动助手。我们将构建一个能够记住参会者偏好、并随时间持续打造个性化体验的智能助手，同时由 Amazon Bedrock AgentCore 承担生产部署的重任：Amazon Bedrock AgentCore Memory 用于在不依赖自定义存储方案的情况下，同时维护对话上下文和长期偏好；Amazon Bedrock AgentCore Identity 用于安全的多 IDP 身份验证；Amazon Bedrock AgentCore Runtime 用于实现无服务器扩缩容和会话隔离。我们还将使用 Amazon Bedrock Knowledge Bases 来实现托管式 RAG 和活动数据检索。

---
## 导语

构建能够真正理解用户并提供长期个性化服务的智能体，往往面临复杂的工程挑战。本文将介绍如何利用 Amazon Bedrock AgentCore 和 Amazon Bedrock Knowledge Bases，快速部署一个具备记忆能力和身份验证机制的活动助手。通过阅读本文，您将掌握如何利用托管式组件处理对话上下文、RAG 检索及生产级部署，从而高效构建可扩展的智能应用。

---
## 摘要

本文介绍了如何利用 **Amazon Bedrock AgentCore** 和 **Amazon Bedrock Knowledge Bases** 快速构建一个生产级的智能活动助理。

该智能助理能够记录参会者的偏好，并随着时间的推移提供个性化体验。在部署过程中，主要依赖 Amazon Bedrock AgentCore 的核心组件来处理生产环境的复杂性：

1.  **Amazon Bedrock AgentCore Memory**：用于维护对话上下文和长期偏好，无需开发自定义存储方案。
2.  **Amazon Bedrock AgentCore Identity**：支持安全的多身份提供商（IDP）身份验证。
3.  **Amazon Bedrock AgentCore Runtime**：负责实现无服务器扩展和会话隔离。

此外，该方案还结合了 **Amazon Bedrock Knowledge Bases**，用于实现托管的检索增强生成（RAG）以及活动数据的检索。

---
## 评论

**中心观点**
文章主张利用 Amazon Bedrock 的 AgentCore 和 Knowledge Bases 组件，可以低代码、高效率地构建具备长期记忆和个性化能力的生产级智能体，从而解决传统 RAG 应用在状态管理和任务编排上的复杂性。

**支撑理由与边界条件**

1.  **技术架构的解耦与自动化**
    *   **事实陈述**：文章强调了 AgentCore 如何接管“繁重的工作”，即通过 Orchestration（编排）层自动进行任务拆解和路由，利用 Knowledge Bases 实现自动化的 RAG 流程，无需手动编写复杂的 LangChain 或 LlamaIndex 逻辑。
    *   **作者观点**：这种“托管式”流程是未来的趋势，因为它降低了维护 Agent 与数据源之间同步关系的成本。
    *   **边界条件/反例**：对于极度定制化的推理逻辑（例如需要严格遵循特定法律条款的推理步骤），托管式编排的“黑盒”特性可能导致不可解释性，此时硬编码的传统流程可能更安全。

2.  **长期记忆与个性化体验**
    *   **事实陈述**：文章提出的“Event Assistant”场景中，Agent 能够记住参会者偏好并随时间优化体验。
    *   **你的推断**：这意味着 Bedrock AgentCore 在架构上支持将用户会话信息持久化，并能够通过检索增强（RAG）在后续对话中调用这些信息，而不仅仅依赖上下文窗口。
    *   **边界条件/反例**：在多租户或高并发环境下，如何确保记忆的隔离性和隐私合规是一个巨大挑战。如果缺乏严格的权限控制，Agent 可能会错误地泄露用户 A 的偏好给用户 B。

3.  **生产就绪的快速部署**
    *   **事实陈述**：文章展示了如何“快速部署”一个生产就绪的系统。
    *   **批判性观点**：虽然部署速度快，但“生产就绪”不仅包含功能实现，还包含延迟、吞吐量和错误率。
    *   **边界条件/反例**：在处理实时性要求极高的场景（如高频交易或即时客服）中，Bedrock AgentCore 多层调用的串行架构可能导致累积延迟过高，无法满足 SLA 要求。

**深入评价**

**1. 内容深度：从 Demo 到工程的跨越**
文章试图填补“Demo 级别 RAG”与“生产级 Agent”之间的鸿沟。
*   **事实陈述**：大多数技术博客仅停留在单次问答，而本文引入了“时间”维度（记忆）和“任务”维度（Agent）。
*   **分析**：深度适中。它没有深入探讨底层的向量索引算法或 Transformer 机制，而是聚焦于**架构集成**。它指出了一个关键痛点：开发者不应在 Prompt Engineering 和数据库管理之间疲于奔命，而应依赖基础设施层的自动化。
*   **不足**：对于“AgentCore”内部如何处理“循环任务”时的错误重试机制描述不够详细。这是生产环境中最容易出故障的地方。

**2. 实用价值：高门槛的降维打击**
*   **分析**：对于已经锁定 AWS 生态的企业来说，这篇文章具有极高的实用价值。它提供了一套标准化的“脚手架”。
*   **实际案例**：假设一家大型会展公司需要为 10 万名参会者提供服务。传统开发需要维护一个庞大的用户画像数据库和一套复杂的推荐算法。利用本文方案，可以直接将用户历史行为存入 Knowledge Base，通过自然语言接口调用，大幅减少了后端 API 的开发工作量。

**3. 创新性：服务化的 Agent 编排**
*   **分析**：文章的核心创新不在于算法，而在于**服务模式的创新**。它将 Agent 的“大脑”（LLM）、“记忆”（KB）和“手脚”封装成一个全托管服务。
*   **对比**：相比 LangChain 等开源库，Bedrock AgentCore 提供了更稳定的版本控制和更少的运维负担。这标志着 AI 开发从“库依赖”向“云服务依赖”的范式转移。

**4. 可读性与逻辑**
*   **评价**：作为一篇技术指南，逻辑清晰，遵循“痛点-方案-实现-效果”的结构。
*   **缺陷**：摘要末尾截断，且可能过于侧重 AWS 术语，对于非 AWS 用户（如使用 Azure 或 GCP）而言，迁移概念可能存在认知门槛。

**5. 行业影响：推动 AI Agent 标准化**
*   **推断**：此类文章的发布预示着云厂商正在争夺“Agent 基础设施”的标准制定权。如果 Bedrock AgentCore 成为事实标准，将导致行业对“全栈 AI 工程师”的需求降低，转而需求“AI 配置/提示词工程师”。

**6. 争议点与不同观点**
*   **Vendor Lock-in（厂商锁定）**：这是最大的争议点。一旦业务逻辑深度依赖 Bedrock 的特定 API（如 AgentCore 的特定编排语法），未来迁移到本地模型或其他云厂商的成本将极高。
*   **成本黑洞**：文章未深入探讨成本。Agent 模式通常涉及多次 LLM 调用和向量检索。在生产环境中，这种“智能”可能带来不可预测的账单，相比传统的确定性逻辑，性价比存疑。

**7. 实际应用建议**
*   **建议一**：不要直接用于核心业务。建议先用于内部辅助工具（如会议日程查询），待验证了 Agent 的幻觉率和延迟可控后，再逐步推向面向客户的 C 端场景。
*   **建议二**：严格监控 Memory 的

---
## 技术分析

基于您提供的文章标题和摘要，结合对 Amazon Bedrock 生态系统（特别是 AgentCore 和 Knowledge Bases）的技术理解，以下是对该文章核心观点和技术要点的深入分析。

---

# 深度分析报告：基于 Amazon Bedrock 构建智能事件代理

## 1. 核心观点深度解读

**主要观点：**
文章的核心观点是**“通过模块化的基础设施服务（Amazon Bedrock AgentCore 和 Knowledge Bases），企业可以快速构建出具备长期记忆、个性化推理能力的生产级 AI 代理，从而将大语言模型从‘对话玩具’转变为‘业务生产力工具’。”**

**核心思想：**
作者试图传达一种**“低代码/高智能”**的开发范式。传统的 AI 应用开发需要繁琐的模型微调、记忆管理和向量数据库集成。作者主张利用 Bedrock 的托管能力，让开发者专注于业务逻辑（如活动策划、用户偏好），而将复杂的模型编排、上下文管理和 RAG（检索增强生成）技术细节交给 AgentCore 处理。

**创新性与深度：**
*   **从“无状态”到“有状态”的跨越：** 摘要中特别提到“remembers attendee preferences and builds personalized experiences over time”（记住偏好并随时间构建个性化体验）。这触及了当前 LLM 应用的痛点——短期上下文窗口的限制。文章暗示了利用 Bedrock 的长期记忆机制或外部数据库存储来解决这一问题。
*   **Agent 编排的自动化：** AgentCore 不仅仅是一个 API 调用层，它隐含了“规划”和“工具使用”的能力。它展示了如何让 AI 自主决定是查询知识库还是调用外部 API（如预订票务）。

**重要性：**
对于企业而言，这意味着**部署时间的指数级缩短**和**可靠性的提升**。在活动管理等高并发、高准确性要求的场景下，这种架构解决了幻觉问题（通过 Knowledge Bases）和意图识别问题（通过 AgentCore），是生成式 AI 落地 B2B/B2C 场景的关键一步。

## 2. 关键技术要点

**涉及的关键技术：**
1.  **Amazon Bedrock AgentCore：** 负责智能体的核心编排，包括 Prompt 管理、思维链推理和工具调用。
2.  **Amazon Bedrock Knowledge Bases：** 实现了 RAG（检索增强生成）的托管化，自动处理文档分块、向量化（Embedding）和检索。
3.  **Foundation Models (FM)：** 可能使用了 Claude 3 或 Amazon Titan 系列模型作为底座。
4.  **User Profile Store (隐含)：** 用于存储长期用户偏好的数据库（如 DynamoDB）。

**技术原理与实现：**
*   **RAG 架构：** 系统不会直接让模型生成回答，而是先通过 Knowledge Bases 从私有数据（如活动日程、演讲者简介）中检索相关片段，将其注入到 Prompt 中，再由模型生成答案。这极大降低了幻觉风险。
*   **Agent Orchestration (代理编排)：** AgentCore 接收用户自然语言输入，将其转化为一系列动作。
    *   *Step 1:* 解析意图（查询日程 vs. 更改偏好）。
    *   *Step 2:* 如果查询信息，调用 Knowledge Base API。
    *   *Step 3:* 如果涉及个性化，读取/写入用户记忆库。
    *   *Step 4:* 综合信息生成最终回复。

**技术难点与解决方案：**
*   **难点：** 准确性控制（幻觉）。
*   **方案：** Knowledge Bases 强制模型基于检索到的数据回答，并配置源属性引用，确保信息可追溯。
*   **难点：** 上下文遗忘。
*   **方案：** 摘要中提到的“over time”暗示了会话记忆或长期记忆存储机制，确保 AI 在多次交互中保持用户偏好的连贯性。

## 3. 实际应用价值

**指导意义：**
这篇文章为**“如何构建企业级知识助手”**提供了标准答案。它证明了不需要从头训练模型，只需要利用现有基础设施和私有数据，就能构建出高度定制化的智能服务。

**应用场景：**
*   **企业内部 IT/HR 机器人：** 员工查询政策、报销流程。
*   **电商智能导购：** 记住用户历史购买记录，推荐商品（类比活动推荐）。
*   **医疗/法律咨询：** 基于专业文档库提供初步建议（需极高准确性）。
*   **教育辅导：** 基于教材回答学生问题，并跟踪学习进度。

**注意事项：**
*   **数据隐私：** 将用户偏好上传到云端需要严格的合规审查。
*   **延迟成本：** RAG 流程涉及检索和生成，响应时间可能长于直接对话，需优化用户体验。

**实施建议：**
不要试图一步到位。先构建一个简单的“只读”知识库助手，验证数据质量，再逐步加入“写入”和“记忆”功能，最后接入外部业务系统（如票务系统）。

## 4. 行业影响分析

**启示：**
行业正在从**“模型战争”**转向**“应用战争”**。谁能最快地将高质量数据与模型能力结合，谁就能胜出。Bedrock AgentCore 的出现降低了这一门槛，使得非 AI 原生公司也能快速部署智能体。

**变革：**
*   **SaaS 的智能化重塑：** 传统的 SaaS 软件将集成“副驾驶”功能。
*   **客服行业的自动化升级：** 从僵硬的关键词匹配机器人转向具备上下文理解能力的智能体。

**发展趋势：**
未来，**“Agentic Workflow”（代理工作流）**将成为标配。AI 不再是被动回答，而是能主动规划任务、调用工具、完成复杂操作。

## 5. 延伸思考

**拓展方向：**
*   **多模态交互：** 目前的代理主要基于文本，未来是否可以支持语音输入（Amazon Transcribe）和图像生成（用于生成会议议程图）？
*   **人机协同：** 当 AI 遇到无法处理的异常情况（如退款请求），如何平滑地转接给人工客服？

**待研究问题：**
*   如何评估 Agent 的“推理能力”？传统的准确率指标是否还适用？
*   在多轮对话中，如何防止“记忆污染”（用户错误的偏好被记住并强化）？

## 6. 实践建议

**如何应用：**
1.  **数据清洗：** 在接入 Knowledge Base 之前，必须清洗非结构化数据（PDF、网页），去除噪音。
2.  **Prompt 工程：** 利用 Bedrock 的 Prompt 管理功能，精心设计 System Prompt，明确 Agent 的角色和边界。
3.  **渐进式部署：** 先在内部环境测试，验证 RAG 的召回率，再面向公网用户。

**补充知识：**
*   学习 LangChain 或 LlamaIndex 的概念，虽然 Bedrock 封装了底层，但理解 RAG 原理有助于调试。
*   了解向量数据库的基本概念（如余弦相似度）。

## 7. 案例分析

**成功案例（假设性推演）：**
*   **案例：** 一个大型科技大会使用此架构构建助手。
*   **表现：** 以前用户需要搜索网页查找“AI 议程”，现在直接问“有哪些关于生成式 AI 的演讲？”。助手不仅列出清单，还根据用户之前的提问（“我对初创公司感兴趣”），优先推荐了相关主题的演讲。
*   **关键成功因素：** 优质的知识库数据（结构化的会议数据）+ 个性化记忆。

**失败反思：**
*   **场景：** 电商客服。
*   **问题：** 用户问“我的货在哪？”，Agent 虽然连接了知识库（退货政策），但没连接物流 API。
*   **教训：** AgentCore 必须配置正确的 Tools（API Schemas），仅有知识库是不够的，**知识（RAG）与行动（Tool Use）必须结合**。

## 8. 哲学与逻辑：论证地图

**中心命题：**
*   **Amazon Bedrock AgentCore 架构是构建生产级、个性化 AI 应用的最高效路径。**

**支撑理由：**
1.  **效率：** 托管服务消除了维护基础设施的复杂性（依据：云原生开发的普遍趋势及摘要中的 "quickly deploy"）。
2.  **准确性：** Knowledge Bases 通过 RAG 技术解决了大模型固有的幻觉问题（依据：检索增强生成的技术原理）。
3.  **个性化能力：** 记忆机制允许应用随时间演变，提供更好的用户体验（依据：摘要中提到的 "remembers... over time"）。

**反例 / 边界条件：**
1.  **成本敏感型场景：** 对于极小规模或对延迟极其敏感的应用，自建轻量级模型可能比 Bedrock 调用更便宜/更快。
2.  **数据主权限制：** 某些高度机密数据（如国家机密）严禁上传至公有云模型，此时无法使用 Bedrock。

**命题分类：**
*   **事实：** Bedrock 提供了 AgentCore 和 Knowledge Bases 组件。
*   **价值判断：** “高效”是相对于传统开发模式而言的。
*   **可检验预测：** 使用该架构开发的“活动助手”，其上线时间将比自建架构缩短 50% 以上，且回答准确率超过 90%。

**立场与验证：**
*   **立场：** 支持该命题，认为对于绝大多数中大型企业应用，这是目前的最佳实践。
*   **验证方式：**
    *   **指标：** 对比开发“从零开始”与“基于 Bedrock”的代码行数（LOC）和部署时间。
    *   **实验：** 构建两个相同的机器人，一个使用纯 Prompt Engineering，一个使用 Bedrock Knowledge Bases，使用相同的问题集测试幻觉率。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化知识库数据的检索质量

**说明**:
构建智能事件代理的核心在于其能够准确检索上下文信息。原始数据通常包含噪声、格式混乱或冗余信息，这会严重阻碍大型语言模型（LLM）准确提取相关内容。为了提高检索增强生成（RAG）系统的性能，必须在将数据摄入 Amazon Bedrock Knowledge Bases 之前，对原始数据进行清洗和结构化处理。

**实施步骤**:
1. **数据清洗与标准化**：在数据摄入阶段，去除 HTML 标签、特殊字符和无关页眉/页脚。将非结构化文本（如 PDF）转换为纯文本或 Markdown 格式，以提高分块效果。
2. **分块策略优化**：根据数据的语义结构（如段落、章节）进行分块，而不是简单地按字符数切割。确保每个分块包含足够的上下文信息，同时保持在模型的上下文窗口限制内。
3. **元数据过滤**：为每个文档或分块添加有意义的元数据（如日期、事件类型、作者），以便在检索时通过元数据过滤来缩小搜索范围，提高精度。

**注意事项**:
避免分块过大导致检索结果包含过多无关信息，或分块过小导致上下文缺失。建议针对特定类型的文档进行分块大小的 A/B 测试。

---

### 实践 2：实施高级检索策略（混合检索与重排序）

**说明**:
传统的向量检索虽然强大，但在处理精确匹配或特定领域术语时可能表现不佳。为了构建能够处理复杂事件（如 IT 运维事件或客户支持工单）的代理，应结合多种检索模式。混合检索结合了关键词搜索（BM25）和语义搜索（向量）的优势，而重排序机制则能进一步筛选出最相关的结果。

**实施步骤**:
1. **启用混合检索**：在 Amazon Bedrock Knowledge Bases 配置中，启用原生向量搜索与关键词搜索的混合模式。这有助于在处理缩略词、ID 号码或精确短语时提高召回率。
2. **配置重排序模型**：在检索步骤之后引入重排序模型。Bedrock 支持使用重排序机制对初始检索结果进行重新打分和排序，仅将 Top-K 个最相关的分块传递给 Agent。
3. **调整检索参数**：根据实际业务场景调整返回的文档数量，确保传递给 LLM 的上下文既充足又不会超出 Token 限制。

**注意事项**:
重排序步骤会增加轻微的延迟。需要在响应速度和检索准确率之间找到平衡点。对于对延迟极其敏感的应用，可考虑仅在复杂查询时启用重排序。

---

### 实践 3：设计精细化的 Agent 指令与提示词工程

**说明**:
Amazon Bedrock AgentCore 依赖于基础提示词来理解其角色、目标和约束条件。模糊的指令会导致 Agent 产生幻觉或偏离任务。为了确保 Agent 能够正确处理“事件”，必须在提示词中明确其职责范围、可用的工具以及输出格式。

**实施步骤**:
1. **定义明确的角色和目标**：在 Agent 配置的“Instructions”部分，清晰定义 Agent 的身份（例如：“你是一个资深的 IT 事件分析助手”），并详细描述其主要任务。
2. **规范输出格式**：强制要求 Agent 以特定的 JSON 或结构化格式输出结果，特别是当 Agent 的输出需要被下游系统自动解析时。
3. **设定边界与约束**：明确告知 Agent 在遇到无法解决的问题时应如何响应（例如：不要编造信息，而是声明知识库中未找到相关记录），并限制其只能使用已定义的 Action Groups。

**注意事项**:
提示词应尽可能简洁明了。过长的提示词会消耗大量的输入 Token 并可能稀释模型的注意力。建议使用迭代测试的方法不断优化提示词。

---

### 实践 4：构建可靠的 Action Groups 与工具调用逻辑

**说明**:
智能事件代理的最终价值通常在于执行操作（如调用 API 查询状态、创建工单或发送通知），而不仅仅是回答问题。Action Groups 是 Agent 实现这些操作的关键。最佳实践是确保 API 的定义清晰、参数完整，并且具备处理错误的能力。

**实施步骤**:
1. **清晰的 API Schema 定义**：使用 OpenAPI 规范（Swagger）定义 API 接口时，确保每个端点的描述、参数说明和示例数据都非常详细。这有助于 LLM 正确理解如何调用工具。
2. **参数验证与预处理**：在 Agent 调用后端 Lambda 函数时，应在代码逻辑中加入参数验证，防止 LLM 生成无效的参数导致 API 调用失败。
3. **实现用户确认机制**：对于具有“破坏性”或高风险的操作（如删除数据、发送大规模邮件），在 Agent 配置中要求必须经过用户确认才能执行 Action Group。

**注意事项**:
确保 Lambda 函数的执行时间设置合理，以避免因后端逻辑处理过慢导致 Agent 超时。同时，要注意 API 返回的错误信息应能被 Agent 理解并转化为自然语言反馈给用户。

---

###

---
## 学习要点

- 利用 Amazon Bedrock AgentCore 构建的事件智能体能够通过自主推理和工具调用，自动化地编排复杂工作流，从而替代传统的硬编码业务逻辑。
- 借助 Amazon Bedrock Knowledge Bases 为智能体配置 RAG（检索增强生成）能力，使其能够基于私有数据回答问题并有效减少模型幻觉。
- 通过 OpenAPI Schema 将企业内部 API 定义为工具，赋予智能体实时查询数据库或执行操作的能力，实现生成式 AI 与业务系统的深度集成。
- 利用 Amazon Bedrock 的“模型路由”功能，可以根据任务复杂度和成本要求，智能地将请求动态分配给最合适的基础模型。
- 采用“链式提示”和思维链设计模式，引导智能体将复杂任务分解为多个步骤，从而显著提高逻辑推理和最终输出的准确性。
- 基于无服务器架构构建智能体，能够利用云服务的弹性伸缩特性，自动应对业务访问量的波动，实现成本与性能的最优平衡。
- 在生产环境中实施严格的护栏机制和用户上下文隔离，是确保智能体应用安全、合规且防止数据泄露的关键措施。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [RAG](/tags/rag/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [个性化](/tags/%E4%B8%AA%E6%80%A7%E5%8C%96/) / [身份验证](/tags/%E8%BA%AB%E4%BB%BD%E9%AA%8C%E8%AF%81/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [利用 Amazon Bedrock 构建具备记忆与个性化能力的智能活动助手]({{< relref "posts/20260225-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-0.md" >}})
- [基于Amazon Bedrock AgentCore构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-12.md" >}})
- [利用 Amazon Bedrock AgentCore 构建统一智能系统]({{< relref "posts/20260220-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-13.md" >}})
- [基于 Amazon Bedrock 构建AI招聘系统优化人才获取流程]({{< relref "posts/20260215-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-8.md" >}})
- [基于Amazon Bedrock构建AI招聘系统优化人才获取流程]({{< relref "posts/20260217-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*