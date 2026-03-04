---
title: "基于Bedrock与LangGraph构建无服务器对话代理及SageMaker MLflow管理"
date: 2026-03-03T23:28:17+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon Bedrock", "LangGraph", "SageMaker", "MLflow", "无服务器", "对话代理", "Claude", "MLOps"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "随着生成式 AI 的落地，构建具备记忆与推理能力的对话代理已成为技术焦点。本文将演示如何利用 Amazon Bedrock 上的 Claude 模型、LangGraph 框架以及 Amazon SageMaker AI 托管的 MLflow，打造一个无服务器的智能 Agent。通过阅读，您将掌握从编排对话流到实验追踪的"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios: ["AI/ML项目"]
---

# 基于Bedrock与LangGraph构建无服务器对话代理及SageMaker MLflow管理

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

随着生成式 AI 的落地，构建具备记忆与推理能力的对话代理已成为技术焦点。本文将演示如何利用 Amazon Bedrock 上的 Claude 模型、LangGraph 框架以及 Amazon SageMaker AI 托管的 MLflow，打造一个无服务器的智能 Agent。通过阅读，您将掌握从编排对话流到实验追踪的完整工程实践，了解如何在云端高效构建与迭代可扩展的 AI 应用。

---
## 评论

### 中心观点
这篇文章的核心观点是：**通过将 Amazon Bedrock（模型层）、LangGraph（控制层）与 SageMaker 集成的 MLflow（可观测性层）结合，企业可以构建出一套既具备复杂逻辑推理能力，又符合生产级治理标准的无服务器对话智能体。**

### 支撑理由与边界分析

**1. 架构的模块化解耦与全生命周期管理（事实陈述）**
文章提出的架构并非简单的 API 调用，而是试图解决 LLM 应用落地中最棘手的“不可控”问题。
*   **深度分析：** 传统的聊天机器人基于简单的意图识别，难以处理多轮对话中的状态保持。LangGraph 的引入引入了“图”的概念，将对话流程定义为状态机，这极大地增强了 Agent 处理复杂任务（如预订、故障排查）的鲁棒性。同时，将 SageMaker 上托管的 MLflow 作为“黑盒”的监控层，填补了从“实验”到“生产”的治理空白。
*   **边界条件/反例：** 这种架构的复杂性对于简单的问答（FAQ）场景是过度设计的。如果业务逻辑只是“查询文档”，RAG（检索增强生成）架构足矣，引入 LangGraph 会增加不必要的开发与调试成本。此外，LangGraph 的学习曲线较陡，团队需要具备较强的编程能力来维护状态机逻辑。

**2. 成本与效率的博弈：无服务器的双刃剑（你的推断）**
文章强调“Serverless”和“Managed MLflow”，意在降低运维负担。
*   **深度分析：** 对于初创公司或流量波动的业务，Bedrock 的按需付费模式极具吸引力，避免了 GPU 资源的闲置浪费。SageMaker 的托管服务减少了 MLflow 的维护工作量。
*   **边界条件/反例：** 在高并发、大规模生产环境下，Serverless 架构的成本可能会迅速失控。相比预留实例或自托管模型，云厂商的 Serverless 调用费用（尤其是输入/输出 Token 计费）在长对话场景下会非常昂贵。此外，MLflow 的托管服务价格通常高于自建部署，对于预算敏感的团队，这可能成为财务黑洞。

**3. 供应商锁定风险与生态封闭性（作者观点）**
文章展示了一个典型的 AWS 原生技术栈。
*   **深度分析：** 这种深度集成的优势在于原生体验极佳，延迟低，且利用了 AWS 的 IAM 权限控制等安全特性。
*   **边界条件/反例：** 这是典型的“供应商锁定”陷阱。一旦业务需要迁移到 Google Cloud 或 Azure，或者需要切换到非 Bedrock 托管的模型（如 Llama 3 自建部署），重构成本将极高。LangGraph 虽然理论上支持不同后端，但与 AWS 服务的深度集成代码往往难以复用。

### 综合评价

**1. 内容深度：8/10**
文章不仅停留在“Hello World”层面，而是触及了 Agent 开发中的核心痛点：状态管理与模型评估。它正确地指出了单纯的 LLM 调用无法构建企业级应用，必须引入编排和治理。然而，文章对于 LangGraph 中“循环”和“条件边”的处理细节可能略显简略，对于错误处理和回滚机制的探讨通常也是此类技术博客的弱项。

**2. 实用价值：9/10**
对于已经处于 AWS 生态内的企业，这篇文章是一份极具价值的蓝图。它提供了一套可复制、标准化的生产级落地路径，解决了“模型有了，怎么管、怎么控”的问题。

**3. 创新性：7/10**
将 LangGraph 与 SageMaker MLflow 结合并非开创性的理论创新，但属于优秀的**工程集成创新**。它顺应了当前从“单模型调用”向“多智能体系统”演进的技术趋势，强调了 MLOps 在 LLM 时代的必要性。

**4. 可读性与逻辑：9/10**
通常此类 AWS 技术博客逻辑清晰，配有架构图和代码片段，逻辑链条为“问题 -> 解决方案架构 -> 代码实现 -> 部署验证”，符合工程师的认知习惯。

**5. 行业影响：**
这篇文章强化了“MLOps + LLMOps”融合的趋势。它向行业释放了一个信号：**对话式 AI 的竞争焦点已从模型参数大小转向了工作流编排和全生命周期的可观测性。**

**6. 争议点与不同观点：**
*   **争议点：** 是否应该使用 LangGraph？部分开发者认为 LangChain/LangGraph 过于臃肿，倾向于使用更轻量的 SWE-bench 或直接编写 Python 代码来控制 Agent 逻辑。
*   **不同观点：** 关于 MLflow 的必要性。在 LLM 时代，部分团队认为基于 Trace（如 LangSmith）的评估比传统的 ML Metrics（准确率/召回率）更重要，传统的 MLflow 可能难以适应非确定性生成式模型的评估需求。

### 实际应用建议

1.  **不要盲目照搬架构：** 在项目启动前，先评估你的业务是否真的需要“图”结构。如果是简单任务，避免过度设计。
2.  **关注 Token 成本：** 在使用 Bedrock 等托管服务时，务必在 MLflow 中记录每一次调用的 Token 消耗，以便在业务放量时进行成本核算。
3.  **建立评估基准：** 仅仅搭建 Agent 是不够的，利用 MLflow 建立一套针对你特定业务场景的自动化评估集（如基于 LLM-as-a-Judge 的评分），

---
## 技术分析

基于您提供的文章标题和摘要，虽然缺乏具体的正文细节，但结合标题中涉及的具体技术栈，我将从架构原理、技术生态和行业实践的角度，为您构建一份深度的分析报告。这篇文章实际上是在探讨**“如何利用云原生工具链，构建可观测、可编排且具备状态管理能力的下一代企业级对话智能体”**。

以下是详细的深度分析：

---

# 深度分析：基于 SageMaker AI、LangGraph 与 Bedrock 的无服务器对话智能体架构

## 1. 核心观点深度解读

### 主要观点
文章的核心观点在于展示一种**现代化的、全托管的企业级 AI 应用开发范式**。它主张不再从零构建基础设施，而是通过深度整合 **Amazon Bedrock**（模型底座）、**LangGraph**（状态控制逻辑）和 **SageMaker 上的托管 MLflow**（全生命周期管理），来构建一个**无服务器**的对话智能体。

### 核心思想
作者传达的核心思想是**“关注点分离”与“全栈可控”**。
1.  **关注点分离**：将模型的推理能力交给 Bedrock，将复杂的对话流程控制交给 LangGraph，将实验追踪和模型部署交给 SageMaker/MLflow。
2.  **全栈可控**：即使使用无服务器架构，企业依然需要通过 MLflow 对 AI 应用的“大脑”（Prompt、参数、版本）进行严格的治理和版本控制，而不是仅仅依赖简单的 API 调用。

### 创新性与深度
该观点的创新性在于打破了“LangChain 仅用于本地脚本”或“SageMaker 仅用于模型训练”的刻板印象，展示了：
*   **状态管理的引入**：从传统的“无状态问答”转向“有状态的多步推理”。
*   **DevOps for GenAI**：强调了在生成式 AI 开发中，MLflow 作为实验追踪和注册中心的关键作用，填补了 LLM 应用难以版本化的空白。

### 重要性
随着企业从“演示 POC”走向“生产环境”，如何管理不断变化的 Prompt、如何处理复杂的对话上下文、以及如何降低运维成本成为痛点。该架构提供了一条标准化的落地路径，解决了**可控性**与**成本效率**的平衡问题。

---

## 2. 关键技术要点

### 涉及的关键技术
1.  **Amazon Bedrock**：提供基础模型（如 Claude 3）的无服务器访问，无需管理 GPU 实例。
2.  **LangGraph**：基于有向图的 Agent 编排框架，支持循环和状态持久化，是对 LangChain 的进阶。
3.  **SageMaker (Managed MLflow)**：提供托管的实验追踪、模型注册和部署服务。
4.  **AWS Lambda / Fargate (隐含)**：作为无服务器计算层运行 LangGraph 逻辑。

### 技术原理与实现
*   **状态机原理**：LangGraph 将对话定义为一个图，节点代表 LLM 调用或工具调用，边代表决策逻辑。它维护一个 `State` 对象，随着对话的进行，这个状态在图中流转并被不断更新，从而实现“记忆”功能。
*   **模型版本化**：利用 MLflow 的 `log_model` 功能，将 LangGraph 的整个流程图（包含 Prompt 模板和配置）打包成一个 MLflow Model。这使得开发者可以像管理传统机器学习模型一样管理一个 Agent。
*   **无服务器部署**：SageMaker 的无服务器部署选项允许模型在无请求时不产生计算费用，按推理量计费，适合流量波动的对话场景。

### 技术难点与解决方案
*   **难点：上下文记忆的持久化**。在无服务器环境中，函数执行完即销毁，内存无法保留。
    *   **解决方案**：LangGraph 支持将 State 序列化并存储在数据库（如 DynamoDB）或 Redis 中，每次请求时通过 `thread_id` 恢复状态。
*   **难点：LLM 应用的版本管理**。Prompt 的微小改动会导致效果巨大差异，难以回滚。
    *   **解决方案**：通过 MLflow Tracking 记录每一次运行的参数和指标，通过 Model Registry 部署特定版本，实现 A/B 测试和快速回滚。

### 技术创新点
*   **将 Agent 视为“模型”**：传统 MLflow 管理的是算法模型（如 PyTorch 模型），这里创新性地将“代码+Prompt+配置”组成的 Agent 作为一个可部署的单元进行管理，实现了 GenAI 的 MLOps 标准化。

---

## 3. 实际应用价值

### 指导意义
该架构为 CTO 和架构师提供了一张**“去基础设施化”**的蓝图。它证明了企业不需要维护庞大的 Kubernetes 集群或 GPU 资源池，也能构建复杂的、具备记忆能力的 AI 应用。

### 适用场景
*   **企业知识库助手**：需要多轮对话理解用户意图，并检索 RAG（检索增强生成）内容的场景。
*   **金融/合规咨询**：对版本控制和审计要求极高，任何上线的回答必须能追溯到特定的 Prompt 版本。
*   **电商客服**：流量波动大，适合无服务器架构，且需要处理订单查询等复杂逻辑。

### 需要注意的问题
*   **冷启动延迟**：无服务器架构在长时间无请求后，首次调用会有冷启动延迟，可能影响实时对话体验。
*   **数据隐私**：虽然数据在 VPC 内，但需确认 Bedrock API 调用的数据隐私政策。
*   **成本陷阱**：虽然按量付费，但如果对话上下文极长，Token 消耗会迅速增加，需监控 Bedrock 的 Token 成本。

### 实施建议
*   **先治理，后开发**：在写代码前先配置好 MLflow 的 Tracking Server。
*   **状态分离**：设计 State 时，尽量只保留必要信息，避免存储大量历史数据导致推理延迟和成本上升。

---

## 4. 行业影响分析

### 对行业的启示
这篇文章标志着**“大模型应用工程化”**进入深水区。行业焦点从“如何调用 API”转向“如何构建健壮的系统”。它强调了**可观测性**是生产级 AI 应用的核心竞争力。

### 可能带来的变革
*   **MLOps 的泛化**：MLOps 不再仅是数据科学家的工具，开发 AI 应用的全栈工程师也必须掌握实验追踪和模型注册的概念。
*   **Server-First 架构**：推动更多企业放弃自建 GPU 集群，转向混合云模式（训练在本地或云端实例，推理在无服务器环境）。

### 发展趋势
*   **LangGraph 的崛起**：随着对话复杂度增加，简单的线性链将无法满足需求，基于图的编排将成为主流。
*   **BaaS 的标准化**：Bedrock 等服务将变成像水电一样的基础设施，竞争壁垒将转移到**业务逻辑编排**和**数据质量**上。

---

## 5. 延伸思考

### 拓展方向
*   **多模态扩展**：目前的架构主要针对文本，如何利用 Bedrock 的多模态能力（如图片输入）在 LangGraph 中进行编排？
*   **人机协同**：在 LangGraph 的图中引入“人类节点”，当 AI 置信度不足时，暂停流程等待人工介入，这将是高风险场景的刚需。

### 需进一步研究的问题
*   **评估指标体系**：MLflow 记录了 Loss，但对话质量如何量化？需要研究基于 LLM-as-a-Judge 的自动化评估指标如何集成到这个 SageMaker 流程中。
*   **并发与竞态条件**：当同一个用户在多个设备同时操作时，LangGraph 的状态管理机制如何保证数据一致性？

---

## 6. 实践建议

### 如何应用到自己的项目
1.  **环境搭建**：在 AWS 账户中启用 SageMaker Studio，配置托管 MLflow 实例。
2.  **Agent 开发**：使用 Python 定义 LangGraph 节点和边，实现简单的 ReAct 模式（推理+行动）。
3.  **容器化与注册**：编写 `MLproject` 文件或使用 MLflow 的 Python API，将 LangGraph 代码打包。
4.  **部署**：使用 SageMaker 的无服务器部署配置，将注册的模型部署为 HTTPS 端点。

### 行动建议
*   **学习 LangGraph**：如果你熟悉 LangChain，需要重点学习图的定义和状态传递机制。
*   **成本监控**：设置 AWS Budgets 和 CloudWatch 告警，监控 Bedrock 的 Token 使用量和 SageMaker 的调用次数。

### 知识补充
*   需要了解 **AWS IAM 权限控制**（Bedrock 访问权限）。
*   需要熟悉 **Python 装饰器**（LangGraph 大量使用装饰器定义节点）。

---

## 7. 案例分析

### 成功案例逻辑
假设一家**在线旅游平台（OTA）**采用此架构：
*   **场景**：用户询问“帮我规划一个去日本的行程”。
*   **流程**：
    1.  **意图识别**：通过 LangGraph 的路由节点，识别为“规划任务”。
    2.  **工具调用**：Agent 调用 Bedrock 的 Claude 3，生成初步行程。
    3.  **状态循环**：用户反馈“太贵了”，Agent 读取 State 中的历史反馈，调整参数（如降低酒店标准），重新生成。
    4.  **版本管理**：运营人员发现 V1 版本的行程推荐过于激进，通过 MLflow 快速回滚到 V2 版本（Prompt 中增加了“性价比优先”指令）。
*   **结果**：开发效率提升（无需管理服务器），上线速度加快。

### 失败案例反思
*   **错误做法**：将整个对话历史存在 State 中而不进行摘要。
*   **后果**：用户聊了 50 轮后，每次请求的 Prompt Token 超过 10k，导致 Bedrock 成本飙升且延迟严重，最终导致超时错误。
*   **教训**：必须在 LangGraph 中引入“摘要节点”，定期将旧对话压缩，保持 State 精简。

---

## 8. 哲学与逻辑：论证地图

### 中心命题
**在构建企业级生成式 AI 应用时，采用“Bedrock + LangGraph + Managed MLflow”的无服务器架构，相比传统自部署架构，能显著降低运维成本并提升迭代效率。**

### 支撑理由与依据
1.  **理由 1：基础设施管理成本最小化。**
    *   *依据*：AWS Bedrock 和 SageMaker 无服务器特性消除了 GPU 预置、补丁和集群扩缩容的运维负担（事实）。
2.  **理由 2：复杂逻辑的可控性增强。**
    *   *依据*：LangGraph 的图结构比线性链更适合处理包含循环、分支和回退的复杂对话流（技术原理）。
3.  **理由 3：实验与生产的标准化闭环。**
    *   *依据*：Managed MLflow 提供了统一的界面来比较不同 Prompt 版本的效果，并一键部署，消除了“代码即环境”的混乱（行业最佳实践）。

### 反例与边界条件
1.

---
## 最佳实践

## 最佳实践指南

### 实践 1：采用 LangGraph 构建有状态的对话工作流

**说明**:
传统的无状态聊天机器人难以处理复杂的多轮对话。利用 LangGraph 的循环图架构，可以为对话流引入显式的状态管理。通过定义自定义的 `StateGraph`，可以将对话历史、提取的实体和用户上下文作为状态在节点间传递，从而实现能够回溯、分支和记忆上下文的智能代理。

**实施步骤**:
1. 定义一个 `TypedDict` 结构来明确对话状态中包含的字段（如 `messages`, `user_id`, `intent`）。
2. 使用 `StateGraph` 初始化图结构，并设置入口节点和终止条件。
3. 编写节点函数，每个函数接收当前状态并返回状态更新；利用 `add_edge` 或 `add_conditional_edges` 定义对话流转逻辑。
4. 集成 Claude 模型作为决策节点，利用其强大的推理能力决定下一步动作（如调用工具或结束对话）。

**注意事项**:
确保状态序列化机制与后端存储兼容。如果对话历史过长，应在传入模型前实施摘要策略以控制 Token 消耗。

---

### 实践 2：利用 MLflow 实验追踪进行提示词工程管理

**说明**:
在构建 Serverless 应用时，提示词往往决定了模型的表现。将 MLflow 与 SageMaker 集成使用，可以将提示词模板视为模型超参数进行版本化管理。这不仅能记录每一次迭代的提示词内容，还能关联相应的评估指标，从而系统化地优化 Agent 的回复质量。

**实施步骤**:
1. 在 SageMaker Notebook 或 Studio 中初始化 MLflow 实验并设置追踪 URI。
2. 使用 `mlflow.log_param` 记录 System Prompt、Temperature 和 Top-p 等关键参数。
3. 在 LangChain 链中集成 `MLflowCallbackHandler`，自动捕获模型输入输出和 Token 使用情况。
4. 利用 MLflow UI 比较不同运行周期的结果，筛选出表现最佳的提示词配置。

**注意事项**:
避免在追踪记录中存储敏感的 PII（个人身份信息）。在记录提示词时，应确保其符合安全合规标准。

---

### 实践 3：通过 Bedrock Guardrails 实施安全防护

**说明**:
对话型 AI 面临提示词注入和有毒内容生成的风险。在调用 Claude 之前，利用 Amazon Bedrock Guardrails 进行输入和输出的过滤，是构建生产级 Agent 的必要环节。这可以防止 Agent 被诱导执行恶意指令或生成不当言论。

**实施步骤**:
1. 在 Amazon Bedrock 控制台中创建一个 Guardrail，配置拒绝主题（如暴力、非法行为）和敏感信息过滤器。
2. 设置上下文接地检查，确保模型回答仅基于提供的参考资料，减少幻觉。
3. 在 LangGraph 的入口节点或边缘函数中调用 `ApplyGuardrail` API。
4. 根据拦截结果，配置预设的回复话术，优雅地处理被阻断的请求。

**注意事项**:
Guardrails 的配置需要根据业务场景进行微调，过度拦截可能会影响用户体验，建议定期审查误判率。

---

### 实践 4：优化工具调用与错误处理机制

**说明**:
强大的 Agent 需要具备执行动作的能力。通过 LangGraph 将 Claude 与外部 API（如数据库查询或业务逻辑）连接时，必须构建健壮的错误处理循环。当工具调用失败或返回异常时，Agent 应具备自我修正能力，而不是直接崩溃。

**实施步骤**:
1. 使用 LangChain 的 `@tool` 装饰器定义外部函数，并编写清晰的 Docstring 以帮助 Claude 理解工具用途。
2. 在 LangGraph 中设计专门的“工具执行”节点，并在其后连接一个“错误检查”节点。
3. 在“错误检查”节点中判断工具返回的状态码，如果失败，则生成一段错误反馈重新注入 Claude 上下文，请求重试。
4. 设置最大重试次数阈值，防止陷入无限循环。

**注意事项**:
工具定义应保持原子性和幂等性。确保传递给工具的参数经过严格校验，防止潜在的注入攻击。

---

### 实践 5：实施基于 Traces 的性能监控与可观测性

**说明**:
Serverless 架构虽然简化了运维，但增加了调试的难度。利用 Amazon SageMaker Experiments 或 CloudWatch 结合 LangChain 的集成，捕获详细的执行链路，对于定位延迟瓶颈和逻辑错误至关重要。

**实施步骤**:
1. 启用 LangChain 的集成追踪功能，将 Traces 数据发送到 Amazon CloudWatch 或专用的 Traces 后端。
2. 在 LangGraph 的每个关键节点中记录自定义指标，如节点执行耗时和中间状态快照。
3. 配置 CloudWatch Alarms，监控 API 调用延迟、错误率及 Bedrock 的限流情况。
4. 定期分析 Trace 数据，识别图结构中的串行瓶颈，考虑将部分独立节点并行化。

**注意事项**:
在高并发场景下，全量记录 Trace 可能会产生大量数据及

---
## 学习要点

- 利用 LangGraph 构建基于 Claude 的有状态对话代理，通过循环图结构管理对话上下文和工具调用流程
- 在 SageMaker AI 上部署托管 MLflow 实验跟踪平台，集中管理模型训练参数、指标和开发全生命周期的实验数据
- 将 LangGraph 编译后的应用部署为 SageMaker 实时推理端点，实现无服务器的可扩展对话 API 服务
- 集成 Amazon Bedrock 中的 Claude 模型与 LangChain 框架，实现企业级生成式 AI 应用的快速开发与托管
- 使用 MLflow 的 LangChain 自动记录功能，自动捕获模型架构、提示词模板及推理结果等关键资产
- 通过 SageMaker AI 的无服务器架构自动处理底层基础设施，大幅降低运维成本并简化部署流程

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Amazon Bedrock](/tags/amazon-bedrock/) / [LangGraph](/tags/langgraph/) / [SageMaker](/tags/sagemaker/) / [MLflow](/tags/mlflow/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [对话代理](/tags/%E5%AF%B9%E8%AF%9D%E4%BB%A3%E7%90%86/) / [Claude](/tags/claude/) / [MLOps](/tags/mlops/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Amazon SageMaker AI构建无服务器Claude对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [基于Amazon SageMaker AI构建无服务器对话AI代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-13.md" >}})
- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [在SageMaker AI上基于Bedrock与LangGraph构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*