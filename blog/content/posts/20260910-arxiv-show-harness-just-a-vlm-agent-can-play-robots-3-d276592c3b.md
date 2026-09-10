---
title: "Show-Harness: Just a VLM Agent Can Play Robots"
date: 2026-09-10T17:46:39+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b97160a4eeab0d311c920a71e0ee3e48758d7bcd4ec2eebad0735798ecfaf120"
source_payload_sha256: "sha256:8d014aea44980269d2479ca9d74323ac660b702ff53a10dd81e212b315c06fcc"
observation_id: obs_d276592c3b006a368d754ae8fac7c1036d8d0e9d427f2d27f21a260558fe1bd4
event_id: evt_78fddf4e7b4d48cead00d4750b3eb37874315caea54b0da2c8c08662c32dfd5f
revision_id: rev_1803aab87d497f3194933cef7c7d5832bc5c73419ced07998a97074597054356
source_published_at: 2026-09-09T17:53:38Z
first_seen_at: 2026-09-10T09:43:38.633286Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 46
interpretation_sha256: "sha256:b7f4144e69e283efe710ec87432c3565b66c2389926c30fe06c19428d2d95b2a"
description: "Show‑Harness 是一个具身化接口，把视觉语言模型的意图通过离散语义动作单元映射为机器人本体的具体动作，使模型能够直接负责细粒度的物理决策。同一接口还能让闭源前沿模型实现零样本控制，或用少量 GPU 小时对开源小模型进行适配。"
external_url: http://arxiv.org/abs/2609.10522v1
parent_observation_id: null
last_seen_at: 2026-09-10T09:43:38.633286Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.10522v1](http://arxiv.org/abs/2609.10522v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Yanzhe Chen、Zechen Bai、Zhijun Cao 等

## 要点解读

### 这是什么  
Show‑Harness 是一个具身化接口，把视觉语言模型的意图通过离散语义动作单元映射为机器人本体的具体动作，使模型能够直接负责细粒度的物理决策。同一接口还能让闭源前沿模型实现零样本控制，或用少量 GPU 小时对开源小模型进行适配。  

### 用在哪里  
适用于需要在多种机器人本体和环境中快速验证视觉语言模型控制能力的研究团队，或在没有专用遥操作硬件的情况下收集演示数据的开发者。  

### 可以推断的  
- 推测：该框架在资源受限或需要快速迭代的项目中具有较高的实用价值。  
- 推测：接口的语义粒度可能影响模型对复杂长时序任务的表现。

## 来源摘要/节选

> Foundation vision-language models (VLMs) exhibit broad intelligence about the world, yet translating this intelligence into robot control remains challenging. We present Show-Harness, an Embodied Harness that enables VLMs to "play" robots through a compact semantic interface linking intent to action. Show-Harness exposes discrete semantic action units that VLMs can naturally reason over, while embodiment-specific interpreters deterministically ground them into local robot actions, keeping the VLM directly responsible for fine-grained physical decisions. Through the same interface, Show-Harness demonstrates the feasibility of (1) directly unlocking closed-source frontier VLMs for zero-shot robot control, and (2) adapting small-scale open-source VLMs for low-cost deployment with just a few GPU-hours of fine-tuning. We further develop GUMI (GUI Manipulation Interface), which extends the same semantic action space to GUI-based demonstration collection, allowing humans and agents to "play" robots across embodiments without specialized teleoperation hardware. Extensive experiments show that Show-Harness-equipped VLM agents generalize robustly across tasks, embodiments, and environments, outperforming representative agentic and VLA paradigms. These results suggest that the right interface can unlock substantial embodied capability from foundation VLMs, without requiring additional model capacity or costly embodiment-specific pretraining.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。