---
title: 'STRIDE: Training Data Attribution via Sparse Recovery from Subset Perturbations'
date: 2026-06-04 18:31:38+08:00
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
external_url: https://arxiv.org/abs/2606.05165v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6795d5d391f5f42ba9decd2f9ef5b82bfdb32b9add6cbb09cdb81cea33bfb62a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
captured_at: '2026-07-18T04:29:58.207159Z'
source_capture_sha256: sha256:51a9444c9891612428abb45f58078a946f9f03ee1f8e4f5f1e29052a5e4ccc12
source_capture_chars_original: 1393
source_publication_excerpt_chars: 1393
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.05165v1](<https://arxiv.org/abs/2606.05165v1>)
- **作者**: Rishit Dagli, Abir Harrasse, Luke Zhang, Florent Draye, Amirali Abdullah, Bernhard Schölkopf, Zhijing Jin
- **分类**: cs.LG
- **论文时间**: 2026-06-03T17:59:36Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.05165v1.pdf](<https://arxiv.org/pdf/2606.05165v1.pdf>)

## 来源摘要/节选

> Training Data Attribution \(TDA\) seeks to trace a model's predictions back to its training data. The gold standard for TDA relies on causal interventions, observing how a model changes when data is added or removed, but repeated retraining is computationally challenging for Large Language Models \(LLMs\). Consequently, most approaches approximate this effect in the parameter space using gradients. However, tracking gradients across billions of parameters is not only prohibitively expensive but relies on local approximations. In this work, we propose a shift: rather than estimating parameter changes, we model the functional effect of training data in the activation space. We introduce STRIDE \(Steering-based Training Data Influence Decomposition\), a framework that formulates TDA as a sparse recovery problem in the spirit of compressive sensing. STRIDE learns lightweight "steering operators" that mimic the behavioral shift caused by training on data subsets. By measuring how these operators perturb test predictions, we recover individual training example influences via sparse linear decomposition. STRIDE achieves state-of-the-art for LLM pre-training attribution while being an order of magnitude \($13\\times$\) faster than previous art. We further validate its practical utility through downstream applications including data selection, data contamination, and qualitative analysis.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
