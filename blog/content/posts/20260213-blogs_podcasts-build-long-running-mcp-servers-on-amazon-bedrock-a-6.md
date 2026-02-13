---
title: "基于Amazon Bedrock AgentCore构建长运行MCP服务器的异步任务框架"
date: 2026-02-13T19:28:07+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长运行任务", "AI 代理", "上下文策略"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种在 Amazon Bedrock AgentCore 上集成 Strands Agents 以构建长期运行 MCP 服务器的综合方法。主要内容包含以下三个方面： 1. **上下文消息策略**：引入了一种策略，用于在服务器与客户端执行扩展操作期间维持持续的通信，确保状态同步。 2. **异步任务管理框架**"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长运行MCP服务器的异步任务框架

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们为您提供了一套全面的方法来实现这一目标。首先，我们将介绍一种上下文消息策略，以便在耗时较长的操作期间保持服务器与客户端之间的持续通信。接下来，我们将开发一个异步任务管理框架，允许您的 AI 代理启动长时间运行的任务，同时不会阻塞其他操作。最后，我们将展示如何结合 Amazon Bedrock AgentCore 和 Strands Agents 将这些策略整合起来，构建可投入生产的 AI 代理，使其能够可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理往往面临着状态管理与通信保持的挑战。本文将介绍如何利用 Amazon Bedrock AgentCore 和 Strands Agents 集成，通过上下文消息策略与异步任务管理框架来解决这一问题。您将了解到如何构建可投入生产的 AI 代理，使其在执行复杂操作时保持客户端的持续通信，且不阻塞其他任务流程。

---
## 摘要

本文介绍了一种在 Amazon Bedrock AgentCore 上集成 Strands Agents 以构建长期运行 MCP 服务器的综合方法。主要内容包含以下三个方面：

1.  **上下文消息策略**：引入了一种策略，用于在服务器与客户端执行扩展操作期间维持持续的通信，确保状态同步。
2.  **异步任务管理框架**：开发了一个框架，允许 AI 代理启动长时间运行的进程，同时不阻塞其他操作，提高了系统的并发处理能力。
3.  **生产级实现**：展示了如何结合 Amazon Bedrock AgentCore 和 Strands Agents，将上述策略整合，从而构建出能够可靠处理复杂、耗时任务的生产级 AI 代理。

---
## 评论

### 中心观点
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构范式，旨在通过上下文消息策略与异步任务管理框架，解决大型语言模型（LLM）在处理长周期任务时的状态保持与交互中断问题，从而构建具备持续执行能力的 MCP（Model Context Protocol）服务器。

### 支撑理由与边界条件分析

**1. 解决了 LLM 的“短期记忆”与“长程执行”矛盾**
*   **事实陈述**：目前的 LLM 受限于 Token 上下文窗口和请求-响应的无状态特性，难以直接处理需要数分钟甚至数小时的复杂业务流（如代码部署、数据分析）。
*   **作者观点**：文章引入的“Strands Agents integration”与“Context message strategy”旨在将计算逻辑从同步阻塞转为异步非阻塞，通过中间层维持对话状态。
*   **你的推断**：这实际上是在应用层实现了一个“状态机”，将 LLM 从“执行者”转变为“调度者”，这是构建 Agent 生产环境的必经之路。

**2. 异步任务管理框架的必要性**
*   **事实陈述**：摘要中明确提到开发了一个“asynchronous task management framework”（异步任务管理框架）。
*   **你的推断**：这通常涉及消息队列（如 SQS）或 WebSocket 长连接。对于 Bedrock 这种 Serverless 服务，必须通过外部存储来保存任务进度，否则 API 超时会导致任务丢失。

**3. 深度绑定 AWS 生态的“围墙花园”策略**
*   **事实陈述**：文章完全基于 Amazon Bedrock AgentCore 和 Strands Agents。
*   **你的推断**：这是典型的云厂商技术布道。虽然技术上可行，但它高度依赖 AWS 的基础设施，可能导致厂商锁定。

**反例/边界条件：**
*   **反例 1（成本与延迟）**：对于简单的、毫秒级的查询任务，引入 Strands Agents 和异步框架会增加不必要的网络跳转和延迟，且 Bedrock 的调用成本可能高于直接调用开源模型（如 Llama 3 自建）。
*   **边界条件（实时性要求）**：如果业务需要毫秒级的状态反馈（例如高频交易辅助或即时游戏控制），基于 Bedrock API 的轮询或异步回调机制可能无法满足极低延迟要求。
*   **边界条件（数据隐私）**：如果任务涉及高度敏感数据，企业可能无法接受将上下文数据发送至 Bedrock 托管服务，此时本地部署的 MCP 服务器（不使用 AgentCore）是更优解。

### 多维度深入评价

#### 1. 内容深度：架构层面的务实解法
从摘要看，文章没有停留在简单的 API 调用演示，而是触及了 Agent 开发的核心痛点：**状态持久化**。
*   **论证严谨性**：通过“Context message strategy”来维持通信，表明作者理解 MCP 协议的局限性。MCP 本身是一个同步协议，要在其上实现长任务，必须引入“令牌”或“回调ID”机制。
*   **不足**：摘要未提及错误处理和重试机制。长任务最容易因网络波动或模型幻觉导致失败，缺乏这部分讨论，方案的完整性存疑。

#### 2. 实用价值：高，但受众特定
*   对于**重度 AWS 用户**，这篇文章提供了官方的最佳实践，具有极高的参考价值，能节省大量架构设计时间。
*   对于**非 AWS 用户**，价值较低。Strands Agents 是 AWS 特有的概念（可能涉及内部工作流编排），移植到 Azure或 GCP 需要重新设计。

#### 3. 创新性：组合创新而非理论突破
*   **新观点**：将 MCP 协议与 Bedrock AgentCore 深度结合，提出了在 Serverless 环境下运行长任务 Server 的模式。
*   **评价**：这属于工程层面的“组合创新”。它没有提出新的算法（如 CoT 的改进），而是解决了基础设施与模型交互的工程难题。

#### 4. 可读性：技术文档的标准范式
*   摘要逻辑清晰：先提出问题，后给出方案，最后列出技术组件。符合技术博客的黄金标准。

#### 5. 行业影响：推动 MCP 协议的企业级落地
*   MCP（Model Context Protocol）是 Anthropic 推出的开放标准。AWS Bedrock 对此的支持表明主流云厂商正在接受这一标准，有助于打破不同 AI 应用之间的数据孤岛。这篇文章实际上是在展示如何用 AWS 的基础设施“工业化”这一标准。

#### 6. 争议点：厂商锁定的隐忧
*   使用 Amazon Bedrock AgentCore 意味着你的业务逻辑与 AWS 的服务深度耦合。未来如果需要切换模型提供商（例如切换到 DeepSeek 或本地 Llama），迁移成本将不仅在于 Prompt，更在于这个异步任务管理框架的重构。

### 实际应用建议
1.  **评估成本**：在实施前，计算 Bedrock 长连接或高频轮询的费用。对于高并发场景，Bedrock 的按 Token 计费模式配合异步框架可能会产生意外的高额账单。
2.  **混合架构**：建议将“控制流”放在 Bedrock AgentCore 上，而将“数据流”和实际执行逻辑放在自己的 ECS/EKS 中，仅通过 MCP 协议交互，以降低耦合度。
3.  **监控告警**：务必为异步任务添加 CloudWatch 告警。长任务容易变成“僵尸任务”，若无超时强制熔断机制，会占用

---
## 技术分析

基于提供的标题和摘要片段，这篇文章主要探讨了在 Amazon Bedrock AgentCore 环境下构建能够处理长时间运行任务的服务器，并重点结合了 Strands Agents 的集成技术。以下是针对该文章核心观点和技术要点的深入分析：

---

# 深入分析：在 Amazon Bedrock AgentCore 上构建长时运行 MCP 服务器

## 1. 核心观点深度解读

### 主要观点
文章的核心观点是：**传统的同步请求-响应模式无法满足现代 AI Agent 处理复杂、长时运行任务的需求。通过引入“上下文消息策略”和“异步任务管理框架”，并利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成，开发者可以构建出既具备高度交互性又能稳定处理长流程的智能体系统。**

### 核心思想
作者试图传达的核心思想是**“交互连续性”与“计算异步化”的解耦**。在 AI Agent 与工具（MCP Server）交互的过程中，不能因为工具执行耗时（如数据查询、代码生成）而阻塞整个会话。系统应当具备一种机制，使得 Agent 在等待 Server 结果时，仍能保持与用户的上下文连接，甚至进行中间状态的反馈。

### 创新性与深度
该观点的创新性在于它不仅仅是在调用 API，而是在构建一个**“有状态的工作流”**。它将 MCP（Model Context Protocol）从一个简单的数据获取协议，提升为一个能够管理任务生命周期、处理流式状态和复杂编排的控制系统。深度在于它解决了生产环境中 AI 落地的最大痛点之一——**长任务处理的超时与用户体验割裂**。

### 重要性
随着 AI Agent 从简单的聊天机器人向能够执行复杂任务的“智能体”演进，处理长时任务（如 RAG 系统中的大数据索引、复杂的多步推理、自动化运维操作）成为刚需。如果无法解决长时运行问题，Agent 的应用场景将被限制在简单的问答领域。

## 2. 关键技术要点

### 关键技术概念
1.  **MCP (Model Context Protocol)**：一种开放协议，用于 AI 应用与数据源/工具之间的连接。文章重点在于 MCP Server 的实现。
2.  **Amazon Bedrock AgentCore**：AWS 提供的构建 Agent 的底层服务/框架，负责编排、内存管理和工具调用。
3.  **Strands Agents**：这是一个关键的技术组件（推测为 AWS 或合作伙伴提供的特定 Agent 框架/模式），专门用于处理“流”或“线索”式的长时交互。
4.  **异步任务管理**：非阻塞的执行模式。

### 技术原理与实现
*   **上下文消息策略**：
    *   **原理**：在长任务执行期间，Server 不保持连接阻塞，而是发送中间状态或“心跳”消息给 Client/Agent。
    *   **实现**：利用 WebSocket 或长轮询机制，或者通过返回一个 `taskId` 并提供独立的查询接口。AgentCore 需要能够解析这些中间消息，并决定是继续等待还是向用户汇报。
*   **异步任务管理框架**：
    *   **原理**：将工具调用分为“启动”、“检查状态”、“获取结果”三个阶段。
    *   **实现**：MCP Server 接收到请求后，立即返回 `202 Accepted` 和任务 ID，后台启动处理流程（如 Lambda 函数或 ECS 任务）。AgentCore 通过 Strands Agents 的逻辑定期轮询或等待回调。

### 技术难点与解决方案
*   **难点**：**状态管理与超时控制**。LLM 的上下文窗口有限，且连接可能超时。
*   **解决方案**：文章提出的框架通过将任务状态外部化（存储在数据库或状态机中），仅将关键状态变更同步给 LLM，从而保持上下文精简且实时。
*   **难点**：**错误恢复**。长任务容易失败。
*   **解决方案**：Strands Agents 集成可能包含了重试机制和断点续传逻辑，确保任务链条的健壮性。

### 技术创新点
将 **Strands Agents**（可能代表一种链式或流式处理架构）与 **Bedrock AgentCore** 结合，实现了从“单轮对话”到“多轮流式协作”的范式转移。

## 3. 实际应用价值

### 指导意义
这篇文章为架构师和 AI 工程师提供了一套**构建生产级 Agent 的标准模式**。它告诉我们，不要试图在一个 API 调用中完成所有工作，必须设计异步的后端服务。

### 应用场景
1.  **企业级 RAG 系统**：向量化数百万份文档需要时间，通过该框架可以在处理过程中向用户报告进度百分比。
2.  **代码生成与部署**：Agent 生成代码后，需要经过漫长的测试、构建、部署流程，该框架可用于实时回传 CI/CD 日志。
3.  **数据分析 Agent**：执行复杂的 SQL 查询或生成大数据报表，通常需要数分钟，异步框架可避免前端超时。
4.  **自动化运维**：执行一系列的系统诊断步骤，逐步返回诊断结果。

### 注意问题
*   **成本控制**：频繁的上下文消息轮询会增加 Token 消耗和 API 调用成本。
*   **状态一致性**：确保异步任务的状态与 Agent 记忆中的状态不发生冲突。

### 实施建议
在实施时，应优先将所有耗时超过 10 秒的工具调用改造为异步模式，并设计标准化的“任务状态对象”供 LLM 理解。

## 4. 行业影响分析

### 对行业的启示
该文章标志着 **Agent 基础设施正在走向“云原生化”和“工程化”**。过去大家关注 Prompt Engineering，现在开始关注如何用 Serverless、异步消息队列等后端技术来支撑 Agent 的运行。

### 可能带来的变革
*   **从 Chatbot 到 Copilot 的转变**：由于解决了长任务交互问题，AI 将能真正介入复杂的工作流，而不仅仅是回答问题。
*   **MCP 协议的普及**：这种长时运行模式可能会成为 MCP 协议进化的一个重要方向，推动更多工具提供商支持异步 MCP。

### 发展趋势
未来的 Agent 开发将越来越像传统的后端开发，需要引入消息队列、状态机和微服务架构。

## 5. 延伸思考

*   **人机协作模式**：如果 Agent 在执行长任务，用户是否可以“打断”或“修改”指令？这需要更复杂的流控制逻辑。
*   **多 Agent 编排**：如果长任务需要多个 Agent 协作（例如一个写代码，一个审核），这种异步框架如何支持 Agent 间的握手？
*   **可观测性**：在异步长任务中，追踪错误和性能瓶颈变得更加困难，需要专门的 AI 运维工具。

## 6. 实践建议

### 如何应用到项目
1.  **评估现有工具**：检查你目前的 Agent 调用的工具中，哪些执行时间不稳定或较长。
2.  **引入状态机**：使用 AWS Step Functions 或类似服务来管理这些长任务的状态。
3.  **改造 MCP Server**：修改你的 MCP Server 代码，使其支持 `jobs` 或 `tasks` 接口，返回 `resource_uri` 而非直接结果。

### 行动建议
*   **阅读 AWS Bedrock 文档**：深入了解 AgentCore 的配置项。
*   **模拟测试**：构建一个模拟的长时任务（如 sleep 60s），测试 Agent 在等待期间的行为，确保它不会产生幻觉或重复调用。

### 补充知识
*   异步编程模式
*   WebSocket 协议
*   AWS Lambda/Step Functions

## 7. 案例分析

### 成功案例：企业财报生成 Agent
*   **场景**：用户要求 Agent 分析过去一年的销售数据并生成图表。
*   **传统做法**：查询数据库 -> 超时 -> 失败。
*   **本文方案**：Agent 调用 MCP Server 启动分析任务（异步）。Server 返回 `TaskID`。Agent 告诉用户“正在分析中，请稍候...”。Server 后台处理。Agent 每隔 10 秒轮询一次，最终拿到结果并展示。
*   **结果**：用户体验流畅，任务成功完成。

### 失败反思
*   **问题**：如果异步任务最终失败，但 Agent 没有正确捕获错误码，可能会告诉用户“任务完成”，但实际上什么也没做。
*   **教训**：必须设计极其详尽的错误处理分支，确保 LLM 能够理解异步任务的“失败”状态。

## 8. 哲学与逻辑：论证地图

### 中心命题
**为了构建能够处理复杂、长时运行任务的生产级 AI Agent，开发者必须在 Amazon Bedrock AgentCore 上采用基于 MCP 的异步任务架构与 Strands Agents 集成方案，而非依赖传统的同步阻塞式调用。**

### 支撑理由与依据
1.  **理由 1：用户体验与交互连续性**
    *   **依据**：同步调用会导致 HTTP 超时或前端无响应，破坏用户体验。事实是，复杂任务（如数据处理）耗时往往超过 LLM 上下文窗口或客户端超时限制。
2.  **理由 2：系统的可扩展性与稳定性**
    *   **依据**：异步模式允许后端资源在任务处理期间被释放或复用，防止因长任务占满连接池而导致系统崩溃。
3.  **理由 3：Strands Agents 的编排能力**
    *   **依据**：Strands Agents 提供了处理“流”和“状态”的原生支持，使得管理非线性的任务进度成为可能，这是基础 Bedrock 配置难以原生实现的。

### 反例与边界条件
1.  **反例 1（简单查询场景）**：对于毫秒级的数据查询（如查天气、查库存），引入异步框架会增加不必要的延迟和架构复杂度。
2.  **边界条件（强一致性要求）**：如果业务逻辑要求必须在拿到结果后才能进行下一步（且用户不能接受中间状态），异步带来的最终一致性问题可能需要复杂的锁机制来解决。

### 事实与价值判断
*   **事实**：MCP 协议支持灵活的消息传递；AWS Bedrock 支持自定义编排。
*   **价值判断**：“长时运行能力”是 Agent 走向“通用人工智能（AGI）辅助”的关键特征，值得为此增加架构复杂度。

### 立场与验证
*   **立场**：支持在构建企业级 Agent 时采用此异步架构。
*   **可证伪验证**：
    *   **指标**：对比同步架构与异步架构在处理 5 分钟长任务时的“任务完成率”和“用户等待感知时间”。
    *   **实验**：构建一个高并发场景，观察同步架构是否导致连接溢出，而异步架构能否保持服务可用。

---
## 最佳实践

## 最佳实践指南

### 实践 1：合理设计 Strands 的生命周期与并发管理

**说明**: 长时间运行的 MCP 服务器通常需要处理多个并发的 Agent 任务。在 Bedrock AgentCore 集成中，必须合理配置 Strands（代表 Agent 的执行线程或会话）的生命周期。避免无限制地创建 Strands 导致资源耗尽，同时要确保在长时间任务中 Strands 能够保持活性而不被超时机制意外终止。

**实施步骤**:
1. 在 AgentCore 配置中，根据后端资源（如数据库连接数、API 限流）设定最大并发 Strands 数量。
2. 实施租约或心跳机制，确保长运行任务在处理耗时操作（如等待外部 API 响应）时，Strands 不会因为空闲而被回收。
3. 为不同类型的任务（如快速查询 vs 长时间数据处理）配置不同的超时策略。

**注意事项**: 监控 Strands 的创建和销毁速率，防止内存泄漏或连接泄漏。

---

### 实践 2：实施健壮的状态持久化机制

**说明**: 长运行服务器面临重启或故障的风险。为了确保 Strands 中的 Agent 任务不丢失，必须将 Agent 的状态（上下文、中间变量、进度）持久化到外部存储（如 DynamoDB 或 S3）中，而不是仅保留在内存中。

**实施步骤**:
1. 定义清晰的状态模型，将 MCP 协议中的状态数据序列化。
2. 在 Strands 的关键执行节点（如完成一个工具调用后）设置检查点，自动保存状态。
3. 实现启动时的恢复逻辑，服务器重启后能根据持久化的状态重新挂起 Strands。

**注意事项**: 频繁的持久化可能会增加延迟，需要在数据安全性和性能之间取得平衡，采用异步写入策略。

---

### 实践 3：优化 MCP 工具的幂等性与重试策略

**说明**: 网络波动或 Bedrock 的限流可能导致工具调用失败。在 Strands Agents 集成中，必须确保 MCP 服务器暴露的工具是幂等的，并配合 AgentCore 实现智能重试，以保证长运行流程的稳定性。

**实施步骤**:
1. 确保所有 MCP 工具接口实现幂等性，即多次调用同样的参数产生的结果一致且不会产生副作用。
2. 在服务器端配置指数退避算法处理可重试的错误（如 5xx 错误或限流错误）。
3. 为非幂等操作（如转账、发送邮件）实现事务性检查，防止重试导致重复执行。

**注意事项**: 区分临时性故障和永久性故障，对于参数错误等永久性故障应立即终止重试并向 Agent 报告。

---

### 实践 4：建立细粒度的可观测性与日志追踪

**说明**: 调试长运行的 Agent 链路非常困难。必须将 Strands 的执行日志与 Bedrock Agent 的追踪 ID 关联，以便在 CloudWatch 或其他日志系统中追踪完整的请求链路。

**实施步骤**:
1. 在 MCP 服务器中集成 OpenTelemetry 或 CloudWatch Logs，注入 `Trace-ID`。
2. 记录详细的工具调用日志，包括输入参数、输出结果和执行耗时。
3. 为 Strands 的状态变更设置特定的事件日志，便于回溯 Agent 的决策过程。

**注意事项**: 避免记录敏感信息（如 PII 数据），在日志输出前对敏感字段进行脱敏处理。

---

### 实践 5：严格的安全控制与最小权限原则

**说明**: MCP 服务器作为 Agent 与外部世界交互的桥梁，极易成为攻击目标。必须严格验证来源请求，并确保 Strands 在执行工具时仅拥有完成任务所需的最小权限。

**实施步骤**:
1. 在 MCP 服务器与 Bedrock AgentCore 之间启用 IAM 身份验证和授权。
2. 为不同的 Strands 或 Agent 角色配置精细的 IAM 策略，限制其可调用的 MCP 工具范围。
3. 对所有输入参数进行严格校验，防止注入攻击。

**注意事项**: 定期轮换凭证，并使用 AWS Secrets Manager 管理数据库或 API 密钥，不要硬编码在代码中。

---

### 实践 6：处理流式响应与部分结果

**说明**: 长运行任务往往耗时较长，用户可能需要即时的反馈。MCP 服务器应支持流式返回或部分结果，以便 Bedrock Agent 能够向用户展示进度，而不是一直等待最终结果。

**实施步骤**:
1. 评估 MCP 协议支持，设计能够返回中间状态的工具接口。
2. 在 Strands 执行过程中，通过回调或 WebSocket 推送进度更新。
3. 配置 AgentCore 以正确处理和展示这些中间状态信息。

**注意事项**: 确保客户端能够正确处理流式数据的结束标记，避免连接挂起。

---
## 学习要点

- 利用 Amazon Bedrock AgentCore 构建的 MCP 服务器支持长时间运行的任务，能够处理需要多步骤或持续状态的复杂工作流。
- 通过集成 Strands Agents，开发者可以构建具备记忆能力和状态管理的智能体，从而实现更连贯的上下文交互。
- 该架构允许将 Bedrock 的托管基础设施与 MCP 协议相结合，显著降低了维护可扩展 AI 系统的复杂性。
- 服务器能够无缝处理异步任务和长时间运行的操作，无需担心传统短连接带来的超时限制。
- 借助 Bedrock AgentCore 的原生集成，开发者可以更专注于核心业务逻辑而非底层基础设施的搭建。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长运行任务](/tags/%E9%95%BF%E8%BF%90%E8%A1%8C%E4%BB%BB%E5%8A%A1/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文策略](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AD%96%E7%95%A5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*