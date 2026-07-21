---
title: 'Reasoning While Asking: Transforming Reasoning Large Language Models from
  Passive Solvers to Proactive Inquirers'
date: 2026-01-30 23:03:03+08:00
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
external_url: https://arxiv.org/abs/2601.22139v1
aliases:
- /posts/20260131-arxiv_ai-reasoning-while-asking-transforming-reasoning-larg-9/
- /posts/20260201-arxiv_ai-reasoning-while-asking-transforming-reasoning-larg-9/
- /posts/20260202-arxiv_ai-reasoning-while-asking-transforming-reasoning-larg-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:60b30ffd760e134c48b4589b4a1a225d8386c8dc0adc0e860b298ab987869f2a
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 112
captured_at: '2026-07-18T04:09:52.752345Z'
source_capture_sha256: sha256:7d2f0d91f1849bc247a38b4c27b092914ba3d3b35f6976150e543a5b37089f70
source_capture_chars_original: 1601
source_publication_excerpt_chars: 1601
observation_id: obs_cbfd6880ce5eafb55dc4fd0d80a6a7e5511b6879785079a7eede349ab4358552
revision_id: rev_3de8e1c4a77feef038abe12d434dc9c8393ec5f413daadbce247e854cea19561
event_id: evt_d677fb45dec8ec8f411e2818aa6f1d5ff58b31914918d5ade6487dcca13c7650
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-01-30T05:20:34Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.22139v1](<https://arxiv.org/abs/2601.22139v1>)
- **作者**: Xin Chen, Feng Jiang, Yiqian Zhang, Hardy Chen, Shuo Yan, Wenya Xie, Min Yang, Shujian Huang
- **分类**: cs.CL
- **论文时间**: 2026-01-29T18:56:12Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.22139v1.pdf](<https://arxiv.org/pdf/2601.22139v1.pdf>)

## 来源摘要/节选

> Reasoning-oriented Large Language Models \(LLMs\) have achieved remarkable progress with Chain-of-Thought \(CoT\) prompting, yet they remain fundamentally limited by a \\emph\{blind self-thinking\} paradigm: performing extensive internal reasoning even when critical information is missing or ambiguous. We propose Proactive Interactive Reasoning \(PIR\), a new reasoning paradigm that transforms LLMs from passive solvers into proactive inquirers that interleave reasoning with clarification. Unlike existing search- or tool-based frameworks that primarily address knowledge uncertainty by querying external environments, PIR targets premise- and intent-level uncertainty through direct interaction with the user. PIR is implemented via two core components: \(1\) an uncertainty-aware supervised fine-tuning procedure that equips models with interactive reasoning capability, and \(2\) a user-simulator-based policy optimization framework driven by a composite reward that aligns model behavior with user intent. Extensive experiments on mathematical reasoning, code generation, and document editing demonstrate that PIR consistently outperforms strong baselines, achieving up to 32.70\\% higher accuracy, 22.90\\% higher pass rate, and 41.36 BLEU improvement, while reducing nearly half of the reasoning computation and unnecessary interaction turns. Further reliability evaluations on factual knowledge, question answering, and missing-premise scenarios confirm the strong generalization and robustness of PIR. Model and code are publicly available at: \\href\{https://github.com/SUAT-AIRI/Proactive-Interactive-R1\}

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
