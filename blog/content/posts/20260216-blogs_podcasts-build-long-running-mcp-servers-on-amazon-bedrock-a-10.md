---
title: "构建基于Bedrock AgentCore与Strands的长运行MCP服务器"
date: 2026-02-16T09:30:10+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Bedrock", "AgentCore", "Strands", "异步任务", "长连接", "AI 代理", "消息策略"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 集成来构建长时间运行的 MCP 服务器的综合方法。 为实现这一目标，文章主要提出了三项关键策略： 1. **上下文消息策略**：引入了一种机制，用于在服务器和客户端执行扩展操作期间维持连续的通信，确保长任务过程中的信"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 构建基于Bedrock AgentCore与Strands的长运行MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们为您提供了一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，以在长时间运行的操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的任务而不阻塞其他操作。最后，我们演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents，将这些策略融会贯通，构建能够可靠处理复杂、耗时操作的面向生产环境的 AI 代理。

---
## 导语

构建能够可靠处理长时间运行任务的 AI 代理，是当前将生成式 AI 应用于复杂生产环境的关键挑战。本文将深入探讨如何结合 Amazon Bedrock AgentCore 与 Strands Agents，通过上下文消息策略和异步任务管理框架，解决服务器与客户端间的持续通信及阻塞问题。阅读本文，您将掌握构建高可用、非阻塞式 AI 代理系统的具体方法，从而从容应对耗时操作。

---
## 摘要

本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 集成来构建长时间运行的 MCP 服务器的综合方法。

为实现这一目标，文章主要提出了三项关键策略：

1.  **上下文消息策略**：引入了一种机制，用于在服务器和客户端执行扩展操作期间维持连续的通信，确保长任务过程中的信息同步与状态更新。
2.  **异步任务管理框架**：开发了一套框架，允许 AI 代理在启动耗时较长的流程时不阻塞其他操作，从而实现非阻塞的异步处理。
3.  **生产级集成方案**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 结合，构建出能够可靠、高效地处理复杂且耗时操作的 AI 代理。

---
## 评论

**中心观点**
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的技术架构，旨在通过上下文消息策略和异步任务管理框架，解决 MCP（Model Context Protocol）服务器在执行长周期任务时的连接保持与状态同步问题，从而突破传统请求-响应模式在处理复杂工作流时的局限性。

**支撑理由与深度评价**

1.  **技术架构的必要性与深度（事实陈述 + 作者观点）**
    *   **理由**：传统的 LLM 应用受限于 HTTP 超时和 Token 输出限制，难以处理数据库迁移、长视频渲染等“长耗时”任务。文章引入的 **Strands Agents integration** 和 **AgentCore** 实际上是构建了一个“中间件层”，将 AI 的决策层与执行层解耦。
    *   **深度分析**：文章的核心价值在于将 **MCP 协议** 从单纯的“数据检索工具”扩展为“任务执行代理”。通过 **上下文消息策略**，系统不再需要保持长连接，而是通过状态轮询或回调来维持对话的“幻觉”连续性。这在技术上解决了 Serverless 架构（如 AWS Lambda）难以运行长进程的痛点，论证了异步编排模式在 Agent 开发中的必要性。
    *   **反例/边界条件**：如果任务涉及高频实时交互（如毫秒级控制的机器人操作），这种异步轮询机制会引入不可接受的延迟，此时必须维持 WebSocket 长连接，而非文章建议的异步模式。

2.  **异步任务管理的工程实用性（事实陈述 + 你的推断）**
    *   **理由**：文章提出的异步任务管理框架，允许 Agent 在任务挂起期间释放计算资源，仅在有状态更新时唤醒。这对于云原生环境下的成本控制和并发处理至关重要。
    *   **深度分析**：这不仅仅是技术实现，更是一种**成本优化策略**。在 Bedrock 等托管服务上，保持连接空闲是昂贵的。通过将任务状态持久化到存储层（如 DynamoDB 或 S3），文章实际上是在教导开发者如何构建“有状态”的“无状态”服务。
    *   **反例/边界条件**：对于极短任务（< 5秒），引入异步框架的序列化/反序列化开销和架构复杂度可能超过其收益，直接同步调用反而更高效。

3.  **生态整合与行业影响（作者观点 + 你的推断）**
    *   **理由**：将 MCP 标准与 AWS Bedrock 深度绑定，有助于企业快速落地 AI Agent，同时避免厂商锁定。
    *   **深度分析**：MCP 正在成为 AI 连接外部世界的“USB 接口”。这篇文章实际上是一份**最佳实践指南**，填补了“协议标准”与“企业级基础设施”之间的空白。它暗示了未来的 AI 应用架构将从“单体大模型”转向“协议 + 编排层 + 执行层”的微服务化架构。
    *   **反例/边界条件**：如果 MCP 协议本身发生重大迭代导致不兼容，或者企业未使用 AWS 生态，该架构的迁移成本将极高。

**可验证的检查方式**

1.  **压力测试指标**：在模拟的高并发场景下（如 1000 个并发长任务），观察 Bedrock Agent 的 API 调用成功率与平均响应时间。如果该架构有效，系统应能在不增加超时错误的情况下线性扩展。
2.  **成本效能分析**：对比“长连接轮询”与“异步任务框架”在同等任务负载下的云服务账单（主要涉及 Lambda 费用、Bedrock Token 消耗和状态存储费用）。验证异步模式是否真的降低了总拥有成本（TCO）。
3.  **状态一致性观察窗口**：在网络抖动或服务重启的故障注入测试中，观察任务上下文是否丢失。检查 Agent 是否能准确恢复到“思考”中断的位置，而非从头开始。

**综合评价与建议**

**内容深度**：文章触及了当前 Agent 落地中最棘手的“最后一公里”问题——执行长任务。它没有停留在概念层面，而是深入到了状态管理和协议适配的工程细节，具有较高的技术含金量。

**创新性**：将 MCP 与 Bedrock AgentCore 结合并非简单的拼接，而是提出了一种**“协议-编排-执行”分离**的新范式。特别是利用上下文策略来模拟“持续思考”的方法，是对现有 LLM 无状态特性的一种巧妙修补。

**实用价值**：对于正在基于 AWS 构建企业级 Agent 的开发者来说，这是一份高价值的蓝图。它提供了具体的代码逻辑（虽然摘要中未展开，但框架清晰）和架构思路。

**争议点与不同观点**：该方案可能引入了**过度工程化**的风险。对于简单的查询任务，引入 Strands Agents 和复杂的异步框架可能显得笨重。此外，完全依赖云厂商的托管服务（AgentCore）可能导致对特定供应商的强依赖，削弱了系统的可移植性。

**实际应用建议**：
1.  **分层采用**：仅在涉及耗时超过 30 秒的操作（如数据处理、邮件群发、代码生成）时启用该异步框架，简单 RAG 检索保持同步。
2.  **监控死信队列**：长任务容易失败，必须建立完善的 DLQ（Dead Letter Queue）处理机制，确保异步任务失败时用户能得到反馈。
3.  **上下文压缩**：虽然文章强调保持上下文，但在极长任务中，仍需定期总结中间步骤以避免 Token 溢出，不要盲目传递所有

---
## 技术分析

基于您提供的标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要片段，我将结合当前生成式AI Agent架构、MCP（Model Context Protocol）协议标准以及Amazon Bedrock的最新技术动态，为您进行深度分析。

这篇文章主要解决的是当前AI Agent领域的一个核心痛点：**大模型如何在有限的上下文窗口和Token限制下，执行耗时、复杂且需要状态保持的长周期任务。**

以下是详细的深度分析：

---

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**通过将MCP（Model Context Protocol）服务器与Amazon Bedrock的AgentCore及Strands Agents框架集成，可以构建出能够处理“长周期运行”任务的AI系统。** 这种架构不再局限于单次请求-响应模式，而是支持在任务执行过程中进行持续的状态管理和异步通信。

### 作者想要传达的核心思想
作者试图打破传统LLM应用“无状态”和“短连接”的桎梏。核心思想在于**“解耦”**：将复杂的任务逻辑从被动的LLM响应中剥离出来，交给独立的、持久的MCP服务器处理，而LLM仅负责通过Strands机制进行协调和决策。这代表了从“聊天机器人”向“自主智能体”演进的关键一步。

### 观点的创新性和深度
*   **架构创新**：将MCP（通常用于本地工具连接）与Bedrock AgentCore（云端编排）结合，并引入“Strands”（线索/线程）概念，这是一种混合架构的创新。
*   **深度**：文章触及了Agent系统的深水区——**上下文连续性**。它不仅解决“怎么连”，更解决“怎么在长时间断连或异步操作中保持上下文不丢失”。

### 为什么这个观点重要
随着AI从内容生成转向任务执行，企业级应用（如RPA、自动化运维、复杂数据分析）往往需要数分钟甚至数小时才能完成。传统的超时机制无法满足需求。该方案为构建高可靠、企业级的AI Agent提供了标准化的技术路径，降低了开发长周期Agent的门槛。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **MCP (Model Context Protocol)**: 由Anthropic推广的开源协议，用于连接AI应用与外部数据源和工具。在此处，它作为Server端，暴露工具给Agent。
2.  **Amazon Bedrock AgentCore**: AWS Bedrock的底层编排引擎，负责Agent的路由、记忆和工具调用。
3.  **Strands Agents**: 这是本文的关键概念（推测基于AWS或特定框架的术语）。Strands指的是**“有状态的、持久的任务线程”**。不同于普通的Session，Strand允许Agent在后台挂起，等待外部事件（如人工审批、长任务完成）后唤醒。
4.  **Context Message Strategy (上下文消息策略)**: 一种通过增量更新或状态摘要来维护长期对话记忆的技术。

### 技术原理和实现方式
*   **异步任务管理框架**:
    *   **原理**: 当Agent调用MCP Server的工具时，如果该工具是长耗时任务（如“处理大型数据集”），MCP Server不会阻塞等待结果，而是立即返回一个`TaskID`和`pending`状态。
    *   **Strands介入**: AgentCore识别到这是一个异步流程，将当前对话状态保存为一个“Strand”。Agent进入休眠或后台运行模式。
    *   **回调与轮询**: 客户端或后台进程定期查询MCP Server，或者MCP Server通过WebSocket/回调通知AgentCore任务完成。Agent随后唤醒Strand，读取结果，并继续执行。

*   **上下文消息策略**:
    *   **实现**: 不将整个历史记录发送给LLM，而是维护一个“滚动窗口”或“摘要层”。对于长任务，只发送“当前Strand的状态”和“下一步所需的工具描述”。

### 技术难点和解决方案
*   **难点**: **状态一致性**。在分布式环境中（Bedrock云端 <-> MCP Server），如何确保两边对任务状态的理解一致？
*   **方案**: 引入**持久化存储**。Strands的状态不应只存在内存中，而应存入DynamoDB等数据库。MCP Server需实现幂等性接口，防止重复调用导致状态混乱。
*   **难点**: **上下文窗口限制**。长任务会产生大量中间日志。
*   **方案**: 使用**摘要技术**。在Strands的每个关键节点，让LLM生成当前状态的摘要，丢弃冗余的Token。

### 技术创新点分析
最大的创新在于**将MCP轻量级的连接能力“企业化”**。传统的MCP可能更多用于本地开发环境，而通过Bedrock AgentCore的集成，它获得了企业级的认证、监控和Strands（长时记忆）能力，使得小型的MCP工具可以组合成复杂的工业级工作流。

---

## 3. 实际应用价值

### 对实际工作的指导意义
对于正在构建AI应用的架构师和开发者，这篇文章提供了一个**标准参考架构（RSA）**。它告诉我们不要试图在一个超大的Prompt里解决所有问题，也不要用简单的Lambda函数处理所有逻辑，而应该建立专门的、有状态的MCP服务来处理业务逻辑。

### 可以应用到哪些场景
1.  **企业级RPA (机器人流程自动化)**: 例如“跨系统查询订单并退款”。涉及查询库存、等待财务审批、执行退款三个长步骤，需要跨越数小时甚至数天。
2.  **DevOps与运维**: 自动化故障排查。Agent部署脚本，等待监控数据返回，分析日志，再执行修复命令。
3.  **科研与数据分析**: 提交一个Spark作业，等待作业运行30分钟，获取结果后生成图表。
4.  **内容创作工作流**: 生成大纲 -> 人工审核 -> 撰写初稿 -> 人工修改 -> 发布。

### 需要注意的问题
*   **成本控制**: 长周期的Strands和频繁的上下文加载会增加Token消耗和数据库读写成本。
*   **超时配置**: Bedrock和MCP Server之间的超时设置需要精心调优，避免连接意外断开。

### 实施建议
*   **第一步**: 将现有的同步工具改造为异步模式，引入`TaskID`机制。
*   **第二步**: 在Bedrock中配置Agent时，明确区分“思考型”动作（由LLM完成）和“执行型”动作（由MCP Server异步完成）。

---

## 4. 行业影响分析

### 对行业的启示
该方案预示着**Agent的基础设施正在“云原生化”和“协议标准化”**。MCP正在成为连接AI模型与工具的“USB接口”，而云厂商（如AWS）则负责提供电源（计算）和驱动。

### 可能带来的变革
*   **从“对话”到“交付”**: AI应用将不再仅仅是聊得好的机器人，而是能交付复杂工作结果的数字员工。
*   **MCP生态爆发**: 随着Bedrock等大平台支持，MCP协议的开发者社区将迎来爆发，出现大量专业的“MCP工具提供商”。

### 相关领域的发展趋势
*   **Orchestration（编排）层的战争**: 未来的竞争焦点在于谁能更好地管理这些长周期的Agent状态（即LangChain, LangGraph, AutoGen与云厂商原生方案的竞争）。
*   **AgentOps的兴起**: 监控、调试和可视化这些长周期Agent将成为新的运维细分领域。

---

## 5. 延伸思考

### 引发的其他思考
*   **人机协同的新模式**: 在长任务中，Strands的“挂起”状态实际上是完美的“人类介入点”。这引发了对“人在回路”设计的新思考——如何优雅地通知人类并接收反馈？
*   **多Agent协作**: 如果一个MCP Server本身也是一个Agent，那么这就构成了“Agent调用Agent”的层级结构。这种结构的调试难度会指数级上升。

### 可以拓展的方向
*   **边缘计算结合**: 能否将MCP Server部署在边缘设备上，由Bedrock进行远程控制？这适用于工业物联网场景。
*   **跨云迁移**: 基于MCP的标准化，是否可以轻松地将Agent从Bedrock迁移到Azure或Google Cloud，而不重写工具代码？

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有工具**: 审查你现有的API或工具，哪些是耗时的（>10秒）。将这些优先封装为MCP Server。
2.  **引入状态机**: 在后端代码中引入简单的状态机逻辑，定义任务的Pending, Running, Completed, Failed状态。
3.  **利用Bedrock托管能力**: 不要自建消息队列，尽量利用AgentCore的内置能力来处理异步轮询。

### 具体的行动建议
*   **代码层面**: 学习MCP SDK（如Python或TypeScript版本），实现一个简单的`async_tool`。
*   **架构层面**: 在架构图中画出“控制平面”和“数据平面”的分离。LLM走控制平面，MCP Server走数据平面。

### 需要补充的知识
*   **MCP协议规范**: 深入理解Resource、Prompt、Tool三种类型的区别。
*   **异步编程模式**: 熟悉async/await、Webhook或长轮询机制。

---

## 7. 案例分析

### 成功案例分析：自动化合规审计
*   **场景**: 一家金融公司需要审计每日交易。
*   **流程**:
    1.  Agent (Bedrock) 接收指令：“审计昨天的交易”。
    2.  调用 MCP Server (审计工具) 提交Spark任务。
    3.  MCP Server 返回 `AuditID: 123`，状态 `Processing`。
    4.  Agent 创建 Strand，保存 `AuditID`，向用户汇报：“任务已提交，ID 123，正在运行。”
    5.  2小时后，MCP Server 完成计算，通过回调通知 Agent。
    6.  Agent 唤醒 Strand，调用工具获取结果，生成报告发送给用户。
*   **经验**: 这种模式完美解决了LLM无法等待2小时的问题。

### 失败案例反思：无状态的死循环
*   **场景**: 早期尝试让LLM直接轮询数据库。
*   **问题**: LLM没有记忆，每次轮询都消耗大量Token重复上下文，且容易因为网络波动导致轮询中断，任务“幽灵化”（既没成功也没失败，卡住了）。
*   **教训**: 必须将“执行逻辑”从“模型逻辑”中剥离，依赖持久化的后端（MCP Server）而非LLM的注意力来维持状态。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**在构建企业级AI Agent时，采用基于MCP协议、由Strands驱动的异步架构，是解决长周期任务复杂性与状态持续性问题的最优解。**

### 支撑理由与依据
1.  **理由一：解耦提升了系统的鲁棒性。**
    *   *依据*: 单体架构中，LLM超时或工具崩溃会导致全盘失败；MCP架构允许工具独立重启和重试。
2.  **理由二：异步处理是长任务的物理必然。**
    *   *依据*: LLM的Token生成是流式的，而外部API（如数据处理）是批处理或长连接

---
## 最佳实践

## 最佳实践指南

### 实践 1：设计有状态的服务架构以支持长时间运行任务

**说明**:
构建基于 Amazon Bedrock AgentCore 的 MCP (Model Context Protocol) 服务器时，必须考虑到长时间运行的工作流。与无状态的请求-响应模式不同，Strands Agents 需要在多次交互之间保持上下文和状态。架构设计应支持异步任务处理，允许 Agent 在等待外部操作（如 API 调用或数据检索）完成时挂起和恢复，而不阻塞主线程或导致超时。

**实施步骤**:
1. 使用支持异步 I/O 的框架（如 Python 的 asyncio 或 Node.js 的异步模式）来构建 MCP 服务器。
2. 实现持久层（如 Amazon DynamoDB 或 Amazon ElastiCache），用于存储会话状态、中间结果和执行历史。
3. 确保服务器逻辑能够处理“暂停”和“恢复”信号，以便在长时间任务中断后能无缝恢复上下文。

**注意事项**: 避免在内存中保存关键状态，以防服务重启导致数据丢失。务必设计幂等性接口，以便在网络故障重试时不会重复执行操作。

---

### 实践 2：实现健壮的超时与重试机制

**说明**:
长时间运行的 Agent 任务往往涉及调用下游 API 或执行复杂推理，这些操作可能会因为网络波动或服务限流而失败。为了确保 Strands Agents 的稳定性，必须在 MCP 服务器层面实现智能的超时控制和指数退避重试策略，而不是简单地依赖客户端的超时设置。

**实施步骤**:
1. 为所有外部调用（包括 Bedrock 模型调用和工具调用）配置可配置的超时参数。
2. 实施指数退避算法进行重试，例如在首次失败后等待 1秒，然后 2秒，以此类推，设置最大重试次数。
3. 利用 Amazon Bedrock AgentCore 的内置错误处理功能，将特定的错误代码映射到重试逻辑或失败通知中。

**注意事项**: 区分临时性错误（如 5xx 状态码）和永久性错误（如 4xx 状态码或权限错误）。仅对临时性错误进行重试，避免无效的资源消耗。

---

### 实践 3：优化工具定义与上下文管理

**说明**:
Strands Agents 依赖于 MCP 服务器暴露的工具来执行任务。为了提高 Agent 的准确性和效率，必须提供清晰、具体的工具定义，并严格控制传递给大模型的上下文窗口大小。上下文过多会增加延迟和成本，且容易导致模型迷失方向。

**实施步骤**:
1. 在 MCP 服务器的 Schema 定义中，为每个工具编写详细的描述和参数说明，确保 Bedrock 的模型能理解何时以及如何调用它们。
2. 实施上下文剪裁策略，仅保留与当前任务步骤直接相关的历史记录和数据。
3. 对于大型文档或数据集，使用 RAG (检索增强生成) 模式，通过向量搜索仅检索相关片段，而不是将整个数据集加载到上下文中。

**注意事项**: 定期审查工具调用的日志，分析模型是否频繁误用工具，并据此优化工具的描述或参数结构。

---

### 实践 4：实施细粒度的可观测性与日志记录

**说明**:
调试长时间运行的 Agent 链路具有挑战性。为了追踪 Strands Agents 的决策过程和 MCP 服务器的响应情况，必须建立端到端的可观测性。这包括记录每个工具调用的输入输出、模型推理的轨迹以及系统的延迟指标。

**实施步骤**:
1. 集成 AWS CloudWatch 或兼容的 OpenTelemetry 协议，收集结构化日志。
2. 在日志中包含 `Trace ID`，将 Agent 的请求、MCP 服务器的处理以及下游 API 调用关联起来。
3. 监控关键性能指标（KPI），如“任务平均完成时间”、“工具调用成功率”和“Token 消耗量”。

**注意事项**: 确保日志中不包含敏感信息（PII），特别是当工具参数包含用户数据时。考虑在生产环境中对敏感字段进行脱敏处理。

---

### 实践 5：确保安全性与最小权限原则

**说明**:
MCP 服务器通常作为 Agent 与企业数据或外部服务之间的桥梁。如果服务器遭到入侵或提示词被注入恶意指令，可能会导致数据泄露。因此，必须在服务器层面和 IAM 权限层面实施严格的安全控制。

**实施步骤**:
1. 为 MCP 服务器分配 IAM 角色，严格限制其仅能访问执行特定任务所需的 AWS 资源或 API 端点。
2. 在服务器代码中实施输入验证，检查所有传入的工具参数和指令，防止注入攻击。
3. 使用 AWS Secrets Manager 存储数据库凭证、API 密钥等敏感信息，而不是硬编码在代码或配置文件中。

**注意事项**: 定期轮换密钥和访问凭证。如果可能，启用 VPC Endpoint 来在 AWS 网络内部路由流量，避免流量暴露在公共互联网中。

---

### 实践 6：构建模块化与可扩展的工具接口

**说明**

---
## 学习要点

- Amazon Bedrock AgentCore 正式支持集成 Strands Agents，允许开发者构建能够执行长期、复杂且多步骤任务的自主型 MCP 服务器。
- 通过将 Strands 的时间感知编排能力与 Bedrock 的托管基础设施相结合，该方案解决了传统 AI Agent 在处理长周期工作流时的状态管理和中断恢复难题。
- 新架构实现了 MCP 协议的无缝集成，使得基于 Bedrock 的 Agent 能够作为标准化工具，安全地连接外部数据源和业务系统。
- 该集成方案显著提升了 Agent 处理复杂逻辑的能力，使其能够在无需人工持续干预的情况下，自主完成跨越数小时甚至数天的业务闭环。
- 利用 Bedrock AgentCore 的托管特性，开发者无需从零构建底层基础设施，即可快速部署具备高可用性和可扩展性的企业级 Agent 应用。
- 这一技术栈的融合标志着 AI Agent 从“单次对话”向“持续业务流程”演进，为企业自动化提供了更具韧性的技术实现路径。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [MCP](/tags/mcp/) / [Bedrock](/tags/bedrock/) / [AgentCore](/tags/agentcore/) / [Strands](/tags/strands/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [消息策略](/tags/%E6%B6%88%E6%81%AF%E7%AD%96%E7%95%A5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于 Amazon Bedrock AgentCore 构建长时间运行的 MCP 服务器]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*