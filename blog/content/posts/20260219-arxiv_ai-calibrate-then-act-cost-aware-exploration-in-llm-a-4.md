---
title: 'Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents'
date: 2026-02-19 22:55:31+08:00
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
external_url: https://arxiv.org/abs/2602.16699v1
aliases:
- /posts/20260220-arxiv_ai-calibrate-then-act-cost-aware-exploration-in-llm-a-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1cc957e6067ce554ad990e47dac2e158c98641697a17f5ce2a6aec6fd9106601
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 56
captured_at: '2026-07-18T04:16:00.196393Z'
source_capture_sha256: sha256:25f2e8e057dc2001d97172c80bd63829721fab4d9463b9f2f8788ed94db045e6
source_capture_chars_original: 1369
source_publication_excerpt_chars: 1369
observation_id: obs_57445f2a46cea9489b31449603d1a0b87ab770b5f417f631c690ff88f926e869
revision_id: rev_482a080ae8b497d2f59e8dc11c513cb34b4467efeca855197d6e621cf3ae6516
event_id: evt_f396340cd7e9e72476e2b48d4316bcc79481b1c80ab1e8a4773b1438e66f0b99
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.16699v1](<https://arxiv.org/abs/2602.16699v1>)
- **作者**: Wenxuan Ding, Nicholas Tomlin, Greg Durrett
- **分类**: cs.CL
- **论文时间**: 2026-02-18T18:46:14Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.16699v1.pdf](<https://arxiv.org/pdf/2602.16699v1.pdf>)

## 来源摘要/节选

> LLMs are increasingly being used for complex problems which are not necessarily resolved in a single response, but require interacting with an environment to acquire information. In these scenarios, LLMs must reason about inherent cost-uncertainty tradeoffs in when to stop exploring and commit to an answer. For instance, on a programming task, an LLM should test a generated code snippet if it is uncertain about the correctness of that code; the cost of writing a test is nonzero, but typically lower than the cost of making a mistake. In this work, we show that we can induce LLMs to explicitly reason about balancing these cost-uncertainty tradeoffs, then perform more optimal environment exploration. We formalize multiple tasks, including information retrieval and coding, as sequential decision-making problems under uncertainty. Each problem has latent environment state that can be reasoned about via a prior which is passed to the LLM agent. We introduce a framework called Calibrate-Then-Act \(CTA\), where we feed the LLM this additional context to enable it to act more optimally. This improvement is preserved even under RL training of both the baseline and CTA. Our results on information-seeking QA and on a simplified coding task show that making cost-benefit tradeoffs explicit with CTA can help agents discover more optimal decision-making strategies.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
