---
title: 'DashAttention: Differentiable and Adaptive Sparse Hierarchical Attention'
date: 2026-05-19 21:00:26+08:00
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
external_url: https://arxiv.org/abs/2605.18753v1
aliases:
- /posts/20260520-arxiv_ai-dashattention-differentiable-and-adaptive-sparse-h-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ca7db645f4d6f1dd26e9dcc3624ef7aa8bebcfccab333cad6a0e54d7636f40cd
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
captured_at: '2026-07-18T04:29:39.576255Z'
source_capture_sha256: sha256:52190104d545f748b8bd054e240af1aed6737419951a8a596f5054a80b89a47b
source_capture_chars_original: 1371
source_publication_excerpt_chars: 1371
observation_id: obs_107eeaa6c9287e4466f573724fffa31ad11769b7fa8576cc6734eea446024398
revision_id: rev_58121cd7e377c6650626cd62acf6385c01a7a926ad90145744b98bac4e58bceb
event_id: evt_968c4d814430d49058d1bd563b8a4190a648ead36168a21d05214380aa6666cb
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-19T10:45:44Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.18753v1](<https://arxiv.org/abs/2605.18753v1>)
- **作者**: Yuxiang Huang, Nuno M. T. Gonçalves, Federico Alvetreti, Lei Li, Xu Han, Edoardo M. Ponti, André F. T. Martins, Marcos V. Treviso
- **分类**: cs.CL
- **论文时间**: 2026-05-18T17:59:52Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.18753v1.pdf](<https://arxiv.org/pdf/2605.18753v1.pdf>)

## 来源摘要/节选

> Current hierarchical attention methods, such as NSA and InfLLMv2, select the top-k relevant key-value \(KV\) blocks based on coarse attention scores and subsequently apply fine-grained softmax attention on the selected tokens. However, the top-k operation assumes the number of relevant tokens for any query is fixed and it precludes the gradient flow between the sparse and dense stages. In this work, we propose DashAttention \(Differentiable and Adaptive Sparse Hierarchical Attention\), which leverages the adaptively sparse $α$-entmax transformation to select a variable number of blocks according to the current query in the first stage. This in turn provides a prior for the second-stage softmax attention, keeping the entire hierarchy fully differentiable. Contrary to other hierarchical attention methods, we show that DashAttention is non-dispersive, translating to better long-context modeling ability. Experiments with large language models \(LLMs\) show that DashAttention achieves comparable accuracy as full attention with 75% sparsity and a better Pareto frontier than NSA and InfLLMv2, especially in high-sparsity regimes. We also provide an efficient, GPU-aware implementation of DashAttention in Triton, which achieves a speedup of up to over FlashAttention-3 at inference time. Overall, DashAttention offers a cost-effective strategy to model long contexts.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
