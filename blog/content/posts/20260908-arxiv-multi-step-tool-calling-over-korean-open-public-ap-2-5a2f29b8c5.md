---
title: "Multi-Step Tool-Calling over Korean Open Public APIs: A Benchmark and a Data-Synthesis Recipe"
date: 2026-09-08T23:12:37+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:626cdfb82dd3893a8643d50bdafbdc035d807a08b74e1f20c4d036c69d9952f7"
source_payload_sha256: "sha256:5527d6dc3ee2a595a56cfe2ef3373c411f34dd17e8841fe6406395d3298de52f"
observation_id: obs_5a2f29b8c5a1e48bda97c5737b24797e1ccf1253cd33f36fb10fc94edbdd339a
event_id: evt_6b4653457440290744510a28489fccdd6d957499bb5e3be21c7db7d355e46f70
revision_id: rev_4687084e9f73ea6ca20de7599d8a982cb076d940ef5bc42c5d8ec5b745ad87d2
source_published_at: 2026-09-04T17:44:52Z
first_seen_at: 2026-09-08T15:24:02Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
interpretation_sha256: "sha256:61f3ff1ff6f0994a98dc77f2822c1d5218fc4fafdf021c5ab8b791afa71065a3"
description: "该条目介绍了一个针对韩国公开公共API的多步骤工具调用评测基准，并提出一种基于实时执行验证的图结构数据合成方法，用于生成可执行的多步骤轨迹，以提升开源模型的调用能力。"
external_url: http://arxiv.org/abs/2609.05395v1
parent_observation_id: null
last_seen_at: 2026-09-09T00:00:00Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.05395v1](http://arxiv.org/abs/2609.05395v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Dain Kim、Eungi Cho、Kyumin Kim 等

## 要点解读

### 这是什么
该条目介绍了一个针对韩国公开公共API的多步骤工具调用评测基准，并提出一种基于实时执行验证的图结构数据合成方法，用于生成可执行的多步骤轨迹，以提升开源模型的调用能力。

### 用在哪里
适用于需要在本地部署开源大模型来处理政府公共服务接口的场景，以及研究多步骤工具调用和benchmark设计的科研人员。

### 可以推断的
推测：该合成方法的核心思路可能对其他语言的公共API工具调用任务具有借鉴意义。  
推测：基于真实API执行验证的轨迹生成方式，有望提高训练数据的可靠性，从而帮助模型在实际任务中表现更佳。

## 来源摘要/节选

> Data-sovereignty regulations increasingly require public institutions to deploy open-source, on-premise LLM agents that chain multiple tool-calls across live government APIs. However, open-source models consistently underperform in this multi-step setting, and no existing benchmark measures the gap. We introduce the Korean Open Public API Benchmark (KOPA-Bench), comprising 145 real-world tasks. To close this gap, we present EDGE, an Execution-grounded Dynamic Graph for tool-calling data synthEsis driven by live execution. EDGE builds a graph of how each tool's output can feed another's input, keeps only the links that succeed when actually called against the live APIs, and traverses these verified links to synthesize executable multi-step trajectories. Fine-tuned via GRPO on the resulting dataset, our 9B model nearly matches the untuned 27B model from the same family, improving substantially not only on KOPA-Bench but also on the BFCL benchmark.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。