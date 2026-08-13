---
title: "Large Language Model-Driven Small-Capitalization Trading: Integrating Financial News Sentiment, Macroeconomic Indicators, and Technical Signals"
date: 2026-08-13T20:02:18+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "q-fin.PM", "ArXiv", "来源快报"]
categories: []
source: "arxiv"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "abstract"
source_snapshot_sha256: "sha256:8c3f9e37230bb5e640bfd725023b409116603f93ee60f48dc9e4b693c87906c3"
source_payload_sha256: "sha256:3132e70bb6560f1611529de2ef68a01fcb835b7de315ec6c56634325e478f1be"
observation_id: obs_f60b8c7e00bb975427f371101e4987e0b2ba430ff7c3e17d8d3639edf4eba8b8
event_id: evt_ef6a3d0f40bb33e6de17a24a61ab45a5182a074994e55dd82f24aba48d64a766
revision_id: rev_866b1bf6be841429994210ecd9820562fe36256ec6e4e90cc716ec5f80673c1e
source_published_at: 2026-08-12T17:28:03Z
first_seen_at: 2026-08-13T12:16:49Z
timestamp_confidence: publisher
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "arxiv_api"
source_completeness: "abstract_only"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 143
description: "当前保存的是来源摘要，不代表论文全文。请以原始来源为准。"
external_url: http://arxiv.org/abs/2608.12283v1
parent_observation_id: null
last_seen_at: 2026-08-13T11:59:15.841536Z
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [http://arxiv.org/abs/2608.12283v1](http://arxiv.org/abs/2608.12283v1)
- **发布域名**: arxiv.org
- **分类**: q-fin.PM
- **作者**: Alireza Kargarzadeh、Nariman Khaledian、Navid Parvini 等

## 来源摘要/节选

> Large language models can extract richer signals from financial news than fixed sentiment lexicons, and recent work has explored feeding such signals into portfolio construction. We study an uncertainty-aware construction that feeds model-predicted risk -- decomposed into aleatoric and epistemic components -- directly into the covariance matrix of portfolio allocators, rather than treating portfolio risk as fixed or adjusting only expected returns. We evaluate the pipeline on Russell 2000 equities under three stock-selection regimes: a pure-alpha trigger that isolates abnormal stock moves not explained by macro indicators, a pure-beta trigger that captures macro-indicator moves before the stock itself fires, and a beta trigger in which both channels agree. Across the full holding-period grid, the separated pure-alpha and pure-beta legs usually dominate the beta intersection on Sharpe and return. Two horizons are especially informative. At one day, pure beta can work under low and moderate transaction costs because it captures immediate lead-lag spillovers from liquid macro and sector indicators into exposed small-cap stocks, but this advantage disappears at 100 bps when turnover and microstructure noise dominate. At 40 days, pure beta works for a different reason: slower macro repricing overtakes the firm-specific pure-alpha channel. The strongest conservative row is pure beta with GPT-4o mini sentiment, a Student-t target, a 40-day holding period, and risk parity allocation, reaching Sharpe 2.33 at 100 bps. The results suggest that stock-selection regime and allocator choice matter at least as much as the sentiment model, and that separating firm-specific and macro-exposure triggers is more informative than requiring both to fire simultaneously.

## 来源说明

当前保存的是来源摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。