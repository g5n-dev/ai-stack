---
title: 'Reasoning Core: A Scalable Procedural Data Generation Suite for Symbolic Pre-training
  and Post-Training'
date: 2026-03-03 23:28:17+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.02208v1
aliases:
- /posts/20260304-arxiv_ai-reasoning-core-a-scalable-procedural-data-generati-0/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:192a6ef23a28b09b14756321a99b18398ba54b62fc3889a3ca49181e60fdcf3f
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 103
captured_at: '2026-07-18T04:26:34.932328Z'
source_capture_sha256: sha256:d3c5e43a60226a4ad6f1c82ca5e310b2d6b8c2788987f733abc2fd7f87d55116
source_capture_chars_original: 1296
source_publication_excerpt_chars: 1296
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02208v1](<https://arxiv.org/abs/2603.02208v1>)
- **作者**: Valentin Lacombe, Valentin Quesnel, Damien Sileo
- **分类**: cs.CL
- **论文时间**: 2026-03-02T18:59:29Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02208v1.pdf](<https://arxiv.org/pdf/2603.02208v1.pdf>)

## 来源摘要/节选

> Training on verifiable symbolic data is a promising way to expand the reasoning frontier of language models beyond what standard pre-training corpora provide. Yet existing procedural generators often rely on fixed puzzles or templates and do not deliver the distributional breadth needed at scale. We introduce Reasoning Core, a scalable suite that procedurally generates verifiable symbolic reasoning data across core formal domains: PDDL planning over randomized domains, first-order logic with equality, context-free grammar parsing and generation, causal reasoning over random Bayesian networks, and systems of equations. Each task is paired with an external solver for rigorous verification and admits continuous difficulty control for curriculum design. Examples can optionally include solver-derived reasoning traces, enabling supervised training from the earliest pre-training stages, and the same interface provides verifiable reward functions for reinforcement learning. Our experiments show that mixing Reasoning Core data into pre-training improves downstream reasoning while preserving, or slightly improving, language modeling quality. Zero-shot evaluations confirm these tasks challenge frontier models such as GPT-5. The code and data are publicly available under the MIT license.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
