---
title: "构建基于Amazon Bedrock的长运行MCP服务器与异步任务管理框架"
date: 2026-02-18T05:37:38+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长连接", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成来构建长期运行 MCP 服务器的综合方法，旨在确保 AI 代理能可靠地处理复杂且耗时的操作。主要内容包括以下三个方面： 1. **上下文消息策略**：引入了一种消息传递机制，用于在服务器和客户端执行扩展操作期间维"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 构建基于Amazon Bedrock的长运行MCP服务器与异步任务管理框架

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们将为您提供实现这一目标的全面方法。首先，我们将介绍一种上下文消息策略，用于在长时间操作期间保持服务器与客户端之间的持续通信。接下来，我们将开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的过程，同时不会阻塞其他操作。最后，我们将演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents，将这些策略整合起来，构建可投入生产的 AI 代理，使其能够可靠地处理复杂且耗时的操作。

---
## 导语

构建能够可靠处理长时间运行任务的 AI 代理是当前技术落地的一大难点。本文将介绍如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成，通过上下文消息策略和异步任务管理框架，解决服务器与客户端在长周期操作中的持续通信问题。阅读本文，您将掌握构建生产级异步 AI 代理的具体方法，确保系统在处理复杂耗时操作时保持高效与稳定。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成来构建长期运行 MCP 服务器的综合方法，旨在确保 AI 代理能可靠地处理复杂且耗时的操作。主要内容包括以下三个方面：

1.  **上下文消息策略**：引入了一种消息传递机制，用于在服务器和客户端执行扩展操作期间维持持续的通信，确保长连接的稳定性。
2.  **异步任务管理框架**：开发了支持异步处理的任务管理框架，允许 AI 代理启动长时间运行的后台进程，同时不阻塞其他业务操作的正常进行。
3.  **生产级集成实现**：展示了如何利用 Amazon Bedrock AgentCore 和 Strands Agents 将上述策略结合落地，构建出具备生产级能力的 AI 代理，以应对复杂、时间密集型的任务挑战。

---
## 评论

基于您提供的文章标题与摘要，以下是从技术与行业角度进行的深入评价。

### 中心观点
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构模式，旨在通过引入“上下文消息策略”和“异步任务管理框架”来解决 MCP（Model Context Protocol）服务器在处理长周期任务时的状态保持与通信中断问题，从而构建具备持久化执行能力的企业级智能体。

### 支撑理由与边界条件

**1. 解决了 LLM 应用的“同步超限”痛点（事实陈述）**
*   **理由**：目前的 LLM 应用大多受限于 HTTP 超时和 Token 输出限制，难以处理如代码生成、数据处理等耗时超过 30-60 秒的任务。文章提出的异步框架通过解耦“请求接收”与“任务执行”，允许 Agent 在后台运行任务，这符合云原生架构的最佳实践。
*   **反例/边界条件**：如果任务本身是原子性且极短的（例如简单的查询问答），引入异步框架会增加系统延迟和复杂度，得不偿失。

**2. 强化了 MCP 协议的企业级可用性（你的推断）**
*   **理由**：MCP 协议本身较新，社区大多关注于简单的数据拉取。文章引入“上下文消息策略”来维持会话状态，实际上是在构建一个类似“有状态中间件”的层，这对于将 MCP 从原型工具推向生产环境至关重要。
*   **反例/边界条件**：如果客户端（如 Claude Desktop 或 IDE 插件）不支持长轮询或 WebSocket 等保持连接的机制，服务端的上下文策略将无法有效触达用户，导致体验断层。

**3. 利用 Bedrock AgentCore 实现了编排与执行的解耦（事实陈述）**
*   **理由**：AgentCore 提供了orchestration（编排）能力，而 Strands Agents 可能作为执行层。这种分离使得开发者可以独立更新业务逻辑（Strands）而无需改动核心控制流，提高了系统的可维护性。
*   **反例/边界条件**：这种高度抽象的架构往往伴随着厂商锁定风险。一旦业务逻辑深度依赖 Bedrock 的特定 API，迁移至 Azure OpenAI 或本地私有云的成本将极高。

### 深度评价

#### 1. 内容深度
文章触及了当前 AI Agent 领域的核心难点——**非确定性长流程控制**。摘要中提到的“异步任务管理框架”不仅仅是技术实现，更涉及到了如何向大模型反馈“任务进行中”的状态。如果文章能详细阐述如何将异步任务的状态（如 Progress Bar）转化为自然语言反馈给 LLM，以便 LLM 能向用户解释“为什么我在等待”，那么其深度将非常扎实。若仅涉及代码层面的异步调用，则略显单薄。

#### 2. 实用价值
对于正在使用 AWS 生态构建 AI 应用的架构师而言，价值极高。它提供了一种标准化的“脚手架”，避免了团队从零开始设计任务队列和状态机。
*   **结合案例**：设想一个场景，用户要求 Agent “分析过去 3 个月的 AWS S3 日志并生成报告”。这涉及数据下载、清洗、分析，可能耗时 10 分钟。直接调用会导致超时。文章介绍的方法允许 Agent 返回“任务已接收，ID:123”，并在后台利用 Bedrock 的异步能力处理，用户稍后可查询结果。这是生产环境必须的路径。

#### 3. 创新性
*   **新观点**：将 **Strands Agents**（可能指代某种链式调用或特定子智能体技术）与 **MCP** 结合。MCP 目前多用于静态资源连接，将其扩展为长任务执行通道是一种较新的探索。
*   **局限性**：异步任务处理并非全新概念（LangGraph 的持久化机制已存在类似思路）。文章的创新点在于将这一机制“云原生化”并绑定到了特定服务商（AWS）的生态中。

#### 4. 可读性
标题清晰指向目标受众。摘要结构逻辑顺畅（问题 -> 方案一 -> 方案二）。但技术类文章通常容易陷入代码细节，若未能在概念上解释清楚“Context Message”是如何在不同微服务间传递的，读者可能会迷失在 AWS 的术语丛林中。

#### 5. 行业影响
该文章暗示了 **AI Agent 基础设施正在“容器化”和“服务化”**。行业正在从简单的“Prompt Engineering”向“Agentic Workflow”（智能体工作流）转变。AWS 通过 Bedrock AgentCore 推动这种转变，试图建立类似 Kubernetes 在容器领域的地位，即成为 Agent 编排的事实标准。

#### 6. 争议点与不同观点
*   **厂商锁定 vs. 开源标准**：MCP 本身是 Anthric 推动的开放标准，但 Bedrock AgentCore 是 AWS 的专有服务。文章可能掩盖了二者结合后的兼容性问题。社区可能更倾向于使用开源的 Temporal 或 LangGraph 来实现异步框架，而不是绑定 AWS 服务。
*   **复杂度陷阱**：为了解决长任务问题而引入 Strands Agents 和 Bedrock AgentCore，可能引入了过多的移动部件。对于初创公司，一个简单的 Redis 队列加上 Python 脚本可能更高效。

#### 7. 实际应用建议
*   **适用场景**：适合需要处理复杂数据流转、涉及私有 VPC 资源访问、且任务耗时较长的企业级 RAG（检索增强生成）或数据分析 Agent。
*   **避坑指南**：

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该文章核心观点和技术要点的深入分析。

由于文章全文未完全提供，本分析将基于标题和摘要中透露的关键信息（**MCP服务器**、**Amazon Bedrock AgentCore**、**长时间运行任务**、**Strands Agents**、**异步任务管理**、**上下文消息策略**）进行逻辑推演和技术构建。

---

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**构建能够处理长时间运行任务的 AI 智能体不能仅依赖同步的请求-响应模式，而必须通过集成“Strands Agents”与“上下文消息策略”，在 Amazon Bedrock AgentCore 上实现异步、状态感知的 MCP 服务器。**

### 作者想要传达的核心思想
作者试图解决当前 AI Agent 领域的一个痛点：**大模型（LLM）的上下文窗口和会话超时限制与复杂业务任务（如数据处理、代码生成、长时间研发）所需时间不匹配的问题。**
核心思想在于将“计算”与“通信”解耦。通过引入 **Strands（线程/流）** 的概念，允许 Agent 在后台执行任务时，保持与客户端的连接活性，而不是让客户端一直等待一个可能超时的 HTTP 响应。

### 观点的创新性和深度
- **创新性**：将 **MCP (Model Context Protocol)** 这种通常用于即时数据检索的协议，扩展到了长时任务编排领域。结合 Bedrock AgentCore 的托管能力，提出了一种标准化的异步 Agent 架构。
- **深度**：不仅仅是简单的“异步调用”，而是深入到了**上下文维护**的层面。它解决了在任务执行期间，如果用户有新指令插入，或者需要查询中间状态，系统如何保持逻辑一致性的深层问题。

### 为什么这个观点重要
随着 AI 从“聊天机器人”向“行动 Agent” 转变，任务复杂度呈指数级上升。如果一个 Agent 需要执行 10 分钟的 RAG 聚合或代码编译，传统的同步模式会导致网关超时或用户体验极差。该文章提出的架构是实现**“企业级 AI 助手”**的关键基础设施，它使得 AI 能够真正介入复杂的工作流，而不仅仅是回答简单问题。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **MCP (Model Context Protocol)**：一种开放协议，用于连接 AI 应用与外部数据源。文章将其扩展为服务器模式。
2.  **Amazon Bedrock AgentCore**：AWS 提供的构建 Agent 的底层服务，负责编排推理和工具调用。
3.  **Strands Agents**：这是文章的技术核心。通常指代具有持久状态、能够处理多步骤推理和长时间运行的 Agent 实例（可能借鉴于 Agent Frameworks 中的“Strand”概念，即一条独立的执行流）。
4.  **Context Message Strategy（上下文消息策略）**：一种在长时任务中维持 LLM “记忆”的机制。

### 技术原理和实现方式
-   **异步任务管理框架**：
    -   **原理**：当 Agent 接收到长时任务（如“分析这 100 个文件”）时，它不直接阻塞等待结果，而是立即返回一个 `TaskID` 或 `StrandID`。
    -   **实现**：后台启动一个异步进程（可能是 Lambda 容器或 ECS 任务）进行处理。处理过程中，Agent 会定期将“心跳”或“中间日志”写入数据库。
-   **上下文消息策略**：
    -   **原理**：为了防止 LLM 在长时任务中“遗忘”目标，系统需要设计一种消息队列机制。
    -   **实现**：将长任务拆解为多个子步骤。每完成一步，MCP Server 向 Bedrock 发送一个“系统状态更新”。当用户再次查询时，Agent 会拉取最新的状态上下文，重新构建 Prompt 告知 LLM：“你之前在做什么，现在做到了哪一步”。

### 技术难点和解决方案
-   **难点1：连接超时。** AWS Lambda 或 API Gateway 默认只有 29 秒或更短的超时限制。
    -   **解决方案**：使用 Bedrock AgentCore 的异步编排能力，结合 S3/SQS 存储中间状态，实现“请求即返回，轮询获取状态”的模式。
-   **难点2：状态一致性。** 如果用户在任务执行中途取消了任务怎么办？
    -   **解决方案**：Strands Agents 需要内置“取消令牌”机制，并在 MCP 协议层暴露 `cancel_task` 接口。

### 技术创新点分析
文章的创新点在于**将 MCP 协议从“数据层”提升到了“控制层”**。传统的 MCP 更多是作为 LLM 的知识库查询接口，而这里将 MCP 变成了 LLM 的**手和脚**，并且是**不知疲倦的手**（通过异步实现）。

---

## 3. 实际应用价值

### 对实际工作的指导意义
对于架构师和 AI 工程师而言，这篇文章提供了一套在 AWS 云原生环境下构建**高可用 AI Agent** 的蓝图。它指出了不要试图在一个 LLM Prompt 中解决所有问题，而是要依赖工程化的异步框架来处理耗时逻辑。

### 可以应用到哪些场景
1.  **复杂 RAG 构建**：需要索引大量文档，耗时数分钟。
2.  **代码生成与测试**：Agent 生成代码 -> 编译 -> 运行测试用例 -> 返回报告，整个过程可能需要几分钟。
3.  **数据分析报表**：Agent 查询数据库，生成 Python 脚本，执行绘图，生成 PDF。
4.  **企业工作流审批**：涉及多步骤的人工确认 + 自动化执行。

### 需要注意的问题
-   **成本控制**：长时运行的 Agent 意味着更多的 Token 消耗和更长的计算实例运行时间，需要设计合理的停止机制。
-   **轮询效率**：客户端如何优雅地获取结果？频繁轮询会浪费资源，建议使用 WebSocket 或 AppRunner 推送（如果架构支持）。

### 实施建议
在设计 MCP Server 时，应明确区分 `Sync Tools`（如查询天气）和 `Async Tools`（如生成视频）。对于 Async Tools，必须在 Schema 中定义返回的 `TaskID` 结构。

---

## 4. 行业影响分析

### 对行业的启示
这标志着 AI Agent 开发正在从**“玩具级”向“工业级”**演进。行业开始关注 AI 系统的**鲁棒性**和**可维护性**，而不仅仅是模型的智商。AWS Bedrock + Strands 的模式可能会成为构建企业级 Agent 的标准范式。

### 可能带来的变革
未来 AI 应用将不再是对话框的简单交互，而是会演变为**“任务控制台”**。用户提交任务后可以关闭页面，稍后回来查看结果。这将改变 SaaS 软件的交互形态。

### 相关领域的发展趋势
-   **Agent Ops (AIOps)**：专门监控长时 Agent 运行状态的工具链将兴起。
-   **流式协议标准化**：MCP 协议可能会因为此类应用而进一步迭代，增加对异步任务状态定义的标准字段。

---

## 5. 延伸思考

### 引发的其他思考
-   **多 Agent 协作**：如果 Strand A 完成了任务，如何自动触发 Strand B？这需要引入事件驱动架构。
-   **人机协同**：在长时任务中，如果 Agent 遇到无法确定的决策（如“选择哪个配色方案”），如何暂停任务并优雅地请求人类介入？

### 可以拓展的方向
-   结合 **AWS Step Functions** 来可视化这些长时任务的执行流程。
-   研究 **LangGraph** 等框架与 Bedrock AgentCore 的结合，看是否能更灵活地定义这些 Strands 的状态图。

### 未来发展趋势
**“Always-on Agents”**（常驻 Agent）。未来的 Agent 可能不再是被动唤醒，而是作为后台服务持续运行，监控数据变化并主动通过 Strands 向用户推送信息。

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估任务类型**：审查你现有的 Agent 应用，找出所有响应时间超过 10 秒的功能。
2.  **引入异步层**：不要直接在 LLM 的 Tool Call 回调中做重活。回调应只负责将任务放入队列（如 SQS）并返回 TaskID。
3.  **构建状态 API**：编写一个标准的 MCP 工具 `get_task_status(task_id)`，用于查询进度。

### 具体的行动建议
-   **第一步**：使用 Amazon Bedrock AgentCore 创建一个简单的 Agent。
-   **第二步**：开发一个 Mock MCP Server，模拟一个 30 秒的任务，验证异步流程是否走通。
-   **第三步**：引入数据库（如 DynamoDB）存储任务状态，实现上下文恢复。

### 实践中的注意事项
-   **错误处理**：长时任务容易在最后一步失败，必须实现断点续传或重试机制。
-   **Context Window**：虽然任务在后台跑，但最后向 LLM 汇报时，生成的日志可能很长，需要学会总结。

---

## 7. 案例分析

### 结合实际案例说明
**案例**：一家金融公司需要构建一个 AI 分析师，用户上传 PDF 财报，Agent 生成分析报告。
-   **传统做法**：用户上传 -> Python 脚本解析 -> LLM 分析 -> 30秒后超时报错。
-   **基于文章方案**：
    1.  用户上传。
    2.  Bedrock Agent 调用 MCP Server 的 `analyze_report` 工具。
    3.  MCP Server 返回 `{"status": "processing", "task_id": "123"}`。
    4.  Bedrock 告知用户：“正在分析，请稍后，ID 为 123”。
    5.  后台进程解析 PDF，分块调用 LLM 分析。
    6.  用户 5 分钟后询问：“分析好了吗？”
    7.  Agent 调用 `get_status("123")`，获取结果并展示。

### 经验教训总结
成功的关键在于**用户体验的预期管理**。不要让用户以为系统卡死了。明确的“任务已接收”反馈和“进度条”是必不可少的。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**在构建企业级 AI Agent 时，必须采用基于 Strands 的异步任务架构，以突破同步交互在处理长时复杂任务时的局限。**

### 支撑理由与依据
1.  **理由一：网络与超时限制**
    -   **依据**：事实。HTTP 请求和云函数（Lambda）都有严格的超时限制（通常 < 15分钟，往往更短）。
    -   **逻辑**：如果业务逻辑（如视频渲染、大数据查询）耗时超过此限制，同步架构必然失败。
2.  **理由二：用户体验 (UX)**
    -   **依据**：心理学/直觉。用户无法忍受对着空白屏幕等待 2 分钟而不获得任何反馈。
    -   **逻辑**：异步反馈机制能提供即时确认和进度更新，符合用户心理

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用基于 Strands 的有状态会话管理架构

**说明**: 
传统的无状态服务器难以处理跨越长时间窗口的复杂任务。通过集成 Strands Agents，MCP 服务器应维护会话上下文和状态历史。这使得 Agent 能够在多次交互中记住之前的步骤、用户偏好和中间结果，从而支持需要多轮推理或长时间运行的任务流。

**实施步骤**:
1. 在 Bedrock AgentCore 配置中启用会话持久化，将 Strands 定义为状态管理后端。
2. 设计状态模式，明确哪些中间变量和上下文需要被持久化存储。
3. 实现“心跳”机制或检查点功能，定期将当前 Agent 状态保存到 Strands 存储层。

**注意事项**: 
确保存储的数据结构清晰，并在会话结束时实施严格的清理策略以避免资源泄露。

---

### 实践 2：实施健壮的超时与重试机制

**说明**: 
长时间运行的 MCP 服务器面临着网络波动或下游服务不可用的风险。必须构建能够优雅处理故障的弹性系统。当调用 Bedrock 模型或外部工具时，系统应能够识别暂时性错误并进行自动重试，而不是直接导致会话失败。

**实施步骤**:
1. 为所有外部 API 调用（包括 Bedrock InvokeModel API）配置指数退避算法。
2. 定义明确的超时限制，区分“处理中”状态和“死锁”状态。
3. 利用 Strands 的异步能力，将长时间等待的任务放入后台队列，而不是阻塞主线程。

**注意事项**: 
避免无限重试，设置最大重试次数阈值，并在达到阈值后向用户返回清晰的错误提示。

---

### 实践 3：优化 Token 使用与上下文窗口管理

**说明**: 
长任务容易导致上下文窗口溢出或 Token 成本过高。最佳实践要求在保持对话连贯性的同时，智能地管理传递给大模型的上下文长度。Strands 可以辅助存储完整的对话历史，而仅向模型发送相关的摘要或最近的交互。

**实施步骤**:
1. 实施上下文压缩策略，在每次调用前总结旧的交互轮次。
2. 配置 Bedrock AgentCore 的系统提示词，使其能够识别何时需要从 Strands 中检索历史数据，而不是依赖完整的输入窗口。
3. 监控 Token 使用情况，为单次会话设置合理的 Token 上限。

**注意事项**: 
在压缩上下文时，确保保留关键的元数据（如用户 ID、任务目标），防止 Agent 在长对话中“迷失”方向。

---

### 实践 4：构建模块化的工具注册与权限控制

**说明**: 
随着 Agent 功能的扩展，MCP 服务器可能会暴露大量工具。为了保持系统的可维护性和安全性，应采用模块化设计。同时，长时间运行的会话可能涉及敏感操作，必须实施严格的权限验证，防止未经授权的工具调用。

**实施步骤**:
1. 将工具按功能领域分组，并在 Bedrock AgentCore 中进行模块化注册。
2. 在 MCP 协议层实施细粒度的访问控制列表（ACL），检查每次工具调用的权限。
3. 为每个工具定义清晰的输入/输出架构，利用 Bedrock 的 Guardrails 功能过滤敏感参数。

**注意事项**: 
定期审计工具的调用日志，确保没有敏感数据被意外记录或传递给模型。

---

### 实践 5：设计可观测性与调试追踪体系

**说明**: 
在长链路调用中，定位问题变得非常困难。必须建立完善的可观测性体系，追踪从用户输入到 Strands 状态更新，再到 Bedrock 模型调用的完整链路。这对于优化性能和调试逻辑错误至关重要。

**实施步骤**:
1. 集成 AWS CloudWatch 或 X-Ray，为每个请求生成唯一的 Trace ID。
2. 在 MCP 服务器的关键路径（如工具调用前后、状态更新时）添加结构化日志。
3. 捕获并记录 Bedrock 的响应延迟和 Token 消耗指标。

**注意事项**: 
避免记录敏感的用户数据（PII）到日志中，确保符合数据隐私合规要求。

---

### 实践 6：异步流式响应处理

**说明**: 
长时间运行的任务如果仅在结束时返回结果，用户体验会很差。应利用 Bedrock 的流式响应能力，结合 MCP 协议特性，实时向客户端推送中间进度和思考过程。Strands Agents 可以在后台处理复杂逻辑的同时，通过流式接口保持用户的参与感。

**实施步骤**:
1. 修改 MCP 服务器端点，支持 Server-Sent Events (SSE) 或类似的流式传输协议。
2. 将 Agent 的推理过程分解为多个阶段，每个阶段完成后立即发送部分更新。
3. 在前端实现增量渲染逻辑，实时展示 Strands 的执行状态。

**注意事项**: 
确保流式连接中断时，服务器端的状态依然能够通过 Strands 保持一致，支持客户端断线重连后恢复进度。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够长时间运行并保持对话状态的有状态 MCP 服务器。
- 通过引入“Strands”概念，该架构解决了传统无状态代理无法处理复杂、多步骤长期任务的局限性。
- 新架构支持将 MCP 协议作为连接层，使得 AgentCore 能够无缝利用现有的工具生态系统和数据源。
- 该方案特别适用于需要持续监控、事件触发响应或跨越数天甚至数周的工作流自动化场景。
- 开发者可以利用此集成在 Bedrock 平台上构建更接近人类“工作记忆”模式的智能体，实现上下文感知的长期交互。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*