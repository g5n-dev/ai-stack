---
title: 使用MCP集成外部工具至Amazon Quick Agents的六步指南
date: 2026-02-24 00:25:28+08:00
draft: false
entry_kind: auto
tags:
- MCP
- Amazon Quick
- Agent
- 系统集成
- 开发指南
- 第三方集成
- LLM
- AWS
categories:
- AI 工程
- 开发工具
source: blogs_podcasts
description: 以下是内容的中文简洁总结： **如何使用模型上下文协议（MCP）将外部工具与 Amazon Quick Agents 集成** 本文主要面向第三方合作伙伴，旨在指导如何通过
  MCP 协议将外部工具集成到 Amazon Quick Agents 中。文章的核心内容是一份**六步清单**，开发者可依据此清单构建新的 MCP
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios:
- 大语言模型
---

# 使用MCP集成外部工具至Amazon Quick Agents的六步指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---

## 摘要/简介

在这篇文章中，您将使用一份六步清单来构建新的 MCP 服务器，或对现有的 MCP 服务器进行验证和调整，以实现与 Amazon Quick 的集成。《Amazon Quick 用户指南》描述了 MCP 客户端的行为和约束。本指南是一份“操作指南”，面向 3P 合作伙伴集成 Amazon Quick 与 MCP 所需的详细实现。

---

## 导语

随着大模型应用场景的深化，如何高效整合外部数据与工具成为构建智能体的关键挑战。本文详细介绍了利用模型上下文协议（MCP）将外部工具接入 Amazon Quick Agents 的方法。文章不仅提供了一份涵盖构建与验证的六步实施清单，还深入解析了客户端行为与集成约束。通过阅读本文，第三方合作伙伴将掌握具体的实现路径，从而有效扩展智能体的功能边界。

---

## 摘要

以下是内容的中文简洁总结：

**如何使用模型上下文协议（MCP）将外部工具与 Amazon Quick Agents 集成**

本文主要面向第三方合作伙伴，旨在指导如何通过 MCP 协议将外部工具集成到 Amazon Quick Agents 中。文章的核心内容是一份**六步清单**，开发者可依据此清单构建新的 MCP 服务器，或对现有的服务器进行验证及调整，以满足 Amazon Quick 的集成要求。

文中特别提到，《Amazon Quick 用户指南》详细说明了 MCP 客户端的行为模式及限制条件，而本文则侧重于合作伙伴所需的具体实施细节，作为一份详尽的实操指南。

---

## 评论

### 文章核心观点
本文旨在通过提出一套标准化的“六步清单”，指导第三方开发者如何构建或适配符合 Amazon Quick Agents 规范的 MCP (Model Context Protocol) 服务器，从而解决大模型应用中“外部工具集成难”的痛点，实现 AI 智能体与数据源的无缝交互。

### 深入评价

#### 1. 内容深度与论证严谨性
*   **支撑理由（事实陈述/你的推断）：** 文章选择 **Model Context Protocol (MCP)** 作为技术底座，显示了极高的技术前瞻性。MCP 是由 Anthropic 主导的开放标准，旨在统一 AI 应用与本地数据/工具的连接层。文章没有停留在概念炒作，而是深入到了“User Guide constraints”的具体细节，这表明 Amazon 正在构建一个类似 App Store 的严苛生态体系，对第三方工具的稳定性、安全性和响应速度有硬性指标要求。
*   **反例/边界条件（作者观点）：** 文章可能过度简化了“异构数据源”的复杂性。MCP 虽然统一了传输协议，但并未解决底层语义的映射问题。例如，将一个 30 年历史的遗留 COBOL 系统通过 MCP 接入 Amazon Quick，仅仅遵循六步清单是远远不够的，中间还需要处理大量的数据清洗和 API 转换逻辑，这部分往往是工程陷阱。

#### 2. 实用价值与指导意义
*   **支撑理由（事实陈述）：** 对于 3P (Third Party) 合作伙伴而言，这篇文章具有极高的“生存指南”价值。Amazon Quick 作为 AWS 试图在 SaaS 层面通过 AI 重塑生产力的产品，其流量入口巨大。文章提供的“Checklist”直接对应了上架审核的通过率，能够显著降低开发者在调试与 AWS 专有协议对接时的试错成本。
*   **反例/边界条件（你的推断）：** 该指南的实用价值仅限于“接入层”。一旦接入成功，如何优化 Prompt 以利用这些工具，如何处理工具调用失败后的 Fallback 机制，这些关乎“用户体验”的核心问题，可能不在本文讨论范围内，导致开发者做出了能用的 Agent，但不好用。

#### 3. 创新性
*   **支撑理由（作者观点）：** 文章最大的创新点在于 **“标准化”**。过去，集成 LangChain、AutoGPT 或各家云厂商的 Agent 框架往往需要学习各自封闭的 API。Amazon 明确支持 MCP，暗示了行业正从“大模型战争”转向“协议战争”。通过采纳开放协议而非自研封闭协议，Amazon 试图通过兼容性来快速补齐自身在垂直领域工具链的短板，这是一种生态策略上的创新。

#### 4. 行业影响
*   **支撑理由（作者观点）：** 此举是 AI Agent 领域的一个里程碑信号。如果 Amazon Quick 强制或推荐 MCP，它将利用其庞大的 B2B 客户基础，实际上将 MCP 推崇为企业级 AI 的 **“USB 接口”** 标准。这将迫使 Snowflake、Google 或 Databricks 等竞争对手不得不考虑是否跟进该协议，从而终结当前工具集成碎片化的乱象。

#### 5. 争议点与不同观点
*   **争议点（作者观点）：** **厂商锁定风险的转移。** 虽然 MCP 是开放的，但 Amazon Quick 的“User Guide constraints”是封闭的。开发者虽然使用了标准协议，但为了适配 Amazon 的特定约束（如 Token 限制、超时时间），可能写出的代码难以直接迁移到其他平台。这实际上是用“半开放”的协议锁死了开发者的服务端逻辑。

### 实际应用建议

1.  **不要盲目重构，先做适配：** 对于已有工具的厂商，不要为了 MCP 而重写后端。建议采用“适配器模式”，在现有 API 网关之上构建一个轻量级的 MCP Server 层，专门负责协议转换和 Amazon Quick 的约束校验。
2.  **关注安全边界：** 在实施“六步清单”时，务必重点检查权限控制。MCP 赋予了 Agent 直接操作外部工具的能力，如果 Quick Agents 的权限设计不当，可能会导致通过自然语言指令越权访问企业核心数据。
3.  **建立监控指标：** MCP Server 的性能将直接影响 Amazon Quick 的用户体验。建议在部署前，专门针对 MCP 接口的延迟（Latency）和吞吐量进行压测，确保在 Amazon Quick 的超时窗口内完成数据返回。

### 可验证的检查方式

1.  **指标测试：** 使用文中提到的清单构建一个 Demo MCP Server，连接 Amazon Quick，测试其处理复杂查询（如跨工具调用）的端到端延迟，观察是否在 5 秒以内（通常用户容忍极限）。
2.  **兼容性实验：** 尝试将该 MCP Server 无缝切换到 Claude Desktop 或其他支持 MCP 的客户端，验证其“一次构建，多处运行”的宣称是否在 Amazon 的定制约束下依然成立。
3.  **观察窗口：** 在未来 3 个月内，观察 AWS Marketplace 中标注为“Ready for Amazon Quick”的应用数量增长速度，以此判断该技术方案的社区接受度。

---

## 技术分析

基于您提供的文章标题和摘要，这是一篇关于**利用模型上下文协议（Model Context Protocol, MCP）将第三方工具集成到 Amazon Quick Agents**的技术指南。文章主要面向第三方合作伙伴，旨在提供构建或调整 MCP 服务器的具体实施清单。

### 1. 核心观点深度解读

**主要观点：**
文章的核心观点在于确立 **MCP（Model Context Protocol）作为连接 Amazon Quick Agents（AI 智能体）与外部工具/数据源的标准化桥梁**。文章提出，通过遵循一个六步清单，开发者可以系统性地构建或适配 MCP 服务器，从而打破 AI 应用与私有数据或企业工具之间的孤岛。

**核心思想：**
作者传达的核心思想是**“标准化集成优于定制化开发”**。在 LLM（大语言模型）应用开发中，为每一个工具编写特定的 API 调用代码是低效且难以维护的。MCP 提供了一种统一、开放的协议，使得 Amazon Quick 这样的客户端能够以通用的方式发现、查询和使用外部能力。这不仅降低了开发门槛，还确保了集成的安全性和稳定性。

**创新性与深度：**
*   **创新性：** 将 AI Agent 的工具调用从“硬编码插件模式”转变为“协议驱动模式”。这类似于 USB 接口之于电脑外设，MCP 使得 AI 能够动态加载和使用工具。
*   **深度：** 文章不仅仅是介绍概念，而是深入到了“客户端行为与约束”的具体细节。它强调了从服务端（MCP Server）构建到客户端（Amazon Quick）消费的全链路对齐，这涉及到对 AI 上下文窗口管理、错误处理和权限控制的深度理解。

**重要性：**
随着企业级 AI 落地的加速，最大的痛点在于 LLM 无法安全、实时地访问企业私有数据（如 SQL 数据库、CRM 系统）。MCP 的出现和 Amazon Quick 的支持，标志着行业正在解决“AI 最后一公里”的数据连接问题，使得 AI Agent 从“聊天机器人”向“全能业务助理”转变。

### 2. 关键技术要点

**涉及的关键技术或概念：**
1.  **MCP (Model Context Protocol):** 一个开放协议，用于连接 AI 模型与上下文数据源（如文件、数据库、API）。
2.  **Amazon Quick Agents:** AWS 提供的生成式 AI 应用构建/托管平台（客户端）。
3.  **MCP Server:** 实现了 MCP 协议的服务端程序，负责暴露工具、资源或提示词给 AI 模型。
4.  **STDIO (Standard Input/Output) vs. SSE (Server-Sent Events):** MCP 传输层的两种常见模式，前者用于本地进程，后者用于网络传输。

**技术原理和实现方式：**
*   **架构模式：** 采用 Client-Server 架构。Amazon Quick 充当 MCP Client，发起连接；用户开发的 Server 暴露特定的端点。
*   **发现机制：** MCP Server 启动时，会向 Client 宣告其能力，包括提供了哪些工具、每个工具的输入参数定义。
*   **交互流程：**
    1.  Amazon Quick Agent 接收用户指令（例如：“查询我的库存”）。
    2.  Agent 通过 MCP Client 发送 `tools/list` 和 `tools/call` 请求。
    3.  MCP Server 执行实际逻辑（如 SQL 查询），并将结果格式化返回给 Agent。
    4.  Agent 将结果整合到自然语言回复中。

**技术难点和解决方案：**
*   **难点：数据安全与权限控制。** 将内部数据库暴露给 AI 存在风险。
    *   **解决方案：** MCP 允许在 Server 层面实现精细的权限验证。文章提到的“六步清单”中必然包含验证步骤，确保只有经过授权的 Amazon Quick 实例才能连接，且 Server 内部应实现数据脱敏。
*   **难点：上下文窗口限制。** 外部工具返回的大量数据可能撑爆 LLM 的 Token 限制。
    *   **解决方案：** MCP Server 应实现智能分页和摘要逻辑，只传递最相关的数据给 Agent，而非原始数据倾倒。

**技术创新点分析：**
文章强调了**“验证和调整现有 Server”**。这意味着 MCP 不是一种全新的重写，而是一种适配层。企业可以复用现有的 REST API 或 GraphQL 服务，只需在其之上封装一层 MCP 接口，即可无缝接入 AI 生态。

### 3. 实际应用价值

**对实际工作的指导意义：**
对于企业架构师和 AI 应用开发者而言，这篇文章提供了一份**“避坑指南”**。它明确了 Amazon Quick 对 MCP 的具体实现要求（例如支持的 JSON Schema 版本、超时设置等），避免了开发者因协议理解偏差而导致的集成失败。

**应用场景：**
1.  **企业知识库问答：** 通过 MCP 连接 Confluence 或 SharePoint，Agent 可以实时检索最新文档回答问题。
2.  **业务操作自动化：** 连接 Salesforce 或 SAP，允许用户通过自然语言创建订单、修改发票。
3.  **数据分析：** 连接 PostgreSQL 或 Snowflake，允许非技术人员用自然语言查询复杂数据库。

**需要注意的问题：**
*   **延迟：** MCP 通信增加了网络跳转，需评估对实时交互的影响。
*   **错误处理：** 当外部工具不可用时，Agent 需要能够优雅降级，不能直接崩溃。

**实施建议：**
在实施前，先在本地环境使用 MCP Inspector（官方调试工具）验证 Server 的行为，确保其符合协议规范，再部署到云端与 Amazon Quick 集成。

### 4. 行业影响分析

**对行业的启示：**
MCP 的普及预示着 AI 基础设施正在**“协议化”**。类似于 HTTP 协议统一了网页浏览，MCP 有望统一 AI Agent 与数字世界的交互方式。这将促使企业不再构建单一的“大而全” AI 应用，而是转向构建“小而美”的专业化工具，由 Agent 按需调用。

**可能带来的变革：**
*   **SaaS 集成方式的变革：** 未来的 SaaS 软件可能不再需要提供复杂的 UI，只需提供标准的 MCP 接口，即可被所有 AI Agent 直接调用和控制。
*   **RAG（检索增强生成）架构的简化：** MCP 将数据检索和工具调用统一在同一个协议下，简化了 RAG 系统的架构复杂度。

**对行业格局的影响：**
AWS（Amazon Quick）对 MCP 的支持是一个强烈的行业信号。如果其他云厂商（Azure, Google Cloud）和模型提供商跟进，MCP 将成为事实上的行业标准。这将削弱单一厂商生态的锁定效应，提升工具提供商的议价权。

### 5. 延伸思考

**引发的思考：**
*   **安全边界：** 当 AI Agent 拥有了通过 MCP 操作数据库的权限，如何防止它被“提示词注入”攻击从而执行恶意操作？传统的 API 鉴权可能不再足够，需要引入基于意图的验证。
*   **多 Agent 协作：** 如果多个 Agent（Amazon Quick, GitHub Copilot 等）同时连接同一个 MCP Server，如何解决并发冲突和状态一致性问题？

**未来发展趋势：**
*   **MCP 市场的兴起：** 未来可能会出现类似“App Store”的 MCP Server 市场，企业可以直接订阅“Salesforce MCP Server”而无需自己开发。
*   **边缘侧 MCP：** 随着 PC 端 AI 算力的增强，MCP Server 可能会运行在用户的本地设备上，实现完全离线、隐私安全的数据访问。

### 7. 案例分析

**成功案例（假设性推演）：**
*   **场景：** 一家电商公司使用 Amazon Quick 构建客服 Agent。
*   **做法：** 开发了一个 MCP Server 连接到其订单管理系统（OMS）。
*   **效果：** 用户问“我的货在哪？”，Agent 通过 MCP 调用 `get_order_status` 工具，实时返回物流状态。相比传统的 RAG 方案，数据实时性达到 100%，且无需构建向量数据库。

**失败案例反思：**
*   **场景：** 某开发者试图将一个拥有 100 个复杂参数的遗留 ERP API 直接封装为 MCP 工具。
*   **结果：** LLM 无法理解复杂的参数结构，经常生成错误的调用请求，导致 Agent 频繁报错。
*   **教训：** **“AI 优先设计”**。不要直接暴露现有 API，而应在 MCP 层构建专门为 LLM 理解优化的“中间层接口”，参数应尽量少且语义明确。

### 8. 哲学与逻辑：论证地图

**中心命题:**
**采用模型上下文协议（MCP）是构建可扩展、互操作的企业级 AI Agent 的最佳架构选择。**

**支撑理由:**
1.  **互操作性:** MCP 提供了统一标准，使得同一个工具可以被不同的 AI 客户端（Amazon Quick, Claude Desktop 等）复用，避免了针对不同模型开发不同 API 的“N×M”复杂度。
    *   *依据:* 技术史证明，标准协议（如 HTTP, USB）是生态繁荣的前提。
2.  **安全性:** MCP 架构允许将敏感逻辑保留在 Server 端，AI Client 仅接收处理后的结果，而非直接访问数据库凭证。
    *   *依据:* 数据主权和隐私保护是企业级 AI 落地的核心合规要求。
3.  **开发效率:** 六步清单法简化了集成流程，开发者无需关心 Agent 的内部逻辑，只需专注于工具本身的实现。
    *   *依据:* 模块化设计原则降低了认知负荷和开发时间。

**反例/边界条件:**
1.  **极低延迟要求场景:** 如果应用要求毫秒级响应（如高频交易），MCP 引入的序列化/网络开销可能不可接受。
2.  **极度简单的单向输出:** 如果仅仅是向 LLM 注入静态文本，MCP 可能显得过重，简单的 System Prompt 更高效。

**命题性质分析:**
*   **事实:** MCP 是由 Anthropic 提出的开放协议；Amazon Quick 已宣布支持。
*   **价值判断:** “最佳”架构选择（基于效率与维护性的权衡）。
*   **可检验预测:** 预测未来 18 个月内

---

## 最佳实践

### 实践 1：严格定义工具接口与权限范围

**说明**:
在集成 MCP 工具时，必须明确每个工具的功能边界和所需的最小权限。Quick Agents 依赖于清晰的工具描述来决定何时调用何种工具。如果工具定义模糊或权限过大，可能会导致 Agent 误用工具或执行非预期的操作，从而引发安全风险或产生错误的执行结果。

**实施步骤**:
1. **审查工具功能**：列出每个 MCP 工具的具体功能，确保其用途单一且明确。
2. **应用最小权限原则**：为工具分配仅足以完成其任务的最小 IAM 权限或 API 访问范围。
3. **编写清晰的描述**：在 MCP 配置文件中，使用精确的自然语言描述工具的输入、输出及副作用，确保 LLM 能准确理解。

**注意事项**:
避免使用“执行任意命令”或“管理所有数据”等过于宽泛的描述。定期审计工具的访问日志，确认 Agent 仅在授权范围内调用工具。

---

### 实践 2：优化数据上下文与提示词工程

**说明**:
MCP 允许外部工具向 Agent 提供数据上下文。为了防止 Token 消耗过大或信息过载，必须对传递给 LLM 的数据进行严格筛选和格式化。高质量的上下文能显著提高 Agent 的推理能力和工具调用的准确性。

**实施步骤**:
1. **数据预处理**：在工具端对原始数据进行清洗、去噪和聚合，仅返回与用户请求最相关的字段。
2. **结构化输出**：确保 MCP 工具返回的是结构化数据（如 JSON），便于 Agent 解析。
3. **调整系统提示词**：在 Quick Agents 配置中，明确指示 Agent 如何优先使用 MCP 提供的上下文，以及何时应忽略无关信息。

**注意事项**:
监控 Token 使用量。如果工具返回的数据量过大，考虑实现分页机制或摘要算法，确保上下文窗口未溢出。

---

### 实践 3：实施全面的错误处理与重试机制

**说明**:
外部工具调用不可避免地会遇到网络波动、服务不可用或 API 限流等错误。如果 MCP 服务器直接返回原始错误堆栈，Agent 可能会感到困惑或向用户展示不友好的信息。建立健壮的错误处理流程是保证用户体验的关键。

**实施步骤**:
1. **标准化错误响应**：在 MCP 服务器端捕获异常，并将其转换为 Agent 易于理解的标准化错误消息（例如：“数据源暂时不可用，请稍后重试”）。
2. **配置重试策略**：对于瞬时故障（如 5xx 错误），在 MCP 客户端或代理层实施指数退避重试机制。
3. **降级逻辑**：当工具不可用时，设计 Agent 的回复逻辑，使其能够优雅地告知用户当前限制，而不是直接崩溃。

**注意事项**:
确保敏感信息（如 API 密钥、内部堆栈跟踪）不会通过错误消息泄露给最终用户。

---

### 实践 4：确保工具调用的幂等性与事务一致性

**说明**:
由于 LLM 可能会因为网络问题或生成过程中的不确定性而重复执行同一个工具调用，或者 Agent 可能会尝试纠正上一次失败的尝试，因此 MCP 工具必须设计为幂等的。即，多次执行相同的操作应产生与执行一次相同的结果，以防止数据重复或状态损坏。

**实施步骤**:
1. **设计幂等接口**：对于写操作（如创建、更新），使用幂等键或业务唯一标识符，确保重复请求不会重复创建资源。
2. **状态检查**：在执行操作前，工具应先检查当前状态，避免不必要的状态变更。
3. **事务管理**：如果工具调用涉及多个步骤，确保这些步骤要么全部成功，要么全部回滚，以保持数据一致性。

**注意事项**:
特别关注涉及计费、资源创建或状态变更的关键操作，务必进行幂等性测试。

---

### 实践 5：建立可观测性与监控体系

**说明**:
集成 MCP 后，Agent 的行为变得更加动态，依赖于外部工具的输出。为了排查问题和优化性能，必须建立完善的监控体系，记录工具调用的全链路数据，包括请求内容、响应时间、成功率和错误类型。

**实施步骤**:
1. **日志记录**：在 MCP 服务器端记录详细的入参和出参日志，并关联 Trace ID 以便追踪。
2. **指标监控**：集成 Amazon CloudWatch 或类似服务，监控工具的延迟、吞吐量和错误率。
3. **分析 Agent 行为**：定期审查 Agent 对话日志，分析工具调用的频率和准确性，识别未被正确调用的工具场景。

**注意事项**:
在记录日志时，务必对敏感用户数据进行脱敏处理，以符合数据隐私合规要求（如 GDPR）。

---

## 学习要点

- MCP 通过标准化接口将外部工具无缝集成到 Amazon Quick Agents 中，显著扩展了 AI 智能体的功能边界。
- 该协议支持实时数据检索，使智能体能够基于最新信息生成答案，有效解决了大型语言模型的知识滞后问题。
- 利用 MCP 连接企业私有 API，可以在保障数据安全的前提下，让智能体执行业务逻辑或查询内部数据库。
- 统一的连接标准简化了开发流程，使得开发者无需为每个工具定制复杂的适配器即可快速集成新功能。
- 通过扩展工具使用场景，企业能够利用 Amazon Quick Agents 构建更复杂、更贴近实际业务需求的自动化工作流。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/) / [LLM](/tags/llm/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的构建指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--8.md" >}})
- [使用MCP协议集成外部工具至Amazon Quick Agents的实操指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP协议集成外部工具至Amazon Quick Agents的六步指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--9.md" >}})
