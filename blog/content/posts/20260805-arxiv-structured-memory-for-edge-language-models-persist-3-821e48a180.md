---
title: "Structured Memory for Edge Language Models: Persistent Context and Corpus Retrieval via O(1) SSM State Injection"
date: 2026-08-05T07:21:52+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "RAG", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:89a5bab14b931cc5d98da0ae365dfa043b7eed67f835c33add49454dfd0c5dc5"
source_payload_sha256: "sha256:65cc8d45af929b69df41f8c388c4d9329e7e01310db99e898f05ba649ae52c27"
observation_id: obs_821e48a1801541edffcff0c7034398255d1efa20724c4185e0fd034aa09495bb
event_id: evt_2d65153d9fbc828a90bc7e35cb0f32bfed9180c72b0f3a26b12e40ea854aa3bd
revision_id: rev_6dc7c89eaaffa8f78380f41e4c5b1969ddd2ed54e1fd6996abab03e117e18031
source_published_at: 2026-08-03T17:43:36Z
first_seen_at: 2026-08-04T23:18:43.244775Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 112
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.02560v1
parent_observation_id: null
last_seen_at: 2026-08-04T23:18:43.244775Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.02560v1](http://arxiv.org/abs/2608.02560v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Anusha Madan Gopal、Aras Pirbadian、Kristofor D. Carlson 等

## 来源摘要/节选

> Retrieval-augmented generation (RAG) imposes a prefill cost proportional to retrieved context length, and -- with Transformer backbones -- a KV-cache that grows with each generated token. State-Space Models (SSMs) avoid the second cost by construction; we eliminate the first, collapsing prefill from $O(L_{context})$ to $O(1)$ per query. We introduce PRECOG (Pre-Computed Context Injection), a retrieval mechanism that exploits a property unique to SSMs: the fixed-size, position-agnostic recurrent hidden state is a complete summary of everything the model has read. PRECOG pre-encodes document corpora offline as SSM hidden states and injects the best-matching state directly at query time, bypassing in-context re-ingestion entirely. The same state-injection mechanism enables SMC (Structured Memory Consolidation): a hierarchical persistent memory with cognitive-domain clustering, an adjustable fidelity-vs-storage dial, and $O(1)$ session initialization, which consolidates short-term episodic states into long-term semantic memory and fuses both with retrieved corpus states at query time. We demonstrate the system on TENNs-LLM, a 1.2B-parameter gated-SSM language model with a 192 KB hidden state. PRECOG matches in-context RAG answer quality, reducing prefill latency from $\sim$27 s to $&lt;$6 ms on edge hardware -- a $\sim$4500$\times$ speedup that crosses the threshold from unusable to interactive. The mechanism is architecturally impossible for Transformer KV-caches, which are position-entangled and grow linearly with context length.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。