---
title: 'InftyThink+: Effective and Efficient Infinite-Horizon Reasoning via Reinforcement
  Learning'
date: 2026-02-09 23:42:37+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.06960v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:09512cfce7e673c5aea69c2e6dc4c19c59cf60d714eb45526f35c172365319bb
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
captured_at: '2026-07-18T04:11:23.963527Z'
source_capture_sha256: sha256:1e9ff8af9e1d737782e08ef0c0069d6e53efab33cdf2fab6bebe2de2cd0521f7
source_capture_chars_original: 1333
source_publication_excerpt_chars: 1333
observation_id: obs_037b22c49bae635704eae64ee4f377314203b91dd74f3514bb3220f7079ac923
revision_id: rev_18fdf755a94fb0054d57f061fdaa25e540f4235b560b36663dabbc48d538148a
event_id: evt_770a41959842e1e7c5fd48d9cbd57aed9aa4acf6b31e920004b5568a12327f68
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06960v1](<https://arxiv.org/abs/2602.06960v1>)
- **作者**: Yuchen Yan, Liang Jiang, Jin Jiang, Shuaicheng Li, Zujie Wen, Zhiqiang Zhang, Jun Zhou, Jian Shao, Yueting Zhuang, Yongliang Shen
- **分类**: cs.CL
- **论文时间**: 2026-02-06T18:59:27Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06960v1.pdf](<https://arxiv.org/pdf/2602.06960v1.pdf>)

## 来源摘要/节选

> Large reasoning models achieve strong performance by scaling inference-time chain-of-thought, but this paradigm suffers from quadratic cost, context length limits, and degraded reasoning due to lost-in-the-middle effects. Iterative reasoning mitigates these issues by periodically summarizing intermediate thoughts, yet existing methods rely on supervised learning or fixed heuristics and fail to optimize when to summarize, what to preserve, and how to resume reasoning. We propose InftyThink+, an end-to-end reinforcement learning framework that optimizes the entire iterative reasoning trajectory, building on model-controlled iteration boundaries and explicit summarization. InftyThink+ adopts a two-stage training scheme with supervised cold-start followed by trajectory-level reinforcement learning, enabling the model to learn strategic summarization and continuation decisions. Experiments on DeepSeek-R1-Distill-Qwen-1.5B show that InftyThink+ improves accuracy by 21% on AIME24 and outperforms conventional long chain-of-thought reinforcement learning by a clear margin, while also generalizing better to out-of-distribution benchmarks. Moreover, InftyThink+ significantly reduces inference latency and accelerates reinforcement learning training, demonstrating improved reasoning efficiency alongside stronger performance.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
