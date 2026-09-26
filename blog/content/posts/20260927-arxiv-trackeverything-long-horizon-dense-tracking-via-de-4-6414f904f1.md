---
title: "TrackEverything: Long Horizon Dense Tracking via De-Duplicating 3D Scene Representations"
date: 2026-09-27T01:12:52+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:a9d9f489a3493eac371bf0b1ec621947f29500e20585ef0e7cadd699d684dd59"
source_payload_sha256: "sha256:f50d128765666b5fd0e8cc71156a84a9210ab288d2bf9a21afbce43910e202ac"
observation_id: obs_6414f904f14454786ee7b9bc09b30daf0f72278d461bc4e3a5bdbdfbdcc6ff03
event_id: evt_342cb69dcb82128f5781e3e28f136ad5ab369f17a77a47b00b69c03e7085a55d
revision_id: rev_621c48d10c3cedc6f0787dec0e5e1ab25e9d3f376f672e453f0bdcea9d1f95f2
source_published_at: 2026-09-24T17:48:20Z
first_seen_at: 2026-09-26T17:09:38.156753Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.30222v1
parent_observation_id: null
last_seen_at: 2026-09-26T17:09:38.156753Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30222v1](http://arxiv.org/abs/2609.30222v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Ayush Jain、Sreeharsha Paruchuri、Ishita Gupta 等

## 来源摘要/节选

> Existing point tracking models face a fundamental tradeoff: they can either track a sparse set of query points over long horizons, or track all points across only short clips. We introduce TrackEverything, a 3D point tracker that breaks this trade-off by representing videos as persistent 3D scene tracks in world coordinates. Grounded in the insight that videos are 2D projections of an underlying 3D world, TrackEverything decouples model complexity from video duration, allowing it to scale with unique physical scene geometry instead. Our approach introduces three key innovations. First, we employ a voxelization-based de-duplication mechanism at sliding-window boundaries to merge co-located tracks, preventing repeated observations of the same surface from redundantly accumulating. Second, we decompose tracking into an endpoint refiner that predicts each point's destination and static-versus-dynamic classification, followed by a lightweight trajectory refiner that decodes dense trajectories exclusively for dynamic points. Third, we propose 3D WAFT, replacing memory-prohibitive 4D correlation volumes with efficient feature sampling in the scene cloud. To the best of our knowledge, TrackEverything is the first 3D tracker capable of tracking all visible points across videos exceeding 1000 frames within 40 GB of GPU memory. On TAPVid-3D, TrackEverything outperforms all open-source all-frame dense 3D trackers by more than 20% APD on short clips, while remaining competitive with state-of-the-art sparse trackers on long sequences, despite tracking far more points.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。