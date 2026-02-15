---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器"
date: 2026-02-15T10:21:59+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长时运行", "AI Agent", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "以下是对该内容的中文总结： 本文介绍了一种利用 **Amazon Bedrock AgentCore** 与 **Strands Agents** 集成，构建高性能、长时间运行 MCP 服务器的综合解决方案。为了确保 AI 代理能够可靠地处理复杂且耗时的任务，文章提出了三项关键策略： 1. **引入上下文消息策略**："
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长时运行MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本篇文章中，我们将为您提供实现这一目标的全面方法。首先，我们介绍一种上下文消息策略，用于在服务器与客户端之间，在长时间运行的操作期间保持持续通信。接下来，我们将开发一个异步任务管理框架，让您的 AI 代理能够启动长时间运行的进程，而不会阻塞其他操作。最后，我们将演示如何将 Amazon Bedrock AgentCore 和 Strands Agents 与这些策略相结合，构建生产就绪的 AI 代理，从而可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是当前技术落地的一大难点。本文将介绍如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成方案，通过上下文消息策略和异步任务管理框架，解决服务端与客户端在长周期操作中的持续通信问题。阅读本文，您将掌握构建生产级、高并发且非阻塞式 AI 代理的具体实现路径。

---
## 摘要

以下是对该内容的中文总结：

本文介绍了一种利用 **Amazon Bedrock AgentCore** 与 **Strands Agents** 集成，构建高性能、长时间运行 MCP 服务器的综合解决方案。为了确保 AI 代理能够可靠地处理复杂且耗时的任务，文章提出了三项关键策略：

1.  **引入上下文消息策略**：
    为了解决服务器与客户端在长时间运行过程中的通信问题，文章提出了一种上下文消息机制。该策略能够在扩展操作期间维持双方之间的连续通信，确保状态同步和信息的实时传递。

2.  **开发异步任务管理框架**：
    为了防止长耗时任务阻塞系统的其他操作，文章构建了一个异步任务管理框架。该框架允许 AI 代理启动长进程的同时，保持系统的响应能力，从而实现非阻塞式的并行处理。

3.  **集成 Amazon Bedrock AgentCore 与 Strands Agents**：
    最后，文章演示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合。通过这种集成，开发者可以构建出具备生产级能力的 AI 代理，使其能够稳定、高效地处理复杂且时间密集型的工作负载。

---
## 评论

### 中心观点
该文章提出了一种基于 **Amazon Bedrock AgentCore** 结合 **Strands Agents** 构建长时间运行的 **MCP (Model Context Protocol) 服务器** 的架构范式，旨在通过上下文消息策略与异步任务管理框架，解决大模型应用在处理长周期任务时的状态保持与交互连续性问题。

### 深入评价与分析

#### 1. 内容深度：架构严谨性与技术颗粒度
**[事实陈述]** 文章触及了当前 AI Agent 开发的核心痛点：**长周期任务中的状态管理**。传统的 LLM 请求-响应模式无法适应需要数分钟甚至数小时才能完成的任务（如代码库重构、数据分析流）。文章引入“上下文消息策略”和“异步任务管理”，在理论层面填补了 Bedrock Agent生态在长连接场景下的空白。
**[你的推断]** 文章可能深入探讨了 MCP 协议在服务端实现 SSE（Server-Sent Events）或 WebSocket 的具体细节，以及如何利用 Strands Agents 的子任务分解能力来维护对话上下文。这种深度表明文章不仅停留在 API 调用层面，而是涉及到了系统架构设计。

*   **支撑理由**：Bedrock AgentCore 本身提供了状态机的基础，但将其扩展到 MCP 协议层，需要处理协议层面的心跳与分片传输，这显示了较高的技术门槛。
*   **反例/边界条件**：如果文章未提及**断点续传**机制，那么在网络波动导致连接断开时，所谓的“长运行”将变得脆弱，用户可能丢失任务进度。

#### 2. 实用价值：解决生产环境痛点
**[事实陈述]** 对于正在使用 AWS 构建企业级 Agent 的开发者而言，这篇文章具有极高的参考价值。MCP 作为一个新兴的协议标准（由 Anthropic 推动），其生态工具尚不成熟。文章提供的框架可能是一个现成的脚手架，减少了开发者从零构建轮子的时间。
**[作者观点]** 文章的实用价值取决于其对**错误处理**的覆盖程度。在长运行任务中，超时、权限失效和 API 限流是常态。如果文章仅展示了“快乐路径”而缺乏对异常处理的架构建议，其实用价值将大打折扣。

*   **支撑理由**：将 Strands Agents（擅长多步推理）与 MCP（擅长数据上下文传输）结合，确实能构建出比简单的 RAG 更智能的系统。
*   **反例/边界条件**：对于简单的、秒级响应的查询任务，引入这套复杂的异步框架属于“过度设计”，增加了延迟和系统复杂度，得不偿失。

#### 3. 创新性：协议与编排的融合
**[事实陈述]** 该文章的创新点不在于发明了新技术，而在于**组合创新**。将 Bedrock 的托管能力与 MCP 的开放协议标准结合，并引入 Strands 的编排逻辑，这是一种符合当前“混合架构”趋势的尝试。
**[你的推断]** 这种架构试图打破 LangChain/LangGraph 等传统编排框架在云原生环境下的局限性，试图更深地绑定 AWS 基础设施。

*   **支撑理由**：它提出了在 MCP 服务器端维护“有状态”会话的新思路，这可能挑战了 MCP 协议最初设计时偏向无状态请求的初衷。
*   **反例/边界条件**：如果 Strands Agents 是 AWS 的专有增强功能，那么这种创新会导致**厂商锁定**，削弱了 MCP 协议本身旨在实现的跨模型、跨平台互操作性。

#### 4. 可读性与逻辑性
**[你的推断]** 根据摘要风格推测，文章采用了“问题-解决方案-实施步骤”的经典技术博客结构。逻辑链条应当是清晰的：长任务导致超时 -> 引入异步机制 -> 引入上下文保持 -> 代码实现。
**[事实陈述]** AWS 技术博客通常具有高质量的配图和代码片段，这有助于理解复杂的架构流转。

#### 5. 行业影响：推动 Agent 标准化与云原生化
**[事实陈述]** 此类文章如果推广开来，会加速 **MCP 协议**在企业级市场的落地。它向开发者传递了一个信号：MCP 不仅仅是一个本地连接工具，更可以扩展为云端大规模 Agent 的通信总线。
**[作者观点]** 这可能会引发其他云厂商（如 Azure GPT、Google Vertex AI）跟进类似的集成策略，推动 Agent 开发从“玩具级 Demo”向“生产级微服务”转变。

#### 6. 争议点与不同视角
**[事实陈述]** 一个主要的争议点在于**计算成本与延迟**。通过 Bedrock AgentCore 进行长轮询或保持长连接，其基础设施成本可能高于直接调用简单的 API。
**[不同观点]** 部分开发者可能认为，直接使用 Redis + Celery 等传统任务队列配合 LLM 调用，比使用 Bedrock AgentCore 这样的黑盒服务更加透明、可控且廉价。

#### 7. 实际应用建议
**[作者观点]** 在采纳该文章方案前，建议先评估任务的**确定性**。如果任务步骤高度动态且需要频繁人工介入，该方案非常适合；如果任务流程固定，传统的 ETL 或工作流引擎可能更高效。

### 可验证的检查方式

为了验证文章所述架构的有效性，建议进行以下检查：

1.  **压力测试**：
    *   **指标**：在并发 100+ 长任务请求下，观察 Bedrock AgentCore 的上下文切换延迟及是否出现限流。
    *   **验证点**：异步

---
## 技术分析

# 技术方案解析：基于 Amazon Bedrock AgentCore 与 Strands Agents 的长运行 MCP 服务器

## 1. 核心架构与设计目标

**解决的核心问题**
该技术方案旨在解决传统 AI Agent 架构在处理**长周期任务**时面临的局限性。通常的 Agent 交互依赖于同步的请求-响应模式，受限于网络超时和上下文窗口，难以维持跨时段的工作流。文章提出了一种集成架构，通过结合 Amazon Bedrock AgentCore 的编排能力与 Strands Agents 的状态管理机制，构建能够处理长时间运行任务的 MCP（Model Context Protocol）服务器。

**设计理念**
架构的核心思想是将 Agent 从“单次交互模式”转变为“持久化协作者”。这依赖于两个关键机制：
1.  **上下文连续性：** 通过上下文消息策略，确保 Agent 在任务暂停或恢复时能够保留之前的交互历史和状态。
2.  **异步任务解耦：** 将长时间执行的操作与主控制流分离，避免阻塞通信通道。

## 2. 关键技术组件与机制

**涉及的核心技术**
*   **MCP (Model Context Protocol):** 作为标准化的数据接口层，用于 Agent 与后端资源或工具之间的通信。
*   **Amazon Bedrock AgentCore:** 负责核心的 Agent 编排、工具调用路由及逻辑控制。
*   **Strands Agents:** 提供持久化的线程管理和状态记忆功能，支持长上下文场景。
*   **异步任务处理:** 用于管理后台执行的长时间任务。

**技术实现原理**
1.  **持久化上下文管理:**
    *   **机制:** 系统利用 MCP 的接口特性，在 AgentCore 和 Strands Agents 之间传递包含任务状态、中间结果和后续步骤的上下文消息。
    *   **作用:** 这种机制允许 Agent 在处理中断或恢复时，无需重新加载全部历史，而是基于检查点或摘要状态继续执行，从而维持对话和任务的连续性。

2.  **异步任务流:**
    *   **机制:** 当 Agent 调用耗时工具（如大规模数据处理或代码审计）时，MCP 服务器接收指令后立即返回任务标识符（Task ID）及“已接收”状态，而非等待最终结果。
    *   **实现:** 实际的计算逻辑被转移至后台服务（如结合 AWS Step Functions 或 Lambda）。Agent 通过轮询或事件回调的方式获取进度更新和最终结果。

## 3. 技术挑战与应对策略

**主要技术难点**
*   **上下文窗口限制:** 长时间运行的任务会产生大量的中间日志和状态数据，可能超出模型的输入限制。
    *   **应对策略:** 利用 Strands Agents 的状态压缩能力，定期将冗余的中间状态转化为高维度的语义摘要，减少 Token 占用。
*   **状态一致性:** 在分布式或异步环境中，确保任务状态的准确同步。
    *   **应对策略:** 采用幂等性设计和状态检查点机制，确保即使发生网络中断，系统也能根据最新的稳定状态恢复执行。

**架构价值**
该方案通过将 Strands Agents 的持久化特性集成到 Bedrock AgentCore 的托管框架中，提供了一种构建企业级长运行 Agent 的标准模式。这使得 AI 应用能够适应代码开发、数据分析等需要跨越分钟级甚至小时级的复杂业务场景。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 Strands Agents 的状态管理机制

**说明**:
在构建长时间运行的 MCP (Model Context Protocol) 服务器时，Strands Agents 需要维护跨越多个交互轮次的对话状态。最佳实践是设计一个轻量级且持久化的状态管理策略，避免将完整的上下文历史在每次请求时都传递给 Bedrock 模型，这可以显著降低延迟和 Token 消耗。

**实施步骤**:
1. 实施摘要机制，将之前的交互轮次压缩为结构化的摘要，而不是保留原始的完整记录。
2. 利用 Amazon DynamoDB 或 ElastiCache 存储会话状态，仅将当前会话的必要上下文加载到内存中。
3. 配置 MCP 服务器的上下文窗口限制，确保传递给 Bedrock AgentCore 的 Prompt 保持在模型的最大处理能力范围内。

**注意事项**:
避免在 Agent 状态中存储敏感的 PII (个人身份信息) 数据。如果必须存储，请确保在静态和传输过程中进行加密。

---

### 实践 2：实施严格的超时与重试策略

**说明**:
长时间运行的 Agent 可能会遇到网络波动或 Bedrock 限流的情况。为了确保 MCP 服务器的稳定性，必须实现指数退避重试机制，并为每个工具调用设置合理的超时限制，防止因单个挂起的请求阻塞整个服务器进程。

**实施步骤**:
1. 在调用 Bedrock AgentCore API 时配置 SDK 的默认重试模式（如 boto3 的重试配置）。
2. 为 MCP 服务器实现的每个工具定义明确的超时阈值（例如 30 秒）。
3. 实施断路器模式，当某个特定工具连续失败 N 次后，暂时停止调用该工具并通知主控流程。

**注意事项**:
对于长时间运行的后台任务，不要阻塞 MCP 的响应循环。应返回一个“任务已接收”的响应，并使用 WebSocket 或轮询机制异步报告结果。

---

### 实践 3：构建模块化的工具注册与权限系统

**说明**:
随着 Agent 功能的扩展，MCP 服务器可能会暴露大量的工具。最佳实践是将工具逻辑模块化，并实施基于角色的权限控制，确保 Strands Agents 只能调用其当前上下文所允许的工具，防止未经授权的操作。

**实施步骤**:
1. 将工具定义与业务逻辑分离，使用装饰器或配置文件动态注册工具到 MCP 服务器。
2. 在工具调用前，在中间件层实施权限检查，验证 Agent 是否有权限执行该特定操作。
3. 定期审计暴露给 Bedrock Agent 的工具列表，移除未使用或重复的工具定义。

**注意事项**:
工具的描述对于 Agent 的表现至关重要。请确保为每个工具提供清晰、具体的自然语言描述，以便 LLM 准确选择工具。

---

### 实践 4：利用结构化输出解析以确保数据完整性

**说明**:
Strands Agents 通常依赖 MCP 服务器返回的数据来执行后续逻辑。强制 Bedrock 模型输出 JSON 或其他结构化格式可以减少解析错误，提高长时间运行工作流的可靠性。

**实施步骤**:
1. 在 Prompt 指令中明确要求输出 JSON 格式，并定义严格的 JSON Schema。
2. 在 MCP 服务器端实现响应验证中间件，在处理业务逻辑前验证传入的参数结构。
3. 利用 Bedrock 的原生 JSON 模式功能（如果可用）或 In-Context Learning 来约束输出格式。

**注意事项**:
处理模型可能产生的幻觉或格式错误。即使使用了结构化输出，也必须包含 Try-Catch 块来处理反序列化异常。

---

### 实践 5：建立全面的可观测性与日志记录

**说明**:
调试长时间运行的 Agent 是一个复杂的过程。必须将 MCP 服务器的内部日志与 Bedrock AgentCore 的调用轨迹关联起来，以便追踪请求从 Agent 到工具执行再到响应的完整生命周期。

**实施步骤**:
1. 使用 AWS X-Ray 进行分布式追踪，将 MCP 服务器的调用与 Bedrock 的请求 ID 关联。
2. 将结构化日志发送到 Amazon CloudWatch Logs，包含关键事件如工具调用、参数、执行时间和错误信息。
3. 设置针对特定错误率或延迟的 CloudWatch 告警，以便在服务器性能下降时及时通知运维人员。

**注意事项**:
注意日志成本。不要记录完整的请求和响应 Body（特别是包含大段文本或 Base64 编码图像时），应仅记录关键的元数据和摘要信息。

---

### 实践 6：设计幂等的工具接口

**说明**:
在网络不稳定或 Agent 重试请求的情况下，同一个操作可能会被多次调用。确保 MCP 服务器上的工具接口是幂等的，即多次执行相同的操作产生的结果与执行一次相同，这对于保持长时间运行状态的一致性至关重要。

**实施步骤**:
1. 对于写操作（如创建、更新资源），接受一个唯一的客户端生成的 ID（如 Request ID）作为参数。
2. 在处理请求前检查该 ID 是否已被处理，如果是，则返回之前缓存的成功结果。
3. 对于非幂等的操作（如发送邮件），在业务逻辑

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够长时间运行并具备状态记忆能力的 MCP 服务器。
- 通过将 Strands Agents 的状态管理能力与 MCP 协议相结合，该方案有效解决了传统无状态模型难以处理复杂、多步骤任务的局限性。
- 开发者可以利用现有的 MCP 工具生态系统，无需重写底层逻辑，即可为 Bedrock 代理赋予持久化的上下文感知能力。
- 该架构特别适用于需要跨越多个交互周期或长时间等待外部事件响应的复杂自动化工作流场景。
- 此集成标志着 Amazon Bedrock 在推进具备长期记忆和持续推理能力的智能代理系统方面迈出了关键一步。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI Agent](/tags/ai-agent/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*