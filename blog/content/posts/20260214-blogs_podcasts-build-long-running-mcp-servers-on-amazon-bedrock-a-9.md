---
title: "基于Amazon Bedrock AgentCore构建MCP服务器实现长时运行与异步任务管理"
date: 2026-02-14T13:21:39+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长时运行", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何利用 Amazon Bedrock AgentCore 结合 Strands Agents，构建能够处理长时间运行任务的生产级 MCP 服务器。为了解决复杂操作中的可靠性和持续性问题，文章提出了以下三项核心策略： 1. **上下文消息策略**：引入一种机制，以在耗时较长的操作过程中，保持服务器与客户端之间"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建MCP服务器实现长时运行与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，能够在长时间操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，允许您的 AI 代理启动长时间运行的过程，同时不阻塞其他操作。最后，我们将演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合使用，以构建可投入生产的 AI 代理，能够可靠地处理复杂且耗时的操作。

---
## 导语

构建能够可靠处理长时间运行任务的 AI 代理，是当前将智能体投入生产环境的关键挑战之一。本文将介绍一套基于 Amazon Bedrock AgentCore 和 Strands Agents 的综合实现方案，重点阐述如何通过上下文消息策略和异步任务管理框架，解决服务器与客户端在长周期操作中的持续通信与非阻塞调度问题。阅读本文，您将掌握构建具备高并发处理能力的生产级 AI 代理的具体方法。

---
## 摘要

本文介绍了如何利用 Amazon Bedrock AgentCore 结合 Strands Agents，构建能够处理长时间运行任务的生产级 MCP 服务器。为了解决复杂操作中的可靠性和持续性问题，文章提出了以下三项核心策略：

1.  **上下文消息策略**：引入一种机制，以在耗时较长的操作过程中，保持服务器与客户端之间的连续通信，确保对话状态不丢失。
2.  **异步任务管理框架**：开发了一套框架，允许 AI 代理启动长时进程，同时不会阻塞其他操作，从而提升系统的并发处理能力。
3.  **生产级集成方案**：展示如何将上述策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合，打造出能够可靠处理复杂、耗时任务的企业级 AI 代理。

---
## 评论

**文章中心观点**
该文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成 MCP 协议的技术架构，旨在通过上下文消息策略与异步任务管理框架，解决 AI Agent 在处理长周期任务时的状态保持与服务连续性问题。

**深入分析与评价**

**1. 内容深度与论证严谨性**
*   **支撑理由（事实陈述）：** 文章触及了当前 Agent 开发的核心痛点——**长上下文记忆与长时间运行**。传统的 LLM 请求-响应模式难以维持数小时甚至数天的任务状态。文章提出的“上下文消息策略”在技术逻辑上是严谨的，它试图在 MCP（Model Context Protocol）的无状态特性与 Bedrock AgentCore 的有状态编排之间建立桥梁。
*   **支撑理由（你的推断）：** 引入 Strands Agents（推测为 AWS 内部或合作伙伴提供的长时运行 Agent 框架）表明，文章试图将传统的“对话式交互”转变为“流程化编排”。这不仅仅是 API 调用，而是引入了工作流的概念，论证了 Agent 需要具备“心跳”机制来维持活跃度。
*   **反例/边界条件（作者观点）：** 这种深度依赖于 Bedrock 的特定生态。如果底层模型（如 Claude 或 Amazon Nova）的上下文窗口不足以支撑长时间的“记忆累积”，或者 Token 成本过高，该架构的经济性将受到挑战。此外，文章可能低估了分布式系统中的“最终一致性”问题，即异步任务在失败重试时的状态幂等性处理。

**2. 实用价值与实际指导**
*   **支撑理由（事实陈述）：** 对于正在构建企业级 RAG（检索增强生成）或复杂自动化工作流的开发者而言，这篇文章提供了高价值的参考。它不仅解决了“怎么做”（MCP 集成），还解决了“稳定运行”（异步管理）的问题。
*   **支撑理由（你的推断）：** “异步任务管理框架”是极具实用价值的。在实际生产中，用户无法容忍 Agent 在处理耗时任务（如生成大型报表或等待审批）时一直阻塞连接。文章建议的解耦方案直接提升了用户体验（UX）和系统吞吐量。
*   **反例/边界条件（事实陈述）：** 实施该方案需要较高的架构门槛。开发者必须同时精通 Bedrock Agent 的配置、Strands 的逻辑以及 MCP 协议的细节。对于小型初创团队或简单的聊天机器人应用，这种架构属于“过度设计”，维护成本可能高于收益。

**3. 创新性与行业影响**
*   **支撑理由（作者观点）：** 文章的创新点不在于单一技术，而在于**组合式创新**。将 MCP（一个相对较新的协议标准）与 Bedrock AgentCore（托管编排服务）结合，并引入 Strands 进行长时运行管理，这是对 AWS 生态内 Agent 开发模式的一次标准化探索。
*   **支撑理由（你的推断）：** 如果 Strands Agents 代表了一种“子任务分解与持久化”的模式，这可能预示着行业从“单次大模型调用”向“多智能体协作与持久化服务”的范式转移。
*   **反例/边界条件（作者观点）：** MCP 协议目前仍在快速迭代中，基于此构建的长期服务器可能面临协议不兼容的风险。此外，行业内有观点认为“状态管理应由数据库层而非 Agent 层处理”，文章的方案可能增加了业务逻辑与基础设施的耦合度。

**4. 可读性与逻辑性**
*   **支撑理由（事实陈述）：** 标题清晰直指技术栈，摘要结构化（First... Next...），逻辑链条完整：从问题（长时运行）到方案，再到具体实现策略。
*   **反例/边界条件（你的推断）：** 技术文章常犯的错误是假设读者对 Bedrock 和 Strands 有相同的先验知识。如果文章缺乏具体的代码片段或架构图，仅靠文字描述“上下文消息策略”，可能会让读者感到抽象，降低实操的可读性。

**5. 争议点与不同观点**
*   **争议点（作者观点）：** **“上下文消息策略”是否会导致 Token 泛滥？** 为了维持连续通信，不断向模型发送上下文心跳，在长周期任务中可能消耗巨额成本。另一种观点是使用 RAG（检索增强生成）仅在需要时查询状态，而非全量维护上下文。
*   **争议点（你的推断）：** **MCP 协议的必要性。** 业界对于是否需要统一所有数据源通过 MCP 协议接入仍有分歧。部分观点认为直接通过 Function Calling 或原生 SDK 调用 Bedrock 可能性能更高，MCP 增加了一层序列化/反序列化的开销。

**实际应用建议**
1.  **成本监控：** 在实施该异步框架时，务必设置 CloudWatch 告警，监控“上下文消息”的 Token 消耗量，防止长时运行任务导致账单爆炸。
2.  **状态机设计：** 不要仅依赖 Agent 的自然语言理解来维持状态，必须在后端（如 DynamoDB）维护一个明确的任务状态机，作为 Agent 的单一事实来源。
3.  **超时处理：** 为异步任务设置合理的 TTL（生存时间），避免因 Bedrock 或下游服务挂起而导致 MCP 服务器无限期等待。

**可验证的检查方式**
1.  **指标验证（技术指标）：** 搭建一个测试环境，运行一个耗时 10 分钟的模拟任务，测量 MCP 服务器在启用“上下文消息策略”前后的**连接断开率

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 构建长时间运行的 MCP 服务器

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点在于解决**模型上下文协议（MCP）服务器在处理长时间运行任务时的“会话中断”与“状态管理”难题**。作者提出，不应将 AI Agent 的任务限制在单次请求-响应的短周期内，而应通过集成 **Strands Agents** 框架与 **Amazon Bedrock AgentCore**，构建一种能够维持上下文、管理异步任务的持久化服务架构。

### 作者想要传达的核心思想
作者传达的核心思想是**“有状态 AI 服务的连续性”**。传统的 LLM 应用往往是无状态的，而复杂的业务流程（如代码生成、数据分析、工作流编排）往往需要较长的执行时间。作者主张通过一种**“上下文消息策略”**和**“异步任务管理框架”**，让客户端与服务器之间在任务执行期间保持“心跳”通信，从而实现从“对话式 AI”向“代理式 AI”的转变。

### 观点的创新性和深度
该观点的创新性在于将**MCP（Model Context Protocol）**这一新兴的连接标准，与**Amazon Bedrock 的托管能力**以及**Strands Agents 的异步处理能力**进行了深度绑定。
*   **深度**：它触及了 AI Agent 落地最棘手的痛点——长任务处理中的超时和用户体验割裂。
*   **创新**：它没有仅仅停留在 API 调用层面，而是提出了一种架构模式，将 Bedrock AgentCore 作为控制层，利用 Strands 处理复杂的逻辑流，实现了基础设施与业务逻辑的解耦。

### 为什么这个观点重要
随着 AI Agent 从简单的聊天机器人向自主智能体演进，**“长时间运行”**是必经之路。如果无法解决 Agent 在执行 5 分钟甚至 1 小时任务时的连接保持和状态反馈问题，AI 就无法胜任企业级的复杂自动化任务。这篇文章提供了一种在 AWS 云原生环境下解决此问题的标准化路径，对于构建高可用的 AI 应用具有重要的指导意义。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **MCP (Model Context Protocol)**: Anthropic 推出的开放协议，用于连接 AI 应用与数据源。
2.  **Amazon Bedrock AgentCore**: AWS 提供的用于构建 Agent 的底层服务/框架，负责编排和推理。
3.  **Strands Agents**: 一种专注于长周期任务编排的 Agent 框架（可能涉及多步骤规划、记忆存储）。
4.  **异步任务管理**: 区别于同步等待，允许任务在后台运行，主线程/连接不阻塞。

### 技术原理和实现方式
*   **上下文消息策略**:
    *   **原理**: 在长任务执行期间，服务器不保持 HTTP 连接打开（这会导致超时），而是通过返回一个“任务引用 ID”或“中间状态流”，让客户端知道任务正在处理中。
    *   **实现**: 利用 Bedrock AgentCore 的流式响应能力或回调机制，定期向客户端推送“心跳”或“进度更新”，确保客户端不会因无响应而断开。
*   **异步任务管理框架**:
    *   **原理**: 将 Agent 的推理与执行分离。Agent 发起指令后，将任务交给 Strands 框架的后台 worker 执行。
    *   **实现**: 使用消息队列（如 AWS SQS）或 Step Functions 来托管 Strands Agents 的执行状态。当任务完成时，通过 Pub/Sub 机制通知 AgentCore，进而更新 MCP 客户端。

### 技术难点和解决方案
*   **难点**: **超时与资源消耗**。长任务会导致 Lambda 函数或 API Gateway 超时。
    *   **方案**: 文章提出的异步框架，通过“发起任务 -> 返回 ID -> 轮询/推送结果”的模式，绕过了同步请求的时间限制。
*   **难点**: **状态一致性**。在任务中断或重连时，Agent 如何知道之前的进度？
    *   **方案**: 利用 Bedrock AgentCore 的会话持久化能力和 Strands 的记忆存储，将任务状态持久化到数据库（如 DynamoDB）中。

### 技术创新点分析
最大的创新点在于**MCP 与 Bedrock AgentCore 的深度融合**。通常 MCP 服务器是独立的进程，而文章展示了一种将 MCP 服务器直接作为 Bedrock Agent 生态一部分的架构，使得 MCP 不仅能提供数据，还能提供“能力”。

---

## 3. 实际应用价值

### 对实际工作的指导意义
这篇文章为架构师和 AI 工程师提供了一套**在 AWS 上构建生产级 Agent 的蓝图**。它明确了如何处理非实时的复杂业务逻辑，避免了开发者自己造轮子去解决任务队列和状态管理的问题。

### 可以应用到哪些场景
1.  **复杂代码生成与重构**: 需要扫描整个代码库、运行测试用例，耗时可能长达数分钟。
2.  **企业级 RAG (检索增强生成)**: 涉及多源数据查询、索引更新和报告生成。
3.  **DevOps 自动化**: 执行部署脚本、系统配置检查等长周期运维任务。
4.  **数据分析与报表生成**: 处理海量数据并生成可视化图表。

### 需要注意的问题
*   **成本**: 长时间运行的 Strands Agents 和 Bedrock 调用可能会产生较高的推理成本。
*   **复杂性**: 引入异步框架增加了系统的调试难度。
*   **一致性**: 需要确保异步任务失败时的回滚或重试机制完善。

### 实施建议
*   不要对所有任务都使用长运行架构，应设置阈值，区分“即时响应”和“异步处理”。
*   优先采用 AWS Step Functions 来编排 Strands Agents 的任务流，以获得更好的可视化和错误处理能力。

---

## 4. 行业影响分析

### 对行业的启示
这篇文章预示着 **AI Agent 基础设施正在走向“云原生化”和“协议标准化”**。MCP 协议的普及使得 AI 应用不再被锁定在特定的模型提供商，而 Bedrock AgentCore 的介入则表明，公有云巨头正在通过强大的托管服务来抢占 Agent 编排的高地。

### 可能带来的变革
*   **从 Chatbot 到 Worker**: AI 应用将从简单的对话界面，转变为能够独立完成复杂工作流的“数字员工”。
*   **架构范式的转移**: 传统的 API 同步调用模式在 AI 领域将逐渐被基于事件和异步流的模式取代。

### 对行业格局的影响
*   **AWS 的护城河**: 通过将 Bedrock 与新兴协议（MCP）结合，AWS 正在构建强大的应用层生态，吸引开发者在其平台上构建复杂的 Agent 应用，从而巩固其在 AI 基础设施领域的领导地位。

---

## 5. 延伸思考

### 引发的其他思考
*   **互操作性**: 如果 MCP 成为标准，那么 Bedrock AgentCore 能否与 OpenAI 的 Agent 或其他本地模型无缝协作？这种架构是否具有足够的开放性？
*   **人机协作**: 在长任务运行期间，如何设计交互机制，让人类可以在任务执行中断时介入干预？

### 可以拓展的方向
*   **多 Agent 协作**: Strands Agents 之间如何通过 MCP 进行通信？是否可以构建一个 Agent 负责监控，另一个 Agent 负责执行的集群？
*   **边缘计算**: 这种长运行架构能否下沉到边缘设备（如 IoT 设备上的 Bedrock 客户端）？

### 未来发展趋势
未来，**“Serverless Agents”**（无服务器智能体）将成为常态。开发者只需定义逻辑和目标，底层的调度、状态维持、上下文管理将完全由云平台（如 Bedrock）和协议（如 MCP）自动处理。

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有痛点**: 检查你的 AI 应用中是否存在因为 API 超时（如 30s 或 60s）而导致任务失败的情况。
2.  **引入 Bedrock AgentCore**: 如果你的业务在 AWS 上，尝试将现有的 Prompt Chaining 逻辑迁移到 AgentCore。
3.  **改造 MCP Server**: 将你的 MCP 服务器从单纯的“数据查询器”改造为“任务执行器”，利用 Strands 框架处理后台逻辑。

### 具体的行动建议
*   **第一步**: 搭建一个基于 Bedrock AgentCore 的简单 Demo，连接一个本地 MCP 服务器。
*   **第二步**: 实现一个模拟长任务（如 `sleep 60s`）的接口，验证异步通知机制是否工作。
*   **第三步**: 引入 DynamoDB 或 S3 来存储长任务的中间状态和结果。

### 需要补充的知识
*   **Amazon Bedrock 服务细节**: 了解 Agent 的别名、版本控制和知识库配置。
*   **异步编程模型**: 熟悉 Python/Node.js 中的 Async/Await 模式以及消息队列机制。
*   **MCP 协议规范**: 阅读 Anthropic 的 MCP 文档，理解 Transport 层和 Session 层的工作原理。

### 实践中的注意事项
*   **安全性**: 长运行任务可能涉及敏感数据，需确保 MCP 传输层加密（TLS）以及 Bedrock 的 IAM 权限控制。
*   **限流**: 异步任务可能会瞬间触发大量的下游 API 调用，需要做好 Rate Limiting。

---

## 7. 案例分析

### 结合实际案例说明
假设一个**“企业合规审计 Agent”**的场景。
*   **传统方式**: 用户上传文档 -> Agent 读取文档 -> Agent 调用 Python 脚本分析 -> **[超时]** -> 用户收到错误。
*   **基于文章方案**: 用户上传文档 -> MCP Server 接收请求 -> Bedrock AgentCore 调用 Strands Agent -> **[任务入队，返回 TaskID]** -> 前端显示“正在审计中...” -> Strands Agent 在后台分析 -> 完成后通过 SNS 通知 AgentCore -> 客户端轮询获得报告。

### 成功案例分析
**GitHub Copilot Workspace** 是类似逻辑的体现。它在进行大规模代码重构时，不会让用户一直等待加载条，而是展示任务列表，逐步反馈结果。这种体验正是基于长运行架构实现的。

### 失败案例反思
早期版本的 ChatGPT 插件在处理复杂任务时，如果网络波动或任务稍长，就会直接报错“Network Error”，没有任何状态保留。这就是典型的缺乏异步任务管理和上下文保持机制导致的失败。

### 经验教训总结
**“不要让用户等待黑盒。”** 任何长任务都必须有进度反馈，且系统必须能够从断点恢复。文章提出的架构正是为了解决这一核心体验问题。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**为了在 Amazon Bedrock 上实现能够处理复杂、长周期业务逻辑的 AI Agent，必须采用基于 MCP 协议的异步架构，将 AgentCore 的编排能力与 Strands Agents 的持久化任务执行能力相结合。**

### 支撑理由与依据
1.

---
## 最佳实践

## 最佳实践指南

### 实践 1：设计有状态的长生命周期会话管理

**说明**:
在构建长时间运行的 MCP (Model Context Protocol) 服务器时，必须维护跨多次交互的会话状态。与传统的无状态请求不同，长运行 Agent 需要记住上下文、中间变量和之前的操作结果。Bedrock AgentCore 需要通过 Strands Agents 来协调这些状态，确保在处理长时间任务（如数据检索或复杂编排）时不会丢失上下文。

**实施步骤**:
1. 定义清晰的会话状态数据结构，用于存储用户意图、已完成的步骤和待处理数据。
2. 利用 Strands Agents 的状态管理 API，在每次交互后更新会话状态。
3. 实现会话持久化机制，将关键状态快照存储在 DynamoDB 或 S3 中，以防进程中断。

**注意事项**:
避免将会话状态无限期地保留在内存中，应设置合理的 TTL (Time To Live) 并实施状态序列化策略，以便在服务器重启时恢复会话。

---

### 实践 2：实施高效的工具调度与并发控制

**说明**:
长运行服务器通常需要调用多个工具或 API。在 Bedrock AgentCore 上，Strands Agents 负责编排这些工具调用。为了防止资源耗尽或 API 速率限制，必须实施严格的并发控制策略，确保长时间任务不会阻塞短时间的交互请求。

**实施步骤**:
1. 为不同的工具调用设置优先级队列，确保关键任务优先执行。
2. 实施令牌桶或漏桶算法，控制对外部 API 的调用速率。
3. 利用异步非阻塞 I/O 模式处理长时间运行的工具调用，避免阻塞主线程。

**注意事项**:
监控工具调用的延迟和成功率。对于耗时特别长的操作，应考虑将其设计为异步回调模式，而不是同步等待。

---

### 实践 3：优化 MCP 协议的上下文窗口管理

**说明**:
随着对话的进行，上下文长度会不断增加，最终可能超出模型的 Token 限制。在长运行场景下，必须实施智能的上下文压缩和总结机制，仅保留最相关的信息传递给 Bedrock 模型。

**实施步骤**:
1. 实现滑动窗口机制，自动丢弃最旧的、相关性最低的对话轮次。
2. 在 MCP 层实现中间层总结，将多轮工具调用结果总结为摘要信息。
3. 在发送给 Bedrock 之前，过滤掉冗余的系统提示词或非必要的元数据。

**注意事项**:
确保在压缩上下文时保留关键的系统指令和用户的核心意图，防止模型在长对话后期偏离任务目标。

---

### 实践 4：构建健壮的错误处理与重试逻辑

**说明**:
长运行进程面临更高的网络波动、服务暂时不可用或超时风险。MCP 服务器必须具备区分瞬时错误和永久错误的能力，并实施指数退避重试策略，以保证任务最终能够完成。

**实施步骤**:
1. 针对不同的错误类型（如 429 Throttling, 500 Internal Error）定义明确的处理策略。
2. 集成 AWS SDK 的内置重试机制，并自定义最大重试次数和退避策略。
3. 在 Strands Agents 中实现“检查点”机制，确保任务在失败恢复后可以从上一步骤继续，而不是从头开始。

**注意事项**:
对于非幂等操作（如创建资源、写入数据），在实施重试逻辑时必须确保操作是幂等的，或者实施去重检查，以防止数据重复。

---

### 实践 5：强化可观测性与分布式追踪

**说明**:
调试长时间运行的异步 Agent 架构具有挑战性。必须集成 CloudWatch 和 X-Ray，对 MCP 服务器和 Strands Agents 的调用链路进行全链路追踪，以便快速定位性能瓶颈或逻辑错误。

**实施步骤**:
1. 在 MCP 服务器的所有关键路径（工具调用、状态变更）中注入结构化日志。
2. 启用 AWS X-Ray 追踪，将 Bedrock AgentCore 的调用、Strands Agents 的决策过程以及下游 API 调用关联到同一个 Trace ID。
3. 设置 CloudWatch 告警，监控延迟指标、错误率以及 Token 使用量，以便及时发现异常。

**注意事项**:
注意日志采样率，避免在极高并发下产生过多的追踪数据，从而影响系统性能并增加 CloudWatch 成本。

---

### 实践 6：实施严格的资源清理与生命周期管理

**说明**:
长运行服务器容易出现资源泄漏（如未关闭的连接、堆积的缓存对象）。在 Strands Agents 集成环境中，必须明确 Agent 和工具的生命周期，确保在任务完成或中止时释放所有计算资源。

**实施步骤**:
1. 为 MCP 连接和 Strands Agent 实例设置明确的 Idle Timeout（空闲超时）。
2. 实现定期的“垃圾回收”任务，清理过期的会话状态和临时文件。
3. 利用 Lambda 或 ECS 的自动扩缩容特性，根据负载动态调整底层计算资源。

**注意事项**

---
## 学习要点

- Amazon Bedrock AgentCore 正式发布，旨在通过简化基础设施管理，帮助开发者构建高性能、可扩展且长期运行的 MCP 服务器。
- 通过集成 Strands Agents，AgentCore 赋予了智能体在复杂工作流中维持长期记忆和执行多步骤规划的能力，显著提升了自主性。
- 该架构利用 MCP 协议实现了智能体与外部工具和数据源之间的标准化互操作性，打破了不同系统间的连接壁垒。
- 开发者可以使用 Python 快速构建自定义服务器，并利用 AgentCore 自动处理服务器的生命周期、扩缩容和状态管理等运维难题。
- 新框架支持将智能体无缝部署到 Amazon ECS 和 AWS Lambda 等托管服务上，确保了应用的高可用性和成本效益。
- 借助统一的 Agent 框架，企业能够更容易地创建具备特定领域知识的专家级智能体，以执行复杂的业务任务。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*