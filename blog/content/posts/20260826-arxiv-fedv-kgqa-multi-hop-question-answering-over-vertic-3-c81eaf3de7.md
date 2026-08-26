---
title: "FedV-KGQA: Multi-Hop Question Answering over Vertically Partitioned Knowledge Graphs"
date: 2026-08-26T17:05:03+08:00
draft: false
entry_kind: "auto"
tags: ["AI", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:50562c440aca2de7994ae1fcdf1adfb67b9c15e0a6f70d375b928650d48af4f1"
source_payload_sha256: "sha256:600122dc6e3fd04bd0ee27ceb16370d8847fe2725b5683c601a1ad990d9bdf20"
observation_id: obs_c81eaf3de73cebd5e38a21952d1ba2060a2d0f24734427727dc052934f4e1543
event_id: evt_c2fc7c080b2543b40d625c072cdea72afbfc9c20e5dd6cbec829f53cb1c78cf7
revision_id: rev_b9713f52906d2247bb4d6e75079fcbaa1e125a5538da4873c16b70e706e9b76c
source_published_at: 2026-08-25T17:34:27Z
first_seen_at: 2026-08-26T17:00:02.558163Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
interpretation_sha256: "sha256:ad3430165d205c8cb1c194901e065e967d5e16de4fb09f334a1793b4ffaf7bea"
description: "它提出一种在垂直分区知识图谱上进行多跳问答的框架，各组织共享实体但保留各自的关系。框架利用本地图增强与嵌入技术，使三元组和关系参数不离开本地，并在无跨 silo 通信的情况下锚定问题对应的图区域。"
external_url: http://arxiv.org/abs/2608.24846v1
parent_observation_id: null
last_seen_at: 2026-08-26T09:02:31.817866Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24846v1](http://arxiv.org/abs/2608.24846v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Md Saikat Islam Khan Bappy、Oshani Seneviratne

## 要点解读

### 这是什么
它提出一种在垂直分区知识图谱上进行多跳问答的框架，各组织共享实体但保留各自的关系。框架利用本地图增强与嵌入技术，使三元组和关系参数不离开本地，并在无跨 silo 通信的情况下锚定问题对应的图区域。

### 用在哪里
适用于因数据治理或主权限制需要把原始三元组保留在各机构、只能通过共享实体实现协作的场景。需要跨机构多跳推理的问答系统、联邦学习平台以及关注隐私保护的语义搜索项目会关注该方案。

### 可以推断的
推测：在没有集中式图谱的情况下，该方案的性能仍能接近集中式系统的水平，说明信息隔离的代价相对可控。  
推测：如果嵌入过程受到噪声或扰动，框架的鲁棒性可能依赖于对嵌入空间的正则化或纠错机制。

## 来源摘要/节选

> Real-world data for knowledge graph question answering is often distributed across different organizations due to governance and data sovereignty constraints. While centralized systems exist, they cannot answer multi-hop questions when the required facts are split across vertically partitioned silos. In this paper, we propose FedV-KGQA, a framework for multi-hop reasoning over knowledge graphs in which organizations share entities but own disjoint sets of relations. Our approach combines local graph enrichment and knowledge graph embeddings to ensure raw triples and relation parameters never leave each silo, establishing a structural data boundary without requiring centralized graph access. We further introduce a topic entity anchoring mechanism that grounds questions in the correct graph neighborhood without any runtime inter-silo communication. We evaluate 12 model configurations across three benchmarks and show that FedV-KGQA performs strongly, remains close to centralized performance, generalizes to 3-hop reasoning, and is robust to embedding perturbations.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。