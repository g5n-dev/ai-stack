---
title: 'SplineFlow: Flow Matching for Dynamical Systems with B-Spline Interpolants'
date: 2026-02-02 02:57:13+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2601.23072v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:50a10a1f21f3b29d76bd1d995b815e49432e2253be2931b78941b6fbf2455270
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 74
captured_at: '2026-07-18T04:10:19.257843Z'
source_capture_sha256: sha256:b3ca36550e69ed21f2cb5934318ee9c16d0cf33986422e53d90571e4747262b4
source_capture_chars_original: 1264
source_publication_excerpt_chars: 1264
observation_id: obs_7b35ea33123c2080bd46281a823417422da1c0ac07de85a3e9d9af44f229cd18
revision_id: rev_1c76bceffdb091c0b6ac8e5ee320d86773f86c4b001782f0b6efa83841d2ba7b
event_id: evt_456a3ab4a19e1bd4ecdc1c8b9f843f2f7c60bf26e344da5e8f62d0a21b97ba2a
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-02T03:02:18Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2601.23072v1](<https://arxiv.org/abs/2601.23072v1>)
- **作者**: Santanu Subhash Rathod, Pietro Liò, Xiao Zhang
- **分类**: cs.LG
- **论文时间**: 2026-01-30T15:19:48Z
- **论文 PDF**: [https://arxiv.org/pdf/2601.23072v1.pdf](<https://arxiv.org/pdf/2601.23072v1.pdf>)

## 来源摘要/节选

> Flow matching is a scalable generative framework for characterizing continuous normalizing flows with wide-range applications. However, current state-of-the-art methods are not well-suited for modeling dynamical systems, as they construct conditional paths using linear interpolants that may not capture the underlying state evolution, especially when learning higher-order dynamics from irregular sampled observations. Constructing unified paths that satisfy multi-marginal constraints across observations is challenging, since naïve higher-order polynomials tend to be unstable and oscillatory. We introduce SplineFlow, a theoretically grounded flow matching algorithm that jointly models conditional paths across observations via B-spline interpolation. Specifically, SplineFlow exploits the smoothness and stability of B-spline bases to learn the complex underlying dynamics in a structured manner while ensuring the multi-marginal requirements are met. Comprehensive experiments across various deterministic and stochastic dynamical systems of varying complexity, as well as on cellular trajectory inference tasks, demonstrate the strong improvement of SplineFlow over existing baselines. Our code is available at: https://github.com/santanurathod/SplineFlow.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
