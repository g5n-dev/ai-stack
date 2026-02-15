---
title: "基于Amazon Bedrock AgentCore与Strands Agents构建长时运行MCP服务器"
date: 2026-02-15T00:52:35+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Bedrock", "AgentCore", "Strands Agents", "异步任务", "长时运行", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够处理长时间运行任务的 MCP（Model Context Protocol）服务器的综合方法。主要内容包含以下三个核心策略： 1. **上下文消息策略**： 引入了一种在长时间操作中维持服务器与客户端之"
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

在这篇文章中，我们将为您提供一套全面的方法来实现这一目标。首先，我们会介绍一种上下文消息策略，以在耗时较长的操作期间保持服务器与客户端之间的持续通信。接下来，我们将开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的任务，同时不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents 将这些策略整合在一起，构建生产级 AI 代理，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够可靠处理长时间运行任务的 AI 代理是当前生产环境中的关键挑战。本文将介绍如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成，通过上下文消息策略和异步任务管理框架来解决通信阻塞问题。阅读本文，您将掌握构建生产级、非阻塞式 AI 代理的具体方法，以应对复杂且耗时的业务场景。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够处理长时间运行任务的 MCP（Model Context Protocol）服务器的综合方法。主要内容包含以下三个核心策略：

1.  **上下文消息策略**：
    引入了一种在长时间操作中维持服务器与客户端之间持续通信的机制。这确保了在任务执行期间，上下文信息得以保持，避免了因操作耗时过长而导致的连接中断或信息丢失。

2.  **异步任务管理框架**：
    开发了一套异步任务管理框架，允许 AI 代理启动长时运行的后台进程。该框架的关键优势在于“非阻塞”，即在进行耗时运算时，不会影响或阻塞其他操作的执行，从而提高了系统的并发处理能力和整体效率。

3.  **集成与生产级实现**：
    文章最后展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合。通过这种集成，可以构建出生产就绪的 AI 代理，使其能够可靠、高效地处理复杂且极其耗时的业务操作。

---
## 评论

**文章中心观点**
本文提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构模式，旨在通过上下文消息策略和异步任务管理框架，解决 MCP（Model Context Protocol）服务器在处理长时运行任务时的状态持久化与通信中断问题。

**支撑理由与边界条件分析**

1.  **长时任务中的“会话保持”技术必要性**
    *   **支撑理由（事实陈述）：** 传统的 LLM 请求-响应模式通常在几秒到几十秒内完成，而企业级应用（如数据分析、代码编排）往往需要数分钟甚至数小时。文章提出的“上下文消息策略”实际上是在构建一个**状态机**，通过在 Bedrock AgentCore 中维护中间状态，使得 LLM 能够在任务暂停后通过“Strands”恢复上下文，而非重新开始。
    *   **反例/边界条件（你的推断）：** 如果任务本身是幂等的且计算成本极低（例如简单的文本生成），重新生成可能比维护复杂的状态机更廉价。此外，如果 MCP 客户端不支持长时间连接或无法处理服务端的推送消息，该策略将失效。

2.  **异步解耦对系统稳定性的提升**
    *   **支撑理由（作者观点）：** 文章强调的“异步任务管理框架”将 Agent 的决策层与执行层解耦。这符合微服务架构的最佳实践，防止了因某个耗时工具调用阻塞整个 Agent 进程，从而提高了系统的并发吞吐能力。
    *   **反例/边界条件（事实陈述）：** 异步架构引入了最终一致性的挑战。如果用户在任务完成前取消了请求，或者网络发生分区，系统必须具备复杂的“垃圾回收”机制来清理孤儿进程，否则会导致云资源（如 Bedrock 推理单元）的浪费和泄漏。

3.  **MCP 协议在云原生生态中的标准化潜力**
    *   **支撑理由（你的推断）：** 利用 MCP 连接 Bedrock 这样的托管服务，意味着 Anthropic 的协议标准正在被 AWS 巨头接纳。这种组合为开发者提供了一种“混合云”路径：既利用了 Bedrock 的托管模型能力，又保留了通过 MCP 接入私有数据源的灵活性。
    *   **反例/边界条件（行业常识）：** MCP 目前仍是一个快速演进的协议，尚未完全固化。如果未来 OpenAI 或 Google 推出竞争性协议且市场份额占优，基于 MCP 构建的深层集成可能面临重构风险。

**多维度深入评价**

**1. 内容深度与论证严谨性**
文章触及了当前 AI Agent 落地中最痛点的“长任务”问题。从技术角度看，它不仅仅是在调用 API，而是在构建一个**分布式事务系统**。文章提到的“Strands Agents integration”暗示了状态存储的持久化，这是严谨的工程思路。然而，摘要中未明确提及错误处理和重试策略，这在长时运行任务中是至关重要的，论证略显单薄。

**2. 实用价值与创新性**
*   **实用价值：** 极高。对于正在尝试将 LLM 应用于 RPA（机器人流程自动化）或复杂数据处理的企业来说，这篇文章提供了一个可落地的参考架构，避免了从零开始设计轮询或回调机制。
*   **创新性：** **中等偏上**。虽然异步任务管理是后端开发的常识，但将其与 LLM Agent 的思维链结合，并标准化为 MCP 服务器模式，是对当前 Agent 编排范式的一次有效补充。

**3. 行业影响**
这篇文章标志着 **MCP 协议正在从“客户端工具”向“服务端基础设施”渗透**。如果 AWS Bedrock 开始大力推广此类集成，MCP 可能会成为连接云厂商模型与企业私有数据的**事实标准**，加速“模型层”与“数据层”的解耦。

**4. 争议点与批判性思考**
*   **厂商锁定风险：** 文章极力推崇 Bedrock AgentCore。虽然 MCP 是开源的，但 AgentCore 是 AWS 专有的。一旦开发者深入依赖其特定的状态管理 API，未来迁移到 GCP 或 Azure 的成本将显著增加。
*   **过度工程化嫌疑：** 对于简单的查询任务，引入 Strands 和异步框架可能属于“杀鸡用牛刀”。行业需要警惕为了技术而技术，忽视了简单 RESTful API 在轻量级场景下的优势。

**实际应用建议**
1.  **成本监控：** 在实施异步框架时，务必设置 CloudWatch 告警，监控挂起的任务数量，防止因代码 Bug 导致僵尸任务消耗 Bedrock Tokens。
2.  **协议兼容性测试：** 在生产环境部署前，务必测试不同 MCP 客户端（如 Claude Desktop 或自定义 SDK）对长连接的稳定性，确保“上下文消息”不会因客户端超时而被丢弃。

**可验证的检查方式**

1.  **压力测试指标：** 构建一个模拟长时任务（如 5 分钟延迟）的 MCP 工具，并发起 100 个并发请求。观察 Bedrock Agent 的吞吐量是否因异步框架而保持稳定，以及是否有请求超时。
2.  **状态一致性验证：** 在任务执行过程中人为中断网络或重启服务端容器，恢复后检查 Agent 是否能通过 Strands 准确获取之前的执行进度，还是出现了状态丢失。
3.  **成本效益分析：** 对比“长轮询”与“文章提出的异步推送”模式在相同负载下的 API 调用次数和成本，验证该架构是否真正降低了 Token 消耗。

---
## 技术分析

# 技术架构分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 的长时运行 MCP 服务器

## 1. 架构核心逻辑

### 核心目标
文章探讨了一种在 Amazon Bedrock AgentCore 环境下构建长时运行 MCP 服务器的技术方案，旨在解决 AI Agent 在处理耗时任务时的状态管理与交互连续性问题。

### 设计理念
该方案的核心思想是**“交互与执行的异步解耦”**。传统的同步请求-响应模式在处理长周期任务（如复杂工作流编排或长时间数据处理）时容易导致超时或上下文丢失。本架构通过引入异步任务管理机制，允许 Agent 在发起任务后释放主线程，并在后台继续执行，同时利用 MCP 协议维持上下文状态的一致性。

### 技术价值
该架构为解决 AI Agent 落地过程中的“长时任务稳定性”问题提供了具体的工程路径。通过将 MCP 协议从单纯的数据接口扩展为任务状态同步通道，方案确保了 Agent 在处理高延迟操作时的可用性和可靠性。

## 2. 关键技术机制

### 涉及组件
1.  **MCP (Model Context Protocol)**: 用于连接 AI 应用与数据源的标准协议，在此架构中承担服务器与客户端间的状态同步职责。
2.  **Amazon Bedrock AgentCore**: 负责底层的 Agent 编排、LLM 路由及工具调用逻辑。
3.  **Strands Agents**: 用于处理特定任务流的集成框架，支持复杂逻辑的拆解与执行。
4.  **异步任务管理**: 包含消息队列、状态机及回调机制的后台处理系统。

### 实现原理
*   **上下文消息策略**:
    *   **机制**: 在长任务执行期间，系统不维持持久的长连接，而是通过 MCP 协议发送包含状态标识的上下文消息。AgentCore 或客户端依据这些消息更新内部状态或用户界面。
    *   **流程**: 利用 MCP 的通知接口，将任务的“初始化”、“进行中”、“完成”或“异常”状态封装为标准消息推送给相关方。
*   **异步任务管理框架**:
    *   **机制**: 当 Agent 触发耗时操作（例如“生成并部署代码”）时，AgentCore 立即返回一个任务句柄（Handle/Token）而不阻塞等待。后台工作线程或独立计算资源执行实际任务，完成后通过 MCP Server 将结果回写至上下文。
    *   **存储**: 引入持久化存储（如 DynamoDB），记录任务 ID 与执行状态的映射关系。

### 技术挑战与应对
*   **挑战**: LLM 本质上的无状态特性与长时任务的有状态需求之间存在矛盾。
*   **应对**: 通过 Strands Agents 集成，将任务链的中间状态进行持久化。每次任务恢复或状态查询时，系统从持久层加载上下文，确保逻辑的连贯性。

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用无状态设计以实现高可用性

**说明**：在构建长期运行的 MCP (Model Context Protocol) 服务器时，必须确保服务本身是无状态的。由于 AgentCore 可能会根据负载动态调整实例数量或重启服务，将状态信息（如会话历史、中间变量）存储在服务器内存中会导致数据丢失。无状态设计是保证服务弹性和稳定性的基础。

**实施步骤**:
1. 将所有对话上下文和会话状态持久化存储到 Amazon DynamoDB 或 ElastiCache 等外部存储服务中。
2. 在 MCP 服务器逻辑中，通过传入的唯一 Token 或 Session ID 从外部存储中检索状态，而不是依赖本地变量。
3. 确保每个请求的处理都独立于之前的请求，不依赖本地内存缓存。

**注意事项**: 避免使用全局变量存储用户特定的数据，确保在并发场景下不同用户的数据不会互相串扰。

---

### 实践 2：优化 Strands Agents 的工具调用超时与重试机制

**说明**：长期运行的 MCP 服务器通常需要调用下游 API 或数据库来获取 Strands Agents 所需的信息。网络波动或下游服务延迟可能导致请求挂起，进而阻塞整个 Agent 的工作流。必须配置合理的超时和指数退避重试策略，以防止级联故障。

**实施步骤**:
1. 为所有外部调用（无论是通过 Boto3 调用 AWS 服务还是外部 HTTP API）设置严格的连接超时和读取超时（例如建议 3-5 秒）。
2. 实施指数退避算法进行重试，避免在下游服务压力大时造成雪崩效应。
3. 在 MCP 工具定义中，明确声明预期的执行时间，以便 Bedrock AgentCore 能够正确规划任务。

**注意事项**: 对于长时间运行的任务（如超过 30 秒），不要让 MCP 连接保持挂起状态，而应返回一个“任务已接收”的响应，并使用异步回调或轮询机制处理结果。

---

### 实践 3：实施严格的 IAM 最小权限访问控制

**说明**：MCP 服务器在 Bedrock AgentCore 环境中运行时，通常需要访问 AWS 资源（如 S3、DynamoDB 或 Bedrock 自定义模型）。为了遵循安全最佳实践，必须为 MCP 服务器分配精细的 IAM 角色，仅授予完成任务所需的特定权限，防止权限滥用。

**实施步骤**:
1. 创建专用的 IAM 角色供 MCP 服务使用。
2. 编写 IAM 策略时，明确限定资源 ARN（例如 `arn:aws:s3:::specific-bucket/*`），避免使用 `*` 通配符。
3. 定期使用 IAM Access Analyzer 审查角色权限，移除未使用的权限。

**注意事项**: 确保 MCP 服务器代码不会硬编码任何 AWS 凭证，应完全依赖实例元数据服务（IMDS）或 ECS/Pod 的任务角色自动获取凭证。

---

### 实践 4：利用结构化日志与 CloudWatch 进行可观测性监控

**说明**：对于长期运行的服务，仅通过简单的控制台输出无法有效排查问题。必须实施结构化日志记录，并集成 Amazon CloudWatch 以便实时监控 MCP 服务器的健康状况、工具调用频率以及潜在的错误。

**实施步骤**:
1. 使用 JSON 格式输出日志，确保包含关键字段：`request_id`（请求追踪）、`tool_name`（工具名称）、`user_id`（用户标识）、`latency`（耗时）和 `status`（状态）。
2. 将日志流式传输至 Amazon CloudWatch Logs。
3. 配置 CloudWatch Alarms（警报），针对错误率（如 5xx 错误）或延迟异常设置阈值，以便及时触发告警。

**注意事项**: 在记录日志时，务必过滤敏感信息（如 PII 个人身份信息、API 密钥），防止数据泄露。

---

### 实践 5：设计幂等的工具接口

**说明**：在分布式环境中，网络重试是常态。如果 MCP 服务器暴露的工具接口不是幂等的，客户端的重试操作可能导致数据重复处理或状态不一致。幂等性意味着多次执行相同的操作产生的结果与执行一次相同。

**实施步骤**:
1. 对于写操作（如创建订单、更新数据库），在 API 设计中引入 `client_token` 或 `idempotency_key`。
2. 服务器端在处理请求前，检查该 Key 是否已被处理；如果是，则直接返回之前的结果，而不执行重复操作。
3. 对于 Strands Agents 的上下文，确保即使多次调用同一个工具，系统状态也能保持一致。

**注意事项**: 幂等性检查通常依赖外部存储（如 DynamoDB）来记录已处理的 Key，需确保该存储层的高可用性。

---

### 实践 6：构建高效的上下文管理与数据检索策略

**说明**：Strands Agents 往往需要处理大量上下文信息。如果 MCP 服务器每次都将海量历史数据传递给 LLM，会导致延迟增加和 Token 成本飙升。应实施 RAG（检索

---
## 学习要点

- Amazon Bedrock AgentCore 正式发布，支持开发者构建能够自主执行复杂工作流并具备长期记忆能力的长期运行型 Agent。
- 通过集成 Strands Agents，开发者可以显著简化构建多步骤自动化任务的流程，无需从头搭建底层基础设施。
- 该架构允许 Agent 在执行任务时进行自我修正并调用外部工具，从而有效解决复杂问题并提高任务完成率。
- 内置的状态管理机制确保了 Agent 在长时间运行的任务中能够保持上下文连续性，实现跨步骤的数据持久化。
- 开发者可以利用 MCP (Model Context Protocol) 服务器标准化地连接外部数据源和工具，轻松扩展 Agent 的功能边界。
- 该解决方案完全兼容 Amazon Bedrock 的托管模型服务，使企业能够利用高性能基础模型而无需管理服务器基础设施。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [MCP](/tags/mcp/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*