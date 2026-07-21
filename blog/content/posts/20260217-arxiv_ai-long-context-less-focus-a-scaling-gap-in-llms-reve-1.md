---
title: 'Long Context, Less Focus: A Scaling Gap in LLMs Revealed through Privacy and
  Personalization'
date: 2026-02-17 22:35:47+08:00
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
external_url: https://arxiv.org/abs/2602.15028v1
aliases:
- /posts/20260218-arxiv_ai-long-context-less-focus-a-scaling-gap-in-llms-reve-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:48de23d7a8e7f3825471717483f110151a46439b0f63b757c2c9a2f488517a1c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 92
captured_at: '2026-07-18T04:15:37.655804Z'
source_capture_sha256: sha256:0be6a8909cbfc747ae655bc25ee8144678aa889176942250322b01314a880af5
source_capture_chars_original: 1383
source_publication_excerpt_chars: 1383
observation_id: obs_e2f0347f9096ccda1bd098c7ff68d7c1e6d30110891b71655719c09ea1be5970
revision_id: rev_c13c51e715a3bb94ffc25984da6c23cee68c7c56fbfe338badf253225236039a
event_id: evt_d11df9e5d82ad39d89a21b85acd50dd2382f742fd3a75e78a0e1580da7d2bc5f
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-17T09:52:08Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.15028v1](<https://arxiv.org/abs/2602.15028v1>)
- **作者**: Shangding Gu
- **分类**: cs.LG
- **论文时间**: 2026-02-16T18:59:42Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.15028v1.pdf](<https://arxiv.org/pdf/2602.15028v1.pdf>)

## 来源摘要/节选

> Large language models \(LLMs\) are increasingly deployed in privacy-critical and personalization-oriented scenarios, yet the role of context length in shaping privacy leakage and personalization effectiveness remains largely unexplored. We introduce a large-scale benchmark, PAPerBench, to systematically study how increasing context length influences both personalization quality and privacy protection in LLMs. The benchmark comprises approximately 29,000 instances with context lengths ranging from 1K to 256K tokens, yielding a total of 377K evaluation questions. It jointly evaluates personalization performance and privacy risks across diverse scenarios, enabling controlled analysis of long-context model behavior. Extensive evaluations across state-of-the-art LLMs reveal consistent performance degradation in both personalization and privacy as context length increases. We further provide a theoretical analysis of attention dilution under context scaling, explaining this behavior as an inherent limitation of soft attention in fixed-capacity Transformers. The empirical and theoretical findings together suggest a general scaling gap in current models -- long context, less focus. We release the benchmark to support reproducible evaluation and future research on scalable privacy and personalization. Code and data are available at https://github.com/SafeRL-Lab/PAPerBench

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
