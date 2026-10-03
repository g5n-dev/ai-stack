---
title: "SILSA: Sliding-Window Slice Latents for Topology-Preserving High-Resolution 3D Generation"
date: 2026-10-03T14:34:10+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:cac7269c35fe80e8678d68ab943ce855398eeaf0edab7ccd64788ed43d560462"
source_payload_sha256: "sha256:a0912134b24bbc93d207f75a8847508b9d75762ed45312692b41db9f3a4665ef"
observation_id: obs_388ce43bd4fdcadf4fb9b579374c37cea89c92375e4d58bef82ef1d759efb15c
event_id: evt_82a335e6b643dc583b09659a3dfab7d82e2efe87e784591352232457f5805aac
revision_id: rev_1ee763cfaef9b034ba91dfbc2f600ff1f065a54a0ee1f33613e6babef4eb1273
source_published_at: 2026-10-01T17:59:46Z
first_seen_at: 2026-10-03T06:31:53.907892Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
interpretation_sha256: "sha256:133fe6c005abdfee8eab4e46b39dbf5982bd9845f98c10dee1876bd3e4f09608"
description: "SILSA是一种把三维形状表示为沿三个主轴的滑动窗口切片潜在向量的生成框架。它通过切片级拓扑监督保持跨截面连续性，并使用单阶段纠正流进行高分辨率建模。"
external_url: http://arxiv.org/abs/2610.02201v1
parent_observation_id: null
last_seen_at: 2026-10-03T06:31:53.907892Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02201v1](http://arxiv.org/abs/2610.02201v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Tianjiao Yu、Xinzhuo Li、Yifan Shen 等

## 要点解读

### 这是什么
SILSA是一种把三维形状表示为沿三个主轴的滑动窗口切片潜在向量的生成框架。它通过切片级拓扑监督保持跨截面连续性，并使用单阶段纠正流进行高分辨率建模。

### 用在哪里
适用于需要保持细长结构、重复部件和长程连通性的三维模型生成任务，尤其在显存和推理时间受限的环境中，可显著降低计算成本。

### 可以推断的
推测：该方法能够与现有的基于体素的生成管线结合，以减少显存占用并加快生成速度。  
推测：在自动化建模、虚拟现实内容生成和大规模场景构建等应用场景中，有望提升结构完整性和生产效率。

## 来源摘要/节选

> High-resolution 3D generation increasingly relies on voxel latents and multi-stage pipelines that first predict active structure and then synthesize local geometry. While effective, this design fragments continuous surfaces into many local tokens, inflates generation cost, and often weakens topological consistency for thin or highly connected shapes. We introduce SILSA, a topology-aware 3D generation framework that represents shapes with compact sliding-window slice latents. Instead of generating expensive voxel tokens, SILSA uses a fixed set of overlapping slices along the three canonical axes, where each token summarizes a local depth window to preserve cross-sectional continuity and support single-stage rectified-flow generation. A Slice VAE encodes oriented surface samples into multi-axis slice latents and reconstructs them with a sparse volumetric decoder, while a Volumetric Anchor Lattice coordinates directional slice streams through a shared 3D workspace. To preserve structural correctness, we introduce slice-level topology supervision that matches persistence diagrams and aligns Betti transitions across neighboring slices. Experiments show that SILSA improves structural fidelity while substantially reducing generation cost. SILSA improves PSNR by $8.7\%$, coverage by $5.96$ absolute points, and Betti error by $9.2\%$ over the strongest baseline, while using $70.0\%$ fewer tokens than the next-most compact baseline and over $98\%$ fewer tokens than sparse or hierarchical tokenizers, effectively reducing training memory by $40.4\%$ and inference time by $58.5\%$. Qualitative results further show improved preservation of thin structures, repeated components, and long-range connectivity.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。