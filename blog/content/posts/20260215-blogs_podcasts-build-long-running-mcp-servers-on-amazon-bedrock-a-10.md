---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理"
date: 2026-02-15T18:26:24+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长时运行", "上下文管理", "AI 智能体"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon Bedrock AgentCore 上集成 Strands Agents，以构建能够处理长时间运行任务的 MCP 服务器。主要内容包括以下三点： 1. **上下文消息策略**：引入了一种机制，用于在服务器和客户端之间维持持续的通信状态，确保在长时间操作中上下文不会丢失。 2. **异步任"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本篇文章中，我们将为您提供一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，用于在服务器与客户端之间维持长时间运行过程中的持续通信。接下来，我们构建一个异步任务管理框架，使您的 AI 智能体能够发起长时间运行的流程，而不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents 将这些策略整合起来，打造生产级的 AI 智能体，使其能够可靠地处理复杂、耗时的操作。

---
## 导语

构建能够处理复杂、耗时任务的 AI 智能体，往往面临着维持上下文与异步管理的挑战。本文将介绍一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的解决方案，重点解析上下文消息策略与异步任务管理框架。通过阅读本文，您将掌握如何构建生产级的长时间运行 MCP 服务器，从而确保智能体在处理复杂工作流时的稳定性与可靠性。

---
## 摘要

本文介绍了如何在 Amazon Bedrock AgentCore 上集成 Strands Agents，以构建能够处理长时间运行任务的 MCP 服务器。主要内容包括以下三点：

1.  **上下文消息策略**：引入了一种机制，用于在服务器和客户端之间维持持续的通信状态，确保在长时间操作中上下文不会丢失。
2.  **异步任务管理框架**：开发了一个框架，允许 AI 代理启动耗时的后台进程，而不会阻塞其他操作，从而保持系统的响应性。
3.  **生产就绪集成**：展示了如何结合上述策略与 Amazon Bedrock AgentCore 及 Strands Agents，构建出能够可靠处理复杂、耗时操作的生产级 AI 代理。

---
## 评论

### 深度评论：Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration

#### 一、 核心观点与架构逻辑

**中心论点**
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构模式，旨在通过上下文消息策略和异步任务管理框架，解决大模型应用中服务器端长时运行任务与客户端实时响应之间的冲突，从而构建持久化的 MCP（Model Context Protocol）服务器。

**支撑理由（基于摘要与行业实践的分析）：**

1.  **突破协议超时限制（技术事实）：** 现有的 LLM 交互协议（如 HTTP 或基础 MCP 实现）通常存在请求超时限制。文章提出的“上下文消息策略”试图通过状态更新机制，允许 Agent 在处理任务时保持连接活性，而非阻塞直至超时。
2.  **计算与交互的解耦（架构设计）：** 通过“异步任务管理框架”，文章主张将复杂的业务逻辑执行与 LLM 的生成过程分离。Agent 可触发后台任务并立即返回确认，随后利用 Strands Agents 的机制在任务完成后更新上下文。
3.  **利用 Bedrock AgentCore 的编排能力（技术推断）：** 文章暗示利用 Bedrock AgentCore 的原生能力管理异步状态，而非构建外部轮询机制，这有助于降低状态管理的复杂性。

**边界条件与潜在挑战（批判性视角）：**

1.  **状态一致性的维护（技术难点）：** 在分布式系统中，维护长时运行的上下文状态极易受网络波动或服务重启影响。若 Bedrock AgentCore 的状态存储缺乏持久化支持，长任务中断可能导致上下文丢失。
2.  **成本与延迟的权衡（工程考量）：** 对于简单查询，引入异步框架和上下文维护可能增加不必要的延迟和 Token 消耗（上下文窗口占用）。并非所有 MCP 交互都需要“长时运行”架构，过度设计会降低系统响应效率。

---

#### 二、 多维度深度评价

**1. 内容深度：架构级解决方案，细节决定成败**
文章触及了当前 Agent 开发中的关键问题：如何处理非瞬时的业务操作。它超越了单纯的 API 调用，上升到了“通信策略”和“任务框架”的架构高度。然而，其方案的严谨性取决于具体的实现细节。若文章未深入探讨错误处理、幂等性和并发控制，其深度仅停留在概念层面。真正的挑战在于如何处理异步回调中的安全验证及上下文注入带来的 Token 成本控制。

**2. 实用价值：填补 AWS 生态 Agent 落地空白**
对于使用 AWS 生态构建 AI 应用的开发者，该文章具有较高的参考价值。Bedrock 在处理需长时间运行的 RAG（检索增强生成）或数据处理任务时，往往缺乏标准范式。文章提供的框架为开发者规避 Lambda 超时或 API Gateway 闲置超时问题提供了直接指导，是将 AI Agent 引入生产环境的参考方案。

**3. 创新性：整合现有技术，拓展协议场景**
“异步任务处理”并非全新概念，但将其与 **MCP (Model Context Protocol)** 和 **Strands Agents** 结合是文章的切入点。MCP 作为较新的标准，其在长连接场景下的最佳实践尚在探索中。文章提出的方案实质上是为 MCP 协议增加了一层“传输层控制”，使其适用于企业级复杂场景，这是对协议应用场景的标准化拓展。

**4. 可读性与逻辑性**
文章遵循了清晰的逻辑递进：问题（长时运行） -> 方案A（上下文策略） -> 方案B（异步框架）。这种“问题-解决方案”的结构符合技术人员的阅读习惯。但需注意，由于涉及 Bedrock AgentCore 和 Strands Agents 两个特定概念，文章对非 AWS 深度用户可能存在一定的认知门槛。

**5. 行业影响：推动 Agent 向工程化演进**
若该模式被采纳，将推动行业从构建简单的“问答机器人”转向能够执行复杂、多步骤业务流程的“自主智能体”。这标志着 AI 应用开发正在向传统的后端微服务架构靠拢，强调了 AI 系统的工程健壮性。

**6. 争议点与局限性**
*   **厂商锁定风险：** 该方案深度依赖 Bedrock AgentCore 和 Strands。相比于开源的 LangChain 或 LangGraph，这种深度绑定可能增加未来的迁移成本。
*   **调试复杂度：** 异步和长时运行的 Agent 系统往往比同步系统更难调试和监控。文章若未提供相应的可观测性方案，生产环境的问题排查将极具挑战。

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点在于解决当前 AI 智能体架构中的一个关键痛点：**如何让基于大语言模型（LLM）的智能体在处理耗时任务时，保持与客户端的持续连接和状态同步，而不是仅仅返回一个最终结果。**

作者提出了一种结合 **Amazon Bedrock AgentCore**、**MCP (Model Context Protocol) 服务器**与 **Strands Agents** 的综合架构方案。这一方案旨在打破传统请求-响应模式在长周期任务中的局限性，实现真正的“长期运行”智能体。

### 核心思想
作者传达的核心思想是**“异步化与上下文连续性”**。在构建复杂的 AI 应用时，智能体往往需要执行一系列跨越数十秒甚至数小时的工具调用（如数据处理、代码部署、复杂检索）。如果客户端在此期间处于“盲等”状态，用户体验将极差。通过引入“上下文消息策略”和“异步任务管理框架”，将任务执行与状态通知解耦，从而赋予 AI 系统类似人类在执行长期任务时的“汇报进度”能力。

### 观点的创新性与深度
该观点的创新性在于将 **MCP** 这一新兴的标准化协议（用于连接 AI 模型与数据源）与 **Amazon Bedrock** 的托管能力及 **Strands**（推测为某种长时序记忆或任务编排机制）进行了深度融合。
*   **深度**：它不仅停留在 API 调用层面，而是深入到了协议层的通信策略（Context Message Strategy），解决了协议本身在长连接场景下的设计缺陷或不足。
*   **重要性**：随着 AI 从“聊天机器人”向“自主智能体”演进，能否可靠地执行长任务是企业级应用落地的分水岭。这篇文章直接切中了从“玩具级 Demo”走向“生产级系统”的关键技术门槛。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **MCP (Model Context Protocol)**：由 Anthropic 推出的开放协议，用于连接 AI 助手与本地数据/工具。在此文中，它作为服务端的标准化接口。
2.  **Amazon Bedrock AgentCore**：AWS 提供的构建智能体的核心框架，负责编排 LLM、工具调用和记忆。
3.  **Strands Agents Integration**：这是文章标题中的特有名词。虽然具体定义需参考全文，但根据上下文推断，Strands 可能指代一种**长时序任务编排技术**或**记忆线程**，用于在 Bedrock 环境中维持任务的持久化状态。
4.  **异步任务管理框架**：用于将同步的 LLM 调用转化为后台异步执行的技术栈。

### 技术原理和实现方式
*   **上下文消息策略**：
    *   **原理**：MCP 协议通常用于数据交换，但在长任务中，连接可能超时。该策略通过在客户端与服务端之间建立一种“心跳”或“中间状态推送”机制，确保 LLM 能够将工具执行的中间结果（如“正在处理第 1 步...”）实时反馈给用户。
    *   **实现**：可能利用了 WebSocket 或 SSE（Server-Sent Events）的变体，或者在 MCP Payload 中嵌入了状态标识符，允许客户端轮询或接收流式更新。

*   **异步任务管理**：
    *   **原理**：当 Bedrock Agent 调用 MCP Server 的工具时，如果该工具耗时较长（例如调起一个 AWS Glue 任务），直接阻塞等待会导致超时。
    *   **实现**：框架接收请求后，立即返回一个“任务 ID”或“已接受”状态，将实际工作放入后台队列（如 AWS SQS + Lambda）。MCP Server 通过 Bedrock AgentCore 的回调接口或 Strands 的状态更新机制，在任务完成时将结果写回。

### 技术难点与解决方案
*   **难点**：**状态一致性**。在异步环境中，LLM 是无状态的，但长任务是有状态的。如何确保 LLM 在任务恢复后能“记得”它在做什么？
*   **解决方案**：利用 **Strands Agents** 的上下文记忆功能，将任务的中间状态持久化存储在 Bedrock 的记忆存储中，使得 LLM 在下一次轮询或回调时能无缝衔接上下文。

### 技术创新点分析
最大的创新点在于**将 MCP 从“数据检索协议”升维为“执行控制协议”**。通常 MCP 用于查询数据库或读取文件，而该架构赋予了它控制复杂、长生命周期工作流的能力，使其成为了 Bedrock Agent 的“远程手”。

---

## 3. 实际应用价值

### 对实际工作的指导意义
对于正在构建企业级 AI 应用的架构师和开发者来说，这篇文章提供了一种**避免重复造轮子**的范式。它展示了如何利用 AWS 的托管服务（Bedrock）配合开源协议（MCP）来构建高可用的 Agent 系统，避免了自行处理复杂的超时、重试和状态管理逻辑。

### 可以应用到哪些场景
1.  **RPA（机器人流程自动化）**：例如 Agent 需要处理一份包含 100 个发票的 PDF，需要几分钟时间，期间需要向用户展示进度。
2.  **DevOps 自动化**：Agent 执行代码部署或基础设施配置，涉及多个步骤的 API 调用，每一步都需要确认状态。
3.  **复杂报告生成**：Agent 需要检索多源数据、进行分析、生成图表，最后合成文档。
4.  **科学计算辅助**：提交长时间的模拟计算任务，并在完成后通知用户。

### 需要注意的问题
*   **成本控制**：长连接和频繁的状态轮询可能会显著增加 API 调用成本和 Token 消耗。
*   **超时配置**：虽然架构支持长任务，但 Bedrock 和负载均衡器（如 ALB）的默认超时时间仍需调整。

### 实施建议
建议采用**事件驱动架构**。不要让 LLM 线程处于阻塞等待状态，而是让 LLM 发起任务后“挂起”，由后端服务完成任务后通过 Webhook 或 SNS 主题唤醒 LLM 继续处理。

---

## 4. 行业影响分析

### 对行业的启示
这标志着 AI Agent 开发正在从**“对话式交互”**向**“任务式交互”**转变。行业开始关注 Agent 的“吞吐量”和“并发处理能力”，而不仅仅是回答的准确性。

### 可能带来的变革
*   **MCP 协议的普及**：该文章若被广泛引用，将推动 MCP 成为连接 LLM 与后端服务的事实标准，特别是在 AWS 生态圈内。
*   **Agent 编排模式的标准化**：Strands Agents 的概念可能会引发关于“Agent 记忆与状态管理”的标准化讨论。

### 对行业格局的影响
这巩固了 AWS 在企业级 AI 基础设施中的地位。通过支持 Strands 和 Bedrock AgentCore，AWS 为企业提供了一个比 OpenAI GPTs 更开放、更可控的长任务运行平台。

---

## 5. 延伸思考

### 引发的其他思考
*   **人机协作的边界**：如果 Agent 能够长时间自主运行，人类介入的时机点如何设计？是仅在异常时介入，还是设置固定的检查点？
*   **多租户隔离**：在长运行任务中，如何确保不同租户的数据和上下文在 MCP Server 中严格隔离？

### 可以拓展的方向
*   **多 Agent 协作**：如果一个任务太长，是否可以由 Strands 协调多个 Bedrock Agents 分别处理子任务，并在此架构下并行工作？
*   **边缘计算结合**：MCP Server 是否可以部署在边缘端，由 Bedrock 核心在云端进行长周期的调度？

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有架构**：检查你目前的 Agent 调用链路，是否存在超过 30 秒的操作。如果有，就必须引入异步框架。
2.  **引入 MCP**：将现有的工具 API 封装为 MCP Server，利用其标准化接口简化与 Bedrock 的集成。
3.  **设计状态机**：为你的长任务设计清晰的状态流转（Pending -> Running -> Succeeded/Failed），并在 Strands 或数据库中记录。

### 具体的行动建议
*   **第一步**：在 Bedrock 中配置 Agent，并启用 Strands（如果可用）或利用 Memory 存储功能。
*   **第二步**：开发一个简单的 MCP Server，实现一个 `long_running_task` 工具，该工具返回 `taskId` 并休眠。
*   **第三步**：实现客户端轮询逻辑或 SSE 推送逻辑，展示任务进度的更新。

### 需要补充的知识
*   **异步编程模型**（如 Python asyncio, JS Promises）。
*   **MCP 协议规范**（了解 Resource, Prompt, Tool 三大核心概念）。
*   **AWS Lambda/SQS 的集成模式**。

---

## 7. 案例分析

### 结合实际案例说明
**场景**：一家电商公司使用 AI Agent 自动处理退款申请。
*   **传统模式**：用户提交退款 -> Agent 调用 API 查询订单 -> 调用 API 审核风险 -> 调用 API 执行退款。如果“审核风险”调用外部征信接口耗时 10 秒，整个请求可能超时断开，用户不知道退款是否成功。
*   **新架构模式**：
    1.  Agent 接收请求，通过 Bedrock AgentCore 发起异步任务。
    2.  MCP Server 返回“任务已接收，ID: 123”。
    3.  前端界面显示“正在审核风险...”。
    4.  Strands 维护“ID: 123”的上下文。
    5.  审核完成后，MCP Server 推送结果，Agent 更新状态为“已退款”，并通知用户。

### 经验教训总结
**失败案例反思**：很多开发者试图通过无限增加 LLM 的 Context Window 来维持长任务状态，结果导致成本高昂且延迟不可控。教训是：**状态管理应下沉到数据库或记忆层，而不是全依赖 LLM 的上下文窗口。**

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**构建基于 Amazon Bedrock AgentCore 和 MCP 的异步任务框架，是实现具备状态感知能力的高可用长运行 AI 智能体的最佳工程实践。**

### 支撑理由与依据
1.  **理由 1：协议局限性**。传统的 HTTP 请求-响应模型无法处理分钟级的任务，会导致超时。
    *   *依据*：网络物理限制及 API Gateway/Load Balancer 的默认超时设置（通常为 29-60 秒）。
2.  **理由 2：用户体验需求**。用户在长时间操作中需要反馈，以建立对系统的信任。
    *   *依据*：HCI（人机交互）心理学研究，2秒以上的无反馈操作会导致用户焦虑。
3.  **理由 3：上下文连续性**。LLM 是无状态的，长任务需要外部机制来

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 Strand 长期运行状态管理

**说明**: 在构建长时间运行的 MCP (Model Context Protocol) 服务器时，Strands Agents 需要维护跨越多次交互的会话状态。由于 Bedrock AgentCore 的无状态特性，必须设计一种机制来持久化和检索 Strand 的执行上下文，以防止在长时间任务中因超时或网络中断导致状态丢失。

**实施步骤**:
1. 设计一个外部状态存储方案（如 Amazon DynamoDB），用于保存每个 Strand 的当前执行指针、变量和中间结果。
2. 在 MCP 服务器逻辑中实现中间件，拦截每个请求以检查并恢复现有的 Strand 上下文。
3. 设置合理的 TTL (Time To Live) 策略，自动清理过期的会话数据以优化成本。

**注意事项**: 避免将整个会话历史存储在单个大字段中，这会影响读取性能。建议采用增量更新策略。

---

### 实践 2：实施严格的超时与异步处理机制

**说明**: 长时间运行的任务（如数据处理或复杂工作流编排）可能会超过 Bedrock 或客户端的请求超时限制。最佳实践是采用“请求-响应”与“异步回调”相结合的模式，确保 MCP 服务器能够立即响应 AgentCore，同时后台任务继续执行。

**实施步骤**:
1. 为 MCP 服务器的每个端点配置较短的最大响应时间（例如 30 秒）。
2. 对于耗时操作，立即返回一个“任务已接受”的响应，其中包含任务 ID 和状态查询端点。
3. 利用 AWS Step Functions 或 Amazon EventBridge 在后台编排长时间运行的逻辑，并在完成后通过回调通知 AgentCore。

**注意事项**: 确保异步任务的状态更新是幂等的，防止重复处理导致的数据不一致。

---

### 实践 3：构建模块化的 Strand 组件库

**说明**: 为了提高代码的可维护性和复用性，应将复杂的业务逻辑拆分为独立的、可组合的 Strand 组件。这使得 Strands 能够像积木一样被动态调用，以应对不同的用户意图。

**实施步骤**:
1. 定义标准化的 Strand 输入和输出接口（JSON Schema），确保所有组件遵循统一的契约。
2. 将通用的功能（如数据提取、API 调用、数据转换）封装为独立的 Strands。
3. 在 MCP 服务器注册表中维护这些组件的元数据，允许 AgentCore 根据上下文动态加载。

**注意事项**: 保持组件的单一职责原则，避免单个 Strand 执行过多不相关的逻辑，以便于错误排查和独立测试。

---

### 实践 4：增强可观测性与日志记录

**说明**: 长期运行的系统难以调试。必须建立完善的可观测性体系，追踪 Strand 在 MCP 服务器上的完整生命周期，包括启动、暂停、恢复和终止状态。

**实施步骤**:
1. 集成 AWS CloudWatch Logs 和 AWS X-Ray，为每个 MCP 请求生成唯一的 Trace ID。
2. 在关键逻辑点（如 Strand 切换、外部 API 调用、状态持久化）输出结构化日志。
3. 配置 CloudWatch Alarms，针对错误率、超时或异常长的执行时间设置告警阈值。

**注意事项**: 日志级别应动态可调。在开发环境使用 DEBUG，生产环境默认使用 INFO 或 WARN，以避免产生高昂的日志存储费用。

---

### 实践 5：设计弹性重试与错误恢复策略

**说明**: 网络波动或下游服务依赖的暂时性故障是不可避免的。MCP 服务器必须具备优雅的错误处理能力，确保 Strands 在遇到 transient error（暂时性错误）时能够自动恢复，而不是直接失败。

**实施步骤**:
1. 实现指数退避算法，用于重试失败的下游 API 调用。
2. 区分可重试错误（如 5xx 服务器错误、限流）和不可重试错误（如 4xx 客户端错误、鉴权失败）。
3. 在 Strand 逻辑中定义“回滚点”或“检查点”，当重试失败时，允许 AgentCore 从上一个稳定状态重新发起。

**注意事项**: 设置最大重试次数限制，防止无限重试循环消耗系统资源。

---

### 实践 6：实施最小权限 IAM 访问控制

**说明**: MCP 服务器作为 AgentCore 与底层 AWS 服务或外部资源之间的桥梁，必须严格遵循最小权限原则，以防止安全漏洞被利用。

**实施步骤**:
1. 为 MCP 服务器创建专用的 IAM 角色，仅授予其执行特定 Strand 所需的权限（如特定的 S3 读写或 DynamoDB 访问）。
2. 避免使用 `*` 通配符，明确限定资源 ARN（Amazon Resource Name）。
3. 定期使用 IAM Access Analyzer 审查权限，移除未使用的策略。

**注意事项**: 如果 MCP 服务器需要访问不同用户的资源，请考虑使用动态 IAM 策略或 Assume Role 机制进行权限隔离。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够处理长期运行任务和复杂工作流的 MCP 服务器。
- 通过将 Strands 的记忆与编排能力与 MCP 协议结合，该架构解决了传统无状态 AI 模型难以维持长期对话上下文和状态的痛点。
- 开发者可以利用 MCP 协议的标准化接口，将 Bedrock 的强大模型能力无缝连接到外部数据源和工具，实现智能体的自动化操作。
- 该方案特别适用于需要多步骤规划、状态跟踪及人机协作的复杂场景，显著提升了 AI 应用在实际业务中的连贯性与可靠性。
- 借助 AgentCore 的托管服务，开发者无需从零构建底层基础设施，即可快速部署具备持久化记忆能力的生成式 AI 应用。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*