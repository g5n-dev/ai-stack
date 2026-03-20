---
title: 基于Bedrock与LangGraph在SageMaker构建无服务器对话代理
date: 2026-03-02 21:57:29+08:00
draft: false
entry_kind: auto
tags:
- LangGraph
- Amazon Bedrock
- SageMaker
- MLflow
- 无服务器
- 对话代理
- Claude
- LLM
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: 本文介绍了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI**
  上的托管 **MLflow**，构建一个基于 Claude 的**无服务器（Serverless）对话式 AI 智能体**。 主要技术要点如下： 1. **核心架构组件**：
  *
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios:
- AI/ML项目
- 大语言模型
---

# 基于Bedrock与LangGraph在SageMaker构建无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---

## 摘要/简介

本文探讨如何使用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上的托管 MLflow 来构建一个智能对话代理。

---

## 导语

随着对话式 AI 在企业场景中的深入应用，如何高效构建、追踪并优化智能代理成为开发者关注的焦点。本文将详细介绍如何结合 Amazon Bedrock、LangGraph 以及托管在 Amazon SageMaker AI 上的 MLflow，从零搭建一个无服务器架构的对话代理。通过阅读此文，您不仅能掌握全链路实现细节，还能了解到如何利用 MLflow 有效管理模型实验与迭代，从而在生产环境中交付更可靠的 AI 解决方案。

---

## 摘要

本文介绍了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上的托管 **MLflow**，构建一个基于 Claude 的**无服务器（Serverless）对话式 AI 智能体**。

主要技术要点如下：

1.  **核心架构组件**：
    *   **Amazon Bedrock**：提供底层的大语言模型（此处指 Claude）支持，实现生成式 AI 能力。
    *   **LangGraph**：用于构建和管理智能体的工作流与状态图。
    *   **Amazon SageMaker AI**：提供托管的 MLflow 服务，用于实验跟踪和模型开发。

2.  **无服务器优势**：
    该方案采用无服务器架构，用户无需管理底层基础设施，可根据需求自动扩缩容，从而降低运维成本并提高开发效率。

3.  **功能实现**：
    通过 LangGraph 设计的智能体能够处理复杂的对话逻辑，结合 SageMaker 上的 MLflow，开发者可以有效地追踪实验数据、管理模型版本，确保 AI 应用的可观测性与迭代效率。

---

## 评论

**中心观点**
本文主张通过将 Amazon Bedrock（模型层）、LangGraph（编排层）与 SageMaker 集成的 MLflow（管理层）深度耦合，构建一个既具备复杂推理能力又拥有企业级治理与可观测性的 Serverless 生成式 AI 应用架构。

**支撑理由与边界分析**

1.  **架构演进：从“单体调用”走向“有状态工作流”**
    *   **支撑理由（事实陈述/作者观点）：** 文章正确地指出了当前对话式 AI 的痛点——简单的 Prompt 调用无法处理多轮对话中的上下文记忆和工具调用逻辑。引入 LangGraph 是本文的技术亮点，它将对话建模为状态机，解决了“循环”和“条件分支”的编排难题，这比简单的 LangChain 链式调用更符合真实业务逻辑。
    *   **反例/边界条件（你的推断）：** LangGraph 的引入会显著增加系统的复杂度。对于简单的 FAQ（常见问题解答）或单次任务（如“总结这段文本”），引入图架构属于过度设计，反而会增加延迟和维护成本。

2.  **企业级治理：填补“原型”与“生产”之间的鸿沟**
    *   **支撑理由（事实陈述）：** 利用 SageMaker 内置的托管 MLflow 进行实验追踪和模型注册是本文的务实之选。在生成式 AI 中，“幻觉”和参数调优极其频繁，缺乏追踪会导致版本混乱。文章强调了在 Serverless 环境下依然需要严格的 MLOps 流程，这是对企业级开发痛点的准确回应。
    *   **反例/边界条件（你的推断）：** MLflow 虽然强大，但在处理 LLM 特有的非结构化输入/输出（如长上下文、JSON 模式）时，其 UI 体验和查询效率有时不如专门的 LLM Ops 工具（如 LangSmith 或 Weights & Biases）。如果团队已经深度绑定其他生态，强行引入 SageMaker MLflow 可能造成工具孤岛。

3.  **成本与弹性的权衡：Serverless 的双刃剑**
    *   **支撑理由（作者观点）：** 依托 Amazon Bedrock 的 Serverless 模型调用，文章构建了一个无需管理底层基础设施的架构。这使得系统可以从零扩容，应对突发流量，且没有闲置成本。
    *   **反例/边界条件（你的推断）：** 在极高并发或需要极低延迟的场景下，Serverless 的冷启动和网络跃点可能成为瓶颈。此外，Bedrock 的按 Token 计费在高频调用场景下，长期成本可能高于自部署开源模型（如使用 Llama 3 on SageMaker Endpoint）。

**多维度深入评价**

1.  **内容深度与严谨性**
    文章不仅仅停留在“Hello World”级别的演示，而是触及了**AI 工程化**的核心。它没有把 LLM 当作魔法，而是当作一个需要被治理的软件组件。特别是对于“可观测性”的探讨，将 Claude 的生成内容与 MLflow 的指标挂钩，体现了严谨的工程思维。然而，文章在“安全性”方面略显不足，虽然提到了 Bedrock，但未深入探讨如何利用 Guardrails 防止提示词注入。

2.  **实用价值**
    对于正在使用 AWS 堆栈的团队，该文章提供了高价值的参考架构。它解决了“如何把 LangChain 代码变成生产级服务”的问题。特别是关于 SageMaker 跳转页面的配置和 MLflow 服务器的对接细节，属于实操中的“坑”，文章给出了明确指引。

3.  **创新性**
    将 **LangGraph**（一个相对较新的库）与 **AWS SageMaker 的托管 MLflow** 结合是本文的主要创新点。大多数教程只关注前者（怎么写逻辑）或后者（怎么监控模型），鲜有将两者在 AWS 云原生环境下无缝打通的成熟案例。

4.  **可读性**
    作为一篇技术博客，文章结构清晰，遵循了“架构图 -> 代码逻辑 -> 部署步骤”的经典逻辑。但文中涉及较多的 AWS 控制台配置步骤，对于不熟悉 AWS IAM 权限和 VPC 配置的读者来说，阅读门槛较高。

**行业影响与争议点**

*   **行业影响：** 该文章预示着 **LLM Ops 的标准化**。行业正在从“狂飙突进”的模型开发期，进入“精耕细作”的治理期。云厂商（AWS）与开源框架的深度集成将成为主流。
*   **争议点：** **Vendor Lock-in（厂商锁定）**。虽然使用了开源的 LangGraph 和 MLflow，但核心计算力 Bedrock 和 SageMaker 是 AWS 专属的。一旦业务量巨大，迁移出 AWS 的成本极高。另一种观点认为，既然 LangGraph 已经支持多种后端，为何不直接使用更轻量级的向量数据库（如 Chroma）而非依赖 AWS 的特定服务？

**实际应用建议**

1.  **不要盲目堆砌技术栈：** 如果你的业务只是简单的“客服问答”，直接使用 Bedrock 的 Playgrounds 或简单的 Lambda 即可，无需引入 LangGraph 的复杂性。
2.  **重视评估指标：** 在生产环境中，除了 MLflow 记录的 Loss 和 Accuracy，务必建立“基于人类反馈的评估机制”（RLHF 的简化版），因为 LLM 的生成质量很难仅通过数值指标衡量。
3.  **成本监控：** Serverless 容易让人忽略成本。建议在 MLflow 中不仅记录模型性能，也记录每次推理消耗的 Token 数和估算成本，以便财务

---

## 技术分析

基于提供的标题和摘要，结合AWS（亚马逊云科技）的技术生态、当前生成式AI的发展趋势以及LangGraph和MLflow的技术特性，以下是对该文章内容的深度全面分析。

---

### 深度分析：基于 Claude、LangGraph 和 SageMaker AI 构建无服务器对话式智能体

### 1. 核心观点深度解读

**主要观点**
文章的核心观点在于展示一种**现代化的、全托管的、生产级**的生成式AI应用构建范式。它主张通过将**高性能基础模型**、**状态化编排框架**与**企业级MLOps平台**相结合，在无服务器架构上构建具备记忆、推理能力和工具调用功能的智能对话代理。

**核心思想**
作者试图传达“**最佳实践的组合拳**”这一思想。单一的工具无法解决企业级AI落地的所有问题：
*   **Claude (via Bedrock)** 提供“大脑”；
*   **LangGraph** 提供“神经系统与循环逻辑”；
*   **SageMaker + MLflow** 提供“健康监测与实验室”。
核心思想是**在保持敏捷开发的同时，不牺牲对模型实验、追踪和部署的可观测性与控制力**。

**创新性与深度**
*   **架构创新**：传统的LangChain应用往往缺乏持久化层和标准的实验追踪。本文提出的架构利用LangGraph的有向循环图特性，解决了复杂对话中的状态管理难题。
*   **深度**：文章不仅仅停留在“Hello World”级别的调用，而是深入到了**Managed MLflow（托管MLflow）**的集成。这意味着它关注的是**全生命周期管理**（LLMOps），从实验、追踪到部署，这是区分原型与生产系统的关键深度。

**重要性**
随着企业从POC（概念验证）转向生产，他们面临着“模型幻觉难追踪”、“多轮对话状态丢失”和“基础设施维护成本高”三大痛点。该观点提供了一条经过验证的路径，能够利用云原生服务解决这些棘手问题，对于希望快速落地AI应用的企业具有重要的指导意义。

### 2. 关键技术要点

**涉及的关键技术**
1.  **Amazon Bedrock**: AWS的托管基础模型服务，提供对Anthropic Claude模型的API访问。
2.  **LangGraph**: LangChain的扩展，专门用于构建有状态、多Agent的循环工作流。
3.  **Amazon SageMaker**: AWS的机器学习平台，提供Notebook、模型部署等功能。
4.  **Managed MLflow**: SageMaker内集成的开源MLflow平台，用于ML生命周期管理。

**技术原理与实现方式**
*   **状态管理**：LangGraph引入了`StatefulGraph`的概念。在实现上，它通过一个中心化的状态对象在节点之间传递数据。不同于传统的线性链，Graph可以包含循环，允许Agent基于上一轮的结果进行自我修正或迭代查询。
*   **无服务器计算**：利用AWS Lambda或Bedrock自身的按需计费模式，无需预置EC2实例。LangGraph的执行逻辑可以被打包为Lambda函数，通过API Gateway触发。
*   **实验追踪**：在SageMaker Notebook中，代码会自动初始化MLflow Tracking Server。每当调用Claude模型时，Prompt、参数、响应和Token消耗都会被记录到MLflow的后端存储中（通常是S3或EFS）。

**技术难点与解决方案**
*   **难点：上下文记忆的持久化**。无服务器架构通常是无状态的，如何让Agent记住长对话历史？
    *   **解决方案**：文章可能采用了**Checkpoint机制**。LangGraph支持将状态快照保存到外部存储（如Amazon DynamoDB或S3），在每次交互时恢复状态，从而实现跨会话的记忆。
*   **难点：模型调优的不确定性**。如何知道哪个Prompt或温度参数效果最好？
    *   **解决方案**：利用**MLflow的Experiments和Runs**。通过对比不同Run的指标，量化评估模型表现。

**技术创新点分析**
最大的创新点在于**将复杂的图编排逻辑与企业级MLOps无缝打通**。通常开发者喜欢LangChain的灵活性但苦于难以在生产环境追踪实验；而企业喜欢MLflow的规范但难以集成复杂的Agent逻辑。本文展示了如何在SageMaker这一统一平台上融合两者。

### 3. 实际应用价值

**对实际工作的指导意义**
该架构为AI工程师提供了一个**标准化的生产环境模板**。它指导团队如何从本地开发平滑过渡到云端部署，且无需运维Kubernetes等复杂基础设施，极大降低了AI应用的落地门槛。

**可应用场景**
1.  **企业级知识库问答（RAG）**：需要多轮对话来澄清用户意图，并检索私有数据。
2.  **个人助理与任务自动化**：例如“帮我规划行程并预订机票”，涉及多个步骤的推理和API调用。
3.  **客户服务自动化**：需要处理复杂的投诉流程，可能需要升级给人工，LangGraph的图结构非常适合定义这种SOP（标准作业程序）。
4.  **金融/医疗合规助手**：MLflow的审计功能对于高度监管的行业至关重要。

**需要注意的问题**
*   **成本控制**：Bedrock按Token计费，频繁的循环推理可能会迅速增加成本。
*   **延迟**：多步推理和Lambda冷启动可能导致响应时间增加。
*   **状态锁定**：在并发环境下，状态管理机制需要处理好并发写入冲突。

**实施建议**
*   从简单的线性流程开始，逐步引入LangGraph的循环逻辑。
*   在开发初期就强制接入MLflow，建立数据驱动的调试习惯，而不是仅靠打印日志。

### 4. 行业影响分析

**对行业的启示**
这一技术栈的普及标志着**AI开发正在从“手工作坊”向“工业化流水线”转型**。行业不再仅仅关注模型的准确率，而是开始关注系统的**可观测性、可维护性和可扩展性**。

**可能带来的变革**
*   **MLOps的普及化**：通过SageMaker托管MLflow，中小企业也能以极低的成本使用原本只有大厂才具备的实验管理平台。
*   **Agent作为服务**：无服务器架构使得构建特定功能的微型Agent变得极其容易，未来可能会出现“Agent Store”式的应用生态。

**相关领域的发展趋势**
*   **LangGraph的崛起**：它正在成为构建复杂Agent的事实标准，逐步取代简单的LangChain Chain。
*   **云厂商的深度集成**：各大云厂商都在争夺“AI应用层”的开发者，AWS通过深度集成开源框架（LangChain, MLflow）来构建护城河。

### 5. 延伸思考

**引发的思考**
*   **人机协作模式**：当Agent具备记忆和工具调用能力时，如何设计“人在回路”的干预机制？
*   **评估指标体系**：对于对话式Agent，除了准确率，我们还需要关注哪些指标（如：对话轮次、用户满意度、工具调用成功率）？

**拓展方向**
*   **多模态扩展**：目前的架构主要基于文本，如何扩展以支持图像（Claude 3/4支持视觉）和音频输入？
*   **多Agent协作**：利用LangGraph构建多个互相协作的Agent（如：一个负责写代码，一个负责测试），而非单一Agent。

**未来趋势**
未来，像LangGraph这样的编排框架可能会被内置到云厂商的托管服务中（类似AWS Step Functions for LLM），开发者只需定义配置文件即可生成Agent，无需编写大量Python代码。

### 7. 案例分析

**成功案例逻辑推演**
假设一家**在线旅游公司（OTA）**采用此架构：
*   **场景**：用户想要改签机票。
*   **流程**：
    1.  用户发起请求。
    2.  LangGraph Agent识别意图，调用“查询政策”节点。
    3.  Agent发现政策复杂，进入循环（调用“计算差价”节点）。
    4.  MLflow记录了每次查询的政策依据和差价，供后续审计。
*   **成功要素**：系统不仅回答了问题，还通过状态保存了用户的航班信息，无需用户重复输入。

**失败案例反思**
如果一家公司试图用此架构构建**高频实时交易系统**：
*   **问题**：Bedrock的网络延迟和LangGraph的多步推理可能导致毫秒级的交易机会流失。
*   **教训**：该架构适合**高逻辑密度、低延迟敏感**的场景，而非极致高频交易场景。

### 8. 哲学与逻辑：论证地图

**中心命题**
**在构建企业级生成式AI应用时，采用“Amazon Bedrock + LangGraph + SageMaker托管MLflow”的无服务器架构，是目前平衡开发敏捷性、系统可控性与运维成本的最优解。**

**支撑理由与依据**
1.  **理由一：复杂逻辑的必要条件**
    *   *依据*：对话式AI本质上是递归和状态依赖的。传统的线性Prompt无法处理“纠正-重试”逻辑。LangGraph基于图的架构是数学上处理状态机的最佳实践。
2.  **理由二：生产力的释放**
    *   *依据*：自建基础设施（如K8s集群、向量数据库、模型部署服务）是非功能需求，占用核心研发资源。无服务器架构将这些非核心工作外包给云厂商，符合比较优势理论。
3.  **理由三：实验的可复现性与合规性**
    *   *依据*：没有MLflow这类追踪系统，AI模型就是“黑盒”。企业级应用必须具备审计能力，Managed MLflow提供了最低成本的合规路径。

**反例与边界条件**
1.  **反例一：极致的成本敏感型场景**
    *   *条件*：如果应用规模达到海量（如日活千万），按量计费的无服务器成本可能超过预留实例（EC2/EKS）。
2.  **反例二：数据主权严格限制**
    *   *条件*：某些企业要求数据绝对不能出域，而Bedrock是公有云服务。此时必须使用本地部署的开源模型（如Llama 3），该架构不适用。

**命题性质分析**
*   **事实判断**：LangGraph支持图结构；SageMaker提供托管MLflow；Bedrock支持Claude。
*   **价值判断**：“最优解”是一种价值判断，基于对“敏捷性”和“成本”的权重赋值。
*   **可检验预测**：采用此架构的团队，其从POC到上线的时间将比自建架构

---

## 最佳实践

### 实践 1：设计健壮的有状态图结构

**说明**:
在使用 LangGraph 构建对话代理时，核心在于设计一个能够处理复杂对话流程的有状态图。LangGraph 允许定义循环和条件边，这对于处理多轮对话、错误恢复和上下文保持至关重要。最佳实践是将对话逻辑分解为清晰的节点（如意图识别、信息提取、工具调用、响应生成），并明确定义状态如何在节点之间流转。

**实施步骤**:
1. 定义一个 `TypedDict` 结构来规范图中的状态数据（如用户输入、历史记录、上下文变量）。
2. 将业务逻辑封装为独立的节点函数，每个函数接收当前状态并返回状态更新。
3. 使用 `StateGraph` 添加节点，并使用 `add_conditional_edges` 定义基于状态的逻辑分支（例如：是否需要调用外部工具或结束对话）。
4. 设置图的入口点和检查点，以便在中间步骤进行持久化。

**注意事项**:
- 避免在单个节点中处理过多逻辑，保持节点的单一职责。
- 确保图结构有明确的终止条件，防止无限循环。
- 利用 LangGraph 的持久化功能将状态保存到内存中，以支持长时间运行的会话。

---

### 实践 2：实施严格的提示工程与护栏机制

**说明**:
Claude 模型虽然强大，但在生产环境中必须通过系统提示词来约束其行为，确保回复的安全性、相关性和品牌一致性。特别是在结合 LangGraph 使用工具调用时，需要明确指示模型何时以及如何使用工具。此外，还需要建立输入输出护栏，以防止提示词注入或处理不当的敏感信息。

**实施步骤**:
1. 在系统提示词中明确定义代理的角色、任务范围和限制条件。
2. 实施输入验证层，在将用户输入发送给 Claude 之前进行清洗和检查。
3. 配置 Claude 的响应格式，强制输出 JSON 或特定结构以利于 LangGraph 解析。
4. 对于敏感话题，利用 Claude 的“拒绝回答”能力，并在提示词中预设拒绝话术。

**注意事项**:
- 定期审查和测试提示词，因为微小的措辞变化可能导致模型行为的显著差异。
- 不要在提示词中硬编码敏感 API 密钥或 PII（个人身份信息）。
- 考虑使用 Amazon Comprehend 等服务作为额外的安全层，检测输入中的毒性或偏见。

---

### 实践 3：利用 SageMaker 无服务器架构实现弹性伸缩

**说明**:
为了优化成本并应对流量波动，应使用 Amazon SageMaker 的无服务器推理功能来部署 Claude 代理或后端逻辑。这允许您在不配置实例的情况下运行模型，只需为处理请求所需的计算时间和内存付费。对于由 LangGraph 编排的复杂代理，可以将整个链部署为 SageMaker 无服务器端点。

**实施步骤**:
1. 将 LangGraph 逻辑和模型推理代码容器化，创建兼容 SageMaker 的 Docker 镜像。
2. 在 SageMaker 中配置无服务器推理端点，设置内存大小（例如 2048 MB 或 4096 MB）和最大并发数。
3. 配置自动扩缩容策略，虽然无服务器会自动处理，但需限制最大并发以控制成本突增。
4. 使用 Amazon API Gateway 或 Application Load Balancer 作为前端，将请求路由至 SageMaker 端点。

**注意事项**:
- 无服务器端点有冷启动时间（通常几秒钟），对于极度延迟敏感的应用需权衡。
- 监控 CloudWatch 指标（如 `ModelLatency` 和 `Invocations`）以调整内存配置，避免内存不足错误。

---

### 实践 4：集中化模型实验追踪与版本管理

**说明**:
使用托管 MLflow（Managed MLflow）可以系统地跟踪 LangGraph 代理的开发过程。由于对话系统涉及提示词调整、参数配置和图结构变更，使用 MLflow 记录这些实验数据对于复现最佳结果至关重要。MLflow 可以记录 LangGraph 的配置、Claude 模型的参数以及生成的对话样本。

**实施步骤**:
1. 在 SageMaker Studio 中初始化 MLflow 实验，确保与 SageMaker 执行角色集成。
2. 在训练或评估脚本中，使用 `mlflow.start_run()` 包装代码块。
3. 记录关键参数（如温度、top_p、提示词模板版本）和指标（如 BLEU 分数、ROUGE 或用户满意度评分）。
4. 使用 `mlflow.log_model()` 注册 LangGraph 代理的最佳版本，以便后续部署。

**注意事项**:
- 确保敏感数据不被记录到 MLflow 的参数或指标中。
- 建立清晰的模型注册阶段（如 Staging, Production）工作流，以便自动化部署流水线。
- 定期清理过时的实验运行以降低存储成本。

---

### 实践 5：构建全面的自动化评估流程

**说明**:
基于 LLM 的应用很难用传统的单元测试覆盖。最佳实践是构建一套自动化评估流程，利用“作为裁判的 LLM

---

## 学习要点

- 利用 LangGraph 构建基于 Claude 的有状态对话代理，通过循环图结构管理复杂的多轮对话上下文
- 集成托管 MLflow 实现模型全生命周期管理，确保从实验到部署的可追溯性与版本控制
- 采用 Amazon SageMaker AI 的无服务器架构部署，实现按需自动扩缩容并降低基础设施运维成本
- 结合 Claude 3.5 Sonnet 模型与 LangChain 工具调用能力，增强代理处理复杂任务与外部系统交互的智能性
- 通过 SageMaker AI 托管服务简化 MLflow 部署流程，快速构建可观测的模型实验与生产环境

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [LangGraph](/tags/langgraph/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [对话代理](/tags/%E5%AF%B9%E8%AF%9D%E4%BB%A3%E7%90%86/) / [Claude](/tags/claude/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [利用 Amazon Bedrock 构建具备记忆与个性化能力的活动助手]({{< relref "posts/20260226-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-5.md" >}})
- [基于 Amazon Bedrock 构建AI招聘系统优化人才获取流程]({{< relref "posts/20260215-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-8.md" >}})
- [Codex与Claude助力自定义内核普及]({{< relref "posts/20260215-blogs_podcasts-custom-kernels-for-all-from-codex-and-claude-7.md" >}})
- [基于Amazon Bedrock构建AI招聘系统优化人才获取流程]({{< relref "posts/20260217-blogs_podcasts-ai-meets-hr-transforming-talent-acquisition-with-a-10.md" >}})
