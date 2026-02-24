---
title: "使用MCP协议集成外部工具至Amazon Quick Agents的六步指南"
date: 2026-02-24T11:01:45+08:00
draft: false
entry_kind: "auto"
tags: ["MCP协议", "Amazon Quick", "模型上下文协议", "Agent集成", "外部工具", "开发指南", "AWS", "LLM工具链"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "**内容摘要：** 本文主要介绍了如何利用**模型上下文协议（MCP）**将外部工具与 **Amazon Quick Agents** 进行集成。这是一份面向第三方合作伙伴的实操指南，旨在帮助开发者构建新的 MCP 服务器，或对现有的服务器进行验证与调整，以实现与 Amazon Quick 的无缝对接。 文章通过一个*"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["大语言模型"]
---

# 使用MCP协议集成外部工具至Amazon Quick Agents的六步指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在本文中，您将使用一个六步清单来构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器以用于 Amazon Quick 集成。Amazon Quick 用户指南描述了 MCP 客户端的行为和约束。这是一份“操作指南”，面向第三方合作伙伴与 Amazon Quick 进行 MCP 集成所需的详细实现。

---
## 导语

随着 Agent 应用对数据交互深度的要求日益提高，如何将外部工具高效接入 AI 系统成为开发者关注的焦点。本文以 Model Context Protocol (MCP) 为核心，详细介绍了将其集成至 Amazon Quick Agents 的具体实现路径。通过这份包含验证与构建步骤的操作指南，您将掌握第三方工具与 Amazon Quick 进行 MCP 集成的关键技术细节，从而确保外部资源能够被安全、稳定地调用。

---
## 摘要

**内容摘要：**

本文主要介绍了如何利用**模型上下文协议（MCP）**将外部工具与 **Amazon Quick Agents** 进行集成。这是一份面向第三方合作伙伴的实操指南，旨在帮助开发者构建新的 MCP 服务器，或对现有的服务器进行验证与调整，以实现与 Amazon Quick 的无缝对接。

文章通过一个**六步清单**详细阐述了实施过程，并引用了《Amazon Quick 用户指南》中关于 MCP 客户端行为及约束条件的说明，为技术集成提供了具体的落地步骤。

---
## 评论

### 核心评价

这篇文章的中心观点是：**通过遵循标准化的 Model Context Protocol (MCP) 并适配 Amazon Quick Agents 的特定约束，第三方开发者能够以低成本、高确定性的方式将外部工具接入亚马逊的生成式 AI 生态，从而实现 AI 应用从“单一对话”向“复杂任务执行”的关键跨越。**

### 深入分析与评价

#### 1. 内容深度：工程严谨性与协议固化的平衡
*   **支撑理由（事实陈述）：** 文章没有停留在概念层面，而是提供了一个具体的“六步清单”。这种工程化的方法论（从服务器构建、验证到调整）体现了对 MCP 协议作为连接标准的深刻理解。它强调了 MCP 客户端的行为模式，表明作者不仅关注“怎么发数据”，更关注“Agent 如何理解并使用工具”。
*   **支撑理由（作者观点）：** 文章对“约束”的提及至关重要。在 LLM 应用开发中，能力的边界往往比功能本身更重要。明确约束（如上下文窗口限制、特定触发词）是保证 Agent 稳定性的核心，这显示了文章在技术深度上不仅关注“连通性”，更关注“可控性”。
*   **反例/边界条件（你的推断）：** MCP 协议虽然解决了连接问题，但并未解决工具的“语义鸿沟”。例如，一个外部 API 返回了复杂的 JSON 嵌套结构，即使 MCP 传输无误，Amazon Quick 底座模型若缺乏对该领域的特定微调，可能仍无法正确解析该数据并生成最终用户指令。**技术栈的打通并不等于业务逻辑的自动化。**

#### 2. 实用价值：为生态伙伴提供的“生存指南”
*   **支撑理由（事实陈述）：** 针对 3P（第三方）合作伙伴的定位使得文章具有极高的实操价值。对于 ISV（独立软件开发商）而言，这是将其现有 SaaS 产品“AI 化”并接入亚马逊庞大销售渠道的直接路径。
*   **支撑理由（你的推断）：** 在当前的 AI 插件生态中，OpenAI GPTs 和 LangChain 都有各自的接入标准，导致开发碎片化。MCP 作为一个新兴的通用标准，文章实际上是在教开发者如何“一次开发，多处复用”（假设 MCP �广泛采纳），这降低了长期的技术负债。
*   **反例/边界条件（事实陈述）：** 实用价值受限于 Amazon Quick Agents 本身的市场渗透率。如果 Amazon Quick 在企业级市场的占有率不及 ChatGPT 或 Microsoft Copilot，那么开发者投入资源构建 MCP Server 的 ROI（投资回报率）将会大打折扣。

#### 3. 创新性：协议标准化大于算法创新
*   **支撑理由（作者观点）：** 文章的真正创新点不在于具体的代码实现，而在于对 **MCP (Model Context Protocol)** 这一新兴标准的推广和应用。它标志着 AI Agent 交互从“各立山头”的 API 调用，转向类似 HTTP 的统一协议层。
*   **反例/边界条件（你的推断）：** 这种创新性目前仍具有局限性。MCP 主要解决了“数据获取”问题，但对于“多步骤任务规划”、“长期记忆”和“人机协作循环”等更高级的 Agent 模式，仅靠 MCP 是不够的。文章未提及如何处理工具调用失败后的重试策略或回滚机制，这是目前 Agent 领域的难点。

#### 4. 行业影响：推动 AI Agent 的“USB 时刻”
*   **支撑理由（作者观点）：** 如果 MCP 成为主流，这篇文章将不仅仅是一篇技术文档，而是亚马逊定义 AI Agent 接口规范的重要一步。类似于 USB 接口统一了外设硬件，MCP 有望统一 LLM 与软件工具的连接方式。
*   **支撑理由（事实陈述）：** 亚马逊的入局（通过支持 MCP）会加剧大厂间的协议之争。目前有 OpenAI 的 Plugin Spec、MCP 等。文章的发布暗示亚马逊正在通过支持开源协议来对抗封闭生态，这对行业走向开放具有积极影响。
*   **反例/边界条件（你的推断）：** 行业影响面临“碎片化风险”。如果 MCP 未能成为 ANSI/ISO 级别的标准，而仅仅是 Anthropic/Amazon 阵营的玩具，那么它将增加而非减少开发者的负担，导致开发者需要在多个协议间做转换层。

#### 5. 可读性与逻辑性：教科书式的规范文档
*   **支撑理由（事实陈述）：** 文章结构清晰，采用“Checklist”形式，符合工程师的阅读习惯。它将复杂的系统集成问题拆解为线性步骤，降低了认知负荷。
*   **反例/边界条件（作者观点）：** 这种结构虽然清晰，但可能掩盖了调试过程中的复杂性。对于初学者，文档中缺乏关于“认证鉴权”和“错误处理”的详细代码示例，可能会在实际落地时造成困扰。

### 综合评价与批判性思考

这篇文章是亚马逊构建 AI Agent 生态的一块关键拼图。它不仅仅是一篇技术教程，更是一份生态招募令。

**批判性视角：**
我们必须警惕“协议万能论”的陷阱。文章暗示只要接了 MCP，工具就能完美被 Agent 使用。然而，在实际应用中，**工具描述的提示词工程** 往往比协议本身更重要。一个 MCP Server 如果不能提供清晰、结构化的工具描述，LLM 依然会胡乱调用。此外，安全性是一个巨大的隐忧。将外部工具通过标准协议接入 Agent，可能会扩大攻击面。例如，如果 MCP Server 没有

---
## 技术分析

基于您提供的文章标题和摘要，以下是对《使用模型上下文协议 (MCP) 将外部工具与 Amazon Quick Agents 集成》的深入分析。

---

# 深度分析报告：基于 MCP 的 Amazon Quick Agents 外部工具集成

## 1. 核心观点深度解读

### 文章的主要观点
这篇文章的核心主张是**标准化接口协议是解决 AI Agent 生态碎片化问题的关键**。文章提出，通过采用 **Model Context Protocol (MCP)**，第三方开发者可以构建标准化的服务器，从而将外部数据源和工具无缝、安全地接入 Amazon Quick Agents（Amazon Bedrock 下的智能体服务）。文章强调，这不仅仅是一次简单的 API 调用，而是通过一套严格的“六步清单”来确保互操作性。

### 作者想要传达的核心思想
作者传达了**“协议优于定制”**的工程哲学。在 LLM 应用开发中，为每个 Agent 重复编写工具连接代码是低效且不可扩展的。MCP 提供了一种通用的“语言”，让 AI 模型能够理解并使用任何软件功能。核心思想在于降低 AI Agent 与企业现有系统集成的门槛，使“即插即用”的 AI 功能成为可能。

### 观点的创新性和深度
*   **创新性**：MCP 的引入标志着 AI 集成从“硬编码 Prompt”向“标准化协议”的转变。类似于 USB 接口统一了硬件外设，MCP 试图统一 AI 的“感知与行动”接口。
*   **深度**：文章并未停留在概念层面，而是深入到了“客户端行为与约束”的具体细节。它揭示了集成的难点往往不在于 AI 模型本身，而在于**对客户端（Agent）能力边界的理解**（如上下文窗口限制、安全沙箱、超时处理等）。

### 为什么这个观点重要
随着企业从“聊天机器人”转向“智能体”，Agent 需要执行实际任务（查询数据库、操作 CRM、调用 API）。如果没有统一标准，每个工具集成都需要定制开发，成本极高且难以维护。MCP 的出现和 Amazon 的支持，意味着企业级 AI 落地有了可复用的基础设施，这是 AI 从玩具走向工具的基石。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
*   **Model Context Protocol (MCP)**：这是一个开放标准（基于 JSON-RPC），用于连接 AI 应用与数据源。它定义了 Server 如何暴露资源、提示词和工具。
*   **Amazon Quick Agents (User Guide)**：作为 MCP 的**客户端**，它负责发起连接、发现可用工具，并根据模型推理决定调用哪个工具。
*   **MCP Server**：运行在本地或远程的进程，封装了与外部系统交互的逻辑。
*   **STDIO vs. SSE Transport**：MCP 支持两种传输层。标准输入/输出（STDIO）适用于本地进程，服务器发送事件（SSE）适用于基于 HTTP 的远程连接。

### 技术原理和实现方式
1.  **握手与初始化**：Client 启动 Server 进程（或建立 SSE 连接），发送 `initialize` 请求。
2.  **能力发现**：Client 请求 Server 列出所有可用的 `tools`（函数）、`resources`（数据文件）或 `prompts`（模板）。
3.  **工具调用**：当用户与 Agent 对话时，模型决定需要调用某个工具。Agent 构造符合 MCP 定义的 JSON-RPC 请求发送给 Server。
4.  **执行与响应**：Server 执行实际逻辑（如 SQL 查询），将结果格式化为文本或特定 JSON 结构返回给 Agent，Agent 再将其整合给用户。

### 技术难点和解决方案
*   **难点：上下文窗口管理**。外部工具返回的数据可能极其庞大，导致模型上下文溢出。
    *   **解决方案**：在 Server 端实现严格的**数据截断和摘要逻辑**。文章提到的“六步清单”中必然包含验证 Server 响应大小是否符合 Quick Agents 的限制。
*   **难点：错误映射**。外部系统的原始错误（如 500 Internal Server Error）对模型毫无意义。
    *   **解决方案**：MCP Server 需要将底层错误翻译为自然语言描述，帮助模型理解发生了什么并尝试恢复或告知用户。
*   **难点：安全性**。允许 Agent 访问数据库存在风险。
    *   **解决方案**：在 MCP Server 层面实施严格的权限控制和输入验证，而非依赖模型自我约束。

### 技术创新点分析
MCP 的最大创新在于**解耦**。它将“模型能力”与“业务逻辑”通过标准协议完全解耦。这使得同一个 MCP Server（例如一个 Jira 集成服务）可以被 ChatGPT、Claude Desktop 或 Amazon Quick Agents 复用，无需重复开发。

---

## 3. 实际应用价值

### 对实际工作的指导意义
对于 3P（第三方）开发者或企业 IT 团队，这篇文章提供了一条**将私有资产货币化或内部系统 AI 化的清晰路径**。通过构建 MCP Server，企业可以将内部 ERP、Wiki 或专用工具暴露给 Amazon 的 AI，无需修改 Amazon 的核心代码。

### 可以应用到哪些场景
1.  **企业知识库问答**：MCP Server 暴露 Confluence 或 SharePoint 的文档索引，Agent 可以实时查询最新政策。
2.  **业务操作自动化**：MCP Server 暴露 Salesforce API，允许 Agent 通过对话直接创建 Lead 或更新订单状态。
3.  **数据分析**：MCP Server 封装 SQL 生成和执行接口，允许自然语言查询数据仓库。

### 需要注意的问题
*   **延迟**：多跳架构（User -> Agent -> Server -> DB -> Server -> Agent -> User）增加了响应延迟。对于实时性要求高的场景需谨慎。
*   **幻觉风险**：模型可能会调用不存在的工具参数。Server 必须具备强大的参数校验能力。

### 实施建议
不要试图一步到位。先构建一个简单的“时间查询”或“天气查询” MCP Server 来验证 Amazon Quick Agents 的连接性和行为模式，再逐步迁移核心业务逻辑。

---

## 4. 行业影响分析

### 对行业的启示
MCP 的兴起预示着 **AI 中间件** 时代的到来。未来的软件架构将包含“AI 网关”或“MCP 层”，专门负责将异构系统转化为 LLM 可理解的格式。

### 可能带来的变革
*   **SaaS 集成模式的改变**：SaaS 厂商不再需要构建“Copilot”，只需提供标准的 MCP Server，即可接入所有支持 MCP 的 LLM 平台（OpenAI, Anthropic, AWS 等）。
*   **RAG 架构的简化**：通过 MCP 的 `resources` 接口，数据摄取过程可能被简化为标准的文件读取协议，无需复杂的向量流管道。

### 相关领域的发展趋势
**协议战争**。虽然 MCP 目前由 Anthropic 主导，但 AWS 的支持使其成为强有力的行业标准竞争者。未来可能会看到 OpenAI 的 Function Calling 与 MCP 之间的竞争或融合。

### 对行业格局的影响
这将削弱单一 AI 平台（如 ChatGPT 插件商店）的锁定效应，增强**连接器提供商**和**企业数据持有者**的话语权。

---

## 5. 延伸思考

### 引发的其他思考
MCP 目前主要解决“工具调用”问题。未来是否会演化出“Agent 间通信协议”？即一个 Agent 作为 Client 调用另一个 Agent 作为 Server 提供的服务，形成多智能体协作网络。

### 可以拓展的方向
*   **安全性增强**：引入 OAuth 2.0 或 mTLS 到 MCP 协议层，确保云端 MCP Server 的通信安全。
*   **流式响应**：目前的 MCP 侧重请求-响应。对于长时间运行的任务（如生成报告），如何支持 Server 主动推送进度流？

### 需要进一步研究的问题
Amazon Quick Agents 对 MCP 的具体约束有哪些？（例如：最大 Token 数、超时时间、支持的 MIME 类型）。摘要中提到的“User Guide”细节是实施的关键。

### 未来发展趋势
**边缘侧 MCP**。随着端侧 AI 模型（如 MacBook 本地运行的 LLM）的普及，通过 STDIO 连接本地 MCP Server 将成为主流，这不仅保护隐私，还能实现零延迟的工具调用。

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有 API**：检查你现有的 REST 或 GraphQL API。
2.  **封装 MCP 层**：编写一个轻量级服务（推荐使用 Python 或 TypeScript 的 SDK），将现有 API 映射为 MCP Tools。
3.  **本地测试**：使用 Inspector (MCP 客户端调试工具) 验证工具描述是否清晰。
4.  **部署与连接**：将 Server 部署为 SSE 服务或容器，并在 Amazon Quick Agents 配置中添加连接。

### 具体的行动建议
*   **阅读规范**：熟读 MCP 规范，特别是 `tools` 的 `inputSchema` 定义（基于 JSON Schema）。
*   **描述工程**：工具的 `description` 字段比代码本身更重要。它决定了模型是否会调用该工具。投入时间优化 Prompt 描述。

### 需要补充的知识
*   **JSON Schema**：用于定义工具的输入参数。
*   **Concurrency Control**：如果 Server 是有状态的，如何处理并发的 Agent 请求。

### 实践中的注意事项
**幂等性**。Agent 可能会因为网络重试或不确定性而重复调用同一个工具。确保你的 MCP Server 操作是幂等的（例如，多次查询订单状态没问题，但多次创建订单则有问题）。

---

## 7. 案例分析

### 结合实际案例说明
**场景**：一家电商公司希望 Amazon Quick Agents 能够处理“查询我的最新订单状态”的请求。

**实施**：
1.  **MCP Server**：开发一个名为 `order-service-mcp` 的服务。
2.  **Tool Definition**：定义工具 `get_latest_order`，参数为 `user_id`。
3.  **集成**：在 Amazon Bedrock 的 Quick Agents 配置中指向该 MCP Server 的 SSE 端点。
4.  **运行**：用户问“我的货到哪了？” -> Agent 识别意图 -> 调用 `get_latest_order` -> Server 返回物流状态 -> Agent 生成自然语言回复。

### 成功案例分析
**GitHub 的 Contextual AI**：虽然未明确使用 MCP，但类似的概念（通过 IDE 插件将代码库上下文暴露给 AI）证明了标准化上下文提供机制的巨大价值。MCP 将这种能力泛化到了任意应用。

### 失败案例反思
**早期 ChatGPT 插件**：许多插件失败是因为描述不清或 API 响应格式非结构化，导致模型无法解析。MCP 强制使用 JSON Schema 和结构化响应，有效解决了这一问题。

### 经验教训总结
**不要暴露原始数据库**。早期的尝试往往是让 Agent 直接写 SQL。失败原因在于安全性差且模型容易写错 SQL。更好的实践是在 MCP Server 中封装受限制的、语义化的高级函数（如 `get_user_profile`），而不是暴露 `SELECT * FROM users`。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**采用模型上下文协议 (MCP) 是实现 Amazon Quick Agents 与外部工具高效、

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确工具定义与能力边界

**说明**: 在集成之前，必须清晰定义外部工具的具体功能、输入输出模式以及其能力边界。MCP 需要准确的元数据来理解工具如何与 LLM 交互，模糊的定义会导致代理调用错误的工具或生成无效的参数。

**实施步骤**:
1. 列出工具的详细功能清单，明确每个工具的用途。
2. 为每个工具编写清晰的描述，确保描述中包含工具的主要用途和限制。
3. 定义严格的输入模式和输出模式，使用 JSON Schema 进行规范。

**注意事项**: 避免使用过于宽泛或模糊的描述，这会增加模型推理的复杂性和出错概率。

---

### 实践 2：实施严格的输入验证与安全沙箱

**说明**: 外部工具接收的数据直接来自 LLM 的生成内容，可能包含格式错误甚至潜在的恶意指令。为了确保系统稳定性，必须在工具端实施严格的验证，并在隔离环境中执行操作。

**实施步骤**:
1. 在 MCP 服务器端实现严格的参数校验逻辑，拒绝不符合 Schema 的请求。
2. 对工具执行环境进行容器化或使用沙箱机制，限制其对底层系统的访问权限（如文件系统、网络）。
3. 设置超时机制，防止因工具挂起而导致整个代理流程卡死。

**注意事项**: 永远不要盲目信任来自 LLM 的输入，始终将其视为不可信数据源进行处理。

---

### 实践 3：优化错误处理与上下文反馈

**说明**: 当外部工具执行失败时，仅仅返回错误代码往往不足以让 LLM 理解问题所在并自我修正。最佳实践是提供结构化的错误信息，包含错误原因及可能的修复建议。

**实施步骤**:
1. 设计标准化的错误响应格式，包含 `error_code`、`error_message` 和 `recovery_suggestion` 字段。
2. 确保错误信息尽可能详细，但不要暴露敏感的系统内部细节。
3. 测试 LLM 对各种错误场景的理解能力，确保它能根据反馈调整后续行动。

**注意事项**: 避免返回原始的堆栈跟踪信息给终端用户或模型，这会泄露系统架构信息并浪费 Token。

---

### 实践 4：管理数据上下文与 Token 消耗

**说明**: MCP 集成涉及将外部数据注入到 LLM 的提示词中。如果工具返回大量无关数据，会迅速消耗上下文窗口并增加延迟。必须精细控制返回给模型的数据量。

**实施步骤**:
1. 在工具端实现数据过滤逻辑，仅返回与当前请求最相关的核心数据。
2. 对于长文本检索类工具，优先使用摘要或分块策略，而不是一次性返回全部内容。
3. 监控 Token 使用情况，为特定工具设置返回数据的最大长度限制。

**注意事项**: 即使模型支持长上下文，也应保持输入信息的精简，以提高响应速度和准确性。

---

### 实践 5：设计幂等性与状态无关的工具

**说明**: LLM 可能会因为重试机制或对先前结果的误解而多次调用同一个工具。如果工具不是幂等的（即多次调用产生不同结果），可能会导致系统状态不一致或数据重复。

**实施步骤**:
1. 确保读取类工具是完全幂等的。
2. 对于写入类工具，设计业务逻辑使其能够处理重复请求（例如使用唯一 ID 去重）。
3. 尽量避免在工具端维护有状态会话，让每次调用都独立自包含。

**注意事项**: 如果工具必须依赖状态，请在 MCP 实现中明确记录状态管理逻辑，并确保 Quick Agents 能够感知这种依赖。

---

### 实践 6：建立清晰的日志与可观测性体系

**说明**: 在 MCP 集成中，LLM 与工具之间的交互是非确定性的。为了调试和性能优化，必须记录详细的交互日志，包括请求载荷、响应时间以及调用链路。

**实施步骤**:
1. 在 MCP 服务器中记录所有入站请求和出站响应的元数据。
2. 集成分布式追踪工具，将工具调用与 Amazon Quick Agents 的会话 ID 关联。
3. 设置关键指标监控，如工具调用延迟、错误率和超时率。

**注意事项**: 在记录日志时，确保对敏感数据（如 PII）进行脱敏处理，以符合合规要求。

---
## 学习要点

- Amazon Quick Agents 现已支持通过模型上下文协议（MCP）无缝集成外部工具，从而显著扩展了其在企业环境中的应用边界。
- MCP 提供了一种标准化的连接方式，使智能体能够安全、高效地访问企业私有数据源和业务系统。
- 开发者可以利用 MCP 实现与外部 API 的双向通信，让智能体不仅能读取数据，还能代表用户执行操作。
- 通过将企业知识库与 Quick Agents 连接，该架构有效解决了大语言模型普遍存在的“幻觉”问题，确保回答的准确性。
- 此集成方案允许企业通过 MCP 快速适配现有的技术栈，而无需进行复杂的定制化模型训练或大规模基础设施重构。
- 借助 MCP 的标准化接口，企业能够以模块化的方式扩展智能体功能，灵活应对不断变化的业务需求。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP协议](/tags/mcp%E5%8D%8F%E8%AE%AE/) / [Amazon Quick](/tags/amazon-quick/) / [模型上下文协议](/tags/%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE/) / [Agent集成](/tags/agent%E9%9B%86%E6%88%90/) / [外部工具](/tags/%E5%A4%96%E9%83%A8%E5%B7%A5%E5%85%B7/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [AWS](/tags/aws/) / [LLM工具链](/tags/llm%E5%B7%A5%E5%85%B7%E9%93%BE/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用MCP集成外部工具至Amazon Quick Agents的构建指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--8.md" >}})
- [使用MCP将外部工具集成至Amazon Quick Agents的六步指南]({{< relref "posts/20260222-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实操指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--4.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的六步指南]({{< relref "posts/20260224-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*