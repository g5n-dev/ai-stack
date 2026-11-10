---
title: "Kolmogorov-Chapman Maps: Trajectory-Free Learning for Simulating Molecular Dynamics"
date: 2026-11-11T07:19:10+08:00
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
first_seen_at: 2026-11-10T23:17:49.783259Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
interpretation_sha256: "sha256:64f78f59ef5373e8351d80f21b21d29e0342af74e0489f117a9a647043a1247c"
description: "KC-Maps 是一种无需完整模拟轨迹的随机微分方程学习方法，仅利用边缘分布样本及已知的漂移、扩散系数，训练神经网络直接预测任意时刻的状态分布。"
external_url: http://arxiv.org/abs/2611.12880v1
parent_observation_id: null
last_seen_at: 2026-11-10T23:17:49.783259Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.12880v1](http://arxiv.org/abs/2611.12880v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Majdi Hassan、Marta Skreta、Dominique Beaini 等

## 要点解读

### 这是什么
KC-Maps 是一种无需完整模拟轨迹的随机微分方程学习方法，仅利用边缘分布样本及已知的漂移、扩散系数，训练神经网络直接预测任意时刻的状态分布。

### 用在哪里
它面向传统数值积分耗时、硬件利用率较低的场景，尤其适合需要捕捉长时间尺度分子动力学的肽类系统模拟。

### 可以推断的
- 推测：对只关心长期状态转移或重要事件、而非每一步轨迹细节的模拟任务，该方法可能更具实用价值。
- 推测：若目标系统的时间跨度较大，直接预测积分后分布有望减少连续求解带来的计算开销。

## 来源摘要/节选

> Stochastic differential equations (SDEs) describe stochastic processes across a wide range of scientific domains, including physics, biology, and finance. Although individual numerical integration steps are inexpensive, observing meaningful events or transitions can require millions of sequential steps, resulting in substantial wall-clock simulation time and poor hardware utilization. Deep learning offers an alternative by amortizing many integration steps into a single neural network forward pass, potentially enabling much faster simulation. However, existing supervised approaches typically require long simulated trajectory data, which restricts their applicability. In this work, we introduce Kolmogorov-Chapman Maps (KC-Maps), a method for learning the transition kernel of an SDE that relies only on the trajectory-free marginal samples together with the known drift and diffusion coefficients. Given an initial time and state of a process, KC-Maps models its distribution integrated to any given time, corresponding to the weak solution of the SDE. To recover the correct dynamics, KC-Maps satisfies two key properties: (i) it satisfies the boundary conditions, which we incorporate directly into the neural network architecture, and (ii) it respects the Kolmogorov--Chapman equation, which provides an efficient training objective. We empirically demonstrate that KC-Maps learns to integrate the dynamics of peptide molecular systems and outperforms classical molecular dynamics in terms of GPU-hours.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。