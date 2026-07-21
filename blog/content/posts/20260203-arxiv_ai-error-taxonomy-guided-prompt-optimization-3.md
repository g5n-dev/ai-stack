---
title: Error Taxonomy-Guided Prompt Optimization
date: 2026-02-03 03:49:30+08:00
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
external_url: https://arxiv.org/abs/2602.00997v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2f93658cb53f6a73628b8bc2cbd98a3b5fa07f8a97e72eafbc53d55ddea73381
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 41
captured_at: '2026-07-18T04:10:26.671991Z'
source_capture_sha256: sha256:9d51fdd27bbe9db7a128c77b4eb016195e585a3e7ce0a88ba242a2be97f647ea
source_capture_chars_original: 1245
source_publication_excerpt_chars: 1245
observation_id: obs_84a07b697a2c9ad4e0dc7d90308796a4734294055f49bb49ea66250c07223a7e
revision_id: rev_0b1b88ec6fb98dfb8a3af2c6c6a41dad4a94de9a8ee8948520a290829e4e4ecd
event_id: evt_ec708b462ab5ce4c1c1ea987c6cfb6cab42fe04954ae1704203d7d25c59a80eb
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-03T03:56:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.00997v1](<https://arxiv.org/abs/2602.00997v1>)
- **作者**: Mayank Singh, Vikas Yadav, Eduardo Blanco
- **分类**: cs.AI
- **论文时间**: 2026-02-01T03:27:44Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.00997v1.pdf](<https://arxiv.org/pdf/2602.00997v1.pdf>)

## 来源摘要/节选

> Automatic Prompt Optimization \(APO\) is a powerful approach for extracting performance from large language models without modifying their weights. Many existing methods rely on trial-and-error, testing different prompts or in-context examples until a good configuration emerges, often consuming substantial compute. Recently, natural language feedback derived from execution logs has shown promise as a way to identify how prompts can be improved. However, most prior approaches operate in a bottom-up manner, iteratively adjusting the prompt based on feedback from individual problems, which can cause them to lose the global perspective. In this work, we propose Error Taxonomy-Guided Prompt Optimization \(ETGPO\), a prompt optimization algorithm that adopts a top-down approach. ETGPO focuses on the global failure landscape by collecting model errors, categorizing them into a taxonomy, and augmenting the prompt with guidance targeting the most frequent failure modes. Across multiple benchmarks spanning mathematics, question answering, and logical reasoning, ETGPO achieves accuracy that is comparable to or better than state-of-the-art methods, while requiring roughly one third of the optimization-phase token usage and evaluation budget.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
