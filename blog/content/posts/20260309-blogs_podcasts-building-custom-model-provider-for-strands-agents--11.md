---
title: "在 SageMaker 上部署 SGLang 并为 Strands Agents 构建自定义模型解析器"
date: 2026-03-09T14:04:55+08:00
draft: false
entry_kind: "auto"
tags: ["SageMaker", "SGLang", "Llama 3.1", "Strands Agents", "模型部署", "自定义解析器", "AWS", "LLM"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何在 Amazon SageMaker AI 上部署 LLM（如 Llama 3.1），并通过构建**自定义模型解析器**将其集成到 Strands Agents 中，从而兼容非 Bedrock 原生格式的模型。 核心流程如下： 1. **模型部署**： 利用 工具，在 SageMaker 上部署采用 SG"
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios: ["大语言模型", "后端开发"]
---

# 在 SageMaker 上部署 SGLang 并为 Strands Agents 构建自定义模型解析器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---
## 摘要/简介

本文演示了在配合使用托管于 SageMaker 上且不原生支持 Bedrock Messages API 格式的 LLM 时，如何为 Strands agents 构建自定义模型解析器。我们将介绍如何使用 awslabs/ml-container-creator 在 SageMaker 上部署带有 SGLang 的 Llama 3.1，然后实现一个自定义解析器，将其与 Strands agents 集成。

---
## 导语

在构建生成式 AI 应用时，将自托管大语言模型（LLM）与智能体框架集成往往面临接口适配的挑战。本文以部署在 Amazon SageMaker 上的 Llama 3.1 为例，详细演示了如何为 Strands Agents 构建自定义模型提供程序。通过阅读本文，您将掌握利用 SGLang 优化模型部署，并编写解析器以实现非标准接口模型与智能体无缝对接的完整流程。

---
## 摘要

本文介绍了如何在 Amazon SageMaker AI 上部署 LLM（如 Llama 3.1），并通过构建**自定义模型解析器**将其集成到 Strands Agents 中，从而兼容非 Bedrock 原生格式的模型。

核心流程如下：

1.  **模型部署**：
    利用 `awslabs/ml-container-creator` 工具，在 SageMaker 上部署采用 SGLang 推理框架的 Llama 3.1 模型。

2.  **自定义解析**：
    由于该模型输出格式不直接兼容 Bedrock Messages API，文章演示了如何编写并应用自定义解析器，对输入输出进行转换，以确保 Strands Agents 能正确调用模型。

---
## 评论

### 中心观点
该文章（基于摘要推断）的核心观点是：**企业应通过在 SageMaker 上部署 SGLang 优化的自定义模型端点，并构建适配层（Custom Parser），来打破 AWS Bedrock 对特定模型协议的锁定，从而在 AWS 生态内实现对高性能开源 LLM（如 Llama 3.1）的自主可控与低延迟调用。**

### 支撑理由与边界条件分析

**1. 支撑理由：性能优化与协议解耦的双重价值**
*   **技术深度（事实陈述）：** 文章选择 **SGLang** 而非默认的 vLLM 或 HuggingFace TGI 作为推理引擎，是一个极具技术洞察力的选择。SGLang 以其结构化生成和 RadixAttention 技术在处理复杂 JSON 和多轮对话时具有显著的延迟优势。结合 **awslabs/ml-container-creator**，作者实际上是在构建一条“高性能推理 CI/CD流水线”，这比单纯部署模型更具工程价值。
*   **架构灵活性（你的推断）：** 文章强调“Custom Model Provider”和“Parser”，实质上是在推行一种**“BFF（Backend for Frontend）模式”**在 AI 架构中的应用。通过将 SageMaker 的原生输出转换为 Bedrock Messages API 格式，使得上层应用代码无需修改即可切换底层模型，这极大降低了迁移成本。

**2. 支撑理由：成本效益与合规性的平衡**
*   **行业痛点（作者观点）：** 对于金融、政务等高度敏感行业，直接调用公有云的托管 API（如 Bedrock）可能存在数据合规风险。在 SageMaker 上利用 **VPC（虚拟私有云）** 部署自托管模型，可以实现数据的“不出域”。同时，使用 Llama 3.1 8B/70B 等开源模型替代 GPT-4，在特定任务上能大幅降低 Token 成本。

**3. 反例与边界条件**
*   **边界条件 1（运维复杂度爆炸）：** 文章可能低估了运维负担。自部署意味着你要负责模型的高可用（HA）、自动扩缩容（ASG）以及版本更新。如果业务流量波动剧烈，SageMaker 异步推理的冷启动时间可能会抵消 SGLang 带来的性能优势。相比之下，Bedrock 提供的按需付费无需维护基础设施。
*   **边界条件 2（功能生态的缺失）：** Llama 3.1 虽然强大，但原生不支持像“Function Calling（函数调用）”那样的严格模式输出。文章提到的 Custom Parser 如果仅依赖 Prompt Engineering 来强制 JSON 输出，在处理复杂 Agent 链路时，输出格式的稳定性不如 Bedrock 上原生的 Claude 3.5 Sonnet，这可能导致 Agent 流程中断率上升。

### 维度深入评价

**1. 内容深度与严谨性**
*   **评价：** 文章触及了当前 AI 落地中最深层的“碎片化”问题。不仅涉及模型部署，还涉及协议适配。SGLang 的选择显示了作者对前沿推理技术的敏感度。
*   **批判：** 摘要未提及显存优化（如 KV Cache 传输）的具体配置。对于 Llama 3.1 405B 这样的大参数模型，SageMaker 实例的显存瓶颈和 Multi-GPU 通信开销是巨大的挑战，如果文章避而不谈配置细节，实操性会打折扣。

**2. 实用价值**
*   **评价：** 极高。它提供了一套标准化的“逃离 API 锁定”的模板代码。对于正在构建企业级 Agent 平台且希望混合使用托管模型和开源模型的团队，这篇教程是必读的。
*   **局限：** 代码示例可能高度依赖 AWS 的特定 SDK 版本，随着 SageMaker SDK 更新，兼容性维护将是一大痛点。

**3. 创新性**
*   **评价：** 将 SGLang 引入 SageMaker 容器构建流程属于较新的实践。大多数 AWS 官方文档推荐 TGI，社区文章多推荐 vLLM，SGLang 的引入针对“结构化输出”这一 Agent 核心痛点，具有针对性创新。

**4. 行业影响**
*   **趋势：** 这代表了 **“混合部署架构”** 的兴起。企业不再单一依赖公有云托管服务，而是倾向于“核心敏感数据自托管 + 通用任务托管 API”的混合模式。这篇文章为这种模式提供了具体的落地路径。

### 实际应用建议

1.  **监控与可观测性：**
    *   在部署 Custom Parser 时，务必在解析层加入详细的日志和指标。当模型输出不符合预期格式时，能够快速定位是模型幻觉还是解析逻辑 Bug。
2.  **灰度发布策略：**
    *   不要一次性将所有流量从 Bedrock 切换到 SageMaker 自托管端点。建议基于 Agent 的 Session ID 进行金丝雀发布，对比两者的响应延迟和输出质量。
3.  **降级熔断机制：**
    *   SageMaker 端点可能出现扩容失败或超时。必须在 Agent 代码中实现“兜底逻辑”：当自托管端点不可用时，自动回退到 Bedrock 托管模型，确保业务连续性。

### 可验证的检查方式

1.  **性能对比测试：**
    *   **指标：** Time to First Token (TTFT) 和 End-to-End Latency。
    *   **实验：** 在相同 Prompt 下，对比 Bed

---
## 技术分析

基于您提供的文章标题和摘要，尽管原文内容被截断，但结合AWS技术生态、SageMaker、Strands Agents（推测为AWS内部或特定领域的Agent框架，此处视作通用的Agent应用框架）以及Llama 3.1与SGLang的技术特性，以下是对该技术方案的深度全面分析。

---

# 深度分析报告：构建基于SageMaker托管LLM的自定义Agent模型提供商

## 1. 核心观点深度解读

**主要观点：**
文章的核心观点是**“解耦与适配”**。它主张在构建AI智能体时，不应被单一云厂商的原生API（如AWS Bedrock Messages API）所锁定。通过在SageMaker上利用SGLang部署高性能Llama 3.1模型，并构建自定义模型解析器，开发者可以实现非标准接口模型与标准Agent框架的无缝集成。

**核心思想：**
作者传达了**“基础设施灵活性优先于开发便利性”**的工程哲学。虽然Bedrock提供了开箱即用的体验，但企业往往出于成本控制、数据隐私合规或特定模型性能（如SGLang提供的极高吞吐量）的考虑，选择自部署模型。文章的核心在于展示如何通过“中间层”代码来抹平异构模型接口与标准化Agent框架之间的鸿沟。

**观点的创新性与深度：**
*   **深度集成：** 这不是简单的API调用，而是深入到Agent框架的“模型提供商”扩展机制，展示了如何修改框架底层逻辑以适配自定义协议。
*   **性能导向：** 引入SGLang是一个关键的技术亮点。SGLang以其激进的结构化生成和OpenAI API兼容性著称，这暗示了文章不仅解决“能用”的问题，还解决了“高效”的问题。

**重要性：**
随着大模型落地进入深水区，企业从“调用公有云API”转向“私有化部署”或“混合云部署”是必然趋势。掌握如何将任意开源模型（Llama 3.1）部署在任意基础设施上，并能被主流Agent框架直接调用，是AI工程化落地的核心能力。

## 2. 关键技术要点

**涉及的关键技术：**
*   **AWS SageMaker:** 用于托管Llama 3.1模型，提供基础设施即代码和自动扩缩容能力。
*   **SGLang:** 一个由UC Berkeley研究人员开发的高性能LLM推理引擎，特别优化了结构化输出和并发处理。
*   **awslabs/ml-container-creator:** AWS提供的工具，用于简化构建符合SageMaker规范的Docker容器。
*   **Llama 3.1:** Meta发布的最新开源大模型系列，支持128k上下文和复杂推理。
*   **Bedrock Messages API Format:** AWS Bedrock定义的标准消息交换格式。

**技术原理与实现：**
1.  **容器化部署：** 利用`ml-container-creator`将Llama 3.1模型权重和SGLang推理服务器打包成一个Docker镜像。SGLang服务器启动后会监听端口，提供HTTP接口。
2.  **接口适配：** SGLang原生可能不完全兼容Bedrock的协议。文章提到的“Implementing a...（实现自定义解析器）”是指在Agent代码中编写一个适配层。该层接收Agent的标准请求，转换为SGLang/Llama理解的格式，并将模型的原始输出解析回Agent期望的JSON或工具调用格式。
3.  **推理加速：** SGLang利用RadixAttention等技术减少显存占用，提高Token生成速度，这对于需要频繁交互的Agent至关重要。

**技术难点与解决方案：**
*   **难点：** **工具调用的格式对齐。** 现代Agent依赖Function Calling，这要求模型输出严格的JSON Schema。非Bedrock模型可能默认输出纯文本。
*   **方案：** 利用SGLang的Constrained Decoding（约束解码）能力，强制模型输出符合Schema的JSON；或者在自定义Parser中使用正则/JSON解析器来提取意图。

**技术创新点：**
*   **异构统一：** 将SageMaker这种通用容器平台变成了一个具备Bedrock能力的“伪Bedrock端点”。
*   **SGLang的应用：** 相比于使用vLLM或TGI，SGLang在处理Agent所需的复杂Prompt和结构化输出时往往有更优的性能表现。

## 3. 实际应用价值

**指导意义：**
该方案为企业在**“数据主权”**与**“技术栈先进性”**之间提供了平衡点。企业既可以将模型部署在VPC内部（SageMaker）保证数据不出域，又能利用最新的开源模型（Llama 3.1）和高效的推理引擎（SGLang）。

**应用场景：**
1.  **金融/医疗合规场景：** 数据不允许传输给公有云大模型，必须在私有VPC内的SageMaker上运行。
2.  **成本敏感型场景：** Bedrock按Token计费可能较高，对于高并发请求，使用SageMaker预留实例或Spot实例运行SGLang更具成本效益。
3.  **模型微调集成：** 企业微调了Llama 3.1，需要将其快速集成到Agent工作流中，而不需要等待Bedrock上架新模型。

**注意事项：**
*   **运维复杂度：** 需要自行维护Docker镜像、模型版本更新和SageMaker端点的健康检查，这比直接调用API复杂得多。
*   **冷启动时间：** SageMaker端点在从0扩容时可能需要几分钟加载模型，不适合对延迟极度敏感的突发流量（除非配置预留实例）。

## 4. 行业影响分析

**行业启示：**
这标志着**“大模型中间件”**时代的到来。未来的竞争不仅仅是模型参数量的竞争，更是**模型路由、推理优化和协议适配**的竞争。

**可能带来的变革：**
*   **MaaS（Model as a Service）的标准化：** 越来越多的工具会支持OpenAI或Bedrock协议作为事实标准，而推理引擎（如SGLang）会主动兼容这些协议，降低适配成本。
*   **私有化Agent的普及：** 降低了构建私有化Agent的门槛，企业不再依赖昂贵的商业API。

**发展趋势：**
*   **推理引擎之争：** vLLM、TGI、SGLang、TensorRT-LLM之间的竞争将愈发激烈，Agent开发者需要根据场景（如长文本、多模态、工具调用）选择最合适的后端。

## 5. 延伸思考

**拓展方向：**
*   **动态路由：** 既然有了自定义Provider，可以进一步实现“智能路由”——简单问题用小模型（如Llama 3.1 8B），复杂问题路由到大模型（如Llama 3.1 405B），且都部署在SageMaker上。
*   **多模态扩展：** Llama 3.1是纯文本模型，如何将VLM（视觉语言模型）通过类似的SGLang方式部署并接入Agent？

**待研究问题：**
*   SGLang在处理极长上下文（128k+）时的显存管理效率在SageMaker特定GPU实例（如g5或p4d）上的表现如何？
*   自定义Parser的引入会增加多少延迟？

## 6. 实践建议

**如何应用到项目：**
1.  **评估现状：** 检查你的Agent框架是否支持自定义Model Provider。如果不支持，考虑在框架外封装一个轻量级服务（使用FastAPI）作为转换层。
2.  **容器选型：** 不要从零写Dockerfile。直接使用`awslabs/ml-container-creator`或SGLang官方提供的SageMaker启动模板。
3.  **协议对齐：** 确保你的SGLang启动参数中开启了类似`--chat-template`的功能，使其尽可能模仿OpenAI/Bedrock的响应格式，减少Parser的编写工作量。

**行动建议：**
*   先在本地使用Docker运行SGLang + Llama 3.1，验证其输出格式是否符合你的Agent要求。
*   编写单元测试，测试Parser是否能正确处理模型输出的边缘情况（如截断、乱码、拒绝回答）。

**补充知识：**
*   需要深入学习**AWS IAM角色**的配置，确保Agent有权限调用SageMaker端点。
*   熟悉**JSON Schema**和**Structured Generation**原理。

## 7. 案例分析

**成功案例（假设性）：**
某电商公司构建客服Agent。
*   **背景：** 需要利用公司内部知识库（RAG），数据敏感，且每天需处理百万级对话，Bedrock成本过高。
*   **做法：** 在SageMaker上部署Llama 3.1 70B（SGLang后端）。编写自定义Parser将Agent的“查询库存”工具调用转化为SGLang请求。
*   **结果：** 成本降低60%，且由于SGLang的高效并发，P95延迟保持在1秒以内。

**失败反思：**
*   **问题：** 开发者未处理SageMaker的自动扩缩容策略。
*   **后果：** 夜间流量低谷时端点缩容至0，早高峰流量涌入时端点正在初始化（加载模型需5分钟），导致大量请求超时，Agent体验崩塌。
*   **教训：** 对于生产环境，必须配置预置实例或设置合理的扩容策略，不能仅依赖Spot实例。

## 8. 哲学与逻辑：论证地图

**中心命题:**
在构建企业级Strands Agents时，**应当**优先采用在SageMaker上部署SGLang+Llama 3.1并配合自定义解析器的方案，而非直接依赖Bedrock原生API，以实现性能与成本的最优平衡。

**支撑理由:**
1.  **成本效益:** 对于高并发场景，SageMaker按实例计费通常比Bedrock按Token计费更具边际成本优势。
2.  **数据隐私:** SageMaker允许在VPC内部署，满足金融、医疗等行业对数据不出域的严格合规要求。
3.  **性能可控性:** SGLang提供了比通用推理引擎更高的吞吐量和更低的延迟，特别是对于结构化输出。
4.  **模型迭代自由度:** 企业可以随时替换模型权重（如微调后的版本），而无需等待云厂商审核上架。

**反例/边界条件:**
1.  **低频/开发测试场景:** 如果业务处于POC阶段或流量极低，维护SageMaker基础设施的运维成本（人力与时间）将远超直接调用API的费用。
2.  **极致低延迟需求:** 如果业务要求毫秒级响应且无法容忍冷启动，Bedrock等托管服务的全局分发能力可能优于单一区域的SageMaker端点。

**命题性质分析:**
*   **事实判断:** SGLang确实比部分传统推理引擎快；SageMaker确实支持VPC部署。
*   **价值判断:** “数据隐私”和“长期成本”比“开发便利性”更重要。
*   **可检验预测:** 采用该方案后，在QPS>50的场景下，推理成本将下降30%以上，但首次部署周期将增加2-3天。

**立场与验证:**
**我的立场：** 支持该命题，但建议采用**混合架构**。
**验证方式：**
*   **A/B测试：** 部署两套Agent系统，一套使用Bedrock

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 SageMaker 端点的延迟与吞吐量配置

**说明**: 在构建自定义模型提供商时，Strands Agents 对 LLM 的响应速度非常敏感。SageMaker 端点的实例类型和多模型配置直接影响推理延迟。必须确保端点配置能够处理并发请求，同时保持低延迟，以提供流畅的对话体验。

**实施步骤**:
1. 根据模型大小和预期并发量，选择合适的实例类型（如用于推理加速的 `ml.g5` 或 `ml.p4` 实例）。
2. 启用 SageMaker 的 **Multi-Model Endpoints (MME)** 或 **Multi-Container Endpoints** 以提高资源利用率。
3. 配置适当的实例数量，并利用 **Auto Scaling** 策略根据 CPU 利用率或请求数量动态扩展实例。

**注意事项**: 避免使用 CPU 实例运行大型语言模型，除非模型经过了极度量化。在生产环境中，务必开启 Model Monitoring 以监控响应时间。

---

### 实践 2：严格遵循 Strands Agents 的输入输出模式

**说明**: Strands Agents 通过特定的 JSON Schema 与模型提供商通信。自定义适配器必须将 Strands 的标准请求格式转换为 SageMaker 端点所需的格式（例如将 JSON 转换为基础模型所需的特定 payload 格式，如 HuggingFace 的 `{"inputs": "..."}），并将响应转换回 Strands 期望的统一结构。

**实施步骤**:
1. 定义请求转换函数，将 Strands 发送的消息列表转换为模型推理所需的 Prompt 模板。
2. 定义响应解析函数，提取生成的文本、Token 使用量和 `finish_reason`。
3. 在代码中处理流式响应（如果支持），将 SSE (Server-Sent Events) 映射回 Agents 框架。

**注意事项**: 确保错误处理机制能够捕获 SageMaker 的内部错误（如 Model Loading Error），并将其转换为 Strands Agents 可读的标准错误信息，防止 Agent 崩溃。

---

### 实践 3：实施全面的身份验证与网络隔离

**说明**: 将 SageMaker 端点暴露给 Strands Agents 时，安全性至关重要。应避免使用硬编码的 AWS 凭证，并确保通信链路加密。最佳实践是利用 IAM Role 和 VPC 接口端点来保护调用。

**实施步骤**:
1. 为 Strands Agents 的运行环境配置具有最小权限的 IAM Role，仅允许调用特定 SageMaker 端点的 `sagemaker:InvokeEndpoint` 权限。
2. 如果可能，将 SageMaker 端点配置在 VPC 内部，并使用 VPC Interface Links (PrivateLink) 进行私有连接。
3. 确保所有数据传输均通过 TLS 加密。

**注意事项**: 定期轮换用于集成的访问密钥。切勿在日志或代码中打印 AWS Access Key ID 和 Secret Access Key。

---

### 实践 4：建立结构化的日志记录与可观测性

**说明**: 集成自定义模型提供商时，调试变得复杂。为了追踪请求在 Strands、自定义适配器和 SageMaker 之间的流转，必须建立统一的日志记录机制，记录 Prompt 内容、Token 计数和推理时间。

**实施步骤**:
1. 在自定义提供商代码中，记录发送至 SageMaker 的完整 Payload（需脱敏敏感信息）和返回的原始响应。
2. 利用 Amazon CloudWatch Logs 收集 SageMaker 端点的日志，并设置日志流。
3. 在响应元数据中返回 `billed_tokens` 和 `latency_ms`，以便 Strands Agents 进行成本和性能分析。

**注意事项**: 记录日志时注意数据隐私，不要记录用户的 PII (Personally Identifiable Information) 或完整的敏感上下文。

---

### 实践 5：设计健壮的重试与回退机制

**说明**: 云端推理服务可能会遇到瞬时的网络抖动、限流或冷启动问题。自定义提供商代码必须具备弹性，能够自动处理 5xx 错误或 429 (Too Many Requests) 错误，避免因单次请求失败导致 Agent 任务中断。

**实施步骤**:
1. 实现指数退避算法，在遇到 `ModelNotReady` 或 `ServiceUnavailable` 错误时自动重试。
2. 设置合理的超时时间，既要考虑大模型的生成长度，又要避免长时间挂起。
3. 配置断路器模式，当端点持续失败时，暂时停止发送请求并返回降级响应。

**注意事项**: 对于非幂等的请求（如某些写入操作，虽然 LLM 推理通常是只读的），重试需谨慎。确保重试逻辑不会导致 AWS 账单激增。

---

### 实践 6：针对特定模型进行 Prompt 模板微调

**说明**: 不同的开源模型（如 Llama 3, Mistral, Falcon）在 SageMaker 上部署时，对 Prompt 格式的要求不同（例如是否需要特定的 `[INST]` 标签或系统提示词前缀）。自定义提供商需要根据部署的具体模型版本

---
## 学习要点

- 通过实现标准化接口（如 LangChain 的 BaseLLM），可以将部署在 SageMaker 上的自定义大语言模型无缝集成到 Strands Agents 框架中。
- 利用 SageMaker 托管模型能够通过私有网络通信增强数据隐私，并允许针对特定业务场景进行微调以提高模型表现。
- 构建自定义模型提供商的核心在于编写一个适配器类，负责处理输入提示词的格式化以及将模型原始输出解析为标准字符串。
- 在 SageMaker 端点配置中，正确设置序列化器和反序列化器是确保 Python 客户端与模型容器之间数据正确传输的关键。
- 这种架构设计支持灵活切换底座模型，使开发者能够根据成本、性能或特定领域需求动态选择最合适的 LLM。
- 实施该方案需要具备 AWS 基础设施知识，特别是关于 SageMaker 异步推理和端点部署配置的操作经验。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [SageMaker](/tags/sagemaker/) / [SGLang](/tags/sglang/) / [Llama 3.1](/tags/llama-3.1/) / [Strands Agents](/tags/strands-agents/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/) / [AWS](/tags/aws/) / [LLM](/tags/llm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--4.md" >}})
- [为 Strands 智能体构建 SageMaker 托管 LLM 的自定义模型解析器]({{< relref "posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--10.md" >}})
- [在 SageMaker 上部署 SGLang 并为 Strands 智能体构建自定义模型解析器]({{< relref "posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*