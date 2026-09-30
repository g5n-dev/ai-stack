---
title: "FurE: Efficient Instance-Specific 3D Fur Reconstruction without Animal-Fur Datasets"
date: 2026-09-29T16:31:16+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:043f2ffd10b9d52df295b7a7e9a3286e34a614e265055ebb2c0cf3b99d90d919"
source_payload_sha256: "sha256:0135aa22cf1d0c187de2aed2c86037fd61a652c6c1ee8b2de986c30fe648268c"
observation_id: obs_9d9b41e3ff66d4cae1c63cc007c522ec94b5ee01a96a4328ab097f2dedff241f
event_id: evt_8c1d1705b9d49ab1f899b099c260f1116cf308974ea207c0086b794ba2158aa0
revision_id: rev_7c823a34f2665d5852520934d038546592fd94f65d9810a63a8f483ceeef222c
source_published_at: 2026-09-28T17:59:58Z
first_seen_at: 2026-09-29T08:43:24Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
interpretation_sha256: "sha256:5839bc727c1878997961e2c9e184b733626ac24d2b73dab15738fd2628f8a1c4"
description: "FurE 是一种基于单根毛发的动物毛发三维重建方法，通过根节点条件潜在场和主成分解码器实现可编辑的毛发生成，并利用表面约束的高斯霜冻表示恢复去毛后的动物体形。"
external_url: http://arxiv.org/abs/2609.35770v1
parent_observation_id: null
last_seen_at: 2026-09-30T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.35770v1](http://arxiv.org/abs/2609.35770v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Srinjay Sarkar、Prakhar Kaushik、Soumava Paul 等

## 要点解读

### 这是什么
FurE 是一种基于单根毛发的动物毛发三维重建方法，通过根节点条件潜在场和主成分解码器实现可编辑的毛发生成，并利用表面约束的高斯霜冻表示恢复去毛后的动物体形。

### 用在哪里
适用于需要从多视角图像快速生成逼真、可编辑动物毛发的数字内容创作、虚拟现实或游戏毛发资产研发场景。

### 可以推断的
- 推测：该方法在缺乏动物毛发专用数据时，可借助人类头发数据进行跨类别迁移，降低数据获取成本。  
- 推测：通过主成分解码和训练加速，适用于在算力或时间受限的环境中快速迭代毛发模型。

## 来源摘要/节选

> Realistic and editable animal fur reconstruction from multi-view images is challenging due to fine-scale detail, self-occlusion and obfuscation, and, unlike human hair, the lack of animal-fur datasets. Fur usually covers most of an animal's body, with large inter-species and intra-species variability. We present FurE, an efficient strand-based animal fur reconstruction method that recovers a per-strand, editable groom by optimizing a root-conditioned latent field, decoded into strand geometry via a PCA-based decoder. We reconstruct a defurred animal body using local fur-thickness cues from a surface-constrained Gaussian Frosting representation together with part-based priors. We further show that a PCA-based decoder learned from human-hair strand data can alleviate animal-data scarcity while enabling substantially faster optimization. FurE achieves a 10x speedup in strand training over current SOTA dense per-strand optimization while retaining strand fidelity and generalizing across synthetic and real-world sequences, with quantitative and qualitative validation despite the reduction in training time.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。