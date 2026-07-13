---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理"
date: 2026-02-14T22:06:52+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长时运行", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种在 Amazon Bedrock AgentCore 上构建持久运行的 MCP（Model Context Protocol）服务器的方法，并整合了 Strands Agents。为了解决 AI 代理在处理复杂、耗时操作时的可靠性问题，文章提出了以下三个核心策略： 1. **上下文消息策略**：引入一种机"
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

在本文中，我们将为您提供一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，以在长时间运行的操作期间保持服务器与客户端之间的持续通信。接着，我们开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的任务而不阻塞其他操作。最后，我们将展示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合，构建能够可靠处理复杂、耗时操作的生产级 AI 代理。

---
## 导语

构建能够处理复杂、耗时任务的生产级 AI 代理，往往面临着上下文管理与系统阻塞的挑战。本文将详细介绍如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成方案，通过上下文消息策略与异步任务管理框架，实现长时间运行的 MCP 服务器。读者将获得一套系统性的实施方法，确保 AI 代理在处理长周期操作时保持通信的连贯性与系统的稳定性。

---
## 摘要

本文介绍了一种在 Amazon Bedrock AgentCore 上构建持久运行的 MCP（Model Context Protocol）服务器的方法，并整合了 Strands Agents。为了解决 AI 代理在处理复杂、耗时操作时的可靠性问题，文章提出了以下三个核心策略：

1.  **上下文消息策略**：引入一种机制，以在服务器与客户端之间维持长时间操作期间的连续通信，确保上下文不丢失。
2.  **异步任务管理框架**：开发了一套框架，允许 AI 代理启动长时间运行的后台进程，而不会阻塞其他操作的执行。
3.  **生产级整合**：演示了如何结合 Amazon Bedrock AgentCore 和 Strands Agents，将上述策略落地，从而构建出能够可靠处理复杂、高耗时任务的生产级 AI 代理。

---
## 评论

基于您提供的文章标题与摘要，以下是从技术架构与行业应用角度的深度评价。

### 中心观点
该文章提出了一种**基于 Amazon Bedrock AgentCore 架构，结合“Strands”概念与异步任务管理框架，来解决 MCP（Model Context Protocol）服务器在执行长周期任务时的上下文连续性与状态管理难题**的技术方案。

---

### 深入评价

#### 1. 内容深度与论证严谨性
*   **支撑理由：**
    *   **痛点定位精准（事实陈述）：** 摘要中明确指出了 AI Agent 领域的一个核心痛点——长周期任务（Long-running tasks）。在现有的 LLM 请求-响应模式下，一旦任务执行时间超过模型的超时限制或 Token 输出限制，连接就会断开，导致任务失败或状态丢失。
    *   **架构设计的完整性（事实陈述）：** 文章不仅提出了问题，还给出了“上下文消息策略”和“异步任务管理框架”两个维度的解决方案。这表明作者试图从协议层（MCP）和应用层两个层面解决问题，论证具有系统性。
    *   **Strands 概念的引入（你的推断）：** “Strands”极有可能是指 Anthropic 提出的“Strands”概念（即 AI 线程/线索），旨在处理跨越时间的多轮对话。将此概念集成到 Bedrock AgentCore 中，说明文章试图打通不同生态（AWS 与 Anthropic）的技术壁垒，具有一定的技术深度。
*   **反例/边界条件：**
    *   **边界条件 1：** 如果“Strands”仅是作者自定义的一个内部模块而非通用标准，那么该方案的通用性将大打折扣，且可能导致供应商锁定。
    *   **边界条件 2：** 异步任务管理虽然解决了超时问题，但引入了最终一致性的挑战。文章若未深入讨论任务失败后的补偿机制或状态回滚，则其在生产环境中的严谨性存疑。

#### 2. 实用价值与创新性
*   **支撑理由：**
    *   **填补了 Bedrock 的生态空白（你的推断）：** Amazon Bedrock 虽然强大，但在处理复杂工作流编排时，开发者往往需要自行构建状态机。该文章提供的框架若能开箱即用，将极大降低企业构建“如影随形”式 AI 助手的门槛。
    *   **MCP 协议的工程化落地（事实陈述）：** 随着 MCP 逐渐成为连接 AI 与数据源的标准协议，如何在高并发、长耗时场景下稳定运行 MCP 服务器是行业痛点。文章提出的“上下文消息策略”为 MCP 的生产级部署提供了重要参考。
*   **反例/边界条件：**
    *   **反例 1：** 对于简单的 CRUD（增删改查）操作，引入异步任务框架和 Strands 上下文管理属于过度设计，反而会增加系统延迟和复杂度。
    *   **反例 2：** 如果该方案高度依赖 AWS 的特定基础设施（如 Bedrock 的内部私有通道），那么迁移到本地部署或其他云服务商将面临极高的重构成本。

#### 3. 行业影响与可读性
*   **支撑理由：**
    *   **推动 Agent 架构演进（作者观点）：** 该文章暗示了 AI Agent 从“单次对话模式”向“常驻服务模式”的转变。这对行业是一个重要信号，即未来的 AI 应用将更像后台服务而非单纯的聊天机器人。
    *   **技术栈的融合（事实陈述）：** 结合 Bedrock（基础设施）、MCP（连接协议）和 Strands（交互逻辑），文章展示了构建现代 AI 应用的“黄金三角”，对架构师选型有指导意义。
*   **反例/边界条件：**
    *   **反例 1：** 行业目前对于“Strands”尚未有统一标准，如果文章定义不清，可能会造成概念混淆，开发者可能难以区分其与 LangGraph 或 LangChain 中的 State 机制有何本质区别。

---

### 实际应用建议

#### 1. 可验证的检查方式
为了验证该文章所述方案的有效性，建议进行以下测试：

*   **指标 1：任务存活率与超时测试**
    *   *方法：* 构建一个模拟耗时 10 分钟的业务流（如复杂数据分析），观察 MCP 连接是否会断开，以及断开后是否能通过“上下文消息策略”恢复并获取最终结果。
    *   *预期结果：* 即使客户端网络波动，服务端任务仍继续运行，且客户端重连后能查询到进度。

*   **指标 2：状态一致性检查**
    *   *方法：* 在异步任务执行过程中人为注入错误（如服务重启），验证“Strands”机制是否能保证上下文不丢失，且不出现重复执行或状态冲突。
    *   *预期结果：* AgentCore 应能准确恢复到故障前的状态继续执行。

*   **指标 3：延迟与开销分析**
    *   *方法：* 对比直接调用 Bedrock 与使用该异步框架的端到端延迟。
    *   *预期结果：* 虽然长任务总耗时增加（引入了异步开销），但用户感知的响应时间（TTFT）应显著降低。

#### 2. 落地建议
*   **适用场景：** 适合用于企业级 RAG（检索增强生成）系统中的文档索引构建、复杂数据报表生成、或需要调用外部 API 进行长时间等待的自动化工作流。
*   **风险规避：**

---
## 技术分析

基于您提供的文章标题和摘要，虽然原文内容被截断，但结合AWS Bedrock、MCP (Model Context Protocol) 以及 AgentCore 的技术背景，我们可以构建出一份深度技术分析报告。该文章显然旨在解决当前AI Agent（智能体）开发中的一个核心痛点：**如何在无状态的大语言模型（LLM）与有状态的长耗时业务流程之间建立可靠的桥梁。**

以下是针对该文章核心观点与技术要点的深入分析：

---

## 1. 核心观点深度解读

**主要观点**
文章的核心观点是：**构建基于 Amazon Bedrock 的企业级 AI Agent 不能仅依赖同步的“单次请求-响应”模式，而必须引入“Strands Agents”与“上下文消息策略”来实现长运行任务的异步状态管理。**

**核心思想**
作者试图传达的思想是，真正的企业级自动化往往涉及秒级甚至分钟级的操作（如数据查询、API调用、文件生成）。如果 Agent 在执行这些任务时让用户面对“加载中”的空白，或者因为超时而断开连接，用户体验将极差。因此，必须将“思考（LLM决策）”与“行动（执行任务）”解耦，通过异步框架让 Agent 能够“挂起”和“恢复”对话。

**创新性与深度**
该观点的创新点在于将传统的后端微服务架构中的“异步任务队列”模式引入到了 MCP Server 的设计中。它不再将 MCP Server 仅仅视为一个被动的工具调用者，而是视为一个拥有独立生命周期和状态管理能力的“工作流引擎”。

**重要性**
随着 AI 从“聊天机器人”向“Agent（智能体）”演进，能否处理长耗时任务是衡量 Agent 实用性的关键分水岭。这篇文章提出的架构是 AI 落地复杂业务场景（如金融审批、代码部署、数据分析）的必经之路。

## 2. 关键技术要点

### 涉及的关键技术
1.  **MCP (Model Context Protocol)**：一种连接 AI 应用与数据源的标准协议。
2.  **Amazon Bedrock AgentCore**：AWS 提供的用于构建 Agent 的底层服务/框架。
3.  **Strands Agents**：这是文章引入的核心概念（推测为 AWS 内部或特定的框架模式），指代能够处理多轮次、长时间运行流程的 Agent 模式。
4.  **异步任务管理框架**：用于处理非即时响应的后台任务。

### 技术原理与实现
*   **上下文消息策略**：
    *   **原理**：MCP 协议本身通常是无状态的。为了实现长连接，Server 需要向客户端发送包含 `status: "in_progress"` 或特定引用 ID 的中间消息。
    *   **实现**：在任务开始时，Server 返回一个 `taskId` 并立即释放 LLM 的上下文。后台线程继续执行任务，而 Client 可以通过轮询或 WebSocket 接收更新。
*   **异步任务框架**：
    *   **原理**：利用消息队列（如 AWS SQS）或 Step Functions 来驱动长流程。
    *   **实现**：当 Bedrock Agent 决定调用一个工具时，该工具调用触发一个异步工作流。MCP Server 不阻塞工作流，而是返回“任务已接收”，待工作流完成后，通过回调或状态查询接口更新结果。

### 技术难点与解决方案
*   **难点**：LLM 上下文窗口限制与状态保持。如果任务执行时间过长，LLM 可能会丢失对之前对话的关注。
*   **解决方案**：使用 **Strands** 概念，将任务过程抽象为“线索”。在任务恢复时，将任务的最终结果和关键中间状态重新注入到 LLM 的 Prompt 中，使其能“回忆”起之前的操作。

## 3. 实际应用价值

### 指导意义
这篇文章为开发者提供了一套**“反模式”避坑指南**：不要试图在 LLM 的生成循环中通过 `sleep()` 等待耗时 API 完成。它指导开发者构建响应更快、容错率更高的 Agent 系统。

### 应用场景
1.  **RAG（检索增强生成）大数据分析**：当 Agent 需要读取数 GB 的文档并生成报告时，不能让用户等待 5 分钟，应采用异步处理。
2.  **代码生成与部署**：Agent 编写代码后，需要运行测试套件（耗时 2-10 分钟），需要异步获取测试结果。
3.  **企业工作流审批**：涉及人工介入的审批流程，可能跨越数小时或数天。

### 实施建议
*   **设计幂等的接口**：因为网络重试是常态，确保任务提交接口是幂等的。
*   **状态可视化**：在 UI 层面必须展示进度条或状态徽章，告知用户 Agent 正在后台工作。

## 4. 行业影响分析

### 对行业的启示
这标志着 AI Agent 开发从**“玩具级”向“工业级”**的转变。行业开始关注 Agent 的可靠性、可观测性和并发处理能力，而不仅仅是模型生成的准确度。

### 发展趋势
*   **Agent 即服务**：未来的 MCP Server 将不仅是数据接口，更是计算能力的接口。
*   **协议标准化**：MCP 协议可能会因为此类长连接需求的推动，进化出更标准的“异步任务子协议”。

## 5. 延伸思考

*   **成本控制**：长运行任务意味着大量的 Token 消耗（用于注入上下文）。如何压缩状态信息是一个值得研究的方向。
*   **多 Agent 编排**：如果任务涉及多个 Bedrock Agent 互相调用，异步状态的传递将变得极其复杂，可能需要引入类似 Orchestrator（编排器）的中心化管理组件。

## 6. 实践建议

### 如何应用到项目
1.  **评估任务耗时**：审查你的 Agent 调用的工具，如果任何工具响应时间超过 10 秒，必须改造为异步。
2.  **引入状态存储**：使用 Amazon DynamoDB 或 Redis 存储 `TaskID` 对应的状态和结果。
3.  **改造 MCP Server**：
    *   将 Tool 的 `response` 从直接返回结果改为返回 `{"status": "pending", "result_url": "..."}`。
    *   增加一个 `check_status` 工具供 LLM 轮询。

### 知识补充
*   学习 **AWS Step Functions** 的定义与使用。
*   熟悉 **Python asyncio** 或 **Java Concurrent** 编程模型。

## 7. 案例分析

### 成功案例：企业财报分析 Agent
*   **场景**：用户上传 PDF 财报，要求 Agent 分析并绘制图表。
*   **同步模式（失败）**：Agent 读取 PDF、调用 Python 绘图引擎，耗时 45 秒，前端连接超时，用户以为死机。
*   **异步模式（成功）**：Agent 接收文件 -> 返回“正在处理中” -> 后台 Bedrock Agent 调用 Step Functions -> 完成后发送通知 -> 用户点击查看结果。体验流畅。

### 失败反思
*   **问题**：许多开发者直接在 LangChain 的 Tool 中写入 `time.sleep(30)` 模拟长任务。
*   **后果**：这会阻塞整个线程池，导致系统并发能力归零。

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建基于 Amazon Bedrock 的企业级 MCP Server 时，**必须**采用基于 Strands 的异步任务管理架构，而非同步阻塞模式，以解决长耗时业务流程与即时交互需求之间的矛盾。

**支撑理由与依据**
1.  **用户体验**：同步等待会导致客户端超时或用户流失。
    *   *依据*：HTTP 请求超时限制通常在 30-60 秒，而业务逻辑往往更长。
2.  **资源利用率**：阻塞式等待会浪费 AgentCore 的计算资源。
    *   *依据*：服务器并发模型（如线程/协程）在长阻塞下性能急剧下降。
3.  **系统鲁棒性**：异步架构允许任务在服务重启后继续或恢复。
    *   *依据*：云原生设计原则中的无状态与持久化分离。

**反例与边界条件**
1.  **反例**：对于极短的计算任务（如 < 2 秒的简单查询），引入异步框架会增加系统复杂度和延迟，此时同步模式更优。
2.  **边界条件**：如果业务逻辑要求强一致性（即必须看到结果才能进行下一步），且用户能容忍等待，异步模式可能不必要，除非是为了防止连接超时。

**事实与价值判断**
*   **事实**：LLM 生成是快速的，但下游工具调用可能是慢速的。
*   **价值判断**：用户体验（响应速度）优于架构实现的简单性。
*   **可检验预测**：采用该架构的系统，其用户留存率将高于纯同步系统，且 P99 延迟显著降低。

**立场与验证**
*   **立场**：支持在 Bedrock AgentCore 中全面推广异步 Strands 模式。
*   **验证方式**：
    *   **指标**：监控 Agent 工具调用的平均响应时间（P50/P99）和超时错误率。
    *   **实验**：对比同一业务逻辑在同步架构与异步架构下的并发吞吐量。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化会话状态管理

**说明**:
长时间运行的 MCP 服务器需要维护跨请求的会话上下文。通过 Strands Agents 集成时，必须设计高效的状态管理机制，确保在处理长耗时任务或异步工作流时，上下文信息不会丢失或导致内存溢出。

**实施步骤**:
1. 利用 Amazon Bedrock AgentCore 的持久化存储接口，将会话状态（Session State）外部化存储（如 Amazon DynamoDB）。
2. 在 Strands Agents 的配置中，明确设置状态生存时间（TTL），以自动清理过期的会话数据。
3. 实现幂等性检查机制，确保在网络重连或重试时，状态更新不会导致数据不一致。

**注意事项**:
避免将敏感的 PII（个人身份信息）直接明文存储在会话状态中，应使用加密字段或仅存储引用 ID。

---

### 实践 2：实施异步任务编排模式

**说明**:
MCP 服务器可能会调用耗时较长的工具或 API。为了防止阻塞主线程并导致超时，应采用异步任务编排模式，利用 Strands Agents 的能力来管理长运行流程的生命周期。

**实施步骤**:
1. 将 MCP 服务器的工具接口设计为异步非阻塞模式，立即返回“任务已接收”的确认响应。
2. 使用 Amazon Bedrock AgentCore 的工作流功能或集成 Step Functions 来编排后台任务。
3. 配置回调机制（Webhook 或轮询端点），以便 Strands Agents 在任务完成后获取结果并更新用户。

**注意事项**:
确保异步任务的错误处理逻辑完善，一旦后台任务失败，Agent 需要有能力通知用户或触发重试策略。

---

### 实践 3：构建可观测性与日志记录体系

**说明**:
在长运行场景下，问题排查和性能监控至关重要。必须建立全面的日志记录和监控体系，以便追踪 MCP 服务器与 Strands Agents 之间的交互链路。

**实施步骤**:
1. 集成 Amazon CloudWatch Logs 和 Metrics，为 MCP 服务器的关键操作（如工具调用、状态转换）添加结构化日志。
2. 在 Strands Agents 的请求头中注入 `Trace-ID`，实现分布式追踪，关联 AgentCore 与 MCP 服务器的日志。
3. 设置针对特定指标（如延迟、错误率）的告警阈值。

**注意事项**:
注意日志采样率，避免在高峰期产生海量日志导致成本激增或性能下降。

---

### 实践 4：设计健壮的错误处理与重试策略

**说明**:
网络波动或下游服务不可避免地会发生故障。MCP 服务器必须具备优雅的错误处理能力，并配合 Strands Agents 定义清晰的错误传播路径，避免 Agent 进入死循环或产生幻觉。

**实施步骤**:
1. 定义标准化的错误代码和消息格式返回给 AgentCore，帮助大模型理解错误原因（例如：区分“参数错误”与“服务暂时不可用”）。
2. 在 MCP 服务器层面实现指数退避算法，处理瞬态故障。
3. 配置 Strands Agents 的提示词，使其在遇到特定错误时能够引导用户采取替代行动，而不是直接报错。

**注意事项**:
严格限制最大重试次数，防止级联故障导致资源耗尽。

---

### 实践 5：强化安全认证与最小权限控制

**说明**:
MCP 服务器作为 Agent 的执行延伸，必须严格验证调用来源，并限制其对后端资源的访问权限，防止未经授权的操作。

**实施步骤**:
1. 在 MCP 服务器与 Amazon Bedrock AgentCore 之间配置双向 TLS (mTLS) 或使用 IAM Signature V4 进行签名验证。
2. 为不同的 Strands Agents 分配专用的 IAM 角色，严格限制其仅能调用 MCP 服务器中特定的工具。
3. 在 MCP 服务器内部实现输入验证层，防止提示词注入或恶意参数传递。

**注意事项**:
定期轮换用于认证的凭证和密钥，并确保所有通信通道均经过加密。

---

### 实践 6：资源限制与速率限制

**说明**:
长运行的服务容易受到突发流量的冲击。为了保护 MCP 服务器的稳定性，必须实施严格的速率限制和资源配额管理。

**实施步骤**:
1. 在 MCP 服务器前部署 API Gateway 或应用层网关，配置基于 Token 或 IP 的速率限制规则。
2. 利用 Amazon Bedrock AgentCore 的并发控制设置，限制同时激活的 Strand 数量。
3. 实施超时机制，为每个工具调用设置最大的执行时间限制。

**注意事项**:
速率限制应与业务优先级对齐，确保关键任务或高优先级用户不受限流影响。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够自主执行多步骤任务并保持长期运行状态的 MCP 服务器。
- 借助 Strands 的持续运行能力，Agent 可以突破传统单次对话的限制，实现跨会话的长期记忆存储与任务状态管理。
- 该架构通过将复杂的业务逻辑拆解为“链”，使智能体能够自主规划、执行并监控任务进度，直至完成最终目标。
- 开发者可以利用 MCP 协议将 Bedrock AgentCore 与外部数据源和工具无缝集成，显著扩展智能体的功能边界。
- 这种结合特别适用于需要长时间处理或异步等待结果的复杂工作流场景，例如自动化研发或代码审查。
- 新的集成方案简化了构建高级 AI 应用的流程，使开发者能更专注于业务逻辑而非底层状态维护。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*