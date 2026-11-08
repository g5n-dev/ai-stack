---
title: "XStack: A Benchmark for ML Repo Migration"
date: 2026-11-07T08:56:25+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "机器学习", "cs.LG", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:387005c31008b4f68bf587f9e51b19553e97add102be57ac4998651ca523fb82"
source_payload_sha256: "sha256:c29bad986d21050d0f5a6f9f5dd6a69d7e837dc99b6f32fe335e487ae16fbb87"
observation_id: obs_c506adad28825d2b4f3de3c5e292070bbd219fb1a6fa5dc04956dc9de5be67a4
event_id: evt_88a612f2b9d9e09fe85c32779b74d6a4a0ca737140afc675eb60eac1496e994b
revision_id: rev_1fe9d1b79f936eeb0fd9991aa1675551483da1a311df421a210b0114b139020c
source_published_at: 2026-11-05T18:55:54Z
first_seen_at: 2026-11-07T01:07:28Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 41
interpretation_sha256: "sha256:6f791c33ee37f16b5418f5ac3e35d94858e68a51fa3a4c24079066f35666ca28"
description: "XStack 是一个用于评估 AI 代理跨框架、跨硬件迁移机器学习代码仓库的基准。代理需要把 PyTorch 仓库迁移为可在 TPU 上运行的 JAX 仓库，并通过基于原仓库结果的校准评分。"
external_url: http://arxiv.org/abs/2611.08472v1
parent_observation_id: null
last_seen_at: 2026-11-08T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2611.08472v1](http://arxiv.org/abs/2611.08472v1)
- **发布域名**: arxiv.org
- **分类**: cs.LG
- **作者**: Linrong Cai、Taiming Lu、Haozhe Chen 等

## 要点解读

### 这是什么
XStack 是一个用于评估 AI 代理跨框架、跨硬件迁移机器学习代码仓库的基准。代理需要把 PyTorch 仓库迁移为可在 TPU 上运行的 JAX 仓库，并通过基于原仓库结果的校准评分。

### 用在哪里
它适用于评估 AI 代理执行完整软件迁移任务的能力，也适合研究如何提升机器学习代码在不同硬件生态之间的可移植性。研究人员可借此比较代理在长期、多步骤迁移任务中的可靠性。

### 可以推断的
- 推测：这类基准不仅考察代码改写，还涉及构建、测试和硬件适配等环节，因此比单一函数级任务更能反映代理的综合工程能力。
- 推测：能够在干净 TPU 环境中完成迁移并满足校准结果的代理，可能具备较强的跨生态协作与问题排查能力。

## 来源摘要/节选

> ML code should run where researchers choose, not where it was first written. Today, machine learning code mainly lives in two ecosystems, PyTorch on NVIDIA GPUs and JAX on Google TPUs. Migrating repositories between them means building and testing across frameworks and hardware. This migration is (1) a practical need, since it unlocks different hardware for researchers, and (2) a natural benchmark: it involves different frameworks and hardware, covers whole repositories, and is long-horizon and challenging. We introduce XStack, a benchmark that evaluates agents on migrating ML repositories between these two ecosystems. Each agent receives a PyTorch repository and a clean TPU machine and must deliver a JAX repository. Its output passes if it meets our grading criteria, based on the source repository's published result, authenticated and calibrated by us. Migration by agents remains unreliable: Claude Opus 5 passes 75%, GPT-5.6-sol 45%, and every other agent at most 40%. XStack is a step toward freeing ML code from its ecosystem. We release XStack to make progress toward reliable migration across frameworks and hardware measurable.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。