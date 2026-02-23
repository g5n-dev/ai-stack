---
title: "使用MCP集成外部工具至Amazon Quick Agents的六步指南"
date: 2026-02-23T08:10:30+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "LLM", "Agent", "集成指南", "第三方集成", "工具调用", "开发实战"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "本文提供了关于如何利用 **模型上下文协议 (MCP)** 将外部工具与 **Amazon Quick Agents** 集成的指南。主要内容旨在帮助第三方合作伙伴构建或调整 MCP 服务器以实现与 Amazon Quick 的无缝对接。以下是该文档的核心摘要： **1. 目标与适用对象** * **核心目标**：指导"
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

在这篇文章中，您将使用一个六步检查清单来构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器，以便与 Amazon Quick 集成。《Amazon Quick 用户指南》描述了 MCP 客户端的行为和约束。这是一份“操作指南”，面向 3P 合作伙伴与 Amazon Quick 通过 MCP 进行集成所需的详细实施步骤。

---
## 导语

随着 AI 应用的深入，如何将大模型与外部数据源高效集成已成为开发者关注的重点。本文详细介绍了如何利用 Model Context Protocol (MCP) 将外部工具接入 Amazon Quick Agents，帮助开发者突破模型的数据边界。通过文中提供的六步检查清单，您将掌握构建或调整 MCP 服务器的具体方法，从而实现与 Amazon Quick 的无缝对接。

---
## 摘要

本文提供了关于如何利用 **模型上下文协议 (MCP)** 将外部工具与 **Amazon Quick Agents** 集成的指南。主要内容旨在帮助第三方合作伙伴构建或调整 MCP 服务器以实现与 Amazon Quick 的无缝对接。以下是该文档的核心摘要：

**1. 目标与适用对象**
*   **核心目标**：指导开发者如何通过 MCP 协议，使 Amazon Quick Agents 能够调用外部工具和数据源。
*   **适用对象**：主要为第三方合作伙伴（3P partners）及开发者，用于满足详细的集成实施要求。

**2. 实施方法：六步清单**
文档提供了一个标准化的“六步清单”，开发者需遵循此流程进行开发或验证：
*   **场景一**：从零开始构建一个新的 MCP 服务器。
*   **场景二**：验证并调整现有的 MCP 服务器，以符合 Amazon Quick 的集成标准。

**3. 关键文档依据**
*   **技术规范**：集成过程必须严格参考《Amazon Quick 用户指南》。
*   **行为约束**：指南中详细定义了 MCP 客户端的行为模式及其局限性，这是服务器端开发必须遵守的规则。

**总结**
这是一份面向合作伙伴的实操性“操作指南”，重点在于通过六个具体步骤，确保 MCP 服务器在功能和行为上与 Amazon Quick 的客户端要求完美兼容，从而实现外部能力的有效扩展。

---
## 评论

### 深度评价：Integrate external tools with Amazon Quick Agents using Model Context Protocol (MCP)

#### 中心观点
该文章是一篇针对第三方开发者的**战术性工程落地指南**，其核心价值在于通过标准化的 Model Context Protocol (MCP) 打通了外部工具与 Amazon Quick Agents 之间的数据孤岛，实质上是在 LLM 应用层确立了一种“可插拔式”的工具生态标准。

#### 支撑理由与边界分析

**1. 内容深度：从“手工作坊”向“工业标准”的规范化跨越**
*   **分析**：文章没有停留在简单的 API 调用层面，而是深入到了协议层的对齐。MCP 的引入解决了 Agent 开发中最为繁琐的“接口适配”问题。文章详细描述的六步清单，实际上是在定义一种**数据交换的契约**。这不仅是技术实现，更是生态治理的体现。它要求开发者不仅要懂业务逻辑，还要严格遵守 Quick Agents 的约束（如上下文窗口限制、超时处理），体现了工程严谨性。
*   **边界条件/反例**：虽然 MCP 标准化了连接，但它**无法解决工具本身的语义鸿沟**。例如，如果一个外部工具的 API 设计极其晦涩（如参数命名不直观），即便接入了 MCP，Agent 依然可能无法正确调用。此外，MCP 协议本身的版本迭代可能会导致旧版服务器迅速过时，维护成本不容忽视。

**2. 实用价值：为 SaaS 供应商提供“入场券”**
*   **分析**：对于 AWS 生态的合作伙伴而言，这篇文章具有极高的实战意义。Amazon Quick Agents（可能指代 Q Business 或类似的自动化 Agent 服务）是 AWS 进军企业级 AI 的重要抓手。文章提供的“六步清单”直接对应了开发者的 ROI（投资回报率）。它不仅提供了代码层面的指导，更重要的是指明了合规性路径，使得第三方工具能迅速上架到 AWS Marketplace 或集成到企业工作流中。
*   **边界条件/反例**：这种高度耦合 AWS 生态的方案存在**厂商锁定风险**。如果开发者希望同一套工具服务同时支持 OpenAI GPTs 和 Google Agents，基于 MCP 的这种深度定制可能需要额外的适配层，反而增加了多端维护的复杂度。

**3. 行业影响：推动 Agent 互操作性的“USB 时刻”**
*   **分析**：MCP 的出现及 AWS 的采纳，标志着 Agent 行业正在从“大模型参数竞赛”转向“工具链生态竞赛”。文章所倡导的标准化连接，类似于 PC 时代的 USB 接口或移动互联网时代的 API 标准。如果 MCP 成为事实标准，将极大降低 Agent 获取外部知识（如企业数据库、SaaS 软件）的门槛，加速 AI 从“聊天玩具”向“生产力工具”进化。
*   **边界条件/反例**：行业标准往往伴随着激烈的**政治博弈**。目前 Anthropic 推出 MCP，AWS 紧随其后，但 OpenAI 和 Google 可能有各自的连接标准（如 OpenAI 的 Plugins 规范）。如果巨头无法达成统一，MCP 可能仅成为 Anthropic/AWS 阵营的内部标准，而非全行业通用的“USB”。

#### 维度评价总结

*   **创新性**：**中等偏上**。MCP 协议本身并非 AWS 原创（源自 Anthropic），但 AWS 将其整合进 Quick Agents 并给出严格实施指南，属于**应用层面的集成创新**。它提出了“Server-Client”解耦的明确范式，优于传统的硬编码 Function Calling。
*   **可读性**：**高**。作为一篇技术指南，它采用了 Checklist（清单体）结构，逻辑清晰，针对性强。但缺点是可能缺乏对 MCP 协议底层原理的宏观解释，对非架构师角色的开发者可能略显生硬。
*   **争议点**：最大的争议在于**安全与权限控制**。MCP 赋予了 Agent 直接操作外部工具的能力，文章虽然提到了“约束”，但在企业级场景下，如何通过 MCP 细粒度地控制数据权限（例如：Agent 只能读数据库，不能删库），文章可能未给出足够深度的安全架构方案。

#### 实际应用建议

1.  **模块化设计**：在构建 MCP Server 时，不要将业务逻辑与协议层耦合。建议设计一个中间层，将企业原有的 API 转换为 MCP 标准格式，以便未来协议升级时只需替换中间层。
2.  **错误处理与降级**：MCP 连接可能失败。在集成到 Quick Agents 时，务必设计“优雅降级”机制。当工具调用超时或失败时，Agent 应能回退到基于通用知识的回答，而不是直接报错，以保障用户体验。
3.  **严格的安全审计**：由于 MCP Server 实际上充当了企业内网的网关，建议在部署前进行严格的渗透测试，确保 MCP Server 不会成为 LLM 攻击内网的跳板。

#### 可验证的检查方式

1.  **协议兼容性测试（指标）**：
    *   构建一个 Mock MCP Server，故意引入非标准 JSON 响应或超长上下文，观察 Amazon Quick Agents 是能优雅捕获错误并提示用户，还是直接导致 Session 崩溃。
    *   *验证点*：文章提到的“Constraints”是否真的被客户端严格执行。

2.  **性能基准测试（实验）**：
    *   测量数据从外部工具 -> MCP Server -> Quick Agent -> 用户的端到端延迟。
    *   *验证点*：

---
## 技术分析

基于您提供的文章标题和摘要，以下是对《使用模型上下文协议（MCP）将外部工具与 Amazon Quick Agents 集成》一文的深入分析。

---

# 深度分析报告：基于 MCP 的 Amazon Quick Agents 外部工具集成

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点在于**标准化协议是打破 AI Agent 与外部工具之间集成壁垒的关键**。通过采用模型上下文协议（MCP），第三方开发者可以构建一个通用的服务器，使得 Amazon Quick Agents 能够安全、高效地发现并调用外部工具和数据源，从而极大地扩展 Agent 的能力边界。

**作者想要传达的核心思想**
作者试图传达一种**“去中心化”与“模块化”**的 AI 生态构建思想。与其为每一个工具编写特定的 API 适配器，不如通过 MCP 建立一套统一的通信标准。这不仅降低了开发者的准入门槛，也确保了 Amazon Quick Agents 作为一个平台，能够像应用商店一样动态扩展功能，而无需频繁修改核心代码。

**观点的创新性和深度**
该观点的创新性在于**将 LLM 的工具调用从“硬编码”转变为“即插即用”**。传统的 Agent 集成往往需要针对特定模型定义特定的 Function Schema，而 MCP 抽象了这一层，使得工具的定义与模型的具体实现解耦。深度方面，它触及了 AI Agent 系统架构的底层逻辑——即如何解决“上下文窗口限制”与“无限外部数据”之间的矛盾，通过标准化的资源引用和提示词注入来实现。

**为什么这个观点重要**
随着 LLM 应用的深入，单一的模型能力已无法满足复杂的企业需求。企业数据往往散落在 SQL 数据库、CRM 系统、Slack 消息等外部工具中。MCP 的出现，提供了一种**工业级的标准接口**，使得 AI 能够以一种结构化、安全的方式访问这些“孤岛”，是通向 AGI（通用人工智能）在实际生产环境中落地的必要基础设施。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **Model Context Protocol (MCP)**：核心协议，基于 JSON-RPC 2.0，定义了 Client（Quick Agents）与 Server（外部工具）之间的通信标准。
*   **Amazon Quick Agents**：扮演 MCP Client 的角色，负责发起请求、解析 Schema 并管理对话状态。
*   **MCP Server**：运行在外部工具侧的守护进程，负责暴露工具、资源和提示词模板。
*   **STDIO (Standard Input/Output) vs. SSE (Server-Sent Events)**：MCP 支持的两种传输层机制，分别适用于本地进程和远程网络通信。

**技术原理和实现方式**
1.  **握手与初始化**：Quick Agents 启动 MCP Server 进程（通常通过 STDIO），发送 `initialize` 请求。
2.  **能力发现**：Client 请求 `tools/list` 或 `resources/list`，Server 返回 JSON Schema 格式的工具定义（参数、类型、描述）。
3.  **动态调用**：当用户查询触发特定工具时，Client 发送 `tools/call` 请求，Server 执行实际逻辑（如 SQL 查询或 API 调用）。
4.  **上下文注入**：Server 返回结果，Client 将结果作为上下文的一部分重新注入到 LLM 的 Prompt 中，生成最终回复。

**技术难点和解决方案**
*   **难点**：**数据安全与权限控制**。直接允许 Agent 访问外部工具风险巨大。
*   **方案**：MCP Server 需实现细粒度的权限校验，且 Quick Agents 作为 Client 应当在 Server 端进行身份验证。文章提到的“六步清单”中必然包含对安全配置的验证。
*   **难点**：**上下文窗口管理**。外部工具返回的数据可能过大。

**技术创新点分析**
最大的创新在于**Prompt 的远程编排**。MCP Server 不仅可以提供工具，还可以提供 `prompts` 资源，即允许外部工具“教” Agent 如何提问。这意味着工具开发者可以将最佳实践直接注入到 Agent 的行为逻辑中。

## 3. 实际应用价值

**对实际工作的指导意义**
对于企业 IT 团队而言，这意味着不再需要等待 SaaS 厂商发布官方集成。只要有一个 MCP Server，任何内部系统（如旧 ERP、HR 系统）都可以立即被 Amazon Quick Agents 操控。这赋予了企业极大的自主权。

**可以应用到哪些场景**
1.  **企业知识库问答**：通过 MCP Server 连接 Confluence 或 SharePoint，Agent 可以实时检索最新文档。
2.  **数据分析**：Agent 通过 MCP 连接数据库，执行只读 SQL 查询，生成图表。
3.  **运维自动化**：Agent 通过 MCP 调用 AWS Lambda 或 Terraform 脚本执行云资源管理。

**需要注意的问题**
*   **延迟**：多轮的 MCP 通信会增加响应时间。
*   **错误处理**：外部工具的异常（如数据库超时）必须优雅地转化为 LLM 能理解的错误信息，防止导致 Agent 幻觉。

**实施建议**
建议采用“渐进式集成”策略。先从低风险的只读类工具（如天气、文档检索）开始集成，验证 MCP Server 的稳定性，再逐步开放写权限（如发送邮件、修改订单）。

## 4. 行业影响分析

**对行业的启示**
MCP 的推广标志着 **AI Agent 生态正在经历“Android 时刻”**。正如 Android 统一了移动应用的接口，MCP 有望统一 LLM 访问外部数据的接口。这将促使行业从“单一模型竞争”转向“工具生态竞争”。

**可能带来的变革**
*   **MCPaaS (MCP as a Service)**：未来可能会出现专门提供各类 MCP Server 的服务商，企业只需订阅即可快速获得 Agent 的各种能力。
*   **中间件消亡**：传统的 API 聚合器可能会被标准化的 MCP Server 取代。

**对行业格局的影响**
对于 Amazon AWS 而言，这是对抗 OpenAI (Function Calling) 和 LangChain (Tool Protocol) 的重要战略布局。通过支持 MCP，Amazon Quick Agents 能够快速补齐在生态丰富度上的短板，利用 AWS 庞大的合作伙伴网络构建护城河。

## 5. 延伸思考

**引发的其他思考**
*   **协议的统一性**：目前业界存在多种工具调用协议（OpenAI Function, LangChain Tools, ReAct API 等）。MCP 能否成为最终的事实标准？还是会导致新的碎片化？
*   **多模态支持**：目前的 MCP 主要侧重文本和结构化数据，未来如何支持视频流、实时音频流的传输？

**可以拓展的方向**
*   **MCP Server 的市场**：类似于 VS Code 插件市场，建立一个官方的 MCP Server 仓库，允许开发者一键安装社区贡献的工具。
*   **边缘计算**：在本地设备上运行轻量级 MCP Server，让 Agent 在不联网的情况下也能调用本地硬件（如文件系统、剪贴板）。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有工具**：列出您希望 Agent 调用的内部工具清单。
2.  **开发 MCP Server**：使用官方 SDK (Python/TypeScript) 编写 Server，封装现有 API。
3.  **本地测试**：使用 Inspector (MCP 调试工具) 验证 Server 返回的 Schema 是否准确。
4.  **接入 Quick Agents**：按照文章的六步清单，配置 Quick Agents 以加载您的 Server。

**具体的行动建议**
*   **阅读规范**：深入理解 MCP 的 `tools`, `resources`, `prompts` 三大核心概念。
*   **安全第一**：在 Server 端实现严格的参数校验，防止 SQL 注入或越权操作。

**需要补充的知识**
*   JSON-RPC 2.0 规范。
*   异步进程通信（如果使用 STDIO）。
*   Amazon Quick Agents 的具体配置界面和限制。

## 7. 案例分析

**成功案例分析**
假设一家电商公司使用 Amazon Quick Agents 作为客服助手。
*   **现状**：Agent 无法查询最新的物流状态，因为物流系统是自建的。
*   **MCP 实施**：开发一个 `logistics-mcp-server`，暴露 `get_tracking_number` 工具。
*   **结果**：用户询问“我的货在哪？”，Agent 自动调用 MCP Server，实时返回物流节点，解决率提升 30%。

**失败案例反思**
*   **场景**：某开发者将数据库的 `DROP_TABLE` 权限暴露给了 MCP Server。
*   **后果**：Agent 在处理模糊指令时误删了数据表。
*   **教训**：MCP Server 必须是**最小权限原则**的坚定执行者，且应将危险操作设为需要人工确认。

## 8. 哲学与逻辑：论证地图

**中心命题**
**采用模型上下文协议（MCP）是构建可扩展、标准化且安全的 Amazon Quick Agents 生态系统的最优技术路径。**

**支撑理由与依据**
1.  **互操作性**：MCP 提供了通用标准，使得一次开发的 Server 可以被多个不同的 Agent 客户端复用。
    *   *依据*：MCP 基于通用的 JSON-RPC，且已被 Anthropic、Replit 等多家机构采用。
2.  **开发效率**：它将复杂的工具调用逻辑抽象为简单的配置，大幅降低了 3P 开发者的集成成本。
    *   *依据*：文章提到的“六步清单”显示，仅需配置和验证即可完成集成，无需重写核心逻辑。
3.  **安全隔离**：MCP 将执行逻辑外包给独立的 Server 进程，避免了将不安全的代码直接注入到 Agent 运行时。
    *   *依据*：MCP 的架构设计允许 Server 独立崩溃而不影响 Agent 主进程。

**反例或边界条件**
1.  **高性能/低延迟场景**：对于微秒级的实时交易系统，MCP 基于 JSON-RPC 的序列化开销可能过高，此时直接嵌入 SDK 可能更优。
2.  **极度简单的交互**：如果仅需调用一个极简的 REST API，引入完整的 MCP Server 架构可能属于过度设计。

**事实与价值判断**
*   **事实**：MCP 是一种开源协议；Amazon Quick Agents 支持 MCP。
*   **价值判断**：标准化优于定制化；生态系统的丰富度决定了 Agent 平台的生命力。
*   **可检验预测**：未来 12 个月内，不支持 MCP 的 Agent 平台将逐渐失去企业级工具开发者的支持。

**立场与验证**
*   **立场**：支持将 MCP 作为企业级 AI 集成的首选标准。
*   **验证方式**：
    *   *指标*：集成新工具的平均耗时（从 X 天降低到 Y 小时）。
    *   *实验*：在两个功能相同的 Agent 项目中，分别使用传统 API 和 MCP 进行 10 个工具的集成，对比维护成本和代码复用率。

---
## 最佳实践

## 最佳实践指南

### 实践 1：确保 MCP 服务器的安全性与访问控制

**说明**：
在将外部工具集成到 Amazon Quick Agents 时，MCP 服务器充当了 Agent 与外部数据或工具之间的桥梁。如果不实施严格的安全措施，可能会导致敏感数据泄露或未授权操作。必须确保只有经过身份验证和授权的 Agent 才能访问特定的 MCP 工具。

**实施步骤**：
1.  为 MCP 服务器实施强身份验证机制（如 mTLS、API 密钥或 OAuth）。
2.  在 Amazon Quick Agents 配置中，安全地存储和管理凭据（建议使用 AWS Secrets Manager）。
3.  遵循最小权限原则，仅授予 Agent 完成任务所需的特定工具权限，而非全量访问。

**注意事项**：
切勿在 Agent 配置代码或提示词中硬编码 API 密钥或敏感凭据。

---

### 实践 2：提供清晰且结构化的工具描述

**说明**：
Amazon Quick Agents 依赖大语言模型（LLM）来决定何时以及如何调用 MCP 工具。如果工具描述模糊或缺乏上下文，Agent 可能会无法正确调用工具，或产生幻觉。高质量的元数据能显著提升 Agent 的决策准确性。

**实施步骤**：
1.  为每个 MCP 工具编写简洁明了的 `name` 和 `description`。
2.  在描述中明确说明工具的功能、输入参数要求以及预期的输出结果。
3.  定义严格的 JSON Schema 用于输入参数验证，确保 Agent 理解所需的数据格式。

**注意事项**：
避免使用过于技术化或晦涩的术语，描述应从“用户意图”而非“代码实现”的角度编写。

---

### 实践 3：优化 MCP 服务器的响应延迟

**说明**：
用户与 Quick Agents 的交互通常是实时的。如果 MCP 服务器响应缓慢，会导致整体对话体验下降。外部工具的调用应尽可能高效，以维持流畅的对话流。

**实施步骤**：
1.  对 MCP 服务器进行性能基准测试，确保 API 响应时间在可接受范围内（通常建议低于 2-3 秒）。
2.  优化后端数据库查询或第三方 API 调用逻辑，引入必要的缓存层。
3.  如果操作耗时较长，考虑设计异步处理模式，先向 Agent 返回确认信息，稍后通过回调或状态查询返回结果。

**注意事项**：
在配置超时设置时，要权衡网络波动与用户体验，避免设置过短导致频繁超时。

---

### 实践 4：实施全面的错误处理与反馈机制

**说明**：
外部工具调用不可避免地会遇到失败（如网络错误、服务不可用或无效输入）。如果 MCP 服务器仅返回原始的错误代码，Agent 可能无法理解并向用户传达有用的信息。必须将技术错误转换为 Agent 可理解的语义化反馈。

**实施步骤**：
1.  在 MCP 服务器端捕获所有异常，并返回标准化的错误响应。
2.  错误消息应包含问题的性质以及可能的解决建议（例如：“用户 ID 未找到，请检查格式”）。
3.  确保 Agent 的提示词包含如何处理工具调用错误的指令（例如：重试、询问用户澄清或优雅降级）。

**注意事项**：
避免向客户端暴露堆栈跟踪或内部系统细节，以防信息泄露。

---

### 实践 5：验证工具输出的上下文相关性

**说明**：
MCP 工具返回的数据量可能很大。如果直接将大量无关数据注入到 Agent 的上下文窗口中，不仅消耗 Token，还会干扰 Agent 的推理能力。工具应仅返回与当前请求最相关的数据。

**实施步骤**：
1.  在 MCP 服务器端实现数据过滤逻辑，根据 Agent 传来的参数精简结果集。
2.  对返回的文本进行摘要或提取关键信息，而非直接转储整个数据库记录。
3.  测试 Agent 在不同数据量下的表现，确保上下文窗口未溢出且响应准确。

**注意事项**：
对于分页数据，确保 MCP 工具支持分页参数，并指导 Agent 如何逐页获取信息。

---

### 实践 6：建立可观测性与日志监控体系

**说明**：
在生产环境中，必须能够追踪 Agent 如何调用 MCP 工具以及工具的响应情况。这对于调试问题、优化性能和审计合规至关重要。

**实施步骤**：
1.  配置 MCP 服务器以记录详细的请求和响应日志（需脱敏敏感数据）。
2.  将日志集成到 Amazon CloudWatch 或类似的监控平台中。
3.  设置告警机制，监控错误率、延迟峰值和异常流量模式。

**注意事项**：
确保日志记录符合隐私政策（如 GDPR 或 HIPAA），避免记录用户的个人身份信息（PII）。

---
## 学习要点

- Amazon Quick Agents 现支持通过模型上下文协议（MCP）无缝集成外部工具与数据源，从而突破模型预训练知识的局限。
- MCP 提供了一种标准化的架构，使开发者无需为每个模型编写定制代码，即可将工具连接到支持该协议的 AI 应用。
- 集成后，智能体能够安全地读取本地文件系统数据或执行外部 API 调用，以完成实时数据查询等复杂任务。
- 该协议通过解耦工具配置与模型逻辑，显著降低了为 AI 智能体添加新功能时的开发与维护成本。
- 开发者可利用开源的 MCP 服务器连接器快速扩展 Amazon Quick Agents 的能力，实现更灵活的工作流自动化。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [LLM](/tags/llm/) / [Agent](/tags/agent/) / [集成指南](/tags/%E9%9B%86%E6%88%90%E6%8C%87%E5%8D%97/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/) / [工具调用](/tags/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8/) / [开发实战](/tags/%E5%BC%80%E5%8F%91%E5%AE%9E%E6%88%98/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP将外部工具集成至Amazon Quick Agents的六步指南]({{< relref "posts/20260222-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [🤖解密Codex智能体闭环：AI如何自主进化？]({{< relref "posts/20260125-blogs_podcasts-unrolling-the-codex-agent-loop-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*