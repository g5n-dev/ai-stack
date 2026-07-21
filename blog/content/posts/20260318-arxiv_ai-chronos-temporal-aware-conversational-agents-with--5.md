---
title: 'Chronos: Temporal-Aware Conversational Agents with Structured Event Retrieval
  for Long-Term Memory'
date: 2026-03-18 05:34:51+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.16862v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b66434b4f6cffde9a495d3ab08ae7f6c3e1db349839a0d7d6f6e14e96e9f61ee
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
captured_at: '2026-07-18T04:28:41.690884Z'
source_capture_sha256: sha256:a649ebb5a52682951c121dca226dabc829266da6b924f116bafc6a8ed06e98c6
source_capture_chars_original: 1579
source_publication_excerpt_chars: 1579
observation_id: obs_60558d798f972d49b0212fb51ccbd7697a26a6d557c08c2f8590a91c0667c00b
revision_id: rev_9a964e7edf4ee1fdf9d2ad906ee9969372f08d23186c919f024af3a2b82b4c8d
event_id: evt_e63bee3ab865190935fc67efa1590fd1b5fbbbbe2568a09b96b2a167548145c1
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-18T04:20:43Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.16862v1](<https://arxiv.org/abs/2603.16862v1>)
- **作者**: Sahil Sen, Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah
- **分类**: cs.CL
- **论文时间**: 2026-03-17T17:59:20Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.16862v1.pdf](<https://arxiv.org/pdf/2603.16862v1.pdf>)

## 来源摘要/节选

> Recent advances in Large Language Models \(LLMs\) have enabled conversational AI agents to engage in extended multi-turn interactions spanning weeks or months. However, existing memory systems struggle to reason over temporally grounded facts and preferences that evolve across months of interaction and lack effective retrieval strategies for multi-hop, time-sensitive queries over long dialogue histories. We introduce Chronos, a novel temporal-aware memory framework that decomposes raw dialogue into subject-verb-object event tuples with resolved datetime ranges and entity aliases, indexing them in a structured event calendar alongside a turn calendar that preserves full conversational context. At query time, Chronos applies dynamic prompting to generate tailored retrieval guidance for each question, directing the agent on what to retrieve, how to filter across time ranges, and how to approach multi-hop reasoning through an iterative tool-calling loop over both calendars. We evaluate Chronos with 8 LLMs, both open-source and closed-source, on the LongMemEvalS benchmark comprising 500 questions spanning six categories of dialogue history tasks. Chronos Low achieves 92.60% and Chronos High scores 95.60% accuracy, setting a new state of the art with an improvement of 7.67% over the best prior system. Ablation results reveal the events calendar accounts for a 58.9% gain on the baseline while all other components yield improvements between 15.5% and 22.3%. Notably, Chronos Low alone surpasses prior approaches evaluated under their strongest model configurations.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
