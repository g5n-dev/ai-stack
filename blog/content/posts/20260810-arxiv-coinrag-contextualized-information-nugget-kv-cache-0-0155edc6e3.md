---
title: "CoinRAG: Contextualized Information Nugget KV Cache Reuse for Long-Context RAG"
date: 2026-08-10T14:43:45+08:00
draft: false
entry_kind: "auto"
tags: ["RAG", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:e895d91f33306ce5200967cc4fbd0cb81945dfeca7b1353e7d66c566e5388782"
source_payload_sha256: "sha256:77622cc2a6dc625cd2289ee460519b1510af54e10e2435ef5f6afbcd12f1ac89"
observation_id: obs_0155edc6e399a21918e4bdc167433bb618be2dd01deca604a4f6afb5eb833eab
event_id: evt_ae2f9230feeae9e6775a7a6494d4850874d3b8d8173a4f267f72f7baa3c16fdb
revision_id: rev_616a9d3b5ec071fbee24389a593d521eab61abda4f4c4bed973c52248f876d96
source_published_at: 2026-08-07T17:51:49Z
first_seen_at: 2026-08-10T06:53:51Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
interpretation_sha256: "sha256:d0ea728cf2efecb92fc4572879ccab1134219e54e646d281eeb33ca871367cd2"
description: "该方法通过在检索得到的段落中定位与查询相关的细粒度语义单元，并把它们对应的 KV 表示与段落级上下文组合，实现细粒度缓存的复用，从而在保持较低预填充延迟的同时提升答案质量。"
external_url: http://arxiv.org/abs/2608.07458v1
parent_observation_id: null
last_seen_at: 2026-08-10T06:41:50.396428Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.07458v1](http://arxiv.org/abs/2608.07458v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Gyuwan Kim、Cheoneum Park、Tao Yang

## 要点解读

### 这是什么  
该方法通过在检索得到的段落中定位与查询相关的细粒度语义单元，并把它们对应的 KV 表示与段落级上下文组合，实现细粒度缓存的复用，从而在保持较低预填充延迟的同时提升答案质量。

### 用在哪里  
适用于需要处理长上下文的检索增强生成系统，特别是多跳问答类任务。研发长上下文模型或优化检索流水线的人员可能会关注此类技术，以在效率和准确性之间取得更好的平衡。

### 可以推断的  
推测：在实际部署中，缓存的细粒度划分可以降低对完整块重新编码的计算开销，从而减少响应延迟。  
推测：该技术的实现需要额外的检索阶段来筛选相关语义单元，可能增加系统设计的复杂度。

## 来源摘要/节选

> Recent optimization studies on Retrieval-Augmented Generation (RAG) have exploited chunk-level KV cache reuse to avoid processing long retrieved contexts for higher efficiency, while significant information redundancy and noise still remain in the coarse-grained chunks. This paper optimizes the Pareto frontier under low prefill latency constraints while maximizing accuracy by proposing CoinRAG (Contextualized Information Nugget KV Cache Reuse for Long-Context RAG). The name metaphorically reflects our core mechanism: much like assembling small tokens (or "coins") to accumulate a larger value, CoinRAG compositionally reuses offline-computed, fine-grained nugget caches to form a learned contextual representation efficiently in a more semantically relevant but compact manner. Specifically, instead of full-chunk encoding, CoinRAG identifies query-relevant semantic units within retrieved chunks through two-stage retrieval and seamlessly assembles their sliced KV representations with a chunk-level context. Extensive evaluations on LongBench multi-hop question answering tasks demonstrate that CoinRAG significantly reduces operational costs and outperforms the other baselines with a new Pareto frontier and an average 5.3% relative improvement in answer quality (F1) under a standard fast prefill latency budget.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。