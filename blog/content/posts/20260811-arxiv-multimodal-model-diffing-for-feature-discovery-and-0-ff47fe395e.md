---
title: "Multimodal Model Diffing for Feature Discovery and Control"
date: 2026-08-11T15:39:40+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c0fc3ce68ec6b8496f3df20439a386171b5c88765cc7c54b4a3878f028d88561"
source_payload_sha256: "sha256:57ebaade236e8796999a2cebdb350596c3d895bc6c53a71fd4dabb2684045bfc"
observation_id: obs_ff47fe395ebcef113fea717a310cbbb3a9334c9da386126b929d95865f687126
event_id: evt_d0a53773353894f7f302a008f54008cf80837b549b8a4f809bd3b3b472168ac6
revision_id: rev_285a43a95e1d7e9cf23d9f5a4d0c4640639cdc690b2690721bfb4760c0b8aa14
source_published_at: 2026-08-10T17:59:30Z
first_seen_at: 2026-08-11T07:36:05.761918Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 58
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.09928v1
parent_observation_id: null
last_seen_at: 2026-08-11T07:36:05.761918Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.09928v1](http://arxiv.org/abs/2608.09928v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Hunar Batra、Lachin Naghashyar、Ashkan Khakzar 等

## 来源摘要/节选

> Multimodal Large Language Models (MLLMs) exhibit strong visual understanding, yet the internal features that cause these behaviors remain difficult to identify, audit, or control. While applicable to post-hoc inspection, hidden states that are decomposed into interpretable feature directions using sparse autoencoders (SAEs) neither readily isolate which features are changed by multimodal training, nor are they directly useful for targeted control. We introduce MMDiff, a multimodal model-diffing framework that trains multimodal SAEs and turns them into feature-level interfaces for discovering and controlling multimodal behavior. MMDiff supports three uses: (i) feature isolation, by diffing a base-LM SAE against its multimodal-adapted counterpart to identify features altered by multimodal training; (ii) task-specific feature detection, via per-token contrastive firing analysis that isolates causal features; and (iii) feature-level control, by causally removing or steering the discovered feature directions. We train multimodal SAEs for three MLLM families, LLaVA-MORE, PaliGemma 2, and InternVL3.5, and evaluate on visual-spatial understanding, multimodal safety, and OCR. MMDiff discovers sparse, causally specific features whose removal selectively degrades target behaviors by an average of 12% on spatial tasks and 17% on OCR, and reduces attack success rate by 24% on multimodal safety attacks, with no impact on VQA performance. Steering these features improves spatial and OCR accuracy by +3.6% and +1.8% on average over a standard single-layer steering baseline. These results show that multimodal SAEs can serve not only as interpretability tools, but as mechanisms for auditing, steering, and controlling MLLMs behavior toward safer and more capable generations.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。