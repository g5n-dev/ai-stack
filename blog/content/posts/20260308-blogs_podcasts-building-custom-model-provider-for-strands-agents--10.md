---
title: "在 Strands 代理中集成 SageMaker 托管的 Llama 3.1"
date: 2026-03-08T10:19:21+08:00
draft: false
entry_kind: "auto"
tags: ["AWS", "SageMaker", "Llama 3.1", "Strands", "SGLang", "LLM", "模型部署", "自定义解析器"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何为 Strands 代理构建自定义模型提供商，以便集成托管在 SageMaker AI 端点上且不原生支持 Bedrock 消息 API 格式的大语言模型（LLM）。主要步骤包括： 1. **背景说明**： 当使用 SageMaker 托管的 LLM（如 Llama 3.1）时，若其输出格式与 Bedro"
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios: ["大语言模型", "后端开发"]
---

# 在 Strands 代理中集成 SageMaker 托管的 Llama 3.1

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---
## 摘要/简介

本文演示了如何在 Strands 代理中构建自定义模型解析器，以适配托管在 SageMaker 上且不原生支持 Bedrock Messages API 格式的 LLM。我们将介绍如何使用 awslabs/ml-container-creator 在 SageMaker 上部署基于 SGLang 的 Llama 3.1，然后实现自定义解析器将其与 Strands 代理集成。

---
## 导语

在构建基于 Strands 的 AI 代理时，开发者常需对接托管在 SageMaker 上的定制化大模型，但这些模型往往不原生兼容 Bedrock 的标准 API 格式。本文将演示如何通过实现自定义模型解析器，将部署在 SageMaker 端点上的 Llama 3.1（基于 SGLang）无缝集成至 Strands 代理。读者将掌握从模型容器化部署到接口适配的完整流程，从而灵活扩展代理框架的底层模型能力。

---
## 摘要

本文介绍了如何为 Strands 代理构建自定义模型提供商，以便集成托管在 SageMaker AI 端点上且不原生支持 Bedrock 消息 API 格式的大语言模型（LLM）。主要步骤包括：

1. **背景说明**：  
   当使用 SageMaker 托管的 LLM（如 Llama 3.1）时，若其输出格式与 Bedrock 消息 API 不兼容，需通过自定义解析器实现与 Strands 代理的集成。

2. **核心流程**：  
   - **模型部署**：利用 `awslabs/ml-container-creator` 工具，在 SageMaker 上部署基于 SGLang 的 Llama 3.1 模型，确保端点可访问。  
   - **解析器开发**：编写自定义解析器，将模型输出转换为 Strands 代理可识别的格式，弥补原生 API 支持的缺失。  
   - **集成验证**：通过解析器连接 SageMaker 端点与 Strands 代理，实现功能调用与响应处理。

3. **技术要点**：  
   - 使用 SGLang 优化模型推理性能。  
   - 解析器需处理输入/输出的格式转换（如 JSON 结构适配）。  
   - 确保 SageMaker 端点与 Strands 代理的网络连通性及认证配置。

4. **应用场景**：  
   适用于需灵活部署私有 LLM 并集成到 AWS 生态系统中的企业，通过自定义适配器降低对特定 API 格式的依赖。

总结：该方案通过容器化部署、自定义解析和集成测试，实现了非标准 LLM 与 Strands 代理的无缝协作，扩展了 AWS AI 服务栈的兼容性。

---
## 评论

**中心观点**
该文章通过展示在 SageMaker 上部署 SGLang 优化的 Llama 3.1 并为 Strands Agents 构建自定义模型解析器，论证了在 AWS 生态内绕过 Bedrock 标准化限制、实现高性能与定制化控制并行的混合架构可行性。

**支撑理由与批判性分析**

1.  **技术架构的解耦与性能优化（事实陈述 + 你的推断）**
    *   **理由**：文章选择 SGLang 而非默认的 vLLM 或 DJL Serving 是一个显著的技术亮点。SGLang 的 RadixAttention 等技术在处理高并发和长文本场景下具有内存和延迟优势。结合 `awslabs/ml-container-creator`，文章实际上是在提倡一种“Infrastructure as Code”的模型部署范式，将模型运行时与上层应用逻辑解耦。
    *   **反例/边界条件**：这种解耦带来了运维复杂度的急剧上升。如果企业没有专门的 MLOps 团队，维护自定义容器（安全补丁、CUDA 版本兼容性）的成本将远超使用托管服务（如 Bedrock）的溢价。此外，SGLang 相对较新，生产环境稳定性不如 vLLAM 成熟。

2.  **对“模型路由”与“中间件层”的重新定义（作者观点 + 你的推断）**
    *   **理由**：文章的核心在于实现 `Custom Model Parser`。这实际上是在构建一个轻量级的“协议翻译层”，将非 OpenAI 兼容的底层输出转换为 Strands 框架（或 Bedrock API）能理解的标准格式。这揭示了行业趋势：企业不再满足于单一模型的黑盒调用，而是需要“模型编排”能力，即在一个 Agent 内部灵活调度不同格式的专有模型和开源模型。
    *   **反例/边界条件**：自定义解析器引入了额外的序列化/反序列化开销。对于对延迟极度敏感的实时交互场景，这种 Python 层面的解析可能成为性能瓶颈。直接修改底层服务端输出格式可能更高效，尽管这牺牲了通用性。

3.  **成本效益与数据主权的权衡（事实陈述 + 行业观点）**
    *   **理由**：通过 SageMaker 部署开源模型（Llama 3.1），企业能够利用 Spot 实例等低成本算力，并确保数据不离开 VPC（虚拟私有云）。这对于金融、医疗等受监管行业是刚需，也是对抗 Bedrock 按 Token 计费昂贵模式的有效手段。
    *   **反例/边界条件**：这种方案隐形成本极高。SageMaker 的实例成本（即使是 Spot）加上存储、网络流量及工程师维护成本，往往使得 TCO（总拥有成本）在低流量场景下高于直接调用 API。只有在高并发或大规模推理场景下，自部署才具有经济性。

**验证与检查方式**

为了验证该文章所述方案的可行性与性能，建议进行以下检查：

1.  **延迟与吞吐量基准测试**：
    *   **指标**：对比 SGLang 自定义端点与原生 Bedrock Llama 3.1 端点在相同 Prompt 长度（如 1k tokens）和生成长度（如 512 tokens）下的 Time to First Token (TTFT) 和 Total Generation Time。
    *   **实验**：使用 Locust 或 K6 进行并发压测，观察 SGLang 的 RadixAttention 在多轮对话中的显存复用率是否提升了吞吐量。

2.  **协议兼容性压力测试**：
    *   **指标**：Strands Agent 在调用自定义 Parser 时的失败率。
    *   **观察窗口**：输入边缘情况（如超长上下文、特殊字符、非结构化 JSON 输出），检查 Parser 是否能稳健地将 SGLang 的输出映射回 Bedrock Message API 格式，而不发生 JSON 解析错误。

3.  **资源利用率监控**：
    *   **指标**：SageMaker 实例的 GPU 利用率和显存占用。
    *   **观察窗口**：在冷启动和热启动状态下，观察 `ml-container-creator` 构建的环境是否存在资源泄漏。特别是连续运行 24 小时后，内存是否呈线性增长（排查 Python Parser 或 SGLang 服务的内存泄漏）。

**综合评价**

从**行业影响**来看，这篇文章虽然看似是技术教程，实则触及了当前 AI 落地的核心矛盾：**通用大模型（API）的便捷性与定制化私有部署的灵活性之间的博弈**。它为那些既希望使用 AWS 原生 Agent 框架，又希望掌握底层模型命运的技术团队提供了一条“中间道路”。

从**实用价值**而言，文章填补了 AWS 文档中的一个空白——即如何让 SageMaker 这种“裸金属”环境跑起来的模型，能够无缝接入 Bedrock 这种“豪华装修”的 Agent 生态。这对于构建企业级 RAG（检索增强生成）应用或复杂多智能体系统的开发者具有极高的参考意义。

然而，必须指出**争议点**在于过度工程化的风险。构建自定义解析器和容器意味着团队需要对 SGLang、Docker、AWS SDK 以及 Strands 框架均有深入了解。对于初创公司或快速原型验证阶段，直接调用 OpenAI 或 Bedrock API 依然是更优解。该方案更适合作为成熟期企业降本增效的“进阶选项”，而非起步的“默认配置”。

---
## 技术分析

基于您提供的文章标题和摘要，以下是对该技术方案的深入分析。文章主要探讨了在AWS生态系统中，如何将非标准接口的大语言模型（如部署在SageMaker上的Llama 3.1）集成到Strands智能体框架中。

---

# 深入分析：构建基于SageMaker托管LLM的Strands Agents自定义模型提供商

## 1. 核心观点深度解读

**主要观点：**
文章的核心观点是**“去耦合化”与“标准化适配”**。它证明了企业不应被锁定在特定的托管模型服务（如AWS Bedrock）中，即便使用像Strands这样的应用框架，也可以通过构建自定义解析器，将任何自托管或第三方托管的LLM（如通过SageMaker部署的Llama 3.1）无缝接入。

**核心思想：**
作者传达了**“基础设施灵活性优于便捷性”**的工程哲学。虽然Bedrock提供了开箱即用的API，但企业出于成本、数据隐私或定制化需求，往往选择SageMaker部署模型。文章的核心思想在于展示如何通过**“适配器模式”**来填补底层模型输出格式与上层应用框架之间的鸿沟。

**创新性与深度：**
该观点的创新性在于解决了**“中间件缺失”**的问题。通常，LLM Ops关注底层部署，App Dev关注上层逻辑，而这篇文章恰恰聚焦于中间的**“粘合层”**。它深入探讨了如何处理SGLang的高吞吐量输出与Strands Agent期望的JSON结构之间的转换，这是构建生产级AI应用的关键细节。

**重要性：**
随着企业从“玩具级”POC转向生产级部署，数据主权和成本控制变得至关重要。能够灵活切换底层模型提供商，而不改变上层Agent代码，是企业级AI架构的**必修课**。

## 2. 关键技术要点

**涉及的关键技术：**
1.  **AWS SageMaker:** 用于托管Llama 3.1模型的计算环境。
2.  **SGLang:** 一个高性能的LLM推理引擎，专为高并发和低延迟设计，比传统vLLM在某些场景下更优。
3.  **awslabs/ml-container-creator:** AWS提供的工具，用于简化构建兼容SageMaker的Docker容器。
4.  **Strands Agents:** AWS推出的智能体框架（假设为Agent应用层），通常期望Bedrock API格式。
5.  **Custom Model Parsers:** 自定义解析逻辑，用于将非标准输出转换为Agent可理解的格式。

**技术原理与实现：**
*   **容器化部署:** 利用`ml-container-creator`将Llama 3.1模型及其运行环境打包。这不仅是模型权重，还包括推理服务器（SGLang）。
*   **协议转换:** SageMaker端点通常暴露的是HTTP REST/gRPC接口，而Strands可能期望特定的JSON Schema（如`messages` API）。实现方式是在中间层（或Lambda函数）编写Python代码，拦截SGLang的原始输出，提取`text`或`tool_calls`字段，并重组为Bedrock兼容格式。
*   **流式处理:** SGLang支持流式输出，技术难点在于如何将SGLang的Server-Sent Events (SSE)流转换为Strands框架支持的流式响应格式。

**技术难点与解决方案：**
*   **难点:** 格式不兼容。SGLang默认输出可能与OpenAI/Bedrock格式不同。
*   **方案:** 实现一个Wrapper类，继承自基类Provider，重写`invoke`和`stream`方法，手动映射字段。
*   **难点:** 工具调用的解析。Agent需要调用函数，模型必须输出特定的JSON结构。
*   **方案:** 在Prompt中强制约束Llama 3.1输出JSON，并在Parser中验证和纠错。

**技术创新点：**
利用SGLang的**RadixAttention**技术（显存优化）在SageMaker上运行，结合自定义Parser，实现了比直接调用Bedrock更低的延迟和更高的吞吐量，同时保持了上层代码的整洁。

## 3. 实际应用价值

**指导意义：**
对于正在构建AI应用的企业，这篇文章提供了**“混合云AI架构”**的蓝图。你不必为了使用Bedrock的高级功能而将数据迁移出VPC，也不必为了使用SageMaker而放弃高级Agent框架。

**应用场景：**
1.  **金融/医疗合规:** 数据不能离开特定VPC或必须加密存储，必须使用SageMaker私有部署，但需要Agent能力。
2.  **极致成本优化:** 使用Spot实例在SageMaker上运行Llama 3.1，比Bedrock按需计费便宜数倍。
3.  **模型微调集成:** 微调后的模型无法直接放在Bedrock上，需部署在SageMaker，此时需要此方案接入Agent。

**注意事项：**
*   **维护成本:** 自建解析器意味着当Bedrock API更新或Strands框架变动时，你需要自行维护适配代码。
*   **延迟:** 相比Bedrock的托管服务，SageMaker端点可能涉及冷启动问题，需配置好预置实例。

**实施建议：**
不要直接硬编码解析逻辑，而是建立一个抽象层。确保你的Parser具有可测试性，能够模拟SGLang的返回进行单元测试。

## 4. 行业影响分析

**启示：**
这标志着LLM Ops正在从**“模型中心”**转向**“应用中心”**。底层模型服务正在商品化，真正的竞争力在于如何将这些模型灵活、高效地编织进业务逻辑中。

**变革：**
未来我们将看到更多**“Bento ML”**式的架构——即在一个应用中同时调用Bedrock（用于通用逻辑）、SageMaker（用于敏感/私有逻辑）和本地模型（用于极速响应）。自定义Provider将成为标准配置。

**发展趋势：**
*   **标准化协议的胜利:** OpenAI API格式正在成为事实标准。SGLang等推理引擎都在向其靠拢，这降低了构建Custom Parser的难度。
*   **推理引擎的崛起:** vLLM, SGLang, TensorRT-LLM等后端技术将比模型本身更受关注，因为它们决定了成本和体验。

## 5. 延伸思考

**拓展方向：**
*   **多模型负载均衡:** 如果一个SageMaker端点挂了，Custom Parser能否自动切换到Bedrock上的GPT-4作为备用？
*   **可观测性:** 如何追踪SageMaker端点的Token使用量和成本？自定义Provider需要集成 telemetry（如OpenTelemetry）。

**待研究问题：**
*   SGLang的结构化生成约束能力是否足以支撑复杂的Agent工具调用，还是完全依赖于Prompt Engineering？
*   在高并发下，SageMaker端点的 autoscaling 策略如何与Agent的请求速率匹配，避免冷启动导致的超时。

## 6. 实践建议

**如何应用到项目：**
1.  **评估现有模型:** 确定你的Agent是否真的需要Bedrock之外的模型（如Llama 3.1 70B或405B）。
2.  **容器化准备:** 使用`ml-container-creator`构建包含SGLang的Docker镜像，推送到ECR。
3.  **部署端点:** 在SageMaker Asynchronous Inference或Real-time Endpoints上部署。
4.  **编写Adapter:** 代码实现一个类，将SageMaker的InvokeEndpointResponse转换为Strands期望的Message格式。

**行动建议：**
*   先从流式输出入手，这是用户体验的关键。
*   务必实现错误重试机制，SageMaker端点可能比Bedrock更不稳定。

**补充知识：**
*   熟悉AWS Boto3 SDK。
*   深入理解HTTP流式传输。
*   了解JSON Schema验证。

## 7. 案例分析

**成功案例（假设场景）：**
一家Fintech公司需要分析内部PDF财报。由于数据敏感，不能发给Bedrock。他们采用此方案，在SageMaker上部署Llama 3.1，通过Custom Parser接入Strands Agent。Agent成功调用了计算工具分析财报数据，且数据未出VPC。

**失败反思：**
某团队直接在Parser中进行复杂的字符串处理来解析工具调用，导致当模型输出格式稍有变化（如多了一个空格）时，Agent崩溃。
**教训：** 使用强类型的Pydantic模型进行解析，而非正则表达式；或者在Prompt中给出极严格的JSON示例。

## 8. 哲学与逻辑：论证地图

**中心命题:**
在企业级AI应用架构中，采用**自定义模型提供商模式**将自托管LLM（如SageMaker上的Llama 3.1）集成到Agent框架（如Strands），是实现**数据主权、成本可控与高性能**三者兼顾的最优解。

**支撑理由:**
1.  **数据隐私与合规:** 依据企业合规要求，敏感数据不能传输至公共模型API，必须通过VPC内部署解决。
2.  **成本效益:** 依据云计费逻辑，SageMaker使用Spot实例或预留实例的长期运行成本，显著低于Bedrock等托管API的按Token计费模式。
3.  **性能定制化:** 依据SGLang技术特性，针对特定模型（如Llama 3.1）进行推理优化，可提供比通用API更低的延迟。

**反例 / 边界条件:**
1.  **维护开销过大:** 如果企业缺乏专业的MLOps团队，维护自定义解析器、容器更新和底层基础设施的成本可能超过购买Bedrock服务的溢价。
2.  **低流量场景:** 如果应用调用量极低，SageMaker端点的“空转成本”（即使不推理也要为实例付费）远高于Bedrock的按量付费。

**命题性质分析:**
*   **事实:** SageMaker支持自定义容器；Strands支持自定义Provider；SGLang性能优于部分通用后端。
*   **价值判断:** 数据主权和长期成本优化优于开发便捷性。
*   **可检验预测:** 采用该架构的企业，在处理百万级Token请求时，其云账单的增长率将低于直接使用Bedrock的企业，同时其数据合规审计通过率将更高。

**立场与验证:**
**立场:** 强烈支持在**中高流量、有数据合规要求**的场景下采用此架构。
**验证方式:**
*   **指标:** 对比单位Token推理成本、端到端延迟。
*   **实验:** 并行运行两套系统（一套Bedrock，一套SageMaker Custom），在相同负载下测试Agent的任务成功率和资源消耗。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 SageMaker 端点配置以实现低延迟推理

**说明**: Strands Agents 需要与大语言模型 (LLM) 进行频繁且快速的交互。SageMaker 端点的配置直接影响响应时间。如果配置不当，会导致 Agent 用户体验下降或出现超时。

**实施步骤**:
1. 根据模型大小和并发请求量，选择适当的实例类型（例如用于推理的 GPU 实例如 `ml.g5` 或 `ml.p4`）。
2. 配置 SageMaker 多模型端点 (MME) 或利用多容器端点来提高资源利用率。
3. 启用 SageMaker 的模型缓存或预编译功能（如适用于 Llama 2/3 的 Better Transformer 优化）。

**注意事项**: 避免在推理端点上同时运行繁重的训练任务。务必根据预期的每秒查询率 (QPS) 设置自动扩缩容策略，以平衡成本与性能。

---

### 实践 2：实现健壮的标准化接口适配层

**说明**: 不同的 LLM 拥有不同的输入输出格式（例如 OpenAI 兼容格式 vs. 原生 Hugging Face 格式）。为了使 Strands Agents 能够无缝调用 SageMaker 托管的模型，必须构建一个适配层来标准化请求和响应。

**实施步骤**:
1. 定义一个通用的请求/响应模式（通常参考 OpenAI API 标准，如 `ChatCompletion` 格式）。
2. 在 SageMaker 推理容器中编写预处理（将 Agent 的标准请求转换为特定模型格式）和后处理逻辑（将模型输出转换回标准格式）。
3. 确保适配层正确处理流式传输（Streaming Response），因为 Agent 通常需要逐字输出以改善用户体验。

**注意事项**: 严格验证 Token 计数和特殊 Token（如 `<EOS>`）的处理，防止 Agent 解析错误导致对话中断。

---

### 实践 3：建立严格的输入验证与安全护栏

**说明**: LLM 可能会生成意外或不安全的内容。在将数据发送给模型或将模型结果返回给 Agent 之前，必须实施验证机制，以确保系统稳定性和安全性。

**实施步骤**:
1. 在调用 SageMaker 端点之前，对 Agent 发送的 Prompt 进行长度限制和敏感词过滤。
2. 利用 SageMaker Model Monitor 监控输入数据分布和异常情况。
3. 在后处理逻辑中实施输出过滤，防止模型返回恶意代码或不当言论。

**注意事项**: 不要依赖模型自身来保证安全性。应使用独立的过滤层（如 Amazon Bedrock Guardrails 或独立的分类模型）来审查输入输出。

---

### 实践 4：实施全面的错误处理与重试机制

**说明**: 云端推理服务可能会遇到瞬时的网络问题或端点内部错误。Strands Agents 需要具备容错能力，以确保对话流程不因单次请求失败而终止。

**实施步骤**:
1. 在自定义提供程序代码中实现指数退避重试策略，专门针对 5xx 系列错误或限流错误（429）。
2. 定义清晰的错误映射，将 SageMaker 的原始错误转换为 Agent 能够理解的语义化错误（例如“服务暂时不可用”或“输入过长”）。
3. 设置合理的超时时间，既要允许长推理完成，又要防止无限期挂起。

**注意事项**: 对于非幂等请求（如写入状态的操作），重试需谨慎。确保捕获并记录详细的错误日志以便排查。

---

### 实践 5：利用提示词工程增强 Agent 上下文感知

**说明**: Strands Agents 依赖于 LLM 理解复杂的业务逻辑和上下文。仅仅托管模型是不够的，需要通过精细的提示词工程来引导模型输出符合 Agent 预期的结果。

**实施步骤**:
1. 在 SageMaker 调用层构建动态 Prompt 模板，注入 Agent 的上下文信息（如用户历史、工具描述）。
2. 为模型设定清晰的角色定义和任务约束。

**注意事项**: 注意 Prompt 的 Token 消耗。随着上下文变长，可能会触及模型的上下文窗口限制或增加推理成本和延迟。

---

### 实践 6：持续监控成本与性能指标

**说明**: 运行 LLM 的成本可能很高，且性能会随负载变化。建立监控体系对于维持 Strands Agents 的长期健康运行至关重要。

**实施步骤**:
1. 使用 Amazon CloudWatch 收集 SageMaker 端点的关键指标，如 `Invocations`（调用次数）、`ModelLatency`（模型延迟）和 `InvocationsPerInstance`（单实例并发数）。
2. 创建自定义仪表板以可视化 Token 吞吐量和成本消耗，确保资源使用在预算范围内。
3. 配置告警通知，以便在错误率飙升或延迟超过阈值时及时介入。

**注意事项**: 定期审查未使用的端点并及时删除以节省成本。同时，分析 `4xx` 和 `5xx`

---
## 学习要点

- 通过实现标准接口，可以将部署在 SageMaker 上的 LLM 无缝集成为 Strands Agents 的自定义模型提供商。
- 利用 SageMaker 托管模型能够通过集中管理基础设施和配置，显著降低大模型应用的运维复杂度。
- 自定义提供商架构支持灵活切换底层模型，从而优化特定业务场景的性能与成本效益。
- 该方案通过将 AI 应用逻辑与模型部署解耦，增强了企业级 AI 系统的可扩展性与安全性。
- 集成过程允许开发者利用 SageMaker 的企业级特性（如监控和自动扩缩容）来保障生产环境的稳定性。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [Llama 3.1](/tags/llama-3.1/) / [Strands](/tags/strands/) / [SGLang](/tags/sglang/) / [LLM](/tags/llm/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--4.md" >}})
- [为 Strands 智能体构建 SageMaker 托管 LLM 的自定义模型解析器]({{< relref "posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--10.md" >}})
- [在 SageMaker 上部署 SGLang 并为 Strands 智能体构建自定义模型解析器]({{< relref "posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*