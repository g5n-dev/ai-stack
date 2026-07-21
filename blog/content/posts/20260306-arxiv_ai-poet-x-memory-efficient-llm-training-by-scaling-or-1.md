---
title: 'POET-X: Memory-efficient LLM Training by Scaling Orthogonal Transformation'
date: 2026-03-06 23:44:05+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 大语言模型
- 机器学习
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.05500v1
aliases:
- /posts/20260307-arxiv_ai-poet-x-memory-efficient-llm-training-by-scaling-or-1/
- /posts/20260308-arxiv_ai-poet-x-memory-efficient-llm-training-by-scaling-or-1/
- /posts/20260309-arxiv_ai-poet-x-memory-efficient-llm-training-by-scaling-or-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:00d4fd0815328d12fe82a8b02d3c1401e49baff8c20683893cafe24816175912
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
captured_at: '2026-07-18T04:27:16.435086Z'
source_capture_sha256: sha256:dbf9d50fdb7d235f16549fdd9a7ae9982795c10212fc6325c4a6ccd9a3089e9b
source_capture_chars_original: 1051
source_publication_excerpt_chars: 1051
observation_id: obs_4fbe4e30acdb651586c6d4f90f88fe925dd2349dc4ef75b815844ed870d94596
revision_id: rev_a07c5bdc58240bd7117d0dfe80abb2fe8ad32011660ee7d1043525ee26daeae2
event_id: evt_73b47e08e2ccda480f7304c1fcb1105fa15e36e2719db4d65b4f8965c4c99bcb
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-06T06:19:07Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.05500v1](<https://arxiv.org/abs/2603.05500v1>)
- **作者**: Zeju Qiu, Lixin Liu, Adrian Weller, Han Shi, Weiyang Liu
- **分类**: cs.LG
- **论文时间**: 2026-03-05T18:59:23Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.05500v1.pdf](<https://arxiv.org/pdf/2603.05500v1.pdf>)

## 来源摘要/节选

> Efficient and stable training of large language models \(LLMs\) remains a core challenge in modern machine learning systems. To address this challenge, Reparameterized Orthogonal Equivalence Training \(POET\), a spectrum-preserving framework that optimizes each weight matrix through orthogonal equivalence transformation, has been proposed. Although POET provides strong training stability, its original implementation incurs high memory consumption and computational overhead due to intensive matrix multiplications. To overcome these limitations, we introduce POET-X, a scalable and memory-efficient variant that performs orthogonal equivalence transformations with significantly reduced computational cost. POET-X maintains the generalization and stability benefits of POET while achieving substantial improvements in throughput and memory efficiency. In our experiments, POET-X enables the pretraining of billion-parameter LLMs on a single Nvidia H100 GPU, and in contrast, standard optimizers such as AdamW run out of memory under the same settings.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
