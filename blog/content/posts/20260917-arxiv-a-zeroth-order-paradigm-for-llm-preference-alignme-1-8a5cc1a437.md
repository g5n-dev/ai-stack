---
title: "A Zeroth-Order Paradigm for LLM Preference Alignment"
date: 2026-09-17T15:42:28+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.CL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:039fcd63eb24df5dd967fd232b3152bb34c5d7ee095a3c2b5c11af86f73ed00a"
source_payload_sha256: "sha256:034f9ec24e3786609f2113b0b01129d45e174b0985140359a475f689dda7c122"
observation_id: obs_8a5cc1a4379e4f4d97a396edb5360cebb84c5be4b74a3b6e5ae17cf848875f90
event_id: evt_57159e44b1e063c137c6507565359eceb16f759445bee4cbe75cd2228f06849c
revision_id: rev_9eb4ac1dffcbe5c2661eebbc867a6086321fefbce8797a24922e183236bdaad4
source_published_at: 2026-09-16T17:59:35Z
first_seen_at: 2026-09-17T07:53:07Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 52
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.19144v1
parent_observation_id: null
last_seen_at: 2026-09-17T07:38:42.193973Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.19144v1](http://arxiv.org/abs/2609.19144v1)
- **发布域名**: arxiv.org
- **分类**: cs.CL
- **作者**: Peter Chen、Xi Chen、Wotao Yin 等

## 来源摘要/节选

> Direct preference alignment methods are widely used to align large language models (LLMs) with human preferences because of their computational and memory efficiency. However, likelihood displacement motivates alternative ways to extract information from preference pairs with small likelihood margins. In this paper, we propose and analyze Comparison-based Preference Optimization (ComPO), a zeroth-order alignment method based on comparison oracles. ComPO extracts directional information from these pairs without directly optimizing a differentiable preference loss on them. We establish a convergence guarantee for its basic offline scheme under smoothness, gradient sparsity, and compatibility between the oracle and a latent objective. We further introduce online ComPO, which retains the offline comparison mechanism and uses unlabeled policy generations for reverse-KL control relative to a reference policy. Following the coverage perspective of preference fine-tuning, we establish a performance guarantee for a basic constrained scheme under local coverage and in-distribution pairwise reward accuracy. Experiments on Mistral, Llama, Gemma-2, Qwen3, and Gemma-3 models demonstrate improvements over existing direct alignment methods, including length-controlled win rates, with pair-level diagnostics providing evidence consistent with mitigating likelihood displacement.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。