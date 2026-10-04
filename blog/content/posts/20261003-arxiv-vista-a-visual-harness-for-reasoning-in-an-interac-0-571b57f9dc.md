---
title: "VISTA: A Visual Harness for Reasoning in an Interactive World"
date: 2026-10-03T20:36:59+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:382f7fffa32ca2c446ee7c0b9b738e0ac93b711cac6f4966c4d728c81970c245"
source_payload_sha256: "sha256:2674f51cb7bcbf633e077c8d88f638b35a7210ffed8ad3e6b3c1e1b3e5692d47"
observation_id: obs_571b57f9dc0e13fc9c0c934ff43dd3820827e6a251c2d42fc8fc591edf39803f
event_id: evt_f3adf15b415669ee4a7c54f7d24a92e5b0dfd46419daab733b43ae21d8fcd43b
revision_id: rev_bc8373779395fb46bf58eecde9c908e3ba7dcba4c38386a32615064d47eea4eb
source_published_at: 2026-10-01T17:59:45Z
first_seen_at: 2026-10-03T12:47:42Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
interpretation_sha256: "sha256:ab883f3102284df6e581ac4053cf6930d72ccdbf71211f471e606d39784b7ff9"
description: "VISTA 是一种视觉框架，让通用多模态模型获得长时间视觉感知能力，并通过无损视觉记忆保留过去观察，使模型能够在推理过程中主动检索并重组视觉输入。"
external_url: http://arxiv.org/abs/2610.02200v1
parent_observation_id: null
last_seen_at: 2026-10-04T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02200v1](http://arxiv.org/abs/2610.02200v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Qiushi Han、Keya Hu、Linlu Qiu 等

## 要点解读

### 这是什么
VISTA 是一种视觉框架，让通用多模态模型获得长时间视觉感知能力，并通过无损视觉记忆保留过去观察，使模型能够在推理过程中主动检索并重组视觉输入。

### 用在哪里
适用于需要在交互式视觉环境中完成长序列任务的多模态智能体研究，也适合作为视觉推理基准的评测工具。

### 可以推断的
推测：通过对视觉信息的持续保存和按需检索，模型能够更好地完成跨步骤的规划与纠错。  
推测：由于保持了原始形式的视觉记忆，框架在迁移到不同视觉游戏或谜题时所需的适配成本较低。

## 来源摘要/节选

> We show that multimodal models possess strong reasoning abilities and that an appropriate harness can unlock their potential to solve tasks across diverse interactive environments. We introduce VISTA, a visual harness that gives a general-purpose multimodal model long-horizon vision. VISTA allows the model to directly perceive the environment through visual observations and maintains a lossless visual memory that preserves past observations in their original form. The model can actively retrieve these observations and reorganize its visual input as it reasons. On ARC-AGI-3, VISTA improves Claude Opus 5.0's Relative Human Action Efficiency score from 40.68 to a perfect 100.00, with the model completing all 25 public games using 57.4% fewer actions than first-time human participants. VISTA's simple design also allows it to extend naturally to diverse visual environments with minimal adaptation. Across three additional benchmarks covering a diverse range of visual games and puzzles, it substantially outperforms baselines using the same underlying model with minimal harnesses. Our results highlight VISTA's potential as a general-purpose visual harness for advancing multimodal agents in complex visual environments.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。