---
title: 'Counterfactual Training: Teaching Models Plausible and Actionable Explanations'
date: 2026-01-25 12:39:55+08:00
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
external_url: https://arxiv.org/abs/2601.16205v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a59c42ccd0f177d36b36b665507c1ea937ba87cfa748bb74f0bf59a48a230a7a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:08:52.620209Z'
source_capture_sha256: sha256:feba04a8757ce5c57f6a4cb16a8afc1b08048ebea73def92c341ed195940ab1a
source_capture_chars_original: 1177
source_publication_excerpt_chars: 1177
observation_id: obs_32af71da4b8dcc4a87d9eda23721c4c3d146e23c7d2108ca9b7cd338c0398c2e
revision_id: rev_87947a574e9b6809dcdce9b231d13fc0cd1f8e66e1f8a703c74dbeefa7623fb5
event_id: evt_76eef9f3dd7587243d382d0ba74458faffdac6ab19350f89930a0bbc635ecb24
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-25T12:41:54Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.16205v1](<https://arxiv.org/abs/2601.16205v1>)
- **作者**: Patrick Altmeyer, Aleksander Buszydlik, Arie van Deursen, Cynthia C. S. Liem
- **分类**: cs.LG
- **论文时间**: 2026-01-22T18:56:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.16205v1.pdf](<https://arxiv.org/pdf/2601.16205v1.pdf>)

## 来源摘要/节选

> We propose a novel training regime termed counterfactual training that leverages counterfactual explanations to increase the explanatory capacity of models. Counterfactual explanations have emerged as a popular post-hoc explanation method for opaque machine learning models: they inform how factual inputs would need to change in order for a model to produce some desired output. To be useful in real-world decision-making systems, counterfactuals should be plausible with respect to the underlying data and actionable with respect to the feature mutability constraints. Much existing research has therefore focused on developing post-hoc methods to generate counterfactuals that meet these desiderata. In this work, we instead hold models directly accountable for the desired end goal: counterfactual training employs counterfactuals during the training phase to minimize the divergence between learned representations and plausible, actionable explanations. We demonstrate empirically and theoretically that our proposed method facilitates training models that deliver inherently desirable counterfactual explanations and additionally exhibit improved adversarial robustness.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
