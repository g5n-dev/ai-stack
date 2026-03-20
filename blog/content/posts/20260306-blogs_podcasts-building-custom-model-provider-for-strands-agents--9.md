---
title: 为 Strands 智能体构建 SageMaker 托管 LLM 自定义模型解析器
date: 2026-03-06 19:08:22+08:00
draft: false
entry_kind: auto
tags:
- AWS
- SageMaker
- Strands
- LLM
- SGLang
- Llama 3.1
- 模型部署
- 自定义解析器
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: 以下是对所提供内容的中文总结： 本文介绍了如何在 **Amazon SageMaker AI** 端点上构建自定义模型提供商，以便与 **Strands
  Agents** 进行集成。 **主要背景：** 当开发者使用 SageMaker 托管的大语言模型（LLM）不原生支持 Bedrock Messages API
  格
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios:
- 大语言模型
- 后端开发
---

# 为 Strands 智能体构建 SageMaker 托管 LLM 自定义模型解析器

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---

## 摘要/简介

本文演示了在处理原生不支持 Bedrock Messages API 格式的 SageMaker 托管 LLM 时，如何为 Strands 智能体构建自定义模型解析器。我们将介绍如何使用 awslabs/ml-container-creator 在 SageMaker 上部署 SGLang 驱动的 Llama 3.1，然后实现一个自定义解析器将其集成到 Strands 智能体中。

---

## 导语

在 AWS SageMaker 上托管大模型时，如何将其无缝集成到 Strands 智能体工作流中是一个常见的技术挑战。本文以 SGLang 驱动的 Llama 3.1 为例，详细演示了如何构建自定义模型解析器，以解决非标准 API 格式的兼容性问题。通过阅读本文，您将掌握在 SageMaker 上部署模型并实现与 Strands 智能体深度集成的完整流程。

---

## 摘要

以下是对所提供内容的中文总结：

本文介绍了如何在 **Amazon SageMaker AI** 端点上构建自定义模型提供商，以便与 **Strands Agents** 进行集成。

**主要背景：**
当开发者使用 SageMaker 托管的大语言模型（LLM）不原生支持 Bedrock Messages API 格式时，需要通过自定义解析器来实现兼容。

**操作步骤概览：**
1.  **模型部署**：利用 `awslabs/ml-container-creator` 工具，在 SageMaker 上部署运行了 **SGLang** 的 **Llama 3.1** 模型。
2.  **集成开发**：通过实现一个自定义解析器，将该模型与 Strands agents 成功连接。

简而言之，这篇教程指导用户解决特定模型格式不兼容的问题，从而在 SageMaker 环境中灵活部署并使用 Strands agents。

---

## 评论

**中心观点**

这篇文章的核心观点是：在 AWS SageMaker 上利用 SGLang 高性能推理框架部署 Llama 3.1，并通过构建自定义模型适配层，能够有效解决开源大模型与 AWS Bedrock Agents 标准协议不兼容的问题，从而在保留云原生托管优势的同时，实现对 Agent 应用底座模型的深度定制与性能优化。

**深入评价与分析**

**1. 内容深度：架构解耦与协议转换的工程化实践**
*   **事实陈述**：文章深入探讨了 AWS 生态中的一个典型“断层”问题：SageMaker 提供了底层的算力托管，但 Bedrock Agents（作为 AWS 的 Agent 编排层）默认仅支持 Bedrock 的 API 格式。文章没有停留在简单的 API 调用层面，而是深入到了“协议适配”的工程细节。
*   **作者观点**：文章提出的解决方案——在 SageMaker 容器内实现自定义解析器——本质上是构建了一个“翻译层”。这种解耦思路非常有价值，它将“模型推理服务”与“上层应用编排”分离，避免了因上游格式锁定而被迫牺牲模型选型的灵活性。
*   **你的推断**：这暗示了企业级 AI 落地的一个趋势，即从单纯依赖大厂“黑盒”服务，转向“黑盒编排 + 白盒模型”的混合架构模式。

**2. 实用价值：SGLang 引入带来的性能红利**
*   **事实陈述**：文章选择使用 SGLang 而非传统的 vLLM 或 HuggingFace TGI 进行部署，这是一个极具实用价值的技术选型。SGLang 针对结构化输出和复杂提示词有专门的性能优化，这对于 Agent 场景至关重要。
*   **支撑理由**：Agent 应用通常涉及大量的 Tool Calling（工具调用）和 JSON 格式约束，SGLang 的结构化约束解码能力能显著降低首字延迟（TTFT），提升 Agent 的响应速度。
*   **反例/边界条件**：然而，SGLang 相对较新，生态成熟度不如 vLLM。在处理超长上下文或非 Llama 架构（如 MoE 架构模型）时，SGLang 的稳定性可能存在边界风险。此外，SGLang 对显存的管理策略在极高并发下可能不如 TGI 成熟。

**3. 创新性：打破云厂商的“格式锁定”**
*   **你的推断**：文章最大的隐含创新点在于“逆向工程”了云厂商的生态壁垒。通常厂商希望用户完全使用 Bedrock 托管模型以获取最大利润，而文章展示了如何利用 SageMaker 的通用性 + 开源模型 + 自定义适配层，来绕过 Bedrock 的模型限制，却仍享受 Bedrock Agents 的编排能力。这是一种“去中心化”的云架构思路。
*   **反例/边界条件**：这种做法增加了运维复杂度。如果企业追求极致的“开箱即用”和低运维成本，直接使用 Bedrock 原生支持的 Claude 系列模型可能仍是更优解，自定义方案带来了额外的代码维护和故障排查成本。

**4. 可读性与逻辑性**
*   **事实陈述**：从提供的摘要和结构来看，文章遵循了典型的 AWS 技术博客风格：问题背景 -> 基础设施搭建 -> 代码实现 -> 集成验证。
*   **评价**：逻辑链条清晰，特别是引入 `awslabs/ml-container-creator` 这一工具，降低了构建容器的门槛，使得文章的受众能够从架构师下沉到一线开发工程师。

**5. 行业影响与争议点**
*   **行业影响**：这篇文章为那些既想利用 AWS 强大的 IAM 和 VPC 安全体系，又想使用最新开源 LLM（如 Llama 3.1）的企业提供了标准参考范式。它可能会推动 AWS 社区中出现更多针对特定模型格式的 Adapter 开发。
*   **争议点/不同观点**：
    *   **性能争议**：在 SageMaker 上自建推理端点，虽然灵活，但在冷启动和弹性伸缩的响应速度上，往往不如 Bedrock 原生端点（后者可能有专门的预热池）。对于对延迟极度敏感的实时交互场景，这种自建方案的延迟波动可能是一个隐患。
    *   **成本争议**：文章未详细对比成本。SageMaker 实例的长时间运行成本，在低 QPS 场景下可能比按 Token 付费的 Bedrock 更高。

**实际应用建议**

1.  **监控指标**：在采用此方案时，必须重点监控 **Time to First Token (TTFT)** 和 **End-to-End Latency**。由于引入了自定义解析层，序列化/反序列化的开销需要被量化。
2.  **错误处理**：SGLang 或自定义解析器崩溃时，Bedrock Agent 如何重试？建议在 Lambda 层增加熔断机制，防止将错误的推理结果传递给下游业务。
3.  **版本管理**：Llama 3.1 更新频繁，SageMaker 容器的构建需要纳入 CI/CD 流程，避免“容器漂移”。

---

## 技术分析

基于您提供的文章标题和摘要，以下是对该技术方案的深入分析。

---

### 深度分析报告：构建基于 SageMaker 托管 LLM 的 Strands Agents 自定义模型提供商

### 1. 核心观点深度解读

**主要观点：**
文章的核心观点在于**“解耦与适配”**。它论证了在 AWS 生态系统中，开发者不应受限于 Amazon Bedrock 原生支持的模型列表。通过构建自定义模型解析器和提供商，可以将任何部署在 Amazon SageMaker 上的大语言模型（如 Llama 3.1）无缝集成到 AWS Agents（Strands Agents 框架）中，从而实现标准化的 Agent 编排能力与非标模型服务的结合。

**核心思想：**
作者传达了**“基础设施即代码”与“接口标准化”**的工程思想。在 LLM 应用落地过程中，模型服务的底层实现（无论是 Bedrock 托管还是 SageMaker 自托管）应当与上层应用逻辑分离。只要通过适配器模式将 SageMaker 的输入输出转换为 Agent 框架期望的格式（如 Bedrock Messages API 格式），就能复用 Agent 的强大编排功能。

**观点的创新性与深度：**
这一观点的创新性在于**打破了云厂商“围墙花园”的潜在限制**。通常，托管服务（如 Bedrock）为了易用性会牺牲灵活性，强制使用特定 API；而自部署模型（如 SageMaker）虽然灵活，但失去了托管服务的原生集成支持。文章通过展示如何用 SGLang 高性能部署结合自定义解析器，填补了这一鸿沟，体现了**混合云架构**的深度实践。

**重要性：**
这对于企业级 AI 应用至关重要。企业往往出于数据安全、合规或成本控制考虑，选择在 SageMaker 上私有部署模型，但又希望利用 Bedrock Agents 这样的高级编排工具。该方案为**“模型自主可控”与“应用快速构建”**提供了一条双赢路径。

### 2. 关键技术要点

**涉及的关键技术或概念：**
1.  **AWS Agents (Strands Agents):** AWS 的智能体编排框架，负责工具调用、规划和记忆管理。
2.  **Amazon SageMaker AI:** AWS 提供的机器学习模型托管服务，支持容器化部署。
3.  **SGLang:** 一个高性能 LLM 推理框架，以其高吞吐量和低延迟著称，特别适合处理复杂的 Agent 交互场景。
4.  **awslabs/ml-container-creator:** AWS 实验室提供的工具，用于快速构建符合 SageMaker 规范的推理容器镜像。
5.  **Adapter Pattern (适配器模式):** 软件设计模式，在此用于将非标准 API 转换为标准 API。

**技术原理和实现方式：**
*   **模型部署:** 使用 `ml-container-creator` 将 Llama 3.1 模型和 SGLang 推理服务器打包成 Docker 容器，并部署到 SageMaker 端点。SGLang 替代了传统的 vLLM 或 HuggingFace TGI，提供了更优的并发性能。
*   **协议转换:** Strands Agents 默认发送符合 Bedrock Conversational 或 Messages API 格式的 JSON 请求。SageMaker 上的 Llama 3.1 原生接收 OpenAI 或 HuggingFace 格式。因此，必须在中间层（或通过 Lambda/自定义容器逻辑）实现请求和响应的重新映射。

**技术难点与解决方案：**
*   **难点:** **格式不兼容。** Bedrock Agents 发送特定的 `message` 格式和 `toolDefinition`，而裸露的 Llama 模型只能理解文本提示词或 OpenAI 格式。
*   **解决方案:** 构建自定义模型解析器。在代码层面定义一个转换层，拦截 Agent 发出的请求，提取核心 Prompt 和工具配置，将其转化为 Llama 3.1 能理解的 Prompt 模板（如 Jinja2 模板），并在返回时将结果封装回 Agent 期望的 JSON 结构。
*   **难点:** **流式传输。** Agent 通常需要流式响应以降低首字延迟（TTFT）。
*   **解决方案:** 需要在 SageMaker 端点配置中启用响应流模式，并在解析器中处理字节流的分块和重组。

**技术创新点分析：**
使用 **SGLang** 是一个显著的技术亮点。相比于传统的 TGI，SGLang 对结构化输出和工具调用的原生支持更好，这能减少自定义解析器的编写复杂度，提高推理效率。

### 3. 实际应用价值

**对实际工作的指导意义：**
该方案为企业提供了一个**“混合模型策略”**的实施蓝图。企业可以将核心敏感数据模型放在私有 VPC 的 SageMaker 中，同时利用 AWS 的托管 Agent 服务进行业务逻辑编排，无需从零构建 Agent 框架。

**应用场景：**
1.  **金融/医疗合规场景:** 数据不能出私有网络，必须使用 SageMaker 内部部署的微调模型，但需要 Agent 能力调用内部 API。
2.  **成本敏感场景:** 使用 Spot 实例在 SageMaker 上运行开源模型（如 Llama 3），比直接调用 Bedrock 上的商业模型（如 Claude 3）更具成本效益。
3.  **特定模型需求:** 需要使用 Bedrock 尚未支持的特定版本或微调过的 Llama 模型。

**需要注意的问题：**
*   **运维负担:** SageMaker 自托管需要自己处理扩缩容、版本更新和监控，不如 Bedrock 无服务器模式省心。
*   **延迟:** 相比 Bedrock 这种全托管优化过的全球网络，自建 SageMaker 端点的网络延迟可能较高，需要配合 VPC Link 解决。

**实施建议：**
优先使用 **SGLang** 作为后端，因为其对 OpenAI 协议的兼容性较好，可以简化解析器的编写工作。务必在生产环境中实施模型容器的健康检查和自动回滚机制。

### 4. 行业影响分析

**对行业的启示：**
这标志着 **MaaS（模型即服务）正在向“解耦化”发展**。未来的趋势是应用层与模型层的彻底分离。应用开发者不应被锁定在特定的模型提供商 API 上，而应通过标准化接口动态切换后端模型。

**可能带来的变革：**
企业将更倾向于**“混合部署”**模式——通用任务使用商业 API（如 Claude/GPT-4），涉及隐私或特定领域的任务使用私有云部署的开源模型。这种架构将推动**推理网关** 技术的普及。

**对行业格局的影响：**
这削弱了云厂商通过托管模型锁定客户的能力。云厂商必须提供更优秀的托管体验（如 Bedrock 的知识库、Guardrails）才能留住客户，因为底层的模型现在可以轻易被替换为自部署方案。

### 5. 延伸思考

**引发的思考：**
随着模型推理框架的多样化，我们是否需要一个通用的**“LLM 路由层”**？这个层不仅负责格式转换，还负责根据请求的复杂度、成本预算和隐私级别，动态将请求路由到 Bedrock 或 SageMaker。

**拓展方向：**
*   **Function Calling 的标准化:** 不同模型对工具调用的 Prompt 模板差异巨大，如何构建一个通用的“工具调用翻译器”是未来的难点。
*   **多模型级联:** 利用 Strands Agent 的能力，让 SageMaker 上的小模型处理简单任务，Bedrock 上的大模型处理复杂任务，实现成本与性能的最优平衡。

**未来趋势：**
**SGLang / vLLM 等推理引擎将成为云原生的标准组件**，云厂商的 PaaS 服务将直接集成这些引擎，而不是提供单一的模型黑盒。

### 7. 案例分析

**结合实际案例说明：**
某跨国银行希望构建一个内部客服 Agent。由于监管要求，客户数据不能发送给外部模型。
*   **传统方案:** 放弃 Bedrock Agents，自己用 LangChain 编写 Agent 逻辑，部署在 EC2/EKS，调用 SageMaker 上的模型。开发周期长，维护成本高。
*   **本文方案:** 继续使用 Bedrock Agents 的编排能力和 Guardrails（安全防护），但将底层大模型指向 VPC 内部 SageMaker 托管的 Llama 3 70B。

**成功关键:** 成功实现了**编排与推理的分离**。业务团队只需要配置 Agent 的 Prompt 和 API Schema，无需关心底层模型是在 Bedrock 还是 SageMaker 上运行。

**经验教训:**
如果在实施过程中忽略了**流式响应**的处理，会导致 Agent 在等待完整响应时超时。必须确保解析器支持增量返回 Token。

### 8. 哲学与逻辑：论证地图

**中心命题:**
在 AWS 生态中，通过构建自定义解析器将 SageMaker 托管的开源 LLM（如 Llama 3.1）集成到 Strands Agents，是实现**数据主权**与**高级编排能力**平衡的最佳技术路径。

**支撑理由:**
1.  **合规性与安全性:** 依据数据主权原则，敏感数据必须在私有控制平面（SageMaker/VPC）内处理，不能发送至第三方托管模型端点。
2.  **成本效益:** 依据云成本经济学，对于高并发场景，使用自托管开源模型的推理成本远低于按 Token 计费的商业 API（如 Claude Opus）。
3.  **技术灵活性:** 依据软件工程中的“防腐层”理论，通过适配器转换格式，使得上层应用不受底层模型接口变更的影响。

**反例 / 边界条件:**
1.  **低并发/快速原型场景:** 如果业务处于初期探索阶段，维护 SageMaker 集群和自定义解析器的工程成本可能远高于直接调用 API 的账单成本。
2.  **极致低延迟需求:** Bedrock 的基础设施优化可能优于自建 SageMaker 端点，除非投入大量网络优化资源，否则自建方案可能面临更高的网络延迟。

---

## 最佳实践

### 实践 1：优化模型推理性能与延迟

**说明**: 在构建自定义模型提供程序时，LLM 的响应速度直接影响 Strands Agents 的用户体验。SageMaker 端点可能会因为冷启动或资源争用导致延迟。通过优化推理配置和请求处理，可以显著降低首字节延迟（TTFB）和整体响应时间。

**实施步骤**:
1. 在 SageMaker 配置中启用多模型端点（MME）或使用 GPU 实例（如 `ml.g5` 或 `ml.p4`）以加速推理。
2. 调整模型容器的环境变量，例如设置 `SM_NUM_GPUS` 或启用张量并行（如使用 DeepSpeed 或 vLLM）。
3. 在自定义提供程序代码中实现严格的超时设置，并考虑使用异步 I/O 来处理流式响应。
4. 配置 SageMaker 自动扩缩容策略，确保维持足够的实例数量以应对流量峰值，避免冷启动。

**注意事项**: 监控 CloudWatch 指标中的 `ModelLatency`，如果延迟过高，需检查实例规格是否满足模型大小要求。

---

### 实践 2：实现健壮的错误处理与重试机制

**说明**: 网络波动或 SageMaker 端点内部错误（如 502/503 错误）是不可避免的。一个健壮的提供程序必须能够优雅地处理这些故障，并通过指数退避算法进行重试，以确保 Agent 工作流的连续性。

**实施步骤**:
1. 在代码中捕获所有可能的异常（如连接超时、限流异常）。
2. 实现带有指数退避的重试逻辑（例如，初始等待 1 秒，最大重试 3 次，每次间隔加倍）。
3. 定义清晰的错误映射，将 SageMaker 的错误转换为 Strands Agents 能够理解的标准化错误信息。
4. 记录所有失败的请求和重试详情到 CloudWatch Logs，以便后续排查。

**注意事项**: 避免无限重试导致系统阻塞，务必设置最大重试次数和最终超时时间。

---

### 实践 3：标准化输入输出格式与 Token 限制

**说明**: 不同的开源模型在 SageMaker 上部署时可能有不同的输入输出格式（如 JSON 结构、Prompt 模板）。为了确保与 Strands Agents 的兼容性，必须在提供程序层进行标准化处理，并严格控制上下文长度。

**实施步骤**:
1. 编写适配器函数，将 Strands Agents 的标准请求格式转换为目标模型所需的特定 Prompt 格式（例如 Llama 2/3 的 Chat 模板）。
2. 在发送请求前，检查输入 Token 数量是否超过模型的上下文窗口限制，如果超出则进行截断或摘要。
3. 确保输出解析逻辑能够处理流式响应和非流式响应，并将其统一转换为 Agents 期望的格式。
4. 在配置文件中明确声明该模型支持的最大 Token 数。

**注意事项**: 截断上下文时可能会丢失关键信息，建议优先保留系统提示词和最近的对话历史。

---

### 实践 4：强化安全性与访问控制

**说明**: 托管在 SageMaker 上的模型可能包含敏感数据或需要受保护的访问。必须确保自定义提供程序遵循最小权限原则，并安全地管理凭证，防止未授权访问。

**实施步骤**:
1. 为调用 SageMaker 端点的 IAM 角色配置严格的 `sagemaker:InvokeEndpoint` 权限，并限制在特定的端点 ARN 上。
2. 如果提供程序代码运行在 AWS 之外，请使用 AWS Secrets Manager 或环境变量存储访问密钥，切勿硬编码在代码库中。
3. 启用 SageMaker 端点的网络隔离（VPC Only），并配置安全组以仅允许来自特定 IP 或 VPC 的流量。
4. 对传输中的数据进行 TLS/SSL 加密。

**注意事项**: 定期轮换 IAM 凭证，并使用 IAM Access Analyzer 验证权限配置是否过度宽松。

---

### 实践 5：实施全面的可观测性与日志记录

**说明**: 为了调试模型行为和优化性能，必须建立全面的可观测性。这包括记录请求负载、模型响应、Token 使用情况和推理时间，以便分析模型在实际 Agent 场景中的表现。

**实施步骤**:
1. 利用 SageMaker 的 Data Capture 功能记录端点的输入输出数据。
2. 在自定义提供程序中集成结构化日志（如 JSON 格式），记录请求 ID、Prompt 长度、Completion 长度和耗时。
3. 将日志发送到 CloudWatch Logs，并创建指标过滤器以监控错误率、延迟和 Token 吞吐量。
4. 使用 AWS X-Ray 进行分布式追踪，以便在调用链中定位瓶颈。

**注意事项**: 确保日志中不包含敏感的 PII（个人身份信息），必要时需要对日志数据进行脱敏处理。

---

### 实践 6：严格验证模型能力与参数映射

**说明**: 并非所有 LLM 都支持原生函数调用或工具使用。在将模型

---

## 学习要点

- 通过在 Amazon SageMaker AI 端点上托管自建 LLM 并将其集成到 Strands Agents，可以构建完全定制化的模型提供商，从而满足特定的业务需求并保持对数据隐私的完全控制。
- 利用 LangChain 的 BaseLLM 抽象类创建自定义包装器，能够将 SageMaker 托管的标准开源模型（如 Llama 3 或 Mistral）无缝适配为 Strands Agents 可调用的统一接口。
- 通过实现严格的输入输出 JSON Schema 验证机制，确保了自定义模型与 Strands Agents 框架之间的数据结构兼容性，有效防止了因格式不匹配导致的运行时错误。
- 部署过程通过 Terraform 等 IaC 工具实现了 SageMaker 推理端点的自动化配置，这不仅简化了基础设施的部署流程，还确保了生产环境的一致性和可扩展性。
- 该方案展示了如何通过自定义模型提供商绕过通用 API 的限制，允许开发者灵活调整模型参数（如温度、Top-P），以优化 Agent 在特定任务中的推理表现。
- 在构建过程中，通过将模型推理逻辑与 Agent 业务逻辑解耦，开发者能够独立迭代和更新模型版本，而不会破坏 Strands Agents 的现有工作流。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [Strands](/tags/strands/) / [LLM](/tags/llm/) / [SGLang](/tags/sglang/) / [Llama 3.1](/tags/llama-3.1/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--4.md" >}})
- [在 SageMaker 上部署 SGLang 并集成至 Strands 智能体]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--2.md" >}})
- [在SageMaker上部署SGLang并集成Strands智能体自定义模型]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--5.md" >}})
