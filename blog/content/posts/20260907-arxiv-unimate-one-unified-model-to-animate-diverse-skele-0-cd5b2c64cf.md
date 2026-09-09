---
title: "UniMate: One Unified Model to Animate Diverse Skeletons"
date: 2026-09-07T18:18:34+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:d0c7064b4380dd4ee577aaf924a1dee13f33565a0d76c87d3c208af39602f9bd"
source_payload_sha256: "sha256:d5a13a1034896341bba9f27561c4af316b77f93a2a1cafa255b71300754d3af2"
observation_id: obs_cd5b2c64cf192d96dc640f5de478784cd12d2217195b00eae95f68a6f46187dc
event_id: evt_86099d7beb081c75994c4878f245ff1a5934ad421c65f16b038a77c5cae1de3a
revision_id: rev_16591a046868ea26b2343251dd145edd3697fc90f4d07a9a09661c84173661bf
source_published_at: 2026-09-04T17:59:00Z
first_seen_at: 2026-09-07T10:28:27Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 55
interpretation_sha256: "sha256:95eeccc93fa07c283f182a5f3fd2617ef3aa0781d19a06f5b97aba29a682a5d1"
description: "该模型是一种统一的动画生成框架，仅凭 rigged 三维资产的骨架结构与一段文本提示，即可直接合成符合该骨架的关节运动。它通过图感知注意力、基于图拉普拉斯的旋转型位置编码以及全局拓扑条件器等机制，实现对任意拓扑结构的支持，省去逐骨架的微调或参考动作。"
external_url: http://arxiv.org/abs/2609.05415v1
parent_observation_id: null
last_seen_at: 2026-09-09T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.05415v1](http://arxiv.org/abs/2609.05415v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Linzhan Mou、Jiahui Lei、Zhiyang Dou 等

## 要点解读

### 这是什么
该模型是一种统一的动画生成框架，仅凭 rigged 三维资产的骨架结构与一段文本提示，即可直接合成符合该骨架的关节运动。它通过图感知注意力、基于图拉普拉斯的旋转型位置编码以及全局拓扑条件器等机制，实现对任意拓扑结构的支持，省去逐骨架的微调或参考动作。

### 用在哪里
适用于需要快速为不同角色模型生成自然动作的制作流程，如游戏角色动画、虚拟主播、电影特效、机器人动作仿真等。动画师和开发者能够在没有大量手动关键帧或针对性训练的情况下，获得多样化的动作素材。

### 可以推断的
推测：该技术有望显著缩短角色动作的制作周期，因为它避免了为每种骨架单独调参和训练的过程。  
推测：在需要跨类别角色实现零样本跨拓扑迁移或一次性生成多种姿态时，可能具备优势，因为模型专门设计了支持任意骨架结构的通用生成能力。

## 来源摘要/节选

> Recent advances in automatic rigging now deliver animation-ready 3D assets at scale, yet generating the motion to drive them remains a bottleneck. Existing learned animators are topology-constrained: they rely on category-specific templates or require per-skeleton fine-tuning and reference motions at inference. We present UniMate, a unified foundation model that synthesizes articulated motion for arbitrary skeletons from a rigged 3D asset and a text prompt, with no test-time optimization or per-skeleton retraining. UniMate introduces a topology-aware diffusion transformer, which integrates skeletal topology into attention via three mechanisms: (1) a graph-aware attention bias from pairwise joint relations and geodesic distances; (2) a spectral rotary position embedding generalizing RoPE to arbitrary kinematic trees via the graph Laplacian; and (3) a global topological conditioner attention-pooled from the rest-pose skeleton. We also curate UniML3D, 13,006 motion sequences spanning bipedal, quadrupedal, avian, marine, insectoid, serpentine, and articulated rigid objects with unified canonicalization and text pairing. Trained on this dataset, UniMate outperforms state-of-the-art baselines in quality, generalization, and efficiency, and supports zero-shot cross-topology transfer, in-betweening, expansion, and text-guided editing. Our project page is available at https://linzhanmou.com/unimate/.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。