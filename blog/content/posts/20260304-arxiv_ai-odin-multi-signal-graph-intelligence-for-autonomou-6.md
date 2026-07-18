---
title: 'Odin: Multi-Signal Graph Intelligence for Autonomous Discovery in Knowledge
  Graphs'
date: 2026-03-04 03:29:03+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.03097v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8cfbda46604b37ecd9871f3fdf1d88bbc596cbf66582d2268ae8ce63db732e59
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
captured_at: '2026-07-18T04:26:49.920939Z'
source_capture_sha256: sha256:4c4dfa21e53e60e6ba2e7e770b1db9d22d1262f1532accb68f182768af4c6007
source_capture_chars_original: 1534
source_publication_excerpt_chars: 1534
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.03097v1](<https://arxiv.org/abs/2603.03097v1>)
- **作者**: Muyukani Kizito, Elizabeth Nyambere
- **分类**: cs.AI
- **论文时间**: 2026-03-03T15:34:02Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.03097v1.pdf](<https://arxiv.org/pdf/2603.03097v1.pdf>)

## 来源摘要/节选

> We present Odin, the first production-deployed graph intelligence engine for autonomous discovery of meaningful patterns in knowledge graphs without prior specification. Unlike retrieval-based systems that answer predefined queries, Odin guides exploration through the COMPASS \(Composite Oriented Multi-signal Path Assessment\) score, a novel metric that combines \(1\) structural importance via Personalized PageRank, \(2\) semantic plausibility through Neural Probabilistic Logic Learning \(NPLL\) used as a discriminative filter rather than generative model, \(3\) temporal relevance with configurable decay, and \(4\) community-aware guidance through GNN-identified bridge entities and inter-community affinity scores. This multi-signal integration, particularly the bridge scoring mechanism, addresses the "echo chamber" problem where graph exploration becomes trapped in dense local communities. We formalize the autonomous discovery problem, prove theoretical properties of our scoring function, and demonstrate that beam search with multi-signal guidance achieves $O\(b \\cdot h\)$ complexity while maintaining high recall compared to exhaustive exploration. To our knowledge, Odin represents the first autonomous discovery system deployed in regulated production environments \(healthcare and insurance\), demonstrating significant improvements in pattern discovery quality and analyst efficiency. Our approach maintains complete provenance traceability -- a critical requirement for regulated industries where hallucination is unacceptable.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
