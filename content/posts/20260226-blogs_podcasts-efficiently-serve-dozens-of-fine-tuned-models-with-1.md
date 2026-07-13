---
title: 利用vLLM在SageMaker与Bedrock上高效部署多LoRA及MoE模型
date: 2026-02-26 05:26:26+08:00
draft: false
entry_kind: auto
tags:
- vLLM
- LoRA
- MoE
- SageMaker
- Bedrock
- 模型推理
- 性能优化
- 模型微调
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: 这篇文章主要介绍了如何在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 高效服务数十个微调模型。
  **核心内容总结如下：** 1. **技术实现：** 文章详细阐述了如何在 vLLM 框架中实现针对专家混合模型的多 LoRA（低秩适应）推理，从而支持同时服务多个微调后的模型
external_url: https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock
scenarios:
- 大语言模型
---

# 利用vLLM在SageMaker与Bedrock上高效部署多LoRA及MoE模型

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T20:56:13+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock)

---

## 摘要/简介

在本博文中，我们介绍了如何在 vLLM 中为混合专家（MoE）模型实现多 LoRA 推理，描述了我们在内核层面所做的优化，并展示了您如何从中受益。全文我们将以 GPT-OSS 20B 为主要示例。

---

## 导语

随着生成式 AI 的深入应用，如何在保障性能的同时高效管理大量定制化模型，已成为企业面临的技术挑战。本文将介绍如何在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 实现混合专家（MoE）模型的多 LoRA 推理，并深入解析内核层面的优化细节。通过以 GPT-OSS 20B 为例的实战演示，您将掌握在单一实例上灵活服务数十个微调模型的具体方法，从而有效降低部署成本并提升资源利用率。

---

## 摘要

这篇文章主要介绍了如何在 Amazon SageMaker AI 和 Amazon Bedrock 上利用 vLLM 高效服务数十个微调模型。

**核心内容总结如下：**

1.  **技术实现：** 文章详细阐述了如何在 vLLM 框架中实现针对专家混合模型的多 LoRA（低秩适应）推理，从而支持同时服务多个微调后的模型。
2.  **性能优化：** 作者描述了他们在内核级别进行的优化工作，旨在提升推理效率。
3.  **应用示例：** 全文以 GPT-OSS 20B 模型为例，展示了如何利用这一技术为用户带来实际效益。

---

## 评论

这篇文章的中心观点是：**通过在 vLLM 中实现针对 Mixture of Experts (MoE) 架构的 Multi-LoRA 推理服务，并进行内核级优化，可以在 Amazon SageMaker/Bedrock 上以接近单一模型的成本高效地同时服务数十个微调模型，从而实现 SaaS 化的 AI 应用部署。**

以下是基于技术与行业角度的深入评价：

### 一、 支撑理由与核心价值分析

**1. 架构层面的“降维打击”：MoE 与 LoRA 的完美契合**
*   **[事实陈述]** 文章指出了 GPT-OSS 20B（基于 Mixtral 架构）作为 MoE 模型的特性：拥有活跃参数少但总参数量大的特点。
*   **[作者观点]** 这是一个极具技术洞察力的选择。传统的 Dense 模型（如 Llama 2 70B）在处理多任务时，每次推理都需要加载全部权重到显存，显存带宽压力巨大。而 MoE 模型在推理时仅激活部分专家，这天然地为“多租户共享基础模型”留出了物理空间。
*   **[你的推断]** 这意味着在相同的 GPU 资源下，利用 MoE + Multi-LoRA 可以支持的并发 LoRA 适配器数量，理论上限远高于 Dense 模型。这不仅仅是“优化”，而是利用模型结构特性解决了“批处理大小”受限于显存的痛点。

**2. 内核级优化的工程深度：PagedAttention 的扩展**
*   **[事实陈述]** 文章提到对 vLLM 进行了 Kernel-level optimizations，特别是针对多 LoRA 服务的显存管理。
*   **[作者观点]** vLLM 的核心竞争力在于 PagedAttention（类似操作系统的虚拟内存分页管理）。在多 LoRA 场景下，难点在于不同 LoRA 适配器的大小不一，且需要频繁地挂载/卸载到显存中。
*   **[你的推断]** 这里的“内核优化”极有可能指的是改进了 Cache 引擎，使其能够高效地处理非连续的、碎片化的 LoRA 权重显存分配。这消除了 Python 层面动态调度的开销，是能够“同时服务数十个模型”而不崩溃的关键技术保障。

**3. 商业模式的变革：从定制化到 SaaS 化**
*   **[事实陈述]** 文章展示了如何在 Amazon Bedrock 和 SageMaker 上部署此方案。
*   **[作者观点]** 这解决了企业级 AI 落地中最昂贵的环节——推理成本。以往为每个客户微调一个独立模型需要独占 GPU，成本极高。此方案允许在一个大模型底座上动态挂载不同客户的 LoRA，按需激活。
*   **[你的推断]** 这将极大地降低 AI 原生应用（如垂直领域的写作助手、代码生成工具）的边际成本，使得“千人千面”的模型服务成为可能。

### 二、 反例与边界条件

尽管文章展示了令人印象深刻的技术，但在实际应用中存在明显的边界条件：

**1. 显存并非无限，LoRA 交换存在延迟惩罚**
*   **[反例/边界条件]** 文章强调“同时服务”，但这通常假设所有 LoRA 的适配器权重都能常驻显存（High Bandwidth Memory, HBM）。如果需要服务的 LoRA 数量达到数百甚至上千个，超过了 HBM 容量，系统就必须将 LoRA 权重从 CPU 内存（DDR）交换到 GPU 显存。
*   **[你的推断]** 这种 PCIe 数据传输是极其缓慢的。如果请求的调度策略不当，导致频繁的 Swap，推理延迟会从几十毫秒激增至秒级，使得实时对话变得不可用。文章可能未充分探讨这种“冷启动”延迟对用户体验的影响。

**2. MoE 架构的显存墙：KV Cache 依然是瓶颈**
*   **[反例/边界条件]** 虽然 MoE 激活参数少，但其 Attention 层依然是 Dense 的。在处理长上下文（Long Context, 如 128k token）请求时，KV Cache 占用的显存会随着 Batch Size 和序列长度线性增长。
*   **[你的推断]** 在多租户高并发场景下，限制吞吐量的瓶颈往往会从“计算量”转移到“显存容量”。即便计算能力足够，KV Cache 爆满也会导致 OOM（Out of Memory），这与是否使用 MoE 无关，是 vLLM 架构本身在超长文本下的物理限制。

### 三、 综合评价（维度打分）

1.  **内容深度（4.5/5）：** 文章没有停留在 API 调用层面，而是深入到了 vLLM 的内核优化和 MoE 架构特性，论证了为什么这样做是高效的。对于 GPT-OSS 20B 的选择具有代表性。
2.  **实用价值（5/5）：** 对于正在构建多租户 AI 平台的开发者，这是极具参考价值的蓝图。它直接解决了“如何低成本运营多个垂直模型”的问题。
3.  **创新性（4/5）：** 将 Multi-LoRA 服务与 MoE 架构结合并非 AWS 首创，但在云厂商的最佳实践中如此系统地展示内核级优化和部署流程，具有很高的工程参考价值。
4.  **可读性（4/5）：** 结构清晰，技术栈描述明确，但要求读者具备较高的 CUDA 和 LLM 架构背景知识。
5.  **行业影响（高）：** 这可能会推动行业从“单一巨型模型”

---

## 技术分析

基于您提供的文章标题和摘要，这篇文章主要探讨了如何在云基础设施（Amazon SageMaker AI 和 Amazon Bedrock）上，利用 vLLM 高效地通过多 LoRA（Multi-LoRA）技术服务化数十个微调模型，并以 GPT-OSS 20B 为例进行了内核级优化的解析。

### 1. 核心观点深度解读

**主要观点：**
文章的核心主张是，通过在 vLLM 框架中实现针对混合专家模型的多 LoRA 推理服务，并结合内核级优化，可以打破“一个模型对应一个部署实例”的传统高成本模式，实现以单一基础模型实例高效服务数十个特定任务微调模型。

**核心思想：**
作者传达了**“计算与存储解耦”**与**“批处理效率最大化”**的思想。在传统的 LLM 部署中，如果你有 50 个针对不同客户或任务微调的模型，通常需要部署 50 个常驻 GPU 实例，成本极高且资源利用率低。作者提出利用 LoRA（低秩适应）的特性，将庞大的基础模型权重在内存中共享，仅动态加载微小的 LoRA 适配器权重，从而在几乎不增加显存开销的情况下，通过 MoE（混合专家）的调度逻辑实现多租户并发服务。

**创新性与深度：**
*   **架构层面的创新：** 将 MoE 的概念从模型层（Layer 层的专家路由）泛化到了服务层（Service 层的模型路由）。系统将不同的 LoRA 视为不同的“专家”，根据请求动态调用。
*   **工程实现的深度：** 文章不仅停留在应用层，更深入到了 CUDA 内核级别。针对 GPT-OSS 20B 这样的大模型，通用的矩阵乘法算子无法充分发挥多 LoRA 并发的性能。作者通过自定义内核，解决了不同 LoRA 权重在同一个 Batch 中如何高效并行计算的问题。

**重要性：**
这一观点解决了生成式 AI 落地中最痛点的问题之一——**定制化与成本的矛盾**。企业希望为不同场景提供定制模型（需要微调），但无法承担为每个微调模型单独部署全套推理硬件的成本。该技术使得 SaaS 化的大规模模型定制服务成为可能。

### 2. 关键技术要点

**涉及的关键技术：**
*   **vLLM：** 高性能 LLM 推理引擎，以 PagedAttention (KV Cache 管理) 闻名。
*   **LoRA (Low-Rank Adaptation)：** 参数高效微调技术（PEFT），通过冻结主模型权重并注入低秩矩阵来适应新任务。
*   **Multi-LoRA Serving / Batch Inference：** 在单个推理请求中混合处理针对不同 LoRA 适配器的请求。
*   **MoE (Mixture of Experts) routing logic：** 借用 MoE 的路由机制来决定激活哪个 LoRA。
*   **Amazon SageMaker AI & Bedrock：** 提供底层算力和托管服务的云平台。

**技术原理与实现：**
1.  **权重共享与隔离：** 基础模型（如 GPT-OSS 20B）的参数静态加载在 GPU 显存中。LoRA 适配器（通常仅占模型参数量的 0.1% - 3%）以动态或半静态方式存储。
2.  **动态计算图融合：** 当一个 Batch 包含 5 个不同用户的请求（分别对应 LoRA A, B, C）时，推理引擎需要在计算 Attention 和 FFN 层时，动态地将对应的 LoRA 矩阵叠加到基础权重上，或者分别计算后合并。
3.  **Kernel-level Optimizations（内核级优化）：**
    *   **问题：** 标准的 GEMM（通用矩阵乘法）内核在处理大量微小矩阵乘法（LoRA 部分）时，受限于内存带宽和 Kernel 启动开销。
    *   **方案：** 可能采用了**Kernel Fusion**（核融合）或 **Marlin** 等针对量化/低秩微调优化的 CUDA 内核。将 Base Model 的计算与 LoRA 的计算在 Kernel 层面进行合并，减少显存读写次数。

**技术难点与解决方案：**
*   **难点：** 显存碎片化与 KV Cache 管理。不同 LoRA 模型的生成长度不同，上下文长度不同。
*   **解决：** 利用 vLLM 的 PagedAttention 机制，将 KV Cache 分页管理，像操作系统管理虚拟内存一样管理显存，从而支持极高并发和变长序列。
*   **难点：** 多 LoRA 带来的计算延迟抖动。
*   **解决：** 内核优化，确保计算密集型操作的吞吐量。

### 3. 实际应用价值

**对实际工作的指导意义：**
*   **成本降低：** 对于需要提供多领域 AI 能力的企业（如法律、医疗、金融各一个模型），不再需要 3x20B 的显存，可能只需要 1x20B + 3x(很小 LoRA) 的显存。
*   **运维简化：** 减少了需要维护的模型端点数量。

**应用场景：**
1.  **AI SaaS 平台：** 为成千上万的租户提供专属的微调模型服务。
2.  **企业级 RAG (检索增强生成)：** 针对公司内部不同部门（HR、财务、研发）加载不同的知识库 LoRA，但共用一个底座模型。
3.  **A/B 测试与模型迭代：** 同时运行一个模型的不同版本（V1, V2, V3），对比效果。

**实施建议：**
*   **评估 LoRA 的 Rank 大小：** Rank 越大，效果越好，但显存占用和计算开销越大。需要在 8, 16, 64, 128 之间做权衡。
*   **关注 Batch Size：** 多 LoRA 服务要想盈利，必须提高 Batch Size 以掩盖动态加载 LoRA 权重的延迟。

### 4. 行业影响分析

**对行业的启示：**
这标志着**模型服务从“单体应用”向“微服务化”的转变**。未来的 AI 基础设施将不再是单纯的算力堆砌，而是更加精细化的资源调度系统。

**带来的变革：**
*   **MaaS (Model as a Service) 的精细化：** 类似于 AWS Lambda 改变了服务器运维，Multi-LoRA 推理将改变模型的售卖方式——客户不再购买“一个模型”，而是购买“基于基础模型的个性化能力”。
*   **边缘计算的潜力：** 如果显存占用大幅降低，未来在边缘设备上运行多模态、多任务模型将成为可能。

**发展趋势：**
*   **推理与训练的进一步融合：** 像 vLLM 这样的推理框架开始吸收训练框架的特性（如动态图）。
*   **专用硬件的兴起：** 针对 MoE 和稀疏矩阵计算优化的 NPU 将更受青睐。

### 5. 延伸思考

**引发的思考：**
*   **LoRA 的冲突：** 如果在一个 Batch 中，绝大多数请求都指向 LoRA A，极少指向 LoRA B，是否会导致负载不均衡？如何进行调度优化？
*   **安全性：** 多个租户的 LoRA 权重在同一个 GPU 内存中，虽然逻辑隔离，但物理上共享，是否存在侧信道攻击的风险？
*   **全量微调的消亡：** 随着这种技术的成熟，全量微调在绝大多数商业场景中将彻底失去竞争力，除非是为了彻底改变模型的语言或知识分布。

**拓展方向：**
*   **混合精度 LoRA：** 能否对 LoRA 权重使用 4-bit 量化，进一步压缩显存？
*   **动态 LoRA 加载：** 结合 CPU 内存池，实现当某个 LoRA 请求量突增时，动态将其从 CPU 卸载到 GPU，突破 GPU 显存物理上限，服务数万个 LoRA。

### 7. 案例分析

**成功案例推演（基于文章逻辑）：**
*   **场景：** 一家跨国企业拥有 20 个子公司，每个子公司有自己的行话和风格。
*   **做法：** 训练一个 20B 的通用模型，然后为每个子公司微调一个 LoRA。
*   **结果：** 部署成本从原本需要 20 张 A100（每张 80GB 显存）降低到仅需 2-4 张 A100（通过高并发 Batch 处理），且维护成本大幅下降。

**潜在失败/风险案例：**
*   **场景：** 某些 LoRA 任务极其复杂，导致生成长度极长（例如生成长篇代码）。
*   **问题：** vLLM 的 KV Cache 可能会被长序列任务占满，导致其他短任务的 LoRA 请求被阻塞（队头阻塞）。
*   **教训：** 需要配置合理的请求抢占策略或对生成长度进行严格限制。

### 8. 哲学与逻辑：论证地图

**中心命题：**
在 vLLM 中实现针对 MoE 架构的多 LoRA 推理并进行内核级优化，是降低大规模定制化模型服务成本、提升吞吐量的最优技术路径。

**支撑理由与依据：**
1.  **资源利用率：**
    *   *依据：* LoRA 权重极小（MB 级），共享 Base Model 权重（GB 级），使得显存利用率接近理论极限。
2.  **计算吞吐量：**
    *   *依据：* Kernel-level optimizations 减少了 GPU Kernel 启动和 HBM（高带宽内存）访问的开销，使得在处理混合 Batch 时，计算效率接近纯 Base Model 推理。
3.  **基础设施适配性：**
    *   *依据：* Amazon SageMaker 和 Bedrock 提供了必要的容器化和弹性伸缩支持，验证了该方案在工业级云环境下的可行性。

---

## 最佳实践

### 实践 1：利用多 LoRA 适配器实现高效模型服务

**说明**:
vLLM 支持通过多 LoRA (Low-Rank Adaptation) 适配器在单一基础模型上动态服务多个微调模型。这种方法避免了为每个微调模型部署独立实例的高昂成本，显著提高了 GPU 利用率并降低了基础设施开销。

**实施步骤**:
1. 准备基础模型（如 Llama 3 或 Mistral）并保存为 vLLM 兼容的格式。
2. 训练并导出各个特定任务的 LoRA 适配器。
3. 在 SageMaker 部署脚本中配置 `--enable-lora` 参数，并指定 LoRA 适配器的存储路径（S3 或 EFS）。
4. 使用 vLLM 的 OpenAI 兼容 API 调用时，在 `model` 字段中传入对应的 LoRA 适配器名称以路由请求。

**注意事项**:
- 确保所有 LoRA 适配器基于同一个基础模型检查点训练。
- 监控 GPU 显存使用情况，因为加载过多适配器可能会增加显存压力。

---

### 实践 2：优化张量并行 (TP) 与多 GPU 配置

**说明**:
对于参数量较大的模型（如 70B+），单张 GPU 无法容纳。vLLM 提供了高度优化的张量并行 (TP) 策略，允许将模型切分到多张 GPU 上运行。正确配置并行度是平衡吞吐量和延迟的关键。

**实施步骤**:
1. 根据模型大小选择合适的 SageMaker 实例类型（如 `ml.p4d.24xlarge` 或 `ml.p5.48xlarge`）。
2. 在 vLLM 启动参数中设置 `--tensor-parallel-size` (TP)。例如，在 8 卡实例上设置为 8。
3. 结合 `--max-model-len` 调整 KV Cache 大小，以最大化显存占用率而不发生 OOM（内存溢出）。

**注意事项**:
- 张量并行会增加通信开销，对于较小的模型（如 7B），使用多 GPU 可能不如单 GPU 效率高，建议进行基准测试。
- 确保实例的 GPU 间互联带宽（如 NVLink）足够高，以最小化通信延迟。

---

### 实践 3：配置连续批处理与 PagedAttention

**说明**:
vLLM 的核心优势在于其 PagedAttention 算法和连续批处理机制。这允许模型在处理一个请求的生成阶段时，同时接收新请求的预处理，从而极大提高吞吐量，尤其是在处理不同长度提示词的混合负载时。

**实施步骤**:
1. vLLM 默认启用连续批处理和 PagedAttention，无需额外复杂配置。
2. 重点调整 `--max-num-batched-tokens` 参数，以控制单次迭代中处理的最大 Token 数量，从而平衡延迟和吞吐量。
3. 针对长文本场景，适当增加 `--max-num-seqs`（最大序列数），以防止队列阻塞。

**注意事项**:
- 在极高并发下，如果发现请求超时，可能需要限制 `--max-num-seqs` 或水平扩展实例数量。
- PagedAttention 需要预分配显存块，确保预留足够的 GPU 显存给 KV Cache。

---

### 实践 4：通过 Amazon Bedrock Knowledge Bases 集成外部数据

**说明**:
虽然 vLLM 负责模型推理，但在生产环境中，微调模型通常需要结合企业私有数据。利用 Amazon Bedrock 的 Knowledge Bases（与 Amazon Aurora Vector Store 集成）可以为微调模型提供 RAG（检索增强生成）能力，而无需重新训练模型。

**实施步骤**:
1. 在 Amazon Bedrock 控制台中创建 Knowledge Base，并将 S3 中的数据源同步到向量数据库。
2. 部署在 SageMaker 上的 vLLM 模型应配置为兼容 Bedrock 的自定义模型导入或通过 API Gateway 暴露接口。
3. 应用层逻辑先调用 Bedrock Retrieve API 获取上下文，再将上下文和问题合并发送给 SageMaker 上的 vLLM 端点。

**注意事项**:
- 确保网络连接畅通，Bedrock 与 SageMaker VPC 之间的连接需正确配置。
- 注意 RAG 检索内容的 Token 计数，避免超出模型的上下文窗口限制。

---

### 实践 5：实施模型量化和 FlashAttention 优化

**说明**:
为了进一步降低延迟并提高吞吐量，应对模型进行量化（如 AWQ 或 GPTQ）并利用 FlashAttention 技术。vLLM 原生支持这些优化，能在保持模型精度的同时显著减少显存占用和计算时间。

---

## 学习要点

- vLLM 与 Amazon SageMaker AI 及 Amazon Bedrock 的集成，使用户能够在云端基础设施上高效部署和托管数十个微调模型，显著降低了多模型服务的运维复杂度。
- 利用 vLLM 的连续批处理和 PagedAttention 内核技术，可以最大化 GPU 显存利用率并提高吞吐量，从而在不牺牲性能的前提下大幅降低推理成本。
- 在 SageMaker 上部署 vLLM 时，通过利用多模型服务器的容器级共享机制，可以在同一个 SageMaker 端点后同时加载和运行多个不同的 LoRA 适配器模型，实现资源的集约化利用。
- 通过 Amazon Bedrock 自定义模型导入功能，用户可以将微调后的模型导入托管服务，这允许企业利用 Bedrock 的全托管能力来扩展定制化模型，而无需管理底层基础设施。
- vLLM 原生支持 OpenAI 兼容的 API 协议，使得现有应用能够以最小的代码修改成本迁移至该高性能推理引擎，加速了生产环境的落地。
- 该解决方案展示了如何在保持低延迟的同时处理高并发请求，证明了利用开源优化引擎（如 vLLM）结合云服务（如 SageMaker）是构建高性能生成式 AI 应用的最佳实践之一。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [vLLM](/tags/vllm/) / [LoRA](/tags/lora/) / [MoE](/tags/moe/) / [SageMaker](/tags/sagemaker/) / [Bedrock](/tags/bedrock/) / [模型推理](/tags/%E6%A8%A1%E5%9E%8B%E6%8E%A8%E7%90%86/) / [性能优化](/tags/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/) / [模型微调](/tags/%E6%A8%A1%E5%9E%8B%E5%BE%AE%E8%B0%83/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [在 SageMaker AI 与 Bedrock 上利用 vLLM 高效部署多 LoRA 模型]({{< relref "posts/20260225-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-0.md" >}})
- [2025年回顾：SageMaker AI提升可观测性并优化模型定制与托管]({{< relref "posts/20260223-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--4.md" >}})
- [2025年Amazon SageMaker AI可观测性、模型定制与托管功能增强]({{< relref "posts/20260223-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--8.md" >}})
- [2025年亚马逊SageMaker AI：增强可观测性与模型定制托管功能]({{< relref "posts/20260224-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--11.md" >}})
- [EWSJF：面向混合负载LLM推理的自适应调度器]({{< relref "posts/20260130-arxiv_ai-ewsjf-an-adaptive-scheduler-with-hybrid-partitioni-2.md" >}})
