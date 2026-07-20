---
title: 'LLM as Graph Kernel: Rethinking Message Passing on Text-Rich Graphs'
date: 2026-03-17 03:25:32+08:00
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
external_url: https://arxiv.org/abs/2603.14937v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ec98db780ea5502d47c6717811591078b45ef6dd18fb9763c5371fec7cd9bc63
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
captured_at: '2026-07-18T04:28:34.236322Z'
source_capture_sha256: sha256:c418b10f9460f8b850d509596f2458c5480222de65a724bbf2098088b4101586
source_capture_chars_original: 1302
source_publication_excerpt_chars: 1302
observation_id: obs_75ff70510b9f6afc30a29c1f03a1269304867f0561751917832f980cf583d2ba
revision_id: rev_60a619c5c8dbb219a7f8f667fcb1bb4dc0e67efb52ac685941c03255b51a1d9c
event_id: evt_e52bd8282ea62ee0118573b75616c4672e739ba7ec3e553b3980a770939cee9b
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.14937v1](<https://arxiv.org/abs/2603.14937v1>)
- **作者**: Ying Zhang, Hang Yu, Haipeng Zhang, Peng Di
- **分类**: cs.LG
- **论文时间**: 2026-03-16T07:40:09Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.14937v1.pdf](<https://arxiv.org/pdf/2603.14937v1.pdf>)

## 来源摘要/节选

> Text-rich graphs, which integrate complex structural dependencies with abundant textual information, are ubiquitous yet remain challenging for existing learning paradigms. Conventional methods and even LLM-hybrids compress rich text into static embeddings or summaries before structural reasoning, creating an information bottleneck and detaching updates from the raw content. We argue that in text-rich graphs, the text is not merely a node attribute but the primary medium through which structural relationships are manifested. We introduce RAMP, a Raw-text Anchored Message Passing approach that moves beyond using LLMs as mere feature extractors and instead recasts the LLM itself as a graph-native aggregation operator. RAMP exploits the text-rich nature of the graph via a novel dual-representation scheme: it anchors inference on each node's raw text during each iteration while propagating dynamically optimized messages from neighbors. It further handles both discriminative and generative tasks under a single unified generative formulation. Extensive experiments show that RAMP effectively bridges the gap between graph propagation and deep text reasoning, achieving competitive performance and offering new insights into the role of LLMs as graph kernels for general-purpose graph learning.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
