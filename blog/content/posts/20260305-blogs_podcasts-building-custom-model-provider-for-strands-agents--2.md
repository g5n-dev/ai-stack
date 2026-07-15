---
title: 在SageMaker上部署SGLang并集成Strands智能体自定义模型
date: 2026-03-05 17:47:47+08:00
draft: false
entry_kind: auto
tags:
- SageMaker
- SGLang
- Llama 3.1
- Strands
- 模型部署
- 自定义解析器
- 推理优化
- AWS
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 以下是针对所提供内容的中文总结： 本文旨在演示如何在 **Amazon SageMaker AI** 端点上托管大语言模型（LLM），并通过构建**自定义模型提供商**将其集成到
  **Strands Agents** 智能体中。此过程主要针对那些不原生支持 Bedrock Messages API 格式的模型，通过自定
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios:
- 后端开发
aliases:
- /posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--10/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--4/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--5/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--6/
- /posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--9/
- /posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--10/
- /posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--9/
- /posts/20260308-blogs_podcasts-building-custom-model-provider-for-strands-agents--10/
- /posts/20260309-blogs_podcasts-building-custom-model-provider-for-strands-agents--10/
- /posts/20260309-blogs_podcasts-building-custom-model-provider-for-strands-agents--11/
- /posts/20260309-blogs_podcasts-building-custom-model-provider-for-strands-agents--12/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# 在SageMaker上部署SGLang并集成Strands智能体自定义模型

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---

## 摘要/简介

本文演示了当使用不支持 Bedrock Messages API 格式的、托管在 SageMaker 上的 LLM 时，如何为 Strands 智能体构建自定义模型解析器。我们将介绍如何使用 awslabs/ml-container-creator 在 SageMaker 上通过 SGLang 部署 Llama 3.1，然后实现一个自定义解析器将其与 Strands 智能体集成。

---

## 导语

当在 Amazon SageMaker 上部署非标准格式的 LLM 时，将其集成到 Strands 智能体往往面临接口兼容性挑战。本文将演示如何通过 SGLang 部署 Llama 3.1 并构建自定义模型解析器，从而解决与 Bedrock Messages API 格式不匹配的问题。读者将掌握实现模型与智能体无缝对接的具体步骤，确保在自有基础设施上灵活调用大模型能力。

---

## 摘要

以下是针对所提供内容的中文总结：

本文旨在演示如何在 **Amazon SageMaker AI** 端点上托管大语言模型（LLM），并通过构建**自定义模型提供商**将其集成到 **Strands Agents** 智能体中。此过程主要针对那些不原生支持 Bedrock Messages API 格式的模型，通过自定义解析器来实现兼容。

主要步骤和内容包括：

1.  **模型部署**：
    文章首先介绍了如何在 SageMaker 上部署 **Llama 3.1** 模型。为了优化推理性能，部署过程使用了 **SGLang** 作为推理引擎，并利用 `awslabs/ml-container-creator` 工具来简化容器的构建与配置。

2.  **实现自定义解析器**：
    由于托管的模型可能不直接遵循 Bedrock 的标准消息格式，文章详细讲解了如何编写**自定义模型解析器**。该解析器负责在 Strands Agents 与 SageMaker 托管的 LLM 之间进行请求和响应的转换，确保数据格式的正确传输。

**总结**：通过结合 SageMaker 的托管能力与 Strands 的可扩展性，开发者可以灵活地使用多样化的开源模型（如 Llama 3.1）构建智能体应用，而不仅限于 Bedrock 原生支持的模型。

---

## 评论

**文章中心观点**
本文的核心观点是：企业应通过在 SageMaker 上自部署高性能推理框架（如 SGLang）并构建自定义模型解析器，来突破 Bedrock 托管服务的格式限制，从而在 AWS 生态内实现对 Llama 3.1 等开源模型的高性能、低成本且标准化的编排集成。

**支撑理由与边界条件**

1.  **推理性能与成本效益的平衡（事实陈述）**
    *   **理由**：文章选择 SGLang 作为推理引擎而非默认的 vLLM 或 HuggingFace TGI，具有显著的技术前瞻性。SGLang 以其激进的结构化生成和 RadixAttention 技术著称，在处理高并发请求时能提供更低的延迟。结合 SageMaker 的托管特性，企业可以在保持数据安全的前提下，获得接近 Bedrock 托管服务的响应速度，同时规避按 token 计费的昂贵成本。
    *   **反例/边界条件**：SGLang 相比 vLLM 生态成熟度较低，社区支持较小。如果业务模型需要极度复杂的采样逻辑或特定的量化格式（如 AWQ/GPTQ 的特殊配置），SGLang 可能存在兼容性风险，此时 vLLM 可能是更稳健的选择。

2.  **解耦模型服务与编排协议的架构设计（你的推断）**
    *   **理由**：文章提出的“自定义模型解析器”方案，实质上是在构建一个**适配器层**。这解决了企业级 AI 落地中的一个核心痛点：模型层的多样性（SGLang/Llama 3.1）与应用层的标准化（Agents/Bedrock API）之间的矛盾。通过这种解耦，开发者可以在不修改上层 Agent 逻辑的情况下，灵活替换底座模型或推理引擎，符合微服务架构的最佳实践。
    *   **反例/边界条件**：这种适配器层引入了额外的代码维护负担。如果底层模型频繁升级（例如 Llama 3.1 升级到 3.2），自定义解析器可能需要手动适配新的 Tokenizer 或特殊 Token，而 Bedrock 原生服务则由 AWS 自动维护。

3.  **对“半托管”模式可行性的验证（作者观点）**
    *   **理由**：文章展示了利用 `awslabs/ml-container-creator` 快速构建容器的过程，论证了 AWS “Bring Your Own Model” (BYOM) 策略的成熟度。这对于金融、医疗等受监管行业尤为重要，这些行业需要将数据保留在 VPC 内部，无法直接调用公网上的 Bedrock 或 OpenAI 接口。此方案提供了一条既合规又能享受现代 Agent 编排能力的路径。
    *   **反例/边界条件**：运维复杂度显著增加。相比 Bedrock 的“无服务器”体验，自部署意味着需要关注 GPU 利用率、自动扩缩容策略以及容器健康检查。如果请求量具有极剧烈的波峰波谷，自部署集群的资源闲置成本可能高于按量付费的 Bedrock。

**多维度深入评价**

1.  **内容深度**
    文章不仅仅停留在“如何调用 API”，而是深入到了**容器化构建**与**协议转换**的层面。它隐含地讨论了 OpenAPI 标准在异构模型服务中的重要性。论证逻辑清晰：从基础设施（SageMaker + SGLang）到中间层再到应用层，形成了一个完整的闭环。然而，文章在**SGLang 的具体调优参数**（如 KV Cache 限制、并发数限制）上着墨较少，略显遗憾。

2.  **实用价值**
    对于正在使用 AWS 构建生成式 AI 应用的架构师而言，这是一篇高价值的实战指南。它提供了一套可复用的模版：如何在非标准接口下实现标准化的 Agent 编排。特别是对于 Strands（AWS 内部的 Agent 编排框架，通常指代 Bedrock Agents 或类似服务）用户，这解决了特定模型无法被原生调用的难题。

3.  **创新性**
    将 **SGLang** 引入 SageMaker 的标准部署流程并对接 Agent 服务，具有一定的技术敏锐度。大多数 AWS 教程倾向于使用保守的 TGI 或 DeepSpeed，SGLang 的引入代表了追求极致性能的工程取向。此外，强调“自定义解析器”而非“修改 Agent 代码”，体现了良好的软件工程思维。

4.  **可读性与逻辑**
    文章结构符合“问题-方案-实施”的经典技术博客范式。逻辑链条完整：因为 SageMaker 端点不支持 Bedrock 格式 -> 所以需要解析器 -> 因为需要高性能 -> 所以选择 SGLang。但在代码片段的上下文衔接上，可能需要读者具备较强的 AWS CDK 或 Docker 背景知识。

5.  **行业影响**
    这篇文章反映了行业趋势：**从“模型即服务”向“推理基础设施即服务”的转变**。企业不再满足于调用黑盒 API，而是开始追求对推理过程的精细控制（如 Speculative Decoding, Structured Generation）。这推动了云厂商从单纯的模型提供商向 AI 基础设施提供商转型。

**争议点与不同观点**

*   **过度工程化风险**：有观点认为，如果仅仅是为了格式兼容，在 API Gateway 或负载均衡层做简单的 JSON 转换即可，无需在模型容器内部或 Agent 代码层面引入复杂的解析器逻辑。
*   **SGLang 的生产就绪度**：虽然 SGLang 性能强悍，但在生产环境的稳定性（Long-running stability）方面，社区反馈仍不如 vLLum 成熟。在关键业务流中使用

---

## 技术分析

**文章主旨**
文章探讨了如何在AWS生态系统中，解决非标准格式模型与智能体框架的兼容性问题。具体而言，即通过构建自定义适配层，使部署在Amazon SageMaker上的开源大模型（如Llama 3.1）能够被Strands智能体框架调用，从而绕过对特定托管API格式的依赖。

**技术逻辑**
文章的核心逻辑基于**适配器模式**。Strands框架通常期望符合Bedrock Messages API标准的输入输出格式，而部署在SageMaker上的模型（特别是结合SGLang等推理引擎时）往往使用OpenAI格式或其他自定义协议。为了解决这种接口不匹配，文章提出在SageMaker端点前或容器内部构建一个转换层，负责协议翻译。这使得开发者可以在保留SageMaker托管能力和SGLang推理性能的同时，复用Strands的Agent编排能力。

**技术价值**
该方案填补了模型部署层与应用编排层之间的技术空白。在构建企业级AI应用时，这种解耦方式允许开发者根据性能和成本需求灵活选择底层模型（如Llama 3.1或特定微调版本），而不受限于上层框架原生支持的模型列表，有助于实现更具弹性的系统架构。

### 2. 关键技术要点

**涉及的关键技术**
*   **Amazon SageMaker Endpoints:** 用于托管模型的HTTP服务端点，支持自定义Docker镜像。
*   **SGLang:** 一个高性能的大语言模型推理运行时，用于优化模型服务的吞吐量和延迟。
*   **Strands Agents:** AWS的智能体应用框架，依赖特定的API协议（通常为Bedrock兼容格式）来驱动Agent工作流。
*   **自定义解析器:** 负责在SageMaker接收到的标准请求与模型推理引擎（SGLang）实际接受的格式之间进行转换的中间件逻辑。

**实现原理**
1.  **容器化部署:** 利用 `ml-container-creator` 等工具，将Llama 3.1模型权重及SGLang推理服务器打包进Docker容器，并部署至SageMaker。
2.  **协议转换:** 在容器内部或SageMaker后端实现解析逻辑。当Strands发送请求时，解析器将其从Bedrock Messages格式转换为SGLang理解的OpenAI格式；推理完成后，再将SGLang的响应转换回Bedrock格式返回给Strands。
3.  **流式处理:** 针对Agent应用常见的流式输出需求，解析器需处理SGLang的Server-Sent Events (SSE)流，将其重新封装为符合Bedrock协议的流式事件块。

**技术难点与应对**
*   **接口差异处理:** SGLang原生输出格式（如OpenAI兼容）与Strands期望的Bedrock格式（包含`stopReason`、特定JSON结构）存在差异。需编写代码精确映射这些字段，确保Agent能正确解析模型意图和终止状态。
*   **流式数据重组:** 实时处理流式响应时，需要维护请求上下文，确保分块传输的数据在经过格式转换后仍能保持语义连贯性和时间顺序，避免因格式转换导致的流式中断或乱码。

---

## 最佳实践

### 实践 1：优化 SageMaker 端点推理配置

**说明**: 为了确保 Strands Agents 能够获得低延迟的响应，必须针对大语言模型（LLM）的特性对 SageMaker 推理端点进行精细调优。默认配置通常无法满足实时交互的需求。

**实施步骤**:
1. 根据模型大小和并发需求，选择合适的实例类型（如 `ml.g5` 或 `ml.p4` 系列）。
2. 在创建端点配置时，调整 `InstanceInferenceTimeout` 和 `ModelDownloadTimeout` 参数，防止长时间推理导致超时。
3. 启用 SageMaker 的多模型端点或多容器端点功能以提高资源利用率。

**注意事项**: 监控 CloudWatch 指标中的 `InvocationLatency`，如果延迟过高，考虑增加实例数量或升级实例类型。

---

### 实践 2：实现标准化输入输出转换逻辑

**说明**: Strands Agents 通过标准接口与 LLM 通信，而部署在 SageMaker 上的模型（如 Llama 3 或 Mistral）通常有特定的输入输出格式。必须编写适配层来处理这种差异。

**实施步骤**:
1. 在自定义模型提供程序代码中，实现 `invoke_stream` 和 `invoke` 方法。
2. 编写转换函数，将 Strands 的标准请求格式（包含 Prompt、Temperature、MaxTokens）转换为 SageMaker 端点所需的 JSON 格式。
3. 解析 SageMaker 返回的原始响应体，提取生成的文本并将其流式传输回 Agent。

**注意事项**: 确保处理了 Token 限制和截断逻辑，避免因 Prompt 过长导致端点返回错误。

---

### 实践 3：配置流式响应处理

**说明**: 为了提供良好的用户体验，Strands Agents 需要实时显示生成的文本。SageMaker 支持流式响应，但需要正确配置连接和缓冲区处理。

**实施步骤**:
1. 在调用 SageMaker `InvokeEndpointWithResponseStream` API 时，确保自定义处理程序能够处理 `PayloadPart` 事件。
2. 实现一个迭代器，逐步接收并拼接从端点返回的数据块。
3. 处理字节流解码，确保特殊字符和多字节字符（如中文）在流式传输中不会出现乱码。

**注意事项**: 测试网络不稳定情况下的重连机制，避免流式传输中断导致整个对话失败。

---

### 实践 4：强化身份验证与 IAM 权限管理

**说明**: 自定义模型提供程序需要安全地调用 SageMaker 端点。使用 AWS IAM 进行严格的权限控制是保障安全的关键。

**实施步骤**:
1. 为运行 Strands Agents 的服务角色分配特定的 IAM 策略，仅允许调用特定的 SageMaker 端点 ARN。
2. 遵循最小权限原则，确保该角色没有访问其他 AWS 资源的权限。
3. 在代码中通过 Boto3 Session 或默认链式凭证提供者获取凭证，避免硬编码 Access Key。

**注意事项**: 定期审计 IAM 策略，并使用 AWS CloudTrail 监控 API 调用日志，以检测异常访问行为。

---

### 实践 5：建立全面的错误处理与重试机制

**说明**: 云环境中的网络抖动或端点负载过高可能导致请求失败。健壮的错误处理机制能保证 Agent 服务的稳定性。

**实施步骤**:
1. 捕获特定的 SageMaker 异常（如 `ModelError`、`ServiceUnavailable` 或 `InternalFailure`）。
2. 实现指数退避算法，在遇到可重试错误时自动重试请求，避免冲击端点。
3. 定义降级策略，当端点完全不可用时，向 Agent 返回友好的错误提示或转接至备用逻辑。

**注意事项**: 区分客户端错误（如 400 Bad Request，通常由 Prompt 格式错误引起）和服务端错误，不要重试客户端错误以免浪费资源。

---

### 实践 6：实施 Prompt 模板管理与版本控制

**说明**: 不同的 Agent 任务可能需要不同的 Prompt 模板。将 Prompt 逻辑硬编码在调用层不利于维护和迭代。

**实施步骤**:
1. 在调用 SageMaker 之前，在自定义提供程序中引入 Prompt 模板层。
2. 使用模板引擎（如 Jinja2）动态构建 Prompt，注入上下文变量。
3. 将 Prompt 模板存储在配置文件或数据库中，以便在不修改代码的情况下进行调整。

**注意事项**: 确保模板中的系统指令与用户输入清晰分离，防止 Prompt 注入攻击。

---

## 学习要点

- 通过将 Amazon Bedrock 的“知识库”功能与自定义模型提供商集成，可以在 SageMaker 托管的模型上实现 RAG（检索增强生成）能力，从而让私有模型能够利用企业私有数据回答问题。
- 利用 Strands Agents 框架的“模型提供商”接口，只需实现一个简单的 Python 类并配置模型 ID 和端点 URL，即可将 SageMaker 托管的 LLM 无缝接入到 Agent 的工具调用流程中。
- 通过在 SageMaker 部署配置中设置 `HF_MODEL_ID` 为 Llama-3-8b-Instruct 等模型，并结合 Hugging Face 的 TGI（文本生成推理）容器，可以快速在 AWS 上部署高性能的推理服务。
- 该解决方案通过自定义模型提供商填补了 Bedrock 与 SageMaker 之间的差距，允许开发者在使用 Bedrock 的编排和 RAG 功能的同时，灵活选择 SageMaker 上的特定开源模型。
- 在实现自定义模型提供商时，必须正确处理 `_prepare_output` 方法，以确保模型生成的原始文本能被解析为 Agent 可识别的标准化消息格式。
- 实现过程中需特别注意处理 Token 计数（`_count_tokens`），因为不同的模型架构（如 Llama-3）需要特定的分词器来准确计算推理成本。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [SageMaker](/tags/sagemaker/) / [SGLang](/tags/sglang/) / [Llama 3.1](/tags/llama-3.1/) / [Strands](/tags/strands/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/) / [推理优化](/tags/%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/) / [AWS](/tags/aws/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [在 SageMaker 上部署 SGLang 并集成至 Strands 智能体]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--2.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--2.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--2.md" >}})
- [为Strands智能体构建SageMaker自定义模型解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--2.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260211-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-0.md" >}})
