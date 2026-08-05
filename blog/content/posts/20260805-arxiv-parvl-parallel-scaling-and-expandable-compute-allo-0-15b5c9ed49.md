---
title: "ParVL: Parallel Scaling and Expandable Compute Allocation for Multimodal LLMs"
date: 2026-08-05T11:35:02+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:1918a69cbc1f141e46e4149b7ad3e8269334b3acb32d9f68261714a544daff64"
source_payload_sha256: "sha256:f274e07b6bd2185c711fc00a24a3438993169014cc96f697c4aaf20dc4137fb8"
observation_id: obs_15b5c9ed4961c3fc228c4ece119ea08750e099b9cd5f71547bf89a60ef0d5ccc
event_id: evt_077657f777b5a688ff3877ca87f3264db810d9812e70c623bce9f261f0cc2cfb
revision_id: rev_1a3ff29bac1f04cb68e4670af47942ab7ccb44abdb903b13af673c650aa10722
source_published_at: 2026-08-04T17:59:58Z
first_seen_at: 2026-08-05T03:43:40Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
interpretation_sha256: "sha256:bdb57fc27136e26faaaee782eec6bdaf01407f9e300d2c6028f02703eb56bc77"
description: "ParVL 是一种多模态大语言模型的并行扩展方案。它在保持原有视觉编码器（ViT）和语言模型（LLM）主干参数不变的前提下，通过添加分支专属的 prefix 参数，让多个视觉和语言分支共享同一套主干，从而实现算力的并行增长并灵活调配视觉与语言之间的计算比例。"
external_url: http://arxiv.org/abs/2608.04010v1
parent_observation_id: null
last_seen_at: 2026-08-05T03:31:52.267969Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.04010v1](http://arxiv.org/abs/2608.04010v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Yang Yang、Qinyu Zhao、Mouxiang Chen 等

## 要点解读

### 这是什么  
ParVL 是一种多模态大语言模型的并行扩展方案。它在保持原有视觉编码器（ViT）和语言模型（LLM）主干参数不变的前提下，通过添加分支专属的 prefix 参数，让多个视觉和语言分支共享同一套主干，从而实现算力的并行增长并灵活调配视觉与语言之间的计算比例。  

### 用在哪里  
适合需要同时处理图像和文本的高阶任务（如视觉问答、跨模态推理等），并且在部署时对显存占用或推理时延有严格限制的场景。研究多模态模型资源分配或想在不同任务上尝试动态算力分配的团队也会受益。  

### 可以推断的  
推测：在固定参数量预算下，通过调节分支专属参数可以在不增加主干规模的情况下提升模型的多模态表现。  
推测：不同任务对视觉与语言算力的需求不同，框架的可调分配特性或能帮助针对具体任务找到更优的配置。

## 来源摘要/节选

> Existing scaling strategies for Multimodal Large Language Models (MLLMs) typically expand either model parameters or sequential inference computation, incurring substantial memory or latency overhead. More importantly, most existing methods fail to alter the rigid, fixed computation allocation between the Vision Transformer and the Large Language Model components, limiting task-specific optimization. To address this, we introduce the Parallel Vision-Language (ParVL) scaling framework for MLLMs, which scales parallel computation by reusing the existing ViT and LLM backbone parameters across multiple vision and language branches. This framework raises a central question: given a fixed backbone parameter budget, how should additional shared-backbone computation be allocated between the vision and language modalities? We instantiate each parallel computational stream with branch-specific prefix parameters over a shared backbone, and train the entire model end-to-end via full-parameter supervised fine-tuning on roughly 13B tokens. We systematically study the computation-allocation trade-off between the ViT encoder and LLM decoder. ParVL improves overall multimodal performance over same-recipe single-branch baselines, and the best evaluated vision--language allocation varies across tasks. Code is available at https://github.com/YangYangGirl/ParVL.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。