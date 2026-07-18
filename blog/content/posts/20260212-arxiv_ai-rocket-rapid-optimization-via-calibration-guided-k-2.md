---
title: 'ROCKET: Rapid Optimization via Calibration-guided Knapsack Enhanced Truncation
  for Efficient Model Compression'
date: 2026-02-12 02:48:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.11008v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4617eeb3e3302bb41dd6accc20d492e24386beb1ac767e4ca948640ad8bbbdc1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 110
captured_at: '2026-07-18T04:15:02.573604Z'
source_capture_sha256: sha256:9547141241ebe1d46d2cd4ea7d7063ded9792046e2a8ddba1fd367c93ad1da45
source_capture_chars_original: 1410
source_publication_excerpt_chars: 1410
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11008v1](<https://arxiv.org/abs/2602.11008v1>)
- **作者**: Ammar Ali, Baher Mohammad, Denis Makhov, Dmitriy Shopkhoev, Magauiya Zhussip, Stamatios Lefkimmiatis
- **分类**: cs.LG
- **论文时间**: 2026-02-11T16:34:52Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11008v1.pdf](<https://arxiv.org/pdf/2602.11008v1.pdf>)

## 来源摘要/节选

> We present ROCKET, a training-free model compression method that achieves state-of-the-art performance in comparison with factorization, structured-sparsification and dynamic compression baselines. Operating under a global compression budget, ROCKET comprises two key innovations: First, it formulates layer-wise compression allocation as a multi-choice knapsack problem, selecting the optimal compression level for each layer to minimize total reconstruction error while adhering to a target model size. Second, it introduces a single-step sparse matrix factorization inspired by dictionary learning: using only a small calibration set, it sparsifies weight coefficients based on activation-weights sensitivity and then updates the dictionary in closed form via least squares bypassing iterative optimization, sparse coding, or backpropagation entirely. ROCKET consistently outperforms existing compression approaches across different model architectures at 20-50\\% compression rates. Notably, it retains over 90\\% of the original model's performance at 30\\% compression without any fine-tuning. Moreover, when applying a light fine-tuning phase, recovery is substantially enhanced: for instance, compressing Qwen3-14B to an 8B-parameter model and healing it with just 30 million tokens yields performance nearly on par with the original Qwen3-8B. The code for ROCKET is at github.com/mts-ai/ROCKET/tree/main.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
