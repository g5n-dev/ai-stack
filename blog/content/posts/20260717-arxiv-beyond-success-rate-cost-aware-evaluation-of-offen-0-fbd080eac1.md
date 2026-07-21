---
title: "Beyond Success Rate: Cost-Aware Evaluation of Offensive and Defensive Security Agents"
date: 2026-07-17T17:24:29+08:00
draft: false
entry_kind: "auto"
tags: ["cs.CR", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9358cd28add3e790392f133c74491517a7a1859afbc82a7a304241e93747b9e2"
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 85
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.15263v1
observation_id: obs_fbd080eac1a37bfb51c1a3ec6eec08b3d743c55676f49e859c11d41d73d95e40
revision_id: rev_1e1196f002292f0354aeeef95ac08bc18402330dc002338162a5df13aed5aeac
event_id: evt_1e786576b391cab9430e811ac7a6c4e9a8b19afd6434245506be3db4e9c1f5b1
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-17T09:26:33Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.15263v1](http://arxiv.org/abs/2607.15263v1)

## 来源摘要/节选

> Security-agent evaluations commonly measure peak offensive capability under generous inference budgets, emphasizing vulnerability discovery, exploit development, penetration testing, and CTF completion. Such measurements are useful but incomplete: in operational security, every reasoning step, tool call, telemetry query, and enrichment request consumes budget. We evaluate language-model security agents through this cost-success lens on offensive Cybench challenges and defensive Splunk BOTS v1 investigation challenges. Instead of reporting only best-case success, we compare models at fixed cost levels and decompose performance by inference spend and tool spend. Our results show distinct scalingregimes for red- and blue-team tasks. Offensive CTF performance improves with additional test-time compute, and scaled open-weight models can approach frontier proprietary systems while remaining cost-competitive. Defensive SOC investigation does not scale in the same way: success depends more heavily on disciplined tool use, telemetry navigation, and selective enrichment than on raw reasoning budget alone. We argue that security-agent benchmarks should measure economic efficiency and operational fit alongside task success. Cost-aware, SOC-native evaluations provide a clearer picture of which models are practically useful today and where defensive agents still need to improve. We present an interactive website with our results https://evals.frontier.security.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。