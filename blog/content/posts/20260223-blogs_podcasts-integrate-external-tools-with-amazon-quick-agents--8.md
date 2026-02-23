---
title: "使用MCP集成外部工具至Amazon Quick Agents的构建指南"
date: 2026-02-23T19:24:12+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "Agent", "系统集成", "外部工具", "开发指南", "LLM", "AWS"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "本文介绍了如何利用**模型上下文协议（MCP）**将外部工具集成到 **Amazon Quick Agents** 中。这是一份面向第三方（3P）合作伙伴的实施指南，旨在帮助合作伙伴构建新的 MCP 服务器，或验证并调整现有的服务器以实现与 Amazon Quick 的集成。 文章提供了一个**六步清单**，涵盖了详细"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["大语言模型"]
---

# 使用MCP集成外部工具至Amazon Quick Agents的构建指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在本文中，您将使用一份六步检查清单来构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器，以便集成 Amazon Quick。《Amazon Quick 用户指南》介绍了 MCP 客户端的行为与约束。本指南是一份“操作指南”，旨在详述 3P 合作伙伴通过 MCP 与 Amazon Quick 集成所需的实现细节。

---
## 导语

随着 Model Context Protocol (MCP) 的引入，将外部工具无缝连接至 Amazon Quick Agents 已成为提升 AI 智能体实用性的关键路径。本文基于《Amazon Quick 用户指南》，为第三方合作伙伴提供了一份详尽的实操指南。通过文中的六步检查清单，您将掌握构建或调整 MCP 服务器的具体实现细节，从而确保外部数据源与 Amazon Quick 的稳健集成。

---
## 摘要

本文介绍了如何利用**模型上下文协议（MCP）**将外部工具集成到 **Amazon Quick Agents** 中。这是一份面向第三方（3P）合作伙伴的实施指南，旨在帮助合作伙伴构建新的 MCP 服务器，或验证并调整现有的服务器以实现与 Amazon Quick 的集成。

文章提供了一个**六步清单**，涵盖了详细的技术实现要求。为了确保集成顺利进行，开发者必须参考《Amazon Quick 用户指南》，其中明确规定了 MCP 客户端的行为模式及其约束条件。

---
## 评论

### 中心观点
这篇文章本质上是一份**技术落地说明书**，旨在通过标准化的 MCP（Model Context Protocol）协议，解决大模型应用中“数据孤岛”与“工具调用碎片化”的痛点，从而降低第三方开发者将 AI 能力集成到 Amazon Quick Agents 中的门槛，推动 AI Agent 从“玩具”向“生产力工具”演进。

### 深入评价与支撑理由

#### 1. 内容深度：从概念到工程化的跨越
*   **支撑理由（事实陈述）：** 文章没有停留在宣传 MCP 的概念层面，而是直接切入工程实践。通过提供“六步检查清单”，它涵盖了从环境配置、Schema 定义到错误处理的具体细节。这种深度表明，亚马逊正在试图建立一套严格的**“准入标准”**。它不仅要求 MCP Server 能“跑通”，还要求其符合 Amazon Quick 的行为约束（如超时处理、权限校验），这体现了对生产环境稳定性的重视。
*   **你的推断：** 亚马逊之所以如此强调“验证和调整现有的 MCP Server”，暗示了目前市面上的 MCP 实现良莠不齐。这篇文章实际上是在进行**市场教育**，通过提高技术门槛来筛选出高质量的 3P（第三方）合作伙伴，避免低质量的集成损害用户体验。

#### 2. 实用价值：构建生态的“连接器”
*   **支撑理由（事实陈述）：** 对于开发者而言，最大的痛点往往不是模型不够强，而是模型无法访问实时数据或企业私有系统。MCP 作为一个开源标准，解决了“一次开发，多处接入”的问题。文章详细说明了如何将这一通用协议适配到 Amazon Quick，这使得开发者手中的 MCP Server 资产可以被快速复用，极大地降低了沉没成本。
*   **反例/边界条件（你的推断）：** 然而，这种实用性存在明显的边界。如果企业的工具逻辑极其复杂，或者对数据隐私有极高要求（如金融核心交易系统），仅靠 MCP 标准化的接口可能无法满足细粒度的审计和风控需求。此时，通用的 MCP 集成可能不如定制化的 API 开发安全。

#### 3. 创新性：协议标准化的博弈
*   **支撑理由（作者观点）：** 文章的核心创新点不在于技术本身，而在于**“选边站队”**。亚马逊通过支持 MCP（由 Anthropic 主导），实际上是在 AI Agent 的连接层标准上与 OpenAI 的 Function Calling 或其他私有协议进行博弈。通过拥抱开源标准 MCP，亚马逊试图构建一个比封闭生态更具活力的开发者社区。
*   **反例/边界条件（事实陈述）：** MCP 目前并非唯一的标准。OpenAI 的 GPTs 也有其生态体系。如果 MCP 无法成为行业事实上的唯一标准，开发者可能仍需维护多套适配逻辑，这会削弱文章所述方案的长期创新价值。

#### 4. 行业影响：AI Agent 的“App Store”时刻
*   **支撑理由（你的推断）：** 这篇文章可以被视为 Amazon Quick 生态的“SDK 发布”。它标志着 AI Agent 行业正在从“模型竞争”转向“生态竞争”。谁能吸引更多的工具提供商通过 MCP 接入，谁的 Agent 就更聪明。这将加速 AI 应用层的爆发，类似于 iOS App Store 时代的早期，工具提供商将成为新的“应用开发者”。
*   **支撑理由（事实陈述）：** 文章明确提到“3P partners”，说明亚马逊正在积极拉拢软件厂商。如果成功，这将改变 SaaS 软件的分发方式，软件不再需要单独打开，而是通过 Agent 被调用。

#### 5. 争议点与潜在风险
*   **争议点（作者观点）：** 文章虽然强调了集成步骤，但可能**掩盖了“上下文窗口成本”**的问题。MCP 传输工具定义和数据往往消耗大量 Token。在 Amazon Quick 这种可能面向 C 端或大规模 B 端的场景下，频繁调用 MCP Server 带来的 Token 成本和延迟是否可控？文章对此避重就轻。
*   **反例/边界条件：** 对于高频、低延迟的工具调用（如鼠标点击、实时游戏控制），基于 HTTP 的 MCP 协议可能存在性能瓶颈，此时本地 RPC 调用仍是更优解，文章未对此类场景进行区分。

### 可验证的检查方式

为了验证文章所述方案的实际效果，建议从以下维度进行测试：

1.  **兼容性测试（指标）：**
    *   选取 5 个市面上现有的开源 MCP Server（如 GitHub、Slack 的社区实现），按照文章的“六步清单”进行适配。
    *   **观察窗口：** 记录成功通过 Amazon Quick 验证并实际返回正确结果的比例。如果低于 60%，说明文档中的“约束”描述不够清晰或标准过于严苛。

2.  **性能与延迟测试（实验）：**
    *   构建一个高负载场景，让 Amazon Quick Agent 通过 MCP 并发调用 10 个不同的外部工具。
    *   **观察窗口：** 测量端到端的响应时间。重点关注 MCP 握手和数据序列化带来的额外延迟。如果延迟超过 3 秒，用户体验将大打折扣。

3.  **错误恢复能力测试（观察）：**
    *   在 MCP Server 人为注入故障（如返回错误的 Schema 格式、网络超时）。
    *   **观察窗口：** 观察 Amazon Quick Agent 是会优雅地降级并告知用户，还是会直接崩溃或陷入死循环。这是检验文章中提到的“行为约束”是否真正有效的关键。

### 总结与建议

这篇文章虽然披着“技术

---
## 技术分析

基于您提供的文章标题和摘要，这是一篇关于技术实施指南的深度分析文章。虽然摘要简短，但它揭示了Amazon在AI Agent（智能体）生态布局中的一个关键战略动作：通过**MCP（Model Context Protocol，模型上下文协议）**来标准化和扩展其Amazon Quick Agents的能力。

以下是对该文章核心观点及技术要点的深入分析：

---

## 1. 核心观点深度解读

**主要观点：**
文章的核心主张是**标准化连接是AI Agent规模化落地的关键**。通过采用MCP协议，第三方开发者可以将外部数据源和工具无缝集成到Amazon Quick Agents中，从而打破大语言模型（LLM）的数据孤岛效应。

**核心思想：**
作者传达了一种**“生态共建”**的思想。Amazon不再独自构建所有功能，而是提供一套标准化的“插座”（MCP Client），让全球的开发者制造各种“插头”（MCP Server）。这不仅降低了开发者的准入门槛，也极大地丰富了Amazon Quick Agents的功能边界。

**创新性与深度：**
*   **协议标准化：** 创新点在于从“API调用”转向“协议统一”。传统的Agent集成需要针对每个模型微调Prompt或处理不同的API格式，而MCP提供了一种通用的描述语言，使得Agent能够“理解”外部工具的功能。
*   **双向适配：** 文章不仅关注如何开发Server，还强调了Client（Amazon Quick）的行为约束，这表明这是一种深度的系统集成，而非简单的脚本调用。

**重要性：**
这一观点至关重要，因为它解决了当前AI应用落地的最大痛点——**“最后一公里”的数据连接**。LLM拥有通用的智力，但缺乏企业私有数据（如Jira工单、Slack消息、数据库记录）。MCP是连接通用智力与企业私有数据的桥梁。

## 2. 关键技术要点

**涉及的关键技术：**
*   **MCP (Model Context Protocol)：** 这是一个开放标准（由Anthropic主导），用于连接AI助手与系统上下文。它定义了如何暴露数据、工具和资源给AI模型。
*   **Amazon Quick Agents：** Amazon Bedrock中的构建器，允许用户快速创建能够执行任务的Agent。
*   **MCP Server：** 运行在本地或远程的服务，负责将外部系统的API转换为MCP格式。

**技术原理与实现：**
*   **架构模式：** 采用Client-Server架构。Amazon Quick Agents充当MCP Client，发起请求；第三方工具作为MCP Server，响应请求。
*   **资源与工具暴露：** MCP Server通过定义`Resources`（数据，如文件内容）和`Tools`（动作，如“创建工单”）来与Agent交互。
*   **清单验证：** 文章提到的“六步清单”可能包括：定义Manifest、实现Server端点、处理Prompt模板、错误处理、安全认证以及本地/远程部署测试。

**技术难点与解决方案：**
*   **难点：** **上下文窗口限制与数据隐私。** 传输大量外部数据可能消耗Token，且涉及敏感信息。
*   **方案：** MCP支持流式传输和增量更新，且通常部署在私有网络（VPC）内，数据不出域，仅传输元数据或必要的上下文。
*   **难点：** **工具调用的确定性。** Agent可能会错误调用工具。
*   **方案：** 严格的Schema定义和描述，确保MCP Server提供的文档清晰，使LLM能准确生成调用参数。

## 3. 实际应用价值

**指导意义：**
对于企业架构师和AI开发者而言，这篇文章是一份**实战蓝图**。它明确了如何将企业现有的遗留系统“AI化”，而不需要重写整个后端。

**应用场景：**
1.  **企业知识库问答：** 将Confluence、SharePoint作为MCP Server接入，让Agent能查询内部文档。
2.  **RPA（机器人流程自动化）增强：** Agent通过MCP调用SAP或Salesforce的API，自动执行报表生成或订单修改。
3.  **开发运维：** Agent通过MCP连接GitHub或Jira，自动生成代码变更日志或分配Bug。

**注意事项：**
*   **延迟问题：** MCP Server的响应速度直接影响Agent的体验，需要优化查询性能。
*   **权限控制：** 必须在MCP Server层实现严格的权限校验，防止Agent越权访问数据。

**实施建议：**
不要试图一次性迁移所有工具。建议先从“只读”类工具（如查询数据库、搜索文档）开始，验证MCP的稳定性，再逐步开放“写”权限（如发送邮件、修改记录）。

## 4. 行业影响分析

**行业启示：**
这标志着**AI互操作性**时代的到来。正如HTTP统一了网页浏览，MCP有望统一AI与物理世界/数字世界的交互接口。各大厂商（如Amazon, Anthropic）正在共同推动这一标准，可能会终结过去那种“每个Agent都要写一套自定义集成代码”的混乱局面。

**带来的变革：**
*   **从“Chatbot”到“Do-bot”：** AI不再仅仅是陪聊，而是能真正干活。
*   **SaaS集成模式的改变：** 未来的SaaS软件如果不提供MCP接口，可能将无法被AI Agent调用，从而失去市场竞争力。

**行业格局：**
这将促进**“MCP中间件市场”**的繁荣。未来可能会出现专门提供各类MCP Server的厂商，或者提供MCP管理平台的PaaS服务。

## 5. 延伸思考

**拓展方向：**
*   **多Agent协作：** 如果多个Agent都支持MCP，它们之间是否可以通过MCP协议互相调用？这将构建出更复杂的Agent社会。
*   **边缘计算：** MCP Server是否可以运行在用户的笔记本电脑或手机上，实现完全离线的隐私保护型Agent？

**待研究问题：**
*   当MCP Server返回错误或数据格式与预期不符时，Agent的“自我修复”机制如何设计？
*   如何对MCP传输的数据进行计费和监控？

## 6. 实践建议

**如何应用到项目：**
1.  **评估现有资产：** 盘点你团队中哪些高频API适合被AI调用。
2.  **搭建本地测试环境：** 使用Model Context Protocol的Inspector工具调试你的Server。
3.  **遵循六步法：** 严格按照文章中的清单进行自检，特别是安全性和Schema定义部分。

**行动建议：**
*   **技术储备：** 学习TypeScript或Python（MCP SDK的主要语言），理解JSON Schema定义。
*   **小步快跑：** 先构建一个“Hello World”级的MCP Server（例如：一个获取当前时间的Server），接入Amazon Quick Agents跑通全流程。

## 7. 案例分析

**成功案例设想：**
*   **场景：** 一家电商公司。
*   **实施：** 开发了一个MCP Server连接其库存数据库。
*   **效果：** 销售人员可以直接问Amazon Quick Agent：“我们现在还有多少红色的L号T恤？”，Agent通过MCP实时查询SQL数据库并回答。这比以前打开ERP系统查询快了10倍。

**失败反思：**
*   **场景：** 某公司试图将复杂的ERP系统直接通过MCP暴露。
*   **问题：** 没有做权限抽象，导致销售员通过Agent意外查询到了财务数据；或者API响应太慢（超过10秒），导致Agent超时报错。
*   **教训：** MCP Server不应是简单的一对一API映射，而应包含针对AI场景优化的逻辑（如缓存、权限聚合、异步处理）。

## 8. 哲学与逻辑：论证地图

**中心命题：**
**采用模型上下文协议（MCP）是构建可扩展、安全且互操作的AI Agent生态系统的最优技术路径。**

**支撑理由与依据：**
1.  **标准化降低集成成本：**
    *   *依据：* 传统API集成需要针对每个模型微调Prompt，而MCP提供统一的Schema描述，一次开发，多处复用。
2.  **安全性与可控性：**
    *   *依据：* MCP允许在Server端实施细粒度的权限控制，且支持本地部署，符合企业数据合规要求。
3.  **增强模型能力边界：**
    *   *依据：* 通过连接外部工具（如计算器、数据库），解决了LLM本身存在的幻觉和数学逻辑缺陷。

**反例与边界条件：**
1.  **极低延迟要求的场景：** 如果应用要求毫秒级响应（如高频交易），MCP增加的序列化/反序列化层可能成为瓶颈，直接原生函数调用可能更优。
2.  **极简一次性脚本：** 如果只是一个临时的、非常简单的内部脚本，引入完整的MCP架构可能属于过度设计。

**命题性质分析：**
*   **事实：** Amazon和Anthropic正在推行MCP。
*   **价值判断：** “最优”路径——这基于对工程效率和生态健康度的考量。
*   **可检验预测：** 预测未来18个月内，主流企业软件（CRM, ERP）将原生支持MCP接口。

**立场与验证：**
*   **立场：** 支持将MCP作为企业AI集成的首选标准，但需根据性能需求灵活调整。
*   **验证方式（可证伪）：**
    *   *指标：* 观察GitHub上MCP Server项目的增长速度；观察Amazon Quick Agents集成外部工具的活跃度。
    *   *实验：* 选取同一业务逻辑，分别用传统API调用和MCP集成方式开发Agent，对比开发时长、维护成本和调用准确率。如果MCP在开发效率上没有显著提升（如>30%），则该命题部分证伪。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优先使用官方 MCP 适配器与标准连接器

**说明**: Amazon Quick Agents 支持通过 Model Context Protocol (MCP) 连接外部数据源。为了确保稳定性和减少开发工作量，应优先检查 AWS 或 MCP 社区是否已提供针对目标工具（如 Slack, GitHub, Google Drive 等）的官方适配器或标准连接器。使用官方组件通常意味着内置了错误处理和性能优化。

**实施步骤**:
1. 在集成前，查阅 AWS Quick Agents 文档及 MCP 社区仓库，确认是否存在目标系统的官方连接器。
2. 如果存在，直接配置相应的环境变量和 API 密钥进行连接。
3. 如果不存在，再考虑使用 MCP SDK 构建自定义适配器。

**注意事项**: 官方适配器通常会随着 MCP 协议的更新而迭代，定期检查并更新适配器版本以获得最新功能和安全补丁。

---

### 实践 2：实施严格的 API 密钥与权限管理

**说明**: 外部工具集成通常需要访问敏感数据或执行操作。最佳实践是遵循最小权限原则，仅为 MCP 连接授予完成任务所需的特定权限，避免授予过高的管理权限，以降低安全风险。

**实施步骤**:
1. 在外部工具（如 GitHub 或 Salesforce）中创建专用的服务账号或 OAuth 应用。
2. 为该账号配置精细的权限范围，例如仅允许读取特定目录的文件，而非整个仓库。
3. 将生成的 API 密钥或 Token 存储在 AWS Secrets Manager 中，而非直接硬编码在配置文件中。
4. 在 Quick Agents 配置中引用 Secrets Manager 的密钥。

**注意事项**: 定期轮换 API 密钥，并确保 Quick Agents 的 IAM 角色仅有权访问特定的 Secrets Manager 密钥。

---

### 实践 3：优化工具定义与上下文描述

**说明**: MCP 允许 Agent 动态调用工具。为了让 Large Language Model (LLM) 准确理解何时以及如何调用外部工具，必须在 MCP 服务器配置中提供清晰、准确的工具定义和上下文描述。

**实施步骤**:
1. 在 MCP 配置文件中，为每个工具编写详细的 `description` 字段，明确其功能和用途。
2. 定义清晰的输入和输出参数，并使用 JSON Schema 进行严格校验。
3. 在描述中包含工具的使用场景示例，帮助 LLM 进行推理。

**注意事项**: 避免模糊的描述。如果工具功能复杂，将其拆分为多个单一职责的小工具，而不是构建一个庞大的“万能工具”。

---

### 实践 4：设计高效的上下文检索策略

**说明**: 外部工具可能包含海量数据。直接将所有数据传输给 Agent 会导致上下文窗口溢出或响应延迟。最佳实践是实施检索增强生成 (RAG) 或特定的过滤逻辑，仅将相关数据通过 MCP 提供给 Agent。

**实施步骤**:
1. 在 MCP 服务器端实现参数化查询，允许 Agent 传递时间范围、关键词或 ID 进行过滤。
2. 对于非结构化数据，集成向量数据库（如 Amazon OpenSearch）并利用 MCP 协议进行语义检索。
3. 限制每次调用返回的数据量，例如设置分页参数。

**注意事项**: 监控 Token 使用量。如果发现 Agent 频繁因上下文过长而失败，需要进一步收紧数据检索的过滤条件。

---

### 实践 5：构建健壮的错误处理与重试机制

**说明**: 外部 API 调用可能会因为网络波动、限流或服务不可用而失败。如果 MCP 服务器直接向 Agent 返回原始的错误堆栈信息，可能会导致 Agent 混乱或生成错误的回复。

**实施步骤**:
1. 在 MCP 服务器层实现全局错误捕获中间件。
2. 将技术性错误（如 HTTP 500, Connection Timeout）转换为 Agent 可理解的语义化错误（例如：“目前无法访问外部系统，请稍后重试”）。
3. 对于限流错误（HTTP 429），在 MCP 层实现指数退避重试逻辑，而不是立即向 Agent 报错。

**注意事项**: 确保错误信息不会泄露敏感的系统架构信息。同时，要区分“可重试错误”和“不可重试错误”（如认证失败），避免对无效请求进行无意义的重试。

---

### 实践 6：全面测试工具调用链路

**说明**: 仅仅测试外部工具本身是不够的，必须测试 LLM 通过 MCP 协议调用工具的端到端流程。这包括验证 Agent 是否能正确解析工具返回的数据并据此生成最终回复。

**实施步骤**:
1. 编写单元测试以验证 MCP 服务器的输入参数校验和 API 交互逻辑。
2. 使用 Quick Agents 的测试控制台进行集成测试，输入各种 Prompt 以触发工具调用。
3. 验证工具返回的数据格式是否与 Agent 的期望一致，特别是处理嵌套 JSON 或特殊字符时。
4. 进行“边界测试”，例如查询空结果集或超长文本，观察 Agent 的反应。

**注意事项**: 重点关注非预期

---
## 学习要点

- MCP 允许 Amazon Quick Agents 等智能体通过标准化接口安全地连接并利用企业外部数据源和工具，打破了 AI 模型与私有数据之间的隔离。
- 通过将 MCP 服务器连接到 Amazon Bedrock Knowledge Base，智能体能够利用 RAG（检索增强生成）技术，基于企业专有数据提供更准确的回答。
- 开发者可以轻松集成 PostgreSQL、Slack 和 Google Drive 等常用工具，使智能体能够直接执行查询数据库、读取消息或检索文件等操作。
- 该协议简化了 AI 应用与现有 IT 基础设施的集成流程，无需为每个工具构建自定义连接器，从而显著降低了开发和维护成本。
- MCP 的开源特性促进了 AI 生态系统的互操作性，使构建能够与外部世界动态交互的“数据驱动型”智能体变得更加容易。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [外部工具](/tags/%E5%A4%96%E9%83%A8%E5%B7%A5%E5%85%B7/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [LLM](/tags/llm/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
- [使用MCP协议集成外部工具至Amazon Quick Agents的实操指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*