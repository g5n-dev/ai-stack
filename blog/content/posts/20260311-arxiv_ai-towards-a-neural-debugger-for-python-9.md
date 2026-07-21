---
title: Towards a Neural Debugger for Python
date: 2026-03-11 22:41:14+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
- AI Agent
- 大语言模型
- Python
categories:
- 论文
- 大模型
scenarios:
- AI/ML项目
- 大语言模型
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.09951v1
aliases:
- /posts/20260312-arxiv_ai-towards-a-neural-debugger-for-python-9/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2528d3fc8eb5635951c69b69046ce69829e0ecabac6665ac2cd62ca3085a7853
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 36
captured_at: '2026-07-18T04:27:47.713351Z'
source_capture_sha256: sha256:42623469e3fd7037b1829da305a2d663fecdc3e77db1fe7984a553f99eb3546b
source_capture_chars_original: 1583
source_publication_excerpt_chars: 1583
observation_id: obs_bfedf7dce1de73d9ca16b1d9b60a9182f63a109085dcfe81ed7f42afaa63335c
revision_id: rev_33ccceecd960f9c2c1f67551c36e483131b29cef2209e76f6b7fddd2a289481a
event_id: evt_bbbdd8415164dd3bb952145007f47fcb11b9ddfbef6fa4bfc690f95a25b80ba4
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-11T04:17:05Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.09951v1](<https://arxiv.org/abs/2603.09951v1>)
- **作者**: Maximilian Beck, Jonas Gehring, Jannik Kossen, Gabriel Synnaeve
- **分类**: cs.LG
- **论文时间**: 2026-03-10T17:47:05Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.09951v1.pdf](<https://arxiv.org/pdf/2603.09951v1.pdf>)

## 来源摘要/节选

> Training large language models \(LLMs\) on Python execution traces grounds them in code execution and enables the line-by-line execution prediction of whole Python programs, effectively turning them into neural interpreters \(FAIR CodeGen Team et al., 2025\). However, developers rarely execute programs step by step; instead, they use debuggers to stop execution at certain breakpoints and step through relevant portions only while inspecting or modifying program variables. Existing neural interpreter approaches lack such interactive control. To address this limitation, we introduce neural debuggers: language models that emulate traditional debuggers, supporting operations such as stepping into, over, or out of functions, as well as setting breakpoints at specific source lines. We show that neural debuggers -- obtained via fine-tuning large LLMs or pre-training smaller models from scratch -- can reliably model both forward execution \(predicting future states and outputs\) and inverse execution \(inferring prior states or inputs\) conditioned on debugger actions. Evaluated on CruxEval, our models achieve strong performance on both output and input prediction tasks, demonstrating robust conditional execution modeling. Our work takes first steps towards future agentic coding systems in which neural debuggers serve as a world model for simulated debugging environments, providing execution feedback or enabling agents to interact with real debugging tools. This capability lays the foundation for more powerful code generation, program understanding, and automated debugging.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
