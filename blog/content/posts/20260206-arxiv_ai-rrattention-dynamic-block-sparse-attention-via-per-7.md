---
title: 'RRAttention: Dynamic Block Sparse Attention via Per-Head Round-Robin Shifts
  for Long-Context Inference'
date: 2026-02-06 03:10:07+08:00
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
external_url: https://arxiv.org/abs/2602.05853v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:0be1389d616d2be4b3f52723a50d04f673733cef46f8650b2daba00ed724c0d5
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 102
captured_at: '2026-07-18T04:11:20.263833Z'
source_capture_sha256: sha256:3c922256a1594ee7341d29ef3b5e29b5f235e938a17f449059cfeaa5f2b8b85f
source_capture_chars_original: 1229
source_publication_excerpt_chars: 1229
observation_id: obs_4f87788c8154cfa684b80da578f27f97f53502ce8b499ac1090c04b0b2002df9
revision_id: rev_752aeb74e43de6b8bd550a7401d54000f9c1b9ea5170c8818000519087327cd7
event_id: evt_5039663efd8769413bdadfcc942f6e3949bae1228020ab41708b60968757295c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.05853v1](<https://arxiv.org/abs/2602.05853v1>)
- **作者**: Siran Liu, Guoxia Wang, Sa Wang, Jinle Zeng, HaoYang Xie, Siyu Lou, JiaBin Yang, DianHai Yu, Haifeng Wang, Chao Yang
- **分类**: cs.CL
- **论文时间**: 2026-02-05T16:37:41Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.05853v1.pdf](<https://arxiv.org/pdf/2602.05853v1.pdf>)

## 来源摘要/节选

> The quadratic complexity of attention mechanisms poses a critical bottleneck for large language models processing long contexts. While dynamic sparse attention methods offer input-adaptive efficiency, they face fundamental trade-offs: requiring preprocessing, lacking global evaluation, violating query independence, or incurring high computational overhead. We present RRAttention, a novel dynamic sparse attention method that simultaneously achieves all desirable properties through a head \\underline\{r\}ound-\\underline\{r\}obin \(RR\) sampling strategy. By rotating query sampling positions across attention heads within each stride, RRAttention maintains query independence while enabling efficient global pattern discovery with stride-level aggregation. Our method reduces complexity from $O\(L^2\)$ to $O\(L^2/S^2\)$ and employs adaptive Top-$τ$ selection for optimal sparsity. Extensive experiments on natural language understanding \(HELMET\) and multimodal video comprehension \(Video-MME\) demonstrate that RRAttention recovers over 99\\% of full attention performance while computing only half of the attention blocks, achieving 2.4$\\times$ speedup at 128K context length and outperforming existing dynamic sparse attention methods.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
