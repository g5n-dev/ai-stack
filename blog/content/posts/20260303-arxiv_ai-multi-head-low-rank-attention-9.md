---
title: Multi-Head Low-Rank Attention
date: 2026-03-03 23:28:17+08:00
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
external_url: https://arxiv.org/abs/2603.02188v1
aliases:
- /posts/20260304-arxiv_ai-multi-head-low-rank-attention-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:9e44d28c6d3c49e3297decb28502f602e91ce0dabfcac7aa31152488cf88cb92
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 29
captured_at: '2026-07-18T04:26:34.932328Z'
source_capture_sha256: sha256:32b6ddde3582b621c74f3c94c509fa25e3c6056ccf24beeba1a039129a551ff4
source_capture_chars_original: 1202
source_publication_excerpt_chars: 1202
observation_id: obs_3ed356cbc2b82e36aaf8cf8c947fe754adb6a0b53e2cd87875a91b0d206ba701
revision_id: rev_6c79f94f452d1c384b7ea27b598d594fb8c4ddc2d0b400992dae987b4b8d0bec
event_id: evt_51155dca5c0539152effa751c8772229426dcda32343febd90ab6c16e29b063a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-03T06:15:49Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02188v1](<https://arxiv.org/abs/2603.02188v1>)
- **作者**: Songtao Liu, Hongwu Peng, Zhiwei Zhang, Zhengyu Chen, Yue Guo
- **分类**: cs.LG
- **论文时间**: 2026-03-02T18:52:38Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02188v1.pdf](<https://arxiv.org/pdf/2603.02188v1.pdf>)

## 来源摘要/节选

> Long-context inference in large language models is bottlenecked by Key--Value \(KV\) cache loading during the decoding stage, where the sequential nature of generation requires repeatedly transferring the KV cache from off-chip High-Bandwidth Memory \(HBM\) to on-chip Static Random-Access Memory \(SRAM\) at each step. While Multi-Head Latent Attention \(MLA\) significantly reduces the total KV cache size, it suffers from a sharding bottleneck during distributed decoding via Tensor Parallelism \(TP\). Since its single latent head cannot be partitioned, each device is forced to redundantly load the complete KV cache for every token, consuming excessive memory traffic and diminishing TP benefits like weight sharding. In this work, we propose Multi-Head Low-Rank Attention \(MLRA\), which enables partitionable latent states for efficient 4-way TP decoding. Extensive experiments show that MLRA achieves state-of-the-art perplexity and downstream task performance, while also delivering a 2.8$\\times$ decoding speedup over MLA. Code is available at https://github.com/SongtaoLiu0823/MLRA. Pretrained weights, along with the training and evaluation data, are available at https://huggingface.co/Soughing/MLRA.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
