---
title: "WorldCrafter: Consistent Video World Model with Implicit 3D-aware Memory"
date: 2026-09-22T22:56:20+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d5f5acc5712ebaa439115f0949b008392a206601e81acea0644d36c95b0b498a"
source_payload_sha256: "sha256:8f20e0d15dfcba21e9a4a98e20610f1ef005b42d848b08d814b922c1c09bc6bf"
observation_id: obs_068d1ed02ce2c86c3095ab7835b5f7993ff5524fa0a99e9cc9b48562704f9484
event_id: evt_22b9ae2ef763417444cf19a600dbe08b5dcad44038bc31a5840739c3a68a6666
revision_id: rev_df078c6ac9bc84447b2e8f68f631529dbbdef1cc2613669bfbfd64a18a6fd21e
source_published_at: 2026-09-21T17:57:06Z
first_seen_at: 2026-09-22T14:52:40.466844Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.24984v1
parent_observation_id: null
last_seen_at: 2026-09-22T14:52:40.466844Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.24984v1](http://arxiv.org/abs/2609.24984v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Wangbo Yu、Kunhao Liu、Wenbo Hu 等

## 来源摘要/节选

> Video world models enable interactive exploration of dynamic environments, yet struggle to respect prior observations over long horizons and across viewpoints. We present WorldCrafter, a video world model that learns a camera-queryable implicit 3D-aware memory for this purpose. The key insight is to let the requested viewpoint shape how multi-view evidence is compressed into the video generator's limited token budget. Trained jointly with the video generator, a memory encoder and pose-conditioned readout module integrate historical observations into a fixed set of target view-specific tokens before denoising, without explicit depth-based correspondences. By combining this memory with recent temporal context and few-step distillation, WorldCrafter enables streaming scene exploration from a single input image or text prompt. Experiments across static and dynamic scenes show substantial gains in long-horizon consistency and camera-control accuracy while preserving visual quality during minute-scale exploration.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。