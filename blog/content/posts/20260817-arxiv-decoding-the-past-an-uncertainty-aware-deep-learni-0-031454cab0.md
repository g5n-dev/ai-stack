---
title: "Decoding the Past: An Uncertainty-Aware Deep Learning Framework for Sex Attribution in Prehistoric Hand Stencils"
date: 2026-08-17T13:54:06+08:00
draft: false
entry_kind: "auto"
tags: ["深度学习", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0fc4f42b80ce00c6e5a1306d339db85ebba46687aded2e50c6f1126fa2b33eac"
source_payload_sha256: "sha256:c6bfceab3f85260065634d25d0e6cd4c66359535435314797bf4d9b525987400"
observation_id: obs_031454cab0f9ab9a11551addbbb00d4cca0146d146970b91799d1b3f9b85f766
event_id: evt_3ff34a78b29cb5cef99ce0f9e889c1d52c4c39b8fb33f55eeb829e7a444ad96f
revision_id: rev_f3d535cb93aca01cd806b1ca7625504036a4477fd30aac3fbe8a4bdeaabb7270
source_published_at: 2026-08-14T17:51:30Z
first_seen_at: 2026-08-17T05:50:12.850582Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 112
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.14539v1
parent_observation_id: null
last_seen_at: 2026-08-17T05:50:12.850582Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.14539v1](http://arxiv.org/abs/2608.14539v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Karel Becerra、Boris Mederos、Dean Snow 等

## 来源摘要/节选

> Determining the biological sex of the individuals who created Upper Paleolithic hand stencils remains a challenging problem due to the absence of ground truth, population differences between contemporary and prehistoric groups, and the uncertainty introduced by image degradation. Traditional morphometric methods suffer from high structural overlap across sexes, poor cross-population generalizability, and subjective feature engineering. This study presents an uncertainty-aware deep learning framework for sex attribution in prehistoric hand stencils that explicitly models, propagates, and aggregates uncertainty throughout the analytical pipeline. The methodology combines dual image processing, dual contour extraction, structured silhouette augmentation, model architectural diversity, and ensemble-based decision aggregation. The pipeline generates twelve plausible silhouette realizations per stencil to capture boundary uncertainties, which are processed by two ensembles of ten deep neural networks each (EfficientNet-B3 and MobileViT-S) trained on 14,036 contemporary hand samples. Furthermore, a triangulated validation scheme integrates ensemble predictions with unsupervised 2D latent-space manifold mapping (UMAP + k-NN) and explainable AI spatial attributions (LayerCAM) to ensure anatomical consistency. On contemporary data, ensemble models achieve strong classification performance, with accuracies exceeding 88% in older age groups. When applied to prehistoric stencils, the framework produces both sex predictions and confidence measures of internal agreement, enabling the distinction between morphologically stable and ambiguous cases. Convergence across ensemble predictions, latent-space structure, and interpretability analyses shows that uncertainty can become a measurable component of archaeological inference, enabling robust and reproducible decoding of ancient rock art.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。