---
title: Multi-layer Cross-Attention is Provably Optimal for Multi-modal In-context
  Learning
date: 2026-02-05 23:03:18+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.04872v1
aliases:
- /posts/20260206-arxiv_ai-multi-layer-cross-attention-is-provably-optimal-fo-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:3913ef73d02d2cfedabb8406eb578887d6a6a9b65cf266909305e31cd07dda35
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
captured_at: '2026-07-18T04:10:53.549487Z'
source_capture_sha256: sha256:4a623cf486eb5b8959f4ebda4a0261e35a5b8346bff8205c5668e89be2c71567
source_capture_chars_original: 1251
source_publication_excerpt_chars: 1251
observation_id: obs_b972bfbbc5544b10e7978d58565e2e09fa9fe1a470f4389e5120310e4999f847
revision_id: rev_04328061f3600f1b22b3f5dbe55521faf65fc23a22e487e3ee7855030f12fb7e
event_id: evt_e67b64187ecf12ecde3fa1577789a065305ef102aeeda0c54f722fc724515572
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.04872v1](<https://arxiv.org/abs/2602.04872v1>)
- **作者**: Nicholas Barnfield, Subhabrata Sen, Pragya Sur
- **分类**: stat.ML
- **论文时间**: 2026-02-04T18:57:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.04872v1.pdf](<https://arxiv.org/pdf/2602.04872v1.pdf>)

## 来源摘要/节选

> Recent progress has rapidly advanced our understanding of the mechanisms underlying in-context learning in modern attention-based neural networks. However, existing results focus exclusively on unimodal data; in contrast, the theoretical underpinnings of in-context learning for multi-modal data remain poorly understood. We introduce a mathematically tractable framework for studying multi-modal learning and explore when transformer-like architectures can recover Bayes-optimal performance in-context. To model multi-modal problems, we assume the observed data arises from a latent factor model. Our first result comprises a negative take on expressibility: we prove that single-layer, linear self-attention fails to recover the Bayes-optimal predictor uniformly over the task distribution. To address this limitation, we introduce a novel, linearized cross-attention mechanism, which we study in the regime where both the number of cross-attention layers and the context length are large. We show that this cross-attention mechanism is provably Bayes optimal when optimized using gradient flow. Our results underscore the benefits of depth for in-context learning and establish the provable utility of cross-attention for multi-modal distributions.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
