---
title: Long-Horizon Traffic Forecasting via Incident-Aware Conformal Spatio-Temporal
  Transformers
date: 2026-03-18 08:22:04+08:00
draft: false
entry_kind: auto
tags:
- ArXiv
categories:
- 论文
scenarios: []
source: arxiv
description: 当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。
external_url: https://arxiv.org/abs/2603.16857v1
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: abstract
source_snapshot_sha256: sha256:2ef06c15ce575c67babb1f1d2a5b5bb21c4b4107983f5e8a2330eae73fd53435
extractor_version: source-contract-v1
discovery_method: arxiv_api
fetch_status: captured
source_completeness: abstract_only
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
captured_at: '2026-07-18T04:28:45.482788Z'
source_capture_sha256: sha256:bb40b7f187fac5e8c8615c3981f1a26cd5eb528fef5793f7202a867de9e817da
source_capture_chars_original: 1499
source_publication_excerpt_chars: 1499
observation_id: obs_f741f0e96115a7dcceded2e523491b05a205b223c746ce7ac72eba184c6c4054
revision_id: rev_2ecba2a6ec4129b0db8af1e8a4a814b8943c03c4f66b4eafc1ce814b45e471f4
event_id: evt_2aa03634411a0fbf5182943a49eecfdfa13a4ab3b338cd20105c87ba818dfd21
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-03-18T07:02:37Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: arxiv
- **原始来源**: [https://arxiv.org/abs/2603.16857v1](<https://arxiv.org/abs/2603.16857v1>)
- **作者**: Mayur Patil, Qadeer Ahmed, Shawn Midlam-Mohler, Stephanie Marik, Allen Sheldon, Rajeev Chhajer, Nithin Santhanam
- **分类**: cs.LG
- **论文时间**: 2026-03-17T17:58:01Z
- **论文 PDF**: [https://arxiv.org/pdf/2603.16857v1.pdf](<https://arxiv.org/pdf/2603.16857v1.pdf>)

## 来源摘要/节选

> Reliable multi-horizon traffic forecasting is challenging because network conditions are stochastic, incident disruptions are intermittent, and effective spatial dependencies vary across time-of-day patterns. This study is conducted on the Ohio Department of Transportation \(ODOT\) traffic count data and corresponding ODOT crash records. This work utilizes a Spatio-Temporal Transformer \(STT\) model with Adaptive Conformal Prediction \(ACP\) to produce multi-horizon forecasts with calibrated uncertainty. We propose a piecewise Coefficient of Variation \(CV\) strategy that models hour-to-hour traveltime variability using a log-normal distribution, enabling the construction of a per-hour dynamic adjacency matrix. We further perturb edge weights using incident-related severity signals derived from the ODOT crash dataset that comprises incident clearance time, weather conditions, speed violations, work zones, and roadway functional class, to capture localized disruptions and peak/off-peak transitions. This dynamic graph construction replaces a fixed-CV assumption and better represents changing traffic conditions within the forecast window. For validation, we generate extended trips via multi-hour loop runs on the Columbus, Ohio, network in SUMO simulations and apply a Monte Carlo simulation to obtain travel-time distributions for a Vehicle Under Test \(VUT\). Experiments demonstrate improved long-horizon accuracy and well-calibrated prediction intervals compared to other baseline methods.

## 来源说明

当前只保存了官方论文摘要，不代表论文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
