---
title: Expanding the Capabilities of Reinforcement Learning via Text Feedback
date: 2026-02-03 23:08:59+08:00
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
external_url: https://arxiv.org/abs/2602.02482v1
aliases:
- /posts/20260204-arxiv_ai-expanding-the-capabilities-of-reinforcement-learni-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6570054453ec607e34aa8f854d3e4e3c5c0af640eaeb0511a349b1469f2e35dc
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:10:26.671991Z'
source_capture_sha256: sha256:7268c0154476494a5aecc829ab06e097fd2466148b1ee0c324337db33a5f164f
source_capture_chars_original: 1479
source_publication_excerpt_chars: 1479
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.02482v1](<https://arxiv.org/abs/2602.02482v1>)
- **作者**: Yuda Song, Lili Chen, Fahim Tajwar, Remi Munos, Deepak Pathak, J. Andrew Bagnell, Aarti Singh, Andrea Zanette
- **分类**: cs.LG
- **论文时间**: 2026-02-02T18:56:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.02482v1.pdf](<https://arxiv.org/pdf/2602.02482v1.pdf>)

## 来源摘要/节选

> The success of RL for LLM post-training stems from an unreasonably uninformative source: a single bit of information per rollout as binary reward or preference label. At the other extreme, distillation offers dense supervision but requires demonstrations, which are costly and difficult to scale. We study text feedback as an intermediate signal: richer than scalar rewards, yet cheaper than complete demonstrations. Textual feedback is a natural mode of human interaction and is already abundant in many real-world settings, where users, annotators, and automated judges routinely critique LLM outputs. Towards leveraging text feedback at scale, we formalize a multi-turn RL setup, RL from Text Feedback \(RLTF\), where text feedback is available during training but not at inference. Therefore, models must learn to internalize the feedback in order to improve their test-time single-turn performance. To do this, we propose two methods: Self Distillation \(RLTF-SD\), which trains the single-turn policy to match its own feedback-conditioned second-turn generations; and Feedback Modeling \(RLTF-FM\), which predicts the feedback as an auxiliary objective. We provide theoretical analysis on both methods, and empirically evaluate on reasoning puzzles, competition math, and creative writing tasks. Our results show that both methods consistently outperform strong baselines across benchmarks, highlighting the potential of RL with an additional source of rich supervision at scale.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
