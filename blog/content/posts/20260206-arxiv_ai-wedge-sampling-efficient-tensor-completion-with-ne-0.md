---
title: 'Wedge Sampling: Efficient Tensor Completion with Nearly-Linear Sample Complexity'
date: 2026-02-06 03:10:07+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.05869v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:98b4a1ae9dcf80a0e6ccf83f14cf76cd9190a6002750c6dbffb9a6ebb753f13c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
captured_at: '2026-07-18T04:11:20.263833Z'
source_capture_sha256: sha256:c3db50428c8826eea91017ab5ee8c69a39d55779d55d73dcd8eeeef32dcd631a
source_capture_chars_original: 1546
source_publication_excerpt_chars: 1546
observation_id: obs_739e6d0db37b382a60fc732a06c843bf339f2e7195654d633842db1e17a826a2
revision_id: rev_b69c6912189dedb1ab2ecb382614c8c668a3ad4a8d8db843206c2ab91710d2ba
event_id: evt_507c669a9fa85ab07ce7d61a80fb2df9a91ed09b52ded7f42bb76722f59b44dd
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-06T03:17:20Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.05869v1](<https://arxiv.org/abs/2602.05869v1>)
- **作者**: Hengrui Luo, Anna Ma, Ludovic Stephan, Yizhe Zhu
- **分类**: stat.ML
- **论文时间**: 2026-02-05T16:47:13Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.05869v1.pdf](<https://arxiv.org/pdf/2602.05869v1.pdf>)

## 来源摘要/节选

> We introduce Wedge Sampling, a new non-adaptive sampling scheme for low-rank tensor completion. We study recovery of an order-$k$ low-rank tensor of dimension $n \\times \\cdots \\times n$ from a subset of its entries. Unlike the standard uniform entry model \(i.e., i.i.d. samples from $\[n\]^k$\), wedge sampling allocates observations to structured length-two patterns \(wedges\) in an associated bipartite sampling graph. By directly promoting these length-two connections, the sampling design strengthens the spectral signal that underlies efficient initialization, in regimes where uniform sampling is too sparse to generate enough informative correlations. Our main result shows that this change in sampling paradigm enables polynomial-time algorithms to achieve both weak and exact recovery with nearly linear sample complexity in $n$. The approach is also plug-and-play: wedge-sampling-based spectral initialization can be combined with existing refinement procedures \(e.g., spectral or gradient-based methods\) using only an additional $\\tilde\{O\}\(n\)$ uniformly sampled entries, substantially improving over the $\\tilde\{O\}\(n^\{k/2\}\)$ sample complexity typically required under uniform entry sampling for efficient methods. Overall, our results suggest that the statistical-to-computational gap highlighted in Barak and Moitra \(2022\) is, to a large extent, a consequence of the uniform entry sampling model for tensor completion, and that alternative non-adaptive measurement designs that guarantee a strong initialization can overcome this barrier.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
