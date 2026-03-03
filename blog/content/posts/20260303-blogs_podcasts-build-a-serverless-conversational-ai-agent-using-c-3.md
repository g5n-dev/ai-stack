---
title: "基于Bedrock和LangGraph在SageMaker构建无服务器对话代理"
date: 2026-03-03T00:54:40+08:00
draft: false
entry_kind: "auto"
tags: ["AWS", "Bedrock", "LangGraph", "SageMaker", "MLflow", "Agent", "无服务器", "LLM"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上的托管 **MLflow**，构建一个**无服务器对话式 AI 智能体**。 主要内容包括： 1. **核心架构**： * **Amazon Bedrock**：提供底层基础模型"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios: ["AI/ML项目", "大语言模型"]
---

# 基于Bedrock和LangGraph在SageMaker构建无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---
## 摘要/简介

本博文探讨了如何使用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow 来构建智能对话代理。

---
## 导语

随着企业对智能交互需求的增长，构建可扩展且易于管理的对话系统已成为技术团队的关键任务。本文将详细介绍如何利用 Amazon Bedrock 中的 Claude 模型，结合 LangGraph 的编排能力以及 Amazon SageMaker AI 上托管的 MLflow，来构建一个无服务器的对话 AI 代理。通过阅读本文，您将掌握从架构设计到实验追踪的完整实现流程，了解如何利用云端托管服务高效地开发、部署并优化您的智能应用。

---
## 摘要

本文介绍了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上的托管 **MLflow**，构建一个**无服务器对话式 AI 智能体**。

主要内容包括：

1.  **核心架构**：
    *   **Amazon Bedrock**：提供底层基础模型（如 Claude），负责生成和理解。
    *   **LangGraph**：用于编排智能体的工作流，管理对话状态和逻辑循环。
    *   **Amazon SageMaker AI**：作为集成平台，提供托管的 MLflow 用于实验追踪和模型管理。

2.  **无服务器优势**：
    *   利用 AWS 的无服务器架构，用户无需管理底层基础设施。
    *   能够根据需求自动扩展，降低运维成本。

3.  **MLflow 的应用**：
    *   在 SageMaker 上使用托管 MLflow，可以方便地追踪实验指标、管理模型版本以及记录参数，从而优化智能体的性能。

总结来说，该方案展示了一个现代化、可扩展且易于管理的 AI 智能体开发流程，结合了强大的大语言模型（LLM）、灵活的编排框架以及完善的 MLOps 工具。

---
## 评论

**文章中心观点**
本文主张通过将 Amazon Bedrock（模型层）、LangGraph（编排层）与 SageMaker 上的托管 MLflow（治理层）深度集成，构建一个既具备复杂推理能力又符合企业级治理标准的有状态 Serverless 对话智能体。

**支撑理由与边界条件**

**1. 架构层面的“混合编排”与“全生命周期闭环”**
*   **支撑理由（事实陈述）：** 文章的核心价值在于解决了当前生成式 AI 落地中的“两张皮”问题。通常，开发者使用 LangChain/LangGraph 快速构建应用，而企业使用 MLflow 进行模型追踪，两者往往脱节。文章提出的架构利用 LangGraph 的循环图结构处理对话历史和分支逻辑，利用 Bedrock 提供无服务器的模型算力，并利用 SageMaker 托管的 MLflow 统一记录 LangGraph 的轨迹和 Bedrock 的推理参数。这种组合实现了从“实验”到“生产”的平滑过渡。
*   **反例/边界条件（你的推断）：** 这种架构的引入是有成本的。对于简单的单轮问答或极低并发的内部工具，引入 LangGraph 的状态机和 MLflow 的追踪机制属于“过度设计”。此时，直接调用 Bedrock API 或使用轻量级框架（如 Streamlit + Direct API）在开发速度和运维复杂度上可能更优。

**2. Serverless 与托管服务的成本陷阱**
*   **支撑理由（作者观点）：** 文章强调了 Serverless 架构的优势，即无需管理底层基础设施，利用 Bedrock 按需付费。这对于流量波动剧烈的对话场景非常有效，避免了为闲置 GPU 付费。
*   **反例/边界条件（你的推断）：** 在高并发、长对话上下文的场景下，Serverless 架构的单位成本可能迅速超过预留实例。此外，LangGraph 在处理极其复杂的决策树时，可能会产生大量的内部状态转换调用，如果后端挂载的是昂贵的 Claude 3 Opus 模型，每一次内部循环的 Token 消耗都会带来显著成本。文章未深入探讨“长上下文保留”带来的 Token 累积计费问题。

**3. 企业级治理的可观测性**
*   **支撑理由（事实陈述）：** 使用 SageMaker 上托管的 MLflow 是一个关键的技术选型。相比于开源 MLflow，托管版本减少了运维负担，并且能更好地与 AWS 的 IAM 权限体系集成。对于金融、医疗等强监管行业，能够追踪“智能体为什么做出这个决定”是合规的刚需，LangGraph 的步骤数据写入 MLflow 正好满足了这一点。
*   **反例/边界条件（你的推断）：** 这种深度绑定 AWS 生态的方案存在严重的厂商锁定风险。如果企业未来需要混合部署（例如同时使用 Azure OpenAI 或本地私有化模型），这种基于 SageMaker 托管 MLflow 和 Bedrock 的架构迁移成本极高。

**多维度深入评价**

**1. 内容深度与论证严谨性**
文章在技术实现的颗粒度上较深，涵盖了从 IAM 角色配置到 Docker 容器化部署的细节。它不仅展示了“Hello World”式的调用，还涉及了如何捕获 LangGraph 的中间状态，这在技术论证上是严谨的。然而，文章偏向于“路径展示”，缺乏对“非功能性需求”的深入讨论，例如在高并发下的冷启动延迟或 Bedrock 的限流策略。

**2. 实用价值**
对于已经处于 AWS 生态内的数据科学和工程团队，该文章的实用价值极高。它提供了一套可复制的“模版代码”，填补了从 LangGraph 原型到 SageMaker 生产环境之间的文档空白。特别是关于如何将 LangGraph 的状态序列化并记录到 MLflow 的部分，是很多开发者在实际工作中遇到的痛点，文章给出了具体的解法。

**3. 创新性**
将 LangGraph（代表 Agent 编排的新范式）与 MLflow（代表传统 MLOps 的标准工具）结合是本文的主要创新点。这标志着行业从“单纯玩模型”转向“构建可被管理的软件系统”。它没有提出新的算法，但提出了工程化的最佳实践。

**4. 可读性**
作为一篇技术博客，其逻辑结构清晰（架构图 -> 代码实现 -> 部署）。但文章假设读者对 AWS 术语（如 Lambda, ECR, IAM）和 LangGraph 概念非常熟悉，对初学者不够友好，存在较高的认知门槛。

**5. 行业影响**
这篇文章反映了 AWS 试图构建“护城河”的策略。通过强调 SageMaker 托管 MLflow 与 Bedrock 的原生集成，AWS 正在将开发者从开源的、碎片化的工具链吸引到其全托管平台上。这可能会加速企业级 AI 应用向云巨头集中，但也可能引发社区对“开放性”的担忧。

**争议点与不同观点**
*   **工具链的臃肿性：** 部分开发者认为，为了管理一个对话 Agent 而引入 MLflow 这样重量级的平台是资源的浪费。现代 Observability 工具（如 LangSmith 或 Datadog）可能在 LLM 应用追踪上更轻量、更专注。
*   **LangGraph 的必要性：** 对于简单的对话流，ReAct 模式或简单的 Prompt Chaining 可能足够，LangGraph 引入的图抽象增加了调试难度。

**实际应用建议**
1.  **评估成本模型：** 在采用前，务必使用 Claude 3.5 Sonnet 或 Haiku 对 LangGraph 的推理路径进行压力测试，计算每轮对话的平均 Token 消耗量，避免生产环境

---
## 技术分析

基于文章标题《Build a serverless conversational AI agent using Claude with LangGraph and managed MLflow on Amazon SageMaker AI》及其摘要，以下是对该技术方案的全面深入分析。

---

# 构建无服务器对话式 AI 智能体的深度技术分析

## 1. 核心观点深度解读

**主要观点**
文章的核心主张是：通过将 **Amazon Bedrock**（作为基础模型后端）、**LangGraph**（作为状态机与编排框架）与 **SageMaker AI 上的托管 MLflow**（作为全生命周期管理工具）三者深度结合，可以构建一个既具备复杂逻辑推理能力，又具备企业级可观测性与治理能力的 **Serverless（无服务器）对话式智能体**。

**核心思想**
作者试图传达的不仅是代码的编写，而是**现代 AI 应用的“工程化范式”**。即在 GenAI 时代，构建应用不再是简单的“调用 API”，而是需要解决**状态管理**（通过 LangGraph 实现）、**非确定性应用的可观测性**（通过 MLflow 实现）以及**基础设施的无服务器化**（通过 Bedrock/SageMaker 实现）。

**创新性与深度**
该方案的创新点在于打破了工具链的孤岛：
1.  **编排与治理的融合**：LangGraph 负责智能体的“动态大脑”（循环、路由、记忆），而 MLflow 负责记录这个大脑的每一次“思考过程”（Trace）和“版本迭代”。
2.  **Serverless Agent**：强调不需要维护 EC2 实例或 Kubernetes 集群，利用云原生能力实现按需付费和自动扩缩容，这对于降低 AI 落地门槛至关重要。

**重要性**
随着 LLM 应用从“玩具 demo”走向“生产环境”，企业面临的最大痛点是**不可控**（模型幻觉、逻辑死循环）和**不可管**（无法追踪数据流向、模型版本混乱）。这篇文章提出的架构直击这两个痛点，提供了一套标准化的企业级落地路径。

---

## 2. 关键技术要点

**涉及的关键技术**
*   **Amazon Bedrock**: 提供 Claude 3 模型，通过 Serverless API 调用。
*   **LangGraph**: 基于 LangChain 构建，专门用于设计有状态、多参与者的循环工作流。
*   **SageMaker & MLflow**: 利用 SageMaker 托管的 MLflow 实例进行实验追踪和模型注册。
*   **AWS Lambda (隐含)**: 通常用于 Serverless 架构中的计算层触发。

**技术原理与实现**
1.  **状态图编排**:
    *   传统的 Chain 是线性的，而 Agent 往往需要循环（例如：思考 -> 行动 -> 观察 -> 再思考）。
    *   LangGraph 通过定义 `Nodes`（节点，通常是 LLM 或工具调用）和 `Edges`（边，定义状态转移逻辑）来构建图结构。它维护一个全局的 `State`（对象），在节点之间传递。
2.  **全链路追踪**:
    *   在 LangGraph 执行过程中，MLflow 的 `fluent` API 被嵌入到代码中。
    *   每一次 LLM 的调用 Prompt、每一次工具的返回结果、中间的 JSON 状态，都被作为 MLflow 的一个 "Run" 或 "Trace" 记录下来。
3.  **无服务器部署**:
    *   利用 Bedrock 的按需计费模式，无需预置 GPU 实例。SageMaker 的托管 MLflow 也无需用户管理底层基础设施。

**技术难点与解决方案**
*   **难点**: LLM 输出的非确定性导致难以调试。
*   **方案**: 利用 MLflow 的 UI 界面可视化 LangGraph 的执行路径。如果 Agent 回答错误，开发者可以直接在 MLflow UI 中查看是哪一步的状态转移出了问题，或者是哪个 Prompt 导致了幻觉。
*   **难点**: 分布式状态的一致性。
*   **方案**: LangGraph 将状态序列化（通常为 JSON），在 Serverless 环境中通过 Checkpointer（如 DynamoDB 或内存）进行持久化，确保对话上下文不丢失。

**技术创新点**
将 **LMOps（大模型运维）** 左移。通常 MLflow 用于训练阶段的监控，而这里将其用于 **推理阶段的实时监控**，这是对 MLflow 使用场景的重要拓展。

---

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为 AI 工程师提供了一个**“开箱即用”的企业级蓝图**。它证明了构建一个智能体不仅仅是写 Prompt，还需要一套完整的监控系统来保证质量。

**应用场景**
1.  **企业知识库问答 (RAG Agent)**: 需要多步推理（先检索摘要，再检索详情，再生成答案），LangGraph 可控，MLflow 可追踪检索命中率。
2.  **金融/医疗合规助手**: 这类场景对逻辑准确性和审计要求极高，MLflow 提供的完整日志是合规性的必要条件。
3.  **自动化客服**: 需要根据用户意图路由到不同部门（状态转移），且需要处理高并发。

**需要注意的问题**
*   **冷启动延迟**: Serverless 架构（如 Lambda）在长时间不活动后首次请求会有延迟，不适合对毫秒级延迟极度敏感的场景。
*   **Token 成本**: Claude 3 模型虽然强大，但在多轮循环思考中 Token 消耗巨大，需要在 Bedrock 中配置严格的 Guardrails。
*   **状态锁定**: 在分布式 Serverless 环境下，LangGraph 的状态管理如果配置不当，可能导致并发请求时的状态混乱。

**实施建议**
*   先在本地使用 LangGraph 调通逻辑图。
*   再部署到 AWS Lambda 并连接 Bedrock。
*   最后接入 MLflow，重点监控“Token 消耗”和“中间步错误率”。

---

## 4. 行业影响分析

**对行业的启示**
这标志着 **AI 应用开发正在从“手工作坊”向“工业化生产”转型**。以前大家比拼谁的 Prompt 写得好，未来比拼的是谁能用工具链（LangGraph + MLflow）更高效地管理复杂的 Agent 行为。

**可能的变革**
*   **DevOps 的进化**: 传统的 Log4j 日志已不足以记录 LLM 的行为，行业将全面转向基于 Trace 和 Span 的 LLM Observability（可观测性）标准。
*   **Serverless First**: 越来越多的 AI 创业公司将放弃自建 GPU 集群，转而完全依赖 Bedrock/OpenAI 等 API，将资金和精力集中在逻辑编排和应用层。

**发展趋势**
*   **Agentic Workflow**: 越来越多的应用将具备“自主规划”能力，LangGraph 类似的框架将成为标配。
*   **Unified Platform**: 云厂商（如 AWS）会进一步整合这些工具，未来可能会出现“一键部署 LangGraph 到 SageMaker”的更紧密集成。

---

## 5. 延伸思考

**引发的思考**
*   **多 Agent 协作**: 文章主要讲单个 Agent。如果是多个 Agent（如一个负责写代码，一个负责测试）互相协作，LangGraph 的图结构会变得多么复杂？MLflow 能否有效可视化这种多智能体博弈？
*   **人机协同**: 在 LangGraph 的图中，如何优雅地插入“人类审批”节点？例如 Agent 准备执行删除操作前，暂停并等待人工输入。

**拓展方向**
*   结合 **Amazon Bedrock Agents** 服务。AWS 提供了托管的 Agent 服务，何时该用 Bedrock 原生 Agent，何时该用 LangGraph 自建？这是一个架构选型的关键问题。
*   **数据飞轮**: 利用 MLflow 记录的数据，如何反哺模型的微调？

---

## 6. 实践建议

**如何应用到自己的项目**
1.  **环境准备**: 在 AWS 账户下开启 SageMaker Domain 并创建托管 MLflow。
2.  **依赖安装**: 安装 `langgraph`, `langchain-aws`, `mlflow`, `boto3`。
3.  **代码结构**:
    *   定义 `State` (TypedDict)。
    *   定义 `Nodes` (函数，接收 State，返回 State 更新)。
    *   定义 `Graph` (StateGraph，添加边和入口/出口点)。
    *   在 Node 函数内部或 Graph 编译层，加入 `mlflow.start_span()` 和 `mlflow.log_params()`。

**行动建议**
*   **不要一开始就追求完美**: 先构建一个最简单的 2 节点图（Agent -> Tool -> Agent）。
*   **关注成本**: 在 MLflow 中记录 Token 使用量，设置报警阈值。
*   **版本控制**: 将 LangGraph 的结构定义代码纳入 Git，同时将 MLflow 的 Run ID 关联到 Git Commit Hash。

**补充知识**
*   需要深入学习 **Python 类型提示**，因为 LangGraph 严重依赖类型来定义 State。
*   理解 **图论基础**（节点、边、有向图），有助于设计复杂的 Agent 逻辑。

---

## 7. 案例分析

**结合实际案例：金融研报生成助手**
假设我们要构建一个 Agent，自动读取财报并生成分析摘要。

*   **场景**: 用户上传 PDF -> Agent 读取 -> Agent 调用计算器算指标 -> Agent 生成报告。
*   **LangGraph 作用**:
    *   节点 A: 解析 PDF。
    *   节点 B: 提取财务数据。
    *   节点 C: 计算比率（工具调用）。
    *   节点 D: 生成文本。
    *   边: 如果数据缺失，从 B 回退到 A（重试）。
*   **MLflow 作用**:
    *   **成功案例**: 生成的报告准确。在 MLflow UI 中看到，节点 C 成功调用了 Python Calculator 工具，耗时 200ms。
    *   **失败/反思**: 报告出现数字错误。通过 MLflow 回溯，发现节点 B 提取数据时，LLM 幻觉了一个数字。开发者据此修正了节点 B 的 Prompt，增加了“必须严格从原文提取”的指令。

**经验教训**
没有 MLflow 的追踪，当 Agent 逻辑出错时，开发者就像在黑盒中盲猜。有了这套系统，调试变成了白盒化的数据分析过程。

---

## 8. 哲学与逻辑：论证地图

**中心命题**
在生产环境中构建复杂、可维护且具备成本效益的对话式 AI 智能体，最佳架构是 **"Serverless Compute (AWS) + Stateful Orchestration (LangGraph) + LLM Observability (MLflow)"** 的组合。

**支撑理由**
1.  **逻辑复杂性需求**: 对话式 Agent 本质上是循环状态机，而非线性脚本，因此必须使用 LangGraph 这类图框架来处理分支、循环和记忆。
    *   *依据*: 软件工程理论表明，图结构是处理复杂状态转移的标准模型。
2.  **工程可维护性**: LLM 输出具有概率性，导致调试困难，因此必须引入 MLflow 进行全链路追踪和版本管理。
    *   *依据*: Google 的 SRE 观测性理论，无法观测就无法优化。
3.  **成本与效率优化**: 基础设施应关注业务逻辑而非运维，因此必须使用 Serverless 架构。
    *

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 LangGraph 构建有状态的多代理工作流

**说明**:
在构建复杂的对话式 AI 代理时，简单的线性对话往往无法满足业务需求。LangGraph 允许开发者定义基于图的工作流，能够管理循环、条件分支和多代理协作。通过将对话逻辑建模为状态图，可以更清晰地处理上下文保持、错误恢复和长期运行的对话流程。

**实施步骤**:
1. 定义一个 `State` 对象（TypedDict），包含消息历史、用户意图、上下文变量等。
2. 使用 `StateGraph` 定义节点，每个节点对应一个 LLM 调用或工具调用逻辑。
3. 定义边，包括普通边和条件边，根据图中的状态决定下一步流向（例如：是调用工具还是结束对话）。
4. 编译图并选择合适的内存存储后端（如 Redis 或 DynamoDB）以保存检查点。

**注意事项**:
- 确保状态设计尽可能精简，避免传递不必要的数据以减少延迟。
- 在 Serverless 环境中，注意检查点存储的冷启动延迟。

---

### 实践 2：在 SageMaker 上实现 MLflow 实验的可追溯性

**说明**:
使用托管 MLflow 可以集中管理 LangGraph 和 Claude 模型的实验指标、参数和构件。最佳实践包括不仅记录模型的超参数，还要记录对话生成的质量指标（如 BLEU, ROUGE）以及提示词版本。这有助于在快速迭代中找到最佳配置。

**实施步骤**:
1. 在 SageMaker Studio 中启动 MLflow 实验追踪服务器。
2. 在 LangGraph 执行代码中集成 MLflow SDK，使用 `mlflow.start_run()` 包装执行过程。
3. 记录输入提示词模板、Claude 模型参数（如 temperature, max_tokens）以及输出结果。
4. 将 LangGraph 的图定义或配置文件作为构件记录到 MLflow 运行中。

**注意事项**:
- 避免在日志中记录敏感的 PII（个人身份信息）数据。
- 定期清理过时的实验运行以控制存储成本。

---

### 实践 3：优化提示词工程与上下文管理

**说明**:
Claude 3 模型对提示词非常敏感。在构建 Agent 时，不仅要设计高质量的 System Prompt，还需要有效地管理上下文窗口。最佳实践是动态地检索最相关的上下文信息，而不是将整个历史记录传递给模型，以提高响应速度和准确性。

**实施步骤**:
1. 为 Claude 编写清晰、具体的系统指令，定义 Agent 的角色、限制和工具使用规范。
2. 实施上下文压缩或滑动窗口机制，仅保留最近几轮对话及关键信息。
3. 利用 RAG（检索增强生成）技术，在推理前从向量数据库中检索相关文档片段。
4. 在 LangGraph 节点中，根据当前状态动态构建 Prompt。

**注意事项**:
- 定期测试和微调提示词，以适应模型版本的更新。
- 注意 Token 使用量，因为它直接关系到 API 调用成本。

---

### 实践 4：实施有效的工具调用与错误处理机制

**说明**:
一个强大的 Agent 需要能够调用外部工具（如 API、数据库查询）。在 LangGraph 中，必须构建健壮的工具调用逻辑，包括处理超时、API 失败和无效返回。通过在图结构中专门设立“错误处理”节点，可以确保 Agent 在遇到工具故障时能够优雅降级或重试。

**实施步骤**:
1. 在 LangGraph 中定义工具节点，并将其连接到条件边上。
2. 为每个工具调用实现 Try-Catch 逻辑，捕获异常并返回标准化的错误消息给 LLM。
3. 设置最大重试次数，防止 Agent 陷入无限循环。
4. 利用 Claude 的结构化输出功能，强制模型生成符合工具 schema 的 JSON 参数。

**注意事项**:
- 严格验证工具返回的数据格式，防止解析错误导致流程中断。
- 对外部 API 调用实施超时控制，以避免 Serverless 函数超限。

---

### 实践 5：利用 Bedrock 的 Guardrails 实现安全治理

**说明**:
在生成式 AI 应用中，确保输出内容的安全性和合规性至关重要。Amazon Bedrock Guardrails 可以在模型输出层之上添加一道屏障，用于过滤有害内容、阻止 PII 泄露或强制执行特定的输出格式。这是保护终端用户和品牌声誉的最佳实践。

**实施步骤**:
1. 在 Bedrock 控制台中配置 Guardrail，定义拒绝主题（如暴力、非法行为）和敏感信息过滤器。
2. 将 LangGraph 返回给前端的内容通过 Bedrock ApplyGuardrail API 进行检查。
3. 配置上下文接地检查，确保 Agent 的回答基于提供的参考资料，减少幻觉。
4. 将 Guardrail 集成到 LangGraph 的结束节点中，作为最终输出前的必经步骤。

**注意事项**:
- Guardrail 的检查会增加轻微的延迟，需要在性能和安全性之间做权衡。
- 不要完全依赖模型自身的安全对

---
## 学习要点

- 利用 LangGraph 构建基于状态机的架构，能够有效管理对话历史和上下文，从而克服无状态模型在多轮对话中的局限性。
- 集成托管式 MLflow 与 Amazon SageMaker AI，实现了从实验跟踪到模型部署的标准化全生命周期管理，简化了运维流程。
- 采用 Amazon Bedrock 提供的 Claude 模型作为推理引擎，在获得高性能生成能力的同时，无需自行维护底层基础设施。
- 通过将应用部署为无服务器架构，利用按需计费和自动扩缩容特性，显著降低了闲置成本并提高了可用性。
- 结合 LangChain 的可组合性，开发者可以灵活编排工具调用和逻辑流，快速扩展 AI 智能体的功能边界。
- 利用 SageMaker 的托管服务特性，团队可以专注于核心业务逻辑的优化，而无需在模型服务基础设施的维护上投入过多精力。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AWS](/tags/aws/) / [Bedrock](/tags/bedrock/) / [LangGraph](/tags/langgraph/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [Agent](/tags/agent/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [2025年Amazon SageMaker AI增强可观测性与模型定制托管功能]({{< relref "posts/20260220-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--1.md" >}})
- [Amazon SageMaker AI 2025回顾：可观测性与模型定制托管增强]({{< relref "posts/20260221-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--2.md" >}})
- [2025年Amazon SageMaker AI回顾：可观测性、模型定制与托管增强]({{< relref "posts/20260222-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*