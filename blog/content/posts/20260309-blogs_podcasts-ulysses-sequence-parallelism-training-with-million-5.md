---
title: Ulysses序列并行：支持百万Token上下文训练
date: 2026-03-09 20:11:31+08:00
draft: false
entry_kind: auto
tags:
- Ulysses
- 序列并行
- 长上下文
- 分布式训练
- LLM
- Megatron
- 显存优化
- 注意力机制
categories:
- 大模型
- 系统与基础设施
source: blogs_podcasts
description: 随着大模型对上下文长度的需求日益增长，如何在有限的显存资源下高效完成百万级 token 的训练成为了一个关键挑战。本文深入解析 Ulysses
  提出的序列并行策略，探讨其如何通过优化注意力机制的通信开销来突破长序列训练的瓶颈。通过阅读本文，读者将掌握该技术的核心原理，并了解如何将其应用于构建超长上下文的大规模模型。
external_url: https://huggingface.co/blog/ulysses-sp
scenarios:
- 大语言模型
aliases:
- /posts/20260309-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-7/
- /posts/20260310-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-10/
- /posts/20260310-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-12/
- /posts/20260310-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-7/
- /posts/20260310-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-8/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# Ulysses序列并行：支持百万Token上下文训练

---

## 基本信息

- **来源**: Hugging Face Blog (blog)
- **发布时间**: 2026-03-09T00:00:00+00:00
- **链接**: [https://huggingface.co/blog/ulysses-sp](https://huggingface.co/blog/ulysses-sp)

---

## 导语

随着大模型对上下文长度的需求日益增长，如何在有限的显存资源下高效完成百万级 token 的训练成为了一个关键挑战。本文深入解析 Ulysses 提出的序列并行策略，探讨其如何通过优化注意力机制的通信开销来突破长序列训练的瓶颈。通过阅读本文，读者将掌握该技术的核心原理，并了解如何将其应用于构建超长上下文的大规模模型。

---

## 评论

**文章中心观点**
Ulysses 提出了一种通过在序列维度进行分布式切分并结合显存高效的 All-Gather 通信策略，从而在几乎不牺牲计算效率的前提下，将大语言模型（LLM）的有效训练上下文长度从数万突破至百万级别的系统级解决方案。

**支撑理由与边界条件分析**

1.  **通信与计算的重叠掩盖了长序列通信瓶颈**
    *   **事实陈述**：Ulysses 的核心技术在于将序列并行与数据并行（DP）或张量并行（TP）结合。它将长序列切分到不同 GPU 上计算 Attention，仅在计算 Attention 矩阵时进行 All-Gather 通信。
    *   **你的推断**：该方案之所以在长序列下高效，是因为长序列的计算量随序列长度呈平方级增长（$O(N^2)$），而通信量仅呈线性增长（$O(N)$）。在超长序列（100万+ token）场景下，计算时间远大于通信时间，从而使得通信开销几乎被计算掩盖，这是其能够保持线性扩展效率的关键数学基础。

2.  **上下文并行（CP）与张量并行（TP）的互补性**
    *   **事实陈述**：实验数据显示，当上下文长度达到 128k 或 1M 时，TP 的效率会显著下降（因为 TP 需要在层间频繁通信，且显存墙限制了 Batch Size），而 Ulysses 引入的 CP 维度正好缓解了这一压力。
    *   **作者观点**：文章认为将 CP 与 TP 结合（Hybrid Parallelism）是训练超长模型的最优解，既利用了 TP 的高带宽利用率，又利用了 CP 的低通信频率特性。

3.  **对 FlashAttention 的深度集成**
    *   **事实陈述**：Ulysses 并非独立存在，它高度依赖 FlashAttention 进行前向和反向的分块计算。通过在分布式环境下协同 FlashAttention，它解决了传统序列并行中显存碎片化严重的问题。

**反例/边界条件：**

1.  **短序列与高通信带宽场景下的不经济性**
    *   **你的推断**：如果模型训练的上下文长度较短（例如 4k-32k），计算时间无法掩盖通信时间，此时 Ulysses 频繁的 All-Gather 操作反而可能导致通信瓶颈，其性能可能不如传统的 Tensor Parallelism 或 Pipeline Parallelism。

2.  **推理阶段的吞吐量限制**
    *   **事实陈述**：Ulysses 极大地优化了训练吞吐量，但在自回归推理阶段，由于每生一个 token 都需要进行一次全局 All-Gather 来计算历史 Attention，这会带来巨大的延迟。因此，Ulysses 主要适用于训练微调阶段，而非直接服务于实时推理场景。

3.  **MoE 架构下的复杂性**
    *   **你的推断**：当结合混合专家模型时，序列并行与专家路由的动态负载均衡之间存在潜在的冲突。MoE 需要全局的 Token 分发，而 Ulysses 试图将 Token 固定在特定卡上计算 Attention，这两者在底层通信调度上可能产生非预期的干涉。

**多维度深入评价**

1.  **内容深度与严谨性**
    文章在系统设计层面展现了极高的严谨性。它没有停留在算法理论层面，而是深入到了 CUDA 算子和通信原语的优化。特别是对“计算-通信比”的分析非常扎实，指出了为什么 Ring Attention 在极长序列下依然不如 All-Gather 策略的原因（带宽利用率问题）。论证过程结合了 Megatron-LM 的框架，工程落地性很强。

2.  **实用价值**
    对于从事 LLM 训练基础设施研发的团队，这篇文章具有极高的参考价值。它直接解决了 Long-Context LLM 训练中“显存不够”和“算力利用率低”的两大痛点。对于需要处理长文本摘要、法律文档分析或代码库理解的行业应用，Ulysses 提供了一条可行的工程路径。

3.  **创新性**
    Ulysses 的创新性不在于提出了全新的 Attention 算法，而在于**并行策略的组合创新**。它巧妙地重新定义了 Attention 计算的通信时机，证明了在特定约束下，All-Gather 的通信成本是可以接受的。它打破了“序列越长，分布式效率越低”的传统认知。

4.  **行业影响**
    该技术可能会成为未来 Long-Context 基座模型训练的标准配置。它推动了行业从“模型参数规模竞赛”向“上下文长度竞赛”的范式转移。随着开源框架（如 Megatron-Core, DeepSpeed）逐步集成 Ulysses，中小型 AI Lab 也能低成本地进行百万级上下文的模型微调，这会加速长场景应用的爆发。

5.  **争议点与不同观点**
    *   **KV Cache 的存储瓶颈**：文章主要优化了训练时的显存，但在推理时，百万级 Token 的 KV Cache 存储依然是巨大的挑战。Ulysses 并没有解决推理时的 KV Cache 显存占用问题，这可能导致模型虽然能训练出来，但难以低成本部署。
    *   **收敛性问题**：虽然数学上等价，但在极端的分布式切分下（如切分到几十张卡），数值精度损失（FP16/BF16 累积误差）是否会影响模型在超长序列上的收敛稳定性，仍需更多实证数据。

**实际应用建议**

1.  **适用场景判断**：仅在 Context Length 超

---

## 技术分析

### 1. 核心观点深度解读

**主要观点**
文章的核心主张是提出 **Ulysses**，一种针对超长上下文大语言模型训练的序列并行策略。该策略旨在解决传统显存架构无法支撑百万级 Token 上下文训练的瓶颈。其核心论点在于：**通过在数据并行组内对序列维度进行切分，并利用注意力机制的分块计算特性，使得模型能够以线性的计算成本和恒定的通信量处理任意长度的上下文。**

**核心思想**
作者传达的深层思想是“**解耦序列长度与单卡显存的硬性绑定**”。在标准的 Transformer 架构中，注意力机制的显存占用随序列长度呈平方级增长（$O(N^2)$），这直接限制了单卡能处理的最大长度。Ulysses 的突破性思维在于：既然注意力计算在数学上可以分块进行，那么就可以将长序列拆解到多个 GPU 上，让每个 GPU 仅计算局部的注意力分数，最后通过极低开销的通信汇总结果。这种“分治法”打破了物理硬件对逻辑上下文的限制。

**创新性与深度**
该技术的创新性在于它重新定义了长序列训练的“不可能三角”，即在**超长序列、高训练吞吐量和低显存占用**三者之间找到了最佳平衡点。与 Ring Attention 等其他序列并行方案相比，Ulysses 的技术深度体现在**其对现有计算框架的侵入性极小**。它不需要重写底层的 CUDA 算子（如 PagedAttention），而是通过巧妙组合 All-Gather 和 Reduce-Scatter 等标准通信原语，实现了对长上下文的无缝支持。

**重要性**
随着大模型应用向长篇小说分析、代码库全文检索乃至基因组数据处理等场景演进，支持百万级 Token 上下文已成为通往 AGI 的关键能力。Ulysses 提供了一种可扩展的工程范式，证明了在有限硬件资源下，通过纯粹的算法优化和通信策略调整，即可实现数量级的上下文长度扩展。

### 2. 关键技术要点

**涉及的关键技术**
1.  **序列并行**：一种不同于张量并行或数据并行的并行策略，它将输入序列按时间步切分到不同的 GPU 上。
2.  **分布式注意力机制**：利用 FlashAttention 的分块计算特性，在分布式环境下计算 $Q \times K^T$，每个 GPU 仅持有部分序列的 Query 和完整的 Key/Value（在特定计算阶段）。
3.  **通信原语组合**：核心依赖于 **All-Gather**（收集全局 K/V）和 **Reduce-Scatter**（聚合局部结果）操作。

**技术原理与实现**
假设集群中有 $P$ 张 GPU，输入序列长度为 $L$。
1.  **序列切分**：输入序列沿时间维度被切分为 $P$ 个子块，每个 GPU 分得 $L/P$ 的 Token。
2.  **局部投影**：每个 GPU 独立计算自己子块的 Query ($Q$), Key ($K$), Value ($V$) 矩阵。
3.  **通信与计算**：
    *   **All-Gather K/V**：为了计算注意力，每个 GPU 需要获取全局的上下文信息。通过 All-Gather 操作，所有 GPU 交换各自的 $K$ 和 $V$，使得每个 GPU 都拥有完整的 $K$ 和 $V$。
    *   **局部 Attention 计算**：每个 GPU 用本地的 $Q$ 与全局聚合后的 $K, V$ 进行注意力计算，得到局部的输出块。
    *   **Reduce-Scatter**：各 GPU 计算出的输出块通过 Reduce-Scatter 操作进行求和，并将最终结果切分回各个 GPU，作为下一层的输入。
4.  **计算与通信重叠**：为了最大化效率，Ulysses 尝试将通信操作与注意力计算在时间轴上重叠，以隐藏通信延迟。

**技术难点与解决方案**
*   **难点**：通信带宽压力。在超长序列下，频繁的 All-Gather 操作可能导致显存和带宽瓶颈。
*   **解决方案**：Ulysses 的设计优势在于其通信量仅与序列长度 $L$ 成正比（$O(L)$），而与模型隐层维度 $d_{model}$ 无关。相比之下，Ring Attention 的通信量与 $d_{model}$ 成正比。在超长上下文（$L$ 极大）且模型参数量固定的场景下，Ulysses 的通信效率显著优于 Ring Attention。

**技术创新点**
Ulysses 证明了在序列维度进行并行化时，**上下文窗口的扩展不再受限于单卡显存，而是受限于集群的规模**。它提出了一种特定的通信拓扑结构，使得在处理百万级 Token 时，通信开销在工程可接受范围内，从而实现了从“十万级”到“百万级”Token 上下文的跨越。

### 3. 实际应用价值

**对实际工作的指导意义**
Ulysses 为 AI 工程师和研究员提供了一种在现有硬件条件下训练超长上下文模型的切实可行的路径。它意味着企业无需采购定制化的超大显存硬件，通过现有的 GPU 集群和合理的并行策略，即可实现对长文本场景的有效支持。

**适用场景**
*   **超长文档理解**：如整本书籍的阅读摘要、长篇财报分析。
*   **代码库分析**：对整个大型项目的代码库进行上下文感知的补全或重构。
*   **DNA 序列分析**：处理生物信息学中极长的基因序列数据。

**局限性**
Ulysses 的性能高度依赖于集群的通信带宽。在带宽较低的集群（如以太网连接）上，All-Gather 操作可能成为瓶颈，导致训练吞吐量下降。此外，它通常需要较大的 Batch Size 来保证通信效率，这在某些小 Batch Size 训练场景下可能受限。

---

## 最佳实践


### 实践 1：精准的序列长度与并行度配置

**说明**:
Ulysses 的核心优势在于处理超长序列，但其通信开销与序列并行度（SP Degree）的平方成正比。盲目增加并行度会导致通信延迟超过计算收益。最佳实践是根据硬件带宽和目标序列长度进行数学建模，找到通信与计算的最佳平衡点。

**实施步骤**:
1. 评估集群的节点间带宽（NVLink 或 InfiniBand）。
2. 根据目标序列长度（如 1M tokens）计算每个 GPU 分片后的显存占用。
3. 设定并行度，通常建议 $SP\_Degree \le 8$，除非网络环境极佳。
4. 进行小规模基准测试，逐步增加并行度直到训练吞吐量不再增长。

**注意事项**:
在低带宽互联环境下（如以太网），应优先降低序列并行度，转而结合张量并行（TP）或流水线并行（PP）来利用显存。

---

### 实践 2：环形通信拓扑优化

**说明**:
Ulysses 依赖 All-to-All 的通信集合操作。在物理连接上，确保参与序列并行的 GPU 在物理拓扑上尽可能靠近，可以显著降低 Attention 计算前后的通信延迟。

**实施步骤**:
1. 使用 `nccl-topology` 或类似工具检测物理连接结构。
2. 在启动脚本中指定 `NCCL_SOCKET_IFNAME` 或使用 PyTorch 的 `process_group` 配置。
3. 强制序列并行的进程组仅在同一物理服务器内或通过 NVLink/NVSwitch 连接的 GPU 间建立。
4. 验证通信带宽利用率是否接近硬件峰值。

**注意事项**:
跨节点序列并行通常是性能杀手。如果必须跨节点，请确保网络配置支持 GPUDirect RDMA（GDR）。

---

### 实践 3：显存高效的注意力机制实现

**说明**:
虽然 Ulysses 分割了序列维度，但在处理百万级上下文时，KV Cache 的显存占用依然巨大。必须结合 FlashAttention v2 或 v3 的分块计算特性，确保在计算 Attention 时不会发生显存溢出（OOM）。

**实施步骤**:
1. 确认训练框架（如 Megatron-LM 或 DeepSpeed）已集成 FlashAttention。
2. 在代码层面启用 `use_flash_attn` 标志。
3. 调整 Attention 的 Block Size，以适配分片后的序列长度。
4. 监控显存峰值，确保 KV Cache 在分片后能装入 HBM。

**注意事项**:
部分旧版 GPU 架构（如 Turing）不支持 FlashAttention 的核心指令，运行效率会大幅下降，建议在 Ampere 及以上架构运行。

---

### 实践 4：动态填充与序列打包策略

**说明**:
在超长上下文训练中，传统的 Padding 策略会导致大量无效计算（计算 Padding 部分的 Attention）。最佳实践是使用序列打包技术，将多个较短的样本拼接成一个长序列，或使用动态 Padding 仅 Pad 至 Batch 内的最大长度。

**实施步骤**:
1. 在数据预处理阶段，将多个短文档拼接并添加分隔符，接近最大序列长度（如 128k 或 1M）。
2. 使用 `attention_mask` 标记有效 Token 与填充 Token。
3. 确保框架支持“打包”后的反向传播，即梯度计算仅作用于有效 Token。
4. 验证 Loss 计算是否正确排除了 Padding 部分。

**注意事项**:
拼接样本时要注意上下文边界，避免模型学习到跨文档的错误关联，通常需要在文档间插入特殊的 `<eos>` 或分隔符。

---

### 实践 5：梯度检查点与激活重计算

**说明**:
对于百万级 Token 的上下文，前向传播产生的激活值即便在序列并行下也相当巨大。为了节省显存用于更大的 Batch Size 或更长的序列，必须实施选择性激活重计算。

**实施步骤**:
1. 在 Transformer 层的 MLP 或 Attention 模块中启用 Checkpointing。
2. 仅对显存占用最大的算子（如 Attention 的 QK^T 计算）开启重计算，平衡计算时间与显存。
3. 调整 `checkpoint_segments` 参数，确保重计算不会导致训练速度下降超过 15%。
4. 监控 GPU 的 SM（流多处理器）利用率，确保计算单元未被闲置。

**注意事项**:
全量重计算（即重算所有层）会导致训练速度减半，建议采用“分段重计算”或仅对特定层（如每隔 N 层）进行重计算。

---

### 实践 6：长上下文特定的学习率调整

**说明**:
长上下文训练比短上下文更容易导致梯度不稳定或 Loss 尖峰，因为 Attention 的范围极广。标准的学习率调度器可能无法直接适用。

---

## 学习要点

- Ulysses 通过将长序列切分到多个 GPU 上进行并行计算，突破了单卡显存限制，实现了百万级 Token 上下文的高效训练。
- 该方法仅在注意力机制的序列维度上进行切分，保持了模型张量并行和流水线并行的原有结构，易于集成到现有分布式训练框架中。
- 通过仅在通信量最小的注意力层进行数据交互，Ulysses 极大降低了长序列训练中的通信开销，显著提升了计算效率。
- 该技术完美兼容 FlashAttention 等显存优化机制，在超长上下文场景下能维持极高的计算吞吐量和 MFU（模型算力利用率）。
- Ulysses 有效解决了长序列训练中的显存墙和通信墙问题，为构建支持无限上下文窗口的大语言模型提供了可扩展的解决方案。

---

## 引用

- **文章/节目**: [https://huggingface.co/blog/ulysses-sp](https://huggingface.co/blog/ulysses-sp)
- **RSS 源**: [https://huggingface.co/blog/feed.xml](https://huggingface.co/blog/feed.xml)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Ulysses](/tags/ulysses/) / [序列并行](/tags/%E5%BA%8F%E5%88%97%E5%B9%B6%E8%A1%8C/) / [长上下文](/tags/%E9%95%BF%E4%B8%8A%E4%B8%8B%E6%96%87/) / [分布式训练](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E8%AE%AD%E7%BB%83/) / [LLM](/tags/llm/) / [Megatron](/tags/megatron/) / [显存优化](/tags/%E6%98%BE%E5%AD%98%E4%BC%98%E5%8C%96/) / [注意力机制](/tags/%E6%B3%A8%E6%84%8F%E5%8A%9B%E6%9C%BA%E5%88%B6/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Ulysses序列并行技术实现百万Token上下文训练]({{< relref "posts/20260309-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-5.md" >}})
- [基于注意力匹配机制实现快速KV压缩]({{< relref "posts/20260220-hacker_news-fast-kv-compaction-via-attention-matching-19.md" >}})
- [基于对称感知泰勒近似实现恒定Token成本注意力机制]({{< relref "posts/20260204-hacker_news-attention-at-constant-cost-per-token-via-symmetry--0.md" >}})
- [基于对称性泰勒近似实现恒定Token成本注意力机制]({{< relref "posts/20260204-hacker_news-attention-at-constant-cost-per-token-via-symmetry--0.md" >}})
- [对称感知泰勒近似实现恒定Token成本注意力机制]({{< relref "posts/20260204-hacker_news-attention-at-constant-cost-per-token-via-symmetry--0.md" >}})
