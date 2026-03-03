---
title: "基于 Bedrock 与 LangGraph 在 SageMaker AI 上构建无服务器对话代理"
date: 2026-03-03T05:12:50+08:00
draft: false
entry_kind: "auto"
tags: ["LangGraph", "Amazon Bedrock", "SageMaker", "MLflow", "无服务器架构", "Agent", "Claude", "LLMOps"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "**构建基于 Claude、LangGraph 和 SageMaker 托管 MLflow 的无服务器对话式 AI 智能体** 本文详细介绍了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上托管的 **MLflow**，构建一个企业级的"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios: ["AI/ML项目", "大语言模型"]
---

# 基于 Bedrock 与 LangGraph 在 SageMaker AI 上构建无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---
## 摘要/简介

本文将探讨如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上的托管 MLflow 来构建一个智能对话代理。

---
## 导语

随着对话式 AI 在实际业务场景中的应用日益深入，如何构建可扩展且易于管理的智能代理成为开发者关注的焦点。本文将详细介绍如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上的托管 MLflow，构建一个无服务器的对话代理。通过阅读本文，您将掌握从模型编排到全生命周期监控的完整实现路径，从而高效地部署和维护生产级 AI 应用。

---
## 摘要

**构建基于 Claude、LangGraph 和 SageMaker 托管 MLflow 的无服务器对话式 AI 智能体**

本文详细介绍了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上托管的 **MLflow**，构建一个企业级的无服务器对话式 AI 智能体。该方案旨在解决传统 AI 应用开发中模型管理混乱、部署复杂以及难以处理复杂多步对话的问题。

### 核心组件

1.  **Amazon Bedrock**: 作为基础模型层，提供对 **Claude 3** 等高性能大模型的访问，用于生成响应和推理。
2.  **LangGraph**: 用于编排智能体的工作流。它允许开发者定义有状态的图结构，从而控制对话流，实现更复杂的逻辑（如循环、条件分支和多步推理）。
3.  **Amazon SageMaker AI (托管 MLflow)**: 用于全生命周期的模型实验、追踪和注册。MLflow 负责管理 LangGraph 组件和提示词的版本，确保开发过程的可重复性和可追溯性。

### 架构与工作流

该解决方案采用**无服务器架构**，无需管理底层基础设施，主要流程如下：

1.  **开发与实验**:
    *   使用 LangGraph 定义智能体的对话逻辑图。
    *   利用 SageMaker 托管的 MLflow 记录实验参数、指标和模型工件。
    *   通过 MLflow UI 比较不同提示词版本或配置的效果。
2.  **模型注册**:
    *   将验证过的 LangGraph 智能体（及其配置）注册到 MLflow 模型注册表中。
3.  **部署**:
    *   利用 **Amazon SageMaker Serverless Inference** 或 **SageMaker Real-Time Endpoints** 部署智能体。
    *   无服务器特性允许自动扩缩容，按实际执行量付费，无需预置实例。

### 关键优势

*   **简化的工作流**: LangGraph 将复杂的对话逻辑可视化、结构化，降低了构建循环式智能体的门槛。
*   **统一的治理**: 托管的 MLflow 与 SageMaker 无缝集成，提供了集中的模型治理能力，解决了 LangChain/LangGraph 应用难以版本化的问题。
*   **成本效益**: 无服务器架构意味着用户只需为对话执行的计算

---
## 评论

**中心观点**
该文章展示了一种典型的“云原生全栈”范式，即利用 Amazon SageMaker 的托管基础设施（MLflow）来治理 LangGraph 构建的多步推理应用，并对接 Bedrock 模型，旨在解决企业级生成式 AI 应用中从“快速原型”到“生产级落地”的最后一公里难题。

**支撑理由与评价**

**1. 内容深度：从“模型调用”转向“工程治理”的务实尝试**
*   **事实陈述**：文章没有停留在简单的“Hello World”式 API 调用，而是引入了 **LangGraph** 来处理状态机和循环逻辑，以及 **Managed MLflow** 来处理 LLM 的实验追踪和模型注册。
*   **深度评价**：这触及了当前 RAG（检索增强生成）和 Agent 开发的痛点——即非确定性代码的调试困难。将 MLflow 引入 LangGraph 流程，试图将数据科学家的模型治理习惯与开发者的应用构建习惯融合。这种论证在工程严谨性上值得肯定，它指出了 Agent 开发不仅仅是提示词工程，更是系统工程。
*   **反例/边界条件**：文章可能低估了 LangGraph 在复杂异步工作流中的状态管理难度。MLflow 虽然强大，但在记录非结构化数据（如长上下文对话历史、中间思维链 JSON）时，查询和可视化效率往往不如专门的 LLM Ops 工具（如 LangSmith 或 Arize）。

**2. 实用价值：强锁定下的高效率**
*   **事实陈述**：对于已经深度依赖 AWS 生态的企业，该方案提供了极高的实用价值。它消除了搭建 MLflow 服务器的运维负担，并直接利用 Bedrock 的企业级安全合规能力。
*   **你的推断**：文章隐含的承诺是“通过托管服务降低运维成本”。在实际工作中，这确实能加速团队从验证到部署的周期，特别是在需要严格权限控制和审计日志的金融或医疗行业。
*   **反例/边界条件**：这种高价值具有极强的“厂商锁定”属性。如果企业需要跨云部署（例如同时使用 Azure 或 GCP 的特定 GPU 实例），或者希望切换到开源模型（如 Llama 3 的本地部署），这种紧密耦合 SageMaker 和 Bedrock 的架构迁移成本会非常高。

**3. 创新性：架构组装大于算法创新**
*   **事实陈述**：文章将 LangGraph（控制层）、MLflow（治理层）和 Bedrock（模型层）结合。
*   **你的观点**：这并非算法层面的创新，而是**架构组装模式的创新**。它验证了“MLOps + LLMOps”融合的趋势。过去 MLflow 主要追踪传统 ML 模型（sklearn, tensorflow），现在将其扩展到追踪 Agent 的“轨迹”和“工具调用”，这种范式的转移对行业有指导意义。
*   **反例/边界条件**：这种架构在处理超大规模并发时可能面临挑战。Serverless 虽然能自动扩缩容，但 LangGraph 的状态持久化和 MLflow 的日志记录在高并发下可能成为 I/O 瓶颈，文章未对此进行性能压测的深度探讨。

**4. 行业影响：推动“Agent 即软件”的标准化**
*   **事实陈述**：AWS 官方博客推荐 LangGraph，这实际上是对 LangGraph 生态的一种背书。
*   **行业影响**：这表明行业正在从单一的“Chatbot”向具备记忆和工具调用能力的“Agent”过渡。大型云厂商开始意识到，仅仅提供模型（Bedrock）是不够的，必须提供编排层和治理层。这会加速行业将 Agent 开发纳入标准的 CI/CD 流程，而非脚本式的游击开发。

**5. 争议点：过度工程化 vs. 企业级刚需**
*   **不同观点**：部分开发者认为，对于一个简单的对话 Agent，引入 MLflow 和 LangGraph 是“杀鸡用牛刀”。
*   **你的观点**：这取决于应用场景。如果是个人项目或简单的客服问答，直接调用 Streamlit + OpenAI API 即可。但如果是涉及金钱交易、多步骤任务规划的 Agent，缺乏 MLflow 这种版本控制和回滚机制是灾难性的。文章的争议点在于其默认假设读者都有“企业级”需求，可能吓退初创团队。

**实际应用建议**

1.  **评估厂商锁定风险**：在采用此架构前，确认公司未来 2-3 年的云战略。如果必须保持多云灵活性，建议将 MLflow 部署在 Kubernetes (如 Kubeflow) 上，而非直接使用 SageMaker 托管版，或者使用 LangSmith 等中立工具。
2.  **关注成本结构**：Serverless 虽然免运维，但 Bedrock 按 Token 计费、SageMaker 按实例/计费，在高频对话场景下成本可能失控。建议在 MLflow 中不仅记录模型指标，也要记录“Token 消耗”和“延迟”作为核心 KPI。
3.  **异步处理优先**：LangGraph 的节点如果是串行执行（如先查数据库再调用工具再总结），总延迟会累加。在实际应用中，应尽量设计并行节点，或在 SageMaker 后端配合异步队列（如 SQS）使用。

**可验证的检查方式**

1.  **指标验证（实验）**：
    *   **检查项**：LangGraph 在 SageMaker 上的冷启动时间。
    *   **验证方法**：构建一个并发测试脚本，模拟从 0 到 100 QPS

---
## 技术分析

基于文章标题《Build a serverless conversational AI agent using Claude with LangGraph and managed MLflow on Amazon SageMaker AI》及摘要，以下是对该技术方案的全面深入分析。

---

# 深度分析：基于 SageMaker AI、LangGraph 与 Claude 的无服务器对话智能体架构

## 1. 核心观点深度解读

**主要观点**
文章的核心主张是：通过将 **Amazon Bedrock**（作为基础模型底座）、**LangGraph**（作为状态机编排层）与 **SageMaker 上的托管 MLflow**（作为全生命周期管理平台）三者结合，可以构建出一个既具备复杂逻辑推理能力，又具备企业级可观测性与治理能力的**无服务器对话智能体**。

**核心思想**
作者试图传达的现代 AI 工程化理念是**“可组合性”与“可观测性”并重**。
1.  **可组合性**：利用 LangGraph 将大语言模型（LLM）的推理能力与外部工具、记忆状态通过图结构组合，突破简单对话的局限。
2.  **可观测性**：在生成式 AI 的非确定性特征下，必须依赖 MLflow 进行严格的实验追踪、模型版本管理和部署监控，才能将 AI 原型转化为可靠的生产力。
3.  **无服务器优先**：利用云原生架构（Serverless）消除基础设施运维负担，让开发者专注于业务逻辑的构建。

**观点的创新性与深度**
该架构的创新点在于**填补了“应用编排”与“MLOps”之间的鸿沟**。通常，LangChain/LangGraph 开发者关注于 Prompt 和流程，而 MLOps 工程师关注于模型训练。该方案提出在 Bedrock 这样的托管服务环境下，如何利用 MLflow 去管理那些不仅包含“模型参数”，还包含“Prompt 模板、Python 代码逻辑（LangGraph 节点）”的复合型 AI 应用。这是一种**全栈式**的 AI Agent 视角。

**重要性**
随着企业从“演示 POC”走向“生产落地”，最大的痛点不再是模型不够强，而是**不可控、不可测、难以维护**。该方案提供了一条标准化的路径，解决了 Agent 应用“难以工程化”的难题。

---

## 2. 关键技术要点

### 涉及的关键技术
1.  **Amazon Bedrock**: 提供 Claude 3/3.5 等大模型的 API 访问，具备 Serverless 伸缩特性。
2.  **LangGraph**: 基于 LangChain，专门用于构建有状态、多参与者的循环图结构，非常适合实现 Agent 的“反思-行动”循环。
3.  **Managed MLflow on SageMaker**: 用于追踪实验、管理模型 artifacts、注册模型。
4.  **Amazon SageMaker AI**: 提供计算环境和统一的 AI 集成开发环境。

### 技术原理与实现方式
*   **Agent 编排**: 利用 LangGraph 定义 `State`（状态）和 `Nodes`（节点）。状态在用户输入、LLM 调用、工具执行之间流转。通过图的循环结构，Agent 可以自主决定是继续查询工具还是直接回答。
*   **模型与代码打包**: MLflow 不仅记录 LLM 的调用参数，还将 LangGraph 的 Python 代码逻辑、Prompt 模板打包为一个 `MLflow Model`。这使得部署时，不仅部署了模型，还部署了其背后的逻辑。
*   **无服务器部署**: 利用 SageMaker 的 Serverless 推理特性或 Bedrock 的直接调用，无需预置 EC2 实例，根据请求量自动伸缩，实现按需付费。

### 技术难点与解决方案
*   **难点**: **状态持久化与并发管理**。Agent 对话需要记忆，但在无服务器环境下，内存是不共享的。
*   **方案**: 文章可能暗示使用外部存储（如 DynamoDB 或 S3）配合 LangGraph 的检查点机制来保存图的状态，实现断点续聊和并发支持。
*   **难点**: **非确定性应用的版本管理**。同样的输入，LLM 可能输出不同结果，导致回归测试困难。
*   **方案**: 利用 MLflow 的 `Evaluation` 功能，不仅记录代码，还记录基于特定数据集的评估指标（如准确率、幻觉率），建立质量基线。

### 技术创新点分析
**“模型即代码，代码即模型”的深度融合**。传统 MLOps 关注 `.pth` 或 `.pkl` 文件，而该方案强调将 Prompt 和 LangGraph 的业务逻辑也纳入版本控制。MLflow 在此充当了**LLM Ops 的标准容器**，解决了 Agent 应用部署格式混乱的问题。

---

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为 AI 工程师提供了一个**从笔记本到生产环境的最小阻力路径**。它展示了如何不脱离 AWS 生态，快速构建一个具备企业级治理能力的 AI 应用，避免了自行搭建 MLOps 平台的巨大成本。

**应用场景**
1.  **企业知识库问答**: 结合 RAG（检索增强生成），Agent 可以读取内部文档，并利用 LangGraph 进行多轮推理。
2.  **自动化运维**: Agent 可以解析自然语言指令，调用 AWS API 执行云资源操作。
3.  **金融/医疗合规助手**: 在需要严格审计和版本回溯的领域，MLflow 提供的追踪能力至关重要。

**需要注意的问题**
*   **冷启动延迟**: 无服务器架构在长时间无请求后，首次调用可能有延迟。
*   **上下文限制**: 复杂的 LangGraph 调用链和大量的历史记录可能迅速消耗 Token 限制。
*   **成本**: 虽然 Serverless 节省了运维成本，但在高并发、长上下文场景下，按 Token 付费的成本可能高于自部署模型。

**实施建议**
*   **先本地，后云端**: 先在本地使用 LangGraph 和 MLflow Tracking 调试逻辑。
*   **模块化设计**: 将 LangGraph 的节点设计得尽可能小且独立，便于测试和替换。
*   **监控告警**: 利用 MLflow 的模型监控功能，实时监控生产环境中的模型漂移或性能下降。

---

## 4. 行业影响分析

**对行业的启示**
该案例预示着 **MLOps 正在向 LLOps（Large Language Model Operations）和 Agentic Ops 演进**。未来的 AI 开发不仅仅是训练模型，更多的是**编排逻辑**。行业工具链正在从“以模型为中心”转向“以 Agent 流程为中心”。

**可能带来的变革**
*   **SaaS 的智能化升级**: 传统的 SaaS 软件可以通过集成此类 Agent 架构，迅速获得对话式交互和自动化任务执行能力。
*   **降低 GenAI 落地门槛**: 通过 SageMaker 和 Bedrock 这种全托管服务，中等规模的企业无需组建庞大的基础设施团队即可使用最先进的 Agent 技术。

**发展趋势**
*   **标准化**: Agent 的定义和部署格式将逐渐标准化（类似 MLflow PyFunc 的普及）。
*   **多云与混合部署**: 企业会寻求类似架构但支持私有化部署或跨云的方案（如使用 Kubernetes 替代 SageMaker Serverless）。

---

## 5. 延伸思考

**引发的思考**
*   **Agent 的安全性**: 当 Agent 获得了工具调用权限（如操作数据库、发送邮件），如何通过 LangGraph 的“守门人”节点防止恶意指令执行？
*   **评估的主观性**: MLflow 如何量化 Agent 的“创造力”或“对话流畅度”？目前的指标（如 ROUGE/BLEU）可能不再适用。

**拓展方向**
*   **多模态 Agent**: 将 Claude 的视觉能力集成到 LangGraph 中，处理图片和文档。
*   **人机协同**: 在 LangGraph 中引入 `human_in_the_loop` 节点，让 Agent 在执行关键操作前等待人工确认。

---

## 6. 实践建议

**如何应用到自己的项目**
1.  **环境准备**: 注册 AWS 账户，开通 Bedrock（申请 Claude 模型权限）和 SageMaker Domain。
2.  **依赖安装**: 安装 `langgraph`, `mlflow`, `boto3`, `langchain-aws`。
3.  **开发流程**:
    *   定义 Agent 的数据结构。
    *   编写节点函数（LLM 调用、工具调用）。
    *   构建图并添加边。
    *   使用 `mlflow.langchain.log_model` 记录整个图。
4.  **部署**: 使用 SageMaker 的预置容器或自定义容器部署 MLflow 记录的模型。

**需补充的知识**
*   **Python 异步编程**: LLM 调用是 I/O 密集型，掌握 `asyncio` 对于高并发 Agent 至关重要。
*   **Prompt Engineering**: 如何编写 System Prompt 以控制图的行为。
*   **AWS 基础安全**: IAM 角色权限配置，确保 Agent 只有最小权限。

---

## 7. 案例分析

**成功案例逻辑推演**
假设某电商公司构建**“智能售后助手”**：
*   **阶段一（简单）**: 仅使用 Claude 回答常见问题。
*   **阶段二（Agent）**: 使用 LangGraph。用户说“查一下我上周买的鞋退了没”。Agent 将任务拆解：1. 识别用户 ID -> 2. 调用订单 API -> 3. 判断状态 -> 4. 生成回复。
*   **阶段三（治理）**: 发现 Agent 偶尔会编造物流状态。利用 MLflow 回溯到某个特定的 Prompt 版本，修改 System Prompt 增加约束，重新部署，并记录新版本的实验指标。

**失败反思**
如果忽视了**状态管理**，在多用户并发时，用户 A 可能会看到用户 A 的对话历史混入了用户 B 的信息（如果使用了单例全局变量而非基于线程或检查点的状态管理）。这是无服务器架构下常见的陷阱。

---

## 8. 哲学与逻辑：论证地图

**中心命题**
> **在构建企业级生成式 AI 应用时，采用“Bedrock + LangGraph + SageMaker MLflow”的无服务器架构是平衡开发敏捷性与生产可维护性的最优解。**

**支撑理由**
1.  **敏捷性**: Bedrock 提供了 SOTA 模型（如 Claude 3.5 Sonnet）的即时访问，无需训练，LangGraph 提供了灵活的编程范式来控制模型行为，比单纯的 Prompt Engineering 更强大。
    *   *依据*: LLM 能力天花板已转移至推理与规划，LangGraph 专为有状态的循环推理设计。
2.  **可维护性**: 托管 MLflow 解决了 GenAI 应用“黑盒”问题，提供了版本控制和 lineage（血缘关系）追踪。
    *   *依据*: 工业界共识，没有可观测性的 AI 系统无法在生产环境长期存活。
3.  **成本效益**: Serverless 架构将资本支出转化为运营支出，且无需维护底层基础设施。
    *   *依据*: AWS 的基础设施规模效应。

**反例与边界条件**
1.  **超低延迟场景**: 如果应用要求毫秒级响应（如高频交易辅助），Serverless 的冷启动和网络延迟可能不可接受，此时需要自托管模型或使用专用实例。
2.  **数据主权严格场景**: 如果数据严禁出境，而 Bedrock 某些模型部署在特定区域，或者企业完全禁止使用公有云

---
## 最佳实践

## 最佳实践指南

### 实践 1：架构设计与无服务器计算优化

**说明**: 在构建基于 Claude 和 LangGraph 的对话式 AI 代理时，应充分利用 Amazon SageMaker AI 的无服务器特性。通过将 LangGraph 的状态管理逻辑与 AWS Lambda 或 SageMaker Serverless Inference 结合，可以实现自动伸缩和按需计费，避免闲置资源浪费。

**实施步骤**:
1. 使用 LangGraph 定义状态图时，将节点设计为无状态函数，便于水平扩展。
2. 将 SageMaker 端点配置为无服务器推理模式，设置合适的内存大小（如 2048 MB 或 4096 MB）和最大并发数。
3. 利用 Amazon API Gateway 或 Application Load Balancer 作为前端入口，触发后端的 LangGraph 工作流。

**注意事项**: 
- 确保冷启动时间在可接受范围内，可通过预置并发或保持少量热实例来优化。
- 监控 Lambda 或 SageMaker 的并发限制，必要时申请配额提升。

---

### 实践 2：利用 LangGraph 实现复杂的对话状态管理

**说明**: LangGraph 非常适合处理多轮对话中的上下文保持。最佳实践是明确定义对话状态图，包括循环、条件边和节点，以处理用户的打断、话题切换或修正意图。

**实施步骤**:
1. 定义一个清晰的 `State` 对象（TypedDict），包含消息历史、当前意图、上下文数据等字段。
2. 设计图结构时，区分“人类输入”节点和“AI 响应”节点，使用条件边来决定下一步是调用工具、查询知识库还是结束对话。
3. 实现“检查pointer”机制，允许在对话出错或需要人工介入时回滚到特定状态。

**注意事项**: 
- 避免状态无限增长，定期对消息历史进行摘要或截断，以控制 Token 消耗。
- 确保图的逻辑是确定性的，便于调试和追踪。

---

### 实践 3：集中化模型管理与 MLflow 集成

**说明**: 使用托管在 SageMaker 上的 MLflow 来管理 Claude 模型提示词、LangGraph 的构建逻辑以及中间件的版本。这有助于实验的可复现性和生产环境的快速迭代。

**实施步骤**:
1. 在 SageMaker Studio 中启动 MLflow 实验追踪服务器。
2. 将 Claude 的 Prompt 模板、系统提示词以及 LangGraph 的配置参数记录为 MLflow Parameters。
3. 将 LangChain 组件的序列化对象或模型配置记录为 MLflow Artifacts，使用 `mlflow.langchain` 模块进行自动记录。
4. 为每个成功的对话流程部署注册一个 MLflow Model，以便于通过 SageMaker 进行一键部署。

**注意事项**: 
- 敏感信息（如 API Key）不要硬编码在日志中，应使用 SageMaker Secret Manager 或环境变量。
- 定期清理无效的实验运行，保持 MLflow 后端存储的整洁。

---

### 实践 4：提示词工程与上下文优化

**说明**: Claude 模型对提示词非常敏感。在通过 SageMaker 调用 Bedrock 中的 Claude 时，应精心设计系统提示词，并利用 LangGraph 的节点动态构建上下文，以减少幻觉并提高准确性。

**实施步骤**:
1. 在 LangGraph 的“Agent”节点中，构建包含角色定义、任务约束和输出格式的系统提示词。
2. 实施检索增强生成（RAG）模式：在特定节点中调用 Amazon OpenSearch 或 Kendra 获取相关文档，并将检索结果注入到 Claude 的上下文窗口中。
3. 使用 Claude 的长上下文窗口能力（如 200k tokens），但通过动态截断策略仅保留最相关的历史对话。

**注意事项**: 
- 严格控制 Prompt 注入攻击，不要直接将未经处理的用户输入拼接进系统提示词。
- 测量不同 Prompt 版本的延迟和成本，在 MLflow 中进行对比。

---

### 实践 5：可观测性与监控

**说明**: 在无服务器架构中，传统的日志收集变得困难。必须利用 AWS CloudWatch、X-Ray 和 SageMaker 的内置监控功能来追踪 LangGraph 的执行路径和 Claude 的调用性能。

**实施步骤**:
1. 在 LangGraph 的每个节点函数中添加结构化日志输出，并打印到 CloudWatch Logs。
2. 启用 AWS X-Ray 追踪，以可视化请求从 API Gateway 穿过 LangGraph 逻辑到达 Bedrock 的完整链路。
3. 配置 CloudWatch Alarms，监控错误率（如 4xx/5xx）、延迟（P95/P99）和 Throttle 次数。
4. 利用 SageMaker Model Monitor 监控数据漂移（如果涉及微调或 RAG 检索质量）。

**注意事项**: 
- 确保日志级别在生产环境中调整为 INFO 或 WARN，避免 DEBUG 级别日志产生额外费用。
- 注意采样率配置，以平衡追踪粒度和 X-Ray 成本。

---

### 实践 6：安全性与权限控制

**

---
## 学习要点

- 利用 LangGraph 构建基于 Claude 的有状态对话智能体，通过定义节点、边和条件边实现复杂的对话流程控制与状态管理。
- 使用托管 MLflow 与 Amazon SageMaker AI 深度集成，实现对话模型的集中化实验跟踪、版本管理及自动化部署，简化 MLOps 流程。
- 采用 Amazon Bedrock 托管的 Claude 模型作为推理核心，无需自行维护基础设施即可获得高性能的大语言模型能力。
- 将 SageMaker AI 作为模型训练与部署平台，能够托管自定义的 LangChain 包装器，从而将对话智能体作为标准机器学习模型进行服务化。
- 通过 LangGraph 的记忆机制与图结构设计，解决传统无状态聊天机器人无法处理多轮复杂上下文的痛点。
- 利用 MLflow 的 LangChain 自动记录功能，自动捕获超参数、指标和模型构件，显著提升了 AI 应用的可复现性与迭代效率。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [LangGraph](/tags/langgraph/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [无服务器架构](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%9E%B6%E6%9E%84/) / [Agent](/tags/agent/) / [Claude](/tags/claude/) / [LLMOps](/tags/llmops/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [基于Amazon SageMaker AI构建无服务器Claude对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于 Amazon Bedrock 构建由 AI 驱动的招聘系统]({{< relref "posts/20260218-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-14.md" >}})
- [基于Amazon Bedrock AgentCore构建统一智能系统]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*