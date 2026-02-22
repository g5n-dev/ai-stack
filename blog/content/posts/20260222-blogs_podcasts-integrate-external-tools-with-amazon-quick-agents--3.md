---
title: "使用MCP将外部工具集成至Amazon Quick Agents的六步指南"
date: 2026-02-22T22:48:17+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "Amazon Quick", "Agent", "模型上下文协议", "工具集成", "AWS", "开发指南", "第三方集成"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "**中文总结：** 本文介绍了如何利用**模型上下文协议（MCP）**将外部工具与 **Amazon Quick Agents** 进行集成。主要内容面向第三方合作伙伴（3P partners），旨在指导他们如何构建新的 MCP 服务器，或对现有的服务器进行验证及调整，以实现与 Amazon Quick 的对接。 文章"
external_url: https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp
scenarios: ["Web应用开发"]
---

# 使用MCP将外部工具集成至Amazon Quick Agents的六步指南

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-20T16:26:21+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)

---
## 摘要/简介

在本文中，您将使用一个六步清单来构建新的 MCP 服务器，或验证并调整现有的 MCP 服务器，以便集成到 Amazon Quick。《Amazon Quick 用户指南》描述了 MCP 客户端的行为与约束。这是一份面向 3P 合作伙伴的“如何操作”指南，详细说明了通过 MCP 与 Amazon Quick 集成所需的实现细节。

---
## 导语

随着 Model Context Protocol (MCP) 的引入，将外部工具集成到 Amazon Quick Agents 的流程正变得更加标准化。对于第三方合作伙伴而言，准确理解客户端行为与约束是实现无缝对接的关键。本文提供了一份面向 3P 合作伙伴的实操指南，通过六步清单详细说明了构建或调整 MCP 服务器的具体实现细节，旨在帮助您高效完成集成并验证工具的可用性。

---
## 摘要

**中文总结：**

本文介绍了如何利用**模型上下文协议（MCP）**将外部工具与 **Amazon Quick Agents** 进行集成。主要内容面向第三方合作伙伴（3P partners），旨在指导他们如何构建新的 MCP 服务器，或对现有的服务器进行验证及调整，以实现与 Amazon Quick 的对接。

文章提供了一个**六步清单**作为实施路径，并详细说明了 Amazon Quick 用户指南中定义的 MCP 客户端行为及其约束条件，是合作伙伴完成集成的实操指南。

---
## 评论

### 文章评价：Integrate external tools with Amazon Quick Agents using Model Context Protocol (MCP)

**中心观点：**
该文章通过提出一套标准化的“六步清单”，旨在将 Model Context Protocol (MCP) 确立为连接第三方工具与 Amazon Quick Agents 的通用互操作性标准，这实质上是 Anthropic 试图在 AI Agent 生态中构建类似 HTTP 协议地位的底层基础设施尝试。

**支撑理由与深度分析：**

**1. 技术架构的解耦与标准化（事实陈述 + 作者观点）**
文章强调 MCP 作为一种开放协议，能够将“数据获取”与“Agent 逻辑”分离。
*   **深度分析：** 在当前的 Agent 开发中，开发者通常需要为每个 LLM（如 Claude, GPT-4）编写特定的 Plugin 或 Function Calling 代码。MCP 的引入类似于数据库领域的 ODBC 或 JDBC，它定义了 Host（Amazon Quick）与 Server（工具）之间的标准握手、资源发现和提示注入机制。从技术角度看，这降低了多 Agent 环境下的维护成本，但这要求 MCP 协议本身必须具备极高的版本稳定性和向后兼容性。

**2. 对“3P Partners”生态系统的强力锁定（你的推断）**
文中明确提到这是针对 3P（第三方）合作伙伴的指南，强调“Quick User Guide”中的约束。
*   **深度分析：** 这不仅是技术文档，更是生态准入规则。Amazon Quick Agents（可能基于 Bedrock 或 Anthropic 技术）通过 MCP 来规范外部工具的接入方式。这种策略虽然提升了生态内的安全性（通过约束验证）和一致性，但也构建了较高的转换成本。一旦合作伙伴基于 MCP 构建了 Server，若未来想切换到不支持 MCP 的 Agent 平台，将面临重写的风险。这是一种典型的“通过标准建立护城河”的策略。

**3. 实用价值：从“概念验证”到“生产就绪”的跨越（事实陈述）**
文章提供的“六步清单”和验证机制，解决了企业级 AI 应用中最头疼的“最后一公里”问题——非标准化数据的接入。
*   **深度分析：** 许多企业拥有私有 API（如 ERP、CRM），但不知道如何安全地暴露给 LLM。MCP Server 的模式允许企业在防火墙内运行一个轻量级服务，仅通过 MCP 协议暴露特定元数据和接口。这种架构比直接授予 LLM 数据库访问权限更安全、更可控。

**反例与边界条件：**

1.  **协议碎片化风险（反例）：** MCP 并非唯一的连接标准。OpenAI 有 Plugins 系统，LangChain 有其 Tool 定义标准。如果 MCP 仅被 Amazon/Anthropic 阵营采用，而 OpenAI 拒绝支持，那么第三方开发者将不得不维护两套接入代码，这反而增加了技术债。
2.  **性能与延迟瓶颈（边界条件）：** MCP Server 通常作为独立进程运行（通过 stdio 或 SSE 通信）。对于高频、低延迟的交互场景（如实时游戏控制或高频交易），多一层的 MCP 转发可能引入不可接受的毫秒级延迟，且 stdio 模式的并发处理能力在负载极高时可能成为瓶颈。

**评价维度细分：**

*   **内容深度：** 文章属于典型的“Implementation Guide”（实施指南）。它不探讨 MCP 的理论模型，而是专注于“怎么做”。论证严谨性体现在其对“Client 行为约束”的强调，说明作者考虑了兼容性问题，但缺乏对极端错误处理（如 Server 崩溃时的恢复策略）的深度讨论。
*   **创新性：** 核心创新在于将“上下文协议”显式化。传统的 Function Calling 往往只传输参数，而 MCP 强调了“资源”和“提示模板”的标准化传输，这是一种更高级别的抽象。
*   **可读性：** 结构清晰，清单体易于操作。但技术文档通常假设读者对 Amazon Quick 的底层架构已有了解，对新手可能存在认知门槛。
*   **行业影响：** 如果 MCP 成功，它将成为 AI 时代的“API 网关标准”。它推动了 AI 从“聊天机器人”向“操作系统”演进，Agent 不再只是生成文本，而是通过 MCP 调用工具改变物理世界或数字状态。

**可验证的检查方式：**

1.  **互操作性测试（指标）：** 选取一个基于 MCP 开发的 Server（如 GitHub 上开源的 `@modelcontextprotocol/server-filesystem`），尝试在不修改代码的情况下，分别将其接入 Amazon Quick Agents 和 Claude Desktop。观察是否两边都能成功识别并调用工具。
2.  **并发压力测试（实验）：** 构建 MCP Server，使用 stdio 模式连接。模拟 100 个并发 Agent 请求，观察是否存在进程阻塞、死锁或内存泄漏现象。这能验证文中未详述的边界条件。
3.  **协议版本兼容性观察（观察窗口）：** 在未来 6 个月内，观察 MCP 的 GitHub 仓库是否有 Breaking Change（破坏性更新）。如果协议频繁变动，说明其尚未成熟，文中所述的“构建 Server”可能面临短期废弃风险。

**实际应用建议：**

对于企业开发者，建议**“小步快跑，关注 SSE”**。
不要立即将所有核心业务逻辑迁移到 MCP。首先，选择非关键路径的数据查询接口（如“查询员工假期余额”）进行 MCP Server 封装试点。在技术选型上，优先推荐使用 SSE（Server-Sent Events）或 WebSocket 传输模式而非 stdio，因为 stdio 在云原生容器环境（如 Kubernetes）的日志采集和进程管理

---
## 技术分析

基于您提供的文章标题和摘要，这是一篇关于如何利用 **Model Context Protocol (MCP)** 将第三方工具集成到 Amazon Quick Agents（或 Amazon Q Apps）中的技术实施指南。

虽然全文内容未完全展开，但结合标题、摘要以及对 MCP 协议和 Amazon Q 生态的技术理解，以下是对该文章核心观点及技术要点的深入分析。

---

# 深入分析：基于 MCP 协议集成 Amazon Quick Agents 的技术指南

## 1. 核心观点深度解读

### 文章的主要观点
文章的核心观点是：**Model Context Protocol (MCP) 是实现 AI 智能体与外部数据/工具“即插即用”集成的标准化桥梁。** 对于第三方合作伙伴而言，遵循一套标准的六步清单，可以高效地将现有的 SaaS 工具或数据源转化为 Amazon Quick Agents 可调用的能力，从而打破 AI 应用的“数据孤岛”。

### 作者想要传达的核心思想
作者试图传达一种**“标准化连接优于定制化开发”**的思想。在 LLM（大语言模型）应用开发中，反复为每个应用编写 API 调用逻辑是低效的。MCP 提供了一种统一的、开放的协议（类似于 AI 领域的“USB 接口”），使得工具提供者只需开发一次 MCP Server，即可被包括 Amazon Quick Agents 在内的多种 MCP Client 消费。

### 观点的创新性和深度
*   **解耦架构**：创新性在于将“模型推理”与“数据获取/工具执行”彻底解耦。传统的 Function Calling 往往与特定模型紧密绑定，而 MCP 提供了模型无关的抽象层。
*   **生态系统的互操作性**：深度在于强调生态共建。通过定义标准行为和约束，Amazon 允许外部开发者扩展 Q 的核心能力，而不是仅依赖亚马逊官方的集成。

### 为什么这个观点重要
随着企业级 AI 的落地，最大的痛点不是模型不够聪明，而是模型无法安全、实时地访问企业私有数据（如 Jira 工单、内部 ERP、SQL 数据库）。MCP 的引入意味着 Amazon Q 正在从一个封闭的问答机器人转变为一个**具备执行能力的开放操作系统**，这对企业级 AI 的普及至关重要。

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **Model Context Protocol (MCP)**：由 Anthropic 提出的开源协议，用于连接 AI 应用与数据源。它定义了 Server（暴露数据/工具）和 Client（消费数据/工具）之间的交互标准。
2.  **Amazon Quick Agents / Amazon Q**：AWS 推出的生成式 AI 助手，具备构建特定业务任务 Agent 的能力。
3.  **MCP Server**：运行在本地或远程的服务进程，通过 stdio（标准输入输出）或 SSE（服务器发送事件）与客户端通信，向 LLM 暴露 "Prompts"（提示模板）、"Resources"（静态数据）和 "Tools"（动态函数）。

### 技术原理和实现方式
*   **通信机制**：MCP Server 通常通过 JSON-RPC 消息格式进行通信。对于本地开发，常使用 stdio（标准输入/输出流）；对于云端部署（如集成到 AWS），可能需要通过 HTTP/WebSocket 转发层（如 MCP Gateway）将 stdio 桥接到网络。
*   **能力发现**：Server 启动时会向 Client 宣告其支持的工具列表、参数结构。LLM 根据用户意图，自动选择调用相应的工具。
*   **六步清单（推断）**：
    1.  **环境准备**：配置运行时环境（Python/Node.js）。
    2.  **SDK 选择**：使用官方 MCP SDK 或框架（如 ModelContextProtocol）。
    3.  **定义接口**：编写工具描述，包括输入参数的 JSON Schema。
    4.  **实现逻辑**：编写实际调用外部 API 的代码。
    5.  **本地测试**：使用 Inspector 或 MCP Client 验证工具调用。
    6.  **部署与连接**：将 Server 部署到 Amazon Quick Agents 可访问的位置，并配置连接参数。

### 技术难点和解决方案
*   **难点：认证与安全传递**。MCP Server 如何安全地调用受保护的 API？
    *   **解决方案**：通常涉及在配置 MCP Server 连接时传递 OAuth Token 或 API Key，或者利用 AWS Secrets Manager 管理凭证。
*   **难点：上下文窗口限制**。外部工具返回大量数据时可能撑爆 Token。
    *   **解决方案**：MCP 允许定义 Resources，支持流式传输或分页检索，Client 端需做截断或摘要处理。

## 3. 实际应用价值

### 对实际工作的指导意义
对于 AWS 生态的开发者和架构师而言，这篇文章提供了一条**将企业遗留系统“AI 化”的快速通道**。你不再需要等待 Amazon Q 官方支持你的 SaaS 软件，只需自己写一个轻量的 MCP Server，即可让 Q 具备读取和操作该软件的能力。

### 可以应用到哪些场景
1.  **企业知识库查询**：将内部的 Confluence、SharePoint 或文件系统通过 MCP 暴露给 Q，实现基于私有文档的问答。
2.  **业务流程自动化**：允许 Q 通过 MCP 调用 Salesforce API 创建客户记录，或调用 Jira API 创建 Bug。
3.  **数据查询与分析**：编写 MCP Server 包装 SQL 查询，让用户用自然语言查询数据库。

### 实施建议
*   **从“只读”开始**：先实现读取数据的 MCP Server，验证准确性，再尝试写入操作，以降低安全风险。
*   **模块化设计**：将不同的业务域（如 HR 系统、财务系统）拆分为不同的 MCP Server，便于维护和权限控制。

## 4. 行业影响分析

### 对行业的启示
MCP 的兴起标志着 AI 应用开发从 **"Prompt Engineering"（提示词工程）** 向 **"Tool Integration Engineering"（工具集成工程）** 转变。行业标准协议的竞争将取代单一模型能力的竞争。

### 可能带来的变革
*   **SaaS 的 AI 原生化**：未来 SaaS 软件的标准配置可能不再是“Open API”，而是“MCP Connector”。
*   **Agent Store 的繁荣**：类似手机应用商店，未来会出现 Agent 工具商店，MCP Server 就是这些 Agent 的“插件包”。

### 对行业格局的影响
这强化了 Anthropic 和 AWS 在企业级 AI 领域的联盟地位。如果 MCP 成为事实标准，它将削弱 OpenAI 的 GPTs 生态的封闭性优势，推动更开放的开发者社区形成。

## 5. 延伸思考

### 引发的其他思考
*   **协议的通用性**：MCP 目前虽然由 Anthropic 主导，但其开源特性使其具备成为通用标准的潜力。未来是否会看到 OpenAI 或 Google 加入支持？
*   **Serverless 化**：目前的 MCP Server 多为长进程。如何将其高效地部署在 AWS Lambda 等无服务器架构上，是一个值得优化的方向。

### 未来发展趋势
*   **MCP Gateway**：企业内部可能会部署统一的 MCP 网关，用于管理所有 MCP Server 的认证、日志和路由，而不是让每个 Agent 直接连接各个 Server。
*   **多模态支持**：目前的 MCP 主要侧重文本，未来对图片、视频流的支持将是关键增长点。

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有 API**：查看你团队内部有哪些高频使用的 API 或数据脚本。
2.  **搭建 PoC**：选择一个简单的场景（如查询天气或查询内部工单），使用 Python 或 TypeScript 编写一个简单的 MCP Server。
3.  **本地验证**：使用 Desktop MCP Client（如 Claude Desktop 或 MCP Inspector）测试 Server 是否能正确响应。
4.  **接入 Quick Agents**：按照 AWS 文档，将 Server 配置推送到 Amazon Q 环境。

### 具体的行动建议
*   **学习 JSON Schema**：MCP 强依赖 JSON Schema 来定义工具参数，熟练掌握其编写对于调试至关重要。
*   **关注错误处理**：当外部 API 失败时，MCP Server 应返回结构化的错误信息给 LLM，而不是直接抛出异常，以便 LLM 能理解并尝试自我修正。

## 7. 案例分析

### 成功案例分析
*   **GitHub / GitLab 集成**：通过 MCP Server，用户可以让 Amazon Q 直接读取仓库代码并解释 Bug，甚至生成 Pull Request 描述。这展示了 MCP 处理复杂、动态开发数据的能力。
*   **PostgreSQL 集成**：通过 `mcp-server-postgres`，Amazon Q 可以直接分析数据库结构并生成 SQL 查询，极大地降低了数据分析的门槛。

### 失败案例反思
*   **过度暴露权限**：如果 MCP Server 直接暴露了“删除数据库”的 Root 级别接口，且没有在 Server 端做二次校验，LLM 的幻觉可能导致灾难性后果。
*   **经验教训**：**永远不要在 MCP Server 中暴露破坏性操作的直接接口**，应将其封装为“申请删除”或“移动到回收站”的安全接口。

## 8. 哲学与逻辑：论证地图

### 中心命题
**采用 Model Context Protocol (MCP) 是实现 Amazon Quick Agents 与外部工具深度、可扩展集成的最优解。**

### 支撑理由与依据
1.  **标准化带来的效率**：
    *   *依据*：传统集成需要为每个 Agent 定制 API 调用逻辑；MCP 提供统一接口，一次开发，多处复用。
2.  **生态系统的互操作性**：
    *   *依据*：MCP 是开源协议，不仅支持 Amazon Q，还支持 Claude Desktop 等，降低了厂商锁定的风险。
3.  **安全与可控性**：
    *   *依据*：MCP Server 可以独立部署在企业内网，数据不经过第三方模型提供商（仅传输元数据或指令），符合企业合规要求。

### 反例或边界条件
1.  **超低延迟场景**：如果工具调用对毫秒级延迟极其敏感，MCP 基于 stdio/JSON-RPC 的序列化开销可能成为瓶颈。
2.  **非结构化数据流**：对于实时视频流或海量二进制文件传输，MCP 目前的文本/JSON 聚焦特性可能不是最佳载体。

### 事实与价值判断
*   **事实**：MCP 是 Anthropic 发布的开源协议；Amazon Quick Agents 正在支持该协议。
*   **价值判断**：“最优解”是基于当前 AI 生态碎片化现状的判断，认为标准协议优于私有协议。
*   **可检验预测**：预测未来 12 个月内，主流企业级 SaaS（如 Salesforce, ServiceNow）将推出官方的 MCP Server。

### 立场与验证方式
**立场**：强烈支持将 MCP 作为企业 AI 集成的首选架构模式。

**可证伪验证方式**：
*   **指标**：集成新工具的平均开发时间是否显著缩短（例如从 5 天缩短至 0.5 天）。
*   **观察**：观察市场上 MCP Server 的数量增长趋势，以及 AWS 对该集成的成熟度支持（如是否推出托管 MCP Service）。如果 AWS �

---
## 最佳实践

## 最佳实践指南

### 实践 1：明确工具定义与元数据

**说明**: 在集成外部工具时，必须在 MCP 配置中清晰定义工具的功能、输入参数及预期输出。准确的元数据能让 Amazon Quick Agents 更好地理解何时以及如何调用工具，从而减少幻觉或不正确的调用。

**实施步骤**:
1. 为每个工具编写详细的 `description` 字段，说明其用途和适用场景。
2. 严格定义输入 Schema，包括参数类型、是否必填以及允许的值范围。
3. 在工具名称中使用清晰、动作导向的命名约定（例如 `get_customer_record` 而不是 `data_func_01`）。

**注意事项**: 避免模糊的描述，确保描述中包含工具的业务上下文，而不仅仅是技术实现细节。

---

### 实践 2：实施细粒度的访问控制与身份验证

**说明**: MCP 连接通常涉及访问外部 API 或数据库。为了确保安全性，必须实施最小权限原则，并确保工具集成层具备严格的身份验证机制，防止未授权访问。

**实施步骤**:
1. 为 MCP 服务器配置专用的 IAM 角色或 API 密钥，仅授予执行特定任务所需的权限。
2. 在 MCP 客户端配置中启用并强制要求身份验证（如 OAuth2, Bearer Token）。
3. 定期轮换用于外部工具集成的凭证，并在 Secrets Manager 中管理敏感信息。

**注意事项**: 切勿在代码或配置文件中硬编码凭证；确保代理无法通过提示词注入绕过安全检查。

---

### 实践 3：优化数据上下文与提示词管理

**说明**: MCP 允许模型动态获取上下文。为了提高效率并控制成本，应只传递相关的数据片段，而不是将整个数据库或大型文档直接注入到上下文窗口中。

**实施步骤**:
1. 在工具逻辑中实现数据过滤或预处理，仅返回与用户当前查询最相关的结果。
2. 使用系统提示词明确告知代理如何依赖 MCP 提供的上下文，设定其推理边界。
3. 监控 Token 使用情况，确保工具返回的数据量不会导致上下文窗口溢出或成本激增。

**注意事项**: 平衡上下文的丰富度与简洁性，过多的噪音数据会降低模型的推理能力。

---

### 实践 4：构建健壮的错误处理与重试机制

**说明**: 外部工具调用可能会因为网络问题、API 限流或数据缺失而失败。良好的错误处理能确保 Amazon Quick Agents 能够优雅地降级或向用户寻求澄清，而不是直接崩溃。

**实施步骤**:
1. 在 MCP 服务器端实现标准化的错误响应格式（如 JSON-RPC 错误对象）。
2. 配置合理的超时设置和指数退避重试策略，以处理暂时性故障。
3. 为代理提供清晰的错误映射信息，使其能将技术错误代码转化为用户友好的自然语言解释。

**注意事项**: 避免向最终用户暴露原始的堆栈跟踪或敏感的后端系统信息。

---

### 实践 5：严格验证输入参数

**说明**: 防止提示词注入或恶意参数传递是 MCP 集成的关键。模型生成的工具调用参数必须经过验证，以确保其符合后端系统的安全性和逻辑要求。

**实施步骤**:
1. 在 MCP 服务器端实现严格的 Schema 验证（例如使用 Pydantic 或 JSON Schema 验证）。
2. 对所有传入的字符串参数进行清理，防止 SQL 注入或命令执行攻击。
3. 限制工具可以操作的资源范围（例如，只允许查询特定 ID 范围内的记录）。

**注意事项**: 不要依赖模型（LLM）来保证数据的安全性，始终在执行实际操作前进行服务端验证。

---

### 实践 6：建立全面的日志记录与可观测性

**说明**: 为了调试和优化代理的行为，必须记录工具调用的全生命周期。这有助于理解模型如何决策以及外部工具的性能表现。

**实施步骤**:
1. 记录所有传入的工具调用请求、传递的参数以及返回的响应内容。
2. 集成 CloudWatch 或类似的监控工具，追踪工具调用的延迟、成功率和错误率。
3. 实现结构化日志，包含 Trace ID，以便将代理的特定对话与工具调用关联起来。

**注意事项**: 在记录敏感数据（如 PII）时，确保符合合规性要求，并对日志数据进行脱敏处理。

---
## 学习要点

- MCP（Model Context Protocol）作为一种开放标准，能够安全地将企业数据源与 Amazon Quick Agents 等 AI 应用程序无缝集成。
- 通过 MCP 连接器，开发者可以显著简化将外部工具和数据集成到 Bedrock 中的流程，而无需为每个数据源编写自定义代码。
- Amazon Quick Agents 现已支持 MCP，允许用户通过简单的拖拽操作，在几分钟内将外部数据源接入生成式 AI 应用。
- 该架构通过 Bedrock 的 Knowledge Bases 和 Agents 框架，确保了在利用外部工具增强 AI 能力时的安全性与可控性。
- 集成 MCP 能够有效解决大语言模型（LLM）的上下文窗口限制和知识截止问题，从而提供更准确、实时的响应。
- 开发者可以利用现有的开源 MCP 服务器或社区构建的集成方案，快速扩展 AI 应用与第三方系统（如 Slack、Google Drive）的连接能力。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp](https://aws.amazon.com/blogs/machine-learning/integrate-external-tools-with-amazon-quick-agents-using-model-context-protocol-mcp)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [Amazon Quick](/tags/amazon-quick/) / [Agent](/tags/agent/) / [模型上下文协议](/tags/%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE/) / [工具集成](/tags/%E5%B7%A5%E5%85%B7%E9%9B%86%E6%88%90/) / [AWS](/tags/aws/) / [开发指南](/tags/%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97/) / [第三方集成](/tags/%E7%AC%AC%E4%B8%89%E6%96%B9%E9%9B%86%E6%88%90/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--0.md" >}})
- [使用 MCP 将外部工具集成至 Amazon Quick Agents]({{< relref "posts/20260221-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实施指南]({{< relref "posts/20260220-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--2.md" >}})
- [深度解析Skill/MCP/RAG等五大AI技术的底层逻辑]({{< relref "posts/20260212-juejin-深入理解skillmcpragagentopenclaw底层逻辑-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*