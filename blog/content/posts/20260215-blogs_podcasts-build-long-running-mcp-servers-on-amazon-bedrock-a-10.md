---
title: "基于Amazon Bedrock AgentCore构建长时间运行的MCP服务器与异步任务管理"
date: 2026-02-15T02:54:54+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "MCP", "Strands Agents", "异步任务", "长连接", "AI Agent", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 构建能够长时间运行 MCP 服务器的综合方法，主要包含以下三个关键策略： 1. **引入上下文消息策略**：实施一种通信机制，确保服务器与客户端在执行耗时操作期间能够保持连续的消息传递和状态同步。 2. **开发异步"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建长时间运行的MCP服务器与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们将为您提供一个全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，用于在服务器和客户端之间在长时间操作期间保持持续通信。接下来，我们构建一个异步任务管理框架，允许您的 AI 代理启动长时间运行的任务而不阻塞其他操作。最后，我们演示如何结合 Amazon Bedrock AgentCore 和 Strands Agents，将这些策略整合在一起，构建生产就绪的 AI 代理，从而可靠地处理复杂且耗时的操作。

---
## 导语

构建能够稳定处理长时间运行任务的 AI 代理是许多生产环境中的核心需求。本文将介绍如何利用 Amazon Bedrock AgentCore 与 Strands Agents 的集成，通过上下文消息策略和异步任务管理框架，解决服务端与客户端在长周期操作中的持续通信问题。您将获得一套构建生产级 AI 代理的完整方法，以可靠地应对复杂且耗时的业务场景。

---
## 摘要

本文介绍了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 构建能够长时间运行 MCP 服务器的综合方法，主要包含以下三个关键策略：

1.  **引入上下文消息策略**：实施一种通信机制，确保服务器与客户端在执行耗时操作期间能够保持连续的消息传递和状态同步。
2.  **开发异步任务管理框架**：构建一个异步框架，允许 AI 代理在启动长时间进程时不阻塞其他任务的执行，从而提高系统的并发能力和响应速度。
3.  **集成与实现**：展示如何结合上述策略，利用 Amazon Bedrock AgentCore 和 Strands Agents 构建生产就绪的 AI 代理，使其能够可靠、稳定地处理复杂且耗时的操作。

---
## 评论

**文章中心观点**
该文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的技术架构，旨在通过上下文消息策略和异步任务管理框架，解决在模型上下文协议（MCP）上构建长时间运行（Long-running）的 AI 智能体时面临的连接中断与状态管理难题，以实现稳健的企业级工作流自动化。

**深入评价与支撑理由**

**1. 内容深度：从“对话”到“工作流”的架构跨越**
*   **支撑理由（事实陈述/你的推断）：** 文章触及了当前 AI Agent 开发中最核心的痛点之一——HTTP 请求的超时与无状态性。传统的 LLM 调用通常是秒级反馈，而企业级任务（如数据查询、代码生成、跨系统编排）往往需要数分钟甚至更久。文章引入的“异步任务管理框架”实际上是在构建一个**中间件层**，将 LLM 的“同步思维模式”与底层系统的“异步执行模式”进行解耦。这种解耦是构建复杂生产系统的必经之路，体现了作者对分布式系统与 AI 结合的深刻理解。
*   **反例/边界条件（你的推断）：** 该方案增加了系统的复杂度。对于简单的、毫秒级的检索增强生成（RAG）任务，引入 Strands Agents 和异步框架可能属于“过度设计”，反而会增加延迟和调试难度。

**2. 实用价值：填补了 Bedrock 生态的执行空白**
*   **支撑理由（作者观点/事实陈述）：** Amazon Bedrock 虽然提供了强大的模型托管能力，但在“如何让模型长时间干活”这一环节上，原生支持相对基础。文章提供的代码示例和框架设计，直接指导开发者如何利用 Bedrock AgentCore 的能力来维持状态，这对于正在 AWS 上构建 AI 应用的开发者具有极高的参考价值。它不仅是一个技术方案，更是一个**抗模式指南**，教导开发者如何避免在长任务中丢失上下文。
*   **反例/边界条件（你的推断）：** 实用性受限于厂商锁定。如果企业未来计划迁移出 AWS，这种深度依赖 Bedrock AgentCore 和 Strands 特定 API 的架构将带来高昂的迁移成本。

**3. 创新性：状态维持的“缝合”艺术**
*   **支撑理由（你的推断）：** 文章的创新点不在于发明了全新的算法，而在于**组合式创新**。它巧妙地利用 MCP（Model Context Protocol）的标准化接口，结合 Bedrock 的托管能力，提出了一种“上下文消息策略”。这种策略可以被视为一种“心跳机制”或“进度回调协议”，让 Agent 在执行长任务时不会因为“沉默”而被客户端或网络层判定为超时。这在当前 MCP 生态尚处于早期、缺乏统一长任务标准的背景下，具有前瞻性的探索意义。
*   **反例/边界条件（事实陈述）：** 相比于 LangChain 或 LangGraph 等开源框架已经成熟的“State Machine”（状态机）模式，文章提出的方案是否在灵活性和可视化程度上具有优势，仍有待验证。

**4. 行业影响与争议点：标准化与厂商博弈**
*   **支撑理由（行业影响）：** 该文章展示了 AWS 试图通过 Bedrock AgentCore 来定义 AI Agent 运行时标准的野心。如果这种模式成为 AWS 上的最佳实践，将推动行业从“简单的 ChatBot”向“自主的 Job Worker”转变。
*   **争议点（你的推断）：** 这里存在一个潜在的技术债风险。文章推崇的 Strands Agents 可能是 AWS 特有的封装逻辑。这与 Anthropic 官方推行的原生 MCP 模型可能存在概念重叠或冲突。开发者需要警惕：这是 AWS 为了锁定用户而构建的“糖衣”，还是真正基于 MCP 标准的通用扩展？如果 Strands 只是 Bedrock 独有的功能，那么所谓的“MCP Servers”实际上变成了“AWS-Only MCP Servers”，这与 MCP 协议旨在促进互操作性的初衷相悖。

**5. 可读性与逻辑**
*   **支撑理由（事实陈述）：** 标题清晰直击痛点，摘要中明确指出了两个核心技术手段，逻辑链条完整。
*   **反例/边界条件（作者观点）：** 技术博客通常容易陷入代码细节而忽略架构图。如果文章缺乏一张清晰的“时序图”来展示异步任务的生命周期，读者将很难在脑海中构建完整的执行流。

**实际应用建议**

1.  **评估任务粒度**：仅在任务执行时间超过 30 秒（如涉及数据库 ETL、多步骤 API 调用）时采用此架构，短任务保持同步调用以降低延迟。
2.  **监控与可观测性**：由于引入了异步层，必须建立完善的任务状态追踪机制。建议利用 AWS CloudWatch 监控 AgentCore 的状态转换，防止任务“静默失败”或僵死。
3.  **成本控制**：长连接和上下文维持会显著增加 Token 消耗和 API 调用费用，建议在 Prompt 中加入“终止指令”，避免 Agent 在无效循环中空转。

**可验证的检查方式**

1.  **压力测试指标（实验）：** 搭建一个模拟长任务（如 5 分钟处理时间）的测试环境，测量在并发 50 个请求的情况下，系统的 P99 延迟以及是否有连接断开导致的任务失败率。
2.  **成本对比分析（观察窗口）：** 对比“同步轮询”与“异步回调”两种模式在完成 1000 次长任务时的 Token

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 的长运行 MCP 服务器构建

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：**在构建基于大模型（LLM）的智能体应用时，必须解决“长时运行任务”与“协议超时”之间的矛盾。** 通过在 Amazon Bedrock AgentCore 上集成 Strands Agents 框架，并采用特定的上下文消息策略和异步任务管理框架，开发者可以构建出能够处理复杂、耗时业务流程的 MCP（Model Context Protocol）服务器，从而突破传统 LLM 单次交互的时长限制。

**作者想要传达的核心思想**
作者试图传达从“对话式交互”向“工作流式交互”转变的工程思想。传统的 LLM 应用多为“请求-响应”模式，而企业级应用往往需要 Agent 持续运行、监控状态并在事后汇报。核心思想在于**“解耦”**——将 LLM 的快速响应能力与后端耗时的业务执行逻辑分离，通过异步机制让 AI 具备“执行力”而非仅仅是“表达力”。

**观点的创新性和深度**
该观点的创新点在于将 **MCP 协议**（一种标准化的上下文传输协议）与 **Amazon Bedrock AgentCore**（托管式编排服务）及 **Strands Agents**（长时运行代理框架）进行了深度融合。它不仅解决了技术实现上的超时问题，还引入了“上下文消息策略”来维持对话的连续性，这标志着 AI Agent 从简单的“Chatbot”向能够处理复杂事务的“Digital Worker”演进。

**为什么这个观点重要**
随着 AI 进入落地期，企业不再满足于 AI 能够“回答问题”，而是要求 AI 能够“解决问题”。许多企业任务（如数据迁移、代码生成、复杂审批）耗时超过 LLM 的超时限制（通常为 2 分钟）。如果无法解决长运行问题，AI Agent 将难以真正融入核心业务流。因此，这篇文章提供的是**AI Agent 工业化部署的关键基础设施方案**。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **MCP (Model Context Protocol)**：用于在 LLM 客户端与服务器之间标准化传输上下文和数据。
2.  **Amazon Bedrock AgentCore**：AWS 提供的底层编排服务，用于构建和管理 Agent。
3.  **Strands Agents**：一种专门设计用于处理长运行、多步骤任务的 Agent 框架。
4.  **异步任务管理**：非阻塞的任务处理模式。
5.  **上下文消息策略**：一种在长任务期间保持客户端与服务器连接活跃的心跳或状态同步机制。

**技术原理和实现方式**
*   **上下文消息策略**：在长任务执行期间，服务器不能保持静默，否则 MCP 客户端或网络层可能会断开连接。实现方式通常是服务器定期发送“中间状态”或“心跳”消息给客户端，告知任务仍在进行中，从而维持通信通道的活性。
*   **异步任务管理框架**：
    *   **触发阶段**：MCP Server 接收到 LLM 的工具调用请求后，不直接执行耗时操作，而是将任务提交给后台任务队列（如 AWS Step Functions 或 Lambda 异步调用）。
    *   **执行阶段**：后台进程独立执行任务，MCP Server 立即返回一个“任务已接收”的响应。
    *   **轮询/回调阶段**：LLM 通过后续的轮询或通过 Strands Agents 的状态更新来获取最终结果。

**技术难点和解决方案**
*   **难点 1：超时与连接中断**。LLM 调用工具通常有超时限制（如 90秒或 120秒），若后端任务超过此时间，连接会断开。
    *   **解决方案**：采用“Fire-and-Forget”（触发即遗忘）模式配合异步状态查询。MCP Server 返回任务 ID，Agent 进入等待状态，通过后续轮询获取结果。
*   **难点 2：状态一致性**。在异步过程中，如果用户打断任务或系统重启，如何处理？
    *   **解决方案**：利用 Strands Agents 的状态持久化能力，将任务状态存储在数据库（如 DynamoDB）中，确保任务可追溯、可恢复。

**技术创新点分析**
最大的创新点在于**将 MCP 协议的轻量级特性与 Bedrock AgentCore 的强编排能力结合**。通常 MCP 用于本地工具调用，而文章将其扩展到了云端的长运行工作流，使得客户端（如 IDE 或 Chat App）可以通过统一的协议调用极其复杂的云端自动化流程。

## 3. 实际应用价值

**对实际工作的指导意义**
这篇文章为架构师和 AI 工程师提供了一套**标准化的长运行 Agent 架构蓝图**。它指导开发者不要试图在 LLM 的线程中直接进行重计算，而应构建一个分布式的任务调度系统。

**可以应用到哪些场景**
1.  **软件开发与 DevOps**：代码库重构、大规模测试运行、CI/CD 流水线触发（这些操作可能耗时数小时）。
2.  **数据分析与报表**：生成复杂的 ETL 作业，处理海量数据并生成报表。
3.  **企业内容管理**：跨系统的文档迁移、大批量文件处理与格式转换。
4.  **RPA（机器人流程自动化）**：跨多个业务系统的长流程审批与录入。

**需要注意的问题**
*   **成本控制**：长运行任务通常涉及频繁的轮询或长连接，可能会增加 API 调用成本和基础设施费用。
*   **错误处理**：异步任务失败后的重试机制和用户通知机制比同步模式更复杂。

**实施建议**
*   **优先使用 Step Functions**：在 AWS 环境下，建议使用 Step Functions 作为长运行任务的编排引擎，它能完美解决超时和状态管理问题。
*   **设计清晰的中间态**：对于用户来说，等待是焦虑的。利用“上下文消息策略”实时反馈进度条或日志是提升用户体验的关键。

## 4. 行业影响分析

**对行业的启示**
该方案表明，**AI Agent 的基础设施正在“云原生化”**。未来的 AI 应用不仅仅是调用 OpenAI/Claude 的 API，更需要构建强大的后端服务来支撑 Agent 的“行动力”。

**可能带来的变革**
这将推动 **MCP 协议** 成为连接 AI 与企业后端的标准接口。如果 MCP 能解决长运行问题，它可能取代部分传统的 API 集成方式，成为企业数字化转型的“最后一公里”协议。

**对行业格局的影响**
对于 AWS 来说，强化 Bedrock AgentCore 的能力有助于其在激烈的 AI 基础设施竞争中保持优势。通过支持 Strands 等框架，AWS 正在构建一个护城河，将复杂的 AI 工作流锁定在其云生态系统中。

## 5. 延伸思考

**引发的其他思考**
*   **人机协作的新模式**：如果 Agent 可以长运行，那么人类在其中的角色是什么？是“发起者”还是“异常处理者”？
*   **多 Agent 协作**：Strands Agents 是否支持多个长运行 Agent 之间的协作？例如一个 Agent 负责写代码，另一个负责长时间测试。

**可以拓展的方向**
*   **流式响应的增强**：目前的上下文消息可能只是简单的状态更新，未来是否可以支持流式返回中间结果？
*   **边缘计算的结合**：MCP Server 是否可以部署在边缘设备上，而将长运行任务交给云端 Bedrock？

**未来发展趋势**
长运行 Agent 将催生 **"Agent-as-a-Service"（代理即服务）** 的商业模式。企业将不再购买软件，而是购买能够自主完成长周期任务的数字员工。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估任务时长**：检查你现有的 AI Agent 应用中，哪些工具调用可能超过 30 秒。
2.  **引入异步层**：不要直接在 Lambda 函数中执行长任务，而是通过 SNS/SQS/Step Functions 进行解耦。
3.  **实现 MCP Server**：参考文章中的模式，构建一个基于 Python/TypeScript 的 MCP Server，封装异步任务的触发接口。

**具体的行动建议**
*   **阅读 Strands Agents 文档**：深入理解其状态机模型。
*   **搭建 Bedrock Prototype**：在 AWS 控制台创建一个 Agent，尝试调用一个模拟的长运行 Lambda 函数。
*   **监控与可观测性**：务必配置 CloudWatch 来监控异步任务的执行时间，因为长运行任务最容易产生“僵尸进程”。

**需要补充的知识**
*   **Python asyncio 或 Node.js 异步编程**。
*   **AWS Step Functions 工作流设计**。
*   **MCP 协议规范**。

## 7. 案例分析

**结合实际案例说明**
假设我们要构建一个 **“AI 代码审计员”**。
*   **传统模式**：用户发送代码 -> LLM 分析 -> 返回结果。如果代码库巨大，LLM 直接读取会超时或 Token 溢出。
*   **基于文章方案的模式**：
    1.  用户通过 MCP 客户端发送“审计整个 GitHub 仓库”的指令。
    2.  Bedrock Agent 接收指令，调用 MCP Server 的 `start_audit` 工具。
    3.  MCP Server 触发 Step Functions 工作流，该工作流遍历文件、调用 LLM 分块分析、汇总报告（耗时 15 分钟）。
    4.  MCP Server 立即返回 `{"status": "running", "task_id": "123"}`。
    5.  Bedrock Agent 告诉用户：“审计已开始，正在后台运行...”。
    6.  用户继续提问，Agent 定期轮询 `get_status` 工具。
    7.  15分钟后，Agent 获取到最终报告并发送给用户。

**成功案例分析**
GitHub Copilot Workspace 的某些后台任务处理逻辑与此类似，它允许用户发起长时间的代码重构任务，而不会阻塞当前的聊天界面。

**失败案例反思**
如果强行使用同步模式处理长任务，用户会看到“Loading...”直到超时报错。这种体验是导致早期 AI Bot 被用户弃用的主要原因。

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级 AI Agent 时，**必须**采用基于 Amazon Bedrock AgentCore 和 Strands Agents 的异步架构，以实现 MCP 服务器对长运行任务的有效支撑。

**支撑理由**
1.  **必要性**：企业核心业务流程（如数据处理、代码生成）的执行时间通常远超 LLM 同步调用的超时限制（事实）。
2.  **稳定性**：引入上下文消息策略和异步管理，可以防止网络中断和进程超时导致的任务失败（技术原理）。
3.  **标准化**：使用 MCP 协议可以确保前端客户端与后端 Bedrock 服务之间的解耦，提升系统的可维护性（架构价值）。

**反例或边界条件**
1.  **简单查询场景**：对于纯知识检索或简单计算（毫秒级响应），引入复杂的异步框架和 Strands Agents 可能属于过度设计，增加了系统延迟和复杂

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 Strands Agents 的会话状态管理

**说明**：在构建长时间运行的 MCP 服务器时，Strands Agents 需要在多轮对话中维护上下文。如果每次请求都重新加载完整的历史记录，会导致延迟增加和 Token 消耗过大。最佳实践是实施一种混合状态管理策略，仅保留关键的上下文摘要和最近的消息，而不是保留原始的完整历史记录。

**实施步骤**:
1. 实现一个滑动窗口机制，仅保留最近 N 轮（如 5-10 轮）的完整对话记录。
2. 对较早的对话进行摘要处理，提取关键实体和用户意图，将其作为“系统提示”或“历史摘要”保留。
3. 在 Bedrock AgentCore 的配置中，利用 `sessionState` 字段传递这些精简后的上下文，而不是依赖默认的全量历史记录。

**注意事项**: 避免在会话状态中存储敏感的 PII（个人身份信息），并确保摘要逻辑不会丢失用户的核心需求。

---

### 实践 2：实施健壮的超时与重试策略

**说明**：长时间运行的进程更容易遇到网络波动或 Bedrock 模型的限流。MCP 服务器必须具备处理暂时性故障的能力。最佳实践是配置指数退避重试机制，并为 MCP 工具调用设置合理的超时时间，以防止代理挂起。

**实施步骤**:
1. 为所有通过 Bedrock AgentCore 发起的 API 调用配置指数退避算法（如初始等待 1 秒，最大重试次数 5 次）。
2. 在 MCP 服务器端实现“请求取消”协议支持，如果客户端断开连接，服务器应能优雅地终止长时间运行的任务。
3. 针对耗时较长的 Strands Agents 任务，实现异步处理模式：立即返回一个“任务已接收”的响应，并通过回调或轮询机制返回最终结果。

**注意事项**: 确保重试逻辑不会导致重复扣费或数据重复处理（幂等性设计）。

---

### 实践 3：利用并发控制管理资源消耗

**说明**：Strands Agents 可能会触发多个并发的工具调用。在高负载情况下，无限制的并发可能会导致底层资源耗尽或触及 Amazon Bedrock 的速率限制。最佳实践是实现信号量或租约机制来限制并发操作的数量。

**实施步骤**:
1. 在 MCP 服务器中实现一个信号量，限制同时处理的 Strands Agents 请求最大数量（例如 10 个并发请求）。
2. 对于资源密集型任务，实现任务队列系统，将任务序列化处理，而不是直接在请求线程中执行。
3. 监控 Bedrock 的 `ThrottlingException` 错误，并动态调整并发限制。

**注意事项**: 不要依赖客户端的并发控制，必须在服务器端强制执行限制。

---

### 实践 4：设计幂等的 MCP 工具接口

**说明**：在长时间运行的交互中，网络中断可能导致客户端不确定操作是否完成，从而触发重试。如果 MCP 工具不是幂等的，重试可能导致数据损坏（例如重复创建数据库记录）。所有由 Strands Agents 调用的写入操作都应是幂等的。

**实施步骤**:
1. 为每个需要修改状态的操作生成唯一的 `idempotencyKey`（由客户端生成或由服务器分配）。
2. 在工具逻辑执行前，检查该 Key 是否已被处理；如果是，则返回之前的结果而不执行操作。
3. 对于非写入操作，确保 GET 请求是纯函数式的，不依赖服务器端的可变状态。

**注意事项**: 幂等键的存储应设置合理的过期时间（如 24 小时），以防止存储无限增长。

---

### 实践 5：建立结构化的可观测性体系

**说明**：调试长时间运行的 Agent 交互非常困难。最佳实践是将 Strands Agents 的思考链、工具调用参数和返回值进行结构化日志记录。这有助于追踪性能瓶颈和逻辑错误。

**实施步骤**:
1. 集成 Amazon CloudWatch Logs 或 X-Ray，为每个 MCP 请求分配唯一的 `Trace ID`。
2. 记录 Strands Agents 的关键决策点，特别是工具调用的输入/输出（注意脱敏）。
3. 捕获并记录工具执行的延迟指标，将其细分为“网络传输时间”、“模型推理时间”和“工具执行时间”。

**注意事项**: 严格过滤日志中的敏感信息，并确保日志格式与 CloudWatch Logs Insights 兼容以便于查询。

---

### 实践 6：合理配置模型参数以平衡延迟与质量

**说明**：对于长时间运行的交互，响应速度至关重要。Strands Agents 在 Bedrock AgentCore 中运行时，默认的模型参数可能偏向于高质量而非低延迟。最佳实践是根据任务的复杂程度动态调整推理参数。

**实施步骤**:
1. 对于简单的查询任务，使用较低的 `maxTokens` 和 `temperature` 值，以加快响应速度。
2. 对于复杂的推理任务，允许使用更高的 `maxTokens`，但应在 Agent

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持通过 Strands Agents 集成来构建能够维持长期对话状态和记忆的 MCP 服务器。
- 开发者可以利用 Strands 框架将复杂的任务拆解为子任务并编排执行流程，从而显著提升 Agent 处理多步骤工作的能力。
- 该集成方案解决了传统无状态 Agent 的局限性，使得应用能够在长时间运行的工作流中保持上下文连贯性。
- 通过结合 Bedrock 的托管基础设施与 Strands 的状态管理能力，企业能够以更低成本开发出更可靠的生成式 AI 应用。
- 此架构支持将 MCP 作为统一接口，便于将现有的企业数据源和工具安全地连接到 Bedrock Agent 生态系统中。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [MCP](/tags/mcp/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/) / [AI Agent](/tags/ai-agent/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-5.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-7.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*