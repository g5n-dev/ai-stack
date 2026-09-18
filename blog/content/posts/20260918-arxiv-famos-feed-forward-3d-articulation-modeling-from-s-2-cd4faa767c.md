---
title: "FAMOS: Feed-Forward 3D Articulation Modeling from Sparse Observations"
date: 2026-09-18T17:47:59+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:66a922c5ee3001b9d5b01fa4ef10f86dd73b472c7740792c3dd721bc44a662c2"
source_payload_sha256: "sha256:c2d298fd1c06a6d301361c4ca31ed5a0c7f44afc21d75886b282e25f9abf08b2"
observation_id: obs_cd4faa767c53c20eaaa675f777a6d7255871fc44ddd6a2e927ef1c429ce323f8
event_id: evt_9265be04aaa44c156395d3ca10d627fb16bd2f508ea9debf41fdb926d4ce355e
revision_id: rev_0bdcd4a3ece538a14b23cad85c3027781f40b7737b4c516e3deb4aa47cd82151
source_published_at: 2026-09-17T17:59:40Z
first_seen_at: 2026-09-18T09:45:25.637138Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.20817v1
parent_observation_id: null
last_seen_at: 2026-09-18T09:45:25.637138Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.20817v1](http://arxiv.org/abs/2609.20817v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Kevin Qu、Tao Sun、Massimiliano Viola 等

## 来源摘要/节选

> Modeling articulated objects from sparse monocular views is challenging because each observation reveals only partial geometry and motion evidence. Most feed-forward methods infer articulation from a single observation and therefore rely heavily on learned category-level shape priors. We present FAMOS, a feed-forward model that predicts movable-part segmentation and joint parameters from a sparse, unordered set of partial point clouds. Our model jointly reasons over multiple observations and naturally supports a variable number of inputs, including a single view. To aggregate articulation cues across observations, we introduce a Multi-state Articulation Transformer with alternating state-wise and global attention. We further propose an observed articulation span objective that supervises the motion range each part exhibits across the input observations, encouraging the model to leverage the full observation set. To overcome the limited scale and diversity of existing datasets, we introduce a procedural data generator that synthesizes self-annotated assets during training. Experiments on PartNet-Mobility, ACD, and ArtiCraft-10K demonstrate consistent improvements over both feed-forward and optimization-based baselines. Project page: https://kevinqu7.github.io/famos

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。