---
title: Split Federated Learning Architectures for High-Accuracy and Low-Delay Model
  Training
date: 2026-03-10 23:05:53+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.08687v1
aliases:
- /posts/20260311-arxiv_ai-split-federated-learning-architectures-for-high-ac-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:87e5c8258bc3631824a9681f4099bf74f77da7ec19406b787189ee498b1e2d91
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:27:35.108002Z'
source_capture_sha256: sha256:05eff8d7f6c1f8de4ef9c692af347825ff65de052e2f1da447fb4b30c23d7743
source_capture_chars_original: 1373
source_publication_excerpt_chars: 1373
observation_id: obs_d6ac4dd04e8f885b84f6ded2ffef1d34f9c7b20e80465ecda73983f963593732
revision_id: rev_427e1a041976fb34fa7d7cea17c5146edcb46771df07b0c453163a1bb23a783a
event_id: evt_d3b2b7d4c0ab675c81b924e4cf2d04dcf325c900576bf381ed0bcd2262734c11
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-10T06:16:07Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.08687v1](<https://arxiv.org/abs/2603.08687v1>)
- **作者**: Yiannis Papageorgiou, Yannis Thomas, Ramin Khalili, Iordanis Koutsopoulos
- **分类**: cs.LG
- **论文时间**: 2026-03-09T17:53:20Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.08687v1.pdf](<https://arxiv.org/pdf/2603.08687v1.pdf>)

## 来源摘要/节选

> Can we find a network architecture for ML model training so as to optimize training loss \(and thus, accuracy\) in Split Federated Learning \(SFL\)? And can this architecture also reduce training delay and communication overhead? While accuracy is not influenced by how we split the model in ordinary, state-of-the-art SFL, in this work we answer the questions above in the affirmative. Recent Hierarchical SFL \(HSFL\) architectures adopt a three-tier training structure consisting of clients, \(local\) aggregators, and a central server. In this architecture, the model is partitioned at two partitioning layers into three sub-models, which are executed across the three tiers. Despite their merits, HSFL architectures overlook the impact of the partitioning layers and client-to-aggregator assignments on accuracy, delay, and overhead. This work explicitly captures the impact of the partitioning layers and client-to-aggregator assignments on accuracy, delay and overhead by formulating a joint optimization problem. We prove that the problem is NP-hard and propose the first accuracy-aware heuristic algorithm that explicitly accounts for model accuracy, while remaining delay-efficient. Simulation results on public datasets show that our approach can improve accuracy by 3%, while reducing delay by 20% and overhead by 50%, compared to state-of-the-art SFL and HSFL schemes.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
