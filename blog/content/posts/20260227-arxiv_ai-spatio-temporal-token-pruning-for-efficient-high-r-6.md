---
title: Spatio-Temporal Token Pruning for Efficient High-Resolution GUI Agents
date: 2026-02-27 02:54:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23235v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:cf6536da8fb9f9dd1b6dbb1f5c95462fb06b06e9dfa54daca099899c91d64546
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:30:44.821176Z'
source_capture_sha256: sha256:4ac076fb0916a0ce436362f83d2b2dbece05e4abb8a854351c6a135f917e4bdc
source_capture_chars_original: 1435
source_publication_excerpt_chars: 1435
observation_id: obs_a63796af91100e9cea8456a2ca7e1c9da6b73bd9442631e2f2df901f8dc2dcdf
revision_id: rev_d9b6fe50dcdab961699168bf9d1d25a35457ef9a1306fdb1ddfb94fb85cb6634
event_id: evt_dc461209f8e8c75948f9a902bb683758e0bf004d08113c690b90a6b5f2ae18e0
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-27T03:55:34Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23235v1](<https://arxiv.org/abs/2602.23235v1>)
- **作者**: Zhou Xu, Bowen Zhou, Qi Wang, Shuwen Feng, Jingyu Xiao
- **分类**: cs.CV
- **论文时间**: 2026-02-26T17:12:40Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23235v1.pdf](<https://arxiv.org/pdf/2602.23235v1.pdf>)

## 来源摘要/节选

> Pure-vision GUI agents provide universal interaction capabilities but suffer from severe efficiency bottlenecks due to the massive spatiotemporal redundancy inherent in high-resolution screenshots and historical trajectories. We identify two critical misalignments in existing compression paradigms: the temporal mismatch, where uniform history encoding diverges from the agent's "fading memory" attention pattern, and the spatial topology conflict, where unstructured pruning compromises the grid integrity required for precise coordinate grounding, inducing spatial hallucinations. To address these challenges, we introduce GUIPruner, a training-free framework tailored for high-resolution GUI navigation. It synergizes Temporal-Adaptive Resolution \(TAR\), which eliminates historical redundancy via decay-based resizing, and Stratified Structure-aware Pruning \(SSP\), which prioritizes interactive foregrounds and semantic anchors while safeguarding global layout. Extensive evaluations across diverse benchmarks demonstrate that GUIPruner consistently achieves state-of-the-art performance, effectively preventing the collapse observed in large-scale models under high compression. Notably, on Qwen2-VL-2B, our method delivers a 3.4x reduction in FLOPs and a 3.3x speedup in vision encoding latency while retaining over 94% of the original performance, enabling real-time, high-precision navigation with minimal resource consumption.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
