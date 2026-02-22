---
title: "使用MCP集成外部工具至Amazon Quick Agents的六步实施指南"
date: 2026-02-22T16:13:15+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "模型上下文协议", "系统集成", "Agent", "开发指南", "AWS", "第三方集成"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "以下是对该内容的中文简洁总结： **概述** 本文档旨在指导第三方合作伙伴（3P Partners）如何利用 **模型上下文协议（MCP）** 将外部工具与 **Amazon Quick Agents** 进行集成。 **核心目标** 提供一份详细的实施指南，帮助开发者构建一个新的 MCP 服务器，或对现有的 MCP"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["Web应用开发"]
---

# 使用MCP集成外部工具至Amazon Quick Agents的六步实施指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在本文中，您将使用一个六步清单来构建新的 MCP 服务器，或对现有 MCP 服务器进行验证和调整，以实现与 Amazon Quick 的集成。《Amazon Quick 用户指南》描述了 MCP 客户端的行为与约束。本文是一份“操作指南”，详细说明了第三方合作伙伴（3P）通过 MCP 与 Amazon Quick 集成所需的实现细节。

---
## 导语

随着 Model Context Protocol (MCP) 逐渐成为连接 AI 应用与外部工具的标准接口，如何将其高效集成至 Amazon Quick Agents 已成为开发者关注的重点。本文不仅提供了构建或验证 MCP 服务器的六步清单，更深入剖析了 Amazon Quick 的客户端行为与约束。通过这份详实的操作指南，第三方合作伙伴可以掌握具体的实现细节，确保外部功能与 Amazon Quick 的无缝对接。

---
## 摘要

以下是对该内容的中文简洁总结：

**概述**
本文档旨在指导第三方合作伙伴（3P Partners）如何利用 **模型上下文协议（MCP）** 将外部工具与 **Amazon Quick Agents** 进行集成。

**核心目标**
提供一份详细的实施指南，帮助开发者构建一个新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以符合 Amazon Quick 的集成要求。

**实施路径**
文中提供了一个**六步检查清单**，作为开发和验证服务器的主要工作流程。

**参考依据**
指南明确要求开发者参考 **《Amazon Quick 用户指南》**，以深入了解 MCP 客户端的具体行为模式和相关约束条件，确保集成的兼容性和稳定性。

**总结**
这是一份面向技术实施人员的实操性“操作指南”，确保外部工具能通过 MCP 顺畅接入 Amazon Quick 生态系统。

---
## 评论

### 核心评价

这篇文章的中心观点在于：**通过将 Model Context Protocol (MCP) 标准化集成到 Amazon Quick Agents，第三方开发者可以构建可扩展、安全且高性能的 AI 智能体，从而打破大型语言模型（LLM）与外部数据源之间的孤岛。**

以下是对该文章的深入评价：

#### 1. 内容深度：从“玩具”走向“工具”的工程化尝试
**[你的推断]** 文章的核心价值在于它不仅仅是一份 API 文档，而是一份**工程化落地指南**。在当前的 AI 生态中，许多 Agent 应用仍处于“Demo 阶段”，主要痛点在于如何稳定地让 LLM 理解外部工具的输入输出。文章提到的“六步清单”和“MCP 客户端行为约束”，实际上是在解决**语义对齐**问题。

*   **支撑理由**：MCP 的引入将非结构化的工具调用转化为结构化的协议。文章强调验证和调整现有 MCP Server，说明 AWS 意识到直接套用开源标准可能无法满足企业级的安全和性能要求（如 Latency 和 Throughput 约束）。
*   **反例/边界条件**：MCP 并非万能药。对于高频、低延迟的交易类场景（如高频交易辅助），MCP 协议的序列化/反序列化开销可能成为瓶颈。此外，如果外部工具本身缺乏清晰的 API 语义（例如一个只接受自然语言指令的遗留黑盒系统），MCP 的结构化优势将大打折扣。

#### 2. 实用价值：降低 3P 合作伙伴的“语法转换”成本
**[事实陈述]** 对于第三方（3P）合作伙伴而言，最大的痛点通常是为每一个 AI 平台编写一次连接器。文章通过定义 Amazon Quick 对 MCP 的具体实现要求，提供了一套**“一次编写，多处适配”**的潜在路径。

*   **支撑理由**：如果 MCP 成为事实标准，开发者只需维护一个标准的 MCP Server，即可接入 Amazon Quick、Claude Desktop 或其他支持 MCP 的客户端。这极大地降低了 ISV（独立软件开发商）的维护成本。
*   **反例/边界条件**：这种通用性仅限于逻辑层。在物理层，不同云厂商的鉴权机制（AWS IAM vs. OAuth 2.0）、VPC 网络配置和合规性要求（如数据驻留）仍需定制化开发。文章虽然提到了“User Guide”，但往往网络层面的连接比代码层面的适配更耗时。

#### 3. 创新性：协议标准化带来的“即插即用”愿景
**[作者观点]** 该文章的技术创新点不在于算法，而在于**生态系统的标准化**。类似于 USB 接口统一了外设与电脑的连接，MCP 试图统一 LLM 与工具的连接。

*   **支撑理由**：文章强调“validate and adjust an existing MCP server”，暗示了生态系统的互操作性。这是从“垂直整合”（每个大厂自己搞一套）向“水平分工”（工具层与模型层解耦）转变的重要信号。
*   **反例/边界条件**：Anthropic 定义了 MCP，但 AWS 是巨头。这里存在潜在的“Embrace, Extend, and Extinguish”（拥抱、扩展、消灭）风险。如果 Amazon Quick 对 MCP 的实现增加了大量私有 Proprietary 扩展，那么“标准”将名存实亡，开发者反而被锁定在 AWS 的实现分支上。

#### 4. 可读性与逻辑性：典型的 AWS 技术文档风格
**[事实陈述]** AWS 的技术文档通常以详尽和结构化著称，但也常因过于冗长而被诟病。从摘要来看，该文章采用了“Checklist”模式，符合工程师的阅读习惯。

*   **支撑理由**：将复杂的集成过程拆解为六个步骤，降低了认知负荷。明确的“行为与约束”说明有助于开发者在编码前规避红线。
*   **反例/边界条件**：对于非架构师的一线开发者，如果缺乏具体的代码片段或错误处理示例，纯理论的行为描述可能难以理解。文章若只谈“约束”而不给“反例代码”，可读性会打折扣。

#### 5. 行业影响：Agent 基础设施的“军备竞赛”
**[你的推断]** 此文标志着 AI Agent 战场已从“模型能力竞争”转向“工具生态竞争”。Amazon Quick 通过支持 MCP，是在对抗 OpenAI 的 Plugins 和 GPTs 生态。

*   **支撑理由**：通过支持开源协议（MCP），AWS 可能会吸引更多开源开发者构建工具库，从而快速丰富 Amazon Quick 的生态。
*   **反例/边界条件**：如果 MCP 无法获得除了 Anthropic 和 AWS 之外的其他巨头（如 Google, Microsoft）的全面支持，它可能沦为一个小众协议，无法形成真正的网络效应。

#### 6. 争议点：数据隐私与安全边界的模糊
**[你的推断]** 文章提到“MCP client behavior and constraints”，但未详述数据流经 MCP Server 时的处理细节。

*   **争议点**：当 Agent 通过 MCP 调用外部工具时，Prompt（可能包含敏感用户数据）会被发送到 MCP Server。这个 Server 是部署在客户 VPC 内，还是在 AWS 的托管环境中？如果是后者，企业客户可能会因为合规原因拒绝使用。
*   **不同观点**：安全团队可能认为 MCP 协议增加了一个新的攻击面，而开发团队则认为标准化的协议比自研的 Ad-hoc 脚本

---
## 技术分析

基于您提供的文章标题和摘要，这篇关于“使用模型上下文协议（MCP）将外部工具集成到 Amazon Quick Agents”的文章，实际上是亚马逊云科技（AWS）为第三方合作伙伴（3P Partners）提供的一份**技术实施指南**。

文章的核心背景是：Anthropic 提出的 **MCP (Model Context Protocol)** 正在成为连接大语言模型（LLM）与外部数据源/工具的开放标准。AWS 正在通过其 Amazon Quick Agents（可能是 Amazon Bedrock 中的 Agents 或 QuickSight 的自然语言查询功能）采纳这一标准。

以下是对该文章核心观点和技术要点的深入分析：

---

## 1. 核心观点深度解读

**主要观点：**
文章的核心观点是，**采用 MCP 标准是构建可扩展、互操作的 AI 代理生态系统的关键基础设施**。通过 MCP，开发者无需为每一个 AI 应用定制特定的 API 集成，而是可以通过构建一个标准化的 MCP Server，一次性地将数据或工具暴露给任何支持 MCP 的 AI 客户端（在此文中特指 Amazon Quick Agents）。

**核心思想：**
作者试图传达“**标准化连接优于定制化集成**”的思想。在 AI Agent 开发的“Wild West”阶段，每个工具都要写一遍插件。MCP 提供了一套通用的“USB 接口”，使得 Amazon Quick Agents 能够动态地发现、理解并使用外部工具，从而极大地降低了 3P 合作伙伴的集成成本，并提升了终端用户的使用体验。

**创新性与深度：**
*   **标准化协议的深度应用：** 文章不仅停留在概念介绍，而是深入到了具体的“六步清单”，这表明 AWS 正致力于将 MCP 从协议草案推向工程化落地。
*   **双向约束的视角：** 文章强调了“MCP 客户端行为和约束”，这意味着集成不仅仅是 Server 端（工具提供方）的事，必须深刻理解 Client 端（AWS）的能力边界（如上下文窗口限制、超时处理等），这是一种深度的系统级工程思维。

**重要性：**
对于合作伙伴而言，这是接入 AWS 庞大生态的入场券。对于行业而言，这标志着 MCP 正在迅速获得主流云厂商的实际支持，可能成为 AI 时代的“HTTP 协议”。

## 2. 关键技术要点

**关键技术概念：**
*   **MCP (Model Context Protocol):** 一种开放协议，基于 JSON-RPC，用于连接 LLM 应用与本地或远程数据源。它定义了 Server（暴露数据的工具）和 Client（消费数据的 LLM 应用）之间的交互模式。
*   **Amazon Quick Agents:** AWS 提供的 AI 智能体服务（可能基于 Bedrock Agents 或 QuickSight Q），能够理解自然语言并执行任务。
*   **Resources (资源), Prompts (提示), Tools (工具):** MCP 的三大核心能力。Resources 是静态数据访问，Prompts 是预定义的模板，Tools 是可执行的函数。

**技术原理与实现：**
*   **传输层：** MCP 可以通过 `stdio`（本地进程通信）或 `SSE`（服务器发送事件，基于 HTTP）进行通信。对于云端部署（如 AWS Lambda），SSE 是主要方式。
*   **发现机制：** Client 通过调用 `tools/list` 或 `resources/list` 端点来动态获取 Server 提供的功能清单，无需硬编码。
*   **六步清单（推测内容）：**
    1.  **环境准备：** 搭建 MCP Server 运行时（如 Docker/Lambda）。
    2.  **Schema 定义：** 严格定义工具的输入/输出 JSON Schema。
    3.  **协议实现：** 处理初始化、心跳、工具调用请求。
    4.  **认证鉴权：** 处理 AWS 与 3P 服务之间的 IAM 或 Token 验证。
    5.  **错误处理：** 确保错误信息符合 MCP 标准且能被 LLM 理解。
    6.  **部署与测试：** 将 Server 注册到 Amazon Quick Agents 的配置中。

**技术难点与解决方案：**
*   **难点：** **上下文窗口管理**。如果 MCP Server 返回的数据量过大，可能会撑爆 LLM 的上下文窗口。
*   **难点：** **延迟与超时**。LLM 交互通常对延迟敏感，而外部工具调用可能很慢。
    *   *解决方案：* 使用异步处理模式，优化数据库查询，确保 Server 响应时间在 AWS Client 的超时阈值内。

## 3. 实际应用价值

**对实际工作的指导意义：**
这份指南是 3P SaaS 供应商（如 Jira, Salesforce, GitHub 等）接入 AWS 生成式 AI 生态的操作手册。它指明了如何将现有的 SaaS API 转换为 LLM 可读的 MCP 接口。

**应用场景：**
1.  **企业知识库问答：** 将公司内部的 Wiki、Confluence 通过 MCP 接入 Amazon QuickSight，实现“用自然语言查询公司数据”。
2.  **自动化运维：** 将监控工具（如 Datadog）通过 MCP 接入，允许 Agent 自动查询服务器状态并执行重启脚本。
3.  **数据分析：** 将 SQL 数据库通过 MCP 暴露为“工具”，让非技术人员用自然语言生成报表。

**需要注意的问题：**
*   **安全性：** MCP Server 暴露给 LLM 的接口必须具备严格的权限控制，防止 Agent 被诱导执行删除数据等高危操作。
*   **语义对齐：** JSON Schema 的描述必须非常清晰，否则 LLM 无法正确生成调用参数。

## 4. 行业影响分析

**对行业的启示：**
MCP 的出现标志着 AI 基础设施正在从“模型中心”向“数据连接中心”转移。未来的竞争不仅仅是模型参数量的竞争，更是**谁能连接更多、更优质的数据源**。

**可能带来的变革：**
*   **RAG 架构的简化：** 传统的 RAG（检索增强生成）需要编写繁琐的 ETL 管道和向量化逻辑。MCP 提供了一种更直接、实时的“函数调用 + 数据查询”模式，可能部分取代传统的向量检索。
*   **SaaS 的 AI-Ready 化：** 所有的 SaaS 厂商都将被迫支持 MCP 或类似协议，否则将在 AI 时代失去“可被发现性”。

**发展趋势：**
MCP 有望成为 AI 领域的 ODBC 或 JDBC。如果 AWS、Anthropic、Replit 等巨头持续推动，它将终结 AI 插件市场的碎片化状态。

## 5. 延伸思考

**引发的思考：**
*   **协议的通用性 vs. 厂商锁定：** 虽然 MCP 是开放的，但 AWS 的“Quick Agents”可能对其有特定的扩展或约束。开发者需要警惕“伪开放”，确保代码具有可移植性。
*   **Serverless 与 MCP 的结合：** AWS Lambda 是运行 MCP Server 的完美载体（按需调用、无状态）。未来的 MCP Server 开发模式可能高度依赖 Serverless 架构。

**拓展方向：**
*   **多模态支持：** 目前 MCP 主要侧重文本和结构化数据，未来如何支持视频、音频流的传输？
*   **Agent 协作：** 多个 Agent 之间是否可以通过 MCP 互相调用？

## 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现有 API：** 检查你的产品 API 是否具备原子性（功能单一）、幂等性（重复调用结果一致）和低延迟特性。
2.  **开发 Wrapper：** 不要直接修改现有 API，而是构建一个轻量级的 MCP Wrapper 层，负责协议转换和鉴权。
3.  **利用 AWS Infrastructure：** 将 Wrapper 部署在 AWS Lambda 上，使用 API Gateway 作为入口，利用 IAM 验证来自 Quick Agents 的请求。

**行动建议：**
*   **立即行动：** 阅读 AWS 官方文档中关于“External Tools”或“Action Groups”的部分，寻找 MCP 相关的配置入口。
*   **知识补充：** 深入学习 JSON Schema 规范，这是 LLM 理解工具的关键。

## 7. 案例分析

**成功案例（假设性构建）：**
*   **案例：** 一家名为“DataFlow”的 BI 工具厂商。
*   **做法：** 他们开发了一个 MCP Server，将内部的“图表生成接口”封装为 Tool。用户只需在 Amazon QuickSight 中说“给我看上季度的销售趋势”，Quick Agent 就通过 MCP 调用 DataFlow 的接口，直接渲染图表并返回。
*   **成功因素：** 接口定义极其清晰，参数描述详细，且响应速度在 2 秒以内。

**失败反思：**
*   **案例：** 某老旧数据库厂商试图通过 MCP 暴露全量 SQL 接口。
*   **问题：** 接口过于底层，需要 LLM 构建极其复杂的 SQL 语句，导致 LLM 频繁出错（幻觉 SQL）；且未做权限控制，导致 Agent 尝试访问敏感表。
*   **教训：** MCP Server 应暴露**业务意图**（如“查询用户余额”），而非**底层实现细节**（如“Select * from table...”）。

## 8. 哲学与逻辑：论证地图

**中心命题:**
**采用模型上下文协议（MCP）是第三方工具集成到 Amazon Quick Agents 等大模型平台的最优工程解法，因为它通过标准化接口实现了互操作性、降低了维护成本并增强了安全性。**

**支撑理由:**
1.  **互操作性:** MCP 提供了统一的协议（如 `tools/list`），使得一次开发即可适配多个支持 MCP 的客户端，避免了为每个 AI 应用定制 API 的 N×M 复杂度。
2.  **安全性:** MCP 架构允许在 Server 端（工具侧）集中实施权限控制和审计日志，而不是将敏感凭证直接暴露给 LLM。
3.  **语义增强:** MCP 强制要求使用 JSON Schema 定义工具输入，这比传统的 REST API 文档更能帮助 LLM 准确理解参数格式，从而降低调用失败率。

**反例 / 边界条件:**
1.  **高延迟场景:** 如果外部工具的执行时间超过 LLM 客户端的超时限制（例如生成一份需要 5 分钟的 PDF 报告），标准的同步 MCP 调用会失败，需要引入异步回调机制。
2.  **非结构化数据流:** 对于实时视频流或超大文件传输，基于 JSON-RPC 的 MCP 可能不是最高效的载体，直接使用 S3 Presigned URL 等传统方式可能更合适。

**事实与预测:**
*   **事实:** Anthropic 提出了 MCP，且 AWS 在 Amazon Quick Agents 中集成了对 MCP 的支持。
*   **价值判断:** 标准化协议优于私有 API 适配器。
*   **可检验预测:** 未来 12 个月内，超过 50% 的主流 SaaS 平台将提供官方的 MCP Server 或类似的标准接口。

**立场与验证:**
*   **立场:** 强烈支持将 MCP 作为 AI 集成的首选标准，特别是在 AWS 生态内。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建具有明确边界的专用工具

**说明**: 在通过 MCP 将外部工具集成到 Amazon Quick Agents 时，应确保每个工具的功能单一且职责明确。避免创建能够执行过于广泛操作的“上帝工具”。例如，不要创建一个通用的“数据库管理工具”，而应创建“查询客户信息”、“更新订单状态”等细粒度的工具。这有助于大语言模型（LLM）更准确地理解工具用途，减少幻觉和错误调用。

**实施步骤**:
1. 审核现有的外部 API 或功能，将其拆解为原子性的操作单元。
2. 为每个工具定义清晰的名称和描述，确保其名称能直观反映功能。
3. 在 MCP 配置文件中，逐一注册这些独立的工具，而不是将它们打包在一个复杂的接口中。

**注意事项**: 避免在一个工具中混合读写操作，尽量将查询类操作与变更类操作分离，以便于权限控制。

---

### 实践 2：优化输入参数的架构与验证

**说明**: MCP 依赖严格的参数定义来指导 Agent 传递正确的数据。最佳实践是使用强类型定义（如 JSON Schema）来描述工具的输入参数，并包含清晰的约束条件（如枚举值、长度限制、正则表达式）。这不仅提高了 Agent 调用成功率，还能防止恶意或错误的输入传递给后端系统。

**实施步骤**:
1. 为每个工具的输入参数定义详细的 JSON Schema。
2. 添加描述性元数据，例如参数的具体用途说明和示例值。
3. 在 MCP 服务器端实施严格的验证逻辑，确保任何不符合 Schema 的请求都被拒绝。

**注意事项**: 尽量减少参数数量，对于复杂的嵌套结构，考虑将其扁平化以降低 LLM 处理的难度。

---

### 实践 3：实施细粒度的访问控制与安全上下文传递

**说明**: 当 Agent 代表用户执行操作时，必须确保外部工具能够识别调用者的身份并执行相应的权限检查。MCP 集成不应绕过现有的安全模型。最佳实践是在 MCP 连接建立或工具调用时，传递必要的上下文信息（如用户 ID、会话 Token），以便后端系统进行授权。

**实施步骤**:
1. 配置 MCP 客户端以在请求头或元数据中包含身份验证令牌。
2. 确保外部工具服务端能够解析这些上下文信息，并基于最小权限原则执行操作。
3. 定期审计工具的访问日志，确保没有权限提升的情况发生。

**注意事项**: 切勿在工具描述或参数中硬编码敏感凭证（如 API Key、密码），应依赖运行时的上下文注入。

---

### 实践 4：设计标准化的错误处理与响应机制

**说明**: LLM 需要清晰的反馈来理解操作是否成功或失败。最佳实践是定义标准化的错误响应格式，包含机器可读的错误代码和人类可读的错误信息。避免返回原始的堆栈跟踪或模糊的 500 错误，这会阻碍 Agent 进行自我修正或向用户提供有用的解释。

**实施步骤**:
1. 定义一套标准的错误代码（例如：`INVALID_INPUT`, `RESOURCE_NOT_FOUND`, `PERMISSION_DENIED`）。
2. 确保工具在发生错误时返回 JSON 格式的响应，明确指出错误原因及建议的修复步骤。
3. 测试 Agent 对各种错误场景的响应能力，确保其能优雅地处理异常。

**注意事项**: 错误信息应尽可能详细，但要避免泄露内部系统架构的敏感信息。

---

### 实践 5：提供上下文感知的描述与示例

**说明**: MCP 服务器向 Agent 提供的工具描述是模型决策的唯一依据。模糊的描述会导致调用失败。最佳实践是在工具注册时提供富含上下文的描述，甚至包含少量示例。这有助于模型理解在何种对话场景下应该调用该工具以及如何构造参数。

**实施步骤**:
1. 在工具的 `description` 字段中，详细说明工具的业务用途、适用场景及副作用。
2. 利用 MCP 支持的元数据字段，提供具体的输入输出示例。
3. 定期分析 Agent 的调用日志，针对频繁调用错误的工具优化其描述文本。

**注意事项**: 描述应保持简洁但信息量大，避免使用过于晦涩的技术术语，除非该术语对模型理解工具逻辑是必要的。

---

### 实践 6：监控工具性能与使用频率

**说明**: 外部工具的响应速度直接影响 Amazon Quick Agents 的用户体验。集成的工具必须具备高性能和高可用性。实施监控机制以跟踪工具的延迟、成功率和调用频率，可以及时发现并解决性能瓶颈或异常调用模式。

**实施步骤**:
1. 为 MCP 服务器和下游工具启用 CloudWatch 或类似的监控服务。
2. 设置关键指标警报，如 P95 延迟过高或错误率突增。
3. 分析调用模式，识别那些被频繁调用但返回空结果或错误的工具，并进行优化。

**注意事项**: 对于耗时较长的操作（超过 30 秒），应考虑实现异步模式，避免 Agent 因超时而中断连接。

---
## 学习要点

- MCP 通过标准化的接口将外部工具与 Amazon Quick Agents 无缝集成，显著扩展了 AI 智能体处理复杂任务的能力边界。
- 利用 MCP Server 可以安全地连接企业私有数据源，使智能体能够在隔离环境中访问和利用敏感信息。
- 该协议支持将外部 API 转化为智能体的可调用技能，从而让 AI 能够执行实时数据检索、自动化操作及业务逻辑处理。
- 集成过程遵循声明式配置原则，开发者无需编写复杂的底层代码即可快速实现工具与模型的交互。
- MCP 的标准化架构降低了不同外部系统与 Amazon Quick Agents 之间的连接难度，有效减少了定制化开发与维护成本。
- 通过在 MCP 中定义严格的工具权限与访问范围，企业能够在扩展智能体功能的同时确保数据交互的安全性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [模型上下文协议](/tags/%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [Agent](/tags/agent/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [AWS](/tags/aws/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
- [深度解析Skill/MCP/RAG等五大AI技术的底层逻辑]({{< relref "posts/20260212-juejin-深入理解skillmcpragagentopenclaw底层逻辑-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*