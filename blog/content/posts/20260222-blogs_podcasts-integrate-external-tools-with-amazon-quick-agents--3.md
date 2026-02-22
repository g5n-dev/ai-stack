---
title: "使用MCP集成Amazon Quick Agents的外部工具实施指南"
date: 2026-02-22T02:59:35+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "LLM", "Agent", "工具集成", "模型上下文协议", "开发指南", "AWS"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "**中文总结：** 本文旨在指导第三方合作伙伴如何使用**模型上下文协议（MCP）**将外部工具集成到 **Amazon Quick Agents** 中。 文章提供了一个**六步清单**，帮助开发者从头构建一个新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以符合 Amazon Quick 的集成要求"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["大语言模型"]
---

# 使用MCP集成Amazon Quick Agents的外部工具实施指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在本文中，您将使用一份六步检查清单来构建新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以实现与 Amazon Quick 的集成。《Amazon Quick 用户指南》描述了 MCP 客户端的行为和约束。这是一份“操作指南”，面向 3P 合作伙伴为通过 MCP 与 Amazon Quick 集成所需的详细实施工作。

---
## 导语

随着 Amazon Quick Agents 的推出，如何高效集成外部工具成为开发者关注的焦点。本文将基于 Model Context Protocol (MCP)，提供一份涵盖构建与验证的六步检查清单，旨在解决第三方合作伙伴在集成过程中面临的实施细节与合规性挑战。通过阅读本文，技术团队将获得清晰的路径，确保外部服务能够顺畅、安全地接入 Amazon Quick 生态。

---
## 摘要

**中文总结：**

本文旨在指导第三方合作伙伴如何使用**模型上下文协议（MCP）**将外部工具集成到 **Amazon Quick Agents** 中。

文章提供了一个**六步清单**，帮助开发者从头构建一个新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以符合 Amazon Quick 的集成要求。文中详细说明了 Amazon Quick 用户指南中定义的 MCP 客户端行为及其约束条件，是针对第三方合作伙伴进行具体实施操作的详细“操作指南”。

---
## 评论

**文章核心观点**
该文章旨在为第三方开发者提供一份构建符合 Amazon Quick Agents 规范的 MCP（Model Context Protocol）服务器的标准化指南。通过遵循“六步检查清单”，开发者能够实现大语言模型与外部数据源及工具的连接，从而完成系统集成。

**技术支撑与逻辑分析**

**1. 协议标准化解决集成异构性问题**
MCP 的核心价值在于提供统一的接口标准。文章描述的适配流程，实质上是将 API 调用、权限验证和数据格式转换逻辑进行标准化。从技术角度看，这解决了 LLM 应用开发中常见的接口碎片化问题。以往连接 Salesforce、Slack 或内部 ERP 需要编写不同的连接器，现在通过 MCP 可以统一 Schema。这减少了重复开发，并规范了 API 调用逻辑。

**2. 强调“安全与验证”是企业级应用的基础**
文章摘要中提到的“验证和调整”环节，暗示了 MCP Client（即 Amazon Quick）对服务器的技术约束。MCP 在此不仅作为数据传输协议，也承担了权限与边界管理的功能。文章若能详细阐述 Quick Agents 如何限制 MCP Server 的访问权限（如数据范围限制），将有助于更准确地说明其安全模型。这种边界控制是区分企业级应用与普通工具集成的重要特征。

**3. 生态系统的技术规范策略**
亚马逊推出 Quick Agents 并推广 MCP 集成，旨在构建 AWS 的 AI 生态技术规范。通过定义 MCP Client 的行为标准，亚马逊制定了接入的技术规则。对于 3P（第三方）合作伙伴而言，遵循这一指南意味着其产品符合 AWS 的接入要求。这种策略通过技术文档明确了合规性标准。

**反例与边界条件**

*   **反例 1：高频实时场景的局限性**
    MCP 模式通常基于请求-响应或 SSE（Server-Sent Events）。对于需要毫秒级低延迟或高频双向通信的场景（如在线游戏协作、实时高频交易），MCP 的序列化开销和上下文切换可能导致性能瓶颈，其效率可能不如原生 WebSocket 或 gRPC 直接调用。
*   **反例 2：非结构化数据处理能力的边界**
    MCP 擅长连接工具和结构化数据。对于需要深度处理非结构化数据（如分析海量 PDF 语意、复杂图像生成）的任务，仅靠 MCP 传递参数可能不足以支撑完整工作流，往往需要 Agent 具备更强的原生推理能力或集成 RAG 管道，MCP 在此主要承担数据传输职能。

**多维度评价**

1.  **内容深度：** 作为一篇“操作指南”，其深度取决于技术细节的颗粒度。如果仅列出清单，深度中等；若包含错误处理、身份认证的具体代码示例，则深度较高。从行业角度看，它填补了“协议标准”到“商业产品”之间的落地空白。
2.  **实用价值：** 较高。对于 SaaS 厂商和技术集成商，这是将产品接入 AWS AI 生态的直接参考，具有明确的技术实施指导意义。
3.  **创新性：** 观点属于技术演进（API 联盟早已有之），但 MCP 试图成为 AI 领域的通用接口标准，这种跨平台的标准化尝试具有技术参考价值。
4.  **可读性：** 清单体结构逻辑清晰，易于工程师按步骤实施，但技术文档通常侧重操作流程，较少涉及架构设计的宏观阐述。
5.  **行业影响：** 如果 MCP 被广泛采用，将影响中间件市场的发展方向。传统的 ETL/ELT 工具可能面临转型，基于语义的“意图-工具”映射层可能成为新的基础设施。

**可验证的检查方式**

1.  **集成成功率指标：** 按照文章指南构建的 MCP Server，在 Amazon Quick Agents 的“连接测试”阶段，通过验证（握手、Schema 校验、权限测试）的比例。如果成功率较低，说明文档存在模糊地带或实现难度被低估。
2.  **延迟与吞吐量测试：** 构建一个测试环境，观察通过 MCP 调用外部工具的平均响应时间。若 P99 延迟显著高于直接 API 调用，则证明了协议层存在客观开销。
3.  **社区采纳率观察：** 在未来的一段时间内，观察 GitHub 或 AWS Marketplace 上声明支持 "Amazon Quick Agents MCP" 的第三方工具数量。如果增长缓慢，说明该标准的普及程度可能有限。

---
## 技术分析

基于您提供的文章标题和摘要，以下是对《使用模型上下文协议 (MCP) 将外部工具集成到 Amazon Quick Agents》一文的深入分析。

---

# 深度分析报告：基于 MCP 的 Amazon Quick Agents 外部工具集成

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**标准化协议（MCP）是打破 AI Agent 与外部数据/工具孤岛的关键**。通过遵循 Model Context Protocol (MCP) 这一开放标准，第三方开发者能够以统一、高效的方式将自有工具和数据源接入 Amazon Quick Agents（Amazon Q 的自主代理组件），从而显著扩展 Agent 的能力边界。

### 作者想要传达的核心思想
作者旨在传达**“互操作性优于定制化”**的工程哲学。在传统的 AI 应用开发中，为每一个大模型应用或 Agent 编写自定义 API 集成是低效且难以维护的。MCP 提供了一种通用的“语言”，使得 Amazon Quick 能够像调用本地功能一样调用远程工具。文章强调，通过一套六步检查清单，开发者可以确保其 MCP 服务器符合 Amazon Quick 的特定行为约束和性能要求。

### 观点的创新性和深度
- **创新性**：MCP 本身是 AI 领域较新的协议标准（由 Anthropic 主导），亚马逊将其集成到 Quick Agents 中，标志着云厂商开始从“封闭生态”转向“协议标准化生态”。这不仅仅是技术集成，更是生态构建策略的转变。
- **深度**：文章不仅停留在“如何连接”，更深入到了“验证与调整”。摘要中提到的“MCP client behavior and constraints”（MCP 客户端行为与约束）表明，文章探讨了服务器端如何适配客户端的特定限制（如超时、数据格式、安全沙箱），这是生产环境落地的关键细节。

### 为什么这个观点重要
随着 AI Agent 从“聊天机器人”向“行动者”转变，**工具调用**成为瓶颈。如果每个 SaaS 软件都需要 Amazon 专门编写集成代码，生态扩展将极其缓慢。MCP 的引入意味着：
1.  **降低门槛**：数以万计的 SaaS 提供商可以轻松成为 Amazon Q 的生态伙伴。
2.  **统一体验**：用户无需关心工具背后的实现细节，交互体验一致。
3.  **企业级就绪**：通过标准化的安全和管理机制，解决企业级 AI 应用中“数据孤岛”的痛点。

---

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Model Context Protocol (MCP)**：一种开放协议，用于连接 AI 应用与数据源（如数据库、文件系统、API）。它定义了请求、响应、资源和提示的交换格式。
2.  **Amazon Quick Agents**：Amazon Q 业务版中的自主代理功能，能够执行多步骤任务。
3.  **MCP Server（服务端）**：托管数据和工具逻辑的一方，负责响应 Amazon Quick（客户端）的查询。
4.  **MCP Client（客户端）**：在此文中指 Amazon Quick Agents，负责发起连接和调用。

### 技术原理和实现方式
-   **架构模式**：采用 Client-Server 架构。Amazon Quick 作为 MCP Client，通过传输层（通常是 WebSocket 或 HTTP，取决于 MCP 具体实现）连接到第三方的 MCP Server。
-   **能力发现**：Server 启动时会向 Client 暴露其提供的“工具”、“资源”和“提示”。Client 会动态注册这些能力，使 LLM 能够感知并调用它们。
-   **执行流**：
    1.  用户向 Amazon Quick 发出指令（例如：“查询 Salesforce 中的最新订单”）。
    2.  Amazon Quick 识别意图，路由到对应的 MCP Server。
    3.  MCP Server 执行实际逻辑（查询 Salesforce API）。
    4.  数据以标准 JSON 格式返回给 Amazon Quick。
    5.  Amazon Quick 结合上下文生成最终回复。

### 技术难点和解决方案
-   **难点1：上下文窗口限制**。外部工具返回的数据可能非常大，直接塞入 LLM 上下文会导致成本激增或截断。
    -   **解决方案**：MCP 支持流式传输和资源引用。文章可能涉及如何优化 Server 返回的数据结构，仅返回摘要或通过 URI 引用资源，而非全文。
-   **难点2：认证与安全**。企业数据不能通过未加密通道传输。
    -   **解决方案**：MCP 支持多种认证机制。在 Amazon Quick 环境中，通常涉及 IAM 角色或 OAuth 2.0 的集成，Server 必须验证 Quick 的访问令牌。
-   **难点3：错误处理与超时**。Agent 调用外部工具可能失败或耗时过长。
    -   **解决方案**：文章提到的“六步检查清单”中必然包含对超时设置、错误码标准化以及重试机制的验证。

### 技术创新点分析
文章的核心创新在于**将通用的 MCP 协议适配到了特定的企业级 Agent 运行时**。这不仅仅是协议的实现，还涉及**资源管理策略**——即如何确保 Agent 在调用外部工具时不会破坏企业现有的权限模型。

---

## 3. 实际应用价值

### 对实际工作的指导意义
对于 3P（第三方）开发者和企业 IT 团队而言，这篇文章提供了一份**“合规指南”**。它告诉开发者：仅仅实现一个 MCP Server 是不够的，还必须满足 Amazon Quick 的特定约束（如响应速度、并发处理能力）。这避免了开发者盲目开发后无法接入的问题。

### 可以应用到哪些场景
1.  **企业知识库查询**：将公司内部的 Confluence、SharePoint、Legacy DB 封装为 MCP Server，供 Amazon Quick 查询。
2.  **业务流程自动化**：通过 MCP Server 暴露 API，让 Amazon Quick 能够执行 ERP 中的操作（如审批、创建工单）。
3.  **SaaS 集成**：独立软件开发商（ISV）将其产品功能通过 MCP 开放给 Amazon Q 用户，无需单独开发插件。

### 需要注意的问题
-   **延迟敏感度**：Agent 交互是实时的，如果 MCP Server 响应慢，用户体验会极差。
-   **数据隐私**：必须明确数据流向。是数据传给 Amazon Quick 处理，还是 Quick 仅发送指令？这决定了合规性。
-   **版本兼容性**：MCP 协议本身在迭代，Amazon Quick 的客户端行为也可能变化，Server 需要具备向后兼容性。

### 实施建议
在实施前，先利用文中提到的“六步检查清单”进行本地测试。不要直接在生产环境部署。建议先从只读操作（如查询）开始，验证通过后再接入写操作（如修改数据）。

---

## 4. 行业影响分析

### 对行业的启示
这篇文章标志着 **AI 互操作性的“HTTP 时刻”**。正如 HTTP 统一了网页浏览，MCP 有望统一 LLM 与工具的连接方式。行业将从“为每个模型开发 Adapter”转向“开发一次 MCP Server，到处运行”。

### 可能带来的变革
-   **中间件市场的兴起**：未来可能会出现专门提供“MCP Gateway”的服务，用于将旧 API 转换为 MCP 协议。
-   **Agent 商店模式**：类似于手机应用商店，未来可能出现“Agent 工具商店”，用户只需一键订阅某个 MCP Server，即可赋予 Agent 新技能。

### 相关领域的发展趋势
-   **协议标准化竞争**：除了 MCP，OpenAI 也有 Function Calling 的定义，LangChain 也有 Tool 标准。MCP 的胜出取决于亚马逊、Anthropic 等巨头的支持力度。
-   **边缘侧 Agent**：随着 MCP 普及，企业可能会在本地（On-Premise）部署 MCP Server，而将推理放在云端，解决数据不出域的问题。

### 对行业格局的影响
这削弱了单一 SaaS 巨头的护城河，增强了**连接器平台**（如 Amazon AWS）的话语权。谁能成为连接 AI 与企业数据的“枢纽”，谁就掌握了下一轮流量入口。

---

## 5. 延伸思考

### 引发的其他思考
-   **安全边界的模糊**：当 Agent 可以通过 MCP 调用删除文件的 API 时，如何防止 Prompt Injection（提示词注入）攻击导致的数据灾难？
-   **成本分摊**：MCP Server 运行在第三方，谁来承担 Token 成本和计算成本？是否需要 Metering（计量）机制？

### 可以拓展的方向
-   **MCP for Mobile**：目前 MCP 多用于云端服务，未来是否可以延伸到手机本地 App，让手机上的 AI 直接调用 App 的本地功能？
-   **多 Agent 协作**：如果多个 Agent 都支持 MCP，它们之间是否可以通过 MCP 协议直接通信，而无需通过 LLM 中转？

### 需要进一步研究的问题
-   MCP 协议在处理流式数据时的具体性能表现。
-   如何在 MCP 层面实现细粒度的权限控制（例如，Agent 只能读取用户 A 的数据，不能读取用户 B 的）。

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有 API**：检查你现有的 SaaS 产品或内部工具是否具备 RESTful/GraphQL API。
2.  **开发 MCP Wrapper**：不要重写逻辑，而是编写一个轻量级的 MCP Server 层，将现有 API 映射为 MCP Tools。
3.  **本地测试**：使用 MCP Inspector（官方调试工具）验证 Server 行为。
4.  **接入 Amazon Quick**：按照文章的六步清单，在 Amazon Q 控制台配置数据源。

### 具体的行动建议
-   **阅读协议规范**：深入理解 MCP 的 `resources`、`prompts` 和 `tools` 三大核心概念的区别。
-   **安全第一**：在 Server 端实现严格的入参校验，防止 SQL 注入或命令注入。
-   **日志记录**：记录所有 Agent 的调用请求，这对于审计和调试至关重要。

### 需要补充的知识
-   **TypeScript/Python**：目前 MCP SDK 主要支持这两种语言。
-   **异步编程**：MCP Server 必须是异步非阻塞的，以处理高并发请求。

### 实践中的注意事项
-   **不要过度暴露功能**：不要把所有内部 API 都变成 MCP Tools。只暴露那些对 LLM 有意义、参数清晰的接口。
-   **处理分页**：如果 API 返回大量列表，MCP Server 必须智能处理分页，而不是一次性返回导致上下文溢出。

---

## 7. 案例分析

### 结合实际案例说明
**案例：一家企业将其内部 HR 系统接入 Amazon Quick。**
*   **背景**：员工经常向 HR 咨询假期余额，但需要登录旧系统查询。
*   **实施**：开发 MCP Server，提供 `get_leave_balance` 工具，接收 `employee_id` 参数。
*   **效果**：员工直接向 Amazon Quick 问“我还剩几天年假？”，Quick 通过 MCP 调用 HR 系统返回结果。

### 成功案例分析
**Slack 的集成（假设性）**：如果 Slack 开发了一个 MCP Server，Amazon Quick 就可以直接在 Agent 对话中读取 Slack 消息或发送通知。这种“

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确工具定义与能力边界

**说明**:
在集成之前，必须清晰定义每个外部工具的具体功能、输入输出模式以及能力边界。这有助于 Quick Agents 准确理解何时以及如何调用该工具，避免无效调用或错误操作。

**实施步骤**:
1. 列出工具的核心功能清单，明确它能解决的具体问题。
2. 详细定义工具的参数结构，包括数据类型和必填字段。
3. 在 MCP 配置中编写清晰的描述信息，确保模型能理解工具用途。

**注意事项**:
避免定义过于宽泛的工具功能，这可能导致模型产生幻觉或误用工具。功能描述应尽可能具体和聚焦。

---

### 实践 2：优化数据架构与上下文管理

**说明**:
MCP 允许模型访问外部数据源。为了提高响应速度和准确性，需要优化数据架构，确保只传输必要的数据，并有效管理上下文窗口，防止信息过载。

**实施步骤**:
1. 对外部数据源进行预处理，建立索引或摘要，减少实时检索的数据量。
2. 配置 MCP 资源时，限制每次返回的数据大小。
3. 实施分块检索策略，仅根据 Agent 当前需求加载相关上下文。

**注意事项**:
监控 Token 使用情况。过大的上下文不仅会增加成本，还可能降低模型的推理能力。

---

### 实践 3：实施严格的输入验证与安全防护

**说明**:
外部工具接口可能成为安全漏洞的入口。必须对所有传入 MCP 工具的参数进行严格验证，防止注入攻击或未授权的系统操作。

**实施步骤**:
1. 在 MCP 服务器端实施 Schema 验证，确保所有输入符合预期的格式和类型。
2. 对连接外部工具的 API 密钥和敏感信息进行加密存储，不要硬编码在配置文件中。
3. 使用 IAM 角色和最小权限原则配置 Quick Agents 对外部工具的访问权限。

**注意事项**:
定期审计访问日志，检查是否有异常的调用模式或参数传递，确保系统合规性。

---

### 实践 4：构建稳健的错误处理与重试机制

**说明**:
外部工具调用可能会因为网络问题、服务不可用或无效参数而失败。良好的错误处理机制能确保 Agent 在遇到这些情况时能够优雅降级或尝试恢复。

**实施步骤**:
1. 在 MCP 集成层定义标准化的错误代码和消息格式。
2. 实现指数退避重试策略，处理暂时性网络故障。
3. 为 Quick Agents 提供清晰的错误反馈，使其能够根据错误信息生成面向用户的自然语言解释。

**注意事项**:
避免无限重试导致系统挂起。设置最大重试次数和超时限制，并确保错误消息不会泄露敏感的系统内部信息。

---

### 实践 5：利用 Prompt 模板引导工具调用

**说明**:
虽然 MCP 负责连接，但 Quick Agents 的行为仍受 Prompt 指导。通过精心设计的 Prompt 模板，可以显著提高模型调用工具的准确性和逻辑性。

**实施步骤**:
1. 在系统提示词中明确列出可用工具及其适用场景。
2. 提供少样本示例，展示在何种情况下应调用特定工具以及如何构造参数。
3. 指导模型在缺乏必要参数时主动向用户提问，而不是编造数据。

**注意事项**:
Prompt 需要根据工具的迭代更新而同步维护，防止描述与实际功能脱节。

---

### 实践 6：全面监控与日志记录

**说明**:
为了持续优化集成效果，必须建立全面的监控体系，跟踪工具调用的成功率、延迟以及用户满意度。

**实施步骤**:
1. 启用 CloudWatch 或其他监控服务，记录 MCP 服务的请求和响应指标。
2. 记录每次工具调用的上下文，包括触发意图、传递参数和返回结果。
3. 定期分析日志，识别高频错误或性能瓶颈。

**注意事项**:
在记录日志时，务必对敏感个人身份信息（PII）进行脱敏处理，以符合数据隐私法规。

---

### 实践 7：遵循异步设计与长时执行模式

**说明**:
某些外部工具（如数据处理或报表生成）可能需要较长时间才能完成。在设计 MCP 集成时，应考虑异步处理模式，避免阻塞 Agent 的响应。

**实施步骤**:
1. 对于耗时任务，设计异步接口，立即返回一个“任务已接收”的确认和任务 ID。
2. 实现 Webhook 或轮询机制，让 Agent 能够在后台查询任务状态。
3. 在用户界面中提供状态反馈，告知用户操作正在进行中。

**注意事项**:
确保异步任务的状态存储具有持久性，防止服务重启导致任务状态丢失。

---
## 学习要点

- MCP 通过标准化的接口将外部工具和数据源无缝集成到 Amazon Quick Agents 中，打破了 AI 应用与外部系统之间的连接壁垒。
- 开发者无需编写复杂的自定义代码，只需配置 MCP 服务器即可快速扩展 Agent 的功能，显著降低了开发难度和时间成本。
- 该协议支持动态上下文检索，使 Agent 能够在执行任务时实时访问最新的外部数据，从而大幅提高响应的准确性。
- 借助 MCP，Amazon Quick Agents 能够跨越系统孤岛执行复杂的多步骤工作流，实现端到端的业务自动化。
- 采用 MCP 这一开放标准架构增强了解决方案的互操作性和未来适应性，使企业能够灵活应对 AI 技术的快速迭代。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [LLM](/tags/llm/) / [Agent](/tags/agent/) / [工具集成](/tags/%E5%B7%A5%E5%85%B7%E9%9B%86%E6%88%90/) / [模型上下文协议](/tags/%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [深度解析Skill/MCP/RAG等五大AI技术的底层逻辑]({{< relref "posts/20260212-juejin-深入理解skillmcpragagentopenclaw底层逻辑-2.md" >}})
- [Agent Skills：智能体技能框架与开发指南]({{< relref "posts/20260203-hacker_news-agent-skills-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*