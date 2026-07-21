---
title: 'MM-TS: Multi-Modal Temperature and Margin Schedules for Contrastive Learning
  with Long-Tail Data'
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
external_url: https://arxiv.org/abs/2603.08202v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6754eab04464ed3c52b7e73f1847726e514002951e543fe3e2428a75c859b668
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:27:35.108002Z'
source_capture_sha256: sha256:e150880088d0ab5b32ef78337d104a7650227ffeb7e62a438721ec929694a739
source_capture_chars_original: 1522
source_publication_excerpt_chars: 1522
observation_id: obs_d4f040931d01a1af7266dc07164722b531508f21797ea012704babd1ab5e3e94
revision_id: rev_4543161dd2d0207ce38ae13f439e7924a70224fe9da3b0bb63e2f7675266aed9
event_id: evt_d70c65ded39b77967f8a8aecdb3964db0ec27d790e5d7aef4f82e4258006712b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.08202v1](<https://arxiv.org/abs/2603.08202v1>)
- **作者**: Siarhei Sheludzko, Dhimitrios Duka, Bernt Schiele, Hilde Kuehne, Anna Kukleva
- **分类**: cs.CV
- **论文时间**: 2026-03-09T10:29:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.08202v1.pdf](<https://arxiv.org/pdf/2603.08202v1.pdf>)

## 来源摘要/节选

> Contrastive learning has become a fundamental approach in both uni-modal and multi-modal frameworks. This learning paradigm pulls positive pairs of samples closer while pushing negatives apart. In the uni-modal setting \(e.g., image-based learning\), previous research has shown that the strength of these forces can be controlled through the temperature parameter. In this work, we propose Multi-Modal Temperature and Margin Schedules \(MM-TS\), extending the concept of uni-modal temperature scheduling to multi-modal contrastive learning. Our method dynamically adjusts the temperature in the contrastive loss during training, modulating the attraction and repulsion forces in the multi-modal setting. Additionally, recognizing that standard multi-modal datasets often follow imbalanced, long-tail distributions, we adapt the temperature based on the local distribution of each training sample. Specifically, samples from dense clusters are assigned a higher temperature to better preserve their semantic structure. Furthermore, we demonstrate that temperature scheduling can be effectively integrated within a max-margin framework, thereby unifying the two predominant approaches in multi-modal contrastive learning: InfoNCE loss and max-margin objective. We evaluate our approach on four widely used image- and video-language datasets, Flickr30K, MSCOCO, EPIC-KITCHENS-100, and YouCook2, and show that our dynamic temperature and margin schedules improve performance and lead to new state-of-the-art results in the field.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
