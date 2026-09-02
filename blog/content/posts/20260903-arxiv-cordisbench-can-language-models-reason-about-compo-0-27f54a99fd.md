---
title: "CordisBench: Can Language Models Reason About Component Lifecycles in Dynamic Agent Harnesses?"
date: 2026-09-03T02:45:09+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:31fe50dd9b7fa3c7c595821bcb98745d52c7276f73a4ac089f629919391523b9"
source_payload_sha256: "sha256:9e18426ba275a7b0648255debd38f1237ff382930d04f8c1d9d588c4ed43a50b"
observation_id: obs_27f54a99fd45b38cc82085451746397413ac3a370f810fc1102e51d8e2737721
event_id: evt_9c85f0b53aabf15bb55dee559461106ac27aa162a7af13eda64091addbb6c5ce
revision_id: rev_e6690b87ab4fa530368ddba58fb4511f878e7ca815b0486d832ccfc698701c4f
source_published_at: 2026-09-01T17:59:13Z
first_seen_at: 2026-09-02T18:41:59.665028Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 94
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.01600v1
parent_observation_id: null
last_seen_at: 2026-09-02T18:41:59.665028Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.01600v1](http://arxiv.org/abs/2609.01600v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Damien Sileo、Dimitri Kachler

## 来源摘要/节选

> Dynamic agent harnesses let language models change the software that shapes their own execution. This flexibility brings a new reasoning burden: a local plugin change can propagate through dependencies and cleanup. We introduce CordisBench, a 1,200-question benchmark of this lifecycle reasoning. It combines a controlled formal setting with programs executed against Cordis, a runtime that manages component dependencies and cleanup, and asks models to identify affected components, predict state after a specified teardown order, determine which conditions hold under all or some orders, and choose reconfigurations that succeed when executed. Across these tasks, we evaluate three efficiency-oriented models at low reasoning effort with 2, 4, 8, 16, 24, or 32 relevant interactions, using deterministic task-specific scoring. Models usually handle small systems well but grow less reliable as more interactions become relevant, especially when predicting final state and when reasoning across teardown orders. Additional inference effort recovers marked gains for some models. The cost is nontrivial: on our 16-interaction subset, GPT-5.6 Luna uses nearly 3,000 reasoning tokens per question at medium effort. For these controlled instances, that cost is avoidable: an independent finite reference semantics agrees with Cordis execution on every observation and action outcome used for scoring across all 528 executable questions.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。