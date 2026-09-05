---
title: "One Editor, Many Edits: A Unified Training-Free Framework for Diverse Video Editing"
date: 2026-09-05T17:08:02+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:dc1f64dec0fbb5a41911a7f47055bccfdcb475153c6fbf1b6f519b170490efa1"
source_payload_sha256: "sha256:b1a2c85b76a9ef36fb0e285730a3dbcadd7ee571688cefbd2cc68ce04730a5bc"
observation_id: obs_ff07077433fa5730b4e0362e2d28d8bf660d3ca2515ff87a9e17008a73c07fa1
event_id: evt_a6841d2dcf068efc723b6eaa38e518388d0bff4d5c9ca11c342fa79b80cacade
revision_id: rev_c2cd5d8ffbe28e5df7b11d02ff86f402b8d10440003dadd7be6c73aafc9e7481
source_published_at: 2026-09-03T17:59:01Z
first_seen_at: 2026-09-05T09:18:12Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
interpretation_sha256: "sha256:62967e26d18508b616aa24b2daec5c2f016ef6919f12b0cf0efcdaf28da028b9"
description: "EditVid 是一种无需训练的通用视频编辑框架，利用稀疏因果记忆保证局部连贯、对应驱动的后注意力令牌注入保持远距离身份，并采用软潜在混合实现编辑局部性。该框架同时支持文字指令和参考图像两种编辑方式。"
external_url: http://arxiv.org/abs/2609.04190v1
parent_observation_id: null
last_seen_at: 2026-09-05T09:04:48.236633Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.04190v1](http://arxiv.org/abs/2609.04190v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Adheesh Sunil Juvekar、Onkar Kishor Susladkar、Kiet A. Nguyen 等

## 要点解读

### 这是什么
EditVid 是一种无需训练的通用视频编辑框架，利用稀疏因果记忆保证局部连贯、对应驱动的后注意力令牌注入保持远距离身份，并采用软潜在混合实现编辑局部性。该框架同时支持文字指令和参考图像两种编辑方式。

### 用在哪里
适用于需要根据文字说明或参照图像对视频进行风格迁移、属性修改、对象插入、部件级编辑或主体替换等多样化编辑任务的场景。

### 可以推断的
推测：该框架不依赖大规模微调，适合资源受限或快速部署的环境。  
推测：将多种编辑需求统一在同一模型中，可降低系统复杂度并简化实际产品的维护。

## 来源摘要/节选

> Video editing spans diverse editing paradigms, yet achieving high-quality instruction-guided and subject-guided editing within a single unified framework remains challenging. We introduce EditVid, a training-free framework combining sparse causal memory for local coherence, correspondence-based post-attention token injection for long-range identity preservation, and soft latent blending for edit locality. The same framework supports instruction-guided and reference-guided edits, including style transfer, attribute modification, object insertion, part-level editing, and subject replacement. On FiVE, EditVid achieves 78.16 FiVE-Acc, compared with 58.95 for the strongest evaluated training-free baseline, while obtaining competitive results on IVEBench. A user study further shows a 51.8\% overall preference for EditVid over 7 competing methods.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。