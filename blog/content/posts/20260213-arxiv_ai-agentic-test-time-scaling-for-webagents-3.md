---
title: Agentic Test-Time Scaling for WebAgents
date: 2026-02-13 23:30:43+08:00
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
external_url: https://arxiv.org/abs/2602.12276v1
aliases:
- /posts/20260214-arxiv_ai-agentic-test-time-scaling-for-webagents-3/
- /posts/20260215-arxiv_ai-agentic-test-time-scaling-for-webagents-3/
- /posts/20260216-arxiv_ai-agentic-test-time-scaling-for-webagents-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:27dd78e9835997895a70195c3d87065bc7e43c5cd16426d5dc45beb33001c15e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 39
captured_at: '2026-07-18T04:15:02.573604Z'
source_capture_sha256: sha256:52824da6465ecfc360e318761e10200471d83d4a5977630d2465bc54c7fe5929
source_capture_chars_original: 1399
source_publication_excerpt_chars: 1399
observation_id: obs_809b85bcfdc9552bdfc5eff91dfec6ca574cb586ec8af66e76a24493f7b00b86
revision_id: rev_366eafc1ade8e7120d16d069d3409bfa7dd7b85c0960d23e9f53e3e687550c22
event_id: evt_0b29caf72df44f4a198893b5be023dca3d5d92092b07f97c4fc3a2225f1e6dde
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-13T06:19:22Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.12276v1](<https://arxiv.org/abs/2602.12276v1>)
- **作者**: Nicholas Lee, Lutfi Eren Erdogan, Chris Joseph John, Surya Krishnapillai, Michael W. Mahoney, Kurt Keutzer, Amir Gholami
- **分类**: cs.AI
- **论文时间**: 2026-02-12T18:58:30Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.12276v1.pdf](<https://arxiv.org/pdf/2602.12276v1.pdf>)

## 来源摘要/节选

> Test-time scaling has become a standard way to improve performance and boost reliability of neural network models. However, its behavior on agentic, multi-step tasks remains less well-understood: small per-step errors can compound over long horizons; and we find that naive policies that uniformly increase sampling show diminishing returns. In this work, we present CATTS, a simple technique for dynamically allocating compute for multi-step agents. We first conduct an empirical study of inference-time scaling for web agents. We find that uniformly increasing per-step compute quickly saturates in long-horizon environments. We then investigate stronger aggregation strategies, including an LLM-based Arbiter that can outperform naive voting, but that can overrule high-consensus decisions. We show that uncertainty statistics derived from the agent's own vote distribution \(entropy and top-1/top-2 margin\) correlate with downstream success and provide a practical signal for dynamic compute allocation. Based on these findings, we introduce Confidence-Aware Test-Time Scaling \(CATTS\), which uses vote-derived uncertainty to allocate compute only when decisions are genuinely contentious. CATTS improves performance on WebArena-Lite and GoBrowse by up to 9.1% over React while using up to 2.3x fewer tokens than uniform scaling, providing both efficiency gains and an interpretable decision rule.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
