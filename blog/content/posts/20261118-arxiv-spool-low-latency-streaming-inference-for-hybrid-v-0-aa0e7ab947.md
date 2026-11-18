---
title: "Spool: Low-Latency Streaming Inference for Hybrid Vision-Language Models"
date: 2026-11-18T21:58:04+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "计算机视觉", "cs.CV", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4266f6e3618f41bbc972bc667cb3b6b6bf60511fc767fe4ebe6f10dc7183f2d9"
source_payload_sha256: "sha256:815cd0da10de22f8bbbb25f745c6bada314902f74edbaa8a6285ca0e1c9ffa3a"
observation_id: obs_aa0e7ab947744a9865e5d99b068d5185f84563f0a8c0f8885050e4157eb7050b
event_id: evt_a5be023a1e4dce95254b73c25b0400273a512383397b1039747e9196fc8004e5
revision_id: rev_3b1e0f1d923bfc6d8511072dd84db338f8627ff734c8cc01360c68c9daa10f03
source_published_at: 2026-11-17T18:59:27Z
first_seen_at: 2026-11-18T13:56:39.057965Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
interpretation_sha256: "sha256:b79d8e4a575331ffe133ee7fac53d27b47b9803902d6b877438d83a52d409455"
description: "Spool 是一种免训练的低延迟流式推理框架，面向结合注意力层与线性循环层的混合视觉语言模型。它缓存各帧对应的状态变换并高效组合，使滑动窗口前移时无需重跑整个视频窗口即可移除过期帧。"
external_url: http://arxiv.org/abs/2611.23228v1
parent_observation_id: null
last_seen_at: 2026-11-18T13:56:39.057965Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.23228v1](http://arxiv.org/abs/2611.23228v1)
- **发布域名**: arxiv.org
- **分类**: cs.CV
- **作者**: Rui Ning、Om Chabra、Hari Balakrishnan

## 要点解读

### 这是什么
Spool 是一种免训练的低延迟流式推理框架，面向结合注意力层与线性循环层的混合视觉语言模型。它缓存各帧对应的状态变换并高效组合，使滑动窗口前移时无需重跑整个视频窗口即可移除过期帧。

### 用在哪里
适用于视觉无障碍代理、机器人等需要围绕近期视频内容快速问答的应用，也适合研究实时视频推理与服务优化的工程团队。

### 可以推断的
- 推测：在 20 组模型与基准测试中均实现最低的首 token 延迟，并优于两种近期 vLLM 基线，说明其工程优化具有较强的实际吸引力。
- 推测：逐层精确移除与跨层残余影响之间的取舍，可能使 Spool 更适合强调响应速度的实时场景，而非追求历史帧影响完全清零。

## 来源摘要/节选

> Applications such as visual accessibility agents and robotics require answering questions about recent video content promptly, over a bounded window of past frames (e.g., the last two minutes). Hybrid vision-language models (VLMs), which interleave attention with linear recurrent layers such as Gated DeltaNet (GDN), are attractive for this setting, but maintaining a sliding window is expensive. The reason is that recurrent layers combine all past frames into a shared state, so expiring old frames normally requires re-running the entire window through the model. We observe that the recurrent update is affine in the state with input-dependent coefficients, so the effect of each frame can be captured as a transformation that composes associatively. We present Spool, a training-free framework that caches per-frame state transformations and composes them efficiently as the window advances, removing expired frames from each recurrent layer's state without replaying frames through the backbone. Removal is exact within each layer; as with key-value eviction in attention, expired frames can retain residual influence through the cached inputs computed by earlier layers. We design a dedicated data structure and GPU kernels to achieve low caching and composition overhead. Across five open-source hybrid VLMs and four video reasoning benchmarks, Spool achieves the lowest p95 time-to-first-token in all 20 model-benchmark tests, reducing it by a geometric mean of $6.6\times$ over the faster of two recent vLLM baselines, while improving accuracy by 2.3 percentage points on average.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。