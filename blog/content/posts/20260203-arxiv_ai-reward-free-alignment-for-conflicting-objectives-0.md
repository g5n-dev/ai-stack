---
title: Reward-free Alignment for Conflicting Objectives
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
external_url: https://arxiv.org/abs/2602.02495v1
aliases:
- /posts/20260204-arxiv_ai-reward-free-alignment-for-conflicting-objectives-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1899d99943372d13d614fbc3cd3a401d285d3571e22a0e9c51cb012a5212816d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 48
captured_at: '2026-07-18T04:10:30.388786Z'
source_capture_sha256: sha256:158d1ed0bf57185d67f28dc1803077cbcfcfd490037f7ff4bec4868be584108c
source_capture_chars_original: 1483
source_publication_excerpt_chars: 1483
observation_id: obs_1e68b3ddb19ce4b29f630a95d233c3304c08a94c26c5ba1c3444c4af788a52ba
revision_id: rev_80a8be7d951b24369ca61f89ca259d44c332b4c824944c59c820f0c8e02228d1
event_id: evt_f5f9d8a7bb199d32745ce9af8ec0b112854562e344a6f0f89e2e70e891c24088
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-03T05:27:06Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.02495v1](<https://arxiv.org/abs/2602.02495v1>)
- **作者**: Peter Chen, Xiaopeng Li, Xi Chen, Tianyi Lin
- **分类**: cs.CL
- **论文时间**: 2026-02-02T18:59:52Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.02495v1.pdf](<https://arxiv.org/pdf/2602.02495v1.pdf>)

## 来源摘要/节选

> Direct alignment methods are increasingly used to align large language models \(LLMs\) with human preferences. However, many real-world alignment problems involve multiple conflicting objectives, where naive aggregation of preferences can lead to unstable training and poor trade-offs. In particular, weighted loss methods may fail to identify update directions that simultaneously improve all objectives, and existing multi-objective approaches often rely on explicit reward models, introducing additional complexity and distorting user-specified preferences. The contributions of this paper are two-fold. First, we propose a Reward-free Alignment framework for Conflicted Objectives \(RACO\) that directly leverages pairwise preference data and resolves gradient conflicts via a novel clipped variant of conflict-averse gradient descent. We provide convergence guarantees to Pareto-critical points that respect user-specified objective weights, and further show that clipping can strictly improve convergence rate in the two-objective setting. Second, we improve our method using some heuristics and conduct experiments to demonstrate the compatibility of the proposed framework for LLM alignment. Both qualitative and quantitative evaluations on multi-objective summarization and safety alignment tasks across multiple LLM families \(Qwen 3, Llama 3, Gemma 3\) show that our method consistently achieves better Pareto trade-offs compared to existing multi-objective alignment baselines.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
