---
title: "TokTier: Exact Stateful Tokenization for Agentic LLM Serving"
date: 2026-08-03T16:05:36+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:c2ed6edc728a7a8c9293979ad196f9eba6e475ae060656ccb3c331853c819405"
source_payload_sha256: "sha256:489ed7419217aba69642c5b9303561b005f4dfbd0d6313f444d3548f6e335bb2"
observation_id: obs_44ebed60b644f36e02ce4e55cff17920304b23c66aee258cd27c99e070da4f2a
event_id: evt_91387868212c6283496fb24692836b47c61cf4fc22eb96447157d4c4f55dbde6
revision_id: rev_093cc95935ba201bc864daae5c9427406f5b4edd7577628d78713dd814e028ec
source_published_at: 2026-07-31T17:56:30Z
first_seen_at: 2026-08-03T08:02:51.725389Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.29678v1
parent_observation_id: null
last_seen_at: 2026-08-03T08:02:51.725389Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.29678v1](http://arxiv.org/abs/2607.29678v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Zhenyu Zhang、Zhichao Cao

## 来源摘要/节选

> LLM serving systems cache prompt KV state, yet most front ends still re-tokenize the full request text on every call. The cost lands on coding agents, which resubmit a long transcript after each small tool result, and reuse is hard because even a short append can change token boundaries near the end of the previous sequence. Across 153,951 calls from two agent ecosystems, the median call appends about 1.4K characters, and only 1.0-3.6% of calls start or rebuild a session with contexts of millions of characters. At a 94.1% fleet prompt-cache hit rate, tokenization reaches up to 64% of time to first token.
> TokTier is a stateful tokenization service with one contract: emitted token IDs are always identical to full reference tokenization of the request text. For a session continuation, it re-tokenizes a small window around the append and splices only after a per-request stable-boundary check, widening the window or falling back to full tokenization on failure. For a call without a reusable prefix, it decomposes GPT-family regex pre-tokenization into run-local rules and runs exact pre-tokenization and BPE on a GPU. A sampled shadow verifier re-checks live traffic.
> Across 17 tokenizer families, differential campaigns cover 1.5x10^10 split checks, a 12.4 TB real-text corpus, and 93,000+ replayed agent steps, with zero divergence. Incremental repair takes 0.5-1.1 ms from 100K to 3M characters, up to 437x faster than HF tokenization and 2.1x faster at 1M than the strongest cache-based baseline (Gigatoken) fully prewarmed. GPU full tokenization encodes a 1M-character request in 0.87 ms, up to 491x below HF and 23.4x below the fastest published CPU method. With vLLM, median time to first token drops 16-34% and P99 drops 23% under recorded bursts. Under a 50 ms P99 objective, four repair cores plus one GPU sustain 1,821 requests/s where a 16-core stateless front end saturates at 40.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。