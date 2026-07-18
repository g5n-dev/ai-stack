---
title: Spiking Layer-Adaptive Magnitude-based Pruning
date: 2026-03-17 03:25:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.14946v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:83defec705c1d171993b7f4938ac496b5a4fdb16c4fd78fa7ff6ec6b93086c69
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 46
captured_at: '2026-07-18T04:28:41.690884Z'
source_capture_sha256: sha256:4af7df3b0eceab687a8bf38a1e616ae1f85ef6cb24750db4d2f547c158a7e72d
source_capture_chars_original: 1277
source_publication_excerpt_chars: 1277
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.14946v1](<https://arxiv.org/abs/2603.14946v1>)
- **作者**: Junqiao Wang, Zhehang Ye, Yuqi Ouyang
- **分类**: cs.LG
- **论文时间**: 2026-03-16T07:55:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.14946v1.pdf](<https://arxiv.org/pdf/2603.14946v1.pdf>)

## 来源摘要/节选

> Spiking Neural Networks \(SNNs\) provide energy-efficient computation but their deployment is constrained by dense connectivity and high spiking operation costs. Existing magnitude-based pruning strategies, when naively applied to SNNs, fail to account for temporal accumulation, non-uniform timestep contributions, and membrane stability, often leading to severe performance degradation. This paper proposes Spiking Layer-Adaptive Magnitude-based Pruning \(SLAMP\), a theory-guided pruning framework that generalizes layer-adaptive magnitude pruning to temporal SNNs by explicitly controlling worst-case output distortion across layers and timesteps. SLAMP formulates sparsity allocation as a temporal distortion-constrained optimization problem, yielding time-aware layer importance scores that reduce to conventional layer-adaptive pruning in single-timestep limit. An efficient two-stage procedure is derived, combining temporal score estimation, global sparsity allocation, and magnitude pruning with retraining for stability recovery. Experiments on CIFAR10, CIFAR100, and the event-based CIFAR10-DVS datasets demonstrate that SLAMP achieves substantial connectivity and spiking operation reductions while preserving accuracy, enabling efficient and deployable SNN inference.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
