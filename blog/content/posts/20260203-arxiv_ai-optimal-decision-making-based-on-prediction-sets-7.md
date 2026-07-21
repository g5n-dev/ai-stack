---
title: Optimal Decision-Making Based on Prediction Sets
date: 2026-02-03 03:49:30+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2602.00989v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:6b4ac96b4b808a21bdd8409b03be29f9fece00a0dcb0a2d26ac45ef760f6ec51
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 48
captured_at: '2026-07-18T04:10:30.388786Z'
source_capture_sha256: sha256:af78f9e79f20ce16494d8922866e0f8e23181d012496e9febf63262202c72753
source_capture_chars_original: 1107
source_publication_excerpt_chars: 1107
observation_id: obs_4caf6c5076c0b1feb1d22ef1027bac1f2fa9e9fde440e419bc6aba6982f9e144
revision_id: rev_fd6af8e7bea1b873df9eba7c027e02aad7c8e397b2578b212de72c7f659d5dc7
event_id: evt_86754f3793428311fb186a01ad1eb4ad4fd7cd635384e1615af3f5f12523ce26
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-02-03T03:56:50Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2602.00989v1](<https://arxiv.org/abs/2602.00989v1>)
- **作者**: Tao Wang, Edgar Dobriban
- **分类**: stat.ML
- **论文时间**: 2026-02-01T03:02:44Z
- **论文 PDF**: [https://arxiv.org/pdf/2602.00989v1.pdf](<https://arxiv.org/pdf/2602.00989v1.pdf>)

## 来源摘要/节选

> Prediction sets can wrap around any ML model to cover unknown test outcomes with a guaranteed probability. Yet, it remains unclear how to use them optimally for downstream decision-making. Here, we propose a decision-theoretic framework that seeks to minimize the expected loss \(risk\) against a worst-case distribution consistent with the prediction set's coverage guarantee. We first characterize the minimax optimal policy for a fixed prediction set, showing that it balances the worst-case loss inside the set with a penalty for potential losses outside the set. Building on this, we derive the optimal prediction set construction that minimizes the resulting robust risk subject to a coverage constraint. Finally, we introduce Risk-Optimal Conformal Prediction \(ROCP\), a practical algorithm that targets these risk-minimizing sets while maintaining finite-sample distribution-free marginal coverage. Empirical evaluations on medical diagnosis and safety-critical decision-making tasks demonstrate that ROCP reduces critical mistakes compared to baselines, particularly when out-of-set errors are costly.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
