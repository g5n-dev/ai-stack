---
title: "EarthVerse: Benchmarking Scientific Agents Across Dynamic Earth Systems and Natural Hazards"
date: 2026-08-26T01:47:33+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:90b6eb11a9cf4bf38d6d3e03f86492c4331929459d0e50ab8c9ba11ef9b66c23"
source_payload_sha256: "sha256:c6e871e61e2355546ed170feeb4e0ce115c3e88092f74e2e7c22ae3304ff4f7f"
observation_id: obs_cdd28ace3e9e57e884b198c23b78e7800bae3fcbfe0d4b4fcfeb02590d03ec26
event_id: evt_05e265863c81ad9532c638eb9eefb8ad9a990e858e2cc691b00fa687d38451cb
revision_id: rev_9b52ca3dcadca90b31dfd47f7d52daa4b403a080e8fc8e8afe94b073f536af8e
source_published_at: 2026-08-24T17:29:16Z
first_seen_at: 2026-08-25T17:45:45.167613Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 91
interpretation_sha256: "sha256:6fcde2788caa2f044fe6cc7a79adc2ef09bb1993855f70af22fec6205aae827d"
description: "EarthVerse 是一套用于评估科学智能体在动态地球系统及自然灾害任务中表现的基准，涵盖基于真实事件的数百个可复现工作单元，要求智能体检查异构证据、执行透明计算并保留答案的溯源信息。"
external_url: http://arxiv.org/abs/2608.23525v1
parent_observation_id: null
last_seen_at: 2026-08-25T17:45:45.167613Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.23525v1](http://arxiv.org/abs/2608.23525v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Zhiqing Cui、Xinxiang Yin、Yihong Tang 等

## 要点解读

### 这是什么  
EarthVerse 是一套用于评估科学智能体在动态地球系统及自然灾害任务中表现的基准，涵盖基于真实事件的数百个可复现工作单元，要求智能体检查异构证据、执行透明计算并保留答案的溯源信息。

### 用在哪里  
适用于需要检验多步骤科学推理、证据选取与数值一致性的自动化分析系统研发；也可为相关课程、竞赛或平台提供统一的性能衡量标准。

### 可以推断的  
推测：随着任务规模和事件种类的扩大，该基准能够更细致地定位智能体在跨尺度、跨模态推理过程中的薄弱环节。  
推测：最高平均准确率与严格评估指标的显著差距表明，提升长链推理的一致性是当前技术的主要瓶颈。

## 来源摘要/节选

> Earth-system analysis reconstructs changing physical processes from observations that differ in source, scale, timing, and modality. Natural hazards make this work consequential because incomplete evidence can change estimates of severity, exposure, and mechanism. We introduce EarthVerse, a benchmark that evaluates scientific agents through package-scoped investigations. Its 405 reproducible tasks are grounded in 199 documented events and 19 hazard families. Agents inspect heterogeneous event packages, choose compatible evidence, execute transparent calculations, reconcile source differences, and preserve provenance in the final answer. We provide executable ground truth that decomposes each task into fine-grained answer units, together with task-specific rubrics that assess the supporting research process while allowing multiple valid paths. We evaluate 25 model and agent systems under a controlled tool-using protocol, then use controlled studies to locate failures in evidence access, tool selection, memory, reasoning, interaction, and scientific execution. Across systems, the best mean answer-unit accuracy is 84.65%, while the highest Strict@95 is only 34.81%. The gap shows that current agents often complete individual steps without maintaining a consistent chain across evidence, scales, units, calculations, and physical interpretation. EarthVerse provides a reproducible basis for measuring end-to-end scientific reliability in dynamic Earth systems.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。