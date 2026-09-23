---
title: "CliffCompaction: Cost-Efficient Compaction for Long-Horizon Coding Agents"
date: 2026-09-24T04:23:48+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:eb8baa7290563c7e062ae0f8f0a414454e949f38eddb73119b95bf77a87445fa"
source_payload_sha256: "sha256:487d917387f8b4317b8bb634fd82fd755a7ea4ab06406394a2a6a3e99c1b1f50"
observation_id: obs_f20fc2a20e714d36bf2e1ba03d420e0a94acf7058a14908b3d61b4564cdca8ce
event_id: evt_55a64230f4751921a419b3c552a933cbd29ea47eeb32e17c442c1226ad092fbe
revision_id: rev_f2b35ffa833558bbd46ba74e9f23d0e67769e0f1ebba3522bd8235ee7820e12c
source_published_at: 2026-09-22T17:55:59Z
first_seen_at: 2026-09-23T20:21:16.411014Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:0ed80cc53ca237750479f4b36b63db77714f7427461ea742a7dcbef9547219d1"
description: "CliffCompaction 是一种自动压缩技术，用于在保持或提升任务表现的同时，降低处理大规模上下文时的成本。它仅通过截断或丢弃原始内容实现压缩，避免重新表述导致的信息漂移。"
external_url: http://arxiv.org/abs/2609.26779v1
parent_observation_id: null
last_seen_at: 2026-09-23T20:21:16.411014Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.26779v1](http://arxiv.org/abs/2609.26779v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Trang Nguyen、Eulrang Cho、Bingqing Chen 等

## 要点解读

### 这是什么
CliffCompaction 是一种自动压缩技术，用于在保持或提升任务表现的同时，降低处理大规模上下文时的成本。它仅通过截断或丢弃原始内容实现压缩，避免重新表述导致的信息漂移。

### 用在哪里
适用于需要在受限上下文窗口内跨多个会话处理上百万 token 的编码任务，如代码生成、调试和基准评估。对关注推理成本和效率的开发者或研究人员尤为有用。

### 可以推断的
- 推测：在成本受限的环境中，这种压缩方式可以让同等性能的系统以更少的调用次数运行，从而实现费用削减。  
- 推测：因为只删除或截断信息而不重新生成文本，CliffCompaction 可能对需要完整保留上下文的场景有一定局限性。

## 来源摘要/节选

> Agents often work on complex problems that require millions of tokens of context, which necessitates compacting across sessions due to limited context windows. We develop CliffCompaction, an autocompaction technique that reduces cost by up to 50% under a bounded context while maintaining or improving performance on Terminal-Bench and achieving new levels of efficiency for test-time scaling and state-of-the-art results on KernelBench. The per-rollout savings of CliffCompaction make the performance--cost trade-off of test-time scaling more efficient, adding over 10 percentage points on Terminal-Bench for less than the cost of two full-context runs. Under parallel test-time scaling, CliffCompaction lets Kimi K2.6 match Opus 4.7, and exceed Opus 4.6 and GPT-5.3 Codex at lower cost. The key to CliffCompaction's effectiveness is that it keeps compacted information faithful by only truncating or dropping content, never rephrasing or rewriting it. We never compact a compaction---each pass operates only on original content, and prior compacted output is discarded, preventing context drift from accumulating. These properties sustain continual learning over sessions exceeding a million tokens: on KernelBench, CliffCompaction reaches CUDA kernel speedups of $2.23\times$ after 200 steps and $3.58\times$ after 400 steps, surpassing specialized search algorithms and trained agents despite being a general-purpose compaction technique. We open-source a scaffold-agnostic API-proxy implementation of CliffCompaction usable with Claude Code, Codex and other harnesses.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。