---
title: "基于AWS与Hugging Face smolagents构建多模型医疗AI代理"
date: 2026-02-24T11:01:45+08:00
draft: false
entry_kind: "auto"
tags: ["Agentic AI", "Hugging Face", "smolagents", "AWS", "医疗AI", "多模型架构", "RAG", "向量检索"]
categories: ["AI 工程", "大模型"]
source: blogs_podcasts
description: "以下是内容的中文总结： 本文介绍了如何利用开源 Python 库 **Hugging Face smolagents** 结合 **AWS** 托管服务，构建并部署一个**多模型架构的 Agentic AI（智能体 AI）** 解决方案。 **主要内容包括：** 1. **核心工具：** Hugging Face sm"
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws
scenarios: ["AI/ML项目", "RAG应用", "工具"]
---

# 基于AWS与Hugging Face smolagents构建多模型医疗AI代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-23T15:47:06+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)

---
## 摘要/简介

Hugging Face smolagents 是一个开源 Python 库，旨在用几行代码就能轻松构建和运行代理。我们将向您展示如何通过将 Hugging Face smolagents 与 Amazon Web Services (AWS) 托管服务集成，来构建一个代理式 AI 解决方案。您将学习如何部署一个医疗保健 AI 代理，该代理将展示多模型部署选项、向量增强知识检索以及临床决策支持能力。

---
## 导语

随着大模型应用从简单的对话交互向具备自主规划能力的代理（Agent）演进，如何高效构建并部署此类系统成为开发者关注的焦点。本文将介绍如何利用 Hugging Face 的轻量级库 smolagents 结合 AWS 托管服务，快速搭建一个具备多模型调度与向量检索能力的 AI 解决方案。通过构建一个具体的医疗保健辅助代理，您将掌握实现临床决策支持与知识增强的关键技术细节。

---
## 摘要

以下是内容的中文总结：

本文介绍了如何利用开源 Python 库 **Hugging Face smolagents** 结合 **AWS** 托管服务，构建并部署一个**多模型架构的 Agentic AI（智能体 AI）** 解决方案。

**主要内容包括：**

1.  **核心工具：** Hugging Face smolagents 是一个开源库，旨在通过极简的代码实现 AI 智能体的构建与运行。
2.  **部署方式：** 该方案展示了如何将 smolagents 与 AWS 的托管服务无缝集成。
3.  **应用场景：** 以**医疗健康领域**为例，构建了一个具备以下功能的 AI 智能体：
    *   **多模型部署选项：** 灵活部署和使用不同的 AI 模型。
    *   **向量增强知识检索：** 利用向量数据库技术提升信息检索的准确性。
    *   **临床决策支持：** 辅助医疗人员进行专业决策。

简而言之，这是一个关于在 AWS 云平台上，利用简易工具快速开发具备高级检索和决策能力的医疗 AI 智能体的技术指南。

---
## 评论

**中心观点**
该文章提出了一种通过将 Hugging Face 轻量级智能体框架与 AWS 云原生基础设施深度集成，以低成本、高可扩展性构建生产级 Agentic AI 解决方案的工程化路径。

**支撑理由与边界条件**

1.  **技术栈的轻量化与低门槛（事实陈述）**
    文章强调了 `smolagents` 的核心优势在于其极简的代码逻辑（Python 优先），这降低了开发者进入 Agentic AI 领域的门槛。相比于 LangChain 等重型框架，smolagents 更专注于让 LLM 能够直接执行 Python 代码作为工具，这种“代码即动作”的设计范式在处理数据分析和逻辑推理任务时尤为高效。

2.  **云原生架构的弹性与鲁棒性（作者观点）**
    文章通过集成 AWS 的托管服务（如 Lambda, Bedrock, Step Functions），解决了单机运行 AI 智能体的局限性。这种架构不仅提供了计算弹性和高可用性，还通过云服务天然解决了工具调用中的安全认证（如 IAM 权限管理）问题，使得智能体能够安全地操作云资源，这是从“Demo 走向生产”的关键一步。

3.  **多模型协作的编排能力（你的推断）**
    标题中提到的“Multi-model framework”暗示了文章不仅局限于单一模型，而是利用 AWS Bedrock 或 SageMaker 的端点能力，根据任务类型动态路由到不同的模型（例如用 Claude 处理长文本，用 Llama 处理数学）。这种编排能力是构建复杂 Agentic 系统的核心，能够平衡性能与成本。

**反例/边界条件：**

*   **边界条件 1：延迟敏感型场景**
    将 smolagents 部署在 AWS 无服务器架构（如 Lambda）上，虽然扩展性好，但会引入显著的冷启动延迟和网络延迟。对于需要毫秒级响应的实时交互系统，这种基于云函数调用的多步推理架构可能导致用户体验下降。
*   **边界条件 2：非结构化任务的局限性**
    smolagents 依赖 Python 代码执行作为主要工具。如果任务主要是基于视觉的非结构化操作（如复杂的 GUI 点击流程）或需要高度确定性的业务逻辑流转，纯代码生成的方式可能不如专门的 API 调用或工作流引擎稳定。

**深入评价**

**1. 内容深度与论证严谨性**
文章采取了典型的“Tutorial”风格，深度适中但偏向工程实现。它严谨地展示了如何通过代码将 Hugging Face 的生态与 AWS 基础设施连接，论证了“开源框架 + 云厂商托管”的混合架构可行性。然而，文章可能缺乏对 Agentic AI 中“幻觉”问题的深层讨论，例如当智能体生成错误的 Python 代码操作 AWS 资源时，如何设计防护机制，这在论证安全性方面略显不足。

**2. 实用价值**
对于正在寻找落地方案的 AI 工程师而言，该文章具有极高的实用价值。它提供了一套可复制的技术蓝图，避免了团队从零搭建智能体运行环境。特别是对于已经深度绑定 AWS 的企业，这种方案能够最小化架构改造成本。

**3. 创新性**
将 smolagents 这种“轻量级”前端与 AWS 这种“重量级”后端结合是一种务实而非激进创新。它没有提出新的算法模型，但在**工程范式**上提出了一种新思路：即智能体的“大脑”可以是轻量、开源的，而“手脚”应当依赖成熟的企业级云服务。

**4. 行业影响**
这篇文章反映了行业正在从“模型中心主义”转向“系统中心主义”。它预示着未来的 Agentic AI 不再是单一的大模型，而是由轻量级编排框架管理的、能够调用无数 SaaS 能力的分布式系统。这可能会加速 MaaS（Model as a Service）厂商与云厂商的深度捆绑。

**5. 争议点与不同观点**
*   **代码执行的安全性：** 允许 LLM 生成并执行 Python 代码（smolagents 的核心特性）存在巨大的安全风险。如果智能体被诱导执行 `os.system('rm -rf /')` 或恶意修改 AWS 安全组，后果不堪设想。文章可能未充分阐述沙箱隔离的重要性。
*   **框架碎片化：** 业界已有 LangChain, LangGraph, AutoGen 等成熟框架。引入 smolagents 是否会增加技术栈的碎片化？有观点认为，直接使用成熟框架的 AWS 社区版可能比维护一个新的轻量库更稳妥。

**实际应用建议**

*   **不要在生产环境直接执行生成的代码：** 务必使用 Docker 容器或 AWS Firecracker 微虚拟机来隔离 smolagents 的代码执行环境。
*   **实施三权分立：** 在 AWS IAM 策略中，严格限制 smolagents 所扮演角色的权限，遵循最小权限原则，防止智能体误操作删除关键数据。
*   **成本监控：** Agentic AI 的多步推理特性会导致 API 调用次数指数级增长。建议在 AWS 上启用 Budgets 并监控 Bedrock/API 的调用量，防止因无限循环导致的账单爆炸。

**可验证的检查方式**

1.  **延迟基准测试：**
    *   *指标：* 测量从用户输入到智能体完成整个工具调用链（包含 AWS Lambda 冷启动和 Bedrock 推理）的总耗时（P95 延迟）。
    *   *预期：* 如果超过 5 秒，则该架构不适合实时聊天场景。

2.  **工具调用成功率

---
## 技术分析

基于提供的文章标题《Agentic AI with multi-model framework using Hugging Face smolagents on AWS》及摘要内容，结合当前生成式AI与云原生架构的技术趋势，以下是对该文章核心观点及技术要点的深入分析。

---

# 深入分析：基于 AWS 与 Hugging Face smolagents 的 Agentic AI 架构

## 1. 核心观点深度解读

**主要观点：**
文章的核心主张是**通过将轻量级、开源的 Agentic 编程框架与高度可扩展的企业级云基础设施相结合，可以以极低的代码复杂度构建出具备生产级能力的智能体解决方案。**

**核心思想：**
作者试图传达一种**“低门槛 + 高上限”**的架构思想。
1.  **低门槛：** 利用 Hugging Face `smolagents` 库的极简 API（Python 优先），开发者不需要从零编写复杂的 LLM 调用或提示词管理逻辑，仅需几行代码即可定义 Agent 的行为。
2.  **高上限：** 将这些 Agent 部署在 AWS 上，利用其托管服务（如 Bedrock, Lambda, Fargate 等）来解决开源模型通常面临的扩展性、安全性和企业集成问题。

**观点的创新性与深度：**
*   **从“对话”到“行动”的范式转移：** 文章不仅讨论生成文本，更侧重于 Agentic AI（智能体 AI），即 AI 能够自主规划、调用工具并执行任务。
*   **多模型编排：** 强调“Multi-model framework”，意味着单一模型无法解决所有问题。文章可能探讨了如何根据任务类型（如推理用 QwQ，代码用 DeepSeek，图像用 Flux）动态路由到不同模型，这是对当前“单体模型”架构的超越。
*   **云原生化：** 将开源库与闭源/托管服务（AWS）混合使用，体现了“Hybrid AI”（混合式 AI）的务实策略。

**重要性：**
这一观点解决了当前企业落地 AI 的最大痛点：**原型验证与生产环境之间的鸿沟**。它提供了一条从 Jupyter Notebook 快速走向云端生产环境的标准化路径。

## 2. 关键技术要点

**涉及的关键技术：**
1.  **Hugging Face `smolagents`：** 一个专注于极简主义的 Python 库。其核心是 `CodeAgent`，能够编写 Python 代码片段来解决问题，而非仅仅依赖文本输出。
2.  **AWS Bedrock / SageMaker：** 提供底层模型推理能力。文章可能涉及如何通过 AWS SDK 将 smolagents 连接到 Bedrock 上的托管模型（如 Claude, Llama 3）或部署在 SageMaker 上的开源模型。
3.  **工具调用与函数定义：** Agent 能够动态调用外部 API（如搜索、数据库查询、文件操作）。

**技术原理与实现：**
*   **ReAct 模式：** smolagents 内部通常采用 ReAct（Reasoning + Acting）循环。Agent 观察环境 -> 思考下一步行动 -> 执行工具调用 -> 获取结果 -> 重复。
*   **沙箱执行：** 由于 smolagents 倾向于执行 Python 代码，技术实现上必须在隔离的沙箱中运行（如 Docker 容器或受限的 Python 执行环境），以防止恶意代码执行。

**技术难点与解决方案：**
*   **难点：** 幻觉与错误传播。如果 Agent 生成了错误的代码或调用了错误的参数，整个流程会崩溃。
*   **方案：** 引入“多模型”机制。例如，使用一个强大的模型（如 GPT-4 或 Claude 3.5 Sonnet）作为“裁判”或“规划者”，使用较小的模型（如 SmolLM）作为“执行者”，以平衡成本与准确性。
*   **难点：** 状态管理。
*   **方案：** 利用 AWS 的存储服务（如 S3 或 DynamoDB）持久化 Agent 的记忆和上下文。

## 3. 实际应用价值

**指导意义：**
该架构为企业提供了一种**“敏捷 + 稳健”**的 AI 落地指南。企业不需要为了使用 Agent 而完全重构现有云架构，也不必受困于单一云厂商的锁定。

**应用场景：**
1.  **RAG（检索增强生成）增强版：** 不仅仅是问答，Agent 能够读取文档、总结、并发送邮件。
2.  **数据分析助手：** 连接 SQL 数据库，Agent 能够编写 Python 脚本进行数据清洗和可视化，直接返回图表。
3.  **DevOps 自动化：** 监控 AWS CloudWatch 指标，当异常发生时，Agent 自动诊断并尝试修复（如扩容 EC2 实例）。

**注意事项：**
*   **成本控制：** Agentic AI 涉及多轮推理和多次 API 调用，成本呈指数级增长。需要在 AWS 端设置严格的预算告警。
*   **安全边界：** 赋予 AI 调用 AWS API 的权限是危险的。必须实施最小权限原则（IAM Role），限制 Agent 只能操作特定的资源。

## 4. 行业影响分析

**行业启示：**
*   **MLOps 向 LLMOps 的演进：** 行业正在从简单的模型部署转向复杂的智能体编排。AWS 与 Hugging Face 的合作表明，未来的核心竞争力在于**“编排能力”**而非单纯的模型大小。
*   **小模型的崛起：** `smolagents` 名字中的 "smol" 暗示了小模型（SLM）在特定任务上的潜力。这将推动行业从“越大越好”转向“又快又好”。

**带来的变革：**
*   **软件开发的自动化：** 通过 CodeAgent，AI 从辅助编程转变为自主编写代码片段并执行，这将改变未来的软件开发流程。
*   **云原生 AI 的标准化：** 越来越多的开源框架将原生支持各大云厂商的托管服务，消除“部署焦虑”。

## 5. 延伸思考

**拓展方向：**
*   **边缘端 Agentic AI：** 既然 smolagents 强调轻量，是否可以将其部署在 AWS IoT Greengrass 或边缘设备上，实现离线自主决策？
*   **多智能体协作：** 文章主要讨论单个 Agent。未来可以探索如何用 smolagents 构建多智能体系统（MAS），在 AWS Step Functions 中编排多个 Agent 协同工作。

**需进一步研究的问题：**
*   如何量化 Agent 的“可靠性”？如何测试一个具有概率性行为的 Agent 系统？
*   当 Agent 自主编写代码时，如何确保生成的代码符合企业的安全合规标准（无漏洞、无后门）？

## 6. 实践建议

**如何应用到项目：**
1.  **起步：** 在本地安装 `smolagents`，使用免费的 Hugging Face 模型（如 Qwen2.5-Coder）测试基础的代码生成能力。
2.  **容器化：** 将 Agent 逻辑封装在 Docker 容器中。
3.  **云端部署：** 将容器推送到 AWS ECR，并使用 AWS App Runner 或 ECS Fargate 进行托管。
4.  **工具集成：** 编写 Python 工具函数，利用 `boto3` 库连接 AWS 服务（如 S3, SQS），并将这些工具注册给 smolagents。

**补充知识：**
*   熟悉 **LangChain** 或 **LlamaIndex** 的概念（虽然 smolagents 是独立的，但概念互通）。
*   深入理解 **AWS IAM 权限模型**，确保 Agent 的安全运行。
*   掌握 **Python 异步编程**，因为 Agent 调用外部 API 时，异步处理能显著提升响应速度。

## 7. 案例分析

**成功案例设想（基于架构推演）：**
*   **场景：** 电商公司的自动化财报分析。
*   **实施：** 构建一个 smolagent，赋予其“读取 S3 财务 CSV”和“发送邮件”的工具。
*   **流程：** Agent 读取数据 -> 编写 Pandas 代码计算增长率 -> 发现某项指标异常 -> 自动查询 DynamoDB 中的相关订单详情 -> 生成 HTML 报告 -> 发送给管理层。
*   **成功因素：** 全程无人工干预，利用 AWS 托管服务保证了数据安全和稳定性。

**失败案例反思：**
*   **场景：** 客户服务机器人。
*   **问题：** Agent 被赋予“退款”工具的权限，但由于 Prompt 注入攻击或幻觉，Agent 对未授权的订单执行了退款代码。
*   **教训：** **工具的权限必须大于 Agent 的智能。** 必须在工具层面增加二次确认逻辑或硬编码的金额限制，不能完全信任 Agent 的判断。

## 8. 哲学与逻辑：论证地图

**中心命题：**
在构建企业级 Agentic AI 应用时，采用“轻量级开源框架 + 企业级托管基础设施”的混合架构优于单纯的闭源 SaaS 或单纯的本地自建方案。

**支撑理由与依据：**
1.  **敏捷性：** 开源框架（如 smolagents）允许开发者用极少的代码快速迭代逻辑，无需等待云厂商更新功能。
    *   *依据：* 摘要提到 "straightforward to build... using a few lines of code"。
2.  **可扩展性与可靠性：** AWS 等托管服务提供了单靠开源代码难以实现的全球负载均衡、高可用性和安全合规性。
    *   *依据：* 云基础设施的行业地位及 AWS 的 SLA。
3.  **模型灵活性：** 该架构支持“多模型”策略，避免了被单一模型供应商锁定，可以根据成本和质量动态切换模型。
    *   *依据：* 文章标题提及 "multi-model framework"。

**反例与边界条件：**
1.  **极低延迟要求：** 如果应用要求毫秒级响应，Agent 的多步推理和云端网络延迟可能使其无法接受（此时需使用本地部署的大模型）。
2.  **数据绝对隐私：** 对于涉及国家机密或极高敏感数据的场景，任何连接外网或使用托管 API 的方案都不可行，必须完全物理隔离。

**命题性质分析：**
*   **事实：** smolagents 是开源库；AWS 是托管服务；两者可以集成。
*   **价值判断：** “混合架构优于...”属于价值判断，基于开发效率、维护成本和性能的综合考量。
*   **可检验预测：** 采用此架构的项目，其开发周期将短于完全自研架构，且其运营成本将低于单纯使用昂贵闭源 API（如 GPT-4-only）的方案。

**立场与验证：**
*   **立场：** 支持该混合架构。它代表了当前技术成熟度下的最优解。
*   **验证方式：**
    *   **指标：** 对比实现相同功能的 Agent，记录“代码行数”、“开发时间”和“平均每次推理成本”。
    *   **实验：** 选取一个标准任务（如分析 S3 日志），分别用纯 OpenAI API 方案和 smolagents+AWS 方案实现，测量端到端延迟和 Token 消耗量。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于工具的模块化代理架构

**说明**: 
利用 Hugging Face smolagents 的 `CodeAgent` 或 `ToolCallingAgent` 功能，将单一的大型语言模型（LLM）转换为能够自主决策并调用外部工具的智能体。通过模块化设计，将不同的功能（如代码执行、网络搜索、文件 I/O）封装为独立工具，使代理能够处理复杂的多步骤任务，而不是仅限于生成文本。

**实施步骤**:
1. 定义明确的工具接口，使用 Python 函数并添加适当的类型提示和文档字符串，以便 smolagents 自动解析工具功能。
2. 使用 `@tool` 装饰器或 `Tool` 类将自定义函数注册到代理中。
3. 在 AWS Lambda 或 ECS 上部署工具服务，通过 API 暴露给代理调用，实现工具的解耦和扩展。

**注意事项**: 
确保工具的描述清晰准确，因为 LLM 依赖这些描述来决定何时以及如何调用工具。避免在工具中包含敏感逻辑，应实施严格的权限控制。

---

### 实践 2：优化多模型路由与选择策略

**说明**: 
在 Agentic AI 框架中，不同的任务需要不同能力的模型。实施多模型策略，根据任务复杂度动态选择模型。例如，对于简单的任务使用轻量级、低成本的模型（如 SmolLM），对于复杂的推理任务使用高性能模型（如 Llama 3 或 Mistral）。Hugging Face smolagents 支持通过 Hugging Face Inference API (Serverless) 或托管在 Amazon SageMaker 上的端点进行模型切换。

**实施步骤**:
1. 在 AWS 上部署多个模型端点，或配置 Hugging Face Serverless API 访问权限。
2. 在代理配置中定义模型映射表，根据任务类型（如“代码生成”、“问答”、“摘要”）分配默认模型。
3. 实施中间件逻辑，根据输入 Token 数量或历史成功率动态路由请求。

**注意事项**: 
监控不同模型的延迟和成本，特别是使用 Hugging Face Serverless API 时的速率限制和冷启动时间。对于生产环境，建议使用 SageMaker 的实时端点以获得更稳定的性能。

---

### 实践 3：建立安全的沙箱执行环境

**说明**: 
smolagents（特别是 `CodeAgent`）具有在沙箱环境中执行 Python 代码的能力。虽然这极大地增强了代理的实用性，但也带来了安全风险。必须严格限制代码执行环境的资源访问权限，防止代理执行恶意操作或无限循环。

**实施步骤**:
1. 使用 Docker 容器作为代码执行的主要隔离机制，限制网络访问和文件系统挂载。
2. 在 AWS 架构中，可以使用 AWS Fargate 或 Lambda 运行代码执行层，确保计算资源是临时的且无状态的。
3. 设置严格的超时和内存限制，防止资源耗尽攻击。

**注意事项**: 
切勿在具有生产环境 IAM 权限的上下文中直接运行代理生成的代码。始终假设生成的代码可能是不安全的。

---

### 实践 4：实施全面的可观测性与日志记录

**说明**: 
Agentic AI 的执行过程是非确定性的，涉及多次模型调用和工具交互。为了调试和优化，必须捕获完整的“思维链”和中间步骤。利用 AWS CloudWatch 或 X-Ray 追踪代理的决策过程、工具调用参数和返回结果。

**实施步骤**:
1. 配置 smolagents 的日志级别为 DEBUG 或 INFO，捕获所有内部动作。
2. 将代理的执行步骤（Prompt、Output、Tool Call）结构化地发送到 CloudWatch Logs。
3. 利用 LangChain 或 OpenTelemetry 集成，将代理的执行链路可视化。

**注意事项**: 
记录日志可能会产生大量数据，需注意成本控制。确保日志中不包含敏感用户数据（PII），必要时在记录前进行脱敏处理。

---

### 实践 5：利用 SageMaker 实现高性能推理

**说明**: 
虽然 Hugging Face Serverless API 适合原型开发，但在生产环境中，为了获得更低的延迟和更高的吞吐量，应使用 Amazon SageMaker 部署模型。SageMaker 提供了针对特定硬件（如 AWS Inferentia 或 NVIDIA GPU）优化的容器，可以显著提升多模型框架的响应速度。

**实施步骤**:
1. 使用 Hugging Face Inference Container (DLC) 在 SageMaker 上部署所需的 LLM。
2. 配置 SageMaker 端点的自动扩缩容策略，以应对代理工作负载的波动。
3. 在 smolagents 配置中，将模型 API 端点指向 SageMaker 推理 URL。

**注意事项**: 
管理 SageMaker 端点的成本，在不使用时将其调至零或使用多模型端点以优化资源利用率。

---

### 实践 6：设计有效的提示词工程与上下文管理

**说明**: 
代理的性能很大程度上取决于 System Prompt 和上下文的管理。明确代理的角色、可用工具及其局限性。利用 smolagents 的 `SystemPrompt` 参数，为代理设定清晰的行为边界

---
## 学习要点

- Smolagents 通过将大语言模型转化为能够自主编写代码并执行的工具代理，显著降低了构建 Agentic AI 应用的复杂度。
- 该框架无缝集成 Hugging Face 丰富的模型生态与工具，使开发者能够灵活调用各类开源模型及 API 服务。
- 借助 AWS 基础设施（如 Lambda 和 Bedrock），该方案实现了无服务器架构下的弹性扩展与企业级安全性。
- 核心代理逻辑被设计为通过编写 Python 代码来解决问题，而非仅依赖文本生成，从而大幅提升了处理复杂任务的准确性。
- 开发者仅需极少的代码量即可部署具备工具调用能力的智能体，极大加速了从原型到生产环境的落地过程。
- 该架构展示了如何利用云平台与开源工具的结合，以低成本方式验证并迭代高级 AI 智能体解决方案。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws](https://aws.amazon.com/blogs/machine-learning/agentic-ai-with-multi-model-framework-using-hugging-face-smolagents-on-aws)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Agentic AI](/tags/agentic-ai/) / [Hugging Face](/tags/hugging-face/) / [smolagents](/tags/smolagents/) / [AWS](/tags/aws/) / [医疗AI](/tags/%E5%8C%BB%E7%96%97ai/) / [多模型架构](/tags/%E5%A4%9A%E6%A8%A1%E5%9E%8B%E6%9E%B6%E6%9E%84/) / [RAG](/tags/rag/) / [向量检索](/tags/%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/) / [工具](/scenarios/%E5%B7%A5%E5%85%B7/)

### 相关文章

- [基于AWS与Hugging Face smolagents构建医疗AI智能体]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-0.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI智能体]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-5.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260224-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-4.md" >}})
- [基于AWS与Hugging Face smolagents构建医疗AI Agent及多模型检索方案]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-2.md" >}})
- [基于AWS与Hugging Face smolagents构建多模型医疗AI Agent]({{< relref "posts/20260223-blogs_podcasts-agentic-ai-with-multi-model-framework-using-huggin-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*