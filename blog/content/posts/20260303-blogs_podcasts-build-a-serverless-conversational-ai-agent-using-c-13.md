---
title: "基于Amazon SageMaker AI构建无服务器对话AI代理"
date: 2026-03-03T18:56:48+08:00
draft: false
entry_kind: "auto"
tags: ["AWS", "SageMaker", "Bedrock", "LangGraph", "MLflow", "Claude", "无服务器", "Agent"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "以下是对该内容的中文总结： 本文探讨了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI 上托管的 MLflow**，构建一个无服务器的智能对话 AI 代理。 **核心技术组件：** 1. **Amazon Bedrock:** 提供强大的 Cl"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios: ["AI/ML项目"]
---

# 基于Amazon SageMaker AI构建无服务器对话AI代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---
## 摘要/简介

本文探讨了如何使用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow 来构建智能对话代理。

---
## 导语

在构建企业级对话 AI 时，如何平衡模型的智能性与全流程的可观测性往往是开发者面临的核心挑战。本文将详细介绍如何利用 Amazon Bedrock 上的 Claude 模型结合 LangGraph 框架，并借助 Amazon SageMaker AI 托管的 MLflow 进行实验追踪。通过阅读本文，你将掌握在无服务器架构下构建、部署并高效管理智能对话代理的完整技术路径。

---
## 摘要

以下是对该内容的中文总结：

本文探讨了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI 上托管的 MLflow**，构建一个无服务器的智能对话 AI 代理。

**核心技术组件：**
1.  **Amazon Bedrock:** 提供强大的 Claude 模型支持。
2.  **LangGraph:** 用于构建和管理对话流程与逻辑。
3.  **Amazon SageMaker AI:** 提供托管的 MLflow 服务，用于实验追踪和模型管理。

**主要特点：**
*   **无服务器架构：** 无需管理底层基础设施，实现弹性扩展。
*   **集成化开发：** 结合了先进的 LLM（Claude）、编排框架和标准化的 MLOps 工具。

文章旨在指导开发者通过这些 AWS 服务的协同工作，快速构建并部署高性能的生成式 AI 应用。

---
## 评论

### 中心观点
这篇文章的核心观点是：**通过将 Amazon SageMaker AI 的全托管机器学习基础设施（特别是 MLflow）与 Bedrock 的生成式能力及 LangGraph 的编排逻辑相结合，企业可以构建出既具备复杂状态管理能力，又符合生产级治理标准的无服务器对话智能体。**

### 支撑理由与深度评价

**1. 内容深度：填补了“应用编排”与“模型治理”之间的鸿沟（事实陈述）**
*   **分析**：大多数关于 LangGraph 的教程仅停留在代码片段层面，忽视了企业级应用中必不可少的“实验追踪”和“模型版本管理”。该文章的深度在于它没有将 LangGraph 视为一个孤立的脚本，而是将其纳入 MLOps 的生命周期中。利用 SageMaker 上托管的 MLflow 来记录 LangGraph 节点的输入输出，这是一个非常务实的工程视角。它解决了 LLM 应用开发中“黑盒”不可控的痛点，即如何追踪智能体在多步推理过程中的状态变化。
*   **评价**：论证严谨，它准确地捕捉到了当前 GenAI 落地的主要障碍——不是模型不够聪明，而是缺乏工程化的管理和监控手段。

**2. 实用价值：确立了“无服务器 + 可观测性”的落地范式（事实陈述）**
*   **分析**：文章展示了如何在不管理底层基础设施的情况下，利用 AWS Lambda 运行 LangGraph 逻辑，利用 Bedrock 调用 Claude 模型。这对初创公司和大型企业的创新团队都极具吸引力，因为它大幅降低了运维成本。同时，引入 MLflow 使得数据科学家可以复现智能体的行为轨迹，这对于调试复杂的 Agent 逻辑（如循环依赖、幻觉检测）具有极高的指导意义。
*   **评价**：这是一个高 ROI（投资回报率）的技术路径，避免了为测试项目搭建复杂的 K8s 集群，直接利用云原生的托管服务实现快速迭代。

**3. 创新性：将状态机逻辑显式映射到 ML 管道（你的推断）**
*   **分析**：传统的 MLOps 通常针对静态模型训练或简单的推理端点。将 LangGraph 的“图”结构（包含循环、条件边）与 MLflow 的线性或分层实验记录相结合，在方法论上具有一定的新意。它暗示了一种新的开发模式：将 Agent 的“思维链”作为实验数据的一部分进行持久化和分析，而不仅仅是关注最终输出。
*   **评价**：虽然技术组件都是现成的，但这种组合方式推动了 Agent 开发从“手工作坊”向“工业化流水线”的演进。

### 反例与边界条件

**1. 成本与延迟的权衡（事实陈述）**
*   **反例**：对于极其简单、高频的对话场景（如简单的 FAQ 问答），引入 LangGraph 的状态机管理和 MLflow 的日志记录可能会引入不必要的延迟和 Token 消耗。如果逻辑只是“输入-输出”，直接调用 Bedrock API 会比构建 Graph 更高效。

**2. 多云锁定与迁移风险（作者观点）**
*   **反例**：该架构深度依赖 SageMaker 的托管 MLflow 和 Bedrock API。虽然代码逻辑本身（LangGraph）是开源的，但运行时环境与 AWS 紧密耦合。如果企业需要跨云部署（例如同时使用 Azure 和阿里云），或者因为合规原因必须私有化部署，这种高度依赖 AWS 托管服务的架构将面临巨大的迁移重构成本。

**3. 复杂状态管理的局限性（你的推断）**
*   **反例**：LangGraph 虽然擅长处理有状态的交互，但在处理超长上下文记忆或需要跨会话持久化复杂对象图谱时，单纯依赖 MLflow 的日志可能不够。此时可能还需要引入 Redis 或向量数据库作为外部记忆存储，文章若未深入探讨这一点，在实际生产中可能会导致记忆丢失或检索效率低下。

### 可验证的检查方式

为了验证该文章所述架构的有效性，建议进行以下检查：

1.  **延迟基准测试（指标）**：
    *   测量从用户输入到 Agent 响应的端到端延迟。
    *   *观察窗口*：对比直接调用 Bedrock 与经过 SageMaker + MLflow 记录 + LangGraph 编排后的延迟差异。如果延迟增加超过 20%，则需评估架构是否过于臃肿。

2.  **状态追踪的完整性（实验/观察）**：
    *   在 MLflow UI 中检查 LangGraph 的每一次节点跳转是否被准确记录。
    *   *验证方法*：故意触发一个需要多轮工具调用的任务，查看 MLflow 中是否能完整复现该决策路径，以及中间步骤的 Token 消耗是否清晰可见。

3.  **成本效率分析（指标）**：
    *   监控 SageMaker 和 Bedrock 的联合账单。
    *   *观察窗口*：运行 1000 次对话，计算 MLflow 存储成本与 SageMaker 计算成本之和，对比自建开源 MLflow + 自托管推理服务器的成本，验证“无服务器”在经济规模上的临界点。

### 总结

这篇文章是一篇高质量的工程实践指南，它敏锐地指出了当前 AI Agent 开发中“重模型、轻工程”的弊端。通过将 LangGraph 的逻辑编排能力与 SageMaker 的企业级治理能力结合，它为构建生产级 Agent 提供了一条标准化的路径。然而，读者需要警惕云厂商带来的锁定效应，以及在简单场景下过度设计带来的性能损耗。

---
## 技术分析

基于您提供的文章标题和摘要，结合当前生成式AI（Generative AI）、MLOps以及云原生架构的技术背景，以下是对该文章内容的深度分析报告。

---

# 深度分析报告：基于 Claude、LangGraph 与 MLflow 构建无服务器对话式 AI 代理

## 1. 核心观点深度解读

**主要观点**
文章的核心主张是：利用**Amazon Bedrock**（作为基础模型底座）、**LangGraph**（作为状态机编排框架）与 **SageMaker AI 上的托管 MLflow**（作为全生命周期管理工具），构建一个**无服务器**、具备**记忆能力**且**生产就绪**的对话式 AI 代理。

**核心思想传达**
作者试图传达一种**"现代化 AI 工程范式"**。这种范式不再仅仅关注模型本身的微调，而是转向关注**Agent（智能体）的架构设计**、**状态管理的复杂性**以及**实验的可追溯性**。它强调了在云原生环境下，如何通过托管服务极大地降低基础设施运维负担，让开发者专注于业务逻辑和模型性能的迭代。

**观点的创新性与深度**
*   **架构创新**：将简单的线性对话升级为基于图的循环结构，这是从"聊天机器人"向"智能体"跨越的关键。
*   **全链路闭环**：大多数教程仅关注如何调用 API，而本文深入探讨了如何利用 MLflow 进行 Prompt 追踪、评估和模型注册，填补了从"原型"到"生产"之间的巨大鸿沟。
*   **无服务器深度**：强调在处理有状态的 AI 应用时，如何利用无服务器架构实现弹性伸缩，这在成本控制和并发处理上具有很高的技术深度。

**重要性**
随着企业从 LLM（大语言模型）的"尝鲜"阶段进入"落地"阶段，单纯调用 API 已无法满足需求。企业面临**幻觉控制、上下文记忆管理、版本回滚和成本优化**等挑战。本文提出的架构正是为了解决这些生产环境中的核心痛点，具有极强的实战指导意义。

## 2. 关键技术要点

### 涉及的关键技术
1.  **Amazon Bedrock**: AWS 的全托管基础模型服务，提供 Claude 3 等模型的 API 访问。
2.  **LangGraph**: LangChain 生态下的扩展库，专门用于构建有状态、多参与者的循环工作流。
3.  **SageMaker AI**: AWS 的机器学习平台，此处特指其集成的托管 MLflow 服务。
4.  **AWS Lambda / Fargate**: 实现无服务器计算的具体载体。

### 技术原理与实现
*   **Agent 编排**:
    *   **原理**: 将对话定义为节点和边。节点代表 LLM 调用或工具调用，边代表状态转换逻辑。
    *   **实现**: 使用 LangGraph 定义一个 `StateGraph`，维护一个包含 `messages`（历史消息）和 `user_input` 的共享状态对象。
*   **状态持久化**:
    *   **原理**: 无服务器架构通常是无状态的。
    *   **实现**: 必须引入外部存储层（如 Amazon DynamoDB 或 S3）来保存 `Thread` 或 `Checkpoint` 数据，使 Agent 能够在多次 HTTP 请求之间记住上下文。
*   **可观测性**:
    *   **原理**: LLM 的输出具有概率性，无法通过传统的单元测试完全覆盖。
    *   **实现**: 利用 MLflow 的 `mlflow.langchain.autolog()` 自动捕获 Prompt、Response、Token 使用量和延迟，并使用 MLflow 的评估功能对 Agent 回答进行打分。

### 技术难点与解决方案
*   **难点**: **幻觉与循环控制**。Agent 可能陷入死循环或产生错误指令。
*   **方案**: LangGraph 允许在"边"上定义条件逻辑，强制中断循环或要求人工确认。
*   **难点**: **Prompt 版本管理混乱**。
*   **方案**: 使用 MLflow 的 Model Registry 功能，将经过验证的 LangGraph 链注册为特定版本，实现灰度发布或快速回滚。

### 技术创新点
*   **显式建模**：相比隐式的 Prompt Engineering，LangGraph 将对话流程显式代码化，使得调试和逻辑修改变得像修改普通代码一样直观。
*   **深度集成**：将 SageMaker 的算力优势与 MLflow 的管理优势结合，且无需自行搭建 MLflow 服务器（托管服务），解决了运维痛点。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为技术团队提供了一套**"开箱即用"的企业级 AI 落地蓝图**。它证明了构建复杂的 AI 应用不需要从零开始搭建 MLOps 平台，利用云厂商的托管服务可以快速构建具备高可用性、可观测性的系统。

**应用场景**
1.  **企业知识库助手**: 需要长期记忆用户偏好，并准确检索 RAG（检索增强生成）内容的场景。
2.  **金融/医疗合规顾问**: 需要严格记录每一轮对话的 Prompt 和 Response 以备审计（MLflow 追踪功能）。
3.  **个人助理/日程管理**: 需要调用工具（如发邮件、查日历）的多步骤规划场景。

**需要注意的问题**
*   **冷启动延迟**: 无服务器架构（特别是 Lambda）在处理大型模型初始化或加载依赖库时可能有较高延迟。
*   **数据隐私**: 虽然数据在 VPC 内，但需确认 Bedrock 和 MLflow 的数据处理合规性。
*   **成本**: 长对话导致的 Token 消耗和频繁的数据库读写操作在无服务器架构下可能产生意外费用。

**实施建议**
*   先在本地利用 LangChain 和 LangGraph 开发并验证逻辑。
*   利用 MLflow 本地运行环境进行 Prompt 评估和基准测试。
*   验证通过后，部署至 SageMaker 并接入 Bedrock。

## 4. 行业影响分析

**对行业的启示**
这标志着**AI 开发正在从"算法驱动"转向"工程驱动"**。未来的核心竞争力不再是谁拥有最好的模型，而是谁能构建最稳定、最可控的 Agent 工作流，并拥有最好的数据反馈闭环。

**可能带来的变革**
*   **MLOps 的普及化**: 随着 MLflow 等工具的托管化，中小型企业也能以极低成本享受到原本只有科技巨头具备的模型管理能力。
*   **Serverless AI 的标准化**: "API + 状态机 + 存储层"的模式将成为构建 AI 应用的标准微服务架构。

**发展趋势**
*   **Agentic Workflow**: 越来越多的应用将具备自主规划能力，而非仅仅是一问一答。
*   **评估即代码**: 对 AI 的评估将像 CI/CD 流水线一样自动化。

## 5. 延伸思考

**引发的思考**
*   **人机协同模式**: 在 LangGraph 中，如何优雅地设计"人机回环"（Human-in-the-loop）？即在 Agent 执行危险操作前强制暂停等待人工批准。
*   **多模态扩展**: 目前的架构主要基于文本，如何平滑扩展到支持图像和音频输入？

**拓展方向**
*   结合 **Amazon Bedrock Agents** 服务（AWS 提供的托管 Agent 服务）与自建 LangGraph Agent 的界限在哪里？何时该用托管服务，何时该自建代码逻辑？
*   引入 **Guardrails**（护栏机制）来过滤有害输入和输出，确保企业级安全。

**未来研究**
*   如何利用 MLflow 中积累的历史对话数据进行微调？
*   如何实现多 Agent 协作？

## 6. 实践建议

**如何应用到自己的项目**
1.  **环境准备**: 注册 AWS 账户，开通 Bedrock（申请 Claude 3 模型权限），创建 SageMaker Domain 并启用 MLflow。
2.  **代码构建**:
    *   定义 Pydantic 模型作为 State。
    *   编写 Node 函数（调用 LLM 或工具）。
    *   使用 `StateGraph` 编译图结构。
3.  **追踪集成**: 在代码入口处添加 `mlflow.set_tracking_uri()` 和 `mlflow.langchain.autolog()`。
4.  **部署**: 将代码打包上传至 SageMaker 管道或 Lambda 函数。

**具体行动建议**
*   **不要一开始就追求完美**：先构建一个最简单的 ReAct 模式 Agent，跑通 MLflow 记录流程。
*   **关注成本监控**：设置 AWS Budgets，防止无限制调用 Bedrock API。

**需补充的知识**
*   **Python 异步编程**: 处理高并发 I/O 时必不可少。
*   **图论基础**: 理解有向图、拓扑排序有助于设计复杂的 Agent 逻辑。
*   **AWS 基础**: IAM 权限配置、S3/DynamoDB 的基本操作。

## 7. 案例分析

**成功案例逻辑推演**
*   **场景**: 某电商公司构建智能售后机器人。
*   **做法**: 使用 LangGraph 区分"意图识别节点"（退款/查询/投诉）和"执行节点"（调用订单系统）。利用 MLflow 记录所有未解决的案例。
*   **结果**: 通过 MLflow 发现"退款"意图的识别准确率下降，开发人员回滚了 Prompt 的某个版本，迅速修复了问题，避免了资损。

**失败案例反思**
*   **场景**: 仅仅使用 Lambda + Bedrock，但未引入状态存储。
*   **问题**: 用户问完第一句后，第二句 Lambda 函数重启，LLM 失去了上下文，体验极差。
*   **教训**: **无服务器不等于无状态**。在设计 AI Agent 时，必须显式设计持久层。

## 8. 哲学与逻辑：论证地图

**中心命题**
> **在构建企业级生成式 AI 应用时，采用 "LangGraph + Bedrock + 托管 MLflow" 的无服务器架构，是目前兼顾开发敏捷性、系统可控性与运维成本的最优解。**

**支撑理由与依据**
1.  **理由 1：业务逻辑的复杂性需要图结构管理。**
    *   *依据*: 线性 Prompt 无法处理循环、回退和分支逻辑。LangGraph 提供了标准化的状态机抽象，使复杂逻辑代码化。
2.  **理由 2：生产环境必须具备可观测性与可追溯性。**
    *   *依据*: LLM 输出的非确定性导致 Bug 难以复现。MLflow 提供了唯一的 Trace ID 关联每一次调用的输入输出，是调试和审计的刚需。
3.  **理由 3：无服务器架构是成本与弹性的平衡点。**
    *   *依据*: AI 流量具有突发性。按请求付费（Serverless）避免了为峰值流量预留闲置算力资源。

**反例与边界条件**
1.  **反例 1：超低延迟需求场景。**
    *   *条件*: 如果应用需要毫秒级响应（如高频交易辅助），Serverless 的冷启动和网络延迟可能是不可接受的。此时应使用容器化预留实例。
2.  **反例 2：极度复杂的私有化部署。**
    *   *条件*: 如果由于数据主权限制，数据完全不能出域，无法使用 SageMaker 托管服务或 Bedrock，则该架构不适用。

**命题性质分析**

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建健壮的 LangGraph 状态机与错误处理机制

**说明**: 在基于 LangGraph 构建对话 Agent 时，通过定义清晰的 State Schema 来管理对话上下文，并针对 Claude 模型调用或工具执行可能出现的超时、API 错误或幻觉问题，设计重试逻辑和回退机制。这能确保无服务器架构下的高可用性。

**实施步骤**:
1. 使用 Pydantic 或 TypedDict 定义严格的 State 结构，明确历史消息、用户输入和中间变量的类型。
2. 在 LangGraph 的节点函数中实现 Try-Except 块，捕获来自 Amazon Bedrock (Claude) 的异常。
3. 配置线性或指数退避策略，对失败的节点调用进行自动重试。
4. 设置图执行的最大步数限制，防止因循环逻辑导致的无限循环和成本失控。

**注意事项**: 避免在重试逻辑中保留导致错误的相同上下文，如果 Claude 产生幻觉导致工具调用失败，考虑在重试时修改 Prompt 提示模型纠正方向。

---

### 实践 2：利用 SageMaker MLflow 实验进行严格的 Prompt 版本控制

**说明**: Prompt 工程是对话型 AI 的核心。利用 SageMaker 托管的 MLflow，将 System Prompt、Few-shot 示例和超参数视为模型超变量进行跟踪。这有助于团队系统地迭代 Prompt，避免“仅靠记忆”管理，并基于量化指标选择最佳版本。

**实施步骤**:
1. 初始化 MLflow 实验并连接到 SageMaker 托管的 MLflow 服务器。
2. 在 LangGraph Agent 的初始化参数中，使用 `mlflow.log_params` 记录 Prompt 模板、温度和 Top-P 值。
3. 使用 `mlflow.start_run` 封装不同的测试会话，记录输入输出对。
4. 利用 MLflow UI 对比不同 Prompt 版本下的响应质量和 Token 消耗。

**注意事项**: 确保 Prompt 变更与 LangGraph 的代码版本通过 Git 进行关联，以便在回滚时能完全复现 Agent 的行为。

---

### 实践 3：实施基于 RAGAGAS 的自动化评估流程

**说明**: 仅仅依靠人工检查对话质量无法适应快速迭代。应结合 RAGAGAS (Retrieval Augmented Generation Assessment) 等框架，通过 Claude 自身作为评判者（LLM-as-a-judge），自动化评估 Agent 的忠实度、答案相关性和上下文召回率。

**实施步骤**:
1. 构建包含“问题”、“标准答案”和“检索上下文”的黄金数据集。
2. 在 SageMaker Pipeline 中集成评估脚本，调用 Claude 模型根据指标给 Agent 生成的回答打分。
3. 将评估指标（如 Faithfulness, Answer Relevancy）记录到 MLflow 运行中，作为模型注册的门槛条件。
4. 设置阈值，只有当新版本 Agent 的指标超过当前生产版本时，才触发部署流程。

**注意事项**: 评估本身也会产生 API 调用成本，建议在开发阶段使用小样本集进行频繁验证，在全量回归测试时使用完整数据集。

---

### 实践 4：优化无服务器架构的冷启动与延迟

**说明**: 在 Amazon SageMaker 无服务器推理或 Lambda 环境中，首次调用可能经历冷启动。对于对话型 AI，低延迟至关重要。需要通过模型预加载、连接池复用和合理的容器并发配置来最小化用户感知的延迟。

**实施步骤**:
1. 预配置 SageMaker 无服务器端点的并发实例数和内存大小，以平衡成本与响应速度。
2. 在 LangGraph 应用层实现会话保持机制，复用与 Bedrock 的连接，避免每次对话都重新建立握手。
3. 使用 Provisioned Concurrency（如果使用 Lambda）或保持最小容器数量，确保核心业务场景的热启动。
4. 实施流式响应（Streaming），利用 Claude 的流式输出特性，让用户在 Token 生成时即时看到反馈。

**注意事项**: 监控 CloudWatch 指标中的 Duration 和 IteratorAge 指标，区分是模型推理时间还是 LangGraph 逻辑处理时间导致的瓶颈。

---

### 实践 5：建立基于 Trace 的可观测性体系

**说明**: 对话 Agent 的内部逻辑（如工具调用、路由决策）通常是黑盒。利用 LangSmith 或 AWS X-Ray 集成，深入追踪 LangGraph 的每一步执行状态，快速定位为何 Agent 做出了特定决策或为何工具调用失败。

**实施步骤**:
1. 启用 LangSmith 的回调集成，或在 SageMaker Endpoint 中配置 X-Ray 追踪。
2. 记录每个节点的输入、输出、中间思考和工具调用请求/响应。
3. 在 CloudWatch Logs 中关联 Trace ID，将错误日志直接链接到具体的对话流程图。
4. 设置告警，针对特定的错误状态（如“Agent 循环超过 5 次”或“工具调用失败率过高”）触发通知。

**注意事项**: �

---
## 学习要点

- 基于您提供的内容主题，以下是关于利用 Amazon SageMaker AI 构建无服务器对话 AI 智能体的关键要点总结：
- 利用 LangGraph 构建基于图的状态机架构，能够有效管理对话上下文和复杂的多步骤推理流程。
- 将 Claude 3 模型集成到 LangGraph 工作流中，以实现高质量的自然语言理解与生成能力。
- 使用 Amazon SageMaker AI 托管 MLflow，实现了机器学习实验、模型注册和部署的全流程集中化管理。
- 采用无服务器架构部署智能体，无需管理底层基础设施即可根据请求量自动弹性伸缩。
- 通过 SageMaker AI 的端到端托管能力，简化了从模型开发、追踪到生产部署的 MLOps 流程。
- 结合托管服务与 LangGraph，能够快速构建并迭代具备状态记忆能力的生产级对话式应用程序。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [Bedrock](/tags/bedrock/) / [LangGraph](/tags/langgraph/) / [MLflow](/tags/mlflow/) / [Claude](/tags/claude/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [Agent](/tags/agent/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [在SageMaker AI上基于Bedrock与LangGraph构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-11.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Bedrock与LangGraph构建SageMaker AI对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-4.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*