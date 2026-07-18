---
title: 'Late Breaking Results: Conversion of Neural Networks into Logic Flows for
  Edge Computing'
date: 2026-01-30 23:03:03+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.22151v1
aliases:
- /posts/20260131-arxiv_ai-late-breaking-results-conversion-of-neural-network-5/
- /posts/20260201-arxiv_ai-late-breaking-results-conversion-of-neural-network-5/
- /posts/20260202-arxiv_ai-late-breaking-results-conversion-of-neural-network-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:3d5900ff53315af01f264117e5117cb27c14df14fa89584a77ca6c5f9f3ea47b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 88
captured_at: '2026-07-18T04:09:52.752345Z'
source_capture_sha256: sha256:393d9884a18095f4b6e39bdf3150f2450bbec1b5d60aebebd45f56e0484b3a9c
source_capture_chars_original: 1139
source_publication_excerpt_chars: 1139
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.22151v1](<https://arxiv.org/abs/2601.22151v1>)
- **作者**: Daniel Stein, Shaoyi Huang, Rolf Drechsler, Bing Li, Grace Li Zhang
- **分类**: cs.LG
- **论文时间**: 2026-01-29T18:59:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.22151v1.pdf](<https://arxiv.org/pdf/2601.22151v1.pdf>)

## 来源摘要/节选

> Neural networks have been successfully applied in various resource-constrained edge devices, where usually central processing units \(CPUs\) instead of graphics processing units exist due to limited power availability. State-of-the-art research still focuses on efficiently executing enormous numbers of multiply-accumulate \(MAC\) operations. However, CPUs themselves are not good at executing such mathematical operations on a large scale, since they are more suited to execute control flow logic, i.e., computer algorithms. To enhance the computation efficiency of neural networks on CPUs, in this paper, we propose to convert them into logic flows for execution. Specifically, neural networks are first converted into equivalent decision trees, from which decision paths with constant leaves are then selected and compressed into logic flows. Such logic flows consist of if and else structures and a reduced number of MAC operations. Experimental results demonstrate that the latency can be reduced by up to 14.9 % on a simulated RISC-V CPU without any accuracy degradation. The code is open source at https://github.com/TUDa-HWAI/NN2Logic

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
