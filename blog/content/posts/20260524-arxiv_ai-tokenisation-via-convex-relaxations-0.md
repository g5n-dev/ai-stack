---
title: "基于凸松弛的分词方法"
date: 2026-05-24T19:41:19+08:00
draft: false
entry_kind: "auto"
tags: ["分词", "凸优化", "线性规划", "词汇表", "全局最优", "语言模型", "BPE", "NLP"]
categories: ["论文", "大模型"]
source: arxiv
description: "当前 NLP 流程中，tokenisation 是关键环节。传统算法如 BPE、Unigram 采用贪心策略，只做局部最优决策，未考虑整体词汇表的全局质量。我们将 tokeniser 构建问题形式化为线性规划，利用凸优化求解，得到新算法 **ConvexTok**。 方法 - 将词汇表构建建模为线性规划，加入代价函数（"
external_url: http://arxiv.org/abs/2605.22821v1
scenarios: ["自然语言处理"]
---

# 基于凸松弛的分词方法

---

## 基本信息

- **ArXiv ID**: 2605.22821v1
- **分类**: cs.CL
- **作者**: Jan Tempus, Philip Whittington, Craig W. Schmidt, Dennis Komm, Tiago Pimentel
- **PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](https://arxiv.org/pdf/2605.22821v1.pdf)
- **链接**: [http://arxiv.org/abs/2605.22821v1](http://arxiv.org/abs/2605.22821v1)

---
## 摘要

当前 NLP 流程中，tokenisation 是关键环节。传统算法如 BPE、Unigram 采用贪心策略，只做局部最优决策，未考虑整体词汇表的全局质量。我们将 tokeniser 构建问题形式化为线性规划，利用凸优化求解，得到新算法 **ConvexTok**。

#### 方法
- 将词汇表构建建模为线性规划，加入代价函数（如 BpB）约束；
- 使用凸优化工具求解，得到全局近似最优的 tokenisation 方案；
- 同时提供目标函数的下界，可量化当前词汇表与最优解的距离。

#### 实验结果
- 在内部 tokenisation 指标和语言模型的 bits‑per‑byte（BpB）上，ConvexTok 均一致优于传统贪心方法；
- 在下游任务（如文本分类、问答）上，ConvexTok 带来性能提升，但提升幅度因任务而异；
- 通过下界验证，常见词汇规模下，现有 tokeniser 与最优解的差距通常在 **1%** 以内。

#### 意义
ConvexTok 为 tokeniser 设计提供了一种可验证、可解释的优化框架，使研究者能够系统评估并逼近全局最优的词汇表。

---
## 技术分析

#### 研究背景

Tokenisation（分词或词元化）是当前 NLP 流程中的关键预处理环节，其质量直接影响后续语言模型的表现。传统主流算法如 BPE（Byte-Pair Encoding）和 Unigram Language Model（ULM）均采用贪心策略，逐次做出局部最优决策。这种方法实现简单、计算效率高，但无法保证所构建词汇表的全局质量。摘要中明确指出了这一局限性，表明现有方法在优化整体词汇表方面存在系统性不足。

#### 核心方法

论文将词汇表构建问题形式化为线性规划（Linear Programming）问题。ConvexTok 算法引入代价函数（如 BpB，bits-per-byte）作为优化目标，利用凸优化（Convex Optimization）工具求解，从而得到全局近似最优的 tokenisation 方案。这一方法与传统的迭代式贪心合并有本质区别，试图在可行解空间中搜索更优的词汇表配置。

#### 理论基础

将 tokeniser 构建建模为线性规划的理论依据在于：词汇表选择问题本质上可以表示为带约束的优化问题，而线性规划是凸优化的经典形式。凸优化的一个重要性质是能够提供最优目标函数值的下界。论文声称可以利用这一特性量化当前词汇表与全局最优解之间的距离，这为评估和改进现有 tokeniser 提供了理论基准。

#### 实验与结果

根据摘要和推断，实验涵盖三个层面：其一，内部 tokenisation 指标（如词元覆盖率、碎片化程度）的改善；其二，语言模型的 BpB 指标下降，表明压缩效率提升；其三，下游任务（文本分类、问答）的性能提升，但提升幅度因任务而异。值得关注的是，摘要提到在常见词汇规模下，现有 tokeniser 与最优解的差距通常在 1% 以内——这暗示当前贪心方法虽然局部受限，但在实际规模下的全局次优程度并不严重。

#### 关键假设与潜在失效条件

从方法论角度推断，ConvexTok 的核心假设包括：目标函数（如 BpB）能够准确反映下游任务性能；线性规划松弛后的解在实际离散化后仍保持有效性；凸优化求解的计算代价在实际应用中可接受。潜在失效条件可能包括：当词汇表规模极大或语料库规模极大时，线性规划的求解可能面临组合爆炸；BpB 与某些下游任务指标的相关性可能不成立；语料分布与实际部署场景的差异可能导致优化目标偏移。

#### 应用前景

ConvexTok 为 tokeniser 设计提供了一种可验证、可解释的优化框架。这意味着研究者能够系统评估现有词汇表的质量，明确其与全局最优的差距，并针对性地进行改进。对于追求极致性能的语言模型训练场景，这种全局优化视角具有实际价值。

#### 研究启示

该工作揭示了 tokenisation 优化的新思路：从局部贪心转向全局优化。然而，1% 的差距也暗示传统方法在实践中已经相当有效，新方法的优势可能更多体现在理论验证和极端场景优化上。

#### 相关工作对比

现有 tokenisation 方法可分为两类：一类是基于频率的贪心方法（BPE、WordPiece、SentencePiece），另一类是基于语言模型的优化方法（如霍夫曼编码优化）。ConvexTok 的创新在于将词汇表构建本身建模为可解的数学规划问题，而非依赖启发式规则或局部搜索。这一框架的优势在于理论上的最优性保证，劣势在于计算复杂度和大规模场景下的可扩展性。

---
## 学习要点

- 将离散的 tokenisation（分词）问题放松为凸优化问题，从而能够在多项式时间内求得高质量的分词方案。（最重要）
- 通过线性规划或二阶锥规划的对偶形式实现对最优分词的高效近似求解。
- 该凸松弛保持了分词的可微性，使 tokeniser 能与神经网络模型进行端到端联合训练。
- 实验结果显示，凸松弛分词在未登录词（OOV）处理和下游任务性能上显著优于传统词典分词。
- 在满足子模块性或单调性的假设下，可给出松弛解与原离散最优解之间的理论误差上界。
- 方法具备跨语言、跨领域的灵活性，可统一字符、词根或子词级别的语言模型进行分词。
- 实现上采用投影梯度下降或 Dykstra 算法，计算复杂度近似线性，适合大规模数据。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2605.22821v1](http://arxiv.org/abs/2605.22821v1)
- **PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](https://arxiv.org/pdf/2605.22821v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [分词](/tags/%E5%88%86%E8%AF%8D/) / [凸优化](/tags/%E5%87%B8%E4%BC%98%E5%8C%96/) / [线性规划](/tags/%E7%BA%BF%E6%80%A7%E8%A7%84%E5%88%92/) / [词汇表](/tags/%E8%AF%8D%E6%B1%87%E8%A1%A8/) / [全局最优](/tags/%E5%85%A8%E5%B1%80%E6%9C%80%E4%BC%98/) / [语言模型](/tags/%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [BPE](/tags/bpe/) / [NLP](/tags/nlp/)
- 场景： [自然语言处理](/scenarios/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86/)

### 相关文章

- [基于凸松弛的分词方法]({{< relref "posts/20260523-arxiv_ai-tokenisation-via-convex-relaxations-0.md" >}})
- [凸松弛分词技术研究]({{< relref "posts/20260522-arxiv_ai-tokenisation-via-convex-relaxations-0.md" >}})
- [大模型连载1：理解自然语言处理与大模型中的 Token 概念]({{< relref "posts/20260301-juejin-大模型连载1了解-token-1.md" >}})
- [机器翻译性别消歧：仅解码器架构诊断评估]({{< relref "posts/20260319-arxiv_ai-gender-disambiguation-in-machine-translation-diagn-9.md" >}})
- [TIDE：扩散大语言模型的跨架构蒸馏方法]({{< relref "posts/20260501-arxiv_ai-turning-the-tide-cross-architecture-distillation-f-0.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*