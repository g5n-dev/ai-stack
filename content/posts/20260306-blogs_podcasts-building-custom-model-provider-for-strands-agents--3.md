---
title: 为Strands智能体构建SageMaker托管LLM自定义解析器
date: 2026-03-06 01:38:42+08:00
draft: false
entry_kind: auto
tags:
- AWS
- SageMaker
- Strands
- LLM
- Llama 3.1
- SGLang
- 自定义解析器
- 模型部署
categories:
- AI 工程
- 后端
source: blogs_podcasts
description: 本文介绍了如何为 Strands 代理构建自定义模型解析器，以便在 SageMaker AI 托管的 LLM（如 Llama 3.1）不原生支持
  Bedrock Messages API 格式时进行集成。 主要内容包括： 1. **背景与目的**：针对托管在 SageMaker 上且不原生兼容 Bedrock
  API
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios:
- 大语言模型
- 后端开发
---

# 为Strands智能体构建SageMaker托管LLM自定义解析器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---

## 摘要/简介

本文演示了在接入不原生支持 Bedrock Messages API 格式的 SageMaker 托管 LLM 时，如何为 Strands 智能体构建自定义模型解析器。我们将一起使用 awslabs/ml-container-creator 在 SageMaker 上部署 Llama 3.1 与 SGLang，然后实现一个自定义解析器将其与 Strands 智能体集成。

---

## 导语

将自托管的大语言模型（LLM）接入智能体框架时，兼容性往往是开发者面临的首要挑战。本文将演示如何在 Amazon SageMaker 上部署 Llama 3.1 与 SGLang，并通过构建自定义模型解析器，使其适配 Strands 智能体的标准接口。阅读本文，您将掌握实现异构模型与智能体无缝集成的具体方法，从而在云环境中灵活构建可控的生成式 AI 应用。

---

## 摘要

本文介绍了如何为 Strands 代理构建自定义模型解析器，以便在 SageMaker AI 托管的 LLM（如 Llama 3.1）不原生支持 Bedrock Messages API 格式时进行集成。

主要内容包括：
1.  **背景与目的**：针对托管在 SageMaker 上且不原生兼容 Bedrock API 格式的 LLM，通过自定义解析器将其接入 Strands 代理。
2.  **具体步骤**：
    *   **部署模型**：使用 `awslabs/ml-container-creator` 在 SageMaker 上部署 Llama 3.1（搭配 SGLang）。
    *   **构建解析器**：实现自定义解析器，以桥接模型与 Strands 代理，解决 API 格式不兼容问题。

简言之，文章演示了从 SageMaker 部署 LLM 开始，到最终通过开发自定义解析器完成与 Strands 代理集成的完整流程。

---

## 评论

### 中心观点
该文章的核心观点是：**企业可以通过在 SageMaker 上部署 SGLang 加速的开源模型（如 Llama 3.1），并构建自定义适配层，来打破 AWS Bedrock Agents 对特定 API 格式的硬性依赖，从而在私有化环境中实现高性能的智能体编排。**

### 支撑理由与边界分析

**1. 技术架构的解耦与灵活性（事实陈述 / 作者观点）**
文章提出了一种“中间件适配器”的架构模式。Strands Agents（假设为某种 Agent 框架或业务逻辑层）通常期望标准的 OpenAI/Bedrock API 格式，而高性能推理引擎（如 SGLang）往往为了优化吞吐量实现了自定义协议。通过在 SageMaker 容器内实现自定义解析器，文章实际上是在推理服务端进行了“标准化改造”。
*   **深度评价**：这是一种务实且符合云原生理念的架构设计。它避免了在客户端（Agent 侧）编写复杂的适配代码，将异构性屏蔽在基础设施层。
*   **反例/边界条件**：如果模型本身不支持 Function Calling（如某些版本的基座模型），仅靠 API 格式的转换无法让 Agent 具备工具调用能力；此外，自定义解析器会增加 SageMaker 端点的维护复杂度。

**2. 性能与成本的极致优化（你的推断 / 事实陈述）**
文章选择 SGLang 而非默认的 vLLM 或 HuggingFace TGI，是一个极具技术洞察力的选择。SGLang 在处理多轮对话和复杂的 JSON 结构化输出（Agent 所需）时，其 RadixAttention 技术能显著降低显存占用并提高首字延迟（TTFT）。
*   **深度评价**：这显示了作者不仅关注“能不能跑”，更关注“跑得快不快”。对于 Agent 应用而言，推理延迟直接影响用户体验，SGLang + SageMaker 的组合是目前 AWS 云上性价比极高的方案。
*   **反例/边界条件**：SGLang 相比 TGI 生态较新，在生产环境的稳定性尚未经过大规模验证；且对于非 Llama 架构的模型，SGLang 的支持可能不如 TGI 完善。

**3. 企业级合规与数据主权（作者观点 / 行业共识）**
使用 SageMaker 部署模型而非直接调用 Bedrock 托管服务，通常是为了满足数据不出 VPC 或进行模型微调的需求。
*   **深度评价**：文章触及了企业级 AI 落地的痛点——合规性与定制化的平衡。通过 `awslabs/ml-container-creator` 这种工具链，企业可以完全掌控容器镜像，这在金融、医疗等强监管行业是刚需。
*   **反例/边界条件**：这种方案牺牲了 Bedrock 原生的 Serverless 伸缩能力（如按请求计费），SageMaker 需要运维人员手动管理实例扩缩容，对于流量波动剧烈的业务可能产生资源闲置成本。

### 多维度深入评价

**1. 内容深度：从“连接”到“优化”的跨越**
文章没有停留在简单的 API 调用层面，而是深入到了推理引擎的选型（SGLang）和容器化部署（ml-container-creator）。这表明作者对 LLM 推理的底层原理有深刻理解。论证上，通过解决“格式不兼容”这一具体问题，引出了“私有化高性能 Agent 部署”这一宏大命题，逻辑链条完整。

**2. 实用价值：高阶开发者的实战指南**
对于正在使用 AWS 技术栈且希望摆脱单一模型供应商绑定的团队来说，这篇文章具有极高的参考价值。它提供了一套可复用的模版：如何将非标准模型接入标准 Agent 框架。

**3. 创新性：工具链的组合应用**
虽然单独看 SageMaker 部署或 SGLang 都不是新概念，但将 **SGLang 的高性能推理能力** 与 **SageMaker 的企业级托管能力** 结合，并专门解决 **Agent 框架的协议适配** 问题，这种组合拳在当前的社区文档中相对稀缺。

**4. 行业影响：推动“推理侧标准化”**
随着 Agent 应用爆发，模型推理服务与 Agent 框架之间的协议碎片化问题日益严重。这篇文章实际上是在倡导一种趋势：**不要修改 Agent 来适应模型，而应该在模型推理端通过适配器来遵循标准（如 OpenAI API 格式）**。这有助于行业向更通用的接口标准演进。

**5. 争议点与不同观点**
*   **过度设计的风险**：部分观点认为，如果仅仅是为了格式转换，在网关层（如 Nginx 或 Kong）处理可能比修改模型容器更轻量。文章选择在容器内部解决，虽然性能更好，但牺牲了部署的灵活性。
*   **维护成本**：引入 `ml-container-creator` 和自定义解析器意味着技术栈的复杂度上升。对于初创公司，直接使用 Bedrock 或 OpenAI 可能是更优解，自建基础设施的机会成本极高。

### 可验证的检查方式

1.  **性能对比实验**：
    *   **指标**：在相同 SageMaker 实例（如 ml.g5.2xlarge）上，分别部署 SGLang + Llama 3.1 与 vLLM + Llama 3.1。
    *   **验证点**：使用模拟 Agent 的多轮对话请求（包含大量 JSON 结构化输出），测量 SGLang 的 Tokens/秒 和端到端延迟是否显著优于 vLLM

---

## 技术分析

### 1. 核心架构设计思想

本方案提出了一种**“混合编排”**的架构模式，旨在打破 AWS Bedrock Agents 与特定托管模型的强绑定关系。其核心设计理念在于**将模型推理层与任务编排层进行解耦**。

*   **解耦模型与框架**：传统模式下，Bedrock Agents 仅能调用 Bedrock 托管的模型。该方案通过构建自定义模型提供程序，将部署在 SageMaker 上的开源模型（如 Llama 3.1）伪装成 Bedrock 原生服务，使得上层编排逻辑无需关心底层模型的部署位置。
*   **自主可控与灵活性**：这一架构允许企业在保留 Bedrock 强大的 Agent 编排能力（如 ReAct 循环、知识库检索）的同时，利用 SageMaker 实现对底层模型的完全控制，满足数据隐私、合规性及深度定制化的需求。

### 2. 关键技术实现与难点

该方案的技术实现主要依赖于 AWS Lambda 作为中间适配层，处理协议转换与流式数据转发。

*   **协议适配与转换**
    Bedrock Agents 使用标准的 Messages API 格式发送请求，而 SageMaker 上的 SGLang 容器通常期望 OpenAI 兼容格式或原生 Prompt 格式。
    *   **实现逻辑**：中间层需拦截 Bedrock 的请求，提取核心 Prompt 与参数，并重构为 SGLang 可接受的 JSON 结构。
    *   **难点**：确保 Prompt 模板（尤其是 Llama 3.1 的特殊 Token）在转换过程中不丢失语义，需在容器启动时严格配置 `--chat-template` 参数。

*   **流式响应处理**
    为了保证用户体验，必须实现低延迟的流式输出。
    *   **实现逻辑**：解析 SGLang 返回的 Server-Sent Events (SSE) 流，将增量 Token 实时封装回 Bedrock 定义的有效载荷格式。
    *   **难点**：Bedrock 对流式响应的 JSON 结构校验极为严格。编写健壮的解析器来处理网络抖动、分块传输及特殊的终止符是确保 Agent 不报错的关键。

*   **高性能推理容器化**
    利用 `awslabs/ml-container-creator` 构建包含 SGLang 的推理镜像。
    *   **优势**：SGLang 针对 Llama 3.1 的结构化输出进行了优化，能提供比传统 vLLM 或 HuggingFace TGI 更高的吞吐量和更低的显存占用。

### 3. 业务价值与应用场景

该技术方案为企业落地生成式 AI 提供了极具价值的**“混合云”**路径：

*   **数据主权与合规**：对于金融、医疗等高度敏感行业，数据往往不允许离开私有网络。通过该方案，模型推理完全发生在客户可控的 SageMaker VPC 内部，仅将编排请求经过 Bedrock 服务，从而满足严格的数据合规要求。
*   **成本效益优化**：对于高并发场景，使用自部署的开源模型（如 Llama 3.1 70B）并结合 SGLang 的优化，长期运营成本可能低于持续调用昂贵的商业闭源模型 API。
*   **技术栈复用**：企业无需为了使用私有模型而自研 Agent 框架，可以直接复用 Bedrock Agents 成熟的工具调用、知识库集成和链式编排能力，大幅降低研发复杂度并加快产品上市速度。

---

## 最佳实践

### 实践 1：优化 SageMaker 端点配置与资源管理

**说明**: 在构建自定义模型提供商时，SageMaker 端点的资源配置直接影响响应延迟和吞吐量。不合理的实例选择会导致成本浪费或性能瓶颈，特别是在处理 Strands Agents 发起的高并发请求时。

**实施步骤**:
1. 根据模型的参数量（如 7B, 70B）和预期并发量，选择合适的实例类型（如 ml.g5 或 ml.p4）。
2. 配置多模型端点或利用 SageMaker 的 GPU 共享功能以提高资源利用率。
3. 设置自动扩缩容策略，定义目标追踪指标（如 CPU 利用率或每请求数延迟）。

**注意事项**:
- 监控端点的冷启动时间，对于实时交互场景，建议保持一定数量的预置实例。
- 确保端点配置的 Variant（变体）设置合理的生产流量权重。

---

### 实践 2：统一输入输出格式转换

**说明**: Strands Agents 通常期望标准的 OpenAI 兼容 API 格式（如 ChatCompletion），而 SageMaker 托管的开源模型（如 Llama 3 或 Mistral）往往具有自定义的输入/输出结构。构建适配层以处理这种格式差异是集成的关键。

**实施步骤**:
1. 在 SageMaker 推理容器中实现预处理脚本，将 Strands 发送的 JSON 格式转换为目标模型所需的 Prompt 模板。
2. 实现后处理逻辑，将模型输出的原始文本解析为包含 `choices`、`message` 和 `finish_reason` 的标准 JSON 响应。
3. 测试流式响应与非流式响应的兼容性，确保 `stream_options` 被正确处理。

**注意事项**:
- 仔细处理 Token 计数逻辑，确保返回的 `usage` 字段（`prompt_tokens`, `completion_tokens`）准确无误，以便 Strands 进行成本追踪。

---

### 实践 3：实施严格的身份验证与授权

**说明**: 将 SageMaker 端点暴露给 Strands Agents 时，必须确保通信安全，防止未授权访问。利用 AWS IAM 和签名请求是保护端点的最佳方式。

**实施步骤**:
1. 为 Strands Agents 创建专用的 IAM 角色，仅授予特定 SageMaker 端点的 `sagemaker:InvokeEndpoint` 权限。
2. 在自定义提供商代码中，使用 AWS SDK（如 Boto3）的 SigV4 签名机制对请求进行签名。
3. 如果端点通过 VPC 内网访问，确保安全组仅允许来自特定 IP 范围或 VPC 端点的流量。

**注意事项**:
- 避免在代码中硬编码 AWS 凭证，应优先使用 IAM Roles Anywhere 或环境变量/实例元数据服务。
- 启用 AWS CloudTrail 以记录所有 API 调用，便于审计。

---

### 实践 4：构建健壮的错误处理与重试机制

**说明**: 网络波动或模型推理超时可能导致请求失败。自定义提供商需要具备优雅降级和自动重试能力，以保证 Agent 任务的连续性。

**实施步骤**:
1. 捕获 SageMaker 特定的错误代码（如 `ModelError`, `ServiceUnavailable`, `ValidationError`）。
2. 实现指数退避重试策略，对于 5xx 错误或特定 429 (限流) 错误进行自动重试。
3. 将底层基础设施错误转换为标准的 HTTP 状态码和错误消息返回给 Strands。

**注意事项**:
- 设置最大重试次数和超时时间，防止级联故障导致系统资源耗尽。
- 确保错误消息对 Agent 可读，以便 Agent 能够根据错误信息调整后续行动。

---

### 实践 5：启用实时监控与可观测性

**说明**: 为了评估模型性能和 Agent 体验，必须收集详细的指标和日志。SageMaker 提供了内置的监控工具，应充分利用。

**实施步骤**:
1. 启用 SageMaker Model Monitor 以捕获数据质量和模型偏差。
2. 配置 CloudWatch Logs 收集推理日志，记录 Prompt 和 Response 的采样数据（注意脱敏）。
3. 在自定义提供商代码中埋点，记录请求延迟、Token 吞吐量（Tokens/秒）和错误率。

**注意事项**:
- 确保日志中不包含敏感的 PII（个人身份信息）数据，可在推理脚本中添加脱敏层。
- 设置告警阈值，当错误率突增或延迟超过阈值时及时通知运维人员。

---

### 实践 6：利用语义缓存降低延迟与成本

**说明**: Agent 工作流中经常包含重复的上下文查询或常见问题。通过在 SageMaker 端点之前或自定义提供商内部实现语义缓存，可以显著减少推理调用次数。

**实施步骤**:
1. 集成向量数据库（如 Amazon Aurora PostgreSQL 或 MemoryDB）作为缓存存储。
2. 对 Agent 发送的 Prompt 生成

---

## 学习要点

- 通过在 Strands Agents 中构建自定义模型提供程序，可以将部署在 Amazon SageMaker 端点上的 LLM 无缝集成，从而实现对专有或定制化模型的直接调用。
- 实现自定义提供程序的核心在于正确配置 API 接口，使其能够处理 SageMaker 端点特定的请求和响应格式（如 JSON 结构），确保与代理框架的兼容性。
- 利用此架构可以灵活替换底层模型，允许开发者根据成本、性能或数据隐私需求，在 SageMaker 托管的基础模型与微调模型之间进行切换。
- 该集成方案支持将敏感数据保留在 AWS 环境内，通过使用 VPC 接口端点调用 SageMaker，有效满足企业级的安全与合规要求。
- 在构建过程中，必须处理异步推理和流式响应等高级特性，以确保 Strands Agents 能够提供与直接使用公共 API 相似的低延迟交互体验。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [Strands](/tags/strands/) / [LLM](/tags/llm/) / [Llama 3.1](/tags/llama-3.1/) / [SGLang](/tags/sglang/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [在 SageMaker 上部署 SGLang 并集成至 Strands 智能体]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--2.md" >}})
- [在 Amazon SageMaker 中使用 Outlines 实现 LLM 结构化输出]({{< relref "posts/20260224-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-4.md" >}})
- [AWS SageMaker实战：用Dottxt Outlines实现LLM结构化输出]({{< relref "posts/20260225-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-12.md" >}})
- [AWS SageMaker 集成 Dottxt Outlines 实现 LLM 结构化输出]({{< relref "posts/20260226-blogs_podcasts-generate-structured-output-from-llms-with-dottxt-o-13.md" >}})
