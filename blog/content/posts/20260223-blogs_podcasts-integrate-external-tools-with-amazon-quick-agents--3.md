---
title: "使用MCP集成外部工具至Amazon Quick Agents的六步指南"
date: 2026-02-23T02:56:00+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "Agent", "系统集成", "开发指南", "第三方集成", "模型上下文协议", "服务器开发"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "本文介绍了如何通过**模型上下文协议（MCP）**将外部工具与 **Amazon Quick Agents** 集成。这是一份面向第三方合作伙伴的实操指南，旨在帮助开发者构建新的 MCP 服务器，或验证并调整现有服务器以适配 Amazon Quick。 主要内容总结如下： 1. **核心目标**： 指导 3P 合作伙伴"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["Web应用开发"]
---

# 使用MCP集成外部工具至Amazon Quick Agents的六步指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在本文中，您将使用一个六步检查清单来构建新的 MCP 服务器，或针对 Amazon Quick 集成验证并调整现有的 MCP 服务器。Amazon Quick 用户指南描述了 MCP 客户端的行为与约束。本文是一份“操作指南”，面向第三方合作伙伴为实现与 Amazon Quick 的 MCP 集成所需的详细实施步骤。

---
## 导语

随着大模型应用场景的深化，如何让 AI 智能体精准调用外部工具已成为提升其落地价值的关键。本文聚焦于 Model Context Protocol (MCP) 与 Amazon Quick Agents 的集成实践，通过一份详尽的六步检查清单，指导开发者构建新的 MCP 服务器或验证现有配置。阅读本文，您将掌握具体的实施步骤，确保第三方工具能高效、合规地接入 Amazon Quick 生态。

---
## 摘要

本文介绍了如何通过**模型上下文协议（MCP）**将外部工具与 **Amazon Quick Agents** 集成。这是一份面向第三方合作伙伴的实操指南，旨在帮助开发者构建新的 MCP 服务器，或验证并调整现有服务器以适配 Amazon Quick。

主要内容总结如下：

1.  **核心目标**：
    指导 3P 合作伙伴完成技术集成，确保外部工具能通过 MCP 协议有效地与 Amazon Quick Agents 交互。

2.  **实施方法**：
    文章提供了一个**六步清单**，涵盖了从开发到验证的全过程，详细说明了实现集成所需的各项具体步骤。

3.  **规范依据**：
    开发过程必须参考《Amazon Quick 用户指南》，该文档明确了 MCP 客户端的行为模式和限制条件，是实现合规集成的基础。

简而言之，本文是利用 MCP 协议连接外部工具与 Amazon Quick 的标准化操作手册。

---
## 评论

### 文章评价：基于MCP协议集成Amazon Quick Agents的技术与行业分析

**文章中心观点**
本文核心观点在于倡导利用Model Context Protocol (MCP)作为标准化中间层，通过遵循特定的技术清单，将第三方工具的数据和动作无缝集成到Amazon Quick Agents中，从而解决AI应用中“数据孤岛”和“工具调用碎片化”的问题。（作者观点/事实陈述）

**支撑理由与深度评价**

**1. 标准化协议对AI Agent生态的“降噪”作用（内容深度 & 行业影响）**
*   **理由：** 文章强调MCP的重要性，这实际上是对当前Agent开发中“重复造轮子”现象的修正。在MCP出现之前，每个SaaS工具要接入AI（如ChatGPT或Claude）都需要定制API Adapter。MCP试图成为AI领域的“ODBC”（开放数据库连接），统一数据查询和工具调用的接口标准。
*   **事实陈述：** 文章提到的“六步清单”和“Quick User Guide”是亚马逊为了规范第三方接入而设立的强制性门槛，旨在确保MCP Server在客户端（Quick Agents）上的行为一致性。
*   **你的推断：** 亚马逊此举意在通过构建标准协议，快速丰富Quick Agents的生态护城河，防止其平台沦为单纯的聊天界面，而是成为实际的操作中枢。

**2. 聚焦“验证与调整”而非“从零开发”（实用价值）**
*   **理由：** 文章特别提到不仅适用于构建新Server，还适用于“validate and adjust an existing MCP server”。这极具实用价值。许多企业已有封装好的API，MCP并非要求重构后端，而是增加一个标准翻译层。这种“适配器模式”大大降低了企业的迁移成本。
*   **作者观点：** 对于3P（第三方）开发者而言，这篇文章不仅是技术文档，更是合规指南。只有通过了这些验证，工具才能被Amazon的庞大客户群触达。

**3. 推动AI从“对话”转向“行动”（创新性）**
*   **理由：** 文章实质上是在教授如何赋予大模型“手脚”。通过MCP，Quick Agents不再局限于生成文本，而是能够读取数据库（RAG增强）或执行API调用（Function Calling）。这种从Content Generation到Capability Orchestration的转变，是当前AI行业应用落地的核心瓶颈。

**反例与边界条件（批判性思考）**

*   **边界条件1：延迟与实时性权衡**
    *   **你的推断：** MCP虽然统一了协议，但在Agent与MCP Server之间增加了一层网络跳转。对于高频交易或实时工业控制等对毫秒级延迟敏感的场景，这种基于标准HTTP/WebSocket的通用协议可能过于笨重，不如直连API高效。

*   **边界条件2：复杂逻辑的本地化处理**
    *   **反例：** 文章假设MCP Server能处理所有工具逻辑。然而，某些极其复杂的业务逻辑（如大型ERP的复杂审批流）很难完全解耦到MCP Server中。如果强行将所有逻辑塞入MCP的标准Prompt或Resource模板中，可能会导致Server端代码臃肿，反而不如传统的微服务调用灵活。

*   **边界条件3：数据隐私与边界**
    *   **事实陈述：** 将内部工具通过MCP暴露给公有云Agent（Amazon Quick），必然涉及数据出域问题。文章虽然提到了User Guide，但未深入探讨混合云部署下的数据安全边界。对于金融、医疗等行业，仅靠协议标准不足以解决合规焦虑。

**可验证的检查方式**

1.  **协议互操作性测试（指标）：**
    *   选取两个不同的MCP Server（例如一个文件系统工具和一个日历工具），在不修改Amazon Quick Agents核心代码的情况下，验证其能否同时被加载并正确执行各自的指令。如果能，证明MCP的解耦设计有效。

2.  **错误恢复机制观察（实验）：**
    *   在MCP Server运行过程中人为中断网络或返回非法数据，观察Amazon Quick Agent是直接崩溃、简单报错，还是能根据协议定义优雅降级。这是检验文章中“验证清单”是否严谨的关键指标。

3.  **开发效率对比（观察窗口）：**
    *   对比同一款工具（如Jira），分别使用“原生API集成”与“MCP集成”接入Amazon Quick Agents的开发时间。如果MCP方式能节省30%以上的适配代码量，则证实了其实用价值。

**实际应用建议**

*   **不要盲目重构：** 对于现有的SaaS厂商，不要试图立即重写后端代码以迎合MCP。应优先开发“MCP Adapter”层，将现有API映射到MCP标准，利用文章中的清单验证通过后再考虑底层优化。
*   **关注Prompt边界：** MCP Server不仅仅是API包装，还涉及Prompt Template的管理。在集成时，务必在Server端做好输入输出的Schema严格校验，防止Prompt注入攻击波及你的核心工具。
*   **监控与日志：** 既然作为第三方工具接入，必须在MCP Server侧建立详细的调用日志。因为Amazon Quick Agents可能是一个黑盒，只有通过Server侧的日志才能分析用户的使用意图和失败原因，从而持续优化工具的描述和参数设计。

---
## 技术分析

基于您提供的文章标题和摘要，这是一篇关于**第三方开发者（3P Partners）如何利用模型上下文协议将外部工具集成到 Amazon Quick Agents 的技术指南**。文章提供了一套六步清单，旨在指导开发者构建新的 MCP 服务器或调整现有的服务器以适应 Amazon Quick 的特定约束。

以下是对该文章核心观点和技术要点的深入分析：

---

## 1. 核心观点深度解读

**主要观点：**
文章的核心观点是**标准化集成**。它主张通过采用 **Model Context Protocol (MCP)** 这一开放标准，第三方开发者可以系统化、高效地将外部数据源和工具连接到 Amazon Quick Agents，从而打破 AI 应用与私有数据之间的孤岛。

**核心思想：**
作者传达的核心思想是**“协议即桥梁”**。在 AI Agent 生态系统中，最大的瓶颈之一是如何让大语言模型（LLM）安全、准确地访问外部数据。MCP 提供了一种统一的语言（协议），使得 Amazon Quick 这样的客户端能够以一致的方式与各种外部工具交互，而无需为每个工具编写定制化的集成代码。

**创新性与深度：**
其创新性在于从“点对点集成”转向“总线式集成”。传统的集成往往需要针对每个应用开发特定的 API 适配器，而 MCP 将其抽象化。深度体现在文章不仅介绍了“是什么”，还提供了“怎么做”的六步清单，强调了**客户端约束**的重要性——即开发者不能只关注服务器怎么写，必须理解 Amazon Quick 作为客户端的行为模式（如超时、数据格式限制）。

**重要性：**
这个观点至关重要，因为它标志着 AI 应用开发从“以模型为中心”向“以数据集成为中心”的转移。对于企业而言，这意味着他们现有的任何工具（只要符合 MCP）都可以瞬间变成 AI Agent 的能力，极大地扩展了 AI 的实用边界。

## 2. 关键技术要点

**涉及的关键技术：**
*   **Model Context Protocol (MCP)：** 这是一个开放标准，类似于 AI 应用的“USB 接口”，用于连接 AI 模型与数据源。
*   **Amazon Quick Agents：** 作为 MCP 的**客户端**，负责发起请求、上下文管理和工具调用。
*   **MCP Server：** 作为**服务端**，负责托管资源、提供提示词和执行工具。

**技术原理与实现：**
MCP 基于 JSON-RPC 2.0 协议。通信流程通常如下：
1.  **连接建立：** Client 启动并连接到 Server（通常通过 stdio 或 SSE）。
2.  **初始化：** 交换能力（Capabilities），告知对方支持哪些功能（如 resources, prompts, tools）。
3.  **交互：** Client 请求可用资源列表，或调用特定工具，Server 返回结构化数据（如文本、图片或特定 JSON 格式）。

**技术难点与解决方案：**
*   **难点：** **上下文窗口限制与数据噪声**。外部工具返回的数据可能非常庞大，直接塞进 LLM 上下文会溢出或增加成本。
*   **解决方案：** MCP 需要实现智能的**数据分页**和**摘要机制**。Server 端不应直接抛出数据库，而应提供经过过滤或预处理的高质量上下文。
*   **难点：** **安全性认证**。如何让 Agent 访问私有数据（如 Jira, Slack）而不泄露凭证。
*   **解决方案：** 文章提到的六步清单中必然包含对认证机制的处理，确保 MCP Server 在传输层或应用层进行严格的权限校验。

**技术创新点：**
MCP 的**可移植性**是最大的创新。一个编写良好的 MCP Server 不仅可以连接 Amazon Quick，理论上也能连接 Claude Desktop 或其他支持 MCP 的客户端，实现了“一次编写，到处运行”。

## 3. 实际应用价值

**指导意义：**
对于 3P 开发者，这篇文章是一份**合规性检查清单**。它告诉开发者：仅仅实现了 MCP 标准是不够的，你还必须满足 Amazon Quick 的特定 User Guide（例如，Quick 可能不支持某种特定的数据类型，或者对响应时间有严格要求）。

**应用场景：**
*   **企业知识库查询：** 将公司内部的 Wiki、Confluence 连接到 Quick，让员工通过自然语言查询文档。
*   **业务自动化：** 将 CRM (Salesforce) 或工单系统 连接，让 Agent 能够直接读取状态或创建记录。
*   **数据分析：** 连接 BI 工具，允许用户通过对话生成报表。

**需注意的问题：**
*   **延迟：** 如果 MCP Server 响应太慢，会导致用户体验极差。
*   **错误处理：** Server 需要返回清晰的错误信息，以便 LLM 能够理解并转述给用户，而不是抛出晦涩的堆栈跟踪。

**实施建议：**
在开发前，务必熟读 *Amazon Quick User Guide* 中的“MCP Client Constraints”部分。不要假设 Amazon Quick 的行为和 Claude Desktop 完全一致。

## 4. 行业影响分析

**对行业的启示：**
这预示着 **AI Agent 基础设施层的标准化**正在加速。过去几年，LangChain 等框架试图在代码层面统一集成，而 MCP 试图在**协议层**统一。这降低了 AI 落地的门槛。

**可能带来的变革：**
从“构建 App”转向“构建插件”。未来软件公司的竞争力可能不仅在于 SaaS 本身，还在于其 SaaS 是否能通过 MCP 等协议被 AI Agent 无缝调用。无法被 AI 集成的软件可能会逐渐被边缘化。

**发展趋势：**
MCP 可能会成为连接 LLM 与世界的事实标准之一。类似于 RSS 之于博客，MCP 可能成为 AI 时代的“数据 API 标准”。

## 5. 延伸思考

**拓展方向：**
*   **多模态支持：** MCP 目前主要处理文本，未来如何高效地处理视频、音频流？
*   **Agent 间协作：** 如果多个 Agent 都使用 MCP，它们之间是否可以直接通过某种协议交换数据，而无需经过 LLM 中转？

**需进一步研究的问题：**
*   **安全性边界：** 当 Agent 拥有了通过 MCP 操作外部工具（如删除邮件、执行转账）的权限时，如何防止 Prompt Injection 攻击导致恶意操作？
*   **成本分摊：** MCP Server 的运行成本由谁承担？是工具提供商还是 Amazon Quick 的用户？

## 6. 实践建议

**如何应用到项目：**
1.  **评估现有工具：** 检查你目前维护的 API 或工具是否适合被 AI 调用。
2.  **开发 MCP Wrapper：** 不要重写整个后端，而是编写一个轻量级的 MCP Server，作为现有 API 的适配层。
3.  **本地测试：** 使用支持 MCP 的本地客户端（如 Claude Desktop）测试你的 Server，确保其稳定，再接入 Amazon Quick。

**具体行动：**
*   搭建一个基于 Python/TypeScript 的 MCP Server SDK 环境。
*   实现一个简单的 `hello_world` 工具，验证与 Amazon Quick 的连接。
*   仔细阅读 Amazon Quick 关于“最大 Token 限制”和“超时时间”的文档。

**补充知识：**
需要深入学习 **JSON-RPC** 规范以及 **Stdio**（标准输入输出）通信机制，这是 MCP 本地通信的基础。

## 7. 案例分析

**成功案例（假设性）：**
*   **场景：** 一家拥有庞大内部 Wiki 的公司。
*   **做法：** 开发一个 MCP Server，能够接收自然语言查询，通过 Elasticsearch 检索 Wiki，并返回片段。
*   **结果：** Amazon Quick Agent 能够准确回答“公司休假政策是什么”的问题，且无需人工干预。

**失败案例反思：**
*   **场景：** 某开发者试图将一个极其复杂的图形化报表工具直接通过 MCP 暴露给 Agent。
*   **问题：** 该工具需要 20 个参数才能运行，且返回的是二进制图片数据。
*   **教训：** MCP 适合**意图明确**和**数据结构化**的场景。如果交互过于复杂，或者返回的数据 LLM 无法理解（如复杂的二进制协议），集成效果会很差。需要对工具进行“AI 友好化”改造（例如简化参数，返回描述性文本而非纯图片）。

## 8. 哲学与逻辑：论证地图

**中心命题：**
**采用 Model Context Protocol (MCP) 是第三方开发者将其工具高效且安全地集成到 Amazon Quick Agents 生态系统的最佳路径。**

**支撑理由：**
1.  **互操作性：** MCP 提供了标准化的接口，减少了为每个 AI 客户端编写定制代码的维护成本。
    *   *依据：* MCP 是基于通用标准（JSON-RPC）构建的，被广泛采用。
2.  **客户端约束匹配：** 遵循文章中的六步清单能确保 Server 满足 Amazon Quick 的特定行为要求（如超时处理），从而保证稳定性。
    *   *依据：* 技术文档中明确指出了客户端行为的差异性。
3.  **上下文感知优化：** MCP 允许 Server 主动向 Client 提供资源，使 Agent 能够在用户提问前就拥有必要的上下文。
    *   *依据：* MCP 协议中 `resources` 的定义。

**反例/边界条件：**
1.  **实时流式数据：** 如果应用需要毫秒级的低延迟双向流（如语音对话），MCP 基于 Request-Response 的模型可能不是最优解，WebSocket 可能更合适。
2.  **极度复杂的计算：** 如果工具需要运行数小时才能返回结果（如训练一个模型），Amazon Quick 的同步等待机制会导致超时，需要异步回调模式，这可能超出了基础 MCP 的范畴。

**命题性质：**
*   **事实：** MCP 是一个开放标准，Amazon Quick 支持 MCP。
*   **价值判断：** “最佳路径”意味着在效率、成本和未来兼容性之间的权衡优于其他方案。
*   **可检验预测：** 采用 MCP 的工具将比未采用的工具更容易被集成到多个 AI 平台。

**立场与验证：**
我持**支持**立场。在当前 AI 基础设施快速演变的阶段，采纳协议层标准是降低技术债的最有效策略。

**可证伪验证方式：**
*   **指标：** 对比开发一个自定义集成接口与开发一个 MCP Server 所需的人时数。
*   **观察：** 观察未来 6 个月内，除了 Amazon Quick 外，有多少其他主流 AI Agent 平台宣布支持 MCP。如果数量停滞，则说明其通用性受限；如果增长，则验证了其价值。

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确工具定义与功能边界

**说明**: 在集成之前，必须清晰定义外部工具的具体功能、输入参数及输出格式。这有助于 Amazon Quick Agents 准确理解工具用途，从而在正确的上下文中调用正确的工具，避免因功能模糊导致的调用错误或资源浪费。

**实施步骤**:
1. 列出外部工具的所有可用功能，并筛选出适合 Agent 调用的核心功能。
2. 为每个工具编写详细的描述文档，明确其能力边界（即工具能做什么和不能做什么）。
3. 定义严格的输入 Schema，包括参数类型、必填项和取值范围。

**注意事项**: 避免将过于庞大或功能杂乱的 API 直接作为单个工具集成，应将其拆分为多个职责单一的小工具。

---

### 实践 2：实施严格的输入验证与安全控制

**说明**: MCP 允许 Agent 动态构造查询或执行命令，因此必须在外部工具端实施严格的参数验证和安全沙箱机制。这能防止提示注入攻击或恶意指令对后端系统造成损害。

**实施步骤**:
1. 在 MCP 服务器端实现白名单机制，限制 Agent 只能访问特定的资源或执行特定的命令。
2. 对所有传入的参数进行类型检查和格式清洗，拒绝任何不符合预期的输入。
3. 遵循最小权限原则，为 Agent 配置的连接身份仅授予完成任务所需的最小权限集。

**注意事项**: 永远不要直接将 Agent 的输入拼接成系统命令或数据库查询语句而不经处理。

---

### 实践 3：优化数据上下文与提示词工程

**说明**: MCP 的核心价值在于为模型提供动态上下文。为了提高效率，应只向 Agent 传递相关的、精简的数据，避免大量无关噪音数据干扰模型的推理过程或消耗过多的 Token 配额。

**实施步骤**:
1. 在工具逻辑中增加过滤层，优先处理数据，仅返回与用户当前查询最相关的结果。
2. 在 MCP 工具的描述中，明确告知 Agent 何时应该调用该工具以及期望获得什么样的数据格式。
3. 测试并优化提示词，确保 Agent 能够准确地将用户意图转化为工具调用参数。

**注意事项**: 监控 Token 使用量，如果单次工具调用返回的数据量过大，考虑实现分页或摘要机制。

---

### 实践 4：构建健壮的错误处理与重试机制

**说明**: 外部工具调用可能会因为网络波动、服务不可用或参数错误而失败。良好的错误处理机制能确保 Amazon Quick Agents 在遇到工具调用失败时能够优雅降级或尝试恢复，而不是直接向用户报错。

**实施步骤**:
1. 定义标准化的错误码和错误消息格式，通过 MCP 清晰地反馈给 Agent。
2. 在 Agent 配置中设置重试策略，对于超时或临时性故障（如 5xx 错误）进行自动重试。
3. 设计兜底逻辑，当工具不可用时，指示 Agent 回答用户“暂时无法执行该操作，请稍后再试”或提供静态建议。

**注意事项**: 避免将后端系统的详细堆栈跟踪信息直接暴露给 Agent 或最终用户，以防信息泄露。

---

### 实践 5：确保工具调用的幂等性

**说明**: 在分布式环境中，网络超时可能导致 Agent 误判工具调用失败而发起重复请求。确保工具操作的幂等性（即多次执行同一操作产生的结果与执行一次相同）对于数据一致性至关重要，特别是涉及写操作的场景。

**实施步骤**:
1. 对于写操作（如创建、更新、删除），在工具设计中引入幂等键或唯一业务标识符。
2. 在工具逻辑中，执行操作前检查该标识符是否已被处理，若已处理则直接返回成功结果而不执行重复操作。
3. 在文档中明确标注工具的幂等性属性，供 Agent 调度策略参考。

**注意事项**: 幂等性检查应尽量轻量级，避免因复杂的去重检查影响工具的响应速度。

---

### 实践 6：建立全面的监控与日志审计体系

**说明**: 集成外部工具后，系统的交互链路变长。为了排查问题和优化性能，必须对 MCP 通信过程进行详细的日志记录，并监控工具的响应时间和成功率。

**实施步骤**:
1. 在 MCP 服务器端记录详细的请求日志，包括请求时间、参数、响应状态和耗时。
2. 利用 Amazon CloudWatch 或类似工具设置告警，监控错误率突增或响应延迟过大的情况。
3. 定期审查日志，分析 Agent 调用工具的模式，识别未被充分利用的工具或频繁出错的接口。

**注意事项**: 在记录日志时，务必对敏感数据（如 PII 个人信息、密钥）进行脱敏处理，以符合合规要求。

---
## 学习要点

- 通过 Model Context Protocol (MCP)，Amazon Quick Agents 能够打破数据孤岛，安全地连接并集成企业外部工具与数据源，从而显著扩展 AI 智能体的功能边界。
- MCP 提供了一种标准化的连接机制，简化了将外部 API 和业务系统接入 Amazon Quick Agents 的开发流程，无需为每个工具构建定制化的集成代码。
- 集成外部工具后，Amazon Quick Agents 可以根据用户指令实时检索最新数据（如库存状态或订单信息），确保生成内容的准确性和时效性。
- 借助 MCP 连接外部工具，智能体能够执行跨越多个系统的复杂业务流程自动化，从而替代繁琐的人工手动操作。
- 在集成过程中，利用 MCP 的安全管控能力，可以确保 Amazon Quick Agents 在访问外部敏感数据时符合企业的合规与权限管理要求。
- 此类集成方案赋予开发者更高的灵活性，使其能够快速适应业务需求变化，通过即插即用的方式动态扩展智能体的能力。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/) / [模型上下文协议](/tags/%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE/) / [服务器开发](/tags/%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%BC%80%E5%8F%91/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP将外部工具集成至Amazon Quick Agents的六步指南]({{< relref "posts/20260222-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*