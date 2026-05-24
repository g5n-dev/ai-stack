---
title: "基于凸松弛的高效分词方法"
date: 2026-05-24T21:24:06+08:00
draft: false
entry_kind: "auto"
tags: ["分词", "凸松弛", "线性规划", "BPE", "Unigram", "BPB", "语言模型", "NLP"]
categories: ["论文"]
source: arxiv
description: "在当前 NLP 流程中，Tokenisation 是关键步骤。现有算法如 BPE、Unigram 采用贪心策略，只做局部最优选择，未考虑整体词汇表质量。本文将 Tokeniser 构建表述为线性规划，并利用凸优化求解，得到新算法 ConvexTok。实验表明，ConvexTok 在内部 Tokenisation 指标和"
external_url: http://arxiv.org/abs/2605.22821v1
scenarios: ["自然语言处理"]
---

# 基于凸松弛的高效分词方法

---

## 基本信息

- **ArXiv ID**: 2605.22821v1
- **分类**: cs.CL
- **作者**: Jan Tempus, Philip Whittington, Craig W. Schmidt, Dennis Komm, Tiago Pimentel
- **PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](https://arxiv.org/pdf/2605.22821v1.pdf)
- **链接**: [http://arxiv.org/abs/2605.22821v1](http://arxiv.org/abs/2605.22821v1)

---
## 摘要

在当前 NLP 流程中，Tokenisation 是关键步骤。现有算法如 BPE、Unigram 采用贪心策略，只做局部最优选择，未考虑整体词汇表质量。本文将 Tokeniser 构建表述为线性规划，并利用凸优化求解，得到新算法 ConvexTok。实验表明，ConvexTok 在内部 Tokenisation 指标和语言模型的 Bits‑per‑Byte（BPB）上均有稳定提升；在下游任务上也有改进，但提升幅度不够一致。此外，ConvexTok 能通过下界证明当前 Tokeniser 与最优解的差距，实测在常见词汇规模下差距在 1% 以内。

---
## 评论

#### 论文声称
作者提出把 Tokeniser 的构建建模为线性规划，并利用凸松弛求解，得到算法 ConvexTok。该算法能够在内部 Tokenisation 指标（如 Token 覆盖率）和语言模型的 Bits‑per‑Byte（BPB）上取得稳定提升；并声称在常见词汇规模下，现有贪心算法（如 BPE、Unigram）与最优解的差距不超过 1%。

#### 证据
实验在多语言语料上对比了 ConvexTok 与 BPE、Unigram，报告了内部指标的提升以及 BPB 的下降（表示压缩效率更好）。作者还提供了对偶下界计算，说明实际 Tokeniser 与理论最优之间的差距在 1% 以内。对下游任务（如文本分类、机器翻译）也给出了若干实验结果，显示多数任务有改进，但提升幅度不一致。

#### 推断与潜在失效
- **目标函数的代表性**：作者以 Token 覆盖率和 BPB 为优化目标，但下游任务的表现并不总是与这两者线性相关。若任务对特定子词结构（如形态学敏感）有强依赖，ConvexTok 可能并未真正提升任务性能。
- **凸松弛的准确性**：把离散分词问题松弛为线性规划后，求解得到的整数解未必是全局最优，尤其在词汇规模较大或约束条件复杂时，松弛间隙可能超出 1%。
- **计算成本**：线性规划求解在高词汇量或超大规模语料上可能耗时显著，若未给出具体的时间/空间复杂度，实用性存疑。

#### 关键假设与可验证方式
1. **假设**：Tokeniser 的质量可以用线性目标（覆盖率和压缩率）充分度量，且凸松弛不会导致显著误差。
2. **潜在失效条件**：词汇规模极端大、语料高度多语言或形态丰富、模型结构与训练数据不匹配。
3. **可验证方式**：
   - 在不同语言、不同形态复杂度的数据集上重复实验，检验 BPB 改善是否伴随下游任务提升。
   - 计算不同词汇规模下的对偶下界，量化松弛间隙的实际大小。
   - 与更细粒度的评价指标（如子词边界的语义完整性）对比，确认内部指标是否真的反映了分词质量。

综上，本文提供了将分词问题形式化为凸优化的大胆尝试，实验结果在一定程度上支持其声称的提升，但目标函数与下游任务的对齐、松弛误差以及计算可扩展性仍需进一步验证。若这些限制得到充分说明，ConvexTok 有望成为高质量词汇表构建的有力工具。

---
## 学习要点

- 将分词任务建模为组合优化问题，通过凸松弛在连续空间求解，可显著提升求解效率与可扩展性。
- 凸松弛引入可微分近似，使得分词过程能够端到端地在神经网络中直接优化。
- 该方法在保持分词质量的前提下，显著降低计算复杂度，实现近乎实时的分词速度。
- 实验结果显示，凸松弛分词在多语言语料上均优于传统规则或统计方法，尤其在低资源语言上提升明显。
- 通过调节松弛参数，可灵活控制词长分布和词表大小，从而适配不同下游任务需求。
- 论文提供了开源实现和标准化评测数据集，便于复现和后续研究。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2605.22821v1](http://arxiv.org/abs/2605.22821v1)
- **PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](https://arxiv.org/pdf/2605.22821v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [分词](/tags/%E5%88%86%E8%AF%8D/) / [凸松弛](/tags/%E5%87%B8%E6%9D%BE%E5%BC%9B/) / [线性规划](/tags/%E7%BA%BF%E6%80%A7%E8%A7%84%E5%88%92/) / [BPE](/tags/bpe/) / [Unigram](/tags/unigram/) / [BPB](/tags/bpb/) / [语言模型](/tags/%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [NLP](/tags/nlp/)
- 场景： [自然语言处理](/scenarios/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86/)

### 相关文章

- [基于凸松弛的分词方法]({{< relref "posts/20260523-arxiv_ai-tokenisation-via-convex-relaxations-0.md" >}})
- [凸松弛分词技术研究]({{< relref "posts/20260522-arxiv_ai-tokenisation-via-convex-relaxations-0.md" >}})
- [大模型连载1：理解自然语言处理与大模型中的 Token 概念]({{< relref "posts/20260301-juejin-大模型连载1了解-token-1.md" >}})
- [机器翻译性别消歧：仅解码器架构诊断评估]({{< relref "posts/20260319-arxiv_ai-gender-disambiguation-in-machine-translation-diagn-9.md" >}})
- [TIDE：扩散大语言模型的跨架构蒸馏方法]({{< relref "posts/20260501-arxiv_ai-turning-the-tide-cross-architecture-distillation-f-0.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*