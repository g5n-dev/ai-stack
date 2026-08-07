---
title: "TRAJDEBUG: Tracing Error Lifecycle to Identify Critical Failures in Long-Horizon Agent Trajectories"
date: 2026-08-08T01:11:37+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:7fbeed1bfb61996348e0a80f35496150eaaeb0f5de8da3f20d986e15087f681c"
source_payload_sha256: "sha256:cdb22819e5a4fc8133e3f3f2b0ea987155dba8fe0f8e386333b45b221d5bd56e"
observation_id: obs_5b5cbce254bb478bb86ec7ad0349d3251885cabed5c08aafeff50d536d936715
event_id: evt_822bf921e627f22e8ab0276638226194305f25e7b549bd30b26e1aeefb2fe381
revision_id: rev_2c385091ee62399d96be2e72001493b479a0c2bde222e7acdc8765442ce46211
source_published_at: 2026-08-06T17:51:20Z
first_seen_at: 2026-08-07T17:07:08.435714Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 99
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.06346v1
parent_observation_id: null
last_seen_at: 2026-08-07T17:07:08.435714Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06346v1](http://arxiv.org/abs/2608.06346v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Yunjia Qi、Zehua Yin、Xintong Shi 等

## 来源摘要/节选

> LLM-based agentic systems have shown remarkable capabilities in complex domains, while suffering from cascading errors and difficulty in debugging. Critical error detection aims to locate the earliest error step in a failed trajectory that is responsible for the final failure. However, progress faces two main challenges. First, long trajectories make it difficult to identify individual errors, since the evidence for judging a step may be scattered across distant instructions, observations, and prior context. Second, failed trajectories often contain multiple local errors with different downstream effects, only some of which remain responsible for the final failure. In this work, we propose TrajDebug, an error-lifecycle tracing framework that addresses long-trajectory error discovery with multi-granularity history compression and evidence-based error identification, and supports critical attribution by tracing each error's resolution status and terminal impact. We further construct TrajErrBench, a benchmark of 486 manually annotated failed trajectories from Tau2Bench and SWE-Bench Pro, covering realistic tool-use and coding scenarios. Experiments across diverse agent benchmarks show that TrajDebug achieves the best overall performance over existing baselines, and application studies further demonstrate that its diagnoses provide actionable feedback for improving downstream agent success. We will release the codes and data to facilitate further research.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。