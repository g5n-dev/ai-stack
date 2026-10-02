---
title: "Embedding Prediction Helps Image Generation"
date: 2026-10-03T04:47:36+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:f8585ad6352caa9ce13ae0b6a98dff96ce4d35e6305f5f86b3997e50cc14330a"
source_payload_sha256: "sha256:aa0446c4e850f29b87880fb08f19a84869825b23f3a8402cd5ac4810829cd305"
observation_id: obs_2e5f8d1d7a0d863acd3da1528ca18c4a307fdde392f4a0d834de4634eae9d7c7
event_id: evt_57d3afcc85972ce34e7e3c9044e99f8f4a318c25a0089b251c5d62d16b65bbaa
revision_id: rev_f23be4522e247c64745d20f291b7eb53975eeb96aa8fd69cdc1a513a50a4d3fb
source_published_at: 2026-10-01T17:59:49Z
first_seen_at: 2026-10-02T20:44:07.579524Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2610.02203v1
parent_observation_id: null
last_seen_at: 2026-10-02T20:44:07.579524Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02203v1](http://arxiv.org/abs/2610.02203v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Sihan Xu、Ji Xie、Zilin Wang 等

## 来源摘要/节选

> In diffusion transformers, a class label or a text prompt is embedded once, and the same condition is reused at every denoising step. We ask whether predicted embeddings can serve as this condition instead. Next-Embedding Predictive Autoregression (NEPA) trains a Transformer to predict the next continuous embedding in a sequence. In generation, the clean image follows the noisy image, so its embeddings are the next embeddings after the condition and the noisy image. We train a NEPA model to predict them all at once with Multi-Embedding Prediction, and in Embedding Conditioned Generation, a DiT generator is conditioned on these predictions, recomputed at every denoising step, so the conditioning signal adapts to the current noisy state. Experiments on class-conditional ImageNet $256\times256$ study the condition of the generator, the design of Multi-Embedding Prediction, and the scaling of both models. The NEPA model adds a second network to every sampling step; with it, and combined with REPA, our final model, NEPA-DiT-XL, reaches an FID of 1.32 using about a third of the training compute of REPA.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。