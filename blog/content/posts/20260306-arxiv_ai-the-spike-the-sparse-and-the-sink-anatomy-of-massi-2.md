---
title: 'The Spike, the Sparse and the Sink: Anatomy of Massive Activations and Attention
  Sinks'
date: 2026-03-06 23:44:05+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.05498v1
aliases:
- /posts/20260307-arxiv_ai-the-spike-the-sparse-and-the-sink-anatomy-of-massi-2/
- /posts/20260308-arxiv_ai-the-spike-the-sparse-and-the-sink-anatomy-of-massi-2/
- /posts/20260309-arxiv_ai-the-spike-the-sparse-and-the-sink-anatomy-of-massi-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:93d20031b781a080447f894c8b6cd4a10a844be2c4995b69e52f9c034a3f597d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
captured_at: '2026-07-18T04:27:16.435086Z'
source_capture_sha256: sha256:1a3a9e52b7f0c2c510f33bf913a8ef1a26900c4e1ec743d53b546ff70d85290e
source_capture_chars_original: 1106
source_publication_excerpt_chars: 1106
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.05498v1](<https://arxiv.org/abs/2603.05498v1>)
- **作者**: Shangwen Sun, Alfredo Canziani, Yann LeCun, Jiachen Zhu
- **分类**: cs.AI
- **论文时间**: 2026-03-05T18:59:04Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.05498v1.pdf](<https://arxiv.org/pdf/2603.05498v1.pdf>)

## 来源摘要/节选

> We study two recurring phenomena in Transformer language models: massive activations, in which a small number of tokens exhibit extreme outliers in a few channels, and attention sinks, in which certain tokens attract disproportionate attention mass regardless of semantic relevance. Prior work observes that these phenomena frequently co-occur and often involve the same tokens, but their functional roles and causal relationship remain unclear. Through systematic experiments, we show that the co-occurrence is largely an architectural artifact of modern Transformer design, and that the two phenomena serve related but distinct functions. Massive activations operate globally: they induce near-constant hidden representations that persist across layers, effectively functioning as implicit parameters of the model. Attention sinks operate locally: they modulate attention outputs across heads and bias individual heads toward short-range dependencies. We identify the pre-norm configuration as the key choice that enables the co-occurrence, and show that ablating it causes the two phenomena to decouple.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
