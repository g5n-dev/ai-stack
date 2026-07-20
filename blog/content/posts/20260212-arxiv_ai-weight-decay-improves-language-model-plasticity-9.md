---
title: Weight Decay Improves Language Model Plasticity
date: 2026-02-12 23:40:07+08:00
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
external_url: https://arxiv.org/abs/2602.11137v1
aliases:
- /posts/20260213-arxiv_ai-weight-decay-improves-language-model-plasticity-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:b4e73eb71c131bc132efbb69e43001b7a28a5808a755fa35b2463cea2e66bf0c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 47
captured_at: '2026-07-18T04:15:02.573604Z'
source_capture_sha256: sha256:a43c2c9968c12e3f86e00623d20386ea71c780d4342f30d82de4800939730a00
source_capture_chars_original: 1425
source_publication_excerpt_chars: 1425
observation_id: obs_1799c5258598e163b9ebd17b63ea1b6ecf259293a251603af703b76ad84ceba0
revision_id: rev_10ec7f090dbccacb8fe7b863311c636ae51839d76b4f33abe214e82c551dc80a
event_id: evt_b006aa2d0ce59316f466f3a8c48b596bd0e58d8a7df8425d810f15cc25e4165f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.11137v1](<https://arxiv.org/abs/2602.11137v1>)
- **作者**: Tessa Han, Sebastian Bordt, Hanlin Zhang, Sham Kakade
- **分类**: cs.LG
- **论文时间**: 2026-02-11T18:49:26Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.11137v1.pdf](<https://arxiv.org/pdf/2602.11137v1.pdf>)

## 来源摘要/节选

> The prevailing paradigm in large language model \(LLM\) development is to pretrain a base model, then perform further training to improve performance and model behavior. However, hyperparameter optimization and scaling laws have been studied primarily from the perspective of the base model's validation loss, ignoring downstream adaptability. In this work, we study pretraining from the perspective of model plasticity, that is, the ability of the base model to successfully adapt to downstream tasks through fine-tuning. We focus on the role of weight decay, a key regularization parameter during pretraining. Through systematic experiments, we show that models trained with larger weight decay values are more plastic, meaning they show larger performance gains when fine-tuned on downstream tasks. This phenomenon can lead to counterintuitive trade-offs where base models that perform worse after pretraining can perform better after fine-tuning. Further investigation of weight decay's mechanistic effects on model behavior reveals that it encourages linearly separable representations, regularizes attention matrices, and reduces overfitting on the training data. In conclusion, this work demonstrates the importance of using evaluation metrics beyond cross-entropy loss for hyperparameter optimization and casts light on the multifaceted role of that a single optimization hyperparameter plays in shaping model behavior.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
