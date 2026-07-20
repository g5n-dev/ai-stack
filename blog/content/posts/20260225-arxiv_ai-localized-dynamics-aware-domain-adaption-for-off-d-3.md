---
title: Localized Dynamics-Aware Domain Adaption for Off-Dynamics Offline Reinforcement
  Learning
date: 2026-02-25 02:57:16+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.21072v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:9b5eb479cde201cabc15909b495ef2264a5027e193fb29e483f7731d5492f74c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
captured_at: '2026-07-18T04:16:49.996029Z'
source_capture_sha256: sha256:bc563686ac3420df72f0df2ed1254cffe80e7660d191f972e942801f90b4e2ed
source_capture_chars_original: 1240
source_publication_excerpt_chars: 1240
observation_id: obs_7d78a499678d924c73a28cd3022ec6959c532291c5269b6b6fc2e33028f60701
revision_id: rev_a96bb40e3a36079930b85291cd6d6d30f2add193897ddd70e00c1b3764000ea3
event_id: evt_32f529cf0fce434eb76fe439ad01409f8cab0dede6ca3b1a55e7f1f3ff23cfab
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21072v1](<https://arxiv.org/abs/2602.21072v1>)
- **作者**: Zhangjie Xia, Yu Yang, Pan Xu
- **分类**: cs.LG
- **论文时间**: 2026-02-24T16:32:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21072v1.pdf](<https://arxiv.org/pdf/2602.21072v1.pdf>)

## 来源摘要/节选

> Off-dynamics offline reinforcement learning \(RL\) aims to learn a policy for a target domain using limited target data and abundant source data collected under different transition dynamics. Existing methods typically address dynamics mismatch either globally over the state space or via pointwise data filtering; these approaches can miss localized cross-domain similarities or incur high computational cost. We propose Localized Dynamics-Aware Domain Adaptation \(LoDADA\), which exploits localized dynamics mismatch to better reuse source data. LoDADA clusters transitions from source and target datasets and estimates cluster-level dynamics discrepancy via domain discrimination. Source transitions from clusters with small discrepancy are retained, while those from clusters with large discrepancy are filtered out. This yields a fine-grained and scalable data selection strategy that avoids overly coarse global assumptions and expensive per-sample filtering. We provide theoretical insights and extensive experiments across environments with diverse global and local dynamics shifts. Results show that LoDADA consistently outperforms state-of-the-art off-dynamics offline RL methods by better leveraging localized distribution mismatch.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
