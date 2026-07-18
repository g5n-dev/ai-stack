---
title: Self-Distillation Enables Continual Learning
date: 2026-01-28 07:28:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.19897v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:edfd6d13ea8b87a56d7270e1eac34048a7efd18a248ff4e5c5c638a238d0cc0d
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 44
captured_at: '2026-07-18T04:09:30.311520Z'
source_capture_sha256: sha256:1f1e99d006bfa67992f159aefca389ad60f37e63390bda6f42ec65f512d212f8
source_capture_chars_original: 1175
source_publication_excerpt_chars: 1175
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.19897v1](<https://arxiv.org/abs/2601.19897v1>)
- **作者**: Idan Shenfeld, Mehul Damani, Jonas Hübotter, Pulkit Agrawal
- **分类**: cs.LG
- **论文时间**: 2026-01-27T18:59:08Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.19897v1.pdf](<https://arxiv.org/pdf/2601.19897v1.pdf>)

## 来源摘要/节选

> Continual learning, enabling models to acquire new skills and knowledge without degrading existing capabilities, remains a fundamental challenge for foundation models. While on-policy reinforcement learning can reduce forgetting, it requires explicit reward functions that are often unavailable. Learning from expert demonstrations, the primary alternative, is dominated by supervised fine-tuning \(SFT\), which is inherently off-policy. We introduce Self-Distillation Fine-Tuning \(SDFT\), a simple method that enables on-policy learning directly from demonstrations. SDFT leverages in-context learning by using a demonstration-conditioned model as its own teacher, generating on-policy training signals that preserve prior capabilities while acquiring new skills. Across skill learning and knowledge acquisition tasks, SDFT consistently outperforms SFT, achieving higher new-task accuracy while substantially reducing catastrophic forgetting. In sequential learning experiments, SDFT enables a single model to accumulate multiple skills over time without performance regression, establishing on-policy distillation as a practical path to continual learning from demonstrations.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
