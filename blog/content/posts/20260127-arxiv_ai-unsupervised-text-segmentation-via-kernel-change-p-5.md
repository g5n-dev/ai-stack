---
title: Unsupervised Text Segmentation via Kernel Change-Point Detection on Sentence
  Embeddings
date: 2026-01-27 23:10:51+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
- Swift
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.18788v1
aliases:
- /posts/20260128-arxiv_ai-unsupervised-text-segmentation-via-kernel-change-p-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2faa33d573f216ca4389da2b34ee149cbaa5293e6e0ec3cca89cd7c4745d3518
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
captured_at: '2026-07-18T04:09:18.936370Z'
source_capture_sha256: sha256:4645338eff4d0cbfaf91b9aaf5bb88a0cc03cac993aceba3e359bf200ea40aa5
source_capture_chars_original: 1235
source_publication_excerpt_chars: 1235
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.18788v1](<https://arxiv.org/abs/2601.18788v1>)
- **作者**: Mumin Jia, Jairo Diaz-Rodriguez
- **分类**: cs.CL
- **论文时间**: 2026-01-26T18:54:34Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.18788v1.pdf](<https://arxiv.org/pdf/2601.18788v1.pdf>)

## 来源摘要/节选

> Unsupervised text segmentation is crucial because boundary labels are expensive, subjective, and often fail to transfer across domains and granularity choices. We propose Embed-KCPD, a training-free method that represents sentences as embedding vectors and estimates boundaries by minimizing a penalized KCPD objective. Beyond the algorithmic instantiation, we develop, to our knowledge, the first dependence-aware theory for KCPD under $m$-dependent sequences, a finite-memory abstraction of short-range dependence common in language. We prove an oracle inequality for the population penalized risk and a localization guarantee showing that each true change point is recovered within a window that is small relative to segment length. To connect theory to practice, we introduce an LLM-based simulation framework that generates synthetic documents with controlled finite-memory dependence and known boundaries, validating the predicted scaling behavior. Across standard segmentation benchmarks, Embed-KCPD often outperforms strong unsupervised baselines. A case study on Taylor Swift's tweets illustrates that Embed-KCPD combines strong theoretical guarantees, simulated reliability, and practical effectiveness for text segmentation.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
