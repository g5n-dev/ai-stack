---
title: "BAL: Bidirectional Autoregression in Latent Space for Learning Human Movement Representations"
date: 2026-11-17T04:29:14+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:927d999cec418e8a6d7c5d43224204eccee8f54a6f76bfb6781e80e647e72749"
source_payload_sha256: "sha256:b7ad6ee71f76bd2da2013e5307df28f5dc7b1df8a8d7351ec9fb2361d73b25f8"
observation_id: obs_bb23effe0afa49bfa17e1d85beaead937e1cca4fd8d9f0c44d363fc18ea14e1d
event_id: evt_307ac6c1faa6b84a995d5bc13a68467961b5d2e616cf0cdd06c4115f8565c788
revision_id: rev_0e8f76d78d41904c069819a269db6c7cd3a45e30749fba44d75878eff7933cd5
source_published_at: 2026-11-13T18:58:54Z
first_seen_at: 2026-11-16T20:27:46.445948Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
interpretation_sha256: "sha256:fa6407b9a87223fba39a072d5c5e0f8a8ab948807cd3c40dccf5f112932bb95a"
description: "BAL 是一种面向三维人体姿态序列的自监督学习框架，在潜在空间中进行前向与后向的自回归预测，利用日常行为本身的时间顺序学习动作语义。它通过区分全局语义与局部运动信息，避免表示完全塌缩。"
external_url: http://arxiv.org/abs/2611.18559v1
parent_observation_id: null
last_seen_at: 2026-11-16T20:27:46.445948Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.18559v1](http://arxiv.org/abs/2611.18559v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Genki Kinoshita、Ko Nishino

## 要点解读

### 这是什么
BAL 是一种面向三维人体姿态序列的自监督学习框架，在潜在空间中进行前向与后向的自回归预测，利用日常行为本身的时间顺序学习动作语义。它通过区分全局语义与局部运动信息，避免表示完全塌缩。

### 用在哪里
该方法可用于从人体动作序列中提取表示，服务于动作描述、动作预测和动作插值等任务。研究人体行为建模、时序表征学习或下游动作理解任务的人可能会关注它。

### 可以推断的
- 推测：该方法尤其适合需要同时利用动作前后文的应用场景。
- 推测：相较依赖人工增强或掩码假设的方法，BAL 的训练目标可能对相关超参数更不敏感。

## 来源摘要/节选

> Learning semantically meaningful human movement representations from 3D pose sequences is essential for human behavior modeling. Existing self-supervised methods derive supervision from artificial assumptions, e.g., invariance to augmentation within a certain range or recoverability of masked regions at a certain temporal scale, introducing heuristic hyperparameters that make the learned semantics sensitive to their settings. We propose BAL, a self-supervised framework that instead exploits supervision intrinsic to human movement: the natural ordering structure of everyday behavior. BAL autoregressively predicts in a semantically abstract latent space, analogous to how humans anticipate others' actions rather than their precise joint configurations. Bidirectional autoregressive prediction, both forward and backward in time, fully leverages these ordering constraints while enabling representation extraction using both past and future context at inference. To suppress representation collapse, BAL decomposes each prediction target into a global component capturing sequence-level semantics and a local component capturing context-independent movement. We prove that the local targets retain nontrivial angular diversity unless the representations are completely collapsed, preserving a meaningful training signal. Experiments on large-scale datasets demonstrate that BAL's representations are highly effective for motion captioning, forecasting, and interpolation, outperforming baselines on most evaluation metrics.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。