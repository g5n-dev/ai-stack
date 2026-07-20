---
title: 'Routing the Lottery: Adaptive Subnetworks for Heterogeneous Data'
date: 2026-01-30 23:03:03+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 深度学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.22141v1
aliases:
- /posts/20260131-arxiv_ai-routing-the-lottery-adaptive-subnetworks-for-heter-8/
- /posts/20260201-arxiv_ai-routing-the-lottery-adaptive-subnetworks-for-heter-8/
- /posts/20260202-arxiv_ai-routing-the-lottery-adaptive-subnetworks-for-heter-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2361cc805ac55b1feda623d39314467459bbf8a5c90f02ff24799361a0f14626
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 64
captured_at: '2026-07-18T04:10:00.628947Z'
source_capture_sha256: sha256:4bbe8e05b43501518a3d35a4a2369592ddd1ed954524eeee33c804fac4be389b
source_capture_chars_original: 1189
source_publication_excerpt_chars: 1189
observation_id: obs_24a8bb6dad3edbef499b5f85ae91c3e005a2b1067161ff140da01552648a5915
revision_id: rev_ef8cacb7eec7dd10b6635852c0708dcc757a2b2bd7f054116e037e2570511cad
event_id: evt_113ac3187327e47afdcdb2769e535a5b535f9f032a8d7951223a7422583ca0fd
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.22141v1](<https://arxiv.org/abs/2601.22141v1>)
- **作者**: Grzegorz Stefanski, Alberto Presta, Michal Byra
- **分类**: cs.AI
- **论文时间**: 2026-01-29T18:56:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.22141v1.pdf](<https://arxiv.org/pdf/2601.22141v1.pdf>)

## 来源摘要/节选

> In pruning, the Lottery Ticket Hypothesis posits that large networks contain sparse subnetworks, or winning tickets, that can be trained in isolation to match the performance of their dense counterparts. However, most existing approaches assume a single universal winning ticket shared across all inputs, ignoring the inherent heterogeneity of real-world data. In this work, we propose Routing the Lottery \(RTL\), an adaptive pruning framework that discovers multiple specialized subnetworks, called adaptive tickets, each tailored to a class, semantic cluster, or environmental condition. Across diverse datasets and tasks, RTL consistently outperforms single- and multi-model baselines in balanced accuracy and recall, while using up to 10 times fewer parameters than independent models and exhibiting semantically aligned. Furthermore, we identify subnetwork collapse, a performance drop under aggressive pruning, and introduce a subnetwork similarity score that enables label-free diagnosis of oversparsification. Overall, our results recast pruning as a mechanism for aligning model structure with data heterogeneity, paving the way toward more modular and context-aware deep learning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
