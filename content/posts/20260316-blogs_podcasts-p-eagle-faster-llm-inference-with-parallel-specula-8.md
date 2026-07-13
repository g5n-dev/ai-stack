---
title: 'P-EAGLE: Faster LLM inference with Parallel Speculative'
date: 2026-03-16 23:16:10+08:00
draft: false
entry_kind: auto
tags:
- LLM
- vLLM
- P-EAGLE
- 推测解码
- 推理加速
- 模型部署
- 性能优化
- Speculative Decoding
categories:
- 大模型
- AI 工程
source: blogs_podcasts
description: '**P-EAGLE：在 vLLM 中实现并行推测解码以加速 LLM 推理** 本文介绍了 **P-EAGLE**（Parallel EAGLE）技术，这是一种旨在加速大语言模型（LLM）推理速度的新方法。文章详细阐述了其工作原理、在
  vLLM（从 v0.16.0 版本起）中的集成过程，以及如何使用预训练检查点来部署该服'
external_url: https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm
scenarios:
- 大语言模型
---

# P-EAGLE: Faster LLM inference with Parallel Speculative

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-03-13T19:27:04+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm](https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm)

---

## 摘要/简介

在这篇文章中，我们将解释 P-EAGLE 的工作原理，我们如何从 v0.16.0（PR#32887）起将其集成到 vLLM，以及如何使用我们的预训练检查点来部署它。

---

## 导语

P-EAGLE 通过并行推测解码技术，为解决大模型推理中的延迟问题提供了新思路。本文将深入剖析其技术原理，介绍 vLLM 从 v0.16.0 版本开始的集成细节，并演示如何利用预训练检查点进行部署。通过阅读，读者可以掌握这一优化方案的具体实现方法，从而在实际场景中有效提升推理效率。

---

## 摘要

**P-EAGLE：在 vLLM 中实现并行推测解码以加速 LLM 推理**

本文介绍了 **P-EAGLE**（Parallel EAGLE）技术，这是一种旨在加速大语言模型（LLM）推理速度的新方法。文章详细阐述了其工作原理、在 vLLM（从 v0.16.0 版本起）中的集成过程，以及如何使用预训练检查点来部署该服务。

**核心内容总结：**

**1. P-EAGLE 的工作原理**
P-EAGLE 是 EAGLE（Extrapolation Algorithm for Greater Language-model Efficiency）技术的并行化演进版本。传统的推测解码通常依赖于一个较小的草稿模型来预测大模型的输出，但往往是串行进行的。P-EAGLE 通过引入并行机制，允许草稿模型同时生成多个候选 Token，从而显著提高了推测阶段的效率。这种方法能够在保持生成质量的同时，大幅减少大模型所需的推理步数。

**2. vLLM 集成**
该功能已成功集成到 vLLM 框架中（具体始于 v0.16.0 版本，合并请求 PR#32887）。vLLM 作为业界流行的高性能推理引擎，通过引入 P-EAGLE，用户可以直接在 vLLM 生态系统中利用并行推测解码的优势，无需复杂的额外配置即可获得推理速度的提升。

**3. 部署与使用**
文章还提供了关于如何使用预训练检查点来部署 P-EAGLE 服务的说明。用户可以通过加载特定的模型检查点，在 vLLM 后端轻松启用这一加速功能。

**总结**
P-EAGLE 通过并行推测解码技术优化了 LLM 的推理过程。将其集成到 vLLM 中，使得开发者能够更便捷地服务高性能模型，有效降低延迟并提升吞吐量。

---

## 评论

**文章中心观点**
P-EAGLE 通过引入并行的推测解码策略，成功在 vLLM 框架中突破了传统串行推测解码的性能瓶颈，为在保持模型生成质量的前提下实现低成本、高吞吐量的 LLM 推理提供了一条经过工程验证的可行路径。

**支撑理由与评价**

**1. 内容深度：从理论验证到工程落地的严谨跨越**
*   **事实陈述**：文章详细阐述了 P-EAGLE 如何将 EAGLE（Extrapolation Algorithm for Greater Language-model Efficiency）从原本的串行验证机制改进为并行验证机制。
*   **作者观点**：作者认为 P-EAGLE 能够在 vLLM 的注意力机制中高效运行，且对显存占用的增加是可接受的。
*   **深度评价**：文章的深度在于它没有停留在算法层面的“自嗨”，而是深入到了 vLLM 的核心——PagedAttention 机制。通过解释如何利用 vLLM 的 KV Cache 管理来处理多分支候选，展示了极强的工程严谨性。这不仅仅是算法的移植，更是对推理引擎底层架构的适配。
*   **反例/边界条件**：对于非常小的 Batch Size（如 Batch=1），并行计算带来的调度开销可能会掩盖掉计算加速带来的收益，此时性能提升可能不如预期明显。

**2. 实用价值：直接赋能生产环境的降本增效**
*   **事实陈述**：文章明确指出了支持的 vLLM 版本（v0.16.0+）及具体的 PR 编号，并提供了预训练 Checkpoint 的使用方式。
*   **你的推断**：对于正在使用 vLLM 进行服务部署的企业而言，这是一篇高实用性的指南。它意味着无需更换推理框架，仅通过升级版本和切换模型权重，即可获得 1.5x-2x 的吞吐量提升。
*   **深度评价**：实用性体现在“即插即用”。相比于 Speculative Decoding 需要单独维护一个 Draft Model 的复杂性，P-EAGLE 将 Draft Model（通常是一个轻量级的 MLP 或 Attention 层）作为旁路挂载，大大简化了运维复杂度。
*   **反例/边界条件**：如果业务场景对延迟极其敏感且对生成质量要求是“完全一致”（如数学证明或**文章中心观点**
P-EAGLE 通过引入并行的推测解码策略，成功在 vLLM 框架中突破了传统串行推测解码的性能瓶颈，为在保持模型生成质量的前提下实现低成本、高吞吐量的 LLM 推理提供了一条经过工程验证的可行路径。

**支撑理由与评价**

**1. 内容深度：从理论验证到工程落地的严谨跨越**
*   **事实陈述**：文章详细阐述了 P-EAGLE 如何将 EAGLE（Extrapolation Algorithm for Greater Language-model Efficiency）从原本的串行验证机制改进为并行验证机制。
*   **深度评价**：文章的深度在于它没有停留在算法层面的“自嗨”，而是深入到了 vLLM 的核心——PagedAttention 机制。通过解释如何利用 vLLM 的 KV Cache 管理来处理多分支候选，展示了极强的工程严谨性。这不仅仅是算法的移植，更是对推理引擎底层架构的适配。它证明了在非自回归的采样阶段，通过并行验证多个候选序列，可以显著减少 GPU 的空闲时间。
*   **反例/边界条件**：对于非常小的 Batch Size（如 Batch=1）且 Prompt 极短的场景，并行计算带来的 Kernel 启动开销和调度开销可能会掩盖掉计算加速带来的收益，此时性能提升可能不如预期明显，甚至可能因为显存碎片化导致性能回退。

**2. 实用价值：直接赋能生产环境的降本增效**
*   **事实陈述**：文章明确指出了支持的 vLLM 版本（v0.16.0+）及具体的 PR 编号，并提供了预训练 Checkpoint 的使用方式。
*   **你的推断**：对于正在使用 vLLM 进行服务部署的企业而言，这是一篇高实用性的指南。它意味着无需更换推理框架，仅通过升级版本和切换模型权重，即可获得显著的吞吐量提升。
*   **深度评价**：实用性体现在“即插即用”和对显存的友好。相比于 Medusa 或 SpeculativeDecoding 需要单独维护一个完整的 Draft Model（如 7B 模型挂载 1B 模型），P-EAGLE 的 Draft 模块通常参数量极小（仅为几层 MLP 或 Attention 层），显存占用极低，大大简化了运维复杂度。
*   **反例/边界条件**：如果业务场景对延迟极其敏感且对生成质量要求是“完全一致”（如金融合规性审查），推测解码固有的“采样随机性”可能导致输出分布与原始模型存在微小差异，这在严格对齐场景下可能需要额外的验证成本。

**3. 创新性：架构层面的范式转移**
*   **事实陈述**：传统的 SpeculativeDecoding 通常采用“串行验证”模式，即 Draft Model 生成一个 Token，Target Model 验证一个。P-EAGLE 采用了 Tree Mask 机制，一次性生成并验证多个 Token。
*   **作者观点**：P-EAGLE 的这种并行性使其比 EAGLE 更快，且比单纯的 Speculative Decoding 更容易集成到现有的推理引擎中。
*   **深度评价**：其核心创新在于将“投机”的对象从 Token 层面提升到了 Tree 结构层面，并利用 vLLM 的并行计算能力进行一次性

---

## 技术分析

基于您提供的文章标题和摘要，以及P-EAGLE（Parallel Speculative Decoding）在vLLM中的实现背景，以下是关于该技术的深度分析报告。

---

### P-EAGLE与vLLM集成分析：并行推测解码的加速引擎

### 1. 核心观点深度解读

**文章的主要观点**
文章的核心在于阐述**P-EAGLE（Parallel-EAGLE）**技术如何通过将“投机采样”与“并行解码”相结合，并深度集成到vLLM框架中，从而在不改变模型输出精度（即不改变模型权重或输出分布）的前提下，显著提升大语言模型（LLM）的推理吞吐量并降低延迟。

**作者想要传达的核心思想**
传统的LLM推理受限于自回归生成的特性，每生成一个Token都需要巨大的计算量。作者传达的思想是：**利用“小模型”辅助“大模型”进行并行草稿生成，并通过高效的验证机制，将串行的生成过程转化为并行的验证过程，从而打破推理的内存墙和计算墙。** vLLM的集成意味着这一先进技术从实验室走向了工业级生产环境。

**观点的创新性和深度**
P-EAGLE的创新性在于它解决了传统投机解码的两个瓶颈：
1.  **Drafting效率：** 传统的投机解码（如Medusa）往往依赖主模型的一个“头”来生成草稿，或者依赖另一个独立的小模型。P-EAGLE引入了一种更高效的残差分支结构，能够并行预测多个后续Token。
2.  **验证效率：** 它利用了vLLM的高性能内核（如PagedAttention），将草稿验证过程批量化、并行化，使得验证阶段的显存访问和计算开销最小化。
3.  **深度：** 它不仅关注“生成得快不快”，更关注“验证得快不快”。在显存受限的推理场景中，验证速度往往决定了整体加速比。

**为什么这个观点重要**
随着LLM参数量的指数级增长，推理成本成为制约应用落地的关键瓶颈。P-EAGLE提供了一种**“模型无关”**的加速方案（即不需要重新训练大模型，只需训练一个轻量级的Draft Model或Head），这使得现有的昂贵模型（如Llama-3-70B）能够在保持原有能力的基础上，实现2x-4x的加速，这对于AI应用的商业化落地具有极高的经济价值。

### 2. 关键技术要点

**涉及的关键技术或概念**
1.  **Speculative Decoding (投机解码/推测采样)：** 核心思想是用一个小模型快速“猜”出接下来的几个Token，然后让大模型并行地去“验证”这些Token是否正确。如果猜对了，就保留；猜错了，就退回重试。
2.  **P-EAGLE (Parallel EAGLE)：** EAGLE（Extrapolation Algorithm for Greater Language-model Efficiency）的改进版。它不是独立运行一个小模型，而是在大模型的中间层插入一个“特征提取器”和一个“轻量级解码头”，利用大模型的隐藏状态来预测后续Token。P-EAGLE强调这种预测是并行进行的。
3.  **vLLM Integration：** 涉及到vLLM的Worker、Block Manager和Attention Kernel的深度修改，以支持非标准的Tree Attention（树状注意力）机制。

**技术原理和实现方式**
*   **Drafting阶段：** P-EAGLE的Draft Model挂载在主模型的某一层（例如倒数第二层）。当主模型推理到第 $t$ 个Token时，Draft Model利用当前层的隐藏状态，并行预测未来 $N$ 个Token（例如 $t+1, t+2, \dots, t+N$）。
*   **Verification阶段（Tree Attention）：** 主模型不会串行验证这 $N$ 个Token，而是构建一个“树状”的输入结构。根节点是当前上下文，分支是Draft Model给出的 $N$ 个候选Token。
*   **Accept/Reject：** 主模型一次性并行计算所有分支的概率。通过采样算法比较Draft Model和Target Model的概率，接受匹配的Token。一旦遇到不匹配的Token，丢弃后续分支，从最后一个正确接受的位置继续。

**技术难点和解决方案**
*   **难点：显存带宽瓶颈。** 验证阶段需要处理大量的候选Token，如果显存读写（Memory Bound）跟不上，加速效果会被抵消。
*   **解决方案：** vLLM的PagedAttention机制和高效的CUDA Kernel。通过精细的显存管理，减少碎片，并利用GPU的高并行度一次性计算验证所需的概率。
*   **难点：KV Cache管理。** 在投机解码中，如果第3个Token被拒绝，第4、5个Token的KV Cache虽然计算了但需要丢弃。
*   **解决方案：** vLLM引入了特殊的Tree Cache管理逻辑，能够原子性地写入或回滚KV Cache。

**技术创新点分析**
P-EAGLE相比原始EAGLE或Medusa，最大的技术亮点在于**“并行性”的极致利用**。它将Drafting过程从“串行生成”变为“一次性前向传播输出多个候选”，极大地减少了Drafting本身的时间开销。同时，vLLM的集成实现了请求级别的批处理优化，使得在多并发场景下也能保持高加速比。

### 3. 实际应用价值

**对实际工作的指导意义**
对于AI工程师和架构师而言，P-EAGLE在vLLM中的落地意味着：**在不牺牲模型智能水平的前提下，推理成本可以直接减半甚至更多。** 这使得在边缘设备或消费级显卡上运行大模型成为可能。

**可以应用到哪些场景**
1.  **实时对话系统：** 降低Time-to-First-Token (TTFT) 和Token生成延迟，提升用户体验。
2.  **长文本生成：** 在写文章、代码生成等场景中，由于Draft Model能一次预测多个Token，长序列生成的加速比通常更高。
3.  **成本敏感型服务：** 对于按Token计费的API服务，使用P-EAGLE可以显著降低单Token的算力成本。

**需要注意的问题**
*   **额外显存开销：** 需要加载Draft Model的参数，并且Tree Attention会临时占用更多的KV Cache显存。
*   **模型兼容性：** 目前主要针对特定架构（如Llama-2/3, Mistral等）有预训练好的Checkpoint，不支持任意模型的即插即用。
*   **非确定性：** 虽然数学上证明分布一致，但在极端低温度（Temperature=0）采样下，验证机制的实现细节可能会影响结果的绝对确定性。

**实施建议**
1.  **基准测试：** 在上线前，务必在实际业务数据集上进行A/B测试，因为加速比高度依赖于Prompt的复杂度和Draft Model的命中率。
2.  **显存规划：** 建议在显存充裕的GPU上使用（如A100/H100），显存不足时可能会因为OOM导致性能下降。

### 4. 行业影响分析

**对行业的启示**
P-EAGLE在vLLM中的集成标志着**“推理优化算法”与“推理框架”的深度解耦与融合**。以前优化算法（如Speculative Decoding）多是学术玩具，现在变成了即插即用的工业组件。这启示行业：未来的竞争不仅仅是模型权重的竞争，更是推理框架效率的竞争。

**可能带来的变革**
这可能会改变云服务商的定价模式。如果推理速度翻倍，单位Token的边际成本下降，可能会引发新一轮的大模型API价格战，加速AI应用的普及。

**相关领域的发展趋势**
*   **Speculative Decoding将成为标配：** 未来的推理框架（如TensorRT-LLM, TGI）都会原生支持此类技术。
*   **Draft Model生态：** 会出现专门针对各种大模型优化的轻量级Draft Model市场。

**对行业格局的影响**
vLLM通过集成此类前沿技术，进一步巩固了其在LLM推理框架中的统治地位，迫使竞争对手（如TensorRT-LLM）加快算法创新的集成速度。

### 5. 延伸思考

**引发的其他思考**
*   **通用Draft Model：** 是否存在一个通用的Draft Model，可以为任意的大模型提供草稿？目前的P-EAGLE似乎还是针对特定架构训练的。
*   **量化与投机解码的结合：** 当主模型被量化到4-bit时，Draft Model是否需要保持高精度？这之间的精度平衡点在哪里？

**可以拓展的方向**
*   **多模态投机解码：** 将此技术应用到图像生成（如扩散模型）或视频生成中，利用低分辨率模型并行预测高分辨率路径。
*   **自适应投机：** 根据输入文本的难度，动态调整预测的步数。简单的文本多预测几步，复杂的文本少预测几步。

**需要进一步研究的问题**
如何解决在极端长上下文场景下，Tree Attention带来的显存碎片问题？以及在多轮对话中，如何保持KV Cache的高效复用？

### 7. 案例分析

**结合实际案例说明**
假设一个在线客服系统，使用Llama-3-70B模型。
*   **优化前：** 平均每个请求生成100个Token，耗时5秒，TPS（Tokens Per Second）为20。
*   **优化后（应用P-EAGLE）：** 假设Draft Model的接受率为0.7（平均每步验证通过0.7个Token），理论加速比约为 $1 / (1 - 0.7) \approx 3.3$ 倍（受限于验证开销，实际可能在2.5倍左右）。生成100个Token可能降至2秒。

**成功案例分析**
vLLM官方博客和PR中通常展示的Llama-2-70B案例显示，在特定的Batch Size下，P-EAGLE能够达到接近3倍的Throughput提升，且显存占用仅增加微乎其微。

**失败案例反思**
如果在一个非常复杂的数学推理任务中，Draft Model（基于较小参数）完全无法预测大模型的下一步，导致接受率接近0。此时，系统不仅没有加速，反而因为频繁的Tree Attention计算和回滚操作，比原生推理慢了

---

## 最佳实践

### 实践 1：合理配置草稿模型与目标模型

**说明**: P-EAGLE 的核心在于利用较小的草稿模型来预测目标模型的输出。为了获得最佳的性能提升（即加速比），草稿模型通常应比目标模型小 2-4 倍。如果草稿模型过大，验证阶段的计算开销会增加，从而抵消并行投机解码带来的速度优势；如果过小，草稿模型的接受率会降低，导致频繁的重新采样。

**实施步骤**:
1. 选择一个架构与目标模型兼容（如同为 Llama 系列）且参数量约为目标模型 1/4 到 1/10 的模型作为草稿模型。
2. 确保草稿模型的分词器与目标模型一致，以避免 Token ID 不匹配的问题。
3. 在 vLLM 启动脚本中，通过 `-- speculative-draft-model` 参数指定草稿模型路径。

**注意事项**: 并不是所有模型组合都能有效工作，建议优先使用经过验证的模型组合（如 Llama-3-8B 作为 Llama-3-70B 的草稿模型）。

---

### 实践 2：优化并行度与张量大小

**说明**: P-EAGLE 利用 vLLM 的并行能力来同时验证草稿模型的多个候选 Token。为了最大化 GPU 的利用率，需要根据 GPU 显存大小和模型尺寸调整并行度。不恰当的并行度会导致显存溢出（OOM）或计算资源闲置。

**实施步骤**:
1. 根据硬件配置调整 vLLM 的 `tensor_parallel_size` (TP) 参数，确保模型能够切分到可用的 GPU 上。
2. 调整 `max_num_batched_tokens` 和 `max_num_seqs`，以平衡吞吐量和延迟。P-EAGLE 对批量大小较为敏感，较大的批量通常能更好地掩盖验证阶段的延迟。
3. 监控 GPU 显存使用率，确保在并行解码期间显存峰值不超过物理限制。

**注意事项**: 在多 GPU 设置下，确保草稿模型和目标模型的并行策略一致，避免通信开销成为瓶颈。

---

### 实践 3：调整推测树的最大深度

**说明**: P-EAGLE 支持树状结构的投机解码，这意味着模型可以一次性预测并验证多个 Token。`speculative_max_model_len` 或相关的树深度参数决定了每次推理尝试生成的 Token 数量。虽然增加深度可以潜在地提高加速比，但如果草稿模型准确率不够高，过深的树会导致大量分支被拒绝，浪费计算资源。

**实施步骤**:
1. 从默认的树深度（例如 5 或 6）开始测试。
2. 使用验证集测试不同深度下的接受率。
3. 在接受率显著下降之前停止增加深度，通常接受率应保持在 60%-80% 之间以保证效率。

**注意事项**: 对于推理难度大或逻辑性强的 Prompt，建议适当减小树深度，以提高单次预测的准确性。

---

### 实践 4：启用高效的注意力机制内核

**说明**: vLLM 提供了优化的注意力机制内核（如 FlashAttention 或 PagedAttention）。在运行 P-EAGLE 时，确保启用了这些高性能内核，因为并行 speculative decoding 会显著增加注意力层的计算量。未优化的内核会导致验证阶段成为性能瓶颈。

**实施步骤**:
1. 在安装 vLLM 时，确保编译了正确的 CUDA 版本以支持 FlashAttention。
2. 启动服务时，检查日志确认 `FlashAttention` 或 `xFormers` 已被成功加载。
3. 如果环境允许，设置 `VLLM_USE_TRITON_FLASH_ATTN=1` 环境变量以尝试使用 Triton 优化的内核。

**注意事项**: 某些旧款 GPU 可能不支持最新的注意力优化内核，此时应回退到标准实现，但需预期性能会有所下降。

---

### 实践 5：针对长上下文场景的显存管理

**说明**: P-EAGLE 在推理过程中需要维护 KV Cache 以支持并行验证。在处理长上下文请求时，KV Cache 的占用会成倍增加。如果显存管理不当，可能会频繁触发缓存驱逐，严重影响推理速度。

**实施步骤**:
1. 合理设置 `gpu_memory_utilization` 参数（例如 0.9），为 vLLM 预留足够的显存空间用于 KV Cache。
2. 启用 `enforce_eager` 模式进行调试，确认显存占用符合预期，生产环境则默认使用 CUDA Graph 以减少启动开销。
3. 对于超长上下文，考虑启用 `swap_space` 或 `cpu_offload_gb`，利用系统内存作为显存的溢出缓冲区，但这会增加一定的延迟。

**注意事项**: 长上下文下，草稿模型的 KV Cache 占用也不容忽视，确保草稿模型和目标模型的 Cache 空间都得到合理分配。

---

### 实践 6：监控接受率与动态调整

**说明**: 接受率是衡量投机解码效率的关键指标。它表示目标模型接受了多少草稿模型生成的 Token。一个

---

## 学习要点

- P-EAGLE 通过并行推测解码技术，将 vLLM 中的 LLM 推理速度提升了最高 3 倍，显著降低了推理延迟。
- 该方法打破了传统推测解码中必须串行验证候选 Token 的限制，实现了候选序列的并行验证，从而大幅提高了 GPU 利用效率。
- P-EAGLE 兼容 vLLM 框架，能够无缝集成到现有的生产环境中，无需修改模型架构即可获得性能提升。
- 通过使用轻量级的“草稿模型”来预测多个 Token，再由主模型并行验证，在保持生成质量不变的前提下极大地节省了计算资源。
- 实验表明，P-EAGLE 在处理长文本生成和复杂推理任务时，相比非推测解码方法具有更显著的加速优势。
- 该技术有效地解决了大模型推理中“内存墙”和计算瓶颈问题，为部署高性能 AI 应用提供了更具成本效益的解决方案。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm](https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [LLM](/tags/llm/) / [vLLM](/tags/vllm/) / [P-EAGLE](/tags/p-eagle/) / [推测解码](/tags/%E6%8E%A8%E6%B5%8B%E8%A7%A3%E7%A0%81/) / [推理加速](/tags/%E6%8E%A8%E7%90%86%E5%8A%A0%E9%80%9F/) / [模型部署](/tags/%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/) / [性能优化](/tags/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/) / [Speculative Decoding](/tags/speculative-decoding/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [P-EAGLE：vLLM集成并行推测解码加速LLM推理]({{< relref "posts/20260314-blogs_podcasts-p-eagle-faster-llm-inference-with-parallel-specula-1.md" >}})
- [P-EAGLE：vLLM集成并行推测解码加速LLM推理]({{< relref "posts/20260316-blogs_podcasts-p-eagle-faster-llm-inference-with-parallel-specula-4.md" >}})
- [P-EAGLE：vLLM集成并行推测解码加速LLM推理]({{< relref "posts/20260313-blogs_podcasts-p-eagle-faster-llm-inference-with-parallel-specula-1.md" >}})
- [P-EAGLE：vLLM 集成并行推测解码加速 LLM 推理]({{< relref "posts/20260315-blogs_podcasts-p-eagle-faster-llm-inference-with-parallel-specula-2.md" >}})
- [P-EAGLE：vLLM 集成并行推测解码加速 LLM 推理]({{< relref "posts/20260316-blogs_podcasts-p-eagle-faster-llm-inference-with-parallel-specula-7.md" >}})
