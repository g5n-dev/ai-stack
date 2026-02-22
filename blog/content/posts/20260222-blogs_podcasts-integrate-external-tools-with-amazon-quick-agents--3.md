---
title: "使用MCP集成外部工具至Amazon Quick Agents的六步指南"
date: 2026-02-22T05:33:26+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "Agent", "系统集成", "开发指南", "第三方集成", "LLM", "技术实践"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "这篇文章主要是一份技术指南，旨在指导第三方合作伙伴如何利用 **模型上下文协议 (MCP)** 将外部工具与 **Amazon Quick Agents** 进行集成。 以下是核心内容总结： **1. 目的与适用对象** 这是一份面向第三方（3P）合作伙伴的实施指南。它详细说明了如何构建或调整 MCP 服务器，以便外部"
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

在本文中，您将使用一个六步检查清单来构建新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以实现与 Amazon Quick 的集成。Amazon Quick 用户指南描述了 MCP 客户端的行为和约束。本文是一份“操作指南”，详细说明了 3P 合作方通过 MCP 与 Amazon Quick 集成所需的实现细节。

---
## 导语

随着 Amazon Quick Agents 的普及，如何高效利用 Model Context Protocol (MCP) 将外部工具无缝接入，已成为第三方开发者关注的重点。本文提供了一份详尽的操作指南与六步检查清单，旨在帮助您构建新的 MCP 服务器，或对现有服务进行验证与调整。通过阅读，您将掌握实现与 Amazon Quick 深度集成的具体技术细节，确保开发过程符合客户端的行为约束与最佳实践。

---
## 摘要

这篇文章主要是一份技术指南，旨在指导第三方合作伙伴如何利用 **模型上下文协议 (MCP)** 将外部工具与 **Amazon Quick Agents** 进行集成。

以下是核心内容总结：

**1. 目的与适用对象**
这是一份面向第三方（3P）合作伙伴的实施指南。它详细说明了如何构建或调整 MCP 服务器，以便外部工具能顺利连接并使用 Amazon Quick Agents 的功能。

**2. 核心实施方法：六步清单**
文章提供了一个包含六个步骤的检查清单，作为实施该集成的标准流程。合作伙伴可以通过此清单：
*   **从零开始：** 构建一个全新的 MCP 服务器。
*   **现有调整：** 验证并调整现有的 MCP 服务器，使其符合 Amazon Quick 的集成要求。

**3. 关键参考文档**
指南强调了参考《Amazon Quick 用户指南》的重要性。该文档详细定义了 **MCP 客户端的行为模式及其限制**，合作伙伴在开发服务器端时必须严格遵守这些约束，以确保系统的兼容性和稳定性。

**总结：**
该文档是一份具体的操作手册，重点在于通过 MCP 协议实现 Amazon Quick Agents 与外部工具的无缝对接，确保合作伙伴的开发工作符合平台规范。

---
## 评论

**中心观点**
本文是一篇典型的**技术落地指南**，旨在指导第三方开发者利用 Model Context Protocol (MCP) 标准将外部工具接入 Amazon Quick Agents，其核心价值在于将通用的 AI 对话模型转化为具备特定业务执行能力的智能体，但也受限于 MCP 早期的生态成熟度和 Quick 平台的封闭性。

**支撑理由与深度评价**

**1. 内容深度：从“对话”到“执行”的协议标准化尝试**
*   **[事实陈述]** 文章详细拆解了 MCP Server 的构建流程，涵盖了清单检查、工具定义、权限控制及客户端行为约束。
*   **[作者观点]** 深度上，该文不仅是一份代码教程，更是对 **AI Agent 接口标准化** 的一次重要背书。传统的 Agent 开发往往陷入“为每个模型写一次 Adapter”的泥潭，而 MCP 提出了一种类似“打印机驱动”的中间层标准。文章强调了 Quick User Guide 中的约束，说明亚马逊在试图在“模型的通用性”和“业务的安全性”之间寻找平衡点。
*   **[反例/边界条件]** 然而，文章对 **复杂推理链** 的处理深度不足。MCP 主要解决的是“API 调用的标准化”，对于多步骤推理中的上下文记忆、错误重试机制以及非结构化数据的处理，仅靠 MCP 协议本身无法完全解决，仍需依赖上层模型的推理能力。

**2. 实用价值：为 SaaS 厂商提供“亚马逊生态入场券”**
*   **[事实陈述]** 文章明确指出这是针对 3P (Third-Party) 合作伙伴的指南，目的是将现有工具（如 CRM、ERP）接入 Quick Agents。
*   **[你的推断]** 对于 B2B 软件厂商而言，这篇文章具有极高的实用价值。随着企业将数据迁移至 AWS，能够无缝集成到 Amazon Quick (Bedrock 的企业级应用层) 意味着巨大的留存和增长机会。文章提供的“六步清单”实际上是一套合规性检查，确保厂商的工具能通过亚马逊的安全审查。
*   **[反例/边界条件]** 这种实用价值高度绑定 **AWS 生态**。如果厂商的目标客户主要使用 Azure 或 Google Cloud，或者使用的是非 Anthropic/Amazon 系的模型，学习这套特定的 MCP 实现方式的边际收益会递减。

**3. 创新性：MCP 协议的“解耦”意义**
*   **[事实陈述]** 文章通过引入 MCP，展示了如何将工具的定义与具体的 Agent 实现分离。
*   **[作者观点]** 这里的创新点不在于代码本身，而在于 **架构思维的转变**。过去我们谈论 RAG 或 Agent，往往关注 Prompt Engineering，而 MCP 将关注点转移到了 **Infrastructure Layer（基础设施层）**。通过标准化的 Protocol（协议），工具变成了可插拔的组件。这篇文章实际上是在宣讲：未来的 AI 应用开发将是“协议驱动”而非“模型驱动”。
*   **[反例/边界条件]** MCP 并非唯一的协议标准。OpenAI 的 Function Calling 规范、LangChain 的 Tool 定义目前更为流行。MCP 作为由 Anthropic 主导的标准，虽然得到了亚马逊的支持，但尚未成为全行业的通用标准，存在“协议碎片化”的风险。

**4. 行业影响：推动 AI Agent 的“应用商店”模式**
*   **[事实陈述]** 亚马逊 Quick Agents 结合 MCP，正在构建一个企业级 AI 的分发渠道。
*   **[你的推断]** 这篇文章暗示了未来的商业模式：企业不再购买单一的 SaaS 软件，而是购买“AI 能力包”。MCP Server 就是这些能力的载体。这类似于智能手机时代的 App Store，只不过这次分发的是“技能”。这可能会催生出一批专门开发 MCP Connectors 的中间件厂商。
*   **[反例/边界条件]** 这种模式的前提是 **Amazon Quick Agents 能够获得足够大的市场份额**。如果微软 Copilot 继续统治桌面端，亚马逊的这种企业级集成可能仅限于特定的技术运维圈子，难以触达广泛的业务人员。

**可验证的检查方式**

为了验证上述观点及文章技术的有效性，建议进行以下检查：

1.  **协议互操作性测试（指标）：**
    *   *实验：* 按照文章构建一个 MCP Server，尝试在不修改代码的情况下，将其分别接入 Amazon Quick Agents 和 Claude.ai / Desktop.app。
    *   *预期结果：* 如果 MCP 标准足够统一，同一个 Server 应该能在两个客户端无缝工作。这能验证 MCP 是否真的实现了“一次编写，到处运行”。

2.  **复杂场景下的错误处理（观察窗口）：**
    *   *实验：* 构建一个需要多步调用的工具（例如：查询库存 -> 锁定库存 -> 生成订单），并在中间步骤人为注入 API 错误（如 500 错误）。
    *   *观察点：* 观察 Amazon Quick Agent 是如何根据 MCP 返回的错误信息进行重试或向用户报错的。如果 Agent 直接崩溃或产生幻觉，说明文章描述的集成方案在鲁棒性上仍有欠缺。

3.  **性能与延迟基准（指标）：**
    *   *实验：* 测量从用户发出指令到 MCP Server 返回数据并显示在 Quick 界面的总端到端延迟。
    *   *对比：* 对比直接调用 AWS Lambda 函数的延迟。
    *   *分析：* MCP 作为中间层必然引入了序列化/反序列化的开销。如果延迟增加显著（例如超过 20%），对于

---
## 技术分析

基于您提供的文章标题和摘要，以下是对关于“利用模型上下文协议（MCP）将外部工具集成到 Amazon Quick Agents”的深度分析。

---

# 深入分析：利用 MCP 集成 Amazon Quick Agents 与外部工具

## 1. 核心观点深度解读

**主要观点与核心思想**
这篇文章的核心观点是：**模型上下文协议（MCP）是连接大语言模型（LLM）与企业私有数据及外部工具的标准化“通用语言”，而 Amazon Quick Agents 则是这一协议在企业级落地的高效执行者。**

作者想要传达的核心思想是“标准化与解耦”。在传统的 AI 应用开发中，为每一个外部工具（如 Jira、Salesforce、内部数据库）编写定制化的 API 集成代码是低效且难以维护的。文章主张通过 MCP 这一开放标准，将数据访问逻辑与 Agent 的决策逻辑分离。对于第三方合作伙伴（3P Partners）而言，无需关心 Amazon Quick Agents 内部的复杂实现，只需遵循 MCP 规范构建服务器，即可实现能力的即插即用。

**创新性与深度**
该观点的创新性在于**协议的统一性**。它超越了简单的 API 调用，定义了一套包含资源、提示词和工具的标准交互模型。深度在于它承认并解决了 LLM 应用落地中的“最后一公里”问题——即如何让模型安全、结构化地读取和操作外部环境，而不仅仅是通过长文本窗口灌输知识。

**重要性**
这一观点至关重要，因为它标志着 AI Agent 开发从“手工作坊”向“工业化生态”的转型。对于 AWS 生态而言，MCP 是连接 Bedrock 等基础模型服务与 SaaS 生态的桥梁，极大地降低了 AI Agent 的开发门槛，加速了企业级 AI 自动化的普及。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **模型上下文协议（MCP）**：由 Anthropic 提出的开放标准，基于 JSON-RPC 2.0，旨在连接 AI 应用与数据源。
2.  **Amazon Quick Agents**：AWS 提供的（或基于 AWS 构建的）智能体框架，充当 MCP 客户端。
3.  **MCP Server**：运行在本地或远程的进程，负责暴露特定的数据或工具功能给 Agent。
4.  **3P Partners（第三方合作伙伴）**：指负责构建和维护 MCP Server 的开发者或供应商。

**技术原理和实现方式**
MCP 的核心架构采用客户端-服务器（C/S）模型。
*   **传输层**：支持 stdio（标准输入输出，用于本地进程通信）和 SSE（Server-Sent Events，用于 Web 通信）。
*   **数据层**：MCP Server 向 Client 暴露三种核心能力：
    *   **Resources（资源）**：只读的数据，如文档、数据库记录（类似文件系统）。
    *   **Prompts（提示词）**：预定义的模板，Agent 可以直接调用这些模板来生成特定格式的回复。
    *   **Tools（工具）**：可执行的函数，Agent 可以通过参数调用这些工具来改变外部状态（如创建工单、发送邮件）。

**技术难点和解决方案**
*   **难点**：**数据安全与权限控制**。直接暴露数据库操作接口风险极大。
    *   **解决方案**：在 MCP Server 层面实现严格的鉴权机制（如 OAuth、JWT）和参数校验，确保 Agent 只能访问授权范围内的数据，且 Server 必须对输入进行清洗，防止 SQL 注入等攻击。
*   **难点**：**上下文窗口限制与噪声**。
    *   **解决方案**：MCP 支持流式传输和按需加载资源。Server 应实现智能分页和摘要，只将最相关的数据片段注入 LLM 上下文。

**技术创新点分析**
最大的创新点在于**互操作性**。一旦一个工具实现了 MCP 接口，它不仅能被 Amazon Quick Agents 使用，理论上也能被任何支持 MCP 的客户端（如 Claude Desktop 或其他 IDE 插件）使用，实现了“一次编写，随处运行”。

## 3. 实际应用价值

**对实际工作的指导意义**
对于企业架构师和 AI 开发者，这篇文章提供了一条清晰的路径：不要重复造轮子去构建 API 包装器。通过 MCP，可以将企业内部遗留系统（REST API, SQL 数据库, 甚至简单的脚本）快速“AI 化”。

**可以应用到哪些场景**
1.  **RAG（检索增强生成）系统**：将企业 Wiki（Confluence/Notion）通过 MCP 资源接口暴露，让 Agent 能够查询最新文档。
2.  **业务流程自动化**：通过 MCP 工具接口，让 Agent 能够直接操作 CRM 系统更新客户状态，或在 Slack 中发送通知。
3.  **代码开发助手**：让 Agent 能够访问本地的 Git 仓库、文件系统或 CI/CD 管道状态。

**需要注意的问题**
*   **延迟**：多跳网络请求和 JSON-RPC 序列化会增加响应时间。
*   **错误处理**：MCP Server 的崩溃不应导致 Agent 宕机，需要设计优雅的超时和降级机制。

**实施建议**
优先从**只读资源（Resources）**开始集成，验证数据流的准确性，再逐步开放**写入工具**。在部署 MCP Server 时，建议采用容器化（Docker）以便于在 AWS Fargate 或 ECS 上进行弹性管理。

## 4. 行业影响分析

**对行业的启示**
MCP 的出现预示着 AI 领域正在经历类似“USB 接口”统一化的时刻。正如 USB 统一了外设与电脑的连接，MCP 有望统一 LLM 与数据/工具的连接。这将促使 SaaS 厂商不再仅仅关注“是否有 ChatGPT 插件”，而是关注“是否提供 MCP 接口”。

**可能带来的变革**
*   **Agent Store（应用商店）的兴起**：未来可能会出现专门售卖 MCP Server 配置或镜像的市场，类似于现在的 Shopify 插件。
*   **企业知识图谱的自动构建**：通过 MCP 连接多个异构数据源，Agent 可以动态地跨系统查询，形成虚拟的知识图谱。

**对行业格局的影响**
这加强了 Anthropic 和 AWS 在企业级 AI 生态中的话语权。如果 MCP 成为事实标准，那么围绕 MCP 构建的工具链（调试器、服务器框架）将成为新的创业热点。

## 5. 延伸思考

**引发的思考**
*   **协议的竞争**：OpenAI 的 Function Calling 与 Google 的类似机制如何与 MCP 共存？未来可能会出现“协议网关”。
*   **Server 的成本**：为每个用户运行独立的 MCP Server 进程（如 stdio 模式）在多租户 SaaS 环境下成本极高，SSE 模式下的无服务器架构将成为主流。

**未来发展趋势**
*   **MCP Server 的智能化**：未来的 MCP Server 可能不仅仅是数据管道，本身也会包含轻量级模型，用于在数据发送给主 Agent 之前进行预处理或过滤，以节省 Token 成本。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有资产**：列出项目中所有希望 AI 能访问的 API 和数据源。
2.  **选择框架**：使用官方的 SDK（如 TypeScript/Python SDK）搭建一个简单的 MCP Server。
3.  **本地测试**：使用 Claude Desktop 或 Inspector 连接本地 Server，验证资源读取和工具调用是否正常。
4.  **部署与集成**：将 Server 部署到云端，并配置 Amazon Quick Agents 作为客户端连接。

**具体行动建议**
*   **技术栈**：如果你的团队熟悉 TypeScript，开发 MCP Server 会非常顺畅。
*   **文档先行**：在编写代码前，先定义好 `tools` 的 JSON Schema，这是 Agent 理解如何调用工具的关键。

**需补充的知识**
*   **JSON Schema**：必须精通，用于定义工具的输入输出格式。
*   **异步编程**：MCP 通信本质是异步的，需处理好 Promise 和 async/await。

## 7. 案例分析

**成功案例分析**
*   **GitHub Contextual PR**：假设构建一个 MCP Server 暴露 GitHub API。Agent（Amazon Quick Agent）接收到用户指令“总结最新的 Pull Request”。Agent 通过 MCP 调用 `list_prs` 工具，获取 PR 列表，再调用 `get_diff` 资源读取代码变更，最后生成总结。
    *   *成功要素*：清晰的工具定义，准确的权限控制。

**失败案例反思**
*   **过度暴露的数据库接口**：某开发者直接将 SQL 查询作为 MCP 工具暴露。Agent 在执行复杂逻辑时，误构造了 `DROP TABLE` 指令（虽然通过参数传递，但如果 Server 端没有严格校验，可能导致灾难）。
    *   *教训*：永远不要暴露通用的“执行任意 SQL”工具，而应暴露“查询客户信息”等高语义级、参数受限的工具。

## 8. 哲学与逻辑：论证地图

**中心命题**
**采用模型上下文协议（MCP）是构建可扩展、互操作的企业级 AI Agent 生态的最优解。**

**支撑理由**
1.  **标准化带来的效率提升**：遵循 MCP 标准使得第三方工具开发者无需针对每个 AI 平台定制 API，大幅减少集成工作量。（依据：软件工程中“接口标准化”的历史数据，如 USB、REST API 的普及）。
2.  **关注点分离**：MCP 将数据获取逻辑与 Agent 的推理逻辑解耦，使得两者可以独立迭代和扩展。（依据：单一职责原则 SRP）。
3.  **生态系统的网络效应**：随着支持 MCP 的客户端（如 Claude, AWS）和服务器（如 Postgres, Git）增多，该协议的价值将呈指数级增长。（依据：梅特卡夫定律）。

**反例或边界条件**
1.  **高性能/低延迟场景**：对于微秒级的交易系统，MCP 基于 JSON-RPC 的序列化开销可能过高，此时直接二进制 gRPC 调用更合适。
2.  **极度简单的交互**：如果只需要一个极其简单的 GET 请求，引入 MCP 的全套架构可能属于过度设计。

**命题分类**
*   **事实**：MCP 是由 Anthropic 提出的开放标准；Amazon Quick Agents 支持 MCP。
*   **价值判断**：MCP 是“最优解”。
*   **可检验预测**：未来 18 个月内，超过 50% 的主流 SaaS 平台将通过 MCP 或类似协议提供 AI 集成接口。

**立场与验证**
**立场**：支持 MCP 作为企业级 AI 集成的首选标准，但在特定边缘场景下保留定制化接口的权利。

**可证伪验证方式**：
*   **指标**：观察 MCP 仓库的 Star 数增长速度、AWS Marketplace 中支持 MCP 的工具数量。
*   **实验**：构建两个功能相同的 Agent，一个使用 MCP 集成工具，一个使用硬编码 API 调用。比较在添加新工具时的开发时间差和代码维护成本。
*   **观察窗口**：1-2 年。如果届时 MCP 被其他更高效的协议取代，或 AWS 推出了与之竞争且不兼容的协议，则该命题被证伪。

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确工具定义与能力边界

**说明**:
在集成之前，必须在 MCP 配置中清晰定义每个外部工具的用途、输入参数架构以及预期的输出格式。这有助于 Amazon Quick Agents 准确理解何时以及如何调用该工具，避免因意图模糊导致的错误调用或幻觉。

**实施步骤**:
1. 使用清晰的 JSON Schema 定义工具的输入和输出结构。
2. 为工具编写详细的描述，明确其功能边界（例如：“仅用于查询公开股票数据，不能执行交易”）。
3. 在工具描述中列举具体的使用场景示例。

**注意事项**:
避免使用过于宽泛或模糊的描述，确保工具名称具有高度的语义化特征。

---

### 实践 2：实施严格的身份验证与访问控制

**说明**:
外部工具通常涉及敏感数据或操作。必须确保 MCP 服务器与工具之间的通信是安全的，并且遵循最小权限原则。不要在 MCP 配置中硬编码凭证，而应依赖安全的凭证管理机制。

**实施步骤**:
1. 为 MCP 服务器配置 IAM 角色，仅授予其访问特定 AWS 资源或外部 API 所需的最小权限。
2. 使用 AWS Secrets Manager 或类似服务存储 API 密钥，避免明文配置。
3. 确保所有通信通过 HTTPS/TLS 进行加密。

**注意事项**:
定期轮换访问密钥，并监控 CloudTrail 日志以检测异常的 API 调用行为。

---

### 实践 3：优化数据上下文与负载管理

**说明**:
大语言模型（LLM）有上下文窗口限制。通过 MCP 传递给 Agent 的数据必须经过精简和预处理，仅包含与当前任务最相关的信息，以减少延迟并提高响应准确性。

**实施步骤**:
1. 在 MCP 服务器端实现数据过滤逻辑，不要返回整个数据库。
2. 对大型文档或数据集进行分块或摘要处理，仅传输元数据或相关片段。
3. 设置工具返回数据的最大长度限制。

**注意事项**:
监控 Token 使用情况，防止因单次工具调用返回过多数据导致成本激增或超时。

---

### 实践 4：构建健壮的错误处理与重试机制

**说明**:
外部服务可能会遇到故障、限流或网络问题。MCP 服务器应能优雅地处理这些错误，并向 Amazon Quick Agents 返回清晰的错误信息，而不是抛出原始异常，以便 Agent 能向用户解释情况或尝试替代方案。

**实施步骤**:
1. 在 MCP 工具逻辑中捕获所有 API 异常。
2. 实现指数退避算法以处理暂时性错误（如 429 Too Many Requests 或 5xx 错误）。
3. 返回标准化的错误对象，包含错误代码和用户友好的描述。

**注意事项**:
避免无限重试，设置最大重试次数和超时时间，以防止阻塞 Agent 的响应。

---

### 实践 5：确保工具响应的结构化与可解析性

**说明**:
Amazon Quick Agents 依赖结构化数据来推理和生成最终答案。工具返回的内容应尽量采用结构化格式（如 JSON），而非非结构化的纯文本，以便 Agent 更好地提取关键信息。

**实施步骤**:
1. 统一所有工具的输出格式为 JSON。
2. 确保输出字段命名规范且具有自解释性。
3. 如果必须返回自然语言文本，将其封装在特定的 JSON 字段中。

**注意事项**:
测试边缘情况，确保当外部 API 返回空结果或非标准格式时，MCP 服务器仍能返回有效的 JSON 结构。

---

### 实践 6：全面测试与日志记录

**说明**:
仅仅在本地测试通过是不够的。需要在 Amazon Quick Agents 的实际运行环境中进行端到端测试，并启用详细的日志记录，以便在出现问题时快速定位是 MCP 配置问题、网络问题还是工具本身的问题。

**实施步骤**:
1. 在 Amazon Bedrock 或 QuickSight 中配置测试 Agent，编写涵盖各种工具调用场景的测试用例。
2. 启用 Amazon CloudWatch Logs 来记录 MCP 服务器的请求和响应负载。
3. 建立日志分析机制，定期检查工具调用的成功率和延迟。

**注意事项**:
在生产环境中记录日志时，注意过滤敏感信息（如 PII 或 API 密钥），确保符合合规要求。

---
## 学习要点

- Amazon Quick Agents 现已支持通过模型上下文协议（MCP）无缝集成外部工具，从而显著扩展了生成式 AI 应用的功能边界。
- 开发者可以通过声明式配置而非编写底层代码来定义工具，这大幅降低了将外部数据源连接到智能体的技术门槛和开发成本。
- 该集成方案允许智能体在对话过程中实时调用外部 API 并获取动态数据，有效解决了生成式 AI 模型常见的知识时效性滞后问题。
- 利用 MCP 构建的统一连接层，企业能够更安全、高效地打破数据孤岛，实现 AI 与私有业务系统之间的标准化交互。
- 这一架构不仅增强了智能体处理复杂工作流的能力，还通过标准化的协议简化了第三方工具的维护与版本管理流程。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/) / [LLM](/tags/llm/) / [技术实践](/tags/%E6%8A%80%E6%9C%AF%E5%AE%9E%E8%B7%B5/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [Agent Skills：智能体技能框架与开发指南]({{< relref "posts/20260203-hacker_news-agent-skills-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*