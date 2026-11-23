---
title: "Non-penetrating World Models"
date: 2026-11-24T05:21:02+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9cfe159e5c167e401863a5627b4e3c3d439da22ab5132e9de793a63295e0b1b9"
source_payload_sha256: "sha256:2117f1b91c3dab198a981fd391dfda3ce3c6d1e7ecaab5769bb89c73ac608f66"
observation_id: obs_f95ee8b0395d4a37bee7b13031110d867885fe36e57148c60fbb0e31d5c74a7c
event_id: evt_f5825fb286cfea1531a3fd9e880ae439c651d3f5f76f7f1d67a51d4ed0cad04a
revision_id: rev_fc8e1a9b4a381072e104b128f4e5bb49ca6b1dddc430d87cbd8301678f07977e
source_published_at: 2026-11-20T18:44:57Z
first_seen_at: 2026-11-23T21:19:42.181819Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 28
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.27963v1
parent_observation_id: null
last_seen_at: 2026-11-23T21:19:42.181819Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.27963v1](http://arxiv.org/abs/2611.27963v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Yuhang Dai、Yinwei Wu、Ziyue Lin 等

## 来源摘要/节选

> We study a new problem of preventing object penetration in interactive video world models. To understand how existing models handle this, we introduce NoPeBench, a benchmark that evaluates how world models respond to physical obstacles. Our evaluation reveals that none of the open-source models can reliably prevent such failures. Surprisingly, however, these models already encode the information needed to predict such violations. We find that the hidden states of diffusion transformers (DiTs) can predict whether a candidate action will penetrate an obstacle. Building on this, we introduce NoPeWorld, a lightweight framework that detects and prevents penetration. Specifically, we train a small prediction head on top of a frozen DiT's hidden states to read out if a candidate action is safe or not. Unsafe actions are then replaced with safe ones that best preserve the original intent. Despite its simplicity, NoPeWorld substantially reduces the physical violation rate, averaged over six video world models, from 74% to 16%. Remarkably, our method shows zero-shot generalization to open-domain imagery, third-person viewpoints, and moving obstacles. We publicly release our code, the NoPeBench benchmark, and model weights. Project Page: https://nopeworld.github.io .

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。