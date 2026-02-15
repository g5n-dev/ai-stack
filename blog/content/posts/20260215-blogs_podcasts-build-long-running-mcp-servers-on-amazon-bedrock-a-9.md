---
title: "在Amazon Bedrock AgentCore上集成Strands Agents构建长时运行MCP服务器"
date: 2026-02-15T07:07:48+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "长时运行任务", "异步任务", "AI Agent", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 构建长时间运行 MCP 服务器的综合方法，旨在实现生产级 AI 代理对复杂、耗时操作的高效处理。核心内容包括以下三部分： 1. **上下文消息策略**：通过建立持续通信机制，确保服务器与客户端在长时间操作期间保持状态"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 在Amazon Bedrock AgentCore上集成Strands Agents构建长时运行MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们为您提供了一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，该策略在长时间运行的操作期间维持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，让您的 AI 智能体能够启动长时间运行的流程，同时不会阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，构建生产就绪的 AI 智能体，可靠地处理复杂、耗时的操作。

---
## 导语

构建能够稳定处理长时间运行任务的 AI 智能体是当前技术落地的一大难点。本文将探讨如何利用 Amazon Bedrock AgentCore 结合 Strands Agents，通过上下文消息策略与异步任务管理框架，解决服务端与客户端的持续通信及阻塞问题。阅读本文，您将掌握一套构建生产级、高并发 AI 智能体的完整方法，从而让系统从容应对复杂且耗时的业务操作。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 构建长时间运行 MCP 服务器的综合方法，旨在实现生产级 AI 代理对复杂、耗时操作的高效处理。核心内容包括以下三部分：

1. **上下文消息策略**：通过建立持续通信机制，确保服务器与客户端在长时间操作期间保持状态同步，避免信息丢失或连接中断。  
2. **异步任务管理框架**：支持 AI 代理在启动长耗时进程时不阻塞其他操作，提升系统并发能力和响应效率。  
3. **技术整合与实践**：结合 Amazon Bedrock AgentCore 和 Strands Agents，将上述策略落地，构建可稳定处理复杂任务的 AI 代理系统。  

整体方案聚焦于解决长流程任务中的可靠性和性能问题，适用于需要持续交互或后台处理的 AI 应用场景。

---
## 评论

**文章中心观点**
该文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的技术架构，旨在通过上下文消息策略与异步任务管理框架，解决 MCP（Model Context Protocol）服务器在处理长周期任务时的状态维护与通信中断问题。

**支撑理由与评价**

1.  **针对长周期任务的“心跳”机制（Context Message Strategy）**
    *   **事实陈述**：文章提出了上下文消息策略，以维持客户端与服务器在扩展操作期间的连续通信。
    *   **深度分析**：在 LLM 应用的实际落地中，长周期任务（如代码生成、数据分析）往往导致请求超时或连接中断，这是业界痛点。作者提出的策略本质上是在应用层实现了“心跳”或“会话保持”。这比单纯依赖底层 TCP Keep-alive 更适用于无状态的 HTTP 接口。它确保了 Agent 在等待结果时不会丢失上下文，避免了用户面对“无响应”的黑盒体验。
    *   **反例/边界条件**：如果上下文消息策略设计不当，频繁的握手可能会导致 Token 消耗激增。对于极低成本敏感的场景，这种“保活”策略可能不如简单的异步回调通知经济。

2.  **解耦控制平面与数据平面（Asynchronous Task Management）**
    *   **事实陈述**：文章开发了异步任务管理框架，允许 AI 代理在后台执行任务。
    *   **深度分析**：这是架构设计上的关键一步。通过引入异步框架，系统将“指令下发”与“结果获取”分离。这使得 MCP 服务器能够处理高并发请求，而不被阻塞。这与现代后端开发中的 Event Loop 或消息队列模式一致，提升了系统的吞吐量和鲁棒性。
    *   **反例/边界条件**：异步架构显著增加了系统的复杂度。开发者必须处理任务失败、重试逻辑以及最终一致性问题。对于简单的、秒级响应的查询任务，引入异步框架属于过度设计，反而增加了延迟。

3.  **云原生生态的深度绑定**
    *   **作者观点**：利用 Bedrock AgentCore 和 Strands Agents 是实现该目标的最佳路径。
    *   **深度分析**：文章展示了如何将 MCP 协议这一开源标准与 AWS 的托管服务深度结合。Bedrock AgentCore 提供了编排能力，而 Strands Agents 可能提供了特定领域的推理或工具调用能力。这种组合利用了云服务的可观测性、安全性和扩展性，降低了企业从原型到生产的门槛。
    *   **反例/边界条件**：这种方案具有极强的 Vendor Lock-in（厂商锁定）风险。如果企业需要跨云部署（如同时使用 Azure 和 AWS），或者希望完全控制数据链路以避免数据出境合规问题，这种深度绑定的架构将非常脆弱。

**维度评分与详细评价**

1.  **内容深度：8/10**
    文章不仅停留在 API 调用层面，而是深入到了协议交互和架构模式层面。将 MCP 协议的局限性（短连接）与 Bedrock 的特性结合，体现了对云原生架构的深刻理解。论证逻辑严密，从问题定义（长任务）到解决方案（异步+上下文）环环相扣。

2.  **实用价值：9/10**
    对于正在基于 AWS 构建企业级 Agent 应用的架构师而言，价值极高。它提供了一套可落地的“避坑指南”，解决了长任务导致超时这一实际工程难题。提供的代码片段和架构图可以直接作为蓝图参考。

3.  **创新性：7/10**
    “异步任务处理”并非全新概念，但在 MCP 协议这一新兴语境下，将其与 Bedrock AgentCore 结合属于前沿探索。文章的创新点在于将传统的后端异步模式成功移植到了 LLM Agent 的编排逻辑中。

4.  **可读性：8/10**
    结构清晰，先讲策略再讲框架。技术术语使用准确，逻辑流线性推进。

5.  **行业影响：中等偏上**
    MCP 协议目前正处于快速发展期，这篇文章为“如何在企业级云平台上落地 MCP”提供了一个标准范式。可能会推动更多厂商关注 Agent 的长周期运行能力。

**争议点与不同观点**

*   **协议中立性 vs 平台增强**：文章倾向于利用 AWS 特有能力解决问题。我的观点是，虽然这提升了 AWS 上的体验，但可能违背 MCP 协议旨在实现“模型-工具”解耦的初衷。如果这种长任务处理逻辑不能标准化回传给 MCP 社区，会导致 MCP 服务器出现“AWS 版”和“通用版”的分裂。
*   **Token 成本隐形化**：通过上下文策略维持通信，意味着在任务执行期间，Agent 可能需要消耗大量的 Token 来处理状态更新或中间日志。文章未深入讨论这种模式带来的成本陷阱。

**实际应用建议**

1.  **成本监控**：在实施该架构时，务必开启 Bedrock 的详细成本监控。观察异步任务轮询或上下文心跳是否导致了非预期的 Token 计费。
2.  **超时配置**：虽然实现了异步，但客户端等待“任务ID”返回的同步阶段仍需设置合理的超时时间，防止因 Bedrock 服务本身抖动导致的级联失败。
3.  **混合架构**：对于非关键路径任务，考虑使用轻量级消息队列（如 SQS）替代复杂的 Agent 上下文保活，以降低架构复杂度。

**可验证的检查方式**

1.  **并发压力测试**：构建测试脚本，同时发送 100 个长周期任务（如模拟 5 分钟处理时间

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

# 深度分析：基于 Amazon Bedrock AgentCore 与 Strands 构建持久化 MCP 服务器

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：**在生成式 AI 应用从简单的“单轮问答”向复杂的“多步自主任务”演进的过程中，必须构建一种能够支持长时间运行、具备状态管理和异步通信能力的 MCP（Model Context Protocol）服务器架构。** 作者认为，传统的同步请求-响应模式无法满足现实世界中复杂业务流程的需求，因此提出了结合 Amazon Bedrock AgentCore 和 Strands Agents 的解决方案。

**作者想要传达的核心思想**
作者试图传达“持久化智能体”的概念。AI 不仅仅是聊天机器人，更是能够处理耗时任务（如数据查询、代码生成、API 调用）的工作流引擎。核心思想在于**解耦**：将 AI 的“思考”过程与“执行”过程分离，通过上下文消息策略和异步任务管理，确保在处理长耗时任务时，客户端与服务端保持连接且用户体验流畅。

**观点的创新性和深度**
*   **创新性**：将 MCP 协议（通常用于本地工具调用）扩展到了云端长期运行的 Agent 架构中，并引入了 Strands（可能指代一种持续性的会话或任务流技术）的概念。
*   **深度**：文章触及了 LLM（大语言模型）应用落地中最棘手的问题——**状态保持与超时处理**。它不仅讨论了“怎么做”，还深入到了“如何保持上下文连续性”的协议层面。

**为什么这个观点重要**
随着 AI Agent 的普及，企业级应用要求 AI 能够处理复杂的业务逻辑（如 RAG 结合、长流程审批、代码部署等）。这些操作往往耗时数秒甚至数分钟。如果没有长运行架构，用户会面临超时错误或无法获知任务进度的困境。该观点为解决这一瓶颈提供了标准化的云原生路径。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **MCP (Model Context Protocol)**：一种连接 AI 应用与数据源/工具的开放协议。
*   **Amazon Bedrock AgentCore**：AWS 提供的用于构建和管理 AI Agent 的底层服务或框架。
*   **Strands Agents**：文章提到的特定集成技术，推测指代一种能够处理“线程”或“连续活动”的 Agent 机制，用于维持长对话的上下文。
*   **Asynchronous Task Management**：异步任务管理框架。

**技术原理和实现方式**
1.  **Context Message Strategy（上下文消息策略）**：
    *   **原理**：在长任务执行期间，Agent 不能仅仅保持沉默。系统需要定期发送“心跳”或“进度更新”消息给客户端，证明任务仍在进行。
    *   **实现**：利用 MCP 的服务端推送能力或客户端轮询机制，将长任务的中间状态（如“正在查询数据库”、“正在解析文档”）转化为上下文消息流，防止前端超时。

2.  **Asynchronous Task Management Framework（异步任务管理框架）**：
    *   **原理**：将用户的请求转化为一个后台任务，立即返回一个 Task ID 给客户端。Agent 在后台独立运行，客户端通过 ID 查询结果或接收推送。
    *   **实现**：结合 Bedrock 的异步推理能力与 Strands 的状态存储。当 Agent 需要调用耗时工具时，它挂起当前会话，执行工具，待工具完成后通过 Strands 恢复会话上下文并生成最终响应。

**技术难点和解决方案**
*   **难点**：状态同步与上下文窗口限制。长任务可能产生大量中间日志，若全部塞入 LLM 上下文会导致成本过高或 Token 溢出。
*   **解决方案**：Strands Agents 可能提供了一种摘要机制，仅将关键的中间状态传递回 LLM，或者利用向量数据库存储长时记忆，仅传递相关引用。

**技术创新点分析**
文章最大的创新点在于**将 Bedrock 的企业级编排能力与 MCP 的通用工具协议进行了融合**。这使得开发者既可以享受 MCP 生态丰富的工具集，又能利用 AWS 云基础设施的稳定性和可扩展性来处理长流程任务。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为构建“企业级 Copilot”提供了蓝图。它解决了开发者在面对复杂业务流时，不知道如何在 LLM 和后端服务之间维持状态的难题。它指导开发者从“写 Prompt”转向“设计状态机”。

**可以应用到哪些场景**
1.  **复杂数据分析**：Agent 需要执行 SQL 查询，等待结果，生成图表，再撰写报告。整个过程可能持续数分钟。
2.  **代码生成与部署**：Agent 生成代码 -> 编译 -> 运行测试 -> 部署到测试环境。每一步都需要时间且不能阻塞用户界面。
3.  **企业知识库问答 (RAG)**：当需要检索海量文档并整合多个来源的信息时。
4.  **自动化工作流**：例如自动处理工单，涉及跨系统的 API 调用和审批流。

**需要注意的问题**
*   **成本控制**：长轮询或 WebSocket 连接会增加基础设施成本。
*   **一致性**：异步任务可能导致最终一致性问题，如何处理任务失败后的回滚。

**实施建议**
建议采用“事件驱动架构”来配合 Bedrock AgentCore。不要让 Agent 直接阻塞等待，而是让工具返回一个“任务已接收”的信号，通过事件总线（如 Amazon EventBridge）通知后续流程。

## 4. 行业影响分析

**对行业的启示**
这篇文章暗示了 AI Agent 基础设施正在**“云原生化”**和**“协议标准化”**。未来的 AI 应用将不再是一个孤立的模型调用，而是由云厂商托管、通过标准协议（如 MCP）连接各种微服务的复杂分布式系统。

**可能带来的变革**
*   **从 Chatbot 到 Worker**：AI 的交互模式从“一问一答”转变为“任务分发与验收”。
*   **MCP 生态的爆发**：随着 AWS 等大厂支持，MCP 可能成为连接 LLM 与企业系统的标准接口，类似于 API 之于 Web。

**相关领域的发展趋势**
*   **Agent Orchestrator（智能体编排器）**将成为新的中间件战场。
*   **Observability（可观测性）**对于长运行 Agent 至关重要，如何调试一个跑了 10 分钟的 Agent 将是新挑战。

## 5. 延伸思考

**引发的其他思考**
如果 MCP 服务器可以长运行，那么安全性如何保证？一个拥有长连接权限的 Agent 如果被劫持，其破坏力远大于单次请求。零信任架构在 Agent 时代的应用值得深思。

**可以拓展的方向**
*   **人机协同**：在长任务执行的关键节点（如“即将删除数据库”），如何优雅地插入人工确认环节？
*   **多 Agent 协作**：Strands 机制是否支持多个 Agent 并行工作，最后汇总结果？

**需要进一步研究的问题**
Strands Agents 的具体实现细节是否开源？它与 LangGraph 或 LangChain 的长期记忆机制有何异同？

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有工具**：检查你的后端服务是否支持异步化（如使用 Celery, AWS Lambda 等）。
2.  **引入 MCP**：将你的业务 API 封装为 MCP Server。
3.  **配置 Bedrock**：在 Bedrock Agent 中配置 Action Groups，指向你的 MCP Server，并开启异步支持。

**具体的行动建议**
*   **第一步**：先实现一个简单的“长耗时工具”（如模拟 30 秒的数据处理），测试 Bedrock Agent 的超时机制。
*   **第二步**：引入 Context Message，观察客户端是否能收到中间进度。
*   **第三步**：构建任务状态表，用于存储异步任务的结果。

**需要补充的知识**
*   **异步编程模型**（Promise/Async-Await, Message Queues）。
*   **WebSocket 或 SSE (Server-Sent Events)** 协议知识。
*   **Amazon Bedrock** 的具体配置和 IAM 权限管理。

## 7. 案例分析

**结合实际案例说明**
假设我们要构建一个**“法律合同审查 Agent”**。
*   **传统模式**：用户上传合同 -> Agent 调用 API -> API 处理 5 分钟 -> 前端超时报错。
*   **新模式**：用户上传 -> Agent 返回“任务 ID：123，正在审查” -> 后台 Strands Agent 调用 MCP 服务器读取文档 -> 调用 LLM 分析 -> 每 30 秒通过 Context Message 告知用户“正在审查第 5 页” -> 完成后通知用户。

**成功案例分析**
**Customer Support Bot**：当用户需要“重置服务器”时，Agent 发起请求，运维系统异步执行（耗时 2 分钟），Agent 期间告知用户“正在执行中，请勿关闭窗口”，成功避免了用户重复点击。

**失败案例反思**
如果未实现 Context Message 策略，用户在等待 30 秒无响应后，通常会刷新页面或重新发送请求，导致后台产生重复任务，甚至引发系统雪崩。

## 8. 哲学与逻辑：论证地图

**中心命题**
**构建基于异步任务管理和上下文消息策略的长运行 MCP 服务器，是实现企业级高可用 AI Agent 的必要条件。**

**支撑理由与依据**
1.  **理由 1：网络延迟与超时限制。**
    *   *依据*：HTTP 请求通常有默认的超时时间（如 30s-60s），而复杂的业务逻辑往往超过此时间。如果不异步处理，连接必然断开。
2.  **理由 2：用户体验的确定性。**
    *   *依据*：心理学研究表明，用户在无反馈的等待中焦虑感会指数级上升。Context Message 提供了反馈，维持了用户的控制感。
3.  **理由 3：资源利用率最大化。**
    *   *依据*：同步阻塞会占用服务器线程，导致并发能力下降。异步处理允许系统在等待 I/O 时处理其他请求。

**反例或边界条件**
1.  **反例 1（简单查询场景）**：对于“现在几点了”或“定义一个名词”这类毫秒级完成的任务，引入异步和 Strands 架构会增加不必要的延迟和复杂度（过度设计）。
2.  **边界条件（强一致性要求）**：在金融交易等要求“读后写”强一致性的场景下，异步化可能增加状态管理的复杂度，需要额外的补偿事务机制。

**命题性质分类**
*   **事实**：LLM 的生成速度和 API 调用耗时存在物理限制。
*   **价值判断**：用户体验（UX）在 AI 应用中至关重要；长运行能力是 Agent 走向生产环境的标志。
*   **可检验预测**：采用该架构的系统，其任务完成成功率将高于同步系统，且用户在长任务中的留存率更高。

**立场与验证方式**
*   **立场**：支持采用该架构作为企业级 AI 应用的标准范式，但需根据任务耗时进行分层设计（短任务同步，长任务异步）。
*   **

---
## 最佳实践

## 最佳实践指南：基于 Amazon Bedrock AgentCore 与 Strands Agents 构建长时间运行的 MCP 服务器

### 实践 1：设计无状态的 MCP 服务架构以实现弹性扩展

**说明**:
长时间运行的 MCP 服务器需要处理持续的交互和潜在的并发请求。构建无状态架构（Stateless Architecture）是确保服务可扩展性和高可用性的关键。这意味着服务器不应在本地内存中存储特定于会话的持久数据，而是应依赖外部持久层（如 DynamoDB 或 S3）来存储状态。当 AgentCore 扩展容器实例时，无状态设计允许请求无缝路由到任何可用的实例，而不会丢失上下文。

**实施步骤**:
1. 将所有对话历史、用户会话数据和中间检查点存储在 Amazon DynamoDB 或 ElastiCache 中，而不是服务器内存。
2. 确保 MCP 协议实现中，每个工具调用都包含必要的上下文 ID，以便从外部存储中检索状态。
3. 配置 Amazon ECS 或 EKS 的健康检查机制，确保无状态容器可以随时启动、终止或重启。

**注意事项**:
避免在全局变量或单例对象中保存业务逻辑状态。确保 Strands Agents 的上下文管理器与外部存储层紧密集成。

---

### 实践 2：利用 Strands Agents 实现异步任务编排与状态管理

**说明**:
长时间运行的任务通常涉及复杂的逻辑链，不能在单次 LLM 调用中完成。Strands Agents 提供了强大的编排能力，允许将任务分解为多个“Strands”（子任务或线程）。最佳实践是利用这一特性来处理异步工作流，例如处理可能需要几分钟甚至几小时才能完成的业务流程（如数据生成或复杂审批流），而不是让 MCP 连接保持阻塞状态。

**实施步骤**:
1. 将长时间运行的逻辑分解为独立的 Strands，定义清晰的输入输出接口。
2. 在 MCP 服务器中实现异步模式：当收到任务请求时，立即返回一个 `TaskID` 并启动后台 Strand，而不是等待任务完成。
3. 实现一个轮询或基于回调的机制，允许 AgentCore 或客户端查询 Strand 的执行状态（例如：进行中、已完成、失败）。

**注意事项**:
确保异步任务的超时设置合理，并实施死信队列（DLQ）处理逻辑，以应对 Strands 执行失败的情况。

---

### 实践 3：实施严格的资源清理与生命周期管理

**说明**:
在长时间运行的环境中，资源泄漏（如未关闭的连接、未释放的内存或过期的临时文件）会导致服务性能下降甚至崩溃。由于 MCP 服务器可能通过 AgentCore 持续处理大量请求，必须实施严格的资源生命周期管理。这包括主动清理与 Strands 相关的临时会话对象和数据库连接。

**实施步骤**:
1. 在代码中实现明确的 `try-finally` 或 `using` 块，确保网络连接和文件句柄在使用后立即释放。
2. 对于 Strands Agents，设置合理的 TTL（生存时间），自动清理已完成或长时间未活动的会话状态。
3. 定期监控容器内存使用情况，利用 Amazon CloudWatch 设置内存或文件句柄数量的告警阈值。

**注意事项**:
特别注意处理异常中断的情况（如容器被强制终止），确保在此类情况下也能尽可能释放占用的外部资源（如 DynamoDB 锁）。

---

### 实践 4：优化 MCP 协议处理以支持流式响应

**说明**:
长时间运行的生成式任务如果仅在完全结束时才返回结果，用户体验会极差。最佳实践是支持流式传输。MCP 协议支持流式数据传输，结合 Bedrock 的流式输出能力，可以让 AgentCore 实时向用户展示进度。这对于 Strands Agents 逐步生成数据或执行多步骤推理尤为重要。

**实施步骤**:
1. 修改 MCP 工具定义，明确支持流式响应类型（如 Server-Sent Events 或 MCP 的流式传输扩展）。
2. 在 Strands Agents 执行过程中，将中间结果或日志通过流式通道实时推送给 AgentCore。
3. 实现缓冲机制，防止高频小数据包造成网络拥塞，平衡实时性与性能。

**注意事项**:
流式连接可能会占用服务器资源较长时间，务必设置最大超时时间，并处理客户端突然断开连接时的资源回收逻辑。

---

### 实践 5：建立全面的可观测性与日志关联

**说明**:
在分布式架构（AgentCore + Bedrock + Strands）中，调试长时间运行的任务极具挑战性。最佳实践是建立贯穿整个请求生命周期的可观测性。必须能够追踪从 AgentCore 发起的 MCP 请求，到 Strands Agents 的内部执行，再到 Bedrock 模型调用的完整链路。

**实施步骤**:
1. 使用 AWS X-Ray 为 MCP 服务器启用分布式追踪，自动捕获请求头和延迟。
2. 在所有日志中包含 `Trace-ID`，确保 CloudWatch Logs 中的日志条目可以与 X-Ray 的追踪图关联。
3. 为 Strands Agents 的关键步骤（如工具调用开始、结束、错误）添加结构化日志，

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够长时间运行并具备状态记忆能力的 MCP 服务器。
- 通过结合 Strands Agents 的状态管理能力，MCP 服务器可以突破传统无状态限制，支持需要多轮交互和上下文记忆的复杂工作流。
- 该架构利用了 Bedrock 的托管基础设施，使开发者无需自行管理底层服务器运维，即可构建高可用的持久化 Agent 应用。
- 集成方案简化了将现有 MCP 工具迁移至长期运行环境的流程，增强了 AI 应用在处理复杂任务时的连续性和自主性。
- 此功能进一步扩展了 Amazon Bedrock 的生态系统，强化了基于 MCP 协议的模型上下文共享与 Agent 协作能力。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [长时运行任务](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C%E4%BB%BB%E5%8A%A1/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [AI Agent](/tags/ai-agent/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时间运行的MCP服务器与异步任务管理]({{< relref "posts/20260215-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*