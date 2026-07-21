---
title: 'AdaEvolve: Adaptive LLM Driven Zeroth-Order Optimization'
date: 2026-02-24 23:13:49+08:00
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
external_url: https://arxiv.org/abs/2602.20133v1
aliases:
- /posts/20260225-arxiv_ai-adaevolve-adaptive-llm-driven-zeroth-order-optimiz-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ebbf67df8640d21b2335e34fc8d74a618e0166edc7c269c6a0679967e9cf6f4b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 56
captured_at: '2026-07-18T04:16:31.219110Z'
source_capture_sha256: sha256:8abb5ddad8dcbbd7708281bdeae40616f6222999bff19475c3cfa63689060303
source_capture_chars_original: 1381
source_publication_excerpt_chars: 1381
observation_id: obs_860853022f25ad2b996b704ef71ea71a5b46c1eb31d225232ec234fb9217bfb8
revision_id: rev_bc4e65422dda7934609d8f8143cdfc5fc34a16f77af86007c432529368b7e9b8
event_id: evt_bc42f766108b53fd56b6c3ed9cec3b2b3eeac00da87595811b00955737d1e94a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-24T06:21:29Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.20133v1](<https://arxiv.org/abs/2602.20133v1>)
- **作者**: Mert Cemri, Shubham Agrawal, Akshat Gupta, Shu Liu, Audrey Cheng, Qiuyang Mang, Ashwin Naren, Lutfi Eren Erdogan, Koushik Sen, Matei Zaharia, Alex Dimakis, Ion Stoica
- **分类**: cs.NE
- **论文时间**: 2026-02-23T18:45:31Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.20133v1.pdf](<https://arxiv.org/pdf/2602.20133v1.pdf>)

## 来源摘要/节选

> The paradigm of automated program generation is shifting from one-shot generation to inference-time search, where Large Language Models \(LLMs\) function as semantic mutation operators within evolutionary loops. While effective, these systems are currently governed by static schedules that fail to account for the non-stationary dynamics of the search process. This rigidity results in substantial computational waste, as resources are indiscriminately allocated to stagnating populations while promising frontiers remain under-exploited. We introduce AdaEvolve, a framework that reformulates LLM-driven evolution as a hierarchical adaptive optimization problem. AdaEvolve uses an "accumulated improvement signal" to unify decisions across three levels: Local Adaptation, which dynamically modulates the exploration intensity within a population of solution candidates; Global Adaptation, which routes the global resource budget via bandit-based scheduling across different solution candidate populations; and Meta-Guidance which generates novel solution tactics based on the previously generated solutions and their corresponding improvements when the progress stalls. We demonstrate that AdaEvolve consistently outperforms the open-sourced baselines across 185 different open-ended optimization problems including combinatorial, systems optimization and algorithm design problems.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
