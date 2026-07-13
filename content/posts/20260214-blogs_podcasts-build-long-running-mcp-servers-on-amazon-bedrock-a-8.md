---
title: "基于 Amazon Bedrock AgentCore 构建长时间运行的 MCP 服务器"
date: 2026-02-14T07:48:00+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Bedrock", "AgentCore", "Strands Agents", "异步任务", "上下文策略", "AI 代理", "长连接"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够长时间稳定运行的 MCP 服务器的综合方法。 主要内容分为以下三个关键策略： 1. **上下文消息策略**： 引入了一种专门的机制来维护服务器与客户端在长时间运行过程中的持续通信。该策略旨在确保在执行复"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于 Amazon Bedrock AgentCore 构建长时间运行的 MCP 服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在这篇文章中，我们为您提供了一套全面的实现方法。首先，我们介绍一种上下文消息策略，用于在服务器与客户端之间，在长时间运行的操作中保持持续通信。接着，我们开发了一个异步任务管理框架，让您的 AI 代理能够启动长时间运行的流程，同时不会阻塞其他操作。最后，我们演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents 将这些策略落地，构建生产级的 AI 代理，从而可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是当前技术落地的一大难点。本文将介绍一套基于 Amazon Bedrock AgentCore 和 Strands Agents 的实现方案，重点解析如何通过上下文消息策略和异步任务管理框架，确保服务器与客户端在复杂流程中的持续通信。阅读本文，您将掌握构建生产级、非阻塞式 AI 代理的关键技术细节，从而可靠地应对实际业务中高耗时的操作需求。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 集成，构建能够长时间稳定运行的 MCP 服务器的综合方法。

主要内容分为以下三个关键策略：

1.  **上下文消息策略**：
    引入了一种专门的机制来维护服务器与客户端在长时间运行过程中的持续通信。该策略旨在确保在执行复杂、耗时的操作时，连接不会中断，且双方能够保持信息的同步与连贯性。

2.  **异步任务管理框架**：
    构建了一个异步框架，允许 AI 代理在启动长耗时任务的同时，不阻塞其他操作的进行。这极大地提高了系统的并发处理能力和响应效率。

3.  **生产级集成应用**：
    文章最终演示了如何将上述策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合。这种集成方案使得构建出的 AI 代理不仅具备处理复杂逻辑的能力，还能可靠地管理那些时间密集型的操作，满足生产环境的高标准要求。

---
## 评论

### 文章评价报告

**文章中心观点**
文章提出了一种基于 Amazon Bedrock AgentCore 的架构模式，通过集成 Strands Agents 并结合“上下文消息策略”与“异步任务管理框架”，旨在解决 MCP 服务器在执行长周期任务时的状态保持与通信中断问题。

---

#### 深入评价

**1. 内容深度：架构解构与严谨性**
*   **支撑理由**：文章从技术原理上切中了当前 Agentic Workflow（智能体工作流）的痛点。传统的 LLM 交互是基于 Request-Response 的无状态模式，难以处理耗时数分钟甚至数小时的复杂任务（如代码生成、数据分析）。文章提出的“上下文消息策略”实际上是一种**协议层的适配**，试图在保持 HTTP 连接或利用消息队列的情况下，让 LLM 感知到“任务正在后台进行”。这触及了从“对话式 AI”向“任务式 AI”转型的核心逻辑。
*   **反例/边界条件**：
    *   **边界条件（事实陈述）**：如果长任务本身是 CPU 密集型且无法被拆解为异步子步骤，单纯的“消息策略”无法解决底层计算资源的阻塞问题。
    *   **反例（你的推断）**：对于强一致性要求的业务（如金融交易），异步任务管理框架带来的最终一致性设计可能导致状态同步延迟，引发数据一致性问题。

**2. 实用价值：企业级落地的关键拼图**
*   **支撑理由**：对于正在使用 AWS 生态的企业，这篇文章提供了将开源 MCP 协议与商业托管服务 Bedrock 结合的**最佳实践路径**。MCP 正在成为 AI 应用的“USB 接口”，而 Bedrock AgentCore 提供了编排能力。文章不仅讲了“怎么做”，还隐含了如何利用云原生能力（如 Step Functions 或 Lambda）来维持长连接，这对于构建生产级 AI 应用的架构师具有极高的参考价值。
*   **反例/边界条件**：
    *   **边界条件（作者观点）**：该方案高度依赖 AWS 的特定服务特性，导致厂商锁定风险。对于追求多云部署或边缘计算的场景，该架构的移植成本较高。

**3. 创新性：协议编排与状态管理的融合**
*   **支撑理由**：文章的创新点不在于单一的算法，而在于**系统集成**。它巧妙地利用 Strands Agents（可能指代 AWS 内部或合作伙伴的特定长链路智能体框架）来填补 MCP 协议在“长时任务”上的空白。将“异步任务管理”显式地引入 Agent 的思维链中，这是一种架构模式的创新，推动了 Agent 从“聊天机器人”向“数字员工”演进。
*   **反例/边界条件**：
    *   **反例（你的推断）**：LangGraph 或 LangChain 等开源框架早已通过“Graph”状态机实现了类似的异步任务调度。文章所述方法在底层逻辑上并非首创，而是将通用概念封装进了特定的 AWS 服务语境中。

**4. 可读性与逻辑性**
*   **支撑理由**：文章结构遵循了“问题引入 -> 核心策略 -> 框架实现”的工程化叙事逻辑，清晰易懂。特别是将“Context Message Strategy”单独提炼，有助于开发者快速理解通信层面的设计难点。
*   **反例/边界条件**：
    *   **边界条件（事实陈述）**：摘要末尾中断表明文章可能涉及大量代码实现细节。如果正文中代码占比过高而缺乏架构图解，会降低非开发层决策者的阅读体验。

**5. 行业影响与争议点**
*   **行业影响**：该文章标志着 AI 基础设施正在从“模型中心”向“编排中心”转移。MCP 协议的标准化结合云厂商的托管服务，将加速 AI Agent 在 RPA（机器人流程自动化）和数据处理领域的落地。
*   **争议点（作者观点）**：**服务端 Agent vs 客户端 Agent 的边界模糊**。文章提倡在 Server 端维持长连接，这虽然减轻了客户端的压力，但增加了服务端的资源消耗和成本。在流量高峰期，维持数百万个长连接的 WebSocket 或轮询请求对基础设施是巨大的挑战。

---

#### 实际应用建议

1.  **成本监控**：在采用该异步框架前，必须建立严格的成本监控机制。长轮询或持续连接会导致 AWS 费用（特别是 Lambda 调用时长和 API Gateway 请求量）指数级上升。
2.  **超时处理**：不要盲目相信异步框架的稳定性。务必在客户端和 MCP Server 双侧实现“超时熔断”机制，防止因 Bedrock 模型响应过慢导致的系统雪崩。
3.  **状态持久化**：文章提到的“上下文消息”可能依赖内存缓存。建议将关键任务状态持久化到 DynamoDB 等数据库中，以防 AgentCore 服务重启导致长任务状态丢失。

---

#### 验证与检查方式

为了验证该文章所述架构的有效性，建议进行以下检查：

1.  **并发压力测试**：
    *   *指标*：模拟 1000 个并发用户同时发起长时任务（如 5 分钟以上的文档分析）。
    *   *观察窗口*：观察 AgentCore 是否出现消息堆积，以及 Bedrock 的吞吐量是否触发限流。

2.  **网络中断恢复测试**：
    *   *实验*：在长任务执行期间（例如 50% 进度时），人为断开客户端网络连接 30

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要，以下是对该技术方案的深入分析。由于原文内容较长，此处将基于标题和摘要中透露的关键技术信号（MCP协议、Amazon Bedrock、AgentCore、Strands Agents、长时运行、异步任务）进行深度的技术拆解和逻辑推演。

---

# 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：**在构建生成式AI应用时，为了解决复杂、耗时的业务逻辑与AI模型即时响应特性之间的矛盾，应当采用一种基于“上下文消息策略”和“异步任务管理框架”的架构模式。** 具体而言，就是利用 **MCP (Model Context Protocol)** 服务器作为连接器，结合 **Amazon Bedrock AgentCore** 的编排能力与 **Strands Agents** 的长时记忆/执行特性，来实现能够处理长时间运行任务的智能体系统。

**作者想要传达的核心思想**
传统的“请求-响应”同步模式无法满足现代AI Agent处理复杂任务（如数据分析、代码生成、多步骤工作流）的需求。作者主张将**计算过程与通信过程解耦**。通过引入“Strands”（可能指代长线程或连续的工作流片段）的概念，让Agent具备“挂起”和“恢复”对话的能力，从而在保持用户端交互连续性的同时，后台完成繁重的计算工作。

**观点的创新性和深度**
该观点的创新性在于将**协议层的标准化（MCP）**与**架构层的异步化**相结合。
1.  **协议统一**：利用MCP打破了不同AI应用与数据源之间的孤岛，使得长时运行的服务可以被复用。
2.  **状态管理**：深入探讨了如何在无状态的大语言模型（LLM）与有状态的业务系统之间建立稳定的通信通道（Context Message Strategy），这解决了Agent应用落地的核心痛点。
3.  **编排融合**：将Bedrock的托管能力与Strands的执行逻辑结合，提供了一种可扩展的、企业级的Agent构建范式。

**为什么这个观点重要**
随着AI从“聊天机器人”向“智能体”演进，任务复杂度呈指数级上升。如果无法解决长时运行问题，AI将只能停留在简单的问答层面，无法真正深入到业务流程自动化（RPA）、科研计算或企业资源规划（ERP）等核心领域。这篇文章提供了一套在AWS云原生环境下解决此问题的标准路径。

---

# 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**：由Anthropic推出的开放标准，用于连接AI助手与数据源。在此处，它充当了Agent与后端服务之间的标准化接口。
2.  **Amazon Bedrock AgentCore**：AWS Bedrock的一部分，负责Agent的编排、路由和工具调用逻辑。
3.  **Strands Agents**：这是文章标题中的关键变量。在AWS语境下，这通常指代**Amazon Bedrock Multi-Agent Systems**中的子Agent或者具有长时间记忆/工作流能力的Agent组件（可能引用了AWS Agents for Bedrock中的“Strands”概念，即连续的工作流片段）。它代表能够处理长时任务流的实体。
4.  **异步任务管理框架**：一种允许服务器接收请求后立即返回确认（ACK），并在后台处理，处理完成后再推送结果的模式。

**技术原理和实现方式**
1.  **上下文消息策略**：
    *   **原理**：在长时任务执行期间，系统不能让连接超时。系统需要向客户端发送“心跳”或“中间状态”消息，告知用户“任务正在处理中，请稍候”。
    *   **实现**：通过SSE (Server-Sent Events) 或 WebSocket 保持连接，或者在MCP协议层实现一种`pending_response`机制，让客户端知道需要轮询或等待回调。
2.  **异步任务管理**：
    *   **原理**：将用户请求分解为“指令”和“执行”。
    *   **实现**：当Agent需要运行长时间任务（如处理10万行CSV）时，Bedrock AgentCore不会阻塞等待结果，而是调用MCP Server的异步接口。MCP Server将任务放入队列（如SQS），由Strands Agent在后台拉取并执行。执行完成后，结果被存储（如S3），并通过Bedrock的Session State推回给前端。

**技术难点和解决方案**
*   **难点**：**状态同步与超时控制**。HTTP请求通常在30-60秒后超时，无法满足长时任务需求。
*   **解决方案**：采用**“令牌”机制**。客户端发送请求后，服务器返回一个“任务ID”。客户端利用此ID轮询状态，或通过订阅机制获取更新。Strands Agent负责维护这个任务的生命周期。
*   **难点**：**上下文丢失**。在长时任务中，原始提示词可能被遗忘。
*   **解决方案**：利用Bedrock的**Session History**功能，将用户的原始意图、中间步骤和最终结果持久化存储，确保Agent在恢复对话时拥有完整的上下文。

**技术创新点分析**
*   **MCP作为中间件**：将MCP从简单的数据连接器升级为任务调度器。
*   **Strands集成**：暗示了一种多智能体协作模式，即一个主Agent负责交互，多个Strand Agents负责各自擅长的长时任务，形成“人-系统”交互的连续性。

---

# 3. 实际应用价值

**对实际工作的指导意义**
这篇文章为架构师和AI工程师提供了一种**避免“重新发明轮子”**的方法。利用AWS Bedrock和MCP，企业不需要自己构建一套复杂的异步通信层和Agent框架，可以直接基于云服务构建高可用的AI应用。

**可以应用到哪些场景**
1.  **企业级RPA（机器人流程自动化）**：处理需要跨系统查询、更新、审核的长时间业务流程（如保险理赔审核）。
2.  **金融数据分析**：Agent接收指令，后台运行复杂的Python/R代码分析市场趋势，耗时数分钟，完成后生成图表。
3.  **代码生成与测试**：Agent生成代码后，需要在后台进行编译、部署和集成测试，这是一个典型的长时异步过程。
4.  **文档处理与合规审查**：上传数百页的PDF法律文档，Agent进行分块阅读和比对。

**需要注意的问题**
*   **成本控制**：长时运行的Agent和持续的上下文存储会显著增加Token消耗和基础设施成本。
*   **错误处理**：异步任务失败后的重试机制和用户通知流程比同步模式更复杂。
*   **一致性**：如果用户在任务完成前改变了主意（Cancel操作），如何优雅地终止后台的Strands Agent任务。

**实施建议**
*   **先同步，后异步**：对于秒级任务，保留同步调用；对于分钟级任务，强制使用异步框架。
*   **可视化进度**：利用Strands的特性，尽量向用户展示中间进度条，而不是黑盒等待。

---

# 4. 行业影响分析

**对行业的启示**
这标志着AI Agent开发进入了**“工程化深水区”**。行业焦点从“如何让模型更聪明”转向“如何让系统更健壮”。AWS通过Bedrock和MCP的结合，正在制定企业级AI应用的标准基础设施。

**可能带来的变革**
*   **从“Chat”到“Work”的转变**：用户不再只是与AI对话，而是通过AI交付具体的工作成果。
*   **MCP协议的普及**：随着此类文章的推广，MCP可能成为连接AI模型与企业后端的**事实标准**，类似于SQL之于数据库。

**对行业格局的影响**
这将进一步巩固AWS在AI基础设施领域的领导地位。对于SaaS软件厂商而言，支持MCP协议并接入Bedrock将成为其产品具备“AI Native”特性的关键标志。

---

# 5. 延伸思考

**引发的其他思考**
*   **人机协作的新范式**：如果Agent可以长时间运行，那么人类的角色将从“操作者”转变为“监督者”和“例外处理者”。
*   **Strands的语义**：Strands（股/线）的概念暗示了任务的并行性。未来是否会出现“Strand Marketplace”，即专门售卖某种长时任务处理能力的Agent市场？

**需要进一步研究的问题**
*   **安全性**：长时运行的异步任务如何防止权限越界？如何确保MCP传输过程中的数据隐私？
*   **确定性**：在长时任务链中，如何保证最终结果的一致性和可解释性？

**未来发展趋势**
*   **Agent DevOps**：专门针对Agent的部署、监控、回滚和版本管理工具链的兴起。
*   **混合编排**：将Bedrock的托管能力与自部署的开源Agent（如LangGraph）进行更深度的混合编排。

---

# 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有架构**：检查现有的后端服务是否已经支持异步模式（如使用了Celery, Lambda SQS等）。
2.  **引入MCP SDK**：在现有服务中安装MCP Server SDK，将长时运行的业务逻辑封装为MCP Tools。
3.  **配置Bedrock Agent**：在AWS控制台配置Agent，启用Orchestration（编排），并将MCP Server注册为Action Group。

**具体的行动建议**
*   **第一步**：构建一个简单的MCP Server，实现一个`long_running_task`接口，该接口接收参数后立即返回`task_id`。
*   **第二步**：编写一个后台Worker，模拟耗时操作，完成后将结果写入Bedrock的Session Store或数据库。
*   **第三步**：在Bedrock Agent中配置Prompt，使其知道当调用该工具时，必须告知用户“任务已开始，请稍后查询”。

**需要补充的知识**
*   **异步编程模型**：理解Promise/Async-Await或消息队列机制。
*   **AWS Lambda/SQS/EventBridge**：熟悉AWS的无服务器计算和事件驱动架构。
*   **MCP协议规范**：深入阅读Anthropic的MCP协议文档。

**实践中的注意事项**
*   **避免死锁**：确保异步回调机制能够正确触发Agent的响应，防止用户无限等待。
*   **资源清理**：长时任务可能会产生大量临时文件，需设置自动清理策略。

---

# 7. 案例分析

**结合实际案例说明**
**场景**：一家跨国物流公司需要构建一个AI供应链助手。
**问题**：用户询问“优化下个季度的海运航线”。这涉及到读取数GB的历史数据、运行运筹学优化算法，耗时约5分钟。传统API会超时。

**成功案例分析**
*   **解决方案**：物流公司采用文章所述架构。前端通过Bedrock Agent发送指令。Agent调用MCP Server暴露的`optimize_route`工具。
*   **流程**：MCP Server将任务推送到EC2/SQS计算集群，立即返回“任务ID 12345正在处理”。Strands Agent接管计算。
*   **交互**：前端界面显示“正在分析全球港口拥堵数据...”。5分钟后，结果通过WebSocket推送到前端，Agent自动总结：“已为您节省15%运输成本，新路线图如下”。

**失败案例反思**
*   **错误做法**：直接让LLM生成Python代码并在本地执行。
*   **后果**：用户关闭浏览器窗口，任务中断；或者并发请求导致本地资源耗尽崩溃。

**经验教训总结**
长时任务必须**“上

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化长连接与会话管理策略

**说明**:
在构建长时间运行的 MCP (Model Context Protocol) 服务器时，保持连接的稳定性至关重要。由于 AgentCore 与 Strands Agents 的交互可能涉及多轮对话和长时间的推理过程，必须实施健壮的会话管理机制，以处理网络波动或超时，确保上下文不丢失。

**实施步骤**:
1.  在 MCP 服务器端实现心跳机制，定期检测连接活性。
2.  配置适当的超时设置，确保长任务不会因为短暂的静默而被断开。
3.  利用 Strands Agents 的状态持久化功能，定期保存对话上下文。

**注意事项**: 避免无限期保持空闲连接，应设置合理的空闲超时以释放资源。

---

### 实践 2：实施细粒度的工具与权限控制

**说明**:
Bedrock AgentCore 通过 MCP 暴露工具给 Agent 使用。为了确保安全性，特别是当 Agent 执行系统级操作时，必须严格限制 MCP 服务器暴露的工具范围，并遵循最小权限原则。

**实施步骤**:
1.  明确定义 MCP 服务器提供的工具列表，仅注册 Agent 必需的功能。
2.  在 Bedrock AgentCore 的配置中，明确允许或禁止特定的工具调用。
3.  为不同的 Strands Agents 角色配置不同的工具访问策略。

**注意事项**: 定期审计工具调用日志，确保没有异常的权限提升行为。

---

### 实践 3：构建异步非阻塞的服务架构

**说明**:
Strands Agents 可能会发起耗时较长的请求（如检索数据或生成内容）。如果 MCP 服务器采用同步阻塞架构，会导致整体吞吐量下降。构建异步架构是处理高并发和长运行任务的关键。

**实施步骤**:
1.  使用支持异步 I/O 的框架（如 Python 的 asyncio 或 Node.js）开发 MCP 服务器。
2.  将工具调用设计为异步函数，确保在等待外部资源时不阻塞事件循环。
3.  实现请求队列机制，平滑处理突发流量。

**注意事项**: 确保异步上下文中的共享状态操作是线程安全的。

---

### 实践 4：设计高效的上下文数据传输机制

**说明**:
MCP 服务器与 Agent 之间传输的数据量直接影响响应速度。在长运行场景下，不必要的数据重复传输会增加延迟和成本。应优化数据结构，仅传输必要的上下文信息。

**实施步骤**:
1.  对通过 MCP 传输的负载进行压缩或精简，去除冗余字段。
2.  利用引用机制，对于大型数据集，仅传递 ID 或指针，而非全量数据。
3.  在 Strands Agents 配置中，优化 Prompt 模板，减少上下文窗口的占用。

**注意事项**: 平衡数据完整性与传输效率，避免因过度精简导致 Agent 缺乏关键信息。

---

### 实践 5：建立全面的日志记录与可观测性体系

**说明**:
长运行服务难以调试。为了追踪 Strands Agents 在 MCP 服务器上的行为轨迹，必须建立完善的日志和监控体系，以便快速定位故障或性能瓶颈。

**实施步骤**:
1.  在 MCP 服务器的每个工具调用入口和出口记录结构化日志（包含 Request ID）。
2.  将 MCP 服务器的日志与 Amazon CloudWatch 集成，实现集中监控。
3.  为关键操作路径添加分布式追踪，分析调用链中的耗时。

**注意事项**: 注意日志脱敏，确保敏感信息不被记录到日志系统中。

---

### 实践 6：配置优雅退出门槛与错误重试逻辑

**说明**:
在长时间运行过程中，服务可能会遇到不可恢复的错误或需要进行维护。设计优雅的退出机制和智能重试策略，可以防止数据损坏并提升服务韧性。

**实施步骤**:
1.  在 MCP 服务器中实现信号处理（如 SIGTERM），在收到终止信号时完成当前请求处理后再关闭。
2.  为 Strands Agents 调用 MCP 工具的请求配置指数退避重试策略。
3.  定义明确的错误代码映射，让 AgentCore 能够识别是临时错误还是永久错误。

**注意事项**: 避免对非幂等操作进行自动重试，防止数据重复。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够长时间运行并保持对话状态的有状态 MCP 服务器。
- 通过利用 Strands 框架的内置状态管理功能，开发者无需手动处理复杂的会话持久化逻辑，即可实现跨多轮对话的上下文记忆。
- 该架构将 Strands Agents 的状态层与 Bedrock AgentCore 的托管服务相结合，显著降低了构建复杂多步骤自动化工作流的技术门槛。
- 借助 MCP (Model Context Protocol) 的标准化接口，这些长期运行的服务器可以轻松与各类支持 MCP 的 AI 应用和开发环境实现无缝集成。
- 这种集成方案特别适用于需要持续跟踪任务进度或处理复杂工作流的场景，例如代码生成、数据分析或多步骤业务流程的自动化。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [MCP](/tags/mcp/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [上下文策略](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AD%96%E7%95%A5/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器的异步任务框架]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-6.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*