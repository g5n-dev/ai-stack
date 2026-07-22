---
title: "SWE-Pruner Pro: The Coder LLM Already Knows What to Prune"
date: 2026-07-21T14:53:17+08:00
draft: false
entry_kind: "auto"
tags: ["cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:efe07b934b81ee54601beda171f377d39a61fc8eb63acd8f357185d81774d943"
source_payload_sha256: "sha256:23b4b9233e4c6197a14fce752109334db0b19015c157dcc90a2b0d04c772013c"
observation_id: obs_839c437bacc17af424d7d647feca8d6e7bf6245da0042c232cbc28f63643b6d4
event_id: evt_4f63d49d2c76c02ef798c998548ea5d9bd6c1df7a6c04a8fb11a5dd95ce6abaf
revision_id: rev_a178f085e84a8b5de2aeb6f39f041af4a77556c4cc7561fb31e82eac27a569b7
source_published_at: 2026-07-20T17:47:44Z
first_seen_at: 2026-07-21T07:08:47Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.18213v1
parent_observation_id: null
last_seen_at: 2026-07-22T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.18213v1](http://arxiv.org/abs/2607.18213v1)

## 来源摘要/节选

> Pruning long context for coding agents has been a vital technology for efficient context management. While existing context pruning methods such as SWE-Pruner realize this by attaching a separate code classifier, we find the agent itself encodes internal representations indicating the relevance of code context when reading tool output. Based on this finding, we propose SWE-Pruner Pro, which prunes tool outputs directly inside the agent. Concretely, a small head turns the agent's own internal representations into a keep-or-prune label for each line, with a length-aware embedding keyed to each tool output's line count. Across two open-weight backbones and four multi-turn benchmarks, SWE-Pruner Pro saves up to 39% of prompt and completion tokens while preserving task quality, with bounded inference overhead. Notably, on MiMo-V2-Flash SWE-Pruner Pro additionally raises the SWE-Bench Verified resolve rate by +3.8% and the long-context Oolong accuracy by +2.2 points.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。