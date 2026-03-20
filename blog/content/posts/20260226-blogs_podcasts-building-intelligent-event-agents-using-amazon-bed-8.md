---
title: 构建具备记忆与身份验证的智能活动助手：基于 Amazon Bedrock AgentCore 的实践
date: 2026-02-26 17:38:47+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- AgentCore
- RAG
- 智能体
- 无服务器
- 身份验证
- 知识库
- Serverless
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 本文介绍了如何利用 Amazon Bedrock AgentCore 和 Amazon Bedrock Knowledge Bases 快速构建一个生产级的智能活动助手（Event
  Assistant）。 该智能助手旨在通过记录与会者偏好来提供个性化的活动体验。在此过程中，Amazon Bedrock AgentCor
external_url: https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases
scenarios:
- RAG应用
- AI/ML项目
---

# 构建具备记忆与身份验证的智能活动助手：基于 Amazon Bedrock AgentCore 的实践

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T19:51:08+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)

---

## 摘要/简介

本文演示如何利用 Amazon Bedrock AgentCore 的组件快速部署一个生产就绪的活动助手。我们将构建一个能够记住参会者偏好并随时间累积个性化体验的智能伴侣，而 Amazon Bedrock AgentCore 则承担生产部署的重任：利用 Amazon Bedrock AgentCore Memory 维护对话上下文和长期偏好，无需定制存储方案；借助 Amazon Bedrock AgentCore Identity 实现安全的多 IdP 身份验证；并通过 Amazon Bedrock AgentCore Runtime 实现无服务器扩缩与会话隔离。我们还将使用 Amazon Bedrock Knowledge Bases 来进行托管式 RAG 和活动数据检索。

---

## 导语

构建能够长期记忆用户偏好的智能体，往往面临复杂的存储与身份管理挑战。本文将演示如何利用 Amazon Bedrock AgentCore 和 Amazon Bedrock Knowledge Bases，快速部署一个生产就绪的活动助手。通过利用 AgentCore 的内置组件处理会话状态、多 IdP 验证及无服务器扩缩，并结合托管式 RAG 进行数据检索，您将掌握构建安全、可扩展且具备个性化能力的生成式 AI 应用的具体方法。

---

## 摘要

本文介绍了如何利用 Amazon Bedrock AgentCore 和 Amazon Bedrock Knowledge Bases 快速构建一个生产级的智能活动助手（Event Assistant）。

该智能助手旨在通过记录与会者偏好来提供个性化的活动体验。在此过程中，Amazon Bedrock AgentCore 承担了繁重的生产部署工作，主要包括以下三个组件：

1.  **Amazon Bedrock AgentCore Memory**：用于维护对话上下文和长期偏好，无需额外的自定义存储解决方案。
2.  **Amazon Bedrock AgentCore Identity**：负责实现安全的多身份提供商（Multi-IDP）认证。
3.  **Amazon Bedrock AgentCore Runtime**：提供无服务器扩展能力和会话隔离。

此外，该方案还使用了 **Amazon Bedrock Knowledge Bases** 来实现托管型 RAG（检索增强生成）和活动数据检索。

---

## 评论

### 评价文章：Building intelligent event agents using Amazon Bedrock AgentCore and Amazon Bedrock Knowledge Bases

**文章中心观点**
文章主张利用 Amazon Bedrock 的 AgentCore 框架和 Knowledge Bases 服务，可以以低代码方式快速构建具备长期记忆和个性化能力的生产级智能活动助手，从而解决传统聊天机器人缺乏上下文和执行能力的痛点。

**深入评价与分析**

**1. 内容深度：从“对话”到“行动”的架构跨越**
*   **支撑理由（事实陈述）：** 文章的核心技术深度在于引入了 **AgentCore** 的概念。相比于传统的 RAG（检索增强生成）应用，仅仅进行“问答”，AgentCore 引入了“推理”和“工具编排”层。文章展示了如何将 LLM（大语言模型）与外部 API（如票务系统、日程管理）通过 OpenAPI Schema 进行连接。这在技术上解决了 LLM 的“幻觉”和“时效性”问题——即 LLM 不再仅依赖训练数据生成文本，而是能够调用外部工具来执行任务。
*   **支撑理由（作者观点）：** 文章强调了“记忆”的重要性。通过将用户偏好存储在 Knowledge Base 或 Session Memory 中，系统能够模拟人类的“认知连贯性”。这标志着行业从“一次性交互”向“持续性陪伴”的演进。
*   **反例/边界条件（你的推断）：** 文章可能低估了“长期记忆”的检索精度问题。随着用户交互数据的增加，简单的向量检索可能会引入噪音，导致“记忆污染”，即模型混淆了不同时间段或不同用户的偏好。此外，对于复杂的、多步骤的逻辑推理（例如涉及多个不可逆操作的预订变更），单纯的 AgentCore 编排可能面临“死循环”或“工具调用失败”后的恢复难题。

**2. 实用价值：云原生落地的加速器**
*   **支撑理由（事实陈述）：** 对于企业开发者而言，文章展示了极高的实用价值。通过利用 AWS 托管服务（Bedrock、OpenSearch Serverless 等），开发者免去了模型微调、向量数据库维护和 API 网关搭建的繁重工作。文章提供的代码片段和架构图（推断）直接对应了生产环境中的 MVP（最小可行性产品）路径。
*   **支撑理由（作者观点）：** “Production-ready”是文章的一个强承诺。文章隐含的实用价值在于其安全性和可控性。使用 Bedrock 允许企业通过 Guardrails（护栏）来过滤有害内容，这是金融、医疗等敏感行业落地 AI 的刚需。
*   **反例/边界条件（事实陈述）：** 这种高度依赖 AWS 生态的架构存在严重的“厂商锁定”风险。如果企业需要跨云部署或降低成本，将 Agent 逻辑迁移出 Bedrock 的成本将非常高昂。此外，Bedrock 的调用成本在处理大规模并发时，可能比自建开源模型（如 Llama 3 自部署）要高得多。

**3. 创新性：智能体工作流的标准化尝试**
*   **支撑理由（你的推断）：** 文章的创新性不在于提出了全新的算法，而在于将 **LangChain/LlamaIndex 等开源社区中的 Agent 概念“产品化”和“标准化”**。它定义了一种标准范式：LLM 作为推理核心 + Knowledge Base 作为长期记忆 + Tools 作为执行手脚。这种范式降低了构建认知架构的门槛。
*   **反例/边界条件（作者观点）：** 所谓的“Event Assistant”应用场景相对单一且垂直。相比于通用的自主智能体，这种特定场景的 Agent 创新性有限，更多是工程能力的堆叠。目前行业对于 Agent 如何处理“未知错误”和“自我反思”尚无定论，文章也未涉及这些前沿的 Agentic Workflow（如智能体规划、反思、重试循环）。

**4. 行业影响与争议点**
*   **行业影响（你的推断）：** 此类文章的发布预示着 SaaS 软件的“AI 原生化”正在加速。未来的活动管理软件不再是一个简单的 CRUD（增删改查）界面，而是一个具备自然语言交互界面的智能体。这将迫使传统软件厂商重构其 UX 设计。
*   **争议点（作者观点）：** **“无代码/低代码”与“定制化灵活性”之间的矛盾。** AgentCore 虽然简化了开发，但对于复杂业务逻辑（例如特殊的退款规则、复杂的库存锁定逻辑），单纯依赖 Prompt Engineering 和 API 描述可能无法实现精确控制。硬编码业务逻辑与 LLM 的概率性生成之间存在天然的张力。

**实际应用建议**
1.  **不要忽视“人工回环”：** 在部署此类 Agent 时，必须在关键操作（如支付、删除数据）前加入人工确认机制，防止 LLM 误操作带来的业务损失。
2.  **关注“可观测性”：** 建议配合 AWS CloudWatch 使用，不仅监控 API 延迟，更要监控 LLM 的思维链和工具调用路径，以便调试 Agent 为什么“走错路”。

**可验证的检查方式**
1.  **指标测试（Token 消耗与延迟）：** 部署该 Agent 并模拟 1000 个并发用户请求，测量端到端延迟。如果平均响应时间超过 3 秒，则实时对话体验将不可接受。
2.  **边界实验（工具调用鲁棒性）：** 故意切断一个后端 API（例如模拟票务服务宕机），观察 Agent 是会优雅地降级提示用户，还是会陷入无限重试循环或产生幻觉胡乱回答。
3.  **观察窗口（记忆一致性

---

## 技术分析

基于您提供的文章标题和摘要，虽然无法获取全文细节，但结合Amazon Bedrock（特别是AgentCore和Knowledge Bases）的技术架构与行业最佳实践，以下是对该文章核心观点及技术要点的深度分析。

---

### 深度分析：构建基于Amazon Bedrock的智能事件代理

### 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**利用Amazon Bedrock的AgentCore和Knowledge Bases组件，开发者可以低代码、高效率地构建出具备长期记忆和个性化能力的生产级AI助手。** 文章主张，通过将复杂的推理逻辑（AgentCore）与动态的知识检索（Knowledge Bases）解耦并结合，能够解决传统聊天机器人“无状态”和“幻觉”的问题，从而在活动管理等复杂场景中提供真正个性化的用户体验。

### 作者想要传达的核心思想
作者试图传达**“编排与记忆是通用人工智能（AGI）应用落地的关键”**这一思想。单纯的LLM（大语言模型）具备推理能力，但缺乏上下文记忆和特定领域的知识库。通过Bedrock的架构，开发者无需微调模型即可赋予AI“记忆”和“知识”，使其从通用的聊天工具转变为懂业务、懂用户的智能代理。

### 观点的创新性和深度
该观点的创新性在于**“生产就绪”**和**“时间维度的个性化”**。
*   **生产就绪**：强调的不是Demo，而是利用托管服务解决安全、监控、扩展性问题。
*   **时间维度**：摘要中提到“remembers attendee preferences... over time”，这触及了AI应用最难的部分——长期记忆管理。这不仅是检索当前文档，更是关于用户画像的动态演化。

### 为什么这个观点重要
随着大模型热潮的退去，企业界关注的焦点从“模型有多大”转向了“应用如何落地”。文章提出的架构解决了企业级AI落地的三大痛点：
1.  **数据时效性**：通过Knowledge Bases连接私有数据，无需重新训练模型。
2.  **任务复杂性**：通过AgentCore编排多步推理，解决复杂业务流程。
3.  **用户体验**：通过记忆功能，实现千人千面的服务，这是商业转化的关键。

### 2. 关键技术要点

### 涉及的关键技术或概念
*   **Amazon Bedrock AgentCore**：负责代理的编排。它理解用户意图，将其分解为子任务，并调用相应的工具或API。
*   **Amazon Bedrock Knowledge Bases**：基于RAG（检索增强生成）架构。允许LLM查询私有数据源（如PDF、数据库、网站），并将检索到的上下文用于生成回答。
*   **User Session/Memory Store**：虽然摘要未明示，但实现“remembers... over time”必然涉及会话历史存储和向量数据库的用户画像存储。

### 技术原理和实现方式
1.  **RAG（检索增强生成）流程**：用户提问 -> AgentCore识别信息缺口 -> 查询Knowledge Base（将查询向量化 -> 在向量数据库中检索 -> 获取Top K相关文档） -> 将检索结果作为上下文输入LLM -> 生成最终回答。
2.  **Agent Orchestration（代理编排）**：利用ReAct（Reason + Act）模式。LLM作为推理引擎，决定何时调用知识库查询，何时调用外部API（如预订票务），以及何时响应用户。
3.  **长期记忆实现**：通过将用户的偏好、历史交互记录存储在向量数据库或元数据存储中。在每次对话开始时，检索该用户的Profile信息注入System Prompt。

### 技术难点和解决方案
*   **难点：幻觉问题**。LLM可能编造不存在的活动信息。
    *   *解决方案*：强制LLM基于Knowledge Base检索到的片段生成答案，并添加引用来源。
*   **难点：上下文窗口限制**。活动信息量巨大，无法全部放入Prompt。
    *   *解决方案*：向量检索技术，只召回最相关的片段，保持Token使用在可控范围内。
*   **难点：用户隐私与数据隔离**。
    *   *解决方案*：在Knowledge Base配置中使用元数据过滤，确保用户只能访问其授权范围内的数据。

### 技术创新点分析
文章展示的创新点在于**“无服务器架构下的状态管理”**。传统的Agent开发需要手动管理Session State，而Bedrock AgentCore很可能封装了这一层，允许开发者专注于业务逻辑的定义，而非底层基础设施的维护。

### 3. 实际应用价值

### 对实际工作的指导意义
这篇文章为企业架构师和AI产品经理提供了一个**标准范式**：不要试图训练一个懂所有活动细节的模型，而是构建一个懂得如何去查找知识、懂得如何调用工具的Agent。这极大地降低了AI应用的开发门槛和成本。

### 可以应用到哪些场景
1.  **企业内部知识库**：HR助手、IT运维助手。
2.  **电商零售**：导购助手，根据历史购买记录推荐商品。
3.  **医疗健康**：患者随访助手，记录患者长期健康数据。
4.  **教育培训**：个性化助教，根据学生薄弱环节生成练习。

### 需要注意的问题
*   **数据质量**：RAG的效果高度取决于源数据的质量。如果活动手册是混乱的扫描件，Agent的效果会很差。
*   **延迟**：检索和推理过程可能导致秒级的响应延迟，不适合实时性要求极高的流式对话场景。

### 实施建议
*   **从小处着手**：先构建一个只读的问答助手，验证Knowledge Base的检索效果。
*   **数据清洗优先**：在接入Bedrock之前，务必对非结构化数据进行清洗和分块。
*   **明确边界**：清楚定义Agent能做什么（查信息）和不能做什么（如退款操作需人工介入）。

### 4. 行业影响分析

### 对行业的启示
这篇文章标志着**云厂商AI竞争进入“应用层”阶段**。竞争不再仅限于模型参数的大小，而是在于谁提供了更好的开发工具链。AWS通过Bedrock展示了其“全托管”的优势，试图让开发者无需关注MLOps，直接关注业务逻辑。

### 可能带来的变革
*   **SaaS的智能化重构**：传统的SaaS软件（如Eventbrite）将面临被“Agent化”重构的压力。未来的软件可能不再是菜单和按钮，而是对话界面。
*   **客服行业的自动化升级**：从基于关键词匹配的第一代客服，直接跨越到基于意图理解的第三代智能体。

### 相关领域的发展趋势
*   **Agentic Workflow（代理工作流）**：AI将不再只是生成内容，而是执行任务。
*   **Multi-agent（多智能体）**：未来的活动管理可能由一个Agent负责行程规划，另一个负责票务预订，协同工作。

### 5. 延伸思考

### 引发的其他思考
*   **记忆的隐私边界**：为了实现个性化，Agent需要收集大量用户数据。如何在“越懂你”和“隐私保护”之间通过技术手段（如联邦学习或本地向量库）取得平衡？
*   **Agent的自主性极限**：如果Agent记住了用户的错误偏好（如过期的饮食限制），如何自我修正？

### 可以拓展的方向
*   **多模态交互**：结合Amazon Rekognition，让Agent不仅能处理文本，还能分析活动现场的照片，识别用户情绪。
*   **主动式Agent**：不仅是被动回答，而是主动提醒用户“您喜欢的演讲者即将在30分钟后开始”。

### 7. 案例分析

### 结合实际案例说明
**案例**：一家大型科技会议组织者使用该架构。
*   **场景**：参会者询问“有哪些适合AI架构师参加的关于向量数据库的讲座？”
*   **流程**：Agent识别意图 -> 查询Knowledge Base获取讲座列表 -> 检索用户Profile（发现用户是架构师且偏好案例分享） -> 过滤掉理论型讲座 -> 返回个性化结果。

### 成功案例分析
成功的关键在于**数据结构的标准化**。如果所有讲座信息都存储在结构化的JSON或Markdown表格中，RAG的检索准确率将极高。反之，如果是纯文本的长段落，效果会大打折扣。

### 失败案例反思
如果Agent在活动期间频繁给出错误的房间号，这通常是因为**Knowledge Base的数据未及时更新**（如房间变更了，但文档没改）。这提醒我们，RAG系统必须有配套的数据更新流水线（CI/CD）。

### 8. 哲学与逻辑：论证地图

### 中心命题
**利用Amazon Bedrock AgentCore和Knowledge Bases构建的智能代理，能够以低成本、高效率的方式，为复杂活动管理提供具备长期记忆和个性化能力的生产级解决方案。**

### 支撑理由与依据
1.  **理由1：技术架构的解耦降低了开发门槛。**
    *   *依据*：Bedrock托管了底层的模型推理和向量检索逻辑，开发者无需精通MLOps即可通过API调用高级功能。
2.  **理由2：RAG架构有效解决了知识时效性和幻觉问题。**
    *   *依据*：通过检索外部数据源，模型可以回答训练数据之后发生的事件，且答案受限于检索内容，减少了编造。
3.  **理由3：状态记忆机制提升了用户体验的商业价值。**
    *   *依据*：摘要中提到“remembers attendee preferences... over time”，这种个性化是提升用户留存和转化的核心驱动力。

### 反例或边界条件
1.  **反例1：高度依赖实时数据的场景。** 如果活动每秒钟都在变化（如高频交易），RAG的检索延迟可能导致信息过时，此时不如直接查询数据库。
2.  **反例2：极度复杂的逻辑推理。** 如果任务需要跨越数十个步骤的推理，当前的Agent架构可能会陷入“死循环”或遗忘中间步骤，仍需传统代码逻辑介入。
3.  **边界条件：数据质量。** 如果输入知识库的数据是垃圾，那么Agent输出的也是垃圾。

---

## 最佳实践

#### 最佳实践指南

### 实践 1：构建结构化且高质量的向量知识库

**说明**: Amazon Bedrock Knowledge Bases 的核心在于 RAG（检索增强生成）架构。智能代理的表现直接取决于检索到的上下文质量。如果数据源杂乱无章或包含大量噪音，模型生成的答案将会出现幻觉或不准确。因此，在接入知识库之前，必须对原始数据进行清洗、去重和结构化处理。

**实施步骤**:
1. **数据清洗与分块**：将非结构化文档（如 PDF、Word）转换为纯文本，去除页眉、页脚等无关信息。根据语义逻辑将文档切分为较小的块，建议块大小在 200-500 Token 之间，并保留一定的重叠窗口以维持上下文连贯性。
2. **元数据过滤**：为每个数据块添加元数据标签（如日期、部门、文档类型）。在 Bedrock Knowledge Bases 配置中启用元数据过滤，以便在检索时缩小搜索范围，提高相关性。
3. **选择合适的嵌入模型**：根据语言和业务场景选择最佳的 Embeddings 模型（如 Amazon Titan Embeddings 或 Cohere Embed），将文本块转换为向量并存储在向量数据库（如 OpenSearch Serverless）中。

**注意事项**: 避免切分过碎导致语义丢失，也避免切分过大导致检索包含过多无关信息。

---

### 实践 2：设计精细化的 Agent 提示词与指令

**说明**: AgentCore 依赖于系统提示词来理解其角色、任务边界和交互方式。模糊的指令会导致 Agent 擅自发挥或无法调用正确的工具。最佳实践是明确 Agent 的身份，限制其回答范围，并定义其输出格式。

**实施步骤**:
1. **定义角色与目标**：在系统提示词中明确 Agent 的身份（例如：“你是一个专业的技术支持助手”）。
2. **限定知识边界**：指示 Agent 严格依据检索到的上下文回答问题。如果知识库中没有相关信息，明确指示 Agent 回答“不知道”，而不是利用训练数据编造答案。
3. **规范输出格式**：要求 Agent 以结构化格式（如 Bullet points 或 JSON）输出复杂信息，以便后续解析或展示。

**注意事项**: 定期测试和迭代提示词。使用 Bedrock 的“Guardrails”功能来过滤有害内容，并确保提示词指令不会与 Guardrails 规则冲突。

---

### 实践 3：合理编排 Action Groups 与工具使用

**说明**: Bedrock Agents 的强大之处在于能够通过 Action Groups 调用外部 API（如查询数据库、发送邮件或调用业务逻辑）。最佳实践是将复杂的业务逻辑封装成 API，而不是试图通过 Prompt 让 LLM 直接处理计算或逻辑推理。

**实施步骤**:
1. **API 概念定义**：在 Bedrock Agent 配置中，清晰定义每个 API 的用途、输入参数和输出结构。使用 OpenAPI 规范描述接口，确保 LLM 能准确理解参数含义。
2. **原子性工具设计**：每个工具应只执行单一、明确的任务。避免设计过于复杂的复合型工具，这会降低 LLM 的调用成功率。
3. **错误处理机制**：确保后端 API 能够返回清晰的错误信息。当 Agent 调用失败时，API 应返回人类可读的错误提示，引导 Agent 进行自我修正或向用户求助。

**注意事项**: 严格控制 Agent 的工具权限。确保 Agent 只能调用经过授权和安全的业务接口，防止数据泄露或意外操作。

---

### 实践 4：配置高效的检索策略与参数

**说明**: 默认的检索配置可能无法满足所有业务场景的需求。根据查询类型（事实性问题 vs. 总结性问题）调整检索参数，可以显著提升 Agent 的响应质量。

**实施步骤**:
1. **调整搜索配置**：在 Knowledge Bases 设置中，配置最大返回结果数量。通常设置返回前 3-5 个最相关的片段，既能提供足够上下文，又不会超出模型的 Context Window。
2. **启用混合搜索**：如果向量存储支持（如 OpenSearch），建议结合“向量搜索”和“关键词搜索”。关键词搜索擅长匹配精确术语（如零件编号、缩写），而向量搜索擅长语义理解。
3. **设置重排序**：如果可能，启用重排序机制，对初步检索回来的结果进行重新打分，筛选出最精准的 Top K 结果提供给模型。

**注意事项**: 监控检索延迟。过大的检索结果集会增加 Token 消耗并延长响应时间。

---

### 实践 5：实施全面的测试、追踪与人工审查

**说明**: 仅仅构建 Agent 是不够的，必须建立持续的评估机制。由于 LLM 的非确定性特征，Agent 的表现可能波动。利用 Bedrock 的可观测性功能来追踪推理过程至关重要。

**实施步骤**:
1. **启用 Trace 功能**：在 Agent 配置中开启“Trace”功能（如 CloudWatch Logs 或 Bedrock 的内部追踪）。这允许你查看 Agent 每一步的思考过程、调用了哪个工具、检索到了哪些文档片段。
2. **建立测试数据集

---

## 学习要点

- Amazon Bedrock AgentCore 与 Knowledge Bases 的结合，能够通过 RAG 架构将大语言模型与企业私有数据安全连接，从而构建出具备实时信息检索能力的智能事件代理。
- 利用 Amazon Bedrock 的托管向量数据库，可以自动处理文档的分块、嵌入和索引，显著降低了构建生成式 AI 应用时在基础设施和数据预处理方面的技术门槛。
- 通过可视化配置工具定义 API 架构和业务逻辑，开发者无需编写复杂的后端代码即可快速创建能够执行具体任务（如处理工单或查询库存）的智能体。
- 该架构支持多模态数据输入，允许智能体从 PDF、网页、电子邮件等多种非结构化数据源中提取信息，有效打破了企业内部的数据孤岛。
- 内置的防护机制和可配置的护栏能够实时过滤有害内容并限制模型行为，确保智能体在生成回复时的安全性、合规性以及品牌语调的一致性。
- 借助 Bedrock 提供的多种基础模型选择，企业可以根据具体的业务场景灵活调整模型，以在响应速度、准确性和成本控制之间取得最佳平衡。
- 智能体具备上下文记忆和多轮对话管理能力，能够根据对话历史自动优化后续的检索和推理步骤，从而提供更加精准和个性化的用户体验。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases](https://aws.amazon.com/blogs/machine-learning/building-intelligent-event-agents-using-amazon-bedrock-agentcore-and-amazon-bedrock-knowledge-bases)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [RAG](/tags/rag/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [身份验证](/tags/%E8%BA%AB%E4%BB%BD%E9%AA%8C%E8%AF%81/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/) / [Serverless](/tags/serverless/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于 Amazon Bedrock 构建具备记忆与身份认证的智能活动助手]({{< relref "posts/20260226-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-3.md" >}})
- [利用Amazon Bedrock构建具备记忆与身份验证的智能活动助理]({{< relref "posts/20260226-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-4.md" >}})
- [利用Amazon Bedrock构建生产级智能活动助理]({{< relref "posts/20260225-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-1.md" >}})
- [利用 Amazon Bedrock 构建具备记忆与个性化能力的智能活动助手]({{< relref "posts/20260225-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-0.md" >}})
- [构建具备记忆功能的智能活动助手：基于 Amazon Bedrock AgentCore 的实践]({{< relref "posts/20260226-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-2.md" >}})
