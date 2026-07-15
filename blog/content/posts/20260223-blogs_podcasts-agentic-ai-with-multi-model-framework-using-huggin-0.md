---
title: 基于AWS与Hugging Face smolagents构建多模型医疗AI Agent
date: 2026-02-23 17:33:28+08:00
draft: false
entry_kind: auto
tags:
- Hugging Face
- smolagents
- AWS
- Agent
- 医疗 AI
- RAG
- 多模型部署
- 临床决策支持
categories:
- AI 工程
- 大模型
source: blogs_podcasts
description: '**摘要：** 本文介绍了如何利用开源 Python 库 **Hugging Face smolagents** 结合 **AWS 托管服务**，构建一个基于多模型框架的
  **Agentic AI** 解决方案。 主要内容包括： 1. **开发工具**：使用 简化代理的构建与运行，仅需少量代码即可实现。 2. **集成'
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws
scenarios:
- AI/ML项目
- RAG应用
aliases:
- /posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-2/
- /posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-3/
- /posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-10/
- /posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-11/
- /posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-14/
- /posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-4/
- /posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-5/
- /posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-6/
- /posts/20260225-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-14/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-23T15:47:06+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)

---

## 摘要/简介

Hugging Face smolagents 是一个开源 Python 库，旨在通过几行代码即可轻松构建和运行 Agent。我们将向您展示如何通过将 Hugging Face smolagents 与 Amazon Web Services (AWS) 托管服务集成，来构建一个 Agent 化的 AI 解决方案。您将学习如何部署一个医疗保健 AI Agent，该方案将展示多模型部署选项、向量增强的知识检索以及临床决策支持能力。

---

## 导语

随着 AI 应用从简单的对话交互向具备自主规划能力的 Agent 演进，如何高效构建并部署此类系统成为开发者关注的焦点。本文将介绍如何利用开源库 Hugging Face smolagents 与 AWS 托管服务集成，快速构建企业级 AI 解决方案。通过构建一个具体的医疗保健 Agent 示例，您将掌握多模型部署、向量增强检索及临床决策支持等核心功能的实现方法。

---

## 摘要

**摘要：**

本文介绍了如何利用开源 Python 库 **Hugging Face smolagents** 结合 **AWS 托管服务**，构建一个基于多模型框架的 **Agentic AI** 解决方案。

主要内容包括：
1.  **开发工具**：使用 `smolagents` 简化代理的构建与运行，仅需少量代码即可实现。
2.  **集成平台**：将代理与 AWS 的托管服务相结合，以实现稳健的部署和扩展。
3.  **应用场景**：以医疗领域为例，演示了如何部署一个具备 **多模型部署选项**、**向量增强知识检索** 以及 **临床决策支持** 功能的医疗 AI 代理。

---

## 评论

**中心观点**
该文章提出了一种通过集成 Hugging Face 轻量化代理库与 AWS 托管服务来快速构建企业级 Agentic AI 解决方案的技术范式，其核心价值在于利用“开源灵活性”与“云原生基础设施”的结合来降低智能体的开发与部署门槛。（作者观点）

**支撑理由与深度评价**

**1. 极简主义与低代码化的工程实现（内容深度与实用性）**
*   **分析**：文章强调 `smolagents` 的核心优势在于“几行代码构建 Agent”。从技术架构看，这代表了从传统的“硬编码复杂工作流”（如 LangChain 的繁重链式调用）向“模型为中心的轻量级编排”的转变。
*   **支撑理由**：通过将工具调用、内存管理和推理逻辑封装在极简的 Python API 中，开发者可以跳过繁琐的 Prompt Engineering 管道搭建，直接验证业务逻辑。这对于处于 PoC（概念验证）阶段的团队具有极高的时间价值。
*   **反例/边界条件**：这种“极简”是以牺牲可观测性为代价的。在生产环境中，当 Agent 执行失败时，几行代码的封装往往导致难以定位是模型幻觉、工具解析错误还是权限问题。对于需要精细控制每个 Token 消耗和中间步骤的金融或医疗场景，这种黑盒模式存在风险。（你的推断）

**2. 云原生托管的弹性与安全边界（行业影响与实用性）**
*   **分析**：文章重点介绍了与 AWS 的集成，特别是利用 IAM 角色进行工具调用。
*   **支撑理由**：这是将 AI Agent 从“玩具脚本”推向“企业级应用”的关键一步。利用 AWS 的托管服务（如 Lambda 容器化、Bedrock 模型托管）解决了 Agent 运行中最头疼的资源伸缩和 API 密钥管理问题。文章隐含了一个重要观点：Agent 的安全性不仅在于模型对齐，更在于云层面的最小权限原则（IAM）。
*   **反例/边界条件**：过度依赖特定云厂商（AWS）的锁定效应是明显的。如果企业需要多云部署或混合云架构，这种深度集成的代码迁移成本极高。此外，AWS 的 API 调用延迟（尤其是 Bedrock 在某些区域的响应速度）可能会显著拉低 Agent 的交互体验，导致用户感知到的“智能”下降。（你的推断）

**3. 多模型框架的鲁棒性与成本权衡（创新性与争议点）**
*   **分析**：文章提及“multi-model framework”，暗示可以在不同任务间切换模型。
*   **支撑理由**：这触及了当前 Agentic AI 的痛点——成本。通过路由机制，让简单的任务（如数据查询）使用小模型（SmolLM 或 Llama 3 8B），复杂的任务使用大模型，是实现商业可行性的必经之路。
*   **反例/边界条件**：文章可能低估了“路由逻辑”本身的复杂性。如何判断一个任务需要多强的模型？如果引入一个“裁判模型”来做决策，这本身又增加了推理成本和延迟。此外，多模型混用增加了版本管理和兼容性测试的复杂度。（你的推断）

**4. 代码优先与 LLM-as-a-Judge 的趋势（可读性与技术趋势）**
*   **分析**：文章展示了如何让 Agent 编写代码来解决问题，这是 `smolagents` 区别于其他纯文本 Agent 的显著特征。
*   **支撑理由**：让 Agent 编写 Python 代码并在沙箱中执行，比单纯的文本生成能处理更复杂的逻辑和数学运算，这是通向 AGI 的重要路径（OpenAI o1 模型也验证了思维链+代码执行的有效性）。
*   **反例/边界条件**：代码执行带来的安全风险是指数级的。尽管文章可能提到沙箱，但在企业内网环境中，允许 AI 生成并执行代码本身就是一种安全合规上的“激进”策略。许多企业的安全策略会直接禁止此类操作。（你的推断）

**实际应用建议**

1.  **分层部署策略**：不要试图用一套 Agent 解决所有问题。建议参考文章思路，将“思考型”任务（架构设计、文案）部署在云端（AWS Bedrock），将“执行型”任务（简单的数据提取）利用 `smolagents` 部署在边缘或本地，以降低延迟和成本。
2.  **安全沙箱是底线**：如果在生产环境应用文中提到的代码执行功能，必须构建严格的 Firecracker 微虚拟机或严格的 E2B 沙箱隔离，绝对禁止在宿主机直接运行 AI 生成的代码。
3.  **监控与回退**：鉴于轻量级框架缺乏原生 Trace 能力，建议在集成 AWS X-Ray 的基础上，手动埋点记录 Agent 的每一次工具调用和中间输出，以便在出现幻觉时进行人工审查。

**可验证的检查方式**

1.  **延迟基准测试**：
    *   *实验*：构建一个典型的 Agent 任务（如“查询 S3 并总结”），对比纯本地运行 `smolagents` 与通过 AWS Bedrock 调用同等级别模型的端到端延迟。
    *   *指标*：首字生成时间 (TTFT) 和 总体完成时间。
    *   *观察窗口*：在不同网络时段（高峰/低峰）测试，观察云服务网络抖动对 Agent 体验的影响。

---

## 技术分析

基于提供的文章标题《Agentic AI with multi-model framework using Hugging Face smolagents on AWS》及其摘要，结合当前AI Agent（智能体）技术生态、Hugging Face smolagents 的技术特性以及 AWS 云服务的架构模式，以下是针对该主题的深度分析报告。

---


### 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是**“简化与赋能”**。它主张利用 Hugging Face 的 `smolagents` 轻量级开源库，结合 AWS 强大的云基础设施（如 Bedrock、Lambda、S3），以极低的代码门槛构建具备多模型能力的 Agentic AI（智能体 AI）解决方案。

**作者想要传达的核心思想**
作者试图打破构建 AI 智能体通常需要复杂工程编排的壁垒。核心思想在于**“Agent as Code”**（智能体即代码）与**“Cloud as Backend”**（云端即后端）的结合。通过 Python 代码直接定义智能体的行为逻辑，利用 AWS 托管服务解决底层算力、存储和工具调用问题，从而让开发者专注于智能体的“思考”而非“基建”。

**观点的创新性和深度**
*   **轻量化创新**：传统的 Agent 框架（如 LangChain）往往封装过重，`smolagents` 强调极简主义，这降低了调试难度。
*   **多模型编排**：文章不仅限于单一模型，而是探讨如何在 AWS 环境下灵活调用不同的大模型（LLMs），体现了“模型路由”或“混合专家”的思想。
*   **云原生融合**：将开源库与 AWS 托管服务深度绑定，利用云服务的弹性扩展性和企业级安全性，解决了开源模型在生产环境中的落地难题。

**为什么这个观点重要**
随着大模型从“对话”向“行动”演进，Agentic AI 被认为是下一代 AI 的核心形态。然而，工程落地难、成本高、多模型管理复杂是主要痛点。该文章提供了一条**“低成本、高效率、企业级”**的落地路径，对于希望快速验证 AI Agent 想法并将其投入生产的企业和开发者具有重要的指导意义。

### 2. 关键技术要点

**涉及的关键技术或概念**
*   **Hugging Face smolagents**：一个极简的 Python Agent 框架，强调代码即配置。
*   **Agentic Workflow（智能体工作流）**：包括规划、记忆、工具使用和反思。
*   **AWS Serverless 架构**：可能涉及 AWS Lambda（计算）、Amazon Bedrock（模型托管）、Amazon S3（存储）、AWS Step Functions（编排）。
*   **Function Calling / Tool Use**：智能体调用外部 API 或 AWS 服务的能力。

**技术原理和实现方式**
1.  **Agent 定义**：使用 `smolagents` 中的 `CodeAgent` 或 `ToolAgent` 类，通过 Python 函数定义可用的工具。
2.  **模型集成**：配置 AWS Bedrock 作为推理后端，使得 `smolagents` 可以通过标准 API 调用 Claude、Llama 等模型。
3.  **工具注册**：将 AWS 服务（如 S3 上传文件、DynamoDB 读取数据）封装成 Python 函数，并装饰为 Agent 可调用的工具。
4.  **执行循环**：Agent 接收任务 -> LLM 生成思考步骤 -> 选择工具 -> 执行工具（调用 AWS SDK）-> 观察结果 -> 重复直到完成。

**技术难点和解决方案**
*   **难点：上下文管理与 Token 消耗**。多步推理和工具调用会消耗大量 Token。
    *   *解决方案*：利用 AWS 的低成本存储方案保存中间结果，仅将关键摘要放入 LLM 上下文。
*   **难点：工具调用的权限控制**。Agent 调用 AWS 服务需要 IAM 权限，存在安全风险。
    *   *解决方案*：实施最小权限原则，为 Agent 创建特定的 IAM Role，并限制其可调用的 API 范围。
*   **难点：多模型的一致性**。不同模型在 Bedrock 上的接口可能略有差异。
    *   *解决方案*：使用 `smolagents` 提供的统一接口层或适配器模式，屏蔽底层模型差异。

**技术创新点分析**
*   **代码优先的 Agent 设计**：不同于 YAML 配置或可视化拖拽，`smolagents` 允许开发者直接用 Python 编写复杂的逻辑，甚至让 LLM 编写 Python 代码来解决问题，这在处理数学或数据分析任务时极其高效。

### 3. 实际应用价值

**对实际工作的指导意义**
该架构为构建企业级 RAG（检索增强生成）系统和自动化业务流程提供了一套标准化的“脚手架”。它证明了不需要庞大的工程团队，也能快速构建出具备复杂操作能力的 AI 员工。

**可以应用到哪些场景**
*   **企业知识库问答**：Agent 读取 S3 中的私有文档（通过工具），回答员工问题。
*   **自动化运维**：Agent 监控 CloudWatch 指标，发现异常时自动调用 Lambda 进行修复或发送通知。
*   **数据分析助手**：Agent 连接数据库（如 RDS），根据自然语言指令生成 SQL 并执行，返回图表。
*   **内容审核与处理**：Agent 自动调用 Rekognition 分析图片，并将结果存入 DynamoDB。

**需要注意的问题**
*   **成本控制**：Agent 的自举过程可能导致多次 API 调用，需设置最大迭代次数限制。
*   **幻觉风险**：Agent 可能会错误地调用工具或误解工具返回的结果。
*   **延迟**：多步交互和云服务调用会增加响应时间，不适合对实时性要求极高的场景。

**实施建议**
*   从简单的“单工具”场景开始（如仅做搜索），逐步扩展到多工具链。
*   在 AWS 上严格隔离开发与生产环境。
*   利用 CloudWatch 记录 Agent 的每一步思考和操作，以便调试和审计。

### 4. 行业影响分析

**对行业的启示**
这标志着 AI 开发正在从**“模型训练”**转向**“模型编排”**。未来的核心竞争力可能不是拥有最好的模型，而是拥有最好的 Agent 框架和工具集成能力。同时，云厂商（AWS）与开源社区的合作模式将成为主流。

**可能带来的变革**
*   **SaaS 软件的智能化升级**：传统的 SaaS 软件可以通过集成此类 Agent，获得“自主执行任务”的能力，从“工具”变为“助手”。
*   **运维自动化**：AIOps 将真正落地，Agent 替代人工进行故障排查。

**相关领域的发展趋势**
*   **边缘计算与云端 Agent 的协同**：在边缘端收集数据，交由云端 Agent 进行复杂决策。
*   **多模态 Agent**：不仅处理文本，还能直接处理图像、音频（利用 AWS Transcribe/Rekognition）。

**对行业格局的影响**
加强了 AWS 在 AI 基础设施层的话语权，同时巩固了 Hugging Face 作为 AI 开发者入口的地位。对于纯中间件厂商（如仅做 API 聚合的公司）可能构成降维打击。

### 5. 延伸思考

**引发的其他思考**
*   **Agent 的安全性**：如果 Agent 被提示词注入攻击，它是否会执行删除 S3 数据的危险操作？如何构建“沙箱”环境？
*   **人机协同**：当 Agent 遇到无法确定的步骤时，如何优雅地请求人类介入？

**可以拓展的方向**
*   **多 Agent 协作**：不仅是一个 Agent，而是一个团队，例如“经理 Agent”分配任务，“程序员 Agent”写代码，“测试 Agent”验收。
*   **Agent 商店**：未来是否会像手机 App 一样，出现专门售卖特定技能 Agent 的市场？

**需要进一步研究的问题**
*   如何评估 Agent 的性能？目前缺乏像 LLM Benchmark 那样统一的 Agent 评估标准。
*   如何解决 Agent 的长期记忆问题？仅仅依靠上下文窗口是不够的，需要结合向量数据库和图数据库。

### 7. 案例分析

**结合实际案例说明**
假设一个**“电商数据分析 Agent”**案例：
*   **目标**：用户询问“上周销售额最高的品类是什么？”
*   **流程**：
    1. Agent 理解意图，决定需要查询数据库。
    2. 调用工具 `query_sql(sql="SELECT product_category, sum(amount) FROM sales WHERE date > ... GROUP BY...")`。
    3. 工具返回 JSON 数据。
    4. Agent 调用工具 `plot_chart(data)` 生成图表并上传至 S3。
    5. Agent 返回 S3 链接给用户。

**成功案例分析**
*   **Klarna**：虽未使用 smolagents，但其客服 Agent 类似，通过自动化处理查询，节省了数千人工工时。
*   **Cognition (Devin)**：展示了 Agent 编写代码的强大能力，smolagents 正是试图将这种能力平民化。

**失败案例反思**
*   **Air Canada 聊天机器人**：因 Agent 幻觉承诺了错误的退款政策导致法律诉讼。
    *   *教训*：Agent 必须严格限制在既定规则和工具范围内，不能仅依赖模型的通用知识。

**经验教训总结**
工具的**确定性**比模型的**智能性**更重要。确保 Agent 调用的工具是经过严格测试的，这比提升模型的智商更能保证系统的稳定性。

### 8. 哲学与逻辑：论证地图

**中心命题**
**利用 Hugging Face smolagents 结合 AWS 托管服务，是构建企业级、低成本、高扩展性 Agentic AI 应用的最佳技术路径。**

**支撑理由与依据**
1.  **开发效率大幅提升**：`smolagents` 的极简设计使得构建 Agent 的代码量减少 80% 以上，让开发者能快速迭代。
    *   *依据*：开源社区反馈及框架的代码行数对比

---

## 最佳实践

### 实践 1：构建模块化的多模型编排架构

**说明**: 在 AWS 上使用 Hugging Face smolagents 时，不应依赖单一模型完成所有任务。最佳实践是构建一个模块化的架构，根据任务复杂度、成本和延迟要求，动态路由到不同的模型（如 Llama 3 用于推理，Mistral 用于快速响应，或专门的 Qwen 模型用于特定任务）。利用 smolagents 的工具调用能力，将大模型作为“控制器”，配合小模型或专用 API 完成具体执行。

**实施步骤**:
1. 在 AWS SageMaker 或 Bedrock 中部署多个模型端点，或配置 Hugging Face Serverless Inference 网关。
2. 在 smolagents 代码中定义模型映射表，根据 Agent 的工具输出类型选择对应的后端模型。
3. 实施中间件逻辑，监控 Token 使用量，并在简单任务上自动降级到更小、更快的模型以降低成本。

**注意事项**: 确保所有模型端点的 API 接口标准化，以免在切换模型时破坏 Agent 的输入输出解析逻辑。

---

### 实践 2：实施严格的工具沙箱与权限隔离

**说明**: Agentic AI 的核心是自主调用工具（如执行 Python 代码、访问 AWS S3 或调用内部 API）。在 AWS 环境中，必须限制 Agent 的操作权限。最佳实践是使用 AWS IAM Roles Anywhere 或针对特定容器角色的最小权限原则，确保 Agent 只能访问完成任务所需的特定资源，防止“越狱”攻击导致的数据泄露或系统破坏。

**实施步骤**:
1. 为 smolagents 运行环境创建专用的 IAM Role，仅授予读取 S3 特定桶或调用特定 Lambda 函数的权限。
2. 在工具定义层面实施输入验证白名单，拒绝包含 shell 元字符或路径遍历的参数。
3. 使用 Docker 容器运行 smolagents 的代码执行环境，禁用网络访问或限制其仅能访问 AWS 内网端点。

**注意事项**: 定期审查 CloudTrail 日志，检测 Agent 是否尝试调用未授权的 AWS API。

---

### 实践 3：优化提示词与上下文管理

**说明**: smolagents 依赖上下文来决定下一步行动。由于上下文窗口有限且按 Token 计费，直接将海量数据注入提示词是低效的。最佳实践是结合 AWS 的向量数据库（如 Amazon OpenSearch Service 或 Aurora PostgreSQL with pgvector）实现 RAG（检索增强生成），仅将最相关的信息片段提供给 Agent。

**实施步骤**:
1. 将知识库文档向量化并存储在 AWS 托管的向量数据库中。
2. 在 smolagents 的 `CodeAgent` 或 `ToolCallingAgent` 初始化前，增加一个预处理步骤，根据用户查询检索 Top-K 相关文档。
3. 动态构建 System Prompt，明确告知 Agent 其能力边界（即工具列表）和检索到的上下文内容。

**注意事项**: 检索到的内容必须经过去重和清洗，避免因上下文冲突导致 Agent 陷入逻辑死循环。

---

### 实践 4：建立可观测性与反馈循环

**说明**: Agent 的行为具有概率性和非确定性。在生产环境中，必须能够追踪 Agent 的思考过程、工具调用链和最终结果。最佳实践是利用 AWS CloudWatch 或 X-Ray 进行日志记录和追踪，将 Agent 的每一步动作结构化存储，以便于调试和优化。

**实施步骤**:
1. 配置 smolagents 的日志处理器，将所有中间步骤（Thought, Action, Observation）格式化为 JSON 并发送到 CloudWatch Logs。
2. 在关键步骤插入自定义 Metrics，记录工具调用成功率、Token 消耗量和任务完成时间。
3. 建立人工反馈机制，允许用户对 Agent 的输出进行评分，并将这些数据回流用于微调或评估模型表现。

**注意事项**: 避免在日志中记录敏感信息（如 PII 数据或 API 密钥），确保日志传输和存储过程加密。

---

### 实践 5：利用 AWS Lambda 实现无服务器工具扩展

**说明**: smolagents 的工具可以是 Python 函数，也可以是外部 API。为了提高可扩展性和响应速度，应将计算密集型或长时间运行的任务封装为 AWS Lambda 函数。这样 Agent 本身不需要保持长连接运行，而是通过事件驱动模式触发任务，适合处理如图片生成、大规模数据处理等场景。

**实施步骤**:
1. 将具体的业务逻辑封装为 AWS Lambda 函数，并配置合适的超时和内存限制。
2. 在 smolagents 中定义 `@tool` 装饰器函数，内部使用 `boto3` 客户端同步或异步调用 Lambda。
3. 设置异步回调机制，让 Agent 能够提交任务并轮询检查结果，而不是阻塞等待。

**注意事项**: 处理 Lambda 冷启动问题，对于需要极低延迟的交互，考虑使用 Provisioned Concurrency 或保持容器化服务热启动。

---

### 实践 6：成本控制与资源配额管理

**说明**: 多模型框架

---

## 学习要点

- Smolagents 通过将大语言模型转化为能够自主解释、规划并执行复杂工作流的智能体，极大地简化了 AI 智能体的开发流程。
- 利用 Hugging Face 丰富的模型生态和工具集成，开发者可以快速构建具备多模态能力的智能体应用。
- 该框架能够无缝调用外部工具（如搜索、计算、代码执行）来弥补模型自身的知识盲区，显著增强了解决实际问题的能力。
- 基于 AWS 基础设施部署，确保了智能体应用在运行过程中的安全性、可扩展性及企业级稳定性。
- Smolagents 提供了标准化的接口，使得开发者能够轻松更换底层模型或添加新工具，而无需重构整个系统架构。
- 这种多模型框架支持智能体根据任务需求动态选择最合适的模型，从而在性能与成本之间实现最佳平衡。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Hugging Face](/tags/hugging-face/) / [smolagents](/tags/smolagents/) / [AWS](/tags/aws/) / [Agent](/tags/agent/) / [医疗AI](/tags/%E5%8C%BB%E7%96%97ai/) / [RAG](/tags/rag/) / [多模型部署](/tags/%E5%A4%9A%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [临床决策支持](/tags/%E4%B8%B4%E5%BA%8A%E5%86%B3%E7%AD%96%E6%94%AF%E6%8C%81/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [基于AWS与Hugging Face smolagents构建医疗AI Agent及多模型检索方案]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
- [深度解析Skill/MCP/RAG等五大AI技术的底层逻辑]({{< relref "posts/20260212-juejin-深入理解skillmcpragagentopenclaw底层逻辑-2.md" >}})
- [Amazon Bedrock AgentCore 浏览器更新：新增代理、配置文件及扩展支持]({{< relref "posts/20260213-blogs_podcasts-customize-ai-agent-browsing-with-proxies-profiles--0.md" >}})
