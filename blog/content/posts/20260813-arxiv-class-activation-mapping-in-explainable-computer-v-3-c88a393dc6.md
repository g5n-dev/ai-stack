---
title: "Class Activation Mapping in Explainable Computer Vision: A Method-Centered Review of CNN, Transformer, and Foundation-Model-Era Visual Explanations"
date: 2026-08-13T16:45:56+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:edaa7ec64ba46785c02429088edb594c0c4b9afd49fdb5a21faf1ff0027cd39d"
source_payload_sha256: "sha256:349ea2e69c163ca7c23a22d995520d64c3ae58da118d26816cff79204ffeb28d"
observation_id: obs_c88a393dc638d1f5e137df052ecca6e6fb6c5995b4930846101a40dbb64a4c12
event_id: evt_ec1e68519cab9fa7fe7c68bbb83930c3fc017204a4abc512b279b45c6f1ec8e9
revision_id: rev_f2c435582d68a640f13939b8f151a48c40a219346f6a05a419f8d22937676224
source_published_at: 2026-08-12T17:45:03Z
first_seen_at: 2026-08-13T08:55:31Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 147
interpretation_sha256: "sha256:21f666c3c00d909d84971d414f4d0527bb159bd9845c814ff438d718e631a1e8"
description: "这篇论文综述了自2016年提出的类激活映射（CAM）方法在可解释计算机视觉中的发展，涵盖了从卷积网络到Transformer以及基于基础模型的视觉归因技术。"
external_url: http://arxiv.org/abs/2608.12299v1
parent_observation_id: null
last_seen_at: 2026-08-13T08:43:29.630038Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12299v1](http://arxiv.org/abs/2608.12299v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: AmirHossein Eshghi、Hamid Saadatfar、Seyyed Ali Hoseini 等

## 要点解读

### 这是什么
这篇论文综述了自2016年提出的类激活映射（CAM）方法在可解释计算机视觉中的发展，涵盖了从卷积网络到Transformer以及基于基础模型的视觉归因技术。

### 用在哪里
适合从事可解释人工智能研究的学者和工程师，用于了解各类CAM方法的设计思路、适用范围以及在不同视觉任务中的表现。

### 可以推断的
推测：文中指出评价体系仍较为分散，未来可能出现统一的评估协议以提升方法可比性。  
推测：随着基础模型在视觉解释中的引入，方法将更倾向于多层次、跨模态的比较与归因。

## 来源摘要/节选

> Class activation mapping (CAM) is one of the most widely used visual explanation families in explainable artificial intelligence. Its purpose is intuitive: it converts internal model evidence into a heatmap that highlights the image regions, convolutional channels, tokens, or patches that support a target class or concept. Since the first CAM formulation in 2016, the field has moved far beyond global-average-pooled CNN classifiers. CAM-style methods now include gradient-based post-hoc explanations, gradient-free score and ablation methods, high-resolution upscaling, weakly supervised localization and segmentation, transformer token attribution, causal and debiasing methods, and foundation-model-era approaches that use CLIP, DINO, SAM, or feature-distribution comparisons. This review synthesizes a strict corpus of 57 method-centered papers published from 2016 onward. The paper develops a taxonomy that separates methods by attribution mechanism, architectural dependence, and evaluation objective. It then reviews gradient-based CAMs, recent and hybrid CAM-style methods, and model-based or architecture-aware methods. Across the corpus, the main trend is clear: the field is shifting from explaining one class score in one low-resolution CNN layer toward comparative, multi-layer, probabilistic, token-aware, and foundation-model-aware explanations. At the same time, evaluation remains fragmented. Faithfulness, localization, robustness, computational cost, and human trust are often measured with different protocols. The review therefore emphasizes not only what each method contributes, but also which gap it leaves open and which later methods attempt to close that gap.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。