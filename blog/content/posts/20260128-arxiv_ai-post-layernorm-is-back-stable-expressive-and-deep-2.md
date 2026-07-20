---
title: 'Post-LayerNorm Is Back: Stable, ExpressivE, and Deep'
date: 2026-01-28 07:28:04+08:00
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
external_url: https://arxiv.org/abs/2601.19895v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:8d1618e97e890fc3fff97534bbc0b9643ca7ae943d1966bcdebea6746a395609
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
captured_at: '2026-07-18T04:09:22.840879Z'
source_capture_sha256: sha256:5a1cfa458678ba029658779f93c2d38359ee0936d2a14a6636dc7c212c0edcbb
source_capture_chars_original: 1355
source_publication_excerpt_chars: 1355
observation_id: obs_7ecc3957e45c9b3cafb04423b81b1085464bc9981845661d7b3a7be0c7ce7707
revision_id: rev_0df30a872a7e7d14fb45782fec2a5d04cb8d81fd215a81d4c21d37a430bd38a9
event_id: evt_0942d88595582ed4861824dad3eb95d75852f25b3483434f009a80d1837595bd
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.19895v1](<https://arxiv.org/abs/2601.19895v1>)
- **作者**: Chen Chen, Lai Wei
- **分类**: cs.LG
- **论文时间**: 2026-01-27T18:58:46Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.19895v1.pdf](<https://arxiv.org/pdf/2601.19895v1.pdf>)

## 来源摘要/节选

> Large language model \(LLM\) scaling is hitting a wall. Widening models yields diminishing returns, and extending context length does not improve fundamental expressivity. In contrast, depth scaling offers theoretically superior expressivity, yet current Transformer architectures struggle to train reliably at extreme depths. We revisit the Post-LayerNorm \(Post-LN\) formulation, whose instability at scale caused its replacement by Pre-LN in modern LLMs. We show that the central failure mode of Post-LN arises from the ResNet-style residual pathway, which introduces gradient vanishing in deep networks. We present Keel, a Post-LN Transformer that replaces this residual path with a Highway-style connection. This modification preserves the gradient flow through the residual branch, preventing signal vanishing from the top layers to the bottom. Unlike prior methods, Keel enables stable training at extreme depths without requiring specialized initialization or complex optimization tricks. Keel trains robustly at depths exceeding 1000 layers and consistently improves perplexity and depth-scaling characteristics over Pre-LN. These findings indicate that Post-LN, when paired with a Highway-style connection, provides a simple and effective foundation for building deeply scalable LLMs, opening the possibility for future infinite-depth architectures.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
