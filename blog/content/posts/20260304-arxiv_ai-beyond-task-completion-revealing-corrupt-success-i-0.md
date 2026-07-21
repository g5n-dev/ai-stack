---
title: 'Beyond Task Completion: Revealing Corrupt Success in LLM Agents through Procedure-Aware
  Evaluation'
date: 2026-03-04 03:29:03+08:00
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
external_url: https://arxiv.org/abs/2603.03116v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:54804c0ad5939c323e55e644335bc0d01049423b109ab784be847194cd96079d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
captured_at: '2026-07-18T04:26:38.668400Z'
source_capture_sha256: sha256:ee4d050cef8513a93362368d90fc63292f43018c9968c1326e30f2c81359d518
source_capture_chars_original: 1622
source_publication_excerpt_chars: 1622
observation_id: obs_2c28e2e12a8993e5cc4bf60d976f697c38cc2433f446bdc2482017a2493aac4e
revision_id: rev_8d89538d3462caa0fd0e489b42153a47038fa911c10769e4dfa6488352b5e1e9
event_id: evt_9d3e714849774d98fdfaa535a9d0bfda8c4df704fc66a22e6ec1e76e5a7f586a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03116v1](<https://arxiv.org/abs/2603.03116v1>)
- **作者**: Hongliu Cao, Ilias Driouich, Eoin Thomas
- **分类**: cs.AI
- **论文时间**: 2026-03-03T15:47:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03116v1.pdf](<https://arxiv.org/pdf/2603.03116v1.pdf>)

## 来源摘要/节选

> Large Language Model \(LLM\)-based agents are increasingly adopted in high-stakes settings, but current benchmarks evaluate mainly whether a task was completed, not how. We introduce Procedure-Aware Evaluation \(PAE\), a framework that formalizes agent procedures as structured observations and exposes consistency relationships between what agents observe, communicate, and execute. PAE evaluates agents along complementary axes \(Utility, Efficiency, Interaction Quality, Procedural Integrity\) and applies multi-dimensional gating that categorically disqualifies corrupt outcomes. Evaluating state-of-the-art LLM agents on tau-bench yields findings at the axis, compliance, and benchmark levels. At the axis level, the dimensions capture non-redundant failure modes: utility masks reliability gaps, speed does not imply precision, and conciseness does not predict intent adherence. At the procedural compliance level, 27-78% of benchmark reported successes are corrupt successes concealing violations across interaction and integrity. Furthermore, gating substantially collapses Pass^4 rate and affects model rankings. The analysis of corrupt success cases reveals distinctive per-model failure signatures: GPT-5 spreads errors across policy, execution, and intent dimensions; Kimi-K2-Thinking concentrates 78% of violations in policy faithfulness and compliance; and Mistral-Large-3 is dominated by faithfulness failures. At the benchmark level, our analysis exposes structural flaws in the benchmark design, including task scope gaps, contradictory reward signals, and simulator artifacts that produce accidental successes.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
