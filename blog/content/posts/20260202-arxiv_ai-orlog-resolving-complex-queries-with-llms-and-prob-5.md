---
title: 'OrLog: Resolving Complex Queries with LLMs and Probabilistic Reasoning'
date: 2026-02-02 02:57:13+08:00
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
external_url: https://arxiv.org/abs/2601.23085v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:bbe5f9a765b919837b3b45ab8144d034769f71149893af8b2e9a1931f273861d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 70
captured_at: '2026-07-18T04:10:15.469098Z'
source_capture_sha256: sha256:975d1ef9ea0bfd90b6e54d231f9064ba67630083636835d9ddcda0dfb16411a3
source_capture_chars_original: 1679
source_publication_excerpt_chars: 1679
observation_id: obs_eacb1e0602016d60bd9bd2f6c97e25462d643c44b0df8c8a25937279eab509ce
revision_id: rev_5f36f7bec7342a149617a54d0e26524f17d57b6e2b543fb2d0808163dbc72dcb
event_id: evt_6aa413ae88ae18bc0f9439be7ee2c69e8dbc28488c92015ac6d7cf7d65ea53fb
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23085v1](<https://arxiv.org/abs/2601.23085v1>)
- **作者**: Mohanna Hoveyda, Jelle Piepenbrock, Arjen P de Vries, Maarten de Rijke, Faegheh Hasibi
- **分类**: cs.IR
- **论文时间**: 2026-01-30T15:31:58Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23085v1.pdf](<https://arxiv.org/pdf/2601.23085v1.pdf>)

## 来源摘要/节选

> Resolving complex information needs that come with multiple constraints should consider enforcing the logical operators encoded in the query \(i.e., conjunction, disjunction, negation\) on the candidate answer set. Current retrieval systems either ignore these constraints in neural embeddings or approximate them in a generative reasoning process that can be inconsistent and unreliable. Although well-suited to structured reasoning, existing neuro-symbolic approaches remain confined to formal logic or mathematics problems as they often assume unambiguous queries and access to complete evidence, conditions rarely met in information retrieval. To bridge this gap, we introduce OrLog, a neuro-symbolic retrieval framework that decouples predicate-level plausibility estimation from logical reasoning: a large language model \(LLM\) provides plausibility scores for atomic predicates in one decoding-free forward pass, from which a probabilistic reasoning engine derives the posterior probability of query satisfaction. We evaluate OrLog across multiple backbone LLMs, varying levels of access to external knowledge, and a range of logical constraints, and compare it against base retrievers and LLM-as-reasoner methods. Provided with entity descriptions, OrLog can significantly boost top-rank precision compared to LLM reasoning with larger gains on disjunctive queries. OrLog is also more efficient, cutting mean tokens by $\\sim$90\\% per query-entity pair. These results demonstrate that generation-free predicate plausibility estimation combined with probabilistic reasoning enables constraint-aware retrieval that outperforms monolithic reasoning while using far fewer tokens.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
