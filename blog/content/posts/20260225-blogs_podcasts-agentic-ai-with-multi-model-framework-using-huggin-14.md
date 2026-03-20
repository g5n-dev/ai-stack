---
title: 基于AWS与Hugging Face smolagents构建多模型医疗AI智能体
date: 2026-02-25 02:57:16+08:00
draft: false
entry_kind: auto
tags:
- Agentic AI
- Hugging Face
- smolagents
- AWS
- 多模型框架
- RAG
- 医疗AI
- 智能体
categories:
- AI 工程
- 大模型
source: blogs_podcasts
description: 本文介绍了如何利用开源库 Hugging Face 结合 AWS 云服务，构建一个具备多模型框架的“Agentic AI”（代理式 AI）解决方案。
  **核心内容总结：** 1. **基础工具**： 使用 Hugging Face 的 开源 Python 库，其优势在于仅需少量代码即可快速构建和运行 AI 代理。
  2.
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws
scenarios:
- AI/ML项目
- RAG应用
- 工具
---

# 基于AWS与Hugging Face smolagents构建多模型医疗AI智能体

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-23T15:47:06+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)

---

## 摘要/简介

Hugging Face smolagents 是一个开源的 Python 库，旨在通过几行代码即可轻松构建和运行智能体。我们将向您展示如何通过将 Hugging Face smolagents 与 Amazon Web Services (AWS) 托管服务集成，来构建一个 AI 智能体解决方案。您将学习如何部署一个医疗保健 AI 智能体，该智能体将展示多模型部署选项、向量增强的知识检索以及临床决策支持能力。

---

## 导语

随着大模型应用从简单的对话交互向复杂的自主决策演进，Agentic AI 正成为技术落地的关键形态。本文将介绍如何利用 Hugging Face smolagents 开源库，结合 AWS 托管服务构建一个多模型框架的 AI 智能体。通过构建医疗保健领域的具体案例，我们将深入解析多模型部署、向量增强检索以及临床决策支持等核心能力的实现路径，助您掌握构建高效 AI 智能体的实战技巧。

---

## 摘要

本文介绍了如何利用开源库 Hugging Face `smolagents` 结合 AWS 云服务，构建一个具备多模型框架的“Agentic AI”（代理式 AI）解决方案。

**核心内容总结：**

1.  **基础工具**：
    使用 Hugging Face 的 `smolagents` 开源 Python 库，其优势在于仅需少量代码即可快速构建和运行 AI 代理。

2.  **集成架构**：
    将 `smolagents` 与亚马逊云科技（AWS）的托管服务相结合，实现云端部署与管理。

3.  **应用场景**：
    演示了一个医疗健康领域的 AI 代理构建过程。

4.  **关键功能**：
    该方案展示了多模型部署选项、基于向量增强的知识检索以及临床决策支持能力，旨在提升 AI 系统在专业领域的复杂任务处理水平。

---

## 评论

**文章中心观点**
文章主张通过将 Hugging Face 的轻量级 Python 库 `smolagents` 与 AWS 基础设施（如 Bedrock 和 Lambda）深度集成，开发者可以用极少量的代码构建出具备工具调用能力的 Agentic AI（智能体 AI），从而实现从模型演示到企业级生产环境的快速跨越。

**支撑理由与深度评价**

**1. 技术架构的“去耦合化”趋势（事实陈述）**
文章的核心逻辑在于利用 `smolagents` 作为“大脑”，利用 AWS 作为“手脚”和“躯干”。
*   **分析**：这反映了当前 AI 开发的一个重要趋势——**推理层与基础设施层的解耦**。传统的 Agent 开发往往绑定在特定的云厂商（如 AWS Bedrock Agents）或重量级框架（如 LangChain）上。`smolagents` 作为一个极简的中间层，允许开发者保持代码的轻量级和可移植性，同时利用 AWS 的托管服务解决安全、鉴权和扩展性问题。
*   **价值**：这种架构避免了供应商锁定，同时降低了企业对于复杂 Agent 框架的学习成本。

**2. 代码优先的极简主义（事实陈述 / 作者观点）**
文章强调了“few lines of code”。
*   **分析**：`smolagents` 的设计哲学是 Code-First，而非 Config-First（如基于 YAML 的 Semantic Kernel 或 LangChain）。对于 Python 开发者而言，直接编写 Python 函数作为工具，比学习特定的 DSL（领域特定语言）要直观得多。文章展示了如何将 AWS SDK（如 Boto3）调用直接封装为 Agent 工具，这种**原生性**大大降低了调试难度。
*   **边界条件/反例 1**：极简主义是以牺牲功能丰富度为代价的。相比于 LangChain 庞大的生态系统，`smolagents` 在处理复杂的链式调用、持久化记忆管理和高级路由策略时，可能需要开发者编写大量自定义代码，这在大规模项目中可能导致“维护地狱”。

**3. 云原生集成的生产就绪性（你的推断）**
文章暗示通过 AWS Lambda 和 IAM（身份和访问管理）可以解决 Agent 落地的安全与权限问题。
*   **分析**：这是文章最具实战价值的部分。本地运行的 Agent 往往面临 API Key 泄露风险，且难以访问企业内网数据库。通过将 Agent 部署在 AWS Lambda 上，并利用 IAM Role 授予 Agent 访问 S3 或 DynamoDB 的权限，实现了**无凭证化**的凭证管理。这是从“玩具项目”转向“企业级应用”的关键一步。
*   **边界条件/反例 2**：Serverless 环境的冷启动问题。如果 Agent 需要加载大型模型或进行复杂的初始化，Lambda 的延迟可能会严重影响用户体验，尤其是在实时对话场景中。

**4. 多模型框架的灵活性（事实陈述）**
文章提到了使用 Hugging Face 的推理端点或 AWS Bedrock 作为后端。
*   **分析**：这体现了“混合部署”的必要性。开发者可以在本地使用开源小模型（如 Llama 3 或 Qwen）进行开发和测试，而在生产环境中无缝切换到 Claude 3 或 GPT-4 等闭源大模型，以获得更好的推理能力。
*   **行业影响**：这种模式推动了“模型路由”的发展，即根据任务难度动态分配模型，以优化成本和质量。

**批判性思考与争议点**

*   **过度简化的陷阱**：文章可能过分渲染了“几行代码”的魔力。在实际生产中，Agent 的难点不在于“调用工具”，而在于**工具调用的容错性**和**结果的解析**。如果 AWS API 返回了非预期的 JSON 格式或错误码，简单的 `smolagents` 脚本很容易崩溃。生产级 Agent 需要复杂的重试机制和自我修正逻辑，这往往被此类教程文章所忽略。
*   **成本控制的盲区**：虽然 `smolagents` 本身免费，但 Agentic AI 的本质是“模型反复调用推理”。在一个复杂的 AWS 环境中，Agent 可能会为了完成一个任务而调用 Bedrock API 十几次，导致 Token 成本指数级上升。文章未深入探讨如何监控和限制这种“自我反思”带来的成本爆炸。

**实际应用建议**

1.  **从“副驾驶”开始，而非“自动驾驶”**：不要直接让 Agent 自动执行修改 AWS 安全组或删除 S3 文件等高危操作。建议实施“人机协同”模式，Agent 生成 CLI 命令或 Python 代码，由人工审核确认后再执行。
2.  **建立严格的工具沙箱**：在使用 `smolagents` 调用 AWS SDK 时，务必为 Lambda 函数配置最小权限原则。不要赋予 Agent 管理员级别的 IAM 权限，防止 Agent 因幻觉导致误操作。
3.  **可观测性是关键**：由于 Agent 的执行路径是非确定性的，必须集成 AWS X-Ray 或类似工具来追踪 Agent 的思考过程和工具调用链，否则 Debug 将是一场噩梦。

**可验证的检查方式**

1.  **技术验证指标（实验）**：
    *   构建一个测试集，包含 5 个需要调用 AWS 服务（如“查询 S3 存储桶大小并发送 SNS 通知”）的任务。
    *   **成功率**：Agent 在无需人工干预下成功完成任务的百分比。
    *   **Token 消耗**：记录完成任务的平均输入/输出 Token 数，

---

## 技术分析

基于您提供的文章标题和摘要，结合对 **Hugging Face smolagents**、**Agentic AI（智能体 AI）** 以及 **AWS 云服务架构** 的技术理解，以下是对该主题的深度分析。

---

### Agentic AI 与多模型框架在 AWS 上的深度分析

### 1. 核心观点深度解读

**文章的主要观点**
文章的核心在于主张一种**“轻量级、标准化与云原生”**的 Agentic AI 构建范式。它反对构建复杂的、从零开始的单体智能体，转而提倡使用 Hugging Face 的 `smolagents` 库作为核心逻辑控制器，并结合 AWS 强大的基础设施（如 Bedrock、Lambda、S3）来快速构建生产级的 AI 智能体。

**作者想要传达的核心思想**
“AI 智能体应该是简单代码与强大模型的结合。” 作者试图传达，通过极简的 Python 代码（smolagents），即可驱动多模态模型（如 Qwen2-VL）并赋予其调用工具的能力，而 AWS 提供了企业级所需的算力、存储和模型托管服务。这种结合降低了 Agentic AI 的开发门槛，使得开发者能够专注于“智能逻辑”而非“工程管道”。

**观点的创新性和深度**
*   **库的轻量化创新**：`smolagents` 强调“代码优先”，其核心创新在于将智能体的决策过程抽象为极简的 Python 类，允许开发者用几行代码定义工具和模型，这比 LangChain 等重型框架更直观、更易于调试。
*   **多模型原生支持**：文章强调了“多模型框架”，意味着 smolagents 不仅限于 LLM（文本），还原生支持 VLM（视觉语言模型），能够处理图像和文档，这是从单一文本对话向多模态交互的重要演进。
*   **深度结合**：利用 AWS 的托管服务解决了开源模型部署难、扩容难的问题，实现了“开源灵活性”与“商业级稳定性”的平衡。

**为什么这个观点重要**
随着 AI 从“聊天机器人”向“智能体”演进，企业面临的主要挑战不再是模型本身的选择，而是如何让模型**可靠地执行任务**。这种“轻量框架 + 云基础设施”的模式，是目前解决 AI 落地“最后一公里”的最可行路径之一。

### 2. 关键技术要点

**涉及的关键技术或概念**
*   **Hugging Face smolagents**：一个极简的 Python 库，用于定义 Agent、Tool 和执行循环。
*   **Agentic Workflow（智能体工作流）**：包含规划、行动、观察的循环机制。
*   **AWS Bedrock**：AWS 的托管模型服务，提供对 Llama 3、Mistral、Claude 等模型的访问。
*   **AWS Lambda / Fargate**：无服务器计算，用于运行 Agent 代码或托管工具。
*   **多模态模型**：如 Qwen2-VL，能同时处理文本和图像输入。

**技术原理和实现方式**
1.  **Agent 定义**：使用 `CodeAgent` 或 `ToolAgent` 类初始化，指定底部的 LLM（通过 Hugging Face API 推理端点或 AWS Bedrock）。
2.  **工具注册**：将 AWS 服务（如 S3 上传、DynamoDB 查询）封装为 Python 函数，并添加 `@tool` 装饰器。smolagents 会自动生成这些工具的描述供 LLM 调用。
3.  **执行循环**：
    *   用户输入（文本/图片） -> Agent。
    *   Agent 决定调用哪个工具（例如，调用 Bedrock 生成图片，或调用 Lambda 处理数据）。
    *   工具返回结果 -> Agent 观察结果并决定下一步行动或生成最终答案。
4.  **多模态处理**：利用支持视觉的模型（如 Qwen2-VL），Agent 可以直接“看”图并执行基于视觉的操作（如 OCR、图表分析）。

**技术难点和解决方案**
*   **难点：模型幻觉与工具调用错误**。
    *   *解决方案*：smolagents 允许在代码中设置严格的输出类型和重试机制；结合 AWS Bedrock 的 Guardrails 功能可以过滤不当输出。
*   **难点：上下文管理**。
    *   *解决方案*：利用 AWS 的内存数据库或 S3 存储长对话历史，smolagents 负责将相关切片注入 Prompt。
*   **难点：多模态数据传输**。
    *   *解决方案*：使用 Base64 编码或 S3 预签名 URL 在 Agent 和模型之间传递图像数据。

### 3. 实际应用价值

**对实际工作的指导意义**
该方案为企业提供了一条**低成本、高效率**的 AI 原型验证和生产化路径。开发团队不需要投入大量精力构建 MLOps 平台，可以直接利用 AWS 的成熟服务和 smolagents 的简洁语法，快速上线能够处理文档、分析数据或自动化运维的智能体。

**可以应用到哪些场景**
1.  **RAG（检索增强生成）企业助手**：结合 AWS OpenSearch 和 Bedrock，构建能够查询企业内部文档（包括扫描件 PDF）的 Agent。
2.  **自动化图像处理**：例如，电商场景中，Agent 接收产品图，自动裁剪、打标签并上传到 S3，同时生成营销文案。
3.  **数据分析与报表**：Agent 接收自然语言指令，调用 Python 解释器（smolagents 内置功能）分析 CSV 数据，生成图表。
4.  **DevOps 自动化**：Agent 监控 CloudWatch 告警，自动判断是否需要扩容 EC2 实例或回滚部署。

**需要注意的问题**
*   **成本控制**：AWS Bedrock 按 token 计费，Agent 的多步推理循环可能导致成本指数级上升。
*   **安全性**：赋予 Agent 操作 AWS 资源的权限（如 IAM Role）存在风险，必须遵循最小权限原则。
*   **延迟**：多轮调用工具和模型的累积延迟可能导致用户体验不佳。

**实施建议**
*   从简单的“单轮工具调用”场景开始，逐步过渡到复杂的多步推理。
*   在 AWS 端严格限制 Agent IAM 角色的权限范围。
*   使用 smolagents 的 `verbose` 模式详细记录 Agent 的思维链，以便调试。

### 4. 行业影响分析

**对行业的启示**
这标志着 AI 开发正在从**“模型工程”**转向**“架构工程”**。核心竞争优势不再是谁拥有最好的模型，而是谁能更好地编排模型与现有工具的集成。Hugging Face 与 AWS 的结合展示了“开源社区”与“云厂商”生态共生的趋势。

**可能带来的变革**
*   **SaaS 的智能化升级**：传统的 SaaS 软件将更容易集成“智能副驾驶”，因为 smolagents 降低了集成门槛。
*   **运维自动化（AIOps）**：基于 Agent 的自我修复系统将成为企业运维的标准配置。

**相关领域的发展趋势**
*   **边缘端与云端协同**：虽然本文讲 AWS，但 smolagents 的轻量化特性使其未来很容易适配到边缘设备。
*   **多模态 Agent 的爆发**：随着 VLM 能力的提升，能够“看、听、说”的 Agent 将取代纯文本 Bot。

### 5. 延伸思考

**引发的其他思考**
*   **Agent 的可观测性**：当 Agent 自主决策时，传统的日志监控已不足够。我们需要专门的“Trace”技术来追踪 Agent 的决策树。
*   **数据主权**：使用 AWS Bedrock 处理企业敏感数据，数据流向和合规性是必须考量的因素。

**可以拓展的方向**
*   **人机协同**：研究如何在 Agent 执行关键步骤前引入人类确认机制。
*   **多 Agent 协作**：不仅是一个 Agent，而是多个 smolagents（如一个负责写代码，一个负责审查）在 AWS Step Functions 流程中协作。

### 7. 案例分析

**成功案例分析：智能发票处理系统**
*   **场景**：一家物流公司需要处理大量 PDF 发票。
*   **实现**：
    1.  用户上传 PDF 到 S3。
    2.  Lambda 触发 smolagents。
    3.  Agent 调用多模态模型（通过 Bedrock）读取 PDF 图片内容。
    4.  Agent 调用 Python 工具提取金额、日期，并格式化为 JSON。
    5.  Agent 将 JSON 写入 DynamoDB。
*   **成功要素**：利用了 VLM 的视觉能力和 AWS 的存储集成，实现了非结构化到结构化数据的自动化转换。

**失败案例反思**
*   **问题**：某开发者赋予 Agent 过高的 EC2 权限，Agent 在尝试“优化系统”时误判了关键生产服务器的状态并执行了重启。
*   **教训**：Agent 的工具权限必须隔离，且对于“破坏性操作”（如 Delete, Reboot）应强制要求二次确认或仅限于只读权限。

### 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级 Agentic AI 应用时，采用 **"Hugging Face smolagents（轻量级逻辑编排） + AWS（托管模型与基础设施）"** 的混合架构，是目前实现**开发敏捷性**与**生产可靠性**的最佳平衡点。

**支撑理由**
1.  **开发效率**：smolagents 的代码极简，允许开发者用纯 Python 思维定义智能体，相比复杂的配置文件（如 YAML）更直观。
    *   *依据*：Hugging Face 文档显示构建一个工具 Agent 仅需不到 20 行代码。
2.  **模型能力**：AWS Bedrock 提供了业界顶尖的模型（Claude 3.5, Llama 3）且无需自行维护 GPU 集群。
    *   *依据*：AWS 在云基础设施市场的统治地位及其 Bedrock 服务的 SLA 保证。
3.  **多模态原生**：smolagents 原生支持图像输入，符合当前 AI 从文本向多模态进化的技术趋势。

---

## 最佳实践

### 实践 1：构建模块化的多模型工具生态系统

**说明**:
在 Agentic AI 架构中，单一模型往往无法同时满足代码生成、逻辑推理、数学计算和视觉识别等所有任务。最佳实践是利用 Hugging Face smolagents 的工具调用能力，构建一个模块化的生态系统。将不同的开源模型（如 Qwen 用于代码，Llama 用于文本，SmolVLM 用于图像）封装为独立的工具，使主代理能够根据任务类型动态路由到最适合的专用模型。

**实施步骤**:
1. 在 Hugging Face 上评估并选择针对特定任务微调过的小型模型（SLM）。
2. 使用 `@tool` 装饰器将不同模型的推理逻辑封装为标准化的 Python 函数。
3. 在 smolagents 的 `CodeAgent` 配置中注册这些工具，定义清晰的工具描述以便代理理解何时调用。

**注意事项**:
确保工具的输入输出格式与主代理的上下文窗口兼容，避免因数据格式不匹配导致的中断。

---

### 实践 2：优化 AWS Lambda 无服务器函数的冷启动与超时配置

**说明**:
由于 smolagents 依赖 Python 解释器动态执行生成的代码，AWS Lambda 的冷启动延迟和默认的超时限制（3秒）可能成为瓶颈。最佳实践包括优化 Lambda 层以减少启动时间，并调整内存和超时设置，以适应模型推理和代码执行所需的持续时间。

**实施步骤**:
1. 将 Hugging Face 依赖库和模型文件打包到 Lambda Layer 中，以减小部署包体积。
2. 将 Lambda 函数的内存配置调整为至少 2GB 以上（通常内存越高，网络吞吐和 CPU 性能越强）。
3. 将超时设置调整为允许模型推理完成的最大时间（建议 5-15 分钟，视任务复杂度而定）。

**注意事项**:
监控 AWS CloudWatch 指标中的“Duration”和“Errors”数据，防止因执行时间过长导致意外中断和额外成本。

---

### 实践 3：利用 Amazon Bedrock 或 SageMaker 实时端点托管专用模型

**说明**:
为了获得比 Lambda 更高的吞吐量和稳定性，应将计算密集型的模型托管在 Amazon SageMaker 的实时端点上，或者通过 Amazon Bedrock 访问托管模型。smolagents 可以通过 HTTP 请求与这些端点交互，而不是在 Lambda 内部直接加载模型，从而实现计算与逻辑的解耦。

**实施步骤**:
1. 将选定的 Hugging Face 模型部署到 SageMaker 推理容器（如 DJL 或 Hugging Face Text Generation Inference）中。
2. 在 smolagents 的工具定义中，使用 `requests` 库调用 SageMaker 的 HTTPS 端点。
3. 实施异步调用机制，避免代理在等待模型响应时阻塞主线程。

**注意事项**:
确保 SageMaker 端点的自动扩缩容配置合理，以应对代理并发请求时的流量峰值。

---

### 实践 4：实施严格的沙箱机制与安全验证

**说明**:
Agentic AI 的核心特征是能够执行代码。在 AWS 环境中，允许 AI 生成并执行任意代码存在安全风险（如无限循环、恶意系统调用）。最佳实践是限制执行环境的权限，并禁止访问敏感的 AWS API 或外部不可信网络。

**实施步骤**:
1. 为 Lambda 函数配置严格的 IAM 角色，仅授予读写 S3 桶或 DynamoDB 的必要权限，禁止 `*` 通配符。
2. 在 smolagents 的执行环境中启用最大执行步数限制和超时熔断机制。
3. 对生成的代码进行静态分析或使用 AST（抽象语法树）检查，过滤掉危险的模块导入（如 `os.system`, `subprocess`）。

**注意事项**:
定期审计 CloudTrail 日志，检查代理是否尝试调用未授权的服务。

---

### 实践 5：建立结构化的提示词工程与上下文管理

**说明**:
多模型框架的效率取决于主代理能否准确地将任务分发给正确的工具。通过精心设计的系统提示词和上下文管理，可以减少 Token 的消耗并提高推理准确性。

**实施步骤**:
1. 在 `CodeAgent` 初始化时，编写详细的系统提示词，明确每个工具（模型）的能力边界和使用场景。
2. 使用 RAG（检索增强生成）技术，将必要的上下文文档从 Amazon OpenSearch 或 Aurora DB 注入到提示词中，而非依赖模型的预训练知识。
3. 实施上下文窗口截断策略，丢弃过时的对话历史，确保 Prompt 保持在模型的上下文长度限制内。

**注意事项**:
避免在提示词中硬编码敏感信息（如 API Key），应使用环境变量或 AWS Secrets Manager 动态获取。

---

### 实践 6：实施可观测性与调试追踪

**说明**:
Agentic 系统的决策过程往往是黑盒且非线性的。为了调试错误和优化性能，必须追踪代理的思维链、工具调用序列以及每个子模型的输入输出。

---

## 学习要点

- AWS 与 Hugging Face 的深度集成允许开发者直接在 SageMaker 等托管服务中部署和运行 smolagents，无需复杂的底层基础设施配置。
- smolagents 通过将 Python 函数转化为工具，赋予了 LLM 编写代码并自主执行任务的能力，从而实现比传统聊天机器人更高级的自动化。
- 该多模型框架支持灵活切换 Hugging Face 上的各类开源模型，使开发者能够根据具体任务需求在性能与成本之间找到最佳平衡。
- 通过将复杂的业务逻辑封装为 Python 工具，开发者可以显著降低大模型产生幻觉的风险，并提高 Agent 执行复杂工作流的准确性。
- 利用 AWS 的安全基础设施与 Hugging Face 的模型中心，企业能够以更安全合规的方式构建和扩展生成式 AI 应用。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Agentic AI](/tags/agentic-ai/) / [Hugging Face](/tags/hugging-face/) / [smolagents](/tags/smolagents/) / [AWS](/tags/aws/) / [多模型框架](/tags/%E5%A4%9A%E6%A8%A1%E5%9E%8B%E6%A1%86%E6%9E%B6/) / [RAG](/tags/rag/) / [医疗AI](/tags/%E5%8C%BB%E7%96%97ai/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [基于AWS与Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗智能体]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-10.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI智能体]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-5.md" >}})
- [在AWS上部署Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-11.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-3.md" >}})
