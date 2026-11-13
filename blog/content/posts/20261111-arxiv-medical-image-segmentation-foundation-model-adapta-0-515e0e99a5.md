---
title: "Medical Image Segmentation: Foundation Model Adaptation versus Task-Specific Training"
date: 2026-11-11T14:14:34+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7cfa718a82a195541fda3edd3d715ae311b6638333d4d0c42bb7670d66f95442"
source_payload_sha256: "sha256:1244d10c6014e33e81812f92b9999174ea884d74a9aa49a878865280a78fcdf3"
observation_id: obs_515e0e99a5a4b6e414052e3e4e9d662d4d5d202de637ef4ef2a5c4ae7c43aaac
event_id: evt_166ae795a76d32596f9d4731aeb56fc949a9e0539f966d9ab4b191df94265fc9
revision_id: rev_04c31e84499d20a331c6c66a2d3cb6124c99b053ff14942abcb3db24e87fe62d
source_published_at: 2026-11-10T18:59:54Z
first_seen_at: 2026-11-11T06:23:55Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.14519v1
parent_observation_id: null
last_seen_at: 2026-11-13T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.14519v1](http://arxiv.org/abs/2611.14519v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Emre Kutlusan、Yongmin Li

## 来源摘要/节选

> Foundation models pretrained on large natural-image collections are increasingly adapted for medical image segmentation, in the expectation that they will replace models trained for each task. Most comparisons, however, use data from the training distribution and a single task-specific baseline whose configuration is rarely justified, and therefore provide limited evidence of performance at new clinical sites. It also remains unclear how much of a foundation model must be adapted, and what determines this. We adapted a foundation model, DINOv2, with strategies ranging from tuning only its bias terms to full fine-tuning, and compared it with U-Nets and ResU-Nets trained from scratch. Experiments covered colonoscopy, breast ultrasound and dermoscopy, with testing on held-out data from the training source and on independent datasets from other institutions. The adapted foundation model generalised better on every external dataset. Within the training distribution, the task-specific models remained competitive when training data were abundant, and delineated boundaries more precisely, while the foundation model more often missed small lesions. Only a small fraction of the foundation model required adaptation, and the capacity needed was determined by the imaging domain rather than by the adaptation method. A widely used polyp test set was also found to duplicate images from another benchmark. Foundation-model adaptation is therefore warranted where models must work across sites, with capacity selected on the target domain.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。