---
title: 'Meta-Sel: Efficient Demonstration Selection for In-Context Learning via Supervised
  Meta-Learning'
date: 2026-02-13 03:01:31+08:00
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
external_url: https://arxiv.org/abs/2602.12123v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:44ed73a93567138e03c940d44d2e6ce710fcf1e844a9d8b6279c4113462a9fde
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 96
captured_at: '2026-07-18T04:15:06.314161Z'
source_capture_sha256: sha256:ffa6d60249a61655597661965dad065888dd8891cde1c3e295bee1ff719cd812
source_capture_chars_original: 1639
source_publication_excerpt_chars: 1639
observation_id: obs_7b3e573961d7c0ebf1e618bdb8065b54b670f420c49a43822dae39672c058239
revision_id: rev_13ad81bff82b170781dc1cd5273ac075189ae73883e33f776f65f69ccc4b4329
event_id: evt_d1b63d261c10fbc49a3a0eee9b28f5506c265104e679945267632082565b2195
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-13T03:55:23Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12123v1](<https://arxiv.org/abs/2602.12123v1>)
- **作者**: Xubin Wang, Weijia Jia
- **分类**: cs.LG
- **论文时间**: 2026-02-12T16:11:29Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12123v1.pdf](<https://arxiv.org/pdf/2602.12123v1.pdf>)

## 来源摘要/节选

> Demonstration selection is a practical bottleneck in in-context learning \(ICL\): under a tight prompt budget, accuracy can change substantially depending on which few-shot examples are included, yet selection must remain cheap enough to run per query over large candidate pools. We propose Meta-Sel, a lightweight supervised meta-learning approach for intent classification that learns a fast, interpretable scoring function for \(candidate, query\) pairs from labeled training data. Meta-Sel constructs a meta-dataset by sampling pairs from the training split and using class agreement as supervision, then trains a calibrated logistic regressor on two inexpensive meta-features: TF--IDF cosine similarity and a length-compatibility ratio. At inference time, the selector performs a single vectorized scoring pass over the full candidate pool and returns the top-k demonstrations, requiring no model fine-tuning, no online exploration, and no additional LLM calls. This yields deterministic rankings and makes the selection mechanism straightforward to audit via interpretable feature weights. Beyond proposing Meta-Sel, we provide a broad empirical study of demonstration selection, benchmarking 12 methods -- spanning prompt engineering baselines, heuristic selection, reinforcement learning, and influence-based approaches -- across four intent datasets and five open-source LLMs. Across this benchmark, Meta-Sel consistently ranks among the top-performing methods, is particularly effective for smaller models where selection quality can partially compensate for limited model capacity, and maintains competitive selection-time overhead.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
