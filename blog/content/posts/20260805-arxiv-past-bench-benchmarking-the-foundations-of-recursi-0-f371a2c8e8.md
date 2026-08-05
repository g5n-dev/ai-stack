---
title: "PAST-Bench: Benchmarking the Foundations of Recursive Self-Improvement in Personal Agents"
date: 2026-08-05T22:37:43+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:47e8e46f7adf24ae9bcaa65024fee6235421572237d5c3fc5a01aa33b088dbff"
source_payload_sha256: "sha256:78d12470d6790bea858cde0fc8880adc71163ffefe68fd57b336fba7c15d049e"
observation_id: obs_f371a2c8e8c2ef5589b2ae0becc07464666cce9ceb29c96f82428838e535966b
event_id: evt_2763a70829a94896bf9a35d0b7fde2e7648fa479dd208c491860992aa74d251f
revision_id: rev_3f05795224eb23cb926cd1fc350bda4974dac3bb969688bbc3aa40fbdd4f0932
source_published_at: 2026-08-04T17:58:05Z
first_seen_at: 2026-08-05T14:47:06Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.04003v1
parent_observation_id: null
last_seen_at: 2026-08-05T14:35:25.725558Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.04003v1](http://arxiv.org/abs/2608.04003v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Shuhan Xue、Zixin Ding、Yichen Shen 等

## 来源摘要/节选

> Recursive self-improvement requires agents to turn accumulated experience into better future behavior. Personal AI agents offer a concrete setting for studying this capability because they retain preferences, task histories, tool routines, and learned skills across sessions. Yet whether retained experience actually improves them over time has not been systematically tested. We introduce PAST-Bench, a benchmark designed to isolate this question. Each agent runs through ordered sequences of fresh-session tasks under matched conditions that turn retained experience on and off. It spans 26 scenarios and 204 episodes across memory, procedural reuse, information gathering, and update. We report both later-task gains and whether those gains follow the intended save, retrieve, and update pathway. Across seven base models and four agent frameworks, improvement is real but uneven across capabilities. Agents with the same headline gain can differ markedly in whether that gain is supported by evidence of the intended pathway. Guided by these findings, we develop Hermes+, which extends Hermes with five targeted interventions across stages of the agent loop. Hermes+ raises the average gain from retained experience and provides clearer pathway evidence, with its strongest improvement on tasks requiring outdated state to be replaced, although the effect remains capability- and model-dependent. Together, PAST-Bench and Hermes+ provide an evaluation and diagnostic foundation for studying how persistent agents can progress from retaining experience to systematically improving through it. Code: https://github.com/Gen-Verse/PAST-Bench

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。