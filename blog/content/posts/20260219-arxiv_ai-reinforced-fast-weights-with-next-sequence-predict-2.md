---
title: Reinforced Fast Weights with Next-Sequence Prediction
date: 2026-02-19 22:55:31+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.16704v1
aliases:
- /posts/20260220-arxiv_ai-reinforced-fast-weights-with-next-sequence-predict-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e9765646bafc06426a937457547849f51b1c81557fd2cb28115f5c0e40fbc3d4
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 53
captured_at: '2026-07-18T04:16:04.060671Z'
source_capture_sha256: sha256:2105ca3d6cc8bb43dd52e57957033ec31fc272f37fff4c5fc1a6d02b085c3d71
source_capture_chars_original: 1484
source_publication_excerpt_chars: 1484
observation_id: obs_e0a4f1f038fcde73ceee005dc5a7c4025705ee761a01734930f51039f46346f4
revision_id: rev_b09d7048b147593afef862853de3ac66fe748301cd5fec24e8c22ca180ee405f
event_id: evt_ef8dfe1ce5dc7269811b27ef72f7e1b42117684cc6c9952318155444d25911b7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-19T06:45:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.16704v1](<https://arxiv.org/abs/2602.16704v1>)
- **作者**: Hee Seung Hwang, Xindi Wu, Sanghyuk Chun, Olga Russakovsky
- **分类**: cs.CL
- **论文时间**: 2026-02-18T18:53:18Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.16704v1.pdf](<https://arxiv.org/pdf/2602.16704v1.pdf>)

## 来源摘要/节选

> Fast weight architectures offer a promising alternative to attention-based transformers for long-context modeling by maintaining constant memory overhead regardless of context length. However, their potential is limited by the next-token prediction \(NTP\) training paradigm. NTP optimizes single-token predictions and ignores semantic coherence across multiple tokens following a prefix. Consequently, fast weight models, which dynamically update their parameters to store contextual information, learn suboptimal representations that fail to capture long-range dependencies. We introduce REFINE \(Reinforced Fast weIghts with Next sEquence prediction\), a reinforcement learning framework that trains fast weight models under the next-sequence prediction \(NSP\) objective. REFINE selects informative token positions based on prediction entropy, generates multi-token rollouts, assigns self-supervised sequence-level rewards, and optimizes the model with group relative policy optimization \(GRPO\). REFINE is applicable throughout the training lifecycle of pre-trained language models: mid-training, post-training, and test-time training. Our experiments on LaCT-760M and DeltaNet-1.3B demonstrate that REFINE consistently outperforms supervised fine-tuning with NTP across needle-in-a-haystack retrieval, long-context question answering, and diverse tasks in LongBench. REFINE provides an effective and versatile framework for improving long-context modeling in fast weight architectures.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
