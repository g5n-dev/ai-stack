---
title: "使用MCP协议集成外部工具至Amazon Quick Agents的六步指南"
date: 2026-02-24T14:10:38+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "Agent", "系统集成", "外部工具", "开发指南", "LLM", "技术实施"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "以下是对该内容的中文总结： 本文旨在指导第三方合作伙伴如何使用**模型上下文协议** 将外部工具集成到 **Amazon Quick Agents** 中。 文章提供了一份**六步清单**，供开发者构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器，以实现与 Amazon Quick 的无缝集成。作为详细的“"
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

在本文中，您将使用一份六步检查清单来构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器，以便实现与 Amazon Quick 的集成。Amazon Quick 用户指南描述了 MCP 客户端的行为和限制。本指南是一份“操作指南”，面向需要通过 MCP 与 Amazon Quick 集成的第三方合作伙伴，涵盖所需的详细实施细节。

---
## 导语

随着 AI 应用场景的深化，如何让大模型模型精准调用外部工具已成为技术落地的关键。本文基于 Model Context Protocol (MCP)，详细拆解了将第三方工具集成至 Amazon Quick Agents 的完整流程。通过这份面向开发者的实操指南，您将掌握构建或调整 MCP 服务器的具体步骤，从而实现数据与能力的无缝对接。

---
## 摘要

以下是对该内容的中文总结：

本文旨在指导第三方合作伙伴如何使用**模型上下文协议** 将外部工具集成到 **Amazon Quick Agents** 中。

文章提供了一份**六步清单**，供开发者构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器，以实现与 Amazon Quick 的无缝集成。作为详细的“操作”指南，它结合了《Amazon Quick 用户指南》中描述的 MCP 客户端行为与限制，为满足集成所需的详细技术实施提供了具体步骤。

---
## 评论

### 评价：基于 MCP 协议集成 Amazon Quick Agents 的技术实践

**中心观点**
该文章实际上是一份**针对第三方开发者的“合规性工程指南”**，其核心在于阐述如何利用 Model Context Protocol (MCP) 将外部工具标准化地接入 Amazon Quick Agents，观点在于**协议适配的严谨性优于功能实现的灵活性**。

**支撑理由与深度评价**

**1. 技术架构的“解耦”与“再耦合”**
*   **事实陈述**：文章重点介绍了 MCP 作为中间层，隔离了 LLM（大语言模型）与外部工具的直接交互。
*   **深度分析**：从技术角度看，这体现了 Agent 架构从“硬编码 Plugin”向“标准化 Protocol”的演进。MCP 类似于 API 网关在微服务中的作用，定义了统一的工具描述、输入输出 Schema。
*   **作者观点（推断）**：Amazon 推广 MCP 不仅仅是为了技术便利，更是为了建立生态护城河。通过 MCP，Amazon 可以在不修改底层模型逻辑的前提下，快速扩展 Agent 的能力边界，同时通过约束 MCP Client 的行为来保证模型调用的安全性（防止 Prompt Injection）。

**2. 开发者体验的标准化**
*   **事实陈述**：文章提供了“六步清单”，涵盖从创建 Server 到验证集成的全过程。
*   **实用价值**：这种清单式的文档对于 B2B 开发极具价值。它降低了认知负荷，使得原本复杂的 Agent 技能接入变成了类似于 CI/CD 流水线般的标准作业。
*   **创新性**：虽然 MCP 本身并非 AWS 独创（源自 Anthropic），但将其系统化地应用到 Quick Agents 这种企业级 SaaS 产品中，并给出具体的约束条件（如 User Guide 中的限制），是一种**工程化落地的创新**。

**3. 企业级集成的安全性与可控性**
*   **事实陈述**：文章强调了“validate and adjust”以及“User Guide constraints”。
*   **深度分析**：这是文章最严谨的部分。在 ToB 场景中，大模型的最大风险是不可控性。通过 MCP Server，企业可以将敏感数据的操作逻辑封装在 Server 端，仅通过 Protocol 暴露元数据给 Agent。这种“数据不离开 Server，指令通过 Protocol”的模式，解决了企业落地 AI 时的核心痛点——数据隐私与合规。

**反例与边界条件**

*   **反例 1：实时性要求极高的场景**
    对于高频交易或毫秒级工业控制，MCP 这种基于文本协议的序列化/反序列化过程可能引入不可接受的延迟。直接调用原生 SDK 或 gRPC 可能更为高效。
*   **反例 2：非结构化数据的复杂处理**
    MCP 擅长处理结构化的工具调用，但如果外部工具涉及极长的非结构化上下文（如处理几百万字的文档检索），MCP 的上下文窗口限制可能会导致信息截断，此时基于 RAG 的直接集成可能比 MCP 工具调用更有效。
*   **边界条件：长尾工具的适配成本**
    对于极其冷门或逻辑极度复杂的遗留系统，强行将其逻辑封装为符合 MCP 标准的 Schema 可能会导致“过度工程化”，甚至为了适配协议而牺牲了原有工具的功能丰富度。

**行业影响与争议点**

*   **行业影响**：这篇文章标志着 AI Agent 生态正在经历“USB 时刻”。正如 USB 统一了外设接口，MCP 有望统一 LLM 与软件工具的连接标准。如果 Amazon Quick Agents、Anthropic、甚至未来的 OpenAI 都采纳 MCP，那么 SaaS 软件的“AI-Ready”程度将成为其核心竞争力。
*   **争议点/不同观点**：
    *   **协议碎片化风险**：虽然 MCP 开源，但巨头们（如 AWS, Google, Microsoft）往往倾向于推广自家的标准。未来可能会出现“MCP vs. Plugins vs. Function Calling”的长期共存与博弈，开发者可能面临“多协议适配”的困境。
    *   **厂商锁定**：虽然 MCP 是开源协议，但 Amazon Quick Agents 的特定 Client 行为约束可能隐含锁定风险。开发者如果完全依赖 AWS 定义的 MCP 扩展，迁移到其他平台时可能仍需修改代码。

**实际应用建议**

1.  **不要盲目重构**：对于简单的 API 调用，现有的 Function Calling 足够用。只有当工具需要被多个 Agent 或多个平台复用时，构建 MCP Server 才有 ROI。
2.  **关注 Schema 设计**：MCP 的核心在于工具描述。投入精力优化 JSON Schema 的定义，能显著提升 LLM 理解工具意图的准确率。
3.  **建立测试沙箱**：利用文章提到的验证步骤，在接入真实业务前，必须在沙箱中模拟 MCP Client 的各种异常输入，确保 Server 的鲁棒性。

**可验证的检查方式**

1.  **集成成功率指标**：
    *   *实验*：统计使用 MCP 接入的工具，在 Agent 调用时的“工具选择错误率”和“参数解析失败率”。
    *   *预期*：相比直接 Prompt 引导，MCP 应能显著降低参数格式错误。

2.  **延迟基准测试**：
    *   *实验*：对比“直接 API 调用”与“通过 MCP Server 调用”的端到端延迟。
    *   *观察窗口*：在网络条件相同的情况下，观察 MCP 协议层引入的额外耗时是否在业务可接受范围内（通常建议 <

---
## 技术分析

基于您提供的文章标题和摘要，虽然无法获取全文的每一个细节，但结合标题《Integrate external tools with Amazon Quick Agents using Model Context Protocol (MCP)》、摘要中的关键信息以及当前AI Agent（智能体）与MCP（Model Context Protocol）的技术背景，以下是对该文章核心观点和技术要点的深入分析。

---

# 深入分析：基于 MCP 协议集成 Amazon Quick Agents 的外部工具扩展

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**通过采用标准化的 Model Context Protocol (MCP)，第三方开发者可以系统性地将外部数据源和工具无缝集成到 Amazon Quick Agents 中，从而突破单一大模型的能力边界，构建具备“手脚”能力的智能体。**

### 作者想要传达的核心思想
作者试图传达一种**“连接主义”**的工程哲学。即未来的 AI 应用不再仅仅依赖于模型参数的大小，而是取决于模型能否高效、安全地调用外部工具。文章强调利用 MCP 这一通用标准，可以消除不同系统之间的“孤岛效应”，使 Amazon Quick Agents 成为一个通用的任务执行入口，而非简单的聊天机器人。

### 观点的创新性和深度
*   **标准化接口的深度应用：** 传统的 Agent 开发往往需要为每个工具编写特定的 API 调用代码，耦合度高。MCP 的引入代表了从“硬编码集成”向“协议级集成”的转变，这是一种架构层面的创新。
*   **双向交互的规范化：** 文章不仅讨论了如何发送请求，还强调了 MCP 客户端的行为约束，这表明作者关注的是**稳定性和可控性**，这在生产环境中至关重要。

### 为什么这个观点重要
随着大模型能力的落地，企业面临的最大痛点是如何让 AI 访问私有的、实时的企业数据。MCP 提供了一个开源、统一的解决方案。如果 Amazon Quick Agents 能够通过 MCP 广泛连接各类 SaaS 工具，它将从一个“玩具”进化为企业级的工作流引擎，这对于推动 AI 在 B 端场景的落地具有里程碑意义。

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Model Context Protocol (MCP)：** 这是一个开放标准（由 Anthropic 主导），用于连接 AI 应用与数据源。它定义了如何查询资源、调用工具和提示模板。
2.  **Amazon Quick Agents：** 亚马逊推出的快速构建 Agent 的平台（可能基于 Bedrock 或相关服务），侧重于低代码/无代码快速部署。
3.  **MCP Server vs. MCP Client：** 在此架构中，Amazon Quick Agents 充当 **Client（客户端）**，而开发者构建的外部工具封装层是 **Server（服务端）**。
4.  **STDIO (Standard Input/Output) 与 SSE (Server-Sent Events)：** MCP 常见的两种传输层通信方式。

### 技术原理和实现方式
文章提到的“六步清单”通常涵盖以下技术实现逻辑：
1.  **环境搭建：** 初始化 Python/Node.js 项目，定义 MCP Server 的配置。
2.  **工具定义：** 使用 JSON Schema 或代码注解，明确外部工具的输入参数和返回结构。例如，定义一个 `query_database` 工具，参数为 `sql_query`。
3.  **资源注册：** 将外部数据（如 API 文档、数据库记录）注册为 MCP 资源，使 Agent 能够“看到”上下文。
4.  **传输层配置：** 决定是通过本地进程通信还是通过 SSE 进行远程网络通信。
5.  **安全与鉴权：** 实现握手协议，确保只有授权的 Agent 才能调用敏感工具。
6.  **部署与测试：** 将 Server 部署到 endpoint，并在 Amazon Quick Agents 控制台进行连接测试。

### 技术难点和解决方案
*   **难点：数据上下文窗口限制。** 外部工具返回的数据可能极其庞大，直接塞给 LLM 会撑爆上下文或导致幻觉。
*   **难点：错误处理的鲁棒性。** 外部 API 可能超时或报错，如果直接传给 LLM 可能会导致 Agent 混乱。
*   **解决方案：** 在 MCP 层实现标准化的错误封装，将技术性错误（如 500 Error）转化为 LLM 能理解的语义化反馈（如“服务暂时不可用，请稍后重试”）。

### 技术创新点分析
最大的创新点在于**解耦**。通过 MCP，外部工具的开发者不需要了解 Amazon Quick Agents 内部如何工作，Quick Agents 也不需要为每个工具编写适配器。这种“即插即用”的模式是 AI 工程化的一大进步。

## 3. 实际应用价值

### 对实际工作的指导意义
对于企业架构师和 AI 工程师而言，这篇文章提供了一份**标准作业程序（SOP）**。它指导如何将现有的企业资产（API、数据库）转化为 AI 可调用的能力，避免了重复造轮子。

### 可以应用到哪些场景
1.  **企业知识库问答：** 通过 MCP 连接 Confluence/Notion/SharePoint，Agent 可以检索最新文档并回答。
2.  **RPA（机器人流程自动化）增强：** Agent 调用 MCP 封装的 Jira/Salesforce API，自动执行创建工单、更新客户状态等操作。
3.  **数据分析：** Agent 通过 MCP 连接 SQL 数据库或 BI 工具，用自然语言生成报表。

### 需要注意的问题
*   **延迟累积：** Agent 思考 + MCP 通信 + 工具执行，整个链路的延迟可能影响用户体验。
*   **权限管控：** 必须在 MCP Server 层严格校验权限，防止 Agent 被诱导执行删除数据等高危操作。

### 实施建议
建议采用**“渐进式集成”**策略。先从低风险的只读接口（如查询天气、查询库存）开始，验证 MCP 的稳定性，再逐步开放写操作（如下单、发邮件）。

## 4. 行业影响分析

### 对行业的启示
这篇文章标志着 AI Agent 领域正在从**“模型之争”**转向**“生态之争”**。谁能掌握更丰富的工具连接生态（如 MCP 或 OpenAI 的 Plugins），谁就能占据流量入口。

### 可能带来的变革
MCP 可能会成为 AI 领域的 **"USB 接口"**。正如 USB 标准统一了外设与电脑的连接，MCP 有望统一 LLM 与企业软件的连接方式。这将催生一大批专门提供“MCP Server”的中间件厂商。

### 相关领域的发展趋势
*   **网关的兴起：** 企业内部会部署统一的 MCP Gateway，用来管理所有对外暴露的 AI 工具接口。
*   **私有化部署增强：** 出于数据安全考虑，大企业更倾向于在本地运行 MCP Server，通过内网与 Agent 平台通信。

## 5. 延伸思考

### 引发的其他思考
*   **多模态数据的传输：** 目前 MCP 主要处理文本，未来如何高效传输图片、视频甚至音频流给 Agent？
*   **Agent 之间的协作：** 如果两个 Agent 都支持 MCP，它们之间能否直接通过 MCP 协议进行 P2P 通信，而无需人类介入？

### 可以拓展的方向
*   **MCP 的安全审计标准：** 随着接入工具增多，如何自动审计 MCP Server 的安全性？
*   **动态工具生成：** MCP Server 能否根据 Agent 的需求，动态生成新的工具？

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有 API：** 审查你目前的项目中有哪些高价值 API。
2.  **开发 Wrapper：** 不要直接暴露原始 API。编写一个中间层，将 API 封装为 MCP 标准格式。
3.  **本地测试：** 使用 Inspector（MCP 的调试工具）在本地测试 Server 的响应是否符合 JSON Schema。

### 具体的行动建议
*   **阅读 MCP 规范：** 理解 `resources`、`prompts`、`tools` 三个核心概念的区别。
*   **动手 Demo：** 尝试用 Python 写一个简单的“时间查询” MCP Server，并接入到 Amazon Quick Agents 或 Claude Desktop 中。

### 需要补充的知识
*   **TypeScript/Python 基础：** MCP SDK 主要基于这两种语言。
*   **JSON Schema：** 用于严格定义工具的输入输出格式。
*   **异步编程模型：** 处理 I/O 密集型工具调用时的并发问题。

## 7. 案例分析

### 结合实际案例说明
**场景：一家电商公司的智能客服 Agent。**

*   **传统方式：** 客户问“我的货到哪了”，客服系统需要硬编码调用物流 API，解析 JSON，然后人工或通过规则回复。
*   **基于 MCP 的方式：**
    1.  开发者构建一个 `Logistics-MCP-Server`，暴露工具 `track_package(order_id)`。
    2.  Amazon Quick Agent 自动发现该工具。
    3.  当用户提问时，Agent 自动判断需要调用 `track_package`。
    4.  MCP Server 返回物流状态。
    5.  Agent 用自然语言总结：“您的包裹已到达北京转运中心”。

### 成功案例分析
**GitHub Copilot Workspace：** 虽然它不完全基于 MCP，但它利用类似的上下文感知能力，将代码库、Issue、CI/CD 状态集成到 AI 编程助手中，极大提升了效率。

### 失败案例反思
如果 MCP Server 定义的工具描述**模糊不清**，例如定义了一个 `do_action(param)` 工具，Agent 会因为不知道 `param` 是什么而频繁报错或产生幻觉。**教训：Schema 设计必须精准且带有丰富的描述性文档。**

## 8. 哲学与逻辑：论证地图

### 中心命题
**采用 Model Context Protocol (MCP) 是实现 Amazon Quick Agents 与外部工具深度、可扩展集成的最优工程路径。**

### 支撑理由与依据
1.  **理由 1：互操作性。** MCP 提供了标准化的接口，消除了异构系统集成的复杂性。
    *   *依据：* 软件工程历史证明，标准化协议（如 HTTP, SQL）是大规模生态形成的前提。
2.  **理由 2：开发效率。** “六步清单”式的方法论显著降低了开发者的认知负荷和开发时间。
    *   *依据：* 摘要中明确提到这是为了“3P partners”（第三方合作伙伴）提供的详细实施指南，暗示其对降低门槛的重视。
3.  **理由 3：上下文感知能力。** MCP 不仅传输数据，还传输资源的上下文，使 Agent 理解力更强。
    *   *依据：* MCP 协议中包含 `resources` 字段，专门用于向模型提供背景信息。

### 反例或边界条件
1.  **反例 1：超低延迟场景。** 在高频交易或毫秒级响应要求的场景中，MCP 这种基于文本协议的封装可能引入不可接受的序列化/反序列化开销。
2.  **边界条件 2：极度复杂的私有协议

---
## 最佳实践

## 最佳实践指南

### 实践 1：确保 MCP 服务器的安全性与访问控制

**说明**：在将外部工具集成到 Amazon Quick Agents 时，MCP 服务器充当了代理与外部数据或 API 之间的桥梁。安全性至关重要，必须防止未授权访问和数据泄露。

**实施步骤**:
1. 为 MCP 服务器实施严格的身份验证机制（例如，使用 API 密钥、OAuth 2.0 或 mTLS）。
2. 在网络层面配置防火墙规则或安全组，仅允许来自特定 IP 范围或 VPC 的连接请求。
3. 定期轮换密钥和凭证，并监控服务器的访问日志以检测异常活动。

**注意事项**: 切勿在代码库或配置文件中硬编码敏感凭证。应使用 AWS Secrets Manager 或类似服务来管理密钥。

---

### 实践 2：优化工具定义与描述的清晰度

**说明**：Amazon Quick Agents 依赖 MCP 协议来理解工具的功能。如果工具定义模糊，模型可能无法正确调用工具。清晰、结构化的元数据能显著提高 Agent 的规划准确性。

**实施步骤**:
1. 在 MCP 配置中，为每个工具提供详细且具体的 `description` 字段，明确说明工具的作用、输入参数及其含义。
2. 定义严格的 JSON Schema 用于输入验证，确保参数类型和限制清晰明了。
3. 为工具参数提供富有上下文的示例，帮助模型理解如何填充参数。

**注意事项**: 避免使用过于宽泛或技术性过强而缺乏上下文的描述。描述应从“用户意图”的角度出发，而不仅仅是“函数功能”的角度。

---

### 实践 3：实施高效的错误处理与响应格式化

**说明**：外部工具调用可能会失败或返回超时。如果直接将原始错误堆栈返回给 Agent，可能会导致混淆。最佳实践是捕获错误并返回结构化、易于理解的反馈。

**实施步骤**:
1. 在 MCP 服务器端实现 try-catch 逻辑，拦截底层 API 错误。
2. 将错误信息转换为自然语言描述或标准化的错误代码（例如，“数据未找到”或“服务暂时不可用”）。
3. 确保成功响应的数据经过清洗，仅返回 Agent 完成任务所需的关键信息，避免过载。

**注意事项**: 确保错误消息中不包含敏感的系统内部信息或追踪 ID，除非用于内部调试，防止信息泄露。

---

### 实践 4：管理工具调用的延迟与超时

**说明**：Amazon Quick Agents 在处理用户请求时通常对延迟敏感。如果 MCP 服务器集成的后端工具响应缓慢，会严重影响用户体验。

**实施步骤**:
1. 为每个 MCP 工具调用设置合理的超时限制（例如 10-30 秒），防止 Agent 无限等待。
2. 对于耗时较长的操作（如生成大型报告），实现异步模式：工具立即返回一个“任务ID”，Agent 随后使用另一个工具查询状态。
3. 监控 MCP 服务器的响应时间，并根据需要优化后端查询或引入缓存层。

**注意事项**: 在设计异步工作流时，必须确保 Agent 能够正确引导用户如何获取最终结果，而不是让用户处于等待状态。

---

### 实践 5：遵循最小权限原则进行工具授权

**说明**：MCP 服务器通常需要代表 Agent 执行操作（如查询数据库或写入文件）。必须限制 MCP 服务器的权限范围，以防止被恶意提示词利用。

**实施步骤**:
1. 为 MCP 服务器创建专用的 IAM 角色或 API 凭证，仅授予完成特定任务所需的最小权限集。
2. 如果工具涉及写操作，实施额外的确认机制或严格的参数白名单。
3. 定期审计 MCP 服务器连接的下游服务的权限设置。

**注意事项**: 避免授予 MCP 服务器通用的 `*` 或 `Admin` 访问权限。特别是在生产环境中，应限制其只能访问特定的表、S3 存储桶前缀或 API 端点。

---

### 实践 6：建立全面的日志记录与可观测性

**说明**：为了调试 Agent 行为和优化工具性能，必须能够追踪从 Agent 到 MCP 服务器再到后端服务的完整调用链路。

**实施步骤**:
1. 在 MCP 服务器中记录每个工具调用的请求体、响应体和延迟时间。
2. 使用 AWS CloudWatch 或类似工具聚合日志，并设置仪表盘监控调用频率和错误率。
3. 在日志中包含关联 ID（Correlation ID），以便将 Agent 的特定对话轮次与后端的 API 调用关联起来。

**注意事项**: 在记录请求和响应体时，要注意合规性，确保对敏感个人数据（PII）进行脱敏处理。

---
## 学习要点

- Amazon Quick Agents 现已支持利用模型上下文协议（MCP）无缝集成外部工具与数据源，从而显著扩展生成式 AI 的应用边界。
- 开发者可以通过标准化配置将企业私有数据（如 SQL 数据库）连接到 Quick Agents，使 AI 能够安全地直接查询和分析内部信息。
- MCP 架构通过将工具定义、提示词和运行时环境解耦，实现了“一次定义，多处运行”的高效开发模式，大幅降低了集成成本。
- 借助 MCP Server，智能体能够动态检索实时数据（例如当前天气或航班状态），有效解决了大语言模型知识滞后的局限性。
- 该协议支持在保持数据本地化和安全合规的前提下，让 AI 应用具备调用复杂业务逻辑和执行实际任务的能力。
- 通过简化外部工具的接入流程，MCP 加速了从原型演示到生产级企业 AI 应用的落地进程。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [系统集成](/tags/%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90/) / [外部工具](/tags/%E5%A4%96%E9%83%A8%E5%B7%A5%E5%85%B7/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [LLM](/tags/llm/) / [技术实施](/tags/%E6%8A%80%E6%9C%AF%E5%AE%9E%E6%96%BD/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [使用MCP集成外部工具至Amazon Quick Agents的构建指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--8.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的六步指南]({{< relref "posts/20260224-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--10.md" >}})
- [使用MCP协议集成外部工具至Amazon Quick Agents的实操指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*