---
title: "在 SageMaker AI 与 Bedrock 上使用 vLLM 高效服务多 LoRA 模型"
date: 2026-02-26T02:52:57+08:00
draft: false
entry_kind: "auto"
tags: ["vLLM", "LoRA", "SageMaker", "Bedrock", "MoE", "模型推理", "内核优化", "GPT-OSS"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "以下是对该内容的中文总结： 本文主要介绍了如何在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 高效托管数十个微调模型。文章详细阐述了团队如何为 Mixture of Experts (MoE) 模型在 vLLM 中实现多 LoRA 推理，并介绍了内核层面的优化工作。此外，"
external_url: https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock
scenarios: ["大语言模型"]
---

# 在 SageMaker AI 与 Bedrock 上使用 vLLM 高效服务多 LoRA 模型

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T20:56:13+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock)

---
## 摘要/简介

在这篇文章中，我们将解释如何在 vLLM 中为混合专家（MoE）模型实现多 LoRA 推理，介绍我们所做的内核级优化，并展示您如何从这项工作中受益。本文我们将全程以 GPT-OSS 20B 为主要示例。

---
## 导语

随着大模型应用场景的细化，如何高效管理并服务数十个微调模型已成为工程落地的关键挑战。本文将深入探讨如何利用 vLLM 在 Amazon SageMaker AI 和 Amazon Bedrock 上实现多 LoRA 推理，并分享针对混合专家（MoE）模型的内核级优化实践。通过以 GPT-OSS 20B 为例的完整演示，您将掌握在保障性能的前提下，显著降低推理资源消耗与部署成本的具体方法。

---
## 摘要

以下是对该内容的中文总结：

本文主要介绍了如何在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 高效托管数十个微调模型。文章详细阐述了团队如何为 Mixture of Experts (MoE) 模型在 vLLM 中实现多 LoRA 推理，并介绍了内核层面的优化工作。此外，文中还展示了如何利用这些技术成果，并以 GPT-OSS 20B 模型为例进行了全程演示。

---
## 评论

**中心观点**
这篇文章揭示了在大模型规模化落地阶段，通过**内核级优化与多LoRA服务架构**，可以在不牺牲推理延迟的前提下，将单一实例服务定制化模型的边际成本降至接近零，这是从“单体大模型”向“分布式模型供给”转型的关键工程实践。

**支撑理由与深度评价**

**1. 技术深度：从暴力堆砌到精细化的内核调度**
*   **支撑理由：** 文章的核心价值在于超越了简单的“服务编排”，深入到了**CUDA内核层面**。针对GPT-OSS 20B这类大模型，推理瓶颈往往不在显存容量，而在计算单元的利用率和内存带宽。vLLM通过PagedAttention和针对多LoRA的定制化内核，解决了在Batching过程中不同LoRA权重动态切换带来的显存碎片和指令跳转开销。
*   **事实陈述：** 文章提到了在Amazon SageMaker和Bedrock上的实现，这表明AWS正在将高性能开源推理框架（vLLM）深度集成进其全托管服务中，以弥补通用框架在特定MoE场景下的性能短板。
*   **你的推断：** 这种优化意味着企业不再需要为每个微调模型（如针对不同法律领域的助手）单独部署一个GPU实例。这是一种**“时间换空间，算法优化换硬件资源”**的典型路径，直接将LoRA从一种“训练技巧”升维为一种“生产部署架构”。

**2. 实用价值：重塑SaaS应用的边际成本结构**
*   **支撑理由：** 对于B2B SaaS服务商而言，该架构极具杀伤力。以往为100个客户部署100个私有模型需要100个实例，成本不可控。通过Multi-LoRA Serving，可能仅需10-20个实例即可承载。
*   **作者观点：** 文章强调在Bedrock上的应用，实际上是在推销一种“Serverless推理”的未来图景——开发者只需关注LoRA ID，无需关心底层GPU的调度。这大大降低了AI原生应用的开发门槛。

**3. 创新性与行业影响：MoE架构的软性落地**
*   **支撑理由：** 虽然Mixture of Experts (MoE)通常指模型内部的激活路由，但这里将Multi-LoRA视为一种MoE的变体（专家即LoRA适配器），这是一种架构上的创新。它证明了不需要重新训练庞大的基础模型，通过动态挂载轻量级适配器也能实现类似的“专家”效果。
*   **行业影响：** 这可能会终结“一亿个聊天机器人App”这种低效形态，转而催生“一个通用内核 + 亿级LoRA插件”的云服务模式。

**反例与边界条件**

尽管文章描绘了美好的前景，但在实际工程中存在显著的边界条件：

1.  **显存与延迟的权衡：**
    *   **边界条件：** 虽然LoRA参数量小，但当并发服务的LoRA数量达到数千甚至上万时，**显存带宽**将成为绝对瓶颈。频繁地从CPU内存向GPU显存搬运LoRA权重会引入不可预测的延迟尖刺。
    *   **反例：** 在对延迟极度敏感（如<100ms）的实时语音交互场景中，这种动态加载机制可能导致超时，此时独立的模型实例反而更稳定。

2.  **模型规模的适用性：**
    *   **边界条件：** 文章以20B参数模型为例。对于70B以上的超大模型，GPU显存几乎被基础模型权重占满，留给LoRA Batch的空间极其有限。
    *   **反例：** 在双卡A100（80GB）运行Llama-3-70B时，显存已接近饱和，多LoRA并发的收益会急剧下降，甚至因为调度开销导致性能劣化。

3.  **基础模型的灾难性遗忘与冲突：**
    *   **边界条件：** Multi-LoRA Serving假设所有LoRA可以共享同一个基础模型。但如果LoRA A将模型微调为“律师风格”，而LoRA B将其微调为“说唱歌手风格”，这种风格差异可能会在底层KV Cache中产生干扰，导致推理输出出现非预期的混合或退化。

**可验证的检查方式**

为了验证文章中技术的实际效果，建议进行以下实验：

1.  **并发压力测试：**
    *   **指标：** 在单张GPU上，逐步增加同时服务的LoRA数量（从1个到100个），观察P95延迟和Token生成吞吐量（TPS）。
    *   **预期：** 优秀的实现应显示吞吐量随LoRA数量线性增长，直到显存带宽饱和。

2.  **权重搬运开销监控：**
    *   **工具：** 使用Nsight Systems或PyTorch Profiler。
    *   **观察窗口：** 监测`cudaMemcpy`（H2D）的时间占比。如果LoRA切换的时间占比超过推理时间的10%，则说明内核优化不足。

3.  **准确性回归测试：**
    *   **实验：** 选取5个不同领域的LoRA（如医疗、金融、代码、写作、翻译），在高并发混合请求下，对比“多LoRA服务”与“单LoRA独立部署”的输出结果。
    *   **目的：** 验证是否存在“交叉干扰”导致输出质量下降。

**总结**

这篇文章在技术层面具有很高的深度，它准确地指出了当前AI推理成本高昂的痛点，并给出了基于vLLM和云原生架构的可行解法。然而，读者应当保持批判性思维：**“Efficiently”是

---
## 技术分析

# 深度分析：在 Amazon SageMaker AI 和 Amazon Bedrock 上使用 vLLM 高效服务多 LoRA 模型

## 1. 核心观点深度解读

**文章的主要观点**
这篇文章的核心观点在于展示如何通过 **vLLM** 框架实现 **多 LoRA（Low-Rank Adaptation）推理**，特别是针对 **混合专家模型**，从而在单一的基础模型实例上同时高效地服务数十个微调过的模型。作者以 GPT-OSS 20B 模型为例，证明了在 Amazon SageMaker AI 和 Amazon Bedrock 基础设施上，这种方法的可行性与高效性。

**作者想要传达的核心思想**
作者传达的核心思想是 **"共享即高效"**。传统的模型部署方式是为每个微调模型（如针对特定行业、特定客户微调的版本）部署独立的全量模型实例，这带来了巨大的显存和计算资源浪费。通过在底层共享基础模型参数，仅在推理时动态注入轻量级的 LoRA 适配器权重，可以实现资源利用率数量级的提升。这不仅降低了成本，还极大地简化了运维复杂度。

**观点的创新性和深度**
这一观点的创新性体现在将 **MoE（混合专家）的架构思想** 应用到了 **模型服务部署层面**。在模型内部，MoE 通过激活不同的神经元来处理不同任务；而在服务层面，这篇文章展示的是通过激活不同的 LoRA 适配器来服务不同的租户或任务。
其深度在于不仅仅停留在应用层的 API 调用，而是深入到了 **内核级优化**。文章详细讨论了如何通过融合 CUDA 内核来解决多 LoRA 并发服务时的显存碎片和计算瓶颈问题，这是从理论走向工程落地的关键一步。

**为什么这个观点重要**
这个观点的重要性在于它解决了生成式 AI 商业化落地的 **"最后一公里"** 成本问题。在 B2B 场景中，客户往往需要基于基础大模型进行私有化微调。如果不能低成本地同时服务这些定制模型，SaaS 服务商将面临难以承受的 GPU 资源开销。多 LoRA 服务技术使得 "千人千面" 的 AI 服务在商业上变得可持续。

## 2. 关键技术要点

**涉及的关键技术或概念**
- **vLLM**: 一个高性能的大语言模型推理服务框架，核心特性是 PagedAttention。
- **LoRA (Low-Rank Adaptation)**: 一种参数高效微调技术（PEFT），通过冻结预训练模型权重并在层间注入低秩矩阵来适应新任务。
- **MoE (Mixture of Experts)**: 本文特指模型架构层面的稀疏化，但在部署语境下，也隐喻了多 LoRA 的动态路由。
- **Dynamic Batching & PagedAttention**: vLLM 的核心技术，用于管理 KV Cache。
- **Cuda Kernel Fusion**: GPU 编程优化技术。

**技术原理和实现方式**
1.  **权重共享与隔离**: 系统在显存中只加载一份基础模型权重。当请求到达时，系统根据请求中的 LoRA ID，动态加载对应的 LoRA 适配器（A和B矩阵）到显存中。
2.  **计算融合**: 在进行矩阵乘法时，将基础模型的权重与动态加载的 LoRA 权重进行融合计算。数学公式通常为：$h = W_0 x + \Delta W x = W_0 x + BAx$。vLLM 的优化在于直接在 GPU 内核层面高效执行 $W_0x + (BA)x$，避免多次 HBM（高带宽内存）读写。
3.  **调度器优化**: vLLM 的调度器被扩展以识别和处理带有 LoRA 标识的请求，确保属于同一 LoRA 的请求或混合 LoRA 的请求能够被高效地打包进同一个 Batch 中。

**技术难点和解决方案**
- **难点 1: 显存管理的碎片化**。
  - *解决方案*: 利用 vLLM 的 PagedAttention 机制来管理 KV Cache，同时将 LoRA 权重也视为可分页的资源进行管理，确保在多 LoRA 并发切换时显存利用率最大化。
- **难点 2: 计算吞吐量下降**。
  - *解决方案*: 进行 **CUDA Kernel 优化**。文章提到实现了定制的融合内核，将 LoRA 的增量计算与基础模型的前向传播合并，减少 Kernel 启动开销和内存访问延迟。
- **难点 3: 批处理效率**。
  - *解决方案*: 动态批处理策略。允许一个 Batch 内包含不同 LoRA ID 的请求，从而最大化 GPU 的并行计算能力（SIMD）。

**技术创新点分析**
最大的技术创新在于 **将 MoE 模型的推理能力集成到 vLLM 的多 LoRA 服务框架中**。MoE 模型本身结构复杂，通常包含庞大的专家层，在其之上再叠加多 LoRA 服务，对显存带宽和计算调度的要求极高。作者展示了如何在支持 GPT-OSS 20B 这种大参数量模型的同时，依然保持低延迟。

## 3. 实际应用价值

**对实际工作的指导意义**
对于 AI 平台工程师和 MLOps 团队来说，这篇文章提供了一套标准化的 **"多租户大模型服务"** 架构蓝图。它证明了不需要为每个微调模型准备专用的 A100/H100 节点，而是可以通过 "1 个基础模型 + N 个 LoRA 适配器" 的模式提供服务。

**可以应用到哪些场景**
1.  **SaaS 多租户平台**: 一个通用的法律大模型底座，为不同律所部署各自的私有数据微调版本（LoRA），物理上共享资源，逻辑上完全隔离。
2.  **多语言/多任务服务**: 同时服务针对英语、中文、西班牙语优化的模型版本，或者同时服务代码生成、文本摘要、对话等不同任务微调的模型。
3.  **A/B 测试与快速迭代**: 在生产环境中同时加载多个不同超参数或不同数据集微调的 LoRA 版本，实时对比效果。

**需要注意的问题**
- **LoRA 之间的相互干扰**: 虽然权重是隔离的，但共享的计算资源可能导致某个高负载的 LoRA 请求挤占其他请求的带宽。
- **显存容量限制**: 即使 LoRA 很小，几十上百个 LoRA 的 KV Cache 依然会占用大量显存。需要精确规划最大并发数。

**实施建议**
建议从显存占用评估入手。计算单个 LoRA 权重大小 + 单个请求的最大 KV Cache 大小，结合 GPU 显存总量，推算出单卡能支持的最大并发 LoRA 数量和总吞吐量。优先在 vLLM 环境下进行压测。

## 4. 行业影响分析

**对行业的启示**
这一技术趋势标志着大模型服务从 **"单体应用"** 向 **"微服务化"** 的演进。正如 Docker 改变了应用交付，LoRA 改变了模型交付。它启示行业：未来的 AI 基础设施不仅要关注训练速度，更要关注 **推理的边际成本**。

**可能带来的变革**
这可能会彻底改变 AI 模型的售卖模式。云厂商可能不再主要售卖 "模型 API 调用次数"，而是售卖 "模型实例 + 挂载 LoRA 插件的数量/时长"。这将催生 **LoRA Store（模型插件商店）** 的兴起，类似于手机应用商店。

**相关领域的发展趋势**
- **推理框架的军备竞赛**: vLLM、TGI (Text Generation Inference)、TensorRT-LLM 等框架将在多 LoRA 支持上展开激烈竞争。
- **专用硬件的发展**: GPU 厂商可能会针对这种 "大权重静态 + 小权重动态" 的访存模式优化显存架构（例如更大的 L2 Cache）。

## 5. 延伸思考

**引发的其他思考**
- **安全性**: 多个租户的 LoRA 权重在同一个物理显存中，虽然逻辑隔离，但是否存在通过侧信道攻击恢复其他租户模型能力的风险？
- **冷启动问题**: 当 LoRA 数量达到数千个时，如何管理从 CPU 内存到 GPU 显存的换入换出？是否需要引入 Redis 等外部缓存层？

**可以拓展的方向**
- **LoRA 路由策略**: 目前 LoRA 是通过请求 ID 指定的。未来是否可以开发一个 "路由模型"，自动根据用户 Query 的内容，决定应该调用哪一个 LoRA（或者混合调用多个 LoRA）？
- **量化感知的多 LoRA**: 结合 4-bit 量化（如 GPTQ, AWQ）与多 LoRA 服务，进一步压缩显存占用。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估模型适配性**: 确认你使用的基础模型（如 Llama 3, Mistral 等）在 vLLM 中是否已支持 Multi-LoRA 功能。
2.  **环境搭建**: 在 AWS SageMaker 上使用 vLLM 的预构建 Docker 镜像，配置好多 LoRA 服务器的启动参数，特别是 `--max-loras` 和 `--max-lora-rank`。
3.  **模型转换**: 将训练好的 LoRA 权重转换为 vLLM 兼容的格式。

**具体的行动建议**
- **Step 1**: 在开发环境使用 vLLM 的 OpenAI 兼容 API 启动一个本地服务，挂载 2-3 个不同的 LoRA 权重进行测试。
- **Step 2**: 使用 `Locust` 或 similar 工具进行并发压测，观察显存占用和 Token 生成延迟（TTFT, TPOT）。
- **Step 3**: 逐步增加 LoRA 数量，寻找性能拐点。

**需要补充的知识**
- 深入理解 **CUDA 编程基础**，有助于理解 Kernel Fusion 带来的性能提升。
- 熟悉 **OpenAI API 协议**，因为 vLLM 兼容该协议，理解 `Authorization` 头部如何传递 LoRA ID 等自定义信息至关重要。

## 7. 案例分析

**结合实际案例说明**
假设一家跨国企业构建了一个基于 Llama 3 70B 的内部知识问答助手。
- **过去**: 针对市场部、HR、研发部分别微调了 3 个全量模型。需要部署 3 个实例，每个需要 4 张 A100 (80GB)，共需 12 张卡。
- **现在**: 使用 vLLM Multi-LoRA。
  - 部署 1 个 Llama 3 70B 基座模型（4 张 A100）。
  - 挂载 3 个 LoRA 适配器（每个仅几十 MB）。
  - 资源节省了 66% 的 GPU 卡数，且运维只需管理一个服务端点。

**成功案例分析**
文章中提到的 GPT-OSS 20B 例子。通过 Kernel 优化，使得在处理多 LoRA 请求时，计算开销接近于处理单一模型。这意味着企业可以用极低的成本为成百上千个垂直领域的小 B 客户提供定制化模型服务。

**失败案例反思**
如果 LoRA 的 Rank 设置得过大（例如 Rank > 128），或者 LoRA 数量过多导致显存不足以容纳所有活跃请求的 KV Cache，可能会导致 OOM（显存溢出）或者频繁的 Swap，导致性能反而不如部署独立小模型。因此，**控制 LoRA Rank 和

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用多 LoRA 适配器服务实现高效模型复用

**说明**:
vLLM 支持在单个基础模型实例上动态加载和切换多个 LoRA（低秩适配器）适配器。这避免了为每一个微调模型部署独立的端点，从而显著降低基础设施成本和运维开销。通过共享基础模型的计算资源（KV Cache 和 GPU 显存），可以在同一硬件上并发服务数十个特定的任务模型。

**实施步骤**:
1. 准备一个经过预训练的基础模型（如 Llama 3 或 Mistral）。
2. 训练特定于任务的 LoRA 适配器，并将其存储在 S3 存储桶中。
3. 在 SageMaker 或 Bedrock 部署配置中，启用 `enable_lora` 参数，并配置 `max_loras`（最大并发适配器数）和 `max_lora_rank`（最大秩）。
4. 在推理请求中指定 `lora_name`，vLLM 将自动加载相应的适配器进行处理。

**注意事项**:
需要根据 GPU 显存大小仔细调整 `max_loras` 和 `max_cpu_loras` 参数，以平衡并发性能和内存溢出（OOM）的风险。

---

### 实践 2：采用 PagedAttention 算法优化显存管理

**说明**:
vLLM 的核心优势在于其 PagedAttention 机制，它借鉴了操作系统中分页内存管理的思想。该机制将 KV Cache 分块存储，并在显存不足时将其换出到 CPU 内存，从而解决了传统推理框架中显存碎片化导致的浪费问题。这对于服务大批量并发请求至关重要。

**实施步骤**:
1. 在部署容器配置中，确保使用 vLLM 原生引擎。
2. 调整 `gpu_memory_utilization` 参数（通常设置为 0.9 或更高），以允许 vLLM 尽可能多地利用 GPU 显存来存储 KV Cache。
3. 监控显存使用情况，根据模型大小和输入长度调整 `block_size`（默认通常为 16）。

**注意事项**:
过高的 `gpu_memory_utilization` 可能会导致 CUDA OOM，建议在生产环境中预留少量显存缓冲（例如 0.05 - 0.1）以处理动态峰值。

---

### 实践 3：实施连续批处理以提升吞吐量

**说明**:
与静态批处理不同，连续批处理允许在一个批次中的某些请求处理完成后，立即插入新的请求，而无需等待整个批次中的所有请求完成。vLLM 原生支持连续批处理，这能极大提高 GPU 的利用率并降低 Token 生成延迟。

**实施步骤**:
1. 在 vLLM 配置中，确保未禁用连续批处理功能（默认开启）。
2. 根据工作负载特性调整调度器参数，例如 `max_num_batched_tokens`，以控制单次迭代的 Token 总数上限。
3. 结合自动扩缩容策略，根据队列长度动态调整实例数量。

**注意事项**:
对于延迟极度敏感的应用，需适当控制批次大小，以免长请求阻塞短请求（即队头阻塞问题），尽管 vLLM 的迭代级调度已缓解了此问题。

---

### 实践 4：利用 SageMaker Multi-Model Endpoints (MME) 或 Bedrock 自定义模型导入

**说明**:
为了高效管理“数十个”模型，应利用平台级的管理能力。在 SageMaker 上，可以使用 Multi-Model Endpoints 功能在单一实例上托管多个模型模型；在 Bedrock 上，可以通过自定义模型导入功能将微调后的模型注册为可调用资源。

**实施步骤**:
1. 将所有微调后的模型工件（LoRA 权重或完整模型）整理并上传至 S3，保持目录结构清晰。
2. 在 SageMaker 中创建 MME 端点，配置 vLLM 作为推理容器，并指向 S3 前缀。
3. 在 Bedrock 中，使用 Import Model 功能将模型注册到您的私有目录中。
4. 配置调用逻辑，根据业务路由逻辑动态调用对应的模型。

**注意事项**:
如果使用完整模型而非 LoRA，首次加载模型时可能会有冷启动延迟，建议配置预加载策略或保持实例预热以应对突发流量。

---

### 实践 5：配置张量并行以支持大模型部署

**说明**:
当单个 GPU 的显存不足以容纳基础模型或需要处理超长上下文时，vLLM 支持张量并行。它将模型权重切分到多个 GPU 上进行并行计算，从而允许在 SageMaker 的多 GPU 实例（如 `ml.g5.12xlarge` 或 `ml.p4d.24xlarge`）上部署大参数模型。

**实施步骤**:
1. 选择具有多 GPU 的 SageMaker 实例类型。
2. 在环境变量或启动脚本中设置 `TENSOR_PARALLEL_SIZE`（例如设置为 4 或 8），对应实例的 GPU 数量。
3. 确保 vLLM 启动脚本正确初始化分布式通信后

---
## 学习要点

- 通过在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 的 PagedAttention 技术，可以显著降低显存占用并提高吞吐量，从而高效地同时服务数十个微调模型。
- 利用 Amazon SageMaker 的模型组件功能，可以将模型权重与推理代码解耦，实现多模型共享同一容器，大幅简化部署流程并节省存储空间。
- 借助 Amazon Bedrock 的自定义模型导入功能，用户可以将微调后的模型导入托管服务，并通过统一 API 调用，无需自行维护底层基础设施。
- vLLM 支持连续批处理和高效的 CUDA 图优化，能够最大化 GPU 利用率，在处理高并发请求时保持低延迟。
- 该解决方案允许在单一推理端点或托管环境中动态加载和切换不同的 LoRA 适配器，实现多租户场景下的资源高效利用。
- 通过将 vLLM 部署在 SageMaker 上，企业可以灵活选择 GPU 实例类型并利用自动扩缩容功能，以更具成本效益的方式处理大规模推理工作负载。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [vLLM](/tags/vllm/) / [LoRA](/tags/lora/) / [SageMaker](/tags/sagemaker/) / [Bedrock](/tags/bedrock/) / [MoE](/tags/moe/) / [模型推理](/tags/%E6%A8%A1%E5%9E%8B%E6%8E%A8%E7%90%86/) / [内核优化](/tags/%E5%86%85%E6%A0%B8%E4%BC%98%E5%8C%96/) / [GPT-OSS](/tags/gpt-oss/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [在 SageMaker AI 与 Bedrock 上利用 vLLM 高效部署多 LoRA 模型]({{< relref "posts/20260225-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-0.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpS]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-2.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已登陆 Amazon SageMaker JumpSt]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-4.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 现已在 Amazon SageMaker JumpSta]({{< relref "posts/20260212-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-6.md" >}})
- [NVIDIA Nemotron 3 Nano 30B 模型现已在 Amazon SageMaker JumpS]({{< relref "posts/20260213-blogs_podcasts-nvidia-nemotron-3-nano-30b-moe-model-is-now-availa-12.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*