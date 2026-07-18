---
title: 'P-GenRM: Personalized Generative Reward Model with Test-time User-based Scaling'
date: 2026-02-13 03:01:31+08:00
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
external_url: https://arxiv.org/abs/2602.12116v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a7f42918f8b56e46682d881bcc6d5bd320e741b43ee7dfdc8af19ef6fac25161
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
captured_at: '2026-07-18T04:15:22.283119Z'
source_capture_sha256: sha256:3ae399a28561dcdc998ead1c6d910bb54275f77c5984f547dc08f996efaf6fdb
source_capture_chars_original: 1522
source_publication_excerpt_chars: 1522
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12116v1](<https://arxiv.org/abs/2602.12116v1>)
- **作者**: Pinyi Zhang, Ting-En Lin, Yuchuan Wu, Jingyang Chen, Zongqi Wang, Hua Yang, Ze Xu, Fei Huang, Kai Zhang, Yongbin Li
- **分类**: cs.CL
- **论文时间**: 2026-02-12T16:07:22Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12116v1.pdf](<https://arxiv.org/pdf/2602.12116v1.pdf>)

## 来源摘要/节选

> Personalized alignment of large language models seeks to adapt responses to individual user preferences, typically via reinforcement learning. A key challenge is obtaining accurate, user-specific reward signals in open-ended scenarios. Existing personalized reward models face two persistent limitations: \(1\) oversimplifying diverse, scenario-specific preferences into a small, fixed set of evaluation principles, and \(2\) struggling with generalization to new users with limited feedback. To this end, we propose P-GenRM, the first Personalized Generative Reward Model with test-time user-based scaling. P-GenRM transforms preference signals into structured evaluation chains that derive adaptive personas and scoring rubrics across various scenarios. It further clusters users into User Prototypes and introduces a dual-granularity scaling mechanism: at the individual level, it adaptively scales and aggregates each user's scoring scheme; at the prototype level, it incorporates preferences from similar users. This design mitigates noise in inferred preferences and enhances generalization to unseen users through prototype-based transfer. Empirical results show that P-GenRM achieves state-of-the-art results on widely-used personalized reward model benchmarks, with an average improvement of 2.31%, and demonstrates strong generalization on an out-of-distribution dataset. Notably, Test-time User-based scaling provides an additional 3% boost, demonstrating stronger personalized alignment with test-time scalability.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
