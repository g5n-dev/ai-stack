---
title: "Can LLMs Reason About Runtime Behavior? A Repository-Level Dynamic Benchmark"
date: 2026-09-24T23:09:16+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.SE", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9b0e43e82424f47c18c1fb632672a142836f91d5bcee93665992125097df7dea"
source_payload_sha256: "sha256:2b3b5bcc96848e5377032c6a21db1365c76d6ee0ce615d07baac6faa1fb7d523"
observation_id: obs_abbef313fdcee3dc2c10ddf4d0dafcb7cddac8501765e2e7046c6d8460e3a3b4
event_id: evt_0ab2e9b9f9598eab2efb067501415f7314978ffc898a17b91e74b113a04fa148
revision_id: rev_c88301232116a543fbc329e6c057f44f096b2b6de551188f0092df5fe88d5922
source_published_at: 2026-09-23T17:46:50Z
first_seen_at: 2026-09-24T15:20:18Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 76
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2609.28449v1
parent_observation_id: null
last_seen_at: 2026-09-24T15:05:35.417245Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2609.28449v1](http://arxiv.org/abs/2609.28449v1)
- **发布域名**: arxiv.org
- **分类**: cs.SE
- **作者**: Hamed Taherkhani、Mohammad Abdollahi、Melika Sepidband 等

## 来源摘要/节选

> Large language models (LLMs) are increasingly used in coding tasks, but their ability to reason about code execution remains unclear. Existing repository-level QA benchmarks mainly evaluate static code understanding and often rely on LLM-based evaluation, while execution-reasoning benchmarks are mostly limited to snippets or functions. We introduce SWE-Flux, a repository-level benchmark for dynamic execution reasoning containing 480 execution-grounded instances across 12 real Python repositories, with gold answers automatically harvested from instrumented test executions rather than written manually or judged by LLMs. The benchmark covers singletest and multi-test questions over control flow, loops, program state, dataflow, exceptions, and program invariants. Evaluating five LLMs shows that this task remains challenging. The best model achieves only 37% accuracy. Models perform better on localized behavior such as invariants, intra-procedural control flow, exceptions, and simple loops, but struggle with dataflow, inter-procedural execution, precise state reasoning, and suite-level aggregation. Finally, we show that the oracle-harvesting pipeline can generate fresh benchmark variants using input perturbation. It successfully harvests valid variants for almost 90% of the selected instances, and the resulting variants are substantially more challenging for the evaluated models.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。