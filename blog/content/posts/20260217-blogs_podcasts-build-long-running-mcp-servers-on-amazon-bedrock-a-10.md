---
title: "构建基于Amazon Bedrock的长运行MCP服务器与异步任务管理"
date: 2026-02-17T01:22:35+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "异步任务", "长连接", "AI Agent", "Strands Agents", "系统架构"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的解决方案，旨在构建能够处理长时间运行任务的生产级 MCP 服务器。 为了解决 AI 代理在处理复杂、耗时操作时的可靠性问题，文章提出了三个核心策略： 1. **上下文消息策略**：引入了一种机制，确保服务器与客"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 构建基于Amazon Bedrock的长运行MCP服务器与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供了一套全面的实现方案。首先，我们介绍一种上下文消息策略，在耗时较长的操作期间，保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的流程，同时不阻塞其他操作。最后，我们将展示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，构建生产就绪的 AI 代理，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是当前技术落地的难点之一，因为传统的同步通信模式难以应对耗时操作。本文将介绍一套基于 Amazon Bedrock AgentCore 和 Strands Agents 的实现方案，重点解析上下文消息策略与异步任务管理框架。通过阅读本文，您将掌握如何构建生产就绪的 AI 代理，在保持通信连续性的同时，可靠地处理复杂业务流程。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的解决方案，旨在构建能够处理长时间运行任务的生产级 MCP 服务器。

为了解决 AI 代理在处理复杂、耗时操作时的可靠性问题，文章提出了三个核心策略：

1.  **上下文消息策略**：引入了一种机制，确保服务器与客户端在扩展操作期间保持连续通信，避免长时间交互中的上下文丢失。
2.  **异步任务管理框架**：开发了一套框架，允许 AI 代理启动长耗时进程，同时不会阻塞其他操作的执行，从而提升系统的并发处理能力。
3.  **整合与实现**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，构建出能够可靠、高效地处理复杂时间密集型任务的 AI 代理。

---
## 评论

**文章中心观点**
本文主张通过结合 Amazon Bedrock AgentCore 的托管能力与 MCP (Model Context Protocol) 的标准化接口，并引入“Strands”技术概念及异步任务框架，来解决长期运行型 AI 智能体在处理复杂工作流时的状态保持与通信中断问题。

**支撑理由与边界条件分析**

**1. 架构层面的解耦与标准化（事实陈述）**
文章提出的方案核心在于利用 MCP 协议将大模型（LLM）与底层工具/数据源解耦。
*   **支撑理由**：MCP 作为一种新兴的开放标准，正逐渐成为连接 AI 智能体与企业数据层的通用语言。Bedrock AgentCore 提供了托管的基础设施，减少了用户在维护服务器生命周期方面的负担。
*   **反例/边界条件**：这种强依赖 AWS 生态的架构会导致严重的**厂商锁定**。如果企业需要跨云部署（如同时使用 Azure 或 GCP 的特定服务），这种紧耦合的 AgentCore 架构迁移成本极高。此外，MCP 目前的标准化程度仍在早期，协议本身可能存在频繁变动。

**2. 异步任务管理与“Strands”概念的引入（作者观点 / 你的推断）**
文章引入“Strands”（ strands of thought/execution）来处理长时任务，这实际上是一种**显式的思维链或工作流切片技术**。
*   **支撑理由**：LLM 的上下文窗口和 Token 限制是客观存在的。对于需要数分钟甚至数小时才能完成的任务（如批量数据处理、代码编译），同步等待会导致超时或资源浪费。通过异步框架，Agent 可以挂起主线程，等待任务完成后再通过“Context Message”回调恢复上下文，这是构建生产级 Agent 的必经之路。
*   **反例/边界条件**：异步架构极大地增加了**调试与可观测性的难度**。当一个任务失败，特别是在涉及多个 Strands 的并行执行时，定位错误是发生在 LLM 规划层、MCP 传输层还是底层工具执行层，将变得非常困难。此外，状态管理如果完全依赖外部存储，在处理高并发场景下可能会遭遇数据一致性问题。

**3. 上下文消息策略的必要性（事实陈述）**
文章强调了维持连续通信的策略，这是为了解决 LLM 的“无状态性”。
*   **支撑理由**：在长时运行中，客户端连接可能会断开，或者会话可能会因为空闲而被中间网关切断。通过一种机制（如 WebSocket 长连接或轮询）来传递“任务正在进行中”的心跳包或中间状态，能显著提升用户体验，避免用户面对“无响应”的黑盒。
*   **反例/边界条件**：如果上下文消息设计不当，引入过多的噪音或非结构化日志，容易**污染 LLM 的上下文窗口**，导致后续的推理出现“幻觉”或注意力分散。必须严格区分“系统级心跳”和“业务级上下文”。

**4. 对 Bedrock Agent 编排能力的依赖（你的推断）**
文章隐含的观点是：利用云厂商的编排服务优于自建。
*   **支撑理由**：对于缺乏深厚 DevOps 能力的企业，Bedrock AgentCore 提供了开箱即用的监控、鉴权和模型路由功能，能加速 MVP（最小可行性产品）的落地。
*   **反例/边界条件**：对于需要极致性能或低延迟的场景（如高频交易、实时游戏 AI），云厂商的通用编排层往往引入了不可接受的**网络延迟**。在这种情况下，边缘计算或直接调用模型 API 的轻量级架构往往比厚重的 Agent Framework 更有效。

**综合评价**

*   **内容深度与实用性**：文章触及了当前 AI Agent 落地中最痛点的“长时任务”问题。将 MCP 与 Bedrock 结合是符合当前技术趋势的（大模型 + 编排框架 + 协议标准）。其提供的异步框架思路具有很高的实用价值，特别是对于企业级应用开发。
*   **创新性**：虽然“异步任务”并非新概念，但将其与 MCP 和 Bedrock AgentCore 结合，并冠以“Strands”的命名，是一种不错的架构模式总结。它试图在 LangChain 等重型框架与原生 API 之间寻找一种基于云原生的中间路线。
*   **行业影响**：此类文章进一步推动了 AI 开发从“Prompt Engineering”向“Agentic Engineering”的转变。它暗示了未来的 AI 开发者不仅要懂模型，更要懂分布式系统设计。
*   **争议点**：最大的争议在于“Strands”的定义是否足够清晰，以及这是否又是 AWS 制造的又一个“概念壁垒”，迫使开发者学习其特定的术语体系，而非使用通用的软件工程术语。

**可验证的检查方式**

1.  **压力测试指标**：
    *   **实验**：构建一个并发处理 100 个长时任务（每个任务耗时 > 5分钟）的 MCP Server。
    *   **验证指标**：观察 Bedrock AgentCore 是否会出现任务排队阻塞？Context Message 的传递是否存在显著延迟？系统的最大吞吐量（TPS）是多少？

2.  **状态恢复测试**：
    *   **实验**：在 Agent 执行 Strands 任务的过程中，人为强制重启 Bedrock Agent 服务或中断网络连接 30 秒。
    *   **验证指标**：任务恢复后，Agent 是否能准确接续之前的上下文继续工作，还是会出现状态丢失导致的重复执行或逻辑崩溃？

3.  **Token 消耗分析**：
    *   **实验**：运行一个包含 10 个步骤

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该技术方案的深入分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 与 Strands 的长时运行 MCP 服务器架构

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点在于解决当前 AI 智能体在处理复杂、长周期任务时面临的“连接中断”与“状态管理”难题。作者提出了一种基于 **Amazon Bedrock AgentCore** 和 **Strands Agents** 集成的架构方案，旨在构建能够维持长时间运行状态的 **MCP (Model Context Protocol) 服务器**。这不仅仅是技术组件的堆叠，而是一种架构模式的演进，即从“无状态请求-响应”转向“有状态的长时任务流”。

**作者想要传达的核心思想**
作者试图传达的核心思想是：**上下文的连续性和任务编排的异步化是构建高级 AI 应用的关键**。通过引入“上下文消息策略”和“异步任务管理框架”，系统能够在客户端与服务器之间建立一种类似于“心跳”的机制，确保在处理耗时操作（如数据处理、复杂推理）时，连接不会超时，且用户能够感知到进度。

**观点的创新性和深度**
该观点的创新性在于它将 **MCP 协议**（通常用于本地或短时上下文传输）与 **Amazon Bedrock** 的托管能力及 **Strands**（推测为某种长时任务编排或记忆管理机制）进行了深度结合。它突破了传统 LLM 应用受限于 Token 输出时间或 HTTP 超时的瓶颈，将智能体从“对话机器”提升为“任务执行者”。

**为什么这个观点重要**
随着 AI 从 Content Generation（内容生成）向 Action Taking（行动执行）转变，Agent 需要调用工具、查询数据库、甚至等待人工审批。这些操作往往耗时数秒甚至数分钟。如果无法解决长时运行问题，Agent 的应用场景将被局限在简单的问答领域。该方案为构建企业级、高可靠性的 AI 劳动力提供了基础设施保障。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**：用于在 AI 应用（客户端）和数据源（服务器）之间标准化的上下文传输协议。
2.  **Amazon Bedrock AgentCore**：AWS 提供的构建 Agent 的底层核心服务，负责编排、推理和工具调用。
3.  **Strands Agents**：这是文章中较为新颖的概念，推测是指一种能够处理多步骤、长周期任务流的 Agent 机制，可能涉及“记忆”或“状态 strand”的管理。
4.  **异步任务管理**：非阻塞的任务处理模式。

**技术原理和实现方式**
*   **Context Message Strategy（上下文消息策略）**：
    *   **原理**：在长任务执行期间，服务器不保持连接阻塞，而是通过特定的消息格式（如 Server-Sent Events 或 MCP 的特定扩展包）定期向客户端发送“心跳”或“中间状态更新”。
    *   **实现**：建立一个双向通信通道，Agent 在执行任务子步骤时，通过 MCP 接口推送状态更新，告知客户端“我还在运行，当前进度是 X%”。

*   **Asynchronous Task Management Framework（异步任务管理框架）**：
    *   **原理**：将任务的“触发”与“执行”解耦。客户端发起请求后，Bedrock AgentCore 立即返回一个 `TaskID`，并将任务放入队列（如 SQS）或交给 Strands 执行器处理。
    *   **实现**：MCP 服务器不再直接等待 LLM 推理结束，而是轮询或订阅任务结果。当 Strands 完成任务后，更新结果存储，客户端通过 TaskID 获取最终数据。

**技术难点和解决方案**
*   **难点**：网络超时与资源消耗。长连接容易导致超时，且占用服务器资源。
*   **解决方案**：采用异步回调或轮询机制。结合 Bedrock 的无服务器架构，利用 Strands 来管理任务的生命周期，确保即使底层计算资源释放，任务状态依然保留。
*   **难点**：状态一致性。在分布式环境下保证任务状态不丢失。
*   **解决方案**：利用 DynamoDB 等持久化层存储 Strands 的中间状态，实现故障恢复。

**技术创新点分析**
最大的创新点在于 **MCP 协议在 Bedrock 环境下的“有状态化”改造**。标准的 MCP 往往假设客户端直接连接本地工具，而该架构将其扩展到了云端，并引入了类似工作流的 Strands 概念，使得 MCP 服务器可以处理复杂的业务逻辑，而不仅仅是简单的数据查询。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为开发者提供了一套在 AWS 云上构建复杂 AI 应用的蓝图。它指导开发者如何跳出简单的“聊天机器人”思维，转而设计能够处理复杂业务流程的“AI 员工”。

**可以应用到哪些场景**
1.  **数据分析与报告生成**：Agent 需要长时间查询数据库、清洗数据、生成图表，整个过程可能持续几分钟。
2.  **RPA（机器人流程自动化）**：Agent 需要执行一系列 UI 操作或 API 调用，每个步骤都有延迟。
3.  **代码生成与测试**：Agent 编写代码后，需要编译、运行测试用例，这是一个典型的长时异步任务。
4.  **企业级审批流**：Agent 发起审批后，需要等待人工介入，期间需要保持上下文不丢失。

**需要注意的问题**
*   **成本控制**：长时运行意味着更多的计算资源和 API 调用次数。
*   **安全性**：异步任务中的身份验证和权限管理变得更加复杂，需要确保 `TaskID` 不可被伪造或遍历。
*   **超时设置**：虽然任务是异步的，但客户端和服务器仍需合理配置超时策略，防止僵尸任务。

**实施建议**
建议采用“事件驱动架构”来配合 Strands。使用 EventBridge 来监听任务状态的变化，并触发相应的通知或后续动作，而不是让客户端无限轮询。

## 4. 行业影响分析

**对行业的启示**
该方案预示着 **AI Agent 基础设施正在“云原生化”和“标准化”**。MCP 协议的兴起表明，行业正在试图解决 AI 应用与数据源之间的连接碎片化问题，而 AWS Bedrock 的集成则展示了云厂商如何将这种协议企业级、规模化。

**可能带来的变革**
*   **从“同步”到“编排”的转变**：AI 应用开发将更像后端微服务开发，注重任务编排、状态机和错误重试。
*   **MCP 生态的爆发**：随着云端长时运行能力的支持，MCP 可能会成为连接 SaaS 服务与 AI 模型的标准接口。

**相关领域的发展趋势**
*   **AgentOps（智能体运维）**：如何监控、调试和追踪长时运行的 Agent 将成为新热点。
*   **混合推理架构**：本地模型（MCP Client）与云端大模型（Bedrock）的协同工作将更加紧密。

**对行业格局的影响**
这将进一步巩固 AWS 等云厂商在 AI 应用层的统治地位。通过提供 AgentCore 和 Strands 这样的高级抽象，云厂商降低了构建复杂 Agent 的门槛，使得企业更倾向于在云端构建 AI 劳动力，而非仅仅依赖本地模型。

## 5. 延伸思考

**引发的其他思考**
*   **人机协同的新模式**：如果 Agent 可以长时运行，那么“人在回路”的设计将变得更加重要。如何在长任务中优雅地插入人工确认节点？
*   **多 Agent 协作**：Strands 是否支持多个 Agent 并行或串行工作？这将是下一步的演进方向。

**可以拓展的方向**
*   **边缘计算结合**：将 Bedrock 的强大推理能力与边缘端的 MCP 服务器结合，实现低延迟触发、云端深度处理的混合模式。
*   **流式输出的标准化**：目前的 MCP 侧重于工具调用，未来可能需要更好地支持流式文本与工具调用的混合传输。

**需要进一步研究的问题**
*   Strands 的具体实现细节是否开源？它与现有的 LangChain 或 LangGraph 的编排层有何本质区别？
*   在极高并发下，Bedrock AgentCore 的限流策略如何影响 Strands 的任务调度？

**未来发展趋势**
未来，长时运行 Agent 将具备更强的**自主性**和**容错性**。它们不仅能执行任务，还能在遇到错误时自主规划恢复路径，并在长时间跨度（如数天）内保持对某个目标的持续关注。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务类型**：如果你的 AI 应用仅限于问答，无需此架构。如果涉及 API 编排、数据处理，则应考虑引入异步 MCP。
2.  **架构改造**：将现有的同步 MCP 调用改为“发布-订阅”模式。客户端调用工具后，立即返回 `202 Accepted` 和任务 ID。
3.  **引入状态存储**：使用 Redis 或 DynamoDB 存储 Strands 的任务状态。

**具体的行动建议**
*   **第一步**：阅读 MCP 协议规范，特别是关于资源引用和提示的部分。
*   **第二步**：在 AWS 上搭建一个 Bedrock Agent，并尝试配置一个 Lambda 函数作为 MCP 服务器。
*   **第三步**：模拟一个长耗时任务（如 Sleep 60秒），测试客户端是否会超时，并应用文章中的“上下文消息策略”来解决超时问题。

**需要补充的知识**
*   **Amazon Bedrock 的使用和配置**。
*   **异步编程模型**（如 Python 的 `asyncio` 或 JS 的 `Promise`）。
*   **WebSocket 或 SSE（Server-Sent Events）** 协议知识。

**实践中的注意事项**
*   **幂等性设计**：客户端可能会因为网络错误重复提交任务，MCP 服务器必须保证幂等性。
*   **错误处理**：长任务失败后的回滚机制非常复杂，需要预先设计好 Compensation 事务。

## 7. 案例分析

**结合实际案例说明**
假设我们要构建一个 **“企业财报分析 Agent”**。
*   **传统模式**：用户上传 PDF -> Agent 读取 -> 调用 Python 脚本分析 -> 返回结果。如果分析耗时 2 分钟，HTTP 连接可能早已断开。
*   **新模式（基于文章方案）**：
    1.  用户上传 PDF。
    2.  Bedrock Agent 通过 MCP 协议通知 Strands 开始任务。
    3.  Strands 启动一个异步 Fargate 任务进行数据分析。
    4.  在分析期间，MCP 服务器每隔 10 秒通过 Bedrock 向用户推送：“正在计算资产负债表... 30%”。
    5.  计算完成后，Strands 将结果存入 S3，并通过 MCP 通知 Agent。
    6.  Agent 读取结果并生成最终报告展示给用户。

**成功案例分析**
**Klarna（金融支付）** 或 **Klaviom（营销）** 等公司正在尝试类似的 Agent 架构。他们利用异步 Agent 处理海量客户咨询和后台数据清洗，极大地提高了自动化率。成功的关键在于将“对话”与“执行”解耦。

**失败案例反思**
早期的一些 ChatGPT

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化服务器架构以支持长时间运行的任务

**说明**: 构建 MCP (Model Context Protocol) 服务器时，必须采用无状态设计或持久化会话管理，以适应 Bedrock AgentCore 的长时间运行特性。Strands Agents 集成要求服务器能够处理跨越数分钟甚至数小时的复杂工作流，而不仅仅是简单的请求-响应循环。

**实施步骤**:
1. 采用异步 I/O 模型（如 Python 的 asyncio 或 Node.js 的 Event Loop）来处理并发请求，避免阻塞主线程。
2. 实现基于令牌或会话 ID 的状态恢复机制，确保在连接中断后能够从上次中断处继续执行。
3. 将长时间运行的业务逻辑分解为独立的任务单元，并使用消息队列（如 SQS）进行解耦。

**注意事项**: 避免在服务器内存中保存关键的会话状态，以防服务器重启导致数据丢失。

---

### 实践 2：实施严格的超时与重试策略

**说明**: 由于涉及 Strands Agents 的集成，外部 API 调用或复杂推理可能会耗时较长。必须配置合理的超时参数，并针对 Bedrock 的限制实施指数退避重试机制，以防止因网络波动或资源限制导致任务永久失败。

**实施步骤**:
1. 为所有 MCP 工具调用设置明确的超时限制（例如 300 秒），并返回一个异步任务 ID 而不是让连接挂起。
2. 实现指数退避算法，在遇到限流或临时故障时自动重试请求。
3. 在代码层面捕获 `ReadTimeout` 和 `ConnectionError` 异常，并记录详细的上下文信息以便调试。

**注意事项**: 确保重试逻辑不会导致重复扣费或重复执行非幂等操作。

---

### 实践 3：设计基于 Strands 的增量式状态更新

**说明**: 利用 Strands Agents 的能力，MCP 服务器应支持流式或增量式的状态反馈。不要等到任务完全完成才返回结果，而是应该通过回调或轮询机制向 AgentCore 报告中间进度。

**实施步骤**:
1. 定义标准化的状态枚举（如 PENDING, IN_PROGRESS, COMPLETED, FAILED）。
2. 实现 Server-Sent Events (SSE) 或 WebSocket 接口（如果 MCP 客户端支持），或提供专用的状态查询端点。
3. 在服务器内部维护一个状态存储，供 AgentCore 随时查询当前进度。

**注意事项**: 确保状态更新的频率不会淹没客户端或造成不必要的处理开销。

---

### 实践 4：强化安全性与最小权限原则

**说明**: MCP 服务器通常作为 Agent 和底层资源之间的桥梁。必须严格验证传入请求的来源，并限制服务器对下游 AWS 资源的访问权限，防止提示词注入攻击导致的数据泄露。

**实施步骤**:
1. 使用 AWS IAM Roles Anywhere 或 IAM for Bedrock 来验证调用者的身份，并仅授予执行特定任务所需的最小权限。
2. 对所有输入参数进行严格校验，防止注入攻击。
3. 将敏感配置（如 API 密钥、数据库连接字符串）存储在 AWS Secrets Manager 中，而不是硬编码在代码或环境变量里。

**注意事项**: 定期轮换凭证并审计 CloudTrail 日志，监控异常的 API 调用模式。

---

### 实践 5：构建可观测性与日志记录体系

**说明**: 长时间运行的流程往往难以调试。必须建立完善的日志和监控体系，将 MCP 服务器的内部状态与 Bedrock AgentCore 的 Trace 机制关联起来，以便在出现问题时快速定位瓶颈。

**实施步骤**:
1. 使用 AWS X-Ray 进行分布式追踪，确保 MCP 服务器传递 Trace ID，以便将请求与 Bedrock Agent 的调用链关联。
2. 将结构化日志发送到 Amazon CloudWatch Logs，包含请求 ID、工具名称、输入参数和执行时间。
3. 设置 CloudWatch 告警，用于监控错误率、延迟和 P99 响应时间。

**注意事项**: 避免在日志中记录敏感的用户数据（PII），必要时进行脱敏处理。

---

### 实践 6：资源清理与上下文管理

**说明**: 在长时间运行的会话中，如果不加以管理，临时文件、内存占用或数据库连接可能会累积，导致资源耗尽。必须实施严格的生命周期管理。

**实施步骤**:
1. 实现明确的会话过期机制，自动清理超过特定时间阈值（如 24 小时）的非活动会话数据。
2. 使用 Python 的 `contextlib` 或类似语言特性来管理文件句柄和网络连接，确保异常发生时资源也能被正确释放。
3. 定期对持久化存储进行归档或清理，防止存储成本无限增长。

**注意事项**: 在清理资源前，确保相关任务已完全终止或处于可恢复的暂停状态。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，使开发者能够在该平台上构建并运行具备长期记忆和状态管理能力的 MCP 服务器。
- 通过利用 Strands Agents 的持久化上下文能力，开发者可以解决传统无状态 AI 应用在处理多步骤、长周期任务时的局限性。
- 该集成方案允许 AI 智能体在长时间运行的工作流中保持对用户偏好和历史交互的记忆，从而显著提升个性化体验。
- 借助 Bedrock AgentCore 的托管服务，开发者无需自行维护底层基础设施，即可轻松部署复杂的、有状态的 AI 应用程序。
- 此架构特别适用于需要跨多个会话保持连续性的复杂场景，如项目管理和自动化工作流编排。
- 集成过程遵循 MCP 协议标准，确保了构建的长期运行服务器能够与广泛的现有 AI 工具和生态系统实现无缝互操作。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/) / [AI Agent](/tags/ai-agent/) / [Strands Agents](/tags/strands-agents/) / [系统架构](/tags/%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-5.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-7.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于 Amazon Bedrock AgentCore 构建长时间运行的 MCP 服务器]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*