---
title: 'The Pensieve Paradigm: Stateful Language Models Mastering Their Own Context'
date: 2026-02-13 03:01:31+08:00
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
external_url: https://arxiv.org/abs/2602.12108v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7540dda7645bf18ca0674010c2ff8645f6236ce1c2a1f8ba92870f09d4e95c0e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
captured_at: '2026-07-18T04:15:22.283119Z'
source_capture_sha256: sha256:b85fdc53bcb806ad942a7e657665debcec6ebf8772905b4eb2db8f7c6d3358b5
source_capture_chars_original: 1482
source_publication_excerpt_chars: 1482
observation_id: obs_471254af01c1c4085a7d1144e95ab9ba284ce018532ec354db7c3ad4ebce7784
revision_id: rev_8358f2b645405172bce4721815672af5deb8d8d22a7588869c1a194dd3df1aee
event_id: evt_27b00288e40ae8bf0038f23bd03fb53fb6ad651163792f55f1654619be5176c8
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12108v1](<https://arxiv.org/abs/2602.12108v1>)
- **作者**: Xiaoyuan Liu, Tian Liang, Dongyang Ma, Deyu Zhou, Haitao Mi, Pinjia He, Yan Wang
- **分类**: cs.AI
- **论文时间**: 2026-02-12T16:00:01Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12108v1.pdf](<https://arxiv.org/pdf/2602.12108v1.pdf>)

## 来源摘要/节选

> In the world of Harry Potter, when Dumbledore's mind is overburdened, he extracts memories into a Pensieve to be revisited later. In the world of AI, while we possess the Pensieve-mature databases and retrieval systems, our models inexplicably lack the "wand" to operate it. They remain like a Dumbledore without agency, passively accepting a manually engineered context as their entire memory. This work finally places the wand in the model's hand. We introduce StateLM, a new class of foundation models endowed with an internal reasoning loop to manage their own state. We equip our model with a suite of memory tools, such as context pruning, document indexing, and note-taking, and train it to actively manage these tools. By learning to dynamically engineering its own context, our model breaks free from the architectural prison of a fixed window. Experiments across various model sizes demonstrate StateLM's effectiveness across diverse scenarios. On long-document QA tasks, StateLMs consistently outperform standard LLMs across all model scales; on the chat memory task, they achieve absolute accuracy improvements of 10% to 20% over standard LLMs. On the deep research task BrowseComp-Plus, the performance gap becomes even more pronounced: StateLM achieves up to 52% accuracy, whereas standard LLM counterparts struggle around 5%. Ultimately, our approach shifts LLMs from passive predictors to state-aware agents where reasoning becomes a stateful and manageable process.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
