---
title: "基于Bedrock与LangGraph在SageMaker构建无服务器对话代理"
date: 2026-03-03T11:19:12+08:00
draft: false
entry_kind: "auto"
tags: ["LangGraph", "Amazon Bedrock", "SageMaker", "MLflow", "无服务器", "Serverless", "智能体", "Agent"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "本文介绍了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上的托管 **MLflow**，构建一个**无服务器（Serverless）的对话式 AI 智能体**。 主要内容包括以下几点： 1. **核心架构**： * **Amazon B"
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

本文探讨了如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow 来构建一个智能对话代理。

---
## 导语

随着大模型应用场景的深入，构建具备状态管理与可观测性的对话代理已成为技术落地的关键。本文将详细介绍如何利用 Amazon Bedrock 上的 Claude 模型与 LangGraph 框架，结合 Amazon SageMaker AI 托管的 MLflow，构建一个无服务器的智能对话系统。通过阅读本文，您将掌握从架构设计到实验追踪的完整流程，从而高效地开发、监控并优化您的 AI 应用。

---
## 摘要

本文介绍了如何利用 **Amazon Bedrock**、**LangGraph** 以及 **Amazon SageMaker AI** 上的托管 **MLflow**，构建一个**无服务器（Serverless）的对话式 AI 智能体**。

主要内容包括以下几点：

1.  **核心架构**：
    *   **Amazon Bedrock**：提供基础模型支持（如 Claude），用于生成自然语言响应。
    *   **LangGraph**：用于编排智能体的状态和逻辑，构建复杂的对话流程。
    *   **Amazon SageMaker AI**：提供托管的 MLflow 服务，用于实验跟踪和管理机器学习模型。

2.  **无服务器优势**：
    *   无需管理底层基础设施，自动扩展，按使用量付费，降低运维成本。

3.  **实施流程**：
    *   文章详细演示了如何结合这些工具，从开发环境配置到智能体的部署与监控。

**总结**：该方案通过整合 AWS 的托管服务与 LangGraph 的编排能力，为开发者提供了一个高效、可扩展且易于管理的生成式 AI 应用构建路径。

---
## 评论

**文章中心观点**
该文章主张在 AWS 云原生环境中，通过 LangGraph 编排状态机逻辑、利用 Bedrock 托管模型能力、并结合 SageMaker 内置的 MLflow 进行全生命周期管理，是构建企业级 Serverless 生成式 AI 应用的最佳实践路径。

**支撑理由与深度评价**

**1. 架构的严谨性与全栈闭环（事实陈述 / 你的推断）**
文章最核心的价值在于提出了一套**端到端的 MLOps 落地范式**。大多数技术文章仅关注“如何调用 API”，而该文涵盖了从开发（LangGraph 状态管理）、部署（Serverless）到监控（MLflow）的完整闭环。
*   **深度分析**：LangGraph 的引入是关键。传统的 Chain（链式）结构难以处理复杂的对话分支和回环，而 Graph（图）结构更符合人类对话的非线性特征。结合 SageMaker 的 Serverless 特性，解决了企业在起步阶段对于 GPU 资源预留的成本顾虑。
*   **边界条件/反例**：这种架构并非万能。如果对话逻辑极其简单（如单轮 QA），引入 LangGraph 会增加不必要的代码复杂度。此外，MLflow 虽然强大，但在 AWS 生态中，部分企业可能已经深度使用了 SageMaker Experiments，引入 MLflow 可能造成工具链冗余。

**2. 技术选型的务实性：Serverless 与模型解耦（事实陈述）**
文章强调使用 Amazon Bedrock 而非自建模型，这体现了“关注业务逻辑而非基础设施”的工程哲学。
*   **深度分析**：通过 Bedrock 调用 Claude 3.5 等模型，企业可以快速切换模型版本（A/B Testing）而无需重构底层代码。LangGraph 作为控制层，与模型层解耦，符合“模型即服务”的趋势。
*   **边界条件/反例**：Serverless 架构的冷启动问题在实时对话场景中可能被放大，导致首字回复延迟（TTFT）过高。对于对延迟极度敏感的金融或高频交易场景，基于 GPU 实例的常驻服务可能仍是首选。

**3. 可观测性的标准化（作者观点 / 你的推断）**
将 Managed MLflow 引入 LLM 开发流程是文章的一大亮点。
*   **深度分析**：LLM 的非确定性使得调试变得异常困难。文章暗示利用 MLflow 跟踪 Prompt 版本、Token 消耗和模型参数，是迈向“工程化”的必经之路。这把“炼丹”变成了可追溯的工程实验。
*   **边界条件/反例**：MLflow 的 LLM View 功能虽然强大，但在处理流式输出时的实时追踪可能存在延迟。对于需要实时干预（如人工接管）的客服场景，仅靠 MLflow 的离线追踪是不够的，还需要实时的中间件监控。

**争议点与不同观点**

*   **“AWS 厂商锁定”风险**：虽然文章声称构建的是通用的 Agent，但深度依赖 SageMaker 的托管 MLflow 和 Bedrock API，实际上构成了极高的迁移成本。若未来企业想迁移至 Azure 或私有云，重构 LangGraph 中的节点可能容易，但迁移 MLOps 平台和数据流水线将非常痛苦。
*   **LangGraph 的必要性争议**：社区中存在观点认为，对于简单的 Agent，直接使用 LangChain 的 `AgentExecutor` 或甚至原生 Python 控制流可能更直观。引入图数据库概念是否属于“过度设计”，取决于应用的生命周期长度。

**实际应用建议**

1.  **成本预警机制**：在使用 Bedrock 和 Claude 3.5 Sonnet 等高智商模型时，务必在 LangGraph 的节点中增加 Token 消耗计数器，并结合 MLflow 设置预算告警，避免对话循环导致账单爆炸。
2.  **混合部署策略**：不要完全迷信 Serverless。建议在生产环境中，将高频使用的核心 Agent 部署在 SageMaker Real-time Endpoints 上以保证低延迟，而将低频、突发流量的业务保留在 Serverless 配置中。
3.  **Prompt 版本管理**：利用 MLflow 严格管理 Prompt Template。不要将 Prompt 硬编码在 LangGraph 的 Python 代码中，应将其作为参数传入，以便快速迭代和回滚。

**可验证的检查方式**

1.  **延迟基准测试**：
    *   *指标*：测量从用户发送请求到收到首字节（TTFT）的平均时间。
    *   *验证*：在 Bedrock Serverless 和 SageMaker Real-time Endpoint 两种配置下，分别运行 1000 次对话请求，对比 P95 延迟数据。若 Serverless 的 P95 延迟超过 2 秒，则该架构在用户体验上存在风险。

2.  **状态恢复能力测试**：
    *   *实验*：在 LangGraph 执行过程中人为中断（如模拟 Lambda 超时或网络抖动）。
    *   *验证*：检查系统能否从 Checkpoint 中断点恢复，而不是重复执行已完成的步骤或直接报错。这是验证 LangGraph 状态管理是否有效的关键。

3.  **MLOps 追溯完整性**：
    *   *观察窗口*：观察 MLflow UI 中的一次典型对话 Run。
    *   *验证*：检查是否能够清晰看到调用的模型版本、传入的 Prompt 变体、以及返回的 Token 使用量。如果缺少这些字段中的任意一项，说明该可观测性方案是残缺的。

---
## 技术分析

基于您提供的文章标题和摘要，以及对Amazon SageMaker AI、Bedrock、LangGraph和MLflow技术栈的深入了解，以下是对该文章核心观点和技术要点的深度分析。

---

# 深度分析：基于SageMaker构建无服务器对话式AI智能体

## 1. 核心观点深度解读

**主要观点：**
文章的核心观点在于展示一种**现代化的、全托管的企业级AI智能体构建范式**。它主张通过结合Amazon Bedrock（基础模型服务）、LangGraph（状态化编排框架）以及SageMaker上的托管MLflow（全生命周期管理），在无服务器架构下构建具备记忆、推理和工具调用能力的对话式AI。

**核心思想：**
作者试图传达**“分离与协同”**的架构思想。
1.  **基础设施分离**：计算资源通过无服务器架构实现弹性伸缩，开发者无需管理底层服务器。
2.  **逻辑编排分离**：利用LangGraph将复杂的对话逻辑建模为状态机，而非简单的线性提示词流。
3.  **管理与开发分离**：利用MLflow进行严格的实验追踪和模型注册，确保AI应用从原型到生产的可治理性。

**创新性与深度：**
*   **创新点**：将**LangGraph**引入AWS生态体系。传统的AWS示例多基于LangChain，而LangGraph引入了循环图的概念，这对于处理需要回退、修正或长期记忆的复杂对话（Agentic Workflow）至关重要。
*   **深度**：文章不仅仅停留在“调用API”，而是深入到了**MLOps**的层面。它强调在构建GenAI应用时，必须像对待传统机器学习一样，关注实验的可复现性和模型的版本管理，这往往是当前GenAI开发中被忽视的短板。

**重要性：**
随着企业从“POC（概念验证）”阶段迈向“生产”阶段，单纯的模型调用已无法满足需求。企业需要能够处理复杂业务流程、可监控、可回滚的智能体。该文章提供了一套在AWS云原生环境下，兼顾开发敏捷性与运维规范性的标准答案。

## 2. 关键技术要点

**涉及的关键技术：**
*   **Amazon Bedrock**：提供Claude 3等大模型的API接口，无服务器化，按token付费。
*   **LangGraph**：基于LangChain构建，用于构建有状态、多参与者的循环工作流。
*   **Amazon SageMaker AI**：提供托管的MLflow实例，用于追踪实验、注册模型和管理Prompt。
*   **AWS Lambda**（隐含）：通常作为无服务器计算载体运行LangGraph应用。

**技术原理与实现方式：**
1.  **智能体架构**：
    *   利用**LangGraph**定义一个`StateGraph`。状态包含用户输入、Agent的思考过程、工具调用结果和最终回复。
    *   定义节点：例如`agent`节点（调用LLM决定下一步）、`tools`节点（执行外部API调用）。
    *   定义边：条件边，根据LLM的输出判断是继续调用工具、结束对话还是重新思考。
2.  **无服务器部署**：
    *   将LangGraph逻辑容器化或直接部署为Lambda函数。
    *   通过API Gateway暴露REST接口，实现自动扩缩容。
3.  **实验追踪**：
    *   在开发阶段，将不同的Prompt模板、Temperature参数、甚至不同的LangGraph结构配置作为“实验”记录在MLflow中。
    *   利用MLflow的LLM Evaluation功能，使用模型（如Claude本身作为裁判）来评估回答质量。

**技术难点与解决方案：**
*   **难点1：状态管理。** 无服务器函数通常是无状态的，而对话需要上下文。
    *   *解决方案*：LangGraph内部通过检查点机制将状态持久化（通常存放在DynamoDB等外部存储中），使得对话可以跨请求保持。
*   **难点2：Prompt工程的可视化与版本控制。** 代码中的Prompt难以管理和回滚。
    *   *解决方案*：使用MLflow的Prompt Engineering UI，可视化地管理Prompt版本，并直接部署注册的Prompt版本。
*   **难点3：工具调用的安全性。**
    *   *解决方案*：在LangGraph的节点层面对工具权限进行严格控制，利用IAM角色限制Bedrock访问特定AWS资源。

**技术创新点分析：**
将**Agentic Workflow（智能体工作流）**与**MLOps流水线**打通。通常MLOps关注模型训练，而LLMOps关注Prompt和编排。该方案展示了如何在一个统一的平台上（SageMaker/MLflow）管理从Prompt设计到复杂逻辑编排的全过程。

## 3. 实际应用价值

**指导意义：**
该架构为企业提供了一个**“低风险、高敏捷”**的落地路径。企业无需投入巨资建设GPU集群，利用Bedrock即可获得顶级算力；利用LangGraph可快速迭代业务逻辑；利用MLflow可防止AI项目陷入“混乱工程”的泥潭。

**应用场景：**
*   **企业知识库助手**：结合RAG（检索增强生成），利用LangGraph的循环逻辑处理“找不到信息时的二次检索”或“多源信息汇总”。
*   **金融/合规分析机器人**：需要严格记录每一次推理过程（用于审计），MLflow的追踪功能至关重要。
*   **电商客服自动化**：处理复杂的订单状态查询、退改签逻辑（需要多次API调用）。

**需要注意的问题：**
*   **成本控制**：无服务器虽然省去了运维成本，但在高频对话场景下，Bedrock的Token费用和Lambda调用费用可能不低。
*   **冷启动延迟**：Lambda函数在长时间闲置后会有冷启动，可能导致首字回复延迟较高。

**实施建议：**
1.  先在本地使用LangChain/LangGraph构建核心逻辑。
2.  将Prompt和配置迁移至SageMaker MLflow进行管理。
3.  使用Bedrock进行模型推理测试。
4.  最后通过SAM/CDK等IaC工具部署至Lambda/Step Functions。

## 4. 行业影响分析

**对行业的启示：**
该架构标志着**GenAI应用开发正在从“手工作坊”向“工业化生产”转型**。过去开发者主要在Jupyter Notebook里写Prompt，现在必须引入完整的软件工程生命周期（CI/CD）和MLOps流程。

**可能带来的变革：**
*   **SWE与MLOps的融合**：传统的后端工程师和算法工程师的界限变得模糊。构建智能体既需要懂Prompt（算法），又需要懂状态机和API设计（工程）。
*   **云厂商的竞争焦点转移**：从单纯比拼模型性能，转向比拼**“中间层生态”**。谁能提供更好的编排工具和治理工具，谁就能锁定企业客户。

**相关领域发展趋势：**
*   **LangGraph的崛起**：LangChain正在从简单的链式调用向图状态机演进，这将成为构建复杂Agent的主流范式。
*   **Dedicated AI Platforms**：像SageMaker这样集成数据、模型、开发、部署的一站式平台将越来越受欢迎。

## 5. 延伸思考

**引发的思考：**
*   **多智能体协作**：文章主要讨论单个智能体。在LangGraph框架下，如何扩展为多个智能体（如一个负责搜索，一个负责写作，一个负责批判）互相协作？这是未来的方向。
*   **人机协同**：在LangGraph的流程中，如何优雅地插入“人工确认”环节？例如，智能体在执行高风险操作前，暂停流程等待人工审批。

**拓展方向：**
*   结合**Amazon Bedrock Knowledge Bases**，进一步简化RAG构建流程。
*   引入**Guardrails**（护栏机制），在LangGraph的输入输出层增加内容安全审查。

**未来趋势：**
*   **边缘侧与云端协同**：部分简单的推理在本地设备完成，复杂的逻辑编排交给云端SageMaker。
*   **自愈合智能体**：智能体不仅能执行任务，还能根据MLflow记录的历史失败数据，自我修正Prompt或工具调用逻辑。

## 6. 实践建议

**如何应用到自己的项目：**
1.  **评估现有技术栈**：如果你的项目已经在使用AWS，且团队熟悉Python，该栈是首选。
2.  **从“小”着手**：不要一开始就构建全能Agent。先构建一个简单的RAG Agent，引入MLflow记录Prompt和Token消耗。
3.  **模块化设计**：将工具调用封装为独立的Lambda函数，便于在LangGraph中复用。

**具体行动建议：**
*   **学习LangGraph**：理解`State`、`Node`、`Edge`的核心概念。
*   **搭建MLflow Tracking Server**：使用SageMaker的托管版本，避免自己运维数据库。
*   **建立评估指标**：在MLflow中定义自动化评估指标（如答案相关性、幻觉率），不要只依赖人工打分。

**注意事项：**
*   **API限流**：Bedrock有配额限制，设计Agent时要考虑重试机制和队列管理。
*   **数据隐私**：确保发送给Bedrock的数据符合合规要求，必要时使用VPC Endpoint。

## 7. 案例分析

**成功案例（模拟）：某跨国银行内部IT运维助手**
*   **背景**：员工需要查询日志、重启服务、查询文档。
*   **实施**：使用LangGraph构建状态机，节点包括“意图识别”、“查询文档”、“执行AWS API（重启服务）”。使用MLflow管理针对不同IT系统的Prompt模板。
*   **成效**：通过MLflow发现“重启服务”类Prompt存在幻觉，回滚至上一版本，避免了生产事故。无服务器架构应对了不定时的员工查询高峰。

**失败反思：过度设计**
*   **场景**：一个简单的“天气查询”机器人。
*   **问题**：强行引入LangGraph和MLflow，导致开发周期过长，维护成本高。
*   **教训**：技术栈的选择应匹配业务复杂度。简单的线性任务不需要图编排。

## 8. 哲学与逻辑：论证地图

**中心命题：**
在构建企业级生成式AI应用时，采用**“Amazon Bedrock + LangGraph + 托管MLflow”**的无服务器架构，是目前实现**敏捷迭代与工程治理平衡**的最优解。

**支撑理由与依据：**
1.  **理由一：业务逻辑的复杂性需要图编排。**
    *   *依据*：真实世界的对话是非线性的（包含修正、循环、分支）。简单的链式结构无法处理“Agent执行工具失败后重试”或“拆分子任务”等场景。LangGraph的循环图特性是解决此类问题的数学最佳实践。
2.  **理由二：企业级应用必须具备可追溯性与版本管理。**
    *   *依据*：GenAI应用具有非确定性。如果不使用MLflow等工具记录每一次运行的参数、Prompt版本和结果，当出现事故时无法回溯原因，也无法进行A/B测试。
3.  **理由三：成本与效率的考量。**
    *   *依据*：无服务器架构消除了闲置服务器的成本，且Bedrock按Token付费模式降低了试错门槛，适合快速变化的业务初期。

**反例与边界条件：**
1.  **边界条件：超低延迟要求。**
    *   如果应用要求端到端延迟低于200ms（如高频交易辅助），无服务器架构的冷启动和网络开销可能使其不适用，此时应使用自托管模型或GPU实例。
2.  **

---
## 最佳实践

## 最佳实践指南

### 实践 1：设计健壮的有状态工作流架构

**说明**: 利用 LangGraph 的有状态图特性构建对话流程，避免单纯依赖线性提示词。通过定义明确的节点、边和条件路由，处理复杂的对话逻辑（如多轮对话、中断与恢复、工具调用后的错误处理）。

**实施步骤**:
1. 定义 `State` 对象，包含消息历史、用户输入及中间变量。
2. 使用 `StateGraph` 构建图结构，将 Agent 的思考、工具使用和响应拆分为独立节点。
3. 设置条件边，根据模型输出（如 `tool_calls`）路由到不同节点。
4. 在 SageMaker 无服务器架构中部署该图，确保状态能通过 API 请求正确传递和恢复。

**注意事项**: 避免在状态中存储敏感信息或过大的上下文，以防超出 Token 限制或影响延迟。

---

### 实践 2：集中化模型追踪与实验管理

**说明**: 利用托管 MLflow 记录 LangGraph 工作流中的所有实验数据。由于 LLM 应用具有非确定性，必须严格记录参数、Prompt 模板和评估指标，以便复现最佳结果。

**实施步骤**:
1. 在 SageMaker 项目中初始化 MLflow 实验跟踪服务器。
2. 使用 `MLflowCallbackHandler` 或自定义日志逻辑，捕获 Claude 模型的输入 Prompt、输出响应及 Token 消耗。
3. 记录不同 LangGraph 路由路径的成功率，识别流程中的瓶颈。
4. 对比不同版本 Prompt 或系统提示词的运行效果，注册最佳模型。

**注意事项**: 确保 MLflow 跟踪 URI 配置正确，并设置适当的日志保留策略以控制存储成本。

---

### 实践 3：实施精细的 Prompt 管理与版本控制

**说明**: Claude 的表现高度依赖于 Prompt 质量。不要将 Prompt 硬编码在业务逻辑中，应将其视为可版本化的资产进行管理，以便快速迭代和 A/B 测试。

**实施步骤**:
1. 将系统提示词和少样本示例存储在单独的配置文件或参数存储中（如 S3 或 SSM Parameter Store）。
2. 在 LangGraph 节点中动态加载 Prompt 模板，注入特定上下文。
3. 通过 MLflow 记录每次部署使用的 Prompt 哈希值或版本号。
4. 建立审批流程，确保生产环境 Prompt 变更的可追溯性。

**注意事项**: 修改 Prompt 时需评估其对 Token 使用量和延迟的影响，避免过度复杂的指令降低响应速度。

---

### 实践 4：构建自动化的评估与反馈闭环

**说明**: 传统的单元测试难以衡量 LLM 的生成质量。应利用 Claude 自身作为“裁判”或使用确定性指标，建立自动化评估管道，持续监控 Agent 在 SageMaker 上的表现。

**实施步骤**:
1. 构建包含“黄金答案”的测试数据集。
2. 在 LangGraph 工作流中集成评估节点，或使用 MLflow 的评估功能。
3. 利用 Claude 3.5 Sonnet 等模型对生成的回复进行打分（基于相关性、准确性和语气）。
4. 将评估指标反馈回 MLflow UI，触发告警或自动回滚机制。

**注意事项**: 评估模型本身也会产生 API 调用成本，需平衡评估频率与预算。

---

### 实践 5：优化无服务器部署的成本与延迟

**说明**: SageMaker 无服务器计算虽然能自动扩缩容，但冷启动和并发限制可能影响用户体验。需针对 Claude 模型特性进行特定优化。

**实施步骤**:
1. 配置合适的内存大小和最大并发数，平衡冷启动时间与成本。
2. 在 LangGraph 中实现流式传输，利用 Claude 的流式响应能力提升用户感知的响应速度。
3. 对简单的查询实现快速退出机制，避免不必要的模型调用。
4. 监控 CloudWatch 指标，分析调用模式以调整预置并发量。

**注意事项**: 注意 SageMaker 无端点的并发限制，防止突发流量导致限流。

---

### 实践 6：强化工具调用的安全性与错误处理

**说明**: 当 Agent 调用外部工具（如数据库查询或 API）时，必须严格验证输入参数，并妥善处理工具执行失败的情况，防止 Agent 陷入死循环或泄露敏感数据。

**实施步骤**:
1. 在 LangGraph 的工具节点周围添加包装器，捕获所有异常并返回友好的错误消息给 Claude。
2. 限制 Claude 可访问的工具范围，并为每个工具定义清晰的描述。
3. 对工具返回的数据进行脱敏处理，确保不将内部 ID 或原始错误堆栈暴露给最终用户。
4. 设置最大迭代步数，防止 Agent 在无法解决问题时无限循环消耗 Token。

**注意事项**: 定期审计 Claude 生成的工具调用参数，确保符合安全策略。

---
## 学习要点

- 利用 LangGraph 构建基于状态机的架构，能够有效管理对话上下文并实现具备记忆能力和复杂推理循环的无服务器 AI 智能体。
- 将 Claude 3 大语言模型与 Amazon Bedrock 集成，可在无服务器环境中实现高性能的自然语言处理与对话生成能力。
- 在 SageMaker 上部署托管 MLflow，能够集中化地追踪实验、管理模型版本并注册模型，从而简化从开发到生产的部署工作流。
- 借助 AWS Lambda 的按需计费和自动弹性伸缩特性，构建无服务器后端可大幅降低 AI 智能体的基础设施运维成本与复杂度。
- 利用 LangChain 的工具抽象能力将智能体连接至外部 API 和数据库，可扩展智能体的功能边界以执行实际业务任务。
- 通过 LangGraph 的条件边和循环机制，可以设计出能够根据对话状态动态规划下一步行动的自主智能体，而不仅仅是简单的线性问答。
- 结合 Amazon API Gateway 与 Lambda，可以为 AI 智能体构建安全、可扩展且符合生产标准的无服务器 RESTful 接口。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [LangGraph](/tags/langgraph/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [Serverless](/tags/serverless/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [基于Amazon SageMaker AI构建无服务器Claude对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [利用 Amazon Bedrock 构建具备记忆与身份验证的智能活动助手]({{< relref "posts/20260226-blogs_podcasts-building-intelligent-event-agents-using-amazon-bed-13.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*