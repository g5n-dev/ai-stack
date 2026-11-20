---
title: "RL Post-Training in Diffusion Transformers Is Activation Steering"
date: 2026-11-20T19:36:41+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "Prompt 工程", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e1a767b564fecb62ee5cbad4148cf2c9d6dff785499a2ced6727067c88cfd466"
source_payload_sha256: "sha256:e7b19b3db62e778f752a783ef3126c405649902594c507940d52d0e289da274c"
observation_id: obs_63c5d50779da2bd3dfc80136fee7a4da67e9695fc57c45246765155aca1377d5
event_id: evt_d7f771bf1e4b9e01a78d5a1c9791c3dbb6de55c4f020e53a4456a193e7b0cdeb
revision_id: rev_5c7595d4fae05bd6ffcf6a86a968a7c14de2a38c0a7d7dd2a08e470ceafb30e3
source_published_at: 2026-11-19T18:59:53Z
first_seen_at: 2026-11-20T11:45:52Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.26627v1
parent_observation_id: null
last_seen_at: 2026-11-20T11:35:05.184789Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26627v1](http://arxiv.org/abs/2611.26627v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Tuna Han Salih Meral、Kaan Oktay、Alec Helbling 等

## 来源摘要/节选

> Reinforcement learning (RL) post-training substantially improves the visual quality, text rendering, and compositional accuracy of diffusion transformers. Because capabilities such as rendering requested text or composing multiple objects are inherently prompt-dependent, a natural hypothesis is that improving them requires learning complex, input-dependent transformations. To isolate how much of these gains an input-independent shift explains, we probe each RL-tuned model with a deliberately simple parameterization: a fixed set of steering vectors added to the block outputs of the frozen base model. On SD3.5-M, these vectors hold 65x fewer parameters than the RL-tuned LoRA (0.29M against 18.8M). We fit them to match the velocity predictions of public RL-tuned checkpoints, with no reward in the objective. Although the vectors are identical for every prompt, token, and sampling seed, they recover 90.0-96.3% of the reward gains of six RL-tuned image models, and 89.8% and 111.9% on two RL-tuned video models. Initialized at zero and trained with online RL, the vectors alone exceed the reward gains of weight-based RL on text rendering (OCR) and human preference (PickScore) on SD3.5-M. A constant shift thus suffices for most of the gain of policy-gradient RL post-training: without new input-dependent transformations, it steers the pretrained generator toward what it can already compute.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。