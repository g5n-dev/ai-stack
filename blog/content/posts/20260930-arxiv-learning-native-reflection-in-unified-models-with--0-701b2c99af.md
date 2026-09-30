---
title: "Learning Native Reflection in Unified Models with Interleaved Reinforcement Learning"
date: 2026-09-30T08:28:45+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:60529f3391ed6cf1c2753776578c4754b6754efd8eb9c98fe1d3ca167e756d3b"
source_payload_sha256: "sha256:c07c42ac7405f527fa9c4ae0c13fb6b81bf82704a52788b88c9b5f5176b656c1"
observation_id: obs_701b2c99af4b11fa199450b67d47c93ba5d551fde5a27d1a16b91384ae7a32ca
event_id: evt_a8ae3d78f2ba1c8a60fea254ecd5f1c4e88ec66c935f9a9f50437c62b54fad5a
revision_id: rev_05b8d0aaf8ce399ad039d18ce6b8ea6f0212c8712d687d6807b9ec7811cdcc8a
source_published_at: 2026-09-28T17:59:36Z
first_seen_at: 2026-09-30T00:26:38.498195Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
interpretation_sha256: "sha256:ed81f8edef5a5176a7a38839a6cd15d870de306c2fcc0cc53ce2fbdfc947bb23"
description: "该研究提出在统一的多模模型内部，通过跨轮强化学习让模型的“反思”文本与图像生成同步优化，实现自我诊断与修订，而无需外部评判器。"
external_url: http://arxiv.org/abs/2609.35767v1
parent_observation_id: null
last_seen_at: 2026-09-30T00:26:38.498195Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.35767v1](http://arxiv.org/abs/2609.35767v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Yijia Fan、Ziqi Huang、Zhongang Cai 等

## 要点解读

### 这是什么
该研究提出在统一的多模模型内部，通过跨轮强化学习让模型的“反思”文本与图像生成同步优化，实现自我诊断与修订，而无需外部评判器。

### 用在哪里
适用于需要模型在生成过程中自行发现并纠正错误的图像生成任务，尤其是统一处理视觉与语言的多模态系统。模型研发者和自动化评测平台可参考此方法提升生成质量。

### 可以推断的
推测：在需要多轮细化的长流程图像生成场景中，这种联合优化方式可能带来更显著的提升。  
推测：由于推理时不再依赖额外的验证模型，整体计算开销和响应延迟有望降低，适合对实时性有要求的应用。

## 来源摘要/节选

> Unified multimodal models can both look at and render images, so in principle they can repair their own generations: diagnose what an image gets wrong, revise it, observe the result, and diagnose again. Whether a revision helps is known only after it is rendered, so the reflection text and the image generation must be learned jointly, over the whole loop. Supervised fine-tuning (SFT) on reflection trajectories gives a cold start but does not find the high-success repair paths, and naive RL that optimizes only the renderer or only one head leaves most of the gain untapped. We introduce UMM-Reflection, which applies reinforcement learning (RL) to complete reflection trajectories inside one unified model: sibling trajectories share one initial image, so the group-relative advantage compares reflection strategies, and one trajectory-level advantage updates both the reflection tokens and the flow-based revisions, avoiding the combinatorial blow-up of per-round credit assignment. Unlike single-round editing or pipelines with an external critic, credit flows across rounds and to both roles of the same model, and no verifier is needed at inference. On BAGEL, UMM-Reflection improves GenEval by 12.05 points over SFT, and the gains transfer to WISE (+10.97), OneIG-Bench (+3.48), and T2I-CompBench++ (+4.63), none of which is used in training.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。