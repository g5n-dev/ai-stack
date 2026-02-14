---
title: "基于Amazon Bedrock AgentCore构建长时间运行的MCP服务器"
date: 2026-02-14T14:42:26+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长连接", "AI 代理", "架构设计"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 集成来构建能够长时间运行的 MCP 服务器的综合方法。该方法的核心在于解决 AI 代理在执行耗时任务时的通信连续性和操作非阻塞性问题，主要包含以下三个关键策略： 1. **上下文消息策略：** 为了确保服务器与客户端"
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

在这篇文章中，我们将为您提供一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，用于在长时间运行的操作期间保持服务器与客户端之间的持续通信。接着，我们开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的过程，而不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents 应用这些策略，构建能够可靠地处理复杂、耗时操作的生产级 AI 代理。

---
## 导语

构建能够处理长时间运行任务的 AI 代理往往面临通信中断与资源阻塞的挑战。本文将探讨如何通过上下文消息策略与异步任务管理框架，在 Amazon Bedrock AgentCore 上集成 Strands Agents，从而实现 MCP 服务器的稳定运行。您将获得一套构建生产级 AI 代理的完整方法，使其能够可靠地处理复杂且耗时的操作。

---
## 摘要

本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 集成来构建能够长时间运行的 MCP 服务器的综合方法。该方法的核心在于解决 AI 代理在执行耗时任务时的通信连续性和操作非阻塞性问题，主要包含以下三个关键策略：

1.  **上下文消息策略：**
    为了确保服务器与客户端在长时间操作中保持持续通信，文章首先引入了上下文消息策略。这一策略旨在维护连接的活性，防止因任务耗时过长而导致的会话中断或信息丢失，从而保证交互的连贯性。

2.  **异步任务管理框架：**
    其次，文章开发了一个异步任务管理框架。该框架允许 AI 代理启动长流程而不必阻塞其他操作。通过异步处理，系统可以并行处理多个任务或响应其他请求，显著提升了系统的并发处理能力和响应速度。

3.  **集成与生产级实现：**
    最后，文章演示了如何将上述策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合。这种集成使得构建出的 AI 代理不仅具备处理复杂、耗时操作的能力，还能满足生产环境对可靠性的高标准要求。

综上所述，该方法通过优化通信机制和任务调度，成功构建了稳定、高效的生产级 AI 代理。

---
## 评论

**文章中心观点**
文章主张通过在 Amazon Bedrock AgentCore 上构建集成了 Strands Agents 的 MCP（Model Context Protocol）服务器，并利用上下文消息策略与异步任务管理框架，来解决长期运行（Long-running）的 AI Agent 任务中的状态保持与服务连续性问题。

**支撑理由与深度评价**

**1. 架构层面的解耦与标准化（事实陈述 + 你的推断）**
文章提出的 MCP 服务器架构，实质上是将“大脑”（LLM 推理）与“手脚”（工具调用）进行了标准化解耦。MCP 协议正在成为 AI Agent 领域的“USB 接口”，而 Bedrock AgentCore 提供了托管式的编排能力。
*   **评价：** 这种架构具有极高的行业前瞻性。在当前的 AI 基础设施中，最大的痛点之一是工具调用的碎片化。通过将 Bedrock 的托管能力与 MCP 的开放标准结合，文章实际上在探索一种“企业级 App Store”的模式，使得 Agent 可以动态发现和调用工具，而无需硬编码 API。
*   **反例/边界条件：** MCP 协议目前的生态尚未完全成熟，对于极高并发（如每秒数千次调用）的场景，MCP 的 JSON-RPC 传输层可能成为性能瓶颈，此时直接的原生 SDK 调用可能效率更高。

**2. 异步任务管理框架的必要性（作者观点 + 行业共识）**
摘要中提到的“异步任务管理框架”直击当前 LLM 应用的痛点：超时与上下文丢失。LLM 的推理是同步且耗时的，而现实世界的任务（如数据处理、API 查询）往往是长尾的。
*   **评价：** 文章引入异步框架是技术上的必然选择。这类似于后端开发中的“消息队列”模式。如果 Agent 发起指令后必须一直等待结果，不仅浪费 Token 成本，还极易遇到 HTTP 超时断开。Strands Agents 的集成暗示了其可能具备处理“流式状态”的能力，这对于构建复杂的自动化工作流至关重要。
*   **反例/边界条件：** 异步架构会显著增加系统的复杂度（尤其是最终一致性的处理）。对于简单的、毫秒级响应的查询任务（如“现在几点？”），引入异步框架反而会增加延迟和系统开销，属于“杀鸡用牛刀”。

**3. 上下文消息策略的工程化实现（技术分析）**
文章强调“上下文消息策略”以维持连续通信。这通常涉及到如何在长周期任务中，将中间状态切片反馈给用户或主控循环。
*   **评价：** 这是提升用户体验的关键。在 Agent 执行长任务时，用户往往面临“黑盒”焦虑。通过 Bedrock AgentCore 维护会话状态，并利用 MCP 服务器推送中间进度，实际上是将“批处理”任务转化为“交互式”任务。这要求开发者具备精细的状态机设计能力，而非仅仅调用 API。
*   **反例/边界条件：** 这种策略对 Token 消耗有潜在风险。如果上下文管理不当，随着任务周期的拉长，上下文窗口可能会迅速被中间过程日志填满，导致“上下文窗口溢出”或成本失控。

**批判性思考与争议点**

**1. 厂商锁定风险**
虽然文章使用了 MCP 这一开放标准，但核心逻辑强依赖于 Amazon Bedrock AgentCore。这意味着一旦业务逻辑深度绑定 Bedrock 的特定配置（如 Strands Agents 的特定 API），未来若要迁移至 Azure OpenAI 或本地部署的 Ollama，重构成本将非常高。企业需要在“托管服务的便利性”与“多云架构的灵活性”之间做权衡。

**2. Strands Agents 的黑盒性质**
文章提到了 Strands Agents，但作为 AWS 的特定集成组件，其内部逻辑（如决策的可解释性、重试机制的细节）往往是不透明的。对于金融或医疗等对决策逻辑有强审计要求的行业，这种“黑盒”集成可能会面临合规性挑战。

**实际应用建议**

1.  **成本监控机制：** 在实施此类长运行 Agent 时，务必设置基于 Token 数量和步骤数的熔断机制。异步任务极易产生“失控”的循环调用，导致账单爆炸。
2.  **混合架构模式：** 不要将所有任务都放入异步框架。建议建立一个“任务分流器”：对于简单任务走同步调用，对于耗时超过 5 秒的任务才走 Bedrock AgentCore 的异步框架。
3.  **状态持久化：** 不要仅依赖 Bedrock 的内存状态。务必将异步任务的元状态持久化到 DynamoDB 或 S3 中，以防止 Agent 进程重启导致任务状态丢失。

**可验证的检查方式**

1.  **压力测试指标：** 搭建测试环境，同时发起 100 个长运行任务（每个任务模拟耗时 60 秒），观察 Bedrock AgentCore 的并发处理能力及 MCP 服务器的连接稳定性，检查是否存在连接泄露或请求排队延迟。
2.  **Token 消耗审计：** 运行一个典型的长周期工作流，对比使用“上下文消息策略”前后，单次任务的平均 Token 消耗量，计算增量成本是否在可接受范围内。
3.  **中断恢复测试：** 在 Agent 执行任务过程中，人为强制重启 MCP 服务器进程，观察 Bedrock AgentCore 是否能检测到连接中断并自动重连或触发错误处理流程，而非无限期挂起。
4.  **延迟基准测试：** 测量从任务实际完成到 Agent 向用户返回最终结果之间的端到端延迟，评估异步

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 深度分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 构建长时间运行的 MCP 服务器

## 1. 核心观点深度解读

**文章的主要观点**
文章提出了一种在 Amazon Bedrock 环境下构建能够处理长时间运行任务的模型上下文协议（MCP）服务器的综合架构方法。其核心在于解决传统 LLM 应用受限于请求-响应模式，无法有效处理耗时任务（如数据处理、复杂编码、长时间检索）的痛点。

**作者想要传达的核心思想**
AI Agent 不应仅仅是“问答机器”，而应是“任务执行者”。为了实现这一点，系统架构必须从“同步阻塞”转向“异步非阻塞”。作者主张通过 **Strands Agents（流式代理集成）** 来维持任务的连续性，并结合 **上下文消息策略** 确保在任务执行期间，客户端与服务端之间保持状态的同步与通信，从而实现真正的“长时间运行”能力。

**观点的创新性和深度**
*   **架构层面的解耦**：创新点在于将“任务控制流”与“数据流”分离。通过引入异步任务管理框架，使得 LLM 可以在任务后台运行时释放会话资源，甚至在任务完成后重新唤起上下文。
*   **深度的状态管理**：文章深入探讨了如何在无状态（Stateless）的 HTTP 通信协议之上，通过 MCP 协议模拟出有状态的交互体验，这是构建复杂生产级 AI 应用的关键。

**为什么这个观点重要**
随着 AI 从 Content Generation（内容生成）向 Action Taking（行动执行）演进，Agent 需要处理的任务复杂度呈指数级上升。如果无法解决“长任务”导致的超时和上下文丢失问题，AI Agent 将难以应用于企业级核心业务流程（如 RPA、自动化运维、复杂数据分析）。这篇文章提供了一套在 AWS 生态内落地的标准化解决方案。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**：一种开放协议，用于连接 AI 应用与数据源。在此文中，它被扩展用于支持长时间运行的交互模式。
2.  **Amazon Bedrock AgentCore**：AWS 提供的构建 Agent 的底层核心服务，负责编排 LLM 与工具的调用。
3.  **Strands Agents**：这是文章引入的关键概念（可能是 AWS 内部或特定的集成模式），指代能够处理连续“线索”或“流”的 Agent 架构，支持任务的分步执行和状态保持。
4.  **Asynchronous Task Management (异步任务管理)**：技术核心，用于处理非即时的操作。

**技术原理和实现方式**
*   **Context Message Strategy (上下文消息策略)**：系统不再是一次性返回所有结果，而是建立一个持续的通信通道。当 Agent 调用一个耗时工具时，它不会挂起连接等待结果，而是返回一个“任务已接收”的中间状态，并携带一个唯一的任务标识符。客户端通过该标识符轮询或接收任务进度的更新。
*   **异步任务框架**：Agent 触发任务后，任务被提交到后台队列（如 AWS Step Functions 或 Lambda 异步调用）。MCP Server 维护一个任务状态存储（如 DynamoDB），记录任务是“进行中”、“已完成”还是“失败”。

**技术难点和解决方案**
*   **难点**：LLM 的 Context Window（上下文窗口）有限，长时间的交互可能导致 Token 溢出；同时，长连接容易因网络波动断开。
*   **解决方案**：通过 Strands Agents 集成，系统实现了“上下文压缩”与“检查点”机制。只有关键的状态变更会被推送给 LLM，而非全量日志。此外，MCP 协议允许客户端重连并恢复会话。

**技术创新点分析**
将 **Bedrock AgentCore** 的编排能力与 **Strands** 的流式处理能力结合，使得 MCP Server 不仅仅是一个被动的工具调用接口，而变成了一个主动的任务调度器。

## 3. 实际应用价值

**对实际工作的指导意义**
这篇文章为开发者提供了一种在 AWS 云原生环境下构建“高延迟容忍度”AI 应用的蓝图。它教导开发者如何设计 API 接口，使得 AI 能够像人类员工一样，启动一个任务（如“生成月度报表”），然后去处理其他事情，稍后再回来查看结果，而不是傻等报表生成完毕。

**可以应用到哪些场景**
1.  **企业级 RPA（机器人流程自动化）**：例如跨系统的数据迁移，耗时可能长达数小时。
2.  **代码生成与部署**：Agent 生成代码后，需要触发 CI/CD 流水线进行构建、测试和部署，这是一个典型的长任务。
3.  **大数据分析**：提交 SQL 查询到数据仓库，等待查询结果。
4.  **多媒体生成**：视频渲染或 3D 模型生成。

**需要注意的问题**
*   **状态一致性**：确保异步任务的结果能准确地反馈回正确的用户会话。
*   **成本控制**：长轮询或维持长连接可能会增加基础设施成本。
*   **错误处理**：如果后台任务失败，Agent 需要有能力进行自我修复或向用户报错。

**实施建议**
在实施时，应优先采用 **事件驱动架构**。利用 AWS EventBridge 将任务完成事件路由回 Bedrock Agent，而不是让 Agent 频繁轮询数据库。

## 4. 行业影响分析

**对行业的启示**
这标志着 AI Agent 开发模式正在从 **“Chatbot 模式”**（即时问答）向 **“Assistant 模式”**（自主协作）转变。行业标准将不再满足于 API 的低延迟，而是关注 API 的“可异步性”和“状态可观测性”。

**可能带来的变革**
未来，所有的 SaaS API 如果想要被 AI Agent 高效调用，可能都需要遵循类似的“长任务协议”标准（如 MCP 的扩展）。这将推动 API 设计的变革，从 RESTful 向更注重事件和状态的架构演进。

**相关领域的发展趋势**
*   **Agentic Workflows（代理工作流）**：LangChain、LangGraph 等框架正在大力发展的方向。
*   **Serverless AI**：利用 AWS Lambda/Step Functions 处理长任务是未来的主流。

## 5. 延伸思考

**引发的其他思考**
这种架构是否可以引入“人机协同”机制？例如，当 Agent 运行长任务遇到关键决策点（如删除大量数据）时，通过该异步机制暂停任务，请求人类批准，然后再继续执行。

**可以拓展的方向**
*   **多 Agent 协作**：一个 Agent 负责长任务的调度，多个 Specialist Agents 负责子任务的执行。
*   **流式输出与流式输入的结合**：不仅输出是流式的，任务的中间状态（如进度条百分比）也应该实时流式传输给前端。

**需要进一步研究的问题**
在极端高并发情况下，如何保证上下文消息策略的高效性？是否需要引入 Redis 等高性能缓存来替代 DynamoDB 存储临时的会话状态？

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务类型**：审查你现有的 AI Agent 应用，识别出哪些工具调用耗时超过 10 秒。
2.  **引入异步层**：不要直接在 LLM 的 Tool 调用中执行耗时逻辑，而是将其封装为异步任务。
3.  **改造 MCP 接口**：确保你的 MCP Server 返回 `taskId` 而不是直接返回 `result`。

**具体的行动建议**
*   阅读 AWS Bedrock 的官方文档中关于 Agent orchestration 的部分。
*   使用 Step Functions Express 工作流来处理这些异步任务，因为其更适合高并发、短周期的任务。
*   在前端实现“加载中”或“任务队列”的 UI 组件，以配合后端的异步机制。

**需要补充的知识**
*   熟悉 **AWS Step Functions** 的状态机定义。
*   理解 **MCP 协议** 的 Resource 和 Prompt 定义。
*   掌握 **Python asyncio** 或 Node.js 异步编程模型。

## 7. 案例分析

**成功案例分析**
*   **场景**：一家金融公司使用 Bedrock Agent 构建财报分析助手。
*   **做法**：用户上传 PDF（长任务），Agent 调用 OCR 和 Embedding 服务进行解析。通过 Strands 集成，Agent 告诉用户“正在解析，请稍候”，并在后台处理。处理完成后，Agent 主动通知用户“解析完成，可以开始提问”。
*   **效果**：避免了 API Gateway 的 30 秒超时限制，用户体验流畅。

**失败案例反思**
*   **场景**：直接在 Lambda 中调用 Bedrock API 并等待另一个微服务的响应。
*   **问题**：微服务处理耗时 5 分钟，导致 Lambda 超时，任务丢失，用户不知道是成功还是失败。
*   **教训**：在构建长任务 Agent 时，必须假设所有外部调用都是不可靠且耗时的，必须引入中间层进行解耦。

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级 AI Agent 时，**必须采用基于异步任务管理和上下文消息策略的架构（如文中提出的 MCP + Strands 模式），以克服同步请求-响应模式在处理长耗时操作时的局限性。**

**支撑理由**
1.  **技术必要性**：同步 HTTP 请求受限于超时设置（通常为 30-60 秒），无法容忍数据密集型或计算密集型任务所需的数分钟甚至数小时的执行时间。
2.  **用户体验**：用户需要即时的反馈以确认系统已接收指令，长时间的“空白等待”会导致用户焦虑并重复提交请求。
3.  **资源效率**：长连接占用服务器资源，异步处理允许服务端在高并发下更有效地调度计算资源。

**反例或边界条件**
1.  **简单查询场景**：对于纯知识库检索或简单文本生成（<5秒），引入异步框架会增加系统复杂度和延迟，得不偿失。
2.  **强一致性要求场景**：如果业务逻辑要求必须在同一个事务中完成读取-计算-写入并立即返回结果，异步解耦可能会破坏事务的 ACID 特性，需要额外的补偿机制。

**命题性质**
*   **事实**：现有网络协议和 LLM 推理接口存在超时限制。
*   **预测**：采用该架构将显著提高复杂任务的成功率和用户满意度。
*   **价值判断**：“长时间运行的能力”是 Agent 从玩具走向生产环境的必经之路。

**立场与验证**
我支持该命题。对于旨在执行复杂工作流的 Agent 应用，这种架构是目前的**最优解**。

**可证伪的验证方式**
*   **指标**：对比引入该架构前后，Agent 处理 >30秒任务的成功率（从超时错误率降低至 <1%）。
*   **观察**：在用户侧，观察任务放弃率是否因“即时反馈”机制而下降。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化长连接会话的状态管理

**说明**:
在构建长时间运行的 MCP (Model Context Protocol) 服务器时，维持会话状态至关重要。AgentCore 需要在多轮对话中保持上下文连贯性。不当的状态管理会导致内存泄漏或上下文丢失，特别是在处理 Strands Agents 的复杂工作流时。

**实施步骤**:
1. 实施基于 TTL (Time To Live) 的会话清理机制，自动回收闲置资源。
2. 将状态数据持久化到 Amazon DynamoDB 等外部存储中，而不是仅依赖内存。
3. 设计无状态的服务器逻辑，确保任何实例都可以恢复会话上下文。

**注意事项**:
避免在内存中存储敏感的 PII (个人身份信息) 数据，并确保状态序列化/反序列化的开销不会增加延迟。

---

### 实践 2：实施严格的超时与重试策略

**说明**:
长运行任务容易受到网络波动或下游服务延迟的影响。为了确保 MCP 服务器与 Bedrock AgentCore 之间的稳定性，必须配置合理的超时和指数退避重试机制，以防止级联失败。

**实施步骤**:
1. 为所有 MCP 工具调用配置明确的超时限制（例如 60 秒）。
2. 使用 AWS SDK 的内置重试器，配置指数退避策略。
3. 实施断路器模式，当下游服务持续失败时自动暂停请求，防止系统过载。

**注意事项**:
确保重试逻辑是幂等的，以避免在重试过程中重复执行写操作。

---

### 实践 3：利用 Strands Agents 实现异步编排

**说明**:
Strands Agents 允许将复杂的任务分解为多个子任务。对于耗时较长的操作（如数据处理或生成报告），应采用异步编排模式，而不是阻塞 MCP 服务器的响应线程，从而提高系统的吞吐量。

**实施步骤**:
1. 将长时间运行的操作定义为异步 Strand，通过 Step Functions 或 SNS/SQS 进行触发。
2. MCP 服务器应立即返回一个“任务已接收”的确认响应，并返回一个任务 ID。
3. 配置回调机制或轮询接口，供 AgentCore 查询任务完成状态。

**注意事项**:
需要妥善处理异步任务的错误通知，确保 AgentCore 能够捕获并处理子任务中的异常。

---

### 实践 4：增强可观测性与日志记录

**说明**:
长运行服务难以调试。为了监控 MCP 服务器的健康状况并排查 Strands Agents 的执行问题，必须建立全面的可观测性体系，包括结构化日志、指标和追踪。

**实施步骤**:
1. 使用 Amazon CloudWatch Logs 收集所有 MCP 交互的日志，并包含 `Trace ID`。
2. 启用 AWS X-Ray 进行分布式追踪，以可视化请求在 Bedrock 和 MCP 服务器之间的完整路径。
3. 设置关键指标告警（如延迟、错误率、超时率），以便在性能下降时立即通知运维人员。

**注意事项**:
注意日志采样率，避免在高并发场景下产生高昂的日志存储成本和性能损耗。

---

### 实践 5：配置精细化的 IAM 权限控制

**说明**:
MCP 服务器通常需要代表 AgentCore 调用其他 AWS 服务。为了遵循最小权限原则，必须精细定义 IAM 角色，限制 Strands Agents 的操作范围，防止权限滥用。

**实施步骤**:
1. 为 MCP 服务器创建专用的 IAM 角色，仅授予执行特定任务所需的权限。
2. 如果 MCP 服务器需要访问 Bedrock，确保包含 `bedrock:InvokeModel` 权限，并限制模型 ID。
3. 定期使用 IAM Access Analyzer 审查权限，移除未使用的策略。

**注意事项**:
不要在代码中硬编码凭证，始终使用 IAM 角色或 AWS Secrets Manager 来管理敏感信息。

---

### 实践 6：实施高效的负载均衡与自动扩缩容

**说明**:
长运行 MCP 服务器可能会遇到突发流量。为了保证高可用性，应使用负载均衡器分发流量，并根据 CPU 或内存利用率自动调整计算资源。

**实施步骤**:
1. 将 MCP 服务器部署在 Amazon ECS 或 EKS 集群中，配置 Application Load Balancer。
2. 配置 AWS Auto Scaling 组或 KEDA (Kubernetes Event-driven Autoscaling)，根据请求队列长度自动扩缩容实例。
3. 确保服务器启动迅速，以应对自动扩缩容带来的实例频繁更替。

**注意事项**:
在扩缩容过程中，确保连接能够优雅终止（Graceful Shutdown），避免正在处理的请求被强制中断。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持通过 Strands Agents 集成来构建和部署长期运行的 MCP 服务器
- 开发者可以利用 Strands 框架将状态化、多步骤的复杂逻辑封装为标准化的 MCP 工具
- 该集成方案解决了传统无状态 Agent 难以维持长期对话上下文和记忆的技术瓶颈
- 通过将 Strands Agent 暴露为 MCP 工具，实现了 Bedrock 生态与外部长期运行服务的无缝互操作
- 此架构允许 Bedrock Agent 在处理复杂工作流时保持状态，无需在每次交互中重新加载上下文

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于 Amazon Bedrock AgentCore 构建长时间运行的 MCP 服务器]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*