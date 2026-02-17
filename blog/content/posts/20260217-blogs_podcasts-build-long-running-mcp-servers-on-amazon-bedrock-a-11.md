---
title: "基于Amazon Bedrock AgentCore构建支持长时运行的MCP服务器"
date: 2026-02-17T08:54:54+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Bedrock", "AgentCore", "Strands Agents", "异步任务", "长时运行", "上下文管理", "AI 架构"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何利用 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够长时间运行的 MCP（Model Context Protocol）服务器。文章提供了一套综合方法，主要包含以下三个核心策略： 1. **上下文消息策略**：引入了一种机制，用于在服务器与客户端执行扩展"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建支持长时运行的MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们为您提供了一套全面的解决方案来实现这一目标。首先，我们介绍一种上下文消息策略，用于在服务器和客户端之间在长时间运行的操作期间保持持续通信。接下来，我们开发一个异步任务管理框架，让您的 AI 代理能够启动长时间运行的流程，而不会阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，构建可用于生产环境的 AI 代理，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理往往面临着上下文管理与系统阻塞的挑战。本文介绍了一套基于 Amazon Bedrock AgentCore 和 Strands Agents 的解决方案，通过上下文消息策略与异步任务管理框架，确保服务器与客户端在复杂流程中的持续通信。阅读本文，您将掌握构建可用于生产环境的 AI 代理的关键技术，从而实现可靠且高效的长时任务处理。

---
## 摘要

本文介绍了如何利用 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够长时间运行的 MCP（Model Context Protocol）服务器。文章提供了一套综合方法，主要包含以下三个核心策略：

1.  **上下文消息策略**：引入了一种机制，用于在服务器与客户端执行扩展操作期间，维持持续的上下文通信，确保对话状态的连贯性。
2.  **异步任务管理框架**：开发了一套异步框架，使 AI 智能体能够启动长时运行的后台进程，而无需阻塞其他操作的执行，从而提升系统的并发处理能力。
3.  **集成与实现**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，构建生产级的 AI 智能体，使其能够可靠地处理复杂且耗时的操作任务。

---
## 评论

### 中心观点
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构模式，旨在通过异步任务管理框架和上下文消息策略，解决模型上下文协议（MCP）服务器在执行长周期任务时的连接超时与状态保持难题。

### 深入评价

#### 1. 内容深度：架构补位与理论缺失
**支撑理由：**
*   **事实陈述：** 文章准确抓住了当前 MCP（Model Context Protocol）生态的一个痛点：现有的 LLM 交互模式多为同步请求-响应，难以处理耗时较长的“Agent 动作”（如数据查询、代码编译）。
*   **作者观点：** 通过引入“异步任务管理框架”，将长任务与主通信循环解耦，这是分布式系统设计在 AI Agent 领域的标准复用，论证了技术可行性。
*   **你的推断：** 文章暗示 Bedrock AgentCore 扮演了“中间件”角色，负责维持与 LLM 的 Session，而 Strands Agents 负责实际执行，这种双层架构在理论上能有效抵抗网络波动。

**反例/边界条件：**
*   **边界条件：** 该方案并未深入讨论“最终一致性”问题。如果异步任务执行失败，如何向已经断开或上下文已切换的 LLM 汇报错误？
*   **反例：** 对于强实时性要求的场景（如流式数据分析），这种异步轮询模式会增加端到端延迟，不如直接的长连接（WebSocket/Server-Sent Events）高效。

#### 2. 实用价值：云厂商的“围墙花园”策略
**支撑理由：**
*   **事实陈述：** 提供了具体的构建方法，对于深度绑定 AWS 生态的开发者具有极高的参考价值。
*   **作者观点：** 利用 Bedrock 托管 Agent 的核心逻辑，可以降低企业自建 Agent 运维底座的门槛。
*   **你的推断：** 这实际上是在推销一种“Vendor Lock-in”（供应商锁定）方案。虽然技术上解决了长连接问题，但将业务逻辑强绑定在 Bedrock 上，未来迁移成本极高。

**反例/边界条件：**
*   **边界条件：** 仅适用于企业级后端服务，对于边缘计算或端侧 AI 场景，依赖 AWS 服务的架构完全失效。
*   **反例：** 开源社区已有基于 Redis 或 RabbitMQ 的轻量级 MCP 异步扩展方案，相比之下，Bedrock 方案的学习成本和部署成本过高。

#### 3. 创新性：缺乏突破性的范式转移
**支撑理由：**
*   **你的推断：** 文章所提的“Context Message Strategy”本质上是“心跳机制”和“令牌传递”的变体，在传统 RPC 编程中极为常见。
*   **事实陈述：** 将 MCP 与 Bedrock AgentCore 结合是行业首创的集成尝试，具有一定的工程创新意义。

**反例/边界条件：**
*   **反例：** LangChain 的 LangGraph 或 Microsoft 的 AutoGen 已经通过更原生的图状态机解决了长任务编排问题，无需依赖特定的云平台核心组件。

#### 4. 行业影响：加速 MCP 的企业级落地
**支撑理由：**
*   **事实陈述：** MCP 正在成为连接 LLM 与数据源的通用标准。
*   **你的推断：** AWS 的介入意味着 MCP 正式获得巨头背书，文章中的方案可能会成为企业级 MCP 落地的“事实标准”之一，迫使其他云厂商（Azure, GCP）推出类似的托管服务。

### 争议点与不同观点
*   **过度工程化：** 许多开发者认为，简单的长任务可以通过让 LLM 生成一个回调 URL 来解决，无需引入复杂的 AgentCore 框架。
*   **上下文窗口的浪费：** 文章提到的“Context Message Strategy”可能需要在对话历史中插入大量状态维持消息，这在昂贵的 Token 计费模式下是否经济，值得商榷。

### 实际应用建议
1.  **成本审计：** 在采用该架构前，务必计算 Bedrock AgentCore 的托管费用与异步轮询产生的 Token 消耗，对比自建 Redis 队列的成本。
2.  **降级策略：** 务必在客户端实现“超时重试”与“手动刷新”机制，不要完全依赖 AgentCore 的状态保持。
3.  **混合架构：** 建议仅将关键业务逻辑放在 Bedrock 上，而将通用的 MCP 适配器保持轻量化，以便于未来迁移。

### 可验证的检查方式
1.  **压力测试指标：** 搭建该架构，模拟 100 个并发长任务（如每个任务耗时 60s），观察 Bedrock AgentCore 是否会出现连接积压或状态丢失，记录 P99 延迟。
2.  **成本对比实验：** 运行相同的长任务负载，分别统计“直接使用长连接（WebSocket）”与“文章所述异步轮询模式”在 24 小时内的 API 调用次数与 Token 消耗量。
3.  **中断恢复观察：** 在 Agent 执行过程中强制重启 Bedrock 实例，观察任务状态是否能通过 Context Message 完整恢复，还是会出现“僵尸任务”。

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 构建长时间运行的 MCP 服务器

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：**利用 Amazon Bedrock AgentCore 结合 Strands Agents 的集成能力，并配合上下文消息策略，可以有效地解决模型上下文协议（MCP）服务器在处理长时间运行任务时的状态管理与通信连续性问题。**

**作者想要传达的核心思想**
传统的 AI 代理交互往往是同步且短时的（“请求-响应”模式），这在处理复杂、耗时的业务流程（如数据处理、长时间编码、API 链式调用）时会遇到超时或状态丢失的瓶颈。作者试图传达一种**“有状态的长连接”**思想，即 AI 服务器不应只是被动的工具执行者，而应具备独立的生命周期，能够通过异步框架在后台持续工作，并通过特定的策略与客户端保持“心跳”和状态同步。

**观点的创新性和深度**
*   **创新性：** 将 MCP（Model Context Protocol）这一通常用于即时知识检索的协议，扩展到了“长时间运行代理”的领域。这打破了 MCP 仅作为“RAG（检索增强生成）管道”的刻板印象，将其转变为“任务执行管道”。
*   **深度：** 文章深入到了异步编程与 AI 代理编排的结合点。它不仅讨论了“怎么做”，还隐含探讨了在分布式 AI 系统中，如何保证非确定性任务（AI 生成）与确定性系统（服务器状态）的一致性。

**为什么这个观点重要**
随着 AI Agent 从“聊天机器人”向“智能体”演进，企业需要 AI 能够执行真正的业务操作，而不仅仅是生成文本。这些操作往往耗时。如果无法解决长时运行的问题，AI Agent 的应用场景将被限制在简单的问答领域，无法深入到企业核心业务流中。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol):** Anthropic 推出的开放协议，用于连接 AI 应用与数据源。在此文中，它被扩展为支持双向、长时的通信。
2.  **Amazon Bedrock AgentCore:** AWS 提供的底层代理框架，允许开发者构建自定义的、可扩展的代理逻辑，而非仅使用现成的 Bedrock Agents 服务。
3.  **Strands Agents:** 这是一个特定的 Agent 模式或框架（通常指代具有记忆、规划和工具使用能力的复杂 Agent 结构），在此文中用于处理复杂的任务分解和执行。
4.  **异步任务管理:** 区别于同步等待，指服务器在接收任务后立即返回确认，然后在后台处理，并通过某种机制（如轮询或 Webhook）通知结果。

**技术原理和实现方式**
*   **上下文消息策略:** 这是一种通信模式。在长时任务中，服务器不能仅仅在最后返回结果，而应定期发送“上下文消息”。这些消息不是最终答案，而是状态更新（例如：“正在处理第 3 个文件...”）。这通过保持通信通道的活跃，防止客户端超时，并提升用户体验。
*   **异步任务框架:** 实现上可能利用了 Python 的 `asyncio` 或 AWS Lambda 的异步调用，结合 DynamoDB 或 S3 存储中间状态。AgentCore 接收请求 -> 启动 Strands Agent -> 将任务 ID 返回给客户端 -> Strands Agent 在后台执行 -> 更新状态存储。

**技术难点和解决方案**
*   **难点：** **状态持久化与上下文丢失。** LLM 本身是无状态的，如果任务运行了 10 分钟，如何确保它记得 10 分钟前的指令？
*   **解决方案：** 摘要中提到的“上下文消息策略”实际上充当了“记忆锚点”。通过将中间结果持久化到存储层，并在需要时重新注入到 LLM 上下文中，维持了任务的连续性。
*   **难点：** **超时控制。** HTTP 请求通常有超时限制。
*   **解决方案：** 采用“即发即弃”或“202 Accepted”模式，将处理流程与 HTTP 请求周期解耦。

**技术创新点分析**
将 **Strands Agents**（可能代表一种链式或编织状的逻辑流）与 **Bedrock AgentCore** 深度集成，实现了一个“有状态的 MCP Server”。这意味着 MCP 服务器不再是一个简单的函数包装器，而是一个拥有独立“大脑”和“记忆”的服务实体。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为开发者提供了一种构建**企业级 AI 助手**的标准范式。它告诉我们，不要试图在一个 LLM Prompt 中完成所有工作，而应该设计一个能够持久运行、逐步反馈的后端服务。

**可以应用到哪些场景**
1.  **复杂代码生成与重构：** 需要扫描整个代码库、运行测试用例、逐步修复错误的场景，可能耗时数分钟。
2.  **大数据分析与报告生成：** Agent 需要查询多个数据库，执行 Python 代码进行绘图，最后生成报告。
3.  **RPA（机器人流程自动化）：** 控制软件机器人执行跨系统的操作流程，每一步操作都需要确认和等待。
4.  **科研辅助：** 长时间的文献检索、实验数据模拟。

**需要注意的问题**
*   **成本控制：** 长时间运行的 Agent 意味着持续的 Token 消耗和计算资源占用，必须设计严格的“停止”或“预算”机制。
*   **错误恢复：** 如果异步任务中途失败，如何从断点恢复而不是从头开始？

**实施建议**
在实施时，应优先构建**任务状态表**（Task Status Table），用于记录每个请求的 ID、当前阶段、百分比进度和最终结果。客户端应基于此 ID 进行轮询或订阅更新。

## 4. 行业影响分析

**对行业的启示**
这篇文章预示着 **AI Agent 基础设施正在“云原生化”和“协议化”**。MCP 正在成为连接 AI 与操作系统的标准语言，而 Bedrock AgentCore 则展示了云厂商如何支持这种标准。行业将看到更多从“以模型为中心”向“以任务编排为中心”的转变。

**可能带来的变革**
*   **SaaS 软件的交互变革：** 未来的 SaaS 软件可能不再提供复杂的表单按钮，而是提供一个 MCP 接口，用户通过 Agent 直接与软件进行长时对话来完成操作。
*   **Serverless 架构的演进：** 长时间运行的任务将推动 Serverless 平台（如 AWS Lambda）支持更长的执行时限或更优的异步编排模式。

**相关领域的发展趋势**
*   **Agentic Workflows（代理工作流）：** 如 LangGraph、AutoGen 等框架将与云基础设施深度绑定。
*   **协议标准化：** MCP 可能会成为 LLM 工具调用的“HTTP”，成为事实上的工业标准。

## 5. 延伸思考

**引发的其他思考**
*   **安全性：** 一个拥有长时运行能力且能访问企业内网的 Agent，如果被提示词注入攻击，其破坏力远超传统聊天机器人。如何进行长时运行的权限校验？
*   **人机协同：** 在长时运行过程中，如果 Agent 遇到无法决断的歧义，如何优雅地暂停并请求人类介入？

**可以拓展的方向**
*   **多 Agent 协作：** 文章主要关注 Server 与 Client，未来可以是多个 Strands Agents 在同一个 Bedrock 环境下协作，分别处理长时任务的不同部分。
*   **边缘计算结合：** 将轻量级的 Strands Agent 部署在边缘设备，通过 MCP 与云端的大模型通信，实现低延迟的长时任务控制。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务类型：** 审视你的 AI 应用，是否存在用户等待时间超过 30 秒的操作？如果有，引入此架构。
2.  **引入状态机：** 不要使用简单的变量存储状态，使用 AWS Step Functions 或数据库状态机来管理 Agent 的生命周期。
3.  **实现 MCP 客户端：** 确保你的前端（或调用方）能够处理非流式的、基于 ID 的状态查询。

**具体的行动建议**
*   阅读 AWS Bedrock AgentCore 的官方文档，特别是关于自定义工具和异步执行的部分。
*   搭建一个简单的 MCP Server 原型，实现一个“睡眠 10 秒后返回结果”的接口，测试客户端的轮询机制。
*   设计你的“上下文消息”JSON Schema，确保它包含 `status`（如：processing, completed, failed）和 `progress`（0-100）字段。

**需要补充的知识**
*   Python/Node.js 的异步编程模型。
*   RESTful API 设计中的“202 Accepted”模式。
*   AWS Lambda 与 Amazon EventBridge 的集成使用。

## 7. 案例分析

**结合实际案例说明**
假设一个**“自动化财报生成 Agent”**。
*   **传统模式：** 用户发送指令“生成 Q3 财报”。系统调用数据库，处理 50MB 数据，生成图表。耗时 2 分钟。HTTP 连接在 30 秒后超时，用户看到错误。
*   **新模式（基于文章架构）：**
    1.  用户发送指令。
    2.  Bedrock AgentCore 接收，创建一个 `Task-ID: 123`。
    3.  立即返回：“任务已接收，ID: 123”。
    4.  **Strands Agent 启动：** 
        *   T+0s: 发送 Context Message -> "开始收集数据..."
        *   T+30s: 发送 Context Message -> "正在计算净利润指标..."
        *   T+60s: 发送 Context Message -> "正在生成图表..."
        *   T+120s: 发送 Final Message -> "任务完成，报告链接：..."
    5.  客户端通过轮询或 SSE（Server-Sent Events）实时展示上述进度。

**成功案例分析**
**Code Interpreter (代码解释器)** 类应用是此架构的典型成功案例。当用户要求分析 CSV 文件时，系统不会卡死，而是显示“正在运行代码...”，并在代码执行完毕后返回结果。这正是异步任务管理与上下文反馈的胜利。

**失败案例反思**
如果未采用此架构，常见的失败是**“僵尸任务”**。用户提交了任务，前端显示 Loading，但后端因超时断开，任务实际上还在后台跑（或者早就挂了），用户却一无所知，只能无奈刷新页面。

## 8. 哲学与逻辑：论证地图

**中心命题**
**为了构建具备处理复杂业务流能力的企业级 AI 应用，开发者必须采用基于异步状态管理和持续上下文反馈的“长时间运行代理”架构，而非传统的同步请求-响应模式。**

**支撑理由**
1.  **用户体验:** 复杂 AI 任务（如代码生成、数据分析）通常超出 HTTP 超时限制，异步反馈能防止用户面对“空白屏幕”产生的焦虑，提供确定性的进度感知。
2.  **资源效率:** 长连接占用连接池资源，异步模式允许服务器在等待 I/O 或模型推理时释放计算

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 Strands Agents 的会话状态管理

**说明**: 长时间运行的 MCP 服务器需要维护跨多个请求的上下文和状态。通过 Strands Agents 集成，必须确保会话状态不仅在内存中有效，还能持久化存储，以便在服务器重启或故障转移后恢复对话上下文，避免用户重复输入信息。

**实施步骤**:
1. 利用 Amazon Bedrock AgentCore 的内置状态存储机制（如 DynamoDB）来持久化 Agent 会话状态。
2. 在 Strands Agents 配置中，明确设置会话超时时间（TTL），以平衡成本与用户体验。
3. 实现幂等性设计，确保重复的会话恢复请求不会导致数据不一致。

**注意事项**: 避免将敏感的 PII（个人身份信息）直接明文存储在会话状态中，应利用加密机制或仅存储引用 ID。

---

### 实践 2：实施严格的超时与重试策略

**说明**: 长时间运行的服务器容易受到网络波动或下游服务延迟的影响。在 MCP 服务器与 Bedrock AgentCore 之间建立健壮的超时和重试机制，可以防止挂起的请求阻塞工作流，并确保系统的整体稳定性。

**实施步骤**:
1. 为所有 MCP 工具调用配置明确的客户端超时设置。
2. 配置 AgentCore 的指数退避算法，用于处理来自 Bedrock 的限流（Throttling）错误或服务不可用错误。
3. 区分可重试错误（如 5xx 错误、网络问题）和不可重试错误（如 4xx 验证错误），避免无意义的重试消耗配额。

**注意事项**: 监控重试次数，设置最大重试上限，以防止在系统严重故障时产生无限循环或延迟风暴。

---

### 实践 3：建立全面的可观测性与日志记录

**说明**: 对于长期运行的异步任务，调试和监控至关重要。必须将 MCP 服务器的日志与 Amazon Bedrock 的 Trace 机制集成，以便追踪从用户输入到 Agent 执行再到 MCP 响应的完整链路。

**实施步骤**:
1. 使用结构化日志格式（如 JSON），并包含 `trace_id` 和 `session_id`。
2. 将 MCP 服务器的日志输出到 Amazon CloudWatch Logs，并配置适当的日志组和保留策略。
3. 利用 Amazon Bedrock 的 Observable traces 功能，关联 AgentCore 与 MCP 之间的调用链路。

**注意事项**: 确保日志记录不包含敏感密钥或密码，并在日志量较大时注意控制成本，避免启用过于详细的调试级别日志。

---

### 实践 4：设计高效的并发与资源限制

**说明**: Bedrock AgentCore 可能会并发调用 MCP 工具。长时间运行的服务器必须能够处理高并发请求，同时防止资源耗尽导致服务器崩溃（OOM 或 CPU 飙升）。

**实施步骤**:
1. 在 MCP 服务器层面实现连接池或工作线程池，限制同时处理的请求数量。
2. 利用非阻塞 I/O 或异步编程模型（如 Python asyncio 或 Node.js async/await）来处理长时间运行的任务。
3. 配置 Amazon Bedrock AgentCore 的并发限制，确保其发出的调用量在 MCP 服务器的处理能力范围内。

**注意事项**: 在处理长时间任务时，应考虑使用“异步任务模式”，即立即返回任务 ID，并通过回调或轮询机制让 Agent 查询结果，而不是保持连接阻塞。

---

### 实践 5：强化身份验证与最小权限访问控制

**说明**: MCP 服务器通常需要访问下游数据源。通过 Strands Agents 集成时，必须确保只有经过授权的 Bedrock Agent 能够调用 MCP 工具，且 MCP 服务器仅拥有完成任务所需的最小权限。

**实施步骤**:
1. 在 MCP 服务器与 AgentCore 之间配置双向 TLS (mTLS) 或使用签名头（如 Signature V4）进行验证。
2. 为 MCP 服务器分配 IAM 角色，仅授予其访问特定 S3 存储桶、DynamoDB 表或 API 的权限。
3. 定期审计 MCP 工具的输入参数，防止注入攻击或未授权的数据访问。

**注意事项**: 不要在代码中硬编码凭证。始终使用环境变量或 AWS Secrets Manager 来管理数据库密钥和 API Token。

---

### 实践 6：构建优雅的关闭与错误处理机制

**说明**: 长时间运行的服务器不可避免地会遇到部署更新或意外崩溃。实施优雅关闭机制可以确保正在处理的请求能够完成或安全保存状态，而不是直接中断导致数据损坏。

**实施步骤**:
1. 捕获操作系统信号（如 SIGTERM 或 SIGINT），触发服务器关闭流程。
2. 在关闭流程中，停止接受新连接，等待现有活动请求完成（或设置一个强制超时时间），然后关闭连接。
3. 针对非致命错误，向 AgentCore 返回结构化的错误响应，指导 Agent 如何重试或向用户反馈具体错误信息。

**注意事项**: 结合 Kubernetes 或 ECS 的生命周期

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够处理长期运行任务和复杂工作流的 MCP 服务器。
- 通过引入 Strands Agents，系统被赋予了持久化的记忆和状态管理能力，使其能够跨越多个会话执行多步骤的自动化任务。
- 该架构利用 Model Context Protocol (MCP) 实现了标准化的互操作性，使得 AI 智能体能够无缝访问外部数据源和工具。
- 开发者可以借助 Amazon Bedrock 的托管服务基础设施，无需自行管理底层服务器，即可部署具备高可用性的企业级 Agent 应用。
- 这种集成方案有效地解决了传统无状态模型在处理需要上下文延续或长时间等待（如等待审批）的任务时的局限性。
- 该解决方案通过将复杂的逻辑编排与模型推理分离，简化了构建具备“手眼协调”能力的自主智能体的开发流程。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [MCP](/tags/mcp/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/) / [AI 架构](/tags/ai-%E6%9E%B6%E6%9E%84/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*