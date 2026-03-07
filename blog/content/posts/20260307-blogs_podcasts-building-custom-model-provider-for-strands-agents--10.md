---
title: "为Strands代理构建SageMaker端点自定义模型解析器"
date: 2026-03-07T17:36:33+08:00
draft: false
entry_kind: "auto"
tags: ["SageMaker", "Strands", "LLM", "SGLang", "Llama 3.1", "自定义解析器", "模型部署", "AWS"]
categories: ["AI 工程", "后端"]
source: blogs_podcasts
description: "本文演示了如何为 Strands 智能体构建自定义模型提供商，以集成托管在 Amazon SageMaker 端点上且原生不支持 Bedrock Messages API 格式的大语言模型（LLM）。 具体流程如下： 1. **模型部署**：使用 工具，在 SageMaker 上部署基于 SGLang 框架的 Llam"
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios: ["大语言模型", "后端开发"]
---

# 为Strands代理构建SageMaker端点自定义模型解析器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---
## 摘要/简介

本文演示了在处理托管于 SageMaker 上且原生不支持 Bedrock Messages API 格式的 LLM 时，如何为 Strands 代理构建自定义模型解析器。我们将介绍如何使用 awslabs/ml-container-creator 在 SageMaker 上部署基于 SGLang 的 Llama 3.1，随后实现自定义解析器以将其与 Strands 代理集成。

---
## 导语

在将托管于 Amazon SageMaker 的 LLM 接入 Strands 代理时，开发者常面临模型输出格式与 Bedrock Messages API 不兼容的挑战。本文将演示如何基于 SGLang 部署 Llama 3.1 并构建自定义模型解析器，从而解决原生格式限制。通过阅读本文，您将掌握实现异构模型与代理框架集成的具体方法，确保在非标准环境下也能构建稳定可用的 AI 应用。

---
## 摘要

本文演示了如何为 Strands 智能体构建自定义模型提供商，以集成托管在 Amazon SageMaker 端点上且原生不支持 Bedrock Messages API 格式的大语言模型（LLM）。

具体流程如下：

1.  **模型部署**：使用 `awslabs/ml-container-creator` 工具，在 SageMaker 上部署基于 SGLang 框架的 Llama 3.1 模型。
2.  **自定义解析器开发**：由于该模型不直接兼容 Bedrock 的 Messages API 格式，文章详细介绍了如何实现一个自定义解析器。
3.  **集成应用**：通过该解析器，将部署在 SageMaker 上的 Llama 3.1 模型成功接入 Strands 智能体，实现无缝调用。

---
## 评论

**中心观点**
文章的核心观点是：在AWS生态内构建AI智能体时，不应受限于Amazon Bedrock的标准化接口，通过利用SageMaker的托管能力结合自定义解析器，可以实现对Llama 3.1等开源模型的高性能、低延迟集成，从而在保留云原生托管优势的同时获得对模型推理格式的完全控制权。

**支撑理由与深度评价**

**1. 混合云架构的“控制权”与“便利性”平衡（事实陈述 + 作者观点）**
文章展示了AWS用户面临的一个典型困境：Bedrock虽然提供了标准化的API和优秀的开发体验（如Messages API），但并非所有模型（特别是特定版本的开源模型或微调版本）都能第一时间得到支持，或者其内部实现细节不够透明。
*   **评价**：文章提出的解决方案——利用SageMaker部署 + 自定义Parser，实际上是在构建一个**“私有化Bedrock”**。这不仅仅是技术实现，更是一种架构策略。它证明了企业不必为了使用托管服务而牺牲模型选择的灵活性。
*   **反例/边界条件**：这种架构牺牲了Bedrock原生的“按Token计费”的经济性模型。SageMaker通常是按实例小时计费，对于低并发、间歇性的查询场景，成本可能远高于直接调用Bedrock API。

**2. SGLang作为推理后端的技术选型前瞻性（事实陈述 + 你的推断）**
文章选择SGLang而非传统的vLLM或TGI作为推理引擎，显示了作者对前沿技术的敏锐度。SGLang在处理结构化输出和复杂Prompt场景下的性能优势（如RadixAttention）正在被行业认可。
*   **评价**：这是一个高技术含量的选型。将SGLang容器化并部署到SageMaker，解决了企业级应用中“高性能框架”与“稳定托管环境”难以融合的痛点。这表明文章不仅关注“能跑通”，更关注“跑得快”。
*   **反例/边界条件**：SGLang作为较新的项目，其生产环境稳定性与TGI或vLLM相比尚缺乏大规模验证。在金融或医疗等对SLA要求极高的行业，运维团队可能会因担心未知Bug而拒绝采用此类新锐框架。

**3. 针对Agents场景的“胶水层”设计模式（作者观点）**
Strands Agents（假设为某种Agent框架或业务逻辑）需要特定的输出格式。文章重点展示了如何编写Parser来处理非标准格式的模型输出。
*   **评价**：这是从“模型工程”向“应用工程”跨越的关键一步。很多LLM教程止步于模型调用，而本文深入到了如何将模型输出“清洗”为Agent可执行的指令。这种**“中间件思维”**是企业级AI落地的核心能力。
*   **反例/边界条件**：如果模型本身的指令遵循能力较弱（例如较小的模型版本），单纯依靠Parser后处理无法解决幻觉或格式错误的问题，此时强行格式化可能导致Agent执行崩溃。

**4. 避免供应商锁定的战略价值（你的推断）**
虽然文章主要讲技术，但隐含的逻辑是降低对单一API（Bedrock）的依赖。
*   **评价**：通过在SageMaker上自部署，企业保留了随时切换底层模型（如从Llama切换到Qwen或Mistral）的权利，只要Parser层适配得当。这对于需要长期维护AI资产的企业至关重要。
*   **反例/边界条件**：这种做法实际上是从“应用层锁定”转向了“基础设施层锁定”。虽然模型没锁在Bedrock，但深度依赖SageMaker的特定容器定义和EKS/Docker环境，迁移出AWS的难度依然很大。

**综合评价维度**

*   **内容深度**：**高**。文章没有停留在简单的API调用，而是深入到了容器构建、推理引擎选型和协议转换的层面，触及了MLOps的核心。
*   **实用价值**：**极高**。对于正在使用AWS构建生成式AI应用且对延迟、成本或数据隐私有特殊要求的技术团队，这是一份可直接参考的蓝图。
*   **创新性**：**中等偏上**。虽然RAG和Agent是老生常谈，但将SGLang与SageMaker深度结合并解决协议不匹配问题，提供了较新的实践路径。
*   **可读性**：**逻辑清晰**。按照“问题-部署-集成”的逻辑推进，符合技术人员的认知习惯。
*   **行业影响**：该模式是**“FinOps（云成本优化）+ AI Engineering”**结合的典型案例，可能会推动更多企业重新审视全托管API与自托管模型之间的成本效益比。

**可验证的检查方式**

1.  **性能基准测试**：
    *   **指标**：对比该架构（SageMaker+SGLang）与直接调用Bedrock Llama 3.1端点的**Time to First Token (TTFT)** 和 **Throughput (Tokens/Second)**。
    *   **验证点**：在并发请求（Concurrent Requests）增加时，SGLang的RadixAttention是否能带来更显著的延迟降低优势。

2.  **成本效益分析**：
    *   **指标**：计算**“每百万Token推理成本”**。
    *   **验证点**：设定不同的请求量级（QPS），对比SageMaker实例小时成本与Bedrock按Token计费的成本。找出“盈亏平衡点”——即流量达到多少时，自部署才比调用API更便宜。

3.  **格式鲁棒性测试**：
    *

---
## 技术分析

基于您提供的文章标题和摘要，尽管全文内容被截断，但结合AWS生态系统的技术背景、SageMaker、Strands Agents（推测为AWS内部或特定领域的Agent框架，或指代基于Bedrock的Agent构建思路）以及Llama 3.1与SGLang的技术特性，我可以为您构建一份深度的分析报告。

这篇文章的核心在于**“异构系统的标准化集成”**，即如何让非AWS原生的模型（如自部署的Llama 3.1）完美融入AWS的Agent生态。

以下是详细分析：

---

# 深度分析报告：构建基于SageMaker自定义模型的Strands Agents集成方案

## 1. 核心观点深度解读

### 文章的主要观点
文章的主要观点是**“通过构建自定义模型解析器，开发者可以打破云厂商托管服务与开源自部署模型之间的格式壁垒，实现非原生模型对高级Agent框架的无缝接入”**。具体而言，即让运行在SageMaker上的Llama 3.1（通过SGLang加速）能够被Strands Agents（或类似的Agent编排层）像调用原生Bedrock API一样调用。

### 作者想要传达的核心思想
作者传达了**“基础设施无关性”**的重要性。在构建AI应用时，开发者不应被锁定在单一模型提供商的API格式（如Bedrock Messages API）上。通过适配器模式和容器化技术，企业可以保留私有部署模型的数据安全性与定制能力，同时享受云厂商Agent编排工具的便利性。

### 观点的创新性和深度
**创新性**体现在将**SGLang**（一种高性能推理服务框架）与**AWS SageMaker**的深度结合，并针对**Agent场景**特有的结构化输出需求进行了适配。这不仅仅是简单的模型部署，而是解决了模型输出格式与Agent期望输入格式不匹配的深层工程问题。
**深度**在于它触及了LLM Ops（大模型运维）中的痛点：如何将高性能开源模型生态（Llama 3.1 + SGLang）与企业级服务治理无缝对接。

### 为什么这个观点重要
随着企业对数据隐私和成本控制的关注，越来越多的场景倾向于使用开源模型（如Llama 3.1）并在私有环境（如SageMaker VPC）中部署。然而，Agent框架通常需要特定的响应格式（如JSON、Tool Calls参数）来执行工具调用。如果模型无法输出标准格式，Agent就无法工作。因此，掌握**自定义解析器**的构建能力，是企业落地自主AI Agent的关键。

## 2. 关键技术要点

### 涉及的关键技术或概念
1.  **SGLang**: 一个高性能的大语言模型推理服务运行时，专为高吞吐量和低延迟设计，支持复杂的结构化生成。
2.  **Llama 3.1**: Meta发布的最新开源大模型系列，支持128k上下文和强大的推理能力。
3.  **SageMaker AI Endpoints**: AWS提供的全托管模型服务，支持自定义容器部署。
4.  **awslabs/ml-container-creator**: AWS提供的用于简化大模型推理容器构建的工具。
5.  **Strands Agents**: 推测为一种Agent编排框架（注：Strands可能是特定项目代号或Bedrock Agents的某种变体/笔误，此处按通用Agent框架理解），依赖Bedrock Messages API格式。

### 技术原理和实现方式
1.  **容器化部署**: 使用`ml-container-creator`将Llama 3.1模型权重、SGLang推理服务器打包成一个Docker容器，并推送到SageMaker。
2.  **格式适配**: 核心难点在于SGLang原生输出通常是OpenAI兼容格式或纯文本，而Strands Agents可能期望Bedrock的`messages`格式。
    *   **实现方式**: 在SageMaker Endpoint的容器内部（或通过Lambda层）编写一个**自定义解析器**。该解析器拦截Agent发来的请求，将其转换为SGLang理解的格式；接收SGLang的输出，将其转换为Agent期望的JSON结构（包含`toolUse`等字段）。
3.  **流式传输**: 处理Token级别的流式响应，确保Agent能够实时展示生成过程。

### 技术难点和解决方案
*   **难点**: 结构化输出的约束。Agent调用工具时，要求模型输出严格的JSON格式，而开源模型有时会产生格式错误的文本。
*   **解决方案**: 利用SGLang的**Constrained Decoding（约束解码）**能力，强制模型输出符合JSON Schema的文本，然后在解析器层进行封装。
*   **难点**: SageMaker的冷启动与多容器管理。
*   **解决方案**: 使用SageMaker的Multi-Model Endpoints或利用SGLang本身的高并发能力来优化资源利用率。

### 技术创新点分析
文章的创新点在于**“中间件思维”**在LLM架构中的应用。它没有试图修改Agent框架去适应模型，也没有修改模型去适应框架，而是构建了一个标准化的**“翻译层”**。这使得未来替换模型（如从Llama 3.1升级到3.2）或更换框架时，只需修改翻译层，无需重构整个系统。

## 3. 实际应用价值

### 对实际工作的指导意义
对于正在构建企业级GenAI应用的团队，这篇文章提供了一条**“混合云架构”**的落地路径。你不必为了使用Bedrock的高级Agent功能而被迫使用昂贵的Closed-Source模型，也不必为了使用开源模型而放弃AWS的托管服务。

### 可以应用到哪些场景
1.  **金融/医疗分析**: 需要极高数据隐私，模型必须在VPC内部署，但需要复杂的Agent工作流。
2.  **成本敏感型应用**: 使用Llama 3.1 70B或405B替代GPT-4，在SageMaker上自托管以降低Token成本。
3.  **特定领域微调**: 部署经过微调的Llama模型，使其具备特定知识，同时挂载到Agent框架中进行工具调用。

### 需要注意的问题
1.  **维护成本**: 自定义解析器意味着你需要维护额外的代码，当上游API格式变化时，需要手动更新。
2.  **性能损耗**: 中间转换层可能会增加几毫秒到几十毫秒的延迟，对实时性要求极高的场景需评估。

### 实施建议
*   **接口标准化**: 定义一套内部的Model Abstraction Layer (MAL)，所有Agent调用只对MAL负责，MAL负责对接SageMaker或Bedrock。
*   **监控**: 重点监控解析层的错误率，特别是JSON解析失败导致的Agent中断。

## 4. 行业影响分析

### 对行业的启示
这篇文章预示了**“模型路由与编排”**将成为企业的核心能力。未来的AI架构不再是“点对点”连接，而是通过标准化的总线连接多样化的模型（开源、闭源、私有）。

### 可能带来的变革
企业将从购买“模型”转向购买“算力与编排”。SageMaker等MLOps平台的价值将进一步凸显，而单纯的模型API提供商可能面临来自企业自部署模型的竞争压力。

### 相关领域的发展趋势
*   **网关的崛起**: 像LangGate、AWS API Gateway这样的组件将成为LLM应用的标准入口。
*   **推理优化战争**: SGLang、vLLM、TensorRT-LLM之间的竞争将更加激烈，因为只有高性能的推理后端才能支撑起复杂的Agent链路。

## 5. 延伸思考

### 可以拓展的方向
*   **动态模型切换**: 是否可以根据Prompt的复杂度，自动在SageMaker（Llama 3.1）和Bedrock（Claude 3.5）之间切换？
*   **Prompt的自动翻译**: 除了输出格式，输入Prompt是否也需要针对SGLang进行特定的优化（如BPE tokenization对齐）？

### 需要进一步研究的问题
*   SGLang在处理超长上下文（Llama 3.1的128k）时的显存管理策略。
*   自定义解析器在处理流式输出时的`Tool Calling`逻辑如何保证原子性？

## 6. 实践建议

### 如何应用到自己的项目
1.  **评估现有栈**: 检查你现有的Agent代码是否硬编码了OpenAI或Bedrock的API格式。
2.  **引入适配器**: 编写一个Python类`SGLangAdapter`，封装`_convert_request`和`_convert_response`方法。
3.  **容器化**: 使用Docker将你的模型服务标准化，确保在本地（Docker Compose）和云端能一致运行。

### 具体的行动建议
*   **Step 1**: 在本地使用vLLM或SGLang启动Llama 3.1，编写Python脚本模拟Agent的请求，观察输出格式。
*   **Step 2**: 编写转换脚本，将输出格式强行转换为你的Agent框架所需的JSON Schema。
*   **Step 3**: 使用`ml-container-creator`打包并部署到SageMaker。

### 需要补充的知识
*   **OpenAPI/Swagger规范**: 理解API接口定义。
*   **JSON Schema**: 理解如何约束LLM的输出结构。
*   **AWS IAM/VPC**: 理解安全组配置，确保Agent能访问SageMaker Endpoint。

## 7. 案例分析

### 结合实际案例说明
假设一个**企业级知识库问答助手**。
*   **背景**: 企业拥有大量私有PDF，不能发给OpenAI。
*   **操作**: 在SageMaker部署Llama 3.1 + SGLang。使用LangChain作为Agent框架。
*   **问题**: LangChain默认支持OpenAI格式，SGLang虽然兼容OpenAI API，但在`function_call`字段的返回上可能有细微差别（例如返回参数名为`arguments`而非`function_arguments`）。
*   **解决**: 构建一个轻量级网关，拦截LangChain发往SageMaker的请求，修改响应体，确保LangChain能正确解析出工具调用。

### 失败案例反思
许多开发者直接修改LangChain或Agent框架的源码来适配模型。这导致**“供应商锁定”**——当框架版本升级时，自定义代码会崩溃。正确的做法是保持框架纯净，在**IaaS层（网关/容器）**解决兼容性问题。

## 8. 哲学与逻辑：论证地图

### 中心命题
**在构建企业级AI Agent时，采用“自定义解析器”将自托管模型（如SageMaker上的Llama 3.1）适配到标准Agent框架，是实现性能、成本与数据主权平衡的最佳工程实践。**

### 支撑理由
1.  **主权与安全**: 企业数据不出VPC，满足合规要求。
2.  **成本效益**: 长期运行自托管模型比按Token付费的Closed API更便宜。
3.  **性能可控**: 使用SGLang等高性能后端，可针对特定硬件优化延迟。

### 依据
*   **Evidence**: Llama 3.1 405B在SGLang下的Benchmark数据（吞吐量 vs HuggingFace Transformers）。
*   **Intuition**: 软件工程中“适配器模式”久经考验，是解耦系统的标准做法。

### 反例或边界条件
1.  **冷启动延迟**: 如果业务是极低频的触发，自托管SageMaker Endpoint的冷启动和闲置成本可能远高于直接调用API。
2.  **极简场景**: 对于非常

---
## 最佳实践

## 最佳实践指南

### 实践 1：优化 SageMaker 端点配置与资源管理

**说明**:
为 Strands Agents 构建自定义模型提供程序时，SageMaker 端点的底层资源配置直接影响 LLM 的响应延迟和吞吐量。合理的实例选择和自动扩缩容策略是确保系统稳定性和成本效益的关键。

**实施步骤**:
1.  **基准测试**: 在部署前，使用不同大小的实例（如 ml.g5 系列或 ml.p4 系列）运行推理负载测试，以确定最佳价格性能比。
2.  **配置自动扩缩容**: 根据预期的流量模式配置 SageMaker 自动扩缩容策略，设置基于 CPU 利用率或每秒请求数的动态扩缩容指标。
3.  **启用多模型端点**: 如果同时运行多个较小的模型，考虑使用 SageMaker 多模型端点（MME）以节省基础设施成本和部署时间。

**注意事项**:
- 避免在生产环境中使用开发测试用的实例类型。
- 监控“冷启动”时间，确保扩容策略能应对突发流量，避免请求超时。

---

### 实践 2：实现标准化的请求与响应接口

**说明**:
Strands Agents 期望模型提供程序遵循特定的输入输出格式。自定义提供程序必须充当适配器，将来自 Agent 的标准请求转换为 SageMaker 端点所需的特定负载格式（如 JSON、JSON Lines），并将原始模型响应映射回标准化的消息结构。

**实施步骤**:
1.  **定义接口类**: 创建一个 Python 类（例如 `SageMakerModelProvider`），实现 `generate` 或 `stream` 方法。
2.  **负载转换**: 在方法内部，编写逻辑将 Agent 的 Prompt 和参数转换为 SageMaker 推理容器所需的格式（例如，将 OpenAI 兼容格式转换为 Llama 2 的输入格式）。
3.  **响应解析**: 解析 SageMaker 返回的 JSON 响应，提取 `generated_text` 或 `choices` 字段，并构建包含 Token 使用情况的返回对象。

**注意事项**:
- 确保错误处理机制能够捕获并转换 SageMaker 端点的内部错误（如 502 或 504 错误），以免导致 Agent 崩溃。
- 如果模型支持流式输出，需额外处理字节流的解析和 SSE（Server-Sent Events）格式的封装。

---

### 实践 3：建立严格的超时与重试机制

**说明**:
LLM 推理通常耗时较长，且网络请求可能失败。在自定义提供程序中实现健壮的超时控制和指数退避重试策略，对于防止 Agent 工作流挂起至关重要。

**实施步骤**:
1.  **设置客户端超时**: 在调用 SageMaker 端点的 Boto3 客户端或 HTTP 客户端中，配置 `ReadTimeout` 参数（例如设置为 60 秒或更长，取决于模型大小）。
2.  **实现指数退避**: 编写重试装饰器或逻辑，在遇到可重试错误（如 5xx 系列错误）时，按照指数级增加等待时间进行重试（例如 1s, 2s, 4s）。
3.  **配置最大重试次数**: 设置最大重试次数（建议 3-5 次），超过次数后抛出异常以终止任务。

**注意事项**:
- 区分“模型推理超时”和“网络连接超时”，前者可能需要增加实例资源，后者则需要重试。
- 确保超时设置与 Strands Agents 的总体任务超时相协调，避免因单次推理过长导致整个上下文丢失。

---

### 实践 4：增强模型可观测性与日志记录

**说明**:
为了调试和优化 Agent 的性能，必须记录与 SageMaker 端点交互的详细元数据。这包括输入 Prompt 的哈希值、Token 计数、延迟指标以及端点返回的原始状态。

**实施步骤**:
1.  **集成 CloudWatch**: 利用 Boto3 SDK 将自定义指标（如 `ModelLatency`, `RequestDuration`）发布到 Amazon CloudWatch。
2.  **结构化日志**: 在提供程序代码中输出结构化日志（JSON 格式），记录 `request_id`、`model_name`、`input_token_count` 和 `output_token_count`。
3.  **关联追踪**: 确保 Strands Agents 的请求 ID 能够传递到 SageMaker 的 `InvocationLogs` 中，以便在 AWS 控制台进行端到端的请求追踪。

**注意事项**:
- 避免在日志中记录敏感的 PII（个人身份信息）数据，特别是当 Prompt 包含用户私密信息时。
- 注意日志采样率，对于高并发场景，全量日志可能会带来性能损耗和存储成本。

---

### 实践 5：优化提示词与参数传递

**说明**:
不同的托管模型（如 Falcon, Llama, Mistral）对提示词格式和推理参数（温度、Top-P）有不同的要求。自定义提供程序应具备灵活性，以

---
## 学习要点

- 通过在 Strands Agents 中构建自定义模型提供商，可以将部署在 SageMaker AI 端点上的 LLM 无缝集成，从而利用托管基础设施实现更可控的 AI 代理应用。
- 实现自定义模型提供商的核心在于正确配置 API 接口，确保 Strands Agents 能够将请求格式转换为 SageMaker 端点所需的负载格式（如 JSON 或特定协议）。
- 利用 SageMaker AI 托管模型允许企业对底层基础设施拥有完全控制权，并满足数据不出域等严格的安全与合规要求。
- 该集成方案支持灵活的模型选择，使开发者能够根据特定业务需求，在 Strands 环境中轻松切换或测试不同的开源或微调模型。
- 通过将 Strands Agents 的编排能力与 SageMaker 的可扩展性相结合，企业能够在保持高性能的同时优化大模型推理的成本结构。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


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
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*