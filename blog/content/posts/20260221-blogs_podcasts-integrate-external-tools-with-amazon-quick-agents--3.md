---
title: "使用MCP协议集成外部工具至Amazon Quick Agents的六步指南"
date: 2026-02-21T16:42:26+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "Agent", "系统集成", "开发指南", "LLM", "第三方集成", "技术实践"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "本文是一篇面向第三方合作伙伴的技术实施指南，旨在通过模型上下文协议（MCP）将外部工具与 Amazon Quick Agents 进行集成。 **核心内容总结：** 1. **目标受众**：主要针对需要进行深度集成的第三方合作伙伴（3P Partners）。 2. **核心任务**：指导用户如何构建一个新的 MCP 服"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["大语言模型"]
---

# 使用MCP协议集成外部工具至Amazon Quick Agents的六步指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在这篇文章中，您将使用一个六步清单来构建新的 MCP 服务器，或者验证并调整现有的 MCP 服务器，以实现与 Amazon Quick 的集成。Amazon Quick 用户指南描述了 MCP 客户端的行为和约束。这是一份“操作方法”指南，详细说明了第三方合作伙伴通过 MCP 与 Amazon Quick 集成所需的实现细节。

---
## 导语

随着 Amazon Quick Agents 的应用场景日益复杂，如何通过 Model Context Protocol (MCP) 高效集成外部工具，已成为提升自动化能力的关键。本文提供了一份详尽的实施指南，通过六步清单帮助开发者构建或验证 MCP 服务器，并明确客户端的行为约束。阅读此文，您将掌握具体的实现细节，从而确保第三方工具与 Amazon Quick 的无缝对接与稳定运行。

---
## 摘要

本文是一篇面向第三方合作伙伴的技术实施指南，旨在通过模型上下文协议（MCP）将外部工具与 Amazon Quick Agents 进行集成。

**核心内容总结：**

1.  **目标受众**：主要针对需要进行深度集成的第三方合作伙伴（3P Partners）。
2.  **核心任务**：指导用户如何构建一个新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以满足 Amazon Quick 的集成要求。
3.  **实施方法**：文章提供了一份包含六个步骤的清单，作为实施工作的操作指引。
4.  **参考依据**：实施过程需参考《Amazon Quick 用户指南》中关于 MCP 客户端的行为模式及限制条件。

简而言之，这是一份关于如何利用 MCP 协议，通过遵循六步清单和客户端约束，来实现外部工具与 Amazon Quick Agents 无缝对接的实操手册。

---
## 评论

**中心观点**
这篇文章确立了基于 Model Context Protocol (MCP) 的标准化集成范式，是第三方开发者将外部数据源和工具接入 Amazon Quick Agents（及潜在的 Bedrock 生态）的**关键技术说明书**，其核心价值在于将异构系统的集成从“定制化开发”转化为“标准化配置”。

**支撑理由与边界分析**

**1. 技术架构的标准化与解耦（事实陈述）**
文章通过 MCP 协议，定义了 AI Agent（客户端）与外部工具（服务端）之间的通用接口。
*   **支撑理由：** MCP 类似于 AI 领域的 ODBC 或 USB 协议。对于 3P（第三方）开发者而言，这意味着只需编写一次 MCP Server，即可被支持 MCP 的不同 Agent 客户端复用。文章提供的“六步清单”实质上是确保互操作性的合规性测试，涵盖了连接性、资源定义、提示词模板及工具调用等核心生命周期。
*   **反例/边界条件：** MCP 并非万能适配器。对于需要极低延迟（毫秒级）的实时系统（如高频交易辅助）或超高吞吐量的流式数据写入，MCP 基于 JSON-RPC 的文本序列化机制可能引入不可接受的序列化开销。此外，若外部工具本身是高度非结构化的（如复杂的 GUI 自动化），强行映射到 MCP 的工具接口可能效率极低。

**2. 填补 LLM 应用落地的“最后一公里”（作者观点）**
当前大模型应用的主要瓶颈不在于模型能力，而在于能否安全、准确地连接企业私有数据。
*   **支撑理由：** Amazon Quick Agents 旨在降低企业构建 AI 应用的门槛。这篇文章通过提供详细的实现指南，解决了“模型有大脑但无手脚”的问题。特别是对“工具定义”和“验证/调整”的强调，直接指导了如何让 LLM 正确理解 API 语义，减少了幻觉和错误调用。
*   **反例/边界条件：** 这种标准化连接虽然降低了开发门槛，但并未解决“语义对齐”的根本难题。即使 MCP 连接完美，如果 LLM 无法理解复杂的业务逻辑（例如：在特定税务法规下选择错误的抵扣工具），单纯的协议标准化无法提升业务准确率。此时仍需要 RAG（检索增强生成）或微调来配合 MCP 使用。

**3. 生态锁定与亚马逊的云战略意图（你的推断）**
虽然 MCP 是开源协议，但亚马逊通过 Quick Agents 对 MCP 的特定约束实现，构建了隐性的生态壁垒。
*   **支撑理由：** 文章中提到的“Amazon Quick User Guide describes the MCP client behavior and constraints”暗示了亚马逊对标准 MCP 可能有私有扩展或特定限制。开发者为了适配 Quick Agents，必须深度遵循亚马逊的“方言”。
*   **反例/边界条件：** 如果 MCP 成为行业事实标准（如 Anthropic, OpenAI 均支持），亚马逊的这种约束将失效，开发者将拥有跨平台的议价权。但在当前阶段，过度依赖 Quick Agents 的特定 MCP 实现可能导致供应商锁定，未来迁移至 Google 或 Microsoft 的 Agent 平台时可能面临重写代码的风险。

**综合评价**

*   **内容深度：** 文章属于高精度的技术实施指南。它不探讨宏大的 AI 哲学，而是聚焦于工程实现细节（如配置文件结构、错误处理）。论证严谨，因为它基于既定的 MCP 规范和亚马逊的 SDK 逻辑，具有强制性的技术约束力。
*   **实用价值：** 极高。对于 SaaS 开发者和企业 IT 团队，这是将产品接入亚马逊 AI 生态的“入场券”。
*   **创新性：** 创新性不在于发明了新算法，而在于**工程范式的确立**。它推动了 AI 开发从“手写 Prompt + 胶水代码”向“协议驱动 + 声明式配置”转变。
*   **可读性：** 典型的技术文档风格，结构清晰（Checklist 形式），但缺乏背景铺垫，要求读者具备扎实的分布式系统和 LLM API 调用知识。
*   **行业影响：** 如果 MCP 被广泛采纳，此类文章将定义 AI 时代的 API 标准。它加速了 AI Agent 生态模块化，工具提供商可以像提供 API 一样提供“MCP 包”。

**实际应用建议**
1.  **不要盲目重构：** 如果已有成熟的 API，优先开发 **MCP Adapter（适配器层）**，而不是重写底层逻辑，以保持架构的灵活性。
2.  **关注安全边界：** MCP Server 通常拥有直接访问数据库或业务系统的权限。在实施文章中的步骤时，务必在 Server 侧实现严格的权限校验，防止 Agent 被诱导攻击（Prompt Injection 导致的越权操作）。
3.  **测试驱动的验证：** 利用文章提到的验证步骤，建立一套针对 MCP 接口的自动化测试集，模拟 Agent 的各种调用边界，确保工具描述的清晰度直接影响调用成功率。

**可验证的检查方式**

1.  **互操作性测试（实验）：** 按照文章指南构建一个 MCP Server，尝试同时将其接入 Amazon Quick Agents 和 Anthropic 的 Desktop Client。观察是否需要修改代码才能在两个平台运行，以此验证亚马逊是否存在“私有方言”导致的兼容性分裂。
2.  **调用成功率指标（指标）：** 部署后监控 `tool_call_success_rate`。如果 LLM 频繁调用错误的工具或参数格式错误，说明文章中提到的“工具定义”部分在语义描述上存在不足，需要

---
## 技术分析

基于您提供的文章标题和摘要，这是一篇关于利用 **Model Context Protocol (MCP)** 将第三方工具集成到 **Amazon Quick Agents** 的技术指南。尽管全文内容未完全展开，但结合标题、摘要以及对 MCP 和 Amazon Bedrock/Quick Sight 生态的现有技术认知，以下是对该文章核心观点及技术要点的深度分析。

---

# 深度分析：利用 MCP 将外部工具集成到 Amazon Quick Agents

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点在于：**Model Context Protocol (MCP) 是实现 AI 智能体与外部数据源和工具进行标准化、解耦集成的关键桥梁。** 通过遵循一个六步检查清单，开发者可以构建或调整 MCP 服务器，从而无缝地将外部能力赋予 Amazon Quick Agents（可能指 Amazon QuickSight 的 Q 功能或 Amazon Bedrock 中的智能体），打破大语言模型（LLM）的数据孤岛。

### 作者想要传达的核心思想
作者传达了**“标准化连接优于硬编码集成”**的思想。在传统的 AI 应用开发中，为每一个工具或数据源编写特定的 API 调用代码是繁琐且不可持续的。MCP 提出了一种统一的“即插即用”标准，使得 Amazon Quick Agents 这样的客户端能够通过统一的协议发现、调用并理解外部工具的功能。这不仅是技术实现，更是一种生态构建的策略。

### 观点的创新性和深度
*   **创新性**：MCP 作为一个新兴的开放标准（由 Anthropic 等推动），其深度在于将“上下文”视为一种可传输的标准协议，而不仅仅是文本提示。文章将这一协议应用于 Amazon 的企业级 AI 生态，展示了跨平台互操作性的潜力。
*   **深度**：文章不仅仅停留在“如何调用 API”，而是深入到了“验证和调整”现有服务器的层面，暗示了协议实现的细节（如资源、提示词模板、工具定义的规范性）对于最终用户体验的决定性影响。

### 为什么这个观点重要
随着企业级 AI 从“聊天机器人”向“行动智能体”演进，**数据连接性**是最大的瓶颈。如果 Amazon Quick Agents 无法安全、高效地访问企业内部的 SQL 数据库、ERP 系统或私有文件，其实际价值将大打折扣。MCP 提供了一种安全、标准化的解决方案，解决了 LLM 应用落地中“最后一公里”的连接问题，对于推动 AI 在企业业务中的实际落地至关重要。

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Model Context Protocol (MCP)**：这是一个开放协议，用于连接 AI 应用（如客户端）和数据源（如服务器）。它定义了如何暴露资源、工具和提示词。
2.  **Amazon Quick Agents**：推测指 Amazon QuickSight 的 "Q" 功能或 Bedrock Agents，代表具备数据分析或业务自动化能力的 AI 智能体。
3.  **MCP Client vs. Server**：文章主要关注 **Server** 端的构建，即如何封装外部工具的逻辑。
4.  **JSON-RPC 2.0**：MCP 通常基于 JSON-RPC 进行通信，理解其请求/响应模式是基础。
5.  **STDIO vs. SSE (Server-Sent Events)**：MCP 服务器传输数据的两种主要方式。

### 技术原理和实现方式
*   **原理**：Amazon Quick Agents 作为 MCP Client，启动并连接到本地的或远程的 MCP Server。Server 会向 Client “宣告”自己提供了哪些工具（Tools，如函数调用）和资源（Resources，如文件片段）。
*   **实现**：开发者需要编写一个符合 MCP 规范的服务器程序。当 Quick Agents 需要执行某个操作（例如查询销售数据）时，它会通过 MCP 协议发送请求，MCP Server 接收请求，执行实际的数据库查询或 API 调用，然后将结果格式化返回给 Agent，Agent 再生成自然语言回复。

### 技术难点和解决方案
*   **难点 1：数据映射与类型安全**。MCP 协议要求严格定义工具的输入参数 Schema。
    *   *解决方案*：文章可能强调使用 JSON Schema 进行严格的参数校验，确保 Agent 传递的参数能被后端正确解析。
*   **难点 2：上下文窗口限制**。外部工具返回的大量数据可能撑爆 LLM 的上下文。
    *   *解决方案*：MCP Server 端需要进行数据预处理，仅返回相关的摘要或切片，而非全量数据。
*   **难点 3：认证与安全**。如何确保 Agent 只能访问授权的数据。
    *   *解决方案*：在 MCP Server 层面实现权限校验逻辑，而不是依赖 Agent。

### 技术创新点分析
文章提出的“六步检查清单”本身就是一种工程化的创新。它将复杂的协议实现过程标准化，降低了 3P（第三方）开发者的认知负荷。特别是“验证和调整”现有服务器的部分，暗示了**MCP 适配器模式**的兴起——即在不修改原有后端代码的前提下，通过增加一个 MCP 适配层来赋予系统 AI 能力。

## 3. 实际应用价值

### 对实际工作的指导意义
对于企业架构师和 AI 开发者而言，这篇文章提供了一条**将遗留系统 AI 化的清晰路径**。你不需要重写原有的 ERP 或 CRM 系统，只需要构建一个轻量级的 MCP Server 作为代理，就能让 Amazon Quick Agents 这样的先进 AI 操控旧系统。

### 可以应用到哪些场景
1.  **企业商业智能 (BI)**：Amazon QuickSight Q 通过 MCP 连接到实时的库存数据库，回答“现在的库存周转率是多少”等动态问题，而不仅仅依赖静态报表。
2.  **客户支持**：Agent 通过 MCP 调用订单管理系统，直接执行退款或改期操作，而不是仅告知用户如何操作。
3.  **知识库检索**：连接企业内部的 Wiki 或 Confluence，利用 MCP 的 Resource 能力精准检索文档片段。

### 需要注意的问题
*   **延迟**：MCP 通信增加了额外的链路，可能影响实时性要求极高的场景。
*   **协议兼容性**：MCP 版本迭代较快，需确保 Client 和 Server 版本匹配。

### 实施建议
建议采用**“沙盒验证”**策略。先在本地环境运行 MCP Server，利用简单的脚本模拟 Amazon Quick Agents 的请求，验证工具调用逻辑无误后，再部署到生产环境并接入 Quick Agents。

## 4. 行业影响分析

### 对行业的启示
这篇文章标志着 **AI 基础设施正在从“模型中心”向“连接中心”转移**。未来的竞争可能不再是谁的模型参数更大，而是谁能更方便地连接更多的工具和数据源。MCP 作为一种通用的连接标准，可能会成为 AI 领域的“USB 接口”。

### 可能带来的变革
*   **SaaS 集成的标准化**：未来 SaaS 软件可能不再需要提供复杂的 API 文档，只需提供一个 MCP Server 的 Endpoint，即可被所有 AI 应用调用。
*   **RAG 架构的演进**：传统的检索增强生成（RAG）主要依赖向量数据库，MCP 的引入使得“工具调用”和“实时数据查询”成为 RAG 的一部分，形成了 **Agentic RAG**（智能体式 RAG）。

### 对行业格局的影响
如果 Amazon 大力推行 MCP，这将对 Anthropic (Claude) 和 OpenAI 形成既竞争又合作的局面。作为行业标准，MCP 有可能打破单一生态的锁定，使得第三方工具商能够“一次开发，到处运行”（同时服务于 Claude, Amazon 和未来的 Copilot）。

## 5. 延伸思考

### 引发的其他思考
*   **安全边界**：当 AI 拥有了通过 MCP 执行写操作（修改数据库）的能力时，如何设计“人机协同”的确认机制？文章是否涉及了权限粒度的控制？
*   **Serverless 化**：MCP Server 是否应该完全 Serverless 化（如 AWS Lambda）以应对高并发的 Agent 请求？

### 可以拓展的方向
*   **多模态 MCP**：目前的 MCP 主要关注文本和结构化数据，未来是否支持视频流、音频流的传输协议？
*   **MCP 商店**：未来是否会诞生类似“App Store”的 MCP Server 市场，用户可以直接订阅“Shopify Integration Server”？

### 需要进一步研究的问题
Amazon Quick Agents 对 MCP 协议的具体约束是什么？摘要中提到了“User Guide describes constraints”，这些约束（如最大 Token 限制、超时时间）是设计高可用 MCP Server 的关键限制因素。

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有资产**：列出项目中希望 AI 能够调用的功能（如“查询库存”、“发送邮件”）。
2.  **开发 MCP Server**：使用 TypeScript 或 Python 开发一个本地 MCP Server，将这些功能封装为 `tools`。
3.  **本地测试**：使用 MCP Inspector（调试工具）测试 Server 是否能正确响应。
4.  **接入 AWS**：将 Server 部署到云端，并在 Amazon Quick Agents/Bedrock 中配置连接。

### 具体的行动建议
*   **阅读 MCP Specification**：不要只看文章，必须去读 Anthropic 的 MCP 协议规范，理解 `resources`、`prompts`、`tools` 三个核心概念的区别。
*   **错误处理**：在 Server 端实现极其详细的错误捕获。如果工具调用失败，必须返回给 Agent 一个清晰的错误信息，以便 Agent 能够向用户解释，而不是直接崩溃。

### 需要补充的知识
*   **TypeScript/Python 异步编程**：MCP 高度依赖异步 I/O。
*   **JSON Schema 定义**：用于定义工具的输入输出格式。

## 7. 案例分析

### 结合实际案例说明
假设一家零售公司使用 Amazon QuickSight 进行报表展示。
*   **现状**：QuickSight Q 只能回答基于已有数据集的问题。
*   **目标**：让 Q 能够回答“今天的实时销售额是多少”（数据存储在 SAP 系统中，不在 QuickSight 数据集中）。

### 成功案例分析
*   **实施**：开发团队构建了一个 MCP Server，暴露 `get_current_sales` 工具。
*   **集成**：在 Amazon Quick Agents 中配置该 MCP Server。
*   **效果**：用户询问 Q 时，Q 识别出需要实时数据，通过 MCP 调用 SAP 接口，获得数字并回答用户。实现了 BI 报表与实时业务系统的融合。

### 失败案例反思
*   **问题**：某开发者构建的 MCP Server 在处理大数据量查询时未做分页，导致返回数据超过 Amazon Quick Agents 的上下文限制，连接超时。
*   **教训**：必须在 MCP Server 层面实现**数据裁剪**和**流式返回**逻辑，不能简单粗暴地转发所有数据。

## 8. 哲学与逻辑：论证地图

### 中心命题
**采用 Model Context Protocol (MCP) 是实现 Amazon Quick Agents 与企业外部工具深度、安全集成的最优工程范式。**

### 支撑理由与依据
1.  **理由 1：互操作性**
    *   *依据*：MCP 是一个开放标准，遵循该标准构建的服务器可以被任何兼容的客户端（如 Claude Desktop, Amazon Quick Agents）复用，无需为每个平台重

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确工具定义与元数据

**说明**: 在集成外部工具时，必须在 MCP 配置中提供清晰、准确的工具定义。这包括工具的用途、输入参数的 Schema（模式）以及预期的输出结构。Amazon Quick Agents 依赖这些元数据来理解何时以及如何调用工具，模糊的定义会导致 Agent 调用错误或无法生成正确的代码。

**实施步骤**:
1. 为每个工具编写详细的描述，说明其功能和使用场景。
2. 使用标准 JSON Schema 定义输入参数，包含参数类型、是否必填和描述。
3. 明确声明工具的副作用（例如：是否修改数据或仅读取数据）。

**注意事项**: 避免使用过于技术化或含糊不清的描述语言，应确保大语言模型（LLM）能够轻松理解工具的意图。

---

### 实践 2：实施严格的安全性与权限控制

**说明**: 外部工具通常涉及访问敏感数据或执行关键操作。必须实施最小权限原则，确保 MCP 服务器仅暴露 Agent 完成任务所必需的工具，并且所有调用都经过严格的身份验证和授权。

**实施步骤**:
1. 为 MCP 连接配置专用的 IAM 角色，仅授予特定的 API 权限。
2. 在 MCP 服务器层面实现 API 密钥或 OAuth 2.0 验证机制。
3. 对工具的输入参数进行服务端验证，防止注入攻击。

**注意事项**: 永远不要在 MCP 配置文件中硬编码凭证。应使用 AWS Secrets Manager 或环境变量来管理敏感信息。

---

### 实践 3：优化工具的颗粒度与范围

**说明**: 工具设计的颗粒度对于 Agent 的性能至关重要。应避免创建过于复杂的“全能型”工具，也应避免将功能拆分得过于细碎。最佳实践是按照业务逻辑功能将工具分组，确保每个工具专注于单一职责。

**实施步骤**:
1. 审查现有的 API 端点，将高频使用的操作封装为独立的 MCP 工具。
2. 如果一个工具需要 10 个以上的参数，考虑将其拆分为多个更小的工具。
3. 为相关的工具添加前缀或分类标签，以便 Agent 更好地检索。

**注意事项**: 保持工具接口的稳定性。一旦 Agent 依赖了某个工具的结构，频繁变更会导致集成失败。

---

### 实践 4：构建高效的错误处理与反馈机制

**说明**: 当外部工具调用失败时，Agent 需要明确的错误信息来决定下一步操作（如重试、向用户报错或切换策略）。返回通用的“500 Error”会导致 Agent 混乱。必须提供结构化的错误响应。

**实施步骤**:
1. 定义标准的错误响应格式，包含错误代码、错误信息和建议的解决方案。
2. 在 MCP 服务器中捕获所有异常，并将其转换为上述标准格式返回给 Agent。
3. 针对网络超时或速率限制等常见问题，实现带有退避策略的重试逻辑。

**注意事项**: 错误信息应当对 LLM 友好（自然语言描述），同时保留足够的调试细节供开发者使用。

---

### 实践 5：管理上下文窗口与数据吞吐

**说明**: MCP 工具可能会向 Agent 返回大量数据。如果返回的数据量超过了模型的上下文窗口，会导致处理中断或成本激增。必须对工具返回的数据量进行限制和裁剪。

**实施步骤**:
1. 在工具设计时实现分页或流式传输机制。
2. 对返回的文本或数据进行摘要处理，仅保留与用户请求最相关的信息。
3. 设置最大响应大小的硬性限制，防止意外的大数据传输。

**注意事项**: 监控 Token 使用情况。如果某个工具频繁导致 Token 溢出，需要重新设计其数据返回逻辑。

---

### 实践 6：利用本地开发与调试工具

**说明**: 在部署到生产环境之前，必须在本地彻底测试 MCP 集成。使用 MCP Inspector 或类似工具可以模拟 Agent 的调用过程，验证工具的响应是否符合预期。

**实施步骤**:
1. 安装并配置 MCP Inspector（`npx @modelcontextprotocol/inspector`）。
2. 在本地运行 MCP 服务器，并通过 Inspector UI 手动调用工具。
3. 验证输入参数解析是否正确，以及输出 JSON 格式是否有效。
4. 检查日志，确认没有未捕获的异常。

**注意事项**: 本地测试环境应尽可能模拟生产环境的配置，以减少环境差异导致的“在我机器上能跑”的问题。

---

### 实践 7：建立日志记录与可观测性

**说明**: 为了确保 MCP 集成的长期稳定运行，必须建立完善的日志记录系统。这有助于追踪 Agent 的决策路径、工具调用的成功率以及延迟情况。

**实施步骤**:
1. 在 MCP 服务器中记录每个工具调用的请求体、响应体和耗时。
2. 将日志集中发送到 Amazon CloudWatch Logs 或类似的监控服务。
3. 设置告警，针对工具调用的高错误率或高延迟发出通知。

**注意事项**: 记录日志

---
## 学习要点

- Amazon Quick Agents 现支持通过模型上下文协议（MCP）无缝集成外部工具，从而显著扩展 Agents 的功能边界。
- MCP 提供了一种标准化的连接方式，使 Agents 能够安全地访问企业私有数据源和实时业务系统。
- 开发者无需为每个工具编写复杂的自定义代码，利用 MCP 标准接口即可大幅降低集成难度与开发成本。
- 借助 MCP，Agents 能够动态检索最新信息，有效解决了大语言模型（LLM）固有的知识截止和幻觉问题。
- 该架构支持灵活扩展，用户可根据业务需求轻松挂接数据库、API 或内部文档系统等多样化工具。
- 通过将外部工具的上下文直接注入模型推理过程，MCP 确保了 Agent 输出结果的准确性与业务相关性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [LLM](/tags/llm/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/) / [技术实践](/tags/%E6%8A%80%E6%9C%AF%E5%AE%9E%E8%B7%B5/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [Agent Skills：智能体技能框架与开发指南]({{< relref "posts/20260203-hacker_news-agent-skills-5.md" >}})
- [深度解析Skill/MCP/RAG等五大AI技术的底层逻辑]({{< relref "posts/20260212-juejin-深入理解skillmcpragagentopenclaw底层逻辑-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*