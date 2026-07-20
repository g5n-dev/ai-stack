---
title: 'LoGeR: Long-Context Geometric Reconstruction with Hybrid Memory'
date: 2026-03-04 22:47:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.03269v1
aliases:
- /posts/20260305-arxiv_ai-loger-long-context-geometric-reconstruction-with-h-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:fcc9d338f3dfab30d9e370ab5af62efbcd645118f4130af01d889ea4b1d75d29
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
captured_at: '2026-07-18T04:26:46.139217Z'
source_capture_sha256: sha256:1568c600af99307ab0b37f14b85d9b8dc9ba8deadb07592e9868838143d4d9f3
source_capture_chars_original: 1375
source_publication_excerpt_chars: 1375
observation_id: obs_6fac2dc4c22df69801e74e025c6d4918685f826033c921824f6940b4d020452d
revision_id: rev_c3dec40bfbfc93c0991f3a64b1a9c3396e225990bf2b55b216b1a1f9bbf7592c
event_id: evt_b524dee7dd1e9be93bbfdf20661db238a1022d25a7ed6b16716e49dd7365d63b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03269v1](<https://arxiv.org/abs/2603.03269v1>)
- **作者**: Junyi Zhang, Charles Herrmann, Junhwa Hur, Chen Sun, Ming-Hsuan Yang, Forrester Cole, Trevor Darrell, Deqing Sun
- **分类**: cs.CV
- **论文时间**: 2026-03-03T18:55:37Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03269v1.pdf](<https://arxiv.org/pdf/2603.03269v1.pdf>)

## 来源摘要/节选

> Feedforward geometric foundation models achieve strong short-window reconstruction, yet scaling them to minutes-long videos is bottlenecked by quadratic attention complexity or limited effective memory in recurrent designs. We present LoGeR \(Long-context Geometric Reconstruction\), a novel architecture that scales dense 3D reconstruction to extremely long sequences without post-optimization. LoGeR processes video streams in chunks, leveraging strong bidirectional priors for high-fidelity intra-chunk reasoning. To manage the critical challenge of coherence across chunk boundaries, we propose a learning-based hybrid memory module. This dual-component system combines a parametric Test-Time Training \(TTT\) memory to anchor the global coordinate frame and prevent scale drift, alongside a non-parametric Sliding Window Attention \(SWA\) mechanism to preserve uncompressed context for high-precision adjacent alignment. Remarkably, this memory architecture enables LoGeR to be trained on sequences of 128 frames, and generalize up to thousands of frames during inference. Evaluated across standard benchmarks and a newly repurposed VBR dataset with sequences of up to 19k frames, LoGeR substantially outperforms prior state-of-the-art feedforward methods--reducing ATE on KITTI by over 74%--and achieves robust, globally consistent reconstruction over unprecedented horizons.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
