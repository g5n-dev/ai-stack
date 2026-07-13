---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理"
date: 2026-02-13T23:30:43+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长时运行", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种在 Amazon Bedrock AgentCore 上结合 Strands Agents 构建长时间运行 MCP 服务器的综合方法。主要内容如下： 1. **上下文消息策略**：引入了一种策略，用于在服务器与客户端之间进行长时间的扩展操作时，保持连续的通信。 2. **异步任务管理框架**：开发了一个框"
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

在本文中，我们为您提供了一套实现这一目标的全面方法。首先，我们介绍一种上下文消息策略，以在长时间操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的进程，而不会阻塞其他操作。最后，我们将演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合使用，从而构建生产级 AI 代理，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够稳定处理长周期任务的 AI 代理是当前技术落地的一大难点。本文将深入探讨如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成特性，解决上下文保持与异步任务管理的问题。通过具体的实现策略，我们将向您展示如何构建生产级系统，确保 AI 在执行复杂操作时既不阻塞通信，又能维持高可靠性。

---
## 摘要

本文介绍了一种在 Amazon Bedrock AgentCore 上结合 Strands Agents 构建长时间运行 MCP 服务器的综合方法。主要内容如下：

1.  **上下文消息策略**：引入了一种策略，用于在服务器与客户端之间进行长时间的扩展操作时，保持连续的通信。
2.  **异步任务管理框架**：开发了一个框架，允许 AI 代理启动长时间运行的进程，同时不会阻塞其他操作。
3.  **生产级解决方案**：展示了如何将这些策略与 Amazon Bedrock AgentCore 及 Strands Agents 集成，从而构建出能够可靠、高效地处理复杂且耗时任务的生产级 AI 代理。

---
## 评论

### 中心观点
该文章提出了一种基于 Amazon Bedrock AgentCore 的技术架构，旨在通过引入“上下文消息策略”与“异步任务管理框架”，解决模型上下文协议（MCP）服务器在处理长周期任务时的状态持久化与交互连续性问题，从而突破传统无状态请求-响应模式在复杂 Agent 工作流中的限制。

### 支撑理由与评价

#### 1. 内容深度：架构设计的严谨性与针对性
*   **事实陈述**：文章针对 MCP（Model Context Protocol）服务器通常面临的“长任务阻塞”痛点，提出了“上下文消息策略”。这意味着系统不再是一次性处理请求，而是维护一个会话流。
*   **你的推断**：这表明文章深入到了 AI Agent 工程化的核心难点——**状态管理**。传统的 RESTful 或短连接 RPC 模式难以适应 AI 生成内容（AIGC）的不确定性和耗时性。文章提出的架构可能涉及将 Bedrock 的异步调用能力与 MCP 的传输层进行深度绑定，确保在 LLM 推理期间或外部工具执行期间，客户端连接不会因为超时而断开，从而保证了用户体验的连贯性。

#### 2. 实用价值：填补了 Bedrock 生态的工程化空白
*   **事实陈述**：AWS Bedrock 虽然提供了强大的基础模型，但在构建复杂应用时，开发者往往需要自己处理 Agent 的记忆和任务队列。
*   **作者观点**：通过构建“异步任务管理框架”，开发者可以将长耗时的操作（如数据库查询、代码生成、文件处理）从主线程剥离。
*   **结合实际案例**：在企业级 RAG（检索增强生成）应用中，查询向量数据库并重排序往往需要数秒。如果使用同步模式，前端会一直卡顿。该文章提出的框架允许后端立即返回一个任务 ID，通过 WebSocket 或 SSE（Server-Sent Events）持续推送进度，这对于生产级应用至关重要。

#### 3. 创新性：Strands Agents 集成的范式转变
*   **事实陈述**：文章提到了“Strands Agents integration”。
*   **你的推断**：这里的“Strands”很可能指的是一种能够处理多步骤、有依赖关系任务的编排机制，或者是 AWS 特定的某种长时运行逻辑模式。将这种机制与 MCP 结合，是一种**混合架构**的创新尝试。它试图将 MCP 协议从简单的“工具调用”提升为“工作流编排”的载体。这不仅是技术实现，更是对 MCP 协议边界的一种拓展探索。

### 反例与边界条件

尽管文章提出了看似完善的解决方案，但在实际落地中存在明显的边界条件和潜在反例：

1.  **反例一：状态一致性的灾难风险**
    *   **边界条件**：在分布式系统中，长运行任务意味着更高的故障概率。
    *   **你的推断**：文章虽然强调了“异步管理”，但可能未充分讨论**幂等性**和**故障恢复**。如果 Bedrock AgentCore 在任务执行到 80% 时宕机，客户端重连后能否自动恢复上下文？如果该框架依赖内存存储上下文而非外部数据库（如 DynamoDB），那么服务重启将导致所有长任务丢失，这在生产环境是不可接受的。

2.  **反例二：成本与延迟的权衡**
    *   **边界条件**：高频轮询或保持长连接。
    *   **你的推断**：为了维持“连续通信”，系统可能需要维持大量的 TCP 长连接或频繁轮询。在 Bedrock 这种 Serverless 架构中，这可能会导致极大的成本开销（如果按连接数或调用次数计费）或冷启动延迟。对于简单的、毫秒级的工具调用，引入这种复杂的异步框架可能是“杀鸡用牛刀”，反而增加了平均延迟。

### 事实与观点标注

*   **[事实陈述]** 文章介绍了在 Amazon Bedrock AgentCore 上构建 MCP 服务器的具体方法。
*   **[事实陈述]** 提到了“Context message strategy”和“Asynchronous task management framework”两个核心组件。
*   **[作者观点]** 该方法能够有效地实现服务器与客户端在扩展操作期间的连续通信。
*   **[你的推断]** 该方案旨在解决 LLM Agent 在处理复杂工作流时面临的“超时”和“无状态”限制，试图模仿 LangChain 等框架中的 LangSmith 功能，但将其深度集成在 AWS 基础设施中。

### 可验证的检查方式

为了验证该文章所述架构的有效性，建议进行以下检查：

1.  **压力测试指标**：
    *   **并发长连接数**：测试 Bedrock AgentCore 在维持 1000+ 个长运行 MCP 连接时的资源消耗与延迟表现。
    *   **超时率**：模拟执行 60 秒以上的任务，观察客户端连接是否会因为 Lambda（假设底层计算单元）或网络层的超时配置而断开。

2.  **故障恢复实验**：
    *   **中断测试**：在异步任务执行过程中手动中断 AgentCore 进程或触发底层计算单元重启，验证任务恢复后上下文是否保留，以及是否会出现重复执行。

3.  **协议兼容性观察**：
    *   **MCP 协议抓包**：观察网络层传输的数据包，验证“Context message”是遵循标准 MCP 协议扩展，还是使用了 AWS 私有的信令通道。如果是私有协议，则可能导致供应商锁定。

4.  **成本分析窗口**：
    *   **计费监控**：对比使用该异步框架与直接调用 Bedrock API 在相同任务

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要，结合 Amazon Bedrock、MCP (Model Context Protocol) 以及 Agentic Workflow 的行业背景，以下是对该文章核心观点和技术要点的深入分析。

---

# 深度分析：构建基于 Amazon Bedrock AgentCore 的长时间运行 MCP 服务器

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心在于解决当前 AI Agent（智能体）在处理复杂、耗时任务时的“同步阻塞”瓶颈。作者提出了一种基于 **Amazon Bedrock AgentCore** 和 **Strands Agents** 集成的架构方案，旨在将传统的“请求-响应”模式转变为“异步任务流”模式，从而实现能够稳定运行长时间任务（如数据研究、代码生成、复杂工作流编排）的 MCP 服务器。

**作者想要传达的核心思想**
AI 的未来不仅仅是单次问答，而是具备持久记忆和连续执行能力的智能体。通过引入 **Context Message Strategy（上下文消息策略）** 和 **Asynchronous Task Management（异步任务管理）**，开发者可以构建出在后台持续运行、能够主动向客户端推送进度的智能系统，而不是让用户在等待中面对超时的错误。

**观点的创新性和深度**
该观点的创新性在于它结合了两个前沿技术：**MCP（模型上下文协议）** 的标准化接口能力与 **Amazon Bedrock AgentCore** 的托管编排能力。它深入探讨了在无状态（Stateless）的 LLM 基础设施之上，如何通过“Strands”（可能指代一种持久化的执行线索或会话流技术）来维持状态。这不仅是技术实现的问题，更是从“对话式交互”向“程序化交互”的范式转移。

**为什么这个观点重要**
随着 AI 从 Copilot（副驾驶）向 Agent（自主代理）演进，任务复杂度呈指数级上升。传统的 API 调用往往在 30-60 秒后超时，无法满足实际业务需求（例如生成一份 50 页的报告或分析数百万行数据）。该文章提出的方案是实现复杂 AI 自动化落地的关键基础设施，解决了 AI 落地“最后一公里”的稳定性问题。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **MCP (Model Context Protocol):** Anthropic 推出的开放协议，用于连接 AI 应用与数据源。文章将其作为服务端暴露能力的标准接口。
*   **Amazon Bedrock AgentCore:** AWS 提供的用于构建和管理 Agent 的底层服务，提供编排、记忆和工具调用能力。
*   **Strands Agents:** 这是文章中的关键技术概念，推测指代一种支持长时间运行、多步骤推理的 Agent 架构（可能涉及 AWS 的多步骤编排或特定的会话持久化技术）。
*   **异步任务队列:** 用于解耦客户端请求与服务端执行。

**技术原理和实现方式**
1.  **Context Message Strategy (上下文消息策略):** 为了保持通信连续性，系统不再是一次性返回最终答案，而是通过流式传输或中间状态回调，定期向客户端发送“心跳”或“进度更新”。这要求客户端能够处理部分响应，并维持一个开放的会话通道。
2.  **异步任务管理框架:** 当 Agent 接收到一个长时间任务（如“分析 Q3 财报”），Bedrock AgentCore 会立即返回一个 `TaskID`，并将任务放入后台队列。Agent 在后台分解任务、调用工具、处理数据。客户端通过 `TaskID` 轮询或通过 WebSocket 接收更新，而不是保持 HTTP 连接不释放。

**技术难点和解决方案**
*   **难点:** LLM 本质是无状态的，且 API 有严格的 Token 限制和超时限制。
*   **解决方案:** 利用 Bedrock AgentCore 的持久化存储能力保存会话历史，利用 Strands 架构将长任务拆解为多个子步骤，每个步骤独立执行并保存中间状态，实现“断点续传”式的任务处理。

**技术创新点分析**
最大的创新点在于将 **MCP 的轻量级连接特性** 与 **Bedrock 的企业级编排能力** 结合。通常 MCP 用于简单的数据查询，而该方案将其扩展为复杂的任务执行终端。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为开发者提供了一种标准模式，用于构建生产级的 AI 应用。它告诉我们：不要试图在一个 LLM Prompt 中完成所有工作，而应该设计“开始-监控-获取结果”的异步交互流程。

**可以应用到哪些场景**
1.  **RAG (检索增强生成) 深度分析:** 对海量文档库进行深度总结和交叉分析，耗时可能长达数分钟。
2.  **代码生成与重构:** 对大型代码库进行理解和重构，需要多次编译和测试循环。
3.  **数据科学工作流:** 自动化数据清洗、特征工程和模型训练的脚本生成。
4.  **企业级自动化:** 涉及多个 API 调用的复杂业务流程（如自动处理报销单）。

**需要注意的问题**
*   **成本控制:** 长时间运行意味着大量的 Token 消耗和 Bedrock 调用次数，必须设置预算和中断机制。
*   **状态一致性:** 确保在任务失败时能够回滚或恢复，避免数据不一致。

**实施建议**
在实施时，应优先构建完善的监控面板。因为用户无法直接看到后台的 Agent 在做什么，可视化的任务进度条和日志输出是提升用户体验的关键。

## 4. 行业影响分析

**对行业的启示**
该文章预示着 AI 基础设施正在从“模型中心”向“任务中心”转变。云厂商（如 AWS）正在构建更完善的中间件，让开发者无需关注底层的模型连接细节，只需关注任务逻辑的定义。

**可能带来的变革**
这将极大地推动 **"Agentic Applications"（代理式应用）** 的爆发。企业不再满足于 ChatBot，而是开始部署能够独立完成复杂工作的数字员工。

**对行业格局的影响**
MCP 协议的普及可能会打破单一生态的锁定。如果 AWS Bedrock 能完美支持 MCP，意味着使用 Claude（Anthropic）或 Llama（Meta）作为核心模型的应用，可以无缝接入 AWS 的基础设施，促进了模型层与基础设施层的解耦与竞争。

## 5. 延伸思考

**引发的其他思考**
*   **人机协作的新模式:** 在长时间任务中，何时需要人类介入？文章提到的“Context Message”是否应该包含“请求确认”的机制？
*   **多租户隔离:** 在 Bedrock 上运行大量长时间任务时，如何确保不同租户的数据安全和资源隔离？

**可以拓展的方向**
*   **多 Agent 协作:** 扩展该架构，不仅是一个 MCP Server，而是多个 Server 之间通过 Bedrock 互相通信，形成 Agent Society（智能体社会）。
*   **边缘计算结合:** 将轻量级的 Strands 部署在边缘，将重型计算放在 Bedrock。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有痛点:** 检查你现有的 AI 应用是否经常遇到 504 Gateway Timeout 错误，或者用户抱怨等待时间过长。
2.  **引入异步层:** 在现有的 LLM 调用层之上，引入消息队列（如 SQS）和任务状态表（DynamoDB）。
3.  **改造 MCP Server:** 如果已在使用 MCP，修改 Server 端的 Tool 定义，使其返回 `async_result_id` 而非直接结果，并新增一个 `check_status` 工具供客户端轮询。

**具体的行动建议**
*   阅读 Amazon Bedrock AgentCore 的官方文档，特别是关于“Orchestration”和“Memory”的部分。
*   在本地搭建一个简单的 MCP Server，尝试模拟一个耗时 10 秒的任务，练习如何处理异步状态返回。

**实践中的注意事项**
*   **超时设置:** 即使是异步轮询，客户端也不能无限等待，需要设置合理的超时和重试策略。
*   **错误处理:** 必须处理 Agent 在后台崩溃的情况，并向用户展示友好的错误信息，而不是抛出堆栈跟踪。

## 7. 案例分析

**结合实际案例说明**
假设我们要构建一个 **“法律合同审查 Agent”**。
*   **传统模式:** 用户上传 100 页合同，点击“审查”。系统转圈 2 分钟后报错“Request Timeout”。
*   **基于文章方案的模式:**
    1.  用户上传合同。
   2.  Bedrock Agent 接收任务，创建 Strands 会话，立即返回：“任务已接收，ID: 12345，正在后台处理”。
   3.  Agent 逐页阅读，每读完 10 页，通过 Context Message 更新进度：“已审查 30%... 发现 2 个潜在风险点”。
   4.  用户可以看到实时进度条。
   5.  2 分钟后任务完成，用户点击查看详细报告。

**成功案例分析**
类似 **GitHub Copilot Workspace** 或 **Devin** 的实现逻辑。它们都不是一次性生成代码，而是展示详细的“思考”和“执行”步骤，让用户感知到 Agent 正在长时间工作。

**失败案例反思**
如果忽视异步管理，仅仅通过增加 Lambda 超时时间（如从 1 分钟改到 15 分钟）来解决问题，会导致成本高昂且极易因网络波动导致任务全盘失败，用户体验极差。

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级 AI 应用时，采用基于 **Amazon Bedrock AgentCore** 和 **Strands** 的 **异步 MCP 服务器架构**，是实现复杂、长时间运行任务的唯一可行且具备扩展性的方案。

**支撑理由与依据**
1.  **理由 1: 用户体验 (UX) 的必要性。**
    *   **依据:** 心理学研究表明，超过 10 秒的等待若无反馈，用户焦虑感会急剧上升。同步阻塞模式无法提供反馈。
2.  **理由 2: 技术稳定性的物理限制。**
    *   **依据:** HTTP 协议和底层 TCP 连接在网络波动下难以维持数分钟不中断；云函数（Lambda）有最大执行时长限制（通常 15 分钟）。
3.  **理由 3: 复杂任务的认知负荷。**
    *   **依据:** Chain-of-Thought (CoT) 推理需要多步验证，单次 Prompt 无法容纳所有上下文，必须分步执行。

**反例或边界条件**
1.  **反例 1 (简单查询场景):** 对于“查一下天气”或“翻译这句话”这类毫秒级完成的简单任务，引入异步架构会带来不必要的延迟和系统复杂度（过度设计）。
2.  **边界条件 (强实时性要求):** 某些高频交易场景可能需要极低延迟的同步响应，异步轮询可能导致延迟不可接受（需用 WebSocket 替代）。

**事实与价值判断**
*   **事实:** Bedrock 支持 AgentCore；MCP 是开放协议；LLM 生成需要时间。
*   **价值判断:** “长时间运行”是 AI Agent 的核心价值所在（即 Agent 应该像人类一样花时间工作）。
*   **可检验预测:** 采用该架构的应用，其任务完成成功率将显著高于同步应用，且用户流失率会降低。

**立场与验证方式**
我支持该文章提出的异步架构方向。
**可证伪验证

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 Strands Agents 的会话状态管理

**说明**: 长时间运行的 MCP 服务器需要维护跨请求的上下文状态。利用 Strands Agents 集成时，不应将所有历史记录存储在内存中，而应利用 Bedrock AgentCore 的持久化存储功能或外部状态存储（如 DynamoDB）来保存会话令牌和中间结果，以防止服务器重启或扩展导致状态丢失。

**实施步骤**:
1. 配置 Bedrock AgentCore 以使用外部状态存储后端。
2. 在 MCP 服务器逻辑中，定义最小必要的会话状态模式。
3. 实现 Strands Agents 的回调机制，在关键步骤将状态快照写入存储。
4. 设置合理的 TTL（生存时间）以清理过期的会话数据。

**注意事项**: 避免在会话状态中存储大型二进制对象，仅保留引用 ID 或必要的元数据。

---

### 实践 2：实施严格的超时与重试策略

**说明**: 长时间运行的任务可能会遇到网络波动或 LLM 响应延迟。为了防止 MCP 服务器连接挂起，必须在 Strands Agents 调用层和底层网络层实施多层超时控制，并结合指数退避算法进行重试，以确保系统的弹性。

**实施步骤**:
1. 为 MCP 工具调用设置明确的执行超时限制。
2. 配置 Bedrock AgentCore 的客户端超时参数。
3. 实现指数退避重试逻辑，特别是针对 Bedrock API 的限流错误。
4. 为长时间运行的异步任务实现“轮询”或“回调”模式，而不是保持连接打开。

**注意事项**: 区分“可重试”错误（如 5xx 错误、限流）和“不可重试”错误（如认证失败、参数错误），避免无意义的重试消耗配额。

---

### 实践 3：设计幂等的 MCP 工具接口

**说明**: 在分布式环境中，网络中断可能导致客户端不确定请求是否成功。如果 MCP 服务器暴露的工具（Tools）不是幂等的，重复执行可能导致数据重复或损坏。确保所有通过 Strands Agents 触发的操作（如写入数据库、调用 API）都支持幂等性。

**实施步骤**:
1. 为每个需要修改状态的操作设计幂等键。
2. 在处理请求前检查是否已处理过该 Idempotency Key。
3. 确保业务逻辑支持“至少一次”交付语义而不产生副作用。
4. 在 MCP Schema 文档中明确标记工具的幂等特性。

**注意事项**: 对于非幂等的操作，应在文档中明确警告，并建议客户端通过上层逻辑进行控制。

---

### 实践 4：结构化日志记录与可观测性集成

**说明**: 长时间运行的服务器难以调试。必须将 Strands Agents 的思维链和 MCP 服务器的内部操作日志通过 Amazon CloudWatch 进行集中管理。日志应包含请求 ID、用户会话 ID 和时间戳，以便追踪复杂的 Agent 行为。

**实施步骤**:
1. 安装并配置 AWS CloudWatch Logs 代理或 SDK。
2. 在 MCP 服务器代码中注入结构化日志（JSON 格式），包含 `trace_id` 和 `session_id`。
3. 利用 AWS X-Ray 进行分布式追踪，关联 Bedrock AgentCore 和 MCP 服务的调用链。
4. 设置针对特定错误代码（如 ToolExecutionError）的告警指标。

**注意事项**: 注意日志脱敏，确保不将 PII（个人身份信息）或敏感密钥打印到日志中。

---

### 实践 5：利用并发控制管理资源消耗

**说明**: Bedrock AgentCore 允许并发请求，但底层的 MCP 服务器可能有资源限制（如数据库连接数、第三方 API 速率限制）。必须实施信号量或队列机制来限制并发处理请求数量，防止后端过载。

**实施步骤**:
1. 评估 MCP 服务器后端依赖的最大并发承载能力。
2. 在服务器入口处实现并发限制中间件。
3. 对于 I/O 密集型任务，使用异步编程模型（如 Python asyncio）提高吞吐量。
4. 配置 Auto Scaling 策略，基于 CPU 或队列长度动态调整实例数量。

**注意事项**: 监控“拒绝”的请求数量，如果频繁触发并发限制，考虑垂直扩展或优化数据库查询。

---

### 实践 6：明确 MCP 工具的输入输出 Schema 定义

**说明**: Strands Agents 依赖准确的工具描述来生成正确的参数。模糊或不正确的 JSON Schema 会导致 Agent 调用失败或陷入循环。最佳实践是严格定义输入参数的类型、格式和必填字段，并在输出中提供标准化的错误结构。

**实施步骤**:
1. 使用严格的 JSON Schema Draft 7 定义 MCP 工具的输入。
2. 为枚举值提供清晰的描述，帮助 LLM 理解选项。
3. 定义统一的错误响应格式，包含 `code` 和 `retryable` 字段。
4. 在开发阶段使用 Bedrock 的 Playground 测试

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够长时间运行并具备状态记忆能力的 MCP 服务器。
- 通过将 MCP 协议与 Bedrock AgentCore 结合，用户可以轻松连接外部数据源和工具，显著扩展了 Agentic AI 的应用边界。
- 该架构解决了传统无状态模型无法处理复杂、多步骤工作流的痛点，使智能体能够维持跨越多个交互轮次的上下文。
- 开发者可以利用 Strands 框架管理智能体的生命周期和状态，从而简化了长时间运行任务的编排与维护流程。
- 这一集成方案不仅提升了 AI 应用在自动化工作流中的实用性，还增强了其在处理复杂业务逻辑时的可靠性与连贯性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*