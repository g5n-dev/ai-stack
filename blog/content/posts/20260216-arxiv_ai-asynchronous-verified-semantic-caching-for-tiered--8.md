---
title: Asynchronous Verified Semantic Caching for Tiered LLM Architectures
date: 2026-02-16 23:54:05+08:00
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
external_url: https://arxiv.org/abs/2602.13165v1
aliases:
- /posts/20260217-arxiv_ai-asynchronous-verified-semantic-caching-for-tiered--8/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:7edc829f1a79f588017517b15ede050593da9364504c8d5540af36070a52e781
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
captured_at: '2026-07-18T04:15:26.440768Z'
source_capture_sha256: sha256:d0ba9135740bc7b82b787981c3565fc2dddd6426e804eca08bb1bce521d64d8f
source_capture_chars_original: 1540
source_publication_excerpt_chars: 1540
observation_id: obs_95c01f2261b5245afa5e61968d922fd0686af5d92333f137c80a6f367e3a6595
revision_id: rev_8b338188d56aa5d2d6050174e1ad0534d5a86d94bb4ee83b6255477ab020dbf8
event_id: evt_43eaf8efe0c6e0770debe1ef709cdd5f5ab3aa1ae780c17eb94b0fce09c82771
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-16T03:51:58Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.13165v1](<https://arxiv.org/abs/2602.13165v1>)
- **作者**: Asmit Kumar Singh, Haozhe Wang, Laxmi Naga Santosh Attaluri, Tak Chiam, Weihua Zhu
- **分类**: cs.IR
- **论文时间**: 2026-02-13T18:25:00Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.13165v1.pdf](<https://arxiv.org/pdf/2602.13165v1.pdf>)

## 来源摘要/节选

> Large language models \(LLMs\) now sit in the critical path of search, assistance, and agentic workflows, making semantic caching essential for reducing inference cost and latency. Production deployments typically use a tiered static-dynamic design: a static cache of curated, offline vetted responses mined from logs, backed by a dynamic cache populated online. In practice, both tiers are commonly governed by a single embedding similarity threshold, which induces a hard tradeoff: conservative thresholds miss safe reuse opportunities, while aggressive thresholds risk serving semantically incorrect responses. We introduce \\textbf\{Krites\}, an asynchronous, LLM-judged caching policy that expands static coverage without changing serving decisions. On the critical path, Krites behaves exactly like a standard static threshold policy. When the nearest static neighbor of the prompt falls just below the static threshold, Krites asynchronously invokes an LLM judge to verify whether the static response is acceptable for the new prompt. Approved matches are promoted into the dynamic cache, allowing future repeats and paraphrases to reuse curated static answers and expanding static reach over time. In trace-driven simulations on conversational and search workloads, Krites increases the fraction of requests served with curated static answers \(direct static hits plus verified promotions\) by up to $\\textbf\{3.9\}$ times for conversational traffic and search-style queries relative to tuned baselines, with unchanged critical path latency.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
