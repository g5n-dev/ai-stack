---
title: "GigaPath-Flash and GigaTIME-Flash: Efficient Pathology Foundation Models for Whole-Slide and Tumor Microenvironment Analysis"
date: 2026-07-21T17:43:08+08:00
draft: false
entry_kind: "auto"
tags: ["cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:ed227c5ffd25c02997a8da5a5381d82dc52face16d31c93ca0b168ea46387127"
source_payload_sha256: "sha256:6a7356d4fb9fd50a4b11d6055d93cbcc69d59a8b16494f2666721f21929b792d"
observation_id: obs_0ab562319659999c2d5f9f361180201665e6a47eb92dcd566167949f4e14689d
event_id: evt_8ffda1727f9681014b86d24678c14d8a7525630e220188135712070a0e943843
revision_id: rev_827ee2a0abdf507edfb3ec130a4360033ceeef34f1dd813cb6a6aeb1367ec82e
source_published_at: 2026-07-20T17:52:33Z
first_seen_at: 2026-07-21T10:01:01Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 124
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.18218v1
parent_observation_id: null
last_seen_at: 2026-07-22T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.18218v1](http://arxiv.org/abs/2607.18218v1)

## 来源摘要/节选

> Foundation models have emerged as a driving force in computational pathology, with the potential to transform cancer diagnosis, prognosis, and treatment selection by learning transferable representations from large-scale histopathology data. A growing landscape of pathology foundation models now spans diverse data sources, architectures, and downstream applications. However, most pretrained models operate only at the image-tile level, use restrictive licenses, and remain computationally expensive, limiting large-scale slide-level clinical and research use.
> Here, we introduce GigaPath-Flash and GigaTIME-Flash, efficient models for whole-slide pathology AI and spatial proteomics prediction. GigaPath-Flash combines a 22M-parameter ViT-S tile encoder with a 21M-parameter LongNet slide encoder, both pretrained on large-scale real-world histopathology data. Its compact tile encoder is distilled from the billion-parameter GigaPath (ViT-g) teacher and shared by both models. GigaPath-Flash retains 97% of GigaPath's average slide-level performance with 50x less compute. GigaTIME-Flash extends this backbone to predict the tumor immune microenvironment directly from routine H&amp;E images. It surpasses the original CNN-based GigaTIME in prediction quality while running 6x faster and using 8x less GPU memory.
> Together with GigaPath and GigaTIME, these models form an open-weight, Apache-2.0-licensed family pretrained on large-scale real-world clinical data. By releasing all models and weights, we provide accessible building blocks for computational pathology, immuno-oncology, and precision health.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。