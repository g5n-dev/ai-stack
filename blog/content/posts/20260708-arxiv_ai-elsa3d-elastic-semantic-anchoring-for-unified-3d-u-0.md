---
title: 'ELSA3D: Elastic Semantic Anchoring for Unified 3D Understanding and Generation'
date: 2026-07-08 22:24:27+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2607.06565v1
aliases:
- /posts/20260709-arxiv_ai-elsa3d-elastic-semantic-anchoring-for-unified-3d-u-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:e7638c54bdf58d697c3f18cc6ec2b207fed3ea562f1499653e05153aa962ae79
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 78
captured_at: '2026-07-18T04:30:25.647174Z'
source_capture_sha256: sha256:196bfa6cfc6c96ce96b6e441b4920454b348d57bfd12482c0ccb24b400473b4d
source_capture_chars_original: 1380
source_publication_excerpt_chars: 1380
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2607.06565v1](<https://arxiv.org/abs/2607.06565v1>)
- **作者**: Tianjiao Yu, Xinzhuo Li, Yifan Shen, Onkar Susladkar, Yuanzhe Liu, Xiaona Zhou, Ismini Lourentzou
- **分类**: cs.CV
- **论文时间**: 2026-07-07T17:59:50Z
- **论文 PDF**: [https://arxiv.org/pdf/2607.06565v1.pdf](<https://arxiv.org/pdf/2607.06565v1.pdf>)

## 来源摘要/节选

> Unified 3D foundation models aspire to generate 3D assets and reason about them in language within a single backbone, but their text-3D interaction remains largely implicit. Existing methods concatenate text and 3D tokens into a flat sequence and rely on self-attention, collapsing coarse structural cues and fine geometric details into one undifferentiated representation. We introduce ELSA3D, a unified 3D model that addresses this with elastic semantic anchoring, structuring language and geometric reasoning jointly along matched abstraction scales. ELSA3D represents geometry with a scale-aware octree tokenizer and introduces Anchor Tokens, sparse cross-modal units that select semantic cues, route them to the most relevant 3D scale, retrieve scale-specific geometric evidence, and write the fused signal back into the unified representation, keeping interaction sparse yet precise. A lightweight per-block router makes both computation and reasoning elastic, choosing which text tokens instantiate anchors at which geometric scale so that cross-modal capacity concentrates where alignment is most needed. ELSA3D achieves state-of-the-art performance across image-to-3D generation, text-to-3D generation, and 3D captioning, outperforming the strongest unified baseline while roughly halving FLOPs and inference latency relative to the non-elastic version of the same model.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
