---
title: Stabilizing Test-Time Adaptation of High-Dimensional Simulation Surrogates
  via D-Optimal Statistics
date: 2026-02-18 21:10:38+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15820v1
aliases:
- /posts/20260219-arxiv_ai-stabilizing-test-time-adaptation-of-high-dimension-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:825cea7d2400d468589c721078e5b476e5a3f41ff9bef88f55a232a5091e6d28
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 99
captured_at: '2026-07-18T04:16:00.196393Z'
source_capture_sha256: sha256:1c5917a2b6c2ee4f1f2718f1af47bfc4030549f19b90b761fb37f5bb617b52c9
source_capture_chars_original: 1126
source_publication_excerpt_chars: 1126
observation_id: obs_98ba7a696ab47f818f3921ed11d1981b637fd9df501c85982a1d13005003bc99
revision_id: rev_69cac1466336ad637fe573484686eb6d86a2d3a5448e04b546a3d273a2ae96fd
event_id: evt_843d8b7117785bb3cc1fc5649b6e5afc015e884a1ecfb50ab602ebd96ca68105
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15820v1](<https://arxiv.org/abs/2602.15820v1>)
- **作者**: Anna Zimmel, Paul Setinek, Gianluca Galletti, Johannes Brandstetter, Werner Zellinger
- **分类**: cs.LG
- **论文时间**: 2026-02-17T18:55:18Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15820v1.pdf](<https://arxiv.org/pdf/2602.15820v1.pdf>)

## 来源摘要/节选

> Machine learning surrogates are increasingly used in engineering to accelerate costly simulations, yet distribution shifts between training and deployment often cause severe performance degradation \(e.g., unseen geometries or configurations\). Test-Time Adaptation \(TTA\) can mitigate such shifts, but existing methods are largely developed for lower-dimensional classification with structured outputs and visually aligned input-output relationships, making them unstable for the high-dimensional, unstructured and regression problems common in simulation. We address this challenge by proposing a TTA framework based on storing maximally informative \(D-optimal\) statistics, which jointly enables stable adaptation and principled parameter selection at test time. When applied to pretrained simulation surrogates, our method yields up to 7% out-of-distribution improvements at negligible computational cost. To the best of our knowledge, this is the first systematic demonstration of effective TTA for high-dimensional simulation regression and generative design optimization, validated on the SIMSHIFT and EngiBench benchmarks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
