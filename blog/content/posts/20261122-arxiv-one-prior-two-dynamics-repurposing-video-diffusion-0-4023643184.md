---
title: "One Prior, Two Dynamics: Repurposing Video Diffusion Transformers for Self-Supervised Latent Action Learning"
date: 2026-11-22T01:31:22+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:73f97c85047baada60193232390224478d7888f2725f384e3ed4af19878ebebf"
source_payload_sha256: "sha256:71131a51ff61757bab9a92bcd640f028bf762451daab9b8f3c8de3222d661630"
observation_id: obs_4023643184071d721debc4864ba5ed4b0c2e92c18739d55eb16d2c9b2172ef7c
event_id: evt_277c93c14d3fcb3c06d3a0b60d4cbb3c71108fbeae17286688585ae1b90db0cb
revision_id: rev_d88bb9d34be56dafac41bc167b45029af16b7cbf3348a6cca15bc40c4962e4e0
source_published_at: 2026-11-19T18:58:14Z
first_seen_at: 2026-11-21T17:40:57Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 108
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.26617v1
parent_observation_id: null
last_seen_at: 2026-11-22T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26617v1](http://arxiv.org/abs/2611.26617v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Yuxin Jiang、Wenqiang Sun、Jiaqi Li 等

## 来源摘要/节选

> Videos reveal how the world changes, but rarely the actions that cause those changes. Latent action learning recovers such supervision from visual transitions, yet often learns the underlying dynamics largely from scratch. We ask whether a pretrained video generator can instead provide the prior for both inverse and forward dynamics. We introduce O$^{2}$LaF, built on a simple principle: one prior, two dynamics. We initialize both models from the same pretrained video DiT and adapt them to their distinct roles: a feed-forward transition encoder with learnable action queries for inverse dynamics, and a causal, action-conditioned video generator for forward dynamics. By controlling information access and optimizing both dynamics end-to-end through a compact bottleneck, O$^{2}$LaF learns transferable actions from unlabeled videos. Across navigation and robotic manipulation, O$^{2}$LaF sets a new state of the art in few-shot action probing and enables stronger zero-shot action transfer across visual contexts and embodiments. Beyond generative video priors, we further extend our framework to predictive representation priors such as V-JEPA2, achieving competitive performance. Our findings suggest a broader paradigm for latent-action learning: repurposing pretrained video models to discover transferable actions and predict their consequences.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。