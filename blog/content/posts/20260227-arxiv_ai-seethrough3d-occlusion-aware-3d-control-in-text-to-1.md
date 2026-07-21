---
title: 'SeeThrough3D: Occlusion Aware 3D Control in Text-to-Image Generation'
date: 2026-02-27 23:20:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23359v1
aliases:
- /posts/20260228-arxiv_ai-seethrough3d-occlusion-aware-3d-control-in-text-to-1/
- /posts/20260301-arxiv_ai-seethrough3d-occlusion-aware-3d-control-in-text-to-1/
- /posts/20260302-arxiv_ai-seethrough3d-occlusion-aware-3d-control-in-text-to-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1b47d9011c6fb4d78bd103a8bc708c3d5a477d94f2e7d89fde0e8bb1a38011e1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
captured_at: '2026-07-18T04:30:44.821176Z'
source_capture_sha256: sha256:69994bdbd38e30865d338d97f5720824477e7d31e4fdf9859c2772588f389132
source_capture_chars_original: 1476
source_publication_excerpt_chars: 1476
observation_id: obs_0933b3876ff96c3c3cf38872c8e2da6612e6e177070fae8796775102f5cbed55
revision_id: rev_0a4e6cc51b9b86d5c99a8340601597d68de8c39bf29a4c39bc94f3dfb65a216f
event_id: evt_afbb98144ce45e8ef09869e95e31736e1935d57435fa64dcb5dcebf14f1124a4
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-27T06:11:48Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23359v1](<https://arxiv.org/abs/2602.23359v1>)
- **作者**: Vaibhav Agrawal, Rishubh Parihar, Pradhaan Bhat, Ravi Kiran Sarvadevabhatla, R. Venkatesh Babu
- **分类**: cs.CV
- **论文时间**: 2026-02-26T18:59:05Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23359v1.pdf](<https://arxiv.org/pdf/2602.23359v1.pdf>)

## 来源摘要/节选

> We identify occlusion reasoning as a fundamental yet overlooked aspect for 3D layout-conditioned generation. It is essential for synthesizing partially occluded objects with depth-consistent geometry and scale. While existing methods can generate realistic scenes that follow input layouts, they often fail to model precise inter-object occlusions. We propose SeeThrough3D, a model for 3D layout conditioned generation that explicitly models occlusions. We introduce an occlusion-aware 3D scene representation \(OSCR\), where objects are depicted as translucent 3D boxes placed within a virtual environment and rendered from desired camera viewpoint. The transparency encodes hidden object regions, enabling the model to reason about occlusions, while the rendered viewpoint provides explicit camera control during generation. We condition a pretrained flow based text-to-image image generation model by introducing a set of visual tokens derived from our rendered 3D representation. Furthermore, we apply masked self-attention to accurately bind each object bounding box to its corresponding textual description, enabling accurate generation of multiple objects without object attribute mixing. To train the model, we construct a synthetic dataset with diverse multi-object scenes with strong inter-object occlusions. SeeThrough3D generalizes effectively to unseen object categories and enables precise 3D layout control with realistic occlusions and consistent camera control.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
