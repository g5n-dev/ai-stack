---
title: 'PatchFormer: A Patch-Based Time Series Foundation Model with Hierarchical
  Masked Reconstruction and Cross-Domain Transfer Learning for Zero-Shot Multi-Horizon
  Forecasting'
date: 2026-01-29 22:59:16+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.20845v1
aliases:
- /posts/20260130-arxiv_ai-patchformer-a-patch-based-time-series-foundation-m-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:86da2043ce2dc491f4174e4fd39cac25496bb4a8bcc7e1493f8283af69d8e88e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 170
captured_at: '2026-07-18T04:09:34.038253Z'
source_capture_sha256: sha256:d7dfc295e4b552efda1eaae9396628ac081ccd781b9de391c37dae5b6e0e0aac
source_capture_chars_original: 1223
source_publication_excerpt_chars: 1223
observation_id: obs_ca33ace0ccd80efc9ec1219a891364955a1efdf96a28c341e62891891a8a1560
revision_id: rev_e2dc442de0820f999ecca391719808cf547847677922a134f6730c4f36537d58
event_id: evt_fb0d6534b0fbb8b692c87c24c99483fbea09f8b2c86aab35a3a4a106586b64b3
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-29T05:04:04Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.20845v1](<https://arxiv.org/abs/2601.20845v1>)
- **作者**: Olaf Yunus Laitinen Imanov, Derya Umut Kulali, Taner Yilmaz
- **分类**: cs.LG
- **论文时间**: 2026-01-28T18:45:45Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.20845v1.pdf](<https://arxiv.org/pdf/2601.20845v1.pdf>)

## 来源摘要/节选

> Time series forecasting is a fundamental problem with applications in climate, energy, healthcare, and finance. Many existing approaches require domain-specific feature engineering and substantial labeled data for each task. We introduce PatchFormer, a patch-based time series foundation model that uses hierarchical masked reconstruction for self-supervised pretraining and lightweight adapters for efficient transfer. PatchFormer segments time series into patches and learns multiscale temporal representations with learnable aggregation across temporal scales. Pretraining uses masked patch reconstruction with dynamic masking and objectives that encourage both local accuracy and global consistency, followed by cross-domain knowledge distillation. Experiments on 24 benchmark datasets spanning weather, energy, traffic, finance, and healthcare demonstrate state-of-the-art zero-shot multi-horizon forecasting, reducing mean squared error by 27.3 percent relative to strong baselines while requiring 94 percent less task-specific training data. The model exhibits near log-linear scaling with more pretraining data up to 100 billion points and processes length-512 sequences 3.8x faster than full-sequence transformers.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
