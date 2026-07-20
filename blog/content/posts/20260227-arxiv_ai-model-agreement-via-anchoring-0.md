---
title: Model Agreement via Anchoring
date: 2026-02-27 23:20:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.23360v1
aliases:
- /posts/20260228-arxiv_ai-model-agreement-via-anchoring-0/
- /posts/20260301-arxiv_ai-model-agreement-via-anchoring-0/
- /posts/20260302-arxiv_ai-model-agreement-via-anchoring-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f3e257f93ee6a6ab3d878dd957657fd05660e61bce16248a81f15179bd39ab60
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:30:40.966842Z'
source_capture_sha256: sha256:527187bbbe0aaf82b66f0f8302c8d70200954b15856ccbc1d93bd039f12b5826
source_capture_chars_original: 1618
source_publication_excerpt_chars: 1618
observation_id: obs_15865a67db8c0fb92871b77a1d449a16cceeaaf2db4c4528458130baf7c1ced9
revision_id: rev_35f57a77924832efb4ccb95e5017c10c1262c7ca2743bfc5f8072689723e7344
event_id: evt_c11d414a66cd5cfdf59aaf45d0b11aa3514fe4f75e91793a6f5ad753c27dff29
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.23360v1](<https://arxiv.org/abs/2602.23360v1>)
- **作者**: Eric Eaton, Surbhi Goel, Marcel Hussing, Michael Kearns, Aaron Roth, Sikata Bela Sengupta, Jessica Sorrell
- **分类**: cs.LG
- **论文时间**: 2026-02-26T18:59:32Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.23360v1.pdf](<https://arxiv.org/pdf/2602.23360v1.pdf>)

## 来源摘要/节选

> Numerous lines of aim to control $\\textit\{model disagreement\}$ -- the extent to which two machine learning models disagree in their predictions. We adopt a simple and standard notion of model disagreement in real-valued prediction problems, namely the expected squared difference in predictions between two models trained on independent samples, without any coordination of the training processes. We would like to be able to drive disagreement to zero with some natural parameter\(s\) of the training procedure using analyses that can be applied to existing training methodologies. We develop a simple general technique for proving bounds on independent model disagreement based on $\\textit\{anchoring\}$ to the average of two models within the analysis. We then apply this technique to prove disagreement bounds for four commonly used machine learning algorithms: \(1\) stacked aggregation over an arbitrary model class \(where disagreement is driven to 0 with the number of models $k$ being stacked\) \(2\) gradient boosting \(where disagreement is driven to 0 with the number of iterations $k$\) \(3\) neural network training with architecture search \(where disagreement is driven to 0 with the size $n$ of the architecture being optimized over\) and \(4\) regression tree training over all regression trees of fixed depth \(where disagreement is driven to 0 with the depth $d$ of the tree architecture\). For clarity, we work out our initial bounds in the setting of one-dimensional regression with squared error loss -- but then show that all of our results generalize to multi-dimensional regression with any strongly convex loss.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
