---
title: Ulysses序列并行：实现百万级Token上下文训练
date: 2026-03-10 16:09:56+08:00
draft: false
entry_kind: auto
tags:
- Ulysses
- 序列并行
- 长上下文
- 分布式训练
- Megatron
- Attention
- 显存优化
- LLM
categories:
- 大模型
- 系统与基础设施
source: blogs_podcasts
description: 随着大语言模型对上下文长度的需求日益增长，如何在有限的计算资源下高效处理超长序列成为技术难点。本文深入探讨 Ulysses 提出的序列并行策略，解析其如何通过优化注意力机制的计算方式，实现百万级
  Token 上下文的稳定训练。通过阅读本文，读者将掌握该方案的核心架构设计，了解其在提升训练吞吐量与显存利用率方面的具体优势
external_url: https://huggingface.co/blog/ulysses-sp
scenarios:
- 大语言模型
---

# Ulysses序列并行：实现百万级Token上下文训练

---

## 基本信息

- **来源**: Hugging Face Blog (blog)
- **发布时间**: 2026-03-09T00:00:00+00:00
- **链接**: [https://huggingface.co/blog/ulysses-sp](https://huggingface.co/blog/ulysses-sp)

---

## 导语

随着大语言模型对上下文长度的需求日益增长，如何在有限的计算资源下高效处理超长序列成为技术难点。本文深入探讨 Ulysses 提出的序列并行策略，解析其如何通过优化注意力机制的计算方式，实现百万级 Token 上下文的稳定训练。通过阅读本文，读者将掌握该方案的核心架构设计，了解其在提升训练吞吐量与显存利用率方面的具体优势。

---

## 评论

**中心观点**
文章提出了一种名为 Ulysses 的序列并行（SP）策略，通过将超长序列切分至多个 GPU 进行独立注意力计算并配合通信重叠，旨在以极低的通信开销实现百万级 Token 上下文的高效训练，从而打破长上下文训练的显存与算力墙。

**支撑理由**

1.  **极致的通信效率（事实陈述）：**
    Ulysses 的核心优势在于其通信量随序列长度（$L$）增加而保持恒定，仅随并行度（$P$）线性增长。与 Ring Attention 需要随 $L$ 增加而增加的带宽密集型通信相比，Ulysses 在处理超长序列（如 1M Token）时，通信瓶颈显著降低。这使得在有限带宽的网络集群（如标准 InfiniBand 或甚至以太网）上进行超长上下文训练成为可能。

2.  **对现有训练栈的解耦与兼容（你的推断）：**
    文章暗示该方法可以与 4D 并行（数据+张量+流水线+序列）中的其他并行策略正交结合。特别是与张量并行（TP）配合时，Ulysses 处理序列维度，TP 处理隐藏层维度，两者互不干扰。这种模块化特性使得现有的 LLM 训练框架（如 Megatron-LM, DeepSpeed）可以在重构极少代码的情况下集成此技术，极大降低了工程落地门槛。

3.  **长上下文性能的线性扩展（事实陈述）：**
    实验数据显示，在 128k 到 1M token 的上下文窗口扩展中，Ulysses 能够维持近乎线性的扩展效率。相比 Ring Attention 在节点间通信时的延迟累积，Ulysses 的 All-Round 通信模式在特定拓扑下能更好地掩盖通信延迟，确保计算单元（GPU）的高利用率。

**反例与边界条件**

1.  **小 Batch Size 下的显存浪费（你的推断）：**
    Ulysses 要求序列长度 $L$ 必须能被并行度 $P$ 整除，且为了维持通信效率，通常要求 $L$ 较大。在微调场景中，如果 Batch Size 较小或序列较短（例如仅 32k 或 4k），强制使用高并行度的 Ulysses 会导致通信计算比（Computation-to-Communication Ratio, CCR）急剧恶化。此时，通信开销可能超过计算收益，导致训练速度反而下降。

2.  **Attention 算子的特定限制（事实陈述）：**
    该方法主要针对标准的 Multi-Head Attention (MHA) 或 Multi-Query Attention (MQA)。如果模型架构采用了非标准的 Attention 变体（如 FlashAttention 的某些特定局部窗口变体，或者极其复杂的稀疏 Attention），Ulysses 的通信切分策略可能需要重新设计，甚至无法应用，因为它依赖于完整的 Attention 矩阵计算。

**深入评价**

**1. 内容深度与论证严谨性**
文章在理论推导上较为扎实，准确指出了 Ring Attention 在超长序列下的带宽瓶颈。通过数学公式对比通信复杂度（Ulysses 为 $O(P)$ vs Ring 为 $O(L)$），论证逻辑清晰。然而，文章略去了对显存碎片管理的详细讨论。在处理 1M token 的 KV Cache 时，即便切分了序列，单卡显存依然面临巨大压力，若未配合高效的显存管理技术（如 vLLM 的 PagedAttention 或显存卸载），实际训练可能仍会 OOM（Out of Memory）。

**2. 实用价值与创新性**
Ulysses 的实用价值极高，它解决了“长上下文训练成本过高”的行业痛点。在 RAG（检索增强生成）和 Long-context Agent 领域，模型能否支持 1M 上下文是关键指标。其创新性不在于发明新的 Attention 算法，而在于**通信策略的工程化创新**：它将序列维度的依赖关系从“环状依赖”转变为“集合通信依赖”，巧妙地利用了现有的高性能通信库（如 NCCL）。这使得它比 Ring Attention 更容易部署在异构或网络环境较差的集群中。

**3. 行业影响与争议**
该技术可能会成为 Long-Context LLM 训练的标准配置。争议点在于“静态切分”的灵活性。实际业务中，输入序列长度往往变化剧烈（Padding 问题）。如果为了凑并行度而大量 Padding，会造成算力浪费。此外，社区中存在不同观点：有观点认为随着 FlashAttention-3 等硬件级优化的出现，单卡处理长序列的能力在提升，复杂的序列并行可能在未来几年内被单卡算力增长所抵消；但反对者认为模型规模增长速度远超单卡显存增长，分布式序列并行是通往 AGI 的必经之路。

**实际应用建议**

1.  **混合并行策略：** 在实际部署中，建议将 Ulysses 用于序列长度超过 100k 的场景。对于较短序列，回退到传统的 Tensor Parallelism 或 Pipeline Parallelism，以避免通信开销占比过高。
2.  **硬件匹配：** Ulysses 对计算密度要求高，对网络带宽相对宽容。如果你的集群是 GPU 卡间带宽大（如 NVLink）、节点间带宽小（如便宜的以太网），Ulysses 是比 Ring Attention 更优的选择。

**可验证的检查方式**

1.  **通信耗时占比测试：**
    *指标：* 在不同序列长度

---

## 技术分析

### 2. 关键技术实现细节

**分布式注意力算法**：
Ulysses 的核心在于对 Transformer Self-Attention 数学性质的重构。它利用矩阵乘法的结合律，调整了计算顺序。
*   **传统方法**：通常需要巨大的显存来存储完整的注意力矩阵。
*   **Ulysses 方法**：通过先进行局部计算，再进行通信聚合，避免了单卡显存溢出，同时保证了数学结果的一致性。

**与 Megatron-LM 的结合**：
Ulysses 通常与张量并行（TP）结合使用。在 MLP 层使用 TP 进行切分，而在 Attention 层使用 Ulysses 进行序列切分，从而在不牺牲模型精度的前提下，最大化利用硬件资源。

---

## 最佳实践

### 实践 1：合理配置序列并行度

**说明**: Ulysses 通过将长序列切分到多个 GPU 上进行处理，从而突破显存限制。最佳实践是将序列并行度（SP Degree）设置为可用 GPU 数量的因数，且通常建议 SP Degree 与张量并行度（TP）的乘积等于总 GPU 数量。对于超长上下文（100万+ token），建议使用较高的 SP Degree（如 4 或 8）以最大化显存节省。

**实施步骤**:
1. 根据模型总 GPU 数量和张量并行度，确定可用的序列并行度（例如：总 GPU 32，TP 4，则 SP 可设为 8）。
2. 在 DeepSpeed 或 Megatron 配置文件中，将序列并行策略设置为 "ulysses"。
3. 确保批次大小能够被 SP Degree 整除，以保证负载均衡。

**注意事项**: 避免将 SP Degree 设置得过大（例如超过 8），因为跨节点的 All-Reduce 通信开销可能会抵消显存节省带来的收益。

---

### 实践 2：优化通信重叠与显存开销

**说明**: Ulysses 的核心机制涉及计算与通信的重叠。为了达到最佳性能，必须确保 Attention 计算中的 All-Gather 和 Reduce-Scatter 操作能够被计算流水线有效隐藏。特别是在处理百万级 Token 时，通信量巨大，优化此点至关重要。

**实施步骤**:
1. 确保底层通信库（如 NCCL）已针对当前网络拓扑（InfiniBand 或 RoCE）进行调优。
2. 启用 FlashAttention 或其变体（如 FlashAttention-2），以加速 Attention 计算从而更好地隐藏通信延迟。
3. 检查训练脚本中是否正确启用了 `sequence_parallel` 参数，确保通信算子被正确插入计算图中。

**注意事项**: 监控 GPU 利用率（SM Utilization）。如果利用率在通信阶段出现明显下降，说明通信未能有效重叠，需要检查 NCCL 环境变量或减少 SP Degree。

---

### 实践 3：动态调整批次大小与上下文长度

**说明**: 在百万级上下文训练中，显存通常首先被 KV Cache 占满。最佳实践是动态调整全局批次大小，或者采用梯度累积来模拟大批次训练，同时保持单个序列的长度最大化。

**实施步骤**:
1. 使用显存分析工具（如 `nvidia-smi` 或 PyTorch Profiler）确定当前 SP Degree 下单个 GPU 能容纳的最大序列长度。
2. 设置较小的 Micro Batch Size（甚至为 1），并增加梯度累积步数以维持等效的 Global Batch Size。
3. 实验性地增加序列长度，直到 OOM（显存溢出），然后回退到稳定值。

**注意事项**: 过小的 Micro Batch Size 可能会影响 BN（Batch Norm）层（如果模型中有）或特定算子的性能，需权衡稳定性与上下文长度。

---

### 实践 4：环形注意力通信拓扑优化

**说明**: Ulysses 依赖环形通信来分发 Attention 的分块。在物理部署上，应尽量让序列并行的 GPU 组位于同一个物理机节点内，或者通过高速网络互联，以最小化通信延迟。

**实施步骤**:
1. 在多节点训练时，优先将 TP（张量并行）组限制在节点内，而将 SP（序列并行）组跨节点部署，或者根据网络带宽灵活调整。
2. 配置 NCCL 的环形拓扑，使其优先使用节点内的高带宽链路（如 NVLink）进行 SP 通信。
3. 测试不同的 SP/TP 组合策略，比较每秒处理的 Token 数量。

**注意事项**: 跨节点的高延迟通信会严重拖慢 Ulysses 的训练速度，因为 Attention 计算依赖于频繁的同步。如果必须跨节点，建议降低 SP Degree。

---

### 实践 5：检查点与容错策略

**说明**: 训练百万级上下文的模型成本极高，且训练时间较长。Ulysses 涉及复杂的张量切分，普通的模型保存和加载可能不兼容。必须确保 Checkpoint 机制能够正确处理序列并行的状态。

**实施步骤**:
1. 使用支持分布式 Checkpoint 的框架（如 DeepSpeed Checkpointing 或 Megatron-LM 的 Checkpoint），确保在保存时仅保存 Rank 0 的模型权重或统一保存分片权重。
2. 设置合理的保存频率，考虑到巨大的显存占用，保存 Checkpoint 可能需要较长时间。
3. 实施自动重启动机制，确保在节点故障后能利用最新的 Checkpoint 恢复训练，且 SP 组的配置保持一致。

**注意事项**: 加载 Checkpoint 时必须严格匹配训练时的 SP Degree，否则模型权重无法正确映射到切分后的注意力块中。

---

### 实践 6：长上下文数据填充与打包

**说明**: 为了充分利用 Ulysses 的并行能力，输入数据应尽量均匀分布。不同长度的样本会导致计算负载

---

## 学习要点

- Ulysses 通过将超长序列切分到多个 GPU 上并行处理，打破了内存限制，从而实现了百万级 Token 上下文的模型训练。
- 该方法将序列并行与数据并行解耦，允许在不增加通信开销的情况下，通过增加 GPU 数量来线性扩展上下文长度。
- Ulysses 在保持计算效率的同时，能够完美维持长上下文训练的数学等价性，确保模型精度不受影响。
- 相比于 Ring Attention 等方案，Ulysses 极大地减少了节点间的通信量，显著提升了长序列训练的吞吐量和扩展性。
- 该技术已集成到 Megatron-LM 中，证明了其在工业级大模型训练框架中的实用性与兼容性。
- Ulysses 为解决长上下文训练中的显存瓶颈和通信延迟问题提供了一种高效且通用的优化范式。

---

## 引用

- **文章/节目**: [https://huggingface.co/blog/ulysses-sp](https://huggingface.co/blog/ulysses-sp)
- **RSS 源**: [https://huggingface.co/blog/feed.xml](https://huggingface.co/blog/feed.xml)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Ulysses](/tags/ulysses/) / [序列并行](/tags/%E5%BA%8F%E5%88%97%E5%B9%B6%E8%A1%8C/) / [长上下文](/tags/%E9%95%BF%E4%B8%8A%E4%B8%8B%E6%96%87/) / [分布式训练](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E8%AE%AD%E7%BB%83/) / [Megatron](/tags/megatron/) / [Attention](/tags/attention/) / [显存优化](/tags/%E6%98%BE%E5%AD%98%E4%BC%98%E5%8C%96/) / [LLM](/tags/llm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Ulysses序列并行：实现百万级Token上下文训练]({{< relref "posts/20260310-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-10.md" >}})
- [Ulysses序列并行技术实现百万Token上下文训练]({{< relref "posts/20260309-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-5.md" >}})
- [Ulysses序列并行：支持百万Token上下文训练]({{< relref "posts/20260309-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-7.md" >}})
- [Ulysses序列并行技术支持百万级Token上下文训练]({{< relref "posts/20260310-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-8.md" >}})
- [Ulysses序列并行技术实现百万Token上下文训练]({{< relref "posts/20260310-blogs_podcasts-ulysses-sequence-parallelism-training-with-million-7.md" >}})
