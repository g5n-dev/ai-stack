---
title: Symbol-Equivariant Recurrent Reasoning Models
date: 2026-03-03 23:28:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.02193v1
aliases:
- /posts/20260304-arxiv_ai-symbol-equivariant-recurrent-reasoning-models-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:691006e923b247266f20c50f48b52d3fed81b276f386bb5bd9357a5e08934b19
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 45
captured_at: '2026-07-18T04:26:38.668400Z'
source_capture_sha256: sha256:2febe0a2ab69ff58809658b93d6bdb66c97b8eccb0349b44162d26b2cd790606
source_capture_chars_original: 1116
source_publication_excerpt_chars: 1116
observation_id: obs_a375cd123d9cacbf076532f7c68b3658873d2c5cc1a8b9bb9c0c9ec95aec482f
revision_id: rev_6c9efedeb0ec9231d9e7cde2d46e0417960ed839e586828e2ec58251ccdd694f
event_id: evt_0398ad1d2137029ab2a5073df06e47f2cae9d2fa61dafa591d03baacfb8d4c1e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-03T06:15:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02193v1](<https://arxiv.org/abs/2603.02193v1>)
- **作者**: Richard Freinschlag, Timo Bertram, Erich Kobler, Andreas Mayr, Günter Klambauer
- **分类**: cs.LG
- **论文时间**: 2026-03-02T18:53:55Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02193v1.pdf](<https://arxiv.org/pdf/2603.02193v1.pdf>)

## 来源摘要/节选

> Reasoning problems such as Sudoku and ARC-AGI remain challenging for neural networks. The structured problem solving architecture family of Recurrent Reasoning Models \(RRMs\), including Hierarchical Reasoning Model \(HRM\) and Tiny Recursive Model \(TRM\), offer a compact alternative to large language models, but currently handle symbol symmetries only implicitly via costly data augmentation. We introduce Symbol-Equivariant Recurrent Reasoning Models \(SE-RRMs\), which enforce permutation equivariance at the architectural level through symbol-equivariant layers, guaranteeing identical solutions under symbol or color permutations. SE-RRMs outperform prior RRMs on 9x9 Sudoku and generalize from just training on 9x9 to smaller 4x4 and larger 16x16 and 25x25 instances, to which existing RRMs cannot extrapolate. On ARC-AGI-1 and ARC-AGI-2, SE-RRMs achieve competitive performance with substantially less data augmentation and only 2 million parameters, demonstrating that explicitly encoding symmetry improves the robustness and scalability of neural reasoning. Code is available at https://github.com/ml-jku/SE-RRM.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
