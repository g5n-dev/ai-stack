---
title: "Kolmogorov-Chapman Maps: Trajectory-Free Learning for Simulating Molecular Dynamics"
date: 2026-11-11T01:50:22+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "深度学习", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:25210c26d57725afb61f71874b360951731603c2bbc1e5532912a0989b218789"
source_payload_sha256: "sha256:fb87c439f259222c1e90a13f5c012d0c2b7e379977a8eae66eec9654fb02e828"
observation_id: obs_5c36d448a8b8e4f59135987bae77e299b85b0879d181d61b7e7c9246ac156721
event_id: evt_bc15a0787a1dbcaf6550bdacd92eb21eb5aa279a241eb77c340680648b80fcb9
revision_id: rev_eb9c2816a5312ee5f7a8e97498b92716a335deae087ca80474bb5330fb0fa58d
source_published_at: 2026-11-09T18:59:13Z
first_seen_at: 2026-11-10T17:49:04.581126Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
interpretation_sha256: "sha256:985e5c073f2f38280c49eed93409cbf926b7b75798ea63e33b2797f864373579"
description: "KC-Maps 是一种面向随机微分方程的神经网络学习方法，用边缘分布样本和已知的漂移、扩散系数学习状态转移核，无需长时间模拟轨迹即可一次预测到指定时刻的状态分布。"
external_url: http://arxiv.org/abs/2611.12880v1
parent_observation_id: null
last_seen_at: 2026-11-10T17:49:04.581126Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.12880v1](http://arxiv.org/abs/2611.12880v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Majdi Hassan、Marta Skreta、Dominique Beaini 等

## 要点解读

### 这是什么
KC-Maps 是一种面向随机微分方程的神经网络学习方法，用边缘分布样本和已知的漂移、扩散系数学习状态转移核，无需长时间模拟轨迹即可一次预测到指定时刻的状态分布。

### 用在哪里
它适合需要捕捉稀有事件或状态转变、但逐步数值积分耗时较长的分子动力学模拟，也可用于其他随机过程模拟。

### 可以推断的
- 推测：该方法可能减少对大规模轨迹数据的依赖，使训练数据准备更高效。
- 推测：将转移规律融入网络结构和训练目标，有望提升模拟结果对真实动力学的保持能力。

## 来源摘要/节选

> Stochastic differential equations (SDEs) describe stochastic processes across a wide range of scientific domains, including physics, biology, and finance. Although individual numerical integration steps are inexpensive, observing meaningful events or transitions can require millions of sequential steps, resulting in substantial wall-clock simulation time and poor hardware utilization. Deep learning offers an alternative by amortizing many integration steps into a single neural network forward pass, potentially enabling much faster simulation. However, existing supervised approaches typically require long simulated trajectory data, which restricts their applicability. In this work, we introduce Kolmogorov-Chapman Maps (KC-Maps), a method for learning the transition kernel of an SDE that relies only on the trajectory-free marginal samples together with the known drift and diffusion coefficients. Given an initial time and state of a process, KC-Maps models its distribution integrated to any given time, corresponding to the weak solution of the SDE. To recover the correct dynamics, KC-Maps satisfies two key properties: (i) it satisfies the boundary conditions, which we incorporate directly into the neural network architecture, and (ii) it respects the Kolmogorov--Chapman equation, which provides an efficient training objective. We empirically demonstrate that KC-Maps learns to integrate the dynamics of peptide molecular systems and outperforms classical molecular dynamics in terms of GPU-hours.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。