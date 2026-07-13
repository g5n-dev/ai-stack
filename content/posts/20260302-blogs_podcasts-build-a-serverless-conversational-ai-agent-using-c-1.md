---
title: 基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理
date: 2026-03-02 20:08:34+08:00
draft: false
entry_kind: auto
tags:
- LangGraph
- Amazon Bedrock
- SageMaker
- MLflow
- Agent
- LLM
- 无服务器
- RAG
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: '**标题：使用 Amazon Bedrock、LangGraph 和 SageMaker AI 构建无服务器对话 AI 智能体** **概述**
  本文档介绍了如何利用 **Amazon Bedrock**（Claude 模型）、**LangGraph** 以及托管在 **Amazon SageMaker
  AI** 上的'
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios:
- AI/ML项目
- 大语言模型
- RAG应用
---

# 基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---

## 摘要/简介

本文探讨如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow 来构建一个智能对话代理。

---

## 导语

构建具备记忆与状态管理能力的对话代理，已成为提升交互体验的关键。本文将介绍如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow，搭建一套无服务器架构的智能对话系统。通过解析技术细节与实施路径，帮助开发者在简化运维的同时，高效实现对话流程的编排与全生命周期管理。

---

## 摘要

**标题：使用 Amazon Bedrock、LangGraph 和 SageMaker AI 构建无服务器对话 AI 智能体**

**概述**
本文档介绍了如何利用 **Amazon Bedrock**（Claude 模型）、**LangGraph** 以及托管在 **Amazon SageMaker AI** 上的 **MLflow**，构建一个智能的、无服务器的对话 AI 智能体。该架构旨在实现高性能的生成式 AI 应用，同时具备强大的可观测性和管理能力。

**核心架构与组件**

该解决方案主要由以下三个核心部分组成：

1.  **Amazon Bedrock (模型层):**
    *   作为基础模型服务，提供 **Claude** 等 LLM 能力，用于处理自然语言理解、推理和生成。
    *   通过无服务器架构，无需管理底层基础设施。

2.  **LangGraph (编排层):**
    *   用于构建智能体的**有状态工作流**和**循环图**结构。
    *   LangGraph 允许开发者定义复杂的对话逻辑（例如：多轮对话、工具调用、循环检查），使智能体不仅能回答问题，还能根据上下文进行规划和执行一系列操作。

3.  **Amazon SageMaker AI + MLflow (管理与追踪层):**
    *   **SageMaker AI** 提供托管的 MLflow 服务。
    *   **MLflow** 在此扮演关键角色，用于**追踪实验**（Tracing）、记录模型参数和版本。
    *   它将 LLM 的调用链、提示词 和响应数据记录下来，为开发者提供了全链路的可观测性，便于调试和优化智能体性能。

**工作流程总结**

1.  **用户交互**：用户向应用发起请求。
2.  **智能体处理**：LangGraph 编排智能体逻辑，决定何时调用 Amazon Bedrock 中的 Claude 模型或使用特定工具。
3.  **推理与执行**：Claude 处理输入并生成响应或操作指令。
4.  **记录与监控**：所有的推理过程、Prompt 和结果均通过 SageMaker 托管的 MLflow 进行记录和追踪。

**主要优势**

*   **无服务器**：利用 Amazon Bedrock 和 SageMaker 的无服务器特性，无需预置服务器，按需付费，降低了运维成本。
*   **状态管理**：LangGraph 解决了传统无

---

## 评论

### 中心观点
这篇文章展示了一种**以全托管云服务为核心、高度工程化**的企业级生成式 AI 落地范式，主张通过 Amazon Bedrock（模型层）、LangGraph（编排层）与 SageMaker（治理层）的深度耦合，来解决大模型应用从原型到生产环境过程中的“最后一公里”治理与部署难题。

---

### 深入评价

#### 1. 内容深度与论证严谨性
**支撑理由：**
*   **全栈闭环的视角：** 文章没有停留在简单的 API 调用演示，而是构建了一个完整的 AI 工程生命周期。它将 MLflow 引入 LLM 开发流程是一个亮点。传统的 LLM 教程往往忽视“评估”和“追踪”，而该文章利用 SageMaker 上托管的 MLflow 解决了 LLM 应用中难以量化的评估问题，论证了从实验到部署的治理闭环。
*   **状态机管理的必要性：** 引入 LangGraph 而非简单的 LangChain，体现了对对话状态管理（CSM）复杂度的深刻理解。在多轮对话中，单纯的线性链路难以处理回退、分支和上下文记忆，文章通过图结构来管理 Agent 的行为逻辑，在技术架构上具备较高的严谨性。

**反例/边界条件：**
*   **厂商锁定的隐性成本：** 文章默认读者完全处于 AWS 生态中。对于混合云部署或边缘计算场景，这种深度依赖 SageMaker 和 Bedrock 的架构会导致极高的迁移成本。
*   **过度工程化的风险：** 对于简单的检索增强生成（RAG）需求，引入 LangGraph 的状态机和 MLflow 的全套治理可能属于“杀鸡用牛刀”，增加了系统复杂度和延迟。

#### 2. 实用价值与创新性
**支撑理由：**
*   **解决“运维”痛点：** 对于企业开发者而言，最大的痛点不是写 Prompt，而是如何监控模型表现、管理版本和部署服务。文章详细展示了如何利用 SageMaker 的托管服务来免除基础设施的运维负担，具有极高的实战参考价值。
*   **工具链的标准化尝试：** 将 MLflow（传统 ML 领域的标准）与 LLM 开发结合，并提出在 SageMaker 上托管 MLflow，这是一种试图在企业内部建立统一标准的创新尝试，有助于打破数据科学团队和 LLM 工程师之间的隔阂。

**反例/边界条件：**
*   **成本控制缺失：** 文章未深入探讨 Bedrock 按Token计费与 SageMaker 实例租用成本叠加后的经济性问题。对于初创公司，这种全托管方案的成本可能远高于自建开源模型服务。
*   **开源替代方案的竞争力：** LangGraph 虽然强大，但并非唯一选择。对于习惯使用 AutoGen 或微软 Semantic Kernel 的团队，该方案的技术栈迁移学习成本较高。

#### 3. 可读性与行业影响
**支撑理由：**
*   **清晰的架构分层：** 文章结构通常遵循“基础设施 -> 编排逻辑 -> 治理评估”的逻辑，符合技术人员的认知习惯。
*   **行业风向标：** 该文章反映了行业趋势：**大模型应用正在从“Prompt Engineering”转向“AI Engineering”**。重点不再是魔法般的 Prompt，而是如何利用成熟工具链构建可观测、可扩展的系统。这推动了行业从“炫技”向“工程化落地”转变。

**反例/边界条件：**
*   **技术栈割裂：** 对于不熟悉 AWS 术语（如 Bedrock, SageMaker）的开发者，文章中充斥的云厂商专有名词可能会造成阅读障碍，掩盖了核心的算法逻辑。

---

### 综合分析与建议

**事实陈述：** 文章提供了一个基于 AWS 云原生技术栈的 Serverless Agent 构建蓝图。
**作者观点：** 作者倾向于认为云原生的托管服务是构建生产级 AI 应用的最佳路径，强调了可视化和治理的重要性。
**你的推断：** 这类文章通常由云厂商技术团队撰写，旨在通过解决工程痛点来锁定用户进入其生态系统。虽然技术方案先进，但本质上是一种“技术壁垒”的构建。

**争议点：**
目前业界对于 Agent 的架构存在两条路线：一条是以 LangGraph 为代表的**确定性状态机路线**（文章所采用），另一条是以完全自主的 LLM 驱动的**规划反思路线**（如 ReWoo, Voyager）。文章的方案虽然可控，但可能牺牲了 Agent 的自主探索能力。

**实际应用建议：**
1.  **适用场景：** 该架构非常适合金融、医疗等对合规性、审计追踪（MLflow）和高可用性要求极高的企业级应用。
2.  **架构解耦：** 建议开发者参考其架构思想，但可以将 Bedrock 替换为本地部署的开源模型（如 Llama 3），将 SageMaker 替换为 Kubernetes，以避免厂商锁定。
3.  **评估先行：** 在引入 LangGraph 复杂逻辑前，先利用 MLflow 建立好基线模型评估，避免在复杂的图结构中难以定位性能下降的瓶颈。

---

### 可验证的检查方式

1.  **延迟基准测试：**
    *   *操作：* 在高并发场景下，测试经过 SageMaker 托管 MLflow 追踪和 LangGraph 编排后的端到端响应延迟。
    *   *预期：* 验证相比直接调用 Bedrock API，引入 LangGraph 和 MLflow 后的额外延迟是否在可接受范围内（通常 < 500ms）。

---

## 技术分析

基于您提供的文章标题和摘要，以及对Amazon SageMaker AI、Bedrock、LangGraph和MLflow等技术栈的深入理解，以下是对该技术方案的全面深度分析。

---

### 深度分析：基于 SageMaker AI、Bedrock 与 LangGraph 构建无服务器对话式 Agent

### 1. 核心观点深度解读

**主要观点：**
文章的核心观点在于展示一种**“全托管、模块化、可观测”**的企业级 AI Agent 架构范式。它主张利用 Amazon SageMaker AI 的托管 MLflow 进行实验追踪，结合 LangGraph 的状态管理能力，并通过 Amazon Bedrock 调用 Claude 模型，从而构建出一个高性能、低维护成本的“无服务器”对话系统。

**核心思想：**
作者试图传达**“关注点分离”**与**“工程化治理”**的思想。
1.  **关注点分离**：将大模型的推理能力交给 Bedrock，将业务逻辑的流转交给 LangGraph，将开发过程的追踪和模型管理交给 MLflow。
2.  **工程化治理**：在 GenAI 应用开发中，仅仅“跑通”是不够的，必须像传统机器学习一样，对 Prompt、参数、Agent 路由轨迹进行严格的版本管理和实验追踪。

**创新性与深度：**
*   **创新性**：该方案将 LangGraph（通常用于本地或自托管环境的编排框架）与 AWS 全托管生态深度结合，特别是利用 **SageMaker 上托管的 MLflow**。这解决了开源 LLM Ops 工具难以在云原生环境下标准集成的痛点。
*   **深度**：它超越了简单的“聊天机器人”Demo，深入到了**Agent 的循环控制**和**模型全生命周期管理（MLLCM）**。它不仅仅是在调用 API，而是在构建一个可以自我反思、拥有记忆、且其开发过程可被复现的智能体。

**重要性：**
随着企业从“玩票式”的 PoC（概念验证）转向生产环境部署，**可观测性**和**扩展性**成为最大瓶颈。该架构提供了一条标准化的落地路径，解决了“Agent 难以调试”和“模型迭代难以回溯”两大难题。

### 2. 关键技术要点

### 涉及的关键技术
*   **Amazon Bedrock**：基础模型服务层，提供 Claude 3/3.5 等模型，无需管理基础设施。
*   **LangGraph**：基于有向图的 Agent 编排框架，支持循环、状态管理和持久化，是构建复杂 Agent 的核心。
*   **Managed MLflow on SageMaker**：开源 MLflow 平台的托管版本，用于 MLflow Tracking（记录指标、参数、模型工件）和 Model Registry。
*   **Amazon SageMaker AI**：提供计算环境（可能是 Serverless Inference 或 Real-time Endpoints）来运行 LangGraph 应用。

### 技术原理与实现
1.  **Graph 架构**：不再是简单的线性 Prompt-Response，而是定义节点和边。例如，一个节点负责意图识别，一个节点负责调用工具，一个节点负责生成最终回复。LangGraph 维护一个全局状态对象，在节点间传递。
2.  **无服务器部署**：LangGraph 应用通常打包为容器或通过特定适配器部署在 SageMaker 上，利用 SageMaker Serverless Inference 或 Bedrock 的 Agent 能力实现按需扩缩容。
3.  **追踪集成**：在 Agent 执行过程中，将 Claude 的 Input/Output tokens、Temperature、Top-P 等参数，以及 Agent 的中间步骤（如调用了哪个工具、返回了什么结果）自动记录到 MLflow 实验中。

### 技术难点与解决方案
*   **难点：状态持久化与无状态 API 的冲突。**
    *   *解决方案*：LangGraph 内置了检查点机制，可以将对话状态保存到外部存储（如 S3 或 DynamoDB），在无服务器环境下实现多轮对话的上下文保持。
*   **难点：LangChain/LangGraph 的“黑盒”调试困难。**
    *   *解决方案*：利用 MLflow 的 `langchain` 自动记录追踪功能，可视化整个 Agent 的执行链路。

### 3. 实际应用价值

### 指导意义
该架构为**企业级 AI 应用开发**提供了一套标准“样板代码”。它证明了如何在不牺牲开发体验（使用开源框架 LangGraph）的前提下，获得企业级的稳定性（AWS 托管服务）。

### 适用场景
*   **企业知识库问答**：需要复杂的检索增强生成（RAG）和多跳推理。
*   **金融/医疗合规助手**：需要严格的对话历史记录、参数可追溯性（MLflow 满足合规审计需求）。
*   **自动化客服与任务执行**：不仅仅是回答问题，还需要通过 API 执行操作（如订票、查询订单）的 Agent。

### 需要注意的问题
*   **成本**：虽然无服务器免除了运维成本，但在高并发、长上下文的 Agent 场景下，Bedrock 的 Token 调用费用和 SageMaker 的计算费用可能不低。
*   **延迟**：Agent 编排涉及多次模型调用和工具调用，端到端延迟较高，不适合实时性要求极高的场景。

### 实施建议
*   **先追踪，后优化**：在开发初期务必开启 MLflow Tracking，积累数据，否则后期无法优化 Prompt 或参数。
*   **模块化设计**：将 LangGraph 中的节点设计得尽可能小且单一职责，便于测试和替换。

### 4. 行业影响分析

### 对行业的启示
这标志着 **LLMOps（大模型运维）正在走向标准化和云原生化**。过去是“手搓代码+ OpenAI API”，现在是通过成熟的编排框架和云厂商的托管模型平台进行工业化生产。

### 可能带来的变革
*   **开发角色的转变**：AI 工程师不再需要关注 CUDA 驱动或 GPU 部署，而是专注于 Graph 的逻辑设计和 Prompt 的微调。
*   **SageMaker 的定位强化**：SageMaker 正从传统的“模型训练平台”转变为“GenAI 全栈开发平台”，通过托管 MLflow 锁定了开发者的工作流。

### 发展趋势
*   **Graph-as-a-Code**：未来的 AI 应用开发将更像画流程图，LangGraph 等状态图模式将成为主流。
*   **统一可观测性**：传统的 APM（应用性能监控）与 LLM 的 Token 追踪将深度融合。

### 5. 延伸思考

*   **多模态扩展**：目前的架构主要基于文本。如何利用 Claude 的多模态能力，在 LangGraph 中处理图片或音频流？
*   **人机协同**：LangGraph 支持在图节点中插入“人工中断”。这意味着 Agent 可以在遇到不确定的情况时，将状态挂起，等待人工审批后再继续执行，这在金融交易审批中极具价值。
*   **边缘计算**：虽然这是无服务器架构，但为了隐私和低延迟，是否可以将 LangGraph 的部分逻辑下沉到 CloudFront 或边缘设备？

### 7. 案例分析

### 成功案例逻辑
*   **场景**：一家大型电商的售后机器人。
*   **问题**：用户问题复杂，可能涉及退款、查物流、投诉，单一 Prompt 无法覆盖。
*   **应用**：使用 LangGraph 构建路由器。第一层判断意图；第二层如果是查物流，调用物流 API；如果是退款，进入“收集信息-验证-执行”的循环子图。
*   **成效**：通过 MLflow 发现“验证”节点的错误率较高，针对性调整了该节点的 Prompt，使问题解决率提升了 30%。

### 失败反思
*   **场景**：构建实时游戏 NPC 对话。
*   **问题**：采用了该架构，但 LangGraph 的多次跳转和 Bedrock 的推理延迟导致 NPC 回复需要 3-5 秒。
*   **教训**：该架构虽然强大，但并非“银弹”。对于超低延迟场景，仍需考虑小模型（如 SLM）的本地部署或流式输出优化。

### 8. 哲学与逻辑：论证地图

**中心命题：**
> **在构建企业级生成式 AI 应用时，采用“Amazon Bedrock + LangGraph + 托管 MLflow”的无服务器架构，是目前平衡开发敏捷性、系统可维护性与生产可观测性的最优解。**

**支撑理由：**
1.  **理由一（敏捷性）：** LangGraph 提供了声明式的状态管理，比命令式代码更能精确控制 Agent 的复杂逻辑流（如回退、重试、分支）。
    *   *依据*：传统代码编写复杂 Agent 逻辑容易陷入“回调地狱”，状态图是处理此类问题的成熟计算机科学范式。
2.  **理由二（可维护性）：** 无服务器架构消除了基础设施维护的负担，使团队专注于业务逻辑。
    *   *依据*：AWS 负责底层高可用性和安全补丁，降低了运维门槛和总拥有成本（TCO）。
3.  **理由三（可观测性）：** 托管 MLflow 提供了标准化的模型和追踪管理，解决了 LLM 应用“黑盒”难以调试和迭代的问题。
    *   *依据*：生产环境中，没有 Trace 数据的 Agent 是无法优化的，MLflow 提供了这种数据基础。

**反例或边界条件：**
1.  **边界条件（成本敏感型）：** 对于超大规模、高并发且逻辑简单的应用（如简单的摘要任务），无服务器架构按 Token 和请求数计费的成本可能远高于自建微服务部署开源模型。
2.  **边界条件（数据隐私）：** 对于涉及极度敏感数据、严禁出域的场景，无法使用公有云的 Bedrock 服务，必须转向私有化部署。

**命题性质分析：**
*   **事实判断**：LangGraph 支持 StateGraph；MLflow 支持 LangChain 追踪；Bedrock 支持 Claude。
*   **价值判断**：“最优解”是一种价值判断，假设了“敏捷性”和“可维护性”的权重高于“极致性能”或“极致数据隐私”。
*   **可检验预测**：采用此架构的团队，其从 PoC 到生产环境的迭代速度将快于采用纯自建架构的团队

---

## 最佳实践

### 实践 1：构建健壮的 LangGraph 状态管理架构

**说明**: 在使用 LangGraph 构建对话 Agent 时，状态管理是核心。通过定义清晰的 TypedState 结构，确保对话历史、上下文和中间结果在不同节点间准确传递。对于复杂的对话流，应设计能够处理循环和条件分支的图结构，避免线性架构的局限性。

**实施步骤**:
1. 使用 `TypedDict` 定义 Agent 的状态模式，明确包含 `messages`、`user_input` 和 `agent_outcome` 等字段。
2. 在 LangGraph 中设计条件边，根据模型输出（如工具调用需求或直接回复）路由到不同的节点。
3. 实现检查点机制，利用 LangGraph 的内存持久化功能保存对话状态，以便支持中断和恢复。

**注意事项**: 确保状态序列化与 MLflow 的日志记录兼容，避免在状态中存储无法序列化的对象（如文件句柄或数据库连接）。

---

### 实践 2：利用 SageMaker 无服务器端点实现弹性推理

**说明**: 为了优化成本和资源利用率，应配置 SageMaker 无服务器端点来部署 Claude 模型或 LangGraph 应用。此实践消除了管理底层基础设施的需要，并自动根据请求流量进行扩缩容，非常适合具有间歇性流量的对话应用。

**实施步骤**:
1. 在 SageMaker 控制台中或通过 Boto3 创建模型实体，指向 ECR 中的 LangGraph 应用镜像或 Claude 模型配置。
2. 配置端点配置，选择“无服务器”推理选项，并设置内存大小（例如 2048 MB 或 4096 MB）和最大并发实例数。
3. 部署端点并配置 CloudWatch 警报，监控 `Invocations` 和 `ModelLatency` 指标。

**注意事项**: 无服务器端点有冷启动时间。如果对首字节延迟极其敏感，请考虑配置预置并发或保留部分实例以应对突发流量。

---

### 实践 3：使用托管 MLflow 进行严格的实验跟踪与版本控制

**说明**: 在迭代开发 Agent 的过程中，利用 SageMaker 托管的 MLflow 实例来记录每一次实验的超参数、Prompt 模板和评估指标。这确保了模型性能的可复现性，并便于在多个版本之间回滚或选择最佳模型。

**实施步骤**:
1. 初始化 MLflow 实验并设置自动记录功能，捕获 LangChain 或 LangGraph 的运行参数。
2. 在训练或评估脚本中，使用 `mlflow.log_param()` 记录 Claude 模型的 `temperature`、`max_tokens` 以及 Prompt 的版本哈希。
3. 使用 `mlflow.evaluate()` 自动计算并记录对话质量指标（如响应相关性、幻觉率等），并将结果关联到特定的运行 ID。

**注意事项**: 不要将敏感数据（如 PII 或真实的 API Key）记录到 MLflow 的 Params 或 Artifacts 中。对于 Prompt 模板，建议使用引用 ID 而非硬编码文本。

---

### 实践 4：实施 Prompt 模板化与动态注入

**说明**: 避免在代码中硬编码 Prompt。最佳实践是将 Prompt 模板化，并根据用户上下文或检索到的知识库片段动态注入内容。这有助于提高 Claude 模型在特定任务上的准确性，并便于后续的 A/B 测试。

**实施步骤**:
1. 创建 Prompt 模板文件（如 Jinja 格式），定义系统消息、少样本示例和用户输入占位符。
2. 在 LangGraph 的节点逻辑中，加载模板并结合 RAG 检索到的文档片段填充占位符。
3. 通过 MLflow UI 跟踪不同模板版本的效果，建立 Prompt 版本控制策略。

**注意事项**: 确保动态注入的内容经过清洗，防止通过注入攻击绕过系统的安全护栏。

---

### 实践 5：建立全面的评估与反馈循环机制

**说明**: 仅仅依赖人工检查对话质量是不可扩展的。应建立自动化的评估流水线，利用 Claude 3.5 Sonnet 等模型作为“评判者”，对 Agent 的输出进行打分，并将反馈数据回流至 MLflow 用于持续改进。

**实施步骤**:
1. 定义评估数据集，包含典型的用户查询及其对应的理想回答。
2. 编写评估脚本，调用 Claude 模型对比 Agent 实际输出与理想回答，生成 1-5 分的评分。
3. 将评估指标作为 MLflow 运行的一部分进行记录，并设置阈值（如 F1 分数低于 0.8 则触发警报）。

**注意事项**: 评估模型本身也可能产生偏见或错误，应定期人工抽检自动化评估的结果，确保“评判者”模型的准确性。

---

### 实践 6：强化安全性与护栏措施

**说明**: 在构建面向用户的 Agent 时，必须防止模型生成有害内容或泄露敏感信息。利用 Amazon Bedrock Guardrails 或在 LangGraph 节点中添加过滤逻辑，在输入和输出两个层面进行审查。

---

## 学习要点

- 利用 LangGraph 构建基于 Claude 的有状态对话代理，通过循环图结构实现复杂的多轮对话逻辑和工具调用。
- 在 Amazon SageMaker 上使用托管 MLflow 实现模型全生命周期的集中管理，确保实验的可追溯性与部署的标准化。
- 采用无服务器架构部署 LangGraph 应用，利用 AWS Lambda 按需计算资源，实现成本优化与自动弹性伸缩。
- 集成 Amazon Bedrock 中的 Claude 模型，结合 LangGraph 的状态管理机制，高效处理需要上下文记忆的复杂任务。
- 通过 LangChain 生态工具与 SageMaker 托管服务的深度集成，简化了从 AI 实验开发到生产环境部署的端到端工作流。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [LangGraph](/tags/langgraph/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [Agent](/tags/agent/) / [LLM](/tags/llm/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [RAG](/tags/rag/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/)

### 相关文章

- [基于Amazon Bedrock AgentCore构建统一智能系统]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-2.md" >}})
- [利用 Amazon Bedrock 构建具备记忆与个性化能力的活动助手]({{< relref "posts/20260226-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-5.md" >}})
- [LinqAlpha利用Amazon Bedrock构建“唱反调”机制以压力测试投资逻辑]({{< relref "posts/20260212-blogs_podcasts-how-linqalpha-assesses-investment-theses-using-dev-7.md" >}})
- [基于 Amazon Bedrock 构建AI招聘系统优化人才获取流程]({{< relref "posts/20260215-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-8.md" >}})
- [基于Amazon Bedrock构建AI招聘系统优化人才获取流程]({{< relref "posts/20260217-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-10.md" >}})
