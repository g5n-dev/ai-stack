---
title: "Can Large Language Models Recover Semantic Optimization Opportunities That Compilers Miss?"
date: 2026-08-06T06:23:59+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "cs.PL", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:9ddf00e1c686c3f1644f29ef913232e3de86d1e60a0badf68a74611b188a431e"
source_payload_sha256: "sha256:6e207b134386a7c923f823c5305ca73de3a5b2fe02f71e68869303fd90986cf7"
observation_id: obs_5d21dbc50a735f429dab7b9b7b3579486ba316b9aa116125691386d8ecdbb220
event_id: evt_31e6c8b06da9cfe70599b7b94560822f574e0b7b0282ab7da6c40c40f15a6179
revision_id: rev_845e7765b3c06c34991569b519533e0be8b35e87ae947b7fe1427e4f8d1ef13b
source_published_at: 2026-08-04T17:47:25Z
first_seen_at: 2026-08-05T22:20:23.935778Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.03983v1
parent_observation_id: null
last_seen_at: 2026-08-05T22:20:23.935778Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.03983v1](http://arxiv.org/abs/2608.03983v1)
- **发布域名**: arxiv.org
- **分类**: cs.PL
- **作者**: Hailong Jiang、Feng Yu、Emran Hossain 等

## 来源摘要/节选

> Optimizing compilers miss profitable transformations when their enabling semantics are absent from the analyzed program representation. We ask whether large language models (LLMs) can recover such semantics from heterogeneous C/C++ context and realize them as validated, contract-preserving artifacts. We introduce SeGaBench, an executable benchmark containing 100 synthetic and 20 source-backed cases spanning low-level assumptions, data-structure invariants, and high-level semantic lifting. Each case includes hidden enabling semantics, an oracle artifact, correctness and semantic validators, and a reproducible performance protocol. We evaluate five LLMs using five independent responses per case. The strongest model produces correct artifacts in 94.8% of responses, achieves at least 1.05x speedup in 83.3%, and obtains a performance success on 93.3% of cases. Nevertheless, correct artifacts often close only part of the oracle gap. These results show that LLMs can complement compiler analysis as speculative semantic proposers, provided that their artifacts are validated and evaluated.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。