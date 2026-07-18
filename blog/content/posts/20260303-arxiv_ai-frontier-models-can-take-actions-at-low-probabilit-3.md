---
title: Frontier Models Can Take Actions at Low Probabilities
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
external_url: https://arxiv.org/abs/2603.02202v1
aliases:
- /posts/20260304-arxiv_ai-frontier-models-can-take-actions-at-low-probabilit-3/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:ba41eeed7845c6c6efdcb59f3ebfa53e204d0cf1591e4743fdef5fbf008ead7c
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 53
captured_at: '2026-07-18T04:26:23.368833Z'
source_capture_sha256: sha256:c7aea762625595ceee90c066f4ea1b2aa560dd3d33f6a466d53fd40cd63c6248
source_capture_chars_original: 1552
source_publication_excerpt_chars: 1552
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.02202v1](<https://arxiv.org/abs/2603.02202v1>)
- **作者**: Alex Serrano, Wen Xing, David Lindner, Erik Jenner
- **分类**: cs.LG
- **论文时间**: 2026-03-02T18:56:59Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.02202v1.pdf](<https://arxiv.org/pdf/2603.02202v1.pdf>)

## 来源摘要/节选

> Pre-deployment evaluations inspect only a limited sample of model actions. A malicious model seeking to evade oversight could exploit this by randomizing when to "defect": misbehaving so rarely that no malicious actions are observed during evaluation, but often enough that they occur eventually in deployment. But this requires taking actions at very low rates, while maintaining calibration. Are frontier models even capable of that? We prompt the GPT-5, Claude-4.5 and Qwen-3 families to take a target action at low probabilities \(e.g. 0.01%\), either given directly or requiring derivation, and evaluate their calibration \(i.e. whether they perform the target action roughly 1 in 10,000 times when resampling\). We find that frontier models are surprisingly good at this task. If there is a source of entropy in-context \(such as a UUID\), they maintain high calibration at rates lower than 1 in 100,000 actions. Without external entropy, some models can still reach rates lower than 1 in 10,000. When target rates are given, larger models achieve good calibration at lower rates. Yet, when models must derive the optimal target rate themselves, all models fail to achieve calibration without entropy or hint to generate it. Successful low-rate strategies require explicit Chain-of-Thought \(CoT\) reasoning, so malicious models attempting this approach could currently be caught by a CoT monitor. However, scaling trends suggest future evaluations may be unable to rely on models' lack of target rate calibration, especially if CoT is no longer legible.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
