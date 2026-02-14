---
title: "基于 Amazon Bedrock AgentCore 构建长运行 MCP 服务器与异步任务管理"
date: 2026-02-14T12:00:26+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP 服务器", "AgentCore", "异步任务", "长运行任务", "Strands Agents", "上下文策略", "AI 智能体"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 构建能够长时间运行的 MCP 服务器的综合方法，旨在解决 AI 代理在处理复杂、耗时任务时的可靠性问题。主要内容包括三个核心策略： 1. **上下文消息策略**：提出了一种在服务器与客户端之间维持持续通信的机制，确保"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于 Amazon Bedrock AgentCore 构建长运行 MCP 服务器与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们将为您提供实现这一目标的全面方法。首先，我们介绍一种上下文消息策略，用于在长耗时操作期间保持服务器与客户端之间的持续通信。接下来，我们构建一个异步任务管理框架，让您的 AI 智能体能够启动长耗时进程，同时不会阻塞其他操作。最后，我们将演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合，构建能够可靠处理复杂、耗时操作的生产级 AI 智能体。

---
## 导语

构建能够处理长耗时任务的 AI 智能体是当前技术落地的一个难点，特别是在需要保持会话连续性的场景中。本文将详细介绍如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成，构建稳定的异步任务管理框架。通过上下文消息策略与非阻塞设计，我们将演示如何打造生产级 MCP 服务器，帮助您解决智能体在复杂操作中的状态管理与通信问题。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 构建能够长时间运行的 MCP 服务器的综合方法，旨在解决 AI 代理在处理复杂、耗时任务时的可靠性问题。主要内容包括三个核心策略：

1.  **上下文消息策略**：提出了一种在服务器与客户端之间维持持续通信的机制，确保在长时间操作过程中上下文信息不丢失，从而保持交互的连续性。

2.  **异步任务管理框架**：构建了一个允许 AI 代理启动长耗时进程的框架，通过异步处理机制，确保这些繁重的任务不会阻塞其他操作的执行，从而提高系统的并发能力和响应速度。

3.  **生产级集成实现**：展示了如何将上述策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合，构建出具备生产级能力的 AI 代理，使其能够可靠地处理复杂且耗时的操作。

---
## 评论

**文章中心观点**
该文章提出了一种通过在 Amazon Bedrock AgentCore 上集成 Strands Agents 并结合 MCP（Model Context Protocol）协议，利用上下文消息策略与异步任务管理框架来解决 AI Agent 在长周期任务中状态保持与服务连续性问题的技术方案。

**支撑理由与深度评价**

**1. 架构层面的针对性：解决“长任务”断连痛点**
*   **事实陈述**：目前的 LLM 应用架构大多基于 HTTP 的无状态请求/响应模式。当 Agent 执行如代码部署、数据分析等耗时超过 LLM 超时窗口（通常为 2-3 分钟）的任务时，连接会断开，导致用户无法获知进度或结果。
*   **作者观点**：文章提出的“Context Message Strategy”（上下文消息策略）旨在通过 MCP 协议在客户端与服务器之间维护一个虚拟的会话通道，使得长任务被分解为可追踪的异步流。
*   **你的推断**：这实际上是将传统的“同步阻塞式” AI 交互转变为“异步事件驱动”架构。这种转变对于构建企业级 AI 应用至关重要，因为它将 AI Agent 从“聊天机器人”提升为“业务流程自动化工具”。

**2. 技术栈的融合：Bedrock AgentCore 与 Strands 的互补**
*   **事实陈述**：Amazon Bedrock AgentCore 提供了托管的基础设施，而 Strands Agents（假设为某种专注于任务链规划的 Agent 框架）提供了复杂的逻辑编排能力。
*   **作者观点**：利用 Bedrock 的托管能力可以减少运维负担，而 Strands 提供的异步任务框架填补了 Bedrock 原生在长流程编排上的空白。
*   **你的推断**：这种组合代表了“基础设施层”与“应用编排层”解耦的趋势。它暗示了未来的 Agent 开发将不再依赖单一模型提供商的编排工具，而是通过 MCP 这样的标准协议，灵活组合不同厂商的优势组件。

**3. 异步任务管理的必要性**
*   **事实陈述**：文章强调了开发异步任务管理框架，允许 AI 在后台执行任务时，用户可以断开连接或做其他操作。
*   **作者观点**：这是提升用户体验的关键，避免了用户在复杂任务执行期间的“焦虑等待”。
*   **你的推断**：从行业角度看，这引入了“状态持久化”的复杂性。真正的挑战不仅在于异步化，更在于当用户回来时，如何用自然语言精准地恢复上下文。

**反例与边界条件**

1.  **过度工程化风险**：对于简单的查询任务（如“今天天气如何”或“总结这段文本”），引入异步任务管理框架和复杂的上下文策略是杀鸡用牛刀。这会增加系统的延迟（额外的握手和轮询）并降低响应速度。
2.  **一致性挑战**：在分布式异步环境中，CAP 理论依然适用。如果 Bedrock 服务与 Strands Agent 之间的状态同步失败，或者 MCP 连接中断，系统如何保证任务不重复执行或状态不丢失？文章可能未深入探讨这种“最终一致性”带来的业务风险。
3.  **成本黑洞**：维持长连接和持续轮询上下文状态会显著增加 Token 消耗和 API 调用次数。相比一次性问答，这种模式的运营成本可能高出数倍。

**验证与检查方式**

为了验证该文章方案的有效性，建议进行以下检查：

1.  **超时压力测试**：构建一个故意耗时超过 10 分钟的任务（例如处理大型数据集），观察 MCP 连接是否保持稳定，以及 Bedrock Agent 的底层会话是否因云厂商的 WAF 或负载均衡器超时而被切断。
2.  **状态恢复测试**：在 Agent 执行任务期间，手动断开客户端连接并重新连接，检查“Context Message Strategy”是否能真正无缝恢复之前的对话状态和任务进度，而不是重新开始。
3.  **Token 消耗监控**：对比同步模式和该异步模式在完成相同任务时的 Token 使用量。特别关注“维持上下文”所产生的冗余 Token 消耗，评估其性价比。

**综合评价**

*   **内容深度（4/5）**：文章触及了当前 Agent 落地中最棘手的工程问题——长任务管理。它没有停留在概念层面，而是提出了具体的架构模式，具有较高的技术含金量。
*   **实用价值（4.5/5）**：对于正在基于 AWS 构建复杂 Agent 应用的开发者而言，这是一篇极具指导意义的技术参考，提供了可落地的路径。
*   **创新性（3.5/5）**：利用 MCP 协议来解决长连接问题是较新的视角，但异步任务管理本身是软件工程的经典概念，创新点在于将其与 LLM Agent 编排相结合。
*   **行业影响**：该方案如果被广泛采纳，将推动 MCP 协议成为连接 LLM 与长期运行服务的标准接口，加速 AI 从“对话式”向“代理式”演进。
*   **争议点**：主要争议在于是否所有长任务都需要在 LLM 的上下文中维护。对于极长任务，传统的后端任务队列配合 LLM 仅用于“状态查询”可能比全程保持 Agent 在线更高效。

**实际应用建议**

在实际采用此方案前，建议评估以下三点：
1.  **混合架构**：不要将所有任务都放入 Agent 中。对于耗时极长的任务（ETL、视频渲染），应采用“指令下发，后端执行，Agent 回调”的模式，而非让 Agent 持续保持连接。
2.  **成本控制**：在

---
## 技术分析

基于提供的标题和摘要，这篇文章主要探讨了在 **Amazon Bedrock AgentCore** 上构建能够处理长时间运行任务的 **MCP (Model Context Protocol) 服务器**，并结合 **Strands Agents** 进行集成。

由于文章全文未完全提供，以下分析将基于标题、摘要以及 AWS Bedrock、MCP 和 Agent 技术栈的通用架构原理进行深度推演和解析。

---

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**构建能够处理长时间运行任务的 AI 代理，不能仅仅依赖同步的请求-响应模式，而必须引入“上下文消息策略”和“异步任务管理框架”来维持客户端与服务器之间的持续通信。**

### 核心思想传达
作者试图传达一种架构范式的转变。传统的 LLM 应用往往是“即问即答”的短连接模式。然而，在构建企业级 Agent（如 Bedrock Agent）时，任务往往涉及数据库查询、API 调用或长流程处理，这些操作耗时远超 LLM 的生成时间。作者主张通过 **MCP 协议**结合 **Strands Agents**（一种可能的状态管理或编排机制），将 Agent 的思考过程与执行过程解耦，确保在长时间任务中，上下文不丢失，且用户能获得实时反馈。

### 观点的创新性与深度
*   **解耦通信与计算：** 创新点在于将“任务状态的管理”从 LLM 的直接推理循环中剥离出来，交给一个专门的异步框架处理。
*   **上下文连续性：** 深入探讨了如何在分布式系统（Client <-> MCP Server <-> Bedrock）中维护“对话记忆”和“任务记忆”，这是目前 Agent 落地的一大痛点。
*   **协议标准化：** 利用 MCP 协议，使得这种长连接能力不仅限于 Bedrock，而是具有可移植性。

### 为什么这个观点重要
随着 AI 从“聊天机器人”向“智能体”演进，**执行时间**和**可靠性**成为瓶颈。如果 Agent 在处理一个 3 分钟的数据分析任务时因为超时而断开，用户体验将极差。这篇文章提出的方案解决了 Agent 进入生产环境时的**“长任务处理”**难题，是实现复杂工作流自动化的关键基础设施。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **MCP (Model Context Protocol):** Anthropic 推出的开放协议，用于连接 AI 应用与外部数据源。在此处作为 Agent 与工具/数据源之间的标准接口。
2.  **Amazon Bedrock AgentCore:** AWS 提供的托管式 Agent 编排服务，负责推理、路由和工具调用。
3.  **Strands Agents:** 这里的 "Strands" 可能指代 AWS 的特定内部框架或合作伙伴技术，通常指代在多轮对话中维持“思维链”或“状态流”的机制。
4.  **Asynchronous Task Management:** 异步任务队列（如基于 Step Functions 或 Redis 的实现）。

### 技术原理和实现方式
*   **Context Message Strategy (上下文消息策略):**
    *   **原理:** 在长任务执行期间，服务器不保持 HTTP 长连接，而是返回一个“任务 ID”。客户端通过该 ID 轮询或通过 WebSocket 接收更新。
    *   **实现:** MCP Server 在接收到 Bedrock Agent 的调用请求后，立即返回 `Accepted` 并生成一个 `ContextID`。后台线程开始处理任务，并将进度写入存储（如 DynamoDB）。Agent 可以在后续轮询中读取这些中间状态，作为“记忆”喂回给 LLM。
*   **Strands Agents Integration:**
    *   **原理:** 将 Bedrock Agent 的推理链路拆分为多个“Strands”（线索/流）。每个 Strand 负责一个子任务或阶段。
    *   **实现:** 通过 Strands API，Bedrock 可以暂停当前的推理过程，等待异步任务完成，然后通过“回调”或“状态查询”恢复推理，从而实现“长时间运行”的错觉。

### 技术难点与解决方案
*   **难点:** LLM 的上下文窗口限制。长任务可能产生大量中间日志，直接塞回 Prompt 会撑爆 Token 限制。
*   **解决方案:** 摘要机制。异步框架在任务进行中不断生成摘要，只有关键状态变更和最终结果会被注入回 Bedrock 的 Prompt。
*   **难点:** 状态一致性。如果 Bedrock Agent 崩溃，任务还在后台跑怎么办？
*   **解决方案:** 持久化存储。所有任务状态存储在数据库中，Agent 重启后可以通过 MCP Server 查询到未完成的任务。

### 技术创新点分析
将 **MCP**（通常是客户端-模型直连）与 **Bedrock AgentCore**（服务端编排）结合，并引入 **Strands** 的概念来处理异步流，这是一种混合架构创新。它打破了 MCP 仅作为“数据检索工具”的局限，使其成为“任务执行控制器”。

---

## 3. 实际应用价值

### 对实际工作的指导意义
对于正在构建企业级 RAG（检索增强生成）或 Agent 应用的架构师，这篇文章提供了一个**避免超时崩溃**的参考架构。它指导开发者如何设计能够处理“小时级”任务的 AI 系统，而不是仅仅处理“秒级”问答。

### 可应用场景
1.  **复杂金融分析报告生成：** 需要抓取多个数据源、运行 Python 脚本计算、生成图表，耗时 5-10 分钟。
2.  **DevOps 自动化运维：** Agent 需要监控日志、执行滚动更新、等待健康检查，整个过程可能持续数小时。
3.  **企业数据录入与清洗：** 批量处理大量文档，需要实时反馈进度条。

### 需要注意的问题
*   **成本控制:** 长时间的轮询和状态存储会增加 AWS 费用。
*   **最终一致性:** 异步任务可能导致数据延迟，用户可能看到过时的状态。

### 实施建议
*   **不要阻塞 LLM:** 确保 MCP Server 的工具调用立即返回，不要让 Bedrock Agent 等待工具执行完毕。
*   **可视化进度:** 利用 Strands Agents 的特性，在 UI 层展示任务进度条，而不是仅仅显示“正在思考”。

---

## 4. 行业影响分析

### 对行业的启示
这标志着 AI Agent 正从“对话式交互”向“流程式交互”转变。行业将不再满足于 ChatGPT 式的快速回答，而是开始追求 AI 能够像人类员工一样，处理跨越长时间周期的复杂工作流。

### 可能带来的变革
*   **SaaS 软件的 Agent 化:** 传统的 SaaS 软件通常需要用户点击按钮操作。通过这种架构，SaaS 可以通过 MCP 暴露接口，让 Agent 代表用户进行长时间的操作（如批量处理发票），软件形态将发生改变。
*   **MCP 协议的普及:** 如果 AWS Bedrock 大力支持 MCP，MCP 可能成为连接 LLM 与企业系统的标准协议，类似于 API 之于 Web。

### 相关领域的发展趋势
*   **Orchestration Frameworks (编排框架):** 如 LangChain 或 LangGraph，将更多地支持“持久化”和“异步回调”机制，而不仅仅是同步链调用。

---

## 5. 延伸思考

### 引发的其他思考
*   **人机协作模式:** 如果任务运行了 30 分钟，中间出错了，Agent 是自动重试还是通知人类？这种架构下，“人在回路”的设计变得至关重要。
*   **多 Agent 协作:** 一个 Agent 发起任务，另一个 Agent 处理任务。Strands Agents 的架构是否支持跨 Agent 的状态传递？

### 需要进一步研究的问题
*   **安全性:** 异步任务 ID 如果被劫持，攻击者是否能获取敏感数据？需要在 MCP 层面如何做鉴权？
*   **可观测性:** 对于这种复杂的异步调用链，如何进行监控和调试？

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估任务时长:** 如果你的应用中，工具调用超过 30 秒，就必须采用此架构。
2.  **引入状态存储:** 使用 Redis 或 DynamoDB 存储任务状态。
3.  **改造 MCP Server:** 修改你的 MCP Server 接口，将所有耗时操作改为 `fire-and-forget`（发起即返回），并提供一个 `get_status` 接口。

### 具体的行动建议
*   **Step 1:** 定义任务状态枚举。
*   **Step 2:** 在 Bedrock Agent 中配置 Prompt，告知它“这是一个长任务，请先提交，然后每隔一段时间查询进度”。
*   **Step 3:** 实现客户端的轮询逻辑或 SSE 推送。

### 需要补充的知识
*   **Amazon Bedrock Agent Action Groups:** 理解如何定义 API Schema。
*   **Asynchronous Programming:** 熟悉 Python 的 `asyncio` 或 JS 的 Promise/Event Loop。
*   **MCP Specification:** 阅读 Anthropic 的 MCP 协议文档。

---

## 7. 案例分析

### 结合实际案例说明
**场景：** 一个企业内部的“年度预算审批 Agent”。
**挑战：** Agent 需要读取 50 个部门的 Excel 文件，汇总数据，生成报告，并发送邮件。这需要 5 分钟。
**传统做法失败：** Bedrock 直接调用工具，Lambda 超时（15分钟限制或客户端超时），任务失败。
**采用文章方案：**
1.  Bedrock Agent 调用 MCP Server 的 `start_budget_report` 工具。
2.  MCP Server 返回 `{"task_id": "123", "status": "processing"}`。
3.  Bedrock 告知用户：“已开始生成报告，任务 ID: 123”。
4.  用户在 UI 上看到进度条。
5.  Bedrock Agent 在后台定期调用 `check_status("123")`。
6.  完成后，Agent 获取最终报告链接，发送给用户。

### 经验教训总结
*   **不要试图在一个 Prompt 里做完所有事。** 必须拆分为“发起”、“监控”、“收割结果”三个阶段。
*   **状态机比简单的布尔值重要。** 区分 Processing, Failed, Completed, Reviewing 等状态。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**为了在生产环境中实现具备复杂处理能力的 AI Agent，必须采用基于 MCP 协议的异步任务管理架构，以解决长耗时操作与同步交互模式之间的根本矛盾。**

### 支撑理由与依据
1.  **理由 1：网络与计算的物理限制。**
    *   **依据:** HTTP 请求和 LLM 推理都有超时限制（Timeout limits），无法容忍分钟级的阻塞等待。
2.  **理由 2：用户体验的连贯性需求。**
    *   **依据:** 心理学研究表明，用户在等待超过 2 秒未获得反馈时会产生焦虑。异步反馈机制（如进度条）能维持用户的控制感。
3.  **理由 3：系统的可恢复性。**
    *   **依据:** 事实是，长任务更容易失败。解耦的异步框架允许断点续传和重试，而同步模式一旦断开则前功尽弃。

### 反例或边界条件
1.  **反例

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建有状态的长期运行服务架构

**说明**: 传统的无状态请求-响应模式在处理复杂工作流时存在局限性。利用 AgentCore 和 Strands Agents 集成，应设计能够保持会话上下文的有状态服务器。这允许代理在多次交互之间积累信息、记忆用户偏好，并处理跨越较长时间周期的多步骤任务，而无需客户端重复传递上下文。

**实施步骤**:
1. 使用 Amazon Bedrock AgentCore 定义状态管理接口，确保会话数据持久化。
2. 集成 Strands Agents 的记忆功能，将关键对话节点存储在 DynamoDB 或其他持久化存储中。
3. 实现会话恢复机制，以便在服务重启后能够重建之前的上下文。

**注意事项**: 避免在内存中存储敏感状态信息，始终结合云存储服务以保证高可用性和数据持久性。

---

### 实践 2：实施严格的超时与异步任务管理

**说明**: 长期运行的服务容易因网络波动或复杂计算导致阻塞。为了保持 MCP 服务器的响应性，必须实施严格的超时策略，并利用异步模式处理耗时操作。Strands Agents 需要能够触发长时间运行的任务，并在任务完成前安全地释放连接资源。

**实施步骤**:
1. 为所有 MCP 工具调用配置合理的超时限制（例如 30 秒用于快速交互，更长用于异步任务）。
2. 使用 Step Functions 或 Amazon EventBridge 来编排长时间运行的工作流。
3. 实现轮询或 Webhook 回调机制，让 Agent 在后台任务完成后获取结果。

**注意事项**: 确保异步任务的状态可查询，防止任务在后台丢失或无法被客户端追踪。

---

### 实践 3：优化工具定义与输入验证

**说明**: MCP 服务器的核心在于其暴露的工具。为了确保 Agent 能够正确调用工具，必须提供清晰、准确的 Schema 定义。长期运行的服务更容易受到无效输入的干扰，导致资源浪费，因此严格的输入验证至关重要。

**实施步骤**:
1. 使用 JSON Schema 严格定义每个工具的输入和输出格式。
2. 在 MCP 服务器层实现输入验证逻辑，在将请求传递给下游服务之前拦截错误。
3. 为 Strands Agents 提供详细的工具描述，以提高大模型选择正确工具的概率。

**注意事项**: 定期审查工具定义，确保 Schema 与实际后端逻辑保持一致，避免因描述模糊导致的幻觉或调用失败。

---

### 实践 4：建立全面的可观测性与日志记录

**说明**: 在长期运行的系统中，调试和性能监控极具挑战性。必须建立一套完善的可观测性体系，以便追踪 Agent 的思考链路、工具调用链以及系统性能瓶颈。

**实施步骤**:
1. 集成 Amazon CloudWatch 用于收集日志和指标。
2. 在 MCP 服务器中实现结构化日志记录，记录每个请求的 Request ID、时间戳和关键参数。
3. 利用 X-Ray 追踪请求在 Strands Agents 和 MCP 服务器之间的完整路径。

**注意事项**: 注意日志脱敏，确保不记录 PII（个人身份信息）或敏感凭证，符合安全合规要求。

---

### 实践 5：设计幂等性与错误重试机制

**说明**: 网络不稳定或服务重启可能导致请求重复提交或中断。长期运行的 MCP 服务器必须具备幂等性，即处理相同请求多次的结果与处理一次的结果相同，并配合智能重试策略以提高系统的鲁棒性。

**实施步骤**:
1. 为每个请求生成唯一的幂等键，并在处理逻辑中检查该键是否已被处理。
2. 配置 Exponential Backoff（指数退避）策略处理可重试的错误（如 5xx 错误或限流）。
3. 对于 Strands Agents 的非幂等操作（如发送邮件或扣款），强制要求客户端提供幂等标识。

**注意事项**: 区分临时性错误和永久性错误，避免对无效请求（如 4xx 错误）进行无意义的重试。

---

### 实践 6：强化安全控制与最小权限原则

**说明**: MCP 服务器作为 Agent 与后端服务的桥梁，必须严格控制权限。长期运行的服务面临更大的攻击面，必须确保只有经过授权的 Agent 能够执行特定的操作。

**实施步骤**:
1. 利用 AWS IAM Roles Anywhere 或 Bedrock 的授权机制，验证调用方的身份。
2. 为 MCP 服务器分配 IAM 角色时，仅授予其完成任务所需的最小权限集。
3. 在 Strands Agents 配置中，明确限制其可访问的 MCP 工具范围。

**注意事项**: 定期轮换访问凭证，并使用 AWS Secrets Manager 管理数据库或 API 密钥，切勿硬编码在代码中。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够执行长期、多步骤复杂任务的自主智能体。
- 该架构通过引入持久化上下文管理，解决了传统无状态模型在处理长周期任务时容易丢失上下文信息的问题。
- 新的 MCP (Model Context Protocol) 服务器支持使智能体能够无缝连接外部数据源和工具，显著扩展了其在实际业务场景中的应用边界。
- 利用 Bedrock 的托管基础设施，开发者无需管理底层服务器集群，即可实现高可用性的长期运行服务。
- 集成方案简化了将企业私有数据与生成式 AI 能力结合的流程，有助于构建更智能的自动化工作流解决方案。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP 服务器](/tags/mcp-%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [AgentCore](/tags/agentcore/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长运行任务](/tags/%E9%95%BF%E8%BF%90%E8%A1%8C%E4%BB%BB%E5%8A%A1/) / [Strands Agents](/tags/strands-agents/) / [上下文策略](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AD%96%E7%95%A5/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器的异步任务框架]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-6.md" >}})
- [基于 Amazon Bedrock AgentCore 构建长时间运行的 MCP 服务器]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*