---
title: 在SageMaker上部署SGLang并集成Strands代理自定义模型
date: 2026-03-09 02:43:00+08:00
draft: false
entry_kind: auto
tags:
- SageMaker
- SGLang
- Llama 3.1
- Strands
- 模型部署
- 自定义解析器
- AWS
- LLM
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: 本文介绍了如何为 Amazon Strands Agents 构建自定义模型提供商，以便集成托管在 Amazon SageMaker AI
  端点上且不原生支持 Bedrock Messages API 格式的大语言模型（LLMs）。 主要内容如下： 1. **背景与目标**： 当用户希望在 Strands
  智能体中使用
external_url: https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints
scenarios:
- 大语言模型
- 后端开发
---

# 在SageMaker上部署SGLang并集成Strands代理自定义模型

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-05T16:15:41+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)

---

## 摘要/简介

本文演示了在 Amazon SageMaker 上使用不支持 Bedrock Messages API 格式的 LLM 时，如何为 Strands 代理构建自定义模型解析器。我们将引导您使用 awslabs/ml-container-creator 在 SageMaker 上部署基于 SGLang 的 Llama 3.1，然后实现一个自定义解析器，将其与 Strands 代理集成。

---

## 导语

在 Amazon SageMaker 上部署大模型时，如果所选模型不支持 Bedrock Messages API 的标准格式，将其集成至 Strands 代理往往面临兼容性挑战。本文将演示如何通过部署 SGLang 并实现自定义解析器来解决这个问题，从而打通模型与代理之间的交互壁垒。阅读后，您将掌握构建自定义模型提供者的完整流程，实现非标准格式模型与 Strands 代理的无缝对接。

---

## 摘要

本文介绍了如何为 Amazon Strands Agents 构建自定义模型提供商，以便集成托管在 Amazon SageMaker AI 端点上且不原生支持 Bedrock Messages API 格式的大语言模型（LLMs）。

主要内容如下：

1.  **背景与目标**：
    当用户希望在 Strands 智能体中使用托管在 SageMaker 上的 LLM（如 Llama 3.1），而这些模型未采用 Bedrock 原生 API 格式时，需要构建自定义解析器来实现集成。

2.  **部署流程**：
    文章演示了使用 `awslabs/ml-container-creator` 工具，在 SageMaker 上部署基于 SGLang 的 Llama 3.1 模型的具体步骤。

3.  **集成实现**：
    重点在于如何编写并实现自定义解析器，以处理特定的输入/输出格式，从而将该 SageMaker 端点成功接入 Strands 智能体系统。

---

## 评论

**中心观点**
文章提出了一种通过构建自定义模型解析器，将非标准接口的SageMaker托管大模型（如Llama 3.1）无缝集成到Strands Agents框架中的技术方案，旨在解决云托管模型与AI Agent框架之间的协议适配问题。

**支撑理由与深度评价**

**1. 解决了异构计算环境下的协议碎片化问题（事实陈述）**
文章的核心价值在于填补了AWS原生生态中的一个空白。Bedrock虽然提供了统一的Messages API，但许多企业出于数据合规、成本控制或特定模型性能（如SGLang的高吞吐量）考虑，选择在SageMaker上自托管模型。这些模型通常遵循OpenAI API或HuggingFace协议，无法直接被Strands Agents调用。文章提出的“自定义模型解析器”实际上是一个适配器层，这不仅是技术实现，更是一种架构模式的体现：**在多模型混合部署的场景下，标准化接入层比单一模型优化更具工程价值**。

**2. SGLang与SageMaker的结合强调了推理性能优化（作者观点）**
文章选择使用SGLang而非常见的vLLM或TGI（Text Generation Inference）作为推理引擎，显示了作者对前沿技术的关注。SGLang在处理结构化输出和长上下文时的性能优势（如RadixAttention技术），对于Agent应用至关重要。Agent应用频繁涉及Tool Calling和JSON格式化输出，SGLang在这些场景下的延迟表现通常优于传统推理后端。这表明文章不仅关注“能跑通”，还关注“跑得快”，符合当前Agent应用从Demo走向生产系统时对低延迟的刚性需求。

**3. 工具链的复用降低了DevOps复杂度（事实陈述）**
利用`awslabs/ml-container-creator`来打包Llama 3.1和SGLang，展示了AWS基础设施即代码的最佳实践。这种方法避免了手动编写复杂的Dockerfile，大大缩短了模型从开发到部署的周期。对于行业而言，这种标准化的构建流程是推动MLOps落地的关键，它将模型部署变成了一个可重复、可审计的工程任务，而非手工作业。

**反例与边界条件**
*   **边界条件1（维护成本）：** 自定义解析器虽然解决了接入问题，但也引入了额外的维护负担。当底层模型API版本升级（例如SGLang更新其API规范）或Strands框架变更时，适配器代码必须随之更新。如果企业内部接入了数十种不同的自托管模型，维护这些“胶水代码”的成本可能会超过Bedrock原生调用带来的溢价。
*   **边界条件2（性能损耗）：** 在Agent架构中，每一层代理调用都会增加延迟。文章展示的解析器逻辑如果处理不当（例如低效的字符串拼接或正则匹配），可能会成为高并发场景下的性能瓶颈。相比之下，Bedrock的On-Demand模式虽然单价高，但省去了服务器运维和中间层的网络开销。

**批判性分析与行业影响**

**创新性评价**
文章的创新性不在于发明了新算法，而在于**系统集成**。它展示了如何在一个受限的企业级云环境中，利用开源组件（Llama 3.1 + SGLang）构建出媲美托管服务的体验。这种“混合云AI架构”——核心控制流利用托管服务，核心模型利用私有化部署——是未来大型企业AI落地的主要趋势。

**争议点与不同观点**
*   **过度工程化 vs 灵活性：** 一种观点认为，既然SageMaker支持将容器端点配置为兼容OpenAI格式，Strands Agents理应直接支持通用的“OpenAI-compatible”接口，而不需要为每个模型编写特定的Python解析器。文章的做法可能被视为一种Workaround（变通方案），而非长久之计。如果Strands团队能在未来版本中原生支持“OpenAI兼容”端点配置，本文的代码逻辑将被废弃。
*   **锁定风险：** 虽然文章旨在逃离Bedrock的模型锁定，但它深度绑定了Strands Agents框架和SageMaker的基础设施。如果未来需要迁移到Azure或GCP，或者更换Agent框架（如LangChain或AutoGen），这部分定制化的代码迁移成本将很高。

**实际应用建议**
1.  **监控中间层性能：** 在生产环境中，必须对自定义解析器添加详细的延迟和吞吐量监控。确保解析器本身不是慢查询的源头。
2.  **抽象化设计：** 不要为每一个模型硬编码解析器。建议建立一个通用的“BaseParser”，通过配置文件（如YAML）定义Prompt Template和JSON Schema，以支持不同模型的快速接入，减少代码重复。
3.  **安全审查：** 自定义解析器直接处理LLM的原始输出，必须严格校验输出内容，防止通过Prompt Injection攻击绕过解析器逻辑，导致下游系统收到恶意指令。

---

## 技术分析

基于您提供的文章标题和摘要，尽管原文内容被截断，但结合AWS技术生态、SageMaker、Strands Agents（推测为AWS App Studio或内部Agent框架的代称/笔误，可能指代Amazon Bedrock Agents或自定义Agent架构）以及Llama 3.1与SGLang的最新技术趋势，以下是对该技术方案的深度全面分析。

---

### 深度分析：在SageMaker上构建自定义模型提供商以支持Strands Agents

### 1. 核心观点深度解读

**主要观点：**
文章的核心主张是**“去耦合化”与“标准化适配”**。它主张企业在构建生成式AI应用时，不应被锁定在单一的云厂商API格式（如Bedrock Messages API）中。通过构建自定义模型解析器，企业可以将部署在SageMaker上的高性能开源模型（如Llama 3.1）无缝集成到高级Agent框架中，从而在保持控制权的同时实现标准化交互。

**核心思想：**
作者传达了**“基础设施灵活性优于生态便利性”**的工程哲学。虽然直接使用Bedrock等托管服务最便捷，但出于数据主权、成本控制或特定性能需求，企业往往需要自部署模型。文章的核心在于展示如何通过工程手段消除“自部署模型”与“托管Agent服务”之间的鸿沟，即**通过适配器模式将非标准接口转化为标准接口**。

**创新性与深度：**
*   **创新性：** 结合了**SGLang**（这一高性能推理框架）与**SageMaker**，并针对**Agent场景**（而非简单的问答）进行了协议转换。这不仅仅是部署模型，更是部署“具备Agent能力的模型服务”。
*   **深度：** 深入到了**协议层**的转换。它解决了当模型输出格式（如JSON模式、工具调用格式）与Agent框架期望格式不一致时的底层处理逻辑。

**重要性：**
随着大模型从“玩具”走向“工具”，Agent（智能体）成为主流。然而，Agent对模型的**工具调用**能力有强依赖。如果自部署模型无法与Agent框架通信，企业将被迫放弃高性能开源模型而选择昂贵的API。这篇文章为企业提供了一条**“既享受开源模型红利，又享受生态编排便利”**的可行路径。

### 2. 关键技术要点

**涉及的关键技术：**
1.  **Amazon SageMaker:** 用于托管底层容器，提供扩缩容和基础设施管理。
2.  **SGLang:** 一个新兴的大模型推理运行时，以高吞吐量和低延迟著称，特别擅长处理复杂的结构化生成和并发请求。
3.  **Llama 3.1:** Meta发布的最新开源模型，支持128k上下文和强大的指令跟随能力。
4.  **awslabs/ml-container-creator:** AWS提供的工具，用于简化大模型推理容器的构建过程，自动处理CUDA、驱动和模型服务器的依赖。
5.  **Custom Model Parsers (自定义模型解析器):** 代码层面的适配器，用于将SGLang的输出转换为Strands Agents（或Bedrock Agents）能理解的格式。

**技术原理与实现：**
*   **部署层：** 使用`ml-container-creator`将Llama 3.1模型权重和SGLang服务器打包成一个Docker容器，推送到ECR，并部署在SageMaker端点。
*   **协议转换层：** SageMaker端点通常接收JSON输入并返回JSON流。Strands Agents通常期望特定的**工具调用格式**（例如OpenAI Function Calling格式或Bedrock的`toolConfig`）。
*   **实现难点：** SGLang原生可能不直接支持Bedrock的特定JSON Schema。文章可能通过在Prompt中注入特定的JSON结构约束，或者编写一个中间件包装SGLang的响应，使其看起来像Bedrock的响应。

**技术难点与解决方案：**
*   **方案：** 实现**Constrained Decoding（约束解码）**或**Prompt Engineering（提示工程）**。SGLang支持结构化生成，可以利用这一点强制模型输出符合Agent框架要求的JSON Schema。

### 3. 实际应用价值

**指导意义：**
对于正在构建企业级AI应用但受限于公有云API数据隐私政策或高昂Token成本的技术团队，这篇文章提供了一套**“混合云AI架构”**的参考蓝图。

**应用场景：**
1.  **金融/医疗合规场景：** 数据不能出私有VPC，必须使用SageMaker内网端点，但又需要Agent进行业务流程自动化。
2.  **成本敏感型场景：** Llama 3.1 405B或70B在SageMaker上长期运行的Token成本通常低于商业API，适合高频调用。
3.  **特定性能优化：** 利用SGLang的高并发特性，处理大量并发的Agent请求。

**注意问题：**
*   **冷启动时间：** SageMaker端点可能存在冷启动，对于实时性要求极高的Agent交互可能需要配置预置实例。
*   **维护成本：** 自建模型意味着需要监控GPU显存、错误率和版本升级，运维负担比直接调用API高。

**实施建议：**
不要从零开始编写适配器。优先利用AWS提供的`model-provider`接口规范。先在本地测试SGLang的JSON输出能力，确认其能稳定输出符合Schema的JSON后，再打包上云。

### 4. 行业影响分析

**对行业的启示：**
这标志着**“推理即服务”的标准化竞争**正在加剧。虽然模型各异，但上层应用（Agent）需要统一的接口。谁能提供高性能的推理引擎（如SGLang, vLLM, TensorRT-LLM）并适配主流Agent框架，谁就能在基础设施层占据优势。

**可能的变革：**
*   **Agent开发的解耦：** 以后开发Agent，选择“大脑”和选择“身体”将完全分离。你可以用Bedrock的Agent框架，搭配SageMaker上的Llama，甚至本地物理机上的Qwen。
*   **开源模型的商业化加速：** 这种技术方案降低了开源模型进入复杂业务流的门槛，会加速企业从GPT-4等闭源模型向Llama 3.1等开源模型的迁移。

**发展趋势：**
未来云厂商将不再仅仅贩卖模型API，而是贩卖**“模型运行时”**。SGLang等高性能推理后端将成为标配，而“协议适配层”将成为PaaS平台的核心竞争力。

### 5. 延伸思考

**引发的思考：**
既然SGLang可以部署在SageMaker上，那么是否可以部署在EKS或EC2上？这种自定义Provider的思路是否可以延伸到**多模型路由**？即一个Agent背后，根据任务难度，自动路由到SageMaker上的小模型或Bedrock上的大模型？

**拓展方向：**
*   **动态Prompt注入：** 在解析器层根据Agent的上下文动态调整System Prompt，以优化SGLang的输出格式。
*   **流式传输的标准化：** 如何保证SGLang的流式输出能完美映射到Bedrock的流式事件格式，这对于用户体验至关重要。

**未来研究：**
如何量化评估“适配器带来的延迟损耗”？如果解析器逻辑过于复杂，是否会抵消SGLang带来的推理加速优势？

### 7. 案例分析

**成功案例（模拟）：**
某电商公司构建了“智能售后Agent”。直接使用GPT-4o成本过高（每次对话$0.05）。通过本文方案，他们将Llama 3.1 70B部署在SageMaker上，利用SGLang加速。通过自定义解析器，该模型完美对接了Bedrock Agents的OrderLookup和RefundAction工具。结果：成本降低70%，且数据保留在AWS VPC内，符合合规要求。

**失败反思：**
若开发者忽略了SGLang对特定JSON Schema的支持限制，强行要求模型输出极复杂的嵌套JSON，可能导致模型频繁产生幻觉或格式错误，导致Agent循环报错。**教训：** 在部署前必须进行严格的“结构化输出”测试。

### 8. 哲学与逻辑：论证地图

**中心命题：**
在构建企业级Strands Agents时，通过在SageMaker上部署高性能开源模型（如Llama 3.1）并构建自定义解析器，优于直接依赖单一的托管API，因为它实现了**成本效益、数据主权与架构灵活性的最优平衡**。

**支撑理由与依据：**
1.  **成本可控性：** 托管API按Token计费，随规模线性（甚至指数）增长；自部署模型为固定算力成本。
    *   *依据：* AWS定价计算器对比，以及高并发场景下的算力利用率分析。
2.  **数据隐私与合规：** 某些行业数据严禁发送至第三方公有云模型训练端。
    *   *依据：* GDPR及金融行业数据驻留合规要求。
3.  **性能可定制性：** SGLang提供了比通用API更灵活的推理参数调优（如Speculative Decoding）。
    *   *依据：* SGLang技术白皮书中的Benchmark数据。

**反例与边界条件：**
1.  **运维复杂度反例：** 如果团队缺乏MLOps能力，维护SageMaker端点和Docker容器的成本可能超过节省的Token费用。
2.  **性能边界：** 对于需要极低延迟（<200ms）的简单Agent任务，自部署模型的冷启动和网络跳转可能比不上高度优化的公有云区域端点。

**事实与价值判断：**
*   **事实：** SageMaker支持容器化部署；SGLang支持Llama 3.1；Agent框架需要特定的API格式。
*   **价值判断：** “控制权”比“便利性”更有长期价值；“开源模型”已足够胜任大多数Agent任务。

**立场与验证：**
**立场：** 拥抱**“混合编排”**策略。对于核心、敏感、高频的Agent任务使用SageMaker+自定义Provider；对于低频、通用任务保留托管API。

---

## 最佳实践

### 实践 1：优化 SageMaker 端点推理配置

**说明**: 为了确保 Strands Agents 能够获得低延迟的响应，必须针对 LLM 的特性对 SageMaker 推理端点进行精细化的资源配置和参数调优。这包括选择合适的实例类型（如利用 G5 或 P4d 实例进行 GPU 加速）以及调整模型分块和量化设置。

**实施步骤**:
1. 根据模型大小和并发需求，选择配备足够显存的 GPU 实例类型（例如 `ml.g5.2xlarge` 或 `ml.p4d.24xlarge`）。
2. 在 SageMaker 配置中启用动态批处理（Dynamic Batching）或多模型端点（MME）以提高吞吐量。
3. 调整 `Tensor Parallel Degree` 或 `Max Model Length` 参数，以平衡内存占用与生成质量。

**注意事项**: 监控 GPU 利用率和内存使用情况，避免显存溢出（OOM）错误。对于实时性要求极高的 Agent 场景，建议优先考虑低延迟的实例配置。

---

### 实践 2：标准化接口适配与响应格式

**说明**: Strands Agents 依赖于特定的输入输出模式（通常是 OpenAI 兼容格式或 Langchain 标准接口）。自定义模型提供商必须将 SageMaker 端点的原生响应转换为 Agent 框架能够解析的标准结构，特别是处理 `stop_sequences` 和 `token` 流式传输。

**实施步骤**:
1. 创建一个适配器类，继承自 Agent 框架的基础 LLM 类（如 `BaseLLM` 或 `ChatModel`）。
2. 在适配器中实现 `_call` 或 `_generate` 方法，将 Agent 的 Prompt 转换为 SageMaker 接受的 JSON 格式。
3. 编写逻辑将 SageMaker 返回的原始响应解析为包含 `text`、`finish_reason` 和 `usage` 字段的标准消息对象。

**注意事项**: 严格处理流式响应与非流式响应的兼容性。确保错误消息能够被 Agent 捕获并重试，而不是导致整个流程崩溃。

---

### 实践 3：实施严格的输入输出验证

**说明**: 由于 Strands Agents 通常会自动生成工具调用参数，因此必须验证发送给 SageMaker 模型的输入数据，防止因格式错误导致的推理失败，同时验证模型输出是否符合 Agent 期望的 JSON Schema。

**实施步骤**:
1. 在请求发送前，使用 Pydantic 或 JSON Schema 验证 Prompt 模板和参数填充后的完整性。
2. 在模型推理后，对输出内容进行解析，确保其符合预定义的结构（例如 JSON 格式的工具调用）。
3. 实现回退机制，当模型输出格式错误时，尝试重新生成或返回默认安全响应。

**注意事项**: 验证逻辑会增加轻微延迟，应在严格性和性能之间取得平衡。对于复杂的工具调用场景，建议在 Prompt 中加入严格的格式示例。

---

### 实践 4：构建全面的端点健康检查与重试策略

**说明**: 分布式系统（如 SageMaker）可能会遇到冷启动或瞬态网络故障。自定义提供商必须具备弹性能力，能够自动识别端点状态，并在不中断 Agent 任务的前提下处理重试。

**实施步骤**:
1. 实现一个健康检查端点或逻辑，定期调用 SageMaker 的 `InvokeEndpoint` 来检测模型是否处于 `InService` 状态。
2. 集成指数退避算法处理 `ModelError` 或 `ServiceUnavailable` 异常。
3. 配置超时设置，确保 Agent 不会无限期等待响应，而是能够优雅降级或切换到备用模型。

**注意事项**: 区分“模型正在加载”（冷启动）和“模型错误”。对于冷启动，可以适当延长超时时间；对于逻辑错误，应快速失败。

---

### 实践 5：利用 IAM 角色实现最小权限访问

**说明**: 安全性是构建 Agent 系统的关键。必须确保 Strands Agents 调用 SageMaker 端点时使用的 IAM 角色仅拥有执行推理的最小权限，避免潜在的安全风险。

**实施步骤**:
1. 创建专用的 IAM 策略，仅授予 `sagemaker:InvokeEndpoint` 权限，并限定到特定的端点 ARN。
2. 如果 Agent 需要访问其他 AWS 资源（如 S3 存储桶获取上下文），使用基于角色的信任策略而非硬编码凭证。
3. 定期审计 CloudTrail 日志，确保没有异常的调用请求。

**注意事项**: 切勿在代码中硬编码 AWS Access Key 或 Secret Key。始终利用 AWS SDK 的默认凭证链或 IAM 角色进行认证。

---

### 实践 6：建立可观测性与日志追踪机制

**说明**: 为了调试 Agent 的推理链路并优化成本，必须记录每次与 SageMaker 交互的详细元数据，包括延迟、Token 消耗和输入输出内容。

**实施步骤**:
1. 在适配器代码中集成日志记录器

---

## 学习要点

- 通过在 Strands Agents 中集成 SageMaker 托管的 LLM，可以构建自定义模型提供商，从而在安全可控的环境中灵活调用私有化部署的大模型。
- 实现自定义提供商的核心在于编写一个轻量级的 Python 类，该类需继承特定基类并实现调用模型和解析流式响应的标准接口方法。
- 该方案支持将模型推理逻辑无缝嵌入到 Strands 的代理工作流中，使智能体能直接利用企业内部定制训练或微调过的专有模型。
- 利用 SageMaker 的无服务器架构或实时端点，可以有效处理 LLM 的流式响应，确保用户在交互时获得低延迟的实时反馈体验。
- 这种架构设计允许开发者通过修改配置或代码轻松切换底座模型，无需重构上层应用逻辑，从而提升了系统的可维护性。
- 集成过程展示了如何通过标准的 API 网关或直接端点调用，将云原生的 AI 基础设施与业务应用层进行解耦。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints](https://aws.amazon.com/blogs/machine-learning/building-custom-model-provider-for-strands-agents-with-llms-hosted-on-sagemaker-ai-endpoints)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [SageMaker](/tags/sagemaker/) / [SGLang](/tags/sglang/) / [Llama 3.1](/tags/llama-3.1/) / [Strands](/tags/strands/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [自定义解析器](/tags/%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%A3%E6%9E%90%E5%99%A8/) / [AWS](/tags/aws/) / [LLM](/tags/llm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [为 Strands 智能体构建 SageMaker 托管 LLM 自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--9.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260305-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker托管LLM自定义解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--3.md" >}})
- [为Strands智能体构建SageMaker自定义模型解析器]({{< relref "posts/20260306-blogs_podcasts-building-custom-model-provider-for-strands-agents--4.md" >}})
- [为 Strands 智能体构建 SageMaker 托管 LLM 的自定义模型解析器]({{< relref "posts/20260307-blogs_podcasts-building-custom-model-provider-for-strands-agents--10.md" >}})
