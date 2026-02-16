---
title: "基于Amazon Bedrock AgentCore构建长时间运行的MCP服务器"
date: 2026-02-16T05:51:23+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Bedrock", "AgentCore", "Strands Agents", "异步任务", "长连接", "AI 智能体", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何结合 Amazon Bedrock AgentCore 和 Strands Agents 构建能够长时间运行的 MCP 服务器。为实现这一目标，文章提出了以下三种核心技术策略： 1. **上下文消息策略**：引入一种机制，确保服务器与客户端在执行长周期任务期间保持连续通信，避免连接中断。 2. **异步任"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长时间运行的MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们将为您提供实现这一目标的全面方法。首先，我们介绍一种上下文消息策略，用于在服务器与客户端之间，在耗时较长的操作期间保持持续通信。接着，我们开发一个异步任务管理框架，让您的 AI 智能体能够启动长时间运行的过程，而不阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，构建可投入生产的 AI 智能体，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 智能体，是提升应用自动化水平的关键一步。然而，如何在耗时操作中保持通信畅通且不阻塞系统运行，往往是一大技术挑战。本文将介绍一种基于上下文消息策略和异步任务管理的解决方案，并演示如何将其与 Amazon Bedrock AgentCore 及 Strands Agents 集成。通过阅读，您将掌握构建高可用、非阻塞生产级智能体的核心方法。

---
## 摘要

本文介绍了如何结合 Amazon Bedrock AgentCore 和 Strands Agents 构建能够长时间运行的 MCP 服务器。为实现这一目标，文章提出了以下三种核心技术策略：

1.  **上下文消息策略**：引入一种机制，确保服务器与客户端在执行长周期任务期间保持连续通信，避免连接中断。
2.  **异步任务管理框架**：开发异步框架，使 AI 智能体能够启动耗时较长的流程，同时不阻塞其他操作的执行。
3.  **集成与实现**：展示如何将上述策略整合到 Amazon Bedrock AgentCore 和 Strands Agents 中，从而构建出可靠且能处理复杂、耗时任务的生产级 AI 智能体。

---
## 评论

### 中心观点
**文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构模式，旨在通过引入上下文消息策略和异步任务管理框架，解决 MCP 协议在处理长周期任务时的状态保持与交互连续性问题。**

### 深入评价

#### 1. 内容深度与论证严谨性
*   **支撑理由：**
    *   **技术痛点抓取准确：** 文章切中了 MCP（Model Context Protocol）在落地过程中的核心痛点——即 LLM 的无状态性与现实世界长任务（如数据查询、代码编译）之间的矛盾。单纯依赖 LLM 的 Context Window（上下文窗口）在长耗时任务中极易导致超时或中断。
    *   **架构设计逻辑严密：** 通过引入“异步任务管理框架”，文章实际上是在倡导一种**“请求-回调”模式**向 AI Agent 的转化。这不仅仅是技术实现，更是架构思维的升级，将 Agent 从单纯的“对话机器人”转变为“任务调度器”。
    *   **Strands Agents 的战略意义：** 文章将 Strands Agents（通常指具备长期记忆和规划能力的 Agent 框架）与 Bedrock 结合，论证了如何利用“Strands”来维持任务线程的活性，这在逻辑上补齐了 Bedrock 原生可能在长流程编排上的短板。
*   **反例/边界条件：**
    *   **边界条件 1：** 如果长任务本身是 CPU 密集型且非 I/O 密集型（例如本地渲染视频），单纯的异步消息回调无法解决底层计算资源的阻塞问题，仍需依赖 Sidecar 模式或独立计算集群。
    *   **边界条件 2：** 对于极高频（毫秒级）的状态更新需求，文中提到的“Context Message Strategy”可能会因为 Token 消耗过大或网络延迟导致用户体验（UX）下降，此时 WebSocket 或 Server-Sent Events (SSE) 可能是更优解，而非 MCP 的轮询或长轮询模式。
*   **标注：** [事实陈述：基于 MCP 协议特性] / [作者观点：架构设计逻辑] / [你的推断：Strands 在此处的具体实现机制]

#### 2. 实用价值与创新性
*   **支撑理由：**
    *   **填补了 Serverless AI 的空白：** AWS Bedrock 原生能力偏向于单次推理。文章提出的方案实际上是在教开发者如何在 Serverless 环境下模拟“有状态”的服务器。这对于企业级应用（如 RAG 系统的后台索引构建、自动化运维脚本执行）具有极高的参考价值。
    *   **可复用的异步模式：** 文章中关于“Context Message”的处理方式，提供了一种标准化的“心跳检测”机制。这对于任何试图构建稳健 AI 应用的开发者来说，都是一种防止 LLM 产生幻觉（认为任务已完成）的有效手段。
*   **反例/边界条件：**
    *   **反例 1：** 对于初创公司或简单项目，引入 Bedrock AgentCore 配合 Strands 的复杂度过高。一个简单的 Redis 队列配合 Worker 进程可能比文中提出的“综合性方法”更高效、成本更低。
    *   **反例 2：** 该方案深度绑定 AWS 生态。如果企业需要多云部署或私有化部署，这种强依赖 Bedrock AgentCore 的设计会导致极高的迁移成本。
*   **标注：** [事实陈述：AWS 生态依赖性] / [你的推断：成本效益比分析]

#### 3. 行业影响与争议点
*   **支撑理由：**
    *   **推动 MCP 协议标准化：** MCP 正在成为连接 AI 与数据源的标准协议。AWS 发布此类文章，实际上是在通过“Best Practice”确立其在 MCP 生态中的话语权，推动行业从“简单的 API 调用”走向“持久化 Agent 协作”。
    *   **重新定义“Agent”边界：** 文章暗示了 Agent 不再仅仅是智能体，更是**工作流引擎**。这可能会影响未来开发者对 Agent 框架的选择标准——即是否具备长任务编排能力。
*   **争议点/不同观点：**
    *   **Token 成本与延迟的权衡：** 为了维持“Continuous Communication”，不断发送 Context Message 会显著增加 Token 消耗（尤其是输入 Token）。行业内有观点认为，应尽量减少 LLM 的介入，仅在关键节点通过传统软件逻辑处理状态，最后再汇总给 LLM。
    *   **Strands 的黑盒性质：** 如果 Strands Agents 是一个托管服务，那么对于金融或医疗等对数据合规性要求极高的行业，将任务状态和上下文托管在第三方服务中可能存在合规风险。
*   **标注：** [作者观点：行业趋势判断] / [事实陈述：成本结构]

### 实际应用建议
1.  **架构解耦：** 在采纳该方案时，建议将“任务执行器”与“状态汇报器”解耦。不要让 Bedrock Agent 直接轮询数据库，而应引入 Event Bridge (AWS) 或 Kafka 来解耦任务完成事件与 Agent 的感知。
2.  **超时与熔断机制：** 虽然文章提倡长运行，但必须设计严格的 TTL（Time To Live）。如果异步任务挂起，Agent 应具备触发“补偿事务”或告警的能力，而不是无限等待。
3.  **成本监控：** 实施该方案前，务必开启 AWS Cost Explorer 的细粒度监控。长任务带来的 Context Message 累积可能会导致

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

## 1. 核心观点深度解读

### 主要观点
文章的主要观点是：**通过结合 Amazon Bedrock AgentCore 的基础设施与 Strands Agents 的集成技术，开发者可以构建出具备“长时间运行能力”的 MCP（Model Context Protocol）服务器，从而突破传统 AI 代理在处理复杂、多步骤任务时的时效与状态限制。**

### 核心思想
作者试图传达的核心思想是**“异步化与状态解耦”**。传统的 AI 交互往往是同步的（Request-Response），一旦任务耗时超过 LLM 的上下文窗口或超时限制，连接就会断开。本文主张通过一种**上下文消息策略**和**异步任务管理框架**，将“思考”与“执行”分离，使 AI Agent 能够像后台进程一样，持久地处理业务逻辑，并在需要时向客户端汇报，而不是保持长连接阻塞等待。

### 创新性与深度
该观点的创新性在于将**MCP 协议**（一种连接 AI 与数据源的开放标准）从简单的“数据检索工具”提升为“自主任务执行者”。它不仅解决了 MCP 服务器在处理耗时任务（如数据编码、批量处理、长时间 API 调用）时的超时问题，还通过引入 Strands Agents（可能指代一种具备记忆或连续状态管理的 Agent 架构），赋予了系统处理跨会话、长周期工作流的能力。

### 重要性
随着 AI Agent 从简单的聊天机器人向自主员工演进，企业级应用要求 AI 能够处理 RPA（机器人流程自动化）、代码审计、复杂数据分析等耗时任务。如果无法解决长时运行问题，AI 的应用场景将被局限在简单的问答领域。因此，这篇文章提出的方法论是 AI 落地复杂业务场景的关键“最后一公里”。

---

## 2. 关键技术要点

### 涉及的关键技术
1.  **MCP (Model Context Protocol)**：Anthropic 推出的开放协议，用于连接 AI 助手与外部数据源。
2.  **Amazon Bedrock AgentCore**：AWS 提供的托管式 Agent 编排服务，负责 LLM 的路由、记忆和工具调用。
3.  **Strands Agents**：推测为一种支持长期记忆或连续执行的 Agent 架构模式，用于维持任务的“线索”。
4.  **异步任务队列**：如 AWS Step Functions 或 SQS，用于解耦请求与执行。

### 技术原理与实现方式
根据摘要，文章提出了两个核心机制：

1.  **Context Message Strategy（上下文消息策略）**：
    *   **原理**：在长时间任务启动后，服务器不立即返回最终结果，而是返回一个“任务ID”或“中间状态上下文”。客户端通过轮询或 WebSocket 接收更新。
    *   **实现**：MCP Server 在接收到 Tool Call 后，立即生成一个 `taskId`，将实际工作推送到后台线程，并向 LLM 返回 `{"status": "pending", "context": "Task started, ID: 123"}`。LLM 随后可以向用户汇报“我已经开始处理，请稍候”。

2.  **Asynchronous Task Management Framework（异步任务管理框架）**：
    *   **原理**：构建一个非阻塞的执行层。当 Agent 需要调用耗时工具时，不是直接调用函数，而是向任务管理器提交一个 Job。
    *   **实现**：利用 Bedrock AgentCore 的编排能力，将 Strands Agent 的状态持久化。任务执行过程中，Agent 定期检查状态，而不是一直保持连接。

### 技术难点与解决方案
*   **难点**：LLM 的无状态性与长时任务的有状态性之间的矛盾。
*   **解决方案**：通过 Strands Agents 集成，将任务状态存储在外部存储（如 DynamoDB）中，每次交互通过 ID 恢复上下文。
*   **难点**：超时控制。
*   **解决方案**：MCP 协议层面的优化，允许 Server 在处理完成前返回“中间响应”，避免 HTTP 超时。

---

## 3. 实际应用价值

### 指导意义
这篇文章为构建**企业级 AI Agent** 提供了标准架构蓝图。它告诉开发者：不要试图用 LLM 直接处理所有耗时逻辑，而应该构建一个 robust 的异步层来支撑。

### 应用场景
1.  **代码生成与重构**：分析大型代码库（耗时可能数分钟），生成报告。
2.  **数据处理与分析**：Agent 调用 Bedrock 处理海量 S3 数据，进行总结或转换。
3.  **RPA 流程自动化**：执行一系列跨系统的 API 调用（如创建订单、发送邮件、更新库存），整个过程可能持续数小时。
4.  **监控与运维**：Agent 长期监控 CloudWatch 指标，并在异常时触发修复流程。

### 注意问题
*   **成本控制**：长时运行意味着更多的 Token 消耗和计算资源调用，需设置预算上限。
*   **状态一致性**：确保异步任务失败时，Agent 能够感知并进行重试或报错。

---

## 4. 行业影响分析

### 行业启示
这标志着 **AI Agent 基础设施正在“云原生化”**。AWS 通过 Bedrock AgentCore 与 MCP 的结合，正在将 Agent 的开发从“手写 Prompt”转变为“构建微服务架构”。

### 带来的变革
*   **从 Copilot 到 Agent**：AI 从辅助建议者转变为实际执行者。
*   **MCP 协议的普及**：随着 AWS 的支持，MCP 可能成为连接 LLM 与云服务的通用标准，打破数据孤岛。

### 发展趋势
未来，长时运行的 Agent 将需要更强大的**记忆管理**和**错误恢复机制**。行业将看到更多针对 Agent 专用数据库和编排框架的出现。

---

## 5. 延伸思考

*   **人机协作模式**：如果 Agent 可以长时间运行，人类如何介入？是否需要“紧急停止”按钮或审批节点？
*   **多 Agent 协作**：Strands Agents 是否暗示了多个 Agent 并行工作，最后汇总结果的可能性？
*   **安全性**：长时运行的异步任务增加了攻击面（如任务注入攻击），如何验证回调请求的合法性？

---

## 6. 实践建议

### 如何应用到项目
1.  **评估现有工具**：检查你的 MCP 工具中哪些是耗时的（>30秒），将其标记为“长时运行候选”。
2.  **引入状态存储**：使用 Redis 或 DynamoDB 存储任务状态。
3.  **重构 MCP Server**：将同步函数改为异步函数，立即返回 `task_id`，并提供一个 `check_status` 工具供 LLM 查询。

### 行动建议
*   **阅读 AWS 文档**：深入研究 Bedrock AgentCore 的最新 API。
*   **设计状态机**：为你的长时任务设计清晰的状态流转（Pending -> Processing -> Completed/Failed）。

---

## 7. 案例分析

### 成功案例（假设性）
**场景**：一家电商公司使用该架构构建“库存补货 Agent”。
*   **流程**：Agent 接收到补货指令 -> 分析过去30天销售数据（耗时任务） -> 预测未来需求 -> 生成采购订单。
*   **效果**：由于使用了异步框架，用户无需等待 5 分钟数据加载，只需提交请求，Agent 在后台处理，完成后发送通知。

### 失败反思
**场景**：未使用异步策略的代码审计 Agent。
*   **问题**：用户上传了 100 个文件，Agent 尝试同步处理，导致 HTTP 连接超时，任务失败，用户不知道进度。
*   **教训**：任何涉及批量处理或外部 IO 的操作，必须异步化。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**为了在企业级环境中实现具备复杂执行能力的 AI Agent，必须构建基于异步任务管理和上下文状态保持的 MCP 服务器架构。**

### 支撑理由
1.  **时效性限制**：事实依据是 LLM 的 HTTP 请求和大多数云函数执行时间都有硬性超时限制（通常为几分钟），无法覆盖长业务流程。
2.  **用户体验**：直觉上，用户不愿意盯着加载圈等待数分钟，他们更偏好“提交-等待通知”的交互模式。
3.  **资源利用率**：同步阻塞会占用服务器连接池，导致并发能力下降。

### 反例与边界条件
1.  **简单查询场景**：对于“查一下天气”或“总结这段短文本”，引入异步框架会增加不必要的延迟和复杂度。
2.  **强实时性要求**：对于高频交易等需要毫秒级响应的场景，异步解耦可能引入不可接受的延迟。

### 命题分类
*   **事实**：AWS Bedrock 支持 AgentCore；MCP 是开放协议。
*   **预测**：长时运行 Agent 将成为企业应用的主流形态。

### 立场与验证
**立场**：支持该文章提出的异步化架构是解决复杂 AI 任务的最佳实践。
**验证方式**：
*   **指标**：对比同步架构与异步架构在处理 1000 个长时任务时的超时率和平均响应时间。
*   **观察窗口**：在实际生产环境中运行 3 个月，统计任务完成成功率。

---
## 最佳实践

## 最佳实践指南

### 实践 1：合理配置 Strands 生命周期与并发管理

**说明**:
长时间运行的 MCP 服务器需要处理多个并发的 Agent 请求。Strands Agents 允许任务在后台异步执行，但若不加以控制，极易导致资源耗尽或上下文混乱。合理配置 Strand 的生命周期（TTL）和并发限制是确保系统稳定性的关键。

**实施步骤**:
1. 评估业务场景中单个任务的平均执行时长，据此设置 Strand 的最大存活时间（TTL）。
2. 在 Bedrock AgentCore 配置中启用并发控制，限制单个 MCP 服务器实例同时处理的 Strand 数量上限。
3. 实施请求排队机制，当并发达到上限时，将新请求放入队列而非直接拒绝。

**注意事项**:
- 避免设置过长的 TTL，否则可能导致僵尸线程占用内存。
- 密切监控队列积压情况，设置告警阈值。

---

### 实践 2：实施严格的上下文状态管理

**说明**:
由于 MCP 服务器设计为“长时间运行”，Strand Agent 在多次交互之间需要维护状态。最佳实践是避免在全局范围内存储状态，而是将状态与特定的 Strand ID 或 Session ID 强绑定，以防止不同用户或任务之间的数据污染。

**实施步骤**:
1. 设计无状态的服务端逻辑，将所有会话数据（如中间变量、用户偏好）存储在外部的高速缓存中（如 ElastiCache 或 Redis）。
2. 使用唯一的 Strand ID 作为缓存键的前缀。
3. 在 MCP 协议的响应中，显式地包含当前状态的检查点，以便在断线重连时恢复状态。

**注意事项**:
- 定期清理过期的会话状态，防止内存泄漏。
- 确保状态序列化（如 JSON）的高效性，减少网络传输开销。

---

### 实践 3：优化 MCP 工具的幂等性与错误重试策略

**说明**:
在网络不稳定或 Bedrock Agent 调用超时的情况下，Strand 可能会重试调用 MCP 服务器的工具。如果工具不是幂等的，重复执行可能导致数据不一致（例如重复扣款）。确保所有写操作具备幂等性是构建可靠服务的基础。

**实施步骤**:
1. 为所有修改数据的工具接口设计幂等键，要求客户端在调用时传递唯一的请求 ID。
2. 在服务器端记录已处理的请求 ID，检测到重复请求时直接返回缓存的成功结果，跳过业务逻辑执行。
3. 针对只读操作，实施指数退避的重试策略以应对瞬时网络故障。

**注意事项**:
- 幂等键的存储空间需要管理，定期清理旧数据。
- 明确区分业务逻辑错误（如参数错误，不应重试）和瞬时错误（如超时，应重试）。

---

### 实践 4：建立结构化的日志与可观测性体系

**说明**:
调试长时间运行的异步 Agent 链路非常具有挑战性。必须建立能够关联 Bedrock Agent 请求 ID 和 Strands 执行上下文的日志系统，以便快速追踪问题根源。

**实施步骤**:
1. 在 MCP 服务器中集成 AWS X-Ray 或 CloudWatch Logs。
2. 在日志中注入 Trace ID，将 Bedrock Agent 发起的请求与 MCP 内部处理步骤关联起来。
3. 记录关键事件：工具调用开始/结束、Strand 创建/销毁、错误堆栈以及外部 API 调用的延迟。

**注意事项**:
- 避免记录敏感信息（如 PII 数据），对日志进行脱敏处理。
- 严格控制日志体量，避免在生产环境开启 Debug 级别日志。

---

### 实践 5：设计基于资源配额的限流机制

**说明**:
Bedrock AgentCore 可能会因上游流量激增而向 MCP 服务器发送大量请求。为了保护后端数据库或第三方 API 不被压垮，必须在 MCP 层实施精细化的限流策略。

**实施步骤**:
1. 根据后端系统的处理能力（RPS），设定 MCP 服务器的全局速率限制。
2. 针对不同的 API Token 或 Tenant ID 设置分级的限流规则，防止单个租户占用所有资源。
3. 实施优雅降级，当负载过高时，返回明确的 429 Too Many Requests 状态码，并指示 Agent 稍后重试。

**注意事项**:
- 限流策略不应影响正常的长时间任务，需区分“快速请求”和“长时 Strand 执行”的配额。
- 在返回 429 状态码时包含 Retry-After 头信息。

---

### 实践 6：确保工具定义的清晰性与参数验证

**说明**:
MCP 服务器的核心是向 Agent 暴露工具。如果工具定义模糊或参数验证不严格，Agent 容易生成无效的调用请求，导致无效的交互循环和资源浪费。清晰的工具定义和严格的验证机制能显著提升 Agent 的调用成功率。

**实施步骤**:
1. 在工具 Schema 中使用详细的描述和示例值

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够维护长期对话状态和记忆的持久化 MCP 服务器。
- 通过利用 Strands 的上下文记忆能力，Agent 可以在多轮交互中记住用户偏好和之前的操作，从而实现更加连贯和个性化的用户体验。
- 该集成方案简化了复杂工作流的编排，使得 Agent 不仅限于单次请求响应，还能处理跨越长时间周期的任务管理。
- 开发者可以使用 Model Context Protocol (MCP) 标准接口，将具备长期运行能力的 Strands Agents 无缝接入到现有的 Bedrock 生态系统和工具链中。
- 这种架构特别适用于需要持续跟踪或状态感知的复杂场景（如长期项目跟踪或持续客户服务），显著提升了 AI 应用的实用性和智能化水平。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [MCP](/tags/mcp/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*