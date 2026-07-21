---
title: 'LoST: Level of Semantics Tokenization for 3D Shapes'
date: 2026-03-19 18:55:56+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.17995v1
aliases:
- /posts/20260320-arxiv_ai-lost-level-of-semantics-tokenization-for-3d-shapes-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:326c7b3c160e20820602d500f4bd07d4e6eeb766412adfddcce833bc78686fa5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 51
captured_at: '2026-07-18T04:29:00.882647Z'
source_capture_sha256: sha256:2a6d5831622690ce21a921ea051eb6c6cce94aa7964e264bb46072680cb272a0
source_capture_chars_original: 1400
source_publication_excerpt_chars: 1400
observation_id: obs_4abd31d75c80a4fcf2866b712cca94bbaa27a0af272fd405a177a5fc3cbb3b1c
revision_id: rev_ec1de70dd04ee3f14246a70a05ab62146449970a615308c64d740cebe505bdb1
event_id: evt_fbb697e49b5fe05369465125321b33282ef74dcfaf96785ce59c636462317aff
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-19T20:50:47Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.17995v1](<https://arxiv.org/abs/2603.17995v1>)
- **作者**: Niladri Shekhar Dutt, Zifan Shi, Paul Guerrero, Chun-Hao Paul Huang, Duygu Ceylan, Niloy J. Mitra, Xuelin Chen
- **分类**: cs.CV
- **论文时间**: 2026-03-18T17:56:06Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.17995v1.pdf](<https://arxiv.org/pdf/2603.17995v1.pdf>)

## 来源摘要/节选

> Tokenization is a fundamental technique in the generative modeling of various modalities. In particular, it plays a critical role in autoregressive \(AR\) models, which have recently emerged as a compelling option for 3D generation. However, optimal tokenization of 3D shapes remains an open question. State-of-the-art \(SOTA\) methods primarily rely on geometric level-of-detail \(LoD\) hierarchies, originally designed for rendering and compression. These spatial hierarchies are often token-inefficient and lack semantic coherence for AR modeling. We propose Level-of-Semantics Tokenization \(LoST\), which orders tokens by semantic salience, such that early prefixes decode into complete, plausible shapes that possess principal semantics, while subsequent tokens refine instance-specific geometric and semantic details. To train LoST, we introduce Relational Inter-Distance Alignment \(RIDA\), a novel 3D semantic alignment loss that aligns the relational structure of the 3D shape latent space with that of the semantic DINO feature space. Experiments show that LoST achieves SOTA reconstruction, surpassing previous LoD-based 3D shape tokenizers by large margins on both geometric and semantic reconstruction metrics. Moreover, LoST achieves efficient, high-quality AR 3D generation and enables downstream tasks like semantic retrieval, while using only 0.1%-10% of the tokens needed by prior AR models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
