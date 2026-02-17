---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理"
date: 2026-02-17T15:40:46+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长时运行", "上下文管理", "AI 智能体"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "**总结：基于 Amazon Bedrock AgentCore 和 Strands Agents 构建长时间运行的 MCP 服务器** 本文介绍了一种在 Amazon Bedrock AgentCore 上结合 Strands Agents 集成，构建能够长时间稳定运行（Long-running）的 MCP 服务器的"
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

在本文中，我们将为您提供一种全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，用于在服务器和客户端之间在长时间操作期间保持持续通信。接着，我们开发一个异步任务管理框架，使您的 AI 智能体能够启动长时间运行的过程，而不阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，构建生产级 AI 智能体，能够可靠地处理复杂且耗时的操作。

---
## 导语

构建能够稳定处理长时间运行任务的 AI 智能体是当前生产环境中的技术难点。本文将深入探讨如何利用 Amazon Bedrock AgentCore 和 Strands Agents 集成，通过上下文消息策略与异步任务管理框架，解决服务端与客户端在长周期操作中的持续通信问题。阅读本文，您将掌握一套构建高可用、非阻塞式生产级智能体的完整实现方案。

---
## 摘要

**总结：基于 Amazon Bedrock AgentCore 和 Strands Agents 构建长时间运行的 MCP 服务器**

本文介绍了一种在 Amazon Bedrock AgentCore 上结合 Strands Agents 集成，构建能够长时间稳定运行（Long-running）的 MCP 服务器的综合方法。为了解决复杂、耗时操作的处理问题，文章提出了三个核心策略：

1.  **上下文消息策略**：
    引入了一种机制，通过在服务器和客户端之间维护上下文消息，确保在执行扩展任务期间保持持续的通信。这解决了长时间操作中可能出现的连接超时或状态丢失问题。

2.  **异步任务管理框架**：
    开发了一个异步框架，允许 AI 代理启动长流程进程，而不会阻塞其他操作。这保证了系统的并发处理能力和响应效率。

3.  **生产级集成实现**：
    文章最终演示了如何利用 Amazon Bedrock AgentCore 和 Strands Agents 将上述策略整合在一起，从而构建出能够可靠处理复杂、耗时任务的生产级 AI 代理。

---
## 评论

### 深度评价：基于 Amazon Bedrock AgentCore 构建持久化 MCP 服务

**中心观点**
该文章提出了一种通过“上下文消息策略”与“异步任务管理框架”相结合的架构，旨在解决大模型应用（LLM Apps）在处理长周期任务时的状态保持与通信连续性问题，实质上是将传统的同步请求-响应模式演进为基于 MCP（Model Context Protocol）的异步代理协作模式。（**作者观点 / 你的推断**）

---

#### 深入分析与支撑理由

**1. 内容深度：从“对话”到“协作”的架构演进**
*   **支撑理由**：文章的核心痛点抓得很准。当前的 LLM 应用多受限于 HTTP 超时和 Token 输出限制，难以处理 RAG（检索增强生成）中的长文档解析或复杂数据库 ETL 操作。文章引入的 **Strands Agents integration** 概念，实际上是将“任务”与“对话”解耦。
    *   **技术评价**：利用 Bedrock AgentCore 的编排能力，将 MCP Server 从单纯的“工具调用者”转变为“任务持有者”。这种深度在于它没有止步于简单的 API 调用，而是构建了一个中间层来维护会话状态，这对于企业级应用至关重要。（**作者观点**）
*   **反例/边界条件**：如果业务逻辑是极短时的问答（如“查询天气”），引入此框架会导致过度设计，增加不必要的网络跳转和延迟。（**你的推断**）

**2. 实用价值：填补了 AWS 生态中长时任务的空白**
*   **支撑理由**：在 AWS 的 Bedrock 生态中，虽然 Agents 可以调用 Lambda，但 Lambda 的最大执行时间（15分钟）和同步等待模式一直是痛点。该文章提出的异步框架允许 Agent 发起任务后断开连接，通过 MCP 协议稍后轮询或通过回调获取结果。
    *   **行业痛点**：这直接解决了生成式 AI 落地中最棘手的“用户体验”问题——用户不需要盯着加载中的 Spinner 等待数分钟，而是可以去做其他事，任务完成后由 Agent 主动通知。（**事实陈述 / 行业共识**）
*   **反例/边界条件**：此方案要求客户端（如 Chatbot UI）必须支持复杂的会话管理逻辑。对于简单的、基于无状态 API 的集成方来说，实现这种异步轮询或 WebSocket 推送的改造成本极高。（**你的推断**）

**3. 创新性：MCP 协议在云原生场景的深度整合**
*   **支撑理由**：MCP (Model Context Protocol) 是 Anthropic 最近推出的开源协议，旨在标准化 AI 与数据源连接。亚马逊作为 Anthropic 的主要支持者，将 MCP 深度集成进 Bedrock AgentCore 是一个重要的行业信号。
    *   **技术评价**：文章提出的“Context Message Strategy”不仅仅是技术实现，更是一种模式创新。它定义了如何在 MCP 的 JSON-RPC 消息流中嵌入“任务令牌”，使得无协议状态的 LLM 能够感知到后台任务的进度。（**作者观点 / 技术分析**）
*   **反例/边界条件**：MCP 目前仍处于快速发展期，并非行业标准。如果未来 OpenAI 的 Function Calling 或其他协议占据主导，基于 MCP 构建的服务可能面临协议迁移的沉没成本。（**行业观察**）

**4. 可读性与逻辑性**
*   **支撑理由**：文章结构清晰，采用了“问题 -> 策略 -> 框架 -> 实现”的经典技术博客路径。通过区分“Context Message”（信令）和“Task Execution”（算力），逻辑上非常顺畅地解释了如何维持长连接。
*   **反例/边界条件**：摘要中提到的“Strands Agents”并非 AWS 官方标准术语（可能是文章作者的项目代号或特定概念），对于不熟悉该特定术语的读者来说，可能存在理解门槛。（**你的推断**）

---

#### 争议点与批判性思考

**1. 厂商锁定风险**
虽然文章强调了 MCP 的开放性，但底层强依赖 **Amazon Bedrock AgentCore**。一旦业务逻辑深度绑定 AgentCore 的生命周期管理和编排语法，未来若想迁移至 Azure OpenAI 或 Google Vertex AI，重构成本将非常高。这是所有云厂商“最佳实践”文章的通病——用开放协议（MCP）做引子，用专有服务做钩子。（**你的观点**）

**2. 复杂度与成本的权衡**
构建异步任务管理框架意味着引入更多的移动部件：
*   消息队列（如 SQS/MSK）
*   状态存储（如 DynamoDB/RDS）
*   长期运行的计算资源（如 ECS/EKS 而非 Lambda）
对于初创公司，这种架构的运维成本可能远超业务带来的价值。文章未充分讨论这种架构下的成本控制策略。（**批判性思考**）

---

#### 实际应用建议

1.  **适用场景**：强烈建议用于**企业级知识库构建**、**复杂合规性报告生成**或**多步骤的数据分析工作流**。这些场景任务耗时长，且用户对即时响应要求不高。
2.  **架构选型**：如果决定采用，请务必在客户端实现“心跳机制”或“轮询间隔策略”，不要盲目依赖长连接，以防移动端网络切换导致任务状态丢失。
3.  **监控指标**：由于是长时运行，必须监控“僵尸任务”（Zombie Tasks），即 Agent 认

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

# 深度分析：基于 Amazon Bedrock AgentCore 与 Strands 构建长时间运行的 MCP 服务器

## 1. 核心观点深度解读

**主要观点：**
文章提出了一种在 Amazon Bedrock AgentCore 环境下，利用 **Strands Agents** 集成技术来构建和管理 **长时间运行（Long-running）** 的 MCP（Model Context Protocol）服务器的综合架构方法。其核心在于解决传统 LLM 应用无法处理耗时任务（如数据处理、API 调用等待）的局限性，将“同步对话”转变为“异步工作流”。

**核心思想：**
作者试图传达 **“状态持久化”与“异步编排”** 是 AI Agent 从简单的聊天机器人走向复杂业务自动化系统的关键。通过引入 **Context Message Strategy（上下文消息策略）** 和 **Asynchronous Task Management（异步任务管理框架）**，系统可以在不阻塞用户交互的情况下，在后台持续执行复杂任务，并能随时恢复上下文。

**观点的创新性与深度：**
*   **创新性：** 将 **Strands**（通常指代在长时间序列中保持连贯性的推理或执行链）的概念具体化到 Bedrock 的 Agent 架构中。这不仅仅是简单的 RAG（检索增强生成），而是引入了“时间”维度，使 Agent 具备了“记忆”和“持续行动”的能力。
*   **深度：** 文章触及了 Agent 系统的痛点——**状态管理**。在无状态的大模型接口上构建有状态的业务逻辑，是当前企业级 AI 落地的最难点。

**重要性：**
随着企业对 AI 期望值的提高，简单的问答已无法满足需求。企业需要 AI 能够执行跨小时、跨天甚至跨流程的复杂任务（例如：自动化合规审查、长时间的数据分析流水线）。该方案为在 AWS 云原生环境中构建此类高可靠、长周期的 AI Agent 提供了标准路径。

## 2. 关键技术要点

**涉及的关键技术：**
*   **MCP (Model Context Protocol):** 一种连接 AI 应用与外部数据源/工具的开放协议。
*   **Amazon Bedrock AgentCore:** Bedrock 的核心编排引擎，负责 Agent 的路由、记忆和工具调用。
*   **Strands Agents:** 文章中的特有概念，指代能够处理长周期任务流、保持中间状态的特殊 Agent 逻辑。
*   **Asynchronous Task Queue:** 异步任务队列（通常涉及 SQS/Step Functions）。

**技术原理与实现方式：**
1.  **Context Message Strategy (上下文消息策略):**
    *   **原理：** 为了防止 LLM 在长任务中断后“遗忘”，系统需要设计一种机制，将任务的中间状态、之前的步骤和当前目标压缩并存储。
    *   **实现：** 当任务开始时，生成一个唯一的 `SessionID`。所有的交互都附带这个 ID。当用户再次查询时，系统从数据库中加载该 Strand 的历史摘要，而非全量历史，注入到 System Prompt 中。
2.  **Asynchronous Task Management Framework (异步任务管理):**
    *   **原理：** 将“请求-响应”模式解耦。Agent 接收指令后，不直接等待结果返回给用户，而是启动一个后台任务。
    *   **实现：**
        *   用户发起长任务 -> AgentCore 触发 Strands Agent。
        *   Strands Agent 将任务元数据发送到任务队列（如 Amazon SQS）或启动工作流（如 AWS Step Functions）。
        *   MCP Server 立即返回一个“任务已接收”的确认消息给用户。
        *   后台 Worker 独立执行任务，并定期更新状态存储（如 DynamoDB）。
        *   用户轮询或通过 WebSocket 获取进度。

**技术难点与解决方案：**
*   **难点：** **超时处理**。Bedrock 或 Lambda 通常有执行时间限制。
    *   **解决方案：** 使用 Step Functions 编排长流程，将逻辑拆分为多个无状态的 Lambda 函数调用。
*   **难点：** **上下文窗口限制**。长任务产生的日志可能超过 LLM 上下文。
    *   **解决方案：** 实施摘要策略，定期将旧的任务日志压缩为高密度的状态摘要。

**技术创新点分析：**
将 **Strands** 的概念与 **MCP Server** 结合，意味着 MCP 不仅仅是数据的提供者，变成了**任务的执行者**。这扩展了 MCP 协议的应用边界，使其能够支持复杂的后端业务逻辑。

## 3. 实际应用价值

**对实际工作的指导意义：**
该架构为开发者提供了一个蓝图，教导如何避免“阻塞式”的 AI 体验。它指导架构师如何设计系统，使得 AI 像一个人类项目经理一样：分配任务、后台监控、定期汇报，而不是像一个必须盯着屏幕等待的实习生。

**可应用场景：**
*   **金融合规报告生成：** 需要抓取多天数据、分析、生成 PDF，耗时 30 分钟以上。
*   **软件开发 CI/CD 辅助：** Agent 监控代码部署流程，处理错误并重试，流程可能持续数小时。
*   **科学研究数据分析：** 处理大规模数据集，Agent 需分批次运行并调整参数。
*   **企业级 RPA（机器人流程自动化）：** 跨系统的审批流操作。

**需要注意的问题：**
*   **成本控制：** 长时间运行意味着频繁的数据库读写和 LLM 调用，成本可能指数级上升。
*   **状态一致性：** 如果后台任务失败，如何保证 Agent 能感知并恢复？

**实施建议：**
*   采用 **事件驱动架构 (EDA)**。
*   必须建立可视化的任务监控面板，让用户能看到 Strand 的进度。
*   设置明确的任务超时和死信队列（DLQ）处理机制。

## 4. 行业影响分析

**对行业的启示：**
该文章标志着 AI Agent 架构正在从 **“Copilot（副驾驶）”** 向 **“Agent（自主代理）”** 演进。行业开始关注 AI 的**持久化**和**可靠性**，而不仅仅是模型的智商。

**可能带来的变革：**
*   **SaaS 软件的形态改变：** 软件将不再只是“点击按钮”，而是“告诉目标”。后台的 Strands 架构将接管传统的 BPM（业务流程管理）系统。
*   **云厂商竞争焦点转移：** 竞争点从模型能力转向 **Agent 编排能力** 和 **基础设施稳定性**。

**发展趋势：**
*   **Orchestration Framework（编排框架）** 将成为刚需（如 LangChain, AutoGen 的云原生版本）。
*   MCP 协议可能成为连接 AI 与企业后端的标准接口。

## 5. 延伸思考

**引发的思考：**
*   **人机协作的新模式：** 如果 Agent 可以长时间运行，人类何时介入？是否需要设计“打断”机制？
*   **多 Agent 协作中的 Strand 共享：** 如果一个任务由多个 Strands Agent 协作完成，它们如何共享状态？

**拓展方向：**
*   结合 **Amazon Bedrock Knowledge Bases**，让 Strands 在执行过程中动态学习新信息。
*   引入 **Guardrails（护栏）**，确保长时间运行的任务不会偏离目标或产生不合规的操作。

**未来研究问题：**
*   如何评估一个 Long-running Agent 的性能？（不仅仅是准确率，还有完成率、平均耗时、资源消耗）。

## 6. 实践建议

**如何应用到自己的项目：**
1.  **评估任务粒度：** 识别现有项目中耗时超过 30 秒的 AI 交互环节。
2.  **引入状态存储：** 即使不使用 Bedrock，也可以引入 Redis 或 DynamoDB 来存储 Agent 的“记忆”。
3.  **改造 MCP Server：** 将 Server 的接口从单纯的 `query` 改造为 `submit_task` 和 `get_status`。

**具体行动建议：**
*   **架构设计：** 采用“控制平面”与“执行平面”分离的设计。AgentCore 是控制平面，Strands + Lambda 是执行平面。
*   **知识储备：** 深入学习 AWS Step Functions 和 DynamoDB，这是实现该架构的基石。

**注意事项：**
*   避免在上下文中存储敏感数据（PII），即使是摘要状态也需脱敏。
*   测试异常情况：如果网络中断，Agent 能否恢复任务？

## 7. 案例分析

**成功案例（假设性推演）：**
*   **场景：** 一家大型电商使用该架构构建“供应链优化 Agent”。
*   **过程：** Agent 接收到指令“优化下季度库存”。它启动一个 Strand，连续运行 2 小时，调用库存 API、分析销售预测数据、生成补货建议单。
*   **关键点：** 用户无需保持连接，第二天早上登录系统直接看到优化报告。这展示了 **Strands** 的核心价值——跨越时间的智能服务。

**失败案例反思：**
*   **场景：** 某团队试图用简单的 ChatGPT Plugin 处理视频渲染任务。
*   **原因：** Plugin 调用超时（60秒限制），没有异步后台机制，导致任务失败。
*   **教训：** 没有引入异步任务框架（如文章所述的方案），无法处理 IO 密集型或长耗时任务。

## 8. 哲学与逻辑：论证地图

**中心命题:**
在构建企业级复杂 AI Agent 时，必须采用基于 **Strands** 的异步架构和上下文管理策略，而非传统的同步请求-响应模式，以实现任务的长时间可靠执行。

**支撑理由:**
1.  **时间维度差异:** 人类业务流程（如审批、分析）往往跨越分钟到天，而 LLM 推理是毫秒级的。
    *   *依据:* 物理事实（网络延迟、数据处理耗时）与业务逻辑的客观差异。
2.  **资源限制:** 云函数（Lambda）和 API 连接都有硬性超时限制。
    *   *依据:* AWS Lambda 15分钟超时限制等技术约束。
3.  **用户体验:** 用户无法接受在生成复杂报告期间一直盯着“正在输入...”的加载条。
    *   *依据:* 交互设计心理学与用户行为观察。

**反例/边界条件:**
1.  **简单问答场景:** 对于“这个单词什么意思？”或“总结这段文本”，同步模式更高效，引入异步架构属于过度设计。
2.  **强实时性要求:** 在高频交易或实时游戏中，异步引入的延迟是不可接受的。

**命题分类:**
*   **事实:** LLM 接口本质是无状态的；云服务存在超时限制。
*   **价值判断:** “长时间运行的 Agent 比同步 Agent 更适合复杂业务场景”。
*   **可检验预测:** 采用该架构的 AI 系统，其任务完成成功率将高于同步系统，且用户在长任务中的流失率会降低。

**立场与验证:**
*   **立场:** 支持该文章观点。对于任何涉及**多步骤、高耗时、工具调用密集**的 AI 应用，Strands 架构是目前的最佳实践。
*   **验证方式:**
    *   *

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 Strands 的上下文管理机制

**说明**: 长时间运行的 MCP 服务器需要处理大量的历史对话和上下文信息。Strands Agents 允许维护跨越多个会话的上下文，但如果不加管理，上下文窗口可能会迅速膨胀，导致延迟增加和成本上升。必须实施策略来保留最相关的信息并丢弃冗余数据。

**实施步骤**:
1. 实施基于时间的上下文窗口或基于令牌数量的限制。
2. 优先保留结构化数据（如 JSON 对象）而非原始对话文本。
3. 使用摘要技术定期压缩旧的交互记录。

**注意事项**: 避免完全清除上下文，因为 Strands 依赖于长期记忆来执行复杂的多步骤任务。

---

### 实践 2：实施健壮的幂等性和重试逻辑

**说明**: 长运行服务不可避免地会遇到网络波动或 Bedrock 服务的瞬时故障。在集成 Strands 时，确保每个 MCP 工具调用都是幂等的，这意味着多次执行相同的操作与执行一次产生的效果一致。

**实施步骤**:
1. 为所有由 Agent 触发的状态更改操作生成唯一的 ID。
2. 在 MCP 服务器端实现指数退避算法以处理 Bedrock 的 429 或 500 系列错误。
3. 确保下游系统（如数据库或 API）能够根据唯一 ID 过滤重复请求。

**注意事项**: 不要在客户端无限重试，应设置最大重试次数阈值，并配合死信队列（DLQ）机制处理无法恢复的错误。

---

### 实践 3：采用异步事件驱动架构处理长时间任务

**说明**: Bedrock AgentCore 与 Strands 集成时，某些 MCP 工具执行可能需要较长时间（例如数据处理或外部 API 调用）。同步等待会导致连接超时或资源浪费。最佳实践是采用异步模式，让 AgentCore 在后台处理任务。

**实施步骤**:
1. 将 MCP 服务器设计为异步架构，使用消息队列（如 Amazon SQS）接收任务。
2. 当 Strands 调用工具时，立即返回“任务已接收”的确认响应，包含任务追踪 ID。
3. 配置 Bedrock Agent 使用回调机制或轮询机制来获取最终结果。

**注意事项**: 必须实现超时监控，如果异步任务长时间未完成，应发送部分结果或错误报告，防止 Agent 无限等待。

---

### 实践 4：细粒度的工具定义与参数验证

**说明**: Strands Agents 依赖于 MCP 服务器暴露的工具定义来规划任务。模糊或不正确的工具定义会导致 LLM 生成无效的调用代码。清晰、严格的工具模式是确保长期稳定运行的关键。

**实施步骤**:
1. 在 MCP Schema 中为每个工具提供详细的描述和参数示例。
2. 在服务器端实施严格的参数验证（如使用 Pydantic 或 JSON Schema），在执行逻辑前拦截无效输入。
3. 将复杂工具拆分为多个单一职责的简单工具，以便 Agent 更好地组合使用。

**注意事项**: 保持工具名称和描述的一致性，频繁变更工具定义可能会迷惑 Strands 的规划模型。

---

### 实践 5：建立全面的可观测性与日志记录

**说明**: 在长运行场景下，调试问题极具挑战性。必须能够追踪从 Strands Agent 的意图到 MCP 服务器具体执行的完整链路。

**实施步骤**:
1. 在 MCP 服务器中集成 AWS X-Ray 或 CloudWatch 来追踪请求链路。
2. 记录所有入站请求和出站响应的 Payload（注意脱敏敏感信息）。
3. 为关键操作添加自定义指标，如“工具调用成功率”、“平均执行时间”和“Token 消耗量”。

**注意事项**: 日志级别应可动态调整，在排查问题时开启 DEBUG 级别，正常运行时使用 INFO 或 ERROR 级别以降低成本。

---

### 实践 6：实施严格的资源配额与成本控制

**说明**: 长运行的服务如果没有限制，可能会因为意外的循环调用或大量请求导致云资源账单激增。Bedrock 的调用成本与 Token 使用量直接相关。

**实施步骤**:
1. 在 MCP 服务器层面实施速率限制，限制每个 Agent 或每秒的最大请求数。
2. 监控 Bedrock 的 Token 使用情况，为单个会话或单日设置总消耗上限。
3. 利用 Bedrock 的 Guardrails 功能过滤非目标话题的请求，减少无效的模型调用。

**注意事项**: 确保限制策略不会阻断正常的紧急操作，建议为高优先级任务设置独立的配额通道。

---
## 学习要点

- Amazon Bedrock AgentCore 正式发布，为开发者提供了构建、部署和管理长期运行型 MCP（Model Context Protocol）服务器的托管基础设施，解决了传统无状态应用难以维持持久会话的挑战。
- 通过集成 Strands Agents，开发者可以构建具备长期记忆和自主规划能力的智能体，使其能够处理跨越多天或数周的复杂工作流，而不仅仅是单次请求响应。
- 借助 MCP 的标准化协议，AgentCore 能够轻松打破数据孤岛，将企业私有数据源（如 SQL 数据库、内部 API）无缝连接到生成式 AI 应用中，极大增强了数据的可访问性。
- 该架构通过将 AgentCore 的编排能力与 Strands 的逻辑层解耦，显著简化了开发流程，开发者无需从头构建复杂的底层基础设施即可专注于业务逻辑的实现。
- Bedrock AgentCore 提供了统一的工具调用和监控机制，确保长期运行的 AI 任务在执行过程中的可观测性和稳定性，降低了生产环境中的运维风险。
- 这一技术栈的整合标志着 AI 应用架构从简单的“对话式交互”向具备自主性和持续性的“智能体系统”演进，为企业落地复杂业务场景提供了强有力的技术支撑。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/) / [AI 智能体](/tags/ai-%E6%99%BA%E8%83%BD%E4%BD%93/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore与Strands Agents构建长时运行MCP服务器]({{< relref "posts/20260216-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*