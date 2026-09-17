---
title: "PANORAMA: Panoptic Grounded Captioning via Mask Proposal Selection"
date: 2026-09-17T21:29:52+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:09a8dcea6f6d0ace5c0fd44a3b1c42ef350bd011eb168dbcdd09b16bd6287785"
source_payload_sha256: "sha256:b9a10ae098cd209b8f9a1ebe6a148dc7eb4235877d5e57843f7dc417dacf568a"
observation_id: obs_d338ec4b9c965a2213a88edb435002be4630bc8da9ee524871fb4ad64f9d2bd7
event_id: evt_e2815a140acb80cdc2674aca202a8be7bde6bdb2e7f4a2e1ce169dbd0e38d0a5
revision_id: rev_eae67b0bb51195df1e52b9d39fffa4e1a3fdc8a415282f4089f1857d368c07b5
source_published_at: 2026-09-16T17:59:30Z
first_seen_at: 2026-09-17T13:26:50.172727Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
interpretation_sha256: "sha256:a177e9f49c59c73b4045b4cec5b76c099b6eef4a96aff925dc099b23b903a693"
description: "该工作围绕一种将图像中的前景对象和背景区域同时用文字描述并与像素级掩码对应的任务展开，构建了 PanoCaps 数据集用于密集标注，并提出 PANORAMA 模型，通过从掩码提议池中挑选与每个短语相匹配的掩码，实现精准的实体级分割与连贯的描述。"
external_url: http://arxiv.org/abs/2609.19143v1
parent_observation_id: null
last_seen_at: 2026-09-17T13:26:50.172727Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.19143v1](http://arxiv.org/abs/2609.19143v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Sara Pieri、Evangelos Kazakos、Shizhe Chen 等

## 要点解读

### 这是什么  
该工作围绕一种将图像中的前景对象和背景区域同时用文字描述并与像素级掩码对应的任务展开，构建了 PanoCaps 数据集用于密集标注，并提出 PANORAMA 模型，通过从掩码提议池中挑选与每个短语相匹配的掩码，实现精准的实体级分割与连贯的描述。

### 用在哪里  
适合需要在视觉层面提供细粒度、空间定位的语言生成任务的研究者和开发者，例如机器人感知、自动导航以及多模态模型的训练与评估。

### 可以推断的  
推测：在需要把文字与具体图像区域关联的应用（如视觉问答或场景图构建）中，这种同时生成文字与掩码的能力有望提升系统的可解释性和准确性。  
推测：掩码提议的选择机制可能在推理时增加计算负担，实际部署时需在精度和速度之间进行权衡。

## 来源摘要/节选

> Intelligent systems that act in the world require image understanding that is both comprehensive and spatially grounded. Current vision-language models (VLMs) can generate fluent and detailed image captions, but reliably associating them with image pixels remains challenging. Existing methods that combine dense captioning with pixel-level grounding often produce either incomplete descriptions or inaccurate segmentation masks. We study this problem through panoptic grounded captioning, a task that requires a VLM to describe both foreground objects and background regions while grounding each referring phrase with pixel-level masks. We make three contributions. First, we introduce PanoCaps, a human-annotated benchmark constructed from panoptic segmentation datasets. It provides dense captions with near-complete pixel coverage and image-text alignments at the entity level, supporting both training and evaluation. We further propose a phrase-mask matching protocol and a generalized Panoptic Quality (gPQ) metric that jointly evaluates textual and mask agreement. Second, we formulate phrase grounding as selection from a phrase-conditioned pool of mask proposals and introduce PANORAMA, a VLM that conditions a pretrained segmenter on contextualized phrase representations to obtain candidate masks and learns to select those corresponding to each phrase. Training this interface jointly with caption generation enables PANORAMA to produce high-quality masks while allowing each phrase to refer to a single region or multiple instances. Third, PANORAMA achieves the best overall grounding on PanoCaps and matches or exceeds specialized models across several pixel-level grounding tasks. Experiments show that our method produces precise entity-level segmentations while maintaining detailed, mask-consistent captions. Code, data and models are available at https://www.di.ens.fr/willow/research/panorama/.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。