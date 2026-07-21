---
title: Differentiable Zero-One Loss via Hypersimplex Projections
date: 2026-02-27 23:20:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23336v1
aliases:
- /posts/20260228-arxiv_ai-differentiable-zero-one-loss-via-hypersimplex-proj-7/
- /posts/20260301-arxiv_ai-differentiable-zero-one-loss-via-hypersimplex-proj-7/
- /posts/20260302-arxiv_ai-differentiable-zero-one-loss-via-hypersimplex-proj-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2f397dcc03eef7d1d75bb95298fa46171eab39660d7d9e11f31a65440eddd30b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
captured_at: '2026-07-18T04:30:37.182965Z'
source_capture_sha256: sha256:ec2ba68f16c926ed2d1b79a151ba29e9b81462cd6b5082315d8d60b5b95355b7
source_capture_chars_original: 1079
source_publication_excerpt_chars: 1079
observation_id: obs_48954559d81b44db3deded6662a10fb46f685630baca5fb01a201f654fe28738
revision_id: rev_a0c775ff6e3785532c6e111d2d6e771cf07231bf3d7383665becd4e352eb62c4
event_id: evt_c1d663e7c1f79f2f07f720eefbf79c2a2e3eab70f9368cc49b87633b058d898e
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-27T06:11:48Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23336v1](<https://arxiv.org/abs/2602.23336v1>)
- **作者**: Camilo Gomez, Pengyang Wang, Liansheng Tang
- **分类**: cs.LG
- **论文时间**: 2026-02-26T18:41:31Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23336v1.pdf](<https://arxiv.org/pdf/2602.23336v1.pdf>)

## 来源摘要/节选

> Recent advances in machine learning have emphasized the integration of structured optimization components into end-to-end differentiable models, enabling richer inductive biases and tighter alignment with task-specific objectives. In this work, we introduce a novel differentiable approximation to the zero-one loss-long considered the gold standard for classification performance, yet incompatible with gradient-based optimization due to its non-differentiability. Our method constructs a smooth, order-preserving projection onto the n,k-dimensional hypersimplex through a constrained optimization framework, leading to a new operator we term Soft-Binary-Argmax. After deriving its mathematical properties, we show how its Jacobian can be efficiently computed and integrated into binary and multiclass learning systems. Empirically, our approach achieves significant improvements in generalization under large-batch training by imposing geometric consistency constraints on the output logits, thereby narrowing the performance gap traditionally observed in large-batch training.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
