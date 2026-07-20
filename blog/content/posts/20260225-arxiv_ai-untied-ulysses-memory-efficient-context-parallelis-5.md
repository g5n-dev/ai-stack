---
title: 'Untied Ulysses: Memory-Efficient Context Parallelism via Headwise Chunking'
date: 2026-02-25 23:30:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.21196v1
aliases:
- /posts/20260226-arxiv_ai-untied-ulysses-memory-efficient-context-parallelis-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:bd01288a58f75d51618814fced295f42aaf4b6ae75cbae8fa7ca8a79f8c154af
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
captured_at: '2026-07-18T04:17:01.203007Z'
source_capture_sha256: sha256:dd6923e40b844278eb87c1d71258cb631a3a3af9c1d06cb0b65835f1a2d3c448
source_capture_chars_original: 1235
source_publication_excerpt_chars: 1235
observation_id: obs_98d363ee12ecd13ba4afa74a013f0e8a183dc6c87d7ba78fe961202f7f020a01
revision_id: rev_60b2761b493623fa3f09fe81eb835f0351bca667f6ce721d656f9be279ee0275
event_id: evt_9154e9c30870aa2e59741ee6cc2f0d99a87049485adb99ed223ddbab44a20fff
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.21196v1](<https://arxiv.org/abs/2602.21196v1>)
- **作者**: Ravi Ghadia, Maksim Abraham, Sergei Vorobyov, Max Ryabinin
- **分类**: cs.LG
- **论文时间**: 2026-02-24T18:54:39Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.21196v1.pdf](<https://arxiv.org/pdf/2602.21196v1.pdf>)

## 来源摘要/节选

> Efficiently processing long sequences with Transformer models usually requires splitting the computations across accelerators via context parallelism. The dominant approaches in this family of methods, such as Ring Attention or DeepSpeed Ulysses, enable scaling over the context dimension but do not focus on memory efficiency, which limits the sequence lengths they can support. More advanced techniques, such as Fully Pipelined Distributed Transformer or activation offloading, can further extend the possible context length at the cost of training throughput. In this paper, we present UPipe, a simple yet effective context parallelism technique that performs fine-grained chunking at the attention head level. This technique significantly reduces the activation memory usage of self-attention, breaking the activation memory barrier and unlocking much longer context lengths. Our approach reduces intermediate tensor memory usage in the attention layer by as much as 87.5$\\%$ for 32B Transformers, while matching previous context parallelism techniques in terms of training speed. UPipe can support the context length of 5M tokens when training Llama3-8B on a single 8$\\times$H100 node, improving upon prior methods by over 25$\\%$.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
