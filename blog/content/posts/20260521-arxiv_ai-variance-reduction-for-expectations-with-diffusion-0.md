---
title: Variance Reduction for Expectations with Diffusion Teachers
date: 2026-05-21 20:21:46+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2605.21489v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1bb745a04ba6c707c0d5db3dc77a63c0f1a1a901711758e9104e682407d3b840
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 59
captured_at: '2026-07-18T04:29:43.284780Z'
source_capture_sha256: sha256:86d8b8e2eaecb6386abd2c6cadd335fc7f6409c64e8b5275f8a4214acf68a02c
source_capture_chars_original: 1091
source_publication_excerpt_chars: 1091
observation_id: obs_ed13c4951b15a505563b802a09039f4ca8dd38fe07205ad865fa6b7e959c60c3
revision_id: rev_8c9700612fa5cf50dc28d08f55669140f77077af4d0855c489a76c7f71385ad9
event_id: evt_6dbf283507562f5b945e663334472d95cecc0e4faf30a68b9f476a7cf739fb13
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-21T04:50:42Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.21489v1](<https://arxiv.org/abs/2605.21489v1>)
- **作者**: Jesse Bettencourt, Xindi Wu, Matan Atzmon, James Lucas, Jonathan Lorraine
- **分类**: cs.LG
- **论文时间**: 2026-05-20T17:59:52Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.21489v1.pdf](<https://arxiv.org/pdf/2605.21489v1.pdf>)

## 来源摘要/节选

> Pretrained diffusion models serve as frozen teachers feeding downstream pipelines such as text-to-3D, single-step distillation, and data attribution. The teacher gradients these pipelines consume are Monte Carlo \(MC\) expectations over noise levels and Gaussian noise samples; their estimator variance dominates compute cost because each draw requires expensive upstream work \(rendering, simulation, encoding\). We introduce CARV, a compute-aware variance-accounting framework that motivates a hierarchical MC estimator: amortize the expensive upstream computation over cheap diffusion-noise resamples, sharpened by timestep importance sampling and a stratified-inverse-CDF construction. In our text-to-3D distillation and attribution experiments, CARV delivers 2-3x effective compute multipliers \(most from amortized reuse; ~25% additional from IS+stratification\) without changing the objective; in single-step distillation, the same techniques cut gradient variance by an order of magnitude but do not improve downstream FID, marking the regime where MC variance is no longer the bottleneck.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
