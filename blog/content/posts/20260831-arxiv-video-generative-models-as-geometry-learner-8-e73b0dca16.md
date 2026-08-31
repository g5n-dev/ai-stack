---
title: "Video Generative Models as Geometry Learner"
date: 2026-08-31T21:49:44+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4b4a38f32562f97c69c3936f1192ca7c237f21607d775a5fe0f59c817b10bf83"
source_payload_sha256: "sha256:f980e9b48c36f1820c513fa197996cf3e61ebdfdb7ee630d8924851f77774a00"
observation_id: obs_e73b0dca16ea1bd48198623c315e85a5e5b94254978b0c21ac77f9c0bdebb3a3
event_id: evt_9b2ed3fd36e6d8b1a88928bb07468b0404ec780fbad85af37fb5fc45a59df500
revision_id: rev_c633151e2daf690a7403f466833c5b94ada0d157a39d9b6d19d2c956b666e6bb
source_published_at: 2026-08-28T17:25:31Z
first_seen_at: 2026-08-31T13:47:02.832555Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
interpretation_sha256: "sha256:01a5342ace8b605729f709dd503446fc82e15df8b9843bc840d47bc42658c8fe"
description: "该工作将预训练的生成式视频模型改造为几何估计框架，通过把深度和表面法线等几何预测任务重新定义为预测后续帧的任务，实现对图像与几何目标的联合建模。"
external_url: http://arxiv.org/abs/2608.28549v1
parent_observation_id: null
last_seen_at: 2026-08-31T13:47:02.832555Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.28549v1](http://arxiv.org/abs/2608.28549v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Haosen Yang、Jifei Song、Zhensong Zhang 等

## 要点解读

### 这是什么
该工作将预训练的生成式视频模型改造为几何估计框架，通过把深度和表面法线等几何预测任务重新定义为预测后续帧的任务，实现对图像与几何目标的联合建模。

### 用在哪里
适用于需要在缺乏大量标注数据的情况下进行单目深度和表面法线估计的研究者和工程师，尤其适合希望在不同数据集上实现零样本迁移的视觉系统开发者。

### 可以推断的
推测：该方法利用视频模型中已有的运动和结构先验，可能在标注数据稀缺的场景下仍保持较好效果。  
推测：由于采用统一的生成式建模思路，模型结构或可扩展至其他几何属性（如光流、场景布局）的估计任务。

## 来源摘要/节选

> Recent generative approaches to geometry estimation adapt pretrained image diffusion models and treat the task as image-conditioned generation. Leveraging off-the-shelf image diffusion models, they either (i) train task-specific geometry models (for depth and surface normal estimation) independently, losing the opportunity of exploring the intrinsic correlation of these geometric targets, or (ii) jointly fine-tune modified image diffusion backbones (e.g., altered self-attention), which typically demands substantial labeled data. To overcome these limitations in a principled fashion, we repurpose pretrained video generative models as a unified and data-efficient framework for geometry estimation, formulated innovatively as a next-frames prediction task. Our method, GeoNeXt, inherits naturally structured knowledge and richer priors from the video model, while further adapting them for joint modeling of images and geometry targets (image &lt;-&gt; geometry), enabling more data efficient and effective learning of geometry. Extensive experiments validate our method for zero-shot monocular depth and surface normal estimation across diverse datasets, outperforming both previous task-specific and unified generative competitors while using substantially less training data. Notably, our method rivals discriminative state-of-the-art approaches trained on over 100x more data and even standouts on several benchmarks.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。