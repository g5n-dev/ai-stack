---
title: 'SmartSearch: How Ranking Beats Structure for Conversational Memory Retrieval'
date: 2026-03-17 20:30:33+08:00
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
external_url: https://arxiv.org/abs/2603.15599v1
aliases:
- /posts/20260318-arxiv_ai-smartsearch-how-ranking-beats-structure-for-conver-6/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:42d657395dc678bda791ecf4dc83ffb8b4fbdb591c596af24a59fa5b2df0d141
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
captured_at: '2026-07-18T04:28:41.690884Z'
source_capture_sha256: sha256:a7ff404ad3d9590378760cb0c9aeb2c647cee0d5a0bb3135f965b6d966d66112
source_capture_chars_original: 955
source_publication_excerpt_chars: 955
observation_id: obs_9415ea91c689ae616414bc0c11f9e998b8684f702b90ddfa8f9ad9193347a6f1
revision_id: rev_cca37de5d1c18dfa5c3a20f2c85b49b774c0f9d3af919ca3dc07e169385c2d48
event_id: evt_ff52887ee684185d3bb001c5da7360e20545ac3a0952ca293c0dce5a422c5916
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-17T06:47:02Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.15599v1](<https://arxiv.org/abs/2603.15599v1>)
- **作者**: Jesper Derehag, Carlos Calva, Timmy Ghiurau
- **分类**: cs.LG
- **论文时间**: 2026-03-16T17:53:21Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.15599v1.pdf](<https://arxiv.org/pdf/2603.15599v1.pdf>)

## 来源摘要/节选

> Recent conversational memory systems invest heavily in LLM-based structuring at ingestion time and learned retrieval policies at query time. We show that neither is necessary. SmartSearch retrieves from raw, unstructured conversation history using a fully deterministic pipeline: NER-weighted substring matching for recall, rule-based entity discovery for multi-hop expansion, and a CrossEncoder+ColBERT rank fusion stage -- the only learned component -- running on CPU in ~650ms. Oracle analysis on two benchmarks identifies a compilation bottleneck: retrieval recall reaches 98.6%, but without intelligent ranking only 22.5% of gold evidence survives truncation to the token budget. With score-adaptive truncation and no per-dataset tuning, SmartSearch achieves 93.5% on LoCoMo and 88.4% on LongMemEval-S, exceeding all known memory systems under the same evaluation protocol on both benchmarks while using 8.5x fewer tokens than full-context baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
