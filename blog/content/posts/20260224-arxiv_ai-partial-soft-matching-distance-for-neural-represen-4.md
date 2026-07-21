---
title: Partial Soft-Matching Distance for Neural Representational Comparison with
  Partial Unit Correspondence
date: 2026-02-24 03:30:14+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.19331v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:68b760f6c80e9a15e5f25afdf9b9ff09315bdd16b5aa7021974fe4a84832f97d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 102
captured_at: '2026-07-18T04:16:34.952314Z'
source_capture_sha256: sha256:c20751a94ab077b342da5d2941b31f75afb3fe9487695161a37c088432c8aad3
source_capture_chars_original: 1532
source_publication_excerpt_chars: 1532
observation_id: obs_47c8530a3ea48e71114388d761f68267077acdb3db02af9d3a8b48d90609617e
revision_id: rev_8c494550012c1b3428891781fb699e59c6dffe6d9b09b8ebc4981edead7b4542
event_id: evt_26033eaf7d7ac42737651cd6778f440a877fec8695b1a1287159408584a9a488
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-24T04:27:31Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.19331v1](<https://arxiv.org/abs/2602.19331v1>)
- **作者**: Chaitanya Kapoor, Alex H. Williams, Meenakshi Khosla
- **分类**: cs.LG
- **论文时间**: 2026-02-22T20:31:35Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.19331v1.pdf](<https://arxiv.org/pdf/2602.19331v1.pdf>)

## 来源摘要/节选

> Representational similarity metrics typically force all units to be matched, making them susceptible to noise and outliers common in neural representations. We extend the soft-matching distance to a partial optimal transport setting that allows some neurons to remain unmatched, yielding rotation-sensitive but robust correspondences. This partial soft-matching distance provides theoretical advantages -- relaxing strict mass conservation while maintaining interpretable transport costs -- and practical benefits through efficient neuron ranking in terms of cross-network alignment without costly iterative recomputation. In simulations, it preserves correct matches under outliers and reliably selects the correct model in noise-corrupted identification tasks. On fMRI data, it automatically excludes low-reliability voxels and produces voxel rankings by alignment quality that closely match computationally expensive brute-force approaches. It achieves higher alignment precision across homologous brain areas than standard soft-matching, which is forced to match all units regardless of quality. In deep networks, highly matched units exhibit similar maximally exciting images, while unmatched units show divergent patterns. This ability to partition by match quality enables focused analyses, e.g., testing whether networks have privileged axes even within their most aligned subpopulations. Overall, partial soft-matching provides a principled and practical method for representational comparison under partial correspondence.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
