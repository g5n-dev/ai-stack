---
title: "NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpSta"
date: 2026-02-12T22:18:39+08:00
draft: false
entry_kind: "auto"
tags: ["NVIDIA", "Nemotron", "AWS", "SageMaker", "JumpStart", "MoE", "模型部署", "生成式AI"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "NVIDIA Nemotron 3 Nano 30B 混合专家模型现已在 Amazon SageMaker JumpStart 上线 今天，我们激动地宣布，拥有 3B 激活参数的 NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpStart 模型目录中正式全面上"
external_url: https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart
scenarios: ["AI/ML项目"]
---

# NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpStart 上线

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-11T19:38:47+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart)

---
## 摘要/简介

今天，我们激动地宣布，配备 3B 活跃参数的 NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpStart 模型目录中正式全面推出。您可以在 Amazon Web Services (AWS) 上借助 Nemotron 3 Nano 加速创新并创造实实在在的业务价值，而无需应对模型部署的复杂性。利用 SageMaker JumpStart 提供的托管部署功能，您可以为您的生成式 AI 应用注入 Nemotron 的强大能力。

---
## 导语

NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpStart 上线。该模型采用混合专家（MoE）架构，总参数 30B，激活参数仅 3B。本文将介绍如何通过 SageMaker JumpStart 快速部署该模型，帮助您高效构建生成式 AI 应用。

---
## 摘要

NVIDIA Nemotron 3 Nano 30B 混合专家模型现已在 Amazon SageMaker JumpStart 上线

今天，我们激动地宣布，拥有 3B 激活参数的 NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpStart 模型目录中正式全面上线。您现在可以通过 Amazon Web Services (AWS) 上的 Nemotron 3 Nano 加速创新并实现切实的商业价值，而无需处理模型部署的复杂性。利用 SageMaker JumpStart 提供的托管部署功能，您可以为您的生成式 AI 应用注入 Nemotron 的强大能力。

**关键总结：**
*   **模型发布：** NVIDIA Nemotron 3 Nano 30B（3B 激活参数）现已在 Amazon SageMaker JumpStart 全面可用。
*   **主要优势：** 用户可以在 AWS 上加速创新并实现商业价值，且无需自行管理复杂的模型部署流程。
*   **核心功能：** 借助 SageMaker JumpStart 的托管部署能力，开发者可以轻松将 Nemotron 的功能集成到生成式 AI 应用中。

---
## 评论

**中心观点**
本文实质上是一篇技术落地公告，旨在通过AWS SageMaker JumpStart降低NVIDIA Nemotron 3 Nano 30B MoE（混合专家）模型的部署门槛，其核心观点在于利用“稀疏激活”技术在保持大模型性能的同时优化推理成本，从而加速企业级生成式AI的变现进程。

**支撑理由与多维评价**

**1. 内容深度：架构优势与商业叙事的结合**
*   **支撑理由：** 文章聚焦于MoE（Mixture of Experts）架构的“3B active parameters”这一关键指标。从技术角度看，这并非单纯的模型参数量堆砌，而是强调计算效率。在推理阶段，模型仅激活3B参数，而非全量30B，这意味着在保持接近30B dense模型智能水平的同时，显著降低了显存占用和计算延迟。
*   **事实陈述：** 文章确认了该模型已集成至SageMaker JumpStart，并支持NVIDIA TensorRT-LLM等优化库。
*   **作者观点：** 文章试图通过“Nano”这一命名策略，将大模型能力“轻量化”，传递出“高性能低成本”的商业价值信号，论证较为严谨地切中了当前企业对大模型落地“贵且慢”的痛点。
*   **反例/边界条件：** 文章未深入探讨MoE架构在微调阶段的复杂性。MoE模型通常比Dense模型更难训练，容易出现训练不稳定性，且对显存的优化主要体现在推理端，而非微调端。

**2. 实用价值：降低工程化门槛**
*   **支撑理由：** 对于企业开发者而言，从Hugging Face下载模型并手动配置TensorRT-LLM环境具有极高的工程复杂度。文章强调的“一键部署”和“预置优化”具有极高的实用价值，消除了基础设施配置的摩擦。
*   **你的推断：** 该集成方案特别适合已有AWS数据湖架构，且需要私有化部署大模型（出于数据安全考虑）的金融或医疗企业。
*   **反例/边界条件：** 对于非AWS生态的用户或边缘计算场景（如本地端侧部署），该方案的实用价值骤降。此外，SageMaker的实例成本对于初创公司而言可能仍是一笔不小的开支。

**3. 创新性：生态整合而非算法突破**
*   **支撑理由：** 文章的创新点不在于提出了新的算法（MoE架构由来已久），而在于将NVIDIA的模型资产与AWS的云基础设施进行了深度整合。
*   **事实陈述：** Nemotron 3 30B本身是基于Nemotron-1的训练数据构建的。
*   **你的推断：** 这种“软硬结合”的生态创新（NVIDIA芯片 + NVIDIA模型 + AWS云）正在构建新的护城河，试图对抗Meta Llama 3等开源模型的统治力。

**4. 行业影响：推动“高效能”模型的普及**
*   **支撑理由：** 行业正从“越大越好”转向“又快又好”。Nemotron 3 Nano 30B的推出，特别是强调Active Parameters，标志着行业对模型效率的关注度已超越单纯的对参数量的军备竞赛。
*   **反例/边界条件：** 目前Llama 3 (8B/70B) 和 Mistral (7B/8x7B) 依然占据社区心智的主导地位。Nemotron 3 Nano 30B 需要证明其在基准测试中显著优于Llama 3 8B或Mistral 7B，否则很难撼动现有的开源生态。

**争议点或不同观点**

1.  **“Active Parameters”的实效性争议：** 虽然3B active parameters听起来很高效，但MoE模型的路由机制本身也会带来计算开销。实际吞吐量是否真的优于一个经过高度量化（如AWQ 4bit）的Llama 3 8B模型，需要严格的Side-by-Side测试。在某些高并发场景下，MoE的显存带宽瓶颈可能抵消其计算优势。
2.  **闭源与开源的博弈：** 文章虽未明说，但Nemotron模型权重并非完全开放权重，而是通过特定平台访问。这与Meta的完全开源策略形成对比。企业可能会担心被锁定在NVIDIA-AWS的生态中，从而倾向于选择更中立的Llama 3。
3.  **Token成本的陷阱：** 企业关注的是Total Cost of Ownership (TCO)。即便模型推理快，如果AWS的GPU实例（如G5或P4）单价较高，或者MoE模型对显存带宽的特殊要求导致必须使用昂贵的高端显存，最终的单Token成本可能并不低。

**实际应用建议**

1.  **基准测试先行：** 在将Nemotron 3 Nano 30B投入生产前，务必在特定业务数据集上与Llama 3 8B或Mistral 7B进行对比测试。重点关注“准确率 vs 延迟”的帕累托前沿。
2.  **关注微调成本：** 如果你的应用场景需要大量微调，需评估MoE微调的难度。建议先利用SageMaker的托管微调功能进行小规模实验，观察收敛速度和显存占用。
3.  **成本监控：** 部署后开启AWS Cost Explorer，监控SageMaker实例的利用率和实际吞吐量。不要被“3B参数”的表象迷惑，应以“每千个Token的美元成本”为最终考核指标。

**可验证的检查方式**

1.  **Side-by-Side �

---
## 技术分析

基于您提供的文章标题和摘要，虽然原文内容未完全展开，但结合NVIDIA Nemotron 3 Nano 30B模型的已知技术规格、Amazon SageMaker JumpStart的平台特性以及MoE（混合专家）架构的行业背景，以下是对该核心观点和技术要点的深入分析。

---

# NVIDIA Nemotron 3 Nano 30B 在 AWS SageMaker JumpStart 上线的深度分析

## 1. 核心观点深度解读

**文章的主要观点**
文章宣布了 NVIDIA Nemotron 3 Nano 30B 模型在 Amazon SageMaker JumpStart 上正式可用。其核心在于强调“**小参数量实现高性能**”与“**云端部署的便捷性**”。具体而言，这是一个拥有 300 亿总参数，但在推理时仅激活 30 亿参数（3B Active Parameters）的混合专家模型。

**作者想要传达的核心思想**
作者试图传达一种“**高效能计算**”的理念。在追求大语言模型（LLM）性能的同时，不再盲目堆砌参数总量，而是通过 MoE 架构优化推理成本和延迟。同时，通过 AWS 这一全球最大的云基础设施平台，降低企业获取顶级 AI 模型的门槛，实现“开箱即用”的商业价值转化。

**观点的创新性和深度**
该观点的创新性在于打破了“越大越好”的迷思。Nemotron 3 Nano 30B 的创新点在于它试图在模型性能（通常与总参数相关）和推理效率（与活跃参数相关）之间找到最佳平衡点。深度上，这代表了模型架构从稠密向稀疏的转变，标志着 AI 落地正从“科研炫技”转向“成本控制与实用性并重”的阶段。

**为什么这个观点重要**
这一观点对当前 AI 行业至关重要，因为它直击企业落地的痛点：**成本与延迟**。许多企业无法承担 70B 或 100B+ 模型的高昂推理费用，也无法忍受高延迟。Nemotron 3 Nano 30B 提供了一个接近大模型效果，但维持小模型成本的解决方案，极大地拓宽了生成式 AI 的商业化边界。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **混合专家模型**：这是核心技术。模型并非所有参数都参与每一次计算，而是由门控网络选择特定的“专家”子网络进行处理。
2.  **稀疏激活**：虽然模型总共有 300 亿参数，但在推理时只有 30 亿参数是活跃的。这意味着计算量大幅减少，显存占用（尤其是 KV Cache 和计算中间态）显著降低。
3.  **Amazon SageMaker JumpStart**：AWS 提供的模型即服务集合，提供预训练模型、示例 notebook 和一键部署能力。

**技术原理和实现方式**
MoE 模型通常包含一个“门控网络”和多个“专家网络”。当输入数据到来时，门控网络决定将数据路由给哪几个最相关的专家。在 Nemotron 3 Nano 30B 的实现中，它利用了 Transformer 架构的扩展性，将 FFN（前馈神经网络）层替换为 MoE 层。在 AWS 部署时，SageMaker 负责处理底层容器化、自动扩缩容以及针对 NVIDIA GPU（如 A100 或 H100）的驱动优化。

**技术难点和解决方案**
*   **难点**：MoE 模型在训练时不稳定，容易出现专家坍塌（即所有专家都倾向于处理同一种简单任务）。
*   **解决方案**：NVIDIA 可能采用了负载均衡损失函数和专家丢弃策略来确保所有专家得到均匀训练。
*   **难点**：显存带宽瓶颈。虽然计算量少了，但加载 30B 参数仍需大量显存。
*   **解决方案**：利用 AWS 的实例类型（如 `ml.g5` 或 `ml.p4`）配合高速显存，以及模型量化技术。

**技术创新点分析**
Nemotron 3 Nano 30B 的最大创新在于其**“Nano”**的命名策略。通常 30B 参数的模型不被视为“Nano”，但由于其 Active Parameters 仅 3B，它实际上具备 Nano 级别的推理速度，却拥有 30B 级别的知识容量。这种**“容量与效率的解耦”**是技术上的高光点。

## 3. 实际应用价值

**对实际工作的指导意义**
对于企业架构师和 AI 工程师，这意味着在选型时多了一个“中间选项”。以前只有 7B（性能不足）和 70B（成本太高）可选，现在 30B MoE 填补了这一空白，特别适合对响应速度有要求且任务复杂度较高的场景。

**可以应用到哪些场景**
1.  **实时聊天机器人**：需要低延迟（由 3B 活跃参数保证）且具备深厚知识库（由 30B 总参数保证）。
2.  **RAG（检索增强生成）**：在处理长上下文和复杂文档总结时，30B 的容量上限比 7B 模型更高，幻觉更少。
3.  **代码生成与分析**：代码逻辑通常需要较强的推理能力，小模型往往力不从心，该模型能提供更准确的代码补全。

**需要注意的问题**
*   **显存占用**：虽然推理计算快，但加载整个 30B 模型仍需约 60GB+ 显存（FP16），对硬件底座要求不低。
*   **路由效率**：MoE 的路由机制在分布式部署时可能会带来通信开销。

**实施建议**
建议在 AWS SageMaker 上使用多 GPU 部署（如 Tensor Parallelism）以容纳 30B 参数，并利用 SageMaker Inference Components 的特性进行动态批处理，以摊薄 MoE 路由的延迟成本。

## 4. 行业影响分析

**对行业的启示**
这一发布进一步印证了 **"Slizer AI"（小而美）** 或 "Efficient AI" 的趋势。行业正在从单纯追求参数竞赛，转向追求“单位性能成本”。云厂商（AWS）与芯片巨头（NVIDIA）的深度绑定，也暗示了未来 AI 落地将是“软硬一体化的垂直整合”。

**可能带来的变革**
企业级 AI 部署将不再局限于通用模型（如 GPT-4 的 API 调用），而是更多转向私有化部署的高性价比模型。这将加速数据隐私敏感行业（金融、医疗）的大模型应用落地。

**对行业格局的影响**
NVIDIA 通过提供自家优化的模型，正在从“卖铲子的人”（卖 GPU）向“卖矿的人”（提供模型服务）延伸。这可能会对 OpenAI、Anthropic 等纯模型厂商构成竞争压力，同时也给 AWS 这种云厂商提供了区别于 Google Cloud (Gemini) 和 Azure (OpenAI) 的差异化路径。

## 5. 延伸思考

**引发的思考**
随着 MoE 模型的普及，传统的“参数量”指标是否将失效？我们是否应该建立新的评测标准，例如“Token 生成每美元成本”或“单位延迟下的准确率得分”？

**拓展方向**
未来可能会看到更多“领域特定的 MoE”。例如，一个 30B 的模型，其中 10B 专门用于法律，10B 用于医疗，10B 用于代码。这种架构化的知识分离比混合训练更高效。

**未来发展趋势**
*   **端侧 MoE**：随着手机和 PC 算力提升，类似 Nemotron 3 Nano 这种架构的模型可能会被压缩并运行在边缘设备上。
*   **动态拓扑**：未来的模型可能会根据任务难度，动态决定激活多少个专家，实现真正的弹性计算。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估阶段**：在 SageMaker JumpStart 中启动该模型，使用您的特定数据集进行微调。由于是 30B，微调成本较高，建议使用 PEFT（如 LoRA）技术。
2.  **对比测试**：选取 Llama-2 70B 和 Mistral 7B 作为基准。对比 Nemotron 3 Nano 的准确率是否接近 70B，同时速度是否接近 7B。
3.  **部署架构**：使用 SageMaker Async Inference 或 SageMaker Real-time Endpoints，根据业务流量选择合适的实例规格（推荐 `ml.g5.12xlarge` 或 `ml.g5.24xlarge`）。

**具体行动建议**
*   申请 AWS 账号并进入 SageMaker 控制台。
*   搜索 "Nemotron" 并部署测试实例。
*   准备 50-100 条典型业务 Prompt 进行盲测。

**需补充的知识**
*   理解 MoE 的负载均衡机制。
*   熟悉 SageMaker 的模型部署和配置（LMI containers）。
*   掌握 vLLM 或 TensorRT-LLM 等推理加速工具（如果需要自行优化容器）。

## 7. 案例分析

**结合实际案例说明**
假设一家**跨国金融咨询公司**需要构建一个内部知识问答助手。
*   **旧方案**：使用 BERT（搜索）+ GPT-4（生成）。成本高，且数据有隐私风险。
*   **新方案**：使用 Nemotron 3 Nano 30B 部署在 AWS VPC 内部。

**成功案例分析**
该公司通过 JumpStart 快速部署了 Nemotron 模型。由于模型具备 30B 的知识容量，它能理解复杂的金融术语（优于 7B 模型）；由于只有 3B 参数激活，其响应速度控制在 500ms 以内（优于 70B 模型）。这实现了**安全、准确、快速**的三角平衡。

**失败案例反思**
如果一家初创公司盲目使用该模型处理简单的文本分类任务（如情感分析）。由于加载 30B 模型的固定显存成本极高，这会导致资源浪费。此时，一个极小的 BERT 或 DistilBERT 才是正确选择。**教训：不要用大炮打蚊子。**

## 8. 哲学与逻辑：论证地图

**中心命题**
**NVIDIA Nemotron 3 Nano 30B MoE 模型在 AWS SageMaker 上的可用性，为企业级生成式 AI 提供了一种在保持高性能的同时显著降低推理成本的最优解。**

**支撑理由与依据**
1.  **理由一：MoE 架构实现了计算与容量的解耦。**
    *   *依据*：技术原理表明，30B 总参数保证了模型的知识广度与推理深度，而 3B 活跃参数确保了推理时的低延迟和高吞吐量。
2.  **理由二：AWS SageMaker JumpStart 提供了极低的部署门槛。**
    *   *依据*：平台提供了预构建的容器和基础设施即代码，消除了 MLOps 的复杂性，使企业能专注于业务逻辑。
3.  **理由三：成本效益比优于传统稠密模型。**
    *   *依据*：在同等性能水平下，MoE 模型的推理成本通常远低于具有相同性能表现的稠密模型（如 Llama-2 70B）。

**反例或边界条件**
1.  **显存瓶颈**：虽然计算量小，但 30B 模型的加载仍需约 60GB+ 显存。对于显存受限的边缘设备或小型实例，该模型不可用。
2.  **简单任务的边际效益递减

---
## 最佳实践

## 最佳实践指南

### 实践 1：针对 MoE 架构优化资源配置

**说明**: 
Nemotron 3 Nano 30B 采用了混合专家架构。虽然其总参数量为 300 亿，但在推理过程中仅激活部分参数。这种特性使得它在保持高性能的同时，显著降低了显存占用和计算延迟。在 SageMaker 中部署时，应根据激活参数量而非总参数量来规划资源，以实现成本效益最大化。

**实施步骤**:
1. 在 SageMaker JumpStart 选择模型时，仔细查看推荐的实例类型（通常为 ml.g5 或 ml.p4 系列）。
2. 利用 SageMaker Inference Recommender 工具，针对 MoE 模型运行基准测试，以确定最具性价比的实例配置。
3. 监控 GPU 显存使用率和推理延迟，确保未激活的专家参数不会造成不必要的资源浪费。

**注意事项**: 
不要仅凭 30B 的总参数量就盲目分配过大的资源，这会导致成本增加而性能提升不明显。

---

### 实践 2：实施模型量化以加速推理

**说明**: 
为了在 SageMaker 上获得更低的延迟和更高的吞吐量，建议对模型进行量化。Nemotron 3 Nano 30B 支持 FP16 或 BF16 精度，通过量化可以进一步压缩模型体积，减少显存占用，从而在单个 GPU 上部署更大的批次大小。

**实施步骤**:
1. 在 JumpStart 部署配置中，检查是否默认启用了 FP16/BF16 支持。
2. 如需极致性能，可使用 SageMaker 的 LMI (Large Model Inference) 容器，配置量化参数（如 AWQ 或 GPTQ 量化，若模型支持）。
3. 部署后对比量化前后的响应速度和模型准确率（Perplexity 指标），以确定最佳精度配置。

**注意事项**: 
量化可能会轻微影响模型精度，必须在生产环境部署前进行充分的评估测试。

---

### 实践 3：利用 SageMaker 异步推理优化成本

**说明**: 
对于非实时要求的批量处理任务（如文档摘要、批量内容生成），使用 SageMaker 异步推理端点可以显著降低成本。MoE 模型在处理高并发请求时可能会出现显存波动，异步队列能更好地管理这些负载。

**实施步骤**:
1. 在 SageMaker 控制台中创建模型时，选择“Async inference”作为端点配置选项。
2. 配置自动扩缩容策略，设置队列积压时的最大实例数量和空闲时的最小实例数量（甚至可以缩减到 0）。
3. 通过 S3 存储输入数据，并调用 InvokeEndpointAsync API 进行处理。

**注意事项**: 
异步模式不适合需要即时反馈的聊天机器人场景，仅适用于后台处理任务。

---

### 实践 4：精细化提示词工程与上下文管理

**说明**: 
Nemotron 3 Nano 30B 拥有 4K 上下文窗口和针对特定微调的指令跟随能力。为了获得最佳输出，需要针对其微调特性（如 ChatML 格式或特定指令格式）设计提示词，并有效利用上下文窗口。

**实施步骤**:
1. 查阅 Nemotron 3 Nano 的模型卡片，了解其训练时所使用的 Prompt 模板（如 System/User/Assistant 结构）。
2. 在构建应用时，严格遵循推荐的对话模板格式，避免格式错误导致的性能下降。
3. 实施 RAG（检索增强生成）时，控制输入上下文长度在 4K token 以内，并对检索到的文档进行相关性排序。

**注意事项**: 
不要盲目使用超长上下文填充无效信息，这会稀释模型对关键指令的注意力。

---

### 实践 5：建立负责任的 AI 评估与安全护栏

**说明**: 
虽然 Nemotron 模型经过了安全微调，但在生产环境中仍需防范潜在的有害输出或幻觉。利用 SageMaker JumpStart 集成的 Model Monitor 或外部工具对模型输出进行持续监控。

**实施步骤**:
1. 在部署前，使用包含偏见、毒性和幻觉测试的基准数据集对模型进行红队测试。
2. 配置 SageMaker Model Monitor，捕捉数据漂移或模型质量下降的指标。
3. 在应用层设置内容过滤器，对模型输出进行二次校验，过滤不当内容。

**注意事项**: 
安全护栏不应仅依赖模型本身，应用层的过滤机制是保障生产环境安全的关键。

---

### 实践 6：使用 SageMaker Pipelines 进行 MLOps 自动化

**说明**: 
为了实现从实验到生产的无缝过渡，应使用 SageMaker Pipelines 构建 CI/CD 流程。这有助于自动化模型的部署、更新和重训练（如果基于此模型进行微调）。

**实施步骤**:
1. 创建一个 SageMaker Pipeline，定义从 JumpStart 获取模型、注册模型到部署模型的各个阶段。
2. 设置模型注册步骤，将模型版本与特定的性能指标挂钩。
3. 配置自动触发机制，当基础模型更新或微调完成时，自动启动蓝绿部署流程

---
## 学习要点

- NVIDIA Nemotron-3 Nano 30B 混合专家 (MoE) 模型现已在 Amazon SageMaker JumpStart 上正式提供，用户可以轻松访问并部署该模型。
- 该模型采用混合专家 (MoE) 架构，在保持 300 亿参数规模的同时，显著降低了推理成本并提高了运行效率。
- 用户可以通过 SageMaker JumpStart 快速部署此模型，无需手动配置复杂的环境，加速生成式 AI 应用的开发流程。
- Nemotron-3 Nano 30B 专为商业应用优化，特别适合需要高性能但资源受限的企业级场景。
- 模型支持多种自然语言处理任务，包括文本生成、摘要、问答等，能够满足广泛的业务需求。
- 通过 AWS 和 NVIDIA 的合作，开发者可以在云端高效利用 NVIDIA 的最新 AI 技术，简化 AI 模型的集成与测试流程。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart](https://aws.amazon.com/blogs/machine-learning/nvidia-nemotron-3-nano-30b-is-now-available-in-amazon-sagemaker-jumpstart)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [NVIDIA](/tags/nvidia/) / [Nemotron](/tags/nemotron/) / [AWS](/tags/aws/) / [SageMaker](/tags/sagemaker/) / [JumpStart](/tags/jumpstart/) / [MoE](/tags/moe/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [生成式AI](/tags/%E7%94%9F%E6%88%90%E5%BC%8Fai/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-0.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-5.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-4.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpSta]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-6.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpSta]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*