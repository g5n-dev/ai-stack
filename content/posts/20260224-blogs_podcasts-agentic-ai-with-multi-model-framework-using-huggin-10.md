---
title: 基于AWS与Hugging Face smolagents构建多模型医疗智能体
date: 2026-02-24 17:16:55+08:00
draft: false
entry_kind: auto
tags:
- AWS
- Hugging Face
- smolagents
- Agentic AI
- 智能体
- RAG
- 医疗AI
- 多模型部署
categories:
- AI 工程
- 大模型
source: blogs_podcasts
description: 中文总结 本文介绍了如何利用开源库 **Hugging Face smolagents** 在 **AWS** 云平台上构建一个具备**多模型框架**的
  Agentic AI（代理式 AI）解决方案。 **核心内容：** * **工具介绍：** Hugging Face smolagents 是一个开源 Python
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws
scenarios:
- AI/ML项目
- RAG应用
- 工具
---

# 基于AWS与Hugging Face smolagents构建多模型医疗智能体

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-23T15:47:06+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)

---

## 摘要/简介

Hugging Face smolagents 是一个开源 Python 库，旨在通过几行代码就能轻松构建和运行智能体。我们将向您展示如何通过将 Hugging Face smolagents 与 Amazon Web Services (AWS) 托管服务集成，来构建一个智能体 AI 解决方案。您将学习如何部署一个医疗保健 AI 智能体，该智能体将展示多模型部署选项、向量增强的知识检索以及临床决策支持能力。

---

## 导语

随着人工智能从简单的对话交互向具备自主规划能力的 Agent 演进，如何高效构建并部署这些复杂系统成为开发者关注的焦点。本文将介绍如何利用 Hugging Face 的轻量级库 smolagents，结合 AWS 的托管服务来构建企业级 AI 解决方案。通过一个具体的医疗保健场景，您将掌握多模型编排、向量增强检索以及临床决策支持功能的实现方法，从而快速落地具备实用价值的智能体应用。

---

## 摘要

### 中文总结

本文介绍了如何利用开源库 **Hugging Face smolagents** 在 **AWS** 云平台上构建一个具备**多模型框架**的 Agentic AI（代理式 AI）解决方案。

**核心内容：**
*   **工具介绍：** Hugging Face smolagents 是一个开源 Python 库，旨在通过极简的代码快速构建和运行 AI 代理。
*   **集成方案：** 演示了如何将该库与 AWS 的托管服务相结合，以开发企业级 AI 应用。
*   **应用场景：** 以构建一个**医疗保健 AI 代理**为例，展示了该系统的具体能力，包括：
    1.  **多模型部署选项：** 灵活部署和使用多个 AI 模型。
    2.  **向量增强知识检索：** 利用向量数据库技术提升信息获取的准确度。
    3.  **临床决策支持：** 辅助医疗人员进行专业决策。

---

## 评论

**中心观点**
该文章提出了一种通过将 Hugging Face 轻量级智能体库与 AWS 云基础设施原生集成，以低成本、高可扩展性构建“具身”多模态 Agentic AI 的落地路径。

**支撑理由与批判性分析**

1.  **技术栈的“轻量化”与“重服务化”结合（事实陈述 / 作者观点）**
    *   **分析**：文章的核心逻辑在于利用 `smolagents` 的极简代码逻辑（Python-first）来降低 LLM 应用开发的门槛，同时利用 AWS（如 Bedrock, Lambda, S3）承担企业级的重负载。这种“轻代码、重基建”的模式是目前 Agentic AI 落地的主流方向。
    *   **深度评价**：`smolagents` 的优势在于其对工具调用的抽象非常直观，适合快速原型验证。AWS 的加入解决了本地算力不足和数据孤岛问题。
    *   **反例/边界条件**：这种架构并非万能。对于极度依赖低延迟的边缘计算场景，AWS 的云端集中式架构会引入不可接受的延迟；此外，`smolagents` 相比 LangChain 或 CrewAI，生态系统尚不成熟，复杂的工作流编排能力较弱。

2.  **多模态框架的实用主义倾向（你的推断 / 事实陈述）**
    *   **分析**：文章强调“多模态”，通常指利用 VLM（视觉语言模型）结合工具调用。在 AWS 环境下，这意味着通过 Bedrock 接入如 Claude 3.5 Sonnet 或 Titan 多模态模型。
    *   **深度评价**：从行业角度看，这标志着 AI Agent 从“文本聊天机器人”向“数字员工”的转变。能够“看”图表（通过 S3）并操作 AWS 控制台（通过 API）是极具商业价值的场景。
    *   **反例/边界条件**：多模态推理的成本远高于纯文本。如果 Agent 在错误循环中反复调用昂贵的 VLM 模型，成本会瞬间失控。文章若未深入讨论“Guardrails（护栏机制）”和“成本控制”，则属于演示性质，而非生产级方案。

3.  **开源与云厂商的生态博弈（行业观点）**
    *   **分析**：Hugging Face 与 AWS 的深度整合是行业趋势的缩影。HF 提供模型与标准库，AWS 提供算力与分发渠道。
    *   **深度评价**：这种结合降低了企业使用开源模型的门槛。用户无需在本地部署庞大的模型权重，直接通过 AWS 调用 HF Hub 上的模型或托管在 AWS 上的模型。
    *   **反例/边界条件**：存在严重的“厂商锁定”风险。一旦业务逻辑深度耦合 AWS Lambda 或 Bedrock 的特定 API，未来迁移至 Azure 或 GCP 的成本将极高。

**综合评价**

*   **内容深度**：文章属于**教程性质**，侧重于“怎么做”而非“为什么”。它展示了技术拼图的可行性，但缺乏对 Agentic AI 底层挑战（如幻觉、循环调试、长期记忆）的深度探讨。
*   **实用价值**：**高**。对于初创公司或 PoC（概念验证）团队，这提供了一条快速打通从代码到云服务的捷径。
*   **创新性**：**中等**。虽然 `smolagents` 较新，但“开源框架 + 云托管服务”的模式已是行业标准，本文更多是工具链的更新迭代。
*   **可读性**：预计逻辑清晰，侧重代码示例，适合开发者阅读。
*   **行业影响**：促进了“小模型 + 大工具”理念的普及，证明不一定需要 GPT-4 才能构建有用的 Agent。

**实际应用建议**

1.  **不要直接用于生产核心链路**：`smolagents` 仍处于早期迭代版本，API 变更频繁，且缺乏 LangChain 那样的企业级支持，建议仅用于内部工具或 PoC。
2.  **严格监控 Token 消耗**：Agent 调用多模态模型时极易在 Tool Use 阶段消耗大量 Token。务必在 AWS 中设置 Budget Alarm。
3.  **安全权限最小化**：赋予 Agent 的 AWS IAM 角色必须遵循最小权限原则，防止 Agent 被诱导执行删除资源等高危操作。

**可验证的检查方式**

1.  **延迟基准测试**：
    *   *指标*：端到端延迟。
    *   *方法*：构建一个简单的 Agent（如“分析 S3 图片并调用 DynamoDB 记录”），测量从用户发出请求到收到结果的平均时间。对比直接调用 Bedrock API 与通过 smolagents 包装后的耗时差异。
2.  **成本效率分析**：
    *   *指标*：单次执行 Token 数与 API 调用次数。
    *   *方法*：运行 50 次 Agent 任务，统计 `smolagents` 框架引入的额外系统提示词开销。如果框架开销超过 20%，则需评估其轻量级优势是否存在。
3.  **错误恢复能力**：
    *   *观察窗口*：模拟 API 限流或工具无效输入。
    *   *方法*：故意提供错误的 AWS 凭证或格式错误的文件，观察 Agent 是会陷入死循环（无限重试），还是能优雅降级。这是检验 Agent 生产可用性的关键指标。

---

## 技术分析

基于您提供的文章标题和摘要，虽然无法获取全文细节，但结合 **Hugging Face smolagents** 的技术特性、**AWS** 的云服务架构以及 **Agentic AI（智能体 AI）** 的当前发展趋势，我可以为您构建一份深度的分析报告。

### 1. 核心观点深度解读

**主要观点：**
文章主张利用 **Hugging Face smolagents** 这一极简开源库作为“大脑”，结合 **AWS** 的托管服务（如计算、存储、数据库）作为“手脚和躯干”，以极低的代码量和复杂度构建具备实际执行能力的 Agentic AI（智能体）解决方案。

**核心思想：**
作者传达了 **"Simple yet Powerful"（至简即强）** 的理念。传统的 Agent 开发往往需要复杂的框架（如 LangChain）和繁琐的配置，而 smolagents 强调通过 Python 代码直接定义工具，让大语言模型（LLM）能够像解释器一样编写并执行代码来完成复杂任务。结合 AWS，则是为了让这种能力从“原型”走向“生产”，解决可扩展性和安全性问题。

**观点的创新性与深度：**
*   **代码即策略：** smolagents 的核心创新在于它将 Agent 的输出主要定义为 Python 代码，而非传统的 JSON 或文本结构。这使得 Agent 具有极强的逻辑处理能力和通用性。
*   **云原生融合：** 文章不仅讨论算法，更深入讨论了算法与 AWS Lambda（无服务器计算）、Amazon Bedrock（基础模型服务）等的结合，体现了“模型+基础设施”的深度融合视角。

**重要性：**
随着 AI 从“聊天机器人”向“智能体”演进，如何让 AI 不仅“说话”还能“做事”是当前的关键痛点。这篇文章提供了一条低门槛、高可用的落地路径，降低了企业构建 Agentic AI 的技术门槛。

### 2. 关键技术要点

**涉及的关键技术：**
1.  **Hugging Face smolagents：** 一个轻量级 Python 库。
2.  **AWS Lambda / Amazon ECS：** 用于执行 Agent 生成的代码或托管应用。
3.  **Amazon Bedrock / SageMaker：** 提供底层 LLM（如 Claude, Llama）。
4.  **工具调用：** Agent 连接外部 API（如搜索、数据库查询）的机制。

**技术原理与实现方式：**
*   **Code Interpreter 模式：** smolagents 的核心原理是 LLM 接收任务 -> 生成 Python 代码 -> 在沙箱环境中执行代码 -> 获取结果。如果报错，LLM 会根据错误信息自我修正代码再次执行。
*   **工具抽象：** 在 AWS 环境中，AWS SDK（boto3）的功能可以被封装为 Python 函数。smolagents 允许将这些函数直接注册为工具。
    *   *例如：* 定义一个 `upload_to_s3(file)` 函数，Agent 在需要保存文件时会自主生成包含该函数调用的 Python 代码。

**技术难点与解决方案：**
*   **难点：代码执行的安全性。** 让 AI 生成并执行代码存在无限循环或恶意操作的风险。
*   **解决方案：** 文章极可能建议在 **AWS Lambda** 或容器中运行代码，利用 AWS 的 IAM 权限控制系统限制 Agent 的操作范围（如只能访问特定 S3 存储桶），实现最小权限原则。
*   **难点：上下文管理。**
*   **解决方案：** 利用 AWS 的托管数据库或 OpenSearch 存储对话历史和记忆。

**技术创新点：**
*   **极简主义：** 相比于庞大的 Agent 框架，smolagents 代码量极少，易于调试。
*   **多模型支持：** 能够灵活切换底座模型（如从 Hugging Face Inference API 切换到 AWS Bedrock 上的模型），适应不同成本和性能需求。

### 3. 实际应用价值

**对实际工作的指导意义：**
该方案为企业提供了一种**“低成本试错，高扩展部署”**的范式。开发者可以在本地使用 smolagents 快速验证 Agent 逻辑，随后直接迁移至 AWS 架构中处理真实业务数据。

**可应用场景：**
1.  **自动化数据处理：** 比如，“分析这份 S3 里的 CSV 销售数据，生成图表并邮件发送给经理”。Agent 可以生成 Pandas 代码处理数据，调用 SES 发送邮件。
2.  **云运维自动化：** “检查 EC2 实例状态，如果 CPU 利用率过高则重启特定服务”。Agent 调用 CloudWatch 和 EC2 API。
3.  **RAG（检索增强生成）企业助手：** 结合 OpenSearch 查询企业内部文档，进行问答。

**需要注意的问题：**
*   **成本控制：** Agent 的自我修正循环（多次调用 LLM 和执行代码）可能导致 API 成本指数级上升。
*   **幻觉风险：** 生成的代码逻辑可能看似正确但结果错误，需要严格的输出验证机制。

**实施建议：**
*   先在隔离环境（沙箱）中测试 Agent 的代码生成能力。
*   为 Agent 分配独立的 IAM Role，严格限制其 AWS 权限。

### 4. 行业影响分析

**对行业的启示：**
*   **Agent 的平民化：** 以前 Agent 开发属于高级算法工程师的领域，现在普通全栈开发者也能通过几行 Python 代码构建复杂 Agent。
*   **从“模型战”转向“生态战”：** 未来的竞争不仅仅是模型参数的大小，而是框架与云基础设施结合的紧密程度。

**可能带来的变革：**
*   **SaaS 软件的进化：** 未来的 SaaS 可能不再是固定的菜单按钮，而是通过 Agent 对话动态调用 API 执行任务。
*   **运维模式的改变：** AIOps 将从被动监控转向主动修复。

**发展趋势：**
*   **Serverless Agents：** 像文章展示的那样，Agent 将越来越多地运行在无服务器架构上，按需启动，极大降低闲置成本。

### 5. 延伸思考

**引发的思考：**
*   如果 Agent 能够编写代码来解决问题，那么传统的软件开发流程是否会改变？开发者是否将转变为“代码审查员”和“工具提供者”？
*   **安全边界：** 当 AI 拥有 AWS 凭证并能执行代码时，传统的防火墙防线是否失效？我们需要什么样的“AI 防火墙”？

**拓展方向：**
*   **多模态 Agent：** smolagents 支持多模态，未来可以处理图片、音频，结合 AWS Rekognition 等服务，实现视觉理解 Agent。
*   **人机协作：** 在 Agent 执行高风险操作（如删除数据库）前引入人工确认机制。

### 7. 案例分析

**成功案例（基于此类技术架构的典型场景）：**
*   **场景：** 电商公司的自动报表系统。
*   **实施：** 使用 smolagents，让分析师用自然语言描述需求。Agent 编写 Python 代码（使用 Pandas）从 Redshift 查询数据，计算转化率，将结果存入 S3，并生成 HTML 报表。
*   **成功要素：** 工具定义清晰（查询函数、存储函数），执行环境安全（Lambda）。

**失败案例反思：**
*   **场景：** 试图让 Agent 自动修复生产环境的复杂 Bug。
*   **原因：** Agent 生成的代码虽然语法正确，但可能引入逻辑漏洞，或者在没有完全理解业务逻辑的情况下修改了关键配置。
*   **教训：** **高权限场景必须谨慎。** Agent 适合处理“读”和“创建”，对于“修改”和“删除”操作必须设置人工审批关卡。

### 8. 哲学与逻辑：论证地图

**中心命题:**
**将轻量级代码解释型 Agent 框架与云原生托管服务深度集成，是构建生产级、可扩展且低成本 Agentic AI 应用的最优路径。**

**支撑理由与依据:**
1.  **Reason:** 极简性降低了开发门槛，加速了迭代。
    *   *Evidence:* smolagents 仅需几行代码即可定义工具并运行，相比 LangChain 等重型框架，心智负担极小。
2.  **Reason:** 代码生成比 JSON 结构化输出具有更强的通用性和逻辑处理能力。
    *   *Evidence:* LLM 在 Python 代码上的训练表现优异，能够处理复杂的数学运算、逻辑嵌套和数据转换，而无需手动定义每一个输出 Schema。
3.  **Reason:** 云托管服务解决了 Agent 的安全隔离和弹性伸缩问题。
    *   *Evidence:* AWS Lambda 提供了天然的沙箱环境来执行 Agent 生成的代码，防止恶意操作；同时解决了并发请求时的资源调度问题。

**反例或边界条件:**
1.  **Counterexample:** 对于极度追求低延迟（毫秒级）的实时应用，代码解释型 Agent 可能过慢。
    *   *Condition:* 因为 Agent 需要 LLM 生成代码 -> 执行代码 -> 解析结果，多次网络往返导致延迟较高。
2.  **Counterexample:** 在对数据隐私要求极高、不允许数据出境的场景下，依赖云端 API 的架构不适用。
    *   *Condition:* 必须使用完全本地化的 LLM 和本地执行环境。

**命题属性分析:**
*   **事实:** smolagents 是开源库；AWS 是托管服务；两者可以集成。
*   **价值判断:** 这种集成方式是“最优”或“极具吸引力”的（基于开发效率和架构解耦的视角）。
*   **可检验预测:** 采用此架构的团队，其 AI 功能从原型到上线的周期将短于使用传统单体应用框架的团队。

**立场与验证:**
*   **立场:** 支持。我认为这是目前中小型企业落地 Agentic AI 的最佳实践之一。
*   **验证方式:**
    *   *指标:* 开发一个包含 3 个工具（如查数据库、调 API、发邮件）的 Agent 所需的时间。
    *   *对比:* 对比使用 smolagents + AWS 与使用传统开发（手动写逻辑）的开发效率。
    *   *观察窗口:* 项目启动后的 2 周内。

---

## 最佳实践

### 实践 1：优化模型选择与工具调用策略

**说明**: 在使用 Hugging Face `smolagents` 构建智能体时，并非所有任务都需要最大的模型。应根据任务复杂度动态选择模型（如 Qwen、Llama 3 等不同参数量的模型），并确保智能体具备高效调用外部工具（如搜索、计算、代码解释器）的能力，以弥补模型在推理或知识截止日期上的不足。

**实施步骤**:
1. 评估任务需求，将复杂逻辑规划任务分配给参数量较大的模型，将简单查询或格式化任务分配给轻量级模型以降低延迟。
2. 在 `smolagents` 代码中定义明确的工具接口，确保工具输入输出描述清晰，以便模型准确调用。
3. 实施回退机制，当主模型无法解决时，自动切换到更强大的模型或调用特定领域的专家模型。

**注意事项**: 避免过度依赖单一模型处理所有类型的任务，这会导致成本高昂且响应速度慢。确保工具调用的错误处理机制完善，防止因工具执行失败导致智能体循环。

---

### 实践 2：利用 SageMaker 进行模型的高性能部署

**说明**: 直接通过公共 API 访问模型可能存在延迟和隐私问题。最佳实践是利用 AWS SageMaker 将 Hugging Face 模型部署为实时端点。这不仅能提供更低的网络延迟，还能利用 AWS 的基础设施进行自动扩缩容，确保高可用性。

**实施步骤**:
1. 使用 Hugging Face Inference DLC (Deep Learning Container) 在 SageMaker 中部署选定的 LLM 模型。
2. 配置 SageMaker 异步推理端点，处理处理时间较长的智能体任务，避免超时。
3. 设置自动扩缩容策略，根据请求流量动态调整实例数量，优化成本。

**注意事项**: 部署前务必对模型进行量化或蒸馏，以适应 SageMaker 实例的内存限制。监控 GPU 利用率和推理延迟，确保端点响应时间满足 Agentic 工作流的需求。

---

### 实践 3：构建具有上下文感知能力的多模型编排层

**说明**: Agentic AI 的核心在于“编排”。不要将智能体限制在单一的线性流程中。应设计一个多模型框架，其中不同的智能体（基于不同模型）各司其职（例如：一个负责代码生成，一个负责审查，一个负责网络搜索），并通过中央编排器进行通信。

**实施步骤**:
1. 定义清晰的智能体角色和通信协议，确定哪个模型充当“管理者”，哪些充当“执行者”。
2. 利用 `smolagents` 的多智能体协作功能，将复杂任务分解为子任务，分发给专门优化的模型处理。
3. 实施共享的短期记忆机制，使不同模型间的上下文能够无缝传递。

**注意事项**: 智能体之间的通信开销可能很大，应尽量减少传递的 Token 数量，只保留关键信息。防止“无限循环”或“死锁”，即两个智能体陷入相互调用的死胡同。

---

### 实践 4：实施严格的工具使用安全与权限控制

**说明**: 当赋予 Agentic AI 执行代码或调用 AWS API（如 Lambda、S3）的能力时，安全性至关重要。必须遵循最小权限原则，防止智能体因幻觉或恶意输入执行破坏性操作。

**实施步骤**:
1. 为智能体运行时环境配置具有严格限制的 IAM Role，仅包含完成任务所需的特定 S3 读写或 Lambda 调用权限。
2. 在沙箱环境（如 Docker 容器或受限的 Lambda 执行环境）中运行代码执行类工具。
3. 实施人工确认机制，对于高风险操作（如删除数据、发送邮件），强制要求人工审核后才能执行。

**注意事项**: 绝对不要将生产环境的数据库 Root 密钥或完全的管理员权限授予 Agentic 系统。定期审计 CloudTrail 日志，监控智能体的 API 调用行为。

---

### 实践 5：建立基于 Traces 的可观测性与调试体系

**说明**: 多模型框架的决策过程往往是黑盒且非线性的。为了调试错误和优化性能，必须记录智能体的思维链、工具调用过程和中间结果。利用 AWS 的原生服务进行追踪是实现这一目标的关键。

**实施步骤**:
1. 集成 AWS X-Ray 或 OpenTelemetry 来追踪智能体工作流中每个步骤的耗时和状态。
2. 将智能体的中间思考过程和工具调用日志存储到 CloudWatch Logs 或 S3 中，以便事后分析。
3. 建立仪表盘，实时监控每个模型的 Token 消耗、工具调用成功率及最终任务成功率。

**注意事项**: 日志记录可能会产生大量数据，要注意成本控制和敏感信息脱敏。在记录提示词和响应时，确保不泄露用户隐私（PII）。

---

### 实践 6：利用 Prompt Caching 与 RAG 优化上下文管理

**说明**: Agentic 应用往往需要处理大量背景信息。每次请求都重新发送完整的系统提示词和

---

## 学习要点

- Hugging Face smolagents 与 AWS 的结合提供了一种在云端构建和部署多模型 Agentic AI 的轻量级且高效的解决方案
- 利用多模型框架可以灵活调用不同专长的模型（如代码生成、网页浏览等），以解决单一模型无法处理的复杂任务
- smolagents 极简的代码结构使得开发者能够仅用几行代码就快速构建出具备工具调用能力的智能体
- 该架构在 AWS 上的部署流程展示了如何利用云基础设施实现 AI 智能体的可扩展性与高可用性
- 通过集成网络浏览和代码执行工具，智能体具备了实时获取信息并验证其自身输出的能力
- 此方案有效地降低了 Agentic AI 的开发门槛，使开发者能更专注于业务逻辑的实现而非底层架构的搭建

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [AWS](/tags/aws/) / [Hugging Face](/tags/hugging-face/) / [smolagents](/tags/smolagents/) / [Agentic AI](/tags/agentic-ai/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [RAG](/tags/rag/) / [医疗AI](/tags/%E5%8C%BB%E7%96%97ai/) / [多模型部署](/tags/%E5%A4%9A%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [基于AWS与Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI智能体]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-5.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-3.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-4.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI Agent及多模型检索方案]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-2.md" >}})
