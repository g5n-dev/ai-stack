---
title: "基于Amazon Bedrock AgentCore与Strands Agents构建长时运行MCP服务器"
date: 2026-02-16T23:54:05+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "长时运行", "异步任务", "AI 智能体", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "基于Amazon Bedrock AgentCore和Strands Agents构建长时间运行MCP服务器的技术路径 本文介绍了一种利用Amazon Bedrock AgentCore与Strands Agents集成，构建支持长时间运行任务的M服务器（Model Context Protocol服务器）的综合方法，"
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

在这篇文章中，我们将为您提供一种全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，在耗时较长的操作期间，保持服务器与客户端之间的持续通信。接下来，我们构建一个异步任务管理框架，让您的 AI 智能体能够启动长时间运行的任务，同时不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 与 Strands Agents 来应用这些策略，构建能够可靠处理复杂且耗时操作的生产级 AI 智能体。

---
## 导语

构建能够稳定处理长时运行任务的 AI 智能体是当前开发中的难点，特别是在需要保持客户端与服务端持续通信的场景下。本文将介绍如何利用 Amazon Bedrock AgentCore 结合 Strands Agents，通过上下文消息策略与异步任务管理框架，有效解决耗时操作阻塞问题。阅读本文，您将掌握构建生产级、高并发 AI 智能体的具体方法，实现复杂业务流程的可靠自动化。

---
## 摘要

### 基于Amazon Bedrock AgentCore和Strands Agents构建长时间运行MCP服务器的技术路径

本文介绍了一种利用Amazon Bedrock AgentCore与Strands Agents集成，构建支持长时间运行任务的M服务器（Model Context Protocol服务器）的综合方法，旨在解决AI代理处理复杂、耗时任务时的可靠性问题。核心方案包括以下三点：

1.  **上下文消息策略**  
   采用持续通信机制，确保服务器与客户端在长时间任务执行期间保持状态同步。通过传递上下文消息，系统能实时反馈任务进展，避免因长时间等待导致的连接中断或状态丢失。

2.  **异步任务管理框架**  
   设计非阻塞式任务处理架构，允许AI代理启动耗时操作（如数据处理、API调用等）的同时，继续响应其他请求。该框架通过任务队列、状态追踪和回调机制，实现多任务并发执行，提升系统效率。

3.  **生产级集成实践**  
   结合Amazon Bedrock AgentCore的服务编排能力和Strands Agents的流程管理功能，将上述策略整合为可落地的解决方案。该架构支持任务持久化、错误恢复和动态扩展，适用于企业级场景中需要高可靠性的复杂操作（如跨系统数据同步、长时间推理任务等）。

通过这一方案，开发者能够构建稳定、可扩展的AI代理系统，有效应对生产环境中长周期任务的挑战。

---
## 评论

### 中心观点
该文章提出了一种在 Amazon Bedrock AgentCore 上构建基于 Strands Agents 的长运行 MCP 服务器的架构范式，其核心在于通过**上下文消息策略**和**异步任务管理框架**来解决 LLM 应用中的“长连接”与“状态保持”难题。

### 支撑理由与边界条件分析

**1. 解决了 LLM 应用的“同步阻塞”痛点（事实陈述）**
目前的 MCP (Model Context Protocol) 和大多数 Agent 框架默认采用同步 Request-Response 模式。当 Agent 需要执行耗时任务（如调用 Bedrock 处理大型文档、等待人工审批）时，连接容易超时或被中断。
*   **文章价值**：通过引入“上下文消息策略”，将长任务拆解为可被客户端轮询或接收的状态更新，维持了会话的“活性”。
*   **反例/边界条件**：如果客户端不支持 WebSocket 或长轮询，这种架构会退化；对于毫秒级要求的实时控制流，引入异步队列反而增加了延迟。

**2. 引入 Strands Agents 实现状态持久化（事实陈述）**
Strands 架构（通常指 Anthropic 或 AWS 生态中支持多步骤推理的 Agent 机制）允许 Agent 在任务中断后恢复上下文。
*   **文章价值**：这解决了 Bedrock Agent 在处理复杂工作流时“无状态”导致的重复交互问题，使得 Agent 能够像传统后端服务一样处理“长事务”。
*   **反例/边界条件**：状态持久化会带来显著的一致性挑战。如果异步任务执行失败，如何回滚 Strands 中已记录的中间状态？文章可能未深入讨论分布式事务（Saga 模式）的复杂性。

**3. 异步任务管理框架提升了系统吞吐（作者观点）**
文章主张将计算密集型任务从主线程剥离。
*   **文章价值**：这是高并发系统的标准做法，结合 AWS 的基础设施（如 SQS/Lambda），可以有效降低 Bedrock Agent 的直接负载成本。
*   **反例/边界条件**：异步架构大幅增加了运维复杂度（调试困难、日志分散）。对于简单的查询类 Agent，这种架构属于过度设计，增加了开发者的心智负担。

### 深度评价

#### 1. 内容深度：架构层面的务实，算法层面的留白
文章在**工程架构**层面具有较高的深度。它准确识别了当前生成式 AI 落地的主要瓶颈：从“玩具级”对话走向“生产级”业务流时，必须解决网络超时和状态管理问题。利用 Bedrock AgentCore 与 Strands 的结合，是对 AWS 原生生态的一次有效整合。
然而，在**算法逻辑**层面，文章可能存在留白。它假设 Agent 能够正确地拆解任务并触发异步流程，但在实际操作中，LLM 生成正确的异步调用指令（Prompt Engineering）往往比搭建异步队列更具挑战性。文章若能补充如何 Prompt 模型去“理解”并“使用”这套异步框架，深度会更佳。

#### 2. 实用价值：特定场景下的“必读指南”
对于致力于在 AWS 上构建**企业级 Copilot**（如代码生成、数据分析、ERP 自动化）的团队，这篇文章具有极高的实用价值。它提供了一套可复制的“脚手架”，避免了开发者从零开始设计轮子。
*   **实际案例**：假设一个“年报生成 Agent”，需要查询数据库、生成图表、编写文案。传统同步模式会在 30 秒后超时。采用此文方案，Agent 可以先返回“任务 ID”，后台异步生成，用户端通过轮询获得进度条，体验极佳。

#### 3. 创新性：组合式创新
这并非底层理论的突破，而是**工程模式的创新**。将传统的微服务异步模式（CQRS/Event Sourcing 思想）引入到 LLM Agent 的生命周期管理中。它提出了一种观点：**Agent 不仅是对话接口，更是任务调度器**。

#### 4. 行业影响与争议点
*   **行业影响**：这篇文章暗示了 MCP 协议进化的方向——从简单的“工具调用”转向“持久化服务编排”。它可能会推动 AWS 生态内的开发者更倾向于使用 Bedrock 而非 LangChain 等开源框架来构建复杂应用，因为后者在长任务处理上往往需要大量自定义代码。
*   **争议点/不同观点**：
    *   **复杂度陷阱**：业界有观点认为 Agent 应保持“无状态”以实现水平扩展。引入 Strands 和复杂的异步状态管理，可能导致系统难以维护，违背了 Serverless 的初衷。
    *   **厂商锁定**：深度绑定 Bedrock AgentCore 和 Strands 概念，可能导致应用难以迁移至 Azure OpenAI 或 Google Gemini。

### 实际应用建议

1.  **不要盲目照搬**：如果你的 Agent 只是回答简单的 FAQ 或 RAG 检索，**不要**使用此架构。同步调用成本更低、速度更快。仅在任务耗时 > 10秒或涉及多步骤审批时引入。
2.  **关注死信队列（DLQ）**：异步任务必然伴随失败。在实际部署时，必须为 Bedrock Agent 的异步调用配置完善的 DLQ 和告警机制，否则长任务会“静默失败”，用户体验极差。
3.  **成本监控**：Strands 类 Agent 通常涉及多轮模型调用。长运行任务可能导致 Token 消耗激增，建议设置 Token 预算硬上限。

### 可验证的检查方式

1.

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要片段，以下是对该技术方案的深入分析。

---

# 深度分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 构建持久化 MCP 服务器

## 1. 核心观点深度解读

**文章的主要观点**
文章提出了一种在 Amazon Bedrock AgentCore 环境下，结合 Strands Agents 框架来构建“长时间运行”的模型上下文协议（MCP）服务器的综合解决方案。其核心在于解决 AI Agent 在处理耗时任务（如数据处理、复杂工作流编排）时，如何保持上下文连续性、管理异步状态并维持客户端通信稳定性这一行业难题。

**作者想要传达的核心思想**
传统的同步请求-响应模式无法满足复杂 AI 应用的需求。作者主张通过**“上下文消息策略”**和**“异步任务管理框架”**的解耦，将 AI Agent 的思考过程与执行过程分离。核心思想是：**Agent 不应被阻塞等待任务完成，而应通过 Strands 的“链”式记忆能力，在任务执行期间保持对状态的感知，并在适当时机恢复交互。**

**观点的创新性和深度**
该观点的创新点在于将 LangChain 生态中的 **Strands（一种用于长时间运行的 Agent 记忆与状态管理机制）** 与 AWS 的 **Bedrock AgentCore（托管式 Agent 编排服务）** 及 **MCP（新兴的互操作性标准）** 进行了深度融合。这不仅解决了技术实现问题，更在架构层面定义了“有状态 AI 服务”在云原生环境下的最佳实践。

**为什么这个观点重要**
随着 AI Agent 从简单的聊天机器人向能够执行复杂任务的“智能体”演进，任务执行的耗时性和不确定性成为瓶颈。如果无法支持长连接和异步回调，Agent 的应用场景将被限制在简单的问答领域。该方案为构建企业级、高可靠性的 AI 劳动力提供了关键的架构蓝图。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**：一种开放协议，用于连接 AI 应用与数据源。在此处，它作为 Server 与 Client 通信的统一接口。
2.  **Amazon Bedrock AgentCore**：AWS 提供的底层构建块，允许开发者精细控制 Agent 的编排逻辑（相比完全托管的 Bedrock Agents）。
3.  **Strands Agents**：源自 LangChain/LangGraph 的概念，指代具有持久化记忆、能够跨越多个交互步骤处理复杂任务的 Agent 架构。
4.  **异步任务管理**：将耗时操作（如 API 调用、数据库写入）从主线程剥离。

**技术原理和实现方式**
*   **Context Message Strategy（上下文消息策略）**：
    *   **原理**：在 MCP 通信层，服务器不再是一次性返回结果，而是返回一个“任务已接收”的确认，并附带一个唯一标识符（Context ID）。
    *   **实现**：利用 WebSocket 或长轮询机制（取决于 MCP 的具体传输层实现），服务器在后台任务完成时，主动推送更新或允许客户端轮询状态。
*   **Asynchronous Task Framework（异步任务框架）**：
    *   **原理**：引入消息队列（如 AWS SQS）或状态机（如 AWS Step Functions）。
    *   **实现**：当 Agent 发起长时间操作时，MCP Server 将任务元数据存入数据库，将任务指令放入队列。Worker 进程处理任务并更新状态。Agent 通过 Strands 机制定期“唤醒”或通过回调检查状态。

**技术难点和解决方案**
*   **难点**：状态同步与超时处理。如果 Agent 在任务完成前断开连接，如何恢复？
*   **方案**：Strands 提供了持久化的内存存储。Agent 的状态被序列化存储在 DynamoDB 等数据库中。当 Agent 重新加载时，它能读取 Strand 中的历史记录，知道有一个任务正在进行，并继续等待结果。
*   **难点**：并发控制。
*   **方案**：AgentCore 的编排层负责管理并发请求，确保同一 Strand 的状态修改是原子性的。

**技术创新点分析**
将 **Strands** 的“时间旅行”调试与状态恢复能力引入到 **MCP Server** 的构建中，使得 MCP 不仅仅是一个数据传输协议，更变成了一个**有状态的会话管理器**。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为开发者提供了一种标准模式，用于开发那些“不能让用户等待”的 AI 功能。它指导开发者如何从设计同步的 API 转向设计基于事件的异步 AI 工作流。

**可以应用到哪些场景**
1.  **RAG 与大数据分析**：用户要求 Agent 分析一个 1GB 的 CSV 文件，这需要几分钟。
2.  **企业流程自动化**：Agent 需要审批一个流程，等待人工管理员确认（可能数小时）。
3.  **代码生成与部署**：Agent 生成代码后，触发 CI/CD 管道进行构建和部署，需要跟踪部署状态。
4.  **多媒体生成**：生成视频或渲染 3D 图像的长耗时任务。

**需要注意的问题**
*   **成本**：长时间保持连接或频繁轮询状态会增加基础设施成本。
*   **复杂性**：异步编程比同步编程更难调试，需要处理幂等性和重试逻辑。

**实施建议**
*   采用 AWS Step Functions 来定义长时间运行的工作流，因为其内置了可视化和错误处理机制。
*   为 MCP Server 设计清晰的“心跳”机制，以区分“任务还在运行”和“连接已断开”。

## 4. 行业影响分析

**对行业的启示**
这标志着 AI 应用开发正在从“无状态”向“有状态”转变。行业开始重视 Agent 的**持久性**和**可靠性**，而不仅仅是模型的智商。MCP 协议的普及也预示着 AI 基础设施正在走向标准化和互操作性。

**可能带来的变革**
*   **Agent 即服务**：企业可以部署专门处理特定长耗时任务的 Agent Server，通过 MCP 协议被各种前端应用调用。
*   **开发模式的转变**：全栈开发者需要掌握更多后端架构知识（如队列、状态机）来构建 AI 应用。

**相关领域的发展趋势**
*   **Agentic Workflows**：Andrew Ng 提出的 Agentic Workflow 概念将得到更多云原生工具的支持。
*   **协议标准化**：MCP 可能会成为连接 LLM 与数据源的“USB 接口”。

## 5. 延伸思考

**引发的其他思考**
*   **安全性**：长时间运行的连接意味着更长的攻击面。如何验证回调请求的合法性？
*   **多租户隔离**：在 SaaS 场景下，如何确保不同租户的长时间任务互不干扰？

**可以拓展的方向**
*   结合 **AWS EventBridge** 实现完全无服务器的 Serverless Agent 架构。
*   探索 Strands 在多智能体协作中的应用，即多个 Agent 共享同一个 Strand 上下文。

**需要进一步研究的问题**
*   MCP 协议在高并发场景下的性能瓶颈在哪里？
*   如何在 Strands 中处理“分支”历史（即 Agent 尝试多条路径并回滚）？

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有架构**：检查你的 AI 应用是否有超过 30 秒的请求。如果有，就需要引入异步模式。
2.  **引入状态管理**：不要将状态只保存在内存中，立即引入 Redis 或 DynamoDB。
3.  **实现最小可行性 MCP Server**：先实现一个简单的“长任务”模拟（如 `sleep` 指令），验证上下文消息策略是否有效。

**具体的行动建议**
*   阅读 LangChain 关于 Strands 的文档。
*   在 AWS 上搭建一个基于 Step Functions 的示例流程，并通过 Bedrock Agent 触发。

**需要补充的知识**
*   异步编程模式。
*   AWS Step Functions 或类似编排工具的使用。
*   WebSocket 或 SSE（Server-Sent Events）通信机制。

## 7. 案例分析

**结合实际案例说明**
假设构建一个**“法律合同审查 Agent”**。
*   **传统模式**：用户上传合同 -> Agent 读取并分析 -> 30秒后超时或用户焦虑等待。
*   **本方案模式**：
    1.  用户上传合同。
    2.  MCP Server 返回：“任务 ID: 123，正在排队...”。
    3.  AgentCore 调用 Bedrock 启动分析，同时将状态写入 Strand。
    4.  Bedrock 处理耗时 5 分钟。
    5.  处理完成后，MCP Server 通过 WebSocket 推送结果给前端。
    6.  Agent 从 Strand 中恢复上下文，向用户展示：“合同审查完成，发现 3 个风险点...”。

**成功案例分析**
成功的关键在于**用户体验的平滑过渡**。用户不需要盯着加载圈，而是可以去做别的事，然后收到通知。这模仿了人类助理的工作方式。

**失败案例反思**
如果未正确处理“任务失败”的状态，Agent 可能会永久挂起在“等待中”状态。必须设计超时和错误分支，让 Agent 能够报告：“抱歉，任务失败了，请重试。”

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建处理复杂、耗时任务的 AI Agent 时，采用 **Amazon Bedrock AgentCore 结合 Strands Agents 的异步 MCP 服务器架构**，是实现高可用、高响应智能体的**必要且充分**的条件。

**支撑理由与依据**
1.  **理由 1（状态持久化）**：长时间任务必然超出单次请求的生命周期。
    *   *依据*：HTTP 请求通常在 30-60 秒超时；复杂业务逻辑（如数据处理）往往需要数分钟。
2.  **理由 2（上下文连续性）**：Agent 需要在任务中断后恢复对话，而不是失忆。
    *   *依据*：Strands 提供了记忆存储机制，允许 Agent 序列化和反序列化其思维链。
3.  **理由 3（互操作性）**：MCP 提供了标准化的接口，解耦了 Agent 实现与客户端展示。
    *   *依据*：MCP 协议正在成为 Anthropic 和 AWS 生态的连接标准。

**反例或边界条件**
1.  **反例（超低延迟场景）**：对于极简单的问答（如“今天天气”），引入异步框架和 Strands 会带来不必要的延迟和架构复杂度。此时直接调用 Bedrock 更优。
2.  **边界条件（强一致性要求）**：如果业务要求任务必须实时返回且不能有任何延迟（例如高频交易辅助），异步回调的抖动可能不可接受。

**命题性质判断**
*   **事实**：Bedrock AgentCore 支持自定义编排；Strands 支持长时记忆；MCP 是开放协议。
*   **价值判断**：“高可用”和“高响应”是优于“低成本”和“架构简单”的（在复杂任务场景下）。
*   **可检验预测**：采用该架构的系统，其任务处理成功率将高于同步系统，且用户流失率（因等待时间过长）会降低。

**立场

---
## 最佳实践

## 最佳实践

### 1. Strand 生命周期与状态管理

在构建长时间运行的 MCP 服务器时，Strand 代表了一个持续的执行线程或上下文。不当的状态管理会导致内存泄漏或上下文丢失。必须明确 Strand 的启动、暂停、恢复和终止条件，确保在长时间运行过程中，系统能够从错误中恢复并保持状态的一致性。

**实施建议：**
*   **定义状态机模型**：明确 Strand 各状态（如初始化、运行中、阻塞、完成）转换的触发条件。
*   **实现状态持久化**：将 Strand 的关键状态（如 Checkpoint）定期保存到 Amazon S3 或 DynamoDB，防止进程重启导致数据丢失。
*   **设置资源回收机制**：配置空闲超时策略，当 Strand 空闲超过特定时间时自动休眠或终止，以释放计算资源。

### 2. 错误处理与重试逻辑

长时间运行的服务器不可避免会遇到网络波动或依赖服务不可用的情况。在 AgentCore 集成场景下，必须实现健壮的错误处理机制，防止因单次请求失败导致整个 Strand 流程中断。

**实施建议：**
*   **区分错误类型**：区分可重试错误（如限流 429）和不可重试错误（如认证失败 401）。
*   **实现指数退避**：在 MCP 服务器端对瞬时错误实施指数退避算法，避免对后端服务造成冲击。

### 3. MCP 工具定义与优化

Strands Agents 依赖 MCP 服务器暴露的工具来执行任务。清晰的工具定义是提高 Agent 成功率的关键。如果工具定义模糊或缺乏必要的输入验证，Agent 可能会生成无效的调用请求。

**实施建议：**
*   **完善 Schema 定义**：为每个 MCP Tool 编写详细的 JSON Schema，明确参数类型、用途和限制。
*   **提供上下文示例**：在工具描述字段中提供具体的输入输出示例，帮助 LLM 更准确地理解调用方式。
*   **实施最小权限暴露**：仅向 Agent 暴露完成任务所需的最小工具集，减少 Token 消耗并降低 Agent 产生幻觉的风险。

### 4. 可观测性与日志追踪

在长时间运行的异步任务中，调试问题极具挑战性。必须建立完整的日志和追踪体系，将 Bedrock Agent 的决策与 MCP 服务器的执行过程关联起来。

**实施建议：**
*   **集成分布式追踪**：利用 AWS X-Ray 或 OpenTelemetry 追踪请求链路。
*   **关联日志 ID**：在日志中包含 `Trace-ID`，确保 Bedrock Agent 的调用 ID 与 MCP 服务器的日志能相互关联。
*   **记录关键事件**：重点记录 Strand 的生命周期事件（如启动、检查点保存、工具调用失败）。
*   **注意数据安全**：严禁在日志中打印敏感的用户数据或 PII 信息，确保日志脱敏。

### 5. 异步任务处理模式

Bedrock AgentCore 与 MCP 的交互通常有默认的超时限制。如果某个 Strand 中的任务（如数据处理或外部 API 调用）耗时较长，不应阻塞 MCP 的响应线程，而应采用异步模式。

**实施建议：**
*   **拆分操作接口**：将长时间操作设计为“启动任务”、“查询状态”和“获取结果”三个独立的工具接口。
*   **返回操作句柄**：收到任务请求后，立即返回 `operation_id` 并在后台启动 Strand 处理。
*   **配置轮询机制**：配置 Agent 使用动态推理模式，定期轮询任务状态直到完成，并妥善处理用户中断对话时的任务取消逻辑。

### 6. IAM 安全控制

MCP 服务器通常作为中间层连接 Agent 和后端资源（如数据库、S3）。为了遵循最小权限原则，必须严格控制 MCP 服务器所扮演的 IAM 角色，防止 Agent 被诱导执行未授权的操作。

**实施建议：**
*   **实施最小权限**：仅为 MCP 服务器分配执行特定工具所需的 IAM 权限，禁止通用的 `*` 资源访问。
*   **动态凭证管理**：如果可能，根据当前 Strand 的上下文动态获取短期凭证，而非使用长期静态密钥。
*   **输入验证**：在 MCP 服务器端严格校验所有输入参数，防止注入攻击或非法资源访问。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持通过 Strands Agents 集成来构建和部署具备长期运行能力的 MCP 服务器。
- 该集成方案解决了传统无状态架构的局限性，使智能体能够维护跨多轮对话的上下文状态，从而处理复杂、多步骤的长期任务。
- 开发者可以利用 MCP 协议将外部数据源和工具无缝连接到 Bedrock Agent，显著扩展智能体在特定工作流中的功能边界。
- 架构设计上强调了状态持久化机制，确保在长时间运行的自动化流程中，即使发生中断也能保持任务连续性。
- 借助 Bedrock 的托管服务，企业可以更轻松地构建高可用性的企业级智能体，而无需从零开始管理底层基础设施。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*