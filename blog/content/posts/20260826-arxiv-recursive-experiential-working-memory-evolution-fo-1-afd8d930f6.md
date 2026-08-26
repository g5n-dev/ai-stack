---
title: "Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses"
date: 2026-08-26T11:20:40+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:4dd08269612e3d9b18f01b3fd4bb08f2fb8af0d33d9386439029ab2ad0cbf965"
source_payload_sha256: "sha256:c07524754067877e97e9980b28da83897ad0087ec33531d2c843ef54f78b17f1"
observation_id: obs_afd8d930f6a32d8c64536719494d85fa50a33b327c75ed8dcaf1d4eb3ccf58f3
event_id: evt_03c891ed6d3715fd76de161325730f9b536d8e16434c12f67569c40fb2f951f3
revision_id: rev_132043cf6c679935f36d6977729d07a94b2381c659c38fcd23b122de75265ea4
source_published_at: 2026-08-25T17:56:35Z
first_seen_at: 2026-08-26T03:17:58.765806Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 80
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.24876v1
parent_observation_id: null
last_seen_at: 2026-08-26T03:17:58.765806Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.24876v1](http://arxiv.org/abs/2608.24876v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Zhaochen Yu、Yingcheng Wu、Zhenfei Yin 等

## 来源摘要/节选

> Recursive self-improvement (RSI) remains hard in long-horizon tasks, where growing histories obscure the task state and misalign skill invocation. We introduce Recuris, a recursive Experiential-Working Memory architecture for long-horizon agent harnesses, in which Working Memory tracks task progress and guides skill selection from Experiential Memory, grounding skill use in current needs rather than the full history. This coupling also turns execution into structured evidence that localizes failures to specific memory components. Across tasks, a fixed Meta-Agent turns that evidence into localized, validation-gated updates to Skill Memory that reshape execution and yield new evidence, forming a bounded recursive memory-evolution loop. Across four long-horizon benchmarks and ten models, Recuris improves task success in 35 of the 37 completed model-benchmark pairs, carrying frontier models to SOTA-level task success: on tau-bench it adds +17.8 points to GPT-5.6 Sol and +15.6 to Claude Opus 5, taking Opus 5 to 87.9%, and +16.6/+13.5 points on Qwen3.6-27B/35B on SkillFlow. The advantage widens as the interaction horizon grows, to +32.2 points on the longest tasks, and common long-horizon failures fall by up to 80%. These results position recursively evolving memory as a scalable foundation for RSI, enabling agents to continuously transform accumulated experience into increasingly effective long-horizon behavior. Code: https://github.com/Gen-Verse/Recuris

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。