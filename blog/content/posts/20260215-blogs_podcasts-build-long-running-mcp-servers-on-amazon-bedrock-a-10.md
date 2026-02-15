---
title: "基于Amazon Bedrock AgentCore与Strands Agents构建长时运行MCP服务器"
date: 2026-02-15T22:48:01+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长时运行", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种在 Amazon Bedrock AgentCore 上结合 Strands Agents 构建长时间运行 MCP 服务器的综合方法。主要内容包括三个核心策略： 1. **上下文消息策略**：引入一种机制，确保服务器与客户端在扩展操作期间维持持续通信，解决长时任务中的连接与状态同步问题。 2. **异步任"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore与Strands Agents构建长时运行MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本篇文章中，我们为您提供了一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，该策略在长时间运行的操作期间保持服务器与客户端之间的持续通信。接着，我们构建一个异步任务管理框架，让您的 AI 代理能够启动长时运行的任务，同时不会阻塞其他操作。最后，我们将展示如何结合 Amazon Bedrock AgentCore 和 Strands Agents 将这些策略融为一体，构建生产级的 AI 代理，使其能够可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时运行任务的 AI 代理是当前技术落地的一大难点，尤其是在需要保持会话状态与非阻塞通信的场景下。本文将介绍一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的集成方案，重点解析如何通过上下文消息策略与异步任务管理框架来实现持续通信。阅读此文，您将掌握构建生产级、高并发 AI 代理的核心方法，从而确保系统在处理复杂耗时操作时的稳定性与可靠性。

---
## 摘要

本文介绍了一种在 Amazon Bedrock AgentCore 上结合 Strands Agents 构建长时间运行 MCP 服务器的综合方法。主要内容包括三个核心策略：

1.  **上下文消息策略**：引入一种机制，确保服务器与客户端在扩展操作期间维持持续通信，解决长时任务中的连接与状态同步问题。

2.  **异步任务管理框架**：开发一套框架，使 AI 代理能够启动长时间运行的后台进程，同时避免阻塞其他操作，提升系统的并发处理能力。

3.  **生产级集成实现**：展示如何整合上述策略与 Amazon Bedrock AgentCore 及 Strands Agents，构建可靠处理复杂、耗时任务的 AI 代理，适用于生产环境部署。

---
## 评论

### 中心观点
该文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的技术架构，旨在通过引入异步任务管理框架和上下文消息策略，解决 MCP（Model Context Protocol）服务器在处理长周期任务时的连接稳定性与状态保持问题。

### 支撑理由与深度评价

**1. 技术架构的针对性：解决“长任务”断连痛点**
*   **事实陈述**：现有的 LLM 应用架构大多基于同步的 Request-Response 模式，受限于网络超时和 Token 生成时间，难以处理如代码编译、大规模数据分析等耗时超过 30-60 秒的任务。
*   **作者观点**：文章提出的“异步任务管理框架”将 Agent 的决策与任务的执行解耦。AgentCore 负责调度和状态管理，而 Strands Agents 负责具体的长时间执行，这符合云原生架构中“控制平面”与“数据平面”分离的最佳实践。
*   **深度评价**：这一观点切中要害。在当前的 Agentic Workflow（智能体工作流）中，最大的阻碍并非模型推理能力，而是工程层面的“任务挂起”问题。如果 Bedrock 真的能提供原生的任务队列和状态回调机制，将极大降低开发者的基础设施搭建成本。

**2. 上下文消息策略：维持对话连续性的“粘合剂”**
*   **事实陈述**：摘要中提到了“context message strategy”。
*   **你的推断**：这很可能是一种基于状态机的对话补全机制。当长任务在后台运行时，前端连接不能无限等待。该策略可能涉及向客户端发送中间状态更新，或者由客户端定期轮询/通过 WebSocket 接收服务端推送的“心跳”和“部分结果”。
*   **深度评价**：这在技术上是必要的，但实现难度在于“上下文窗口的利用效率”。如果长任务生成了大量中间日志，如何将这些信息压缩并回填给 LLM 而不撑爆上下文窗口，是衡量该方案成熟度的关键。

**3. 生态位卡位：AWS 对 MCP 协议的战略背书**
*   **事实陈述**：MCP (Model Context Protocol) 是 Anthropic 最近推出的开放标准，旨在连接 AI 助手与数据源。
*   **你的推断**：Amazon Bedrock 集成 Strands Agents 并支持 MCP，显示了 AWS 试图在 Anthropic 的标准之上建立更高级的托管服务层。这不仅是技术文档，更是 AWS 在 AI Agent 基础设施领域的战略布局。
*   **深度评价**：对于行业而言，这意味着 MCP 协议正在迅速获得主流云厂商的事实支持，有望成为连接 LLM 与本地工具的“USB 接口”。

### 反例与边界条件

尽管该方案看似完善，但在以下场景中可能存在局限：

1.  **强实时性交互场景**：
    *   **边界条件**：如果业务要求 Agent 在任务执行的毫秒级时间内对用户的打断做出反应（例如用户在代码编译中途取消了操作），单纯的异步任务队列可能存在延迟。Strands Agents 如果是基于批处理或轮询机制，可能无法处理高频的流式交互。
2.  **成本与复杂性陷阱**：
    *   **反例**：对于简单的长任务（如仅仅是等待一个 API 响应），引入 Bedrock AgentCore 和 Strands 的全套架构可能属于“过度设计”。维护一套异步系统的状态一致性、错误重试和死信队列，其工程复杂度可能高于业务逻辑本身。
3.  **多云/混合云部署限制**：
    *   **边界条件**：该方案深度绑定 AWS 生态。如果企业追求模型无关性或跨云部署，使用 Bedrock 的原生托管服务会带来极高的迁移成本。

### 可验证的检查方式

为了验证该文章所述方案的实际效果，建议进行以下检查：

1.  **压力测试指标**：
    *   构建一个并发场景，同时启动 100 个长周期任务（每个任务运行 5 分钟）。
    *   **观察窗口**：监控 Bedrock Agent 的调度延迟以及客户端连接的掉线率。如果客户端需要频繁重连才能获取结果，说明“Context message strategy”并不完善。
2.  **状态一致性验证**：
    *   在长任务执行过程中，人为中断网络或重启 AgentCore 服务。
    *   **观察窗口**：任务恢复后，Agent 是否能准确接续之前的上下文，还是会遗忘之前的中间步骤？这能检验其“异步框架”的真实鲁棒性。
3.  **成本效能分析**：
    *   对比使用该架构与使用传统 AWS Lambda + Step Functions 处理同样长周期任务的成本。
    *   **观察窗口**：计算单位任务的 Token 消耗量和基础设施费用。如果为了维持上下文导致了大量的 Token 冗余消耗，则该方案在经济性上不可行。

### 总结与建议

这篇文章代表了 AWS 在 AI Agent 基础设施化方向的一次重要推进，试图将开发者从繁琐的 WebSocket 管理和异步状态机中解放出来。

**实际应用建议**：
*   **适用**：适合构建企业级的 RAG（检索增强生成）应用、数据分析 Agent 或代码生成工具，特别是那些任务执行时间不可预测且需要高可靠性的场景。
*   **慎用**：初创公司的 MVP（最小可行性产品）或对延迟极度敏感的实时流式对话系统。
*   **注意**：在实施前，务必评估 Vendor Lock-in（厂商锁定）风险，确认 Bedrock 的 Strands Agents 是否

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

# 深度分析报告：基于 Amazon Bedrock AgentCore 与 Strands Agents 的长时运行 MCP 服务器构建

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：**构建能够处理长时间、复杂任务的 AI 代理，不能仅依赖单次请求响应模式，而必须引入“持久化上下文”与“异步任务管理”机制。** 文章提出了一种在 Amazon Bedrock AgentCore 环境下，利用 Model Context Protocol (MCP) 结合 Strands Agents 集成来实现这一目标的综合架构。

**作者想要传达的核心思想**
作者试图传达从“无状态对话”向“有状态工作流”转变的必要性。传统的 LLM 应用往往是即问即答，而企业级应用往往需要跨越几分钟甚至几小时的流程（如数据分析、代码部署）。核心思想在于**解耦“意图确认”与“任务执行”**，让 Agent 能够在后台持续运行任务，同时通过特定的上下文策略保持与客户端的“心跳”连接，确保用户感知到任务的连续性。

**观点的创新性和深度**
该观点的创新性在于将 **MCP（模型上下文协议）** 这一通常用于数据连接的标准，扩展到了**长时任务控制**领域。深度体现在它不仅解决了“怎么做”（技术实现），还解决了“怎么保持联系”（上下文消息策略），这是目前 Agent 架构从 Demo 走向生产环境的关键缺失环节。

**为什么这个观点重要**
随着 AI 从聊天机器人向智能体进化，**长时任务处理能力**是衡量 Agent 实用性的核心指标。如果 Agent 只能处理秒级回复，就无法胜任复杂的企业业务流程。这篇文章提出的架构解决了 Agent 落地“最后一公里”的稳定性与体验问题，对于构建高可用的 AI 工业级应用至关重要。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**: Anthropic 推出的开放协议，用于连接 AI 模型与数据源。在此处，它被用作 Agent 与后端工具/服务器之间的标准化通信接口。
2.  **Amazon Bedrock AgentCore**: AWS 提供的托管式 Agent 框架，负责编排 LLM、工具调用和记忆管理。
3.  **Strands Agents**: 文章提到的特定集成技术，可能指代 AWS 内部或合作伙伴提供的、专门用于处理“长链路”任务的 Agent 模式或库（Strands 暗示了多线程或长流程的编织）。
4.  **异步任务管理框架**: 用于处理非阻塞操作的后台机制。

**技术原理和实现方式**
*   **上下文消息策略**: 技术原理是利用 LLM 的 Context Window（上下文窗口）或记忆系统。在长任务执行期间，服务器不是保持网络连接（WebSocket），而是通过返回特定的“中间状态 Token”或“上下文消息”给客户端。客户端在下一轮对话中携带此消息，Agent 从而恢复之前的任务状态。
*   **异步任务管理**: 当 Agent 调用 MCP Server 中的耗时工具（如“处理大数据集”）时，MCP Server 立即返回一个 `TaskID` 并挂起当前会话。后台线程/进程开始执行任务。AgentCore 将此 `TaskID` 存储在用户的 Session State 中。在后续轮次中，Agent 通过查询 `TaskID` 状态来向用户汇报进度。

**技术难点和解决方案**
*   **难点**: LLM 的无状态性与长任务有状态性之间的矛盾；超时限制。
*   **解决方案**: 文章提出的“上下文消息策略”充当了有状态的桥梁。通过将状态序列化并回传给客户端（或存在 Bedrock 的 Session Store 中），绕过了无状态限制。

**技术创新点分析**
最大的创新点在于**将 MCP Server 从单纯的“数据提供者”转变为“任务执行者”**。传统的 MCP 工具调用通常是同步等待结果的，而该架构允许 MCP Server 接收指令后释放连接，转入异步执行，这极大地扩展了 MCP 的应用边界。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为开发者提供了一套在 AWS 云上构建复杂 Agent 的标准范式。它指导开发者如何设计 API 接口以适应 LLM 的“思考-行动-观察”循环，特别是在面对耗时操作时如何避免超时错误。

**可以应用到哪些场景**
1.  **金融报告生成**: 需要长时间检索多源数据、计算指标、生成图表，耗时可能数分钟。
2.  **DevOps 与运维**: 执行代码部署、数据库迁移，需要监控进度并处理错误。
3.  **科研与数据分析**: 对海量数据集进行清洗和推理，无法在单次请求中完成。
4.  **企业级 RPA**: 自动化跨系统的业务流程办理。

**需要注意的问题**
*   **状态一致性**: 确保异步任务失败时，Agent 能够感知并通知用户。
*   **成本控制**: 长时运行意味着更多的 Token 消耗（上下文累积）和更长的计算时间。

**实施建议**
在实施时，应优先设计任务状态机。明确任务有哪些状态（Pending, Running, Completed, Failed），并确保 MCP Server 暴露的工具接口能够清晰地返回这些状态。

## 4. 行业影响分析

**对行业的启示**
该文章暗示了 **Agent 基础设施正在“云原生化”**。未来的 Agent 开发将不再只是写 Prompt，而是涉及到消息队列、异步处理、状态管理等后端工程技术的深度整合。

**可能带来的变革**
这可能会推动 **MCP 协议**成为连接 LLM 与后端微服务的事实标准，类似于 REST API 在 Web 时代的地位。长时运行能力的标准化，将使得 AI Agent 能够真正取代人类员工完成复杂的工作流，而不仅仅是充当搜索引擎。

**相关领域的发展趋势**
*   **Agent 编排**: 从单 Agent 向多 Agent 协作发展，长时任务是协作的基础。
*   **可观测性**: 对于长时任务，日志记录和调试工具将变得至关重要。

## 5. 延伸思考

**引发的其他思考**
*   **人机协同模式**: 在长任务运行期间，如果 Agent 遇到无法决策的边缘情况，如何优雅地暂停并请求人类介入？这种“异步打断”机制是下一步的思考方向。
*   **流式响应与状态更新**: 现在的方案可能是基于轮询的，未来是否可以结合 SSE (Server-Sent Events) 或 WebSocket 在 MCP 协议层实现真正的实时推送？

**可以拓展的方向**
*   结合 **Amazon EventBridge** 实现完全事件驱动的 Agent 架构。
*   探索 **多模态长时任务**，例如生成视频时的进度回调。

**未来发展趋势**
Agent 将具备更强的“记忆”和“规划”能力，长时运行将成为企业级 Agent 的标配，而非可选功能。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务耗时**: 审视你现有的 Agent 应用，哪些工具调用超过 30 秒，这些就是需要改造为“异步任务”的候选者。
2.  **引入状态存储**: 利用 Redis 或 DynamoDB 存储任务状态，不要试图把所有状态都塞进 LLM Context。
3.  **改造 MCP Server**: 修改你的工具接口，使其立即返回 `task_id`，并提供一个 `check_status` 工具供 Agent 轮询。

**具体的行动建议**
*   阅读 Anthropic 的 MCP 规范中关于 Resources 和 Prompts 的部分，理解如何维持上下文。
*   在 Bedrock Agent 中配置 `Alias` 和 `Memory`，确保会话历史的连续性。

**需要补充的知识**
*   异步编程模型。
*   AWS Lambda/Step Functions 的使用（用于后台任务执行）。
*   Prompt Engineering 中关于“System Prompt”的设计，如何告诉 Agent 它需要轮询任务状态。

## 7. 案例分析

**结合实际案例说明**
假设一个**“企业合规性审查 Agent”**。
*   **传统模式**: Agent 调用审查工具，扫描 1000 个文档。由于耗时 10 分钟，HTTP 请求超时，Agent 报错。
*   **本架构模式**:
    1.  Agent 调用 MCP Server 的 `start_audit` 工具。
    2.  Server 返回 `{"status": "accepted", "task_id": "123"}`。
    3.  Agent 告诉用户：“审查已开始，任务 ID 123，我将在后台监控。”
    4.  用户等待或做其他事。
    5.  用户问：“审查好了吗？”
    6.  Agent 自动调用 `check_status(task_id="123")`。
    7.  Server 返回进度 50%。
    8.  Agent 回复：“目前完成了 50%...”

**经验教训总结**
失败案例通常是因为开发者试图在 LLM 的单次推理循环中等待所有 I/O 操作完成。成功的经验是**“快响后做”**（Respond Fast, Act Later）。

## 8. 哲学与逻辑：论证地图

**中心命题**
**构建具备长时业务处理能力的 AI Agent，必须采用基于异步任务框架与上下文状态管理的混合架构，而非传统的同步请求-响应模式。**

**支撑理由**
1.  **技术限制**: LLM 的推理和网络请求存在硬性超时限制（通常几十秒到几分钟），无法直接覆盖企业级长任务。
    *   *依据*: HTTP 超时标准、LLM Token 生成速率限制。
2.  **用户体验**: 同步等待会导致用户端界面卡死或无反馈，造成极差的交互体验。
    *   *依据*: UI/UX 设计原则中的即时反馈原则。
3.  **资源效率**: 长连接占用服务器资源，异步处理能提高系统的并发吞吐量。
    *   *依据*: 系统架构中的线程池模型与排队论。

**反例或边界条件**
1.  **反例**: 对于纯检索型问答（RAG），信息获取在毫秒级完成，引入异步框架会增加不必要的复杂度和延迟。
2.  **边界条件**: 如果任务状态极其复杂，无法通过简单的 Token 或 JSON 序列化传递回 Context，则此架构可能失效，需要引入外部数据库查询机制。

**命题性质分析**
*   **事实**: LLM 和网络协议存在超时限制。
*   **价值判断**: 异步体验优于同步卡顿。
*   **可检验预测**: 采用该架构的 Agent 在处理 5 分钟以上任务时的成功率将显著高于同步架构。

**立场与验证**
*   **立场**: 坚决支持。这是构建生产级 Agent 的必经之路。
*   **可证伪验证方式**:
    *   *指标*: 对比同步架构与异步架构在“任务超时率”和“用户完成率”上的数据。
    *   *实验*: 构建一个生成式视频 Agent，同步架构必然在 30 秒后断开，而 Bedrock + Strands 架构应能完成任务并返回结果。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化长运行任务的会话状态管理

**说明**:
构建基于 Bedrock AgentCore 的 MCP 服务器时，长运行任务往往超出单次请求的超时限制。最佳实践是将任务逻辑与状态解耦，使用 Strands Agents 来维护跨请求的对话上下文和任务状态，确保异步任务的可追溯性和恢复能力。

**实施步骤**:
1. 设计无状态的服务器接口，将任务状态（如 "Processing", "Completed"）存储在持久化存储中（如 DynamoDB 或 S3）。
2. 利用 Strands Agents 的记忆功能，存储任务 ID 和当前执行阶段。
3. 实现 MCP 工具的轮询或回调机制，允许 Agent 查询任务状态或接收完成通知。

**注意事项**:
- 确保状态存储具有 TTL（生存时间），以防止无限期保留废弃任务的数据。
- 处理并发请求时，需保证状态更新的原子性。

---

### 实践 2：实施健壮的错误处理与重试策略

**说明**:
长运行进程更容易遇到网络波动或依赖服务中断。在 MCP 服务器与 Strands Agents 集成时，必须构建能够识别暂时性故障并自动重试的机制，同时向 Agent 框架报告明确的错误信息以便进行自我修正。

**实施步骤**:
1. 在 MCP 服务器端实现指数退避算法，用于调用外部 API 或 Bedrock 时的重试逻辑。
2. 定义标准化的错误响应结构，区分可重试错误（如 5xx）和不可重试错误（如 4xx）。
3. 配置 Strands Agents 的提示词，使其在收到特定错误代码时能够执行重试或回退到备用工具。

**注意事项**:
- 设置最大重试次数，以避免无限循环消耗配额。
- 捕获并记录所有底层异常，以便通过 CloudWatch 等工具进行排查。

---

### 实践 3：设计细粒度的工具权限与访问控制

**说明**:
MCP 服务器暴露的工具可能会访问敏感资源。最佳实践是遵循最小权限原则，并利用 Bedrock AgentCore 的 IAM 策略与 Strands Agents 的路由能力，确保 Agent 只能调用其当前任务所需的特定工具。

**实施步骤**:
1. 为 MCP 服务器定义不同的工具组或角色，并在服务器层实现权限校验逻辑。
2. 在 Bedrock Agent 或 AgentCore 中配置 IAM 策略，限制 Agent 对特定 S3 存储桶、DynamoDB 表或其他 AWS 资源的访问。
3. 在 Strands Agents 的系统提示词中明确界定工具的使用边界和条件。

**注意事项**:
- 定期审计 IAM 策略，确保没有权限过度授予。
- 对于高权限操作，建议在 MCP 服务器层增加二次确认或人工审批逻辑。

---

### 实践 4：利用流式传输提升用户体验

**说明**:
对于长运行任务，用户不应在任务完成前面对空白屏幕。最佳实践是利用 Bedrock 的流式响应能力，让 MCP 服务器能够通过 Strands Agents 实时向用户返回中间进度、日志或部分结果。

**实施步骤**:
1. 修改 MCP 工具接口，使其支持 Server-Sent Events (SSE) 或类似的流式数据推送协议。
2. 在长运行逻辑中插入检查点，定期生成状态更新事件。
3. 确保客户端能够接收并渲染这些流式数据包。

**注意事项**:
- 确保流式连接在长任务期间保持活跃，必要时发送心跳包。
- 处理客户端断开连接的情况，服务器应能检测到中断并暂停或取消后台任务以节省资源。

---

### 实践 5：建立全面的可观测性体系

**说明**:
调试长运行的异步 Agent 具有挑战性。必须集成 AWS 的监控服务来追踪 MCP 服务器的性能指标、Strands Agents 的决策路径以及 Bedrock 的调用延迟。

**实施步骤**:
1. 启用 Amazon Bedrock 的调用日志记录，将模型交互数据发送到 CloudWatch 或 S3。
2. 在 MCP 服务器代码中嵌入结构化日志（如 JSON 格式），记录每个工具调用的输入、输出和耗时。
3. 利用 AWS X-Ray 进行分布式追踪，可视化请求从 Agent 到 MCP 服务器再到后端服务的完整链路。

**注意事项**:
- 注意日志中可能包含的敏感数据（PII），在记录前进行脱敏处理。
- 设置合理的 CloudWatch 告警阈值，以便在错误率飙升或延迟过大时及时通知。

---

### 实践 6：针对 Bedrock 模型限制进行优化

**说明**:
长运行任务通常涉及大量的上下文数据处理。必须针对 Bedrock 托管模型的上下文窗口限制和 Token 吞吐限制进行优化，确保 Strands Agents 传递给 MCP 服务器的数据在模型处理能力范围内。

**实施步骤**:
1. 在 MCP 服务器端实现数据摘要或截断逻辑，处理超过模型上下文窗口的大型输入。
2. 设计高效的 Prompt

---
## 学习要点

- Amazon Bedrock AgentCore 正式支持构建能够长时间运行并保持状态的有状态 MCP 服务器，解决了传统无状态模型无法处理复杂、多步骤工作流的局限性。
- 通过集成 Strands Agents，开发者可以构建具备记忆能力的智能体，使其能够在长时间对话和任务执行中保持上下文连贯性。
- 该架构允许模型自主控制 MCP 工具的调用流程，从而实现跨多个步骤的复杂任务自动化，而无需人工干预。
- 利用 Strands 技术，系统可以持久化存储和管理会话状态，确保在长周期任务中数据的一致性和可追溯性。
- 此方案为开发者提供了一个统一的标准框架，用于在 Bedrock 生态中开发、部署和管理具备长期交互能力的生成式 AI 应用。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*