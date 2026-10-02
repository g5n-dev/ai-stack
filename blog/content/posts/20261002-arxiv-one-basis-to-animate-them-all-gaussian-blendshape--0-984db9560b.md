---
title: "One Basis to Animate Them All: Gaussian Blendshape Distillation for Real-Time Avatars"
date: 2026-10-02T10:17:39+08:00
draft: false
entry_kind: "auto"
tags: ["计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:b640b852cc670da73742e34a5f20c49ae1e4601262a76ec297cbdbcb7ac8c3be"
source_payload_sha256: "sha256:7dbb7c2231f3ae5dbda13b9832cbf50c14892d2f47f8b4cfaddd381af482611b"
observation_id: obs_984db9560b38a6dd6fa05cb53a34d0df886f57f71e63ca479780c7df8b02e956
event_id: evt_6f04178b70f47444e09ed59f222b147174821c510dd931ed87b4b9e68c560d62
revision_id: rev_d4e00ae0af09b61044c3c60dd5828708e9b49501db0efa155d34067592225466
source_published_at: 2026-10-01T17:59:58Z
first_seen_at: 2026-10-02T02:15:24.047089Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
interpretation_sha256: "sha256:b5553e805a1cc44e47f9e17c210342455e70cf715904de70f04bcb000a824052"
description: "该研究提出一种基于线性混合形状的蒸馏方法，用浅层网络预测混合系数并通过线性组合实现三维角色的实时动画，省去逐帧的高开销神经解码。"
external_url: http://arxiv.org/abs/2610.02207v1
parent_observation_id: null
last_seen_at: 2026-10-02T02:15:24.047089Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2610.02207v1](http://arxiv.org/abs/2610.02207v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Ramazan Fazylov、Stamatis Lefkimmiatis、Ivan Laptev

## 要点解读

### 这是什么
该研究提出一种基于线性混合形状的蒸馏方法，用浅层网络预测混合系数并通过线性组合实现三维角色的实时动画，省去逐帧的高开销神经解码。

### 用在哪里
适用于需要高效实时渲染的角色动画系统，特别是移动端或资源受限的设备；可为三维虚拟形象、实时交互或游戏开发者提供参考。

### 可以推断的
推测：线性混合形状的使用可大幅降低计算负载，使在硬件条件有限的平台上仍能实现流畅动画。  
推测：由于采用身份无关的基础表示，该方法可能在不同角色模型之间具有良好的通用性。

## 来源摘要/节选

> 3D Gaussian avatars support fast rendering, however, their real-time animation is often challenged by the costly neural inference. We address this bottleneck and show that the animation of pretrained avatar models can be closely approximated by a linear combination of identity-independent blendshapes. Building on this finding, we introduce GALA (Gaussian Animation via Linear Approximation), a distillation method that replaces per-frame heavy neural decoding with a shallow coefficient predictor and a linear blend. To improve fidelity and reduce memory requirements, we propose to construct the basis using block-local PCA under a rendering-aware metric and a memory budget. Our method learns a shallow MLP network to predict blendshape coefficients and applies to various animation architectures without retraining original models. We validate GALA by accelerating the inference of three distinct avatar models for 3D animation of facial expressions and full-bodies with clothing dynamics. Across these models, our distillation generalizes to held-out identities and reduces CPU animation cost by up to three orders of magnitude while preserving most of the rendering quality. Excellent results of our method confirm the shared linear structure of learned avatar representations and enable highly efficient and accurate animation at frame rates reaching up to 60fps on mobile devices. Project page: https://ramazan793.github.io/gala/

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。