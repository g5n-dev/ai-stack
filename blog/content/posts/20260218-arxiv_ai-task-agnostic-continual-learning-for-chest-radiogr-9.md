---
title: Task-Agnostic Continual Learning for Chest Radiograph Classification
date: 2026-02-18 21:10:38+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15811v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f53113f5235cb4ed0a05eeb7703c690767aad7551e16511046c769669ea2f41f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
captured_at: '2026-07-18T04:16:00.196393Z'
source_capture_sha256: sha256:ac97841cca244cc262e78be97401d2b540974e5eb3ac4811998d1f91932c6c76
source_capture_chars_original: 1613
source_publication_excerpt_chars: 1613
observation_id: obs_52add4693741fedcaacdfa98a44d42b68df9ecbd81cc59e7658ac73123121729
revision_id: rev_43c1b589f4c74278c8a5e53e53dc089ae1997c3d939ae9542de971d72a21ae78
event_id: evt_c71f3f492adda612b45451f75ca01e1a2a8f47e1728036c1eee1b4e3aa62506b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15811v1](<https://arxiv.org/abs/2602.15811v1>)
- **作者**: Muthu Subash Kavitha, Anas Zafar, Amgad Muneer, Jia Wu
- **分类**: cs.CV
- **论文时间**: 2026-02-17T18:47:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15811v1.pdf](<https://arxiv.org/pdf/2602.15811v1.pdf>)

## 来源摘要/节选

> Clinical deployment of chest radiograph classifiers requires models that can be updated as new datasets become available without retraining on previously ob- served data or degrading validated performance. We study, for the first time, a task-incremental continual learning setting for chest radiograph classification, in which heterogeneous chest X-ray datasets arrive sequentially and task identifiers are unavailable at inference. We propose a continual adapter-based routing learning strategy for Chest X-rays \(CARL-XRay\) that maintains a fixed high-capacity backbone and incrementally allocates lightweight task-specific adapters and classifier heads. A latent task selector operates on task-adapted features and leverages both current and historical context preserved through compact prototypes and feature-level experience replay. This design supports stable task identification and adaptation across sequential updates while avoiding raw-image storage. Experiments on large-scale public chest radiograph datasets demonstrate robust performance retention and reliable task-aware inference under continual dataset ingestion. CARL-XRay outperforms joint training under task-unknown deployment, achieving higher routing accuracy \(75.0\\% vs.\\ 62.5\\%\), while maintaining competitive diagnostic performance with AUROC of 0.74 in the oracle setting with ground-truth task identity and 0.75 under task-unknown inference, using significantly fewer trainable parameters. Finally, the proposed framework provides a practical alternative to joint training and repeated full retraining in continual clinical deployment.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
