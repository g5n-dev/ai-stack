---
title: "构建基于Amazon Bedrock AgentCore的长运行MCP服务器"
date: 2026-02-18T00:15:54+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长连接", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 构建能够长时间运行的 MCP 服务器的综合方法。 主要内容包括以下三个关键策略： 1. **引入上下文消息策略**：通过该策略在服务器和客户端之间维持扩展操作期间的持续通信，确保连接不中断。 2. **开发异步任务管"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 构建基于Amazon Bedrock AgentCore的长运行MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供了一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，用于在长时间运行的操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的过程，而不会阻塞其他操作。最后，我们将演示如何将 Amazon Bedrock AgentCore 和 Strands Agents 与这些策略相结合，构建可投入生产的 AI 代理，使其能够可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是当前技术落地的一大难点，尤其是在需要保持状态稳定且不阻塞主流程的场景下。本文将详细介绍一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的解决方案，重点涵盖上下文消息策略与异步任务管理框架。通过阅读，您将掌握如何构建高可用的生产级代理系统，使其能够可靠地执行复杂且耗时的操作。

---
## 摘要

本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 构建能够长时间运行的 MCP 服务器的综合方法。

主要内容包括以下三个关键策略：

1.  **引入上下文消息策略**：通过该策略在服务器和客户端之间维持扩展操作期间的持续通信，确保连接不中断。
2.  **开发异步任务管理框架**：构建一个允许 AI 代理启动长时间运行流程的框架，同时确保这些繁重任务不会阻塞其他操作的执行。
3.  **整合 Bedrock AgentCore 与 Strands Agents**：文章最后演示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，从而打造出能够可靠、高效地处理复杂且耗时任务的生产级 AI 代理。

---
## 评论

**文章核心架构与机制**

本文提出了一种基于 Amazon Bedrock AgentCore 的长期运行 MCP 服务器架构，旨在解决 LLM Agent 在处理长周期任务时的会话超时与状态保持问题。其核心手段是构建“上下文消息策略”与“异步任务管理框架”，将 Agent 的决策逻辑与耗时任务的实际执行进行解耦。

**深度技术评价**

**1. 架构解耦：从同步阻塞到异步编排**
*   **机制分析**：文章提出的异步任务管理框架，本质上是将 Agent 的“规划/思考”阶段与工具的“执行”阶段分离。传统 Agent 模式通常在单次请求链路中完成工具调用，一旦遇到数据处理或长等待等耗时操作，极易受限于 HTTP 超时或上下文窗口限制导致会话中断。
*   **架构演进**：通过引入异步框架，Agent 能够立即返回中间状态，由后台进程接手执行。这种设计实际上将 AI Agent 从单一的“对话接口”转变为“任务调度器”，使其具备了处理复杂工作流的能力。

**2. 状态连续性：突破无状态协议限制**
*   **协议适配**：MCP 协议本身倾向于无状态或短连接。文章提出的“Context Message Strategy”实际上是在客户端与服务器之间建立了一种状态快照传递机制。
*   **适用场景**：对于 RPA（机器人流程自动化）或金融分析等需要数小时甚至数天执行周期的企业级应用，该策略确保了任务完成后，LLM 仍能基于历史上下文处理结果，避免了任务状态丢失。

**3. 云平台集成的工程化考量**
*   **平台依赖**：利用 Bedrock 的托管服务能力维护会话线索，降低了底层基础设施的维护成本。
*   **落地意义**：该参考架构主要解决了从原型代码向生产级服务迁移过程中的工程化难题，特别是针对长时间运行任务的稳定性保障。

**局限性与边界条件**

**1. 成本与延迟的权衡**
*   **过度设计风险**：对于简单的、毫秒级工具调用（如查询天气、简单的数据库读取），引入复杂的异步框架和上下文策略属于过度设计。这不仅增加了系统延迟，还因多次往返传递上下文而显著增加了 Token 消耗。
*   **适用边界**：该架构主要适用于端到端延迟较大（如 > 10秒）或任务执行时间高度不确定的场景。

**2. 分布式状态的一致性挑战**
*   **数据一致性**：异步任务架构面临“最终一致性”挑战。若异步任务执行成功但通知消息丢失，或用户在执行期间取消会话，系统需具备完善的错误处理和补偿机制。
*   **事务要求**：在强一致性要求的金融交易场景中，单纯的异步回调可能不足，需引入 Saga 模式或幂等性校验以确保数据准确。

**3. 供应商锁定风险**
*   **迁移成本**：虽然 MCP 是开源协议，但 Bedrock AgentCore 属于 AWS 专有特性。深度绑定该架构会导致未来迁移至其他云平台（如 Azure 或 GCP）时，重写底层编排逻辑的成本较高。

**验证方式与指标**

**1. 长时任务存活率测试**
*   **测试方法**：启动耗时 30 分钟以上的模拟任务（如数据处理），期间断开客户端连接，任务完成后重新连接查询。
*   **预期指标**：Agent 应准确返回结果，无超时错误，且状态保持一致。

**2. Token 消耗基准测试**
*   **测试方法**：对比“同步直接调用”与“异步 Strand 模式”在完成相同逻辑时的总 Token 数量。
*   **预期指标**：异步模式的额外 Token 开销应处于可控范围（例如不超过同步模式的 120%），以确保架构的经济性。

**3. 并发压力与状态测试**
*   **测试方法**：模拟高并发 Agent 同时启动长时任务，观察系统的吞吐量及消息队列积压情况。
*   **观察重点**：监控是否存在任务丢失、上下文错乱或状态不一致的现象。

**实施建议**

1.  **按需采用**：仅对确定的 I/O 密集型或 CPU 密集型长任务使用此架构，简单 CRUD 操作宜保持同步调用以降低系统复杂度。
2.  **幂等性设计**：必须设计幂等性接口，防止因网络重试或异步回调重复导致的业务逻辑错误。
3.  **监控机制**：建立针对异步任务生命周期的监控体系，以便及时发现并处理“僵尸任务”或状态悬挂问题。

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该技术方案的深度分析。由于原文完整内容未完全给出，本分析将基于标题和摘要中透露的关键技术信号（MCP协议、Bedrock AgentCore、长时运行任务、异步任务管理、Strands集成）进行逻辑推演和技术拆解。

---

# 深度分析：基于 Amazon Bedrock AgentCore 与 Strands 构建长时运行 MCP 服务器

## 1. 核心观点深度解读

### 主要观点
文章的核心观点是：**为了解决当前 AI Agent 在处理复杂、长周期任务时的交互中断和状态管理难题，应当采用一种结合了“上下文消息策略”与“异步任务管理框架”的混合架构。** 具体而言，通过在 Amazon Bedrock 的 AgentCore 上集成 Strands Agents 概念，利用 Model Context Protocol (MCP) 构建能够维持长期会话状态的服务器。

### 核心思想
作者试图传达的思想是**“交互模式的解耦”**。传统的 LLM 交互是同步的（提问-回答），而复杂的业务流程往往是异步的（提交任务-等待-处理-返回结果）。作者主张通过技术手段，将 AI 的即时对话能力与后端的长时任务处理能力剥离，通过 MCP 协议作为粘合层，使 AI 能够像“项目经理”一样持续跟踪任务进度，而不是在任务执行期间“挂起”或产生超时幻觉。

### 创新性与深度
该观点的创新性在于将**Strands（通常指代具有连续性、记忆链的智能体架构）**与 **MCP（新兴的 AI 上下文连接标准）** 结合。深度体现在对“状态”的处理：不仅关注任务结果的返回，更关注任务执行过程中的上下文连续性，解决了 Serverless 或短连接架构下难以维持长时状态的痛点。

### 重要性
随着 AI 从“聊天机器人”向“Agent（智能体）”演进，能够处理如“代码生成与部署”、“数据分析报告生成”等动辄数分钟甚至数小时的任务成为刚需。此架构直接解决了 Agent 无法处理长时工作流（Long-running Workflows）的致命短板，是 AI 落地企业级应用的关键基础设施。

## 2. 关键技术要点

### 涉及的关键技术概念
1.  **MCP (Model Context Protocol)**: Anthropic 推出的开放协议，用于连接 AI 应用与数据源。在此处，它作为 Agent 与 Bedrock 之间的标准化通信层。
2.  **Amazon Bedrock AgentCore**: Bedrock 的底层编排引擎，负责 Agent 的路由、记忆和工具调用。
3.  **Strands Agents**: 指代具备“链式思考”或“连续记忆”能力的 Agent 架构，能够在长时间跨度内保持目标一致性。
4.  **Context Message Strategy (上下文消息策略)**: 一种在断开连接或长时等待期间，维持或传递对话上下文的技术。

### 技术原理和实现方式
*   **异步任务管理框架**:
    *   **原理**: 当 Agent 调用 MCP Server 执行长时任务（如视频渲染）时，Server 不保持连接阻塞等待，而是立即返回一个 `Task ID` 或 `Pending` 状态。
    *   **实现**: 后端启动独立进程或线程处理任务。Agent 进入“轮询”或“Webhook 回调”模式，定期查询任务状态，直到任务完成并获取结果。
*   **上下文消息策略**:
    *   **原理**: 利用 Bedrock 的 Session State 或外部存储（如 DynamoDB/Redis），将任务的中间状态或关键检查点封装为 Context Messages。
    *   **实现**: 当用户再次询问或 Agent 恢复连接时，系统自动加载之前的 Context Messages，使 LLM “记得”之前提交的任务及其当前进度。

### 技术难点与解决方案
*   **难点**: LLM 的 Token 限制与超时机制。长时任务可能导致上下文溢出或 API 调用超时。
*   **方案**: 摘要机制。在任务执行过程中，不将所有日志喂给 LLM，而是生成阶段性摘要存入上下文；利用 MCP 的资源引用能力，只传递关键状态变更。
*   **难点**: 并发与状态一致性。
*   **方案**: 使用分布式锁和状态机管理任务生命周期。

### 技术创新点分析
将 **MCP Server** 的轻量级连接特性与 **Bedrock AgentCore** 的强编排能力结合，并引入 **Strands** 的连续性理念，实际上是在构建一个**“有记忆的分布式任务调度系统”**，而非简单的问答系统。

## 3. 实际应用价值

### 对实际工作的指导意义
该架构为企业构建“AI 员工”提供了蓝图。它指导开发者不要试图在一个 LLM Prompt 中完成所有工作，而是设计异步的工具链，让 LLM 充当大脑，MCP Server 充当手脚，Bedrock 充当小脑。

### 适用场景
1.  **DevOps 与 CI/CD**: Agent 修改代码 -> 触发构建 -> 等待测试 -> 返回报告。耗时可能 10-30 分钟。
2.  **复杂数据分析**: Agent 查询数据库 -> 清洗数据 -> 训练模型 -> 生成图表。
3.  **企业级 RPA**: 跨系统审批流程，涉及人工确认和长时间等待。
4.  **内容生成**: 长视频渲染、大型文档翻译。

### 需要注意的问题
*   **成本**: 频繁的轮询或长上下文维护会增加 Token 消耗和 API 调用成本。
*   **安全性**: 异步任务中的凭证管理和权限传递（如 IAM Role 传递）需要严格设计。

### 实施建议
采用“状态机”模式设计 MCP Server 的工具接口。明确区分 `start_task`（返回 ID）、`check_status`（返回进度）和 `get_result`（返回数据）三个阶段。

## 4. 行业影响分析

### 对行业的启示
这标志着 AI Agent 开发从“单次对话”向“流程自动化”的范式转移。行业标准将不再满足于简单的 RAG（检索增强生成），而是追求 **Agentic Workflow（智能体工作流）** 的可靠性。

### 可能带来的变革
*   **MCP 协议的普及**: 作为连接 AI 和后端服务的标准，MCP 可能成为 API 之后的下一代接口标准。
*   **云原生 AI 的深化**: Bedrock 等托管服务将进一步垄断底层编排，开发者的价值向业务逻辑和 MCP 工具开发迁移。

### 发展趋势
未来会出现更多“长时运行中间件”，专门用于管理 AI Agent 的生命周期、记忆持久化和异步任务队列。

## 5. 延伸思考

### 拓展方向
*   **人机协同**: 在长时任务中，如何设计“断点”让人工介入确认，然后再由 Agent 继续执行？
*   **多 Agent 协作**: 一个 Strands Agent 负责长时任务调度，其他 Specialist Agent 负责具体子任务。

### 需进一步研究的问题
*   如何在长时运行中处理“幻觉漂移”？（即随着任务进行，Agent 是否会忘记最初的目标？）
*   异步任务失败后的“回滚”或“自我修复”机制如何设计？

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有工具**: 检查你现有的 API 是否是同步且耗时的。如果是，将其改造为异步模式。
2.  **引入状态存储**: 选择一个键值存储（如 Redis）来保存 Bedrock Agent 的 Session State 和任务 ID。
3.  **开发 MCP Server**: 按照 Anthropic 的 MCP 规范，封装你的异步 API。

### 行动建议
*   **第一步**: 搭建一个简单的 Bedrock Agent，配置一个 MCP Server。
*   **第二步**: 实现一个模拟的长时任务（如 `sleep 60s`），观察 Agent 的行为。
*   **第三步**: 引入 Context Message 策略，确保 Agent 在等待期间能正确响应用户的“进度查询”。

### 知识补充
需要深入学习 **Amazon Bedrock Agent Framework** 的 API 定义，以及 **MCP (Model Context Protocol)** 的 SDK 使用。

## 7. 案例分析

### 成功案例（假设性构建）
**场景**: 某金融公司使用该架构构建“财报分析 Agent”。
*   **流程**: 用户上传 PDF -> Agent 提取数据 -> MCP Server 调用 Python 脚本进行复杂计算（耗时 5 分钟） -> Server 通过 WebSocket 更新进度 -> Agent 汇总结果。
*   **成功点**: 用户不需要盯着“正在输入”的界面焦虑等待，Agent 会主动告知“正在计算波动率，请稍候”，并在计算完成后通知用户。

### 失败反思
*   **场景**: 未使用异步策略，直接让 LLM 等待 API 返回。
*   **后果**: API 超时，LLM 报错 "Tool use error"，或者产生幻觉捏造数据。

## 8. 哲学与逻辑：论证地图

### 中心命题
**为了构建具备企业级处理能力的 AI Agent，必须在 Bedrock AgentCore 上采用基于 MCP 的异步任务架构与上下文连续性策略。**

### 支撑理由
1.  **时效性不匹配**: LLM 的响应是秒级的，而业务任务（如数据处理、部署）是分钟级的。同步调用会导致超时或资源浪费。
    *   *依据*: 计算机科学中的异步 I/O 理论及 HTTP 超时限制。
2.  **上下文连续性**: 复杂任务需要多步推理，中断后必须恢复状态，否则任务无法闭环。
    *   *依据*: 认知科学中的工作记忆理论，AI Agent 的“心流”体验需求。
3.  **标准化互操作性**: MCP 提供了统一的连接层，降低了 Bedrock 与自定义工具集成的复杂度。
    *   *依据*: API 经济的发展历史，标准化协议带来的效率提升。

### 反例与边界条件
1.  **反例**: 对于简单的、毫秒级的信息查询（如“查天气”、“查库存”），引入异步框架和 Strands 集成属于过度设计，增加了延迟和系统复杂度。
2.  **边界条件**: 如果任务必须在极短时间内完成且状态极小（如简单的数学计算），同步调用更高效。

### 命题性质分析
*   **事实**: Bedrock AgentCore 支持工具调用；MCP 是连接协议；长时任务存在超时风险。
*   **价值判断**: “应该”采用异步架构，因为这能提供更好的用户体验和系统稳定性。
*   **可检验预测**: 采用该架构的系统，在处理长时任务时的超时错误率将显著低于同步架构，且用户满意度更高。

### 立场与验证
**立场**: 支持该架构作为企业级复杂 Agent 的标准参考架构。
**验证方式**:
*   **指标**: 任务成功率、平均端到端延迟、Token 消耗量。
*   **实验**: 对比同步架构与异步架构在处理 5 分钟以上任务时的超时率和上下文丢失率。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化会话状态管理与持久化

**说明**: 长时间运行的 MCP 服务器需要维护跨请求的上下文状态。在 AgentCore 环境中，必须确保会话状态不仅存储在内存中，还要持久化到外部存储（如 DynamoDB 或 S3），以便在服务器重启或扩展时恢复状态。

**实施步骤**:
1. 配置状态存储后端，选择低延迟的数据库服务。
2. 定义清晰的状态生命周期策略，包括过期时间和清理机制。
3. 实现状态序列化与反序列化逻辑，确保对象版本兼容性。

**注意事项**: 避免在状态中存储敏感信息，应对敏感字段进行加密。同时，要注意状态对象的大小，防止超过存储限制或影响网络传输性能。

---

### 实践 2：实施严格的超时与重试机制

**说明**: Strands Agents 调用 MCP 服务器时，可能会因为网络波动或下游服务响应慢而导致挂起。为了防止资源耗尽和阻塞 Agent 的主循环，必须为所有 MCP 工具调用配置合理的超时和指数退避重试策略。

**实施步骤**:
1. 根据工具的预期执行时间，设置客户端和服务器端的超时阈值。
2. 实现指数退避算法处理可重试的错误（如 5xx 错误或限流）。
3. 记录超时和重试日志，用于后续监控和性能调优。

**注意事项**: 区分临时性错误和永久性错误。对于业务逻辑错误（如参数验证失败），不应进行重试，而应直接返回错误信息给 Agent。

---

### 实践 3：构建异步非阻塞架构

**说明**: 长时间运行的任务（如数据处理、文件生成）不应阻塞 MCP 服务器的响应线程。最佳实践是采用异步模式，立即返回一个“任务已接收”的确认或任务 ID，并通过轮询或 Webhook 的方式通知 Agent 最终结果。

**实施步骤**:
1. 使用支持异步的框架（如 FastAPI 或 asyncio）构建服务器。
2. 将耗时任务推送到后台队列（如 Amazon SQS）或由 Step Functions 处理。
3. 设计状态查询接口，供 Strands Agents 检查任务进度。

**注意事项**: 确保异步任务的幂等性，防止因网络重试导致任务重复执行。同时，需要处理任务失败后的补偿逻辑。

---

### 实践 4：标准化工具定义与输入验证

**说明**: 为了让 Strands Agents 能够准确调用 MCP 工具，必须在 Schema 定义中提供清晰、准确的描述和参数结构。模糊的定义会导致 Agent 生成无效的调用请求。

**实施步骤**:
1. 使用 JSON Schema 严格定义工具的输入参数。
2. 在工具描述中详细说明参数的用途、格式和限制。
3. 在代码入口处实施数据验证，拒绝不符合 Schema 的请求。

**注意事项**: 保持 Schema 的向后兼容性。如果必须进行破坏性更改，应考虑版本控制策略（例如 `/v2/tool`）。

---

### 实践 5：利用结构化日志与可观测性工具

**说明**: 在 Bedrock AgentCore 环境中，调试长连接问题非常困难。必须实施全面的日志记录和指标监控，以便追踪请求链路、性能瓶颈和错误根因。

**实施步骤**:
1. 集成 Amazon CloudWatch 用于日志聚合和指标监控。
2. 在日志中包含 `Trace ID`，以便与 AWS X-Ray 集成进行分布式追踪。
3. 记录关键业务指标，如请求延迟、错误率和工具调用频率。

**注意事项**: 避免记录敏感的 PII（个人身份信息）数据。确保日志级别在生产环境中配置得当（如 INFO 或 ERROR），防止日志量过大产生额外费用。

---

### 实践 6：实施细粒度的安全控制与最小权限原则

**说明**: MCP 服务器通常作为中间层连接 Agent 和后端资源。必须严格验证调用方的身份，并为服务器角色分配最小的 IAM 权限，以防止安全漏洞。

**实施步骤**:
1. 配置 Bedrock AgentCore 的身份验证机制，确保只有授权的 Agent 可以访问 MCP 端点。
2. 为 MCP 服务器使用的 IAM Role 仅授予特定任务所需的权限（如特定的 S3 bucket 访问权）。
3. 定期审计 IAM 策略和访问日志。

**注意事项**: 不要在代码中硬编码 API 密钥或凭证。利用 AWS Secrets Manager 或 IAM Roles for Tasks 来动态获取权限。

---

### 实践 7：设计幂等性接口

**说明**: 网络不稳定可能导致 Agent 发送重复的请求。为了确保数据一致性和避免重复操作，所有 MCP 工具接口应设计为幂等的，即多次调用相同的参数产生的结果与一次调用相同。

**实施步骤**:
1. 对于写操作，要求客户端生成唯一的 `ClientRequestID` 或 `IdempotencyKey`。
2. 服务器端在处理前检查该 Key 是否已被处理，

---
## 学习要点

- Amazon Bedrock AgentCore 现支持集成 Strands Agents，允许开发者构建能够维护长期对话状态和记忆的持久化 MCP 服务器。
- 通过利用 Strands Agents 的状态管理能力，开发者可以创建能够跨多个会话记住上下文和用户偏好的智能代理。
- 此集成解决了传统无状态模型连接器的局限性，使 AI 应用能够执行更复杂、多步骤的长期任务。
- 开发者现在可以在 Bedrock 的托管基础设施上运行这些长期运行的代理，从而无需自行管理底层服务器资源。
- 该架构利用 MCP (Model Context Protocol) 实现了代理与外部数据源及工具之间的标准化通信。
- 这种组合为构建需要持续交互的高级生产级 AI 应用（如个人助理或复杂工作流自动化）提供了可扩展的解决方案。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*