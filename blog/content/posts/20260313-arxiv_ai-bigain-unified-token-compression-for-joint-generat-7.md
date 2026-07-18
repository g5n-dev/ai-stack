---
title: 'BiGain: Unified Token Compression for Joint Generation and Classification'
date: 2026-03-13 23:24:24+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.12240v1
aliases:
- /posts/20260314-arxiv_ai-bigain-unified-token-compression-for-joint-generat-7/
- /posts/20260315-arxiv_ai-bigain-unified-token-compression-for-joint-generat-7/
- /posts/20260316-arxiv_ai-bigain-unified-token-compression-for-joint-generat-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f487d63b3b30b4af67a3d0f4a538bae7e777c1cf628c97cc040df293e6718eee
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
captured_at: '2026-07-18T04:28:03.257131Z'
source_capture_sha256: sha256:f325e6081c2c0d27fa3c9166461375ed3543bda6416f188f9d4d7679f16b6dc2
source_capture_chars_original: 1920
source_publication_excerpt_chars: 1920
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.12240v1](<https://arxiv.org/abs/2603.12240v1>)
- **作者**: Jiacheng Liu, Shengkun Tang, Jiacheng Cui, Dongkuan Xu, Zhiqiang Shen
- **分类**: cs.CV
- **论文时间**: 2026-03-12T17:55:53Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.12240v1.pdf](<https://arxiv.org/pdf/2603.12240v1.pdf>)

## 来源摘要/节选

> Acceleration methods for diffusion models \(e.g., token merging or downsampling\) typically optimize synthesis quality under reduced compute, yet often ignore discriminative capacity. We revisit token compression with a joint objective and present BiGain, a training-free, plug-and-play framework that preserves generation quality while improving classification in accelerated diffusion models. Our key insight is frequency separation: mapping feature-space signals into a frequency-aware representation disentangles fine detail from global semantics, enabling compression that respects both generative fidelity and discriminative utility. BiGain reflects this principle with two frequency-aware operators: \(1\) Laplacian-gated token merging, which encourages merges among spectrally smooth tokens while discouraging merges of high-contrast tokens, thereby retaining edges and textures; and \(2\) Interpolate-Extrapolate KV Downsampling, which downsamples keys/values via a controllable interextrapolation between nearest and average pooling while keeping queries intact, thereby conserving attention precision. Across DiT- and U-Net-based backbones and ImageNet-1K, ImageNet-100, Oxford-IIIT Pets, and COCO-2017, our operators consistently improve the speed-accuracy trade-off for diffusion-based classification, while maintaining or enhancing generation quality under comparable acceleration. For instance, on ImageNet-1K, with 70% token merging on Stable Diffusion 2.0, BiGain increases classification accuracy by 7.15% while improving FID by 0.34 \(1.85%\). Our analyses indicate that balanced spectral retention, preserving high-frequency detail and low/mid-frequency semantics, is a reliable design rule for token compression in diffusion models. To our knowledge, BiGain is the first framework to jointly study and advance both generation and classification under accelerated diffusion, supporting lower-cost deployment.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
