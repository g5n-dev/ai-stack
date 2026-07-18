---
title: Influence Guided Sampling for Domain Adaptation of Text Retrievers
date: 2026-01-30 03:54:32+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.21759v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1972242e732fa94d21d5bef7e4022d330f53f63cb8194f50c8519db3b1dde6f5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 66
captured_at: '2026-07-18T04:09:52.752345Z'
source_capture_sha256: sha256:f5ff653b1547cac5fba2eb802e5e75a440ecdf2c61829df227bd1160ccffbc78
source_capture_chars_original: 1454
source_publication_excerpt_chars: 1454
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.21759v1](<https://arxiv.org/abs/2601.21759v1>)
- **作者**: Meet Doshi, Vishwajeet Kumar, Yulong Li, Jaydeep Sen
- **分类**: cs.IR
- **论文时间**: 2026-01-29T14:14:29Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.21759v1.pdf](<https://arxiv.org/pdf/2601.21759v1.pdf>)

## 来源摘要/节选

> General-purpose open-domain dense retrieval systems are usually trained with a large, eclectic mix of corpora and search tasks. How should these diverse corpora and tasks be sampled for training? Conventional approaches sample them uniformly, proportional to their instance population sizes, or depend on human-level expert supervision. It is well known that the training data sampling strategy can greatly impact model performance. However, how to find the optimal strategy has not been adequately studied in the context of embedding models. We propose Inf-DDS, a novel reinforcement learning driven sampling framework that adaptively reweighs training datasets guided by influence-based reward signals and is much more lightweight with respect to GPU consumption. Our technique iteratively refines the sampling policy, prioritizing datasets that maximize model performance on a target development set. We evaluate the efficacy of our sampling strategy on a wide range of text retrieval tasks, demonstrating strong improvements in retrieval performance and better adaptation compared to existing gradient-based sampling methods, while also being 1.5x to 4x cheaper in GPU compute. Our sampling strategy achieves a 5.03 absolute NDCG@10 improvement while training a multilingual bge-m3 model and an absolute NDCG@10 improvement of 0.94 while training all-MiniLM-L6-v2, even when starting from expert-assigned weights on a large pool of training datasets.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
