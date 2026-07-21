---
title: 'TDAD: Test-Driven Agentic Development - Reducing Code Regressions in AI Coding
  Agents via Graph-Based Impact Analysis'
date: 2026-03-19 18:55:56+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
categories:
- 论文
scenarios:
- AI/ML项目
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.17973v1
aliases:
- /posts/20260320-arxiv_ai-tdad-test-driven-agentic-development-reducing-code-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e8944c8ed28f027c71d12b7150169672f0f1660c4632b24c972a470d6c7bd828
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 117
captured_at: '2026-07-18T04:29:00.882647Z'
source_capture_sha256: sha256:a662cc103f96e38be5996f3e00bcd4715bccdf3515fb19fa5a81b68995efc2c0
source_capture_chars_original: 1362
source_publication_excerpt_chars: 1362
observation_id: obs_d6f724ef7e21daabd74bce567be02a13830bd9d7ecfca071eae1e3a3317c1401
revision_id: rev_d7f2cbb1521f06e167bbed94a17d013d3acff777bd6f5c279eac538a435307ad
event_id: evt_dc3956f9e74f9208a7909e12ae83898c60768106d662c65f47f38180725e5f95
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-19T20:50:47Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.17973v1](<https://arxiv.org/abs/2603.17973v1>)
- **作者**: Pepe Alonso
- **分类**: cs.SE
- **论文时间**: 2026-03-18T17:38:22Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.17973v1.pdf](<https://arxiv.org/pdf/2603.17973v1.pdf>)

## 来源摘要/节选

> AI coding agents can resolve real-world software issues, yet they frequently introduce regressions, breaking tests that previously passed. Current benchmarks focus almost exclusively on resolution rate, leaving regression behavior under-studied. This paper presents TDAD \(Test-Driven Agentic Development\), an open-source tool and benchmark methodology that combines abstract-syntax-tree \(AST\) based code-test graph construction with weighted impact analysis to surface the tests most likely affected by a proposed change. Evaluated on SWE-bench Verified with two local models \(Qwen3-Coder 30B on 100 instances and Qwen3.5-35B-A3B on 25 instances\), TDAD's GraphRAG workflow reduced test-level regressions by 70% \(6.08% to 1.82%\) and improved resolution from 24% to 32% when deployed as an agent skill. A surprising finding is that TDD prompting alone increased regressions \(9.94%\), revealing that smaller models benefit more from contextual information \(which tests to verify\) than from procedural instructions \(how to do TDD\). An autonomous auto-improvement loop raised resolution from 12% to 60% on a 10-instance subset with 0% regression. These findings suggest that for AI agent tool design, surfacing contextual information outperforms prescribing procedural workflows. All code, data, and logs are publicly available at https://github.com/pepealonso95/TDAD.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
