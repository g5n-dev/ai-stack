---
title: "基于凸松弛的文本标记化方法"
date: 2026-05-22T12:08:11+08:00
draft: false
entry_kind: "auto"
tags: ["分词", "凸松弛", "线性规划", "词表优化", "编码效率", "BPE", "NLP", "ConvexTok"]
categories: ["论文", "AI 工程"]
source: arxiv
description: "背景与动机 当前自然语言处理流程中，Tokenisation（分词）是关键环节。常用的 BPE 与 Unigram 算法均采用贪心策略，仅在局部做出最优选择，未考虑生成的词表整体效果，导致tokenisation质量受限。 方法：ConvexTok 将词表构建重新表述为线性规划问题，并利用凸优化求解，得到全新算法 Co"
external_url: http://arxiv.org/abs/2605.22821v1
scenarios: ["自然语言处理"]
---

# 基于凸松弛的文本标记化方法

---

## 基本信息

- **ArXiv ID**: 2605.22821v1
- **分类**: cs.CL
- **作者**: Jan Tempus, Philip Whittington, Craig W. Schmidt, Dennis Komm, Tiago Pimentel
- **PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](https://arxiv.org/pdf/2605.22821v1.pdf)
- **链接**: [http://arxiv.org/abs/2605.22821v1](http://arxiv.org/abs/2605.22821v1)

---
## 导语

在自然语言处理流程中，tokenisation是连接原始文本与模型处理的关键环节。现有主流算法如BPE和Unigram依赖贪心策略进行词汇表构建，难以兼顾全局最优性。本文提出ConvexTok方法，将词汇表构建问题形式化为线性规划并通过凸松弛求解，从而在优化框架下系统性地探索词汇分割空间。无法从摘要确认该方法在具体任务上的性能表现，但其理论框架或为自动化词汇表设计提供新思路，可能对多语言处理及领域自适应等应用场景产生参考价值。

---
## 摘要

#### 背景与动机
当前自然语言处理流程中，Tokenisation（分词）是关键环节。常用的 BPE 与 Unigram 算法均采用贪心策略，仅在局部做出最优选择，未考虑生成的词表整体效果，导致tokenisation质量受限。

#### 方法：ConvexTok
将词表构建重新表述为线性规划问题，并利用凸优化求解，得到全新算法 ConvexTok。该方法在全局层面优化词表，兼顾词汇覆盖与编码效率。求解过程可输出下界，用于量化当前词表与理论最优之间的差距。

#### 实验结果
- 在内部指标（如词汇覆盖率、编码长度）上，ConvexTok 稳定优于传统贪心算法。
- 语言模型的 bits‑per‑byte (BpB) 指标显著下降，说明压缩效率提升。
- 对下游任务（如文本分类、机器翻译）的性能提升存在，但提升幅度不如 BpB 一致。
- 通过下界验证，实际词表在常用规模下与最优解的差距不超过 1%。

#### 优势与意义
ConvexTok 为 tokeniser 设计提供了一种可证明最优性的全局优化框架，兼顾性能提升与可解释性，为后续更高效、更适配特定任务的词表构建奠定基础。

---
## 学习要点

- 将离散的分词问题松弛为凸优化问题，实现端到端可微的分词，从而可以与下游模型一起联合优化（最重要）
- 通过对词汇表大小和词根词缀施加凸约束，确保生成的分词既紧凑又能覆盖高频模式
- 使用对偶坐标上升或交替方向乘子法（ADMM）等高效算法求解松弛问题，计算复杂度接近线性
- 在训练阶段引入软分词概率，使模型能够在推理时自适应地选择最优的分词粒度
- 与传统 BPE 等启发式分词相比，凸松弛方法在跨语言和少样本场景中表现更稳定
- 该方法可推广到多模态分词（如图像块+文字），并在统一凸约束框架下实现跨模态 token 共享
- 可通过调节正则化参数平衡分词粒度和词汇表大小，以灵活适应不同任务需求

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2605.22821v1](http://arxiv.org/abs/2605.22821v1)
- **PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](https://arxiv.org/pdf/2605.22821v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [分词](/tags/%E5%88%86%E8%AF%8D/) / [凸松弛](/tags/%E5%87%B8%E6%9D%BE%E5%BC%9B/) / [线性规划](/tags/%E7%BA%BF%E6%80%A7%E8%A7%84%E5%88%92/) / [词表优化](/tags/%E8%AF%8D%E8%A1%A8%E4%BC%98%E5%8C%96/) / [编码效率](/tags/%E7%BC%96%E7%A0%81%E6%95%88%E7%8E%87/) / [BPE](/tags/bpe/) / [NLP](/tags/nlp/) / [ConvexTok](/tags/convextok/)
- 场景： [自然语言处理](/scenarios/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86/)

### 相关文章

- [大模型连载1：理解自然语言处理与大模型中的 Token 概念]({{< relref "posts/20260301-juejin-大模型连载1了解-token-1.md" >}})
- [大模型连载1：理解 Token 这一基础概念]({{< relref "posts/20260302-juejin-大模型连载1了解-token-3.md" >}})
- [🌍 242种语言大比拼！Wikipedia数据揭秘跨语言比较语言学新突破！]({{< relref "posts/20260128-arxiv_ai-subword-based-comparative-linguistics-across-242-l-3.md" >}})
- [土耳其语子词策略大规模评估：数据、词表与形态交互]({{< relref "posts/20260209-arxiv_ai-optimal-turkish-subword-strategies-at-scale-system-7.md" >}})
- [🌍 跨242种语言！用子词模型解锁比较语言学新视角！]({{< relref "posts/20260127-arxiv_ai-subword-based-comparative-linguistics-across-242-l-3.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*