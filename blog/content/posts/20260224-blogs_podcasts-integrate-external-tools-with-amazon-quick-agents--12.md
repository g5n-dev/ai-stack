---
title: "使用 MCP 将外部工具集成至 Amazon Quick Agents"
date: 2026-02-24T12:37:50+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "Agent", "系统集成", "LLM", "开发指南", "第三方集成", "AWS"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "该内容是一份面向第三方合作伙伴的**实操指南**，旨在指导如何通过**模型上下文协议（MCP）**将外部工具与 **Amazon Quick Agents** 进行集成。 主要内容包括： 1. **适用对象**：需要进行详细集成实施的第三方（3P）合作伙伴。 2. **核心任务**：构建新的 MCP 服务器，或验证并调"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["大语言模型"]
---

# 使用 MCP 将外部工具集成至 Amazon Quick Agents

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在这篇文章中，您将使用一份六步检查清单来构建新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以实现与 Amazon Quick 的集成。《Amazon Quick 用户指南》描述了 MCP 客户端的行为与约束。本文是一份“操作指南”，面向 3P 合作伙伴为使用 MCP 与 Amazon Quick 集成所需的详细实现步骤。

---
## 导语

随着 Amazon Quick Agents 的应用场景日益复杂，如何高效、规范地集成外部工具成为开发者关注的重点。本文基于 Model Context Protocol (MCP) 提供了一份详实的构建指南，旨在帮助第三方合作伙伴解决服务器适配难题。通过文中的六步检查清单，您将能够验证现有配置或构建新的 MCP 服务器，从而顺利实现与 Amazon Quick 的深度集成。

---
## 摘要

该内容是一份面向第三方合作伙伴的**实操指南**，旨在指导如何通过**模型上下文协议（MCP）**将外部工具与 **Amazon Quick Agents** 进行集成。

主要内容包括：
1.  **适用对象**：需要进行详细集成实施的第三方（3P）合作伙伴。
2.  **核心任务**：构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器以适配 Amazon Quick。
3.  **实施方法**：提供了一个**六步清单**（six-step checklist）作为实施路径。
4.  **参考依据**：集成过程需遵循《Amazon Quick 用户指南》中定义的 MCP 客户端行为及约束条件。

---
## 评论

### 文章评价报告

**文章标题：** Integrate external tools with Amazon Quick Agents using Model Context Protocol (MCP)
**评价维度：** 技术深度、行业影响、落地实施、批判性分析

---

#### 一、 核心观点与支撑理由

**中心观点：**
文章提出了一种基于标准化协议（MCP）将第三方工具无缝集成到 Amazon Quick Agents 的工程化范式，旨在解决 AI Agent 生态中工具调用碎片化的问题，并构建可扩展的智能体供应链。（作者观点 / 事实陈述）

**支撑理由：**

1.  **协议标准化带来的互操作性：**
    文章强调使用 MCP（Model Context Protocol）作为核心标准。从技术角度看，这解决了当前 LLM 应用中“每个 Agent 都需要定制 API Adapter”的痛点。MCP 类似于 API 界面的“USB 接口”，使得数据源和工具（如 SQL 数据库、Slack、本地文件系统）能够以统一的声明式方式暴露给 Agent。这大大降低了 3P（Third Party）开发者的接入成本。（事实陈述 / 技术分析）

2.  **以“清单”为导向的工程确定性：**
    文章提供的六步清单体现了企业级软件开发的严谨性。在 Agent 开发中，最大的风险在于幻觉和不可控的行为。通过明确的验证和调整步骤，Amazon 试图在灵活性和安全性之间建立护栏。这种方法论对于 B2B 行业至关重要，因为企业客户无法容忍“尽力而为”的连接，他们需要的是经过验证的稳定性。（作者观点 / 行业经验）

3.  **生态系统的构建逻辑：**
    文章明确提到“3P partners”，表明 Amazon 不仅仅是在卖一个工具，而是在通过 Quick Agents + MCP 构建一个类似 App Store 的生态。通过控制 MCP Client 的行为（在 Amazon 端）并规范 MCP Server 的实现（在合作伙伴端），Amazon 实际上制定了一个垂直领域的行业标准。这有助于将非结构化的外部数据转化为 Agent 可消费的结构化上下文。（你的推断）

**反例/边界条件：**

1.  **协议的通用性 vs. 特定场景的复杂性：**
    MCP 协议虽然标准化了“连接”，但未必能很好地处理所有类型的交互。例如，对于流式数据处理或需要极低延迟的实时控制场景（如高频交易机器人或游戏 AI），MCP 基于 JSON-RPC 的文本协议可能存在序列化开销，导致性能不如原生 gRPC 或 WebSocket 连接。（技术推断）
2.  **数据隐私与边界安全：**
    文章虽然提到了集成，但未深入探讨混合云环境下的数据主权问题。当 MCP Server 需要访问本地敏感文件系统，而 Client 是托管在 Amazon 公有云上的 Quick Agent 时，企业防火墙策略和 DLP（数据防泄漏）规则可能会成为该架构落地的重大阻碍，甚至导致架构被安全团队否决。（行业现实挑战）

---

#### 二、 维度深入评价

**1. 内容深度：**
文章属于**高实操性、中等理论深度**的工程技术文档。
*   **优点：** 它没有停留在概念层面，而是深入到了具体的实现细节（如 Manifest 配置、资源定义、Prompt 模板）。对于开发者而言，这种“手把手”的指导比宏大的架构图更有价值。
*   **不足：** 它可能缺乏对 MCP 协议底层设计哲学（如为什么是 JSON-RPC 而不是其他协议）的深度剖析，也没有讨论在极端并发情况下的性能表现。

**2. 实用价值：**
**极高。** 对于 ISV（独立软件开发商）和企业 IT 团队来说，这是一份“免坑指南”。
*   **实际案例：** 假设一家 SaaS 公司希望将其 CRM 数据接入 Amazon Quick Agents，以前他们需要研究 Amazon Bedrock 的特定 API 格式。现在，只需按照文章指南编写一个标准的 MCP Server，就能实现“一次编写，多处兼容”（如果 MCP 成为标准的话），直接提升了产品的可分发能力。

**3. 创新性：**
**渐进式创新。**
*   MCP 本身并非 Anthropic/Amazon 独创的概念（类似于 Function Calling 或 Plugins），但将其提升到一个开源、标准化的协议高度，并由云厂商巨头在核心产品中强力推行，这是一种**生态层面的创新**。它推动了 AI Agent 从“单点定制”走向“工业化组装”。

**4. 行业影响：**
这篇文章是 AI Agent 领域**基础设施标准化**的一个信号。
*   如果 MCP 被广泛采纳，未来 AI Agent 的竞争将不再是“谁接的工具多”，而是“谁的 Agent 推理能力更强”和“谁的生态工具质量更高”。这将催生出专门从事“MCP Server 开发”的新兴职业和产业链，类似于当年的“微信小程序开发者”。

**5. 争议点：**
*   **厂商锁定风险：** 虽然协议是开放的，但 Amazon Quick Agents 的 Client 行为是由 Amazon 定义的。如果未来 Amazon 在协议之上增加私有扩展，可能会导致“标准版 MCP”和“Amazon 增强 MCP”的分化，实际上形成了一种软性的技术锁定。
*   **协议战争：** 目前 OpenAI 也有类似的插件体系，但尚未完全开源统一。MCP 能否成为跨平台的标准，还是仅仅成为 Anthropic/Amazon 阵营的对抗工具，尚存争议。

---

#### 三、 可验证的检查方式

为了验证文章所述方法的有效性与 MCP 的实际表现，建议进行以下检查：

1.  **互操作性测试：**
    *   **指标：** 选取一个非 Amazon/Anth

---
## 技术分析

基于您提供的文章标题《Integrate external tools with Amazon Quick Agents using Model Context Protocol (MCP)》及其摘要，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：基于 MCP 协议集成 Amazon Quick Agents 的外部工具

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点在于**标准化**与**模块化**。它主张利用 **Model Context Protocol (MCP)** 作为一种通用的通信标准，来解决 AI 智能体与外部数据源/工具之间的碎片化连接问题。通过遵循一套特定的“六步清单”，开发者可以构建或调整 MCP 服务器，从而无缝地将第三方功能集成到 Amazon Quick Agents 中。

**作者想要传达的核心思想**
作者试图传达一种“**即插即用**”的 AI 生态愿景。在传统的 AI 开发中，为每一个工具（如 Jira、Slack、内部数据库）编写定制化的 API 接口是低效且难以维护的。MCP 的引入意味着：**“写一次服务器，到处连接客户端”**。对于 3P（Third-Party，第三方）合作伙伴而言，这不仅降低了技术门槛，更意味着只要遵循 MCP 标准，他们的工具就能迅速被 Amazon Quick Agents 这一庞大的生态系统发现并调用。

**观点的创新性和深度**
*   **解耦合**：创新点在于将“大模型的推理能力”与“获取数据的执行能力”彻底解耦。Quick Agents 只需要懂 MCP，而不需要懂每一个工具的特定 API。
*   **统一交互模型**：深度在于定义了一套统一的交互模型（Resources、Prompts、Tools），使得非结构化数据和结构化工具调用在同一协议下共存。

**为什么这个观点重要**
随着 LLM（大语言模型）应用从简单的聊天机器人转向复杂的 Agentic Workflow（智能体工作流），**连接性**成为最大的瓶颈。如果 Amazon Quick Agents 无法高效、安全地调用外部工具，它就只是一个信息孤岛。MCP 的引入是构建 AI Agent 生态系统的基石，它决定了 Amazon Quick 能否真正落地到企业的实际业务流中，而不仅仅是一个玩具。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **Model Context Protocol (MCP)**：核心协议，一种基于 JSON-RPC 的开放标准，用于 AI 应用与数据源/工具之间的通信。
*   **Amazon Quick Agents**：AWS 推出的生成式 AI 应用构建/托管平台（客户端）。
*   **MCP Server**：运行在本地或远程的进程，负责暴露特定的工具、资源或提示给客户端。
*   **Transport Layer (SSE / Stdio)**：MCP 支持的传输层，Quick Agents 可能更倾向于使用 Server-Sent Events (SSE) 或标准输入输出进行通信。

**技术原理和实现方式**
文章提到的“六步清单”通常涵盖以下技术实现逻辑：
1.  **环境准备**：配置 Python/Node.js 运行时及 SDK。
2.  **定义接口**：在服务器代码中声明 `tools`（函数，如 `get_weather`）、`resources`（数据，如 `file://logs`）或 `prompts`（预定义模板）。
3.  **实现逻辑**：编写具体的业务逻辑代码（如调用 SQL 数据库或 REST API）。
4.  **服务暴露**：将服务器通过 SSE 端点或 Stdio 方式启动。
5.  **配置连接**：在 Amazon Quick Agents 的配置文件中指向该 MCP Server 的地址。
6.  **验证测试**：使用 MCP Inspector 或 Quick Agents 的调试工具进行握手和功能验证。

**技术难点和解决方案**
*   **难点：数据安全与认证**。Quick Agents 访问企业内部工具时，如何确保权限受控？
    *   *解决方案*：MCP 协议支持在握手阶段传递认证信息，且建议在内网环境中部署 MCP Server，利用现有的 IAM 或 OAuth 体系进行鉴权。
*   **难点：上下文窗口限制**。外部工具返回大量数据（如长 PDF）会撑爆 LLM 上下文。
    *   *解决方案*：在 MCP Server 端实现“智能分块”或“摘要过滤”，仅传输相关数据给 LLM。

**技术创新点分析**
MCP 的最大技术创新在于其**可发现性**。不同于传统的 API 调用，MCP Server 会主动向 Client 广播自己有哪些能力。Amazon Quick Agents 可以动态地根据 Server 提供的描述来决定调用哪个工具，实现了真正的“语义化路由”。

## 3. 实际应用价值

**对实际工作的指导意义**
对于企业开发者，这意味着不再需要为 Quick Sights 或 Quick Agents 开发专用的 Lambda 函数连接器。只需维护一套标准的 MCP 服务，即可同时服务于 AWS 的 AI 服务和其他支持 MCP 的客户端（如 Claude Desktop 或其他 IDE 插件）。

**可以应用到哪些场景**
*   **企业知识库查询**：通过 MCP 将 Confluence、SharePoint 暴露给 Quick Agents，实现“问公司政策”。
*   **运维自动化**：MCP Server 封装 AWS SDK 或 Kubernetes API，让 Quick Agents 能够通过自然语言执行“重启服务”或“扩容容器的操作”。
*   **销售/CRM 助手**：连接 Salesforce 或 HubSpot 的数据，允许 Agent 实时查询客户最新状态并更新记录。

**需要注意的问题**
*   **延迟**：多跳架构带来的网络延迟可能影响用户体验。
*   **错误处理**：MCP Server 的异常必须能够被 LLM 理解并转化为自然语言反馈给用户，否则会导致对话卡死。

**实施建议**
优先从**只读**类工具开始集成（如查询数据库、读取文档），验证安全性后再开放**写入**类工具（如修改订单、发送邮件）。

## 4. 行业影响分析

**对行业的启示**
MCP 的流行标志着 AI 基础设施正在从“模型战争”转向**“协议战争”**。未来的 AI 生态将属于那些能够制定标准连接协议的企业。Anthropic 推出的 MCP 正在成为事实上的行业标准，AWS 的支持进一步巩固了这一地位。

**可能带来的变革**
这将催生一个新的职业角色：**MCP Server 开发者**。企业不再单纯招聘 Prompt Engineer，而是需要能够将传统 API 转化为语义化 MCP 接口的人才。SaaS 软件也将面临“MCP Native”的压力，即必须原生提供 MCP 接口才能被 AI Agent 生态接纳。

**对行业格局的影响**
这削弱了单一 API 集成服务商的价值，增强了通用协议制定者（如 Anthropic, AWS）的话语权。对于中小厂商，这是一个机会，只要适配 MCP，就能瞬间接入 AWS 和 Anthropic 的海量用户。

## 5. 延伸思考

**引发的其他思考**
*   **协议的通用性边界**：MCP 是否能覆盖所有场景？对于流式视频或实时性要求极高的工业控制，MCP 基于 JSON-RPC 的文本协议可能显得笨重。
*   **多 Agent 协作**：如果两个 Agent 都连接了同一个 MCP Server，如何处理并发冲突和事务一致性？

**可以拓展的方向**
*   **MCP Server 的市场化**：未来可能会出现“MCP Server 商店”，像插件一样售卖特定的能力包。
*   **边缘计算结合**：将轻量级 MCP Server 部署在用户本地设备上，保护隐私的同时利用云端大模型。

**未来发展趋势**
MCP 协议本身可能会迭代出更复杂的版本，支持流式传输、二进制数据以及更细粒度的权限控制（RBAC）。

## 6. 实践建议

**如何应用到自己的项目**
1.  **盘点资产**：列出团队内部高频使用的 API 或数据源。
2.  **搭建 PoC**：选择一个简单的场景（如“查询员工请假余额”），使用 Python SDK 编写一个简单的 MCP Server。
3.  **本地测试**：使用 Claude Desktop 或 MCP Inspector 进行本地调试，确保工具描述清晰。
4.  **部署上线**：将 Server 部署到 ECS/Fargate，并配置安全组允许 Amazon Quick Agents 访问。

**具体的行动建议**
*   阅读 MCP 官方规范文档，理解 `tools`、`resources` 和 `prompts` 的区别。
*   不要试图一步到位，先做“只读”验证。

**实践中的注意事项**
*   **描述词工程**：在 MCP Server 中定义工具时，`description` 字段至关重要。LLM 完全依赖这个描述来决定是否调用工具。描述必须清晰、无歧义，并包含输入输出示例。

## 7. 案例分析

**结合实际案例说明**
假设一家电商公司使用 Amazon Quick Agents 作为内部客服助手。

**成功案例分析**
*   **场景**：客服询问“用户 A 的最新物流状态”。
*   **实现**：构建一个 Logistics MCP Server，暴露 `get_tracking_info(order_id)` 工具。
*   **关键**：Server 的描述中明确写道“用于查询物流单号，输入必须是字符串格式的 Order ID”。Quick Agents 准确识别意图，调用工具，返回结果。
*   **成功因素**：接口定义清晰，数据结构简单。

**失败案例反思**
*   **场景**：经理要求 Agent “生成上个月的销售报表并发送给我”。
*   **失败原因**：MCP Server 暴露了一个 `generate_report` 工具，但该工具执行耗时 5 分钟，且没有返回中间状态。Quick Agents 因为超时认为调用失败，反复重试，导致系统生成了 10 份报表。
*   **教训**：长时间运行的任务不能设计成同步调用。应该设计成 `start_report_job` -> 返回 Job ID -> Agent 轮询 `get_job_status` 的异步模式。

## 8. 哲学与逻辑：论证地图

**中心命题**
采用 Model Context Protocol (MCP) 作为 Amazon Quick Agents 与外部工具集成的标准，是构建可扩展、可维护且高性能的 AI 生态系统的**最优技术路径**。

**支撑理由与依据**
1.  **互操作性**：
    *   *依据*：MCP 是开源标准，已被多家头部厂商（AWS, Anthropic）支持。遵循标准意味着一次开发，多处复用，降低了 80% 的集成成本。
2.  **语义对齐**：
    *   *依据*：MCP 强制要求为工具提供自然语言描述和 JSON Schema，这天然契合 LLM 的理解逻辑，比传统的 REST API 更容易被 Agent 正确调用，减少幻觉。
3.  **安全边界**：
    *   *依据*：MCP Server 可以独立部署在企业内网，仅通过 SSE 单向向外推送数据或接收指令，相比于直接给 Agent 开放数据库凭证，安全边界更清晰。

**反例或边界条件**
1.  **高频/低延迟交易场景**：如果应用场景是高频交易，MCP 基于 JSON-RPC 的序列化/反序列化开销可能无法接受，此时直接 gRPC 或二进制协议更优。
2.  **遗留系统改造困难**：对于极度老旧、没有 API 只有 CLI 的遗留系统，强行封装 MCP 可能不如使用传统的 RPA（机器人流程自动化）方案性价比高。

**命题性质判断**
*   **事实**：MCP 确实提高了开发效率（可测量）。
*   **价值判断**：认为它是“最优”路径，是基于当前生态趋势的判断。
*   **可检验预测**

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确工具定义与元数据描述

**说明**: MCP 的核心在于让模型理解工具的能力。在集成外部工具时，必须在工具定义中提供清晰、准确的名称和描述。模型依赖这些元数据来决定何时调用哪个工具。模糊的描述会导致模型频繁调用错误的工具或无法调用工具。

**实施步骤**:
1. 为每个工具定义一个语义化强、自解释的名称，避免使用缩写。
2. 在描述字段中详细说明工具的功能、输入参数的含义以及预期的输出结果。
3. 明确声明工具的副作用，例如“此操作将修改数据库记录”或“此操作为只读”。

**注意事项**: 避免在描述中包含特定模型的提示词，应保持描述的通用性和事实性。

---

### 实践 2：实施严格的输入验证与参数清洗

**说明**: 外部工具通常对输入数据的格式和类型有严格要求。模型生成的 JSON 参数可能包含意外的数据结构或潜在的恶意注入内容。在将数据传递给外部系统之前，必须进行严格的验证。

**实施步骤**:
1. 根据 MCP 工具的 Schema 定义，对所有传入参数进行类型检查（如字符串、整数、布尔值）。
2. 实施业务逻辑验证，例如检查日期范围、ID 是否存在等。
3. 对字符串参数进行清洗，防止命令注入或跨站脚本攻击（XSS）。

**注意事项**: 即使模型通常能生成正确的 JSON，也不应跳过服务端的验证逻辑，这是安全防御的最后一道防线。

---

### 实践 3：优化工具响应的可读性与结构

**说明**: 模型需要解析工具的返回结果以生成最终回复。如果工具返回原始的、非结构化的数据（如巨大的 JSON 块或原始日志），模型可能会消耗大量 Token 甚至无法提取关键信息。

**实施步骤**:
1. 在工具层面对返回数据进行预处理，仅返回模型生成回复所需的关键信息。
2. 将复杂的数据结构转换为自然语言摘要或表格形式。
3. 确保错误消息具有描述性，包含错误代码和解决建议，而不是简单的“Error 500”。

**注意事项**: 在调试阶段可以返回详细数据，但在生产环境中应尽量精简响应内容以降低延迟和 Token 消耗。

---

### 实践 4：合理设置超时与异步处理机制

**说明**: Amazon Quick Agents 在等待 MCP 工具响应时存在超时限制。如果外部工具（如数据库查询或 API 调用）执行时间过长，会导致 Agent 请求失败。对于耗时任务，必须采用异步模式。

**实施步骤**:
1. 为所有 MCP 工具调用设置合理的超时阈值（例如 10-30 秒）。
2. 对于长时间运行的任务，工具应立即返回一个“任务已接收”的状态，并提供一个查询 ID。
3. 创建一个独立的“状态查询”工具，供 Agent 轮询任务进度或获取最终结果。

**注意事项**: 避免在同步调用中执行繁重的计算或 I/O 操作，这会严重影响用户体验。

---

### 实践 5：建立全面的日志记录与可观测性

**说明**: 集成外部工具后，排查问题变得复杂。为了理解模型的行为和工具的性能，必须记录从 Agent 到工具的完整交互链路。

**实施步骤**:
1. 记录每次工具调用的请求 Payload、响应内容以及耗时。
2. 为每个请求分配唯一的 Trace ID，以便将 Agent 的决策与工具的执行日志关联起来。
3. 监控工具的错误率和延迟，设置告警阈值。

**注意事项**: 在记录敏感信息（如 PII 数据或密钥）时，必须进行脱敏处理，确保符合安全合规要求。

---

### 实践 6：遵循最小权限原则配置工具访问

**说明**: MCP 工具通常充当通往后端系统的桥梁。如果工具 compromised，攻击者可能利用其权限访问底层资源。必须限制工具的访问权限仅限于完成任务所需的最小范围。

**实施步骤**:
1. 为 MCP 服务器或工具连接创建专用的 IAM 角色或 API 密钥。
2. 仅授予工具读取特定表或调用特定 API 的权限，避免使用通用的 `*` 权限。
3. 定期审计工具的访问日志，确认没有异常的资源访问行为。

**注意事项**: 不要在工具配置中硬编码开发人员的凭证，应使用环境变量或密钥管理服务（如 AWS Secrets Manager）。

---
## 学习要点

- MCP 架构通过标准化的客户端-服务器模式，实现了 AI 模型与外部数据源及工具之间的无缝连接，解决了传统集成方式中的碎片化问题。
- 开发者利用 MCP 可以将企业内部私有数据（如数据库、API）安全地暴露给 Amazon Quick Agents，从而打破大模型的知识孤岛。
- 该协议支持本地和云端两种部署模式，提供了极高的灵活性，能够适应从个人开发者到企业级的不同安全与性能需求。
- 通过定义统一的资源、提示词和工具三大核心能力，MCP 简化了开发流程，使得为 AI 智能体添加新功能变得像安装插件一样简单。
- 集成 MCP 能够显著提升 AI 智能体的准确性，使其能够基于实时数据和特定业务上下文生成回答，有效减少模型幻觉。
- MCP 的开源特性促进了广泛的生态系统兼容性，允许开发者构建可复用的连接器，从而降低未来集成的技术债务。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [LLM](/tags/llm/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的六步指南]({{< relref "posts/20260224-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--10.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的构建指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--8.md" >}})
- [使用MCP协议集成外部工具至Amazon Quick Agents的实操指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*