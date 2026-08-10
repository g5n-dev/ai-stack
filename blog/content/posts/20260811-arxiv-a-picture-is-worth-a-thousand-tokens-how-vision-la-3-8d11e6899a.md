---
title: "A Picture is Worth a Thousand Tokens: How Vision Language Models Cut AI Energy Costs While Improving Accuracy"
date: 2026-08-11T07:54:31+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0fc9a3365eb2626236d9d62d4abd204a74456e09500139ae6e3c1d895bf2b3a6"
source_payload_sha256: "sha256:c18f80304fa36144f59df6f4934edc01b5307f880d59481e25ce75959b5f3907"
observation_id: obs_8d11e6899aa6deb336e2198944ec6b19b36a4b3a2b72fde609a1046bfc5a84ea
event_id: evt_55cce8c03c87405b4d1d5f62f3e3f4f751f879b44a1047f3c6cab67b9130ffe9
revision_id: rev_efd4253ac6d79a321dfb26f260e7d0d257aff84565d053f64a7c016bc0214632
source_published_at: 2026-08-07T17:14:45Z
first_seen_at: 2026-08-10T23:51:01.419598Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 109
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.07427v1
parent_observation_id: null
last_seen_at: 2026-08-10T23:51:01.419598Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07427v1](http://arxiv.org/abs/2608.07427v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Bhavika Jalli、Nikhil Korati Prasanna、Jayanta Choudhury

## 来源摘要/节选

> LLM inference accounts for over 90% of AI operational energy, scaling directly with input token count---a critical inefficiency for telecom network analytics and numerical time-series data analysis (NTSDA), where raw multivariate KPI windows from 4G/5G cell sites expand into thousands of floating-point tokens. Vision-Language Models (VLMs) eliminate this mismatch by encoding time-series as 2D plots, achieving 3.6-10.4x input token reduction across Llama-3.2-90B, Qwen2.5-VL-72B, and Pixtral-12B architectures. This translates to 1.8-2.5x measured inference energy reduction, saving approximately 7.2 MJ/day at telecom edge deployments and CloudRAN that monitor 200 cells per 15-minute interval. Critically, efficiency gains do not sacrifice accuracy: a fine-tuned Llama-3.2-90B-Vision VLM achieves 220.7% higher precision than its text-only counterpart and outperforms LSTM and ARIMA baselines by over 144% on telecom anomaly detection. On public benchmarks, Pixtral-12B achieves a 20.6x improvement in J/F1 score at mean F1 = 0.82. At 24 KPIs, text representations exceed the 128K context window of most production LLMs, rendering text-only processing infeasible without truncation, while visual representations remain within standard limits. These results establish VLMs as an energy-efficient and accuracy-superior modality for numerical time-series workloads, providing empirical grounding for AI inference systems that treat energy consumption as a first-class engineering constraint.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。