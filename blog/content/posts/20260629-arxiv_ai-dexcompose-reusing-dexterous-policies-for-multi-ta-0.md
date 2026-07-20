---
title: 'DexCompose: Reusing Dexterous Policies for Multi-Task Manipulation with a
  Single Hand'
date: 2026-06-29 23:10:48+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.28323v1
aliases:
- /posts/20260630-arxiv_ai-dexcompose-reusing-dexterous-policies-for-multi-ta-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:fc5d3c6f774b4c0cf70f18909b231a0fecaac1109f1085a5cbda6ae49fd05cff
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:30:14.398876Z'
source_capture_sha256: sha256:1d0e35bc489f7b476c965132a2e74285c480b9f9233e4fea5970e21eff19ec09
source_capture_chars_original: 1427
source_publication_excerpt_chars: 1427
observation_id: obs_5fead5d1d02d3d8d64b7f5bbb41eaf687a70d60582eede2c3d621db1e94c413c
revision_id: rev_62471c55e9c2b230a2f4ece990889c6b6aa66bde65b8cee91c17fb4043e8bdaf
event_id: evt_763c5098549d1ea93c616f10307bc6970805c1a96fa53adafa1747fd9d6ba203
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.28323v1](<https://arxiv.org/abs/2606.28323v1>)
- **作者**: Dihong Huang, Zhenyu Wei, Zhuxiu Xu, Yunchao Yao, Sikai Li, Mingyu Ding
- **分类**: cs.RO
- **论文时间**: 2026-06-26T17:59:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.28323v1.pdf](<https://arxiv.org/pdf/2606.28323v1.pdf>)

## 来源摘要/节选

> Dexterous manipulation policies can solve individual skills, but composing them to perform multiple tasks with a single hand remains challenging. Adding a new task on top of an existing manipulation skill often imposes conflicting demands on overlapping fingers and contact modes, causing destructive interference between preserving an existing manipulation outcome and executing a new one. We propose DexCompose, a role-aware residual composition framework that reuses pretrained dexterous policies for multi-task manipulation through explicit finger-level action ownership. Given two pretrained full-hand policies, DexCompose first collects successful post-task states from the first skill and performs release tests over candidate finger masks to identify which fingers are necessary for maintaining the established skill state. It then trains two asymmetric residual modules: a bounded residual stabilizer for task preservation, and a context-aware residual that adapts the frozen downstream policy only within the action subspace assigned to the new task. We evaluate the framework on 16 composite dexterous manipulation tasks spanning four object-retention skills and four downstream interactions. DexCompose achieves a 77.4% average composite success rate, demonstrating that structural action ownership with dual residuals offers a promising direction for composing dexterous skills beyond conventional policy chaining.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
