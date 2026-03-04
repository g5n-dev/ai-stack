---
title: "基于Bedrock与LangGraph在SageMaker构建无服务器对话代理"
date: 2026-03-04T01:39:34+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "Agent", "LangGraph", "Amazon Bedrock", "SageMaker", "MLflow", "无服务器", "Claude"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "以下是对该内容的中文总结： 本文探讨了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上托管的 **MLflow**，来构建一个**无服务器的智能对话 AI 代理**。 主要技术架构与组件如下： 1. **核心模型服务**： * 使用 *"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios: ["大语言模型", "AI/ML项目"]
---

# 基于Bedrock与LangGraph在SageMaker构建无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---
## 摘要/简介

本文探讨了如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow 来构建一个智能对话代理。

---
## 导语

随着生成式 AI 在企业级应用中的深入，构建可扩展、可管理的对话系统成为技术关键。本文将介绍如何利用 Amazon Bedrock 中的 Claude 模型，结合 LangGraph 的编排能力以及 Amazon SageMaker AI 上托管的 MLflow，构建一个无服务器的对话 AI 代理。通过本文，您将掌握从模型调用到全链路追踪的完整实现流程，学会利用云端托管服务简化开发与运维，高效构建生产级的智能应用。

---
## 摘要

以下是对该内容的中文总结：

本文探讨了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上托管的 **MLflow**，来构建一个**无服务器的智能对话 AI 代理**。

主要技术架构与组件如下：

1.  **核心模型服务**：
    *   使用 **Claude**（通常通过 Amazon Bedrock 调用）作为底层大语言模型（LLM），提供强大的自然语言处理与生成能力。

2.  **应用编排框架**：
    *   利用 **LangGraph** 构建代理的工作流。LangGraph 适合创建有状态、循环的图状结构，能够管理对话的上下文和复杂的多步骤推理。

3.  **实验管理与追踪**：
    *   集成 **Amazon SageMaker AI** 上托管的 **MLflow**。这用于集中管理机器学习模型的整个生命周期，包括实验追踪、模型注册以及版本管理，确保开发过程的可追溯性和模型部署的标准化。

**核心优势：**
该方案采用**无服务器**架构，意味着开发者无需管理底层基础设施，即可快速构建、扩展和部署高性能的对话式 AI 系统。

---
## 评论

### 中心观点
该文章展示了一种**“模型编排与可观测性解耦”**的企业级生成式AI落地范式，即利用 Amazon SageMaker AI 的托管 MLflow 解决 LangGraph 构建的多步推理应用中的模型评估与追踪难题，旨在解决生产环境中“黑盒模型”难以治理的痛点。

### 深入评价与分析

#### 1. 内容深度：严谨但偏向“全家桶”式解决方案
*   **支撑理由（事实陈述/你的推断）：**
    文章的技术深度体现在**将 LangGraph 的状态机逻辑与 MLflow 的实验管理能力进行了实质性整合**。通常，LangGraph 示例仅展示如何通过代码构建循环图，而较少讨论如何追踪图内部每一个节点的性能。该文利用 SageMaker 上托管的 MLflow，不仅记录了 LLM 的输入输出，还试图记录中间推理步骤，这对于构建复杂的 Agent（如需要多步推理的场景）至关重要。这不仅是代码堆砌，而是对 MLOps 原理在 LLM 时代的正确应用。
*   **反例/边界条件（事实陈述/你的推断）：**
    文章可能**过度简化了“评估”的难度**。MLflow 擅长记录日志和传统的 ML 指标，但对于 Agent 产生的非结构化文本输出，仅靠 MLflow 自带的 UI 很难直接判断质量。文章可能未深入探讨如何构建“基于 LLM 的评估器”来自动打分，而是更多停留在“记录和回溯”层面。此外，对于 Bedrock 等托管服务，MLflow 可能无法直接捕获模型内部的 Token 级别细节，导致可观测性存在盲区。

#### 2. 实用价值：填补了 Serverless 架构下的治理空白
*   **支撑理由（事实陈述）：**
    对于已经深度绑定 AWS 生态的企业，该方案具有极高的参考价值。它解决了 LangGraph 开发者面临的一个具体痛点：**在无服务器架构下如何保留调试信息**。传统的本地调试文件无法在生产环境复用，而利用 SageMaker 托管的 MLflow 提供了一个中心化的数据湖，使得团队可以复现对话历史、调试 Chain 的逻辑分支，这是从 Demo 走向 Production 的关键一步。
*   **反例/边界条件（你的推断）：**
    **成本与架构耦合度过高**是主要问题。如果企业仅为了使用 MLflow 而被迫使用 SageMaker，可能会导致 Vendor Lock-in（厂商锁定）。此外，Bedrock + SageMaker 的调用链路可能产生双重网络延迟或数据传输费用，对于高频、低延迟的对话场景，这种架构可能显得过于厚重。

#### 3. 创新性：整合大于创新
*   **支撑理由（作者观点/你的推断）：**
    文章的“新”不在于发明了算法，而在于**验证了一条成熟的工具链**。LangGraph 代表了最新的控制流范式，MLflow 代表了传统的治理标准，将两者在 AWS 云原生环境下打通，本身就是一种工程上的创新实践。它提出了“Serverless Agent”也需要“Serverless Ops”的观点。
*   **反例/边界条件（事实陈述）：**
    这种组合并非唯一解。LangSmith（LangChain 官方平台）在原生支持 LangGraph 追踪方面可能比 MLflow 更丝滑；或者使用 Weights & Biases (W&B) 也能达到类似效果。文章的创新性受限于其作为 AWS 官方博客的营销属性，主要在于推广自家服务，而非提出通用的技术新知。

#### 4. 行业影响：推动“Agentic Workflows”的标准化治理
*   **支撑理由（你的推断）：**
    这篇文章反映了行业正在从“单一 Prompt 工程”向“多 Agent 编排与治理”转型。它向开发者社区传递了一个信号：**构建 Agent 不仅仅是写好 Prompt，更需要建立完善的评估体系**。这将促使更多开发者关注 LLMOps 的具体落地，特别是如何利用现有 MLOps 工具（如 MLflow）兼容新架构（如 LangGraph）。
*   **反例/边界条件（你的推断）：**
    如果 AWS 或其他云厂商不能进一步简化“评估指标”的定义（例如自动化的 Answer Relevance 评分），这种架构仍然只能解决“看见问题”，而不能解决“衡量问题”。行业可能会因此产生一种新的误区：认为有了日志和追踪就等于有了高质量的模型。

### 综合评价与批判性思考

这篇文章是一篇典型的**“架构验证型”**技术文档。它的价值不在于理论突破，而在于**验证了工具链的兼容性**。

从批判性角度来看，我们需要警惕**“工具万能论”**。文章暗示使用了 SageMaker 和 MLflow 就能构建“生产级” Agent，但实际上，生产级 Agent 的最大瓶颈往往在于**非技术因素**（如安全合规、幻觉控制）和**评估指标的科学性**。仅仅把数据存到 MLflow 里，并不代表模型变好了。

此外，**LangGraph 的引入增加了系统的复杂性**。对于简单的问答场景，使用 LangGraph 可能是过度设计。文章未充分讨论何时应该使用简单的 Chain，何时必须使用 Graph，容易引导初级开发者为了用新技术而滥用 Graph。

### 实际应用建议

1.  **评估指标先行：** 在接入 MLflow 之前，先定义好什么是“好的回答”。不要只记录 Log，要利用 MLflow 的 Evaluation 功能配置 LLM-as-a-judge 的自动化评分脚本。
2.  **成本监控：** Bedrock 的按量计费结合 SageMaker 的托管费用，在长对话场景

---
## 技术分析

基于您提供的文章标题《Build a serverless conversational AI agent using Claude with LangGraph and managed MLflow on Amazon SageMaker AI》及其摘要，以下是对该技术方案的全面深入分析。

---

# 深度分析：基于 SageMaker AI 的无服务器对话智能体架构

## 1. 核心观点深度解读

**主要观点与核心思想**
这篇文章的核心观点在于展示一种**现代化的、全托管式的 AI 工程化范式**。作者主张，构建复杂的生成式 AI 应用（如对话 Agent）不应再是传统的“从零搭建”模式，而应采用**“编排 + 托管 + 可观测性”**的组合拳。具体而言，即利用 **Amazon Bedrock** 提供基础模型能力，**LangGraph** 处理复杂的状态与逻辑编排，并依托 **Amazon SageMaker AI** 上的托管 MLflow 来解决全生命周期的管理与追踪问题。

**观点的创新性和深度**
该方案的深度在于它**超越了简单的 API 调用**。传统的 LLM 应用开发往往止步于“Prompt Engineering”或简单的函数调用。而引入 **LangGraph** 意味着应用具备了**状态机**的属性，能够处理循环、分支和记忆，这是从“聊天机器人”向“智能体”跨越的关键。同时，将 **MLflow** 引入 SageMaker 的无服务器环境，解决了“实验”与“生产”割裂的行业痛点，体现了 **MLOps** 在 GenAI 时代的延续与进化。

**为什么这个观点重要**
这一观点极其重要，因为它解决了企业落地 GenAI 的**三大核心障碍**：
1.  **复杂性：** 如何管理 Agent 的多轮对话状态（LangGraph 解决）。
2.  **运维成本：** 如何避免管理底层基础设施（SageMaker 无服务器架构解决）。
3.  **可追溯性：** 如何在非确定性生成环境中调试和评估模型（MLflow 解决）。

## 2. 关键技术要点

**涉及的关键技术**
*   **Amazon Bedrock:** 提供模型（如 Claude 3）的统一接入点，无需自行托管模型。
*   **LangGraph:** 基于 LangChain 的库，专门用于构建有状态、多参与者的循环图结构，是 Agent 的“大脑皮层”。
*   **Amazon SageMaker AI:** 提供无服务器计算环境。
*   **Managed MLflow (on SageMaker):** 用于追踪实验、管理模型版本和注册表。

**技术原理和实现方式**
*   **Agent 编排:** 通过定义 Graph（图）、Nodes（节点，通常是 LLM 或工具调用）和 Edges（边，条件判断路由），将对话流程代码化。LangGraph 维护一个 `State` 对象，在节点间传递，确保上下文的连贯性。
*   **无服务器部署:** 利用 SageMaker 的无服务器推理或容器镜像，将 LangGraph 应用封装为 API 端点。无需预置 EC2 实例，按调用次数和计算时间计费。
*   **LLM 追踪:** 利用 MLflow 的 `mlflow.langchain` 自动追踪功能，自动捕获 Agent 执行过程中的每一个 Prompt、Response 和中间步骤，将其记录到 MLflow Tracking Server。

**技术难点与解决方案**
*   **难点：** Agent 执行路径是非线性的，难以调试。
*   **解决：** MLflow 的 Trace UI 提供了可视化的执行链路，开发者可以直观看到每一步的输入输出、耗时以及错误信息。
*   **难点：** 环境依赖管理混乱。
*   **解决：** 使用容器化或 SageMaker 的预置镜像，结合 MLflow 的 Model Registry，确保“开发环境”与“生产环境”的一致性。

**技术创新点**
将**控制流逻辑**从硬编码代码中剥离到图结构中，并结合**云端原生 MLOps** 平台进行统一管理。这种架构使得 Agent 既可以像传统代码一样版本控制，又可以像数据模型一样性能评估。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为 AI 工程师提供了一套**“开箱即用”的企业级蓝图**。它证明了在不需要庞大运维团队的情况下，小团队也能构建出具备高可用性、可观测性的复杂智能体系统。

**应用场景**
*   **企业知识库问答：** Agent 需要多步检索（RAG）并生成答案，LangGraph 可管理检索与生成的循环。
*   **自动化客服与订单处理：** 需要调用 API 查询库存、修改订单，LangGraph 的条件路由功能至关重要。
*   **金融/医疗合规助手：** 需要严格的审计追踪，MLflow 提供了完整的对话日志用于合规审查。

**需要注意的问题**
*   **冷启动延迟：** 无服务器架构在长时间闲置后首次请求可能有较高延迟。
*   **状态持久化：** LangGraph 的内存状态通常存储在内存中，分布式部署时需配合 Redis 或外部数据库进行持久化。
*   **成本不可控：** 在复杂的循环逻辑中，若陷入死循环或频繁调用 LLM，可能导致 Bedrock API 成本激增。

**实施建议**
先在本地使用 LangChain/LangGraph 开发并验证逻辑，利用 MLflow 本地追踪调试；确认无误后，将代码打包上传至 SageMaker，利用托管 MLflow 进行集中管理，最后开启无服务器端点进行灰度发布。

## 4. 行业影响分析

**对行业的启示**
该方案标志着 **GenAI 正在从“原型阶段”走向“工业化阶段”**。行业关注的焦点从“谁的模型参数大”转移到了“谁能更稳定、更便宜地管理好 Agent 的生命周期”。

**可能带来的变革**
*   **MLOps 的泛化：** 传统的 MLOps 关注模型训练指标，未来的 MLOps 将更关注 Agent 的“轨迹质量”和“工具调用成功率”。
*   **开发角色的融合：** 全栈开发者需要掌握图状态编程，数据科学家需要了解云原生部署，边界逐渐模糊。

**相关领域的发展趋势**
*   **BaaS 蓝图：** 更多云厂商会模仿这种“模型托管 + 编排框架 + 托管 MLOps”的捆绑服务。
*   **标准化：** OpenTelemetry 在 LLM 应用追踪中的地位将进一步提升。

## 5. 延伸思考

**引发的思考**
*   **Agent 的安全性：** 当 Agent 拥有工具调用权限时，如何通过 LangGraph 的“边”来限制其危险操作？是否需要引入“看门狗”节点？
*   **评估的主观性：** MLflow 记录了日志，但如何自动化评估一个对话 Agent 的“好坏”？LLM-as-a-judge 的评估指标如何集成进 MLflow？

**拓展方向**
*   **多模态 Agent：** 结合 Bedrock 的多模态能力（如图片分析），扩展 LangGraph 的处理节点。
*   **人机协同：** 在 LangGraph 中引入 `human_in_the_loop` 节点，让关键决策（如发送邮件、转账）前必须经过人工审核。

## 6. 实践建议

**如何应用到自己的项目**
1.  **环境准备：** 注册 AWS 账户，开通 Bedrock（申请 Claude 模型权限），创建 SageMaker Domain 并启用 MLflow。
2.  **本地开发：** 使用 Python 编写 LangGraph 代码，定义 `State` 和 `Graph`。
3.  **集成追踪：** 在代码中加入 `mlflow.langchain.autolog()`，确保本地运行能看到 Trace。
4.  **容器化：** 编写 `requirements.txt` 和推理脚本，使用 SageMaker 预置容器或自定义容器。
5.  **部署：** 调用 SageMaker Python SDK 将模型部署到无服务器推理端点。

**补充知识**
*   **图论基础：** 理解有向图的概念。
*   **异步编程：** LangGraph 大量使用 Python 的 `asyncio`，需熟悉异步写法。
*   **AWS IAM 权限管理：** 确保 SageMaker 角色有权限调用 Bedrock 和访问 MLflow。

## 7. 案例分析

**成功案例模拟：电商智能导购 Agent**
*   **场景：** 用户询问“我要买一双适合跑步的鞋，预算500元”。
*   **流程：**
    1.  **意图识别节点：** 识别为“购买咨询”。
    2.  **检索节点：** 调用商品数据库 API（LangGraph 的 Tool Node）。
    3.  **推荐节点：** 将检索结果输入 Claude，生成自然语言推荐。
    4.  **MLflow 追踪：** 记录了检索 API 返回了 5 个商品，Claude 选中了其中 3 个进行推荐。
*   **价值：** 整个过程在无服务器架构上运行，流量高峰时自动扩容，无需人工干预服务器。

**失败反思**
若未使用 LangGraph 而使用简单的 `if-else`，当用户说“不要红色的，要蓝色的”时，Agent 可能无法理解上下文关联。若未使用 MLflow，当 Agent 推荐了错误的商品，开发者无法回溯是 API 返回了空数据还是 LLM 理解错误。

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级生成式 AI 应用时，采用 **"Bedrock + LangGraph + SageMaker MLflow"** 的全托管编排架构，比传统的自建微服务架构具有更高的**工程效率**和**可维护性**。

**支撑理由与依据**
1.  **理由 1：复杂逻辑的可控性。**
    *   *依据：* LangGraph 将 Agent 行为建模为状态机，显式处理循环和分支，相比隐式的 Prompt 嵌套更易于逻辑推演和错误排查。
2.  **理由 2：运维成本的最小化。**
    *   *依据：* 无服务器架构消除了对底层基础设施（GPU/OS）的管理需求，按需计费模式降低了非高峰期的闲置成本。
3.  **理由 3：调试过程的可观测性。**
    *   *依据：* 托管 MLflow 提供了标准化的追踪界面，解决了 LLM 应用“黑盒”特性带来的调试难题，实现了从实验到生产的全链路监控。

**反例或边界条件**
1.  **边界条件 1：超低延迟要求。** 如果应用需要毫秒级响应（如高频交易辅助），无服务器架构的冷启动和网络延迟可能使其不可接受，此时需使用裸金属或预留实例。
2.  **边界条件 2：极度敏感的数据合规。** 某些严苛的合规场景可能要求数据不能离开本地私有云，此时无法使用公有云的 Bedrock 服务。

**命题性质分析**
*   **事实：** LangGraph 支持循环图；SageMaker 支持 MLflow；Bedrock 提供 API。
*   **价值判断：** “更高”的工程效率和可维护性（这取决于具体业务场景和团队背景）。
*   **可检验预测：** 采用该架构的团队，其从“原型”到“生产环境”的部署时间将比传统方式缩短 X%，且 Bug 排查时间将缩短 Y%。

**立场与验证方式**
*   **立场：** 支持。对于绝大多数中低并发、逻辑复杂度中等的商业 AI 应用，这是

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建健壮的 LangGraph 状态管理架构

**说明**:
在构建基于 Claude 的对话代理时，LangGraph 的状态图是核心组件。最佳实践是设计一个结构化的状态模式，明确区分对话历史、用户输入、中间步骤和最终输出。使用 TypedDict 定义状态结构，确保类型安全，并利用 LangGraph 的图结构来处理复杂的对话流转，包括回退、分支和循环逻辑，而不是简单的线性链。

**实施步骤**:
1. 使用 Python 的 `typing.TypedDict` 定义严格的状态 Schema，包含 `messages`、`next_action` 等关键字段。
2. 设计节点函数时，确保每个节点只更新它负责的状态片段，保持函数的幂等性。
3. 在图中实现条件边，根据模型输出（如工具调用需求）动态路由到不同的处理节点。
4. 配置 `checkpointer`（如使用 `MemorySaver` 或 DynamoDB），以支持对话历史的持久化和中断恢复。

**注意事项**:
避免在状态中存储过大的上下文窗口，这会增加延迟和 Token 消耗。应实施摘要策略，将旧对话压缩。

---

### 实践 2：利用 MLflow 实现严格的模型与提示词版本控制

**说明**:
在生产环境中部署 AI 代理时，必须对 LangChain 组件、Prompt 模板和 Claude 模型参数进行严格的版本控制。利用 SageMaker 托管的 MLflow 可以记录每一次实验的配置、参数和结果。这不仅有助于复现最佳结果，还能在需要时快速回滚到之前的稳定版本，实现 MLOps 的闭环。

**实施步骤**:
1. 在初始化 LangGraph 或 Chain 时，使用 `mlflow.langchain.autolog()` 自动捕获配置参数。
2. 为每一个 Prompt 模板变更创建独立的 MLflow Run，并打上有意义的 Tag（如 `prompt_v2`, `aggressive_mode`）。
3. 将经过验证的 LangGraph 逻辑注册为 MLflow Model，加载到 SageMaker 模型注册表中。
4. 在部署时，引用具体的 Model Version URI，而不是使用“最新”这种模糊的引用。

**注意事项**:
确保敏感信息（如 API Key）不被记录到 MLflow 参数中，使用环境变量或 Secrets Manager 管理凭证。

---

### 实践 3：设计高效的 Serverless 计算与冷启动优化策略

**说明**:
Serverless 架构（如 AWS Lambda）虽然能显著降低成本，但可能导致冷启动延迟，影响对话体验。最佳实践是将 LangGraph 的初始化逻辑与执行逻辑分离。利用 Lambda 的 SnapStart（针对 Java）或 Provisioned Concurrency（针对 Python）来保持环境热度，并优化依赖包的大小以加快加载速度。

**实施步骤**:
1. 将 LangGraph 构建图和加载 MLflow 模型的逻辑放在 Lambda Handler 外部（全局区域），以便在容器复用时重用。
2. 创建 Lambda 层或将依赖项打包到优化后的容器镜像中，减小部署包体积。
3. 配置 Provisioned Concurrency 以维持最小数量的热实例，确保首字节响应（TTFB）符合实时对话要求。
4. 实施异步处理模式，对于耗时较长的 Claude 推理调用，使用流式响应或异步回调。

**注意事项**:
监控 Lambda 的 Duration 和 Memory 使用率，调整内存分配。有时增加内存配置可以显著缩短 CPU 密集型任务（如模型初始化）的执行时间。

---

### 实践 4：实施基于反馈的模型评估与监控循环

**说明**:
仅仅部署代理是不够的，必须持续评估其质量。利用 MLflow 的评估功能结合 SageMaker，可以建立自动化流水线。通过“黄金数据集”对 Claude 回复的相关性、准确性和毒性进行评分。同时，在生产环境中记录用户交互日志，定期用于微调或 Prompt 优化。

**实施步骤**:
1. 构建一个包含典型用户查询和预期回复的“黄金数据集”。
2. 使用 MLflow 的 `mlflow.evaluate()` API，配置评估器（如基于 Claude 的 LLM-as-a-Judge）来对新版本进行离线测试。
3. 在 LangGraph 节点中集成日志记录，将 Trace 数据发送回 MLflow 或 CloudWatch。
4. 建立告警机制，当模型输出的置信度低或用户负面反馈率高时触发警报。

**注意事项**:
评估指标应与业务目标对齐。除了传统的 ROUGE/BLEU 分数，更应关注基于 LLM 的语义相似度评分（如 `answer_relevance`）。

---

### 实践 5：强化安全性与数据隐私保护

**说明**:
对话式 AI 代理通常处理敏感用户数据。在 Serverless 环境中，必须确保数据传输和存储的安全，并防止 Prompt 注入攻击。利用 VPC 端点连接 SageMaker 和 MLflow，避免流量暴露在公共互联网中。同时，在 Prompt 层面设置护栏，过滤恶意输入。

**实施步骤**:
1. 将 Lambda 函数配置在私有

---
## 学习要点

- 利用 LangGraph 构建基于 Claude 的有状态对话代理，通过循环图结构管理对话历史和上下文，实现比传统链式结构更灵活的复杂交互逻辑。
- 在 SageMaker 上使用托管 MLflow 实现模型全生命周期管理，集中追踪实验参数、版本和性能指标，从而加速迭代并优化模型效果。
- 采用无服务器架构部署 AI 应用，利用 SageMaker 的按需计费和自动扩缩容能力，在降低基础设施运维成本的同时保障高可用性。
- 通过将 Claude 3 模型与 LangGraph 的工具调用能力结合，使智能体具备执行外部函数和实时数据检索的能力，有效解决大模型幻觉问题。
- 利用 Amazon Bedrock 提供的 Claude 模型 API，无需自行维护底层模型基础设施，即可快速构建高性能的生成式 AI 应用。
- 借助 LangGraph 的预置检查点机制，自动维护对话的内部状态，确保在多轮对话和长流程任务中的上下文连贯性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [LLM](/tags/llm/) / [Agent](/tags/agent/) / [LangGraph](/tags/langgraph/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [Claude](/tags/claude/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [基于Amazon SageMaker AI构建无服务器Claude对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [在SageMaker AI上基于Bedrock与LangGraph构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-11.md" >}})
- [基于Bedrock与LangGraph构建无服务器对话代理及SageMaker MLflow管理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-12.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*