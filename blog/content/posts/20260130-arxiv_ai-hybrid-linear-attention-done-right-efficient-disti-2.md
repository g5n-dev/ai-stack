---
title: 'Hybrid Linear Attention Done Right: Efficient Distillation and Effective Architectures
  for Extremely Long Contexts'
date: 2026-01-30 23:03:03+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.22156v1
aliases:
- /posts/20260131-arxiv_ai-hybrid-linear-attention-done-right-efficient-disti-2/
- /posts/20260201-arxiv_ai-hybrid-linear-attention-done-right-efficient-disti-2/
- /posts/20260202-arxiv_ai-hybrid-linear-attention-done-right-efficient-disti-2/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a97c2c050a9773774e5f5b053afddb9f0935246b2ac03927aaa91d03755ccc40
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 114
captured_at: '2026-07-18T04:09:52.752345Z'
source_capture_sha256: sha256:5d46b912655807587fdb023da7a5e2f3997bff3f29f797489c533c6567688b4a
source_capture_chars_original: 1355
source_publication_excerpt_chars: 1355
observation_id: obs_895b6051d2e381455c25df7e3b7a5d36723050c275b7fb99e7f6d74c91805c4d
revision_id: rev_90f46628bf100f5ba63dc4e2c18fc138bb9cd77fa3031c3d2eff60a910c29241
event_id: evt_88ab189626f9a0362fdd733bd0d429f0971344280a3309baee36b3136acb3ec2
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.22156v1](<https://arxiv.org/abs/2601.22156v1>)
- **作者**: Yingfa Chen, Zhen Leng Thai, Zihan Zhou, Zhu Zhang, Xingyu Shen, Shuo Wang, Chaojun Xiao, Xu Han, Zhiyuan Liu
- **分类**: cs.CL
- **论文时间**: 2026-01-29T18:59:53Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.22156v1.pdf](<https://arxiv.org/pdf/2601.22156v1.pdf>)

## 来源摘要/节选

> Hybrid Transformer architectures, which combine softmax attention blocks and recurrent neural networks \(RNNs\), have shown a desirable performance-throughput tradeoff for long-context modeling, but their adoption and studies are hindered by the prohibitive cost of large-scale pre-training from scratch. Some recent studies have shown that pre-trained softmax attention blocks can be converted into RNN blocks through parameter transfer and knowledge distillation. However, these transfer methods require substantial amounts of training data \(more than 10B tokens\), and the resulting hybrid models also exhibit poor long-context performance, which is the scenario where hybrid models enjoy significant inference speedups over Transformer-based models. In this paper, we present HALO \(Hybrid Attention via Layer Optimization\), a pipeline for distilling Transformer models into RNN-attention hybrid models. We then present HypeNet, a hybrid architecture with superior length generalization enabled by a novel position encoding scheme \(named HyPE\) and various architectural modifications. We convert the Qwen3 series into HypeNet using HALO, achieving performance comparable to the original Transformer models while enjoying superior long-context performance and efficiency. The conversion requires just 2.3B tokens, less than 0.01% of their pre-training data

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
