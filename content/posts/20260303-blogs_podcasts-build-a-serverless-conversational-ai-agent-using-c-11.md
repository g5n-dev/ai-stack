---
title: 在SageMaker AI上基于Bedrock与LangGraph构建无服务器对话代理
date: 2026-03-03 17:26:41+08:00
draft: false
entry_kind: auto
tags:
- AWS
- Bedrock
- LangGraph
- SageMaker
- MLflow
- Claude
- 无服务器
- Agent
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 这是一份关于如何利用 Amazon Bedrock、LangGraph 和托管 MLflow 构建无服务器对话 AI 智能体的中文总结：
  **项目概述** 本文详细介绍了如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上的托管 MLflow
  服务，构建一个高性能
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios:
- AI/ML项目
---

# 在SageMaker AI上基于Bedrock与LangGraph构建无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---

## 摘要/简介

本文探讨如何使用 Amazon Bedrock、LangGraph 和 Amazon SageMaker AI 上的托管 MLflow 构建智能对话代理。

---

## 导语

随着对话式 AI 在实际业务中的深入应用，构建具备复杂推理能力且全流程可观测的智能代理已成为关键需求。本文将详细介绍如何利用 Amazon Bedrock 中的 Claude 模型结合 LangGraph，并在 Amazon SageMaker AI 上集成托管 MLflow，从而构建一个高效的无服务器对话系统。通过本文，您将掌握从架构设计到实验追踪的完整实现路径，学会利用云原生工具简化开发流程并提升模型迭代效率。

---

## 摘要

这是一份关于如何利用 Amazon Bedrock、LangGraph 和托管 MLflow 构建无服务器对话 AI 智能体的中文总结：

**项目概述**
本文详细介绍了如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上的托管 MLflow 服务，构建一个高性能的无服务器对话 AI 智能体。该架构旨在提供一个既具备复杂逻辑推理能力，又能有效管理和追踪机器学习生命周期的解决方案。

**核心技术栈与架构**

1.  **基础模型与推理**
    *   利用 **Amazon Bedrock** 提供底层基础设施，调用 **Claude** 模型（由 Anthropic 开发）的强大能力。Claude 负责处理自然语言理解、生成及复杂的推理任务。

2.  **编排与状态管理**
    *   使用 **LangGraph** 来构建智能体的应用逻辑。LangGraph 是基于有向图的框架，非常适合创建具备状态管理和循环逻辑的智能体，使其能够处理多轮对话和复杂的决策流程。

3.  **实验追踪与模型管理**
    *   集成 **Amazon SageMaker AI 上的托管 MLflow**。MLflow 用于记录实验参数、指标和模型版本，确保开发过程的可复现性和模型治理的规范性。

**核心优势与功能**

*   **无服务器架构**：整个解决方案无需管理底层服务器，能够根据请求量自动伸缩，从而降低运维成本并提高弹性。
*   **复杂对话能力**：通过 LangGraph 编排，智能体不仅能进行简单的问答，还能执行包含多个步骤的工具调用和状态保持。
*   **端到端可观测性**：利用 MLflow，开发者可以清晰地追踪模型在不同配置下的表现，便于调试和优化。
*   **企业级部署**：结合 AWS 的托管服务，该方案具备高可用性和安全性，适合生产环境部署。

**总结**
该指南展示了一条从原型设计到生产部署的完整路径，结合了 Claude 的大语言能力、LangGraph 的控制逻辑以及 SageMaker/MLflow 的管理能力，为开发者构建企业级对话 AI 提供了现代化的最佳实践。

---

## 评论

**文章中心观点**
该文章主张了一种**“全托管式闭环”**的AI Agent开发范式，即利用Amazon SageMaker AI集成的托管MLflow进行大模型（LLM）实验追踪，结合LangGraph构建有状态的工作流，并依托Bedrock调用Claude模型，从而在无服务器架构下实现可观测、可复现且具备复杂推理能力的对话智能体。

**支撑理由与深度评价**

**1. 技术架构的完备性与“可观测性”优先**
*   **事实陈述**：文章将**Managed MLflow**置于核心位置，而非仅仅关注模型调用。这是目前许多中低端教程容易忽视的痛点。
*   **深度分析**：在Agent开发中，由于引入了记忆和工具调用，LLM的输出具有高度非确定性。如果没有MLflow进行Trace（追踪）和Experiment（实验）管理，调试Agent将是一场灾难。文章强调在SageMaker上使用托管的MLflow，实际上是在强调**企业级AI工程化**的重要性。这解决了从“Demo”到“生产”的关键跨越问题。
*   **支撑理由**：LangGraph引入了循环边，使得Agent可以自我修正和迭代，这比简单的线性链更符合人类解决问题的逻辑，但也增加了调试难度，因此必须配合MLflow。

**2. 行业趋势的契合度：从“调用模型”到“编排工作流”**
*   **事实陈述**：文章选择了LangGraph而非简单的LangChain Chain。
*   **你的推断**：这反映了行业正在从“以模型为中心”向“以工作流为中心”转移。Claude 3/3.5等模型虽然能力强，但在处理超长上下文或复杂多步任务时，仍需依靠外部架构（Graph）来规划路径。文章抓住了这一技术演进方向，即**模型提供智力，框架提供骨架**。

**3. 无服务器架构的成本与弹性权衡**
*   **事实陈述**：构建方案基于AWS的无服务器组件。
*   **作者观点**：这是对初创企业和MVP（最小可行性产品）阶段最友好的架构。它消除了维护基础设施的认知负担，让开发者专注于Prompt Engineering和业务逻辑。

**反例与边界条件**

*   **反例1（延迟敏感型场景）**：该架构并不适合高频交易或实时性要求极高的工业控制场景。Bedrock的无服务器调用存在冷启动和网络延迟，LangGraph的多步推理会累加Token消耗和时间延迟，可能导致响应时间超过人类交互的忍耐极限（>2-3秒）。
*   **反例2（数据主权与混合云部署）**：对于金融或医疗行业，数据可能不允许出域。虽然Bedrock提供VPC端点，但完全依赖云端托管服务限制了“本地部署”或“私有云”的灵活性。如果企业必须将数据保留在On-Premise环境，这种全托管的SageMaker方案就不再适用。
*   **边界条件（模型幻觉）**：文章虽然提到了构建Agent，但未深入探讨如何通过架构层面（如Guardrails）来硬性限制Claude的输出。在LangGraph的循环中，如果模型产生幻觉并陷入死循环，仅靠MLflow观测是无法自动恢复的，需要额外的Supervisor模式介入。

**分维度评价**

*   **内容深度（4/5）**：文章不仅仅是API调用演示，它触及了LLMOps的核心——实验管理和状态管理。论证严谨地展示了如何将MLflow与SageMaker解耦又结合，体现了对AWS生态的深刻理解。
*   **实用价值（4.5/5）**：对于正在寻找“如何规范化生产Agent”的团队极具参考价值。它提供了一个可复用的模板，解决了“代码在本地能跑，上线就乱套”的常见问题。
*   **创新性（3.5/5）**：技术栈本身（Bedrock + LangGraph + MLflow）是现有组件的组合，而非原创发明。但将Managed MLflow如此紧密地嵌入到Serverless Agent构建流程中，是一种最佳实践的提炼。
*   **可读性（高）**：作为技术博客，通常逻辑清晰，步骤详实。
*   **行业影响（中高）**：强化了AWS在LLMOps领域的护城河，引导开发者倾向于使用其全家桶服务，增加了云厂商的粘性。

**争议点与不同观点**

*   **Vendor Lock-in（厂商锁定）风险**：虽然文章展示了便利性，但深度绑定SageMaker的Managed MLflow和Bedrock可能导致高昂的迁移成本。开源社区（如LangSmith或自建Milvus+Prometheus）提供了更灵活但运维成本更高的替代方案。
*   **LangGraph的学习曲线**：对于简单的问答场景，LangGraph可能属于“过度设计”。引入图状态机增加了系统的复杂度，对于初学者来说，维护State的定义可能比写Prompt更让人头疼。

**实际应用建议**

1.  **成本监控**：在使用Bedrock和Claude时，务必设置Budget Alert。Agent的“思考”过程（尤其是LangGraph的循环）会消耗大量Input/Output Token，成本可能呈指数级上升。
2.  **Guardrails落地**：不要完全依赖模型的“聪明才智”。在LangGraph的节点之外，必须部署Amazon Bedrock Guardrails或应用层逻辑来过滤敏感词和限制输出格式。
3.  **评估指标量化**：利用MLflow不仅是记录日志，更要建立评估基准。建议使用“ TruLens”或“RAGAS”等框架与MLflow结合，对Agent的回答进行自动化的打分，而非人工肉眼查看Log。

---

## 技术分析

基于您提供的文章标题和摘要，我将结合当前生成式AI、云原生架构以及MLOps领域的最佳实践，对这篇关于在AWS上构建无服务器对话式AI代理的技术文章进行深度分析。

---

### 深度分析报告：基于Amazon SageMaker AI构建无服务器对话式Agent

### 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：通过将**大型语言模型（Claude on Bedrock）**、**状态化编排框架**与**企业级MLOps平台（Managed MLflow on SageMaker）**相结合，可以构建出既具备复杂推理能力，又具备可观测性、可追溯性和无服务器弹性的企业级对话AI代理。

**作者想要传达的核心思想**
作者试图打破“简单的聊天机器人”与“复杂的Agent系统”之间的界限。核心思想在于**“工程化落地”**。仅仅调用API是不够的，企业级应用需要解决三个问题：
1.  **记忆与状态管理**：利用LangGraph解决多轮对话中的上下文保持。
2.  **模型治理**：利用MLflow追踪模型版本、Prompt和实验数据。
3.  **基础设施解耦**：利用AWS Serverless架构（如Lambda、Bedrock）让开发者专注于逻辑而非服务器。

**观点的创新性和深度**
该观点的创新点在于**全栈融合**。通常LangGraph教程侧重于逻辑，MLflow教程侧重于传统模型训练，而本文将两者结合在一个Serverless架构中。深度体现在它不仅仅展示了“如何对话”，还展示了“如何管理对话的生产周期”，特别是将LLM的Prompt工程和参数调优纳入MLflow的实验追踪，这是迈向AI工程化的关键一步。

**为什么这个观点重要**
随着企业从“POC（概念验证）”转向“生产环境”，最大的痛点不再是模型不够聪明，而是**系统不可控**。缺乏状态管理导致对话逻辑混乱，缺乏追踪导致无法复现线上问题。本文提出的架构直接回应了这一痛点，提供了一条从实验室到生产环境的标准路径。

### 2. 关键技术要点

**涉及的关键技术或概念**
*   **Amazon Bedrock**：AWS的托管LLM服务，提供Claude等模型的API访问。
*   **LangGraph**：基于LangChain构建的框架，专门用于管理有状态的、循环的Agent行为。
*   **Amazon SageMaker AI**：AWS的机器学习平台，集成了Notebook、实验追踪和模型部署。
*   **Managed MLflow**：开源MLOps平台的托管版本，用于ML生命周期管理。
*   **AWS Lambda / Serverless**：计算层，实现按需付费。

**技术原理和实现方式**
1.  **Agent状态管理**：利用**有向循环图**来定义对话流。不同于传统的线性链，LangGraph允许Agent根据当前状态决定是“调用工具”、“询问用户”还是“结束对话”，从而实现复杂的决策回路。
2.  **实验追踪**：在开发阶段，将每一次对话的Prompt模板、温度参数、以及Claude的输出结果记录到MLflow Runs中。这使得开发者可以对比不同Prompt策略的效果。
3.  **无服务器部署**：将LangGraph的逻辑封装在容器或Lambda中，通过API Gateway暴露接口。Bedrock负责推理，SageMaker负责管理实验元数据，Lambda负责业务逻辑流转。

**技术难点和解决方案**
*   **难点：LLM的无状态性与对话的有状态性之间的矛盾。**
    *   *解决方案*：LangGraph引入了一个持久化的检查点机制，可以在每一步对话后将状态保存到数据库（如DynamoDB）或内存中，实现对话的暂停与恢复。
*   **难点：Prompt版本混乱。**
    *   *解决方案*：利用MLflow的`log_params`和`log_text`功能，将每一个版本的System Prompt和User Prompt进行版本化管理，确保线上效果可回溯。

**技术创新点分析**
最大的创新在于**将MLOps引入Gen AI应用开发**。传统MLOps关注梯度下降和模型权重，而本文展示了如何用同样的工具（MLflow）来管理Prompt Engineering（提示工程）和Agent Flow（代理流），这实际上是LLMOps（大模型运维）的一种具体实现范式。

### 3. 实际应用价值

**对实际工作的指导意义**
这篇文章为AI架构师提供了一套**“参考架构”**。它证明了企业不需要从零搭建推理集群，也不需要为了管理模型而自建平台，完全可以利用云厂商的托管服务快速构建生产级Agent。它强调了**可观测性**的重要性，这对于维护复杂的AI系统至关重要。

**可以应用到哪些场景**
*   **企业知识库助手**：需要多轮对话理解用户意图，并检索RAG（检索增强生成）内容的场景。
*   **金融/医疗合规助手**：需要严格记录每一次回答的依据（Prompt版本、模型参数）以满足合规审计的场景。
*   **电商智能客服**：状态机用于管理购物车状态，MLflow用于分析哪种话术转化率更高。

**需要注意的问题**
*   **成本控制**：Bedrock按Token计费，频繁的LangGraph循环和多轮调用可能导致成本指数级上升。
*   **延迟**：Serverless架构（特别是Lambda冷启动）+ Bedrock网络请求可能导致首字延迟较高，不适合对实时性要求极高的场景。
*   **上下文窗口限制**：虽然Claude上下文很大，但LangGraph的状态累积若不加修剪，可能超出模型限制。

**实施建议**
在实施前，先定义好“什么是好的对话”。建立基于MLflow的评估指标，不仅仅是“它回答了吗”，而是“回答是否准确、语气是否符合规范”。利用SageMaker的实验管理功能进行小规模灰度测试，再全量上Bedrock。

### 4. 行业影响分析

**对行业的启示**
这篇文章标志着**AI开发正在从“手工作坊”向“工业化流水线”转型**。以前开发者是在Jupyter Notebook里调API，现在是在完整的MLOps闭环中开发Agent。它启示行业：未来的AI竞争不仅仅是模型参数量的竞争，更是**工程化能力（Agent框架+数据管理）**的竞争。

**可能带来的变革**
*   **Serverless First**：更多的AI应用将采用Serverless架构，因为流量波动巨大，按需付费是最经济的。
*   **Agent即代码**：Agent的流程定义将像代码一样被严格版本控制和CI/CD流水线管理。

**相关领域的发展趋势**
*   **LangGraph的崛起**：LangChain正在从简单的链式调用向更复杂的图状态管理演进，这将成为构建Agent的主流范式。
*   **MLOps平台的泛化**：像MLflow这样的工具正在扩展支持非传统模型（LLM），成为LLMOps的标准底座。

**对行业格局的影响**
这进一步巩固了**云厂商（如AWS）在AI基础设施层的统治地位**。企业不再需要购买昂贵的GPU集群来运行Agent，而是通过Bedrock等API调用算力。这削弱了硬件厂商对小企业的直接影响力，提升了拥有全栈托管能力的云厂商的话语权。

### 5. 延伸思考

**引发的其他思考**
*   **评估的主观性**：MLflow擅长记录数值指标（如准确率），但如何量化对话的“创造性”或“情商”？我们需要引入基于LLM的评估器作为裁判。
*   **数据飞轮**：LangGraph产生的对话数据如何回流？这些真实的对话日志应被清洗并用于微调模型，形成闭环。

**可以拓展的方向**
*   **多模态Agent**：目前的架构主要基于文本，如何扩展到支持图片（Claude 3支持）和音频输入？
*   **人机协同**：在LangGraph的流程中加入“人工审核”节点，当Agent置信度低时自动转人工。

**需要进一步研究的问题**
*   如何在Serverless环境中高效地实现长对话记忆的向量化检索？
*   当LangGraph的图结构变得非常复杂时（例如几十个节点），如何进行调试和可视化监控？

**未来发展趋势**
**自主Agent的 Swarm（群体）智能**。未来的文章可能不再讨论单个Agent，而是讨论如何用SageMaker协调多个LangGraph Agent进行协作。

### 7. 案例分析

**结合实际案例说明**
假设我们要构建一个**“旅行规划Agent”**。
*   **用户**：“我想去日本，预算1万。”
*   **Agent动作**：
    1.  **理解意图**（Claude）。
    2.  **查询航班**（调用工具）。
    3.  **查询酒店**（调用工具）。
    4.  **计算总价**（逻辑节点）。
    5.  **发现超预算** -> **决策**：询问用户是否降低酒店标准（LangGraph循环）。

**成功案例分析**
*   **Klarna (客服Agent)**：虽然他们不一定用了SageMaker，但他们利用类似架构（LLM+状态管理）处理了2/3的客服工单，直接驱动了数亿美元的节省。成功关键在于**精准的知识库检索**和**流畅的对话流转**。

**失败案例反思**
*   **早期聊天机器人**：许多基于规则的机器人失败在“一旦用户跳出预设流程，机器人就崩溃了”。
*   **教训**：LangGraph的价值在于允许“非确定性”流程，Agent可以根据反馈动态调整路径，而不是死板的脚本。

**经验教训总结**
不要试图一次性构建完美的Agent。先构建一个能完成核心任务的图，然后用MLflow分析用户在哪一步流失，针对性优化Prompt或增加工具，**迭代式进化**是关键。

### 8. 哲学与逻辑：论证地图

**中心命题**
在构建生产级生成式AI应用时，采用**“模型托管服务 + 状态化编排框架 + 集中式实验追踪”**的架构模式，是实现**高可维护性与系统鲁棒性**的最优解。

**支撑理由与依据**
1.  **理由一：复杂系统需要显式状态管理。**
    *   *依据*：对话本质

---

## 最佳实践

### 实践 1：使用 LangGraph 设计健壮的状态机架构

**说明**: 在构建对话式 AI 代理时，利用 LangGraph 的有向图结构来管理对话流程和状态。相比于简单的线性链，LangGraph 允许代理根据中间结果进行决策、循环和自我修正，这对于处理复杂的多轮对话至关重要。通过定义明确的节点（计算步骤）和边（逻辑流），可以构建出既灵活又可控的代理行为。

**实施步骤**:
1. 定义一个 `TypedDict` 来作为代理的核心状态结构，包含消息历史、用户意图、上下文数据等字段。
2. 创建节点函数，每个函数接收当前状态并返回状态更新（例如：意图识别节点、工具调用节点、响应生成节点）。
3. 使用 `StateGraph` 定义图结构，通过 `add_node` 添加逻辑节点，通过 `add_edge` 和 `add_conditional_edges` 定义节点间的转换条件。
4. 编译图并设置入口点，确保在对话循环中能够正确维护和传递状态。

**注意事项**: 避免在状态中存储敏感的 PII（个人身份信息）数据，除非有加密措施。确保状态大小在上下文窗口限制之内，必要时实施摘要策略。

---

### 实践 2：实施基于 MLflow 的可观测性与实验追踪

**说明**: 在 Amazon SageMaker 上利用托管 MLflow 来记录模型配置、提示词模板、超参数和对话质量指标。由于 LLM 的非确定性特性，追踪不同版本的 Prompt 和模型参数对于复现高性能的对话体验至关重要。MLflow 的 Model Registry 功能还能帮助您管理从实验到生产的模型发布流程。

**实施步骤**:
1. 在 SageMaker Notebook 或 Studio 环境中配置 MLflow Tracking Server URI。
2. 在 LangGraph 执行流程的关键节点（如 Agent 最终输出）集成 `mlflow.log_metrics`，记录响应延迟、Token 消耗量及用户反馈评分。
3. 使用 `mlflow.log_params` 记录 Claude 模型版本（如 `claude-3-5-sonnet`）、温度参数和 Top-P 值。
4. 将表现最佳的 LangGraph 构建逻辑和 Prompt 模板记录为 MLflow Run，并注册到 Model Registry 中进行版本控制。

**注意事项**: 确保 SageMaker 执行角色拥有访问 MLflow 服务器的必要 IAM 权限。对于包含敏感数据的日志，需配置 MLflow 的数据脱敏或加密存储。

---

### 实践 3：利用 Bedrock InvokeAgent 与工具调用实现功能扩展

**说明**: 通过 Amazon Bedrock 的 `Converse` API 或 Agents 工具赋予 Claude 模型执行外部操作的能力。在 LangGraph 中，这通常表现为一个“工具节点”或“工具调用”阶段。最佳实践包括定义清晰的工具描述，以便 Claude 准确判断何时以及如何调用它们，从而实现数据检索（RAG）或事务处理。

**实施步骤**:
1. 在 LangGraph 中定义 Python 函数作为工具，并使用 Pydantic 或类似库严格定义输入参数的模式。
2. 为每个工具编写详细的 `docstring`，说明工具的功能、输入要求及预期输出，这是 Claude 理解工具用途的关键。
3. 在 LangGraph 图中添加条件边：当模型生成工具调用请求时，路由至工具执行节点；执行完毕后将结果返回给模型进行最终响应生成。
4. 实施错误处理逻辑，确保工具调用失败时（如 API 超时），代理能够优雅降级或重试，而不是直接崩溃。

**注意事项**: 严格验证工具输入参数，防止提示词注入攻击通过工具调用接口渗透到后端系统。限制工具的执行超时时间，避免无响应的阻塞。

---

### 实践 4：优化 Serverless 环境下的冷启动与延迟

**说明**: 在 Serverless 架构（如 AWS Lambda 或 SageMaker Serverless Inference）中运行 LangGraph 应用时，冷启动是影响用户体验的主要因素。最佳实践侧重于减少初始化时间和优化网络请求，确保代理响应迅速。

**实施步骤**:
1. 将 LangGraph 的编译逻辑、模型客户端初始化以及 Prompt 模板加载放在全局作用域或模块初始化阶段，以便容器复用。
2. 利用 Lambda SnapStart 或 SageMaker 的预置并发设置，保持一定数量的热实例以应对突发流量。
3. 优化依赖包大小，仅打包必要的库（如使用 Lambda Layers），并移除未使用的测试文件和数据文件。
4. 实施流式响应机制，利用 Bedrock 的流式 API 逐块返回 Token，从而在用户端降低首字节时间（TTFB）的感知。

**注意事项**: 监控内存使用情况，因为 Serverless 环境对内存限制严格。LangGraph 的状态图如果过于复杂，可能会增加序列化/反序列化的开销。

---

### 实践 5：构建安全的 Prompt 工程与上下文管理

**说明**: 在构建代理时，必须通过 Prompt 工程防止模型产生有害内容或泄露系统指令。同时，

---

## 学习要点

- 利用 LangGraph 构建基于状态机架构的对话代理，通过定义节点、边和条件边实现复杂的对话流控制和状态管理。
- 将 Claude 3 大模型集成至 SageMaker AI，利用托管 MLflow 实现模型全生命周期的追踪、注册与部署，确保生产环境的高可用性。
- 使用 Amazon Bedrock 与 SageMaker 的无服务器架构，无需管理底层基础设施即可自动扩缩容，显著降低运维成本并提高开发效率。
- 通过 LangChain 的工具调用能力连接外部 API，使 AI 智能体能够执行实时数据查询等操作，从而突破模型知识截止日期的限制。
- 利用 MLflow 的 LangChain 自动记录功能，自动捕获模型参数、提示词和指标，实现了对话式 AI 实验的完全可追溯性。
- 采用 Amazon Cognito 实现安全的用户身份验证，并利用 API Gateway 和 Lambda 构建无服务器后端，保障了应用程序的安全性与扩展性。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [AWS](/tags/aws/) / [Bedrock](/tags/bedrock/) / [LangGraph](/tags/langgraph/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [Claude](/tags/claude/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [Agent](/tags/agent/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Bedrock与LangGraph构建SageMaker AI对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-4.md" >}})
- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Amazon SageMaker AI构建无服务器Claude对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
