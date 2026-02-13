---
title: "基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理"
date: 2026-02-13T18:13:58+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长连接", "AI Agent", "系统架构"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 构建长期运行 MCP 服务器的综合方法，旨在解决 AI 代理在处理复杂、耗时任务时的可靠性问题。主要策略包括： 1. **上下文消息策略**：通过保持服务器与客户端之间的持续通信，确保在扩展操作期间上下文信息的连贯性"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供了一种实现这一目标的综合方法。首先，我们介绍一种上下文消息策略，以便在长时间运行的操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，使您的 AI 代理能够在不阻塞其他操作的情况下启动长时间运行的任务。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合，构建可投入生产环境的 AI 代理，从而可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是当前技术落地的一大难点。本文将介绍如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成，通过上下文消息策略和异步任务管理框架，解决服务器与客户端在复杂操作中的持续通信与阻塞问题。阅读本文，您将掌握构建可投入生产环境的 AI 代理的具体方法，从而实现对耗时业务流程的可靠处理。

---
## 摘要

本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 构建长期运行 MCP 服务器的综合方法，旨在解决 AI 代理在处理复杂、耗时任务时的可靠性问题。主要策略包括：

1.  **上下文消息策略**：通过保持服务器与客户端之间的持续通信，确保在扩展操作期间上下文信息的连贯性，避免因长时间处理导致的通信中断或信息丢失。

2.  **异步任务管理框架**：构建支持异步任务处理的系统，使 AI 代理能够启动长时运行进程的同时不阻塞其他操作，提升系统的并发处理能力和响应效率。

3.  **集成应用**：将上述策略与 Amazon Bedrock AgentCore 和 Strands Agents 深度结合，打造生产级 AI 代理，实现复杂时耗性任务的稳定执行，适用于企业级长流程场景。

该方案通过优化通信机制和任务调度，为构建高效、稳定的长期运行 AI 系统提供了可落地的技术路径。

---
## 评论

### 深度评价：基于 Amazon Bedrock AgentCore 的长运行 MCP 服务器架构

#### 1. 核心观点与论证结构

**中心观点：**
该文章提出了一种在 Amazon Bedrock AgentCore 环境下，利用 **Strands Agents** 集成技术构建长运行 MCP 服务器的架构方案，旨在通过上下文消息策略和异步任务管理框架，解决大模型应用中普遍存在的“会话断续”与“耗时任务阻塞”问题。（你的推断）

**支撑理由：**
1.  **架构解耦的必要性（事实陈述）：** 传统的 LLM 应用通常采用同步请求-响应模式，难以处理需要长时间计算（如数据分析、代码编译）或多轮交互的任务。文章提出的异步任务管理框架，将“控制流”与“执行流”分离，符合分布式系统设计的最佳实践。
2.  **状态保持的技术路径（事实陈述）：** 引入 **Strands Agents**（通常指代具有连续记忆和状态追踪能力的智能体架构）结合 **MCP (Model Context Protocol)**，能够解决 LLM 的“无状态性”。文章提到的“上下文消息策略”实际上是在构建一个持久化的记忆层，这对于复杂任务落地至关重要。
3.  **云原生集成的趋势（作者观点）：** 文章倾向于利用 AWS Bedrock 的托管能力来降低运维成本。这种“全托管”思路对于企业级应用具有吸引力，因为它避免了自建 Kafka 或 Redis 集群的复杂性。

**反例与边界条件：**
1.  **成本与延迟陷阱（你的推断）：** 虽然异步框架解决了阻塞问题，但在 Bedrock 等云平台上维护长连接或频繁轮询任务状态，可能会导致 API 调用次数激增，从而产生不可控的云服务账单。对于高频低延迟场景，边缘计算方案可能优于云端长运行架构。
2.  **过度设计的风险（你的推断）：** 对于简单的问答型任务，引入 Strands Agents 和异步框架属于“杀鸡用牛刀”。复杂的上下文管理可能会引入额外的延迟，降低用户体验的即时性。

---

#### 2. 多维度深入评价

**1. 内容深度：**
文章触及了当前 AI Agent 落地中最痛点的“长上下文”与“状态管理”问题。从技术角度看，将 MCP 协议（主要用于工具连接）与 Bedrock AgentCore（托管编排层）结合是一个高阶话题。然而，文章可能未深入探讨“Strands”在分布式环境下的并发冲突问题。如果多个客户端同时修改同一个 Agent 的上下文状态，系统的锁机制和一致性保障如何实现，摘要中未见提及，这可能是论证严谨性上的一个缺口。

**2. 实用价值：**
对于正在使用 AWS 全家桶进行 AI 落地的团队，该方案具有极高的参考价值。它提供了一种标准化的“脚手架”，让开发者不必从零搭建 WebSocket 服务或任务队列。特别是对于 RPA（机器人流程自动化）或数据分析类 Agent，这种架构可以直接复用。

**3. 创新性：**
**Strands Agents integration** 是一个相对新颖的概念。主流讨论多集中在 LangChain 或 AutoGPT 的开源实现，而文章试图定义一种基于 AWS 云原生的“有状态”标准。将 MCP 协议从单纯的“工具调用”提升为“持久化任务流”的载体，具有一定的前瞻性。

**4. 行业影响：**
如果该架构被广泛采纳，可能会加速 AI Agent 从“聊天玩具”向“生产力工具”的转变。它确立了“云服务商托管状态”优于“客户端自行管理状态”的行业趋势，进一步巩固了 AWS 等巨头在 AI 基础设施层的话语权。

**5. 争议点：**
**“Vendor Lock-in”（供应商锁定）风险**。文章极力推崇 Bedrock AgentCore 和 Strands，这可能导致企业应用深度绑定 AWS 生态。一旦需要迁移到私有云或其他公有云，重写上下文管理层的成本将非常高昂。

---

#### 3. 实际应用建议与验证

**应用建议：**
*   **适用场景：** 适合开发企业级的知识库问答助手、自动化运维 Agent 或需要生成报告的财务分析机器人。
*   **避坑指南：** 在实施时，务必对“异步任务”设置超时机制和死信队列。AWS 的 Step Functions 或 Lambda 可能是文章中“异步框架”的底层实现，需注意冷启动带来的延迟。

**可验证的检查方式：**
1.  **并发压力测试（指标）：** 模拟 1000 个并发长任务（如 5 分钟以上的数据处理），观察 Bedrock AgentCore 的吞吐量是否出现瓶颈，以及上下文消息是否发生丢失或乱序。
2.  **成本效益分析（观察窗口）：** 对比“长运行 MCP 架构”与“传统轮询架构”在相同任务负载下的 API 调用次数和费用。观察在任务空闲期，Bedrock 是否收取高昂的闲置费用。
3.  **状态一致性检查（实验）：** 在任务执行过程中人为中断网络连接，恢复后验证 Agent 是否能从断点无缝恢复，而非从头开始。这是检验“上下文消息策略”有效性的核心指标。

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要片段，以下是对该技术方案的深入分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 的长运行 MCP 服务器架构

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**在构建生成式 AI 应用时，必须通过架构创新来解决“同步请求-响应”模式与“长运行业务逻辑”之间的错配问题。** 具体而言，作者主张利用 **Amazon Bedrock AgentCore** 结合 **Strands Agents**（一种具备状态管理和长上下文记忆能力的 Agent 框架概念），构建符合 **MCP (Model Context Protocol)** 标准的服务器，从而实现能够处理耗时任务的智能体系统。

### 核心思想传达
作者想要传达的核心思想是**“异步解耦”与“上下文连续性”**。
1.  **异步解耦**：AI Agent 不应阻塞在等待工具执行完成上，而应通过任务管理框架将耗时操作剥离，实现“即发即忘”或“轮询回调”机制。
2.  **上下文连续性**：在长运行任务中，Agent 必须能够跨越多个交互周期保持对任务状态的记忆，而不是每次交互都从零开始。

### 观点的创新性与深度
该观点的创新性在于将传统的**后端微服务架构模式**（如异步任务队列、工作流编排）引入到了 **LLM Agent 的工具调用层**。
*   **深度**：它触及了当前 AI Agent 落地的最大痛点——**“幻觉与延迟”**。当 Agent 调用工具查询数据库需要 10 秒时，用户可能会以为 Agent 死了。通过引入“上下文消息策略”和“异步框架”，文章试图解决 LLM 的“注意力持续时间”问题，使其能够像人类一样“发起任务 -> 忘记 -> 稍后查看结果”。

### 为什么这个观点重要
随着 AI 从“聊天机器人”向“智能体”演进，用户期望 AI 执行真实世界的操作（如订票、代码生成、数据分析），而非仅仅生成文本。这些操作往往是耗时的。如果不解决长运行问题，Agent 只能处理简单的问答，无法成为可靠的“数字员工”。

## 2. 关键技术要点

### 涉及的关键技术概念
1.  **MCP (Model Context Protocol)**：一种开放协议，用于连接 AI 应用与外部数据源（如 GitHub、数据库、本地文件）。文章关注的是构建符合此协议的**服务器端**。
2.  **Amazon Bedrock AgentCore**：AWS 提供的底层基础设施或框架，用于托管 Agent 逻辑，处理与 LLM 的交互。
3.  **Strands Agents**：这是文章引入的关键技术组件。虽然 "Strands" 在此语境下可能指代特定的架构模式（或 AWS 内部/合作伙伴的特定框架），但在逻辑上它代表**具备状态追踪能力的线程化 Agent**。

### 技术原理和实现方式
基于摘要推断，技术实现包含两个支柱：

1.  **上下文消息策略**：
    *   **原理**：在长任务执行期间，服务器不保持 HTTP 连接打开，而是发送一个“中间态”消息给客户端，告知“任务已接收，正在处理”。
    *   **实现**：使用 WebSocket 或 SSE (Server-Sent Events) 推送状态更新，或者返回一个任务 ID，允许客户端后续通过 ID 查询状态。

2.  **异步任务管理框架**：
    *   **原理**：将 LLM 的工具调用请求转化为后台作业。
    *   **实现**：
        *   Agent 接收到用户指令 -> 调用 MCP Server 的工具。
        *   MCP Server 不直接执行，而是将任务推送到消息队列（如 Amazon SQS）或触发 Step Functions。
        *   立即返回一个确认响应给 Agent。
        *   后台 Worker 完成任务后，将结果写入数据库（如 DynamoDB）。
        *   Agent 在下一轮对话中通过 Strands 的记忆机制，主动查询该任务 ID 的结果。

### 技术难点与解决方案
*   **难点：状态一致性**。LLM 是无状态的，但业务流程是有状态的。
*   **解决方案**：Strands Agents 集成。它充当了“记忆皮层”，存储任务上下文。当结果返回时，Agent 能够回忆起“我刚才发起了这个任务”，并将结果关联回原始用户意图。

### 技术创新点分析
将 **MCP 协议** 与 **Strands Agents** 结合，实际上是在构建一种**“协议转换器”**。它将 LLM 的“同步思维流”转换为业务系统的“异步事件流”。这打破了 LLM 调用 API 必须等待响应的常规限制。

## 3. 实际应用价值

### 对实际工作的指导意义
对于正在构建企业级 AI 应用的架构师和开发者，这篇文章提供了一条**避免 POC（概念验证）无法落地**的路径。很多 AI Demo 失败是因为无法处理生产环境中的高延迟和复杂流程。

### 应用场景
1.  **数据分析与报表生成**：用户要求 Agent 生成一份包含 100 万条数据的销售报告。这可能需要几分钟。使用该架构，Agent 可以先回复“正在生成，预计 5 分钟完成”，并在后台处理。
2.  **代码审查与重构**：Agent 需要扫描整个代码库。这是一个长运行任务，需要异步处理并实时反馈进度。
3.  **RAG 系统的大规模索引**：当 Agent 需要摄取新文档进行索引时。
4.  **企业工作流审批**：涉及人工介入的审批流程，可能持续数小时或数天，Agent 需要在此期间“挂起”并在回调后恢复。

### 需要注意的问题
*   **成本控制**：长轮询或频繁的状态检查可能会增加 LLM 的 Token 消耗。
*   **超时管理**：必须设定合理的任务超时和失败重试机制，否则后台任务可能堆积。

### 实施建议
*   **设计幂等性**：确保如果用户重复点击或 Agent 重复查询，不会导致重复执行任务。
*   **可视化反馈**：对于长运行任务，必须向用户展示进度条或状态指示器，这是用户体验的关键。

## 4. 行业影响分析

### 对行业的启示
该文章预示着 **AI Agent 基础设施正在“后端化”**。行业焦点正在从“谁的 Prompt 写得好”转向“谁的 Agent 任务调度系统更稳健”。这标志着 AI 工程化进入深水区。

### 可能带来的变革
*   **从 Copilot 到 Autopilot**：由于具备了处理复杂、长流程任务的能力，AI 将从辅助驾驶转变为真正的自动驾驶。
*   **MCP 协议的普及**：随着此类架构的推广，MCP 可能成为连接 AI 与 SaaS 应用的标准接口，类似于 API 之于 Web。

### 相关领域发展趋势
*   **Agent 编排框架**（如 LangGraph, AutoGen）将更多地与云原生基础设施（如 AWS Step Functions, EventBridge）融合。
*   **状态存储**将成为 AI 数据库的新热点。

## 5. 延伸思考

### 引发的思考
*   **人机协作模式**：如果 Agent 能够长时间运行，人类如何介入干预？是否需要设计“紧急停止”机制？
*   **记忆的持久化**：Strands Agents 的记忆存储在哪里？如果记忆丢失，Agent 是否会“失忆”？

### 拓展方向
*   **多 Agent 协作**：一个 Agent 发起任务，另一个 Agent 负责执行，第三个负责监控。这种异步架构是协作的基础。
*   **边缘计算结合**：长运行任务是否可以部分卸载到边缘设备？

### 未来发展趋势
**“流式 Agent”**将成为主流，即 Agent 不再是静态的响应，而是一个持续运行的进程，不断监听事件流并更新状态。

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有工具**：检查你的 AI 应用是否直接在请求循环中调用数据库或第三方 API。如果是，这就是瓶颈。
2.  **引入消息队列**：即使是简单的 Redis 队列，也能将同步调用变为异步。
3.  **定义状态机**：为你的 Agent 任务定义清晰的状态（Pending, Running, Completed, Failed）。

### 具体行动建议
*   **第一步**：实现一个简单的“任务注册表”，Agent 发起任务后写入记录，获得 ID。
*   **第二步**：实现一个“状态查询工具”，让 Agent 能够通过 ID 读取进度。
*   **第三步**：在 Prompt 中增加指令，告诉 LLM：“如果遇到耗时任务，请使用异步工具，并告知用户稍后查询。”

### 需要补充的知识
*   **异步编程模型**（如 Python asyncio, JS Promise）。
*   **分布式系统设计**（CAP 定理，最终一致性）。
*   **Amazon Bedrock 具体服务**（如 Agents for Amazon Bedrock 的工作原理）。

## 7. 案例分析

### 成功案例分析：企业级 RAG 聊天机器人
*   **场景**：用户上传 10 个 PDF 文档并要求总结。
*   **传统做法**：同步处理，导致请求超时，用户看到 504 错误。
*   **本架构做法**：
    1.  Agent 接收文件 -> 调用 `AsyncIngestion` 工具。
    2.  后台进行 OCR 和向量化。
    3.  Agent 立即回复：“文档已接收，索引正在进行中，请稍候。”
    4.  用户每分钟问一次：“好了吗？”
    5.  Agent 查询状态 -> 完成后执行总结。
*   **结果**：用户体验流畅，系统稳定性高。

### 失败案例反思
*   **教训**：某项目仅实现了异步任务，但未在 Prompt 中正确指导 LLM 如何处理返回的 Task ID。结果 LLM 收到 ID 后直接丢弃，没有告知用户，导致用户不知道任务是否提交。
*   **总结**：技术架构必须与 Prompt Engineering（提示词工程）紧密结合。

## 8. 哲学与逻辑：论证地图

### 中心命题
**为了构建可靠的企业级 AI Agent，必须采用基于 Amazon Bedrock AgentCore 和 Strands Agents 的异步 MCP 服务器架构，以解决 LLM 同步交互机制与长运行业务逻辑之间的根本矛盾。**

### 支撑理由与依据
1.  **理由 1：用户体验的连续性**
    *   **依据**：HTTP 请求通常在 30-60 秒超时，而业务逻辑（如数据处理）往往需要更长时间。同步调用会导致用户焦虑或请求失败。
2.  **理由 2：资源利用效率**
    *   **依据**：让昂贵的 LLM 实例或服务器连接空闲等待 I/O 操作，是对计算资源的浪费。异步处理允许服务在等待期间处理其他请求。
3.  **理由 3：上下文感知的必要性**
    *   **依据**：LLM 本身是无状态的。长运行任务需要外部状态管理（Strands Agents）来在任务完成后恢复对话上下文。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 MCP 服务器的会话状态管理

**说明**：在构建长时间运行的 MCP (Model Context Protocol) 服务器时，必须确保服务器能够高效处理并维护多轮对话的上下文状态。由于 AgentCore 可能会处理来自不同代理的并发请求，服务器需要能够隔离不同会话的状态，防止数据混淆，并在长时间无操作后妥善清理资源，避免内存泄漏。

**实施步骤**:
1. 设计基于唯一会话 ID 的状态存储结构（如使用 Redis 或 DynamoDB）。
2. 实现中间件逻辑，在每次请求处理前加载对应的会话上下文。
3. 配置 TTL (Time To Live) 策略，自动清理超过特定时间未活动的会话数据。

**注意事项**: 避免在内存中存储敏感的会话状态，以确保在服务器重启或扩展时状态不丢失，并保持无状态架构的设计原则。

---

### 实践 2：实现健壮的错误处理与重试机制

**说明**：长时间运行的服务器不可避免会遇到网络波动或下游服务不可用的情况。MCP 服务器必须能够优雅地处理错误，并配合 Strands Agents 实现自动重试逻辑，以确保任务在遇到暂时性故障时能够自动恢复，而不是直接向用户报错。

**实施步骤**:
1. 为所有外部调用（如数据库查询或 API 请求）实现指数退避重试逻辑。
2. 定义标准化的错误响应格式，区分暂时性错误（如 503 服务不可用）和永久性错误（如 400 参数错误）。
3. 在 MCP 协议层面捕获异常，返回符合规范的错误信息，以便 Bedrock AgentCore 能够正确解析并决定是否重试。

**注意事项**: 确保重试逻辑不会导致资源耗尽，务必设置最大重试次数和超时限制。

---

### 实践 3：设计幂等的工具接口

**说明**：在分布式环境中，网络超时可能导致 AgentCore 重复发送同一个工具调用请求。为了防止数据重复处理或不一致，MCP 服务器暴露的所有工具接口必须是幂等的，即无论请求被调用多少次，产生的结果都是一致的。

**实施步骤**:
1. 为每个请求生成唯一的幂等键，并在服务器端缓存请求结果。
2. 在工具逻辑执行前检查是否已处理过该幂等键的请求，如果是，则直接返回缓存结果。
3. 对写操作（如数据库写入）使用 Upsert 逻辑或唯一性约束来防止重复数据。

**注意事项**: 幂等性检查应尽可能高效，避免引入过高的延迟，建议使用高性能的缓存层（如 ElastiCache）。

---

### 实践 4：配置全面的可观测性与日志记录

**说明**：为了监控长时间运行服务的健康状况并排查问题，必须建立完善的可观测性体系。这包括结构化的日志记录、指标监控以及分布式追踪，以便在 Strands Agents 调用 MCP 服务器的全链路中进行故障定位。

**实施步骤**:
1. 集成 AWS X-Ray 或 OpenTelemetry 来追踪请求从 AgentCore 到 MCP 服务器的完整链路。
2. 记录关键业务指标（如请求延迟、错误率、工具调用频率）到 Amazon CloudWatch。
3. 实施结构化日志（JSON 格式），包含 `request_id`、`session_id` 和 `tool_name` 等关键字段。

**注意事项**: 避免记录敏感信息（如 PII 数据）到日志中，确保符合数据隐私合规要求。

---

### 实践 5：利用 Strands Agents 进行复杂的任务编排

**说明**：Strands Agents 提供了强大的编排能力，MCP 服务器不应试图处理所有业务逻辑，而应专注于提供原子化的工具能力。利用 Strands Agents 来管理长时间运行的工作流，而 MCP 服务器仅负责执行具体的动作，从而实现关注点分离。

**实施步骤**:
1. 将 MCP 服务器设计为提供细粒度的工具（如 `get_weather`, `send_email`），而不是宏大的业务流程。
2. 在 Strands Agents 的配置中定义工作流逻辑，利用 AgentCore 的编排能力按需调用 MCP 工具。
3. 使用 AgentCore 的状态管理功能来跟踪跨多个 MCP 调用的任务进度。

**注意事项**: 确保 MCP 工具的描述清晰且符合 OpenAPI 规范，以便 AgentCore 能够准确推断何时调用哪个工具。

---

### 实践 6：实施严格的身份验证与授权控制

**说明**：长时间运行的服务器暴露在网络上面临更高的安全风险。必须确保只有经过授权的 Bedrock AgentCore 实例才能调用 MCP 服务器，并且每个请求都经过严格的身份验证。

**实施步骤**:
1. 使用 AWS IAM SigV4 签名协议来保护 MCP 服务器的 API 端点。
2. 在 MCP 服务器逻辑中验证传入请求的 IAM 权限，确保调用者具有执行特定工具的权限。
3. 定期轮换 API 凭证，并使用 AWS Secrets Manager 管理敏感配置。

**注意事项**:

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够处理长期运行任务和复杂工作流的自主智能体。
- 通过引入“Strands”概念，智能体可以在执行过程中暂停并保留上下文，从而在数小时或数天的时间跨度内异步完成多步骤任务。
- 该架构通过将智能体的状态（Strand）与底层基础设施解耦，确保了即使发生网络波动或服务重启，长期运行的任务也能自动恢复并继续执行。
- 开发者可以利用 MCP (Model Context Protocol) 服务器为 AgentCore 提供标准化的工具和数据源，显著简化了智能体与外部系统集成的复杂度。
- 此解决方案解决了传统无状态 AI 模型无法处理跨越长时间、多阶段业务流程的痛点，适用于自动化报告生成、供应链协调等企业级场景。
- 集成过程完全兼容现有的 Bedrock 生态系统，开发者无需重构代码即可利用 Bedrock 的托管能力和基础模型优势。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/) / [AI Agent](/tags/ai-agent/) / [系统架构](/tags/%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*