---
title: 'PixelGen: Pixel Diffusion Beats Latent Diffusion with Perceptual Loss'
date: 2026-02-03 23:08:59+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.02493v1
aliases:
- /posts/20260204-arxiv_ai-pixelgen-pixel-diffusion-beats-latent-diffusion-wi-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:070812c9f0117e643d8255425eeee7f23f99ad0de33d9c703e645a42ac462abb
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
captured_at: '2026-07-18T04:10:30.388786Z'
source_capture_sha256: sha256:7d1f5ecf2e9b90ad2448ac81aab65a1b097291aa1c199104e6736c9628b6553b
source_capture_chars_original: 1280
source_publication_excerpt_chars: 1280
observation_id: obs_c1f0103730c48aeca5a0f5b295f161c840bc28e7f8569fd318c90284cfc9dc12
revision_id: rev_9252eb87b80dd1558c02c5cf2aa0587c7658d919066734d58ea7d48aeb4ea760
event_id: evt_b0f18f2ab0b877108699b755e16f5c53dc06231dce4169124b88555ce6d26ed1
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.02493v1](<https://arxiv.org/abs/2602.02493v1>)
- **作者**: Zehong Ma, Ruihan Xu, Shiliang Zhang
- **分类**: cs.CV
- **论文时间**: 2026-02-02T18:59:42Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.02493v1.pdf](<https://arxiv.org/pdf/2602.02493v1.pdf>)

## 来源摘要/节选

> Pixel diffusion generates images directly in pixel space in an end-to-end manner, avoiding the artifacts and bottlenecks introduced by VAEs in two-stage latent diffusion. However, it is challenging to optimize high-dimensional pixel manifolds that contain many perceptually irrelevant signals, leaving existing pixel diffusion methods lagging behind latent diffusion models. We propose PixelGen, a simple pixel diffusion framework with perceptual supervision. Instead of modeling the full image manifold, PixelGen introduces two complementary perceptual losses to guide diffusion model towards learning a more meaningful perceptual manifold. An LPIPS loss facilitates learning better local patterns, while a DINO-based perceptual loss strengthens global semantics. With perceptual supervision, PixelGen surpasses strong latent diffusion baselines. It achieves an FID of 5.11 on ImageNet-256 without classifier-free guidance using only 80 training epochs, and demonstrates favorable scaling performance on large-scale text-to-image generation with a GenEval score of 0.79. PixelGen requires no VAEs, no latent representations, and no auxiliary stages, providing a simpler yet more powerful generative paradigm. Codes are publicly available at https://github.com/Zehong-Ma/PixelGen.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
