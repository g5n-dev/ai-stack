---
title: 'CoFEH: LLM-driven Feature Engineering Empowered by Collaborative Bayesian
  Hyperparameter Optimization'
date: 2026-02-11 03:18:02+08:00
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
external_url: https://arxiv.org/abs/2602.09851v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:460053d09f04a6312a58f52627f5b849999fa11b5e2e49d0bd7c197c161084d1
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 101
captured_at: '2026-07-18T04:14:39.893621Z'
source_capture_sha256: sha256:7dd40e35a203cb5b21d9a38cd6302c04819e1b0d941c6c277e13bd55de0f39d7
source_capture_chars_original: 1402
source_publication_excerpt_chars: 1402
observation_id: obs_0c95f1890a0557b731e96c4852d7f9721690c6ab0a8ba1a389c91e3a50ec7598
revision_id: rev_09fe6eae634540c424e2e55709f489467c1dac2ca77e21f762ba1a1de0389815
event_id: evt_464bd0660ca86722d83efb6fd4ba79e7f9cd122c9c560d6ce3ab6b1b261c87a9
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.09851v1](<https://arxiv.org/abs/2602.09851v1>)
- **作者**: Beicheng Xu, Keyao Ding, Wei Liu, Yupeng Lu, Bin Cui
- **分类**: cs.LG
- **论文时间**: 2026-02-10T14:54:17Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.09851v1.pdf](<https://arxiv.org/pdf/2602.09851v1.pdf>)

## 来源摘要/节选

> Feature Engineering \(FE\) is pivotal in automated machine learning \(AutoML\) but remains a bottleneck for traditional methods, which treat it as a black-box search, operating within rigid, predefined search spaces and lacking domain awareness. While Large Language Models \(LLMs\) offer a promising alternative by leveraging semantic reasoning to generate unbounded operators, existing methods fail to construct free-form FE pipelines, remaining confined to isolated subtasks such as feature generation. Most importantly, they are rarely optimized jointly with hyperparameter optimization \(HPO\) of the ML model, leading to greedy "FE-then-HPO" workflows that cannot capture strong FE-HPO interactions. In this paper, we present CoFEH, a collaborative framework that interleaves LLM-based FE and Bayesian HPO for robust end-to-end AutoML. CoFEH uses an LLM-driven FE optimizer powered by Tree of Thought \(ToT\) to explore flexible FE pipelines, a Bayesian optimization \(BO\) module to solve HPO, and a dynamic optimizer selector that realizes interleaved optimization by adaptively scheduling FE and HPO steps. Crucially, we introduce a mutual conditioning mechanism that shares context between LLM and BO, enabling mutually informed decisions. Experiments show that CoFEH not only outperforms traditional and LLM-based FE baselines, but also achieves superior end-to-end performance under joint optimization.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
