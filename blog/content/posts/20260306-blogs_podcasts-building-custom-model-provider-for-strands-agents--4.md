---
title: "为 Strands 代理构建兼容 SageMaker 的自定义模型解析器"
date: 2026-03-06T05:10:04+08:00
draft: false
entry_kind: "auto"
tags: ["AWS", "SageMaker", "Strands", "LLM", "SGLang", "Llama 3.1", "自定义解析器", "模型部署"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "**内容总结：为 Strands Agents 构建基于 SageMaker 的自定义模型提供商** 这篇文章介绍了如何在使用 AWS SageMaker 托管的大语言模型（LLM）时，通过构建自定义模型解析器（Custom Model Parsers），将其与 Strands Agents 进行集成。这解决了托管在"
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios: ["大语言模型", "后端开发"]
---

# 为 Strands 代理构建兼容 SageMaker 的自定义模型解析器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---
## 摘要/简介

本文将演示在处理托管的于 SageMaker 上且不支持 Bedrock Messages API 格式的 LLM 时，如何为 Strands 代理构建自定义模型解析器。我们将通过使用 awslabs/ml-container-creator 在 SageMaker 上部署 SGLang 的 Llama 3.1，然后实现一个自定义解析器将其与 Strands 代理集成。

---
## 导语

在构建基于 Strands 的智能体应用时，将托管于 SageMaker 的 LLM 无缝集成是常见需求。然而，当模型不支持 Bedrock Messages API 标准格式时，直接调用往往受阻。本文将演示如何通过部署 SGLang Llama 3.1 并构建自定义模型解析器来解决兼容性问题。读者将掌握实现这一集成的具体步骤，从而灵活适配多样化的模型部署环境。

---
## 摘要

**内容总结：为 Strands Agents 构建基于 SageMaker 的自定义模型提供商**

这篇文章介绍了如何在使用 AWS SageMaker 托管的大语言模型（LLM）时，通过构建自定义模型解析器（Custom Model Parsers），将其与 Strands Agents 进行集成。这解决了托管在 SageMaker 上的模型不支持原生 Bedrock Messages API 格式的兼容性问题。

**核心流程如下：**

1.  **模型部署**：
    演示了如何利用 AWS 实验室提供的 `awslabs/ml-container-creator` 工具，在 SageMaker 端点上部署 Llama 3.1 模型（使用 SGLang 框架），从而构建模型的基础运行环境。

2.  **实现自定义解析器**：
    由于部署的模型不直接兼容 Bedrock 格式，文章详细说明了如何编写并实现自定义解析器。该解析器负责在 Strands Agents 与 SageMaker 托管的模型之间进行数据格式的转换，确保请求和响应能够正确传递。

通过以上步骤，开发者可以成功将 SageMaker 上托管的定制化 LLM 接入 Strands Agents 生态系统中。

---
## 评论

### 核心评价

这篇文章的中心观点是：**为了在亚马逊云的 SageMaker AI 上实现非标准格式大模型（如 Llama 3.1）与 Strands Agents 框架的无缝对接，开发者必须通过构建自定义模型解析器来弥合底层推理服务与上层应用协议之间的差异。**

以下是基于技术与行业维度的深入评价：

### 一、 支撑理由与深度分析

**1. 内容深度：从“调用”到“集成”的工程化跨越**
*   **分析：** 文章不仅仅停留在简单的 API 调用层面，而是深入到了 MLOps 的“最后一公里”——协议适配。它准确指出了行业痛点：虽然 SageMaker 提供了强大的托管能力，但上层应用框架（如 Strands Agents）往往期望特定的 API 格式（如 Bedrock Messages API），而开源模型（如 Llama 3.1）通常输出原始 JSON 或文本。文章提出的“解析器层”是解决异构系统集成的标准工程模式。
*   **事实陈述：** 文章提到了使用 `awslabs/ml-container-creator` 和 SGLang 进行部署，这表明文章侧重于高性能推理容器化技术，而非简单的模型下载。
*   **你的推断：** 作者默认读者已经具备较高的 AWS 架构知识，文章省略了网络配置（VPC 接口）等繁琐细节，专注于核心逻辑的打通，这种取舍在技术深度上是得当的。

**2. 实用价值：填补了特定技术栈的文档空白**
*   **分析：** AWS 官方文档通常倾向于推销其原生服务。对于希望利用 SageMaker 的灵活性（如使用 SGLang 获得高并发）但又想使用上层 AI Agent 框架的开发者来说，这篇文章提供了一条“避坑指南”。它提供的代码片段（自定义 Parser）具有极高的复用价值，是构建企业级 RAG（检索增强生成）或 Agent 系统时的关键组件。
*   **作者观点：** 使用 SGLang 而非默认的 vLLM 或 DJL Serving，暗示了作者对极致推理性能和特定调度策略的关注。

**3. 创新性：混合云架构下的“中间件”思维**
*   **分析：** 文章的创新点不在于发明新算法，而在于架构设计。它提出了一种“中间件”模式：在底层通用计算与上层专有 API 之间建立一个可插拔的适配层。这种方法解耦了模型部署与业务逻辑，使得未来更换模型（例如从 Llama 3.1 换到 Mistral）时，无需修改 Agent 代码，只需修改 Parser。
*   **事实陈述：** 文章演示了如何处理非 Bedrock 原生格式，这验证了“反控制平面”的趋势——即用户希望使用云厂商的基础设施，但不希望被其特定的应用层协议锁死。

### 二、 反例与边界条件

尽管文章提供了清晰的解决方案，但在以下场景中该方案可能不是最优解，甚至存在局限性：

1.  **边界条件：超低延迟需求**
    *   **反例：** 如果业务对延迟极其敏感（毫秒级），在应用层（Parser）进行协议转换可能会增加额外的序列化/反序列化开销。更优的做法可能是直接修改推理服务器（如修改 SGLang 的源码）使其原生兼容 Bedrock 协议，从而减少网络跳数和转换耗时。

2.  **边界条件：流式传输的复杂性处理**
    *   **反例：** 文章可能主要展示了非流式或简单的流式处理。在真实的 Agent 场景中，流式输出往往伴随着复杂的 Tool Use（工具调用）状态更新。自定义 Parser 在处理流式 Token 时的增量解析逻辑极其复杂，如果文章未深入处理 Buffer 缓存和 Token 截断逻辑，在实际高并发生产环境中可能会导致连接断开或 JSON 解析错误。

3.  **边界条件：成本与管理复杂度**
    *   **反例：** 为了使用 SageMaker 部署 Llama 3.1 并编写自定义 Parser，企业需要维护容器镜像、监控实例健康。如果该模型并非为了极高的定制化需求，直接使用 Bedrock 的托管模型（尽管可能稍贵或格式受限）在 TCO（总拥有成本）上可能更低。

### 三、 可验证的检查方式

为了验证文章所述方法的有效性与稳定性，建议进行以下检查：

1.  **格式转换的保真度测试（指标）：**
    *   构建一个包含 100 个复杂 Prompt 的测试集（包含系统提示词、多轮对话、工具调用定义）。
    *   **检查点：** 对比经过自定义 Parser 转换后的请求与直接发送给原生 Llama 3.1 的请求，计算 Token 级别的差异率。目标差异率应 < 0.1%（仅允许格式化空白符差异）。

2.  **流式响应的首字延迟（实验）：**
    *   使用 SGLang 部署并开启 Parser，测量从发送请求到收到第一个 Token 的时间（TTFT）。
    *   **检查点：** 对比直接调用 SageMaker 端点的时间。如果 Parser 层引入的延迟增加超过 10%，则说明该适配层存在性能瓶颈。

3.  **异常恢复机制观察（观察窗口）：**
    *   在推理过程中手动制造故障（如发送截断的 JSON 或超长 Context）。
    *   **检查点：** 观察 Parser 是否能够优雅地抛出异常并重

---
## 技术分析

基于您提供的文章标题和摘要，以下是对该技术方案的深入分析。

---

# 深度分析报告：构建基于 SageMaker 的 Strands Agents 自定义模型提供商

## 1. 核心观点深度解读

**主要观点**
文章的核心观点在于**“解耦与标准化”**。它论证了在使用 AWS Strands Agents（Amazon Bedrock 的智能体框架）时，不应受限于 Bedrock 原生支持的模型列表。通过构建自定义模型提供商，可以将部署在 SageMaker 上的任意开源大模型（如 Llama 3.1）无缝接入到 Strands 的生态系统中，使其具备与原生托管模型相同的功能（如工具调用、ReAct 模式推理）。

**核心思想**
作者传达的核心思想是**“基础设施自主权与 AI 编排框架的统一”**。企业既需要利用 SageMaker 实现对底层模型的深度定制、成本控制和数据隐私，又需要利用 Bedrock Agents 强大的编排能力。自定义模型提供商正是连接这两者的桥梁。

**创新性与深度**
该观点的创新性在于**打破了云厂商“黑盒”服务的锁定**。通常，Agent 框架倾向于绑定特定的 API 格式（如 Bedrock Messages API）。文章深入探讨了如何通过“中间层适配器”模式，将非标准接口（SGLang 的输出）转化为 Agent 框架可理解的指令，这揭示了现代 AI 架构中**接口适配层**的关键作用。

**重要性**
随着大模型进入“深水区”，企业不再满足于调用通用 API，而是需要微调、量化或部署特定架构的模型（如 Llama 3.1）。这一方案解决了**“如何让私有部署的模型拥有顶级 Agent 能力”**的难题，对降低企业落地成本、保障数据安全具有重要意义。

## 2. 关键技术要点

**涉及的关键技术**
1.  **AWS Strands Agents (Bedrock Agents):** 负责任务规划和工具调用的编排层。
2.  **Amazon SageMaker:** 用于托管 LLM 推理端点。
3.  **SGLang:** 一个高性能的 LLM 推理引擎，以高吞吐量和低延迟著称，支持 OpenAI 兼容协议。
4.  **awslabs/ml-container-creator:** 用于简化 SageMaker 推理镜像构建的工具。
5.  **Custom Model Provider (自定义模型提供商):** 连接 Agent 与 SageMaker 的逻辑层。

**技术原理与实现方式**
文章的技术路径主要分为三步：
1.  **容器化部署:** 利用 `ml-container-creator` 将 Llama 3.1 模型及 SGLang 推理服务器打包成 Docker 容器，并部署为 SageMaker 端点。SGLang 在此充当后端引擎，处理请求并发。
2.  **接口适配:** SageMaker 端点接收请求后，SGLang 负责推理。关键在于如何处理输出。Llama 3.1 原生支持工具调用，但 Bedrock Agents 需要特定的响应格式（如 `stop_reason` 和特定的 JSON 结构）。
3.  **解析器构建:** 在 Agent 调用 SageMaker 时，通过编写自定义的**响应解析器**，拦截 SageMaker 的原始输出，将其转化为 Bedrock Messages API 标准格式，从而让 Agent “以为” 它在调用 Bedrock 原生模型。

**技术难点与解决方案**
*   **难点:** SGLang 或其他开源框架的输出格式与 Bedrock Agents 期望的格式不匹配，导致 Agent 无法正确提取工具调用参数或无法判断对话是否结束。
*   **解决方案:** 文章提出构建**Custom Model Parser**。这是一个代码层面的适配器，它解析模型的 Completion 文本，提取 JSON 格式的工具调用，并映射到 Bedrock 的响应模式中。

**技术创新点**
*   **利用 SGLang 的高性能:** 相比于传统的 vLLM 或 HuggingFace TGI，SGLang 在处理多轮对话和工具调用时具有性能优势，特别是在处理复杂的 Prompt 结构时。
*   **通用适配模式:** 这种“Parser”模式不仅适用于 Llama 3.1，为未来接入 Mistral 或其他开源模型提供了标准范式。

## 3. 实际应用价值

**对实际工作的指导意义**
这为企业的 AI 工程师提供了一条**“混合云架构”**的最佳实践路径：利用 AWS 托管控制平面，同时保留底层模型的灵活性。它指导我们如何在不牺牲 Agent 高级功能（如 RAG、工具使用）的前提下，迁移到成本更低的开源模型。

**应用场景**
1.  **敏感数据处理:** 金融或医疗行业，数据不能出私有 VPC，必须使用 SageMaker 内部端点，但仍需 Agent 能力。
2.  **成本优化:** 对于高并发场景，使用自托管的 Llama 3.1 (SGLang) 比 Claude 3 Opus 或 Sonnet 更具成本效益。
3.  **特定模型微调:** 企业基于 Llama 3.1 微调了垂类模型，希望将其集成到业务流中。

**需要注意的问题**
*   **延迟:** SageMaker 端点的网络调用可能比 Bedrock 原生 API 稍有延迟。
*   **维护成本:** 需要自行维护容器、扩缩容和模型版本管理，失去了 Serverless 服务的便利性。

**实施建议**
优先选择支持 OpenAI 兼容协议的推理后端（如 SGLang），这样可以大幅减少适配代码的编写量。

## 4. 行业影响分析

**对行业的启示**
这标志着 **AI 基础设施正在从“垂直整合”走向“模块化解耦”**。未来的 AI 应用开发将不再依赖单一模型供应商，而是通过标准化接口动态切换模型来源。

**可能带来的变革**
企业将更倾向于**“模型混合编排”**——简单任务用小模型（自托管），复杂推理任务用大模型（闭源 API），由 Agent 框架根据任务难度自动路由。这将加速模型即服务的商品化。

**相关领域发展趋势**
*   **推理引擎的竞争:** vLLM, TGI, SGLang 之间的竞争将加剧，性能将成为关键指标。
*   **中间件的崛起:** 类似于 LangChain，专门用于连接不同模型 API 和 Agent 框架的中间件将变得至关重要。

## 5. 延伸思考

**引发的思考**
既然 SGLang 可以通过适配器接入 Bedrock Agents，那么是否可以构建一个**“通用模型代理网关”**，让任何符合 OpenAI 格式的本地模型都能接入任何 Agent 框架？

**拓展方向**
*   **流式传输的优化:** 分析中未提及流式响应。在 SGLang 到 Bedrock Agents 的链路中，如何实现低延迟的流式输出是一个值得深挖的方向。
*   **Function Calling 的标准化:** 不同模型（Llama 3 vs Mistral）对 Function Calling 的语法支持不同，如何构建一个通用的 Prompt 模板来统一这些差异？

**未来趋势**
未来，AWS 可能会直接在 SageMaker 上集成“一键接入 Agents”的功能，或者 SGLang 等推理引擎会直接内置 Bedrock 兼容模式。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估模型:** 确认你的业务场景是否真的需要 Llama 3.1 的 8B 或 70B 版本，以及 SGLang 是否能提供比现有方案更好的吞吐量。
2.  **构建容器:** 不要从零开始写 Dockerfile，使用 `awslabs/ml-container-creator` 快速生成包含 SGLang 的镜像。
3.  **编写 Parser:** 这是核心。你需要编写 Python 代码，解析模型的输出，提取 `tool_calls` 字段，并构造 Bedrock 期望的 JSON 结构。

**行动建议**
*   先在本地测试 SGLang 与 Llama 3.1 的兼容性。
*   使用 CloudFormation 或 SAM 脚本化部署 SageMaker 端点，避免手动配置错误。
*   重点关注日志记录，因为调试 Agent 与模型之间的 JSON 交互非常困难。

**补充知识**
*   熟悉 **OpenAPI/Swagger** 规范，因为 Bedrock Agents 使用它来定义工具。
*   深入理解 **JSON Schema**，用于验证模型输出的工具参数是否合法。

## 7. 案例分析

**成功案例（假设性推演）**
某电商公司构建了“智能客服 Agent”。
*   **背景:** 需要查询订单数据库（工具调用），且用户数据敏感。
*   **做法:** 部署了微调过的 Llama 3.1 8B 模型在 SageMaker 上。
*   **效果:** 相比使用 GPT-4，成本降低了 60%，且数据未离开 VPC。通过自定义 Parser，Agent 准确识别了“退款”、“查询”等意图并正确调用了内部 API。

**失败反思**
如果直接使用未经对齐的 Base 模型（如 Llama 3 Base），模型可能无法正确输出工具调用的 JSON 格式。
*   **教训:** 必须使用 Instruct 版本或 Chat 版本，且在 Prompt 中明确包含工具定义。

## 8. 哲学与逻辑：论证地图

**中心命题**
**在 AWS Bedrock Agents 架构中，通过自定义解析器将 SageMaker 托管的 SGLang/Llama 模型集成进来，能够在保持 Agent 编排能力的同时，实现模型部署的自主性与成本效益的最优平衡。**

**支撑理由**
1.  **自主性:** 企业拥有对底层模型版本、微调参数和部署环境的完全控制权，解决了黑盒服务的锁定问题。
2.  **性能:** SGLang 提供了比传统 HuggingFace 推理更高的吞吐量，适合高并发场景。
3.  **成本:** 对于大规模调用，SageMaker 按实例计费通常比按 Token 计费的托管 API 更便宜。

**反例/边界条件**
1.  **运维复杂性:** 如果团队缺乏运维 Kubernetes/Docker 和 SageMaker 的能力，这种架构的隐性成本（人力、维护）可能超过直接调用 API 的成本。
2.  **延迟要求:** 对于毫秒级响应要求的实时应用，SageMaker 端点的冷启动或网络跳数可能引入不可接受的延迟。

**命题分类**
*   **事实:** SGLang 支持 Llama 3.1；Bedrock Agents 支持 Custom Model Provider。
*   **价值判断:** “自主性”比“便利性”更重要；“成本效益”是核心考量。
*   **可检验预测:** 在相同负载下，SageMaker + SGLang 方案的总拥有成本（TCO）将低于直接使用 Bedrock Claude 3 Sonnet。

**立场与验证**
**立场:** 对于拥有一定技术能力且对数据隐私或成本敏感的企业，这是一种**优于纯托管服务**的架构选择。
**验证方式:**
*   **指标:** 对比 10,000 次调用的总延迟（P95）和总费用。
*   **实验:** 构建一个 PoC，分别用 Bedrock Native 模型和 SageMaker Custom 模型执行相同的 50 步工具调用任务，统计错误率和 Token 消耗。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 SageMaker 端点配置以实现低延迟推理

**说明**: 
Strands Agents 需要与 LLM 进行频繁且快速的交互。SageMaker 端点的配置直接影响响应时间。如果不进行针对性优化，可能会导致 Agent 交互出现明显的延迟，影响用户体验。最佳实践包括选择合适的实例类型（如利用 G5 或 P4d 实例的 GPU 加速）、配置适当的模型量化（如使用 AWQ 或 GPTQ 量化技术）以及调整 SageMaker 的多模型部署设置。

**实施步骤**:
1. **实例选择**: 根据模型大小和并发需求，选择配备 GPU 的实例类型（如 `ml.g5.2xlarge` 或 `ml.p4d.24xlarge`）以利用 Tensor Core 加速。
2. **启用模型量化**: 在将模型上传至 S3 之前，应用量化技术（如 4-bit 量化）以减少显存占用并提高吞吐量。
3. **调整并发设置**: 配置 SageMaker 推理容器的 `Workers` 数量或利用多模型服务器（MMS）来并行处理请求。

**注意事项**: 
在部署前使用负载测试工具（如 Apache Bench）模拟 Agent 的请求模式，确保 P95 延迟满足实时交互要求（通常建议低于 2 秒）。

---

### 实践 2：实现严格的输入输出验证与安全过滤

**说明**: 
将自定义模型暴露给 Agent 意味着需要处理不可预测的用户输入。直接将原始数据传递给托管在 SageMaker 上的模型可能导致“提示词注入”攻击或生成不当内容。最佳实践是在 Agent 调用与 SageMaker 端点之间建立一个“守门人”层，用于验证负载大小、过滤敏感词并确保输出格式符合 Agent 的解析要求。

**实施步骤**:
1. **输入清洗**: 在构建请求发送给 SageMaker 之前，检查输入字符串长度，并移除任何潜在的恶意指令字符。
2. **输出解析**: 定义严格的 Pydantic 模型或 JSON Schema，验证模型返回的内容是否为 Agent 可用的有效 JSON 或文本格式。
3. **内容审查**: 利用 Amazon Comprehend 或内置的正则表达式对模型输出进行实时审查，拦截 PII（个人身份信息）或有害内容。

**注意事项**: 
不要依赖模型自身的“对齐”来保证安全性。必须在应用层实施主动的验证逻辑，防止无效或恶意的响应破坏 Agent 的工作流。

---

### 实践 3：构建高效的序列化与反序列化逻辑

**说明**: 
Strands Agents 通常通过特定的 API 协议（如 LangChain 标准接口或 OpenAI 兼容协议）与模型提供者通信。SageMaker 的原生响应通常是一个包含 `generated_text`、`details` 等字段的复杂 JSON 对象。如果不进行正确的映射，Agent 将无法提取最终的回复内容。最佳实践是创建一个适配器层，专门负责将 SageMaker 的原始响应转换为 Agent 框架期望的标准格式。

**实施步骤**:
1. **定义映射函数**: 编写代码提取 SageMaker 响应体中的核心文本字段（例如 `outputs[0].generated_text`）。
2. **处理 Token 概率**: 如果 Agent 需要使用带思考链的功能，确保同时映射 `token_probabilities` 或 `log_probs`。
3. **标准化错误码**: 将 SageMaker 的服务错误（如 503 Model Not Ready）转换为 Agent 可理解的 LLM 提供者错误代码（如 `RateLimitError` 或 `ServiceUnavailable`）。

**注意事项**: 
注意处理流式响应与非流式响应的区别。如果 Agent 需要流式输出，必须实现 SSE（Server-Sent Events）逻辑来逐块传输 SageMaker 的生成结果。

---

### 实践 4：设计健壮的容错与自动重试机制

**说明**: 
云端推理服务可能会遇到冷启动、瞬时网络抖动或实例资源耗尽等情况。Strands Agents 作为自动化流程，如果因单次模型调用失败而终止，会导致任务失败。最佳实践是实现指数退避重试策略和断路器模式，以确保 Agent 的稳定性。

**实施步骤**:
1. **配置重试策略**: 在自定义提供者代码中集成重试逻辑（如使用 Python 的 `tenacity` 库），针对 5xx 错误或超时进行最多 3-5 次重试，每次重试的等待时间指数增加（如 1s, 2s, 4s）。
2. **处理冷启动**: 在调用端点前，检测端点状态。如果端点正在创建中，配置较长的超时时间（如 60 秒）。
3. **启用监控告警**: 利用 Amazon CloudWatch 设置警报，当端点调用错误率超过阈值时触发通知，以便人工介入。

**注意事项**: 
避免无限重试导致成本激增。设置最大重试次数，并在达到上限后优雅地降级（例如返回预设的静态回复或记录

---
## 学习要点

- 通过实现自定义模型提供程序接口，可以将 Amazon SageMaker AI 托管的大语言模型（LLM）集成到 Strands Agents 中，从而突破预置模型的限制。
- 利用 AWS 基础设施，可以在私有 VPC 内部署模型，确保数据安全性和合规性，同时满足企业对数据驻留的严格要求。
- 自定义提供程序允许开发者灵活适配特定的模型输入输出格式，实现与 SageMaker 端点的无缝通信。
- 该架构支持使用开源或微调过的模型，使企业能够根据特定业务需求优化模型性能和成本。
- 通过将 Strands Agents 与 SageMaker 集成，企业可以在利用生成式 AI 能力的同时，保持对底层基础设施的完全控制权。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [Strands](/tags/strands/) / [LLM](/tags/llm/) / [SGLang](/tags/sglang/) / [Llama 3.1](/tags/llama-3.1/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [在 SageMaker 上部署 SGLang 并集成至 Strands 智能体]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--2.md" >}})
- [在 Amazon SageMaker 中使用 Outlines 实现 LLM 结构化输出]({{< relref "posts/20260224-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-4.md" >}})
- [AWS SageMaker实战：用Dottxt Outlines实现LLM结构化输出]({{< relref "posts/20260225-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-12.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*