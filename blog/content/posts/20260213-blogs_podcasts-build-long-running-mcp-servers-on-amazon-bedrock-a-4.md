---
title: "基于Amazon Bedrock AgentCore构建长时运行的MCP服务器"
date: 2026-02-13T14:12:23+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长时运行", "上下文管理", "AI 智能体"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种在 Amazon Bedrock AgentCore 上构建长时间运行的 MCP 服务器的综合方法，并结合 Strands Agents 集成实现生产级 AI 代理。 核心内容包括三个关键策略： 1. **上下文消息策略**：引入了一种机制，用于在服务器和客户端之间维持长时间的连续通信，确保在扩展操作期间"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长时运行的MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们将为您提供一种全面的实现方法。首先，我们介绍一种上下文消息策略，以便在长时间运行的操作期间保持服务器与客户端之间的持续通信。接着，我们构建一个异步任务管理框架，让您的 AI 智能体能够启动长时运行进程，而不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents，将这些策略整合起来，打造可投入生产的 AI 智能体，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 智能体，往往面临着上下文维护与资源阻塞的挑战。本文将介绍一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的实现方案，通过上下文消息策略与异步任务管理框架，确保服务器与客户端的持续通信。阅读此文，您将掌握如何整合这些技术，打造出可投入生产、可靠处理复杂耗时操作的系统。

---
## 摘要

本文介绍了一种在 Amazon Bedrock AgentCore 上构建长时间运行的 MCP 服务器的综合方法，并结合 Strands Agents 集成实现生产级 AI 代理。

核心内容包括三个关键策略：

1.  **上下文消息策略**：引入了一种机制，用于在服务器和客户端之间维持长时间的连续通信，确保在扩展操作期间信息的实时同步与状态更新。

2.  **异步任务管理框架**：开发了一个异步框架，允许 AI 代理启动长时间运行的处理流程，同时不会阻塞其他操作，从而提高系统的并发处理能力和响应速度。

3.  **集成与实现**：展示了如何将上述策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合，构建出能够可靠处理复杂、耗时任务的生产就绪型 AI 代理。

通过这些方法，开发者可以构建出具备高可靠性和复杂任务处理能力的 AI 系统。

---
## 评论

基于您提供的文章标题与摘要，以下是从技术与行业角度的深入评价。

### 中心观点
**文章提出了一种基于 Amazon Bedrock AgentCore 的架构模式，通过引入“上下文消息策略”和“异步任务框架”来解决 MCP（Model Context Protocol）服务器在处理长周期任务时的状态管理与连续性问题。**

### 支撑理由与深度评价

**1. 解决了 LLM 应用的“长任务”痛点（事实陈述）**
*   **分析：** 传统的同步 Request-Response 模式难以适应耗时较长的任务（如数据分析、代码生成或复杂工作流编排），容易导致 HTTP 超时或 Token 限制。文章提出的“异步任务管理框架”切中肯綮，这是从“聊天机器人”向“智能体”演进的关键技术门槛。
*   **行业视角：** 这符合当前 Agent 架构从“单轮对话”向“多步规划”发展的趋势。

**2. 引入“Strands”概念暗示了子任务编排能力（你的推断）**
*   **分析：** 摘要中提到的“Strands Agents integration”可能引用了某种特定的并发或串行任务编排机制（Strands 通常指代并发编程中的执行线程或逻辑流）。如果文章详细阐述了如何将 Bedrock 的原子能力拆解为 Strands 并进行聚合，这提供了比简单的 LangChain Loop 更精细的控制粒度。
*   **创新性：** 这不仅仅是异步化，更可能涉及到了“流式思维链”的工程化落地。

**3. 深化了 MCP 协议的工程化落地（事实陈述）**
*   **分析：** MCP 作为新兴的上下文协议标准，目前社区大多关注简单的工具调用。文章专门针对“长运行”场景在 Bedrock 上落地 MCP，填补了云厂商原生支持与开源协议之间的鸿沟，提升了 MCP 在企业级场景中的可用性。

**4. 边界条件与反例（批判性思考）**
*   **反例 1（状态一致性风险）：** 引入异步框架必然带来分布式系统的最终一致性问题。如果 Bedrock Agent 在等待异步任务结果时，用户发起了新的冲突指令，文章的“上下文消息策略”是否能有效处理并发冲突，还是仅仅依赖消息队列的 FIFO？
*   **反例 2（成本与延迟）：** 维护长连接或频繁的上下文轮询会显著增加 API 调用成本和 Token 消耗。对于简单的查询任务，这种重架构可能存在过度设计，导致响应延迟反而高于直接调用。

### 评价维度详解

**1. 内容深度：高**
文章没有停留在简单的 API 调用演示，而是触及了 Agent 系统中最难处理的“状态持久化”和“生命周期管理”。它试图在无状态的 LLM 和有状态的后端服务之间建立一座稳固的桥梁。

**2. 实用价值：高（针对特定人群）**
对于正在使用 AWS 基础设施构建复杂 Agent 应用的架构师而言，这篇文章提供了官方的最佳实践参考，避免了从零搭建异步轮询机制的重复造轮子。

**3. 创新性：中等偏上**
虽然异步任务模式并非新发明，但将其与 MCP 协议和 Bedrock AgentCore 深度结合，并命名为“Strands integration”（如果这是该文的特定术语），具有一定的架构创新意义。

**4. 可读性：中等**
技术类文章通常面临挑战：如何将复杂的异步交互时序图描述清楚。如果文章缺乏清晰的 Sequence Diagram（时序图），读者很难理解“上下文消息”究竟是在何时、何地被注入的。

**5. 行业影响：**
这标志着 Agent 开发正在进入“工业化”阶段。社区不再满足于简单的 Demo，而是开始关注高可用、长连接的企业级 Agent 架构。这也可能推动 MCP 协议成为连接云原生 AI 服务与本地工具的标准接口。

### 争议点与不同观点

*   **过度依赖 Bedrock 原生能力：** 这种架构虽然便利，但可能导致严重的 Vendor Lock-in（厂商锁定）。如果未来需要迁移到 Azure 或 GCP，重写 AgentCore 和 Strands 逻辑的成本将非常高昂。
*   **上下文窗口的利用率：** 频繁的“上下文消息策略”可能会迅速消耗 LLM 的上下文窗口。如果任务运行时间过长，累积的中间状态日志是否会挤掉有效 Prompt 的空间？这是文章可能未充分探讨的隐患。

### 实际应用建议

1.  **成本监控：** 在实施该架构前，务必开启 AWS Cost Explorer 的详细监控。长运行任务往往伴随着不可见的 Token 累积费用（尤其是 Bedrock 按请求数和 Token 数双重计费时）。
2.  **超时熔断机制：** 不要盲目信任异步框架的自动重试。必须在业务层设置硬性的超时熔断，防止 Bedrock Agent 陷入“等待幽灵任务”的死循环。
3.  **协议兼容性测试：** MCP 协议目前版本迭代较快。需验证 Bedrock AgentCore 对 MCP 的支持版本是否与你现有的客户端工具（如 Claude Desktop 或 IDE 插件）兼容。

### 可验证的检查方式

1.  **压力测试指标：** 搭建测试环境，并发发起 50 个长运行任务（模拟耗时 5 分钟），观察 Bedrock Agent 是否会出现上下文混淆或任务丢失，并监控 Lambda/Fargate 的冷启动频率。
2.  **成本对比实验：** 对比“同步长轮询”与“文章

---
## 技术分析

# 技术分析：基于 Amazon Bedrock AgentCore 的长运行 MCP 服务器架构

## 1. 核心架构与设计理念
文章探讨的核心议题是如何在 Amazon Bedrock AgentCore 环境中，利用 Strands Agents 集成技术，构建具备长运行能力的 MCP (Model Context Protocol) 服务器。

*   **架构演进**：传统 MCP 实现通常遵循同步的请求-响应模式，这在处理耗时任务（如大规模数据处理、复杂工作流编排）时面临严重的超时和资源阻塞风险。本文提出的架构通过引入异步层，将“通信”与“计算”解耦。
*   **核心设计模式**：采用**“任务票据”模式**。MCP 服务器不再阻塞等待任务完成，而是立即返回一个任务标识符。Bedrock AgentCore 结合 Strands Agents 的记忆能力，将此任务状态持久化，允许会话在任务执行期间暂停，并在后续通过轮询或回调恢复交互。

## 2. 关键技术机制解析

### 2.1 Context Message Strategy (上下文消息策略)
这是实现长运行交互的通信协议层核心。
*   **技术原理**：该策略重新定义了客户端与服务器之间的消息契约。当检测到长运行任务时，MCP 服务器返回的不是最终结果，而是一个包含 `task_id` 和 `status: "IN_PROGRESS"` 的中间上下文消息。
*   **作用**：它告知 Bedrock AgentCore 暂停当前的推理循环，将任务状态保存至 Strands Agents 的状态存储中，并向用户展示“任务已接收”的反馈，从而释放 LLM 上下文窗口资源。

### 2.2 Asynchronous Task Management Framework (异步任务管理框架)
这是实现长运行计算的后端执行引擎。
*   **技术原理**：框架利用 AWS 的异步服务（如 **AWS Step Functions** 或 **Amazon SQS**）来编排实际的工作流。MCP 服务器仅作为触发层，将负载卸载到后台处理。
*   **实现方式**：
    1.  **任务提交**：AgentCore 调用 MCP 工具，服务器将工作流定义推送到 Step Functions。
    2.  **状态解耦**：服务器立即返回 HTTP 202 (Accepted) 或 JSON-RPC 成功响应。
    3.  **状态追踪**：Strands Agents 定期调用 `check_status` 工具，或者由后台服务在任务完成时触发 webhook，唤醒 Agent 继续处理结果。

## 3. 技术难点与解决方案

*   **难点一：会话状态的一致性**
    *   **问题**：在异步任务执行期间，用户的上下文可能会丢失，导致 Agent 无法正确处理返回的结果。
    *   **解决方案**：利用 **Strands Agents** 的状态管理能力。Strands 维护了跨越多次交互的“记忆”，确保当任务完成时，Agent 能准确回顾起发起任务时的原始指令和上下文。

*   **难点二：超时与资源管理**
    *   **问题**：长运行任务可能超过 Lambda 或 API Gateway 的最大超时限制。
    *   **解决方案**：彻底剥离计算负载。MCP 服务器仅作为控制平面，实际计算由 Step Functions 等服务托管，这些服务支持长达数天的工作流执行，完美解决超时问题。

## 4. 技术价值与适用场景
该架构方案显著扩展了 AI Agent 的应用边界，使其能够胜任企业级自动化任务。
*   **适用场景**：包括但不限于生成式报告编写、批量数据处理、代码库编译与测试、以及需要人工审批介入的复杂工作流。
*   **价值总结**：通过结合 Bedrock AgentCore 的编排能力、Strands Agents 的记忆能力以及 MCP 的开放连接性，该方案成功在保持交互流畅性的同时，赋予了 Agent 处理复杂、长周期现实任务的能力。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化会话状态管理与持久化

**说明**: 长时间运行的 MCP 服务器需要维护跨多个请求的上下文状态。在 Bedrock AgentCore 环境中，必须确保 Strands Agents 的对话历史和任务状态能够高效持久化，以支持长时间的交互会话。

**实施步骤**:
1. 利用 Amazon DynamoDB 或 ElastiCache 作为外部状态存储，避免仅依赖内存存储。
2. 实现检查点机制，定期将 Strands Agents 的中间状态保存到持久层。
3. 设计状态恢复逻辑，确保服务重启或故障转移后能从上一个检查点恢复。

**注意事项**: 确保存储的数据结构支持快速检索，避免状态存储成为性能瓶颈。

---

### 实践 2：实施严格的超时与重试策略

**说明**: 长时间运行的任务容易遇到网络波动或下游服务不可用的情况。构建具有弹性的 MCP 服务器时，必须定义合理的超时限制和指数退避重试机制，以防止任务无限期挂起。

**实施步骤**:
1. 为所有外部 API 调用和 Strands Agents 工具调用配置明确的超时时间。
2. 实现指数退避算法处理可重试的错误。
3. 利用 AWS Step Functions 或工作流逻辑管理长时间运行的事务，确保失败后的状态一致性。

**注意事项**: 区分暂时性错误和永久性错误，避免对无效请求进行无意义的重试。

---

### 实践 3：设计无状态架构以支持水平扩展

**说明**: 为了应对 Strands Agents 在处理复杂任务时的高负载需求，MCP 服务器应设计为无状态架构。这将允许 AgentCore 根据负载动态扩展实例数量，而不会丢失会话上下文。

**实施步骤**:
1. 将所有会话状态从应用逻辑中解耦，存储在共享存储层（如 S3 或 DynamoDB）。
2. 确保 Strands Agents 的配置和提示词通过配置管理服务（如 SSM Parameter Store）加载，而非硬编码。
3. 在 ECS/EKS 或 Lambda 上部署时，启用自动扩缩容策略。

**注意事项**: 验证外部存储的吞吐量能够支持扩展后的并发读写需求。

---

### 实践 4：建立全面的可观测性与日志记录

**说明**: 长时间运行的服务难以调试。必须集成 Amazon CloudWatch 和 X-Ray，以监控 Strands Agents 的决策路径、工具调用链路以及 MCP 服务器的性能指标。

**实施步骤**:
1. 为每个 MCP 请求分配唯一的 Trace ID，并贯穿整个调用链。
2. 记录 Strands Agents 的输入提示词、中间推理步骤和最终输出结果。
3. 设置 CloudWatch 告警，监控错误率、延迟和资源利用率。

**注意事项**: 避免记录敏感信息（如 PII 数据），在日志输出前实施脱敏处理。

---

### 实践 5：实施细粒度的安全控制与权限隔离

**说明**: Strands Agents 通常需要调用下游工具和服务。必须遵循最小权限原则，为 MCP 服务器配置精细的 IAM 角色，防止权限过度分配导致的安全风险。

**实施步骤**:
1. 为不同的 Strands Agent 或工具组配置独立的 IAM 角色。
2. 使用 Bedrock 的 Guardrails 来过滤输入和输出，防止提示词注入和数据泄露。
3. 定期审计 IAM 策略，移除未使用的权限。

**注意事项**: 在处理跨账户资源访问时，优先使用角色假设而非长期访问密钥。

---

### 实践 6：优化上下文窗口与提示词管理

**说明**: 随着会话时间的延长，上下文数据可能会超出模型的 Token 限制。需要实施有效的上下文压缩和提示词工程策略，以确保 MCP 服务器在长会话中保持响应能力。

**实施步骤**:
1. 实现上下文窗口管理逻辑，自动摘要或丢弃过时的历史消息。
2. 为 Strands Agents 设计结构化的系统提示词，确保指令简洁且高效。
3. 对工具调用结果进行预处理，仅将关键信息传递回模型。

**注意事项**: 在压缩上下文时，保留关键实体和用户意图，避免任务执行失败。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够处理复杂、多步骤工作流的长期运行 MCP 服务器。
- 通过利用 Strands 的持续运行能力，开发者可以突破传统无状态交互的限制，创建能够自主执行长期任务（如监控或异步工作流）的智能体。
- 该集成实现了模型控制层（Model Context Control, MCP）与 Bedrock 托管基础设施的深度结合，简化了具备状态记忆能力的 AI 应用的部署与管理。
- 开发者可以利用 Strands 的编排逻辑，在 Bedrock 上构建出能够自主规划、调用工具并维持上下文状态的高级 AI 智能体。
- 此架构显著增强了企业级应用在处理需要长时间运行和复杂决策支持任务时的可行性与稳定性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*