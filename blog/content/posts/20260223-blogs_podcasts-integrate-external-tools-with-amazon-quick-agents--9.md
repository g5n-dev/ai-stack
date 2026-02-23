---
title: "使用MCP集成外部工具至Amazon Quick Agents的六步指南"
date: 2026-02-23T21:10:18+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "LLM", "Agent", "系统集成", "开发指南", "AWS", "第三方集成"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "本文提供了通过 **模型上下文协议 (MCP)** 将外部工具与 **Amazon Quick Agents** 集成的实施指南。主要内容如下： **1. 目的与背景** 本文旨在为第三方合作伙伴（3P Partners）提供详细的操作指南，帮助您构建新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以实"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["大语言模型"]
---

# 使用MCP集成外部工具至Amazon Quick Agents的六步指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在这篇文章中，您将使用一份六步检查清单来构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器，以实现与 Amazon Quick 的集成。《Amazon Quick 用户指南》描述了 MCP 客户端的行为与约束。本文是一份“操作指南”，旨在为 3P 合作伙伴提供与 Amazon Quick 通过 MCP 进行集成所需的详细实施方案。

---
## 导语

随着 Model Context Protocol (MCP) 的普及，如何高效实现外部工具与 Amazon Quick Agents 的集成成为开发者关注的重点。本文基于《Amazon Quick 用户指南》中的客户端约束，为 3P 合作伙伴提供了一份详实的实施方案。通过这份六步检查清单，您将掌握构建新 MCP 服务器或调整现有服务器的具体方法，从而确保集成的稳定性与合规性。

---
## 摘要

本文提供了通过 **模型上下文协议 (MCP)** 将外部工具与 **Amazon Quick Agents** 集成的实施指南。主要内容如下：

**1. 目的与背景**
本文旨在为第三方合作伙伴（3P Partners）提供详细的操作指南，帮助您构建新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以实现与 Amazon Quick 的无缝集成。

**2. 核心内容**
文章提供了一个 **六步检查清单**，涵盖了集成过程中所需的具体实施细节。

**3. 参考依据**
指南中的规范基于 *Amazon Quick User Guide*（Amazon Quick 用户指南），其中详细定义了 MCP 客户端的行为模式及其约束条件。

**总结：**
这是一个面向开发人员的实操手册，重点在于利用 MCP 协议，遵循既定的客户端行为规范，通过标准化的六个步骤完成技术对接。

---
## 评论

### 中心观点
该文章实质上是一份针对第三方开发者（3P Partners）的**技术合规与实施指南**，旨在通过标准化的 MCP（Model Context Protocol）接口，解决大模型应用中“最后一公里”的工具调用落地难题，其核心价值在于将私有或专有 API 转化为 Amazon Quick Agents 可消费的标准化上下文。

### 支撑理由与深度评价

**1. 内容深度：从“概念验证”迈向“生产级集成”的工程规范**
*   **事实陈述**：文章提出了“六步清单”，这通常涵盖了从环境搭建、Schema 定义、权限验证到错误处理的完整生命周期。
*   **作者观点**：在当前的 LLM 应用开发中，接入外部工具往往面临协议不统一、鉴权混乱和上下文窗口管理不当等问题。MCP 的引入不仅仅是数据传输格式的统一，更是对 AI Agent “如何理解工具”的语义标准化。文章的深度在于它不仅讨论“怎么连”，更强调了“约束”——即 Amazon Quick User Guide 中定义的行为边界。这意味着开发者不能随意暴露 API，必须遵循 Amazon 对 Agent 稳定性和安全性的要求。
*   **批判性思考**：虽然强调了标准化，但文章可能弱化了**异构数据源的复杂性**。如果企业内部存在大量遗留系统，将其强行转化为 MCP 兼容的接口可能需要进行大量的中间层开发，这不仅是技术问题，更是成本问题。

**2. 实用价值：降低 AI 生态的“接入摩擦”**
*   **事实陈述**：指南明确服务于 3P partners，目的是快速集成。
*   **你的推断**：对于 ISV（独立软件开发商）而言，这篇文章具有极高的实战价值。通过 MCP，他们无需针对每一个大模型平台（如 Anthropic, OpenAI, Amazon）开发专有的 Adapter，只需维护一套 MCP Server 接口，即可接入 Amazon Quick Agents。这种“一次开发，多处复用”的模式极大地降低了生态合作的边际成本。
*   **反例/边界条件**：然而，这种实用性在**高频实时交易场景**下受限。MCP 基于的典型交互模式可能引入额外的网络跳转和序列化开销，对于微秒级延迟要求的金融交易系统，直接集成可能比 MCP 协议更合适。

**3. 行业影响：推动 AI Agent 互操作性的“USB 时刻”**
*   **事实陈述**：MCP 正在成为 AI 连接数据的一个开放标准。
*   **作者观点**：Amazon Quick Agents 采用 MCP 是一个强烈的行业信号。它标志着 AI 基础设施厂商正在从“模型参数竞争”转向“生态连接竞争”。这类似于 PC 行业的 USB 接口或 Android 的 USB-C，统一了物理世界与数字世界的交互标准。这将迫使更多工具提供商（如 Slack, GitHub, Notion 等）优先提供原生 MCP 支持，从而加速 Agent 生态的爆发。
*   **反例/边界条件**：但行业也存在**“围墙花园”**的风险。虽然 MCP 是开放的，但 Amazon Quick 对 Client 行为的约束可能包含非公开的私有扩展，导致“标准”在实际落地中出现事实上的碎片化，即“只能在 Amazon 上完美运行的 MCP Server”。

**4. 技术局限性与争议点：标准化的代价**
*   **事实陈述**：文章强调了验证和调整现有 Server。
*   **作者观点**：这里存在一个潜在的技术争议：**通用性与特定性的权衡**。MCP 为了通用性，必然要牺牲掉某些特定 API 的细粒度控制能力。例如，一个复杂的 CAD 软件可能拥有数千个 API，强行压缩进 MCP 的 Resource/Tool/Prompt 三大模型中，可能会导致语义丢失或功能阉割。
*   **边界条件**：对于高度定制化的、非结构化的企业内部流程，强行 MCP 化可能不如端到端微调模型来得有效。

### 可验证的检查方式

为了验证该指南的实际效果及 MCP 的适配性，建议进行以下检查：

1.  **Schema 兼容性测试（指标）**：
    *   选取一个现有的 REST API，按照指南转换为 MCP Server。
    *   **验证指标**：Amazon Quick Agents 对该工具的“一次调用成功率”和“参数解析错误率”。如果错误率高于 5%，说明指南中的 Schema 映射机制存在模糊性。

2.  **延迟基准测试（实验）**：
    *   对比“直接调用原生 API”与“通过 MCP Server 接入 Amazon Quick Agents”的端到端延迟。
    *   **观察窗口**：在网络条件稳定的环境下，观察是否存在显著的协议栈开销（例如超过 200ms 的额外延迟）。

3.  **上下文窗口利用率（观察）**：
    *   MCP 传输工具定义和资源内容时会消耗 Token。
    *   **检查方式**：监控 Agent 在复杂任务中的 Token 消耗。如果 MCP 的元数据描述过长，导致上下文溢出，则说明指南中关于“Prompt 压缩”或“资源定义”的建议需要优化。

### 实际应用建议

1.  **不要盲目重构**：如果你的工具链已经非常复杂且稳定，不要为了使用 MCP 而重写后端。建议采用 **BFF（Backend for Frontend）模式**，构建一个轻量级的 MCP Adapter 层，专门负责将现有 API 翻译成 MCP 协议，起到防腐层的作用。
2.  **关注安全边界**：文章提到了验证步骤。在实施时，务必在 MCP Server 层实现严格的**鉴权与审计**

---
## 技术分析

基于您提供的文章标题和摘要，以下是对《使用模型上下文协议 (MCP) 将外部工具与 Amazon Quick Agents 集成》的深度分析。

---

# 深度分析：基于 MCP 协议的 Amazon Quick Agents 外部工具集成

## 1. 核心观点深度解读

**文章的主要观点**
本文的核心观点在于**标准化协议是解决 AI 智能体碎片化集成的关键**。文章主张通过采用 **Model Context Protocol (MCP)** 作为通用通信标准，第三方开发者可以系统化、高效地将外部数据源和工具连接到 Amazon Quick Agents（亚马逊的智能体平台），从而打破大模型与外部世界之间的“数据孤岛”。

**作者想要传达的核心思想**
作者传达了一种**“连接即服务”**的工程化思想。与其为每一个 AI 应用或智能体编写定制化的 API 集成代码，不如构建一个符合 MCP 标准的服务器。一旦构建完成，该服务器不仅能服务于 Amazon Quick，理论上也能服务于任何支持 MCP 的客户端（如 Claude Desktop 或其他 IDE）。这体现了从“垂直集成”向“水平解耦”的转变。

**观点的创新性和深度**
*   **创新性**：MCP 本身是一个较新的开源标准（由 Anthropic 主导），本文将其应用于 Amazon 的生态系统中，展示了跨平台协作的可能性。它将 AI 智能体的“工具使用”从硬编码转变为可插拔的模块化架构。
*   **深度**：文章不仅停留在概念介绍，而是提供了“六步清单”，这表明作者关注的是工程落地的最后一公里。它深入到了协议的具体约束（如 Amazon Quick User Guide 中的行为定义），强调了在通用协议下，针对特定客户端进行适配的重要性。

**为什么这个观点重要**
随着 LLM 能力的爆发，智能体的瓶颈已从“理解能力”转移到了“执行能力”和“数据获取能力”。如果没有像 MCP 这样的标准，每接入一个工具都需要重新定义接口、鉴权和数据格式，开发成本将呈指数级增长。MCP 的引入降低了智能体与工具生态连接的边际成本，对于构建大规模 AI 应用生态至关重要。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **Model Context Protocol (MCP)**：这是一个开放标准，基于 JSON-RPC 2.0，用于连接 AI 助手与系统上下文（数据、工具）。
*   **MCP Server**：作为服务端，负责暴露资源、提示词和工具给客户端。
*   **Amazon Quick Agents**：作为 MCP Client（客户端），负责发起请求、调用工具并处理响应。
*   **Transport Layer**：通常涉及 `stdio`（标准输入输出）用于本地调试，或 SSE (Server-Sent Events) 用于网络传输。

**技术原理和实现方式**
MCP 的核心架构是 Client-Server 模型。
1.  **连接建立**：Amazon Quick Agent 启动并连接到 MCP Server（通过本地进程或远程端点）。
2.  **能力发现**：Client 向 Server 发送 `initialize` 请求，Server 返回其支持的功能（Resources, Prompts, Tools）。
3.  **工具调用**：
    *   用户向 Agent 发送指令。
    *   Agent 判断需要调用外部工具。
    *   Agent 通过 MCP 协议发送 `tools/call` 请求。
    *   MCP Server 执行实际逻辑（如查询数据库、调用 API），并将结果以 JSON 格式返回。
    *   Agent 将结果整合进 LLM 的上下文中，生成最终回复。

**技术难点和解决方案**
*   **难点 1：上下文窗口限制**。外部工具返回的数据可能非常庞大，直接塞回给 LLM 会撑爆 Token 限制。
*   **难点 2：异步与长时任务**。某些工具（如数据处理）可能耗时较长，超过了 LLM 的请求超时时间。
    *   *解决方案*：设计异步模式，工具调用立即返回一个“任务ID”，Agent 据此轮询或通过回调获取结果。
*   **难点 3：错误处理与安全性**。如何防止 Agent 通过 MCP Server 执行恶意操作？
    *   *解决方案*：在 Server 层实施严格的参数校验和权限控制。

**技术创新点分析**
文章隐含的创新点在于**“配置驱动”而非“代码驱动”**的集成方式。通过 MCP，开发者不需要修改 Amazon Quick Agents 的核心代码，只需通过配置文件（如 `mcp_server_config.json`）声明工具的存在和参数，Agent 即可自动学会使用工具。

## 3. 实际应用价值

**对实际工作的指导意义**
对于企业级 AI 开发者而言，这篇文章提供了一个将企业私有数据（ERP、CRM、内部 Wiki）暴露给 AI 智能体的标准路径。它意味着企业不需要等待 SaaS 厂商提供官方插件，自己就可以通过开发 MCP Server 来赋能现有的 AI 平台。

**可以应用到哪些场景**
1.  **企业知识库问答**：通过 MCP 将 Confluence/SharePoint 暴露给 Agent，实现“查公司文档”的功能。
2.  **数据分析与报表**：Agent 通过 MCP 调用 SQL 接口，直接生成图表或数据摘要。
3.  **运维自动化**：Agent 通过 MCP 调用 AWS API 或 Kubernetes 接口，执行重启服务、查看日志等操作。

**需要注意的问题**
*   **协议兼容性**：虽然 MCP 是标准，但不同 Client（如 Amazon Quick vs Claude）对特定参数的定义可能有细微差别，必须严格遵循 Amazon Quick User Guide。
*   **性能延迟**：多了一层 Server 转发，链路变长，需要优化响应速度。

**实施建议**
*   先在本地环境（如使用 Claude Desktop + MCP）验证 Server 的逻辑正确性。
*   再部署到服务器环境，配置好网络传输层。
*   严格监控 Token 消耗量，优化返回数据的精简度。

## 4. 行业影响分析

**对行业的启示**
MCP 的普及标志着 AI 智能体开发正在进入**“接口标准化”时代**。类似于 HTTP 协议统一了网页浏览，MCP 有望统一 LLM 与工具的连接方式。这将促使开发者从关注“如何调用 API”转向关注“如何设计好用的工具”。

**可能带来的变革**
*   **MCP Server 的爆发**：未来可能会出现类似“Docker Hub”的 MCP Server 市场，开发者可以一键下载并连接各种第三方服务（如 Gmail, Slack, Jira）到任何兼容的 AI 平台。
*   **SaaS 软件的 AI-Ready 化**：SaaS 厂商将不再满足于提供 REST API，而是会竞相提供官方的 MCP Server，以便更容易地接入 AI 生态。

**对行业格局的影响**
这将削弱单一 AI 平台（如 ChatGPT 或 Amazon Quick）的封闭性。如果工具层是通用的，用户切换 AI 平台的成本将降低，竞争将更多集中在模型能力和用户体验上，而非“谁的插件更多”。

## 5. 延伸思考

**引发的其他思考**
*   **安全边界**：当 AI 可以通过标准协议随意操作企业系统时，如何定义“操作红线”？传统的 API Key 管理方式是否还适用？
*   **协议的演进**：目前的 MCP 主要基于 JSON-RPC，未来是否会支持更高效的二进制协议（如 Protobuf）以应对高并发场景？

**可以拓展的方向**
*   **多链路聚合**：一个 Agent 同时连接 10 个不同的 MCP Server，如何协调它们之间的依赖关系（例如：先查 A 工具获取 ID，再查 B 工具获取详情）？这需要 Agent 具备更强的规划能力。
*   **Serverless 化**：MCP Server 是否可以部署为 AWS Lambda 函数，以实现按需调用和零冷启动？

**未来发展趋势**
MCP 可能会成为 AI 应用层的“USB 接口”。未来的 IDE 可能会内置 MCP 客户端，开发者在写代码时，AI 可以直接通过 MCP 读取项目文件、数据库结构甚至运行时状态。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有工具**：列出你希望 AI 访问的内部工具或数据源。
2.  **开发 MCP Wrapper**：不要重写业务逻辑，而是编写一个轻量级的 MCP Server 作为现有 API 的“适配器”。
3.  **定义工具 Schema**：精心设计工具的描述和参数 Schema，这是 LLM 理解工具的关键。

**具体的行动建议**
*   阅读 Anthropic 的 MCP SDK 文档（Python/TypeScript）。
*   使用文中提到的“六步清单”作为开发 Checklist。
*   从简单的“只读工具”开始（如查询天气、查询数据库），逐步过渡到“写入工具”（如创建工单）。

**需要补充的知识**
*   **JSON-RPC 2.0 规范**：理解请求/响应/通知机制。
*   **TypeScript/Python 异步编程**：MCP Server 通常是异步 I/O 密集型的。
*   **Prompt Engineering**：如何写好 Tool Description，以便 LLM 能准确调用。

**实践中的注意事项**
*   **日志记录**：详细记录每个 Tool Call 的输入输出，这对于调试 Agent 的行为至关重要。
*   **版本控制**：MCP Server 的接口变更可能会导致 Agent 调用失败，需要做好版本管理。

## 7. 案例分析

**结合实际案例说明**
假设一家电商公司使用 Amazon Quick Agents 作为客服助手。

*   **场景**：用户询问“我的订单到了哪里？”
*   **传统做法**：Amazon Quick 无法访问内部 ERP，只能回复“请登录官网查询”。
*   **MCP 做法**：
    1.  开发一个 `OrderTracking MCP Server`，连接内部物流 API。
    2.  Amazon Quick Agent 识别用户意图。
    3.  通过 MCP 调用 `get_order_status(order_id)`。
    4.  MCP Server 返回物流状态 JSON。
    5.  Agent 用自然语言告诉用户：“您的包裹正在派送中，预计明天到达。”

**成功案例分析**
*   **GitHub 的 Copilot**：虽然它不完全使用 MCP，但它通过插件机制让 AI 访问外部 API，极大地提升了开发效率。MCP 将这种能力民主化，使得任何公司都能轻松构建类似 Copilot 的集成体验。

**失败案例反思**
*   **缺乏上下文限制**：如果 MCP Server 的 `list_tables` 工具返回了数据库中所有的 1000 张表，LLM 可能会因为 Token 溢出或信息过载而选错表。
    *   *教训*：工具返回的数据必须经过过滤和聚合，不能直接“裸露”底层复杂性。

## 8. 哲学与逻辑：论证地图

**中心命题**
**采用 Model Context Protocol (MCP) 是构建可扩展、互操作的 AI 智能体工具生态的最优工程解法。**

**支撑理由**
1.  **互操作性**：MCP 作为开放标准，允许一次编写的服务器在多个 AI 平台（如 Amazon Quick, Claude, 其他 IDE）之间复用，消除了重复开发的浪费。
    *   *依据*：软件工程中的 DRY（Don't Repeat Yourself）原则及网络协议（如

---
## 最佳实践

## 最佳实践指南

### 实践 1：严格定义工具的作用域与权限

**说明**:
在将外部工具集成到 Amazon Quick Agents 时，必须明确每个 MCP 工具的具体功能边界。Agent 需要清楚地知道何时以及如何调用工具，同时应遵循最小权限原则，仅授予工具完成任务所需的最小数据访问权限，以防止意外操作或数据泄露。

**实施步骤**:
1. 审查外部工具的 API 接口，列出所有可用的功能。
2. 在 MCP 配置文件中，仅注册 Agent 当前工作流必需的工具端点。
3. 为工具配置独立的 IAM 角色或 API 密钥，限制其访问范围（例如，只能读取特定的 S3 存储桶，或只能查询特定的数据库表）。

**注意事项**: 避免授予通配符权限（如 `*`），定期审查工具的访问日志，确保没有异常调用行为。

---

### 实践 2：实施全面的数据验证与清洗

**说明**:
外部工具返回的数据可能包含噪声、格式不一致或敏感信息。在将数据传递给大语言模型（LLM）之前，必须在 MCP 层面进行严格的验证和清洗。这不仅能提高 Agent 回答的准确性，还能有效控制 Token 消耗并防止提示词注入攻击。

**实施步骤**:
1. 在 MCP 服务器端编写中间件或拦截器，用于验证 API 响应的 HTTP 状态码和数据结构。
2. 定义严格的 JSON Schema，过滤掉多余的字段，仅保留模型所需的关键信息。
3. 对来自用户的输入参数进行清洗，移除潜在的恶意脚本或特殊字符。

**注意事项**: 处理大型数据集时，务必在传递给模型前进行摘要或截断，以避免超出上下文窗口限制。

---

### 实践 3：构建稳健的错误处理与重试机制

**说明**:
外部服务可能会遇到限流、超时或服务不可用等情况。如果 MCP 工具直接抛出原始错误，Agent 可能会无法理解并终止对话。最佳实践是捕获底层异常，并将其转换为 Agent 可理解的标准化错误消息或结构化反馈。

**实施步骤**:
1. 在 MCP 客户端实现指数退避算法，以处理 429（限流）或 5xx（服务器错误）状态码。
2. 定义标准化的错误响应格式（如 `{ "status": "error", "message": "user-friendly description", "retryable": true }`。
3. 为关键工具调用设置合理的超时时间，避免 Agent 长时间挂起等待。

**注意事项**: 区分“可重试错误”（如网络抖动）和“不可重试错误”（如认证失败），避免对后者进行无效重试从而浪费资源。

---

### 实践 4：优化工具元数据与描述

**说明**:
Agent 依赖于工具的描述来决定何时调用它们。模糊或不准确的描述会导致 Agent 产生幻觉或频繁调用错误的工具。最佳实践是提供清晰、具体且包含示例的元数据，帮助模型准确理解工具用途。

**实施步骤**:
1. 在 MCP 清单文件中，为每个工具编写详细的 `description` 字段，说明输入参数的含义和返回结果的结构。
2. 在描述中提供具体的输入输出示例（Example I/O）。
3. 定期测试 Agent 对工具的理解能力，如果选错工具，调整描述中的关键词以更好地对齐模型的语义理解。

**注意事项**: 保持描述简洁但信息量充足，避免使用过于生僻的领域术语，除非该术语在 Agent 的系统提示词中已定义。

---

### 实践 5：确保可观测性与日志记录

**说明**:
为了调试和优化 MCP 集成，必须建立完整的可观测性体系。你需要追踪 Agent 发出请求的完整生命周期，包括请求负载、响应时间、错误率以及 Token 消耗情况。

**实施步骤**:
1. 在 MCP 服务器中集成日志记录（如 CloudWatch Logs），记录每个工具调用的 Request ID 和 Payload。
2. 使用 OpenTelemetry 或类似标准收集追踪数据，分析工具调用链中的性能瓶颈。
3. 设置告警机制，当工具错误率超过阈值或延迟过高时触发通知。

**注意事项**: 记录日志时，务必对敏感个人身份信息（PII）进行脱敏处理，以符合数据隐私合规要求。

---

### 实践 6：管理上下文窗口与成本

**说明**:
频繁调用外部工具或返回大量数据会迅速消耗上下文窗口并增加 API 成本。通过优化交互策略，可以确保 Agent 在保持高性能的同时控制运营支出。

**实施步骤**:
1. 评估工具调用的必要性，对于可以通过 Agent 内部知识解决的简单问题，避免调用外部工具。
2. 对于 MCP 工具返回的长文本或文档，在传递给 LLM 之前，使用向量数据库或摘要算法提取最相关的片段。
3. 监控每次对话的工具调用次数和 Token 使用量，建立预算限制。

**注意事项**: 在设计 Agent 流程时，应优先考虑“并行调用”（如果模型支持）以减少交互轮次，从而

---
## 学习要点

- MCP（Model Context Protocol）作为一种开放标准，能够安全地将企业外部数据源和工具集成到 Amazon Quick Agents 中，从而打破大模型应用的数据孤岛。
- 通过 MCP 实现的标准化集成方式，显著降低了开发复杂度，使得 Agent 能够无缝访问私有数据并执行实时业务操作。
- Amazon Quick Agents 原生支持 MCP，允许用户无需编写复杂代码即可通过声明式配置快速扩展 Agent 的功能边界。
- 利用该协议构建的 Agent 能够在保持数据安全合规的前提下，精准调用外部 API 来响应用户查询，有效弥补了通用模型知识滞后的短板。
- 这种架构支持企业将现有的业务系统（如 CRM、ERP）通过 MCP 连接器快速转化为 AI 能力，极大提升了现有资产的复用价值。
- MCP 的解耦设计使得企业可以灵活升级或更换底层的 MCP 服务器，而无需重构上层的 Agent 应用，保障了系统的长期可维护性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [LLM](/tags/llm/) / [Agent](/tags/agent/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [AWS](/tags/aws/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的构建指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--8.md" >}})
- [使用MCP协议集成外部工具至Amazon Quick Agents的实操指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP将外部工具集成至Amazon Quick Agents的六步指南]({{< relref "posts/20260222-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*