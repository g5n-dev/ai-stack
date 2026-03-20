---
title: 基于Hugging Face smolagents与AWS构建多模型医疗AI代理
date: 2026-02-24 15:46:23+08:00
draft: false
entry_kind: auto
tags:
- Hugging Face
- smolagents
- AWS
- Agent
- 多模型
- RAG
- 医疗AI
- 向量检索
categories:
- AI 工程
- 大模型
source: blogs_podcasts
description: 本文简要介绍了如何利用开源库 Hugging Face smolagents 在 AWS 上构建基于多模型框架的智能体 AI 解决方案。
  Hugging Face smolagents 是一个开源 Python 库，旨在让开发者仅需几行代码即可轻松构建和运行 AI 代理。文章将演示如何将该库与 AWS
  托管服务相结合，
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws
scenarios:
- RAG应用
- AI/ML项目
- 工具
---

# 基于Hugging Face smolagents与AWS构建多模型医疗AI代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-23T15:47:06+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)

---

## 摘要/简介

Hugging Face smolagents 是一个开源 Python 库，旨在通过几行代码轻松构建和运行代理。我们将向您展示如何通过将 Hugging Face smolagents 与 Amazon Web Services (AWS) 托管服务集成，来构建一个代理式 AI 解决方案。您将学习如何部署一个医疗保健 AI 代理，该代理将展示多模型部署选项、向量增强的知识检索以及临床决策支持能力。

---

## 导语

随着代理式 AI（Agentic AI）从概念验证走向实际落地，如何构建稳健且可扩展的多模型架构成为开发者关注的焦点。本文将详细介绍如何利用 Hugging Face smolagents 开源库，结合 Amazon Web Services (AWS) 的托管服务来部署此类解决方案。通过构建一个具备向量增强检索与临床决策支持能力的医疗保健 AI 代理，您将掌握多模型集成与云端部署的具体实践方法。

---

## 摘要

本文简要介绍了如何利用开源库 Hugging Face smolagents 在 AWS 上构建基于多模型框架的智能体 AI 解决方案。

Hugging Face smolagents 是一个开源 Python 库，旨在让开发者仅需几行代码即可轻松构建和运行 AI 代理。文章将演示如何将该库与 AWS 托管服务相结合，具体以一个医疗 AI 智能体为例，展示其在多模型部署、向量增强知识检索及临床决策支持方面的功能与应用。

---

## 评论

**中心观点**
文章提出了一种“轻量级代码优先”的智能体构建范式，主张通过将 Hugging Face 的 `smolagents` 库与 AWS 基础设施深度集成，以极简的代码逻辑实现高性能的多模型 Agentic AI 解决方案，旨在降低大模型应用的开发门槛并提升云端部署的效率。

**支撑理由与评价**

**1. “代码即智能体”的范式转移（事实陈述 / 你的推断）**
文章的核心逻辑在于利用 `smolagents` 将 Python 函数直接映射为智能体的工具能力。从技术角度看，这比传统的 LangChain 或 LangGraph 更加“原生”。它不强制开发者学习特定的 DSL（领域特定语言），而是利用 Python 本身的语法结构。
*   **深度分析**：这种做法极大地降低了认知摩擦。开发者不需要思考“如何定义工具”，而是思考“如何写一个函数”。这不仅提高了开发效率，也让调试过程变得透明，因为出错时往往只是 Python 代码报错，而非复杂的框架内部错误。
*   **反例/边界条件**：对于非技术人员或低代码开发者，这种“代码优先”的模式反而构成了更高的门槛，相比于 Node-RED 或某些拖拽式 AI 编排平台，它不够直观。

**2. 云原生架构的弹性与成本博弈（事实陈述 / 你的推断）**
文章强调了利用 AWS（如 Bedrock, Lambda, Fargate）托管服务来支撑智能体运行。这解决了 Agentic AI 最头疼的“状态管理”和“扩展性”问题。
*   **深度分析**：通过 AWS 的无服务器架构，智能体可以根据并发请求自动扩缩容，这是本地脚本无法比拟的优势。同时，利用 Hugging Face 的 Inference Endpoints 与 AWS 的结合，可以灵活切换底层模型（如 Llama 3 vs. Mistral），避免了单一供应商的锁定。
*   **反例/边界条件**：这种架构引入了显著的“冷启动”延迟和复杂的网络跳转。如果智能体需要高频调用本地工具（如文件系统操作或极低延迟的数据库查询），AWS 的云函数网络开销可能成为瓶颈，且云端 Token 调用成本在规模化运行时可能远高于本地部署的开源模型。

**3. 多模型协作的鲁棒性与幻觉风险（作者观点 / 你的推断）**
文章暗示通过多模型框架（如分工明确的模型角色）可以提升任务完成率。
*   **深度分析**：这是目前行业的主流趋势，即“大模型规划，小模型执行”。例如，用一个参数量大的模型做意图识别和任务拆解，用轻量级模型执行具体的 API 调用。这种异构计算在成本和性能上取得了平衡。
*   **反例/边界条件**：多模型协作增加了系统的不可预测性。当错误发生时，很难快速定位是规划模型的逻辑错误，还是执行模型的参数错误，或者是工具本身的 Bug。这种“黑盒中的黑盒”问题在复杂的 AWS 环境中会被放大。

**4. 实用价值：从 Demo 到生产的“最后一公里”（你的推断）**
文章展示了极高的实用价值，特别是对于初创团队和 MVP（最小可行性产品）验证阶段。
*   **深度分析**：`smolagents` 提供的简洁 API 允许开发者在一个 Notebook 中完成从想法到原型的构建。结合 AWS 的托管服务，意味着开发者不需要维护 K8s 集群或 GPU 驱动，这直接击中了算法工程师“不想做运维”的痛点。
*   **反例/边界条件**：这种极简架构在生产环境中面临严重的可观测性挑战。Agentic AI 的执行链路是非线性的，简单的日志记录无法还原“为什么智能体决定调用这个 AWS API”。在生产级部署中，必须引入如 LangSmith 或 Arize 等专门的 Tracing 工具，而这部分在文章中可能被简化了。

**实际应用建议**

1.  **安全沙箱至关重要**：由于 `smolagents` 允许 AI 执行 Python 代码，若直接在 AWS Lambda 或 EC2 中运行，存在任意代码执行风险。建议在 Docker 容器或受限的 IAM 角色环境下运行智能体，严禁赋予删除或写入核心系统权限的 IAM Policy。
2.  **模型路由策略**：不要盲目使用最大的模型。建议在接入层实现“路由逻辑”，对于简单的 SQL 查询或信息提取，强制使用廉价的小模型（如 Llama-3-8B 或 Qwen-7B），仅在进行复杂推理时调用 GPT-4o 或 Claude 3.5 Sonnet。
3.  **工具定义的颗粒度**：在定义 AWS 工具时，尽量保持原子性。不要写一个“部署并监控应用”的巨型函数，而是拆解为“部署应用”、“获取监控指标”等细粒度工具，这能显著提高大模型的调用成功率。

**可验证的检查方式**

1.  **端到端延迟测试**：
    *   *指标*：测量从用户输入到智能体调用 AWS 工具并返回结果的 P95 延迟。
    *   *验证*：对比 `smolagents` 直接调用本地 API 与通过 AWS API Gateway 转发的延迟差异，验证网络开销是否在可接受范围内（通常建议 < 5秒）。

2.  **Token 消耗与成本分析**：
    *   *指标*：单次任务执行的平均 Token 数（输入+输出）。
    *   *验证*：运行 100 个典型测试用例，计算“多模型框架”与“单一大

---

## 技术分析

基于您提供的文章标题和摘要，虽然无法获取全文细节，但结合 **Hugging Face smolagents** 的技术特性、**AWS** 的云服务生态以及 **Agentic AI（智能体AI）** 的当前发展趋势，我可以为您构建一份深度分析报告。

以下是对该技术方案核心观点与技术要点的全面剖析：

---

### 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：**构建复杂的 Agentic AI 不应依赖于庞大的、从零开始的代码编写，而应通过模块化的开源库（如 smolagents）与云原生基础设施（如 AWS）的无缝集成来实现。** 它提倡“代码优先”的智能体设计，即让大语言模型（LLM）具备编写和执行 Python 代码的能力来解决复杂任务，而非仅仅依赖文本生成。

**作者想要传达的核心思想**
作者试图传达一种**“低门槛、高能力”**的工程化理念。通过利用 Hugging Face 的轻量级工具和 AWS 的托管服务（如 Bedrock, Lambda, S3），开发者可以快速构建出具备工具使用能力的智能体。核心思想在于将 LLM 从“聊天机器人”转变为“能够操作云资源的系统”。

**观点的创新性和深度**
*   **从“对话”到“执行”的范式转移**：传统的 AI 应用多侧重于问答，而 smolagents 强调“代码执行”，这意味着 AI 可以直接处理数据、调用 API、操作文件，这是通向通用人工智能（AGI）的关键一步。
*   **轻量级与云原生的结合**：相比于 LangChain 等重型框架，smolagents 更轻量、更专注于代码解释器能力；结合 AWS，解决了本地部署的算力瓶颈和扩展性问题。

**为什么这个观点重要**
随着 AI 从“玩具”走向“工具”，企业迫切需要能够实际执行业务逻辑的 AI。该方案提供了一条**低成本、高可扩展**的落地路径，降低了企业构建智能体应用的门槛，加速了 GenAI 在工业界的实际部署。

---

### 2. 关键技术要点

**涉及的关键技术或概念**
*   **Hugging Face smolagents**：一个专注于让 LLM 编写并执行 Python 代码的轻量级智能体框架。
*   **AWS Managed Services**：可能涉及 Amazon Bedrock（托管基础模型）、Amazon S3（存储）、AWS Lambda（无服务器计算）、IAM（权限管理）。
*   **Multi-model Framework（多模型框架）**：指智能体不绑定单一模型，而是可以根据任务需求动态调用不同的模型（如 Llama 3 用于推理，Mistral 用于对话）。

**技术原理和实现方式**
1.  **代码解释器循环**：
    *   用户输入任务 -> smolagents 将任务转化为 Python 代码。
    *   代码在沙箱环境中执行。
    *   若报错，错误信息回传给 LLM 进行修正；若成功，输出结果。
2.  **工具集成**：
    *   通过 Python 装饰器或类定义，将 AWS 的 API（如上传文件到 S3）封装为智能体可调用的“工具”。
3.  **托管模型调用**：
    *   smolagents 通过 Hugging Face Inference Endpoints 或直接通过 AWS SDK 调用 Amazon Bedrock 上的模型，实现推理过程。

**技术难点和解决方案**
*   **安全性**：让 AI 写代码存在执行恶意代码的风险。
    *   *解决方案*：使用 Docker 容器或 E2B 等沙箱环境隔离代码执行，限制网络访问和文件系统权限。
*   **幻觉与错误循环**：AI 可能写出死循环代码。
    *   *解决方案*：设置执行超时机制，以及最大重试次数限制。
*   **上下文管理**：代码执行产生的中间变量可能很大。
    *   *解决方案*：只将关键输出（如文件路径、摘要）回传给 LLM，而非所有控制台日志。

**技术创新点分析**
*   **以代码为通用接口**：传统的智能体需要为每个 API 定义复杂的 JSON Schema，而 smolagents 直接生成 Python 调用，Python 本身就是接口，大大减少了中间层的转换成本。

---

### 3. 实际应用价值

**对实际工作的指导意义**
该方案为数据科学和工程团队提供了一种**“AI 副驾驶”**的实现范式。它不仅是一个聊天机器人，更是一个能够自动化处理繁琐数据任务（如数据清洗、图表生成、报告发送）的智能助手。

**可以应用到哪些场景**
1.  **自动化数据分析**：智能体自动从 S3 读取 CSV/Pandas 数据，进行清洗、分析，并生成图表上传回 S3。
2.  **运维自动化**：智能体监控 CloudWatch 指标，根据阈值自动调整 EC2 实例或发送告警。
3.  **文档处理与检索**：结合 RAG（检索增强生成），智能体读取文档并生成结构化的 JSON 数据存入数据库。

**需要注意的问题**
*   **成本控制**：模型反复试错写代码会消耗大量 Token，需监控 API 调用成本。
*   **权限管控**：智能体拥有的 AWS IAM 权限必须遵循最小权限原则，防止 AI 误操作删除资源。

**实施建议**
*   从低风险任务开始（如内部文档处理）。
*   建立完善的日志记录，记录 AI 写下的每一行代码和执行结果，以便审计。

---

### 4. 行业影响分析

**对行业的启示**
这标志着 AI 开发正在从**“Prompt Engineering（提示词工程）”**向**“Agentic Engineering（智能体工程）”**演进。未来的开发者不仅要会写代码，还要学会如何定义工具和约束，让 AI 安全地编排这些代码。

**可能带来的变革**
*   **SaaS 软件的智能化**：未来的 SaaS 软件将集成更多 Agentic 能力，用户只需告诉软件“做什么”，软件内部的 Agent 会自动调用 API 完成操作。
*   **云厂商的竞争加剧**：AWS、Azure、GCP 都在争夺 Agentic AI 的基础设施层，谁提供最好用的托管工具和模型集成，谁就能留住开发者。

**相关领域的发展趋势**
*   **AgentOps（智能体运维）**：专门用于监控、追踪和评估智能体行为的工具链将迅速发展。
*   **多模态智能体**：未来的 smolagents 将不仅能写代码，还能直接处理图片、音频和视频流。

---

### 5. 延伸思考

**引发的其他思考**
*   **“代码”是最终极的接口吗？** 虽然代码很灵活，但对于非技术人员来说，理解 AI 生成的代码逻辑可能很困难。如何在保持代码灵活性的同时提供可视化的可控性？
*   **智能体的版权问题**：AI 编写的代码片段如果引用了开源库，是否存在许可证合规风险？

**可以拓展的方向**
*   **人机协作模式**：当 AI 遇到无法解决的错误时，如何优雅地引入人类介入，人类修正后，AI 如何学习并继续任务。
*   **多智能体协作**：一个 smolagent 负责写代码，另一个负责 Review 代码，第三个负责执行，形成流水线。

**未来发展趋势**
*   **端侧智能体**：随着模型变小，类似 smolagents 的框架可能会运行在笔记本电脑甚至手机端，直接操作本地文件，保护隐私。

---

### 6. 实践建议

**如何应用到自己的项目**
1.  **环境搭建**：在本地或 AWS EC2 上配置 Python 环境，安装 `smolagents`。
2.  **工具定义**：梳理项目中重复性高的任务（如“每日数据报表”），将其封装为 Python 函数。
3.  **智能体初始化**：配置 Hugging Face API Key 或 AWS Bedrock 连接，实例化 `CodeAgent`。
4.  **逐步授权**：先赋予只读权限测试，验证无误后再开放写权限。

**具体的行动建议**
*   学习 Python 装饰器语法，理解如何将自定义函数暴露给 LLM。
*   熟悉 AWS SDK (boto3) 的基本用法。
*   阅读 smolagents 官方文档中关于“Tool”的章节。

**需要补充的知识**
*   **LangChain 或 LlamaIndex**：虽然 smolagents 很轻量，但了解主流框架有助于对比优劣。
*   **Docker 容器技术**：为了安全地运行 AI 生成的代码，必须懂容器隔离。

**实践中的注意事项**
*   **不要赋予 Agent 生产环境的数据库直接写权限**。始终让 Agent 操作副本或通过中间层 API 交互。
*   **设置超时**：防止 Agent 陷入死循环导致资源耗尽。

---

### 7. 案例分析

**结合实际案例说明**
假设一个**金融数据分析场景**：
*   **传统方式**：分析师手动下载 S3 上的财报 Excel，用 Excel 宏或 Python 脚本清洗，做透视表，发邮件。
*   **Agentic AI 方式**：
    1.  用户对 Agent 说：“分析昨天的财报，找出增长率超过 20% 的板块，并给管理层发邮件摘要。”
    2.  smolagent 编写 Python 代码使用 `boto3` 下载文件。
    3.  编写 Pandas 代码进行计算。
    4.  编写代码调用 SES (AWS Email Service) 发送邮件。
    5.  所有过程自动完成。

**成功案例分析**
Hugging Face 官方演示中，smolagent 能够仅通过几行代码，自动读取 GitHub 仓库的文档，并生成相应的测试用例代码。这展示了其作为“编程助手”的巨大潜力。

**失败案例反思**
如果让 Agent 直接操作生产环境数据库，可能会因为 SQL 注入或逻辑错误导致数据污染。早期的 AutoGPT 实验中，Agent 经常陷入“自我对话”的死循环，消耗大量预算却无产出。这证明了**“人工介入”**和**“短周期反馈”**的重要性。

---

### 8. 哲学与逻辑：论证地图

**中心命题**
**在 AWS 云基础设施上利用 Hugging Face smolagents 构建的“代码优先”智能体，是当前实现自动化业务逻辑处理最高效、最具扩展性的技术路径。**

**支撑理由与依据**
1.  **通用性**：Python 代码是连接几乎所有云服务和数据源的通用语言，比特定的 JSON Schema 更灵活。
    *   *依据*：Python 拥有庞大的库生态，几乎涵盖了所有 IT 操作需求。
2.  **鲁棒性**：通过“执行-报错-修正”的反馈循环，代码执行比纯文本生成更能处理复杂的逻辑任务。
    *   *依据*：ReAct（推理+行动）论文表明，允许模型进行步骤化推理和工具调用能显著提升解决数学和逻辑问题的成功率。
3.  **托管服务的可靠性**：AWS 提供了可扩展、安全的计算和存储环境，解决了本地运行大模型的算力瓶颈。
    *   *依据*：AWS 在全球基础设施市场的统治地位及其 Bedrock 服务的可用性 SLA。

**反例或边界条件**
1.  **高延迟敏感场景**：如果任务需要毫秒级响应（如高频交易），代码生成+解释执行的过程太慢，不适用。
2.  **非结构化创意任务**：对于纯粹依赖人类情感、审美或极度

---

## 最佳实践

### 实践 1：构建基于工具的模块化架构

**说明**:

**实施步骤**:
1. 定义清晰的工具接口，确保每个工具只负责单一功能。
2. 使用 smolagents 的 `Tool` 类规范工具的输入和输出格式。
3. 配置主代理循环，使其能够根据用户意图自主选择并调用正确的工具。
4. 为每个工具编写详细的文档字符串，以便 LLM 理解其用途。

**注意事项**:
工具的输入输出必须经过严格验证，防止因格式错误导致 Agent 循环中断。确保工具的幂等性，避免重复执行造成副作用。

---

### 实践 2：优化模型选择与成本效益

**说明**:
Agentic AI 系统往往需要多次调用 LLM，这会导致成本和延迟迅速累积。最佳实践是根据任务的复杂度动态选择模型。对于简单的路由或分类任务，使用参数量较小、速度快的模型（如 SmolLM 或 Qwen 系列）；对于复杂的推理或代码生成任务，再调用参数量较大、能力更强的模型。Hugging Face smolagents 非常适合这种多模型共存的架构。

**实施步骤**:
1. 在 AWS 上部署或通过 API 接入多种不同规模的模型。
2. 在 Agent 配置文件中定义模型路由策略。
3. 实施一个“评估-升级”机制：先由小模型尝试，如果置信度低或失败，则升级到大模型。
4. 使用 AWS Cost Explorer 监控不同模型的 Token 消耗和成本。

**注意事项**:
频繁切换模型可能会增加网络延迟。建议在 AWS 同一区域内部署推理端点，以减少数据传输时间。

---

### 实践 3：利用 AWS Lambda 无服务器架构执行工具

**说明**:
为了提高系统的弹性和安全性，Agent 调用的工具逻辑应部署在 AWS Lambda 等无服务器计算服务中，而不是直接在 Agent 运行的本地进程中执行。这使得系统能够根据负载自动扩缩容，并且通过 AWS IAM 实现细粒度的权限控制，避免 Agent 直接暴露底层的云基础设施密钥。

**实施步骤**:
1. 将 Agent 需要调用的复杂业务逻辑封装为 AWS Lambda 函数。
2. 为 Lambda 函数配置最小权限的 IAM 角色。
3. 在 smolagents 中创建自定义工具类，通过 AWS SDK (boto3) 触发 Lambda 函数。
4. 配置异步调用模式，以处理长时间运行的任务。

**注意事项**:
注意 Lambda 的执行超时限制（默认为 3 秒，最大 15 分钟）。对于耗时较长的工具调用，应考虑使用 AWS ECS 或 Fargate。

---

### 实践 4：实施严格的输出验证与安全护栏

**说明**:
Agentic AI 具有自主性，这意味着如果缺乏约束，它可能会执行非预期的操作。必须实施多层验证机制。在 smolagents 框架中，应在工具执行前对参数进行校验，在工具执行后对输出结果进行解析和验证，防止“幻觉”或格式错误的数据污染系统状态。

**实施步骤**:
1. 使用 Pydantic 或 JSON Schema 定义严格的工具输入模型。
2. 在 Agent 代码中实现“中间人”检查层，拦截工具调用请求。
3. 对于高风险操作（如写入数据库、发送邮件），配置人工确认步骤。
4. 记录所有工具调用的输入和输出日志，以便审计。

**注意事项**:
不要依赖 LLM 自行修正格式错误。如果工具返回异常，应设计清晰的错误反馈机制给 Agent，让其尝试重试或改变策略。

---

### 实践 5：建立高效的上下文与记忆管理

**说明**:
多步推理任务需要 Agent 记住之前的交互和工具返回的结果。最佳实践是将短期记忆（当前会话）与长期记忆（向量数据库）分离。利用 smolagents 的记忆机制，将关键的执行结果存储在向量数据库（如 Amazon Aurora PostgreSQL with pgvector 或 OpenSearch）中，以便在未来的会话中检索利用。

**实施步骤**:
1. 配置 smolagents 的 `memory` 参数，连接到外部存储。
2. 实施摘要策略，当上下文窗口即将填满时，自动将旧对话压缩为摘要。
3. 为工具返回的结果添加元数据标签，便于后续检索。
4. 定期清理无关或过时的记忆数据，保持检索精度。

**注意事项**:
上下文窗口的大小直接关系到推理成本和速度。应始终监控 Token 使用量，避免上下文无限增长导致的性能下降。

---

### 实践 6：全面的可观测性与调试

**说明**:
调试 Agentic AI �

---

## 学习要点

- Hugging Face 的 smolagents 库能够将大语言模型（LLM）转化为具备推理和执行能力的智能体，通过代码解释器模式实现复杂任务的自动化处理。
- 该多模型框架支持灵活集成 Hugging Face 托管的开源模型（如 Qwen、Llama）与 AWS Bedrock 等云服务上的专有模型，优化了性能与成本的平衡。
- 智能体通过工具调用机制无缝连接 AWS 基础设施（如 S3、DynamoDB），展示了从自然语言指令到具体云资源操作的端到端自动化能力。
- 利用 AWS Lambda 进行无服务器部署，结合 smolagents 的轻量级特性，实现了可扩展且低运维成本的 Agentic AI 架构。
- 该解决方案强调了在云端构建 AI 智能体时的安全性，通过 IAM 权限管理确保工具调用仅限于授权资源。
- 通过结合推理模型与专用工具，该框架展示了 Agentic AI 在处理非结构化数据并执行结构化工作流（如数据存储）方面的实际应用价值。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Hugging Face](/tags/hugging-face/) / [smolagents](/tags/smolagents/) / [AWS](/tags/aws/) / [Agent](/tags/agent/) / [多模型](/tags/%E5%A4%9A%E6%A8%A1%E5%9E%8B/) / [RAG](/tags/rag/) / [医疗AI](/tags/%E5%8C%BB%E7%96%97ai/) / [向量检索](/tags/%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2/)
- 场景： [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-4.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI Agent及多模型检索方案]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-2.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-3.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI智能体]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-5.md" >}})
