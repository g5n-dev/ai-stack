---
title: 'Efficient Sampling with Discrete Diffusion Models: Sharp and Adaptive Guarantees'
date: 2026-02-17 22:35:47+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.15008v1
aliases:
- /posts/20260218-arxiv_ai-efficient-sampling-with-discrete-diffusion-models--9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c33e3f5f0c1a3d6add4b90c54b96dd941b30f65b2dae8db38499c496e863ebce
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
captured_at: '2026-07-18T04:15:37.655804Z'
source_capture_sha256: sha256:869ea095f3fea08f7733c7f1f5755f05f95f8db61ecab686665c717458804d22
source_capture_chars_original: 1614
source_publication_excerpt_chars: 1614
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15008v1](<https://arxiv.org/abs/2602.15008v1>)
- **作者**: Daniil Dmitriev, Zhihan Huang, Yuting Wei
- **分类**: cs.LG
- **论文时间**: 2026-02-16T18:48:17Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15008v1.pdf](<https://arxiv.org/pdf/2602.15008v1.pdf>)

## 来源摘要/节选

> Diffusion models over discrete spaces have recently shown striking empirical success, yet their theoretical foundations remain incomplete. In this paper, we study the sampling efficiency of score-based discrete diffusion models under a continuous-time Markov chain \(CTMC\) formulation, with a focus on $τ$-leaping-based samplers. We establish sharp convergence guarantees for attaining $\\varepsilon$ accuracy in Kullback-Leibler \(KL\) divergence for both uniform and masking noising processes. For uniform discrete diffusion, we show that the $τ$-leaping algorithm achieves an iteration complexity of order $\\tilde O\(d/\\varepsilon\)$, with $d$ the ambient dimension of the target distribution, eliminating linear dependence on the vocabulary size $S$ and improving existing bounds by a factor of $d$; moreover, we establish a matching algorithmic lower bound showing that linear dependence on the ambient dimension is unavoidable in general. For masking discrete diffusion, we introduce a modified $τ$-leaping sampler whose convergence rate is governed by an intrinsic information-theoretic quantity, termed the effective total correlation, which is bounded by $d \\log S$ but can be sublinear or even constant for structured data. As a consequence, the sampler provably adapts to low-dimensional structure without prior knowledge or algorithmic modification, yielding sublinear convergence rates for various practical examples \(such as hidden Markov models, image data, and random graphs\). Our analysis requires no boundedness or smoothness assumptions on the score estimator beyond control of the score entropy loss.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
