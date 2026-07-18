---
title: Causality in Video Diffusers is Separable from Denoising
date: 2026-02-11 23:34:28+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.10095v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1a971d8d24233933bd8c1674f2ea1066a52bc5faae1ee1aa8c18d3cf05a683cc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 56
captured_at: '2026-07-18T04:14:36.051132Z'
source_capture_sha256: sha256:7ecc8c5c664d552cd77b3f6fa060e99da50424b299ccba8b9e76bdcaace94425
source_capture_chars_original: 1364
source_publication_excerpt_chars: 1364
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.10095v1](<https://arxiv.org/abs/2602.10095v1>)
- **作者**: Xingjian Bai, Guande He, Zhengqi Li, Eli Shechtman, Xun Huang, Zongze Wu
- **分类**: cs.CV
- **论文时间**: 2026-02-10T18:57:21Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.10095v1.pdf](<https://arxiv.org/pdf/2602.10095v1.pdf>)

## 来源摘要/节选

> Causality -- referring to temporal, uni-directional cause-effect relationships between components -- underlies many complex generative processes, including videos, language, and robot trajectories. Current causal diffusion models entangle temporal reasoning with iterative denoising, applying causal attention across all layers, at every denoising step, and over the entire context. In this paper, we show that the causal reasoning in these models is separable from the multi-step denoising process. Through systematic probing of autoregressive video diffusers, we uncover two key regularities: \(1\) early layers produce highly similar features across denoising steps, indicating redundant computation along the diffusion trajectory; and \(2\) deeper layers exhibit sparse cross-frame attention and primarily perform intra-frame rendering. Motivated by these findings, we introduce Separable Causal Diffusion \(SCD\), a new architecture that explicitly decouples once-per-frame temporal reasoning, via a causal transformer encoder, from multi-step frame-wise rendering, via a lightweight diffusion decoder. Extensive experiments on both pretraining and post-training tasks across synthetic and real benchmarks show that SCD significantly improves throughput and per-frame latency while matching or surpassing the generation quality of strong causal diffusion baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
