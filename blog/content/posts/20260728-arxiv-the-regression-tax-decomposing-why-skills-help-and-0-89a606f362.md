---
title: "The Regression Tax: Decomposing Why Skills Help and Hurt LLM Agents"
date: 2026-07-28T06:21:35+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4262441d2854a27a6c353d7689de9a0ab6e3c768066834ff56487b0537c0e8bf"
source_payload_sha256: "sha256:2f09a6d9a6d21217714eee1fba634b24efd4605e1421fdd93030ce8a00c6d74c"
observation_id: obs_89a606f362d88b4ef4a58ce8ec053248c713232876515a3aadc034344301eb53
event_id: evt_fdb6f4aa5d5de1432f64ceba9160d54a1c2dba53e856424fd1c6799774340382
revision_id: rev_2c1859f10ae8802ea2f6aad62e1fcb924791fce68747989277dfa7147729931a
source_published_at: 2026-07-24T17:50:03Z
first_seen_at: 2026-07-27T22:37:14Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 67
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.22520v1
parent_observation_id: null
last_seen_at: 2026-07-27T22:20:40.219345Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.22520v1](http://arxiv.org/abs/2607.22520v1)

## 来源摘要/节选

> Adding procedural skills to an LLM agent is typically evaluated by average improvement in task success. However, this metric hides an important cost: skills can also make agents worse. We measure both sides by comparing agents with and without skills across nearly 6,000 runs spanning two office automation benchmarks and three model harness stacks. This allows us to distinguish two outcomes. A regression is a task solved without skills but failed after skills are added. A residual failure is a task that fails both with and without skills. We find that regressions are substantial enough that the best performing skills outperform others primarily by regressing less, not by gaining more. We identify three causes of regression: (i) skill description osmosis, a skill changes an agent's behavior simply by being present in context, even when it is never invoked; (ii) grounding displacement, a skill's prescribed procedure overrides how the agent interprets its inputs; and (iii) verification displacement, where the procedure suppresses checks the agent would otherwise perform on its outputs. Analysing persistent failures reveals the same underlying pattern. Existing skills overemphasize procedural guidance the stage least often responsible for failure while under supporting grounding and verification, the dominant sources of remaining errors. After correcting evaluation artifacts and studying traces, we find many regressions and persistent failures recoverable through better grounding and verification. Procedural skills should be evaluated by decomposing their net effect into gains and regressions, not by aggregate improvement alone. We identify three regression modes skills should avoid, and find that reliability depends more on grounding and verification than on procedural skill choice.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。