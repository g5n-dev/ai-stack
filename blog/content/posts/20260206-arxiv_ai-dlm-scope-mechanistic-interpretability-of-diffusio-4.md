---
title: 'DLM-Scope: Mechanistic Interpretability of Diffusion Language Models via Sparse
  Autoencoders'
date: 2026-02-06 03:10:07+08:00
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
external_url: https://arxiv.org/abs/2602.05859v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:4b8f93147f771e4d6f9b7c2d82a2d0ebb2ecbf7347ebda0f3365ec7716ea214c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 92
captured_at: '2026-07-18T04:11:12.826784Z'
source_capture_sha256: sha256:8b3802685e470d31238c0f3b41dcb1bdca1cfb35934fef9ab7938f7a4793ff15
source_capture_chars_original: 1407
source_publication_excerpt_chars: 1407
observation_id: obs_476f4294b936d100a43b7635285862cdd65dead40363b10bcf314261ba496d21
revision_id: rev_fd731b0cec40f9acedbe9ceb1a45196e41bceb24568fa07e6729360462aca230
event_id: evt_699ca1f7b7150ecb1c86b286dbd10adec1134abc8c569b66bc78b46b64cc100f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-06T03:17:20Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.05859v1](<https://arxiv.org/abs/2602.05859v1>)
- **作者**: Xu Wang, Bingqing Jiang, Yu Wan, Baosong Yang, Lingpeng Kong, Difan Zou
- **分类**: cs.LG
- **论文时间**: 2026-02-05T16:41:25Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.05859v1.pdf](<https://arxiv.org/pdf/2602.05859v1.pdf>)

## 来源摘要/节选

> Sparse autoencoders \(SAEs\) have become a standard tool for mechanistic interpretability in autoregressive large language models \(LLMs\), enabling researchers to extract sparse, human-interpretable features and intervene on model behavior. Recently, as diffusion language models \(DLMs\) have become an increasingly promising alternative to the autoregressive LLMs, it is essential to develop tailored mechanistic interpretability tools for this emerging class of models. In this work, we present DLM-Scope, the first SAE-based interpretability framework for DLMs, and demonstrate that trained Top-K SAEs can faithfully extract interpretable features. Notably, we find that inserting SAEs affects DLMs differently than autoregressive LLMs: while SAE insertion in LLMs typically incurs a loss penalty, in DLMs it can reduce cross-entropy loss when applied to early layers, a phenomenon absent or markedly weaker in LLMs. Additionally, SAE features in DLMs enable more effective diffusion-time interventions, often outperforming LLM steering. Moreover, we pioneer certain new SAE-based research directions for DLMs: we show that SAEs can provide useful signals for DLM decoding order; and the SAE features are stable during the post-training phase of DLMs. Our work establishes a foundation for mechanistic interpretability in DLMs and shows a great potential of applying SAEs to DLM-related tasks and algorithms.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
