---
title: 'Revisiting Gradient Staleness: Evaluating Distance Metrics for Asynchronous
  Federated Learning Aggregation'
date: 2026-03-10 02:45:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.08211v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ec6ce437ea1ff10ddb8eb307890a4c774dcdbc0e96a99e3f3b4c6ba9477c2831
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 106
captured_at: '2026-07-18T04:27:35.108002Z'
source_capture_sha256: sha256:f7305f87b4dd9a15b9039270af445aadf5a314d2561bf8a27944fc9a4531386e
source_capture_chars_original: 893
source_publication_excerpt_chars: 893
observation_id: obs_3c87c0943bf2a92d26a99d4b00842efda0a264858ab38147cb2b9ee928443b74
revision_id: rev_f2e96ada356502aa74b08b35db317059b327e59b789aa9985c0c42bc520064d1
event_id: evt_46a2ef2b0412e8ec15aef400ad4dcad4917dd0d8bf8207b6c9678ef8fed841aa
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.08211v1](<https://arxiv.org/abs/2603.08211v1>)
- **作者**: Patrick Wilhelm, Odej Kao
- **分类**: cs.LG
- **论文时间**: 2026-03-09T10:40:25Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.08211v1.pdf](<https://arxiv.org/pdf/2603.08211v1.pdf>)

## 来源摘要/节选

> In asynchronous federated learning \(FL\), client devices send updates to a central server at varying times based on their computational speed, often using stale versions of the global model. This staleness can degrade the convergence and accuracy of the global model. Previous work, such as AsyncFedED, proposed an adaptive aggregation method using Euclidean distance to measure staleness. In this paper, we extend this approach by exploring alternative distance metrics to more accurately capture the effect of gradient staleness. We integrate these metrics into the aggregation process and evaluate their impact on convergence speed, model performance, and training stability under heterogeneous clients and non-IID data settings. Our results demonstrate that certain metrics lead to more robust and efficient asynchronous FL training, offering a stronger foundation for practical deployment.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
