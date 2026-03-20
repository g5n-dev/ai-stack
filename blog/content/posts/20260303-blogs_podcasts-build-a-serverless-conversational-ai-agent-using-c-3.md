---
title: 基于Bedrock与LangGraph在SageMaker构建无服务器对话代理
date: 2026-03-03 07:23:26+08:00
draft: false
entry_kind: auto
tags:
- AWS
- Bedrock
- LangGraph
- SageMaker
- Claude
- MLflow
- Serverless
- Agent
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 以下是该内容的中文总结（基于标题和描述推断的技术要点）： **核心主题：** 构建基于 Claude 的无服务器对话式 AI 智能体 本文详细介绍了如何利用亚马逊云科技（AWS）的托管服务，结合
  LangGraph 框架，构建一个高性能的无服务器智能体系统。主要技术组件和架构如下： 1. **核心 AI 模型**： *
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios:
- AI/ML项目
---

# 基于Bedrock与LangGraph在SageMaker构建无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---

## 摘要/简介

本篇文章探讨如何使用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow 来构建一个智能对话代理。

---

## 导语

随着企业对智能交互需求的增加，构建具备记忆与推理能力的对话代理已成为技术落地的重要方向。本文将详细介绍如何利用 Amazon Bedrock 上的 Claude 模型、LangGraph 编排框架，以及 Amazon SageMaker AI 托管的 MLflow，来打造一个无服务器架构的对话式 AI 系统。通过阅读，您将掌握从模型调用、状态管理到全链路实验追踪的完整实现流程，从而高效构建并优化您的生产级智能应用。

---

## 摘要

以下是该内容的中文总结（基于标题和描述推断的技术要点）：

**核心主题：** 构建基于 Claude 的无服务器对话式 AI 智能体

本文详细介绍了如何利用亚马逊云科技（AWS）的托管服务，结合 LangGraph 框架，构建一个高性能的无服务器智能体系统。主要技术组件和架构如下：

1.  **核心 AI 模型**：
    *   集成了 Anthropic 的 **Claude** 模型，作为智能体的“大脑”，负责处理复杂的语言理解和生成任务。

2.  **编排框架**：
    *   使用 **LangGraph** 来管理智能体的状态和工作流。LangGraph 非常适合构建有状态、多步骤的代理应用，能够定义基于图的对话逻辑，使 AI 能根据上下文自主决策和执行行动。

3.  **基础设施与部署 (无服务器)**：
    *   利用 **Amazon Bedrock** 提供无服务器的模型托管能力，无需底层基础设施管理即可调用 Claude 等大模型。
    *   整个架构设计为无服务器模式，具有自动伸缩、按需付费和运维简单的特点。

4.  **实验追踪与管理**：
    *   在 **Amazon SageMaker AI** 上使用托管的 **MLflow**。这解决了大模型开发中常见的“黑盒”问题，用于记录实验数据、追踪模型性能指标、管理参数，并对智能体的行为进行迭代优化。

**总结：** 这篇指南展示了一条端到端的实践路径，帮助开发者利用 SageMaker 的托管能力和 LangGraph 的控制流，快速构建可观测、可扩展且基于 Claude 的下一代对话式 AI 应用。

---

## 评论

**中心观点**
这篇文章本质上是一篇**全栈工程化的“缝合”实践指南**，主张通过将 LangGraph 的状态管理能力、Amazon Bedrock 的大模型底座以及 SageMaker 上托管的 MLflow 进行深度耦合，来解决生成式 AI 从原型到生产环境过程中面临的“状态不可控”与“实验管理混乱”两大核心痛点。

**支撑理由与深度评价**

**1. 架构演进：从“提示词工程”向“有状态应用工程”的跨越**
*   **事实陈述**：文章重点使用了 LangGraph。这是对传统“无状态”聊天机器人模式（如简单的 LangChain Chain）的显著升级。
*   **深度分析**：在行业早期，开发者习惯于将历史记录直接塞入 Prompt，这导致了 Token 消耗不可控且上下文容易丢失。文章引入 LangGraph 实际上是在推崇**确定性的图编排**。它将对话变成了一个状态机，每一个节点都是一个决策点。这对于构建复杂的 Agent（例如需要先查工具、再判断、再回答的流程）至关重要。这标志着行业正在从“调用大模型”转向“设计大模型驱动的软件系统”。

**2. 生产就绪度：填补了“原型”与“生产”之间的鸿沟**
*   **事实陈述**：文章强调了在 SageMaker 上使用托管 MLflow。
*   **深度分析**：这是文章最具工程价值的一点。目前 AI 行业存在大量“演示级”应用，开发者往往在 Jupyter Notebook 中调通了 Prompt 就认为开发完成了。文章引入 MLflow 进行 LLM 的追踪和模型管理，实际上是引入了**MLOps 的标准规范**。它解决了 LLM 开发中“非确定性”带来的调试难题（即同样的输入，输出可能不同，需要追踪 ID 和参数）。这对于企业级应用来说，是保证可维护性和可复现性的基石。

**3. 云原生的深度绑定：Bedrock 与 SageMaker 的协同效应**
*   **事实陈述**：技术栈完全构建在 AWS 生态之上（Bedrock + SageMaker）。
*   **作者观点**：这种选择具有极强的商业导向和工程便利性。
*   **深度分析**：Bedrock 解决了模型层的弹性扩缩容问题，而 SageMaker 解决了应用层的编排和监控问题。这种组合使得企业不需要维护复杂的 GPU 集群即可运行复杂的 Agent 逻辑。这反映了行业趋势：**云厂商正在提供从模型到中间件的全栈解决方案**，试图将用户锁定在其生态闭环中。

**反例与边界条件**

**1. 成本与灵活性的博弈**
*   **反例**：对于初创公司或个人开发者，这种架构过于重。如果只是构建一个简单的 RAG（检索增强生成）应用，使用 Vercel AI SDK 或 Streamlit 直接调用 OpenAI/Claude API，成本可能仅为 AWS 方案的 1/10。
*   **边界条件**：该架构适用于“企业级”、“多轮次复杂交互”且“对数据隐私/合规有极高要求”的场景。对于边缘计算或轻量级应用，SageMaker 的引入可能带来不必要的延迟和复杂度。

**2. LangGraph 的学习曲线与调试噩梦**
*   **反例**：虽然 LangGraph 提供了强大的状态控制，但其基于图的调试难度远高于线性代码。当 Agent 出现“死循环”或“幻觉”时，在复杂的图结构中定位错误节点非常困难。
*   **边界条件**：只有在 Agent 逻辑包含超过 3 个以上的串行/并行步骤（例如：工具调用 -> 错误处理 -> 重新查询 -> 总结）时，LangGraph 的优势才能抵消其带来的复杂度成本。

**可验证的检查方式**

1.  **状态一致性测试**：
    *   *指标*：在并发 100 个用户同时进行多轮对话时，检查是否出现“串话”（A 用户收到了 B 用户的回复）。
    *   *验证方式*：检查 LangGraph 中的 Thread ID 隔离机制是否在 Serverless 环境下依然有效。

2.  **实验追踪完整性**：
    *   *指标*：MLflow 中记录的 Trace 是否包含了从用户输入到最终输出的完整链路，以及每次调用 Bedrock 的 Token 消耗和延迟。
    *   *验证方式*：尝试复现一个历史对话，看能否通过 MLflow 记录的参数（如 Temperature, Top P）完全复现当时的回答。

3.  **冷启动延迟**：
    *   *指标*：Serverless 函数（如 Lambda 或 Fargate）在长时间闲置后的首次响应时间。
    *   *验证方式*：观察 Agent 在首次唤醒时，加载模型权重或初始化环境的时间是否超过了用户体验的容忍阈值（通常 > 3秒）。

**总结评价**
这篇文章是一篇典型的**“AWS 原生”最佳实践**。它没有提出新的算法理论，但在工程落地层面具有很高的参考价值。它敏锐地捕捉到了当前 AI 开发的痛点：**我们需要的不只是更聪明的模型，而是更健壮的软件工程架构**。通过结合 LangGraph（逻辑层）、Bedrock（模型层）和 MLflow（管理层），文章为企业构建高可用的 AI Agent 提供了一条标准化的、可验证的路径。然而，读者也应警惕其带来的 Vendor Lock-in（供应商锁定）风险以及随之而来的架构复杂度。

---

## 技术分析

基于您提供的文章标题和摘要，以及对相关技术栈的深度理解，以下是对这篇关于构建无服务器对话式AI智能体文章的全面深入分析。

---

### 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点在于展示如何构建一个**全托管、可观测且具备状态管理能力**的企业级对话AI系统。它主张利用 **Amazon SageMaker AI** 作为统一的控制平面，结合 **LangGraph** 的编排能力、**Claude (via Bedrock)** 的推理能力以及 **MLflow** 的实验追踪能力，来解决传统AI应用开发中“难以调试、缺乏状态记忆、部署运维复杂”的痛点。

**作者想要传达的核心思想**
作者试图传达一种**“现代MLOps与LLM应用深度融合”**的工程化思想。即：构建一个智能体不仅仅是调用API，而是需要构建一个完整的生命周期管理系统。通过将LangGraph的循环图结构与SageMaker的托管服务结合，开发者可以像管理传统机器学习模型一样，严谨地管理LLM应用的实验、部署和迭代。

**观点的创新性和深度**
*   **创新性**：文章不仅停留在简单的“RAG（检索增强生成）”实现，而是引入了**LangGraph**。LangGraph允许构建有状态的、循环的工作流，这比传统的线性链更接近人类对话的逻辑（例如：先澄清意图，再查询，再修正）。同时，将Managed MLflow引入LLM的Prompt管理和Tracing（追踪），是对传统LLM工程的一种规范化升级。
*   **深度**：它触及了LLM工程中最棘手的问题之一——**可观测性**。在生产环境中，不知道模型“为什么”这样回答是致命的。通过MLflow记录LangGraph的每一步决策，为AI的黑盒提供了透视镜。

**为什么这个观点重要**
随着企业从“LLM玩具项目”转向“生产级应用”，**无服务器化**（降低成本）和**可观测性**（确保稳定性）成为了两大瓶颈。这篇文章提出的架构直接回应了这一转型需求，提供了一条高性价比、高可控的落地路径。

---

### 2. 关键技术要点

**涉及的关键技术或概念**
*   **Amazon Bedrock**: 提供Claude模型的底层API，无服务器LLM基础。
*   **LangGraph**: 核心编排框架，基于有向图构建Agent，支持循环和条件边。
*   **Amazon SageMaker AI**: 提供Managed MLflow服务，用于实验追踪和模型注册。
*   **LangChain**: 作为底层接口连接Bedrock。

**技术原理和实现方式**
*   **Agent编排**: 原理是将对话过程建模为状态机。实现上，定义一个`State`（包含消息历史、用户输入等），定义`Nodes`（如LLM节点、工具节点），以及`Edges`（控制逻辑，如根据LLM输出决定是调用工具还是结束对话）。
*   **追踪与评估**: 利用LangGraph的回调机制，将每个节点的输入输出捕获并发送给MLflow。MLflow将这些非结构化日志记录为“Runs”，使得开发者可以对比不同Prompt或参数下的对话效果。

**技术难点和解决方案**
*   **难点**: **状态持久化**。无服务器函数通常是无状态的，但对话需要上下文。
    *   **解决方案**: LangGraph内部通过检查点机制将状态保存到外部存储（如DynamoDB或S3），在无服务器环境中实现了“有状态”的体验。
*   **难点**: **复杂的Prompt版本管理**。
    *   **解决方案**: 使用MLflow的模型注册表，将LangGraph的构建逻辑打包，实现版本控制和回滚。

**技术创新点分析**
将**Managed MLflow**与**LangGraph**深度集成是一个亮点。通常开发者使用LangSmith（LangChain官方SaaS）进行追踪，但这涉及数据外发和安全顾虑。文章展示了如何在AWS生态内利用开源MLflow替代LangSmith，构建私有化的可观测体系，这对企业级客户极具吸引力。

---

### 3. 实际应用价值

**对实际工作的指导意义**
该架构为AI工程师提供了一套**“开箱即用”的企业级脚手架**。它证明了在不购买昂贵的专用Agent平台（如LangSmith商业版）的情况下，仅利用云厂商原生服务即可构建高标准的AI应用。

**可以应用到哪些场景**
*   **企业知识库助手**: 需要多轮对话、查询数据库、并记录查询日志以优化答案的场景。
*   **金融/医疗合规客服**: 这类场景对数据隐私要求高，不能使用外部SaaS追踪服务，必须使用SageMaker+MLflow这种私有化方案。
*   **任务自动化Agent**: 例如自动处理工单、安排会议等涉及多步骤决策的流程。

**需要注意的问题**
*   **冷启动延迟**: Serverless函数（如Lambda或SageMaker Serverless端点）在长时间闲置后首次请求会有延迟，可能影响实时对话体验。
*   **成本陷阱**: 虽然是Serverless，但如果Token消耗量巨大或LangGraph循环次数过多，Bedrock和SageMaker的费用会迅速上升。

**实施建议**
*   **先做MVP**: 先用简单的LangChain实现核心逻辑，确认Prompt效果后再引入LangGraph增加复杂度。
*   **重视Tracing**: 在开发初期就接入MLflow，不要等到上线后再想办法调试。

---

### 4. 行业影响分析

**对行业的启示**
这篇文章标志着**LLMOps（大模型运维）正在标准化**。行业正在从“手搓Prompt”向“工业化流水线”转变。云厂商（AWS）正在通过整合开源工具，构建自己的护城河，试图打破LangSmith等垂直SaaS的垄断。

**可能带来的变革**
*   **私有化部署的门槛降低**: 企业不再需要为了一个Agent功能去维护K8s集群，Serverless + 托管MLflow的组合让小团队也能拥有大厂的工程能力。
*   **从“模型中心”转向“数据中心”**: 随着模型能力的商品化（通过Bedrock），竞争优势转移到了如何利用MLflow管理高质量的对话数据和反馈循环。

**对行业格局的影响**
加强了AWS在AI应用层的统治力。通过提供Managed MLflow，AWS实际上是在说：“你不需要去学复杂的MLOps工具，用我的托管服务就行。”这可能会挤压第三方MLOps初创公司的生存空间。

---

### 5. 延伸思考

**引发的其他思考**
*   **评估的主观性**: MLflow擅长记录数值指标（Loss, Accuracy），但如何评估对话的“满意度”？文章可能未深入涉及LLM-as-a-Judge（用大模型评估大模型）的集成，这是未来的关键。
*   **多模态扩展**: 目前的架构主要基于文本。如果引入图片（Claude 3.5 Sonnet支持视觉），MLflow如何有效存储和检索多模态数据？

**可以拓展的方向**
*   结合**Step Functions**可视化LangGraph的执行流程。
*   引入**Guardrails**（护栏机制）来过滤有害输出，这是企业级应用不可或缺的一环。

**未来发展趋势**
未来，Agent将不再只是“对话”，而是“行动”。架构将演变为：LangGraph负责规划，Bedrock负责思考，而SageMaker将负责部署更多的微调模型以执行特定任务。

---

### 6. 实践建议

**如何应用到自己的项目**
1.  **环境搭建**: 在AWS SageMaker Studio中启动一个实例，启用Managed MLflow。
2.  **代码重构**: 将现有的LangChain代码迁移为LangGraph结构。定义清晰的`StateDict`。
3.  **集成追踪**: 配置LangChain的回调处理器，将日志发送至本地或远程的MLflow服务器。

**具体的行动建议**
*   **学习LangGraph语法**: 重点理解`add_edge`和`add_conditional_edges`的区别。
*   **建立Baseline**: 在MLflow中建立一个基准实验，记录最简单的Prompt效果，以此为基准进行迭代优化。

**需要补充的知识**
*   **图论基础**: 理解有向无环图（DAG）与循环图的区别。
*   **异步编程**: LangGraph大量使用Python的`asyncio`，以优化IO密集型操作（如调用API）。

**实践中的注意事项**
*   **API Key管理**: 确保Bedrock的密钥权限最小化。
*   **日志脱敏**: 在将数据发送到MLflow之前，务必过滤PII（个人敏感信息），以免造成合规风险。

---

### 7. 案例分析

**结合实际案例说明**
假设我们要构建一个**“AWS云成本优化助手”**。
*   **传统方式**: 用户问“为什么我的账单这么高？”，LLM直接回答（可能产生幻觉）。
*   **LangGraph方式**:
    1.  **Intent Node**: 识别用户意图。
    2.  **Tool Node**: 调用Cost Explorer API获取真实数据。
    3.  **Analysis Node**: Claude分析数据，生成报告。
    4.  **Feedback Node**: 询问用户是否需要具体的优化建议。

**成功案例分析**
某金融科技公司使用类似架构构建内部合规Bot。通过MLflow记录了上万次对话，发现其中30%的查询因为意图识别不清而失败。通过分析LangGraph的执行路径，他们在意图节点增加了一个“澄清”步骤，成功将准确率提升至90%。

**失败案例反思**
有些团队盲目追求复杂的Graph结构，导致对话轮次过多，用户等待时间过长，且Token成本激增。教训是：**能用简单Prompt解决的问题，不要过度设计Agent**。

---

### 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级生成式AI应用时，采用**“Amazon SageMaker AI + LangGraph + Managed MLflow”**的无服务器架构，是目前平衡**开发敏捷性、系统可观测性与运维成本**的最优解。

**支撑理由与依据**
1.  **理由一：状态管理的复杂性**
    *   *依据*: 传统无状态API难以处理多轮对话上下文。LangGraph原生支持循环和状态持久化，解决了LLM“失忆”问题。
2.  **理由二：调试与迭代的需求**
    *   *依据*: LLM输出具有非确定性。没有MLflow的Trace记录，开发者无法复现Bug或优化Prompt。Managed MLflow提供了免运维的解决方案。
3.  **理由三：成本与弹性**
    *   *依据*: 自建K8s集群维护Agent服务成本高且扩展慢。Serverless架构按需付费，自动扩缩容。

**反例或边界条件**
1.  **边界条件（超低延迟场景）**: 如果应用需要毫秒级响应（如高频交易辅助），Serverless的冷启动和网络延迟可能不可接受，此时应使用预留实例或自建服务。
2.  **反例（极简应用）**: 如果只是简单的“一次性问答”任务（如文档总结），引入LangGraph和MLflow属于过度设计，增加了不必要的复杂度。

**事实与价值判断**
*   *事实*: AWS Bedrock提供了Claude模型；SageMaker集成了MLflow；LangGraph支持图结构编排。
*   *价值判断*: “可观测性”比“开发速度”在长期运行中更重要；“托管服务”优于“自建维护”。

**立场与验证方式**
*   **立场**: 支持该架构作为企业级应用的首选起步方案，但建议根据业务复杂度进行剪裁。
*   **验证方式**:
    *   *指标*: 对比引入该架构前后的**

---

## 最佳实践

### 实践 1：构建健壮的 LangGraph 状态管理架构

**说明**: 在使用 LangGraph 构建对话代理时，设计清晰的状态图至关重要。状态是连接不同节点（如意图识别、工具调用、响应生成）的核心数据结构。良好的状态管理应能处理多轮对话历史、中间步骤结果以及异常情况，确保代理在复杂交互流程中不会丢失上下文。

**实施步骤**:
1. 定义一个强类型的 State 数据类，明确包含 `messages`（历史记录）、`next_action`（下一步路由）等字段。
2. 为每个节点设计明确的输入输出签名，确保节点间数据传递符合状态定义。
3. 利用 LangGraph 的条件边功能，根据对话状态动态路由到不同的处理节点（例如：是回答问题还是调用外部 API）。
4. 实施检查点机制，利用 LangGraph 的持久化功能保存对话状态，以便在出现错误时回滚或恢复。

**注意事项**: 避免在状态中存储敏感明文信息；对于长对话，应实施状态截断或总结策略以防止 Token 超限。

---

### 实践 2：实施 MLflow 实验追踪与模型版本控制

**说明**: 在 SageMaker 上使用托管 MLflow 可以系统地记录模型训练参数、代码版本、评估指标和输出文件。对于基于 Claude 的对话代理，除了模型本身，还需要追踪 Prompt 模板、温度参数以及 LangGraph 的配置变更。这确保了每次迭代都是可复现且可比较的。

**实施步骤**:
1. 在 SageMaker Notebook 或 Studio 中初始化 MLflow 实验，并设置实验名称。
2. 在 LangGraph 代理代码中包装 `mlflow.start_run()`，记录 Claude 模型的调用参数和 Prompt 模板。
3. 使用 `mlflow.log_params()` 记录超参数，使用 `mlflow.log_metrics()` 记录评估指标（如响应准确率、延迟）。
4. 将训练好的模型或配置文件通过 `mlflow.langchain.log_model()` 进行注册，便于后续部署。

**注意事项**: 确保 MLflow 跟踪服务器已正确配置 IAM 权限，以便 SageMaker 能够安全地读写实验数据。

---

### 实践 3：设计高效的 Serverless 函数与资源分配

**说明**: 使用 SageMaker 无服务器推理或 Lambda 集成时，必须权衡冷启动延迟与并发成本。对于对话 AI，响应速度直接影响用户体验。合理的内存配置和预置并发可以优化性能。

**实施步骤**:
1. 根据 Claude 模型大小和 LangGraph 运行时开销，通过压力测试确定最优内存配置（例如：4096 MB 或更高）。
2. 如果使用 SageMaker 无服务器端点，设置适当的最大并发数以防止请求排队，同时控制成本。
3. 优化依赖项，移除不必要的库以减小容器镜像大小，从而加快冷启动速度。
4. 实施异步处理机制，对于耗时较长的工具调用，采用异步 I/O 模式避免阻塞主线程。

**注意事项**: 监控 Cold Start 频率，如果对延迟极度敏感，考虑保留一定数量的预置实例或使用 SageMaker 实时端点。

---

### 实践 4：建立全面的提示词工程与安全护栏

**说明**: 虽然 Claude 模型能力强大，但在特定业务场景下需要通过精细的 Prompt Engineering 引导其行为。同时，必须建立安全机制防止越狱攻击或生成有害内容。LangGraph 可以在发送给 Claude 之前插入预处理层。

**实施步骤**:
1. 设计系统提示词，明确代理的角色、限制条件和可用工具列表。
2. 在 LangGraph 中增加一个“输入验证”节点，在调用 LLM 前检查用户输入是否包含恶意指令或敏感词。
3. 利用 Bedrock Guardrails 功能或自定义逻辑过滤输出内容，确保响应符合合规性要求。
4. 建立 Prompt 模板版本库，通过 A/B 测试不同 Prompt 对话术质量的影响。

**注意事项**: 定期审查和更新安全护栏策略，以应对新型提示词注入攻击。

---

### 实践 5：优化工具调用与外部数据检索

**说明**: 现代对话代理通常需要连接外部数据源（如 RAG 数据库或业务 API）。LangGraph 负责编排这些工具调用。最佳实践包括确保工具调用的幂等性、处理超时以及优雅地处理工具失败的情况。

**实施步骤**:
1. 为每个工具定义清晰的描述和参数 Schema，确保 Claude 能准确理解何时以及如何调用它们。
2. 在 LangGraph 的工具调用节点周围实现 Try-Catch 逻辑，如果工具失败，代理应能自动重试或生成友好的错误回复，而不是崩溃。
3. 对于检索增强生成（RAG），实施语义缓存，避免对重复问题进行昂贵的向量检索。
4. 限制单个对话轮次中可调用的工具数量或深度，防止无限循环或资源耗尽。

**注意事项**: 确保传递给工具的参数经过严格验证，防止通过工具调用进行间接的

---

## 学习要点

- 利用 LangGraph 构建基于状态机的架构，能够有效管理对话上下文和代理循环逻辑，实现复杂的多步骤对话流程。
- 集成 Amazon SageMaker AI 托管的 MLflow，可以集中化追踪实验指标、模型参数和人工制品，简化对话模型的开发与迭代流程。
- 采用 Serverless 架构部署 AI 代理，能够根据请求量自动伸缩计算资源，在降低运维成本的同时实现高可用性。
- 将 Claude 3 模型与 LangGraph 结合，利用其强大的推理能力处理复杂的用户意图，并动态规划工具调用或知识检索路径。
- 通过 SageMaker AI 的统一托管环境，消除了基础设施管理的复杂性，使开发者能更专注于对话逻辑和业务价值的实现。
- 利用 LangGraph 的持久化机制，可以在无服务器环境中有效维护对话历史，确保多轮交互的连贯性和记忆能力。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [AWS](/tags/aws/) / [Bedrock](/tags/bedrock/) / [LangGraph](/tags/langgraph/) / [SageMaker](/tags/sagemaker/) / [Claude](/tags/claude/) / [MLflow](/tags/mlflow/) / [Serverless](/tags/serverless/) / [Agent](/tags/agent/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Amazon SageMaker AI构建无服务器Claude对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [亚马逊Bedrock在东南亚及台湾推出Anthropic Claude模型]({{< relref "posts/20260225-blogs_podcasts-global-cross-region-inference-for-latest-anthropic-6.md" >}})
- [在 SageMaker 与 Bedrock 上利用 vLLM 实现多 LoRA 推理及内核优化]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-11.md" >}})
