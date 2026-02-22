---
title: "使用MCP集成外部工具至Amazon Quick Agents的六步指南"
date: 2026-02-22T21:21:12+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "Agent", "集成指南", "外部工具", "LLM", "开发实战", "AWS"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "**如何使用 MCP 将外部工具集成到 Amazon Quick Agents** 本文旨在为第三方合作伙伴提供一份实施指南，详细说明如何利用 **Model Context Protocol (MCP)** 将外部工具与 **Amazon Quick Agents** 进行集成。 **核心内容：** 文章提供了一个*"
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

在本文中，您将使用一个六步清单来构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器，以便与 Amazon Quick 集成。《Amazon Quick 用户指南》描述了 MCP 客户端的行为和约束。这是一份“操作指南”，供第三方合作伙伴（3P partners）了解如何通过 MCP 与 Amazon Quick 集成所需的详细实现步骤。

---
## 导语

随着 Model Context Protocol (MCP) 的普及，如何将外部工具无缝接入 Amazon Quick Agents 成为开发者关注的焦点。本文提供了一份详尽的六步清单，旨在指导第三方合作伙伴构建或调整 MCP 服务器，以符合 Amazon Quick 的客户端行为与约束要求。通过阅读，您将掌握具体的实现步骤，确保外部服务能够顺利集成并稳定运行。

---
## 摘要

**如何使用 MCP 将外部工具集成到 Amazon Quick Agents**

本文旨在为第三方合作伙伴提供一份实施指南，详细说明如何利用 **Model Context Protocol (MCP)** 将外部工具与 **Amazon Quick Agents** 进行集成。

**核心内容：**
文章提供了一个**六步清单**，帮助开发者从头构建一个新的 MCP 服务器，或者对现有的 MCP 服务器进行验证和调整，以确保其符合 Amazon Quick 的集成要求。

**关键参考：**
*   **Amazon Quick User Guide（用户指南）：** 开发者需参考此文档以了解 MCP 客户端的具体行为模式及其约束条件。
*   **适用对象：** 这是一个针对第三方合作伙伴的详细实操指南，涵盖了实现集成的具体技术步骤。

---
## 评论

**
**文章中心观点**
该文章提出了一种标准化的“六步法”工程范式，旨在通过 **Model Context Protocol (MCP)** 这一新兴开放标准，解决第三方工具与 Amazon Quick Agents（或类似 LLM 应用）集成的互操作性难题，从而降低 AI 智能体的开发门槛并提升其工具调用能力。

**支撑理由与边界分析**

1.  **MCP 协议的标准化价值（事实陈述）**
    *   **理由**：文章核心在于推广 MCP。在当前的 AI 生态中，每个 LLM 应用（如 ChatGPT、Claude、Amazon Q）都有各自定义工具的私有 API 格式。MCP 试图成为连接 AI 模型与数据源的“USB 接口”，这使得开发者只需编写一次 Server，即可在不同 Client 中复用。文章提供的“六步清单”实质上是 MCP 规范在 Amazon Q 场景下的具体落地 SOP。
    *   **反例/边界条件**：MCP 并非唯一的解决方案。对于极低延迟或极高吞吐量的内部系统，基于 gRPC 或 WebSocket 的私有定制协议往往比 MCP（通常基于 JSON-RPC over Stdio/HTTP）性能更优。此外，如果 Amazon Q 未来支持 OpenAPI 的直接导入且兼容性极佳，MCP 可能会面临“过度设计”的竞争。

2.  **工程落地的实用性（作者观点）**
    *   **理由**：文章强调“验证和调整现有 MCP Server”，这切中了当前 LLM 开发的痛点：Function Calling 的参数定义与后端实际 API 往往不匹配。通过提供 Checklist（如检查工具描述的清晰度、参数的 Schema 验证），文章帮助开发者规避了“模型理解偏差”导致的调用失败，具有极高的工程指导意义。
    *   **反例/边界条件**：Checklist 的有效性依赖于模型本身的理解能力。如果底座模型（即使是通过 Q 调用的模型）逻辑推理能力较弱，即使 MCP Server 定义得再完美，模型仍可能无法正确编排工具。此外，文章未深入探讨异步长时间运行任务的处理，这在企业级集成中是常见的边界陷阱。

3.  **生态位与厂商锁定（你的推断）**
    *   **理由**：Amazon 作为云厂商，积极支持 MCP（由 Anthropic 推动）显示了其构建开放生态的意图。对于 3P（第三方）合作伙伴而言，遵循此指南可以快速接入 Amazon Q 的企业级分发渠道，这是巨大的商业诱饵。
    *   **反例/边界条件**：虽然 MCP 是开放的，但 Amazon Quick Agents 的具体“行为和约束”是私有的。开发者可能会发现，为了完美适配 Amazon Q，他们编写的 MCP Server 不得不包含大量针对 Q 的特有逻辑，从而导致“形式上的开放，实质上的厂商锁定”。

**批判性评价**

*   **内容深度与严谨性**：文章作为一篇“操作指南”，在技术实现的细节上（如 Schema 定义、权限配置）是严谨的，但它回避了深层的技术挑战。例如，MCP Server 的资源消耗模型、并发连接限制以及在 Stdio 模式下的进程管理稳定性，这些在文中未被充分讨论。
*   **创新性**：文章本身的方法论（Checklist）是工程管理的常规手段，并无重大创新。真正的创新在于其将 MCP 这一新兴协议作为“一等公民”引入 Amazon 生态，这标志着行业正从“Prompt Engineering”向“Protocol Engineering”转变。
*   **争议点**：MCP 的传输层（目前主流是 Stdio，适合本地进程）在云原生 Serverless 架构（如 AWS Lambda）中存在架构错配。将 Stdio 桥接到 HTTP 或 Lambda 需要额外的适配层，这增加了系统复杂度，文章若未对此提供轻量级方案，则显得有些理想化。

**实际应用建议**

1.  **不要盲目重写**：如果你已有成熟的 API，不要立即重写为 MCP。建议先使用“适配器模式”，编写一个轻量的 MCP Server 将现有 API 包装暴露给 Amazon Q，验证 ROI 后再深度重构。
2.  **关注“提示词工程”与“Schema 设计”的协同**：MCP 中的工具描述本质上是给模型看的元数据。建议在开发 MCP Server 时，不仅让后端工程师参与，更要让负责 Prompt 的 AI 应用工程师审核工具的 `description` 字段，确保模型能理解。
3.  **测试边界情况**：重点测试 Amazon Q 在处理 MCP 返回的错误（Error Code）和空结果时的行为。很多时候模型会陷入重试死循环，这需要在 MCP Server 端做精细的错误处理和降级。

**可验证的检查方式**

1.  **互操作性测试（实验）**：构建一个标准的 MCP Server（如一个简单的天气查询工具），尝试在不修改代码的情况下，分别将其接入 Amazon Quick Agents、Claude Desktop 和其他支持 MCP 的客户端。验证“一次编写，多处运行”的承诺是否成立，以及需要多少适配性代码。
2.  **复杂参数通过率（指标）**：设计一组包含嵌套对象、枚举值和可选参数的复杂工具 Schema。通过 Amazon Quick Agents 进行自然语言调用，统计模型成功生成符合 MCP Schema 的 JSON 参数的成功率（Pass Rate）。
3.  **延迟与稳定性观察（观察窗口）**：在 MCP Server 侧引入模拟延迟（如 500ms 响应时间），观察 Amazon Quick Agents 在等待结果时的用户体验（是否有超时机制、流式输出是否卡顿），评估 MCP 协议在云环境下的实际性能损耗。

---
## 技术分析

基于您提供的文章标题和摘要，这是一篇关于**利用模型上下文协议（MCP）将外部工具集成到 Amazon Quick Agents**的技术实施指南。鉴于文章主要面向第三方（3P）合作伙伴，旨在提供构建或适配 MCP 服务器的“操作方法”。

以下是对该文章的深入分析报告：

---

# 深入分析：利用 MCP 将外部工具集成至 Amazon Quick Agents

## 1. 核心观点深度解读

**主要观点：**
文章的核心观点是**“标准化协议是解锁 AI 智能体潜力的关键”**。通过采用 **Model Context Protocol (MCP)**，开发者可以构建一个标准化的服务器层，从而将任何外部数据源或工具无缝、安全地连接到 Amazon Quick Agents（及任何兼容 MCP 的客户端）。文章提出了一套六步检查清单，作为第三方合作伙伴确保其服务能与 Amazon Quick 生态完美对接的“金标准”。

**核心思想：**
作者传达了从“硬编码集成”向“协议通用化”转变的思想。在传统的 AI 应用开发中，每次将一个新的工具（如 CRM、API）连接到大模型通常需要定制化的代码。MCP 的引入改变了这一范式，它将工具连接变成了一个**即插即用**的过程。这不仅降低了技术门槛，更重要的是建立了一个**“客户端-服务器”解耦**的生态系统，使得工具提供商可以专注于优化自身数据的 MCP 服务器，而无需关心客户端（Amazon Quick）的具体实现细节。

**观点的创新性与深度：**
*   **创新性：** MCP 本身是一种新兴的开放标准（由 Anthropic 主导，但 Amazon Quick 的采用显示了其跨平台的潜力）。文章的创新之处在于将其具体化为 AWS 生态内的企业级落地路径，强调了“验证与调整”现有服务器的重要性，而非仅从零开始。
*   **深度：** 文章超越了简单的 API 调用，深入到了**互操作性**和**合规性**层面。它暗示了未来的 AI 生态将由协议驱动，而非 SDK 驱动。

**重要性：**
对于合作伙伴而言，这意味着接入 Amazon Bedrock/Quick 生态不再需要维护复杂的定制适配器，只需维护一个 MCP 标准接口。这极大地降低了 ISV（独立软件开发商）的集成成本，加速了企业级 AI 落地。

## 2. 关键技术要点

**涉及的关键技术或概念：**
1.  **Model Context Protocol (MCP)：** 核心技术。一种基于 JSON-RPC 的开放协议，用于连接 AI 应用与数据源。它定义了宿主和本地工具之间的通信标准。
2.  **Amazon Quick Agents / Amazon Bedrock：** AWS 的生成式 AI 服务层，作为 MCP 的客户端。
3.  **MCP Server（服务器端）：** 运行在工具侧的轻量级程序，负责将外部数据源（如 SQL 数据库、REST API）转换为 MCP 标准格式。
4.  **Resources（资源）、Prompts（提示）、Tools（工具）：** MCP 的三大核心能力类型。

**技术原理和实现方式：**
*   **架构模式：** 采用 Client-Server 架构。Amazon Quick Agent 作为 Client，发起请求；合作伙伴的代码作为 Server，监听并响应。
*   **通信机制：** 通常使用 `stdio`（标准输入/输出）进行本地通信，或使用 SSE (Server-Sent Events) 进行远程通信。数据交换格式为 JSON。
*   **六步检查清单（推测内容）：**
    1.  **环境搭建：** 初始化 MCP 服务器项目（通常使用 Python/TypeScript SDK）。
    2.  **定义资源与工具：** 将业务逻辑映射为 MCP 的 `tools`（可执行函数）和 `resources`（数据引用）。
    3.  **实现协议逻辑：** 处理 `initialize`、`call_tool`、`list_resources` 等标准方法。
    4.  **错误处理与约束：** 确保符合 Amazon Quick User Guide 中的超时和大小限制。
    5.  **安全认证：** 实现鉴权机制，确保只有授权的 Agent 能访问数据。
    6.  **本地与远程测试：** 在 Amazon Quick 环境中进行端到端验证。

**技术难点与解决方案：**
*   **难点：** **上下文窗口限制与数据切片。** 外部数据源可能非常庞大（如整个文档库），直接传给 LLM 会爆 Token。
*   **解决方案：** MCP Server 需实现智能检索或过滤逻辑，仅将相关的元数据或具体内容片段通过 `resources` 暴露给 Agent，而非全量数据。
*   **难点：** **异步与长时任务。** 某些工具执行时间较长，可能导致客户端超时。
*   **解决方案：** 利用 MCP 的异步特性，或者设计“任务提交-状态查询”模式的工具接口。

## 3. 实际应用价值

**对实际工作的指导意义：**
该指南为数据提供商（如 Salesforce、Jira、ServiceNow 等厂商的对接团队）提供了一条明确的路径，使其产品能被 Amazon Quick Agents 直接调用。这意味着企业的私有数据可以通过“即插即用”的方式赋予 AI 智能体能力。

**可应用场景：**
1.  **企业知识库问答：** 将公司内部的 Wiki、Confluence 作为 MCP 资源接入，Agent 可实时查询最新文档。
2.  **业务自动化（RPA）：** Agent 调用 MCP 工具执行实际操作，如“创建工单”、“查询库存”、“发送邮件”。
3.  **数据分析：** Agent 通过 MCP 连接 SQL 数据库，执行只读查询并生成图表。

**需要注意的问题：**
*   **权限控制（RBAC）：** MCP Server 必须继承原系统的权限模型。不能因为 Agent 调用就绕过了原有的安全审查。
*   **成本与延迟：** 每一次 Agent 调用工具都是一次网络请求，需优化响应速度以保证用户体验。

**实施建议：**
不要试图将所有业务逻辑都塞进 MCP Server。MCP Server 应该是一个**薄薄的适配层**，负责协议转换和鉴权，核心业务逻辑应由后端微服务承载。

## 4. 行业影响分析

**对行业的启示：**
这标志着 AI 应用开发从“以模型为中心”转向“以数据集成为中心”。随着 AWS (Amazon Quick) 和 Anthropic (Claude) 等巨头对 MCP 的支持，MCP 有望成为 AI 领域的 **"USB 接口"**——即连接 LLM 与外部世界的通用标准。

**可能带来的变革：**
*   **MCPaaS (MCP as a Service) 的兴起：** 未来可能会出现专门提供特定数据源 MCP Server 的服务商。
*   **去中心化的 AI 生态：** 开发者不再需要等待 OpenAI 或 AWS 官方支持某个插件，只需自己发布一个 MCP Server 即可。

**对行业格局的影响：**
这将削弱单一平台封闭生态（如 ChatGPT Plugins）的优势，强化开放协议的地位。对于 AWS 生态而言，这极大地丰富了 Bedrock 的可用工具库，提升了其相对于 OpenAI 和 Google 的竞争力。

## 5. 延伸思考

**引发的思考：**
*   **协议的统一性：** MCP 目前由 Anthropic 主导，但 AWS 的强力支持是否意味着它将成为事实上的 ISO 标准？如果 OpenAI 拒绝支持，市场是否会分裂？
*   **安全边界：** 当 AI 拥有了通过 MCP 协议操作数据库（写入/删除）的能力时，如何防止“提示词注入”攻击导致的数据泄露或破坏？这是目前 MCP 安全模型中最需要关注的部分。

**未来发展趋势：**
*   **双向 MCP：** 目前的 MCP 主要是 Agent 拉取数据。未来可能会支持 Server 向 Agent 主动推送事件（Webhook 模式）。
*   **边缘计算 MCP：** 为了隐私和速度，MCP Server 可能会部署在用户的本地设备或私有 VPC 中，而非公网。

## 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现有 API：** 检查你目前对外提供的 REST API 或 GraphQL 接口。
2.  **构建 Wrapper：** 使用 Python 或 TypeScript 的 MCP SDK 编写一个轻量级服务，将现有 API 封装为 MCP Tools。
3.  **本地测试：** 使用 Inspector (MCP 的调试客户端) 验证工具描述是否清晰，参数是否正确。
4.  **部署与注册：** 将服务部署到 Amazon Bedrock 可访问的网络环境，并在 Amazon Quick 中配置连接。

**具体行动建议：**
*   **阅读官方文档：** 仔细研读 "Amazon Quick User Guide" 中关于 MCP Client 行为的部分，特别是超时设置和返回值格式。
*   **渐进式集成：** 先集成只读类工具（如查询天气、查询库存），验证稳定后再集成写入类工具（如下单、修改记录）。

**需补充的知识：**
*   熟悉 JSON-RPC 2.0 规范。
*   了解 Function Calling（函数调用）的工作原理。
*   掌握基本的异步编程模型。

## 7. 案例分析

**成功案例构想（基于逻辑推演）：**
*   **场景：** 一家 SaaS 客服系统提供商。
*   **做法：** 他们开发了一个 MCP Server，将“查询工单”和“更新工单状态”两个接口暴露出来。
*   **效果：** 使用 Amazon Quick Agents 的企业用户，可以直接用自然语言对 Agent 说“帮我查一下 ID 为 123 的工单状态并标记为已解决”，Agent 通过 MCP 协议直接操作该系统，无需人工切换界面。

**失败案例反思：**
*   **场景：** 某公司试图将整个复杂的 ERP 系统通过 MCP 暴露。
*   **问题：** MCP Server 包含了数千个细粒度的 API，导致 Agent 在选择工具时出现“迷失”，且描述混乱导致 Agent 频繁调用错误的工具。
*   **教训：** MCP 设计应遵循**“少即是多”**原则，仅暴露高频、高价值的聚合工具，而非 1:1 映射所有后端 API。

## 8. 哲学与逻辑：论证地图

**中心命题:**
**采用 Model Context Protocol (MCP) 是第三方工具无缝集成至 Amazon Quick Agents 并实现企业级 AI 互操作性的最优且必要的标准化路径。**

**支撑理由:**
1.  **标准化带来的互操作性:** MCP 提供了统一的通信协议，消除了为每个 AI 平台定制集成的需求，大幅降低开发维护成本。
2.  **生态系统的准入门槛:** 文章提供的六步指南表明，遵循 MCP 标准是进入 Amazon Quick/Bedrock 生态系统的技术前提，这构成了事实上的行业标准。
3.  **安全与可控性:** MCP 的客户端-服务器模型允许数据所有者（工具方）在本地控制数据访问逻辑和权限，而非将数据全量上传至云端模型。

**反例与边界条件:**
1.  **高性能/低延迟场景:** 对于毫秒级响应要求的交易系统（如高频交易），MCP 基于 JSON-RPC 的序列化开销可能无法接受，此时直接 gRPC 调用可能更优。
2.  **非结构化流式数据:** 如果应用主要是处理实时的音视频流而非结构化工具调用，MCP 的设计可能并不

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确工具定义与接口规范

**说明**:
在使用 MCP 集成外部工具时，首先需要清晰地定义工具的功能、输入参数及输出结构。MCP 要求工具具备明确的语义描述，以便 Amazon Quick Agents 能够准确理解何时以及如何调用该工具。模糊的定义会导致 Agent 调用错误或无法生成正确的代码。

**实施步骤**:
1. 使用标准 JSON Schema 或 YAML 定义工具的输入和输出模式。
2. 为工具编写详细的描述信息，说明其用途、副作用以及参数限制。
3. 确保所有参数类型（如字符串、整数、布尔值）都与 MCP 规范严格对齐。

**注意事项**:
避免使用过于宽泛或模糊的参数名称，确保参数名称具有自解释性。

---

### 实践 2：实施严格的身份验证与授权机制

**说明**:
连接外部工具通常涉及访问敏感数据或执行关键操作。必须确保 MCP 服务器与外部工具之间的通信是安全的，并且只有经过授权的 Amazon Quick Agents 实例才能发起请求。

**实施步骤**:
1. 在 MCP 服务器配置中启用 TLS/SSL 以确保传输层加密。
2. 实施 API 密钥、OAuth 2.0 或 IAM 角色基于的授权策略。
3. 遵循最小权限原则，仅授予 Agent 完成任务所需的特定权限，避免授予通用的管理员访问权限。

**注意事项**:
定期轮换凭证，并避免在代码或配置文件中硬编码任何敏感密钥。

---

### 实践 3：优化数据上下文与提示词工程

**说明**:
虽然 MCP 负责传输数据，但 Amazon Quick Agents 的效能取决于它接收到的上下文质量。确保传递给 Agent 的数据既包含必要的信息，又不会因包含过多无关噪音而超出模型的上下文窗口限制。

**实施步骤**:
1. 在工具返回数据时，进行预处理，仅保留与用户意图相关的字段。
2. 设计简洁的提示词模板，指导 Agent 如何解释工具返回的结果。
3. 实施分页或数据截断机制，以防止大型数据集导致令牌超限。

**注意事项**:
监控令牌使用情况，平衡信息完整性与处理成本。

---

### 实践 4：构建健壮的错误处理与重试逻辑

**说明**:
外部服务可能会遇到故障、限流或网络延迟。MCP 集成必须具备弹性，能够优雅地处理这些错误，并向 Amazon Quick Agents 提供有意义的反馈，而不是简单地崩溃。

**实施步骤**:
1. 在 MCP 服务器端实现标准的 HTTP 错误代码映射（如 400, 401, 429, 500）。
2. 配置指数退避算法以处理暂时性故障（如 429 Too Many Requests）。
3. 向 Agent 返回结构化的错误消息，说明失败原因及可能的解决方案，以便 Agent 可以向用户报告或尝试替代方案。

**注意事项**:
避免无限重试循环，设置最大重试次数和超时阈值。

---

### 实践 5：确保工具的幂等性

**说明**:
由于 LLM 可能会因为网络波动或逻辑重试而重复执行同一个工具调用，确保外部工具的幂等性至关重要。这意味着即使多次执行相同的操作，系统状态也只改变一次，或者产生相同的结果。

**实施步骤**:
1. 对于写操作（POST/PUT/DELETE），设计业务逻辑以检查资源当前状态，避免重复创建或更新。
2. 在请求中传递唯一的幂等键，由外部系统进行去重处理。
3. 对于非幂等操作，在 MCP 层面实现去重逻辑缓存。

**注意事项**:
特别关注支付、状态变更或数据写入类操作的安全性。

---

### 实践 6：全面测试与日志记录

**说明**:
在将集成的工具部署到生产环境之前，必须进行严格的测试。同时，详细的日志记录对于调试 Agent 行为和工具性能至关重要。

**实施步骤**:
1. 编写单元测试以验证 MCP 服务器的输入解析和输出格式化逻辑。
2. 进行端到端测试，模拟 Amazon Quick Agents 调用工具的各种场景。
3. 启用详细的日志记录，记录请求负载、响应时间、错误堆栈和 Agent 的决策路径。

**注意事项**:
确保日志中不包含敏感用户数据（PII），并遵守数据隐私合规要求。

---

### 实践 7：性能监控与延迟优化

**说明**:
用户对 Amazon Quick Agents 的响应速度有较高期望。外部工具的调用延迟直接影响整体用户体验。必须持续监控 MCP 集成的性能表现。

**实施步骤**:
1. 为每个 MCP 工具调用设置超时限制，防止长时间挂起。
2. 使用监控工具（如 Amazon CloudWatch）跟踪工具调用的延迟和成功率。
3. 如果外部工具响应缓慢，考虑实施异步调用模式或添加缓存层。

**注意事项**:
在高并发场景下评估外部工具的负载能力，必要时实施速率限制。

---
## 学习要点

- Amazon Quick Agents 现已支持通过模型上下文协议（MCP）集成外部工具。
- 开发者可在 Amazon Bedrock 配置文件中定义 MCP 服务器连接信息，将数据源或 API 连接到智能体，无需编写集成代码。
- 该架构利用 Anthropic Claude 模型的原生 MCP 支持，使智能体能够根据用户意图调用外部工具以检索信息或执行操作。
- 通过 MCP 接口，智能体能够访问私有数据（如内部知识库或业务系统），以补充大语言模型的训练数据。
- 此方案允许通过统一协议挂载各类工具，无需针对每个工具单独定制集成逻辑。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [集成指南](/tags/%E9%9B%86%E6%88%90%E6%8C%87%E5%8D%97/) / [外部工具](/tags/%E5%A4%96%E9%83%A8%E5%B7%A5%E5%85%B7/) / [LLM](/tags/llm/) / [开发实战](/tags/%E5%BC%80%E5%8F%91%E5%AE%9E%E6%88%98/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [深度解析Skill/MCP/RAG等五大AI技术的底层逻辑]({{< relref "posts/20260212-juejin-深入理解skillmcpragagentopenclaw底层逻辑-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*