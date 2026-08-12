---
title: "Scheduling Mixed RL Rollouts Beyond Prefix Locality"
date: 2026-08-13T03:23:51+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.DC", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:94aebed04734d5364490b4b496a1226491c0cef044d4355d5ac35b5b21b10d78"
source_payload_sha256: "sha256:1362e3d3faf23520b792ce3e67ac055cea715e4255e12e88b01a4c264259a2de"
observation_id: obs_97941e1323ed4e61bd3c1ba90491aabe76cd66c67827e798da2820447ca70306
event_id: evt_09be56bbbceb308c0fe2cab2a1f6e6b1dfd3069c651b2eabaed6fb250016ead3
revision_id: rev_c170a67d748ecb515e581242f8ceca7bf8e473f18527eb918622b1e6c002af53
source_published_at: 2026-08-11T17:10:50Z
first_seen_at: 2026-08-12T19:20:16.853903Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 51
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.11152v1
parent_observation_id: null
last_seen_at: 2026-08-12T19:20:16.853903Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.11152v1](http://arxiv.org/abs/2608.11152v1)
- **发布域名**: arxiv.org
- **分类**: cs.DC
- **作者**: Zetao Hong、Song Yuan、Yuanhao Ding 等

## 来源摘要/节选

> Modern reinforcement learning (RL) post-training pipelines for large language models (LLMs) increasingly combine rollout workloads across multiple domains and feedback paradigms. Prefix-aware routing improves inference efficiency through cache reuse and load balancing, but it does not control how heterogeneous rollout sessions compete for KV-cache capacity. When reinforcement learning with verifiable rewards (RLVR), reinforcement learning from human feedback (RLHF), and agentic rollouts share an asynchronous inference service, their distinct sequence structures, interaction patterns, and KV-residency times create substantially different serving demands. Rollout scheduling must account for this heterogeneity without distorting the workload mixture specified by the trainer. We present MISA-T, a routing-layer admission policy for mixed rollout serving. MISA-T combines adaptive session admission, workload-aware KV-capacity allocation, and residency-time-aware KV accounting. In rollout-only ablations on Step3.7 and Qwen3.6-35B-A3B, MISA-T improves rollout throughput over a sweep-tuned cache-aware vLLM Router by 53.3% and 43.6%, respectively, while maintaining high prefix-cache hit rates. In a matched 50-iteration Step3.7 experiment, it increases rollout throughput by 35.6% and reduces mean iteration time by 22.8%, while keeping the consumed workload mixture close to the trainer target and achieving comparable task scores.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。