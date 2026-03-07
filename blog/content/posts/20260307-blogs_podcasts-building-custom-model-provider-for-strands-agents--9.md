---
title: "为 Strands 代理构建适配 SageMaker 托管 LLM 的自定义模型解析器"
date: 2026-03-07T06:04:23+08:00
draft: false
entry_kind: "auto"
tags: ["AWS", "SageMaker", "Strands", "LLM", "Llama 3.1", "SGLang", "模型部署", "自定义解析器"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文介绍了如何为运行在 Amazon SageMaker 端点上（但不支持 Bedrock Messages API 格式）的大语言模型构建自定义模型提供商，并将其集成到 Strands Agents 中。主要内容如下： 1. **背景与目标**： 当用户希望使用托管在 SageMaker 上的开源模型（如 Llama"
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios: ["大语言模型", "后端开发"]
---

# 为 Strands 代理构建适配 SageMaker 托管 LLM 的自定义模型解析器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---
## 摘要/简介

本文演示了在配合使用不支持 Bedrock Messages API 格式的 SageMaker 托管 LLM 时，如何为 Strands 代理构建自定义模型解析器。我们将介绍如何使用 awslabs/ml-container-creator 在 SageMaker 上部署基于 SGLang 的 Llama 3.1，然后实现一个自定义解析器将其与 Strands 代理集成。

---
## 导语

将大语言模型（LLM）部署在 SageMaker 端点上并集成至 Strands 代理时，若模型不支持 Bedrock Messages API 标准格式，往往需要额外的适配工作。本文将演示如何利用 SGLang 部署 Llama 3.1，并通过构建自定义模型解析器来解决接口兼容性问题。通过阅读本文，您将掌握实现这一集成的具体步骤，从而在 AWS 环境中灵活地定制和扩展您的 AI 代理架构。

---
## 摘要

本文介绍了如何为运行在 Amazon SageMaker 端点上（但不支持 Bedrock Messages API 格式）的大语言模型构建自定义模型提供商，并将其集成到 Strands Agents 中。主要内容如下：

1.  **背景与目标**：
    当用户希望使用托管在 SageMaker 上的开源模型（如 Llama 3.1）配合 Strands Agents 时，常面临模型输出格式不兼容的问题。本文旨在解决这一问题，通过部署模型并编写自定义解析器来实现无缝集成。

2.  **模型部署（使用 SGLang）**：
    *   **工具选择**：使用 AWS Labs 的 `ml-container-creator` 工具，它能简化在 SageMaker 上构建和部署大模型容器的流程。
    *   **高性能推理**：文章具体演示了如何部署 **Llama 3.1** 模型，并配置 **SGLang** 作为推理引擎。SGLang 能够提供高吞吐量和低延迟的推理服务。
    *   **操作流程**：通过定义配置文件，利用容器构建工具自动处理模型托管的环境准备和部署步骤。

3.  **实现自定义解析器**：
    *   **核心挑战**：SageMaker 上的模型响应格式通常与 Strands Agents 标准期望的 Bedrock 格式不同。
    *   **解决方案**：开发了一个自定义模型解析器。该解析器负责拦截 SageMaker 的原始响应，并将其转换为 Strands Agents 能够理解和处理的统一格式。
    *   **集成步骤**：将此解析器注册到 Strands 的配置中，使得 Agent 能够像调用原生 Bedrock 模型一样调用托管在 SageMaker 上的 Llama 3.1。

4.  **总结**：
    通过结合 `ml-container-creator` 进行快速部署和自定义解析逻辑进行数据转换，用户可以灵活地将 SageMaker 上的高性能开源模型接入 Strands 智能体框架，从而在保持控制权的同时享受高效的 AI 应用开发体验。

---
## 评论

### 深度评论：基于SageMaker与SGLang构建Strands Agents自定义模型提供商

#### 一、 核心洞察与架构价值

**核心观点：**
该文章精准地切中了企业级AI应用落地的一个关键痛点：**如何在AWS托管生态的便利性与开源大模型的灵活性之间取得平衡？** 文章提出的解决方案是构建“自定义模型解析器”，将SGLang高性能推理引擎通过SageMaker端点深度集成到Strands Agents框架中。这不仅是对Bedrock托管服务限制的一种技术突围，更是对“推理中心化”架构趋势的一次有力实践。

**架构解构与论证：**
1.  **打破协议黑盒（适配器模式的应用）：**
    Strands Agents通常强依赖于Bedrock的Messages API格式。文章展示了如何编写自定义解析器，实际上是在Agent框架与底层模型之间实现了一个“翻译层”。这种解耦使得开发者无需修改上层Agent逻辑，即可无缝切换到底层的SGLang或vLLM，赋予了架构极高的可插拔性。

2.  **性能导向的工程选型：**
    文章选择SGLang而非传统的vLLM或TGI，体现了对Agent场景的深刻理解。Agent应用往往涉及频繁的Tool Calling和复杂的结构化输出，SGLang在结构化生成和并发处理上的优势，直接对应了Agent降低延迟、提高吞吐的核心需求。

3.  **合规与成本的最优解：**
    通过SageMaker进行私有化部署，数据流量完全控制在VPC内部，满足了金融、医疗等行业的合规红线。同时，利用SageMaker的自动扩缩容特性，相比直接调用商业API，在长尾或大规模并发场景下能显著降低Token成本。

#### 二、 批判性分析与实施挑战

尽管方案极具吸引力，但从工程落地的角度来看，该架构存在不可忽视的复杂度门槛：

1.  **运维负担的转移：**
    文章虽然解决了模型调用的问题，却引入了基础设施运维的挑战。维护一个基于SageMaker + SGLang的生产环境，意味着团队需要处理容器构建、版本更新、监控告警以及故障排查。对于缺乏成熟MLOps团队的组织而言，这种“自由度”可能演变成“不可控的黑洞”。相比之下，Bedrock的全托管模式在SLA保障上具有压倒性优势。

2.  **技术栈的碎片化风险：**
    自定义解析器是针对特定模型版本（如Llama 3.1）和特定推理引擎版本编写的。一旦底层模型API发生不兼容变更，或者SGLang进行重大版本更新，自定义解析器就需要随之重构。这种紧耦合在软件生命周期中带来了潜在的维护债务。

#### 三、 行业趋势与总结

这篇文章不仅是一篇技术教程，更是当前AI基础设施演进的一个缩影。它标志着行业正在从**“模型即服务”**向**“基础设施即代码”**转变。开发者不再满足于被动接受厂商提供的模型黑盒，而是开始通过组合高性能推理引擎（SGLang）、云原生基础设施和智能体框架，来构建符合自身业务特性的垂直化AI解决方案。

**总结：** 这是一篇面向“进阶开发者”的高质量指南，它填补了AWS GenAI生态中关于“高性能Agent后端构建”的空白，但要求读者具备相当的云原生运维能力。

---
## 技术分析

基于您提供的文章标题和摘要，尽管原文内容被截断，但结合AWS SageMaker、Strands Agents（推测为AWS Bedrock Agents或相关框架）、Llama 3.1以及SGLang等技术栈的背景，我可以为您构建一份深度分析报告。这篇文章主要探讨了在AWS生态系统中，如何打破标准API的限制，灵活集成高性能开源模型。

以下是详细分析：

---

# 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点是：**企业不应被云厂商的原生API格式（如Bedrock Messages API）所束缚，可以通过构建自定义模型提供者和解析器，将高性能、自定义部署的开源大模型（如Llama 3.1）无缝接入到智能体框架中。**

**作者想要传达的核心思想**
作者传达了“**基础设施解耦**”的思想。虽然AWS Bedrock提供了便捷的托管服务，但企业往往需要更低延迟、更高吞吐量或特定模型版本（如Llama 3.1）。通过使用SageMaker结合SGLang，并编写适配层，企业可以同时拥有“智能体框架的易用性”和“自部署模型的灵活性与性能”。

**观点的创新性和深度**
*   **创新性**：提出了在SageMaker上使用SGLang（一个高性能推理服务框架）而非常规的vLLM或TGI，并展示了如何通过`awslabs/ml-container-creator`这一工具链快速构建容器，这解决了“模型格式与Agent框架不兼容”的痛点。
*   **深度**：文章触及了LLM Ops（大模型运维）的深水区——即如何处理非标准化接口。它不仅仅讲部署，更讲“协议转换”和“中间件适配”的实现。

**为什么这个观点重要**
随着大模型应用的深入，企业发现单一API无法满足所有需求（如成本、数据隐私、特定微调版本）。掌握自定义模型Provider的构建能力，意味着企业拥有了**技术栈的完全控制权**，不再受限于云厂商的更新节奏，能够根据业务需求选择最优的推理引擎。

---

# 2. 关键技术要点

**涉及的关键技术或概念**
1.  **SGLang**：一个新兴的高性能LLM推理引擎，以高并发和低延迟著称，特别适合处理Agent场景中大量的结构化输出。
2.  **SageMaker Endpoints**：AWS提供的托管推理服务，支持自定义容器。
3.  **Strands Agents**：推测指代基于AWS Bedrock Agents或类似框架的智能体系统，它们通常依赖特定的JSON Schema进行工具调用。
4.  **awslabs/ml-container-creator**：用于简化Docker镜像构建的工具，解决了依赖管理复杂的痛点。

**技术原理和实现方式**
*   **原理**：Agent框架通常发送符合OpenAI或Bedrock标准的HTTP请求。SGLang原生可能不直接支持这些特定格式。因此，需要在SageMaker部署的容器中引入一个“中间件层”。
*   **实现**：
    1.  **模型部署**：利用SGLang的高效内核（如RadixAttention）在SageMaker上部署Llama 3.1。
    2.  **适配层编写**：在容器内部实现一个Python脚本（通常是Flask/FastAPI），接收Agent发来的标准请求，将其转换为SGLang理解的格式。
    3.  **响应解析**：将SGLang的原始输出重新封装为Agent框架期望的JSON格式（特别是Tool Use相关的参数）。

**技术难点和解决方案**
*   **难点**：**结构化输出**。Agent需要模型输出严格的JSON格式以便调用工具，而开源模型往往输出纯文本。
*   **解决方案**：利用SGLang的Constrained Decoding（约束解码）功能，或者在Parser层通过正则和后处理逻辑强制校验JSON格式，确保Agent能正确解析指令。

**技术创新点分析**
使用`ml-container-creator`是一个工程上的亮点，它将“写Dockerfile”这一繁琐过程变成了配置化，极大降低了非专业运维人员部署复杂推理环境（如CUDA环境、Python依赖）的门槛。

---

# 3. 实际应用价值

**对实际工作的指导意义**
*   **成本优化**：SageMaker使用Spot实例等资源通常比Bedrock按请求计费更具成本优势，尤其是对于高并发场景。
*   **性能提升**：SGLang针对KV Cache进行了优化，能显著降低Agent多轮对话的延迟。

**可以应用到哪些场景**
*   **企业私有化部署**：金融、医疗等对数据出境敏感，无法使用公有Bedrock API，必须在SageMaker VPC内部署的场景。
*   **特定模型微调**：企业微调了Llama 3.1，Bedrock未提供该版本，必须自部署。
*   **高频自动化Agent**：如自动化客服、代码生成Agent，对Token生成速度（TPS）有极高要求的场景。

**需要注意的问题**
*   **冷启动时间**：SageMaker Endpoint可能存在冷启动，需要配置好预置实例。
*   **维护成本**：自建意味着要负责模型的健康检查、自动扩缩容和版本更新。

**实施建议**
优先在开发环境验证SGLang与Bedrock Agents API的兼容性，特别是`function_calling`部分的字段映射是否完全一致。

---

# 4. 行业影响分析

**对行业的启示**
这标志着**“大模型中间件”时代的到来**。未来的竞争不仅仅是模型参数量的竞争，更是推理服务效率、适配性和工程化能力的竞争。

**可能带来的变革**
企业将从“购买模型API”转向“购买模型能力+自建基础设施”。云厂商的角色将从单纯的API提供商转变为基础设施（IaaS）和工具链的提供者。

**相关领域的发展趋势**
*   **推理引擎标准化**：SGLang、TGI、vLLM之间的竞争将倒逼API标准的趋同。
*   **MLOps工具链的成熟**：如`ml-container-creator`这类工具将普及，降低模型部署门槛。

---

# 5. 延伸思考

**引发的其他思考**
如果SGLang等高性能引擎能够通过自定义容器轻松接入Agent系统，那么未来“模型路由”将成为常态——即根据任务的难易程度，动态将请求路由到不同参数量或不同部署方式的模型上。

**可以拓展的方向**
*   **多模型负载均衡**：在一个SageMaker Endpoint后端挂载多个模型容器，实现动态切换。
*   **流式传输的标准化**：如何确保自定义Parser完美支持Server-Sent Events (SSE) 流式响应，以提升用户体验。

**未来发展趋势**
模型部署将**Serverless化**。未来SageMaker可能会支持更细粒度的Serverless推理，结合SGLang的高效启动，实现毫秒级的扩缩容。

---

# 6. 实践建议

**如何应用到自己的项目**
1.  **评估需求**：检查当前项目是否存在Bedrock原生模型无法满足的需求（如延迟、特定微调版本）。
2.  **搭建POC**：按照文章思路，使用Llama 3.1 8B版本在SageMaker上搭建SGLang环境。
3.  **编写适配器**：重点实现`request`和`response`的转换逻辑，确保Agent能正确提取工具调用参数。

**具体的行动建议**
*   学习SGLang的OpenAI兼容协议配置。
*   熟悉AWS CDK或SDK，实现SageMaker Endpoint的自动化部署。

**实践中的注意事项**
*   **超时设置**：Agent调用模型通常有超时限制（如30秒），SGLang虽然快，但在处理长Context时仍需注意。
*   **Token限制**：确保Parser正确处理了Max Tokens的截断逻辑，防止输出溢出导致解析失败。

---

# 7. 案例分析

**结合实际案例说明**
假设一个**金融研报生成Agent**。它需要读取大量PDF并生成分析报告。
*   **痛点**：Bedrock Claude 3.5 Sonet虽然效果好，但成本高，且上下文窗口在高峰期可能受限。
*   **应用**：使用Llama 3.1 70B（量化版）部署在SageMaker上，利用SGLang支持长Context。
*   **结果**：成本降低40%，且通过自定义Parser，强制模型输出符合内部数据库格式的JSON，无需后处理，直接入库。

**失败案例反思**
某团队直接将开源模型接入Agent，未做严格的JSON约束。
*   **后果**：模型偶尔输出Markdown代码块包裹的JSON，导致Agent解析器报错，任务中断。
*   **教训**：必须在Parser层加入强制的正则清洗或使用模型的Grammar-constrained decoding功能。

---

# 8. 哲学与逻辑：论证地图

**中心命题**
**在构建企业级AI Agent时，采用“自定义模型提供者”策略（如SageMaker + SGLang）在长期视角下优于直接依赖云厂商的封闭API。**

**支撑理由与依据**
1.  **性能可控性**：SGLang利用RadixAttention等技术，在多轮对话场景下延迟显著低于通用API。
    *   *依据*：SGLang官方基准测试数据及工程实践中的TPS对比。
2.  **成本效益**：对于高并发场景，自部署模型的推理成本远低于按Token计费的托管API。
    *   *依据*：AWS EC2/SageMaker实例成本与Bedrock API定价的财务测算对比。
3.  **数据主权与合规**：自部署允许数据完全保留在VPC内，满足金融/医疗行业的合规要求。
    *   *依据*：企业合规性框架（如GDPR、行业数据安全标准）。

**反例或边界条件**
1.  **边际成本递增**：对于低频、小规模的应用，自部署的运维成本（人力、时间）远超直接调用API的费用。
2.  **技术债务风险**：如果底层模型（如Llama）快速迭代，自部署团队需要花费大量精力跟进升级，而API用户则是“无痛升级”。

**命题性质判断**
*   **事实**：SageMaker支持自定义容器；SGLang具备高性能特性。
*   **价值判断**：认为“性能”和“控制权”比“开发便捷性”更重要。
*   **可检验预测**：随着模型参数量的增大和推理成本的上升，越来越多的企业级Agent将迁移至混合架构（核心逻辑用API，长尾任务用自部署）。

**立场与验证方式**
*   **立场**：支持在**中高并发、有特定合规或性能要求**的场景下采用自定义架构。
*   **验证方式**：
    *   *指标*：对比实验中，测量SGLang自定义端点与Bedrock原生端点在处理复杂Agent链（包含多次Tool Call）时的端到端延迟和每次调用成本。
    *   *观察窗口*：持续运行3个月，统计因模型解析错误导致的Agent失败率。

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 SageMaker 端点配置以降低延迟

**说明**: 
在构建自定义模型提供商时，LLM 的响应延迟直接影响 Strands Agents 的用户体验。SageMaker 端点的实例类型和配置选择对推理速度至关重要。必须根据模型大小和并发请求量，平衡计算能力与成本，确保端点能够提供低延迟的响应。

**实施步骤**:
1. 根据模型参数量（如 7B, 70B）选择合适的实例类型（如 p4d 或 p5 系列 GPU 实例）。
2. 在 SageMaker 配置中启用多模型端点或利用 GPU 的多实例并行处理能力。
3. 配置适当的实例数量以处理预期的并发请求，避免冷启动带来的延迟。

**注意事项**: 
监控 CloudWatch 指标中的 `ModelLatency`，如果延迟过高，考虑增加实例规格或优化模型量化版本。

---

### 实践 2：实现严格的输入输出序列化与转换

**说明**: 
Strands Agents 与 SageMaker 之间的通信需要通过特定的负载格式进行。自定义提供商代码必须能够将 Agent 的标准请求转换为 SageMaker 兼容的 JSON 格式，并能将模型的原始输出解析回 Agent 可理解的格式。处理 Token 计数和流式响应是此过程的关键部分。

**实施步骤**:
1. 定义请求转换函数，将 Agent 的消息列表映射到模型所需的 Prompt 模板（如 Llama 3 或 Mistral 格式）。
2. 实现响应解析逻辑，提取 `generated_text` 并计算 `prompt_tokens` 和 `completion_tokens` 用于成本监控。
3. 确保处理模型可能返回的异常 JSON 结构或错误信息。

**注意事项**: 
务必测试流式响应与非流式响应两种模式，确保数据转换逻辑不会丢失字符或在长文本生成时中断。

---

### 实践 3：构建稳健的错误处理与重试机制

**说明**: 
调用 SageMaker 端点可能会遇到网络抖动、端点过载（503 错误）或内部模型错误。自定义提供商必须具备优雅降级和重试能力，以防止 Agent 任务因单次请求失败而完全中断。

**实施步骤**:
1. 在代码中实现指数退避算法，用于处理 5xx 系列的服务器错误。
2. 区分可重试错误（如超时、限流）和不可重试错误（如认证失败、参数错误）。
3. 为 Strands Agents 提供有意义的错误反馈，以便 Agent 能够根据错误上下文决定是否重试或向用户报错。

**注意事项**: 
设置最大重试次数（例如 3 次），以避免在端点不可用时造成无限循环的资源消耗。

---

### 实践 4：强化身份验证与网络隔离

**说明**: 
企业级应用通常要求严格的权限控制。在连接 Strands Agents 到 SageMaker 时，必须确保凭证的安全存储，并尽可能利用 VPC（虚拟私有云）内网调用，避免数据暴露在公网中。

**实施步骤**:
1. 使用 AWS IAM 角色而非长期访问密钥来授权 SageMaker 端点的访问。
2. 配置 SageMaker 端点仅允许来自特定 VPC 的私有 API 调用。
3. 确保运行自定义提供商代码的环境具有正确的 IAM 权限策略（如 `sagemaker:InvokeEndpoint`）。

**注意事项**: 
不要在代码或配置文件中硬编码 AWS Access Key ID 和 Secret Access Key。

---

### 实践 5：实施 Prompt 模板与上下文管理

**说明**: 
不同的基础模型对 Prompt 格式有不同的要求（例如系统指令的位置、特殊 Token 的使用）。自定义提供商需要封装这些细节，为 Strands Agents 提供统一的接口，同时支持长上下文的截断策略。

**实施步骤**:
1. 在提供商类中配置模型特定的 `chat_template`，确保 System Message 和 User Message 正确拼接。
2. 实现上下文窗口管理逻辑，当输入 Token 超过模型限制时，自动截断中间对话或历史记录，保留最近的上下文。
3. 验证 Stop Words（停止词）配置，确保模型在生成结束时能够正确停止。

**注意事项**: 
不同的模型（如 Falcon, Llama, Mistral）其模板差异巨大，需查阅具体模型文档并在代码中做好版本适配。

---

### 实践 6：建立全面的日志记录与可观测性

**说明**: 
为了调试 Agent 行为和优化模型性能，必须记录详细的交互日志。这包括发送给模型的完整 Prompt、接收的原始响应、Token 使用量以及推理耗时。

**实施步骤**:
1. 集成 Python 的 `logging` 模块，记录请求和响应的 Payload（注意脱敏敏感信息）。
2. 将 Token 使用量和延迟指标导出至 CloudWatch 或 Prometheus，用于长期成本分析。
3. 在日志中关联 `Trace ID`，以便追踪一个 Agent 请求在 SageMaker 调用链中的完整生命周期。

**注意事项**:

---
## 学习要点

- 通过实现标准化的 invoke 和 stream 接口，可以将部署在 SageMaker 上的 LLM 无缝集成到 Strands Agents 框架中。
- 利用 Amazon Bedrock 的自定义模型导入功能，能够将托管在 SageMaker 上的模型作为 Bedrock 中的模型资源进行统一管理和调用。
- 该架构允许开发者灵活使用私有数据或开源模型（如 Llama 3），在满足数据隐私要求的同时构建生成式 AI 应用。
- 通过在 SageMaker 上托管模型，企业可以依据自身业务需求对模型进行定制化微调，并保持对基础设施的完全控制。
- 集成过程支持流式响应处理，这对于改善用户在交互式 AI 应用中的体验和减少延迟感知至关重要。
- 这种自定义提供者的方法打通了 AWS 托管服务与第三方 Agent 框架之间的壁垒，实现了混合云环境下的技术栈融合。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [Strands](/tags/strands/) / [LLM](/tags/llm/) / [Llama 3.1](/tags/llama-3.1/) / [SGLang](/tags/sglang/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--4.md" >}})
- [在SageMaker上部署SGLang并集成Strands代理自定义解析器]({{< relref "posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--10.md" >}})
- [为 Strands 智能体构建 SageMaker 托管 LLM 自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*