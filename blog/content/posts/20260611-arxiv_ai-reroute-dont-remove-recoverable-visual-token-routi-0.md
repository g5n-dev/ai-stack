---
title: 'Reroute, Don''t Remove: Recoverable Visual Token Routing for Vision-Language
  Models'
date: 2026-06-11 23:39:46+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2606.12412v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:194e172eaaed4e156ee191c437fa8799599cb1138e1c6b485ace553e2e445ae4
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 82
captured_at: '2026-07-18T04:30:02.047374Z'
source_capture_sha256: sha256:a86aa9a91605ff9491277b2b9ace1bc10ae96baf9d123928383a116866c7745c
source_capture_chars_original: 1380
source_publication_excerpt_chars: 1380
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2606.12412v1](<https://arxiv.org/abs/2606.12412v1>)
- **作者**: Cheng-Yu Yang, Shao-Yuan Lo, Yu-Lun Liu
- **分类**: cs.CV
- **论文时间**: 2026-06-10T17:59:57Z
- **论文 PDF**: [https://arxiv.org/pdf/2606.12412v1.pdf](<https://arxiv.org/pdf/2606.12412v1.pdf>)

## 来源摘要/节选

> Vision-language models \(VLMs\) project images into hundreds to thousands of visual tokens, making decoder inference expensive in both attention computation and KV-cache memory. Existing visual-token reduction methods largely follow a rank-and-remove paradigm: they score visual tokens, keep a compact subset, and permanently discard the rest. We show that this irreversible action is fragile because visual-token importance changes across decoder depth; tokens ranked low at one stage may become relevant in later layers, especially for grounding-sensitive queries. We propose Reroute, a training-free plug-in that replaces removal with recoverable routing. At each routing stage, selected vision tokens pass through decoder blocks, while deferred tokens bypass the stage and re-enter the candidate pool at the next routing decision. Reroute reuses existing attention-score ranking rules and stage-wise schedules, preserving the theoretical TFLOPs and KV-cache budget class of the pruning method it augments. Across FastV, PDrop, and Nüwa variants on LLaVA-1.5 and Qwen backbones, reroute improves grounding under aggressive token reduction while maintaining general VQA performance. These results suggest that VLM token reduction should not be viewed only as irreversible pruning, but also as recoverable routing. The code can be found here: https://github.com/elmma/mllm-reroute/

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
