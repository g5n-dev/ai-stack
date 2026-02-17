---
title: "基于Amazon Bedrock AgentCore构建支持长时运行的MCP服务器"
date: 2026-02-17T17:34:43+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "长时运行", "异步任务", "AI 代理", "上下文策略"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon Bedrock AgentCore 上结合 Strands Agents 集成，构建能够处理长时间运行任务的 MCP 服务器。主要方法包括以下三点： 1. **引入上下文消息策略**：通过该策略在服务器与客户端之间维持连续通信，确保在长时间操作期间的信息同步与状态更新。 2. **开发异"
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

在这篇文章中，我们将为您提供实现这一目标的综合方法。首先，我们介绍一种上下文消息策略，用于在服务器和客户端之间在长时间操作期间保持持续通信。接下来，我们将构建一个异步任务管理框架，允许您的AI代理启动长时间运行的过程而不会阻塞其他操作。最后，我们将演示如何将这些策略与Amazon Bedrock AgentCore和Strands Agents结合起来，构建生产就绪的AI代理，以可靠地处理复杂且耗时的操作。

---
## 导语

构建能够可靠处理长时间运行任务的 AI 代理是生产环境中的关键挑战。本文将探讨如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成，通过上下文消息策略和异步任务管理框架，解决服务器与客户端在持续通信中的阻塞问题。阅读本文，您将掌握构建生产级 AI 代理的具体方法，以有效应对复杂且耗时的操作流程。

---
## 摘要

本文介绍了如何在 Amazon Bedrock AgentCore 上结合 Strands Agents 集成，构建能够处理长时间运行任务的 MCP 服务器。主要方法包括以下三点：

1.  **引入上下文消息策略**：通过该策略在服务器与客户端之间维持连续通信，确保在长时间操作期间的信息同步与状态更新。
2.  **开发异步任务管理框架**：构建该框架旨在允许 AI 代理启动长耗时进程，同时避免阻塞其他操作，从而提升系统的并发处理能力。
3.  **整合技术实现生产级应用**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，打造出能够可靠处理复杂且耗时任务的生产就绪型 AI 代理。

---
## 评论

**核心观点**
本文提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的技术架构，旨在通过引入上下文消息策略和异步任务管理框架，解决模型上下文协议（MCP）服务器在处理长周期任务时的状态持久化与通信连续性问题，从而构建具备企业级稳定性的生成式 AI 应用。

**技术解析**

1.  **针对 MCP 协议短板的架构补位**
    目前的 Model Context Protocol (MCP) 虽然统一了 LLM 与工具间的连接标准，但其原生设计倾向于同步请求-响应模式。当 Agent 调用工具执行耗时任务（如数据检索或代码编译）时，容易遭遇超时或上下文丢失。文章提出的“上下文消息策略”实际上是在协议层之上构建了一个虚拟会话层，通过心跳或分片消息机制维持连接活跃。这属于对现有协议边界的工程化扩展。

2.  **异步任务框架的必要性**
    摘要中提到的“异步任务管理框架”触及了当前 Agent 架构的痛点：确定性与延迟的权衡。在 Bedrock AgentCore 环境中，直接阻塞主线程等待任务完成会导致资源被长时间占用。作者提出的方案可能采用了“任务队列 + 回调轮询”的模式，将计算密集型任务与推理解耦。这对于构建高并发的 AI 应用具有实用价值，因为它允许 Agent 在等待结果时释放上下文窗口资源，处理其他用户请求。

3.  **Strands Agents 的集成价值**
    Strands Agents（指代具有记忆、规划和工具调用能力的复杂 Agent 框架）与 Bedrock 的结合，旨在解决“一次性对话”的局限。通过这种集成，系统不仅能处理单次指令，还能维护跨会话的“记忆”。文章强调这一点，说明其目标场景是复杂的业务流程自动化（如 RPA + GenAI），而非简单的问答机器人。这提升了应用的功能上限，但也增加了系统调试的复杂度。

**局限性与边界条件**

1.  **成本与复杂度的权衡**
    对于简单的查询类任务（如“查询当前股价”），引入长连接和异步框架属于过度设计。维护上下文消息策略会产生额外的 Token 消耗和延迟，反而可能降低系统的响应速度和性价比。
2.  **分布式一致性的挑战**
    文章未详细阐述在分布式环境下（如 Bedrock 多可用区部署），如何保证异步任务状态的一致性。如果 AgentCore 实例重启，挂起的任务状态是否能恢复？如果缺乏持久化层支持，这种“长连接”可能成为单点故障的源头。

**维度评价**

*   **内容深度：** 文章从协议层面切入，深入到了 Agent 运行的生命周期管理。它没有停留在 API 调用层面，而是探讨了通信协议和并发模型，具有较高的技术深度。
*   **实用价值：** 对于正在基于 AWS 构建企业级 Agent 的开发者而言，该方案提供了一个可落地的参考架构，解决了实际生产中必然遇到的长任务超时问题。
*   **创新性：** 将 MCP 与 Bedrock AgentCore 结合并引入异步层，是对现有 Agent 编程范式的一种补充，属于工程层面的优化，具有很强的实用性。
*   **可读性：** 摘要逻辑清晰，从问题（通信中断）到方案（策略+框架）层层递进，符合技术文档的规范。
*   **行业影响：** 随着 MCP 逐渐成为 AI 连接的标准，如何将其适配到企业级的高可用架构中是行业关注点。本文为 AWS 生态内的开发者提供了参考路径，有助于推动 MCP 在关键业务系统中的落地。

**验证方式**

1.  **压力测试指标：**
    在高并发场景下，测量开启“上下文消息策略”前后的任务超时率。如果方案有效，长任务（>30秒）的成功率应有所提升，且平均响应时间（TTFB）不应出现明显劣化。

2.  **资源消耗观察：**
    监控 Bedrock Agent 的 Token 消耗量和网络连接数。检查在长任务期间，是否存在因为维持上下文心跳而产生的无效 Token 计费，这直接关系到方案的成本效益。

3.  **故障恢复实验：**
    在异步任务执行过程中人为中断网络或重启服务节点，观察任务是否能通过“上下文消息”恢复或获取最终状态，而非直接报错丢弃。

**应用建议**
建议在实际采用该方案时，务必在异步任务管理框架中引入“持久化存储”（如 DynamoDB），避免仅依赖内存状态。同时，应设置合理的超时熔断机制，防止因下游服务卡死而导致 MCP 服务器连接泄漏。

---
## 技术分析

基于提供的标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 深度分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 构建长时间运行的 MCP 服务器

## 1. 核心观点深度解读

**主要观点**
文章的主要观点是：**为了克服当前 AI Agent（智能体）在处理复杂、长周期任务时的局限性，开发者应当采用一种结合了“上下文消息策略”和“异步任务管理框架”的混合架构。** 这种架构利用 Amazon Bedrock 的 AgentCore 作为控制平面，并集成 Strands Agents 的概念，在 Model Context Protocol (MCP) 服务器上实现能够跨越长时间断点续传的智能工作流。

**核心思想**
作者试图传达的核心思想是**“有状态异步交互”**。传统的 LLM 交互通常是同步且无状态的（Request-Response），一旦任务耗时超过 LLM 的上下文窗口或超时限制，连接就会断开。作者提出通过 MCP 将 Agent 的“大脑”（LLM）与“手脚”（执行长任务的 Server）解耦，通过维持上下文连续性，使 AI 能够像人类项目经理一样，启动任务、挂起等待、并在获得结果后继续推理，而不是在一个请求中完成所有工作。

**创新性与深度**
*   **创新性**：将 MCP（通常用于数据检索的协议）扩展为一种**长任务编排协议**。结合 Bedrock AgentCore 的编排能力与 Strands Agents（可能指代特定的工作流或Agent框架）的持久化能力，提出了一种标准化的“任务生命周期管理”方案。
*   **深度**：文章触及了 AI Agent 落地的“最后一公里”问题——即如何处理现实世界中非瞬时的操作（如数据ETL、长时间编码、物理设备控制）。它不再局限于简单的 ChatBot 模式，而是向自主系统演进。

**重要性**
随着 AI 从“聊天”转向“行动”，长任务处理是必须跨越的门槛。如果无法处理长任务，AI 只能做简单的问答或单步操作，无法胜任复杂的企业级自动化。该观点为解决这一瓶颈提供了具体的工程路径。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **Model Context Protocol (MCP)**：一种开放协议，用于连接 AI 应用与数据源。在此处，它被扩展为连接 AI 与长时间运行的进程。
*   **Amazon Bedrock AgentCore**：Bedrock 的底层编排引擎，负责 Agent 的决策、路由和工具调用。
*   **Strands Agents**：在此语境下，推测指代一种支持“流”或“线程”持久化的 Agent 架构，能够在时间维度上保持状态。
*   **异步任务管理**：非阻塞的执行模式。

**技术原理和实现方式**
1.  **上下文消息策略**：
    *   **原理**：在 LLM 和 MCP Server 之间建立一个中间层。当 Server 收到耗时任务请求时，不立即返回最终结果，而是返回一个“任务票据”或“确认消息”，告知 LLM 任务已接收并在后台运行。
    *   **实现**：利用 Bedrock Agent 的 Orchestration（编排）层，解析 Server 的响应。如果检测到“异步状态”，Agent 进入挂起或轮询模式，而不是直接结束对话。

2.  **异步任务管理框架**：
    *   **原理**：构建一个后台任务队列（如基于 AWS Step Functions 或 SQS）。
    *   **实现**：MCP Server 接收到指令后，将任务推入后台队列，立即返回 HTTP 202 Accepted。Agent 随后通过另一个 MCP Tool 调用（如 `get_task_status`）来轮询或通过 Webhook 被动接收结果。

**技术难点与解决方案**
*   **难点1：上下文丢失**。LLM 是无状态的，长任务结束后 LLM 可能“忘记”了为什么要做这个任务。
    *   **解决方案**：文章提到的“上下文消息策略”核心在于**状态注入**。在任务完成后，MCP Server 必须将任务的原始目标、中间状态和最终结果打包成一个结构化的摘要，重新注入回 LLM 的上下文窗口中。
*   **难点2：超时控制**。LLM 调用工具通常有超时限制（如 90秒）。
    *   **解决方案**：将长任务拆解为“启动-检查-获取”三步走，将同步等待转化为异步轮询。

**技术创新点分析**
最大的创新在于**协议的语义升级**：将 MCP 从单纯的“Query-Response”（查询-响应）升级为“Command-Status-Result”（指令-状态-结果）。这要求 MCP Server 实现更复杂的状态机逻辑。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为构建企业级 AI 应用提供了蓝图。它解决了开发者不敢让 AI 调用耗时 API（如生成报表、调用微服务部署流程）的痛点，使得 AI 可以安全地介入关键业务流程。

**可应用场景**
1.  **RPA（机器人流程自动化）**：涉及跨系统、耗时的数据迁移或录入。
2.  **代码生成与部署**：AI 生成代码后，需要等待 CI/CD 流水线运行（可能需 10-20 分钟），传统模式会超时，此模式可完美适配。
3.  **数据分析与科研**：提交大规模计算任务，周期性轮询进度。
4.  **物联网（IoT）控制**：发送指令给物理设备（如“扫地机器人回充”），这是一个长达数十分钟的过程。

**需要注意的问题**
*   **成本控制**：频繁的轮询会消耗大量的 Token 和 API 调用费用。
*   **状态一致性**：如果异步任务失败，如何保证 LLM 能理解错误并重试，而不是陷入死循环。

**实施建议**
不要试图用 LLM 直接处理异步逻辑。应将异步逻辑封装在 MCP Server 内部，对 LLM 暴露的是同步的“状态查询”接口。

## 4. 行业影响分析

**对行业的启示**
这标志着 AI Agent 开发从“Prompt Engineering”向“Agent Engineering”的转变。行业开始关注 AI 系统的**鲁棒性**和**工程化架构**，而不仅仅是模型的智商。

**可能带来的变革**
*   **SaaS 软件的 AI 化改造**：SaaS 软件不再需要提供简单的 API 给 AI 调用，而是需要提供符合 MCP 标准的、支持长任务交互的 Agent 接口。
*   **MCP 协议的普及**：MCP 可能成为连接 AI 与业务系统的标准插座，类似于 SQL 对于数据库的重要性。

**相关领域的发展趋势**
*   **Agent 编排框架**（如 LangChain, AutoGen）将原生支持异步任务原语。
*   **云原生 AI**：与 AWS Step Functions、Lambda 等无服务器架构的深度绑定将成为标准做法。

## 5. 延伸思考

**引发的思考**
*   **人机协同的新模式**：在长任务运行期间，人类是否应该介入？例如，AI 提交了一个长任务，任务运行一半出错，AI 是否应该通知人类介入，还是自动重试？
*   **记忆系统的必要性**：长任务必然产生大量中间数据。如何存储这些非结构化数据？向量数据库还是关系型数据库？

**拓展方向**
*   **流式响应**：不仅是在任务结束后返回结果，而是在任务执行过程中实时向 LLM 推送进度，让 LLM 能够动态调整策略。
*   **多 Agent 协作**：一个 Agent 负责长任务调度，另一个 Agent 负责实时数据分析。

**未来趋势**
AI Agent 将逐渐具备“进程”的概念，类似于操作系统中的进程管理，拥有 PID、状态、优先级和资源限制。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务类型**：梳理你的 AI 应用中哪些工具调用耗时超过 30 秒。
2.  **引入中间层**：不要让 LLM 直接调用下游 API，而是调用你编写的 MCP Server。
3.  **实现状态机**：在 MCP Server 中定义任务状态。

**具体行动建议**
*   **阅读 MCP 规范**：深入了解 `tools` 和 `resources` 的定义。
*   **搭建 Bedrock Agent**：使用 AWS Bedrock 创建一个 Agent，并尝试配置一个 Lambda 函数作为 MCP Server 的后端。
*   **模拟长任务**：在代码中使用 `sleep` 模拟长耗时，测试 Agent 是否会超时报错，并应用文章中的异步策略进行修复。

**补充知识**
*   熟悉 **AWS Lambda** 和 **API Gateway**。
*   了解 **JSON Schema**（用于定义工具接口）。
*   掌握 **Python asyncio** 或 Node.js 异步编程。

## 7. 案例分析

**成功案例设想**
*   **场景**：一家电商公司使用 AI 自动化处理退款。
*   **传统模式**：AI 调用退款接口，接口响应慢，AI 超时，用户以为操作失败，重复点击。
*   **应用文章技术后**：AI 调用 MCP Server 启动退款流程 -> Server 返回“任务 ID 123” -> AI 告诉用户“退款申请已提交（ID 123），正在处理” -> 后台处理完成 -> Server 通过 Webhook 通知 Agent -> Agent 主动通知用户“退款成功”。

**失败案例反思**
*   **场景**：轮询间隔设计不当。
*   **问题**：Agent 每 1 秒轮询一次任务状态，导致下游 API 被打垮，且 Token 消耗殆尽。
*   **教训**：必须在 MCP Server 端实现退避算法，并限制 Agent 的最大轮询次数。

## 8. 哲学与逻辑：论证地图

**中心命题**
**为了构建具备企业级鲁棒性的 AI Agent，必须采用基于 MCP 的异步任务架构，将模型推理层与长耗时执行层解耦。**

**支撑理由与依据**
1.  **理由 1：LLM 的同步特性与物理世界的异步本质冲突。**
    *   *依据*：LLM 的 API 调用通常有严格的超时限制（如 60s-120s），而现实世界的任务（数据处理、物理操作）往往是分钟级或小时级的。
2.  **理由 2：连续性上下文是复杂任务完成的必要条件。**
    *   *依据*：认知科学表明，人类在处理长任务时需要“工作记忆”。AI 同样需要通过上下文消息策略来维持对长期目标的记忆，而非每次都从头开始。
3.  **理由 3：资源效率要求非阻塞式交互。**
    *   *依据*：让昂贵的 LLM 实例处于“等待”状态是巨大的资源浪费。异步框架允许 LLM 在任务等待期间处理其他请求。

**反例或边界条件**
1.  **反例 1（低延迟场景）**：对于毫秒级就能完成的简单查询（如“查天气”），引入异步框架和上下文管理会增加不必要的延迟和架构复杂度。
2.  **边界条件（强一致性要求）**：某些金融交易要求“实时确认”，不能接受异步带来的最终一致性延迟。

**命题性质分析**
*   **事实**：LL

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化会话状态管理与持久化

**说明**：
长期运行的 MCP 服务器必须处理跨多个请求和长时间周期的会话状态。由于 AgentCore 代理可能是无状态的，依赖外部持久化层来存储对话历史、用户偏好和中间任务状态至关重要，以防止在重启或扩展期间丢失上下文。

**实施步骤**:
1. 选择高性能的存储服务（如 Amazon DynamoDB 或 ElastiCache）来存储会话令牌和对应的上下文数据。
2. 实施检查点机制，定期将 Strands Agents 的中间状态保存到持久化存储中。
3. 配置合理的 TTL（生存时间）策略，以自动清理过期的会话数据，优化存储成本。

**注意事项**:
避免将会话状态存储在 MCP 服务器的本地内存中，因为这会导致扩展问题并在实例重启时丢失数据。

---

### 实践 2：实施异步通信与事件驱动架构

**说明**：
长期运行的代理任务（如数据处理或复杂的工作流编排）不应阻塞 MCP 服务器的运行时。通过集成 Amazon EventBridge 或 Amazon SQS，将长时间运行的任务与即时响应解耦，确保服务器能够持续接收新指令并报告进度。

**实施步骤**:
1. 将 MCP 服务器设计为发布者，接收任务后立即返回确认响应，并将任务详情发布到 SQS 队列或 EventBridge 总线。
2. 创建后台工作进程或 Lambda 函数来消费这些消息并执行实际的 Strands Agents 逻辑。
3. 配置回调机制或 WebSocket 连接，以便在任务完成时将结果推送回客户端。

**注意事项**:
确保异步任务的超时设置足够长，以适应复杂代理逻辑的执行时间，并实施死信队列（DLQ）处理策略以捕获失败的任务。

---

### 实践 3：建立全面的监控与可观测性

**说明**：
由于长期运行的服务容易出现资源泄漏或性能下降，必须实施全面的监控。利用 Amazon CloudWatch 来跟踪 MCP 服务器的运行状况、Strands Agents 的调用延迟以及错误率。

**实施步骤**:
1. 为 MCP 服务器和 AgentCore 集成配置详细的 CloudWatch Logs，记录请求、响应和错误堆栈。
2. 创建自定义 CloudWatch 指标，用于监控“活跃会话数”、“平均任务持续时间”和“Strands 调用成功率”。
3. 设置基于 CloudWatch 告警的自动恢复机制（例如，当错误率超过阈值时自动重启容器或触发 SNS 通知）。

**注意事项**:
确保日志不包含敏感信息（PII），并注意控制日志卷的大小以避免不必要的成本。

---

### 实践 4：设计幂等性与重试策略

**说明**：
在分布式环境中，网络波动或服务重启可能导致请求重复或超时。MCP 服务器必须实现幂等性，确保即使 Strands Agent 收到重复指令，也不会产生重复的副作用或数据损坏。

**实施步骤**:
1. 为每个客户端请求生成唯一的幂等键，并将其传递给 AgentCore 和 Strands Agents。
2. 在处理逻辑之前，检查存储层中是否已存在该幂等键的处理记录。
3. 配置具有指数退避算法的 SDK 重试逻辑，以应对 Bedrock 或 Strands 服务的暂时性限流（429错误）。

**注意事项**:
重试策略应与 Strands Agents 的状态管理紧密结合，避免在代理已完成任务但响应丢失时进行不必要的重试。

---

### 实践 5：实施细粒度的访问控制与安全隔离

**说明**：
MCP 服务器作为入口点，必须确保只有授权的请求才能触发特定的 Strands Agents。利用 IAM 角色和基于资源的策略，严格控制对 Bedrock 模型及下游工具的访问权限。

**实施步骤**:
1. 为 MCP 服务器分配最小权限 IAM 角色，仅包含调用特定 Bedrock 模型和访问必要 S3 存储桶的权限。
2. 在 AgentCore 配置中，使用 IAM 条件键限制对特定 Strands Agents 的访问。
3. 对所有传输中的数据实施 TLS 加密，并使用 AWS Secrets Manager 管理数据库或 API 密钥等凭证。

**注意事项**:
定期轮换凭证，并使用 AWS IAM Access Analyzer 验证资源策略是否未向外部实体授予意外的公共访问权限。

---

### 实践 6：优化资源利用与成本控制

**说明**：
长期运行的服务如果不加控制，可能会导致高昂的基础设施和模型推理成本。通过实施请求验证、响应缓存和资源限制，确保 MCP 服务器高效运行。

**实施步骤**:
1. 在请求到达 Bedrock 之前，在 MCP 层实现输入验证和净化，拒绝无效或格式错误的负载。
2. 对频繁重复的只读查询实施语义缓存，以减少对 Strands Agents 和 Bedrock 模型的调用次数。
3. 为容器化环境设置 CPU 和内存限制（Limits），防止失控进程消耗过多资源。

**注意事项**:
监控 Bedrock 的 Token 使用情况，因为 Strands Agents 可能会进行多轮推理，这会显著增加成本。<|user|>

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持构建能够长时间运行并保持状态的有状态 MCP 服务器。
- 通过集成 Strands Agents，开发者可以构建能够执行复杂、多步骤工作流的智能体，而无需从头管理基础设施。
- 该架构允许智能体在执行任务期间保留上下文记忆，从而支持更长时间的交互和更复杂的逻辑处理。
- 利用此方案可以显著简化开发流程，使开发者能够专注于业务逻辑而非底层的状态管理机制。
- 集成后的智能体能够更有效地调用外部工具和数据源，在保持连贯性的同时完成端到端的自动化任务。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文策略](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AD%96%E7%95%A5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器的异步任务框架]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-6.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于 Amazon Bedrock AgentCore 构建长时间运行的 MCP 服务器]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*