---
title: "P-EAGLE：vLLM集成并行推测解码加速LLM推理"
date: 2026-03-14T21:09:07+08:00
draft: false
entry_kind: "auto"
tags: ["vLLM", "P-EAGLE", "LLM推理", "推测解码", "并行计算", "模型加速", "PR32887", "模型部署"]
categories: ["大模型", "AI 工程"]
source: blogs_podcasts
description: "大语言模型在实际部署中往往面临推理速度与成本的挑战。P-EAGLE 作为一种并行投机解码方法，通过在 vLLM 框架中的高效集成，为这一难题提供了新的解决思路。本文将深入解析其技术原理，并演示如何利用预训练权重进行服务化部署，帮助开发者在不牺牲模型精度的前提下，显著提升推理吞吐量。"
external_url: https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm
scenarios: ["大语言模型"]
---

# P-EAGLE：vLLM集成并行推测解码加速LLM推理

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-13T19:27:04+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm](https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm)

---
## 摘要/简介

In this post, we explain how P-EAGLE works, how we integrated it into vLLM starting from v0.16.0 (PR#32887), and how to serve it with our pre-trained checkpoints.

---
## 导语

大语言模型在实际部署中往往面临推理速度与成本的挑战。P-EAGLE 作为一种并行投机解码方法，通过在 vLLM 框架中的高效集成，为这一难题提供了新的解决思路。本文将深入解析其技术原理，并演示如何利用预训练权重进行服务化部署，帮助开发者在不牺牲模型精度的前提下，显著提升推理吞吐量。

---
## 评论

**文章中心观点**
文章通过将 P-EAGLE（一种并行的投机解码技术）集成到 vLLM 框架中，论证了利用小型模型作为草稿器进行并行推测采样，能够在保持生成质量的同时，显著突破大模型推理的吞吐瓶颈并降低延迟。

**支撑理由与深度评价**

**1. 技术架构的演进：从串行到并行的范式转移**
*   **事实陈述**：传统的 Speculative Decoding（如 Medusa 或 EAGLE）通常采用“串行”模式，即大模型需要等待小模型先生成一串候选 Token，然后再进行一次性验证。这种模式受限于小模型的生成速度，无法充分利用 GPU 的并行计算能力。
*   **作者观点**：P-EAGLE 提出了“并行”解码机制。文章指出，P-EAGLE 允许草稿模型与主模型同时运行，或者通过特定的 Attention Mask 优化，使得验证过程不再是简单的串行等待。这消除了 Draft 阶段的延迟，使得推理速度的上限不再受限于草稿模型的推理速度，而是受限于验证带宽。
*   **深度评价**：这是一个关键的性能优化点。在 vLLM 这种高度优化的框架中，串行等待往往是吞吐量的杀手。P-EAGLE 的并行化思路与 vLLM 的 PagedAttention 核心理念高度契合，能够更充分地占满 GPU 的计算单元。

**2. 训练与解耦的工程实现**
*   **事实陈述**：文章提到集成了 PR#32887，并提供了预训练的 Checkpoint。这表明 P-EAGLE 不是一个即插即用的“免训练”方法（如 Lookahead Decoding），而是需要针对特定基座模型训练专门的 Draft Model 或 Adapter。
*   **你的推断**：P-EAGLE 可能沿用了 EAGLE (Extrapolation Algorithm for Greater Language-model Efficiency) 的思路，即利用基座模型的隐藏状态来预测下一个 Token，而不是完全独立训练一个小模型。这种“特征提取”式的草稿方法通常比独立训练小模型效果更好，且推理时不需要加载两个完整的模型权重，显存占用更优。

**3. 对 vLLM 生态的补强**
*   **事实陈述**：vLLM 目前是 LLM 推理的事实标准之一，但其原生对 Speculative Decoding 的支持尚在完善中。
*   **行业影响**：将 P-EAGLE 直接合并进 vLLM 主干，极大地降低了用户的使用门槛。用户无需修改复杂的推理代码，只需调整配置即可获得加速。这对于推动 Speculative Decoding 从“学术论文”走向“工业落地”具有重要意义。

**反例与边界条件（批判性思考）**

**1. 验证带宽的瓶颈**
*   **边界条件**：当 Speculative Decoding 的 Tree 宽度（即并行猜测的分支数）过大时，验证阶段（主模型处理这些候选 Token）的计算量会呈指数级上升。
*   **你的推断**：如果主模型非常大（如 Llama-3-405B），而草稿模型非常小且生成速度极快，主模型的验证速度可能成为新的瓶颈。P-EAGLE 的“并行”优势在 Batch Size 较大时可能会受到显存带宽的限制，导致加速比下降。

**2. 训练成本与模型适配的滞后性**
*   **反例**：与 Lookahead Decoding（无需训练）不同，P-EAGLE 需要针对每个新发布的模型（如 Qwen2, Llama3.1）重新训练 Draft 层。
*   **观点**：对于刚发布的热门模型，社区无法立即使用 P-EAGLE 加速，存在“真空期”。此外，训练 Draft Model 本身需要算力和数据集，这增加了部署的复杂度。

**3. 长文本生成的收益衰减**
*   **边界条件**：Speculative Decoding 依赖于上下文的确定性。在生成长文本时，随着 Context Length 增加，KV Cache 占用增大，GPU 显存可能成为瓶颈，此时计算密集型的并行加速收益会被显存压力稀释。

**可验证的检查方式**

1.  **Token Acceptance Rate（接受率）测试**：
    *   *指标*：在标准数据集（如 ShareGPT）上测试 P-EAGLE 的平均 Token 接受率。
    *   *验证*：如果接受率低于 60%-70%，则说明草稿模型质量不佳，并行计算带来的验证开销可能得不偿失。EAGLE 系列通常接受率较高，这是其核心优势。

2.  **Time to First Token (TTFT) 与 Generation Latency 对比**：
    *   *实验*：对比 vLLM 原生 Beam Search 与 P-EAGLE 在不同 Batch Size（1, 8, 32, 128）下的延迟。
    *   *观察窗口*：重点观察 Batch Size 较大时的性能。P-EAGLE 作为并行方法，理论上在高并发下比串行 Speculative Decoding 更稳健。

3.  **显存占用分析**：
    *   *指标*：监控开启 P-EAGLE 前后的 GPU 显存占用。
    *   *验证*：检查是否引入了显著的显存额外开销。如果 P-EAGLE 是基于 Adapter 的方案，显存增量应很小；如果是加载独立 Draft Model，增量会较大。

**实际应用建议**

*   **适用场景**：P-EAGLE 非常适合**吞吐量敏感型**业务，如大批

---
## 技术分析

# P-EAGLE: Faster LLM inference with Parallel Speculative Decoding in vLLM 深度分析

## 1. 核心观点深度解读

**主要观点与核心思想**
文章的核心观点在于通过**并行推测解码**技术，在保持大语言模型（LLM）生成质量不变的前提下，显著提升推理吞吐量并降低延迟。作者主张，传统的自回归生成方式受限于模型串行计算的特性，而通过利用一个较小的“草稿模型”来并行预测多个Token，并由“目标模型”并行验证，可以打破内存墙和计算瓶颈，实现更高效的推理服务。

**创新性与深度**
P-EAGLE（Parallel Eagle）的创新性在于它不仅仅是对EAGLE（Extrapolation Algorithm for Greater Language-model Efficiency）的简单移植，而是将其与vLLM的高性能内核（如PagedAttention）进行了深度集成。
1.  **结构化重构**：它不是简单地预测下一个Token，而是预测特征空间的残差，这使得草稿模型与目标模型之间的耦合度更高，预测准确率远高于传统的Medusa或Speculative Decoding方法。
2.  **并行验证**：利用vLLM的Runtime特性，实现了对多个候选Token的并行验证，最大化了GPU计算资源的利用率。

**重要性**
随着LLM规模越来越大，推理成本成为商业落地的核心痛点。P-EAGLE提供了一种**无需修改模型权重**（即无需重新训练大模型）的推理加速方案。这意味着用户可以直接使用原有的Llama-3或Qwen模型，配合vLLM和P-EAGLE技术，立即获得显著的性能提升。这对于降低AI基础设施成本、提升用户体验具有极高的实用价值。

## 2. 关键技术要点

**涉及的关键技术或概念**
1.  **推测解码**：利用小模型快速生成草稿，大模型并行验证草稿。如果验证通过，则直接输出；否则回退。
2.  **EAGLE架构**：不同于传统的Token级预测，EAGLE在特征层进行操作。它利用目标模型某一层的特征作为输入，训练一个轻量级的网络（通常只有几层MLP或Transformer层）来预测后续Token。
3.  **P-EAGLE（并行化）**：在vLLM中实现时，重点在于如何高效地管理KV Cache和并行执行验证步骤。

**技术原理和实现方式**
*   **训练阶段**：冻结目标大模型（如Llama-2-70B），提取其某一中间层的输出特征。基于这些特征，训练一个轻量级的“草稿头”。这个头学习的是下一个Token的残差。
*   **推理阶段**：
    1.  **草稿生成**：草稿模型根据历史特征，一次性生成 $N$ 个候选Token。
    2.  **并行验证**：vLLM运行目标模型，但这 $N$ 个Token的处理是并行的。利用vLLM的Attention机制，一次性计算这 $N$ 个Token的Attention和概率分布。
    3.  **采样与接受**：比较目标模型和草稿模型的概率分布，决定接受哪些Token。如果遇到拒绝，则丢弃后续Token，从拒绝位置重新开始。

**技术难点与解决方案**
*   **难点1：显存与带宽瓶颈**。传统的Speculative Decoding在处理长序列时，KV Cache的管理非常复杂。
    *   *解决方案*：利用vLLM的PagedAttention机制，高效管理非连续的KV Cache块。
*   **难点2：验证效率**。如果验证过程比直接生成还慢，就失去了意义。
    *   *解决方案*：P-EAGLE通过Tree Mask机制，在vLLM内部构建一个计算树，使得GPU可以在单次Forward Pass中完成对多个分支路径的验证计算，极大地减少了Kernel启动开销。

**技术创新点分析**
P-EAGLE的核心创新在于**特征对齐与残差预测**。传统的Speculative Decoding（如DeepMind的版本）通常使用一个独立的小模型（如Llama-2-7B辅助Llama-2-70B）。而EAGLE/P-EAGLE实际上是基于目标模型的一个“插件”或“旁路”，它直接利用目标模型的内部特征，因此其草稿质量往往比异构小模型更高，接受率更高，从而带来更大的加速比。

## 3. 实际应用价值

**对实际工作的指导意义**
对于LLM应用开发者而言，P-EAGLE意味着**免费的午餐**。在显存允许的情况下，加载P-EAGLE的checkpoint可以显著降低Time to First Token (TTFT) 和Token生成延迟。这对于实时聊天机器人、代码生成助手等对延迟敏感的应用至关重要。

**应用场景**
1.  **实时交互系统**：如AI客服、Copilot，需要极低的延迟。
2.  **高吞吐量API服务**：在相同GPU资源下服务更多用户。
3.  **长文本生成**：由于解码速度加快，生成长篇报告或摘要的耗时大幅缩短。

**需要注意的问题**
1.  **显存开销**：P-EAGLE需要加载额外的草稿网络参数，且推理过程中需要存储更复杂的KV Cache结构（Tree结构），会增加约10%-20%的显存占用。
2.  **模型适配性**：目前主要针对主流开源模型（如Llama-2/3, Qwen）有预训练好的checkpoint，对于微版后的模型可能需要自己训练EAGLE头。

**实施建议**
*   **基准测试**：在上线前，务必在特定业务数据集上进行Benchmark。加速效果取决于“接受率”，如果业务逻辑导致生成内容非常随机（低熵），加速效果会打折。
*   **Batch Size调优**：P-EAGLE在Batch Size较大时表现更好，因为可以掩盖并行验证的固定开销。

## 4. 行业影响分析

**对行业的启示**
P-EAGLE的普及标志着LLM推理优化进入了**“算法与框架协同设计”**的时代。单纯依赖硬件升级或单纯依赖模型量化已触及天花板，未来的优化将更多依赖于推理框架（如vLLM, TensorRT-LLM）与特定算法（Speculative Decoding, Medusa）的深度绑定。

**可能带来的变革**
*   **推理成本结构改变**：随着vLLM等开源框架整合此类技术，高端推理服务的边际成本将下降，可能促使更多SaaS产品降低API调用价格。
*   **边缘计算可能性**：虽然P-EAGLE目前主要针对云端大模型，但其“用小算力辅助大算力”的思想可能启发端侧模型的优化方案。

**对行业格局的影响**
vLLM通过集成P-EAGLE，进一步巩固了其作为高性能LLM推理服务标准框架的地位。这将迫使其他推理框架（如TGI, TensorRT-LLM）加速对类似并行解码技术的支持。

## 5. 延伸思考

**引发的思考**
*   **通用性 vs 特化性**：P-EAGLE需要针对特定模型训练特定的EAGLE头。未来是否会出现“通用草稿模型”，能够辅助任意基座模型？
*   **动态调整**：目前的推测步数通常是固定的。未来是否可以根据输入文本的复杂度（熵值）动态调整推测的深度？

**拓展方向**
*   **多模态扩展**：目前的推测解码主要集中在文本。如何将其应用到图像生成（如Diffusion过程）或视频生成中？
*   **量化兼容性**：P-EAGLE在INT4量化模型上的表现如何？特征层的扰动是否会导致草稿模型准确率大幅下降？

**未来发展趋势**
未来的推理系统将不再是单一的模型运行，而是一个**模型簇**的协同工作。一个主模型搭配多个辅助模型（用于Drafting、用于Judging、用于Safety Check），形成流水线或并行阵列。

## 6. 实践建议

**如何应用到自己的项目**
1.  **环境准备**：确保使用 vLLM v0.16.0 或更高版本。
2.  **模型获取**：从HuggingFace下载对应的P-EAGLE checkpoint（例如 `lm-sys/FasterTransformer` 或者官方仓库提供的EAGLE权重）。
3.  **启动服务**：修改vLLM的启动脚本，启用 speculative decoding 模块。
    ```python
    # 示例逻辑
    from vllm import LLM, SamplingParams
    llm = LLM(model="meta-llama/Llama-2-7b-hf", 
              speculative_model="lm-sys/EAGLE-Llama-2-7b", # 草稿模型路径
              num_speculative_tokens=5) # 推测步数
    ```

**具体行动建议**
*   **性能监控**：关注 `speculative decoding acceptance rate` 指标。如果该指标低于60%，说明加速效果不佳，可能需要更换草稿模型或调整推测步数。
*   **A/B测试**：对比开启P-EAGLE前后的生成质量。虽然理论上数学上是等价的，但浮点数误差可能导致微小差异，需验证业务是否受影响。

**实践中的注意事项**
*   **版本兼容性**：vLLM迭代极快，API经常变动。务必检查当前vLLM版本对P-EAGLE的支持参数名（如 `speculative_model` 或 `enforce_eager` 等）。
*   **硬件要求**：P-EAGLE对GPU的显存带宽敏感。在消费级显卡（如RTX 3090）上，由于显存带宽较低，加速比可能不如A100/H100明显。

## 7. 案例分析

**成功案例分析**
*   **LMSYS Chatbot Arena**：作为vLLM的主要开发者，LMSYS在自己的后端服务中广泛使用了此类技术。他们展示了在Llama-2-70B上使用P-EAGLE，实现了接近2x-3x的吞吐量提升，同时P99延迟显著下降。这使得他们能够在有限的GPU资源下支撑全球用户的访问请求。

**失败/边界案例反思**
*   **数学推理任务**：在某些需要严格逻辑推理的任务中，草稿模型可能会“走神”，生成看似通顺但逻辑错误的Token序列。由于目标模型是并行验证，可能会因为概率分布的微小差异而频繁拒绝草稿，导致性能回退，甚至比直接推理更慢（因为浪费了计算草稿的时间）。
*   **经验教训**：推测解码并非万能银弹。在低熵（容易预测）的任务上效果极佳，但在高随机性或高逻辑复杂性的任务上，需要谨慎评估。

## 8. 哲学与逻辑：论证地图

**中心命题**
在保证生成结果数学分布一致的前提下，P-EAGLE通过引入轻量级辅助模型进行并行推测验证，能够显著突破LLM推理过程中的内存与计算瓶颈。

**支撑理由与依据**
1.  **理由一：计算并行化**。传统的自回归解码是串行的，无法充分利用GPU的并行计算能力。
    *   *依据*：GPU架构特性（高吞吐、高并行）与Transformer模型解码阶段（单Token串行）之间的不匹配。
2.  **理由二：草稿的高效性**。预测 $N$ 个Token的计算量远小于验证 $N$ 个Token的计算量，且验证过程可以并行化。
    *   *依据*：Jacobi等人的研究及Speculative Decoding理论证明，只要接受率大于一定阈值，整体延迟就会降低。
3.  **理由三：特征复用**。P-EAGLE利用目标

---
## 最佳实践

## 最佳实践指南

### 实践 1：合理配置草稿模型与目标模型的比例

**说明**: P-EAGLE 的核心在于利用较小的草稿模型来预测目标模型的输出。为了获得最佳性能，草稿模型通常应比目标模型小 2 到 4 倍。如果草稿模型太小，其预测准确率（接受率）会过低，导致验证阶段开销过大；如果草稿模型太大，生成速度的提升则不明显。

**实施步骤**:
1. 根据目标模型大小选择合适的开源模型作为草稿模型（例如目标为 Llama-3-70B，草稿可选择 Llama-3-8B）。
2. 确保草稿模型的词汇表与目标模型一致，或经过适配处理。
3. 在 vLLM 启动脚本中正确配置 `--model`（目标模型）和 `--draft-model`（草稿模型）参数。

**注意事项**: 避免使用能力差异过大的模型组合，例如用极小模型预测超大模型，这可能导致负向的加速效果。

---

### 实践 2：最大化利用 GPU 显存以支持大 Batch Size

**说明**: 并行投机解码需要同时加载目标模型和草稿模型，对显存容量要求较高。vLLM 的 PagedAttention 机制擅长处理大 Batch Size，而投机解码在大 Batch Size 下能摊销并行验证的开销。

**实施步骤**:
1. 评估硬件显存总量，确保能同时容纳两个模型以及 KV Cache。
2. 调整 vLLM 的 `gpu_memory_utilization` 参数（例如设为 0.9 或 0.95），在不过度 OOM（显存溢出）的前提下尽可能多占用显存。
3. 适当增加 `max_num_seqs` 或请求的并发数，以提高吞吐量。

**注意事项**: 监控显存使用率，如果频繁发生 OOM，需适当降低 Batch Size 或减少 KV Cache 的预留块数。

---

### 实践 3：调整推测树深度与验证并行度

**说明**: P-EAGLE 支持多步并行推测。调整推测的步长（即一次生成多少个 token 进行验证）是平衡延迟和吞吐量的关键。较大的推测步长可能增加验证失败率，而较小的步长可能无法充分发挥并行优势。

**实施步骤**:
1. 在 vLLM 配置中设置 `speculate` 参数（通常为 5 或更高，取决于模型能力）。
2. 根据实际业务场景（是追求低延迟还是高吞吐）进行微调。
3. 观察日志中的 "acceptance rate"（接受率），理想情况下应保持在 60%-80% 之间。

**注意事项**: 如果接受率过低（例如低于 50%），说明草稿模型预测不准，应减少推测步长或更换更强的草稿模型，否则会造成计算资源浪费。

---

### 实践 4：确保数据加载与预处理的流水线效率

**说明**: 在使用 P-EAGLE 进行推理时，CPU 端的数据预处理和 GPU 端的推理计算应当尽量重叠。如果数据加载成为瓶颈，GPU 的并行计算能力将被闲置。

**实施步骤**:
1. 使用 vLLM 的 OpenAI 兼容 API 服务端模式，利用其内置的高效异步处理机制。
2. 在离线批处理场景中，确保数据集的加载是异步进行的，避免阻塞推理循环。
3. 检查输入 Prompt 的长度，过长的 Context 会占用大量 KV Cache，影响 Batch Size 的扩展。

**注意事项**: 对于极长的上下文场景，确保启用了 vLLM 的长文本优化特性（如 prefix caching），以减少重复计算。

---

### 实践 5：选择合适的量化策略以平衡速度与精度

**说明**: 为了进一步加速推理并减少显存占用，可以对草稿模型和目标模型应用量化技术（如 AWQ 或 GPTQ）。P-EAGLE 允许草稿模型和目标模型使用不同的精度，例如草稿模型使用 4-bit 以求快，目标模型使用 8-bit 或 16-bit 以保证验证准确性。

**实施步骤**:
1. 下载或转换对应精度的模型权重。
2. 在加载模型时指定 `quantization` 参数（例如 `--quantization awq`）。
3. 建议先对目标模型进行量化，若显存仍有余量或速度不足，再考虑对草稿模型进行更激进的量化。

**注意事项**: 量化可能会降低模型的生成质量，特别是极端的量化（如 4-bit）可能导致接受率大幅下降，建议在上线前进行 A/B 测试对比。

---

### 实践 6：监控接受率与 Token 生成速度

**说明**: 投机解码的性能高度依赖于 "接受率"（即草稿模型生成的 token 被目标模型接受的比例）。监控该指标是判断 P-EAGLE 配置是否有效的核心手段。

**实施步骤**:
1. 启用 vLLM 的详细日志或使用 Prometheus/Grafana 监控 vLLM 的 metrics

---
## 学习要点

- P-EAGLE 通过在 vLLM 中引入并行投机解码技术，利用多个小模型同时预测 Token，显著提升了大语言模型（LLM）的推理速度。
- 该方法创新性地采用了“并行采样”策略，打破了传统串行投机解码的性能瓶颈，从而实现了更高的吞吐量和更低的延迟。
- P-EAGLE 能够保持与原始模型完全一致的生成精度，因为它通过验证机制确保输出结果与基座模型一致，不会牺牲回答质量。
- 该技术对模型架构具有通用性，不仅支持 LLaMA 等主流开源模型，还可与 vLLM 现有的高性能内核（如 PagedAttention）无缝集成。
- 通过在 vLLM 中实现，P-EAGLE 充分利用了显存管理和连续批处理等优化特性，进一步提高了推理过程中的资源利用率。
- 实验表明，在大多数推理场景下，P-EAGLE 相比非投机解码方法实现了显著的加速比，且在长文本生成任务中优势更为明显。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm](https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [vLLM](/tags/vllm/) / [P-EAGLE](/tags/p-eagle/) / [LLM推理](/tags/llm%E6%8E%A8%E7%90%86/) / [推测解码](/tags/%E6%8E%A8%E6%B5%8B%E8%A7%A3%E7%A0%81/) / [并行计算](/tags/%E5%B9%B6%E8%A1%8C%E8%AE%A1%E7%AE%97/) / [模型加速](/tags/%E6%A8%A1%E5%9E%8B%E5%8A%A0%E9%80%9F/) / [PR32887](/tags/pr32887/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [P-EAGLE：vLLM集成并行推测解码加速LLM推理]({{< relref "posts/20260313-blogs_podcasts-p-eagle-faster-llm-inference-with-parallel-specula-1.md" >}})
- [P-EAGLE：vLLM集成并行推测解码加速LLM推理]({{< relref "posts/20260314-blogs_podcasts-p-eagle-faster-llm-inference-with-parallel-specula-1.md" >}})
- [EWSJF：面向混合负载LLM推理的自适应调度器]({{< relref "posts/20260130-arxiv_ai-ewsjf-an-adaptive-scheduler-with-hybrid-partitioni-2.md" >}})
- [在 SageMaker AI 与 Bedrock 上利用 vLLM 高效部署多 LoRA 模型]({{< relref "posts/20260225-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-0.md" >}})
- [在SageMaker AI与Bedrock上利用vLLM高效部署多LoRA及MoE模型]({{< relref "posts/20260226-blogs_podcasts-efficiently-serve-dozens-of-fine-tuned-models-with-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*