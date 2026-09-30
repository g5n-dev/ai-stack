---
title: "LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization"
date: 2026-09-30T21:45:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5429ad25b42e8580ec8f7dd5b0d7a842c0d6d9a86cf32e76a03ac221d4c2b48c"
source_payload_sha256: "sha256:66851779f2f2d9493f307bea851194cffb0729347b9c564df0ac7291775c975c"
observation_id: obs_ff9a484b197856ccd490e50de35d472d44603fe0055fa29c7d4b9f1142dd582f
event_id: evt_3dffa9deceb5c822057d0176afc4f5999d50ef8cd4f0f1ecc3588da18ab3e37c
revision_id: rev_d96c949769991ee72a0e2011a2853526cf608f35b430eeb7660cb0e2a1af20a0
source_published_at: 2026-09-29T17:59:34Z
first_seen_at: 2026-09-30T13:57:06Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.38166v1
parent_observation_id: null
last_seen_at: 2026-09-30T13:42:32.589242Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.38166v1](http://arxiv.org/abs/2609.38166v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Yi Pan、Haocheng Xi、Kan Zhu 等

## 来源摘要/节选

> Recent LLMs increasingly adopt hybrid designs that replace standard attention with linear attention, such as Gated DeltaNet (GDN) and Kimi Delta Attention (KDA). Although they compress the context into a fixed-size recurrent state and substantially reduce the cost of long-context processing, repeatedly reading and updating that state remains a major inference bottleneck. Quantization offers a natural way to reduce this cost, but can significantly degrade model quality, due to the accumulation of rounding errors and the presence of outlier rows and columns in the state. To address these challenges, we propose LeapQuant, a training-free method that achieves near-lossless performance under 8-bit recurrent-state quantization. First, to mitigate error accumulation, we propose per-window quantization, which leaps over a window of tokens and quantizes the state only once at its end. Within a window, outputs are computed from the fixed low-bit state together with high-precision buffered updates. Second, to reduce the error introduced by each quantization, LeapQuant retains the state's largest outliers as a few high-precision Compensator Tokens, which share the update path of real tokens. We then smooth the remaining residual before quantization to further reduce the error. Comprehensive experiments across the Qwen, Kimi, and GLM model families show that LeapQuant substantially reduces memory and compute costs during inference. With accuracy comparable to the FP32 baseline, it achieves average speedups of 2.05--3.70$\times$ at the kernel level and 1.47$\times$ for end-to-end inference on NVIDIA B200, RTX PRO 6000, and RTX 5090 GPUs.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。