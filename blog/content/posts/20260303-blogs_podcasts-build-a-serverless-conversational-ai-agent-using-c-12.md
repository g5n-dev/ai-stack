---
title: "基于 Bedrock 与 LangGraph 在 SageMaker AI 构建无服务器对话代理"
date: 2026-03-03T21:58:18+08:00
draft: false
entry_kind: "auto"
tags: ["LangGraph", "Amazon Bedrock", "SageMaker AI", "MLflow", "对话代理", "无服务器", "Agent", "AWS Lambda"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "**基于 Amazon SageMaker AI、Claude 和 LangGraph 构建无服务器对话式 AI 智能体** 本文详细介绍了如何利用 Amazon Bedrock、LangGraph 以及托管在 Amazon SageMaker AI 上的 MLflow，构建一个无服务器架构的智能对话代理（Agent）"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai
scenarios: ["AI/ML项目"]
---

# 基于 Bedrock 与 LangGraph 在 SageMaker AI 构建无服务器对话代理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-02T18:51:43+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)

---
## 摘要/简介

本文将探讨如何利用 Amazon Bedrock、LangGraph 以及 Amazon SageMaker AI 上托管的 MLflow 来构建一个智能对话代理。

---
## 导语

随着生成式 AI 技术的深入应用，构建具备记忆与上下文理解能力的对话代理已成为企业智能化转型的关键一环。本文将介绍如何结合 Amazon Bedrock 上的 Claude 模型、LangGraph 框架以及托管在 Amazon SageMaker AI 上的 MLflow，从零开始构建一个无服务器架构的智能对话系统。通过阅读本文，您将掌握从模型编排到实验追踪的完整技术路径，学会在云端高效搭建可扩展、可观测的 AI 应用。

---
## 摘要

**基于 Amazon SageMaker AI、Claude 和 LangGraph 构建无服务器对话式 AI 智能体**

本文详细介绍了如何利用 Amazon Bedrock、LangGraph 以及托管在 Amazon SageMaker AI 上的 MLflow，构建一个无服务器架构的智能对话代理（Agent）。

### 1. 核心架构与组件
该解决方案结合了以下关键技术：
*   **Amazon Bedrock:** 提供强大的基础模型支持（本例中主要使用 Claude 3），用于生成自然语言回复。
*   **LangGraph:** 用于编排代理的工作流。它允许定义状态图，控制 Agent 的决策逻辑（例如：是直接回答还是调用工具）。
*   **Amazon SageMaker AI:** 提供托管的 MLflow 服务，用于集中管理实验、追踪模型指标和版本，以及存储模型制品。
*   **AWS Lambda:** 用于托管 LangGraph 代码，实现无服务器计算。

### 2. 构建流程
文章主要分为以下几个步骤：
1.  **初始化环境:** 创建 SageMaker 域名并启用托管 MLflow 应用程序。
2.  **模型选择与配置:** 在 Amazon Bedrock 中启用 Claude 模型。
3.  **定义 Agent 逻辑:** 使用 Python 和 LangGraph 定义 Agent 的结构，包括系统提示词、工具绑定（如搜索功能）以及状态流转逻辑。
4.  **部署与集成:** 将 LangGraph 应用程序容器化，并部署到 AWS Lambda。配置 API Gateway 作为前端入口，接收用户请求并触发 Lambda 函数。

### 3. 关键功能：MLflow 集成
这是一个重要的差异化功能。通过将 LangGraph 与 MLflow 集成，开发者可以实现：
*   **Prompt 追踪:** 自动记录 Agent 运行时的 Prompt 和响应，方便调试。
*   **实验管理:** 在 MLflow UI 中可视化 Agent 的执行轨迹和中间步骤。
*   **版本控制:** 对 Agent 的配置和逻辑进行版本管理。

### 4. 优势总结
*   **无服务器:** 利用 AWS Lambda 和 API Gateway，无需管理服务器，可实现自动伸缩，按需付费。
*   **可观测性:** 借助 SageMaker 上的托管 MLflow，弥补了传统无服务器应用难以追踪和调试的短板。
*   **灵活性:** LangGraph 使得构建复杂的多步骤对话代理变得

---
## 评论

**文章中心观点**
本文主张在 AWS 云原生环境中，通过 LangGraph 编排状态机逻辑、利用 Amazon Bedrock 提供基础模型能力、并借助 SageMaker 集成的 MLflow 进行全生命周期管理，是构建企业级 Serverless 对话 AI Agent 的最佳实践路径。

**深入评价与支撑理由**

**1. 内容深度：从“玩具级”Demo向“生产级”架构的跨越**
*   **支撑理由（事实陈述）：** 文章没有止步于简单的 API 调用，而是引入了 **LangGraph** 这一关键组件。相比于简单的链式调用，LangGraph 引入了“有状态”和“循环”的概念，这是构建复杂 Agent（如需要多步推理、自我修正或工具调用的智能体）的必要条件。
*   **支撑理由（作者观点）：** 将 **MLflow** 引入 SageMaker 是文章的一大亮点。大多数 GenAI 教程只关注“如何运行”，忽略了“如何迭代和追踪”。在 LLM 应用中，Prompt 版本管理和参数追踪是痛点，文章将 SageMaker 的托管能力与 MLflow 结合，填补了从原型到生产部署之间的“工程化鸿沟”。
*   **反例/边界条件（你的推断）：** 这种架构的深度主要局限在 AWS 生态圈内。如果企业采用多云策略，或者需要极致的低延迟（边缘计算），这种重度依赖云端托管服务的架构可能会面临厂商锁定或网络延迟的问题。

**2. 实用价值：Serverless 的权衡与成本陷阱**
*   **支撑理由（事实陈述）：** 利用 Bedrock 和 SageMaker 的 Serverless 特性，确实降低了运维基础设施的门槛，开发者无需管理 GPU 集群即可快速上线服务。
*   **支撑理由（你的推断）：** 对于初创公司或 PoC（概念验证）阶段，该方案具有极高的实用价值，能够以最快速度验证产品想法。
*   **反例/边界条件（事实陈述）：** **成本陷阱**是明显的边界条件。Serverless 适合间歇性流量，但对于高并发、大规模流量的生产环境，按 Token 请求数和计算时长的计费模式可能远高于预留实例。此外，Bedrock 的数据出境合规性（如中国区开发者无法直接使用）限制了其在特定区域的实用价值。

**3. 行业影响：定义了“云厂商+开源框架”的标准范式**
*   **支撑理由（作者观点）：** 这篇文章反映了当前 AI 行业的“分工明确”趋势：云厂商（AWS）负责算力和基座模型，开源框架负责逻辑编排，MLOps 工具负责管理。这种“三明治”架构正在成为企业构建 AI 应用的主流范式。
*   **支撑理由（事实陈述）：** AWS 强调 SageMaker 的“统一平台”属性，试图将数据科学家（用 Notebook）和工程师（用 CI/CD）的工作流收敛在一个平台上，这对推动 MLOps 落地有正面影响。
*   **反例/边界条件（你的推断）：** 随着 Hugging Face TGI 或 vLLM 等推理框架的兴起，越来越多的企业开始选择“自托管”高性能推理，以获得比 Serverless 更高的吞吐量和更低的成本。这可能会削弱 Bedrock 等 Serverless 服务的长期吸引力。

**争议点与不同观点**

1.  **编排框架的选型之争：** 文章选定 LangGraph 作为编排层，但这并非唯一解。目前 **LangChain** 的生态更成熟，而 **AutoGen** 或 **CrewAI** 在多智能体协作上表现更优。LangGraph 的学习曲线较陡峭，且其状态机逻辑在处理极其复杂的非线性对话时，可能会变得难以维护。
2.  **MLflow 的必要性：** 虽然文章推崇 MLflow，但在 LLM 开发中，**Weights & Biases (WandB)** 或 **PromptLayer** 往往提供了更针对 GenAI 的可视化评估工具。MLflow 虽然全面，但在 LLM Trace（链路追踪）的易用性上，有时不如专门针对 LLM 的工具轻量。

**实际应用建议**

1.  **架构解耦：** 在实际采用该方案时，建议使用接口抽象层隔离 Bedrock。这样未来如果需要切换到 Azure OpenAI 或本地部署的 Llama 3，无需重写核心业务逻辑。
2.  **监控先行：** 不要只依赖 MLflow 的模型记录，务必在生产环境中配置 AWS CloudWatch 或 X-Ray，专门监控 Bedrock 的调用延迟和 Token 消耗，以防止意外的高额账单。
3.  **评估闭环：** 利用 MLflow 的 Evaluation 功能建立“黄金数据集”。不要依赖人工测试，而是建立自动化的评估流水线，确保 LangGraph 的逻辑修改不会引入回归错误。

**可验证的检查方式**

1.  **延迟基准测试（指标）：** 构建一个包含 5 轮对话和 2 次工具调用的测试用例，测量从用户输入到 Agent 返回首字的端到端延迟（E2E Latency）。对比 Serverless 架构与自托管推理框架的延迟差异。
2.  **成本波动观察（观察窗口）：** 在一个月的周期内，记录不同流量波峰波谷时段的 Bedrock + SageMaker 账单。计算单次对话的平均成本，验证在流量低谷期 Serverless 是否真的比预留实例省钱。
3.  **状态恢复测试（实验）：** 模拟 LangGraph 执行过程中途 Bedrock API 超时的场景，验证 Agent 的状态机是否能够正确回滚

---
## 技术分析

基于文章标题《Build a serverless conversational AI agent using Claude with LangGraph and managed MLflow on Amazon SageMaker AI》及摘要内容，以下是对该技术方案的深度全面分析。

---

# 构建下一代无服务器对话智能体的深度技术分析

## 1. 核心观点深度解读

**主要观点**
文章的核心观点在于提出一种**全托管、模块化且可观测的**现代 AI 智能体构建范式。作者主张通过结合 Amazon Bedrock（基础模型服务）、LangGraph（状态机编排框架）以及 SageMaker 上的托管 MLflow（全生命周期管理），来解决构建复杂对话 AI 时面临的**基础设施复杂性**与**模型迭代不可控性**两大痛点。

**核心思想**
作者传达的核心思想是“**关注业务逻辑，而非基础设施**”。在生成式 AI 从简单的“聊天机器人”向能够执行复杂任务的“智能体”演进的过程中，开发者面临的最大挑战不再是模型本身的能力，而是如何管理多轮对话的状态、记忆以及如何持续优化模型性能。通过将无服务器架构与工业级 MLOps 相结合，可以实现高性能与低成本、快速迭代之间的平衡。

**创新性与深度**
该观点的创新性在于**技术栈的深度融合**：
1.  **架构演进**：从简单的 API 调用转向基于 LangGraph 的**有状态循环计算图**，这代表了从“单次预测”到“多步推理”的架构升级。
2.  **Ops 融合**：将 SageMaker 的算力优势与 MLflow 的管理优势深度结合，打破了“实验环境”与“生产环境”的隔阂，实现了真正的**MLOps 自动化闭环**。
3.  **无服务器落地**：将智能体逻辑部署在无服务器架构上，解决了传统 AI 部署中资源利用率低、扩缩容不灵活的难题。

**重要性**
这一观点至关重要，因为它为企业级 AI 落地提供了一套**“开箱即用”的最佳实践**。它不仅解决了技术实现的可行性，更解决了模型在生产环境中“黑盒化”的问题，使得 AI 智能体不仅能跑起来，还能被持续监控和优化，直接降低了企业拥抱 GenAI 的试错成本。

## 2. 关键技术要点

**涉及的关键技术**
1.  **Amazon Bedrock**：提供 Claude 3 等基础大模型的 API 接口，实现无服务器的模型推理。
2.  **LangGraph**：基于 LangChain 的扩展，专门用于构建有状态、多参与者的循环应用流程。
3.  **Amazon SageMaker**：提供托管的 MLflow 实例，用于实验跟踪和模型注册。
4.  **AWS Lambda**（隐含）：通常用于无服务器架构中执行具体的业务逻辑代码。

**技术原理与实现方式**
*   **智能体编排**：利用 LangGraph 定义“图”结构，节点代表 LLM 调用或工具调用，边代表状态流转逻辑。通过显式定义状态，解决了 LLM 幻觉和上下文记忆丢失的问题。
*   **无服务器计算**：通过 Bedrock 的 Serverless 模式，无需预留 EC2 实例即可按 Token 付费；后端逻辑通过 API Gateway + Lambda 处理，实现毫秒级冷启动和自动弹性伸缩。
*   **MLOps 集成**：
    *   **实验跟踪**：在 LangGraph 执行过程中，将 Prompt、模型参数（如 temperature, max_tokens）、中间状态和最终结果自动记录至 SageMaker 托管的 MLflow。
    *   **模型注册**：将经过验证的 Prompt 模板或 Agent 配置注册为模型版本，实现灰度发布和回滚。

**技术难点与解决方案**
*   **难点**：LangGraph 的循环执行在无服务器环境中可能导致超时或状态管理复杂。
*   **方案**：利用 AWS Step Functions 或 LangGraph 的持久化机制，将对话状态存储在 DynamoDB 等数据库中，实现“中断后恢复”。
*   **难点**：LLM 输出的非确定性导致难以评估。
*   **方案**：利用 MLflow 记录每次调用的输入输出，建立基于 LLM-as-a-Judge 的自动化评估流水线。

**技术创新点分析**
最大的创新点在于**将 Agent 的“逻辑代码”视为“模型”进行管理**。传统 MLOps 关注权重文件，而此方案关注的是 Prompt 模板、Chain 结构和工具定义。这标志着 MLOps 从“模型中心”向“应用中心”的范式转移。

## 3. 实际应用价值

**对实际工作的指导意义**
该架构为 AI 工程师提供了一个**标准化的企业级脚手架**。它指导开发者如何从“写 Demo”转向“做产品”，特别是强调了可观测性和版本控制的重要性。

**应用场景**
1.  **企业级知识库问答**：需要高并发、低延迟且需持续优化回答准确率的场景。
2.  **个性化销售助手**：需要根据对话历史动态调整策略，并记录不同策略的转化率。
3.  **代码生成或数据分析助手**：涉及多步推理（如生成代码->执行->修正->再生成），LangGraph 的状态管理能力在此至关重要。

**需要注意的问题**
*   **成本控制**：无服务器虽省去了运维成本，但在高并发流量下，Bedrock 的 Token 调用费用可能很高。
*   **冷启动延迟**：无服务器架构在长时间闲置后首次请求可能有较高延迟。
*   **数据隐私**：需确认数据传输至 Bedrock 和 MLflow 的合规性。

**实施建议**
*   **起步阶段**：先使用 LangChain 快速验证逻辑，再迁移至 LangGraph 以增强状态控制。
*   **监控先行**：在开发第一天就接入 MLflow，不要等到上线后再补监控。
*   **Prompt 版本化**：将 Prompt 视为代码，通过 MLflow 进行严格的版本管理。

## 4. 行业影响分析

**对行业的启示**
该方案预示着 **“AI 工程化”** 时代的正式到来。行业焦点从“谁的模型参数大”转向“谁的模型运维更稳、迭代更快”。云厂商（如 AWS）正在构建从模型层到应用层的全栈护城河。

**可能带来的变革**
*   **DevOps 与 MLOps 的融合**：未来的 AI 开发将不再区分算法工程师和后端工程师，而是趋向于全栈 AI 工程师。
*   **SaaS 模式的升级**：软件将具备更强的对话和推理能力，从“GUI 交互”转向“LUI（自然语言交互）”。

**发展趋势**
*   **BaaS 蓬勃发展**：更多针对 Agent 的后端服务（如专门的向量数据库、Agent 编排服务）将涌现。
*   **标准化评估体系**：基于 MLflow 等工具，行业将建立起针对 Agent 性能而非单纯模型性能的评估标准。

## 5. 延伸思考

**引发的思考**
*   **Agent 的安全性**：当 Agent 拥有工具调用权限时，如何防止其执行恶意操作？LangGraph 如何与权限控制系统结合？
*   **多模态扩展**：当前的架构主要基于文本，如何平滑扩展到图像或音频处理？

**拓展方向**
*   结合 **RAG (检索增强生成)**：将企业私有数据通过向量数据库接入 LangGraph 的节点中。
*   **人机协同**：在 LangGraph 中引入“人工确认”节点，处理高风险决策。

**未来研究问题**
*   如何在 LangGraph 中实现自动化的“错误自愈”机制？
*   如何量化评估一个“图结构”的优劣，而不仅仅是评估 LLM 的输出？

## 6. 实践建议

**如何应用到自己的项目**
1.  **环境搭建**：注册 AWS 账号，开通 SageMaker、Bedrock 和 Lambda 服务。
2.  **依赖安装**：安装 `langgraph`, `mlflow`, `boto3` 等库。
3.  **定义状态**：使用 `TypedDict` 定义你的 Agent 在对话过程中需要传递的数据结构。

**具体行动建议**
*   **阅读官方文档**：深入研究 LangGraph 的 `StateGraph` 用法。
*   **建立基线**：先不使用 MLflow，跑通一个简单的 Bedrock 调用。
*   **集成 MLflow**：编写一个简单的 Wrapper，将 Prompt 和 Response 记录到 MLflow 实验中。

**需补充的知识**
*   **Python 异步编程**：LangGraph 大量使用 async/await 模式以提高并发性能。
*   **AWS 基础架构知识**：理解 IAM 权限、VPC 网络配置。
*   **图论基础**：理解节点、边、有向图的概念有助于设计 Agent 流程。

**注意事项**
*   **API Key 管理**：切勿将 AWS Access Key 硬编码在代码中，应使用 IAM Role。
*   **Token 限制**：注意 Claude 模型的 Context Window 限制，避免对话历史过长导致截断。

## 7. 案例分析

**成功案例逻辑推演**
假设某电商公司构建**“智能售后客服 Agent”**：
*   **背景**：原有客服机器人基于规则，无法处理复杂问题。
*   **实施**：使用 Claude 3 理解用户意图，LangGraph 编排“查询订单”、“退款”、“转人工”等节点。SageMaker MLflow 记录每次交互的满意度。
*   **成效**：通过 MLflow 分析发现“退款”节点的 Prompt 导致用户反复询问，工程师调整 Prompt 并通过 A/B 测试验证，成功将退款处理时长缩短 40%。

**失败案例反思**
*   **场景**：某初创公司直接将复杂的 Agent 逻辑部署在 Lambda 上。
*   **问题**：LangGraph 的循环逻辑导致 Lambda 执行时间超过 15 分钟上限，且未配置正确的状态持久化。
*   **教训**：无服务器架构有严格的运行时间限制，对于长链路 Agent，必须采用 Step Functions 或将状态外置存储，不能仅依赖内存。

## 8. 哲学与逻辑：论证地图

**中心命题**
在构建企业级生成式 AI 应用时，采用 **"Amazon Bedrock + LangGraph + SageMaker MLflow"** 的**无服务器全托管架构**，是实现**开发效率**、**运行成本**与**系统可维护性**三者最优平衡的**最佳技术选型**。

**支撑理由与依据**
1.  **理由 1：开发效率最大化**
    *   *依据*：LangGraph 提供了直观的图抽象，比纯代码更易于管理复杂的多轮对话状态；Bedrock 免去了模型微调的基础设施搭建时间。
2.  **理由 2：运维成本极小化**
    *   *依据*：无服务器架构按量付费，消除了闲置资源的浪费；托管服务免去了底层 K8s/OS 的维护负担。
3.  **理由 3：模型迭代科学化**
    *   *依据*：MLflow 提供了标准化的实验追踪，使得 Prompt Engineering 从“玄学”变为“数据驱动的科学实验”，确保持续优化。

**反例或边界条件**
1.  **边界条件 1（超低延迟要求）**：如果业务要求延迟在 50ms 以内（如高频交易辅助），Bedrock 的网络延迟和 LangGraph 的编排开销可能无法接受，此时需考虑自

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建健壮的 LangGraph 状态管理机制

**说明**:
在构建对话式 AI 代理时，LangGraph 的核心在于状态图的设计。最佳实践要求明确定义状态模式，确保在多轮对话中能够正确传递上下文、历史记录和中间结果。对于复杂代理，应使用 TypedDict 定义清晰的数据结构，避免状态污染或数据丢失。

**实施步骤**:
1. 使用 Python 的 `TypedDict` 定义 Agent 的状态结构，包含 `messages`、`user_input` 和 `intermediate_steps` 等字段。
2. 在图的节点设计函数中，确保每个节点只更新它负责的状态字段，而不是覆盖整个状态。
3. 利用 LangGraph 的持久化功能，配置检查点以保存对话历史，实现无服务器环境下的会话恢复。

**注意事项**:
避免在全局状态中存储敏感的 PII（个人身份信息）或过大的上下文对象，以防性能下降或安全风险。

---

### 实践 2：利用 SageMaker 无服务器端点实现弹性推理

**说明**:
为了优化成本和延迟，应使用 Amazon SageMaker 的无服务器推理功能来部署 LLM。这消除了管理底层基础设施的需要，并能够根据对话流量自动扩展。对于 LangGraph 中的工具调用或模型推理步骤，配置 SageMaker 无服务器端点是最佳选择。

**实施步骤**:
1. 在 SageMaker 中创建模型实体，选择适合对话生成的模型（如 Claude 3）。
2. 配置端点配置，指定内存大小和最大并发数，启用无服务器计算。
3. 在 LangChain 的 SageMaker 调用链中，配置端点名称和推理参数，确保超时设置适合 LLM 的生成时间。

**注意事项**:
无服务器端点有冷启动时间。如果对首字延迟（TTFT）极其敏感，考虑配置预置并发或保持一定数量的热实例。

---

### 实践 3：集成托管 MLflow 进行全生命周期实验跟踪

**说明**:
使用 Amazon SageMaker 托管的 MLflow 实例来跟踪 LangGraph 的实验数据。这包括记录不同的图结构配置、Prompt 模板、Claude 模型参数以及评估指标。托管 MLflow 简化了运维，无需自行管理追踪服务器。

**实施步骤**:
1. 在 SageMaker Studio 中创建并启动 MLflow 实验跟踪服务器。
2. 在 LangGraph 代码中初始化 MLflow 客户端，使用 `mlflow.start_run()` 包装代理的执行或训练循环。
3. 记录关键参数（如 temperature, max_tokens）和指标（如对话轮次、用户满意度评分、Token 消耗量）。
4. 将 LangGraph 的构建逻辑或 Prompt 模板作为 Artifact 记录下来，以便版本回溯。

**注意事项**:
确保 MLflow 服务器与 SageMaker 执行角色之间的 IAM 权限配置正确，以便能够写入实验数据。

---

### 实践 4：实现基于工具调用的 RAG 与数据隔离

**说明**:
现代对话代理通常需要访问外部数据。最佳实践是将检索增强生成（RAG）逻辑封装为 LangGraph 中的“工具”。在 SageMaker 环境中，应确保这些工具通过私有链接访问数据源（如 Amazon RDS 或 OpenSearch Serverless），以保证数据安全。

**实施步骤**:
1. 定义 Python 函数作为工具，使用 LangChain 的 `@tool` 装饰器，并在函数内部实现知识库检索逻辑。
2. 在 LangGraph 中绑定这些工具到 Claude 模型，使模型能够自主决定何时调用检索工具。
3. 确保运行 LangGraph 的 Lambda 函数或容器拥有访问 VPC 内资源的权限，且数据传输经过加密。

**注意事项**:
严格限制工具的权限范围。如果工具涉及数据库查询，务必使用参数化查询防止 SQL 注入，并限制返回的行数以控制 Token 消耗。

---

### 实践 5：设计人机协同的审查与反馈循环

**说明**:
在无服务器架构中，处理 AI 幻觉或错误决策至关重要。最佳实践是在 LangGraph 中设计一个“人类审查”节点。当模型的置信度较低或涉及敏感操作时，流程应暂停并等待人工输入（通过 Amazon SQS 或 Step Functions 发送通知），然后再继续执行。

**实施步骤**:
1. 在 LangGraph 中定义条件边，根据模型的输出元数据（如 `stop_reason` 或自定义置信度分数）决定是进入结束节点还是审查节点。
2. 审查节点应将当前状态快照发送到 Amazon Simple Notification Service (SNS) 或 Step Functions 等待人工批准。
3. 构建一个简单的 API 端点，用于接收人工反馈并将其注入回 LangGraph 的状态中，以恢复图执行。

**注意事项**:
设计超时机制。如果人工在指定时间内未响应，系统应默认执行安全的回退操作（如拒绝请求或给出兜底回复），避免对话挂起。

---

### 实践 6：优化 Prompt 策略

---
## 学习要点

- 利用 LangGraph 构建基于 Claude 的有状态对话代理，通过循环图结构管理复杂的多轮对话上下文
- 集成托管式 MLflow 与 SageMaker AI，实现从模型实验、追踪到生产部署的全生命周期自动化管理
- 采用无服务器架构部署 AI 应用，消除基础设施运维负担并实现根据请求量的自动弹性伸缩
- 使用 Amazon Bedrock 托管 Claude 模型，无需自行维护底层模型即可获得高性能的生成式 AI 能力
- 通过 SageMaker AI 的统一托管环境，简化了机器学习模型的开发、训练与部署流程
- 结合 LangGraph 的状态管理机制与 MLflow 的实验追踪功能，有效提升对话式 AI 的迭代效率与可观测性

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/build-a-serverless-conversational-ai-agent-using-claude-with-langgraph-and-managed-mlflow-on-amazon-sagemaker-ai)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [LangGraph](/tags/langgraph/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [SageMaker AI](/tags/sagemaker-ai/) / [MLflow](/tags/mlflow/) / [对话代理](/tags/%E5%AF%B9%E8%AF%9D%E4%BB%A3%E7%90%86/) / [无服务器](/tags/%E6%97%A0%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [Agent](/tags/agent/) / [AWS Lambda](/tags/aws-lambda/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [基于Bedrock与LangGraph在SageMaker构建无服务器对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-2.md" >}})
- [基于Bedrock与LangGraph构建SageMaker无服务器AI对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
- [基于Amazon SageMaker AI构建无服务器Claude对话代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-3.md" >}})
- [基于Amazon SageMaker AI构建无服务器对话AI代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-13.md" >}})
- [在SageMaker AI上基于Bedrock与LangGraph构建无服务器对话代理]({{< relref "posts/20260303-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*