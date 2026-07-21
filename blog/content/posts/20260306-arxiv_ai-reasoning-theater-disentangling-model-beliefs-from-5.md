---
title: 'Reasoning Theater: Disentangling Model Beliefs from Chain-of-Thought'
date: 2026-03-06 23:44:05+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.05488v1
aliases:
- /posts/20260307-arxiv_ai-reasoning-theater-disentangling-model-beliefs-from-5/
- /posts/20260308-arxiv_ai-reasoning-theater-disentangling-model-beliefs-from-5/
- /posts/20260309-arxiv_ai-reasoning-theater-disentangling-model-beliefs-from-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:28c91594923064d7b4b24dd842f5b063b552b1d9cbb0e149e73aaad22354e518
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 68
captured_at: '2026-07-18T04:27:16.435086Z'
source_capture_sha256: sha256:c1d481fc7617b291d5113c680cc377559987eb152f0bc7826822adc6b5305ff2
source_capture_chars_original: 1119
source_publication_excerpt_chars: 1119
observation_id: obs_f664f1010fd184bda1b0081f038ef6e7121e1077c9301060258871fbf6b63719
revision_id: rev_39983e2aefd99d7092faa17e9d7c5e37d33c4791f1477472d6758997892fa7b9
event_id: evt_7676be2a15abcb6aa6773d84c79fd052dc76379351a4ab690bbd764877bf4473
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.05488v1](<https://arxiv.org/abs/2603.05488v1>)
- **作者**: Siddharth Boppana, Annabel Ma, Max Loeffler, Raphael Sarfati, Eric Bigelow, Atticus Geiger, Owen Lewis, Jack Merullo
- **分类**: cs.CL
- **论文时间**: 2026-03-05T18:55:16Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.05488v1.pdf](<https://arxiv.org/pdf/2603.05488v1.pdf>)

## 来源摘要/节选

> We provide evidence of performative chain-of-thought \(CoT\) in reasoning models, where a model becomes strongly confident in its final answer, but continues generating tokens without revealing its internal belief. Our analysis compares activation probing, early forced answering, and a CoT monitor across two large models \(DeepSeek-R1 671B &amp; GPT-OSS 120B\) and find task difficulty-specific differences: The model's final answer is decodable from activations far earlier in CoT than a monitor is able to say, especially for easy recall-based MMLU questions. We contrast this with genuine reasoning in difficult multihop GPQA-Diamond questions. Despite this, inflection points \(e.g., backtracking, 'aha' moments\) occur almost exclusively in responses where probes show large belief shifts, suggesting these behaviors track genuine uncertainty rather than learned "reasoning theater." Finally, probe-guided early exit reduces tokens by up to 80% on MMLU and 30% on GPQA-Diamond with similar accuracy, positioning attention probing as an efficient tool for detecting performative reasoning and enabling adaptive computation.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
