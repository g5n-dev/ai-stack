---
title: "ReWorld: An Interactive World Model with Long-Horizon Memory"
date: 2026-08-25T12:57:25+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:3bef8b3ae0761bcde0a59607c990ff5372ab6e527ccdc9721e57f10cbc325c10"
source_payload_sha256: "sha256:b48ed1b0f08977efd6d77a6a193ba1fc7518841dab6379418e4c1b103c34d46c"
observation_id: obs_d15b95708f3299606b1b77790e5cbef2bb26f79224e6f10a1622f4e3817ed050
event_id: evt_85a1f226aa20c70397deb85fec37e3e0f0f47043e2fa095dbae0d46366450baf
revision_id: rev_dcc0220116c59dd13e14029ccb23cce8851c1a59972221301f70623e20e04957
source_published_at: 2026-08-24T17:59:05Z
first_seen_at: 2026-08-25T04:53:41.410525Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
interpretation_sha256: "sha256:62d008ce318680056dbb232020ad1e59755fb0e000933cd105084312d15973e3"
description: "ReWorld 是一种交互式世界模型，能够在实时视频流中跟踪用户输入并保留对过去场景的长期记忆。它通过在训练阶段区分短期控制与长期记忆、在推理阶段使用受限的键值缓存和姿态索引的地标库来实现这一点，从而在保持响应速度的同时支持分钟级别的回溯。"
external_url: http://arxiv.org/abs/2608.23565v1
parent_observation_id: null
last_seen_at: 2026-08-25T04:53:41.410525Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23565v1](http://arxiv.org/abs/2608.23565v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Zhifei Chen、Luozhou Wang、Guibao Shen 等

## 要点解读

### 这是什么
ReWorld 是一种交互式世界模型，能够在实时视频流中跟踪用户输入并保留对过去场景的长期记忆。它通过在训练阶段区分短期控制与长期记忆、在推理阶段使用受限的键值缓存和姿态索引的地标库来实现这一点，从而在保持响应速度的同时支持分钟级别的回溯。

### 用在哪里
适用于需要持续交互且对历史视觉信息有依赖的场景，例如沉浸式游戏、虚拟现实仿真和机器人决策系统的实时视觉预测。

### 可以推断的
- 推测：由于使用了固定大小的缓存和地标检索机制，即使在显存或计算资源受限的环境中，模型仍能维持长时间记忆而不会因历史信息无限增长导致溢出。  
- 推测：将不同来源的动作尺度统一后，模型可以在多种视觉风格之间迁移，从而提升跨领域的交互体验。

## 来源摘要/节选

> An interactive world model must follow the user's actions, remember the places it has shown, and stream in real time. The tension is structural: control wants a short horizon, memory wants an unbounded one. ReWorld separates the two during training and bounds them at inference. Mixed per-head attention windows confine most heads to the recent past while a small set of global heads attends over the entire history, and random head routing keeps either capability from binding to particular heads; random chunk dropping makes sparse histories in-distribution. At inference the whole past lives under a fixed budget: a bounded KV cache backed by a pose-indexed landmark bank, from which the model retrieves the landmarks nearest the current pose. A metric-scale-aligned data engine places eight sources -- Unreal-rendered fly-throughs, game roaming, and real-world footage -- on one physical action scale, so the same key press moves the camera the same distance in every source, and palindrome trajectories supply the revisit evidence that memory training needs. Distribution-matching distillation confined to a LoRA adapter then compresses sampling to four steps: one backbone serves both a high-fidelity multi-step mode and a real-time interactive one, streaming 704x1280 video across photorealistic, game-style, and stylized worlds. Under a three-axis protocol covering action following, long-horizon recall, and video quality, against six recent interactive world models it attains the best control fidelity ($11.95^\circ$ rotation error and the best camera-motion consistency) and the best generation quality; and on minute-long out-and-back rollouts ($64$\,s, $384$ latents), its fixed 12-chunk cache still regenerates the starting view -- at rollout lengths where a sliding window has long evicted the evidence and full-KV attention runs out of memory.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。