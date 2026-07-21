---
title: Function-Space Empirical Bayes Regularisation with Student's t Priors
date: 2026-02-26 02:52:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- 深度学习
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.22015v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f7733471d85c0c68e0d4dde3ce6a60563013746684fec3165c8a69e804125b23
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
captured_at: '2026-07-18T04:17:05.285632Z'
source_capture_sha256: sha256:0d966987677a7715f21a6a1f58b5b95b5582aec3bef701fd3cf622711c5a7168
source_capture_chars_original: 1177
source_publication_excerpt_chars: 1177
observation_id: obs_bfb2543de1432081211de454e2828e0867a6356ede57c15c168f26362011fa2b
revision_id: rev_e49d6869a709675b11d9ea812f9d2f1e6c0c25e0b5946c104f92a6ae29d4e1ed
event_id: evt_ab4ad389b7bd2ce6ed46c7c27d0399844e521d2945acf9167450580714f01b7f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-26T03:54:16Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.22015v1](<https://arxiv.org/abs/2602.22015v1>)
- **作者**: Pengcheng Hao, Ercan Engin Kuruoglu
- **分类**: cs.LG
- **论文时间**: 2026-02-25T15:29:44Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.22015v1.pdf](<https://arxiv.org/pdf/2602.22015v1.pdf>)

## 来源摘要/节选

> Bayesian deep learning \(BDL\) has emerged as a principled approach to produce reliable uncertainty estimates by integrating deep neural networks with Bayesian inference, and the selection of informative prior distributions remains a significant challenge. Various function-space variational inference \(FSVI\) regularisation methods have been presented, assigning meaningful priors over model predictions. However, these methods typically rely on a Gaussian prior, which fails to capture the heavy-tailed statistical characteristics inherent in neural network outputs. By contrast, this work proposes a novel function-space empirical Bayes regularisation framework -- termed ST-FS-EB -- which employs heavy-tailed Student's $t$ priors in both parameter and function spaces. Also, we approximate the posterior distribution through variational inference \(VI\), inducing an evidence lower bound \(ELBO\) objective based on Monte Carlo \(MC\) dropout. Furthermore, the proposed method is evaluated against various VI-based BDL baselines, and the results demonstrate its robust performance in in-distribution prediction, out-of-distribution \(OOD\) detection and handling distribution shifts.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
