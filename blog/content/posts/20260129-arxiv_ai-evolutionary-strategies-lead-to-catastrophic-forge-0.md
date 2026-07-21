---
title: Evolutionary Strategies lead to Catastrophic Forgetting in LLMs
date: 2026-01-29 22:59:16+08:00
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
external_url: https://arxiv.org/abs/2601.20861v1
aliases:
- /posts/20260130-arxiv_ai-evolutionary-strategies-lead-to-catastrophic-forge-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f6964bfa0cc6b3d4a84c9dd4602b07d63b441ba0584dbee212fb011a4caea741
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 63
captured_at: '2026-07-18T04:09:34.038253Z'
source_capture_sha256: sha256:bc6263afc7286a9ba365d2a00252eabae6cbc0f60c93b431b2e1eb7cee396022
source_capture_chars_original: 1416
source_publication_excerpt_chars: 1416
observation_id: obs_e2bb155a37e1a45a6afeb619f784794e02be36b7bdf92d0b11ccd10329e348cb
revision_id: rev_008a955b5b42d26d19c6a01f600031cfffae3faa4cfb2d6188e32889c3424b21
event_id: evt_783748b7655d4474c3176ee772654838b5aa6f2bf8edcd256a6b3f96582662dc
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.20861v1](<https://arxiv.org/abs/2601.20861v1>)
- **作者**: Immanuel Abdi, Akshat Gupta, Micah Mok, Alexander Lu, Nicholas Lee, Gopala Anumanchipalli
- **分类**: cs.LG
- **论文时间**: 2026-01-28T18:59:34Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.20861v1.pdf](<https://arxiv.org/pdf/2601.20861v1.pdf>)

## 来源摘要/节选

> One of the biggest missing capabilities in current AI systems is the ability to learn continuously after deployment. Implementing such continually learning systems have several challenges, one of which is the large memory requirement of gradient-based algorithms that are used to train state-of-the-art LLMs. Evolutionary Strategies \(ES\) have recently re-emerged as a gradient-free alternative to traditional learning algorithms and have shown encouraging performance on specific tasks in LLMs. In this paper, we perform a comprehensive analysis of ES and specifically evaluate its forgetting curves when training for an increasing number of update steps. We first find that ES is able to reach performance numbers close to GRPO for math and reasoning tasks with a comparable compute budget. However, and most importantly for continual learning, the performance gains in ES is accompanied by significant forgetting of prior abilities, limiting its applicability for training models online. We also explore the reason behind this behavior and show that the updates made using ES are much less sparse and have orders of magnitude larger $\\ell\_2$ norm compared to corresponding GRPO updates, explaining the contrasting forgetting curves between the two algorithms. With this study, we aim to highlight the issue of forgetting in gradient-free algorithms like ES and hope to inspire future work to mitigate these issues.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
