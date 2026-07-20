---
title: 'AgentRx: Diagnosing AI Agent Failures from Execution Trajectories'
date: 2026-02-03 23:08:59+08:00
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
external_url: https://arxiv.org/abs/2602.02475v1
aliases:
- /posts/20260204-arxiv_ai-agentrx-diagnosing-ai-agent-failures-from-executio-8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:c2e23f2089cd86244304ac031a66bcfdf3c6d25d7c40b4b90c402aaccca08718
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 65
captured_at: '2026-07-18T04:10:19.257843Z'
source_capture_sha256: sha256:811249ad898e5795a9f3f15882b98935022788513d22b45db1e4c41b54cb8746
source_capture_chars_original: 1030
source_publication_excerpt_chars: 1030
observation_id: obs_d94b052eafe90a69b2aa04bdd50bde2d7adc431f49e7b6d9194bce2af1576b62
revision_id: rev_602ab26bd3393cb190b4d94f14ab9d5fcab68afe2b3d5091e2e25ccd518c9a30
event_id: evt_539772d47e108373ced7145cc8bcf8006725880f1d23eff7309511f39fcbb0a7
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.02475v1](<https://arxiv.org/abs/2602.02475v1>)
- **作者**: Shraddha Barke, Arnav Goyal, Alind Khare, Avaljot Singh, Suman Nath, Chetan Bansal
- **分类**: cs.AI
- **论文时间**: 2026-02-02T18:54:07Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.02475v1.pdf](<https://arxiv.org/pdf/2602.02475v1.pdf>)

## 来源摘要/节选

> AI agents often fail in ways that are difficult to localize because executions are probabilistic, long-horizon, multi-agent, and mediated by noisy tool outputs. We address this gap by manually annotating failed agent runs and release a novel benchmark of 115 failed trajectories spanning structured API workflows, incident management, and open-ended web/file tasks. Each trajectory is annotated with a critical failure step and a category from a grounded-theory derived, cross-domain failure taxonomy. To mitigate the human cost of failure attribution, we present AGENTRX, an automated domain-agnostic diagnostic framework that pinpoints the critical failure step in a failed agent trajectory. It synthesizes constraints, evaluates them step-by-step, and produces an auditable validation log of constraint violations with associated evidence; an LLM-based judge uses this log to localize the critical step and category. Our framework improves step localization and failure attribution over existing baselines across three domains.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
