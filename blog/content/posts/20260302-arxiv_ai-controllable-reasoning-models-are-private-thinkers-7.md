---
title: Controllable Reasoning Models Are Private Thinkers
date: 2026-03-02 02:56:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.24210v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b5ee52d066da199e96500e7b7389ed77bb32e57a0056a8521930b6c9cb335e33
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 50
captured_at: '2026-07-18T04:26:08.408518Z'
source_capture_sha256: sha256:60b5c04320e185a4a08fb37afed520cd855bda952a13e6dbb4002efb10dcd978
source_capture_chars_original: 1574
source_publication_excerpt_chars: 1574
observation_id: obs_86d6082f8c576fb14e222d966fde34cb1b0235ce4ea91fd60003c3f0d2db3d01
revision_id: rev_7e0694057b6a501cc6df9878d3f2b78cbb34a44607849afd8c808d2657b68227
event_id: evt_15fa76364a3a628d8160772d6f8b854a1fd6baf5e736605b903a3dadf4bd08ab
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.24210v1](<https://arxiv.org/abs/2602.24210v1>)
- **作者**: Haritz Puerto, Haonan Li, Xudong Han, Timothy Baldwin, Iryna Gurevych
- **分类**: cs.CL
- **论文时间**: 2026-02-27T17:39:10Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.24210v1.pdf](<https://arxiv.org/pdf/2602.24210v1.pdf>)

## 来源摘要/节选

> AI agents powered by reasoning models require access to sensitive user data. However, their reasoning traces are difficult to control, which can result in the unintended leakage of private information to external parties. We propose training models to follow instructions not only in the final answer, but also in reasoning traces, potentially under different constraints. We hypothesize that improving their instruction following abilities in the reasoning traces can improve their privacy-preservation skills. To demonstrate this, we fine-tune models on a new instruction-following dataset with explicit restrictions on reasoning traces. We further introduce a generation strategy that decouples reasoning and answer generation using separate LoRA adapters. We evaluate our approach on six models from two model families, ranging from 1.7B to 14B parameters, across two instruction-following benchmarks and two privacy benchmarks. Our method yields substantial improvements, achieving gains of up to 20.9 points in instruction-following performance and up to 51.9 percentage points on privacy benchmarks. These improvements, however, can come at the cost of task utility, due to the trade-off between reasoning performance and instruction-following abilities. Overall, our results show that improving instruction-following behavior in reasoning models can significantly enhance privacy, suggesting a promising direction for the development of future privacy-aware agents. Our code and data are available at https://github.com/UKPLab/arxiv2026-controllable-reasoning-models

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
