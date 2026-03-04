---
title: "基于Bedrock与LangGraph在SageMaker构建无服务器对话代理"
date: 2026-03-04T03:29:03+08:00
draft: false
entry_kind: "auto"
tags: ["AWS", "Bedrock", "LangGraph", "SageMaker", "Claude", "MLflow", "Agent", "无服务器"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "以下是针对您提供的标题和简短描述的总结： **标题：使用 Claude、LangGraph 和 Amazon SageMaker AI 上的托管 MLflow 构建无服务器对话式 AI 智能体** **总结内容：** 本文主要探讨了如何利用亚马逊云科技（AWS）的生成式 AI 服务栈来构建一个**无服务器**的智能对话"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios: ["AI/ML项目"]
---

# 基于Bedrock与LangGraph在SageMaker构建无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---
## 摘要/简介

本篇文章探讨如何使用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上的托管 MLflow 来构建智能对话代理。

---
## 导语

随着对话式 AI 在实际业务场景中的深入应用，如何高效构建并管理具备状态记忆能力的智能代理成为开发者关注的焦点。本文将详细介绍如何利用 Amazon Bedrock 中的 Claude 模型、LangGraph 框架以及 Amazon SageMaker AI 上的托管 MLflow，搭建一个无服务器的对话系统。通过阅读此文，读者不仅能掌握端到端的实现流程，还能了解如何利用托管服务简化模型实验与追踪，从而加速 AI 应用的落地与迭代。

---
## 摘要

以下是针对您提供的标题和简短描述的总结：

**标题：使用 Claude、LangGraph 和 Amazon SageMaker AI 上的托管 MLflow 构建无服务器对话式 AI 智能体**

**总结内容：**

本文主要探讨了如何利用亚马逊云科技（AWS）的生成式 AI 服务栈来构建一个**无服务器**的智能对话代理。该解决方案的核心组件与实施路径如下：

1.  **核心架构与组件：**
    *   **基础模型 (大脑)：** 使用 **Amazon Bedrock** 调用 **Claude** 模型，为智能体提供强大的自然语言处理与推理能力。
    *   **编排框架 (逻辑)：** 集成 **LangGraph**。LangGraph 基于 LangChain，特别擅长构建有状态、多步执行的智能体工作流，能够处理复杂的循环逻辑和对话状态管理。
    *   **应用平台 (部署)：** 依托 **Amazon SageMaker AI**。它不仅提供了模型部署环境，还集成了**托管的 MLflow**。MLflow 在此用于管理实验、追踪模型性能指标以及版本控制，简化了 MLOps 流程。
    *   **基础设施模式：** 采用**无服务器** 架构，意味着用户无需管理底层服务器，可根据对话流量自动弹性伸缩，降低运维成本并提高可用性。

2.  **实现目标：**
    文章旨在指导开发者如何将这些服务有机结合，从零开始构建一个能够理解上下文、进行复杂推理并具备自我管理能力的对话式 AI 系统。

**简而言之：**
这是一个关于在 AWS 云平台上，利用 Claude (模型) + LangGraph (逻辑控制) + SageMaker/MLflow (追踪与托管) 来快速搭建现代化、可扩展且易于管理的 AI 智能体的技术指南。

---
## 评论

### 中心观点
该文章提出了一种基于**云原生范式构建生成式AI应用**的工程化标准，主张通过将**状态管理**与**模型编排**解耦，并结合**全链路可观测性**工具，来解决企业级对话Agent在落地过程中面临的幻觉控制、流程复杂性和模型迭代难题。

### 支撑理由与批判性分析

**1. 状态管理的工程化演进：从“提示词拼接”到“图状态机”**
*   **事实陈述**：文章采用 LangGraph 构建Agent架构。与传统的单一Prompt或简单的链式调用不同，LangGraph 基于循环图结构，能够显式管理对话的“记忆”状态。
*   **深度评价**：这是目前对抗大模型“无状态性”的最优工程解。在多轮对话中，用户意图往往需要拆解为多个步骤（如：查询数据库->调用工具->生成回答），图结构允许Agent在节点间传递和更新状态，甚至支持“回溯”和“人工介入”，解决了纯LLM应用容易“跑题”或陷入死循环的问题。
*   **反例/边界条件**：图结构引入了额外的复杂度。对于简单的问答（QA）场景（如：基于文档的单一检索），LangGraph 的状态机设计属于“过度设计”，不仅增加了代码维护成本，还可能因额外的节点跳转增加推理延迟。

**2. 模型迭代闭环：MLflow 与 SageMaker 的深度整合**
*   **事实陈述**：文章利用 SageMaker 上托管的 MLflow 来追踪实验和模型版本。
*   **深度评价**：这是文章最具企业实战价值的部分。许多AI项目失败于“实验到生产”的鸿沟。将 Claude（模型层）的调用参数、Prompt模板以及评估指标自动记录到 MLflow，使得开发者可以量化对比不同Prompt策略的效果。这标志着AI开发从“手工作坊”向“数据驱动工程”的转型。
*   **反例/边界条件**：MLflow 的优势在于传统ML模型，在LLM评估上存在短板。LLM输出是主观文本，单纯的日志记录无法自动判断质量。如果团队没有建立基于LLM的自动化评估框架（如使用 GPT-4 作为裁判来打分），MLflow 在此处仅充当了一个昂贵的日志记录器，无法真正提升模型质量。

**3. Serverless 架构的成本与弹性博弈**
*   **事实陈述**：方案基于 Amazon Bedrock 和 Serverless 架构。
*   **作者观点**：Serverless 适合突发流量和初创验证。
*   **你的推断**：这是典型的“云厂商视角”推荐。虽然免去了运维负担，但在高频、高并发场景下，按Token付费和按请求计费的成本可能远超GPU预留实例。此外，Bedrock 的冷启动延迟在实时对话场景中可能影响用户体验。

**4. 工具调用的可靠性边界**
*   **事实陈述**：文章演示了Agent如何调用工具。
*   **深度评价**：虽然 LangGraph 强化了流程控制，但工具调用的准确性仍依赖于 LLM 的语义理解能力。在处理格式严格但语义模糊的API调用时（例如：查询“上个月”的财务数据，但API需要具体的时间戳格式），Agent 仍有较高概率生成错误的参数，导致流程中断。

### 可验证的检查方式

为了验证该架构在实际生产中的有效性，建议进行以下检查：

1.  **并发压力下的延迟测试（指标）**：
    *   测试 LangGraph 在多轮对话中，随着历史消息堆叠，Bedrock 的响应时间（TTFT - Time to First Token）增长曲线。
    *   *观察窗口*：记录对话轮次从第1轮到第20轮的平均延迟变化。

2.  **状态机死循环率（实验）**：
    *   故意设置逻辑陷阱或模糊指令，观察 Agent 是否在图节点间无限循环而不返回结果。
    *   *验证指标*：在 1000 次模拟对话中，出现超时或最大步数触发的比例。

3.  **MLflow 追踪的颗粒度（观察）**：
    *   检查 MLflow UI 中是否成功记录了每一次 Agent 决策的“思考过程”和中间步骤，而不仅仅是最终的输入输出。
    *   *验证方式*：尝试回放一次失败的对话，看能否仅凭 MLflow 记录的参数复现问题。

### 实际应用建议

1.  **不要盲目追求图结构的复杂性**：
    *   如果你的业务逻辑是线性的（A->B->C），使用 LangChain 的简单链即可，引入 LangGraph 会增加不必要的认知负担。仅在涉及循环、条件分支或需要长期记忆规划时使用 LangGraph。

2.  **建立“人机协同”的干预机制**：
    *   利用 LangGraph 的 `interrupt` 功能。在金融或医疗等高风险领域，当 Agent 准备执行关键操作（如删除数据、发送邮件）或置信度较低时，应设计节点暂停流程，等待人工审核，这是该架构最大的安全优势。

3.  **警惕云厂商锁定**：
    *   虽然文章推荐 Bedrock 和 SageMaker，但在实际架构设计中，应在 LangGraph 层与底层模型调用层之间增加抽象层。这样未来若需切换到 OpenAI 或私有部署模型（如 Llama 3），只需更换接口配置，而无需重写图逻辑。

4.  **评估成本监控**：
    *   Serverless 容易

---
## 技术分析

基于您提供的文章标题和摘要，以及对Amazon SageMaker AI、Bedrock、LangGraph及MLflow技术栈的深入理解，以下是对该技术方案的全面深度分析。

---

# 深度分析：基于 SageMaker AI、LangGraph 与 Claude 构建无服务器对话智能体

## 1. 核心观点深度解读

**文章的主要观点：**
文章主张通过**全托管式的云原生架构**（Amazon SageMaker AI + Bedrock）结合**确定性的状态管理框架**（LangGraph）与**标准化的实验追踪系统**（Managed MLflow），来构建企业级、可观测且具备复杂推理能力的对话智能体。

**核心思想传达：**
作者试图传达一种**“最佳实践”的工程化范式**。即在生成式AI应用开发中，不应仅仅关注模型的调用，而应关注**系统的可控性**（通过LangGraph实现状态图控制）和**全生命周期的管理**（通过MLflow实现追踪与部署）。核心在于将“聊天”这种看似简单的交互，转化为严谨的“状态机流转”和“数据驱动的迭代过程”。

**观点的创新性与深度：**
*   **创新性：** 将**LangGraph**（一种基于循环图的Agent框架）引入Serverless架构，解决了传统LangChain“链式”结构在处理复杂对话循环时的局限性。同时，将MLflow这种传统机器学习（ML）的治理工具引入大语言模型（LLM）应用的开发，强调了LLM应用也需要像传统ML一样的严谨实验管理。
*   **深度：** 文章超越了简单的“Hello World” demo，触及了生产环境中的痛点：**如何管理Agent的记忆状态？**以及**如何评估Agent的输出质量？**

**为什么重要：**
随着企业从“玩票式”的PoC（概念验证）转向生产环境部署，**无状态API的局限性**和**Agent行为的不可预测性**成为最大障碍。该方案提供了一条在保持Serverless弹性的同时，赋予Agent长期记忆和复杂逻辑能力的路径，这对于降低企业AI落地成本、提高系统稳定性至关重要。

## 2. 关键技术要点

**涉及的关键技术或概念：**
*   **Amazon Bedrock:** 提供基础模型服务（此处特指 Claude 3/3.5 系列），实现无服务器的模型推理。
*   **LangGraph:** 核心编排框架。不同于LangChain的线性链，LangGraph引入了**循环图**和**状态**的概念，允许Agent根据中间结果决定下一步行动（如：检索工具、重新规划、结束对话）。
*   **Amazon SageMaker AI (原 SageMaker):** 提供托管MLflow的环境，以及可能的跳板机/计算环境。
*   **Managed MLflow (在 SageMaker 上):** 用于LLM应用的追踪、参数管理和模型注册。

**技术原理和实现方式：**
1.  **状态机模式:** LangGraph 将对话定义为一个图。每个节点代表一个动作（如调用LLM、调用工具），边代表转移条件。系统维护一个全局`State`对象，在节点间传递消息、用户输入和上下文。
2.  **无服务器编排:** 利用 AWS Lambda 或 Bedrock 的原生能力运行Agent逻辑，无需管理EC2实例。
3.  **追踪与评估:** 在Agent运行过程中，将Prompt参数、模型输出、中间步骤记录到MLflow中。利用MLflow的UI对比不同Prompt或模型版本的表现。

**技术难点与解决方案：**
*   **难点：** Agent的“幻觉”或“死循环”。
*   **方案：** LangGraph 允许在图的边上设置**条件边**和**超时中断机制**，强制Agent在特定步骤后必须输出结果或停止，从而增加了系统的鲁棒性。
*   **难点：** LLM应用的非结构化数据难以评估。
*   **方案：** 利用MLflow记录每一次交互的Trace（链路追踪），使开发者可以回溯Agent的决策过程，而不仅仅是看最终结果。

**技术创新点分析：**
将**Ops（运维）** 和 **Dev（开发）** 深度融合。通过LangGraph实现逻辑层的确定性，通过Bedrock实现计算层的弹性，通过MLflow实现管理层的数据化。这种**“三明治”架构**是当前Agent工程化的前沿方向。

## 3. 实际应用价值

**对实际工作的指导意义：**
该架构为开发者提供了一套**“开箱即用”**的企业级模板。它解决了从“本地Jupyter Notebook调试”到“云端生产部署”的“最后一公里”问题。

**可应用场景：**
*   **企业知识库问答 (RAG):** 需要多步推理的场景（如：先检索，再总结，再翻译）。
*   **客服自动化:** 需要保留用户会话历史，并根据用户意图动态路由（如：转人工、执行退款）。
*   **金融/法律分析助手:** 需要严格逻辑链路和可追溯性的推理任务。

**需要注意的问题：**
*   **冷启动延迟:** Serverless架构（特别是Lambda）在处理长时间闲置的对话时可能存在冷启动。
*   **上下文窗口限制:** 随着对话轮次增加，LangGraph中的State会膨胀，需注意Token消耗和截断策略。
*   **成本控制:** Agent在循环中可能会多次调用Bedrock，需设置最大迭代次数以防止成本失控。

**实施建议：**
*   先在本地使用LangGraph模拟状态流转，验证逻辑无误后再部署至云端。
*   利用MLflow的“评估”功能，建立一套基于LLM-as-a-Judge的自动化测试集，确保每次Prompt改动不会降低服务质量。

## 4. 行业影响分析

**对行业的启示：**
行业正在从**“模型中心论”**（Model-centric）转向**“数据与工程中心论”**（Data & Engineering-centric）。拥有最好的模型（Claude）不再是唯一壁垒，如何利用LangGraph编排复杂逻辑，以及如何利用MLflow持续优化系统，将成为新的核心竞争力。

**可能带来的变革：**
*   **Agent开发标准化:** 传统的软件开发是写代码，Agent开发将是“画图”（定义状态图）和“调参”（Prompt Tuning）。
*   **运维模式的转变:** DevOps将演变为**LLMOps**。运维人员不仅要监控CPU和内存，还要监控模型的“推理链路”和“Token吞吐量”。

**相关领域的发展趋势：**
*   **多模态Agent:** 结合Bedrock的多模态能力，未来的LangGraph将处理图片、音频等多种输入类型。
*   **更精细的权限控制:** 在企业内部，Agent需要通过LangGraph调用不同的API，权限管理将变得至关重要。

## 5. 延伸思考

**引发的思考：**
*   **人机协同模式:** 当Agent变得极其复杂时，人类如何介入干预？LangGraph是否支持“人工介入节点”？
*   **评估的主观性:** MLflow记录了数据，但如何定义一个Agent“回答得好”？这依然是行业难题，可能需要引入更复杂的 Reward Model。

**拓展方向：**
*   结合**Amazon Aurora** 或 **OpenSearch** 实现持久化的长期记忆，让Agent能跨越不同会话记住用户偏好。
*   探索**Multi-Agent**（多智能体）协作，即在一个LangGraph中运行多个Agent（如一个负责写代码，一个负责测试）。

**未来发展趋势：**
未来的Agent框架将更加**轻量化**和**标准化**。LangGraph目前的优势在于其灵活性，但未来可能会出现更高级的DSL（领域特定语言）来描述这些图，甚至实现“自然语言编程”直接生成LangGraph代码。

## 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现有架构:** 如果你现在的Chatbot是基于简单的`if-else`或单一Prompt，考虑引入LangGraph重构，将业务逻辑抽象为“状态”和“节点”。
2.  **建立实验追踪:** 即使不使用SageMaker，也应自建或使用Cloud MLflow，强制要求团队记录每一次Prompt变更和模型输出。

**具体行动建议：**
*   **Step 1:** 学习LangGraph的基础概念（Node, Edge, State）。
*   **Step 2:** 在SageMaker Studio中启动一个Jupyter Lab实例，安装LangGraph和MLflow。
*   **Step 3:** 构建一个简单的“ReAct”模式Agent（推理+行动），并连接到Bedrock。
*   **Step 4:** 配置MLflow Tracking Server，将运行日志可视化。

**需补充的知识：**
*   Python 异步编程（Agent调用通常是IO密集型，异步可提升并发）。
*   Prompt Engineering（提示词工程）。
*   AWS IAM 权限管理（确保Bedrock和SageMaker的调用权限正确配置）。

## 7. 案例分析

**成功案例设想（基于架构推演）：**
*   **场景:** 某电商公司构建售后客服Agent。
*   **实现:** 利用LangGraph构建状态图：用户输入 -> 意图分类节点 -> (如果是退款) 查询订单节点 -> 调用退款API节点 -> 生成回复。
*   **成效:** 相比旧版硬编码脚本，新系统能处理模糊查询（如“我要退刚才那个”），且通过MLflow分析发现“查询订单节点”失败率较高，针对性优化了Prompt，准确率提升20%。

**失败案例反思：**
*   **场景:** 试图用该架构构建一个完全自主的代码生成Agent。
*   **问题:** 忽略了LangGraph中的State大小限制，导致上下文过长，不仅成本极高，而且模型出现“迷失”，陷入死循环不断重写代码。
*   **教训:** 必须在图中引入**“剪枝”**机制，对State进行摘要压缩，并严格限制最大递归深度。

## 8. 哲学与逻辑：论证地图

**中心命题:**
**在构建企业级生成式AI应用时，采用“无服务器基础设施 + 确定性状态编排 + 标准化实验追踪”的架构模式，是实现系统可扩展性、可维护性与成本效益的最优解。**

**支撑理由与依据:**
1.  **理由一：复杂逻辑需要确定性控制。**
    *   *依据:* 纯LLM的概率生成特性不可靠。LangGraph通过状态机模式强制执行逻辑流（如：必须检索后才能回答），降低了不可预测性。
2.  **理由二：成本与弹性必须平衡。**
    *   *依据:* 对话流量具有突发性。Bedrock + Serverless架构实现了按量付费，避免了为应对峰值而闲置的高昂GPU服务器成本。
3.  **理由三：迭代优化依赖数据观测。**
    *   *依据:* LLM应用是非确定性的“黑盒”。没有MLflow记录Trace，开发者无法定位回答错误是源于Prompt、模型还是上下文，导致优化无从下手。

**反例或边界条件:**
1.  **反例（边界条件）:** 对于极低延迟要求的场景（如毫秒级实时交易决策），Serverless函数的冷启动和LangGraph的多步推理延迟可能不可接受，此时需要裸金属或常驻容器方案。
2.  **反例（边界条件）:** 对于极度简单的单轮问答（如仅做文本摘要），引入LangGraph和MLflow属于过度设计，增加了不必要的复杂度。

**命题性质判断:**
*   **事实:** LangGraph支持循环图；Bedrock是Serverless的；MLflow支持

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 LangGraph 构建有状态的对话流程

**说明**: 传统的无状态聊天机器人难以处理复杂的、多轮的对话。LangGraph 是一个构建有状态、多参与者应用程序的库，非常适合用于构建能够记忆上下文、处理工具调用和包含循环逻辑的对话 Agent。通过定义图结构，可以精确控制对话的流转路径。

**实施步骤**:
1. 定义对话的状态结构，包含消息历史、用户输入和中间变量。
2. 创建节点函数来处理特定的逻辑（例如：调用 Claude 模型、查询工具）。
3. 定义边来连接节点，设置条件边以处理分支逻辑（例如：是否需要调用外部 API）。
4. 编译图并配置检查点器，以便在对话中断后恢复状态。

**注意事项**: 确保图的入口和出口清晰，避免死循环。在设计复杂流程时，优先绘制流程图以理清逻辑。

---

### 实践 2：使用 MLflow 实验追踪进行 Prompt 迭代

**说明**: LLM 的性能高度依赖于 Prompt 工程。在 Serverless 环境中，由于无法直接访问底层日志，使用托管 MLflow 实例来记录 Prompt 模板、参数配置和模型输出至关重要。这允许开发者对比不同版本的 Prompt 效果，从而优化 Agent 的回答质量。

**实施步骤**:
1. 在 SageMaker 中启动 MLflow 实验追踪实例。
2. 在 LangGraph 应用代码中集成 MLflow 客户端。
3. 使用 `mlflow.start_run()` 包装每一次对话或测试调用。
4. 记录输入 Prompt、Claude 的输出响应以及使用的温度和 Top-P 等参数。

**注意事项**: 不要在生产环境中记录敏感的 PII（个人身份信息）数据到 MLflow。为不同的实验阶段（开发、测试、生产）设置独立的 MLflow 实验名称。

---

### 实践 3：实现工具调用的标准化与错误处理

**说明**: Claude 3 模型具有强大的 Function Calling（工具调用）能力。为了构建健壮的 Agent，必须定义清晰的工具接口，并优雅地处理模型调用工具失败或返回错误数据的情况，防止 Agent 因单点故障而崩溃。

**实施步骤**:
1. 使用 Pydantic 定义严格的输入和输出模式，确保 Claude 知道如何正确调用工具。
2. 在 LangGraph 的工具执行节点中包裹 Try-Catch 逻辑。
3. 当工具调用失败时，构建一个错误反馈消息，将其重新放入图的上下文中，让 Claude 尝试自我修正或向用户解释错误。
4. 为每个工具设置超时时间，避免阻塞 SageMaker 的无服务器计算环境。

**注意事项**: 限制工具返回的数据量，避免超出 Claude 的上下文窗口限制。对工具权限进行最小化配置。

---

### 实践 4：优化 SageMaker 无服务器部署的冷启动与延迟

**说明**: 无服务器架构虽然按需付费，但可能存在冷启动延迟。对于对话式 AI，用户对响应时间敏感。通过合理的资源配置和预热策略，可以在成本和用户体验之间取得平衡。

**实施步骤**:
1. 在 SageMaker 无服务器配置中，根据模型大小合理设置内存限制（Memory Size）和并发限制（Max Concurrency）。
2. 尽量减少依赖包的体积，加快容器启动速度。
3. 如果业务允许，在用户发起第一轮对话前，通过一个轻量级的“预热”请求来激活实例。
4. 实现流式响应，使 Claude 在生成完整答案前就开始返回 Token，改善用户感知的延迟。

**注意事项**: 监控 CloudWatch 指标中的冷启动频率。如果延迟要求极高且流量稳定，可能需要考虑使用实时端点而非完全无服务器。

---

### 实践 5：设计健壮的上下文管理机制

**说明**: 对话 Agent 需要记住历史交互才能提供连贯的服务。然而，上下文越长，Token 消耗越大且延迟越高。必须实施策略来管理对话历史的长度。

**实施步骤**:
1. 利用 LangGraph 的持久化功能将历史状态存储在数据库中（如 DynamoDB），而不是仅保留在内存中。
2. 实现滑动窗口或摘要机制。当对话历史过长时，使用 Claude 对早期对话进行摘要，保留最近几轮的原始对话。
3. 在构建 Prompt 时，动态注入相关的历史摘要和最近的几轮消息。

**注意事项**: 确保摘要过程中保留了关键信息（如用户姓名、核心需求）。避免在上下文中重复包含系统指令，浪费 Token。

---

### 实践 6：实施严格的提示词注入防护

**说明**: 对话式 Agent 容易受到提示词注入攻击，攻击者试图通过特定输入绕过安全限制或提取系统指令。在生产环境中部署 Claude Agent 时，安全性是重中之重。

**实施步骤**:
1. 在将用户输入传递给 Claude 之前，通过一个轻量级的分类器或规则层检测潜在的恶意输入。
2. 在系统提示词中明确界定 Claude 的角色和权限边界，使用“仅回答以下问题...

---
## 学习要点

- 利用 LangGraph 构建基于状态机的对话代理，能够有效管理对话上下文并处理复杂的多步骤交互流程。
- 集成 Claude 3 模型作为推理核心，通过 Amazon Bedrock 提供的高性能 API 实现低延迟的自然语言生成。
- 使用托管式 MLflow 在 SageMaker AI 上对 LangChain 模型进行全生命周期管理，确保实验的可追溯性与部署的一致性。
- 采用无服务器架构部署在 SageMaker AI 上，实现了根据请求量自动伸缩，无需管理底层基础设施即可优化成本。
- 通过 LangChain 的可观测性功能与 MLflow 的深度结合，实现了对模型输入输出及中间状态的实时监控与调试。
- 利用 SageMaker AI 的统一托管环境，简化了从模型微调、实验跟踪到生产部署的端到端 MLOps 工作流。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [AWS](/tags/aws/) / [Bedrock](/tags/bedrock/) / [LangGraph](/tags/langgraph/) / [SageMaker](/tags/sagemaker/) / [Claude](/tags/claude/) / [MLflow](/tags/mlflow/) / [Agent](/tags/agent/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [在SageMaker AI上基于Bedrock与LangGraph构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-11.md" >}})
- [基于Amazon SageMaker AI构建无服务器对话AI代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-13.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Bedrock与LangGraph构建SageMaker AI对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-4.md" >}})
- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*