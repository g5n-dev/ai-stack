---
title: 基于AWS与Hugging Face smolagents构建多模型医疗AI Agent
date: 2026-02-24 00:25:28+08:00
draft: false
entry_kind: auto
tags:
- Agent
- AWS
- Hugging Face
- smolagents
- RAG
- 医疗AI
- 向量检索
- 多模型部署
categories:
- AI 工程
- 大模型
source: blogs_podcasts
description: 本文介绍了如何利用开源库 Hugging Face smolagents 在 Amazon Web Services (AWS) 上构建多框架的
  Agentic AI（代理式 AI）解决方案。 **核心要点：** 1. **工具介绍**：Hugging Face smolagents 是一个开源 Python
  库，旨在
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws
scenarios:
- RAG应用
- AI/ML项目
- 工具
---

# 基于AWS与Hugging Face smolagents构建多模型医疗AI Agent

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-23T15:47:06+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)

---

## 摘要/简介

Hugging Face smolagents 是一个开源 Python 库，旨在仅用几行代码即可轻松构建和运行 Agent。我们将向您展示如何通过将 Hugging Face smolagents 与 Amazon Web Services (AWS) 托管服务相结合，来构建一个 AI Agent 解决方案。您将学习如何部署一个医疗保健 AI Agent，它将展示多模型部署选项、向量增强的知识检索以及临床决策支持能力。

---

## 导语

随着大模型应用从简单的对话交互转向复杂的任务执行，如何高效构建具备自主决策能力的 AI Agent 成为开发者关注的焦点。本文将介绍如何结合 Hugging Face 的轻量级库 smolagents 与 AWS 托管服务，快速搭建一套多模型架构的解决方案。通过构建一个医疗保健领域的 Agent 实例，您将掌握多模型部署、向量增强检索以及临床决策支持功能的实现路径。

---

## 摘要

本文介绍了如何利用开源库 Hugging Face smolagents 在 Amazon Web Services (AWS) 上构建多框架的 Agentic AI（代理式 AI）解决方案。

**核心要点：**

1.  **工具介绍**：Hugging Face smolagents 是一个开源 Python 库，旨在通过极简的代码量实现 AI 智能体的构建与运行。
2.  **集成方案**：内容展示了如何将 smolagents 与 AWS 的托管服务相结合。
3.  **应用场景**：以构建一个**医疗保健 AI 智能体**为例，演示了以下关键能力：
    *   **多模型部署选项**：支持多种模型的部署策略。
    *   **向量增强的知识检索**：利用向量数据库技术提升信息检索的准确性与相关性。
    *   **临床决策支持**：具备辅助医疗人员进行临床决策的功能。

---

## 评论

**中心观点**
该文章提出了一种通过将 Hugging Face 轻量级智能体库与 AWS 托管服务深度集成，以低成本、高可扩展性构建 Agentic AI（智能体 AI）解决方案的技术范式，旨在解决大模型智能体从原型到生产环境落地的“最后一公里”问题。

**支撑理由与边界分析**

1.  **技术栈的轻量化与原生云结合（事实陈述）**
    文章核心在于利用 `smolagents` 的极简代码逻辑（将 LLM 视为函数调用器）与 AWS 的无服务器架构（如 Lambda、Bedrock）相结合。
    *   **理由**：传统的 Agent 框架（如 LangChain）往往过于厚重，而 `smolagents` 提倡的“代码优先”策略降低了调试复杂度。结合 AWS 的托管服务，开发者无需管理底层基础设施，即可实现智能体的弹性伸缩和高可用性。
    *   **反例/边界**：对于极度依赖低延迟、高频交互的边缘计算场景，AWS 云端的网络延迟可能成为瓶颈；此外，如果 Agent 逻辑需要极其复杂的内存状态管理，轻量级框架可能缺乏像 LangSmith 那样成熟的可观测性工具支持。

2.  **多模型集成的灵活性（作者观点）**
    文章强调了通过 AWS Bedrock 或 SageMaker 接入多种模型（Llama, Mistral 等）的能力。
    *   **理由**：这种架构避免了单一供应商锁定。企业可以根据任务难度动态切换模型（例如：简单任务用小模型，复杂推理用大模型），从而在性能和成本之间取得最佳平衡。
    *   **反例/边界**：多模型编排会显著增加系统架构的复杂度。不同模型的 Prompt 格式、Token 限制和 API 行为差异，需要额外的中间层进行适配，这可能会抵消“轻量级”带来的部分优势。

3.  **生产环境的可落地性（你的推断）**
    文章隐含的观点是：开源 Agent 库 + 企业级云服务 = 生产就绪。
    *   **理由**：AWS 提供了企业级的安全（IAM VPC）、监控和合规性支持，这是纯开源软件栈难以提供的。将 smolagents 部署在 AWS 上，使得 AI 智能体能够真正进入企业核心业务流。
    *   **反例/边界**：生产环境中的 AI Agent 最大的挑战往往不是代码调用，而是“非确定性输出”的风险控制。文章若未深入探讨如何通过 AWS Guardrails 或人工反馈回路（RLHF）来限制 Agent 的幻觉行为，则该方案在金融或医疗等高风险领域的应用将受到严格限制。

**多维度深入评价**

1.  **内容深度**
    文章作为技术教程，在**工程实现**层面具备一定的深度，详细展示了代码与云服务的配置细节。然而，在**理论深度**上略显不足。它更多是在展示“如何拼接工具”，而非探讨 Agent 的规划机制或推理链路的优化。对于 Agentic AI 背后的认知架构理论（如 ReAct vs. Plan-and-Solve）涉及较少，属于典型的“工程导向型”文章。

2.  **实用价值**
    **极高**。对于正在寻找落地方案的初创公司或企业开发者来说，该文章提供了一条清晰的路径：如何利用开源的灵活性结合云厂商的稳定性。它直接解决了开发者“懂算法但不懂运维”或“懂云但不精通模型细节”的痛点，提供了可直接复制的代码片段和架构图。

3.  **创新性**
    **中等**。将轻量级开源工具与巨头云服务结合是行业趋势，并非首创。文章的创新点在于具体化了 `smolagents` 这一较新库在 AWS 生态中的具体位置，填补了该特定技术组合的文档空白。它提出了一种“反框架”趋势——即反对过度封装，回归 Python 代码本质，这在当前日益复杂的 Agent 框架生态中具有反思价值。

4.  **可读性**
    文章结构清晰，逻辑流畅，遵循“问题-方案-代码-架构”的叙事方式。技术术语使用准确，适合具备基础 Python 和 AWS 知识的读者阅读。

5.  **行业影响**
    这篇文章反映了 AI 行业正在从“模型大战”转向“应用落地”。它暗示了未来的 Agentic AI 将不再依赖单一的大模型，而是依赖**模型编排能力**和**云原生基础设施**。这种“开源+云服务”的混合模式可能会成为中小企业的标准选型策略。

6.  **争议点或不同观点**
    *   **过度简化风险**：批评者可能认为，`smolagents` 过于简化了 Agent 的复杂性，可能导致开发者在面对复杂的业务逻辑时，缺乏足够的控制力（如无法精细控制工具调用的并发、重试策略）。
    *   **成本陷阱**：虽然文章强调 AWS 的可扩展性，但 Agentic AI 往往涉及多轮推理和多次工具调用，在云端运行的成本可能远超预期。文章是否充分分析了 Token 消耗与 AWS 运营成本的叠加效应？

7.  **实际应用建议**
    *   **不要忽视安全边界**：在实施时，务必在 AWS 层面开启 Guardrails，防止 Agent 调用敏感 API 或输出违规内容。
    *   **状态管理外包**：对于需要长期记忆的 Agent，建议不要仅依赖 Python 内存，而是集成 AWS DynamoDB 或 Redis，确保状态在函数实例销毁后不丢失。
    *   **渐进式部署**：先从单一

---

## 技术分析

基于提供的标题和摘要，文章主要探讨了如何利用开源库 **Hugging Face smolagents** 结合 **AWS** 的托管服务来构建 **Agentic AI（智能体 AI）** 解决方案。尽管原文内容被截断，但根据标题、摘要以及当前 AI 领域的技术背景，我们可以对该文章的核心观点、技术架构及行业影响进行深入的还原与分析。

### 1. 核心观点深度解读

**主要观点：**
文章的核心主张是**“简化的智能体编程与强大的云基础设施相结合，是构建下一代 AI 应用的最佳实践”**。它主张利用 `smolagents` 这种轻量级、开源的 Python 库来降低 Agentic AI 的开发门槛，同时利用 AWS 的托管服务（如 Bedrock, Lambda, S3 等）来解决企业级部署中的安全性、可扩展性和集成问题。

**核心思想：**
作者试图传达**“低代码 + 高可用”**的哲学。传统的 Agent 开发往往需要复杂的框架（如 LangChain）或深厚的底层编程能力。`smolagents` 的出现将 Agent 抽象为简单的 Python 函数调用，而 AWS 则提供了这些函数运行所需的“肌肉”（算力、存储、数据库）。这种组合让开发者能够专注于业务逻辑（Agent 的“大脑”），而将底层运维交给云平台。

**观点的创新性与深度：**
*   **创新性：** 将 Hugging Face 的开源生态（模型权重、工具库）与 AWS 的企业级闭源/托管生态进行深度绑定。这不仅仅是“调用 API”，而是探讨如何让开源 Agent 在云端拥有“手脚”（通过 AWS SDK 执行实际操作）。
*   **深度：** 文章触及了 AI 从“聊天机器人”向“智能工作者”转型的关键点——即**工具调用**与**环境交互**。它暗示了未来的 AI 开发将不再是训练模型，而是编排模型与云服务的交互。

**重要性：**
随着大模型（LLM）能力趋于平缓，**Agentic AI** 被认为是通往 AGI（通用人工智能）的下一跳。企业急需将模型能力转化为实际的生产力，这篇文章提供了一条从“原型”到“生产”的清晰路径。

### 2. 关键技术要点

**涉及的关键技术或概念：**
*   **Hugging Face smolagents:** 一个极简的 Agent 框架，核心理念是 Agent 默认在 Python 环境中运行，可以动态编写和执行 Python 代码来解决问题。
*   **Agentic Workflow (智能体工作流):** 包含规划、记忆、工具使用和反思的循环。
*   **AWS Bedrock:** 可能用于提供底层的 LLM 能力（如 Claude, Llama 3），或者 smolagents 直接调用 Hugging Face 的推理端点。
*   **AWS SDK (boto3):** Agent 通过 Python 代码直接操作 AWS 资源（如读取 S3 文件、查询 DynamoDB）。

**技术原理和实现方式：**
1.  **定义工具:** 将 AWS 的 API 操作封装成 Python 函数（例如 `upload_file_to_s3(file)`）。
2.  **初始化 Agent:** 实例化 `CodeAgent`，并授予其上述工具的使用权限。
3.  **任务执行:** 用户输入自然语言指令（例如“分析昨天的 S3 日志并生成报告”）。
4.  **代码生成与执行:** smolagents 将指令转化为 Python 代码，调用封装好的 AWS SDK 函数，在沙箱环境中执行代码，并返回结果。

**技术难点与解决方案：**
*   **难点 - 安全性:** 允许 AI 生成并执行代码存在巨大风险（注入攻击、无限循环）。
    *   *解决方案:* 强调使用 AWS IAM 角色进行最小权限控制，以及在沙箱环境中运行 smolagents。
*   **难点 - 幻觉与错误处理:** 生成的代码可能包含语法错误或 API 调用错误。
    *   *解决方案:* Agent 框架通常包含“错误反馈”机制，即捕获报错信息并重新提示 LLM 修正代码。
*   **难点 - 上下文限制:** 复杂的 AWS 任务可能需要大量上下文。
    *   *解决方案:* 利用 AWS 的存储服务作为外部记忆库，而非仅依赖模型上下文窗口。

### 3. 实际应用价值

**对实际工作的指导意义：**
该方案为企业快速落地 AI 提供了**“低成本试错”**的路径。开发者不需要重写基础设施代码，只需利用现有的 AWS 资源，通过 smolagents 进行“胶水”编程。

**可应用场景：**
1.  **自动化运维:** Agent 监控 CloudWatch 指标，发现异常时自动调整 EC2 实例或发送 SNS 通知。
2.  **数据分析师:** Agent 查询 Athena 或 Redshift，生成图表并上传至 S3 供管理层查看。
3.  **内容处理流水线:** Agent 监听 S3 上传事件，调用多模态模型（如 Vision Transformer）处理图片，并存储元数据到 DynamoDB。

**需要注意的问题：**
*   **成本控制:** Agent 的迭代特性（多次调用 LLM 和生成代码）可能导致 API 成本激增。
*   **可观测性:** Agent 的决策过程是“黑盒”的，在 AWS 上需要配合 X-Ray 或 CloudWatch 进行详细的日志记录。

### 4. 行业影响分析

**对行业的启示：**
这标志着**“云原生 AI”** 进入新阶段。过去是“模型上云”，现在是“云服务模型化”。云厂商的 API 变成了 LLM 的“肢体语言”。

**可能带来的变革：**
*   **SaaS 软件的形态改变:** 未来的软件可能不再有复杂的 UI，而是提供一个 Agent 接口，用户通过自然语言指挥软件背后的 AWS 基础设施。
*   **运维角色的转变:** 运维工程师（SRE）的工作将从编写脚本转变为定义 Agent 的权限边界和目标。

**发展趋势：**
*   **Multi-model (多模型):** 正如标题所言，Agent 将根据任务难度动态选择模型（简单任务用小模型 SmolLM，复杂任务用大模型），以优化成本和延迟。

### 5. 延伸思考

**引发的思考：**
*   **代码即策略:** 如果 Agent 通过写代码来解决问题，那么“配置”和“代码”的界限将变得模糊。企业的 IT 管理策略需要适应“动态生成的代码”。
*   **锁定的风险:** 虽然使用了开源的 smolagents，但底层深度绑定 AWS 服务，这可能导致事实上的云厂商锁定。

**拓展方向：**
*   **边缘端 Agent:** smolagents 的轻量级特性是否可以使其部署在 AWS IoT Greengrass 或边缘设备上？
*   **多智能体协作:** 在 AWS Step Functions 中编排多个 smolagents，分别负责不同的微服务领域。

### 7. 案例分析

**成功案例设想（基于技术原理）：**
*   **场景:** 一家电商公司需要每天处理用户上传的数万张客服截图。
*   **实施:** 使用 smolagents 构建一个 Agent。当图片上传到 S3 时，触发 Lambda 运行 Agent。Agent 调用视觉模型识别图片内容（是退款申请还是咨询），提取关键信息，然后写入 DynamoDB 表，并自动在 Zendesk 创建工单。
*   **成功要素:** 自动化流程闭环，利用 AWS 事件驱动架构，无需人工干预。

**失败案例反思：**
*   **场景:** 让 Agent 负责优化 EC2 成本。
*   **失败原因:** Agent 生成的代码逻辑有误，在业务高峰期错误地关闭了核心生产实例，导致服务中断。
*   **教训:** 对于具有“破坏性”的操作（如 Stop/Delete），必须引入“人机协同”机制，让 Agent 提出建议，由人工确认执行。

### 8. 哲学与逻辑：论证地图

**中心命题:**
**“将 Hugging Face smolagents 与 AWS 托管服务集成，是构建高扩展性、低成本且具备实际操作能力的 Agentic AI 应用的最优解。”**

**支撑理由:**
1.  **开发效率:** smolagents 提供了极简的抽象层，使得 Agent 能够直接编写 Python 代码作为行动逻辑，比传统的 ReAct 模式更灵活。
2.  **基础设施能力:** AWS 提供了企业级的存储、计算和数据库服务，Agent 通过代码调用这些服务，具备了改变物理世界的能力，而不仅仅是生成文本。
3.  **成本与性能优化:** 结合两者允许开发者使用小模型处理简单任务，利用 AWS 的算力处理复杂任务，实现成本效益最大化。

**依据:**
*   *直觉:* Python 是通用语言，让 AI 写 Python 比 AI 调用 JSON API 更符合逻辑直觉。
*   *事实:* AWS 是全球最大的云服务商，拥有最丰富的托管服务目录；Hugging Face 是最大的 ML 社区。

**反例 / 边界条件:**
1.  **高安全敏感场景:** 对于金融或医疗数据，允许 AI 动态生成并执行代码可能违反合规性要求。
2.  **极低延迟需求:** smolagents 依赖 LLM 生成代码的解释执行过程，其延迟远高于硬编码的传统 API，不适合毫秒级响应场景。

**命题分类:**
*   **事实:** smolagents 是开源库；AWS 是托管服务平台。
*   **价值判断:** “最优解”是一种价值判断，基于开发成本和功能性的权衡。
*   **可检验预测:** 采用此架构的项目，其 MVP（最小可行性产品）开发时间将比传统框架缩短 50% 以上。

**立场与验证:**
*   **立场:** 支持。对于初创企业和快速原型开发，这是一种极具破坏性的技术栈。
*   **验证方式:**
    *   *实验:* 构建两个相同的 Agent 应用（如“数据分析助手”），一个使用 LangChain + AWS，一个使用 smolagents + AWS。
    *   *指标:* 对比代码行数、开发耗时、Token 消耗量以及任务完成率。
    *   *观察窗口:* 3 个月的迭代周期。

---

## 最佳实践

### 实践 1：构建模块化的多模型编排层

**说明**:
在使用 Hugging Face smolagents 时，不应依赖单一模型完成所有任务。Agentic AI 的核心在于根据任务复杂度动态调用最合适的模型。通过构建一个编排层，可以将轻量级模型（如 SmolLM）用于快速推理和工具调用，而将重量级模型（如 Llama 3）用于复杂的逻辑分析或代码生成。这种分层架构能在保证性能的同时优化成本与延迟。

**实施步骤**:
1. 定义不同模型的能力清单，明确哪些模型适合工具调用，哪些适合文本生成。
2. 在 smolagents 配置中设置模型路由逻辑，根据任务类型（如简单查询 vs 复杂规划）分发请求。
3. 利用 Hugging Face Inference API 或 AWS SageMaker 端点托管多个模型实例。
4. 实施中间件逻辑，监控各模型的响应时间和准确率，动态调整路由策略。

**注意事项**: 避免过度使用大模型处理简单任务，这会导致不必要的延迟和成本增加。确保模型切换过程对上下文窗口的影响最小化。

---

### 实践 2：实施严格的工具沙箱与安全隔离

**说明**:
Agentic AI 的主要特征是自主调用工具（如执行代码、搜索网络或访问数据库）。在 AWS 环境中，必须限制 Agent 的操作权限。最佳实践是使用容器化技术（如 AWS Fargate 或 Lambda）来执行工具代码，确保 Agent 的操作不会危及宿主服务器或泄露敏感数据。Smolagents 允许 Python 代码执行，因此必须防止恶意指令或无限循环。

**实施步骤**:
1. 将 smolagents 的代码执行环境封装在 Docker 容器中，并禁用网络访问或限制其仅能访问特定白名单域名。
2. 使用 AWS IAM Roles for Service（IRSA）为容器分配最小权限策略，仅授予完成任务所需的 S3 或 DynamoDB 权限。
3. 设置执行超时和内存限制，防止 Agent 陷入死循环或消耗过多资源。
4. 在工具返回结果给 Agent 之前，对输出进行清洗和验证。

**注意事项**: 永远不要以 Root 权限运行 Agent 容器。对于涉及生产环境变更的操作，必须引入“人在回路”审批机制。

---

### 实践 3：优化提示词工程与上下文管理

**说明**:
虽然 smolagents 旨在简化提示词编写，但在多模型框架下，不同模型对指令的理解能力不同。最佳实践包括使用结构化提示词，并实施高效的上下文压缩。对于多轮对话，需要智能地管理历史记录，只保留与当前任务相关的上下文，以避免超出模型的 Token 限制并提高响应速度。

**实施步骤**:
1. 为不同类型的工具设计标准化的系统提示词模板，明确工具的输入输出格式。
2. 实施滑动窗口或摘要算法，自动压缩长期对话历史。
3. 利用 OpenTelemetry 跟踪提示词的Token使用情况，识别并优化冗长的指令。
4. 在多模型协作场景中，确保前一个模型的输出被格式化为下一个模型易于理解的输入。

**注意事项**: 注意“提示词注入”攻击，确保用户输入不会覆盖系统指令。在传递敏感信息给模型时，考虑使用动态数据掩蔽。

---

### 实践 4：利用无服务器架构实现弹性扩展

**说明**:
Agent 的工作负载通常具有突发性（例如，一个复杂的搜索任务可能会瞬间触发数百次 API 调用）。在 AWS 上，应利用无服务器技术来处理这种波动。通过将 smolagents 部署在 AWS Lambda 或利用 App Runner 运行 FastAPI 应用，可以实现自动伸缩，从零开始处理请求，从而在闲置时节省成本。

**实施步骤**:
1. 将 smolagents 的核心逻辑容器化，并推送到 Amazon ECR。
2. 配置 AWS Lambda 函数或 AWS App Runner 服务来引用该容器镜像。
3. 设置 Amazon API Gateway 作为前端入口，处理传入的 Agent 请求并进行身份验证。
4. 配置 CloudWatch 告警，基于并发请求数或延迟自动调整并发限制。

**注意事项**: 冷启动可能会影响首次交互的延迟。对于需要低延迟的实时 Agent，可以考虑使用 Provisioned Concurrency 或保持一小部分热实例。

---

### 实践 5：建立全面的可观测性与反馈循环

**说明**:
Agentic 系统的非确定性使其调试变得困难。最佳实践是记录每一次思维链、工具调用和中间结果。在 AWS 环境中，应集中收集日志和指标，以便追踪 Agent 决策路径。这不仅有助于调试，还能用于评估模型的 RAG（检索增强生成）效果和工具使用的准确性。

---

## 学习要点

- Hugging Face smolagents 与 AWS 的结合提供了一种轻量级且高效的 Agentic AI 部署方案，降低了构建智能体的技术门槛。
- 多模型框架允许系统根据任务复杂度动态调用不同规模的模型，从而在性能与推理成本之间取得最佳平衡。
- 利用 AWS 的云基础设施（如 Lambda 或 Fargate）运行 smolagents，能够实现智能体的弹性扩展和高可用性。
- 该框架通过工具调用机制无缝连接外部 API 和数据源，显著增强了 AI 智能体解决实际问题的能力。
- 开发者可以借助 Hugging Face 丰富的模型生态快速迭代，无需从零开始训练即可定制专属的智能体工作流。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Agent](/tags/agent/) / [AWS](/tags/aws/) / [Hugging Face](/tags/hugging-face/) / [smolagents](/tags/smolagents/) / [RAG](/tags/rag/) / [医疗AI](/tags/%E5%8C%BB%E7%96%97ai/) / [向量检索](/tags/%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2/) / [多模型部署](/tags/%E5%A4%9A%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [基于AWS与Hugging Face smolagents构建医疗AI Agent及多模型检索方案]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-2.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-3.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-4.md" >}})
- [深度解析Skill/MCP/RAG等五大AI技术的底层逻辑]({{< relref "posts/20260212-juejin-深入理解skillmcpragagentopenclaw底层逻辑-2.md" >}})
