---
title: 'IVGT: Implicit Visual Geometry Transformer for Neural Scene Representation'
date: 2026-05-18 20:40:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 计算机视觉
categories:
- 论文
scenarios:
- AI/ML项目
- 计算机视觉
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.16258v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:d2c22f90e71899934240f0d651dcd61012b188246fceeaed088492bd81397f4b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
captured_at: '2026-07-18T04:29:39.576255Z'
source_capture_sha256: sha256:7b5f544014b7da5fbc0b2cc9748442df5c7f12d48f0943349497a10c90578e0e
source_capture_chars_original: 1237
source_publication_excerpt_chars: 1237
observation_id: obs_c0bb5e6e91b0850dcc3738d3b4b819efb10fa5deef65ed5bedd0f7ae0d5a07af
revision_id: rev_cee511bfb7045aba5cf8f11c82754cd036f16e21caa4bfb76d949a1583a068ae
event_id: evt_5e4f2d22f07f39e6ff00be9a4ad8dd1de86181f7623eaa2be3f82b7f8f9b354f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-18T09:43:23Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.16258v1](<https://arxiv.org/abs/2605.16258v1>)
- **作者**: Yuqi Wu, Tianyu Hu, Wenzhao Zheng, Yuanhui Huang, Haowen Sun, Jie Zhou, Jiwen Lu
- **分类**: cs.CV
- **论文时间**: 2026-05-15T17:59:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.16258v1.pdf](<https://arxiv.org/pdf/2605.16258v1.pdf>)

## 来源摘要/节选

> Reconstructing coherent 3D geometry and appearance from unposed multi-view images is a fundamental yet challenging problem in computer vision. Most existing visual geometry foundation models predict explicit geometry by regressing pixel-aligned pointmaps, often suffering from redundancy and limited geometric continuity. We propose IVGT, an Implicit Visual Geometry Transformer that implicitly models continuous and coherent geometry from pose-free multi-view images. This formulation learns a continuous neural scene representation in a canonical coordinate system and supports continuous spatial queries at any 3D positions, retrieving local features to predict signed distance \(SDF\) values and colors using lightweight decoders. It allows direct extraction of continuous and coherent surface geometry, enabling rendering of RGB images, depth maps, and surface normal maps from arbitrary viewpoints. We train IVGT via multi-dataset joint optimization with 2D supervision and 3D geometric regularization. IVGT demonstrates generalization across scenes and achieves strong performance on various tasks, including mesh and point cloud reconstruction, novel view synthesis, depth and surface normal estimation, and camera pose estimation.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
