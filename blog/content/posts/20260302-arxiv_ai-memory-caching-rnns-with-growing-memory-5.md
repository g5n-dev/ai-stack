---
title: 'Memory Caching: RNNs with Growing Memory'
date: 2026-03-02 23:25:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.24281v1
aliases:
- /posts/20260303-arxiv_ai-memory-caching-rnns-with-growing-memory-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ea333c125e9aaff81aabf8d6d9403cd955a23217dc04bdfef5987cfb6386cea3
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 40
captured_at: '2026-07-18T04:26:12.126510Z'
source_capture_sha256: sha256:5ccb400cfe7faf074855055a816ee72e7703ec17431322704ba0ab78f1711fd4
source_capture_chars_original: 1563
source_publication_excerpt_chars: 1563
observation_id: obs_310798776a118132e5939528d4fd90808633c752aa0a9427377ca254a8649655
revision_id: rev_0040fbcc23449ee28f7c7f7212fcceb9a798bb6dbdc53c4a28b8678459a04dc5
event_id: evt_39d8d83b86a0c2eed9ab01e13813242a40fc781cde627a2a4267fe94fc49c67f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-02T06:24:05Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24281v1](<https://arxiv.org/abs/2602.24281v1>)
- **作者**: Ali Behrouz, Zeman Li, Yuan Deng, Peilin Zhong, Meisam Razaviyayn, Vahab Mirrokni
- **分类**: cs.LG
- **论文时间**: 2026-02-27T18:53:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24281v1.pdf](<https://arxiv.org/pdf/2602.24281v1.pdf>)

## 来源摘要/节选

> Transformers have been established as the de-facto backbones for most recent advances in sequence modeling, mainly due to their growing memory capacity that scales with the context length. While plausible for retrieval tasks, it causes quadratic complexity and so has motivated recent studies to explore viable subquadratic recurrent alternatives. Despite showing promising preliminary results in diverse domains, such recurrent architectures underperform Transformers in recall-intensive tasks, often attributed to their fixed-size memory. In this paper, we introduce Memory Caching \(MC\), a simple yet effective technique that enhances recurrent models by caching checkpoints of their memory states \(a.k.a. hidden states\). Memory Caching allows the effective memory capacity of RNNs to grow with sequence length, offering a flexible trade-off that interpolates between the fixed memory \(i.e., $O\(L\)$ complexity\) of RNNs and the growing memory \(i.e., $O\(L^2\)$ complexity\) of Transformers. We propose four variants of MC, including gated aggregation and sparse selective mechanisms, and discuss their implications on both linear and deep memory modules. Our experimental results on language modeling, and long-context understanding tasks show that MC enhances the performance of recurrent models, supporting its effectiveness. The results of in-context recall tasks indicate that while Transformers achieve the best accuracy, our MC variants show competitive performance, close the gap with Transformers, and performs better than state-of-the-art recurrent models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
