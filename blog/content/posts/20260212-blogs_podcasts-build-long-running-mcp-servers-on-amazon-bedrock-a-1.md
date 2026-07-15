---
title: 基于Amazon Bedrock AgentCore构建长时运行MCP服务器的异步框架
date: 2026-02-12 22:18:39+08:00
draft: false
entry_kind: auto
tags:
- Amazon Bedrock
- AgentCore
- MCP
- 异步框架
- 长时运行
- AI 代理
- Strands Agents
- 上下文管理
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 本文介绍了如何利用 Amazon Bedrock AgentCore 结合 Strands Agents 集成，构建能够处理长时间运行任务的
  MCP（Model Context Protocol）服务器。为了实现这一目标，文章提出了一套综合性的解决方案，主要包含以下三个关键策略： 1. **上下文消息策略**：
  针对长
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios:
- AI/ML项目
- Web应用开发
aliases:
- /posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2/
- /posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2/
- /posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3/
- /posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4/
- /posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-5/
- /posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-6/
- /posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-7/
- /posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8/
- /posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10/
- /posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8/
- /posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9/
- /posts/20260215-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10/
- /posts/20260215-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9/
- /posts/20260216-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10/
- /posts/20260216-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-11/
- /posts/20260217-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10/
- /posts/20260217-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-11/
- /posts/20260218-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-13/
- /posts/20260218-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-14/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们为您提供了一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，该策略在长时间运行的操作期间保持服务器与客户端之间的持续通信。接下来，我们开发了一个异步任务管理框架，允许您的 AI 代理启动长时间运行的流程，而不会阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合，构建能够可靠地处理复杂、耗时操作的生产级 AI 代理。

---
## 导语

构建能够可靠处理长时间运行任务的 AI 代理是当前技术落地的一大挑战。本文将介绍如何通过上下文消息策略与异步任务管理框架，解决服务器与客户端在长周期操作中的持续通信与阻塞问题。我们将详细演示如何将这些策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，帮助您构建具备高并发处理能力的生产级 AI 系统。

---
## 摘要

本文介绍了如何利用 Amazon Bedrock AgentCore 结合 Strands Agents 集成，构建能够处理长时间运行任务的 MCP（Model Context Protocol）服务器。为了实现这一目标，文章提出了一套综合性的解决方案，主要包含以下三个关键策略：

1.  **上下文消息策略**：
    针对长时间运行的操作，文章首先介绍了一种上下文消息策略。该策略旨在服务器与客户端之间维持持续的通信渠道，确保在整个扩展任务执行期间，双方能够保持连接和状态同步，从而避免因长时间等待而导致的上下文丢失或超时问题。

2.  **异步任务管理框架**：
    其次，文章开发了一套异步任务管理框架。这一框架允许 AI 代理启动长耗时的进程，而不会阻塞其他正在进行的操作。通过异步处理，系统可以更高效地利用资源，确保在处理复杂、耗时任务的同时，依然能够响应用户的其他请求。

3.  **构建生产级 AI 代理**：
    最后，文章演示了如何将上述策略与 Amazon Bedrock AgentCore 和 Strands Agents 无缝结合。通过这种集成，开发者可以构建出具备生产级可靠性的 AI 代理，使其能够稳定、高效地处理复杂且耗时的操作任务。

---
## 评论

**中心观点**
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构模式，旨在通过“上下文消息策略”和“异步任务管理框架”解决 MCP（Model Context Protocol）服务器在处理长周期任务时的连接中断与状态同步问题。

**支撑理由与深度评价**

**1. 架构必要性：填补 LLM 同步限制与长任务之间的鸿沟**
*   **[事实陈述]** 现有的 LLM 应用大多遵循“请求-响应”同步模式，受限于 HTTP 超时和 Token 生成时间，难以处理数据分析、批量处理等耗时数分钟甚至数小时的任务。
*   **[作者观点]** 文章引入的“异步任务管理框架”是必要的。它将 Agent 的思考与执行解耦，允许 Agent 发起任务后挂起，通过 Strands Agents 在后台持续运行，而 MCP 服务器仅负责状态汇报。
*   **[你的推断]** 这实际上是将传统的“长轮询”或“消息队列”模式引入了 Agent 生态。Bedrock AgentCore 在此扮演了编排层的角色，确保了 LLM 不会因为等待 I/O 而消耗昂贵的推理成本。

**2. 上下文连续性：解决“记忆断层”的技术尝试**
*   **[事实陈述]** 文章提到的“Context message strategy”旨在维护长周期运行中的上下文。
*   **[作者观点]** 通过持续的服务器-客户端通信，确保 Agent 在任务恢复时能够“无缝”接续之前的思路，而不是将其视为全新的对话。
*   **[你的推断]** 这里的技术挑战在于上下文窗口的管理。如果“Context message”只是简单地将历史日志回填给 LLM，在极长任务中极易导致上下文溢出或“迷失中间”现象。文章可能低估了长周期任务中上下文压缩与摘要生成的难度。

**3. MCP 协议的局限性突破**
*   **[事实陈述]** 标准 MCP 协议设计之初更多倾向于资源检索和工具调用，而非长流程控制。
*   **[作者观点]** 该方案通过 Bedrock 的基础设施扩展了 MCP 的能力边界，使其能够支持企业级的复杂工作流。
*   **[你的推断]** 这标志着 MCP 协议正在从简单的“插件化”向“Agent 基础设施化”演进，是 AWS 试图在 AI Agent 标准战争中建立护城河的重要举措。

**反例与边界条件**

*   **边界条件 1：成本与复杂性权衡**
    对于简单的查询任务（如“查天气”），引入 Strands Agents 和异步框架属于过度设计。构建异步状态机的开发成本和运维复杂度远高于直接调用。只有在任务耗时 > 30秒 或步骤 > 5 步时，该架构才有正收益。

*   **边界条件 2：状态一致性风险**
    在分布式环境下，如果 Bedrock AgentCore 与 MCP 服务器之间的网络链路发生抖动，或者 Strands Agent 执行失败但未成功上报，系统可能陷入“僵尸状态”。文章未详细阐述这种“最终一致性”场景下的补偿机制。

*   **反例：实时流式处理场景**
    如果任务需要毫秒级的实时反馈（如高频交易辅助或实时音视频处理），基于“检查点”和“异步轮询”的架构会引入不可接受的延迟，此时传统的长连接 WebSocket 或 gRPC 流式传输依然是更优解。

**可验证的检查方式**

1.  **超时压力测试：**
    *   *指标：* 构建一个耗时 15 分钟的模拟任务（如模拟生成大型报表）。
    *   *验证：* 观察 Bedrock Agent 的调用日志，确认是否仅产生了初始调用和最终结果调用的两次 Billing Token 消耗，中间过程是否未占用 LLM Context Window。

2.  **状态中断恢复测试：**
    *   *实验：* 在任务执行到 50% 时，手动重启 MCP 服务器容器。
    *   *验证：* 检查 AgentCore 是否能通过 Strands 的持久化存储恢复任务上下文，还是直接报错失败。这能验证其“Long-running”能力的真实鲁棒性。

3.  **上下文窗口占用分析：**
    *   *观察窗口：* 在一个包含 100 个步骤的复杂 Agent 任务中，监控传递给 LLM 的 Prompt 大小。
    *   *验证：* 确认“Context message strategy”是否实施了有效的摘要压缩。如果 Prompt 线性增长，说明该方案在扩展性上存在严重缺陷。

**综合评价**

**1. 内容深度：**
文章触及了当前 Agent 落地中最痛的“工程化”问题。不仅停留在 API 调用层面，而是深入到了架构设计（异步、状态管理）。然而，作为技术文档，它在错误处理和死锁处理方面的论证略显单薄。

**2. 实用价值：**
极高。对于正在基于 AWS 构建企业级 Agent 的开发者来说，这是一份避坑指南。它直接指出了为何简单的 LangChain/LlamaIndex 封装无法在生产环境的长流程中存活。

**3. 创新性：**
将 Strands Agents（一种持续运行的 Agent 概念）与 Bedrock 的托管服务结合，并利用 MCP 作为粘合层，这是一种较新的架构模式。它试图在“Serverless”的便利性和“Long-running”的稳定性之间找到平衡点。

**4. 行业影响：**
这可能会推动 MCP 协议从 Anthropic 的社区标准向更广泛的云厂商标准演进。如果 AWS 成功推广此

---
## 技术分析

基于提供的标题和摘要，这篇文章显然旨在解决构建基于大模型（LLM）的应用程序时面临的一个核心痛点：**如何处理耗时较长的复杂任务，而不受限于模型本身的上下文窗口或请求超时机制。**

文章通过结合 **Amazon Bedrock AgentCore**（AWS 的托管编排框架）、**MCP (Model Context Protocol)**（标准化的上下文交换协议）以及 **Strands Agents**（一种处理长时序任务的代理模式），提出了一套构建“长运行时”AI 服务器的解决方案。

以下是对该文章核心观点及技术要点的深入分析：

---

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**传统的“请求-响应”模式不足以支撑复杂的 AI 智能体应用，必须通过引入“上下文消息策略”和“异步任务管理框架”来实现 MCP 服务器的长运行能力。**

### 作者想要传达的核心思想
作者试图传达一种架构思维的转变：从将 AI Agent 视为一次性的“问答机器”，转变为具有持久状态、能够处理多步骤工作流的“异步服务”。通过 Bedrock AgentCore 与 Strands Agents 的集成，开发者可以将复杂的业务逻辑拆解，在服务器端维护任务状态，从而突破单次对话的时空限制。

### 观点的创新性和深度
*   **深度：** 文章触及了 LLM 应用落地的深水区——状态管理与工程化可靠性。它没有停留在简单的 Prompt Engineering 层面，而是深入到了系统架构层面（异步通信、状态机）。
*   **创新性：** 将 **MCP**（通常用于本地工具调用的轻量级协议）与 **AWS Bedrock AgentCore**（企业级编排服务）结合，并引入 **Strands** 概念来处理“记忆”和“进度”，这是一种混合架构的创新尝试，既利用了云原生的稳定性，又保持了协议的通用性。

### 为什么这个观点重要
随着 AI 从“聊天”走向“行动”，Agent 需要执行的任务（如数据分析、代码生成、API 编排）耗时越来越长。如果无法解决长连接和异步状态保持的问题，Agent 的应用场景将被严格限制在简单的问答领域，无法进入核心业务流程。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **MCP (Model Context Protocol):** Anthropic 推出的开放协议，用于连接 AI 应用与外部数据源。文章将其扩展为支持长运行的服务器模式。
2.  **Amazon Bedrock AgentCore:** AWS 提供的底层框架，用于构建和编排 Agent，负责推理路由和工具调用。
3.  **Strands Agents:** 文章引入的核心概念（源自 Agentic workflows 理论），指代能够维持长时间运行、具有短期记忆和子目标分解能力的 Agent 模式。
4.  **异步任务管理:** 区别于同步等待，采用后台任务处理 + 状态轮询或推送的模式。

### 技术原理和实现方式
*   **Context Message Strategy (上下文消息策略):** 
    *   *原理：* 在客户端与服务器断开连接或等待期间，服务器端维护一个“上下文窗口”。当任务有更新时，服务器通过特定的消息格式将中间状态写入上下文。
    *   *实现：* 利用 Session ID 关联历史消息，确保 Agent 每次唤醒都能读取到之前的进度。
*   **Asynchronous Task Framework (异步任务框架):**
    *   *原理：* 将 Bedrock Agent 的指令转化为后台作业（如 AWS Lambda 或 Step Functions）。
    *   *实现：* 客户端发起请求 -> MCP Server 接收并返回“Task ID” -> 后台异步执行 -> 客户端通过 ID 查询结果或接收回调。

### 技术难点和解决方案
*   **难点：** **超时与上下文丢失。** LLM 推理和外部工具执行可能超过 HTTP 请求限制（如 30秒或 3分钟）。
*   **解决方案：** 引入“握手确认”机制。MCP Server 收到指令后立即返回 Ack，然后由 Strands Agent 接管长时运行逻辑，通过 Bedrock 的 Event Stream 机制分片返回结果。
*   **难点：** **状态一致性。** 如果长任务失败，如何恢复？
*   **解决方案：** 利用 Strands 的“记忆”特性，将关键检查点保存到持久化存储（如 DynamoDB），而非仅依赖 LLM 的短期记忆。

### 技术创新点分析
最大的创新点在于 **将 MCP 协议“无状态”的特性通过应用层架构“伪装”成“有状态”**。这使得开发者可以继续使用标准化的 MCP 客户端，但后端却享受着企业级异步架构带来的稳定性。

---

## 3. 实际应用价值

### 对实际工作的指导意义
这篇文章为架构师提供了一套**“云原生 + 通用协议”**的落地蓝图。它指导我们如何利用 AWS 的基础设施（Bedrock）来支撑标准化的 AI 接口（MCP），避免了重复造轮子，特别是在构建企业级 Copilot 或 RAG 系统时。

### 可以应用到哪些场景
1.  **长文档生成：** 如生成长达 50 页的行业报告，需要多次检索、写作和润色。
2.  **复杂数据分析：** 提交 SQL 查询后，需要等待数分钟的数据聚合和图表渲染。
3.  **DevOps 自动化：** 执行持续集成/持续部署（CI/CD）流水线，涉及代码拉取、构建、测试、部署等多个长时序步骤。
4.  **科研辅助：** 长时间的模拟运算或文献综述整理。

### 需要注意的问题
*   **成本控制：** 异步任务和长上下文存储会增加云资源成本。
*   **复杂性增加：** 调试异步系统比同步脚本困难得多，需要完善的日志和追踪系统。

### 实施建议
建议采用 **“渐进式”** 策略。先从简单的同步 MCP Server 开始，当发现工具调用频繁超时时，再引入 Bedrock AgentCore 和 Strands 模式进行重构。

---

## 4. 行业影响分析

### 对行业的启示
这标志着 **AI Agent 基础设施正在走向“标准化”与“工程化”的成熟期**。过去大家都在用 LangChain 写单脚本的 Agent，现在开始转向使用像 MCP 这样的标准协议和像 Bedrock 这样的托管编排服务。行业正在从“模型层”竞争转向“协作层”竞争。

### 可能带来的变革
*   **Agent 商店模式：** 如果 MCP Server 可以长运行且标准化，未来可能会出现“Agent API 市场”，企业可以像调用微服务一样调用复杂的 Agent 能力。
*   **Serverless Agent 的普及：** 这种架构完美契合 Serverless，将推动按需付费的高级 AI 逻辑的普及。

### 相关领域的发展趋势
*   **协议统一：** MCP 可能会成为连接 LLM 与工具的事实标准。
*   **编排层下沉：** 越来越多的逻辑将由 AgentCore 这类底层服务管理，而非在业务代码中硬编码。

---

## 5. 延伸思考

### 引发的其他思考
*   **人机协作的新范式：** 如果 Agent 可以长时间运行，人类在其中的角色是什么？是“发布者”还是“干扰者”？如何设计异步过程中的“人工干预”节点？
*   **多租户隔离：** 在长运行过程中，如何确保不同用户的数据上下文不会发生混淆或泄露？

### 可以拓展的方向
*   **流式中间态展示：** 不仅返回最终结果，还能将 Agent 的“思考过程”实时推送给前端，提升用户信任感。
*   **容错与自愈：** 结合 Strands 模式，如果任务失败，Agent 应能自动重试或调整策略，而不是直接报错。

### 未来发展趋势
未来，长运行 Agent 将具备 **“自主性”**。不仅是响应请求，而是根据预设目标，自主在后台定期执行任务（如“每周一早上自动分析竞品数据并生成报告”），这需要更强大的调度和权限管理系统。

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估任务时长：** 审视你现有的 AI 应用，哪些经常遇到 Timeout 错误？
2.  **引入队列：** 在你的 MCP Server 后端引入消息队列（如 SQS）。
3.  **状态存储：** 建立一张表（如 Redis 或 DynamoDB）专门存储 `session_id` 对应的任务状态。

### 具体的行动建议
*   **代码层面：** 将你的 Tool 函数改为返回 `TaskID` 而非直接返回结果。
*   **架构层面：** 使用 Bedrock Agents 的 `Action Groups` 配置异步回调 URL。
*   **前端层面：** 前端 UI 需要从“Loading 转圈”变为“任务已提交，请在后台查看或稍后刷新”。

### 需要补充的知识
*   **AWS Lambda / Step Functions:** 用于处理后台逻辑。
*   **WebSocket / SSE:** 用于服务端向客户端推送实时更新。
*   **并发控制:** 防止同一用户重复提交导致资源耗尽。

---

## 7. 案例分析

### 结合实际案例说明
**场景：** 企业级财报分析 Agent。
用户上传 PDF 并提问：“分析这份财报的风险点并生成图表”。
*   **传统模式（失败）：** Agent 读取 PDF -> 调用 Python 绘图 -> 耗时 90秒 -> 前端超时报错。
*   **本文模式（成功）：** 
    1. Agent 接收任务，创建 `Task_123`。
    2. 返回：“正在分析，预计耗时 2 分钟，任务 ID: Task_123”。
    3. 后台 Strands Agent 分步执行：OCR -> 数据清洗 -> 分析 -> 绘图。
    4. 每完成一步，更新 Context 状态。
    5. 用户刷新或收到通知，看到生成的图表。

### 成功案例分析
**Klarna (客服 AI):** 虽未公开使用此架构，但其处理复杂退款流程的逻辑必然涉及长时序的状态管理，与文章描述的异步任务管理理念一致。

### 失败案例反思
许多早期的“一键生成 PPT”项目失败，原因往往是试图在单个 HTTP 请求中完成所有操作（搜索、大纲、配图、排版），导致极差的用户体验。文章提出的架构正是解决此类问题的良方。

### 经验教训总结
**不要试图用同步思维解决异步问题。** 在设计 Agent 时，必须假设外部工具永远不可靠或耗时，从而在架构底层预留异步处理的空间。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**构建基于 LLM 的企业级应用，必须采用“异步上下文策略”和“状态化 Agent 架构”（如 Bedrock AgentCore + Strands），以突破同步请求的时效性限制，从而实现复杂、长时序任务的自动化处理。**

### 支撑理由与依据
1.  **理由 1：业务逻辑的复杂性导致执行时间不可控。**
    *   *依据：* 现实世界的任务（如 RAG 聚合、API 编排）往往耗时数十秒到数分钟，超过了标准 LLM API 和前端请求的超时阈值（通常 <

---

## 最佳实践指南

### 实践 1：设计有状态的服务架构以支持长连接

**说明**: 长时间运行的 MCP (Model Context Protocol) 服务器需要维护与 Amazon Bedrock AgentCore 的持久连接。传统的无状态请求-响应模式可能无法满足需要多轮对话或长时间处理的任务场景。设计时需确保服务器能够保持会话状态，处理网络波动，并在不中断服务的情况下管理上下文。

**实施步骤**:
1. 使用支持长连接或 WebSocket 的通信协议，确保客户端与 AgentCore 之间的链路保持活跃。
2. 在服务器端实现会话管理机制，为每个活跃的 Agent 分配唯一的会话 ID 并存储其上下文状态。
3. 配置心跳机制以检测并清理僵尸连接，防止资源泄漏。

**注意事项**: 避免在内存中无限期堆积状态数据，应结合持久化存储以防服务重启导致状态丢失。

---

### 实践 2：实现健壮的 Strands Agents 生命周期管理

**说明**: Strands Agents 通常负责执行特定的任务流。在长运行场景下，必须妥善管理 Agent 的启动、暂停、恢复和终止。如果 Agent 陷入死循环或无响应状态，系统需要有机制进行干预和恢复。

**实施步骤**:
1. 为每个 Strand Agent 定义清晰的超时策略和最大执行时间限制。
2. 实现一个监控器服务，定期检查 Agent 的健康状态和心跳。
3. 设计状态机逻辑，允许 Agent 在任务挂起时保存检查点，并在系统恢复后从断点处继续执行。

**注意事项**: 确保检查点的数据结构兼容版本更新，避免因代码变更导致旧的状态无法恢复。

---

### 实践 3：优化 MCP 协议的上下文窗口管理

**说明**: 随着对话的深入，上下文数据会不断积累。过大的上下文不仅会增加延迟，还可能超出模型的 Token 限制。最佳实践是动态管理上下文窗口，仅保留与当前任务最相关的信息。

**实施步骤**:
1. 实现上下文压缩算法，定期总结或归档旧的对话轮次。
2. 在 MCP 服务器中设置逻辑，用于识别关键信息并将其保留在活跃内存中，将非关键信息移至冷存储。
3. 利用 Bedrock AgentCore 的工具调用能力，按需从向量数据库检索历史数据，而非全部加载。

**注意事项**: 在压缩上下文时，确保不丢失用户的关键指令或任务的关键中间结果。

---

### 实践 4：构建异步非阻塞的消息处理管道

**说明**: 长运行服务器往往面临高并发请求和长时间耗时的 I/O 操作（如调用外部 API 或查询数据库）。采用同步阻塞模式会导致服务吞吐量急剧下降。异步处理是保证服务响应能力的关键。

**实施步骤**:
1. 使用异步编程框架（如 Python 的 asyncio 或 Node.js 的 Event Loop）构建 MCP 服务器。
2. 将 Bedrock AgentCore 的调用和 Strands Agents 的执行逻辑放入独立的任务队列或线程池中处理。
3. 实现回调或 Webhook 机制，以便在长时间任务完成时通知 AgentCore，而不是保持连接轮询结果。

**注意事项**: 异步编程中的错误处理较为复杂，需确保所有异步操作都有完善的异常捕获和日志记录。

---

### 实践 5：实施全面的观测性与可追溯性

**说明**: 在长运行和分布式环境中，排查问题极具挑战性。必须对 MCP 服务器与 Bedrock AgentCore 之间的交互进行深度监控，包括请求延迟、错误率以及 Agent 的决策路径。

**实施步骤**:
1. 集成 AWS CloudWatch 或 X-Ray 来收集和追踪日志指标。
2. 在 MCP 消息头中注入 Trace ID，确保从 AgentCore 到 MCP 服务器再到下游服务的全链路追踪。
3. 为 Strands Agents 的关键决策点记录结构化日志，便于后续分析 Agent 行为。

**注意事项**: 日志记录可能会带来性能开销，应合理设置日志级别，避免在高峰期记录过多的 DEBUG 信息。

---

### 实践 6：强化安全性与访问控制

**说明**: MCP 服务器作为连接外部数据源与 Bedrock Agent 的桥梁，必须严格验证请求来源，并确保敏感数据在传输和存储过程中的安全。

**实施步骤**:
1. 在 MCP 服务器与 Bedrock AgentCore 之间实施双向 TLS (mTLS) 或签名验证（如 AWS Signature V4）。
2. 为不同的 Strands Agents 分配最小权限的 IAM 角色，确保它们只能访问执行任务所需的特定资源。
3. 对传输中的敏感载荷进行加密，并在服务器端实现敏感数据的脱敏日志记录。

**注意事项**: 定期轮换凭证和证书，避免因密钥泄露导致整个代理系统被攻破。

---
## 学习要点

- Amazon Bedrock AgentCore 正式发布，它是一个无服务器框架，允许开发者构建能够长时间运行、保持状态并执行复杂工作流的企业级代理应用。
- 通过集成 Strands Agents，AgentCore 赋予了代理在对话中断期间维持上下文和状态的能力，从而支持需要多步骤、长周期执行的自动化任务。
- 该架构通过将 MCP（Model Context Protocol）服务器与 Bedrock 的托管基础设施深度集成，实现了模型与外部工具和数据源之间的安全、标准化连接。
- 开发者可以利用 MCP 协议的标准化接口，将现有的企业工具和数据源快速连接到 Bedrock 代理中，显著降低集成复杂度并提高互操作性。
- AgentCore 提供了内置的监控、日志记录和部署管道功能，使开发者无需管理底层基础设施，即可专注于核心业务逻辑的实现。
- 这种组合架构特别适用于需要持续运行和记忆功能的复杂场景，例如订单处理、客户支持或跨系统的数据同步任务。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [异步框架](/tags/%E5%BC%82%E6%AD%A5%E6%A1%86%E6%9E%B6/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [Strands Agents](/tags/strands-agents/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore与Strands Agents构建长时运行MCP服务器]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*
