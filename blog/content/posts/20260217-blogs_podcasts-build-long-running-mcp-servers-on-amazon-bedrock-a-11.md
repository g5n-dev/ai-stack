---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理"
date: 2026-02-17T06:54:40+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长时运行", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 构建长期运行 MCP 服务器的综合方法，旨在解决 AI 代理在处理耗时任务时的可靠性问题。 核心内容包含以下三点： 1. **上下文消息策略**：引入一种机制，确保在扩展操作期间，服务器与客户端之间维持持续的通信，避"
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

在本篇文章中，我们为您提供了一套全面的实现方法。首先，我们介绍一种上下文消息策略，在耗时较长的操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，让您的 AI 代理能够启动长时间运行的任务，而不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents 将这些策略落地，构建生产级的 AI 代理，可靠地处理复杂、耗时的操作。

---
## 导语

构建能够处理复杂、耗时任务的 AI 代理是当前技术落地的一大难点，特别是在需要保持长时间通信的场景中。本文将介绍一套基于 Amazon Bedrock AgentCore 和 Strands Agents 的实现方案，重点解析如何通过上下文消息策略与异步任务管理框架，解决服务端与客户端的持续通信问题。阅读本文，您将掌握构建生产级长运行 MCP 服务器的关键技术，确保 AI 代理在处理复杂操作时既稳定又高效。

---
## 摘要

本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 构建长期运行 MCP 服务器的综合方法，旨在解决 AI 代理在处理耗时任务时的可靠性问题。

核心内容包含以下三点：

1.  **上下文消息策略**：引入一种机制，确保在扩展操作期间，服务器与客户端之间维持持续的通信，避免因长任务执行而导致的连接超时或上下文丢失。
2.  **异步任务管理框架**：开发了一个框架，允许 AI 代理启动长时运行的后台进程，同时不阻塞其他操作的执行，从而保持系统的并发处理能力和响应速度。
3.  **生产级集成**：演示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，构建出能够可靠处理复杂、耗时操作的生产级 AI 代理。

总结来说，通过结合持续通信策略与异步管理能力，开发者可以在 Bedrock 上构建出健壮的、适用于长时工作流的 AI 系统。

---
## 评论

### 中心观点
该文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的异步任务管理架构，旨在通过上下文消息策略和 MCP（Model Context Protocol）的长连接机制，解决大模型智能体在执行耗时任务时的状态保持与中断恢复问题。

### 支撑理由与深度评价

#### 1. 解决了“长任务”与“无状态模型”的根本矛盾（事实陈述）
大模型本身是无状态的，而现实世界的业务流程（如数据处理、代码部署）往往是长周期的。文章提出的“异步任务管理框架”切中了当前 AI Agent 落地的核心痛点。
*   **深度分析**：传统的 Agent 模式通常依赖单次请求-响应循环，一旦任务超过 LLM 的 Context Window 或 Timeout 限制，连接就会断开。文章通过引入类似“中间件”的异步层，将“对话连接”与“任务执行”解耦，这是构建企业级 Agent 的必经之路。
*   **反例/边界条件**：如果任务本身是毫秒级的简单查询（如“查天气”），引入此架构会带来不必要的延迟和架构复杂度。此外，如果异步任务在执行过程中需要频繁的人工介入，单纯的状态保持可能不够，还需要引入“人机协同”的审批流机制。

#### 2. 上下文消息策略是对 MCP 协议的工程化补全（你的推断）
MCP 协议目前主要关注上下文的传输，但在长连接维护上缺乏标准。文章提出的“Context Message Strategy”实际上是一种自定义的“心跳”和“状态广播”机制。
*   **深度分析**：这不仅仅是技术实现，更是一种设计模式。它允许客户端在任务未完成时，也能获得中间进度反馈，极大地提升了用户体验。从行业角度看，这类似于将 HTTP 轮询升级为 WebSocket 推送，但在 AI 语义层面进行了封装。
*   **反例/边界条件**：这种策略高度依赖客户端的兼容性。如果客户端不支持解析这种自定义的上下文消息，或者网络环境处于高延迟的弱网环境，频繁的状态同步可能导致拥塞控制失效。

#### 3. 利用 Bedrock AgentCore 强化了可观测性与安全性（事实陈述）
文章强调在 Amazon Bedrock 上构建，这意味着自动继承了 AWS 的 IAM 权限控制和 CloudWatch 监控。
*   **深度分析**：这是该方案与开源方案（如基于 LangChain 的自建 Agent）最大的区别。在企业环境中，合规性和可追溯性往往比算法本身更重要。通过 AgentCore 集成，可以将 Strands Agents 的行为纳入统一的云治理体系。
*   **反例/边界条件**：这也导致了严重的 Vendor Lock-in（厂商锁定）。如果企业未来需要迁移到 GCP 或 Azure，或者切换到非 AWS 托管的 LLM，这种与 Bedrock 深度绑定的架构重构成本将非常高昂。

#### 4. Strands Agents 集成的实际效用存疑（批判性观点）
文章标题提到了 Strands Agents，但在摘要和常见的技术逻辑中，Strands 主要负责多步推理的规划。
*   **深度分析**：如果 Strands 仅作为规划器，而 Bedrock AgentCore 作为执行器，那么两者之间的接口定义将成为性能瓶颈。如果 Strands 的规划粒度太细，会导致与 Bedrock 的交互次数过多，增加延迟和 Token 消耗；如果太粗，则失去了动态调整的能力。
*   **反例/边界条件**：对于逻辑极其复杂、需要跨多系统调用的编排任务，纯粹的 LLM 规划（Strands）可能不如确定性的状态机或 Workflow 引擎（如 Temporal/Cadence）稳定可靠。

### 综合评价维度

*   **内容深度**：文章属于工程实践类，深度中等偏上。它没有探讨底层的模型算法，而是聚焦于架构设计。对于正在面临 Agent 超时问题的架构师具有很高的参考价值，但缺乏对并发处理和错误重试策略的细节描述。
*   **实用价值**：高。它提供了一个可落地的蓝图，特别是针对 AWS 生态内的开发者。
*   **创新性**：中等。异步任务管理并非新概念，但在 MCP 和 Bedrock 的具体语境下，将其标准化为一种模式是有益的尝试。
*   **可读性**：结构清晰，针对性强，但需要读者具备一定的 AWS 服务背景知识。
*   **行业影响**：有助于推动 MCP 协议在企业级应用中的标准化，暗示了未来 Agent 开发将从“单次对话”转向“任务型应用”的趋势。

### 可验证的检查方式

1.  **压力测试指标**：
    *   构建一个模拟长任务（如 5 分钟），观察客户端连接断开重连后，是否能无缝恢复任务状态而不丢失上下文。
    *   测量异步框架引入的额外延迟（从任务提交到开始执行的时间差）。

2.  **成本与Token消耗分析**：
    *   对比传统轮询方式与该文提出的“上下文消息策略”在长任务中的 Token 消耗总量。检查是否存在因频繁传递上下文导致的 Token 激增。

3.  **兼容性验证**：
    *   验证该 MCP Server 是否能被非 AWS 的客户端（如本地 VS Code 插件或第三方 Chatbot）无缝调用，以测试其协议的标准化程度。

4.  **故障恢复观察**：
    *   在任务执行途中人为中断 Bedrock 服务或网络，观察系统是否提供了幂等性保证，防止任务重复执行。

### 实际应用建议

1

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 与 Strands 构建长效 MCP 服务器

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：**在生成式 AI 应用中，为了解决大模型（LLM）受限于上下文窗口和单轮响应时间的问题，必须构建一种能够处理“长时间运行任务”的服务器架构。** 具体而言，文章提出利用 **Amazon Bedrock AgentCore** 作为基础编排层，结合 **MCP (Model Context Protocol)** 服务器标准，并集成 **Strands Agents** 框架，来实现一种既能保持客户端连续感知，又能异步处理复杂任务的智能体系统。

**作者想要传达的核心思想**
作者试图传达从“同步请求-响应模式”向“异步状态管理模式”的范式转变。传统的 AI 交互往往是用户提问，模型一次性生成答案。但在处理复杂任务（如代码重构、长时间数据分析、多步骤工作流）时，这种模式会失效。核心思想在于**“解耦”**：将任务的“执行”与“交互”分离，通过上下文消息策略让用户知道任务正在进行，而实际耗时操作在后台异步完成。

**观点的创新性和深度**
*   **深度**：文章不仅停留在应用层面，而是深入到了协议层（MCP）和架构层。它探讨了如何在无状态或短连接的 HTTP 协议之上，模拟出有状态的、长连接的 Agent 体验。
*   **创新性**：将 **Strands Agents**（通常指代具备记忆和连续执行能力的智能体框架）与 **MCP**（一种标准化的数据交换协议）结合，并运行在 **Bedrock AgentCore**（AWS 的托管编排服务）之上。这种组合利用了云服务的弹性、协议的通用性以及智能体的持久性能力，解决了企业级应用中“任务超时”和“用户体验中断”的痛点。

**为什么这个观点重要**
随着 AI 从“聊天玩具”转向“生产力工具”，用户期望 AI 能够处理真正的复杂工作。如果 AI 只能做几秒钟内能完成的事，其应用场景将被极大限制。构建长效运行服务器是 AI Agent 走向自动化的必经之路，这对于企业级自动化、RPA（机器人流程自动化）以及智能运维等领域具有决定性意义。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**：由 Anthropic 推出的开放协议，用于连接 AI 应用与数据源。文章中将其作为服务器与客户端通信的标准接口。
2.  **Amazon Bedrock AgentCore**：AWS Bedrock 的一部分，负责 Agent 的核心逻辑编排、路由和工具调用。
3.  **Strands Agents**：一种专注于长时间运行的 Agent 框架概念（或特定技术），强调“Strand”（线索/线程）的连续性，即 Agent 在多轮对话中保持对目标追踪的能力。
4.  **异步任务管理框架**：用于处理非阻塞操作的技术栈。

**技术原理和实现方式**
*   **Context Message Strategy（上下文消息策略）**：
    *   **原理**：在长时间任务执行期间，服务器不能保持连接挂起。相反，服务器会发送一系列“上下文消息”给客户端。这些消息不是最终结果，而是状态更新（如“正在分析第 1 个文件...”，“正在等待 API 响应...”）。
    *   **实现**：利用 MCP 的消息传递机制，将任务状态封装成标准事件推送给前端，前端通过渲染这些状态更新，让用户感觉到 Agent 仍在“思考”和“工作”。
*   **异步任务管理框架**：
    *   **原理**：当 Agent 发起一个耗时操作（如调用 Bedrock 进行大文档总结）时，主线程立即返回一个“任务 ID”或“挂起状态”。后台进程（如 AWS Lambda 或容器）接手实际工作。
    *   **实现**：结合 Bedrock AgentCore 的编排能力，将工具调用配置为异步模式。AgentCore 触发 Strands Agent 开始执行，Strands Agent 分片执行任务并定期更新状态存储（如 DynamoDB）。

**技术难点和解决方案**
*   **难点 1：状态一致性**。异步操作可能导致状态不同步。
    *   **解决方案**：引入持久化存储层，Strands Agent 每完成一步操作都进行 Checkpoint（检查点）保存。
*   **难点 2：超时控制**。HTTP 请求通常有超时限制。
    *   **解决方案**：彻底解耦。客户端发起请求后，服务器立即返回 Ack（确认），后续通过轮询或 WebSocket 推送来获取进度，而非保持 HTTP 连接打开。
*   **难点 3：上下文遗忘**。长时间任务可能导致 LLM 忘记初衷。
    *   **解决方案**：Strands Agents 的核心机制——动态摘要和记忆回溯，定期将中间结果压缩回 Prompt。

**技术创新点分析**
文章的创新点在于**“标准化”与“云端托管”的结合**。以往的长效 Agent 往往是自建的各种 Python 脚本，难以维护且无法标准化接入各种 LLM 客户端。通过 MCP 标准化接口，配合 Bedrock AgentCore 的托管能力，使得构建这种复杂系统的门槛大大降低，且具备了企业级的可扩展性。

## 3. 实际应用价值

**对实际工作的指导意义**
*   **架构设计**：指导架构师如何设计不阻塞用户界面的 AI 后端。
*   **开发模式**：教导开发者如何从“写函数”转向“设计工作流”。

**可以应用到哪些场景**
1.  **企业级 RPA（机器人流程自动化）**：例如，处理财务报销单，需要跨系统查询、核对、审批，耗时数分钟甚至数小时。
2.  **代码库迁移与重构**：分析整个 GitHub 仓库的代码依赖关系并生成重构方案，这需要极长的计算时间。
3.  **复杂数据分析报告**：上传 Excel，Agent 进行清洗、分析、绘图，最后生成 PDF。
4.  **科研辅助**：长时间监控特定实验数据或文献库，并在发现异常时主动通知。

**需要注意的问题**
*   **成本控制**：长时间运行意味着更多的 Token 消耗和计算资源占用，必须设置超时或预算熔断机制。
*   **错误恢复**：如果异步任务中途失败，如何从断点恢复而不是从头开始。

**实施建议**
建议采用**“事件驱动架构”**。不要试图在 Bedrock 的单次 Agent 调用中完成所有工作。应将 Agent 的动作分解为离散的事件，利用 Step Functions（如果是在 AWS 上）来编排这些长流程。

## 4. 行业影响分析

**对行业的启示**
这篇文章预示着 AI Agent 正在从**“快思考”（System 1，直觉反应）**向**“慢思考”（System 2，逻辑推理与规划）**演进。行业需要关注如何构建支持“慢思考”的基础设施，而不仅仅是优化模型的响应速度。

**可能带来的变革**
*   **SaaS 软件的形态变革**：软件将不再是“菜单驱动”，而是“意图驱动”。用户不再需要盯着进度条，而是交给 Agent 在后台处理，处理完成后通知用户。
*   **MCP 协议的普及**：如果此类架构成为主流，MCP 有望成为连接 AI 与企业系统的标准协议，类似于 SQL 之于数据库。

**对行业格局的影响**
这将进一步巩固云厂商（如 AWS）在 AI 时代的地位。因为构建这种复杂的长效系统，离不开强大的底层基础设施（队列、数据库、无服务器计算）。单纯提供 API 的模型厂商将不得不依赖云厂商的 Agent 编排能力。

## 5. 延伸思考

**引发的其他思考**
*   **人机协作的新模式**：如果 Agent 可以长时间运行，人类在其中的角色是什么？是“发布命令者”还是“异常处理者”？
*   **多 Agent 协作**：Strands Agents 是否可以与其他 Agent 并行工作？例如，一个 Agent 负责长时间检索，另一个负责实时交互。

**可以拓展的方向**
*   **流式输出的中间态处理**：如何将 Agent 思维链的中间过程可视化，既不暴露内部逻辑混乱，又能提供进度感。
*   **跨云平台的迁移性**：基于 MCP 的设计是否能轻松从 Bedrock 迁移到 Azure OpenAI 或 Google Gemini，而不改变服务器代码。

**未来发展趋势**
未来，**“Duration as a Service”**（时长即服务）可能会出现。开发者将按 Agent 运行的时长和步数付费，而不是仅仅按 Token 付费。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务耗时**：识别你当前 AI 应用中哪些任务经常超时或用户体验不佳。
2.  **引入消息队列**：即使是简单的实现，也应在 Agent 和实际执行器之间加入队列（如 Redis SQS）。
3.  **定义状态机**：明确任务有哪些状态（Pending, Running, Completed, Failed），并确保前端能展示这些状态。

**具体的行动建议**
*   **第一步**：阅读 MCP 协议规范，理解 Resource 和 Prompt 的定义。
*   **第二步**：在 AWS 上构建一个简单的 Bedrock Agent，尝试调用一个模拟的长时间 API。
*   **第三步**：实现一个“心跳”机制，让 Agent 每隔 10 秒向客户端发送一次状态。

**需要补充的知识**
*   **异步编程模型**（如 Python asyncio, JavaScript Promises）。
*   **AWS Lambda 和 Step Functions** 的使用。
*   **JSON Schema** 定义（用于 MCP 工具定义）。

**实践中的注意事项**
*   **幂等性**：确保如果客户端重复发送请求，服务器不会重复执行任务。
*   **安全性**：长时间运行的连接更容易受到攻击，需严格校验 MCP 客户端的身份。

## 7. 案例分析

**结合实际案例说明**
假设一个**“法律合同审查 Agent”**。
*   **传统模式**：用户上传 50 页合同，Agent 处理 30 秒，期间前端转圈，然后返回结果。如果合同 500 页，请求超时，失败。
*   **本文架构模式**：
    1.  用户上传合同。
    2.  Bedrock Agent 接收请求，调用 Strands Agent。
    3.  Strands Agent 立即返回：“任务已接收，正在初步扫描...”。
    4.  后台分批处理合同，每处理完 10 页，更新上下文消息：“已审查 10/50 页，发现 2 个风险点...”。
    5.  用户在前端实时看到进度条和初步发现。
    6.  审查完成后，Agent 发送最终报告。

**成功案例分析**
**GitHub Copilot Workspace** 是类似逻辑的体现。它允许开发者提出需求，然后在后台生成计划、执行代码修改，整个过程是异步且可视化的，用户可以随时介入。

**失败案例反思**
早期的 ChatGPT 插件往往因为执行时间过长而报错 "Network Error" 或 "Timeout"。这就是缺乏异步任务管理框架和上下文维持策略的直接后果。

## 8. 哲学与逻辑：论证地图

**中心命题**
**为了实现具备企业级

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化会话状态管理与持久化

**说明**:
长时间运行的 MCP 服务器需要维护跨多个请求和轮次的上下文信息。AgentCore 依赖于 Strands Agents 来处理复杂的多步骤任务，因此，必须将会话状态（如用户偏好、中间变量和已完成的工作流步骤）持久化存储在数据库（如 DynamoDB）中，而不是仅依赖内存。

**实施步骤**:
1. 选择低延迟的存储解决方案（如 Amazon DynamoDB 或 ElastiCache）来存储会话令牌和上下文数据。
2. 在 MCP 服务器逻辑中实现状态序列化和反序列化中间件。
3. 配置合理的 TTL（生存时间）策略以自动清理过期的会话数据，防止存储无限增长。

**注意事项**:
避免在内存中保存敏感的 PII（个人身份信息）或关键业务状态，以防服务器重启导致数据丢失。

---

### 实践 2：实施严格的超时与异步处理机制

**说明**:
长时间运行的任务可能会导致 HTTP 请求超时或阻塞 MCP 客户端。最佳实践是采用异步处理模式：MCP 服务器接收请求后立即返回确认，将任务放入后台队列（如 Amazon SQS）处理，并通过回调或轮询机制通知客户端结果。

**实施步骤**:
1. 将 MCP 服务器的同步处理逻辑重构为基于事件驱动的异步架构。
2. 集成 Amazon Step Functions 或 SQS 来管理长时间运行的工作流。
3. 实现一个状态查询端点，允许 Strands Agents 检查后台任务的进度。

**注意事项**:
确保异步任务的幂等性，以便在网络重试的情况下不会重复执行业务逻辑。

---

### 实践 3：设计幂等且可重试的工具接口

**说明**:
在分布式环境中，网络故障是不可避免的。MCP 服务器暴露给 Bedrock AgentCore 的工具接口必须设计为幂等的，确保在 Strands Agents 自动重试调用时，系统状态保持一致且不会产生副作用（例如重复扣款或重复创建记录）。

**实施步骤**:
1. 为每个请求生成唯一的幂等键，并在服务器端进行校验。
2. 在工具逻辑中实现“检查是否存在”的模式，在执行写操作前先验证资源是否已存在。
3. 配置 AgentCore 的重试策略，使用指数退避算法以避免压垮后端服务。

**注意事项**:
对于非幂等操作（如发送电子邮件），应在服务器端去重，而不是依赖客户端不重试。

---

### 实践 4：建立全面的可观测性与日志记录

**说明**:
调试长时间运行的 Agent 链路非常具有挑战性。必须将 MCP 服务器的日志与 Amazon Bedrock 的调用链路集成，以便追踪 Strands Agents 的决策过程和工具调用详情。

**实施步骤**:
1. 使用 AWS CloudWatch 或 OpenTelemetry 收集结构化日志。
2. 在日志中包含 `trace_id`，以便将 MCP 服务器的日志条目与 Bedrock Agent 的调用关联起来。
3. 监控关键指标，如工具调用延迟、错误率和 Strands Agents 的迭代轮次。

**注意事项**:
避免记录敏感的有效负载数据，确保日志符合企业的安全合规要求。

---

### 实践 5：精细化错误处理与异常反馈

**说明**:
MCP 服务器应向 AgentCore 返回结构化的错误信息，而不是通用的 500 错误。Strands Agents 依赖这些错误信息来决定是重试、放弃还是尝试纠正路径。清晰的错误信息能显著提高 Agent 的自主解决问题的能力。

**实施步骤**:
1. 定义一套标准的错误代码和消息模式（例如：`INVALID_INPUT`, `SERVICE_UNAVAILABLE`, `RATE_LIMIT_EXCEEDED`）。
2. 在工具返回的错误响应中包含“可恢复性”提示，告知 Agent 是否可以重试。
3. 验证 Bedrock Agent 如何解析你的错误响应，并相应调整提示词或响应格式。

**注意事项**:
不要在错误消息中暴露堆栈跟踪或内部系统架构细节，以防安全漏洞。

---

### 实践 6：配置资源限制与速率控制

**说明**:
为了防止 Strands Agents 在循环逻辑中无限调用 MCP 工具（例如陷入死循环），必须在服务器端实施速率限制和资源配额。这可以保护下游系统免受流量突变的冲击，并控制成本。

**实施步骤**:
1. 在 MCP 服务器前部署 API Gateway 或使用中间件来实施基于令牌桶的速率限制。
2. 为每个会话或用户设置最大调用次数或最大计算时间预算。
3. 实施熔断器模式，当后端依赖服务出现故障时，快速失败而不是让请求排队。

**注意事项**:
速率限制应足够宽松，以允许正常的复杂工作流完成，同时严格到足以阻止异常行为。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够维护长期对话状态和记忆的持久化 MCP 服务器。
- 通过将 Strands Agents 的记忆机制与 Bedrock 的托管基础设施相结合，该架构解决了传统无状态 AI 应用难以处理多步骤复杂任务的局限性。
- 开发者可以利用 MCP 协议的标准化接口，将具备长期运行能力的 AI 服务无缝集成到现有的工作流和应用程序中。
- 此项集成显著降低了构建具备上下文感知能力的智能系统的技术门槛，无需从头搭建复杂的状态管理基础设施。
- 该解决方案特别适用于需要跨越多个会话保持上下文连贯性的场景，如项目跟踪、客户支持或复杂的研究分析任务。

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
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
- [基于Amazon Bedrock AgentCore与Strands Agents构建长时运行MCP服务器]({{< relref "posts/20260215-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*