---
title: Speculative Speculative Decoding
date: 2026-03-04 22:47:33+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.03251v1
aliases:
- /posts/20260305-arxiv_ai-speculative-speculative-decoding-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a7f3485b6dff7c36b2c77526858bd1a2d6b79087df4f2c1b2d687c6b09670c98
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 32
captured_at: '2026-07-18T04:26:49.920939Z'
source_capture_sha256: sha256:cac2eb13b69a1be332fc587eb07a9f5a6f4e229095b93bc657a9f78a9180f6e7
source_capture_chars_original: 1121
source_publication_excerpt_chars: 1121
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03251v1](<https://arxiv.org/abs/2603.03251v1>)
- **作者**: Tanishq Kumar, Tri Dao, Avner May
- **分类**: cs.LG
- **论文时间**: 2026-03-03T18:41:32Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03251v1.pdf](<https://arxiv.org/pdf/2603.03251v1.pdf>)

## 来源摘要/节选

> Autoregressive decoding is bottlenecked by its sequential nature. Speculative decoding has become a standard way to accelerate inference by using a fast draft model to predict upcoming tokens from a slower target model, and then verifying them in parallel with a single target model forward pass. However, speculative decoding itself relies on a sequential dependence between speculation and verification. We introduce speculative speculative decoding \(SSD\) to parallelize these operations. While a verification is ongoing, the draft model predicts likely verification outcomes and prepares speculations pre-emptively for them. If the actual verification outcome is then in the predicted set, a speculation can be returned immediately, eliminating drafting overhead entirely. We identify three key challenges presented by speculative speculative decoding, and suggest principled methods to solve each. The result is Saguaro, an optimized SSD algorithm. Our implementation is up to 2x faster than optimized speculative decoding baselines and up to 5x faster than autoregressive decoding with open source inference engines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
