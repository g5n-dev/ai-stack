---
title: 'From Buffers to Registers: Unlocking Fine-Grained FlashAttention with Hybrid-Bonded
  3D NPU Co-Design'
date: 2026-02-12 02:48:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.11016v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:467ad78816cd711b7bde4131eb8992d90df3eb42d96e5ddb2e0c7c006d41ea50
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 100
captured_at: '2026-07-18T04:14:55.115056Z'
source_capture_sha256: sha256:b49991e15edef3d37009c9066d47b716d502eed50dde154ca227ff4cb6ccbadf
source_capture_chars_original: 1328
source_publication_excerpt_chars: 1328
observation_id: obs_eb791c68cccacaada598614f76deb02c7a42b1cf3e377c1a07b407fad2a5fae2
revision_id: rev_6132e2506eab1b8290c428da941e08b2ff28dc77165a9f30989ae61d360906fc
event_id: evt_b6612c95c8dcb0c1c517792df6b106b9e2ca7ed7d7d7877247c8c49c622499fa
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-12T03:43:06Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11016v1](<https://arxiv.org/abs/2602.11016v1>)
- **作者**: Jinxin Yu, Yudong Pan, Mengdi Wang, Huawei Li, Yinhe Han, Xiaowei Li, Ying Wang
- **分类**: cs.AR
- **论文时间**: 2026-02-11T16:40:34Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11016v1.pdf](<https://arxiv.org/pdf/2602.11016v1.pdf>)

## 来源摘要/节选

> Transformer-based models dominate modern AI workloads but exacerbate memory bottlenecks due to their quadratic attention complexity and ever-growing model sizes. Existing accelerators, such as Groq and Cerebras, mitigate off-chip traffic with large on-chip caches, while algorithmic innovations such as FlashAttention fuse operators to avoid materializing large attention matrices. However, as off-chip traffic decreases, our measurements show that on-chip SRAM accesses account for over 60% of energy in long-sequence workloads, making cache access the new bottleneck. We propose 3D-Flow, a hybrid-bonded, 3D-stacked spatial accelerator that enables register-to-register communication across vertically partitioned PE tiers. Unlike 2D multi-array architectures limited by NoC-based router-to-router transfers, 3D-Flow leverages sub-10 um vertical TSVs to sustain cycle-level operator pipelining with minimal overhead. On top of this architecture, we design 3D-FlashAttention, a fine-grained scheduling method that balances latency across tiers, forming a bubble-free vertical dataflow without on-chip SRAM roundtrips. Evaluations on Transformer workloads \(OPT and QWEN models\) show that our 3D spatial accelerator reduces 46-93% energy consumption and achieves 1.4x-7.6x speedups compared to state-of-the-art 2D and 3D designs.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
