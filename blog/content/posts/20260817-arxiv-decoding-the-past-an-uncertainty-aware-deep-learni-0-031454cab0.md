---
title: "Decoding the Past: An Uncertainty-Aware Deep Learning Framework for Sex Attribution in Prehistoric Hand Stencils"
date: 2026-08-17T12:05:13+08:00
draft: false
entry_kind: "auto"
tags: ["深度学习", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0fc4f42b80ce00c6e5a1306d339db85ebba46687aded2e50c6f1126fa2b33eac"
source_payload_sha256: "sha256:c6bfceab3f85260065634d25d0e6cd4c66359535435314797bf4d9b525987400"
observation_id: obs_031454cab0f9ab9a11551addbbb00d4cca0146d146970b91799d1b3f9b85f766
event_id: evt_3ff34a78b29cb5cef99ce0f9e889c1d52c4c39b8fb33f55eeb829e7a444ad96f
revision_id: rev_f3d535cb93aca01cd806b1ca7625504036a4477fd30aac3fbe8a4bdeaabb7270
source_published_at: 2026-08-14T17:51:30Z
first_seen_at: 2026-08-17T04:01:44.607352Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 112
interpretation_sha256: "sha256:09e950f99cbece7648ecd3aa8ebedb3dcb30e8d948b6798c7e650274038db5e3"
description: "一种将不确定量化嵌入全流程的深度学习方案，旨在从旧石器时期的手印拓印中推断创作者的性别。方案通过生成多个轮廓实现、双模型集成以及结合无监督空间映射的可解释性验证，提供预测值和内部一致性置信度。"
external_url: http://arxiv.org/abs/2608.14539v1
parent_observation_id: null
last_seen_at: 2026-08-17T04:01:44.607352Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.14539v1](http://arxiv.org/abs/2608.14539v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Karel Becerra、Boris Mederos、Dean Snow 等

## 要点解读

### 这是什么  
一种将不确定量化嵌入全流程的深度学习方案，旨在从旧石器时期的手印拓印中推断创作者的性别。方案通过生成多个轮廓实现、双模型集成以及结合无监督空间映射的可解释性验证，提供预测值和内部一致性置信度。

### 用在哪里  
适用于考古学者在研究岩画创作者特征时需要客观、可复现的性别判断；也适合计算考古或机器学习团队在处理图像质量参差不齐的古代文物时评估模型输出的可靠性。

### 可以推断的  
推测：在边界模糊或保存状况差的手印上，框架给出的置信度会显著下降，从而帮助使用者识别需要进一步人工确认的案例。  
推测：由于涉及多个模型和大量轮廓实现的并行计算，完整流程的计算资源需求较高，可能更适合在具备较强 GPU 的服务器上运行，而非现场便携设备。

## 来源摘要/节选

> Determining the biological sex of the individuals who created Upper Paleolithic hand stencils remains a challenging problem due to the absence of ground truth, population differences between contemporary and prehistoric groups, and the uncertainty introduced by image degradation. Traditional morphometric methods suffer from high structural overlap across sexes, poor cross-population generalizability, and subjective feature engineering. This study presents an uncertainty-aware deep learning framework for sex attribution in prehistoric hand stencils that explicitly models, propagates, and aggregates uncertainty throughout the analytical pipeline. The methodology combines dual image processing, dual contour extraction, structured silhouette augmentation, model architectural diversity, and ensemble-based decision aggregation. The pipeline generates twelve plausible silhouette realizations per stencil to capture boundary uncertainties, which are processed by two ensembles of ten deep neural networks each (EfficientNet-B3 and MobileViT-S) trained on 14,036 contemporary hand samples. Furthermore, a triangulated validation scheme integrates ensemble predictions with unsupervised 2D latent-space manifold mapping (UMAP + k-NN) and explainable AI spatial attributions (LayerCAM) to ensure anatomical consistency. On contemporary data, ensemble models achieve strong classification performance, with accuracies exceeding 88% in older age groups. When applied to prehistoric stencils, the framework produces both sex predictions and confidence measures of internal agreement, enabling the distinction between morphologically stable and ambiguous cases. Convergence across ensemble predictions, latent-space structure, and interpretability analyses shows that uncertainty can become a measurable component of archaeological inference, enabling robust and reproducible decoding of ancient rock art.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。