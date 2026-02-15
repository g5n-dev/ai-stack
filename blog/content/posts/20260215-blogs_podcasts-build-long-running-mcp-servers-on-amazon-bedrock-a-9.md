---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理"
date: 2026-02-15T12:10:18+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长时运行", "上下文管理", "AI 代理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何利用 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够处理长时间运行任务的生产级 MCP 服务器。主要内容包括以下三点： 1. **上下文消息策略**：引入了一种机制，通过在服务器与客户端之间维持持续的通信流，确保在长时间操作期间上下文的一致性和连接的稳定"
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

在这篇文章中，我们将为您提供一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，以便在长时间运行的操作期间保持服务器与客户端之间的持续通信。接着，我们构建一个异步任务管理框架，使您的 AI 代理能够在不阻塞其他操作的情况下启动长时运行进程。最后，我们将展示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合，构建可投入生产环境的 AI 代理，从而可靠地处理复杂且耗时的操作。

---
## 导语

构建能够可靠处理长时间运行任务的 AI 代理是当前技术落地的一大难点。本文将介绍如何利用 Amazon Bedrock AgentCore 和 Strands Agents 集成，通过上下文消息策略与异步任务管理框架，解决服务端与客户端的持续通信及进程阻塞问题。阅读本文，您将掌握一套构建生产级 AI 代理的完整方法，从而在复杂业务场景中实现高效、稳定的自动化处理。

---
## 摘要

本文介绍了如何利用 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够处理长时间运行任务的生产级 MCP 服务器。主要内容包括以下三点：

1.  **上下文消息策略**：引入了一种机制，通过在服务器与客户端之间维持持续的通信流，确保在长时间操作期间上下文的一致性和连接的稳定性。
2.  **异步任务管理框架**：开发了一套框架，允许 AI 代理启动耗时较长的流程，同时不会阻塞其他操作的执行，从而提升系统的并发处理能力。
3.  **集成与实现**：展示了如何将这些策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，构建出可靠、能够处理复杂且耗时任务的生产级 AI 代理。

---
## 评论

**中心观点**
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的架构范式，旨在通过引入“上下文消息策略”和“异步任务管理框架”，解决模型上下文协议（MCP）服务器在执行长周期任务时的状态保持与通信中断问题。

**深入评价与支撑理由**

**1. 内容深度：从“请求-响应”向“有状态协同”的架构跨越**
*   **支撑理由**：[事实陈述] 传统的 LLM 应用多采用无状态的 HTTP 请求-响应模式，难以处理分钟级的业务流程。文章提出的“上下文消息策略”实际上是在构建一个**虚拟会话层**。它不依赖底层的 TCP 长连接，而是通过在应用层维持上下文锚点，使 Bedrock Agent 能够在多次推理轮次中“拼凑”出完整的长任务状态。这种设计论证了如何在不改变底层推理模型（仍是无状态的）的前提下，在 Agent 架构层实现“有状态”的业务逻辑。
*   **反例/边界条件**：[你的推断] 如果长任务执行过程中发生严重的上下文切换或中间数据量超过 Token 限制，单纯的“消息策略”可能会失效。此外，如果 Bedrock Agent 的路由策略发生抖动，这种松散的上下文关联可能导致任务状态丢失。

**2. 实用价值：填补了生成式 AI 在企业级工作流中的空白**
*   **支撑理由**：[作者观点] 企业级应用（如 RPA、数据 ETL、代码部署）往往需要耗时数分钟甚至数小时，且必须具备可观测性。文章引入的“异步任务管理框架”将 AI 的角色从“直接执行者”转变为“指挥官”，通过解耦决策与执行，使得 AI Agent 可以接入企业现有的异步作业系统。这为解决目前 AI Agent “只能闲聊，不能干活”的痛点提供了极具指导意义的落地路径。
*   **反例/边界条件**：[事实陈述] 这种架构显著增加了系统的复杂度。对于简单的查询类任务，引入异步框架和上下文管理是过度设计，不仅增加延迟，还提高了 Bedrock 的调用成本。

**3. 创新性：对 MCP 协议的“企业级”扩展**
*   **支撑理由**：[你的推断] MCP（Model Context Protocol）目前主要被视为一种连接数据源的标准化接口，多用于读取知识库或工具调用。该文章的创新点在于将 MCP 服务器“服务化”，使其具备独立的生存周期和任务处理能力，而不仅仅是被动的工具。通过 Strands Agents 的集成，实际上是在 MCP 之上构建了一层微服务编排逻辑，这是对 MCP 协议应用场景的重要拓展。
*   **反例/边界条件**：[作者观点] 这种创新依赖于 Amazon Bedrock 的私有生态。如果用户使用的是 OpenAI 的 ChatGPT 或开源的 LlamaStack，该方案的迁移性较差，存在厂商锁定的风险。

**4. 行业影响：推动 Agent 从“玩具”走向“SOP”**
*   **支撑理由**：[事实陈述] 目前行业面临的主要瓶颈是 Agent 的可靠性。长任务失败率高是阻碍其进入生产环境的核心原因。如果该文章提出的框架能有效降低长任务的掉线率并增加可视性，它将直接推动 AI Agent 进入标准作业程序（SOP）领域，如自动化运维、长文档合规性审查等，加速“AI 员工”的落地。
*   **反例/边界条件**：[你的推断] 这种模式可能会引发新的安全挑战。长周期的异步任务意味着权限验证的窗口被拉长，如何保证任务中途不会被恶意劫持或重放攻击，是行业需要共同面对的新问题。

**5. 争议点与批判性思考：状态管理的成本与复杂性**
*   **争议点**：[你的推断] 文章似乎倾向于由 Agent Core 来管理状态，但在高并发场景下，这种中心化的状态管理可能成为性能瓶颈。
*   **不同观点**：[作者观点] 另一种更轻量的思路是让客户端持有状态 ID，完全无状态地驱动服务端。虽然这会增加客户端的开发负担，但在微服务架构中可能更具弹性。文章的方案虽然全面，但可能略显厚重。

**实际应用建议**
1.  **任务分级处理**：不要对所有任务启用此框架。建议设置阈值（如执行时间超过 30 秒），仅对长任务启用 Strands Agents 和异步上下文管理，短任务保持同步调用以降低延迟。
2.  **引入“心跳”机制**：在实现上下文消息策略时，务必加入心跳检测。如果 Bedrock Agent 长时间未收到上下文更新，应主动查询任务状态，防止因网络分区导致的“幽灵任务”。
3.  **Sidecar 模式**：在部署 MCP Server 时，建议采用 Sidecar 模式将任务队列与逻辑解耦，避免长任务阻塞 MCP Server 的主线程，确保其始终能响应 Agent 的状态查询请求。

**可验证的检查方式**
1.  **中断恢复测试**：在长任务执行过程中人为断开 Bedrock Agent 与 MCP Server 的网络连接，或重启 Agent Core 实例，验证任务是否能在连接恢复后通过上下文消息继续执行，而非从头开始。
2.  **并发压力指标**：逐步增加长任务的并发数量，观察上下文消息策略导致的 Token 消耗增长曲线。重点监控“元数据 Token”占比是否随着任务时长线性增长，以此评估架构的经济性。
3.  **状态一致性观察窗口**：在异步任务完成后

---
## 技术分析

## 技术分析

### 1. 核心架构与设计思路
文章主要探讨了在 Amazon Bedrock AgentCore 环境下，利用 Strands Agents 框架构建支持长周期运行的 MCP (Model Context Protocol) 服务器的技术路径。其核心逻辑在于解决 LLM 应用在处理耗时任务（如代码生成、数据分析）时的状态管理与异步通信问题。

该架构采用了**控制流与执行流解耦**的设计模式：
*   **控制层**：由 Bedrock AgentCore 负责，处理推理调度和工具调用决策。
*   **执行层**：由 MCP Server 结合 Strands Agents 构成，负责维持任务的生命周期和状态记忆。
这种分离机制使得系统能够在 Bedrock 无状态特性的基础上，实现类似“有状态长连接”的业务处理能力。

### 2. 关键技术机制

*   **上下文消息策略**
    针对长时任务导致的 Token 积累和注意力漂移问题，文章强调了上下文管理的重要性。这涉及如何在任务暂停和恢复的过程中，精简并传递关键的状态信息，以确保 LLM 对任务目标的一致性理解。

*   **异步任务处理**
    为了避免阻塞主线程或超出 API 超时限制，系统采用异步模式处理耗时操作。通常的实现逻辑包括：
    1.  LLM 发起指令，MCP Server 接收并返回任务 ID（Task ID）。
    2.  连接转为非阻塞模式（轮询或回调）。
    3.  后台进程（如 Lambda/ECS）执行具体逻辑。
    4.  通过 Session ID 恢复会话，并将结果反馈给 Agent。

### 3. 技术难点与应对

*   **超时与会话恢复**
    LLM 调用通常存在严格的超时限制。解决方案通常涉及利用 Bedrock 的会话控制机制（如 `returnControl`），在任务发起后释放控制权，待后台任务完成后，通过携带特定上下文信息的 API 调用恢复对话。

*   **状态一致性**
    在任务恢复阶段，直接返回海量原始数据可能导致 LLM 理解困难。技术实现上通常采用**摘要注入**机制，即向 LLM 提供经过处理的任务状态摘要（例如：“之前执行了任务 A，当前状态为完成，请继续步骤 B”），而非原始日志，以确保决策的连贯性。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化长连接会话的生命周期管理

**说明**:
在构建长时间运行的 MCP (Model Context Protocol) 服务器时，必须妥善管理 Agent 的会话状态。由于 Bedrock AgentCore 的 Strands Agents 可能会处理跨越数小时或数天的任务，简单的超时设置会导致任务中断。需要实现一种机制，既能保持会话活跃以完成复杂任务，又能防止资源泄漏。

**实施步骤**:
1. 实现基于心跳的会话保活机制，定期在后台线程中发送轻量级状态更新。
2. 配置合理的空闲超时与最大存活时间策略，在任务完成后自动释放资源。
3. 使用状态存储（如 DynamoDB）持久化会话上下文，以便在连接重建时恢复状态。

**注意事项**:
避免无限期地保持连接打开，应设定业务逻辑允许的最大会话期限，并在日志中监控长时间运行的会话数量，防止内存溢出。

---

### 实践 2：构建健壮的错误重试与幂等性机制

**说明**:
长运行任务极易受到网络波动或底层服务瞬断的影响。对于 Strands Agents 调用的 MCP 工具，必须实现自动重试逻辑。同时，为了确保重试不会导致重复操作（例如重复下单或重复写入数据库），所有的服务端操作必须具备幂等性。

**实施步骤**:
1. 在 MCP 服务器客户端中集成指数退避算法，以处理 Bedrock Agent 的 API 限流或临时错误。
2. 为每个请求生成唯一的幂等键，并在业务逻辑层处理该键，确保同一请求多次执行只产生一次效果。
3. 区分可重试错误（如 5xx 错误、网络超时）与不可重试错误（如 4xx 验证错误），避免无意义的重试消耗配额。

**注意事项**:
监控重试频率，设置最大重试次数阈值。如果达到阈值仍未成功，应将任务标记为失败并触发人工介入流程，而不是无限循环。

---

### 实践 3：实施细粒度的流式响应与状态反馈

**说明**:
对于长运行任务，用户不应长时间面对黑屏等待。利用 Bedrock 的流式传输能力，MCP 服务器应向 AgentCore 实时返回中间状态、进度百分比或部分结果。这能显著提升用户体验，并让 Strands Agent 能够根据中间结果动态调整后续步骤。

**实施步骤**:
1. 修改 MCP 工具接口，支持 Server-Sent Events (SSE) 或流式响应格式。
2. 在代码中将长任务拆解为多个阶段，每个阶段完成后发送“心跳”或“检查点”数据给 Agent。
3. 配置 AgentCore 的提示词，使其能够解析并展示这些中间状态信息，而不是仅在最终结束时才响应。

**注意事项**:
流式传输的数据量不宜过大，避免频繁发送微小状态更新阻塞网络带宽。建议按批次或按时间间隔（如每 5 秒）发送状态更新。

---

### 实践 4：异步任务编排与解耦设计

**说明**:
并非所有长运行任务都应该在 HTTP 请求的上下文中同步完成。为了防止 Bedrock Agent 超时，MCP 服务器应采用“即发即弃”模式，立即返回一个任务 ID，然后在后台异步处理实际工作，Agent 随后可以通过查询接口获取结果。

**实施步骤**:
1. 引入消息队列（如 Amazon SQS）或后台任务处理框架，接收来自 AgentCore 的工具调用请求。
2. 设计两个 MCP 工具接口：一个用于启动任务，返回 `task_id` 和 `status="QUEUED"`；另一个用于查询任务状态和结果。
3. 在 Strands Agent 的逻辑中配置轮询机制，定期检查任务状态直到完成。

**注意事项**:
确保异步处理器的可扩展性，能够应对高并发的任务请求。同时，必须提供取消任务的接口，以便用户或 Agent 中止不再需要的后台作业。

---

### 实践 5：强化可观测性与链路追踪

**说明**:
在复杂的 Strands Agents 调用链中，定位长运行任务的瓶颈或失败点极具挑战性。必须实施全面的日志记录、指标监控和分布式追踪，以便可视化从 Agent 到 MCP 服务器的完整请求路径。

**实施步骤**:
1. 在 MCP 服务器的所有日志中包含 `trace_id`，确保其能与 AWS X-Ray 或 CloudWatch 的追踪 ID 关联。
2. 记录关键业务指标，如工具执行耗时、输入/输出 Token 消耗量以及错误率。
3. 为长运行任务设置结构化日志，记录每个阶段的开始和结束时间，便于事后分析耗时分布。

**注意事项**:
避免记录敏感信息（如 PII 数据或完整的 API 密钥）到日志中。确保日志级别配置合理，生产环境通常设置为 INFO 或 WARN，避免 DEBUG 日志造成的性能损耗。

---

### 实践 6：严格的安全验证与最小权限原则

**说明**:
MCP 服务器作为 Agent 访问后端资源和数据的

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够维护长期对话状态和记忆的 MCP 服务器。
- 通过将 Strands Agents 的记忆机制与 MCP 协议相结合，该架构解决了传统无状态模型难以处理复杂、多步骤工作流的局限性。
- 该集成方案显著增强了智能体的上下文感知能力，使其能够在跨越多个会话的长时间周期内持续执行任务。
- 开发者可以利用这一框架在 Bedrock 上部署具备持久化记忆能力的 AI 应用，而无需自行管理底层的状态同步基础设施。
- 此举标志着 Bedrock 在支持高级 Agent 架构方面的演进，为构建需要长期交互和任务追踪的企业级应用提供了标准化的技术路径。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*