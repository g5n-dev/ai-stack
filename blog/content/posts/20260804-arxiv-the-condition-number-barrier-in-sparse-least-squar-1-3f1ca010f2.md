---
title: "The Condition-Number Barrier in Sparse Least Squares"
date: 2026-08-04T17:53:30+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.DS", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5b3e712bed95e8dd2ef9997809e298f6fdb71459bbc7e46f210f448b814ede0b"
source_payload_sha256: "sha256:8f9082e5a87e2a2e805908349124538f1797ad8db4fc1b3d377a97e88ef0a184"
observation_id: obs_3f1ca010f2acdfdf993da629a3cacd752c145a479ac90215a38449f44b28aacf
event_id: evt_4393b67c2408e34b2042a6fc3d54ba9f8712b54b22e9e8bcbd632250ea82dc35
revision_id: rev_63acfb8aaca94ea690734ac97fdb63eb47f2f3f03240917be66a37ac9ae2c5e9
source_published_at: 2026-08-03T17:57:01Z
first_seen_at: 2026-08-04T10:02:28Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
interpretation_sha256: "sha256:9d94732fe1adcbbc0e408bb26b271c7819126900da347c1c9d943a8e9aa4633a"
description: "这是一篇理论工作，给出了稀疏最小二乘问题在随机精确体积小集合展开假设下的计算下界，说明在该假设成立时，任何随机多项式时间算法都难以在满足稀疏度约束的同时把残差误差降到一定水平以下，证明过程借助了内部开发的自动化系统。"
external_url: http://arxiv.org/abs/2608.02588v1
parent_observation_id: null
last_seen_at: 2026-08-04T09:50:48.583748Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.02588v1](http://arxiv.org/abs/2608.02588v1)
- **发布域名**: arxiv.org
- **分类**: cs.DS
- **作者**: Honghao Lin、Vahab Mirrokni、David P. Woodruff

## 要点解读

### 这是什么  
这是一篇理论工作，给出了稀疏最小二乘问题在随机精确体积小集合展开假设下的计算下界，说明在该假设成立时，任何随机多项式时间算法都难以在满足稀疏度约束的同时把残差误差降到一定水平以下，证明过程借助了内部开发的自动化系统。  

### 用在哪里  
适用于对稀疏回归与稀疏优化算法进行复杂度分析的研究者，以及在高维稀疏建模任务中需要评估算法理论极限的工程师和学者。  

### 可以推断的  
推测：在实际任务中，如果对稀疏性和误差都有严格要求，往往只能求助于超多项式时间或近似启发式方法，而难以找到满足该下界的快速算法。  
推测：该下界表明，在不引入更强计算假设的情况下，设计能在稀疏度和近似误差上同时改进的多项式时间算法在理论上极为困难。

## 来源摘要/节选

> In [AS21], Axiotis and Sviridenko conjectured that the linear dependence on the restricted condition number in sparse convex optimization cannot be improved by a polynomial-time algorithm. We establish their conjectured lower bound for least-squares objectives, conditional on the randomized exact-volume Small-Set Expansion Hypothesis in the weighted regular-graph formulation of Raghavendra, Steurer, and Tulsiani [RST12]. Concretely, for every fixed $γ\in(0,1]$, there is no randomized polynomial-time algorithm that, with probability at least $2/3$, returns a vector $x$ such that, writing $s=\lVert x\rVert_0$, \[
> \lVert Ax-b\rVert_2^2
> \leq
> \min_{\lVert z\rVert_0\leq k}\lVert Az-b\rVert_2^2+\varepsilon
> \quad\text{and}\quad
> s=O\!\left(k\,κ_{s+k}^{\,1-γ}\right), \] where $κ_r$ is the restricted condition number at sparsity level $r$. The result holds even on rational instances with $A$ of full column rank.
> The proof was first obtained using a fully automated Gemini-based agentic system developed internally at Google. The authors have verified the proof and edited it for clarity of presentation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。