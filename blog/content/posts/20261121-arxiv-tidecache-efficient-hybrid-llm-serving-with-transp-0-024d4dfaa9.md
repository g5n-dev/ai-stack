---
title: "TideCache: Efficient Hybrid LLM Serving with Transparent Cache Management and Layer-Wise Streaming"
date: 2026-11-21T17:48:46+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.DC", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:eed0d3bfc6dc5bc6e3af26cbf7ef5e1fbb47e7dde76f66b6ee439a8f80d6f66f"
source_payload_sha256: "sha256:e9affbccf185d410b51a7601aff024057d8ea0caae5fc0fb8d13dbc85a629f8d"
observation_id: obs_024d4dfaa92472bb45ad3f362734909814bedfaa4cf900b6dd0f1c889307d928
event_id: evt_4d904102204bec831047a8651d072e24b2166a47f3a97f0caef5c52d1f5975ab
revision_id: rev_ccd5fce6946756a0e44cc8f84e24f779b81ebb98fbb663a723949b59c229e403
source_published_at: 2026-11-19T18:58:31Z
first_seen_at: 2026-11-21T09:47:22.336174Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 98
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2611.26619v1
parent_observation_id: null
last_seen_at: 2026-11-21T09:47:22.336174Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.26619v1](http://arxiv.org/abs/2611.26619v1)
- **发布域名**: arxiv.org
- **分类**: cs.DC
- **作者**: Jinbin Luo、Xiaozhe Yao、Shang Yang 等

## 来源摘要/节选

> Hybrid architectures have become mainstream among open-weight language models. Their global-attention and bounded-state layers maintain heterogeneous caches whose demands vary with context length and concurrency. We present TideCache, a serving system on CPU--GPU superchips with three components for allocating GPU memory among caches and managing their residency across GPU and host memory. The Transparent Cache Pool redistributes physical pages among cache components behind fixed virtual addresses, preserving cache layouts and backend interfaces. The Cache Streamer uses computation intervals provided by bounded-state layers to prefetch the next global-attention layer's prefix into GPU slots shared across global-attention layers, reducing GPU residency while overlapping layer-wise transfers with computation. Generated KV remains resident. The Request Scheduler selects resident or streamed execution and triggers capacity adjustments according to request size and queue state. Together, they let HBM released by streaming accommodate other cache components and additional requests. Implemented in SGLang and evaluated on GB300 and GH200 across seven model/platform configurations, TideCache completes up to 2.04x as many agent turns, reduces overall P50 per-token latency by 20--59%, and improves agent P50 TTFT by 1.40--3.05x compared with SGLang with HiCache.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。