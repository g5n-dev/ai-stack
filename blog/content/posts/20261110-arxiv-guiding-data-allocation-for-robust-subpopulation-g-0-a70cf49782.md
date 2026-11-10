---
title: "Guiding Data Allocation for Robust Subpopulation Generalization"
date: 2026-11-10T17:48:03+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c1f33ecc297c5b8aac5375e4e9967eee28db8441b5db027a6bea1bf27c3baeae"
source_payload_sha256: "sha256:2a16de163c80dc1eee8d8527f18d2513e6b1d2e1a8aa7bb7b18d3ee5ac8427f7"
observation_id: obs_a70cf49782d88fbad3727501b0d642065d879ba3747b5f463298aff7da02c173
event_id: evt_0c7f0300ee5ba879b0c4a33efd397600d6ac70673f63f91580ed7aef65e2352c
revision_id: rev_3bee4d82f68ec49931c17c25289a3dddba8cde217109279851fb67225e3df3ed
source_published_at: 2026-11-09T18:59:40Z
first_seen_at: 2026-11-10T09:46:39.074170Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
interpretation_sha256: "sha256:6f544287cbffaf62914d0d0fd2a7fe1a6d127d13757b13cf38b60baa431a8fa2"
description: "这篇论文研究如何在训练数据中分配不同子群体，以提升模型在子群体分布变化下的稳健泛化能力。作者在理论上刻画了不同分配方案的表现，并提出通过梯度调整子群体比例来改善整体调整准确率和最差子群体准确率。"
external_url: http://arxiv.org/abs/2611.12884v1
parent_observation_id: null
last_seen_at: 2026-11-10T09:46:39.074170Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.12884v1](http://arxiv.org/abs/2611.12884v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Zhaoying Pan、Yipei Wang、Shenyu Lu 等

## 要点解读

### 这是什么
这篇论文研究如何在训练数据中分配不同子群体，以提升模型在子群体分布变化下的稳健泛化能力。作者在理论上刻画了不同分配方案的表现，并提出通过梯度调整子群体比例来改善整体调整准确率和最差子群体准确率。

### 用在哪里
适用于训练数据包含多个子群体、需要关注平均性能或最差群体表现的数据构建与模型训练场景。可帮助研究者和实践者制定比简单均衡更灵活的数据分配策略。

### 可以推断的
- 推测：对子群体比例进行精细调整，可能比完全均衡更节省成本，也更适合数据构成受现实条件限制的场景。
- 推测：该方法或可为数据分配与稳健性优化之间的权衡提供理论依据。

## 来源摘要/节选

> Machine learning models often achieve high average accuracy in the training data while performing poorly on test data due to subpopulation shift. A common data-centric solution is to enforce balanced subgroup proportions, but full balance can be costly, infeasible, and not always necessary. In this work, we study whether balanced training data is the unique optimal configuration for robust subpopulation generalization. We extend a Gaussian feature-model framework to theoretically characterize the performance landscape across general training subgroup distributions. We show that multiple configurations, including substantially imbalanced ones, can perform comparably to the balanced one. We further derive gradient-based directions for adjusting subgroup proportions to improve adjusted accuracy and worst-group accuracy more efficiently. These findings suggest that strategically allocating data offers a more flexible and principled path to robust performance than simple balancing. The code is available at https://github.com/zhaoyingpan/subpop-data-allocation.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。