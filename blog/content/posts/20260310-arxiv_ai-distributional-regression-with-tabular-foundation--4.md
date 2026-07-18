---
title: 'Distributional Regression with Tabular Foundation Models: Evaluating Probabilistic
  Predictions via Proper Scoring Rules'
date: 2026-03-10 02:45:40+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 机器学习
- 深度学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.08206v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a819ef2c3666563a4ee0ba873ad6d1fcadb4ce1cf50da18c3faf35ec6821639f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 119
captured_at: '2026-07-18T04:27:31.441787Z'
source_capture_sha256: sha256:7c54e4f9ea4491ddaa154604b4cf96404a2e1a38fb9fda51c87c85e464531f41
source_capture_chars_original: 1676
source_publication_excerpt_chars: 1676
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.08206v1](<https://arxiv.org/abs/2603.08206v1>)
- **作者**: Jonas Landsgesell, Pascal Knoll
- **分类**: cs.LG
- **论文时间**: 2026-03-09T10:38:01Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.08206v1.pdf](<https://arxiv.org/pdf/2603.08206v1.pdf>)

## 来源摘要/节选

> Prior-Data Fitted Networks \(PFNs\), such as TabPFN and TabICL, have revolutionized tabular deep learning by leveraging in-context learning for tabular data. These models are meant as foundation models for classification and regression settings and promise to greatly simplify deployment in practical settings because their performance is unprecedented \(in terms of mean squared error or $R^2$, when measured on common benchmarks like TabArena or TALENT\). However, we see an important weakness of current benchmarks for the regression setting: the current benchmarks focus on evaluating win rates and performance using metrics like \(root\) mean squared error or $R^2$. Therefore, these leaderboards \(implicitly and explicitly\) push researchers to optimize for machine learning pipelines which elicit a good mean value estimate. The main problem is that this approach only evaluates a point estimate \(namely the mean estimator which is the Bayes estimator associated with the mean squared error loss\). In this article we discuss the application of proper scoring rules for evaluating the goodness of probabilistic forecasts in distributional regression. We also propose to enhance common machine learning benchmarks with metrics for probabilistic regression. To improve the status quo and make the machine learning community aware of scoring rules for probabilistic regression, we advocate to use the continuous ranked probability score \(CRPS\) in benchmarks for probabilistic regression. However, we also illustrate that the choice of the scoring rule changes the inductive bias of the trained model. We, therefore, advocate for finetuning or promptable tabular foundation models.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
