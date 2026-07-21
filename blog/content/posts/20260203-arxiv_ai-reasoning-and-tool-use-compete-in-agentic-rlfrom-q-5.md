---
title: Reasoning and Tool-use Compete in Agentic RL:From Quantifying Interference
  to Disentangled Tuning
date: 2026-02-03 03:49:30+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.00994v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:5c7220e01e844ec10387376afec1d370024d6ec77be95075aafa2352fe40390d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 97
captured_at: '2026-07-18T04:10:30.388786Z'
source_capture_sha256: sha256:242ae6837ea47dc6ea646a723fc0cf88b2f0f125170a7a660e9d9fa9f1a48c0a
source_capture_chars_original: 1377
source_publication_excerpt_chars: 1377
observation_id: obs_c2e40af0569a93ae6f81194d4dd9f4b595f6ad124398f061583e803589208a87
revision_id: rev_1df31ed890be05a6122394184b374f9de616b05a421cc286dda4055890116b46
event_id: evt_769460b0fc270b59f55cc49540d5d509aa7f0478e921ce2f510feb1a1838ae48
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-03T03:56:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.00994v1](<https://arxiv.org/abs/2602.00994v1>)
- **作者**: Yu Li, Mingyang Yi, Xiuyu Li, Ju Fan, Fuxin Jiang, Binbin Chen, Peng Li, Jie Song, Tieying Zhang
- **分类**: cs.AI
- **论文时间**: 2026-02-01T03:19:22Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.00994v1.pdf](<https://arxiv.org/pdf/2602.00994v1.pdf>)

## 来源摘要/节选

> Agentic Reinforcement Learning \(ARL\) focuses on training large language models \(LLMs\) to interleave reasoning with external tool execution to solve complex tasks. Most existing ARL methods train a single shared model parameters to support both reasoning and tool use behaviors, implicitly assuming that joint training leads to improved overall agent performance. Despite its widespread adoption, this assumption has rarely been examined empirically. In this paper, we systematically investigate this assumption by introducing a Linear Effect Attribution System\(LEAS\), which provides quantitative evidence of interference between reasoning and tool-use behaviors. Through an in-depth analysis, we show that these two capabilities often induce misaligned gradient directions, leading to training interference that undermines the effectiveness of joint optimization and challenges the prevailing ARL paradigm. To address this issue, we propose Disentangled Action Reasoning Tuning\(DART\), a simple and efficient framework that explicitly decouples parameter updates for reasoning and tool-use via separate low-rank adaptation modules. Experimental results show that DART consistently outperforms baseline methods with averaged 6.35 percent improvements and achieves performance comparable to multi-agent systems that explicitly separate tool-use and reasoning using a single model.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
