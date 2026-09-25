---
title: "Temporal Gradient Inversion for Private Trajectory Reconstruction in Embodied Reinforcement Learning"
date: 2026-09-26T02:37:47+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:cfdf0c6eeed04fc9b525093e6decec2363dafc807634245633052da91808d6dd"
source_payload_sha256: "sha256:3ad3694cfcaf0a1e7cd98c9db45781eb6ec6c5fbb0aff63b13fcbe03dcd157f9"
observation_id: obs_7f3c8a336f364d6f3e853e328fa746248619e501c6e93d9da2caf5e2ac0197fb
event_id: evt_3ca9d732643e252305f5cd833decee6be6bde1e8c12fc2736cb418356f9831b3
revision_id: rev_c5ede78ed4051bdc7412c22924b8e68472e977ca8aa5f84efb94a999cd7c5e3a
source_published_at: 2026-09-24T17:59:18Z
first_seen_at: 2026-09-25T18:48:57Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 100
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.30258v1
parent_observation_id: null
last_seen_at: 2026-09-25T18:35:58.796810Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.30258v1](http://arxiv.org/abs/2609.30258v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Sudip Bhujel、Shanghao Shi、Ruiquan Huang 等

## 来源摘要/节选

> Distributed learning in embodied reinforcement-learning agents offers a degree of privacy by retaining raw sensor data on-device and transmitting only policy gradients to the server. Yet temporal structure can amplify this leakage beyond single-frame attacks. We introduce Temporal Reconstruction Attack on Consecutive Encodings (TRACE), an amortized temporal gradient-inversion attack that autoregressively reconstructs the sequence of private observation-action trajectories from per-step policy-learning gradients. The attack exploits two structural signals ignored by prior single-frame methods: (i) cross-time correlation between successive embodied gradients, which we formalize via a conditional mutual-information bound, and (ii) closed-form action recovery from policy-head gradient structure, which we prove exact when standard entropy regularization is sufficiently small. On held-out embodied scenes, TRACE reaches $18.8$ dB PSNR with near-perfect action recovery at $3$-$4.5$ ms per reconstructed frame, dominating the learning-based baseline across all reconstruction metrics and exceeding optimization attacks while running orders of magnitude faster. Further evaluation demonstrates TRACE's broader applicability across recurrent, residual, and compact transformer victim architectures, multi-modal inputs, and larger discrete action spaces. Defense experiments suggest that protecting temporal gradient streams may require sequence-aware privacy mechanisms.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。