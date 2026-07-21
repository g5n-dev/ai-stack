---
title: 'SpatialEvo: Self-Evolving Spatial Intelligence via Deterministic Geometric
  Environments'
date: 2026-04-16 23:27:45+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2604.14144v1
aliases:
- /posts/20260417-arxiv_ai-spatialevo-self-evolving-spatial-intelligence-via--0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7770ad1671d06953f037d0640703b46cf2a088ce555be91d64262ef0bf18994f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
captured_at: '2026-07-18T04:29:12.103286Z'
source_capture_sha256: sha256:b87534ae8fbf5aaac125e41db7c3bfaafa0772197142e4ecff2f95d7f17f1d87
source_capture_chars_original: 1669
source_publication_excerpt_chars: 1669
observation_id: obs_86ec6f370f871d0c738d159115f8f691207d7511d6ef21b9b5297ad1f2b3768f
revision_id: rev_11192207200e485d3cf58ef5c79b2a955e2dbcbd16edddbae8eb4e582b769f0f
event_id: evt_c906f9c677b41b2e6d7a6e385522e696a6fa7f78a9646b0bda181ad963951892
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-04-16T06:34:21Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2604.14144v1](<https://arxiv.org/abs/2604.14144v1>)
- **作者**: Dinging Li, Yingxiu Zhao, Xinrui Cheng, Kangheng Lin, Hongbo Peng, Hongxing Li, Zixuan Wang, Yuhong Dai, Haodong Li, Jia Wang, Yukang Shi, Liang Zhao, Jianjian Sun, Zheng Ge, Xiangyu Zhang, Weiming Lu, Jun Xiao, Yueting Zhuang, Yongliang Shen
- **分类**: cs.CV
- **论文时间**: 2026-04-15T17:59:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2604.14144v1.pdf](<https://arxiv.org/pdf/2604.14144v1.pdf>)

## 来源摘要/节选

> Spatial reasoning over three-dimensional scenes is a core capability for embodied intelligence, yet continuous model improvement remains bottlenecked by the cost of geometric annotation. The self-evolving paradigm offers a promising path, but its reliance on model consensus to construct pseudo-labels causes training to reinforce rather than correct the model's own geometric errors. We identify a property unique to 3D spatial reasoning that circumvents this limitation: ground truth is a deterministic consequence of the underlying geometry, computable exactly from point clouds and camera poses without any model involvement. Building on this insight, we present SpatialEvo, a self-evolving framework for 3D spatial reasoning, centered on the Deterministic Geometric Environment \(DGE\). The DGE formalizes 16 spatial reasoning task categories under explicit geometric validation rules and converts unannotated 3D scenes into zero-noise interactive oracles, replacing model consensus with objective physical feedback. A single shared-parameter policy co-evolves across questioner and solver roles under DGE constraints: the questioner generates physically valid spatial questions grounded in scene observations, while the solver derives precise answers against DGE-verified ground truth. A task-adaptive scheduler endogenously concentrates training on the model's weakest categories, producing a dynamic curriculum without manual design. Experiments across nine benchmarks demonstrate that SpatialEvo achieves the highest average score at both 3B and 7B scales, with consistent gains on spatial reasoning benchmarks and no degradation on general visual understanding.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
