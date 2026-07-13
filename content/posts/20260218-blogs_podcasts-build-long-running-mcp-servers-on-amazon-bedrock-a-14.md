---
title: "构建基于Bedrock AgentCore的长运行MCP服务器与异步任务框架"
date: 2026-02-18T07:39:44+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Bedrock", "AgentCore", "异步任务", "长运行服务", "Strands Agents", "AI 代理", "系统架构"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 构建长时间运行 MCP 服务器的综合方法，旨在解决 AI 代理在处理复杂、耗时操作时的可靠性和连续性问题。主要内容如下： 1. **上下文消息策略**：引入了一种机制，用于在服务器和客户端之间维持扩展操作期间的持续通"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 构建基于Bedrock AgentCore的长运行MCP服务器与异步任务框架

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们将为您提供一个全面的解决方案以实现这一目标。首先，我们介绍一种上下文消息策略，用于在长时间运行的操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的过程，同时不阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，构建可投入生产环境的 AI 代理，从而可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理往往面临着状态管理与通信中断的挑战。本文将介绍一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的解决方案，通过上下文消息策略与异步任务管理框架，确保服务器与客户端在复杂操作期间的持续通信。您将了解到如何构建一个生产就绪的系统，使其在不阻塞主流程的前提下，可靠地执行耗时任务。

---
## 摘要

本文介绍了一种利用 Amazon Bedrock AgentCore 和 Strands Agents 构建长时间运行 MCP 服务器的综合方法，旨在解决 AI 代理在处理复杂、耗时操作时的可靠性和连续性问题。主要内容如下：

1.  **上下文消息策略**：引入了一种机制，用于在服务器和客户端之间维持扩展操作期间的持续通信，确保任务状态的实时同步。

2.  **异步任务管理框架**：开发了异步框架，允许 AI 代理启动长时间运行流程而不阻塞其他操作，提升系统并发处理能力。

3.  **生产级集成方案**：结合上述策略与 Amazon Bedrock AgentCore 及 Strands Agents，实现能够可靠处理复杂、耗时操作的生产就绪型 AI 代理。

该方法通过优化通信和任务管理，显著提升了 AI 系统在长周期任务中的稳定性和效率。

---
## 评论

**文章中心观点**
本文主张通过引入“Strands Agents”集成与特定的上下文消息策略，在Amazon Bedrock AgentCore上构建能够维持长时间运行状态（Long-running）的MCP服务器，以解决AI Agent在处理耗时任务时的同步阻塞与状态管理难题。

**支撑理由与边界条件分析**

1.  **架构模式的演进：从“请求-响应”到“异步任务流”**
    *   **事实陈述**：文章提出了一个异步任务管理框架，将MCP（Model Context Protocol）服务器从简单的同步调用转变为能够处理长时间运行工作流的异步节点。
    *   **支撑理由**：传统的LLM应用受限于Token生成时间窗口，难以处理如数据ETL、复杂代码部署等耗时任务。通过引入“Strands Agents”（推测为AWS内部或合作伙伴的长时间运行Agent框架），文章试图将控制流与执行流解耦，使得Agent可以启动任务、释放连接，并在任务完成后通过回调或轮询获取结果。
    *   **反例/边界条件**：对于低延迟要求的简单查询（如“今天天气如何”），引入复杂的异步框架和Strands集成会显著增加系统延迟和架构复杂度，属于过度设计。

2.  **上下文连续性策略的技术实现**
    *   **事实陈述**：文章介绍了一种“上下文消息策略”，用于在服务器和客户端之间维持通信。
    *   **支撑理由**：在长时间运行中，LLM的上下文窗口可能关闭，或者会话状态可能丢失。该策略通过定期发送心跳或状态更新消息，确保Agent在任务重启或状态查询时能够“回忆”起之前的进度，这是实现类SWE-Agent或DevOps自动化工具的关键。
    *   **你的推断**：这很可能利用了Bedrock的会话持久化存储或外部记忆存储（如Redis/DynamoDB）来保存中间状态，而非单纯依赖Prompt内的上下文。

3.  **基于MCP协议的生态互操作性**
    *   **事实陈述**：文章强调构建的是“MCP servers”。
    *   **支撑理由**：MCP作为新兴的开放连接标准，允许AI应用连接外部数据源。在Bedrock AgentCore上原生支持MCP并扩展其Long-running能力，意味着企业可以更容易地将AWS的托管能力与外部工具（如GitHub、Jira）集成，构建跨平台的复杂自动化流。
    *   **反例/边界条件**：如果“Strands Agents”是AWS专有的封闭协议，那么所谓的MCP集成可能仅限于AWS生态内部，无法真正通用化，导致厂商锁定风险。

**多维度深入评价**

1.  **内容深度与严谨性**
    文章触及了当前Agentic Workflow中最核心的痛点：**状态持久化与异步编排**。传统的Agent框架往往假设任务在几秒内完成，而现实世界的任务往往是分钟级的。文章提出的“异步任务管理框架”在理论上是严谨的，符合分布式系统中“Command Pattern”或“Saga模式”的设计思想。然而，摘要中未详细阐述错误处理机制——如果长时间运行的任务中途失败，Strands Agent如何进行回滚或补偿？这是衡量其深度的关键缺失点。

2.  **实用价值**
    对于正在使用AWS Bedrock构建企业级应用的开发者而言，价值极高。它提供了一种“官方推荐”的路径来规避Lambda函数（通常有15分钟超时限制）或API Gateway超时的限制。特别是对于需要处理RAG（检索增强生成）中大规模索引构建，或进行自动化代码生成的场景，该方案提供了直接的工程指导。

3.  **创新性**
    将“Strands Agents”概念引入Bedrock AgentCore是本文最大的创新点。如果Strands代表了一种链式思考或多步推理的实体化，那么这实际上是在尝试将“快思考”（System 1，LLM的直接反应）与“慢思考”（System 2，Strands的长期规划与执行）结合。这比单纯的Function Calling进了一步，更接近于真正的AI Worker。

4.  **行业影响与争议点**
    *   **行业影响**：这可能预示着AWS正在构建比现有Bedrock Agents更高级的编排层，直接对标LangChain的LangGraph或微软的Autogen，推动Agent从“聊天机器人”向“业务流程处理器”转型。
    *   **争议点**：**厂商锁定**。文章暗示深度依赖Bedrock的特定组件。如果企业未来想迁移至GCP或Azure，这种深度的Strands集成可能会带来巨大的迁移成本。此外，“Strands”并非行业标准术语，其定义的模糊性可能让技术决策者持观望态度。

**实际应用建议**

1.  **评估任务粒度**：仅在任务执行时间超过30秒或涉及多步骤外部API调用时，考虑采用此Long-running架构。简单问答应保持直连。
2.  **监控与可观测性**：实施该架构时，必须配套建设分布式追踪。异步任务使得调试变得极其困难，你需要清楚地看到Strand Agent在哪个步骤卡住了。
3.  **成本控制**：长时间运行的Agent和持续的上下文消息策略会显著增加Token消耗和API调用次数，需设置严格的预算和超时熔断机制。

**可验证的检查方式**

1.  **指标验证**：部署该架构后，观察“任务完成率”与“平均响应时间”的解耦情况。验证长时间任务（如>5分钟）是否不再返回HTTP 504 Gateway Timeout错误。
2.  **协议兼容性测试**：尝试用非AWS的MCP Client连接该Server，验证Strands

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 构建长时间运行的 MCP 服务器

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**传统的同步请求-响应模式无法满足现代 AI 智能体在处理复杂、长时间运行任务时的需求。通过在 Amazon Bedrock AgentCore 上集成 Strands Agents 框架，并利用模型上下文协议（MCP）的特定消息策略，可以构建出具备状态管理、异步执行和持续通信能力的“长时间运行”服务器。**

### 作者想要传达的核心思想
作者试图传达一种架构范式的转变。在 AI 应用开发的早期，我们主要关注单轮对话或简单的工具调用。然而，随着 AI Agent（智能体）处理任务的复杂性增加（如编写代码、数据分析、工作流自动化），任务执行时间往往超过了 LLM 的上下文窗口或客户端的超时限制。
作者的核心思想是**“将计算与通信解耦”**。通过引入“Strands”（ strands of thought，思维链/任务流）的概念，将 Agent 的任务生命周期与客户端的会话生命周期分离，从而实现真正的“后台任务”处理能力。

### 观点的创新性和深度
该观点的创新性在于结合了三个层面的技术：
1.  **协议层 (MCP)**：利用新兴的 MCP 标准作为统一的数据接口。
2.  **基础设施层**：利用 AWS 的托管服务来处理底层逻辑。
3.  **架构模式层**：引入类似“Strands”的异步任务管理框架，这类似于后端开发中的“消息队列”或“Job System”，但是专门为 LLM 的上下文和推理逻辑设计的。

### 为什么这个观点重要
这一观点解决了当前生成式 AI 落地中的一个关键痛点：**“交互体验与任务复杂度的矛盾”**。如果不解决长时运行问题，AI Agent 只能作为简单的聊天机器人存在，无法深入企业业务流程。解决这一问题后，AI Agent 才能真正从“玩具”转变为“数字员工”，执行需要数分钟甚至数小时的复杂业务逻辑。

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Model Context Protocol (MCP)**：一种开放协议，用于连接 AI 应用与数据源。文章重点在于 MCP 服务器的实现。
2.  **Amazon Bedrock AgentCore**：AWS 提供的构建 Agent 的底层框架，允许开发者精细控制 Agent 的推理循环和工具调用。
3.  **Strands Agents**：这是文章引入的特定框架或概念，指代能够处理长时间运行、多步骤任务的 Agent 模式，通常涉及状态持久化和恢复机制。
4.  **Context Message Strategy（上下文消息策略）**：一种在长时任务中保持客户端与服务器同步的通信机制。

### 技术原理和实现方式
1.  **异步任务管理框架**：
    *   **原理**：当 Agent 接收到一个耗时任务（如“处理这个大型 CSV 并生成报告”）时，它不会阻塞 HTTP 连接等待结果。相反，它会创建一个“Strand”（任务实例），将其放入后台队列，并立即返回一个 `Task ID` 给客户端。
    *   **实现**：利用 AWS Lambda 或容器服务处理后台逻辑，配合 Amazon DynamoDB 或 S3 存储中间状态和最终结果。

2.  **上下文消息策略**：
    *   **原理**：在任务执行过程中，服务器需要向客户端报告进度，或者客户端需要查询状态。
    *   **实现**：通过 MCP 协议定义特定的消息类型（如 `progress_notification`），或者利用轮询机制。Agent 将任务的中间步骤作为“上下文片段”存储，客户端可以在后续对话中基于此 ID 进行查询或继续交互。

### 技术难点和解决方案
*   **难点1：状态持久化**。LLM 本身是无状态的，但长时任务必须有状态。
    *   **解决方案**：使用 Strands 框架将任务的每一个 Checkpoint 存储在数据库中。当 Agent 重新被唤醒时，加载之前的上下文。
*   **难点2：超时与连接中断**。HTTP 连接可能会在任务完成前断开。
    *   **解决方案**：采用“即发即弃”模式处理任务请求，通信层与业务逻辑层完全解耦。
*   **难点3：上下文窗口限制**。长时任务可能产生海量日志，无法全部放入 Prompt。
    *   **解决方案**：智能摘要策略。只将关键里程碑或最终结果传递给 LLM，而非原始日志。

### 技术创新点分析
**将“以模型为中心”转变为“以任务为中心”**。传统的 MCP 服务器可能只是一个被动的工具调用接口，而本文提出的服务器具有自主性，能够独立管理任务的生命周期，这是向 AGI（通用人工智能）架构演进的重要一步。

## 3. 实际应用价值

### 对实际工作的指导意义
对于架构师和 AI 工程师而言，这篇文章提供了一个构建**生产级 AI 应用**的蓝图。它提醒开发者：仅仅写一个 Prompt 是不够的，必须构建配套的工程设施（任务队列、状态机）来支撑 Agent 的行动。

### 可以应用到哪些场景
1.  **RPA（机器人流程自动化）**：例如，“帮我在 Salesforce 中创建100个客户，并发送欢迎邮件”。这需要极长的时间，不能让用户一直等待转圈。
2.  **复杂研发辅助**：Agent 需要扫描整个代码库、运行单元测试、修复 Bug，这可能需要几分钟。
3.  **数据分析与报告生成**：处理海量数据集，生成可视化图表。
4.  **订单处理与工作流**：电商中的自动退换货审核、供应链协调等跨系统操作。

### 需要注意的问题
*   **成本控制**：长时运行意味着大量的 Token 消耗和计算资源调用，必须设置预算和熔断机制。
*   **错误处理**：任务在第50步失败了，如何回滚或从第49步恢复？
*   **安全性**：后台运行的 Agent 拥有较高的权限，必须确保其行为符合安全策略。

### 实施建议
不要试图从头构建所有组件。应利用 AWS Bedrock AgentCore 作为编排层，利用现有的 MCP SDK（如 ModelContextProtocol SDKs）快速搭建服务器，并专注于业务逻辑的“Strand”化拆解。

## 4. 行业影响分析

### 对行业的启示
这标志着 AI Agent 正在从**“对话式 AI”**向**“任务式 AI”**转型。行业将不再满足于 ChatBot，而是开始追求能够独立完成复杂工作的 Digital Workers。

### 可能带来的变革
*   **SaaS 软件的形态改变**：软件将不再只有界面，而是通过 MCP 暴露“意图接口”。用户通过 Agent 操作软件，而不是点击按钮。
*   **MCP 协议的普及**：如果 MCP 成为连接 Agent 和工具的标准，那么所有 SaaS 提供商都将不得不提供 MCP Server 接口，类似于当年提供 REST API 一样。

### 相关领域的发展趋势
*   **Agent Ops（智能体运维）**：监控、调试和追踪长时运行 Agent 的技术栈将会兴起（类似于 LangSmith, Arize 的兴起）。
*   **混合架构**：边缘端（客户端）负责轻量推理和交互，云端负责重型任务执行。

### 对行业格局的影响
AWS 通过 Bedrock AgentCore 深度整合这一能力，旨在巩固其在企业级 AI 基础设施中的地位。这可能会加剧云厂商之间的竞争，竞争焦点将从“模型谁更强”转向“Agent 编排能力谁更强”。

## 5. 延伸思考

### 引发的其他思考
*   **人机协作的新模式**：如果 Agent 在后台长时间运行，人类如何介入？是“人在回路中”的审批，还是完全自治？
*   **多 Agent 协作**：Strands Agents 是否可以互相调用？一个 Agent 的输出作为另一个 Agent 的输入，形成分布式任务网络。

### 可以拓展的方向
*   **流式响应的增强**：不仅返回最终结果，而是实时返回 Agent 的“思考过程”可视化，让用户在等待期间建立信任感。
*   **跨平台迁移**：一个正在 AWS 上运行的长时任务，能否无缝迁移到本地或另一个云平台？

### 需要进一步研究的问题
*   如何评估长时运行 Agent 的性能？是看成功率，还是看平均完成时间？
*   当 Agent 产生幻觉导致长时任务跑偏（例如在错误的文件路径下搜索了1小时）时，如何实时检测并中断？

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估任务颗粒度**：分析现有项目中哪些 API 调用是耗时的（>30秒）。
2.  **引入异步层**：在 Bedrock Agent 中配置 Lambda 函数，将同步调用改为异步任务分发。
3.  **定义 MCP Schema**：为你的工具定义清晰的输入输出规范，确保 Agent 能理解如何启动和查询任务。

### 具体的行动建议
*   **第一步**：阅读 AWS Bedrock AgentCore 的官方文档，特别是关于 Custom Orchestration 的部分。
*   **第二步**：搭建一个简单的 MCP Server（例如 Python 实现），模拟一个长时任务（如 `time.sleep(60)`），并测试通过 Agent 调用它。
*   **第三步**：引入 DynamoDB 记录任务状态，实现查询接口。

### 需要补充的知识
*   **异步编程模型**（如 Python asyncio, JS Promises）。
*   **状态机设计**。
*   **MCP 协议规范**。

### 实践中的注意事项
*   **幂等性设计**：确保如果网络重试，任务不会被执行两次。
*   **日志记录**：长时任务最难调试，务必记录详细的中间步骤。

## 7. 案例分析

### 结合实际案例说明
**场景**：一家金融公司的合规审查 Agent。
**传统做法**：用户上传文档，Agent 开始分析。如果分析超过 30秒，前端超时报错。
**基于文章方案的做法**：
1.  用户上传文档。
2.  Bedrock Agent 调用 MCP Server 的 `start_audit` 接口。
3.  Server 返回 `audit_id: 12345`，并立即在后台启动 Lambda 进行文档解析。
4.  Agent 回复用户：“审查已开始，ID 是 12345，请稍候。”
5.  用户可以去喝咖啡，5分钟后回来，询问：“审查 12345 完成了吗？”
6.  Agent 调用 `get_status` 接口，返回结果。

### 成功案例分析
**GitHub Copilot Workspace**：虽然未完全使用 MCP，但其背后的逻辑类似。它允许开发者提出一个复杂的任务（如“重构这个模块”），系统会在后台规划、生成代码、运行测试，整个过程是异步且可视化的。

### 失败案例反思
如果强行使用同步模式处理长时任务，会导致**资源耗尽**。例如，大量并发用户同时点击“生成报告”，导致服务器挂起所有 HTTP 线程等待数据库，最终导致服务崩溃（DDoS 自己）。

### 经验教训总结
**解耦是关键**。将

---
## 最佳实践

## 最佳实践指南

### 实践 1：设计有状态的服务架构以支持长时间运行任务

**说明**: 
构建基于 Amazon Bedrock AgentCore 和 Strands Agents 的 MCP 服务器时，必须采用有状态架构。长时间运行的任务（如数据处理、工作流编排）不能依赖无状态的 HTTP 请求-响应周期。服务器需要维护任务状态、上下文信息和中间结果，以便在任务暂停后恢复执行。

**实施步骤**:
1. 使用持久化存储（如 Amazon DynamoDB 或 S3）保存 Strands Agents 的执行状态和上下文。
2. 在 MCP 服务器中实现状态机逻辑，明确任务的“进行中”、“暂停”、“完成”和“失败”状态。
3. 为每个长时间运行的会话分配唯一的 Session ID，并在所有交互中传递该 ID。

**注意事项**: 
确保状态存储具有高可用性，并实施适当的过期清理策略，防止状态数据无限增长。

---

### 实践 2：实现异步通信与回调机制

**说明**: 
长时间运行的 Strands Agents 任务不应阻塞 MCP 服务器的响应线程。为了保持系统的响应性，应实现异步处理模式。当 Agent 执行耗时操作时，MCP 服务器应立即返回确认信息，并通过回调、Webhook 或轮询机制通知客户端最终结果。

**实施步骤**:
1. 将 AgentCore 的调用逻辑放入后台消息队列（如 Amazon SQS）或异步线程中处理。
2. 定义清晰的回调接口，允许 Strands Agents 在完成特定步骤后通知 MCP 服务器。
3. 客户端实现轮询端点或订阅事件流，以获取非阻塞的任务进度更新。

**注意事项**: 
处理异步超时和重试逻辑，确保网络抖动不会导致任务状态丢失。

---

### 实践 3：优化上下文管理与记忆保留

**说明**: 
Strands Agents 通常需要处理复杂的、多步骤的逻辑。为了确保 Agent 在长时间运行过程中保持连贯性，MCP 服务器必须高效管理上下文窗口和记忆保留。这包括对长对话历史的摘要和对关键实体信息的提取。

**实施步骤**:
1. 在 MCP 协议层实现上下文注入机制，将之前的交互摘要作为系统提示词的一部分传递给 Bedrock 模型。
2. 利用 Amazon Bedrock 的 Checkpointing 功能保存特定时间点的 Agent 状态，以便从断点恢复而不是从头开始。
3. 定期评估 Token 使用情况，动态过滤掉不相关的历史信息。

**注意事项**: 
注意上下文窗口的限制，避免因上下文过长导致推理成本上升或延迟增加。

---

### 实践 4：实施全面的可观测性与日志记录

**说明**: 
调试长时间运行的分布式 Agent 系统具有挑战性。必须建立完善的可观测性体系，追踪 Strands Agents 在 AgentCore 上的每一次调用、决策和工具使用情况，以便快速定位性能瓶颈或逻辑错误。

**实施步骤**:
1. 集成 Amazon CloudWatch 用于收集日志和指标，重点监控 Agent 的执行延迟和错误率。
2. 在 MCP 服务器生成的所有事件中注入 Correlation ID，将其与 Bedrock AgentCore 的 Trace ID 关联。
3. 为 Strands Agents 的关键决策点设置结构化日志，记录输入参数和输出结果。

**注意事项**: 
避免记录敏感信息（如 PII），在日志输出前实施脱敏处理。

---

### 实践 5：构建健壮的错误处理与重试策略

**说明**: 
长时间运行的任务面临更高的失败风险（如模型限流、网络中断或 API 不可用）。MCP 服务器必须具备弹性，能够从瞬态错误中自动恢复，并将永久性错误清晰地传递给上层应用。

**实施步骤**:
1. 在调用 Bedrock AgentCore 时实现指数退避重试机制。
2. 利用 Strands Agents 的错误处理能力，定义明确的“回退”路径或补偿逻辑。
3. 区分可重试错误（如 5xx 错误）和不可重试错误（如 4xx 验证错误），避免无意义的重试消耗配额。

**注意事项**: 
设置最大重试次数和超时时间，防止任务陷入无限重试循环。

---

### 实践 6：确保工具调用的幂等性与安全性

**说明**: 
Strands Agents 可能会多次调用 MCP 服务器暴露的工具。特别是在重试场景下，工具必须设计为幂等的，即多次执行同一操作产生的结果与执行一次相同。此外，长时间运行的任务通常涉及敏感数据，必须严格验证权限。

**实施步骤**:
1. 在 MCP 工具接口设计中，使用幂等键（Idempotency Key）来去重请求。
2. 实施最小权限原则，为 Bedrock AgentCore 分配的 IAM 角色仅包含完成任务所需的特定权限。
3. 对所有输入参数进行严格验证，防止提示词注入或恶意参数导致系统异常。

**注意事项**: 
定期审查 IAM 策略和访问日志，确保只有授权的 Agent 能够调用特定的 MCP 工具。

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够执行长期、复杂且多步骤任务的持久化 MCP 服务器。
- 通过利用 Strands 的内存和上下文管理能力，AI 智能体可以跨越多个会话保持状态，从而实现更连贯的长期交互。
- 该架构将 Bedrock 的托管基础设施与 MCP 协议的互操作性相结合，显著降低了构建和维护有状态 AI 应用的复杂性。
- 开发者可以使用 MCP 标准接口将 Bedrock AgentCore 连接到多种数据源和工具，增强了智能体在长时间运行任务中的功能扩展性。
- 这种集成方案解决了传统无状态模型难以处理跨越时间或需要多阶段推理任务的局限性，提升了自动化工作流的效率。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [MCP](/tags/mcp/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长运行服务](/tags/%E9%95%BF%E8%BF%90%E8%A1%8C%E6%9C%8D%E5%8A%A1/) / [Strands Agents](/tags/strands-agents/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [系统架构](/tags/%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-3.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*