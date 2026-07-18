---
title: The Seriality Gap in Video Diffusion Models
date: 2026-07-15 14:00:41+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2607.13031v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7fbc2b51c0ef03afdb79664ec793ea463db948f1e4c6d6e4310be80c516219c7
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 43
captured_at: '2026-07-18T04:30:29.635417Z'
source_capture_sha256: sha256:26bc7554775ec39066dabda8e9354fdb0ff5f43bbe7b2cd46676614ac8f7b424
source_capture_chars_original: 1120
source_publication_excerpt_chars: 1120
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2607.13031v1](<https://arxiv.org/abs/2607.13031v1>)
- **作者**: Jorge Diaz Chao, Konpat Preechakul, Yuxi Liu, Yutong Bai
- **分类**: cs.LG
- **论文时间**: 2026-07-14T17:59:22Z
- **论文 PDF**: [https://arxiv.org/pdf/2607.13031v1.pdf](<https://arxiv.org/pdf/2607.13031v1.pdf>)

## 来源摘要/节选

> When one ball strikes another, then another, video models should predict the consequences of each bounce. In controlled experiments on multi-ball hard-sphere dynamics, we find that the performance of standard bidirectional video diffusion degrades as the causal chain lengthens, even when provided more denoising steps. In a length-matched single-ball control, where ball-ball interactions are absent, the degradation largely disappears, isolating dependent-event structure rather than video length as the cause. Across intervention studies, methods that increase effective serial computation improve performance disproportionately, including autoregressive/blockwise generation and architectural depth. We identify this pattern as the seriality gap: a mismatch between tasks requiring growing serial computation and video diffusion models whose denoising loop does not provide scalable serial compute. We then prove that, for deterministic video prediction, denoising steps do not add serial computation beyond the backbone, indicating a structural obstacle for video diffusion on serial reasoning and simulation tasks.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
