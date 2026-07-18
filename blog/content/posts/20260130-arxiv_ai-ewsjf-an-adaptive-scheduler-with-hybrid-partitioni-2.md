---
title: 'EWSJF: An Adaptive Scheduler with Hybrid Partitioning for Mixed-Workload LLM
  Inference'
date: 2026-01-30 03:54:32+08:00
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
external_url: https://arxiv.org/abs/2601.21758v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6a0c316a94da78b0e083d51f03f2d1c817de6a9fe32f2c260605c71a2e021a9e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 86
captured_at: '2026-07-18T04:09:48.978849Z'
source_capture_sha256: sha256:1d897a220daefdf98cb3c864b55875488a35fbf3c62492c508ba31496236580b
source_capture_chars_original: 1422
source_publication_excerpt_chars: 1422
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.21758v1](<https://arxiv.org/abs/2601.21758v1>)
- **作者**: Bronislav Sidik, Chaya Levi, Joseph Kampeas
- **分类**: cs.DC
- **论文时间**: 2026-01-29T14:14:16Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.21758v1.pdf](<https://arxiv.org/pdf/2601.21758v1.pdf>)

## 来源摘要/节选

> Serving Large Language Models \(LLMs\) under mixed workloads--short, latency-sensitive interactive queries alongside long, throughput-oriented batch requests--poses a fundamental scheduling challenge. Standard First-Come, First-Served \(FCFS\) policies suffer from severe head-of-line blocking, leading to high tail latency and underutilized hardware. We introduce EWSJF \(Effective Workload-based Shortest Job First\), an adaptive request-level scheduler that learns workload structure in real time to jointly improve fairness and throughput. EWSJF operates upstream of execution-level schedulers and integrates four components: \(1\) Refine-and-Prune, an unsupervised partitioning algorithm that discovers performance-homogeneous request groups; \(2\) Dynamic Queue Routing for assigning requests to these groups; \(3\) Density-Weighted Scoring, a context-aware prioritization function balancing urgency and fairness; and \(4\) Bayesian Meta-Optimization, which continuously tunes scoring and partitioning parameters based on live performance feedback. Implemented in vLLM, EWSJF improves end-to-end throughput by over 30% and reduces average Time-To-First-Token for short requests by up to 4x compared to FCFS. These results demonstrate that adaptive, learning-based request scheduling is a critical missing layer for efficient and responsive LLM serving. Implementation available at https://anonymous.4open.science/r/vllm\_0110-32D8.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
