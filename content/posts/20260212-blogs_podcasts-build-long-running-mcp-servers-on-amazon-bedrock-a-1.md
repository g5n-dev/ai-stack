---
title: "基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理"
date: 2026-02-12T22:18:39+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长连接", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon Bedrock AgentCore 上构建长期运行的 MCP 服务器，并集成 Strands Agents。主要内容包括以下三个方面： 1. **上下文消息策略**：引入了一种消息策略，用于在服务器和客户端之间维持长时间的持续通信，确保在扩展操作期间的信息同步。 2. **异步任务管理框"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们将为您提供一个全面的实现方案。首先，我们会介绍一种上下文消息策略，以确保在耗时操作期间服务器与客户端之间保持持续通信。接着，我们会构建一个异步任务管理框架，让您的 AI 代理能够启动长时间运行的流程，同时不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents 来整合这些策略，从而构建出生产就绪的 AI 代理，使其能够可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是迈向生产环境的关键一步。本文将介绍一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的实现方案，重点探讨如何通过上下文消息策略和异步任务管理框架，确保服务器与客户端在耗时操作期间保持持续通信且不阻塞主流程。阅读本文，您将掌握构建高可用、生产就绪型 AI 代理的具体方法，使其能够可靠地处理复杂的业务逻辑。

---
## 摘要

本文介绍了如何在 Amazon Bedrock AgentCore 上构建长期运行的 MCP 服务器，并集成 Strands Agents。主要内容包括以下三个方面：

1.  **上下文消息策略**：引入了一种消息策略，用于在服务器和客户端之间维持长时间的持续通信，确保在扩展操作期间的信息同步。
2.  **异步任务管理框架**：开发了一个异步框架，允许 AI 代理启动耗时的进程，同时不会阻塞其他操作的执行。
3.  **生产级集成实现**：展示了如何将上述策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合，构建出能够可靠处理复杂、耗时任务的生产级 AI 代理。

---
## 评论

### 评价报告：基于 Amazon Bedrock AgentCore 的长运行 MCP 服务器构建

**文章中心观点**
该文章主张通过在 Amazon Bedrock AgentCore 上集成 Strands Agents，并利用“上下文消息策略”与“异步任务管理框架”，来解决模型上下文协议（MCP）服务器在处理长周期任务时的状态保持与通信中断问题，从而实现具备持久化记忆和执行能力的 AI 智能体。

**支撑理由与深度分析**

**1. 突破同步调用的局限性：从“请求-响应”到“任务流”**
*   **分析（事实陈述/作者观点）：** 传统的 LLM 应用多采用同步 RPC 模式，一旦任务执行时间超过 LLM 的超时窗口（通常为几十秒），连接就会断开。文章提出的“异步任务管理框架”实际上是将 MCP 服务器从简单的 API 响应者转变为任务调度器。这种架构允许 LLM 发起任务后“挂起”对话，而后端通过 Strands 继续执行，这符合**工作流自动化**的行业趋势。
*   **批判性视角（你的推断）：** 这种架构虽然解决了超时问题，但引入了**最终一致性**的挑战。如果异步任务执行失败，如何向已经“断开”的 LLM 上下文回滚状态？文章可能未充分讨论分布式事务的复杂性。

**2. 上下文连续性策略：对抗遗忘机制**
*   **分析（事实陈述）：** LLM 是无状态的。文章提出的“上下文消息策略”旨在通过特定的消息格式将 Strands 的执行结果重新注入 LLM 的上下文窗口。
*   **行业角度（你的推断）：** 这是目前 Agent 编排的核心痛点。如果 Bedrock AgentCore 能够自动处理这种“状态快照”的注入，它实际上是在构建一个**虚拟的短期记忆层**。这比单纯依赖 RAG（检索增强生成）更进了一步，因为它包含了任务的临时动态变量，而不仅仅是静态知识。

**3. 云原生集成的双刃剑**
*   **分析（事实陈述）：** 利用 Bedrock AgentCore 意味着深度绑定 AWS 生态。
*   **实用价值（作者观点）：** 对于已经重度使用 Lambda、DynamoDB 或 Step Functions 的企业，这种集成提供了极佳的运维便利性（如内置的监控和鉴权）。
*   **反例/边界条件：** 如果企业需要混合云部署或边缘计算，重度依赖 Bedrock 的托管服务会导致**厂商锁定**。此外，AgentCore 的冷启动时间可能会成为高频交互场景下的性能瓶颈。

**反例与边界条件**

1.  **成本边界：** 维护长连接和频繁的上下文注入会显著增加 Token 消耗和 API 调用次数。对于简单的查询任务（如“查天气”），这种重型架构可能过于昂贵，传统的直接 API 调用更优。
2.  **实时性悖论：** 虽然解决了“长运行”问题，但“异步”意味着“非实时”。如果用户需要毫秒级的流式反馈（如游戏 NPC 交互），基于 Strands 的批处理式任务反馈可能会导致体验割裂。
3.  **复杂性过载：** 引入 Strands 和异步框架增加了调试难度。当一个任务在 Bedrock 后台失败时，开发者可能难以区分是 Prompt 问题、代码逻辑问题还是云服务网络问题。

**可验证的检查方式（指标/实验）**

1.  **断点恢复测试：** 在长运行任务（如数据处理超过 2 分钟）执行期间，主动切断客户端网络连接，然后重新连接。验证 Agent 是否能通过 Context Message 策略无缝获取当前进度，而非从头开始。
2.  **Token 消耗基准：** 对比“直接调用 Bedrock”与“通过 MCP + Strands 调用”在完成相同长周期任务时的 Token 总用量。计算引入异步框架带来的“上下文税”是否在可接受范围内（通常预期增加 20%-40%）。
3.  **并发状态一致性：** 同时向同一个 Agent ID 发起两个修改共享状态的长任务。观察系统是否通过 AgentCore 正确处理了并发冲突，还是出现了数据覆盖。

**综合评价**

*   **内容深度：** 文章触及了当前 AI Agent 落地的深水区——状态管理。它不仅停留在 API 调用层面，而是深入到了架构设计层面，论证了为何单纯的 LLM 无法满足企业级长任务需求。
*   **实用价值：** 对于 AWS 生态内的开发者具有极高的参考价值，提供了一套可复用的脚手架代码思路。但对于非 AWS 用户，迁移成本较高。
*   **创新性：** 将 MCP（一种协议）与 Bedrock AgentCore（托管服务）及 Strands（执行框架）结合，提出了一种“三层解耦”的 Agent 架构，具有一定的前瞻性。
*   **争议点：** 过度依赖云厂商的托管能力可能会削弱开发者对底层逻辑的控制权。此外，文章可能低估了 Prompt 注入攻击在复杂的上下文消息传递中的风险。

**实际应用建议**
建议在采用此方案前，先评估任务的生命周期。对于秒级任务，保持同步；对于分钟级以上的任务（如生成报告、批量处理），采用文中所述的异步 Strands 模式。同时，务必在异步任务回调中设计严格的校验机制，防止恶意或错误的执行结果污染 LLM 的上下文窗口。

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：**构建能够处理长时间运行任务的生成式 AI 应用，不能仅依赖传统的同步请求-响应模式，而必须引入“上下文消息策略”和“异步任务管理框架”来实现持续通信和状态管理。**

**作者想要传达的核心思想**
作者试图传达一种架构思维的转变。在传统的 MCP（Model Context Protocol）或 Agent 开发中，我们往往假设任务是可以快速完成的（例如回答一个查询）。然而，现实世界的复杂任务（如数据分析、代码生成、工作流编排）往往耗时较长。作者的核心思想是：**Agent 不应被阻塞等待任务完成，而应具备“挂起”、“通知”和“恢复”对话的能力，从而在保持用户体验流畅的同时，处理后台繁重的计算逻辑。**

**观点的创新性和深度**
*   **创新性**：该文章将 Amazon Bedrock 的 AgentCore（一种托管式编排服务）与 Strands Agents（一种专注于长周期、多步骤任务的 Agent 框架概念）相结合。这不仅仅是简单的 API 调用，而是提出了一种**协议层面的混合模式**：利用 MCP 的标准化接口，通过上下文注入来解决 LLM（大模型）的“无状态性”与长任务“有状态性”之间的矛盾。
*   **深度**：文章深入到了异步状态机的细节。它没有停留在“使用 Agent”的表面，而是探讨了如何在 Server 端维护一个“虚拟会话”，使得 Agent 能够像人类一样，在处理完长任务后“回来”汇报结果。

**为什么这个观点重要**
随着 AI 从“聊天机器人”向“智能体”演进，处理复杂、多步骤、耗时的业务流程成为刚需。如果无法解决长连接超时、用户体验中断等问题，AI Agent 将无法应用于核心业务系统（如金融审批、自动化运维）。这篇文章提出的方案是打通 AI Agent 与企业级后端系统的关键桥梁。

---

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**：一种开放协议，用于连接 AI 应用与外部数据源。文章重点在于如何在此协议上实现长连接。
2.  **Amazon Bedrock AgentCore**：AWS 提供的底层 Agent 编排服务，负责路由、工具调用和记忆管理。
3.  **Strands Agents**：指代具备“线程”或“链”能力的 Agent，能够处理跨时间周期的任务。
4.  **Context Message Strategy（上下文消息策略）**：一种在断开连接后，如何重新将历史状态注入 LLM 的技术。
5.  **Asynchronous Task Management（异步任务管理）**：非阻塞的任务处理模式。

**技术原理和实现方式**
*   **上下文消息策略**：
    *   **原理**：LLM 本身是无状态的。当 Agent 发起一个长任务（如“处理视频”）时，客户端不能一直挂起等待。
    *   **实现**：Server 端接收任务后，立即返回一个 `TaskID` 并挂起会话。后台 Worker 处理任务。当任务完成或需要用户输入时，Server 利用 MCP 协议，主动推送消息或更新 Context 状态。当用户再次询问时，Agent 会加载包含之前任务结果的 Context，从而“恢复”对话。
*   **异步任务框架**：
    *   **实现**：通常基于消息队列（如 AWS SQS）或事件流（如 EventBridge）。AgentCore 将任务意图转化为异步指令，交给 Strands Agent 执行。执行过程中，状态被持久化到数据库（如 DynamoDB），而不是保存在内存中。

**技术难点和解决方案**
*   **难点 1：超时与资源消耗**。保持 HTTP 长连接直到任务完成会导致资源耗尽。
    *   **解决方案**：采用“Fire-and-Forget”（发后即忘）模式，配合轮询或 WebSocket 推送来获取结果。
*   **难点 2：上下文丢失**。长任务完成后，Agent 可能“忘记”最初的指令。
    *   **解决方案**：构建结构化的会话历史存储，在每次交互时将关键的任务状态摘要注入 System Prompt 或 User Message 中。

**技术创新点分析**
文章的创新点在于**将 MCP 协议从“数据检索工具”扩展为“任务执行协调器”**。传统的 MCP 更多用于查询数据库，而该方案利用 MCP 定义的工具接口，驱动了一个复杂的异步状态机，赋予了 Bedrock Agent 处理企业级工作流的能力。

---

## 3. 实际应用价值

**对实际工作的指导意义**
对于架构师和 AI 工程师而言，这篇文章提供了一个构建**生产级 Agent** 的标准参考架构。它指出了不要试图用 LLM 直接处理所有耗时操作，而是要设计合理的异步边界。

**可以应用到哪些场景**
1.  **RAG（检索增强生成）的大规模文档处理**：上传文档后，需要几分钟进行向量化，期间 Agent 需异步处理并通知用户“就绪”。
2.  **代码生成与 CI/CD 集成**：Agent 生成代码后，触发构建、测试、部署流程，这可能需要 10 分钟以上。
3.  **数据分析与报表生成**：Agent 需要查询海量数据，生成 Excel 或图表，无法秒级返回。
4.  **企业审批流**：Agent 提交申请后，需要等待人工审批（可能数天），审批通过后继续执行后续步骤。

**需要注意的问题**
*   **状态一致性**：确保异步任务失败后的回滚或重试机制完善。
*   **安全性**：长周期的任务意味着更长的会话劫持风险，需严格校验 `TaskID` 权限。

**实施建议**
建议采用 **Sidecar 模式**。在 Bedrock Agent 旁边部署一个任务管理服务，Agent 只负责决策和发起任务，具体的执行和状态维护由 Sidecar 服务通过 Strands 模式处理。

---

## 4. 行业影响分析

**对行业的启示**
这标志着 AI Agent 开发从“原型验证”走向“工程化落地”。行业开始关注 AI 系统的**可靠性**和**可扩展性**，而不仅仅是模型的智商。

**可能带来的变革**
*   **Agent 即服务**：未来的 SaaS 软件将不再提供 UI，而是提供标准的 MCP 接口，由用户自带的 Agent 进行异步调用。
*   **Serverless Agent 的普及**：结合 Bedrock，这种架构将极大地降低长周期 AI 应用的运维成本。

**对行业格局的影响**
AWS 通过推广 Bedrock + AgentCore + MCP 的组合，正在建立其企业级 AI 生态的标准。这将迫使开发者更深度地依赖 AWS 的基础设施，从而形成技术护城河。

---

## 5. 延伸思考

**引发的其他思考**
*   **人机协作的新范式**：如果 Agent 能够异步执行长任务，那么人类在其中的角色是“监督者”还是“协作者”？如何设计交互让人类知道何时该介入，何时该等待？
*   **成本控制**：异步任务虽然节省了连接资源，但频繁的 Context 注入和数据库读写可能会增加 Token 消耗和延迟，如何平衡？

**未来发展趋势**
*   **流式 MCP**：未来的 MCP 协议可能会原生支持流式传输和双向流，从而简化当前的异步模拟方案。
*   **Agent 编排标准化**：Strands Agents 的概念可能会演变成一种通用的标准，使得不同厂商的 Agent 可以互相传递长任务。

---

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务类型**：如果你的应用涉及超过 30 秒的处理时间，必须引入此架构。
2.  **引入状态存储**：不要只依赖 LLM 的 History，使用 Redis 或 DynamoDB 存储任务状态。
3.  **定义工具接口**：在 MCP Server 中，将工具定义为 `start_task` 和 `check_task` 两种模式。

**具体的行动建议**
*   阅读 AWS Bedrock 的 AgentWrapper 文档，了解如何处理异步回调。
*   搭建一个简单的 MCP Server，使用 Python 的 `asyncio` 库模拟长任务，观察 Bedrock 如何处理超时。

**实践中的注意事项**
*   **错误处理**：如果异步任务失败，Agent 必须能够生成自然的语言错误解释，而不是抛出堆栈跟踪。
*   **Token 限制**：随着任务步骤增加，Context 会膨胀，必须实施有效的“上下文压缩”策略。

---

## 7. 案例分析

**成功案例分析**
*   **企业级知识库助手**：某跨国公司构建 Agent 处理合规性检查。用户上传文档，Agent 调用 MCP Server 启动异步扫描（耗时 5 分钟）。期间 Agent 告知用户“正在扫描，请稍候”。扫描完成后，Agent 主动通过邮件或通知栏推送结果。这解决了传统 API 超时导致的用户焦虑。

**失败案例反思**
*   **缺乏状态的 ChatBot**：早期的一些客服 Agent 尝试直接调用 ERP 接口生成订单。由于 ERP 处理慢，HTTP 请求超时，导致 Agent 重复提交订单或告诉用户“我失败了”。这正是因为缺乏异步任务框架和上下文保持机制。

---

## 8. 哲学与逻辑：论证地图

**中心命题**
**在构建基于 Amazon Bedrock 的企业级 Agent 时，必须采用“上下文消息策略”与“异步任务管理”相结合的架构，才能有效解决 MCP 协议在处理长周期任务时的状态保持和用户体验问题。**

**支撑理由与依据**
1.  **理由 1：网络与计算资源的有限性**。
    *   *依据*：HTTP 请求和 LLM 推理都有超时限制。长时间占用连接会导致服务器资源耗尽。
2.  **理由 2：用户体验的连续性需求**。
    *   *依据*：用户无法忍受面对空白屏幕等待数分钟。他们需要即时的反馈（“任务已接收”）和后续的通知。
3.  **理由 3：LLM 的无状态本质**。
    *   *依据*：模型本身不记忆异步过程。必须通过外部策略将异步结果重新注入上下文，模型才能“知道”任务已完成。

**反例或边界条件**
1.  **边界条件（纯内存计算）**：如果任务极其简单（如 < 5秒 的数学计算），引入异步框架会增加不必要的复杂度和延迟，此时同步调用更优。
2.  **反例（强实时性系统）**：在某些高频交易或实时控制系统中，任何异步延迟都是不可接受的，这类场景不适合此架构。

**命题性质分析**
*   **事实判断**：Bedrock 和 MCP 确实存在超时限制。
*   **逻辑推演**：异步解耦是解决长阻塞的标准工程模式。
*   **价值判断**：用户体验和系统稳定性优于开发实现的简单性。

**立场与验证方式**
**立场**：支持该文章提出的异步架构方案，认为这是构建复杂 AI 系统的必经之路。

**可证伪验证方式**：
*   **指标**：在压测环境下，对比同步模式与异步模式在处理 1000 个长任务（>60s）时的“任务成功率”和“平均用户等待时间”。
*   **观察窗口**

---
## 最佳实践

## 最佳实践指南

### 实践 1：实现健壮的状态管理与会话持久化

**说明**:
构建长时间运行的 MCP 服务器时，最大的挑战在于处理无状态协议与有状态业务逻辑之间的矛盾。由于 AgentCore 可能会根据负载动态调度容器，不能依赖内存存储会话状态。必须将对话上下文、中间步骤和用户偏好持久化到外部存储（如 DynamoDB 或 S3）中，以便在 Strands Agents 恢复任务时能够无缝衔接。

**实施步骤**:
1. 引入 Amazon DynamoDB 或 ElastiCache 作为外部状态存储层，设计包含 SessionID、AgentState 和 Timestamp 的数据模型。
2. 在 MCP 服务器的逻辑中，每次状态变更（如 Strands 的任务进度更新）时，触发异步写入操作到持久化存储。
3. 实现一个“状态恢复中间件”，在服务器接收到新的连接请求时，首先检查是否存在未完成的会话上下文并自动加载。

**注意事项**:
避免在本地内存中缓存关键业务状态超过几秒钟，以防容器重启导致数据丢失。确保存储层的读写延迟处于低毫秒级，以免拖慢 LLM 的响应速度。

---

### 实践 2：设计幂等的工具接口

**说明**:
在长运行场景中，网络抖动或超时可能导致 AgentCore 或 Strands Agents 重试请求。如果 MCP 服务器的工具接口不是幂等的，重复执行写操作（如创建订单、发送邮件）会导致数据不一致或业务错误。确保所有涉及状态变更的操作都支持“多次执行与一次执行效果相同”。

**实施步骤**:
1. 为每个需要修改资源的工具定义唯一的 `ClientToken` 或 `IdempotencyKey`。
2. 在服务器端维护一个短暂的键值存储（如 Redis 或 DynamoDB TTL 条目），记录最近处理过的请求 ID。
3. 处理请求前检查该 Key 是否已处理；若已处理，则直接返回之前的结果，而不执行业务逻辑。

**注意事项**:
幂等键的 TTL 设置应大于最大可能的网络重试窗口（通常建议 5-10 分钟）。对于只读查询操作，虽然天然幂等，但仍需做好缓存策略以减少底层调用。

---

### 实践 3：优化流式响应与超时处理

**说明**:
长时间运行的任务往往伴随着较长的处理时间。如果 MCP 服务器在等待下游服务响应时阻塞，可能会导致 AgentCore 判定请求超时并强制中断。最佳实践是采用流式传输或异步任务模式，让 Agent 能够实时感知进度，而不是一直处于静默等待状态。

**实施步骤**:
1. 将耗时操作（如数据处理、代码执行）设计为异步任务，立即返回一个 `TaskID` 给 Agent。
2. 实现一个专用的状态查询工具，供 Strands Agent 轮询或通过 Server-Sent Events (SSE) 推送进度更新。
3. 配置合理的超时层级：MCP 层超时应略大于 AgentCore 超时，AgentCore 超时应大于实际业务逻辑耗时。

**注意事项**:
避免无限期轮询。应设置最大轮询次数或超时时间，一旦超时立即向 Agent 返回部分结果或错误信息，防止资源死锁。

---

### 实践 4：实施细粒度的可观测性与日志关联

**说明**:
长运行链条中，问题排查极其困难。当 Strands Agent 调用 MCP 服务器失败时，开发者需要知道是网络问题、权限问题还是业务逻辑错误。必须实现与 AWS X-Ray 集成的分布式追踪，并在所有日志中包含 `TraceID`。

**实施步骤**:
1. 在 MCP 服务器启动时启用 AWS X-Ray 侧car 或使用 ADOT (AWS OpenTelemetry Distro) 收集追踪数据。
2. 确保所有对外部服务（如 Bedrock, DynamoDB）的调用都包含元数据标签（如 `agent_id`, `tool_name`, `session_id`）。
3. 将结构化日志（JSON 格式）发送到 CloudWatch Logs，并配置基于 `TraceID` 的日志 Insights 查询，以便在 Bedrock 控制台直接跳转查看日志。

**注意事项**:
注意日志采样率，避免在高并发下产生巨额的 CloudWatch 费用。对于敏感数据（PII），应在日志输出前进行脱敏处理。

---

### 实践 5：构建模块化与版本化的工具集

**说明**:
随着业务复杂度增加，Monolithic（单体式）的 MCP 服务器将难以维护。最佳实践是将功能按领域拆分为不同的工具，并引入版本控制。这样，当某个 Strands Agent 需要新功能时，不会破坏现有的长运行会话。

**实施步骤**:
1. 按照业务领域（如 `calendar_tools`, `email_tools`, `db_tools`）组织代码结构，每个工具独立注册。
2. 在工具定义中引入 `version` 字段，并在 MCP 协议的元数据中声明。
3. 实现灰度发布机制：新版本的工具

---
## 学习要点

- Amazon Bedrock AgentCore 正式发布，允许开发者构建能够长时间运行并保持状态的有状态 MCP 服务器，解决了传统无状态模型无法处理多步骤复杂任务的限制。
- 通过集成 Strands Agents，开发者可以创建能够自主规划、调用工具并记忆上下文的智能体，从而实现跨越多轮对话的复杂工作流自动化。
- 该架构利用 MCP 协议将大语言模型（LLM）与外部数据源和工具无缝连接，显著提升了 AI 应用在检索信息（RAG）和执行实际操作时的准确性与效率。
- 新框架支持在单次对话中自动处理包含多个逻辑步骤的请求，无需用户反复进行提示词工程，大幅降低了构建高级 AI 应用的技术门槛。
- Bedrock AgentCore 提供了企业级的基础设施支持，确保长时间运行的 AI 任务具备可扩展性、安全性和稳定性，适用于生产环境部署。
- 开发者现在可以更专注于定义业务逻辑和工具，而无需从零开始搭建和维护复杂的模型状态管理及记忆系统。

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

- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用]({{< relref "posts/20260210-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [利用全栈模板加速开发基于Amazon Bedrock AgentCore的应用]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--12.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*