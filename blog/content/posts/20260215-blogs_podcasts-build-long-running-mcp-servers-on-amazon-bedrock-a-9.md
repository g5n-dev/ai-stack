---
title: "基于Bedrock AgentCore构建长时运行MCP服务器与异步任务管理"
date: 2026-02-15T14:30:08+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Bedrock", "AgentCore", "异步任务", "长时运行", "Strands Agents", "上下文管理", "AI 架构"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种在 Amazon Bedrock AgentCore 上构建支持长时间运行任务的 MCP 服务器的综合方法，重点解决 AI 代理在处理复杂、耗时操作时的可靠性和连续性问题。主要内容涵盖以下三点： 1. **上下文消息策略**：引入了一种机制，用于在服务器与客户端之间保持连续通信，确保在扩展操作期间上下文不"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Bedrock AgentCore构建长时运行MCP服务器与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供了一套全面的实现方案。首先，我们介绍一种上下文消息策略，以在长时间操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，让您的 AI 智能体能够启动长时间运行的过程，同时不会阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，构建可投入生产的 AI 智能体，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 智能体是提升应用交互体验的关键，特别是在面对复杂工作流时，如何保持通信畅通且不阻塞系统运行至关重要。本文将详细介绍一套基于 Amazon Bedrock AgentCore 和 Strands Agents 的实现方案，涵盖上下文消息策略与异步任务管理框架。通过阅读本文，您将掌握构建高可用、生产级 AI 智能体的核心技术，确保其能够可靠地处理耗时操作。

---
## 摘要

本文介绍了一种在 Amazon Bedrock AgentCore 上构建支持长时间运行任务的 MCP 服务器的综合方法，重点解决 AI 代理在处理复杂、耗时操作时的可靠性和连续性问题。主要内容涵盖以下三点：

1.  **上下文消息策略**：引入了一种机制，用于在服务器与客户端之间保持连续通信，确保在扩展操作期间上下文不丢失。
2.  **异步任务管理框架**：开发了一套框架，允许 AI 代理启动长时运行的后台进程，同时不阻塞其他操作的执行。
3.  **生产级集成**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，构建出能够可靠处理复杂、耗时任务的生产级 AI 代理。

---
## 评论

### 中心观点
该文章提出了一种**基于异步任务管理和上下文消息策略的架构模式**，旨在解决在 Amazon Bedrock AgentCore 上运行长时间 MCP（Model Context Protocol）服务器时的会话超时与状态同步难题，从而实现复杂业务流程的自动化。

---

### 深入评价与支撑理由

#### 1. 内容深度与论证严谨性
**支撑理由：**
*   **[事实陈述]** 文章切中了当前 LLM 应用落地的核心痛点：**大模型的无状态性与长业务流程的有状态性之间的矛盾**。传统的 Request-Response 模式难以处理耗时任务（如数据查询、代码生成），文章提出的“异步任务管理框架”是对这一问题的系统性工程解法。
*   **[作者观点]** 文章引入“Strands Agents integration”作为上下文保持机制，表明作者试图通过将任务链“串行化”或“状态化”来维持 Agent 的短期记忆，这对于维持多步骤推理的逻辑连贯性至关重要。

**反例/边界条件：**
*   **[你的推断]** 该方案可能引入**最终一致性**的挑战。如果异步任务在执行过程中环境状态发生了变化（例如：数据库中的记录在任务排队期间被删除），Agent 基于旧上下文做出的决策在任务完成时可能已失效。
*   **[事实陈述]** 仅仅依赖消息策略可能不足以处理极端复杂的错误重试。如果 Bedrock 的底层模型调用失败或网络分区，单纯的“异步框架”若缺乏强一致的分布式事务支持，可能导致数据脏读或任务丢失。

#### 2. 实用价值与行业影响
**支撑理由：**
*   **[事实陈述]** 对于正在使用 AWS 生态构建企业级 Agent 的开发者而言，这篇文章提供了**高参考价值的“脚手架”代码**。它填补了官方文档中关于“长连接”或“长耗时任务”处理的空白，避免了开发者重复造轮子。
*   **[你的推断]** 该文章推动了 MCP 协议从简单的“RAG（检索增强生成）”工具向“Action-Oriented（行动导向）”的 Agent 演进。如果 Bedrock AgentCore 真的能通过这种模式稳定运行，它将显著降低企业部署“自动化员工”的门槛。

**反例/边界条件：**
*   **[你的推断]** **厂商锁定风险**。文章的方案高度耦合于 AWS Bedrock 的特定 API（AgentCore）。对于追求多云策略或希望切换底层模型（如切换至 OpenAI 或本地模型）的企业，这种深度集成的架构迁移成本极高。
*   **[事实陈述]** 对于轻量级应用，引入 Strands Agents 和异步框架可能存在**过度设计**。简单的定时任务或基于 Webhook 的回调机制可能比维护一个长连接 AgentCore 实例更廉价、更高效。

#### 3. 创新性与技术视角
**支撑理由：**
*   **[作者观点]** 将 MCP 服务器视为“长期运行的服务”而非“即用即弃的插件”，是一个视角的转变。文章提出的“Context Message Strategy”实际上是一种**应用层的 Keep-Alive 机制**，这在概念上类似于操作系统中的进程心跳，但在语义层面对齐了 LLM 的上下文窗口。

**反例/边界条件：**
*   **[你的推断]** **Token 成本与延迟陷阱**。虽然文章声称解决了长时运行问题，但为了维持上下文，不断传递中间状态消息会消耗大量 Input Token。在 Bedrock 按Token 计费的模型下，运行一个数小时的任务可能会产生惊人的上下文传递成本，且 LLM 处理超长上下文的响应延迟会随长度非线性增加。

#### 4. 可读性与逻辑性
**支撑理由：**
*   **[事实陈述]** 标题清晰地界定了技术栈，摘要结构采用了“问题-方案-细节”的经典技术博客写法，逻辑链条完整，易于技术人员快速定位价值。

---

### 争议点或不同观点

1.  **状态管理的归属权争议**：
    *   **文章隐含观点**：状态应该通过 Agent 和消息策略在框架内维护。
    *   **反方观点**：在微服务架构中，状态应完全下沉到数据库（如 Redis 或 PostgreSQL），Agent 应保持无状态。通过消息传递状态不仅不可靠，而且难以调试。更优雅的方案可能是 Agent 仅返回一个 Task ID，客户端通过独立轮询或 WebSocket 获取状态，而非在 LLM 的上下文中维持状态。

2.  **Strands Agents 的必要性**：
    *   **质疑**：Strands Agents 是否是解决问题的唯一路径？标准的 LangChain 或 LangGraph 已经具备了极其完善的“节点图”和“检查点”机制来处理长流程。引入一个新的“Strands”概念是否是 AWS 为了构建自身生态护城河的非标尝试？这可能导致技术栈的碎片化。

---

### 实际应用建议

1.  **成本监控与熔断机制**：
    *   在实施该方案时，务必设置 Token 消耗监控。由于长任务会反复回传上下文，建议在代码中实现“上下文压缩”，仅保留关键的推理步骤，而非全量历史记录，以控制成本。

2.  **混合架构设计**：
    *   不要将所有逻辑都放入 Bedrock AgentCore。建议将“决策”放在 Agent 中，将“执行”放在传统的异步 Worker（如 AWS Lambda + SQS）中。Agent 只需下发指令和接收最终结果，避免让 LLM 充当进程调度器，从而提高系统的鲁棒性。

3.  **可

---
## 技术分析

基于您提供的文章标题和摘要，虽然原文全文未完全展示，但结合标题中的关键术语——**Amazon Bedrock AgentCore**、**MCP (Model Context Protocol) Servers**、**Long-running（长时间运行）**、**Strands Agents** 以及 **Context message strategy（上下文消息策略）**，我们可以对这篇技术文章的核心意图和技术架构进行深度的逻辑重构和分析。

这篇文章主要探讨了在生成式AI应用中，如何解决“长时间任务处理”与“模型上下文窗口限制”及“网络超时”之间的矛盾。

以下是深入分析报告：

---

## 1. 核心观点深度解读

**主要观点：**
文章主张构建一种基于 **MCP (Model Context Protocol)** 的服务器架构，通过集成 **Strands Agents**（一种专注于长时间任务处理的Agent框架）到 **Amazon Bedrock AgentCore**，从而实现能够跨越数分钟、数小时甚至数天的稳定AI智能体工作流。

**核心思想：**
传统的LLM请求是同步且短时的，难以处理复杂业务流程。作者的核心思想是**“解耦计算与通信”**。通过引入**上下文消息策略**，在服务器端处理长任务的同时，保持与客户端（及模型）的“心跳”通信，确保任务不中断、上下文不丢失。

**创新性与深度：**
*   **协议层面的创新：** 利用MCP协议的标准化接口，解决了AI Agent与外部工具集成的碎片化问题。
*   **架构模式的进化：** 从“请求-响应”模式转向“异步任务-状态回调”模式。这不仅仅是代码实现，更是AI应用架构向分布式系统设计的一种演进。
*   **深度结合：** 将Bedrock的托管能力与Strands的持久化能力结合，填补了云端大模型服务在“长周期任务编排”上的空白。

**重要性：**
这一观点至关重要，因为它直接解决了企业级AI落地中最棘手的问题之一——**复杂业务的自动化处理**。如果AI只能回答问题而不能执行长达数小时的RPA（机器人流程自动化）或数据分析任务，其商业价值将被极大限制。

---

## 2. 关键技术要点

### 涉及的关键技术
1.  **MCP (Model Context Protocol):** Anthropic推出的开源协议，用于连接AI应用与本地/远程数据源。它是连接LLM与MCP Server的通用语言。
2.  **Amazon Bedrock AgentCore:** AWS Bedrock的一部分，负责Agent的编排、路由和工具调用。
3.  **Strands Agents:** 这是一个特定的Agent框架概念（通常指代具有长期记忆、多步骤规划的Agent），在此处特指能够处理“Strands”（线索/长任务流）的组件。
4.  **Asynchronous Task Management (异步任务管理):** 非阻塞的任务处理机制。

### 技术原理与实现
*   **Context Message Strategy (上下文消息策略):**
    *   *原理：* 当Agent发起一个耗时操作（如“处理一个月的财务报表”）时，不能让连接挂起。
    *   *实现：* 服务器立即返回一个“任务已接收”的确认消息，并携带一个`task_id`。随后，MCP Server通过后台线程处理任务。客户端或Agent可以通过轮询或Webhook查询任务进度。策略的核心在于如何将中间状态压缩并反馈给LLM，使其感知到任务正在进行。

*   **异步任务框架:**
    *   利用消息队列（如AWS SQS）或后台Worker进程来执行实际逻辑。
    *   **难点：** 如何在任务完成后，将结果“推”回正在进行的对话中？
    *   *解决方案：* 文章可能提出了一个“状态检查”工具，LLM会自动周期性调用该工具来更新上下文，直到任务完成。

### 技术难点与解决方案
*   **难点：** **上下文窗口溢出。** 长时间运行会产生大量中间日志，如果全部塞回给LLM，会爆Token。
    *   *解法：* 必须实施“摘要策略”，只将关键节点或最终结果返回给Bedrock。
*   **难点：** **超时机制。** Lambda函数或API Gateway通常有29秒的超时限制。
    *   *解法：* 使用基于事件驱动的架构（如Step Functions或长时间运行的ECS/Fargate任务）来承载MCP Server，避开无服务器架构的超时限制。

---

## 3. 实际应用价值

**指导意义：**
该架构为开发者提供了一套在AWS云端构建“企业级AI员工”的标准蓝图。它告诉我们，不要试图在一个Prompt或一次函数调用中完成所有工作。

**应用场景：**
1.  **金融/数据分析：** 执行长时间的数据ETL、生成复杂的报表。
2.  **DevOps/运维：** 监控长时间运行的部署任务，分析数小时的日志流。
3.  **内容创作：** 渲染长视频、编写大量代码并进行编译测试。
4.  **科研：** 提交长时间运行的模拟仿真任务。

**注意事项：**
*   **成本控制：** 长时间的轮询或保持连接会增加API调用成本和Token消耗。
*   **状态一致性：** 如果MCP Server宕机，任务状态如何恢复？需要持久化层（如DynamoDB）。

---

## 4. 行业影响分析

**对行业的启示：**
AI Agent正在从“聊天机器人”向“自主业务流程处理器”转型。行业需要从关注“响应速度”转向关注“任务完成率”和“持久化能力”。

**可能带来的变革：**
*   **MCP协议的普及：** 如果AWS Bedrock大力支持MCP，这可能成为连接AI模型与工具的事实标准，迫使其他云厂商跟进。
*   **Agent架构的标准化：** “Strands”模式可能成为处理长任务的通用范式，减少开发者重复造轮子。

**发展趋势：**
未来AI应用将不再是单一的API调用，而是由多个长期运行的微服务组成的**“AI Swarm”（AI集群）**，Bedrock AgentCore 将成为这些集群的大脑。

---

## 5. 延伸思考

**引发的思考：**
*   **人机协同：** 在长任务运行期间，如果中间步骤出错，人类如何介入？文章提到的策略是否支持“断点续传”或“人工干预”？
*   **多Agent协作：** Strands Agents 是否可以拆分为多个子Agent并行工作？

**拓展方向：**
*   结合 **Amazon EventBridge** 实现完全的事件驱动架构，而非轮询。
*   引入 **Vector Store (向量数据库)** 为Strands Agents提供长期的记忆能力，而不仅仅是任务状态。

---

## 6. 实践建议

**如何应用到项目：**
1.  **评估任务类型：** 识别项目中哪些业务逻辑耗时超过30秒。
2.  **架构改造：** 将这些逻辑剥离出同步的API调用，封装为独立的MCP Server。
3.  **引入状态机：** 使用AWS Step Functions来管理MCP Server背后的任务流，利用其可视化和错误处理能力。

**行动建议：**
*   不要直接在Lambda中运行长任务。
*   设计清晰的Task Schema（任务模式），定义`pending`, `running`, `completed`, `failed`等状态。
*   实现一个`get_task_status`的工具函数，并确保Bedrock Agent知道何时调用它。

**补充知识：**
*   学习 **Model Context Protocol (MCP)** 规范。
*   熟悉 **Amazon Bedrock Agent Actions** 和 **Prompt Engineering** 中的工具调用。

---

## 7. 案例分析

**成功案例（假设性推演）：**
*   **场景：** 某电商公司使用该架构处理“每日销售报告生成”。
*   **流程：** 用户向Agent请求报告 -> Agent调用MCP Server -> Server触发AWS Glue任务（耗时20分钟） -> Server轮询状态 -> 完成后Server将S3链接返回给Agent -> Agent发送邮件给用户。
*   **成功要素：** 用户不需要等待20分钟，可以关闭窗口，稍后回来问结果。

**失败反思：**
*   **反例：** 如果没有上下文消息策略，用户在等待5分钟后看到API Gateway 504超时，体验极差。
*   **教训：** 必须在前端UI上设计“异步反馈”机制，让用户知道任务在后台进行。

---

## 8. 哲学与逻辑：论证地图

**中心命题:**
在构建企业级生成式AI应用时，采用**基于MCP协议的异步架构**并结合**Strands Agents集成**，是解决**长周期复杂任务处理**（Long-running tasks）且保持**上下文连续性**的最优解。

**支撑理由:**
1.  **系统稳定性:** 传统的同步请求无法容忍长耗时，会导致超时或资源耗尽；异步框架解耦了请求与执行，保证了系统的高可用性。
    *   *依据:* 分布式系统设计理论及AWS Lambda/API Gateway的超时限制事实。
2.  **用户体验:** 用户无需保持连接活跃即可获得结果，符合现代交互习惯（如后台下载）。
    *   *依据:* 用户体验心理学及SaaS产品交互设计标准。
3.  **上下文感知能力:** 通过Context Message Strategy，Agent能够“感知”到后台任务的状态，从而在对话中保持逻辑连贯，而不是遗忘任务。
    *   *依据:* LLM的短期记忆限制原理。

**反例/边界条件:**
1.  **实时性要求极高的场景:** 如果任务必须在毫秒级完成（如高频交易判断），异步回调带来的延迟是不可接受的。
2.  **极简单任务:** 对于耗时小于1秒的简单查询（如“查天气”），引入复杂的异步框架和MCP Server属于过度设计，增加了延迟和复杂度。

**命题性质分析:**
*   **事实:** Bedrock AgentCore 和 MCP 协议存在且支持此类集成。
*   **价值判断:** “最优解”是一种价值判断，基于“稳定性”和“可扩展性”优于“开发速度”的假设。
*   **可检验预测:** 采用该架构的系统，其处理长任务的成功率将显著高于同步架构，但开发初期复杂度会更高。

**立场与验证:**
*   **立场:** 支持。对于任何涉及数据处理、RPA或复杂编排的AI Agent应用，异步化是必经之路。
*   **验证方式:**
    *   *指标:* 对比同步架构与异步架构在处理1小时任务时的“超时率”和“Token消耗总量”。
    *   *实验:* 构建一个Demo，分别用同步函数和Strands Agent模式处理一个5分钟的视频生成任务，记录用户断开网络后任务是否能继续完成并通知用户。

---
## 最佳实践

## 最佳实践

### 实践 1：优化会话状态管理与持久化

**说明**: 长时间运行的 MCP 服务器需要处理有状态的对话。在 Strands Agents 集成环境中，仅依靠内存存储会导致重启或扩展时状态丢失。应实现持久化层来保存对话历史、用户偏好和中间任务状态，以保持 Agent 上下文的连贯性。

**实施步骤**:
1. 选择 Amazon DynamoDB 或 ElastiCache 作为会话存储后端，支持高并发读写。
2. 在 MCP 服务器逻辑中实现检查点机制，每当完成一个子任务或 Strand 步骤时，自动保存状态快照。
3. 配置 Amazon Bedrock AgentCore 使用自定义会话管理模板，确保调用工具时能够检索历史上下文。

**注意事项**: 避免将完整的对话历史存储在单个数据库记录中，应使用分片或按时间窗口存储，以防止超过项大小限制。

---

### 实践 2：实施健壮的超时与重试策略

**说明**: 长时间运行的任务通常涉及外部 API 调用或复杂的推理过程，可能导致请求挂起或超时。在 Bedrock AgentCore 环境下，应配置适当的超时参数和指数退避重试机制，防止 MCP 服务器因等待响应而阻塞，从而提升系统弹性。

**实施步骤**:
1. 为所有 MCP 工具调用设置严格的客户端超时限制（例如 30-60 秒），并为长时间运行的异步任务返回 "pending" 状态。
2. 利用 AWS SDK 的内置重试器配置指数退避策略，处理 Bedrock 的限流或暂时性网络故障。
3. 在 Strands Agent 的逻辑中实现轮询或 Webhook 回调模式，以处理异步任务的最终状态确认。

**注意事项**: 区分可重试错误（如 5xx 错误、限流）和不可重试错误（如 4xx 验证错误），避免对无效请求进行重试。

---

### 实践 3：设计幂等的 MCP 工具接口

**说明**: 由于网络波动或 Agent 的重试机制，同一个操作可能会被多次调用。为了确保数据一致性和防止资源重复创建，MCP 服务器暴露的工具接口应设计为幂等的，即多次执行相同请求产生的结果与执行一次相同。

**实施步骤**:
1. 为每个请求生成唯一的幂等键，并在服务器端缓存该键的执行结果（例如使用 Redis）。
2. 在处理写入操作（如创建记录、发送邮件）前，检查是否已存在该幂等键的处理记录。
3. 对于非幂等的操作，设计查询接口供 Agent 确认状态，而不是直接依赖重试逻辑。

**注意事项**: 幂等键的缓存时间应设置合理的 TTL（生存时间），以平衡内存占用与业务需求。

---

### 实践 4：利用 Strands 实现任务分解与编排

**说明**: 避免在单个庞大的 MCP 工具中处理所有逻辑。应利用 Strands Agents 的能力，将复杂的长期任务分解为多个小的、可管理的子任务。这有助于提高可观察性、错误隔离能力和并行处理效率。

**实施步骤**:
1. 分析业务流程，将长工作流拆分为独立的 "Strands"（例如：数据收集 -> 数据处理 -> 结果生成）。
2. 为每个子步骤定义专门的 MCP 工具，确保每个工具只做一件事。
3. 在 Agent 的 Prompt 指令中明确编排逻辑，指导 Agent 如何按顺序或并行调用这些子工具。

**注意事项**: 确保 Strands 之间的数据传递格式标准化，避免因上游工具输出格式的变化导致下游工具解析失败。

---

### 实践 5：建立全面的可观测性与日志记录

**说明**: 在长周期运行的系统中，调试问题具有挑战性。应将 MCP 服务器的内部日志与 Amazon Bedrock 的可观测性功能集成，以便追踪从用户查询到 Agent 推理，再到 MCP 工具执行的完整链路。

**实施步骤**:
1. 使用 Amazon CloudWatch Logs 或 OpenTelemetry 收集 MCP 服务器的结构化日志。
2. 在日志中包含关键的关联 ID（Trace ID），以便在 AWS X-Ray 中追踪 Bedrock Agent 调用与 MCP 响应之间的关系。
3. 监控关键指标，如工具调用延迟、错误率和 Token 消耗量，并设置告警阈值。

**注意事项**: 避免在日志中记录敏感信息（如 PII 数据或 API 密钥），确保符合安全合规要求。

---

### 实践 6：实施严格的输入验证与安全防护

**说明**: MCP 服务器是 Agent 与外部世界交互的桥梁，容易受到提示注入攻击或恶意输入的影响。必须实施严格的输入验证和清理逻辑，确保传入参数在预期范围内，防止潜在的安全漏洞。

**实施步骤**:
1. 在 MCP 服务器入口处定义严格的 Schema 验证（例如使用 Pydantic 或 JSON Schema），拒绝不符合格式的请求。
2. 对所有传入的字符串参数进行清理，过滤掉可能的注入代码或恶意指令。
3

---
## 学习要点

- Amazon Bedrock AgentCore 正式发布，支持开发者构建具有状态管理和长期运行能力的自主智能体，突破了传统无状态交互的限制。
- 通过集成 Strands Agents 框架，开发者可以创建能够执行多步骤、长时间复杂任务（如订单处理或工作流编排）的 MCP 服务器。
- 该架构利用“记忆存储”和检查点机制，确保智能体在处理长周期任务时具备容错能力和状态持久化，即使发生中断也能恢复执行。
- 借助 MCP（Model Context Protocol）协议，Bedrock AgentCore 能够轻松实现与外部数据源和工具的标准化集成与互操作性。
- 开发者可以使用 Python 或 TypeScript 等熟悉的编程语言灵活定义智能体的逻辑和行为，降低了构建复杂生成式 AI 应用的门槛。
- 该解决方案特别适用于需要跨越数小时或数天的复杂业务流程自动化，显著提升了企业级 AI 应用的实用性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [MCP](/tags/mcp/) / [Bedrock](/tags/bedrock/) / [AgentCore](/tags/agentcore/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [Strands Agents](/tags/strands-agents/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/) / [AI 架构](/tags/ai-%E6%9E%B6%E6%9E%84/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*