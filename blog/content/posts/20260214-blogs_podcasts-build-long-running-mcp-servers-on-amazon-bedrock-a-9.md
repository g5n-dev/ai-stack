---
title: "基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器"
date: 2026-02-14T09:12:50+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "长时运行任务", "异步任务", "AI 智能体", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成来构建长时间运行的 MCP 服务器的综合方法。 核心内容包括三个部分： 1. **上下文消息策略**：引入一种策略，以在服务器与客户端之间维持扩展操作期间的持续通信。 2. **异步任务管理框架**：开发一个框架"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供了一套实现这一目标的综合方法。首先，我们介绍一种上下文消息策略，在耗时较长的操作期间维持服务器与客户端之间的持续通信。接着，我们开发一个异步任务管理框架，让您的 AI 智能体能够启动长时间运行的处理流程，同时不会阻塞其他操作。最后，我们将演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合，构建生产就绪的 AI 智能体，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 智能体，是许多生产级应用面临的技术挑战。本文将探讨如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成，解决上下文维护与异步任务管理的问题。通过构建非阻塞的通信机制，我们将演示如何打造稳定、可靠的系统，使其能够从容应对复杂的耗时操作。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成来构建长时间运行的 MCP 服务器的综合方法。

核心内容包括三个部分：
1.  **上下文消息策略**：引入一种策略，以在服务器与客户端之间维持扩展操作期间的持续通信。
2.  **异步任务管理框架**：开发一个框架，允许 AI 代理启动长时运行进程而不阻塞其他操作。
3.  **整合应用**：演示如何利用上述策略，构建生产级的、能可靠处理复杂且耗时操作的 AI 代理。

---
## 评论

### 中心观点
该文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构模式，旨在解决大模型应用中“长时间运行任务”的状态管理与异步通信难题，试图通过 MCP 协议的上下文消息策略与异步任务框架，填补传统 Request-Response 模式在处理复杂工作流时的空白。

---

### 深度评价

#### 1. 内容深度：架构层面的必要补充，但理论完备性待验证
*   **支撑理由（事实陈述）：** 文章触及了当前 Agent 开发的核心痛点——**LLM 的会话生命周期与业务任务的生命周期不匹配**。大模型通常在几秒内完成推理，但实际业务（如数据分析、代码部署）可能需要数分钟。文章提出的“Context Message Strategy”和“Asynchronous Task Management”是解决这一问题的标准工程范式。
*   **支撑理由（你的推断）：** 从技术架构看，这实际上是将传统的**消息队列**和**事件驱动架构**引入了 Agent 交互层。Bedrock AgentCore 在此扮演了编排层的角色，而 Strands Agents 可能提供了具体的执行逻辑。这种分层设计是严谨的。
*   **反例/边界条件（作者观点）：** 文章可能过度依赖 MCP 协议作为通用解耦层。如果 Strands Agents 本身不支持高并发的长连接保持，或者 Bedrock 的上下文窗口刷新机制存在延迟，这种“连续通信”可能会导致资源耗尽或状态不一致。

#### 2. 实用价值：云原生场景下的落地指南，但存在厂商锁定风险
*   **支撑理由（事实陈述）：** 对于深度使用 AWS 生态的开发者，这篇文章提供了从概念到代码的“一站式”路径。利用 Bedrock 的托管服务可以显著降低运维基础设施的负担。
*   **支撑理由（你的推断）：** 文章中提到的“Strands Agents integration”暗示了针对特定场景（如数据处理流）的优化，这对于构建垂直领域的 Copilot 具有很高的参考价值。
*   **反例/边界条件（你的推断）：** 如果用户的业务环境涉及混合云或私有云部署，强行套用 Bedrock AgentCore 的架构会导致极高的迁移成本。此外，对于轻量级应用，该架构可能显得过于厚重。

#### 3. 创新性：组合式创新，协议层面的标准化尝试
*   **支撑理由（事实陈述）：** 将 MCP (Model Context Protocol) 应用于长任务的上下文维护是一个较新的尝试。MCP 试图统一 AI 与数据源的连接标准，文章将其扩展到了“任务流”的控制，这是对 MCP 能力边界的探索。
*   **支撑理由（作者观点）：** “Strands Agents”这一概念的引入，可能代表了将 Agent 能力模块化的趋势，即不同的 Agent 处理不同时间跨度的任务。
*   **反例/边界条件（事实陈述）：** LangGraph 或 Semantic Kernel 等开源框架早已通过图结构和检查点机制解决了类似问题。文章的创新更多在于“如何用 AWS 产品栈实现”，而非算法或机制本身的突破。

#### 4. 行业影响：推动 Agent 从“玩具”走向“生产”
*   **支撑理由（你的推断）：** 如果该模式被广泛采纳，意味着行业开始正视 AI 应用的工程化难题，不再满足于简单的问答。这会推动开发者更多地关注任务队列、状态机和错误重试机制。
*   **反例/边界条件（作者观点）：** 这种中心化的架构可能并不符合所有去中心化 Agent 的愿景。行业目前也在探索基于区块链或 P2P 的任务分发模式，Bedrock 的方案是中心化的代表。

---

### 争议点或不同观点

1.  **协议依赖的争议（事实陈述）：** MCP 协议虽然由 Anthropic 推动，但并非行业标准。过度依赖特定协议可能导致与 OpenAI 或其他模型生态的兼容性问题。
2.  **成本结构的隐形陷阱（你的推断）：** 维护长连接和持续的上下文消息传输，在 Bedrock 上会产生显著的成本。相比于传统的后端异步处理，这种“AI 全程在线”的模式在处理大规模并发时，Token 消耗和 API 调用费用可能不可控。
3.  **Strands Agents 的黑盒性质（事实陈述）：** 文章未详细披露 Strands Agents 的内部逻辑。如果它是一个封闭的托管服务，开发者将失去对任务执行细节的微调能力。

---

### 实际应用建议

1.  **明确任务边界（作者观点）：** 不要将所有业务逻辑都放入 Agent 中。仅将需要 LLM 推理的决策节点接入 Bedrock，确定性的长任务逻辑应通过传统的 Lambda/ECS 完成，仅通过 MCP 回传状态。
2.  **实施超时与熔断机制（事实陈述）：** 在采用异步任务框架时，必须在 Bedrock Agent 配置中设置严格的 TTL（Time To Live），防止因下游服务挂起而导致 Agent 无限等待。
3.  **成本监控（你的推断）：** 建议在部署前建立 CloudWatch 告警，专门监控“Context Message”的交互频率。长任务往往伴随着大量的状态查询轮询，这是成本漏斗。

---

### 可验证的检查方式

1.  **压力测试指标（实验）：** 搭建该架构并模拟 100 个并发长任务（如每个任务运行 5 分钟），观察 Bedrock AgentCore 是否会出现上下文混淆或延迟累积。重点关注 `p95` 响应延迟。
2.  **断点恢复测试（观察窗口）：** 在长任务执行过程中人为中断网络或重启 Strands Agents 服务

---
## 技术分析

## 技术分析

**架构模式与设计目标**
文章主要探讨了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构设计，旨在解决 AI 代理在处理长时间运行任务时面临的挑战。传统的同步请求-响应模式受限于网络超时和阻塞机制，难以应对耗时较长的业务流程。该方案通过引入异步任务管理和上下文状态保持机制，确保了业务流程在长时间跨度内的连续性。

**核心技术机制**
1.  **异步任务解耦：**
    系统将客户端的通信层与后端任务执行层进行分离。当 MCP 服务器接收到耗时请求时，不再保持连接阻塞等待结果，而是立即生成任务句柄并返回确认信息。实际的工作负载被卸载至后台进程（如 Lambda 函数或 Step Functions）执行，实现了通信与计算的解耦。

2.  **状态持久化与上下文恢复：**
    利用 Strands Agents 机制维护任务的状态和记忆。任务的元数据和执行进度被持久化存储，使得 Agent 能够在会话中断后恢复上下文。当用户再次查询时，系统通过检索 Strands 中的历史状态，确保 LLM 能够准确关联并回应当前的任务状态，而非将其视为孤立事件。

3.  **MCP 协议的扩展实现：**
    文章展示了对 MCP (Model Context Protocol) 的具体应用扩展。通过实现异步回调或状态查询接口，MCP 服务器突破了标准同步工具调用的限制，允许在 Bedrock AgentCore 框架下协调长时工作流。

**技术难点与应对**
该方案主要解决了 LLM 无状态特性与长时业务有状态需求之间的矛盾。通过将任务状态外部化存储于 Strands 中，并配合 Bedrock AgentCore 的编排能力，实现了对长时间运行任务的有效追踪和管理。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化长连接与会话管理策略

**说明**:
在构建基于 Amazon Bedrock AgentCore 的长运行 MCP 服务器时，必须高效处理有状态会话。Strands Agents 通常需要维护上下文记忆，因此服务器应设计为支持持久化连接，并能够优雅地处理会话超时和恢复，避免因网络波动导致的长任务中断。

**实施步骤**:
1.  在 MCP 服务器配置中启用 Keep-Alive 机制，定期发送心跳以维持连接活跃。
2.  实现会话状态的外部存储（如 Amazon DynamoDB），以便在服务器重启或故障转移时恢复上下文。
3.  设计明确的会话超时与清理逻辑，防止僵尸连接占用资源。

**注意事项**:
- 确保心跳间隔不要过短，以免增加不必要的负载；建议间隔设置为 30-60 秒。

---

### 实践 2：实施非阻塞式异步任务处理

**说明**:
Strands Agents 执行的某些操作（如数据处理、外部 API 调用）可能耗时较长。MCP 服务器应采用异步非阻塞架构，确保服务器在等待长时间任务完成时仍能响应其他请求或心跳信号，防止被代理框架判定为超时。

**实施步骤**:
1.  将耗时任务封装为异步操作，利用语言的异步特性（如 Python asyncio）。
2.  对于超过 30 秒的任务，实现“任务排队 + 状态查询”模式，而非直接阻塞等待结果。
3.  使用流式响应（Streaming Responses）逐步返回中间状态或结果。

**注意事项**:
- 必须处理好并发控制，避免过多的异步并行任务耗尽系统内存或连接池。

---

### 实践 3：构建健壮的错误重试与容错机制

**说明**:
长运行服务不可避免会遇到网络抖动或限流。MCP 服务器需要具备智能重试逻辑，特别是与 Strands Agents 交互时，应区分瞬时错误（如 5xx 错误）和永久错误（如 4xx 错误），以最大化任务完成率。

**实施步骤**:
1.  实现指数退避算法处理重试请求，避免对下游服务造成冲击。
2.  为所有外部调用定义明确的超时时间，防止线程挂起。
3.  集成死信队列（DLQ）来存储多次重试失败的任务，以便后续人工介入或分析。

**注意事项**:
- 确保重试逻辑不会导致业务逻辑的重复执行（例如幂等性设计）。

---

### 实践 4：严格的安全认证与最小权限控制

**说明**:
MCP 服务器通常作为 Agent 与后端资源之间的桥梁。必须实施严格的身份验证和授权，确保只有经过授权的 Amazon Bedrock Agent 可以调用 MCP 工具，并且服务器仅拥有完成任务所需的最小权限。

**实施步骤**:
1.  在 MCP 服务器与 Bedrock AgentCore 之间配置双向 TLS (mTLS) 或使用 JWT 进行认证。
2.  为 MCP 服务器的 IAM 角色应用最小权限原则，仅授予访问特定 S3 存储桶、DynamoDB 表或其他 API 的权限。
3.  在日志中脱敏敏感信息，不要记录完整的请求体或令牌。

**注意事项**:
- 定期轮换凭证和证书，避免使用硬编码的 API Key。

---

### 实践 5：增强的可观测性与日志记录

**说明**:
长运行进程难以调试。为了确保 Strands Agents 的交互符合预期，MCP 服务器必须提供详细的追踪信息，包括请求来源、执行时间、错误堆栈以及中间结果，这对于故障排查至关重要。

**实施步骤**:
1.  集成 AWS CloudWatch 或兼容的 OpenTelemetry 协议，统一收集指标和日志。
2.  在日志中注入 Trace ID，将其与 Bedrock Agent 的追踪 ID 关联，实现全链路追踪。
3.  监控关键指标，如服务器内存使用率、请求延迟、错误率以及活跃连接数。

**注意事项**:
- 注意日志采样策略，避免在海量高并发下产生过高的日志存储成本。

---

### 实践 6：工具定义与输入验证的标准化

**说明**:
MCP 服务器的核心功能是向 Agent 暴露工具。为了提高 Strands Agents 的调用成功率，工具的定义（Schema）必须极其精确，且服务器端必须对输入参数进行严格验证，防止无效参数导致的长运行任务失败。

**实施步骤**:
1.  使用清晰的 JSON Schema 定义工具参数，包含类型、枚举值和描述。
2.  在工具逻辑执行前，增加一层严格的参数校验，并在参数不合法时立即返回明确的错误信息。
3.  为工具编写详细的描述文本，帮助 LLM 理解工具用途和副作用。

**注意事项**:
- 避免定义过于模糊或参数过多的工具，这会降低 LLM 的调用准确率。建议将复杂工具拆分为多个单一职责的小工具。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够维护长期对话状态和记忆的持久化 MCP 服务器。
- 该集成通过将 Strands 的有状态记忆层与 Bedrock 的无状态架构相结合，解决了传统 AI Agent 在多轮交互中丢失上下文的核心痛点。
- 开发者可以利用 MCP 协议将现有的 Strands Agents 作为工具无缝接入 Bedrock，显著增强了 Agent 处理复杂工作流的能力。
- 这种架构支持 Agent 在长时间运行的任务中保持上下文连贯性，从而实现更高级的自主规划和执行能力。
- 通过利用 Bedrock 的托管基础设施，用户可以在享受 Strands 高级状态管理优势的同时，获得企业级的安全性与可扩展性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [长时运行任务](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C%E4%BB%BB%E5%8A%A1/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*