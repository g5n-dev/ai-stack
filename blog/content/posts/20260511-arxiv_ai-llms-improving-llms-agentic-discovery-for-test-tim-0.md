---
title: 'LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling'
date: 2026-05-11 23:12:19+08:00
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
external_url: https://arxiv.org/abs/2605.08083v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:f7ae29848e69a4003f023ecfa52a4e7f9f753aada0501ba417e9d6276e72ad3c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 60
captured_at: '2026-07-18T04:29:31.582048Z'
source_capture_sha256: sha256:b05dfaf6505f4e2da7c95f42b0555a6df379d6eec758f6f9aa3b216646a02b45
source_capture_chars_original: 1584
source_publication_excerpt_chars: 1584
observation_id: obs_17d9b49d18b9c6a58ee5b45a261d70f08ffc1b055ea46252a91308f7e98cf5dc
revision_id: rev_c215ac64908f671db947450b648a9c3353a638d7dccaa597de130f9fb033401b
event_id: evt_e72e72b745ca2f1b3183839967b0b6af03c6c8d03356418d5c8aff6f8fdef6ba
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-05-11T04:31:48Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2605.08083v1](<https://arxiv.org/abs/2605.08083v1>)
- **作者**: Tong Zheng, Haolin Liu, Chengsong Huang, Huiwen Bao, Sheng Zhang, Rui Liu, Runpeng Dai, Ruibo Chen, Chenxi Liu, Tianyi Xiong, Xidong Wu, Hongming Zhang, Heng Huang
- **分类**: cs.CL
- **论文时间**: 2026-05-08T17:59:40Z
- **论文 PDF**: [https://arxiv.org/pdf/2605.08083v1.pdf](<https://arxiv.org/pdf/2605.08083v1.pdf>)

## 来源摘要/节选

> Test-time scaling \(TTS\) has become an effective approach for improving large language model performance by allocating additional computation during inference. However, existing TTS strategies are largely hand-crafted: researchers manually design reasoning patterns and tune heuristics by intuition, leaving much of the computation-allocation space unexplored. We propose an environment-driven framework, AutoTTS, that changes what researchers design: from individual TTS heuristics to environments where TTS strategies can be discovered automatically. The key to AutoTTS lies in environment construction: the discovery environment must make the control space tractable and provide cheap, frequent feedback for TTS search. As a concrete instantiation, we formulate width--depth TTS as controller synthesis over pre-collected reasoning trajectories and probe signals, where controllers decide when to branch, continue, probe, prune, or stop and can be evaluated cheaply without repeated LLM calls. We further introduce beta parameterization to make the search tractable and fine-grained execution trace feedback to improve discovery efficiency by helping the agent diagnose why a TTS program fails. Experiments on mathematical reasoning benchmarks show that the discovered strategies improve the overall accuracy--cost tradeoff over strong manually designed baselines. The discovered strategies generalize to held-out benchmarks and model scales, while the entire discovery costs only $39.9 and 160 minutes. Our data, and code will be open-source at https://github.com/zhengkid/AutoTTS.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
