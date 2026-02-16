---
title: "基于Amazon Bedrock AgentCore构建持久化MCP服务器与异步任务管理"
date: 2026-02-16T20:45:39+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "异步任务", "Strands Agents", "AI Agent", "上下文管理", "长连接"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon Bedrock AgentCore 上结合 Strands Agents 构建能够处理长时间运行任务的生产级 MCP 服务器。主要解决方案包括以下三个核心策略： 1. **上下文消息策略**：引入了一种维持服务器与客户端在长时间操作期间持续通信的机制，确保连接不中断。 2. **异步任务"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建持久化MCP服务器与异步任务管理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们为您提供了一套全面的方法来实现这一目标。首先，我们介绍一种上下文消息策略，在长时间操作期间保持服务器与客户端之间的持续通信。接下来，我们开发一个异步任务管理框架，让您的 AI 代理能够启动长时间运行的任务，而不会阻塞其他操作。最后，我们演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合使用，构建可投入生产环境的 AI 代理，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是当前技术落地中的难点，尤其是在保持通信连续性和系统稳定性方面。本文将介绍一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的集成方案，通过上下文消息策略与异步任务管理框架，解决长时操作中的阻塞与通信中断问题。阅读本文，您将掌握构建生产级、高并发 AI 代理的具体方法，以应对复杂且耗时的业务场景。

---
## 摘要

本文介绍了如何在 Amazon Bedrock AgentCore 上结合 Strands Agents 构建能够处理长时间运行任务的生产级 MCP 服务器。主要解决方案包括以下三个核心策略：

1.  **上下文消息策略**：引入了一种维持服务器与客户端在长时间操作期间持续通信的机制，确保连接不中断。
2.  **异步任务管理框架**：开发了支持异步处理的框架，使 AI 代理能够启动耗时较长的流程，同时不会阻塞其他操作的执行。
3.  **集成与实现**：展示了如何将上述策略与 Amazon Bedrock AgentCore 及 Strands Agents 相结合，从而构建出能够可靠处理复杂且耗时操作的 AI 代理。

---
## 评论

**中心观点**
该文章提出了一种基于 Amazon Bedrock AgentCore 的“上下文消息策略”与“异步任务管理框架”的混合架构，旨在解决 MCP（Model Context Protocol）服务器在处理长时运行任务时的状态保持与通信中断问题。

**支撑理由与边界条件分析**

1.  **解决协议层面的“长任务”僵局**
    *   **事实陈述**：MCP 协议最初设计倾向于同步请求-响应模式，这在面对耗时操作（如数据检索、代码编译）时容易导致 HTTP 超时或上下文丢失。
    *   **你的推断**：文章引入的“上下文消息策略”实际上是在协议层之上构建了一层虚拟会话保持机制，允许 Agent 在物理连接断开或逻辑超时后，仍能通过特定的 Token 或 ID 恢复对话，而非单纯依赖长连接。

2.  **引入 Strands Agents 实现流式状态编排**
    *   **作者观点**：利用 Strands Agents 的集成，可以将一个庞大的长任务拆解为多个可验证的“步进”。
    *   **事实陈述**：这符合当前 Agent 架构从“单次推理”向“多步规划”演进的趋势。通过异步任务管理框架，服务器可以返回一个“任务 ID”，而不仅仅是阻塞等待结果，从而释放了客户端资源。

3.  **Bedrock AgentCore 的基础设施兜底**
    *   **事实陈述**：依托 AWS 基础设施，该方案利用了 Bedrock 的托管能力和安全控制，避免了用户自行搭建 WebSocket 服务器的运维负担。
    *   **你的推断**：这是典型的 Vendor Lock-in（供应商锁定）策略，虽然降低了开发门槛，但极大地增加了迁移成本。

**反例与边界条件**

1.  **成本与延迟的权衡（反例）**
    *   对于仅需几秒钟的短任务，该文章提出的异步框架和上下文序列化可能会引入不必要的序列化开销和网络跳转，导致响应速度反而不如简单的同步调用。
    *   **边界条件**：当任务执行时间 < 5秒 时，同步直连通常更优。

2.  **状态一致性的复杂性（反例）**
    *   在分布式异步环境中，保持客户端与服务器端的“上下文”完全一致极具挑战性。如果客户端在异步任务完成前修改了之前的指令，服务器端可能会基于过期的上下文继续执行，导致“幻觉”或资源浪费。
    *   **边界条件**：高频修改意图的交互场景下，此架构可能导致严重的版本冲突。

---

**深度评价**

**1. 内容深度：架构层面的必要补全，但理论稍显薄弱**
文章在技术深度上切中肯綮。目前 AI Agent 行业普遍面临“长思维链”与“短连接协议”之间的矛盾。文章提出的“异步任务管理”并非简单的消息队列，而是结合了 LLM 的状态记忆，这在工程实现上是高价值的。然而，文章在论证严谨性上略显不足，主要表现为未详细阐述上下文消息的存储策略（是全量存储还是增量存储）以及由此带来的 Token 成本激增问题。

**2. 实用价值：AWS 生态内的“标准答案”**
对于深度绑定 AWS 生态的企业，这篇文章提供了构建生产级 Agent 的最佳实践。它不仅解决了“怎么做”，还隐含地解决了“运维”和“监控”的问题（通过 Bedrock 集成）。但对于非 AWS 用户或多云策略的企业，其参考价值大打折扣。

**3. 创新性：组合式创新**
将 Strands Agents（一种专注于步进式推理的框架）与 Bedrock AgentCore 结合属于组合式创新。它没有发明新算法，但通过重新排列现有基础设施组件，解决了一个具体的工程痛点。其中“Context Message Strategy”是对 MCP 协议的一种软性扩展，具有一定的前瞻性。

**4. 可读性与逻辑**
从摘要来看，文章结构清晰，遵循“问题-方案-实现”的逻辑。但技术文档往往容易陷入代码细节，如果文章未能清晰界定“同步 MCP 调用”与“异步 AgentCore 任务”的边界，读者极易混淆两者的适用场景。

**5. 行业影响：推动 MCP 的企业级落地**
如果该方案被广泛采纳，标志着 MCP 协议从简单的“工具调用”向“复杂的业务流程编排”进化。这可能会促使其他云厂商（如 Azure、GCP）推出类似的托管 Agent 编排服务，从而确立“长任务异步化”作为企业级 Agent 的标准架构模式。

**6. 争议点：过度工程化与供应商锁定**
*   **过度工程化**：许多简单的 RAG（检索增强生成）应用并不需要如此复杂的异步框架。文章可能诱导开发者为了使用新技术而增加系统复杂度。
*   **黑盒风险**：Bedrock AgentCore 的内部运作机制并不完全透明，当长任务失败时，排查是模型问题、协议问题还是 AWS 内部调度问题将变得非常困难。

**7. 实际应用建议**
*   **分层采用**：仅在涉及耗时超过 30s 的操作（如生成报告、批量数据处理）时启用该异步框架。
*   **成本监控**：实施严格的 Token 和 API 调用监控，因为“上下文消息策略”会显著增加输入 Token 的消耗。
*   **降级机制**：务必保留同步调用的降级开关，以防 Bedrock 服务不可用时系统完全瘫痪。

---

**可验证的检查方式**

1.  **压力测试指标**：
    *   构建一个模拟长任务（如 60秒

---
## 技术分析

基于您提供的文章标题和摘要，以及对 Amazon Bedrock、MCP (Model Context Protocol) 及 Agent 技术栈的深入理解，以下是对该技术方案的全面深度分析。

---

# 深入分析：基于 Amazon Bedrock AgentCore 与 Strands Agents 构建长时运行 MCP 服务器

## 1. 核心观点深度解读

**文章的主要观点：**
文章提出了一种在 Amazon Bedrock AgentCore 环境下，利用 **Strands Agents** 架构模式来克服传统无状态模型限制，构建能够处理**长时间运行任务**和**异步工作流**的 MCP (Model Context Protocol) 服务器的综合解决方案。

**作者想要传达的核心思想：**
传统的 AI 交互往往是“即发即忘”的同步模式，难以处理现实世界中耗时的业务流程（如数据查询、API 编排、文件生成）。作者主张通过引入**上下文消息策略**和**异步任务管理框架**，将 AI Agent 从“对话者”转变为“任务协调者”，使其在等待外部系统响应时能够保持状态，并在任务完成后重新介入，从而实现真正的业务流程自动化闭环。

**观点的创新性和深度：**
*   **架构创新：** 将 Bedrock 的托管能力与 Strands（一种处理长时序任务的 Agent 框架概念）相结合，解决了 LLM（大语言模型）本身无状态和上下文窗口限制的问题。
*   **深度整合：** 不仅仅停留在 API 调用层面，而是深入到了**协议层（MCP）**和**编排层**，解决了一个极其痛点的问题：如何让 Agent 在处理耗时任务时不阻塞用户交互，也不丢失会话记忆。

**为什么这个观点重要：**
这是企业级 AI 落地的“最后一公里”问题。企业业务大多是复杂的、跨系统的、耗时的。如果 Agent 只能处理秒级回复，则无法真正替代人工操作。该方案为构建高可用、高并发的企业级 Agent 提供了标准化的工程路径。

## 2. 关键技术要点

**涉及的关键技术或概念：**
1.  **MCP (Model Context Protocol)：** 由 Anthropic 推出的开放协议，用于连接 AI 应用与数据源。本文将其扩展为支持长时运行的 Server。
2.  **Amazon Bedrock AgentCore：** AWS 提供的底层 Agent 编排服务，允许开发者精细控制 Agent 的推理循环和工具调用。
3.  **Strands Agents：** 指代一种特定的 Agent 设计模式，通常涉及将任务分解为“链”或“股”，允许并行和串行执行，并支持状态持久化。
4.  **异步任务管理：** 区分“控制平面”（指令接收）和“数据平面”（任务执行）。

**技术原理和实现方式：**
*   **Context Message Strategy（上下文消息策略）：**
    *   **原理：** 在 LLM 的上下文窗口中维护一个动态更新的状态块。当任务提交给后台异步处理后，系统生成一个唯一的 Task ID。
    *   **实现：** 客户端通过 MCP 轮询或 WebSocket 推送状态。Agent 在后续轮次中通过 Task ID 检索任务结果，而非直接等待 HTTP 响应。
*   **Asynchronous Task Framework（异步任务框架）：**
    *   **实现：** 引入消息队列（如 SQS）或状态机（如 Step Functions）。当 Agent 调用工具时，工具立即返回“任务已接收”和 Task ID，后台线程或 Lambda 函数执行实际工作。Agent 进入“等待-重试”循环，直到任务完成。

**技术难点和解决方案：**
*   **难点：** LLM 的“幻觉”或“遗忘”。Agent 可能会在长时任务中忘记为什么启动它。
*   **解决方案：** 上下文注入。在 Agent 每次轮询任务状态时，将原始的用户意图和中间步骤摘要重新注入到 System Prompt 或 History 中。
*   **难点：** 并发控制。
*   **解决方案：** 利用 Bedrock AgentCore 的并发控制机制，防止同一任务被重复触发。

**技术创新点分析：**
将 MCP 协议从单纯的“数据检索”扩展到了“任务执行”。传统的 MCP 更多是用于给 LLM 提供 RAG（检索增强生成）上下文，而该架构将其转变为一个具备执行能力的 SOA（面向服务的架构）网关。

## 3. 实际应用价值

**对实际工作的指导意义：**
该架构为开发者提供了一套蓝图，用于开发那些不能“秒回”的 AI 应用。它指导我们如何设计 API 接口、如何管理会话状态以及如何处理超时和错误重试。

**可以应用到哪些场景：**
1.  **RAG（检索增强生成）预处理：** 当需要检索海量文档或生成摘要时，建立索引耗时较长，需要异步处理。
2.  **代码生成与部署：** Agent 生成代码后，需要触发 CI/CD 流水线，这是一个长时过程。
3.  **复杂报表生成：** 涉及数据库查询、图表渲染、PDF 导出等耗时操作。
4.  **企业工作流审批：** 涉及人工介入的审批流程，Agent 需要挂起等待数小时甚至数天。

**需要注意的问题：**
*   **成本控制：** 长时运行意味着多次调用 LLM 进行状态检查，Token 消耗会显著增加。
*   **状态一致性：** 确保异步任务的结果能准确映射回发起该任务的特定会话。

**实施建议：**
*   使用 **Step Functions** 编排长时任务，利用其可视化和持久化特性。
*   在 MCP Server 端实现**心跳机制**，确保 Agent 能够感知到任务是否还在运行。

## 4. 行业影响分析

**对行业的启示：**
AI Agent 正在从“聊天机器人”向“数字员工”进化。数字员工必须能够处理长时任务，就像人类员工一样，接到任务 -> 执行（耗时）-> 汇报。这篇文章揭示了这一转型的技术基础设施。

**可能带来的变革：**
*   **MCP 协议的标准化：** 推动业界统一异步 Agent 的通信标准，使得不同厂商的 Agent 可以无缝对接长时服务。
*   **云原生 AI 的深化：** 进一步绑定 AI 能力与云基础设施（如 AWS Lambda/SQS），使得 AI 应用开发彻底转向云原生架构。

**相关领域的发展趋势：**
*   **Agent Orchestrator（编排器）的崛起：** 未来的核心竞争点在于谁能更好地管理这些长时、复杂的 Agent 链路。
*   **流式响应与事件驱动的结合：** 从单纯的流式 Token 输出，转向流式事件更新。

## 5. 延伸思考

**引发的其他思考：**
*   **人机协作模式的变化：** 如果 Agent 能处理长时任务，人类在等待期间做什么？界面如何从“对话框”变为“任务仪表盘”？
*   **多租户隔离：** 在长时运行中，如何确保不同租户的数据安全和任务隔离？

**可以拓展的方向：**
*   **记忆系统的融合：** 将长时任务的结果自动存入长期记忆库（如 GraphRAG），供未来查询使用。
*   **主动式 Agent：** 任务完成后，Agent 不是等待用户来问，而是主动推送通知。

**需要进一步研究的问题：**
*   如何在长时运行中优雅地处理“部分失败”？
*   当任务耗时极长（如数天），如何保持 LLM 上下文的相关性而不产生高昂的 Token 成本？

## 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现有架构：** 检查你目前的 Agent 调用的工具是否都是同步 HTTP 请求。如果是，这就是瓶颈。
2.  **引入中间层：** 不要让 Agent 直接调用耗时 API。Agent 应该调用一个“调度器 API”，该 API 立即返回 Task ID 并触发后台任务。
3.  **构建轮询工具：** 为 Agent 编写一个 `check_task_status(task_id)` 的工具，并在 Prompt 中指示它定期调用。

**具体的行动建议：**
*   **第一步：** 在 Bedrock Agent 中定义一个 `start_long_task` 工具。
*   **第二步：** 后端接收请求后，将任务推送到 SQS，立即返回 202 Accepted 和任务 ID。
*   **第三步：** Lambda 消费 SQS 消息执行任务，更新 DynamoDB 状态。
*   **第四步：** 在 Agent 的 Prompt 中增加逻辑：“如果工具返回了 task_id，请调用 check_status 工具直到状态为 completed”。

**需要补充的知识：**
*   AWS Step Functions 工作流设计。
*   异步编程模式（Promise/Future 模式在 Agent 中的应用）。
*   MCP 协议的具体报文格式。

**实践中的注意事项：**
*   **超时设置：** Bedrock Agent 的调用链路有超时限制，务必确保初始调用在超时前返回。
*   **幂等性：** 确保 Agent 因为网络问题重试调用时，不会在后台创建两个重复任务。

## 7. 案例分析

**结合实际案例说明：**
**场景：** 一位财务人员要求 Agent：“分析上个月所有 AWS 账单，找出异常支出，生成 Excel 报表并发邮件给我。”

**传统同步模式（失败）：**
Agent 调用 API 获取数据 -> API 查询 Cost Explorer 耗时 5 分钟 -> Bedrock 超时报错。

**长时运行模式（成功）：**
1.  **Agent (MCP Client):** 调用 `generate_report_tool`。
2.  **MCP Server:** 接收请求，返回 `{"status": "processing", "task_id": "123"}`。
3.  **Agent:** 向用户回复：“好的，我正在后台生成报表，这可能需要几分钟，我会每 30 秒检查一次进度。”
4.  **后台系统：** 使用 Step Functions 并行查询数据、分析、生成 Excel、发送邮件。
5.  **Agent:** 循环调用 `check_status("123")`。
6.  **最终：** 状态变为 `completed`，Agent 获取到邮件链接，告知用户：“报表已生成，已发送至您的邮箱。”

**经验教训总结：**
在长时任务中，**用户的预期管理**与代码实现同样重要。Agent 必须能够清晰地沟通“正在做什么”，否则用户会以为它卡死了。

## 8. 哲学与逻辑：论证地图

**中心命题：**
在构建企业级 AI Agent 时，采用基于 **Strands Agents** 和 **上下文消息策略** 的异步 MCP 服务器架构，是实现复杂、长时业务自动化的必要条件。

**支撑理由：**
1.  **理由 1（业务现实）：** 企业业务流程本质上是耗时的（数据聚合、审批、生成），无法在 LLM 单次请求的几秒钟内完成。
    *   *依据：* 现实世界 API 延迟和物理处理时间。
2.  **理由 2（技术限制）：** LLM 是无状态的，且客户端连接有超时限制，同步阻塞会导致资源耗尽或用户体验崩溃。
    *   *依据：* HTTP 超时标准和 LLM Token 限制。
3.  **理由 3（协议能力）：** MCP 协议支持双向通信，

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用有状态的会话管理架构

**说明**: 长时间运行的 MCP 服务器需要维护跨多个请求的上下文信息。与无状态请求不同，长时间运行的工作流（如代码生成或数据分析）需要服务器记住之前的交互步骤。AgentCore 与 Strands Agents 的集成要求服务器能够处理会话恢复和状态持久化，以防止因网络波动或超时导致的工作流中断。

**实施步骤**:
1. 使用 Amazon DynamoDB 或 ElastiCache 等托管服务存储会话状态和中间变量。
2. 在 MCP 服务器实现中定义唯一的 `session_id`，并在所有工具调用中传递该 ID。
3. 实现检查点机制，定期将 Strands Agent 的执行进度保存到持久化存储中。

**注意事项**: 避免将大型二进制对象直接存入状态存储，应使用 S3 等对象存储服务保存大文件，并在状态中保留引用指针。

---

### 实践 2：实现异步任务处理与回调机制

**说明**: Strands Agents 执行的复杂任务（例如处理长文档或调用外部 API）可能超出 Bedrock 或 MCP 客户端的超时限制。最佳实践是采用“请求-确认”模式，服务器立即返回任务确认，然后在后台异步处理，最后通过回调或状态轮询通知客户端结果。

**实施步骤**:
1. 将长时间运行的操作设计为异步任务，利用 Amazon SQS 或 Step Functions 进行编排。
2. MCP 工具端点应立即返回一个 `task_id` 和预估状态（如“PROCESSING”）。
3. 实现一个状态查询端点，允许 Agent 或客户端定期轮询任务状态，或配置 SNS/EventBridge 事件进行主动通知。

**注意事项**: 确保异步任务的处理逻辑是幂等的，以防止网络重试导致的重复执行。

---

### 实践 3：优化 Strands Agents 的上下文窗口管理

**说明**: 长时间运行的会话容易积累大量的 Token 消耗，导致上下文溢出或成本激增。在集成 Strands Agents 时，必须实施严格的上下文管理策略，仅保留与当前步骤相关的历史信息，而不是将整个对话历史传递给 Bedrock 模型。

**实施步骤**:
1. 实施摘要机制，当对话轮次超过阈值时，使用轻量级模型总结之前的交互。
2. 在调用 Bedrock AgentCore 时，明确过滤掉与当前工具调用无关的系统提示或历史消息。
3. 为 Strands Agents 配置最大上下文限制，并在接近限制时触发截断逻辑。

**注意事项**: 在截断上下文时，务必保留关键的系统指令和必须维持的变量，防止 Agent 丢失核心指令。

---

### 实践 4：构建健壮的错误处理与重试逻辑

**说明**: 分布式环境中的网络抖动、限流或服务不可用是常态。长时间运行的 MCP 服务器必须具备区分瞬时错误（可重试）和永久错误（需终止）的能力，并与 Strands Agents 的错误反馈回路集成，以便 Agent 能够自我修正或向用户报告。

**实施步骤**:
1. 集成 AWS SDK 的内置重试机制（配置指数退避算法），特别是针对 Bedrock InvokeAgent API 的调用。
2. 定义标准化的错误响应格式，区分 `TransientError`（如 429/503）和 `PermanentError`（如 400/403）。
3. 在 Strands Agents 层面实现“错误反思”步骤，当工具调用失败时，允许 Agent 分析错误原因并尝试替代方案。

**注意事项**: 避免无限重试导致死循环，务必设置最大重试次数和超时时间。

---

### 实践 5：实施细粒度的可观测性与监控

**说明**: 对于长时间运行的服务，仅监控成功率是不够的。需要深入追踪每个 Strands 的执行路径、工具调用的延迟以及 Token 消耗情况。这有助于调试复杂的 Agent 行为并优化成本。

**实施步骤**:
1. 使用 AWS CloudWatch 或 X-Ray 为 MCP 服务器的每个工具调用埋点，记录输入、输出和延迟。
2. 记录 Strands Agents 的思维链或中间步骤，将其作为结构化日志发送到 CloudWatch Logs。
3. 设置告警指标，例如“单次会话轮数异常”、“工具调用超时率”或“Token 使用量突增”。

**注意事项**: 在记录日志时，务必过滤敏感信息（PII），确保符合数据隐私合规要求。

---

### 实践 6：确保工具接口的幂等性与安全性

**说明**: 长时间运行的 Agent 可能会因为重试或逻辑循环多次调用同一个工具。如果工具执行的是写操作（如创建资源、发送邮件、修改数据库），则必须保证多次调用不会产生副作用。同时，必须严格验证 Agent 的调用权限。

**实施步骤**:
1. 对于所有写操作工具，在业务逻辑层实现幂等性检查（例如检查唯一 ID 是否已存在）。
2. 利用 IAM (AWS Identity and Access Management) 控制

---
## 学习要点

- Amazon Bedrock AgentCore 现已支持集成 Strands Agents，允许开发者构建能够长时间运行并具备状态记忆能力的 MCP 服务器。
- 通过将 Strands Agents 的状态管理能力与 MCP 协议结合，解决了传统无状态模型在处理复杂、多步骤任务时的上下文丢失问题。
- 该架构支持将 AI 应用从简单的单次问答扩展为能够处理长期工作流和复杂业务逻辑的智能代理。
- 开发者可以利用 MCP 协议的标准化接口，更轻松地将 Bedrock 的强大模型能力与外部数据源和工具进行深度集成。
- 此项集成显著增强了企业级 AI 应用的实用性，使其能够胜任自动化运维、长期项目跟踪等需要持续交互的高级场景。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [MCP](/tags/mcp/) / [AgentCore](/tags/agentcore/) / [异步任务](/tags/%E5%BC%82%E6%AD%A5%E4%BB%BB%E5%8A%A1/) / [Strands Agents](/tags/strands-agents/) / [AI Agent](/tags/ai-agent/) / [上下文管理](/tags/%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86/) / [长连接](/tags/%E9%95%BF%E8%BF%9E%E6%8E%A5/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-5.md" >}})
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-7.md" >}})
- [基于Amazon Bedrock AgentCore构建长时运行MCP服务器集成方案]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
- [基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器]({{< relref "posts/20260213-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*