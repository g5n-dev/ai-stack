---
title: Auto-Regressive Masked Diffusion Models
date: 2026-01-26 22:15:20+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.16971v1
aliases:
- /posts/20260127-arxiv_ai-auto-regressive-masked-diffusion-models-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ccf1dd0db10c8599d242259ed0fb2eedfe247cd3801b4138a23ea1f24f9eb509
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 39
captured_at: '2026-07-18T04:09:03.986411Z'
source_capture_sha256: sha256:1d53c5bc448761a885adcad0d5d704118874864cedc414e5f76d53207513d062
source_capture_chars_original: 1519
source_publication_excerpt_chars: 1519
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16971v1](<https://arxiv.org/abs/2601.16971v1>)
- **作者**: Mahdi Karami, Ali Ghodsi
- **分类**: cs.LG
- **论文时间**: 2026-01-23T18:42:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16971v1.pdf](<https://arxiv.org/pdf/2601.16971v1.pdf>)

## 来源摘要/节选

> Masked diffusion models \(MDMs\) have emerged as a promising approach for language modeling, yet they face a performance gap compared to autoregressive models \(ARMs\) and require more training iterations. In this work, we present the Auto-Regressive Masked Diffusion \(ARMD\) model, an architecture designed to close this gap by unifying the training efficiency of autoregressive models with the parallel generation capabilities of diffusion-based models. Our key insight is to reframe the masked diffusion process as a block-wise causal model. This perspective allows us to design a strictly causal, permutation-equivariant architecture that computes all conditional probabilities across multiple denoising steps in a single, parallel forward pass. The resulting architecture supports efficient, autoregressive-style decoding and a progressive permutation training scheme, allowing the model to learn both canonical left-to-right and random token orderings. Leveraging this flexibility, we introduce a novel strided parallel generation strategy that accelerates inference by generating tokens in parallel streams while maintaining global coherence. Empirical results demonstrate that ARMD achieves state-of-the-art performance on standard language modeling benchmarks, outperforming established diffusion baselines while requiring significantly fewer training steps. Furthermore, it establishes a new benchmark for parallel text generation, effectively bridging the performance gap between parallel and sequential decoding.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
