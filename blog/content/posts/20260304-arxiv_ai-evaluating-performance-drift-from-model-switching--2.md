---
title: Evaluating Performance Drift from Model Switching in Multi-Turn LLM Systems
date: 2026-03-04 03:29:03+08:00
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
external_url: https://arxiv.org/abs/2603.03111v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:17af5ad974d386ef8e73a3251781304ef50cf916bb3c14e372286a9d9c1b016b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
captured_at: '2026-07-18T04:26:46.139217Z'
source_capture_sha256: sha256:81457b2d20498d4497d8a401dc8b8cb6e187bcca51bf9dc4ac5c2774eb43b35b
source_capture_chars_original: 1497
source_publication_excerpt_chars: 1497
observation_id: obs_b0108d592921786fe9ccb8b8b4e668bb32d84bb35f31f91a1f4afabfb1476af0
revision_id: rev_c0e07fd2ee16c3abfeb1db98312de4da36767d04315a1ee55c0730267f67df95
event_id: evt_f60b7d46dc91661a0cc618ec3f6e519c356c4eb9b8e2ff9edaf4507f72bb59c7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03111v1](<https://arxiv.org/abs/2603.03111v1>)
- **作者**: Raad Khraishi, Iman Zafar, Katie Myles, Greig A Cowan
- **分类**: cs.CL
- **论文时间**: 2026-03-03T15:44:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03111v1.pdf](<https://arxiv.org/pdf/2603.03111v1.pdf>)

## 来源摘要/节选

> Deployed multi-turn LLM systems routinely switch models mid-interaction due to upgrades, cross-provider routing, and fallbacks. Such handoffs create a context mismatch: the model generating later turns must condition on a dialogue prefix authored by a different model, potentially inducing silent performance drift. We introduce a switch-matrix benchmark that measures this effect by running a prefix model for early turns and a suffix model for the final turn, and comparing against the no-switch baseline using paired episode-level bootstrap confidence intervals. Across CoQA conversational QA and Multi-IF benchmarks, even a single-turn handoff yields prevalent and statistically significant, directional effects and may swing outcomes by -8 to +13 percentage points in Multi-IF strict success rate and +/- 4 absolute F1 on CoQA, comparable to the no-switch gap between common model tiers \(e.g., GPT-5-nano vs GPT-5-mini\). We further find systematic compatibility patterns: some suffix models degrade under nearly any non-self dialogue history, while others improve under nearly any foreign prefix. To enable compressed handoff risk monitoring, we decompose switch-induced drift into per-model prefix influence and suffix susceptibility terms, accounting for ~70% of variance across benchmarks. These results position handoff robustness as an operational reliability dimension that single-model benchmarks miss, motivating explicit monitoring and handoff-aware mitigation in multi-turn systems.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
