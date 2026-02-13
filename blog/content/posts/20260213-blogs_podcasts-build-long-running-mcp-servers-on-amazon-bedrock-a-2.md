---
title: "基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器"
date: 2026-02-13T01:06:49+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "MCP", "AgentCore", "Strands Agents", "异步任务", "长时运行", "AI 代理", "上下文管理"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "这篇文章介绍了如何在 Amazon Bedrock AgentCore 上利用 Strands Agents 集成来构建能够长时间运行的 MCP（Model Context Protocol）服务器。为实现这一目标，文章提出了一套综合性的解决方案： 1. **上下文消息策略**：引入了一种保持服务器与客户端在长时间操作"
external_url: https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration
scenarios: ["AI/ML项目", "Web应用开发"]
---

# 基于Amazon Bedrock AgentCore构建支持长时运行任务的MCP服务器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-12T20:16:20+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration](https://aws.amazon.com/blogs/machine-learning/build-long-running-mcp-servers-on-amazon-bedrock-agentcore-with-strands-agents-integration)

---
## 摘要/简介

在本文中，我们将为您提供一套全面的实现方法。首先，我们会介绍一种上下文消息策略，以便在长时间运行的操作期间保持服务器与客户端之间的持续通信。接下来，我们会构建一个异步任务管理框架，让您的 AI 代理能够启动长时间运行的流程，同时不会阻塞其他操作。最后，我们将演示如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 结合起来，打造可用于生产环境的 AI 代理，可靠地处理复杂且耗时的操作。

---
## 导语

构建能够处理长时间运行任务的 AI 代理是当前技术落地的一大难点，因为这要求系统在保持通信的同时避免阻塞主流程。本文将详细介绍如何利用上下文消息策略和异步任务管理框架，解决这一技术瓶颈。通过将其与 Amazon Bedrock AgentCore 及 Strands Agents 集成，我们将演示如何打造稳定、可用于生产环境的 AI 代理，帮助您在实际业务中可靠地处理复杂且耗时的操作。

---
## 摘要

这篇文章介绍了如何在 Amazon Bedrock AgentCore 上利用 Strands Agents 集成来构建能够长时间运行的 MCP（Model Context Protocol）服务器。为实现这一目标，文章提出了一套综合性的解决方案：

1.  **上下文消息策略**：引入了一种保持服务器与客户端在长时间操作中持续通信的机制，确保在任务执行期间上下文不丢失。
2.  **异步任务管理框架**：开发了一个框架，允许 AI 代理启动耗时较长的流程，同时不阻塞其他操作的执行。
3.  **生产级集成**：展示了如何将这些策略与 Amazon Bedrock AgentCore 和 Strands Agents 相结合，从而构建出可靠、能够处理复杂且耗时任务的生产级 AI 代理。

---
## 评论

**文章中心观点**
该文章提出了一种基于 Amazon Bedrock AgentCore 和 Strands Agents 的技术架构，旨在通过引入上下文消息策略和异步任务管理框架，解决 MCP（Model Context Protocol）服务器在执行长周期任务时的状态保持与通信中断问题，从而实现稳定的长对话链路。

**支撑理由与深度评价**

**1. 解决了 LLM 应用中的“长任务”真空期痛点（事实陈述）**
在当前的生成式 AI 应用架构中，主流的同步请求-响应模式在处理耗时任务（如数据批量处理、复杂代码生成）时，极易遭遇 HTTP 超时或 Token 输出中断。文章提出的“异步任务管理框架”切中了行业痛点。通过将 Agent 的思考过程与任务的执行过程解耦，允许 Agent 在后台任务运行时释放对话线程，这是一种符合现代云原生架构（如事件驱动架构）的合理演进。

**2. 引入 Strands Agents 实现状态连续性（作者观点）**
文章重点强调的“Strands Agents integration”是其核心创新点。Strands（通常指代具有连续记忆或子线程代理能力的概念）在此处的应用，本质上是构建了一个“虚拟看板”。它不仅仅是一个消息队列，更是一个具备状态感知的中介。这使得 AI Agent 能够在长任务完成后，准确地“找回”之前的对话上下文，而不是开启一个新的无状态会话。这种设计对于提升用户体验（UX）至关重要，避免了用户在等待期间无法进行交互或必须重新提示的尴尬。

**3. MCP 协议在 Bedrock 生态中的企业级落地（你的推断）**
MCP（Model Context Protocol）正逐渐成为连接 LLM 与数据源的标准协议。Amazon Bedrock 支持 MCP 并结合 AgentCore，标志着 AWS 正在试图将 MCP 从一种“数据连接工具”升级为“长期服务的代理载体”。文章展示的不仅是代码实现，更是 AWS 对“Agent 即服务”这一商业愿景的技术铺垫。

**反例与边界条件**

**1. 成本与复杂度的权衡（边界条件）**
虽然异步框架解决了超时问题，但它显著增加了系统复杂度。开发者需要维护额外的任务状态存储、异步消息队列（如 SQS）以及 Strands 的生命周期管理。对于简单的查询类任务，这种架构属于“过度设计”，不仅增加了延迟，还提高了运营成本。

**2. 状态一致性的最终一致性挑战（反例/技术难点）**
文章可能淡化了分布式系统中的状态同步问题。如果异步任务执行失败，或者 Strands Agent 在回传上下文时网络中断，Bedrock Agent 如何处理回滚？不同于同步调用中的即时报错，这种长链路异步架构的错误排查极其困难，可能导致任务“悬空”且用户无感知。

**3. 厂商锁定风险（你的推断）**
该方案深度耦合了 Amazon Bedrock 的 AgentCore 和 Strands 机制。虽然 MCP 本身是通用的，但一旦业务逻辑依赖于 Bedrock 特定的异步编排能力，未来迁移至 Azure OpenAI 或 Google Vertex AI 将面临极高的重构成本。

**可验证的检查方式**

**1. 任务超时与恢复测试（实验/指标）**
*   **检查方式**：构建一个模拟耗时 5 分钟的任务（如生成超大报表），在任务执行期间切断客户端连接，然后在任务结束后重新发起连接。
*   **验证指标**：系统是否能自动推送完成通知？重新连接后，Agent 是否能无缝接续刚才的结果继续处理，还是需要用户重新输入上下文？

**2. 并发状态下的 Token 消耗与延迟测试（观察窗口）**
*   **检查方式**：在 Strands 维护长连接上下文时，观察 Bedrock 的 API 调用次数和 Token 消耗。
*   **验证指标**：对比传统的“用户轮询”模式与该文的“Agent 主动推送”模式，验证是否因为频繁的上下文同步导致了不必要的 Token 开销（即“幻觉性对话”或冗余的 Heartbeat 消息）。

**3. 错误处理机制的鲁棒性（压力测试）**
*   **检查方式**：在异步任务执行到 50% 时，人为强制杀死下游的计算服务或切断 Strands 与 Bedrock 的网络连接。
*   **验证指标**：Bedrock AgentCore 是否能捕获异常并向用户报告具体的失败原因，还是仅仅返回一个通用的“Task Failed”错误？

**总结评价**
这篇文章从技术落地上看，是一篇典型的“架构模式”指南，具有较高的实用价值，特别是针对正在构建企业级 AI 应用的 AWS 开发者。它清晰地指出了从“Demo”走向“生产环境”时必须跨越的异步化鸿沟。然而，文章带有较强的厂商推销色彩，可能有意无意地忽略了运维复杂度和调试难度。建议读者在采纳该方案时，务必评估业务的真实复杂度，并设计完善的可观测性工具来应对长周期任务带来的不确定性。

---
## 技术分析

基于您提供的文章标题《Build long-running MCP servers on Amazon Bedrock AgentCore with Strands Agents integration》及其摘要片段，以下是对该文章核心观点和技术要点的深入分析。

---

# 深度分析报告：基于 Amazon Bedrock AgentCore 与 Strands 的长时运行 MCP 服务器构建

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**在构建基于大模型（LLM）的智能体应用时，必须突破传统的“单次请求-响应”模式，转而构建一种能够处理长时间、多步骤复杂任务的持久化服务架构。** 具体而言，通过结合 **Amazon Bedrock AgentCore** 的托管能力与 **Strands Agents** 的上下文管理机制，开发者可以创建出既能保持长期连接，又能异步处理复杂任务流的 Model Context Protocol (MCP) 服务器。

### 作者想要传达的核心思想
作者试图传达的核心思想是**“有状态的连续性”**与**“异步解耦”**。在 AI Agent 处理现实世界任务（如代码部署、数据分析、工作流自动化）时，任务往往耗时较长，不能受限于 LLM 的超时机制。作者主张通过**上下文消息策略**维持客户端与服务器的“心跳”感知，同时利用**异步任务管理框架**将指令下发与实际执行分离，从而实现真正的“长时运行”能力。

### 观点的创新性和深度
该观点的创新性在于将 **MCP（模型上下文协议）** 这一通常用于即时知识检索的协议，扩展到了**任务编排**领域。它不仅解决了 MCP 在 Bedrock 环境下的集成问题，更深入探讨了如何在无状态（Stateless）的 LLM 调用之上，通过 AgentCore 和 Strands 架构构建有状态的业务逻辑层。这是对当前 AI Agent 从“聊天机器人”向“自主工作者”演进的一次重要技术落地。

### 为什么这个观点重要
随着 AI Agent 从简单的问答转向复杂的企业级业务操作，**长时任务处理**成为刚需。如果 Agent 只能处理秒级响应的任务，其应用场景将被极大限制。该文章提出的架构解决了 AI 落地中最棘手的“稳定性”与“时效性”矛盾，使得构建能够处理分钟级、甚至小时级复杂任务的 AI Agent 成为可能。

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Amazon Bedrock AgentCore**: AWS 提供的基础设施，用于托管和编排 Agent 逻辑，提供安全、可扩展的运行环境。
2.  **MCP (Model Context Protocol)**: 一种开放协议，用于连接 AI 模型与外部数据源（本文中扩展为连接外部任务执行器）。
3.  **Strands Agents**: 文章引入的核心组件，专注于“Strands”（线索/流）的上下文管理，负责维护长时间对话和任务的状态。
4.  **Asynchronous Task Management (异步任务管理)**: 允许 AI 发起任务后立即释放连接，后台继续处理，并通过轮询或回调获取结果。

### 技术原理和实现方式
*   **上下文消息策略**: 
    *   **原理**: 在长任务执行期间，服务器不会保持连接阻塞等待，而是发送包含“任务状态 ID”的中间响应。
    *   **实现**: 客户端收到中间状态后，可以挂起当前会话，在用户再次询问或通过后台轮询时，利用之前的 Context ID 恢复通信，确保 AI “知道”任务正在进行中。
*   **异步任务框架**:
    *   **实现**: MCP Server 接收到 Bedrock Agent 的指令后，不直接同步执行耗时操作，而是将任务推送到消息队列（如 AWS SQS）或触发 Step Functions，并立即返回一个“任务已接收”的确认给 Agent。Agent 利用 Strands 的记忆能力，在后续轮转中检查任务状态。

### 技术难点和解决方案
*   **难点**: LLM 本质是无状态的，如何让 LLM 在等待任务完成时不产生幻觉或重复调用？
*   **解决方案**: 利用 **Strands Agents** 的持久化记忆层。将任务状态写入 Strands 的上下文存储中，每次 LLM 思考时，强制其读取该状态，从而确保决策的连续性。
*   **难点**: 网络超时与资源消耗。
*   **解决方案**: Bedrock AgentCore 提供了托管的高并发处理能力，配合异步架构，使得长连接不会阻塞服务器线程。

### 技术创新点分析
最大的创新点在于 **MCP 协议的“流式”改造**。传统的 MCP 工具调用通常是同步函数调用，而该架构将其改造为支持“任务提交 -> 状态追踪 -> 结果汇总”的异步工作流，这赋予了 LLM 操作系统的“进程管理”能力雏形。

## 3. 实际应用价值

### 对实际工作的指导意义
该架构为开发者提供了一套在 AWS 云原生环境下构建复杂 AI 应用的标准蓝图。它指导开发者如何从“写 Prompt”转向“写系统”，特别是如何处理 AI 与后端业务逻辑的深度集成。

### 可以应用到哪些场景
1.  **DevOps 与代码生成**: Agent 生成代码后，需要调用 CI/CD 流水线进行部署（耗时可能长达 10-20 分钟），期间需要 Agent 持续监控日志并反馈。
2.  **复杂数据分析**: Agent 接收数据查询请求，后台启动 Spark/EMR 任务进行大数据处理，处理完成后通知用户下载结果。
3.  **企业工作流自动化**: 例如审批流程，Agent 提交申请后，需要等待数小时的人工审批，并在审批通过后执行下一步操作。

### 需要注意的问题
*   **状态一致性**: 确保异步任务的状态更新能够实时准确地反映到 LLM 的上下文窗口中。
*   **错误处理**: 如果后台任务失败，Strands Agent 需要具备足够的智能来分析错误日志并进行重试或报错，而不是陷入死循环。

### 实施建议
建议采用 **AWS Step Functions** 来可视化编排长时运行的任务，并将其状态直接映射到 Strands Agents 的上下文中，以利用 AWS 原生服务的稳定性和可观测性。

## 4. 行业影响分析

### 对行业的启示
该文章标志着 **AI Agent 基础设施** 正在走向成熟。行业重心从“模型参数大小”转向了“任务执行时长”和“系统可靠性”。它表明，未来的 AI 竞争将不仅是模型能力的竞争，更是 **Agent 编排框架** 的竞争。

### 可能带来的变革
这将推动 **“自主 AI 助手”** 从简单的客服工具转变为真正的 **“数字员工”**。企业可以开始将需要长时间跨度的业务流程（如月度结账、供应链协调）交给 AI 管理，从而大幅降低人力成本。

### 相关领域的发展趋势
*   **协议标准化**: MCP 可能会成为连接 LLM 与业务系统的标准协议，类似于 SQL 对于数据库的地位。
*   **混合架构**: “推理层（LLM）+ 执行层”的分离将成为主流设计模式。

### 对行业格局的影响
AWS 通过 Bedrock AgentCore 结合 Strands（可能是内部或合作伙伴的高级框架），正在构建强大的护城河。这使得 AWS 上的开发者更容易构建复杂应用，从而锁定用户在其生态系统中。

## 5. 延伸思考

### 引发的其他思考
如果长时运行成为常态，**计费模式**该如何改变？按 Token 计费可能不再适用，应转向按“任务步骤”或“执行时长”计费。此外，**安全性**也是巨大挑战——一个具有长时记忆和异步执行能力的 Agent，如果被恶意指令利用，可能会造成更大的破坏。

### 可以拓展的方向
*   **多 Agent 协作**: 一个 Strand Agent 分解任务，多个专门的 Bedrock Agent 并行处理不同的长时任务。
*   **人机协同**: 在长时任务的关键节点（如高风险操作），自动引入人工审批机制。

### 需要进一步研究的问题
1.  上下文窗口的极限：当任务运行数天，上下文信息极其庞大时，如何高效检索？
2.  成本控制：长时运行意味着大量的 Token 消耗和 API 调用，如何优化成本？

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有业务**: 寻找业务中耗时超过 30 秒且规则明确的流程（如报表生成、API 数据聚合）。
2.  **引入 Bedrock**: 将现有的 Lambda 函数或 ECS 任务包装为 Bedrock Agent 的 Action Group。
3.  **改造通信模式**: 将同步 API 调用改为“返回 TaskID + 异步执行”的模式。

### 具体的行动建议
*   **第一步**: 搭建一个简单的 Bedrock Agent，并配置一个通过 MCP 协议连接的“模拟长时任务”工具（如 sleep 60秒）。
*   **第二步**: 实现上下文策略，观察 Agent 在等待期间如何响应用户的追问。
*   **第三步**: 引入 DynamoDB 或 ElastiCache 存储 Strands 的状态，确保多轮对话状态不丢失。

### 需要补充的知识
*   **Amazon Bedrock 服务架构**。
*   **异步编程模型**。
*   **Prompt Engineering for Planning** (如何让 LLM 制定计划)。

### 实践中的注意事项
务必设置严格的 **Timeout（超时）** 和 **Retry（重试）** 机制。LLM 容易产生“幻觉”，如果它认为任务完成了但实际没有，系统需要能够自动纠正或触发告警。

## 7. 案例分析

### 结合实际案例说明
**场景**: 一家电商公司需要 AI Agent 每天凌晨分析数百万条交易记录并生成营销报表。

**传统做法**: 用户请求 -> LLM 调用后端脚本 -> 脚本运行 30 分钟 -> HTTP 超时 -> 任务失败。

**基于文章架构的做法**:
1.  **请求**: 用户要求“生成日报”。
2.  **分解与分发**: Bedrock Agent 识别任务耗时，通过 MCP 发送指令启动 EMR 集群。
3.  **异步执行**: EMR 开始计算，MCP Server 立即返回“任务 ID: 12345, 状态: Processing”。
4.  **上下文保持**: 用户中途问“进度如何？”，Agent 通过 Strands 查询 ID 12345 状态，回复“正在处理，已完成 60%”。
5.  **结果反馈**: 任务完成后，Agent 主动通知用户或等待用户下次询问时展示报表链接。

### 成功案例分析
**Case**: **CodeWhisperer (或类似 coding Agent) 的 PR 部署功能**。
成功因素在于它不仅生成代码，还调用 CI/CD API，并在构建失败时读取 Log，自动修复错误。这正是长时运行 Agent 的典型应用。

### 失败案例反思
如果缺乏 **Context Message Strategy**，Agent 会在任务提交后因为网络波动或超时而“失忆”，导致用户询问时回答“我没有执行过任何任务”，造成极差的用户体验。

## 8. 哲学与逻辑：论证地图

### 中心命题
**为了在企业级场景中实现具有高可靠性的自主 AI Agent，必须采用基于 Amazon Bedrock AgentCore 与 Strands 的异步 MCP 服务器架构，以突破同步交互的时效性限制。**

### 支撑理由

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化会话状态管理与持久化

**说明**:
长时间运行的 MCP 服务器需要维护跨多个请求的上下文状态。在 Bedrock AgentCore 环境中，必须确保状态不仅存储在内存中，还要持久化到外部存储（如 DynamoDB 或 S3），以便在服务器重启或扩展时恢复状态。

**实施步骤**:
1. 设计无状态的服务器逻辑，将会话状态（如用户偏好、对话历史）序列化为 JSON 或 Protocol Buffers。
2. 在每次 MCP 工具调用结束时，将更新后的状态保存到 Amazon DynamoDB 表中，使用 SessionID 作为主键。
3. 在处理新的 MCP 请求时，首先从持久层加载状态，并将其注入到 Strands Agent 的执行上下文中。

**注意事项**:
避免在内存中保存敏感的 PII（个人身份信息）数据，如果必须保存，请确保在持久化之前进行加密。

---

### 实践 2：实施严格的超时与重试策略

**说明**:
长时间运行的操作（如数据处理或外部 API 调用）可能会超过 Bedrock 或客户端的默认超时限制。最佳实践是使用异步模式处理长任务，并配置适当的指数退避重试策略以处理瞬态故障。

**实施步骤**:
1. 将所有通过 MCP 暴露的操作设计为异步模式：立即返回一个 `taskId`，并在后台处理任务。
2. 为 Strands Agents 配置专门的“状态检查”工具，允许客户端轮询任务状态。
3. 在 MCP 服务器代码中，针对调用 Bedrock AgentCore 或下游服务实施指数退避算法（如使用 jitter 的指数退避）。

**注意事项**:
确保轮询接口有速率限制，以防止客户端过度频繁地查询状态，从而导致服务器过载。

---

### 实践 3：构建模块化的 Strands Agent 架构

**说明**:
为了保持长运行服务的可维护性，应避免构建单一的庞大 Agent。相反，应利用 Strands 的特性，将复杂逻辑分解为多个专门的子 Agent，每个 Agent 负责特定的领域或功能。

**实施步骤**:
1. 分析业务流程，识别出独立的逻辑域（例如：数据检索 Agent、数据分析 Agent、报告生成 Agent）。
2. 为每个子 Agent 定义清晰的 MCP 工具接口和输入/输出模式。
3. 在主编排层中，使用 Bedrock AgentCore 的路由功能将请求分发给相应的 Strands 子 Agent 处理。

**注意事项**:
确保子 Agent 之间的通信开销最小化，避免过深的调用链导致延迟累积。

---

### 实践 4：建立全面的可观测性与日志记录

**说明**:
调试长运行的异步流程非常困难。必须实施结构化日志记录和指标追踪，以便能够跨请求追踪执行路径，并快速定位性能瓶颈或错误。

**实施步骤**:
1. 在 MCP 服务器的整个生命周期中注入 Trace ID（可以使用 X-Ray 或 OpenTelemetry）。
2. 记录关键事件：MDC（消息分发中心）事件、工具调用开始/结束、错误堆栈以及状态转换。
3. 设置 CloudWatch 告警，用于监控错误率、延迟（P95/P99）以及死信队列（DLQ）的深度。

**注意事项**:
注意日志记录的成本，避免在循环或高频调用中记录过于详细的调试信息，建议在生产环境中调整日志级别为 INFO 或 WARN。

---

### 实践 5：实施基于 IAM 的最小权限访问控制

**说明**:
MCP 服务器通常需要代表用户调用 AWS 服务或其他 API。必须严格限制服务器的 IAM 权限，仅授予完成特定任务所需的最小权限集，以减少安全风险。

**实施步骤**:
1. 为不同的 Strands Agent 创建不同的 IAM 角色。
2. 编写 IAM 策略时，明确限定资源 ARN（例如，限制只能访问特定的 S3 bucket 前缀或 DynamoDB 键）。
3. 定期使用 IAM Access Analyzer 审查权限，移除未使用的权限。

**注意事项**:
不要在代码中硬编码凭证。始终使用 IAM 角色或 AWS Secrets Manager 来管理外部 API 的密钥。

---

### 实践 6：设计幂等的 MCP 工具接口

**说明**:
在分布式系统中，网络重试是常态。如果客户端重试请求，你的 MCP 工具必须能够安全地处理重复调用，而不会导致数据重复或状态不一致。

**实施步骤**:
1. 在工具设计时引入幂等键。客户端在调用时生成唯一的 ID，服务器检查该 ID 是否已处理。
2. 对于写操作，使用条件写入（如 DynamoDB 的 PutItem 操作，仅在条件不满足时写入）。
3. 确保所有状态更新操作都是原子性的或可重放的。

**注意事项**:
幂等性检查本身不应成为性能瓶颈，考虑使用 Redis 或 ElastiCache 等高性能存储来存储短期幂等键。

---
## 学习要点

- 通过在 Amazon Bedrock AgentCore 上集成 Strands Agents，开发者能够构建具备长时间运行能力和状态记忆的 MCP 服务器，从而克服传统无状态模型在处理复杂、多步骤任务时的局限性。
- 利用 Strands Agents 的“Strands”概念，服务器可以将连续的对话和操作步骤封装在独立的上下文线程中，确保在长时间任务执行过程中状态的持久化和逻辑的连贯性。
- 该架构通过 MCP 协议实现了 AI 智能体与外部工具和数据源的无缝集成，使得模型不仅能进行对话，还能自主调用 API 并执行实际的操作逻辑。
- Amazon Bedrock AgentCore 提供了托管的基础设施，简化了底层运维，让开发者可以专注于定义智能体的业务逻辑，而无需管理服务器生命周期。
- 这种集成方案特别适用于需要跨越数小时或数天的工作流场景（如复杂的研发流程或长期客户服务），显著提升了自动化任务的完成度和可靠性。
- 开发者可以利用 MCP 协议的标准化特性，灵活地将自定义工具挂载到 Bedrock AgentCore 上，快速扩展智能体的功能边界。
- 通过将长时间运行的逻辑卸载到 AgentCore 服务器，该方案有效解决了大型语言模型（LLM）上下文窗口有限和无法自动保持状态的痛点。

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
- [基于Amazon Bedrock AgentCore构建长运行MCP服务器与异步任务管理]({{< relref "posts/20260212-blogs_podcasts-build-long-running-mcp-servers-on-amazon-bedrock-a-1.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用]({{< relref "posts/20260210-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*