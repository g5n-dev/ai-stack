---
title: "Nonequilibrium Phases of Repulsive Self-Attention: Chaos, Attention Condensation, and Emergent Locality"
date: 2026-09-25T03:13:20+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cond-mat.dis-nn", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:1a65aace397377d7a93a58ed044afbda6caf4730353d9b7ad9dc1297eca40d53"
source_payload_sha256: "sha256:cf90f8a1192cb2ecee62efe80de1d3286f6770e94b45829fb9310287302304b8"
observation_id: obs_b96f629991ad5cfc75cb08b8f2c808a531b7b49e2c9185930e550088b0bcd5ff
event_id: evt_c0444bab38ee1e7bb5340f8c0a5f5a7998e76ae0c45031933c234ca0610459af
revision_id: rev_4288421ae3d337bc5a3392892d7200e8f3d58959ce8ff511bbea30961f1904c2
source_published_at: 2026-09-23T17:46:38Z
first_seen_at: 2026-09-24T19:09:21.891384Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 103
interpretation_sha256: "sha256:9f7cf3e66b74f33dee25bd0d125869b2c4c0531a2182e81aa964f2a960d3d0e5"
description: "这篇论文在一个最小循环transformer模型里，通过把价值映射设为负，研究了注意力反馈导致的非平衡相变，包括混沌、凝聚和局部几何聚类等现象。"
external_url: http://arxiv.org/abs/2609.28448v1
parent_observation_id: null
last_seen_at: 2026-09-24T19:09:21.891384Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.28448v1](http://arxiv.org/abs/2609.28448v1)
- **发布域名**: arxiv.org
- **分类**: cond-mat.dis-nn
- **作者**: Qucheng Gao、Zuyi Yang、Xiao Chen

## 要点解读

### 这是什么
这篇论文在一个最小循环transformer模型里，通过把价值映射设为负，研究了注意力反馈导致的非平衡相变，包括混沌、凝聚和局部几何聚类等现象。

### 用在哪里
适用于想了解注意力机制在长期演化中会出现哪些集体行为的研究者，尤其对注意力在稀疏设定下仍能保持活跃动态的机制感兴趣的人。

### 可以推断的
推测：当 softmax 锐度随 token 数目提升到约 N^2 规模时，注意力才可能出现凝聚。  
推测：在维度趋于无限且锐度保持在常数阶时，系统可以从均匀状态转变为凝聚相。

## 来源摘要/节选

> We study the nonequilibrium dynamics of a minimal recurrent transformer with $N$ normalized tokens, $Q=K=I$, and a negative value map $V=-I$. Similarity-based attention selects nearby representations, while the negative value map drives tokens away from the selected field. This feedback can continually reorganize both the representation geometry and the attention network. For $d=2$, the tokens lie on a circle, where the regular polygon is an exact fixed point. As the attention feedback strength $γ$ is increased, the polygon loses stability through a flip bifurcation, giving rise to period-two motion, chaos, and cluster-exchange or cluster-flip states. Despite this temporal complexity, attention remains diffuse as $N\to\infty$ at finite fixed softmax sharpness $β$. Attention condensation instead emerges in the scaling regime $β\sim N^2$. In the hard-routing limit, repulsive updates amplify local perturbations and routing-partner switches transmit them ballistically, producing an emergent butterfly cone in representation space. High-dimensional geometry provides a distinct route to localization. For $d=N\to\infty$, simulations from Gaussian initial conditions provide evidence for a condensation transition at $β=O(1)$, driven by dynamically generated finite overlap gaps. Depending on $γ$, the resulting phases include diffuse simplex-like states, consensus flips, condensed active routing with signatures of chaos, and fragmented cluster flips. These results establish temporal activity, attention condensation, and geometric clustering as distinct collective phenomena, and show that sparse attention can sustain persistent dynamics rather than freeze it.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。