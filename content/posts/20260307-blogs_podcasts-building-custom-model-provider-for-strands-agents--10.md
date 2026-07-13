---
title: 为 Strands 智能体构建 SageMaker 托管 LLM 的自定义模型解析器
date: 2026-03-07 22:28:45+08:00
draft: false
entry_kind: auto
tags:
- SageMaker
- Strands
- LLM
- SGLang
- Llama 3.1
- 自定义解析器
- 模型部署
- AWS
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 本文主要介绍了如何为 Strands 智能体构建自定义模型提供商，以集成托管在 Amazon SageMaker 端点上且不支持 Bedrock
  Messages API 格式的大语言模型（LLM）。文章以在 SageMaker 上使用 部署 Llama 3.1 并结合 SGLang 为例，详细讲解了如何通过实现自定义
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios:
- 大语言模型
- 后端开发
---

# 为 Strands 智能体构建 SageMaker 托管 LLM 的自定义模型解析器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---

## 摘要/简介

本文演示了在处理托管于 SageMaker 上且原生不支持 Bedrock Messages API 格式的 LLM 时，如何为 Strands 智能体构建自定义模型解析器。我们将介绍如何使用 awslabs/ml-container-creator 在 SageMaker 上部署搭载 SGLang 的 Llama 3.1，然后实现一个自定义解析器，将其与 Strands 智能体集成。

---

## 导语

在构建基于 Amazon Bedrock 的 Strands 智能体时，开发者常需整合托管于 SageMaker 的第三方大模型，但这往往受限于 API 格式不兼容的问题。本文将演示如何通过部署 SGLang 推理框架并编写自定义解析器，将 SageMaker 端点上的 Llama 3.1 模型无缝接入智能体工作流。读者将掌握处理非标准模型响应格式的具体方法，从而在异构模型架构中实现灵活的集成与调用。

---

## 摘要

本文主要介绍了如何为 Strands 智能体构建自定义模型提供商，以集成托管在 Amazon SageMaker 端点上且不支持 Bedrock Messages API 格式的大语言模型（LLM）。文章以在 SageMaker 上使用 `awslabs/ml-container-creator` 部署 Llama 3.1 并结合 SGLang 为例，详细讲解了如何通过实现自定义解析器来实现与 Strands 智能体的无缝集成。

---

## 评论

**中心观点**
本文的核心观点是：在 AWS 生成式 AI 生态中，开发者不应受限于 Amazon Bedrock 的标准化托管服务，而应通过在 SageMaker 上自部署高性能推理框架（如 SGLang）并构建自定义模型解析器，来实现对 Strands Agents 应用中底层大模型（如 Llama 3.1）的深度定制与成本优化。

**支撑理由与评价**

**1. 技术架构的解耦与灵活性（事实陈述 / 作者观点）**
文章展示了一条非常有价值的技术路径：将“模型运行时”与“应用编排层”解耦。
*   **深度评价**：Strands Agents（AWS App2DC 的演进或内部代号）通常倾向于原生 Bedrock 集成，这带来了便利但也形成了厂商锁定。文章通过引入 `awslabs/ml-container-creator` 和 SGLang，实际上是在构建一个“私有化 Bedrock”。SGLang 的引入是点睛之笔，它不仅解决了部署问题，更通过 RadixAttention 等技术解决了 LLM 在高并发场景下的显存瓶颈。这证明了在需要极高吞吐量或特定模型版本（如 Llama 3.1 特定量化版）时，自托管往往比托管服务更具技术控制力。

**2. 自定义解析器的必要性（事实陈述 / 行业共识）**
文章重点强调了处理非 Bedrock Messages API 格式的挑战，即实现“自定义模型提供者”。
*   **深度评价**：这是企业级落地中非常真实的痛点。开源模型（如 Llama 3）的输出格式（Prompt template、Completion 格式）与 Bedrock 标准化的 `messages` API 往往不兼容。通过编写 Python 中间层来转换请求/响应体，不仅解决了格式问题，还允许企业注入特定的预处理逻辑（如特定的系统提示词注入、敏感词过滤）。这种“胶水代码”虽然看似技术含量不高，但却是连接开源生态与闭源 PaaS 平台的关键桥梁。

**3. 成本效益与性能权衡（你的推断 / 作者观点）**
文章隐含了一个观点：对于大规模 Agent 部署，SageMaker + SGLang 的组合在长尾成本和延迟上可能优于 Bedrock 按需计费。
*   **深度评价**：Bedrock 虽然免运维，但单价较高。SageMaker 利用 Spot 实例或预留实例可大幅降低成本。特别是对于 Agent 应用，往往涉及大量的 Token 交换和较短的上下文，SGLang 的低延迟特性至关重要。然而，这也引入了运维复杂度，作者显然认为这种性能收益是值得投入运维成本的。

**反例与边界条件**

1.  **运维负担的激增（边界条件）**：对于初创公司或非基础设施团队，自行维护 SageMaker 端点、处理容器构建、监控 GPU 利用率以及处理 SGLang 自身的潜在 Bug，其隐性成本可能远超 Bedrock 的托管溢价。如果业务规模不大，Bedrock 的“开箱即用”仍是更优解。
2.  **模型漂移与版本管理（边界条件）**：自部署意味着你需要手动跟进 Llama 3.1 -> 3.2 的升级。文章未详细讨论模型生命周期的自动化管理。在生产环境中，一旦模型版本更新，自定义解析器若未同步适配，会导致整个 Agent 链路崩溃，而 Bedrock 则能平滑处理底层模型升级。

**行业影响与争议点**

*   **行业影响**：这篇文章实际上是 AWS 官方对“混合云 AI”策略的一种侧面印证。它承认了开源模型 + 自有算力的重要性，并给出了官方工具链的指导，有助于打破“Bedrock 是唯一出路”的认知误区，鼓励企业在 AWS 上构建更具差异化的 AI 能力。
*   **争议点**：**“重复造轮子” vs “深度定制”**。业界有观点认为，既然使用 AWS，应尽量利用托管服务以减少技术债。自行引入 SGLang 等新兴框架，虽然性能好，但生态成熟度不如 vLLM 或 Triton，且团队学习曲线陡峭。这是否属于为了优化而过度设计，取决于团队的具体技术储备。

**实际应用建议**

1.  **分阶段实施**：在开发初期，直接使用 Bedrock 或 SageMaker JumpStart 快速验证 Agent 逻辑。只有在确认了性能瓶颈（如 P99 延迟过高）或成本过高后，再迁移至 SGLang 自部署方案。
2.  **关注解析器的可扩展性**：在编写自定义 Model Provider 时，不要硬编码针对 Llama 3.1 的逻辑。建议设计成策略模式，以便未来能低成本地切换到 Mistral 或 Qwen 等其他开源模型。
3.  **建立可观测性**：SageMaker 默认监控较为基础。在接入 Agent 时，务必为 SGLang 端点添加详细的 Token 吞吐量、Time-to-first-token (TTFT) 和 GPU 显存利用率监控，以量化自部署带来的性能收益。

**可验证的检查方式**

1.  **性能基准测试（指标）**：构建一个并发测试脚本，对比 Bedrock 托管的 Llama 3.1 与 SageMaker 上 SGLang 部署的 Llama 3.1 在 `Time-to-first-token (TTFT)` 和 `Tokens-per-second` 上的表现差异。观察在并发数超过 50 时，SGLang 的吞吐量优势是否明显。
2.  **格式兼容性检查（实验）**：故意发送包含复杂

---

## 技术分析

基于您提供的文章标题和摘要，尽管原文内容不完整，但结合AWS生态、SageMaker、Strands Agents（推测为AWS Bedrock Agents或相关框架）以及Llama 3.1与SGLang的技术背景，我可以为您构建一份深度分析报告。这篇文章的核心在于**解决企业级AI应用中“模型托管与智能体框架之间的协议不兼容”问题**。

以下是详细分析：

---

### 1. 核心观点深度解读

**主要观点：**
文章主张并演示了一种**“中间件适配器模式”**，即当企业选择使用SageMaker等托管服务部署高性能开源模型（如Llama 3.1）而非直接调用商业API时，可以通过构建自定义模型解析器来填补非标准模型输出与智能体框架标准输入之间的鸿沟。

**核心思想：**
作者传达了**“基础设施解耦”**的思想。智能体的应用层应当与底层的模型实现细节解耦。企业不应因为选择了特定的部署后端（如SageMaker + SGLang）就被迫放弃使用高级智能体框架（如Strands Agents），也不应为了适配框架而牺牲模型的性能特性。

**创新性与深度：**
*   **创新性：** 将SGLang（一种高性能推理服务）与AWS SageMaker深度集成，并解决了与上层Agent协议的兼容问题，这是一种典型的**全栈优化思维**。它不仅关注“怎么跑起来”，更关注“怎么跑得快且用得顺”。
*   **深度：** 文章触及了LLM Ops中的深水区——**协议标准化与异构模型管理**。它揭示了当前LLM生态中“模型格式碎片化”的痛点，并给出了工程化的解决路径。

**重要性：**
随着企业从“原型验证”走向“生产部署”，成本控制和数据隐私成为首要考量，直接调用OpenAI或Bedrock API可能不再适用。企业需要将Llama 3.1等开源模型部署在私有环境（VPC内部）。然而，智能体框架通常期望特定的API格式（如Bedrock Messages API）。这篇文章提供的方案是**企业级AI落地“最后一公里”**的关键技术拼图。

---

### 2. 关键技术要点

**涉及的关键技术：**
1.  **SGLang:** 一种高性能的大语言模型推理服务引擎，以其高吞吐和低延迟著称，特别适合处理复杂的结构化输出。
2.  **AWS SageMaker:** AWS提供的机器学习模型托管平台，支持自定义容器。
3.  **awslabs/ml-container-creator:** AWS Labs提供的工具，用于简化构建兼容SageMaker的推理容器。
4.  **Strands Agents (推测):** 指代AWS Bedrock Agents或类似的Agent编排框架，依赖标准的Messages API格式。
5.  **Llama 3.1:** Meta发布的最新开源大模型系列，支持大规模上下文和工具调用。

**技术原理与实现：**
*   **部署层：** 利用`ml-container-creator`将SGLang引擎和Llama 3.1模型打包成Docker容器，部署在SageMaker上。SGLang负责优化模型推理（如KV Cache管理、RadixAttention）。
*   **适配层：** 这是文章的核心。SageMaker endpoint通常暴露的是OpenAI兼容格式或HuggingFace格式，而Strands Agents可能需要Bedrock原生格式。文章通过编写一个**Custom Model Parser（自定义模型解析器）**，拦截Agent的请求，转换为SGLang/Llama理解的格式，并将模型的原始输出解析回Agent框架需要的结构化数据（如JSON格式的工具调用参数）。

**技术难点与解决方案：**
*   **难点：** Llama 3.1虽然支持Function Calling，但其原生输出格式（JSON schema）与Bedrock的`toolUse`块结构不同。直接连接会导致Agent无法解析工具调用指令。
*   **方案：** 实现一个转换层，将Bedrock的`toolConfig`映射到Llama 3.1的Prompt模板中，并在响应端将模型生成的JSON反序列化为Agent框架的标准响应对象。

**技术创新点：**
*   **结构化输出的端到端打通：** 结合SGLang对结构化生成的约束能力和自定义解析器，确保了Agent在调用工具时的准确性和稳定性，避免了传统正则匹配解析JSON的错误率。

---

### 3. 实际应用价值

**指导意义：**
对于正在构建AI Agent应用但受限于商业API成本或隐私合规的企业，这篇文章提供了一条**“最佳实践路径”**：即利用开源模型获得商业级API的功能体验（特别是Function Calling能力）。

**应用场景：**
1.  **金融/医疗分析：** 数据敏感，不允许出公网，需在VPC内部署Llama 3.1，并使用Agent进行报表分析或辅助诊断。
2.  **企业级知识库问答：** 需要极高的并发吞吐量（SGLang优势），且Agent需要调用企业内部API查询订单或库存。

**注意问题：**
*   **冷启动延迟：** SageMaker endpoint可能会遇到自动扩缩容带来的冷启动问题。
*   **维护成本：** 自定义解析器意味着需要随着模型版本的更新而维护代码，不像使用Bedrock托管服务那样“无感升级”。

**实施建议：**
*   优先在模型侧进行Prompt Engineering，确保模型能稳定输出符合Schema的JSON。
*   在解析器层增加重试机制和异常捕获，防止模型输出畸形JSON导致Agent崩溃。

---

### 4. 行业影响分析

**行业启示：**
这标志着LLM基础设施正在从**“寡头垄断API”**向**“多元化混合部署”**转型。企业不再满足于单一模型供应商，而是倾向于根据任务难度、成本和隐私要求，动态切换模型后端。**“模型路由”**和**“协议适配”**将成为AI工程栈的核心能力。

**带来的变革：**
*   **MaaS (Model as a Service) 的边界模糊：** 未来的MaaS将不再局限于API调用，任何托管在Kubernetes或SageMaker上的模型都可以通过适配层无缝接入到Agent框架中。
*   **推理引擎的崛起：** SGLang、vLLM等推理后端的重要性日益凸显，它们成为了模型性能的倍增器。

**发展趋势：**
*   **标准化协议的普及：** 虽然现在需要自定义解析器，但长远来看，OpenAI的Messages API格式正在成为事实上的行业标准。大多数推理引擎（SGLang, vLLM）和框架都在向此靠拢。

---

### 5. 延伸思考

**引发思考：**
*   **性能与精度的权衡：** SGLang虽然快，但在处理极其复杂的逻辑推理时，量化后的模型是否还能保持与全精度模型（如GPT-4）相当的Tool Calling准确率？
*   **可观测性：** 当我们引入了自定义解析器层，如何追踪请求从Agent到SGLang的完整链路？如何调试Prompt转换过程中的信息损失？

**拓展方向：**
*   **多模型负载均衡：** 在自定义解析器中增加逻辑，简单请求走小模型，复杂请求走大模型，对上层Agent透明。
*   **流式传输的适配：** 文章可能侧重于同步调用，但在实际对话场景中，如何适配流式输出的Tool Call是一个更复杂的工程挑战。

---

### 6. 实践建议

**如何应用到项目：**
1.  **评估现状：** 检查你的Agent框架是否支持自定义Provider。如果是LangChain，检查`BaseLLM`类；如果是AWS Bedrock Agents，检查如何配置Proxy。
2.  **搭建环境：** 使用`ml-container-creator`构建一个包含vLLM或SGLang的Docker镜像，先在本地用Curl测试Llama 3.1的Function Calling能力。
3.  **编写适配器：** 编写一个Python类，实现`invoke`和`stream`方法。内部逻辑包括：接收标准请求 -> 转换Prompt -> 调用SageMaker -> 解析JSON -> 返回标准响应。

**行动建议：**
*   不要从零开始写解析器，参考LangChain或LlamaIndex社区中关于SageMaker集成的现有Connector代码。
*   重点关注Prompt Template的转换，Llama 3.1有特定的Function Calling Prompt格式（如`<|python_tag|>`），错误的格式会导致模型失效。

**补充知识：**
*   深入理解OpenAPI Specification (Swagger)，因为Function Calling本质上就是将API Schema转化为模型可读的文本。
*   学习Docker和Kubernetes网络，因为SageMaker endpoint的调试往往比本地调试复杂。

---

### 7. 案例分析

**成功案例（基于技术逻辑推演）：**
*   **案例：** 某电商公司构建“智能订单助理”。
*   **做法：** 部署Llama 3.1 70B在SageMaker上，使用SGLang加速。通过自定义解析器，将Bedrock Agents的意图转换为对内部订单系统的SQL查询。
*   **成功原因：** 相比使用GPT-4，成本降低了70%，且数据未离开VPC。SGLang保证了在大促期间的高并发响应。

**失败反思：**
*   **潜在失败点：** 忽略了模型的“幻觉”问题。
*   **场景：** 模型生成了一个看似合法但参数错误的JSON（例如将`product_id`填为了字符串而非数字）。
*   **教训：** 自定义解析器必须包含**严格的JSON Schema验证**（如使用Pydantic），如果解析失败，应触发模型重试，而不是直接抛出异常给用户。

---

### 8. 哲学与逻辑：论证地图

**中心命题:**
在企业级AI架构中，通过构建**自定义协议适配层**来连接**高性能自托管推理服务（如SGLang on SageMaker）**与**标准化智能体框架**，是实现**成本效益、数据主权与开发效率**三者平衡的最优解。

**支撑理由:**
1.  **成本与性能:** 理由：SGLang等开源推理引擎提供了比商业API更优的性价比和吞吐量。依据：Benchmark数据显示SGLang在Llama 3.1上的推理速度显著高于标准TGI。
2.  **功能对等:** 理由：Llama 3.1等开源模型已具备接近GPT-4级别的指令遵循和工具调用能力。依据：LMSYS Chatbot Arena排行榜及Meta技术报告。
3.  **架构灵活性:** 理由：自定义解析器消除了供应商锁定，允许企业随时切换底层模型或部署平台，而无需重写上层Agent逻辑。依据：软件工程中的“依赖倒置原则”（DIP）。

**反例/边界条件:**
1.  **极低延迟要求:** 如果业务要求<100ms的端到端延迟，自建SageMaker架构可能受限于网络开销，不如使用边缘计算或商业API的全局CDN节点。
2.  **极高精度要求:** 在高风险场景（如医疗诊断），开源模型的微调版可能仍不如GPT-4等顶尖闭源模型稳定，此时适配层做得再好也无法弥补模型能力的差距。

---

## 最佳实践

### 实践 1：优化 SageMaker 端点配置以实现低延迟推理

**说明**:
Strands Agents 需要与大语言模型 (LLM) 进行频繁且快速的交互。为了确保用户体验流畅，必须最小化推理延迟。SageMaker 端点的配置直接影响响应速度，包括实例类型、模型量化程度以及并发处理能力。

**实施步骤**:
1.  **选择合适的实例类型**：对于推理工作负载，推荐使用支持 GPU 的实例（如 `ml.g5` 或 `ml.p4`），而非 CPU 实例，以获得最佳吞吐量。
2.  **应用模型量化技术**：在部署模型到 SageMaker 之前，使用量化技术（如 AWQ 或 GPTQ）压缩模型，这可以显著减少显存占用并提高推理速度，而对精度影响极小。
3.  **配置多模型端点 (MME)**：如果需要运行多个小型模型，利用 SageMaker 多模型端点功能在同一个 GPU 实例上加载多个模型，优化资源利用率。

**注意事项**:
*   监控 CloudWatch 指标中的 `ModelLatency`，确保其保持在 Agent 可接受的范围内（通常建议低于 2 秒）。
*   避免在生产环境中使用 `ml.t2` 或 `ml.t3` 等突发型实例，因为它们可能导致性能不稳定。

---

### 实践 2：实现健壮的输入输出数据转换逻辑

**说明**:
Strands Agents 使用特定的消息格式与模型交互，而不同的 LLM（如 Llama 3, Mistral, Falcon）在 SageMaker 上可能期望不同的负载格式（JSON 结构、Prompt 模板）。自定义提供商必须充当适配器，处理请求和响应的序列化与反序列化。

**实施步骤**:
1.  **标准化 Prompt 模板**：在代码中为特定模型定义明确的 Prompt 模板（例如：将 Agent 的系统消息和用户消息转换为模型所需的特定指令格式）。
2.  **处理 Token 限制**：在发送请求前，检查输入文本的 Token 长度。如果超过模型的上下文窗口，实施截断或摘要策略，防止 SageMaker 端点返回错误。
3.  **流式响应解析**：如果 Agent 需要流式输出，确保自定义提供商能够正确解析 SSE (Server-Sent Events) 流，并将增量 Token 实时回传给 Agent。

**注意事项**:
*   严格处理 API 调用可能引发的异常（如 `ModelError` 或 `ValidationError`），防止因格式错误导致 Agent 进程崩溃。
*   确保返回给 Agent 的响应包含 `finish_reason` 字段，以便 Agent 判断模型是否完成了思考。

---

### 实践 3：建立全面的错误处理与自动重试机制

**说明**:
云环境中的网络波动或端点暂时不可用是不可避免的。为了确保 Strands Agents 的可靠性，自定义模型提供商必须具备从瞬态故障中恢复的能力，避免因单次请求失败而中断整个 Agent 任务链。

**实施步骤**:
1.  **实施指数退避重试**：在调用 SageMaker `invoke_endpoint` API 时，配置重试策略。建议初始等待时间为 1 秒，最大重试次数为 3 次，每次重试的等待时间指数增加。
2.  **区分错误类型**：捕获特定的 SageMaker 错误（如 `ServiceUnavailable`, `ModelTimeout`）进行重试；对于客户端错误（如 `ValidationError`, `ResourceLimitExceeded`），则应立即停止重试并记录日志。
3.  **定义降级策略**：当主端点持续失败时，设计逻辑将请求路由到备用端点或返回一个预设的安全响应，告知用户当前服务暂时不可用。

**注意事项**:
*   不要无限重试，这可能导致请求堆积并耗尽 SageMaker 端点的并发配额。
*   在重试逻辑中包含“断路器”模式，如果端点在短时间内连续失败多次，则在一段时间内暂停向其发送流量。

---

### 实践 4：利用 Trace 和日志记录进行可观测性

**说明**:
调试 Agent 与 LLM 之间的交互非常困难，因为涉及多轮对话和工具调用。通过集成 AWS X-Ray 和 CloudWatch Logs，可以追踪请求的全链路路径，快速定位性能瓶颈或幻觉问题。

**实施步骤**:
1.  **启用 AWS X-Ray 追踪**：在 SageMaker 端点配置中开启数据捕获，并在自定义提供商代码中注入 Trace Headers，以便在 X-Ray 控制台中查看从 Agent 到端点的完整调用链。
2.  **结构化日志记录**：记录每次请求的关键信息，包括：输入 Prompt 的摘要（注意脱敏）、生成的首个 Token 延迟、总延迟以及模型返回的原始文本。
3.  **关联日志与 Agent 会话**：在日志中包含 `session_id` 或 `conversation_id`，以便能够将特定的模型输出与用户的 Agent 会话历史关联起来。

---

## 学习要点

- 通过构建自定义模型提供商，Strands Agents 能够集成部署在 SageMaker AI 端点上的托管 LLM，从而实现更灵活的模型选择与控制。
- 利用 Amazon Bedrock 的自定义模型集成功能，可以将 SageMaker 托管的模型无缝接入 Strands 框架，无需修改底层代理逻辑。
- 实现自定义提供商需要配置模型端点、身份验证及推理参数，确保与 Strands Agents 的 API 规范兼容。
- 该方法支持动态模型切换，允许根据任务需求（如延迟、成本或性能）选择不同的 SageMaker 托管模型。
- 通过 SageMaker AI 托管 LLM，可优化数据隐私与合规性，尤其适合对敏感数据处理有严格要求的场景。
- 集成过程需关注模型响应格式的一致性，以确保 Strands Agents 能正确解析和执行生成的指令。
- 该方案为混合部署架构提供基础，未来可扩展支持多区域或多云端的模型端点。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [SageMaker](/tags/sagemaker/) / [Strands](/tags/strands/) / [LLM](/tags/llm/) / [SGLang](/tags/sglang/) / [Llama 3.1](/tags/llama-3.1/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [AWS](/tags/aws/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--4.md" >}})
- [在 SageMaker 上部署 SGLang 并为 Strands 智能体构建自定义模型解析器]({{< relref "posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--9.md" >}})
- [为 Strands 智能体构建 SageMaker 托管 LLM 自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--9.md" >}})
