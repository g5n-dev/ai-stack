---
title: "Multi-Expert Routing for Multi-Domain Low-Resource OCR: A Manchu Case Study"
date: 2026-07-16T14:34:01+08:00
draft: false
entry_kind: "auto"
tags: ["cs.CV", "arXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:fac7515b360256b80f8347657f9113d4310e946b285547c066c6c5e9c2780b30"
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2607.14041v1
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2607.14041v1](http://arxiv.org/abs/2607.14041v1)

## 来源摘要/节选

> Historical Manchu OCR must accommodate various visually distinct writing styles, including regular script, running script, and the semi-cursive chancery hand used in palace memorials, despite limited labeled data. We study a multi-expert system that reuses checkpoints from an iterative fine-tuning process as domain specialists and uses a lightweight page-level image classifier to dispatch pages by visual style. When the checkpoint pool lacks a suitable specialist, we train an additional expert for that domain. On three frozen test sets, the routed system matches the selected specialist for each style at two-decimal precision: 0.30 percent CER on regular script, 1.57 percent on memorials, and 4.83 percent on running script. The router achieves 99.3 percent page-level domain accuracy and matches the domain-label oracle at the same precision. Two of the three selected specialists were not trained specifically for their final domain; only the running-script expert was trained with that domain as its target. We report the evaluation protocol, router design, and per-page predictions to make the comparison reproducible.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。