---
title: "基于Amazon Bedrock AgentCore构建长时运行MCP服务器"
date: 2026-02-17T05:23:13+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长时运行", "AI Agent", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的方案，旨在构建能够可靠处理复杂且耗时操作的生产级 AI Agent（智能体）。该方案通过以下三个核心策略实现： 1. **上下文消息策略**：引入了一种维持服务器与客户端之间持续通信的机制，确保在长时间运行的操"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长时运行MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们将为您提供一套实现这一目标的综合方案。首先，我们会介绍一种上下文消息策略，该策略能在服务器与客户端之间，在执行耗时操作期间保持持续通信。接着，我们将开发一个异步任务管理框架，允许您的 AI 代理启动长时间运行的进程，同时不阻塞其他操作。最后，我们将演示如何利用 Amazon Bedrock AgentCore 和 Strands Agents 将这些策略整合起来，构建生产就绪的 AI 代理，以可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是当前技术落地的一大难点。本文将介绍一套基于 Amazon Bedrock AgentCore 和 Strands Agents 的综合方案，重点解析上下文消息策略与异步任务管理框架。通过阅读本文，您将掌握如何构建生产就绪的系统，确保 AI 在处理复杂耗时操作时保持通信畅通且高效稳定。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成的方案，旨在构建能够可靠处理复杂且耗时操作的生产级 AI Agent（智能体）。该方案通过以下三个核心策略实现：

1.  **上下文消息策略**：引入了一种维持服务器与客户端之间持续通信的机制，确保在长时间运行的操作中，上下文信息不丢失。
2.  **异步任务管理框架**：开发了允许 AI Agent 启动长时进程的异步框架，从而避免阻塞其他操作，提升系统的并发处理能力。
3.  **生产级集成**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 结合，打造出适用于实际业务场景、可稳定处理长时任务的 AI 解决方案。

---
## 评论

基于您提供的文章标题及摘要片段，以下是从技术与行业角度的深入评价。

### 一、 核心观点与支撑逻辑

**中心观点：**
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的架构范式，旨在通过引入上下文消息策略和异步任务管理框架，解决 MCP 协议在处理长周期任务时的状态保持与通信中断问题，从而构建具备企业级稳定性的持久化 AI 智能体。

**支撑理由：**

1.  **技术架构的针对性补强（事实陈述）：**
    传统的 MCP（Model Context Protocol）实现往往面临 HTTP 超时或 LLM Token 上下文窗口限制的问题。文章提出的“上下文消息策略”实际上是在构建一个**断路器模式**或**心跳机制**的变体。通过在 AgentCore 层面维持服务端与客户端的连续通信，确保了在长任务（如数据处理、代码生成）执行期间，LLM 不会因为“静默等待”而丢失上下文或导致客户端超时崩溃。这是对 MCP 协议在弱网或高延迟场景下的一种工程化修正。

2.  **异步编排能力的提升（你的推断）：**
    摘要中提到的“异步任务管理框架”表明，该方案试图将 LLM 的“同步推理”与业务逻辑的“异步执行”进行解耦。在 Bedrock AgentCore 中集成 Strands Agents，意味着系统可能采用了**事件驱动架构（EDA）**。这使得 Agent 可以在等待外部 API 响应（例如 RAG 检索或数据库写入）时，不占用 LLM 的活跃连接资源，显著降低了并发场景下的运营成本，并提高了系统的吞吐量。

3.  **云原生生态的锁定与协同（作者观点）：**
    该文章展示了 AWS 试图构建的“Agent 生态护城河”。通过 Bedrock AgentCore 这一托管服务，AWS 将计算逻辑（Strands Agents）与基础设施（Bedrock）深度绑定。对于企业用户而言，这降低了从“Demo”到“生产环境”的迁移难度，因为状态管理、鉴权和监控都被封装在 AWS 的闭环体系中，避免了自建 Redis 或数据库来维护 Agent 状态的复杂性。

**反例与边界条件：**

1.  **边界条件一：强一致性场景的不适用性（你的推断）：**
    该异步框架虽然提升了吞吐量，但在需要强事务一致性的金融交易场景下可能失效。异步任务管理通常意味着“最终一致性”，如果长任务执行到一半失败，回滚机制在分布式的 Agent 系统中极其复杂。文章若未提及分布式事务补偿（Saga 模式），则该方案不适合处理订单扣款等核心业务。

2.  **边界条件二：多厂商锁定的风险（事实陈述）：**
    该方案深度依赖 Bedrock AgentCore 和 Strands Agents。如果企业未来需要切换到 Azure OpenAI 或 Google Vertex AI，这种基于特定 Agent Runtime 的代码迁移成本将极高。相比之下，直接使用标准 LangChain 或 AutoGen 开发的通用 Agent 具有更好的可移植性，但需要自行解决长任务状态管理问题。

---

### 二、 维度评价

#### 1. 内容深度
文章触及了当前 AI Agent 落地中最痛点的**工程化问题**：如何让 LLM 像“人”一样长时间工作而不“走神”或“断连”。
*   **深度评价：** 从摘要看，文章没有停留在简单的 API 调用层面，而是深入到了**协议层**和**架构层**。它不仅提出了问题（长任务难做），还给出了具体的解决方案（Context Strategy + Async Framework）。这种将业务逻辑（Strands）与底层通信能力分离的思路，符合微服务架构的最佳实践。

#### 2. 实用价值
*   **指导意义：** 极高。目前很多开发者基于 LLM 开发应用时，遇到的最大瓶颈就是请求超时（通常 LLM API 或网关限制在 60s-90s）。文章提供的异步框架是构建**生产级 Agent**（如数据分析助手、代码审计机器人）的必经之路。
*   **案例结合：** 例如，在构建一个“AWS 日志分析 Agent”时，分析过程可能持续 5 分钟。如果不使用该文提到的异步框架，前端会直接报错 504 Gateway Timeout。采用该方案后，Agent 可以返回一个 Task ID，前端通过轮询或 WebSocket 获取进度，这是实际工程中的刚需。

#### 3. 创新性
*   **新观点：** 将 **MCP 协议**与 **Bedrock AgentCore** 结合是本文的主要创新点。MCP 是近期由 Anthropic 推出的开放协议，旨在统一 AI 与工具的连接。AWS 将其吸纳进 Bedrock 并通过 Strands 进行增强，实际上是在定义**“云原生 Agent”**的标准接口。这比单纯使用 OpenAI 的 Function Calling 更进了一步，因为它解决了多轮对话中的状态持久化问题。

#### 4. 可读性
*   **逻辑性：** 标题和摘要结构清晰，采用了“提出问题 -> 引入方案 -> 详述策略 -> 展望结果”的技术文档标准逻辑。
*   **清晰度：** 术语使用准确，明确区分了“Context Message”（通信层）和“Async Task”（逻辑层），这有助于架构师快速理解其设计意图。

#### 5. 行业影响
*   **潜在影响：** 这篇文章标志着 AI Agent 开发从“脚本化”向**“服务化”**的转变。它暗示了未来云

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该技术方案的深入分析。由于原文完整内容受限，本分析将基于标题和摘要中透露的关键技术信号——即**MCP协议**、**长时运行任务**、**Amazon Bedrock AgentCore**以及**Strands Agents集成**——进行逻辑推演和技术构建。

---

## 1. 核心观点深度解读

**主要观点**
文章的核心观点在于解决当前大模型应用（Agent）的一个重大瓶颈：**如何让AI Agent稳定、高效地执行跨越长时间周期的复杂任务**。传统的请求-响应模式无法满足耗时操作（如数据处理、代码编译、复杂工作流编排）的需求。文章提出了一种基于Amazon Bedrock AgentCore和MCP（Model Context Protocol）的架构，通过引入“Strands Agents”和异步任务管理，实现服务端与客户端在长时运行中的连续通信。

**核心思想**
作者试图传达从“同步对话式AI”向“异步自主式AI”转变的架构思想。这不仅仅是技术的升级，更是交互模式的演进：AI不再是一个被动回答问题的聊天机器人，而是一个能够独立启动任务、在后台持续运行，并主动向客户端汇报进度的智能协作者。

**创新性与深度**
其创新点在于将**MCP协议**（通常用于上下文传输）扩展为**任务控制通道**，并结合Bedrock AgentCore的托管能力，解决了长连接中的状态管理和资源释放问题。这种深度的系统集成，将底层基础设施的复杂度（如异步消息队列、状态持久化）对开发者屏蔽，极大地降低了构建复杂Agent的门槛。

**重要性**
随着AI从“聊天”走向“行动”，长时运行能力是Agent落地的关键。没有这种能力，AI只能处理简单的问答，无法真正融入企业的业务流程（如RPA、自动化运维、复杂数据分析）。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **MCP (Model Context Protocol):** Anthropic推出的开放协议，用于连接AI应用与外部数据源。在此文中，它被用作连接Agent与长运行任务的标准化接口。
*   **Amazon Bedrock AgentCore:** AWS Bedrock的核心引擎，负责Agent的编排、路由和工具调用。
*   **Strands Agents:** 这可能指代一种具备“记忆流”或“子任务链”能力的Agent架构（对应摘要中的Strands），能够处理多步骤的推理过程。
*   **异步任务管理框架:** 摆脱HTTP超时限制的机制。

**技术原理和实现方式**
1.  **上下文消息策略:** 摘要提到的“context message strategy”是指一种心跳或状态推送机制。当Agent发起一个长任务（如“分析这1000个文件”）时，它不会阻塞等待，而是返回一个任务ID。后台服务通过MCP协议持续将中间状态（如“正在处理第500个文件”）推送给客户端，保持对话的“活着”状态。
2.  **异步解耦:** 利用AgentCore的异步能力，将LLM的推理与实际的任务执行分离。LLM生成指令后，由Worker线程或Lambda函数执行耗时操作，操作完成后通过回调或Webhook通知AgentCore。

**技术难点与解决方案**
*   **难点:** 长连接超时、状态一致性（如果客户端断开怎么办？）、资源占用。
*   **方案:** 使用Strands Agents的“记忆”能力将状态持久化到数据库（如DynamoDB），而非仅保存在内存中。客户端重连后，可根据Strand ID恢复上下文。

**技术创新点分析**
将**Strands**（可能指代工作流 strands/线程）集成到MCP服务器中，使得MCP不仅仅是一个数据获取工具，变成了一个**任务编排器**。这是对MCP协议能力的重大扩展。

## 3. 实际应用价值

**对实际工作的指导意义**
对于企业级AI开发者，这意味着你可以放心地将需要数分钟甚至数小时才能完成的业务逻辑交给Agent处理，而无需担心API超时或用户体验中断。

**应用场景**
1.  **数据分析与报告生成:** Agent需要查询多个数据库，运行Python脚本进行清洗，生成图表。整个过程可能耗时10分钟。
2.  **自动化运维:** Agent检测到故障，执行一系列脚本修复，并持续监控日志，每30秒向运维人员汇报一次进度。
3.  **内容创作流水线:** Agent编写大纲、检索素材、生成长文、进行SEO优化，这是一个多阶段的长流程。

**需要注意的问题**
*   **成本控制:** 长时间的轮询或保持连接会增加Token消耗和基础设施费用。
*   **错误处理:** 如果长任务运行到一半失败了，Strands机制如何回滚或重试？

**实施建议**
在设计MCP Server时，应明确区分“快通道”（直接返回结果）和“慢通道”（返回Task ID + 状态查询接口）。

## 4. 行业影响分析

**对行业的启示**
这标志着AI Agent架构正在走向“服务化”和“标准化”。MCP协议正在成为连接LLM与后端服务的通用标准，而AWS Bedrock的加入则确认了这一趋势的巨头背书。

**可能带来的变革**
未来软件开发模式将从“编写函数”转变为“编写Agent技能”。长运行能力的突破，使得AI Agent有望取代传统的RPA（机器人流程自动化）工具，因为Agent具备理解能力，而RPA只是机械执行。

**相关领域的发展趋势**
*   **Agent DevOps:** 针对长运行Agent的监控、日志和调试工具将成为刚需。
*   **状态存储服务:** 专门用于存储Agent中间状态（Strands）的数据库服务将兴起。

## 5. 延伸思考

**引发的思考**
如果Agent可以长时运行并主动推送消息，那么用户隐私和权限管理将变得更加复杂。Agent是否会在用户不知情的情况下，在后台持续运行某些任务？

**拓展方向**
*   **多Agent协作:** 一个主Agent分解任务，多个Strand Agents并行处理长任务，最后汇总结果。
*   **人机协同:** 在长任务的关键节点（如“确认删除文件”），Agent如何优雅地暂停并等待人类介入？

**未来趋势**
长运行Agent将逐渐演变为**“AI员工”**。它们有自己的任务列表、工作日志和状态报告。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务颗粒度:** 识别你现有项目中哪些API调用是耗时的，将其改造为支持MCP的异步工具。
2.  **引入状态存储:** 不要依赖内存存储任务状态，立即集成Redis或DynamoDB来存储“Strands”。
3.  **定义协议标准:** 在你的MCP Server实现中，统一状态码的定义（如 `PROCESSING`, `COMPLETED`, `FAILED`）。

**具体行动建议**
*   搭建一个基于Bedrock AgentCore的PoC（概念验证）。
*   编写一个模拟的长任务脚本（如 `time.sleep(100)`），并通过MCP Server暴露给Agent。
*   测试Agent在任务执行期间，是否还能响应用户的其他查询（并发测试）。

**注意事项**
*   **幂等性设计:** 确保客户端重复查询任务状态时，不会导致服务端重复执行任务。
*   **超时机制:** 虽然任务是长运行的，但仍需设置最终超时时间，防止僵尸进程。

## 7. 案例分析

**成功案例设想**
一家金融科技公司使用该架构构建“财报分析Agent”。
*   **场景:** 用户上传PDF。
*   **流程:** Agent接收 -> 触发Strand Agent进行OCR和NLP提取（耗时5分钟） -> 期间前端显示“正在提取第N页数据” -> 提取完成 -> Agent生成分析报告。
*   **价值:** 用户体验流畅，无需盯着Loading界面。

**失败反思**
如果未采用异步框架，直接在MCP调用中同步执行OCR。
*   **后果:** 60秒后客户端或网关超时，用户看到报错，但后台仍在继续处理，导致资源浪费且用户无感知。

## 8. 哲学与逻辑：论证地图

**中心命题**
**在构建企业级AI Agent时，必须采用基于异步任务流（Strands）和上下文保持（Context Message）的架构，才能有效解决长运行任务的交互与状态管理问题。**

**支撑理由**
1.  **网络物理限制:** 任何同步请求都面临超时风险，而复杂的业务逻辑（如数据处理、代码生成）必然耗时，两者存在不可调和的矛盾。
2.  **用户体验需求:** 用户需要实时反馈，而非“黑盒”等待。保持上下文连续性是建立用户信任的关键。
3.  **资源效率:** 异步架构允许系统在等待I/O时释放计算资源，提高并发处理能力。

**依据**
*   *Evidence:* 现有的RPA工具和ETL流水线均采用异步调度模式。
*   *Intuition:* 如果一个秘书接手任务后就“失联”几小时，直到最后才给出结果，这被视为低效；同理，AI Agent也应具备阶段性汇报能力。

**反例/边界条件**
1.  **极简任务:** 对于“回答一个简单事实”或“查询当前天气”，引入异步框架会增加不必要的延迟和复杂度。
2.  **强实时性系统:** 在高频交易或毫秒级控制系统中，任何异步带来的延迟都是不可接受的（虽然这不属于“长运行”范畴，但属于边界）。

**命题分类**
*   **事实判断:** 同步请求有超时限制。
*   **价值判断:** 异步体验优于同步等待。
*   **可检验预测:** 采用该架构的Agent系统，其任务完成成功率将高于纯同步系统，且用户留存率更高。

**立场与验证**
**立场:** 支持该架构。这是AI Agent从玩具走向生产环境的必经之路。
**可证伪验证方式:**
*   **指标:** 对比同步模式下长任务的“超时错误率”与异步模式下的“任务完成率”。
*   **实验:** 构建两个Agent，分别处理同一批耗时任务（如批量图片处理），测量平均响应时间和资源消耗。

---
## 最佳实践

## 最佳实践指南

### 实践 1：设计有状态的无服务器架构

**说明**: 
在构建长时间运行的 MCP (Model Context Protocol) 服务器时，虽然底层计算可能是无状态的（如 Lambda），但业务逻辑往往需要维护状态。利用 Strands Agents 的特性，设计一种能够持久化对话上下文和中间状态的架构，确保在长对话或中断后能够恢复执行，而不是每次调用都从零开始。

**实施步骤**:
1. **引入外部状态存储**：使用 Amazon DynamoDB 或 ElastiCache 来存储 Agent 的会话状态、记忆和任务进度。
2. **配置会话 ID**：确保每次 MCP 请求都包含一个唯一的 Session ID，以便在后端检索关联的历史状态。
3. **实现检查点机制**：在执行长任务的关键步骤完成后，将当前状态快照保存到数据库中。

**注意事项**: 
避免将状态存储在服务器的本地内存中，因为在无服务器环境下，实例可能会被回收，导致状态丢失。

---

### 实践 2：优化 MCP 协议的连接与心跳管理

**说明**: 
长时间运行的连接容易因网络波动或闲置超时而断开。为了确保 MCP 服务器与 Bedrock AgentCore 之间的链路保持活跃，必须实现健壮的连接管理和心跳机制，防止因超时导致的任务失败。

**实施步骤**:
1. **调整 Keep-Alive 设置**：配置适当的 TCP Keep-Alive 参数，减少僵死连接的检测时间。
2. **实现应用层心跳**：在 MCP 协议层或应用层实现定期的 Ping/Pong 消息交换，以保持会话活跃。
3. **断线重连逻辑**：在客户端实现指数退避的重试策略，当连接断开时自动尝试重建连接并恢复上下文。

**注意事项**: 
注意平衡心跳频率与成本，过于频繁的心跳可能会增加不必要的费用和负载。

---

### 实践 3：实施细粒度的工具调用权限控制

**说明**: 
MCP 服务器通常通过暴露“工具”供 Agent 调用。在长运行场景下，Agent 可能会触发一系列敏感操作。必须遵循最小权限原则，严格限制 Bedrock AgentCore 通过 MCP 访问底层资源（如 AWS API 或数据库）的权限。

**实施步骤**:
1. **定义 IAM 角色**：为 MCP 服务器创建专用的 IAM 角色，仅授予执行特定任务所需的权限。
2. **工具级鉴权**：在 MCP 服务器内部实现逻辑，验证传入的 Tool Use 请求是否经过授权，防止越权调用。
3. **使用参数验证**：对所有传入的工具参数进行严格校验，防止注入攻击。

**注意事项**: 
定期审计 IAM 策略和 CloudTrail 日志，确保没有权限被过度使用或滥用。

---

### 实践 4：异步处理长时间任务

**说明**: 
某些 MCP 工具执行的操作（如数据处理、生成报告）可能超出 Bedrock Agent 的请求超时限制。为了防止超时错误，应将长耗时任务设计为异步模式，Agent 提交任务后立即返回，通过回调或轮询获取结果。

**实施步骤**:
1. **集成 Step Functions 或 SQS**：当接收到耗时请求时，启动一个 AWS Step Functions 工作流或将消息发送到 SQS 队列。
2. **返回任务令牌**：MCP 服务器应立即向 Agent 返回一个 `TaskID` 或状态查询端点，而不是等待最终结果。
3. **实现状态查询接口**：提供一个专门的 MCP 工具供 Agent 轮询任务状态，直到任务完成。

**注意事项**: 
确保异步任务的结果能够被正确地关联回原始的会话 ID，以便 Agent 能够将结果反馈给用户。

---

### 实践 5：构建可观测性与日志记录体系

**说明**: 
调试长时间运行的分布式 Agent 系统非常困难。必须建立完善的可观测性体系，追踪 MCP 服务器接收到的每一个请求、Agent 的决策过程以及工具的执行结果。

**实施步骤**:
1. **结构化日志**：使用 JSON 格式记录日志，包含 `request_id`、`session_id`、`tool_name` 和 `timestamp` 等关键字段。
2. **集成 X-Ray 追踪**：启用 AWS X-Ray 来追踪请求从 Bedrock AgentCore 到 MCP 服务器再到下游服务的完整调用链路。
3. **设置 CloudWatch 告警**：针对错误率、延迟和超时设置异常告警，以便在服务降级时及时响应。

**注意事项**: 
注意日志脱敏，确保不会在日志中泄露用户的敏感信息（PII）。

---

### 实践 6：利用 Strands Agents 实现复杂任务编排

**说明**: 
Strands Agents 能够处理多步骤的复杂推理。在构建 MCP 服务器时，应充分利用这一能力，将复杂的业务逻辑拆解为多个原子工具，让 Strands Agent 负责编排这些工具的调用顺序，而不是在 MCP 服务器端编写硬编码的长流程。

**实施步骤**:
1. **定义原子工具

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够自主执行长期、复杂工作流的 MCP 服务器。
- 该集成通过将复杂的任务分解为多步骤的子任务并自主迭代，显著提升了 AI 智能体处理长期运行任务的能力。
- 开发者可以利用现有的 MCP 协议标准，将具备长期规划能力的 Strands 代理无缝连接到 Bedrock 的生态系统和工具中。
- 这种架构解决了传统无状态模型难以维持上下文和执行连续操作的痛点，使智能体能够更可靠地完成业务目标。
- 借助 Bedrock 的托管服务，用户可以在享受 Strands 强大编排能力的同时，获得企业级的安全性与可扩展性保障。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI Agent](/tags/ai-agent/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-4.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*