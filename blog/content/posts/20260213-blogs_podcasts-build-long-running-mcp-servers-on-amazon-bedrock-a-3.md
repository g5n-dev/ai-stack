---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理"
date: 2026-02-13T09:55:56+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长时运行", "上下文消息", "AI 代理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的长期运行 MCP 服务器的构建方法。 首先，文章提出了一种**上下文消息策略**，旨在服务器与客户端之间维持持续通信，确保在长时间操作中信息的连贯性。其次，构建了**异步任务管理框架**，使 AI 代理能够启动"
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

在本文中，我们将为您提供一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，该策略可在耗时较长的操作期间保持服务器与客户端之间的持续通信。接下来，我们构建一个异步任务管理框架，允许您的 AI 代理启动长时间运行的任务，而不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 与 Strands Agents，将这些策略融会贯通，打造可投入生产环境的 AI 代理，从而可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理往往面临着状态管理与通信中断的挑战。本文将详细介绍如何利用 Amazon Bedrock AgentCore 结合 Strands Agents，构建具备持久化通信能力的 MCP 服务器。通过实施上下文消息策略与异步任务管理框架，您将掌握打造生产级 AI 代理的关键步骤，从而确保系统在处理复杂耗时操作时依然保持可靠与高效。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的长期运行 MCP 服务器的构建方法。

首先，文章提出了一种**上下文消息策略**，旨在服务器与客户端之间维持持续通信，确保在长时间操作中信息的连贯性。其次，构建了**异步任务管理框架**，使 AI 代理能够启动耗时较长的流程，同时不阻塞其他任务的执行。最后，展示了如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合，打造出能够可靠处理复杂、耗时任务的生产级 AI 代理。

---
## 评论

**中心观点**
该文章提出了一种在 Amazon Bedrock AgentCore 上构建基于 MCP 协议的长期运行服务器的架构方案，其核心在于通过“上下文消息策略”和“异步任务框架”来解决大模型代理在处理长周期任务时的状态保持与通信连续性问题。

**支撑理由与评价**

**1. 解决了 LLM 应用的“同步阻塞”痛点**
*   **事实陈述**：当前主流的 LLM 应用多采用 Request-Response 模式，受限于 Token 生成时间和 HTTP 超时设置，难以处理如数据编码、批量渲染等耗时超过 30-60 秒的任务。
*   **作者观点**：文章引入的“Strands Agents”概念，实质上是将 Agent 的执行链路从“同步调用”转变为“异步编排”。
*   **深度评价**：这是对 Agent 架构的一次重要修正。传统的 Agent 往往因为一次工具调用超时而导致整个对话失败。通过引入异步任务管理框架，文章实际上是在倡导一种**“任务调度与对话解耦”**的设计模式。这不仅提升了系统的鲁棒性，也使得 AI 能够介入更复杂的工业级工作流，而不仅仅是简单的问答。

**2. MCP 协议在云原生环境下的深度集成**
*   **事实陈述**：MCP (Model Context Protocol) 正在成为连接 AI 模型与数据源的标准接口。
*   **你的推断**：文章利用 Bedrock AgentCore 作为托管层，实际上是在解决 MCP 协议在企业级落地时的“最后一公里”问题——即身份认证、权限控制和可观测性。
*   **深度评价**：从行业角度看，这是 AWS 试图在 AI 生态中确立“连接器标准”的尝试。通过展示如何在 Bedrock 上托管 MCP Server，AWS 实际上是在向开发者暗示：**不要把 MCP Server 仅仅当作本地脚本，而应将其视为云原生微服务**。这种思路的转变对于构建企业级 AI 应用至关重要。

**3. 上下文消息策略的工程化实现**
*   **事实陈述**：摘要中提到的“Context message strategy”旨在维持服务器与客户端的连续通信。
*   **深度评价**：这是文章最具技术含金量的部分。在长任务运行期间，客户端不能干等，服务器也不能静默。文章提出的策略可能涉及“心跳检测”、“中间状态流式返回”或“引用令牌”机制。这解决了用户在 AI 处理长任务时的“焦虑感”问题，符合 UX 设计的**3H原则（Here, Hypertext, Hierarchy）中的即时反馈需求**。

**反例与边界条件**

尽管该方案具有前瞻性，但在实际落地中存在以下显著挑战：

1.  **状态一致性的复杂度爆炸**：
    *   **反例**：如果异步任务在执行过程中需要用户介入（例如：审批流中的确认步骤），单纯的异步框架会导致上下文丢失。文章的方案若未处理“人机协同”的中断点，那么在复杂业务流中，Agent 可能会陷入死锁或盲目执行。
    *   **边界条件**：当并发任务量极大时，维护长连接上下文对内存的消耗是巨大的，Bedrock AgentCore 是否能承受高并发的 WebSocket 连接存疑。

2.  **厂商锁定的风险**：
    *   **反例**：虽然 MCP 是开源协议，但文章深度耦合了 Amazon Bedrock AgentCore 和 Strands Agents 的特定 API。如果企业未来想迁移到 Azure OpenAI 或本地部署的 Ollama，重构代码的成本极高。
    *   **边界条件**：对于非 AWS 生态的开发者，或者只需要极简脚本（如 Python Flask + MCP）的用户，该架构显得过于厚重。

**可验证的检查方式**

为了验证该文章所述架构的有效性，建议进行以下检查：

1.  **超时中断恢复测试**：
    *   *方法*：在 MCP Server 模拟一个耗时 5 分钟的任务（如视频渲染），并在任务进行到 50% 时人为切断网络连接 10 秒，随后恢复。
    *   *验证指标*：Agent 是否能自动重连并获取剩余结果，还是直接报错？上下文是否依然保留？

2.  **Token 成本与延迟分析**：
    *   *方法*：对比“同步长轮询”与“文章所述异步框架”在处理相同任务时的 Token 消耗量和端到端延迟。
    *   *验证指标*：异步框架虽然提升了用户体验，但是否因为频繁的状态查询消息而导致 Token 成本激增？

3.  **并发压力测试**：
    *   *方法*：使用 K6 或 Locust 模拟 1000 个并发用户同时触发长时任务。
    *   *验证指标*：观察 Bedrock AgentCore 的冷启动时间和消息吞吐量，验证其是否真正具备生产环境所需的弹性。

**实际应用建议**

1.  **不要盲目追求全异步**：如果你的任务逻辑简单（如单一数据库查询），传统的同步调用依然是最简单、最高效的。只有在涉及多步骤编排或外部 API 聚合时，才考虑引入 Strands Agents 模式。
2.  **关注断点续传机制**：在实施该架构时，务必设计“任务快照”功能。确保即使 Agent 进程重启，也能根据任务 ID 恢复之前的执行状态，而不是从头开始。
3.  **建立监控看板**：长任务最容易出问题的地方在于“黑盒化”。务必为异步任务配置 CloudWatch 告警，监控任务队列积压情况

---
## 技术分析

## 技术分析

### 1. 核心架构与设计理念
文章探讨的是构建长时间运行（Long-running）AI Agent的技术实现路径。其核心架构基于**Amazon Bedrock AgentCore**，并结合了**Strands Agents**的概念。

*   **解耦设计**：技术方案将大模型（LLM）的推理逻辑与具体任务的执行过程分离。LLM负责决策和指令下发，而后续耗时的操作（如数据处理、长流程API调用）由独立的异步组件处理。
*   **状态管理**：针对长任务场景，文章强调了“持续性”的重要性。系统不再依赖传统的无状态HTTP请求/响应模式，而是引入了能够维持任务上下文的机制，确保Agent在任务执行期间能够感知进度并处理中断。

### 2. 关键技术机制
文章重点分析了实现长任务Agent所需的两个关键技术支撑：

*   **MCP (Model Context Protocol) 的应用**：
    *   **标准化连接**：利用MCP协议连接AI应用与数据源，解决了异构系统间的上下文传输问题。
    *   **上下文策略**：通过MCP定义上下文消息的传递策略，确保模型能够获取到执行过程中的关键信息，而非仅仅是最终结果。

*   **异步任务处理与Strands Agents**：
    *   **异步编排**：系统在接收到LLM指令后，启动后台任务并返回任务标识（Task ID），主流程不阻塞。后台服务（如AWS Lambda或容器服务）执行具体逻辑，完成后通过回调或轮询通知AgentCore。
    *   **Strands模式**：Strands Agents被描述为一种处理连续状态流的机制。它允许系统在长周期运行中，对中间状态进行管理和反馈，解决了传统Agent在处理多步骤、长延时任务时的超时和状态丢失问题。

### 3. 技术挑战与应对
在长任务场景下，文章指出了主要的技术难点及应对思路：

*   **Token消耗与上下文窗口**：长任务会产生大量的中间日志。如果将所有原始数据反馈给LLM，会导致上下文窗口溢出或成本过高。
    *   **解决方案**：采用摘要机制。系统仅在关键节点将处理结果的摘要或状态变更反馈给模型，保持上下文精简。
*   **连接稳定性**：长时间运行容易导致网络连接中断。
    *   **解决方案**：引入WebSocket或SSE（Server-Sent Events）等流式传输技术，配合心跳机制，确保客户端与后端服务的通信链路在任务周期内保持活跃。

### 4. 架构演进意义
该技术方案标志着AI应用从简单的“问答交互”向“复杂业务流程自动化”的演进。通过结合Bedrock的基础设施能力与MCP的开放协议标准，企业可以构建出能够处理实际业务逻辑（如批量数据处理、跨系统工单流转）的稳定Agent系统，突破了传统同步交互模式下的时效限制。

---
## 最佳实践

## 最佳实践指南

### 实践 1：设计有状态的长连接会话管理

**说明**:
在构建长时间运行的 MCP (Model Context Protocol) 服务器时，必须维护会话的上下文状态。与无状态的 HTTP 请求不同，长连接需要服务器在多次交互之间记住用户的意图、之前的工具调用结果以及中间步骤。Strands Agents 集成要求会话能够跨越多个逻辑步骤而不丢失上下文。

**实施步骤**:
1. 使用支持持久化的会话存储（如 Redis 或 DynamoDB）来保存会话状态和上下文变量。
2. 在 MCP 服务器实现中，为每个连接分配唯一的 Session ID，并将所有交互与该 ID 绑定。
3. 定义会话超时与清理策略，以防止资源泄漏。

**注意事项**:
避免将敏感的 PII (个人身份信息) 直接明文存储在会话状态中。确保状态存储具有高可用性，以免单点故障导致长任务中断。

---

### 实践 2：实现健壮的流式响应与心跳机制

**说明**:
长时间运行的任务往往需要较长的处理时间，客户端可能会因为超时而断开连接。为了保持连接活跃并提供良好的用户体验，必须实现流式传输数据（如增量返回 Token 或工具执行进度）以及心跳机制来检测连接健康状态。

**实施步骤**:
1. 利用 Bedrock AgentCore 的流式响应接口，实时向客户端推送 LLM 生成的文本或工具执行的中间状态。
2. 实现双向心跳协议，定期发送 Ping/Pong 帧，及时发现并清理死锁或断开的连接。
3. 在 MCP 协议层实现“进度通知”消息，告知客户端当前正在执行的工具及其进度百分比。

**注意事项**:
心跳间隔不宜设置过短，以免增加不必要的网络带宽消耗；也不宜过长，以免无法及时发现断路。

---

### 实践 3：异步化工具调用与任务编排

**说明**:
Strands Agents 可能需要调用耗时较长的工具（例如数据库查询、API 请求或文件处理）。如果在主线程中同步阻塞执行这些操作，会阻塞整个 MCP 服务器的消息循环，导致其他请求无法得到响应。

**实施步骤**:
1. 将所有工具调用逻辑封装为异步任务，使用 Python 的 asyncio 或 Node.js 的 Promise/Async-Await 模式。
2. 为每个工具调用设置合理的超时时间，并实现取消令牌模式，允许 Agent 在用户取消请求时中断正在执行的工具。
3. 使用任务队列处理高延迟操作，MCP 服务器仅返回任务 ID，后续通过轮询或 WebSocket 推送结果。

**注意事项**:
确保异步代码中的异常处理机制完善，避免因单个工具调用失败导致整个服务器进程崩溃。

---

### 实践 4：优化 MCP 工具定义与元数据

**说明**:
为了让 Bedrock AgentCore 和 Strands Agents 能够最有效地调用 MCP 服务器暴露的工具，工具的定义必须清晰、准确且语义丰富。LLM 依赖工具的 JSON Schema 来理解何时以及如何调用它们。

**实施步骤**:
1. 为每个工具编写详细的 `description` 字段，明确说明工具的功能、输入参数含义及预期输出。
2. 优化 JSON Schema，使用枚举限制输入范围，减少幻觉或无效调用。
3. 对工具进行逻辑分组，避免一次性暴露过多功能相似的工具，以免混淆 Agent 的决策逻辑。

**注意事项**:
定期审查工具的调用日志，如果发现 Agent 频繁错误调用某个工具，应调整该工具的描述或 Schema 定义。

---

### 实践 5：构建可观测性与日志追踪体系

**说明**:
调试长连接和复杂的 Agent 交互链路非常困难。完善的可观测性体系对于定位性能瓶颈、理解 Agent 推理路径以及排查工具调用失败原因至关重要。

**实施步骤**:
1. 集成 AWS X-Ray 或 OpenTelemetry，为跨服务的请求生成 Trace ID，实现从 Bedrock Agent 到 MCP 服务器的全链路追踪。
2. 记录结构化日志，包含 Session ID、Trace ID、调用的工具名称、输入参数、返回状态及耗时。
3. 设置 CloudWatch 告警，监控错误率、延迟和连接数等关键指标。

**注意事项**:
在记录日志时，注意过滤敏感参数（如密码、Token），确保符合安全合规要求。

---

### 实践 6：实施严格的输入验证与安全防护

**说明**:
MCP 服务器作为 Agent 与后端系统交互的桥梁，必须防止恶意指令或通过 Prompt 注入导致的非法操作。长连接环境更容易受到持续性的攻击尝试。

**实施步骤**:
1. 在 MCP 服务器入口处实施严格的输入参数验证，不信任任何来自 Agent 的输入。
2. 实施最小权限原则，为 MCP 服务器配置 IAM 角色，仅授予其完成任务所需的最小权限集。
3. 限制工具的递归调用次数和总执行步数，防止因 Agent 陷入死循环而导致资源耗尽。

**注意事项**:
定期进行安全审计，测试 Agent 是否能被诱导执行破坏性操作（如删除数据、修改权限）。

---
## 学习要点

- Amazon Bedrock AgentCore 正式发布，支持构建具备长期记忆和状态管理能力的持久化 MCP 服务器，解决了传统无状态模型无法处理多轮复杂任务的限制。
- 通过集成 Strands Agents，开发者可以创建能够自主规划、执行并跨越多个交互步骤维持上下文的高级 AI 智能体。
- 该架构利用 MCP 协议实现了 AI 智能体与外部数据源及工具之间的标准化互操作性，显著降低了集成复杂度。
- 借助 AgentCore 的托管基础设施，开发者无需维护底层服务器状态，即可轻松构建具备企业级可靠性和可扩展性的生成式 AI 应用。
- 这一解决方案特别适用于需要长时间运行的复杂工作流场景，如代码库分析、多步骤数据处理或需要跨越数天甚至数周的自动化任务编排。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [上下文消息](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E6%B6%88%E6%81%AF/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用]({{< relref "posts/20260210-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*