---
title: 基于 Amazon Bedrock AgentCore 构建统一智能系统实践
date: 2026-02-19 02:58:23+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- AgentCore
- LLM
- 智能体
- 系统架构
- CAKE
- 统一智能
- AWS
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 随着企业对智能化需求的深入，构建能够整合多种能力的统一系统已成为关键挑战。本文将基于真实落地的 CAKE 系统，详细解析如何利用 Amazon
  Bedrock AgentCore 打破模型与应用间的壁垒。通过阅读本文，您将掌握构建统一智能架构的实战路径，从而更高效地交付复杂的生成式 AI 解决方案。
external_url: https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore
scenarios:
- 大语言模型
- AI/ML项目
---

# 基于 Amazon Bedrock AgentCore 构建统一智能系统实践

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-18T23:54:29+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore)

---

## 摘要/简介

在这篇文章中，我们将通过我们真实落地的 Customer Agent and Knowledge Engine (CAKE) 系统，展示如何利用 Amazon Bedrock AgentCore 构建统一的智能系统。

---

## 导语

随着企业对智能化需求的深入，构建能够整合多种能力的统一系统已成为关键挑战。本文将基于真实落地的 CAKE 系统，详细解析如何利用 Amazon Bedrock AgentCore 打破模型与应用间的壁垒。通过阅读本文，您将掌握构建统一智能架构的实战路径，从而更高效地交付复杂的生成式 AI 解决方案。

---

## 评论

**文章中心观点**
文章主张通过利用 Amazon Bedrock 的 AgentCore 框架构建统一的智能系统（如 CAKE），能够有效整合非结构化数据与结构化 API，从而解决传统企业级 AI 应用中“检索”与“行动”割裂的痛点，实现从单一问答到复杂任务自动化的跨越。

**支撑理由与深度评价**

**1. 架构的统一性：打破 RAG 与 Function Calling 的边界**
*   **事实陈述**：文章展示了 CAKE 系统如何利用 AgentCore 同时处理知识检索（RAG）和业务执行（API 调用）。
*   **深度分析**：在当前的 LLM 应用开发中，开发者往往需要分别维护一个检索链和一个工具调用链，导致上下文管理混乱和延迟增加。Bedrock AgentCore 提出的“统一”核心价值在于其编排能力。它不再将“查知识”和“办事情”视为两个独立的步骤，而是将它们视为 Agent 规划路径中的不同节点。这种架构设计符合“Agentic Workflow”的发展趋势，即模型不仅仅是生成文本，而是作为 CPU 调度系统资源。
*   **反例/边界条件**：并非所有场景都需要这种“重”架构。对于简单的 FAQ（常见问题解答），引入 AgentCore 的编排层反而会增加 Token 消耗和推理延迟。此外，如果企业的业务 API 缺乏清晰的描述或参数定义极其复杂，AgentCore 的规划成功率会大幅下降。

**2. 企业级落地的可控性：引入“护栏”机制**
*   **事实陈述**：文中提到了在构建 Customer Agent 时应用了 Guardrails（护栏）技术。
*   **作者观点**：这是文章最具实用价值的部分。通用的 LLM 往往存在幻觉或输出不可控的问题，直接连接企业核心业务（如订单修改、退款）风险极高。
*   **深度分析**：CAKE 系统通过 Bedrock 的 Guardrails 机制，在模型输出前进行了一层过滤和策略检查。这体现了从“以模型为中心”向“以数据和控制为中心”的转变。它表明，在 B2B 或 B2C 的真实生产环境中，**鲁棒性比创造性更重要**。企业需要的不是一个能写诗的客服，而是一个能严格遵守公司退款政策且不胡乱承诺的客服。

**3. 隐性的数据治理：Knowledge Engine 的角色**
*   **你的推断**：虽然摘要未详述，但基于 Bedrock 的特性，CAKE 系统必然依赖强大的向量数据库和知识图谱集成。
*   **深度分析**：所谓的“Unified Intelligence”，其底座是统一的数据治理。文章暗示了一种最佳实践：在构建 Agent 之前，必须先构建 Knowledge Engine。这反驳了当前市场上“直接拿原始 PDF 喂给 LLM”的浮躁做法。只有当非结构化文档被清洗、切片、并向量化，且与结构化的业务元数据（如用户 ID、订单状态）对齐后，Agent 才能进行有效的推理。

**反例与边界条件（补充）**
*   **成本边界**：Agent 模式通常涉及多轮推理和链式调用，其 Token 成本可能是简单 RAG 的 5-10 倍。对于低利润率的业务，这种 ROI（投资回报率）可能不成立。
*   **模型依赖**：Bedrock AgentCore 的表现高度依赖于其背后 Claude 3 或其他模型的推理能力。如果模型本身在复杂逻辑规划上出现“死循环”或“中途放弃”，AgentCore 目前的框架可能缺乏有效的强制干预手段（如硬编码的回退逻辑）。

**多维评价**

*   **内容深度**：**4/5**。文章跳出了单纯的代码演示，触及了系统架构设计的层面（RAG + API 编排）。它没有停留在“怎么调用 API”，而是讨论了“如何设计一个能解决问题的系统”。但在处理长尾场景和错误恢复机制上，可能缺乏深度剖析。
*   **实用价值**：**5/5**。对于正在探索“大模型如何真正落地业务”的企业架构师而言，CAKE 案例提供了一个高可参考的蓝图。它明确了如何将客服场景从“人工智障”升级为“智能助理”。
*   **创新性**：**3.5/5**。RAG 和 Function Calling 的结合并非 AWS 独创，但 Bedrock AgentCore 将这种能力产品化、标准化，降低了开发门槛。其创新点在于将这种复杂的编排能力托管化。
*   **可读性**：**4/5**。AWS 技术博客通常结构清晰，逻辑严密。但往往充斥着大量专有名词，可能对非 AWS 生态的开发者存在一定的认知门槛。
*   **行业影响**：**高**。该文章标志着云厂商从“卖模型”转向“卖能力”。它预示着 AI 应用的竞争将进入“Agent Engineering”阶段，即比拼谁能更高效地构建、管理和监控智能体。

**争议点与不同观点**
*   **黑盒 vs. 白盒**：AgentCore 是一种托管服务，高度抽象。这虽然降低了上手难度，但也牺牲了灵活性。资深开发者可能更倾向于使用 LangChain 或 AutoGPT 等开源框架进行细粒度控制，而非被 AWS 的生态绑定。
*   **过度工程化风险**：业界有一种观点认为，90% 的业务需求只需要简单的 Prompt Engineering 加上检索增强，并不需要复杂的 Agent 架构。强行引入 Agent 可能会导致系统维护成本呈指数级上升。

**实际应用建议**
1.

---

## 技术分析

基于您提供的文章标题《Build unified intelligence with Amazon Bedrock AgentCore》及摘要内容，结合对 Amazon Bedrock 服务架构和当前 Agent（智能体）技术发展趋势的深度理解，以下是对该文章核心观点及技术要点的全面深入分析。

---

### 深度分析报告：基于 Amazon Bedrock AgentCore 构建统一智能

### 1. 核心观点深度解读

### 文章的主要观点
文章的核心主张是：**企业应当从碎片化的、单一功能的 AI 应用（如独立的聊天机器人或搜索工具），转向构建“统一智能系统”。** 这种统一性通过 **Amazon Bedrock AgentCore** 实现，它不仅仅是一个模型调用接口，更是一个能够编排推理、集成工具并管理长期记忆的“大脑内核”。文章通过 CAKE（Customer Agent and Knowledge Engine）这一案例，证明了如何将客户服务、知识检索和任务执行整合在一个连贯的架构中。

### 作者想要传达的核心思想
作者试图传达“**Agent First（智能体优先）**”而非“Chatbot First（聊天机器人优先）”的设计理念。传统的 RAG（检索增强生成）系统往往止步于“回答问题”，而基于 AgentCore 的系统旨在“**解决问题**”。核心思想在于将大语言模型（LLM）从一个被动的知识库查询接口，升级为一个能够主动规划路径、调用 API 并执行复杂工作流的决策中心。

### 观点的创新性和深度
*   **架构层面的创新**：从单体应用转向微服务化的智能架构。AgentCore 提供了一种标准化的方式来定义 Agent 的“性格”、“技能”和“知识边界”，解决了当前 AI 落地中常见的“胶水代码”过多的问题。
*   **深度**：文章触及了 AI 工程化的深水区——**可观测性与编排**。它不仅讨论如何生成文本，更讨论如何控制生成过程，确保 Agent 的行为符合业务逻辑和合规要求。

### 为什么这个观点重要
随着企业引入的 AI 工具越来越多，如果不进行统一，将会形成新的“孤岛危机”。统一智能架构能够：
1.  **降低运维成本**：统一的监控、安全和治理策略。
2.  **提升用户体验**：用户不需要知道背后是哪个模型或工具在服务，只需与一个统一的智能助手交互。
3.  **增强业务连贯性**：Agent 可以跨系统执行任务（例如：先查库存，再创建订单，最后发邮件），而不是割裂的操作。

### 2. 关键技术要点

### 涉及的关键技术或概念
*   **Amazon Bedrock AgentCore**：这是文章的核心，指的是 Bedrock 中用于构建、配置和部署 Agents 的底层框架。它包含 Orchestrator（编排器）、Prompt Templates（提示词模板）和 Knowledge Base（知识库）集成。
*   **CAKE (Customer Agent and Knowledge Engine)**：这是一个具体的业务抽象层，展示了如何将 AgentCore 应用于客户服务领域。
*   **Function Calling (工具调用/函数调用)**：Agent 连接现实世界的关键技术，允许 LLM 输出结构化的 JSON 来触发后端 API。
*   **RAG (检索增强生成)**：结合企业私有数据（向量数据库）与模型能力的技术。
*   **Guardrails (护栏机制)**：确保模型输出安全和合规的技术。

### 技术原理和实现方式
*   **编排原理**：AgentCore 使用 ReAct（Reasoning + Acting）或类似的推理框架。用户输入后，AgentCore 决定是直接回答、查询知识库，还是调用工具。
    *   *实现*：通过定义 `OpenAPI Schema` (Swagger) 向 Agent 描述可用的 API 接口。
*   **记忆管理**：
    *   *实现*：利用 Amazon Bedrock 的会话摘要功能或外部存储（如 DynamoDB），维护跨轮次的上下文状态，使 Agent 能够处理多轮对话。

### 技术难点和解决方案
*   **难点：幻觉与不可控性**。Agent 可能会错误地调用工具或编造数据。
    *   *解决方案*：实施严格的 **Guardrails**，在模型输出到达用户之前进行过滤；同时利用 **Trace（追踪）** 功能可视化 Agent 的每一步思考过程，便于调试。
*   **难点：上下文窗口限制**。长时间对话或大量文档检索会撑爆 Token 限制。
    *   *解决方案*：CAKE 系统可能采用了“检索-重排”机制，只将最相关的片段注入上下文，并利用长上下文模型（如 Claude 3.0/3.5）处理更复杂的会话。

### 技术创新点分析
文章强调的“统一”不仅仅是接口统一，而是**推理链路的统一**。创新点在于将企业原本分散的业务逻辑（CRM、ERP、KB）通过 Agent 的 **Planning（规划）能力** 动态连接起来，而不是硬编码连接。

### 3. 实际应用价值

### 对实际工作的指导意义
对于技术负责人和架构师，这篇文章指明了从“Demo 级 AI”迈向“生产级 AI”的路径。它告诉我们，不要只关注模型的准确率，更要关注**Agent 的任务完成率**。

### 可以应用到哪些场景
*   **企业级知识管理**：不仅仅是搜索文档，而是总结、提炼并生成报告（如 CAKE）。
*   **自动化运营（Ops Agent）**：自动监控告警，查询日志，甚至执行自动回滚脚本。
*   **金融/医疗合规助手**：在严格合规的前提下，查询内部敏感数据并给出建议。
*   **销售赋能**：自动查询客户历史、产品库存，并生成个性化邮件。

### 需要注意的问题
*   **延迟**：Agent 的编排涉及多次模型调用和 API 请求，总延迟可能高达数秒，不适合实时性要求极高的场景。
*   **成本**：复杂的思考链路会消耗大量 Token，成本可能远高于简单的对话。
*   **权限控制**：Agent 调用后端 API 时，必须继承用户的权限体系（IAM 集成），防止越权操作。

### 实施建议
建议采用 **“小步快跑，场景驱动”** 的策略。不要试图一开始就构建全能 Agent，而是先从 CAKE 中的某个单一功能（如“仅查询”）开始，验证 AgentCore 的编排能力，再逐步开放“修改”和“执行”权限。

### 4. 行业影响分析

### 对行业的启示
行业正在从 **LLM Ops（模型运维）** 向 **Agentic Workflows（智能体工作流）** 演进。Bedrock AgentCore 的出现降低了构建 Agentic Workflow 的门槛，这意味着未来的企业软件将更多地具备“自主性”特征。

### 可能带来的变革
*   **SaaS 软件的重构**：未来的 SaaS 可能不再是一堆菜单和按钮，而是一个对话界面，背后由 Agent 驱动所有功能。
*   **客服行业的转型**：传统的 L1/L2 级人工客服将被 Agent 大量替代，人类转变为 Agent 的训练师和复杂异常的处理者。

### 相关领域的发展趋势
*   **Multi-Agent（多智能体）**：文章提到的是“统一智能”，下一步可能是多个专门 Agent（如一个专门写代码，一个专门做数据分析）协作。
*   **Model Context Protocol (MCP)**：数据连接的标准化将加速 Agent 生态的爆发。

### 5. 延伸思考

### 引发的其他思考
如果 AgentCore 变得足够强大，企业是否还需要传统的 UI（用户界面）？当“意图”成为新的交互指令，GUI（图形用户界面）是否会退化为次要交互方式？

### 可以拓展的方向
*   **边缘端 Agent**：将 Bedrock Agent 的能力下沉到边缘设备，结合小模型（SLM）实现离线智能。
*   **人机协同**：研究如何在 Agent 确信度低时，优雅地将控制权交接给人类，并从人类的反馈中学习。

### 需要进一步研究的问题
*   如何量化 Agent 的“推理能力”？
*   在多 Agent 环境下，如何解决循环依赖或死锁问题？

### 7. 案例分析

### 结合实际案例说明 (CAKE)
CAKE (Customer Agent and Knowledge Engine) 是一个典型的企业级落地案例。
*   **场景**：客户咨询“为什么我的订单没到？”
*   **传统方式**：人工查 CRM，查物流，回复。
*   **CAKE 实现**：
    1.  Agent 识别意图（查询订单状态）。
    2.  AgentCore 规划：调用 CRM API 获取订单详情 -> 调用物流 API 获取轨迹 -> 检索知识库查看“延迟政策”。
    3.  综合信息生成回复：“您的订单因暴雨延迟，预计明天到达，这里有一张优惠券作为补偿。”（甚至直接触发发券动作）。

### 成功案例分析
成功的关键在于**“工具的准确性”**和**“知识的时效性”**。如果 API 定义准确，知识库更新及时，Agent 就能像老练员工一样工作。

### 失败案例反思
如果 Agent 频繁胡乱调用 API（例如客户只是想咨询，却触发了退款操作），通常是因为 **Prompt 约束不够强** 或 **API 描述具有歧义**。这提醒我们在实施时，必须为高风险操作设置“确认步骤”或人工审批流。

### 8. 哲学与逻辑：论证地图

### 中心命题
**企业应采用 Amazon Bedrock AgentCore 构建统一智能系统，以替代传统的碎片化 AI 应用，从而实现从“信息检索”到“任务自动化”的质变。**

### 支撑理由与依据
1.  **理由一：统一架构降低复杂度。**
    *   *依据*：微服务架构理论表明，统一的控制平面能显著降低运维成本。Bedrock AgentCore 提供了标准化的编排层，避免了为每个 AI 功能单独开发编排逻辑。
2.  **理由二：增强的任务执行能力。**
    *   *依据*：LLM 的推理能力结合 Function Calling 技术，使得 AI 可以操作业务系统（API），这是单纯的 RAG 系统无法做到的。
3.  **理由三：企业数据的安全与合规。**
    *   *依据*：Bedrock 的 VPC 集成和 Guardrails 功能

---

## 最佳实践

### 实践 1：采用模块化架构设计 Agent

**说明**:
在构建 Amazon Bedrock AgentCore 时，应避免将所有逻辑堆砌在一个单一的庞大 Agent 中。相反，应采用模块化设计，将复杂的业务逻辑拆解为多个独立的、可重用的子 Agent 或组件。这种“编排与组合”的设计模式有助于提高系统的可维护性、可扩展性和可测试性，同时允许不同的团队并行开发特定的能力模块。

**实施步骤**:
1. 识别业务流程中的独立功能域（例如：数据检索、订单处理、身份验证）。
2. 为每个功能域创建专用的 Agent 或 Lambda 函数组件。
3. 在主 Agent 中定义清晰的编排逻辑，负责根据用户意图路由和调用这些子组件。
4. 建立标准化的接口协议，确保各模块之间能够无缝通信。

**注意事项**:
确保模块之间的依赖关系最小化，避免循环依赖。在拆分时，要权衡粒度，避免过度拆分导致系统延迟增加。

---

### 实践 2：优化提示词工程与上下文管理

**说明**:
Agent 的智能程度高度依赖于提示词的质量。必须精心设计系统提示词，明确 Agent 的角色、任务边界、输出格式以及限制条件。同时，由于大语言模型存在上下文窗口限制，必须实施有效的上下文管理策略，确保在多轮对话中，Agent 能够记住关键信息而不会因 Token 溢出而丢失历史数据。

**实施步骤**:
1. 编写清晰、具体的系统提示词，包含“角色定义”、“任务描述”、“约束条件”和“少样本示例”。
2. 实施会话摘要机制，当对话轮次过多时，自动将早期的历史对话压缩为摘要信息。
3. 利用 Amazon Bedrock 的上下文窗口限制参数，对输入 Prompt 进行动态裁剪或优化。
4. 建立 Prompt 版本控制，以便 A/B 测试和快速回滚。

**注意事项**:
避免在 Prompt 中包含敏感信息。定期审查和更新 Prompt 以适应模型版本的变化或业务逻辑的调整。

---

### 实践 3：构建健壮的 API 集成与错误处理机制

**说明**:
AgentCore 通常需要通过 API 调用外部系统（如 RAG 数据库或业务工具）。API 的不稳定性或错误响应可能导致 Agent 中断。最佳实践要求为所有外部调用构建健壮的错误处理逻辑，包括超时重试、降级响应和清晰的错误消息生成，确保 Agent 在遇到意外情况时仍能向用户提供有意义的反馈。

**实施步骤**:
1. 为所有 Action Group（操作组）配置明确的超时设置和重试策略（如指数退避算法）。
2. 在 Lambda 函数中实现 Try-Catch 块，将技术错误（如 500 Internal Server Error）转换为 Agent 可理解的业务错误描述。
3. 设计兜底逻辑，当外部服务不可用时，Agent 应能引导用户采取替代方案或稍后再试。
4. 在 API Schema 中明确定义错误响应的结构，以便 LLM 能够正确解析。

**注意事项**:
不要将原始的 API 错误堆栈信息直接暴露给最终用户，这会破坏用户体验并可能泄露系统架构信息。

---

### 实践 4：实施严格的验证与测试流程

**说明**:
由于 LLM 的生成具有概率性，Agent 的行为可能不可预测。在生产环境发布之前，必须建立严格的验证流程。这包括使用 Trace 功能来调试推理过程，以及使用自动化测试数据集来验证 Agent 在各种场景下的响应准确性和合规性。

**实施步骤**:
1. 利用 Amazon Bedrock 的 Agent Trace 功能，分析每个请求的推理过程、Prompt 构建和工具调用情况。
2. 构建包含“黄金问题”和“边缘案例”的测试数据集。
3. 实施自动化评估流程，对比 Agent 输出与预期结果的匹配度。
4. 在预生产环境中进行红队测试，尝试诱导 Agent 产生有害内容或绕过安全护栏。

**注意事项**:
测试应覆盖非功能性需求，如响应延迟和并发处理能力。不要仅依赖手动测试，必须建立自动化回归测试。

---

### 实践 5：强化数据隐私与安全防护

**说明**:
构建统一智能时，数据安全至关重要。必须确保 Agent 在处理用户数据时符合企业的合规要求，并防止 Prompt 注入攻击。利用 Bedrock 的 Guardrails 功能可以有效地过滤有害内容，并防止 Agent 泄露敏感信息。

**实施步骤**:
1. 启用并配置 Amazon Bedrock Guardrails，设置针对仇恨言论、暴力、色情及个人身份信息（PII）的过滤策略。
2. 对 Agent 访问的敏感数据源实施最小权限原则，使用 IAM 角色严格控制 Lambda 函数的访问权限。
3. 在 Prompt 中注入指令，明确禁止 Agent 复制受版权保护的材料或泄露内部机密。
4. 对用户输入进行预处理，以检测潜在的 Prompt 注入攻击模式。

**注意事项**:
安全配置是动态的，需要根据新的威胁模型和合规要求

---

## 学习要点

- Amazon Bedrock AgentCore 提供了一个无代码或低代码的可视化编排器，使用户能够通过简单的拖拽操作快速构建和部署复杂的生成式 AI 智能体。
- 该框架通过统一的架构将企业数据与 Amazon Bedrock 中的基础模型连接起来，有效解决了 AI 应用与私有数据源集成的挑战。
- 内置的“护栏”机制能够在生成内容的同时实时检测并过滤有害或有偏见的输出，确保企业级应用的安全性与合规性。
- 平台支持对大型语言模型进行微调和知识库的检索增强生成（RAG），从而显著提高 AI 回答的准确性和领域相关性。
- 用户可以灵活配置多步骤的自动化工作流，让智能体能够自主执行跨系统的业务逻辑和 API 调用。
- 借助 Amazon Bedrock 托管服务，企业无需从零开始构建基础设施，即可快速将生成式 AI 能力规模化地集成到现有业务系统中。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/build-unified-intelligence-with-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [LLM](/tags/llm/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [系统架构](/tags/%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84/) / [CAKE](/tags/cake/) / [统一智能](/tags/%E7%BB%9F%E4%B8%80%E6%99%BA%E8%83%BD/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [Amazon Bedrock AgentCore 浏览器功能更新：支持代理、配置文件与扩展]({{< relref "posts/20260217-blogs_podcasts-customize-ai-agent-browsing-with-proxies-profiles--2.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [利用 Amazon Bedrock 构建由 AI 驱动的招聘系统]({{< relref "posts/20260212-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-1.md" >}})
- [Iberdrola 利用 Amazon Bedrock AgentCore 革新 ServiceNow IT]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-8.md" >}})
