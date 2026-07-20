---
title: 'Post-Training Fairness Control: A Single-Train Framework for Dynamic Fairness
  in Recommendation'
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
external_url: https://arxiv.org/abs/2601.20848v1
aliases:
- /posts/20260130-arxiv_ai-post-training-fairness-control-a-single-train-fram-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:237dfde31c2bdd9980657645f4875842f99a4dba85e709f8c10a9504b2ff5715
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
captured_at: '2026-07-18T04:09:34.038253Z'
source_capture_sha256: sha256:efae9c51f1ca9c3b733b8d07388d2c2dce1dc3956b01bd29d545ff6d3f85758a
source_capture_chars_original: 1359
source_publication_excerpt_chars: 1359
observation_id: obs_4ac9f0a4c963ee2fbdab09a868bcd009778f83fd11fd2927ca7e03761058cd8d
revision_id: rev_f52aa04c02b699877c9b3f73ffc1801d90de63d07519c5e493e1a2db6f1267a5
event_id: evt_73f2dab0b96712c365ea2eef1235449742b02848f6e4da128beb20ccb017b449
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.20848v1](<https://arxiv.org/abs/2601.20848v1>)
- **作者**: Weixin Chen, Li Chen, Yuhan Zhao
- **分类**: cs.LG
- **论文时间**: 2026-01-28T18:48:43Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.20848v1.pdf](<https://arxiv.org/pdf/2601.20848v1.pdf>)

## 来源摘要/节选

> Despite growing efforts to mitigate unfairness in recommender systems, existing fairness-aware methods typically fix the fairness requirement at training time and provide limited post-training flexibility. However, in real-world scenarios, diverse stakeholders may demand differing fairness requirements over time, so retraining for different fairness requirements becomes prohibitive. To address this limitation, we propose Cofair, a single-train framework that enables post-training fairness control in recommendation. Specifically, Cofair introduces a shared representation layer with fairness-conditioned adapter modules to produce user embeddings specialized for varied fairness levels, along with a user-level regularization term that guarantees user-wise monotonic fairness improvements across these levels. We theoretically establish that the adversarial objective of Cofair upper bounds demographic parity and the regularization term enforces progressive fairness at user level. Comprehensive experiments on multiple datasets and backbone models demonstrate that our framework provides dynamic fairness at different levels, delivering comparable or better fairness-accuracy curves than state-of-the-art baselines, without the need to retrain for each new fairness requirement. Our code is publicly available at https://github.com/weixinchen98/Cofair.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
