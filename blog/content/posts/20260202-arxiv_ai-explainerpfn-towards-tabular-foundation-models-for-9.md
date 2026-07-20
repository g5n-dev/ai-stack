---
title: 'ExplainerPFN: Towards tabular foundation models for model-free zero-shot feature
  importance estimations'
date: 2026-02-02 02:57:13+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.23068v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:075c0c2a07e7d758e786aa9affd5614f5e99846c2a2da83bc400bd3f71f47e22
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 103
captured_at: '2026-07-18T04:10:04.354932Z'
source_capture_sha256: sha256:67013b539346d3eeeee569f3b6aaade5ca3aa1241dcc7881bf02df6876fe4fe3
source_capture_chars_original: 1598
source_publication_excerpt_chars: 1598
observation_id: obs_c27462d9b0e7c6a8bb4d7a454fd932e5651faaa6248fd168b395846a6ecc70fb
revision_id: rev_b3ffacf123cff5df2cc7c0cbc7877e17f3de2c9891a17929e6a4b60548d9026a
event_id: evt_2b9e0884da65ef1b7467a686cf353b52d2d725dc084cea35bdbd05eaffd3150f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23068v1](<https://arxiv.org/abs/2601.23068v1>)
- **作者**: Joao Fonseca, Julia Stoyanovich
- **分类**: cs.LG
- **论文时间**: 2026-01-30T15:17:36Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23068v1.pdf](<https://arxiv.org/pdf/2601.23068v1.pdf>)

## 来源摘要/节选

> Computing the importance of features in supervised classification tasks is critical for model interpretability. Shapley values are a widely used approach for explaining model predictions, but require direct access to the underlying model, an assumption frequently violated in real-world deployments. Further, even when model access is possible, their exact computation may be prohibitively expensive. We investigate whether meaningful Shapley value estimations can be obtained in a zero-shot setting, using only the input data distribution and no evaluations of the target model. To this end, we introduce ExplainerPFN, a tabular foundation model built on TabPFN that is pretrained on synthetic datasets generated from random structural causal models and supervised using exact or near-exact Shapley values. Once trained, ExplainerPFN predicts feature attributions for unseen tabular datasets without model access, gradients, or example explanations. Our contributions are fourfold: \(1\) we show that few-shot learning-based explanations can achieve high fidelity to SHAP values with as few as two reference observations; \(2\) we propose ExplainerPFN, the first zero-shot method for estimating Shapley values without access to the underlying model or reference explanations; \(3\) we provide an open-source implementation of ExplainerPFN, including the full training pipeline and synthetic data generator; and \(4\) through extensive experiments on real and synthetic datasets, we show that ExplainerPFN achieves performance competitive with few-shot surrogate explainers that rely on 2-10 SHAP examples.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
