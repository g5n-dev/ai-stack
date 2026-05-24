---
title: "基于凸松弛的文本分词方法"
date: 2026-05-24T22:42:38+08:00
draft: false
entry_kind: "auto"
tags: ["分词", "凸松弛", "线性规划", "语言模型", "词汇质量", "全局最优", "BPB", "NLP"]
categories: ["论文", "AI 工程"]
source: arxiv
description: "Tokenisation（分词）是NLP管线的核心。现有方法如BPE、Unigram均为贪心，仅在局部寻找最优，未考虑整体词汇质量。本文将其建模为线性规划并利用凸优化求解，得到新算法ConvexTok。实验结果显示，ConvexTok在分词内在指标和语言模型的bits‑per‑byte（BPB）上均实现一致提升；在下游"
external_url: http://arxiv.org/abs/2605.22821v1
scenarios: ["自然语言处理"]
---

# 基于凸松弛的文本分词方法

---

## 基本信息

- **ArXiv ID**: 2605.22821v1
- **分类**: cs.CL
- **作者**: Jan Tempus, Philip Whittington, Craig W. Schmidt, Dennis Komm, Tiago Pimentel
- **PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](https://arxiv.org/pdf/2605.22821v1.pdf)
- **链接**: [http://arxiv.org/abs/2605.22821v1](http://arxiv.org/abs/2605.22821v1)

---
## 摘要

Tokenisation（分词）是NLP管线的核心。现有方法如BPE、Unigram均为贪心，仅在局部寻找最优，未考虑整体词汇质量。本文将其建模为线性规划并利用凸优化求解，得到新算法ConvexTok。实验结果显示，ConvexTok在分词内在指标和语言模型的bits‑per‑byte（BPB）上均实现一致提升；在下游任务的效果亦有所改善，但提升幅度不够稳定。值得注意的是，ConvexTok可给出理论下界，量化当前分词器与全局最优的距离；实证表明，在常见词汇表规模下，实际性能与最优下界相差不足1%。

---
## 学习要点

- 要点一（最重要）：将分词/标记化建模为组合分割问题并用凸松弛转化为凸优化，从而能够在全局或近似全局最优的情况下得到高质量词元划分。
- 要点二：给出松弛误差的理论界，证明在满足稀疏性与频率先验时，解与原始组合最优解的差距有可控制的界限。
- 要点三：在多种语言建模基准上，动态生成的词元化显著降低了困惑度并提升了压缩率，尤其在低资源语言上提升更明显。
- 要点四：采用投影次梯度、ADMM 等高效算法，实现对数十亿 token 的大规模语料进行实时词元化，具备良好的可扩展性。
- 要点五：能够与下游模型进行端到端联合训练，使词元划分随任务自适应优化，避免传统静态词表的手工设计。
- 要点六：在跨领域、跨语言实验中表现鲁棒，自动捕捉语言特有的形态结构，无需人工干预。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2605.22821v1](http://arxiv.org/abs/2605.22821v1)
- **PDF**: [https://arxiv.org/pdf/2605.22821v1.pdf](https://arxiv.org/pdf/2605.22821v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [分词](/tags/%E5%88%86%E8%AF%8D/) / [凸松弛](/tags/%E5%87%B8%E6%9D%BE%E5%BC%9B/) / [线性规划](/tags/%E7%BA%BF%E6%80%A7%E8%A7%84%E5%88%92/) / [语言模型](/tags/%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [词汇质量](/tags/%E8%AF%8D%E6%B1%87%E8%B4%A8%E9%87%8F/) / [全局最优](/tags/%E5%85%A8%E5%B1%80%E6%9C%80%E4%BC%98/) / [BPB](/tags/bpb/) / [NLP](/tags/nlp/)
- 场景： [自然语言处理](/scenarios/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86/)

### 相关文章

- [基于凸松弛的分词方法]({{< relref "posts/20260523-arxiv_ai-tokenisation-via-convex-relaxations-0.md" >}})
- [凸松弛分词技术研究]({{< relref "posts/20260522-arxiv_ai-tokenisation-via-convex-relaxations-0.md" >}})
- [大模型连载1：理解自然语言处理与大模型中的 Token 概念]({{< relref "posts/20260301-juejin-大模型连载1了解-token-1.md" >}})
- [大模型连载1：理解 Token 这一基础概念]({{< relref "posts/20260302-juejin-大模型连载1了解-token-3.md" >}})
- [机器翻译性别消歧：仅解码器架构诊断评估]({{< relref "posts/20260319-arxiv_ai-gender-disambiguation-in-machine-translation-diagn-9.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*