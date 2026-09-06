---
title: "Rethinking On-Policy Distillation of Large Language Models II: One Training Example"
date: 2026-09-07T05:22:59+08:00
draft: false
entry_kind: "auto"
tags: ["Prompt 工程", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:5706488179d70b47062dfa39073c330b317837f265a09d8e5175840833a90bda"
source_payload_sha256: "sha256:29095ec6feea156732f97d8a5de453221ecd9b7591cada060c99848e6001480a"
observation_id: obs_c46ee15bbc76b9563e8072cb1172868cd23fade5a1060ecb9ddedb5bc794ecaa
event_id: evt_b3e6a569c884d6998900de952943f3a9f1a38cc7d5266ca84a01e96f90698ee5
revision_id: rev_8c1edfd20a0464e2aff857325ce6e9352d531688d3c101c47693e529b5e65434
source_published_at: 2026-09-03T17:54:38Z
first_seen_at: 2026-09-06T21:20:39.192367Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 83
interpretation_sha256: "sha256:29a7c9f6ebd89e3c5e8afdeae75d2139c80937b10106ecaa7129e9ec896a02f2"
description: "研究在大型语言模型的同策略蒸馏中，仅使用一条查询进行训练的效果。实验发现单查询在数百步后已能接近全数据蒸馏的收益，并用状态覆盖率解释了这一现象。"
external_url: http://arxiv.org/abs/2609.04172v1
parent_observation_id: null
last_seen_at: 2026-09-06T21:20:39.192367Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.04172v1](http://arxiv.org/abs/2609.04172v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Zixuan Fu、Bingxiang He、Yuxin Zuo 等

## 要点解读

### 这是什么
研究在大型语言模型的同策略蒸馏中，仅使用一条查询进行训练的效果。实验发现单查询在数百步后已能接近全数据蒸馏的收益，并用状态覆盖率解释了这一现象。

### 用在哪里
适用于资源受限但希望快速微调模型的研究团队，以及需要评估蒸馏所需数据量的工程实践者。

### 可以推断的
推测：在多数任务上，少量查询已能提供足够的监督信号，进一步增加查询的收益可能呈递减趋势。  
推测：当前蒸馏过程在后期学习效率下降，未来的改进方向可能聚焦于提升每步的更新效率或引入更丰富的监督信号。

## 来源摘要/节选

> On-policy distillation (OPD) combines student-generated rollouts with dense token-level supervision from a teacher. Existing work has mainly studied its algorithmic behavior, leaving the role of training data unclear. We examine this role at the data-minimal limit by training on a single query. One-shot OPD keeps improving for hundreds of steps and recovers most of full-data OPD's gain across task domains and model families. We explain this result through the states visited during training and the rate at which the student aligns with the teacher. We measure \emph{state coverage}, the fraction of the states full-data OPD visits that a query set's rollouts reach. A single query already reaches \(71.5\%\), most of it within the first 100 steps. Adding semantically distinct queries raises coverage and validation accuracy together, until 16 queries reach \(98.9\%\) and match full-data training. Yet alignment slows at a similar pace whether OPD trains on one query or the whole dataset, and even a fixed set of states takes hundreds of steps to absorb. OPD is therefore data-overfed but algorithm-starved. Its rollouts quickly expose broad supervision, while the student absorbs that supervision increasingly slowly. The state-coverage result extends to multi-teacher OPD, where 16 semantically diverse queries per domain match full-data MOPD. As a further stress test, content-light templates and off-domain WildChat queries also approach the real-query baseline. Task content and induced state coverage can therefore come apart. We hope these findings direct future work toward the step efficiency of OPD, and prompt a re-examination of the data and the mechanisms behind its recent successes in frontier post-training.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。