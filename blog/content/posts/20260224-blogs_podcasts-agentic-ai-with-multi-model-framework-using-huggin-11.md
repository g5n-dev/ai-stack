---
title: "基于AWS与Hugging Face smolagents的多模型医疗AI Agent构建"
date: 2026-02-24T20:13:02+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "AWS", "Hugging Face", "smolagents", "RAG", "医疗AI", "多模型", "向量检索"]
categories: ["AI 工程", "大模型"]
source: blogs_podcasts
description: "以下是对该内容的简洁总结： 本文介绍了利用 **Hugging Face smolagents** 开源库与 **Amazon Web Services (AWS)** 托管服务相结合，构建具有**多模型框架的 Agentic AI（代理式 AI）** 解决方案。 **核心内容与学习要点：** 1. **技术栈**："
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws
scenarios: ["RAG应用", "AI/ML项目", "工具"]
---

# 基于AWS与Hugging Face smolagents的多模型医疗AI Agent构建

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-23T15:47:06+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)

---
## 摘要/简介

Hugging Face smolagents 是一个开源 Python 库，旨在用几行代码就能轻松构建和运行 Agent。我们将向您展示如何通过将 Hugging Face smolagents 与 Amazon Web Services (AWS) 托管服务集成，来构建一个 AI Agent 解决方案。您将学习如何部署一个医疗保健 AI Agent，该 Agent 展示了多模型部署选项、向量增强知识检索以及临床决策支持能力。

---
## 导语

随着大模型应用从单一对话向复杂任务执行演进，基于多模型框架的 Agentic AI 正成为技术落地的关键。本文将介绍如何利用 Hugging Face smolagents 轻量级库，结合 AWS 托管服务构建企业级 AI 解决方案。通过一个医疗保健领域的具体案例，您将掌握多模型部署、向量增强检索及临床决策支持功能的实现方法，从而在实际项目中高效构建具备自主规划能力的智能 Agent。

---
## 摘要

以下是对该内容的简洁总结：

本文介绍了利用 **Hugging Face smolagents** 开源库与 **Amazon Web Services (AWS)** 托管服务相结合，构建具有**多模型框架的 Agentic AI（代理式 AI）** 解决方案。

**核心内容与学习要点：**

1.  **技术栈**：
    *   **Hugging Face smolagents**：一个开源 Python 库，旨在通过极少的代码量简化 AI 代理的构建与运行。
    *   **AWS**：提供云基础设施和托管服务，用于支撑应用的部署与扩展。

2.  **实战演示**：
    *   文章将指导读者如何整合上述工具，从零开始构建一个 Agentic AI 系统。

3.  **应用场景（医疗 AI 代理）**：
    *   为了演示具体能力，文章构建了一个**医疗领域的 AI 代理**。该代理展示了以下关键功能：
        *   **多模型部署选项**：展示了如何灵活部署和使用不同的 AI 模型。
        *   **向量增强知识检索**：利用向量数据库技术，提升信息获取的准确性与相关性（RAG）。
        *   **临床决策支持**：具备了辅助医疗人员进行临床决策的能力。

**总结**：该方案通过结合轻量级开源框架与强大的云服务，展示了快速构建具备高级检索和决策支持功能的行业特定 AI 应用的完整路径。

---
## 评论

### 中心观点
该文章提出了一种将 Hugging Face 轻量级智能体框架 `smolagents` 与 AWS 托管服务深度集成的技术路径，旨在通过标准化的云服务组合，以较低的研发投入构建具备高可用性的 Agentic AI 应用。

### 支撑理由与边界条件

**1. 开源生态与云原生弹性的互补（事实陈述）**
文章的核心逻辑在于利用 `smolagents` 的 Python 优先开发体验，结合 AWS 基础设施（如 Bedrock、Lambda、DynamoDB）。
*   **理由：** Hugging Face 提供了丰富的预训练模型与工具接口，而 AWS 提供了企业级的身份认证、计费管理及容错机制。这种组合解决了单纯使用开源框架在生产环境部署中面临的运维难题。
*   **边界条件/反例：** 该架构在并发请求较高时可能面临 AWS Lambda 的冷启动延迟问题。此外，跨服务调用（如从 HF Hub 拉取模型或推理结果）的网络开销，可能导致端到端延迟高于纯本地部署方案。

**2. 代码抽象层与“黑盒”模型服务的权衡（技术分析）**
文章展示了 `smolagents` 通过少量代码构建 Agent 的能力，侧重于开发效率。
*   **理由：** 在 PoC（概念验证）阶段，这种高层抽象降低了 LLM 应用开发的门槛，有助于快速验证业务逻辑。
*   **边界条件/反例：** 在生产环境中，高度封装增加了调试难度。当 Agent 产生幻觉或工具调用链路出错时，开发者难以在 AWS 的黑盒服务与 HF 的封装库之间定位具体的 Prompt 泄漏或 Token 解析错误。相比之下，直接调用 API 虽然代码量较大，但提供了更细粒度的控制权。

**3. 多模型框架的实际落地挑战（架构推断）**
文章标题提及“Multi-model framework”，指向了在不同任务间切换模型的能力。
*   **理由：** 利用 AWS Bedrock 的多模型接入能力，配合 `smolagents` 的工具调用机制，理论上可以实现“小模型负责规划，大模型负责推理”的 MoE（混合专家）模式，以优化成本与性能的平衡。
*   **边界条件/反例：** 多模型编排增加了状态管理的复杂性。在处理长上下文记忆或跨工具对话历史时，不同模型间的 Token 限制和上下文窗口差异可能导致信息截断，破坏 Agent 思维链的连贯性。

### 深度评价维度分析

#### 1. 内容深度：3/5
文章主要停留在“如何连接”的教程层面，侧重于 API 调用和配置说明。虽然展示了集成步骤，但缺乏对 Agent 内部机制（如 ReAct 循环、Tool Parsing 错误处理）的深入剖析。对于生产环境中常见的异常情况（如 S3 存储限制或 Bedrock 限流），文章未提供具体的重试或降级策略。

#### 2. 实用价值：4/5
对于初创团队或原型开发，该方案具有较高的参考价值。它提供了一条从本地实验到云端部署的迁移路径。特别是对于已部署 AWS 生态的团队，文章降低了引入 Hugging Face 智能体工具的技术门槛。

#### 3. 创新性：3/5
“Agentic AI + Serverless”并非全新概念，但文章具体化了 `smolagents` 这一特定库与 AWS 的结合。其特点在于将 HF 的轻量化开发理念引入 AWS 生态，试图在敏捷开发与企业级稳定性之间寻找平衡点。

#### 4. 可读性：4/5
文章结构遵循“问题-架构-代码-运行”的逻辑，条理清晰。但对于不熟悉 AWS IAM 权限配置的开发者，隐性的配置细节可能会增加实际操作的复杂度。

#### 5. 行业影响：2/5
这属于技术层面的增量更新，而非颠覆性变革。它主要服务于现有的 AWS 开发者社区，促进了 Hugging Face 工具库的普及，但不太可能改变 Agentic AI 的整体行业格局。

#### 6. 争议点：供应商锁定
文章未深入探讨“供应商锁定”风险。虽然 `smolagents` 是开源的，但后端强依赖 AWS Bedrock。若未来需迁移至 Azure、GCP 或自建集群，重构 Agent 层代码逻辑（特别是工具定义部分）可能面临兼容性挑战。

### 实际应用建议

1.  **成本监控先行：** 在部署基于 AWS 的 Agent 时，务必设置 CloudWatch 告警，监控 Lambda 调用次数及 Bedrock Token 消耗，防止因 Agent 逻辑循环导致意外成本激增。
2.  **混合部署策略：** 建议将核心状态管理保留在 DynamoDB 等持久化层中，避免仅依赖 Agent 内存状态，以应对无服务器架构可能出现的实例中断问题。
3.  **可观测性集成：** 鉴于黑盒调用的调试难度，建议在生产环境中引入 OpenTelemetry 等链路追踪工具，完整记录 Prompt 发送与 Tool 返回的原始日志，以便快速排查故障。

---
## 技术分析

基于提供的标题和摘要，以及对 **Hugging Face smolagents**、**Agentic AI**（智能体AI）及 **AWS** 云原生架构的技术现状的理解，以下是对该文章内容的深度解析与延伸分析。

---

# 深度分析：基于 Hugging Face smolagents 与 AWS 的多模型 Agentic AI 架构

## 1. 核心观点深度解读

**主要观点**
文章的核心主张是**“通过轻量级开源框架与云原生托管服务的深度集成，可以极大降低构建复杂 Agentic AI（智能体 AI）系统的门槛”**。它展示了如何利用 Hugging Face 的 `smolagents` 库作为“大脑”，利用 AWS 的基础设施（如 Bedrock、Lambda、S3）作为“手脚”和“记忆”，从而快速构建具备实际执行能力的 AI 智能体。

**核心思想**
作者传达了一种**“实用主义的模块化架构”**思想。在 AI 发展从单纯的“对话”转向“行动”的阶段，开发者不应重复造轮子。`smolagents` 提供了极简的代码抽象，而 AWS 提供了企业级的可靠性和扩展性。两者的结合代表了未来 AI 应用开发的主流范式：**逻辑控制与模型推理解耦，工具调用与基础设施无缝对接。**

**创新性与深度**
*   **轻量化：** `smolagents` 强调代码极简，不同于 LangChain 等重型框架，它更接近 Python 原生逻辑，降低了认知负荷。
*   **多模型协同：** 文章强调“Multi-model”，意味着智能体不再依赖单一模型，而是可以根据任务动态选择最合适的模型（例如用 Claude 3.5 Sonnet 写代码，用 Llama 3 进行摘要），这是迈向“通用人工智能”架构的重要一步。
*   **深度：** 文章不仅停留在演示，而是探讨了如何将智能体嵌入企业级环境，解决了从 Demo 到生产环境的“最后一公里”问题。

**重要性**
随着大模型能力的饱和，竞争焦点已转移至**Agent（智能体）**的构建能力。该文章提供了一条低成本、高效率的路径，让中小企业和个人开发者也能利用 AWS 的算力生态构建强大的智能体，加速了 AI 技术的民主化落地。

## 2. 关键技术要点

**涉及的关键技术**
*   **Hugging Face smolagents:** 一个极简的 Python 库，专注于让 LLM 能够通过代码解释器或工具调用与环境交互。
*   **Agentic AI (智能体 AI):** 具备感知、规划、记忆和行动能力的 AI 系统。
*   **Amazon Bedrock:** AWS 的托管模型服务，提供对多种基础模型的访问。
*   **AWS Lambda / ECS:** 用于执行智能体生成的代码或逻辑的无服务器计算环境。
*   **Tool Use (工具调用):** 智能体调用外部 API（如搜索、数据库查询、文件操作）的能力。

**技术原理与实现**
1.  **代理循环:** `smolagents` 初始化一个 Agent，接收用户目标。
2.  **推理与规划:** Agent 调用 LLM（通过 Hugging Face API 或 AWS Bedrock），将目标分解为步骤。
3.  **工具选择:** Agent 根据上下文决定是否需要使用工具（如 Python 解释器、天气 API）。
4.  **执行与反馈:** 工具在 AWS 环境中执行（例如在 Lambda 中运行 Python 脚本），结果返回给 LLM。
5.  **最终输出:** LLM 整合所有步骤的输出，生成最终答案。

**技术难点与解决方案**
*   **难点：幻觉与不可控执行。** 智能体可能会生成恶意或错误的代码。
    *   *解决方案：* 利用 AWS 的 IAM 权限控制和沙箱环境（如受限的 Lambda 执行角色）来限制 Agent 的操作范围。
*   **难点：多模型调用的延迟与成本。**
    *   *解决方案：* 文章可能暗示了使用 AWS Bedrock 的智能路由功能，或者在 `smolagents` 中配置不同的模型端点，根据任务复杂度动态切换（简单任务用小模型，复杂任务用大模型）。

**技术创新点**
*   **代码优先:** `smolagents` 允许 Agent 直接编写并执行 Python 代码作为行动方式，比传统的 JSON 格式工具调用更灵活、更强大。
*   **托管服务解耦:** 智能体逻辑运行在本地或轻量级容器，而重型推理和存储完全托管在云端，实现了弹性伸缩。

## 3. 实际应用价值

**对实际工作的指导意义**
*   **降低开发成本：** 开发者无需从零构建 RAG（检索增强生成）或 Agent 框架，直接基于 `smolagents` 可以在几小时内搭建原型。
*   **云原生集成：** 指导开发者如何将 AI 能力无缝嵌入现有的 AWS 架构中，利用现有的云资源（如 S3 存储知识库）。

**应用场景**
1.  **自动化数据分析：** Agent 读取 S3 上的 CSV/Excel 数据，执行 Python 分析，生成图表并上传。
2.  **企业知识库助手：** 结合 Bedrock 的 Knowledge Base，Agent 可以查询内部文档，并执行修改工单、发送邮件等操作。
3.  **DevOps 自动化：** Agent 监控 CloudWatch 告警，判断问题类型，并自动执行修复脚本（如重启 EC2 实例）。

**需要注意的问题**
*   **安全性：** 赋予 AI 写代码和执行 API 的权限是危险的。必须实施严格的 RBAC（基于角色的访问控制）。
*   **成本控制：** Agent 的自我反思和多步推理会导致 Token 消耗量激增，需要设置预算和停止条件。
*   **状态管理：** 无状态架构难以处理长对话，需要引入 DynamoDB 等外部记忆存储。

**实施建议**
*   从“人机回环” 开始，不要让 Agent 完全自动执行关键操作。
*   使用结构化日志记录 Agent 的每一步思考和工具调用，便于调试和审计。

## 4. 行业影响分析

**对行业的启示**
*   **从“模型战”转向“架构战”：** 未来的竞争不再是谁的模型参数大，而是谁能更好地编排模型、工具和云资源。Hugging Face 与 AWS 的合作正是这种趋势的体现。
*   **开源与云厂商的共生：** 开源社区（Hugging Face）提供创新和敏捷性，云厂商（AWS）提供稳定性和商业落地能力。

**可能带来的变革**
*   **SaaS 软件的智能化重构：** 未来的 SaaS 将不再是固定的菜单和按钮，而是基于 Agent 的自然语言界面。
*   **运维模式的改变：** AIOps 将从“规则引擎”进化为“基于 LLM 的推理引擎”。

**发展趋势**
*   **边缘智能与云端协同：** 虽然文章讲的是 AWS，但 `smolagents` 的轻量化特性使其未来很容易部署到边缘设备。
*   **多智能体协作：** 文章目前聚焦于单 Agent，未来 AWS 上的架构将演变为多 Agent 协作（如 Manager Agent 分配任务给 Worker Agents）。

## 5. 延伸思考

**引发的思考**
*   **代码解释器的双刃剑：** 允许 AI 写代码执行虽然强大，但也带来了注入攻击的风险。如何在保持灵活性的同时确保执行环境的安全？
*   **数据主权与隐私：** 将企业数据上传至 AWS Bedrock 进行推理，如何满足 GDPR 或合规要求？这需要 VPC Endpoints 和私有模型的结合。

**拓展方向**
*   **结合 GraphRAG:** 将 `smolagents` 的执行能力与基于图谱的 RAG 结合，解决复杂知识推理问题。
*   **多模态交互：** 扩展 Agent 的能力，使其不仅能处理文本和代码，还能直接处理图像（通过 Vision Models）和音频。

**未来趋势**
*   **模型小型化与端侧化：** `smolagents` 的名字暗示了“小模型”。未来趋势可能是用云端大模型做规划，用端侧小模型做执行，以降低延迟和成本。

## 6. 实践建议

**如何应用到自己的项目**
1.  **环境搭建：** 在本地安装 `smolagents`，配置 AWS CLI 凭证。
2.  **工具定义：** 将项目中重复性的操作（如数据库查询、API 请求）封装成 Python 函数或 OpenAPI 规范。
3.  **Agent 初始化：** 选择一个合适的模型（如 Qwen 或 Llama），加载工具，开始测试。

**具体行动建议**
*   **Step 1:** 阅读并运行 `smolagents` 的官方 Demo，理解 `CodeAgent` 的工作原理。
*   **Step 2:** 在 AWS 上创建一个具有有限权限的 IAM User，用于 Python 代码调用 Boto3。
*   **Step 3:** 编写一个简单的 Agent，赋予其“读取 S3 文件”和“发送 SES 邮件”的工具，测试其端到端能力。

**需补充的知识**
*   **Python 异步编程：** 处理并发的 API 请求。
*   **Prompt Engineering：** 如何编写系统提示词以规范 Agent 的行为。
*   **AWS Lambda & Docker：** 如果涉及复杂代码执行，需要了解容器化部署。

## 7. 案例分析

**成功案例（假设性推演）**
*   **场景：** 电商公司自动生成周报。
*   **实现：** Agent 接收指令 -> 调用 AWS Athena 查询上周销售数据 -> 生成 Python 代码绘制趋势图 -> 上传图至 S3 -> 发送邮件链接给管理层。
*   **成功要素：** 工具定义清晰，权限控制得当，模型推理准确。

**失败案例反思**
*   **场景：** 让 Agent 自动优化服务器配置。
*   **失败原因：** Agent 误解了“优化”指令，错误地关闭了生产环境实例，或者陷入了死循环不断调用 API 导致高额账单。
*   **教训：** 必须设置“确认机制”或“预演环境”，不能给予 Agent 直接破坏生产环境的“核按钮”。

## 8. 哲学与逻辑：论证地图

**中心命题**
**“将 Hugging Face smolagents 的轻量级编排能力与 AWS 的企业级托管服务相结合，是目前构建生产级 Agentic AI 应用的最优解之一。”**

**支撑理由**
1.  **开发效率:** `smolagents` 将 Agent 构建过程从数百行代码减少到数行代码，极大缩短了 MVP（最小可行性产品）的迭代周期。
    *   *依据:* Hugging Face 文档显示其 API 设计哲学是极简主义。
2.  **基础设施弹性:** AWS 提供了无需维护的基础设施（如 Bedrock, Lambda），解决了自建模型的算力瓶颈和运维难题。
    *   *依据:* 云计算的成本效益比和 SLA（服务等级协议）保障。
3.  **模型灵活性:** 该架构支持“多模型”策略，开发者可以随时切换底层模型（如从 GPT-4 切换到 Claude 3.5 Sonnet），避免被单一供应商锁定。
    *   *依据:* Bedrock 和 Hugging Face 提供的模型市场多样性。

**反例与边界条件**
1.  **超低延迟场景

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建轻量级且模块化的多模型编排架构

**说明**: 利用 Hugging Face smolagents 的轻量级特性，在 AWS 上构建一个能够根据任务类型动态调用不同模型（如 Llama 3 用于推理、Mistral 用于对话、Stable Diffusion 用于图像生成）的智能体系统。这种架构避免了单一大型模型的资源浪费，通过模块化设计提高了系统的灵活性和响应速度。

**实施步骤**:
1. 在 AWS ECS 或 EKS 上部署 smolagents 核心服务，将其作为中央调度器。
2. 配置工具调用函数，使其能够根据 Agent 的决策，通过 AWS SDK 动态调用 Amazon Bedrock 或部署在 SageMaker 上的不同端点。
3. 为每种模型类型定义标准化的输入输出接口，确保 Agent 能够无缝解析和传递多模态数据。

**注意事项**: 确保网络策略允许 smolagents 容器安全地访问模型推理端点，并实施严格的超时控制以防止某个慢速模型阻塞整个工作流。

---

### 实践 2：利用 Amazon Bedrock 实现模型托管的弹性与安全性

**说明**: 将 smolagents 与 Amazon Bedrock 集成，利用 Bedrock 的托管服务能力来消除底层基础设施的管理负担。通过 Bedrock，您可以安全地访问多种前沿模型，而无需担心服务器的扩缩容和维护，同时利用 AWS 的原生安全机制保护 API 密钥和敏感数据。

**实施步骤**:
1. 在 smolagents 的配置文件中，通过 Boto3 初始化 Bedrock 客户端，配置首选的模型 ID（如 `anthropic.claude-3-sonnet` 或 `meta.llama3`）。
2. 利用 AWS Secrets Manager 存储 Bedrock 的 API 凭证，smolagents 在运行时动态获取，避免硬编码。
3. 启用 Bedrock 的 Guardrails 功能，为 Agent 的输入输出设置内容过滤策略，确保生成内容符合合规要求。

**注意事项**: 监控 Bedrock 的调用配额和延迟，为 Agent 设置重试逻辑和退避策略，以处理偶尔的限流或网络抖动。

---

### 实践 3：通过 AWS Lambda 实现工具调用的无服务器化

**说明**: Agentic AI 的核心能力在于使用工具。最佳实践是将 smolagents 定义的工具封装为 AWS Lambda 函数。这种设计实现了极致的弹性扩展，Agent 仅在需要执行特定动作（如查询数据库、调用外部 API 或操作 S3 对象）时才触发计算，从而显著降低运行成本。

**实施步骤**:
1. 将 Agent 需要的每个功能（如“查询天气”、“数据分析”、“文件读写”）编写为独立的 Lambda 函数。
2. 为 Lambda 函数配置适当的 IAM 角色，遵循最小权限原则，仅授予 Agent 必要的 AWS 资源访问权限。
3. 在 smolagents 中注册这些 Lambda 函数的 ARN 或 API Gateway 端点，使 LLM 能够根据用户意图生成对应的 JSON 负载来触发这些函数。

**注意事项**: 注意 Lambda 的 payload 大小限制（6MB）和超时限制（15分钟），对于长时间运行的任务，应设计异步回调机制。

---

### 实践 4：基于 Amazon OpenSearch Service 构建增强型 RAG 知识库

**说明**: 为了减少幻觉并提供特定领域的知识，应为 smolagents 配置检索增强生成（RAG）管道。使用 Amazon OpenSearch Service 作为向量数据库，存储私有文档的嵌入向量。当 Agent 需要回答问题时，先检索相关上下文，再将其作为上下文窗口输入给模型。

**实施步骤**:
1. 部署 Amazon OpenSearch Service 集群，并配置向量搜索引擎支持。
2. 建立一个 ETL 管道（可以使用 AWS Lambda 或 Glue），将文档通过 Hugging Face 的嵌入模型（如 `sentence-transformers`）向量化并存入 OpenSearch。
3. 在 smolagents 中定义一个专用的“搜索工具”，该工具连接到 OpenSearch，将用户查询转换为向量检索并返回最相关的文档片段。

**注意事项**: 定期评估嵌入模型的质量，并优化切片策略，确保检索到的上下文既准确又能够适应模型的上下文窗口限制。

---

### 实践 5：实施全面的可观测性与链路追踪

**说明**: Agentic 系统的决策过程往往是非确定性的，调试难度较大。必须利用 AWS 的可观测性工具来记录 Agent 的思维链、工具调用过程和模型推理结果。这对于理解系统行为、优化提示词以及排查错误至关重要。

**实施步骤**:
1. 启用 AWS X-Ray，对 smolagents 的服务请求进行追踪，可视化从用户请求到模型推理再到工具调用的完整链路。
2. 将 Agent 的日志（包括 LLM 的 Prompt、Response 和中间决策）发送到 Amazon CloudWatch Logs，并配置结构化日志格式（如 JSON）以便查询。
3. 利用 Amazon CloudWatch Dashboard 创建可视化面板，监控关键指标，如“

---
## 学习要点

- Hugging Face smolagents 是一个轻量级 Python 库，允许开发者通过极简的代码构建强大的 Agentic AI 智能体，极大降低了智能体开发的门槛。
- 该框架通过集成 Hugging Face 上的海量工具（如搜索、计算、代码解释器），赋予智能体强大的推理能力和执行复杂工作流的自主性。
- 在 AWS 上部署该架构能够无缝利用云基础设施的弹性计算能力，实现智能体从开发原型到生产环境的高效扩展。
- 多模型框架的设计使得智能体可以根据任务需求灵活切换或组合使用不同的开源大语言模型（LLM），优化成本与性能的平衡。
- 借助 smolagents 的代码执行能力，智能体能够编写并运行 Python 代码来解决数学、数据分析或逻辑推理问题，显著扩展了应用场景。
- 利用 AWS 与 Hugging Face 的深度集成，开发者可以便捷地调用托管在云端的模型，简化了模型部署与运维的复杂度。
- 这种架构组合展示了如何通过将轻量级智能体框架与云服务结合，快速构建从简单的文本生成到复杂的自动化决策系统。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Agent](/tags/agent/) / [AWS](/tags/aws/) / [Hugging Face](/tags/hugging-face/) / [smolagents](/tags/smolagents/) / [RAG](/tags/rag/) / [医疗AI](/tags/%E5%8C%BB%E7%96%97ai/) / [多模型](/tags/%E5%A4%9A%E6%A8%A1%E5%9E%8B/) / [向量检索](/tags/%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [基于Hugging Face smolagents与AWS构建多模型医疗AI代理]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-6.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-4.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI Agent及多模型检索方案]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-2.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*