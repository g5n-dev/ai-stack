---
title: "The Bitter Lesson of Tool Calling"
date: 2026-08-07T13:06:47+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:cb2fd93c67a09507c031af885499d471ed0041cb187829fe501dcc145acb695e"
source_payload_sha256: "sha256:18204ecbcb1583082268f2b7bd44661c6ce19c3feed9f5fd90b2b03aeb214acd"
observation_id: obs_2caabefc0ab852d670c8512d5803b347e08e2e32ea439a0382f81cf80cf4d7d1
event_id: evt_b3b5980296f8bdb6d19a6d521bd1a161f18bd2f64de9d7ded8360f358cec9e7b
revision_id: rev_1c546c92061b5496d0871a60230df0995bff6681f9e8153ff72c82c725864820
source_published_at: 2026-08-06T17:58:32Z
first_seen_at: 2026-08-07T05:03:51.551910Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 33
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.06370v1
parent_observation_id: null
last_seen_at: 2026-08-07T05:03:51.551910Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.06370v1](http://arxiv.org/abs/2608.06370v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Ishan Patel、Sahil Sen、Elias Lumer 等

## 来源摘要/节选

> Tool use transforms LLMs into agents that act beyond their training data, and for code-capable models, programmatic tool calling extends this further by replacing rigid JSON calls with scripts that chain and parallelize naturally. However, a systematic evaluation of tools as code on an established benchmark across current and prior model generations under real-world task conditions has not been conducted. In this work, we empirically compare programmatic tool calling (PTC) to native JSON tool calling across 14 language models on BFCL v4. In the programmatic tool calling paradigm, tools are exposed as typed Python stubs that the model invokes through code, with execution and results handled in a single agent turn. Programmatic tool calling matches or exceeds native JSON tool calling in 11 of 14 models on BFCL v4, with the GPT-5.6 family achieving a 10.6% improvement over the JSON tool calling baseline. Further, it matches or outperforms baseline in 13 of 14 models under parallel fan-out, and holds stable under context rot conditions where baseline degrades 2.3% on average. Our results demonstrate that programmatic tool calling is a viable and robust alternative to JSON tool calling, with performance tracking model capability across release generations.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。