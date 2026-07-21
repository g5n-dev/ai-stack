---
title: Unified Spatio-Temporal Token Scoring for Efficient Video VLMs
date: 2026-03-19 18:55:56+08:00
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
external_url: https://arxiv.org/abs/2603.18004v1
aliases:
- /posts/20260320-arxiv_ai-unified-spatio-temporal-token-scoring-for-efficien-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:93ad832b6e88446b233f120f2d1ac68615e22d060e5ea77a0eb0faba71d52c16
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 62
captured_at: '2026-07-18T04:29:04.624314Z'
source_capture_sha256: sha256:80c4a9f1ef242a4e6a7de0857a73ba54456864703c1827c2d5261f45312b9535
source_capture_chars_original: 1469
source_publication_excerpt_chars: 1469
observation_id: obs_9da904f0e355bb85e10ab99f6a6aba295de26ea08d2124c053f8a9f17e3e2a44
revision_id: rev_047e5c427a8594436c5777ac3bd34c4865a1e3693be5815b71e5ec25a2120ab1
event_id: evt_40ee0c58a84e9991fa6fae7800c75df603a7b522395c8404238eef1b95f954e8
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-19T20:50:47Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.18004v1](<https://arxiv.org/abs/2603.18004v1>)
- **作者**: Jianrui Zhang, Yue Yang, Rohun Tripathi, Winson Han, Ranjay Krishna, Christopher Clark, Yong Jae Lee, Sangho Lee
- **分类**: cs.CV
- **论文时间**: 2026-03-18T17:59:56Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.18004v1.pdf](<https://arxiv.org/pdf/2603.18004v1.pdf>)

## 来源摘要/节选

> Token pruning is essential for enhancing the computational efficiency of vision-language models \(VLMs\), particularly for video-based tasks where temporal redundancy is prevalent. Prior approaches typically prune tokens either \(1\) within the vision transformer \(ViT\) exclusively for unimodal perception tasks such as action recognition and object segmentation, without adapting to downstream vision-language tasks; or \(2\) only within the LLM while leaving the ViT output intact, often requiring complex text-conditioned token selection mechanisms. In this paper, we introduce Spatio-Temporal Token Scoring \(STTS\), a simple and lightweight module that prunes vision tokens across both the ViT and the LLM without text conditioning or token merging, and is fully compatible with end-to-end training. By learning how to score temporally via an auxiliary loss and spatially via LLM downstream gradients, aided by our efficient packing algorithm, STTS prunes 50% of vision tokens throughout the entire architecture, resulting in a 62% improvement in efficiency during both training and inference with only a 0.7% drop in average performance across 13 short and long video QA tasks. Efficiency gains increase with more sampled frames per video. Applying test-time scaling for long-video QA further yields performance gains of 0.5-1% compared to the baseline. Overall, STTS represents a novel, simple yet effective technique for unified, architecture-wide vision token pruning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
