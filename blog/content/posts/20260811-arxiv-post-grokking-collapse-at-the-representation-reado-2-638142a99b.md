---
title: "Post-Grokking Collapse at the Representation-Readout Interface in Muon-Trained Transformers"
date: 2026-08-11T03:20:05+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:2f142080ff2d9d74fa528e8c03da9a972eded6199a943806bfc6f7ea87a71b7d"
source_payload_sha256: "sha256:07100d8814d985ae278f772e809646d85c6dface36c3f11cc122d7130309b7ca"
observation_id: obs_638142a99bbdf7c0eda4c1e291b1753e87717cdb6420d7a7cce94658abbee61b
event_id: evt_be35c3035da3276dbe692459a9df475646e4338e57a2c5c609967c73075bb7d3
revision_id: rev_bc2a1f8662c9ec71c0f1c63739e2c9e33715fe054efd0fa5925f27e993c67848
source_published_at: 2026-08-07T17:21:49Z
first_seen_at: 2026-08-10T21:02:06.430076Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 91
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.07436v1
parent_observation_id: null
last_seen_at: 2026-08-10T19:16:32.604111Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07436v1](http://arxiv.org/abs/2608.07436v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Ali Janati、Kaoutar El Maghraoui、Andrei Kanavalau 等

## 来源摘要/节选

> Under the standard split, Muon gets hidden matrices and AdamW embeddings/output head. Muon groks modular addition faster, but its solutions do not hold. All nine configurations on $(a+b) \bmod 113$ grok and later lose generalization. Across five seeds the selected AdamW reference falls below threshold on four, reaching 27.59%. Instability persists across two moduli, two widths, two training fractions, subtraction, and depth.
> The failure arises at the representation-readout interface, identified only jointly up to an invertible map unselected by the loss. After solving the training set, the gradient falls to order $10^{-6}$ and the optimizers respond differently: step-size elasticity is -0.03 for Muon versus +1.5 for AdamW, and the Muon group moves 8.0 times faster per parameter. From bit-identical states, freezing either group prevents failure. Freezing embeddings/readout removes it in five runs over 451,400 post-grokking steps and five paired seeds: unfrozen arms record 137-321 sub-threshold evaluations, frozen arms none. Removing Muon's normalization and orthogonalization is no substitute: it collapses representation from 326 effective conjugate pairs to 4, shows no recurrent collapse, and fails terminally.
> Fourier filtering separates circuit failure from masking. Across 43 checkpoints over five seeds and three regimes, the task-aligned family reaches exactly 100% alone. In circuit failure it no longer solves the task; in masking it remains perfect while the full model reaches 45.85%, giving a positive margin on every example, including errors, but being outvoted by a near-equal adversarial remainder. Rescaling it restores 99.9%; grokking is the same condition resolving upward. The task selects the family, swapping $(k,k)$ for $(k,-k)$ under subtraction. Across an abrupt collapse, standard Fourier support is unchanged and the power-distribution cosine remains 0.9899.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。