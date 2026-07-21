---
title: Step-resolved data attribution for looped transformers
date: 2026-02-11 22:09:57+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.10097v1
aliases:
- /posts/20260212-arxiv_ai-step-resolved-data-attribution-for-looped-transfor-4/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:a0eed218992e1590f9e3d75a8d6ce4ef33c613fe1628a44792d3b0673d817a2e
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 54
captured_at: '2026-07-18T04:14:51.451682Z'
source_capture_sha256: sha256:43641142b9060f72918dc409be880cc006dc1dc38c0bcb266016a589e490012b
source_capture_chars_original: 1024
source_publication_excerpt_chars: 1024
observation_id: obs_a34a9a7f96ef4aaf5860281f88f3d62cf5b6254d32fc90ee4c2aabf267b890a8
revision_id: rev_295092f584efbe390832ef5ceb860b60852e96f4a15fce026193437c88c0d2a5
event_id: evt_9c34f0228d9ac009c994fb96fdd65a90031df1e36ba4a36829f56854b6994acb
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-11T08:34:35Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.10097v1](<https://arxiv.org/abs/2602.10097v1>)
- **作者**: Georgios Kaissis, David Mildenberger, Juan Felipe Gomez, Martin J. Menten, Eleni Triantafillou
- **分类**: cs.LG
- **论文时间**: 2026-02-10T18:57:53Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.10097v1.pdf](<https://arxiv.org/pdf/2602.10097v1.pdf>)

## 来源摘要/节选

> We study how individual training examples shape the internal computation of looped transformers, where a shared block is applied for $τ$ recurrent iterations to enable latent reasoning. Existing training-data influence estimators such as TracIn yield a single scalar score that aggregates over all loop iterations, obscuring when during the recurrent computation a training example matters. We introduce \\textit\{Step-Decomposed Influence \(SDI\)\}, which decomposes TracIn into a length-$τ$ influence trajectory by unrolling the recurrent computation graph and attributing influence to specific loop iterations. To make SDI practical at transformer scale, we propose a TensorSketch implementation that never materialises per-example gradients. Experiments on looped GPT-style models and algorithmic reasoning tasks show that SDI scales excellently, matches full-gradient baselines with low error and supports a broad range of data attribution and interpretability tasks with per-step insights into the latent reasoning process.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
