---
title: "在Amazon Bedrock AgentCore上构建长时运行的MCP服务器"
date: 2026-02-15T21:22:14+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长时运行", "AI 代理", "上下文消息"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon Bedrock AgentCore 上结合 Strands Agents 集成，构建能够长时间运行的 MCP（Model Context Protocol）服务器。为实现这一目标，文章提出了一套包含三大核心策略的综合方法： 1. **上下文消息策略**：引入了一种机制，用于在执行长时间操"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 在Amazon Bedrock AgentCore上构建长时运行的MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供了一种实现这一目标的综合方法。首先，我们介绍一种上下文消息策略，以便在长时间运行的操作期间保持服务器与客户端之间的持续通信。接着，我们构建一个异步任务管理框架，使您的 AI 代理能够启动长时间运行的进程，而不会阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合，打造生产级的 AI 代理，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是迈向生产级应用的关键一步，但这往往面临着上下文管理与服务响应性的双重挑战。本文将详细介绍一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的综合解决方案，通过上下文消息策略与异步任务管理框架，确保服务器与客户端在复杂操作期间的持续通信。阅读本文，您将掌握如何构建稳健的系统架构，从而让您的 AI 代理可靠地执行耗时任务且不阻塞其他操作。

---
## 摘要

本文介绍了如何在 Amazon Bedrock AgentCore 上结合 Strands Agents 集成，构建能够长时间运行的 MCP（Model Context Protocol）服务器。为实现这一目标，文章提出了一套包含三大核心策略的综合方法：

1.  **上下文消息策略**：引入了一种机制，用于在执行长时间操作期间，维持服务器与客户端之间的持续通信，确保连接不中断。
2.  **异步任务管理框架**：开发了一套框架，允许 AI 代理启动耗时较长的后台进程，而不会阻塞其他操作的执行，从而提高系统的并发处理能力。
3.  **生产级集成实施**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 结合，打造出可靠、能够处理复杂且耗时任务的生产级 AI 代理。

总结来说，通过这些技术手段，开发者可以构建出既具备长时间运行能力，又能保持系统稳定性和响应速度的 AI 代理解决方案。

---
## 评论

### 文章评价报告

**文章标题：** Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration

#### 1. 中心观点
文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的集成架构，旨在通过引入“上下文消息策略”和“异步任务管理框架”，解决模型上下文协议（MCP）服务器在处理长周期任务时的状态保持与通信中断问题。

#### 2. 深入分析与评价

**支撑理由（事实陈述 + 作者观点）：**

1.  **架构层面的必要补位（技术深度）：**
    *   **事实陈述：** 现有的 LLM 交互大多遵循同步的 Request-Response 模式，受限于网络超时和 Token 输出时长，难以直接处理耗时数分钟甚至数小时的任务（如大规模数据处理或复杂代码编译）。
    *   **作者观点：** 文章提出的“异步任务管理框架”是对 Bedrock AgentCore 能力的关键扩展。它将 Agent 的职责从“执行者”转变为“调度者”，通过解耦任务接收与结果返回，使得 LLM 能够在有限的上下文窗口内管理跨越长时间维度的业务逻辑。这种设计模式在技术上具有严谨性，符合现代分布式系统中“最终一致性”的设计理念。

2.  **上下文连续性的创新解法（创新性）：**
    *   **你的推断：** 文章提到的“上下文消息策略”可能利用了 Strands Agents 的记忆机制或 Bedrock 的长期记忆服务。
    *   **作者观点：** 这是一个高价值的创新点。传统的长任务处理往往依赖客户端轮询，体验割裂。通过在服务端维持上下文心跳，并允许 MCP Server 在任务完成后主动“回调”或更新状态，系统实现了对话流的连续性。这种方法不仅提升了用户体验，还降低了客户端实现的复杂度。

3.  **对 MCP 生态的工业化落地（实用价值）：**
    *   **事实陈述：** MCP (Model Context Protocol) 正在成为连接 AI 与数据工具的标准协议，但目前缺乏关于生产级高可用部署的官方最佳实践。
    *   **作者观点：** 文章将 Bedrock 的企业级托管能力与 MCP 的轻量级协议相结合，提供了一条从“原型演示”走向“生产环境”的清晰路径。对于开发者而言，直接利用 AWS 的基础设施来承载 MCP Server，避免了自行维护 WebSocket 连接池和消息队列的繁琐工作，具有极高的实用价值。

**反例与边界条件（批判性思考）：**

1.  **成本与延迟的权衡（边界条件）：**
    *   **你的推断：** 虽然异步框架解决了长任务问题，但引入 AgentCore 和额外的异步消息队列（如 SQS/EventBridge）必然增加系统延迟和基础设施成本。
    *   **反例：** 对于简单的、毫秒级完成的工具调用（如查询天气、简单计算），引入这套复杂的异步框架属于“过度设计”。额外的网络跳转可能导致响应时间增加 100ms 以上，这在实时性要求极高的场景下是不可接受的。

2.  **状态一致性的最终挑战（争议点）：**
    *   **作者观点：** 文章似乎假设上下文消息能够完美同步。
    *   **反例/风险：** 在分布式系统中，网络分区或服务重启是常态。如果 AgentCore 在任务执行期间崩溃，或者上下文消息丢失，如何保证 MCP Server 的状态与 Agent 的认知一致？文章摘要未详细阐述“幂等性”和“故障恢复”机制，这是长任务系统中最容易出故障的地方。

3.  **厂商锁定的风险（行业影响）：**
    *   **事实陈述：** 该方案深度依赖 Amazon Bedrock AgentCore 和 Strands Agents。
    *   **反例：** 如果企业希望未来迁移到 Azure OpenAI 或本地部署的 LLM，这种深度耦合特定云厂商元语法的架构将带来极高的迁移成本。

#### 3. 综合维度评分

*   **内容深度：** **高**。触及了 Agent 架构中最难处理的“长任务”痛点，没有停留在简单的 API 调用层面，而是深入到了异步编排和生命周期管理。
*   **实用价值：** **高**。对于正在使用 AWS 技术栈构建 AI 应用的架构师和开发者来说，这是一份不可多得的实操指南。
*   **创新性：** **中**。虽然异步任务模式在传统软件工程中很常见，但在 LLM Agent 领域，将其与 MCP 协议结合并标准化是一种值得肯定的工程化创新。
*   **可读性：** **优**（基于摘要推断）。结构清晰，先讲策略（Context），再讲框架，逻辑递进合理。
*   **行业影响：** **中**。它推动了 MCP 协议在企业级应用中的标准化，但也可能加剧 AWS 生态的技术壁垒。

#### 4. 可验证的检查方式

为了验证文章所述方案的有效性，建议在实际测试中关注以下指标：

1.  **任务超时突破验证（实验）：**
    *   **操作：** 构建一个耗时超过 5 分钟的 MCP 工具调用（例如视频渲染或大文件 RAG 索引）。
    *   **观察窗口：** 观察 Agent 是否在任务期间保持连接不中断，且客户端是否收到中间状态更新，而非直接抛出 504 Gateway Timeout 错误。

2.  **状态一致性测试（指标）：**
    *   **操作：** 在任务执行过程中人为重启 AgentCore 实例或中断网络连接。
    *   **检查

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

## 1. 核心观点深度解读

**文章的主要观点**
文章提出了一种在 Amazon Bedrock AgentCore 环境下构建**长期运行**的 MCP（Model Context Protocol）服务器的综合解决方案。其核心在于解决传统 AI 代理在面对耗时任务（如数据处理、复杂编排）时容易遇到的超时和中断问题。

**作者想要传达的核心思想**
AI 代理不应仅限于“请求-响应”式的短对话，而应具备处理**复杂、多步骤、长周期业务流程**的能力。通过结合 **Strands Agents**（一种具备状态管理和长时间运行能力的代理架构）与 **MCP**，可以实现客户端与服务器之间在任务执行期间的**持续上下文感知**，而不是让用户面对漫长的加载等待。

**观点的创新性和深度**
*   **从“同步等待”转向“异步流式交互”**：传统做法是等待 Agent 完成所有步骤后返回结果，这受限于 LLM 的上下文窗口和超时机制。本文的创新点在于引入了“上下文消息策略”和“异步任务管理”，将任务执行与用户交互解耦。
*   **深度集成**：将开源的 MCP 协议标准与 Amazon Bedrock 的托管能力结合，填补了通用协议与云端高性能执行环境之间的鸿沟。

**为什么这个观点重要**
随着企业级 AI 应用的深入，简单的问答已无法满足需求。企业需要 AI 能够执行 RPA（机器人流程自动化）、数据分析等耗时操作。如果无法解决长连接和状态保持问题，AI 代理将难以落地到核心业务流中。本文提供的方法论是 AI Agent 从“玩具”走向“工具”的关键一步。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **MCP (Model Context Protocol)**：一种开放协议，用于连接 AI 应用与数据源。在此文中，它被扩展为支持长连接的服务端实现。
*   **Amazon Bedrock AgentCore**：AWS 提供的构建代理的基础设施，负责编排 LLM 和工具。
*   **Strands Agents**：这是文章的技术核心（推测为 AWS 内部或特定合作伙伴的框架/概念，Strands 通常指代具有连续性的线程或链）。它代表了具备持久化记忆和任务拆解能力的 Agent 架构。
*   **异步任务管理框架**：用于处理非阻塞操作的后台机制。

**技术原理和实现方式**
1.  **上下文消息策略**：
    *   **原理**：在长任务运行期间，服务器不保持 HTTP 连接打开，而是通过特定的消息通道（如 WebSocket 或轮询机制）定期发送“心跳”或“中间状态更新”。
    *   **实现**：MCP 服务器不仅返回最终结果，还返回 `TaskId` 和状态标识。客户端根据此 ID 查询进度或接收推送。
2.  **异步任务管理**：
    *   **原理**：当 Bedrock Agent 调用 MCP 工具时，MCP 服务器立即返回一个“任务已接收”的确认，随后在后台异步执行实际工作。
    *   **实现**：利用 AWS Lambda 或容器（ECS/EKS）配合消息队列（SQS）或状态机（Step Functions）来驱动长流程。

**技术难点和解决方案**
*   **难点**：LLM 的会话通常是幂等的，但长任务是有状态的。如何让 LLM 在任务完成后“回忆”起之前的上下文？
*   **解决方案**：通过 Strands Agents 集成，将任务的中间状态持久化存储（如 DynamoDB），并在下一次交互时将状态作为上下文注入回 LLM。
*   **难点**：超时控制。
*   **解决方案**：MCP 服务器实现与 Bedrock 的超时配置解耦，服务器端处理长任务，Bedrock 仅负责逻辑判断和状态轮询。

**技术创新点分析**
最大的创新在于 **MCP 协议的“有状态化”改造**。标准的 MCP 往往是无状态的查询，而本文通过 Strands Agents 赋予了 MCP 协议处理“事务”的能力，使其能够支持类似数据库 ACID 特性中的原子性和持久性在业务逻辑层面的实现。

## 3. 实际应用价值

**对实际工作的指导意义**
对于正在开发企业级 AI 应用的架构师和开发者，这篇文章提供了一套避免“轮子重新发明”的蓝图。它指导我们如何利用 AWS 的托管服务来构建复杂的 Agent 系统，而不是自己从零搭建 WebSocket 服务器和状态管理库。

**可以应用到哪些场景**
*   **金融报告生成**：需要几分钟来获取数据、分析、渲染图表的场景。
*   **企业级 RPA**：如自动处理报销单，涉及跨系统审批，耗时数小时甚至数天。
*   **代码生成与部署**：Agent 生成代码后，需要进行漫长的 CI/CD 流程，需要实时向用户反馈构建日志。
*   **科学研究辅助**：进行长时间的模拟运算或数据清洗。

**需要注意的问题**
*   **成本控制**：长轮询或保持 Strands Agents 活跃可能会产生更高的 API 调用费用和计算成本。
*   **状态一致性**：在分布式环境下，确保 MCP 服务器状态与 Bedrock Agent 认知状态的同步是极具挑战的。

**实施建议**
在设计系统时，应明确区分“交互层”和“执行层”。交互层负责快速响应用户，执行层（MCP Server + Strands）负责慢速处理。建议使用 Step Functions 来编排 MCP 后端的长时间运行逻辑。

## 4. 行业影响分析

**对行业的启示**
这标志着 AI Agent 基础设施正在向**“云原生化和标准化”**迈进。MCP 作为新兴标准，其与 AWS Bedrock 的深度整合意味着“协议即服务”的趋势。行业将更加关注如何让 AI 具备“行动力”而非仅仅是“理解力”。

**可能带来的变革**
*   **SaaS 软件的智能化升级**：SaaS 软件可以通过暴露 MCP 接口，无缝接入企业的 Bedrock Agent，实现长时间的自动化操作。
*   **Agent 即服务**：未来可能出现专门出租“长运行 Agent”的服务商。

**相关领域的发展趋势**
*   **协议统一**：MCP 可能成为连接 LLM 与企业工具的事实标准。
*   **混合架构**：边缘计算（快速响应）与云端计算（复杂推理）的结合将更加紧密。

## 5. 延伸思考

**引发的其他思考**
如果 MCP 服务器可以长运行，那么安全性如何保障？长时间运行的通道是否更容易受到攻击？此外，Strands Agents 的引入是否会增加 Vendor Lock-in（厂商锁定）的风险？

**可以拓展的方向**
*   **多 Agent 协作**：基于此架构，多个 Strands Agents 如何在同一个长任务中协作？
*   **人机协同**：在长任务执行的关键节点（如支付前），如何优雅地插入人工确认环节？

**需要进一步研究的问题**
Strands Agents 的具体实现细节是否开源？它与 LangChain 的 LangGraph 或微软的 AutoGen 在长任务处理上的性能对比如何？

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有架构**：检查现有的 AI 应用是否存在“长任务阻塞”问题。
2.  **引入异步模式**：改造现有的 Tool 调用逻辑，将其从同步改为异步（返回 TaskID）。
3.  **搭建 MCP Server**：使用官方 SDK 构建一个简单的 MCP Server，并将其部署在 AWS Fargate 或 Lambda 上。

**具体的行动建议**
*   阅读 MCP 协议规范，特别是关于资源引用和提示部分。
*   在 Bedrock Agent 中配置一个简单的 Action Group，指向一个异步的 Lambda 函数模拟长任务。
*   构建前端轮询逻辑，根据返回的 TaskID 查询状态。

**需要补充的知识**
*   **异步编程模型**：理解 Promise, Future, async/await 以及消息队列模式。
*   **Amazon Bedrock Knowledge Base**：了解如何将私有数据注入以辅助长任务决策。
*   **状态机设计**：学习 Step Functions 的设计模式。

## 7. 案例分析

**结合实际案例说明**
假设一个**企业合规审查 Agent**。
*   **传统模式**：用户上传文档，Agent 转圈 3 分钟，如果超时则报错，用户体验极差。
*   **基于本文的模式**：
    1.  用户上传文档。
    2.  Bedrock Agent 调用 MCP Server。
    3.  MCP Server 返回 `TaskID: 101`，状态 `Processing`。
    4.  Bedrock 响应用户：“文档已接收，正在审查，ID: 101”。
    5.  后台 Strands Agent 逐页分析文档，并通过上下文消息更新进度（如“已分析 50%”）。
    6.  用户可以随时询问：“101 号任务现在怎么样了？”
    7.  任务完成后，Agent 主动通知用户并生成报告。

**成功案例分析**
类似 **Klarna** 的客服助手或 **Devin**（AI 软件工程师），它们都具备长任务处理能力。Devin 可以通过 SSH 连接环境、运行代码、等待构建，这正是 Strands Agents 所追求的能力。

**失败案例反思**
早期的 ChatGPT 插件往往因为超时或无法反馈中间进度而失败。例如，订票插件在查询航班时如果超过 30 秒没反应，用户就会关闭页面。本文提出的架构正是为了解决此类痛点。

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级 AI Agent 时，采用 **基于 MCP 协议并结合 Strands Agents 的异步长运行架构**，是实现复杂业务流程自动化和提升用户体验的**必要且充分条件**（优于传统同步架构）。

**支撑理由与依据**
1.  **理由一：用户体验的连续性**
    *   *依据*：心理学研究表明，超过 2 秒的延迟会显著降低用户满意度。长任务如果不解耦，必然导致超时。
    *   *直觉*：没有人愿意盯着转圈等待 5 分钟。
2.  **理由二：系统鲁棒性与可扩展性**
    *   *依据*：云原生架构模式（如 SQS + Lambda）证明了异步处理能有效应对流量洪峰，防止系统崩溃。
    *   *直觉*：将“接单”和“做菜”分开，餐厅效率更高。
3.  **理由三：上下文感知的准确性**
    *   *依据*：LLM 受限于上下文窗口。Strands Agents 通过外部记忆存储中间状态，使得 LLM 可以随时“唤醒”并继续任务，而不需要将所有历史重新加载。

**反例或边界条件**
1.  **反例：极度简单的查询任务**
    *   对于“现在几点了？”或“翻译这句话”，引入异步架构和 Strands Agents 是过度设计，增加了延迟和复杂度。
2.  **边界条件：强一致性要求**
    *   如果业务要求在毫秒级内获得事务结果（如高频交易扣款），异步的最终一致性模型可能不适用，除非配合复杂的锁机制。

**事实与价值判断**
*   **事实**：MCP 是一个开放协议；Bedrock 支持 Agent 开发；长任务会导致 HTTP

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 MCP 服务器的无状态设计

**说明**:
长期运行的 MCP 服务器必须具备高可用性和快速恢复能力。无状态设计确保服务器实例可以独立于任何特定会话运行，使得在负载增加时能够无缝扩展，或在故障发生时快速重启，而不会丢失上下文信息或中断正在进行的任务流。

**实施步骤**:
1. 将所有会话状态、上下文变量和中间数据存储在外部持久化存储中（如 Amazon DynamoDB 或 S3），而不是保存在服务器内存中。
2. 确保每个请求都包含恢复处理所需的所有必要上下文信息。
3. 实现幂等性处理逻辑，以便在重试时不会产生副作用。

**注意事项**:
避免在服务器实例内存中缓存用户特定的数据。如果必须使用缓存，请确保使用分布式缓存机制（如 ElastiCache），并设置适当的过期时间。

---

### 实践 2：实施严格的超时与重试策略

**说明**:
由于 AgentCore 和 Strands Agents 涉及多轮对话和外部工具调用，网络延迟或服务不可用可能导致请求挂起。为了防止资源耗尽并保持响应速度，必须为所有 MCP 工具调用配置明确的超时限制，并配合指数退避算法进行智能重试。

**实施步骤**:
1. 为每个 MCP 工具定义明确的超时阈值（例如，简单查询 5 秒，复杂处理 30 秒）。
2. 在客户端（Agent 侧）和 MCP 服务器侧同时实施超时处理。
3. 配置自动重试机制，使用指数退避策略（例如，首次重试等待 1 秒，第二次 2 秒，以此类推），并设置最大重试次数（如 3 次）。

**注意事项**:
对于非幂等操作（如写入数据库或发送邮件），重试需谨慎，确保不会导致数据重复。对于长时间运行的异步任务，应返回任务 ID 并提供状态查询接口，而不是保持连接等待。

---

### 实践 3：利用 Strands Agents 进行上下文感知的流式处理

**说明**:
Strands Agents 允许将复杂的任务分解为多个子任务。在 Bedrock AgentCore 中集成 MCP 服务器时，应利用流式传输来提供即时反馈，特别是在处理耗时较长的操作时。这可以显著改善用户体验，避免用户在面对长时间空白等待时感到困惑。

**实施步骤**:
1. 在 MCP 服务器接口中启用流式响应模式（Server-Sent Events 或 WebSocket）。
2. 将长任务分解为多个步骤，每个步骤完成后立即发送部分结果或状态更新。
3. 在 AgentCore 层面配置 Strands Agents 以处理和聚合这些流式事件，形成连贯的最终回复。

**注意事项**:
确保流式输出的格式与 Bedrock Agent 的期望一致。需要在客户端处理流结束的异常情况，防止因连接中断导致用户只收到部分信息。

---

### 实践 4：集中式日志记录与可观测性集成

**说明**:
在分布式架构中，调试长期运行的服务器极具挑战性。必须将 MCP 服务器的日志、指标和追踪数据与 AWS 的可观测性服务（如 CloudWatch 和 X-Ray）集成，以便实时监控性能瓶颈并快速排查故障。

**实施步骤**:
1. 使用统一的日志格式（如 JSON），并包含 `request_id`、`session_id` 和 `tool_name` 等关键关联字段。
2. 将应用程序日志直接发送到 Amazon CloudWatch Logs。
3. 启用 AWS X-Ray 追踪，以可视化请求从 AgentCore 到 MCP 服务器再到后端服务的完整路径。

**注意事项**:
避免记录敏感信息（PII），如用户密码或个人身份信息。在日志输出前实施脱敏处理。注意控制日志体量，以免产生高昂的 CloudWatch 费用。

---

### 实践 5：建立细粒度的访问控制与安全隔离

**说明**:
MCP 服务器通常作为连接器访问后端敏感数据或 API。必须实施最小权限原则，确保 Bedrock Agent 只能调用其完成任务所需的特定工具，并且每个工具调用都经过严格的身份验证和授权。

**实施步骤**:
1. 使用 AWS IAM 定义精细的角色策略，限制 MCP 服务器只能访问特定的 S3 存储桶、DynamoDB 表或外部 API 端点。
2. 在 MCP 服务器层实现 API 密钥验证或基于 JWT 的令牌验证，确保只有来自 Bedrock AgentCore 的有效请求才能通过。
3. 利用 VPC Endpoint 将 MCP 服务器部署在私有网络中，隔离公共互联网访问。

**注意事项**:
定期轮换 API 密钥和 IAM 凭证。不要在代码中硬编码任何凭证，使用 AWS Secrets Manager 或 Systems Manager Parameter Store 存储配置。

---

### 实践 6：异步处理与任务队列管理

**说明**:
对于执行时间超过 Bedrock Agent 超时限制（通常为几分钟）的繁重任务，同步调用会导致失败。最佳实践是采用异步模式：MCP

---
## 学习要点

- Amazon Bedrock AgentCore 正式支持集成 Strands Agents，允许开发者构建能够执行长期、多步骤复杂任务的自主智能体。
- 通过将 Strands Agents 的持久化记忆与状态管理能力集成到 Bedrock，解决了传统无状态模型在处理长周期工作流时的上下文丢失问题。
- 借助 Bedrock 的托管基础设施，开发者无需维护底层服务器，即可轻松构建和运行高可用的 MCP（Model Context Protocol）服务器。
- 该集成方案显著增强了智能体处理复杂工作流的能力，使其能够跨越较长时间跨度自主协调和完成任务。
- 利用 MCP 协议的标准化特性，新架构促进了不同 AI 系统与工具之间的无缝互操作性与数据交换。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [Strands Agents](/tags/strands-agents/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [长时运行](/tags/%E9%95%BF%E6%97%B6%E8%BF%90%E8%A1%8C/) / [AI 代理](/tags/ai-%E4%BB%A3%E7%90%86/) / [上下文消息](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E6%B6%88%E6%81%AF/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-8.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-10.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器与异步任务管理]({{< relref "posts/20260214-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-9.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*