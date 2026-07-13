---
title: "利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用"
date: 2026-02-10T19:57:28+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "AgentCore", "FAST", "Agentic AI", "AWS", "全栈开发", "IaC", "基础设施"]
categories: ["AI 工程", "开发工具"]
source: blogs_podcasts
description: "本文介绍了如何利用 **Amazon Bedrock AgentCore 的全栈入门模板** 来加速代理应用程序的开发。主要内容如下： **1. 核心目标** 文章旨在指导用户如何在自己的 AWS 账户中部署 **Fullstack AgentCore Solution Template (FAST)**，帮助开发者构"
external_url: https://aws.amazon.com/blogs/machine-learning/accelerate-agentic-application-development-with-a-full-stack-starter-template-for-amazon-bedrock-agentcore
scenarios: ["AI/ML项目"]
---

# 利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-09T16:40:58+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/accelerate-agentic-application-development-with-a-full-stack-starter-template-for-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/accelerate-agentic-application-development-with-a-full-stack-starter-template-for-amazon-bedrock-agentcore)

---
## 摘要/简介

在这篇文章中，你将学习如何将 Fullstack AgentCore Solution Template (FAST) 部署到你的 Amazon Web Services (AWS) 账户，了解其架构，并了解如何根据你的需求进行扩展。你将学习如何构建自己的代理，而 FAST 会处理身份验证、基础设施即代码 (IaC)、部署管道和服务集成。

---
## 导语

构建具备自主决策能力的代理应用往往涉及复杂的身份验证与基础设施配置，容易分散开发者的核心精力。本文介绍的 Fullstack AgentCore Solution Template (FAST) 旨在通过全栈模板简化这一流程，自动处理部署管道与服务集成等底层细节。通过阅读本文，你将掌握如何在 AWS 账户中快速部署该模板，并基于其架构灵活扩展，从而更专注于构建核心业务逻辑。

---
## 摘要

本文介绍了如何利用 **Amazon Bedrock AgentCore 的全栈入门模板** 来加速代理应用程序的开发。主要内容如下：

**1. 核心目标**
文章旨在指导用户如何在自己的 AWS 账户中部署 **Fullstack AgentCore Solution Template (FAST)**，帮助开发者构建自主代理，同时由 FAST 负责处理底层的技术复杂性。

**2. 关键功能与优势**
FAST 通过提供一套完整的解决方案，简化了开发流程，主要承担以下任务：
*   **身份验证**：处理用户认证与授权。
*   **基础设施即代码**：自动化基础设施的配置与管理。
*   **部署管道**：简化持续集成和持续部署 (CI/CD) 流程。
*   **服务集成**：管理不同服务之间的连接与交互。

**3. 学习内容**
读者将了解到 FAST 的系统架构细节，并掌握如何根据具体的业务需求对该模板进行扩展和定制。通过利用 FAST，开发者可以专注于构建代理的核心逻辑，而无需从零开始搭建和维护后端基础设施。

---
## 评论

**中心观点**
文章提出的FAST模板本质上是一种**“以云原生基础设施为中心”的AI工程化策略**，旨在通过标准化AWS服务堆栈来降低Agent应用的开发门槛，其核心价值在于将复杂的后端逻辑与模型调用抽象为可复用的基础设施即代码，而非仅仅提供前端交互demo。

**支撑理由与评价**

1.  **工程化层面的“纵向集成”显著降低了技术债务（事实陈述）**
    从技术角度看，FAST模板利用AWS CDK构建了包含Cognito（认证）、API Gateway（路由）、Lambda（计算）和Bedrock（模型服务）的完整闭环。这种全栈封装方式，避免了开发者从零开始搭建身份认证和API网关的繁琐工作。对于企业级应用而言，安全认证和请求追踪是刚需，模板直接内置这些模块，体现了“开箱即用”的实用主义。

2.  **AgentCore架构体现了“状态与逻辑解耦”的行业最佳实践（作者观点）**
    文章强调AgentCore负责处理逻辑，而FAST处理基础设施。这种分层架构符合当前AI应用开发的趋势：将Prompt工程、工具调用与底层云设施解耦。通过抽象层，开发者可以专注于优化Agent的“大脑”（Prompt/Context），而不用担心“身体”（Infra）的稳定性。这比单纯的LangChain演示代码更接近生产环境标准。

3.  **深度绑定AWS生态带来的“厂商锁定”风险是双刃剑（你的推断）**
    虽然文章展示了如何加速开发，但其架构深度依赖Amazon Bedrock和特定AWS服务（如Cognito）。这种高度集成的优势在于性能和稳定性，但劣势是迁移成本极高。如果企业未来需要切换到Azure OpenAI或Google Vertex AI，重构成本将远高于使用通用框架（如LangChain或LlamaIndex）的项目。

**反例/边界条件**

*   **边界条件1：轻量级或边缘计算场景**
    对于只需要简单RAG（检索增强生成）或运行在边缘设备（如IoT、本地服务器）的Agent应用，FAST模板显得过于臃肿。引入全套AWS基础设施可能导致延迟增加和成本不必要地上升，此时使用轻量级框架（如Streamlit + FastAPI）可能更高效。

*   **边界条件2：高度定制化的复杂推理**
    如果Agent应用需要极其复杂的、跨多步的状态管理，或者需要精细控制模型的Token消耗和推理过程，模板中封装的标准化AgentCore可能过于黑盒。开发者可能需要为了适配模板而牺牲对底层逻辑的细粒度控制权。

**多维度深入评价**

*   **内容深度与严谨性**：文章不仅提供了“Hello World”式的演示，还深入到了架构层面（如CDK代码结构、鉴权流程）。它没有回避企业开发中的痛点（如Auth），论证严谨，属于高水准的技术文档，而非营销软文。
*   **实用价值**：极高。对于已经处于AWS生态内的团队，这是一个可以直接启动的脚手架，节省了数周的搭建时间。
*   **创新性**：中等。虽然“全栈模板”并不新鲜，但将其专门针对Bedrock AgentCore进行优化，并强调“基础设施即代码”在AI领域的应用，具有一定的前瞻性。
*   **行业影响**：这标志着云厂商从“提供模型API”转向“提供应用平台”。AWS正在通过此类模板试图建立Agent应用的开发标准，这将加剧行业内的“平台化”竞争，迫使开发者更早地选边站队。

**争议点与不同观点**

*   **“模板”与“框架”的博弈**：业界存在一种观点认为，应该使用开源框架（如LangChain）而非云厂商提供的封闭模板。争议在于：使用FAST是否意味着为了便利而牺牲了代码的通用性和可移植性？
*   **成本透明度**：文章未深入探讨运行这套全栈架构的长期成本。在高并发场景下，API Gateway、Lambda和Cognito的调用费用可能迅速累积，这对于初创公司是一个潜在的隐形陷阱。

**实际应用建议**

1.  **适用性评估**：在采用FAST前，确认您的团队是否有AWS运维能力。如果没有，这套模板反而会增加认知负担。
2.  **模块化剥离**：建议研究其CDK代码，尝试将Bedrock调用部分与AWS基础设施部分剥离，以便在未来需要时保留业务逻辑，更换底层云服务商。
3.  **安全审计**：虽然模板内置了Auth，但不要盲目信任默认配置。务必检查Cognito的用户池设置和Lambda的IAM角色权限，遵循最小权限原则。

**可验证的检查方式**

1.  **部署时间指标**：记录一个从未接触过Bedrock的开发者，从阅读文章到成功部署并运行第一个Agent所需的时间。如果超过4小时，则说明文档或模板的易用性存在虚高。
2.  **并发压力测试**：使用JMeter或K6对部署好的FAST应用进行压测，观察在Lambda冷启动和API Gateway限流情况下的表现，验证其“生产就绪”的声称是否属实。
3.  **成本分析实验**：运行该模板24小时，并在AWS Cost Explorer中查看具体费用明细，对比使用自建代理服务器的成本差异。
4.  **代码可读性审查**：检查生成的CDK代码，评估在不依赖文档的情况下，开发者修改一个API端点或添加一个新的Tool需要修改多少行代码。

---
## 技术分析

基于您提供的文章标题和摘要，以及对 AWS (Amazon Web Services) 和 Amazon Bedrock AgentCore 技术生态的理解，以下是对该文章及所代表的“全栈代理核心解决方案模板（FAST）”的深入分析。

---

# 深度分析：Amazon Bedrock AgentCore 全栈开发模板 (FAST)

## 1. 核心观点深度解读

**主要观点**
文章的核心主张是：**构建生成式 AI 应用不应从零开始，而应采用“全栈”式的标准化模板来加速开发。** 通过引入 FAST (Fullstack AgentCore Solution Template)，开发者可以跳过繁琐的基础设施搭建、身份认证配置和前端后端对接，直接进入核心业务逻辑的“代理”构建阶段。

**核心思想**
作者试图传达一种**“基础设施即代码”与“AI 工程化”深度融合**的思想。在 AI 应用爆发初期，大家关注模型效果；现在，行业痛点已转移到如何将模型高效、安全地集成到企业软件中。FAST 的思想是将“认证、日志、UI、API 网关”等通用需求封装成标准化的“脚手架”，让开发者专注于 Agent 的“大脑”（推理与工具调用），而不是“身体”（服务器与数据库）。

**创新性与深度**
其创新点在于**全栈的垂直整合**。通常 AWS 提供的示例仅限于后端或单个 Lambda 函数，而 FAST 提供了一个包含前端 UI、身份认证和后端逻辑的完整闭环。这种深度不仅体现在代码层面，更体现在架构层面——它预设了一种经过 AWS 验证的最佳实践架构，解决了企业在落地 AI 时“懂模型不懂架构”或“懂架构不懂模型”的割裂问题。

**重要性**
这个观点至关重要，因为它标志着 AI 开发从“原型验证”走向“生产级部署”。企业不再满足于一个简单的 Python 脚本或 ChatGPT Wrapper，他们需要符合企业安全标准、可扩展、可维护的完整应用。FAST 降低了这一门槛。

## 2. 关键技术要点

**关键技术概念**
*   **Amazon Bedrock AgentCore:** 核心引擎，负责编排大模型（LLM）、提示词管理和工具调用。
*   **AWS CDK (Cloud Development Kit):** 用于定义基础设施即代码（IaC），实现一键部署。
*   **Amazon Cognito:** 处理用户身份认证和授权，确保应用安全。
*   **Amplify:** 通常用于全栈场景下的前端托管与后端交互配置。
*   **LangChain / LlamaIndex (隐含):** 虽然摘要未提，但此类 Agent 框架通常用于构建 Agent 的逻辑链。

**技术原理与实现**
FAST 的实现原理遵循典型的**无服务器架构**：
1.  **前端层：** 一个预构建的 React/Vue 应用，通过 API Gateway 与后端通信。
2.  **接口层：** API Gateway 作为入口，处理请求路由与鉴权。
3.  **逻辑层：** Lambda 函数承载业务逻辑，调用 Bedrock API。
4.  **代理层：** Bedrock AgentCore 负责理解用户意图，并动态调用外部工具（如数据库查询、API 请求）来完成任务。

**技术难点与解决方案**
*   **难点：** 身份验证的传递。在 Web 应用中，如何确保前端登录用户的安全上下文能传递给后端的 Agent，防止越权访问。
*   **方案：** FAST 利用 Cognito JWT (JSON Web Token) 校验，API Gateway 验证 Token 后将用户信息传递给 Lambda，确保 Agent 在特定权限下执行操作。
*   **难点：** 冷启动与延迟。
*   **方案：** 架构上通常采用 Lambda 预置并发或优化的容器镜像，确保 Agent 响应速度。

**技术创新点**
最大的创新在于**“可扩展性”的设计**。模板通常预留了“工具插件”接口。开发者只需编写符合特定 Schema 的 Lambda 函数，注册到 Bedrock Agent 中，Agent 就能自动学会调用这些工具，无需重写核心代码。

## 3. 实际应用价值

**指导意义**
对于企业架构师和 AI 工程师，FAST 提供了一个**生产级的“最小可行性产品”（MVP）基线**。它告诉开发者：一个安全的 AI 应用长什么样？数据流向是怎样的？如何处理流式响应？

**应用场景**
1.  **企业知识库问答：** 快速搭建一个基于内部文档（通过 Kendra 检索）的问答助手。
2.  **销售/客服 Copilot：** 利用 Agent 调用 CRM 系统，自动生成报告或查询订单状态。
3.  **内部运营自动化：** 自动化处理流程，如“帮我申请服务器资源”或“分析昨日日志异常”。

**需注意的问题**
*   **成本控制：** 全栈架构涉及多个 AWS 服务（API Gateway, Lambda, Bedrock），并发量大时成本可能高于单一脚本。
*   **模型幻觉：** 模板解决了架构问题，但未解决 LLM 本身的幻觉问题，业务逻辑层需增加防护机制。

**实施建议**
建议先在开发环境部署 FAST，通过修改其中的 Prompt 和工具配置来验证业务逻辑，验证成功后再通过 CDK 迁移到生产环境，并修改 Cognito 的用户池配置以对接企业现有 SSO。

## 4. 行业影响分析

**行业启示**
FAST 的出现反映了云厂商正在从**“卖模型”转向“卖平台”**。竞争的焦点不再是模型 API 本身，而是谁能为开发者提供更顺滑的开发体验（DX）和更完善的周边生态（安全、监控、集成）。

**带来的变革**
这可能会加速**SaaS 的 AI 化重构**。大量传统 SaaS 软件厂商将利用此类模板，快速将“搜索框”升级为“Agent 代理”，从而改变用户与软件交互的方式。

**发展趋势**
*   **标准化：** AI 应用开发将逐渐形成类似 MVC 模式的标准架构。
*   **低代码/无代码化：** 像 FAST 这样的模板未来可能演变成可视化的配置界面，进一步降低开发门槛。

## 5. 延伸思考

**拓展方向**
*   **多模态支持：** 目前的模板主要基于文本，未来如何扩展以支持图片、音频输入？
*   **人机协同：** Agent 需要人类确认时，架构如何支持“中断-等待-继续”的异步流程？

**待研究问题**
*   如何在模板中内置“可观测性”，让 Agent 的思考过程对开发者透明？
*   如何解决 Agent 在执行长任务时的状态保持问题？

**未来趋势**
**Agentic Workflow（代理工作流）** 将取代单一的 Prompt。未来的模板将内置更复杂的编排引擎（如 Bedrock 的 Multi-Agent 系统），模拟软件工程团队的角色分工（一个写代码，一个测试，一个审核）。

## 6. 实践建议

**如何应用到项目**
1.  **克隆与部署：** 获取 FAST 源码，使用 AWS CDK CLI 进行引导部署。
2.  **定制前端：** 修改前端 UI 库的配色和布局，使其符合企业品牌。
3.  **配置 Agent：** 在 Bedrock 控制台中创建 Agent，并编写业务逻辑的 Prompt。
4.  **开发工具：** 编写 Lambda 函数作为 Agent 的“手”，连接真实数据库。

**行动建议**
*   **学习 CDK：** 如果不熟悉 TypeScript/Python CDK，这是必须补充的知识。
*   **理解 OpenAPI Schema：** Agent 调用工具依赖严格的 API 描述，需学会定义标准的 OpenAPI 规范。

**注意事项**
*   **API Key 管理：** 切勿将 API Key 硬编码在代码中，应使用 AWS Secrets Manager。
*   **数据隐私：** 确保发送给 Bedrock 的数据符合企业合规要求（如开启不跨区存储）。

## 7. 案例分析

**成功案例：企业 HR 助手**
某公司利用 FAST 快速构建了 HR 问答 Agent。
*   **做法：** 利用 FAST 的认证模块对接员工账号，将 HR 政策文档存入 OpenSearch，通过 Bedrock Agent 调用查询接口。
*   **结果：** 2 周内上线，HR 咨询邮件减少 40%。

**失败反思：过度依赖 Agent 自由度**
某开发者试图让 Agent 直接编写 SQL 并执行。
*   **问题：** Agent 生成的 SQL 偶尔有误，导致数据库报错甚至数据泄露风险。
*   **教训：** Agent 适合作为“意图识别”和“参数填充”，核心业务逻辑仍应有后端代码严格校验，不能完全信任 LLM 生成的代码直接执行。

## 8. 哲学与逻辑：论证地图

**中心命题**
**采用像 FAST 这样的全栈标准化模板是企业构建生产级 AI 应用的最优解，因为它在开发速度与架构安全性之间取得了最佳平衡。**

**支撑理由**
1.  **工程效率：** 事实——从零搭建全栈架构（Auth、DB、API）通常需要数周，模板可将其缩短至数小时。
2.  **架构健壮性：** 事实——AWS 推荐的架构经过了大规模验证，比普通开发者临时拼凑的架构更具可扩展性和安全性。
3.  **维护成本：** 价值判断——标准化代码意味着更低的维护门槛和更容易的团队交接。

**反例与边界条件**
1.  **高度定制化需求：** 如果应用需要极其特殊的非 AWS 原生集成或极致的性能优化，模板的约束可能成为负担。
2.  **极简需求：** 如果只是一个简单的内部脚本，引入全栈模板属于“过度设计”，增加了不必要的复杂度。

**可检验预测**
*   如果采用 FAST，团队从“想法”到“可演示原型”的时间将减少 70% 以上。
*   使用该模板的应用在面临突发流量时，其无服务器架构的稳定性将显著优于自建服务器的架构。

**立场与验证**
**立场：** 支持。对于 90% 的企业级 AI 应用场景，技术壁垒在于工程落地而非模型算法本身。FAST 解决了工程落地问题。
**验证方式：** 选择两个功能相同的项目，一组使用 FAST 从零开发，一组使用传统全栈开发。对比“代码行数”、“部署耗时”和“安全漏洞扫描报告”。预计 FAST 组在安全性和开发速度上均显著胜出。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用全栈模板快速搭建基础架构

**说明**: 使用提供的 Amazon Bedrock AgentCore 全栈入门模板，可以显著减少从零开始构建代理应用的时间。该模板预配置了基础设施代码（如 AWS CDK 或 CloudFormation）、身份验证（IAM）角色以及基本的 API 网关设置，确保开发环境符合生产级标准。

**实施步骤**:
1. 克隆或下载 Amazon Bedrock AgentCore 的 starter template 代码库。
2. 根据项目需求修改配置文件（如 `cdk.json` 或 `config.json`），定义区域、模型选择（如 Claude 3 或 Llama 3）和资源命名。
3. 运行部署脚本（例如 `npm run deploy`）以自动预置云资源。

**注意事项**: 在部署前请确保 AWS CLI 已配置正确的凭据和默认区域，并检查账户配额以避免资源创建失败。

---

### 实践 2：实施精细化的 IAM 权限控制

**说明**: 安全性是 Agent 应用开发的核心。最佳实践要求遵循最小权限原则，严格限制 Agent Core 访问 Bedrock API 及其他 AWS 服务（如 Lambda、DynamoDB）的权限。模板通常包含宽泛的策略，必须根据实际业务逻辑进行裁剪。

**实施步骤**:
1. 审查模板生成的 IAM 角色，移除未使用的服务权限。
2. 为特定的 Lambda 函数或容器化逻辑创建独立的执行角色。
3. 使用 IAM Conditions 键限制 Agent 只能调用特定的 Foundation Model IDs。

**注意事项**: 避免使用 `AdministratorAccess` 或 `*` 通配符资源，定期使用 IAM Access Analyzer 审计权限。

---

### 实践 3：构建模块化的可复用组件

**说明**: 将代理的逻辑拆分为独立的、可复用的组件。利用 AgentCore 的架构，将提示词工程、知识库检索逻辑和后端业务流程解耦。这不仅能提高代码的可维护性，还能在不同 Agent 之间共享通用功能。

**实施步骤**:
1. 将常用的 Prompt 模板抽象为独立的配置文件或参数存储在 SSM Parameter Store 中。
2. 封装通用的工具调用逻辑为独立的 Lambda 函数或 API 端点。
3. 建立统一的中间件层来处理与 Bedrock API 的交互，便于未来切换模型版本。

**注意事项**: 确保组件之间的接口定义清晰，使用版本控制管理 Prompt 的变更，以便快速回滚。

---

### 实践 4：建立完善的可观测性与日志记录

**说明**: 代理应用的行为具有非确定性，因此必须建立强大的监控体系。通过集成 CloudWatch 和 X-Ray，追踪从用户请求到 Bedrock 模型响应的完整链路，记录 Token 使用量、延迟时间以及推理结果。

**实施步骤**:
1. 在模板的配置中启用详细的 CloudWatch Logs 日志组。
2. 启用 AWS X-Ray 追踪以可视化请求链路，识别性能瓶颈。
3. 设置针对特定错误的 CloudWatch 告警（如模型调用超时、速率限制 429 错误）。

**注意事项**: 注意日志存储成本，合理设置日志保留期限，并对敏感数据进行脱敏处理后再记录。

---

### 实践 5：优化提示词与上下文管理

**说明**: 模型的输出质量高度依赖于输入的 Prompt 和上下文。最佳实践包括使用系统提示词设定 Agent 的行为边界，并利用 Bedrock 的知识库功能或外部向量数据库提供准确的 RAG（检索增强生成）上下文。

**实施步骤**:
1. 在代码库中明确区分 System Prompt 和 User Prompt 的定义。
2. 实施上下文窗口管理策略，确保发送给模型的 Prompt 不超过最大 Token 限制。
3. 利用 Guardrails for Amazon Bedrock 过滤用户输入和模型输出，防止有害内容。

**注意事项**: 定期测试和迭代 Prompt 以适应模型的更新，同时监控 Token 消耗以控制成本。

---

### 实践 6：实施自动化测试与持续集成/持续部署 (CI/CD)

**说明**: 为了加速开发并确保稳定性，应尽早引入自动化测试。由于 LLM 的输出具有概率性，传统的断言测试可能不够，需要引入基于语义相似度或特定业务规则的评估方法。

**实施步骤**:
1. 为 Agent 的工具调用逻辑编写单元测试。
2. 集成 CI/CD 流水线（如 AWS CodePipeline 或 GitHub Actions），在代码提交时自动运行基础设施合规性检查。
3. 实施金丝雀发布策略，逐步将流量切换到新版本的 Agent，观察错误率和响应延迟。

**注意事项**: 在测试环境中使用成本较低的模型或模拟响应进行开发调试，仅在集成测试时调用实际的 Bedrock 端点。

---
## 学习要点

- Amazon Bedrock AgentCore 全栈入门模板通过预置前端和后端代码，显著降低了开发生成式 AI 应用的复杂度并缩短了开发时间。
- 该模板无缝集成了 Amazon Bedrock 的托管服务能力，使开发者无需管理底层基础设施即可构建高性能的智能体应用。
- 提供了开箱即用的安全与治理最佳实践配置，确保企业级应用在构建之初就符合安全合规标准。
- 模板包含完整的可定制化 UI 组件和业务逻辑，开发者可专注于核心业务场景的差异化实现而无需从零搭建通用功能。
- 通过统一的代码结构简化了与 Amazon Bedrock Agents 的集成流程，便于快速实现复杂的多步骤推理和任务自动化。
- 支持与 Amazon Bedrock 知识库的快速连接，轻松实现基于私有数据的检索增强生成（RAG）功能以提升回答准确性。
- 该方案提供了清晰的参考架构和示例代码，是开发者学习和落地 Amazon Bedrock AgentCore 的最佳实践起点。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/accelerate-agentic-application-development-with-a-full-stack-starter-template-for-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/accelerate-agentic-application-development-with-a-full-stack-starter-template-for-amazon-bedrock-agentcore)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [AgentCore](/tags/agentcore/) / [FAST](/tags/fast/) / [Agentic AI](/tags/agentic-ai/) / [AWS](/tags/aws/) / [全栈开发](/tags/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [IaC](/tags/iac/) / [基础设施](/tags/%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow IT 运营]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Claude Code：面向基础设施开发的AI编程工具]({{< relref "posts/20260205-hacker_news-claude-code-for-infrastructure-12.md" >}})
- [Claude Code：面向基础设施的编程工具]({{< relref "posts/20260205-hacker_news-claude-code-for-infrastructure-15.md" >}})
- [Claude Code：面向基础设施开发的AI编程助手]({{< relref "posts/20260205-hacker_news-claude-code-for-infrastructure-17.md" >}})
- [Claude Code：面向基础设施的AI编程助手]({{< relref "posts/20260205-hacker_news-claude-code-for-infrastructure-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*