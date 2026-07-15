---
title: 'MARTI-MARS$^2$: Scaling Multi-Agent Self-Search via Reinforcement Learning
  for Code Generation'
date: 2026-02-10 03:34:40+08:00
draft: false
entry_kind: auto
tags:
- arxiv
- cs.LG
categories:
- 论文
source: arxiv
description: 本文介绍了 MARTI-MARS$^2$，一种结合强化学习与多智能体树搜索的代码生成框架，旨在突破单一大语言模型（LLM）的性能瓶颈。 单智能体系统在复杂代码生成任务中面临性能天花板。现有的多智能体框架通常依赖基于提示词的交互或同质化参数训练，缺乏有效的错误纠正能力和策略多样性。
external_url: http://arxiv.org/abs/2602.07848v1
scenarios:
- Web应用开发
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **ArXiv ID**: 2602.07848v1
- **分类**: cs.LG
- **作者**: Shijie Wang, Pengfei Li, Yikun Fu, Kaifeng Liu, Fangyuan Li
- **PDF**: [https://arxiv.org/pdf/2602.07848v1.pdf](https://arxiv.org/pdf/2602.07848v1.pdf)
- **链接**: [http://arxiv.org/abs/2602.07848v1](http://arxiv.org/abs/2602.07848v1)

---
## 摘要

本文介绍了 **MARTI-MARS$^2$**，一种结合强化学习与多智能体树搜索的代码生成框架，旨在突破单一大语言模型（LLM）的性能瓶颈。

### 核心问题与动机
单智能体系统在复杂代码生成任务中面临性能天花板。现有的多智能体框架通常依赖基于提示词的交互或同质化参数训练，缺乏有效的错误纠正能力和策略多样性。

### 方法创新
MARTI-MARS$^2$ 将多智能体协作探索过程构建为一个动态且可学习的环境，通过以下方式实现突破：
1.  **策略学习与树搜索融合**：允许智能体在环境中迭代探索和修正。
2.  **从同质到异质的演进**：训练过程从“参数共享的同质多角色”进化为“异质多智能体”，打破了单智能体的能力限制。
3.  **高效推理策略**：提出了 MARTI-MARS$^2$-T+ 策略，在测试时充分释放多智能体协作的潜力。

### 实验结果与新发现
在多个规模的代码生成基准测试中，该框架表现优异。使用两个协作的 32B 模型，MARTI-MARS$^2$ 达到了 **77.7%** 的通过率，超越了 GPT-5.1 等强基线模型。

### 新缩放定律
研究揭示了一条新的缩放定律：从单智能体过渡到同质多角色，最终演变为异质多智能体范式，能够逐步提高强化学习的性能上限、增强鲁棒的文本到代码（TTS）能力，并显著提升策略多样性。这表明，**策略多样性**是通过多智能体强化学习扩展智能的关键因素。

---
## 引用

- **ArXiv**: [http://arxiv.org/abs/2602.07848v1](http://arxiv.org/abs/2602.07848v1)
- **PDF**: [https://arxiv.org/pdf/2602.07848v1.pdf](https://arxiv.org/pdf/2602.07848v1.pdf)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


## 站内链接

- 分类： [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [arxiv](/tags/arxiv/) / [cs.LG](/tags/cs.lg/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于朗之万动力学的直接软策略采样]({{< relref "posts/20260210-arxiv_ai-direct-soft-policy-sampling-via-langevin-dynamics-2.md" >}})
- [基于嵌入的Top-$k$检索：理论上$\mathbb{R}^{2k}$维空间已足够]({{< relref "posts/20260129-arxiv_ai-mathbbr2k-is-theoretically-large-enough-for-embedd-8.md" >}})
- [R^{2k}维度理论上足以支持基于嵌入的Top-k检索]({{< relref "posts/20260129-arxiv_ai-mathbbr2k-is-theoretically-large-enough-for-embedd-8.md" >}})
- [为何Adam在$β_1=β_2$时更优：缺失的梯度尺度不变性原理]({{< relref "posts/20260130-arxiv_ai-why-adam-works-better-with-β_1-β_2-the-missing-gra-8.md" >}})
- [神经网络转逻辑流以优化边缘计算性能]({{< relref "posts/20260130-arxiv_ai-late-breaking-results-conversion-of-neural-network-5.md" >}})
*本文由 AI Stack 自动生成，深度解读学术研究。*
