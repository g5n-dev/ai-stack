---
title: 'Impermanent: A Live Benchmark for Temporal Generalization in Time Series Forecasting'
date: 2026-03-10 16:09:56+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.08707v1
aliases:
- /posts/20260311-arxiv_ai-impermanent-a-live-benchmark-for-temporal-generali-1/
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:1990681f640c6a47a4a6fc57adfcb9a072695737d33ab583e7a7aba0ca4ca93b
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 84
captured_at: '2026-07-18T04:27:31.441787Z'
source_capture_sha256: sha256:2a8a19f1320aab1090a946a79e154855d23e68dcacf9407c60f4429774cb49b3
source_capture_chars_original: 1641
source_publication_excerpt_chars: 1641
observation_id: obs_fcac03108bb6b665ec176bf1ee320b7261ffefc77b059b05293cca3bee681de0
revision_id: rev_1aa74fd284bea1699684361de1ddd55f1838d0a1686f594518fea153cfa82f85
event_id: evt_08384e8ad7656efc082aed8fe04acabd162465636dc25a6707c3edc958d3cb7c
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-10T00:28:17Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.08707v1](<https://arxiv.org/abs/2603.08707v1>)
- **作者**: Azul Garza, Renée Rosillo, Rodrigo Mendoza-Smith, David Salinas, Andrew Robert Williams, Arjun Ashok, Mononito Goswami, José Martín Juárez
- **分类**: cs.LG
- **论文时间**: 2026-03-09T17:59:00Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.08707v1.pdf](<https://arxiv.org/pdf/2603.08707v1.pdf>)

## 来源摘要/节选

> Recent advances in time-series forecasting increasingly rely on pre-trained foundation-style models. While these models often claim broad generalization, existing evaluation protocols provide limited evidence. Indeed, most current benchmarks use static train-test splits that can easily lead to contamination as foundation models can inadvertently train on test data or perform model selection using test scores, which can inflate performance. We introduce Impermanent, a live benchmark that evaluates forecasting models under open-world temporal change by scoring forecasts sequentially over time on continuously updated data streams, enabling the study of temporal robustness, distributional shift, and performance stability rather than one-off accuracy on a frozen test set. Impermanent is instantiated on GitHub open-source activity, providing a naturally live and highly non-stationary dataset shaped by releases, shifting contributor behavior, platform/tooling changes, and external events. We focus on the top 400 repositories by star count and construct time series from issues opened, pull requests opened, push events, and new stargazers, evaluated over a rolling window with daily updates, alongside standardized protocols and leaderboards for reproducible, ongoing comparison. By shifting evaluation from static accuracy to sustained performance, Impermanent takes a concrete step toward assessing when and whether foundation-level generalization in time-series forecasting can be meaningfully claimed. Code and a live dashboard are available at https://github.com/TimeCopilot/impermanent and https://impermanent.timecopilot.dev.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
