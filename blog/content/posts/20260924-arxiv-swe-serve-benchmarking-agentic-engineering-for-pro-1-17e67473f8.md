---
title: "SWE-Serve: Benchmarking Agentic Engineering For Production Inference Serving"
date: 2026-09-24T07:43:18+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "cs.AI", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:0de0aeac37bd0ff24eea198a1ff3bd882bcab7feeb0fe2f2c53237b46045b5d6"
source_payload_sha256: "sha256:ed466fd0ba07c5baab63986dbaacc647fa62acf724e059401c9a4fc0ee9f1598"
observation_id: obs_17e67473f8c2a2f660f9595f645354fa1b3be93c44345bf6a802ffe431815222
event_id: evt_616445aec390ab695111862a3eff145d1b8d238aa012eabde1e457e1da86b751
revision_id: rev_8b0b0139dbaf57e5e7f240b5f7e6fcfe6001369f13a0e75d32908037eba55126
source_published_at: 2026-09-22T17:54:59Z
first_seen_at: 2026-09-23T23:41:47.575977Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.26777v1
parent_observation_id: null
last_seen_at: 2026-09-23T23:41:47.575977Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.26777v1](http://arxiv.org/abs/2609.26777v1)
- **发布域名**: arxiv.org
- **分类**: cs.AI
- **作者**: Jennifer Williams、Dave Farris、Jeff Farris 等

## 来源摘要/节选

> We introduce SWE-Serve, a benchmark for evaluating agents on production inference engineering tasks. Implementing an inference feature can require coordinating multiple changes across the serving stack, including model support, runtime execution, and public APIs. Existing benchmarks provide limited coverage of production inference engineering: repository-level software engineering benchmarks do not target inference, while general terminal-agent benchmarks include only a few inference tasks. Dedicated inference benchmarks, meanwhile, focus primarily on isolated kernel generation or performance optimization rather than repository-scale production feature implementation. SWE-Serve provides 53 repository-grounded tasks derived from recent production changes to SGLang, spanning six inference engineering families. Each task executes on either CPU or a single GPU (H100) and is evaluated with hidden functional and regression tests, including, where applicable, end-to-end (E2E) serving tests and calibrated performance gates. Executable no-op and oracle controls, adversarial verifier review, and closed-book execution support task validity and evaluation integrity. Across 11 models and 31 model-effort configurations, the best-performing configuration achieves 75% mean pass@1. SWE-Serve exposes a substantial gap between completing tasks locally and achieving production correctness. On 19 tasks with end-to-end coverage, model-serving E2E tests reject roughly one-third of patches that pass every other test (45.9% under the verifier versus 69.4% with E2E tests excluded from scoring), with pass rate increasing for each model's best-performing configuration. By making the production correctness gap directly measurable, SWE-Serve enables the field to track whether future agents move beyond completing tasks locally to achieving production correctness.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。