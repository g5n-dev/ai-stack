---
title: Learning Query-Aware Budget-Tier Routing for Runtime Agent Memory
date: 2026-02-06 23:01:34+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.06025v1
aliases:
- /posts/20260207-arxiv_ai-learning-query-aware-budget-tier-routing-for-runti-9/
- /posts/20260208-arxiv_ai-learning-query-aware-budget-tier-routing-for-runti-9/
- /posts/20260209-arxiv_ai-learning-query-aware-budget-tier-routing-for-runti-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:260215642a05b7dc72b66f67919cd35b47dadccabd492ebd123237b6f8be1e88
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
captured_at: '2026-07-18T04:11:12.826784Z'
source_capture_sha256: sha256:77fecfa9a2348ca7ab2def25755a7c3824138ece63524626d0c0ac2f5719cc48
source_capture_chars_original: 1532
source_publication_excerpt_chars: 1532
observation_id: obs_520dfed42b7d3f76b7a45c516e554bfde2eadf588aef2f0fa181124a49a6fd58
revision_id: rev_a709a64d5eda1e004ba879ec009d75a7b33ef197f9a9a682e1dbba78bdc9716c
event_id: evt_6ec1ff05305cfc55ea8b6703521d15f07f62bc2602ba1c25338e5b1574037adc
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.06025v1](<https://arxiv.org/abs/2602.06025v1>)
- **作者**: Haozhen Zhang, Haodong Yue, Tao Feng, Quanyu Long, Jianzhu Bao, Bowen Jin, Weizhi Zhang, Xiao Li, Jiaxuan You, Chengwei Qin, Wenya Wang
- **分类**: cs.CL
- **论文时间**: 2026-02-05T18:57:09Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.06025v1.pdf](<https://arxiv.org/pdf/2602.06025v1.pdf>)

## 来源摘要/节选

> Memory is increasingly central to Large Language Model \(LLM\) agents operating beyond a single context window, yet most existing systems rely on offline, query-agnostic memory construction that can be inefficient and may discard query-critical information. Although runtime memory utilization is a natural alternative, prior work often incurs substantial overhead and offers limited explicit control over the performance-cost trade-off. In this work, we present \\textbf\{BudgetMem\}, a runtime agent memory framework for explicit, query-aware performance-cost control. BudgetMem structures memory processing as a set of memory modules, each offered in three budget tiers \(i.e., \\textsc\{Low\}/\\textsc\{Mid\}/\\textsc\{High\}\). A lightweight router performs budget-tier routing across modules to balance task performance and memory construction cost, which is implemented as a compact neural policy trained with reinforcement learning. Using BudgetMem as a unified testbed, we study three complementary strategies for realizing budget tiers: implementation \(method complexity\), reasoning \(inference behavior\), and capacity \(module model size\). Across LoCoMo, LongMemEval, and HotpotQA, BudgetMem surpasses strong baselines when performance is prioritized \(i.e., high-budget setting\), and delivers better accuracy-cost frontiers under tighter budgets. Moreover, our analysis disentangles the strengths and weaknesses of different tiering strategies, clarifying when each axis delivers the most favorable trade-offs under varying budget regimes.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
