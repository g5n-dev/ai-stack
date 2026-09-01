---
title: "On the Complexity of the Compatibility Problem for Succinctly Encoded Conditional Distributions"
date: 2026-09-02T05:48:55+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:a5836908085f86a57e0ce62e7f8b3af2daa2783731eb3edac9de1451fb6724f9"
source_payload_sha256: "sha256:8b68ad30fb4c32f1d77c8d7d075105e16241c10ff7b1a27b8c36fd5bce8c1183"
observation_id: obs_ba50d782ff93b7d20cdf71602618291adedbb38739b5f6ccbc1fbf08c8b5b143
event_id: evt_4ba73d29db59db80954bb5594debc1a0691861e1b70efb6a88ec3fe7191f2809
revision_id: rev_a33eeb342ab218b8805a36449960e512c22701fb267347b53c832d1a89d944cd
source_published_at: 2026-08-31T17:32:21Z
first_seen_at: 2026-09-01T21:46:37.267296Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 95
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.31120v1
parent_observation_id: null
last_seen_at: 2026-09-01T21:46:37.267296Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.31120v1](http://arxiv.org/abs/2608.31120v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Guy Emerson

## 来源摘要/节选

> The motivation for this paper is the investigation of the trade-offs implicit in probabilistic models used in machine learning. Models are often used to make predictions in the form of conditional probabilities. However, a pair of conditional distributions p(x|y) and p(y|x) may not be compatible with any joint distribution p(x,y). Given two such conditionals, determining if there exists a compatible joint is known as the compatibility problem. For discrete random variables, when the conditionals are encoded as probability tables, the compatibility problem has a known solution, which is computationally tractable. In this paper, we formalise and study a succinct version of the problem, encoding conditional distributions as arithmetic circuits. This is applicable to practical applications of probabilistic modelling in high-dimensional settings, including neural network models. We show that, for succinct circuit representations of conditionals, the compatibility problem is intractable. In the case that all probabilities are non-zero, the problem is co-NP-complete. In the case that probabilities can be zero, we give examples to demonstrate that several notions of compatibility can be distinguished, and we prove that multiple versions of the problem are PSPACE-complete. Furthermore, we show that, assuming the polynomial hierarchy does not collapse, there exist compatible succinct conditionals whose joint cannot be expressed succinctly. Implications of these results for probabilistic modelling and machine learning are discussed.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。