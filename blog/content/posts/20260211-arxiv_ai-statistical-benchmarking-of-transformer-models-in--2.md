---
title: Statistical benchmarking of transformer models in low signal-to-noise time-series
  forecasting
date: 2026-02-11 03:18:02+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.09869v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:852db66be7b129488cf91608ef7b8db52c8af9ddf8055d2ac38bfaeb6a11a1b8
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
captured_at: '2026-07-18T04:14:39.893621Z'
source_capture_sha256: sha256:e1bb31fe528c00a43e7b49ec03ed68b847ed901302079be02cb0b4020f6ace70
source_capture_chars_original: 1262
source_publication_excerpt_chars: 1262
observation_id: obs_702a306de49f0a1b598e12f4da0e6bedd705918ea95249aef1fdc15ab4f3538c
revision_id: rev_4c86c35a09af6f38312d95525efd6832f1bbc0b087c89faed98abf87fe295aca
event_id: evt_94f01b683f74e28c77b16fbe560b9a680eeb09ada9f5df2e4d97dcbeb34aef53
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.09869v1](<https://arxiv.org/abs/2602.09869v1>)
- **作者**: Cyril Garcia, Guillaume Remy
- **分类**: cs.LG
- **论文时间**: 2026-02-10T15:13:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.09869v1.pdf](<https://arxiv.org/pdf/2602.09869v1.pdf>)

## 来源摘要/节选

> We study the performance of transformer architectures for multivariate time-series forecasting in low-data regimes consisting of only a few years of daily observations. Using synthetically generated processes with known temporal and cross-sectional dependency structures and varying signal-to-noise ratios, we conduct bootstrapped experiments that enable direct evaluation via out-of-sample correlations with the optimal ground-truth predictor. We show that two-way attention transformers, which alternate between temporal and cross-sectional self-attention, can outperform standard baselines-Lasso, boosting methods, and fully connected multilayer perceptrons-across a wide range of settings, including low signal-to-noise regimes. We further introduce a dynamic sparsification procedure for attention matrices applied during training, and demonstrate that it becomes significantly effective in noisy environments, where the correlation between the target variable and the optimal predictor is on the order of a few percent. Analysis of the learned attention patterns reveals interpretable structure and suggests connections to sparsity-inducing regularization in classical regression, providing insight into why these models generalize effectively under noise.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
