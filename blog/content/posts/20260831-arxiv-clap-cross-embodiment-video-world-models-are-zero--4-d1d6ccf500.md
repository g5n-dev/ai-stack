---
title: "CLAP: Cross-Embodiment Video World Models are Zero-Shot Physical Simulators"
date: 2026-08-31T05:07:20+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.RO", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:6741b693e18ca548b9323796a632e3a364f835d3b52b033bf74148ef8a8cb530"
source_payload_sha256: "sha256:3fa6dc6577a05d9ab17001ba6e8f3f7c20e0d1b2ec8c5bf372452688e95137ce"
observation_id: obs_d1d6ccf5005ae1befe4f2ffc4f3db5b8212fae636b373ede4ee20231cff4d596
event_id: evt_48b3384b365651364cc8c12453a27ced9b4e9b788d2d3c95f9d43c09b212526e
revision_id: rev_4e0dd7e58055fd4e534d77aa16f0f6d35210be86a9a9a2c951e7ac0d0bd7c28c
source_published_at: 2026-08-27T17:35:10Z
first_seen_at: 2026-08-30T21:04:45.575079Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
interpretation_sha256: "sha256:e8127dcc5401853fc1e6b407ba6ccd2c30afe5b3bcc240d6a527e205a61a19e1"
description: "CLAP 是一种跨机体动作条件视频生成框架，能够在包含人类和机器人动作的多种网络规模视频上进行训练，借助通用物理规律实现对不同形态的行为预测。"
external_url: http://arxiv.org/abs/2608.27406v1
parent_observation_id: null
last_seen_at: 2026-08-30T21:04:45.575079Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.27406v1](http://arxiv.org/abs/2608.27406v1)
- **发布域名**: arxiv.org
- **分类**: cs.RO
- **作者**: Kechen Liu、Ola Shorinwa

## 要点解读

### 这是什么  
CLAP 是一种跨机体动作条件视频生成框架，能够在包含人类和机器人动作的多种网络规模视频上进行训练，借助通用物理规律实现对不同形态的行为预测。

### 用在哪里  
适用于需要通用物理先验的机器人视频世界模型研发，尤其是想在未见过的机器人平台上实现零样本部署的团队；也可以为跨机体的动作模仿和实时仿真提供基础模型。

### 可以推断的  
推测：在大规模未标注视频上先学习潜在动作，再在特定机体上进行末端执行器动作微调的课程式训练，可能兼顾了跨机体的泛化能力和对特定平台的适配精度。  
推测：已在包含 DROID、Bridge、双臂 YAM 机器人及 G1 人形机器人等多种形态的数据上验证，说明其适用范围不局限于单一机器人。

## 来源摘要/节选

> State-of-the-art action-conditioned video models are typically restricted to a single robot embodiment, preventing them from leveraging the vast corpus of heterogeneous video data that contains rich signals for learning generalizable physics. To bridge this gap, we introduce CLAP, a framework for cross-embodiment action-conditioned video generation capable of being trained on diverse, internet-scale videos across human and robotic agents. CLAP is grounded in the insight that universal physical laws govern spatiotemporal dynamics regardless of the actor. However, cross-embodiment learning is non-trivial because action representations vary sharply across robot platforms and are typically absent in human videos. CLAP addresses this fundamental challenge through the following core contributions. First, CLAP reconciles disparate action spaces using end-effector poses, language instructions, and latent actions. Second, to resolve their individual limitations, CLAP introduces a curriculum-based cross-embodiment learning recipe that first learns foundational physical priors across unlabeled video data using latent actions and subsequently grounds them in end-effector action spaces for zero-shot deployment to real-world tasks. Crucially, CLAP approaches or surpasses state-of-the-art single-embodiment video models in challenging environments like DROID. These performance advantages compound via few-shot adaptation to establish a novel paradigm for training single-embodiment video world models. Ultimately, CLAP delivers the most comprehensive suite of action-conditioned video world models to date - spanning diverse action-conditioning spaces (end-effector, language, and latent) and robot morphologies (including cross-embodiment, DROID, Bridge, bimanual YAM robots, and G1 humanoids). We open-source all code and models. Project Website at https://omni-clap.github.io .

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。