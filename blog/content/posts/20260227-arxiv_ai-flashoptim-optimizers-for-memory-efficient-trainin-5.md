---
title: 'FlashOptim: Optimizers for Memory Efficient Training'
date: 2026-02-27 23:20:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23349v1
aliases:
- /posts/20260228-arxiv_ai-flashoptim-optimizers-for-memory-efficient-trainin-5/
- /posts/20260301-arxiv_ai-flashoptim-optimizers-for-memory-efficient-trainin-5/
- /posts/20260302-arxiv_ai-flashoptim-optimizers-for-memory-efficient-trainin-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ebf1e2218468bdf1dd106b9e6f78e7c881819c3ce8432fe44f11121a12ab5e23
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
captured_at: '2026-07-18T04:30:40.966842Z'
source_capture_sha256: sha256:006f2bcc98062347246d3882f11707ba5a7af72b1bc1f5d4089e63a40230b00d
source_capture_chars_original: 1230
source_publication_excerpt_chars: 1230
observation_id: obs_d84d0fa45635dc0a10c1d3ad49e92e6ecd7a67fad1156d97323d0952a39917bc
revision_id: rev_9881a2564bcb4e862625874670bd827dc1a861b5936380f0bfa9ac40df050f6c
event_id: evt_29b17b6b47ba7c49ff44eae81714a74c4b9485ba0a5b48ea167fc4cad710723c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-27T06:11:48Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23349v1](<https://arxiv.org/abs/2602.23349v1>)
- **作者**: Jose Javier Gonzalez Ortiz, Abhay Gupta, Chris Renard, Davis Blalock
- **分类**: cs.LG
- **论文时间**: 2026-02-26T18:52:22Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23349v1.pdf](<https://arxiv.org/pdf/2602.23349v1.pdf>)

## 来源摘要/节选

> Standard mixed-precision training of neural networks requires many bytes of accelerator memory for each model parameter. These bytes reflect not just the parameter itself, but also its gradient and one or more optimizer state variables. With each of these values typically requiring 4 bytes, training even a 7 billion parameter model can be impractical for researchers with less than 100GB of accelerator memory. We introduce FlashOptim, a suite of optimizations that reduces per-parameter memory by over 50% while preserving model quality and API compatibility. Our approach introduces two key techniques. First, we improve master weight splitting by finding and exploiting a tight bound on its quantization error. Second, we design companding functions that greatly reduce the error in 8-bit optimizer state quantization. Together with 16-bit gradients, these techniques reduce AdamW memory from 16 bytes to 7 bytes per parameter, or 5 bytes with gradient release. They also cut model checkpoint sizes by more than half. Experiments with FlashOptim applied to SGD, AdamW, and Lion show no measurable quality degradation on any task from a collection of standard vision and language benchmarks, including Llama-3.1-8B finetuning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
