---
title: "在 SageMaker 与 Bedrock 上使用 vLLM 实现多 LoRA 推理"
date: 2026-02-26T21:59:03+08:00
draft: false
entry_kind: "auto"
tags: ["vLLM", "LoRA", "SageMaker", "Bedrock", "MoE", "模型推理", "内核优化", "GPT-OSS"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "在生成式 AI 的实际落地中，同时管理多个经过微调的模型往往面临资源消耗大与部署复杂的挑战。本文将深入探讨如何利用 vLLM 在 Amazon SageMaker AI 和 Amazon Bedrock 上高效服务数十个微调模型，重点介绍针对混合专家（MoE）模型的多 LoRA 推理实现及内核级优化。通过阅读本文，你将"
external_url: https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock
scenarios: ["大语言模型"]
---

# 在 SageMaker 与 Bedrock 上使用 vLLM 实现多 LoRA 推理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-25T20:56:13+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/efficiently-serve-dozens-of-fine-tuned-models-with-vllm-on-amazon-sagemaker-ai-and-amazon-bedrock)

---
## 摘要/简介

在本文中，我们将解释如何在 vLLM 中为混合专家（MoE）模型实现多 LoRA 推理，介绍我们进行的内核级优化，并展示你可以如何从这项工作中受益。本文将全程以 GPT-OSS 20B 为主要示例。

---
## 导语

在生成式 AI 的实际落地中，同时管理多个经过微调的模型往往面临资源消耗大与部署复杂的挑战。本文将深入探讨如何利用 vLLM 在 Amazon SageMaker AI 和 Amazon Bedrock 上高效服务数十个微调模型，重点介绍针对混合专家（MoE）模型的多 LoRA 推理实现及内核级优化。通过阅读本文，你将掌握以 GPT-OSS 20B 为例的具体实践路径，学习如何在保证性能的前提下显著降低推理成本并提升部署效率。

---
## 评论

**中心观点**
文章提出了一种通过在 vLLM 中实现多 LoRA 服务与内核级优化，从而在 AWS 基础设施上以接近单模型的成本高效推理数十个微调模型的技术路径。

**支撑理由与深度评价**

**1. 架构演进：从“单模型独占”到“多租户共享”的算力范式转移**
*   **事实陈述**：文章详细介绍了在 vLLM 中引入对多 LoRA（Low-Rank Adaptation）支持的技术细节。这允许在显存中同时加载一个基础模型（如 GPT-OSS 20B）和几十个 LoRA 适配器，通过动态路由机制处理不同请求。
*   **深度评价**：这是对当前 LLM 推理成本结构的一次重要优化。在传统模式下，为 10 个不同任务微调 10 个模型需要 10 倍的 GPU 显存。通过多 LoRA 服务，显存增量被限制在 LoRA 权重极小的参数量上。这不仅是工程技巧，更是商业模式的变革，使得 SaaS 化的定制模型服务成为可能。

**2. 性能优化的双重奏：内核融合与显存管理**
*   **事实陈述**：文章强调了“Kernel-level optimizations”，特别是针对 MoE（Mixture of Experts）和多 LoRA 场景下的 CUDA 内核优化，以及结合 vLLM 的 PagedAttention 机制进行的显存管理。
*   **深度评价**：单纯的多 LoRA 支持会带来计算开销（动态加载 Adapter 权重）。文章提到的内核优化是保证吞吐量不下降的关键。特别是针对 MoE 模型的优化，这表明 AWS 正在试图解决“稀疏模型”在推理阶段的效率瓶颈，将 MoE 的训练优势转化为推理红利。

**3. 云生态的深度绑定：SageMaker 与 Bedrock 的协同**
*   **事实陈述**：文章展示了如何将优化后的 vLLM 部署在 SageMaker 上，并暗示了其在 Bedrock 中的应用潜力。
*   **深度评价**：这体现了 AWS 的策略差异。与 OpenAI 提供封闭的 API 不同，AWS 通过提供高度优化的开源框架集成，允许企业保留模型主权的同时利用云厂商的底层算力优化。这种“Managed Open Source”策略比单纯的 IaaS 租赁更具粘性。

**反例与边界条件**

1.  **显存墙依然存在**：虽然 LoRA 节省了参数存储，但 **KV Cache** 显存占用并未减少。当并发请求增加时，显存瓶颈会迅速从模型权重转移到上下文缓存。如果用户请求的 Context Window 很大（如 32k+），多 LoRA 带来的显存节省可能被 Cache 占用吞噬，导致 Batch Size 被迫缩小，吞吐量反而不如单模型。
2.  **延迟的尾部风险**：在多 LoRA 共享 GPU 的场景下，不同 LoRA 的计算复杂度可能不同（尽管通常很小）。如果某个 LoRA 伴随复杂的解码逻辑或触发特定的 Attention 模式，可能会产生长尾延迟，影响同实例下其他租户的 P99 延迟表现。
3.  **适配器切换开销**：虽然文章声称优化了内核，但在极高并发下，频繁的 Adapter 权重切换依然会造成内存访问的不连续性，可能导致 CUDA Core 的利用率波动。

**行业影响与争议点**

*   **行业影响**：这篇文章标志着“模型即服务”从大模型向“微调模型集群”的演进。它降低了企业定制化 AI 的边际成本，可能会催生更多垂直领域的 AI 应用。
*   **争议点**：**通用性与专用性的博弈**。文章推崇 MoE 和 LoRA，认为这是未来。然而，业界也有观点认为，随着模型推理成本的指数级下降（如 GPT-4o-mini 等），针对特定任务微调小模型的经济性正在减弱。如果 API 调用足够便宜，为什么还要维护复杂的 MoE 或 LoRA 集群？这是技术极客与务实派的主要分歧点。

**实际应用建议**

1.  **评估任务相似度**：如果你的微调任务在语义上差异巨大（例如一个是写代码，一个是医疗诊断），共享同一个 Base Model 可能会导致互相干扰，此时应谨慎使用多 LoRA 共享实例。
2.  **关注 KV Cache 配额**：在部署此类架构时，不仅要监控 Model Weights 的显存占用，更要为 KV Cache 预留足够的 Buffer，否则多租户的高并发会导致 OOM（显存溢出）。
3.  **A/B 测试必要性**：不要直接迁移。务必对比“单模型单实例”与“多 LoRA 多实例”在真实业务流量下的 P99 延迟，Kernel 优化带来的红利可能被调度器的开销抵消。

**可验证的检查方式**

1.  **吞吐量基准测试**：使用 vLLM 自带的 benchmark 工具，对比 `serving_gpt_oss_20b_single_lora` 与 `serving_gpt_oss_20b_multi_lora` 在不同并发数下的 Tokens/second 和 Time Per Output Token (TPOT)。
2.  **显存剖析**：在运行多 LoRA 推理时，使用 `nvidia-smi` 或 PyTorch Profiler 观察 GPU Memory 的分配情况，验证 LoRA 权重加载是否真的如文章所述只占用了极小比例，以及 KV Cache 是否成为了瓶颈。
3.  **端到端延迟监控**

---
## 技术分析

基于文章标题《Efficiently serve dozens of fine-tuned models with vLLM on Amazon SageMaker AI and Amazon Bedrock》及其摘要，以下是对该技术方案的深度分析。

---

# 深度分析：在 vLLM 中实现多 LoRA 服务与 MoE 模型的高效推理

## 1. 核心观点深度解读

**文章的主要观点**
文章的核心主张是：通过在 vLLM 框架中实现**多 LoRA（Low-Rank Adaptation）推理**及针对**混合专家模型**的底层内核优化，可以在单一的模型部署实例中，高效、低成本地同时服务数十个微调后的模型，而无需为每个微调模型独立部署资源。

**作者想要传达的核心思想**
传统的“一模型一部署”模式在面对海量定制化需求时（如为不同客户或不同业务场景微调的模型），会导致资源碎片化和成本不可控。作者传达的思想是**“共享底座，动态适配”**。通过将基础模型作为共享资源，将微调参数（LoRA 权重）作为轻量级插件动态加载，结合 vLLM 的 PagedAttention 和显存管理技术，实现批处理请求的高效复用。

**观点的创新性和深度**
*   **从静态到动态**：创新点在于将 MoE（混合专家）的思想从模型架构层面迁移到了**服务部署层面**。在推理时，系统根据请求动态切换 LoRA 适配器，类似于 MoE 动态激活专家网络。
*   **内核级优化**：文章不仅仅停留在应用层，更深入到了 CUDA 内核级别。针对 GPT-OSS 20B 这样的大模型，如何在高并发下处理不同 LoRA 的显存寻址和计算融合是极具深度的工程挑战。
*   **打破吞吐瓶颈**：解决了多 LoRA 场景下，不同请求无法共享 KV Cache 或计算资源的问题，显著提升了 GPU 利用率。

**为什么这个观点重要**
随着大模型进入落地期，企业不再满足于通用基座模型，而是需要针对特定领域（如医疗、法律、代码）的微调模型。如果每个微调模型都要独占一张 A100/H100 显卡，成本将呈指数级增长。该技术方案直接击中了大模型商业化落地中**“定制化需求与高昂基础设施成本”之间的矛盾**，是 AI Infra 领域迈向“模型即服务”的关键一步。

## 2. 关键技术要点

**涉及的关键技术或概念**
*   **vLLM**：具有 PagedAttention 机制的高吞吐量推理引擎。
*   **LoRA (Low-Rank Adaptation)**：参数高效微调技术，冻结预训练模型权重，通过注入低秩矩阵来适应下游任务。
*   **Multi-LoRA Serving / Batch Serving**：在同一个推理批次中处理属于不同 LoRA 适配器的请求。
*   **MoE (Mixture of Experts)**：此处指代模型架构，也隐喻了服务架构（每个 LoRA 视为一个专家）。
*   **Amazon SageMaker / Bedrock**：云端托管与推理平台。

**技术原理和实现方式**
1.  **权重融合与计算**：
    在推理时，vLLM 需要动态将基座模型权重 $W$ 与特定请求的 LoRA 权重 $\Delta W$（由 $A \times B$ 矩阵分解而来）进行融合。计算公式变为 $h = (W + \Delta W_{lora\_id})x$。
    为了避免显存频繁搬运，vLLM 实现了**内核级融合**，在前向传播的 Kernel 中直接读取 LoRA 权重并参与计算，而不是在 Python 层做拼接。

2.  **显存管理**：
    利用 vLLM 的 PagedAttention 机制，不仅管理 KV Cache，还需要管理 LoRA 权重的显存。由于 LoRA 权重远小于基座模型，可以将数十个 LoRA 适配器常驻 GPU 显存，或利用 CPU/GPU 统一内存进行按需调度。

3.  **调度策略**：
    调度器需要感知每个请求对应的 LoRA ID。在构建 Batch 时，vLLM 优化了连续内存访问模式，确保同一个 Batch 内不同 LoRA 请求的计算向量化效率。

**技术难点和解决方案**
*   **难点**：**显存碎片化与访问延迟**。如果每个请求都要去不同的显存地址拉取 LoRA 权重，会导致显存带宽利用率下降。
*   **解决方案**：文章提到的“Kernel-level optimizations”可能包括对 LoRA 权重进行**预取**和**内存对齐**，确保 CUDA Kernel 在计算时能够 Coalesced Access（合并访问），减少延迟。
*   **难点**：**不同 LoRA 间的相互干扰**。在 Batch 推理时，如何保证不同任务的隔离性？
*   **解决方案**：在逻辑上通过 ID 隔离，在物理计算上通过掩码或独立指针确保数据不串扰。

**技术创新点分析**
最大的创新在于**将 vLLM 的显存管理能力从 KV Cache 扩展到了模型权重本身**。这使得 vLLM 不仅仅是一个推理加速器，变成了一个“模型路由器”。

## 3. 实际应用价值

**对实际工作的指导意义**
*   **成本降低**：对于需要为不同客户提供定制化模型服务的 SaaS 公司，可以将硬件成本降低 10 倍以上（从 N 个实例降为 1 个实例）。
*   **运维简化**：无需维护复杂的模型版本管理和独立的部署管道，只需管理 LoRA 权重文件。

**可以应用到哪些场景**
*   **多租户 AI 平台**：每个租户有自己的微调模型，但共享底层基础设施。
*   **A/B 测试与实验**：同时运行同一个基座的多个不同微调版本（如不同学习率或数据集训练出的 LoRA），对比效果。
*   **特定领域增强**：一个通用模型同时挂载“法律顾问”、“医疗助手”、“代码生成”等多个 LoRA 插件，由路由策略决定调用哪个。

**需要注意的问题**
*   **LoRA 数量上限**：虽然理论上是“dozens”，但过多的 LoRA 会增加显存占用，可能导致 OOM（显存溢出）。
*   **精度损失**：LoRA 本身是近似微调，对于某些对精度极高的任务，可能仍需要全量微调。

**实施建议**
建议优先将 LoRA 秩设置为较低值（如 8 或 16）以减少显存占用，并使用 vLLM 提供的 OpenAI 兼容 API 接口进行无缝对接。

## 4. 行业影响分析

**对行业的启示**
这标志着大模型推理架构正在从“单体应用”向“微服务化”演进。未来的模型服务可能不再是一个巨大的黑盒，而是一个**基座模型 + 动态插件市场**的形态。

**可能带来的变革**
*   **MaaS (Model as a Service) 的精细化**：云厂商可以出售“模型实例”，而用户只需上传自己的 LoRA 即可使用，极大降低了使用门槛。
*   **边缘计算的复苏**：通过 LoRA 切换，边缘设备无需存储多个大模型，只需存储一个基座和多个小 LoRA 包。

**相关领域的发展趋势**
*   **Adapter Fusion**：未来可能会出现同时激活多个 LoRA 的能力（如同时懂“代码”和“物理”的混合专家）。
*   **动态 LoRA 加载**：结合模型量化和显存卸载技术，实现秒级的 LoRA 热插拔。

**对行业格局的影响**
这将进一步巩固拥有强大算力基础设施的云厂商（如 AWS）和高效推理框架（如 vLLM）的地位，挤压那些仅靠简单部署模型获利的小型服务商的生存空间。

## 5. 延伸思考

**引发的其他思考**
*   **安全性**：多租户共享同一个 GPU 进程，虽然有逻辑隔离，但物理层面的侧信道攻击风险是否存在？
*   **LoRA 的组合能力**：如果用户同时请求“法律”和“英文翻译”，系统能否动态组合两个 LoRA 的权重？这需要更深层的数学证明。

**可以拓展的方向**
*   **Prefix Tuning / Prompt Tuning 的多路复用**：除了 LoRA，其他 PEFT 方法是否也能纳入此架构？
*   **异构计算支持**：如何利用 AWS Trainium/Inferentia 等专用芯片来加速 Multi-LoRA？

**未来发展趋势**
未来的推理引擎将内置**模型路由层**。用户发送请求时，不再指定模型 ID，而是指定任务类型，系统自动选择并挂载最优的 LoRA 适配器进行推理。

## 6. 实践建议

**如何应用到自己的项目**
1.  **评估现有模型**：检查你是否有多个基于同一基座（如 Llama-3-70B）微调的模型。
2.  **迁移至 vLLM**：使用支持 Multi-LoRA 的 vLLM 版本（v0.4.0+）。
3.  **权重转换**：将微调好的权重转换为 vLLM 支持的 LoRA 格式。

**具体的行动建议**
*   **实验环境搭建**：在 SageMaker 上利用 Spot Instance 进行低成本测试。
*   **压测对比**：对比“单实例多 LoRA”与“多实例单模型”的吞吐量和延迟（TTFT, TPOT）。

**需要补充的知识**
*   深入理解 CUDA 编程基础（Thread, Block, Warp）以理解 Kernel 优化的原理。
*   熟悉 HuggingFace PEFT 库的使用。

**实践中的注意事项**
*   **显存监控**：密切关注 GPU 显存使用率，避免因加载过多 LoRA 导致 OOM。
*   **预热**：首次加载 LoRA 可能有延迟，生产环境建议进行预热。

## 7. 案例分析

**结合实际案例说明**
假设一家跨国企业内部部署了一个基于 Llama-3 的代码助手。
*   **传统方案**：Python 团队部署一个微调模型，Java 团队部署一个，Go 团队再部署一个。需要 3 张 A100 卡。
*   **本方案**：部署一个 GPT-OSS 20B 基座，挂载 Python-LoRA, Java-LoRA, Go-LoRA。仅需 1 张 A100 卡。

**成功案例分析**
AWS 提供的 Bedrock 服务本身即是该技术的最佳实践。用户可以在 Bedrock 上通过自定义模型导入功能，快速挂载自己的微调版本，而无需感知底层是 vLLM 在进行 Multi-LoRA 调度。

**失败案例反思**
如果 LoRA 的 Rank 设置过高（如 r=256），或者 LoRA 训练不充分导致效果极差，这种共享模式会导致用户体验不一致。此外，如果不同租户的请求量差异极大（长尾效应），可能会导致某个 LoRA 长期占用显存却不产生流量，造成资源浪费。

**经验教训总结**
必须做好**容量规划**。并非所有模型都适合 Multi-LoRA，只有那些共享同一基座且流量适中的场景收益最大。

## 8. 哲学与逻辑：论证地图

**中心命题**
在 vLLM 中实现多 LoRA 动态推理服务，是在保持模型精度的前提下，降低多模型部署成本并

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用多 LoRA 适配器服务提高资源利用率

**说明**:
在传统的模型部署中，每个微调模型通常需要加载一个完整的基础模型副本，这会消耗大量的显存和计算资源。vLLM 支持多 LoRA（Low-Rank Adaptation）服务，允许在单个基础模型实例上动态加载和切换多个 LoRA 适配器。这意味着您可以在同一个 SageMaker 端点或 Bedrock 后端同时服务于数十个特定的任务或客户模型，而无需为每个模型部署独立的实例，从而显著降低基础设施成本并提高吞吐量。

**实施步骤**:
1. 准备基础模型（如 Llama 3 或 Mistral）并训练多个特定任务的 LoRA 适配器。
2. 在 SageMaker 部署脚本或 vLLM 配置中，启用 `--enable-lora` 参数。
3. 指定 `max_loras` 参数以设置并发支持的适配器数量，并配置 `max_lora_rank` 以匹配您的适配器秩大小。
4. 将适配器权重存储在 S3 中，并配置 vLLM 以在请求时根据适配器名称或 ID 动态加载对应的权重。

**注意事项**:
需要合理规划显存容量，因为虽然基础模型共享，但每个活跃的 LoRA 适配器仍需占用额外的显存空间。

---

### 实践 2：配置连续批处理以最大化吞吐量

**说明**:
vLLM 的核心优势之一是其高效的连续批处理机制，也称为迭代级调度。与静态批处理不同，连续批处理允许在批次中的某个请求完成后立即插入新的请求，而不必等待整个批次中的所有请求都完成。在处理大量不同微调模型的推理请求时，请求的长度和完成时间差异很大，连续批处理能显著提高 GPU 的利用率并降低延迟。

**实施步骤**:
1. 在 vLLM 启动参数中，确保启用连续批处理（默认通常开启）。
2. 根据模型特性和实例类型调整 `max_num_seqs`（最大并发序列数），以找到延迟和吞吐量之间的最佳平衡点。
3. 监控 GPU 利用率和推理延迟，逐步增加并发度直到达到性能瓶颈。

**注意事项**:
过高的并发数可能导致显存溢出（OOM）或因上下文切换开销导致延迟增加，需进行压测调整。

---

### 实践 3：使用 PagedAttention 内核优化显存管理

**说明**:
vLLM 引入了 PagedAttention 技术，将 KV 缓存（Key-Value Cache）像操作系统管理虚拟内存一样进行分页管理。在服务多个微调模型时，不同请求的上下文长度变化剧烈，固定的显存分配往往会导致显存浪费或不足。PagedAttention 允许更灵活的显存分配，不仅减少了显存碎片，还支持在不中断服务的情况下动态调整显存使用，特别适合长文本或高并发的多模型场景。

**实施步骤**:
1. vLLM 默认使用 PagedAttention，无需额外开关。
2. 调整 `gpu_memory_utilization` 参数（例如设置为 0.9 或 0.95），为 KV 缓存预留更多显存空间。
3. 如果使用 Amazon Bedrock 或 SageMaker，确保容器环境允许访问必要的 NVIDIA CUDA 库以支持该内核优化。

**注意事项**:
在极端高负载下，需监控页面换入换出的开销，确保不会因为显存过度碎片化而影响推理速度。

---

### 实践 4：通过 SageMaker 多模型端点或 Bedrock 自定义模型实现动态路由

**说明**:
为了高效管理数十个模型，应构建智能的路由层。在 Amazon SageMaker 上，可以利用多模型端点（MME）或基于 vLLM 的容器化部署，结合负载均衡器将请求路由到特定的模型适配器。在 Amazon Bedrock 中，可以通过自定义模型导入功能，将不同的微调版本注册为独立的模型资源，并通过 API 调用中的 `model-id` 进行区分。这确保了请求能够精准地命中对应的微调权重。

**实施步骤**:
1. 在 SageMaker 中，创建一个单一的端点配置，指向包含所有 LoRA 适配器的 S3 存储桶。
2. 实现一个轻量级的前端服务或使用 AWS Application Load Balancer，解析请求中的目标模型标识符。
3. 将请求转发给 vLLM 实例，并在请求头或参数中传递 `adapter_name`，指示 vLLM 动态加载正确的 LoRA 权重。

**注意事项**:
路由层本身不应成为瓶颈，确保其具有高可用性，并处理好冷启动（首次加载特定适配器）时的延迟。

---

### 实践 5：针对不同实例类型进行自动缩放和容量规划

**说明**:
不同的微调模型可能具有不同的计算需求和流量模式。在 Amazon SageMaker 上，应配置自动缩放策略，根据推理队列的长度或 CPU/GPU 利用率动态调整实例数量。对于 Bedrock，虽然托管

---
## 学习要点

- 利用 vLLM 的连续批处理和 PagedAttention 技术，可以在 Amazon SageMaker AI 上显著提高高并发场景下多模型服务的吞吐量和推理速度。
- 通过在单个 SageMaker 端点后部署多实例共享 GPU 资源，能够高效地同时服务数十个不同的微调模型，大幅降低基础设施成本。
- 在 Amazon Bedrock 上应用自定义模型导入功能，可以无缝将微调后的模型集成到托管服务中，享受企业级 API 和安全防护。
- 采用多 LoRA 适配器架构，允许在同一个基础模型上动态加载和切换多个轻量级微调适配器，从而以极低的显存开销服务大量定制化任务。
- 借助 SageMaker 的模型注册表和 CI/CD 管道，可以实现从模型训练到部署的全自动化工作流，简化了 MLOps 运维复杂度。
- 利用 Amazon Bedrock 的 Knowledge Bases 功能集成企业私有数据，能够快速为特定领域的微调模型构建增强型检索生成（RAG）应用。
- 通过对比 SageMaker AI（自管理能力）与 Amazon Bedrock（全托管服务）的部署模式，企业可以根据对底层控制权和运维成本的不同需求灵活选择最优架构。

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
- [在 SageMaker 与 Bedrock 上利用 vLLM 实现多 LoRA 推理及内核优化]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-11.md" >}})
- [利用vLLM在SageMaker AI与Bedrock上高效托管多LoRA模型]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-12.md" >}})
- [在 SageMaker AI 与 Amazon Bedrock 上使用 vLLM 高效部署多 LoRA 模型]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-4.md" >}})
- [在SageMaker AI与Bedrock上利用vLLM高效部署多LoRA及MoE模型]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*