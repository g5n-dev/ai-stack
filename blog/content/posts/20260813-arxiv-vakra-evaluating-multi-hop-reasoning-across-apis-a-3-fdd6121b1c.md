---
title: "VAKRA: Evaluating Multi-Hop Reasoning Across APIs and Retrieval Under Tool-Use Policies"
date: 2026-08-13T21:48:18+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:46b56802fe626b113ad300513678d1d38e91bcce50c89aaa2e6525661920ca86"
source_payload_sha256: "sha256:c82174db4c53cb262c58c07bd4e9e34b6fec1fba61a058077511fbe1320159cb"
observation_id: obs_fdd6121b1c5df0b7e2dfab63ee16ce671c78f0c1818f2e3fd0a3b1d671a95a6f
event_id: evt_1e724eed81adc0853af2a6fb872f8927ba4c8d82fb2bb0f8b1c8e9ca26baf68c
revision_id: rev_db0cc9802395aee35bd1c3e533d6ddd326379807a92cd835a97d38637ae3fd36
source_published_at: 2026-08-12T17:27:27Z
first_seen_at: 2026-08-13T13:46:35.356907Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 87
interpretation_sha256: "sha256:b6742e05f2d1dc3037e4d39326e3f5b580d16f01b2790e8faf92ab326a6046fd"
description: "该内容提出一套评估框架，用来衡量智能体在同时访问大量可执行 API 与文档集合时的多跳推理能力。框架定义了三种难度递增的场景，并通过在实际接口上重新执行模型生成的工具调用来验证答案的正确性。"
external_url: http://arxiv.org/abs/2608.12282v1
parent_observation_id: null
last_seen_at: 2026-08-13T13:46:35.356907Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12282v1](http://arxiv.org/abs/2608.12282v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Ankita Rajaram Naik、Anupama Murthi、Benjamin Elder 等

## 要点解读

### 这是什么
该内容提出一套评估框架，用来衡量智能体在同时访问大量可执行 API 与文档集合时的多跳推理能力。框架定义了三种难度递增的场景，并通过在实际接口上重新执行模型生成的工具调用来验证答案的正确性。

### 用在哪里
适用于需要将语言模型嵌入企业级业务流程的研发团队，也适合学术界对比不同模型在组合式 API 调用和策略约束下的表现。

### 可以推断的
推测：在真实业务中，模型若只能在单一步骤完成接口调用，往往不足以支撑需要跨多个系统协作的复杂任务。  
推测：提升模型在语言层面的实体消解和跨来源信息对齐能力，可能是突破当前性能瓶颈的关键方向。

## 来源摘要/节选

> Agents deployed in enterprise settings must reason across structured APIs and document collections, yet existing benchmarks evaluate these capabilities in isolation. We introduce VAKRA (e\textbf{V}aluating \textbf{A}PI and \textbf{K}nowledge \textbf{R}etrieval \textbf{A}gents), a benchmark of over $8{,}000$ executable APIs across $62$ domains with tasks spanning three settings of increasing difficulty: diverse API interaction styles, multi-hop reasoning over structured APIs, and multi-source reasoning with natural-language tool-use policy constraints. Correctness is verified by re-executing predicted tool calls against live APIs, accommodating multiple valid paths. Using a fixed ReAct harness to isolate model capabilities from agent architecture, we evaluate frontier and open-weight models and find that even the best model achieves only 70.4\% on single-hop endpoint-style tasks and drops to 50--51\% on compositional APIs; performance degrades by over 50\% as reasoning depth increases, and policy-constrained questions expose severe failures (as low as 2.4\% on unanswerable queries). Trace analysis shows failures concentrate at language-mediated reasoning - entity disambiguation, cross-source grounding, rather than tool invocation mechanics. Code is available https://github.com/IBM/VAKRA. Dataset is available https://huggingface.co/datasets/ibm-research/VAKRA

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。