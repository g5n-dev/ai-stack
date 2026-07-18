---
title: Leech Lattice Vector Quantization for Efficient LLM Compression
date: 2026-03-12 21:14:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.11021v1
aliases:
- /posts/20260313-arxiv_ai-leech-lattice-vector-quantization-for-efficient-ll-7/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:fa59cc49cb74dbf92d503fdf628a849bef19faa8f87b1cf899c25c728610a337
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
captured_at: '2026-07-18T04:28:03.257131Z'
source_capture_sha256: sha256:7d115b1725f5758e26384cc91d6f569877108d1663e174189c57262681e3b7f7
source_capture_chars_original: 1290
source_publication_excerpt_chars: 1290
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.11021v1](<https://arxiv.org/abs/2603.11021v1>)
- **作者**: Tycho F. A. van der Ouderaa, Mart van Baalen, Paul Whatmough, Markus Nagel
- **分类**: cs.LG
- **论文时间**: 2026-03-11T17:48:45Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.11021v1.pdf](<https://arxiv.org/pdf/2603.11021v1.pdf>)

## 来源摘要/节选

> Scalar quantization of large language models \(LLMs\) is fundamentally limited by information-theoretic bounds. While vector quantization \(VQ\) overcomes these limits by encoding blocks of parameters jointly, practical implementations must avoid the need for expensive lookup mechanisms or other explicit codebook storage. Lattice approaches address this through highly structured and dense packing. This paper explores the Leech lattice, which, with its optimal sphere packing and kissing configurations at 24 dimensions, is the highest dimensional lattice known with such optimal properties. To make the Leech lattice usable for LLM quantization, we extend an existing search algorithm based on the extended Golay code construction, to i\) support indexing, enabling conversion to and from bitstrings without materializing the codebook, ii\) allow angular search over union of Leech lattice shells, iii\) propose fully-parallelisable dequantization kernel. Together this yields a practical algorithm, namely Leech Lattice Vector Quantization \(LLVQ\). LLVQ delivers state-of-the-art LLM quantization performance, outperforming recent methods such as Quip\\#, QTIP, and PVQ. These results highlight the importance of high-dimensional lattices for scalable, theoretically grounded model compression.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
