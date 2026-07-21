---
title: 'Multi-Head LatentMoE and Head Parallel: Communication-Efficient and Deterministic
  MoE Parallelism'
date: 2026-02-05 23:03:18+08:00
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
external_url: https://arxiv.org/abs/2602.04870v1
aliases:
- /posts/20260206-arxiv_ai-multi-head-latentmoe-and-head-parallel-communicati-5/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:67269691d9923e888c4b55e2dec12781f52aabbf4ad1fcae4928907721200e45
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 97
captured_at: '2026-07-18T04:10:49.793468Z'
source_capture_sha256: sha256:6d0cafc1cb16985a9d61bfdf06aa6980cc84fb7d6245babf1d5a1af7d0179eeb
source_capture_chars_original: 1106
source_publication_excerpt_chars: 1106
observation_id: obs_6d71a6347f7a531669d850013b6d2da33fb6ff571d738d93cd4ce70439465af1
revision_id: rev_7ebbbf6572a4a3db7061e2811a4cbe52a98e905a973a0dca5dd636735062bea6
event_id: evt_26baf9570f1935c19459d2d361e36344a7d3080012a8251e43cb3227ae5dbf0c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.04870v1](<https://arxiv.org/abs/2602.04870v1>)
- **作者**: Chenwei Cui, Rockwell Jackson, Benjamin Joseph Herrera, Ana María Tárano, Hannah Kerner
- **分类**: cs.LG
- **论文时间**: 2026-02-04T18:57:19Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.04870v1.pdf](<https://arxiv.org/pdf/2602.04870v1.pdf>)

## 来源摘要/节选

> Large language models have transformed many applications but remain expensive to train. Sparse Mixture of Experts \(MoE\) addresses this through conditional computation, with Expert Parallel \(EP\) as the standard distributed training method. However, EP has three limitations: communication cost grows linearly with the number of activated experts $k$, load imbalance affects latency and memory usage, and data-dependent communication requires metadata exchange. We propose Multi-Head LatentMoE and Head Parallel \(HP\), a new architecture and parallelism achieving $O\(1\)$ communication cost regardless of $k$, completely balanced traffic, and deterministic communication, all while remaining compatible with EP. To accelerate Multi-Head LatentMoE, we propose IO-aware routing and expert computation. Compared to MoE with EP, Multi-Head LatentMoE with HP trains up to $1.61\\times$ faster while having identical performance. With doubled granularity, it achieves higher overall performance while still being $1.11\\times$ faster. Our method makes multi-billion-parameter foundation model research more accessible.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
