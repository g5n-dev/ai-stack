---
title: Shared LoRA Subspaces for almost Strict Continual Learning
date: 2026-02-06 23:01:34+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.06043v1
aliases:
- /posts/20260207-arxiv_ai-shared-lora-subspaces-for-almost-strict-continual--0/
- /posts/20260208-arxiv_ai-shared-lora-subspaces-for-almost-strict-continual--0/
- /posts/20260209-arxiv_ai-shared-lora-subspaces-for-almost-strict-continual--0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ea01189a82c3240dd6a86112ff84387ad26986a4ac069671554cfe2d63bc6939
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
captured_at: '2026-07-18T04:11:20.263833Z'
source_capture_sha256: sha256:9927d4f1a79c471b0a0ac878a65366c1d55b4c5427c484257315b36457880958
source_capture_chars_original: 1532
source_publication_excerpt_chars: 1532
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06043v1](<https://arxiv.org/abs/2602.06043v1>)
- **作者**: Prakhar Kaushik, Ankit Vaidya, Shravan Chaudhari, Rama Chellappa, Alan Yuille
- **分类**: cs.LG
- **论文时间**: 2026-02-05T18:59:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06043v1.pdf](<https://arxiv.org/pdf/2602.06043v1.pdf>)

## 来源摘要/节选

> Adapting large pretrained models to new tasks efficiently and continually is crucial for real-world deployment but remains challenging due to catastrophic forgetting and the high cost of retraining. While parameter-efficient tuning methods like low rank adaptation \(LoRA\) reduce computational demands, they lack mechanisms for strict continual learning and knowledge integration, without relying on data replay, or multiple adapters. We propose Share, a novel approach to parameter efficient continual finetuning that learns and dynamically updates a single, shared low-rank subspace, enabling seamless adaptation across multiple tasks and modalities. Share constructs a foundational subspace that extracts core knowledge from past tasks and incrementally integrates new information by identifying essential subspace directions. Knowledge from each new task is incorporated into this evolving subspace, facilitating forward knowledge transfer, while minimizing catastrophic interference. This approach achieves up to 100x parameter reduction and 281x memory savings over traditional LoRA methods, maintaining performance comparable to jointly trained models. A single Share model can replace hundreds of task-specific LoRA adapters, supporting scalable, asynchronous continual learning. Experiments across image classification, natural language understanding, 3D pose estimation, and text-to-image generation validate its effectiveness, making Share a practical and scalable solution for lifelong learning in large-scale AI systems.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
