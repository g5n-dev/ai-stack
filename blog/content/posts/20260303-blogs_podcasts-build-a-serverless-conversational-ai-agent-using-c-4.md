---
title: "基于Amazon SageMaker AI构建Claude无服务器对话代理"
date: 2026-03-03T09:40:55+08:00
draft: false
entry_kind: "auto"
tags: ["AWS", "Amazon Bedrock", "Claude", "LangGraph", "SageMaker", "MLflow", "Agent", "无服务器"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "**摘要：利用 Claude、LangGraph 和 SageMaker AI 托管 MLflow 构建无服务器对话式 AI 智能体** 本文介绍了如何结合 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow，构建一个智能的无服务器对话式 AI 智能体"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios: ["AI/ML项目"]
---

# 基于Amazon SageMaker AI构建Claude无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---
## 摘要/简介

本文探讨如何使用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow 来构建智能对话代理。

---
## 导语

随着生成式 AI 的落地应用，如何构建具备记忆与状态管理能力的对话代理成为开发者关注的重点。本文将详细介绍如何利用 Amazon Bedrock 中的 Claude 模型、LangGraph 框架以及 Amazon SageMaker AI 上托管的 MLflow，来搭建一个无服务器的智能对话系统。通过阅读本文，您将掌握从模型编排到实验追踪的完整流程，从而高效构建并优化生产级的 AI 应用。

---
## 摘要

**摘要：利用 Claude、LangGraph 和 SageMaker AI 托管 MLflow 构建无服务器对话式 AI 智能体**

本文介绍了如何结合 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow，构建一个智能的无服务器对话式 AI 智能体。文章重点阐述了该解决方案的技术架构、实现步骤及其在简化开发流程方面的优势。

**1. 核心技术栈与架构**
该解决方案旨在利用生成式 AI 构建能够处理复杂任务的智能体，主要包含以下组件：
*   **Amazon Bedrock**：作为底层基础模型服务，提供高性能的 Claude 3 模型，用于生成响应和处理自然语言。
*   **LangGraph**：用于构建智能体的核心逻辑。它通过有向图定义状态机，控制智能体的推理循环、工具调用和多步骤交互流程，使智能体能够根据上下文自主决定下一步行动。
*   **Amazon SageMaker AI 托管的 MLflow**：用于全生命周期的机器学习管理。MLflow 负责跟踪实验、管理模型版本以及记录参数和指标，确保开发过程的可重复性和可追溯性。

**2. 实现方案概述**
文章指导开发者从零开始部署这一系统，主要步骤包括：
*   **环境准备**：利用 AWS CloudFormation 或类似工具快速部署基础设施，确保 Amazon SageMaker、Bedrock 及相关权限配置正确。
*   **模型与逻辑集成**：通过 LangGraph 定义智能体的行为图，集成 Claude 模型作为“推理引擎”，并配置必要的工具（如数据查询或 API 调用）。
*   **实验追踪**：在 SageMaker 环境中启用托管 MLflow，将 LangGraph 的运行参数、Prompt 版本以及输出结果记录到 MLflow 中。这使得开发者可以对比不同配置的性能，优化智能体表现。

**3. 方案优势**
*   **无服务器架构**：利用 AWS 的托管服务，无需维护底层基础设施，实现弹性伸缩和按需付费。
*   **可观测性与治理**：通过集成 MLflow，解决了传统 AI 开发中缺乏版本控制和实验追踪的痛点，使企业能够安全地管理和部署生成式 AI 应用。

**总结**
本文展示了一个现代化的生成式 AI 落地范式，通过将 Amazon Bedrock 的强大模型能力、LangGraph 的灵活

---
## 评论

### 深度评论：构建基于 AWS 的全栈无服务器对话智能体

**中心观点**
本文构建了一个基于 Amazon 全栈生态的无服务器对话智能体范式，主张通过 LangGraph 实现复杂状态管理、利用 Bedrock 托管模型能力并结合 MLflow 进行实验追踪，以此系统性解决生成式 AI 应用从原型到生产过程中面临的可观测性缺失、扩展性瓶颈与成本控制难题。

**核心价值与架构解析**

**1. 云原生“黄金路径”的工程化落地**
文章的核心逻辑在于展示 AWS 托管服务如何消弭基础设施复杂性。
*   **技术互补性**：将 LangGraph 的循环计算图与 Bedrock 的 Serverless 调用结合，在架构上极具合理性。LangGraph 有效解决了传统链式调用难以维持的上下文状态持久化问题，而 Bedrock 则彻底屏蔽了底层 GPU 资源的运维痛点。
*   **可观测性实践**：文章不仅展示了模型调用，更强调了利用 Managed MLflow 记录 Trace（追踪）和 Prompt 版本。这种“全链路监控”视角是区分“Demo 级”与“生产级”应用的关键，为解决 LLM 应用常见的“黑盒化”问题提供了具体路径。

**2. 成本效益与弹性博弈**
作者主张利用 Serverless 架构应对对话流量的波峰波谷，这对初创企业或流量不可预测的业务确实能显著降低 CapEx（资本支出）。
*   **边界条件警示**：然而，对于高并发、低延迟要求的成熟业务，Serverless 的冷启动可能导致不可接受的延迟。此时，预留实例或自托管推理端点可能更具性价比。

**局限性与潜在风险**

**1. 供应商锁定的隐形成本**
该架构深度耦合了 AWS 特定服务（Bedrock, SageMaker）。虽然集成效率极高，但若未来 Claude API 定价调整或需迁移至 GCP/Azure，重构包含 AWS 特定 SDK 的状态逻辑与部署脚本将带来高昂的迁移成本。

**2. 安全围栏与幻觉治理的缺失**
文章侧重于“怎么搭起来”，却忽视了“怎么搭得好”。在构建 Agent 时，如何利用 Bedrock Guardrails 或 LangGraph 的逻辑回路防止提示词注入和数据泄露，是生产环境中比架构搭建更为关键的安全议题，文中对此涉及较少。

**批判性思考与替代方案**

*   **过度工程化风险**：对于简单的对话任务，引入 LangGraph（状态机）+ MLflow（全链路追踪）可能存在过度设计。简单的 FastAPI + OpenAI SDK 可能足以应对 MVP 阶段。
*   **工具链的排他性**：虽然 MLflow 是行业标准，但在 LLM 领域，LangSmith 可能提供了对 LangGraph 更原生的追踪体验。在 SageMaker 上强行使用 MLflow 追踪 LangGraph，虽然在统一管控上有优势，但在开发体验（DX）上未必优于原生工具链。

**总结**
本文为 AWS 重度用户提供了一套高可用的生产级落地指南，但在采纳前，架构师需权衡供应商锁定风险，并补充必要的安全治理模块。

---
## 技术分析

基于文章标题《Build a serverless conversational AI agent using Claude with LangGraph and managed MLflow on Amazon SageMaker AI》及摘要内容，以下是对该技术方案的深入分析。虽然无法获取全文细节，但基于AWS技术生态、LangGraph架构模式以及MLOps的标准实践，可以对该文章的核心逻辑进行高度还原和深度剖析。

---

## 1. 核心观点深度解读

**主要观点：**
文章主张通过**全托管的无服务器架构**来构建复杂的对话式AI智能体。它不再仅仅关注模型本身，而是强调如何利用**Amazon Bedrock**（模型层）、**LangGraph**（编排与状态管理层）和**SageMaker上的托管MLflow**（实验与追踪层）三者结合，构建一个生产级、可观测、可迭代且具备成本效益的AI应用系统。

**核心思想：**
作者传达的核心思想是**“关注点分离”与“工程化最佳实践”**。将大模型的推理交给Bedrock，将复杂的对话逻辑和状态管理交给LangGraph，将模型的全生命周期管理（追踪、注册、部署）交给SageMaker集成的MLflow。这种组合让开发者能够像构建传统软件一样构建AI应用，而不是停留在脚本原型阶段。

**创新性与深度：**
其创新点在于**将状态机引入对话流**。传统的对话机器人通常基于简单的轮次或线性流程，难以处理复杂的多步骤任务。LangGraph引入了图结构，允许Agent进行循环、回退和分支，这是从“聊天机器人”向“任务执行体”跨越的关键。同时，利用SageMaker托管MLflow，解决了企业级AI开发中普遍存在的“实验孤岛”问题。

**重要性：**
随着大模型落地进入深水区，企业面临的挑战不再是“怎么调用API”，而是“如何管理成百上千个Prompt版本”、“如何追踪Agent的决策路径”以及“如何控制成本”。该文章提出的架构直接回应了这些痛点，提供了一条通往企业级AI治理的标准化路径。

## 2. 关键技术要点

**涉及的关键技术：**
1.  **Amazon Bedrock:** AWS的托管基础模型服务，提供Claude 3等模型的API调用。
2.  **LangGraph:** LangChain生态下的扩展库，用于构建有状态、多Actor的图结构应用。
3.  **Managed MLflow on SageMaker:** 开源的MLOps平台在AWS上的托管版本，用于MLflow Tracking、Model Registry等。
4.  **AWS Lambda / Fargate (隐含):** 用于承载LangGraph运行时的无服务器计算环境。

**技术原理与实现：**
*   **Agent编排:** 利用LangGraph定义节点和边。节点代表LLM调用或工具调用，边代表逻辑流转。通过维护一个`State`对象，在图的各个节点间传递历史消息、上下文和中间结果。
*   **模型调用:** LangGraph作为Controller，通过Bedrock API调用Claude模型。利用Bedrock的Converse API或Messages API，实现流式响应或结构化输出。
*   **全生命周期管理:** 在LangGraph的节点中，或者在开发阶段，利用MLflow SDK记录Prompt模板、模型参数（Temperature, TopP）以及Agent的执行轨迹。MLflow作为“单一事实来源”，记录哪个版本的Prompt产生了最好的结果。

**技术难点与解决方案：**
*   **难点：** 对话Agent的**状态持久化**。在无服务器环境中，内存是不共享的。
*   **方案：** LangGraph支持使用外部存储（如Redis、DynamoDB）来保存检查点。这使得Agent在处理长对话或需要异步回调（如等待人工审批）时，能够从断点恢复，而不是从头开始。
*   **难点：** **可观测性**。图结构执行路径复杂，难以调试。
*   **方案：** 将LangGraph的执行步骤与MLflow的日志记录绑定，或者利用LangSmith（虽然文章主要提MLflow），可视化每一步的输入输出。

**技术创新点：**
将**MLOps（MLflow）**与**AgentOps（LangGraph）**在Serverless环境中打通。通常MLOps关注训练模型，而AgentOps关注推理时的行为。该方案暗示了可以将Prompt Engineering视为一种“微调”，利用MLflow来管理Prompt版本，这是LLM Ops的一个重要范式转变。

## 3. 实际应用价值

**指导意义：**
该架构为CIO和CTO提供了一个**“降本增效”**的蓝图。无服务器架构意味着不需要维护GPU集群，按量付费；使用托管服务减少了运维负担。它教导开发者不要重复造轮子，而应专注于业务逻辑的图结构设计。

**应用场景：**
1.  **企业知识库助手：** 需要多轮对话、检索增强生成（RAG）以及准确记录来源的场景。
2.  **金融/医疗合规助手：** 需要严格记录每一次决策依据（MLflow追踪）和对话历史的场景。
3.  **自动化客服与工单处理：** Agent需要根据用户意图进行分支操作（如退款、查询、转人工），LangGraph的图结构非常适合此类流程。

**注意问题：**
*   **冷启动延迟：** Serverless函数（如Lambda）在长时间闲置后冷启动可能导致首字回复延迟。
*   **上下文窗口限制：** 虽然Claude 3支持大窗口，但LangGraph的State如果无限增长会消耗大量Token并增加延迟。需要实施适当的截断策略。
*   **Vendor Lock-in (厂商锁定):** 深度依赖Bedrock和SageMaker生态，迁移成本较高。

**实施建议：**
先在SageMaker Studio中利用Notebook进行实验，使用MLflow记录不同Prompt模板的效果。验证逻辑无误后，将LangGraph代码封装为容器或Lambda函数，通过Bedrock调用模型，部署到生产环境。

## 4. 行业影响分析

**对行业的启示：**
这标志着**AI开发正在从“手工作坊”向“工业化流水线”转变**。过去开发者写Python脚本调用OpenAI API；现在企业需要一套完整的系统来管理Prompt、追踪状态和部署模型。AWS通过整合Bedrock、SageMaker和开源工具（LangChain/MLflow），正在定义企业级AI开发的标准栈。

**可能的变革：**
*   **Prompt工程管理的正规化：** MLflow的引入意味着Prompt不再只是代码里的字符串，而是被版本管理的资产。
*   **Agent作为服务：** 未来企业交付的软件可能不再是有固定界面的App，而是具备特定技能的Agent。

**发展趋势：**
*   **Agentic Workflow（代理工作流）**将成为LLM应用的主流形态，取代单一的Prompt调用。
*   **MLOps与LLMOps的融合：** 传统的模型管理工具（如MLflow）正在迅速进化以支持LLM特有的Trace和Evaluate功能。

## 5. 延伸思考

**拓展方向：**
*   **多模态扩展：** 该架构是否支持图片输入（Claude 3的能力）？如何在LangGraph的State中传递非文本数据？
*   **人机协同：** LangGraph允许中断执行，这为“AI做草稿，人类审核”的工作流提供了天然支持。
*   **评估体系：** 仅仅记录是不够的。如何利用MLflow的Evaluation功能来自动评估Agent的回答质量？建立“黄金数据集”是下一步。

**未来研究：**
如何实现**自愈Agent**？即Agent发现自己执行路径错误时，利用MLflow记录的历史数据，自动调整Prompt或重试路径。

## 6. 实践建议

**如何应用到项目：**
1.  **环境搭建：** 在AWS账号中启用SageMaker Domain，并配置托管MLflow。
2.  **原型开发：** 使用LangGraph定义你的业务流程图。例如：`Input -> Classify Intent -> [Route: RAG / Route: SQL] -> Output`。
3.  **实验追踪：** 在代码中集成`mlflow.start_run()`，记录每次运行的Prompt和模型参数。
4.  **部署：** 将LangGraph编译成的应用部署为API endpoint。

**行动建议：**
*   学习**状态机**的设计模式，理解如何将业务逻辑映射为图结构。
*   熟悉**MLflow的Logging API**，特别是如何记录LLM相关的参数和指标。
*   关注**成本监控**，为Bedrock调用设置预算告警。

**补充知识：**
需要深入了解Python异步编程（因为LLM调用是IO密集型），以及AWS IAM权限控制（确保Bedrock和SageMaker的访问安全）。

## 7. 案例分析

**成功案例（假设性构建）：**
一家电商公司构建了“售后处理Agent”。
*   **流程：** 用户发起投诉 -> LangGraph节点判断情感（负面） -> 节点调用Bedrock生成共情回复 -> 节点查询订单系统 -> 节点计算退款金额 -> 生成工单。
*   **MLflow作用：** 团队发现V1.0版本的Agent退款金额计算错误。通过查看MLflow记录的Trace，发现是Prompt中关于“税费”的描述有歧义。修改Prompt并在MLflow中注册V2.0版本，重新部署，问题解决。

**失败反思：**
如果直接使用简单的LangChain链而不是LangGraph，当用户中途改变意图（从“退货”变为“咨询产品”），Agent可能会陷入死循环或无法回退。这凸显了图结构和状态管理的重要性。

## 8. 哲学与逻辑：论证地图

**中心命题:**
在构建企业级生成式AI应用时，采用**“Amazon Bedrock + LangGraph + 托管MLflow”的无服务器架构**，是实现**开发效率、系统可控性与成本优化**三者平衡的最优技术解。

**支撑理由:**
1.  **可控性:** LangGraph的图结构提供了比线性链更精确的流程控制能力，能够处理包含循环、分支和条件判断的复杂任务逻辑，这是构建可靠Agent的基础。（依据：软件工程中的控制流理论；复杂系统无法通过单一Prompt解决）
2.  **可观测性与迭代:** 集成MLflow使得Prompt工程和模型参数从“黑盒”变为“白盒”，允许团队通过数据驱动的方式迭代模型，而非依靠直觉。（依据：MLOps最佳实践；DevOps中的监控反馈循环）
3.  **敏捷性与成本效益:** 无服务器架构消除了基础设施维护开销，并根据实际请求量付费，极大降低了初创期和业务波动期的试错成本。（依据：云经济学中的CapEx转OpEx优势）

**反例 / 边界条件:**
1.  **极端低延迟要求:** 如果业务要求毫秒级响应（如高频交易辅助），Serverless函数的冷启动延迟和网络跳转可能成为不可接受的瓶颈，此时需要裸金属或预留实例。
2.  **数据主权与隐私:** 如果企业法规要求数据绝不能离开本地VPC或特定物理区域，完全依赖公网Bedrock API可能存在合规风险（尽管Bedrock支持VPC Interface，但架构复杂度增加）。

**命题性质分析:**
*   **事实:** LangGraph支持状态机；Bedrock是托管服务；MLflow支持追踪。
*   **价值判断:** “最优”、“平衡”是基于企业级应用标准的判断。
*   **可检验预测:** 采用该架构的团队，其从原型到生产环境的部署速度将比传统自建集群的方式快X倍（假设），且运维人力投入将显著降低。

**立场与验证:**
我支持该命题作为

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建基于 LangGraph 的有状态对话工作流

**说明**:
利用 LangGraph 的循环图结构来管理对话状态，而不是简单的线性链。这允许 AI 智能体根据上下文进行自我修正、回溯或调用外部工具。在 Serverless 环境中，通过显式定义状态模式，确保在无状态函数调用之间保持对话上下文的连贯性。

**实施步骤**:
1. 定义一个 `TypedDict` 结构来明确对话状态的数据模式（如消息历史、用户意图、中间变量）。
2. 使用 `StateGraph` 构建工作流，定义节点（Node）为具体的 LLM 调用或工具使用逻辑，定义边（Edge）为状态转换条件。
3. 实现条件边，根据模型输出（如意图识别结果）路由到不同的后续节点（例如：查询数据库 vs. 结束对话）。

**注意事项**:
- 避免在状态中存储过大的上下文对象，以防超出 Lambda 或容器限制。
- 确保状态序列化格式（如 JSON）兼容，以便在 SageMaker endpoints 之间传递。

---

### 实践 2：实施严格的 Prompt 工程与模板管理

**说明**:
在 Serverless 架构中，代码更新可能不如传统服务器灵活，因此需要将 Prompt 模板与业务逻辑解耦。利用 Claude 的长上下文窗口能力，构建包含系统角色、任务指令和少样本示例的结构化 Prompt。

**实施步骤**:
1. 将 System Prompt 存储在 S3 或 Parameter Store 中，而非硬编码在函数内。
2. 使用 LangChain 的 `PromptTemplate` 或 `ChatPromptTemplate` 动态注入用户上下文。
3. 为 Claude 设置明确的输出格式指令（如 JSON 或 XML），以便后续节点解析。

**注意事项**:
- 定期审查 Prompt 以防止“提示词注入”攻击。
- 在 Prompt 中包含“护栏”指令，限制模型回答超出范围的问题。

---

### 实践 3：利用 MLflow 跟踪与模型注册中心进行实验管理

**说明**:
使用 Amazon SageMaker 上托管的 MLflow 来记录 LangGraph 工作流的参数、指标和模型产件。这有助于迭代优化 Prompt 参数、温度设置或不同的模型版本（如 Claude 3 Opus vs. Sonnet）。

**实施步骤**:
1. 在 SageMaker Studio 中初始化 MLflow 实验并设置追踪 URI。
2. 在 LangGraph 执行节点中包装 MLflow `start_run`，记录输入 Prompt、输出响应和 Token 消耗。
3. 将表现最好的 Prompt 模板或 LangChain 工具链注册到 MLflow Model Registry，并打上生产环境标签。

**注意事项**:
- 确保记录的数据不包含敏感 PII（个人身份信息）。
- 利用 MLflow 的模型别名功能，实现 A/B 测试或蓝绿部署，无需更改底层推理代码。

---

### 实践 4：优化 SageMaker 端点配置以实现成本与延迟平衡

**说明**:
Claude 模型调用通常涉及较高的延迟和 Token 成本。在 Serverless 设置下，需要合理配置 SageMaker 的推理选项（如 Serverless Inference 或 Multi-Model Endpoints）以应对突发流量，同时控制成本。

**实施步骤**:
1. 对于开发测试环境，使用 SageMaker Serverless Inference 按毫秒计费，避免配置闲置实例。
2. 对于生产环境，如果需要低延迟，考虑使用 SageMaker Inference Components（推理组件）动态调整计算容量。
3. 实现请求批处理或利用 Claude 的流式响应 API 提升终端用户的感知速度。

**注意事项**:
- 监控 `InvocationsPerInstance` 指标，防止触发 SageMaker 的并发限制。
- 设置合理的超时时间，避免因 Claude 处理长上下文导致 Lambda 函数超时。

---

### 实践 5：建立全面的可观测性与日志记录机制

**说明**:
在分布式 Serverless 架构中，调试对话失败的原因较为困难。必须集成 CloudWatch 和 X-Ray 来追踪请求从 API Gateway 到 SageMaker Endpoint 的完整链路，特别是 LangGraph 中的循环逻辑。

**实施步骤**:
1. 启用 AWS X-Ray 追踪 LangGraph 的每个节点执行时间，识别性能瓶颈。
2. 将 LangChain 的回调处理器配置为将 Token 使用情况、中间步骤和最终输出发送到 CloudWatch Logs。
3. 为 MLflow 设置告警，当模型准确率下降或响应时间过长时触发通知。

**注意事项**:
- 注意日志采样率，避免产生巨额 CloudWatch 费用。
- 确保敏感数据在记录到日志之前已被脱敏。

---

### 实践 6：设计健壮的错误处理与重试策略

**说明**:
网络抖动、限流或模型幻觉都可能导致对话中断。在 LangGraph 工作流中必须集成错误捕获逻辑，确保即使某个工具调用失败，智能体也能优雅降级或重试，

---
## 学习要点

- 利用 LangGraph 构建基于 Claude 的有状态对话代理，通过循环图结构管理对话上下文，实现复杂的多轮交互逻辑。
- 在 Amazon SageMaker AI 上部署托管的 MLflow，集中化跟踪 LangGraph 实验的指标、参数和模型版本，简化开发流程。
- 将 LangGraph 应用程序封装为标准的 LangChain 服务，使其能够无缝接入 MLflow 进行模型注册和部署管理。
- 结合 Amazon Bedrock 提供的 Claude 模型与 SageMaker 的托管基础设施，实现无需管理服务器的全托管 Serverless 架构。
- 利用 SageMaker AI 的集成环境直接部署和运行 MLflow，消除了自行搭建和运维 MLflow 服务器的复杂性。
- 通过 MLflow 的模型注册功能，可以统一管理从 LangGraph 实验到生产环境的模型全生命周期，确保部署的一致性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AWS](/tags/aws/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [Claude](/tags/claude/) / [LangGraph](/tags/langgraph/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [Agent](/tags/agent/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Amazon SageMaker AI构建无服务器Claude对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [Amazon Bedrock 新增中东区域支持 Anthropic Claude 模型推理]({{< relref "posts/20260224-blogs_podcasts-introducing-amazon-bedrock-global-cross-region-inf-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*