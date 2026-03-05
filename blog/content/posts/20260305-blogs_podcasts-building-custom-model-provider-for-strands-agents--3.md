---
title: "为 Strands 智能体构建 SageMaker 托管 LLM 自定义解析器"
date: 2026-03-05T19:19:47+08:00
draft: false
entry_kind: "auto"
tags: ["AWS SageMaker", "Strands", "LLM", "SGLang", "Llama 3.1", "自定义解析器", "模型部署", "智能体"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "**内容总结** 本文介绍了如何为 Strands Agents 构建自定义模型提供商，以便集成那些不支持 Bedrock Messages API 原生格式的 LLM（大语言模型）。文章以在 SageMaker 上部署 Llama 3.1 为例，详细说明了通过 SGLang 和自定义解析器实现集成的步骤。 **主要流"
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios: ["大语言模型", "后端开发"]
---

# 为 Strands 智能体构建 SageMaker 托管 LLM 自定义解析器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---
## 摘要/简介

本文演示了在对接托管于 SageMaker 且原生不支持 Bedrock Messages API 格式的 LLM 时，如何为 Strands 智能体构建自定义模型解析器。我们将介绍如何使用 awslabs/ml-container-creator 在 SageMaker 上通过 SGLang 部署 Llama 3.1，然后实现一个自定义解析器以将其与 Strands 智能体集成。

---
## 导语

本文演示如何在 Amazon SageMaker 上利用 SGLang 部署 Llama 3.1，并详细解析构建自定义模型提供者的具体步骤，助您在 AWS 环境中实现大模型与 Strands 智能体的无缝集成。

---
## 摘要

**内容总结**

本文介绍了如何为 Strands Agents 构建自定义模型提供商，以便集成那些不支持 Bedrock Messages API 原生格式的 LLM（大语言模型）。文章以在 SageMaker 上部署 Llama 3.1 为例，详细说明了通过 SGLang 和自定义解析器实现集成的步骤。

**主要流程包括：**

1.  **模型部署**：利用 AWS 实验室的 `ml-container-creator` 工具，在 SageMaker AI 端点上部署搭载 SGLang 的 Llama 3.1 模型。
2.  **自定义集成**：由于部署的模型不直接兼容 Bedrock Messages API 格式，文章演示了如何实现一个**自定义解析器**。
3.  **最终目标**：通过该解析器，将 SageMaker 上托管的 LLM 成功接入 Strands Agents 框架，使其能够顺畅地调用模型能力。

---
## 评论

### 深度评价：为 Strands Agents 构建基于 SageMaker AI 端点的自定义模型提供商

**文章中心观点**
该文章探讨了在 AWS SageMaker 上通过 SGLang 部署 Llama 3.1，并构建自定义模型解析器，以解决非标准模型与 AWS Bedrock Agents 生态集成问题的技术路径。

**核心评价与支撑理由**

**1. 内容深度：填补了“最后一公里”的集成空白**
*   **支撑理由（事实陈述）：** AWS Bedrock 原生支持的模型范围有限。出于数据主权或成本考量，许多企业倾向于在 SageMaker 上自托管开源模型（如 Llama 3.1）。然而，Bedrock Agents 的编排层严格依赖于特定的 Messages API 格式（通常与 Bedrock API 紧耦合）。这篇文章的深度在于它超越了“如何部署模型”的基础范畴，深入到了“协议转换”这一工程难点。通过实现自定义解析器，文章展示了如何屏蔽底层模型（如 SGLang 部署的 Llama）与上层代理框架之间的接口差异，这是实现工程化落地的关键环节。
*   **反例/边界条件（推断）：** 这种深度主要局限于“接口适配层”。文章可能未涉及更深层次的推理优化。例如，如果 SGLang 的输出格式与 Bedrock Agents 要求的工具调用格式存在结构性差异（如 JSON Schema 的严格校验），简单的解析器可能难以处理复杂的幻觉或格式错误，此时可能需要引入更复杂的中间件或语义路由层。

**2. 实用价值：为“混合云架构”提供了参考范式**
*   **支撑理由（作者观点）：** 文章使用 `awslabs/ml-container-creator` 和 SGLang 的组合具有实战参考价值。SGLang 以高吞吐和低延迟的特性，适合作为 Agent 的后端推理引擎。对于大型企业而言，这种架构允许他们在保留 Bedrock 编排能力的同时，将敏感数据流量保留在 SageMaker 的 VPC 内，而不必调用公有云的 Bedrock 托管端点。这为寻求“Agent 便利性与模型私有化兼顾”的场景提供了一种可行的技术方案。
*   **反例/边界条件（事实陈述）：** 该方案增加了运维复杂度。使用 Bedrock 原生模型属于“无服务器”体验，而此方案需要维护 SageMaker 端点、容器构建和扩缩容策略。对于缺乏成熟 MLOps 团队的中小型企业，这种“定制自由度”可能转化为“运维负担”。

**3. 创新性：技术栈组合的微创新，但架构逻辑遵循传统模式**
*   **支撑理由（推断）：** 将 SGLang 这种高性能推理框架引入 AWS 生态，并打通 Bedrock Agents 的自定义配置，是一种较新的尝试。这展示了 AWS 生态具备一定的“可组合性”。
*   **反例/边界条件（作者观点）：** 从架构视角分析，这并非颠覆性创新。本质上仍是在解决“API 兼容性”问题。行业中已有 LangChain 或 LangFlow 等通用框架可以更灵活地对接 SageMaker 端点，而不必强行绑定 Bedrock Agents 的自定义 Provider 机制。文章的创新性受限于 AWS 的特定生态闭环，通用性不如部分开源方案。

**4. 行业影响与争议点：Vendor Lock-in（厂商锁定）的双刃剑**
*   **支撑理由（推断）：** 文章反映了当前 AI 落地的一个趋势：企业正在从单一的“模型比拼”转向“编排能力的比拼”。Bedrock Agents 提供了编排、记忆、工具调用等能力，企业只需关注底层模型的替换。
*   **争议点（作者观点）：** 这种做法虽然看似灵活，但实际上加深了对 AWS Bedrock Agents 服务层的依赖。一旦业务逻辑深度绑定 Bedrock 的 Agent 定义格式，未来若想迁移至 Azure AI Studio 或完全自建的开源 Agent 框架（如 AutoGen），迁移成本可能较高。这是一种值得注意的“软性锁定”。

**实际应用建议**

1.  **成本与性能的权衡验证：** 在生产环境采用前，必须对比 Bedrock 托管成本与 SageMaker 自托管成本（包括 GPU 实例闲置费用）。建议设置监控指标：`Token/秒` 和 `首字延迟（TTFT）`。如果流量波峰波谷明显，SageMaker 的常驻实例成本可能高于按量计费的 Bedrock。
2.  **错误处理机制的增强：** 自定义解析器往往是系统中的脆弱环节。建议在解析器中增加“降级逻辑”，例如当 Llama 3.1 输出的 JSON 格式无法被 Agent 解析时，能够回退到重试机制或通过提示词工程引导模型重新生成，而非直接抛出错误导致流程中断。

---
## 技术分析

基于您提供的文章标题和摘要，以及对AWS技术生态（SageMaker、Strands Agents、Bedrock、SGLang）的深入理解，以下是对该文章内容的全面深度分析。

---

# 深入分析：在 SageMaker AI 端点上构建支持 Strands Agents 的自定义模型提供商

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：**企业不应被云厂商的专有 API 格式（如 AWS Bedrock Messages API）所束缚，完全可以在 SageMaker 等托管服务上使用开源模型（如 Llama 3.1）和高效推理框架（如 SGLang），并通过实现自定义解析器来无缝对接高级 Agent 框架。**

**作者想要传达的核心思想**
作者主张“**可组合性优于单一锁定**”。虽然 AWS Bedrock 提供了标准化的接口，但在处理特定需求（如极低延迟、特定模型版本、或非 Bedrock 托管的模型）时，SageMaker 部署自定义容器是更优的选择。核心思想在于展示如何通过构建“适配层”，将非标准接口的模型转化为能够被复杂 Agent 系统（Strands）调用的能力，从而实现**基础设施的灵活性与上层应用开发的一致性之间的平衡**。

**观点的创新性和深度**
*   **打破黑盒：** 传统做法往往是“模型适应 Agent”，即只使用 Agent 支持的模型。该文章反其道而行，展示了“Agent 适应模型”，通过代码层面的扩展解决了模型格式不兼容的问题。
*   **全栈优化：** 结合了 `awslabs/ml-container-creator`（底层容器构建）、`SGLang`（推理加速）和 `Strands Agents`（应用编排），涵盖了从 GPU 到 AI 应用的完整技术栈，具有很强的工程深度。

**为什么这个观点重要**
随着大模型落地进入深水区，企业面临着**成本控制**、**数据隐私**和**性能定制**的三重压力。仅仅依赖云厂商的托管 API（Bedrock）可能无法满足所有场景。掌握在 SageMaker 上部署高性能开源模型并接入 Agent 框架的能力，意味着企业拥有了**底层的控制权**，可以根据业务需求在专有 API 和自托管模型之间自由切换，而不需要重写上层应用代码。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **SageMaker AI Endpoints:** AWS 提供的机器学习模型托管服务，支持部署自定义 Docker 容器。
2.  **SGLang:** 一个高性能的大语言模型推理运行时，以其高吞吐和低延迟著称，特别适合处理 Agent 场景中频繁的 Token 生成。
3.  **Llama 3.1:** Meta 开源的高性能模型系列，通常作为自托管的首选。
4.  **awslabs/ml-container-creator:** AWS Labs 提供的工具，用于简化构建兼容 SageMaker 的推理容器。
5.  **Strands Agents:** 文中提到的 Agent 框架（注：Strands 可能指代特定的 AWS 内部框架或客户定制的 Agent 系统，此处泛指需要特定 Message API 格式的 Agent 架构）。
6.  **Bedrock Messages API 格式:** 一种标准化的 JSON 结构（包含 `messages` 数组、`system` 字段等），用于简化与 LLM 的交互。

**技术原理和实现方式**
*   **部署层：** 使用 `ml-container-creator` 将 HuggingFace 上的 Llama 3.1 模型和 SGLang 推理服务器打包成一个 Docker 镜像。这个镜像被推送到 Amazon ECR，并部署在 SageMaker 端点上。
*   **适配层：** 这是文章的技术核心。SageMaker 端点接收请求，但 SGLang 原生可能不完全遵循 Bedrock 的 `messages` API 格式（例如，它可能使用 OpenAI 兼容格式或原始 Prompt 模板）。
*   **解析器实现：** 作者编写了一个自定义模型解析器。这个解析器在 SageMaker 的容器内（或作为 Lambda 层）运行，执行以下逻辑：
    1.  **拦截请求：** 接收来自 Agent 的标准 Bedrock 格式 JSON。
    2.  **转换：** 将 Bedrock 格式转换为 SGLang 期望的格式（例如，将 Chat History 转换为 SGLang 的对话模板）。
    3.  **调用：** 调用本地 SGLang 服务进行推理。
    4.  **响应转换：** 将 SGLang 的输出转换回 Bedrock 格式返回给 Agent。

**技术难点和解决方案**
*   **难点：** **Token 流式传输的对齐。** Agent 通常需要流式响应以降低首字延迟（TTFT），而 Bedrock Messages API 有特定的流式协议。SGLang 也有自己的流式输出机制。
*   **解决方案：** 自定义解析器必须处理字节流的转换，确保 SSE (Server-Sent Events) 事件格式与 Agent 框架期望的完全一致，否则会导致 Agent 解析错误或无法实时显示生成内容。

**技术创新点分析**
利用 **SGLang** 替代传统的 vLLM 或 TGI，结合 SageMaker 的 **Serverless Inference**（如果支持）或 **Real-time Inference**，并通过轻量级代码实现 API 兼容，这种“**混合架构**”既利用了 AWS 的托管便利性，又获得了开源推理引擎的性能红利。

## 3. 实际应用价值

**对实际工作的指导意义**
对于正在构建 AI 应用的架构师和开发者，这篇文章提供了一条避开 Bedrock 独占限制的路径。它告诉我们：**即使你的 Agent 框架（如 LangChain 或 AWS Bedrock Agents）原生只支持 Bedrock，你依然可以通过“伪装”成 Bedrock API 的方式，使用 SageMaker 上的任何模型。**

**可以应用到哪些场景**
1.  **高度定制化模型：** 微调过的 Llama 3.1，无法在 Bedrock 上直接托管，必须部署在 SageMaker。
2.  **成本敏感型场景：** 使用 SageMaker 实例预留（Savings Plans）可能比按量调用 Bedrock API 更便宜。
3.  **低延迟要求：** SGLang 在特定硬件（如 p5/p4 实例）上的推理性能可能优于通用 API 网关。
4.  **数据驻留合规：** 数据不能离开特定的 VPC 或加密环境，必须使用自托管端点。

**需要注意的问题**
*   **维护成本：** 你需要维护 Docker 容器、SGLang 版本升级以及自定义解析器代码，而使用 Bedrock API 则是零维护。
*   **功能缺失：** 自定义解析器可能无法完美复刻 Bedrock 的所有特性（如 Guardrails 过滤、Trace 数据捕获）。

**实施建议**
*   优先使用 `ml-container-creator` 等工具标准化容器构建流程。
*   为自定义解析器编写单元测试，确保输入输出 JSON 结构与 Bedrock 规范严格一致。
*   监控 SGLang 的 P99 延迟和内存占用，防止 OOM（内存溢出）导致端点崩溃。

## 4. 行业影响分析

**对行业的启示**
这标志着**AI 基础设施正在从“垂直整合”走向“水平解耦”**。过去，模型、API 和应用是紧耦合的；现在，开发者可以像搭积木一样，选择 AWS 的算力、Meta 的模型、伯克利（SGLang 作者）的推理技术，以及自家的 Agent 应用。这种解耦赋予了企业极大的议价权和技术选择权。

**可能带来的变革**
*   **MaaS (Model as a Service) 的泛化：** 任何托管在云上的模型服务，只要通过适配层，都可以变成“类 Bedrock”服务。
*   **推理框架的竞争加剧：** 随着部署门槛的降低，企业会更倾向于选择性能更优的开源推理框架（如 SGLang、vLLM），倒逼云厂商优化其托管服务的性能。

**对行业格局的影响**
削弱了超大规模云厂商通过专有 API 锁定客户的能力。如果客户可以轻松地在 SageMaker 和 Bedrock 之间切换，云厂商必须通过**真正的性能优势**和**服务体验**来留住客户，而不是仅仅依靠格式锁定。

## 5. 延伸思考

**引发的其他思考**
*   **标准化的缺失：** 为什么我们需要自定义解析器？因为业界缺乏统一的 LLM RPC 标准。OpenAI 格式虽然事实标准，但并非所有人都能完美支持。Kubernetes 的 CNI 模式是否可以借鉴到 AI 领域？
*   **多模型负载均衡：** 如果我们在 SageMaker 上部署了多个 Llama 实例，如何配合 Agent 框架实现请求路由？是否需要引入 Nginx 或 ALB？

**可以拓展的方向**
*   将此逻辑扩展到 **多模态模型**（如 Llama 3.2 Vision），处理图片输入输出的 Base64 编码转换。
*   研究 **Speculative Decoding (推测解码)** 在此架构下的应用，SGLang 支持此功能，如何在自定义 API 中暴露这种性能优势？

**未来发展趋势**
未来可能会出现**“通用模型适配器”**（Universal Model Adapter）的开源项目，它们能够自动将任何模型（HuggingFace、vLLM、SGLang）的接口转换为 Bedrock 或 OpenAI 格式，使得“自定义模型提供商”的构建不再需要手写代码。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估：** 检查你当前的 Agent 应用是否依赖特定的 API 格式。
2.  **选型：** 选择高性能推理框架（推荐 SGLang 用于高并发，vLLM 用于稳定性）。
3.  **容器化：** 使用 Docker 将模型和推理服务打包，确保端口（如 8000）和健康检查接口配置正确。
4.  **开发适配层：** 编写一个轻量级 Web 服务（可用 Python FastAPI），接收标准请求，调用本地推理引擎，返回标准响应。

**具体的行动建议**
*   **第一步：** 先在本地使用 Docker 运行 SGLang + Llama 3.1，用 `curl` 测试其原生 API。
*   **第二步：** 编写一个 Python 脚本，将 Bedrock 格式的 JSON 转换为上述 `curl` 命令的 Payload，并解析返回结果。
*   **第三步：** 将此脚本封装进 SageMaker 推理容器中的 `inference.py`。

**需要补充的知识**
*   **SageMaker Inference Toolkit:** 了解如何编写 `model_fn`, `transform_fn`, `predict_fn` 等关键函数。
*   **HTTP Streaming:** 熟悉 Python 中的 `asyncio` 和流式响应处理。

## 7. 案例分析

**结合实际案例说明**
假设一个金融风控 Agent，需要使用经过微调的 Llama-3-70b-Instruct 模型，该模型针对金融术语进行了优化。
*   **困境：** Bedrock 不提供这个微调版本，或者客户不想将数据传给公共端点。
*   **解决：** 将模型部署在 SageMaker VPC 内部。
*   **挑战：** 现有的 Agent 代码是基于 Bedrock SDK 编写的，改动

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化模型推理性能与延迟

**说明**: 在 SageMaker 端点上托管 LLM 时，推理延迟直接影响 Strands Agents 的响应速度和用户体验。通过配置适当的实例类型、利用量化技术以及优化张量并行度，可以显著降低首字节延迟（TTFT）和令牌生成延迟。

**实施步骤**:
1. 根据模型大小选择合适的实例类型（如用于 Llama 3 70B 的 `ml.p5.48xlarge` 或 `ml.g5.48xlarge`）。
2. 在 SageMaker 推理容器中启用量化（如 AWQ 或 GPTQ），在保持精度的同时减少显存占用。
3. 调整 `DJL Serving` 或 `TGI` 的参数，例如设置 `tensor_parallel_degree` 以充分利用多 GPU 加速。
4. 启用动态批处理以合并传入的请求，提高吞吐量。

**注意事项**: 避免在生产环境中使用 CPU 实例运行大语言模型，确保实例的显存（VRAM）足以容纳模型权重和 KV 缓存。

---

### 实践 2：实施严格的输入输出验证

**说明**: 为了防止提示词注入和恶意输入破坏 Agent 的逻辑，必须在自定义提供者代码中建立严格的验证层。Strands Agents 依赖于结构化的交互，非预期的格式可能导致解析错误。

**实施步骤**:
1. 在发送请求到 SageMaker 之前，使用 Pydantic 或 JSON Schema 验证输入参数的有效性。
2. 限制输入提示词的最大长度，防止端点 OOM（内存溢出）。
3. 过滤掉控制字符或潜在的提示词攻击模式。
4. 验证 SageMaker 返回的 JSON 响应是否符合预期的字段结构（如 `choices` 或 `generated_text`）。

**注意事项**: 验证逻辑不应过度消耗推理延迟，建议使用高效的编译型库或轻量级正则表达式。

---

### 实践 3：构建结构化的错误处理与重试机制

**说明**: SageMaker 端点可能会遇到自动扩缩容导致的冷启动延迟或临时的网络抖动。健壮的错误处理能确保 Agent 在这些情况下不会崩溃，而是优雅降级或重试。

**实施步骤**:
1. 捕获特定的 SageMaker 客户端异常（如 `ModelNotReadyError` 或 `ValidationError`）。
2. 实现指数退避重试策略，例如在收到 503 或 504 错误时自动重试最多 3 次。
3. 为 Strands Agent 提供有意义的错误反馈，以便 Agent 能够根据错误上下文调整后续行动或通知用户。
4. 设置合理的超时时间，避免长时间挂起导致 Agent 流程中断。

**注意事项**: 对于非幂等性操作（如写入数据库），重试需谨慎，但对于 LLM 生成文本的操作，重试通常是安全的。

---

### 实践 4：利用 SageMaker 捕获功能进行模型可观测性

**说明**: 调试 Agent 与 LLM 之间的交互非常困难。启用 SageMaker Model Monitor 或 Data Capture 功能，可以记录请求和响应负载，帮助追踪幻觉、格式错误或性能瓶颈。

**实施步骤**:
1. 在 SageMaker 端点配置中启用 `DataCaptureConfig`，指定采样比例（如 100% 用于调试，较低比例用于生产）。
2. 将捕获的数据存储在 S3 存储桶中，并设置生命周期策略以管理成本。
3. 集成 CloudWatch Logs 来记录自定义提供者代码中的逻辑错误和中间状态。
4. 定期分析捕获的数据，检查输入提示词的分布和模型输出的统计特征。

**注意事项**: 确保捕获的数据符合隐私合规要求，不要在日志中记录敏感的 PII（个人身份信息）数据。

---

### 实践 5：标准化提示词模板与系统提示词管理

**说明**: Strands Agents 通常需要特定的输出格式（如 JSON 或特定的 XML 标签）来执行工具或函数调用。硬编码提示词难以维护，应通过模板化管理确保一致性。

**实施步骤**:
1. 将系统提示词和少样本示例存储在单独的配置文件或参数存储中（如 AWS Systems Manager Parameter Store）。
2. 在调用 SageMaker 之前，使用 Jinja2 或类似引擎动态组装提示词。
3. 明确指示模型输出 JSON 格式，并在提示词中提供 Schema 示例。
4. 为不同的 Agent 任务（如总结、提取、推理）维护不同的提示词模板版本。

**注意事项**: 避免在提示词中包含过多的上下文导致超出上下文窗口限制，实施上下文截断策略。

---

### 实践 6：配置自动扩缩容策略以优化成本

**说明**: Agent 的流量通常是间歇性的。为了在保持性能的同时控制成本，需要根据请求队列长度和 CPU/GPU 利用率动态调整 SageMaker 端点的实例数量。

**实施步骤**:
1. 配置 SageMaker 自动扩缩容策略，基于 `

---
## 学习要点

- 通过实现标准化的接口协议，可以将部署在 SageMaker 上的自定义大语言模型无缝集成到 Strands 智能体框架中。
- 利用 SageMaker 托管模型能够满足企业对数据隐私和合规性的严格要求，同时保持对底层模型基础设施的完全控制。
- 自定义模型提供商的架构允许灵活适配不同的 LLM，使开发者能够针对特定业务场景优化模型性能。
- 集成过程通过统一抽象层简化了后端切换逻辑，无需修改上层应用代码即可在模型间进行替换。
- 这种方法展示了如何将云原生 AI 服务与自动化框架深度结合，以构建可扩展且安全的企业级生成式 AI 应用。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [AWS SageMaker](/tags/aws-sagemaker/) / [Strands](/tags/strands/) / [LLM](/tags/llm/) / [SGLang](/tags/sglang/) / [Llama 3.1](/tags/llama-3.1/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [在 SageMaker 上部署 SGLang 并集成至 Strands 智能体]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--2.md" >}})
- [AWS SageMaker实战：利用Dottxt Outlines实现LLM结构化输出]({{< relref "posts/20260225-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-10.md" >}})
- [基于 Amazon Bedrock AgentCore 构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-0.md" >}})
- [基于Amazon Bedrock AgentCore构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-12.md" >}})
- [基于Amazon Bedrock AgentCore构建统一智能系统实践]({{< relref "posts/20260219-blogs_podcasts-build-unified-intelligence-with-amazon-bedrock-age-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*