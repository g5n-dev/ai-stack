---
title: Process-Supervised Multi-Agent Reinforcement Learning for Reliable Clinical
  Reasoning
date: 2026-02-17 03:10:02+08:00
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
external_url: https://arxiv.org/abs/2602.14160v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:3465fab61801e26689c018d927e6d85c858aaa62047c9b32b25f8f5e69d8011a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
captured_at: '2026-07-18T04:15:37.655804Z'
source_capture_sha256: sha256:044fdf1ca6a4495f894a16fbdd0c2744deb5480b9d251c6644163dd66389b7e9
source_capture_chars_original: 1271
source_publication_excerpt_chars: 1271
observation_id: obs_a529ad0774867abba9bf3eb62a1e0e19ccc0fd280dad0c7f8e1f209bbbc89b72
revision_id: rev_8c38b8ce59b48f243e5466210edf37045353f81e8baf21caa175b39806c6f978
event_id: evt_456d627be52553686c850855503802c7813fdf2bd97763159000fc26bfe7be82
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.14160v1](<https://arxiv.org/abs/2602.14160v1>)
- **作者**: Chaeeun Lee, T. Michael Yates, Pasquale Minervini, T. Ian Simpson
- **分类**: cs.AI
- **论文时间**: 2026-02-15T14:21:21Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.14160v1.pdf](<https://arxiv.org/pdf/2602.14160v1.pdf>)

## 来源摘要/节选

> Clinical decision-making requires nuanced reasoning over heterogeneous evidence and traceable justifications. While recent LLM multi-agent systems \(MAS\) show promise, they largely optimise for outcome accuracy while overlooking process-grounded reasoning aligned with clinical standards. One critical real-world case of this is gene-disease validity curation, where experts must determine whether a gene is causally implicated in a disease by synthesising diverse biomedical evidence. We introduce an agent-as-tool reinforcement learning framework for this task with two objectives: \(i\) process-level supervision to ensure reasoning follows valid clinical pathways, and \(ii\) efficient coordination via a hierarchical multi-agent system. Our evaluation on the ClinGen dataset shows that with outcome-only rewards, MAS with a GRPO-trained Qwen3-4B supervisor agent substantially improves final outcome accuracy from 0.195 with a base model supervisor to 0.732, but results in poor process alignment \(0.392 F1\). Conversely, with process + outcome rewards, MAS with GRPO-trained supervisor achieves higher outcome accuracy \(0.750\) while significantly improving process fidelity to 0.520 F1. Our code is available at https://github.com/chaeeunlee-io/GeneDiseaseCurationAgents.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
