---
title: 'From Complex Dynamics to DynFormer: Rethinking Transformers for PDEs'
date: 2026-03-04 03:29:03+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.03112v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:eb2da08505e889fd2747c465b4a6a57ddf56fd84ad00025e1b5a6e8a21578afc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
captured_at: '2026-07-18T04:26:46.139217Z'
source_capture_sha256: sha256:0c0faca50ae61ee47c513c72f2f9275136b0f93b2abfd0a770591c2ba040333f
source_capture_chars_original: 1918
source_publication_excerpt_chars: 1918
observation_id: obs_d25ffb40a1899deb736859a57d898938d08c1a1d735df279339cc851ce51ee30
revision_id: rev_3a5120150fbe8a2c331f65cc046582c4b66c608c0604310dd5f59bf214d1024e
event_id: evt_8fea29f9107e5232c53d5d1328e5ce9f66c5d305e1810628a73304263d05cc6f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-04T04:34:10Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03112v1](<https://arxiv.org/abs/2603.03112v1>)
- **作者**: Pengyu Lai, Yixiao Chen, Dewu Yang, Rui Wang, Feng Wang, Hui Xu
- **分类**: cs.LG
- **论文时间**: 2026-03-03T15:45:09Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03112v1.pdf](<https://arxiv.org/pdf/2603.03112v1.pdf>)

## 来源摘要/节选

> Partial differential equations \(PDEs\) are fundamental for modeling complex physical systems, yet classical numerical solvers face prohibitive computational costs in high-dimensional and multi-scale regimes. While Transformer-based neural operators have emerged as powerful data-driven alternatives, they conventionally treat all discretized spatial points as uniform, independent tokens. This monolithic approach ignores the intrinsic scale separation of physical fields, applying computationally prohibitive global attention that redundantly mixes smooth large-scale dynamics with high-frequency fluctuations. Rethinking Transformers through the lens of complex dynamics, we propose DynFormer, a novel dynamics-informed neural operator. Rather than applying a uniform attention mechanism across all scales, DynFormer explicitly assigns specialized network modules to distinct physical scales. It leverages a Spectral Embedding to isolate low-frequency modes, enabling a Kronecker-structured attention mechanism to efficiently capture large-scale global interactions with reduced complexity. Concurrently, we introduce a Local-Global-Mixing transformation. This module utilizes nonlinear multiplicative frequency mixing to implicitly reconstruct the small-scale, fast-varying turbulent cascades that are slaved to the macroscopic state, without incurring the cost of global attention. Integrating these modules into a hybrid evolutionary architecture ensures robust long-term temporal stability. Extensive memory-aligned evaluations across four PDE benchmarks demonstrate that DynFormer achieves up to a 95% reduction in relative error compared to state-of-the-art baselines, while significantly reducing GPU memory consumption. Our results establish that embedding first-principles physical dynamics into Transformer architectures yields a highly scalable, theoretically grounded blueprint for PDE surrogate modeling.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
