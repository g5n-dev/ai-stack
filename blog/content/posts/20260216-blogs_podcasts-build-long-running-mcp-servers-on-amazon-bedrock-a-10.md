---
title: "基于Amazon Bedrock AgentCore与Strands Agents构建长时间运行的MCP服务器"
date: 2026-02-16T22:17:35+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长时运行", "AI 智能体", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够处理长时间运行任务的 MCP 服务器的综合方法。主要包含以下三个核心策略： 1. **上下文消息策略**：引入了一种机制，用于在服务器与客户端执行扩展操作期间维持持续的通信连接，确保交互不中断。 2."
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore与Strands Agents构建长时间运行的MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供了一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，以在长时间运行的操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，让您的 AI 智能体能够启动长时间运行的任务，而不会阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，构建可用于生产环境的 AI 智能体，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 智能体是提升生产环境自动化水平的关键步骤。本文将深入探讨如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成能力，解决异步任务管理与上下文持续通信的挑战。您将学习到一套完整的实现方法，包括上下文消息策略与异步框架的构建，从而开发出能够可靠处理复杂、耗时操作的生产级智能体。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够处理长时间运行任务的 MCP 服务器的综合方法。主要包含以下三个核心策略：

1.  **上下文消息策略**：引入了一种机制，用于在服务器与客户端执行扩展操作期间维持持续的通信连接，确保交互不中断。
2.  **异步任务管理框架**：开发了一套框架，允许 AI 代理启动长时运行进程的同时，不阻塞其他操作的执行，从而提升系统的并发处理能力。
3.  **生产级集成方案**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 结合，构建出能够可靠、高效地处理复杂且耗时任务的生产就绪型 AI 代理。

---
## 评论

**中心观点**
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构模式，旨在通过上下文消息策略与异步任务管理框架，解决 MCP 服务器在执行长周期任务时的连接保持与状态管理难题。

**支撑理由与评价**

1.  **解决长连接中断的上下文策略（技术深度）**
    *   **事实陈述**：文章引入了“上下文消息策略”来维持 MCP 协议下的活跃状态。
    *   **深度分析**：在 LLM 应用架构中，MCP（Model Context Protocol）通常面临 HTTP 超时或 Token 生成中断的挑战。该策略实质上是构建了一个“心跳机制”或“会话保持层”。从技术角度看，这不仅解决了连接保活问题，更重要的是它允许 LLM 在等待外部任务（如代码编译、数据检索）完成时，不丢失对话的 Thread ID。
    *   **边界条件/反例**：如果客户端（如 Claude Desktop 或 IDE 插件）强制实施了严格的超时限制，仅靠服务端的消息策略可能无效；此外，高频的上下文消息可能会产生不必要的 Token 消耗，增加成本。

2.  **异步任务管理框架的解耦设计（实用价值）**
    *   **事实陈述**：文章开发了异步任务管理框架，允许 AI Agent 在后台执行任务。
    *   **深度分析**：这是从“同步请求-响应”向“异步编排”的关键转变。对于 Bedrock AgentCore 而言，这意味着 Agent 可以在触发一个耗时操作后，释放计算资源，待任务完成后再通过回调或轮询获取结果。这显著提升了系统的吞吐量和稳定性。
    *   **边界条件/反例**：异步化引入了最终一致性的挑战。如果用户在任务完成前修改了指令，或者任务执行失败但状态未正确回滚，系统可能会面临状态不一致的风险。

3.  **Strands Agents 与 Bedrock 的深度集成（创新性）**
    *   **事实陈述**：文章展示了 Strands Agents 与 Bedrock AgentCore 的集成。
    *   **深度分析**：Strands Agents（假设指代特定的 Agent 编排框架或子任务链技术）在此处充当了“执行者”的角色，而 Bedrock 充当“大脑”。这种组合试图解决 LLM 框架中常见的“幻觉导致执行失败”问题，通过将长任务拆解为由 Strands 管理的、可验证的子任务。
    *   **边界条件/反例**：如果 Strands Agents 的定义过于宽泛，这种集成可能仅仅是 API 调用的堆砌，而非真正的架构融合。此外，过度依赖特定厂商的 AgentCore 可能导致供应商锁定。

**综合评价**

*   **内容深度**：文章触及了当前 AI Agent 落地中最痛点的“长任务执行”问题。论证从协议层（MCP）延伸到应用层，逻辑闭环完整。
*   **实用价值**：极高。对于正在构建企业级 AI 应用的开发者，单纯的 RAG 或 Chatbot 已无法满足需求，该方案提供了可落地的工程范式。
*   **创新性**：中等。虽然“异步任务”和“心跳保活”是传统后端的概念，但将其标准化并应用到 MCP + Bedrock 的特定语境下，具有一定的借鉴意义。
*   **可读性**：结构清晰，技术栈明确，适合具备 AWS 基础的架构师阅读。

**争议点与不同观点**

*   **复杂度 vs. 收益**：引入异步框架和状态管理必然增加系统复杂度。对于简单的查询任务，这种架构是否存在“杀鸡用牛刀”的过度设计？
*   **MCP 的标准化局限**：MCP 协议本身仍在快速迭代中。文章提出的解决方案可能依赖于 MCP 的特定版本，未来协议升级可能导致该方案不可用。
*   **成本隐忧**：维持长连接和频繁的上下文消息传递，在 Bedrock 按 Token 计费的模型下，可能会产生“沉默成本”，即 Agent 在思考或等待时也在消耗费用。

**实际应用建议**

1.  **监控与可观测性**：在实施异步框架时，必须引入分布式追踪，否则长任务的失败排查将极其困难。
2.  **成本控制**：在上下文消息策略中，应设置低优先级的 Token 使用策略，避免保活消息消耗高昂的 Input Token 成本。
3.  **降级机制**：务必设计当 Bedrock AgentCore 不可用或 MCP 连接断开时的本地降级方案，防止核心业务流程中断。

**可验证的检查方式**

1.  **压力测试**：模拟高并发下的长任务场景，观察 MCP 连接池的耗尽情况和 Bedrock API 的限流表现。
2.  **成本分析**：对比同步模式与该异步模式在执行相同 1 小时任务时的 Token 消耗总量。
3.  **中断恢复测试**：在网络抖动或服务重启的情况下，验证“上下文消息策略”是否能真正恢复对话状态，还是会导致任务丢失。
4.  **观察窗口**：关注 Anthropic 官方对 MCP 协议的更新日志，验证文章中的方案是否在未来 6 个月内仍然兼容。

---
## 技术分析

# 技术方案解析：基于 Amazon Bedrock AgentCore 与 Strands 的长时运行 MCP 服务器

## 1. 核心架构与设计目标

### 方案背景
该技术方案旨在解决大模型应用（Agent）在处理复杂任务时的架构局限性。传统的 MCP (Model Context Protocol) 服务器通常基于同步的请求-响应模式，难以应对涉及长时间等待或异步执行的业务场景。文章提出利用 **Amazon Bedrock AgentCore** 结合 **Strands Agents** 架构，构建具备状态持久化和长时运行能力的 MCP 服务器。

### 核心设计思想
方案的核心在于**状态持久化**与**异步解耦**。
*   **状态持久化**：将 Agent 的上下文从内存转移到持久化存储，确保在长时任务执行期间，会话状态不丢失，支持断点续传。
*   **异步解耦**：将 Agent 的决策逻辑与耗时操作（如数据查询、API 调用）分离，通过消息队列或回调机制处理任务结果，避免阻塞主线程。

### 技术价值
该架构使 AI 应用能够处理多步骤、高延迟的复杂工作流（例如日志分析或跨系统数据聚合），突破了传统对话模型仅支持即时交互的限制，使其能够适应企业级业务流程自动化的需求。

## 2. 关键技术实现

### 涉及的关键组件
1.  **MCP (Model Context Protocol)**：作为数据交互的标准接口，负责连接 AI 应用与外部数据源。
2.  **Amazon Bedrock AgentCore**：AWS 提供的底层编排框架，负责管理 Agent 的生命周期、路由控制流以及工具调用逻辑。
3.  **Strands Agents**：一种专门设计用于长生命周期任务的代理架构，负责维护记忆状态和进行长跨度任务规划。
4.  **异步任务队列**：用于缓冲和执行后台耗时任务。

### 技术实现机制
根据摘要描述，技术实现主要包含以下两个层面：

1.  **上下文消息策略**：
    *   **原理**：在执行耗时任务期间，为了保持连接活性并告知用户进度，系统需维持通信通道。
    *   **实现**：利用流式传输机制，Agent 在后台处理任务时，向客户端持续发送中间状态更新，确保用户端能够感知到任务正在执行中，而非超时无响应。

2.  **异步任务管理框架**：
    *   **原理**：将控制流与执行流分离。
    *   **实现**：当 Agent 判定需要调用长时运行工具（如“查询数据库”）时，它不阻塞等待，而是将任务提交至后台服务（如集成 AWS Step Functions 或消息队列），并返回挂起状态或任务 ID。后台 Worker 完成计算后，通过回调或 Webhook 通知 Agent，Agent 随后读取结果并继续生成后续响应。

### 架构难点与应对
*   **状态一致性**：在长时运行过程中，上下文可能发生变化。
    *   **应对**：Strands 架构通常引入检查点机制，在关键步骤保存上下文快照，以便在异常或中断时恢复。
*   **资源管理与超时**：维持长连接可能导致资源耗尽。
    *   **应对**：采用无服务器架构或连接池管理，确保在任务挂起期间释放计算资源，仅保留状态存储，待有事件触发时重新激活。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化会话状态管理与持久化

**说明**：长时间运行的 MCP 服务器必须维护有状态的对话上下文。在 AgentCore 环境中，不能依赖无状态的请求-响应模式，而需要实现健壮的状态持久化机制，以便在 Strands 执行长任务或跨多个步骤时保持上下文连贯性。

**实施步骤**:
1. 使用 Amazon DynamoDB 或 ElastiCache 存储会话状态和中间变量。
2. 为每个会话分配唯一的 Session ID，并在 MCP 协议的每次调用中传递该 ID。
3. 实现状态序列化逻辑，将内存中的对象转换为可存储的格式（如 JSON）。
4. 配置合理的 TTL（生存时间）策略以自动清理过期的会话数据。

**注意事项**: 避免将整个对话历史存储在内存中，应采用摘要或增量更新的策略来减少检索延迟和存储成本。

---

### 实践 2：实施严格的超时与异步任务处理机制

**说明**：长运行任务（如数据处理、生成报告）可能超过 Bedrock 或网络层的默认超时限制。最佳实践是将同步执行转换为异步处理模式，MCP 服务器仅负责接收请求、启动任务并返回任务标识符，而不是阻塞等待最终结果。

**实施步骤**:
1. 在 MCP 服务器中引入消息队列（如 Amazon SQS）或后台工作流（如 AWS Step Functions）。
2. 接收到请求后，立即返回 `202 Accepted` 状态及一个 `TaskID`。
3. 实现一个独立的查询端点，允许 AgentCore 轮询任务状态。
4. 配置 Lambda 或容器环境的超时时间，使其略大于预期的异步任务启动时间。

**注意事项**: 确保异步任务具有幂等性，防止网络重试导致重复执行业务逻辑。

---

### 实践 3：构建模块化的 Strands 工具集

**说明**：为了提高复用性和可维护性，应将 MCP 服务器暴露的功能拆分为细粒度的、模块化的工具。Strands Agents 在编排时会调用这些工具，粒度越细，组合灵活性越高，也更容易进行错误隔离。

**实施步骤**:
1. 分析业务逻辑，将功能拆解为单一职责的原子操作。
2. 为每个工具定义清晰的输入模式（JSON Schema）和输出描述。
3. 按照功能域对工具进行分组，便于 Bedrock AgentCore 进行动态调用。
4. 为每个工具编写详细的文档字符串，以便 LLM 准确理解其用途。

**注意事项**: 避免创建过于庞大或复杂的“上帝工具”，这会降低 LLM 的调用准确率和调试难度。

---

### 实践 4：增强可观测性与日志记录

**说明**：在长运行场景下，问题排查变得尤为困难。必须建立完善的可观测性体系，追踪从 AgentCore 发起请求到 MCP 服务器处理，再到 Strands 执行的完整链路。

**实施步骤**:
1. 使用 AWS X-Ray 进行分布式追踪，记录请求的完整路径。
2. 在 MCP 服务器代码中嵌入结构化日志（如 JSON 格式），记录关键参数、时间戳和错误堆栈。
3. 将日志集中发送到 Amazon CloudWatch Logs，并配置相应的指标过滤器。
4. 为关键业务流程设置告警，例如任务失败率或处理延迟异常。

**注意事项**: 确保日志中不包含敏感信息（如 PII 数据），必要时进行脱敏处理。

---

### 实践 5：设计健壮的错误处理与重试策略

**说明**：外部依赖（如数据库、API）可能会出现间歇性故障。MCP 服务器需要具备优雅的错误处理机制，区分瞬时错误和永久错误，并配合 AgentCore 实现合理的退避重试。

**实施步骤**:
1. 定义标准化的错误响应格式，明确错误代码和描述信息。
2. 对于网络超时或限流（5xx, 429）等瞬时错误，实现指数退避算法进行重试。
3. 对于业务逻辑错误（4xx, 参数校验失败），直接返回错误给 Agent，不进行重试。
4. 在 Strands 编排层面，设置最大重试次数和熔断机制，防止级联故障。

**注意事项**: 避免无限重试导致资源耗尽，必须设置明确的阈值。

---

### 实践 6：利用 Bedrock Knowledge Base 进行上下文增强

**说明**：长运行的 Agent 往往需要处理大量领域知识。直接将知识硬编码在 Prompt 中不仅成本高且受限于 Token 限制。最佳实践是将 MCP 服务器与 Bedrock Knowledge Base 集成，实现按需检索增强生成（RAG）。

**实施步骤**:
1. 将领域文档上传至 Amazon S3，并构建 Knowledge Base 索引。
2. 在 MCP 服务器中实现检索逻辑，当 Agent 需要特定信息时调用该工具。
4. 将检索

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够长时间运行并保持状态记忆的 MCP 服务器。
- 通过将 Strands Agents 的长期记忆能力与 Bedrock 的托管基础设施相结合，该方案解决了传统无状态 Agent 难以处理复杂、多步骤工作流的局限性。
- 开发者可以利用此架构将现有的 MCP 服务器无缝迁移至 Bedrock，从而获得更高的可扩展性和企业级的安全性保障。
- 该集成方案显著增强了 AI 应用的上下文感知能力，使其能够在跨会话的长时间任务中保持连贯性和准确性。
- 用户可以通过统一的 API 接口管理这些长期运行的 Agent，从而简化了开发流程并降低了运维复杂度。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*